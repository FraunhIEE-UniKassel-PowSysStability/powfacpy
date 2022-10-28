"""Contains the class PFBaseInterface (interaction with the PF database)
and the class PFStringManipuilation for string manipulation.

The abbreviation 'PF' is sometimes used for 'PowerFactory'.
"""

import sys
sys.path.insert(0,r'.\src')
import powfacpy
from os import path as os_path
from collections.abc import Iterable

# ToDo: get_active_networks, copy_graphics_pages

class PFBaseInterface:
  """Base interface for interaction with the PF database.
  """
  language = "en" 

  def __init__(self,app,language=None):  
    if app:
      self.app = app
    else:
      raise TypeError("The input app is of type 'NoneType'. Maybe the PowerFactory "
      "app was not loaded correctly.")  
    if not language:
      self.language = app.GetLanguage()
    else:
      self.language = language  

  def get_obj(self,path,condition=None,parent_folder=None,error_if_non_existent=True,
    include_subfolders=False):
    """Returns the PowerFactory object(s) under 'path'. 
    'path' can contain wildcards ("*") after the last "\". 
    A condition may be specified as a function, for example to check 
    certain attributes with lambda function:
      (eg. "condition = lambda x : getattr(x,"uknom")==110)".
    By default, the 'path' is relative to the folder of the active project.
    Only if 'parent_folder' is specified, it is relative to that folder.
    The parent_folder can be a PF container object or a string:
      parent_folder = "user" means 'path' is relative to the active user instead
      of the active project.
    An error is raised if no object is found, unless 'error_if_non_existent=False'.

    Examples:
      pfbi.get_obj("Network Model\\Network Data\\Grid\\Terminal 1")
    The path can also start with "\\" and contain wildcards after last "\\":
      get_obj("\\Network Model\\Network Data\\Grid\\*.ElmTerm")
    With condition:   
      pfbi.get_obj("Network Model\\Network Data\\Grid\\*.ElmTerm"",
        condition = lambda x : getattr(x,"uknom")==110)
    Search in folder of the active user (instead of in the active project):
      pfbi.get_obj("My project name", parent_folder="user")

    Note that you can also use r" at the beginning of the string
    argument to use single "\".  

    See also method 'get_single_obj'
    """
    if not parent_folder:
      parent_folder = self.get_active_project()
    else:
      parent_folder=self.handle_single_pf_object_or_path_input(parent_folder)  
    if not include_subfolders:
      try:  
        obj = parent_folder.GetContents(path)
      except(RuntimeError):
        raise TypeError("Path must be of type string.")
    else:
      obj = self.handle_inclusion_of_subfolders(path,parent_folder,error_if_non_existent)
    if not obj:
      return self.handle_non_existing_obj(path,parent_folder,error_if_non_existent)
    if condition:
      obj_with_condition = self.get_by_condition(obj,condition)
      if obj_with_condition:
        return obj_with_condition
      else:
        return self.handle_condition_of_obj_not_met(path,obj,error_if_non_existent)
    else:
      return obj    

  def handle_inclusion_of_subfolders(self,path,parent_folder,error_if_non_existent):
    """If subfolders are included, 'GetChildren' must
    be used instead of 'GetContents'. 'GetChildren'
    requires the input to be splitted between path and object name.
    """
    try:
      head,tail = os_path.split(path)
    except(TypeError):
      raise TypeError("Path must be of type string")  
    if head:
      new_parent_folder = parent_folder.GetContents(head)
      if new_parent_folder:
        parent_folder = new_parent_folder[0]
      else:
        return self.handle_non_existing_obj(head,parent_folder,error_if_non_existent)
    return parent_folder.GetChildren(1,tail,1)

  def get_single_obj(self,path,parent_folder=None,error_if_non_existent=True):
    """Use this method if you want to access one single unique object.
    This method is an alterntive to 'get_obj' and returns the unique object instead
    of a list (that needs to be accessed with '[0]').
    """
    obj = self.get_obj(path,parent_folder=parent_folder,
      error_if_non_existent=error_if_non_existent)
    if obj:
      if len(obj) < 2:
        return obj[0]
      else:
        raise TypeError(f"The path {path} is not a unique object. Did you use wildcards ('*')?" 
          "This method only returns single unique objects.")
    else:
      return None      

  def get_multiple_obj_from_similar_sub_directories(self,parent_folders,sub_path):
    """Returns multiple objects that are in a similar subdirectory relativ to
    their parent folders.
    Arguments:
      parents: Parent folders (string path,list of objects/string paths)
      sub_path: Path within the parent folders (string). Must be unique (don't
        use placeholders '*')

    Example:
      If you want to get the "All calculation" objects of all the study cases 
      in the study case folder, use
        self.get_multiple_obj_from_similar_sub_directories(
          r"Study Cases\*","All calculations")     
    """
    if isinstance(parent_folders,str):
      parent_folders = self.get_obj(parent_folders)
    objs = []  
    for parent in parent_folders:
      parent = self.handle_single_pf_object_or_path_input(parent)
      objs.append(self.get_single_obj(sub_path,parent_folder=parent))
    return objs
    
  def handle_non_existing_obj(self,path,parent_folder,error_if_non_existent):
    """Handles the attempted access to a non existent object.
    """
    if not error_if_non_existent:
      return []
    else:
      exists_bool,existing_path,non_existing_child = self.path_exists(
        path,parent_folder,return_info=True)
      raise powfacpy.PFPathError(non_existing_child,existing_path)

  def handle_condition_of_obj_not_met(self,path,obj,error_if_non_existent):
    """Handles the attempted access to an object with a certain condition
    that does not exist.
    """
    if not error_if_non_existent:
      return []
    else:
      head,tail = os_path.split(path)
      raise powfacpy.PFNonExistingObjectError(obj[0].GetParent(),tail,condition=True)

  def get_first_level_folder(self,folder):
    """Returns folder on first level of PF database.
    Currently the folder of the active user ('folder'='user') 
    or the global library ('folder'='global library') can be accessed.
    """
    if folder == "user":
      return self.get_active_user_folder()
    elif folder == "global library": 
      return self.app.GetGlobalLibrary()
    else:
      raise TypeError(f"The first level folder {folder} is not valid. " 
       "Use one of these: 'user', 'global library'.")  

  def path_exists(self,path,parent=None,return_info=False):
    """Check if the path exists.
    By default, it is searched in the folder of the active project
    If 'parent' is specified it is searched relative to that folder.
    If 'return_info' is True, information about where the path is
    corrupted is returned. 
    """
    if not parent:
      parent = self.get_active_project()
    else:
      parent = self.handle_single_pf_object_or_path_input(parent)
    splitted_path = path.split('\\')
    if path[0] == "\\" or not splitted_path:
      raise powfacpy.PFPathInputError(path)
    existing_path=""
    child = parent
    for child_name in splitted_path:
      child = child.GetContents(f"{child_name}")
      if child:
        child = child[0]
        existing_path = f"{existing_path}\{child.loc_name}"
      else: 
        if not return_info:
          return False
        else:
          parent_path = parent.GetFullName()
          parent_path = PFStringManipuilation.delete_classes(parent_path)
          existing_path = f"{parent_path}{existing_path}" 
          non_existent_child_name = child_name
          return False,existing_path,non_existent_child_name
    return True    

  def get_active_project(self):
    """Returns the currently active project and throws an
    error if no prject has been activated.
    """
    active_project = self.app.GetActiveProject()
    if active_project:
      return active_project
    else:
      raise powfacpy.PFNotActiveError("a project")

  def get_active_user_folder(self):
    """Return the folder of the active user.
    """
    parent = self.get_active_project()
    while not parent.GetClassName() == "IntUser":
      parent = parent.GetParent()
    return parent  

  def get_active_networks(self,error_if_no_network_is_active=True):
    """Get active networks/grids.  
    """
    grids = self.app.GetCalcRelevantObjects(".ElmNet") # This also returns the summary grid in the study case
    # Delete the summary grid which is in the study case
    grids[:] = [grid for grid in grids if not grid.GetParent().GetClassName() == "IntCase"]  
    if error_if_no_network_is_active and not grids:
      raise PFNotActiveError("a network (ElmNet).")
    return grids  

  def get_by_condition(self,objects,condition):
    """From a list of objects, get those for whom the 'condition' 
    (which is a function) returns 'True'.
    Example:
      pfbi.get_by_condition(list_of_objects,lambda x : getattr(x,"uknom")==110)
    """
    objects_true = []
    for obj in objects:
      try:
        # This anonymous function is problematic because it does
        # not always throw an error when it the user provided
        # an anonymous function that does not make sense.
        if condition(obj):
          objects_true.append(obj)
      except(AttributeError) as e:
        raise powfacpy.PFAttributeError(obj,e,self)
      except(TypeError) as e:
        object_str = powfacpy.PFStringManipuilation.format_full_path(str(obj),self)
        raise TypeError(f"{e}. Maybe an unexpected type is used "
          f"for attribute of object '{object_str}'.")  
    return objects_true
  
  def get_path_of_object(self,obj):
    return PFStringManipuilation.format_full_path(str(obj),self)

  def get_attr(self,obj,attr,parent_folder=None):
    """Get the value of an attribute of an object.
    'obj' can be a path (string) or a Powerfactory object.
    If parent_folder is specified, the path is relative to 
    this folder.

    Example:
     pfbi.get_attr(terminal_1,"systype")
    """
    if isinstance(obj,str):
      obj = self.get_single_obj(obj,parent_folder=parent_folder)
    try:
      if not isinstance(attr, list):
        return obj.GetAttribute(attr)
      else:
        attr_values = dict()
        for attribute in attr:
          attr_values[attribute]=obj.GetAttribute(attribute)
        return attr_values
    except(AttributeError) as e:
      raise powfacpy.PFAttributeError(obj,e,self)

  def get_attr_by_path(self,path_with_attr):
    head_tail = os_path.split(path_with_attr)
    return self.get_attr(head_tail[0],head_tail[1])

  def set_attr(self,obj,params,parent_folder=None):
    """
    Set the attribute(s) of an object. 
    obj: PowerFactory object or its path (string).
    If 'parent_folder' is specified, the path is relative to 
    this folder.
    params: dictionary {parameter1:value1, parameter2:value2,..}.
    """
    if isinstance(obj,str):
      obj = self.get_single_obj(obj,parent_folder=parent_folder)
    for attr, value in params.items():
      try:
        obj.SetAttribute(attr,value)
      except(TypeError) as e:
        raise powfacpy.PFAttributeTypeError(obj,attr,e,self)
      except(AttributeError) as e:
        raise powfacpy.PFAttributeError(obj,e,self)

  def set_attr_by_path(self,path_with_attr,value):
    """
    path_with_attr: path of object plus the attribute name
    Example:
      pfbi.set_attr_by_path(self,
        "Library\\Dynamic Models\\Linear_interpolation\\desc",["description"])
      Here 'desc' is the name of the attribute.  
    """
    head_tail = os_path.split(path_with_attr)
    self.set_attr(head_tail[0],{head_tail[1]:value})

  def create_by_path(self,path,overwrite=True):
    """Create an object by specifying its path including its class and return the object.
    If overwrite is true, objects with the same name will be overwritten.
    Example:
      pfbi.create_by_path(r"Library\Dynamic Models\dummy.BlkDef") 
    """
    try:
      folder_path, obj_name_incl_class = path.rsplit('\\',1)
    except(AttributeError):
      raise TypeError("The argument 'path' must be of type string.")
    folder = self.get_single_obj(folder_path)
    return self.create_in_folder(folder,obj_name_incl_class,overwrite=overwrite)
  
  def create_in_folder(self,folder,obj,overwrite=True):
    """Creates an obj inside a folder and returns the object.
    If overwrite is true, objects with the same name will be overwritten.
    Example:
      pfbi.create_in_folder("Library\\Dynamic Models","dummy2.BlkDef")
    """
    folder = self.handle_single_pf_object_or_path_input(folder)
    try:
      obj_name, class_name = obj.split('.')
    except(AttributeError):
      raise TypeError("The argument 'obj' must be of type string.")
    if overwrite:
      self.delete_obj(obj,parent_folder=folder,error_if_non_existent=False)
    return folder.CreateObject(class_name, obj_name)

  def create_directory(self,directory,parent_folder=None):
    """Create a directory of folders ('IntFolder') if the 
    directory does not yet exist.
    Arguments:
      path: path of folders
      parent_folder: If not specified, the active project folder
        is used.

    Returns the folder in the lowest subdirectory.  
    """
    if not self.path_exists(directory,parent=parent_folder):
      if parent_folder:
        folder = parent_folder
      else:
        folder = self.app.GetActiveProject()
      folder_names = directory.split("\\")
      for folder_name in folder_names:
        if not self.path_exists(folder_name,parent=folder):
          folder = self.create_in_folder(folder,folder_name+".IntFolder")
        else:
          folder = self.get_single_obj(folder_name,parent_folder=folder)
      return folder     
    else:
      return self.get_single_obj(directory,parent_folder=parent_folder)      
         

  def delete_obj(self,obj_or_path,condition=None,parent_folder=None,error_if_non_existent=True,
    include_subfolders=False):
    """Delete object(s). In a first step, the objects are loaded using the `get_obj`
    method. In a second step, they are deleted. For further info on the input 
    arguments, see the `get_obj` method. 
    """
    obj = self.handle_pf_object_or_path_input(obj_or_path,
      condition=condition,
      parent_folder=parent_folder,
      error_if_non_existent=error_if_non_existent,
      include_subfolders=include_subfolders)
    for o in obj:
      success = o.Delete()
      """
      if not success == 0:
        o.Deactivate()
        o.Delete()
      # Due to a PF bug, study cases need special treatment.
      # Here, Delete() returns 0 even if it was not successful.  
      elif o.GetClassName() == "IntCase":
        try:
          o.Deactivate()
          o.Delete()
        except:
          pass  
      """
      if not o.IsDeleted():
        try:
          o.Deactivate()
          o.Delete()
        except:
          pass

  def handle_pf_object_or_path_input(self,obj_or_path,condition=None,parent_folder=None,
    error_if_non_existent=True,include_subfolders=False):
    """Handles the input argument when a method accepts either
      - a path string
      - a PF object
      - an iterable (of PF objects) 

    Returns the PF object(s) in a list.
    If 'obj' is a path string, it returns the PF object(s) of that path.
    If 'obj' is a PF object (or multiple), it does nothing and just returns 
    the object(s).

    Note: Unfortunately, it cannot be checked whether 'obj' is a PF DataObject, 
    because the module powerfactory is not available.
    
    See also method 'handle_single_pf_object_or_path_input'
    """
    if isinstance(obj_or_path,str):
      return self.get_obj(obj_or_path,condition=condition,
        parent_folder=parent_folder,
        error_if_non_existent=error_if_non_existent,
        include_subfolders=include_subfolders)
    elif not isinstance(obj_or_path,Iterable):
      return [obj_or_path]
    else: # If all former conditions are False, it is assumed that the
      # input already was a list of PF object(s). 
      return obj_or_path

  def handle_single_pf_object_or_path_input(self,obj,parent_folder=None,
    error_if_non_existent=True):
    """Handles the input argument when a method accepts either
      - a path string
      - or a PF object
      - but NOT an iterable of PF objects

    If 'obj' is a path string, it returns the PF object of that path.
    If 'obj' is a PF object, it does nothing and just returns the object.
    If 'obj' is an iterable (unexpected), a meaningfull error message is provided.

    Note: Unfortunately, it cannot be checked whether 'obj' is a PF DataObject, 
    because the module powerfactory is not available.

    See also method 'handle_pf_object_path_input'
    """    
    if isinstance(obj, str):
      return self.get_single_obj(obj,parent_folder=parent_folder,
        error_if_non_existent=error_if_non_existent)
    elif isinstance(obj, Iterable):
      elements_count = len(obj)
      first_obj_type = type(obj[0])
      try:
        first_obj_path = self.get_path_of_object(obj[0])
        msg_obj = (f"The first element is of type {first_obj_type} and its "
          f"path is {first_obj_path}.")
      except(AttributeError):
        msg_obj = f"The first element is of type {first_obj_type}." 
      msg = (f"Expected a PowerFactory object or a path string. Instead an "
        f"iterable of length {elements_count} is given. {msg_obj}")
      raise TypeError(msg)
    else: # If all former conditions are False, it is assumed that the
      # input already was a PF object.
      return obj

  def copy_obj(self,obj_or_path,target_folder,overwrite=True,condition=None,
    parent_folder=None,error_if_non_existent=True,include_subfolders=False):
    """Copies object(s) by using 'get_obj' in first step and the copying 
    the returned objects to 'target_folder'.
    The argument 'parent_folder' refers to the source folder and is used in
    combination with 'obj_or_path' to get the object(s) to be copied.
    If 'overwrite' is True, existing objects wit the same name are overwritten
    in the target folder.
    For further information on the input arguments, see method 'get_obj'.

    Returns a list of the created copy/copies.

    See also 'copy_single_obj'
    """
    obj = self.handle_pf_object_or_path_input(obj_or_path,
      condition=condition,
      parent_folder=parent_folder,
      error_if_non_existent=error_if_non_existent,
      include_subfolders=include_subfolders)
    target_folder = self.handle_single_pf_object_or_path_input(target_folder)
    if overwrite:
      for object_to_be_copied in obj:
        self.delete_obj(object_to_be_copied.GetAttribute("loc_name"),
          parent_folder=target_folder,error_if_non_existent=False)
    target_folder.AddCopy(obj)
    if isinstance(obj,Iterable):
      return obj
    else:
      return [obj]

  def copy_single_obj(self,obj_or_path,target_folder,overwrite=True,
    new_name=None,parent_folder=None,error_if_non_existent=True):
    """Copies single object by using 'get_single_obj' in first step and the copying 
    the returned objects to 'target_folder'.
    The argument 'parent_folder' refers to the source folder and is used in
    combination with 'obj_or_path' to get the object(s) to be copied.
    If 'overwrite' is True, existing objects wit the same name are overwritten
    in the target folder.
    A 'new_name' can be provided (in contrast to method 'copy_obj').
    For further information on the input arguments, see methods 'get_obj' or
    'get_single_obj'.

    Returns a list of the created copy.

    See also 'copy_obj'
    """
    obj = self.handle_single_pf_object_or_path_input(obj_or_path,
      parent_folder=parent_folder,
      error_if_non_existent=error_if_non_existent)
    target_folder = self.handle_single_pf_object_or_path_input(target_folder)
    if overwrite:
      if not new_name:
        self.delete_obj(obj.GetAttribute("loc_name"),
          parent_folder=target_folder,error_if_non_existent=False)
      else:
        self.delete_obj(f"{new_name}.*",
          parent_folder=target_folder,error_if_non_existent=False)
    if new_name: 
      return target_folder.AddCopy(obj,new_name)
    else:
      return target_folder.AddCopy(obj)
  
  def is_container(self,obj):
    """Checks whether a PF object is a container. It is assumed
    that an object is a container if it has the attribute 'contents'.
    """
    obj = self.handle_single_pf_object_or_path_input(obj)
    return obj.HasAttribute("contents")

  def activate_study_case(self, path):
    """Activate study case under path.
    """
    study_case = self.get_single_obj(path)
    study_case.Activate()

  def add_results_variable(self,obj,variables,results_obj=None):
    """Adds variables of the object to the PowerFactory results object (ElmRes)
    obj: PowerFactory object or its path
    """
    if not results_obj:
      results_obj_name = powfacpy.PFTranslator.get_default_result_object_name(self.language)
      results_obj = self.app.GetFromStudyCase(results_obj_name)
    else:
      results_obj = self.handle_single_pf_object_or_path_input(results_obj)
    obj = self.handle_single_pf_object_or_path_input(obj)
    if isinstance(variables, str):
      variables = [variables]
    for var in variables:
      results_obj.AddVariable(obj,var)
    results_obj.Load()

  def get_parameter_value_string(self,parameters,delimiter=" "):
    param_value_string = ""
    for parname,path_with_par in parameters.items():
        value = self.get_attr_by_path(path_with_par)
        param_value_string += parname + "=" + str(value) + delimiter
    return param_value_string[:-len(delimiter)] # omit last delimiter

