Module powfacpy.pf_classes.elm.comp
===================================

Classes
-------

`CompositeModel(obj: ElmComp)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.pf_classes.elm.elm_base.ElmBase
    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic

    ### Methods

    `export_block_diagram(self, target_dir: str = '.\\', file_name: str = '', format: str = 'svg') ‑> tuple[str, int]`
    :   Export the block diagram.
        
        Args:
            target_dir (str, optional): target directory. Defaults to ".".
            file_name (str, optional): File name. Defaults to "".
            format (str, optional): _description_. Defaults to "svg".
        
        Returns:
            tuple[str, int]: The path of the exported graphic and returned value of the PF 'comwr' object (0: successful export, 1: not successful)

    `get_dsl_models_in_slots(self) ‑> list[powfacpy.pf_classes.protocols.ElmDsl]`
    :   Get all network elements in the slots that are of class 'ElmDsl'

    `get_network_elms(self) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :

    `get_slots(self) ‑> list[powfacpy.pf_classes.protocols.BlkSlot]`
    :

    `get_slots_and_network_elms_dict(self, include_empty_slots: bool = True) ‑> dict[powfacpy.pf_classes.protocols.BlkSlot, powfacpy.pf_classes.protocols.PFGeneral]`
    :   Get all slots and respective network elements.
        
        Args:
            include_empty_slots (bool, optional): If true, slots without network elements are included. Defaults to True.
        
        Returns:
            dict[BlkSlot, PFGeneral]: slots (keys) and respective network elements (values)

    `show_block_diagram(self) ‑> None`
    :   Show the graphic of the composite model