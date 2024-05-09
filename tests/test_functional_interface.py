import sys

import pytest

from powfacpy.functional_interface import set_attr_of_obj

sys.path.insert(0, r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)
from test_active_project_interface import pfp, pf_app, activate_test_project


def test_set_attr_of_obj(pfp, activate_test_project):
    test_string_1 = "TestString1"
    model = pfp.get_single_obj(r"Library\Dynamic Models\Linear_interpolation")
    set_attr_of_obj(model,{"sTitle":test_string_1})
    stitle = pfp.get_attr(model,"sTitle")
    assert stitle == test_string_1
