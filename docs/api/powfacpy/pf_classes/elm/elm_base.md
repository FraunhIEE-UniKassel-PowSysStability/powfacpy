Module powfacpy.pf_classes.elm.elm_base
=======================================

Classes
-------

`ElmBase(obj: PFGeneral)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic

    ### Descendants

    * powfacpy.pf_classes.elm.area.AreaStatic
    * powfacpy.pf_classes.elm.boundary.Boundary
    * powfacpy.pf_classes.elm.comp.CompositeModel
    * powfacpy.pf_classes.elm.dsl.DSLModel
    * powfacpy.pf_classes.elm.file.MeasurementFile
    * powfacpy.pf_classes.elm.sym.SynchronousMachine
    * powfacpy.pf_classes.elm.term.Terminal
    * powfacpy.pf_classes.elm.zone.ZoneStatic

    ### Methods

    `get_parent_grid(self) ‑> powfacpy.pf_classes.protocols.ElmNet`
    :

    `set_into_service(self)`
    :

    `set_out_of_service(self)`
    :

`ElmPlantControlledBase()`
:   Elm that can be part of DSL frame (has attribute 'c_pmod' that points to a composite frame, i.e. a plant model).

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * powfacpy.pf_classes.elm.sym.SynchronousMachine

    ### Instance variables

    `composite_frame: ElmComp`
    :

    ### Methods

    `get_network_elements_of_plant_model(self, condition: Callable | None = None, error_if_non_existent: bool = True) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Get network elements of plant model (composite frame) on condition.
        
        Args:
            condition (Callable | None, optional): Condition to select network elements, e.g. 'lambda x: x.typ_id.loc_name.startswith("gov_")' to get governors. Defaults to None.
            error_if_non_existent (bool, optional): Raise exception if no objects that satisfy condition are found. Defaults to True.
        
        Raises:
            PFInvalidCondition: If no objects that satisfy condition are found.
        
        Returns:
            list[PFGeneral]: Network elements

`SinglePortBase()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * powfacpy.pf_classes.elm.sym.SynchronousMachine

    ### Instance variables

    `p`
    :

    `q`
    :

    `terminal`
    :

    ### Methods

    `rated_apparent_power() ‑> float`
    :