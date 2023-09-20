import pytest
import sys
import os
import json
settings_file = open('.\\settings.json')
settings = json.load(settings_file)
sys.path.append(settings["local path to PowerFactory application"])
import powerfactory
sys.path.insert(0, r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)


@pytest.fixture(scope='session')
def pf_app():
    return powerfactory.GetApplication()

@pytest.fixture
def pfbi(pf_app):
    # Return PFBaseInterface instance
    return powfacpy.PFBaseInterface(pf_app)   

@pytest.fixture
def activate_test_project(pfbi):
    """The project for testing must be located in the current
    user under "powfacpy\\powfacpy_tests". This method will create
    a copy of that project which is then used for the tests. This 
    ensures that the tests are always run with the same initial
    project state.
    """
    user = pfbi.app.GetCurrentUser()
    project_for_testing = pfbi.get_single_obj(r"powfacpy\powfacpy_tests",
        parent_folder = user)
    folder_of_project_for_testing = pfbi.get_single_obj(r"powfacpy",
        parent_folder = user)    
    project_copy = pfbi.copy_single_obj(project_for_testing,
        folder_of_project_for_testing, new_name="powfacpy_tests_copy_where_tests_are_run")    
    project_copy.Activate()    
    
def test_get_single_object(pfbi, activate_test_project):
    terminal_1=pfbi.get_single_obj(r"Network Model\Network Data\test_base_interface\Grid\Terminal HV 1") 
    assert isinstance(terminal_1, powerfactory.DataObject)
    with pytest.raises(TypeError):
       terminals=pfbi.get_single_obj(r"Network Model\Network Data\test_base_interface\Grid\Terminal*")  

def test_get_obj(pfbi, activate_test_project):
    terminal_1 = pfbi.get_obj(r"Network Model\Network Data\test_base_interface\Grid\Terminal HV 1")[0]
    assert isinstance(terminal_1, powerfactory.DataObject)
    with pytest.raises(powfacpy.PFPathError):
        terminal_1 = pfbi.get_obj(r"Stretchwork Model\Stretchwork Data\Grid\Termalamala")[0]
    with pytest.raises(powfacpy.PFPathError):
        terminal_1 = pfbi.get_obj(r"N")[0]    
    with pytest.raises(TypeError):
        terminal_1 = pfbi.get_obj(terminal_1)[0]
    with pytest.raises(TypeError):
        terminal_1 = pfbi.get_obj(terminal_1, include_subfolders=False)[0]

def test_get_obj_with_condition(pfbi, activate_test_project):
    hv_terminals = pfbi.get_obj(r"Network Model\Network Data\test_base_interface\Grid\Terminal*",
        condition=lambda x: getattr(x,"uknom") > 50)
    assert len(hv_terminals) == 2    

def test_get_obj_with_parent_folder_argument(pfbi, activate_test_project):
    parent_folder = pfbi.get_first_level_folder("user")
    terminal_1 = pfbi.get_obj(r"powfacpy\powfacpy_tests\Network Model\Network Data\test_base_interface\Grid\Terminal HV 1",
        parent_folder=parent_folder)[0]
    assert isinstance(terminal_1, powerfactory.DataObject)

    grid = pfbi.get_obj("Grid", parent_folder=r"Network Model\Network Data\test_base_interface")[0]
    assert isinstance(grid, powerfactory.DataObject)

def test_get_obj_including_subfolders(pfbi, activate_test_project):
    terminals = pfbi.get_obj(r"Network Data\test_base_interface\*.ElmTerm", parent_folder="Network Model",
        include_subfolders=True) 
    assert len(terminals) == 3    

def test_path_exists(pfbi, activate_test_project):
    assert pfbi.path_exists(r"Network Model\Network Data\test_base_interface\Grid\Terminal HV 1")

