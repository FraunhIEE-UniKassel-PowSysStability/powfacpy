import os
import zipfile
import glob
import importlib
import sys

import pytest
import numpy as np

sys.path.insert(0, r".\src")

import powfacpy
import powfacpy.applications.model_exchange
from powfacpy.applications.model_exchange import CGMES

importlib.reload(powfacpy)


@pytest.fixture
def pfcgmes(pf_app) -> CGMES:
    # Return PFModelExchangeInterface instance and show app
    pfcgmes = CGMES(pf_app)
    return pfcgmes


def _get_loadflow_results(pfcgmes: CGMES):
    loadflow = pfcgmes.act_prj.app.GetFromStudyCase("ComLdf")
    loadflow.Execute()
    terminals = pfcgmes.act_prj.app.GetCalcRelevantObjects("*.ElmTerm")
    voltages = {term.loc_name: term.GetAttribute("m:u1") for term in terminals}
    lines = pfcgmes.act_prj.app.GetCalcRelevantObjects("*.ElmLne")
    active_powers = {line.loc_name: line.GetAttribute("m:P:bus1") for line in lines}
    return voltages, active_powers


def _clear_output_path(output_path):
    if os.path.isdir(output_path):
        _ = [os.remove(file) for file in glob.glob(os.path.join(output_path, "*"))]
    return None


def _get_output_path():
    return os.path.abspath(r".\tests\tests_output\cgmes_export")


def _activate_new_study_case_and_grid(pfcgmes: CGMES):
    pfcgmes.act_prj.app.GetActiveStudyCase().Deactivate()
    new_study_case = pfcgmes.act_prj.create_in_folder(
        "New Study Case.IntCase",
        r"Study Cases\test_model_exchange_interfaces",
        overwrite=True,
    )
    new_study_case.Activate()
    new_grid = pfcgmes.act_prj.create_in_folder(
        "New Grid.ElmNet",
        r"Network Model\Network Data\test_model_exchange_interfaces",
        overwrite=True,
    )
    new_grid.Activate()
    return new_study_case


def _compare_loadflow_results(before: dict, after: dict, THRESHOLD=1e-4):
    for element_name, value_before in before.items():
        before_after_difference = abs(
            (value_before - after[element_name]) / value_before
        )
        assert before_after_difference < THRESHOLD


def _assert_that_steady_state_changed(u1: dict, u2: dict):
    u1 = np.array(list(u1.values()))
    u2 = np.array(list(u2.values()))
    assert np.abs((u1 - u2) / u1).max() > 0.01


def _convert_xml_names_to_profile_names(names):
    return [x.split('_')[-2] for x in names] 

def _assert_profiles_in_list(profiles_list, profiles_to_check):
    assert len(profiles_list) == len(profiles_to_check) 
    assert all(s in profiles_list for s in profiles_to_check)

def test_cgmes_export(pfcgmes: CGMES, activate_powfacpy_test_project):
    
    OUTPUT_PATH = os.path.abspath(r".\tests\tests_output\cgmes_export")
    _clear_output_path(OUTPUT_PATH)

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles="all", as_zip=True)
    file = os.listdir(OUTPUT_PATH)
    assert 'cgmes_profiles.zip' in file
    with zipfile.ZipFile('\\'.join([OUTPUT_PATH]+file), 'r') as zip_file:
        zip_contents = zip_file.namelist()
    profiles = _convert_xml_names_to_profile_names(zip_contents)
    _assert_profiles_in_list(profiles, ['EQ', 'TP', 'SSH', 'SV', 'DY', 'DL', 'GL', 'SC'])

    _clear_output_path(OUTPUT_PATH)
    assert not os.listdir(OUTPUT_PATH) # assert folder is empty

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles="ssh", as_zip=False)
    profiles = _convert_xml_names_to_profile_names(os.listdir(OUTPUT_PATH))
    _assert_profiles_in_list(profiles, ['SSH'])
    _clear_output_path(OUTPUT_PATH)

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles="all", as_zip=False)
    profiles = _convert_xml_names_to_profile_names(os.listdir(OUTPUT_PATH))
    _assert_profiles_in_list(profiles, ['EQ', 'TP', 'SSH', 'SV', 'DY', 'DL', 'GL', 'SC'])
    _clear_output_path(OUTPUT_PATH)

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles="ssh eq", as_zip=True)
    file = os.listdir(OUTPUT_PATH)
    assert len(file) == 1
    with zipfile.ZipFile('\\'.join([OUTPUT_PATH]+file), 'r') as zip_file:
        zip_contents = zip_file.namelist()
    profiles = _convert_xml_names_to_profile_names(zip_contents)
    _assert_profiles_in_list(profiles, ['EQ', 'SSH'])
    _clear_output_path(OUTPUT_PATH)


def test_cgmes_export_import(pfcgmes: CGMES, activate_powfacpy_test_project):
    OUTPUT_PATH = _get_output_path()
    _clear_output_path(OUTPUT_PATH)

    pfcgmes.act_prj.get_unique_obj(
        r"Study Cases\test_model_exchange_interfaces\Study Case"
    ).Activate()
    voltages_before, active_powers_before = _get_loadflow_results(pfcgmes)

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles="all", as_zip=True)

    _ = _activate_new_study_case_and_grid(pfcgmes)
    pfcgmes.cgmes_import(OUTPUT_PATH + "\\" + pfcgmes.exported_zip_name + ".zip")

    voltages_after, active_powers_after = _get_loadflow_results(pfcgmes)

    _compare_loadflow_results(voltages_before, voltages_after)
    _compare_loadflow_results(active_powers_before, active_powers_after)


def test_cgmes_update_profiles(pfcgmes: CGMES, activate_powfacpy_test_project):
    OUTPUT_PATH = _get_output_path()
    _clear_output_path(OUTPUT_PATH)

    study_case_source = pfcgmes.act_prj.get_unique_obj(
        r"Study Cases\test_model_exchange_interfaces\Study Case"
    )
    study_case_source.Activate()
    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles="all", as_zip=True)

    study_case_destination = _activate_new_study_case_and_grid(pfcgmes)
    pfcgmes.cgmes_import(OUTPUT_PATH + "\\" + pfcgmes.exported_zip_name + ".zip")

    voltages_source_before_changes, active_powers_source_before_changes = (
        _get_loadflow_results(pfcgmes)
    )
    study_case_source.Activate()
    for load in pfcgmes.act_prj.get_obj("*.ElmLod", include_subfolders=True):
        load.qlini = 0
    voltages_source, active_powers_source = _get_loadflow_results(pfcgmes)

    _assert_that_steady_state_changed(voltages_source_before_changes, voltages_source)

    pfcgmes.cgmes_export(OUTPUT_PATH, selected_profiles="ssh dl", as_zip=True)
    study_case_destination.Activate()
    base_archive = pfcgmes.act_prj.get_unique_obj(
        r"cgmes_archive_folder\cgmes_archive_imported"
    )
    pfcgmes.update_profiles(
        OUTPUT_PATH + "\\" + pfcgmes.exported_zip_name + ".zip", base_archive
    )
    voltages_destination, active_powers_destination = _get_loadflow_results(pfcgmes)

    for load in pfcgmes.act_prj.get_obj("*.ElmLod", include_subfolders=True):
        assert load.qlini == 0
    _compare_loadflow_results(voltages_source, voltages_destination)
    _compare_loadflow_results(active_powers_source, active_powers_destination)


if __name__ == "__main__":
    pytest.main(([r"tests\applications\test_model_exchange.py"]))
