import sys
import importlib

import pytest

sys.path.insert(0, r".\src")
import powfacpy
from powfacpy.base.base import BaseObjectStatic, BaseChild, BaseChildStatic
from powfacpy.base.active_project import ActiveProject

importlib.reload(powfacpy)


def test_base_obj_static(act_prj: ActiveProject, activate_test_project):
    terminal = act_prj.get_calc_relevant_obj("*.ElmTerm")[0]
    terminal_base_obj = BaseObjectStatic(terminal)
    assert terminal_base_obj.obj == terminal_base_obj._obj  # test property obj
    assert terminal_base_obj == terminal  # test __eq__
    assert str(terminal_base_obj) == terminal.loc_name  # test __str__


def test_base_child_caching(act_prj: ActiveProject, activate_test_project):
    terminal = act_prj.get_calc_relevant_obj("*.ElmTerm")[0]
    terminal_base_child = BaseChild(terminal)
    terminal_base_child.cache_attr("uknom")
    assert terminal_base_child.__dict__["uknom"] == terminal.uknom

    terminal_base_child.cache_method("GetClassName")
    assert "GetClassName" in terminal_base_child.__dict__
    assert terminal_base_child.GetClassName() == terminal.GetClassName()


def test_base_child_static(act_prj: ActiveProject, activate_test_project):
    terminal = act_prj.get_calc_relevant_obj("*.ElmTerm")[0]
    terminal_base_child_static = BaseChildStatic(terminal)
    # Call methods, get attributes..
    cub = terminal_base_child_static.CreateObject("StaCubic", "a")
    terminal_base_child_static.AddCopy(cub)
    assert terminal_base_child_static.GetParent() == terminal.GetParent()
    assert terminal_base_child_static.GetContents() == terminal.GetContents()
    assert terminal_base_child_static.uknom == terminal.uknom

    # cannot dynamically add attributes
    with pytest.raises(AttributeError):
        terminal_base_child_static.foo


if __name__ == "__main__":
    pytest.main([r"tests\test_base.py"])
