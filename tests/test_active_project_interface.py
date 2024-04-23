"""Tests for the class PFActiveProject.

The class PFActiveProject inherits from PFFolder. There are no separate tests for the PFFolder class, all tests for both classes are included here.
"""
import sys
import os
import json
import importlib

import pytest

with open('.\\settings.json') as settings_file:
    settings = json.load(settings_file)
sys.path.append(settings["local path to PowerFactory application"])
import powerfactory

sys.path.insert(0, r'.\src')
import powfacpy 
importlib.reload(powfacpy)


@pytest.fixture(scope='session')
def pf_app():
    return powerfactory.GetApplication()


@pytest.fixture(scope='session')
def pfp(pf_app) -> powfacpy.PFActiveProject:
    # Return PFActiveProject instance
    return powfacpy.PFActiveProject(pf_app)   


@pytest.fixture()
def activate_test_project(pfp):
    """The project for testing must be located in the current
    user under "powfacpy\\powfacpy_tests". This method will create
    a copy of that project which is then used for the tests. This 
    ensures that the tests are always run with the same initial
    project state.
    """
    user = pfp.app.GetCurrentUser()
    project_for_testing = pfp.get_single_obj(r"powfacpy\powfacpy_tests",
        parent_folder = user, include_subfolders=False)
    folder_of_project_for_testing = pfp.get_single_obj(r"powfacpy",
        parent_folder = user, include_subfolders=False)   
    project_copy = pfp.copy_single_obj(project_for_testing,
        folder_of_project_for_testing, 
        new_name="powfacpy_tests_copy_where_tests_are_run")    
    project_copy.Activate()   
    

