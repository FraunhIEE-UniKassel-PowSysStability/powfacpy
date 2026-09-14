"""Isolated dynamic-model testing inside a prebuilt composite frame.

`powfacpy.applications.modelica.ModelicaModelTest` validates a Modelica model type on
its own by stepping its inputs with parameter events (`EvtParam`). That is fast and
needs no frame, but a parameter event is a step change only - a `der`-sensitive stage
(a RoCoF relay, a washout filter, ...) never sees a real ramp, only a staircase whose
slope is zero between steps and infinite at each step.

`FrameTest` drives the model inside the shipped `BlockDefinitionTesting` composite
frame instead. The model under test sits in the `BlockDefinitionTested` slot; its
inputs come from the `Input` slot - a DSL macro that emits `lapprox(time(), array_k)`,
one linearly interpolated lookup table per input signal - so ramps and arbitrary
piecewise-linear profiles work. The `Sink` slot terminates the outputs.

The frame's two routed signal lines cannot be created from a script (PowerFactory has
no API for it), so the frame is shipped as `pf_models/control_block_testing.pfd`. Only
the slot signal strings are rewritten per model: every device signal is aggregated
onto the single existing connector node with `;` separators - see PowerFactory
UserManual ch. 30, "a node can aggregate two or more variables by separating these
variables with a semicolon".

`FrameTest` is model-kind agnostic. `powfacpy.applications.modelica.ModelicaModelFrameTest`
puts a compiled Modelica `TypMdl` in the device slot; `BlockDefinitionFrameTest`
(below) puts an `ElmDsl` referencing a `BlkDef`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.applications.dynamic_simulation import DynamicSimulation
from powfacpy.applications.results import Results
from powfacpy.exceptions import PFInterfaceError
from powfacpy.pf_classes.protocols import BlkSlot, ElmComp, ElmDsl, ElmMdl, PFApp, PFGeneral


class FrameTest(ApplicationBase, ABC):
    """Base class: run one dynamic model in isolation inside the `BlockDefinitionTesting` frame.

    Subclasses implement `_create_device` (create the `ElmMdl` / `ElmDsl` for the
    `BlockDefinitionTested` slot) and `_device_io_names` (its input / output signal
    names, in declaration order). Everything else - wiring the slots, feeding the
    input signals, running the RMS simulation - is shared.
    """

    #: slot names expected in the shipped frame
    INPUT_SLOT = "Input"
    DEVICE_SLOT = "BlockDefinitionTested"
    SINK_SLOT = "Sink"

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)
        self.composite_model: ElmComp | None = None
        "The frame instance (`ElmComp`) the test runs in, set by `build`."
        self.device: ElmMdl | ElmDsl | None = None
        "The model under test, created by `build` and placed in the device slot."
        self._input_names: list[str] = []
        self._output_names: list[str] = []
        self._slots: dict[str, BlkSlot] = {}
        self._input_dsl: ElmDsl | None = None
        self._sink_dsl: ElmDsl | None = None

    # ------------------------------------------------------------------ #
    # subclass hooks
    # ------------------------------------------------------------------ #
    @abstractmethod
    def _create_device(self, parent: ElmComp, name: str) -> ElmMdl | ElmDsl:
        """Create the model-under-test object inside `parent` and return it (with its `typ_id` set)."""

    @abstractmethod
    def _device_io_names(self) -> tuple[list[str], list[str]]:
        """Return `(input_signal_names, output_signal_names)` of the device, in declaration order."""

    def _sink_equations(self, n_outputs: int) -> list[str]:
        """Additional equations of the sink block definition.

        The default is an empty list: a pure signal sink that only terminates the
        device outputs. `BlockDefinitionFrameTest` overrides this because a DSL block
        under test may need its outputs back-initialised (`inc(y) = 0`).
        """
        return []

    # ------------------------------------------------------------------ #
    # shared build steps
    # ------------------------------------------------------------------ #
    def _setup_frame(
        self, composite_model: ElmComp | str, name: str, overwrite: bool
    ) -> ElmMdl | ElmDsl:
        self.composite_model = self.act_prj._handle_single_pf_object_or_path_input(
            composite_model
        )
        # the frame drives the test - make sure it is in service even if an
        # earlier teardown parked it
        self.composite_model.outserv = 0
        slots = list(self.composite_model.pblk)
        elms = list(self.composite_model.pelm)
        self._slots = {s.loc_name: s for s in slots}
        for required in (self.INPUT_SLOT, self.DEVICE_SLOT, self.SINK_SLOT):
            if required not in self._slots:
                raise PFInterfaceError(
                    f"'{self.act_prj.get_path_of_object(self.composite_model)}' is not a "
                    f"BlockDefinitionTesting frame - it has no '{required}' slot "
                    f"(slots: {sorted(self._slots)})"
                )
        slot_to_elm = {s.loc_name: e for s, e in zip(slots, elms)}
        self._input_dsl = slot_to_elm[self.INPUT_SLOT]
        self._sink_dsl = slot_to_elm[self.SINK_SLOT]
        if self._input_dsl is None or self._sink_dsl is None:
            raise PFInterfaceError(
                "the frame's 'Input' and 'Sink' slots must be populated with their "
                "DSL models (they are part of the shipped frame)"
            )

        if overwrite:
            # drop any device left in the frame by an earlier test - an orphaned
            # ElmMdl / ElmDsl inside the ElmComp is still initialised by PowerFactory
            # even when no slot references it.
            keep = {self._input_dsl, self._sink_dsl}
            for old in (
                list(self.composite_model.GetContents("*.ElmMdl"))
                + list(self.composite_model.GetContents("*.ElmDsl"))
            ):
                if old not in keep:
                    old.Delete()

        self.device = self._create_device(self.composite_model, name)
        self._input_names, self._output_names = self._device_io_names()
        self._check_capacity()
        self._wire()
        return self.device

    def _input_signal_capacity(self) -> int:
        """How many input signals the `Input` DSL macro can provide (its `y0..yN`)."""
        outputs = self._input_dsl.typ_id.GetAttribute("sOutput")
        if not outputs:
            return 0
        return len(outputs[0].replace(";", ",").split(","))

    def _check_capacity(self) -> None:
        capacity = self._input_signal_capacity()
        if len(self._input_names) > capacity:
            names = ", ".join(self._input_names)
            raise PFInterfaceError(
                f"the device under test has {len(self._input_names)} inputs ({names}) "
                f"but the frame's signal generator only provides {capacity}. Extend the "
                f"'Linear_interpolation' block definition or test fewer inputs."
            )

    def _wire(self) -> None:
        """Assign the device to the device slot and aggregate all signals onto the frame's connectors."""
        pelm = []
        for slot in self.composite_model.pblk:
            if slot.loc_name == self.DEVICE_SLOT:
                pelm.append(self.device)
            elif slot.loc_name == self.INPUT_SLOT:
                pelm.append(self._input_dsl)
            elif slot.loc_name == self.SINK_SLOT:
                pelm.append(self._sink_dsl)
            else:
                pelm.append(None)
        self.composite_model.SetAttribute("pelm", pelm)

        n_in = len(self._input_names)
        n_out = len(self._output_names)
        # one aggregated node per connector (';' groups signals onto a single node)
        self._slots[self.INPUT_SLOT].SetAttribute(
            "sOutput", [";".join(f"y{i}" for i in range(n_in))]
        )
        self._slots[self.DEVICE_SLOT].SetAttribute("sInput", [";".join(self._input_names)])
        self._slots[self.DEVICE_SLOT].SetAttribute("sOutput", [";".join(self._output_names)])
        self._slots[self.SINK_SLOT].SetAttribute(
            "sInput", [";".join(f"y{i}" for i in range(n_out))]
        )
        sink_def = self._sink_dsl.typ_id
        sink_def.SetAttribute("sInput", [",".join(f"y{i}" for i in range(n_out))])
        sink_def.SetAttribute("sAddEquat", self._sink_equations(n_out))

    # ------------------------------------------------------------------ #
    # input signals
    # ------------------------------------------------------------------ #
    def set_input_signals(
        self, signals: dict[str, "pd.Series | dict[float, float]"]
    ) -> None:
        """Define the time profile of every device input as a piecewise-linear lookup table.

        `signals` maps each input name to either a `pandas.Series` indexed by time [s]
        or a `{time: value}` dict. PowerFactory linearly interpolates between the
        breakpoints (`lapprox`), so a two-point series is an exact ramp and a
        near-vertical pair (`{1.0 - 1e-6: a, 1.0: b}`) is a step. Every input of the
        device must be given.
        """
        missing = [n for n in self._input_names if n not in signals]
        if missing:
            raise ValueError(
                f"no signal given for input(s) {missing} - every device input needs a "
                f"profile (use a constant two-point series for the ones held fixed)"
            )
        series_by_name = {
            name: (
                value
                if isinstance(value, pd.Series)
                else pd.Series(dict(sorted(value.items())))
            )
            for name, value in signals.items()
            if name in self._input_names
        }
        self._ensure_input_matrix_rows(
            max(len(s) for s in series_by_name.values())
        )
        for i, name in enumerate(self._input_names):
            DynamicSimulation.set_dsl_obj_array_from_pandas_series(
                self._input_dsl, series_by_name[name], array_num=i + 1
            )

    def _ensure_input_matrix_rows(self, n_rows: int) -> None:
        """Grow the `Input` DSL lookup-table matrix so it has at least `n_rows` data rows."""
        header = list(self._input_dsl.GetAttribute("matrix:0"))
        current = int(max(header)) if header else 0
        if n_rows <= current:
            return
        last_row = list(self._input_dsl.GetAttribute(f"matrix:{current}"))
        for row in range(current + 1, n_rows + 1):
            self._input_dsl.SetAttribute(f"matrix:{row}", last_row)

    # ------------------------------------------------------------------ #
    # run
    # ------------------------------------------------------------------ #
    def run(
        self,
        monitor: list[str],
        tstop: float,
        *,
        initialization_parameters: dict | None = None,
        simulation_parameters: dict | None = None,
    ) -> pd.DataFrame:
        """Run the RMS simulation and return a `pandas.DataFrame` of the monitored signals.

        Args:
            monitor: signal names to record on the device, with or without the leading
                `s:` / `c:` (e.g. `["dpext", "kShed", "rocof"]`).
            tstop: simulation stop time [s].
            initialization_parameters / simulation_parameters: extra `ComInc` / `ComSim` settings.

        Returns:
            DataFrame indexed by simulation time, one column per monitored signal (bare name).
        """
        if self.device is None:
            raise PFInterfaceError("call build() before run()")
        variables = [s if s.startswith(("s:", "c:")) else f"s:{s}" for s in monitor]
        self.act_prj.clear_results_variables()
        self.act_prj.add_results_variable(self.device, variables)

        dynamic_simulation = DynamicSimulation(self.app)
        init = {"iopt_sim": "rms", **(initialization_parameters or {})}
        if dynamic_simulation.initialize_sim(init) != 0:
            raise PFInterfaceError(
                "the frame test did not initialise - check the PowerFactory output "
                "window (common causes: an output the sink also initialises, or an "
                "input signal value the model rejects at t=0)"
            )
        dynamic_simulation.run_sim({"tstop": tstop, **(simulation_parameters or {})})

        results = Results(self.app)
        results.pf_objects_in_labels = True
        df = results.export_to_pandas()
        df.columns = [
            column[1].split(" ", 1)[0].replace("s:", "").replace("c:", "")
            for column in df.columns
        ]
        return df


