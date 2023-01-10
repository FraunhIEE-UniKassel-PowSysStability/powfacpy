"""Plotting interface.
"""

import sys
from unittest import result

from powfacpy.base_interface import PFTranslator
from powfacpy.dyn_sim_interface import PFDynSimInterface
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


  def set_active_plot(self,name_or_obj,graphics_page=None):
    """Set the currently active plot.
    Arguments:
      name_or_obj: name of plot (string) or plot object
      graphics_page: name of grphics page (string). If  
        specified, this sets the currently active page.
    """
    if graphics_page:
      self.set_active_graphics_page(graphics_page)
      if not isinstance(name_or_obj,str):
        self.active_plot = name_or_obj
      else:
        self.active_plot = self.active_graphics_page.GetOrInsertCurvePlot(name_or_obj)
    else:
      self.active_plot = name_or_obj
      self.set_active_graphics_page(self.active_plot.GetParent())


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
    x_axis = self.get_x_axis_of_active_plot()
    self.set_x_axis_attributes(x_axis, **kwargs)
    self.active_graphics_page.Show()


  def _handle_possible_no_plot_activated_error(self, get_from_plot_function):
    """Handle error if no active plot available.
    """
    try:
      return get_from_plot_function()
    except(AttributeError) as e:
      if not self.active_plot:
        raise powfacpy.PFNoPlotActivatedError()
      else:
        raise AttributeError(e)

  def get_data_series_of_active_plot(self):
    """Get the dataseries of the currently active plot.
    """
    return self._handle_possible_no_plot_activated_error(
      self.active_plot.GetDataSeries)

  def get_x_axis_of_active_plot(self):
    """Get the x-axis of the currently active plot.
    """
    return self._handle_possible_no_plot_activated_error(
      self.active_plot.GetAxisX)
  
  def get_y_axis_of_active_plot(self):
    """Get the y-axis of the currently active plot.
    """
    return self._handle_possible_no_plot_activated_error(
      self.active_plot.GetAxisX)
    

  def plot(self,obj,variables,graphics_page=None,plot=None,**kwargs):
    """Plots the variables of 'obj' to the currently active plot.
    Includes adding the variables to the results (ElmRes) object.
    The active plot can be set with the optional arguments.
    Arguments:
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
    if "results_obj" in kwargs:
      results_obj = kwargs["results_obj"]
    else:
      results_obj = None
    self.add_results_variable(obj,variables,results_obj=results_obj)
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

  def set_x_axis_attributes(self,x_axis,**kwargs):
    """Set x-axis attributes.
    Arguments:
      x_axis: x-axis of plot.
      kwargs:
        xaxislabelmode: int (e. g. 0=standard, 1=time, 2=date)
    """
    if  "xaxislabelmode" in kwargs:
      x_axis.SetAttribute("axisMode",kwargs["xaxislabelmode"])
    

  def plot_from_csv_using_elm_file(self,file_path,variable,**kwargs):
    """Use an ElmFile object to plot data from csv file.
    The ElmFiles are stored in a dummy network because the simulation needs to be run
    to read the data from the csv file and is not just printed to the plot automatically.
    """
    # Deactivate currently active networks
    active_networks = self.get_active_networks(
      error_if_no_network_is_active=False)
    for network in active_networks:
      network.Deactivate()
    # Activate dummy network
    elmfiles_network = self.create_dummy_network("network_for_elmfiles")  
    elmfiles_network.Activate()  
    # Add new ElmFile
    elmfile_num = 1
    while True:
      existing_elmfile = self.get_single_obj("elmfile_"+str(elmfile_num),
        parent_folder=elmfiles_network,error_if_non_existent=False)
      if not existing_elmfile:
        break
      elmfile_num += 1 
    elmfile = self.create_in_folder(elmfiles_network,
      "elmfile_"+str(elmfile_num)+".ElmFile",overwrite=True)
    self.clear_elmres_from_objects_with_status_deleted()
    elmfile.f_name = file_path + ".csv"
    # Add ElmREs for ElmFiles
    active_case = self.app.GetActiveStudyCase()
    elmres_for_elmfiles = self.create_in_folder(active_case,
      "elmres_for_elmfiles.ElmRes",overwrite=False,use_existing=True)
    # Plot
    kwargs.update({"results_obj":elmres_for_elmfiles})  
    self.plot(elmfile,variable,**kwargs)
    # Simulate
    pfds = PFDynSimInterface(self.app)
    cominc = self.app.GetFromStudyCase("ComInc")
    initial_elmres = self.get_attr(cominc,"p_resvar")
    self.set_attr(cominc,{"p_resvar":elmres_for_elmfiles})
    pfds.initialize_and_run_sim()
    self.set_attr(cominc,{"p_resvar":initial_elmres})
    # Reactivate the initial networks
    elmfiles_network.Deactivate()
    for network in active_networks:
      network.Activate()

  def create_dummy_network(self,name=None):
    """Creates a network with only one terminal.
    """
    if not name:
      name = "dummy_network"
    network_folder = self.app.GetProjectFolder("netdat",1)
    dummy_network = self.create_in_folder(network_folder,
      name+".ElmNet",overwrite=False,use_existing=True)
    self.create_in_folder(dummy_network,
      "dummy_terminal.ElmTerm",overwrite=False,use_existing=True)
    return dummy_network

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
    self.clear_graphics_board(obj="*.GrpPage")

  def clear_grid_diagrams(self):
    self.clear_graphics_board(obj="*.SetDeskpage")  

  def clear_graphics_board(self,obj="*"):
    """Clear the graphics board from specific objects or from all objects.
    Objects of class SetDeskpage are closed, others are removed.
    """
    grb = self.get_or_create_graphics_board()
    graphics = grb.GetContents(obj)
    for graphic in graphics:
      if graphic.GetClassName() == "SetDeskpage":
        graphic.Close()
      else:
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
    
    currently_active_study_case = self.app.GetActiveStudyCase() # Method should not change active case
    graphics_board_name = powfacpy.PFTranslator.get_graphics_board_name_from_studycase(
      currently_active_study_case) # assumption: graphics board names identical in all study cases 
    source_study_case = self.handle_single_pf_object_or_path_input(source_study_case)
    source_graphics_board = self.get_single_obj(graphics_board_name,
      parent_folder=source_study_case)
    if not isinstance(target_study_cases,(list,tuple)):
      target_study_cases = [target_study_cases]  
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

  def get_data_series_from_plot(self,plot=None,indexes=None,include_curve_options=False):
    if not plot:
      data_series = self.get_data_series_of_active_plot()
    else:
      plot = self.handle_single_pf_object_or_path_input(plot)
      data_series = plot.GetDataSeries()
    lists_from_data_series_of_plot = self.get_lists_from_data_series_of_plot(
      data_series,indexes=None,include_curve_options=False)
    return self.get_pf_result_variables_from_lists_of_data_series_of_plot(curveTableElements,curveTableVariable,curveTableResultFile,
      curveTableLineStyle,curveTableLineWidth,curveTableColor,
      curveTableLabelinclude_curve_options=False)  

  def get_lists_from_data_series_of_plot(self,plot=None,indexes=None,include_curve_options=False):
    """Returns PFListsOfDataSeriesOfPlot object with lists of the data from 
    DataSeries (PltDataseries) of a plot.
    """
    if not plot:
        data_series = self.get_data_series_of_active_plot()
    else:
      plot = self.handle_single_pf_object_or_path_input(plot)
      data_series = plot.GetDataSeries()  
    lists = PFListsOfDataSeriesOfPlot(
      data_series.GetAttribute("curveTableElement"),  
      data_series.GetAttribute("curveTableVariable"), 
      [], [], [], [], []
    )
    if data_series.useIndividualResults:
      lists.result_objects = data_series.GetAttribute("curveTableResultFile") 
      for idx,res_obj in enumerate(lists.result_objects):
        if not res_obj:
          lists.result_objects[idx] = data_series.GetAttribute("userSelectedResultFile")
    else:
      # PF bug:
      # Even if 'autoSearchResultsFile' is True, 'userSelectedResultFile' and 
      # not 'autoSelectedResultFile' must be used.
      # Furthermore, 'autoSearchResultFile' must be deactivated and activated once.
      data_series.autoSearchResultFile = 0
      data_series.autoSearchResultFile = 1
      lists.result_objects = [data_series.GetAttribute("userSelectedResultFile")]*len(lists.elements)
    if include_curve_options:
      lists.line_styles = data_series.GetAttribute("curveTableResultFile") 
      lists.line_widths = data_series.GetAttribute("curveTableLineWidth") 
      lists.colors = data_series.GetAttribute("curveTableColor") 
      lists.labels = data_series.GetAttribute("curveTableLabel")
    # Return only curves contained in indexes  
    if indexes:
      lists.elements = [lists.elements[i] for i in indexes]
      lists.variables = [lists.variables[i] for i in indexes]
      lists.result_objects = [lists.result_objects[i] for i in indexes] 
      if include_curve_options:
        lists.line_style = [lists.line_style[i] for i in indexes] 
        lists.line_widths = [lists.line_widths[i] for i in indexes] 
        lists.colors = [lists.colors[i] for i in indexes]  
        lists.labels = [lists.labels[i] for i in indexes]  
    return lists
    

class PFListsOfDataSeriesOfPlot:

  def __init__(self,elements,variables,result_objects,line_styles,line_widths,colors,labels) -> None:
    self.elements = elements
    self.variables = variables 
    self.result_objects = result_objects
    self.line_styles = line_styles
    self.line_widths = line_widths
    self.colors = colors
    self.labels = labels        