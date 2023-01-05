import pytest
import sys
sys.path.append(r'C:\Program Files\DIgSILENT\PowerFactory 2022 SP1\Python\3.10')
import powerfactory
sys.path.insert(0,r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)
from os import remove

from test_base_interface import pfbi, pf_app, activate_test_project

@pytest.fixture
def pfsim(pf_app):
    # Return PFDynSimInterface instance
    return powfacpy.PFDynSimInterface(pf_app)   

def test_export_to_csv(pfsim,activate_test_project):
    export_dir = r"D:\User\mfranke\documents\software_projects\powfacpy\tests"
    file_name = "test_results"
    study_case = pfsim.get_single_obj(r"Study Cases\test_dyn_sim_interface\Study Case")
    study_case.Activate()
    pfsim.add_results_variable(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\AC Voltage Source","m:Psum:bus1")    
    pfsim.initialize_and_run_sim()  

    pfsim.export_dir =  export_dir
    pfsim.export_to_csv() 
    remove(export_dir + "\\results.csv")

    pfsim.export_to_csv(dir=export_dir, file_name=file_name)
    remove(export_dir + "\\" + file_name + ".csv")

    results_obj = pfsim.get_single_obj(
        r"Study Cases\test_dyn_sim_interface\Study Case\All calculations")
    pfsim.export_to_csv(results_obj=results_obj) 
    remove(export_dir + "\\results.csv")    

def test_set_and_get_dsl_obj_array(pfsim,activate_test_project):
    array = [[2,0,2,0],[1,2,3,4],[5,6,7,8]]
    array_two_column = [[2,0],[1,2],[5,6]]
    dsl_obj = pfsim.get_single_obj(r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\Voltage source ctrl\Angle")

    powfacpy.PFDynSimInterface.set_dsl_obj_array(dsl_obj,array)
    array_returned = powfacpy.PFDynSimInterface.get_dsl_obj_array(dsl_obj)
    assert(array_returned == array)

    powfacpy.PFDynSimInterface.set_dsl_obj_array(dsl_obj,array,size_included_in_array=False)
    array_returned = powfacpy.PFDynSimInterface.get_dsl_obj_array(dsl_obj,size_included_in_array=False)
    assert(array_returned == array)

    powfacpy.PFDynSimInterface.set_dsl_obj_array(dsl_obj,array_two_column,array_num=2)
    array_returned = powfacpy.PFDynSimInterface.get_dsl_obj_array(dsl_obj,array_num=2)
    assert(array_returned == array_two_column)

    powfacpy.PFDynSimInterface.set_dsl_obj_array(
        dsl_obj,array_two_column,array_num=2,size_included_in_array=False)
    array_returned = powfacpy.PFDynSimInterface.get_dsl_obj_array(
        dsl_obj,array_num=2,size_included_in_array=False)
    assert(array_returned == array_two_column)

def test_create_event(pfsim,activate_test_project):
    
    target = pfsim.get_single_obj(r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\AC Voltage Source")
    pfsim.create_event("test.EvtParam",{"time":1,"p_target":target,"variable":"u0","value":"1.05"})

    target = pfsim.get_single_obj(r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\General Load HV")
    pfsim.create_event("loadevent.EvtLod",{"time":1,"p_target":target,"dP":100})

if __name__ == "__main__":
    pytest.main(([r"tests\test_dyn_sim_interface.py"]))