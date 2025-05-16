from abc import ABC, abstractmethod
from typing import Callable

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import PFGeneral, ElmRes, StaPll


class GroupingBase(ABC):
    """Base class for groupings (ElmZone, ElmArea, ElmBoundary). Provides a common interface (e.g. to get internal elements)."""

    __slots__ = ()

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

    def get_phase_locked_loops(self) -> list[StaPll]:
        """Get all internal phase-locked loops (StaPll) objects (i.e. PLLs that measure at internal terminals).

        Returns:
            list[StaPll]: List of internal PLLs.
        """
        act_prj = ActiveProjectCached()
        all_plls: list[StaPll] = act_prj.get_calc_relevant_obj("*.StaPll")
        internal_terminals = set(self.get_internal_elms_of_class("ElmTerm"))
        return [pll for pll in all_plls if pll.pbusbar in internal_terminals]

    @abstractmethod
    def get_all_internal_elms(self) -> list[PFGeneral]:
        """Get all internal elements (to be implemented in concrete class)

        Returns:
            list[PFGeneral]: list of all internal elements.
        """
        pass
