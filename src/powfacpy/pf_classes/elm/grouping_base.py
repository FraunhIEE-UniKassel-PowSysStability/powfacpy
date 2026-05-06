from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

import numpy as np
from icecream import ic

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import ElmArea, ElmZone, PFGeneral, ElmRes, StaPll
from powfacpy.pf_classes.elm.sym import SynchronousMachine
from powfacpy.pf_classes.class_conversion import convert_pf_obj_to_powfacpy
from powfacpy.exceptions import PFInvalidLoadFlow
from powfacpy.result_variables import ResVar

LF = ResVar.LF_Bal


class GroupingBase(ABC):
    """Base class for groupings (ElmZone, ElmArea, ElmBoundary). Provides a common interface (e.g. to get internal elements)."""

    __slots__ = ()

    def __eq__(self, other: GroupingBase) -> bool:
        if not isinstance(other, GroupingBase):
            return False
        return self._obj == other._obj

    def add_results_variable_for_elms(
        self,
        condition_for_elms: Callable,
        result_variables: str | list[str],
        results_obj: ElmRes | None = None,
    ) -> None:
        """Add results variable for internal elements selected by 'condition'.

        Args:
            condition_for_elms (Callable): Condition to select elements, e.g. 'lambda x: x.GetClassName() = "ElmTerm"'

            result_variables (str | list[str]): Results variable name(s).

            results_obj (ElmRes | None, optional): Results object where variables are added. Defaults to None ('get_from_study_case' is used).
        """
        act_prj = ActiveProjectCached()
        if not results_obj:
            results_obj = act_prj.get_from_study_case("ElmRes")
        else:
            results_obj = act_prj._handle_single_pf_object_or_path_input(results_obj)
        elms = self.get_internal_elms(condition_for_elms)
        for elm in elms:
            act_prj.add_results_variable(elm, result_variables, results_obj)

    def get_internal_elms(self, condition: Callable | None = None) -> list[PFGeneral]:
        """Get internal elements with optional condition.

        Args:
            condition_for_elms (Callable): Condition to select elements, e.g. 'lambda x: x.GetClassName() = "ElmTerm"'

        Returns:
            list[PFGeneral]: list of network elements.
        """
        elms = self.get_all_internal_elms()
        if condition:
            act_prj = ActiveProjectCached()
            elms = act_prj.get_by_condition(elms, condition)
        return elms

    def get_internal_elms_of_class(self, class_name: str) -> list[PFGeneral]:
        return self.get_internal_elms(lambda x: x.GetClassName() == class_name)

    def get_network_elements_of_plant_models(
        self,
        elm_objs: list[str] | list[PFGeneral],
        condition: Callable,
    ) -> dict:
        elm_objs = list(elm_objs)
        if isinstance(elm_objs[0], str):
            objs = []
            for cls in elm_objs:
                objs += self.get_internal_elms_of_class(cls)
            elm_objs = objs
        obj_netelm = {}
        for obj in elm_objs:
            obj = convert_pf_obj_to_powfacpy(obj)
            netelm = obj.get_network_elements_of_plant_model(
                condition, error_if_non_existent=False
            )
            obj_netelm[obj._obj] = netelm
        return obj_netelm

    def get_network_elements_of_plant_models_sorted_by_block_definition(
        self,
        elm_objs: list[str] | list[PFGeneral],
        condition: Callable,
    ) -> dict:
        obj_netelm = self.get_network_elements_of_plant_models(elm_objs, condition)
        blkdef_elm = {}
        for obj, netelms in obj_netelm.items():
            for netelm in netelms:
                blkdef = netelm.typ_id
                val = blkdef_elm.get(blkdef)
                if not val:
                    blkdef_elm[blkdef] = {"elm": [], "elmdsl": []}
                blkdef_elm[blkdef]["elm"].append(obj)
                blkdef_elm[blkdef]["elmdsl"].append(netelm)
        return blkdef_elm

    def get_total_inertia_of_synchronous_machines_in_MWs(self) -> float:
        """Sum of inertia of internal synchronous machines in MWs"""
        sms = self.get_internal_elms_of_class("ElmSym")
        return np.sum([SynchronousMachine(sm).H_in_MWs for sm in sms])

    def get_phase_locked_loops(self) -> list[StaPll]:
        """Get all internal phase-locked loops (StaPll) objects (i.e. PLLs that measure at internal terminals).

        Returns:
            list[StaPll]: List of internal PLLs.
        """
        act_prj = ActiveProjectCached()
        all_plls: list[StaPll] = act_prj.get_calc_relevant_obj("*.StaPll")
        internal_terminals = set(self.get_internal_elms_of_class("ElmTerm"))
        return [pll for pll in all_plls if pll.pbusbar in internal_terminals]

    def get_converters(self) -> list:
        return self.get_internal_elms(
            lambda x: x.GetClassName() in ["ElmGenstat", "ElmPvsys", "ElmVsc"]
        )

    def get_grid_forming_converters(self) -> list:
        return [conv for conv in self.get_converters() if conv.ctrlStruct == 1]

    def get_grid_following_converters(self) -> list:
        return [conv for conv in self.get_converters() if conv.ctrlStruct == 0]

    def is_internal_elm(self, elm: PFGeneral) -> bool:
        class_elm = elm.GetClassName()
        all_elm_of_class = self.get_internal_elms_of_class(class_elm)
        return elm in all_elm_of_class

    def are_internal_elms(self, elms: list[PFGeneral]) -> bool:
        all_elms = self.get_all_internal_elms()
        return set(elms).issubset(all_elms)

    def are_internal_elms_with_same_class(self, elms: list[PFGeneral]) -> bool:
        """Checks whether all network elements in 'elms' (which MUST all be of the same class) are internal elements.

        Args:
            elms (list[PFGeneral]): list of network elements of same class

        Returns:
            bool: True if all elements are included
        """
        class_of_elms = elms[0].GetClassName()
        all_elm_of_class = self.get_internal_elms_of_class(class_of_elms)
        return set(elms).issubset(all_elm_of_class)

    # Load flow
    def load_flow_total_power_exchange_in_MVA(self) -> complex:
        return (
            self._obj.GetAttribute("c:Pinter") + self._obj.GetAttribute("c:Qinter") * 1j
        )

    @abstractmethod
    def get_all_internal_elms(self) -> list[PFGeneral]:
        """Get all internal elements (to be implemented in concrete class)

        Returns:
            list[PFGeneral]: list of all internal elements.
        """
        pass

    @abstractmethod
    def get_all_groupings_of_same_type(self) -> list:
        """Get all calculation relevant groupings of the same type (Zone class returns ElmZone, Area class returns...)

        Returns:
            list: alls groupings of same type
        """
        pass

    @abstractmethod
    def get_all_powfacpy_groupings_of_same_type(self) -> list:
        """Get all calculation relevant groupings of the same type (Zone class returns Zone, Area class returns...)

        Difference to 'get_all_groupings_of_same_type' is that e.g. Zones instead ElmZone are returned

        Returns:
            list: alls groupings of same type
        """
        pass


