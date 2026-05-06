Module powfacpy.applications.dynamic_simulation
===============================================
Module with interface for dynamic simulations (RMS/EMT)

Classes
-------

`DynamicSimulation(pf_app: powfacpy.pf_classes.protocols.PFApp | None | bool = False, cached: bool = False)`
:   Dynamic simulation interface

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Static methods

    `get_dsl_lookup_arrays_and_matrices_names()`
    :

    `get_dsl_obj_array(dsl_obj, array_num=None, size_included_in_array=True)`
    :   Get the array of DSL object ('Advanced 1' tab).
        The array_num specifies which array is returend (if None,
        all arays/colmns are returned).
        If size_included_in_array=True, the first row (where the size
        of the array is spedified) is included.

    `is_dsl_lookup_arrays_and_matrices_name(string: str)`
    :   dsl has a special variable type for lookup tables. Such variables
        are defined using certain variable names starting with e.g. 'array_'.

    `set_dsl_obj_array(dsl_obj, rows: list, array_num: int | None = None, size_included_in_array=True) ‑> None`
    :   Set the array of a DSL object ('Advanced 1' tab).
        The array_num specifies which array is set (if None,
        all arrays/colums are set).
        If size_included_in_array=True, the first row (where the size
        of the array is specified) is included.

    `set_dsl_obj_array_from_pandas_series(dsl_obj, series: pandas.core.series.Series, array_num: int | None = None) ‑> None`
    :

    ### Instance variables

    `initialization_obj: powfacpy.pf_classes.protocols.ComInc`
    :

    `simulation_obj: powfacpy.pf_classes.protocols.ComSim`
    :

    ### Methods

    `clear_all_dyn_sim_events(self) ‑> None`
    :   Clear all dynamic simulation events.

    `create_dyn_sim_event(self, name_incl_class: str, params: dict[str, object] = {}, parent_folder: powfacpy.pf_classes.protocols.PFGeneral | str = None, overwrite: bool = True)`
    :   Creates an event for dynamic simulations (RMS/EMT) and sets the parameters in 'params'.
        
        Args:
            name_incl_class (str): Event name including the class.
        
            params (dict, optional): Paramter-values dictionary for created event object. Defaults to {}.
        
            parent_folder (PFGeneral | str, optional): Folder where event is created. If None, the events folder from the initial conditions calculation (ComInc) is used. Defaults to None.
        
            overwrite (bool, optional): Overwrite existing event with same name. Defaults to True.

    `create_event(self, name_incl_class, params={}, parent_folder=None, overwrite=True)`
    :   Creates an event and sets the parameters in 'params'.
        
        Arguments:
          name_incl_class: Event name including the class.
          params: Parameter-values dictionary.
          parent_folder: If None, the events folder from the initial conditions calculation (ComInc) is used.
          overwrite: Oerwrite existing event with same name.

    `get_dsl_model_parameter_names(self, dsl_model)`
    :   Get the parameter names of the block definition (BlkDef)
        of a dsl model.

    `get_dsl_models_inside_composite_model(self, composite_model)`
    :

    `get_eigenvalues_of_current_state(self, commod_parameters: dict[str, object] = {}) ‑> pandas.core.frame.DataFrame`
    :   Get the eigenvalues of the current state of the system.
        
        Uses the modal analysis command (ComMod) to calculate the eigenvalues (Eigenvectors and participation factors are omitted). The operating point of the current simulation time is used.
        Then uses result export (ComRes) to export the eigenvalues to csv, which is then read to a pandas DataFrame.
        
        Args:
            commod_parameters (dict[str, str], optional): Additional parameter settings of modal analysis command (ComMod). Defaults to {}.
        
        Returns:
            pd.DataFrame: pandas DataFrame with columns "real in 1/s", "imag in rad/s"

    `get_parameters_of_dsl_models_in_composite_model(self, composite_model: powfacpy.pf_classes.protocols.ElmComp, single_dict_for_all_dsl_models: bool = False)`
    :   Returns a dictionary with the parameter names (of the block definition)
        and values of all dsl models inside a composite model.
        
        dsl lookup variables (e.g. 'array_*', 'omatrix_*',.. ) are ignored.
        
        TODO: this method should be in the CompositeModel class
        
        Arguments:
          composite_model: ElmComp or its path
        
          single_dict_for_all_dsl_models:
            - If true, a single dictionary with the parameters of all dsl models is returned (no distinction is made between the dsl models).
            This assumes that a parameter that occurs in several dsl
            models has the same value.
            Example: {"a": 1, "b":0, "c":2}
            - If false, the returned dictionary contains dictionaries for each dsl model.
            Example:
              {
                "controller_a": {"a": 1, "b":0}
                "controller_b": {"a": 5, "c":2}
              }

    `initialize_and_run_sim(self, param_initialization: dict | None = None, param_simulation: dict | None = None)`
    :   Initialize and perform time domain simulation.

    `initialize_sim(self, param=None)`
    :   Initialize time domain simulation.
        Parameters for 'ComInc' command object can be specified in 'param' dictionary.

    `run_sim(self, param=None)`
    :   Perform dynamic simulation.
        Parameters for 'ComSim' command object can be specified in 'param' dictionary.

    `set_parameters_of_dsl_models_in_composite_model(self, composite_model, models_params_dict, single_dict_for_all_dsl_models=False) ‑> None`
    :   Set the parameters of the dsl models (i.e. of its block definition) in
        a composite model.
        
        Args:
          composite_model: ElmComp or its path
          models_params_dict: dictionary with model parameters and values
          single_dict_for_all_dsl_models:
            - If true, models_params_dict is a single dictionary that is used to set the parameters of all dsl models.
            Example: {"a": 1, "b":0, "c":2} -> if a dsl model has an attribute ("a","b",
            "c"), the value is set, otherwise it is ignored.
            - If false, models_params_dict contains dictionaries for each dsl model.
            Example:
              {
              "controller_a": {"a": 1, "b":0}
              "controller_b": {"a": 5, "c":2}
              }