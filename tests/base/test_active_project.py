"""Tests for the class ActiveProject.

The class 'ActiveProject' inherits from 'Folder'. There are no separate tests for the 'Folder' class, all tests for both classes are included here.
"""

import os
import pytest

# conftest.py has already put the PowerFactory application on sys.path (if available).
try:
    import powerfactory
except ImportError:
    powerfactory = None

from powfacpy.base.folder import Folder
from powfacpy.base.base import BaseObjectStatic
from powfacpy.base.string_manipulation import PFStringManipulation
from powfacpy.base.active_project import ActiveProject
from powfacpy.exceptions import (
    PFAttributeError,
    PFAttributeTypeError,
    PFPathError,
    PFNonExistingObjectError,
    PFNoActiveStudyCaseError,
)


def test_get_obj(act_prj: ActiveProject, activate_powfacpy_test_project):
    terminal_1 = act_prj.get_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )[0]
    assert isinstance(terminal_1, powerfactory.DataObject)
    with pytest.raises(PFPathError):
        terminal_1 = act_prj.get_obj(
            r"Stretchwork Model\Stretchwork Data\Grid\Termalamala"
        )[0]
    with pytest.raises(PFPathError):
        terminal_1 = act_prj.get_obj(r"N")[0]
    with pytest.raises(TypeError):
        terminal_1 = act_prj.get_obj(terminal_1)[0]
    with pytest.raises(TypeError):
        terminal_1 = act_prj.get_obj(terminal_1, include_subfolders=False)[0]


def test_get_single_object(act_prj: ActiveProject, activate_powfacpy_test_project):
    terminal_1 = act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )
    assert isinstance(terminal_1, powerfactory.DataObject)
    with pytest.raises(TypeError):
        act_prj.get_unique_obj(
            r"Network Model\Network Data\test_active_project_interface\Grid\Terminal*"
        )


def test_get_obj_with_condition(act_prj: ActiveProject, activate_powfacpy_test_project):
    hv_terminals = act_prj.get_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal*",
        condition=lambda x: getattr(x, "uknom") > 50,
    )
    assert len(hv_terminals) == 2


