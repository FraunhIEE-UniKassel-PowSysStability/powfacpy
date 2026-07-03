"""
The name 'def' is not allowed for python modules, so the module is named 'definition'.
"""

from __future__ import annotations
from typing import Any, Callable
import re
import math

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
    def internal_variables(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sIntern")

    @property
    def upper_limitation_signals(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sUpLimInp")

    @property
    def lower_limitation_signals(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sLowLimInp")

    @property
    def upper_limitation_parameters(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sUpLimPar")

    @property
    def lower_limitation_parameters(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sLowLimPar")

    @property
    def additional_equations(self) -> list[str]:
        return "\n".join(self._obj.sAddEquat)

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
        """Get default information of BlockDefinition in a dictionary:

        - attributes defined in method 'get_attr_property_mapping' (e.g. "Name",
            "Title", "Output signals", "Input signals", "States",           "Parameters", "Upper limitation parameters", "Lower limitation parameters", "Equations")
        - 'Subblocks': blockdefs of subblocks
        - 'Grafic': Graphical object (if exists)
        - 'BlkDef': Block definition (BlkDef)
        - 'BlockDefinition': BlockDefinition object (self)
        - 'Name mapping': mapping of names of parameters and states between block references and their block definitions

        Returns:
            dict: dict with default information. 
        """
        attr_info = self.get_attribute_info()
        attr_info["Subblocks"] = self.get_blkdefs_of_subblocks()
        graphic = self._obj.GetContents("*.IntGrfnet")
        if graphic:
            attr_info["Grafic"] = graphic
        attr_info["BlkDef"] = self._obj
        attr_info["BlockDefinition"] = self
        attr_info["Name mapping"] = self.get_names_mapping_of_blkdefs_and_blkrefs()
        return attr_info

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
            "Equations": "additional_equations",
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

    def get_names_mapping_of_blkdefs_and_blkrefs(self) -> dict:
        """Get mapping of names of parameters and states between block references and their block definitions. 
        
        The parameter and state names can differ (e.g. when the same name occurs in several block references inside a block definition - assume several references have a state named 'x', those names need to differ on the level of the block definition(x, x1, x2,...)).

        Args:
            blkrefs_blkdefs_dict (dict[BlkRef, BlkDef]): dict with blkrefs as keys and respective blkdefs as values.

        Returns:
            dict: blkrefs as keys and name mapping (tuples) as values
        """
        mapping = {}
        mapped_attr = ["sParams", "sStates", "sUpLimPar", "sLowLimPar", "sIntern"]
        blkrefs_blkdefs_dict = self.get_blkdefs_of_subblocks()
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
    
    def get_signal_results_variables(self, signal_types: list[str] | None = None) -> list[str]:
        """Get names of results variables for signals (e.g. 's:varname') of the block definition. 

        Args:
            signal_types (list[str]): e.g. ["input_signals", "output_signals", "states", "internal_variables""upper_limitation_signals", 
            "lower_limitation_signals"]). If None, all internal signals are monitored. Defaults to None.

        Returns:
            list[str]: _description_
        """
        if signal_types is None:
            signal_types = [
                "input_signals",
                "output_signals",
                "states",
                "internal_variables",
                "upper_limitation_signals",
                "lower_limitation_signals"
            ]
        signal_results_variables = []   
        for signal_type in signal_types:
            signale = getattr(self, signal_type)
            if not signal_type == "internal_variables":
                signal_results_variables += [
                        f"s:{sig}" for sig in signale
                    ]
            else:
                signal_results_variables += [
                        f"c:{sig}" for sig in signale
                    ] 
        return signal_results_variables
    
    def get_info_incl_subblocks(self, all_blkdef_info: dict | None = None, parent: None | BlkDef = None):
        """
        Recursive
        """
        if all_blkdef_info is None:
            all_blkdef_info = {
                "blkdefs_without_subblocks": [], # non-graphical (macros)
                "blkdefs_with_subblocks": [], # graphical
            }
        info = self.get_info()
        if parent is not None:
            info["Parent"] = parent
        if info["Subblocks"]:
            all_blkdef_info["blkdefs_with_subblocks"].append(info)
            for blkdef in info["Subblocks"].values():
                blkdef = BlockDefinition(blkdef)
                all_blkdef_info = blkdef.get_info_incl_subblocks(all_blkdef_info=all_blkdef_info, parent=self._obj)   
        else: # lowest level reached
            blkdef_in_list = [blkdef_info for blkdef_info in all_blkdef_info["blkdefs_without_subblocks"] if blkdef_info["BlkDef"] == self._obj]
            if not blkdef_in_list:
                all_blkdef_info["blkdefs_without_subblocks"].append(info)     
        return all_blkdef_info

    def get_parameter_limits_from_equations(self, exclusive_limit_distance: float = 0) -> dict:
        equations = self._obj.sAddEquat
        param_limits = {}
        for line in equations:
            if line.startswith("limfix"):
                parlim = parse_limfix(line, exclusive_limit_distance)
                param_limits[parlim["param"]] = parlim["limits"]
        return param_limits        

def parse_limfix(s: str, exclusive_limit_distance: float = 0) -> dict:
    # Truncate comment
    s = s.split("!")[0]

    # Extract parameter name
    param = re.search(r'limfix\((\w+)\)', s).group(1)
    
    # Extract the range string, e.g. "(0,)", "[0,10]", "(,-5)"
    range_str = re.search(r'=\s*(.+)', s).group(1).strip()
    
    # Determine bracket types
    lower_inclusive = range_str[0] == '['
    upper_inclusive = range_str[-1] == ']'
    
    # Extract lower and upper values
    inner = range_str[1:-1]  # strip brackets
    parts = inner.split(',')
    lower_str = parts[0].strip()
    upper_str = parts[1].strip()
    
    # Parse lower limit
    if lower_str == '':
        lower = -math.inf
    else:
        lower = float(lower_str)
        if not lower_inclusive:
            lower += exclusive_limit_distance

    # Parse upper limit
    if upper_str == '':
        upper = math.inf
    else:
        upper = float(upper_str)
        if not upper_inclusive:
            upper -= exclusive_limit_distance

    return {"param": param, "limits": (lower, upper)}                
