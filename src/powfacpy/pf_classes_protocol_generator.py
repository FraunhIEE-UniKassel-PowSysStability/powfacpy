"""
Create protocoll classes for all python classes in the PF python scripting reference pdf file (by running this python module). See output module 'pf_class_protocols' which is used in powfacpy. If you run this module a new module is created ('pf_class_protocols_new'). You can then delete the old one and rename the new file. 

IMPORTANT: If you miss a class please add it to the 'missing_classes_that_are_not_in_scripting_reference' list below.


This module is not used by other modules of powfacpy and has the sole purpose of creating the protocols.
"""

missing_classes_that_are_not_in_scripting_reference = ["IntFolder", "ElmSite", "ComVstab", "ComMod", "ElmSecctrl", "ElmLod", "ElmIac", "ElmLodlv", "ElmLodmv", "ElmSind", "ElmVsc", "ElmVscmono", "ElmZpu"]


import os 
import keyword
import sys
import json

powfacpy_directory = os.path.dirname(os.path.abspath(__file__)).replace(r"\src\powfacpy","")

sys.path.insert(0, powfacpy_directory + r'\src')
import powfacpy 


class Empty:
  """This empty class is used to get the generic attributes that every python object has (e.g. using 'dir(class_instance)'). 
  For the PF class protocols, these attributes are not added to the protocol classes of the PowerFactory objects."""
  pass


