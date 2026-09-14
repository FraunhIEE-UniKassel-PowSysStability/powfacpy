"""Tests for powfacpy.applications.subsystems (SubSystem + SubSystemDynamics).

Runs against the 39-bus New England project, which has one zone ('South-East')
with four synchronous machines and no converters.
"""

import sys

import numpy as np
import pytest

sys.path.insert(0, r".\src")

from powfacpy.applications.subsystems import SubSystem, SubSystemDynamics


@pytest.fixture(scope="module")
def subsystem(pf_app, copy_39_bus_new_england_test_project) -> SubSystem:
    copy_39_bus_new_england_test_project.Activate()
    zone = pf_app.GetCalcRelevantObjects("*.ElmZone")[0]
    return SubSystem(zone, pf_app)


def test_subsystem_constructs_and_exposes_helpers(subsystem: SubSystem):
    assert subsystem.name == "South-East"
    # the lazy sub-interfaces are cached
    assert subsystem.load_flow is subsystem.load_flow
    assert subsystem.dynamics is subsystem.dynamics
    assert isinstance(subsystem.dynamics, SubSystemDynamics)
    assert {sm.loc_name for sm in subsystem.get_internal_elms_of_class("ElmSym")} == {
        "G 04",
        "G 05",
        "G 06",
        "G 07",
    }


def test_inertia_details(subsystem: SubSystem):
    df = subsystem.dynamics.get_inertia_details()
    assert list(df["class"]) == ["ElmSym"] * 4
    # inertia_MWs = H * S for every row
    assert np.allclose(df["inertia_MWs"], df["H_s"] * df["S_MVA"])
    assert (df["S_MVA"] > 0).all()


def test_total_inertia_and_constant(subsystem: SubSystem):
    dyn = subsystem.dynamics
    df = dyn.get_inertia_details()
    expected = df["inertia_MWs"].sum()
    assert dyn.synchronous_machine_inertia_MWs() == pytest.approx(expected)
    assert dyn.converter_inertia_MWs() == 0.0  # no converters in this project
    assert dyn.total_inertia_MWs() == pytest.approx(expected)
    assert dyn.inertia_constant_on_base(1000.0) == pytest.approx(expected / 1000.0)


def test_power_margins(subsystem: SubSystem):
    df = subsystem.load_flow.get_power_margins()
    assert len(df) == 4
    # margins are just the arithmetic of the configured limits and the operating point
    assert np.allclose(df["upward_margin_MW"], df["P_max_MW"] - df["P_MW"])
    assert np.allclose(df["downward_margin_MW"], df["P_MW"] - df["P_min_MW"])
    assert subsystem.load_flow.upward_power_margin_MW(
        execute_load_flow=False
    ) == pytest.approx(np.nansum(df["upward_margin_MW"]))


def test_get_state_summary(subsystem: SubSystem):
    state = subsystem.dynamics.get_state(format="dict")
    for key in (
        "total_load_MW",
        "total_generation_MW",
        "total_inertia_MWs",
        "inertia_constant_on_generation_s",
        "upward_power_margin_MW",
        "downward_power_margin_MW",
    ):
        assert key in state
    assert state["total_inertia_MWs"] > 0
    df = subsystem.dynamics.get_state(format="pandas")
    assert list(df.index) == ["South-East"]


def test_create_secondary_controller(subsystem: SubSystem):
    controller = subsystem.load_flow.create_secondary_controller(
        synchronous_machines=True
    )
    try:
        assert controller.GetClassName() == "ElmSecctrl"
        assert controller.loc_name == "South-East secondary controller"
        assert controller.GetParent().GetClassName() == "ElmNet"
        assert controller.iexchange == 2  # "Exchange for" -> Zone
        assert controller.pPmeas == subsystem._obj  # regulates its own zone
        assert {m.loc_name for m in controller.psym} == {
            "G 04",
            "G 05",
            "G 06",
            "G 07",
        }
        # nothing else is configured by default
        assert controller.i_net == 0
        assert controller.psetp == 0.0

        with_attr = subsystem.load_flow.create_secondary_controller(
            name="SecCtrl explicit", attr={"psetp": 250.0, "i_net": 1}
        )
        try:
            assert with_attr.loc_name == "SecCtrl explicit"
            assert with_attr.iexchange == 2
            assert with_attr.psetp == pytest.approx(250.0)
            assert with_attr.i_net == 1
        finally:
            with_attr.Delete()
    finally:
        controller.Delete()


if __name__ == "__main__":
    pytest.main([__file__])