def test_set_attr(pfbi, activate_test_project):
    test_string_1 = "TestString1"
    test_string_2 = "TestString2"
    pfbi.set_attr(r"Library\Dynamic Models\Linear_interpolation",{"sTitle":test_string_1})
    pfbi.set_attr("Linear_interpolation",{"sTitle":test_string_2,
        "desc":["dummy description"]}, parent_folder=r"Library\Dynamic Models")
    stitle = pfbi.get_attr(r"Library\Dynamic Models\Linear_interpolation","sTitle")
    assert stitle == test_string_2

def test_set_attr_of_obj(pfbi, activate_test_project):
    test_string_1 = "TestString1"
    model = pfbi.get_single_obj(r"Library\Dynamic Models\Linear_interpolation")
    powfacpy.set_attr_of_obj(model,{"sTitle":test_string_1})
    stitle = pfbi.get_attr(model,"sTitle")
    assert stitle == test_string_1

def test_set_attr_exceptions(pfbi, activate_test_project):
    with pytest.raises(powfacpy.exceptions.PFAttributeTypeError):
        pfbi.set_attr(r"Library\Dynamic Models\Linear_interpolation",{"sTitle":"dummy",
        "desc":2}) # "desc" should be a list with one string item
    with pytest.raises(powfacpy.exceptions.PFAttributeError):
        pfbi.set_attr(r"Library\Dynamic Models\Linear_interpolation",{"sTie":"dummy",
        "desc":["dummy description"]}) # 'sTie' is not a valid attribute 
    with pytest.raises(powfacpy.exceptions.PFPathError):
        terminal_1 = pfbi.get_obj(r"Network Model\Network Data\test_base_interface\Grid\Termalamala")

def test_set_attr_by_path(pfbi, activate_test_project):
    pfbi.set_attr_by_path(r"Library\Dynamic Models\Linear_interpolation\desc",["description"])
    with pytest.raises(powfacpy.exceptions.PFPathError):
        pfbi.set_attr_by_path(r"Stretchwork Model\Stretchwork Data\Grid\Termalamala",["description"])

def test_get_attr(pfbi, activate_test_project):
    terminal_1 = pfbi.get_obj(r"Network Model\Network Data\test_base_interface\Grid\Terminal HV 1")[0]
    systype = pfbi.get_attr(terminal_1,"systype")
    assert systype == 0
    with pytest.raises(powfacpy.exceptions.PFAttributeError):
        systype = pfbi.get_attr(terminal_1,"trixi")

def test_create_by_path(pfbi, activate_test_project):
    pfbi.create_by_path(r"Library\Dynamic Models\dummy.BlkDef")   
    with pytest.raises(powfacpy.exceptions.PFPathError):
        pfbi.create_by_path(r"ry\Dynamic Models\dummy.BlkDef")
    with pytest.raises(TypeError):
        pfbi.create_by_path(4)

def test_create_in_folder(pfbi, activate_test_project):
    pfbi.create_in_folder(r"Library\Dynamic Models","dummy2.BlkDef")
    with pytest.raises(TypeError):
        pfbi.create_in_folder(r"Library\Dynamic Models",2)

def test_get_by_condition(pfbi, activate_test_project):
    folder = r"Network Model\Network Data\test_base_interface\Grid"
    all_terminals = pfbi.get_obj("*.ElmTerm", parent_folder=folder)
    
    mv_terminals = pfbi.get_by_condition(all_terminals, lambda x:getattr(x,"uknom") > 100)
    assert len(mv_terminals) == 2

    with pytest.raises(powfacpy.exceptions.PFAttributeError):
        mv_terminals = pfbi.get_by_condition(all_terminals,
            lambda x:getattr(x,"wrong_attr") > 100)

