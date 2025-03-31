from __future__ import annotations

from powfacpy.pf_classes.protocols import SetColscheme, PFGeneral
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.pf_classes.elm.grouping_base import GroupingBase
from powfacpy.result_variables import ResVar

RMS_BAL = ResVar.RMS_Bal
LF_BAL = ResVar.LF_Bal


class DiagramColorScheme(ElmBase):

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

    def show_boundary_interior_regions(self) -> None:
        self._obj.cUseColouring = 1
        self._obj.cGroup = 1
        self._obj.cColouring = 20

    def show_zones(self) -> None:
        self._obj.cUseColouring = 1
        self._obj.cGroup = 4
        self._obj.cColouring = 18

    def show_areas(self) -> None:
        self._obj.cUseColouring = 1
        self._obj.cGroup = 4
        self._obj.cColouring = 25