class PFStringManipuilation:
  
  @staticmethod
  def replace_between_characters(char1,char2,replacement,string):
    new_string = ""
    is_between_chars = False
    for c in string:
      if c == char1:
        is_between_chars = True
      elif c == char2 and is_between_chars:
        is_between_chars = False
        new_string = new_string + replacement
      elif not is_between_chars:
        new_string = new_string + c
    return new_string   

  @staticmethod
  def delete_classes(path):
    return PFStringManipuilation.replace_between_characters('.','\\','\\',path)

  @staticmethod
  def format_full_path(path,pf_interface):
    """
    Takes the full path (including user and project) and returns the path 
    relative to the currently active project.
    Example:
      input path:  \\username.IntUser\\powfacpy_base.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\Grid.ElmNet\\Terminal 1.ElmTerm
      output: Network Model\\Network Data\\Grid\\Terminal 1 
    """
    project_name = pf_interface.app.GetActiveProject().loc_name + '.IntPrj\\'
    path = path[path.find(project_name)+len(project_name):]
    return PFStringManipuilation.delete_classes(path)
  
  @staticmethod
  def handle_path(path):
    try:
      if not path[0] == "\\":
        return path
      else:
        return path[1:] 
    except(TypeError):
      raise TypeError("Path must be of type string.")

class PFTranslator:

  @staticmethod
  def get_default_result_object_name(language):
    if language == "en":
      return "All calculations.ElmRes"
    elif language == "de":
      return "Alle Berechnungsarten.ElmRes"

  @staticmethod
  def get_default_graphics_board_name(language):
    if language == "en":
      return "Graphics Board.SetDesktop"
    elif language == "de":
      return "Grafiksammlung.SetDesktop"

  @staticmethod
  def get_default_study_case_folder_name(language):
    if language == "en":
      return "Study Cases.IntPrjfolder"
    elif language == "de":
      return "Berechnungsfälle.IntPrjfolder"

  @staticmethod
  def get_default_operation_scenario_folder_path(language):
    if language == "en":
      return r"Network Model\Operation Scenarios"
    elif language == "de":
      return r"Netzmodell\Betriebsfälle"  

  @staticmethod
  def get_default_variations_folder_path(language):
    if language == "en":
      return r"Network Model\Variations"
    elif language == "de":
      return r"Netzmodell\Varianten"      



if __name__ == "__main__":
  print("ok")
  