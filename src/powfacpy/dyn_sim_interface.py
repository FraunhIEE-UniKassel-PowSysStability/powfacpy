import itertools
import sys
import pathlib


sys.path.insert(0,r'.\src')
import powfacpy
import pandas
from os import getcwd, replace

class PFDynSimInterface(powfacpy.PFBaseInterface):
  
  def __init__(self,app): 
    super().__init__(app) 
    self.export_dir = None

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

  def export_to_csv(self,dir=None,file_name=None,results_obj=None):
    """Exports simulation results to csv.
    Arguments:
      dir: export directory, if 'None' the current working directory 
        (where script is run) is used 
      file_name: file name, if 'None', 'results' is used
      results_obj: PF ElmRes object, if 'None', 'All calculations.ElmRes' in
        active study case is used. All variables from this object are exported.
    """
    comres = self.app.GetFromStudyCase("ComRes")
    if not results_obj:
      results_obj_name = powfacpy.PFTranslator.get_default_result_object_name(self.language)
      comres.pResult = self.app.GetFromStudyCase(results_obj_name)
    else:
      comres.pResult = self.handle_single_pf_object_or_path_input(results_obj)
    if not dir:
      if self.export_dir:
        dir = self.export_dir
      else:
        # Use current working directory (where script is run)
        dir = getcwd()
    if not file_name:  
      file_name = "results"  
    comres.iopt_exp = 6 # to export as csv
    path = dir + "\\" + file_name + ".csv"
    comres.f_name = path
    comres.iopt_sep = 1 # to use the system seperator
    comres.iopt_honly = 0 # to export data and not only the header
    comres.iopt_csel = 0 # export all variables 
    comres.iopt_locn = 3 # column header includes path
    comres.ciopt_head = 1 # full variable name
    comres.Execute()
    try:
      self.format_csv(path)
    except(IndexError):
      raise Exception(f"Is the file \n" 
        f"'{path}' \nopen in another program?")
    # ToDo: Implement selection of variabels to export

  def format_csv(self,file_path):
    """Format the csv file that is exported from PF.
    The PF exported csv uses the first row for the full path 
    of the object and the second row for the variable name.
    The formated csv file uses only the first row as a header.
    This row contains the path of the object and the variable name
    without description.

    Example first row of some column before formating: 
      '\\username.IntUser\\powfacpy_base.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\Grid.ElmNet\\AC Voltage Source.ElmVac\\s:u0'
    Example input second row of the column before formating:
      's:u0 in kV'
    Example first row of the column after formating:
      'Network Model\\Network Data\\Grid\\AC Voltage Source\\s:u0'
    """
    with open(file_path) as read_file, open(file_path + ".temp", "w") as write_file:
      full_paths = read_file.readline().split(",")
      variables = read_file.readline().split(",")
      for col,path in enumerate(full_paths):
          if col > 0:
              formated_path = powfacpy.PFStringManipuilation.format_full_path(path,self)
              variable_name = variables[col].split(" ", 1)[0][1:] # get rid of description and quotation marks
              row = row + formated_path + "\\" + variable_name + "," # consistently add headers to row
          else:
              row = "Time," # Header of first column
      write_file.write(row+"\n")
      # Write remaining data rows until end of file is reached
      while row:
          row = read_file.readline()
          write_file.write(row)
    replace(file_path + ".temp",file_path)  

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