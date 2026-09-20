"""Dynamic modal (small-signal) analysis.

Wraps PowerFactory's modal analysis command (`ComMod`) to compute, for
whatever state is currently active (activate the study case/scenario/
operating point yourself first, as with `DynamicSimulation` or `StaticCalc`):

- the system's eigenvalues, their damping ratio, natural and damped
  frequency, and dominant states (`ModalAnalysis`, `ModalAnalysisResults`);
- participation factors of each state in each eigenvalue
  (`ParticipationFactorSet`);
- how the eigenvalues move as a parameter changes and the sensitivity of an
  eigenvalue's metrics to that change (`track_eigenvalues`,
  `EigenvalueSweepResults`, `Sensitivity`, `sensitivity_between`,
  `ParametricSensitivity`) - built on top of `parstudy.Study` (see the
  *Parameter Studies* tutorial) rather than a bespoke sweep loop: `evaluate()`
  calls `ModalAnalysis.run()` once per point, `parstudy` handles the sweep
  strategy and snapshot/restore, and the helpers here turn the resulting
  sequence of `ModalAnalysisResults` into a consistently-indexed eigenvalue
  trajectory (PowerFactory does not guarantee eigenvalues come back in the
  same order run to run);
- two ways to get an eigenvalue's sensitivity to a parameter: `sensitivity_between`
  finite-differences the *eigenvalues* between two (tracked) runs; the
  analytical, eigenvector-weighted `ModalAnalysisResults.eigenvalue_sensitivity`
  needs only `dA/dp` (usually itself a finite difference of the *state
  matrix* - `system_matrix_sensitivity`) evaluated at a single run, so it
  needs no eigenvalue tracking at all. See the tutorial for a comparison of
  both on the same system.

See the *Dynamic Modal Analysis* tutorial, which also shows the connection to
`powfacpy.applications.dynamic_simulation`: a poorly-damped or unstable mode
found here should be visible as a sustained or growing oscillation in a
time-domain simulation of the same parameter point.

Needs the optional 'scipy' dependency: `pip install powfacpy[dynamic_modal_analysis]`.
Eigenvalue *sweeps* additionally need 'parstudy': `pip install powfacpy[parstudy]`.
"""

from powfacpy.applications.dynamic_modal_analysis._common import (  # noqa: F401
    INDEX_COL,
    REAL_COL,
    IMAG_COL,
    NATURAL_FREQ_COL,
    DAMPED_FREQ_COL,
    DAMPING_RATIO_COL,
    MODE_COL,
    DOMINANT_STATES_COL,
    _STYLE_PRECISION,
    DEFAULT_DOMINANT_QUANTILE,
    _auto_real_xlim,
)
from powfacpy.applications.dynamic_modal_analysis.eigenvalues import (  # noqa: F401
    Eigenvalue,
    EigenvalueSet,
    ParticipationFactor,
    ParticipationFactorSet,
)
from powfacpy.applications.dynamic_modal_analysis.tracking import (  # noqa: F401
    _IndexCandidate,
    _EigenvaluePositionElection,
    EigenvalueTracker,
    track_eigenvalues,
)
from powfacpy.applications.dynamic_modal_analysis.results import (  # noqa: F401
    ModalAnalysisResults,
)
from powfacpy.applications.dynamic_modal_analysis.analysis import (  # noqa: F401
    ModalAnalysis,
)
from powfacpy.applications.dynamic_modal_analysis.sweep import (  # noqa: F401
    EigenvalueSweepResults,
)
from powfacpy.applications.dynamic_modal_analysis.sensitivity import (  # noqa: F401
    Sensitivity,
    sensitivity_between,
    system_matrix_sensitivity,
    ParametricSensitivity,
)

__all__ = [
    "DAMPED_FREQ_COL",
    "DAMPING_RATIO_COL",
    "DEFAULT_DOMINANT_QUANTILE",
    "DOMINANT_STATES_COL",
    "Eigenvalue",
    "EigenvalueSet",
    "EigenvalueSweepResults",
    "EigenvalueTracker",
    "IMAG_COL",
    "INDEX_COL",
    "MODE_COL",
    "ModalAnalysis",
    "ModalAnalysisResults",
    "NATURAL_FREQ_COL",
    "ParametricSensitivity",
    "ParticipationFactor",
    "ParticipationFactorSet",
    "REAL_COL",
    "Sensitivity",
    "sensitivity_between",
    "system_matrix_sensitivity",
    "track_eigenvalues",
]
