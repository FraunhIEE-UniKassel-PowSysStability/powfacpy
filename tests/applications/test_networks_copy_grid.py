"""Tests for `Networks.copy_grid`.

Uses a small synthetic source grid (not the full 39-bus network - activating a
duplicate of that corrupts the RMS engine for the rest of the session). The
diagram copy + re-link path is exercised end-to-end by the amprion
`model-creation` notebook and covered here only for the no-diagram case.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.base.active_project import ActiveProject
from powfacpy.applications.networks import Networks

STUDY_CASE = r"Study Cases\2.3 Simulation Fault Bus 31 Stable"


@pytest.fixture
def setup(pf_app, copy_39_bus_new_england_test_project):
    """(networks, active_project, source_grid) with a 2-bus synthetic source grid."""
    copy_39_bus_new_england_test_project.Activate()
    act_prj = ActiveProject(pf_app)
    study_case = act_prj.get_unique_obj(STUDY_CASE)
    study_case.Activate()
    networks = Networks(pf_app)
    net_data = act_prj.network_data_folder

    def cleanup():
        study_case.Deactivate()
        for name in ("Mini Source", "Mini Copy"):
            for leftover in net_data.GetContents(f"{name}.ElmNet"):
                leftover.Delete()
        study_case.Activate()

    cleanup()

    source = act_prj.create_in_folder("Mini Source.ElmNet", net_data)
    source.Activate()
    bus = act_prj.create_in_folder("Bus.ElmTerm", source)
    bus.SetAttribute("uknom", 110.0)
    xnet = act_prj.create_in_folder("Slack.ElmXnet", source)
    xnet.SetAttribute("bus1", networks.get_vacant_cubicle_of_terminal(bus))
    xnet.SetAttribute("bustp", "SL")
    load = act_prj.create_in_folder("Load.ElmLod", source)
    load.SetAttribute("bus1", networks.get_vacant_cubicle_of_terminal(bus))
    load.SetAttribute("plini", 10.0)

    yield networks, act_prj, source
    cleanup()


def test_copy_grid_copies_the_full_topology(setup):
    networks, act_prj, source = setup
    net_data = act_prj.network_data_folder

    copy = networks.copy_grid(source, net_data, "Mini Copy")

    assert copy.GetClassName() == "ElmNet"
    assert copy.loc_name == "Mini Copy"
    assert copy.IsCalcRelevant()  # always activated once
    for pattern in ("*.ElmTerm", "*.ElmXnet", "*.ElmLod"):
        assert len(copy.GetContents(pattern)) == len(source.GetContents(pattern))
    copied_load = act_prj.get_unique_obj("Load", parent_folder=copy)
    assert copied_load.GetAttribute("bus1").cterm == act_prj.get_unique_obj(
        "Bus", parent_folder=copy
    )
    assert act_prj.app.GetFromStudyCase("ComLdf").Execute() == 0


def test_copy_grid_deactivate_switches_the_copy_back_off(setup):
    networks, act_prj, source = setup
    copy = networks.copy_grid(
        source, act_prj.network_data_folder, "Mini Copy", deactivate=True
    )
    assert not copy.IsCalcRelevant()
    # the connections still resolve once re-activated (stored on the cubicles)
    copy.Activate()
    assert (
        act_prj.get_unique_obj("Load", parent_folder=copy).GetAttribute("bus1")
        is not None
    )


def test_copy_grid_without_diagram_is_a_no_op_for_the_diagram(setup):
    networks, act_prj, source = setup
    assert source.pDiagram is None
    copy = networks.copy_grid(
        source, act_prj.network_data_folder, "Mini Copy", copy_diagram=False
    )
    assert copy.pDiagram is None


def test_copy_grid_use_existing_returns_the_first_copy(setup):
    networks, act_prj, source = setup
    net_data = act_prj.network_data_folder
    first = networks.copy_grid(source, net_data, "Mini Copy", deactivate=True)
    second = networks.copy_grid(
        source, net_data, "Mini Copy", deactivate=True, use_existing=True
    )
    assert first.GetFullName() == second.GetFullName()
    assert len(net_data.GetContents("Mini Copy.ElmNet")) == 1


if __name__ == "__main__":
    pytest.main([__file__])
