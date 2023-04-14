import pytest
import sys
sys.path.insert(0, r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)
from matplotlib import pyplot
from os import getcwd
import os

from test_base_interface import pfbi, pf_app, activate_test_project

@pytest.fixture
def pfplot(pf_app):
    # Return PFPlotInterface instance and show app
    pfplot = powfacpy.PFPlotInterface(pf_app)
    # PF app needs to be shown for some reason, because otherwise 
    # PF can error when plotting.
    pfplot.app.Show()
    return pfplot 

def test_plot(pfplot, activate_test_project):
    pfsim = powfacpy.PFDynSimInterface(pfplot.app)
    pfsim.activate_study_case(r"Study Cases\test_plot_interface\Study Case 1")
    pfsim.initialize_and_run_sim()

    with pytest.raises(powfacpy.PFAttributeNotSetError):
        pfplot.plot(r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",["s:u0","m:Qsum:bus1"])

    pfplot.clear_plot_pages()
    pfplot.set_active_plot("test_plot 1","test_plot_interface 1")
    pfplot.plot(r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source",["s:u0","m:Qsum:bus1"])

    pfplot.set_active_plot("test_plot 2","test_plot_interface 1")
    pfplot.plot(r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source","s:u0",
        linestyle=2, linewidth=100, color=3, label="u0 test",
        result_obj=r"Study Cases\test_plot_interface\Study Case 1\All calculations",
        )
    pfplot.set_x_axis_attributes(axisMode=2)
    pfplot.set_y_axis_attributes(scaleType=1)

def test_pyplot_from_csv(pfplot, activate_test_project):
    export_dir = os.path.dirname(__file__) + r"\tests_output"
    file_name = "results"
    pfsim = powfacpy.PFDynSimInterface(pfplot.app)
    pfsim.export_dir =  export_dir
    pfsim.activate_study_case(r"Study Cases\test_plot_interface\Study Case 1")
    pfsim.initialize_and_run_sim()
    pfsim.export_to_csv(file_name=file_name)

    pyplot.figure()
    powfacpy.PFPlotInterface.plot_from_csv(
        export_dir + "\\" + file_name + ".csv",
        [r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source\s:u0",
        r"Network Model\Network Data\test_plot_interface\Grid 1\AC Voltage Source\m:Qsum:bus1"]) 
    pyplot.xlabel("t [s]")

def test_copy_graphics_board_content(pfplot, activate_test_project):
    source_study_case = r"Study Cases\test_plot_interface\Study Case 1"
    target_study_cases = [r"Study Cases\test_plot_interface\Study Case 2", 
        r"Study Cases\test_plot_interface\Study Case 3"]
    pfplot.copy_graphics_board_content(source_study_case, target_study_cases,
        obj_to_copy="*.GrpPage", clear_target_graphics_board=True) 

    pfplot.copy_graphics_board_content(source_study_case, r"Study Cases\test_plot_interface\Study Case 2",
        obj_to_copy="*.GrpPage", clear_target_graphics_board=True)      

def test_copy_graphics_board_content_to_all_study_cases(pfplot, activate_test_project):
    source_study_case = r"Study Cases\test_plot_interface\Study Case 1"
    pfplot.copy_graphics_board_content_to_all_study_cases(source_study_case,
        target_parent_folder=r"Study Cases\test_plot_interface")

def test_plot_from_comtrade(pfplot, activate_test_project):
    path_of_cfg = os.path.dirname(__file__) + r"\tests_input\test_comtrade.cfg"
    pfplot.set_active_plot("test_plot 1","test_plot_interface 1")
    pfplot.plot_from_comtrade(path_of_cfg,
        "AC Voltage Source:m:u:bus1:A",
        linestyle=2, linewidth=100, color=3, label="comtrade test")

def test_activate_plot(pfplot, activate_test_project):
    with pytest.raises(powfacpy.PFAttributeNotSetError):
        pfplot.set_active_plot("test_plot 1")

if __name__ == "__main__":
    pytest.main(([r"tests\test_plot_interface.py"]))
    #pytest.main(([r"tests\test_plot_interface.py::test_plot"]))


