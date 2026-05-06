Module powfacpy.applications.results
====================================

Classes
-------

`Results(pf_app: powfacpy.pf_classes.protocols.PFApp | None | bool = False, cached: bool = False)`
:   Base class for applications. Allows to create versions with
    - ActiveProjectCached (recommended when only one project stays active)
    - or ActiveProject (recommended when the active project may change)

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Static methods

    `get_result_variable_description(obj_or_class: powfacpy.pf_classes.protocols.PFGeneral | str, variable: str, simulation_type: str = 'RMS_Bal') ‑> str`
    :   Get result variable description provided by PowerFactory.
        
        Args:
            obj_or_class (PFGeneral | str): PF object or PF class
            variable (str): Variable (of obj)
            simulation_type (str, optional): Simulation type, e.g. 'Basic', 'LF_Bal', 'LF_Unbal', 'RMS_Bal', 'RMS_Unbal', 'EMT', 'Sensitivities_Bal'. Defaults to "RMS_Bal".
        
        Returns:
            str: The varible description

    ### Instance variables

    `multi_index_labels`
    :   If True, multi index column labels are used (object, variable) in pandas format. If false, single index labels are used (path of object and variable strings are concatenated). Default is True.

    `pf_objects_in_labels`
    :   If True, PowerFactory objects are used in multi index column labels in pandas. If false, their path string is used. Only relevant if 'multi_index_labels' is True. Default is False.

    ### Methods

    `export_to_csv(self, dir=None, file_name='results', results_obj=None, list_of_results_objs: list = None, elements: list = None, variables: list = None, column_separator: str = ',', decimal_separator: str = '.', comres_parameters: dict = {}, format_csv_file: bool = True) ‑> str`
    :   Exports simulation results to csv.
        
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
            voltage_source = pfbi.get_unique_obj(r'Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source')
            control_model = pfbi.get_unique_obj('Network Model\Network Data\test_plot_interface\Grid 1\WECC WT Control System Type 4A\REEC_A Electrical Control Model')
            objects =   [voltage_source, voltage_source, control_model]
            variables = ['m:Qsum:bus1',  'm:Psum:bus1',  's:Ipcmd'    ]
            elmres_list = [pfbi.app.GetFromStudyCase('ElmRes'),]*len(variables)
            df = pfbi.export_to_csv(list_of_results_objs = elmres_list,
                                    objects = objects,
                                    variables = variables)
            ```

    `export_to_pandas(self, results_obj: powfacpy.pf_classes.protocols.ElmRes = None, list_of_results_objs: list = None, elements: list = None, variables: list = None, comres_parameters: dict = {}) ‑> pandas.core.frame.DataFrame`
    :   Returns pandas DataFrame of the simulation results in ElmRes. By default, all  results variables of the first ElmRes object found in the active study case are exported. A selection of specific variables can be exported using
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
            voltage_source = pfri.get_unique_obj('Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source')
            control_model = pfri.get_unique_obj('Network Model\Network Data\test_plot_interface\Grid 1\WECC WT Control System Type 4A\REEC_A Electrical Control Model')
            elements =   [voltage_source, voltage_source, control_model]
            variables = ['m:Qsum:bus1',  'm:Psum:bus1',  's:Ipcmd'    ]
            elmres_list = [pfri.app.GetFromStudyCase('ElmRes'),]*len(variables)
            df = pfri.export_to_pandas(list_of_results_objs=elmres_list,
                                        elements=elements,
                                        variables=variables)
            ```

    `get_list_with_results_of_column_from_elmres(self, column, results_obj=None, load_elmres=True)`
    :

    `get_list_with_results_of_variable_from_elmres(self, obj, variable, results_obj=None, load_elmres=True)`
    :

    `get_result_variables_descriptions_from_dataframe(self, df_simulation_results: pandas.core.frame.DataFrame, simulation_type: str = 'RMS_Bal') ‑> dict`
    :   Get result variable description provided by PowerFactory for all the results in a DataFrame.
        
        Args:
            df_simulation_results (pd.DataFrame): Simulation results (generated with 'export_to_pandas')
            simulation_type (str, optional): Simulation type, e.g. 'Basic', 'LF_Bal', 'LF_Unbal', 'RMS_Bal', 'RMS_Unbal', 'EMT', 'Sensitivities_Bal'. Defaults to "RMS_Bal".
        
        Returns:
            dict: The varible descriptions for each class

    `get_simulation_results_from_dataframe(self, df: pandas.core.frame.DataFrame, objs: powfacpy.pf_classes.protocols.PFGeneral | str | Iterable[powfacpy.pf_classes.protocols.PFGeneral | str], variables: str | Iterable[str]) ‑> pandas.core.frame.DataFrame`
    :   Get simulation results from a DataFrame (which was created using 'export_to_pandas').
        
        Args:
        
            df (pd.DataFrame): DataFrame with simulation results (created using 'export_to_pandas')
        
            objs (PFGeneral | str | Iterable[PFGeneral  |  str]): objects (for which results must be contained in the 'df')
        
            variables (str | Iterable[str]): variables (for which results must be contained in the 'df')
        
        Returns:
            DataFrame: DataFrame with specified results

    `replace_object_aliases(self, obj_name: str) ‑> str`
    :   Replace 'obj_name' with corresponding entry in 'self.obj_aliases'.
        
        If no such key exists in 'self.obj_aliases', 'obj_name' is returned.
        
        Args:
            obj_name (str): Original name (key in 'self.obj_aliases')
        
        Returns:
            str: Replacement (value in 'self.obj_aliases')

    `replace_variable_aliases(self, var_name: str) ‑> str`
    :   Replace 'var_name' with corresponding entry in 'self.variable_aliases'. If no such key exists in 'self.variable_aliases', 'var_name' is returned.
        
        Args:
            var_name (str): Original name (key in 'self.variable_aliases')
        
        Returns:
            str: Replacement (value in 'self.variable_aliases')