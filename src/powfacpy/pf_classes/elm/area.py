from __future__ import annotations

from typing import Callable

import numpy as np

from powfacpy.pf_classes.protocols import ElmArea, ElmTerm, PFGeneral
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.pf_classes.elm.grouping_base import AreaZoneBase
from powfacpy.result_variables import ResVar
from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.set.colscheme import DiagramColorScheme

RMS_BAL = ResVar.RMS_Bal
LF_BAL = ResVar.LF_Bal


class AreaStatic(ElmBase, AreaZoneBase):

    __slots__ = ()

    def __init__(self, obj: ElmArea) -> None:
        super().__init__(obj)
        self._obj: ElmArea

    def __new__(cls, *args, **kwargs) -> ElmArea | Area:
        """Implemented only to add type hints for the instance.

        Returns:
            ElmArea | Area: New instance
        """
        instance = super().__new__(cls)
        return instance

    def _get_elm_input(self, area: Area | ElmArea) -> ElmArea:
        """Handle Area or ElmArea input and always return ElmArea.

        Small helper method to handle area input argument for example.

        Args:
            area (Area | ElmArea): Area or ElmArea

        Returns:
            ElmArea: Always ElmArea
        """
        try:
            if area.GetClassName() == "ElmArea":
                return area
            elif isinstance(area, area):
                return area._obj
            else:
                raise ValueError(
                    f"Expected type 'Area' or 'ElmArea' for input argument 'area'"
                )
        except AttributeError:
            raise ValueError(
                f"Expected type 'Area' or 'ElmArea' for input argument 'area'"
            )

    def _get_powfacpy_obj_input(self, area: Area | ElmArea) -> Area:
        """Handle Area or ElmArea input and always return Area.

        Small helper method to handle area input argument for example.

        Args:
            area (Area | ElmArea): Area or ElmArea

        Returns:
            Area: Always Area
        """
        try:
            if isinstance(area, Area):
                return area
            elif area.GetClassName() == "ElmArea":
                return Area(area)
            else:
                raise ValueError(
                    f"Expected type 'Area' or 'ElmArea' for input argument 'area'"
                )
        except AttributeError:
            raise ValueError(
                f"Expected type 'Area' or 'ElmArea' for input argument 'area'"
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

    def get_all_groupings_of_same_type(self) -> list[ElmArea]:
        act_prj = ActiveProjectCached()
        return act_prj.get_calc_relevant_obj("ElmArea")

    def get_all_powfacpy_groupings_of_same_type(self) -> list[Area]:
        return [Area(z) for z in self.get_all_groupings_of_same_type()]

    def merge(self, area_to_merge: ElmArea | Area) -> ElmArea:
        if not isinstance(area_to_merge, Area):
            area_to_merge = Area(area_to_merge)
        terminals: list[ElmTerm] = area_to_merge.get_internal_elms_of_class("ElmTerm")
        for term in terminals:
            term.pArea = self._obj
        area_to_merge.Delete()
        return self._obj

    # Load flow
    def load_flow_power_exchange_with_in_MVA(
        self, area: ElmArea | Area, return_value_no_exchange=np.nan
    ) -> complex:
        if isinstance(area, Area):
            area = area._obj
        if self.CalculateInterchangeTo(area) > 0:
            return self._obj.GetAttribute("c:Pinter") + 1j * self._obj.GetAttribute(
                "c:Qinter"
            )
        else:
            return return_value_no_exchange

    @staticmethod
    def show_areas_in_network_graphic() -> None:
        """Shows interior regions of all areas in the single line diagram."""
        act_prj = ActiveProjectCached()
        setcolscheme = act_prj.get_diagram_color_scheme()
        DiagramColorScheme(setcolscheme).show_areas()

    @staticmethod
    def get_P_exchange_res_var_lf_bal() -> str:
        return LF_BAL.ElmArea.c_InterP.value

    @staticmethod
    def get_Q_exchange_res_var_lf_bal() -> str:
        return LF_BAL.ElmArea.c_InterQ.value

    @staticmethod
    def get_P_exchange_res_var_rms_bal() -> str:
        return RMS_BAL.ElmArea.c_Pinter.value

    @staticmethod
    def get_Q_exchange_res_var_rms_bal() -> str:
        return RMS_BAL.ElmArea.c_Qinter.value


class Area(AreaStatic):
    pass
