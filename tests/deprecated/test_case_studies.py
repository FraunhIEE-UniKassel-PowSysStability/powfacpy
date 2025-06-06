import sys

import pytest

sys.path.insert(0, r".\src")
import powfacpy
import importlib

importlib.reload(powfacpy)

from test_active_project_interface import pfp


@pytest.fixture
def pfsc(pf_app):
    return powfacpy.PFStudyCases(pf_app)


def test_create_cases_1(pfsc, activate_powfacpy_test_project):
    pfsc.parameter_values = {
        "p HV load": [1, 2, 1, 2],
        "q HV load": [-1, -1, 1, 1],
    }
    pfsc.parameter_paths = {
        "p HV load": r"Network Model\Network Data\test_case_studies\Grid 1\General Load HV\plini",
        "q HV load": r"Network Model\Network Data\test_case_studies\Grid 1\General Load HV\qlini",
    }
    pfsc.active_grids = r"Network Model\Network Data\test_case_studies\Grid 1"
    pfsc.delimiter = " "
    pfsc.set_parent_folders_for_cases_scenarios_variations(
        r"test_case_studies\autogenerated"
    )
    pfsc.clear_parent_folders()
    pfsc.hierarchy = ["q HV load"]
    pfsc.create_cases()
    pfsc.get_obj(pfsc.hierarchy[0] + "*", parent_folder=pfsc.parent_folder_study_cases)

    # Second time with some attributes changed
    pfsc.clear_parent_folders()
    pfsc.active_grids = r"Network Model\Network Data\test_case_studies\Grid 1"
    pfsc.hierarchy = None
    pfsc.parameter_values = {"p HV load": [1, 2], "q HV load": 1}
    pfsc.create_cases()


def test_create_cases_with_base_study_case(pfsc, activate_powfacpy_test_project):
    pfsc.parameter_values = {
        "p HV load": [1, 2, 1, 2],
        "q HV load": [-1, -1, 1, 1],
    }
    pfsc.base_study_case = r"Study Cases\test_case_studies\base_study_case"
    pfsc.add_scenario_to_each_case = False
    pfsc.set_parent_folders_for_cases_scenarios_variations(
        r"test_case_studies\autogenerated"
    )
    pfsc.delete_obj(
        "*", parent_folder=pfsc.parent_folder_study_cases, error_if_non_existent=False
    )
    pfsc.delete_obj(
        "*", parent_folder=pfsc.parent_folder_scenarios, error_if_non_existent=False
    )
    pfsc.delete_obj(
        "*", parent_folder=pfsc.parent_folder_variations, error_if_non_existent=False
    )
    pfsc.create_cases()


def test_create_cases_regression(pfsc, activate_powfacpy_test_project):
    pfsc.parameter_values = {
        "p HV load": [
            1,
            2,
            1,
            2,
            1,
            2,
            1,
            2,
        ],
        "q HV load": [
            -1,
            -1,
            1,
            1,
            -1,
            -1,
            1,
            1,
        ],
        "control": [
            "A",
            "A",
            "A",
            "A",
            "B",
            "B",
            "B",
            "B",
        ],
    }
    pfsc.parameter_paths = {
        "p HV load": r"Network Model\Network Data\test_case_studies\Grid 2\General Load HV\plini",
        "q HV load": r"Network Model\Network Data\test_case_studies\Grid 2\General Load HV\qlini",
    }
    pfsc.active_grids = [
        [
            r"Network Model\Network Data\test_case_studies\Grid 1",
            r"Network Model\Network Data\test_case_studies\Grid 2",
        ],
        [r"Network Model\Network Data\test_case_studies\Grid 1"],
        r"Network Model\Network Data\test_case_studies\Grid 1",
        [
            r"Network Model\Network Data\test_case_studies\Grid 1",
            r"Network Model\Network Data\test_case_studies\Grid 2",
        ],
        r"Network Model\Network Data\test_case_studies\Grid 2",
        r"Network Model\Network Data\test_case_studies\Grid 2",
        r"Network Model\Network Data\test_case_studies\Grid 2",
        r"Network Model\Network Data\test_case_studies\Grid 2",
    ]

    pfsc.delimiter = " "
    pfsc.set_parent_folders_for_cases_scenarios_variations(
        r"test_case_studies\autogenerated"
    )
    pfsc.delete_obj(
        "*", parent_folder=pfsc.parent_folder_study_cases, error_if_non_existent=False
    )
    pfsc.delete_obj(
        "*", parent_folder=pfsc.parent_folder_scenarios, error_if_non_existent=False
    )
    pfsc.delete_obj(
        "*", parent_folder=pfsc.parent_folder_variations, error_if_non_existent=False
    )
    pfsc.hierarchy = ["control", "q HV load"]
    pfsc.add_variation_to_each_case = True
    pfsc.create_cases()

    for case_num, study_case_obj in enumerate(pfsc.study_cases):
        study_case_obj.Activate()
        # Set controller parameter
        dsl_controller_obj = r"Network Model\Network Data\test_case_studies\Grid 2\WECC WT Control System Type 4A\REEC_A Electrical Control Model"
        if pfsc.get_value_of_parameter_for_case("control", case_num) == "A":
            pfsc.set_attr(dsl_controller_obj, {"PfFlag": 0})
            pfsc.set_attr(dsl_controller_obj, {"VFlag": 1})
        elif pfsc.get_value_of_parameter_for_case("control", case_num) == "B":
            pfsc.set_attr(dsl_controller_obj, {"PfFlag": 1})
            pfsc.set_attr(dsl_controller_obj, {"VFlag": 0})

    for case_num, study_case_obj in enumerate(pfsc.study_cases):
        dsl_controller_obj = r"Network Model\Network Data\test_case_studies\Grid 2\WECC WT Control System Type 4A\REEC_A Electrical Control Model"
        if pfsc.get_value_of_parameter_for_case("p HV load", case_num) == 1:
            case_label = pfsc.get_case_params_value_string(
                case_num,
                omitted_parameters="p HV load",
                delimiter=" | ",
                equals_sign="=",
            )


