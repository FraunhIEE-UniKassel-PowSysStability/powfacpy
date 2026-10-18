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

from powfacpy.applications.modelica._codegen import (  # noqa: F401
    _declare,
    _split_array_literal,
    _split_top_level,
    _FOR_RE,
    _END_FOR_RE,
    _flatten_equations,
    _unroll_for_loops,
    _substitute_index,
    _rewrite_array_access,
    _int_or_none,
)
from powfacpy.applications.modelica.spec import (  # noqa: F401
    BASE_TYPES,
    VARIABILITIES,
    _BASE_TYPE_CODE,
    _VARIABILITY_CODE,
    _BASE_TYPE_NAME,
    _VARIABILITY_NAME,
    _METHOD_CODE,
    _METHOD_NAME,
    ModelicaVariable,
    ModelicaModelSpec,
    _first,
    _looks_like_path,
    _MODEL_RE,
    _DECL_RE,
    _SECTION_KEYWORDS,
    _parse_modelica,
    _parse_modifiers,
)
from powfacpy.applications.modelica.model import (  # noqa: F401
    ModelicaModel,
)
from powfacpy.applications.modelica.testing import (  # noqa: F401
    ModelicaModelTest,
    ModelicaModelFrameTest,
    _num_str,
    ramp_events,
)

__all__ = [
    "BASE_TYPES",
    "ModelicaModel",
    "ModelicaModelFrameTest",
    "ModelicaModelSpec",
    "ModelicaModelTest",
    "ModelicaVariable",
    "VARIABILITIES",
    "ramp_events",
]
