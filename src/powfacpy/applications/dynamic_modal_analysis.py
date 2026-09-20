"""Dynamic modal (small-signal) analysis.

Wraps PowerFactory's modal analysis command (`ComMod`) to compute, for
whatever state is currently active (activate the study case/scenario/
operating point yourself first, as with `DynamicSimulation` or `StaticCalc`):

- the system's eigenvalues, their damping ratio, natural and damped
  frequency, and dominant states (`ModalAnalysis`, `ModalAnalysisResults`);
- participation factors of each state in each eigenvalue
  (`ParticipationFactorSet`);
- how the eigenvalues move as a parameter changes and the sensitivity of an
  eigenvalue's metrics to that change (`track_eigenvalues`,
  `EigenvalueSweepResults`, `Sensitivity`, `sensitivity_between`,
  `ParametricSensitivity`) - built on top of `parstudy.Study` (see the
  *Parameter Studies* tutorial) rather than a bespoke sweep loop: `evaluate()`
  calls `ModalAnalysis.run()` once per point, `parstudy` handles the sweep
  strategy and snapshot/restore, and the helpers here turn the resulting
  sequence of `ModalAnalysisResults` into a consistently-indexed eigenvalue
  trajectory (PowerFactory does not guarantee eigenvalues come back in the
  same order run to run);
- two ways to get an eigenvalue's sensitivity to a parameter: `sensitivity_between`
  finite-differences the *eigenvalues* between two (tracked) runs; the
  analytical, eigenvector-weighted `ModalAnalysisResults.eigenvalue_sensitivity`
  needs only `dA/dp` (usually itself a finite difference of the *state
  matrix* - `system_matrix_sensitivity`) evaluated at a single run, so it
  needs no eigenvalue tracking at all. See the tutorial for a comparison of
  both on the same system.

See the *Dynamic Modal Analysis* tutorial, which also shows the connection to
`powfacpy.applications.dynamic_simulation`: a poorly-damped or unstable mode
found here should be visible as a sustained or growing oscillation in a
time-domain simulation of the same parameter point.

Needs the optional 'scipy' dependency: `pip install powfacpy[dynamic_modal_analysis]`.
Eigenvalue *sweeps* additionally need 'parstudy': `pip install powfacpy[parstudy]`.
"""

from __future__ import annotations

import math
from os import getcwd, makedirs
from os.path import join
from shutil import rmtree
from typing import TYPE_CHECKING, Any, Literal, Self, Sequence

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas import DataFrame, Series
from pandas.io.formats.style import Styler

try:
    from scipy.linalg import eig
except ImportError as exc:
    raise ImportError(
        "powfacpy.applications.dynamic_modal_analysis needs the 'scipy' package - "
        "install with `pip install powfacpy[dynamic_modal_analysis]`"
    ) from exc

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.exceptions import (
    PFAttributeNotSetError,
    PFEigenvalueMismatchError,
    PFEigenvalueTrackingError,
)
from powfacpy.pf_classes.protocols import ComMod, PFApp

if TYPE_CHECKING:
    from parstudy import StudyResults

# Column names shared by the eigenvalue / participation-factor / modal-results
# DataFrames.
INDEX_COL = "Index"
REAL_COL = "Real (1/s)"
IMAG_COL = "Imag (rad/s)"
NATURAL_FREQ_COL = "Undamped natural frequency (Hz)"
DAMPED_FREQ_COL = "Damped frequency (Hz)"
DAMPING_RATIO_COL = "Damping ratio"
MODE_COL = "Mode"
DOMINANT_STATES_COL = "Dominant states"

_STYLE_PRECISION = 4
#: default quantile (of the real part) used by the eigenvalue-plotting
#: methods' `xlim="auto"` to zoom in on the dominant (slowest-decaying, least
#: negative) eigenvalues instead of letting a handful of very fast/heavily
#: damped ones stretch the x-axis.
DEFAULT_DOMINANT_QUANTILE = 0.75


