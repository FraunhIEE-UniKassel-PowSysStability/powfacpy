"""Eigenvalue sensitivities to parameters: finite differences between tracked runs and analytical, eigenvector-weighted sensitivities.
"""

from __future__ import annotations

from typing import Any, Literal, Self, Sequence
import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas import DataFrame
from pandas.io.formats.style import Styler

from powfacpy.exceptions import PFEigenvalueMismatchError
from powfacpy.applications.dynamic_modal_analysis._common import _STYLE_PRECISION
from powfacpy.applications.dynamic_modal_analysis.eigenvalues import EigenvalueSet
from powfacpy.applications.dynamic_modal_analysis.results import ModalAnalysisResults


class Sensitivity:
    """Change in every (tracked) eigenvalue's metrics between two modal
    analyses - build with `sensitivity_between`, which tracks the eigenvalues
    for you."""

    def __init__(
        self,
        eig_before: EigenvalueSet,
        eig_after: EigenvalueSet,
        metrics: list[str] | None = None,
    ) -> None:
        if eig_before.get_indexes() != eig_after.get_indexes():
            raise PFEigenvalueMismatchError(
                "Eigenvalue indexes must match to compute a sensitivity - "
                "track the eigenvalues first (see 'sensitivity_between'). "
                f"Got indexes {eig_before.get_indexes()} and {eig_after.get_indexes()}."
            )
        self.eig_before = eig_before
        self.eig_after = eig_after
        self.metrics = metrics or []
        self.df = eig_after - eig_before
        if self.metrics:
            self.df = self.df[self.metrics]

    def filter_by_metrics(self, metrics: str | list[str]) -> Self:
        """Keep only the given eigenvalue metric column(s) (e.g. `"Damping ratio"`)."""
        metrics = [metrics] if isinstance(metrics, str) else list(metrics)
        return Sensitivity(self.eig_before, self.eig_after, metrics)

    def filter_by_index(self, index: int | list[int]) -> Self:
        return self._filtered(
            self.eig_before.filter_by_index(index), self.eig_after.filter_by_index(index)
        )

    def filter_by_damping_ratio(self, max_damping_ratio: float) -> Self:
        return self._filtered(
            self.eig_before.filter_by_damping_ratio(max_damping_ratio),
            self.eig_after.filter_by_damping_ratio(max_damping_ratio),
        )

    def filter_out_conjugates(self) -> Self:
        return self._filtered(
            self.eig_before.filter_out_conjugates(), self.eig_after.filter_out_conjugates()
        )

    def filter_out_real_modes(self) -> Self:
        return self._filtered(
            self.eig_before.filter_out_real_modes(), self.eig_after.filter_out_real_modes()
        )

    def _filtered(self, eig_before: EigenvalueSet, eig_after: EigenvalueSet) -> Self:
        """Restrict both sides to the eigenvalue indexes that independently
        passed the filter on *both* sides - a mode can cross from real to
        complex (or vice versa) as the swept parameter changes, so filtering
        `eig_before` and `eig_after` separately can otherwise leave them with
        different indexes."""
        common = sorted(set(eig_before.get_indexes()) & set(eig_after.get_indexes()))
        return Sensitivity(
            eig_before.filter_by_index(common), eig_after.filter_by_index(common), self.metrics
        )

    def get_dataframe(self) -> DataFrame:
        """`eigenvalue_after - eigenvalue_before` for every metric column,
        indexed by (tracked) eigenvalue index."""
        return self.df.copy()

    def show(self) -> Styler:
        """Styled version of `get_dataframe()` - return it as the last
        expression of a notebook cell, or pass it to `display()`."""
        return (
            self.df.style.format(precision=_STYLE_PRECISION)
            .format_index(precision=_STYLE_PRECISION, axis=0)
            .format_index(precision=_STYLE_PRECISION, axis=1)
        )


def sensitivity_between(
    before: ModalAnalysisResults, after: ModalAnalysisResults
) -> Sensitivity:
    """Sensitivity of every eigenvalue's metrics between two modal analyses.

    `after`'s eigenvalues are tracked against `before`'s first, so the
    subtraction lines up the same physical mode even if PowerFactory returned
    the eigenvalues in a different order.
    """
    tracked_after = after.track_eigenvalues_from(before)
    return Sensitivity(before.get_eigenvalues(), tracked_after.get_eigenvalues())


def system_matrix_sensitivity(
    before: ModalAnalysisResults, after: ModalAnalysisResults, delta: float
) -> npt.NDArray[np.complex128]:
    """Finite-difference estimate of `dA/dp`, the state matrix's sensitivity
    to a parameter `p`: `(after's state matrix - before's) / delta`, where
    `delta` is the change in `p` between the two runs.

    Feed the result into `ModalAnalysisResults.eigenvalue_sensitivity` (on
    either `before` or `after` - the eigenvectors of both are valid
    evaluation points for a small enough `delta`) for the analytical,
    eigenvector-weighted eigenvalue sensitivity - see the module docstring
    and the *Dynamic Modal Analysis* tutorial for a comparison against
    `sensitivity_between`'s finite-difference-on-eigenvalues approach.
    """
    return (after.get_system_matrix() - before.get_system_matrix()) / delta


