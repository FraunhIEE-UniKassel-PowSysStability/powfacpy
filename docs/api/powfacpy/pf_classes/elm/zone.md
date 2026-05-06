Module powfacpy.pf_classes.elm.zone
===================================

Classes
-------

`Zone(obj: ElmZone)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.pf_classes.elm.zone.ZoneStatic
    * powfacpy.pf_classes.elm.elm_base.ElmBase
    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic
    * powfacpy.pf_classes.elm.grouping_base.AreaZoneBase
    * powfacpy.pf_classes.elm.grouping_base.GroupingBase
    * abc.ABC

    ### Descendants

    * powfacpy.applications.subsystems.SubSystem

`ZoneStatic(obj: ElmZone)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.pf_classes.elm.elm_base.ElmBase
    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic
    * powfacpy.pf_classes.elm.grouping_base.AreaZoneBase
    * powfacpy.pf_classes.elm.grouping_base.GroupingBase
    * abc.ABC

    ### Descendants

    * powfacpy.pf_classes.elm.zone.Zone

    ### Static methods

    `get_P_exchange_res_var_lf_bal() ‑> str`
    :

    `get_P_exchange_res_var_rms_bal() ‑> str`
    :

    `get_Q_exchange_res_var_lf_bal() ‑> str`
    :

    `get_Q_exchange_res_var_rms_bal() ‑> str`
    :

    `show_zones_in_network_graphic(reactivate_study_case: bool = True) ‑> None`
    :   Shows interior regions of all areas in the single line diagram.

    ### Methods

    `get_internal_elms_of_class(self, class_name: str, condition: Callable | None = None) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :