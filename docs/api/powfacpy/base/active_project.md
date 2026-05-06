Module powfacpy.base.active_project
===================================

Classes
-------

`ActiveProject(pf_app: PFApp | None | bool = False)`
:   Interface to the currently active project.
    
    Args:
        folder (Union[PFGeneral, str]): folder object or path in active project (or in active user if no project is active)
        pf_app (PFApp | None | bool, optional): Powerfactory app (returned by GetApplication). Defaults to False (does not default to None because None is returned by GetApplication if something goes wrong; Therefore, None should raise an exception).
    
    Raises:
        TypeError: When pf_app is None. See explanation of argument 'pf_app'.

    ### Ancestors (in MRO)

    * powfacpy.base.folder.Folder
    * powfacpy.base.base.BaseObjectStatic

    ### Descendants

    * powfacpy.base.active_project.ActiveProjectCached
    * powfacpy.pf_classes.protocol_generator.PFClassesProtocolGenerator

    ### Instance variables

    `areas_folder`
    :

    `boundaries_folder`
    :

    `circuits_folder`
    :

    `equipment_type_lib_folder`
    :

    `feeders_folder`
    :

    `library_folder`
    :

    `load_flow_command: ComLdf`
    :

    `network_data_folder`
    :

    `network_model_folder`
    :

    `operation_scenarios_folder`
    :

    `scripts_folder`
    :

    `stored_attr: dict`
    :   DatabaseDict to store and reset attributes of PF objects.

    `study_cases_folder`
    :

    `templates_folder`
    :

    `variations_folder`
    :

    `versions_folder`
    :

    `zones_folder`
    :

    ### Methods

    `activate_study_case(self, path: str) ‑> powfacpy.pf_classes.protocols.IntCase`
    :   Activate study case under path.

    `add_results_variable(self, obj: PFGeneral | str | list[PFGeneral | str], variables: str | list[str], results_obj: ElmRes | None = None) ‑> powfacpy.pf_classes.protocols.ElmRes`
    :   Add variable(s) of 'obj' to the monitored variables in of result object.
        
        Args:
        
            obj (PFGeneral | str | list[PFGeneral | str]): PF object or its path
        
            variables (list[str]): variable names
        
            results_obj (ElmRes, optional): Results object. Defaults to None (ElmRes from active study case is used).
        
        Returns:
            ElmRes: the results object

    `add_template_from_global_library(self, template_name: str | list[str], target_folder: PFGeneral | None = None) ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :   Add a template from the global library to the active project.
        
        Args:
            template_name (str): Name of the template (e.g. 'MyTemplate.dz')
            target_folder (PFGeneral | None, optional): Target folder in the active project. Defaults to None (i.e. templates folder).
        
        Returns:
            PFGeneral: The created object in the active project.

    `add_variable_selection_obj_to_results_obj(self, name, results_obj: ElmRes, class_name: str = None, variables: list[str] = []) ‑> powfacpy.pf_classes.protocols.IntMon`
    :   Add a variable selection object (IntMon) to a result object (ElmRes).
        
        Args:
            name (str): Name of IntMon
            results_obj (ElmRes): Results object
            class_name (str, optional): 'classnm' parameter of IntMon. Defaults to None.
            variables (list[str], optional): 'vars' parameter of IntMon. Defaults to [].
        
        Returns:
            IntMon: variable selection object

    `check_load_flow_results(self, when_invalid: str = 'error') ‑> bool`
    :   Check whether load flow results in PF are present and valid and raise exception, warning or execute load flow if not.
        
        Args:
            when_invalid (str, optional): If load flow results are invalid, 'error' (raises exception), 'warning' raises warning, 'execute' executes load flow and raises exception if results are invalid. Defaults to "error".
        
        Raises:
            PFInvalidLoadFlow: When load flow results are invalid and 'when_invalid'= 'error' or 'execute' and results are invalid.
        
        Returns:
            bool: True only when results are valid.

    `clear_elmres(self, results_obj: ElmRes = None)`
    :   Clear all results variables from results object (ElmRes).
        
        Args:
            results_obj (ElmRes, optional): Results object. Defaults to None (get elmres from study case).

    `clear_elmres_from_objects_with_status_deleted(self, results_obj: ElmRes | None = None)`
    :   Deletes all objects from a results object (ElmRes) that have the
        status deleted (i.e. attribute 'obj_id' is deleted).

    `clear_results_variables(self, results_obj: ElmRes | None = None) ‑> None`
    :

    `create_comtrade_obj(self, file_path: str, parent_folder: Union[PFGeneral, str] = None) ‑> powfacpy.pf_classes.protocols.IntComtrade`
    :   Add an IntComtrade that refers to file_path (*.cfg).
        The objects are stored in a folder "Comtrade" in the currently active
        study case, unless a parent_folder is given. A new object is only
        created if there exists no object yet that points to the same file
        ('f_name' attribute is the file path). The file name is used for the
        new object name (without the .cfg ending).

    `create_parallel_scenario_for_study_case(self, case: IntCase | str, overwrite: bool = True, activate: bool = True) ‑> powfacpy.pf_classes.protocols.IntScenario`
    :   Create a parallel scenario for a study case (same subfolders as in the study cases folder are also used in the scenarios folder).
        
        Args:
            case (IntCase | str): study case
            overwrite (bool, optional): overwrite existing object. Defaults to True.
            activate (bool, optional): activate variation. Defaults to True.
        
        Returns:
            IntScenario: Scenario

    `create_parallel_variation_for_study_case(self, case: IntCase | str, overwrite: bool = True, activate: bool = True) ‑> powfacpy.pf_classes.protocols.IntScheme`
    :   Create a parallel variation for a study case (same subfolders as in the study cases folder are also used in the variations folder).
        
        Args:
            case (IntCase | str): study case
            overwrite (bool, optional): overwrite existing object. Defaults to True.
            activate (bool, optional): activate variation. Defaults to True.
        
        Returns:
            IntScheme: variation

    `create_project_version(self, version_name: str, overwrite: bool = True) ‑> None`
    :   Create a version of current state of the project.
        
        Uses 'CreateVersion'. New version will be added to top level versions folder of project.
        
        Args:
            version_name (str): Name (loc_name) of version
        
            overwrite (bool, optional): Overwrite existing version with same name. Defaults to True.

    `create_scenario(self, name: str, parent_folder: str | PFGeneral = None, activate: bool = True, overwrite: bool = True) ‑> powfacpy.pf_classes.protocols.IntScenario`
    :

    `create_study_case(self, name: str, copy_from: IntCase | str | None = None, parent_folder: PFGeneral | str | None = None, create_variation: bool = False, create_scenario: bool = False, overwrite: bool = True, use_existing=False, activate: bool = True) ‑> powfacpy.pf_classes.protocols.IntCase | list[powfacpy.pf_classes.protocols.IntCase | powfacpy.pf_classes.protocols.IntScheme | powfacpy.pf_classes.protocols.IntScenario]`
    :   Create a new study case and optionally a variation and/or scenario.
        
        Args:
            name (str): name (used for case name and variation/scenario name)
            copy_from (IntCase | str | None, optional): case to copy from. Defaults to None.
            parent_folder (PFGeneral | str | None, optional): parent folder (same subfolders are used for variation/scenario). Defaults to None.
            create_variation (bool, optional): Defaults to False.
            create_scenario (bool, optional): Defaults to False.
            overwrite (bool, optional): existing objects are overwritten. Defaults to True.
            use_existing (bool, optional): existing objects are used. Defaults to False.
            activate (bool, optional): activate case/variation/scenario. Defaults to True.
        
        Returns:
            IntCase | list[IntCase | IntScheme | IntScenario]: Created case or list with case/variation/scenario.

    `create_variation(self, name: str, parent_folder: str | PFGeneral = None, name_expansion_stage: str = 'Expansion Stage', activationTime: int = 0, activate: int = 1, overwrite: bool = True) ‑> powfacpy.pf_classes.protocols.IntScheme`
    :   Create variation (including one expansion stage).
        
        Args:
            name (str): Name of variation
            parent_folder (str | PFGeneral, optional): Parent folder where variation is created. Defaults to None (i.e. variations folder).
            name_expansion_stage (str, optional): Name of. Defaults to "Expansion Stage".
            activationTime (int, optional): UTC time
            activate (int, optional): If 1, expansion stage is activated. If 0, expansion stage is not activated. Defaults to 1.
        
        Returns:
            IntScheme: The created variation object

    `duplicate_to_restore_attributes(self, obj: PFGeneral | str, attr: str | list[str], parent_folder: PFGeneral | Folder | str = None, suffix_of_duplicate: str = '_COPY') ‑> PFGeneral`
    :

    `execute_load_flow(self, params: dict = {}) ‑> int`
    :

    `get_active_networks(self, error_if_no_network_is_active: bool = True) ‑> powfacpy.pf_classes.protocols.ElmNet`
    :   Get active networks/grids.

    `get_active_study_case(self, error_if_no_active_case: bool = True) ‑> powfacpy.pf_classes.protocols.IntCase | None`
    :   Get the currently active study case. Control whether error should be raised if no case is active.
        
        Args:
            error_if_no_active_case (bool, optional): If True, raise exception if no case is active. If False, return none. Defaults to True.
        
        Raises:
            PFNoActiveStudyCaseError: When no case is active.
        
        Returns:
            IntCase: The active study case | None

    `get_active_user_folder(self) ‑> powfacpy.pf_classes.protocols.IntUser`
    :   Get folder of active user.

    `get_calc_relevant_obj(self, obj_str: str, condition: Callable | None = None, error_if_non_existent=True, includeOutOfService: int = 1, topoElementsOnly: int = 0, bAcSchemes: int = 0) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Wraps the method 'GetCalcRelevantObjects' (see PF scripting reference) and adds optional arguments similar to 'get_obj'.
        
        Warning: If 'obj_str' contains several objects separated by comma, the order of the returned objects may differ from the order in the string.
        
        Args:
            obj_str (str): name including class of object(s) (NOT their path)
        
            condition (Callable | None, optional): See get_obj. Defaults to lambda x:True.
        
            error_if_non_existent (bool, optional): See get_obj. Defaults to True.
        
            includeOutOfService (int, optional): Flag whether to include out of service objects. Defaults to 1. (Copied from scripting reference)
        
            topoElementsOnly (int, optional): Flag to filter for topology relevant objects only. Defaults to 0. (Copied from scripting reference)
        
            bAcSchemes (int, optional): Flag to include hidden objects in active schemes. Defaults to 0. (Copied from scripting reference)
        
        Returns:
            list[PFGeneral]: Found object(s)

    `get_diagram_color_scheme(self) ‑> powfacpy.pf_classes.protocols.SetColscheme`
    :

    `get_events_folder_from_initial_conditions_calc(self) ‑> powfacpy.pf_classes.protocols.IntEvt`
    :   Get events folder (IntEvt) from the initial conditions calculation object (ComInc).
        
        This folder is used for the events in dynamic time domain simulation (RMS/EMT).
        
        Returns:
            IntEvt: Events folder.

    `get_first_level_folder(self, folder_type: str) ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :   Get folder on first level of PF database.
        
        Args:
            folder_type (str): The folder of the active user ('user') or the global library ('global library') can be accessed.
        
        Raises:
            TypeError: Invalid folder_type input
        
        Returns:
            PFGeneral: first level folder

    `get_from_global_library(self, name: str | list[str]) ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :   Get object(s) from global library.
        
        Args:
            name (str): name(s) of object(s) to get from global library (used for 'GetContents').
        
        Returns:
            PFGeneral: Object(s) from global library

    `get_from_study_case(self, class_name: str, if_not_unique: str = 'warning', if_no_study_case: str = 'error') ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :   Get objects from active study case (similar to PF built-in function 'app.GetFromStudyCase()').
        
        Additionally, this method prints a warning or raises an exception if there is more than one object found in the study case and if no study case is activated.
        
        Args:
            class_name (str): class name of the object (e.g. 'ElmRes'), optionally preceded by an object name without wildcards and a dot (e.g. 'All Calcualations.ElmRes')
        
            if_not_unique (str, optional): Warn ('warning') or raise exception ('error') if there are more than one objects of class 'class_name'. Defaults to "warning".
        
            if_no_study_case (str, optional): Warn ('warning') or raise exception ('error') if no study case is active. Defaults to "error".
        
        Raises:
            PFNoActiveStudyCaseError: No study case activated
            TypeError: More than one object was found
        
        Returns:
            PFGeneral: Found or created object

    `get_global_library_folder(self) ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :

    `get_parameter_value_string(self, parameters: dict, delimiter=' ') ‑> str`
    :   Get string with parameters and their values.
        
        Args:
            parameters (dict): parameters (keys) and values (values)
            Example: {'P': 2.5, 'Q': 0}
        
            delimiter (str, optional): Delimiter between parameter value pairs. Defaults to " ".
        
        Returns:
            str: parameter value string (e.g. 'P = 2.5 Q = 0')

    `get_project_directory(self) ‑> str`
    :   Get the project directory (for related files).
        
        Returns:
            str: Path

    `get_project_version(self, version_name: str) ‑> powfacpy.pf_classes.protocols.IntVersion | None`
    :   Get (previous) version of project.
        
        Args:
            version_name (str): Name (loc_name) of version
        
        Returns:
            IntVersion | None: Version object

    `get_results_obj_from_initial_conditions_calc(self) ‑> powfacpy.pf_classes.protocols.ElmRes`
    :   Get results object (ElmRes) from the initial conditions calculation object (ComInc).
        
        This is the results object where results from time domain (RMS/EMT) simulation are written to.
        
        Returns:
            ElmRes: ElmRes object

    `has_valid_load_flow_results(self) ‑> bool`
    :

    `import_dz_file(self, file_path: str, target_folder: PFGeneral | None = None) ‑> list`
    :   Import a .dz file (e.g. a template).
        
        Args:
            file_path (str): path of .dz file
            target_folder (PFGeneral | None, optional): target folder. Defaults to None (active project).
        
        Returns:
            list: [int errorCode, list importedObjects]

    `import_project(self, file_path: str, target_folder_in_active_user: str | PFGeneral | None = None, keep_current_project_activated: bool = True) ‑> powfacpy.pf_classes.protocols.IntPrj`
    :   Import a project (.pfd file)
        
        Args:
            file_path (str): Windows path. Don't use relative paths.
        
            target_folder_in_active_user (str | PFGeneral | None, optional): Target folder for project import in active user. Defaults to None.
        
            keep_current_project_activated (bool, optional): If True, the initial project and study case remain active.If False, the imported project will be active after import. Defaults to True.
        
        Returns:
            IntPrj: Imported project

    `mark_in_graphics(self, elms: list[PFGeneral] | PFGeneral, searchOpenedDiagramsOnly: int = 0) ‑> None`
    :

    `reactivate_project(self) ‑> None`
    :   Deactivate and activate the active project.

    `reactivate_study_case(self) ‑> None`
    :

    `reset_default_units(self) ‑> None`
    :   Reset the default units of the active project. Deletes the content in the 'Settings\Units' folder and reactivates the project so that settings take effect.

    `reset_stored_attr(self, flush_memory: bool = False, store_current_values: bool = False) ‑> None`
    :   Reset the original values stored when calling 'set_attr_resettable'.
        
        Args:
            flush_memory (bool, optional): Stored values will be deleted. Defaults to False.
            store_current_values (bool, optional): Current values will be written to the dictionary of the stored values. Defaults to False.

    `rollback_project_to_previous_version(self, version_name: str) ‑> None`
    :   Rollback to previous project version (IntVersion in versions folder).
        
        Args:
            version_name (str): Name (loc_name) of version.

    `set_attr_resettable(self, obj: PFGeneral | str, params: dict, parent_folder: PFGeneral | Folder | str = None) ‑> None`
    :   Set attributes of an object and to store the original values (e.g. to reset them later).
        
        Args:
            obj (PFGeneral | str): PF object or its path
            params (dict): parameter names (keys) and values (values)
            parent_folder (PFGeneral | Folder | str, optional): parent folder of object. Defaults to None.

    `set_time_using_year(self, year)`
    :

`ActiveProjectCached(pf_app: PFApp | None | bool = False)`
:   Caches the properties. Should be used only with one active project (the caching fails after a different project has been activated).
    
    Args:
        folder (Union[PFGeneral, str]): folder object or path in active project (or in active user if no project is active)
        pf_app (PFApp | None | bool, optional): Powerfactory app (returned by GetApplication). Defaults to False (does not default to None because None is returned by GetApplication if something goes wrong; Therefore, None should raise an exception).
    
    Raises:
        TypeError: When pf_app is None. See explanation of argument 'pf_app'.

    ### Ancestors (in MRO)

    * powfacpy.base.active_project.ActiveProject
    * powfacpy.base.folder.Folder
    * powfacpy.base.base.BaseObjectStatic

    ### Instance variables

    `areas_folder`
    :

    `boundaries_folder`
    :

    `circuits_folder`
    :

    `equipment_type_lib_folder`
    :

    `feeders_folder`
    :

    `library_folder`
    :

    `network_data_folder`
    :

    `network_model_folder`
    :

    `operation_scenarios_folder`
    :

    `scripts_folder`
    :

    `study_cases_folder`
    :

    `templates_folder`
    :

    `variations_folder`
    :

    `versions_folder`
    :

    `zones_folder`
    :