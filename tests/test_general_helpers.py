"""Tests for powfacpy.general_helpers.

Pure Python - no PowerFactory dependency, no fixtures needed.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory

from powfacpy.general_helpers import get_indices


def test_get_indices_large_list_true():
    superset = ["a", "b", "c", "d", "e"]
    subset = ["c", "a", "e"]
    assert get_indices(subset, superset, large_list=True) == [2, 0, 4]


def test_get_indices_large_list_false():
    superset = ["a", "b", "c", "d", "e"]
    subset = ["c", "a", "e"]
    assert get_indices(subset, superset, large_list=False) == [2, 0, 4]


def test_get_indices_both_modes_agree():
    superset = list(range(20))
    subset = [15, 3, 7, 0]
    assert get_indices(subset, superset, large_list=True) == get_indices(
        subset, superset, large_list=False
    )


def test_get_indices_missing_item_raises():
    with pytest.raises((ValueError, KeyError)):
        get_indices(["x"], ["a", "b"], large_list=False)
    with pytest.raises((ValueError, KeyError)):
        get_indices(["x"], ["a", "b"], large_list=True)


if __name__ == "__main__":
    pytest.main([__file__])
