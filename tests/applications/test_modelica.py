import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.applications.modelica import (
    ModelicaModel,
    ModelicaModelSpec,
    ModelicaModelTest,
    ModelicaVariable,
    ramp_events,
)
from powfacpy.pf_classes.protocols import PFApp
from powfacpy.exceptions import PFModelicaCompilationError


PI_CONTROLLER_MO = '''model PI_controller "time-continuous PI controller"
  parameter Real Kp = 3.0 "proportional gain";
  parameter Real Ki(unit="1/s") = 2.5 "integral gain";
  input Real reference "reference signal";
  input Real measurement "measured signal";
  output Real control "control command";
protected
  Real x(start=0) "integrator state";
  Real error "control error";
initial equation
  x = 0;
equation
  error = reference - measurement;
  der(x) = error;
  control = Kp*error + Ki*x;
end PI_controller;
'''


# --------------------------------------------------------------------------- #
# pure python - no PowerFactory
# --------------------------------------------------------------------------- #


def test_from_modelica_parses_declarations_and_sections():
    spec = ModelicaModelSpec.from_modelica(PI_CONTROLLER_MO)
    assert spec.name == "PI_controller"
    assert spec.method == "hybrid"
    assert [p.name for p in spec.parameters] == ["Kp", "Ki"]
    assert spec.parameters[1].unit == "1/s"
    assert spec.parameters[0].default == "3.0"
    assert [i.name for i in spec.inputs] == ["reference", "measurement"]
    assert [o.name for o in spec.outputs] == ["control"]
    assert [s.name for s in spec.states] == ["x"]  # der(x) -> state
    assert [v.name for v in spec.internals] == ["error"]  # no der() -> internal
    assert spec.init_equations == ["x = 0;"]
    assert spec.equations[1] == "der(x) = error;"


def test_to_modelica_roundtrips():
    spec = ModelicaModelSpec.from_modelica(PI_CONTROLLER_MO)
    reparsed = ModelicaModelSpec.from_modelica(spec.to_modelica())
    assert [p.name for p in reparsed.parameters] == [p.name for p in spec.parameters]
    assert [i.name for i in reparsed.inputs] == [i.name for i in spec.inputs]
    assert [s.name for s in reparsed.states] == [s.name for s in spec.states]
    assert reparsed.equations == spec.equations


def test_flattened_unrolls_loops_and_arrays():
    spec = ModelicaModelSpec(
        name="staged",
        parameters=[
            ModelicaVariable("n", base_type="Integer", default="3"),
            ModelicaVariable("level", size="n", default="{1.0, 2.0, 3.0}"),
        ],
        inputs=[ModelicaVariable("u")],
        outputs=[ModelicaVariable("y")],
        internals=[ModelicaVariable("hit", base_type="Boolean", size="n")],
        equations=[
            "for i in 1:n loop",
            "hit[i] = u > level[i];",
            "end for;",
            "y = sum(hit);",
        ],
    )
    flat = spec.flattened()
    assert [p.name for p in flat.parameters] == ["n", "level_1", "level_2", "level_3"]
    assert flat.parameters[1].default == "1.0"
    assert [v.name for v in flat.internals] == ["hit_1", "hit_2", "hit_3"]
    assert "hit_2 = u > level_2;" in flat.equations
    assert "y = (hit_1 + hit_2 + hit_3);" in flat.equations
    assert not any("for " in e for e in flat.equations)


def test_flattened_load_shedding_controller():
    spec = ModelicaModelSpec.from_modelica("pf_models/modelica/LoadSheddingController.mo")
    flat = spec.flattened()
    assert not any(e.strip().startswith("for ") for e in flat.equations)
    assert not any("[" in v.name for v in flat.all_variables)
    assert "fArm_4 = enable and (f < fLevel_4);" in flat.equations
    assert any(e.startswith("kTarget = min(") and "fCon_1 + fCon_2" in e for e in flat.equations)


# --------------------------------------------------------------------------- #
# live PowerFactory
# --------------------------------------------------------------------------- #


@pytest.fixture
def pfmdl(pf_app: PFApp):
    return ModelicaModel(pf_app)


@pytest.fixture
def scratch_folder(pfmdl: ModelicaModel):
    dyn_models = pfmdl.get_dynamic_models_folder()
    folder = pfmdl.act_prj.create_in_folder(
        "test_modelica_scratch.IntFolder", dyn_models, overwrite=True
    )
    yield folder
    folder.Delete()


def test_get_dynamic_models_folder(activate_powfacpy_test_project, pfmdl: ModelicaModel):
    folder = pfmdl.get_dynamic_models_folder()
    assert folder.GetAttribute("iopt_typ") == "blk"
    assert folder == pfmdl.app.GetProjectFolder("blk")


