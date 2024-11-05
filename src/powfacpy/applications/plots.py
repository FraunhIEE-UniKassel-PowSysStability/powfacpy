"""Plotting interface.
"""

from os import getcwd

from matplotlib import pyplot
import pandas

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_class_protocols import (
    GrpPage,
    SetVipage,
    VisPlot,
    PltLinebarplot,
    PltVectorplot,
    SetDesktop,
    PFGeneral,
    PltDataseries,
    PltAxis,
    PltLegend,
    PltTitle,
    IntCase,
    ElmNet,
    PFApp,
)
import powfacpy


class Plots(ApplicationBase):

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)
        self.active_graphics_page: GrpPage | SetVipage = None
        "Currently active graphics page."
        self.active_plot: VisPlot | PltLinebarplot | PltVectorplot = None
        "Currently active plot."

    def plot(
        self,
        obj: PFGeneral | str,
        variables: str | list[str],
        graphics_page: str | GrpPage | SetVipage = None,
        plot: str | VisPlot | PltLinebarplot | PltVectorplot = None,
        **kwargs,
    ) -> None:
        """Plots the variables of 'obj' to the currently active plot.

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
        """
        obj = self.act_prj._handle_single_pf_object_or_path_input(obj)
        if "results_obj" in kwargs:
            results_obj = kwargs["results_obj"]
        else:
            results_obj = None
        self.act_prj.add_results_variable(obj, variables, results_obj=results_obj)
        self.plot_monitored_variables(
            obj, variables, graphics_page=graphics_page, plot=plot, **kwargs
        )

    def plot_monitored_variables(
        self,
        obj: PFGeneral,
        variables: str | list[str],
        graphics_page: str | GrpPage | SetVipage = None,
        plot: VisPlot | PltLinebarplot | PltVectorplot = None,
        **kwargs,
    ) -> None:
        """Plot varibales. Variables must have been added to the monitored
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
        """
        if graphics_page:
            self.set_active_graphics_page(graphics_page)
        if plot:
            self.set_active_plot(plot)
        data_series = self.get_data_series_of_active_plot()
        if "results_obj" in kwargs:
            data_series.SetAttribute("useIndividualResults", 1)
        obj = self.act_prj._handle_single_pf_object_or_path_input(obj)
        if isinstance(variables, str):
            variables = [variables]
        for var in variables:
            data_series.AddCurve(obj, var)
            self.set_curve_attributes(data_series, **kwargs)
        self.active_graphics_page.Show()

    def set_active_graphics_page(self, page: str | GrpPage | SetVipage) -> None:
        """Sets the active graphics page.

        Args:
            page (str | GrpPage | SetVipage): graphics page object or name
        """
        if isinstance(page, str):
            grb = self.get_or_create_graphics_board()
            self.active_graphics_page = grb.GetPage(page, 1, "GrpPage")
        else:
            self.active_graphics_page = page

    def set_active_plot(
        self,
        name_or_obj: str | VisPlot | PltLinebarplot | PltVectorplot,
        graphics_page: GrpPage | SetVipage = None,
    ) -> None:
        """Set the currently active plot.

        Adjusts the active graphics page accordingly if 'name_or_object' is a PF plot object (the graphics page cannot be infered from a string path) or if the optional argument graphics_page is given.

        Args:
            name_or_obj (str): name of plot (string) or plot object
            graphics_page (str | GrpPage | SetVipage, optional): Graphics page object or string. Defaults to None.
        """
        if graphics_page:
            self.set_active_graphics_page(graphics_page)
        if not isinstance(name_or_obj, str):  # is plot object
            self.active_plot = name_or_obj
            self.set_active_graphics_page(self.active_plot.GetParent())
        else:
            try:
                self.active_plot = self.active_graphics_page.GetOrInsertCurvePlot(
                    name_or_obj
                )
            except AttributeError as e:
                self.act_prj._handle_possible_attribute_not_set_error(
                    self.active_graphics_page, "active_grapics_page", e
                )

    def get_or_create_graphics_board(self) -> SetDesktop:
        """Get the graphics board of the currently active study case or create
        a new graphics board if it does not exist within the study case yet.
        """
        grb = self.act_prj.app.GetGraphicsBoard()
        if not grb:
            grb = self.act_prj.get_from_study_case("SetDesktop")
            grb.Show()
        return grb

    def get_data_series_of_active_plot(self) -> PltDataseries:
        """Get dataseries object of the currently active plot."""
        try:
            return self.active_plot.GetDataSeries()
        except AttributeError as e:
            self.act_prj._handle_possible_attribute_not_set_error(
                self.active_plot, "active_plot", e
            )

    def get_x_axis_of_active_plot(self) -> PltAxis:
        """Get the x-axis of the currently active plot."""
        try:
            return self.active_plot.GetAxisX()
        except AttributeError as e:
            self.act_prj._handle_possible_attribute_not_set_error(
                self.active_plot, "active_plot", e
            )

    def get_y_axis_of_active_plot(self) -> PltAxis:
        """Get the y-axis of the currently active plot."""
        try:
            return self.active_plot.GetAxisY()
        except AttributeError as e:
            self.act_prj._handle_possible_attribute_not_set_error(
                self.active_plot, "active_plot", e
            )

    def get_legend_of_active_plot(self) -> PltLegend:
        try:
            return self.active_plot.GetLegend()
        except AttributeError as e:
            self.act_prj._handle_possible_attribute_not_set_error(
                self.active_plot, "active_plot", e
            )

    def get_title_obj_of_active_plot(self) -> PltTitle:
        try:
            return self.active_plot.GetTitleObject()
        except AttributeError as e:
            self.act_prj._handle_possible_attribute_not_set_error(
                self.active_plot, "active_plot", e
            )

    def set_all_fonts_of_active_plot(
        self, fontsize: int = 10, fontname: str = "Arial", fontstyle: int = 0
    ) -> None:
        """Sets the fonts of all text elements (axis labels,legend,title).

        Note that the fonts are not attributes of the PF objects (x-axis, title object,..), but can only be set using the method 'SetFont'.

        Args:
            fontsize (int, optional): Defaults to 10.
            fontname (str, optional): Defaults to "Arial".
            fontstyle (int, optional): Defaults to 0.
        """
        self.get_x_axis_of_active_plot().SetFont(fontname, fontsize, fontstyle)
        self.get_y_axis_of_active_plot().SetFont(fontname, fontsize, fontstyle)
        self.get_legend_of_active_plot().SetFont(fontname, fontsize, fontstyle)
        self.get_title_obj_of_active_plot().SetFont(fontname, fontsize, fontstyle)

    def set_curve_attributes(
        self, data_series: PltDataseries | None = None, curve_num: int = -1, **kwargs
    ) -> None:
        """Set curve attributes in dataseries object of a plot.

        Args:
            data_series (PltDataseries, optional): data series of plot. Defaults to None (dataseries of active plot is used).

            curve_num (int, optional): Curve number. Defaults to -1 (last curve).

            kwargs:
              results_obj: result object used (object or path)
              linestyle: int
              linewidth: double
              color: int
              label: str
        """
        if curve_num > 0:
            curve_num -= 1
        if not data_series:
            data_series = self.get_data_series_of_active_plot()
        if "linestyle" in kwargs:
            list_curveTableAttr = data_series.GetAttribute("curveTableLineStyle")
            list_curveTableAttr[curve_num] = kwargs["linestyle"]
            data_series.SetAttribute("curveTableLineStyle", list_curveTableAttr)
        if "linewidth" in kwargs:
            list_curveTableAttr = data_series.GetAttribute("curveTableLineWidth")
            list_curveTableAttr[curve_num] = kwargs["linewidth"]
            data_series.SetAttribute("curveTableLineWidth", list_curveTableAttr)
        else:
            # The linewidth must be set to the standard value. Otherwise PF uses
            # the value from the previous data series (this seems to be a PF bug).
            list_curveTableAttr = data_series.GetAttribute("curveTableLineWidth")
            list_curveTableAttr[curve_num] = 100
            data_series.SetAttribute("curveTableLineWidth", list_curveTableAttr)
        if "color" in kwargs:
            list_curveTableAttr = data_series.GetAttribute("curveTableColor")
            list_curveTableAttr[curve_num] = kwargs["color"]
            data_series.SetAttribute("curveTableColor", list_curveTableAttr)
        # The label must be handled differently because PF returns an empty list
        # if there haven't been any labels specified yet for any of the curves.
        if "label" in kwargs:
            list_curveTableAttr = data_series.GetAttribute("curveTableLabel")
            if list_curveTableAttr:
                list_curveTableAttr[curve_num] = kwargs["label"]
            else:
                list_curveTableAttr = [kwargs["label"]]
            data_series.SetAttribute("curveTableLabel", list_curveTableAttr)
        if "results_obj" in kwargs:
            list_curveTableAttr = data_series.GetAttribute("curveTableResultFile")
            list_curveTableAttr[curve_num] = (
                self.act_prj._handle_single_pf_object_or_path_input(
                    kwargs["results_obj"]
                )
            )
            data_series.SetAttribute("curveTableResultFile", list_curveTableAttr)

    def set_x_axis_attributes(self, **kwargs) -> None:
        """Set y-axis attributes.

        Args:
          kwargs:
            key-value-pairs of axis-related PF attributes and their value.
        """
        x_axis = self.get_x_axis_of_active_plot()
        for attribute, value in kwargs.items():
            x_axis.SetAttribute(attribute, value)

    def set_y_axis_attributes(self, **kwargs) -> None:
        """Set y-axis attributes.

        Args:
          kwargs:
            key-value-pairs of axis-related PF attributes and their value.
        """
        y_axis = self.get_y_axis_of_active_plot()
        for attribute, value in kwargs.items():
            y_axis.SetAttribute(attribute, value)

    def set_x_axis_range_of_active_plot(self, range: tuple[float]) -> None:
        self.set_x_axis_attributes(rangeMin=range[0], rangeMax=range[1])

    def set_y_axis_range_of_active_plot(self, range: tuple[float]) -> None:
        self.set_y_axis_attributes(rangeMin=range[0], rangeMax=range[1])

    def autoscale(self) -> None:
        """Autoscale all axis.

        ToDo: Check if this really works as expected.
        """
        self.active_graphics_page.DoAutoScaleY()
        self.active_graphics_page.DoAutoScaleX()
        self.active_graphics_page.DoAutoScaleY()
        self.active_graphics_page.DoAutoScaleX()

    def clear_curves(self) -> None:
        """Clear all curves from active plot."""
        data_series = self.get_data_series_of_active_plot()
        data_series.ClearCurves()

    def clear_curves_from_all_plots(self) -> None:
        """Clear curves from all plots of the active study case."""
        grb = self.get_or_create_graphics_board()
        graphics = grb.GetContents()
        for graphic in graphics:
            if graphic.GetClassName() == "GrpPage":
                for child in graphic.GetContents():
                    if child.GetClassName() == "PltLinebarplot":
                        data_series = child.GetDataSeries()
                        data_series.ClearCurves()

    def clear_plot_pages(self) -> None:
        """Deletes all graphics (plot) pages from the graphics board of
        the active study case.
        """
        self.clear_graphics_board(obj="*.GrpPage")

    def clear_grid_diagrams(self) -> None:
        self.clear_graphics_board(obj="*.SetDeskpage")

    def clear_all_graphics_pages(self) -> None:
        self.clear_graphics_board(obj="*.GrpPage")
        self.clear_graphics_board(obj="*.SetDeskpage")

    def clear_graphics_board(self, obj: str = "*") -> None:
        """Clear the graphics board from specific objects or from all objects.
        Objects of class SetDeskpage are closed,
        objects of class GrpPage are removed,
        other objects are deleted.

        Args:
            obj (str, optional): Object name (can include class and placeholders). Defaults to "*".
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

    def copy_graphics_board_content(
        self,
        source_study_case: str | IntCase,
        target_study_cases: str | IntCase | list[str] | list[IntCase],
        obj_to_copy: str = "*",
        clear_target_graphics_board: bool = False,
    ) -> None:
        """Copy the graphics board content of a study case to another study cases.

        Args:
            source_study_case (str | IntCase): Source case (path or object)

            target_study_cases (str | IntCase | list[str] | list[IntCase]): Target case(s) (path(s) or object(s))

            obj_to_copy (str, optional): name of objects to be copied from graphics board.(e.g. "*.GrpPage" to copy only the plot pages). Defaults to "*".

            clear_target_graphics_board (bool, optional): If true, the graphics boards of the target cases are cleared before pasting the content. Defaults to False.
        """
        currently_active_study_case = (
            self.act_prj.app.GetActiveStudyCase()
        )  # Method should not change active case
        source_study_case = self.act_prj._handle_single_pf_object_or_path_input(
            source_study_case, include_subfolders=False
        )
        source_graphics_board = self.act_prj.get_unique_obj(
            ".SetDesktop", parent_folder=source_study_case, include_subfolders=False
        )
        if not isinstance(target_study_cases, (list, tuple)):
            target_study_cases = [target_study_cases]
        for target_study_case in target_study_cases:
            target_study_case = self.act_prj._handle_single_pf_object_or_path_input(
                target_study_case, include_subfolders=False
            )
            if not target_study_case == source_study_case:
                target_study_case.Deactivate()  # Writing to active graphics board not possible
                target_graphics_board = self.act_prj.get_unique_obj(
                    ".SetDesktop",
                    parent_folder=target_study_case,
                    include_subfolders=False,
                )
                if clear_target_graphics_board:
                    self.act_prj.delete_obj(
                        "*",
                        parent_folder=target_graphics_board,
                        error_if_non_existent=False,
                    )
                self.act_prj.copy_obj(
                    obj_to_copy,
                    target_folder=target_graphics_board,
                    overwrite=True,
                    parent_folder=source_graphics_board,
                )
        if currently_active_study_case:
            currently_active_study_case.Activate()  # Activate if it was deactivated

    def copy_graphics_board_content_to_all_study_cases(
        self,
        source_study_case: str | IntCase,
        target_parent_folder: str | PFGeneral = None,
        include_subfolders: bool = True,
        obj_to_copy: str = "*",
        clear_target_graphics_board: bool = False,
    ) -> None:
        """Copy the content of the graphics board to all study cases.

        Args:
            source_study_case (str | IntCase): Source case (path or object)

            target_parent_folder (str | PFGeneral, optional): Parent folder of target cases. By default, the study case folder of the project is used. Any folder inside the study case folder of the project can be specified.

            include_subfolders (bool, optional): Applies to search for target study cases. Defaults to True.

            obj_to_copy (str, optional): name of objects to be copied from graphics board (e.g. "*.GrpPage" to copy only the plot pages). . Defaults to "*".

            clear_target_graphics_board (bool, optional): If true, the graphics boards of the target cases are cleared before pasting the content. Defaults to False.
        """
        if not target_parent_folder:
            target_parent_folder = self.act_prj.app.GetProjectFolder("study")
        target_study_cases = self.act_prj.get_obj(
            "*.IntCase",
            parent_folder=target_parent_folder,
            include_subfolders=include_subfolders,
        )
        self.copy_graphics_board_content(
            source_study_case,
            target_study_cases,
            obj_to_copy=obj_to_copy,
            clear_target_graphics_board=clear_target_graphics_board,
        )

    @staticmethod
    def plot_from_csv(
        csv_path: str,
        variables: str | list[str],
        offset: float = 0,
        plot_interface: object = None,
    ) -> VisPlot | PltLinebarplot | PltVectorplot:
        """Plot results from csv file using pyplot.

        Args:
            csv_path (str): path of csv file
            variables (str | list[str]): variables to be plotted
            offset (float, optional): time offset. Defaults to 0.
            plot_interface (object, optional): _description_. Defaults to None.

        Returns:
            VisPlot | PltLinebarplot | PltVectorplot: Returns the plot.

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
                plot = plot_interface.plot(
                    csv_file["time"] + offset, csv_file[var], label=var
                )
        return plot

    def plot_from_comtrade(
        self,
        file_path: str,
        variables: str | list[str],
        graphics_page: str | GrpPage | SetVipage = None,
        plot: VisPlot | PltLinebarplot | PltVectorplot = None,
        parent_folder_comtrade: str | PFGeneral = None,
        **kwargs,
    ) -> None:
        """Plot a varibale from a COMTRADE formated file.

        Creates the comtrade object (IntComtrade) and plots. For further info on the arguments see method 'plot_monitored_variables'.
        If you want to plot from a comtrade object (IntComtrade) that already
        exists in the PF database, use the method 'plot_monitored_variables' as shown in the code below.

        Args:
            file_path (str): of comtrade file

            variables (str | list[str]): The entry in the second column of a signal in .cfg

            graphics_page (str | GrpPage | SetVipage, optional): _description_. Defaults to None.

            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): _description_. Defaults to None.

            parent_folder_comtrade (str | PFGeneral, optional): FolderContainer in PF database for comtrade objects (str or PF object). Defaults to None ("Comtrade.IntFolder" in active study case is used).
        """
        intcomtrade = self.act_prj.create_comtrade_obj(
            file_path, parent_folder=parent_folder_comtrade
        )
        self.plot_monitored_variables(
            intcomtrade,
            variables,
            graphics_page=graphics_page,
            plot=plot,
            results_obj=intcomtrade,
            **kwargs,
        )

    def plot_from_csv_using_elm_file(
        self, file_path: str, variable: str, **kwargs
    ) -> None:
        """Use an ElmFile object to plot data from csv file.

        It is generally preferrable and more stable to use the COMTRADE format to plot external data.

        The ElmFile objects are stored in a dummy network because the simulation needs to be run to read the data from the csv file and is not just printed to the plot automatically.

        Args:
            file_path (str): path to csv file
            variable (str): varaible name in csv file header
        """
        # Deactivate currently active networks
        active_networks = self.act_prj.get_active_networks(
            error_if_no_network_is_active=False
        )
        for network in active_networks:
            network.Deactivate()
        # Activate dummy network
        elmfiles_network = self.create_dummy_network("network_for_elmfiles")
        elmfiles_network.Activate()
        # Add new ElmFile
        elmfile_num = 1
        while True:
            existing_elmfile = self.act_prj.get_unique_obj(
                "elmfile_" + str(elmfile_num),
                parent_folder=elmfiles_network,
                error_if_non_existent=False,
            )
            if not existing_elmfile:
                break
            elmfile_num += 1
        elmfile = self.act_prj.create_in_folder(
            "elmfile_" + str(elmfile_num) + ".ElmFile", elmfiles_network, overwrite=True
        )
        self.act_prj.clear_elmres_from_objects_with_status_deleted()
        elmfile.f_name = file_path + ".csv"
        # Add ElmREs for ElmFiles
        active_case = self.act_prj.app.GetActiveStudyCase()
        elmres_for_elmfiles = self.act_prj.create_in_folder(
            "elmres_for_elmfiles.ElmRes",
            active_case,
            overwrite=False,
            use_existing=True,
        )
        # Plot
        kwargs["results_obj"] = elmres_for_elmfiles
        self.plot(elmfile, variable, **kwargs)
        # Simulate
        pfds = powfacpy.PFDynSimInterface(self.app)
        cominc = self.act_prj.get_from_study_case("ComInc")
        initial_elmres = self.act_prj.get_attr(cominc, "p_resvar")
        self.act_prj.set_attr(cominc, {"p_resvar": elmres_for_elmfiles})
        pfds.initialize_and_run_sim()
        self.act_prj.set_attr(cominc, {"p_resvar": initial_elmres})
        # Reactivate the initial networks
        elmfiles_network.Deactivate()
        for network in active_networks:
            network.Activate()

    def create_dummy_network(self, name: str = "dummy_network") -> ElmNet:
        """Creates a network with only one terminal.
        Such a network is used for example to read in ElmFile objects.
        """
        network_folder = self.act_prj.app.GetProjectFolder("netdat", 1)
        dummy_network = self.act_prj.create_in_folder(
            name + ".ElmNet", network_folder, overwrite=False, use_existing=True
        )
        self.act_prj.create_in_folder(
            "dummy_terminal.ElmTerm", dummy_network, overwrite=False, use_existing=True
        )
        return dummy_network

    def get_data_series_of_plot(
        self, plot: VisPlot | PltLinebarplot | PltVectorplot | None = None
    ) -> PltDataseries:
        """Returns the data series object of a plot. If plot is None, the active plot is used."""
        if not plot:
            return self.get_data_series_of_active_plot()
        else:
            plot = self.act_prj._handle_single_pf_object_or_path_input(plot)
            return plot.GetDataSeries()

    def get_curve_table_attributes(
        self,
        plot: VisPlot | PltLinebarplot | PltVectorplot = None,
        adjust_result_file=True,
    ) -> dict[str, list]:
        """Get dictionary with all curve table attributes (keys) and
        list with the attributes values for each curve (values) of a plot (i.e. its data series).

        Args:
            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): path or PF object. If None, the active plot is used.

            adjust_result_file (bool, optional): please see get_curve_table_attributes_referring_to_data_source
            for a detailed description . Defaults to True.

        Returns:
            dict[str, list]: curve table attributes
        """
        attributes_referring_to_data_source = (
            self.get_curve_table_attributes_referring_to_data_source(
                plot=plot, adjust_result_file=adjust_result_file
            )
        )
        attributes_referring_to_visualisation_visualization = (
            self.get_curve_table_attributes_referring_to_visualization(plot=plot)
        )
        return {
            **attributes_referring_to_data_source,
            **attributes_referring_to_visualisation_visualization,
        }

    def get_curve_table_attributes_referring_to_data_source(
        self,
        plot: VisPlot | PltLinebarplot | PltVectorplot = None,
        adjust_result_file: bool = True,
    ) -> dict:
        """Get the curve table attributes referring to the data source
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

        Returns:
            dict:
              - keys: attribute names
              - values: lists with the values for each curve
        """
        data_series = self.get_data_series_of_plot(plot)
        attributes = dict.fromkeys(
            ["curveTableResultFile", "curveTableElement", "curveTableVariable"]
        )
        attributes["curveTableElement"] = data_series.GetAttribute("curveTableElement")
        attributes["curveTableVariable"] = data_series.GetAttribute(
            "curveTableVariable"
        )
        if adjust_result_file:
            # PF bug:
            # Even if 'autoSearchResultsFile' is True, 'userSelectedResultFile' and
            # not 'autoSelectedResultFile' must be used.
            # Furthermore, 'autoSearchResultFile' must be deactivated and activated once.
            auto_search_result_file_original_value = data_series.autoSearchResultFile
            data_series.autoSearchResultFile = 0
            data_series.autoSearchResultFile = 1
            data_series.autoSearchResultFile = auto_search_result_file_original_value
            attributes["curveTableResultFile"] = [
                data_series.GetAttribute("userSelectedResultFile")
            ] * len(attributes["curveTableElement"])
            if data_series.useIndividualResults:
                curve_table_result_list = data_series.GetAttribute(
                    "curveTableResultFile"
                )
                for idx, result_file in enumerate(curve_table_result_list):
                    if result_file:
                        attributes["curveTableResultFile"][idx] = result_file
        else:
            attributes["curveTableResultFile"] = data_series.GetAttribute(
                "curveTableResultFile"
            )
        return attributes

    def get_curve_table_attributes_referring_to_visualization(
        self, plot: VisPlot | PltLinebarplot | PltVectorplot | None = None
    ) -> dict[str, object]:
        """Get the curve table attributes of a plot  (i.e. its data series)
        that refer to the visualisation.

        The return value is a dictionary with
          - keys: attribute names
          - values: lists with the values for each curve

        Use this method if the data sources of the curves are of interest.
        If further attributes on the data sources are of interest, see also the
        methods:
          - get_curve_table_attributes
          - get_curve_table_attributes_referring_to_data_source

        Args:
            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): path or PF object. If None, the active plot is used. Defaults to None.

        Returns:
            dict[str, object]: dict with attributes and their values.
        """
        data_series = self.get_data_series_of_plot(plot)
        attributes = dict.fromkeys(
            [
                "curveTableVisible",
                "curveTableNormalise",
                "curveTableNormValue",
                "curveTableColor",
                "curveTableLineStyle",
                "curveTableLineWidth",
                "curveTableShape",
                "curveTableFillStyle",
                "curveTableLabel",
            ]
        )
        for attr in attributes.keys():
            attributes[attr] = data_series.GetAttribute(attr)
        return attributes

    def set_curve_table_attributes(
        self,
        attributes: dict[str, list],
        plot: VisPlot | PltLinebarplot | PltVectorplot = None,
    ) -> None:
        """Set the curve table attributes of a plot  (i.e. its data series).

        Args:
            attributes (dict[str, list]): a dictionary with
              - keys: argument names, e.g. "curveTableLabel"
              - values: list with the values for each curve

            plot (VisPlot | PltLinebarplot | PltVectorplot, optional): Plot object. Defaults to None (active plot is used).
        """
        data_series = self.get_data_series_of_plot(plot)
        for attr, value in attributes.items():
            data_series.SetAttribute(attr, value)

    @staticmethod
    def clear_curves_from_curve_table_attributes_dict(
        attributes: dict, index: int | slice
    ) -> None:
        """Clear curves from a dictionary with the curve table attributes (keys)
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
        """
        for values in attributes.values():
            del values[index]

    def clear_curves_by_index_from_active_plot(self, index: int | slice) -> None:
        """Clear curves with certain index from plot (i.e. its data series).
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
        """
        curve_table_attr = self.get_curve_table_attributes()
        self.clear_curves()
        powfacpy.PFPlotInterface.clear_curves_from_curve_table_attributes_dict(
            curve_table_attr, index
        )
        self.set_curve_table_attributes(curve_table_attr)

    def export_active_page(self, format: str = "pdf", path: str = getcwd()) -> None:
        """Export active page (e.g. to pdf) using the 'ComWr' object.

        Args:
            format (str, optional): Export format. Defaults to 'pdf'.
            path (str, optional): Export path. Defaults to current working directory (getcwd()).
        """
        self.active_graphics_page.Show()
        comwr = self.act_prj.get_from_study_case("ComWr")
        self.act_prj.set_attr(
            comwr, {"iopt_rd": format, "iopt_savas": 0, "f": path + "." + format}
        )
        comwr.Execute()
