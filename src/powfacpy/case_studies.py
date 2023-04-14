import sys
sys.path.insert(0, r'.\src')
import powfacpy
from itertools import product

class PFStudyCases(powfacpy.PFBaseInterface):
  language = powfacpy.PFBaseInterface.language

  def __init__(self, app):
    super().__init__(app)
    self.active_grids = None
    self.parameter_values = {}
    self.parameter_paths = {}
    self.delimiter = " "
    self.hierarchy = []
    self.study_cases = []
    self.omitted_combinations = []
    # ToDo base case/scen/var to copy or only base case
    """
    self.parent_folder_study_cases = powfacpy.PFTranslator.get_default_study_case_folder_name(
      self.language)
    self.parent_folder_scenarios = powfacpy.PFTranslator.get_default_operation_scenario_folder_path(
      self.language)
    self.parent_folder_variations = powfacpy.PFTranslator.get_default_variations_folder_path(
      self.language)
    """
    self.parent_folder_study_cases = None
    self.parent_folder_scenarios = None
    self.parent_folder_variations = None
    # Options  
    self.add_scenario_to_each_case = True
    self.add_variation_to_each_case = False
    self.consecutively_number_case_names = False
    self.anonymous_parameters = [] # Paramters of which names are not used 
    # in folder/case names (only their values are used)
    self.ignore_parameters_that_are_none_in_names = True

  def create_cases(self):
    """Create study cases (and corresponding scenarios/variations)
    Iterates through all cases and creates study cases (and folders
    according to 'hierarchy') using parameter-value strings for the
    study cases (and folder names). 
    """
    number_of_cases = len(next(iter(self.parameter_values.values())))
    for case_num in range(number_of_cases):
      folder_path = self.get_folder_path(case_num)
      parameter_values_string = self.get_case_params_value_string(
        case_num, omitted_parameters=self.hierarchy) 
      if self.consecutively_number_case_names:
        parameter_values_string = str(case_num) + " " + parameter_values_string  
      self.study_cases.append(
        self.create_study_case(parameter_values_string, folder_path))
      self.activate_grids(case_num)
      if self.add_scenario_to_each_case:
        scen = self.create_scenario(parameter_values_string, folder_path)
      if self.add_variation_to_each_case:
        self.create_variation(parameter_values_string, folder_path)
      self.set_parameters(case_num)
      if self.add_scenario_to_each_case:
        scen.Save()

  def get_folder_path(self, case_num):
    """Returns the folder path of a case.
    The path corresponds to parameter-value pairs specified
    in 'hierarchy'. 
    """
    if self.hierarchy:
      folder_path = ""
      for par_name in self.hierarchy:
        parameter_value = self.get_value_of_parameter_for_case(par_name, case_num)
        if parameter_value is not None or not self.ignore_parameters_that_are_none_in_names:
          add_to_string = str(parameter_value) + "\\"
          if not par_name in self.anonymous_parameters: 
            add_to_string = par_name + "_" + add_to_string
          folder_path += add_to_string
      if folder_path:   
        return folder_path[:-1] # discard last "\\""
    return None

  def get_value_of_parameter_for_case(self, par_name, case_obj_or_case_num):
    """Returns a parameter value for a certain case.
    Arguments:
      par_name: Parameter name (string)
      case_obj_or_case_num: Either the case number (int) or
        a study case PF object (then the case number/index is derived first)

    Note that the values in 'parameter_values' can be 
      - a list/tuple where each element corresponds to a case number
      - or a single value which is used for all cases
    """
    case_num = self.handle_case_input(case_obj_or_case_num)
    values = self.parameter_values[par_name]
    if isinstance(values,(list, tuple)):
      try:
        return values[case_num]
      except(IndexError):
        raise powfacpy.PFCaseStudyParameterValueDefinitionError(par_name, values)  
    else:
      return values

  def handle_case_input(self, case_obj_or_case_num):
    """Accepts PF study case object or integer.
    If the input is a PF object, the corresponding case number is returned,
    else simply the input (integer) is returned.   
    """
    if not isinstance(case_obj_or_case_num, int):
      return self.study_cases.index(case_obj_or_case_num)
    else:
      return case_obj_or_case_num  

  def get_case_params_value_string(self, case_obj_or_case_num,
    omitted_parameters=None,
    delimiter=None,
    equals_sign=None,
    anonymous_parameters=None):
    """Returns the parameter-value string for a case name.
    """
    case_num = self.handle_case_input(case_obj_or_case_num)
    if not delimiter:
      delimiter = self.delimiter
    if not equals_sign:
      equals_sign = " _ "   
    parameter_values_string = ""
    for par_name in self.parameter_values.keys():
      if omitted_parameters is None or par_name not in omitted_parameters:
        par_value = self.get_value_of_parameter_for_case(par_name, case_num)
        if par_value is not None or not self.ignore_parameters_that_are_none_in_names:
          add_to_string = str(par_value) + delimiter
          if anonymous_parameters is None:
            if par_name not in self.anonymous_parameters:
              add_to_string = par_name + equals_sign + add_to_string
          elif par_name not in anonymous_parameters:
            add_to_string = par_name + equals_sign + add_to_string 
          parameter_values_string += add_to_string
    return parameter_values_string[:-len(delimiter)] # discard last delimiter

  def create_study_case(self, name, folder_path):
    """Creates a study case with the name 'parameter_values_string'
    in the folder corresponding to 'folder_path' (this path is 
    relativ to 'parent_folder_study_cases)
    """
    parent_folder_study_case = self.get_study_cases_parent_folder() 
    if folder_path:
      parent_folder_study_case = self.create_directory(folder_path,
        parent_folder=parent_folder_study_case)
    study_case_obj = self.create_in_folder(parent_folder_study_case,
      name+".IntCase")
    study_case_obj.Activate()
    pfpi = powfacpy.PFPlotInterface(self.app)
    self.app.GetFromStudyCase("SetDesktop")
    return study_case_obj

  def create_scenario(self, parameter_values_string, folder_path): 
    """Creates a scenario with the name 'parameter_values_string'
    in the folder corresponding to 'folder_path' (this parth is 
    relativ to 'parent_folder_scenarios)
    """
    parent_folder_scenario = self.get_scenarios_parent_folder()
    if folder_path:
      parent_folder_scenario = self.create_directory(folder_path,
        parent_folder=parent_folder_scenario)       
    scenario_obj = self.create_in_folder(parent_folder_scenario,
      parameter_values_string+".IntScenario")
    scenario_obj.Activate()
    scenario_obj.Save()
    return scenario_obj

  def create_variation(self, parameter_values_string, folder_path):
    """Creates a variation with the name 'parameter_values_string'
    in the folder corresponding to 'folder_path' (this path is 
    relativ to 'parent_folder_variations)
    """ 
    parent_folder_variation = self.get_variations_parent_folder()
    if folder_path:
      parent_folder_variation = self.create_directory(folder_path,
        parent_folder=parent_folder_variation)
    variation_obj = self.create_in_folder(parent_folder_variation,
      parameter_values_string+".IntScheme")
    variation_obj.NewStage(parameter_values_string,0,1)
    variation_obj.Activate()
    return variation_obj

  def activate_grids(self, case_num):
    """Activate the corresponding grids of a study case.
    If 'active_grids' is a list/tuple, the elements correspond to
    each study case. If multiple grids are active, list/tuples can be 
    used in the elements in 'active_grids'. 
    If 'active_grid' is not a list/tuple, than one gird will be used
    for all cases.
    The grids can be thir paths or PF objects.
    """
    if isinstance(self.active_grids,(list, tuple)):
      grids = self.active_grids[case_num]
      if not isinstance(grids,(list, tuple)):
          grids = [grids]
      for grid in grids:
          grid = self.handle_single_pf_object_or_path_input(grid)
          grid.Activate()
    elif self.active_grids:
      grid = self.handle_single_pf_object_or_path_input(self.active_grids)
      grid.Activate() 

  def set_parameters(self, case_obj_or_case_num):
    """Set the parameters according to paths specified in 'parameter_paths'
    and values specified in 'parameter_values'. 
    """
    case_num = self.handle_case_input(case_obj_or_case_num)
    for par_name, path in self.parameter_paths.items():
      value = self.get_value_of_parameter_for_case(par_name, case_num)
      if value:
        self.set_attr_by_path(path, value)  

  def get_study_cases(self, conditions):
    """Retrieve study case objects depending on parameter values.
    Arguments:
      conditions: A dictionary with
        keys: parameter names
        values: lambda function with boolean return value depending on 
          parameter (key)
    Returns the study case objects whose parameters fullfill the conditions.

    Example:
      get_study_cases({"par1": lambda x: x == 2, "par2": lambda x: x>0})
        This returns the study cases for which 'par1' equals 2 and 'par2' is 
        positive.       
    """
    cases = []
    for case_num, case_obj in enumerate(self.study_cases):
      conditions_fullfiled = True
      for parameter, condition in conditions.items():
        if not condition(self.get_value_of_parameter_for_case(parameter, case_num)):
          conditions_fullfiled = False
          break
      if conditions_fullfiled:
        cases.append(case_obj)
    return cases

  def apply_permutation(self,omitted_combinations=None):
    """Replaces the values in 'parameter_values' with the permutation of
    their unique elements. 
    Use this method if you want to create cases of the permutation of all
    parameters. Note that 'parameter_values' is changed irreversibly.
    """
    # Make sure values are unique
    for param_name in self.parameter_values.keys():
      self.parameter_values[param_name] = list(
        set(self.parameter_values[param_name]))
    # Use 'product' to get iterable that returns permutation    
    permutation_iterable = product(*self.parameter_values.values())
    # Clear values
    original_parameter_values =  self.parameter_values
    for param_name in self.parameter_values.keys():
        self.parameter_values[param_name] = []
    # Copy values from iterable    
    for values_of_all_parameters_for_case in permutation_iterable:
      if omitted_combinations:
        values_of_all_parameters_for_case = self.filter_omitted_combinations(
          values_of_all_parameters_for_case,omitted_combinations,original_parameter_values)
      if values_of_all_parameters_for_case:    
        for param_num, param_name in enumerate(self.parameter_values.keys()):
          self.parameter_values[param_name].append(
            values_of_all_parameters_for_case[param_num])

  def filter_omitted_combinations(
      self,
      values_of_all_parameters_for_case,
      omitted_combinations,
      original_parameter_values):
    """Filter the parameter combinations that should be omitted. 
    The difficulty is the handling of the 'all' case. In this case, the combination
    with any value of a parameter is omitted, but combinations with the other parameters
    must be allowed
    """
    # Create list from tuple because values might be changed/set to 'None'
    values_of_all_parameters_for_case = list(values_of_all_parameters_for_case)
    for omitted_combination_dict in omitted_combinations:
      is_omitted_combination = True
      for param_num, param_name in enumerate(self.parameter_values.keys()):
        if param_name in omitted_combination_dict:
          if omitted_combination_dict[param_name] == "all":
            # If the parameter is 'all', then only one case should be created. The case where
            # the value of the parameter takes on the value of the first entry in 
            # original_parameter_values[param_name][0] is selected. This must be the case for all
            # parameters that are set to 'all'
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

  def get_study_cases_parent_folder(self):
    if not self.parent_folder_study_cases:
      return self.app.GetProjectFolder("study")
    else:
      return self.parent_folder_study_cases

  def get_scenarios_parent_folder(self):
    if not self.parent_folder_scenarios:
      return self.app.GetProjectFolder("scen")
    else:
      return self.parent_folder_scenarios  

  def get_variations_parent_folder(self):
    if not self.parent_folder_variations:
      return self.app.GetProjectFolder("scheme")
    else:
      return self.parent_folder_variations       

  def clear_parent_folders(self):
    """Deletes all objects in the folders
      - self.parent_folder_study_cases
      - self.parent_folder_scenarios
      - self.parent_folder_variations
    if theses attributes are defined.  
    """
    parent_folders = [
      self.get_study_cases_parent_folder(),
      self.get_scenarios_parent_folder(),
      self.get_variations_parent_folder(),
    ]
    for parent_folder in parent_folders:
      if parent_folder:
        self.delete_obj("*",
          parent_folder=parent_folder,
          error_if_non_existent=False,
          include_subfolders=True)  

