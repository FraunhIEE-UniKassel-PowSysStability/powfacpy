import sys
from os import getcwd

import pytest

sys.path.insert(0, r".\src")

from powfacpy.applications.dynamic_simulation import DynamicSimulation
from powfacpy.applications.results import Results
from powfacpy.pf_classes.protocols import PFApp
from powfacpy.result_variables import ResVar
from powfacpy.exceptions import PFNoActiveStudyCaseError


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
    pfdi = DynamicSimulation(pfri.act_prj.app)
    elmres_list = []
    terminal_hv_1 = pfri.act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid\Terminal HV 2"
    )
    for case in [study_case_1, study_case_2]:
        case.Activate()
        pfri.act_prj.add_results_variable(terminal_hv_1, "m:u1")
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


def _run_rms_sim_with_relative_rotor_angle(pfri: Results) -> list:
    """Monitor 'c:firel' for all synchronous machines and run the RMS simulation of the active study case. Returns the synchronous machines (ElmSym)."""
    machines = pfri.act_prj.get_calc_relevant_obj("*.ElmSym")
    pfri.act_prj.add_results_variable(machines, ResVar.RMS_Bal.ElmSym.c_firel.value)
    DynamicSimulation(pfri.act_prj.app).initialize_and_run_sim(
        param_initialization={"iopt_sim": "rms"},
        param_simulation={"tstop": 5.0},
    )
    return machines


def test_get_out_of_step_machines(
    activate_39_bus_new_england_test_project, pfri: Results
):
    # Unstable short circuit fault -> at least one machine loses synchronism
    pfri.act_prj.activate_study_case(
        r"Study Cases\2.2 Simulation Fault Bus 16 Unstable"
    )
    _run_rms_sim_with_relative_rotor_angle(pfri)

    out_of_step = pfri.get_out_of_step_machines()
    assert out_of_step
    assert all(machine.GetClassName() == "ElmSym" for machine in out_of_step)

    out_of_step_names = sorted(machine.loc_name for machine in out_of_step)

    # Passing an already exported DataFrame gives the same result
    df = pfri.export_to_pandas()
    assert (
        sorted(
            machine.loc_name
            for machine in pfri.get_out_of_step_machines(df_simulation_results=df)
        )
        == out_of_step_names
    )

    # An explicit machine selection is respected
    assert pfri.get_out_of_step_machines(machines=out_of_step[0]) == [out_of_step[0]]

    # A very large threshold flags nothing
    assert pfri.get_out_of_step_machines(threshold_deg=1e6) == []

    # Stable fault -> no machine out of step
    pfri.act_prj.activate_study_case(
        r"Study Cases\2.1 Simulation Fault Bus 16 Stable"
    )
    _run_rms_sim_with_relative_rotor_angle(pfri)
    assert pfri.get_out_of_step_machines() == []


def test_get_relative_rotor_angles(
    activate_39_bus_new_england_test_project, pfri: Results
):
    machines = pfri.act_prj.activate_study_case(
        r"Study Cases\2.2 Simulation Fault Bus 16 Unstable"
    )
    machines = _run_rms_sim_with_relative_rotor_angle(pfri)

    angles = pfri.get_relative_rotor_angles()
    assert len(angles.columns) == len(machines)
    assert angles.index.name == "time"
    assert all(var == "c:firel" for _, var in angles.columns)

    # Unwrapped: the machine that slips a pole leaves the (-180, 180] range
    assert angles.abs().to_numpy().max() > 180
    out_of_step_names = {
        machine.loc_name for machine in pfri.get_out_of_step_machines()
    }
    unwrapped_over_180 = {
        obj.split("\\")[-1]
        for obj, _ in angles.columns
        if angles[(obj, "c:firel")].abs().max() > 180
    }
    assert unwrapped_over_180 == out_of_step_names

    # Without unwrapping the PowerFactory signal stays wrapped to (-180, 180]
    wrapped = pfri.get_relative_rotor_angles(unwrap=False)
    assert wrapped.abs().to_numpy().max() <= 180 + 1e-6

    # Reading from an already exported DataFrame gives the same result
    df = pfri.export_to_pandas()
    from_df = pfri.get_relative_rotor_angles(df_simulation_results=df)
    assert from_df.shape == angles.shape
    assert from_df.abs().to_numpy().max() == pytest.approx(
        angles.abs().to_numpy().max()
    )


if __name__ == "__main__":
    pytest.main(([r"tests\applications\test_results.py"]))
