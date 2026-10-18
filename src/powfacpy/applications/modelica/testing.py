"""Testing Modelica models: `ModelicaModelTest` (validate a model type) and `ModelicaModelFrameTest` (in a frame), plus event helpers.
"""

from __future__ import annotations

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.applications.frame_test import FrameTest
from powfacpy.pf_classes.protocols import ElmComp, ElmMdl, PFApp, PFGeneral, TypMdl
from powfacpy.applications.modelica.model import ModelicaModel
from powfacpy.applications.modelica.spec import ModelicaModelSpec


class ModelicaModelTest(ApplicationBase):
    """Exercise a Modelica model type on its own with an RMS simulation and return the traces.

    The model instance is created standalone - no composite-model frame, no slots, no signal wiring. Its inputs are given literal start values so they initialise while unconnected, and are then stepped over time with parameter events. This is the fast way to validate controller / relay / signal-processing logic whose inputs are exogenous test signals (a frequency profile, a load step, ...). Closed-loop tests, where the model reacts on the power system, still need a composite model.

    The project must contain a grid (`ElmNet`) and an active study case; a single terminal in the grid is enough for the RMS solver.
    """

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)
        self.model: ElmMdl | None = None
        "The model instance created by `build`."

    def build(
        self,
        spec: ModelicaModelSpec,
        input_start_values: dict[str, float],
        *,
        parameters: dict[str, float | int | bool] | None = None,
        parent: PFGeneral | str | None = None,
        name: str = "modelica_test",
        overwrite: bool = True,
    ) -> ElmMdl:
        """Compile a per-test model type and create a standalone instance of it.

        A standalone `ElmMdl` (no composite model) does not expose its parameters for `SetAttribute`, so per-test parameter values are folded into the spec as **defaults** before compiling. `input_start_values` become the inputs' start values so they initialise while unconnected.

        Args:
            spec: the model description. It is copied, so the caller's spec is untouched.
            input_start_values: `{input_name: value}` - a start value for every input. Inputs left out default to 0.
            parameters: `{parameter_name: value}` - overrides the spec's parameter defaults for this test (e.g. `{"useRocof": True, "kShedMax": 0.9}`).
            parent: where to create the `ElmMdl`; defaults to the first grid in the project.
            name: instance and model-type name.
            overwrite: replace an existing model type / instance of the same name.
        """
        import copy

        spec = copy.deepcopy(spec)
        spec.name = name
        for var in spec.inputs:
            if var.name in input_start_values:
                var.start = _num_str(input_start_values[var.name])
        for var in spec.parameters:
            if parameters and var.name in parameters:
                value = parameters[var.name]
                var.default = (
                    ("true" if value else "false")
                    if isinstance(value, bool)
                    else _num_str(value)
                )

        modelica = ModelicaModel(self.act_prj.__class__.app)
        model_type = modelica.create_model_type(spec, overwrite=overwrite)

        if parent is None:
            grids = self.act_prj.get_obj(
                "*.ElmNet",
                parent_folder=self.act_prj.network_data_folder,
                include_subfolders=True,
                error_if_non_existent=False,
            )
            if not grids:
                raise FileNotFoundError("the project has no grid (ElmNet) to host the test model")
            parent = grids[0]
        else:
            parent = self.act_prj._handle_single_pf_object_or_path_input(parent)

        if overwrite:
            self.act_prj.delete_obj(
                f"{name}.ElmMdl", parent_folder=parent, error_if_non_existent=False
            )
        model_obj: ElmMdl = parent.CreateObject("ElmMdl", name)
        model_obj.SetAttribute("typ_id", model_type)
        self.model = model_obj
        return model_obj

    def set_input_events(self, schedule: dict[str, dict[float, float]]) -> None:
        """Define the time profile of the inputs as step events.

        `schedule` is `{input_name: {time: value, ...}}`. All existing parameter events in the study case are cleared first. A ramp is approximated by many closely spaced steps (helper: `ramp_events`).
        """
        events_folder = self.act_prj.get_events_folder_from_initial_conditions_calc()
        for event in events_folder.GetContents("*.EvtParam"):
            event.Delete()
        for signal, points in schedule.items():
            for time, value in sorted(points.items()):
                event = events_folder.CreateObject("EvtParam", f"{signal}_{time:g}")
                event.SetAttribute("time", float(time))
                event.SetAttribute("p_target", self.model)
                event.SetAttribute("variable", signal)
                event.SetAttribute("value", _num_str(value))

    def run(
        self,
        monitor: list[str],
        tstop: float,
        *,
        initialization_parameters: dict | None = None,
        simulation_parameters: dict | None = None,
    ):
        """Run the RMS simulation and return a `pandas.DataFrame` of the monitored signals.

        Args:
            monitor: signal names to record, with or without the leading `s:` (e.g. `["f", "kShed", "dpext"]`).
            tstop: simulation stop time [s].
            initialization_parameters / simulation_parameters: extra `ComInc` / `ComSim` settings.

        Returns:
            DataFrame indexed by simulation time, one column per monitored signal (bare name).
        """
        from powfacpy.applications.dynamic_simulation import DynamicSimulation
        from powfacpy.applications.results import Results
        from powfacpy.exceptions import PFInterfaceError

        variables = [s if s.startswith(("s:", "c:")) else f"s:{s}" for s in monitor]
        self.act_prj.clear_results_variables()
        self.act_prj.add_results_variable(self.model, variables)

        # The model is tested on its own: any composite model still in the study
        # case (e.g. the shipped BlockDefinitionTesting frame that
        # ModelicaModelFrameTest wires up) would take part in the initialisation
        # and can break it. Park them for the duration of the run and restore
        # their service state afterwards.
        parked = [
            comp
            for comp in self.act_prj.__class__.app.GetCalcRelevantObjects("*.ElmComp")
            if not comp.outserv
        ]
        for comp in parked:
            comp.outserv = 1

        dynamic_simulation = DynamicSimulation(self.act_prj.__class__.app)
        init = {"iopt_sim": "rms", **(initialization_parameters or {})}
        try:
            if dynamic_simulation.initialize_sim(init) != 0:
                raise PFInterfaceError(
                    "the test model did not initialise - check the PowerFactory output window "
                    "(a common cause is a missing start value for an input)"
                )
            dynamic_simulation.run_sim({"tstop": tstop, **(simulation_parameters or {})})

            results = Results(self.act_prj.__class__.app)
            results.pf_objects_in_labels = True
            df = results.export_to_pandas()
        finally:
            for comp in parked:
                comp.outserv = 0
        df.columns = [
            column[1].split(" ", 1)[0].replace("s:", "").replace("c:", "")
            for column in df.columns
        ]
        return df