def test_create_and_compile_model_type(
    activate_powfacpy_test_project, pfmdl: ModelicaModel, scratch_folder
):
    spec = ModelicaModelSpec.from_modelica(PI_CONTROLLER_MO)
    typ = pfmdl.create_model_type(spec, folder=scratch_folder, compile=True)

    assert typ.GetClassName() == "TypMdl"
    assert typ.GetAttribute("modMethod") == 0  # hybrid
    assert typ.GetAttribute("inputName") == ["reference", "measurement"]
    assert typ.GetAttribute("inputVariability")[0] == 1  # continuous
    assert typ.GetAttribute("paramName") == ["Kp", "Ki"]
    assert typ.GetAttribute("paramDefault") == ["3.0", "2.5"]
    assert typ.GetAttribute("equation")[1] == "der(x) = error;"
    assert typ.GetAttribute("modelType") == 1  # compiled
    assert typ.GetAttribute("cfilePath").endswith(".pfmu")

    # round trip via read_model_type
    read = pfmdl.read_model_type(typ)
    assert [p.name for p in read.parameters] == ["Kp", "Ki"]
    assert [i.name for i in read.inputs] == ["reference", "measurement"]
    assert read.states and read.states[0].name == "x"


def test_compile_load_shedding_controller(
    activate_powfacpy_test_project, pfmdl: ModelicaModel, scratch_folder
):
    spec = ModelicaModelSpec.from_modelica("pf_models/modelica/LoadSheddingController.mo")
    typ = pfmdl.create_model_type(spec, folder=scratch_folder, compile=True)
    assert typ.GetAttribute("modelType") == 1  # compiled
    assert typ.GetAttribute("cfilePath").endswith(".pfmu")
    # for-loops were unrolled to the 4 default under-frequency stages
    assert "fLevel_4" in typ.GetAttribute("paramName")


def test_create_model_type_compilation_error(
    activate_powfacpy_test_project, pfmdl: ModelicaModel, scratch_folder
):
    spec = ModelicaModelSpec(
        name="broken",
        inputs=[ModelicaVariable("u")],
        outputs=[ModelicaVariable("y")],
        equations=["y = u + nonexistent_symbol;"],
    )
    with pytest.raises(PFModelicaCompilationError):
        pfmdl.create_model_type(spec, folder=scratch_folder, compile=True)


def test_create_model_instance(
    activate_powfacpy_test_project, pfmdl: ModelicaModel, scratch_folder
):
    spec = ModelicaModelSpec.from_modelica(PI_CONTROLLER_MO)
    typ = pfmdl.create_model_type(spec, folder=scratch_folder, compile=True)
    grid = pfmdl.act_prj.get_unique_obj(
        r"Network Model\Network Data\test_active_project_interface\Grid"
    )
    model = pfmdl.create_model(typ, parent_folder=grid, name="PI_instance")
    assert model.GetClassName() == "ElmMdl"
    assert model.GetAttribute("typ_id") == typ
    model.Delete()


# --------------------------------------------------------------------------- #
# ModelicaModelTest - isolated RMS validation
# --------------------------------------------------------------------------- #


def test_ramp_events():
    pts = ramp_events(1.0, 50.0, -2.0, 49.0, step=0.05)
    assert pts[1.05] == pytest.approx(49.9)
    assert min(pts.values()) == 49.0  # ends exactly at stop_value
    assert all(1.0 < t <= 1.5 + 1e-9 for t in pts)


def test_modelica_model_test_load_shedding(
    activate_39_bus_new_england_test_project, pf_app: PFApp
):
    test = ModelicaModelTest(pf_app)
    test.act_prj.activate_study_case(
        r"Study Cases\2.1 Simulation Fault Bus 16 Stable"
    )
    spec = ModelicaModelSpec.from_modelica("pf_models/modelica/LoadSheddingController.mo")

    # staged under-frequency + latching: f steps through the 4 thresholds, then recovers
    test.build(spec, {"f": 50.0, "pLoad": 100.0, "qLoad": 20.0}, name="lsc_validation")
    test.set_input_events(
        {"f": {1: 49.5, 3: 48.9, 5: 48.7, 7: 48.5, 9: 48.3, 15: 50.0}}
    )
    df = test.run(["f", "kShed", "dpext"], tstop=20.0)

    def kshed_at(t):
        return float(df["kShed"].iloc[df.index.get_indexer([t], method="nearest")[0]])

    assert kshed_at(2.0) == pytest.approx(0.0)      # f=49.5, above stage 1
    assert kshed_at(4.5) == pytest.approx(0.10, abs=1e-3)   # stage 1
    assert kshed_at(6.5) == pytest.approx(0.20, abs=1e-3)   # stages 1-2
    assert kshed_at(8.5) == pytest.approx(0.35, abs=1e-3)   # stages 1-3
    assert kshed_at(12.0) == pytest.approx(0.50, abs=1e-3)  # all four
    assert kshed_at(19.0) == pytest.approx(0.50, abs=1e-3)  # latched after f recovers
    assert df["dpext"].iloc[-1] == pytest.approx(-0.5 / 0.5 * 100.0, rel=1e-2)

    test.model.Delete()
    test.act_prj.delete_obj(
        "lsc_validation.TypMdl",
        parent_folder=pf_app.GetProjectFolder("blk"),
        error_if_non_existent=False,
    )


if __name__ == "__main__":
    pytest.main([r"tests\applications\test_modelica.py"])
