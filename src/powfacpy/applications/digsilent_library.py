"""Navigate the global DIgSILENT library with the folder names shown in the GUI.

PowerFactory's built-in ("system") library folders have coded ``loc_name``s -
``Templ``, ``TemplGfc``, ``TemplPv`` - while the GUI (and the documentation)
shows translated names like ``Templates`` / ``Grid-forming Converters``. The
Python API only accepts the coded names, so a GUI-style path such as
``r"Templates\\Grid-forming Converters"`` cannot be resolved directly.

`DigsilentLibrary` bridges the two using PowerFactory's own localisation
database (``<install>/localisation/en-GB/data.db``), so no hand-maintained
mapping is needed and user-created subfolders (whose ``loc_name`` already is the
displayed name) just work.
"""

from __future__ import annotations

import sqlite3
from functools import cached_property
from pathlib import Path
from re import split as _re_split
from warnings import warn

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.exceptions import PFInterfaceError
from powfacpy.pf_classes.protocols import (
    IntFolder,
    IntLibrary,
    IntTemplate,
    PFApp,
    PFGeneral,
)

#: Used only if the localisation database cannot be read. Covers the
#: ``Templates`` branch (the one powfacpy needs); everything else then falls
#: back to the literal ``loc_name``.
_FALLBACK_FOLDER_NAMES: dict[str, str] = {
    "Templ": "Templates",
    "TemplGfc": "Grid-forming Converters",
    "TemplPv": "Photovoltaic",
    "TemplWind": "Wind Turbines",
    "TemplBess": "Storage Systems",
    "TemplVsd": "Variable Speed Drives",
    "TemplPlantCtrl": "Plant Controllers",
    "TemplDer": "Distributed Energy Resources",
    "TemplPp": "Steam/Gas/Diesel Power Plants",
    "TemplLod": "Loads",
    "TemplHvdc": "HVDC",
    "TemplFacts": "FACTS",
}


