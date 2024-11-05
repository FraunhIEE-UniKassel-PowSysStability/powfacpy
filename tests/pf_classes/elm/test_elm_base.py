import sys

import pytest

sys.path.insert(0, r".\src")
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.base.active_project import ActiveProject

sys.path.insert(0, r".\tests")


def test_elm_base(act_prj: ActiveProject, activate_powfacpy_test_project):
    terminal = act_prj.get_calc_relevant_obj("*.ElmTerm")[0]
    terminal_elmbase = ElmBase(terminal)

    terminal_elmbase.set_out_of_service()
    assert terminal.outserv == 1
    assert terminal_elmbase.outserv == 1

    terminal_elmbase.set_into_service()
    assert terminal.outserv == 0
    assert terminal_elmbase.outserv == 0


if __name__ == "__main__":
    pytest.main([r"tests\pf_classes\elm\test_elmbase.py"])
