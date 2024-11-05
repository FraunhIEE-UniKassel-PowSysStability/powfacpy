import sys
from os import remove, getcwd

import pytest

sys.path.insert(0, r".\src")
import powfacpy
from powfacpy.applications.dynamic_simulation import DynamicSimulation
from powfacpy.applications.results import Results
from powfacpy.pf_classes.protocols import PFApp
import importlib

importlib.reload(powfacpy)


@pytest.fixture
def pfsim(pf_app: PFApp) -> DynamicSimulation:
    # Return PFDynSimInterface instance
    return DynamicSimulation(pf_app)


def test_export_to_csv(pfsim: DynamicSimulation, activate_powfacpy_test_project):
    export_dir = getcwd() + r"\tests\tests_output"
    file_name = "test_results"
    study_case = pfsim.act_prj.get_unique_obj(
        r"Study Cases\test_dyn_sim_interface\Study Case"
    )
    study_case.Activate()
    pfsim.act_prj.add_results_variable(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\AC Voltage Source",
        "m:Psum:bus1",
    )
    pfsim.initialize_and_run_sim()

    pfri = Results(pfsim.act_prj.app)
    export_dir = export_dir
    pfri.export_to_csv(export_dir)
    remove(export_dir + "\\results.csv")

    pfri.export_to_csv(dir=export_dir, file_name=file_name)
    remove(export_dir + "\\" + file_name + ".csv")

    results_obj = pfsim.act_prj.get_unique_obj(
        r"Study Cases\test_dyn_sim_interface\Study Case\All calculations"
    )
    pfri.export_to_csv(export_dir, results_obj=results_obj)
    remove(export_dir + "\\results.csv")


def test_set_and_get_dsl_obj_array(
    pfsim: DynamicSimulation, activate_powfacpy_test_project
):
    array = [[2, 0, 2, 0], [1, 2, 3, 4], [5, 6, 7, 8]]
    array_two_column = [[2, 0], [1, 2], [5, 6]]
    dsl_obj = pfsim.act_prj.get_unique_obj(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\Voltage source ctrl\Angle"
    )

    pfsim.set_dsl_obj_array(dsl_obj, array)
    array_returned = powfacpy.PFDynSimInterface.get_dsl_obj_array(dsl_obj)
    assert array_returned == array

    pfsim.set_dsl_obj_array(dsl_obj, array, size_included_in_array=False)
    array_returned = pfsim.get_dsl_obj_array(dsl_obj, size_included_in_array=False)
    assert array_returned == array

    pfsim.set_dsl_obj_array(dsl_obj, array_two_column, array_num=2)
    array_returned = pfsim.get_dsl_obj_array(dsl_obj, array_num=2)
    assert array_returned == array_two_column

    pfsim.set_dsl_obj_array(
        dsl_obj, array_two_column, array_num=2, size_included_in_array=False
    )
    array_returned = pfsim.get_dsl_obj_array(
        dsl_obj, array_num=2, size_included_in_array=False
    )
    assert array_returned == array_two_column


def test_create_event(pfsim: DynamicSimulation, activate_powfacpy_test_project):

    target = pfsim.act_prj.get_unique_obj(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\AC Voltage Source"
    )
    pfsim.create_dyn_sim_event(
        "test.EvtParam",
        {"time": 1, "p_target": target, "variable": "u0", "value": "1.05"},
    )

    target = pfsim.act_prj.get_unique_obj(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\General Load HV"
    )
    pfsim.create_dyn_sim_event(
        "loadevent.EvtLod", {"time": 1, "p_target": target, "dP": 100}
    )


def test_get_parameters_of_dsl_models_in_composite_model(
    pfsim: DynamicSimulation, activate_powfacpy_test_project
):
    pfsim.act_prj.get_unique_obj(
        r"Study Cases\test_dyn_sim_interface\Study Case"
    ).Activate()
    composite_model = pfsim.act_prj.get_unique_obj(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\test_composite_model"
    )

    par_val_dict_1 = pfsim.get_parameters_of_dsl_models_in_composite_model(
        composite_model
    )
    assert not par_val_dict_1["test_no_parameters"]
    assert par_val_dict_1["test_a"]["d"] == 0
    assert not "oarray_x" in par_val_dict_1["test_a"]

    par_val_dict_2 = pfsim.get_parameters_of_dsl_models_in_composite_model(
        composite_model, single_dict_for_all_dsl_models=True
    )
    assert par_val_dict_2["d"] == 0

    # Raise exception if parameter values are not consistent for all DSL models
    # and a single dict is used.
    par_val_dict_1["test_a"]["a"] = 199
    pfsim.set_parameters_of_dsl_models_in_composite_model(
        composite_model, par_val_dict_1
    )
    with pytest.raises(
        powfacpy.exceptions.PFInconsistentParamValueOfDSLModelInCompositeModel
    ):
        pfsim.get_parameters_of_dsl_models_in_composite_model(
            composite_model, single_dict_for_all_dsl_models=True
        )


def test_set_parameters_of_dsl_models_in_composite_model(
    pfsim: DynamicSimulation, activate_powfacpy_test_project
):
    pfsim.act_prj.get_unique_obj(
        r"Study Cases\test_dyn_sim_interface\Study Case"
    ).Activate()
    composite_model = pfsim.act_prj.get_unique_obj(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\test_composite_model"
    )

    par_val_dict = {"test_a": {"a": 50}}
    pfsim.set_parameters_of_dsl_models_in_composite_model(composite_model, par_val_dict)
    par_val_dict = pfsim.get_parameters_of_dsl_models_in_composite_model(
        composite_model
    )
    assert par_val_dict["test_a"]["a"] == 50

    par_val_dict = {"b": 70}
    pfsim.set_parameters_of_dsl_models_in_composite_model(
        composite_model, par_val_dict, single_dict_for_all_dsl_models=True
    )
    par_val_dict = pfsim.get_parameters_of_dsl_models_in_composite_model(
        composite_model
    )
    assert par_val_dict["test_a"]["b"] == 70
    assert par_val_dict["test_b"]["b"] == 70

    # Make sure there is no exception when par_val_dict is empty
    par_val_dict = {}
    pfsim.set_parameters_of_dsl_models_in_composite_model(
        composite_model, par_val_dict, single_dict_for_all_dsl_models=True
    )


def test_get_dsl_model_parameter_names(
    pfsim: DynamicSimulation, activate_powfacpy_test_project
):
    pfsim.act_prj.get_unique_obj(
        r"Study Cases\test_dyn_sim_interface\Study Case"
    ).Activate()
    composite_model = pfsim.act_prj.get_unique_obj(
        r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\test_composite_model_no_blkdef"
    )
    dsl_model = pfsim.act_prj.get_unique_obj("test_a", parent_folder=composite_model)
    with pytest.raises(powfacpy.exceptions.PFObjectAttributeTypeError):
        pfsim.get_dsl_model_parameter_names(dsl_model)


if __name__ == "__main__":
    pytest.main(([r"tests\applications\test_dynamic_simulation.py"]))