def _auto_real_xlim(
    real_parts: npt.NDArray, quantile: float = DEFAULT_DOMINANT_QUANTILE
) -> tuple[float, float]:
    """A `(lo, hi)` x-axis range framing the dominant eigenvalues - those
    with the largest (least negative) real part, which decay slowest and
    therefore dominate the long-term time response - instead of the full
    range, which a handful of very fast/heavily-damped eigenvalues can
    otherwise stretch until the dominant ones are an unreadable cluster near
    the origin.

    `lo` is the `quantile`-th percentile of the real parts (raise `quantile`
    to zoom in further, lower it to include more of the faster eigenvalues);
    `hi` is just past the largest real part (at least 0, so the
    stable/unstable boundary is always visible).
    """
    real_parts = np.asarray(real_parts, dtype=float)
    hi = max(float(np.max(real_parts)), 0.0)
    lo = min(float(np.quantile(real_parts, quantile)), hi - 1.0)
    lo = max(lo, float(np.min(real_parts)))
    span = hi - lo
    margin = 0.15 * span if span > 0 else 1.0
    return lo - margin, hi + margin


# --------------------------------------------------------------------------- #
# eigenvalues
# --------------------------------------------------------------------------- #


class Eigenvalue:
    """A single eigenvalue of the system state matrix, with the natural
    frequency, damped frequency and damping ratio derived from it. Immutable.
    """

    EPSILON = 1e-9
    "Imaginary part below which an eigenvalue is treated as purely real."

    def __init__(self, value: complex | float, index: int) -> None:
        """
        Args:
            value: the eigenvalue's real and/or imaginary part.
            index: the eigenvalue's index (1-based, matching PowerFactory's
                own numbering of the state matrix).
        """
        self.index = index
        self.value = complex(value)
        self.nat_freq = self._natural_frequency(self.value)
        self.damp_freq = self._damped_frequency(self.value)
        self.damp_ratio = self._damping_ratio(self.value)

    def get_index(self) -> int:
        return self.index

    def get_value(self) -> complex:
        return self.value

    def get_imag(self) -> float:
        return self.value.imag

    def get_nat_freq(self) -> float:
        return self.nat_freq

    def get_damp_ratio(self) -> float:
        return self.damp_ratio

    def get_series(self) -> Series:
        """A `Series` with this eigenvalue and the quantities derived from it."""
        return pd.Series(
            {
                INDEX_COL: self.index,
                REAL_COL: self.value.real,
                IMAG_COL: self.value.imag,
                NATURAL_FREQ_COL: self.nat_freq,
                DAMPED_FREQ_COL: self.damp_freq,
                DAMPING_RATIO_COL: self.damp_ratio,
            }
        )

    def set_index(self, index: int) -> Self:
        """A copy of this eigenvalue with a different index (does not mutate `self`)."""
        return Eigenvalue(self.value, index)

    def _damping_ratio(self, eig: complex) -> float:
        if abs(eig.real) < self.EPSILON and abs(eig.imag) < self.EPSILON:
            return 1.0
        return -eig.real / math.sqrt(eig.real**2 + eig.imag**2)

    def _natural_frequency(self, eig: complex) -> float:
        if abs(eig.imag) < self.EPSILON:
            return 0.0
        w_n = math.sqrt(eig.real**2 + eig.imag**2)
        return w_n / (2 * math.pi)

    def _damped_frequency(self, eig: complex) -> float:
        w_n = 2 * math.pi * self._natural_frequency(eig)
        zeta = self._damping_ratio(eig)
        w_d = w_n * math.sqrt(max(1 - zeta**2, 0.0))
        return w_d / (2 * math.pi)

    def __lt__(self, other: Self) -> bool:
        return self.index < other.index

    def __copy__(self) -> Self:
        return Eigenvalue(self.value, self.index)

    def __repr__(self) -> str:
        return f"Eigenvalue({self.value.real:.4f}{self.value.imag:+.4f}j, index={self.index})"


