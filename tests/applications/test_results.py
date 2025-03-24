import sys
from os import getcwd

import pytest

sys.path.insert(0, r".\src")
import powfacpy
from powfacpy.applications.dynamic_simulation import DynamicSimulation
from powfacpy.applications.results import Results
from powfacpy.pf_classes.protocols import PFApp
from powfacpy.exceptions import PFNoActiveStudyCaseError
import importlib

importlib.reload(powfacpy)


@pytest.fixture
def pfri(pf_app: PFApp):
    # Return PFResultsInterface instance and show app
    pfri = Results(pf_app)
    return pfri


def test_export_to_csv(activate_powfacpy_test_project, pfri: Results):
    study_case_1 = pfri.act_prj.get_unique_obj(
        r"Study Cases\test_results_interface\Export Simulation 1.IntCase"
    )
    study_case_2 = pfri.act_prj.get_unique_obj(
        r"Study Cases\test_results_interface\Export Simulation 2.IntCase"
    )
    pfdi = powfacpy.PFDynSimInterface(pfri.act_prj.app)
    elmres_list = []
    terminal_hv_1 = pfri.act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 2"
    )
    for case in [study_case_1, study_case_2]:
        case.Activate()
        pfdi.add_results_variable(terminal_hv_1, "m:u1")
        pfdi.initialize_and_run_sim()
        elmres_list.append(pfri.act_prj.get_from_study_case("ElmRes"))
    study_case_1.Activate()
    dir = getcwd() + "\\tests\\tests_output"
    pfri.export_to_csv(dir=dir, file_name="test_1")
    pfri.export_to_csv(dir=dir, file_name="test_2", results_obj=elmres_list[0])
    # lists and different elmres
    pfri.export_to_csv(
        dir=dir,
        file_name="test_3",
        list_of_results_objs=elmres_list,
        elements=[terminal_hv_1, terminal_hv_1],
        variables=["m:u1", "m:u1"],
    )
    # lists and same elmres
    pfri.export_to_csv(
        dir=dir,
        file_name="test_4",
        list_of_results_objs=[elmres_list[0], elmres_list[0]],
        elements=[terminal_hv_1, terminal_hv_1],
        variables=["m:u1", "m:u1"],
    )
    # don't format csv, use comres parameter argument
    pfri.export_to_csv(
        dir=dir,
        file_name="test_5",
        comres_parameters={"iopt_rscl": 1, "scl_start": 0.5},
        format_csv_file=False,
    )

    with pytest.raises(PFNoActiveStudyCaseError):
        study_case = pfri.act_prj.app.GetActiveStudyCase()
        study_case.Deactivate()
        pfri.export_to_csv(dir=dir, file_name="test_6")

    with pytest.raises(ValueError):
        # specified results_obj in combination with list_of_results_objs
        study_case.Activate()
        pfri.export_to_csv(
            dir=dir,
            file_name="test_exception",
            results_obj=elmres_list[0],
            list_of_results_objs=elmres_list,
            elements=[terminal_hv_1, terminal_hv_1],
            variables=["m:u1", "m:u1"],
        )

    with pytest.raises(ValueError):
        # variables specified without elements
        pfri.export_to_csv(
            dir=dir,
            file_name="test_exception",
            list_of_results_objs=elmres_list,
            # elements=[terminal_hv_1, terminal_hv_1],
            variables=["m:u1", "m:u1"],
        )


def test_export_to_pandas(activate_powfacpy_test_project, pfri: Results):
    pfri.act_prj.get_unique_obj(
        r"Study Cases\test_results_interface\Study Case"
    ).Activate()
    network_element = pfri.act_prj.get_obj(
        r"Network Model\Network Data\test_results_interface\Grid\General Load HV.ElmLod",
        include_subfolders=True,
    )[0]
    variables = ["m:i1:bus1", "m:u1:bus1"]
    elmres = pfri.act_prj.add_results_variable(network_element, variables)
    pfdi = DynamicSimulation(pfri.act_prj.app)
    pfdi.initialize_sim(param={"p_resvar": elmres})
    pfdi.run_sim()
    nr_of_columns = len(variables)
    df = pfri.export_to_pandas(
        list_of_results_objs=[
            elmres,
        ]
        * len(variables),
        elements=[
            network_element,
        ]
        * len(variables),
        variables=variables,
    )
    assert len(df.columns) == nr_of_columns

    df = pfri.export_to_pandas()


def test_get_result_variable_description(activate_powfacpy_test_project, pfri: Results):
    assert (
        pfri.get_result_variable_description("ElmArea", "c_cosgen", "RMS_Bal")
        == "Generators, Power Factor"
    )


if __name__ == "__main__":
    pytest.main(([r"tests\applications\test_results.py"]))
