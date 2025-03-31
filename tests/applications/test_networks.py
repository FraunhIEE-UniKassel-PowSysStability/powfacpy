import sys
import importlib

import pytest

sys.path.insert(0, r".\src")
from powfacpy.pf_classes.protocols import StaCubic
import powfacpy
from powfacpy.applications.networks import Networks

importlib.reload(powfacpy)


@pytest.fixture
def pfnet(pf_app) -> Networks:
    return Networks(pf_app)


def test_get_vacant_cubicle_of_terminal(
    pfnet: Networks, activate_powfacpy_test_project
) -> None:
    study_case = pfnet.act_prj.get_single_obj(
        r"Study Cases\test_network_interface\Study Case"
    )
    study_case.Activate()
    cub: StaCubic = pfnet.get_vacant_cubicle_of_terminal(
        r"Network Model\Network Data\test_plot_interface\Grid 1\Terminal HV 2"
    )
    assert cub.GetClassName() == "StaCubic"
    assert cub.obj_id is None


if __name__ == "__main__":
    pytest.main(([r"tests\applications\test_networks.py"]))
