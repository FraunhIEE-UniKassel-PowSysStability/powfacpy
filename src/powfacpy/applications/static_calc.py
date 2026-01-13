"""Module with interface for static calculations (load flow, short circuits,..)"""

from warnings import warn
from os import getcwd, remove

import pandas as pd
from icecream import ic

import powfacpy
from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_classes.protocols import ElmSecctrl, PFGeneral, PFApp


class StaticCalc(ApplicationBase):
    """Static calculation (e.g. load flow, short circuit,..) interface"""

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)

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
