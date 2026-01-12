"Interface to pandas package."

import pandas as pd
import numpy as np
from pandas.api.types import is_complex_dtype
from icecream import ic

from powfacpy.pf_classes.protocols import PFApp
from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_classes.protocols import (
    PFApp,
)


class PandasInterface(ApplicationBase):

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)

    def replace_loc_name_with_pf_objects_in_labels(
        self,
        df: pd.DataFrame,
        class_name: str,
        only_calc_relevant: bool = True,
        index_and_column_labels_are_equal: bool = False,
        level: int = 0,
    ) -> pd.DataFrame:
        """Replaces string labels ('loc_name' of PF objects) of a dataframe with the corresponding PF objects.

        It is assumed that all PF objects are of the same class.

        Args:
            df (pd.DataFrame): index and column labels are 'loc_name' attributes of PF objects

            class_name (str): PF class name of the labels (e.g. 'ElmTerm'). Note that all PF objects must be of the same class.

            only_calc_relevant (bool): Search only for calculation relevant objects (using 'GetCalcRelevantObjects'). If False, search all objects (using 'get_obj') Defaults to True.

            index_and_column_labels_are_equal (bool, optional): If True, it is assumed that indices and columns have the same labels (improved performance). This is common for symmetric matrices. Defaults to False.

            level (int, optional): If labels are MultiIndex, the level that is replaced can be specified. Defaults to 0.

        Returns:
            pd.DataFrame: Frame with updated labels
        """
        if only_calc_relevant:
            all_objs = [
                self.app.GetCalcRelevantObjects(obj + ".ElmTerm")[0]
                for obj in df.columns.get_level_values(0)
            ]
        else:
            all_objs = [
                self.act_prj.get_unique_obj(obj + ".ElmTerm", include_subfolders=True)
                for obj in df.columns.get_level_values(0)
            ]
        df.columns = all_objs
        if not index_and_column_labels_are_equal:
            if only_calc_relevant:
                all_objs = [
                    self.app.GetCalcRelevantObjects(obj + ".ElmTerm")[0]
                    for obj in df.index.get_level_values(0)
                ]
            else:
                all_objs = [
                    self.act_prj.get_unique_obj(
                        obj + ".ElmTerm", include_subfolders=True
                    )
                    for obj in df.index.get_level_values(0)
                ]
        df.index = all_objs
        return df

    @staticmethod
    def separate_complex_columns_into_real_and_imaginary(
        df: pd.DataFrame, real_suffix: str = "_real", imag_suffix: str = "_imag"
    ) -> pd.DataFrame:
        """Separates complex columns into real and imaginary parts.

        Args:
            df (pd.DataFrame): DataFrame with complex columns.
            real_suffix (str, optional): Suffix for real part columns (added to original column label). Defaults to "_real".
            imag_suffix (str, optional): Suffix for imaginary part columns. Defaults to "_imag".
        """
        for col in df.columns:
            if is_complex_dtype(df[col]):
                df[col + real_suffix] = np.real(df[col])
                df[col + imag_suffix] = np.imag(df[col])
                del df[col]
        return df
