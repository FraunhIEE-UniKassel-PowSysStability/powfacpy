"""
Base classes for elm.
"""

from abc import ABC
from powfacpy.pf_classes.protocols import PFGeneral, ElmNet
from powfacpy.base.base import BaseChildStatic
from powfacpy.base.active_project import ActiveProject


class ElmBase(BaseChildStatic):
    __slots__ = ()

    def __init__(self, obj: PFGeneral) -> None:
        super().__init__(obj)

    def set_out_of_service(self):
        self._obj.outserv = 1

    def set_into_service(self):
        self._obj.outserv = 0

    def get_parent_grid(self) -> ElmNet:
        act_prj = ActiveProject()
        return act_prj.get_upstream_obj(
            self._obj, lambda x: x.GetClassName() == "ElmNet"
        )


class SinglePortBase(ABC):
    __slots__ = ()

    @property
    def terminal(self):
        return self.bus1.cterm

    @property
    def p(self):
        return self._obj.pgini

    @p.setter
    def p(self, p: float):
        self.pgini = p

    def q(self):
        return self.qgini

    @p.setter
    def q(self, q: float):
        self.qgini = q
