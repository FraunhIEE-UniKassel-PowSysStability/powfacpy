"""Custom exceptions for powfacpy.
"""
import sys
sys.path.insert(0,r'.\src')
import powfacpy

class PFInterfaceError(Exception):
  """There should always be a base class (that inherits
  from 'Exception') for all custom errors/exceptions.
  """
  pass

class PFAttributeError(PFInterfaceError):
  """Attempt to access an invalid attribute of a PF object.
  """
  def __init__(self,obj,msg_raised,pf_base_interface):
    object_str = powfacpy.PFStringManipulation._format_full_path(str(obj),pf_base_interface)
    self.message = (f"Unexpected attribute of object '{object_str}': {msg_raised}.")
    super().__init__(self.message)

class PFAttributeTypeError(PFInterfaceError):
  """Attempt to set an invalid type for the attribute of a PF object.
  """
  def __init__(self,obj,attr,msg_raised,pf_base_interface):
    object_str = powfacpy.PFStringManipulation._format_full_path(str(obj),pf_base_interface)
    self.message = (f"The attribute '{attr}' of the object '{object_str}' "
      f"is of unexpected type: {msg_raised}.")
    super().__init__(self.message)

class PFPathError(PFInterfaceError):
  """Attempt to access invalid path in PF database.
  """
  def __init__(self,non_existing_child,existing_path):
    self.message = f"'{non_existing_child}' does not exist in '{existing_path}'"
    super().__init__(self.message)

class PFPathInputError(PFInterfaceError):
  """Invalid input for a PF path.
  """
  def __init__(self,path):
    self.message = (f"The path '{path}' is invalid or empty. Please don't start " +
    f"the path with '\\'.")
    super().__init__(self.message)

class PFNonExistingObjectError(PFInterfaceError):
  """Attempt to access PF object that does not exist.
  """
  def __init__(self,folder,obj,condition=False,include_subfolders=False):
    folder_str = powfacpy.PFStringManipulation.delete_classes(str(folder))
    if include_subfolders:
      msg_subfolder = " (and its subfolders)"
    else:
      msg_subfolder = ""
    msg = (f"The folder '{folder_str}'{msg_subfolder} does not contain "
      f"any object named '{obj}'")
    if condition:
      msg = msg + " with specified condition"  
    self.message = msg
    super().__init__(self.message)

class PFNotActiveError(PFInterfaceError):
  """Unexpected inactive PF object.
  """
  def __init__(self,obj_str):
    self.message = (f"Please activate {obj_str}.")
    super().__init__(self.message)

class PFAttributeNotSetError(PFInterfaceError):
  """Attempt to access an attribute of a powfacpy class,
  but it was not specified.
  """ 
  def __init__(self,attribute_description):
    self.message = (f"Attempt to access {attribute_description}, " 
    "but it was not set.")
    super().__init__(self.message)

class PFCaseStudyParameterValueDefinitionError(PFInterfaceError):
  """Number of parameter values is not the same for every parameter. 
  """
  def __init__(self,par_name,values):
    self.message = (f"Incorrect number of values defined for parameter '{par_name}'. "
    f"Only {len(values)} values were defined.")
    super().__init__(self.message)