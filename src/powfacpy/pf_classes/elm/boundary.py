from __future__ import annotations

from typing import Callable

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.applications.results import Results
from powfacpy.pf_classes.protocols import ElmBoundary, PFGeneral
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.pf_classes.elm.grouping_base import GroupingBase
from powfacpy.pf_classes.set.colscheme import DiagramColorScheme
from powfacpy.result_variables import ResVar

RMS_BAL = ResVar.RMS_Bal


class Boundary(ElmBase, GroupingBase):

    __slots__ = ()

    def __init__(self, obj: ElmBoundary) -> None:
        super().__init__(obj)
        self._obj: ElmBoundary

    def __new__(cls, *args, **kwargs) -> ElmBoundary | Boundary:
        """Implemented only to add type hints for the created instance.

        Returns:
            ElmBoundary | Boundary: New instance
        """
        instance = super().__new__(cls)
        return instance

    def get_all_internal_elms(
        self,
    ) -> list[PFGeneral]:
        return self._obj.GetInterior()

    def exclude_node_elms_by_condition(self, condition: Callable) -> list[PFGeneral]:
        """Exclude elements from the interior of the boundary by adding their cubicle to the boundary.

        Args:
            condition (Callable): Condition to select the elements to be excluded among all interior elements (e.g. `lambda x: x.GetClassName() == "ElmLod" to exclude all ElmLod)

        Returns:
            list[PFGeneral]: Elements that were excluded
        """
        act_prj = ActiveProjectCached()
        excluded_elms = act_prj.get_by_condition(self._obj.GetInterior(), condition)
        for elm in excluded_elms:
            self._obj.AddCubicle(elm.GetCubicle(0), 1)
        return excluded_elms

    def get_average_frequency(
        self,
        simulation_results: pd.DataFrame,
        source: str = "terminals",
        ignored_elms: list[PFGeneral] | None = None,
    ) -> float:
        """Get the average frequency inside the boundary.

        Args:
            simulation_results (pd.DataFrame): Simulation results (exported using the 'Results' interface)
            source (str, optional): Frequency measurement source. Options:
                - 'terminal' (ElmTerm, default)
                - 'pll' (StaPll)
                - 'sm' (ElmSym)
            ignored_elms (list[PFGeneral] | None, optional): sources (e.g. ElmTerm/StaPll objects) that are not included. Defaults to None.

        Returns:
            float: Average frequency
        """

        def remove_ignored(elms: list):
            if ignored_elms:
                return [elm for elm in elms if not elm in ignored_elms]
            else:
                return elms

        pfres = Results(cached=True)
        if source == "pll":
            plls_in_boundary = remove_ignored(self.get_phase_locked_loops())
            return pfres.get_simulation_results_from_dataframe(
                simulation_results, plls_in_boundary, "s:fmeas"
            ).mean(1)
        elif source == "sm":
            synchronous_machines_in_boundary = remove_ignored(
                self.get_internal_elms(lambda x: x.GetClassName() == "ElmSym")
            )
            return pfres.get_simulation_results_from_dataframe(
                simulation_results,
                synchronous_machines_in_boundary,
                RMS_BAL.ElmSym.s_xspeed.value,
            ).mean(1)
        elif source == "terminal":
            terminals_in_boundary = remove_ignored(
                self.get_internal_elms(lambda x: x.GetClassName() == "ElmTerm")
            )
            return pfres.get_simulation_results_from_dataframe(
                simulation_results, terminals_in_boundary, RMS_BAL.ElmTerm.m_fe.value
            ).mean(1)

    @staticmethod
    def show_boundary_interior_regions_in_network_graphic() -> None:
        """Shows interior regions of all boundaries in the single line diagram."""
        act_prj = ActiveProjectCached()
        setcolscheme = act_prj.get_diagram_color_scheme()
        DiagramColorScheme(setcolscheme).show_boundary_interior_regions()

    @staticmethod
    def get_P_exchange_res_var_rms_bal() -> str:
        return RMS_BAL.ElmZone.c_Pinter.value

    @staticmethod
    def get_Q_exchange_res_var_rms_bal() -> str:
        return RMS_BAL.ElmZone.c_Qinter.value
