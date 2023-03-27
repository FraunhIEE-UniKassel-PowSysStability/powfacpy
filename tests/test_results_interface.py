import pytest
import sys
sys.path.insert(0,r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)

from test_base_interface import pfbi, pf_app, activate_test_project_quasi_dynamic

@pytest.fixture
def pfri(pf_app):
    # Return PFResultsInterface instance and show app
    pfri = powfacpy.PFResultsInterface(pf_app)
    return pfri

def test_export_to_pandas(pfri, activate_test_project_quasi_dynamic):
    object = pfbi.get_obj(r'Network Model\Network Data\test_base_interface\Grid\General Load HV.ElmLod', include_subfolders=True)[0]
    variables = ['m:i1:bus1', 'm:u1:bus1']
    nr_of_columns_including_time = len(variables) + 1
    elmres = pfbi.app.GetFromStudyCase('ElmRes')
    df = pfbi.export_to_pandas(
        result_objects=[elmres,]*len(variables),
        elements=[object,]*len(variables), 
        variables=variables)
    assert len(df.columns) == nr_of_columns_including_time

if __name__ == "__main__":
    pytest.main(([r"tests\test_results_interface.py"]))