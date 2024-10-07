from __future__ import annotations

from powfacpy.applications.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import StaPll

from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.result_variables import ResVar

RMS_BAL = ResVar.RMS_Bal


class PhaseLockedLoop(ElmBase):

    def __init__(self, obj: StaPll) -> None:
        super().__init__(obj)
        self._obj: StaPll

    def __new__(cls, *args, **kwargs) -> StaPll | PhaseLockedLoop:
        """Implemented only to add type hints for the created instance.

        Returns:
            StaPll | PhaseLockedLoop: New instance
        """
        instance = super().__new__(cls)
        return instance

    def set_standard_parameters(self):
        self._obj.i_norm = 1  # improved behavior during large voltage deviations
        self._obj.Kp = 1