def test_get_obj(pfp, activate_test_project):
    terminal_1 = pfp.get_obj(r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1")[0]
    assert isinstance(terminal_1, powerfactory.DataObject)
    with pytest.raises(powfacpy.PFPathError):
        terminal_1 = pfp.get_obj(r"Stretchwork Model\Stretchwork Data\Grid\Termalamala")[0]
    with pytest.raises(powfacpy.PFPathError):
        terminal_1 = pfp.get_obj(r"N")[0]    
    with pytest.raises(TypeError):
        terminal_1 = pfp.get_obj(terminal_1)[0]
    with pytest.raises(TypeError):
        terminal_1 = pfp.get_obj(terminal_1, include_subfolders=False)[0]


def test_get_single_object(pfp, activate_test_project):
    terminal_1=pfp.get_single_obj(r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1") 
    assert isinstance(terminal_1, powerfactory.DataObject)
    with pytest.raises(TypeError):
       terminals=pfp.get_single_obj(r"Network Model\Network Data\test_active_project_interface\Grid\Terminal*")  


def test_get_obj_with_condition(pfp, activate_test_project):
    hv_terminals = pfp.get_obj(r"Network Model\Network Data\test_active_project_interface\Grid\Terminal*",
        condition=lambda x: getattr(x,"uknom") > 50)
    assert len(hv_terminals) == 2    


def test_get_obj_with_parent_folder_argument(pfp, activate_test_project):
    parent_folder = pfp.get_first_level_folder("user")
    terminal_1 = pfp.get_obj(r"powfacpy\powfacpy_tests\Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1",
        parent_folder=parent_folder)[0]
    assert isinstance(terminal_1, powerfactory.DataObject)

    grid = pfp.get_obj("Grid", parent_folder=r"Network Model\Network Data\test_active_project_interface")[0]
    assert isinstance(grid, powerfactory.DataObject)
    
    parent_folder = powfacpy.PFFolder(r"Network Model\Network Data\test_active_project_interface", pfp.app)
    grid = pfp.get_obj("Grid", parent_folder=parent_folder)[0]
    assert isinstance(grid, powerfactory.DataObject)


def test_get_obj_including_subfolders(pfp, activate_test_project):
    terminals = pfp.get_obj(r"Network Data\test_active_project_interface\*.ElmTerm", parent_folder="Network Model",
        include_subfolders=True) 
    assert len(terminals) == 3    


def test_path_exists(pfp, activate_test_project):
    assert pfp.path_exists(r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1")


def test_set_attr(pfp, activate_test_project):
    test_string_1 = "TestString1"
    test_string_2 = "TestString2"
    pfp.set_attr(r"Library\Dynamic Models\Linear_interpolation",{"sTitle":test_string_1})
    pfp.set_attr("Linear_interpolation",{"sTitle":test_string_2,
        "desc":["dummy description"]}, parent_folder=r"Library\Dynamic Models")
    stitle = pfp.get_attr(r"Library\Dynamic Models\Linear_interpolation","sTitle")
    assert stitle == test_string_2


def test_set_attr_exceptions(pfp, activate_test_project):
    with pytest.raises(powfacpy.exceptions.PFAttributeTypeError):
        pfp.set_attr(r"Library\Dynamic Models\Linear_interpolation",{"sTitle":"dummy",
        "desc":2}) # "desc" should be a list with one string item
    with pytest.raises(powfacpy.exceptions.PFAttributeError):
        pfp.set_attr(r"Library\Dynamic Models\Linear_interpolation",{"sTie":"dummy",
        "desc":["dummy description"]}) # 'sTie' is not a valid attribute 
    with pytest.raises(powfacpy.exceptions.PFPathError):
        terminal_1 = pfp.get_obj(r"Network Model\Network Data\test_active_project_interface\Grid\Termalamala")


def test_set_attr_by_path(pfp, activate_test_project):
    pfp.set_attr_by_path(r"Library\Dynamic Models\Linear_interpolation\desc",["description"])
    with pytest.raises(powfacpy.exceptions.PFPathError):
        pfp.set_attr_by_path(r"Stretchwork Model\Stretchwork Data\Grid\Termalamala",["description"])


def test_get_attr(pfp, activate_test_project):
    terminal_1 = pfp.get_obj(r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 1")[0]
    systype = pfp.get_attr(terminal_1,"systype")
    assert systype == 0
    with pytest.raises(powfacpy.exceptions.PFAttributeError):
        systype = pfp.get_attr(terminal_1,"trixi")


def test_create_by_path(pfp, activate_test_project):
    pfp.create_by_path(r"Library\Dynamic Models\dummy.BlkDef")   
    with pytest.raises(powfacpy.exceptions.PFPathError):
        pfp.create_by_path(r"ry\Dynamic Models\dummy.BlkDef")
    with pytest.raises(TypeError):
        pfp.create_by_path(4)


def test_create_in_folder(pfp, activate_test_project):
    pfp.create_in_folder("dummy2.BlkDef", r"Library\Dynamic Models")
    with pytest.raises(TypeError):
        pfp.create_in_folder(2, r"Library\Dynamic Models")


def test_get_by_condition(pfp, activate_test_project):
    folder = r"Network Model\Network Data\test_active_project_interface\Grid"
    all_terminals = pfp.get_obj("*.ElmTerm", parent_folder=folder)
    
    mv_terminals = pfp.get_by_condition(all_terminals, lambda x:getattr(x,"uknom") > 100)
    assert len(mv_terminals) == 2

    with pytest.raises(powfacpy.exceptions.PFAttributeError):
        mv_terminals = pfp.get_by_condition(all_terminals,
            lambda x:getattr(x,"wrong_attr") > 100)


def test_delete_obj(pfp, activate_test_project):
    folder = r"Library\Dynamic Models\TestDelete"
    pfp.create_in_folder("dummy_to_be_deleted_1.BlkDef", folder,)
    pfp.create_in_folder("dummy_to_be_deleted_2.BlkDef", folder,)    
    pfp.delete_obj("dummy_to_be_deleted*", parent_folder=folder)
    objects_in_folder = pfp.get_obj("*", parent_folder=folder,
        error_if_non_existent=False)
    assert len(objects_in_folder) == 0

    pfp.create_in_folder("dummy_to_be_deleted_1.BlkDef", folder,)
    pfp.create_in_folder("dummy_to_be_deleted_2.BlkDef", folder,)    
    pfp.delete_obj("dummy_to_be_deleted_1.BlkDef", parent_folder=folder)
    objects_in_folder = pfp.get_obj("*", parent_folder=folder)
    assert len(objects_in_folder) == 1
    
    pfp.create_in_folder("dummy_to_be_deleted_1.BlkDef", folder,)
    pfp.create_in_folder("dummy_to_be_deleted_2.BlkDef", folder,)
    pfp.delete_obj("dummy_to_be_deleted*",
        parent_folder=r"Library\Dynamic Models", include_subfolders=True)
    objects_in_folder = pfp.get_obj("*", parent_folder=folder,
        error_if_non_existent=False)
    assert len(objects_in_folder) == 0

    pfp.create_in_folder("dummy_to_be_deleted_1.BlkDef",folder,)
    pfp.create_in_folder("dummy_to_be_deleted_2.BlkDef",folder,)
    objects_in_folder = pfp.get_obj("*", parent_folder=folder)
    pfp.delete_obj(objects_in_folder)
    objects_in_folder = pfp.get_obj("*", parent_folder=folder,
        error_if_non_existent=False)
    assert len(objects_in_folder) == 0

    pfp.create_in_folder("dummy_to_be_deleted_1.BlkDef",folder)
    object_in_folder = pfp.get_single_obj("*", parent_folder=folder)
    pfp.delete_obj(object_in_folder)
    objects_in_folder = pfp.get_obj("*", parent_folder=folder,
        error_if_non_existent=False)
    assert len(objects_in_folder) == 0


def test_copy_obj(pfp, activate_test_project):
    folder_copy_from = r"Library\Dynamic Models\TestCopyFrom"
    folder_copy_to = r"Library\Dynamic Models\TestCopyTo"

    pfp.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    copied_objects = pfp.copy_obj("*", folder_copy_to, parent_folder=folder_copy_from)
    assert len(copied_objects) == 2
    # test that the copied objects are returned and not the initial objects to be copied
    obj_to_be_copied = pfp.get_obj("*", parent_folder=folder_copy_from)
    for idx, obj in enumerate(obj_to_be_copied):
        assert copied_objects[idx] != obj
    
    pfp.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    folder_copy_from = pfp.get_obj(r"Library\Dynamic Models\TestCopyFrom")[0]
    folder_copy_to = pfp.get_obj(r"Library\Dynamic Models\TestCopyTo")[0]
    copied_objects = pfp.copy_obj("*", folder_copy_to, parent_folder = folder_copy_from)
    assert len(copied_objects) == 2

    objects_to_copy = pfp.get_obj("*", parent_folder=folder_copy_from)
    copied_objects = pfp.copy_obj(objects_to_copy, folder_copy_to, overwrite=False)
    assert len(copied_objects) == 2
    all_objects_in_folder = pfp.get_obj("*", parent_folder=folder_copy_to)
    assert len(all_objects_in_folder) == 4
    
    pfp.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    objects_to_copy = pfp.get_obj("*", parent_folder=folder_copy_from)[0]
    copied_objects = pfp.copy_obj(objects_to_copy, folder_copy_to, overwrite=False)
    assert len(copied_objects) == 1
    all_objects_in_folder = pfp.get_obj("*", parent_folder=folder_copy_to)
    assert len(all_objects_in_folder) == 1


def test_copy_single_obj(pfp, activate_test_project):
    folder_copy_from = r"Library\Dynamic Models\TestDummyFolder"
    folder_copy_to = r"Library\Dynamic Models\TestCopy"

    pfp.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    copied_object=pfp.copy_single_obj("dummy.*", folder_copy_to,
        parent_folder=folder_copy_from, new_name="new_dummy_name")
    copied_obj_from_folder = pfp.get_single_obj("new_dummy_name",
        parent_folder = folder_copy_to)
    assert copied_object == copied_obj_from_folder

    obj_to_copy = pfp.get_single_obj("dummy2.*", parent_folder=folder_copy_from)
    copied_object=pfp.copy_single_obj(obj_to_copy, folder_copy_to, overwrite=True) 
    copied_obj_from_folder = pfp.get_single_obj("dummy2",
        parent_folder = folder_copy_to)
    assert copied_object == copied_obj_from_folder

    pfp.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    obj_to_copy = pfp.get_single_obj("dummy2.*", parent_folder=folder_copy_from)
    copied_object=pfp.copy_single_obj(obj_to_copy, folder_copy_to, overwrite=False,
        parent_folder=folder_copy_from, new_name="new_dummy_name")  
    copied_obj_from_folder = pfp.get_single_obj("new_dummy_name",
        parent_folder = folder_copy_to)
    assert copied_object == copied_obj_from_folder


def test_handle_single_pf_object_or_path_input(pfp, activate_test_project):
    folder = pfp.get_obj(r"Network Model\Network Data")[0]
    with pytest.raises(TypeError):
        pfp._handle_single_pf_object_or_path_input([folder])
    
    same_folder_returned = pfp._handle_single_pf_object_or_path_input(folder)
    assert same_folder_returned == folder

    same_folder_using_string = pfp._handle_single_pf_object_or_path_input(
        r"Network Model\Network Data")
    assert same_folder_using_string == folder


def test_get_parameter_value_string(pfp, activate_test_project):
    params = {
        "p":r"Network Model\Network Data\test_active_project_interface\Grid\General Load HV\plini",
        "q":r"Network Model\Network Data\test_active_project_interface\Grid\General Load HV\qlini",
        "u":r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 2\uknom"
    }
    pfp.get_parameter_value_string(params, delimiter=" ")      


def test_create_directory(pfp, activate_test_project):
    pfp.create_directory(r"test1\test2",
        parent_folder=r"Study Cases\test_case_studies")

    pfp.create_directory(r"test1\test2\test3\test4",
        parent_folder=r"Study Cases\test_case_studies")
    pfp.delete_obj("test1", parent_folder=r"Study Cases\test_case_studies")

    pfp.create_directory(r"test1\test2")
    pfp.delete_obj("test1")


def test_get_loc_name_with_class(pfp, activate_test_project):
    pf_objects = pfp.get_obj(r'*.ElmTerm', include_subfolders=True)
    pfp.get_loc_name_with_class(pf_objects)
    pfp.get_loc_name_with_class(pf_objects[0])


def test_create_comtrade_obj(pfp, activate_test_project):
    path_of_cfg = os.path.dirname(__file__) + r"\tests_input\test_comtrade.cfg"
    intcomtrade = pfp.create_comtrade_obj(path_of_cfg)
    intcomtrade.Load()
    assert(intcomtrade.FindColumn("AC Voltage Source:m:u:bus1:A") == 1)


def test_replace_outside_or_inside_of_strings_in_a_string(pfp, activate_test_project):
    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1' control 1"
    conditions = powfacpy.PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
	    conditions, {"control 1": "x[1]"})    
    assert(conditions == "lorem ipsum x[1] == 'ABC control 1' 'control 1' x[1]")

    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1'"
    conditions = powfacpy.PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
	    conditions, {"control 1": "x[1]"})    
    assert(conditions == "lorem ipsum x[1] == 'ABC control 1' 'control 1'")

    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1' "
    conditions = powfacpy.PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
	    conditions, {"control 1": "x[1]"})    
    assert(conditions == "lorem ipsum x[1] == 'ABC control 1' 'control 1'")

    conditions = "lorem ipsum control 1 == 'ABC control 1' 'control 1' "
    conditions = powfacpy.PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
	    conditions, {"control 1": "x[1]"}, outside=False)    
    assert(conditions == "lorem ipsum control 1 == 'ABC x[1]' 'x[1]'")


