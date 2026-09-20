"""The `ModalAnalysis` application: wraps PowerFactory's modal analysis command (`ComMod`).
"""

from __future__ import annotations

from os import getcwd, makedirs
from os.path import join
from shutil import rmtree
from typing import Any
import numpy as np
import numpy.typing as npt
import pandas as pd

try:
    from scipy.linalg import eig
except ImportError as exc:
    raise ImportError(
        "powfacpy.applications.dynamic_modal_analysis needs the 'scipy' package - "
        "install with `pip install powfacpy[dynamic_modal_analysis]`"
    ) from exc

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_classes.protocols import ComMod, PFApp
from powfacpy.applications.dynamic_modal_analysis.eigenvalues import EigenvalueSet, ParticipationFactorSet
from powfacpy.applications.dynamic_modal_analysis.results import ModalAnalysisResults


class ModalAnalysis(ApplicationBase):
    """Modal (small-signal) analysis of PowerFactory's current state.

    Activate the study case / scenario / operating point you want analyzed
    yourself first (like `DynamicSimulation` or `StaticCalc` - this class
    does not switch study cases for you).
    """

    #: default `ComMod` parameters: calculate eigenvectors and participation
    #: factors and export the system matrix, without dropping any eigenvalue
    #: from the results (every 'only record ...' filter switched off).
    DEFAULT_COMMOD_PARAMS: dict[str, Any] = {
        "iLeft": True,
        "iRight": True,
        "iPart": True,
        "initMode": 0,
        "iSysMatsMatl": True,
        "isRecOscModesOnly": False,
        "isRecUnstabModesOnly": False,
        "isRecMinReal": False,
        "isRecMaxReal": False,
        "isRecMinImag": False,
        "isRecMaxImag": False,
        "isRecMinMagn": False,
        "isRecMaxMagn": False,
        "isRecMinDampRat": False,
        "isRecMaxDampRat": False,
    }

    def __init__(self, pf_app: PFApp | None | bool = False, cached: bool = False) -> None:
        super().__init__(pf_app, cached)

    def run(self, commod_params: dict[str, Any] | None = None) -> ModalAnalysisResults:
        """Run the modal analysis command (`ComMod`) and return the eigenvalues
        and participation factors of the current operating point.

        Args:
            commod_params: additional/overriding `ComMod` parameters, merged
                over `DEFAULT_COMMOD_PARAMS`.

        Returns:
            ModalAnalysisResults: the eigenvalues, participation factors and
            system matrix.
        """
        export_dir = join(getcwd(), "dynamic_modal_analysis_export")
        makedirs(export_dir, exist_ok=True)
        try:
            self._run_commod(export_dir, commod_params or {})
            sys_matrix = self._read_system_matrix(export_dir)
            state_names = self._read_state_names(export_dir)
        finally:
            rmtree(export_dir, ignore_errors=True)

        indexes = list(range(1, len(state_names) + 1))
        eigenvalue_vec, participation, left_vec, right_vec = self._eigenvalues_and_participation(
            sys_matrix
        )
        eigenvalues = EigenvalueSet(eigenvalue_vec, indexes)
        participation_factors = ParticipationFactorSet(participation, state_names, indexes)
        right_eigenvectors = pd.DataFrame(right_vec, index=state_names, columns=indexes)
        left_eigenvectors = pd.DataFrame(left_vec, index=state_names, columns=indexes)
        return ModalAnalysisResults(
            sys_matrix,
            eigenvalues,
            participation_factors,
            right_eigenvectors=right_eigenvectors,
            left_eigenvectors=left_eigenvectors,
        )

    def _run_commod(self, export_dir: str, commod_params: dict[str, Any]) -> None:
        commod: ComMod = self.act_prj.get_from_study_case("ComMod")
        params = {**self.DEFAULT_COMMOD_PARAMS, "dirMatl": export_dir, **commod_params}
        self.act_prj.set_attr(commod, params)
        commod.Execute()

    def _read_system_matrix(self, export_dir: str) -> npt.NDArray[np.complex128]:
        """Parse the exported system (A) matrix.

        `Amat.mtl` follows the sparse coordinate format MATLAB's `spconvert`
        expects: each row is `row column real [imag]`.
        """
        df = pd.read_csv(
            join(export_dir, "Amat.mtl"),
            sep=r"\s+",
            header=None,
            names=["row", "column", "re", "imag"],
            dtype={"row": int, "column": int, "re": float, "imag": float},
            encoding="ISO-8859-1",
            engine="python",
        )
        size = int(df["row"].max())
        sys_matrix = np.zeros((size, size), dtype=np.complex128)
        rows = df["row"].to_numpy() - 1
        cols = df["column"].to_numpy() - 1
        re = df["re"].to_numpy()
        imag = df["imag"].to_numpy()
        has_imag = ~np.isnan(imag)
        sys_matrix[rows[~has_imag], cols[~has_imag]] = re[~has_imag]
        sys_matrix[rows[has_imag], cols[has_imag]] = re[has_imag] + 1j * imag[has_imag]
        return sys_matrix

    def _read_state_names(self, export_dir: str) -> npt.NDArray[np.str_]:
        """Parse the exported list of state variable names, as
        `"<model name>\\\\<state variable>"`."""
        df = pd.read_csv(
            join(export_dir, "VariableToIdx_Amat.txt"),
            sep=r"\s\s+",
            header=0,
            names=["Matrix column index", "Model name", "State variable"],
            dtype={"Matrix column index": int, "Model name": str, "State variable": str},
            encoding="ISO-8859-1",
            index_col=0,
            engine="python",
        )
        state_var = df["State variable"].str.replace('"', "", regex=False)
        return (df["Model name"] + "\\" + state_var).to_numpy(dtype=str)

    def _eigenvalues_and_participation(
        self, sys_matrix: npt.NDArray[np.complex128]
    ) -> tuple[
        npt.NDArray[np.complex128],
        npt.NDArray[np.float64],
        npt.NDArray[np.complex128],
        npt.NDArray[np.complex128],
    ]:
        """Eigenvalues, the (normalized) participation of every state in
        every eigenvalue, and the raw left/right eigenvectors, from one
        combined eigendecomposition.

        Participation factor `p_ki = |phi_ki| * |psi_ik|` (right eigenvector
        element times left eigenvector element), normalized so each
        eigenvalue's participation column sums to 1 (Perez-Arriaga et al.) -
        the same `phi`/`psi` also used, unnormalized, by
        `ModalAnalysisResults.eigenvalue_sensitivity`.
        """
        eigenvalues, left_vec, right_vec = eig(sys_matrix, left=True, right=True)
        participation = np.abs(left_vec) * np.abs(right_vec)
        participation = participation / participation.sum(axis=0, keepdims=True)
        return eigenvalues, participation, left_vec, right_vec
