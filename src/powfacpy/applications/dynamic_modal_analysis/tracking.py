"""Consistent indexing of eigenvalues across runs.

PowerFactory does not return eigenvalues in the same order from run to run. The tracker matches them between consecutive runs so that a sweep yields one trajectory per eigenvalue.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Sequence
import numpy as np

from powfacpy.exceptions import PFEigenvalueMismatchError, PFEigenvalueTrackingError
from powfacpy.applications.dynamic_modal_analysis.eigenvalues import EigenvalueSet, ParticipationFactorSet

if TYPE_CHECKING:
    from powfacpy.applications.dynamic_modal_analysis.results import ModalAnalysisResults


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
