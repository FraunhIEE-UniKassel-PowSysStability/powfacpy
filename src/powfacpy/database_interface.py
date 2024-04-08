"""
The database interface is helpful to interact with larger numbers
of PF objects in the database (getting, setting, storing or comparing
attributes).
One use case is for example to define a set of standard parameters for a
larger model. Using the interface, one can easily get, store (e.g. in a json file)
and later reset a set of parameters.

ToDo: Add tutorial for this interface (when there is more functionality).
"""


import sys
sys.path.insert(0, r'.\src')
import powfacpy
from fnmatch import fnmatchcase

class PFDatabaseInterface(powfacpy.PFBaseInterface):
  
  def __init__(self, app):
    super().__init__(app)

  def get_object_attributes(
      self,
      objs,
      class_attributes: dict = None,
      truncated_path: str = "",
      pf_obj_handling: str ="path") -> dict:
    """
    Get dictionary with attributes of objects.
    The keys of the dictionary are the paths of the objects.
    The values are dictionaries with keys (attribute names) and values (attribute
    values), see "example return dict" below. 
    
    Arguments:
      - objs: Iterable with PF objects
      - class_attributes: dictionary with keys (class names) and values 
        (iterable with attribute names). To control which attributes are 
        relevant for a class. The class names can contain wildcards ("*").
        Example:
          {
            "ElmTr2": ["typ_id"],
            "*": ["loc_name", ],
            "ElmVac": ["bus1", "outserv"],    
          }
          -> "loc_name" is relevant for every class
      - truncated_path: If specified, this path is truncated from the keys (object paths)
        Example: truncated_path = "Network Model\\Network Data"
          -> Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_database_interface\\Grid.ElmNet\\AC Voltage Source.ElmVac"
          becomes "test_database_interface\\Grid.ElmNet\\AC Voltage Source.ElmVac" (first part truncated)
      - pf_obj_handling: If the value of an attribute is a PF object, there are several options on 
        how to read the attribute (please see _handle_attribute_type_for_reading)
          
    Example return dict:
    {
      "Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_database_interface\\Grid.ElmNet\\AC Voltage Source.ElmVac": {
            "loc_name": "AC Voltage Source",
            "bus1": "Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_database_interface\\Grid.ElmNet\\Terminal HV 1.ElmTerm\\Cub_1.StaCubic",
            "outserv": 0
      },
      "Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_database_interface\\Grid.ElmNet\\Terminal HV 1.ElmTerm\\Cub_1.StaCubic": {
            "loc_name": "Cub_1"
      },
    }
    """
    if not class_attributes:
      class_attributes = {"*": []} # no relevant attributes -> get only keys (object paths)
    if truncated_path: # include class names in truncated_path
      truncated_path = self.get_path_of_obj_with_class_names_relative_to_project(truncated_path)  

    obj_attr_dict = {}
    for obj in objs:
      obj_path = self.get_path_of_obj_with_class_names_relative_to_project(obj)
      if truncated_path: 
        obj_path = powfacpy.PFStringManipulation.truncate_until(
          obj_path,truncated_path + "\\") 
      obj_attr_dict[obj_path] = {}
      for class_name in class_attributes.keys():
        if fnmatchcase(obj.GetClassName(), class_name): # fnmatch allows to use wildcards ("*")
          for attr in class_attributes[class_name]:
            obj_attr_dict[obj_path][attr] = self._handle_attribute_type_for_reading(
              obj, attr, pf_obj_handling)
    return obj_attr_dict
  
  def set_object_attributes(
      self,
      obj_attr_dict: dict,
      added_path: str = ""):
    """
    Takes a dict with keys (object paths) and values (dict with attributes 
    and their values) and writes the data to the PF database.
    (the dict can be created e.g. with 'get_object_attributes')

    Arguments:
      - obj_attr_dict: data
      - added_path: Assumes that the object paths are relative to a parent 
        folder inside the project. Adds added_path to the paths. 
    """
    for obj, attr_key_val in obj_attr_dict.items():
      if added_path:
        obj = added_path + "\\" + obj
      obj = self.get_unique_obj(obj)
      for attr, value in attr_key_val.items():
        if isinstance(value, str):
          if not isinstance(obj.GetAttributeType(attr), str): # Then a PF objeczt is expected
            value_pf_obj = self.get_unique_obj(value, error_if_non_existent=False)
            if value_pf_obj:
              value = value_pf_obj    
        self.set_attr(obj, {attr: value})  

  def _handle_attribute_type_for_reading(
      self,
      obj,
      attr: str,
      pf_obj_handling="path",
      truncated_path=""):
    """
    Offers various ways to handle attributes which are PF objects when
    reading from the PF database.
    PF objects can be read as
      - a PF object (pf_obj_handling="original_pf_obj")
      - the path of the object (pf_obj_handling="path")
      
    Arguments:
      - obj: PF object
      - attr: Attribute of the object
      - pf_obj_handling: see above
      - truncated_path: If pf_obj_handling="path", then this truncated_path is truncated
    """
    attr_value = self.get_attr(obj,attr)
    if isinstance(attr_value, (str, int, float)) or not attr_value:
      return attr_value
    else: # Then it must be a PF object
      if pf_obj_handling == "path":
        if truncated_path:
          truncated_path = self.get_path_of_obj_with_class_names_relative_to_project(truncated_path)    
        return self.get_path_of_obj_with_class_names_relative_to_project(attr_value)
      elif pf_obj_handling == "original_pf_obj":
        return attr_value 


  # Todo: define standard class attributes
  def get_standard_class_attributes():
    return {
      "ElmTerm": ["Unom"]  
    }
  
  