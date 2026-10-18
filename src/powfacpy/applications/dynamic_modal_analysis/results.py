"""Results of one modal analysis run (`ModalAnalysisResults`).
"""

from __future__ import annotations

from typing import Literal, Self
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas import DataFrame, Series
from pandas.io.formats.style import Styler

from powfacpy.exceptions import PFAttributeNotSetError
from powfacpy.applications.dynamic_modal_analysis._common import (
    DEFAULT_DOMINANT_QUANTILE,
    DOMINANT_STATES_COL,
    IMAG_COL,
    INDEX_COL,
    MODE_COL,
    REAL_COL,
    _STYLE_PRECISION,
)
from powfacpy.applications.dynamic_modal_analysis.eigenvalues import Eigenvalue, EigenvalueSet, ParticipationFactorSet
from powfacpy.applications.dynamic_modal_analysis.tracking import EigenvalueTracker


class ModalAnalysisResults:
    """Result of one modal analysis run: eigenvalues, participation factors
    and the system (state) matrix they were computed from."""

    #: minimum participation for a state to be listed as "dominant" for a mode.
    DOMINANT_STATES_MIN_PARTICIPATION = 0.05

    def __init__(
        self,
        sys_matrix: npt.NDArray[np.complex128],
        eigenvalues: EigenvalueSet,
        participation_factors: ParticipationFactorSet,
        *,
        right_eigenvectors: DataFrame | None = None,
        left_eigenvectors: DataFrame | None = None,
    ) -> None:
        """
        Args:
            sys_matrix: the system (state) matrix.
            eigenvalues: the eigenvalues.
            participation_factors: participation of every state in every eigenvalue.
            right_eigenvectors: `(state, eigenvalue index)` matrix of the raw
                (complex, unnormalized) right eigenvectors - needed for
                `eigenvalue_sensitivity`. `None` if not computed (e.g. a
                `ModalAnalysisResults` built by hand without them).
            left_eigenvectors: the matching left eigenvectors.
        """
        self.sys_matrix = sys_matrix
        self.eigenvalues = eigenvalues
        self.participation_factors = participation_factors
        self.right_eigenvectors = right_eigenvectors
        self.left_eigenvectors = left_eigenvectors

    def filter_by_damping_ratio(self, max_damping_ratio: float) -> Self:
        """Keep only the eigenvalues with a damping ratio at or below
        `max_damping_ratio` - i.e. the poorly-damped/unstable ones."""
        eigenvalues = self.eigenvalues.filter_by_damping_ratio(max_damping_ratio)
        return self._with_eigenvalues(eigenvalues)

    def filter_by_index(self, index: int | list[int]) -> Self:
        """Keep only the eigenvalue(s) at the given index(es)."""
        eigenvalues = self.eigenvalues.filter_by_index(index)
        return self._with_eigenvalues(eigenvalues)

    def filter_by_state(self, state_names: str | list[str]) -> Self:
        """Keep only the given states' participation factors."""
        participation_factors = self.participation_factors.filter_by_states(state_names)
        return ModalAnalysisResults(
            self.sys_matrix,
            self.eigenvalues,
            participation_factors,
            right_eigenvectors=self.right_eigenvectors,
            left_eigenvectors=self.left_eigenvectors,
        )

    def filter_by_min_state_participation(self, min_participation: float) -> Self:
        """Keep only states that participate at least `min_participation`
        across all eigenvalues currently in this result."""
        participation_factors = (
            self.participation_factors.filter_by_min_state_participation(
                min_participation
            )
        )
        return ModalAnalysisResults(
            self.sys_matrix,
            self.eigenvalues,
            participation_factors,
            right_eigenvectors=self.right_eigenvectors,
            left_eigenvectors=self.left_eigenvectors,
        )

    def filter_out_conjugates(self) -> Self:
        """Keep only one eigenvalue of each complex-conjugate pair."""
        return self._with_eigenvalues(self.eigenvalues.filter_out_conjugates())

    def filter_out_real_modes(self) -> Self:
        """Keep only the complex (oscillatory) eigenvalues."""
        return self._with_eigenvalues(self.eigenvalues.filter_out_real_modes())

    def get_system_matrix(self) -> npt.NDArray[np.complex128]:
        """The system (state) matrix this result was computed from."""
        return self.sys_matrix

    def get_states(self) -> npt.NDArray[np.str_]:
        """State variable names, as `"<model>\\\\<state variable>"`."""
        return self.participation_factors.get_states()

    def get_eigenvalues(self) -> EigenvalueSet:
        return self.eigenvalues

    def get_participation_factors(self) -> ParticipationFactorSet:
        return self.participation_factors

    def get_right_eigenvectors(self) -> DataFrame | None:
        """`(state, eigenvalue index)` matrix of the raw right eigenvectors,
        or `None` if this result was built without them."""
        return None if self.right_eigenvectors is None else self.right_eigenvectors.copy()

    def get_left_eigenvectors(self) -> DataFrame | None:
        """`(state, eigenvalue index)` matrix of the raw left eigenvectors,
        or `None` if this result was built without them."""
        return None if self.left_eigenvectors is None else self.left_eigenvectors.copy()

    def eigenvalue_sensitivity(
        self, mode_index: int, delta_matrix: npt.NDArray[np.complex128]
    ) -> complex:
        """Analytical eigenvalue sensitivity `d(lambda)/d(p)` to a
        perturbation direction `delta_matrix` (= `dA/dp`) in the state
        matrix, via the classical eigenvector-weighted formula

            d(lambda_i)/dp = (psi_i^H @ dA/dp @ phi_i) / (psi_i^H @ phi_i)

        where `phi_i`/`psi_i` are the right/left eigenvectors of mode
        `mode_index` (Perez-Arriaga, Verghese & Schweppe 1982). Unlike
        `sensitivity_between` (which finite-differences the *eigenvalues*
        between two tracked runs), this is evaluated entirely at this one
        operating point - `delta_matrix` is usually itself a finite
        difference of the *state matrix* between two runs (see
        `system_matrix_sensitivity`), but does not require eigenvalue
        tracking, since no eigenvalue comparison across runs is involved.

        Args:
            mode_index: the eigenvalue (`Index`) to compute the sensitivity for.
            delta_matrix: the state-matrix perturbation direction `dA/dp`,
                same shape as `get_system_matrix()`.

        Returns:
            complex: the (generally complex) sensitivity `d(lambda)/dp`. Its
            real part is the sensitivity of the eigenvalue's damping; its
            imaginary part that of its frequency.
        """
        if self.right_eigenvectors is None or self.left_eigenvectors is None:
            raise PFAttributeNotSetError(
                "eigenvectors (this ModalAnalysisResults was built without them - "
                "only ModalAnalysis.run()'s results have them)"
            )
        phi = self.right_eigenvectors[mode_index].to_numpy()
        psi = self.left_eigenvectors[mode_index].to_numpy()
        numerator = np.vdot(psi, delta_matrix @ phi)
        denominator = np.vdot(psi, phi)
        return complex(numerator / denominator)

    def get_dataframe(self) -> DataFrame:
        """One row per eigenvalue: real/imaginary part, natural/damped
        frequency, damping ratio, a `"Mode"` display string and its
        `"Dominant states"` (participation >= `DOMINANT_STATES_MIN_PARTICIPATION`)."""
        df = self.eigenvalues.get_dataframe().copy()
        df[MODE_COL] = df.apply(self._format_mode, axis=1)
        df[DOMINANT_STATES_COL] = df.index.map(
            lambda idx: ",".join(self._dominant_states(idx))
        )
        return df

    def get_participation_dataframe(self) -> DataFrame:
        """`(state, eigenvalue index)` matrix of participation factors."""
        return self.participation_factors.get_dataframe()

    def show(self, hide_columns: list[str] | None = None) -> Styler:
        """Styled version of `get_dataframe()` - return it as the last
        expression of a notebook cell, or pass it to `display()`."""
        style = [{"selector": "th", "props": [("vertical-align", "middle")]}]
        styled = (
            self.get_dataframe()
            .style.set_table_styles(style)
            .format(precision=_STYLE_PRECISION)
            .format_index(precision=_STYLE_PRECISION)
        )
        if hide_columns:
            styled = styled.hide(hide_columns, axis="columns")
        return styled

    def show_participation(self) -> Styler:
        """Styled version of `get_participation_dataframe()`, with a colour
        gradient and the mode string as a second column header level."""
        df = self.get_participation_dataframe()
        modal_results = self.get_dataframe()
        df.columns = pd.MultiIndex.from_arrays(
            [df.columns, modal_results.loc[df.columns, MODE_COL]],
            names=[INDEX_COL, MODE_COL],
        )
        style = [
            {"selector": "th, td", "props": [("text-align", "center")]},
        ]
        return (
            df.style.set_table_styles(style)
            .format(precision=_STYLE_PRECISION)
            .format_index(precision=_STYLE_PRECISION)
            .background_gradient(axis=None, vmin=0, vmax=1, cmap="YlGnBu")
        )

    def plot(
        self,
        ax: plt.Axes | None = None,
        *,
        xlim: tuple[float, float] | Literal["auto"] | None = "auto",
        quantile: float = DEFAULT_DOMINANT_QUANTILE,
    ) -> plt.Axes:
        """Scatter the eigenvalues in the complex plane - see
        `EigenvalueSet.plot` for `xlim`/`quantile`."""
        return self.eigenvalues.plot(ax, xlim=xlim, quantile=quantile)

    def plot_participation(self, *, top_n: int | None = 15) -> plt.Figure:
        """Bar chart of the participation of every state, one panel per
        eigenvalue currently in this result - see
        `ParticipationFactorSet.plot` for `top_n`."""
        return self.participation_factors.plot(top_n=top_n)

    def track_eigenvalues_from(self, other: Self) -> Self:
        """Reorder this result's eigenvalues (and participation factors /
        eigenvectors) to match the index assigned to the corresponding mode
        in `other`."""
        index_map = EigenvalueTracker(
            other.get_eigenvalues(),
            self.get_eigenvalues(),
            other.get_participation_factors(),
            self.get_participation_factors(),
        ).calculate_index_map()
        return ModalAnalysisResults(
            self.sys_matrix,
            self.eigenvalues.map_eigenvalues(index_map),
            self.participation_factors.map_eigenvalues(index_map),
            right_eigenvectors=self._remap_eigenvectors(self.right_eigenvectors, index_map),
            left_eigenvectors=self._remap_eigenvectors(self.left_eigenvectors, index_map),
        )

    def _with_eigenvalues(self, eigenvalues: EigenvalueSet) -> Self:
        """Rebuild with a filtered `EigenvalueSet`, slicing the
        participation factors and eigenvectors to match."""
        kept = eigenvalues.get_indexes()
        return ModalAnalysisResults(
            self.sys_matrix,
            eigenvalues,
            self.participation_factors.filter_by_eigenvalue_index(kept),
            right_eigenvectors=self._select_eigenvectors(self.right_eigenvectors, kept),
            left_eigenvectors=self._select_eigenvectors(self.left_eigenvectors, kept),
        )

    @staticmethod
    def _select_eigenvectors(df: DataFrame | None, indexes: list[int]) -> DataFrame | None:
        return None if df is None else df[indexes]

    @staticmethod
    def _remap_eigenvectors(
        df: DataFrame | None, index_map: dict[int, int]
    ) -> DataFrame | None:
        return None if df is None else df.rename(columns=index_map)

    def _format_mode(self, row: Series) -> str:
        if abs(row[IMAG_COL]) < Eigenvalue.EPSILON:
            return f"{row[REAL_COL]:.4f}"
        return f"{row[REAL_COL]:.4f} ± {abs(row[IMAG_COL]):.4f}j"

    def _dominant_states(self, mode_index: int) -> list[str]:
        df = self.participation_factors.get_dataframe()
        return df.index[
            df[mode_index] >= self.DOMINANT_STATES_MIN_PARTICIPATION
        ].tolist()

    def __len__(self) -> int:
        return len(self.eigenvalues)