def test_get_obj_with_parent_folder_argument(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    parent_folder = act_prj.get_first_level_folder("user")
    terminal_1 = act_prj.get_obj(
        r"powfacpy\powfacpy_tests\Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1",
        parent_folder=parent_folder,
    )[0]
    assert isinstance(terminal_1, powerfactory.DataObject)

    grid = act_prj.get_obj(
        "Grid",
        parent_folder=r"Network Model\Network Data\test_active_project_interface",
    )[0]
    assert isinstance(grid, powerfactory.DataObject)

    parent_folder = Folder(
        r"Network Model\Network Data\test_active_project_interface", act_prj.app
    )
    grid = act_prj.get_obj("Grid", parent_folder=parent_folder)[0]
    assert isinstance(grid, powerfactory.DataObject)


def test_get_obj_including_subfolders(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    terminals = act_prj.get_obj(
        r"Network Data\test_active_project_interface\*.ElmTerm",
        parent_folder="Network Model",
        include_subfolders=True,
    )
    assert len(terminals) == 3


def test_path_exists(act_prj: ActiveProject, activate_powfacpy_test_project):
    assert act_prj.path_exists(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )


def test_set_attr(act_prj: ActiveProject, activate_powfacpy_test_project):
    test_string_1 = "TestString1"
    test_string_2 = "TestString2"
    act_prj.set_attr(
        r"Library\Dynamic Models\Linear_interpolation", {"sTitle": test_string_1}
    )
    act_prj.set_attr(
        "Linear_interpolation",
        {"sTitle": test_string_2, "desc": ["dummy description"]},
        parent_folder=r"Library\Dynamic Models",
    )
    stitle = act_prj.get_attr(r"Library\Dynamic Models\Linear_interpolation", "sTitle")
    assert stitle == test_string_2


def test_set_attr_exceptions(act_prj: ActiveProject, activate_powfacpy_test_project):
    with pytest.raises(PFAttributeTypeError):
        act_prj.set_attr(
            r"Library\Dynamic Models\Linear_interpolation",
            {"sTitle": "dummy", "desc": 2},
        )  # "desc" should be a list with one string item
    with pytest.raises(PFAttributeError):
        act_prj.set_attr(
            r"Library\Dynamic Models\Linear_interpolation",
            {"sTie": "dummy", "desc": ["dummy description"]},
        )  # 'sTie' is not a valid attribute
    with pytest.raises(PFPathError):
        act_prj.get_obj(
            r"Network Model\Network Data\test_active_project_interface\Grid\Termalamala"
        )


def test_set_attr_by_path(act_prj: ActiveProject, activate_powfacpy_test_project):
    act_prj.set_attr_by_path(
        r"Library\Dynamic Models\Linear_interpolation\desc", ["description"]
    )
    with pytest.raises(PFPathError):
        act_prj.set_attr_by_path(
            r"Stretchwork Model\Stretchwork Data\Grid\Termalamala", ["description"]
        )


def test_get_attr(act_prj: ActiveProject, activate_powfacpy_test_project):
    terminal_1 = act_prj.get_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )[0]
    systype = act_prj.get_attr(terminal_1, "systype")
    assert systype == 0
    with pytest.raises(PFAttributeError):
        systype = act_prj.get_attr(terminal_1, "trixi")


def test_create_by_path(act_prj: ActiveProject, activate_powfacpy_test_project):
    act_prj.create_by_path(r"Library\Dynamic Models\dummy.BlkDef")
    with pytest.raises(PFPathError):
        act_prj.create_by_path(r"ry\Dynamic Models\dummy.BlkDef")
    with pytest.raises(TypeError):
        act_prj.create_by_path(4)


def test_create_in_folder(act_prj: ActiveProject, activate_powfacpy_test_project):
    act_prj.create_in_folder("dummy2.BlkDef", r"Library\Dynamic Models")
    with pytest.raises(TypeError):
        act_prj.create_in_folder(2, r"Library\Dynamic Models")


def test_get_by_condition(act_prj: ActiveProject, activate_powfacpy_test_project):
    folder = r"Network Model\Network Data\test_active_project_interface\Grid"
    all_terminals = act_prj.get_obj("*.ElmTerm", parent_folder=folder)

    mv_terminals = act_prj.get_by_condition(
        all_terminals, lambda x: getattr(x, "uknom") > 100
    )
    assert len(mv_terminals) == 2

    with pytest.raises(PFAttributeError):
        mv_terminals = act_prj.get_by_condition(
            all_terminals, lambda x: getattr(x, "wrong_attr") > 100
        )


def test_delete_obj(act_prj: ActiveProject, activate_powfacpy_test_project):
    folder = r"Library\Dynamic Models\TestDelete"
    act_prj.create_in_folder(
        "dummy_to_be_deleted_1.BlkDef",
        folder,
    )
    act_prj.create_in_folder(
        "dummy_to_be_deleted_2.BlkDef",
        folder,
    )
    act_prj.delete_obj("dummy_to_be_deleted*", parent_folder=folder)
    objects_in_folder = act_prj.get_obj(
        "dummy_to_be_deleted*.BlkDef", parent_folder=folder, error_if_non_existent=False
    )
    assert len(objects_in_folder) == 0

    act_prj.create_in_folder(
        "dummy_to_be_deleted_1.BlkDef",
        folder,
    )
    act_prj.create_in_folder(
        "dummy_to_be_deleted_2.BlkDef",
        folder,
    )
    act_prj.delete_obj("dummy_to_be_deleted_1.BlkDef", parent_folder=folder)
    objects_in_folder = act_prj.get_obj(
        "dummy_to_be_deleted*.BlkDef", parent_folder=folder
    )
    assert len(objects_in_folder) == 1

    act_prj.create_in_folder(
        "dummy_to_be_deleted_1.BlkDef",
        folder,
    )
    act_prj.create_in_folder(
        "dummy_to_be_deleted_2.BlkDef",
        folder,
    )
    act_prj.delete_obj(
        "dummy_to_be_deleted*",
        parent_folder=r"Library\Dynamic Models",
        include_subfolders=True,
    )
    objects_in_folder = act_prj.get_obj(
        "dummy_to_be_deleted*", parent_folder=folder, error_if_non_existent=False
    )
    assert len(objects_in_folder) == 0

    act_prj.create_in_folder(
        "dummy_to_be_deleted_1.BlkDef",
        folder,
    )
    act_prj.create_in_folder(
        "dummy_to_be_deleted_2.BlkDef",
        folder,
    )
    objects_in_folder = act_prj.get_obj("*", parent_folder=folder)
    act_prj.delete_obj(objects_in_folder)
    objects_in_folder = act_prj.get_obj(
        "*", parent_folder=folder, error_if_non_existent=False
    )
    assert len(objects_in_folder) == 0

    act_prj.create_in_folder("dummy_to_be_deleted_1.BlkDef", folder)
    object_in_folder = act_prj.get_unique_obj("*", parent_folder=folder)
    act_prj.delete_obj(object_in_folder)
    objects_in_folder = act_prj.get_obj(
        "*", parent_folder=folder, error_if_non_existent=False
    )
    assert len(objects_in_folder) == 0


def test_copy_obj(act_prj: ActiveProject, activate_powfacpy_test_project):
    folder_copy_from = r"Library\Dynamic Models\TestCopyFrom"
    folder_copy_to = r"Library\Dynamic Models\TestCopyTo"

    act_prj.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    copied_objects = act_prj.copy_obj(
        "*", folder_copy_to, parent_folder=folder_copy_from
    )
    assert len(copied_objects) == 3
    # test that the copied objects are returned and not the initial objects to be copied
    obj_to_be_copied = act_prj.get_obj("*", parent_folder=folder_copy_from)
    for idx, obj in enumerate(obj_to_be_copied):
        assert copied_objects[idx] != obj

    act_prj.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    folder_copy_from = act_prj.get_obj(r"Library\Dynamic Models\TestCopyFrom")[0]
    folder_copy_to = act_prj.get_obj(r"Library\Dynamic Models\TestCopyTo")[0]
    copied_objects = act_prj.copy_obj(
        "*", folder_copy_to, parent_folder=folder_copy_from
    )
    assert len(copied_objects) == 3

    objects_to_copy = act_prj.get_obj("*", parent_folder=folder_copy_from)
    copied_objects = act_prj.copy_obj(objects_to_copy, folder_copy_to, overwrite=False)
    assert len(copied_objects) == 3
    all_objects_in_folder = act_prj.get_obj("*", parent_folder=folder_copy_to)
    assert len(all_objects_in_folder) == 6

    act_prj.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    objects_to_copy = act_prj.get_obj("*", parent_folder=folder_copy_from)[0]
    copied_objects = act_prj.copy_obj(objects_to_copy, folder_copy_to, overwrite=False)
    assert len(copied_objects) == 1
    all_objects_in_folder = act_prj.get_obj("*", parent_folder=folder_copy_to)
    assert len(all_objects_in_folder) == 1


def test_copy_single_obj(act_prj: ActiveProject, activate_powfacpy_test_project):
    folder_copy_from = r"Library\Dynamic Models\TestDummyFolder"
    folder_copy_to = r"Library\Dynamic Models\TestCopy"

    act_prj.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    copied_object = act_prj.copy_single_obj(
        "dummy.*",
        folder_copy_to,
        parent_folder=folder_copy_from,
        new_name="new_dummy_name",
    )
    copied_obj_from_folder = act_prj.get_unique_obj(
        "new_dummy_name", parent_folder=folder_copy_to
    )
    assert copied_object == copied_obj_from_folder

    copied_object = act_prj.copy_single_obj(
        "dummy3.TypMdl",
        folder_copy_to,
        parent_folder=folder_copy_from,
        new_name="new_dummy_name",
    )
    # expected behavior is that new_dummy_name1.TypMdl is created because new_dummy_name.BlkDef already exists
    copied_obj_from_folder = act_prj.get_unique_obj(
        "new_dummy_name1.TypMdl", parent_folder=folder_copy_to
    )
    assert copied_object == copied_obj_from_folder

    obj_to_copy = act_prj.get_unique_obj("dummy2.*", parent_folder=folder_copy_from)
    copied_object = act_prj.copy_single_obj(obj_to_copy, folder_copy_to, overwrite=True)
    copied_obj_from_folder = act_prj.get_unique_obj(
        "dummy2", parent_folder=folder_copy_to
    )
    assert copied_object == copied_obj_from_folder

    act_prj.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    obj_to_copy = act_prj.get_unique_obj("dummy2.*", parent_folder=folder_copy_from)
    copied_object = act_prj.copy_single_obj(
        obj_to_copy,
        folder_copy_to,
        overwrite=False,
        parent_folder=folder_copy_from,
        new_name="new_dummy_name",
    )
    copied_obj_from_folder = act_prj.get_unique_obj(
        "new_dummy_name", parent_folder=folder_copy_to
    )
    assert copied_object == copied_obj_from_folder


def test_move_obj(act_prj: ActiveProject, activate_powfacpy_test_project):
    folder_move_from = r"Library\Dynamic Models\TestCopyFrom"
    folder_move_to = r"Library\Dynamic Models\TestCopyTo"

    act_prj.delete_obj("*", parent_folder=folder_move_to, error_if_non_existent=False)
    success = act_prj.move_obj("*", folder_move_to, parent_folder=folder_move_from)
    moved_objects = act_prj.get_obj("*", parent_folder=folder_move_to)
    assert success == 0
    assert len(moved_objects) == 3
    empty_objects = act_prj.get_obj(
        "*", parent_folder=folder_move_from, error_if_non_existent=False
    )
    assert len(empty_objects) == 0
    # Undo changes
    act_prj.move_obj(moved_objects, target_folder=folder_move_from)


def test_move_single_obj(act_prj: ActiveProject, activate_powfacpy_test_project):
    folder_move_from = r"Library\Dynamic Models\TestCopyFrom"
    folder_move_to = r"Library\Dynamic Models\TestCopyTo"

    act_prj.delete_obj("*", parent_folder=folder_move_to, error_if_non_existent=False)
    obj_to_move = act_prj.get_obj("*", parent_folder=folder_move_from)[0]
    success = act_prj.move_single_obj(
        obj_to_move, folder_move_to, parent_folder=folder_move_from
    )
    moved_objects = act_prj.get_obj("*", parent_folder=folder_move_to)
    assert success == 0
    assert len(moved_objects) == 1
    # Undo changes
    act_prj.move_single_obj(obj_to_move, target_folder=folder_move_from)


def test_handle_single_pf_object_or_path_input(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    folder = act_prj.get_obj(r"Network Model\Network Data")[0]
    with pytest.raises(TypeError):
        act_prj._handle_single_pf_object_or_path_input([folder])

    same_folder_returned = act_prj._handle_single_pf_object_or_path_input(folder)
    assert same_folder_returned == folder

    same_folder_using_string = act_prj._handle_single_pf_object_or_path_input(
        r"Network Model\Network Data"
    )
    assert same_folder_using_string == folder


def test_get_parameter_value_string(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    params = {
        "p": r"Network Model\Network Data\test_active_project_interface\Grid\General Load HV\plini",
        "q": r"Network Model\Network Data\test_active_project_interface\Grid\General Load HV\qlini",
        "u": r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 2\uknom",
    }
    act_prj.get_parameter_value_string(params, delimiter=" ")


def test_create_directory(act_prj: ActiveProject, activate_powfacpy_test_project):
    act_prj.create_directory(
        r"test1\test2", parent_folder=r"Study Cases\test_case_studies"
    )

    act_prj.create_directory(
        r"test1\test2\test3\test4", parent_folder=r"Study Cases\test_case_studies"
    )
    act_prj.delete_obj("test1", parent_folder=r"Study Cases\test_case_studies")

    act_prj.create_directory(r"test1\test2")
    act_prj.delete_obj("test1")


def test_get_loc_name_with_class(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    pf_objects = act_prj.get_obj(r"*.ElmTerm", include_subfolders=True)
    act_prj.get_loc_name_with_class(pf_objects)
    act_prj.get_loc_name_with_class(pf_objects[0])


def test_create_comtrade_obj(act_prj: ActiveProject, activate_powfacpy_test_project):
    path_of_cfg = os.getcwd() + r"\tests\tests_input\test_comtrade.cfg"
    intcomtrade = act_prj.create_comtrade_obj(path_of_cfg)
    intcomtrade.Load()
    assert intcomtrade.FindColumn("AC Voltage Source:m:u:bus1:A") == 1


def test_replace_outside_or_inside_of_strings_in_a_string(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1' control 1"
    conditions = PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
        conditions, {"control 1": "x[1]"}
    )
    assert conditions == "lorem ipsum x[1] == 'ABC control 1' 'control 1' x[1]"

    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1'"
    conditions = PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
        conditions, {"control 1": "x[1]"}
    )
    assert conditions == "lorem ipsum x[1] == 'ABC control 1' 'control 1'"

    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1' "
    conditions = PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
        conditions, {"control 1": "x[1]"}
    )
    assert conditions == "lorem ipsum x[1] == 'ABC control 1' 'control 1'"

    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1' "
    conditions = PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
        conditions, {"control 1": "x[1]"}, outside=False
    )
    assert conditions == "lorem ipsum control 1 == 'ABC x[1]' 'x[1]'"


def test_get_path_of_object(act_prj: ActiveProject, activate_powfacpy_test_project):
    path = "Network Model\\Network Data\\test_active_project_interface\\Grid\\Line 1.2"
    line = act_prj.get_unique_obj(path)
    path_derived = act_prj.get_path_of_object(line)
    assert path == path_derived


def test_get_upstream_object(act_prj: ActiveProject, activate_powfacpy_test_project):
    grid = act_prj.get_upstream_obj(
        r"Network Model\Network Data\test_database_interface\Grid\Voltage source ctrl\Frequency",
        lambda x: x.loc_name == "Grid",
    )
    grid_using_get_unique_obj = act_prj.get_unique_obj(
        r"Network Model\Network Data\test_database_interface\Grid"
    )
    assert grid == grid_using_get_unique_obj
    with pytest.raises(Exception):
        act_prj.get_upstream_obj(
            r"Network Model\Network Data\test_database_interface\Grid\Voltage source ctrl\Frequency",
            lambda x: x.loc_name == "wrong name",
        )


def test_get_from_study_case(act_prj: ActiveProject, activate_powfacpy_test_project):
    act_prj.activate_study_case(
        r"Study Cases\test_active_project_interface\multiple_elmres"
    )
    with pytest.warns():
        act_prj.get_from_study_case("ElmRes")
    with pytest.raises(Exception):
        act_prj.get_from_study_case("ElmRes", if_not_unique="error")
    # None disables the check (no warning); an invalid flag is rejected
    act_prj.get_from_study_case("ElmRes", if_not_unique=None)
    with pytest.raises(ValueError):
        act_prj.get_from_study_case("ElmRes", if_not_unique="warn")


def test_get_calc_relevant_obj(act_prj: ActiveProject, activate_powfacpy_test_project):
    act_prj.activate_study_case(
        r"Study Cases\test_active_project_interface\Study Case 1"
    )
    # Assert similar objects found with with get_obj
    terminals_getobj = []
    for network in act_prj.get_active_networks():
        terminals_getobj += act_prj.get_obj(
            "*.ElmTerm", parent_folder=network, include_subfolders=True
        )
    terminals_calc_rel = act_prj.get_calc_relevant_obj("*.ElmTerm")
    assert len(terminals_getobj) == len(terminals_calc_rel)

    terminals_getobj = []
    for network in act_prj.get_active_networks():
        terminals_getobj += act_prj.get_obj(
            "*.ElmTerm",
            parent_folder=network,
            include_subfolders=True,
            condition=lambda x: x.uknom > 100,
        )
    terminals_calc_rel = act_prj.get_calc_relevant_obj(
        "*.ElmTerm", condition=lambda x: x.uknom > 100
    )
    assert len(terminals_getobj) == len(terminals_calc_rel)

    with pytest.raises(PFNonExistingObjectError):
        act_prj.get_calc_relevant_obj("*.ElmTerm", condition=lambda x: x.uknom > 5000)


def test_export_to_pfd(
    act_prj: ActiveProject, activate_powfacpy_test_project, tmp_path
):
    # whole active project
    project_pfd = act_prj.export_to_pfd(str(tmp_path / "exported_project"))
    assert project_pfd.endswith(".pfd") and os.path.getsize(project_pfd) > 0

    # a group of objects, round-tripped through import
    terminal = act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )
    group_pfd = act_prj.export_to_pfd(str(tmp_path / "group.pfd"), [terminal])
    scratch = act_prj.app.GetCurrentUser().CreateObject(
        "IntFolder", "test_export_to_pfd_scratch"
    )
    try:
        pfd_import = act_prj.get_from_study_case("ComPfdimport")
        pfd_import.g_file = group_pfd
        pfd_import.g_target = scratch
        pfd_import.Execute()
        assert [obj.loc_name for obj in scratch.GetContents()] == [terminal.loc_name]
    finally:
        scratch.Delete()

    with pytest.raises(PFPathError):
        act_prj.export_to_pfd(str(tmp_path / "x.pfd"), r"Does\Not\Exist")


