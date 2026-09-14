"""Tests for powfacpy.applications.dynamic_modal_analysis.

Pure Python - EigenvalueSet / ParticipationFactorSet / EigenvalueTracker /
ModalAnalysisResults / Sensitivity / ParametricSensitivity only manipulate
plain arrays and DataFrames, so no PowerFactory is needed. ModalAnalysis
itself (running ComMod against a real project) is exercised separately in
tests that need a live PowerFactory (not included here).
"""

import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, r".\src")

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory

pytest.importorskip("scipy")
from scipy.linalg import eig

from powfacpy.applications.dynamic_modal_analysis import (
    DEFAULT_DOMINANT_QUANTILE,
    Eigenvalue,
    EigenvalueSet,
    EigenvalueSweepResults,
    EigenvalueTracker,
    ModalAnalysisResults,
    ParametricSensitivity,
    ParticipationFactor,
    ParticipationFactorSet,
    Sensitivity,
    sensitivity_between,
    system_matrix_sensitivity,
    track_eigenvalues,
)
from powfacpy.applications.dynamic_modal_analysis import _auto_real_xlim
from powfacpy.exceptions import PFAttributeNotSetError, PFEigenvalueMismatchError

REAL_COL = "Real (1/s)"
IMAG_COL = "Imag (rad/s)"
MODE_COL = "Mode"
DAMPED_FREQ_COL = "Damped frequency (Hz)"
UNDAMPED_FREQ_COL = "Undamped natural frequency (Hz)"
DOMINANT_STATES_COL = "Dominant states"


def gen_state_names(n: int) -> np.ndarray:
    return np.array([f"state{i}" for i in range(n)])


def gen_zero_participation_factors(n: int) -> ParticipationFactorSet:
    return ParticipationFactorSet(np.zeros((n, n)), gen_state_names(n))


# --------------------------------------------------------------------------- #
# EigenvalueSet
# --------------------------------------------------------------------------- #


def test_EigenvalueSet_can_be_instantiated_with_array():
    df = EigenvalueSet(np.array([0.1, 0.2, 0.3])).get_dataframe()

    assert df.index.to_list() == [1, 2, 3]
    assert df.loc[1, REAL_COL] == 0.1
    assert df.loc[2, REAL_COL] == 0.2
    assert df.loc[3, REAL_COL] == 0.3


def test_EigenvalueSet_can_be_instantiated_with_array_and_index():
    df = EigenvalueSet(np.array([0.1, 0.2, 0.3]), indexes=[4, 5, 6]).get_dataframe()

    assert df.index.to_list() == [4, 5, 6]
    assert df.loc[4, REAL_COL] == 0.1


def test_EigenvalueSet_can_be_instantiated_with_eigenvalue_list():
    e1 = Eigenvalue(value=0.1, index=10)
    e2 = Eigenvalue(value=0.2, index=20)
    df = EigenvalueSet([e1, e2]).get_dataframe()

    assert df.index.to_list() == [10, 20]
    assert df.loc[10, REAL_COL] == 0.1
    assert df.loc[20, REAL_COL] == 0.2


def test_EigenvalueSet_index_is_integer():
    df = EigenvalueSet(np.array([1, 2, 3])).get_dataframe()
    assert df.index.dtype == int


def test_EigenvalueSet_dataframe_sorted_by_index():
    e1 = Eigenvalue(value=0.1, index=3)
    e2 = Eigenvalue(value=0.2, index=2)
    e3 = Eigenvalue(value=0.3, index=1)
    df = EigenvalueSet([e1, e2, e3]).get_dataframe()

    assert df.index.to_list() == [1, 2, 3]


def test_EigenvalueSet_filter_by_one_index():
    eig = EigenvalueSet(np.array([1, 2, 3]))
    df = eig.filter_by_index(2).get_dataframe()

    assert len(df) == 1
    assert df.loc[2, REAL_COL] == 2