def test_case_studies_permutation(pfsc, activate_powfacpy_test_project):
    pfsc.set_parent_folders_for_cases_scenarios_variations(
        r"test_case_studies\autogenerated"
    )
    pfsc.clear_parent_folders()

    pfsc.parameter_values = {
        "p HV load": [1, 2],
        "q HV load": [
            -1,
            1,
        ],
        "control": [
            "A",
            "B",
        ],
    }
    pfsc.parameter_paths = {
        "p HV load": r"Network Model\Network Data\test_case_studies\Grid 2\General Load HV\plini",
        "q HV load": r"Network Model\Network Data\test_case_studies\Grid 2\General Load HV\qlini",
    }
    pfsc.hierarchy = [
        "q HV load",
        "control",
    ]
    pfsc.active_grids = r"Network Model\Network Data\test_case_studies\Grid 2"
    pfsc.apply_permutation()
    pfsc.create_cases()


def test_case_studies_permutation_with_omitted_combinations(
    pfsc, activate_powfacpy_test_project
):
    pfsc.set_parent_folders_for_cases_scenarios_variations(
        r"test_case_studies\autogenerated"
    )
    pfsc.clear_parent_folders()

    pfsc.parameter_values = {
        "p HV load": [1, 2, 3],
        "q HV load": [-1, 1, 0],
        "control 1": ["A", "B", "C"],
        "control 2": ["R", "S", "T"],
    }
    pfsc.parameter_paths = {
        "p HV load": r"Network Model\Network Data\test_case_studies\Grid 2\General Load HV\plini",
        "q HV load": r"Network Model\Network Data\test_case_studies\Grid 2\General Load HV\qlini",
    }
    pfsc.hierarchy = [
        "p HV load",
        "control 1",
    ]
    pfsc.active_grids = r"Network Model\Network Data\test_case_studies\Grid 2"
    omitted_combinations = [
        {"p HV load": [2], "control 1": "all", "control 2": "all"},
        {"q HV load": [1, 0], "control 2": ["R", "T"]},
    ]
    pfsc.apply_permutation(omitted_combinations=omitted_combinations)
    # Assert that the omitted combinations are not included
    for case_num, _ in enumerate(pfsc.parameter_values["p HV load"]):
        assert not (
            (pfsc.parameter_values["p HV load"][case_num] == 2)
            and (pfsc.parameter_values["control 1"][case_num] is not None)
            and (pfsc.parameter_values["control 2"][case_num] is not None)
        )
        assert not (
            (pfsc.parameter_values["q HV load"][case_num] == 0)
            and (pfsc.parameter_values["control 2"][case_num] == "T")
        )
        assert not (
            (pfsc.parameter_values["q HV load"][case_num] == 1)
            and (pfsc.parameter_values["control 2"][case_num] == "R")
        )
    pfsc.create_cases()


def test_get_study_cases(pfsc, activate_powfacpy_test_project):
    # Create cases
    pfsc.parameter_values = {
        "p HV load": [1, 2, 3],
        "q HV load": [-1, 1],
        "control 1": ["A", "B"],
        "control 2": ["R", "S"],
    }
    pfsc.set_parent_folders_for_cases_scenarios_variations(
        r"test_case_studies\autogenerated"
    )
    pfsc.hierarchy = [
        "p HV load",
        "control 1",
    ]
    pfsc.apply_permutation()
    pfsc.clear_parent_folders()
    pfsc.create_cases()
    # Actual tests
    conditions = {"p HV load": lambda x: x > 2, "control 2": lambda x: x == "S"}
    cases = pfsc.get_study_cases(conditions)
    for case in cases:
        assert pfsc.get_value_of_parameter_for_case("p HV load", case) > 2
        assert pfsc.get_value_of_parameter_for_case("control 2", case) == "S"


