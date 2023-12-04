import pytest
import sys
sys.path.insert(0, r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)
import os
import glob

from test_base_interface import pfbi, pf_app, activate_test_project

@pytest.fixture
def pfmei(pf_app):
    # Return PFModelExchangeInterface instance and show app
    pfmei = powfacpy.PFModelExchangeInterface(pf_app)
    return pfmei


def test_cgmes_export(pfmei, activate_test_project):
    OUTPUT_PATH = os.path.abspath(r'.\tests\tests_output\cgmes_export')
    clear_output_path = lambda: [os.remove(file) for file in glob.glob(os.path.join(OUTPUT_PATH, '*'))]
    clear_output_path()
    
    pfmei.get_unique_obj(r"Study Cases\test_model_exchange_interface\Study Case").Activate()
    
    pfmei.cgmes_export(OUTPUT_PATH, selected_profiles='all', as_zip=False)
    clear_output_path()
    # TODO create assertion

    pfmei.cgmes_export(OUTPUT_PATH, selected_profiles='ssh', as_zip=False)
    clear_output_path()
    # TODO create assertion

    pfmei.cgmes_export(OUTPUT_PATH, selected_profiles='all', as_zip=True)
    clear_output_path()
    # TODO create assertion

    pfmei.cgmes_export(OUTPUT_PATH, selected_profiles='ssh eq', as_zip=True)
    clear_output_path()
    # TODO create assertion



if __name__ == "__main__":
    pytest.main(([r"tests\test_model_exchange_interface.py"]))