def test_EigenvalueSet_filter_by_index_accepts_numpy_integer():
    # pandas .idxmin()/.idxmax() return numpy.int64, not a plain int - a
    # common way to obtain the index to filter by (e.g. the worst-damped mode).
    eig = EigenvalueSet(np.array([1, 2, 3]))
    numpy_index = eig.get_dataframe()[REAL_COL].idxmax()
    assert isinstance(numpy_index, np.integer)

    df = eig.filter_by_index(numpy_index).get_dataframe()
    assert len(df) == 1
    assert df.loc[3, REAL_COL] == 3


def test_EigenvalueSet_filter_by_multiple_indexes():
    eig = EigenvalueSet(np.array([1, 2, 3]))
    df = eig.filter_by_index([1, 3]).get_dataframe()

    assert len(df) == 2
    assert df.loc[1, REAL_COL] == 1
    assert df.loc[3, REAL_COL] == 3


def test_EigenvalueSet_filter_by_damping_ratio():
    eig = EigenvalueSet(np.array([complex(-0.5, 7), -1, -1]))
    df = eig.filter_by_damping_ratio(0.5).get_dataframe()

    assert len(df) == 1
    assert df.loc[1, REAL_COL] == -0.5
    assert df.loc[1, IMAG_COL] == 7


def test_EigenvalueSet_filter_out_conjugates():
    eig = EigenvalueSet(np.array([complex(-0.5, 7), complex(-0.5, -7), -1]))
    df = eig.filter_out_conjugates().get_dataframe()

    assert df.index.to_list() == [1, 3]


def test_EigenvalueSet_filter_out_real_modes():
    eig = EigenvalueSet(np.array([complex(-0.5, 7), complex(-0.5, -7), -1, -1]))
    df = eig.filter_out_real_modes().get_dataframe()

    assert df.index.to_list() == [1, 2]


def test_EigenvalueSet_subtraction():
    eig = EigenvalueSet(np.array([1, 1]))
    diff = eig - eig

    assert diff.loc[1, REAL_COL] == 0
    assert diff.loc[1, IMAG_COL] == 0


def test_EigenvalueSet_subtraction_different_number_eigenvalues():
    eig1 = EigenvalueSet(np.array([1, 1]))
    eig2 = EigenvalueSet(np.array([1, 1, -1]))

    with pytest.raises(PFEigenvalueMismatchError):
        eig1 - eig2


def test_EigenvalueSet_iteration_and_len():
    eig = EigenvalueSet(np.array([1, 2, 3]))
    assert len(eig) == 3
    assert [e.get_index() for e in eig] == [1, 2, 3]
    # iterating twice must both work (counter is reset)
    assert [e.get_index() for e in eig] == [1, 2, 3]


def test_EigenvalueSet_plot_auto_xlim_uses_default_quantile():
    real_parts = np.array([-1.0, -10.0, -20.0, -40.0, -100.0])
    ax = EigenvalueSet(real_parts.astype(complex)).plot()
    assert ax.get_xlim() == _auto_real_xlim(real_parts, quantile=DEFAULT_DOMINANT_QUANTILE)


def test_EigenvalueSet_plot_auto_xlim_quantile_is_forwarded():
    real_parts = np.array([-1.0, -10.0, -20.0, -40.0, -100.0])
    ax = EigenvalueSet(real_parts.astype(complex)).plot(quantile=0.4)
    assert ax.get_xlim() == _auto_real_xlim(real_parts, quantile=0.4)


def test_auto_real_xlim_higher_quantile_zooms_in_tighter():
    real_parts = np.array([-1.0, -10.0, -20.0, -40.0, -100.0])
    loose_lo, _ = _auto_real_xlim(real_parts, quantile=0.25)
    tight_lo, _ = _auto_real_xlim(real_parts, quantile=0.9)
    # a higher quantile keeps only the more dominant (less negative) tail,
    # so its lower bound must not reach as far left as the loose one's.
    assert tight_lo > loose_lo


