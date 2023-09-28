import pytest
import sys
sys.path.append(r'C:\Program Files\DIgSILENT\PowerFactory 2022 SP1\Python\3.10')
import powerfactory
sys.path.insert(0, r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)
from os import remove, getcwd

from test_base_interface import pfbi, pf_app, activate_test_project

@pytest.fixture
def pfsim(pf_app):
    # Return PFDynSimInterface instance
    return powfacpy.PFDynSimInterface(pf_app)   

def test_export_to_csv(pfsim, activate_test_project):
    export_dir = getcwd()
    file_name = "test_results"
    study_case = pfsim.get_single_obj(r"Study Cases\test_dyn_sim_interface\Study Case")
    study_case.Activate()
    pfsim.add_results_variable(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\AC Voltage Source","m:Psum:bus1")    
    pfsim.initialize_and_run_sim()  

    pfsim.export_dir = export_dir
    pfsim.export_to_csv() 
    remove(export_dir + "\\results.csv")

    pfsim.export_to_csv(dir=export_dir, file_name=file_name)
    remove(export_dir + "\\" + file_name + ".csv")

    results_obj = pfsim.get_single_obj(
        r"Study Cases\test_dyn_sim_interface\Study Case\All calculations")
    pfsim.export_to_csv(results_obj=results_obj) 
    remove(export_dir + "\\results.csv")    

def test_set_and_get_dsl_obj_array(pfsim, activate_test_project):
    array = [[2,0,2,0],[1,2,3,4],[5,6,7,8]]
    array_two_column = [[2,0],[1,2],[5,6]]
    dsl_obj = pfsim.get_single_obj(r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\Voltage source ctrl\Angle")

    powfacpy.PFDynSimInterface.set_dsl_obj_array(dsl_obj, array)
    array_returned = powfacpy.PFDynSimInterface.get_dsl_obj_array(dsl_obj)
    assert(array_returned == array)

    powfacpy.PFDynSimInterface.set_dsl_obj_array(dsl_obj, array, size_included_in_array=False)
    array_returned = powfacpy.PFDynSimInterface.get_dsl_obj_array(dsl_obj, size_included_in_array=False)
    assert(array_returned == array)

    powfacpy.PFDynSimInterface.set_dsl_obj_array(dsl_obj, array_two_column, array_num=2)
    array_returned = powfacpy.PFDynSimInterface.get_dsl_obj_array(dsl_obj, array_num=2)
    assert(array_returned == array_two_column)

    powfacpy.PFDynSimInterface.set_dsl_obj_array(
        dsl_obj, array_two_column, array_num=2, size_included_in_array=False)
    array_returned = powfacpy.PFDynSimInterface.get_dsl_obj_array(
        dsl_obj, array_num=2, size_included_in_array=False)
    assert(array_returned == array_two_column)

def test_create_event(pfsim, activate_test_project):
    
    target = pfsim.get_single_obj(r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\AC Voltage Source")
    pfsim.create_event("test.EvtParam",{"time":1,"p_target":target,"variable":"u0","value":"1.05"})

    target = pfsim.get_single_obj(r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\General Load HV")
    pfsim.create_event("loadevent.EvtLod",{"time":1,"p_target":target,"dP":100})
    
def test_get_parameters_of_dsl_models_in_composite_model(pfsim, activate_test_project):
    pfsim.get_single_obj(r"Study Cases\test_dyn_sim_interface\Study Case").Activate()
    composite_model = pfsim.get_unique_obj(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\test_composite_model")
    
    par_val_dict = pfsim.get_parameters_of_dsl_models_in_composite_model(
        composite_model)
    assert not par_val_dict["test_no_parameters"]
    assert par_val_dict["test_a"]["d"] == 0
    assert not "oarray_x" in par_val_dict["test_a"]
    
    par_val_dict = pfsim.get_parameters_of_dsl_models_in_composite_model(
        composite_model,
        single_dict_for_all_dsl_models=True)
    assert par_val_dict["d"] == 0
    
def test_set_parameters_of_dsl_models_in_composite_model(pfsim, activate_test_project):
    pfsim.get_single_obj(r"Study Cases\test_dyn_sim_interface\Study Case").Activate()
    composite_model = pfsim.get_unique_obj(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\test_composite_model")
    
    par_val_dict = {"test_a": {"a": 50}}
    pfsim.set_parameters_of_dsl_models_in_composite_model(
    composite_model,
    par_val_dict)
    par_val_dict = pfsim.get_parameters_of_dsl_models_in_composite_model(
        composite_model)
    assert par_val_dict["test_a"]["a"] == 50
    
    par_val_dict = {"b": 70}
    pfsim.set_parameters_of_dsl_models_in_composite_model(
        composite_model,
        par_val_dict,
        single_dict_for_all_dsl_models=True)
    par_val_dict = pfsim.get_parameters_of_dsl_models_in_composite_model(
        composite_model)
    assert par_val_dict["test_a"]["b"] == 70
    assert par_val_dict["test_b"]["b"] == 70
    
    # Make sure there is no exception when par_val_dict is empty
    par_val_dict = {}
    pfsim.set_parameters_of_dsl_models_in_composite_model(
        composite_model,
        par_val_dict,
        single_dict_for_all_dsl_models=True)
    
def test_get_dsl_model_parameter_names(pfsim, activate_test_project):    
    pfsim.get_unique_obj(r"Study Cases\test_dyn_sim_interface\Study Case").Activate()
    composite_model = pfsim.get_unique_obj(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\test_composite_model_no_blkdef")
    dsl_model = pfsim.get_unique_obj("test_a", parent_folder=composite_model)
    with pytest.raises(powfacpy.PFObjectAttributeTypeError):
        pfsim.get_dsl_model_parameter_names(dsl_model)
    
if __name__ == "__main__":
    pytest.main(([r"tests\test_dyn_sim_interface.py"]))