"""``Templates\\Grid-forming Converters\\Virtual Synchronous Machine - …``."""

from __future__ import annotations

from powfacpy.template_models.base import register
from powfacpy.template_models.digsilent_library.grid_forming_converters._base import (
    GridFormingConverter,
)


@register
class VirtualSynchronousMachine(GridFormingConverter):
    """DIgSILENT Virtual Synchronous Machine (VSM) grid-forming converter.

    Swing equation (tech. ref. eq. 3): ``Ta * s * dw = p_set - p_mea - Dp * dw``.
    ``Ta`` ("mechanical time constant") is taken as ``2 * H`` -> `get_inertia_constant`
    returns ``Ta / 2`` [s]. ``Dp`` is the damping; the steady-state droop is
    ``1/Dp``. ``w_c`` [rad/s] is the power-measurement filter cut-off.

    Covers the ``basic`` and ``extended`` block definitions (the extended one
    adds limiters and an optional df/dt feedback ``Kw``/``Tw``).
    """

    TEMPLATE_LOC_NAMES = (
        "Virtual Synchronous Machine - Generation",
        "Virtual Synchronous Machine - Storage",
    )
    FRAME_BLKDEF_NAMES = ("Grid-forming Converter Frame",)
    SIGNATURE_BLKDEF_NAMES = (
        "gfm_virtual synchronous machine basic",
        "gfm_virtual synchronous machine extended",
    )
    SIGNATURE_PARAMETER_NAMES = ("Ta", "Dp", "w_c")

    INERTIA_MODE = "acceleration_time"
    INERTIA_PARAM = "Ta"
    DAMPING_PARAM = "Dp"
    POWER_FILTER_CUTOFF_PARAM = "w_c"

    def get_acceleration_time_constant(self) -> float | None:
        """`Ta` [s] as stored in PowerFactory (assumed to be `2 * H`)."""
        return self._gf_param("Ta")

    def has_frequency_derivative_feedback(self) -> bool:
        """Extended block only: whether the df/dt feedback (`Kw`, `Tw`) is active."""
        return bool(self._gf_param("Kw", 0.0))
