Module powfacpy.applications.topology
=====================================

Classes
-------

`Topology(pf_app: PFApp | None | bool = False, cached: bool = False)`
:   Base class for applications. Allows to create versions with
    - ActiveProjectCached (recommended when only one project stays active)
    - or ActiveProject (recommended when the active project may change)

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Methods

    `create_area(self, name: str, elms: list[PFGeneral], color: int = 2, parent_folder: str | PFGeneral = None, overwrite: bool = True) ‑> powfacpy.pf_classes.protocols.ElmZone`
    :

    `create_boundary_from_bus_branch(self, name: str, bus_branch: dict, to_branch: bool = True, color: int = 2, parent_folder: str | PFGeneral = None, overwrite: bool = True) ‑> powfacpy.pf_classes.protocols.ElmBoundary`
    :   Create a boundary by specifying buses (terminals) and branches (connected to the buses).
        
        Args:
            name (str): name of boundary
        
            bus_branch (dict): keys are the buses (terminals) as path strings or PF objects. Values are a list of one or more branch elements (e.g. lines) as path strings or PF objects which are connected with the bus.
        
            to_branch (bool, optional): Direction of boundary is towards branch (or towards terminal). Defaults to True.
        
            color (int, optional): Color of boundary shown in single line diagram. Defaults to 2.
        
            parent_folder (PFGeneral | str | None, optional): Parent folder where boundary is created. Defaults to None (i.e. default boundary folder).
        
            overwrite (bool, optional): Overwrite existing boundary with same name. Defaults to True.
        
        Returns:
            ElmBoundary: The boundary created.

    `create_boundary_using_intermediate_zone(self, name: str, elms: list[PFGeneral], exclude_node_elms: Callable | None = None, color: int = 2, parent_folder: PFGeneral | str | None = None, overwrite: bool = True) ‑> powfacpy.pf_classes.protocols.ElmBoundary`
    :   Create boundary (ElmBoundary) that includes 'elms'. A zone is created as an intermediate step.
        
        Warning: If there are existing zones in the network model those might be changed if 'elms' are included (because elements can only be part of one zone). To avoid this use 'create_boundary_without_changing_initial_zones' instead.
        
        Args:
            name (str): Name of boundary created
        
            elms (list[PFGeneral]): Network elements contained in boundary
            exclude_node_elms (Callable | None, optional): Condition to select elements to be excluded from the interior (e.g. `lambda x: x.GetClassName() == "ElmLod" to exclude all ElmLod). Defaults to None.
        
            color (int, optional): Color of boundary shown in single line diagram. Defaults to 2.
        
            parent_folder (PFGeneral | str | None, optional): PArent folder where boundary is created. Defaults to None (i.e. default boundary folder).
        
            overwrite (bool, optional): Overwrite existing boundary with same name. Defaults to True.
        
        Returns:
            ElmBoundary: Boundary object created.

    `create_boundary_without_changing_initial_zones(self, name: str, elms: list[PFGeneral], exclude_node_elms: Callable | None = None, color: int = 2, parent_folder: PFGeneral | str | None = None, overwrite: bool = True) ‑> powfacpy.pf_classes.protocols.ElmBoundary`
    :   Create boundary (ElmBoundary) that includes 'elms'. A zone is created as an intermediate step.
        
        In comparison to 'create_boundary_using_intermediate_zone', this methods avoids altering existing zones by creating an intermediate variation.
        
        Args:
            name (str): Name of boundary created
        
            elms (list[PFGeneral]): Network elements contained in boundary
            exclude_node_elms (Callable | None, optional): Condition to select elements to be excluded from the interior (e.g. `lambda x: x.GetClassName() == "ElmLod" to exclude all ElmLod). Defaults to None.
        
            color (int, optional): Color of boundary shown in single line diagram. Defaults to 2.
        
            parent_folder (PFGeneral | str | None, optional): PArent folder where boundary is created. Defaults to None (i.e. default boundary folder).
        
            overwrite (bool, optional): Overwrite existing boundary with same name. Defaults to True.
        
        Returns:
            ElmBoundary: Boundary object created.

    `create_zone(self, name: str, elms: list[PFGeneral], color: int = 2, parent_folder: str | PFGeneral = None, overwrite: bool = True) ‑> powfacpy.pf_classes.protocols.ElmZone`
    :

    `create_zone_from_boundary_bus_branch(self, name: str, bus_branch: dict, to_branch: bool = True, color: int = 2, parent_folder: str | PFGeneral = None, overwrite: bool = True) ‑> powfacpy.pf_classes.protocols.ElmZone`
    :   Create a zone via intermediate boundary and by specifying buses (terminals) and branches (connected to the buses).
        
        Args:
            name (str): name of zone
        
            bus_branch (dict): keys are the buses (terminals) as path strings or PF objects. Values are a list of one or more branch elements (e.g. lines) as path strings or PF objects which are connected with the bus.
        
            to_branch (bool, optional): Direction of boundary is towards branch (or towards terminal). Defaults to True.
        
            color (int, optional): Color of boundary shown in single line diagram. Defaults to 2.
        
            parent_folder (PFGeneral | str | None, optional): Parent folder where zone is created. Defaults to None (i.e. default zone folder).
        
            overwrite (bool, optional): Overwrite existing boundary with same name. Defaults to True.
        Returns:
            ElmZone: _description_