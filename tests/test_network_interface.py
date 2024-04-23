import pytest
import sys
sys.path.insert(0, r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)

from test_active_project_interface import pfp, pf_app, activate_test_project

@pytest.fixture
def pfni(pf_app):
  return powfacpy.PFNetworkInterface(pf_app)

def test_get_vacant_cubicle_of_terminal(pfni, activate_test_project):
  study_case = pfni.get_single_obj(r"Study Cases\test_network_interface\Study Case")
  study_case.Activate()
  pfni.get_vacant_cubicle_of_terminal(
    r"Network Model\Network Data\test_plot_interface\Grid 1\Terminal HV 2")

if __name__ == "__main__":
  pytest.main(([r"tests\test_network_interface.py"]))