class ModelicaModelFrameTest(FrameTest):
    """Validate a Modelica model type inside the prebuilt `BlockDefinitionTesting` frame.

    The event-driven `ModelicaModelTest` can only step the inputs; this one feeds them
    from the frame's `lapprox` signal generator, so **true ramps and arbitrary
    piecewise-linear input profiles** work - the way to exercise a `der`-sensitive
    stage such as the RoCoF relay. It needs the shipped `control_block_testing.pfd`
    project (or any project containing an `ElmComp` built on the `BlockDefinitionTesting`
    frame). See `powfacpy.applications.frame_test` for how the wiring works.

    ```python
    test = ModelicaModelFrameTest(app)
    spec = ModelicaModelSpec.from_modelica("LoadSheddingController.mo")
    test.build(
        spec,
        r"Network Model\\Network Data\\Grid\\BlockDefinitionTesting",
        parameters={"useRocof": True},
    )
    test.set_input_signals({
        "f":     {0.0: 50.0, 0.5: 50.0, 3.0: 47.0},   # -1.4 Hz/s ramp
        "pLoad": {0.0: 100.0},
        "qLoad": {0.0: 20.0},
    })
    df = test.run(monitor=["rocof", "kShed", "dpext"], tstop=3.0)
    ```
    """

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)
        self._spec: ModelicaModelSpec | None = None
        self._model_type_folder: PFGeneral | None = None
        self._overwrite: bool = True
        self.model_type: TypMdl | None = None
        "The per-test model type compiled by `build`."

    def build(
        self,
        spec: ModelicaModelSpec,
        composite_model: ElmComp | str,
        *,
        parameters: dict[str, float | int | bool] | None = None,
        model_type_folder: PFGeneral | str | None = None,
        name: str = "modelica_frame_test",
        flatten: bool = True,
        overwrite: bool = True,
    ) -> ElmMdl:
        """Compile a per-test model type from `spec` and place it in the frame's device slot.

        Args:
            spec: the model description. It is copied, so the caller's spec is untouched.
            composite_model: the frame instance (`ElmComp`) - object or path.
            parameters: `{parameter_name: value}` folded into the spec as **defaults**
                before compiling (a model type's parameters are not otherwise settable
                on an instance from a script - same restriction as `ModelicaModelTest`).
            model_type_folder: where to create the `TypMdl`; defaults to the project's
                dynamic-models library folder.
            name: instance and model-type name.
            flatten: apply `spec.flattened()` first (unroll for-loops / arrays).
            overwrite: replace an existing model type / instance of the same name.
        """
        import copy

        spec = copy.deepcopy(spec)
        spec.name = name
        for var in spec.parameters:
            if parameters and var.name in parameters:
                value = parameters[var.name]
                var.default = (
                    ("true" if value else "false")
                    if isinstance(value, bool)
                    else _num_str(value)
                )
        self._spec = spec.flattened() if flatten else spec
        self._overwrite = overwrite
        self._model_type_folder = model_type_folder
        return self._setup_frame(composite_model, name, overwrite)

    def _create_device(self, parent: ElmComp, name: str) -> ElmMdl:
        modelica = ModelicaModel(self.app)
        folder = (
            modelica.get_dynamic_models_folder()
            if self._model_type_folder is None
            else self.act_prj._handle_single_pf_object_or_path_input(
                self._model_type_folder
            )
        )
        self.model_type = modelica.create_model_type(
            self._spec, folder=folder, flatten=False, overwrite=self._overwrite
        )
        device: ElmMdl = parent.CreateObject("ElmMdl", name)
        device.SetAttribute("typ_id", self.model_type)
        return device

    def _device_io_names(self) -> tuple[list[str], list[str]]:
        return (
            [v.name for v in self._spec.inputs],
            [v.name for v in self._spec.outputs],
        )


def _num_str(value) -> str:
    """Render a Python scalar as a Modelica literal (bool -> "1"/"0")."""
    if isinstance(value, bool):
        return "1" if value else "0"
    return repr(value)


def ramp_events(
    start_time: float, start_value: float, rate: float, stop_value: float, step: float = 0.02
) -> dict[float, float]:
    """A `{time: value}` staircase that approximates a linear ramp from `start_value` at `start_value_time` toward `stop_value` at slope `rate` (per second), one step every `step` seconds.

    Use it to feed `ModelicaModelTest.set_input_events` a ramp - e.g. a frequency falling at a defined RoCoF: `ramp_events(1.0, 50.0, -1.5, 49.0)`.
    """
    points: dict[float, float] = {}
    n = max(1, int(abs(stop_value - start_value) / abs(rate * step)))
    for k in range(1, n + 1):
        t = round(start_time + k * step, 6)
        v = start_value + rate * k * step
        points[t] = round(v, 6)
    points[round(start_time + n * step, 6)] = stop_value
    return points
