""" """

from __future__ import annotations

import sys, os, shutil
from fnmatch import fnmatchcase
from typing import Callable, Iterable, Any, OrderedDict
import importlib, inspect
import copy

import pandas as pd
import numpy as np
from icecream import ic


from powfacpy.applications.application_base import ApplicationBase
from powfacpy.base.string_manipulation import PFStringManipulation
from powfacpy.pf_classes.protocols import ElmDsl, PFGeneral, PFApp, ElmComp


class DynamicModelDocs(ApplicationBase):

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)
        self.target_directory: str = ".\\"

    def create_docs(
        self, model: ElmComp | ElmDsl, clear_target_dir: bool = False
    ) -> None:
        if clear_target_dir:
            if os.path.exists(self.target_directory):
                shutil.rmtree(self.target_directory)
            os.makedirs(self.target_directory)
