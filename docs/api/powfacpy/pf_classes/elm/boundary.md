Module powfacpy.pf_classes.elm.boundary
=======================================

Classes
-------

`Boundary(obj: ElmBoundary)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.pf_classes.elm.elm_base.ElmBase
    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic
    * powfacpy.pf_classes.elm.grouping_base.GroupingBase
    * abc.ABC

    ### Static methods

    `get_P_exchange_res_var_rms_bal() ‑> str`
    :

    `get_Q_exchange_res_var_rms_bal() ‑> str`
    :

    `show_boundary_interior_regions_in_network_graphic(reactivate_study_case: bool = True) ‑> None`
    :   Shows interior regions of all boundaries in the single line diagram.

    ### Methods

    `create_zone(self, name: str | None = None, parent_folder: str | None = None, color: int | None = None, overwrite: bool = True) ‑> powfacpy.pf_classes.protocols.ElmZone`
    :   Create Zone based on boundary
        
        Args:
            name (str | None, optional): Name of Zone. Defaults to None (same as boundary).
            parent_folder (str | None, optional): parent folder. Defaults to None (zone project folder).
            color (int | None, optional): color of zone. Defaults to None.
            overwrite (bool, optional): If true, any existing zone object with same name is overwritten. Defaults to True.
        
        Returns:
            ElmZone: Created zone object

    `exclude_node_elms_by_condition(self, condition: Callable) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Exclude elements from the interior of the boundary by adding their cubicle to the boundary.
        
        Args:
            condition (Callable): Condition to select the elements to be excluded among all interior elements (e.g. `lambda x: x.GetClassName() == "ElmLod" to exclude all ElmLod)
        
        Returns:
            list[PFGeneral]: Elements that were excluded

    `get_average_frequency(self, simulation_results: pd.DataFrame, source: str = 'terminals', ignored_elms: list[PFGeneral] | None = None) ‑> float`
    :   Get the average frequency inside the boundary.
        
        Args:
            simulation_results (pd.DataFrame): Simulation results (exported using the 'Results' interface)
            source (str, optional): Frequency measurement source. Options:
                - 'terminal' (ElmTerm, default)
                - 'pll' (StaPll)
                - 'sm' (ElmSym)
            ignored_elms (list[PFGeneral] | None, optional): sources (e.g. ElmTerm/StaPll objects) that are not included. Defaults to None.
        
        Returns:
            float: Average frequency