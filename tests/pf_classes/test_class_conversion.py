"""Tests for powfacpy.pf_classes.class_conversion.convert_pf_obj_to_powfacpy.

Uses fake PF objects (only 'GetClassName' is needed) so no PowerFactory
connection is required.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory

from powfacpy.pf_classes.class_conversion import convert_pf_obj_to_powfacpy
from powfacpy.pf_classes.blk.definition import BlockDefinition
from powfacpy.pf_classes.blk.slot import Slot
from powfacpy.pf_classes.elm.comp import CompositeModel
from powfacpy.pf_classes.elm.dsl import DSLModel
from powfacpy.pf_classes.elm.sym import SynchronousMachine


class _FakePFObject:
    def __init__(self, class_name):
        self._class_name = class_name

    def GetClassName(self):
        return self._class_name


@pytest.mark.parametrize(
    "class_name, expected_type",
    [
        ("ElmSym", SynchronousMachine),
        ("ElmDsl", DSLModel),
        ("ElmComp", CompositeModel),
        ("BlkDef", BlockDefinition),
        ("BlkSlot", Slot),
    ],
)
def test_convert_pf_obj_to_powfacpy_maps_known_classes(class_name, expected_type):
    fake = _FakePFObject(class_name)
    converted = convert_pf_obj_to_powfacpy(fake)
    assert isinstance(converted, expected_type)
    assert converted._obj is fake


def test_convert_pf_obj_to_powfacpy_unknown_class_prefix_raises_key_error():
    with pytest.raises(KeyError):
        convert_pf_obj_to_powfacpy(_FakePFObject("XyzFoo"))


def test_convert_pf_obj_to_powfacpy_known_prefix_unknown_suffix_raises_key_error():
    # 'Elm' prefix is known, but no mapping for e.g. 'ElmTerm'
    with pytest.raises(KeyError):
        convert_pf_obj_to_powfacpy(_FakePFObject("ElmTerm"))


if __name__ == "__main__":
    pytest.main([__file__])
