import pytest
import sys
import json
settings_file = open('.\\settings.json')
settings = json.load(settings_file)
sys.path.append(settings["local path to PowerFactory application"])
import powerfactory
sys.path.insert(0, r'.\src')
import powfacpy 
import importlib
importlib.reload(powfacpy)
from jsondiff import diff

from test_base_interface import pfbi, pf_app, activate_test_project

@pytest.fixture
def pfdbi(pf_app):
  # Return PFDataBaseInterface instance
  return powfacpy.PFDatabaseInterface(pf_app)

def test_get_and_set_object_attributes(pfdbi, activate_test_project):
  """
  Tests for getting and setting object attributes.
  The methods get_object_attributes and set_object_attributes can best be tested
  together by 
    1. getting data of PF objects from the PF database.
    2. modifiy some of the data.
    3. setting the data of the PF objects in the PF database with the output from 2.
    4. again getting data of PF objects from the PF database.
    5. Checking if the output from 2. and 4. are equal. If so, getting and setting
    data works correctly.
  This process is done with various optional arguments (relative_paths, pf_obj_handling_options).
  The json files under 'tests\tests_output\test_get_object_attributes*.json' can help with the 
  interpretation of the operations.
  """
  truncated_paths = ["", r"Network Model\Network Data"]
  pf_obj_handling_options = ["path", "original_pf_obj"]
  for truncated_path in truncated_paths:
    for pf_obj_handling in pf_obj_handling_options:
      objs = pfdbi.get_obj("*",parent_folder=r"Network Model\Network Data\test_database_interface\Grid")
      class_attributes =  {
        "*": ["loc_name", "chr_name"],
        "ElmVac": ["bus1", "outserv"],
        "ElmTr2": ["typ_id"],    
      }
      obj_attr_dict = pfdbi.get_object_attributes(
        objs,
        class_attributes = class_attributes,
        truncated_path = truncated_path,
        pf_obj_handling = pf_obj_handling) 
      if pf_obj_handling == "path":
        with open(r'tests\tests_output\test_get_object_attributes.json', 'w') as json_file:
          json.dump(obj_attr_dict,json_file,indent=5)
      # Modify data    
      for obj in obj_attr_dict.keys():
        obj_attr_dict[obj]["chr_name"] += "A"   
      if pf_obj_handling == "path":
        with open(r'tests\tests_output\test_get_object_attributes_modified.json', 'w') as json_file:       
          json.dump(obj_attr_dict,json_file,indent=5)
      pfdbi.set_object_attributes(obj_attr_dict, added_path=truncated_path)  
      obj_attr_dict_after_reading_and_writing = pfdbi.get_object_attributes(
        objs,
        class_attributes=class_attributes,
        truncated_path=truncated_path,
        pf_obj_handling = pf_obj_handling) 
      assert(not diff(obj_attr_dict, obj_attr_dict_after_reading_and_writing))


if __name__ == "__main__":
  pytest.main([r"tests\test_database_interface.py"])
  # pytest.main(([r"tests"]))
