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
def pfcgmes(pf_app):
    # Return PFModelExchangeInterface instance and show app
    pfcgmes = powfacpy.PFCgmesInterface(pf_app)
    return pfcgmes


def test_cgmes_export(pfcgmes, activate_test_project):
    OUTPUT_PATH = os.path.abspath(r'.\tests\tests_output\cgmes_export')
    clear_output_path = lambda: [os.remove(file) for file in glob.glob(os.path.join(OUTPUT_PATH, '*'))]
    clear_output_path()
    # TODO create assertion

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles='all', as_zip=True)
    clear_output_path()
    # TODO create assertion

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles='ssh', as_zip=False)
    clear_output_path()
    # TODO create assertion

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles='all', as_zip=False)
    clear_output_path()
    # TODO create assertion

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles='ssh eq', as_zip=True)
    clear_output_path()
    # TODO create assertion


def test_cgmes_export_import(pfcgmes, activate_test_project):
    OUTPUT_PATH = os.path.abspath(r'.\tests\tests_output\cgmes_export')
    clear_output_path = lambda: [os.remove(file) for file in glob.glob(os.path.join(OUTPUT_PATH, '*'))]
    clear_output_path()
    
    pfcgmes.get_unique_obj(r"Study Cases\test_model_exchange_interfaces\Study Case").Activate()
    
    loadflow_before = pfcgmes.app.GetFromStudyCase('ComLdf')
    loadflow_before.Execute()
    terminals = pfcgmes.app.GetCalcRelevantObjects('*.ElmTerm')
    voltages_before = {term.loc_name:term.GetAttribute('m:u1') for term in terminals}
    lines = pfcgmes.app.GetCalcRelevantObjects('*.ElmLne')
    active_powers_before = {line.loc_name:line.GetAttribute('m:P:bus1') for line in lines}

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles='all', as_zip=True)

    pfcgmes.app.GetActiveStudyCase().Deactivate()
    new_study_case = pfcgmes.create_in_folder(r'Study Cases\test_model_exchange_interfaces', 'New Study Case.IntCase')
    new_study_case.Activate()
    new_grid = pfcgmes.create_in_folder(r'Network Model\Network Data\test_model_exchange_interfaces', 'New Grid.ElmNet')
    new_grid.Activate()

    pfcgmes.cgmes_import(OUTPUT_PATH + '\\' + pfcgmes.EXPORTED_ZIP_NAME + '.zip')

    loadflow_after = pfcgmes.app.GetFromStudyCase('ComLdf')
    loadflow_after.Execute()
    terminals = pfcgmes.app.GetCalcRelevantObjects('*.ElmTerm')
    voltages_after = {term.loc_name:term.GetAttribute('m:u1') for term in terminals}
    lines = pfcgmes.app.GetCalcRelevantObjects('*.ElmLne')
    active_powers_after = {line.loc_name:line.GetAttribute('m:P:bus1') for line in lines}
    
    for terminal_name, voltage_before in voltages_before.items():
        before_after_difference = abs(voltage_before - voltages_after[terminal_name])
        assert before_after_difference < 1e-4
    for line_name, active_power_before in active_powers_before.items():
        before_after_difference = abs(active_power_before - active_powers_after[line_name])
        assert before_after_difference < 1e-2


def test_cgmes_update_profiles(pfcgmes, activate_test_project):
    #TODO
    pass



if __name__ == "__main__":
    pytest.main(([r"tests\test_model_exchange_interfaces.py"]))