"""Plotting interface.
"""

import sys
sys.path.insert(0, r'.\src')
import powfacpy
import pandas
from matplotlib import pyplot
from collections.abc import Iterable
from os import getcwd, path
from os import path as os_path

class PFPlotInterface(powfacpy.PFBaseInterface):

  def __init__(self, app):
    super().__init__(app) 
    self.active_graphics_page = None
    self.active_plot = None


  def set_active_graphics_page(self, page):
    """Sets the active graphics page.
    Arguments:
      page:graphics page  name.
    """
    if isinstance(page, str):
      grb = self.get_or_create_graphics_board()
      self.active_graphics_page = grb.GetPage(page,1,"GrpPage")
    else:
      self.active_graphics_page = page


  def set_active_plot(self, name_or_obj, graphics_page=None):
    """Set the currently active plot. Adjusts the active graphics
    page accordingly if name_or_object is a PF plot object (the graphics
    page cannot be infered from a string path) or if the
    optional argument graphics_page is given.
    Arguments:
      name_or_obj: name of plot (string) or plot object.
      graphics_page: name of grphics page (string). If  
        specified, this sets the currently active page.
    """
    if graphics_page:
      self.set_active_graphics_page(graphics_page)
    if not isinstance(name_or_obj, str): # is plot object
      self.active_plot = name_or_obj
      self.set_active_graphics_page(self.active_plot.GetParent())
    else:
      try:
        self.active_plot = self.active_graphics_page.GetOrInsertCurvePlot(name_or_obj)
      except(AttributeError) as e:
        self._handle_possible_attribute_not_set_error(self.active_graphics_page,
          "active_grapics_page", e) 

  def get_or_create_graphics_board(self):
    """Get the graphics board of the currently active study case or create
    a new graphics board if it does not exist within the study case yet.
    """
    grb = self.app.GetGraphicsBoard()  
    if not grb:
      active_study_case = self.app.GetActiveStudyCase()
      graphics_board_name = powfacpy.PFTranslator.get_default_graphics_board_name(
         self.language)
      grb = self.create_in_folder(graphics_board_name, active_study_case)
      grb.Show()
      grb = self.app.GetGraphicsBoard() # get grb again to get correct object from PF
    return grb  


  def plot_monitored_variables(self, obj, variables,
    graphics_page=None, plot=None,**kwargs):
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
      data_series.AddCurve(obj, var)
      self.set_curve_attributes(data_series,**kwargs)
    self.active_graphics_page.Show()

  def get_data_series_of_active_plot(self):
    """Get the dataseries of the currently active plot.
    """
    try:
      return self.active_plot.GetDataSeries()
    except(AttributeError) as e:
      self._handle_possible_attribute_not_set_error(self.active_plot,
          "active_plot", e)

  def get_x_axis_of_active_plot(self):
    """Get the x-axis of the currently active plot.
    """
    try:
      return self.active_plot.GetAxisX()
    except(AttributeError) as e:
      self._handle_possible_attribute_not_set_error(self.active_plot,
          "active_plot", e)
  
  def get_y_axis_of_active_plot(self):
    """Get the y-axis of the currently active plot.
    """
    try:
      return self.active_plot.GetAxisY()
    except(AttributeError) as e:
      self._handle_possible_attribute_not_set_error(self.active_plot,
          "active_plot", e)

  def get_legend_of_active_plot(self): 
    try:
      return self.active_plot.GetLegend()
    except(AttributeError) as e:
      self._handle_possible_attribute_not_set_error(self.active_plot,
          "active_plot", e) 

  def get_title_obj_of_active_plot(self): 
    try:
      return self.active_plot.GetTitleObject()
    except(AttributeError) as e:
      self._handle_possible_attribute_not_set_error(self.active_plot,
          "active_plot", e) 
      
  def set_all_fonts_of_active_plot(self, fontsize=10, fontname="Arial", fontstyle=0):
    """Sets the fonts of all text elements (axis labels,legend,title). Note that the 
    fonts are not attributes of the PF objects (x-axis, title object,..), but can only be 
    set using the method 'SetFont'.
    """
    self.get_x_axis_of_active_plot().SetFont(fontname,fontsize,fontstyle)
    self.get_y_axis_of_active_plot().SetFont(fontname,fontsize,fontstyle) 
    self.get_legend_of_active_plot().SetFont(fontname,fontsize,fontstyle)  
    self.get_title_obj_of_active_plot().SetFont(fontname,fontsize,fontstyle)

  def plot(self, obj, variables, graphics_page=None, plot=None,**kwargs):
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
    self.add_results_variable(obj, variables, results_obj=results_obj)
    self.plot_monitored_variables(obj, variables,
      graphics_page=graphics_page, plot=plot,**kwargs) 
  

  def set_curve_attributes(self, data_series,**kwargs):
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
      data_series.SetAttribute("curveTableLineStyle", list_curveTableAttr)
    if "linewidth" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLineWidth")
      list_curveTableAttr[-1] = kwargs['linewidth']
      data_series.SetAttribute("curveTableLineWidth", list_curveTableAttr)
    else:
      # The linewidth must be set to the standard value. Otherwise PF uses 
      # the value from the previous data series (this seems to be a PF bug).
      list_curveTableAttr = data_series.GetAttribute("curveTableLineWidth")
      list_curveTableAttr[-1] = 100
      data_series.SetAttribute("curveTableLineWidth", list_curveTableAttr)
    if "color" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableColor")
      list_curveTableAttr[-1] = kwargs['color']
      data_series.SetAttribute("curveTableColor", list_curveTableAttr)
    # The label must be handled differently because PF returns an empty list
    # if there haven't been any labels specified yet for any of the curves.
    if "label" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLabel")
      if list_curveTableAttr:
        list_curveTableAttr[-1] = kwargs['label']
      else:
        list_curveTableAttr = [kwargs['label']]
      data_series.SetAttribute("curveTableLabel", list_curveTableAttr)
    if "results_obj" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableResultFile")
      list_curveTableAttr[-1] = self.handle_single_pf_object_or_path_input(
        kwargs['results_obj'])
      data_series.SetAttribute("curveTableResultFile", list_curveTableAttr)

  def set_x_axis_attributes(self,**kwargs):
    """Set x-axis attributes.
    Arguments:
      key-value-pairs of axis-related PF attributes and the desired value.
    """
    self._set_axis_attributes(
      self.get_x_axis_of_active_plot(),
      kwargs)
    
  def set_y_axis_attributes(self, **kwargs):
    """Set y-axis attributes.
    Arguments:
      key-value-pairs of axis-related PF attributes and the desired value.
    """
    self._set_axis_attributes(
      self.get_y_axis_of_active_plot(),
      kwargs)      
    
  def _set_axis_attributes(self, axis, kwargs):
    """ set axis attributes for given axis. 
    set_y_axis_attributes() and set_x_axis_attributes() use this funciton.
    """
    for attribute, value in kwargs.items():
      axis.SetAttribute(attribute, value)      

  def set_x_axis_range_of_active_plot(self, range: Iterable):
    self.set_x_axis_attributes(rangeMin=range[0], rangeMax=range[1])

  def set_y_axis_range_of_active_plot(self, range: Iterable):
    self.set_y_axis_attributes(rangeMin=range[0], rangeMax=range[1])  

  def plot_from_comtrade(self,
                      file_path,
                      variables,
                      graphics_page=None,
                      plot=None,
                      parent_folder_comtrade=None,
                      **kwargs):
    """Plot a varibale from a COMTRADE formated file under file_path (*.cfg).
    Creates the comtrade object (IntComtrade) and plots.
    
    If you want to plot from a comtrade object (IntComtrade) that already 
    exists in the PF database, use the method plot_monitored_variables as shown
    in this method.
    
    Arguments:
      file_path: str
      variables: The entry in the second column of a signal in .cfg
      parent_folder_comtrade: Container in PF database for comtrade objects
        (str or PF object)
         
    For further info on the arguments see method plot_monitored_variables.  
    """                  
    intcomtrade = self.create_comtrade_obj(file_path,
      parent_folder=parent_folder_comtrade)
    self.plot_monitored_variables(intcomtrade,
              variables,
              graphics_page=graphics_page,
              plot=plot,
              results_obj=intcomtrade,
              **kwargs)

  def plot_from_csv_using_elm_file(self, file_path, variable,**kwargs):
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
        parent_folder=elmfiles_network, error_if_non_existent=False)
      if not existing_elmfile:
        break
      elmfile_num += 1 
    elmfile = self.create_in_folder(
      "elmfile_" + str(elmfile_num) + ".ElmFile",       
      elmfiles_network,
      overwrite=True)
    self.clear_elmres_from_objects_with_status_deleted()
    elmfile.f_name = file_path + ".csv"
    # Add ElmREs for ElmFiles
    active_case = self.app.GetActiveStudyCase()
    elmres_for_elmfiles = self.create_in_folder(
      "elmres_for_elmfiles.ElmRes",
      active_case,
      overwrite=False, 
      use_existing=True)
    # Plot
    kwargs.update({"results_obj":elmres_for_elmfiles})  
    self.plot(elmfile, variable,**kwargs)
    # Simulate
    pfds = powfacpy.PFDynSimInterface(self.app)
    cominc = self.app.GetFromStudyCase("ComInc")
    initial_elmres = self.get_attr(cominc,"p_resvar")
    self.set_attr(cominc,{"p_resvar":elmres_for_elmfiles})
    pfds.initialize_and_run_sim()
    self.set_attr(cominc,{"p_resvar":initial_elmres})
    # Reactivate the initial networks
    elmfiles_network.Deactivate()
    for network in active_networks:
      network.Activate()


  def create_dummy_network(self, name=None):
    """Creates a network with only one terminal.
    Such a network is used for example to read in ElmFile objects.
    """
    if not name:
      name = "dummy_network"
    network_folder = self.app.GetProjectFolder("netdat",1)
    dummy_network = self.create_in_folder(
      name+".ElmNet", 
      network_folder,
      overwrite=False, 
      use_existing=True)
    self.create_in_folder("dummy_terminal.ElmTerm", dummy_network, overwrite=False, use_existing=True)
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

  def clear_all_graphics_pages(self):
    self.clear_graphics_board(obj="*.GrpPage")
    self.clear_graphics_board(obj="*.SetDeskpage") 

  def clear_graphics_board(self, obj="*"):
    """Clear the graphics board from specific objects or from all objects.
    Objects of class SetDeskpage are closed, 
    objects of class GrpPage are removed, 
    others are deleted.
    """
    grb = self.get_or_create_graphics_board()
    graphics = grb.GetContents(obj)
    for graphic in graphics:
      if graphic.GetClassName() == "SetDeskpage":
        graphic.Close()
      elif graphic.GetClassName() == "GrpPage":
        graphic.RemovePage()
      else:
        graphic.Delete()
  
  def copy_graphics_board_content(self, source_study_case,
    target_study_cases, obj_to_copy="*",
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
    source_graphics_board = self.get_single_obj(".SetDesktop",
      parent_folder=source_study_case)
    if not isinstance(target_study_cases,(list, tuple)):
      target_study_cases = [target_study_cases]  
    for target_study_case in target_study_cases:
      target_study_case = self.handle_single_pf_object_or_path_input(target_study_case)
      if not target_study_case == source_study_case:
        target_study_case.Deactivate() # Writing to active graphics board not possible 
        target_graphics_board = self.get_single_obj(".SetDesktop", parent_folder=target_study_case)
        if clear_target_graphics_board:
          self.delete_obj("*", parent_folder=target_graphics_board, error_if_non_existent=False)
        self.copy_obj(obj_to_copy, target_folder=target_graphics_board, overwrite=True,
          parent_folder=source_graphics_board)
    if currently_active_study_case:         
      currently_active_study_case.Activate() # Activate if it was deactivated

  def copy_graphics_board_content_to_all_study_cases(self, source_study_case,
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
    self.copy_graphics_board_content(source_study_case, target_study_cases,
      obj_to_copy=obj_to_copy,
      clear_target_graphics_board=clear_target_graphics_board)

  @staticmethod
  def plot_from_csv(csv_path, variables, offset=0, plot_interface=None):
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
        plot = plot_interface.plot(csv_file["time"]+offset, csv_file[var], label = var)   
    return plot

  def get_data_series_of_plot(self, plot=None):
    """Returns the data series object of a plot,
    If plot is None, the active plot is used.
    """
    if not plot:
      return self.get_data_series_of_active_plot()
    else:
      plot = self.handle_single_pf_object_or_path_input(plot)
      return plot.GetDataSeries()

  def get_curve_table_attributes(
      self, 
      plot=None, 
      adjust_result_file=True) -> dict:
    """Returns a dictionary with all curve table attributes (keys) and
    list with the attributes values for each curve (values) of a plot (i.e. its data series).

    Arguments:
      - plot: path or PF object. If None, the active plot is used
      - adjust_result_file: please see get_curve_table_attributes_referring_to_data_source
        for a detailed description 
    """
    attributes_referring_to_data_source = self.get_curve_table_attributes_referring_to_data_source(
      plot=plot, 
      adjust_result_file=adjust_result_file)
    attributes_referring_to_visualisation_visualization = self.get_curve_table_attributes_referring_to_visualization(
      plot=plot)
    return {**attributes_referring_to_data_source,
            **attributes_referring_to_visualisation_visualization}

  def get_curve_table_attributes_referring_to_data_source(
      self, 
      plot=None, 
      adjust_result_file=True) -> dict:
    """Get the curve table attributes referring to the data source 
    of the curves from a plot (i.e. its data series).
    These attributes are: "curveTableResultFile", "curveTableElement",
      "curveTableVariable"
    The return value is a dictionary with 
      - keys: attribute names
      - values: lists with the values for each curve

    Use this method if the data sources of the curves are of interest.
    If further attributes on visualisation are of interest, see also the
    methods:
      - get_curve_table_attributes
      - get_curve_table_attributes_referring_to_visualization

    Arguments:
      - plot: path or PF object. If None, the active plot is used.
      - adjust_result_file: 
        - If False, the list in "curveTableResultFile" is used as is
        - If True, the list is adjusted depending on the plot settings
          "useIndividualResults". If "useIndividualResults" is True,
          the result files from the list "curveTableResultFile" are used
          by default. If an element of this list is empty, the 
          "userSelectedResultFile" is used. Note that there is a bug in
          PF so that "autoSelectedResultFile" is always empty as described 
          below.
    """
    data_series = self.get_data_series_of_plot(plot)
    attributes = dict.fromkeys(["curveTableResultFile", 
                                "curveTableElement",
                                "curveTableVariable"]) 
    attributes["curveTableElement"] = data_series.GetAttribute("curveTableElement")
    attributes["curveTableVariable"] = data_series.GetAttribute("curveTableVariable")
    if adjust_result_file:
      # PF bug:
      # Even if 'autoSearchResultsFile' is True, 'userSelectedResultFile' and 
      # not 'autoSelectedResultFile' must be used.
      # Furthermore, 'autoSearchResultFile' must be deactivated and activated once.
      auto_search_result_file_original_value = data_series.autoSearchResultFile 
      data_series.autoSearchResultFile = 0
      data_series.autoSearchResultFile = 1
      data_series.autoSearchResultFile = auto_search_result_file_original_value
      attributes["curveTableResultFile"] = [data_series.GetAttribute(
      "userSelectedResultFile")]*len(attributes["curveTableElement"])  
      if data_series.useIndividualResults:
        curve_table_result_list = data_series.GetAttribute(
        "curveTableResultFile")
        for idx, result_file in enumerate(curve_table_result_list):
          if result_file:
            attributes["curveTableResultFile"][idx] = result_file   
    else:
      attributes["curveTableResultFile"] = data_series.GetAttribute(
        "curveTableResultFile")  
    return attributes
  
  def get_curve_table_attributes_referring_to_visualization(
      self, 
      plot=None) -> dict:
    """Returns the curve table attributes of a plot  (i.e. its data series) 
    that refer to the visualisation. 

    The return value is a dictionary with 
      - keys: attribute names
      - values: lists with the values for each curve

    Use this method if the data sources of the curves are of interest.
    If further attributes on the data sources are of interest, see also the
    methods:
      - get_curve_table_attributes
      - get_curve_table_attributes_referring_to_data_source    

    Arguments:
      - plot: path or PF object. If None, the active plot is used.

    """
    data_series = self.get_data_series_of_plot(plot)
    attributes = dict.fromkeys(["curveTableVisible", 
                                "curveTableNormalise",
                                "curveTableNormValue",
                                "curveTableColor", 
                                "curveTableLineStyle",
                                "curveTableLineWidth", 
                                "curveTableShape",
                                "curveTableFillStyle", 
                                "curveTableLabel"])
    for attr in attributes.keys():
      attributes[attr] = data_series.GetAttribute(attr)
    return attributes

  def set_curve_table_attributes(
      self, 
      attributes:dict, 
      plot=None) -> None:
    """Set the curve table attributes of a plot  (i.e. its data series).

    Arguments:
      - attributes: a dictionary with 
        - keys: argument names, e.g. "curveTableLabel"
        - values: list with the values for each curve
        - plot: path or PF object. If None, the active plot is used. 
    """     
    data_series = self.get_data_series_of_plot(plot)
    for attr,value in attributes.items():
      data_series.SetAttribute(attr,value)

  @staticmethod
  def clear_curves_from_curve_table_attributes_dict(
    attributes: dict, 
    index: "int|slice") -> dict:
    """Clear curves from a dictionary with the curve table attributes (keys)
    and the entries for each curve (values).
    IMPORTANT: Zero based indexing is used i.e. the first curve has index 0.
    Note that this does not clear the curves from the data series in the 
    PF plot, but only from the dictionary. If you want to clear the curves
    from a plot, use clear_curves_by_index_from_active_plot

    Arguments: 
      - attributes: dictionary with attribute names (keys) and entries for each 
        curve (values)
      - index: can be an integer or slice
        - integer: index of one curve to be deleted
        - slice: several curves are deleted. Examples:
          - slices have the general form "slice(start, end, step)" (see for example https://www.programiz.com/python-programming/methods/built-in/slice) 
          - "slice(2,4)": clear curves with index 2,3 (step=1 is default)
          - "slice(-1,1,-1): start at the end and delete all curves larger than index 1  
    """
    for values in attributes.values():
      del values[index]

  def clear_curves_by_index_from_active_plot(self, index: "int|slice") -> None:
    """Clear curves with certain index from plot (i.e. its data series).
    IMPORTANT: Zero based indexing is used i.e. the first curve has index 0.
    The native PF API has no such functionality and can only delete all curves.
    The method works as follows: 
     - gets the curve table attributes in a dictionary
     - clears all curves from plot
     - clear certain curves from the dictionary
     - set the curve table attributes according to the dictionary

     Arguments:
      - index: for a detailled description please have 
        a look at clear_curves_from_curve_table_attributes_dict
    """
    curve_table_attr = self.get_curve_table_attributes()
    self.clear_curves()
    powfacpy.PFPlotInterface.clear_curves_from_curve_table_attributes_dict(
      curve_table_attr,index)
    self.set_curve_table_attributes(curve_table_attr)

  def get_lists_from_data_series_of_plot(self, plot=None, indexes=None, include_curve_options=False):
    """Depracated: Please use get_curve_table_attributes instead. The usage of
    a the class PFListsOfDataSeriesOfPlot has turned out to be less convenient than
    just using a dictionary for the curve table attributes.

    Returns PFListsOfDataSeriesOfPlot object with lists of the data from 
    DataSeries (PltDataseries) of a plot.
    """
    data_series = self.get_data_series_of_plot(plot)   
    lists = PFListsOfDataSeriesOfPlot(
      data_series.GetAttribute("curveTableElement"),  
      data_series.GetAttribute("curveTableVariable"), 
      [], [], [], [], []
    )
    if data_series.useIndividualResults:
      lists.result_objects = data_series.GetAttribute("curveTableResultFile") 
      for idx, res_obj in enumerate(lists.result_objects):
        if not res_obj:
          lists.result_objects[idx] = data_series.GetAttribute("userSelectedResultFile")
    else:
      # PF bug:
      # Even if 'autoSearchResultsFile' is True, 'userSelectedResultFile' and 
      # not 'autoSelectedResultFile' must be used.
      # Furthermore, 'autoSearchResultFile' must be deactivated and activated once.
      auto_search_result_file_original_value = data_series.autoSearchResultFile 
      data_series.autoSearchResultFile = 0
      data_series.autoSearchResultFile = 1
      data_series.autoSearchResultFile = auto_search_result_file_original_value
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

  def export_active_page(self, format='pdf', path=getcwd()):
    """Export active page using ComWr.
    """
    self.active_graphics_page.Show()
    comwr = self.app.GetFromStudyCase('ComWr')
    self.set_attr(comwr,{'iopt_rd': format,'iopt_savas': 0, 'f': path + "." + format})
    comwr.Execute()  


class PFListsOfDataSeriesOfPlot:
  """Deprecated: This class turned out to be less convenient than
  just using a dictionary for the curve table attributes"""

  def __init__(self, elements, variables, result_objects, line_styles, line_widths, colors, labels) -> None:
    self.elements = elements
    self.variables = variables 
    self.result_objects = result_objects
    self.line_styles = line_styles
    self.line_widths = line_widths
    self.colors = colors
    self.labels = labels          
