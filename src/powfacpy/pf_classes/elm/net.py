from __future__ import annotations



from powfacpy.pf_classes.protocols import ElmNet
from powfacpy.pf_classes.elm.elm_base import (
    ElmBase,

)
from powfacpy.result_variables import ResVar

LDF = ResVar.LF_Bal


class Network(ElmBase):

    __slots__ = ()

    def __init__(self, obj: ElmNet) -> None:
        super().__init__(obj)
        self._obj: ElmNet

    def __new__(cls, *args, **kwargs) -> ElmNet | Network:
        """Implemented only to add type hints for the created instance.

        Returns:
            ElmNet | Network: New instance
        """
        instance = super().__new__(cls)
        return instance
    
    def show_grafic(self):
        self.pDiagram.Show()