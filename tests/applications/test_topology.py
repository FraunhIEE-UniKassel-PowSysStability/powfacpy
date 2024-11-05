from powfacpy.result_variables import ResVar
from powfacpy.pf_classes.protocols import PFGeneral, ElmZone
from powfacpy.applications.topology import Topology
from powfacpy.base.active_project import ActiveProject
import sys

import pytest

sys.path.insert(0, r".\src")
RMS_BAL = ResVar.RMS_Bal


@pytest.fixture(scope="function")
def create_zone(
    act_prj: ActiveProject, activate_39_bus_new_england_test_project
) -> tuple[ElmZone, list[PFGeneral]]:
    topo = Topology()
    terminals = act_prj.get_calc_relevant_obj(
        "Bus 36.ElmTerm, Bus 23.ElmTerm, Bus 22.ElmTerm, Bus 35.ElmTerm"
    )
    zone = topo.create_zone("South-East", terminals)
    return zone, terminals


def test_create_boundary(create_zone):
    zone, terminals = create_zone
    all_elms_in_zone = zone.GetAll()
    topo = Topology()

    boundary_without_changing = topo.create_boundary_without_changing_initial_zones(
        "South-East-without-changing", terminals
    )
    assert zone.GetAll() == all_elms_in_zone

    boundary_with_changing = topo.create_boundary_using_intermediate_zone(
        "South-East-with-changing", terminals
    )
    assert not (zone.GetAll() == all_elms_in_zone)

    assert (
        boundary_with_changing.GetInterior() == boundary_without_changing.GetInterior()
    )


if __name__ == "__main__":
    pytest.main([r"tests\applications\test_topology.py"])
