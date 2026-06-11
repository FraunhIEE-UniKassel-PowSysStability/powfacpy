from __future__ import annotations

from fnmatch import fnmatch
from typing import Callable

import numpy as np

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import ElmNet, PFGeneral, TypSym, ElmTerm, ElmDsl
from powfacpy.pf_classes.elm.elm_base import (
    ElmBase,
    SinglePortBase,

)
from powfacpy.pf_classes.elm.elm_plant_controlled_base import ElmPlantControlledBase
from powfacpy.pf_classes.elm.term import Terminal
from powfacpy.result_variables import ResVar
from powfacpy.engineering_helpers import get_weighted_average

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