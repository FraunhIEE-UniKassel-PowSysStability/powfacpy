"""Tests for `Networks.connect` - wire the single open cubicle of a branch
element to a terminal.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.base.active_project import ActiveProject
from powfacpy.applications.networks import Networks
from powfacpy.exceptions import PFInterfaceError

STUDY_CASE = r"Study Cases\2.3 Simulation Fault Bus 31 Stable"


@pytest.fixture
def setup(pf_app, copy_39_bus_new_england_test_project):
    """(networks, active_project, grid); removes the ``Extras`` grid it creates."""
    copy_39_bus_new_england_test_project.Activate()
    act_prj = ActiveProject(pf_app)
    study_case = act_prj.get_unique_obj(STUDY_CASE)
    study_case.Activate()
    networks = Networks(pf_app)
    net_data = act_prj.network_data_folder
    grid = act_prj.get_unique_obj("Grid", parent_folder=net_data)

    def cleanup():
        study_case.Deactivate()
        for leftover in net_data.GetContents("Extras.ElmNet"):
            leftover.Delete()
        study_case.Activate()

    cleanup()
    yield networks, act_prj, grid
    cleanup()


def test_connect_wires_the_open_cubicle_of_a_breaker(setup):
    networks, act_prj, grid = setup
    net_data = act_prj.network_data_folder
    extras = act_prj.create_in_folder("Extras.ElmNet", net_data)
    extras.Activate()

    bus_a = act_prj.get_unique_obj("Bus 15", parent_folder=grid)
    bus_b = act_prj.get_unique_obj("Bus 16", parent_folder=grid)
    breaker = act_prj.create_in_folder("Tie.ElmCoup", extras)
    breaker.SetAttribute("aUsage", "cbk")
    breaker.SetAttribute("bus1", networks.get_vacant_cubicle_of_terminal(bus_a))
    assert breaker.GetAttribute("bus2") is None

    cubicle = networks.connect(breaker, bus_b)

    assert cubicle.cterm == bus_b
    assert breaker.GetAttribute("bus2") == cubicle
    assert breaker.GetAttribute("bus1").cterm == bus_a
    assert act_prj.app.GetFromStudyCase("ComLdf").Execute() == 0


def test_connect_needs_exactly_one_open_cubicle(setup):
    networks, act_prj, grid = setup
    net_data = act_prj.network_data_folder
    extras = act_prj.create_in_folder("Extras.ElmNet", net_data)

    fully_open = act_prj.create_in_folder("Both open.ElmCoup", extras)
    with pytest.raises(PFInterfaceError, match="disconnected cubicle"):
        networks.connect(fully_open, act_prj.get_unique_obj("Bus 15", parent_folder=grid))

    bus_a = act_prj.get_unique_obj("Bus 15", parent_folder=grid)
    bus_b = act_prj.get_unique_obj("Bus 16", parent_folder=grid)
    fully_wired = act_prj.create_in_folder("Both wired.ElmCoup", extras)
    fully_wired.SetAttribute(
        "bus1", networks.get_vacant_cubicle_of_terminal(bus_a)
    )
    fully_wired.SetAttribute(
        "bus2", networks.get_vacant_cubicle_of_terminal(bus_b)
    )
    with pytest.raises(PFInterfaceError, match="disconnected cubicle"):
        networks.connect(fully_wired, bus_a)


if __name__ == "__main__":
    pytest.main([__file__])
