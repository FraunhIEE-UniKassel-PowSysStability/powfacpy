"""Tests for the class ActiveProject.

The class 'ActiveProject' inherits from 'Folder'. There are no separate tests for the 'Folder' class, all tests for both classes are included here.
"""

import sys
import os
import json
import importlib

import pytest

with open(".\\settings.json") as settings_file:
    settings = json.load(settings_file)
sys.path.append(settings["local path to PowerFactory application"])
import powerfactory

sys.path.insert(0, r".\src")
import powfacpy
from powfacpy.applications.folder import Folder
import powfacpy.exceptions

importlib.reload(powfacpy)


def test_get_obj(act_prj, activate_test_project):
    terminal_1 = act_prj.get_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )[0]
    assert isinstance(terminal_1, powerfactory.DataObject)
    with pytest.raises(powfacpy.exceptions.PFPathError):
        terminal_1 = act_prj.get_obj(
            r"Stretchwork Model\Stretchwork Data\Grid\Termalamala"
        )[0]
    with pytest.raises(powfacpy.exceptions.PFPathError):
        terminal_1 = act_prj.get_obj(r"N")[0]
    with pytest.raises(TypeError):
        terminal_1 = act_prj.get_obj(terminal_1)[0]
    with pytest.raises(TypeError):
        terminal_1 = act_prj.get_obj(terminal_1, include_subfolders=False)[0]


def test_get_single_object(act_prj, activate_test_project):
    terminal_1 = act_prj.get_single_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )
    assert isinstance(terminal_1, powerfactory.DataObject)
    with pytest.raises(TypeError):
        terminals = act_prj.get_single_obj(
            r"Network Model\Network Data\test_active_project_interface\Grid\Terminal*"
        )


def test_get_obj_with_condition(act_prj, activate_test_project):
    hv_terminals = act_prj.get_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal*",
        condition=lambda x: getattr(x, "uknom") > 50,
    )
    assert len(hv_terminals) == 2


def test_get_obj_with_parent_folder_argument(act_prj, activate_test_project):
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


def test_get_obj_including_subfolders(act_prj, activate_test_project):
    terminals = act_prj.get_obj(
        r"Network Data\test_active_project_interface\*.ElmTerm",
        parent_folder="Network Model",
        include_subfolders=True,
    )
    assert len(terminals) == 3


def test_path_exists(act_prj, activate_test_project):
    assert act_prj.path_exists(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )


def test_set_attr(act_prj, activate_test_project):
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


def test_set_attr_exceptions(act_prj, activate_test_project):
    with pytest.raises(powfacpy.exceptions.PFAttributeTypeError):
        act_prj.set_attr(
            r"Library\Dynamic Models\Linear_interpolation",
            {"sTitle": "dummy", "desc": 2},
        )  # "desc" should be a list with one string item
    with pytest.raises(powfacpy.exceptions.PFAttributeError):
        act_prj.set_attr(
            r"Library\Dynamic Models\Linear_interpolation",
            {"sTie": "dummy", "desc": ["dummy description"]},
        )  # 'sTie' is not a valid attribute
    with pytest.raises(powfacpy.exceptions.PFPathError):
        terminal_1 = act_prj.get_obj(
            r"Network Model\Network Data\test_active_project_interface\Grid\Termalamala"
        )


def test_set_attr_by_path(act_prj, activate_test_project):
    act_prj.set_attr_by_path(
        r"Library\Dynamic Models\Linear_interpolation\desc", ["description"]
    )
    with pytest.raises(powfacpy.exceptions.PFPathError):
        act_prj.set_attr_by_path(
            r"Stretchwork Model\Stretchwork Data\Grid\Termalamala", ["description"]
        )


def test_get_attr(act_prj, activate_test_project):
    terminal_1 = act_prj.get_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1"
    )[0]
    systype = act_prj.get_attr(terminal_1, "systype")
    assert systype == 0
    with pytest.raises(powfacpy.exceptions.PFAttributeError):
        systype = act_prj.get_attr(terminal_1, "trixi")


def test_create_by_path(act_prj, activate_test_project):
    act_prj.create_by_path(r"Library\Dynamic Models\dummy.BlkDef")
    with pytest.raises(powfacpy.exceptions.PFPathError):
        act_prj.create_by_path(r"ry\Dynamic Models\dummy.BlkDef")
    with pytest.raises(TypeError):
        act_prj.create_by_path(4)


