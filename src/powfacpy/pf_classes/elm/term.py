from __future__ import annotations

from typing import Callable

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import ElmTerm, PFGeneral, StaCubic, StaPll

from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.pf_classes.elm.grouping_base import GroupingBase
from powfacpy.result_variables import ResVar

RMS_BAL = ResVar.RMS_Bal


class Terminal(ElmBase):

    __slots__ = ()

    def __init__(self, obj: ElmTerm) -> None:
        super().__init__(obj)
        self._obj: ElmTerm

    def __new__(cls, *args, **kwargs) -> ElmTerm | Terminal:
        """Implemented only to add type hints for the created instance.

        Returns:
            ElmTerm | Terminal: New instance
        """
        instance = super().__new__(cls)
        return instance

    def get_cubicle_of_connected_elm(self, elm: PFGeneral) -> StaCubic:
        for cub in self._obj.GetConnectedCubicles():
            if cub.GetBranch() == elm:
                return cub

    def get_connected_elements(
        self, only_calc_relevant: bool = False, condition: Callable | None = None
    ) -> list[PFGeneral]:
        """Get all elements connected to terminal.

        Args:
            only_calc_relevant (bool, optional): Only calculation relevant elements are considered. Defaults to False.
            condition (Callable | None, optional): Condition to select elements. Defaults to None.

        Returns:
            list[PFGeneral]: Connected elements
        """
        if only_calc_relevant:
            cubs = self._obj.GetCalcRelevantCubicles()
        else:
            cubs = self._obj.GetConnectedCubicles()
        if condition is None:
            return [cub.obj_id for cub in cubs]
        else:
            return [cub.obj_id for cub in cubs if condition(cub.obj_id)]

    def add_phase_locked_loop(
        self,
        folder: PFGeneral | None = None,
        monitor_frequency_pu: bool = False,
        monitor_frequency_Hz: bool = False,
    ) -> StaPll:
        """Add a PLL to monitor the frequency.

        Args:
            folder (PFGeneral | None, optional): parent folder. Defaults to None (parent grid folder is used).
            monitor_frequency_pu (bool, optional): monitor frequency in pu. Defaults to False.
            monitor_frequency_Hz (bool, optional): monitor frequency in Hz. Defaults to False.

        Returns:
            StaPll: Created PLL object
        """
        act_prj = ActiveProjectCached()
        if not folder:
            parent_grid = act_prj.get_upstream_obj(
                self._obj, lambda x: x.GetClassName() == "ElmNet"
            )
            folder = act_prj.create_in_folder(
                "Phase locked loops.IntFolder",
                folder=parent_grid,
                overwrite=False,
                use_existing=True,
            )
        pll: StaPll = act_prj.create_in_folder(
            "PLL at " + self._obj.loc_name + ".StaPll", folder=folder
        )
        pll.pbusbar = self._obj
        if monitor_frequency_Hz:
            act_prj.add_results_variable(pll, "s:Fmeas")
        if monitor_frequency_pu:
            act_prj.add_results_variable(pll, "s:fmeas")
        return pll
