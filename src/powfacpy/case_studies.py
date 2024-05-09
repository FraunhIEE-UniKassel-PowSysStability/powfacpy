from typing import Any, Callable
from itertools import product
from os import getcwd, makedirs
from os.path import join

import powfacpy
from powfacpy.pf_class_protocols import ElmNet, IntCase, IntScenario, ElmRes, IntFolder, IntPrjfolder, IntScheme


class PFStudyCases(powfacpy.PFActiveProject):

    def __init__(self, app):
        super().__init__(app)

        self.title: str = "Case_Studies"
        "Title of the case studies."

        # Study Cases Definition
        self.active_grids: ElmNet | list[ElmNet | list[ElmNet]] = None
        "Active grids for each study case (can be multiple for each). If only one is given, the same grid is active in every case."
        self.parameter_values: dict[str, list[Any]] = {}
        "Dictionary with parameters names (keys) and lists with parameter values for each case (values)."
        self.parameter_paths: dict[str, str] = {}
        "Dictionary with parameter names (keys) and their path."
        self.hierarchy: list[str] = []
        "Hierarchy of folders (named after the parameters) where case/scenario/varaition objects are located."
        self.omitted_combinations: list[dict[str, list]] = []
        "Omitted parameter combinations (in permutation)."
        self.base_study_case: IntCase | str = None
        "Base study case (or its path) which is copied to create the cases."
        self.parent_folder_study_cases: IntFolder | IntPrjfolder = None
        "Parent folder where study cases are created."
        self.parent_folder_scenarios: IntFolder | IntPrjfolder = None
        "Parent folder where scenarios are created."
        self.parent_folder_variations: IntFolder | IntPrjfolder = None
        "Parent folder where variations are created."

        # Options
        self.add_scenario_to_each_case: bool = True
        "If True, a corresponding scenario is created for each case."
        self.add_variation_to_each_case: bool = False
        "If True, a corresponding variation is created for each case."
        self.consecutively_number_case_names: bool = False
        "If True, numbering is added to the case names."
        self.anonymous_parameters: list[str] = []
        "Parameters for which names are not used in folder/case name strings (only the parameter values are used)."
        self.ignore_parameters_that_are_none_in_names: bool = True
        "If True, parameters with value None are ignored in names (of cases etc.)."
        self.overwrite_study_cases: bool = True
        "If True, existing study cases are overwriten (e.g. when calling 'create_case' one more time with the same settings)."
        self.delimiter: str = " "
        "Default delimiter used in parameter-value strings."

        # Autocreated
        self._study_cases: list[IntCase] = []
        "List of created study case objects when calling 'create_cases'."

    @property
    def study_cases(self) -> list[IntCase]:
        """List of created study case objects when calling 'create_cases' (read-only).
        """
        return self._study_cases

    def create_cases(self) -> None:
        """Create study cases.

        Optionally create corresponding scenarios/variations (if add_scenario_to_each_case/add_variation_to_each_case is True).

        Iterates through all cases and creates study cases (and folders
        according to 'hierarchy') using parameter-value strings for the
        study cases (and folder names). 
        """
        self._study_cases = []
        number_of_cases = len(next(iter(self.parameter_values.values())))
        if self.base_study_case:
            self.base_study_case = self._handle_single_pf_object_or_path_input(
                self.base_study_case)
        for case_num in range(number_of_cases):
            folder_path = self.get_folder_path(case_num)
            parameter_values_string = self.get_case_params_value_string(
                case_num, omitted_parameters=self.hierarchy)
            if self.consecutively_number_case_names:
                parameter_values_string = str(
                    case_num) + " " + parameter_values_string
            self._study_cases.append(
                self._create_study_case(parameter_values_string, folder_path))
            self.activate_grids(case_num)
            if self.add_scenario_to_each_case:
                scen = self._create_scenario(
                    parameter_values_string, folder_path)
            if self.add_variation_to_each_case:
                self._create_variation(parameter_values_string, folder_path)
            self._set_parameters(case_num)
            if self.add_scenario_to_each_case:
                scen.Save()

    def get_folder_path(self, case_num: int) -> str | None:
        """Get folder path (inside parent folder) of a case.

        The path corresponds to parameter-value pairs specified
        in 'self.hierarchy'.

        Args:
          case_num (int): case number

        Returns:
          str | None: path of study case or None if there is no hierarchy    
        """
        if self.hierarchy:
            folder_path = ""
            for par_name in self.hierarchy:
                parameter_value = self.get_value_of_parameter_for_case(
                    par_name, case_num)
                if parameter_value is not None or not self.ignore_parameters_that_are_none_in_names:
                    add_to_string = str(parameter_value) + "\\"
                    if not par_name in self.anonymous_parameters:
                        add_to_string = par_name + "_" + add_to_string
                    folder_path += add_to_string
            if folder_path:
                return folder_path[:-1]  # discard last "\\""
        return None

    def get_value_of_parameter_for_case(self,
                                        par_name: str,
                                        case_obj_or_case_num: IntCase | int) -> Any:
        """Get parameter value for a certain case.

        Note that the values in 'parameter_values' can be 

          - a list/tuple where each element corresponds to a case number

          - or a single value which is used for all cases

        Args:
            par_name (str): Parameter name

            case_obj_or_case_num (IntCase | int): Either the case number (int) or
            a study case PF object (then the case number/index is derived first)

        Raises:
            powfacpy.PFCaseStudyParameterValueDefinitionError: If a value is not defined for a certain study case

        Returns:
            Any: a parameter value for a certain case.
        """
        case_num = self._handle_case_input(case_obj_or_case_num)
        values = self.parameter_values[par_name]
        if isinstance(values, (list, tuple)):
            try:
                return values[case_num]
            except (IndexError):
                raise powfacpy.PFCaseStudyParameterValueDefinitionError(
                    par_name, values)
        else:
            return values

    def get_value_of_all_parameters_for_case(
            self,
            case_obj_or_case_num: IntCase | int) -> list[Any]:
        """Get the value of all paameters for a specific study case.

        Args:
            case_obj_or_case_num (IntCase | int): study case

        Returns:
            list[Any]: parameter values
        """
        parameter_values = []
        case_num = self._handle_case_input(case_obj_or_case_num)
        for par_name in self.parameter_values.keys():
            parameter_values.append(
                self.get_value_of_parameter_for_case(par_name, case_num))
        return parameter_values

    def get_case_params_value_string(
            self,
            case_obj_or_case_num: IntCase | int,
            omitted_parameters: list[str] = None,
            delimiter: str = None,
            equals_sign: str = None,
            anonymous_parameters: list[str] = None) -> str:
        """Get parameter-value string for a case

        Args:
            case_obj_or_case_num (IntCase | int): study case

            omitted_parameters (list[str], optional): parameters will not be considered. Defaults to None.

            delimiter (str, optional): delimiter between parameter value pairs. Defaults to None.

            equals_sign (str, optional): sign between parameter name and value. Defaults to None.

            anonymous_parameters (list[str], optional): only the value of these parameters will be added (not their name). Defaults to None.

        Returns:
            str: Parameters and their values
        """
        case_num = self._handle_case_input(case_obj_or_case_num)
        if not delimiter:
            delimiter = self.delimiter
        if not equals_sign:
            equals_sign = " _ "
        parameter_values_string = ""
        for par_name in self.parameter_values.keys():
            if omitted_parameters is None or par_name not in omitted_parameters:
                par_value = self.get_value_of_parameter_for_case(
                    par_name, case_num)
                if par_value is not None or not self.ignore_parameters_that_are_none_in_names:
                    add_to_string = str(par_value) + delimiter
                    if anonymous_parameters is None:
                        if par_name not in self.anonymous_parameters:
                            add_to_string = par_name + equals_sign + add_to_string
                    elif par_name not in anonymous_parameters:
                        add_to_string = par_name + equals_sign + add_to_string
                    parameter_values_string += add_to_string
        # discard last delimiter
        return parameter_values_string[:-len(delimiter)]

    def activate_grids(self, case_num: int) -> None:
        """Activate the corresponding grids of a study case.

        If 'self.active_grids' is a list/tuple, the items correspond to
        each study case. If multiple grids are active for a case, list/tuples can be used in the elements in 'active_grids'. 
        If 'self.active_grid' is not a list/tuple, then one grid will be used
        for all cases.

        The grids can be thier paths or PF objects.
        """
        if isinstance(self.active_grids, (list, tuple)):
            grids = self.active_grids[case_num]
            if not isinstance(grids, (list, tuple)):
                grids = [grids]
            for grid in grids:
                grid = self._handle_single_pf_object_or_path_input(grid)
                grid.Activate()
        elif self.active_grids:
            grid = self._handle_single_pf_object_or_path_input(
                self.active_grids)
            grid.Activate()

    def set_parent_folders_for_cases_scenarios_variations(
            self, folder_directory: str = "") -> None:
        """Set the parent folder for the cases, scenarios and variations (if the folders don't exist, a new folder is created).

        Args:
            folder_directory (str, optional): 
              directory of folders inside study case/scenarios/variations folder of the project. If it is an empty string, the default project folders are used (e.g. app.GetProjectFolder("study"))
        """
        if folder_directory:
            self.parent_folder_study_cases = self.create_directory(
                folder_directory, self.app.GetProjectFolder("study"))
            self.parent_folder_scenarios = self.create_directory(
                folder_directory, self.app.GetProjectFolder("scen"))
            self.parent_folder_variations = self.create_directory(
                folder_directory, self.app.GetProjectFolder("scheme"))
        else:
            self.parent_folder_study_cases = self.app.GetProjectFolder("study")
            self.parent_folder_scenarios = self.app.GetProjectFolder("scen")
            self.parent_folder_scenarios = self.app.GetProjectFolder("scheme")

    def get_study_cases_parent_folder(self) -> IntFolder | IntPrjfolder:
        """Get folder where study cases are created.

        Returns:
          IntFolder | IntPrjfolder: folder
        """
        if not self.parent_folder_study_cases:
            return self.app.GetProjectFolder("study")
        else:
            return self.parent_folder_study_cases

    def get_scenarios_parent_folder(self) -> IntFolder | IntPrjfolder:
        """Get folder where scenarios are created.

        Returns:
            IntFolder | IntPrjfolder: folder
        """
        if not self.parent_folder_scenarios:
            return self.app.GetProjectFolder("scen")
        else:
            return self.parent_folder_scenarios

    def get_variations_parent_folder(self) -> IntFolder | IntPrjfolder:
        """Get folder where variations are created.

        Returns:
            IntFolder | IntPrjfolder: folder
        """
        if not self.parent_folder_variations:
            return self.app.GetProjectFolder("scheme")
        else:
            return self.parent_folder_variations

    def clear_parent_folders(self):
        """Deletes all objects in the folders returned by
          - self.get_study_cases_parent_folder
          - self.get_scenarios_parent_folder
          - self.get_variations_parent_folder 
        """
        parent_folders = [
            self.get_study_cases_parent_folder(),
            self.get_scenarios_parent_folder(),
            self.get_variations_parent_folder(),
        ]
        for parent_folder in parent_folders:
            if parent_folder:
                self.clear_folder(parent_folder)

    def get_study_cases(
            self,
            conditions: dict[str, Callable] | Callable,
            return_case_numbers: bool = False) -> list[IntCase] | tuple[list[IntCase], list[int]]:
        """Retrieve study case objects depending on parameter values.

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
        """
        cases_objects = []
        if return_case_numbers:
            case_numbers = []
        # Dictionary with conditions for parameters
        if isinstance(conditions, dict):
            for case_num, case_obj in enumerate(self._study_cases):
                conditions_fullfiled = True
                for parameter, condition in conditions.items():
                    if not condition(self.get_value_of_parameter_for_case(parameter, case_num)):
                        conditions_fullfiled = False
                        break
                if conditions_fullfiled:
                    cases_objects.append(case_obj)
                    if return_case_numbers:
                        case_numbers.append(case_num)
        # Callables (e.g. lambda function for all parameters)
        elif callable(conditions):
            for case_num, case_obj in enumerate(self._study_cases):
                parameter_values = self.get_value_of_all_parameters_for_case(
                    case_num)
                if conditions(parameter_values):
                    cases_objects.append(case_obj)
                    if return_case_numbers:
                        case_numbers.append(case_num)
        else:
            raise ValueError("conditions must be a dictionary or a callable.")
        if not return_case_numbers:
            return cases_objects
        else:
            return cases_objects, case_numbers

    def get_study_cases_from_string(
            self,
            conditions: str,
            return_case_numbers: bool = False) -> list[IntCase] | tuple[list[IntCase], list[int]]:
        """This method is another convenient way to get study cases according to conditions. The conditions are a simple lambda function argument string (see example below). This method is more convenient but less safe than 'self.get_study_cases' because the conditions string is evaluated and a lambda function is created from it. Using eval() statements is generally not recommended due to unforeseeable behavior.
        However, for convenience, it is used here.

        Args:
          conditions (str): 
            lambda function argument string: 
              Example: "p HV load >= 2 and (control 1 == 'A' and control 2 != 'S')"

          return_case_numbers (bool): If True, not only study case objects, but also study case numbers (indexes) are returned as a tuple.  

        Returns:
            list[IntCase] | tuple[list[IntCase], list[int]]: study case objects and case numbers (optional)    
        """
        # To create a lambda function from the conditions string, the parameter names need to be replaced by proper python variable names (e.g. "p HV load" is not a proper variable name because of the spaces). Therefore, a dict with the mapping  from parameter names to a list is required (e.g. {"p HV load": x[0],..})
        par_name_to_list_mapping = self._get_parameter_name_to_list_mapping()
        # Then the parameter names are replaced in conditions. Note that there could be strings inside conditions which should not be considered: For example, if there is condition "control == 'control A'", then only the parameter name 'control' should be replaced, not the value 'control A' which also contains 'control', i.e x[0] == 'control A'.
        condition_strings_list = powfacpy.PFStringManipulation.replace_outside_or_inside_of_strings_in_a_string(
            conditions, par_name_to_list_mapping)
        lambda_fun = "lambda x: " + "".join(condition_strings_list).strip()
        # Going back to example in the docstring, we now have a lambda function string that can be executed: "lambda x: x[0] >= 2 and (x[1] == 'A' and x[2] != 'S')"
        lambda_fun = eval(lambda_fun)
        cases = self.get_study_cases(
            lambda_fun, return_case_numbers=return_case_numbers)
        return cases

    def get_study_case_number(self, study_case: IntCase) -> int:
        """Get the number (index) of a study case object.
        """
        return self._study_cases.index(study_case)

    def apply_permutation(
            self,
            omitted_combinations: list[dict[str, list]] = None) -> None:
        """Replaces the values in 'parameter_values' with the permutation of
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
        """
        if omitted_combinations:
            self.omitted_combinations = omitted_combinations
        # Make sure values are unique
        for param_name in self.parameter_values.keys():
            self.parameter_values[param_name] = list(
                set(self.parameter_values[param_name]))
        # Use 'product' to get iterable that returns permutation
        permutation_iterable = product(*self.parameter_values.values())
        # Clear values
        original_parameter_values = self.parameter_values.copy()
        for param_name in self.parameter_values.keys():
            self.parameter_values[param_name] = []
        # Copy values from iterable
        for values_of_all_parameters_for_case in permutation_iterable:
            if self.omitted_combinations:
                values_of_all_parameters_for_case = self._filter_omitted_combinations(
                    values_of_all_parameters_for_case,
                    original_parameter_values)
            if values_of_all_parameters_for_case:
                for param_num, param_name in enumerate(self.parameter_values.keys()):
                    self.parameter_values[param_name].append(
                        values_of_all_parameters_for_case[param_num])

    def export_results_of_study_cases_to_csv(
            self,
            export_dir: str = None,
            study_cases: list[IntCase] = None,
            case_numbers: list[int] = None,
            results_obj: str = "ElmRes",
            results_variables: list[str] = None,
            format_csv_file=True) -> list[str]:
        """Export the simulation results (ElmRes) of the study cases to csv files. 
        The csv files are named according to the study case number (e.g. case0.csv, case1.csv,..)
        Returns the full paths of the csv files.

        Arguments:
          - export_dir: directory for export (default is working directory)
          - study_cases: study case objects
          - case_numbers: corresponing study case numbers
          - results_obj: string that is used in GetFromStudyCase to get the ElmRes object (e.g. 
            'self.app.GetFromStudyCase("ElmRes")' )
          - results_variables: if only specific variables should be export (see also 
              export_to_csv). By default all variables are exported.
          - format_csv_file: see export_to_csv    
        """
        study_cases, case_numbers = self._handle_study_case_objects_case_numbers_input(
            study_cases=study_cases,
            case_numbers=case_numbers)

        if not export_dir:
            export_dir = getcwd() + "\\" + self.title
        makedirs(export_dir, exist_ok=True)

        csv_files_full_paths = []
        pfri = powfacpy.PFResultsInterface(self.app)
        for case_num, case in zip(case_numbers, study_cases):
            case.Activate()
            elmres: ElmRes = self.app.GetFromStudyCase(results_obj)
            case_file_name = "case" + str(case_num)
            pfri.export_to_csv(
                export_dir,
                case_file_name,
                elmres,
                variables=results_variables,
                format_csv_file=format_csv_file)
            csv_files_full_paths.append(
                join(export_dir, case_file_name + ".csv"))
        return csv_files_full_paths

    def _handle_case_input(self, case_obj_or_case_num: IntCase | int) -> int:
        """Handle PF study case object (IntCase) or case number (int) input and return the case number.

        If the input is a PF object, the corresponding case number is returned,
        else simply the input (integer) is returned.

        Args:
            case_obj_or_case_num (IntCase | int): study case object (IntCase) or case number (int)

        Returns:
            int: case number
        """
        if not isinstance(case_obj_or_case_num, int):
            return self._study_cases.index(case_obj_or_case_num)
        else:
            return case_obj_or_case_num

    def _create_study_case(self, name: str, folder_path: str) -> IntCase:
        """Create a study case in the folder under 'folder_path'.

        Args:
            name (str): name of study case object without class (e.g. parameter-value pairs)

            folder_path (str): relativ to 'self.get_study_cases_parent_folder'

        Returns:
            IntCase: Created study case object
        """
        parent_folder_study_case = self.get_study_cases_parent_folder()
        if folder_path:
            parent_folder_study_case = self.create_directory(folder_path,
                                                             parent_folder=parent_folder_study_case)
        if not self.base_study_case:
            study_case_obj = self.create_in_folder(
                name + ".IntCase",
                parent_folder_study_case,
                overwrite=self.overwrite_study_cases)
        else:
            study_case_obj = self.copy_single_obj(
                self.base_study_case,
                parent_folder_study_case,
                overwrite=self.overwrite_study_cases,
                new_name=name)
        study_case_obj.Activate()
        self.app.GetFromStudyCase("SetDesktop")
        return study_case_obj

    def _create_scenario(self,
                         name: str,
                         folder_path: str) -> IntScenario:
        """Create scenario in folder under 'folder_path'.

        Args:
            name (str): name of scenaeio (e.g. parameter-value pairs)

            folder_path (str): relativ to 'self.get_scenarios_parent_folder'

        Returns:
            IntScenario: Created scenario
        """
        parent_folder_scenario = self.get_scenarios_parent_folder()
        if folder_path:
            parent_folder_scenario = self.create_directory(folder_path,
                                                           parent_folder=parent_folder_scenario)
        scenario_obj: IntScenario = self.create_in_folder(
            name+".IntScenario", parent_folder_scenario)
        scenario_obj.Activate()
        scenario_obj.Save()
        return scenario_obj

    def _create_variation(self, name: str, folder_path: str) -> IntScheme:
        """Create variation with the name 'name' in folder under 'folder_path.

        Args:
            name (str): name of variation (e.g. parameter value pairs)
            folder_path (str): relativ to 'self.get_variations_parent_folder'

        Returns:
            IntScheme: Created variation
        """
        parent_folder_variation = self.get_variations_parent_folder()
        if folder_path:
            parent_folder_variation = self.create_directory(folder_path,
                                                            parent_folder=parent_folder_variation)
        variation_obj = self.create_in_folder(
            name+".IntScheme", parent_folder_variation)
        variation_obj.NewStage(name, 0, 1)
        variation_obj.Activate()
        return variation_obj

    def _set_parameters(self, case_obj_or_case_num: IntCase | int):
        """Set the parameters according to paths specified in 'self.parameter_paths'
        and values specified in 'self.parameter_values'. 
        """
        case_num = self._handle_case_input(case_obj_or_case_num)
        for par_name, path in self.parameter_paths.items():
            value = self.get_value_of_parameter_for_case(par_name, case_num)
            if value is not None:
                self.set_attr_by_path(path, value)

    def _filter_omitted_combinations(
            self,
            values_of_all_parameters_for_case: list | tuple,
            original_parameter_values: dict[str, Any]) -> list | None:
        """Filter the parameter combinations that should be omitted. Returns the parameters if the combination is not omitted, otherwise returns None.

        The difficulty is the handling of the 'all' case. In this case, the combination with any value of a parameter is omitted, but combinations of the remaining parameters must be allowed.

        Args:
            values_of_all_parameters_for_case (list | tuple): paramert values for specific case

            original_parameter_values (dict[str, Any]): original values BEFORE permutation is applied.

        Returns:
            list | None: parameters if the combination is not omitted, otherwise returns None
        """
        # Create list from tuple because values might be changed/set to 'None'
        values_of_all_parameters_for_case = list(
            values_of_all_parameters_for_case)
        for omitted_combination_dict in self.omitted_combinations:
            is_omitted_combination = True
            for param_num, param_name in enumerate(self.parameter_values.keys()):
                if param_name in omitted_combination_dict:
                    if omitted_combination_dict[param_name] == "all":
                        # If the parameter is 'all', then only one case should be created. The case where the value of the parameter takes on the value of the first entry in  original_parameter_values[param_name] is selected. This must be the case for all parameters that are set to 'all'
                        if not (original_parameter_values[param_name][0] ==
                                values_of_all_parameters_for_case[param_num]):
                            return False
                        else:
                            is_omitted_combination = False
                            values_of_all_parameters_for_case[param_num] = None
                    elif not values_of_all_parameters_for_case[param_num] in omitted_combination_dict[param_name]:
                        is_omitted_combination = False
                        break
            if is_omitted_combination:
                return False
        return values_of_all_parameters_for_case

    def _get_parameter_name_to_list_mapping(self) -> dict[str, str]:
        """Returns a dictionary that maps the parameters to a string with a list including indexing.

        Example:
          If there are two parameters "p HV load" and "control 1",
          the dictionary is
          {"p HV load": "x[0]", "control 1": "x[1]"}
          {"p HV load": "x[0]", "control 1": "x[1]"}
        """
        par_name_to_list_mapping = {}
        for par_num, par_name in enumerate(self.parameter_values.keys()):
            par_name_to_list_mapping[par_name] = "x[" + str(par_num) + "]"
        return par_name_to_list_mapping

    def _handle_study_case_objects_case_numbers_input(
            self,
            study_cases: list[IntCase] = None,
            case_numbers: list[int] = None):
        """Handles input for study case objects and case numbers/indexes.
        Always returns BOTH study case objects and case numbers, independent from
        the input.
        Arguments:
          If only study_cases are provided, case_numbers are inferred.
          If only case_numbers are provided, study_cases are inferred.
          If none are provided, all study cases and case_numbers are returned.
        """
        if not study_cases and not case_numbers:
            # Use all study cases
            study_cases = self._study_cases
            case_numbers = range(len(study_cases))
        elif not case_numbers:
            case_numbers = [self.get_study_case_number(
                case) for case in study_cases]
        elif not study_cases:
            study_cases = [self._study_cases[case_num]
                           for case_num in case_numbers]
        return study_cases, case_numbers
