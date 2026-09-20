"""Eigenvalue trajectories over a parameter sweep (built on `parstudy`).
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any, Literal, Self, Sequence
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

from powfacpy.exceptions import PFEigenvalueMismatchError
from powfacpy.applications.dynamic_modal_analysis._common import (
    DEFAULT_DOMINANT_QUANTILE,
    IMAG_COL,
    INDEX_COL,
    REAL_COL,
    _auto_real_xlim,
)
from powfacpy.applications.dynamic_modal_analysis.results import ModalAnalysisResults
from powfacpy.applications.dynamic_modal_analysis.tracking import track_eigenvalues

if TYPE_CHECKING:
    from parstudy import StudyResults


class EigenvalueSweepResults:
    """How the eigenvalues move as one parameter is swept - the modal-analysis
    equivalent of `parstudy.StudyResults`, built from a plain list of
    `ModalAnalysisResults` (typically the tracked `raw` results of a
    `parstudy.Study` sweep whose `evaluate()` called `ModalAnalysis.run()`;
    see `from_study_results` and the tutorial).
    """

    def __init__(
        self, param_values: Sequence[Any], results: Sequence[ModalAnalysisResults]
    ) -> None:
        if len(param_values) != len(results):
            raise PFEigenvalueMismatchError(
                f"'param_values' and 'results' must have the same length; got "
                f"{len(param_values)} and {len(results)}."
            )
        self.param_values = list(param_values)
        self.results = list(results)

    @classmethod
    def from_study_results(
        cls,
        study_results: "StudyResults",
        parameter_name: str,
        *,
        include_baseline: bool = True,
    ) -> Self:
        """Build from a `parstudy.StudyResults` whose runs' `raw` is a
        `ModalAnalysisResults` - i.e. an `evaluate(values)` that returned
        `(metrics, modal_analysis.run())`.

        Args:
            study_results: the `StudyResults` returned by `Study(...).run()`.
            parameter_name: name of the swept `parstudy.ModelParameter` whose
                value becomes this sweep's parameter axis.
            include_baseline: the default `"one_at_a_time"` strategy inserts
                one baseline run (every parameter at its default) before the
                swept values - set `False` to drop it, e.g. if the swept
                range already includes the default value and would otherwise
                plot/count it twice.
        """
        records = study_results.records
        if not include_baseline:
            records = [r for r in records if r.varied is not None]
        param_values = [r.values[parameter_name] for r in records]
        results = [study_results.raw(record.index) for record in records]
        return cls(param_values, results)

    def when(self, param_value: Any) -> ModalAnalysisResults:
        """The result run with `parameter == param_value`."""
        for value, result in zip(self.param_values, self.results):
            if value == param_value:
                return result
        raise KeyError(f"No result found for parameter value {param_value!r}.")

    def when_index(self, run: int) -> ModalAnalysisResults:
        """The result at position `run` (0-based, in sweep order)."""
        return self.results[run]

    def track_eigenvalues(self) -> Self:
        """Track eigenvalues across the sweep (each run against the previous)."""
        return EigenvalueSweepResults(self.param_values, track_eigenvalues(self.results))

    def filter_by_damping_ratio(self, max_damping_ratio: float) -> Self:
        results = [r.filter_by_damping_ratio(max_damping_ratio) for r in self.results]
        return EigenvalueSweepResults(self.param_values, results)

    def filter_by_index(self, index: int | list[int]) -> Self:
        results = [r.filter_by_index(index) for r in self.results]
        return EigenvalueSweepResults(self.param_values, results)

    def filter_out_conjugates(self) -> Self:
        results = [r.filter_out_conjugates() for r in self.results]
        return EigenvalueSweepResults(self.param_values, results)

    def filter_out_real_modes(self) -> Self:
        results = [r.filter_out_real_modes() for r in self.results]
        return EigenvalueSweepResults(self.param_values, results)

    def plot(
        self,
        *,
        colorbar_label: str = "",
        ax: plt.Axes | None = None,
        xlim: tuple[float, float] | Literal["auto"] | None = "auto",
        quantile: float = DEFAULT_DOMINANT_QUANTILE,
    ) -> plt.Axes:
        """Scatter every run's eigenvalues in the complex plane, colored by
        the parameter value - the classic "root locus" view of a parameter
        sweep.

        Args:
            colorbar_label: label for the parameter-value colorbar.
            ax: axes to draw on (a new figure is created if omitted).
            xlim: `"auto"` (default) zooms the x-axis to the dominant
                eigenvalues (see `EigenvalueSet.plot`), computed across every
                run in the sweep; pass an explicit `(lo, hi)` to override, or
                `None` for matplotlib's own full-range default.
            quantile: only used when `xlim="auto"` - see `EigenvalueSet.plot`.
        """
        if ax is None:
            _, ax = plt.subplots()
        max_len = max(len(r) for r in self.results)

        real, imag, color = [], [], []
        for value, result in zip(self.param_values, self.results):
            df = result.get_dataframe()
            real.append(self._pad(df[REAL_COL].to_numpy(), max_len))
            imag.append(self._pad(df[IMAG_COL].to_numpy(), max_len))
            color.append(np.full(max_len, value))

        sc = ax.scatter(real, imag, c=color, marker="x", cmap="jet")
        if xlim == "auto":
            xlim = _auto_real_xlim(np.concatenate(real), quantile=quantile)
        if xlim is not None:
            ax.set_xlim(xlim)
        left, right = ax.get_xlim()
        ax.axvspan(0, right, facecolor="red", alpha=0.2)
        ax.set_xlim([left, right])
        ax.set_xlabel("Real")
        ax.set_ylabel("Imaginary")
        ax.grid(True)
        cbar = ax.figure.colorbar(sc, ax=ax)
        cbar.set_label(colorbar_label)
        return ax

    def plot_eigenvalue_tracking(
        self,
        ax: plt.Axes | None = None,
        *,
        xlim: tuple[float, float] | Literal["auto"] | None = "auto",
        quantile: float = DEFAULT_DOMINANT_QUANTILE,
        max_legend_entries: int = 20,
    ) -> plt.Axes:
        """Scatter every run's eigenvalues, colored by eigenvalue *index*
        rather than by parameter value - a sanity check that
        `track_eigenvalues()` followed each mode correctly (a mode that jumps
        discontinuously between runs signals a tracking mistake).

        Args:
            ax: axes to draw on (a new figure is created if omitted).
            xlim: `"auto"` (default) zooms the x-axis to the dominant
                eigenvalues (see `EigenvalueSet.plot`); pass an explicit
                `(lo, hi)` to override, or `None` for matplotlib's own
                full-range default.
            quantile: only used when `xlim="auto"` - see `EigenvalueSet.plot`.
            max_legend_entries: at most this many eigenvalues - the most
                dominant ones, by their largest (least negative) real part
                across the sweep - get a legend entry. With every eigenvalue
                of a large system otherwise labeled, the legend becomes an
                unreadable wall of entries; set to `None` to label all of
                them regardless.
        """
        if ax is None:
            _, ax = plt.subplots()
        by_index: dict[int, tuple[list[float], list[float]]] = {}
        for result in self.results:
            for idx, row in result.get_dataframe().iterrows():
                real, imag = by_index.setdefault(idx, ([], []))
                real.append(row[REAL_COL])
                imag.append(row[IMAG_COL])

        if xlim == "auto":
            all_real = np.concatenate([real for real, _ in by_index.values()])
            xlim = _auto_real_xlim(all_real, quantile=quantile)

        labeled_indexes: set[int] = set(by_index.keys())
        if xlim is not None:
            labeled_indexes = {
                idx for idx, (real, _) in by_index.items() if max(real) >= xlim[0]
            }
        if max_legend_entries is not None and len(labeled_indexes) > max_legend_entries:
            ranked = sorted(labeled_indexes, key=lambda idx: max(by_index[idx][0]), reverse=True)
            labeled_indexes = set(ranked[:max_legend_entries])

        for idx, (real, imag) in by_index.items():
            ax.scatter(real, imag, marker="x", label=idx if idx in labeled_indexes else None)

        if xlim is not None:
            ax.set_xlim(xlim)
        left, right = ax.get_xlim()
        ax.axvspan(0, right, facecolor="red", alpha=0.2)
        ax.set_xlim([left, right])
        ax.set_xlabel("Real")
        ax.set_ylabel("Imaginary")
        ax.grid(True)
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ncol = max(1, math.ceil(len(handles) / 12))
            ax.legend(
                title=INDEX_COL,
                fontsize="small",
                ncol=ncol,
                loc="upper left",
                bbox_to_anchor=(1.02, 1.0),
            )
        ax.set_title("Eigenvalue tracking")
        return ax

    def _pad(self, values: npt.NDArray, size: int) -> npt.NDArray:
        if len(values) == size:
            return values
        return np.pad(values, (0, size - len(values)), constant_values=np.nan)

    def __len__(self) -> int:
        return len(self.results)
