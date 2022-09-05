"""Helper functions in the electrical and power engineering domain.
"""
import math


def get_R_and_X_from_RX_ratio(RX_ratio,Z_abs):
  """Get the resistor and reactance from R/X-ratio
  and absolte impedance.

  Derivation:
  sqrt(R^2 + X^2) = Z_abs
  --> sqrt((X*RX_ratio)^2 + X^2) = Z_abs
  --> X = sqrt(Z_abs^2/(1 + RX_ratio^2))
  """
  X = math.sqrt(Z_abs**2/(1 + RX_ratio**2))
  R = X*RX_ratio
  return R,X