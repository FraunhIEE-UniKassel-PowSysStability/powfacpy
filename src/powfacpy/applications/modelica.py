"""Import a Modelica model into PowerFactory: build and compile a model type ('TypMdl') from a `.mo` file (or from Python), without the GUI.

**Experimental / best effort.** PowerFactory has no `.mo` file import - not in the GUI, not in the scripting API - and a `TypMdl` only supports a *subset* of Modelica 3.5. This module bridges that gap for the kinds of model it can handle (controllers, relays, signal processing - e.g. the load-shedding controller in `pf_models/modelica/`); it is not a general Modelica compiler. Constructs outside the subset (see the rules below), or that the best-effort `.mo` parser / array-and-for-loop flattener do not understand, must be simplified in the source or assembled as a `ModelicaModelSpec` by hand. For full standard Modelica, compile the `.mo` to an FMU with OpenModelica or Dymola and load that into a `TypMdl` (tick "Compiled model") instead.

A `TypMdl` is a *decomposed* model: separate tabular declarations for inputs / outputs / parameters / states / internal variables, plus text fields for the initial and dynamic equations (Hybrid method) or algorithm sections (Clocked method). This module writes all of that from a single description.

Typical workflow - `.mo` file -> compiled `TypMdl` -> model instance:

    from powfacpy.applications.modelica import ModelicaModel, ModelicaModelSpec

    spec = ModelicaModelSpec.from_modelica("LoadSheddingController.mo")  # parse the file
    pfmdl = ModelicaModel(app)
    model_type = pfmdl.create_model_type(spec)        # create + compile the TypMdl
    model = pfmdl.create_model(model_type, name="Load 23 shedding")  # ElmMdl instance

The `ElmMdl` instance still has to be placed in a composite model (`ElmComp` with a frame) to take part in a simulation - that remains a GUI step. To validate the model type on its own first, use `ModelicaModelTest` (inputs stepped by time events) or `ModelicaModelFrameTest` (true ramp inputs via the shipped test frame).

Building a model from Python instead of a file: construct a `ModelicaModelSpec` directly (see its docstring), or parse a file and edit the result. `spec.to_modelica()` emits a standalone standard-Modelica `.mo` string (for OpenModelica / Dymola / documentation). `spec.flattened()` unrolls `for` loops, expands array variables to scalars and expands `sum(array)`, because PowerFactory's support for arrays and `for` loops inside the equation fields is limited. The pure-Python part (`ModelicaVariable`, `ModelicaModelSpec` and the module helpers) has no PowerFactory dependency; only `ModelicaModel` and the `*Test` classes talk to PowerFactory.

PowerFactory Modelica subset - things a Hybrid model must obey (verified against PF 2025 SP5):
  - a state's start value must be a literal constant, not a parameter reference; initialise states in the initial-equation section instead;
  - every equation must have exactly `x` or `der(x)` on the left-hand side, so write `der(x) = (u - x) / T`, not `T * der(x) = u - x`;
  - `der()` may only be applied to a declared state variable, never to an output - make it a `protected` state and monitor it as `s:<name>`;
  - every state must be assigned exactly once in the initial-equation section.
`reinit()`, `when`, `pre()`, `if`/`for` (once unrolled), `min`/`max` and latching booleans (a `Boolean` written only inside a `when`) do work.

Empirical PowerFactory facts this module relies on:
  - a `TypMdl` can only be created in the project's dynamic-models library folder (`app.GetProjectFolder("blk")`) or a subfolder of it; `CreateObject("TypMdl", ...)` returns `None` anywhere else. That folder's display name varies by project / language ('Dynamic Models', 'User Defined Models', ...).
  - `TypMdl.modMethod` defaults to 1 (Clocked); this module sets 0 (Hybrid) unless the spec says `method="clocked"`.
  - string declaration columns accept a whole-list write; the numeric-enum columns (base type, variability) must be written element by element (`SetAttribute("inputType:0", 0)`) - whole-list writes are silently ignored.
  - scalar parameter values on a fresh `ElmMdl` are not settable from a script until PowerFactory has populated the instance's parameter list (open the model dialog once); `create_model` warns for any it could not set. The `*Test` classes fold test parameters into the spec as defaults before compiling to work around this.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from pathlib import Path
from warnings import warn

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.applications.frame_test import FrameTest
from powfacpy.pf_classes.protocols import ElmComp, ElmMdl, IntFolder, PFApp, PFGeneral, TypMdl
from powfacpy.exceptions import PFModelicaCompilationError

# --------------------------------------------------------------------------- #
# enums (PowerFactory stores base type / variability as numeric codes)
# --------------------------------------------------------------------------- #

BASE_TYPES = ("Real", "Integer", "Boolean")
VARIABILITIES = ("inherited", "continuous", "discrete")

_BASE_TYPE_CODE = {name: i for i, name in enumerate(BASE_TYPES)}
_VARIABILITY_CODE = {name: i for i, name in enumerate(VARIABILITIES)}
_BASE_TYPE_NAME = {i: name for name, i in _BASE_TYPE_CODE.items()}
_VARIABILITY_NAME = {i: name for name, i in _VARIABILITY_CODE.items()}

# TypMdl.modMethod
_METHOD_CODE = {"hybrid": 0, "clocked": 1}
_METHOD_NAME = {0: "hybrid", 1: "clocked"}


# --------------------------------------------------------------------------- #
# spec
# --------------------------------------------------------------------------- #


@dataclass
class ModelicaVariable:
    """One declared variable of a Modelica model.

    `base_type` is Real | Integer | Boolean. `variability` (inputs/outputs only) is continuous | discrete | inherited. `size` is "" for a scalar or e.g. "n" / "[n]" / "3" for a vector (n may be an Integer parameter name). `default` is used for parameters, `start` for inputs/outputs/states/internals.
    """

    name: str
    base_type: str = "Real"
    variability: str = "continuous"
    size: str = ""
    unit: str = ""
    description: str = ""
    start: str = ""
    default: str = ""
    minimum: str = ""
    maximum: str = ""

    @property
    def is_array(self) -> bool:
        return bool(self.size.strip().strip("[]").strip())

    def array_length(self, int_params: dict[str, int]) -> int:
        token = self.size.strip().strip("[]").strip()
        if not token:
            return 1
        if token.isdigit():
            return int(token)
        if token in int_params:
            return int_params[token]
        raise ValueError(
            f"cannot resolve array size {self.size!r} of {self.name!r} - "
            f"give an integer or an Integer parameter with a default value"
        )


@dataclass
class ModelicaModelSpec:
    """A backend-agnostic description of a Modelica model.

    Maps 1:1 onto the fields of a PowerFactory `TypMdl`: `inputs` / `outputs` / `parameters` / `states` / `internals` are the declaration tables, and for the Hybrid method (`method="hybrid"`, the default) `init_equations` / `equations` are the initial- and dynamic-equation sections, while for the Clocked method (`method="clocked"`) they are the initial- and dynamic-algorithm (statement) sections. Each entry of `init_equations` / `equations` is one line of source.

    Three ways to obtain one: `ModelicaModelSpec.from_modelica(path_or_text)` (best-effort parse of a single-model `.mo` file); construct it directly in Python (see the tutorial - the way to go for anything the parser cannot handle); or `ModelicaModel(app).read_model_type(typ)` (reconstruct it from an existing `TypMdl`).

    `to_modelica()` renders it back to a standalone `.mo` string; `flattened()` returns an equivalent spec with arrays and `for` loops expanded (needed before creating a `TypMdl`, done automatically by `create_model_type`).
    """

    name: str
    method: str = "hybrid"
    inputs: list[ModelicaVariable] = field(default_factory=list)
    outputs: list[ModelicaVariable] = field(default_factory=list)
    parameters: list[ModelicaVariable] = field(default_factory=list)
    states: list[ModelicaVariable] = field(default_factory=list)
    internals: list[ModelicaVariable] = field(default_factory=list)
    init_equations: list[str] = field(default_factory=list)
    equations: list[str] = field(default_factory=list)
    description: str = ""
    author: str = ""

    # ---- introspection ------------------------------------------------- #
    @property
    def all_variables(self) -> list[ModelicaVariable]:
        return [
            *self.inputs,
            *self.outputs,
            *self.parameters,
            *self.states,
            *self.internals,
        ]

    def integer_parameter_values(self) -> dict[str, int]:
        """{name: int(default)} for every Integer parameter that has an integer default - used to resolve array sizes and `for` ranges."""
        out: dict[str, int] = {}
        for p in self.parameters:
            if p.base_type == "Integer" and p.default.strip().lstrip("-").isdigit():
                out[p.name] = int(p.default.strip())
        return out

    # ---- transforms -------------------------------------------------- #
    def flattened(self) -> "ModelicaModelSpec":
        """Return an equivalent spec with no arrays and no `for` loops.

        Array variables `x[n]` become scalars `x_1 ... x_n`; `x[k]` in equations becomes `x_k`; `for i in a:b loop ... end for;` is unrolled; `sum(x)` over a known array becomes `(x_1 + ... + x_n)`. Integer array-size parameters are kept (harmless) but their array uses are resolved.

        Best effort: it handles the constructs typical of relay / controller models (scalar-indexed 1-D arrays, integer ranges). Nested indexing, 2-D arrays and `for` with non-integer ranges are not supported - keep those scalar in the source, or build the `TypMdl` from an already-flat spec.
        """
        sizes = self.integer_parameter_values()

        def expand(vars_: list[ModelicaVariable]) -> list[ModelicaVariable]:
            out: list[ModelicaVariable] = []
            for v in vars_:
                if not v.is_array:
                    out.append(v)
                    continue
                n = v.array_length(sizes)
                defaults = _split_array_literal(v.default, n)
                starts = _split_array_literal(v.start, n)
                for k in range(1, n + 1):
                    out.append(
                        replace(
                            v,
                            name=f"{v.name}_{k}",
                            size="",
                            default=defaults[k - 1],
                            start=starts[k - 1],
                            description=(f"{v.description} [{k}]" if v.description else ""),
                        )
                    )
            return out

        array_names = {v.name for v in self.all_variables if v.is_array}
        array_lengths = {
            v.name: v.array_length(sizes) for v in self.all_variables if v.is_array
        }
        return ModelicaModelSpec(
            name=self.name,
            method=self.method,
            inputs=expand(self.inputs),
            outputs=expand(self.outputs),
            parameters=expand(self.parameters),
            states=expand(self.states),
            internals=expand(self.internals),
            init_equations=_flatten_equations(
                self.init_equations, sizes, array_names, array_lengths
            ),
            equations=_flatten_equations(
                self.equations, sizes, array_names, array_lengths
            ),
            description=self.description,
            author=self.author,
        )

    # ---- codegen ---------------------------------------------------- #
    def to_modelica(self) -> str:
        """Emit a standalone, standard-Modelica `.mo` source string."""
        lines = [f"model {self.name}"]
        if self.description:
            lines[0] += f' "{self.description}"'
        for p in self.parameters:
            lines.append("  " + _declare(p, prefix="parameter "))
        for v in self.inputs:
            lines.append("  " + _declare(v, prefix="input "))
        for v in self.outputs:
            lines.append("  " + _declare(v, prefix="output "))
        if self.states or self.internals:
            lines.append("protected")
            for v in (*self.states, *self.internals):
                lines.append("  " + _declare(v))
        if self.init_equations:
            kw = "initial equation" if self.method == "hybrid" else "initial algorithm"
            lines.append(kw)
            lines += [f"  {e}" for e in self.init_equations]
        kw = "equation" if self.method == "hybrid" else "algorithm"
        lines.append(kw)
        lines += [f"  {e}" for e in self.equations]
        lines.append(f"end {self.name};")
        return "\n".join(lines) + "\n"

    # ---- parsing --------------------------------------------------- #
    @classmethod
    def from_modelica(cls, source: str | Path) -> "ModelicaModelSpec":
        """Best-effort parse of a single-model `.mo` file (path or text).

        Understands `model NAME "desc"` ... `end NAME;`, one declaration per line (`[parameter|input|output] Type name[size] [= default] ["desc"]` with optional `(unit=..., start=..., min=..., max=...)` modifiers), a `protected` section (a variable is a state if `der(<name>)` appears in the equations, otherwise an internal variable), and `initial equation` / `equation` / `initial algorithm` / `algorithm` sections. It does not evaluate expressions or handle multi-line declarations - for anything exotic, build the spec directly.
        """
        text = Path(source).read_text() if _looks_like_path(source) else str(source)
        return _parse_modelica(text)


# --------------------------------------------------------------------------- #
# PowerFactory interface
# --------------------------------------------------------------------------- #


class ModelicaModel(ApplicationBase):
    """Create, compile and read back PowerFactory Modelica model types ('TypMdl') and their instances ('ElmMdl').

    This is the PowerFactory-facing half of the module (see the module docstring for the full picture). Give `create_model_type` a `ModelicaModelSpec` - from a parsed `.mo` file or built in Python - and it writes every declaration column and equation field of a new `TypMdl` and compiles it, raising `PFModelicaCompilationError` (with the PowerFactory output-window messages) if `Check()` or `Compile()` fails. `create_model` then instantiates it as an `ElmMdl`, and `read_model_type` goes the other way, turning an existing `TypMdl` back into a `ModelicaModelSpec`.

    Needs an active project; the `TypMdl` is created in that project's dynamic-models library folder (`get_dynamic_models_folder`) by default.
    """

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)

    # ---- folders ---------------------------------------------------- #
    def get_dynamic_models_folder(self) -> PFGeneral:
        """The project's dynamic-models library folder (`app.GetProjectFolder("blk")`). Its display name varies by project / language ('Dynamic Models', 'User Defined Models', ...); TypMdl objects can only be created here or in a subfolder of it."""
        folder = self.app.GetProjectFolder("blk")
        if folder is None:
            raise FileNotFoundError(
                "the active project has no dynamic-models folder "
                "(app.GetProjectFolder('blk') returned None)"
            )
        return folder

    # ---- model type ----------------------------------------------- #
    def create_model_type(
        self,
        spec: ModelicaModelSpec,
        folder: PFGeneral | str | None = None,
        *,
        flatten: bool = True,
        compile: bool = True,
        overwrite: bool = True,
    ) -> TypMdl:
        """Create the `TypMdl` for `spec` and (optionally) compile it.

        This is the step that turns a parsed `.mo` file (or a hand-built spec) into a usable PowerFactory Modelica model type: it creates the `TypMdl`, sets `modMethod`, fills the input / output / parameter / state / internal declaration tables and the equation (or algorithm) fields, then runs `Check()` and `Compile()`.

        Args:
            spec: the model description.
            folder: target folder (must be 'Dynamic Models' or a subfolder); defaults to `get_dynamic_models_folder()`.
            flatten: apply `spec.flattened()` first (unroll for-loops / arrays). Leave True unless the spec is already scalar-only.
            compile: run `TypMdl.Compile()` and raise `PFModelicaCompilationError` on failure. If False, only `Check()` is run.
            overwrite: replace an existing TypMdl of the same name in `folder`.

        Returns:
            TypMdl: the created (and compiled) model type.
        """
        if flatten:
            spec = spec.flattened()
        folder = (
            self.get_dynamic_models_folder()
            if folder is None
            else self.act_prj._handle_single_pf_object_or_path_input(folder)
        )
        if overwrite:
            self.act_prj.delete_obj(
                f"{spec.name}.TypMdl", parent_folder=folder, error_if_non_existent=False
            )
        typ: TypMdl = folder.CreateObject("TypMdl", spec.name)
        if typ is None:
            raise RuntimeError(
                f"PowerFactory refused to create '{spec.name}.TypMdl' in "
                f"'{self.act_prj.get_path_of_object(folder)}' - "
                f"the folder must be 'Dynamic Models' or a subfolder of it"
            )

        typ.SetAttribute("modMethod", _METHOD_CODE[spec.method])
        if spec.description:
            typ.SetAttribute("desc", [spec.description])
        if spec.author:
            typ.SetAttribute("author", spec.author)

        self._write_variable_table(typ, "input", spec.inputs, with_variability=True)
        self._write_variable_table(typ, "output", spec.outputs, with_variability=True)
        self._write_variable_table(typ, "param", spec.parameters, value_field="default")
        self._write_variable_table(typ, "state", spec.states, value_field="start")
        self._write_variable_table(typ, "inter", spec.internals, value_field="start")

        if spec.method == "hybrid":
            typ.SetAttribute("initEquation", list(spec.init_equations))
            typ.SetAttribute("equation", list(spec.equations))
        else:
            typ.SetAttribute("initAlgorithm", list(spec.init_equations))
            typ.SetAttribute("algorithm", list(spec.equations))

        self._check_or_compile(typ, spec.name, compile)
        return typ

    def _write_variable_table(
        self,
        typ: TypMdl,
        prefix: str,
        variables: list[ModelicaVariable],
        *,
        with_variability: bool = False,
        value_field: str = "start",
    ) -> None:
        """Write one declaration table of a TypMdl.

        String columns (name/unit/description/size + default|start) are set as whole lists; the numeric-enum columns (base type, variability) must be set element by element (`SetAttribute("inputType:0", 0)`), whole-list writes to them are silently ignored by PowerFactory.
        """
        if not variables:
            return
        typ.SetAttribute(f"{prefix}Name", [v.name for v in variables])
        typ.SetAttribute(f"{prefix}Unit", [v.unit for v in variables])
        typ.SetAttribute(f"{prefix}Desc", [v.description for v in variables])
        typ.SetAttribute(f"{prefix}Size", [v.size for v in variables])
        typ.SetAttribute(f"{prefix}Min", [v.minimum for v in variables])
        typ.SetAttribute(f"{prefix}Max", [v.maximum for v in variables])
        value_attr = "paramDefault" if prefix == "param" else f"{prefix}Start"
        typ.SetAttribute(
            value_attr, [getattr(v, "default" if prefix == "param" else "start") for v in variables]
        )
        for i, v in enumerate(variables):
            typ.SetAttribute(f"{prefix}Type:{i}", _BASE_TYPE_CODE[v.base_type])
            if with_variability:
                typ.SetAttribute(
                    f"{prefix}Variability:{i}", _VARIABILITY_CODE[v.variability]
                )

    def _check_or_compile(self, typ: TypMdl, name: str, compile: bool) -> None:
        self.app.ClearOutputWindow()
        if typ.Check() != 0:
            raise PFModelicaCompilationError(name, self._output_window_messages())
        if not compile:
            return
        self.app.ClearOutputWindow()
        # second arg overrideModel=1: replace an already compiled model at the same location
        if typ.Compile("", 1) != 0:
            raise PFModelicaCompilationError(name, self._output_window_messages())

    def _output_window_messages(self) -> list[str]:
        try:
            content = self.app.GetOutputWindow().GetContent()
        except Exception:
            return []
        return [str(line).replace("\n", " ") for line in content]

    # ---- model instance ----------------------------------------- #
    def create_model(
        self,
        model_type: TypMdl | str,
        parent_folder: PFGeneral | str | None = None,
        *,
        name: str | None = None,
        parameters: dict[str, float | int | bool] | None = None,
        overwrite: bool = True,
    ) -> ElmMdl:
        """Create a Modelica Model ('ElmMdl') instance referencing `model_type`.

        Args:
            model_type: the TypMdl (or its path).
            parent_folder: where to create the ElmMdl; defaults to the network data folder.
            name: instance name; defaults to the type name.
            parameters: `{param_name: value}` scalar parameter values to set on the instance. Setting these only works once PowerFactory has populated the instance's parameter list from the (compiled) type; a warning is issued for any name that cannot be set, and array parameters (which reference IntMat objects) are not handled here.
            overwrite: replace an existing ElmMdl of the same name.
        """
        model_type = self.act_prj._handle_single_pf_object_or_path_input(model_type)
        parent_folder = (
            self.act_prj.network_data_folder
            if parent_folder is None
            else self.act_prj._handle_single_pf_object_or_path_input(parent_folder)
        )
        name = name or model_type.loc_name
        if overwrite:
            self.act_prj.delete_obj(
                f"{name}.ElmMdl",
                parent_folder=parent_folder,
                error_if_non_existent=False,
            )
        model: ElmMdl = parent_folder.CreateObject("ElmMdl", name)
        model.SetAttribute("typ_id", model_type)
        unset = []
        for param_name, value in (parameters or {}).items():
            try:
                if not model.HasAttribute(param_name):
                    raise AttributeError(param_name)
                model.SetAttribute(param_name, value)
            except Exception:
                unset.append(param_name)
        if unset:
            warn(
                f"could not set parameter(s) {unset} on '{name}' - open the model dialog "
                f"once or set them after the type's parameter list is populated",
                stacklevel=2,
            )
        return model

    # ---- read back --------------------------------------------- #
    def read_model_type(self, model_type: TypMdl | str) -> ModelicaModelSpec:
        """Reconstruct a `ModelicaModelSpec` from an existing `TypMdl` (the editable declarations, not the compiled cache)."""
        typ = self.act_prj._handle_single_pf_object_or_path_input(model_type)
        method = _METHOD_NAME.get(int(typ.GetAttribute("modMethod")), "hybrid")

        def read_table(prefix: str, has_variability: bool, value_field: str) -> list:
            names = typ.GetAttribute(f"{prefix}Name") or []
            units = typ.GetAttribute(f"{prefix}Unit") or []
            descs = typ.GetAttribute(f"{prefix}Desc") or []
            sizes = typ.GetAttribute(f"{prefix}Size") or []
            types = typ.GetAttribute(f"{prefix}Type") or []
            varis = typ.GetAttribute(f"{prefix}Variability") or [] if has_variability else []
            values = (
                typ.GetAttribute("paramDefault" if prefix == "param" else f"{prefix}Start")
                or []
            )
            out = []
            for i, nm in enumerate(names):
                out.append(
                    ModelicaVariable(
                        name=nm,
                        base_type=_BASE_TYPE_NAME.get(int(types[i]) if i < len(types) else 0, "Real"),
                        variability=_VARIABILITY_NAME.get(
                            int(varis[i]) if i < len(varis) else 1, "continuous"
                        ),
                        size=sizes[i] if i < len(sizes) else "",
                        unit=units[i] if i < len(units) else "",
                        description=descs[i] if i < len(descs) else "",
                        **{
                            value_field: values[i] if i < len(values) else "",
                        },
                    )
                )
            return out

        init_attr, eq_attr = (
            ("initEquation", "equation")
            if method == "hybrid"
            else ("initAlgorithm", "algorithm")
        )
        return ModelicaModelSpec(
            name=typ.loc_name,
            method=method,
            inputs=read_table("input", True, "start"),
            outputs=read_table("output", True, "start"),
            parameters=read_table("param", False, "default"),
            states=read_table("state", False, "start"),
            internals=read_table("inter", False, "start"),
            init_equations=list(typ.GetAttribute(init_attr) or []),
            equations=list(typ.GetAttribute(eq_attr) or []),
            description=_first(typ.GetAttribute("desc")),
        )


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


