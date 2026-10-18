import sys

import pytest

sys.path.insert(0, r".\src")
from powfacpy.pf_classes.protocols import StaCubic
from powfacpy.applications.networks import Networks


@pytest.fixture
def pfnet(pf_app) -> Networks:
    return Networks(pf_app)


def test_get_vacant_cubicle_of_terminal(
    pfnet: Networks, activate_powfacpy_test_project
) -> None:
    study_case = pfnet.act_prj.get_unique_obj(
        r"Study Cases\test_network_interface\Study Case"
    )
    study_case.Activate()
    cub: StaCubic = pfnet.get_vacant_cubicle_of_terminal(
        r"Network Model\Network Data\test_plot_interface\Grid 1\Terminal HV 2"
    )
    assert cub.GetClassName() == "StaCubic"
    assert cub.obj_id is None


# --- single-line diagram geometry --------------------------------------------


@pytest.fixture
def new_england_grid(pfnet, copy_39_bus_new_england_test_project):
    copy_39_bus_new_england_test_project.Activate()
    grid = pfnet.act_prj.get_unique_obj(
        "Grid", parent_folder=pfnet.act_prj.network_data_folder
    )
    if grid.pDiagram is None:
        pytest.skip("39-bus New England grid has no single-line diagram")
    return grid


def test_get_graphical_objects_and_positions(pfnet: Networks, new_england_grid):
    terminals = pfnet.act_prj.get_obj("*.ElmTerm", parent_folder=new_england_grid)[:5]

    graphical = pfnet.get_graphical_objects(terminals)
    assert set(graphical) == set(terminals)
    for objects in graphical.values():
        assert objects and all(o.GetClassName() == "IntGrf" for o in objects)

    positions = pfnet.get_positions(terminals)
    assert set(positions) == set(terminals)
    for x, y in positions.values():
        assert isinstance(x, float) and isinstance(y, float)
    assert len(set(positions.values())) > 1  # not all drawn on top of each other


def test_get_positions_missing_element_warns(pfnet: Networks, new_england_grid):
    fresh = pfnet.act_prj.create_in_folder("probe bus.ElmTerm", new_england_grid)
    with pytest.warns(RuntimeWarning):
        pfnet.get_positions([fresh])  # not drawn anywhere
    fresh.Delete()


def test_rename_branches_after_terminals(pfnet: Networks, new_england_grid):
    lines = pfnet.act_prj.get_obj("*.ElmLne", parent_folder=new_england_grid)[:3]
    original = {line: line.loc_name for line in lines}
    try:
        renamed = pfnet.rename_branches_after_terminals(lines, order_key=str)
        for line, name in renamed.items():
            a, b = line.bus1.cterm.loc_name, line.bus2.cterm.loc_name
            assert name == "-".join(["L", *sorted([a, b])])
            assert line.loc_name == name
    finally:
        for line, name in original.items():
            line.loc_name = name


def test_rename_branches_after_terminals_dedupes_parallel(pfnet: Networks):
    class _Term:
        def __init__(self, name):
            self.loc_name = name

    class _Cub:
        def __init__(self, name):
            self.cterm = _Term(name)

    class _Branch:
        def __init__(self, a, b):
            self._a, self._b, self.loc_name = _Cub(a), _Cub(b), "?"

        def HasAttribute(self, attr):
            return attr in ("bus1", "bus2")

        def GetAttribute(self, attr):
            return {"bus1": self._a, "bus2": self._b}[attr]

    branches = [_Branch("A", "B"), _Branch("A", "B"), _Branch("A", "C")]
    names = list(pfnet.rename_branches_after_terminals(branches).values())
    assert names == ["L-A-B", "L-A-B-1", "L-A-C"]


if __name__ == "__main__":
    pytest.main(([r"tests\applications\test_networks.py"]))
