import sys
sys.path.insert(0, r'.\src')
import powfacpy


class PFDynSimInterface(powfacpy.PFBaseInterface):
  
  def __init__(self, app): 
    super().__init__(app) 
    

  def initialize_sim(self, param=None):
    """
    Initialize time domain simulation.
    Parameters for 'ComInc' command object can be specified in 'param' dictionary.
    """
    cominc = self.app.GetFromStudyCase("ComInc")
    if param is not None:
      self.set_attr(cominc, param)
    cominc.Execute()

  def run_sim(self, param=None):
    """
    Perform dynamic simulation.
    Parameters for 'ComSim' command object can be specified in 'param' dictionary.
    """
    comsim = self.app.GetFromStudyCase("ComSim")
    if param is not None:
      self.set_attr(comsim, param)
    comsim.Execute()

  def initialize_and_run_sim(self):
    """Initialize and perform time domain simulation."""
    self.initialize_sim()
    self.run_sim()

  
  """
  def create_reference_signal(self, path, points):
    composite_model = self.create_by_path(path + ".ElmComp")
    composite_frame = self.get_obj(self.dynamic_model_teamplates_path +
      r"\reference_signal_frame")
    composite_model.SetAttribute("typ_id", composite_frame)
    dsl_obj = self.create_in_folder(composite_model,"lin_interpol_model.ElmDsl")
    lin_interpol_model = self.get_obj(self.dynamic_model_teamplates_path +
      r"\Linear_interpolation")
    dsl_obj.SetAttribute("typ_id", lin_interpol_model)
    set_dsl_obj_matrix(dsl_obj, points)
    composite_model.SetAttribute("pelm",[dsl_obj])
  """

  def create_event(self, name_incl_class, params={}, parent_folder=None, overwrite=True):
    """Creates an event and sets the parameters in 'params'.
    Arguments:
      name_incl_class: Event name including the class.
      params: Paramter-values dictionary.
      parent_folder: If None, the events folder from the active study case is used.
      overwrite: Oerwrite existing event with same name.
    """
    if not parent_folder:
      parent_folder = self.app.GetFromStudyCase("IntEvt")
    event_obj = self.create_in_folder(parent_folder, name_incl_class, overwrite=overwrite)
    self.set_attr(event_obj, params)  

  def get_dsl_model_parameter_names(self, dsl_model):
    """
    Get the parameter names of the block definition (BlkDef)
    of a dsl model.
    """
    dsl_model = self.handle_single_pf_object_or_path_input(dsl_model)
    try: 
      parameter_names = dsl_model.typ_id.sParams
      if parameter_names:
        return parameter_names[0].split(",")
    except AttributeError:
      msg = "Attribute 'typ_id' is of type 'None'"
      raise powfacpy.PFObjectAttributeTypeError(dsl_model, msg, self)
  
  def get_dsl_models_inside_composite_model(self, composite_model):
    return self.get_obj("*.ElmDsl", 
                        parent_folder=composite_model,
                        include_subfolders=True)
  
  def get_parameters_of_dsl_models_in_composite_model(
      self, 
      composite_model,
      single_dict_for_all_dsl_models = False,
      ):
    """
    Returns a dictionary with the parameter names (of the block definition) 
    and values of all dsl models inside a composite model.
    dsl lookup varibales (e.g. 'array_*', 'omatrix_*',.. ) are ignored.
    
    Arguments:
      composite_model: ElmComp or its path
      single_dict_for_all_dsl_models: 
        - If true, a single dictionary with the parameters of all dsl models is 
        returned (no distinction is made between the dsl models). 
        This assumes that a parameter that occurs in several dsl
        models has the same value.
        Example: {"a": 1, "b":0, "c":2}
        - If false, the returned dictionary contains dictionaries for each dsl model.
        Example:
          {
          "controller_a": {"a": 1, "b":0}
          "controller_b": {"a": 5, "c":2}
          } 
    """
    composite_model = self.handle_single_pf_object_or_path_input(composite_model)
    dsl_models = self.get_dsl_models_inside_composite_model(composite_model)
    all_models_params_dict = {}
    for dsl_model in dsl_models:
      parameter_names_incl_dsl_lookup = self.get_dsl_model_parameter_names(dsl_model)
      # Ignore dsl lookup arrays/matrices
      parameter_names = []
      if parameter_names_incl_dsl_lookup:
        for parameter_name in parameter_names_incl_dsl_lookup:
          if not PFDynSimInterface.is_dsl_lookup_arrays_and_matrices_name(parameter_name):
            parameter_names.append(parameter_name)
              
      if parameter_names:       
        parameter_names_and_values = self.get_attr(
          dsl_model, 
          parameter_names)
        if single_dict_for_all_dsl_models: 
          # Check if 
          for param_name in parameter_names:
            if param_name in all_models_params_dict:
              if all_models_params_dict[param_name] != parameter_names_and_values[param_name]:
                raise powfacpy.PFInconsistentParamValueOfDSLModelInCompositeModel(param_name,
                                                                          composite_model)
          all_models_params_dict = {**all_models_params_dict, 
                                    **parameter_names_and_values}
        else:
          all_models_params_dict[dsl_model.loc_name] = parameter_names_and_values
      elif not single_dict_for_all_dsl_models:
        all_models_params_dict[dsl_model.loc_name] = {}  
    return all_models_params_dict

  def set_parameters_of_dsl_models_in_composite_model(
      self, 
      composite_model,
      models_params_dict,
      single_dict_for_all_dsl_models = False,
      ):
    """
    Set the parameters of the dsl models (i.e. of its block definition) in
    a composite model.
    Arguments:
      composite_model: ElmComp or its path
      models_params_dict: dictionary with model parameters and values
      single_dict_for_all_dsl_models: 
        - If true, models_params_dict is a single dictionary that is used to 
        set the parameters of all dsl models.
        Example: {"a": 1, "b":0, "c":2} -> if a dsl model has an attribute ("a","b",
        "c"), the value is set, otherwise it is ignored.
        - If false, models_params_dict contains dictionaries for each dsl model.
        Example:
          {
          "controller_a": {"a": 1, "b":0}
          "controller_b": {"a": 5, "c":2}
          } 
    """
    composite_model = self.handle_single_pf_object_or_path_input(composite_model)
    if not single_dict_for_all_dsl_models:
      for dsl_model, parameter_value_dict in models_params_dict.items():
        dsl_model = self.get_unique_obj(dsl_model+".ElmDsl", 
                                        parent_folder=composite_model,
                                        include_subfolders=True)
        self.set_attr(dsl_model, parameter_value_dict)
    else:
      dsl_models = self.get_dsl_models_inside_composite_model(composite_model)
      for dsl_model in dsl_models:
        for param_name, value in models_params_dict.items(): 
          if dsl_model.HasAttribute(param_name):
            dsl_model.SetAttribute(param_name, value)   

  @staticmethod
  def is_dsl_lookup_arrays_and_matrices_name(string: str):
    """
    dsl has a special variable type for lookup tables. Such variables
    are defined using certain variable names starting with e.g. 'array_'.
    """
    is_dsl_lookup = False
    for dsl_lookup_name in PFDynSimInterface.get_dsl_lookup_arrays_and_matrices_names():
      if dsl_lookup_name in string:
        is_dsl_lookup = True
    return is_dsl_lookup    

  @staticmethod
  def get_dsl_lookup_arrays_and_matrices_names():
    return ["oarray_", "array_", "matrix", "omatrix"]

  @staticmethod 
  def set_dsl_obj_array(dsl_obj,
                        rows,
                        array_num=None,
                        size_included_in_array=True): 
    """Set the array of a DSL object ('Advanced 1' tab).
    The array_num specifies which array is set (if None,
    all arrays/colums are set).
    If size_included_in_array=True, the first row (where the size
    of the array is specified) is included.
    """  
    if not size_included_in_array:
      if not array_num:
        dsl_obj.SetAttribute("matrix:0",[len(rows)]*len(rows[0]))
      else:
        complete_row = dsl_obj.GetAttribute("matrix:0")
        complete_row[(array_num-1)*2] = len(rows)
        dsl_obj.SetAttribute("matrix:0", complete_row)                                              
    for row_num, row in enumerate(rows):
      if not size_included_in_array:
        attrib = "matrix:" + str(row_num+1)
      else:
        attrib = "matrix:" + str(row_num)
      if not array_num:
        dsl_obj.SetAttribute(attrib, row)
      else:
        complete_row = dsl_obj.GetAttribute(attrib)
        complete_row[(array_num-1)*2] = row[0]
        complete_row[(array_num-1)*2+1] = row[1]
        dsl_obj.SetAttribute(attrib, complete_row)

  @staticmethod 
  def get_dsl_obj_array(dsl_obj,
                        array_num=None,
                        size_included_in_array=True):
    """Get the array of DSL object ('Advanced 1' tab).
    The array_num specifies which array is returend (if None,
    all arays/colmns are returned).
    If size_included_in_array=True, the first row (where the size
    of the array is spedified) is included.
    """                    
    if not array_num:
      number_of_rows = int(max(dsl_obj.GetAttribute("matrix:0"))) + 1
    else:
      number_of_rows = int(dsl_obj.GetAttribute("matrix:0")[(array_num-1)*2]) + 1   
    array = []
    for row_num in range(number_of_rows):
      if row_num == 0 and not size_included_in_array:
        continue
      attrib = "matrix:" + str(row_num)
      row = dsl_obj.GetAttribute(attrib)
      if array_num:
        row = [row[(array_num-1)*2], row[(array_num-1)*2+1]]  
      array.append(row)
    return array
      

if __name__ == "__main__":
  pass
