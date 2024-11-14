"""
Interface with pandapower.
Tutorial on internal data structure and matrices of pandapower: https://github.com/e2nIEE/pandapower/blob/develop/tutorials/internal_datastructure.ipynb
"""

from abc import abstractmethod
from typing import Callable

import pandapower as pp
from pandapower.converter.powerfactory.validate import validate_pf_conversion
import pandas as pd
import numpy as np
import copy
from icecream import ic

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_classes.protocols import (
    PFGeneral,
    PFApp,
)


class PandapowerInterface(ApplicationBase):

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)

    def pf_project_to_pandapower(
        self, project_path_in_user: str = None, json_path: str = None
    ) -> pp.auxiliary.pandapowerNet:
        """
        Convert PowerFactory network to pandapower format.

        see pandapower docs: https://pandapower.readthedocs.io//en//v2.13.1//converter//powerfactory.html

        The method 'from_pfd' that is used deactivates the currently active PF project, so it is reactivated.

        Arguments:
            project_path_in_user (str): path of the project in PowerFactory database relative to user

            json_path (str): path of exported pandapower json file

        Returns:
            pp.auxiliary.pandapowerNet: pandapower network
        """
        active_project = self.act_prj.app.GetActiveProject()
        if project_path_in_user is None:
            project_path_in_user = self.act_prj.get_path_of_object_in_current_user(
                active_project
            )
        net = pp.converter.powerfactory.from_pfd(
            self.app, prj_name=project_path_in_user, path_dst=json_path
        )
        if active_project:
            active_project.Activate()
        return net

    def get_Ybus_matrix(self, net: pp.pandapowerNet, return_deepcopy=True) -> np.matrix:
        """
        Get admittance matrix (sparse).

        If internal bus-branch model does not exist yet, a power flow must be executed.

        Arguments:
            net: pandapower network
            return_deepcopy: If True, a deepcopy of the matrix stored in 'net' is returned.

        Returns:
            np.matrix: admittance matrix
        """
        if not net._ppc or net._ppc["internal"]["Ybus"].size == 0:
            pp.runpp(net)
        if return_deepcopy:
            return copy.deepcopy(net._ppc["internal"]["Ybus"])
        else:
            return net._ppc["internal"]["Ybus"]

    def get_Ybus_frame(self, net: pp.pandapowerNet) -> pd.DataFrame:
        """Get Dataframe with admittance matrix and row (column) labels according to the 'loc_name' of the terminal objects.

        Args:
            net (pp.pandapowerNet): pandapower dataset (exported from PF)

        Returns:
            pd.DataFrame: admittance matrix
        """
        Yb = self.get_Ybus_matrix(net)
        matrix_index_labels = self.get_admittance_matrix_labels(net)
        return pd.DataFrame(
            Yb.todense(), columns=matrix_index_labels, index=matrix_index_labels
        )

    def get_imaginary_Ybus_matrix(
        self, net: pp.pandapowerNet, return_deepcopy=True
    ) -> np.matrix:
        """Get imaginary part of admittance matrix (sparse).

        Args:
            net (pp.pandapowerNet): pandapower dataset (exported from PF)
            return_deepcopy (bool, optional): _description_. Defaults to True.

        Returns:
            np.matrix: imaginary part of admittance matrix (sparse)
        """
        if return_deepcopy:
            return copy.deepcopy(np.imag(self.get_Ybus_matrix(net)))
        else:
            return np.imag(self.get_Ybus_matrix(net))

    def get_admittance_matrix_labels(self, net: pp.pandapowerNet):
        pd2ppc_lookups = net._pd2ppc_lookups["bus"]
        matrix_index_labels = [None] * net._ppc["internal"]["Ybus"].shape[0]
        for ybus_idx in range(len(matrix_index_labels)):
            bus_idx = np.argmax(net._pd2ppc_lookups["bus"] == ybus_idx)
            matrix_index_labels[ybus_idx] = net.bus.iloc[bus_idx, :]["name"]
        return matrix_index_labels

    def get_Bbus_matrix(self, net: pp.pandapowerNet, return_deepcopy=True) -> np.matrix:
        """
        Get Bbus matrix  (sparse) used for dc power flow.

        If internal bus-branch model for dc power flow does not exist yet, a dc power flow must be executed.

        Arguments:
        - net: pandapower network
        """
        if not net._ppc or not net._ppc["internal"]["Bbus"].size == 0:
            pp.rundcpp(net)
        if return_deepcopy:
            return copy.deepcopy(net._ppc["internal"]["Bbus"])
        else:
            return net._ppc["internal"]["Bbus"]

    def get_jacobian_matrix(
        self, net: pp.pandapowerNet, return_deepcopy=True
    ) -> np.matrix:
        """
        Get load flow jacobian matrix.

        Arguments:
        - net: pandapower network
        """
        if not net._ppc:
            pp.runpp(net)
        if return_deepcopy:
            return copy.deepcopy(net._ppc["internal"]["J"])
        else:
            return net._ppc["internal"]["J"]

    def get_connectivity_matrix(
        self, net: pp.pandapowerNet, boolean: bool = False
    ) -> np.array:
        """Get the connectivity (also called adjacency) matrix.

        Indices of connected nodes are True. The connectivity matrix is the admittance matrix where nonzero entries are True, other entries are False.

        Args:
            net (pp.pandapowerNet): pandapower dataset

        Returns:
            np.array[bool]: Connectivity matrix.
        """
        Ybus = net._ppc["internal"]["Ybus"]
        if not boolean:
            connect_mat = np.full(Ybus.shape, 0)
            connect_mat[np.array(Ybus.todense() != 0)] = 1
        else:
            connect_mat = np.full(Ybus.shape, False)
            connect_mat[np.array(Ybus.todense() != 0)] = True
        return connect_mat

    def get_connectivity_frame(
        self, net: pp.pandapowerNet, boolean: bool = False
    ) -> pd.DataFrame:
        con_mat = self.get_connectivity_matrix(net, boolean=boolean)
        matrix_index_labels = self.get_admittance_matrix_labels(net)
        return pd.DataFrame(
            con_mat, columns=matrix_index_labels, index=matrix_index_labels
        )

    def get_difference_between_pf_and_pandapower_dataset(
        self,
        net: pp.auxiliary.pandapowerNet,
    ) -> pd.DataFrame | None:
        """
        Get difference between pandapower dataset (exported from PF) and the original PF.

        Assumes default settings for units in the PF project (see Settings/Units). Note that only a small subset of classes and parameters is checked (see 'get_pandapower_2_pf_parameter_mapping' and 'get_pandapower_2_pf_class_mapping')

        Args:
            net (pp.auxiliary.pandapowerNet): pandapower dataset (exported from PF)

        Returns:
            pd.DataFrame | None: Dataframe with differences. None if there are no differences
        """
        pandapower_2_pf_class_mapping = self.get_pandapower_2_pf_class_mapping()
        pandapower_2_pf_parameter_mapping = self.get_pandapower_2_pf_parameter_mapping()
        differing_objects = {
            "name": [],
            "pf_class": [],
            "pp_parameter": [],
            "pf_value": [],
            "pp_value": [],
        }
        for pp_class, pf_classes in pandapower_2_pf_class_mapping.items():
            df_pp_class = net[pp_class].set_index("name")
            for pf_class in pf_classes:
                pf_objects: list[PFGeneral] = self.app.GetCalcRelevantObjects(
                    f"*.{pf_class}"
                )
                for pp_param, pf_param in pandapower_2_pf_parameter_mapping[
                    pf_class
                ].items():
                    for pf_obj in pf_objects:
                        if isinstance(pf_param, str):
                            pf_value = getattr(pf_obj, pf_param)
                        else:
                            pf_value = pf_param(pf_obj)
                        pp_value = df_pp_class.loc[pf_obj.loc_name, pp_param]
                        if not (pf_value == pp_value):
                            differing_objects["name"].append(pf_obj.loc_name)
                            differing_objects["pf_class"].append(pf_obj.GetClassName())
                            differing_objects["pp_parameter"].append(pp_param)
                            differing_objects["pf_value"].append(pf_value)
                            differing_objects["pp_value"].append(pp_value)
        if not differing_objects["name"]:
            return None
        else:
            return pd.DataFrame(differing_objects)

    def get_pandapower_2_pf_class_mapping(self) -> dict[str, list[str]]:
        """Get mapping between pandapower classes (components) and PowerFactory classes.

        Returns:
            dict[str, list[str]]: Mapping. Note that the values are lists because one pandapower class can have multiple corresponding pf classes.
        """
        return {
            "bus": ["ElmTerm"],
            "line": ["ElmLne"],
            "trafo": ["ElmTr2", "ElmTr3"],
            "impedance": ["ElmZpu", "ElmSind"],
        }

    def get_pandapower_2_pf_parameter_mapping(
        self,
    ) -> dict[str, dict[str, str | Callable]]:
        """Get parameter mapping between pandapower and PowerFactory.

        Only a small subset of all the parameters is currently implemented.

        Returns:
            dict[str, dict[str, str | Callable]]: For each pf class, a mapping between the pandapower and the pf parameter is provided. The pf parameter can be a string or a callable (input is the pf object; used for example to access a parameter of the type).
        """
        return {
            "ElmTerm": {
                "vn_kv": "uknom",
            },
            "ElmLne": {
                "length_km": "dline",
                "parallel": "nlnum",
                "r_ohm_per_km": lambda x: x.typ_id.rline,
                "x_ohm_per_km": lambda x: x.typ_id.xline,
                "c_nf_per_km": lambda x: x.typ_id.cline
                * 1000  # from micro to nano
                * x.typ_id.frnom  # nominal frequency is adapted to 50 Hz by pandapower
                / 50.0,
                "g_us_per_km": lambda x: x.typ_id.gline,
            },
            "ElmTr2": {
                "sn_mva": lambda x: x.typ_id.strn,
                "parallel": "ntnum",
                "vn_hv_kv": lambda x: x.typ_id.utrn_h,
                "vn_lv_kv": lambda x: x.typ_id.utrn_l,
                "vk_percent": lambda x: x.typ_id.uktr,
                "vkr_percent": lambda x: x.typ_id.uktrr,
            },
            "ElmTr3": {
                "parallel": "nt3nm",
                "sn_hv_mva": lambda x: x.typ_id.strn3_h,
                "sn_mv_mva": lambda x: x.typ_id.strn3_m,
                "sn_lv_mva": lambda x: x.typ_id.strn3_l,
                "vn_hv_kv": lambda x: x.typ_id.utrn3_h,
                "vn_mv_kv": lambda x: x.typ_id.utrn3_m,
                "vn_lv_kv": lambda x: x.typ_id.utrn3_l,
                "vk_hv_percent": lambda x: x.typ_id.uktr3_h,
                "vk_mv_percent": lambda x: x.typ_id.uktr3_m,
                "vk_lv_percent": lambda x: x.typ_id.uktr3_l,
                "vkr_hv_percent": lambda x: x.typ_id.uktrr3_h,
                "vkr_mv_percent": lambda x: x.typ_id.uktrr3_m,
                "vkr_lv_percent": lambda x: x.typ_id.uktrr3_l,
            },
            "ElmZpu": {
                "sn_mva": "Sn",
                "rft_pu": "r_pu",
                "xft_pu": "x_pu",
            },
            "ElmSind": {
                "sn_mva": "Sn",
                "rft_pu": lambda x: (x.rrea * x.Sn) / (x.ucn**2),
                "xft_pu": lambda x: (x.xrea * x.Sn) / (x.ucn**2),
            },
        }