class EigenvalueSet:
    """An immutable set of `Eigenvalue`s, e.g. all the eigenvalues of one
    modal analysis run."""

    def __init__(
        self,
        eigenvalues: npt.NDArray | list[Eigenvalue],
        indexes: int | list[int] | None = None,
    ) -> None:
        """
        Args:
            eigenvalues: an array of eigenvalues, or a list of `Eigenvalue` objects.
            indexes: a single index or list of indexes for the eigenvalues.
                If `eigenvalues` is an array and `indexes` is omitted, they
                are indexed 1..len(eigenvalues). If a list of `Eigenvalue`
                objects is passed together with `indexes`, they are reindexed.
        """
        indexes = self._handle_indexes(indexes, eigenvalues)
        if isinstance(eigenvalues, np.ndarray):
            self.eigenvalues = self._from_array(eigenvalues, indexes)
        else:
            self.eigenvalues = self._from_list(eigenvalues, indexes)
        self.df = self._create_dataframe(self.eigenvalues)
        self._iter_pos = 0

    def get_indexes(self) -> list[int]:
        return [e.get_index() for e in self.eigenvalues]

    def get_vector(self) -> npt.NDArray:
        """The eigenvalues as a complex vector, in index order."""
        real = self.df[REAL_COL].to_numpy()
        imag = self.df[IMAG_COL].to_numpy()
        return real + 1j * imag

    def get_dataframe(self) -> DataFrame:
        """One row per eigenvalue: real/imaginary part, natural/damped
        frequency and damping ratio, indexed by eigenvalue index."""
        return self.df.copy()

    def filter_by_index(self, indexes: int | list[int]) -> Self:
        """Keep only the eigenvalues at the given index(es)."""
        indexes = self._normalize_indexes(indexes)
        eigenvalues = [e for e in self.eigenvalues if e.get_index() in indexes]
        return EigenvalueSet(eigenvalues)

    def filter_by_damping_ratio(self, max_damping_ratio: float) -> Self:
        """Drop eigenvalues whose damping ratio is above `max_damping_ratio`
        - i.e. keep the poorly-damped/unstable ones."""
        eigenvalues = [
            e for e in self.eigenvalues if e.get_damp_ratio() <= max_damping_ratio
        ]
        return EigenvalueSet(eigenvalues)

    def filter_out_conjugates(self) -> Self:
        """Keep only one eigenvalue of each complex-conjugate pair (the one
        with non-negative imaginary part)."""
        eigenvalues = [e for e in self.eigenvalues if e.get_imag() >= 0]
        return EigenvalueSet(eigenvalues)

    def filter_out_real_modes(self) -> Self:
        """Keep only the complex (oscillatory) eigenvalues."""
        eigenvalues = [
            e for e in self.eigenvalues if abs(e.get_imag()) >= Eigenvalue.EPSILON
        ]
        return EigenvalueSet(eigenvalues)

    def map_eigenvalues(self, index_map: dict[int, int]) -> Self:
        """Reindex the eigenvalues according to a map from current to new index."""
        eigenvalues = [e.set_index(index_map[e.get_index()]) for e in self.eigenvalues]
        return EigenvalueSet(eigenvalues)

    def plot(
        self,
        ax: plt.Axes | None = None,
        *,
        xlim: tuple[float, float] | Literal["auto"] | None = "auto",
        quantile: float = DEFAULT_DOMINANT_QUANTILE,
    ) -> plt.Axes:
        """Scatter the eigenvalues in the complex plane, shading the unstable
        (right) half-plane.

        Args:
            ax: axes to draw on (a new figure is created if omitted).
            xlim: `"auto"` (default) zooms the x-axis to the dominant
                eigenvalues via `_auto_real_xlim`; pass an explicit `(lo, hi)`
                to override, or `None` for matplotlib's own full-range default.
            quantile: only used when `xlim="auto"`. The fraction of
                eigenvalues (by real part) to zoom *out* past - e.g. the
                default 0.75 frames roughly the most dominant quarter of
                eigenvalues; raise it (closer to 1) to zoom in on fewer,
                more dominant eigenvalues, or lower it to include more of
                the faster/better-damped ones.
        """
        if ax is None:
            _, ax = plt.subplots()
        df = self.get_dataframe()
        ax.scatter(df[REAL_COL], df[IMAG_COL], marker="x")
        if xlim == "auto":
            xlim = _auto_real_xlim(df[REAL_COL].to_numpy(), quantile=quantile)
        if xlim is not None:
            ax.set_xlim(xlim)
        left, right = ax.get_xlim()
        ax.axvspan(0, right, facecolor="red", alpha=0.2)
        ax.set_xlim([left, right])
        ax.set_xlabel("Real")
        ax.set_ylabel("Imaginary")
        ax.set_title("Eigenvalues")
        ax.grid(True)
        return ax

    def _create_dataframe(self, eigenvalues: list[Eigenvalue]) -> DataFrame:
        return (
            pd.concat([e.get_series() for e in eigenvalues], axis=1)
            .T.astype({INDEX_COL: int})
            .set_index(INDEX_COL)
        )

    def _handle_indexes(
        self,
        indexes: int | list[int] | None,
        eigenvalues: npt.NDArray | list[Eigenvalue],
    ) -> list[int] | None:
        if indexes is None:
            if isinstance(eigenvalues, np.ndarray):
                return list(range(1, len(eigenvalues) + 1))
            return None
        return self._normalize_indexes(indexes)

    def _normalize_indexes(self, indexes: int | list[int]) -> list[int]:
        return [indexes] if isinstance(indexes, (int, np.integer)) else list(indexes)

    def _from_array(
        self, array: npt.NDArray, indexes: list[int]
    ) -> list[Eigenvalue]:
        eigenvalues = [Eigenvalue(value, idx) for value, idx in zip(array, indexes)]
        eigenvalues.sort()
        return eigenvalues

    def _from_list(
        self, eigenvalues: list[Eigenvalue], indexes: list[int] | None
    ) -> list[Eigenvalue]:
        if indexes:
            eigenvalues = [e.set_index(idx) for e, idx in zip(eigenvalues, indexes)]
        eigenvalues = list(eigenvalues)
        eigenvalues.sort()
        return eigenvalues

    def __sub__(self, other: Self) -> DataFrame:
        """Difference of the two sets, column by column (real/imag part,
        frequencies, damping ratio), row-aligned by eigenvalue index -
        track_eigenvalues()/track_eigenvalues_from() first if the indexes
        might not already correspond to the same physical mode."""
        self_df, other_df = self.get_dataframe(), other.get_dataframe()
        if len(self_df.index) != len(other_df.index):
            raise PFEigenvalueMismatchError(
                "Cannot subtract eigenvalue sets of different length: "
                f"{len(self_df.index)} vs {len(other_df.index)}."
            )
        return self_df - other_df

    def __len__(self) -> int:
        return len(self.eigenvalues)

    def __iter__(self) -> Self:
        self._iter_pos = 0
        return self

    def __next__(self) -> Eigenvalue:
        if self._iter_pos >= len(self):
            raise StopIteration
        e = self.eigenvalues[self._iter_pos]
        self._iter_pos += 1
        return e

    def __repr__(self) -> str:
        return f"EigenvalueSet({np.array2string(self.get_vector(), precision=2, suppress_small=True)})"


