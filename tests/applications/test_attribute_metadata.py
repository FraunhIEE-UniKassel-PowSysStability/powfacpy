"""Tests for powfacpy.applications.attribute_metadata.AttributeMetadata.

The `_parse_inline_options` / `_strip_marker` unit tests need no PowerFactory; the
rest read the GUI-string database and the live attribute descriptions.
"""

import sys

import pandas as pd
import pytest

sys.path.insert(0, r".\src")

from powfacpy.applications.attribute_metadata import (
    AttributeMetadata,
    _parse_inline_options,
    _strip_marker,
)
from powfacpy.exceptions import PFEnumValueError


# --------------------------------------------------------------------------- #
# pure-Python parsing
# --------------------------------------------------------------------------- #


@pytest.mark.unit
@pytest.mark.parametrize(
    "description, expected",
    [
        ("Control mode:Vac-phi:Vdc-phi:PWM-phi", {0: "Vac-phi", 1: "Vdc-phi", 2: "PWM-phi"}),
        ("Star Point:&0&grounded:&2&isolated", {0: "grounded", 2: "isolated"}),
        (
            "Modelica Model Type:&1&Clocked:&0&Hybrid (pilot version)",
            {1: "Clocked", 0: "Hybrid (pilot version)"},
        ),
        ("Bus type:AS:PQ|Bus t.", {0: "AS", 1: "PQ"}),
        ("Machine", {}),
        ("~Active Power|Act.Pow.", {}),
        ("Note: one short segment is not an enum", {}),
        ("Prose: a long descriptive sentence that ends with a period.", {}),
        (None, {}),
        ("", {}),
    ],
)
def test_parse_inline_options(description, expected):
    assert _parse_inline_options(description) == expected


@pytest.mark.unit
def test_strip_marker():
    assert _strip_marker("~Shunt Type|Type") == "Shunt Type"
    assert _strip_marker("  Generator  ") == "Generator"
    assert _strip_marker("~Local Controller") == "Local Controller"


# --------------------------------------------------------------------------- #
# against a live PowerFactory (class-name route - no active project needed)
# --------------------------------------------------------------------------- #


@pytest.fixture(scope="module")
def meta(pf_app) -> AttributeMetadata:
    return AttributeMetadata(pf_app)


def test_gui_string_db_is_readable(meta: AttributeMetadata):
    assert meta.localisation_db_path.is_file()
    assert meta._db  # non-empty {(class, param): message}


def test_label(meta: AttributeMetadata):
    assert meta.label("ElmSym", "i_mot") == "Machine"
    assert meta.label("ElmSym", "nonexistent_attr") is None


def test_enum_options_inline(meta: AttributeMetadata):
    # ElmVsc.i_acdc stores its options inline -> comes from the live description
    options = meta.enum_options("ElmVsc", "i_acdc")
    assert options[0] == "Vac-phi"
    assert options[1] == "Vdc-phi"
    assert len(options) >= 5


def test_enum_options_from_option_rows(meta: AttributeMetadata):
    # these have only a label from the API; the options are <attr>_<n> db rows
    assert meta.enum_options("ElmSym", "i_mot") == {
        0: "Generator",
        1: "Motor",
        2: "Condenser",
    }
    assert meta.enum_options("ElmSecctrl", "i_net") == {
        0: "Frequency Control",
        1: "Power-Frequency Control",
    }


def test_enum_options_unknown_is_empty(meta: AttributeMetadata):
    # string-coded enum -> {} (reads/writes as its string anyway)
    assert meta.enum_options("ElmGenstat", "mode_inp") == {}
    # options in neither the API nor the db
    assert meta.enum_options("ElmSecctrl", "iexchange") == {}


def test_enum_name_and_code(meta: AttributeMetadata):
    assert meta.enum_name("ElmSym", "i_mot", 2) == "Condenser"
    assert meta.enum_code("ElmSecctrl", "i_net", "Power-Frequency Control") == 1
    # case-insensitive, ~ tolerated, int / numeric string pass through
    assert meta.enum_code("ElmSym", "i_mot", "motor") == 1
    assert meta.enum_code("ElmSym", "i_mot", 2) == 2
    assert meta.enum_code("ElmSym", "i_mot", "2") == 2


def test_enum_name_unknown_options_returns_str(meta: AttributeMetadata):
    assert meta.enum_name("ElmSecctrl", "iexchange", 2) == "2"


def test_enum_code_invalid_raises(meta: AttributeMetadata):
    with pytest.raises(PFEnumValueError, match="Condenser"):
        meta.enum_code("ElmSym", "i_mot", "Nonsense")


# --------------------------------------------------------------------------- #
# against a live object (needs an active project)
# --------------------------------------------------------------------------- #


@pytest.fixture
def der_project(activate_39_bus_with_der_test_project):
    return activate_39_bus_with_der_test_project


def test_live_object_route(meta: AttributeMetadata, act_prj, der_project):
    machine = act_prj.get_calc_relevant_obj("*.ElmSym")[0]
    assert meta.enum_options(machine, "i_mot") == {
        0: "Generator",
        1: "Motor",
        2: "Condenser",
    }
    assert meta.enum_name(machine, "i_mot", machine.i_mot) in {
        "Generator",
        "Motor",
        "Condenser",
    }


def test_set_enum_and_set_attributes(meta: AttributeMetadata, act_prj, der_project):
    grid = act_prj.get_unique_obj("Grid", parent_folder=act_prj.network_data_folder)
    controller = act_prj.create_in_folder("meta_test.ElmSecctrl", grid, overwrite=True)
    try:
        meta.set_enum(controller, "i_net", "Power-Frequency Control")
        assert controller.i_net == 1

        meta.set_attributes(
            controller,
            {"imode": "According to Dispatched Active Power", "psetp": 1.5},
        )
        assert controller.imode == 2
        assert controller.psetp == pytest.approx(1.5)

        # a string value for a non-enum attribute is written unchanged
        meta.set_attributes(controller, {"loc_name": "meta_test"})
        assert controller.loc_name == "meta_test"
    finally:
        controller.Delete()


def test_active_project_set_attr_resolve_enum_names(act_prj, der_project):
    grid = act_prj.get_unique_obj("Grid", parent_folder=act_prj.network_data_folder)
    controller = act_prj.create_in_folder("meta_test.ElmSecctrl", grid, overwrite=True)
    try:
        act_prj.set_attr(
            controller,
            {"i_net": "Power-Frequency Control", "psetp": 2.0},
            resolve_enum_names=True,
        )
        assert controller.i_net == 1
        assert controller.psetp == pytest.approx(2.0)
        # default (flag off): a raw code still works
        act_prj.set_attr(controller, {"i_net": 0})
        assert controller.i_net == 0
    finally:
        controller.Delete()


def test_describe(meta: AttributeMetadata, act_prj, der_project):
    machine = act_prj.get_calc_relevant_obj("*.ElmSym")[0]
    described = meta.describe(machine, ["i_mot", "pgini"])
    assert isinstance(described, pd.DataFrame)
    assert list(described.index) == ["i_mot", "pgini"]
    assert described.loc["i_mot", "enum_name"] in {"Generator", "Motor", "Condenser"}
    assert described.loc["pgini", "enum_name"] is None


if __name__ == "__main__":
    pytest.main([__file__])
