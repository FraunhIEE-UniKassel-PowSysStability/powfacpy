Module powfacpy.base.functional
===============================
Functional interface.

powfacpy is mainly object oriented and builds upon base classes like 'Folder' or 'ActiveProject'.
This is a collection of helper functions (utils) to be used as an alternative and that can be more performant (for example, only PF objects are accepted and not their path string).

Functions
---------

`set_attr_of_child(parent, child: str, attributes: dict[str, object])`
:   Set attributes of a child object in parent.
    Just syntactic sugar.

`set_attr_of_obj(obj, attributes: dict[str, object]) ‑> None`
:   Set attributes of object.
    
    The difference to set_attr of 'PFFolder' class is that
    this method only accepts PF objects (and not path strings)
    and is slightly more performant.

`set_attr_of_objects(objects: Iterable, attributes: dict[str, object]) ‑> None`
:   Set attributes of multiple objects.