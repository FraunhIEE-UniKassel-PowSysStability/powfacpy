from __future__ import annotations

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import ElmSym, TypSym

from powfacpy.pf_classes.elm.elm_base import ElmBase, SinglePortBase
from powfacpy.result_variables import ResVar


class SynchronousMachine(ElmBase, SinglePortBase):

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
    def H_in_pu_based_on_Snom(self) -> float:
        "Inertia constant [s]"
        return self._obj.typ_id.h

    @property
    def J(self) -> float:
        "Moment of Inertia [kgm^2]. Parallel machines are considered."
        obj = self._obj
        return obj.typ_id.J * obj.ngnum

    def get_averaged_internal_reactance(self) -> float:
        """If the machine is not symmetrical, an average of the d-and q-axis internal reactances are used. For example, for a 6th order model, one has xG =0.5(x'' d + x'' q ).

        Returns:
            float: internal reactance [pu]
        """
        typ: TypSym = self._obj.typ_id
        return 0.5 * (typ.xdss + typ.xqss)

    def get_averaged_internal_susceptance(self) -> float:
        return 1 / self.get_averaged_internal_reactance()

    @staticmethod
    def get_cgmes_mapping():
        return {"inertia": "h"}
