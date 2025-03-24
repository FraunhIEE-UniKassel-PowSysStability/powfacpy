from __future__ import annotations

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import ElmSym, TypSym, ElmTerm

from powfacpy.pf_classes.elm.elm_base import ElmBase, SinglePortBase
from powfacpy.result_variables import ResVar

LDF = ResVar.LF_Bal


class SynchronousMachine(ElmBase, SinglePortBase):

    __slots__ = ()

    def __init__(self, obj: ElmSym) -> None:
        super().__init__(obj)
        self._obj: ElmSym

    def __new__(cls, *args, **kwargs) -> ElmSym | SynchronousMachine:
        """Implemented only to add type hints for the created instance.

        Returns:
            ElmSym | SynchronousMachine: New instance
        """
        instance = super().__new__(cls)
        return instance

    @property
    def ratedS(self) -> float:
        "Apparent power [MVA]. Parallel machines are considered."
        obj = self._obj
        typ: TypSym = obj.typ_id
        return typ.sgn * obj.ngnum

    @property
    def H_in_seconds_based_on_Snom(self) -> float:
        "Inertia constant [s]"
        return self._obj.typ_id.h

    @property
    def J(self) -> float:
        "Moment of Inertia [kgm^2]. Parallel machines are considered."
        obj = self._obj
        return obj.typ_id.J * obj.ngnum

    def get_averaged_internal_reactance(
        self, base_apparent_power_MVA: float | None = None
    ) -> float:
        """Get average of the d-and q-axis internal reactances:
        xG = 0.5 (x''d + x''q)

        Returns:
            float: internal reactance [pu]
        """
        typ: TypSym = self._obj.typ_id
        x = 0.5 * (typ.xdss + typ.xqss)
        if base_apparent_power_MVA is None:
            return x
        else:
            return x / (self.ratedS / base_apparent_power_MVA)

    def get_averaged_internal_susceptance(
        self, base_apparent_power_MVA: float | None = None
    ) -> float:
        return 1 / self.get_averaged_internal_reactance(base_apparent_power_MVA)

    def get_approximate_internal_voltage(self) -> complex:
        """Get approximate internal voltage from power supply, terminal voltage and internal reactance.

        This is for example one way a system operator could approximate the internal voltage based on measurements at the point of connection.

        Returns:
            complex: approximate internal voltage
        """
        p = self._obj.GetAttribute(LDF.ElmSym.m_Psum_bus1.value) / self.ratedS
        q = self._obj.GetAttribute(LDF.ElmSym.m_Qsum_bus1.value) / self.ratedS
        terminal: ElmTerm = self._obj.bus1.cterm
        u_bus = terminal.GetAttribute("m:ur") + 1j * terminal.GetAttribute("m:ui")
        x = self.get_averaged_internal_reactance()
        return u_bus + (q * x + 1j * p * x) / u_bus

    def get_H_in_seconds(self, base_apparent_power_MVA: float | None = None) -> float:
        "Inertia constant [s]"
        if base_apparent_power_MVA is None:
            return self._obj.typ_id.h
        else:
            return self._obj.typ_id.h * (self.ratedS / base_apparent_power_MVA)

    @staticmethod
    def get_cgmes_mapping():
        return {"inertia": "h"}
