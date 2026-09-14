"""``Templates\\Grid-forming Converters\\Droop Controlled Converter - …``
and ``… Droop Ctrld Converter - Island Grid …``."""

from __future__ import annotations

from powfacpy.template_models.base import register
from powfacpy.template_models.digsilent_library.grid_forming_converters._base import (
    GridFormingConverter,
)


@register
class DroopControlledConverter(GridFormingConverter):
    """DIgSILENT droop-controlled grid-forming converter (no explicit inertia).

    Droop law (tech. ref. eq. 8): ``dw_droop = mp * dp_LPF`` with a first-order
    power filter. `get_inertia_constant` returns None;
    `get_equivalent_inertia_constant` gives ``Tpf / (2 * mp)``.

    Covers the ``basic`` block (parameters ``mp``, ``mq``, ``w_c``) and the
    ``extended`` block (``mp``, ``mq``, ``Tpf``, ``Tqf``, plus P/Q limiters) - the
    ``basic`` block gives the filter as a cut-off ``w_c`` [rad/s], the
    ``extended`` one as a time constant ``Tpf`` [s]. The island-grid variants use
    the same block definitions.
    """

    TEMPLATE_LOC_NAMES = (
        "Droop Controlled Converter - Generation",
        "Droop Controlled Converter - Storage",
        "Droop Ctrld Converter - Island Grid Gen",
        "Droop Ctrld Converter - Island Grid Stor",
    )
    FRAME_BLKDEF_NAMES = ("Grid-forming Converter Frame",)
    SIGNATURE_BLKDEF_NAMES = (
        "gfm_droop control basic",
        "gfm_droop control extended",
    )
    SIGNATURE_PARAMETER_NAMES = ("mp", "mq")

    INERTIA_MODE = "none"
    DROOP_PARAM = "mp"
    POWER_FILTER_TIME_CONSTANT_PARAM = "Tpf"  # extended block
    POWER_FILTER_CUTOFF_PARAM = "w_c"  # basic block

    def get_reactive_power_droop(self) -> float | None:
        """`mq` - the reactive-power / voltage droop coefficient."""
        return self._gf_param("mq")
