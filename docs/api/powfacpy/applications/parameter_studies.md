Module powfacpy.applications.parameter_studies
==============================================

Functions
---------

`format_sig_no_sci(x, sig=3) ‑> str`
:   Format figure to three significant digits

Classes
-------

`ParameterStudy(pf_app=False, cached=False)`
:   Parameter studies using Variants.

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Instance variables

    `all_objs_and_attr`
    :   List of tuples with all PF objects and attributes of all variants

    `default_values`
    :   Default values (values) for PF objects, attributes (keys).

    `postprocessing_step`
    :   Function that is called at each step of the variants AFTER the simulation. Must be defined as a function with one input argument. 
        This argument is a dict that gives access to the following data:
        - "sim_res": DataFrame with simulation results of step
        - "variant": variant
        - "var_num": current variant number
        - "sim_num": current total simulation number
        - "step_num": current step number
        
        IMPORTANT: If the simulation results are changed, the function must return them.

    `preprocessing_step`
    :   Function that is called at each step of the variants BEFORE the simulation. Must be defined as a function with one input argument. This argument is a dict that gives access to the following data:
        - "variant": variant
        - "var_num": current variant number
        - "sim_num": current total simulation number
        - "step_num": current step number

    `preprocessing_variant`
    :   Function that is called before each variant is simulated. Must be defined as a function with one input argument. This argument is a dict that gives access to the following data:
        - "variant": variant
        - "var_num": current variant number
        - "sim_num": current total simulation number

    `values`
    :   List of values for all variants (values) of PFobjects, attributes (keys)

    `variants`
    :   Variants considered in this study

    ### Methods

    `execute_dynamic_simulations(self) ‑> dict`
    :   Execute dynamic simulations for all steps of all variants. Allows functions calls for pre- and postprocessing (the functions take all local variables as input arguments).
        
        Args:
            sample_time (float): resample simulation results
        
        Returns:
            dict: simulation result DataFrames (values) of all simulations (keys are names of simulations)

    `execute_postprocessing_step(self, pre_post_process_dict: dict) ‑> None`
    :

    `execute_preprocessing_step(self, pre_post_process_dict) ‑> None`
    :

    `execute_preprocessing_variant(self, pre_post_process_dict) ‑> None`
    :

    `get_all_names(self) ‑> list[str]`
    :   Get names of all simulations/steps.
        
        Returns:
            list[str]: list of names

    `get_all_objs_and_attr(self, sort: bool = True, cache: bool = False) ‑> list`
    :   Get list of tuples with all PF objects and their attribute.
        
        Args:
            cache (bool, optional): If True, the list is stored in 'self.all_objs_and_attr'. Defaults to False.
        
        Returns:
            list: list of tuples with all PF objects and their attribute

    `get_all_values(self) ‑> dict`
    :   Get values of PF object attributes for all variants.
        
        Returns:
            dict: Tuple of PF object, attribute (keys) and (flat) list of attribute values for all variants (values).

    `get_current_values_of_all_attr_in_pf(self) ‑> dict[tuple, typing.Any]`
    :   Get the current (in PF) attribute values of all PF objects.
        
        Returns:
            dict: PF objects, attributes (keys) and attribute values (values)

    `get_default_values(self) ‑> dict`
    :   Get all default attribute values of all variants.
        
        Returns:
            dict: tuple of PF object, attribute (keys) and attribute values (values)

    `get_values_of_variant(self, variant: powfacpy.applications.parameter_studies.Variant | int | str, step_num: int | None = None) ‑> dict`
    :   Get the attribute values of all PF objects for one of the variants.
        
        Args:
            variant (Variant | int | str): The variant instance, the variant index or the variant name.
            step_num (int | None, optional): If given, only the value of this step is returned. Defaults to None.
        
        Returns:
            dict: Tuple of PF objects, attributes (keys) and attribute values (values)

    `get_variant(self, variant: powfacpy.applications.parameter_studies.Variant | int | str) ‑> powfacpy.applications.parameter_studies.Variant`
    :   Get variant.
        
        Args:
            variant (Variant | int | str): If the input is the variant instance already, just returns it. If it is an int it is assumed to be the index. If at is a string it is assumed to be the name.
        
        Returns:
            Variant: variant

    `initialize(self) ‑> None`
    :

    `set_default_values(self) ‑> None`
    :   Set default values of all variants.

    `set_values_in_pf(self, variant: powfacpy.applications.parameter_studies.Variant | int | str, step_num: int, reset_default_values: bool = True) ‑> None`
    :   Set attribute values of all PF objects of a variant in PowerFactory for a certain step number.
        
        Args:
            variant (Variant | int | str): The variant instance, the variant index or the variant name.
            step_num (int): step number
            reset_default_values (bool, optional): If True, all the default values are initially reset. Defaults to True.

    `step_generator(self, set_values_in_pf: bool = True) ‑> Generator[tuple[dict, str], None, None]`
    :

