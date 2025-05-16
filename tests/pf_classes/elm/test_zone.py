import sys

import pytest

sys.path.insert(0, r".\src")
sys.path.insert(0, r".\tests")

from powfacpy.pf_classes.elm.zone import Zone
from powfacpy.base.active_project import ActiveProject

from applications.test_topology import create_zone
from powfacpy.result_variables import ResVar

RMS_BAL = ResVar.RMS_Bal


def test_get_all_internal_elms(create_zone) -> None:
    zone, terminals = create_zone
    zone = Zone(zone)
    all_internal_elms = zone.get_all_internal_elms()
    assert set(terminals).issubset(all_internal_elms)


if __name__ == "__main__":
    pytest.main([r"tests\pf_classes\elm\test_zone.py"])