class BlockDefinitionFrameTest(FrameTest):
    """Run a DSL block definition (`BlkDef`) in isolation inside the `BlockDefinitionTesting` frame.

    This is the powfacpy-native, single-model counterpart of the many-models,
    random-input `BlockDefTesting` sweep in `powfacpypro`. Use it to feed a controller
    / relay / signal-processing `BlkDef` a designed input profile and check the response.
    """

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)
        self._block_definition = None

    def build(
        self,
        block_definition: PFGeneral | str,
        composite_model: ElmComp | str,
        *,
        parameters: dict[str, float] | None = None,
        name: str = "blkdef_frame_test",
        overwrite: bool = True,
    ) -> ElmDsl:
        """Place `block_definition` in the frame's device slot and wire it up.

        Args:
            block_definition: the `BlkDef` to test (object or path).
            composite_model: the frame instance (`ElmComp`) - object or path.
            parameters: `{parameter_name: value}` set on the created `ElmDsl`.
            name: name of the created `ElmDsl`.
            overwrite: replace an existing device of the same name in the frame.
        """
        self._block_definition = self.act_prj._handle_single_pf_object_or_path_input(
            block_definition
        )
        self._parameters = parameters or {}
        return self._setup_frame(composite_model, name, overwrite)

    def _create_device(self, parent: ElmComp, name: str) -> ElmDsl:
        dsl: ElmDsl = parent.CreateObject("ElmDsl", name)
        dsl.SetAttribute("typ_id", self._block_definition)
        for param_name, value in self._parameters.items():
            dsl.SetAttribute(param_name, value)
        return dsl

    def _device_io_names(self) -> tuple[list[str], list[str]]:
        from powfacpy.pf_classes.blk.definition import BlockDefinition

        blkdef = BlockDefinition(self._block_definition)
        inputs = (
            blkdef.input_signals
            + blkdef.upper_limitation_signals
            + blkdef.lower_limitation_signals
        )
        return inputs, blkdef.output_signals

    def _sink_equations(self, n_outputs: int) -> list[str]:
        return [f"inc(y{i})=0" for i in range(n_outputs)]
