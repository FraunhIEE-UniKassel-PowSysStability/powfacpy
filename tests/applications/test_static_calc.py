"""Tests for powfacpy.applications.static_calc (StaticCalc).

Runs against the 39-bus New England project.
"""

import numpy as np
import pandas as pd
import pytest

from powfacpy.applications.static_calc import StaticCalc
from powfacpy.exceptions import PFInvalidLoadFlow


@pytest.fixture(scope="module")
def static_calc(pf_app, copy_39_bus_new_england_test_project) -> StaticCalc:
    copy_39_bus_new_england_test_project.Activate()
    return StaticCalc(pf_app)


@pytest.fixture
def valid_load_flow(static_calc: StaticCalc):
    assert static_calc.execute_load_flow() == 0
    return static_calc


def test_execute_load_flow_and_validity(static_calc: StaticCalc):
    assert static_calc.execute_load_flow() == 0
    assert static_calc.has_valid_load_flow_results()
    assert static_calc.check_load_flow_results() is True


def _invalidate_load_flow(static_calc: StaticCalc):
    """Changing a network parameter makes existing load flow results invalid."""
    load = static_calc.app.GetCalcRelevantObjects("*.ElmLod")[0]
    load.plini = load.plini + 1.0
    assert not static_calc.has_valid_load_flow_results()


def test_check_load_flow_results_when_invalid(valid_load_flow: StaticCalc):
    _invalidate_load_flow(valid_load_flow)
    with pytest.raises(PFInvalidLoadFlow):
        valid_load_flow.check_load_flow_results("error")
    with pytest.warns(UserWarning):
        assert valid_load_flow.check_load_flow_results("warning") is False
    assert valid_load_flow.check_load_flow_results("execute") is True
    assert valid_load_flow.has_valid_load_flow_results()


def test_get_result_dataframe(valid_load_flow: StaticCalc):
    terminals = valid_load_flow.app.GetCalcRelevantObjects("*.ElmTerm")[:3]
    df = valid_load_flow.get_result_dataframe(terminals, ["m:u", "m:phiu"])
    assert list(df.columns) == ["m:u", "m:phiu"]
    assert list(df.index) == terminals
    assert df["m:u"].between(0.8, 1.2).all()  # per unit voltage magnitude
    assert not np.isnan(df.to_numpy()).any()


def test_get_result_dataframe_with_unknown_variable(valid_load_flow: StaticCalc):
    terminals = valid_load_flow.app.GetCalcRelevantObjects("*.ElmTerm")[:1]
    with pytest.raises(Exception, match="has not attribute"):
        valid_load_flow.get_result_dataframe(terminals, ["m:does_not_exist"])


def test_replace_obj_with_loc_name_and_add_variable_desc(valid_load_flow: StaticCalc):
    terminals = valid_load_flow.app.GetCalcRelevantObjects("*.ElmTerm")[:3]
    df = valid_load_flow.get_result_dataframe(terminals, ["m:u", "m:phiu"])
    result = valid_load_flow.replace_obj_with_loc_name_and_add_variable_desc(df)
    assert list(result.index) == [t.loc_name for t in terminals]
    assert isinstance(result.columns, pd.MultiIndex)
    assert [c[0] for c in result.columns] == ["m:u", "m:phiu"]
    assert all(isinstance(c[1], str) and c[1] for c in result.columns)
    assert np.allclose(result.to_numpy(), df.to_numpy())


def test_create_secondary_controller(valid_load_flow: StaticCalc):
    machines = valid_load_flow.app.GetCalcRelevantObjects("*.ElmSym")[:2]
    parent = valid_load_flow.act_prj.network_data_folder
    secctrl = valid_load_flow.create_secondary_controller(
        name="tc_secctrl",
        parent_folder=parent,
        controlled_objs=machines,
        attr={"outserv": 1},
    )
    try:
        assert secctrl.GetClassName() == "ElmSecctrl"
        assert secctrl.loc_name == "tc_secctrl"
        assert list(secctrl.psym) == machines
        assert secctrl.outserv == 1
    finally:
        secctrl.Delete()
