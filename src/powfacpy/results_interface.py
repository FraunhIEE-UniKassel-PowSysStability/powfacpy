import sys
sys.path.insert(0,r'.\src')
import powfacpy
import numpy as np
from os import remove, getcwd
from pandas import read_csv

class PFResultsInterface(powfacpy.PFBaseInterface):

  def __init__(self, app):
    super().__init__(app)

  def get_list_with_results_of_variable(self,obj,variable,results_obj=None,load_elmres=True):
    if not results_obj:
      results_obj = self.app.GetFromStudyCase("ElmRes")
    if load_elmres:  
      results_obj.Load()  
    obj = self.handle_single_pf_object_or_path_input(obj)  
    column = results_obj.FindColumn(obj,variable)
    return self.get_list_with_results_of_column(column,results_obj=results_obj,load_elmres=False)  

  def get_list_with_results_of_column(self,column,results_obj=None,load_elmres=True):
    if not results_obj:
      results_obj = self.app.GetFromStudyCase("ElmRes")
    if load_elmres:  
      results_obj.Load()   
    intvec = self.create_in_folder(results_obj.GetParent(),"test.IntVec",overwrite=True) 
    results_obj.GetColumnValues(intvec,column) 
    list = intvec.V
    intvec.Delete()
    return list
  
  def export_to_pandas(self, result_objects, elements, variables):
    """returns pandas DataFrame of specified simulation results.
      Arguments:
        result_objects: List of ElmRes for each result variable (repeat if identical or several variables) 
        elements: List of Powerfactory Objects for each result variable 
        variables: List of variable names for each result variable
    """
    FILE_NAME = 'temp'
    FILE_PATH = getcwd()
    FULL_PATH = FILE_PATH + "\\" + FILE_NAME + ".csv"
    self.export_to_csv(
      dir= FILE_PATH,
      file_name=FILE_NAME,
      results_variables_lists={
          'result_objects':result_objects,
          'elements':elements,
          'variables':variables},
      leave_csv_file_unchanged=True,
      )
    
    df = read_csv(FULL_PATH, encoding='ISO-8859-1', header=[0,1])
    def _reformat(column):
      path = powfacpy.PFStringManipulation._format_full_path(column[0], self)
      var = powfacpy.PFStringManipulation._format_variable_name(column[1])
      return path + '\\' + var
    df.columns = [_reformat(x) for x in df.columns]
    remove(FULL_PATH)
    return df
  
  @staticmethod
  def _get_time_variable_name_from_elmres(elmres):
    """Returns the variable name of simulation time. 
    Different PF simulation types generally have different names for the time variable.
    """
    simulation_type_number = elmres.calTp
    time_names = {
      0:'b:tnow', # all calculations
      29:'b:ucttime' # quaidynamic simulation
      # TODO to be continued if needed
    }
    return time_names[simulation_type_number]

""" class ElmRes2NumPyArray():

  def __init__(self) -> None:
    self.time_series = None # np.empty(1,dtype=float)

  def get(element,variable): """
