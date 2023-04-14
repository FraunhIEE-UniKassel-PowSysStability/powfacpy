import pytest
import sys

sys.path.insert(0, r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)

from test_base_interface import pfbi, pf_app, activate_test_project

@pytest.fixture
def pfscripts(pf_app):
    return powfacpy.PFComPythonObjectInterface(pf_app)

def test_create_file_from_embedded_script(pfscripts, activate_test_project):
  compython = r"Library\Scripts\embedded_test_script"
  pfscripts.create_file_from_embedded_script(
    r".\tests\tests_output\file_from_embedded_script.py", compython)

def test_set_embedded_script_from_file(pfscripts, activate_test_project):
  compython = pfscripts.create_by_path(
    r"Library\Scripts\auto_created_embedded_test_script.ComPython")
  pfscripts.set_embedded_script_from_file(compython,
    r".\tests\tests_input\simple_script.py")

def test_merge_file_into_embedded_script(pfscripts, activate_test_project):
  compython = r"Library\Scripts\embedded_test_script"
  pfscripts.merge_file_into_embedded_script(compython,
    r".\tests\tests_input\simple_script.py",
    "#### Insert after this line",
    "#### Insert before this line")

def test_merge_powfacpy_package_into_single_file(pfscripts, activate_test_project):
  pfscripts.merge_powfacpy_package_into_single_file(
  r".\tests\tests_output\powfacpy_single_file.py")
  compython = r"Library\Scripts\embedded_test_script"
  pfscripts.merge_file_into_embedded_script(compython,
    r".\tests\tests_output\powfacpy_single_file.py",
    "#### Insert powfacpy after this line",
    "#### End powfacpy before this line")
  # Please manually execute this compython script (not possible to test
  # this automatically)   


if __name__ == "__main__":
  pytest.main(([r"tests\test_script_interface.py"]))  