class AreaZoneBase(GroupingBase):
    """Abstract base class for Areas and Zones. Those classes basically offer the same functionality ibn PF."""

    @property
    def total_power_loads(self) -> complex:
        return self._obj.GetAttribute("c:LoadP") + 1j * self._obj.GetAttribute(
            "c:LoadQ"
        )

    def is_neighbor(self, grouping: AreaOrZone | ElmAreaOrZone) -> bool:
        grouping = self._get_elm_input(grouping)
        interchange_flag = self._obj.CalculateInterchangeTo(grouping)
        if interchange_flag > 0:
            return True
        elif interchange_flag == 0:
            return False
        elif self._obj == grouping:
            raise ValueError(
                f"Potential neighbor is equal to grouping ('{self._obj.loc_name}')"
            )
        else:
            raise PFInvalidLoadFlow()

    def get_neighbors(
        self, groupings: list[AreaZoneBase] | list[ElmAreaOrZone] | None = None
    ) -> list[AreaZoneBase] | list[ElmAreaOrZone]:
        if groupings is None:
            groupings = self.get_all_groupings_of_same_type()
        groupings = [self._get_elm_input(g) for g in groupings]
        return [g for g in groupings if not g == self._obj and self.is_neighbor(g)]

    # Load flow
    def load_flow_power_exchange_with_in_MVA(
        self, grouping: ElmAreaOrZone | AreaOrZone, return_value_no_exchange=np.nan
    ) -> complex:
        """Get load flow apparent power exchange (in MVA) with other grouping.

        Args:
            grouping (ElmAreaOrZone | AreaOrZone): other grouping
            return_value_no_exchange (_type_, optional): return value when there is no connection. Defaults to np.nan.

        Returns:
            complex: load flow apparent power exchange (in MVA) if connected
        """
        grouping = self._get_elm_input(grouping)
        interchange_flag = self._obj.CalculateInterchangeTo(grouping)
        if interchange_flag > 0:
            return self._obj.GetAttribute("c:Pinter") + 1j * self._obj.GetAttribute(
                "c:Qinter"
            )
        elif interchange_flag == 0:
            return return_value_no_exchange
        else:
            raise PFInvalidLoadFlow()

    def load_flow_total_power_loads_in_MVA(self) -> complex:
        try:
            return self._obj.GetAttribute(
                LF.ElmZone.c_TotLoadP.value
            ) + 1j * self._obj.GetAttribute(LF.ElmZone.c_TotLoadQ.value)
        except AttributeError:
            raise PFInvalidLoadFlow()

    def load_flow_total_power_generation_in_MVA(self) -> complex:
        try:
            return self._obj.GetAttribute(
                LF.ElmZone.c_TotgenP.value
            ) + 1j * self._obj.GetAttribute(LF.ElmZone.c_TotgenQ.value)
        except AttributeError:
            raise PFInvalidLoadFlow()

    @abstractmethod
    def _get_elm_input(self, input: AreaOrZone | ElmAreaOrZone) -> ElmAreaOrZone:
        """Handle Zone/Area or ElmZone/ElmAre input and always return ElmZone/ElmArea."""
        pass

    @abstractmethod
    def _get_powfacpy_obj_input(self, input: AreaOrZone | ElmAreaOrZone) -> AreaOrZone:
        """Handle Zone/Area or ElmZone/ElmAre input and always return Zone/Area."""
        pass

    @abstractmethod
    def merge(self, grouping_to_merge: GroupingBase) -> ElmAreaOrZone:
        """Merge another grouping of same type into current grouping. The other grouping is deleted after merging.

        Args:
            grouping_to_merge (GroupingBase): grouping to merge (must be of same type as self)

        Returns:
            ElmAreaOrZone: merged grouping (as ElmArea or ElmZone)
        """
        pass


from powfacpy.pf_classes.elm.zone import Zone
from powfacpy.pf_classes.elm.area import Area

type ElmAreaOrZone = ElmArea | ElmZone
type AreaOrZone = Area | Zone
