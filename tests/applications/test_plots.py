import sys
import os
from os import remove, getcwd

import pytest
from matplotlib import pyplot

import powfacpy.applications
import powfacpy.applications.dynamic_simulation

sys.path.insert(0, r".\src")
import powfacpy
from powfacpy.applications.plots import Plots
from powfacpy.applications.dynamic_simulation import DynamicSimulation
from powfacpy.applications.results import Results
from powfacpy.pf_classes.protocols import PFApp
import importlib

importlib.reload(powfacpy)


@pytest.fixture
def pfplt(pf_app: PFApp):
    # Return pfpltInterface instance and show app
    pfplt = Plots(pf_app)
    return pfplt


@pytest.fixture(autouse=True)
def run_around_tests(pfplt: Plots):
    # Code run before each test:
    # PF app needs to be shown, because otherwise PF can error when plotting for some reason.
    pfplt.act_prj.app.Show()
    # Run test
    yield  # gives control back to the 'context manager', i. e. the function that called this fixture.
    # Code that will run after each test: Make sure that app is hidden for other modules than plot interface
    pfplt.act_prj.app.Hide()


def test_plot(pfplt: Plots, activate_powfacpy_test_project):
    pfsim = DynamicSimulation(pfplt.act_prj.app)
    pfsim.act_prj.activate_study_case(r"Study Cases\test_plot_interface\Study Case 1")
    pfsim.initialize_and_run_sim()

    with pytest.raises(powfacpy.exceptions.PFAttributeNotSetError):
        pfplt.plot(
            r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
            ["s:u0", "m:Qsum:bus1"],
        )

    pfplt.clear_plot_pages()
    pfplt.set_active_plot("test_plot 1", "test_plot_interface 1")
    pfplt.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        ["s:u0", "m:Qsum:bus1"],
    )

    pfplt.set_active_plot("test_plot 2", "test_plot_interface 1")
    pfplt.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "s:u0",
        linestyle=2,
        linewidth=100,
        color=3,
        label="u0 test",
        result_obj=r"Study Cases\test_plot_interface\Study Case 1\All calculations",
    )
    pfplt.set_x_axis_attributes(axisMode=2)
    pfplt.set_y_axis_attributes(scaleType=1)


def test_pyplot_from_csv(pfplt: Plots, activate_powfacpy_test_project):
    export_dir = os.getcwd() + r"\tests\tests_output"
    file_name = "results"
    pfsim = DynamicSimulation(pfplt.act_prj.app)
    pfsim.act_prj.activate_study_case(r"Study Cases\test_plot_interface\Study Case 1")
    pfsim.initialize_and_run_sim()
    pfri = Results(pfplt.act_prj.app)
    pfri.export_to_csv(export_dir, file_name=file_name)

    pyplot.figure()
    pfplt.plot_from_csv(
        export_dir + "\\" + file_name + ".csv",
        [
            r"test_plot_interface\Grid 1\AC Voltage Source\s:u0",
            r"test_plot_interface\Grid 1\AC Voltage Source\m:Qsum:bus1",
        ],
    )
    pyplot.xlabel("t [s]")


def test_copy_graphics_board_content(pfplt: Plots, activate_powfacpy_test_project):
    source_study_case = r"Study Cases\test_plot_interface\Study Case 1"
    target_study_cases = [
        r"Study Cases\test_plot_interface\Study Case 2",
        r"Study Cases\test_plot_interface\Study Case 3",
    ]
    pfplt.copy_graphics_board_content(
        source_study_case,
        target_study_cases,
        obj_to_copy="*.GrpPage",
        clear_target_graphics_board=True,
    )

    pfplt.copy_graphics_board_content(
        source_study_case,
        r"Study Cases\test_plot_interface\Study Case 2",
        obj_to_copy="*.GrpPage",
        clear_target_graphics_board=True,
    )


def test_copy_graphics_board_content_to_all_study_cases(
    pfplt: Plots, activate_powfacpy_test_project
):
    source_study_case = r"Study Cases\test_plot_interface\Study Case 1"
    pfplt.copy_graphics_board_content_to_all_study_cases(
        source_study_case, target_parent_folder=r"Study Cases\test_plot_interface"
    )


def test_plot_from_comtrade(pfplt: Plots, activate_powfacpy_test_project):
    path_of_cfg = os.path.dirname(__file__) + r"\tests_input\test_comtrade.cfg"
    pfplt.set_active_plot("test_plot 1", "test_plot_interface 1")
    pfplt.plot_from_comtrade(
        path_of_cfg,
        "AC Voltage Source:m:u:bus1:A",
        linestyle=2,
        linewidth=100,
        color=3,
        label="comtrade test",
    )


def test_activate_plot(pfplt: Plots, activate_powfacpy_test_project):
    with pytest.raises(powfacpy.exceptions.PFAttributeNotSetError):
        pfplt.set_active_plot("test_plot 1")


def test_clear_curves_by_index_from_active_plot(
    pfplt: Plots, activate_powfacpy_test_project
):
    pfplt.act_prj.get_unique_obj(
        r"Study Cases\test_plot_interface\Study Case 1", include_subfolders=False
    ).Activate()
    pfplt.set_active_plot("test clear curves", "test clear curves")

    # Plot and simulate
    pfplt.clear_curves()
    pfplt.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "m:Psum:bus1",
    )
    pfplt.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "m:Qsum:bus1",
    )
    pfplt.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "s:u0",
    )
    pfdi = powfacpy.applications.dynamic_simulation.DynamicSimulation(pfplt.act_prj.app)
    pfdi.initialize_and_run_sim()
    # Clear the last curve
    pfplt.clear_curves_by_index_from_active_plot(slice(-1, 1, -1))
    attributes = pfplt.get_curve_table_attributes()
    assert len(attributes["curveTableResultFile"]) == 2
    assert attributes["curveTableVariable"][0] == "m:Psum:bus1"

    # Plot again
    pfplt.clear_curves()
    pfplt.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "m:Psum:bus1",
    )
    pfplt.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "m:Qsum:bus1",
    )
    pfplt.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "s:u0",
    )
    # Clear the first curve
    pfplt.clear_curves_by_index_from_active_plot(0)
    attributes = pfplt.get_curve_table_attributes()
    assert len(attributes["curveTableResultFile"]) == 2
    assert attributes["curveTableVariable"][0] == "m:Qsum:bus1"


if __name__ == "__main__":
    pytest.main(([r"tests\applications\test_plots.py"]))
    # pytest.main(([r"tests\test_plot_interface.py::test_plot"]))
