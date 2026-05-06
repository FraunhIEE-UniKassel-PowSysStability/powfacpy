Module powfacpy.applications.static_calc
========================================
Module with interface for static calculations (load flow, short circuits,..)

Classes
-------

`StaticCalc(pf_app: powfacpy.pf_classes.protocols.PFApp | None | bool = False, cached: bool = False)`
:   Static calculation (e.g. load flow, short circuit,..) interface

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Methods

    `check_load_flow_results(self, when_invalid: str = 'error') ‑> bool`
    :   Check whether load flow results in PF are present and valid and raise exception, warning or execute load flow if not.
        
        Args:
            when_invalid (str, optional): If load flow results are invalid, 'error' (raises exception), 'warning' raises warning, 'execute' executes load flow and raises exception if results are invalid. Defaults to "error".
        
        Raises:
            PFInvalidLoadFlow: When load flow results are invalid and 'when_invalid'= 'error' or 'execute' and results are invalid.
        
        Returns:
            bool: True only when results are valid.

    `create_secondary_controller(self, name: str | None = None, parent_folder: powfacpy.pf_classes.protocols.PFGeneral | None = None, controlled_objs: list[powfacpy.pf_classes.protocols.PFGeneral] | None = None, attr: dict | None = None) ‑> powfacpy.pf_classes.protocols.ElmSecctrl`
    :   Create secondary controller (ElmSecctrl)
        
        Args:
            name (str | None, optional): Name of ElmSecctrl. Defaults to None.
            parent_folder (PFGeneral | None, optional): Parent folder. Defaults to None.
            controlled_objs (list[PFGeneral] | None, optional): Network elements that are controlled ('psym' attribute). Defaults to None.
            attr (dict | None, optional): Attributes (keys) and their values (values) of teh created ElmSecctrl to be set. Defaults to None.
        
        Returns:
            ElmSecctrl: _description_

    `execute_load_flow(self, params: dict = {}) ‑> int`
    :

    `get_result_dataframe(self, objs: list[powfacpy.pf_classes.protocols.PFGeneral], resvars: list[str]) ‑> pandas.core.frame.DataFrame`
    :

    `has_valid_load_flow_results(self) ‑> bool`
    :

    `replace_obj_with_loc_name_and_add_variable_desc(self, df: pandas.core.frame.DataFrame, simulation_type: str = 'LF_Bal') ‑> pandas.core.frame.DataFrame`
    :