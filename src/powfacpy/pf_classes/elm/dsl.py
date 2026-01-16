from __future__ import annotations

from icecream import ic

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import PFGeneral, BlkSlot, ElmDsl

from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.result_variables import ResVar
from powfacpy.applications.plots import Plots
from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.blk.definition import BlockDefinition


class DSLModel(ElmBase):

    __slots__ = ()

    def __init__(self, obj: ElmDsl) -> None:
        super().__init__(obj)
        self._obj: ElmDsl

    def add_results_signals(self, signal_names: list[str]) -> None:
        """Add signals to monitored variables.

        Args:
            signal_names (list[str]): names of signals (without 's:')
        """
        act_prj = ActiveProjectCached()
        signal_names = [f"s:{sig}" for sig in signal_names]
        act_prj.add_results_variable(self._obj, signal_names)

    def add_results_signal_type(self, signal_types: list[str]) -> None:
        """TODO explain

        Args:
            signal_types (list[str]): _description_

        Returns:
            _type_: _description_
        """
        act_prj = ActiveProjectCached()
        blkdef = BlockDefinition(self._obj.typ_id)
        signal_mapping = blkdef.get_signal_type_name_mapping()
        for n, sig_type in enumerate(signal_types):
            sig_type_map = signal_mapping.get(sig_type)
            if sig_type_map:
                signal_types[n] = sig_type_map
        signals = [
            f"s:{sig}" for sig_type in signal_types for sig in getattr(blkdef, sig_type)
        ]
        act_prj.add_results_variable(self._obj, signals)
        return signals
