"""Tests for SubSystemContainer.get_tie_branches / get_tie_lines / get_tie_branches_between.

Runs against the 39-bus New England project, split into 'West' and 'East'
zones by the same line-based boundary used in the Subsystems tutorial - the
three lines crossing that boundary ('Line 04 - 14', 'Line 13 - 14',
'Line 16 - 17') are the known tie lines between the two zones, so the
expected result of get_tie_branches is known in advance.

This module gets its own copy of the 39-bus project (copy_39_bus_new_england_
test_project is module-scoped, i.e. cached per test *module*), so clearing
the zones/boundaries folders here cannot affect the 'South-East' zone that
test_subsystems.py relies on.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.applications.subsystems import SubSystemContainer
from powfacpy.applications.topology import Topology

_BUS_BRANCH = {
    r"Network Model\Network Data\Grid\Bus 14": [
        r"Network Model\Network Data\Grid\Line 04 - 14",
        r"Network Model\Network Data\Grid\Line 13 - 14",
    ],
    r"Network Model\Network Data\Grid\Bus 16": [
        r"Network Model\Network Data\Grid\Line 16 - 17"
    ],
}
_TIE_LINE_NAMES = {"Line 04 - 14", "Line 13 - 14", "Line 16 - 17"}


@pytest.fixture(scope="module")
def west_east_container(
    pf_app, act_prj, copy_39_bus_new_england_test_project
) -> SubSystemContainer:
    copy_39_bus_new_england_test_project.Activate()
    act_prj.clear_folder(act_prj.zones_folder)
    act_prj.clear_folder(act_prj.boundaries_folder)
    topo = Topology(pf_app)
    zone_west = topo.create_zone_from_boundary_bus_branch("West", _BUS_BRANCH)
    zone_east = topo.create_zone_from_boundary_bus_branch(
        "East", _BUS_BRANCH, to_branch=False
    )
    return SubSystemContainer([zone_east, zone_west], pf_app)


def test_get_tie_lines(west_east_container: SubSystemContainer):
    ties = west_east_container.get_tie_lines()
    assert set(ties["name"]) == _TIE_LINE_NAMES
    assert (ties["class"] == "ElmLne").all()
    assert all(set(s) == {"East", "West"} for s in ties["subsystems"])


def test_get_tie_branches_without_class_filter_matches_tie_lines(
    west_east_container: SubSystemContainer,
):
    # This boundary was drawn purely along lines, so no other branch class
    # (e.g. a transformer or coupler) should cross it.
    all_ties = west_east_container.get_tie_branches()
    assert set(all_ties["name"]) == _TIE_LINE_NAMES


def test_get_tie_branches_between(west_east_container: SubSystemContainer):
    elements = west_east_container.get_tie_branches_between(0, 1)
    assert {e.loc_name for e in elements} == _TIE_LINE_NAMES
    assert (
        west_east_container.get_tie_branches_between(0, 1, element_classes=["ElmTr2"])
        == []
    )


if __name__ == "__main__":
    pytest.main([__file__])
