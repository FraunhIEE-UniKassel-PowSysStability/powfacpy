"""``Templates\\Grid-forming Converters\\Synchronverter``."""

from __future__ import annotations

from powfacpy.template_models.base import register
from powfacpy.template_models.digsilent_library.grid_forming_converters._base import (
    GridFormingConverter,
)


@register
class Synchronverter(GridFormingConverter):
    """Synchronverter grid-forming converter (Zhong & Weiss).

    Like the VSM it is based on the swing equation (tech. ref. eq. 3, with
    ``t_set``/``t_calc`` instead of ``p_set``/``p_mea``): ``Ta`` is treated as
    ``2 * H`` and ``Dp`` is the damping. Reactive power is controlled internally
    (``Kq`` integrator gain, ``Dq`` voltage droop), so there is no separate
    voltage-control slot.
    """

    TEMPLATE_LOC_NAMES = ("Synchronverter",)
    FRAME_BLKDEF_NAMES = ("Synchronverter Frame",)
    SIGNATURE_BLKDEF_NAMES = ("scv_synchronverter",)
    SIGNATURE_PARAMETER_NAMES = ("Ta", "Dp", "Kq", "Dq")

    INERTIA_MODE = "acceleration_time"
    INERTIA_PARAM = "Ta"
    DAMPING_PARAM = "Dp"
    POWER_FILTER_CUTOFF_PARAM = "w_c"

    def get_acceleration_time_constant(self) -> float | None:
        """`Ta` [s] as stored in PowerFactory (assumed to be `2 * H`)."""
        return self._gf_param("Ta")

    def get_reactive_power_droop(self) -> float | None:
        """`Dq` - the voltage / reactive-power droop coefficient."""
        return self._gf_param("Dq")
