"""``Templates\\Grid-forming Converters\\WECC REGFM_B1 VSM Inverter - …``."""

from __future__ import annotations

from powfacpy.template_models.base import register
from powfacpy.template_models.digsilent_library.grid_forming_converters._base import (
    GridFormingConverter,
)


@register
class WeccRegfmB1(GridFormingConverter):
    """WECC REGFM_B1 - a VSM-type grid-forming inverter with an explicit inertia constant.

    The grid-forming control block (`BlkDef` ``REGFM_B1``) carries ``H`` [s] (on
    the converter MVA base) directly, plus the active-power droop ``mp`` and the
    power-measurement filter ``Tpf``. Damping is split over ``D1`` (transient)
    and ``D2`` (through the washout ``wD``); `get_damping` falls back to
    ``1/mp`` - use `get_transient_damping` / `get_steady_state_damping` for the
    individual terms.

    Reference: Unifi Consortium, *"Virtual Synchronous Machine Grid-Forming
    Inverter Model Specification (REGFM_B1)"*, NREL/TP-5D00-90260, 2024.
    """

    TEMPLATE_LOC_NAMES = (
        "WECC REGFM_B1 VSM Inverter - Generation",
        "WECC REGFM_B1 VSM Inverter - Storage",
    )
    FRAME_BLKDEF_NAMES = ("Frame WECC GFM Inverter",)
    SIGNATURE_BLKDEF_NAMES = ("REGFM_B1",)
    SIGNATURE_PARAMETER_NAMES = ("H", "mp", "Tp", "D1", "D2", "wD")

    INERTIA_MODE = "direct_H"
    INERTIA_PARAM = "H"
    DROOP_PARAM = "mp"
    POWER_FILTER_TIME_CONSTANT_PARAM = "Tpf"

    def get_transient_damping(self) -> float | None:
        """`D1` - damping acting on the full frequency deviation."""
        return self._gf_param("D1")

    def get_steady_state_damping(self) -> float | None:
        """`D2` - damping acting on the washout-filtered frequency deviation."""
        return self._gf_param("D2")

    def get_washout_time_constant(self) -> float | None:
        """`1 / wD` [s] - the washout applied to the `D2` damping path."""
        w_d = self._gf_param("wD")
        return 1.0 / w_d if w_d else None