def test_create_in_folder(act_prj, activate_test_project):
    act_prj.create_in_folder("dummy2.BlkDef", r"Library\Dynamic Models")
    with pytest.raises(TypeError):
        act_prj.create_in_folder(2, r"Library\Dynamic Models")


def test_get_by_condition(act_prj, activate_test_project):
    folder = r"Network Model\Network Data\test_active_project_interface\Grid"
    all_terminals = act_prj.get_obj("*.ElmTerm", parent_folder=folder)

    mv_terminals = act_prj.get_by_condition(
        all_terminals, lambda x: getattr(x, "uknom") > 100
    )
    assert len(mv_terminals) == 2

    with pytest.raises(powfacpy.exceptions.PFAttributeError):
        mv_terminals = act_prj.get_by_condition(
            all_terminals, lambda x: getattr(x, "wrong_attr") > 100
        )


def test_delete_obj(act_prj, activate_test_project):
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
        "*", parent_folder=folder, error_if_non_existent=False
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
    objects_in_folder = act_prj.get_obj("*", parent_folder=folder)
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
        "*", parent_folder=folder, error_if_non_existent=False
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
    object_in_folder = act_prj.get_single_obj("*", parent_folder=folder)
    act_prj.delete_obj(object_in_folder)
    objects_in_folder = act_prj.get_obj(
        "*", parent_folder=folder, error_if_non_existent=False
    )
    assert len(objects_in_folder) == 0


def test_copy_obj(act_prj, activate_test_project):
    folder_copy_from = r"Library\Dynamic Models\TestCopyFrom"
    folder_copy_to = r"Library\Dynamic Models\TestCopyTo"

    act_prj.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    copied_objects = act_prj.copy_obj(
        "*", folder_copy_to, parent_folder=folder_copy_from
    )
    assert len(copied_objects) == 2
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
    assert len(copied_objects) == 2

    objects_to_copy = act_prj.get_obj("*", parent_folder=folder_copy_from)
    copied_objects = act_prj.copy_obj(objects_to_copy, folder_copy_to, overwrite=False)
    assert len(copied_objects) == 2
    all_objects_in_folder = act_prj.get_obj("*", parent_folder=folder_copy_to)
    assert len(all_objects_in_folder) == 4

    act_prj.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    objects_to_copy = act_prj.get_obj("*", parent_folder=folder_copy_from)[0]
    copied_objects = act_prj.copy_obj(objects_to_copy, folder_copy_to, overwrite=False)
    assert len(copied_objects) == 1
    all_objects_in_folder = act_prj.get_obj("*", parent_folder=folder_copy_to)
    assert len(all_objects_in_folder) == 1


def test_copy_single_obj(act_prj, activate_test_project):
    folder_copy_from = r"Library\Dynamic Models\TestDummyFolder"
    folder_copy_to = r"Library\Dynamic Models\TestCopy"

    act_prj.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    copied_object = act_prj.copy_single_obj(
        "dummy.*",
        folder_copy_to,
        parent_folder=folder_copy_from,
        new_name="new_dummy_name",
    )
    copied_obj_from_folder = act_prj.get_single_obj(
        "new_dummy_name", parent_folder=folder_copy_to
    )
    assert copied_object == copied_obj_from_folder

    obj_to_copy = act_prj.get_single_obj("dummy2.*", parent_folder=folder_copy_from)
    copied_object = act_prj.copy_single_obj(obj_to_copy, folder_copy_to, overwrite=True)
    copied_obj_from_folder = act_prj.get_single_obj(
        "dummy2", parent_folder=folder_copy_to
    )
    assert copied_object == copied_obj_from_folder

    act_prj.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    obj_to_copy = act_prj.get_single_obj("dummy2.*", parent_folder=folder_copy_from)
    copied_object = act_prj.copy_single_obj(
        obj_to_copy,
        folder_copy_to,
        overwrite=False,
        parent_folder=folder_copy_from,
        new_name="new_dummy_name",
    )
    copied_obj_from_folder = act_prj.get_single_obj(
        "new_dummy_name", parent_folder=folder_copy_to
    )
    assert copied_object == copied_obj_from_folder