# --------------------------------------------------------------------------- #
# helpers (pure python)
# --------------------------------------------------------------------------- #


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


def _declare(v: ModelicaVariable, prefix: str = "") -> str:
    is_parameter = prefix.startswith("parameter")
    decl = f"{prefix}{v.base_type} {v.name}"
    if v.is_array:
        decl += f"[{v.size.strip().strip('[]').strip()}]"
    mods = []
    if v.unit:
        mods.append(f'unit="{v.unit}"')
    if v.start and not is_parameter:
        mods.append(f"start={v.start}")
    if v.minimum:
        mods.append(f"min={v.minimum}")
    if v.maximum:
        mods.append(f"max={v.maximum}")
    if mods:
        decl += "(" + ", ".join(mods) + ")"
    if is_parameter and v.default:
        decl += f" = {v.default}"
    if v.description:
        decl += f' "{v.description}"'
    return decl + ";"


def _split_array_literal(literal: str, n: int) -> list[str]:
    """'{1, 2, 3}' -> ['1','2','3']; '' -> ['']*n; a scalar -> [scalar]*n."""
    literal = literal.strip()
    if not literal:
        return [""] * n
    if literal.startswith("{") and literal.endswith("}"):
        parts = _split_top_level(literal[1:-1])
        if len(parts) != n:
            raise ValueError(f"array literal {literal!r} has {len(parts)} entries, expected {n}")
        return [p.strip() for p in parts]
    return [literal] * n


