"""Module with interface for static calculations (load flow, short circuits,..)"""

from warnings import warn
from os import getcwd, remove

import pandas as pd
import numpy as np
from icecream import ic


from powfacpy.applications.application_base import ApplicationBase
from powfacpy.applications.results import Results
from powfacpy.pf_classes.protocols import ElmSecctrl, PFGeneral, PFApp
from powfacpy.exceptions import PFInvalidLoadFlow


class StaticCalc(ApplicationBase):
    """Static calculation (e.g. load flow, short circuit,..) interface"""

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)

    def execute_load_flow(self, params: dict = {}) -> int:
        return self.act_prj.execute_load_flow(params=params)

    def has_valid_load_flow_results(self) -> bool:
        return self.act_prj.app.IsLdfValid() != 0

    def check_load_flow_results(self, when_invalid: str = "error") -> bool:
        """
        Check whether load flow results in PF are present and valid and raise exception, warning or execute load flow if not.

        Args:
            when_invalid (str, optional): If load flow results are invalid, 'error' (raises exception), 'warning' raises warning, 'execute' executes load flow and raises exception if results are invalid. Defaults to "error".

        Raises:
            PFInvalidLoadFlow: When load flow results are invalid and 'when_invalid'= 'error' or 'execute' and results are invalid.

        Returns:
            bool: True only when results are valid.
        """
        self.act_prj.check_load_flow_results(when_invalid)

    def create_secondary_controller(
        self,
        name: str | None = None,
        parent_folder: PFGeneral | None = None,
        controlled_objs: list[PFGeneral] | None = None,
        attr: dict | None = None,
    ) -> ElmSecctrl:
        """Create secondary controller (ElmSecctrl)

        Args:
            name (str | None, optional): Name of ElmSecctrl. Defaults to None.
            parent_folder (PFGeneral | None, optional): Parent folder. Defaults to None.
            controlled_objs (list[PFGeneral] | None, optional): Network elements that are controlled ('psym' attribute). Defaults to None.
            attr (dict | None, optional): Attributes (keys) and their values (values) of teh created ElmSecctrl to be set. Defaults to None.

        Returns:
            ElmSecctrl: _description_
        """
        secctrl: ElmSecctrl = self.act_prj.create_in_folder(
            name + ".ElmSecctrl", parent_folder
        )
        if controlled_objs is not None:
            secctrl.psym = controlled_objs
        if attr is not None:
            self.act_prj.set_attr(secctrl, attr)
        return secctrl

    def get_result_dataframe(
        self, objs: list[PFGeneral], resvars: list[str]
    ) -> pd.DataFrame:
        df = pd.DataFrame(index=objs)
        for var in resvars:
            col_vector = np.empty(len(objs))
            for n, obj in enumerate(objs):
                try:
                    col_vector[n] = obj.GetAttribute(var)
                except AttributeError:
                    raise Exception(
                        f"'{obj}' has not attribute '{var}'. Perhaps calculation results are not present or invalid?"
                    )
            df[var] = col_vector
        return df

    def replace_obj_with_loc_name_and_add_variable_desc(
        self, df: pd.DataFrame, simulation_type: str = "LF_Bal"
    ) -> pd.DataFrame:
        pfres = Results(self.act_prj.app)
        columns = pd.MultiIndex.from_tuples(
            [
                (
                    col,
                    pfres.get_result_variable_description(
                        df.index[0], col, simulation_type=simulation_type
                    ),
                )
                for col in df.columns
            ]
        )
        index = [obj.loc_name for obj in df.index]
        return pd.DataFrame(df.to_numpy(), columns=columns, index=index)