# --------------------------------------------------------------------------- #
# ParticipationFactorSet
# --------------------------------------------------------------------------- #


def test_ParticipationFactorSet_can_be_instantiated_with_array():
    df = ParticipationFactorSet(
        np.array([[0.5, 0.5], [0.3, 0.7]]), states=np.array(["position", "speed"])
    ).get_dataframe()

    assert df.loc["position", 1] == 0.5
    assert df.loc["speed", 2] == 0.7


def test_ParticipationFactorSet_can_be_instantiated_with_participation_list():
    states = np.array(["position", "speed"])
    p1 = ParticipationFactor(np.array([0.5, 0.3]), states, index=10)
    p2 = ParticipationFactor(np.array([0.5, 0.7]), states, index=20)
    df = ParticipationFactorSet([p1, p2]).get_dataframe()

    assert df.loc["position", 10] == 0.5
    assert df.loc["speed", 20] == 0.7


def test_ParticipationFactorSet_dataframe_sorted_by_index():
    states = np.array(["position", "speed"])
    p1 = ParticipationFactor(np.array([0.5, 0.3]), states, index=2)
    p2 = ParticipationFactor(np.array([0.5, 0.7]), states, index=1)
    df = ParticipationFactorSet([p1, p2]).get_dataframe()

    assert df.columns.to_list() == [1, 2]


def test_ParticipationFactorSet_filter_by_eigenvalue_index():
    pf = ParticipationFactorSet(
        np.array([[0.5, 0.5], [0.3, 0.7]]),
        states=np.array(["position", "speed"]),
        indexes=[1, 2],
    )
    df = pf.filter_by_eigenvalue_index(1).get_dataframe()

    assert df.loc["position", 1] == 0.5
    assert df.loc["speed", 1] == 0.3


def test_ParticipationFactorSet_filter_by_state():
    pf = ParticipationFactorSet(
        np.array([[0.5, 0.5], [0.3, 0.7]]), states=np.array(["position", "speed"])
    )
    df = pf.filter_by_states("position").get_dataframe()

    assert df.index.to_list() == ["position"]


def test_ParticipationFactorSet_filter_by_min_state_participation():
    pf = ParticipationFactorSet(
        np.array([[0.5, 0.5], [0.05, 0.03]]), states=np.array(["position", "speed"])
    )
    df = pf.filter_by_min_state_participation(0.1).get_dataframe()

    assert df.index.to_list() == ["position"]


def test_ParticipationFactor_rejects_multidimensional_input():
    with pytest.raises(PFEigenvalueMismatchError):
        ParticipationFactor(np.array([[0.1, 0.2]]), np.array(["a", "b"]), index=1)


# --------------------------------------------------------------------------- #
# EigenvalueTracker
# --------------------------------------------------------------------------- #


def test_EigenvalueTracker():
    eig1 = EigenvalueSet(np.array([-1, -2 + 1j, -2 - 1j]))
    eig2 = EigenvalueSet(np.array([-2 + 1j, -2 - 1j, -1]))
    pf1 = gen_zero_participation_factors(3)
    pf2 = gen_zero_participation_factors(3)

    want = {1: 2, 2: 3, 3: 1}
    got = EigenvalueTracker(eig1, eig2, pf1, pf2).calculate_index_map()

    assert want == got


def test_EigenvalueTracker_different_eigenvalue_lengths():
    eig1 = EigenvalueSet(np.array([-1, -2 + 1j, -2 - 1j]))
    eig2 = EigenvalueSet(np.array([-1, -1]))
    pf1 = gen_zero_participation_factors(3)
    pf2 = gen_zero_participation_factors(2)

    with pytest.raises(PFEigenvalueMismatchError):
        EigenvalueTracker(eig1, eig2, pf1, pf2)


