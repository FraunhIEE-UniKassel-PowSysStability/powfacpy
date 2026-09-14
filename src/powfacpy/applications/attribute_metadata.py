"""Work with PowerFactory attributes through the names shown in the GUI.

PowerFactory stores every attribute under a terse code (``pgini``, ``i_mot``,
``iexchange``) and many attributes are *enumerations* whose value is an opaque
integer (``ElmSym.i_mot`` is ``0`` / ``1`` / ``2`` for Generator / Motor /
Condenser). `AttributeMetadata` bridges that gap:

  - `set_enum` / `set_attributes` - write an enumeration by the option name shown
    in the dialog (``machine.i_mot = "Motor"``), not the integer;
  - `enum_options` / `enum_name` / `enum_code` - list an enumeration's options and
    translate between code and name;
  - `label` - the GUI label of an attribute (``ElmSym`` / ``pgini`` -> "Dispatch");
  - `describe` - a small table of an object's attributes with labels and decoded
    values.

The same enum-name translation is available directly on
``ActiveProject.set_attr(obj, params, resolve_enum_names=True)``.

Where the names come from: PowerFactory ships a SQLite database of every GUI
string (``<install>/localisation/en-GB/data.db``, one table ``Message(lang,
class, param, message)`` - the same file `DigsilentLibrary` uses for folder
names). Enum options are resolved from, in order: the live attribute description
(``obj.GetAttributeDescription`` / ``app.GetAttributeDescription``), the same
string in that database, then the database's ``<attr>_<code>`` option rows. The
database is needed only for that last source - PowerFactory's API returns inline
option lists (``ElmVsc.i_acdc`` -> ``"Control mode:Vac-phi:Vdc-phi:..."``) but
just the label for many enums (``i_mot``, ``i_net``, ``imode``, ...). If the
database cannot be read, those fall back to "options unknown" (one warning) and
everything else keeps working.

Scope: this covers **integer-coded** enumerations. String-coded ones
(``ElmSym.av_mode`` = ``"vdroop"``, ``ElmGenstat.mode_inp`` = ``"PQ"``) already
read and write as their string, so `enum_options` returns ``{}`` for them and
`set_attributes` passes the string through unchanged. A few enums (``iexchange``)
have their options in neither the API nor the database and also return ``{}`` -
pass the integer code for those.
"""

from __future__ import annotations

import re
import sqlite3
from functools import cached_property, lru_cache
from pathlib import Path
from warnings import warn

import pandas as pd

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.exceptions import PFEnumValueError
from powfacpy.pf_classes.protocols import PFApp, PFGeneral


# --------------------------------------------------------------------------- #
# database access (module-level, cached so the ~30 MB file is read at most once)
# --------------------------------------------------------------------------- #

#: `param` of an option row: ``<attr>_<code>`` (e.g. ``i_mot_2``).
_OPTION_ROW = re.compile(r"^(?P<attr>.+)_(?P<code>\d+)$")
#: an inline option carrying an explicit code, e.g. ``&2&isolated``.
_EXPLICIT_CODE = re.compile(r"^&(?P<code>\d+)&(?P<label>.*)$")


@lru_cache(maxsize=4)
def _read_localisation_db(path: str) -> dict[tuple[str, str], str]:
    """`{(class, param): message}` for the English rows of a localisation database.

    Cached on the path string. Raises `OSError` / `sqlite3.Error` on failure; the
    caller decides whether to warn and fall back.
    """
    with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as connection:
        rows = connection.execute(
            "SELECT class, param, message FROM Message WHERE lang = 'en'"
        ).fetchall()
    return {(class_name, param): message for class_name, param, message in rows}


def _strip_marker(text: str) -> str:
    """Drop PowerFactory's leading ``~`` (translatable-string marker) and trailing
    ``|<abbreviation>`` (column-header short form)."""
    text = text.strip()
    if text.startswith("~"):
        text = text[1:]
    return text.split("|", 1)[0].strip()


def _parse_inline_options(description: str | None) -> dict[int, str]:
    """Parse ``"Label:opt0:opt1:..."`` (optionally ``"...:&2&opt:&5&opt"``).

    Returns ``{}`` unless the string has at least two colon-separated option
    segments that look like enum entries (short, no sentence punctuation), so a
    prose description that happens to contain a colon is not misread.
    """
    if not description or ":" not in description:
        return {}
    label, *raw_options = description.split(":")
    if len(raw_options) < 2:
        return {}
    # the last option may carry the label's trailing "|abbreviation"
    raw_options[-1] = raw_options[-1].split("|", 1)[0]
    raw_options = [option.strip() for option in raw_options if option.strip()]

    explicit = [_EXPLICIT_CODE.match(option) for option in raw_options]
    if all(explicit):
        return {
            int(match.group("code")): _strip_marker(match.group("label"))
            for match in explicit
        }
    if any(explicit):  # mixed - malformed, don't guess
        return {}
    if any(len(option) > 40 or option.endswith((".", "!")) for option in raw_options):
        return {}  # looks like prose, not an enum
    return {index: _strip_marker(option) for index, option in enumerate(raw_options)}


