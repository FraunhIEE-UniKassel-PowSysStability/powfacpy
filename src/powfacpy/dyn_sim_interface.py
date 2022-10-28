import sys
sys.path.insert(0,r'.\src')
import powfacpy


class PFDynSimInterface(powfacpy.PFBaseInterface):
  
  def __init__(self,app): 
    super().__init__(app) 
    

  def initialize_sim(self,param=None):
    """
    Initialize time domain simulation.
    Parameters for 'ComInc' command object can be specified in 'param' dictionary.
    """
    cominc = self.app.GetFromStudyCase("ComInc")
    if param is not None:
      self.set_attr(cominc,param)
    cominc.Execute()

  def run_sim(self,param=None):
    """
    Perform dynamic simulation.
    Parameters for 'ComSim' command object can be specified in 'param' dictionary.
    """
    comsim = self.app.GetFromStudyCase("ComSim")
    if param is not None:
      self.set_attr(comsim,param)
    comsim.Execute()

  def initialize_and_run_sim(self):
    """Initialize and perform time domain simulation."""
    self.initialize_sim()
    self.run_sim()

  
  """
  def create_reference_signal(self,path,points):
    composite_model = self.create_by_path(path + ".ElmComp")
    composite_frame = self.get_obj(self.dynamic_model_teamplates_path +
      r"\reference_signal_frame")
    composite_model.SetAttribute("typ_id",composite_frame)
    dsl_obj = self.create_in_folder(composite_model,"lin_interpol_model.ElmDsl")
    lin_interpol_model = self.get_obj(self.dynamic_model_teamplates_path +
      r"\Linear_interpolation")
    dsl_obj.SetAttribute("typ_id",lin_interpol_model)
    set_dsl_obj_matrix(dsl_obj,points)
    composite_model.SetAttribute("pelm",[dsl_obj])
  """

  def create_event(self,name_incl_class,params={},parent_folder=None,overwrite=True):
    """Creates an event and sets the parameters in 'params'.
    Arguments:
      name_incl_class: Event name including the class.
      params: Paramter-values dictionary.
      parent_folder: If None, the events folder from the active study case is used.
      overwrite: Oerwrite existing event with same name.
    """
    if not parent_folder:
      parent_folder = self.app.GetFromStudyCase("IntEvt")
    event_obj = self.create_in_folder(parent_folder,name_incl_class,overwrite=overwrite)
    self.set_attr(event_obj,params)  

  @staticmethod 
  def set_dsl_obj_array(dsl_obj,
                        rows,
                        array_num=None,
                        size_included_in_array=True): 
    """Set the array of DSL object ('Advanced 1' tab).
    The array_num specifies which array is set (if None,
    all arrays/colums are set).
    If size_included_in_array=True, the first row (where the size
    of the array is spedified) is included.
    """  
    if not size_included_in_array:
      if not array_num:
        dsl_obj.SetAttribute("matrix:0",[len(rows)]*len(rows[0]))
      else:
        complete_row = dsl_obj.GetAttribute("matrix:0")
        complete_row[(array_num-1)*2] = len(rows)
        dsl_obj.SetAttribute("matrix:0",complete_row)                                              
    for row_num,row in enumerate(rows):
      if not size_included_in_array:
        attrib = "matrix:" + str(row_num+1)
      else:
        attrib = "matrix:" + str(row_num)
      if not array_num:
        dsl_obj.SetAttribute(attrib,row)
      else:
        complete_row = dsl_obj.GetAttribute(attrib)
        complete_row[(array_num-1)*2] = row[0]
        complete_row[(array_num-1)*2+1] = row[1]
        dsl_obj.SetAttribute(attrib,complete_row)

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
        row = [row[(array_num-1)*2],row[(array_num-1)*2+1]]  
      array.append(row)
    return array
      

if __name__ == "__main__":
  pass