def test_delete_obj(pfbi, activate_test_project):
    folder = r"Library\Dynamic Models\TestDelete"
    pfbi.create_in_folder(folder,"dummy_to_be_deleted_1.BlkDef")
    pfbi.create_in_folder(folder,"dummy_to_be_deleted_2.BlkDef")    
    pfbi.delete_obj("dummy_to_be_deleted*", parent_folder=folder)
    objects_in_folder = pfbi.get_obj("*", parent_folder=folder,
        error_if_non_existent=False)
    assert len(objects_in_folder) == 0

    pfbi.create_in_folder(folder,"dummy_to_be_deleted_1.BlkDef")
    pfbi.create_in_folder(folder,"dummy_to_be_deleted_2.BlkDef")    
    pfbi.delete_obj("dummy_to_be_deleted_1.BlkDef", parent_folder=folder)
    objects_in_folder = pfbi.get_obj("*", parent_folder=folder)
    assert len(objects_in_folder) == 1
    
    pfbi.create_in_folder(folder,"dummy_to_be_deleted_1.BlkDef")
    pfbi.create_in_folder(folder,"dummy_to_be_deleted_2.BlkDef")
    pfbi.delete_obj("dummy_to_be_deleted*",
        parent_folder=r"Library\Dynamic Models", include_subfolders=True)
    objects_in_folder = pfbi.get_obj("*", parent_folder=folder,
        error_if_non_existent=False)
    assert len(objects_in_folder) == 0

    pfbi.create_in_folder(folder,"dummy_to_be_deleted_1.BlkDef")
    pfbi.create_in_folder(folder,"dummy_to_be_deleted_2.BlkDef")
    objects_in_folder = pfbi.get_obj("*", parent_folder=folder)
    pfbi.delete_obj(objects_in_folder)
    objects_in_folder = pfbi.get_obj("*", parent_folder=folder,
        error_if_non_existent=False)
    assert len(objects_in_folder) == 0

    pfbi.create_in_folder(folder,"dummy_to_be_deleted_1.BlkDef")
    object_in_folder = pfbi.get_single_obj("*", parent_folder=folder)
    pfbi.delete_obj(object_in_folder)
    objects_in_folder = pfbi.get_obj("*", parent_folder=folder,
        error_if_non_existent=False)
    assert len(objects_in_folder) == 0

def test_copy_obj(pfbi, activate_test_project):
    folder_copy_from = r"Library\Dynamic Models\TestCopyFrom"
    folder_copy_to = r"Library\Dynamic Models\TestCopyTo"

    pfbi.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    copied_objects = pfbi.copy_obj("*", folder_copy_to, parent_folder=folder_copy_from)
    assert len(copied_objects) == 2
    # test that the copied objects are returned and not the initial objects to be copied
    obj_to_be_copied = pfbi.get_obj("*", parent_folder=folder_copy_from)
    for idx, obj in enumerate(obj_to_be_copied):
        assert copied_objects[idx] != obj
    
    pfbi.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    folder_copy_from = pfbi.get_obj(r"Library\Dynamic Models\TestCopyFrom")[0]
    folder_copy_to = pfbi.get_obj(r"Library\Dynamic Models\TestCopyTo")[0]
    copied_objects = pfbi.copy_obj("*", folder_copy_to, parent_folder = folder_copy_from)
    assert len(copied_objects) == 2

    objects_to_copy = pfbi.get_obj("*", parent_folder=folder_copy_from)
    copied_objects = pfbi.copy_obj(objects_to_copy, folder_copy_to, overwrite=False)
    assert len(copied_objects) == 2
    all_objects_in_folder = pfbi.get_obj("*", parent_folder=folder_copy_to)
    assert len(all_objects_in_folder) == 4
    
    pfbi.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    objects_to_copy = pfbi.get_obj("*", parent_folder=folder_copy_from)[0]
    copied_objects = pfbi.copy_obj(objects_to_copy, folder_copy_to, overwrite=False)
    assert len(copied_objects) == 1
    all_objects_in_folder = pfbi.get_obj("*", parent_folder=folder_copy_to)
    assert len(all_objects_in_folder) == 1

