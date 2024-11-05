import sys

import pytest
import numpy as np
import pandas as pd

sys.path.insert(0, r".\src")
from powfacpy.pf_classes.elm.file import MeasurementFile
from powfacpy.base.active_project import ActiveProject
from powfacpy.pf_classes.protocols import IntPrj


@pytest.fixture(
    scope="function",
)
def create_measurement_file(
    act_prj,
) -> MeasurementFile:
    # activate_powfacpy_test_project.Activate()
    # act_prj = ActiveProject()
    # act_prj.app.ActivateProject(
    #     r"\seberlein\powfacpy\powfacpy_tests_copy_where_tests_run"
    # )
    print(f"############# {act_prj.app.GetActiveProject()}")
    elmfile = act_prj.create_in_folder(
        "Measurement file.ElmFile",
        folder=r"Network Model\Network Data\test_dyn_sim_interface\Grid 1\test_composite_model",
    )
    return MeasurementFile(elmfile)


def test_from_pandas_dataframe(
    activate_powfacpy_test_project,
    create_measurement_file: MeasurementFile,
):
    meas_file = create_measurement_file
    df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6]]), index=[0, 1])
    meas_file.from_pandas_dataframe(df, "test")


def test_get_full_path_of_elmfile_data(activate_powfacpy_test_project):
    MeasurementFile.get_full_path_of_elmfile_data_in_external_data_directory()
    MeasurementFile.get_path_of_elmfile_data_inside_external_data_directory()


if __name__ == "__main__":
    # pytest.main([r"tests\pf_classes\elm\test_file.py"])
    # pytest.main([r"tests\pf_classes"])
    # pytest.main([r"tests", r"--ignore=tests\deprecated"])
    pytest.main([r"tests"])
