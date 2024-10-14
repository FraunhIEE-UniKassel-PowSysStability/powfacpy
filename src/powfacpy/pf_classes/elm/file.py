from __future__ import annotations

import os
from os import replace

import pandas as pd
import numpy as np
from icecream import ic

from powfacpy.pf_classes.protocols import ElmFile
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.base.active_project import ActiveProjectCached


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

    @staticmethod
    def replace_headers_of_csv_file_with_number_of_colums(file_path: str) -> int:
        """Replaces the first row (headers) of a csv file with its number of
        columns. This is needed for import of csv files to PF using ElmFile.
        """
        with (
            open(file_path + ".csv") as read_file,
            open(file_path + ".temp", "w") as write_file,
        ):
            columns_of_first_row = read_file.readline().split(",")
            if columns_of_first_row[-1] == "\n":
                columns_of_first_row = columns_of_first_row[:-1]
            # Minus one because first column is time and should not be counted.
            number_of_columns = len(columns_of_first_row) - 1
            write_file.write(str(number_of_columns) + "\n")
            row = read_file.readline()
            while row:
                write_file.write(row)
                row = read_file.readline()
        replace(file_path + ".temp", file_path + ".csv")
        return number_of_columns

    @staticmethod
    def insert_row_with_number_of_columns_in_csv_file(file_path: str) -> int:
        """Gets the number of columns of the first row in a csv file and
        inserts a row (first row) with this number in the first column.
        This is needed for ElmFile to read csv files.
        """
        with (
            open(file_path + ".csv") as read_file,
            open(file_path + ".temp", "w") as write_file,
        ):
            first_row = read_file.readline()
            columns_of_first_row = first_row.split(",")
            if columns_of_first_row[-1] == "\n":
                columns_of_first_row = columns_of_first_row[:-1]
            # Minus one because first column is time and should not be counted.
            number_of_columns = len(columns_of_first_row) - 1
            write_file.write(str(number_of_columns) + "\n")
            write_file.write(first_row)
            row = read_file.readline()
            while row:
                write_file.write(row)
                row = read_file.readline()
        replace(file_path + ".temp", file_path + ".csv")
        return number_of_columns
