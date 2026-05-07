from __future__ import annotations

"""
Base classes for elm.
"""

from abc import ABC
from typing import Callable
from powfacpy.exceptions import PFInvalidCondition
from powfacpy.pf_classes.protocols import ElmComp, PFGeneral, ElmNet
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

    def q(self) -> float:
        return self.qgini

    @p.setter
    def q(self, q: float):
        self.qgini = q

    def rated_apparent_power() -> float:
        pass


from powfacpy.pf_classes.elm.comp import CompositeModel


class ElmPlantControlledBase(ABC):
    """Elm that can be part of DSL frame (has attribute 'c_pmod' that points to a composite frame, i.e. a plant model)."""

    __slots__ = ()

    @property
    def composite_frame(self) -> ElmComp:
        return self._obj.c_pmod

    @composite_frame.setter
    def composite_frame(self, frame: ElmComp) -> None:
        self._obj.c_pmod = frame

    def get_network_elements_of_plant_model(
        self, condition: Callable | None = None, error_if_non_existent: bool = True
    ) -> list[PFGeneral]:
        """
        Get network elements of plant model (composite frame) on condition.

        Args:
            condition (Callable | None, optional): Condition to select network elements, e.g. 'lambda x: x.typ_id.loc_name.startswith("gov_")' to get governors. Defaults to None.
            error_if_non_existent (bool, optional): Raise exception if no objects that satisfy condition are found. Defaults to True.

        Raises:
            PFInvalidCondition: If no objects that satisfy condition are found.

        Returns:
            list[PFGeneral]: Network elements
        """
        elmcomp = CompositeModel(self.composite_frame)
        if condition is None:
            return elmcomp.get_network_elms()
        netelms = []
        for netelm in elmcomp.get_network_elms():
            if netelm and condition(netelm):
                netelms.append(netelm)
        if error_if_non_existent and not netelms:
            raise PFInvalidCondition("No network element found.")
        return netelms
