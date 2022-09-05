import pytest
import sys

sys.path.insert(0,r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)

from test_base_interface import pfbi, pf_app, activate_test_project

@pytest.fixture
def pfsc(pf_app):
    return powfacpy.PFStudyCases(pf_app)

def test_create_cases_1(pfsc,activate_test_project):   
    pfsc.parameter_values = {
        "p HV load":[1, 2, 1, 2],
        "q HV load":[-1, -1, 1, 1],
    }
    pfsc.parameter_paths = {
        "p HV load":r"Network Model\Network Data\test_case_studies\Grid 1\General Load HV\plini",
        "q HV load":r"Network Model\Network Data\test_case_studies\Grid 1\General Load HV\qlini",
    }
    pfsc.active_grids = [
        r"Network Model\Network Data\test_case_studies\Grid 1",
        r"Network Model\Network Data\test_case_studies\Grid 1",
        r"Network Model\Network Data\test_case_studies\Grid 1",
        r"Network Model\Network Data\test_case_studies\Grid 1"
    ]
    pfsc.active_grids = r"Network Model\Network Data\test_case_studies\Grid 1"
    pfsc.delimiter = " "
    pfsc.parent_folder_study_cases = r"Study Cases\test_case_studies"
    pfsc.parent_folder_scenarios = r"Network Model\Operation Scenarios\test_case_studies"
    pfsc.parent_folder_variations = r"Network Model\Variations\test_case_studies"

    pfsc.delete_obj("*",
        parent_folder = pfsc.parent_folder_study_cases,error_if_non_existent=False)
    pfsc.delete_obj("*",parent_folder =pfsc.parent_folder_scenarios,
        error_if_non_existent=False)
    pfsc.delete_obj("*",parent_folder =pfsc.parent_folder_variations,
        error_if_non_existent=False)
    pfsc.hierarchy = ["q HV load"]
    pfsc.create_cases()
    pfsc.get_obj(pfsc.parent_folder_study_cases + "\\" + pfsc.hierarchy[0] + "*")

    # Second time with some attributes changed
    pfsc.delete_obj("*",
        parent_folder = pfsc.parent_folder_study_cases,error_if_non_existent=False)
    pfsc.delete_obj("*",parent_folder =pfsc.parent_folder_scenarios,
        error_if_non_existent=False)
    pfsc.delete_obj("*",parent_folder =pfsc.parent_folder_variations,
        error_if_non_existent=False)
    pfsc.active_grids = r"Network Model\Network Data\test_case_studies\Grid 1"
    pfsc.hierarchy = None
    pfsc.parameter_values = {
        "p HV load":[1, 2],
        "q HV load":1
    }
    pfsc.create_cases()

def test_create_cases_regression(pfsc,activate_test_project): 
    pfsc.parameter_values = {
        "p HV load":[1, 2, 1, 2, 1, 2, 1, 2,],
        "q HV load":[-1, -1, 1, 1,-1, -1, 1, 1,],
        "control": ["A","A","A","A","B","B","B","B",]
    }
    pfsc.parameter_paths = {
        "p HV load":r"Network Model\Network Data\test_case_studies\Grid 2\General Load HV\plini",
        "q HV load":r"Network Model\Network Data\test_case_studies\Grid 2\General Load HV\qlini",
    }
    pfsc.active_grids = [
        [r"Network Model\Network Data\test_case_studies\Grid 1",
        r"Network Model\Network Data\test_case_studies\Grid 2"],
        [r"Network Model\Network Data\test_case_studies\Grid 1"],
        r"Network Model\Network Data\test_case_studies\Grid 1",
        [r"Network Model\Network Data\test_case_studies\Grid 1",
        r"Network Model\Network Data\test_case_studies\Grid 2"],
        r"Network Model\Network Data\test_case_studies\Grid 2",
        r"Network Model\Network Data\test_case_studies\Grid 2",
        r"Network Model\Network Data\test_case_studies\Grid 2",
        r"Network Model\Network Data\test_case_studies\Grid 2",
    ]

    pfsc.delimiter = " "
    pfsc.parent_folder_study_cases = r"Study Cases\test_case_studies"
    pfsc.parent_folder_scenarios = r"Network Model\Operation Scenarios\test_case_studies"
    pfsc.parent_folder_variations = r"Network Model\Variations\test_case_studies"
    pfsc.delete_obj("*",
        parent_folder = pfsc.parent_folder_study_cases,error_if_non_existent=False)
    pfsc.delete_obj("*",parent_folder =pfsc.parent_folder_scenarios,
        error_if_non_existent=False)
    pfsc.delete_obj("*",parent_folder =pfsc.parent_folder_variations,
        error_if_non_existent=False)
    pfsc.hierarchy = ["control","q HV load"]
    pfsc.add_variation_to_each_case = True
    pfsc.create_cases()

    for case_num,study_case_obj in enumerate(pfsc.study_cases):
        study_case_obj.Activate()
        # Set controller parameter
        dsl_controller_obj = r"Network Model\Network Data\test_case_studies\Grid 2\WECC WT Control System Type 4A\REEC_A Electrical Control Model"
        if pfsc.get_value_of_parameter_for_case("control",case_num) == "A":
            pfsc.set_attr(dsl_controller_obj,{"PfFlag":0}) 
            pfsc.set_attr(dsl_controller_obj,{"VFlag":1}) 
        elif pfsc.get_value_of_parameter_for_case("control",case_num) == "B":
            pfsc.set_attr(dsl_controller_obj,{"PfFlag":1}) 
            pfsc.set_attr(dsl_controller_obj,{"VFlag":0}) 

    for case_num,study_case_obj in enumerate(pfsc.study_cases):   
        dsl_controller_obj = r"Network Model\Network Data\test_case_studies\Grid 2\WECC WT Control System Type 4A\REEC_A Electrical Control Model"
        if pfsc.get_value_of_parameter_for_case("p HV load",case_num) == 1:
            case_label = pfsc.get_case_params_value_string(case_num,
                omitted_parameters="p HV load",
                delimiter=" | ",
                equals_symbol="=") 

if __name__ == "__main__":
    pytest.main(([r"tests\test_case_studies.py"]))