def test_EigenvalueTracker_repeated_eigenvalues():
    eig1 = EigenvalueSet(np.array([-1, -1]))
    eig2 = EigenvalueSet(np.array([-1, -1]))
    pf1 = gen_zero_participation_factors(2)
    pf2 = gen_zero_participation_factors(2)

    want = {1: 1, 2: 2}
    got = EigenvalueTracker(eig1, eig2, pf1, pf2).calculate_index_map()

    assert want == got


def test_EigenvalueTracker_tracks_real_eigenvalues():
    eig1 = EigenvalueSet(np.array([-1, -10]))
    eig2 = EigenvalueSet(np.array([-1.5, -10.5]))
    pf1 = gen_zero_participation_factors(2)
    pf2 = gen_zero_participation_factors(2)

    want = {1: 1, 2: 2}
    got = EigenvalueTracker(eig1, eig2, pf1, pf2).calculate_index_map()

    assert want == got


def test_EigenvalueTracker_tracks_complex_eigenvalues():
    eig1 = EigenvalueSet(np.array([-1, -2 + 1j, -2 - 1j]))
    eig2 = EigenvalueSet(np.array([-2 + 1.1j, -2.1 - 1j, -1.2]))
    pf1 = gen_zero_participation_factors(3)
    pf2 = gen_zero_participation_factors(3)

    want = {1: 2, 2: 3, 3: 1}
    got = EigenvalueTracker(eig1, eig2, pf1, pf2).calculate_index_map()

    assert want == got


def test_EigenvalueTracker_uses_participation():
    # by eigenvalue distance alone, -1.5 is equidistant from -1 and -2, so
    # participation factors must break the tie.
    eig1 = EigenvalueSet(np.array([0, -1, -2]))
    eig2 = EigenvalueSet(np.array([-1.5, 0.1, -1.5]))
    pf1 = ParticipationFactorSet(
        np.array([[0.1, 0.1, 0.1], [0.2, 0.2, 0.2], [0.3, 0.3, 0.3]]).T,
        gen_state_names(3),
    )
    pf2 = ParticipationFactorSet(
        np.array([[0.3, 0.3, 0.3], [0.1, 0.1, 0.1], [0.2, 0.2, 0.2]]).T,
        gen_state_names(3),
    )

    want = {1: 3, 2: 1, 3: 2}
    got = EigenvalueTracker(eig1, eig2, pf1, pf2).calculate_index_map()

    assert want == got


def test_EigenvalueTracker_uses_natural_frequency():
    # 2+1j and 1+2j share a natural frequency (2.23 Hz); 2+1j is numerically
    # closer to 2+0j, but the natural-frequency match should win.
    eig1 = EigenvalueSet(np.array([2 + 1j, 4]))
    eig2 = EigenvalueSet(np.array([2, 1 + 2j]))
    pf1 = gen_zero_participation_factors(2)
    pf2 = gen_zero_participation_factors(2)

    want = {1: 2, 2: 1}
    got = EigenvalueTracker(eig1, eig2, pf1, pf2).calculate_index_map()

    assert want == got


# --------------------------------------------------------------------------- #
# ModalAnalysisResults
# --------------------------------------------------------------------------- #


def _make_results(eigenvalues, participation, states=("position", "speed")) -> ModalAnalysisResults:
    n = len(eigenvalues)
    return ModalAnalysisResults(
        sys_matrix=np.eye(n),
        eigenvalues=EigenvalueSet(np.array(eigenvalues)),
        participation_factors=ParticipationFactorSet(
            np.array(participation), states=np.array(states)
        ),
    )


results1 = _make_results([1, 1], [[0.99, 0.5], [0.01, 0.5]])
results2 = _make_results(
    [1, 1, -1],
    [[0.5, 0.3, 0.2], [0.3, 0.6, 0.1], [1, 0, 0]],
    states=("position", "speed", "acceleration"),
)
results3 = _make_results(
    [complex(-0.5, 7), complex(-0.5, -7), -1],
    [[0.5, 0.3, 0.2], [0.3, 0.6, 0.1], [1, 0, 0]],
    states=("position", "speed", "acceleration"),
)
results4 = _make_results(
    [-1.1, complex(-0.51, 7.2), complex(-0.51, -7.2)],
    [[0.5, 0.3, 0.2], [0.3, 0.6, 0.1], [1, 0, 0]],
    states=("position", "speed", "acceleration"),
)


