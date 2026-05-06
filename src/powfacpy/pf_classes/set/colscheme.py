from __future__ import annotations

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import IntCase, SetColscheme, PFGeneral
from powfacpy.pf_classes.elm.grouping_base import GroupingBase
from powfacpy.result_variables import ResVar
from powfacpy.base.base import BaseChildStatic

RMS_BAL = ResVar.RMS_Bal
LF_BAL = ResVar.LF_Bal


class DiagramColorScheme(BaseChildStatic):

    __slots__ = ()

    def __init__(self, obj: SetColscheme) -> None:
        super().__init__(obj)
        self._obj: SetColscheme

    def __new__(cls, *args, **kwargs) -> SetColscheme | DiagramColorScheme:
        """Implemented only to add type hints for the instance.

        Returns:
            SetColscheme | DiagramColorScheme: New instance
        """
        instance = super().__new__(cls)
        return instance

    def show_boundary_interior_regions(
        self, reactivate_study_case: bool = True
    ) -> None:
        self._obj.cUseColouring = 1
        self._obj.cGroup = 1
        self._obj.cColouring = 20
        if reactivate_study_case:
            self.reactivate_study_case()

    def show_zones(self, reactivate_study_case: bool = True) -> None:
        self._obj.SetAttribute("cUseColouring", 1)
        self._obj.SetAttribute("cGroup", 4)
        self._obj.SetAttribute("cColouring", 18)
        if reactivate_study_case:
            self.reactivate_study_case()

    def show_areas(self, reactivate_study_case: bool = True) -> None:
        self._obj.cUseColouring = 1
        self._obj.cGroup = 4
        self._obj.cColouring = 25
        if reactivate_study_case:
            self.reactivate_study_case()

    @staticmethod
    def reactivate_study_case() -> None:
        """
        The PF GUI might not react to the new settings. A reliable way to update the GUI is to reactivate the study case.
        """
        act_prj = ActiveProjectCached()
        act_prj.reactivate_study_case()