class ParticipationFactor:
    """The participation of every state in a single eigenvalue."""

    def __init__(
        self, participation: npt.NDArray, states: npt.NDArray[np.str_], index: int
    ) -> None:
        if participation.ndim > 1 or states.ndim > 1:
            raise PFEigenvalueMismatchError(
                "'participation' and 'states' must both be one-dimensional; got "
                f"{participation.ndim} and {states.ndim} dimensions."
            )
        self.participation = participation
        self.states = states
        self.index = index

    def get_index(self) -> int:
        return self.index

    def get_array(self) -> npt.NDArray:
        return self.participation

    def get_series(self) -> Series:
        # Built from plain lists (not np.insert into self.states) because a
        # fixed-width numpy string array (e.g. dtype '<U1' for single-char
        # state names) would silently truncate the "Index" label.
        index = [INDEX_COL, *self.states.tolist()]
        values = [self.index, *self.participation.tolist()]
        return pd.Series(values, index=index)

    def set_index(self, index: int) -> Self:
        """A copy with a different eigenvalue index (does not mutate `self`)."""
        return ParticipationFactor(self.participation, self.states, index)

    def filter_by_states(self, states: str | list[str]) -> Self:
        states_to_keep = {states} if isinstance(states, str) else set(states)
        mask = np.isin(self.states, list(states_to_keep))
        return ParticipationFactor(self.participation[mask], self.states[mask], self.index)

    def __lt__(self, other: Self) -> bool:
        return self.index < other.index


