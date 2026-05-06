Module powfacpy.pf_classes.set.colscheme
========================================

Classes
-------

`DiagramColorScheme(obj: SetColscheme)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic

    ### Static methods

    `reactivate_study_case() ‑> None`
    :   The PF GUI might not react to the new settings. A reliable way to update the GUI is to reactivate the study case.

    ### Methods

    `show_areas(self, reactivate_study_case: bool = True) ‑> None`
    :

    `show_boundary_interior_regions(self, reactivate_study_case: bool = True) ‑> None`
    :

    `show_zones(self, reactivate_study_case: bool = True) ‑> None`
    :