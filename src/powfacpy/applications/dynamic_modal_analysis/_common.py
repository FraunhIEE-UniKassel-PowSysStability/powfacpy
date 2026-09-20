"""Column names, shared constants and small helpers used across the modal analysis modules.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


# Column names shared by the eigenvalue / participation-factor / modal-results
# DataFrames.
INDEX_COL = "Index"


REAL_COL = "Real (1/s)"


IMAG_COL = "Imag (rad/s)"


NATURAL_FREQ_COL = "Undamped natural frequency (Hz)"


DAMPED_FREQ_COL = "Damped frequency (Hz)"


DAMPING_RATIO_COL = "Damping ratio"


MODE_COL = "Mode"


DOMINANT_STATES_COL = "Dominant states"


_STYLE_PRECISION = 4


#: default quantile (of the real part) used by the eigenvalue-plotting
#: methods' `xlim="auto"` to zoom in on the dominant (slowest-decaying, least
#: negative) eigenvalues instead of letting a handful of very fast/heavily
#: damped ones stretch the x-axis.
DEFAULT_DOMINANT_QUANTILE = 0.75


def _auto_real_xlim(
    real_parts: npt.NDArray, quantile: float = DEFAULT_DOMINANT_QUANTILE
) -> tuple[float, float]:
    """A `(lo, hi)` x-axis range framing the dominant eigenvalues - those
    with the largest (least negative) real part, which decay slowest and
    therefore dominate the long-term time response - instead of the full
    range, which a handful of very fast/heavily-damped eigenvalues can
    otherwise stretch until the dominant ones are an unreadable cluster near
    the origin.

    `lo` is the `quantile`-th percentile of the real parts (raise `quantile`
    to zoom in further, lower it to include more of the faster eigenvalues);
    `hi` is just past the largest real part (at least 0, so the
    stable/unstable boundary is always visible).
    """
    real_parts = np.asarray(real_parts, dtype=float)
    hi = max(float(np.max(real_parts)), 0.0)
    lo = min(float(np.quantile(real_parts, quantile)), hi - 1.0)
    lo = max(lo, float(np.min(real_parts)))
    span = hi - lo
    margin = 0.15 * span if span > 0 else 1.0
    return lo - margin, hi + margin