def test_get_study_cases_from_string(pfsc, activate_powfacpy_test_project):
    # Create cases
    pfsc.parameter_values = {
        "p HV load": [1, 2, 3],
        "q HV load": [-1, 1],
        "control 1": ["A", "B"],
        "control 2": ["R", "S"],
    }
    pfsc.set_parent_folders_for_cases_scenarios_variations(
        r"test_case_studies\autogenerated"
    )
    pfsc.hierarchy = [
        "p HV load",
        "control 1",
    ]
    pfsc.apply_permutation()
    pfsc.clear_parent_folders()
    pfsc.create_cases()
    # Actual tests
    conditions = " p HV load >= 2 and (control 1 == 'A' and control 2 != 'S'  ) "
    _, case_numbers = pfsc.get_study_cases_from_string(
        conditions, return_case_numbers=True
    )
    for case_num in case_numbers:
        assert pfsc.get_value_of_parameter_for_case("p HV load", case_num) >= 2
        assert pfsc.get_value_of_parameter_for_case("control 1", case_num) == "A"
        assert pfsc.get_value_of_parameter_for_case("control 2", case_num) != "S"

    conditions = "q HV load == 1"
    _, case_numbers = pfsc.get_study_cases_from_string(
        conditions, return_case_numbers=True
    )
    for case_num in case_numbers:
        assert pfsc.get_value_of_parameter_for_case("q HV load", case_num) == 1
        assert not (pfsc.get_value_of_parameter_for_case("q HV load", case_num) == -1)


def test_export_results_of_study_cases_to_csv(pfsc, activate_powfacpy_test_project):
    # Create cases
    pfsc.parameter_values = {
        "p HV load": [1, 2, 3],
        "q HV load": [-1, 1],
    }
    pfsc.parameter_paths = {
        "p HV load": r"Network Model\Network Data\test_case_studies\Grid 2\General Load HV\plini",
        "q HV load": r"Network Model\Network Data\test_case_studies\Grid 2\General Load HV\qlini",
    }
    pfsc.set_parent_folders_for_cases_scenarios_variations(
        r"test_case_studies\autogenerated"
    )
    pfsc.hierarchy = ["p HV load"]
    pfsc.apply_permutation()
    pfsc.clear_parent_folders()
    pfsc.base_study_case = r"Study Cases\test_case_studies\base_study_case"
    pfsc.create_cases()
    pfds = powfacpy.PFDynSimInterface(pfsc.app)
    cases, case_numbers = pfsc.get_study_cases_from_string(
        "p HV load >= 1 and q HV load > 0", return_case_numbers=True
    )
    # Run RMS simulations
    for case in cases:
        case.Activate()
        pfds.initialize_and_run_sim()
    # Export to csv
    export_dir = r"tests\tests_output\Case_studies"
    csv_files_full_paths = pfsc.export_results_of_study_cases_to_csv(
        study_cases=cases, case_numbers=case_numbers, export_dir=export_dir
    )
    assert len(csv_files_full_paths) == 3


def test_handle_study_case_objects_case_numbers_input(
    pfsc, activate_powfacpy_test_project
):
    # Create cases
    pfsc.parameter_values = {
        "p HV load": [1, 2, 3],
        "q HV load": [-1, 1],
    }
    pfsc.set_parent_folders_for_cases_scenarios_variations(
        r"test_case_studies\autogenerated"
    )
    pfsc.hierarchy = ["p HV load"]
    pfsc.apply_permutation()
    pfsc.clear_parent_folders()
    pfsc.base_study_case = r"Study Cases\test_case_studies\base_study_case"
    pfsc.create_cases()
    # Actual tests
    # Make sure the various possible input argument variations give
    # the same results.
    study_cases = pfsc.study_cases
    study_cases1, case_numbers1 = pfsc._handle_study_case_objects_case_numbers_input(
        study_cases=pfsc.study_cases
    )
    assert study_cases == study_cases1
    study_cases2, case_numbers2 = pfsc._handle_study_case_objects_case_numbers_input(
        case_numbers=case_numbers1
    )
    assert case_numbers1 == case_numbers2
    study_cases3, case_numbers3 = pfsc._handle_study_case_objects_case_numbers_input()
    assert study_cases == study_cases3
    assert case_numbers2 == list(case_numbers3)


if __name__ == "__main__":
    pytest.main(([r"tests\deprecated\test_case_studies.py"]))