def test_ModalAnalysisResults_eigenvalues_match():
    df = results1.get_dataframe()
    assert df.loc[df.index[0], REAL_COL] == 1
    assert df.loc[df.index[0], IMAG_COL] == 0


def test_ModalAnalysisResults_damped_and_undamped_frequency_are_zero_for_real_mode():
    df = results1.get_dataframe()
    assert df.loc[df.index[0], DAMPED_FREQ_COL] == 0
    assert df.loc[df.index[0], UNDAMPED_FREQ_COL] == 0


def test_ModalAnalysisResults_real_mode_string():
    df = results1.get_dataframe()
    assert df.loc[df.index[0], MODE_COL] == "1.0000"


def test_ModalAnalysisResults_complex_mode_string():
    df = results3.get_dataframe()
    assert df.loc[df.index[0], MODE_COL] == "-0.5000 ± 7.0000j"
    assert df.loc[df.index[2], MODE_COL] == "-1.0000"


def test_ModalAnalysisResults_dominant_states():
    df = results1.get_dataframe()
    assert df.loc[df.index[0], DOMINANT_STATES_COL] == "position"
    assert df.loc[df.index[1], DOMINANT_STATES_COL] == "position,speed"


def test_ModalAnalysisResults_filter_by_one_index():
    df = results1.filter_by_index(1).get_dataframe()
    assert len(df) == 1
    assert df.loc[1, REAL_COL] == 1


def test_ModalAnalysisResults_filter_by_multiple_indexes():
    filtered = results2.filter_by_index([1, 3])
    df_eig = filtered.get_dataframe()
    df_part = filtered.get_participation_dataframe()

    assert len(df_eig) == 2
    assert df_eig.loc[3, REAL_COL] == -1
    assert len(df_part.columns) == 2
    assert len(df_part.index) == 3


def test_ModalAnalysisResults_filter_by_damping_ratio():
    filtered = results3.filter_by_damping_ratio(0.5)
    assert len(filtered.get_dataframe()) == 2


def test_ModalAnalysisResults_filter_out_real_modes():
    filtered = results3.filter_out_real_modes()
    df = filtered.get_dataframe()
    assert len(df) == 2
    assert set(df[REAL_COL]) == {-0.5}


def test_ModalAnalysisResults_filter_out_conjugates():
    filtered = results3.filter_out_conjugates()
    assert len(filtered.get_dataframe()) == 2


def test_ModalAnalysisResults_filter_by_state():
    df = results1.filter_by_state("position").get_participation_dataframe()
    assert df.index.to_list() == ["position"]


def test_ModalAnalysisResults_filter_by_min_state_participation():
    df = (
        results1.filter_by_index(1)
        .filter_by_min_state_participation(0.1)
        .get_participation_dataframe()
    )
    assert df.index.to_list() == ["position"]


def test_ModalAnalysisResults_show_participation_does_not_mutate():
    want = results3.get_participation_dataframe().copy()
    results3.show_participation()
    got = results3.get_participation_dataframe()

    assert want.equals(got)


def test_ModalAnalysisResults_tracks_eigenvalues():
    tracked = results4.track_eigenvalues_from(results3)
    df = tracked.get_dataframe()
    pf = tracked.get_participation_dataframe()

    # before: [-1.1, -0.51+7.2j, -0.51-7.2j] -> after: [-0.51+7.2j, -0.51-7.2j, -1.1]
    assert df.index.to_list() == [1, 2, 3]
    assert df.loc[1, REAL_COL] == pytest.approx(-0.51)
    assert df.loc[1, IMAG_COL] == pytest.approx(7.2)
    assert df.loc[3, REAL_COL] == pytest.approx(-1.1)
    assert df.loc[3, IMAG_COL] == pytest.approx(0)

    assert pf.iloc[0, 0] == pytest.approx(0.3)
    assert pf.iloc[2, 2] == pytest.approx(1)


