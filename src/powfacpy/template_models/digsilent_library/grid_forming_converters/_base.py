"""Shared base class for the ``Templates\\Grid-forming Converters`` templates.

Frequency-relevant quantities and the conventions used here (from the DIgSILENT
technical reference *"Grid-forming Converter Templates"*, PF 2025, Sec. 2):

VSM / Synchronverter - swing equation, per unit (eq. 3):

    Ta * s * dw = p_set - p_mea - Dp * (w_r - w_set)

``Ta`` is DIgSILENT's "mechanical time constant". This module assumes the usual
convention ``Ta = 2 * H`` (as for `TypSym`'s acceleration time constant), so
``H = Ta / 2`` seconds on the converter's rated MVA. **TODO: confirm with the
user / a REGFM_B1 cross-check.**

Droop control (eq. 8): ``dw_droop = mp * dp_LPF`` with a first-order power
filter (``wc / (wc + s)``, i.e. time constant ``Tpf = 1 / wc``). The reference
notes droop and VSM behave identically when tuned so that

    Dp  <->  1 / mp        and        Ta  <->  Tpf / mp

hence the *equivalent* inertia of a droop converter is
``H_eq = Ta_eq / 2 = Tpf / (2 * mp)``.

**The meaning/scaling of ``mp`` differs between block definitions** (a plain pu
droop vs. a percentage vs. a gain); each concrete class states which it uses.
Where unsure the value is returned as-is and the docstring flags it.
"""

from __future__ import annotations

from powfacpy.pf_classes.protocols import ElmDsl
from powfacpy.template_models.base import TemplateModel


class GridFormingConverter(TemplateModel):
    """Base for the grid-forming-converter templates (Sec. 2 of the tech. ref.)."""

    NETWORK_ELEMENT_CLASSES = ("ElmGenstat", "ElmVsc", "ElmPvsys")

    #: how `get_inertia_constant` is obtained from the grid-forming DSL model
    INERTIA_MODE: str = "droop_equivalent"  # 'direct_H' | 'acceleration_time' | 'droop_equivalent' | 'none'
    INERTIA_PARAM: str | None = None  # H [s] (direct_H) or Ta [s] (acceleration_time)
    DROOP_PARAM: str | None = None  # active-power droop mp
    DAMPING_PARAM: str | None = None  # Dp
    #: power-measurement filter: a time constant Tpf [s], or a cut-off wc [rad/s]
    POWER_FILTER_TIME_CONSTANT_PARAM: str | None = None
    POWER_FILTER_CUTOFF_PARAM: str | None = None

    # ------------------------------------------------------------------ #
    @property
    def grid_forming_control(self) -> ElmDsl | None:
        """The wired DSL model that implements the grid-forming control law."""
        dsl = self.dsl_by_blkdef(*self.SIGNATURE_BLKDEF_NAMES)
        return dsl or self.dsl_in_slot("grid-forming", "grid forming")

    def _gf_param(self, name: str | None, default: float | None = None) -> float | None:
        if name is None:
            return default
        return self.parameter(self.grid_forming_control, name, default)

    # ------------------------------------------------------------------ #
    # frequency-stability quantities
    # ------------------------------------------------------------------ #
    def get_power_filter_time_constant(self) -> float | None:
        """First-order active-power measurement filter time constant `Tpf` [s]."""
        if self.POWER_FILTER_TIME_CONSTANT_PARAM:
            return self._gf_param(self.POWER_FILTER_TIME_CONSTANT_PARAM)
        cutoff = self._gf_param(self.POWER_FILTER_CUTOFF_PARAM)
        if cutoff:
            return 1.0 / cutoff
        return None

    def get_active_power_droop(self) -> float | None:
        """Active-power / frequency droop `mp` of the grid-forming control.

        Scaling is block-definition specific - see the concrete class docstring.
        """
        return self._gf_param(self.DROOP_PARAM)

    def get_damping(self) -> float | None:
        """Damping coefficient `Dp` (VSM/Synchronverter) or `1/mp` (droop)."""
        if self.DAMPING_PARAM:
            return self._gf_param(self.DAMPING_PARAM)
        droop = self.get_active_power_droop()
        return 1.0 / droop if droop else None

    def get_inertia_constant(self) -> float | None:
        """Inertia constant `H` [s] on the converter's rated MVA, or None.

        Returns None for pure-droop controls that carry no inertia term (use
        `get_equivalent_inertia_constant` for those).
        """
        if self.INERTIA_MODE == "direct_H":
            return self._gf_param(self.INERTIA_PARAM)
        if self.INERTIA_MODE == "acceleration_time":
            ta = self._gf_param(self.INERTIA_PARAM)
            return ta / 2.0 if ta is not None else None
        return None

    def get_equivalent_inertia_constant(self) -> float | None:
        """Inertia constant `H` [s], derived from the droop + filter if there is
        no explicit inertia (`H_eq = Tpf / (2 * mp)`)."""
        explicit = self.get_inertia_constant()
        if explicit is not None:
            return explicit
        tpf = self.get_power_filter_time_constant()
        droop = self.get_active_power_droop()
        if tpf is not None and droop:
            return tpf / (2.0 * droop)
        return None

    def get_effective_time_constant(self) -> float | None:
        """Time constant of the converter's first-order active-power / frequency
        response [s].

        - explicit inertia: `2 * H / D`
        - pure droop: the power-filter time constant `Tpf`
        """
        h = self.get_inertia_constant()
        d = self.get_damping()
        if h is not None and d:
            return 2.0 * h / d
        return self.get_power_filter_time_constant()

    def get_kinetic_energy_MWs(self) -> float | None:
        """Stored kinetic energy `H_eq * S` [MW s]."""
        h = self.get_equivalent_inertia_constant()
        s = self.rated_apparent_power_MVA
        if h is None or s is None:
            return None
        return h * s
