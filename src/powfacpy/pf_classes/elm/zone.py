from __future__ import annotations

from typing import Callable

from powfacpy.pf_classes.protocols import ElmTerm, ElmZone, PFGeneral
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.pf_classes.elm.grouping_base import AreaZoneBase
from powfacpy.result_variables import ResVar
from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.set.colscheme import DiagramColorScheme

RMS_BAL = ResVar.RMS_Bal
LF_BAL = ResVar.LF_Bal


class ZoneStatic(ElmBase, AreaZoneBase):

    __slots__ = ()

    def __init__(self, obj: ElmZone) -> None:
        super().__init__(obj)
        self._obj: ElmZone

    def __new__(cls, *args, **kwargs) -> ElmZone | Zone:
        """Implemented only to add type hints for the instance.

        Returns:
            ElmZone | Zone: New instance
        """
        instance = super().__new__(cls)
        return instance

    def _get_elm_input(self, zone: Zone | ElmZone) -> ElmZone:
        """Handle Zone or ElmZone input and always return ElmZone.

        Small helper method to handle zone input argument for example.

        Args:
            zone (Zone | ElmZone): Zone or ElmZone

        Returns:
            ElmZone: Always ElmZone
        """
        try:
            if isinstance(zone, Zone):
                return zone._obj
            elif zone.GetClassName() == "ElmZone":
                return zone
            else:
                raise ValueError(
                    f"Expected type 'Zone' or 'ElmZone' for input argument 'zone'"
                )
        except AttributeError:
            raise ValueError(
                f"Expected type 'Zone' or 'ElmZone' for input argument 'zone'"
            )

    def _get_powfacpy_obj_input(self, zone: Zone | ElmZone) -> Zone:
        """Handle Zone or ElmZone input and always return Zone.

        Small helper method to handle zone input argument for example.

        Args:
            zone (Zone | ElmZone): Zone or ElmZone

        Returns:
            Zone: Always Zone
        """
        try:
            if isinstance(zone, Zone):
                return zone
            elif zone.GetClassName() == "ElmZone":
                return Zone(zone)
            else:
                raise ValueError(
                    f"Expected type 'Zone' or 'ElmZone' for input argument 'zone'"
                )
        except AttributeError:
            raise ValueError(
                f"Expected type 'Zone' or 'ElmZone' for input argument 'zone'"
            )

    def get_all_internal_elms(
        self,
    ) -> list[PFGeneral]:
        return self._obj.GetAll()

    def get_internal_elms_of_class(
        self, class_name: str, condition: Callable | None = None
    ) -> list[PFGeneral]:
        objs = self._obj.GetObjs(class_name)
        if not condition:
            return objs
        else:
            act_prj = ActiveProjectCached()
            elms = act_prj.get_by_condition(elms, condition)

    def get_all_groupings_of_same_type(self) -> list[ElmZone]:
        act_prj = ActiveProjectCached()
        return act_prj.get_calc_relevant_obj("ElmZone")

    def get_all_powfacpy_groupings_of_same_type(self) -> list[Zone]:
        return [Zone(z) for z in self.get_all_groupings_of_same_type()]

    def merge(self, zone_to_merge: ElmZone | Zone) -> ElmZone:
        if not isinstance(zone_to_merge, Zone):
            zone_to_merge = Zone(zone_to_merge)
        terminals: list[ElmTerm] = zone_to_merge.get_internal_elms_of_class("ElmTerm")
        for term in terminals:
            term.pZone = self._obj
        zone_to_merge.Delete()
        return self._obj

    @staticmethod
    def show_zones_in_network_graphic(reactivate_study_case: bool = True) -> None:
        """
        Shows interior regions of all areas in the single line diagram.
        """
        act_prj = ActiveProjectCached()
        setcolscheme = act_prj.get_diagram_color_scheme()
        DiagramColorScheme(setcolscheme).show_zones(reactivate_study_case)

    @staticmethod
    def get_P_exchange_res_var_lf_bal() -> str:
        return LF_BAL.ElmZone.c_InterP.value

    @staticmethod
    def get_Q_exchange_res_var_lf_bal() -> str:
        return LF_BAL.ElmZone.c_InterQ.value

    @staticmethod
    def get_P_exchange_res_var_rms_bal() -> str:
        return RMS_BAL.ElmZone.c_Pinter.value

    @staticmethod
    def get_Q_exchange_res_var_rms_bal() -> str:
        return RMS_BAL.ElmZone.c_Qinter.value


class Zone(ZoneStatic):
    pass
