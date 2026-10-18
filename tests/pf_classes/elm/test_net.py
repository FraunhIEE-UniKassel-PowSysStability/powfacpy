"""Tests for powfacpy.pf_classes.elm.net (wrapped object replaced by a fake)."""

from types import SimpleNamespace

import pytest

from powfacpy.pf_classes.elm.net import Network

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory


def test_show_grafic_shows_the_diagram_of_the_wrapped_grid() -> None:
    shown = []
    diagram = SimpleNamespace(Show=lambda: shown.append(True))
    Network(SimpleNamespace(pDiagram=diagram)).show_grafic()
    assert shown == [True]


def test_attributes_are_forwarded_to_wrapped_grid() -> None:
    assert Network(SimpleNamespace(loc_name="Grid")).loc_name == "Grid"
