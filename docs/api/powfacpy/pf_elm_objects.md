Module powfacpy.pf_elm_objects
==============================

Functions
---------

`create_elm_object(pf_elm_object) ‑> powfacpy.pf_elm_objects.PFElm`
:   

Classes
-------

`Area(pf_obj: ElmArea)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * powfacpy.pf_elm_objects.PFElm
    * abc.ABC
    * powfacpy.pf_classes.protocols.PFGeneral
    * typing.Protocol
    * typing.Generic

    ### Methods

    `get_P_exchange_res_var_lf_bal() ‑> str`
    :

    `get_P_exchange_res_var_rms_bal() ‑> str`
    :

    `get_Q_exchange_res_var_lf_bal() ‑> str`
    :

    `get_Q_exchange_res_var_rms_bal() ‑> str`
    :

`Line(pf_obj: ElmLne)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * powfacpy.pf_elm_objects.PFElm
    * abc.ABC
    * powfacpy.pf_classes.protocols.PFGeneral
    * typing.Protocol
    * typing.Generic

    ### Methods

    `get_P_res_var_lf_bal(self, bus_index: int | slice = slice(0, None, None))`
    :

    `get_P_res_var_rms_bal(self, bus_index: int | slice = slice(0, None, None))`
    :

    `get_Q_res_var_lf_bal(self, bus_index: int | slice = slice(0, None, None))`
    :

    `get_Q_res_var_rms_bal(self, bus_index: int | slice = slice(0, None, None))`
    :

    `get_connected_elms_ordered(self) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :

`PFElm(pf_obj)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC
    * powfacpy.pf_classes.protocols.PFGeneral
    * typing.Protocol
    * typing.Generic

    ### Descendants

    * powfacpy.pf_elm_objects.Area
    * powfacpy.pf_elm_objects.Line
    * powfacpy.pf_elm_objects.Site
    * powfacpy.pf_elm_objects.StaticGenerator
    * powfacpy.pf_elm_objects.SynchronousMachine
    * powfacpy.pf_elm_objects.Terminal
    * powfacpy.pf_elm_objects.Transformer2Winding
    * powfacpy.pf_elm_objects.Transformer3Winding
    * powfacpy.pf_elm_objects.Zone

    ### Methods

    `get_bus_index_of_terminal(self, connected_terminal: ElmTerm)`
    :

    `set_into_service(self)`
    :

    `set_out_of_service(self)`
    :

`Site(pf_obj: ElmSite)`
:   Network components including Substations and Branches can be grouped together within a “Site” (ElmSite). This may include Elements such as substations / busbars at different voltage levels.
    (from manual)

    ### Ancestors (in MRO)

    * powfacpy.pf_elm_objects.PFElm
    * abc.ABC
    * powfacpy.pf_classes.protocols.PFGeneral
    * typing.Protocol
    * typing.Generic

    ### Methods

    `get_substations(self)`
    :

    `set_area_of_substations(self, area: ElmArea)`
    :

    `set_zone_of_substations(self, zone: ElmZone)`
    :

`StandardLoadFlowElm()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * powfacpy.pf_elm_objects.StaticGenerator
    * powfacpy.pf_elm_objects.SynchronousMachine

    ### Instance variables

    `P: float`
    :

    `P_max: float`
    :

    `P_min: float`
    :

    `Q: float`
    :

    `Q_max: float`
    :

    `Q_min: float`
    :

    `S: float`
    :

    `S_nom: float`
    :

    `p_max_pu: float`
    :

    `p_min_pu: float`
    :

    `p_pu: float`
    :

    `q_max_pu: float`
    :

    `q_min_pu: float`
    :

    `q_pu: float`
    :

    `s_pu: float`
    :

    `u`
    :

    ### Methods

    `get_P_margin(self) ‑> tuple[float, float]`
    :

    `get_Q_margin(self) ‑> tuple[float, float]`
    :

    `get_p_margin_pu(self) ‑> tuple[float, float]`
    :

    `get_q_margin_pu(self) ‑> tuple[float, float]`
    :

    `scale_p(self, factor: float)`
    :

    `scale_q(self, factor: float)`
    :

    `scale_s(self, factor: float)`
    :

    `set_dispatch_input_mode(self, mode)`
    :

    `set_p_and_adapt_limits(self, p_pu)`
    :

    `set_q_and_adapt_limits(self, q_pu)`
    :

`StaticGenerator(pf_obj: ElmGenstat)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * powfacpy.pf_elm_objects.PFElm
    * powfacpy.pf_elm_objects.StandardLoadFlowElm
    * abc.ABC
    * powfacpy.pf_classes.protocols.PFGeneral
    * typing.Protocol
    * typing.Generic

    ### Methods

    `get_connected_elms_ordered(self) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :

    `set_short_circuit_impedance_uk(self, uk) ‑> None`
    :

`SynchronousMachine(pf_obj: ElmSym)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * powfacpy.pf_elm_objects.PFElm
    * powfacpy.pf_elm_objects.StandardLoadFlowElm
    * abc.ABC
    * powfacpy.pf_classes.protocols.PFGeneral
    * typing.Protocol
    * typing.Generic

    ### Instance variables

    `S_nom: float`
    :

    ### Methods

    `get_connected_elms_ordered(self) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :

    `set_local_controller_mode_for_load_flow(self, mode)`
    :

`Terminal(pf_obj: ElmTerm)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * powfacpy.pf_elm_objects.PFElm
    * abc.ABC
    * powfacpy.pf_classes.protocols.PFGeneral
    * typing.Protocol
    * typing.Generic

    ### Methods

    `get_connected_elms_ordered(self) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :

`Transformer2Winding(pf_obj: ElmTr2)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * powfacpy.pf_elm_objects.PFElm
    * abc.ABC
    * powfacpy.pf_classes.protocols.PFGeneral
    * typing.Protocol
    * typing.Generic

    ### Methods

    `get_P_res_var_rms_bal(self, bus_index: int | slice = slice(0, None, None))`
    :

    `get_Q_res_var_rms_bal(self, bus_index: int | slice = slice(0, None, None))`
    :

    `get_connected_elms_ordered(self) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :

`Transformer3Winding(pf_obj: ElmTr3)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * powfacpy.pf_elm_objects.PFElm
    * abc.ABC
    * powfacpy.pf_classes.protocols.PFGeneral
    * typing.Protocol
    * typing.Generic

    ### Methods

    `get_connected_elms_ordered(self) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :

`Zone(pf_obj: ElmZone)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * powfacpy.pf_elm_objects.PFElm
    * abc.ABC
    * powfacpy.pf_classes.protocols.PFGeneral
    * typing.Protocol
    * typing.Generic

    ### Static methods

    `get_P_exchange_res_var_lf_bal() ‑> str`
    :

    `get_P_exchange_res_var_rms_bal() ‑> str`
    :

    `get_Q_exchange_res_var_lf_bal() ‑> str`
    :

    `get_Q_exchange_res_var_rms_bal() ‑> str`
    :

    ### Methods

    `add_results_variable_F_rms_bal_of_all_terminals(self, pfp: ActiveProject) ‑> None`
    :

    `add_results_variable_f_rms_bal_of_all_terminals(self, pfp: ActiveProject) ‑> None`
    :