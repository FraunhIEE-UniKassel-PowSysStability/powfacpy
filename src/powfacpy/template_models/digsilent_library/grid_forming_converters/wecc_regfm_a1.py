"""``Templates\\Grid-forming Converters\\WECC REGFM_A1 Droop Inverter - …``."""

from __future__ import annotations

from powfacpy.template_models.base import register
from powfacpy.template_models.digsilent_library.grid_forming_converters._base import (
    GridFormingConverter,
)


@register
class WeccRegfmA1(GridFormingConverter):
    """WECC REGFM_A1 - a pure-droop grid-forming inverter (no explicit inertia).

    Grid-forming control block (`BlkDef` ``REGFM_A1``): active-power droop ``mp``
    and power-measurement filter ``Tpf``. `get_inertia_constant` returns None;
    `get_equivalent_inertia_constant` gives ``Tpf / (2 * mp)``.

    Reference: WECC REGFM_A1 model specification (WECC MVWG).
    """

    TEMPLATE_LOC_NAMES = (
        "WECC REGFM_A1 Droop Inverter - Gen",
        "WECC REGFM_A1 Droop Inverter - Storage",
    )
    FRAME_BLKDEF_NAMES = ("Frame WECC GFM Inverter",)
    SIGNATURE_BLKDEF_NAMES = ("REGFM_A1",)
    SIGNATURE_PARAMETER_NAMES = ("mp", "Tpf", "Pmax", "Pmin", "ImaxF")

    INERTIA_MODE = "none"
    DROOP_PARAM = "mp"
    POWER_FILTER_TIME_CONSTANT_PARAM = "Tpf"

    def get_active_power_limits_pu(self) -> tuple[float | None, float | None]:
        """`(Pmax, Pmin)` of the grid-forming control, in pu of rated power."""
        return self._gf_param("Pmax"), self._gf_param("Pmin")
