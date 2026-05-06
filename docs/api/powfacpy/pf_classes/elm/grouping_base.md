Module powfacpy.pf_classes.elm.grouping_base
============================================

Classes
-------

`AreaZoneBase()`
:   Abstract base class for Areas and Zones. Those classes basically offer the same functionality ibn PF.

    ### Ancestors (in MRO)

    * powfacpy.pf_classes.elm.grouping_base.GroupingBase
    * abc.ABC

    ### Descendants

    * powfacpy.pf_classes.elm.area.AreaStatic
    * powfacpy.pf_classes.elm.zone.ZoneStatic

    ### Instance variables

    `total_power_loads: complex`
    :

    ### Methods

    `get_neighbors(self, groupings: list[AreaZoneBase] | list[ElmAreaOrZone] | None = None) ‑> list[powfacpy.pf_classes.elm.grouping_base.AreaZoneBase] | list[ElmAreaOrZone]`
    :

    `is_neighbor(self, grouping: AreaOrZone | ElmAreaOrZone) ‑> bool`
    :

    `load_flow_power_exchange_with_in_MVA(self, grouping: ElmAreaOrZone | AreaOrZone, return_value_no_exchange=nan) ‑> complex`
    :   Get load flow apparent power exchange (in MVA) with other grouping.
        
        Args:
            grouping (ElmAreaOrZone | AreaOrZone): other grouping
            return_value_no_exchange (_type_, optional): return value when there is no connection. Defaults to np.nan.
        
        Returns:
            complex: load flow apparent power exchange (in MVA) if connected

    `load_flow_total_power_generation_in_MVA(self) ‑> complex`
    :

    `load_flow_total_power_loads_in_MVA(self) ‑> complex`
    :

    `merge(self, grouping_to_merge: GroupingBase) ‑> ElmAreaOrZone`
    :   Merge another grouping of same type into current grouping. The other grouping is deleted after merging.
        
        Args:
            grouping_to_merge (GroupingBase): grouping to merge (must be of same type as self)
        
        Returns:
            ElmAreaOrZone: merged grouping (as ElmArea or ElmZone)

`GroupingBase()`
:   Base class for groupings (ElmZone, ElmArea, ElmBoundary). Provides a common interface (e.g. to get internal elements).

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * powfacpy.pf_classes.elm.boundary.Boundary
    * powfacpy.pf_classes.elm.grouping_base.AreaZoneBase

    ### Methods

    `add_results_variable_for_elms(self, condition_for_elms: Callable, result_variables: str | list[str], results_obj: ElmRes | None = None) ‑> None`
    :   Add results variable for internal elements selected by 'condition'.
        
        Args:
            condition_for_elms (Callable): Condition to select elements, e.g. 'lambda x: x.GetClassName() = "ElmTerm"'
        
            result_variables (str | list[str]): Results variable name(s).
        
            results_obj (ElmRes | None, optional): Results object where variables are added. Defaults to None ('get_from_study_case' is used).

    `are_internal_elms(self, elms: list[PFGeneral]) ‑> bool`
    :

    `are_internal_elms_with_same_class(self, elms: list[PFGeneral]) ‑> bool`
    :   Checks whether all network elements in 'elms' (which MUST all be of the same class) are internal elements.
        
        Args:
            elms (list[PFGeneral]): list of network elements of same class
        
        Returns:
            bool: True if all elements are included

    `get_all_groupings_of_same_type(self) ‑> list`
    :   Get all calculation relevant groupings of the same type (Zone class returns ElmZone, Area class returns...)
        
        Returns:
            list: alls groupings of same type

    `get_all_internal_elms(self) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Get all internal elements (to be implemented in concrete class)
        
        Returns:
            list[PFGeneral]: list of all internal elements.

    `get_all_powfacpy_groupings_of_same_type(self) ‑> list`
    :   Get all calculation relevant groupings of the same type (Zone class returns Zone, Area class returns...)
        
        Difference to 'get_all_groupings_of_same_type' is that e.g. Zones instead ElmZone are returned
        
        Returns:
            list: alls groupings of same type

    `get_converters(self) ‑> list`
    :

    `get_grid_following_converters(self) ‑> list`
    :

    `get_grid_forming_converters(self) ‑> list`
    :

    `get_internal_elms(self, condition: Callable | None = None) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Get internal elements with optional condition.
        
        Args:
            condition_for_elms (Callable): Condition to select elements, e.g. 'lambda x: x.GetClassName() = "ElmTerm"'
        
        Returns:
            list[PFGeneral]: list of network elements.

    `get_internal_elms_of_class(self, class_name: str) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :

    `get_network_elements_of_plant_models(self, elm_objs: list[str] | list[PFGeneral], condition: Callable) ‑> dict`
    :

    `get_network_elements_of_plant_models_sorted_by_block_definition(self, elm_objs: list[str] | list[PFGeneral], condition: Callable) ‑> dict`
    :

    `get_phase_locked_loops(self) ‑> list[powfacpy.pf_classes.protocols.StaPll]`
    :   Get all internal phase-locked loops (StaPll) objects (i.e. PLLs that measure at internal terminals).
        
        Returns:
            list[StaPll]: List of internal PLLs.

    `get_total_inertia_of_synchronous_machines_in_MWs(self) ‑> float`
    :   Sum of inertia of internal synchronous machines in MWs

    `is_internal_elm(self, elm: PFGeneral) ‑> bool`
    :

    `load_flow_total_power_exchange_in_MVA(self) ‑> complex`
    :