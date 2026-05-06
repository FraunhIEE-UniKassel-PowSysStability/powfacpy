Module powfacpy.engineering_helpers
===================================
Helper functions in the electrical and power engineering domain.

Functions
---------

`get_R_and_X_from_RX_ratio(RX_ratio, Z_abs)`
:   Get the resistor and reactance from R/X-ratio
    and absolte impedance.
    
    Derivation:
    sqrt(R^2 + X^2) = Z_abs
    --> sqrt((X*RX_ratio)^2 + X^2) = Z_abs
    --> X = sqrt(Z_abs^2/(1 + RX_ratio^2))

`get_resistance_and_reactance_from_uk_and_copper_losses(uk, loss_kW, Snom_MVA, Unom_kV)`
:   P = I^2*R
    I = S/U
    P = (S/U)^2*R

`get_weighted_average(values, weights, return_sum_of_weights: bool = False) ‑> list | numpy.ndarray`
: