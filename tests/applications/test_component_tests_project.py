"""Smoke test for the component_tests seed project (the SMIB test bench used by
the dynamic model validation tutorial).

Its purpose is twofold: verify the project imports/activates cleanly, and make
the test suite create ``component_tests_copy_to_run_tests`` so the
tutorial and any component-test work run against a clean copy.
"""

import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.base.active_project import ActiveProject

DUT_COMPOSITE_MODEL_PATH = (
    r"Network Model\Network Data\Grid\WECC WT Control System Type 4B"
)


def test_component_tests_copy_activates_with_expected_structure(
    pf_app, activate_component_tests_test_project
):
    """The copy activates and still contains the DUT and voltage-source
    composite models the dynamic-model-validation tutorial expects."""
    act_prj = ActiveProject(pf_app)
    assert (
        act_prj.app.GetActiveProject().loc_name
        == "component_tests_copy_to_run_tests"
    )

    dut = act_prj.get_unique_obj(DUT_COMPOSITE_MODEL_PATH)
    assert dut.GetClassName() == "ElmComp"

    voltage_source_ctrl = act_prj.get_unique_obj(
        r"Network Model\Network Data\Grid\Voltage source ctrl"
    )
    assert voltage_source_ctrl.GetClassName() == "ElmComp"


if __name__ == "__main__":
    pytest.main([__file__])
