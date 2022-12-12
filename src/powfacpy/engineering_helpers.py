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

def get_resistance_and_reactance_from_uk_and_copper_losses(uk,loss_kW,Snom_MVA,Unom_kV):
  """
  P = I^2*R
  I = S/U
  P = (S/U)^2*R
  """
  Znom = (Unom_kV*1e3)**2/(Snom_MVA*1e6)
  R = loss_kW*1e3*(Unom_kV*1e3/(Snom_MVA*1e6))**2
  r_pu = R/Znom
  x_pu = math.sqrt((uk/100)**2 - r_pu**2)
  return r_pu,x_pu
