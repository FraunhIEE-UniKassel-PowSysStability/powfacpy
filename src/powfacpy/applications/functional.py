"""Functional interface.
powfacpy is mainly object oriented and builds upon base calsses like PFFolder or PFActive project.
This is a collection of helper functions (utils) to be used as an alternative and that can be more performant (for example, only PF onjects are accepted and not their path). 
"""
from typing import Iterable


def set_attr_of_obj(obj, attributes: dict[str, object]) -> None:
    """Set attributes of object.
    
    The difference to set_attr of 'PFFolder' class is that
    this method only accepts PF objects (and not path strings)
    and is slightly more performant.
    """
    for attr, value in attributes.items():
        obj.SetAttribute(attr, value)


def set_attr_of_objects(objects: Iterable, attributes: dict[str, object]) -> None:
    """Set attributes of multiple objects.
    """
    for obj in objects:
        set_attr_of_obj(obj, attributes)


def set_attr_of_child(parent, child: str, attributes: dict[str, object]):
    """Set attributes of a child object in parent.
    Just syntactic sugar.
    """
    child = parent.GetContents(child)[0]
    for attr, value in attributes.items():
        child.SetAttribute(attr, value)
