from __future__ import annotations

from icecream import ic

from powfacpy.pf_classes.protocols import PFGeneral
from powfacpy.applications.caching import (
    cache_attr,
    cache_method,
)


class BaseObjectStatic:
    """Base class that can be used to store a PF object (in attribute '_obj'). Adds functionality for checking equality and string representation. Uses slots for efficient attribute access and memory usage (read more about slots in the documentation: https://wiki.python.org/moin/UsingSlots)."""

    __slots__ = "_obj"

    def __init__(self, obj: PFGeneral) -> None:
        self._obj: PFGeneral = obj

    def __eq__(self, value: BaseObjectStatic) -> bool:
        """Check equality with a PF object.

        Args:
            value (BaseObjectStatic)

        Returns:
            bool: If equal
        """
        return self._obj == value._obj

    def __str__(self):
        """Returns the 'loc_name' of the PF object."""
        return self._obj.loc_name

    @property
    def obj(self):
        return self._obj


class BaseChildStatic(BaseObjectStatic):
    """
    Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.

    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).

    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').
    """

    __slots__ = ()

    def __init__(self, obj: PFGeneral) -> None:
        super(BaseChildStatic, self).__setattr__("_obj", obj)

    def __getattribute__(self, attr):
        _obj = super(BaseChildStatic, self).__getattribute__("_obj")
        if attr == "_obj":
            return _obj
        try:
            return _obj.__getattribute__(attr)
        except AttributeError:
            try:
                return _obj.__getattr__(attr)
            except AttributeError:  # Fallback that should never happen
                return super(BaseChildStatic, self).__getattribute__(attr)

    def __setattr__(self, attr, value):
        if hasattr(self._obj, attr):
            self._obj.__setattr__(attr, value)
        else:
            super(BaseChildStatic, self).__setattr__(attr, value)

    def cache_attr(self, attr: str) -> None:
        cache_attr(self._obj, attr)

    def cache_method(self, method: str):
        cache_method(self._obj, method)


class BaseChild(BaseChildStatic):
    """This is a dynamic alternative to 'BaseChildStatic', i.e. just by declaring the class (without '__slots__ = ()', a '__dict__' is added and attributes can be added dynamical by any class that inherits from 'BaseChild'"""
