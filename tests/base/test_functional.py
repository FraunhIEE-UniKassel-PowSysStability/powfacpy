"""Tests for powfacpy.base.functional.

Uses a minimal fake PF object (only 'SetAttribute' / 'GetContents' are needed) so
no PowerFactory connection is required.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory

from powfacpy.base.functional import (
    set_attr_of_obj,
    set_attr_of_objects,
    set_attr_of_child,
)


class _FakePFObject:
    def __init__(self, loc_name="fake", children=None):
        self.loc_name = loc_name
        self._children = children or {}

    def SetAttribute(self, attr, value):
        setattr(self, attr, value)

    def GetContents(self, name):
        return [self._children[name]]


def test_set_attr_of_obj():
    obj = _FakePFObject()
    set_attr_of_obj(obj, {"outserv": 1, "pgini": 42.0})
    assert obj.outserv == 1
    assert obj.pgini == 42.0


def test_set_attr_of_objects():
    obj1, obj2 = _FakePFObject("a"), _FakePFObject("b")
    set_attr_of_objects([obj1, obj2], {"outserv": 1})
    assert obj1.outserv == 1
    assert obj2.outserv == 1


def test_set_attr_of_child():
    child = _FakePFObject("child")
    parent = _FakePFObject("parent", children={"child": child})
    set_attr_of_child(parent, "child", {"pgini": 7.5})
    assert child.pgini == 7.5


if __name__ == "__main__":
    pytest.main([__file__])
