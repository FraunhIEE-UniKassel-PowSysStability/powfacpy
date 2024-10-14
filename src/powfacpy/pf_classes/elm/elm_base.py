from abc import ABC

from powfacpy.pf_classes.protocols import PFGeneral
from powfacpy.base.base import BaseChildStatic


class ElmBase(BaseChildStatic):
    __slots__ = ()

    def __init__(self, obj: PFGeneral) -> None:
        super().__init__(obj)

    def set_out_of_service(self):
        self._obj.outserv = 1

    def set_into_service(self):
        self._obj.outserv = 0


class SinglePortBase(ABC):
    __slots__ = ()

    @property
    def terminal(self):
        return self.bus1

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
