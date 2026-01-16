from __future__ import annotations


from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import PFGeneral, BlkSlot, ElmComp, ElmDsl

from powfacpy.pf_classes.elm.elm_base import ElmBase
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
