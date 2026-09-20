"""Tests for powfacpy.pf_classes.sta.pll (wrapped object replaced by a fake)."""

from types import SimpleNamespace

import pytest

from powfacpy.pf_classes.sta.pll import PhaseLockedLoop

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory


def test_set_standard_parameters_sets_i_norm_on_wrapped_object() -> None:
    pf_pll = SimpleNamespace(i_norm=0)
    PhaseLockedLoop(pf_pll).set_standard_parameters()
    assert pf_pll.i_norm == 1


def test_attributes_are_forwarded_to_wrapped_object() -> None:
    pf_pll = SimpleNamespace(i_norm=0, loc_name="PLL")
    pll = PhaseLockedLoop(pf_pll)
    assert pll.loc_name == "PLL"
    pll.i_norm = 2  # existing attribute -> written to the wrapped object
    assert pf_pll.i_norm == 2
