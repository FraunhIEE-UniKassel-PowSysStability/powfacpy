from __future__ import annotations
from textwrap import indent


import numpy as np
from icecream import ic

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import PFGeneral, BlkSlot, ElmDsl

from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.blk.definition import BlockDefinition
from powfacpy.engineering_helpers import get_weighted_average


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

    def add_results_signal_type(self, signal_types: list[str]) -> list[str]:
        """Add all signals of a certain type to monitored result variables

        Args:
            signal_types (list[str]): signal types according to block definition
             (for example "sOutput", "sInput", "sStates", "sParams", "sUpLimPar", "sLowLimPar")

        Returns:
            list[str]: list of signals that were added to the monitored result variables.
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

    def get_parameters(self) -> dict:
        """Get model parameter (keys) and value (values) dict of DSL model.

        Returns:
            dict: parameter-value dict
        """
        return {
            k: v
            for k, v in zip(self.get_parameter_names(), self.get_parameter_values())
        }

    def get_parameter_names(self) -> list[str]:
        return self._obj.parameterNames.split(",")

    def get_parameter_values(self) -> list:
        return self._obj.params


def get_parameters_of_dsl_models(
    dsl_models: list[ElmDsl] | list[DSLModel], parameter_names: list[str] | None = None
) -> dict:
    """Get a dict with parameter names (keys) and a list of values (values) of the DSL models in 'dsl_models' (these models must have the same parameters, i.e. reference the same block definition).

    Args:
        dsl_models (list[ElmDsl] | list[DSLModel]): list of ElmDsl or DSLModels which must have the same parameters.
        parameter_names (list[str] | None): list of parameter names. If None, all parameters considered. Defaults to None.

    Returns:
        dict: parameter (keys) and list of values (values) dict
    """
    if not isinstance(dsl_models[0], DSLModel):
        dsl_models = [DSLModel(elmdsl) for elmdsl in dsl_models]
    if parameter_names is None:
        parameter_names = dsl_models[0].get_parameter_names()
    params = {name: np.empty(len(dsl_models)) for name in parameter_names}
    for n, dsl_model in enumerate(dsl_models):
        for name in params.keys():
            params[name][n] = dsl_model._obj.__getattr__(name)
    return params


def get_average_parameter_values_of_dsl_models(
    dsl_models: list[ElmDsl] | list[DSLModel],
    parameter_names: list[str] | None = None,
    weights: list[float] | None = None,
) -> dict:
    """Get the average value of the parameters of DSL models (these models must have the same parameters, i.e. reference the same block definition).

    Args:
        dsl_models (list[ElmDsl] | list[DSLModel]): list of ElmDsl or DSLModels which must have the same parameters.
        parameter_names (list[str] | None): list of parameter names. If None, all parameters considered. Defaults to None.
    Returns:
        dict: dict with parameter names (keys) and average value (values)
    """
    params = get_parameters_of_dsl_models(dsl_models, parameter_names=parameter_names)
    if weights is not None:
        params = {
            par: get_weighted_average(values, weights) for par, values in params.items()
        }
    else:
        params = {par: np.mean(values) for par, values in params.items()}
    return params


from powfacpy.pf_classes.class_conversion import convert_pf_obj_to_powfacpy


def get_dsl_models_info_sorted_by_block_definition(
    dsl_models: list[ElmDsl] | list[DSLModel],
    parent_elms: list[PFGeneral] | None = None,
    average: str | None = None,
) -> dict:
    """Get a dict with the block definitions of `dsl_models` as keys and further information about the `dsl_models` as values.

    The information are the dsl objects of the block definitions (keys: 'dsl_models'), their parameter values (keys: 'parameters') and, if `parent_elms` is not None, the parent elements of the dsl models (keys: 'parent_elms'). If `average` is not None, also the (weighted) average parameter values of the dsl models are calculated and added to the information (keys: 'average').

    The information is relevant for example to create dynamic equivalents of subsystems where simplified and averaged dynamic models are needed.

    Args:
        dsl_models (list[ElmDsl] | list[DSLModel]): list of ElmDsl or DSLModels.
        parent_elms (list[PFGeneral] | None, optional): List of parent network elements of the 'dsl_models' (e.g. synchronous machines (ElmSym)). Defaults to None.
        average (str | None, optional): Type of average to calculate ('not_weighted', 'apparent_power_weighted': weighted by apparent power of 'parent_elms'). Defaults to None.

    Returns:
        dict: Dict with block definitions as keys and further information about the `dsl_models` as values.

    Example:
        ```python
        dsl_models_info = get_dsl_models_info_sorted_by_block_definition(
            governor_dsl_models,
            synchronous_machines,
            average='apparent_power_weighted',
        )

        ```
    """
    if not isinstance(dsl_models[0], DSLModel):
        dsl_models = [DSLModel(m) for m in dsl_models if m]
    dsl_models_info = {}
    for n, dsl_model in enumerate(dsl_models):
        blkdef = dsl_model.typ_id
        blkdef_info = dsl_models_info.get(blkdef)
        if not blkdef_info:
            dsl_models_info[blkdef] = {}
            parameter_names = dsl_model.get_parameter_names()
            dsl_models_info[blkdef]["dsl_models"] = []
            dsl_models_info[blkdef]["parameters"] = {
                name: [] for name in parameter_names
            }
            if parent_elms is not None:
                dsl_models_info[blkdef]["parent_elms"] = []
        dsl_models_info[blkdef]["dsl_models"].append(dsl_model)
        parameter_values = dsl_model.get_parameter_values()
        for k, par in enumerate(parameter_names):
            dsl_models_info[blkdef]["parameters"][par].append(parameter_values[k])
        if parent_elms is not None:
            dsl_models_info[blkdef]["parent_elms"].append(parent_elms[n])
    if average is not None:
        for blkdef, info in dsl_models_info.items():
            info["average"] = {p: float for p in info["parameters"]}
            if average == "not_weighted":
                for par, values in info["parameters"].items():
                    info["average"][par] = np.mean(values)
            if average == "apparent_power_weighted":
                weights = [
                    convert_pf_obj_to_powfacpy(elm).rated_apparent_power
                    for elm in info["parent_elms"]
                ]
                for par, values in info["parameters"].items():
                    info["average"][par] = get_weighted_average(values, weights)
    return dsl_models_info


def display_dsl_models_info(dsl_models_info: dict, indent="   ") -> None:
    """Display the information about DSL models sorted by block definition (see `get_dsl_models_info_sorted_by_block_definition`) in a readable way.

    Args:
        dsl_models_info (dict): dict with block definitions as keys and further information about the `dsl_models` as values. Output of `get_dsl_models_info_sorted_by_block_definition()`.
    """
    for blkdef, info in dsl_models_info.items():
        print(f"Block Definition '{blkdef.loc_name}': {blkdef}")
        if "parent_elms" in info:
            print(f"{indent}Parent elements:")
            for elm in info["parent_elms"]:
                print(f"{2*indent}{elm.loc_name} of class {elm.GetClassName()} ({elm})")
        print(f"{indent}Parameter values:")
        for par, values in info["parameters"].items():
            print(f"{2*indent}{par}: {values}")
        if "average" in info:
            print(f"{indent}Average parameter values:")
            for par, value in info["average"].items():
                print(f"{2*indent}{par}: {value}")
        print("\n")
