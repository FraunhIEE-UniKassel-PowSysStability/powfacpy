"""Helper functions in the electrical and power engineering domain."""

import math

import numpy as np
from numpy import ndarray


def get_R_and_X_from_RX_ratio(RX_ratio, Z_abs):
    """Get the resistor and reactance from R/X-ratio
    and absolte impedance.

    Derivation:
    sqrt(R^2 + X^2) = Z_abs
    --> sqrt((X*RX_ratio)^2 + X^2) = Z_abs
    --> X = sqrt(Z_abs^2/(1 + RX_ratio^2))
    """
    X = math.sqrt(Z_abs**2 / (1 + RX_ratio**2))
    R = X * RX_ratio
    return R, X


def get_resistance_and_reactance_from_uk_and_copper_losses(
    uk, loss_kW, Snom_MVA, Unom_kV
):
    """
    P = I^2*R
    I = S/U
    P = (S/U)^2*R
    """
    Znom = (Unom_kV * 1e3) ** 2 / (Snom_MVA * 1e6)
    R = loss_kW * 1e3 * (Unom_kV * 1e3 / (Snom_MVA * 1e6)) ** 2
    r_pu = R / Znom
    x_pu = math.sqrt((uk / 100) ** 2 - r_pu**2)
    return r_pu, x_pu


def get_weighted_average(
    values, weights, return_sum_of_weights: bool = False
) -> list | ndarray:
    sum_of_weights = np.sum(weights)
    values = np.sum(np.multiply(values, weights)) / sum_of_weights
    if not return_sum_of_weights:
        return values
    else:
        return values, sum_of_weights


def unwrap_degrees(angle_deg) -> ndarray:
    """Unwrap an angle signal given in degrees (remove +-360 deg discontinuities).

    PowerFactory wraps rotor angle signals such as 'c:firel' and 'c:firot' to (-180, 180] deg. Unwrapping restores a continuous trajectory so that out-of-step / pole-slip conditions (relative rotor angle growing beyond 180 deg) can be detected and angle differences computed correctly.

    Args:
        angle_deg: Angle signal (1D array-like) in degrees.

    Returns:
        ndarray: Unwrapped angle signal in degrees.
    """
    return np.unwrap(np.asarray(angle_deg, dtype=float), period=360.0)


def is_out_of_step(relative_rotor_angle_deg, threshold_deg: float = 180.0) -> bool:
    """Check whether a relative rotor angle signal indicates loss of synchronism.

    The (wrapped) input signal is unwrapped first (see 'unwrap_degrees'); the machine is considered out of step if the magnitude of the unwrapped angle exceeds 'threshold_deg' at any point in time.

    Args:
        relative_rotor_angle_deg: Rotor angle relative to the reference machine ('c:firel'), 1D array-like in degrees.
        threshold_deg: Angle magnitude above which the machine is considered out of step. Defaults to 180.

    Returns:
        bool: True if the machine falls out of step.
    """
    unwrapped = unwrap_degrees(relative_rotor_angle_deg)
    if unwrapped.size == 0:
        return False
    return bool(np.max(np.abs(unwrapped)) > threshold_deg)