class ParticipationFactorSet:
    """Participation factors of every state in every eigenvalue of one modal
    analysis run - a `(state, eigenvalue index)` matrix."""

    def __init__(
        self,
        participations: npt.NDArray | list[ParticipationFactor],
        states: npt.NDArray[np.str_] | None = None,
        indexes: int | list[int] | None = None,
    ) -> None:
        """
        Args:
            participations: a `(state, eigenvalue)` array, or a list of
                `ParticipationFactor` objects (one per eigenvalue).
            states: state names - required when `participations` is an array.
            indexes: eigenvalue indexes (one per column of `participations`).
                Defaults to 1..n.
        """
        indexes = self._handle_indexes(indexes, participations)
        if isinstance(participations, np.ndarray):
            if states is None:
                raise PFEigenvalueMismatchError(
                    "'states' must be given when 'participations' is an array."
                )
            self.parts = [
                ParticipationFactor(participations[:, n], states, idx)
                for n, idx in enumerate(indexes)
            ]
            self.parts.sort()
        else:
            parts = list(participations)
            if indexes:
                parts = [p.set_index(idx) for p, idx in zip(parts, indexes)]
            parts.sort()
            self.parts = parts
        self.df = self._create_dataframe(self.parts)
        self._iter_pos = 0

    def get_states(self) -> npt.NDArray[np.str_]:
        return self.df.index.to_numpy()

    def get_array(self) -> npt.NDArray:
        return self.df.to_numpy()

    def get_dataframe(self) -> DataFrame:
        """`(state, eigenvalue index)` matrix of participation factors."""
        return self.df.copy()

    def filter_by_eigenvalue_index(self, index: int | list[int]) -> Self:
        indexes = self._normalize_indexes(index)
        parts = [p for p in self.parts if p.get_index() in indexes]
        return ParticipationFactorSet(parts)

    def filter_by_states(self, states: str | list[str]) -> Self:
        parts = [p.filter_by_states(states) for p in self.parts]
        return ParticipationFactorSet(parts)

    def filter_by_min_state_participation(self, min_participation: float) -> Self:
        """Keep only states whose participation, summed over every eigenvalue
        currently in this set, is at least `min_participation`."""
        totals = self.df.sum(axis=1)
        states_to_keep = totals.index[totals >= min_participation].tolist()
        return self.filter_by_states(states_to_keep)

    def map_eigenvalues(self, index_map: dict[int, int]) -> Self:
        parts = [p.set_index(index_map[p.get_index()]) for p in self.parts]
        return ParticipationFactorSet(parts)

    def plot(self, *, top_n: int | None = 15) -> plt.Figure:
        """Horizontal bar chart of the participation of every state - one
        panel per eigenvalue currently in this set.

        Args:
            top_n: only the `top_n` states with the highest total
                participation (summed over every eigenvalue currently in
                this set) are shown - with many states, showing all of them
                makes the y-axis labels unreadably crowded. `None` shows
                every state.
        """
        df = self.get_dataframe()
        if top_n is not None and len(df.index) > top_n:
            top_states = df.sum(axis=1).sort_values(ascending=False).index[:top_n]
            df = df.loc[top_states]
        states = df.index.tolist()
        y_pos = np.arange(len(states))
        eigenvalue_indexes = df.columns.tolist()
        fig, axes = plt.subplots(
            len(eigenvalue_indexes),
            1,
            squeeze=False,
            figsize=(6, 0.3 * len(states) + 1.2 * len(eigenvalue_indexes)),
        )
        for row, idx in enumerate(eigenvalue_indexes):
            ax = axes[row][0]
            ax.barh(y_pos, df[idx].to_numpy())
            ax.set_yticks(y_pos, labels=states, fontsize="small")
            ax.set_xlabel("Participation")
            ax.set_title(f"Eigenvalue {idx}")
        fig.tight_layout()
        return fig

    def _create_dataframe(self, parts: list[ParticipationFactor]) -> DataFrame:
        return (
            pd.concat([p.get_series() for p in parts], axis=1)
            .T.astype({INDEX_COL: int})
            .set_index(INDEX_COL)
            .T
        )

    def _handle_indexes(
        self,
        indexes: int | list[int] | None,
        participations: npt.NDArray | list[ParticipationFactor],
    ) -> list[int] | None:
        if indexes is None:
            if isinstance(participations, np.ndarray):
                return list(range(1, participations.shape[1] + 1))
            return None
        return self._normalize_indexes(indexes)

    def _normalize_indexes(self, indexes: int | list[int]) -> list[int]:
        return [indexes] if isinstance(indexes, (int, np.integer)) else list(indexes)

    def __len__(self) -> int:
        return len(self.parts)

    def __iter__(self) -> Self:
        self._iter_pos = 0
        return self

    def __next__(self) -> ParticipationFactor:
        if self._iter_pos >= len(self):
            raise StopIteration
        p = self.parts[self._iter_pos]
        self._iter_pos += 1
        return p


# --------------------------------------------------------------------------- #
# eigenvalue tracking
# --------------------------------------------------------------------------- #


class _IndexCandidate:
    """One candidate mapping from a scrambled eigenvalue's current position to
    a reference eigenvalue's position, with a certainty score (higher = better)."""

    def __init__(self, current_position: int, target_position: int, certainty: float) -> None:
        self.current_position = current_position
        self.target_position = target_position
        self.certainty = certainty