def test_copy_single_obj(pfbi, activate_test_project):
    folder_copy_from = r"Library\Dynamic Models\TestDummyFolder"
    folder_copy_to = r"Library\Dynamic Models\TestCopy"

    pfbi.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    copied_object=pfbi.copy_single_obj("dummy.*", folder_copy_to,
        parent_folder=folder_copy_from, new_name="new_dummy_name")
    copied_obj_from_folder = pfbi.get_single_obj("new_dummy_name",
        parent_folder = folder_copy_to)
    assert copied_object == copied_obj_from_folder

    obj_to_copy = pfbi.get_single_obj("dummy2.*", parent_folder=folder_copy_from)
    copied_object=pfbi.copy_single_obj(obj_to_copy, folder_copy_to, overwrite=True) 
    copied_obj_from_folder = pfbi.get_single_obj("dummy2",
        parent_folder = folder_copy_to)
    assert copied_object == copied_obj_from_folder

    pfbi.delete_obj("*", parent_folder=folder_copy_to, error_if_non_existent=False)
    obj_to_copy = pfbi.get_single_obj("dummy2.*", parent_folder=folder_copy_from)
    copied_object=pfbi.copy_single_obj(obj_to_copy, folder_copy_to, overwrite=False,
        parent_folder=folder_copy_from, new_name="new_dummy_name")  
    copied_obj_from_folder = pfbi.get_single_obj("new_dummy_name",
        parent_folder = folder_copy_to)
    assert copied_object == copied_obj_from_folder

def test_handle_single_pf_object_or_path_input(pfbi, activate_test_project):
    folder = pfbi.get_obj(r"Network Model\Network Data")[0]
    with pytest.raises(TypeError):
        pfbi.handle_single_pf_object_or_path_input([folder])
    
    same_folder_returned = pfbi.handle_single_pf_object_or_path_input(folder)
    assert same_folder_returned == folder

    same_folder_using_string = pfbi.handle_single_pf_object_or_path_input(
        r"Network Model\Network Data")
    assert same_folder_using_string == folder

def test_get_parameter_value_string(pfbi, activate_test_project):
    params = {
        "p":r"Network Model\Network Data\test_base_interface\Grid\General Load HV\plini",
        "q":r"Network Model\Network Data\test_base_interface\Grid\General Load HV\qlini",
        "u":r"Network Model\Network Data\test_base_interface\Grid\Terminal HV 2\uknom"
    }
    pfbi.get_parameter_value_string(params, delimiter=" ")      

def test_create_directory(pfbi, activate_test_project):
    pfbi.create_directory(r"test1\test2",
        parent_folder=r"Study Cases\test_case_studies")

    pfbi.create_directory(r"test1\test2\test3\test4",
        parent_folder=r"Study Cases\test_case_studies")
    pfbi.delete_obj("test1", parent_folder=r"Study Cases\test_case_studies")

    pfbi.create_directory(r"test1\test2")
    pfbi.delete_obj("test1")

def test_get_loc_name_with_class(pfbi, activate_test_project):
    pf_objects = pfbi.get_obj(r'*.ElmTerm', include_subfolders=True)
    pfbi.get_loc_name_with_class(pf_objects)
    pfbi.get_loc_name_with_class(pf_objects[0])

def test_create_comtrade_obj(pfbi, activate_test_project):
    path_of_cfg = os.path.dirname(__file__) + r"\tests_input\test_comtrade.cfg"
    intcomtrade = pfbi.create_comtrade_obj(path_of_cfg)
    intcomtrade.Load()
    assert(intcomtrade.FindColumn("AC Voltage Source:m:u:bus1:A") == 1)

def test_replace_outside_or_inside_of_strings_in_a_string(pfbi, activate_test_project):
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

def test_get_path_of_object(pfbi, activate_test_project):
    path = "Network Model\\Network Data\\test_base_interface\\Grid\\Line 1.2"
    line = pfbi.get_unique_obj(path)    
    path_derived = pfbi.get_path_of_object(line)
    print(path_derived)
    assert (path==path_derived)

if __name__ == "__main__":
    pytest.main([r"tests\test_base_interface.py::test_get_path_of_object"])
    # pytest.main(([r"tests"]))
