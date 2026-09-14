import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.applications.frame_test import BlockDefinitionFrameTest
from powfacpy.applications.modelica import ModelicaModelSpec, ModelicaModelFrameTest
from powfacpy.pf_classes.protocols import PFApp


COMPOSITE_MODEL = r"Network Model\Network Data\Grid\BlockDefinitionTesting"


@pytest.fixture
def load_shedding_spec() -> ModelicaModelSpec:
    return ModelicaModelSpec.from_modelica(
        "pf_models/modelica/LoadSheddingController.mo"
    )


def _nearest(df, t, col):
    return float(df[col].iloc[df.index.get_indexer([t], method="nearest")[0]])


def test_modelica_frame_test_true_ramp_drives_rocof_stage(
    activate_control_block_testing_test_project,
    pf_app: PFApp,
    load_shedding_spec: ModelicaModelSpec,
):
    """A real frequency ramp (only possible with the frame source) trips the RoCoF stage
    with a clean df/dt estimate - the staircase of parameter events cannot do this."""
    test = ModelicaModelFrameTest(pf_app)
    test.act_prj.activate_study_case(r"Study Cases\Study Case")
    test.build(
        load_shedding_spec,
        COMPOSITE_MODEL,
        parameters={"useRocof": True, "kShedMax": 0.9},
        name="lsc_ramp",
    )
    test.set_input_signals(
        {
            "f": {0.0: 50.0, 0.5: 50.0, 3.0: 47.0},  # -1.2 Hz/s
            "pLoad": {0.0: 100.0, 3.0: 100.0},
            "qLoad": {0.0: 20.0, 3.0: 20.0},
        }
    )
    df = test.run(monitor=["rocof", "kShed", "dpext"], tstop=3.0)

    # df/dt estimate settles at the true ramp slope (not a noisy staircase)
    assert df["rocof"].min() == pytest.approx(-1.2, abs=0.02)
    # RoCoF stage (rFrac 0.10) picks up while f is still well above 49 Hz
    assert _nearest(df, 1.1, "kShed") == pytest.approx(0.10, abs=1e-3)
    # then the under-frequency stages add on as the ramp continues
    assert df["kShed"].iloc[-1] > 0.5

    test.device.Delete()


def test_modelica_frame_test_reproduces_event_based_staged_shedding(
    activate_control_block_testing_test_project,
    pf_app: PFApp,
    load_shedding_spec: ModelicaModelSpec,
):
    """Stepping f through the four thresholds in the frame gives the same staircase as
    ModelicaModelTest.set_input_events (tests/applications/test_modelica.py)."""
    test = ModelicaModelFrameTest(pf_app)
    test.act_prj.activate_study_case(r"Study Cases\Study Case")
    test.build(load_shedding_spec, COMPOSITE_MODEL, name="lsc_stages")

    e = 1e-6
    test.set_input_signals(
        {
            "f": {
                0.0: 50.0, 1 - e: 50.0, 1: 49.5, 3 - e: 49.5, 3: 48.9, 5 - e: 48.9,
                5: 48.7, 7 - e: 48.7, 7: 48.5, 9 - e: 48.5, 9: 48.3, 15 - e: 48.3,
                15: 50.0,
            },
            "pLoad": {0.0: 100.0, 20.0: 100.0},
            "qLoad": {0.0: 20.0, 20.0: 20.0},
        }
    )
    df = test.run(["kShed", "dpext"], tstop=20.0)

    assert _nearest(df, 2.0, "kShed") == pytest.approx(0.0)
    assert _nearest(df, 4.5, "kShed") == pytest.approx(0.10, abs=1e-3)
    assert _nearest(df, 6.5, "kShed") == pytest.approx(0.20, abs=1e-3)
    assert _nearest(df, 8.5, "kShed") == pytest.approx(0.35, abs=1e-3)
    assert _nearest(df, 12.0, "kShed") == pytest.approx(0.50, abs=1e-3)
    assert _nearest(df, 19.0, "kShed") == pytest.approx(0.50, abs=1e-3)  # latched
    assert df["dpext"].iloc[-1] == pytest.approx(-100.0, rel=1e-2)

    test.device.Delete()


def test_block_definition_frame_test_pt1_step_response(
    activate_control_block_testing_test_project, pf_app: PFApp
):
    """BlockDefinitionFrameTest drives a plain DSL block definition the same way."""
    test = BlockDefinitionFrameTest(pf_app)
    test.act_prj.activate_study_case(r"Study Cases\Study Case")

    dyn_models = pf_app.GetProjectFolder("blk")
    for old in dyn_models.GetContents("PT1_frame_test.BlkDef"):
        old.Delete()
    pt1 = dyn_models.CreateObject("BlkDef", "PT1_frame_test")
    pt1.SetAttribute("sInput", ["u"])
    pt1.SetAttribute("sOutput", ["y"])
    pt1.SetAttribute("sStates", ["x"])
    pt1.SetAttribute("sParams", ["T"])
    pt1.SetAttribute("sAddEquat", ["inc(x) = u", "x. = (u - x)/T", "y = x"])

    test.build(pt1, COMPOSITE_MODEL, parameters={"T": 0.5}, name="pt1_frame")
    test.set_input_signals({"u": {0.0: 0.0, 1.0 - 1e-6: 0.0, 1.0: 1.0, 5.0: 1.0}})
    df = test.run(["y"], tstop=5.0)

    assert _nearest(df, 1.5, "y") == pytest.approx(0.632, abs=5e-3)  # one time constant
    assert _nearest(df, 5.0, "y") == pytest.approx(1.0, abs=5e-3)

    test.device.Delete()
    pt1.Delete()


if __name__ == "__main__":
    pytest.main([r"tests\applications\test_frame_test.py"])
