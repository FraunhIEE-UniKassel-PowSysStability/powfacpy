"""Tests for powfacpy.applications.parameter_studies (the parstudy integration).

Pure Python - 'affects' targets are fake objects with GetAttribute/SetAttribute
(the same duck-typing parstudy itself relies on), so no PowerFactory is needed.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory

parstudy = pytest.importorskip("parstudy")

from powfacpy.applications.parameter_studies import apply_gradient, pf_parameter


class _FakeObj:
    """Duck-types PowerFactory's GetAttribute/SetAttribute."""

    def __init__(self, value: float = 0.0):
        self.value = value

    def GetAttribute(self, attr):
        return getattr(self, attr)

    def SetAttribute(self, attr, value):
        setattr(self, attr, value)


def test_pf_parameter_builds_model_parameter_with_linspace_values():
    objs = [_FakeObj(), _FakeObj()]
    param = pf_parameter("H", objs, "value", (0.6, 1.4), steps=5)

    assert param.name == "H"
    assert param.values == pytest.approx([0.6, 0.8, 1.0, 1.2, 1.4])
    assert param.affects == [(objs[0], "value"), (objs[1], "value")]
    assert param.mode == "set"


def test_pf_parameter_accepts_single_object():
    obj = _FakeObj()
    param = pf_parameter("H", obj, "value", (0.6, 1.4), steps=3)
    assert param.affects == [(obj, "value")]


def test_pf_parameter_multiply_mode_scales_relative_to_captured_baseline():
    objs = [_FakeObj(10.0), _FakeObj(20.0)]
    param = pf_parameter("H_mult", objs, "value", (0.5, 1.5), steps=3, mode="multiply")

    study = parstudy.Study([param], lambda values: {"y": values["H_mult"]})
    results = study.run()

    # baseline run: parameter at its default (mean of range = 1.0) -> no change
    assert objs[0].value == pytest.approx(10.0)
    assert objs[1].value == pytest.approx(20.0)
    assert results.evaluations[("parameters", "H_mult")].tolist() == pytest.approx(
        [1.0, 0.5, 1.0, 1.5]
    )


def test_apply_gradient_preserves_group_average_and_reverses_across_objects():
    objs = [_FakeObj(), _FakeObj(), _FakeObj()]

    apply_gradient(objs, "value", (6.0, 10.0), value=6.0)
    assert [o.value for o in objs] == pytest.approx([6.0, 8.0, 10.0])

    apply_gradient(objs, "value", (6.0, 10.0), value=10.0)
    assert [o.value for o in objs] == pytest.approx([10.0, 8.0, 6.0])

    # midpoint: every object sits at the range's mean regardless of position
    apply_gradient(objs, "value", (6.0, 10.0), value=8.0)
    assert [o.value for o in objs] == pytest.approx([8.0, 8.0, 8.0])


def test_apply_gradient_multiply_mode_combines_with_baseline():
    objs = [_FakeObj(), _FakeObj()]
    baseline = [2.0, 4.0]

    apply_gradient(objs, "value", (0.5, 1.5), value=0.5, mode="multiply", baseline=baseline)

    assert objs[0].value == pytest.approx(0.5 * 2.0)
    assert objs[1].value == pytest.approx(1.5 * 4.0)


def test_apply_gradient_rejects_invalid_mode():
    with pytest.raises(ValueError):
        apply_gradient([_FakeObj()], "value", (0.0, 1.0), value=0.5, mode="bogus")


if __name__ == "__main__":
    pytest.main([__file__])
