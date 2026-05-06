Module powfacpy.pf_classes.elm.term
===================================

Classes
-------

`Terminal(obj: ElmTerm)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.pf_classes.elm.elm_base.ElmBase
    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic

    ### Methods

    `add_phase_locked_loop(self, folder: PFGeneral | None = None, monitor_frequency_pu: bool = False, monitor_frequency_Hz: bool = False) ‑> powfacpy.pf_classes.protocols.StaPll`
    :   Add a PLL to monitor the frequency.
        
        Args:
            folder (PFGeneral | None, optional): parent folder. Defaults to None (parent grid folder is used).
            monitor_frequency_pu (bool, optional): monitor frequency in pu. Defaults to False.
            monitor_frequency_Hz (bool, optional): monitor frequency in Hz. Defaults to False.
        
        Returns:
            StaPll: Created PLL object

    `get_connected_elements(self, only_calc_relevant: bool = False, condition: Callable | None = None) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Get all elements connected to terminal.
        
        Args:
            only_calc_relevant (bool, optional): Only calculation relevant elements are considered. Defaults to False.
            condition (Callable | None, optional): Condition to select elements. Defaults to None.
        
        Returns:
            list[PFGeneral]: Connected elements

    `get_cubicle_of_connected_elm(self, elm: PFGeneral) ‑> powfacpy.pf_classes.protocols.StaCubic`
    :