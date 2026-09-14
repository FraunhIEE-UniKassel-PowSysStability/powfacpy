"""PowerFactory-specific glue for the `parstudy` package.

Parameter studies - vary an attribute of one or several PF objects over a range,
run a simulation for each value, collect the results - are backend-agnostic
functionality that lives in the sibling `parstudy` package
(https://github.com/FraunhIEE-UniKassel-PowSysStability/parstudy): declare each
quantity to vary as a `parstudy.ModelParameter`, give a `parstudy.Study` one
`evaluate(values) -> (evaluated, raw)` callable, and it handles the sweep
strategy (one-at-a-time, grid, Latin hypercube, Sobol, ...), execution
(serial / parallel / resumable), restoring the model afterwards, and the
results table with correlation, regression, Sobol indices and plots on top.

`parstudy.ModelParameter` already accepts PowerFactory objects directly in its
`affects=[(obj, "attribute"), ...]` - it only calls `GetAttribute`/`SetAttribute`
if the object has them, `getattr`/`setattr` otherwise - so most parameter
studies need no powfacpy-specific class at all any more; see the
*Parameter Studies* tutorial. This module supplies the two things that are
genuinely PowerFactory-specific and not generic enough for `parstudy` itself:

- `pf_parameter(...)`: convenience for the common case of one attribute swept,
  in lockstep, across a *list* of PF objects (a linear range via
  `parstudy.linspace`, "set"/"multiply"/"add" against each object's own current
  value).
- `apply_gradient(...)`: writes a linear *gradient* across a list of objects
  instead - object 0 sweeps `par_range` one way, the last object the other way,
  so the group's average stays put. `parstudy.ModelParameter` only ever holds
  one shared value across all of `affects`, so there is no generic equivalent;
  declare such a parameter with `auto_apply=False` (keeping `affects` for the
  snapshot / restore / audit trail) and call `apply_gradient` from `evaluate` -
  see the tutorial.

Needs the optional 'parstudy' dependency: `pip install powfacpy[parstudy]`.
"""

from __future__ import annotations

from typing import Any, Sequence

import numpy as np

try:
    from parstudy import UNSET, ModelParameter, linspace
    from parstudy.parameters import set_attribute
except ImportError as exc:
    raise ImportError(
        "powfacpy.applications.parameter_studies needs the 'parstudy' package - "
        "install with `pip install powfacpy[parstudy]`"
    ) from exc

from powfacpy.pf_classes.protocols import PFGeneral


def pf_parameter(
    name: str,
    objs: "PFGeneral | Sequence[PFGeneral]",
    attr: str,
    par_range: tuple[float, float],
    steps: int,
    *,
    mode: str = "set",
    default: Any = UNSET,
    affects_simulation: bool = True,
) -> ModelParameter:
    """A `ModelParameter` sweeping `attr` in lockstep on one or several PF objects.

    Args:
        name: parameter name (becomes a column of the results table).
        objs: one PF object, or a list of them that all receive the same value.
        attr: attribute name written with `SetAttribute`.
        par_range: `(min, max)` of the swept range.
        steps: number of values in the range (`parstudy.linspace(*par_range, steps)`).
        mode: `"set"` (default, verbatim) / `"multiply"` / `"add"` - combined with
            each object's own value captured when the study starts
            (`parstudy.ModelParameter.mode`).
        default: value held while a different parameter is varied; defaults to
            the mean of `par_range` (`ModelParameter`'s own default).
        affects_simulation: set False for a parameter that only affects
            post-processing, not the simulation itself - see the tutorial.
    """
    if not isinstance(objs, (list, tuple)):
        objs = [objs]
    return ModelParameter(
        name,
        linspace(*par_range, steps),
        default=default,
        affects=[(obj, attr) for obj in objs],
        mode=mode,
        affects_simulation=affects_simulation,
    )


def apply_gradient(
    objs: Sequence[PFGeneral],
    attr: str,
    par_range: tuple[float, float],
    value: float,
    *,
    mode: str = "set",
    baseline: Sequence[float] | None = None,
) -> None:
    """Write `value` (a point in `par_range`) across `objs` as a linear gradient.

    Object 0 moves from `par_range[0]` (reached when `value == par_range[0]`)
    towards `par_range[1]`; the last object moves the opposite way; every object
    in between interpolates linearly. The group's average therefore stays at the
    range's midpoint as `value` sweeps - e.g. spreading generator inertias across
    a fleet while keeping the system's total inertia unchanged.

    `mode` combines the gradient target with each object's own baseline value
    (`baseline[i]`, required unless `mode="set"`), exactly like
    `parstudy.ModelParameter.mode`: `"set"` (default) writes it verbatim,
    `"multiply"` / `"add"` combine it with `baseline[i]`.

    Call this from `evaluate`, once per run, for a parameter declared with
    `ModelParameter(..., affects=[(obj, attr) for obj in objs], auto_apply=False)`
    - `affects` then only drives the snapshot / restore-on-exit and the audit
    trail in `StudyResults.affected_values`; the actual write happens here.
    """
    if mode not in ("set", "multiply", "add"):
        raise ValueError("mode must be 'set', 'multiply' or 'add'")
    lo, hi = par_range
    n = len(objs)
    frac = 0.0 if hi == lo else (value - lo) / (hi - lo)
    grad_start = np.linspace(lo, hi, n)
    for k, obj in enumerate(objs):
        target = grad_start[k] + frac * (grad_start[-1 - k] - grad_start[k])
        if mode == "multiply":
            target *= baseline[k]
        elif mode == "add":
            target += baseline[k]
        set_attribute(obj, attr, target)
