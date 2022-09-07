"""Plotting interface.
"""

import sys

from powfacpy.base_interface import PFTranslator
sys.path.insert(0,r'.\src')
import powfacpy
import pandas
from matplotlib import pyplot
from collections.abc import Iterable

class PFPlotInterface(powfacpy.PFBaseInterface):

  def __init__(self,app):
    super().__init__(app) 
    self.active_graphics_page = None
    self.active_plot = None

  def set_active_graphics_page(self,page):
    """Sets the active graphics page.
    Arguments:
      page:graphics page  name.
    """
    if isinstance(page, str):
      grb = self.get_or_create_graphics_board()
      self.active_graphics_page = grb.GetPage(page,1,"GrpPage")
    else:
      self.active_graphics_page = page

  def set_active_plot(self,name,graphics_page=None):
    """Set the currently active plot.
    Arguments:
      name: name of plot (string)
      graphics_page: name of grphics page (string). If  
        specified, this sets the currently active page.
    """
    if not graphics_page==None:
      self.set_active_graphics_page(graphics_page)
    self.active_plot = self.active_graphics_page.GetOrInsertCurvePlot(name)

  def get_or_create_graphics_board(self):
    """Get the graphics board of the currently active study case or create
    a new graphics board if it does not exist within the study case yet.
    """
    grb = self.app.GetGraphicsBoard()  
    if not grb:
      active_study_case = self.app.GetActiveStudyCase()
      graphics_board_name = PFTranslator.get_default_graphics_board_name(
         self.language)
      grb = self.create_in_folder(active_study_case,graphics_board_name)
      grb.Show()
      grb = self.app.GetGraphicsBoard() # get grb again to get correct object from PF
    return grb  

  def plot_monitored_variables(self,obj,variables,
    graphics_page=None,plot=None,**kwargs):
    """Plot varibales that were already added to the monitored
    variables.
    Arguments:
      obj: PowerFactory object or its path
      variables: string or list of variable names 
      graphics_page: name of graphics page
      plot: name of plot
      kwargs:
        result_obj: result object used (object or path)
        linestyle: int
        linewidth: double
        color: int
        label: str
    """
    if graphics_page:
      self.set_active_graphics_page(graphics_page)
    if plot:
      self.set_active_plot(plot)
    data_series = self.get_data_series_of_active_plot()
    if "results_obj" in kwargs:
      data_series.SetAttribute("useIndividualResults", 1)
    obj = self.handle_single_pf_object_or_path_input(obj)
    if isinstance(variables, str):
     variables = [variables]
    for var in variables:
      data_series.AddCurve(obj,var)
      self.set_curve_attributes(data_series,**kwargs)
    self.active_graphics_page.Show()

  def get_data_series_of_active_plot(self):
    """Get the dataseries of the currently active plot.
    """
    try:
      return self.active_plot.GetDataSeries()
    except(AttributeError) as e:
      if not self.active_plot:
        raise powfacpy.PFNoPlotActivatedError()
      else:
        raise AttributeError(e)

  def plot(self,obj,variables,graphics_page=None,plot=None,**kwargs):
    """Plots the variables of 'obj' to the currently active plot.
    Includes adding the variables to the results (ElmRes) object.
    The active plot can be set with the optional arguments.
    Arguemnts:
      variables: string or list of variable names 
      graphics_page: name of graphics page
      plot: name of plot
      kwargs:
        results_obj: result object used (object or path)
        linestyle: int
        linewidth: double
        color: int
        label: str
    """
    obj = self.handle_single_pf_object_or_path_input(obj)
    self.add_results_variable(obj,variables)
    self.plot_monitored_variables(obj,variables,
      graphics_page=graphics_page,plot=plot,**kwargs) 
  
  def set_curve_attributes(self,data_series,**kwargs):
    """Set curve attributes.
    Arguments:
      data_series: data series of plot.
      kwargs:
        results_obj: result object used (object or path)
        linestyle: int
        linewidth: double
        color: int
        label: str
    """
    if  "linestyle" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLineStyle")
      list_curveTableAttr[-1] = kwargs['linestyle']
      data_series.SetAttribute("curveTableLineStyle",list_curveTableAttr)
    if "linewidth" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLineWidth")
      list_curveTableAttr[-1] = kwargs['linewidth']
      data_series.SetAttribute("curveTableLineWidth",list_curveTableAttr)
    else:
      # The linewidth must be set to the standard value. Otherwise PF uses 
      # the value from the previous data series (this seems to be a PF bug).
      list_curveTableAttr = data_series.GetAttribute("curveTableLineWidth")
      list_curveTableAttr[-1] = 100
      data_series.SetAttribute("curveTableLineWidth",list_curveTableAttr)
    if "color" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableColor")
      list_curveTableAttr[-1] = kwargs['color']
      data_series.SetAttribute("curveTableColor",list_curveTableAttr)
    # The label must be handled differently because PF returns an empty list
    # if there haven't been any labels specified yet for any of the curves.
    if "label" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLabel")
      if list_curveTableAttr:
        list_curveTableAttr[-1] = kwargs['label']
      else:
        list_curveTableAttr = [kwargs['label']]
      data_series.SetAttribute("curveTableLabel",list_curveTableAttr)
    if "results_obj" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableResultFile")
      list_curveTableAttr[-1] = self.handle_single_pf_object_or_path_input(
        kwargs['results_obj'])
      data_series.SetAttribute("curveTableResultFile",list_curveTableAttr)

  def autoscale(self):
    self.active_graphics_page.DoAutoScaleY()
    self.active_graphics_page.DoAutoScaleX()
    self.active_graphics_page.DoAutoScaleY()
    self.active_graphics_page.DoAutoScaleX()

  def clear_curves(self):
    """Clear all curves from active plot.
    """
    data_series = self.get_data_series_of_active_plot()
    data_series.ClearCurves()

  def clear_curves_from_all_plots(self): 
    """Clear curves from all plots of the active study case.
    """     
    grb = self.get_or_create_graphics_board()
    graphics = grb.GetContents()
    for graphic in graphics:
      if graphic.GetClassName() == "GrpPage":    
        for child in graphic.GetContents(): 
          if child.GetClassName() == "PltLinebarplot":
            data_series =child.GetDataSeries()
            data_series.ClearCurves()  

  def clear_plot_pages(self):
    """Deletes all graphics (plot) pages from the graphics board of 
    the active study case. 
    """
    grb = self.get_or_create_graphics_board()
    graphics = grb.GetContents("*.GrpPage")
    for graphic in graphics:   
      graphic.RemovePage()
        
  def copy_graphics_board_content(self,source_study_case,
    target_study_cases,obj_to_copy="*",
    clear_target_graphics_board=False):
    """Copy the graphics board content of a study case to another study cases.
    Arguments:
      source_study_case: Source case (path or object)
      target_study_cases: Target case(s) (path(s) or object(s))
      obj_to_copy: name of objects to be copied from graphics board 
        (e.g. "*.GrpPage" to copy only the plot pages)
      clear_target_graphics_board: If true, the graphics boards of the target 
        cases are cleared before pasting the content  
    """    
    graphics_board_name = powfacpy.PFTranslator.get_default_graphics_board_name(
      self.language)  
    source_study_case = self.handle_single_pf_object_or_path_input(source_study_case)
    source_graphics_board = self.get_single_obj(graphics_board_name,
      parent_folder=source_study_case)
    currently_active_study_case = self.app.GetActiveStudyCase() # Method should not change active case
    if not isinstance(target_study_cases,Iterable):
      target_study_case = [target_study_cases]  
    for target_study_case in target_study_cases:
      target_study_case = self.handle_single_pf_object_or_path_input(target_study_case)
      if not target_study_case == source_study_case:
        target_study_case.Deactivate() # Writing to active graphics board not possible 
        target_graphics_board = self.get_single_obj(graphics_board_name,parent_folder=target_study_case)
        if clear_target_graphics_board:
          self.delete_obj("*",parent_folder=target_graphics_board,error_if_non_existent=False)
        self.copy_obj(obj_to_copy,target_folder=target_graphics_board,overwrite=True,
          parent_folder=source_graphics_board)
    if currently_active_study_case:         
      currently_active_study_case.Activate() # Activate if it was deactivated

  def copy_graphics_board_content_to_all_study_cases(self,source_study_case,
    target_parent_folder=None,
    include_subfolders=True,
    obj_to_copy="*",
    clear_target_graphics_board=False):
    """Copy the content of the graphics board to all study cases.
    Arguments:
      source_study_case: Source case (path or object)
      target_parent_folder: Parent folder of target cases. By default,
        the study case folder of the project is used. Any folder inside
        the study case folder of the project can be specified.
      obj_to_copy: name of objects to be copied from graphics board 
        (e.g. "*.GrpPage" to copy only the plot pages)
      clear_target_graphics_board: If true, the graphics boards of the target 
        cases are cleared before pasting the content
    """
    if not target_parent_folder:
      #study_case_project_folder_name = powfacpy.PFTranslator.get_default_study_case_folder_name(
      #  self.language)
      #target_parent_folder = self.get_single_obj(study_case_project_folder_name)
      target_parent_folder = self.app.GetProjectFolder("study")  
    target_study_cases = self.get_obj("*.IntCase",
      parent_folder=target_parent_folder,
      include_subfolders=include_subfolders)
    self.copy_graphics_board_content(source_study_case,target_study_cases,
      obj_to_copy=obj_to_copy,
      clear_target_graphics_board=clear_target_graphics_board)

  @staticmethod
  def plot_from_csv(csv_path,variables,offset=0,plot_interface=None):
    """Plot results from csv file using pyplot.
    Arguments:
      csv_path: path of csv file
      variables: path of variables to be plotted
      offset: time offset

    Returns the plot.

    Example:
      plot_from_csv("results.csv",
        ["Network Model\\Network Data\\Grid\\AC Voltage Source\\s:u0",
        "Network Model\\Network Data\\Grid\\AC Voltage Source\\m:Psum:bus1"])  
    """
    if not plot_interface:
      plot_interface = pyplot
    if isinstance(variables, str):
      variables = [variables]
    with open(csv_path) as file:
      csv_file = pandas.read_csv(file)
      for var in variables:
        plot = plot_interface.plot(csv_file["Time"]+offset, csv_file[var], label = var)   
    return plot




          