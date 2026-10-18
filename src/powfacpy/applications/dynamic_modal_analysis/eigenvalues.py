"""Eigenvalues and participation factors (single values and sets, with tables and plots).
"""

from __future__ import annotations

import math
from typing import Literal, Self
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas import DataFrame, Series

from powfacpy.exceptions import PFEigenvalueMismatchError
from powfacpy.applications.dynamic_modal_analysis._common import (
    DAMPED_FREQ_COL,
    DAMPING_RATIO_COL,
    DEFAULT_DOMINANT_QUANTILE,
    IMAG_COL,
    INDEX_COL,
    NATURAL_FREQ_COL,
    REAL_COL,
    _auto_real_xlim,
)


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