class PFClassesProtocolGenerator(powfacpy.PFActiveProject):
  """Generate protocol classes for PF classes from the PF python scripting reference.
  """
  def __init__(self, app):
    super().__init__(app)
    self.indentation_increment:str = "  "
    self.general_methods = self.get_general_methods()

  
  def create_pf_class_protocols(self) -> None:
    """Main method of this class. 
    """
    pf_class_names = pfcpg.get_all_class_names_from_scripting_reference()
    pf_class_names += missing_classes_that_are_not_in_scripting_reference
    pf_class_objects, pf_class_objects_not_found, project = pfcpg.get_pf_objects(pf_class_names) # pf_class_objects_not_found is used only for debugging
    try:
      self.app.Hide() 
      with open(".\\src\\powfacpy\\pf_class_protocols_new.py", 'w') as out_file:
        out_file.write("\"\"\"Protocol classes for (almost) all PowerFactory classes in the python scripting reference pdf file. Protocol classes are helpful for example for type hints where they can be used just like 'normal' implementations of classes.\n\"\"\"\n\n")
        out_file.write("from typing import Protocol\n\n")
        out_file.write(self.get_general_class_string())
        for pf_obj in pf_class_objects:
          definition:str = pfcpg.get_class_definition(pf_obj)
          out_file.write(definition)
          data_attributes, methods = pfcpg.get_class_attribute_definitions(pf_obj)
          out_file.write(data_attributes + "\n\n")     
          out_file.write(methods + "\n\n") 
    finally:
      project.Deactivate()
      project.Delete()
      self.app.Show()
            
  
  def get_all_class_names_from_scripting_reference(self) -> list[str]:
    """Uses a .txt file to which the TOC of the python scripting reference pdf document was copied (includes the class names).
    Iterates all words from the TOC and checks if they are PF class names.

    Returns:
        list[str]: PF class names
    """
    pf_class_names = []
    with open(powfacpy_directory + r"\power_factory_objects\CopyOfObjectsInTableOfContentsOfScriptingReference.txt", 'r') as in_file:
      for line in in_file:
        words = line.split()
        for word in words:
          if self.is_pf_class(word):
            pf_class_names.append(word)
    return pf_class_names
  
  
  def get_pf_objects(self, pf_class_names: list[str]) -> list:
    """Get instances of the PF classes in 'pf_class_names'.
    
    Creates a new project and tries to create each class in one of the folders in the project. Some objects can only be created insided certain folders. Hence, the procedure is done twice to ensure that the folders are present (i.e. create folders in first run, use those folders to create the specific objects in the second run).
    Finally, further objects that cannot be created in this way are added.

    Args:
        pf_class_names (list[str]): _description_

    Returns:
        pf_class_objects: list of powerfactory class instances/objects
        pf_class_objects_not_found: list of objects that could not be found/created
    """
    try:
      self.app.Hide() # for performace
      project = self.app.CreateProject("delete_this_project","grid")
      project.Activate()
      
      for n in range(2):
        folders = self.get_obj("*", include_subfolders=True)
        pf_class_objects = []
        pf_class_objects_not_found = [] 
        for pf_class in pf_class_names:
          for folder in folders:
            pf_class_obj = self.create_in_folder("new."+pf_class, folder)
            if pf_class_obj: 
              break # break loop when successfully created an object
          if not pf_class_obj:
            pf_class_objects_not_found.append(pf_class) 
          else:
            pf_class_objects.append(pf_class_obj) 
      # Insert some further objects        
      pf_class_objects.insert(0,self.app) 
      pf_class_objects.append(project)
      pf_class_objects_not_found.remove(pf_class_objects[-1].GetClassName())
      pf_class_objects.append(self.get_active_user_folder())
      pf_class_objects_not_found.remove(pf_class_objects[-1].GetClassName())
      pf_class_objects.append(self.get_first_level_folder("global library"))
      pf_class_objects_not_found.remove(pf_class_objects[-1].GetClassName())
    finally:
      self.app.Show()
    return pf_class_objects, pf_class_objects_not_found, project


  def get_class_definition(self, pf_obj) -> str:
    """Get string with the definition of a protocol class for a PF object. 
    Example: 'class ElmTr2(Protocol):'

    Args:
        pf_obj: PF object

    Returns:
        str: class definition
    """
    definition:str = ""
    if not isinstance(pf_obj, type(self.app)):
      class_name = pf_obj.GetClassName()
      definition += "class "+ class_name + "(PFGeneral):\n"
    else:
      class_name = "PFApp"  
      definition += "class "+ class_name + "(Protocol):\n"
    
    if hasattr(pf_obj, "GetClassDescription"):
      class_description = self.app.GetClassDescription(class_name) # It seems that GetClassDescription always retuns an empty string for every class
      if class_description:
        definition += self.indentation_increment + "\"\"\"" + class_description + "\"\"\"\n\n"
    return definition    
            

  def get_class_attribute_definitions(self, pf_obj) -> str:
    """Get definitions of class attributes (data attributes and methods) of a PF object.

    Args:
        pf_obj: PF object

    Returns:
        str: definitions of all attributes of the class of the object
    """
    class_attributes:set = set(dir(pf_obj)) - set(dir(Empty)) - self.general_methods # omit attributes that all python objects have and general methods.
    class_attributes = sorted(class_attributes)
    data_attributes = ""
    methods = ""
    for attr in class_attributes:
      # In rare cases, the attributes are named after python keywords - such names are not allowed in python classes and are omitted.
      if hasattr(pf_obj,attr) and not keyword.iskeyword(attr): 
        if callable(getattr(pf_obj,attr)):
          # Due to lack of knowledge about the method arguments, the generic '(*args)' is used.
          methods += self.indentation_increment + "def " + attr + "(*args):\n" + 2*self.indentation_increment + "...\n\n"
        else:
          attribute_value = getattr(pf_obj,attr)
          attribute_type = type(attribute_value).__name__
          # The types "DataObject", "NoneType" are replace with 'object'
          # "DataObject" is replaced because powfacpy should not depend on an import of the powerfactory module (which is necessary for this type hint)
          # "NoneType" is not a helpful information 
          if not attribute_type in ["DataObject", "NoneType"]:
            data_attributes += self.indentation_increment + attr + ": " + attribute_type + "\n"
          else:   
            data_attributes += self.indentation_increment + attr + ": object\n"
          if not isinstance(pf_obj, type(self.app)):
            attribute_description = pf_obj.GetAttributeDescription(attr)
            if attribute_description:
              # some characters need to be deleted (newlines, '\xb0' is not a unicode symbol)
              attribute_description = attribute_description.replace("\n","").replace("\"","").replace('\xb0',"")
              data_attributes += self.indentation_increment + "\"" + attribute_description + "\"\n"
    return data_attributes, methods
  
  
  def get_general_class_string(self):
    """Add class with 'general methods' (see Section 'General Methods' in scripting reference). All other classes (except for PFApp) inherit from this class. 
    """
    class_str = f"class PFGeneral(Protocol):\n{self.indentation_increment}\"\"\"Class with general methods (see Section 'General Methods' in scripting reference. All other methods (except for PFApp) inherit from this class). \n{self.indentation_increment}\"\"\"\n"
    for method in self.get_general_methods():
      class_str += self.indentation_increment + "def " + method + "(*args):\n" + 2*self.indentation_increment + "...\n\n"
    return class_str
    
  
  def get_general_methods(self):
    """General methods from python scripting reference."""
    general_methods = "AddCopy ContainsNonAsciiCharacters CopyData CreateObject Delete Energize GetAttribute GetAttributeDescription GetAttributeLength GetAttributes GetAttributeShape GetAttributeType GetAttributeUnit GetChildren GetClassName GetCombinedProjectSource GetConnectedElements GetConnectionCount GetContents GetControlledNode GetCubicle GetFullName GetImpedance GetInom GetNode GetOperator GetOwner GetParent GetReferences GetRegion GetSupplyingSubstations GetSupplyingTransformers GetSupplyingTrfstations GetSystemGrounding GetUnom GetZeroImpedance HasAttribute HasResults IsCalcRelevant IsDeleted IsEarthed IsEnergized IsHidden IsInFeeder IsNetworkDataFolder IsNode IsObjectActive IsObjectModifiedByVariation Isolate IsOutOfService IsReducible IsShortCircuited MarkInGraphics Move PasteCopy PurgeUnusedObjects ReplaceNonAsciiCharacters ReportNonAsciiCharacters ReportUnusedObjects SearchObject SetAttribute SetAttributeLength SetAttributes SetAttributeShape ShowEditDialog ShowModalSelectTree SwitchOff SwitchOn WriteChangesToDb"
    return set(general_methods.split())


if __name__ == "__main__": 
  with open(powfacpy_directory + '\\settings.json') as settings_file:
    settings = json.load(settings_file)
  sys.path.append(settings["local path to PowerFactory application"])
  import powerfactory
  app = powerfactory.GetApplication()
  pfcpg = PFClassesProtocolGenerator(app)
  pfcpg.create_pf_class_protocols()
