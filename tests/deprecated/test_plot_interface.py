import pytest
import sys

sys.path.insert(0, r".\src")
import powfacpy
import importlib

importlib.reload(powfacpy)
from matplotlib import pyplot
from os import getcwd
import os

from test_active_project_interface import pfp


@pytest.fixture
def pfplot(pf_app):
    # Return PFPlotInterface instance and show app
    pfplot = powfacpy.PFPlotInterface(pf_app)

    return pfplot


@pytest.fixture(autouse=True)
def run_around_tests(pfplot):
    # Code run before each test:
    # PF app needs to be shown for some reason, because otherwise
    # PF can error when plotting.
    pfplot.app.Show()
    # Run test
    yield  # gives control back to the 'context manager', i. e. the function that called this fixture.
    # Code that will run after each test:
    # Make sure that app is hidden for other modules than plot interface
    pfplot.app.Hide()


def test_plot(pfplot, activate_powfacpy_test_project):
    pfsim = powfacpy.PFDynSimInterface(pfplot.app)
    pfsim.activate_study_case(r"Study Cases\test_plot_interface\Study Case 1")
    pfsim.initialize_and_run_sim()

    with pytest.raises(powfacpy.exceptions.PFAttributeNotSetError):
        pfplot.plot(
            r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
            ["s:u0", "m:Qsum:bus1"],
        )

    pfplot.clear_plot_pages()
    pfplot.set_active_plot("test_plot 1", "test_plot_interface 1")
    pfplot.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        ["s:u0", "m:Qsum:bus1"],
    )

    pfplot.set_active_plot("test_plot 2", "test_plot_interface 1")
    pfplot.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "s:u0",
        linestyle=2,
        linewidth=100,
        color=3,
        label="u0 test",
        result_obj=r"Study Cases\test_plot_interface\Study Case 1\All calculations",
    )
    pfplot.set_x_axis_attributes(axisMode=2)
    pfplot.set_y_axis_attributes(scaleType=1)


def test_pyplot_from_csv(pfplot, activate_powfacpy_test_project):
    export_dir = os.getcwd() + r"\tests\tests_output"
    file_name = "results"
    pfsim = powfacpy.PFDynSimInterface(pfplot.app)
    pfsim.activate_study_case(r"Study Cases\test_plot_interface\Study Case 1")
    pfsim.initialize_and_run_sim()
    pfri = powfacpy.PFResultsInterface(pfplot.app)
    pfri.export_to_csv(export_dir, file_name=file_name)

    pyplot.figure()
    powfacpy.PFPlotInterface.plot_from_csv(
        export_dir + "\\" + file_name + ".csv",
        [
            r"test_plot_interface\Grid 1\AC Voltage Source\s:u0",
            r"test_plot_interface\Grid 1\AC Voltage Source\m:Qsum:bus1",
        ],
    )
    pyplot.xlabel("t [s]")


def test_copy_graphics_board_content(pfplot, activate_powfacpy_test_project):
    source_study_case = r"Study Cases\test_plot_interface\Study Case 1"
    target_study_cases = [
        r"Study Cases\test_plot_interface\Study Case 2",
        r"Study Cases\test_plot_interface\Study Case 3",
    ]
    pfplot.copy_graphics_board_content(
        source_study_case,
        target_study_cases,
        obj_to_copy="*.GrpPage",
        clear_target_graphics_board=True,
    )

    pfplot.copy_graphics_board_content(
        source_study_case,
        r"Study Cases\test_plot_interface\Study Case 2",
        obj_to_copy="*.GrpPage",
        clear_target_graphics_board=True,
    )


def test_copy_graphics_board_content_to_all_study_cases(
    pfplot, activate_powfacpy_test_project
):
    source_study_case = r"Study Cases\test_plot_interface\Study Case 1"
    pfplot.copy_graphics_board_content_to_all_study_cases(
        source_study_case, target_parent_folder=r"Study Cases\test_plot_interface"
    )


def test_plot_from_comtrade(pfplot, activate_powfacpy_test_project):
    path_of_cfg = os.path.dirname(__file__) + r"\tests_input\test_comtrade.cfg"
    pfplot.set_active_plot("test_plot 1", "test_plot_interface 1")
    pfplot.plot_from_comtrade(
        path_of_cfg,
        "AC Voltage Source:m:u:bus1:A",
        linestyle=2,
        linewidth=100,
        color=3,
        label="comtrade test",
    )


def test_activate_plot(pfplot, activate_powfacpy_test_project):
    with pytest.raises(powfacpy.exceptions.PFAttributeNotSetError):
        pfplot.set_active_plot("test_plot 1")


def test_clear_curves_by_index_from_active_plot(pfplot, activate_powfacpy_test_project):
    pfplot.get_unique_obj(
        r"Study Cases\test_plot_interface\Study Case 1", include_subfolders=False
    ).Activate()
    pfplot.set_active_plot("test clear curves", "test clear curves")

    # Plot and simulate
    pfplot.clear_curves()
    pfplot.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "m:Psum:bus1",
    )
    pfplot.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "m:Qsum:bus1",
    )
    pfplot.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "s:u0",
    )
    pfdi = powfacpy.PFDynSimInterface(pfplot.app)
    pfdi.initialize_and_run_sim()
    # Clear the last curve
    pfplot.clear_curves_by_index_from_active_plot(slice(-1, 1, -1))
    attributes = pfplot.get_curve_table_attributes()
    assert len(attributes["curveTableResultFile"]) == 2
    assert attributes["curveTableVariable"][0] == "m:Psum:bus1"

    # Plot again
    pfplot.clear_curves()
    pfplot.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "m:Psum:bus1",
    )
    pfplot.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "m:Qsum:bus1",
    )
    pfplot.plot(
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",
        "s:u0",
    )
    # Clear the first curve
    pfplot.clear_curves_by_index_from_active_plot(0)
    attributes = pfplot.get_curve_table_attributes()
    assert len(attributes["curveTableResultFile"]) == 2
    assert attributes["curveTableVariable"][0] == "m:Qsum:bus1"


if __name__ == "__main__":
    pytest.main(([r"tests\test_plot_interface.py"]))
    # pytest.main(([r"tests\test_plot_interface.py::test_plot"]))
