"""Tests for `powfacpy.pf_classes.elm.tr2.TransformerTwoWinding` and the
step-up-transformer helpers on `SinglePortBase` / `UnitCollection`.

Builds a small synthetic grid (HV bus + two LV buses, each with a static
generator behind a two-winding transformer, the two transformers sharing one
`TypTr2`) inside the ``39_bus_with_der`` copy.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.base.active_project import ActiveProject
from powfacpy.applications.networks import Networks
from powfacpy.pf_classes.elm.genstat import StaticGenerator
from powfacpy.pf_classes.elm.tr2 import TransformerTwoWinding
from powfacpy.pf_classes.elm.unit_collection import UnitCollection
from powfacpy.exceptions import PFInterfaceError


@pytest.fixture
def grid(pf_app, activate_39_bus_with_der_test_project):
    act_prj = ActiveProject(pf_app)
    act_prj.activate_study_case(r"Study Cases\QDS")
    networks = Networks(pf_app)
    net_data = act_prj.network_data_folder

    def cleanup():
        for leftover in net_data.GetContents("Tr2 Test.ElmNet"):
            leftover.Delete()

    cleanup()
    net = act_prj.create_in_folder("Tr2 Test.ElmNet", net_data)
    net.Activate()

    hv_bus = act_prj.create_in_folder("HV.ElmTerm", net)
    hv_bus.uknom = 110.0
    slack = act_prj.create_in_folder("Slack.ElmXnet", net)
    slack.bus1 = networks.get_vacant_cubicle_of_terminal(hv_bus)
    slack.bustp = "SL"

    tr_type = act_prj.create_in_folder("Unit Trf.TypTr2", net)
    tr_type.strn = 100.0
    tr_type.utrn_h = 110.0
    tr_type.utrn_l = 20.0
    tr_type.uktr = 12.0
    tr_type.pcutr = 300.0
    tr_type.ntpmn, tr_type.ntpmx, tr_type.nntap0 = -8, 8, 0
    tr_type.dutap = 1.5
    tr_type.tap_side = 0

    generators = {}
    transformers = {}
    for name in ("A", "B"):
        lv_bus = act_prj.create_in_folder(f"LV {name}.ElmTerm", net)
        lv_bus.uknom = 20.0
        transformer = act_prj.create_in_folder(f"Trf {name}.ElmTr2", net)
        transformer.typ_id = tr_type
        transformer.bushv = networks.get_vacant_cubicle_of_terminal(hv_bus)
        transformer.buslv = networks.get_vacant_cubicle_of_terminal(lv_bus)
        gen = act_prj.create_in_folder(f"Gen {name}.ElmGenstat", net)
        gen.bus1 = networks.get_vacant_cubicle_of_terminal(lv_bus)
        gen.SetAttribute("aCategory", "wgen")
        gen.sgn = 80.0
        gen.pgini = 40.0
        generators[name] = gen
        transformers[name] = transformer

    act_prj.activate_study_case(r"Study Cases\QDS")
    yield act_prj, generators, transformers, tr_type
    cleanup()


def test_get_step_up_transformer(grid):
    _, generators, transformers, _ = grid
    assert StaticGenerator(generators["A"]).get_step_up_transformer() == transformers["A"]


def test_rated_apparent_power_and_sharing(grid):
    _, _, transformers, _ = grid
    trf = TransformerTwoWinding(transformers["A"])
    assert trf.rated_apparent_power == pytest.approx(100.0)
    assert {t.loc_name for t in trf.get_transformers_sharing_type()} == {"Trf B"}


def test_set_rated_apparent_power_shared_type_guard(grid):
    _, _, transformers, tr_type = grid
    trf = TransformerTwoWinding(transformers["A"])
    uktr_before = tr_type.uktr
    pcutr_before = tr_type.pcutr

    with pytest.raises(PFInterfaceError, match="shared"):
        trf.set_rated_apparent_power(250.0)

    trf.set_rated_apparent_power(250.0, copy_shared_type=True)
    assert transformers["A"].typ_id != transformers["B"].typ_id
    assert transformers["A"].typ_id.strn == pytest.approx(250.0)
    assert transformers["A"].typ_id.uktr == pytest.approx(uktr_before)  # kept
    assert transformers["A"].typ_id.pcutr == pytest.approx(pcutr_before * 2.5)  # scaled
    assert transformers["B"].typ_id.strn == pytest.approx(100.0)  # untouched
    assert transformers["B"].typ_id.pcutr == pytest.approx(pcutr_before)  # untouched


def test_tap_and_ratio_helpers(grid):
    _, _, transformers, _ = grid
    trf = TransformerTwoWinding(transformers["A"])
    assert trf.tap_range == (-8, 8)
    assert trf.neutral_tap_position == 0
    assert trf.tap_side == "HV"
    assert trf.nominal_voltage_ratio == pytest.approx(110.0 / 20.0)

    trf.set_tap_position(4)
    assert trf.tap_position == 4
    assert trf.voltage_ratio == pytest.approx(110.0 * (1 + 4 * 1.5 / 100) / 20.0)

    trf.set_tap_position(99)  # clamped
    assert trf.tap_position == 8
    trf.reset_tap()
    assert trf.tap_position == 0


def test_rescale_step_up_transformer(grid):
    _, generators, transformers, _ = grid
    gen = StaticGenerator(generators["A"])
    gen.sgn = 150.0  # 150 MVA unit, 100 MVA transformer

    wrapped = gen.rescale_step_up_transformer(margin=0.2)
    assert isinstance(wrapped, TransformerTwoWinding)
    assert transformers["A"].typ_id.strn == pytest.approx(150.0 * 1.2)
    assert transformers["A"].typ_id != transformers["B"].typ_id  # private copy


def test_set_rated_power_scales_transformer_via_flag(grid):
    act_prj, generators, transformers, _ = grid
    collection = UnitCollection([generators["A"], generators["B"]])

    collection.make_step_up_transformer_types_private()
    assert transformers["A"].typ_id != transformers["B"].typ_id

    collection.set_rated_power(
        200.0, distribute=True, scale_step_up_transformer=True
    )
    for name in ("A", "B"):
        assert generators[name].sgn == pytest.approx(100.0)
        assert transformers[name].typ_id.strn == pytest.approx(100.0)


if __name__ == "__main__":
    pytest.main([__file__])
