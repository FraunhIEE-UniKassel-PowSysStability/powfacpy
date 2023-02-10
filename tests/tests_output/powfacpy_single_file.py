"""Contains the class PFBaseInterface (interaction with the PF database)
and the class PFStringManipulation for string manipulation.

The abbreviation 'PF' is sometimes used for 'PowerFactory'.
"""

from argparse import ArgumentError
import sys

sys.path.insert(0,r'.\src')
from os import path as os_path
from collections.abc import Iterable
from os import getcwd, replace
import math


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

  def get_unique_obj(self,path,parent_folder=None,error_if_non_existent=True,
    include_subfolders=False):
    """This method is equal to get_single_obj and was added because the method
    name fits better to what the method does (i.e. to get a unique object and to
    throw an error if the object is not unique).
    """
    return self.get_single_obj(path,parent_folder=parent_folder,
      error_if_non_existent=error_if_non_existent,
      include_subfolders=include_subfolders)

  def get_single_obj(self,path,parent_folder=None,error_if_non_existent=True,
    include_subfolders=False):
    """Use this method if you want to access one single unique object.
    This method is an alterntive to 'get_obj' and returns the unique object instead
    of a list (that needs to be accessed with '[0]'). It also checks whether the found
    object is unique (only one object is found).
    """
    obj = self.get_obj(path,parent_folder=parent_folder,
      error_if_non_existent=error_if_non_existent,
      include_subfolders=include_subfolders)
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
      raise PFPathError(non_existing_child,existing_path)

  def handle_condition_of_obj_not_met(self,path,obj,error_if_non_existent):
    """Handles the attempted access to an object with a certain condition
    that does not exist.
    """
    if not error_if_non_existent:
      return []
    else:
      head,tail = os_path.split(path)
      raise PFNonExistingObjectError(obj[0].GetParent(),tail,condition=True)

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
      raise PFPathInputError(path)
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
          parent_path = PFStringManipulation.delete_classes(parent_path)
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
      raise PFNotActiveError("a project")

  def get_active_user_folder(self):
    """Return the folder of the active user.
    ToDo: Implement using app.GetCurrentUser()
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
        raise PFAttributeError(obj,e,self)
      except(TypeError) as e:
        object_str = PFStringManipulation.format_full_path(str(obj),self)
        raise TypeError(f"{e}. Maybe an unexpected type is used "
          f"for attribute of object '{object_str}'.")  
    return objects_true
  
  def get_path_of_object(self,obj):
    return PFStringManipulation.format_full_path(str(obj),self)

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
      raise PFAttributeError(obj,e,self)

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
        raise PFAttributeTypeError(obj,attr,e,self)
      except(AttributeError) as e:
        raise PFAttributeError(obj,e,self)

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
      if obj:
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
      else:
        msg = (f"Expected a PowerFactory object or a path string. Instead an "
            f"empty object of type '{type(obj).__name__}' is given.")
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
      results_obj_name = PFTranslator.get_default_result_object_name(self.language)
      results_obj = self.app.GetFromStudyCase(results_obj_name)
    else:
      results_obj = self.handle_single_pf_object_or_path_input(results_obj)
    obj = self.handle_single_pf_object_or_path_input(obj)
    if isinstance(variables, str):
      variables = [variables]
    for var in variables:
      results_obj.AddVariable(obj,var)
    results_obj.Load()
    return results_obj

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
    results_variables_lists=None,
    column_separator=',',
    decimal_separator='.'
    ):
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
      comres.iopt_sep = 0 # to use specified column and decimal separator symbols
      comres.col_Sep = column_separator
      comres.dec_Sep = decimal_separator
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
              formated_path = PFStringManipulation.format_full_path(path,self)
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
      return self.get_upstream_obj(obj_or_path, condition)

  def get_path_between_objects(self, obj_high, obj_low):
    """Returns the path between two objects in the database.
    Arguments:
      object_high: Object higher in the hierarchy.
      object_low: Object lower in the hierarchy. 
    """
    obj_high = self.handle_single_pf_object_or_path_input(obj_high)
    obj_high = PFStringManipulation.format_full_path(str(obj_high),self)
    obj_low = self.handle_single_pf_object_or_path_input(obj_low)
    obj_low = PFStringManipulation.format_full_path(str(obj_low),self)
    path = str(obj_low).split(str(obj_high))[1][1:] 
    return path     
  
  @staticmethod
  def get_loc_name_with_class(powerfactory_objects):

    is_list = True
    if not type(powerfactory_objects) == list:
      powerfactory_objects = [powerfactory_objects,]
      is_list = False

    loc_name_with_class = []
    for powerfactory_object in powerfactory_objects:
      loc_name_with_class.append(
        powerfactory_object.loc_name
        + '.'
        + powerfactory_object.GetClassName())
    if not is_list:
      loc_name_with_class = loc_name_with_class[0]  
    return loc_name_with_class
    
  def add_comtrade_obj(self,file_path: str,parent_folder=None):
    """Add an IntComtrade that refers to file_path (*.cfg).
    The objects are stored in a folder "Comtrade" in the currently active
    study case, unless a parent_folder is provided. A new object is only
    created if there exists no object yet that points to the same file
    (f_name attribute is the file path). The file name is used for the
    new object name (without the .cfg ending).
    """
    if parent_folder:
      parent_folder = self.handle_single_pf_object_or_path_input(parent_folder)
    else:
      parent_folder = self.app.GetFromStudyCase("Comtrade.IntFolder")

    intcomtrade = self.get_obj("*.IntComtrade",
      parent_folder=parent_folder,
      condition=lambda x : getattr(x,"f_name")==file_path,
      error_if_non_existent=False)
    if not intcomtrade:
      _,file_name = os_path.split(file_path)
      intcomtrade = self.create_in_folder(parent_folder,
        file_name.replace(".cfg","") + ".IntComtrade", overwrite=False,
        use_existing=False) 
      intcomtrade.f_name = file_path
    else:
      intcomtrade = intcomtrade[0]
    # intcomtrade.Load() probably not required
    return intcomtrade


class PFStringManipulation:
  
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
    return PFStringManipulation.replace_between_characters('.','\\','\\',path)

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
    return PFStringManipulation.delete_classes(path)
  
  @staticmethod
  def handle_path(path):
    """Checks if path starts with \ (not accepted by most PF method)
    and also if 'path' is of type string.
    """
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

  @staticmethod
  def _get_language_dependent_name_from_studycase(
    studycase, english_name, german_name):
    studycase_contents = PFTranslator.\
      get_name_with_ending(
        studycase.GetContents())
    has_english_name = english_name in studycase_contents
    has_german_name = german_name in studycase_contents
    assert not (has_english_name and has_german_name), \
      'Two redundant file versions: English and German named files exist.'
    if has_english_name:
      return english_name
    else:
      return german_name

  @staticmethod
  def get_graphics_board_name_from_studycase(studycase):
    name = PFTranslator.\
      _get_language_dependent_name_from_studycase(
      studycase=studycase,
      english_name="Graphics Board.SetDesktop",
      german_name="Grafiksammlung.SetDesktop",
    )
    return name

  @staticmethod
  def get_result_object_name_from_studycase(studycase):
    name = PFTranslator.\
      _get_language_dependent_name_from_studycase(
      studycase=studycase,
      english_name="All calculations.ElmRes",
      german_name="Alle Berechnungsarten.ElmRes",
    )
    return name

  @staticmethod
  def get_name_with_ending(objects):
    if not type(objects) == list:
      objects = [objects]
    return [x.GetFullName().split('\\')[-1] for x in objects]


def set_attr_of_obj(obj, attributes:dict):
  """Set attributes of object.
  The difference to set_attr of PFBaseInterface is that
  this method only accepts PF objects (and not path strings)
  and is slightly more performant.
  """
  for attr,value in attributes.items():
    obj.SetAttribute(attr,value)

def set_attr_of_objects(objects: Iterable,attributes: Iterable):
  """Set attributes of multiple objects.
  """
  for obj in objects:
    set_attr_of_obj(obj,attributes)

def set_attr_of_child(parent,child:str, attributes:dict):
  """Set attributes of a child object in parent.
  Just syntactic sugar.
  """
  child = parent.GetContents(child)[0]
  for attr,value in attributes.items():
    child.SetAttribute(attr,value)
 
"""Custom exceptions for 
"""
import sys
sys.path.insert(0,r'.\src')

class PFInterfaceError(Exception):
  """There should always be a base class (that inherits
  from 'Exception') for all custom errors/exceptions.
  """
  pass

class PFAttributeError(PFInterfaceError):
  """Attempt to access an invalid attribute of a PF object.
  """
  def __init__(self,obj,msg_raised,pf_base_interface):
    object_str = PFStringManipulation.format_full_path(str(obj),pf_base_interface)
    self.message = (f"Unexpected attribute of object '{object_str}': {msg_raised}.")
    super().__init__(self.message)

class PFAttributeTypeError(PFInterfaceError):
  """Attempt to set an invalid type for the attribute of a PF object.
  """
  def __init__(self,obj,attr,msg_raised,pf_base_interface):
    object_str = PFStringManipulation.format_full_path(str(obj),pf_base_interface)
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
    folder_str = PFStringManipulation.delete_classes(str(folder))
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

class PFNoPlotActivatedError(PFInterfaceError):
  """Attempt to plot, but no plot is active.
  """ 
  def __init__(self):
    self.message = (f"Attempt access plot, but no plot is active. "
    "Please activate a plot (use 'set_active plot').")
    super().__init__(self.message)

class PFCaseStudyParameterValueDefinitionError(PFInterfaceError):
  """Number of parameter values is not the same for every parameter. 
  """
  def __init__(self,par_name,values):
    self.message = (f"Incorrect number of values defined for parameter '{par_name}'. "
    f"Only {len(values)} values were defined.")
    super().__init__(self.message)
 
import sys
sys.path.insert(0,r'.\src')


class PFDynSimInterface(PFBaseInterface):
  
  def __init__(self,app): 
    super().__init__(app) 
    
  def initialize_sim(self,param=None):
    """
    Initialize time domain simulation.
    Parameters for 'ComInc' command object can be specified in 'param' dictionary.
    """
    cominc = self.app.GetFromStudyCase("ComInc")
    if param is not None:
      self.set_attr(cominc,param)
    cominc.Execute()

  def run_sim(self,param=None):
    """
    Perform dynamic simulation.
    Parameters for 'ComSim' command object can be specified in 'param' dictionary.
    """
    comsim = self.app.GetFromStudyCase("ComSim")
    if param is not None:
      self.set_attr(comsim,param)
    comsim.Execute()

  def initialize_and_run_sim(self):
    """Initialize and perform time domain simulation."""
    self.initialize_sim()
    self.run_sim()

  
  """
  def create_reference_signal(self,path,points):
    composite_model = self.create_by_path(path + ".ElmComp")
    composite_frame = self.get_obj(self.dynamic_model_teamplates_path +
      r"\reference_signal_frame")
    composite_model.SetAttribute("typ_id",composite_frame)
    dsl_obj = self.create_in_folder(composite_model,"lin_interpol_model.ElmDsl")
    lin_interpol_model = self.get_obj(self.dynamic_model_teamplates_path +
      r"\Linear_interpolation")
    dsl_obj.SetAttribute("typ_id",lin_interpol_model)
    set_dsl_obj_matrix(dsl_obj,points)
    composite_model.SetAttribute("pelm",[dsl_obj])
  """

  def create_event(self,name_incl_class,params={},parent_folder=None,overwrite=True):
    """Creates an event and sets the parameters in 'params'.
    Arguments:
      name_incl_class: Event name including the class.
      params: Paramter-values dictionary.
      parent_folder: If None, the events folder from the active study case is used.
      overwrite: Oerwrite existing event with same name.
    """
    if not parent_folder:
      parent_folder = self.app.GetFromStudyCase("IntEvt")
    event_obj = self.create_in_folder(parent_folder,name_incl_class,overwrite=overwrite)
    self.set_attr(event_obj,params)  

  @staticmethod 
  def set_dsl_obj_array(dsl_obj,
                        rows,
                        array_num=None,
                        size_included_in_array=True): 
    """Set the array of DSL object ('Advanced 1' tab).
    The array_num specifies which array is set (if None,
    all arrays/colums are set).
    If size_included_in_array=True, the first row (where the size
    of the array is spedified) is included.
    """  
    if not size_included_in_array:
      if not array_num:
        dsl_obj.SetAttribute("matrix:0",[len(rows)]*len(rows[0]))
      else:
        complete_row = dsl_obj.GetAttribute("matrix:0")
        complete_row[(array_num-1)*2] = len(rows)
        dsl_obj.SetAttribute("matrix:0",complete_row)                                              
    for row_num,row in enumerate(rows):
      if not size_included_in_array:
        attrib = "matrix:" + str(row_num+1)
      else:
        attrib = "matrix:" + str(row_num)
      if not array_num:
        dsl_obj.SetAttribute(attrib,row)
      else:
        complete_row = dsl_obj.GetAttribute(attrib)
        complete_row[(array_num-1)*2] = row[0]
        complete_row[(array_num-1)*2+1] = row[1]
        dsl_obj.SetAttribute(attrib,complete_row)

  @staticmethod 
  def get_dsl_obj_array(dsl_obj,
                        array_num=None,
                        size_included_in_array=True):
    """Get the array of DSL object ('Advanced 1' tab).
    The array_num specifies which array is returend (if None,
    all arays/colmns are returned).
    If size_included_in_array=True, the first row (where the size
    of the array is spedified) is included.
    """                    
    if not array_num:
      number_of_rows = int(max(dsl_obj.GetAttribute("matrix:0"))) + 1
    else:
      number_of_rows = int(dsl_obj.GetAttribute("matrix:0")[(array_num-1)*2]) + 1   
    array = []
    for row_num in range(number_of_rows):
      if row_num == 0 and not size_included_in_array:
        continue
      attrib = "matrix:" + str(row_num)
      row = dsl_obj.GetAttribute(attrib)
      if array_num:
        row = [row[(array_num-1)*2],row[(array_num-1)*2+1]]  
      array.append(row)
    return array
      

if __name__ == "__main__":
  pass
 
"""Plotting interface.
"""

import sys
sys.path.insert(0,r'.\src')
import pandas
from matplotlib import pyplot
from collections.abc import Iterable
from os import getcwd, path
from os import path as os_path

class PFPlotInterface(PFBaseInterface):

  def __init__(self,app):
    super().__init__(app) 
    self.active_graphics_page = None
    self.active_plot = None


  def set_active_graphics_page(self,page):
    """Sets the active graphics page.
    Arguments:
      page:graphics page  name.
    """
    if isinstance(page, str):
      grb = self.get_or_create_graphics_board()
      self.active_graphics_page = grb.GetPage(page,1,"GrpPage")
    else:
      self.active_graphics_page = page


  def set_active_plot(self,name_or_obj,graphics_page=None):
    """Set the currently active plot.
    Arguments:
      name_or_obj: name of plot (string) or plot object
      graphics_page: name of grphics page (string). If  
        specified, this sets the currently active page.
    """
    if graphics_page:
      self.set_active_graphics_page(graphics_page)
      if not isinstance(name_or_obj,str):
        self.active_plot = name_or_obj
      else:
        self.active_plot = self.active_graphics_page.GetOrInsertCurvePlot(name_or_obj)
    else:
      self.active_plot = name_or_obj
      self.set_active_graphics_page(self.active_plot.GetParent())


  def get_or_create_graphics_board(self):
    """Get the graphics board of the currently active study case or create
    a new graphics board if it does not exist within the study case yet.
    """
    grb = self.app.GetGraphicsBoard()  
    if not grb:
      active_study_case = self.app.GetActiveStudyCase()
      graphics_board_name = PFTranslator.get_default_graphics_board_name(
         self.language)
      grb = self.create_in_folder(active_study_case,graphics_board_name)
      grb.Show()
      grb = self.app.GetGraphicsBoard() # get grb again to get correct object from PF
    return grb  


  def plot_monitored_variables(self,obj,variables,
    graphics_page=None,plot=None,**kwargs):
    """Plot varibales that were already added to the monitored
    variables.
    Arguments:
      obj: PowerFactory object or its path
      variables: string or list of variable names 
      graphics_page: name of graphics page
      plot: name of plot
      kwargs:
        result_obj: result object used (object or path)
        linestyle: int
        linewidth: double
        color: int
        label: str
    """
    if graphics_page:
      self.set_active_graphics_page(graphics_page)
    if plot:
      self.set_active_plot(plot)
    data_series = self.get_data_series_of_active_plot()
    if "results_obj" in kwargs:
      data_series.SetAttribute("useIndividualResults", 1)
    obj = self.handle_single_pf_object_or_path_input(obj)
    if isinstance(variables, str):
     variables = [variables]
    for var in variables:
      data_series.AddCurve(obj,var)
      self.set_curve_attributes(data_series,**kwargs)
    self.active_graphics_page.Show()


  def _handle_possible_no_plot_activated_error(self, e):
    """Handle error if no active plot available.
    """
    if not self.active_plot:
      raise PFNoPlotActivatedError()
    else:
      raise AttributeError(e)

  def get_data_series_of_active_plot(self):
    """Get the dataseries of the currently active plot.
    """
    try:
      return self.active_plot.GetDataSeries()
    except(AttributeError) as e:
      self._handle_possible_no_plot_activated_error(e)

  def get_x_axis_of_active_plot(self):
    """Get the x-axis of the currently active plot.
    """
    try:
      return self.active_plot.GetAxisX()
    except(AttributeError) as e:
      self._handle_possible_no_plot_activated_error(e)
  
  def get_y_axis_of_active_plot(self):
    """Get the y-axis of the currently active plot.
    """
    try:
      return self.active_plot.GetAxisY()
    except(AttributeError) as e:
      self._handle_possible_no_plot_activated_error(e)
    

  def plot(self,obj,variables,graphics_page=None,plot=None,**kwargs):
    """Plots the variables of 'obj' to the currently active plot.
    Includes adding the variables to the results (ElmRes) object.
    The active plot can be set with the optional arguments.
    Arguments:
      variables: string or list of variable names 
      graphics_page: name of graphics page
      plot: name of plot
      kwargs:
        results_obj: result object used (object or path)
        linestyle: int
        linewidth: double
        color: int
        label: str
    """
    obj = self.handle_single_pf_object_or_path_input(obj)
    if "results_obj" in kwargs:
      results_obj = kwargs["results_obj"]
    else:
      results_obj = None
    self.add_results_variable(obj,variables,results_obj=results_obj)
    self.plot_monitored_variables(obj,variables,
      graphics_page=graphics_page,plot=plot,**kwargs) 
  

  def set_curve_attributes(self,data_series,**kwargs):
    """Set curve attributes.
    Arguments:
      data_series: data series of plot.
      kwargs:
        results_obj: result object used (object or path)
        linestyle: int
        linewidth: double
        color: int
        label: str
    """
    if  "linestyle" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLineStyle")
      list_curveTableAttr[-1] = kwargs['linestyle']
      data_series.SetAttribute("curveTableLineStyle",list_curveTableAttr)
    if "linewidth" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLineWidth")
      list_curveTableAttr[-1] = kwargs['linewidth']
      data_series.SetAttribute("curveTableLineWidth",list_curveTableAttr)
    else:
      # The linewidth must be set to the standard value. Otherwise PF uses 
      # the value from the previous data series (this seems to be a PF bug).
      list_curveTableAttr = data_series.GetAttribute("curveTableLineWidth")
      list_curveTableAttr[-1] = 100
      data_series.SetAttribute("curveTableLineWidth",list_curveTableAttr)
    if "color" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableColor")
      list_curveTableAttr[-1] = kwargs['color']
      data_series.SetAttribute("curveTableColor",list_curveTableAttr)
    # The label must be handled differently because PF returns an empty list
    # if there haven't been any labels specified yet for any of the curves.
    if "label" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLabel")
      if list_curveTableAttr:
        list_curveTableAttr[-1] = kwargs['label']
      else:
        list_curveTableAttr = [kwargs['label']]
      data_series.SetAttribute("curveTableLabel",list_curveTableAttr)
    if "results_obj" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableResultFile")
      list_curveTableAttr[-1] = self.handle_single_pf_object_or_path_input(
        kwargs['results_obj'])
      data_series.SetAttribute("curveTableResultFile",list_curveTableAttr)

  def set_x_axis_attributes(self,**kwargs):
    """Set x-axis attributes.
    Arguments:
      key-value-pairs of axis-related PF attributes and the desired value.
    """
    self._set_axis_attributes(
      self.get_x_axis_of_active_plot(),
      kwargs)
    
  def set_y_axis_attributes(self, **kwargs):
    """Set y-axis attributes.
    Arguments:
      key-value-pairs of axis-related PF attributes and the desired value.
    """
    self._set_axis_attributes(
      self.get_y_axis_of_active_plot(),
      kwargs)      
    
  def _set_axis_attributes(self, axis, kwargs):
    """ set axis attributes for given axis. 
    set_y_axis_attributes() and set_x_axis_attributes() use this funciton.
    """
    for attribute, value in kwargs.items():
      axis.SetAttribute(attribute, value)      

  def plot_from_comtrade(self,
                      file_path,
                      variables,
                      graphics_page=None,
                      plot=None,
                      parent_folder_comtrade=None,
                      **kwargs):
    """Plot a varibale from a COMTRADE formated file under file_path (*.cfg).
    Creates the comtrade object (IntComtrade) and plots.
    
    If you want to plot from a comtrade object (IntComtrade) that already 
    exists in the PF database, use the method plot_monitored_variables as shown.
    
    Arguments:
      file_path: str
      variables: The entry in the second column of a signal in .cfg
      parent_folder_comtrade: Container in PF database for comtrade objects
        (str or PF object)
         
    For further info on the arguments see method plot_monitored_variables.  
    """                  
    intcomtrade = self.add_comtrade_obj(file_path,
      parent_folder=parent_folder_comtrade)
    self.plot_monitored_variables(intcomtrade,
              variables,
              graphics_page=graphics_page,
              plot=plot,
              results_obj=intcomtrade,
              **kwargs)

  def plot_from_csv_using_elm_file(self,file_path,variable,**kwargs):
    """Use an ElmFile object to plot data from csv file.
    The ElmFiles are stored in a dummy network because the simulation needs to be run
    to read the data from the csv file and is not just printed to the plot automatically.
    """
    # Deactivate currently active networks
    active_networks = self.get_active_networks(
      error_if_no_network_is_active=False)
    for network in active_networks:
      network.Deactivate()
    # Activate dummy network
    elmfiles_network = self.create_dummy_network("network_for_elmfiles")  
    elmfiles_network.Activate()  
    # Add new ElmFile
    elmfile_num = 1
    while True:
      existing_elmfile = self.get_single_obj("elmfile_"+str(elmfile_num),
        parent_folder=elmfiles_network,error_if_non_existent=False)
      if not existing_elmfile:
        break
      elmfile_num += 1 
    elmfile = self.create_in_folder(elmfiles_network,
      "elmfile_"+str(elmfile_num)+".ElmFile",overwrite=True)
    self.clear_elmres_from_objects_with_status_deleted()
    elmfile.f_name = file_path + ".csv"
    # Add ElmREs for ElmFiles
    active_case = self.app.GetActiveStudyCase()
    elmres_for_elmfiles = self.create_in_folder(active_case,
      "elmres_for_elmfiles.ElmRes",overwrite=False,use_existing=True)
    # Plot
    kwargs.update({"results_obj":elmres_for_elmfiles})  
    self.plot(elmfile,variable,**kwargs)
    # Simulate
    pfds = PFDynSimInterface(self.app)
    cominc = self.app.GetFromStudyCase("ComInc")
    initial_elmres = self.get_attr(cominc,"p_resvar")
    self.set_attr(cominc,{"p_resvar":elmres_for_elmfiles})
    pfds.initialize_and_run_sim()
    self.set_attr(cominc,{"p_resvar":initial_elmres})
    # Reactivate the initial networks
    elmfiles_network.Deactivate()
    for network in active_networks:
      network.Activate()

  def set_x_axis_range_of_active_plot(self,range: Iterable):
    x_axis = self.get_single_obj("x-Axis.PltAxis",parent_folder=self.active_plot)
    x_axis.rangeMin = range[0]
    x_axis.rangeMax = range[1]

  def create_dummy_network(self,name=None):
    """Creates a network with only one terminal.
    Such a network is used for example to read in ElmFile objects.
    """
    if not name:
      name = "dummy_network"
    network_folder = self.app.GetProjectFolder("netdat",1)
    dummy_network = self.create_in_folder(network_folder,
      name+".ElmNet",overwrite=False,use_existing=True)
    self.create_in_folder(dummy_network,
      "dummy_terminal.ElmTerm",overwrite=False,use_existing=True)
    return dummy_network

  def autoscale(self):
    self.active_graphics_page.DoAutoScaleY()
    self.active_graphics_page.DoAutoScaleX()
    self.active_graphics_page.DoAutoScaleY()
    self.active_graphics_page.DoAutoScaleX()

  def clear_curves(self):
    """Clear all curves from active plot.
    """
    data_series = self.get_data_series_of_active_plot()
    data_series.ClearCurves()

  def clear_curves_from_all_plots(self): 
    """Clear curves from all plots of the active study case.
    """     
    grb = self.get_or_create_graphics_board()
    graphics = grb.GetContents()
    for graphic in graphics:
      if graphic.GetClassName() == "GrpPage":    
        for child in graphic.GetContents(): 
          if child.GetClassName() == "PltLinebarplot":
            data_series =child.GetDataSeries()
            data_series.ClearCurves()  

  def clear_plot_pages(self):
    """Deletes all graphics (plot) pages from the graphics board of 
    the active study case. 
    """
    self.clear_graphics_board(obj="*.GrpPage")

  def clear_grid_diagrams(self):
    self.clear_graphics_board(obj="*.SetDeskpage")  

  def clear_graphics_board(self,obj="*"):
    """Clear the graphics board from specific objects or from all objects.
    Objects of class SetDeskpage are closed, others are removed.
    """
    grb = self.get_or_create_graphics_board()
    graphics = grb.GetContents(obj)
    for graphic in graphics:
      if graphic.GetClassName() == "SetDeskpage":
        graphic.Close()
      else:
        graphic.RemovePage()
  
  def copy_graphics_board_content(self,source_study_case,
    target_study_cases,obj_to_copy="*",
    clear_target_graphics_board=False):
    """Copy the graphics board content of a study case to another study cases.
    Arguments:
      source_study_case: Source case (path or object)
      target_study_cases: Target case(s) (path(s) or object(s))
      obj_to_copy: name of objects to be copied from graphics board 
        (e.g. "*.GrpPage" to copy only the plot pages)
      clear_target_graphics_board: If true, the graphics boards of the target 
        cases are cleared before pasting the content  
    """    
    
    currently_active_study_case = self.app.GetActiveStudyCase() # Method should not change active case
    graphics_board_name = PFTranslator.get_graphics_board_name_from_studycase(
      currently_active_study_case) # assumption: graphics board names identical in all study cases 
    source_study_case = self.handle_single_pf_object_or_path_input(source_study_case)
    source_graphics_board = self.get_single_obj(".SetDesktop",
      parent_folder=source_study_case)
    if not isinstance(target_study_cases,(list,tuple)):
      target_study_cases = [target_study_cases]  
    for target_study_case in target_study_cases:
      target_study_case = self.handle_single_pf_object_or_path_input(target_study_case)
      if not target_study_case == source_study_case:
        target_study_case.Deactivate() # Writing to active graphics board not possible 
        target_graphics_board = self.get_single_obj(".SetDesktop",parent_folder=target_study_case)
        if clear_target_graphics_board:
          self.delete_obj("*",parent_folder=target_graphics_board,error_if_non_existent=False)
        self.copy_obj(obj_to_copy,target_folder=target_graphics_board,overwrite=True,
          parent_folder=source_graphics_board)
    if currently_active_study_case:         
      currently_active_study_case.Activate() # Activate if it was deactivated

  def copy_graphics_board_content_to_all_study_cases(self,source_study_case,
    target_parent_folder=None,
    include_subfolders=True,
    obj_to_copy="*",
    clear_target_graphics_board=False):
    """Copy the content of the graphics board to all study cases.
    Arguments:
      source_study_case: Source case (path or object)
      target_parent_folder: Parent folder of target cases. By default,
        the study case folder of the project is used. Any folder inside
        the study case folder of the project can be specified.
      obj_to_copy: name of objects to be copied from graphics board 
        (e.g. "*.GrpPage" to copy only the plot pages)
      clear_target_graphics_board: If true, the graphics boards of the target 
        cases are cleared before pasting the content
    """
    if not target_parent_folder:
      #study_case_project_folder_name = PFTranslator.get_default_study_case_folder_name(
      #  self.language)
      #target_parent_folder = self.get_single_obj(study_case_project_folder_name)
      target_parent_folder = self.app.GetProjectFolder("study")  
    target_study_cases = self.get_obj("*.IntCase",
      parent_folder=target_parent_folder,
      include_subfolders=include_subfolders)
    self.copy_graphics_board_content(source_study_case,target_study_cases,
      obj_to_copy=obj_to_copy,
      clear_target_graphics_board=clear_target_graphics_board)

  @staticmethod
  def plot_from_csv(csv_path,variables,offset=0,plot_interface=None):
    """Plot results from csv file using pyplot.
    Arguments:
      csv_path: path of csv file
      variables: path of variables to be plotted
      offset: time offset

    Returns the plot.

    Example:
      plot_from_csv("results.csv",
        ["Network Model\\Network Data\\Grid\\AC Voltage Source\\s:u0",
        "Network Model\\Network Data\\Grid\\AC Voltage Source\\m:Psum:bus1"])  
    """
    if not plot_interface:
      plot_interface = pyplot
    if isinstance(variables, str):
      variables = [variables]
    with open(csv_path) as file:
      csv_file = pandas.read_csv(file)
      for var in variables:
        plot = plot_interface.plot(csv_file["Time"]+offset, csv_file[var], label = var)   
    return plot

  def get_data_series_from_plot(self,plot=None,indexes=None,include_curve_options=False):
    if not plot:
      data_series = self.get_data_series_of_active_plot()
    else:
      plot = self.handle_single_pf_object_or_path_input(plot)
      data_series = plot.GetDataSeries()
    lists_from_data_series_of_plot = self.get_lists_from_data_series_of_plot(
      data_series,indexes=None,include_curve_options=False)
    return self.get_pf_result_variables_from_lists_of_data_series_of_plot(curveTableElements,curveTableVariable,curveTableResultFile,
      curveTableLineStyle,curveTableLineWidth,curveTableColor,
      curveTableLabelinclude_curve_options=False)  

  def get_lists_from_data_series_of_plot(self,plot=None,indexes=None,include_curve_options=False):
    """Returns PFListsOfDataSeriesOfPlot object with lists of the data from 
    DataSeries (PltDataseries) of a plot.
    """
    if not plot:
        data_series = self.get_data_series_of_active_plot()
    else:
      plot = self.handle_single_pf_object_or_path_input(plot)
      data_series = plot.GetDataSeries()  
    lists = PFListsOfDataSeriesOfPlot(
      data_series.GetAttribute("curveTableElement"),  
      data_series.GetAttribute("curveTableVariable"), 
      [], [], [], [], []
    )
    if data_series.useIndividualResults:
      lists.result_objects = data_series.GetAttribute("curveTableResultFile") 
      for idx,res_obj in enumerate(lists.result_objects):
        if not res_obj:
          lists.result_objects[idx] = data_series.GetAttribute("userSelectedResultFile")
    else:
      # PF bug:
      # Even if 'autoSearchResultsFile' is True, 'userSelectedResultFile' and 
      # not 'autoSelectedResultFile' must be used.
      # Furthermore, 'autoSearchResultFile' must be deactivated and activated once.
      data_series.autoSearchResultFile = 0
      data_series.autoSearchResultFile = 1
      lists.result_objects = [data_series.GetAttribute("userSelectedResultFile")]*len(lists.elements)
    if include_curve_options:
      lists.line_styles = data_series.GetAttribute("curveTableResultFile") 
      lists.line_widths = data_series.GetAttribute("curveTableLineWidth") 
      lists.colors = data_series.GetAttribute("curveTableColor") 
      lists.labels = data_series.GetAttribute("curveTableLabel")
    # Return only curves contained in indexes  
    if indexes:
      lists.elements = [lists.elements[i] for i in indexes]
      lists.variables = [lists.variables[i] for i in indexes]
      lists.result_objects = [lists.result_objects[i] for i in indexes] 
      if include_curve_options:
        lists.line_style = [lists.line_style[i] for i in indexes] 
        lists.line_widths = [lists.line_widths[i] for i in indexes] 
        lists.colors = [lists.colors[i] for i in indexes]  
        lists.labels = [lists.labels[i] for i in indexes]  
    return lists

  def export_active_page(self,format='pdf',path=getcwd()):
    """Export active page using ComWr.
    """
    self.active_graphics_page.Show()
    comwr = self.app.GetFromStudyCase('ComWr')
    self.set_attr(comwr,{'iopt_rd': format,'iopt_savas': 0, 'f': path + "." + format})
    comwr.Execute()  

class PFListsOfDataSeriesOfPlot:

  def __init__(self,elements,variables,result_objects,line_styles,line_widths,colors,labels) -> None:
    self.elements = elements
    self.variables = variables 
    self.result_objects = result_objects
    self.line_styles = line_styles
    self.line_widths = line_widths
    self.colors = colors
    self.labels = labels        
 
import sys
sys.path.insert(0,r'.\src')
from itertools import product

class PFStudyCases(PFBaseInterface):
  language = PFBaseInterface.language

  def __init__(self,app):
    super().__init__(app)
    self.active_grids = None
    self.parameter_values = {}
    self.parameter_paths = {}
    self.delimiter = " "
    self.hierarchy = []
    self.study_cases = []
    self.omitted_combinations = []
    # ToDo base case/scen/var to copy or only base case
    """
    self.parent_folder_study_cases = PFTranslator.get_default_study_case_folder_name(
      self.language)
    self.parent_folder_scenarios = PFTranslator.get_default_operation_scenario_folder_path(
      self.language)
    self.parent_folder_variations = PFTranslator.get_default_variations_folder_path(
      self.language)
    """
    self.parent_folder_study_cases = None
    self.parent_folder_scenarios = None
    self.parent_folder_variations = None
    # Options  
    self.add_scenario_to_each_case = True
    self.add_variation_to_each_case = False
    self.consecutively_number_case_names = False
    self.anonymous_parameters = [] # Paramters of which names are not used 
    # in folder/case names (only their values are used)
    self.ignore_parameters_that_are_none_in_names = True

  def create_cases(self):
    """Create study cases (and corresponding scenarios/variations)
    Iterates through all cases and creates study cases (and folders
    according to 'hierarchy') using parameter-value strings for the
    study cases (and folder names). 
    """
    number_of_cases = len(next(iter(self.parameter_values.values())))
    for case_num in range(number_of_cases):
      folder_path = self.get_folder_path(case_num)
      parameter_values_string = self.get_case_params_value_string(
        case_num,omitted_parameters=self.hierarchy) 
      if self.consecutively_number_case_names:
        parameter_values_string = str(case_num) + " " + parameter_values_string  
      self.study_cases.append(
        self.create_study_case(parameter_values_string,folder_path))
      self.activate_grids(case_num)
      if self.add_scenario_to_each_case:
        scen = self.create_scenario(parameter_values_string,folder_path)
      if self.add_variation_to_each_case:
        self.create_variation(parameter_values_string,folder_path)
      self.set_parameters(case_num)
      if self.add_scenario_to_each_case:
        scen.Save()

  def get_folder_path(self,case_num):
    """Returns the folder path of a case.
    The path corresponds to parameter-value pairs specified
    in 'hierarchy'. 
    """
    if self.hierarchy:
      folder_path = ""
      for par_name in self.hierarchy:
        parameter_value = self.get_value_of_parameter_for_case(par_name,case_num)
        if parameter_value is not None or not self.ignore_parameters_that_are_none_in_names:
          add_to_string = str(parameter_value) + "\\"
          if not par_name in self.anonymous_parameters: 
            add_to_string = par_name + "_" + add_to_string
          folder_path += add_to_string
      if folder_path:   
        return folder_path[:-1] # discard last "\\""
    return None

  def get_value_of_parameter_for_case(self,par_name,case_obj_or_case_num):
    """Returns a parameter value for a certain case.
    Arguments:
      par_name: Parameter name (string)
      case_obj_or_case_num: Either the case number (int) or
        a study case PF object (then the case number/index is derived first)

    Note that the values in 'parameter_values' can be 
      - a list/tuple where each element corresponds to a case number
      - or a single value which is used for all cases
    """
    case_num = self.handle_case_input(case_obj_or_case_num)
    values = self.parameter_values[par_name]
    if isinstance(values,(list,tuple)):
      try:
        return values[case_num]
      except(IndexError):
        raise PFCaseStudyParameterValueDefinitionError(par_name,values)  
    else:
      return values

  def handle_case_input(self,case_obj_or_case_num):
    """Accepts PF study case object or integer.
    If the input is a PF object, the corresponding case number is returned,
    else simply the input (integer) is returned.   
    """
    if not isinstance(case_obj_or_case_num,int):
      return self.study_cases.index(case_obj_or_case_num)
    else:
      return case_obj_or_case_num  

  def get_case_params_value_string(self,case_obj_or_case_num,
    omitted_parameters=None,
    delimiter=None,
    equals_sign=None,
    anonymous_parameters=None):
    """Returns the parameter-value string for a case name.
    """
    case_num = self.handle_case_input(case_obj_or_case_num)
    if not delimiter:
      delimiter = self.delimiter
    if not equals_sign:
      equals_sign = " _ "   
    parameter_values_string = ""
    for par_name in self.parameter_values.keys():
      if omitted_parameters is None or par_name not in omitted_parameters:
        par_value = self.get_value_of_parameter_for_case(par_name,case_num)
        if par_value is not None or not self.ignore_parameters_that_are_none_in_names:
          add_to_string = str(par_value) + delimiter
          if anonymous_parameters is None:
            if par_name not in self.anonymous_parameters:
              add_to_string = par_name + equals_sign + add_to_string
          elif par_name not in anonymous_parameters:
            add_to_string = par_name + equals_sign + add_to_string 
          parameter_values_string += add_to_string
    return parameter_values_string[:-len(delimiter)] # discard last delimiter

  def create_study_case(self,name,folder_path):
    """Creates a study case with the name 'parameter_values_string'
    in the folder corresponding to 'folder_path' (this path is 
    relativ to 'parent_folder_study_cases)
    """
    parent_folder_study_case = self.get_study_cases_parent_folder() 
    if folder_path:
      parent_folder_study_case = self.create_directory(folder_path,
        parent_folder=parent_folder_study_case)
    study_case_obj = self.create_in_folder(parent_folder_study_case,
      name+".IntCase")
    study_case_obj.Activate()
    pfpi = PFPlotInterface(self.app)
    self.app.GetFromStudyCase("SetDesktop")
    return study_case_obj

  def create_scenario(self,parameter_values_string,folder_path): 
    """Creates a scenario with the name 'parameter_values_string'
    in the folder corresponding to 'folder_path' (this parth is 
    relativ to 'parent_folder_scenarios)
    """
    parent_folder_scenario = self.get_scenarios_parent_folder()
    if folder_path:
      parent_folder_scenario = self.create_directory(folder_path,
        parent_folder=parent_folder_scenario)       
    scenario_obj = self.create_in_folder(parent_folder_scenario,
      parameter_values_string+".IntScenario")
    scenario_obj.Activate()
    scenario_obj.Save()
    return scenario_obj

  def create_variation(self,parameter_values_string,folder_path):
    """Creates a variation with the name 'parameter_values_string'
    in the folder corresponding to 'folder_path' (this path is 
    relativ to 'parent_folder_variations)
    """ 
    parent_folder_variation = self.get_variations_parent_folder()
    if folder_path:
      parent_folder_variation = self.create_directory(folder_path,
        parent_folder=parent_folder_variation)
    variation_obj = self.create_in_folder(parent_folder_variation,
      parameter_values_string+".IntScheme")
    variation_obj.NewStage(parameter_values_string,0,1)
    variation_obj.Activate()
    return variation_obj

  def activate_grids(self,case_num):
    """Activate the corresponding grids of a study case.
    If 'active_grids' is a list/tuple, the elements correspond to
    each study case. If multiple grids are active, list/tuples can be 
    used in the elements in 'active_grids'. 
    If 'active_grid' is not a list/tuple, than one gird will be used
    for all cases.
    The grids can be thir paths or PF objects.
    """
    if isinstance(self.active_grids,(list,tuple)):
      grids = self.active_grids[case_num]
      if not isinstance(grids,(list,tuple)):
          grids = [grids]
      for grid in grids:
          grid = self.handle_single_pf_object_or_path_input(grid)
          grid.Activate()
    elif self.active_grids:
      grid = self.handle_single_pf_object_or_path_input(self.active_grids)
      grid.Activate() 

  def set_parameters(self,case_obj_or_case_num):
    """Set the parameters according to paths specified in 'parameter_paths'
    and values specified in 'parameter_values'. 
    """
    case_num = self.handle_case_input(case_obj_or_case_num)
    for par_name,path in self.parameter_paths.items():
      value = self.get_value_of_parameter_for_case(par_name,case_num)
      if value:
        self.set_attr_by_path(path,value)  

  def get_study_cases(self,conditions):
    """Retrieve study case objects depending on parameter values.
    Arguments:
      conditions: A dictionary with
        keys: parameter names
        values: lambda function with boolean return value depending on 
          parameter (key)
    Returns the study case objects whose parameters fullfill the conditions.

    Example:
      get_study_cases({"par1": lambda x: x == 2, "par2": lambda x: x>0})
        This returns the study cases for which 'par1' equals 2 and 'par2' is 
        positive.       
    """
    cases = []
    for case_num,case_obj in enumerate(self.study_cases):
      conditions_fullfiled = True
      for parameter,condition in conditions.items():
        if not condition(self.get_value_of_parameter_for_case(parameter,case_num)):
          conditions_fullfiled = False
          break
      if conditions_fullfiled:
        cases.append(case_obj)
    return cases


  def apply_permutation(self,omitted_combinations=None):
    """Replaces the values in 'parameter_values' with the permutation of
    their unique elements. 
    Use this method if you want to create cases of the permutation of all
    parameters. Note that 'parameter_values' is changed irreversibly.
    """
    # Make sure values are unique
    for param_name in self.parameter_values.keys():
      self.parameter_values[param_name] = list(
        set(self.parameter_values[param_name]))
    # Use 'product' to get iterable that returns permutation    
    permutation_iterable = product(*self.parameter_values.values())
    # Clear values 
    for param_name in self.parameter_values.keys():
        self.parameter_values[param_name] = []
    # Copy values from iterable    
    for values_of_all_parameters_for_case in permutation_iterable:
      if omitted_combinations:
        values_of_all_parameters_for_case = self.filter_omitted_combinations(
          values_of_all_parameters_for_case,omitted_combinations)
      if values_of_all_parameters_for_case:    
        for param_num,param_name in enumerate(self.parameter_values.keys()):
          self.parameter_values[param_name].append(
            values_of_all_parameters_for_case[param_num])

  def filter_omitted_combinations(self,values_of_all_parameters_for_case,omitted_combinations):
    """Filter the parameter combinations that should be omitted. 
    The difficulty is the handling of the 'all' case. In this case, the combination
    with any value of a parameter is omitted, but combinations with the other parameters
    must be allowed
    """
    # Create list from tuple because values might be changed/set to 'None'
    values_of_all_parameters_for_case = list(values_of_all_parameters_for_case)
    for omitted_combination_dict in omitted_combinations:
      is_omitted_combination = True
      for param_num,param_name in enumerate(self.parameter_values.keys()):
        if param_name in omitted_combination_dict:
          if omitted_combination_dict[param_name] == "all":
            # If the parameter is 'all', then only one case should be created. The case where
            # the value of the parameter takes on the value of the first entry in 
            # self.parameter_values[param_name][0] is selected. This must be the case for all
            # parameters that are set to 'all'
            if not (self.parameter_values[param_name][0] == values_of_all_parameters_for_case[param_num]): 
              return False
            else:
              is_omitted_combination = False
              values_of_all_parameters_for_case[param_num] = None
          elif not values_of_all_parameters_for_case[param_num] in omitted_combination_dict[param_name]:
            is_omitted_combination = False
            break
      if is_omitted_combination:
        return False
    return values_of_all_parameters_for_case

  def get_study_cases_parent_folder(self):
    if not self.parent_folder_study_cases:
      return self.app.GetProjectFolder("study")
    else:
      return self.parent_folder_study_cases

  def get_scenarios_parent_folder(self):
    if not self.parent_folder_scenarios:
      return self.app.GetProjectFolder("scen")
    else:
      return self.parent_folder_scenarios  

  def get_variations_parent_folder(self):
    if not self.parent_folder_variations:
      return self.app.GetProjectFolder("scheme")
    else:
      return self.parent_folder_variations       

  def clear_parent_folders(self):
    """Deletes all objects in the folders
      - self.parent_folder_study_cases
      - self.parent_folder_scenarios
      - self.parent_folder_variations
    if theses attributes are defined.  
    """
    parent_folders = [
      self.get_study_cases_parent_folder(),
      self.get_scenarios_parent_folder(),
      self.get_variations_parent_folder(),
    ]
    for parent_folder in parent_folders:
      if parent_folder:
        self.delete_obj("*",
          parent_folder=parent_folder,
          error_if_non_existent=False,
          include_subfolders=True)  


 
import sys
sys.path.insert(0,r'.\src')

class PFNetworkInterface(PFBaseInterface):
    
  def __init__(self,app):
    super().__init__(app) 

  def get_vacant_cubicle_of_terminal(self,terminal,new_cubicle_name=None):
    """Gets the first vacant cubicle found in a terminal (i.e. nothing is connected
    to this cubicle).
    If there is no vacant cuibicle, a new cubicle is created.

    Arguments:
      terminal: ElmTerm
      new_cubicle_name: Name  that is set for the found or created cubicle 
    """
    terminal = self.handle_single_pf_object_or_path_input(terminal)
    cubicles = self.get_cubicles_of_terminal(terminal)
    for cubicle in cubicles:
      if cubicle.obj_id == None:
        if new_cubicle_name:
          cubicle.loc_name = new_cubicle_name
        return cubicle
    if not new_cubicle_name:
      new_cubicle_name = "Cub_"+str(len(cubicles)+1)     
    return self.create_in_folder(terminal, new_cubicle_name+".StaCubic")

  def get_cubicles_of_terminal(self,terminal,only_calc_relevant=False):
    if not only_calc_relevant:
      return self.get_obj("*",parent_folder=terminal,
        condition=lambda x: x.GetClassName() == "StaCubic")
    else:
      return terminal.GetCalcRelevantCubicles()

  def get_elements_connected_to_terminal(self,terminal,only_calc_relevant=False):
    cubicles = self.get_cubicles_of_terminal(terminal,only_calc_relevant=only_calc_relevant)
    elements = []
    for cub in cubicles:
      if cub.obj_id is not None: 
        elements.append(cub.obj_id)
    return elements  

  def get_connected_terminal(self,element):
    return element.bus1.cterm 

  def copy_grid(self,grid_or_path,target_folder,new_name,
    parent_folder=None,
    error_if_non_existent=True):
    """Copying a grid is not trivial in PF because the graphical network objects
    need to be copied and assigned manually as this is not done automatically.
    """
    grid_to_be_copied = self.handle_single_pf_object_or_path_input(grid_or_path)
    new_grid = self.copy_single_obj(grid_to_be_copied,target_folder,
      overwrite=True,
      new_name=new_name,
      parent_folder=parent_folder,
      error_if_non_existent=error_if_non_existent)
    new_network_diagram = self.copy_single_obj(grid_to_be_copied.pDiagram,
      grid_to_be_copied.pDiagram.GetParent(),new_name=new_name,overwrite=True)
    graphical_net_objects = self.get_obj("*.IntGrf",
      parent_folder=new_network_diagram,include_subfolders=True)
    for graphical_net_obj in graphical_net_objects:
      element = graphical_net_obj.pDataObj
      path_in_grid = self.get_path_between_objects(grid_to_be_copied,element)
      graphical_net_obj.pDataObj = self.get_single_obj(path_in_grid,parent_folder=new_grid)
    new_network_diagram.pDataFolder = new_grid
    new_grid.pDiagram = new_network_diagram
    return new_grid

  def get_parent_grid(self,obj_or_path):
    obj_or_path = self.handle_single_pf_object_or_path_input(obj_or_path)
    return self.get_upstream_obj(obj_or_path,lambda x: x.GetClassName == "IntNet")    


 
"""Helper functions in the electrical and power engineering domain.
"""
import math


def get_R_and_X_from_RX_ratio(RX_ratio,Z_abs):
  """Get the resistor and reactance from R/X-ratio
  and absolte impedance.

  Derivation:
  sqrt(R^2 + X^2) = Z_abs
  --> sqrt((X*RX_ratio)^2 + X^2) = Z_abs
  --> X = sqrt(Z_abs^2/(1 + RX_ratio^2))
  """
  X = math.sqrt(Z_abs**2/(1 + RX_ratio**2))
  R = X*RX_ratio
  return R,X

def get_resistance_and_reactance_from_uk_and_copper_losses(uk,loss_kW,Snom_MVA,Unom_kV):
  """
  P = I^2*R
  I = S/U
  P = (S/U)^2*R
  """
  Znom = (Unom_kV*1e3)**2/(Snom_MVA*1e6)
  R = loss_kW*1e3*(Unom_kV*1e3/(Snom_MVA*1e6))**2
  r_pu = R/Znom
  x_pu = math.sqrt((uk/100)**2 - r_pu**2)
  return r_pu,x_pu

 
import sys
sys.path.insert(0,r'.\src')
import numpy as np


class PFResultsInterface(PFBaseInterface):

  def __init__(self, app):
    super().__init__(app)

  def get_list_with_results_of_variable(self,obj,variable,results_obj=None,load_elmres=True):
    if not results_obj:
      results_obj = self.app.GetFromStudyCase("ElmRes")
    if load_elmres:  
      results_obj.Load()  
    obj = self.handle_single_pf_object_or_path_input(obj)  
    column = results_obj.FindColumn(obj,variable)
    return self.get_list_with_results_of_column(column,results_obj=results_obj,load_elmres=False)  

  def get_list_with_results_of_column(self,column,results_obj=None,load_elmres=True):
    if not results_obj:
      results_obj = self.app.GetFromStudyCase("ElmRes")
    if load_elmres:  
      results_obj.Load()   
    intvec = self.create_in_folder(results_obj.GetParent(),"test.IntVec",overwrite=True) 
    results_obj.GetColumnValues(intvec,column) 
    list = intvec.V
    intvec.Delete()
    return list

  

""" class ElmRes2NumPyArray():

  def __init__(self) -> None:
    self.time_series = None # np.empty(1,dtype=float)

  def get(element,variable): """

 
"""Provides classes to interface python script objects (ComPython)
and to create an embedded script in the PF database based on a
python package. Used for example to add powfacpy to the embedded
script of a ComPython object to avoid having to install powfacpy,
which is an obstacle for some users without experience in coding 
or with pip.
"""

import sys
sys.path.insert(0,r'.\src')
import warnings
from os import path as os_path
import os
import shutil


class PFComPythonObjectInterface(PFBaseInterface):
  """Interface to python script objects.
  """

  def __init__(self,app): 
    super().__init__(app) 

  def create_file_from_embedded_script(self,out_file,compython):
    """Create a .py file from an embedded script.
    """
    compython = self.handle_single_pf_object_or_path_input(compython)
    # The xScript attribute is a list with all lines of the script
    TextFileProcessor.create_file_from_list_of_lines(out_file,compython.xScript)

  def set_embedded_script_from_file(self,compython,file):
    """Set the embedded script based on a .py file.
    """
    compython = self.handle_single_pf_object_or_path_input(compython)
    compython.xScript = TextFileProcessor.get_list_of_lines_of_file(file)

  def merge_file_into_embedded_script(self,
    compython,
    inserted_file:str,
    start_after_line,
    end_before_line):
    """Merge a file into an embedded script between the starting 
    and ending lines.
    The start and end lines can either be integers (line numbers) or
    string matches.
    """
    compython = self.handle_single_pf_object_or_path_input(compython)
    temporary_dir = "powfacpy_temp"
    os.makedirs(temporary_dir)
    try:
      embedded_script_original_file = temporary_dir + r"\embedded_script_original.py"
      self.create_file_from_embedded_script(embedded_script_original_file,compython)
      merged_file = temporary_dir + r"\merged.py"
      TextFileProcessor.merge_into_file(embedded_script_original_file,
        inserted_file,merged_file,start_after_line,end_before_line)
      self.set_embedded_script_from_file(compython,merged_file)  
    finally:
      # Delete temporary directory
      shutil.rmtree(temporary_dir)  

  def merge_package_into_embedded_script(self,
    compython,
    init_file,
    start_after_line,
    end_before_line):
    """Merge a whole package into an embedded script between the starting 
    and ending lines.
    The start and end lines can either be integers (line numbers) or
    string matches.
    """
    temporary_dir = "powfacpy_temp"  
    os.makedirs(temporary_dir)
    try:
      compython = self.handle_single_pf_object_or_path_input(compython)
      merged_package_file = temporary_dir + r"\merged_package.py"
      PythonFileInterface.merge_package_into_single_file(init_file,merged_package_file)
      original_embedded_script_file = temporary_dir + r"\original_embedded_script.py"
      self.create_file_from_embedded_script(original_embedded_script_file,compython)
      merged_package_into_embedded_file = temporary_dir + r"\merged_package_into_embedded.py"
      TextFileProcessor.merge_into_file(original_embedded_script_file,
        merged_package_file,
        merged_package_into_embedded_file,
        start_after_line,
        end_before_line)
      self.set_embedded_script_from_file(compython,merged_package_into_embedded_file)  
    finally:
      # Delete temporary directory
      shutil.rmtree(temporary_dir)

  def merge_powfacpy_package_into_single_file(self,out_file):
    init_file = os.path.dirname(__file__) + r"\__init__.py"
    PythonFileInterface.merge_package_into_single_file(init_file,out_file)


class PythonFileInterface():
  """Interface for .py files and python packages.
  """
  # ToDo: Convert notebooks to scripts (delete magic etc.)

  @staticmethod
  def read_init_file_of_package(path_of_init_file: str):
    """Reads the __init__.py file of a python package and returns
    the paths of the .py files the package uses and the name of the package.
    For now, only lines with the syntax
      'from example import *'
    are considered (i.e. this method does not work with all packages, but for example 
    with powfacpy)    
    """
    # The dir of the __init__.py file is also the directory of the files of the packages
    dir_of_all_files,_ = os_path.split(path_of_init_file)
    # The name of the package is the name of the parent folder of the __init__.py file 
    name_of_package = dir_of_all_files.split("\\")[-1] 
    file_paths= []
    with open(path_of_init_file, 'r') as init_file:
      for line in init_file:
        if line.startswith("from "):
          line = line.replace("from ","").replace(".","")
          file,imported_content = line.split(" import ")
          if not "*" in imported_content:
            falsely_read_line = line.split("import")[0] + "import *"
            warnings.warn(f"Cannot read <{line}>. Instead <{falsely_read_line}> is read.")
          file_paths.append(dir_of_all_files + "\\" + file + ".py")
    return file_paths,name_of_package

  @staticmethod
  def merge_package_into_single_file(init_file:str,out_file:str):
    """Merges all .py files of a package into a single file.
    Arguments:
      init_file: path of __init__.py of package
      out_file: path of file created  
    """
    package_files,package_name = PythonFileInterface.read_init_file_of_package(init_file)     
    merged_package_file = out_file
    replaced_chars = {package_name + ".":""}
    ignored_lines = {"import " + package_name:""} 
    TextFileProcessor.merge_files(package_files,
      merged_package_file,
      ignored_lines,
      replaced_chars)

class TextFileProcessor():
  """Processes plain text files (e.g. .txt or .py)
  """
  
  @staticmethod
  def merge_files(
    in_files: list,
    out_file: str,
    replace_line_if_startswith: dict = None,
    replace_chars: dict = None):
    """Merges several files into one. 
    Optionally replaces lines and chars.
    Arguments:
      in_files: list of input file paths
      out_file: output file path
      replace_line_if_startswith: dict to replace lines that 
        start with key with value
      replace_chars: dict to replace chars in key with value 
    """
    if not out_file.endswith(".py"):
      out_file = out_file + ".py"
    with open(out_file, 'w') as outfile:
      for fname in in_files:
        with open(fname) as infile:
          for line in infile:
            line = TextFileProcessor._replace_line(line,
              replace_line_if_startswith,replace_chars)
            if line:
              outfile.write(line)
          outfile.write("\n \n")

  @staticmethod
  def _replace_line(
    line: str,
    replace_line_if_startswith: dict = None,
    replace_chars: dict = None):
    """Handle replacements in line.
    """
    if replace_line_if_startswith:
      for start,replacement in replace_line_if_startswith.items():
        if line.startswith(start):
          line = replacement
          break
    if replace_chars:
      for replaced_char,replacement in replace_chars.items():
        line = line.replace(replaced_char,replacement)
    return line    

  @staticmethod
  def merge_into_file(
    target_file:str,
    inserted_file:str,
    out_file:str,
    start_after_line,
    end_before_line):
    """
    Creates a new file where one file is merged into another.
    Searches for start_after_line and end_before_line in target_file
    and replaces everything in between with inserted_file.
    The start and end lines can either be integers (line numbers) or
    string matches.
    """
    with open(out_file, 'w') as outfile:
      with open(target_file,'r') as sourcefile:
        start_line_was_reached = False
        end_line_was_reached = False
        line_count = 0
        for line in sourcefile:
          line_count = line_count + 1
          if not start_line_was_reached:
            outfile.write(line)
            if TextFileProcessor._line_is_reached(line,line_count,start_after_line):
              with open(inserted_file,'r') as insfile:
                outfile.write(insfile.read())
              outfile.write("\n")	
              start_line_was_reached = True
          elif TextFileProcessor._line_is_reached(line,line_count,end_before_line):		
            end_line_was_reached = True
          if end_line_was_reached:
            outfile.write(line)			
    if not start_line_was_reached:
      raise Exception(f"The spefified starting line for merging \n" +
        f"\"\n{start_after_line}\" \n was not found in the file {target_file}.")


  @staticmethod
  def _line_is_reached(current_line: str,
                      current_line_count:int,
                      condition):
    """Checks if a line is reached based upon a condition that can
    either be a line number or a string match.
    """
    if isinstance(condition, int):
      if current_line_count == condition:
        return True
      else:
        return False
    elif isinstance(condition, str):
      if current_line.rstrip() == condition:
        return True
      else:
        return False			

  @staticmethod
  def get_list_of_lines_of_file(file):
    """Reads all lines into a python list.
    """
    lines = []
    with open(file,'r') as f:
      for line in f:
        lines.append(line.rstrip()) # Omit line break and whitespace at the end 
    return lines

  @staticmethod
  def create_file_from_list_of_lines(out_file,lines):
    
    with open(out_file,"w") as f:
      for line in lines:
        f.write(line + "\n")  

  @staticmethod
  def process_file(
    in_file: str,
    out_file: str,
    replace_line_if_startswith: dict = None,
    replace_chars: dict = None,
    ):
    """Replaces chars and lines that start with a certain string.
    """
    with open(in_file,"r") as infile:
      with open(out_file,"w") as outfile:
        for line in infile:
          line = TextFileProcessor._replace_line(
              line,
              replace_line_if_startswith,
              replace_chars)
          if line:
            outfile.write(line)

  @staticmethod
  def extract_from_file(
    source_file: str,
    out_file: str,
    start_after_line,
    end_before_line):
    """Extracts the content between two lines from a file and writes
    to a new file.
    The start and end lines can either be integers (line numbers) or
    string matches.
    """
    with open(source_file,"r") as sourcefile:
      with open(out_file,"w") as outfile:
        start_line_was_reached = False
        end_line_was_reached = False
        line_count = 0
        for line in sourcefile:
          line_count = line_count + 1
          if not start_line_was_reached:
            if TextFileProcessor._line_is_reached(line,line_count,start_after_line):
              start_line_was_reached = True
          elif not end_line_was_reached:
            if TextFileProcessor._line_is_reached(line,line_count,end_before_line):		
              end_line_was_reached = True
            else:
              outfile.write(line)
  


  






 
