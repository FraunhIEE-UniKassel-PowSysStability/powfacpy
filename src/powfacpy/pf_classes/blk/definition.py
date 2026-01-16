"""
The name 'def' is not allowed for python modules, so the module is named 'definition'.
"""

from __future__ import annotations
from typing import Any, Callable

from numpy import diff
from icecream import ic

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.base.base import BaseChildStatic
from powfacpy.pf_classes.protocols import BlkDef, BlkRef
from powfacpy.applications.plots import Plots


class BlockDefinition(BaseChildStatic):

    def __init__(self, obj: BlkDef) -> None:
        super().__init__(obj)

    @property
    def name(self) -> str:
        return self._obj.loc_name

    @property
    def title(self) -> str:
        return self._obj.sTitle

    @property
    def output_signals(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sOutput")

    @property
    def input_signals(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sInput")

    @property
    def states(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sStates")

    @property
    def parameters(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sParams")

    @property
    def upper_limitation_parameters(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sUpLimPar")

    @property
    def lower_limitation_parameters(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sLowLimPar")

    @property
    def equations(self) -> list[str]:
        return "\n\n".join(self._obj.sAddEquat)

    def read_attribute_that_is_string_in_list(self, attr: str) -> list[str]:
        """PF returns some attribute values as strings (with commas as separators). Use this method to get the values as a list of strings.

        Args:
            attr (str): attribute name

        Returns:
            list[str]: values as a list of strings
        """
        val = getattr(self._obj, attr)
        if val:
            return val[0].split(",")
        else:
            return []

    def get_info(self) -> dict:
        """Get default information:
        - attributes defined in method 'get_attr_property_mapping'
        - blockdefs of subblocks
        - Further attributes (see method body)

        Returns:
            dict: dict with default information.
        """
        attr_info = self.get_attribute_info()
        subblock_info = self.get_blkdefs_of_subblocks(
            macros_and_graphical_separately=True
        )
        graphic = self._obj.GetContents("*.IntGrfnet")
        if graphic:
            attr_info["Grafic"] = graphic
        attr_info["BlkDef"] = self._obj
        attr_info["BlockDefinition"] = self
        attr_info["Mappings"] = self.get_mapping(
            subblock_info["Macros"] | subblock_info["Graphical"]
        )
        return attr_info | subblock_info

    def get_attribute_info(self) -> dict[str, Any]:
        """Get attribute values for attributes defined in 'get_attr_property_mapping'.

        Returns:
            dict[str, Any]: _description_
        """
        return {
            attr: getattr(self, prop)
            for attr, prop in self.get_attr_property_mapping().items()
        }

    def get_blkrefs(self) -> list[BlkRef]:
        return self._obj.GetContents("*.BlkRef")

    def get_blkdefs_of_subblocks(
        self, macros_and_graphical_separately: bool = False
    ) -> dict:
        """Get block definitions of subblocks.

        Args:
            macros_and_graphical_separately (bool, optional): If true, blockdefs that are macros and blockdefs that are graphical models are returned separately. Defaults to False.

        Returns:
            dict: dict with block references as keys and blockdefs as values or, if 'macros_and_graphical_separately' is true, a dict with keys 'Macros' and 'Graphical' and according values is returned.
        """
        act_prj = ActiveProjectCached()
        if not macros_and_graphical_separately:
            return {blkref: blkref.typ_id for blkref in self.get_blkrefs()}
        else:
            defs = {model_type: {} for model_type in ["Macros", "Graphical"]}
            for blkref in self.get_blkrefs():
                graphic_of_blkdef = act_prj.get_unique_obj(
                    "*.IntGrfnet",
                    parent_folder=blkref.typ_id,
                    error_if_non_existent=False,
                )
                if graphic_of_blkdef is not None:
                    defs["Graphical"][blkref] = blkref.typ_id
                else:
                    defs["Macros"][blkref] = blkref.typ_id
            return defs

    def get_attr_property_mapping(self) -> dict[str, Callable]:
        return {
            "Name": "name",
            "Title": "title",
            "Output signals": "output_signals",
            "Input signals": "input_signals",
            "States": "states",
            "Parameters": "parameters",
            "Upper limitation parameters": "upper_limitation_parameters",
            "Lower limitation parameters": "lower_limitation_parameters",
            "Equations": "equations",
        }

    def export_block_diagram(
        self, target_dir: str = ".\\", file_name: str = "", format: str = "svg"
    ) -> tuple[str, int]:
        """Export grapic of block diagram.

        Args:
            target_dir (str, optional): Target directory. Defaults to ".\".
            file_name (str, optional): file name. Defaults to "".
            format (str, optional): graphic format. Defaults to "svg".

        Returns:
            tuple[str, int]: _description_
        """
        if not file_name:
            file_name = f"{self._obj.loc_name}"
        pfplt = Plots(cached=True)
        act_prj = ActiveProjectCached()
        grp = act_prj.get_unique_obj("*.IntGrfnet", parent_folder=self._obj)
        grp.Show()
        pfplt.set_shown_page_as_active_page()
        path = target_dir + "\\" + file_name
        return pfplt.export_active_page(format=format, path=path)

    def get_mapping(self, blkrefs_blkdefs_dict: dict[BlkRef, BlkDef]) -> dict:
        """Get mapping of parameter and state names between block references and block definitions. The parameter and state names can differ (e.g. when the same name occurs in several block references of a block definition).

        Args:
            blkrefs_blkdefs_dict (dict[BlkRef, BlkDef]): dict with blkrefs as keys and respective blkdefs as values.

        Returns:
            dict: blkrefs as keys and name mapping (tuples) as values
        """
        mapping = {}
        mapped_attr = ["sParams", "sStates"]
        for blkref, blkdef in blkrefs_blkdefs_dict.items():
            difference_found = False
            mapping[blkref] = {attr: [] for attr in mapped_attr}
            for attr in mapped_attr:
                blkref_attrs = getattr(blkref, attr)
                if not blkref_attrs:
                    continue

                for blkref_par, blkdef_par in zip(
                    blkref_attrs[0].split(","), getattr(blkdef, attr)[0].split(",")
                ):
                    if not blkref_par == blkdef_par:
                        mapping[blkref][attr].append((blkref_par, blkdef_par))
                        difference_found = True
            if not difference_found:
                del mapping[blkref]
        return mapping

    def get_signal_type_name_mapping(self) -> dict[str, str]:
        return {
            "sOutput": "output_signals",
            "sInput": "input_signals",
            "sStates": "states",
            "sParams": "parameters",
            "sUpLimPar": "upper_limitation_parameters",
            "sLowLimPar": "lower_limitation_parameters",
        }
