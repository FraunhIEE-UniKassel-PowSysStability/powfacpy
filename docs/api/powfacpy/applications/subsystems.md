Module powfacpy.applications.subsystems
=======================================

Classes
-------

`SubSystem(grouping: ElmAreaOrZone, pf_app=False, cached=False)`
:   Subsystem of a larger power system. This is the grouping class of powfacpy to extend the functionality of zones and areas in PowerFactory.

    ### Ancestors (in MRO)

    * powfacpy.pf_classes.elm.zone.Zone
    * powfacpy.pf_classes.elm.zone.ZoneStatic
    * powfacpy.pf_classes.elm.elm_base.ElmBase
    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic
    * powfacpy.pf_classes.elm.grouping_base.AreaZoneBase
    * powfacpy.pf_classes.elm.grouping_base.GroupingBase
    * abc.ABC
    * powfacpy.applications.application_base.ApplicationBase

    ### Instance variables

    `dynamic_models: SubSystemDynamicModels`
    :

    `load_flow: SubSystemLoadFlow`
    :

    `name: str`
    :

    `topology: SubSystemTopology`
    :

    ### Methods

    `get_load_flow_state(self, execute_load_flow: bool = True, format: str | None = 'pandas') ‑> powfacpy.applications.subsystems.SubSystemLoadFlow`
    :

`SubSystemContainer(subsystems: list[SubSystem] | list[ElmZone], pf_app=False, cached=False)`
:   Container for multiple subsystems, e.g. to analyze the power exchange between them.

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Instance variables

    `elm_zones: list[ElmZone]`
    :

    `names: list[str]`
    :

    `num_subsystems: int`
    :

    `power_exchange: pd.DataFrame`
    :

    `subsystems: list[SubSystem]`
    :

    `total_power_generation: np.ndarray`
    :

    `total_power_loads: np.ndarray`
    :

    ### Methods

    `delete_subsystem(self, subsystem: int | SubSystem) ‑> None`
    :   Delete subsystem from the container.
        
        Ensure that all attributes of the container that depend on the subsystems are updated/reset accordingly (e.g. power exchange matrix, total loads/generation etc.).
        
        Args:
            subsystem (int | SubSystem): subsystem or its index in the container to be deleted

    `get_index_of_subsystem(self, subsys: SubSystem) ‑> int`
    :

    `get_load_flow_state(self, execute_load_flow: bool = True) ‑> pandas.core.frame.DataFrame`
    :   Get load flow state of all subsystems in the container.
        
         Args:
            execute_load_flow (bool, optional): If true, execute load flow first to ensure that results are present. Defaults to True.
        
        Returns:
            pd.DataFrame: Load flow state of all subsystems in the container.

    `get_neighboring_subsystems_in_container(self, subsystem: int | SubSystem | ElmZone) ‑> list[powfacpy.applications.subsystems.SubSystem]`
    :   Get neighbors of 'subsystem' in container.
        
        Args:
            subsystem (int | SubSystem): subsystem or its index in the container for which the neighbors should be found.
        
        Returns:
            list[SubSystem]: List of neighboring subsystems.

    `get_power_exchange_in_MVA(self, execute_load_flow: bool = True, format: str = 'dataframe', value_no_exchange=(nan+0j)) ‑> np.array | pd.DataFrame`
    :   Get power exchange between subsystems in MVA.
        
        Args:
            execute_load_flow (bool, optional): If true, execute load flow first to ensure that results are present. Defaults to True.
            format (str, optional): If "dataframe", return a pandas DataFrame; otherwise, return a numpy array. Defaults to "dataframe".
            value_no_exchange (_type_, optional): The value to use for no exchange between subsystems that are not connected. Defaults to np.nan+0j.
        
        Returns:
            np.array | pd.DataFrame: power exchange.

    `subsys_to_indices(self, subsys: list[SubSystem]) ‑> list[int]`
    :   Get indices of subsystems.
        
        Args:
            subsys (list[SubSystem]): subsystems
        
        Returns:
            list[int]: Indices

`SubSystemDynamicModels(parent: Subsystem)`
:   Subsystem dynamic models (e.g. synchronous machines, governors, controllers).

    ### Instance variables

    `synchronous_machines: SubSystemTopology`
    :

`SubSystemLoadFlow(parent: Subsystem)`
:   Load (power) flow properties of subsystem.

    ### Methods

    `get_load_flow_state(self, execute_load_flow: bool = True, format: str | None = 'pandas') ‑> None`
    :   Get load flow results of subsystem.
        
        Includes total load/generation, power exchange etc.
        
        Args:
            execute_load_flow (bool, optional): _description_. Defaults to True.
            format (str | None, optional): Format of the returned results. Options are 'pandas', 'dict' or None. Defaults to "pandas".

`SubSystemSynchronousMachines(parent: Subsystem)`
:   Synchronnous machines and their controllers in the subsystem.

    ### Instance variables

    `avrs: list[ElmTerm]`
    :   Get automatic voltage regulators (AVR)

    `governors: list[ElmTerm]`
    :   Get governors

    `pss: list[ElmDsl]`
    :   Get power system stabilizers (PSS)

    `root_subsystem: list[ElmTerm]`
    :

    `synchronous_machines: list[ElmTerm]`
    :

    `synchronous_machines_powfacpy: list[SynchronousMachine]`
    :   Get synchronous machines as powfacpy objects.

    ### Methods

    `get_avr_info(self, average: str | None = 'apparent_power_weighted') ‑> None`
    :

    `get_governor_info(self, average: str | None = 'apparent_power_weighted') ‑> None`
    :

    `get_pss_info(self, average: str | None = 'apparent_power_weighted') ‑> None`
    :

`SubSystemTopology(parent: Subsystem)`
:   

    ### Instance variables

    `lines: list[ElmLne]`
    :

    `terminals: list[ElmTerm]`
    :

    ### Methods

    `get_indices_of_terminals(self, terminals_superset: list[ElmTerm]) ‑> list[int]`
    :   Get indices of the terminals inside the subsystem in a terminal superset (e.g. all terminals of the whole system).
        
        Args:
            terminals_superset (list[ElmTerm]): Superset of terminals
        
        Returns:
            list[int]: list of indices of the terminals inside the subsystem in the terminal superset

    `is_neighbor(self, grouping: ElmAreaOrZone | AreaOrZone | SubSystem) ‑> bool`
    :   Check if another subsystem/grouping is physically connected to this subsystem (by calculating the power exchange).
        
        Args:
            grouping (ElmAreaOrZone | AreaOrZone | Subsystem): Potential neighboring subsystem/grouping
        
        Returns:
            bool: true if the other subsystem/grouping is a neighbor, false otherwise