def test_track_eigenvalues_tracks_each_run_against_the_previous():
    eig1 = EigenvalueSet(np.array([-1, -2]))
    eig2 = EigenvalueSet(np.array([-1.5, -1.5]))
    eig3 = EigenvalueSet(np.array([-2, -1]))
    pf = gen_zero_participation_factors(2)

    r1 = ModalAnalysisResults(np.eye(2), eig1, pf)
    r2 = ModalAnalysisResults(np.eye(2), eig2, pf)
    r3 = ModalAnalysisResults(np.eye(2), eig3, pf)

    tracked = track_eigenvalues([r1, r2, r3])

    assert tracked[0].get_eigenvalues().get_vector() == pytest.approx([-1, -2])
    assert tracked[1].get_eigenvalues().get_vector() == pytest.approx([-1.5, -1.5])
    # if eig3 were tracked against eig1 (instead of eig2) it would be reordered;
    # tracked against eig2 it is not, since -1.5 is equidistant from -1 and -2.
    assert tracked[2].get_eigenvalues().get_vector() == pytest.approx([-2, -1])


# --------------------------------------------------------------------------- #
# EigenvalueSweepResults
# --------------------------------------------------------------------------- #


def test_EigenvalueSweepResults_when_and_when_index():
    sweep = EigenvalueSweepResults([1, 2, 3], [results1, results2, results3])

    assert sweep.when(2) is results2
    assert sweep.when_index(0) is results1
    assert len(sweep) == 3


def test_EigenvalueSweepResults_when_missing_value_raises():
    sweep = EigenvalueSweepResults([1, 2], [results1, results2])
    with pytest.raises(KeyError):
        sweep.when(99)


def test_EigenvalueSweepResults_length_mismatch_raises():
    with pytest.raises(PFEigenvalueMismatchError):
        EigenvalueSweepResults([1, 2, 3], [results1, results2])


def test_EigenvalueSweepResults_track_eigenvalues():
    eig1 = EigenvalueSet(np.array([-1, -2 + 1j, -2 - 1j]))
    eig2 = EigenvalueSet(np.array([-2 + 1j, -2 - 1j, -1]))
    pf = gen_zero_participation_factors(3)

    sweep = EigenvalueSweepResults(
        [0, 1],
        [
            ModalAnalysisResults(np.eye(3), eig1, pf),
            ModalAnalysisResults(np.eye(3), eig2, pf),
        ],
    ).track_eigenvalues()

    assert sweep.when_index(1).get_eigenvalues().get_vector() == pytest.approx(
        [-1, -2 + 1j, -2 - 1j]
    )


# --------------------------------------------------------------------------- #
# Sensitivity / ParametricSensitivity
# --------------------------------------------------------------------------- #


def test_sensitivity_between_tracks_and_subtracts():
    before = _make_results([-1, -2 + 1j, -2 - 1j], np.zeros((3, 3)), states=("a", "b", "c"))
    after = _make_results([-2 + 1j, -2 - 1j, -1.5], np.zeros((3, 3)), states=("a", "b", "c"))

    s = sensitivity_between(before, after)
    df = s.get_dataframe()

    assert df.loc[1, REAL_COL] == pytest.approx(-0.5)  # -1.5 - (-1)
    assert df.loc[1, IMAG_COL] == pytest.approx(0)


def test_Sensitivity_rejects_mismatched_indexes():
    eig_before = EigenvalueSet(np.array([1, 2]), indexes=[1, 2])
    eig_after = EigenvalueSet(np.array([1, 2]), indexes=[1, 3])

    with pytest.raises(PFEigenvalueMismatchError):
        Sensitivity(eig_before, eig_after)