class _EigenvaluePositionElection:
    """Assigns each scrambled eigenvalue position a unique target position by
    repeatedly picking the remaining candidate pair with the highest certainty."""

    def __init__(self, current_indexes: list[int], target_indexes: list[int]) -> None:
        self.candidates: dict[int, dict[int, _IndexCandidate | None]] = {
            n: {m: None for m in target_indexes} for n in current_indexes
        }
        self.winners: dict[int, int] = {n: -1 for n in current_indexes}

    def add_candidates(self, candidates: list[_IndexCandidate]) -> None:
        for candidate in candidates:
            existing = self.candidates[candidate.current_position].get(
                candidate.target_position
            )
            if existing is not None:
                candidate = _IndexCandidate(
                    candidate.current_position,
                    candidate.target_position,
                    existing.certainty + candidate.certainty,
                )
            self.candidates[candidate.current_position][candidate.target_position] = (
                candidate
            )

    def elect_best_candidate(self) -> bool:
        """Elect the remaining candidate with the highest certainty. Returns
        False (without electing anything) once no candidates remain."""
        best: _IndexCandidate | None = None
        for candidates in self.candidates.values():
            for candidate in candidates.values():
                if candidate is not None and (
                    best is None or candidate.certainty > best.certainty
                ):
                    best = candidate
        if best is None:
            return False

        self.winners[best.current_position] = best.target_position
        for target in self.candidates[best.current_position]:
            self.candidates[best.current_position][target] = None
        for candidates in self.candidates.values():
            candidates[best.target_position] = None
        return True

    def get_winners(self) -> dict[int, int]:
        return self.winners


class EigenvalueTracker:
    """Reorders a 'scrambled' set of eigenvalues (and matching participation
    factors) to line up index-for-index with a reference set from another
    run - PowerFactory does not guarantee eigenvalues come back in the same
    order between two modal analyses.

    Candidates for "this scrambled eigenvalue is that reference eigenvalue"
    are scored by three independent distances (nearest eigenvalue in the
    complex plane, nearest participation-factor vector, nearest natural
    frequency - the latter weighted up, since it discriminates well between
    otherwise-similar complex-conjugate-like pairs) and elected by taking the
    best-scoring pair first, repeatedly, until every position is assigned.
    """

    #: weight amplifying the natural-frequency distance relative to the
    #: eigenvalue and participation-factor distances (chosen empirically).
    NATURAL_FREQUENCY_WEIGHT = 3
    #: the maximum possible distance between two (normalized) participation vectors.
    PARTICIPATION_NORMALIZATION = 2

    def __init__(
        self,
        eig_ref: EigenvalueSet,
        eig_scrambled: EigenvalueSet,
        pf_ref: ParticipationFactorSet,
        pf_scrambled: ParticipationFactorSet,
    ) -> None:
        """
        Args:
            eig_ref: eigenvalues of the reference run.
            eig_scrambled: eigenvalues to reorder to match `eig_ref`.
            pf_ref: participation factors of the reference run.
            pf_scrambled: participation factors matching `eig_scrambled`.
        """
        if len(eig_ref) != len(eig_scrambled):
            raise PFEigenvalueMismatchError(
                f"Length of eigenvalue sets must match to track them: got "
                f"{len(eig_ref)} and {len(eig_scrambled)}."
            )
        self.eig_ref = eig_ref
        self.eig_scrambled = eig_scrambled
        self.pf_ref = pf_ref
        self.pf_scrambled = pf_scrambled
        self.election = _EigenvaluePositionElection(
            eig_scrambled.get_indexes(), eig_ref.get_indexes()
        )

    def calculate_index_map(self) -> dict[int, int]:
        """Compute the map from `eig_scrambled`'s current indexes to the
        index of the reference eigenvalue each one is deemed to correspond to."""
        self._add_eigenvalue_distance_candidates()
        self._add_participation_distance_candidates()
        self._add_natural_frequency_distance_candidates()
        while self.election.elect_best_candidate():
            pass
        index_map = self.election.get_winners()

        if len(set(index_map.values())) < len(index_map):
            raise PFEigenvalueTrackingError(
                "Eigenvalue tracking is ambiguous: two or more eigenvalues "
                "would map to the same position.\n"
                f"Reference eigenvalues: {self.eig_ref!r}\n"
                f"Scrambled eigenvalues: {self.eig_scrambled!r}\n"
                f"Index map: {index_map}"
            )
        return index_map

    def unscramble(self) -> tuple[EigenvalueSet, ParticipationFactorSet]:
        """Reorder `eig_scrambled` / `pf_scrambled` to match `eig_ref`'s order."""
        index_map = self.calculate_index_map()
        return (
            self.eig_scrambled.map_eigenvalues(index_map),
            self.pf_scrambled.map_eigenvalues(index_map),
        )

    def _add_eigenvalue_distance_candidates(self) -> None:
        for eig in self.eig_scrambled:
            candidates = [
                _IndexCandidate(
                    eig.get_index(),
                    ref.get_index(),
                    -abs(ref.get_value() - eig.get_value()),
                )
                for ref in self.eig_ref
            ]
            self.election.add_candidates(candidates)

    def _add_participation_distance_candidates(self) -> None:
        for pf in self.pf_scrambled:
            candidates = [
                _IndexCandidate(
                    pf.get_index(),
                    ref.get_index(),
                    -np.linalg.norm(ref.get_array() - pf.get_array())
                    / self.PARTICIPATION_NORMALIZATION,
                )
                for ref in self.pf_ref
            ]
            self.election.add_candidates(candidates)

    def _add_natural_frequency_distance_candidates(self) -> None:
        for eig in self.eig_scrambled:
            candidates = [
                _IndexCandidate(
                    eig.get_index(),
                    ref.get_index(),
                    -abs(ref.get_nat_freq() - eig.get_nat_freq())
                    * self.NATURAL_FREQUENCY_WEIGHT,
                )
                for ref in self.eig_ref
            ]
            self.election.add_candidates(candidates)


