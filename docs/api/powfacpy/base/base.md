Module powfacpy.base.base
=========================

Classes
-------

`BaseChild(obj: PFGeneral)`
:   This is a dynamic alternative to 'BaseChildStatic', i.e. just by declaring the class (without '__slots__ = ()', a '__dict__' is added and attributes can be added dynamical by any class that inherits from 'BaseChild'

    ### Ancestors (in MRO)

    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic

`BaseChildStatic(obj: PFGeneral)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.base.base.BaseObjectStatic

    ### Descendants

    * powfacpy.base.base.BaseChild
    * powfacpy.pf_classes.blk.definition.BlockDefinition
    * powfacpy.pf_classes.blk.slot.Slot
    * powfacpy.pf_classes.elm.elm_base.ElmBase
    * powfacpy.pf_classes.set.colscheme.DiagramColorScheme
    * powfacpy.pf_classes.sta.pll.PhaseLockedLoop

    ### Methods

    `cache_attr(self, attr: str) ‑> None`
    :

    `cache_method(self, method: str)`
    :

`BaseObjectStatic(obj: PFGeneral)`
:   Base class that can be used to store a PF object (in attribute '_obj'). Adds functionality for checking equality and string representation. Uses slots for efficient attribute access and memory usage (read more about slots in the documentation: https://wiki.python.org/moin/UsingSlots).

    ### Descendants

    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.folder.Folder

    ### Instance variables

    `obj`
    :