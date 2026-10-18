"""Tests for powfacpy.applications.pandas_interface.

The PowerFactory application and the active project are replaced by small fakes,
so no PowerFactory connection is required.
"""

import numpy as np
import pandas as pd
import pytest

from powfacpy.applications.pandas_interface import PandasInterface

pytestmark = pytest.mark.unit  # pure Python - runs without PowerFactory


class _FakeApp:
    def __init__(self):
        self.calc_relevant_queries = []

    def GetCalcRelevantObjects(self, name):
        self.calc_relevant_queries.append(name)
        return [f"pf_obj<{name}>"]


class _FakeActiveProject:
    app = _FakeApp()

    def __init__(self):
        self.unique_obj_queries = []

    def get_unique_obj(self, name, include_subfolders=False):
        self.unique_obj_queries.append((name, include_subfolders))
        return f"unique<{name}>"


@pytest.fixture
def interface():
    _FakeActiveProject.app = _FakeApp()
    pandas_interface = PandasInterface.__new__(PandasInterface)  # skip ActiveProject
    pandas_interface.act_prj = _FakeActiveProject()
    return pandas_interface


def _matrix():
    return pd.DataFrame(
        [[1, 2], [3, 4]], index=["T1", "T2"], columns=["T1", "T2"], dtype=float
    )


def test_separate_complex_columns_into_real_and_imaginary() -> None:
    df = pd.DataFrame({"v": [1 + 2j, 3 - 4j], "p": [1.0, 2.0]})
    result = PandasInterface.separate_complex_columns_into_real_and_imaginary(df)
    assert list(result.columns) == ["p", "v_real", "v_imag"]
    assert result["v_real"].tolist() == [1.0, 3.0]
    assert result["v_imag"].tolist() == [2.0, -4.0]
    assert result["p"].tolist() == [1.0, 2.0]


def test_separate_complex_columns_custom_suffixes() -> None:
    df = pd.DataFrame({"z": np.array([1j, 2 + 0j])})
    result = PandasInterface.separate_complex_columns_into_real_and_imaginary(
        df, real_suffix=".re", imag_suffix=".im"
    )
    assert list(result.columns) == ["z.re", "z.im"]


def test_separate_complex_columns_without_complex_data_is_a_no_op() -> None:
    df = pd.DataFrame({"a": [1, 2], "b": [0.5, 0.25]})
    result = PandasInterface.separate_complex_columns_into_real_and_imaginary(df)
    assert list(result.columns) == ["a", "b"]


def test_replace_labels_using_calc_relevant_objects(interface) -> None:
    df = interface.replace_loc_name_with_pf_objects_in_labels(_matrix(), "ElmTerm")
    assert list(df.columns) == ["pf_obj<T1.ElmTerm>", "pf_obj<T2.ElmTerm>"]
    assert list(df.index) == ["pf_obj<T1.ElmTerm>", "pf_obj<T2.ElmTerm>"]
    # columns and index are looked up separately
    assert len(interface.app.calc_relevant_queries) == 4


def test_replace_labels_equal_index_and_columns_looks_up_once(interface) -> None:
    df = interface.replace_loc_name_with_pf_objects_in_labels(
        _matrix(), "ElmTerm", index_and_column_labels_are_equal=True
    )
    assert list(df.index) == list(df.columns)
    assert len(interface.app.calc_relevant_queries) == 2


def test_replace_labels_searching_all_objects(interface) -> None:
    df = interface.replace_loc_name_with_pf_objects_in_labels(
        _matrix(), "ElmTerm", only_calc_relevant=False
    )
    assert list(df.columns) == ["unique<T1.ElmTerm>", "unique<T2.ElmTerm>"]
    assert interface.app.calc_relevant_queries == []
    assert all(sub for _, sub in interface.act_prj.unique_obj_queries)
