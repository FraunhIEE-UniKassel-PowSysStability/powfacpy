import pytest
import sys
sys.path.insert(0, r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)

from test_base_interface import pfbi, pf_app, activate_test_project

@pytest.fixture
def pfri(pf_app):
    # Return PFResultsInterface instance and show app
    pfri = powfacpy.PFResultsInterface(pf_app)
    return pfri

def test_export_to_pandas(pfri, activate_test_project):
    pfri.get_unique_obj(r"Study Cases\test_results_interface\Study Case").Activate()
    network_element = pfri.get_obj(r'Network Model\Network Data\test_results_interface\Grid\General Load HV.ElmLod', include_subfolders=True)[0]
    variables = ['m:i1:bus1', 'm:u1:bus1']
    elmres = pfri.add_results_variable(network_element, variables)
    pfdi = powfacpy.PFDynSimInterface(pfri.app)
    pfdi.initialize_sim(param={"p_resvar":elmres})
    pfdi.run_sim()
    nr_of_columns_including_time = len(variables) + 1
    df = pfri.export_to_pandas(
        result_objects=[elmres,]*len(variables),
        elements=[network_element,]*len(variables), 
        variables=variables)
    assert len(df.columns) == nr_of_columns_including_time

if __name__ == "__main__":
    pytest.main(([r"tests\test_results_interface.py"]))