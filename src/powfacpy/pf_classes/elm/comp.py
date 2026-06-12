from __future__ import annotations

from icecream import ic

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import PFGeneral, BlkSlot, ElmComp, ElmDsl
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.pf_classes.blk.slot import Slot
from powfacpy.pf_classes.blk.definition import BlockDefinition
from powfacpy.result_variables import ResVar
from powfacpy.applications.plots import Plots
from powfacpy.base.active_project import ActiveProjectCached


class CompositeModel(ElmBase):

    __slots__ = ()

    def __init__(self, obj: ElmComp) -> None:
        super().__init__(obj)
        self._obj: ElmComp

    def get_slots(self) -> list[BlkSlot]:
        return self._obj.pblk

    def get_network_elms(self) -> list[PFGeneral]:
        return self._obj.pelm

    def get_slots_and_network_elms_dict(
        self, include_empty_slots: bool = True
    ) -> dict[BlkSlot, PFGeneral]:
        """Get all slots and respective network elements.

        Args:
            include_empty_slots (bool, optional): If true, slots without network elements are included. Defaults to True.

        Returns:
            dict[BlkSlot, PFGeneral]: slots (keys) and respective network elements (values)
        """
        if include_empty_slots:
            return {
                slot: net_elm
                for slot, net_elm in zip(self.get_slots(), self.get_network_elms())
            }
        else:
            return {
                slot: net_elm
                for slot, net_elm in zip(self.get_slots(), self.get_network_elms())
                if net_elm
            }

    def export_block_diagram(
        self, target_dir: str = ".\\", file_name: str = "", format: str = "svg"
    ) -> tuple[str, int]:
        """Export the block diagram.

        Args:
            target_dir (str, optional): target directory. Defaults to ".\".
            file_name (str, optional): File name. Defaults to "".
            format (str, optional): _description_. Defaults to "svg".

        Returns:
            tuple[str, int]: The path of the exported graphic and returned value of the PF 'comwr' object (0: successful export, 1: not successful)
        """
        if not file_name:
            file_name = f"Composite model {self._obj.loc_name}"
        pfplt = Plots(cached=True)
        act_prj = ActiveProjectCached()
        grp = act_prj.get_unique_obj("*.IntGrfnet", parent_folder=self._obj.typ_id)
        grp.Show()
        pfplt.set_shown_page_as_active_page()
        path = target_dir + "\\" + file_name
        return pfplt.export_active_page(format=format, path=path)

    def get_dsl_models_in_slots(self) -> list[ElmDsl]:
        """Get all network elements in the slots that are of class 'ElmDsl'"""
        return [
            obj
            for obj in self.get_network_elms()
            if obj is not None and obj.GetClassName() == "ElmDsl"
        ]

    def show_block_diagram(self) -> None:
        """Show the graphic of the composite model"""
        act_prj = ActiveProjectCached()
        grp = act_prj.get_unique_obj("*.IntGrfnet", parent_folder=self._obj.typ_id)
        grp.Show()

    def monitor_signals_of_slots(self, signal_types: list[str] | None = None, create_plots: bool = False) -> None:
        """Monitor signals of the network elements in the slots. Only signals of the specified types are monitored.

        Args:
            signal_types (list[str]): signal types to monitor (e.g. ["sInput", "sOutput", "sUpLimInp", "sLowLimInp"])
            create_plots (bool): If True, plots are created for the signals of each slot. Defaults to False.
        """
        if signal_types is None:
            signal_types = ["sInput", "sOutput", "sUpLimInp", "sLowLimInp"]
        pfplt = Plots(cached=True)
        act_prj = ActiveProjectCached()
        for slot, net_elm in self.get_slots_and_network_elms_dict(
            include_empty_slots=False
        ).items():
            slot = Slot(slot)
            result_signals = slot.get_signal_type(signal_types) 
            act_prj.add_results_variable(slot._obj, result_signals)
            if create_plots:
                pfplt.set_active_plot(net_elm.loc_name, "§ " + net_elm.loc_name)
                pfplt.plot(net_elm, result_signals)

    def monitor_signals_of_dsl_models(self, signal_types: list[str] | None = None, create_plots: bool = False) -> None:
        """Monitor internals of the network elements in the slots that are of class 'ElmDsl'.

        Args:
            signals (list[str]): Internal signals to monitor (e.g. ["input_signals", "output_signals", "states", "internal_variables","upper_limitation_signals", 
            "lower_limitation_signals"]). If None, all signals are monitored. Defaults to None.
            create_plots (bool): If True, plots are created for the signals of each 'ElmDsl' model. Defaults to False.
        """
        if signal_types is None:
            signal_types = ["input_signals", "output_signals", "states", "internal_variables", "upper_limitation_signals", "lower_limitation_signals"]
        pfplt = Plots(cached=True)
        act_prj = ActiveProjectCached()
        for slot, net_elm in self.get_slots_and_network_elms_dict(
            include_empty_slots=False
        ).items():
            if net_elm.GetClassName() == "ElmDsl":
                blkdef = BlockDefinition(net_elm.typ_id)
                result_variables = blkdef.get_signal_results_variables(signal_types)  
                act_prj.add_results_variable(net_elm, result_variables)
                if create_plots:
                    pfplt.set_active_plot(net_elm.loc_name, "§ " + net_elm.loc_name)
                    pfplt.plot(net_elm, result_variables)


            
