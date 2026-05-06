Module powfacpy.pf_classes.elm.dsl
==================================

Functions
---------

`display_dsl_models_info(dsl_models_info: dict, indent='   ') ‑> None`
:   Display the information about DSL models sorted by block definition (see `get_dsl_models_info_sorted_by_block_definition`) in a readable way.
    
    Args:
        dsl_models_info (dict): dict with block definitions as keys and further information about the `dsl_models` as values. Output of `get_dsl_models_info_sorted_by_block_definition()`.

`get_average_parameter_values_of_dsl_models(dsl_models: list[ElmDsl] | list[DSLModel], parameter_names: list[str] | None = None, weights: list[float] | None = None) ‑> dict`
:   Get the average value of the parameters of DSL models (these models must have the same parameters, i.e. reference the same block definition).
    
    Args:
        dsl_models (list[ElmDsl] | list[DSLModel]): list of ElmDsl or DSLModels which must have the same parameters.
        parameter_names (list[str] | None): list of parameter names. If None, all parameters considered. Defaults to None.
    Returns:
        dict: dict with parameter names (keys) and average value (values)

`get_dsl_models_info_sorted_by_block_definition(dsl_models: list[ElmDsl] | list[DSLModel], parent_elms: list[PFGeneral] | None = None, average: str | None = None) ‑> dict`
:   Get a dict with the block definitions of `dsl_models` as keys and further information about the `dsl_models` as values.
    
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

`get_parameters_of_dsl_models(dsl_models: list[ElmDsl] | list[DSLModel], parameter_names: list[str] | None = None) ‑> dict`
:   Get a dict with parameter names (keys) and a list of values (values) of the DSL models in 'dsl_models' (these models must have the same parameters, i.e. reference the same block definition).
    
    Args:
        dsl_models (list[ElmDsl] | list[DSLModel]): list of ElmDsl or DSLModels which must have the same parameters.
        parameter_names (list[str] | None): list of parameter names. If None, all parameters considered. Defaults to None.
    
    Returns:
        dict: parameter (keys) and list of values (values) dict

Classes
-------

`DSLModel(obj: ElmDsl)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.pf_classes.elm.elm_base.ElmBase
    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic

    ### Methods

    `add_results_signal_type(self, signal_types: list[str]) ‑> list[str]`
    :   Add all signals of a certain type to monitored result variables
        
        Args:
            signal_types (list[str]): signal types according to block definition
             (for example "sOutput", "sInput", "sStates", "sParams", "sUpLimPar", "sLowLimPar")
        
        Returns:
            list[str]: list of signals that were added to the monitored result variables.

    `add_results_signals(self, signal_names: list[str]) ‑> None`
    :   Add signals to monitored variables.
        
        Args:
            signal_names (list[str]): names of signals (without 's:')

    `get_parameter_names(self) ‑> list[str]`
    :

    `get_parameter_values(self) ‑> list`
    :

    `get_parameters(self) ‑> dict`
    :   Get model parameter (keys) and value (values) dict of DSL model.
        
        Returns:
            dict: parameter-value dict