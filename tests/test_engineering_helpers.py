"""Tests for powfacpy.engineering_helpers.

Pure Python/numpy - no PowerFactory dependency, no fixtures needed.
"""

import math
import sys

import numpy as np
import pytest

sys.path.insert(0, r".\src")

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory

from powfacpy.engineering_helpers import (
    get_R_and_X_from_RX_ratio,
    get_resistance_and_reactance_from_uk_and_copper_losses,
    get_weighted_average,
    unwrap_degrees,
    is_out_of_step,
)


def test_get_R_and_X_from_RX_ratio():
    R, X = get_R_and_X_from_RX_ratio(RX_ratio=3.0, Z_abs=10.0)
    assert R / X == pytest.approx(3.0)
    assert math.sqrt(R**2 + X**2) == pytest.approx(10.0)


def test_get_R_and_X_from_RX_ratio_zero_ratio_is_purely_reactive():
    R, X = get_R_and_X_from_RX_ratio(RX_ratio=0.0, Z_abs=5.0)
    assert R == pytest.approx(0.0)
    assert X == pytest.approx(5.0)


def test_get_resistance_and_reactance_from_uk_and_copper_losses():
    # a typical distribution transformer: 400 kVA, 20/0.4 kV, uk=6%, losses=4.6 kW
    r_pu, x_pu = get_resistance_and_reactance_from_uk_and_copper_losses(
        uk=6.0, loss_kW=4.6, Snom_MVA=0.4, Unom_kV=0.4
    )
    # the short-circuit impedance triangle must close: r^2 + x^2 = (uk/100)^2
    assert r_pu**2 + x_pu**2 == pytest.approx((6.0 / 100) ** 2)
    assert r_pu > 0
    assert x_pu > 0


def test_get_weighted_average():
    avg = get_weighted_average([1.0, 2.0, 3.0], [1.0, 1.0, 1.0])
    assert avg == pytest.approx(2.0)

    avg = get_weighted_average([10.0, 20.0], [1.0, 3.0])
    assert avg == pytest.approx((10 * 1 + 20 * 3) / 4)


def test_get_weighted_average_returns_sum_of_weights():
    avg, sum_of_weights = get_weighted_average(
        [1.0, 2.0], [2.0, 2.0], return_sum_of_weights=True
    )
    assert avg == pytest.approx(1.5)
    assert sum_of_weights == pytest.approx(4.0)


def test_unwrap_degrees_removes_360_deg_jump():
    # a rotor angle crossing the +-180 deg wrap boundary
    wrapped = [170.0, 179.0, -179.0, -170.0]
    unwrapped = unwrap_degrees(wrapped)
    assert unwrapped[0] == pytest.approx(170.0)
    # continuous trajectory: no jump greater than a few degrees between samples
    assert np.max(np.abs(np.diff(unwrapped))) < 20.0
    assert unwrapped[-1] == pytest.approx(190.0)


def test_unwrap_degrees_leaves_continuous_signal_unchanged():
    signal = [0.0, 10.0, 20.0, 30.0]
    assert unwrap_degrees(signal) == pytest.approx(signal)


def test_is_out_of_step_false_within_threshold():
    # two machines drifting but staying within +-180 deg
    relative_angle = [0.0, 30.0, 60.0, 90.0, 60.0, 30.0]
    assert is_out_of_step(relative_angle) is False


def test_is_out_of_step_true_beyond_threshold():
    # angle winds through the wrap boundary and keeps growing -> loss of synchronism
    relative_angle = [170.0, 179.0, -179.0, -170.0, -100.0, -20.0, 60.0]
    assert is_out_of_step(relative_angle) is True


def test_is_out_of_step_respects_custom_threshold():
    relative_angle = [0.0, 90.0, 150.0]
    assert is_out_of_step(relative_angle, threshold_deg=180.0) is False
    assert is_out_of_step(relative_angle, threshold_deg=100.0) is True


def test_is_out_of_step_empty_signal_is_false():
    assert is_out_of_step([]) is False


if __name__ == "__main__":
    pytest.main([__file__])
