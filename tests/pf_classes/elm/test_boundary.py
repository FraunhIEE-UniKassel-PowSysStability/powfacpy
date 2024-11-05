import sys

import pytest

sys.path.insert(0, r".\src")
from powfacpy.pf_classes.elm.boundary import Boundary
from powfacpy.base.active_project import ActiveProject
from powfacpy.applications.topology import Topology
from powfacpy.pf_classes.protocols import PFGeneral
from powfacpy.result_variables import ResVar

RMS_BAL = ResVar.RMS_Bal


@pytest.fixture(scope="function")
def create_boundary(
    act_prj: ActiveProject, activate_39_bus_new_england_test_project
) -> tuple[Boundary, list[PFGeneral]]:
    topo = Topology()
    terminals = act_prj.get_calc_relevant_obj(
        "Bus 36.ElmTerm, Bus 23.ElmTerm, Bus 22.ElmTerm, Bus 35.ElmTerm"
    )
    boundary = topo.create_boundary_without_changing_initial_zones(
        "South-East", terminals
    )
    return boundary, terminals


def test_get_all_internal_elms(create_boundary):
    boundary, terminals = create_boundary
    boundary = Boundary(boundary)
    internal_terminals = boundary.get_internal_elms(
        condition=lambda x: x.GetClassName() == "ElmTerm"
    )
    assert len(internal_terminals) == len(terminals)


def test_add_results_variable_for_elms(create_boundary):
    boundary, terminals = create_boundary
    boundary = Boundary(boundary)
    boundary.add_results_variable_for_elms(
        lambda x: x.GetClassName() == "ElmTerm",
        [RMS_BAL.ElmTerm.m_fe.value, RMS_BAL.ElmTerm.m_u.value],
    )


def test_caching(create_boundary):
    boundary, terminals = create_boundary
    boundary = Boundary(boundary)
    boundary.cache_method("GetInterior")
    assert boundary.GetInterior() == boundary._obj.GetInterior()


if __name__ == "__main__":
    pytest.main([r"tests\pf_classes\elm\test_boundary.py"])
