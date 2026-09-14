"""Pure string helpers for PowerFactory paths and expressions.

Module-level functions - import them directly:

    from powfacpy.base.string_manipulation import remove_class_names

The `PFStringManipulation` class at the bottom is a deprecated namespace kept so
that `from powfacpy.base.string_manipulation import PFStringManipulation` keeps
working; new code should use the functions.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from powfacpy.pf_classes.protocols import PFApp


def replace_between_characters(
    char1: str, char2: str, replacement: str, original: str
) -> str:
    """Replace text between 'char1' and 'char2' in 'original' with 'replacement'.

    Example:
      Calling
        replace_between_characters(
          '.',
          '\\',
          '\\',
          'username.IntUser\\pow.facpy.\\powfacpy.tests.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_base_interface\\Grid.ElmNet\\Terminal HV 1.ElmTerm')
      would give the output:
        'username\\pow.facpy\\powfacpy.tests\\Network Model\\Network Data\\test_base_interface\\Grid\\Terminal HV 1'
      Note the behavior when there are several '.' in between '\\'
      -> then the replacement starts after the last '.'
    """
    new_string = ""
    is_after_char_1 = False
    string_between_char_1_occurrences = ""
    for c in original:
        if c == char1:
            is_after_char_1 = True
            new_string += string_between_char_1_occurrences
            string_between_char_1_occurrences = ""
        elif c == char2:
            if is_after_char_1:
                new_string += replacement
            else:
                new_string += c
            string_between_char_1_occurrences = ""
            is_after_char_1 = False
        if is_after_char_1:
            string_between_char_1_occurrences += c
        elif not c == char2:
            new_string += c
    return new_string


def remove_html_tags_from_path(path: str) -> str:
    return path[path.find(">") + 1 : path.rfind("<")]


def remove_opening_html_tag_from_path(path: str) -> str:
    return path[path.find(">") + 1 :]


def remove_closing_html_tag_from_path(path: str) -> str:
    return path[0 : path.rfind("<")]


#: matches a '.ClassName' segment that sits right before a '\' or the end of
#: the string (so 'a.b.ElmFoo\c' -> the '.ElmFoo' is removed, 'a.b' is not)
_CLASS_NAME_SUFFIX = re.compile(r"\.[^.\\]*(?=\\|$)")


def remove_class_names(path: str) -> str:
    """Strip the '.ClassName' suffixes from every element of a PF path.

    ``'Grid.ElmNet\\Terminal 1.ElmTerm'`` -> ``'Grid\\Terminal 1'``.
    """
    return _CLASS_NAME_SUFFIX.sub("", path)


def truncate_until(original: str, string_pattern: str) -> str:
    """Truncate all characters up to (and including) the first `string_pattern`.

    Returns `original` unchanged if `string_pattern` does not occur in it.
    """
    index = original.find(string_pattern)
    if index == -1:
        return original
    return original[index + len(string_pattern) :]


def truncate_beginning(original: str, string_pattern: str) -> str:
    """Remove `string_pattern` (plus the single following separator char) from the
    start of `original`. Returns `original` unchanged if it does not start with it.
    """
    if original.startswith(string_pattern):
        return original[len(string_pattern) + 1 :]
    return original


def format_variable_name(name: str) -> str:
    """Shorten a PF-generated csv export variable name.

    Example: `'s:u0 in kV'` -> `'s:u0'` (drops the unit/description and quotes).
    """
    return name.split(" ", 1)[0].replace('"', "").replace("\n", "")


def handle_path(path: str) -> str:
    """Strip a leading '\\' (not accepted by most PF methods); raise if not a string."""
    try:
        if not path[0] == "\\":
            return path
        return path[1:]
    except TypeError:
        raise TypeError("Path must be of type string.")


def replace_outside_or_inside_of_strings_in_a_string(
    string: str, replacements: dict, outside: bool = True
) -> str:
    """Apply `replacements` only outside (or, with `outside=False`, inside) quoted substrings.

    Example: in `"p HV load >= 2 and 'p HV load is a string'"` the quoted part is
    left untouched when `outside=True`.
    """
    target_parity = 0 if outside else 1
    parts = split_but_keep_delimiter(string, "'")
    for n, part in enumerate(parts):
        if n % 2 == target_parity:  # even indices are the parts outside quotes
            for old, new in replacements.items():
                part = part.replace(old, new)
            parts[n] = part
    return "".join(parts).strip()


def split_but_keep_delimiter(string: str, delimiter: str) -> list[str]:
    """Like `str.split(delimiter)` but keeps the delimiter attached to each piece.

    Example:
      `split_but_keep_delimiter("a == 'A' and b != 'S')", "'")`
      -> `["a == '", "A'", " and b != '", "S'", ')']`
    """
    split_strings_list = [part + delimiter for part in string.split(delimiter)]
    split_strings_list[-1] = split_strings_list[-1].rstrip(delimiter)
    return split_strings_list


def pf_name_to_windows(name: str) -> str:
    """Convert a PF object name into a valid Windows file/folder name."""
    name = re.sub(r'[<>:"/\\|?*]', "", name)  # invalid Windows filename characters
    name = name.strip().rstrip(".")  # Windows disallows trailing dots/spaces
    return name


def get_path_inside_active_project_from_full_path(path: str, pf_app: "PFApp") -> str:
    """Full path (incl. user and project) -> path relative to the active project.

    Example:
      `\\username.IntUser\\proj.IntPrj\\Network Model.IntPrjfolder\\Grid.ElmNet\\T1.ElmTerm`
      -> `Network Model.IntPrjfolder\\Grid.ElmNet\\T1.ElmTerm`
    """
    project_name = pf_app.GetActiveProject().loc_name + ".IntPrj\\"
    path = truncate_until(path, project_name)
    # str() on a PF object can leave a trailing closing tag (</l3>) - drop it.
    if path and path[-1] == ">":
        path = path[0 : path.rfind("<")]
    return path


def format_full_path(path: str, pf_app: "PFApp") -> str:
    """Full path -> path relative to the active project, without class names.

    See also `powfacpy.base.paths.Paths.format_full_path`, which needs no `pf_app`.
    """
    return remove_class_names(
        get_path_inside_active_project_from_full_path(path, pf_app)
    )


class PFStringManipulation:
    """Deprecated namespace - use the module-level functions instead.

    Kept so that ``from powfacpy.base.string_manipulation import PFStringManipulation``
    and ``PFStringManipulation.<method>(...)`` keep working.
    """  # TODO deprecate

    replace_between_characters = staticmethod(replace_between_characters)
    remove_html_tags_from_path = staticmethod(remove_html_tags_from_path)
    remove_opening_html_tag_from_path = staticmethod(remove_opening_html_tag_from_path)
    remove_closing_html_tag_from_path = staticmethod(remove_closing_html_tag_from_path)
    remove_class_names = staticmethod(remove_class_names)
    truncate_until = staticmethod(truncate_until)
    truncate_beginning = staticmethod(truncate_beginning)
    format_variable_name = staticmethod(format_variable_name)
    handle_path = staticmethod(handle_path)
    replace_outside_or_inside_of_strings_in_a_string = staticmethod(
        replace_outside_or_inside_of_strings_in_a_string
    )
    split_but_keep_delimiter = staticmethod(split_but_keep_delimiter)
    pf_name_to_windows = staticmethod(pf_name_to_windows)
    format_full_path = staticmethod(format_full_path)
    _get_path_inside_active_project_from_full_path = staticmethod(
        get_path_inside_active_project_from_full_path
    )
