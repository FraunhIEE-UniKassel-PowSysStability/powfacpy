import sys

import pytest
import numpy as np
import pandas as pd

sys.path.insert(0, r".\src")
from powfacpy.pf_classes.elm.file import MeasurementFile
from powfacpy.applications.active_project import ActiveProject


@pytest.fixture(scope="module")
def create_measurement_file(
    act_prj: ActiveProject, activate_test_project
) -> MeasurementFile:
    elmfile = act_prj.create_in_folder(
        "Measurement file.ElmFile",
        folder=r"Network Model\Network Data\test_dyn_sim_interface\TestElmFile\Composite Model",
    )
    return MeasurementFile(elmfile)


def test_get_full_path_of_elmfile_data():
    MeasurementFile.get_full_path_of_elmfile_data_in_external_data_directory()
    MeasurementFile.get_path_of_elmfile_data_inside_external_data_directory()


def test_from_pandas_dataframe(create_measurement_file):
    meas_file = create_measurement_file
    df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6]]), index=[0, 1])
    meas_file.from_pandas_dataframe(df, "test")


if __name__ == "__main__":
    pytest.main([r"tests\pf_classes\elm\test_file.py"])