def test_import_project(act_prj: ActiveProject, activate_powfacpy_test_project):
    # a small, known-good full-project .pfd shipped for powfacpy.applications.frame_test
    imported = act_prj.import_project(
        os.path.abspath(r"pf_models\control_block_testing.pfd")
    )
    try:
        assert imported.GetClassName() == "IntPrj"
        assert imported.loc_name == "control_block_testing"
        # keep_current_project_activated=True (default): the original project/case stay active
        assert act_prj.get_active_project() != imported
    finally:
        imported.Delete()


def test_folder_properties(act_prj: ActiveProject, activate_powfacpy_test_project):
    act_prj.activate_study_case(r"Study Cases\test_active_project_interface\Study Case 1")
    app = act_prj.app
    assert act_prj.network_model_folder == app.GetProjectFolder("netmod")
    assert act_prj.network_data_folder == app.GetProjectFolder("netdat")
    assert act_prj.operation_scenarios_folder == app.GetProjectFolder("scen")
    assert act_prj.variations_folder == app.GetProjectFolder("scheme")
    assert act_prj.study_cases_folder == app.GetProjectFolder("study")
    assert act_prj.equipment_type_lib_folder == app.GetProjectFolder("equip")
    assert act_prj.library_folder == app.GetProjectFolder("lib")
    assert act_prj.scripts_folder == app.GetProjectFolder("scripts")
    assert act_prj.templates_folder == app.GetProjectFolder("templ")
    assert act_prj.zones_folder == app.GetDataFolder("ElmZone")
    assert act_prj.areas_folder == app.GetDataFolder("ElmArea")
    assert act_prj.boundaries_folder == app.GetDataFolder("IntBoundary")
    assert act_prj.circuits_folder == app.GetDataFolder("IntCircuit")
    assert act_prj.feeders_folder == app.GetDataFolder("IntFeeder")
    assert act_prj.versions_folder.GetClassName() == "IntVersionman"
    assert act_prj.load_flow_command == act_prj.get_from_study_case("ComLdf")