`Variant(pf_app=False, cached=False)`
:   Create variations for parameter studies (not to confuse with the  variation (IntScheme) class of PF).

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Instance variables

    `default_values`
    :   Default values (values) for PF objects, attributes (keys).

    `max: float`
    :

    `min: float`
    :

    `name`
    :   Name of variation

    `number_of_objs: int`
    :

    `objs: list`
    :   Shortcut to get all PF objects

    `objs_and_attr`
    :   The PF objects and their attributes to which the parameter variants are applied. Can be a dict with objects (keys) and attributes (values) or a list where the first element is a list of objects and the second element is the attribute (which is shared by all objects).

    `par_range`
    :   The parameter range.

    `postprocessing_step`
    :   Function that is called at each step after the simulation. Must be defined as a function with one input argument. This argument is a dict that gives access to the following data:
        - "sim_res": DataFrame with simulation results of step
        - "variant": variant
        - "var_num": current variant number
        - "sim_num": current total simulation number
        - "step_num": current step number
        
        IMPORTANT: If the simulation results are changed, the function must return them.

    `preprocessing_step`
    :   Function that is called at each step before the simulation. Must be defined as a function with one input argument. This argument is a dict that gives access to the following data:
        - "variant": variant
        - "var_num": current variant number
        - "step_num": current step number
        - "sim_num": current total simulation number

    `steps`
    :   The number of steps (in the parameter range).

    `value_calculation`
    :   Specifies how the values are calculated. Options are 'equal', 'multiply', 'add'. 'equal' means that the values are just set in PF. 'multiply' means that the attribute values are calculated by multiplying by the default value. 'add' means the attribute values are calculated by adding to the default value.

    `values`
    :   List of values (values) of PF objects, attributes (keys) for all parameter sets

    `variation_type`
    :   Specifies how the parameter values are set for the various PF objects. 'const' means that the same parameter value is set for all PF objects. 'gradient' means that there is a gradient for values that starts at the first object and ends at the last.

    ### Methods

    `execute_postprocessing_step(self, pre_post_process_dict: dict) ‑> None`
    :

    `execute_preprocessing_step(self, pre_post_process_dict: dict) ‑> None`
    :

    `get_current_values_of_all_attr_in_pf(self) ‑> dict`
    :   Get the current (in PF) attribute values of all PF objects.
        
        Returns:
            dict: PF objects, attributes (keys) and attribute values (values)

    `get_list_of_objs_and_attr(self) ‑> list`
    :   Get list of obj, attr tuples.
        
        Returns:
            list: list of obj, attr tuples

    `get_name_for_each_step(self, use_calculated_vales: bool = False) ‑> list[str]`
    :   Get a list of names for each steps. The names consist of 'self.name' and the value of the step (if the values of the targeted PF objects differ, the value of the first object in 'self.values' is used).
        
        Args:
            use_calculated_vales (bool): If True, the calculated values are used, else the values as specified by the user are used. Relevant if self.value_calculation is 'multiply' or 'add. Defaults to False.
        
        Returns:
            list[str]: list of names

    `get_values(self) ‑> dict[powfacpy.pf_classes.protocols.PFGeneral, typing.Any]`
    :   Get the values of each PF object for each step.
        
        Returns:
            dict[PFGeneral, Any]: PF objects, attributes (keys) and list of values (values)

    `initialize(self) ‑> None`
    :

    `set_default_values(self) ‑> None`
    :   Reset the default attribute values in PF.

    `set_values_in_pf(self, step_num: int) ‑> None`
    :   Set the attribute values of the step in PF
        
        Args:
            step_num (int): step number