class DigsilentLibrary(ApplicationBase):
    """Interface to the global DIgSILENT library, addressed by GUI folder names.

    Example:
        ```python
        lib = DigsilentLibrary(app)
        gfc = lib.get_folder(r"Templates\\Grid-forming Converters")
        template = lib.get_template(
            r"Templates\\Grid-forming Converters\\WECC REGFM_A1 Droop Inverter - Storage"
        )
        ```
    """

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)

    # ------------------------------------------------------------------ #
    # localisation ("skey") translations
    # ------------------------------------------------------------------ #
    @cached_property
    def localisation_db_path(self) -> Path:
        """Path of PowerFactory's English localisation database."""
        return (
            Path(self.app.GetInstallationDirectory())
            / "localisation"
            / "en-GB"
            / "data.db"
        )

    @cached_property
    def folder_name_translations(self) -> dict[str, str]:
        """`{loc_name: displayed_name}` for the built-in (system) library folders.

        Read from `localisation_db_path`; on any failure, falls back to
        `_FALLBACK_FOLDER_NAMES` and warns.
        """
        path = self.localisation_db_path
        try:
            with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as con:
                rows = con.execute(
                    "SELECT param, message FROM Message "
                    "WHERE class = 'IntFolder' AND param LIKE 'skey%'"
                ).fetchall()
            return {param[len("skey") :]: message for param, message in rows}
        except (sqlite3.Error, OSError) as error:
            warn(
                f"Could not read the PowerFactory localisation database at '{path}' "
                f"({error}); falling back to a built-in name table (Templates branch only).",
                RuntimeWarning,
            )
            return dict(_FALLBACK_FOLDER_NAMES)

    def gui_name(self, folder: PFGeneral | str) -> str:
        """The name shown in the GUI for a library folder (or its `loc_name`).

        Args:
            folder: a PF folder object, or a `loc_name` string.
        """
        loc_name = folder if isinstance(folder, str) else folder.loc_name
        return self.folder_name_translations.get(loc_name, loc_name)

    # ------------------------------------------------------------------ #
    # navigation
    # ------------------------------------------------------------------ #
    @property
    def root(self) -> IntLibrary:
        """The global library (`app.GetGlobalLibrary()`)."""
        return self.app.GetGlobalLibrary()

    def get_object(
        self, display_path: str, error_if_non_existent: bool = True
    ) -> PFGeneral | None:
        """Resolve a GUI-style path under the global library.

        Each path segment is matched against the child objects' displayed names
        (translated `loc_name`) and, as a fallback, their literal `loc_name`.
        `"\\"` and `"/"` are both accepted as separators.

        Args:
            display_path: e.g. `r"Templates\\Grid-forming Converters"`. Empty
                string / `"\\"` returns the library root.
            error_if_non_existent: raise if a segment cannot be resolved;
                otherwise return None.
        """
        node: PFGeneral = self.root
        for segment in [s for s in _re_split(r"[\\/]", display_path) if s]:
            match = self._child_by_name(node, segment)
            if match is None:
                if not error_if_non_existent:
                    return None
                raise PFInterfaceError(
                    f"'{segment}' not found under '{self.gui_path(node)}'. "
                    f"Available: {sorted(self.list_contents(self.gui_path(node)))}."
                )
            node = match
        return node

    def __getitem__(self, display_path: str) -> PFGeneral:
        return self.get_object(display_path)

    def get_folder(
        self, display_path: str, error_if_non_existent: bool = True
    ) -> IntFolder | None:
        """`get_object`, asserting the result is a folder."""
        return self._get_of_class(
            display_path, ("IntFolder", "IntPrjfolder"), error_if_non_existent
        )

    def get_template(
        self, display_path: str, error_if_non_existent: bool = True
    ) -> IntTemplate | None:
        """`get_object`, asserting the result is an `IntTemplate`."""
        return self._get_of_class(display_path, ("IntTemplate",), error_if_non_existent)

    def list_contents(
        self, display_path: str = "", classes: tuple[str, ...] | None = None
    ) -> dict[str, PFGeneral]:
        """`{displayed_name: object}` of the children of the folder at `display_path`.

        Args:
            display_path: folder to list (default: the library root).
            classes: keep only these PF class names (default: all).
        """
        parent = self.get_object(display_path)
        result: dict[str, PFGeneral] = {}
        for child in parent.GetContents():
            if classes and child.GetClassName() not in classes:
                continue
            result[self.gui_name(child)] = child
        return result

    def list_templates(self, display_path: str) -> dict[str, IntTemplate]:
        """`{name: IntTemplate}` directly under the folder at `display_path`."""
        return self.list_contents(display_path, classes=("IntTemplate",))

    def gui_path(self, obj: PFGeneral) -> str:
        """GUI-style path of a library object, relative to the library root."""
        library_full_name = self.root.GetFullName()
        full_name = obj.GetFullName()
        if not full_name.startswith(library_full_name):
            return full_name
        remainder = full_name[len(library_full_name) :].lstrip("\\")
        segments = [seg.rsplit(".", 1)[0] for seg in remainder.split("\\") if seg]
        return "\\".join(self.gui_name(seg) for seg in segments)

    # ------------------------------------------------------------------ #
    # diagnostics
    # ------------------------------------------------------------------ #
    def unmapped_system_folders(self, within: str = "Templates") -> list[str]:
        """`loc_name`s of system folders (below `within`) that have no translation.

        A non-empty result means the localisation table and this PowerFactory
        version have drifted - navigation still works via literal `loc_name`s.

        Args:
            within: GUI path of the subtree to check. Defaults to `"Templates"`
                (the branch powfacpy uses). Pass `""` for the whole library
                (slow - the global library has thousands of folders).
        """
        translations = self.folder_name_translations
        start = self.get_object(within) if within else self.root
        unmapped: list[str] = []

        def walk(folder: PFGeneral) -> None:
            for child in folder.GetContents("*.IntFolder"):
                loc_name = child.loc_name
                if (
                    child.HasAttribute("iopt_sys")
                    and child.GetAttribute("iopt_sys") == 1
                    and " " not in loc_name  # coded keys never contain spaces
                    and loc_name not in translations
                ):
                    unmapped.append(loc_name)
                walk(child)

        walk(start)
        return unmapped

    # ------------------------------------------------------------------ #
    # internals
    # ------------------------------------------------------------------ #
    def _child_by_name(self, parent: PFGeneral, name: str) -> PFGeneral | None:
        matches = [
            child
            for child in parent.GetContents()
            if self.gui_name(child) == name or child.loc_name == name
        ]
        if len(matches) > 1:
            raise PFInterfaceError(
                f"'{name}' is ambiguous under '{self.gui_path(parent)}' "
                f"({[c.GetFullName() for c in matches]})."
            )
        return matches[0] if matches else None

    def _get_of_class(
        self,
        display_path: str,
        classes: tuple[str, ...],
        error_if_non_existent: bool,
    ) -> PFGeneral | None:
        obj = self.get_object(display_path, error_if_non_existent)
        if obj is None:
            return None
        if obj.GetClassName() not in classes:
            raise PFInterfaceError(
                f"'{display_path}' is a {obj.GetClassName()}, expected one of {classes}."
            )
        return obj
