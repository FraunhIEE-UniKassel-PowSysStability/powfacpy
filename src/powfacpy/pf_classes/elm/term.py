from __future__ import annotations

from typing import Callable

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import ElmTerm, PFGeneral, StaPll

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

    def add_phase_locked_loop(
        self,
        folder: PFGeneral | None = None,
        monitor_frequency_pu: bool = False,
        monitor_frequency_Hz: bool = False,
    ) -> StaPll:
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
