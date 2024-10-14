import sys
from os import remove, getcwd, replace
from math import inf
from warnings import warn
from typing import Iterable
import re

import pandas as pd
from icecream import ic

sys.path.insert(0, r".\src")
import powfacpy
from powfacpy.applications.application_base import ApplicationBase
from powfacpy import PFStringManipulation
from powfacpy.pf_class_protocols import PFGeneral, ElmRes, PFApp


class Results(ApplicationBase):

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)
        self.truncate_paths_until: str = (
            self.act_prj.get_path_of_object_in_active_project(
                self.act_prj.network_data_folder
            )
            + "\\"
        )  # = 'Network Model\Network Data\'
        "Paths (inside network data folder) will be truncated (e.g. when exported to pandas/csv)."
        self.multi_index_labels: bool = True
        "If True, multi index column labels are used (object, variable) in pandas format. If false, single index labels are used (path of object and variable strings are concatenated). Default is True."
        self.pf_objects_in_labels: bool = False
        "If, True PowerFactory objects are used in multi index column labels in pandas. If false, their path string is used. Only relevant if 'multi_index_labels' is True. Default is False."
        self.variable_aliases: dict[str, str] = {}
        self.obj_aliases: dict[str, str] = {}

    def export_to_csv(
        self,
        dir=None,
        file_name="results",
        results_obj=None,
        list_of_results_objs: list = None,
        elements: list = None,
        variables: list = None,
        column_separator: str = ",",
        decimal_separator: str = ".",
        comres_parameters: dict = {},
        format_csv_file: bool = True,
    ) -> str:
        """Exports simulation results to csv.

        Arguments:
          dir: export directory, if 'None' the current working directory
            (where script is run) is used

          file_name: Name of target csv file

          results_obj: PF ElmRes or IntComtrade object, by default the first ElmRes found in the active study case is used. All variables from this object are exported.

          list_of_results_objs: Specify if selected variables from several results objects should be exported. Used in combination with arguments 'elements' and 'variables'. Don't specify in combination with 'results_obj'. Note that PF (i.e. ComRes objects) does not allow the combined export from ElmRes and IntComtrade objects.

          elements: Specify if only selected variables from the grid elements in this list (e.g. ElmTerm etc.) should be exported. Used in combination with 'variables' and 'list_of_results_objs'(several different results objects)).

          variables: Specify if only selected variables (e.g. "m:u") should be exported). Used in combination with 'elements' and 'list_of_results_objs'.

          comres_parameters: Dictionary with parameters (and values) for the comres object.

          format_csv_file: Format csv file so there is only one row for the header (see also _format_csv_for_elmres and format_csv_for_comtrade).

        Returns:
          Path of csv file.

        Examples:

            Export a selection of results variables:
            ```
            voltage_source = pfbi.get_unique_obj(r'Network Model\\Network Data\\test_plot_interface\\Grid 1\\AC Voltage Source')
            control_model = pfbi.get_unique_obj('Network Model\\Network Data\\test_plot_interface\Grid 1\\WECC WT Control System Type 4A\\REEC_A Electrical Control Model')
            objects =   [voltage_source, voltage_source, control_model]
            variables = ['m:Qsum:bus1',  'm:Psum:bus1',  's:Ipcmd'    ]
            elmres_list = [pfbi.app.GetFromStudyCase('ElmRes'),]*len(variables)
            df = pfbi.export_to_csv(list_of_results_objs = elmres_list,
                                    objects = objects,
                                    variables = variables)
            ```
        """
        comres = self.act_prj.app.GetFromStudyCase("ComRes")
        if results_obj and list_of_results_objs:
            raise ValueError(
                "Results objects were given in 'results_obj' and in "
                + "'list_of_results_objs'. This is redundant, specify only one."
            )
        if elements and variables and list_of_results_objs:
            self._add_selected_variables_for_export(
                comres, list_of_results_objs, elements, variables
            )
            comres.iopt_csel = 1  # export selected variables
            if not comres.timeSclObj:  # Leading results object
                comres.timeSclObj = list_of_results_objs[0]
        elif elements or variables or list_of_results_objs:
            raise ValueError(
                "The arguments 'list_of_results_objs', 'elements' and 'variables' "
                + "must be specified together."
            )
        else:
            if not results_obj:
                if not self.act_prj.app.GetActiveStudyCase():
                    raise powfacpy.exceptions.PFNotActiveError("study case")
                comres.pResult = self.act_prj.get_from_study_case("ElmRes")
            else:
                comres.pResult = self.act_prj._handle_single_pf_object_or_path_input(
                    results_obj
                )
            comres.iopt_csel = 0  # export all variables

        self._set_comres_settings_for_csv_export(
            comres,
            dir,
            file_name,
            column_separator,
            decimal_separator,
            comres_parameters,
        )
        export_successful = comres.Execute()
        if export_successful != 0:
            comres_path = self.act_prj.get_path_of_object(comres)
            raise Exception(
                "CSV export was not successful using '" + str(comres_path) + "'"
            )

        path = self.act_prj._replace_special_PF_characters_in_path_string(comres.f_name)
        if format_csv_file:
            num_header_rows = self._get_number_of_header_rows_of_exported_csv_file(
                list_of_results_objs
            )
            self._format_exported_csv_file(
                path, comres, list_of_results_objs, num_header_rows
            )
        return path

    def _get_number_of_header_rows_of_exported_csv_file(
        self, list_of_results_objs: list
    ) -> int:
        """
        When PF exports to csv with ComRes, the number of header rows varies.
        Dependending on a list of results objects is used and whether all elements in list_of_results_objs are the same, PF will add 3 or 2 header rows to the exported csv file.
        """
        if list_of_results_objs:
            if all(i == list_of_results_objs[0] for i in list_of_results_objs):
                return 2
            else:
                return 3
        else:
            return 2

    def _set_comres_settings_for_csv_export(
        self,
        comres,
        dir: str,
        file_name: str,
        column_separator: str,
        decimal_separator: str,
        comres_parameters: dict,
    ) -> None:
        if not dir:
            dir = getcwd()
        comres.f_name = dir + "\\" + file_name + ".csv"
        comres.col_Sep = column_separator
        comres.dec_Sep = decimal_separator
        comres.iopt_exp = 6  # to export as csv
        comres.iopt_sep = 0  # to use specified column and decimal separator symbols
        comres.iopt_honly = 0  # to export data and not only the header
        comres.iopt_locn = 3  # export full path - '3' is the only setting where object's paths can be identified exactly. If set to 2, the exported path is inconsistent for objects inside grids and other folders inside the network data folder.
        comres.ciopt_head = 1  # full variable name
        comres.numberFormat = 1  # scientific notation
        _ = [
            comres.SetAttribute(attr, value)
            for attr, value in comres_parameters.items()
        ]

    def _format_exported_csv_file(
        self,
        path: str,
        comres,
        list_of_results_objs: list,
        num_header_rows: int,
    ) -> None:
        """
        Format csv file depending on the type of the results objects (ElmRes or
        IntComtrade).
        """
        if (comres.pResult and comres.pResult.GetClassName() == "ElmRes") or (
            list_of_results_objs and list_of_results_objs[0].GetClassName() == "ElmRes"
        ):
            self._format_csv_for_elmres(path, num_header_rows, list_of_results_objs)
        else:  # results objects are in COMTRADE format
            self._format_csv_for_comtrade(path)

    def _format_csv_for_comtrade(self, file_path: str) -> None:
        """Format the .csv file created (using ComRes) based on a Comtrade object (IntComtrade).
        There is a bug in PF so that the time in the first column sometimes
        is not monotonously increasing. This methods corrects this by checking
        for each time value (1. column) whether it is larger than the previous and discarding rows
        where this is not the case.
        """
        with open(file_path) as read_file, open(file_path + ".temp", "w") as write_file:
            row = read_file.readline()
            write_file.write(row)
            time = inf
            row = read_file.readline()
            while row:
                row_entries = row.split(",")
                if float(row_entries[0]) > time:
                    write_file.write(row)
                    time = float(row_entries[0])
                row = read_file.readline()
        replace(file_path + ".temp", file_path)

    def _format_csv_for_elmres(
        self, file_path: str, num_header_rows: int, list_of_results_objs: list
    ) -> None:
        """Format the csv file that is exported from PF.
        The PF exported csv uses the first rows either for
        - result object name (e.g. ElmRes name), element name (e.g. ElmTerm), variable name (e.g. "m:u")

        or only for

        - element name (e.g. ElmTerm), variable name (e.g. "m:u")
        This must be specified in num_header_rows (either 2 or 3).

        The formatted csv file will use only the first row as a header.
        This row contains the path of the object and the variable name
        without description.

        Example first row of some column before formatting:
          '\\username.IntUser\\powfacpy_base.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\Grid.ElmNet\\AC Voltage Source.ElmVac\\s:u0'
        Example input second row of the column before formatting:
          's:u0 in kV'
        Example first row of the column after formatting:
          'Network Model\\Network Data\\Grid\\AC Voltage Source\\s:u0'
        """
        with open(file_path) as read_file, open(file_path + ".temp", "w") as write_file:
            if num_header_rows == 2:
                full_paths = read_file.readline().split(",")
                variables = read_file.readline().split(",")
            else:
                read_file.readline().split(",")
                full_paths = read_file.readline().split(",")
                variables = read_file.readline().split(",")
            for col, path in enumerate(full_paths):
                is_last_column = col == len(full_paths) - 1
                if col > 0:
                    path = self._format_path_of_obj_inside_active_project(
                        PFStringManipulation.format_full_path(path, self.act_prj.app)
                    )
                    variable_name = PFStringManipulation.format_variable_name(
                        variables[col]
                    )
                    row = (
                        row + path + "\\" + variable_name + "," * (not is_last_column)
                    )  # consistently add headers to row
                else:
                    row = "time,"  # Header of first column
            write_file.write(row + "\n")
            # Write remaining data rows until end of file is reached
            while row:
                row = read_file.readline()
                write_file.write(row)
        replace(file_path + ".temp", file_path)
        if list_of_results_objs:
            if (
                len(list_of_results_objs) != len(full_paths) - 1
            ):  # -1 because of time in first column
                warn(
                    "Not all specified results were exported. Some of the elements may be 'out of service' and were not included."
                )

    def _add_selected_variables_for_export(
        self, comres, list_of_results_objs: list, elements: list, variables: list
    ):
        """Adds selected variables to ComRes for export.
        The time is added by default if the variable of the first row is not the
        simulaiton time.

        Arguments:
          comres: Results export object
          results_obj: list of results objects (ElmRes, IntComtrade)
          elements: list of grid objects (e.g. terminals, dsl models, etc.)
          variables: list of varaibles (corresponding to elements)
        """
        comres.iopt_csel = 1  # export only selected variables
        elmres = list_of_results_objs[0]
        # Insert simuation time
        time_variable_name = self._get_time_variable_name_from_elmres(elmres)
        first_row_is_time = variables[0] == time_variable_name

        if not first_row_is_time:  # add time as first row
            comres.resultobj = [elmres] + list_of_results_objs
            comres.element = [elmres] + elements
            comres.variable = [time_variable_name] + variables
        else:
            comres.resultobj = list_of_results_objs
            comres.element = elements
            comres.variable = variables

    def export_to_pandas(
        self,
        results_obj: ElmRes = None,
        list_of_results_objs: list = None,
        elements: list = None,
        variables: list = None,
        comres_parameters: dict = {},
    ) -> pd.DataFrame:
        """
        Returns pandas DataFrame of the simulation results in ElmRes. By default, all  results variables of the first ElmRes object found in the active study case are exported. A selection of specific variables can be exported using
        the optional arguments. Uses intermediate step by exporting to csv format
        with comres object.

        Arguments:
            results_obj: PF ElmRes or IntComtrade object, by default the first ElmRes found in the active study case is used. All variables from this object are exported.

            list_of_results_objs: Specify if selected variables from several results objects should be exported. Used in combination with arguments 'elements' and 'variables'. Don't specify in combination with 'results_obj'. Note that PF (i.e. ComRes objects) does not allow the combined export from ElmRes and IntComtrade objects.

            elements: Specify if only selected variables from the grid elements in this list (e.g. ElmTerm etc.) should be exported. Used in combination with 'variables' and 'list_of_results_objs'(several different results objects)).

            variables: Specify if only selected variables (e.g. "m:u") should be
            exported). Used in combination with 'elements' and 'list_of_results_objs'.

            comres_parameters: Dictionary with parameters (and values) for the comres object (for intermediate step to export to csv).

        Examples:
            Export a selection of results variables):
            ```
            voltage_source = pfri.get_unique_obj('Network Model\\Network Data\\test_plot_interface\\Grid 1\\AC Voltage Source')
            control_model = pfri.get_unique_obj('Network Model\\Network Data\\test_plot_interface\\Grid 1\\WECC WT Control System Type 4A\\REEC_A Electrical Control Model')
            elements =   [voltage_source, voltage_source, control_model]
            variables = ['m:Qsum:bus1',  'm:Psum:bus1',  's:Ipcmd'    ]
            elmres_list = [pfri.app.GetFromStudyCase('ElmRes'),]*len(variables)
            df = pfri.export_to_pandas(list_of_results_objs=elmres_list,
                                        elements=elements,
                                        variables=variables)
            ```
        """
        FILE_NAME = "temp"
        file_path = getcwd()
        full_path = file_path + "\\" + FILE_NAME + ".csv"

        try:
            self.export_to_csv(
                dir=file_path,
                file_name=FILE_NAME,
                results_obj=results_obj,
                list_of_results_objs=list_of_results_objs,
                elements=elements,
                variables=variables,
                comres_parameters=comres_parameters,
                format_csv_file=False,
            )

            df = pd.read_csv(full_path, encoding="ISO-8859-1", header=[0, 1])
            self._format_pandas_column_headers(
                df,
                list_of_results_objs,
            )
            if elements:
                if len(elements) != len(df.columns) - 1:
                    warn(
                        "Not all specified results were exported. Some of the elements may be 'out of service' and were not included."
                    )
        finally:
            remove(full_path)
        df.set_index(df.columns[0], inplace=True)
        df.index.name = "time"
        return df

    def _format_pandas_column_headers(
        self,
        df: pd.DataFrame,
        list_of_results_objs: list[ElmRes],
    ) -> None:
        """Format column headers of pandas DataFrame.

        Use single line column headers with path of object and results variable.

        Args:
            df (pd.DataFrame): unformatted DataFrame.

            list_of_results_objs (list[ElmRes]): Used to get number of header rows of exported csv file.
        """
        num_header_rows = self._get_number_of_header_rows_of_exported_csv_file(
            list_of_results_objs
        )
        headers = [None] * len(df.columns)
        if self.multi_index_labels:
            headers[0] = ("time", "s")
            parent_folder = self.act_prj.network_data_folder
            for n, col in enumerate(df.columns[1:], start=1):
                var = PFStringManipulation.format_variable_name(
                    col[num_header_rows - 1]
                )
                if self.pf_objects_in_labels:
                    obj = self.act_prj.GetContents(col[0])[0]
                else:
                    obj = PFStringManipulation.format_full_path(
                        col[num_header_rows - 2], self.act_prj.app
                    )
                    obj = self._format_path_of_obj_inside_active_project(obj)
                headers[n] = (obj, var)
            df.columns = pd.MultiIndex.from_tuples(headers)
        else:
            headers[0] = "time"
            for n, col in enumerate(df.columns[1:], start=1):
                var = PFStringManipulation.format_variable_name(
                    col[num_header_rows - 1]
                )
                obj = PFStringManipulation.format_full_path(
                    col[num_header_rows - 2], self.act_prj.app
                )
                obj = self._format_path_of_obj_inside_active_project(obj)
                headers[n] = obj + "\\" + var
            df.columns = headers

    def _format_path_of_obj_inside_active_project(
        self,
        path: str,
    ) -> str:
        """Format the path inside active project folder.

        Args:
             path (str): path inside network data folder (without class names)

        Returns:
            str: path truncated until 'self.truncate_paths_until'
        """
        if self.truncate_paths_until:
            path = PFStringManipulation.truncate_until(path, self.truncate_paths_until)
        return path

    # def _format_path_inside_network_data_folder(self, path: str) -> str:
    #     """Format the path inside network data folder.

    #     Args:
    #         path (str): path inside network data folder (without class names)

    #     Returns:
    #         str: path truncated until 'self.truncate_paths_until'
    #     """
    #     if self.truncate_paths_until:
    #         path = PFStringManipulation.truncate_until(path, self.truncate_paths_until)
    #     return path

    def replace_variable_aliases(self, var_name: str) -> str:
        """Replace 'var_name' with corresponding entry in 'self.variable_aliases'. If no such key exists in 'self.variable_aliases', 'var_name' is returned.

        Args:
            var_name (str): Original name (key in 'self.variable_aliases')

        Returns:
            str: Replacement (value in 'self.variable_aliases')
        """
        replacement = self.variable_aliases.get(var_name)
        if replacement:
            return replacement
        else:
            return var_name

    def replace_object_aliases(self, obj_name: str) -> str:
        """Replace 'obj_name' with corresponding entry in 'self.obj_aliases'. If no such key exists in 'self.obj_aliases', 'obj_name' is returned.

        Args:
            obj_name (str): Original name (key in 'self.obj_aliases')

        Returns:
            str: Replacement (value in 'self.obj_aliases')
        """
        replacement = self.obj_aliases.get(obj_name)
        if replacement:
            return replacement
        else:
            return obj_name

    def get_simulation_results_from_dataframe(
        self,
        df: pd.DataFrame,
        objs: PFGeneral | str | Iterable[PFGeneral | str],
        variables: str | Iterable[str],
    ) -> pd.DataFrame:
        """Get simulation results from a DataFrame (which was created using 'export_to_pandas').

        Args:

            df (pd.DataFrame): DataFrame with simulation results (created using 'export_to_pandas')

            objs (PFGeneral | str | Iterable[PFGeneral  |  str]): objects (for which results must be contained in the 'df')

            variables (str | Iterable[str]): variables (for which results must be contained in the 'df')

        Returns:
            DataFrame: DataFrame with specified results
        """
        if not isinstance(objs, Iterable):
            objs = [objs]
        if isinstance(variables, str):
            variables = [variables]

        obj_and_vars = []
        if self.multi_index_labels:
            if self.pf_objects_in_labels:
                objs = self.act_prj._handle_pf_object_or_path_input(objs)
            for obj in objs:
                if not self.pf_objects_in_labels:
                    obj = self._format_path_of_obj_inside_active_project(
                        PFStringManipulation.format_full_path(
                            str(obj), self.act_prj.app
                        )
                    )
                for var in variables:
                    obj_and_vars.append((obj, var))
        else:
            network_data_folder_path = PFStringManipulation.format_full_path(
                str(self.act_prj.network_data_folder), self.act_prj.app
            )
            for obj in objs:
                obj = self._format_path_of_obj_inside_active_project(
                    PFStringManipulation.format_full_path(str(obj), self.act_prj.app),
                )
                for var in variables:
                    obj_and_vars.append(f"{obj}\\{var}")
        return df[obj_and_vars]

    def _get_time_variable_name_from_elmres(self, elmres) -> str:
        """Returns the variable name of simulation time in an ElmRes object.
        Different PF simulation types (RMS, quasi-static,..)
        have different names for the time variable.
        """
        if elmres.calTp == 0:  # RMS/EMT
            return "b:tnow"
        elif elmres.calTp == 29:  # quasi-static
            return "b:ucttime"
        else:
            elmres_path = self.act_prj.get_path_of_object(elmres)
            raise Exception(
                f"""The PF simulation type number '{elmres.calTp}' of the results object 
      '{elmres_path}' 
      (attribute 'calTp' of ElmRes object) is not known or has not been implemented yet. Consider changes in the source code to 
      _get_time_variable_name_from_elmres (or open an issue: https://github.com/FraunhIEE-UniKassel-PowSysStability/powfacpy/)."""
            )

    def get_list_with_results_of_variable_from_elmres(
        self, obj, variable, results_obj=None, load_elmres=True
    ):
        # TODO move these methods to a separate class 'ResultExport' i.e. a specific ElmRes interface
        if not results_obj:
            results_obj = self.act_prj.app.GetFromStudyCase("ElmRes")
        if load_elmres:
            results_obj.Load()
        obj = self.act_prj._handle_single_pf_object_or_path_input(obj)
        column = results_obj.FindColumn(obj, variable)
        return self.get_list_with_results_of_column_from_elmres(
            column, results_obj=results_obj, load_elmres=False
        )

    def get_list_with_results_of_column_from_elmres(
        self, column, results_obj=None, load_elmres=True
    ):
        if not results_obj:
            results_obj = self.act_prj.app.GetFromStudyCase("ElmRes")
        if load_elmres:
            results_obj.Load()
        intvec = self.act_prj.create_in_folder(
            "test.IntVec", results_obj.GetParent(), overwrite=True
        )
        results_obj.GetColumnValues(intvec, column)
        list = intvec.V
        intvec.Delete()
        return list
