"""Tests for powfacpy.base.string_manipulation.

Pure string manipulation - no PowerFactory dependency (except
'format_full_path' / 'get_path_inside_active_project_from_full_path', which only
need an object with a '.GetActiveProject().loc_name', faked here).

Exercised through the deprecated `PFStringManipulation` namespace so the back-
compat shim stays covered; `test_module_functions_match_shim` checks the
module-level functions are the same callables.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory

from powfacpy.base import string_manipulation as strman
from powfacpy.base.string_manipulation import PFStringManipulation


class _FakeProject:
    def __init__(self, loc_name):
        self.loc_name = loc_name


class _FakeApp:
    def __init__(self, project_loc_name):
        self._project = _FakeProject(project_loc_name)

    def GetActiveProject(self):
        return self._project


def test_replace_between_characters_docstring_example():
    result = PFStringManipulation.replace_between_characters(
        ".",
        "\\",
        "\\",
        r"username.IntUser\pow.facpy.\powfacpy.tests.IntPrj\Network Model.IntPrjfolder\Network Data.IntPrjfolder\test_base_interface\Grid.ElmNet\Terminal HV 1.ElmTerm",
    )
    assert (
        result
        == r"username\pow.facpy\powfacpy.tests\Network Model\Network Data\test_base_interface\Grid\Terminal HV 1"
    )


def test_replace_between_characters_no_occurrence():
    assert PFStringManipulation.replace_between_characters(
        ".", "\\", "\\", r"no dots here at all"
    ) == r"no dots here at all"


def test_remove_html_tags_from_path():
    tagged = "<l3>Network Model\\Grid\\Terminal 1</l3>"
    assert (
        PFStringManipulation.remove_html_tags_from_path(tagged)
        == "Network Model\\Grid\\Terminal 1"
    )


def test_remove_opening_html_tag_from_path():
    tagged = "<l3>Network Model\\Grid</l3>"
    assert (
        PFStringManipulation.remove_opening_html_tag_from_path(tagged)
        == "Network Model\\Grid</l3>"
    )


def test_remove_closing_html_tag_from_path():
    tagged = "<l3>Network Model\\Grid</l3>"
    assert (
        PFStringManipulation.remove_closing_html_tag_from_path(tagged)
        == "<l3>Network Model\\Grid"
    )


def test_remove_class_names():
    path = r"Network Model.IntPrjfolder\Network Data.IntPrjfolder\Grid.ElmNet\Terminal 1.ElmTerm"
    assert (
        PFStringManipulation.remove_class_names(path)
        == r"Network Model\Network Data\Grid\Terminal 1"
    )


def test_remove_class_names_matches_the_old_state_machine():
    # remove_class_names switched from replace_between_characters(".","\\","\\",..)
    # to a regex - check parity on the tricky cases (dots inside names, trailing
    # class name, no class names, empty).
    for path in (
        r"username.IntUser\pow.facpy.\powfacpy.tests.IntPrj\Grid.ElmNet\T.ElmTerm",
        r"A.IntPrjfolder\B.ElmNet",
        r"Grid.ElmNet\Terminal 1.ElmTerm",
        r"no dots or slashes",
        r"a.b.c\d.e",
        "",
        r"\leading.ElmNet\x.ElmTerm",
    ):
        assert strman.remove_class_names(path) == strman.replace_between_characters(
            ".", "\\", "\\", path
        )


def test_truncate_until():
    original = r"\user.IntUser\my_project.IntPrj\Network Model\Grid"
    assert (
        PFStringManipulation.truncate_until(original, "my_project.IntPrj\\")
        == r"Network Model\Grid"
    )


def test_truncate_until_pattern_not_found_returns_original():
    assert PFStringManipulation.truncate_until("abc", "xyz") == "abc"


def test_truncate_beginning_removes_matching_prefix():
    assert (
        PFStringManipulation.truncate_beginning("prefix_rest", "prefix")
        == "rest"
    )


def test_truncate_beginning_leaves_non_matching_string_unchanged():
    assert (
        PFStringManipulation.truncate_beginning("something_else", "prefix")
        == "something_else"
    )


def test_format_variable_name_strips_unit_and_quotes():
    assert PFStringManipulation.format_variable_name('"s:u0 in kV"\n') == "s:u0"
    assert PFStringManipulation.format_variable_name("s:u0 in kV") == "s:u0"
    assert PFStringManipulation.format_variable_name("s:u0") == "s:u0"


def test_handle_path_strips_leading_backslash():
    assert PFStringManipulation.handle_path("\\Network Model\\Grid") == (
        "Network Model\\Grid"
    )


def test_handle_path_leaves_relative_path_unchanged():
    assert (
        PFStringManipulation.handle_path("Network Model\\Grid")
        == "Network Model\\Grid"
    )


def test_handle_path_raises_type_error_for_non_string():
    with pytest.raises(TypeError):
        PFStringManipulation.handle_path(123)


def test_replace_outside_or_inside_of_strings_in_a_string_default_outside():
    result = PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
        "p HV load >= 2 and 'p HV load is a string'",
        {"p HV load": "p_HV_load"},
    )
    assert result == "p_HV_load >= 2 and 'p HV load is a string'"


def test_replace_outside_or_inside_of_strings_in_a_string_inside():
    result = PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
        "p HV load >= 2 and 'p HV load is a string'",
        {"p HV load": "p_HV_load"},
        outside=False,
    )
    assert result == "p HV load >= 2 and 'p_HV_load is a string'"


def test_split_but_keep_delimiter():
    result = PFStringManipulation.split_but_keep_delimiter(
        "p HV load >= 2 and (control 1 == 'A' and control 2 != 'S')", "'"
    )
    assert result == [
        "p HV load >= 2 and (control 1 == '",
        "A'",
        " and control 2 != '",
        "S'",
        ")",
    ]


def test_format_full_path():
    fake_app = _FakeApp("my_project")
    full_path = (
        r"\username.IntUser\my_project.IntPrj\Network Model.IntPrjfolder"
        r"\Network Data.IntPrjfolder\Grid.ElmNet\Terminal 1.ElmTerm"
    )
    assert PFStringManipulation.format_full_path(
        full_path, fake_app
    ) == r"Network Model\Network Data\Grid\Terminal 1"


def test_format_full_path_strips_trailing_closing_tag():
    fake_app = _FakeApp("my_project")
    full_path = (
        r"\username.IntUser\my_project.IntPrj\Network Model.IntPrjfolder"
        r"\Grid.ElmNet\Terminal 1.ElmTerm</l3>"
    )
    assert PFStringManipulation.format_full_path(
        full_path, fake_app
    ) == r"Network Model\Grid\Terminal 1"


def test_pf_name_to_windows_removes_invalid_characters():
    assert (
        PFStringManipulation.pf_name_to_windows('a<b>c:d"e/f\\g|h?i*j')
        == "abcdefghij"
    )


def test_pf_name_to_windows_strips_trailing_dots_and_spaces():
    assert PFStringManipulation.pf_name_to_windows("Switch sig 3-1 by sig. ") == (
        "Switch sig 3-1 by sig"
    )


def test_module_functions_match_shim():
    # the deprecated PFStringManipulation namespace exposes the same callables
    for name in (
        "replace_between_characters",
        "remove_class_names",
        "truncate_until",
        "truncate_beginning",
        "format_variable_name",
        "handle_path",
        "split_but_keep_delimiter",
        "pf_name_to_windows",
        "format_full_path",
    ):
        assert getattr(PFStringManipulation, name) is getattr(strman, name)
    assert (
        PFStringManipulation._get_path_inside_active_project_from_full_path
        is strman.get_path_inside_active_project_from_full_path
    )


def test_get_path_inside_active_project_from_full_path():
    fake_app = _FakeApp("my_project")
    full = r"\u.IntUser\my_project.IntPrj\Network Model.IntPrjfolder\Grid.ElmNet\T1.ElmTerm"
    assert strman.get_path_inside_active_project_from_full_path(full, fake_app) == (
        r"Network Model.IntPrjfolder\Grid.ElmNet\T1.ElmTerm"
    )


if __name__ == "__main__":
    pytest.main([__file__])
