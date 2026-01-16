from __future__ import annotations
from typing import Any, Callable

from numpy import diff
from icecream import ic

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.base.base import BaseChildStatic
from powfacpy.pf_classes.protocols import BlkSlot


class Slot(BaseChildStatic):

    def __init__(self, obj: BlkSlot) -> None:
        super().__init__(obj)

    @property
    def name(self) -> str:
        return self._obj.loc_name

    @property
    def output_signals(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sOutput")

    @property
    def input_signals(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sInput")

    @property
    def upper_limitation_input(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sUpLimInp")

    @property
    def lower_limitation_input(self) -> list[str]:
        return self.read_attribute_that_is_string_in_list("sLowLimInp")

    def read_attribute_that_is_string_in_list(self, attr: str) -> list[str]:
        """Read attributes that are returned by PF in inconvenient format as a string (with comma separation) in a list (e.g. '[s1, s2, s3]'). Return a list with all values as items instead (e.g. [s1, s2, s3]).

        Args:
            attr (str): attribute name

        Returns:
            list[str]: list with all values as items
        """
        val = getattr(self._obj, attr)
        if val:
            return val[0].replace(";", ",").split(",")
        else:
            return []

    def get_signal_type_name_mapping(self) -> dict[str, str]:
        return {
            "sOutput": "output_signals",
            "sInput": "input_signals",
            "sUpLimInp": "upper_limitation_input",
            "sLowLimInp": "lower_limitation_input",
        }

    def get_signal_type(self, signal_types: list[str]) -> None:
        """TODO explain

        Args:
            signal_types (list[str]): _description_

        Returns:
            _type_: _description_
        """
        signal_mapping = self.get_signal_type_name_mapping()
        for n, sig_type in enumerate(signal_types):
            sig_type_map = signal_mapping.get(sig_type)
            if sig_type_map:
                signal_types[n] = sig_type_map
        signals = [
            f"s:{sig}" for sig_type in signal_types for sig in getattr(self, sig_type)
        ]
        return signals
