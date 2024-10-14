from __future__ import annotations

from icecream import ic

from powfacpy.pf_classes.protocols import PFGeneral
from powfacpy.applications.caching import (
    cache_attr,
    cache_attrs,
    cache_method,
    cache_methods,
)


class BaseObjectStatic:
    __slots__ = "_obj"

    def __init__(self, obj: PFGeneral) -> None:
        self._obj: PFGeneral = obj

    def __eq__(self, value: object) -> bool:
        return self._obj == value

    def __str__(self):
        return self._obj.loc_name

    @property
    def obj(self):
        return self._obj


class BaseChildStatic(BaseObjectStatic):
    __slots__ = ()
    """
    Child in object oriented sense (not like in GetParent())
    __dict__ are used to avoid infinite recursion of __getattr__ and __setattr__ calls
    __getattr__ is apparently called when __getattribute__ fails
    """

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
            except AttributeError:  # Should never happen
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
    """Adds '__dict__'"""
