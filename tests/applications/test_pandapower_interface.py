"""Tests for the pure-Python helpers in powfacpy.applications.pandapower_interface.

'rearrange_matrix_rows_and_cols' has no PowerFactory dependency; the class
'PandapowerInterface' itself needs a live pandapower/PowerFactory conversion
and is not covered here.
"""

import sys

import numpy as np
import pytest

sys.path.insert(0, r".\src")

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory

from powfacpy.applications.pandapower_interface import rearrange_matrix_rows_and_cols


def test_rearrange_matrix_rows_and_cols_identity_order():
    matrix = np.array([[1, 2], [3, 4]])
    result = rearrange_matrix_rows_and_cols(matrix, [0, 1])
    assert np.array_equal(result, matrix)


def test_rearrange_matrix_rows_and_cols_swaps_rows_and_cols_consistently():
    matrix = np.array(
        [
            [11, 12, 13],
            [21, 22, 23],
            [31, 32, 33],
        ]
    )
    # swap index 0 and 2
    result = rearrange_matrix_rows_and_cols(matrix, [2, 1, 0])
    expected = np.array(
        [
            [33, 32, 31],
            [23, 22, 21],
            [13, 12, 11],
        ]
    )
    assert np.array_equal(result, expected)


def test_rearrange_matrix_rows_and_cols_diagonal_preserved_under_permutation():
    # the diagonal entries follow their row/col to the same new position
    matrix = np.diag([1.0, 2.0, 3.0])
    result = rearrange_matrix_rows_and_cols(matrix, [2, 0, 1])
    assert np.array_equal(np.diag(result), [3.0, 1.0, 2.0])


if __name__ == "__main__":
    pytest.main([__file__])
