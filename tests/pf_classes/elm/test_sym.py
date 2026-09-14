import sys

import pytest

sys.path.insert(0, r".\src")

from powfacpy.pf_classes.elm.sym import SynchronousMachine
from powfacpy.pf_classes.protocols import PFApp


def test_p_and_q_read_and_write(
    activate_39_bus_new_england_test_project, pf_app: PFApp
):
    """Regression test: 'q' used to be a plain (undecorated) method whose body was
    then silently replaced by a mis-targeted '@p.setter', so reading '.q' returned
    active power ('pgini') instead of reactive power ('qgini')."""
    elm_sym = pf_app.GetCalcRelevantObjects("G 01.ElmSym")[0]
    machine = SynchronousMachine(elm_sym)

    assert machine.p == pytest.approx(elm_sym.pgini)
    assert machine.q == pytest.approx(elm_sym.qgini)
    assert machine.p != machine.q  # would coincide if 'q' still read 'pgini'

    original_p, original_q = elm_sym.pgini, elm_sym.qgini
    try:
        machine.p = original_p + 1.0
        machine.q = original_q + 2.0
        assert elm_sym.pgini == pytest.approx(original_p + 1.0)
        assert elm_sym.qgini == pytest.approx(original_q + 2.0)
        assert machine.p == pytest.approx(original_p + 1.0)
        assert machine.q == pytest.approx(original_q + 2.0)
    finally:
        elm_sym.pgini = original_p
        elm_sym.qgini = original_q


if __name__ == "__main__":
    pytest.main([r"tests\pf_classes\elm\test_sym.py"])
