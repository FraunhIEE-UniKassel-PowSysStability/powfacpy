"""Tests for the dispatchable-unit API:

- `SinglePortBase.set_power_dispatch` / `scale_power_dispatch` / rated-power
  helpers and their operational-limit auto-adaptation (on `StaticGenerator`,
  `PVSystem`, `SynchronousMachine`).
- `powfacpy.pf_classes.elm.unit_collection.UnitCollection` (totals, distribute,
  scale_to_total, rated power, shared-`TypSym` guard).
- `GroupingBase.get_internal_pv` / `get_internal_wind` / `get_internal_bess` /
  `get_internal_sg` and the `pv` / `wind` / `bess` / `sg` accessors.

Everything is built on a small synthetic grid inside the ``39_bus_with_der``
copy so the tests are deterministic and don't depend on the seed project's
dispatch.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.base.active_project import ActiveProject
from powfacpy.applications.networks import Networks
from powfacpy.applications.topology import Topology
from powfacpy.pf_classes.elm.genstat import StaticGenerator
from powfacpy.pf_classes.elm.pvsys import PVSystem
from powfacpy.pf_classes.elm.sym import SynchronousMachine
from powfacpy.pf_classes.elm.unit_collection import UnitCollection
from powfacpy.pf_classes.elm.zone import Zone
from powfacpy.exceptions import PFInterfaceError


@pytest.fixture
def grid(pf_app, activate_39_bus_with_der_test_project):
    """A synthetic grid with wind/PV/BESS static generators, PV systems and two
    synchronous machines (one on a shared type), all on one bus, plus a zone."""
    act_prj = ActiveProject(pf_app)
    act_prj.activate_study_case(r"Study Cases\QDS")
    networks = Networks(pf_app)
    net_data = act_prj.network_data_folder

    def cleanup():
        for leftover in net_data.GetContents("Dispatch Test.ElmNet"):
            leftover.Delete()
        for leftover in act_prj.zones_folder.GetContents("Dispatch Zone.ElmZone"):
            leftover.Delete()

    cleanup()

    net = act_prj.create_in_folder("Dispatch Test.ElmNet", net_data)
    net.Activate()
    bus = act_prj.create_in_folder("Bus.ElmTerm", net)
    bus.uknom = 110.0
    slack = act_prj.create_in_folder("Slack.ElmXnet", net)
    slack.bus1 = networks.get_vacant_cubicle_of_terminal(bus)
    slack.bustp = "SL"

    def add(class_name, name, **attrs):
        elm = act_prj.create_in_folder(f"{name}.{class_name}", net)
        elm.bus1 = networks.get_vacant_cubicle_of_terminal(bus)
        for key, value in attrs.items():
            elm.SetAttribute(key, value)
        return elm

    units = {
        "wind_1": add("ElmGenstat", "Wind 1", aCategory="wgen", sgn=100.0, pgini=40.0),
        "wind_2": add("ElmGenstat", "Wind 2", aCategory="wgen", sgn=300.0, pgini=120.0),
        "pv_gen": add("ElmGenstat", "PV Gen", aCategory="pv", sgn=50.0, pgini=20.0),
        "bess": add(
            "ElmGenstat", "BESS 1", aCategory="stor", aSubCategory="Battery",
            sgn=80.0, pgini=0.0,
        ),
        "pv_1": add("ElmPvsys", "PV 1", sgn=60.0, pgini=25.0),
        "pv_2": add("ElmPvsys", "PV 2", sgn=140.0, pgini=60.0),
    }

    shared_type = act_prj.create_in_folder("Shared.TypSym", net)
    shared_type.sgn = 200.0
    units["sg_1"] = add("ElmSym", "SG 1", typ_id=shared_type, pgini=100.0)
    units["sg_2"] = add("ElmSym", "SG 2", typ_id=shared_type, pgini=100.0)
    own_type = act_prj.create_in_folder("Own.TypSym", net)
    own_type.sgn = 150.0
    units["sg_3"] = add("ElmSym", "SG 3", typ_id=own_type, pgini=80.0)

    zone = Topology().create_zone("Dispatch Zone", [bus])
    act_prj.activate_study_case(r"Study Cases\QDS")  # refresh calc-relevant set

    yield act_prj, Zone(zone), units
    cleanup()


# --------------------------------------------------------------------------
# element level


def test_set_power_dispatch_pq_and_pf(grid):
    _, _, units = grid
    gen = StaticGenerator(units["wind_1"])

    gen.set_power_dispatch(70.0, 15.0)
    assert units["wind_1"].pgini == pytest.approx(70.0)
    assert units["wind_1"].qgini == pytest.approx(15.0)
    assert units["wind_1"].mode_inp == "PQ"

    gen.set_power_dispatch(60.0, power_factor=0.95, capacitive=True)
    assert units["wind_1"].pgini == pytest.approx(60.0)
    assert units["wind_1"].cosgini == pytest.approx(0.95)
    assert units["wind_1"].pf_recap == 1
    assert units["wind_1"].mode_inp == "PC"

    with pytest.raises(PFInterfaceError):
        gen.set_power_dispatch(10.0, 1.0, power_factor=0.9)


def test_set_power_dispatch_adapts_limits(grid):
    _, _, units = grid
    elm = units["wind_2"]
    elm.Pmax_uc, elm.Pmin_uc = 250.0, 0.0
    elm.cQ_max, elm.cQ_min = 100.0, -100.0
    gen = StaticGenerator(elm)

    gen.set_power_dispatch(400.0, 150.0)
    assert elm.Pmax_uc == pytest.approx(400.0)  # widened
    assert elm.cQ_max == pytest.approx(150.0)

    gen.set_power_dispatch(-30.0, -120.0)
    assert elm.Pmin_uc == pytest.approx(-30.0)
    assert elm.cQ_min == pytest.approx(-120.0)
    assert elm.Pmax_uc == pytest.approx(400.0)  # never narrowed

    before = (elm.Pmin_uc, elm.Pmax_uc)
    gen.set_power_dispatch(100.0, 0.0, adapt_limits=False)
    assert (elm.Pmin_uc, elm.Pmax_uc) == before


def test_scale_power_dispatch_keeps_power_factor(grid):
    _, _, units = grid
    elm = units["pv_1"]
    pv = PVSystem(elm)
    pv.set_power_dispatch(40.0, 30.0)
    pv.scale_power_dispatch(1.5)
    assert elm.pgini == pytest.approx(60.0)
    assert elm.qgini == pytest.approx(45.0)


def test_rated_apparent_power_and_scaling(grid):
    _, _, units = grid
    elm = units["pv_2"]
    elm.ngnum = 2
    pv = PVSystem(elm)
    assert pv.rated_apparent_power == pytest.approx(140.0 * 2)

    pv.set_rated_apparent_power(400.0)
    assert elm.sgn == pytest.approx(200.0)

    elm.pgini = 100.0
    pv.scale_rated_apparent_power(2.0, scale_setpoints=True)
    assert elm.sgn == pytest.approx(400.0)
    assert elm.pgini == pytest.approx(200.0)


def test_set_rated_power_scale_limits(grid):
    _, _, units = grid
    elm = units["wind_1"]
    elm.Pmax_uc, elm.Pmin_uc = 90.0, 10.0
    gen = StaticGenerator(elm)  # sgn = 100

    gen.set_rated_apparent_power(250.0, scale_limits=True)  # x2.5
    assert elm.sgn == pytest.approx(250.0)
    assert elm.Pmax_uc == pytest.approx(225.0)
    assert elm.Pmin_uc == pytest.approx(25.0)

    gen.scale_rated_apparent_power(0.4, scale_limits=True)  # back to sgn 100
    assert elm.sgn == pytest.approx(100.0)
    assert elm.Pmax_uc == pytest.approx(90.0)


def test_make_type_private(grid):
    _, _, units = grid
    sg_1 = SynchronousMachine(units["sg_1"])  # shares its type with SG 2
    sg_2_type_before = units["sg_2"].typ_id

    private_type = sg_1.make_type_private()
    assert units["sg_1"].typ_id == private_type
    assert units["sg_1"].typ_id != units["sg_2"].typ_id
    assert units["sg_2"].typ_id == sg_2_type_before  # untouched
    assert sg_1.get_machines_sharing_type() == []

    # now per-machine rating / inertia work without copy_shared_type
    sg_1.set_rated_apparent_power(400.0)
    sg_1.set_inertia(7.0)
    assert units["sg_1"].typ_id.sgn == pytest.approx(400.0)
    assert units["sg_1"].typ_id.h == pytest.approx(7.0)
    assert units["sg_2"].typ_id.sgn == pytest.approx(200.0)

    # already private -> returns the same type, no error
    assert sg_1.make_type_private() == private_type


def test_synchronous_machine_shared_type_guard(grid):
    _, _, units = grid
    machine = SynchronousMachine(units["sg_1"])
    assert {m.loc_name for m in machine.get_machines_sharing_type()} == {"SG 2"}

    with pytest.raises(PFInterfaceError, match="shared"):
        machine.set_rated_apparent_power(300.0)

    machine.set_rated_apparent_power(300.0, copy_shared_type=True)
    assert units["sg_1"].typ_id != units["sg_2"].typ_id
    assert units["sg_1"].typ_id.sgn == pytest.approx(300.0)
    assert units["sg_2"].typ_id.sgn == pytest.approx(200.0)  # untouched

    machine_3 = SynchronousMachine(units["sg_3"])  # private type
    machine_3.set_rated_apparent_power(250.0)
    assert units["sg_3"].typ_id.sgn == pytest.approx(250.0)


def test_set_inertia_uses_the_shared_type_guard(grid):
    _, _, units = grid

    machine_3 = SynchronousMachine(units["sg_3"])  # private type
    machine_3.set_inertia(6.0)
    assert units["sg_3"].typ_id.h == pytest.approx(6.0)
    machine_3.scale_inertia(0.5)
    assert units["sg_3"].typ_id.h == pytest.approx(3.0)

    shared = SynchronousMachine(units["sg_1"])  # shares its type with SG 2
    h_of_sg_2 = units["sg_2"].typ_id.h
    with pytest.raises(PFInterfaceError, match="shared"):
        shared.set_inertia(5.0)
    shared.set_inertia(5.0, copy_shared_type=True)
    assert units["sg_1"].typ_id.h == pytest.approx(5.0)
    assert units["sg_2"].typ_id.h == pytest.approx(h_of_sg_2)  # untouched
    assert units["sg_1"].typ_id != units["sg_2"].typ_id


def test_shared_type_check_ignores_variation_shadows(grid):
    """Regression: editing a machine inside a variation makes `TypSym.GetReferences()`
    also return a variation-stage shadow of that same machine - which must not be
    mistaken for another machine sharing the type."""
    act_prj, _, units = grid
    variation = act_prj.create_variation("Dispatch scenario")
    try:
        machine = SynchronousMachine(units["sg_3"])  # private type
        machine.set_power_dispatch(120.0)  # creates a variation-stage record
        assert machine.get_machines_sharing_type() == []
        machine.set_rated_apparent_power(180.0)  # must not raise
        assert units["sg_3"].typ_id.sgn == pytest.approx(180.0)
    finally:
        variation.Deactivate()
        variation.Delete()


# --------------------------------------------------------------------------
# UnitCollection


def test_unit_collection_totals_and_distribute(grid):
    _, _, units = grid
    group = UnitCollection([units["wind_1"], units["wind_2"]])
    units["wind_1"].pgini, units["wind_2"].pgini = 40.0, 120.0
    assert group.total_active_power == pytest.approx(160.0)
    assert group.total_rated_power == pytest.approx(400.0)

    group.set_power_dispatch(200.0, distribute=True)
    assert group.total_active_power == pytest.approx(200.0)
    assert units["wind_1"].pgini == pytest.approx(100.0)

    group.set_power_dispatch(55.0)  # same value on every unit
    assert units["wind_1"].pgini == pytest.approx(55.0)
    assert units["wind_2"].pgini == pytest.approx(55.0)


def test_unit_collection_distribute_accounts_for_parallel_units(grid):
    _, _, units = grid
    units["wind_2"].ngnum = 3
    group = UnitCollection([units["wind_1"], units["wind_2"]])
    group.set_power_dispatch(240.0, distribute=True)
    assert units["wind_1"].pgini == pytest.approx(120.0)
    assert units["wind_2"].pgini == pytest.approx(40.0)  # 120 / 3 parallel units
    assert group.total_active_power == pytest.approx(240.0)


def test_unit_collection_scale_to_total(grid):
    _, _, units = grid
    group = UnitCollection([units["wind_1"], units["wind_2"], units["pv_gen"]])
    units["wind_1"].pgini, units["wind_2"].pgini, units["pv_gen"].pgini = 40.0, 120.0, 40.0

    group.scale_to_total(400.0, base="current")
    assert group.total_active_power == pytest.approx(400.0)
    assert units["wind_2"].pgini == pytest.approx(240.0)  # kept its 60 % share

    group.scale_to_total(450.0, 45.0, base="rated")
    assert group.total_active_power == pytest.approx(450.0)
    assert group.total_reactive_power == pytest.approx(45.0)
    assert units["wind_2"].pgini == pytest.approx(450.0 * 300.0 / 450.0)

    for elm in (units["wind_1"], units["wind_2"], units["pv_gen"]):
        elm.pgini = 0.0
    with pytest.raises(PFInterfaceError):
        group.scale_to_total(100.0, base="current")


def test_unit_collection_rated_power_preflight_is_atomic(grid):
    _, _, units = grid
    group = UnitCollection([units["sg_3"], units["sg_1"]])  # sg_1 has a shared type
    sgn_before = units["sg_3"].typ_id.sgn

    with pytest.raises(PFInterfaceError, match="shared"):
        group.set_rated_power(500.0)
    assert units["sg_3"].typ_id.sgn == pytest.approx(sgn_before)  # not partially applied

    group.set_rated_power(500.0, distribute=True, copy_shared_type=True)
    assert units["sg_3"].typ_id.sgn == pytest.approx(250.0)
    assert units["sg_1"].typ_id.sgn == pytest.approx(250.0)


def test_unit_collection_make_types_private_then_set_rated_power(grid):
    _, _, units = grid
    group = UnitCollection([units["sg_1"], units["sg_2"], units["sg_3"]])

    group.make_types_private()
    assert len({m.typ_id.GetFullName() for m in group}) == 3  # all distinct now

    # no copy_shared_type needed any more, and each machine can differ
    group.set_rated_power(300.0, distribute=True)
    for machine in group:
        assert machine.typ_id.sgn == pytest.approx(100.0)
    units["sg_1"].typ_id.sgn = 500.0
    assert units["sg_2"].typ_id.sgn == pytest.approx(100.0)  # independent


def test_unit_collection_operational_limits_and_scale_limits(grid):
    _, _, units = grid
    group = UnitCollection([units["wind_1"], units["wind_2"]])  # sgn 100, 300

    group.set_active_power_operational_limits(-10.0, 1e5)
    for elm in (units["wind_1"], units["wind_2"]):
        assert elm.Pmin_uc == pytest.approx(-10.0)
        assert elm.Pmax_uc == pytest.approx(1e5)

    group.set_active_power_operational_limits(0.0, 100.0)
    group.scale_rated_power(2.0, scale_limits=True)
    assert {round(e.sgn) for e in (units["wind_1"], units["wind_2"])} == {200, 600}
    for elm in (units["wind_1"], units["wind_2"]):
        assert elm.Pmax_uc == pytest.approx(200.0)


# --------------------------------------------------------------------------
# GroupingBase category getters


def test_grouping_category_getters(grid):
    _, zone, units = grid

    assert {e.loc_name for e in zone.get_internal_wind()} == {"Wind 1", "Wind 2"}
    assert {e.loc_name for e in zone.get_internal_pv()} == {"PV Gen", "PV 1", "PV 2"}
    assert {e.loc_name for e in zone.get_internal_bess()} == {"BESS 1"}
    assert {e.loc_name for e in zone.get_internal_sg()} == {"SG 1", "SG 2", "SG 3"}


def test_grouping_accessors_return_unit_collections(grid):
    _, zone, units = grid
    units["pv_1"].pgini, units["pv_2"].pgini = 25.0, 60.0
    units["pv_gen"].pgini = 20.0

    assert isinstance(zone.pv, UnitCollection)
    assert zone.pv.total_active_power == pytest.approx(105.0)

    zone.wind.set_power_dispatch(300.0, distribute=True)
    assert {e.pgini for e in zone.get_internal_wind()} == {150.0}

    assert zone.pv.total_rated_power == pytest.approx(50.0 + 60.0 + 140.0)


if __name__ == "__main__":
    pytest.main([__file__])