def test_get_active_study_case(act_prj: ActiveProject, activate_powfacpy_test_project):
    act_prj.activate_study_case(r"Study Cases\test_active_project_interface\Study Case 1")
    case = act_prj.get_active_study_case()
    assert case is not None and case.GetClassName() == "IntCase"

    case.Deactivate()
    try:
        with pytest.raises(PFNoActiveStudyCaseError):
            act_prj.get_active_study_case()
        assert act_prj.get_active_study_case(error_if_no_active_case=False) is None
    finally:
        case.Activate()


def test_reactivate_study_case(act_prj: ActiveProject, activate_powfacpy_test_project):
    act_prj.activate_study_case(r"Study Cases\test_active_project_interface\Study Case 1")
    case_before = act_prj.get_active_study_case()
    act_prj.reactivate_study_case()
    assert act_prj.get_active_study_case() == case_before


def test_get_results_obj_from_initial_conditions_calc(
    act_prj: ActiveProject, activate_39_bus_new_england_test_project
):
    # 'ComInc.p_resvar' is only populated once initial conditions have actually been
    # calculated - not merely by fetching/creating an ElmRes in the study case.
    act_prj.activate_study_case(r"Study Cases\2.1 Simulation Fault Bus 16 Stable")
    cominc = act_prj.get_from_study_case("ComInc", if_not_unique="error")
    assert cominc.Execute() == 0
    try:
        results_obj = act_prj.get_results_obj_from_initial_conditions_calc()
        assert results_obj.GetClassName() == "ElmRes"
        assert results_obj == cominc.p_resvar
    finally:
        act_prj.get_from_study_case("ComSim").Execute()  # end the simulation cleanly


def test_set_attr_resettable_and_reset_stored_attr(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    act_prj.activate_study_case(r"Study Cases\test_active_project_interface\Study Case 1")
    terminal = act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )
    original_uknom = terminal.uknom
    try:
        act_prj.set_attr_resettable(terminal, {"uknom": original_uknom + 5})
        assert terminal.uknom == pytest.approx(original_uknom + 5)

        act_prj.reset_stored_attr()
        assert terminal.uknom == pytest.approx(original_uknom)
    finally:
        terminal.uknom = original_uknom
        act_prj.reset_stored_attr(flush_memory=True)


def test_set_attr_resettable_remembers_the_first_value(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    # regression: a second call used to overwrite the stored 'original' with the
    # already-modified value, so reset restored the in-between value, not the true one
    act_prj.activate_study_case(r"Study Cases\test_active_project_interface\Study Case 1")
    terminal = act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )
    original_uknom = terminal.uknom
    try:
        act_prj.set_attr_resettable(terminal, {"uknom": original_uknom + 5})
        act_prj.set_attr_resettable(terminal, {"uknom": original_uknom + 9})
        assert terminal.uknom == pytest.approx(original_uknom + 9)

        act_prj.reset_stored_attr()
        assert terminal.uknom == pytest.approx(original_uknom)
    finally:
        terminal.uknom = original_uknom
        act_prj.reset_stored_attr(flush_memory=True)


def test_set_attr_resettable_accepts_path_string(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    # regression: 'obj' used to stay a path string internally, so the final
    # 'obj.SetAttribute(...)' crashed with AttributeError when called with a path
    path = r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    terminal = act_prj.get_unique_obj(path)
    original_uknom = terminal.uknom
    try:
        act_prj.set_attr_resettable(path, {"uknom": original_uknom + 3})
        assert terminal.uknom == pytest.approx(original_uknom + 3)
        act_prj.reset_stored_attr()
        assert terminal.uknom == pytest.approx(original_uknom)
    finally:
        terminal.uknom = original_uknom
        act_prj.reset_stored_attr(flush_memory=True)


# ---------------------------------------------------------------------------
# Regression tests for base-class hygiene fixes (see refactor notes §2)
# ---------------------------------------------------------------------------


def test_wrapper_equality_and_hash(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    grid = act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid"
    )
    other = act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface"
    )
    wrapper_a = BaseObjectStatic(grid)
    wrapper_b = BaseObjectStatic(grid)

    # wrapper vs wrapper and wrapper vs raw PF object
    assert wrapper_a == wrapper_b
    assert wrapper_a == grid
    assert wrapper_a != BaseObjectStatic(other)

    # comparison with None / unrelated types must return False, not raise
    assert (wrapper_a == None) is False  # noqa: E711
    assert wrapper_a != None  # noqa: E711
    assert wrapper_a != "not a pf object"

    # defining __eq__ without __hash__ would make wrappers unhashable
    assert hash(wrapper_a) == hash(wrapper_b)
    assert {wrapper_a, wrapper_b} == {wrapper_a}


