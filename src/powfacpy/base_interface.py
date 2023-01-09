"""Contains the class PFBaseInterface (interaction with the PF database)
and the class PFStringManipuilation for string manipulation.

The abbreviation 'PF' is sometimes used for 'PowerFactory'.
"""

from argparse import ArgumentError
import sys

from powfacpy.exceptions import PFNotActiveError
sys.path.insert(0,r'.\src')
import powfacpy
from os import path as os_path
from collections.abc import Iterable
from os import getcwd, replace
import math

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
    self.export_dir = None

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
    'attr' can be a string or a list of strings.
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
  
  def create_in_folder(self,folder,obj,overwrite=True,use_existing=False):
    """Creates an obj inside a folder and returns the object.
    If overwrite is true, objects with the same name will be overwritten.
    If use_existing is True, objects with the same name are not replaced.
    If overwrite and use_existing are false and an object with the same name
    exists, a new object with "(1)"/"(2)".. in name is created.
    Example:
      pfbi.create_in_folder("Library\\Dynamic Models","dummy2.BlkDef")
    """
    folder = self.handle_single_pf_object_or_path_input(folder)
    try:
      obj_name, _, class_name = obj.rpartition('.')
    except(AttributeError):
      raise TypeError("The argument 'obj' must be of type string.")
    if overwrite:
      self.delete_obj(obj,parent_folder=folder,error_if_non_existent=False)
    elif use_existing:
      existing_obj = self.get_single_obj(obj,parent_folder=folder,error_if_non_existent=False)
      if existing_obj:
        return existing_obj 
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
    It is also checked whether the object was really deleted, otherwise it is tried
    to deactivate the object and then delete it.
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
      # 'IsDeleted' seems to be the savest way to check whether an object has been deleted. 
      if not o.IsDeleted():
        try:
          o.Deactivate()
          o.Delete()
        except:
          raise ArgumentError(r"Object {o} cannot be deleted.")
        if not o.IsDeleted():  
          raise ArgumentError(r"Object {o} cannot be deleted.")

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
    """Copies object(s) by using 'get_obj' in first step and then copying 
    the returned objects to 'target_folder'.
    The argument 'parent_folder' refers to the source folder and is used in
    combination with 'obj_or_path' to get the object(s) to be copied.
    If 'overwrite' is True, existing objects with the same name are overwritten
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
    """Copies single object by using 'get_single_obj' in first step and then copying 
    the returned object to 'target_folder'.
    The argument 'parent_folder' refers to the source folder and is used in
    combination with 'obj_or_path' to get the object to be copied.
    If 'overwrite' is True, existing objects with the same name are overwritten
    in the target folder.
    A 'new_name' can be provided (in contrast to method 'copy_obj').
    For further information on the input arguments, see methods 'get_obj' or
    'get_single_obj'.

    Returns the created copy.

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
    return study_case

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

  def clear_elmres_from_objects_with_status_deleted(self,results_obj=None):
    """Deletes all objects from a results object (ElmRes) that have the
    status deleted (i.e. attribute 'obj_id' is deleted).
    """
    if not results_obj:
      results_obj = self.app.GetFromStudyCase("ElmRes")
    obj_in_elmres = results_obj.GetContents("*")
    for o in obj_in_elmres:
      obj_id = o.obj_id
      if obj_id.IsDeleted():
          o.Delete()

  def get_parameter_value_string(self,parameters,delimiter=" "):
    param_value_string = ""
    for parname,path_with_par in parameters.items():
        value = self.get_attr_by_path(path_with_par)
        param_value_string += parname + "=" + str(value) + delimiter
    return param_value_string[:-len(delimiter)] # omit last delimiter

  def export_to_csv(self,
    dir=None,
    file_name=None,
    results_obj=None,
    results_variables_lists=None):
      """Exports simulation results to csv.
      Arguments:
        dir: export directory, if 'None' the current working directory 
          (where script is run) is used 
        file_name: file name, if 'None', 'results' is used
        results_obj: PF ElmRes object, if 'None', 'All calculations.ElmRes' in
          active study case is used. All variables from this object are exported.
        results_variables_lists: Lists of results variables (PFResultVariable) that 
          are added to ComRes if only selected variables should be exported. Note
          that results_obj is ignored if results_variables_lists is specified.
      """
      comres = self.app.GetFromStudyCase("ComRes")
      if not results_obj:
        comres.pResult = self.app.GetFromStudyCase("ElmRes")
      else:
        comres.pResult = self.handle_single_pf_object_or_path_input(results_obj)
      if not dir:
        if self.export_dir:
          dir = self.export_dir
        else:
          # Use current working directory (where script is run)
          dir = getcwd()
      if not file_name:  
        file_name = "results"  
      if results_variables_lists:
        PFBaseInterface.add_selected_variables_for_export(comres,results_variables_lists)
      else:
        comres.iopt_csel = 0 # export all variables
      comres.iopt_exp = 6 # to export as csv
      path = dir + "\\" + file_name + ".csv"
      comres.f_name = path
      comres.iopt_sep = 0 # Do NOT use system separator
      comres.col_Sep = "," # Column separator
      comres.dec_Sep = "." # Decimal separator
      comres.iopt_honly = 0 # to export data and not only the header
      comres.iopt_locn = 3 # column header includes path
      comres.ciopt_head = 1 # full variable name
      comres.Execute()

      path = self.replace_special_PF_characters_in_path_string(path)
      # If the result object(s) are ElmRes, the the csv file is formated.
      if (comres.pResult and comres.pResult.GetClassName() == "ElmRes") or (results_variables_lists and results_variables_lists.result_objects[0].GetClassName() == "ElmRes"):
        try:
          self.format_csv_for_elmres(path)
        except(IndexError):
          raise Exception(f"Is the file \n" 
            f"'{path}' \nopen in another program?")
      else:
        self.format_csv_for_comtrade(path)

  def replace_special_PF_characters_in_path_string(self,path):
    """Replaces special characters '$(ExtDataDir)','$(WorkspaceDir)','$(InstallationDir)'
    in a path string with their actual directories.
    """
    if "$(ExtDataDir)" in path:
      project_settings = self.get_project_settings()
      ext_data_dir = self.get_attr(project_settings,"extDataDir")
      path = path.replace("$(ExtDataDir)",ext_data_dir)
    path = path.replace("$(WorkspaceDir)",self.app.GetWorkspaceDirectory())
    return path.replace("$(InstallationDir)",self.app.GetInstallationDirectory())

  def get_project_settings(self):
    """Returns project settings object.
    """
    project_settings_folder = self.get_single_obj("*.SetFold")
    return self.get_single_obj("*.SetPrj",parent_folder=project_settings_folder)

  @staticmethod
  def add_selected_variables_for_export(comres,results_variables_lists):
    """Adds selected variables to ComRes for export.
    Arguments:
      comres: PF object ComRes for export
      results_variables_lists: lists with infos about exported data (results objects,
        elements,variables)
    """
    comres.iopt_csel = 1 # export only selected variables
    comres.pResult = None # export only selected variables
    # Insert time
    if not results_variables_lists.variables[0] == "b:tnow":
      results_variables_lists.result_objects.insert(0,results_variables_lists.result_objects[0])
      results_variables_lists.elements.insert(0,results_variables_lists.result_objects[0])
      results_variables_lists.variables.insert(0,"b:tnow")
    comres.resultobj = results_variables_lists.result_objects
    comres.element = results_variables_lists.elements
    comres.variable = results_variables_lists.variables

  def format_csv_for_comtrade(self,file_path):
    """Format the csv created from a Comtrade object with ComRes.
    There is a bug in PF so that the time in the first column sometimes
    is not monotonously increasing. This methods corrects this by checking 
    for each time value (1. column) whether it is larger than the previous and discarding rows
    where this is not the case.
    """
    with open(file_path) as read_file, open(file_path + ".temp", "w") as write_file:
      row = read_file.readline()
      write_file.write(row)
      time = -math.inf
      row = read_file.readline()
      while row:
        row_entries = row.split(",")
        if float(row_entries[0]) > time:
          write_file.write(row)
          time = float(row_entries[0])
        row = read_file.readline()  
    replace(file_path + ".temp",file_path)  

  def format_csv_for_elmres(self,file_path):
    """Format the csv file that is exported from PF.
    The PF exported csv uses the first row for the full path 
    of the object and the second row for the variable name.
    The formated csv file uses only the first row as a header.
    This row contains the path of the object and the variable name
    without description.

    Example first row of some column before formating: 
      '\\username.IntUser\\powfacpy_base.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\Grid.ElmNet\\AC Voltage Source.ElmVac\\s:u0'
    Example input second row of the column before formating:
      's:u0 in kV'
    Example first row of the column after formating:
      'Network Model\\Network Data\\Grid\\AC Voltage Source\\s:u0'
    """
    with open(file_path) as read_file, open(file_path + ".temp", "w") as write_file:
      full_paths = read_file.readline().split(",")
      variables = read_file.readline().split(",")
      for col,path in enumerate(full_paths):
          if col > 0:
              formated_path = powfacpy.PFStringManipuilation.format_full_path(path,self)
              variable_name = variables[col].split(" ", 1)[0].replace("\"","").replace("\n","") # get rid of description and quotation marks
              row = row + formated_path + "\\" + variable_name + "," # consistently add headers to row
          else:
              row = "Time," # Header of first column
      write_file.write(row+"\n")
      # Write remaining data rows until end of file is reached
      while row:
          row = read_file.readline()
          write_file.write(row)
    replace(file_path + ".temp",file_path)  

  @staticmethod
  def replace_headers_of_csv_file_with_number_of_colums(file_path):
    """Replaces the first row (headers) of a csv file with its number of
    columns. This is needed for import of csv files to PF using ElmFile.
    """
    with open(file_path+".csv") as read_file, open(file_path + ".temp", "w") as write_file:
      columns_of_first_row = read_file.readline().split(",")
      if columns_of_first_row[-1] == "\n":
        columns_of_first_row = columns_of_first_row[:-1]
      number_of_columns = len(columns_of_first_row)-1 # Minus one because first column is time and should not be counted.
      write_file.write(str(number_of_columns)+"\n") 
      row = read_file.readline()
      while row:
          write_file.write(row)
          row = read_file.readline()
    replace(file_path + ".temp",file_path+".csv") 
    return number_of_columns

  @staticmethod
  def insert_row_with_number_of_columns_in_csv_file(file_path):
    """Gets the number of columns of the first row in a csv file and
    inserts a row (first row) with this number in the first column.
    This is needed for ElmFile to read csv files.
    """
    with open(file_path+".csv") as read_file, open(file_path + ".temp", "w") as write_file:
      first_row = read_file.readline()
      columns_of_first_row = first_row.split(",")
      if columns_of_first_row[-1] == "\n":
        columns_of_first_row = columns_of_first_row[:-1]
      number_of_columns = len(columns_of_first_row)-1 # Minus one because first column is time and should not be counted.
      write_file.write(str(number_of_columns)+"\n")
      write_file.write(first_row)
      row = read_file.readline()
      while row:
          write_file.write(row)
          row = read_file.readline()
    replace(file_path + ".temp",file_path+".csv")  
    return number_of_columns

  def get_upstream_obj(self, obj_or_path, condition):
    """Returns the upstream object that meets the condition.
    Goes up step by step to the parent folders until the condition is met.
    Arguments:
      obj_or_path: Object (or its path) to start from.
      condition: lamba function with condition for parent object.
    """
    obj_or_path = self.handle_single_pf_object_or_path_input(obj_or_path)
    obj_or_path = obj_or_path.GetParent()
    if condition(obj_or_path):
      return obj_or_path
    else:
      self.get_upstream_obj(obj_or_path, condition)

  def get_path_between_objects(self, obj_high, obj_low):
    """Returns the path between two objects in the database.
    Arguments:
      object_high: Object higher in the hierarchy.
      object_low: Object lower in the hierarchy. 
    """
    obj_high = self.handle_single_pf_object_or_path_input(obj_high)
    obj_high = PFStringManipuilation.format_full_path(str(obj_high),self)
    obj_low = self.handle_single_pf_object_or_path_input(obj_low)
    obj_low = PFStringManipuilation.format_full_path(str(obj_low),self)
    path = str(obj_low).split(str(obj_high))[1][1:] 
    return path     


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

  
class PFResultVariable:

  def __init__(self,result_object,element,variable) -> None:

    self.result_object = result_object
    self.element = element
    self.variable = variable

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
  