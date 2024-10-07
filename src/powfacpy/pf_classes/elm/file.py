from __future__ import annotations

import os

import pandas as pd
import numpy as np
from icecream import ic

from powfacpy.pf_classes.protocols import ElmFile
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.applications.active_project import ActiveProjectCached


class MeasurementFile(ElmBase):

    def __init__(self, obj: ElmFile) -> None:
        super().__init__(obj)
        self._obj: ElmFile

    def __new__(cls, *args, **kwargs) -> ElmFile | MeasurementFile:
        """Implemented only to add type hints for the created instance.

        Returns:
            ElmTerm | Terminal: New instance
        """
        instance = super().__new__(cls)
        return instance

    def from_pandas_dataframe(
        self,
        dataframe: pd.DataFrame,
        csv_file_name: str,
        csv_file_dir: str | None = None,
    ) -> str:
        """Read data from a pandas dataframe.

        A csv file is created from the dataframe and the measurement file reads from the csv file.

        Args:
            dataframe (pd.DataFrame): Data for measurement file. IMPORTANT: The index of the frame is the time.
            csv_file_name (str): Name of csv file (created using the dataframe) from which the measurement file reads.
            csv_file_dir (str | None, optional): directory where csv file is created. Defaults to None (external data directory of PF is used).

        Returns:
            str: Directory where csv file was created
        """
        act_prj = ActiveProjectCached()
        if not csv_file_dir:
            csv_file_dir_with_special_chars = (
                "$(ExtDataDir)\\"
                + self.get_path_of_elmfile_data_inside_external_data_directory()
            )
            csv_file_dir = act_prj._replace_special_PF_characters_in_path_string(
                csv_file_dir_with_special_chars
            )
            if not os.path.exists(csv_file_dir):
                os.makedirs(csv_file_dir)
        else:
            csv_file_dir_with_special_chars = csv_file_dir

        np_array = np.concatenate(
            [dataframe.index.to_numpy().reshape(-1, 1), dataframe.to_numpy()], axis=1
        )
        first_row = np.zeros((1, np_array.shape[1]))
        first_row[0, 0] = np_array.shape[1]
        np_array = np.concatenate([first_row, np_array])
        np.savetxt(
            csv_file_dir + "\\" + csv_file_name + ".csv", np_array, delimiter=","
        )

        self.f_name = csv_file_dir_with_special_chars + "\\" + csv_file_name + ".csv"
        return csv_file_dir

    @staticmethod
    def get_path_of_elmfile_data_inside_external_data_directory() -> str:
        """Path inside (i.e. relative to) external data directory of PF where Elmfile data are stored.

        Returns:
            str: path
        """
        return "ElmFiles"

    @staticmethod
    def get_full_path_of_elmfile_data_in_external_data_directory() -> str:
        """Get full path of directory where elmfile data are stored (in PF's exteral working directory)

        Returns:
            str: path
        """
        act_prj = ActiveProjectCached()
        ext_data_dir = act_prj.get_external_data_directory()
        return (
            ext_data_dir
            + "\\"
            + MeasurementFile.get_path_of_elmfile_data_inside_external_data_directory()
        )