def test_folder_equality_with_none_does_not_raise(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    folder = Folder(r"Network Model\Network Data", act_prj.app)
    # used to raise AttributeError ('NoneType' has no attribute '_obj')
    assert (folder == None) is False  # noqa: E711
    assert folder != None  # noqa: E711


def test_get_by_condition_type_error_is_wrapped(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    terminals = act_prj.get_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal*"
    )
    with pytest.raises(TypeError):
        act_prj.get_by_condition(terminals, lambda x: x.loc_name > 5)


def test_get_by_condition_evaluates_condition_once_per_object(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    terminals = act_prj.get_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal*"
    )
    assert len(terminals) >= 1
    seen = []

    def condition(obj):
        seen.append(obj)
        return getattr(obj, "definitely_not_a_real_attribute") == 1

    with pytest.raises(PFAttributeError):
        act_prj.get_by_condition(terminals, condition)
    # the old implementation ran a list comprehension, caught the error with a
    # bare 'except:' and then re-ran the loop - evaluating the first object twice
    assert len(seen) == 1


def test_get_single_obj_emits_deprecation_warning(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    path = (
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )
    with pytest.warns(DeprecationWarning):
        obj = act_prj.get_single_obj(path)
    assert obj == act_prj.get_unique_obj(path)


def test_get_obj_default_excludes_subfolders(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    parent = r"Network Model\Network Data\test_active_project_interface"
    # 'Terminal HV 1' sits one level below 'parent' (in '...\Grid')
    with pytest.raises(PFPathError):
        act_prj.get_obj("Terminal HV 1", parent_folder=parent)
    found = act_prj.get_obj(
        "Terminal HV 1", parent_folder=parent, include_subfolders=True
    )
    assert len(found) == 1


def test_mark_in_graphics_accepts_a_single_object(
    act_prj: ActiveProject, activate_powfacpy_test_project, monkeypatch
):
    terminal = act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )

    class _FakeApp:
        def __init__(self):
            self.calls = []

        def MarkInGraphics(self, elms, flag):
            self.calls.append((elms, flag))

    fake_app = _FakeApp()
    monkeypatch.setattr(type(act_prj), "app", fake_app)

    act_prj.mark_in_graphics(terminal)  # single object used to raise (list(elm))
    act_prj.mark_in_graphics([terminal, terminal])
    assert fake_app.calls == [([terminal], 0), ([terminal, terminal], 0)]


# ---------------------------------------------------------------------------
# §3 / §4 structural refactor
# ---------------------------------------------------------------------------


def test_get_unique_obj_non_unique_raises_typeerror_subclass(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    from powfacpy.exceptions import PFNonUniqueObjectError

    with pytest.raises(PFNonUniqueObjectError):
        act_prj.get_unique_obj(
            r"Network Model\Network Data\test_active_project_interface\Grid\Terminal*"
        )
    # stays catchable as a plain TypeError (backwards compatible)
    with pytest.raises(TypeError):
        act_prj.get_unique_obj(
            r"Network Model\Network Data\test_active_project_interface\Grid\Terminal*"
        )


def test_folder_forwards_unknown_attributes_to_wrapped_object(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    data_folder = Folder(r"Network Model\Network Data", act_prj.app)
    # 'GetClassName' / 'loc_name' are not defined on Folder - forwarded to _obj
    assert data_folder.GetClassName() == data_folder.obj.GetClassName()
    assert data_folder.loc_name == data_folder.obj.loc_name
    # ActiveProject forwards project attributes (used to need .obj / .app detour)
    assert act_prj.GetFullName() == act_prj.get_active_project().GetFullName()
    with pytest.raises(AttributeError):
        data_folder.this_attribute_does_not_exist


def test_active_project_cached_uses_cached_property_for_app_accessors():
    from functools import cached_property
    from powfacpy.base.active_project import ActiveProjectCached, _APP_ACCESSORS

    for name in _APP_ACCESSORS:
        assert isinstance(ActiveProject.__dict__[name], property)
        assert isinstance(ActiveProjectCached.__dict__[name], cached_property)

    # active_study_case must NOT be cached (changes on activation)
    assert isinstance(ActiveProject.__dict__["active_study_case"], property)
    assert "active_study_case" not in ActiveProjectCached.__dict__


def test_folder_accessor_property_aliases(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    assert act_prj.active_user_folder == act_prj.get_active_user_folder()
    assert act_prj.global_library_folder == act_prj.get_global_library_folder()
    act_prj.activate_study_case(
        r"Study Cases\test_active_project_interface\Study Case 1"
    )
    assert act_prj.active_study_case == act_prj.get_active_study_case()


def test_monitored_variables_helper_and_forwarders(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    from powfacpy.base.monitored_variables import MonitoredVariables

    act_prj.activate_study_case(
        r"Study Cases\test_active_project_interface\Study Case 1"
    )
    assert isinstance(act_prj.monitored_variables, MonitoredVariables)
    assert act_prj.monitored_variables is act_prj.monitored_variables  # cached

    terminal = act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )
    results_obj = act_prj.create_in_folder(
        "test_monitored_variables.ElmRes", act_prj.get_active_study_case()
    )
    act_prj.add_results_variable(terminal, "m:u", results_obj=results_obj)  # forwarder
    assert len(results_obj.GetContents("*.IntMon")) >= 1

    act_prj.monitored_variables.clear(results_obj)  # helper directly
    assert len(results_obj.GetContents("*.IntMon")) == 0

    # add_variable_selection_obj_to_results_obj (forwarder + helper)
    intmon = act_prj.add_variable_selection_obj_to_results_obj(
        "sel", results_obj, class_name="ElmTerm", variables=["m:u", "m:phiu"]
    )
    assert intmon.GetClassName() == "IntMon"
    assert intmon.classnm == "ElmTerm"
    assert list(intmon.vars) == ["m:u", "m:phiu"]

    # clear_elmres wipes everything
    act_prj.clear_elmres(results_obj)
    assert results_obj.GetContents("*") == []

    # clear_elmres_from_objects_with_status_deleted removes stale entries
    act_prj.add_results_variable(terminal, "m:u", results_obj=results_obj)
    terminal_to_delete = act_prj.create_in_folder(
        "tc_stale_terminal.ElmTerm",
        r"Network Model\Network Data\test_active_project_interface\Grid",
    )
    act_prj.add_results_variable(terminal_to_delete, "m:u", results_obj=results_obj)
    n_before = len(results_obj.GetContents("*"))
    terminal_to_delete.Delete()
    act_prj.clear_elmres_from_objects_with_status_deleted(results_obj)
    assert len(results_obj.GetContents("*")) == n_before - 1

    results_obj.Delete()


# ===========================================================================
# Safety net for the pending §4 helper extractions (Paths / StudyCases /
# Projects). These exercise the cohesive method groups that are going to move
# into composed helpers behind the same public API.
# ===========================================================================

# --- path helpers (future `Paths`) -----------------------------------------

_LINE_PATH = (
    r"Network Model\Network Data\test_active_project_interface\Grid\Line 1.2"
)


def test_path_of_object_relative_full_project_user(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    line = act_prj.get_unique_obj(_LINE_PATH)
    project = act_prj.get_active_project()

    # relative to the folder object (the active project, for ActiveProject)
    assert act_prj.get_path_of_object(line) == _LINE_PATH
    with_classes = act_prj.get_path_of_obj_with_class_names(line)
    assert with_classes.startswith("Network Model.IntPrjfolder\\")
    assert with_classes.endswith("Line 1.2.ElmLne")
    assert PFStringManipulation.remove_class_names(with_classes) == _LINE_PATH

    # relative to the active project (same as folder here) and to the user
    assert act_prj.get_path_of_object_in_active_project(line) == _LINE_PATH
    assert (
        act_prj.get_path_of_object_in_active_project_with_class_names(line)
        == with_classes
    )
    user_rel = act_prj.get_path_of_object_in_current_user(line)
    assert user_rel.endswith(f"{project.loc_name}\\{_LINE_PATH}")
    assert user_rel.count("\\") > _LINE_PATH.count("\\")  # user-relative is longer
    assert act_prj.get_path_of_object_in_current_user_with_class_names(
        line
    ).endswith("Line 1.2.ElmLne")

    # full database path
    full = act_prj.get_full_path_of_object(line)
    assert full.startswith("\\") and full.endswith(_LINE_PATH)
    assert act_prj.get_full_path_of_object_with_class_names(line) == line.GetFullName()

    # a path string is accepted wherever an object is
    assert act_prj.get_path_of_object(_LINE_PATH) == _LINE_PATH


def test_get_path_between_objects(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    grid = r"Network Model\Network Data\test_active_project_interface\Grid"
    assert act_prj.get_path_between_objects(grid, grid + r"\Line 1.2") == "Line 1.2"


def test_paths_helper_and_forwarders(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    from powfacpy.base.paths import Paths

    line = act_prj.get_unique_obj(_LINE_PATH)
    assert isinstance(act_prj.paths, Paths)
    assert act_prj.paths is act_prj.paths  # cached

    # helper methods match the forwarders one-for-one
    assert act_prj.paths.of(line) == act_prj.get_path_of_object(line) == _LINE_PATH
    assert act_prj.paths.of(line, with_class_names=True) == (
        act_prj.get_path_of_obj_with_class_names(line)
    )
    assert act_prj.paths.absolute(line) == act_prj.get_full_path_of_object(line)
    assert act_prj.paths.in_active_project(line) == (
        act_prj.get_path_of_object_in_active_project(line)
    )
    assert act_prj.paths.in_current_user(line) == (
        act_prj.get_path_of_object_in_current_user(line)
    )
    assert act_prj.paths.between(
        r"Network Model\Network Data\test_active_project_interface\Grid",
        _LINE_PATH,
    ) == "Line 1.2"


def test_replace_special_pf_characters_in_path_string(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    workspace = act_prj.get_workspace_directory()
    installation = act_prj.get_installation_directory()
    assert act_prj._replace_special_PF_characters_in_path_string(
        r"$(WorkspaceDir)\x\$(InstallationDir)\y"
    ) == rf"{workspace}\x\{installation}\y"
    # unchanged when there is nothing to replace
    assert (
        act_prj._replace_special_PF_characters_in_path_string(r"C:\plain\path")
        == r"C:\plain\path"
    )
    # $(ExtDataDir) branch (external data dir is usually empty -> replaced by "")
    ext = act_prj.get_external_data_directory()
    assert act_prj._replace_special_PF_characters_in_path_string(
        r"$(ExtDataDir)\file"
    ) == rf"{ext}\file"


def test_get_project_settings(act_prj: ActiveProject, activate_powfacpy_test_project):
    assert act_prj.get_project_settings().GetClassName() == "SetPrj"


def test_path_exists_return_info_and_invalid_input(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    assert act_prj.path_exists(r"Network Model\Network Data") is True
    exists, existing_path, missing_child = act_prj.path_exists(
        r"Network Model\Does Not Exist\Deeper", return_info=True
    )
    assert exists is False
    assert missing_child == "Does Not Exist"
    assert existing_path.endswith("Network Model")
    with pytest.raises(Exception):  # PFPathInputError - leading backslash
        act_prj.path_exists(r"\Network Model")


# --- study case / variation / scenario creation (future `StudyCases`) ------


def test_create_study_case_branches(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    sc_folder = act_prj.study_cases_folder
    created_case_names = ["tc_plain", "tc_copy", "tc_nested", "tc_flat", "tc_full"]
    try:
        plain = act_prj.create_study_case("tc_plain")
        assert plain.GetClassName() == "IntCase"
        assert act_prj.get_active_study_case() == plain  # activate=True default

        from_existing = act_prj.create_study_case(
            "tc_copy",
            copy_from=r"Study Cases\test_active_project_interface\Study Case 1",
            activate=False,
        )
        assert from_existing.loc_name == "tc_copy"

        # parent_folder path containing "\" -> created via create_by_path
        nested = act_prj.create_study_case(
            "tc_nested", parent_folder=r"Study Cases\tc_sub", activate=False
        )
        assert act_prj.get_path_of_object(nested) == r"Study Cases\tc_sub\tc_nested"

        # parent_folder as a bare name -> subfolder of the study cases folder
        in_subfolder = act_prj.create_study_case(
            "tc_flat", parent_folder="tc_bare", activate=False
        )
        assert in_subfolder.GetParent().loc_name == "tc_bare"
        assert in_subfolder.GetParent().GetParent() == sc_folder

        objs = act_prj.create_study_case(
            "tc_full", create_variation=True, create_scenario=True, activate=False
        )
        assert [o.GetClassName() for o in objs] == [
            "IntCase",
            "IntScheme",
            "IntScenario",
        ]
    finally:
        for scheme in act_prj.get_obj(
            "tc_*", parent_folder=act_prj.variations_folder, error_if_non_existent=False
        ):
            scheme.Deactivate()
        for scenario in act_prj.get_obj(
            "tc_*",
            parent_folder=act_prj.operation_scenarios_folder,
            error_if_non_existent=False,
        ):
            scenario.Deactivate()
        for name in created_case_names:
            act_prj.delete_obj(
                f"{name}.IntCase", parent_folder=sc_folder, error_if_non_existent=False
            )
        for folder_name in ("tc_sub.IntPrjfolder", "tc_bare.IntPrjfolder"):
            act_prj.delete_obj(
                folder_name, parent_folder=sc_folder, error_if_non_existent=False
            )
        act_prj.delete_obj(
            "tc_*", parent_folder=act_prj.variations_folder, error_if_non_existent=False
        )
        act_prj.delete_obj(
            "tc_*",
            parent_folder=act_prj.operation_scenarios_folder,
            error_if_non_existent=False,
        )


def test_create_variation_and_scenario_directly(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    act_prj.activate_study_case(
        r"Study Cases\test_active_project_interface\Study Case 1"
    )
    try:
        variation = act_prj.create_variation("tc_var", activate=True)
        assert variation.GetClassName() == "IntScheme"
        assert len(variation.GetContents("*.IntSstage")) == 1

        scenario = act_prj.create_scenario("tc_scen", activate=True)
        assert scenario.GetClassName() == "IntScenario"
        assert act_prj.app.GetActiveScenario() == scenario
    finally:
        for name, folder in (
            ("tc_var", act_prj.variations_folder),
            ("tc_scen", act_prj.operation_scenarios_folder),
        ):
            obj = act_prj.get_unique_obj(
                name, parent_folder=folder, error_if_non_existent=False
            )
            if obj:
                obj.Deactivate()
                obj.Delete()


def test_create_parallel_variation_mirrors_study_case_subfolder(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    case = act_prj.get_unique_obj(
        r"Study Cases\test_active_project_interface\Study Case 1"
    )
    # the study case sits in the 'test_active_project_interface' subfolder, so
    # the parallel variation must land in the same-named subfolder
    assert (
        act_prj._get_path_of_folder_of_study_case_inside_study_cases_folder(case)
        == "test_active_project_interface"
    )
    try:
        variation = act_prj.create_parallel_variation_for_study_case(
            case, activate=False
        )
        assert variation.GetClassName() == "IntScheme"
        assert variation.loc_name == case.loc_name
        # placed in a 'test_active_project_interface' subfolder of the variations folder
        assert variation.GetParent().loc_name == "test_active_project_interface"
        assert variation.GetParent().GetParent() == act_prj.variations_folder
    finally:
        act_prj.delete_obj(
            r"test_active_project_interface\Study Case 1.IntScheme",
            parent_folder=act_prj.variations_folder,
            error_if_non_existent=False,
        )

    # a case directly in the study cases folder -> no subfolder
    top_case = act_prj.create_study_case("tc_top", activate=False)
    try:
        assert (
            act_prj._get_path_of_folder_of_study_case_inside_study_cases_folder(
                top_case
            )
            is None
        )
    finally:
        top_case.Delete()


# --- project lifecycle (future `Projects`) --------------------------------


def test_project_version_create_get_overwrite_rollback(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    version_name = "tc_safety_net_version"
    term_path = (
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )
    original_uknom = act_prj.get_unique_obj(term_path).uknom
    try:
        assert act_prj.get_project_version(version_name) is None
        act_prj.create_project_version(version_name)
        version = act_prj.get_project_version(version_name)
        assert version is not None and version.GetClassName() == "IntVersion"

        # overwrite=True replaces the existing version rather than erroring
        act_prj.create_project_version(version_name)
        assert (
            len(
                [
                    v
                    for v in act_prj._obj.GetVersions()
                    if v.loc_name == version_name
                ]
            )
            == 1
        )

        act_prj.get_unique_obj(term_path).uknom = original_uknom + 7.0
        act_prj.rollback_project_to_previous_version(version_name)
        assert act_prj.get_unique_obj(term_path).uknom == pytest.approx(
            original_uknom
        )
    finally:
        leftover = act_prj.get_project_version(version_name)
        if leftover:
            leftover.Delete()
        act_prj.get_unique_obj(term_path).uknom = original_uknom


def test_reactivate_project(act_prj: ActiveProject, activate_powfacpy_test_project):
    project = act_prj.get_active_project()
    act_prj.reactivate_project()
    assert act_prj.get_active_project() == project


def test_set_time_using_year(act_prj: ActiveProject, activate_powfacpy_test_project):
    act_prj.activate_study_case(
        r"Study Cases\test_active_project_interface\Study Case 1"
    )
    act_prj.set_time_using_year(2035)
    settime = act_prj.get_from_study_case("SetTime")
    # SetTimeUTC was called with an approximate epoch for 2035
    assert 2033 <= _utc_year(settime) <= 2037


def _utc_year(settime) -> int:
    import datetime

    return datetime.datetime.fromtimestamp(
        settime.GetTimeUTC(), datetime.timezone.utc
    ).year


def test_execute_load_flow_and_check_results(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    act_prj.activate_study_case(
        r"Study Cases\test_active_project_interface\Study Case 1"
    )
    assert act_prj.execute_load_flow() == 0
    assert act_prj.has_valid_load_flow_results() is True
    assert act_prj.check_load_flow_results() is True
    assert act_prj.check_load_flow_results(when_invalid="execute") is True

    # a freshly (re)activated study case has no valid load flow results
    act_prj.activate_study_case(
        r"Study Cases\test_active_project_interface\multiple_elmres"
    )
    if act_prj.has_valid_load_flow_results():
        pytest.skip("load flow unexpectedly still valid after switching study case")
    with pytest.raises(Exception):  # PFInvalidLoadFlow
        act_prj.check_load_flow_results(when_invalid="error")
    with pytest.warns(UserWarning):
        assert act_prj.check_load_flow_results(when_invalid="warning") is False


def test_import_dz_file(act_prj: ActiveProject, activate_powfacpy_test_project):
    dz_path = os.path.abspath(r"tests\tests_input\Stochastic load.dz")
    target = act_prj.create_in_folder(
        "tc_dz_import.IntFolder", act_prj.get_active_project()
    )
    try:
        act_prj.import_dz_file(dz_path, target_folder=target)
        assert len(target.GetContents("*")) > 0
    finally:
        target.Delete()


def test_duplicate_to_restore_attributes(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    term_path = (
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )
    terminal = act_prj.get_unique_obj(term_path)
    original_uknom = terminal.uknom
    copy_name = terminal.loc_name + "_COPY"
    try:
        # first call: no copy yet -> a duplicate is created
        act_prj.duplicate_to_restore_attributes(terminal, "uknom")
        duplicate = act_prj.get_unique_obj(
            copy_name, parent_folder=terminal.GetParent()
        )
        assert duplicate.uknom == pytest.approx(original_uknom)

        # second call: copy exists -> the stored value is written back
        terminal.uknom = original_uknom + 13.0
        act_prj.duplicate_to_restore_attributes(terminal, ["uknom"])
        assert terminal.uknom == pytest.approx(original_uknom)
    finally:
        leftover = act_prj.get_unique_obj(
            copy_name, parent_folder=terminal.GetParent(), error_if_non_existent=False
        )
        if leftover:
            leftover.Delete()
        terminal.uknom = original_uknom


# --- remaining Folder gaps ------------------------------------------------


def test_get_obj_partial_and_including_subfolders(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    lazy = act_prj.get_obj_partial(
        r"Network Data\test_active_project_interface\*.ElmTerm",
        parent_folder="Network Model",
        include_subfolders=True,
    )
    assert len(lazy()) == 3
    assert (
        len(
            act_prj.get_obj_including_subfolders(
                r"Network Data\test_active_project_interface\*.ElmTerm",
                parent_folder="Network Model",
            )
        )
        == 3
    )


def test_create_filter_obj(act_prj: ActiveProject, activate_powfacpy_test_project):
    grid = r"Network Model\Network Data\test_active_project_interface\Grid"
    filter_obj = act_prj.create_filter_obj(
        "tc_filter",
        folder=act_prj.get_active_project(),
        object_filter="*.ElmTerm",
        look_in=grid,
        expression="uknom>50",
    )
    try:
        assert filter_obj.GetClassName() == "SetFilt"
        assert filter_obj.objset == ["*.ElmTerm"]
        assert filter_obj.expr == ["uknom>50"]
        assert filter_obj.pstart == act_prj.get_unique_obj(grid)
    finally:
        filter_obj.Delete()


def test_is_pf_class_and_is_container(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    assert act_prj.is_pf_class("ElmTerm") is True
    assert act_prj.is_pf_class("NotARealClass") is False
    assert act_prj.is_container(r"Network Model\Network Data")
    assert not act_prj.is_container(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )


def test_get_multiple_obj_from_similar_sub_directories(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    grids = act_prj.get_obj(
        "*", parent_folder=r"Network Model\Network Data\test_active_project_interface"
    )
    parents = [g for g in grids if g.GetClassName() == "ElmNet"]
    # every grid has a 'Grid' terminal set? use a child known to exist: none is
    # guaranteed, so build the fixture explicitly
    for i, parent in enumerate(parents):
        act_prj.create_in_folder("tc_similar_child.IntFolder", parent)
    try:
        children = act_prj.get_multiple_obj_from_similar_sub_directories(
            parents, "tc_similar_child"
        )
        assert len(children) == len(parents)
        assert all(c.GetClassName() == "IntFolder" for c in children)
    finally:
        for parent in parents:
            act_prj.delete_obj(
                "tc_similar_child.IntFolder",
                parent_folder=parent,
                error_if_non_existent=False,
            )


def test_input_handlers_iterable_branches(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    grid = r"Network Model\Network Data\test_active_project_interface\Grid"
    # _handle_pf_object_or_path_input with a list of path strings
    resolved = act_prj._handle_pf_object_or_path_input(
        [grid + r"\Terminal HV 1", grid + r"\Terminal HV 2"]
    )
    assert len(resolved) == 2

    # _handle_single_pf_object_or_path_input rejects iterables with a helpful error
    with pytest.raises(TypeError):
        act_prj._handle_single_pf_object_or_path_input([5, 6])  # non-obj first elem
    with pytest.raises(TypeError):
        act_prj._handle_single_pf_object_or_path_input([])  # empty iterable


def test_copy_single_obj_use_existing_and_copy_project(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    src = act_prj.get_unique_obj(r"Library\Dynamic Models\Linear_interpolation")
    target = act_prj.create_in_folder(
        "tc_copy_target.IntFolder", r"Library\Dynamic Models"
    )
    try:
        first = act_prj.copy_single_obj(src, target)
        again = act_prj.copy_single_obj(src, target, use_existing=True)
        assert again == first  # returned the existing copy, no duplicate
        assert len(target.GetContents(f"{src.loc_name}*")) == 1
    finally:
        target.Delete()

    project = act_prj.get_active_project()
    copy = act_prj.copy_project(new_name="tc_project_copy")
    try:
        assert copy.GetClassName() == "IntPrj"
        assert copy.loc_name == "tc_project_copy"
    finally:
        copy.Delete()
        project.Activate()


def test_composed_helpers_are_cached(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    from powfacpy.base.paths import Paths
    from powfacpy.base.monitored_variables import MonitoredVariables
    from powfacpy.base.study_cases import StudyCases
    from powfacpy.base.projects import Projects
    from powfacpy.base.object_operations import ObjectOperations

    for name, cls in (
        ("paths", Paths),
        ("monitored_variables", MonitoredVariables),
        ("study_cases", StudyCases),
        ("projects", Projects),
        ("objects", ObjectOperations),
    ):
        helper = getattr(act_prj, name)
        assert isinstance(helper, cls)
        assert getattr(act_prj, name) is helper  # cached_property


def test_study_cases_and_projects_helpers_forward(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    # StudyCases helper vs forwarder
    try:
        case = act_prj.study_cases.create("tc_helper_case", activate=False)
        assert case.GetClassName() == "IntCase"
        variation = act_prj.study_cases.create_variation("tc_helper_var", activate=0)
        assert variation.GetClassName() == "IntScheme"
    finally:
        act_prj.delete_obj(
            "tc_helper_case.IntCase",
            parent_folder=act_prj.study_cases_folder,
            error_if_non_existent=False,
        )
        act_prj.delete_obj(
            "tc_helper_var.IntScheme",
            parent_folder=act_prj.variations_folder,
            error_if_non_existent=False,
        )

    # Projects helper vs forwarder
    version = "tc_helper_version"
    try:
        act_prj.projects.create_version(version)
        assert act_prj.get_project_version(version) == act_prj.projects.get_version(
            version
        )
    finally:
        leftover = act_prj.projects.get_version(version)
        if leftover:
            leftover.Delete()

    project = act_prj.get_active_project()
    act_prj.projects.reactivate()
    assert act_prj.get_active_project() == project


def test_get_first_level_folder_invalid_input(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    assert act_prj.get_first_level_folder("user") == act_prj.get_active_user_folder()
    assert (
        act_prj.get_first_level_folder("global library")
        == act_prj.get_global_library_folder()
    )
    with pytest.raises(TypeError):
        act_prj.get_first_level_folder("nonsense")


if __name__ == "__main__":
    # pytest.main([r"tests\base\test_active_project.py"])
    # pytest.main([r"tests"])
    # pytest.main([r"tests\applications\test_study_cases.py"])
    # pytest.main([r"tests\pf_classes"])
    pytest.main([r"tests"])


def test_objects_helper_forwarders_and_clear_folder(
    act_prj: ActiveProject, activate_powfacpy_test_project
):
    """Folder.copy_obj/move_single_obj/clear_folder forward to `Folder.objects`."""
    project = act_prj.get_active_project()
    src = act_prj.create_in_folder("tc_objects_src.IntFolder", project)
    dst = act_prj.create_in_folder("tc_objects_dst.IntFolder", project)
    dst_2 = act_prj.create_in_folder("tc_objects_dst_2.IntFolder", project)
    child = act_prj.create_in_folder("tc_objects_child.IntFolder", src)

    copied = act_prj.copy_obj(child, dst)
    assert [o.loc_name for o in copied] == ["tc_objects_child"]
    assert act_prj.objects.copy(child, dst_2)[0].loc_name == "tc_objects_child"

    act_prj.move_single_obj(copied[0], dst_2)  # overwrites the copy already in dst_2
    assert dst.GetContents("*") == []
    assert len(dst_2.GetContents("*")) == 1

    act_prj.clear_folder(dst_2)
    assert dst_2.GetContents("*") == []

    for folder in (src, dst, dst_2):
        act_prj.delete_obj(folder)
