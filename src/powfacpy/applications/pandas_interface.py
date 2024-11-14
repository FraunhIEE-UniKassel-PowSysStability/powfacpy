"Interface to pandas package."

import pandas as pd

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
        separator = f".{class_name},"
        all_objs = separator.join(df.columns.get_level_values(level).to_list())
        if only_calc_relevant:
            all_objs = self.app.GetCalcRelevantObjects(all_objs)
        else:
            all_objs = self.act_prj.get_obj(all_objs, include_subfolders=True)
        df.columns = all_objs
        if not index_and_column_labels_are_equal:
            all_objs = separator.join(df.index.get_level_values(level).to_list())
            all_objs = self.app.GetCalcRelevantObjects(all_objs)
        df.index = all_objs
        return df