def test_handle_single_pf_object_or_path_input(act_prj, activate_test_project):
    folder = act_prj.get_obj(r"Network Model\Network Data")[0]
    with pytest.raises(TypeError):
        act_prj._handle_single_pf_object_or_path_input([folder])

    same_folder_returned = act_prj._handle_single_pf_object_or_path_input(folder)
    assert same_folder_returned == folder

    same_folder_using_string = act_prj._handle_single_pf_object_or_path_input(
        r"Network Model\Network Data"
    )
    assert same_folder_using_string == folder


def test_get_parameter_value_string(act_prj, activate_test_project):
    params = {
        "p": r"Network Model\Network Data\test_active_project_interface\Grid\General Load HV\plini",
        "q": r"Network Model\Network Data\test_active_project_interface\Grid\General Load HV\qlini",
        "u": r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 2\uknom",
    }
    act_prj.get_parameter_value_string(params, delimiter=" ")


def test_create_directory(act_prj, activate_test_project):
    act_prj.create_directory(
        r"test1\test2", parent_folder=r"Study Cases\test_case_studies"
    )

    act_prj.create_directory(
        r"test1\test2\test3\test4", parent_folder=r"Study Cases\test_case_studies"
    )
    act_prj.delete_obj("test1", parent_folder=r"Study Cases\test_case_studies")

    act_prj.create_directory(r"test1\test2")
    act_prj.delete_obj("test1")


def test_get_loc_name_with_class(act_prj, activate_test_project):
    pf_objects = act_prj.get_obj(r"*.ElmTerm", include_subfolders=True)
    act_prj.get_loc_name_with_class(pf_objects)
    act_prj.get_loc_name_with_class(pf_objects[0])


def test_create_comtrade_obj(act_prj, activate_test_project):
    path_of_cfg = os.getcwd() + r"\tests\tests_input\test_comtrade.cfg"
    intcomtrade = act_prj.create_comtrade_obj(path_of_cfg)
    intcomtrade.Load()
    assert intcomtrade.FindColumn("AC Voltage Source:m:u:bus1:A") == 1


def test_replace_outside_or_inside_of_strings_in_a_string(
    act_prj, activate_test_project
):
    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1' control 1"
    conditions = (
        powfacpy.PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
            conditions, {"control 1": "x[1]"}
        )
    )
    assert conditions == "lorem ipsum x[1] == 'ABC control 1' 'control 1' x[1]"

    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1'"
    conditions = (
        powfacpy.PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
            conditions, {"control 1": "x[1]"}
        )
    )
    assert conditions == "lorem ipsum x[1] == 'ABC control 1' 'control 1'"

    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1' "
    conditions = (
        powfacpy.PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
            conditions, {"control 1": "x[1]"}
        )
    )
    assert conditions == "lorem ipsum x[1] == 'ABC control 1' 'control 1'"

    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1' "
    conditions = (
        powfacpy.PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
            conditions, {"control 1": "x[1]"}, outside=False
        )
    )
    assert conditions == "lorem ipsum control 1 == 'ABC x[1]' 'x[1]'"


def test_get_path_of_object(act_prj, activate_test_project):
    path = "Network Model\\Network Data\\test_active_project_interface\\Grid\\Line 1.2"
    line = act_prj.get_unique_obj(path)
    path_derived = act_prj.get_path_of_object(line)
    assert path == path_derived


def test_get_upstream_object(act_prj, activate_test_project):
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


def test_get_from_study_case(act_prj, activate_test_project):
    act_prj.activate_study_case(
        r"Study Cases\test_active_project_interface\multiple_elmres"
    )
    with pytest.warns():
        act_prj.get_from_study_case("ElmRes")
    with pytest.raises(Exception):
        act_prj.get_from_study_case("ElmRes", if_not_unique="error")


def test_get_calc_relevant_obj(act_prj, activate_test_project):
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

    with pytest.raises(powfacpy.exceptions.PFNonExistingObjectError):
        act_prj.get_calc_relevant_obj("*.ElmTerm", condition=lambda x: x.uknom > 5000)


if __name__ == "__main__":
    # pytest.main([r"tests\applications\test_active_project.py"])
    # pytest.main([r"tests"])
    # pytest.main([r"tests\applications"])
    # pytest.main([r"tests\pf_classes"])
    pytest.main([r"tests"])