def track_eigenvalues(results: Sequence["ModalAnalysisResults"]) -> list["ModalAnalysisResults"]:
    """Track eigenvalues across a sequence of modal analysis runs (e.g. the
    `raw` results of a `parstudy.Study` sweep), so every result's eigenvalue
    index consistently refers to the same physical mode.

    Each result is tracked against the *previous* (already-tracked) one, not
    against the first, so a mode can drift gradually across many runs without
    ever being compared to a very different reference.

    Args:
        results: the modal analysis results in run order. The first is kept
            as-is and used as the initial reference.

    Returns:
        A new list of `ModalAnalysisResults`, reindexed to be consistent
        with one another.
    """
    tracked: list[ModalAnalysisResults] = []
    for i, result in enumerate(results):
        if i == 0:
            tracked.append(result)
        else:
            tracked.append(result.track_eigenvalues_from(tracked[-1]))
    return tracked


# --------------------------------------------------------------------------- #
# modal analysis
# --------------------------------------------------------------------------- #


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


class ModalAnalysis(ApplicationBase):
    """Modal (small-signal) analysis of PowerFactory's current state.

    Activate the study case / scenario / operating point you want analyzed
    yourself first (like `DynamicSimulation` or `StaticCalc` - this class
    does not switch study cases for you).
    """

    #: default `ComMod` parameters: calculate eigenvectors and participation
    #: factors and export the system matrix, without dropping any eigenvalue
    #: from the results (every 'only record ...' filter switched off).
    DEFAULT_COMMOD_PARAMS: dict[str, Any] = {
        "iLeft": True,
        "iRight": True,
        "iPart": True,
        "initMode": 0,
        "iSysMatsMatl": True,
        "isRecOscModesOnly": False,
        "isRecUnstabModesOnly": False,
        "isRecMinReal": False,
        "isRecMaxReal": False,
        "isRecMinImag": False,
        "isRecMaxImag": False,
        "isRecMinMagn": False,
        "isRecMaxMagn": False,
        "isRecMinDampRat": False,
        "isRecMaxDampRat": False,
    }

    def __init__(self, pf_app: PFApp | None | bool = False, cached: bool = False) -> None:
        super().__init__(pf_app, cached)

    def run(self, commod_params: dict[str, Any] | None = None) -> ModalAnalysisResults:
        """Run the modal analysis command (`ComMod`) and return the eigenvalues
        and participation factors of the current operating point.

        Args:
            commod_params: additional/overriding `ComMod` parameters, merged
                over `DEFAULT_COMMOD_PARAMS`.

        Returns:
            ModalAnalysisResults: the eigenvalues, participation factors and
            system matrix.
        """
        export_dir = join(getcwd(), "dynamic_modal_analysis_export")
        makedirs(export_dir, exist_ok=True)
        try:
            self._run_commod(export_dir, commod_params or {})
            sys_matrix = self._read_system_matrix(export_dir)
            state_names = self._read_state_names(export_dir)
        finally:
            rmtree(export_dir, ignore_errors=True)

        indexes = list(range(1, len(state_names) + 1))
        eigenvalue_vec, participation, left_vec, right_vec = self._eigenvalues_and_participation(
            sys_matrix
        )
        eigenvalues = EigenvalueSet(eigenvalue_vec, indexes)
        participation_factors = ParticipationFactorSet(participation, state_names, indexes)
        right_eigenvectors = pd.DataFrame(right_vec, index=state_names, columns=indexes)
        left_eigenvectors = pd.DataFrame(left_vec, index=state_names, columns=indexes)
        return ModalAnalysisResults(
            sys_matrix,
            eigenvalues,
            participation_factors,
            right_eigenvectors=right_eigenvectors,
            left_eigenvectors=left_eigenvectors,
        )

    def _run_commod(self, export_dir: str, commod_params: dict[str, Any]) -> None:
        commod: ComMod = self.act_prj.get_from_study_case("ComMod")
        params = {**self.DEFAULT_COMMOD_PARAMS, "dirMatl": export_dir, **commod_params}
        self.act_prj.set_attr(commod, params)
        commod.Execute()

    def _read_system_matrix(self, export_dir: str) -> npt.NDArray[np.complex128]:
        """Parse the exported system (A) matrix.

        `Amat.mtl` follows the sparse coordinate format MATLAB's `spconvert`
        expects: each row is `row column real [imag]`.
        """
        df = pd.read_csv(
            join(export_dir, "Amat.mtl"),
            sep=r"\s+",
            header=None,
            names=["row", "column", "re", "imag"],
            dtype={"row": int, "column": int, "re": float, "imag": float},
            encoding="ISO-8859-1",
            engine="python",
        )
        size = int(df["row"].max())
        sys_matrix = np.zeros((size, size), dtype=np.complex128)
        rows = df["row"].to_numpy() - 1
        cols = df["column"].to_numpy() - 1
        re = df["re"].to_numpy()
        imag = df["imag"].to_numpy()
        has_imag = ~np.isnan(imag)
        sys_matrix[rows[~has_imag], cols[~has_imag]] = re[~has_imag]
        sys_matrix[rows[has_imag], cols[has_imag]] = re[has_imag] + 1j * imag[has_imag]
        return sys_matrix

    def _read_state_names(self, export_dir: str) -> npt.NDArray[np.str_]:
        """Parse the exported list of state variable names, as
        `"<model name>\\\\<state variable>"`."""
        df = pd.read_csv(
            join(export_dir, "VariableToIdx_Amat.txt"),
            sep=r"\s\s+",
            header=0,
            names=["Matrix column index", "Model name", "State variable"],
            dtype={"Matrix column index": int, "Model name": str, "State variable": str},
            encoding="ISO-8859-1",
            index_col=0,
            engine="python",
        )
        state_var = df["State variable"].str.replace('"', "", regex=False)
        return (df["Model name"] + "\\" + state_var).to_numpy(dtype=str)

    def _eigenvalues_and_participation(
        self, sys_matrix: npt.NDArray[np.complex128]
    ) -> tuple[
        npt.NDArray[np.complex128],
        npt.NDArray[np.float64],
        npt.NDArray[np.complex128],
        npt.NDArray[np.complex128],
    ]:
        """Eigenvalues, the (normalized) participation of every state in
        every eigenvalue, and the raw left/right eigenvectors, from one
        combined eigendecomposition.

        Participation factor `p_ki = |phi_ki| * |psi_ik|` (right eigenvector
        element times left eigenvector element), normalized so each
        eigenvalue's participation column sums to 1 (Perez-Arriaga et al.) -
        the same `phi`/`psi` also used, unnormalized, by
        `ModalAnalysisResults.eigenvalue_sensitivity`.
        """
        eigenvalues, left_vec, right_vec = eig(sys_matrix, left=True, right=True)
        participation = np.abs(left_vec) * np.abs(right_vec)
        participation = participation / participation.sum(axis=0, keepdims=True)
        return eigenvalues, participation, left_vec, right_vec


# --------------------------------------------------------------------------- #
# eigenvalue sweeps (built on parstudy.Study)
# --------------------------------------------------------------------------- #


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


# --------------------------------------------------------------------------- #
# modal sensitivity
# --------------------------------------------------------------------------- #


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
