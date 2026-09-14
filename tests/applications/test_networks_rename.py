"""Tests for `Networks.rename_children` and `Networks.rename_drawn_elements`."""

import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.base.active_project import ActiveProject
from powfacpy.applications.networks import Networks
from powfacpy.exceptions import PFInterfaceError

STUDY_CASE = r"Study Cases\2.3 Simulation Fault Bus 31 Stable"


@pytest.fixture
def grid_with_diagram(pf_app, copy_39_bus_new_england_test_project):
    """A small synthetic grid: a bus (drawn) + slack (not drawn) + load (drawn)."""
    copy_39_bus_new_england_test_project.Activate()
    act_prj = ActiveProject(pf_app)
    study_case = act_prj.get_unique_obj(STUDY_CASE)
    study_case.Activate()
    networks = Networks(pf_app)
    net_data = act_prj.network_data_folder
    diagram_folder = act_prj.app.GetProjectFolder("dia")

    def cleanup():
        study_case.Deactivate()
        for leftover in net_data.GetContents("Mini.ElmNet"):
            leftover.Delete()
        for leftover in diagram_folder.GetContents("Mini.IntGrfnet"):
            leftover.Delete()
        study_case.Activate()

    cleanup()

    grid = act_prj.create_in_folder("Mini.ElmNet", net_data)
    grid.Activate()
    bus = act_prj.create_in_folder("Bus.ElmTerm", grid)
    bus.SetAttribute("uknom", 110.0)
    slack = act_prj.create_in_folder("Slack.ElmXnet", grid)
    slack.SetAttribute("bus1", networks.get_vacant_cubicle_of_terminal(bus))
    slack.SetAttribute("bustp", "SL")
    load = act_prj.create_in_folder("Load.ElmLod", grid)
    load.SetAttribute("bus1", networks.get_vacant_cubicle_of_terminal(bus))
    load.SetAttribute("plini", 5.0)

    diagram = act_prj.create_in_folder("Mini.IntGrfnet", diagram_folder)
    diagram.SetAttribute("pDataFolder", grid)
    grid.SetAttribute("pDiagram", diagram)
    for element in (bus, load):  # slack deliberately not drawn
        act_prj.create_in_folder(
            f"g_{element.loc_name}.IntGrf", diagram
        ).SetAttribute("pDataObj", element)

    yield networks, act_prj, grid, {"bus": bus, "slack": slack, "load": load}
    cleanup()


def test_rename_children_affixes_every_direct_child(grid_with_diagram):
    networks, act_prj, grid, elms = grid_with_diagram
    renamed = networks.rename_children(grid, prefix="A ", suffix=" B")
    assert {e.loc_name for e in grid.GetContents()} == {
        "A Bus B",
        "A Slack B",
        "A Load B",
    }
    assert set(renamed.values()) == {"A Bus B", "A Slack B", "A Load B"}
    # idempotent
    assert networks.rename_children(grid, prefix="A ", suffix=" B") == {}


def test_rename_drawn_elements_only_touches_drawn_objects(grid_with_diagram):
    networks, act_prj, grid, elms = grid_with_diagram

    renamed = networks.rename_drawn_elements(grid, suffix=" X")

    assert elms["bus"].loc_name == "Bus X"
    assert elms["load"].loc_name == "Load X"
    assert elms["slack"].loc_name == "Slack"  # not drawn -> untouched
    assert set(renamed) == {elms["bus"], elms["load"]}
    # idempotent, and accepts the diagram object directly
    assert networks.rename_drawn_elements(grid.pDiagram, suffix=" X") == {}


def test_rename_drawn_elements_needs_a_diagram(grid_with_diagram):
    networks, act_prj, grid, elms = grid_with_diagram
    grid.SetAttribute("pDiagram", None)
    with pytest.raises(PFInterfaceError, match="no single-line diagram"):
        networks.rename_drawn_elements(grid, prefix="Z ")


if __name__ == "__main__":
    pytest.main([__file__])