def test_Sensitivity_filter_by_metrics():
    eig_before = EigenvalueSet(np.array([1, 2]))
    eig_after = EigenvalueSet(np.array([2, 4]))

    s = Sensitivity(eig_before, eig_after).filter_by_metrics(REAL_COL)
    df = s.get_dataframe()

    assert df.columns.to_list() == [REAL_COL]
    assert df.loc[1, REAL_COL] == 1
    assert df.loc[2, REAL_COL] == 2


def test_ParametricSensitivity_combines_several_conditions():
    s_a = Sensitivity(EigenvalueSet(np.array([1, 2])), EigenvalueSet(np.array([2, 4])))
    s_b = Sensitivity(EigenvalueSet(np.array([1, 2])), EigenvalueSet(np.array([1.5, 3])))

    ps = ParametricSensitivity(["cond_a", "cond_b"], [s_a, s_b])
    df = ps.get_dataframe()

    assert df[("cond_a", REAL_COL)].tolist() == [1, 2]
    assert df[("cond_b", REAL_COL)].tolist() == [0.5, 1]


def test_Sensitivity_filter_out_real_modes_handles_mode_crossing_real_complex():
    # index 2 is real in 'before' but complex in 'after' (a mode can cross
    # from real to complex as a swept parameter changes) - filtering
    # eig_before/eig_after independently would then disagree on which
    # indexes remain, breaking Sensitivity's index-match invariant.
    eig_before = EigenvalueSet(np.array([-1, -2, -3 + 4j]), indexes=[1, 2, 3])
    eig_after = EigenvalueSet(np.array([-1, -2 + 3j, -3 + 5j]), indexes=[1, 2, 3])

    s = Sensitivity(eig_before, eig_after).filter_out_real_modes()
    # index 1: real in both -> excluded. index 2: real before/complex after
    # -> excluded (ambiguous whether it's "the same" oscillatory mode).
    # index 3: complex in both -> kept.
    assert s.get_dataframe().index.to_list() == [3]


def test_ParametricSensitivity_length_mismatch_raises():
    s_a = Sensitivity(EigenvalueSet(np.array([1])), EigenvalueSet(np.array([2])))
    with pytest.raises(PFEigenvalueMismatchError):
        ParametricSensitivity(["a", "b"], [s_a])


# --------------------------------------------------------------------------- #
# eigenvalue_sensitivity / system_matrix_sensitivity
#
# A(p) = [[-1, 1], [p, -2]] has characteristic polynomial
# lambda^2 + 3*lambda + (2 - p) = 0, so
# lambda(p) = (-3 +/- sqrt(1 + 4*p)) / 2. At p=0: lambda = -1, -2, with
# d(lambda)/dp = +1 (for -1) and -1 (for -2) - worked out by hand and used
# here as a known-correct reference for both sensitivity approaches.
# --------------------------------------------------------------------------- #


def _state_matrix(p: float) -> np.ndarray:
    return np.array([[-1.0, 1.0], [p, -2.0]], dtype=complex)


def _modal_results_for(p: float) -> ModalAnalysisResults:
    A = _state_matrix(p)
    w, vl, vr = eig(A, left=True, right=True)
    participation = np.abs(vl) * np.abs(vr)
    participation = participation / participation.sum(axis=0, keepdims=True)
    states = np.array(["x1", "x2"])
    indexes = [1, 2]
    return ModalAnalysisResults(
        A,
        EigenvalueSet(w, indexes),
        ParticipationFactorSet(participation, states, indexes),
        right_eigenvectors=pd.DataFrame(vr, index=states, columns=indexes),
        left_eigenvectors=pd.DataFrame(vl, index=states, columns=indexes),
    )


def _index_closest_to(results: ModalAnalysisResults, value: float) -> int:
    df = results.get_dataframe()
    return df[REAL_COL].sub(value).abs().idxmin()


