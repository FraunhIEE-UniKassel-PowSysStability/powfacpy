Module powfacpy.applications.plots
==================================
Plotting interface.

Classes
-------

`Plots(pf_app: powfacpy.pf_classes.protocols.PFApp | None | bool = False, cached: bool = False)`
:   Base class for applications. Allows to create versions with
    - ActiveProjectCached (recommended when only one project stays active)
    - or ActiveProject (recommended when the active project may change)

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Static methods

    `clear_curves_from_curve_table_attributes_dict(attributes: dict, index: int | slice) ‑> None`
    :   Clear curves from a dictionary with the curve table attributes (keys)
        and the entries for each curve (values).
        
        IMPORTANT: Zero based indexing is used i.e. the first curve has index 0.
        Note that this does not clear the curves from the data series in the
        PF plot, but only from the dictionary. If you want to clear the curves
        from a plot, use clear_curves_by_index_from_active_plot
        
        Arguments:
          - attributes (dict): dictionary with attribute names (keys) and entries for each
            curve (values)
          - index (int | slice): can be an integer or slice
            - integer: index of one curve to be deleted
            - slice: several curves are deleted. Examples:
              - slices have the general form "slice(start, end, step)" (see for example https://www.programiz.com/python-programming/methods/built-in/slice)
              - "slice(2,4)": clear curves with index 2,3 (step=1 is default)
              - "slice(-1,1,-1): start at the end and delete all curves larger than index 1

    `plot_from_csv(csv_path: str, variables: str | list[str], offset: float = 0, plot_interface: object = None) ‑> powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot`
    :   Plot results from csv file using pyplot.
        
        Args:
            csv_path (str): path of csv file
            variables (str | list[str]): variables to be plotted
            offset (float, optional): time offset. Defaults to 0.
            plot_interface (object, optional): _description_. Defaults to None.
        
        Returns:
            VisPlot | PltLinebarplot | PltVectorplot: Returns the plot.
        
        Example:
          plot_from_csv("results.csv",
            ["Network Model\Network Data\Grid\AC Voltage Source\s:u0",
            "Network Model\Network Data\Grid\AC Voltage Source\m:Psum:bus1"])

    ### Instance variables

    `active_graphics_page`
    :   Currently active graphics page.

    `active_plot`
    :   Currently active plot.

    ### Methods

    `autoscale(self) ‑> None`
    :   Autoscale all axis.
        
        ToDo: Check if this really works as expected.

    `clear_all_graphics_pages(self) ‑> None`
    :

    `clear_curves(self) ‑> None`
    :   Clear all curves from active plot.

    `clear_curves_by_index_from_active_plot(self, index: int | slice) ‑> None`
    :   Clear curves with certain index from plot (i.e. its data series).
        IMPORTANT: Zero based indexing is used i.e. the first curve has index 0.
        The native PF API has no such functionality and can only delete all curves.
        The method works as follows:
         - gets the curve table attributes in a dictionary
         - clears all curves from plot
         - clear certain curves from the dictionary
         - set the curve table attributes according to the dictionary
        
         Arguments:
          - index (int | slice): for a detailled description please have
            a look at clear_curves_from_curve_table_attributes_dict

    `clear_curves_from_all_plots(self) ‑> None`
    :   Clear curves from all plots of the active study case.

    `clear_graphics_board(self, obj: str = '*') ‑> None`
    :   Clear the graphics board from specific objects or from all objects.
        Objects of class SetDeskpage are closed,
        objects of class GrpPage are removed,
        other objects are deleted.
        
        Args:
            obj (str, optional): Object name (can include class and placeholders). Defaults to "*".

    `clear_grid_diagrams(self) ‑> None`
    :

    `clear_plot_pages(self) ‑> None`
    :   Deletes all graphics (plot) pages from the graphics board of
        the active study case.

    `copy_graphics_board_content(self, source_study_case: str | powfacpy.pf_classes.protocols.IntCase, target_study_cases: str | powfacpy.pf_classes.protocols.IntCase | list[str] | list[powfacpy.pf_classes.protocols.IntCase], obj_to_copy: str = '*', clear_target_graphics_board: bool = False) ‑> None`
    :   Copy the graphics board content of a study case to another study cases.
        
        Args:
            source_study_case (str | IntCase): Source case (path or object)
        
            target_study_cases (str | IntCase | list[str] | list[IntCase]): Target case(s) (path(s) or object(s))
        
            obj_to_copy (str, optional): name of objects to be copied from graphics board.(e.g. "*.GrpPage" to copy only the plot pages). Defaults to "*".
        
            clear_target_graphics_board (bool, optional): If true, the graphics boards of the target cases are cleared before pasting the content. Defaults to False.

    `copy_graphics_board_content_to_all_study_cases(self, source_study_case: str | powfacpy.pf_classes.protocols.IntCase, target_parent_folder: powfacpy.pf_classes.protocols.PFGeneral | str = None, include_subfolders: bool = True, obj_to_copy: str = '*', clear_target_graphics_board: bool = False) ‑> None`
    :   Copy the content of the graphics board to all study cases.
        
        Args:
            source_study_case (str | IntCase): Source case (path or object)
        
            target_parent_folder (str | PFGeneral, optional): Parent folder of target cases. By default, the study case folder of the project is used. Any folder inside the study case folder of the project can be specified.
        
            include_subfolders (bool, optional): Applies to search for target study cases. Defaults to True.
        
            obj_to_copy (str, optional): name of objects to be copied from graphics board (e.g. "*.GrpPage" to copy only the plot pages). . Defaults to "*".
        
            clear_target_graphics_board (bool, optional): If true, the graphics boards of the target cases are cleared before pasting the content. Defaults to False.

    `create_dummy_network(self, name: str = 'dummy_network') ‑> powfacpy.pf_classes.protocols.ElmNet`
    :   Creates a network with only one terminal.
        Such a network is used for example to read in ElmFile objects.

    `export_active_page(self, format: str = 'pdf', path: str = 'D:\\User\\seberlein\\FraunhIEE-UniKassel-PowSysStability\\powfacpy') ‑> tuple[str, int]`
    :   Export active page (e.g. to pdf) using the 'ComWr' object.
        
        Args:
            format (str, optional): Export format. Defaults to 'pdf'.
            path (str, optional): Export path. Defaults to current working directory (getcwd()).
        
        Returns
            tuple[str, int]: The path of the exported graphic and returned value of the PF 'comwr' object (0: successful export, 1: not successful)

    `export_curves_to_pandas_dataframe(self, plot: powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot | None = None, curves: list[int] | None = None) ‑> pandas.core.frame.DataFrame`
    :   Export data of curves from a plot to a pandas DataFrame.
        
        This methods is only applicable to curves from ElmRes objects.
        
        Args:
            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): Plot object. Defaults to None (active plot is used).
        
            curves (list[int] | None, optional): If not None, only the curves with the given indices are exported. Defaults to None (all curves are exported).
        
        Returns:
            pandas.DataFrame: DataFrame with time and curve values.

    `get_curve_table_attributes(self, plot: powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot = None, adjust_result_file=True, curves: list[int] | None = None) ‑> dict[str, list]`
    :   Get dictionary with all curve table attributes (keys) and
        list with the attributes values for each curve (values) of a plot (i.e. its data series).
        
        Args:
            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): path or PF object. If None, the active plot is used.
        
            adjust_result_file (bool, optional): please see get_curve_table_attributes_referring_to_data_source
            for a detailed description . Defaults to True.
        
            curves (list[int] | None, optional): If not None, only the attributes of the curves with the given indices are returned.
        
        Returns:
            dict[str, list]: curve table attributes

    `get_curve_table_attributes_referring_to_data_source(self, plot: powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot = None, adjust_result_file: bool = True, curves: list[int] | None = None) ‑> dict`
    :   Get the curve table attributes referring to the data source
        of the curves from a plot (i.e. its data series).
        
        These attributes are: "curveTableResultFile", "curveTableElement",
          "curveTableVariable"
        
        Use this method if the data sources of the curves are of interest.
        If further attributes on visualisation are of interest, see also the
        methods:
          - get_curve_table_attributes
          - get_curve_table_attributes_referring_to_visualization
        
        Args:
            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): path or PF object. If None, the active plot is used. Defaults to None.
        
            adjust_result_file (bool, optional): Defaults to True.
              - If False, the list in "curveTableResultFile" is used as is
              - If True, the list is adjusted depending on the plot settings
                "useIndividualResults". If "useIndividualResults" is True,
                the result files from the list "curveTableResultFile" are used
                by default. If an element of this list is empty, the
                "userSelectedResultFile" is used. Note that there is a bug in
                PF so that "autoSelectedResultFile" is always empty as described
                below.
        
            curves (list[int] | None, optional): If not None, only the attributes of the curves with the given indices are returned.
        
        Returns:
            dict:
              - keys: attribute names
              - values: lists with the values for each curve

    `get_curve_table_attributes_referring_to_visualization(self, plot: powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot | None = None, curves: list[int] | None = None) ‑> dict[str, object]`
    :   Get the curve table attributes of a plot  (i.e. its data series)
        that refer to the visualisation.
        
        The return value is a dictionary with
          - keys: attribute names
          - values: lists with the values for each curve
        
        Use this method if the attributes relevant for visualization of the curves are of interest.
        If further attributes on are of interest, see also the
        methods:
          - get_curve_table_attributes
          - get_curve_table_attributes_referring_to_data_source
        
        Args:
            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): path or PF object. If None, the active plot is used. Defaults to None.
        
        Returns:
            dict[str, object]: dict with attributes and their values.

    `get_data_series_of_active_plot(self) ‑> powfacpy.pf_classes.protocols.PltDataseries`
    :   Get dataseries object of the currently active plot.

    `get_data_series_of_plot(self, plot: powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot | None = None) ‑> powfacpy.pf_classes.protocols.PltDataseries`
    :   Returns the data series object of a plot. If plot is None, the active plot is used.

    `get_legend_of_active_plot(self) ‑> powfacpy.pf_classes.protocols.PltLegend`
    :

    `get_or_create_graphics_board(self) ‑> powfacpy.pf_classes.protocols.SetDesktop`
    :   Get the graphics board of the currently active study case or create
        a new graphics board if it does not exist within the study case yet.

    `get_title_obj_of_active_plot(self) ‑> powfacpy.pf_classes.protocols.PltTitle`
    :

    `get_x_axis_of_active_plot(self) ‑> powfacpy.pf_classes.protocols.PltAxis`
    :   Get the x-axis of the currently active plot.

    `get_y_axis_of_active_plot(self) ‑> powfacpy.pf_classes.protocols.PltAxis`
    :   Get the y-axis of the currently active plot.

    `plot(self, obj: powfacpy.pf_classes.protocols.PFGeneral | str, variables: str | list[str], graphics_page: str | powfacpy.pf_classes.protocols.GrpPage | powfacpy.pf_classes.protocols.SetVipage = None, plot: str | powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot = None, **kwargs) ‑> None`
    :   Plots the variables of 'obj' to the currently active plot.
        
        Also adds the variables to the results (ElmRes) object.
        The active plot can be set with the optional arguments.
        
        Args:
        
          obj (PFGeneral): Object (e.g. of class 'Elm...') of which variables are plotted.
        
          variables (str | list[str]): string or list of variable names
        
          graphics_page (str | GrpPage | SetVipage, optional): Defaults to None.
        
          plot (str | VisPlot | PltLinebarplot | PltVectorplot, optional): Plot object. Defaults to None.
        
          kwargs:
        
          results_obj: result object used (object or path)
          linestyle: int
          linewidth: double
          color: int
          label: str

    `plot_from_comtrade(self, file_path: str, variables: str | list[str], graphics_page: str | powfacpy.pf_classes.protocols.GrpPage | powfacpy.pf_classes.protocols.SetVipage = None, plot: powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot = None, parent_folder_comtrade: powfacpy.pf_classes.protocols.PFGeneral | str = None, **kwargs) ‑> None`
    :   Plot a varibale from a COMTRADE formated file.
        
        Creates the comtrade object (IntComtrade) and plots. For further info on the arguments see method 'plot_monitored_variables'.
        If you want to plot from a comtrade object (IntComtrade) that already
        exists in the PF database, use the method 'plot_monitored_variables' as shown in the code below.
        
        Args:
            file_path (str): of comtrade file
        
            variables (str | list[str]): The entry in the second column of a signal in .cfg
        
            graphics_page (str | GrpPage | SetVipage, optional): _description_. Defaults to None.
        
            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): _description_. Defaults to None.
        
            parent_folder_comtrade (str | PFGeneral, optional): FolderContainer in PF database for comtrade objects (str or PF object). Defaults to None ("Comtrade.IntFolder" in active study case is used).

    `plot_from_csv_using_elm_file(self, file_path: str, variable: str, **kwargs) ‑> None`
    :   Use an ElmFile object to plot data from csv file.
        
        It is generally preferrable and more stable to use the COMTRADE format to plot external data.
        
        The ElmFile objects are stored in a dummy network because the simulation needs to be run to read the data from the csv file and is not just printed to the plot automatically.
        
        Args:
            file_path (str): path to csv file
            variable (str): varaible name in csv file header

    `plot_from_pandas_using_comtrade(self, df: pandas.core.frame.DataFrame, graphics_page: str | powfacpy.pf_classes.protocols.GrpPage | powfacpy.pf_classes.protocols.SetVipage = None, plot: powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot = None, comtrade_file_dir: str | None = None, comtrade_file_name: str | None = None) ‑> str`
    :   Plot data from a pandas DataFrame inside PF using the COMTRADE format as an intermediate step.
        
        Args:
            df (pandas.DataFrame): Frame with time index and columns (labels must be single index) for each variable to be plotted.
            graphics_page (str | GrpPage | SetVipage, optional): target grapics page. Defaults to None (active page is used).
            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): target plot. Defaults to None (active is used).
            comtrade_file_dir (str | None, optional): directory to store COMTRADE file. Defaults to None (project dir is used).
            comtrade_file_name (str | None, optional): Name of COMTRADE file. Defaults to None (name is created from plot name).
        
        Returns:
            str: path of the created COMTRADE file (without extension).

    `plot_monitored_variables(self, obj: powfacpy.pf_classes.protocols.PFGeneral, variables: str | list[str], graphics_page: str | powfacpy.pf_classes.protocols.GrpPage | powfacpy.pf_classes.protocols.SetVipage = None, plot: powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot = None, **kwargs) ‑> None`
    :   Plot varibales. Variables must have been added to the monitored
        variables before (e.g. using 'add_results_variable').
        
        Args:
            obj (PFGeneral): Object (e.g. of class 'Elm...') of which variables are plotted.
        
            variables (str | list[str]): Variable(s) to be plotted.
        
            graphics_page (str | GrpPage | SetVipage, optional): Graphics page. Defaults to None.
        
            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): Plot object. Defaults to None.
        
            kwargs:
              results_obj: result object used (object or path)
              linestyle: int
              linewidth: double
              color: int
              label: str

    `set_active_graphics_page(self, page: str | powfacpy.pf_classes.protocols.GrpPage | powfacpy.pf_classes.protocols.SetVipage) ‑> None`
    :   Sets the active graphics page.
        
        Args:
            page (str | GrpPage | SetVipage): graphics page object or name

    `set_active_plot(self, name_or_obj: str | powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot, graphics_page: powfacpy.pf_classes.protocols.GrpPage | powfacpy.pf_classes.protocols.SetVipage = None) ‑> None`
    :   Set the currently active plot.
        
        Adjusts the active graphics page accordingly if 'name_or_object' is a PF plot object (the graphics page cannot be infered from a string path) or if the optional argument graphics_page is given.
        
        Args:
            name_or_obj (str): name of plot (string) or plot object
            graphics_page (str | GrpPage | SetVipage, optional): Graphics page object or string. Defaults to None.

    `set_all_fonts_of_active_plot(self, fontsize: int = 10, fontname: str = 'Arial', fontstyle: int = 0) ‑> None`
    :   Sets the fonts of all text elements (axis labels,legend,title).
        
        Note that the fonts are not attributes of the PF objects (x-axis, title object,..), but can only be set using the method 'SetFont'.
        
        Args:
            fontsize (int, optional): Defaults to 10.
            fontname (str, optional): Defaults to "Arial".
            fontstyle (int, optional): Defaults to 0.

    `set_curve_attributes(self, data_series: powfacpy.pf_classes.protocols.PltDataseries | None = None, curve_num: int = -1, **kwargs) ‑> None`
    :   Set curve attributes in dataseries object of a plot.
        
        Args:
            data_series (PltDataseries, optional): data series of plot. Defaults to None (dataseries of active plot is used).
        
            curve_num (int, optional): Curve number. Defaults to -1 (last curve).
        
            kwargs:
              results_obj: result object used (object or path)
              linestyle: int
              linewidth: double
              color: int
              label: str

    `set_curve_table_attributes(self, attributes: dict[str, list], plot: powfacpy.pf_classes.protocols.VisPlot | powfacpy.pf_classes.protocols.PltLinebarplot | powfacpy.pf_classes.protocols.PltVectorplot = None) ‑> None`
    :   Set the curve table attributes of a plot  (i.e. its data series).
        
        Args:
            attributes (dict[str, list]): a dictionary with
              - keys: argument names, e.g. "curveTableLabel"
              - values: list with the values for each curve
        
            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): Plot object. Defaults to None (active plot is used).

    `set_shown_page_as_active_page(self) ‑> powfacpy.pf_classes.protocols.GrpPage`
    :   Set the page currently show in the PF GUI as the 'active_graphics_page'. Note that the 'active_plot' attribute is not affected.

    `set_x_axis_attributes(self, **kwargs) ‑> None`
    :   Set y-axis attributes.
        
        Args:
          kwargs:
            key-value-pairs of axis-related PF attributes and their value.

    `set_x_axis_range_of_active_plot(self, range: tuple[float]) ‑> None`
    :

    `set_y_axis_attributes(self, **kwargs) ‑> None`
    :   Set y-axis attributes.
        
        Args:
          kwargs:
            key-value-pairs of axis-related PF attributes and their value.

    `set_y_axis_range_of_active_plot(self, range: tuple[float]) ‑> None`
    :