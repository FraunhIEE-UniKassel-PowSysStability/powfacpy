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
          'variables':variables})

    df = read_csv(FULL_PATH, encoding='ISO-8859-1')
    remove(FULL_PATH)
    return df

  

""" class ElmRes2NumPyArray():

  def __init__(self) -> None:
    self.time_series = None # np.empty(1,dtype=float)

  def get(element,variable): """
