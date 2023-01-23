import sys
sys.path.insert(0,r'.\src')
import powfacpy
import numpy as np


class PFResultsInterface(powfacpy.PFBaseInterface):

  def __init__(self, app):
    super().__init__(app)

  def get_list_with_results_of_variable(self,obj,variable,results_obj=None,load_elmres=True):
    if not results_obj:
      results_obj = self.app.GetFromStudyCase("ElmRes") 
    obj = self.handle_single_pf_object_or_path_input(obj)  
    column = results_obj.FindColumn(obj,variable)
    return self.get_list_with_results_of_column(column,results_obj=results_obj,load_elmres=load_elmres)  

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

  

""" class ElmRes2NumPyArray():

  def __init__(self) -> None:
    self.time_series = None # np.empty(1,dtype=float)

  def get(element,variable): """
