"""Tests for the grid-forming-converter template interfaces + the matcher.

Exercised against the templates in the global DIgSILENT library (their internal
composite models), so a live PowerFactory with the standard library is needed.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.applications.digsilent_library import DigsilentLibrary
from powfacpy.template_models import TemplateMatcher
from powfacpy.template_models.digsilent_library.grid_forming_converters import (
    DroopControlledConverter,
    Synchronverter,
    VirtualSynchronousMachine,
    WeccRegfmA1,
    WeccRegfmB1,
)

_GFC = r"Templates\Grid-forming Converters"


@pytest.fixture(scope="module")
def lib(pf_app) -> DigsilentLibrary:
    return DigsilentLibrary(pf_app)


def _composite_model(template):
    for child in _iter(template):
        if child.GetClassName() == "ElmComp":
            return child
    raise AssertionError("no ElmComp in template")


def _iter(obj):
    for child in obj.GetContents():
        yield child
        yield from _iter(child)


@pytest.mark.parametrize(
    "template_name, cls",
    [
        ("WECC REGFM_A1 Droop Inverter - Storage", WeccRegfmA1),
        ("WECC REGFM_B1 VSM Inverter - Storage", WeccRegfmB1),
        ("Virtual Synchronous Machine - Storage", VirtualSynchronousMachine),
        ("Synchronverter", Synchronverter),
        ("Droop Controlled Converter - Storage", DroopControlledConverter),
    ],
)
def test_matcher_identifies_library_template(lib, template_name, cls):
    comp = _composite_model(lib.get_template(_GFC + "\\" + template_name))
    match = TemplateMatcher().identify(comp, level="signature")
    assert match.template_class is cls
    assert match.confidence >= 0.75
    model = match.build()
    assert isinstance(model, cls)


def test_regfm_b1_has_explicit_inertia(lib):
    comp = _composite_model(
        lib.get_template(_GFC + r"\WECC REGFM_B1 VSM Inverter - Storage")
    )
    model = WeccRegfmB1(comp)
    assert model.rated_apparent_power_MVA == pytest.approx(100.0)
    assert model.get_inertia_constant() == pytest.approx(0.5)
    assert model.get_equivalent_inertia_constant() == pytest.approx(0.5)
    assert model.get_kinetic_energy_MWs() == pytest.approx(50.0)
    assert model.get_active_power_droop() == pytest.approx(0.02)
    assert model.get_steady_state_damping() == pytest.approx(100.0)


def test_regfm_a1_is_pure_droop(lib):
    comp = _composite_model(
        lib.get_template(_GFC + r"\WECC REGFM_A1 Droop Inverter - Storage")
    )
    model = WeccRegfmA1(comp)
    assert model.get_inertia_constant() is None
    tpf = model.get_power_filter_time_constant()
    mp = model.get_active_power_droop()
    assert model.get_equivalent_inertia_constant() == pytest.approx(tpf / (2 * mp))


def test_vsm_inertia_from_acceleration_time_constant(lib):
    comp = _composite_model(
        lib.get_template(_GFC + r"\Virtual Synchronous Machine - Storage")
    )
    model = VirtualSynchronousMachine(comp)
    ta = model.get_acceleration_time_constant()
    assert model.get_inertia_constant() == pytest.approx(ta / 2)
    assert model.get_damping() == pytest.approx(model._gf_param("Dp"))


def test_synchronverter_inertia(lib):
    comp = _composite_model(lib.get_template(_GFC + r"\Synchronverter"))
    model = Synchronverter(comp)
    assert model.get_inertia_constant() == pytest.approx(
        model.get_acceleration_time_constant() / 2
    )
    assert model.get_reactive_power_droop() is not None


def test_droop_converter_equivalent_inertia(lib):
    comp = _composite_model(
        lib.get_template(_GFC + r"\Droop Controlled Converter - Storage")
    )
    model = DroopControlledConverter(comp)
    assert model.get_inertia_constant() is None
    assert model.get_equivalent_inertia_constant() == pytest.approx(
        model.get_power_filter_time_constant()
        / (2 * model.get_active_power_droop())
    )
    assert model.get_effective_time_constant() == pytest.approx(
        model.get_power_filter_time_constant()
    )


def test_matcher_no_match_for_unrelated_composite_model(
    pf_app, activate_39_bus_new_england_test_project
):
    from powfacpy.base.active_project import ActiveProject

    act_prj = ActiveProject(pf_app)
    comps = act_prj.app.GetCalcRelevantObjects("*.ElmComp")
    if not comps:
        pytest.skip("no composite models in the 39-bus project")
    for comp in comps:  # governor/AVR frames - none is a GFC template
        assert TemplateMatcher().identify(comp).template_class is None


if __name__ == "__main__":
    pytest.main([__file__])