def test_get_path_of_object(pfp, activate_test_project):
    path = "Network Model\\Network Data\\test_active_project_interface\\Grid\\Line 1.2"
    line = pfp.get_unique_obj(path)    
    path_derived = pfp.get_path_of_object(line)
    assert (path==path_derived)


def test_get_upstream_object(pfp, activate_test_project):
    grid = pfp.get_upstream_obj(r"Network Model\Network Data\test_database_interface\Grid\Voltage source ctrl\Frequency",
                      lambda x: x.loc_name == "Grid")
    grid_using_get_unique_obj = pfp.get_unique_obj(r"Network Model\Network Data\test_database_interface\Grid")
    assert(grid == grid_using_get_unique_obj)
    with pytest.raises(Exception):
        pfp.get_upstream_obj(r"Network Model\Network Data\test_database_interface\Grid\Voltage source ctrl\Frequency",
                        lambda x: x.loc_name == "wrong name") 


def test_get_from_study_case(pfp, activate_test_project):
    pfp.activate_study_case(r"Study Cases\test_active_project_interface\multiple_elmres")
    with pytest.warns():
        pfp.get_from_study_case("ElmRes")
    with pytest.raises(Exception):    
        pfp.get_from_study_case("ElmRes", if_not_unique="error")
    

if __name__ == "__main__":
    # pytest.main([r"tests\test_active_project_interface.py"])
    pytest.main(([r"tests"]))