# --------------------------------------------------------------------------- #
# interface
# --------------------------------------------------------------------------- #


class AttributeMetadata(ApplicationBase):
    """Read and write PowerFactory attributes by their GUI names.

    Example:
        ```python
        meta = AttributeMetadata(app)

        meta.set_enum(machine, "i_mot", "Motor")          # machine.i_mot = 1
        meta.set_attributes(controller, {"i_net": "Power-Frequency Control", "psetp": 0.0})

        meta.enum_options("ElmSym", "i_mot")              # {0: 'Generator', 1: 'Motor', 2: 'Condenser'}
        meta.enum_name(machine, "i_mot", 1)               # 'Motor'
        meta.enum_code("ElmSecctrl", "i_net", "Power-Frequency Control")  # 1

        meta.label("ElmSym", "pgini")                     # 'Dispatch'
        meta.describe(machine, ["i_mot", "pgini"])        # a small DataFrame
        ```

    Every lookup accepts either a PowerFactory object (uses its class and its live
    `GetAttributeDescription`) or a class name string (uses
    `app.GetAttributeDescription`).
    """

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)
        self._db_unavailable_warned = False

    # ---- database ------------------------------------------------------- #
    @cached_property
    def localisation_db_path(self) -> Path:
        """Path of PowerFactory's English GUI-string database."""
        return (
            Path(self.app.GetInstallationDirectory())
            / "localisation"
            / "en-GB"
            / "data.db"
        )

    @property
    def _db(self) -> dict[tuple[str, str], str]:
        """The localisation table as `{(class, param): message}`, or `{}` if it
        cannot be read (warns once)."""
        try:
            return _read_localisation_db(str(self.localisation_db_path))
        except (OSError, sqlite3.Error) as error:
            if not self._db_unavailable_warned:
                warn(
                    f"Could not read the PowerFactory GUI-string database at "
                    f"'{self.localisation_db_path}' ({error}); enum options that are "
                    f"not in the live attribute description are unavailable.",
                    RuntimeWarning,
                )
                self._db_unavailable_warned = True
            return {}

    # ---- labels ------------------------------------------------------- #
    def label(
        self, obj_or_class: PFGeneral | str, attr: str, *, short: bool = False
    ) -> str | None:
        """The GUI label of an attribute (e.g. `ElmSym` / `pgini` -> "Dispatch").

        `short=True` returns the abbreviated column-header form where one exists.
        Returns `None` if the attribute has no known label.
        """
        description = self._description(obj_or_class, attr, short=short)
        if description is None:
            class_name = self._class_name(obj_or_class)
            description = self._db.get((class_name, attr))
        if not description:
            return None
        # drop any inline option list; the label may still carry "~" and "|abbrev"
        full = description.partition(":")[0].lstrip("~")
        if "|" in full:
            long_form, short_form = full.split("|", 1)
            return short_form.strip() if short else long_form.strip()
        return full.strip()

    # ---- enums ------------------------------------------------------- #
    def enum_options(
        self, obj_or_class: PFGeneral | str, attr: str
    ) -> dict[int, str]:
        """`{code: name}` for an enumeration attribute, or `{}` if the attribute is
        not a known integer-coded enumeration.

        Merges the live/API description, the same string in the database, and the
        database's `<attr>_<code>` option rows (used only when `<attr>_0` exists
        and the codes run contiguously from 0).
        """
        class_name = self._class_name(obj_or_class)

        for description in (
            self._description(obj_or_class, attr),
            self._db.get((class_name, attr)),
        ):
            options = _parse_inline_options(description)
            if options:
                return options

        return self._option_rows(class_name, attr)

    def enum_name(
        self, obj_or_class: PFGeneral | str, attr: str, code: int
    ) -> str:
        """The option name for an integer `code`. Falls back to `str(code)` if the
        options are unknown; raises `PFEnumValueError` if they are known but do not
        contain `code`."""
        options = self.enum_options(obj_or_class, attr)
        if not options:
            return str(code)
        try:
            return options[int(code)]
        except (KeyError, ValueError):
            raise PFEnumValueError(
                self._class_name(obj_or_class), attr, code, options
            )

    def enum_code(
        self, obj_or_class: PFGeneral | str, attr: str, value: int | str
    ) -> int:
        """The integer code for an option `value` (its name, or an int / numeric
        string passed straight through).

        Names match case-insensitively and ignore a leading `~`. Raises
        `PFEnumValueError` if `value` is a string that is not one of the options
        (and the options are known)."""
        if isinstance(value, int):
            return value
        text = str(value).strip()
        if text.lstrip("-").isdigit():
            return int(text)
        options = self.enum_options(obj_or_class, attr)
        wanted = text.lstrip("~").casefold()
        for code, name in options.items():
            if name.casefold() == wanted:
                return code
        if not options:
            raise PFEnumValueError(
                self._class_name(obj_or_class),
                attr,
                f"{value} (no option names known for this attribute - pass the "
                f"integer code)",
                options,
            )
        raise PFEnumValueError(self._class_name(obj_or_class), attr, value, options)

    # ---- writing --------------------------------------------------- #
    def set_enum(
        self, obj: PFGeneral, attr: str, value: int | str
    ) -> None:
        """`SetAttribute(attr, ...)` with `value` given as an option name or code."""
        obj.SetAttribute(attr, self.enum_code(obj, attr, value))

    def set_attributes(
        self,
        obj: PFGeneral | str,
        params: dict,
        parent_folder: PFGeneral | str | None = None,
    ) -> None:
        """Like `ActiveProject.set_attr`, but a string value for an enumeration
        attribute is translated to its integer code first.

        A string value whose attribute is not a known enumeration is written
        unchanged, so this is a safe drop-in. `ActiveProject.set_attr(obj, params,
        resolve_enum_names=True)` does the same thing.
        """
        obj = self.act_prj._handle_single_pf_object_or_path_input(
            obj, parent_folder=parent_folder
        )
        self.act_prj.set_attr(obj, self.resolve_enum_names(obj, params))

    def resolve_enum_names(self, obj: PFGeneral, params: dict) -> dict:
        """Return `params` with every string value that names an enumeration option
        replaced by its integer code (other values untouched).

        Used by `set_attributes` and by `ActiveProject.set_attr(...,
        resolve_enum_names=True)`.
        """
        resolved = {}
        for attr, value in params.items():
            if isinstance(value, str) and self.enum_options(obj, attr):
                resolved[attr] = self.enum_code(obj, attr, value)
            else:
                resolved[attr] = value
        return resolved

    # ---- describe ------------------------------------------------- #
    def describe(
        self, obj: PFGeneral, attrs: list[str]
    ) -> pd.DataFrame:
        """A table (`attr` index) with the GUI `label`, the raw `value`, and the
        decoded `enum_name` (``None`` for non-enum attributes) of each attribute.

        Handy for an at-a-glance look at an object in a notebook.
        """
        attrs = list(attrs)
        labels, values, names = [], [], []
        for attr in attrs:
            value = obj.GetAttribute(attr)
            options = self.enum_options(obj, attr)
            name = None
            if options and isinstance(value, (int, float)):
                value = int(value)  # enum codes come back as float from the API
                name = options.get(value)
            labels.append(self.label(obj, attr))
            values.append(value)
            names.append(name)
        return pd.DataFrame(
            {
                "label": labels,
                "value": pd.Series(values, index=attrs, dtype=object),
                "enum_name": names,
            },
            index=attrs,
        )

    # ---- internals ------------------------------------------------- #
    def _class_name(self, obj_or_class: PFGeneral | str) -> str:
        return (
            obj_or_class
            if isinstance(obj_or_class, str)
            else obj_or_class.GetClassName()
        )

    def _description(
        self, obj_or_class: PFGeneral | str, attr: str, *, short: bool = False
    ) -> str | None:
        """The live attribute description, from the object or `app`, or `None`."""
        flag = 1 if short else 0
        try:
            if isinstance(obj_or_class, str):
                description = self.app.GetAttributeDescription(
                    obj_or_class, attr, flag
                )
            else:
                description = obj_or_class.GetAttributeDescription(attr, flag)
        except (AttributeError, RuntimeError, TypeError):
            return None
        return description or None

    def _option_rows(self, class_name: str, attr: str) -> dict[int, str]:
        """Enum options from the database's ``<attr>_<code>`` rows.

        Only used when the base ``<attr>`` row exists without inline options and
        the codes run contiguously from 0 (so result-variable siblings such as
        ``loading_1`` / ``loading_2`` are not mistaken for enum options).
        """
        database = self._db
        if not database or (class_name, attr) not in database:
            return {}
        if ":" in (database.get((class_name, attr)) or ""):
            return {}
        options: dict[int, str] = {}
        for (row_class, param), message in database.items():
            if row_class != class_name:
                continue
            match = _OPTION_ROW.match(param)
            if match and match.group("attr") == attr:
                options[int(match.group("code"))] = _strip_marker(message)
        if not options or set(options) != set(range(len(options))):
            return {}
        return options
