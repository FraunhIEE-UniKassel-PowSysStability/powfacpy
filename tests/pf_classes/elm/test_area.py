import sys

import pytest

sys.path.insert(0, r".\src")
sys.path.insert(0, r".\tests")

from powfacpy.pf_classes.elm.area import Area
from applications.test_topology import create_area
from powfacpy.result_variables import ResVar

RMS_BAL = ResVar.RMS_Bal


def test_get_all_internal_elms(create_area) -> None:
    area, terminals = create_area
    area = Area(area)
    all_internal_elms = area.get_all_internal_elms()
    assert set(terminals).issubset(all_internal_elms)


def test_get_internal_elms_of_class(create_area) -> None:
    area, terminals = create_area
    area = Area(area)
    internal_terminals = area.get_internal_elms_of_class("ElmTerm")
    assert len(internal_terminals) == len(terminals)


if __name__ == "__main__":
    pytest.main([r"tests\pf_classes\elm\test_area.py"])