def test_eigenvalue_sensitivity_matches_hand_derived_analytical_value():
    before = _modal_results_for(0.0)
    delta = 1e-6
    delta_A = system_matrix_sensitivity(before, _modal_results_for(delta), delta)

    idx_minus1 = _index_closest_to(before, -1.0)
    idx_minus2 = _index_closest_to(before, -2.0)

    assert before.eigenvalue_sensitivity(idx_minus1, delta_A).real == pytest.approx(
        1.0, abs=1e-4
    )
    assert before.eigenvalue_sensitivity(idx_minus2, delta_A).real == pytest.approx(
        -1.0, abs=1e-4
    )


def test_eigenvalue_sensitivity_matches_finite_difference_on_eigenvalues():
    # validates the eigenvector-weighted (analytical) approach against
    # sensitivity_between's finite-difference-on-eigenvalues approach - the
    # two are independent implementations of the same derivative and should
    # agree for a small enough step.
    before = _modal_results_for(0.0)
    delta = 1e-6
    after = _modal_results_for(delta)
    delta_A = system_matrix_sensitivity(before, after, delta)

    fd = sensitivity_between(before, after).get_dataframe() / delta

    for value in (-1.0, -2.0):
        idx = _index_closest_to(before, value)
        analytical = before.eigenvalue_sensitivity(idx, delta_A)
        assert analytical.real == pytest.approx(fd.loc[idx, REAL_COL], abs=1e-3)
        assert analytical.imag == pytest.approx(fd.loc[idx, IMAG_COL], abs=1e-3)


def test_eigenvalue_sensitivity_without_eigenvectors_raises():
    results = ModalAnalysisResults(
        _state_matrix(0.0),
        EigenvalueSet(np.array([-1.0, -2.0])),
        ParticipationFactorSet(np.zeros((2, 2)), np.array(["x1", "x2"])),
    )
    with pytest.raises(PFAttributeNotSetError):
        results.eigenvalue_sensitivity(1, np.zeros((2, 2), dtype=complex))


def test_filter_by_index_slices_eigenvectors_to_match():
    results = _modal_results_for(0.0)
    idx = _index_closest_to(results, -1.0)

    filtered = results.filter_by_index(idx)

    assert filtered.get_right_eigenvectors().columns.to_list() == [idx]
    assert filtered.get_left_eigenvectors().columns.to_list() == [idx]
    # slicing must not change the eigenvector's own values
    pd.testing.assert_series_equal(
        filtered.get_right_eigenvectors()[idx], results.get_right_eigenvectors()[idx]
    )


def test_track_eigenvalues_from_remaps_eigenvector_columns():
    eig1 = EigenvalueSet(np.array([-1, -2 + 1j, -2 - 1j]))
    eig2 = EigenvalueSet(np.array([-2 + 1j, -2 - 1j, -1]))
    pf1 = gen_zero_participation_factors(3)
    pf2 = gen_zero_participation_factors(3)
    vec1 = pd.DataFrame(np.eye(3, dtype=complex), columns=[1, 2, 3])
    vec2 = pd.DataFrame(np.eye(3, dtype=complex) * 2, columns=[1, 2, 3])

    before = ModalAnalysisResults(
        np.eye(3), eig1, pf1, right_eigenvectors=vec1, left_eigenvectors=vec1
    )
    after = ModalAnalysisResults(
        np.eye(3), eig2, pf2, right_eigenvectors=vec2, left_eigenvectors=vec2
    )

    tracked = after.track_eigenvalues_from(before)

    # eig2's index 1 (-2+1j) is tracked to index 2 (see test_EigenvalueTracker);
    # its eigenvector column (originally column 1 of vec2) must move with it.
    assert tracked.get_right_eigenvectors()[2].to_numpy() == pytest.approx(
        vec2[1].to_numpy()
    )


if __name__ == "__main__":
    pytest.main([__file__])
