Module powfacpy.applications.study_cases
========================================

Classes
-------

`StudyCases(pf_app: powfacpy.pf_classes.protocols.PFApp | None | bool = False, cached: bool = False)`
:   Base class for applications. Allows to create versions with
    - ActiveProjectCached (recommended when only one project stays active)
    - or ActiveProject (recommended when the active project may change)

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Instance variables

    `active_grids`
    :   Active grids for each study case (can be multiple for each). If only one is given, the same grid is active in every case.

    `add_scenario_to_each_case`
    :   If True, a corresponding scenario is created for each case.

    `add_variation_to_each_case`
    :   If True, a corresponding variation is created for each case.

    `anonymous_parameters`
    :   Parameters for which names are not used in folder/case name strings (only the parameter values are used).

    `base_study_case`
    :   Base study case (or its path) which is copied to create the cases.

    `consecutively_number_case_names`
    :   If True, numbering is added to the case names.

    `delimiter`
    :   Default delimiter used in parameter-value strings.

    `hierarchy`
    :   Hierarchy of folders (named after the parameters) where case/scenario/variation objects are located.

    `ignore_parameters_that_are_none_in_names`
    :   If True, parameters with value None are ignored in names (of cases etc.).

    `omitted_combinations`
    :   Omitted parameter combinations (in permutation).

    `overwrite_study_cases`
    :   If True, existing study cases are overwritten (e.g. when calling 'create_case' one more time with the same settings).

    `parameter_paths`
    :   Dictionary with parameter names as keys and their path or and object, attribute tuple as values).

    `parameter_values`
    :   Dictionary with parameters names (keys) and lists with parameter values for each case (values).

    `parent_folder_scenarios`
    :   Parent folder where scenarios are created.

    `parent_folder_study_cases`
    :   Parent folder where study cases are created.

    `parent_folder_variations`
    :   Parent folder where variations are created.

    `study_cases: list[powfacpy.pf_classes.protocols.IntCase]`
    :   List of created study case objects when calling 'create_cases' (read-only).

    `study_cases_names`
    :   Names of study cases. If not specified, names are automatically created from parameters and values.

    `title`
    :   Title of the case studies.

    ### Methods

    `activate_grids(self, case_num: int) ‑> None`
    :   Activate the corresponding grids of a study case.
        
        If 'self.active_grids' is a list/tuple, the items correspond to
        each study case. If multiple grids are active for a case, list/tuples can be used in the elements in 'active_grids'.
        If 'self.active_grid' is not a list/tuple, then one grid will be used
        for all cases.
        
        The grids can be PF objects or their paths.

    `apply_permutation(self, omitted_combinations: list[dict[str, list]] = None) ‑> None`
    :   Replaces the values in 'parameter_values' with the permutation of
        their unique elements.
        
        Use this method if you want to create cases of the permutation of all
        parameters. Note that 'parameter_values' is changed irreversibly.
        
        Args:
            omitted_combinations (list[dict[str, list]], optional): Parameter combinations that are omitted. Defaults to None.
        
            Example:
              omitted_combinations = [
                {"Par 1": [1, 0], "Par 2": ["R", "T"]},
                {"Par 3": [2], "Par 1": "all", "Par 4": "all"},
              ]
              Note that the 'all' keyword is used which means that all combiations with this parameter are omitted.

    `clear_parent_folders(self)`
    :   Deletes all objects in the folders returned by
        - self.get_study_cases_parent_folder
        - self.get_scenarios_parent_folder
        - self.get_variations_parent_folder

    `create_cases(self, reactivate_initially_activated_study_case: bool = True) ‑> None`
    :   Create study cases.
        
        Optionally create corresponding scenarios/variations (if add_scenario_to_each_case/add_variation_to_each_case is True).
        
        Iterates through all cases and creates study cases (and folders
        according to 'hierarchy') using parameter-value strings for the
        study cases (and folder names).

    `export_results_of_study_cases_to_csv(self, export_dir: str = None, study_cases: list[powfacpy.pf_classes.protocols.IntCase] = None, case_numbers: list[int] = None, results_obj: str = 'ElmRes', results_variables: list[str] = None, format_csv_file=True) ‑> list[str]`
    :   Export the simulation results (ElmRes) of the study cases to csv files.
        The csv files are named according to the study case number (e.g. case0.csv, case1.csv,..)
        Returns the full paths of the csv files.
        
        Arguments:
          - export_dir: directory for export (default is working directory)
          - study_cases: study case objects
          - case_numbers: corresponding study case numbers
          - results_obj: string that is used in GetFromStudyCase to get the ElmRes object (e.g.
            'self.act_prj.app.GetFromStudyCase("ElmRes")' )
          - results_variables: if only specific variables should be export (see also
              export_to_csv). By default all variables are exported.
          - format_csv_file: see export_to_csv

    `get_case_params_value_string(self, case_obj_or_case_num: powfacpy.pf_classes.protocols.IntCase | int, omitted_parameters: list[str] = None, delimiter: str = None, equals_sign: str = None, anonymous_parameters: list[str] = None) ‑> str`
    :   Get parameter-value string for a case
        
        Args:
            case_obj_or_case_num (IntCase | int): study case
        
            omitted_parameters (list[str], optional): parameters will not be considered. Defaults to None.
        
            delimiter (str, optional): delimiter between parameter value pairs. Defaults to None.
        
            equals_sign (str, optional): sign between parameter name and value. Defaults to None.
        
            anonymous_parameters (list[str], optional): only the value of these parameters will be added (not their name). Defaults to None.
        
        Returns:
            str: Parameters and their values

    `get_folder_path(self, case_num: int) ‑> str | None`
    :   Get folder path (inside parent folder) of a case.
        
        The path corresponds to parameter-value pairs specified
        in 'self.hierarchy'.
        
        Args:
          case_num (int): case number
        
        Returns:
          str | None: path of study case or None if there is no hierarchy

    `get_scenarios_parent_folder(self) ‑> powfacpy.pf_classes.protocols.IntFolder | powfacpy.pf_classes.protocols.IntPrjfolder`
    :   Get folder where scenarios are created.
        
        Returns:
            IntFolder | IntPrjfolder: folder

    `get_study_case_number(self, study_case: powfacpy.pf_classes.protocols.IntCase) ‑> int`
    :   Get the number (index) of a study case object.

    `get_study_cases(self, conditions: dict[str, typing.Callable] | Callable, return_case_numbers: bool = False) ‑> list[powfacpy.pf_classes.protocols.IntCase] | tuple[list[powfacpy.pf_classes.protocols.IntCase], list[int]]`
    :   Retrieve study case objects depending on parameter values.
        
        Example 1:
          get_study_cases({"par1": lambda x: x == 2, "par2": lambda x: x>0})
            This returns the study cases for which 'par1' equals 2 and 'par2' is
            positive.
        
        Example 2 (lambda function):
          get_study_cases(lambda x: x[0] >= 2 and x[2] == 'A')
        
        Args:
            conditions (dict[str, Callable] | Callable):
              Either a dictionary with
                keys: parameter names
                values: Callables with boolean return value depending on
                  parameter (key)
        
              or a single Callable that accepts an iterable containing all
                parameters.
                Example: lambda x: x[0] >= 2 and x[2] == 'A'
        
                Note that the order of the parameters in x must be the same as the
                order of the keys in self.parameter_values.
        
            return_case_numbers (bool, optional): If True, the case number are also returned. Defaults to False.
        
        Raises:
            ValueError: If 'callable' is invalid.
        
        Returns:
            list[IntCase] | tuple[list[IntCase], list[int]]: study case objects and case numbers (optional)

    `get_study_cases_from_string(self, conditions: str, return_case_numbers: bool = False) ‑> list[powfacpy.pf_classes.protocols.IntCase] | tuple[list[powfacpy.pf_classes.protocols.IntCase], list[int]]`
    :   This method is another convenient way to get study cases according to conditions. The conditions are a simple lambda function argument string (see example below). This method is more convenient but less safe than 'self.get_study_cases' because the conditions string is evaluated and a lambda function is created from it. Using eval() statements is generally not recommended due to unforeseeable behavior.
        However, for convenience, it is used here.
        
        Args:
          conditions (str):
            lambda function argument string:
              Example: "p HV load >= 2 and (control 1 == 'A' and control 2 != 'S')"
        
          return_case_numbers (bool): If True, not only study case objects, but also study case numbers (indexes) are returned as a tuple.
        
        Returns:
            list[IntCase] | tuple[list[IntCase], list[int]]: study case objects and case numbers (optional)

    `get_study_cases_parent_folder(self) ‑> powfacpy.pf_classes.protocols.IntFolder | powfacpy.pf_classes.protocols.IntPrjfolder`
    :   Get folder where study cases are created.
        
        Returns:
          IntFolder | IntPrjfolder: folder

    `get_value_of_all_parameters_for_case(self, case_obj_or_case_num: powfacpy.pf_classes.protocols.IntCase | int) ‑> list[typing.Any]`
    :   Get the value of all paameters for a specific study case.
        
        Args:
            case_obj_or_case_num (IntCase | int): study case
        
        Returns:
            list[Any]: parameter values

    `get_value_of_parameter_for_case(self, par_name: str, case_obj_or_case_num: powfacpy.pf_classes.protocols.IntCase | int) ‑> Any`
    :   Get parameter value for a certain case.
        
        Note that the values in 'parameter_values' can be
        
        - a list/tuple where each element corresponds to a case number
        - or a single value which is used for all cases
        
        Args:
            par_name (str): Parameter name
        
            case_obj_or_case_num (IntCase | int): Either the case number (int) or
            a study case PF object (then the case number/index is derived first)
        
        Raises:
            PFCaseStudyParameterValueDefinitionError: If a value is not defined for a certain study case
        
        Returns:
            Any: a parameter value for a certain case.

    `get_variations_parent_folder(self) ‑> powfacpy.pf_classes.protocols.IntFolder | powfacpy.pf_classes.protocols.IntPrjfolder`
    :   Get folder where variations are created.
        
        Returns:
            IntFolder | IntPrjfolder: folder

    `set_parent_folders_for_cases_scenarios_variations(self, folder_directory: str = '') ‑> None`
    :   Set the parent folder for the cases, scenarios and variations (if the folders don't exist, a new folder is created).
        
        Args:
            folder_directory (str, optional):
              directory of folders inside study case/scenarios/variations folder of the project. If it is an empty string, the default project folders are used (e.g. app.GetProjectFolder("study"))