def _split_top_level(s: str) -> list[str]:
    """Split on commas that are not inside braces/parens."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch in "{(":
            depth += 1
        elif ch in ")}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


_FOR_RE = re.compile(r"^\s*for\s+(\w+)\s+in\s+([^:]+):([^:]+)\s+loop\s*$")
_END_FOR_RE = re.compile(r"^\s*end\s+for\s*;\s*$")


def _flatten_equations(
    lines: list[str],
    int_params: dict[str, int],
    array_names: set[str],
    array_lengths: dict[str, int],
) -> list[str]:
    """Unroll `for i in a:b loop ... end for;`, then rewrite `x[k]`/`sum(x)` for array names."""
    unrolled = _unroll_for_loops(lines, int_params)
    return [_rewrite_array_access(ln, array_names, array_lengths) for ln in unrolled]


def _unroll_for_loops(lines: list[str], int_params: dict[str, int]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        m = _FOR_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        var, lo_s, hi_s = m.group(1), m.group(2).strip(), m.group(3).strip()
        lo = int_params.get(lo_s, _int_or_none(lo_s))
        hi = int_params.get(hi_s, _int_or_none(hi_s))
        if lo is None or hi is None:
            raise ValueError(f"cannot unroll {lines[i].strip()!r} - range must be integers or Integer parameters")
        depth, body = 1, []
        i += 1
        while i < len(lines):
            if _FOR_RE.match(lines[i]):
                depth += 1
            elif _END_FOR_RE.match(lines[i]):
                depth -= 1
                if depth == 0:
                    i += 1
                    break
            body.append(lines[i])
            i += 1
        body = _unroll_for_loops(body, int_params)  # nested loops
        for k in range(lo, hi + 1):
            for bl in body:
                out.append(_substitute_index(bl, var, k))
    return out


def _substitute_index(line: str, var: str, value: int) -> str:
    return re.sub(rf"\b{re.escape(var)}\b", str(value), line)


def _rewrite_array_access(line: str, array_names: set[str], array_lengths: dict[str, int]) -> str:
    """`x[3]` -> `x_3` for known arrays; `sum(x)` -> `(x_1 + x_2 + ... + x_n)`."""

    def sum_repl(m: re.Match) -> str:
        name = m.group(1)
        if name not in array_lengths:
            return m.group(0)
        n = array_lengths[name]
        return "(" + " + ".join(f"{name}_{k}" for k in range(1, n + 1)) + ")"

    line = re.sub(r"\bsum\(\s*(\w+)\s*\)", sum_repl, line)

    def idx_repl(m: re.Match) -> str:
        name, idx = m.group(1), m.group(2).strip()
        if name in array_names and idx.lstrip("-").isdigit():
            return f"{name}_{idx}"
        return m.group(0)

    return re.sub(r"\b(\w+)\[\s*([^\]]+)\s*\]", idx_repl, line)


def _int_or_none(s: str) -> int | None:
    try:
        return int(s)
    except ValueError:
        return None


def _first(value) -> str:
    if isinstance(value, (list, tuple)):
        return value[0] if value else ""
    return value or ""


def _looks_like_path(source) -> bool:
    if isinstance(source, Path):
        return True
    return isinstance(source, str) and "\n" not in source and source.strip().endswith(".mo")


# ---- .mo parser -------------------------------------------------------- #

_MODEL_RE = re.compile(r'^\s*(?:model|block|class)\s+(\w+)\s*(?:"([^"]*)")?')
_DECL_RE = re.compile(
    r"""^\s*
    (?P<prefixes>(?:parameter\s+|input\s+|output\s+|constant\s+|discrete\s+|flow\s+|each\s+)*)
    (?P<type>Real|Integer|Boolean)\s+
    (?P<name>\w+)
    (?:\s*\[\s*(?P<size>[^\]]+)\s*\])?
    (?:\s*\(\s*(?P<mods>[^)]*)\s*\))?
    (?:\s*=\s*(?P<default>[^";]+?))?
    (?:\s*"(?P<desc>[^"]*)")?
    \s*;\s*$
    """,
    re.VERBOSE,
)
_SECTION_KEYWORDS = {
    "protected": "protected",
    "public": "public",
    "initial equation": "init_eq",
    "initial algorithm": "init_eq",
    "equation": "eq",
    "algorithm": "eq",
}


def _parse_modelica(text: str) -> ModelicaModelSpec:
    spec = ModelicaModelSpec(name="Model")
    section = "decl"
    visibility = "public"
    method = "hybrid"
    protected_vars: list[ModelicaVariable] = []

    for raw in text.splitlines():
        line = raw.split("//", 1)[0].rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        m = _MODEL_RE.match(line)
        if m and section == "decl":
            spec.name = m.group(1)
            spec.description = m.group(2) or ""
            continue
        end_m = re.match(r"^\s*end\s+(\w+)\s*;\s*$", line)
        if end_m and end_m.group(1) not in ("when", "for", "if", "while"):
            break  # end of the model (`end <ModelName>;`)

        low = stripped.lower()
        if low in _SECTION_KEYWORDS:
            tag = _SECTION_KEYWORDS[low]
            if tag == "protected":
                visibility = "protected"
                section = "decl"
            elif tag == "public":
                visibility = "public"
                section = "decl"
            else:
                section = tag
                if "algorithm" in low:
                    method = "clocked"
            continue

        if section in ("init_eq", "eq"):
            (spec.init_equations if section == "init_eq" else spec.equations).append(stripped)
            continue

        d = _DECL_RE.match(line)
        if not d:
            continue
        prefixes = d.group("prefixes") or ""
        mods = _parse_modifiers(d.group("mods") or "")
        var = ModelicaVariable(
            name=d.group("name"),
            base_type=d.group("type"),
            size=(d.group("size") or "").strip(),
            unit=mods.get("unit", ""),
            description=d.group("desc") or "",
            start=mods.get("start", ""),
            default=(d.group("default") or "").strip(),
            minimum=mods.get("min", ""),
            maximum=mods.get("max", ""),
        )
        if "parameter" in prefixes:
            spec.parameters.append(var)
        elif "input" in prefixes:
            var.variability = "continuous"
            spec.inputs.append(var)
        elif "output" in prefixes:
            var.variability = "continuous"
            spec.outputs.append(var)
        elif visibility == "protected":
            protected_vars.append(var)

    # protected variable is a state if der(name) appears in the equations, else internal
    equation_text = " ".join(spec.equations)
    for var in protected_vars:
        if re.search(rf"\bder\(\s*{re.escape(var.name)}\b", equation_text):
            spec.states.append(var)
        else:
            spec.internals.append(var)
    spec.method = method
    return spec


def _parse_modifiers(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in _split_top_level(text):
        if "=" in part:
            k, _, v = part.partition("=")
            out[k.strip()] = v.strip().strip('"')
    return out
