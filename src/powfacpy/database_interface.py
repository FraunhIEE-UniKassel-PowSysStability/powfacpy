import sys
sys.path.insert(0, r'.\src')
import powfacpy
from fnmatch import fnmatchcase

class PFDatabaseInterface(powfacpy.PFBaseInterface):
  language = powfacpy.PFBaseInterface.language
  
  def __init__(self, app):
    super().__init__(app)

  def get_object_attributes(
      self,
      objs,
      class_attributes: dict = None,
      relative_path: str = "") -> dict:
    """
    
    """
    if not class_attributes:
      class_attributes = {"*":[]}
    if relative_path:
      relative_path = self.get_path_of_obj_with_class_names_relative_to_project(relative_path)  
    
    obj_attr_dict = {}
    for obj in objs:
      obj_path = self.get_path_of_obj_with_class_names_relative_to_project(obj)
      if relative_path:
        obj_path = obj_path[obj_path.find(relative_path)+len(relative_path)+1:]
      obj_attr_dict[obj_path] = {}
      for class_name in class_attributes.keys():
        if fnmatchcase(obj.GetClassName(), class_name):
          for attr in class_attributes[class_name]:
            obj_attr_dict[obj_path][attr] = self._handle_attribute_type_for_reading(obj,attr)
    return obj_attr_dict
  
  def set_object_attributes(
      self,
      obj_attr_dict: dict,
      relative_path: str = ""):
    """
    
    """
    for obj, attr_key_val in obj_attr_dict.items():
      if relative_path:
        obj = relative_path + "\\" + obj
      obj = self.get_unique_obj(obj)
      for attr, value in attr_key_val.items():
        if isinstance(value, str):
          if not isinstance(obj.GetAttributeType(attr), str):
            print(attr)
            print(value)
            value_pf_obj = self.get_unique_obj(value, error_if_non_existent=False)
            
            if value_pf_obj:
              print(value_pf_obj)
              value = value_pf_obj 
              
        self.set_attr(obj, {attr: value})  

  def _handle_attribute_type_for_reading(
      self,
      obj,
      attr,
      pf_obj_handling="path",
      relative_path=""):
    attr_value = self.get_attr(obj,attr)
    if isinstance(attr_value, (str, int, float)) or not attr_value:
      return attr_value
    else:
      if pf_obj_handling == "path":
        if relative_path:
          relative_path = self.get_path_of_obj_with_class_names_relative_to_project(relative_path)    
        return self.get_path_of_obj_with_class_names_relative_to_project(attr_value)
      elif pf_obj_handling == "original_pf_obj":
        return attr_value 
      
  def get_standard_class_attributes():
    return {
      "ElmTerm": ["Unom"]  
    }