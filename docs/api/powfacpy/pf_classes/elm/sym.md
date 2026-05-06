Module powfacpy.pf_classes.elm.sym
==================================

Functions
---------

`weight_by_apparent_power_of_synchronous_machines(values: list[float], synchronous_machines: list[SynchronousMachine] | list[ElmSym], return_sum_of_weights: bool = False) ‑> float`
:   

Classes
-------

`SynchronousMachine(obj: ElmSym)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.pf_classes.elm.elm_base.ElmBase
    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic
    * powfacpy.pf_classes.elm.elm_base.SinglePortBase
    * powfacpy.pf_classes.elm.elm_base.ElmPlantControlledBase
    * abc.ABC

    ### Static methods

    `get_cgmes_mapping()`
    :

    ### Instance variables

    `H_in_MWs: float`
    :   Inertia constant [MWs]

    `H_in_seconds_based_on_Snom: float`
    :   Inertia constant [s]

    `J: float`
    :   Moment of Inertia [kgm^2]. Parallel machines are considered.

    `ratedS: float`
    :   Apparent power [MVA]. Parallel machines are considered. 'ratedS' is CGMES conform.

    `rated_apparent_power: float`
    :

    ### Methods

    `add_external_station_controller(self, parent_folder: PFGeneral | None = None, controlled_terminal: ElmTerm | None = None) ‑> None`
    :   Add external station controller.
        
        Args:
            parent_folder (PFGeneral | None, optional): Parent folder of station controller. Defaults to None (same folder as ElmSym is used).
            controlled_terminal (ElmTerm | None, optional): target terminal. Defaults to None.
        
        Returns:
            _type_: _description_

    `get_H_in_seconds(self, base_apparent_power_MVA: float | None = None) ‑> float`
    :   Inertia constant [s]

    `get_approximate_internal_voltage(self) ‑> complex`
    :   Get approximate internal voltage from power supply, terminal voltage and internal reactance.
        
        This is one way a system operator could approximate the internal voltage based on measurements at the point of connection.
        
        Returns:
            complex: approximate internal voltage

    `get_averaged_internal_reactance(self, base_apparent_power_MVA: float | None = None) ‑> float`
    :   Get average of the d-and q-axis internal reactances:
        xG = 0.5 (x''d + x''q)
        
        Returns:
            float: internal reactance [pu]

    `get_averaged_internal_susceptance(self, base_apparent_power_MVA: float | None = None) ‑> float`
    :

    `get_avr(self, error_if_non_existent: bool = True) ‑> powfacpy.pf_classes.protocols.ElmDsl`
    :

    `get_connecting_transformer(self, transformer_class: str = 'ElmTr*') ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :   Gets the next trafo (compared to GetStepupTransformer which requires a voltage level to stop the search)
        
        Args:
            transformer_class (str, optional): _description_. Defaults to "ElmTr2".
        
        Returns:
            PFGeneral: _description_

    `get_governor(self, error_if_non_existent: bool = True) ‑> powfacpy.pf_classes.protocols.ElmDsl`
    :

    `get_pss(self, error_if_non_existent: bool = True) ‑> powfacpy.pf_classes.protocols.ElmDsl`
    :

    `get_terminal_of_transformer_hv_side(self, transformer_class: str = 'ElmTr*') ‑> powfacpy.pf_classes.protocols.ElmTerm`
    :