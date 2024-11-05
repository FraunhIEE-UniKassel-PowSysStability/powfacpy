from __future__ import annotations

from powfacpy.pf_classes.protocols import ElmZone, PFGeneral
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.pf_classes.elm.grouping_base import GroupingBase
from powfacpy.result_variables import ResVar

RMS_BAL = ResVar.RMS_Bal
LF_BAL = ResVar.LF_Bal


class ZoneStatic(ElmBase, GroupingBase):

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

    def get_all_internal_elms(
        self,
    ) -> list[PFGeneral]:
        return self._obj.GetAll()

    def get_internal_elms_of_class(self, class_name: str) -> list[PFGeneral]:
        return self._obj.GetObjs(class_name)

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
