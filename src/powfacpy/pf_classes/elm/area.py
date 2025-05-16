from __future__ import annotations

from powfacpy.pf_classes.protocols import ElmArea, ElmZone, PFGeneral
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.pf_classes.elm.grouping_base import GroupingBase
from powfacpy.result_variables import ResVar
from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.set.colscheme import DiagramColorScheme

RMS_BAL = ResVar.RMS_Bal
LF_BAL = ResVar.LF_Bal


class AreaStatic(ElmBase, GroupingBase):

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

    def get_all_internal_elms(
        self,
    ) -> list[PFGeneral]:
        return self._obj.GetAll()

    def get_internal_elms_of_class(self, class_name: str) -> list[PFGeneral]:
        return self._obj.GetObjs(class_name)

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