class ParametricSensitivity:
    """Sensitivity across several conditions - e.g. the sensitivity of the
    eigenvalues to one parameter, recomputed at several values of a second
    ("condition") parameter. Build the list of `Sensitivity` objects yourself
    (one `sensitivity_between()` call per condition value - see the tutorial)
    and pass them in together with the condition values.
    """

    def __init__(
        self,
        condition_values: Sequence[Any],
        sensitivities: Sequence[Sensitivity],
        normalization: Literal["column", "all"] | None = None,
    ) -> None:
        if len(condition_values) != len(sensitivities):
            raise PFEigenvalueMismatchError(
                "'condition_values' and 'sensitivities' must have the same "
                f"length; got {len(condition_values)} and {len(sensitivities)}."
            )
        self.condition_values = list(condition_values)
        self.sensitivities = list(sensitivities)
        self.normalization = normalization
        self.df = self._create_dataframe(
            self.condition_values, self.sensitivities
        )

    def filter_by_metrics(self, metrics: str | list[str]) -> Self:
        sensitivities = [s.filter_by_metrics(metrics) for s in self.sensitivities]
        return ParametricSensitivity(
            self.condition_values, sensitivities, self.normalization
        )

    def filter_by_index(self, index: int | list[int]) -> Self:
        sensitivities = [s.filter_by_index(index) for s in self.sensitivities]
        return ParametricSensitivity(
            self.condition_values, sensitivities, self.normalization
        )

    def filter_by_damping_ratio(self, max_damping_ratio: float) -> Self:
        sensitivities = [
            s.filter_by_damping_ratio(max_damping_ratio) for s in self.sensitivities
        ]
        return ParametricSensitivity(
            self.condition_values, sensitivities, self.normalization
        )

    def filter_out_conjugates(self) -> Self:
        sensitivities = [s.filter_out_conjugates() for s in self.sensitivities]
        return ParametricSensitivity(
            self.condition_values, sensitivities, self.normalization
        )

    def filter_out_real_modes(self) -> Self:
        sensitivities = [s.filter_out_real_modes() for s in self.sensitivities]
        return ParametricSensitivity(
            self.condition_values, sensitivities, self.normalization
        )

    def normalize(self, normalization: Literal["column", "all"]) -> Self:
        """Return a copy that `show()`s normalized (0-1) instead of raw values."""
        return ParametricSensitivity(
            self.condition_values, self.sensitivities, normalization
        )

    def get_dataframe(self) -> DataFrame:
        return self.df.copy()

    def show(self) -> Styler:
        """Styled version of `get_dataframe()` (with a colour gradient if
        `normalize()` was called) - return it as the last expression of a
        notebook cell, or pass it to `display()`."""
        df = self.df
        match self.normalization:
            case "column":
                styled = df.div(df.max(axis=1), axis=0).style.background_gradient(
                    axis=1, vmin=0, vmax=1, cmap="YlGnBu"
                )
            case "all":
                styled = df.div(df.max(axis=None), axis=0).style.background_gradient(
                    axis=None, vmin=0, vmax=1, cmap="YlGnBu"
                )
            case _:
                styled = df.style
        return (
            styled.format(precision=_STYLE_PRECISION)
            .format_index(precision=_STYLE_PRECISION, axis=0)
            .format_index(precision=_STYLE_PRECISION, axis=1)
        )

    def _create_dataframe(
        self, condition_values: list[Any], sensitivities: list[Sensitivity]
    ) -> DataFrame:
        df = pd.concat(
            [s.get_dataframe() for s in sensitivities], axis=1, keys=condition_values
        )
        return self._drop_unused_levels(df)

    def _drop_unused_levels(self, df: DataFrame) -> DataFrame:
        """Drop MultiIndex levels (rows or columns) that take only one value -
        no longer informative once e.g. every sensitivity has the same
        eigenvalue indexes."""
        result = df.copy()
        result.index = self._drop_unused_levels_of(df.index)
        result.columns = self._drop_unused_levels_of(df.columns)
        return result

    def _drop_unused_levels_of(
        self, index: pd.MultiIndex | pd.Index
    ) -> pd.MultiIndex | pd.Index:
        if not isinstance(index, pd.MultiIndex):
            return index
        result = index
        for level in reversed(range(index.nlevels)):
            if result.nlevels > 1 and len(index.unique(level=level)) == 1:
                result = result.droplevel(level=level)
        return result
