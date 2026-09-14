"""Tests for powfacpy.applications.digsilent_library.DigsilentLibrary.

Needs a live PowerFactory (reads the global library and the localisation db).
"""

import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.applications.digsilent_library import DigsilentLibrary
from powfacpy.exceptions import PFInterfaceError

_GFC = r"Templates\Grid-forming Converters"
_REGFM_A1_STORAGE = _GFC + r"\WECC REGFM_A1 Droop Inverter - Storage"


@pytest.fixture(scope="module")
def lib(pf_app) -> DigsilentLibrary:
    return DigsilentLibrary(pf_app)


def test_folder_name_translations_from_localisation_db(lib: DigsilentLibrary):
    assert lib.localisation_db_path.is_file()
    translations = lib.folder_name_translations
    assert translations["Templ"] == "Templates"
    assert translations["TemplGfc"] == "Grid-forming Converters"
    assert translations["TemplPv"] == "Photovoltaic"


def test_gui_name(lib: DigsilentLibrary):
    assert lib.gui_name("TemplGfc") == "Grid-forming Converters"
    # unknown / user folder -> literal loc_name
    assert lib.gui_name("Some User Folder") == "Some User Folder"


def test_get_folder_resolves_gui_path(lib: DigsilentLibrary):
    folder = lib.get_folder(_GFC)
    assert folder.GetClassName() == "IntFolder"
    assert folder.loc_name == "TemplGfc"
    assert folder.GetFullName().endswith(r"\Templ\TemplGfc")
    # forward slashes work too
    assert lib.get_folder("Templates/Grid-forming Converters") == folder


def test_get_template(lib: DigsilentLibrary):
    template = lib.get_template(_REGFM_A1_STORAGE)
    assert template.GetClassName() == "IntTemplate"
    assert template.loc_name == "WECC REGFM_A1 Droop Inverter - Storage"


def test_get_object_root_and_literal_loc_name(lib: DigsilentLibrary):
    assert lib.get_object("") == lib.root
    # the coded loc_name is accepted as well as the GUI name
    assert lib.get_object(r"Templ\TemplGfc") == lib.get_folder(_GFC)


def test_get_of_wrong_class_raises(lib: DigsilentLibrary):
    with pytest.raises(PFInterfaceError):
        lib.get_folder(_REGFM_A1_STORAGE)  # it's an IntTemplate
    with pytest.raises(PFInterfaceError):
        lib.get_template(_GFC)  # it's an IntFolder


def test_missing_segment(lib: DigsilentLibrary):
    assert lib.get_object(r"Templates\Does Not Exist", error_if_non_existent=False) is None
    with pytest.raises(PFInterfaceError):
        lib.get_object(r"Templates\Does Not Exist")


def test_list_templates(lib: DigsilentLibrary):
    templates = lib.list_templates(_GFC)
    assert "WECC REGFM_A1 Droop Inverter - Storage" in templates
    assert all(t.GetClassName() == "IntTemplate" for t in templates.values())
    assert len(templates) >= 5


def test_gui_path_round_trips(lib: DigsilentLibrary):
    template = lib.get_template(_REGFM_A1_STORAGE)
    assert lib.gui_path(template) == _REGFM_A1_STORAGE
    assert lib.gui_path(lib.get_folder(_GFC)) == _GFC


def test_unmapped_system_folders(lib: DigsilentLibrary):
    # if this ever grows, the localisation table drifted from this PF version -
    # navigation still works, but the mapping should be reviewed
    unmapped = lib.unmapped_system_folders()
    assert isinstance(unmapped, list)


if __name__ == "__main__":
    pytest.main([__file__])
