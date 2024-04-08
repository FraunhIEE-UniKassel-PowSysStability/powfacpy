"""Contains the class PFBaseInterface (interaction with the PF database)
and the class PFStringManipulation for string manipulation.

The abbreviation 'PF' is sometimes used for 'PowerFactory'.
"""
from __future__ import annotations
from warnings import warn
from os import replace
from collections.abc import Iterable
from typing import Union, Callable, Any
from os import path as os_path


import powfacpy
import sys
sys.path.insert(0, r'.\src')
from powfacpy.pf_class_protocols import *


class PFFolder():
    
    def __init__(self, folder:Union[PFGeneral,str], pf_app:PFApp):
        if pf_app:
            self.app:PFApp = pf_app
        else:
            raise TypeError("The input app is of type 'NoneType'. Maybe the PowerFactory app was not loaded correctly.")   
        self._folder:PFGeneral = self.handle_pf_object_or_path_input(folder)
    
    
    def GetContents(self, name:str, recursive:int=0):
        self._folder.GetContents(name, recursive)
        
    
    def GetChildren(self, hiddenMode:int, filter:str, subfolders:int):
        self._folder.GetChildren(hiddenMode, filter, subfolders) 
    
    
    def GetAttribute(self, attr:str) -> Union[int|float|str|PFGeneral|list]:
        self._folder.GetAttribute(attr)
    
    
    def SetAttribute(self, attr:str, value:Union[int|float|str|PFGeneral|list]) -> None:
        self._folder.SetAttribute(attr, value)    
    
    
    def GetParent(self) -> PFGeneral:
        self._folder.GetParent()  
    
    
    def CreateObject(self, 
                     className:str, 
                     objectNameParts:Union[int, str]="") -> PFGeneral:
        self._folder.CreateObject(className, objectNameParts)
    
    
    def Delete(self) -> int:
        self._folder.Delete()      
        
    
    def AddCopy(self, objectToCopy:PFGeneral, partOfName: Union[str, int] ="") -> PFGeneral:
        self._folder.AddCopy(objectToCopy, partOfName)     
       
##################
# Get
##################
    def get_obj(self, 
                path:str, 
                condition:Callable=None, 
                parent_folder:Union[PFGeneral, PFFolder, str]=None, 
                error_if_non_existent:bool=True,
                include_subfolders:bool=True) -> list[PFGeneral]:
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
        parent_folder = self._folder if not parent_folder else self.handle_single_pf_object_or_path_input(parent_folder)
        
        if not include_subfolders:
            try:
                obj = parent_folder.GetContents(path)
            except (RuntimeError):
                raise TypeError("Path must be of type string.")
        else:
            obj = self.handle_inclusion_of_subfolders(
                path, parent_folder, error_if_non_existent)
        if not obj:
            return self.handle_non_existing_obj(path, parent_folder, error_if_non_existent)
        if condition:
            obj_with_condition = self.get_by_condition(obj, condition)
            if obj_with_condition:
                return obj_with_condition
            else:
                return self.handle_condition_of_obj_not_met(path, obj, error_if_non_existent)
        else:
            return obj    

    
    def get_unique_obj(self, 
                       path:str, 
                       parent_folder: Union[PFGeneral, PFFolder, str]=None, error_if_non_existent:bool=True,
                       include_subfolders:bool=False) -> PFGeneral:
        """This method is equal to get_single_obj and was added because the method
        name fits better to what the method does (i.e. to get a unique object and to
        throw an error if the object is not unique).
        """
        return self.get_single_obj(path, parent_folder=parent_folder,
                                   error_if_non_existent=error_if_non_existent,
                                   include_subfolders=include_subfolders)


    def get_single_obj(self, 
                       path:str, 
                       parent_folder:Union[PFGeneral, PFFolder, str] = None, error_if_non_existent:bool = True,
                       include_subfolders:bool = False) -> PFGeneral:
        """Use this method if you want to access one single unique object.
        This method is an alterntive to 'get_obj' and returns the unique object instead
        of a list (that needs to be accessed with '[0]'). It also checks whether the found
        object is unique (only one object is found).
        """
        obj = self.get_obj(path, parent_folder=parent_folder,
                           error_if_non_existent=error_if_non_existent,
                           include_subfolders=include_subfolders)
        if obj:
            if len(obj) < 2:
                return obj[0]
            else:
                raise TypeError(f"The path {path} is not a unique object. Did you use wildcards ('*')? This method only returns single unique objects.")
        else:
            return None


    def get_multiple_obj_from_similar_sub_directories(
        self, 
        parent_folders:Union[list[PFGeneral], str], 
        sub_path:str) -> list[PFGeneral]:
        """Returns multiple objects that are in a similar subdirectory relativ to
        their parent folders.
        Arguments:
          parents: Parent folders (string path, list of objects/string paths)
          sub_path: Path within the parent folders (string). Must be unique (don't
            use placeholders '*')

        Example:
          If you want to get the "All calculation" objects of all the study cases 
          in the study case folder, use
            self.get_multiple_obj_from_similar_sub_directories(
              r'Study Cases\*','All calculations')     
        """
        if isinstance(parent_folders, str):
            parent_folders = self.get_obj(parent_folders)
        objs = []
        for parent in parent_folders:
            parent = self.handle_single_pf_object_or_path_input(parent)
            objs.append(self.get_single_obj(sub_path, parent_folder=parent))
        return objs


    def get_upstream_obj(self,
                         obj_or_path:Union[PFGeneral, str],
                         condition:Callable,
                         error_if_non_existent:bool=True) -> PFGeneral:
        """Returns the upstream object that meets the condition.
        Goes up step by step to the parent folders until the condition is met.
        Arguments:
          obj_or_path: Object (or its path) to start from.
          condition: lamba function with condition for parent object.
          error_if_non_existent: If True, an exception is raised if no upstream 
            object is found. If False, None is then returned.
        """
        obj_or_path = self.handle_single_pf_object_or_path_input(obj_or_path)
        obj_or_path = obj_or_path.GetParent()
        if obj_or_path:
            if condition(obj_or_path):
                return obj_or_path
            else:
                return self.get_upstream_obj(obj_or_path, condition)
        else:
            if error_if_non_existent:
                raise Exception(
                    "There is no upstream object that fullfills the condition.")
            else:
                return None
    
    
    

    def get_by_condition(self, 
                         objects:list[PFGeneral], 
                         condition:Callable) -> list[PFGeneral]:
        """From a list of objects, get those for whom the 'condition' 
        (which is a function) returns 'True'.
        Example:
          pfbi.get_by_condition(list_of_objects, lambda x : getattr(x,"uknom")==110)
        """
        objects_true = []
        for obj in objects:
            try:
                # This anonymous function is problematic because it does
                # not always throw an error when it the user provided
                # an anonymous function that does not make sense.
                if condition(obj):
                    objects_true.append(obj)
            except (AttributeError) as e:
                raise powfacpy.PFAttributeError(obj, e, self)
            except (TypeError) as e:
                object_str = powfacpy.PFStringManipulation._format_full_path(
                    str(obj), self.app)
                raise TypeError(f"{e}. Maybe an unexpected type is used "
                                f"for attribute of object '{object_str}'.")
        return objects_true


 ##################
 # Create
 ##################
    def create_by_path(self, path:str, overwrite:bool=True) -> PFGeneral:
        """Create an object by specifying its path including its class and return the object.
        If overwrite is true, objects with the same name will be overwritten.
        Example:
          pfbi.create_by_path(r'Library\Dynamic Models\dummy.BlkDef') 
        """
        try:
            folder_path, obj_name_incl_class = path.rsplit('\\', 1)
        except (AttributeError):
            raise TypeError("The argument 'path' must be of type string.")
        folder = self.get_single_obj(folder_path)
        return self.create_in_folder(obj_name_incl_class, folder, overwrite=overwrite)


    def create_in_folder(self, 
                         obj:str,
                         folder:Union[PFGeneral, PFFolder, str], 
                         overwrite:bool = True, 
                         use_existing:bool = False) -> PFGeneral:
        """Creates an obj inside a folder and returns the object.
        If overwrite is true, objects with the same name will be overwritten.
        If use_existing is True, objects with the same name are not replaced.
        If overwrite and use_existing are false and an object with the same name
        exists, a new object with "(1)"/"(2)".. in name is created.
        Example:
          pfbi.create_in_folder("dummy2.BlkDef", "Library\\Dynamic Models",)
        """
        folder = self._folder if not folder else self.handle_single_pf_object_or_path_input(folder)
        try:
            obj_name, _, class_name = obj.rpartition('.')
        except (AttributeError):
            raise TypeError("The argument 'obj' must be of type string.")
        if overwrite:
            self.delete_obj(obj, 
                            parent_folder=folder,
                            error_if_non_existent=False)
        elif use_existing:
            existing_obj = self.get_single_obj(
                obj, parent_folder=folder, error_if_non_existent=False)
            if existing_obj:
                return existing_obj
        return folder.CreateObject(class_name, obj_name)


    def create_directory(self, 
                         directory:str, 
                         parent_folder:Union[PFGeneral, PFFolder, str] = None) -> IntFolder:
        """Create a directory of folders ('IntFolder') if the 
        directory does not yet exist.
        Arguments:
          path: path of folders
          parent_folder: If not specified, the active project folder
            is used.

        Returns the folder in the lowest subdirectory.  
        """
        if not self.path_exists(directory, parent=parent_folder):
            folder = self._folder if not parent_folder else parent_folder
            folder_names = directory.split("\\")
            for folder_name in folder_names:
                if not self.path_exists(folder_name, parent=folder):
                    folder = self.create_in_folder(
                        folder_name+".IntFolder", folder)
                else:
                    folder = self.get_single_obj(
                        folder_name, parent_folder=folder)
            return folder
        else:
            return self.get_single_obj(directory, parent_folder=parent_folder)


 ##################
 # Copy
 ##################
    def copy_obj(self, 
                 obj_or_path:Union[PFGeneral, str], 
                 target_folder:Union[PFGeneral, PFFolder, str], 
                 overwrite:bool=True, 
                 condition:Callable=None,
                 parent_folder:Union[PFGeneral, PFFolder, str]=None, 
                 error_if_non_existent:bool=True, 
                 include_subfolders:bool=False):
        """Copies object(s) by using 'get_obj' in first step and then copying 
        the returned objects to 'target_folder'. Source and target must be in 
        the active project (otherwise use PasteCopy(), see scripting reference).
        The argument 'parent_folder' refers to the source folder and is used in
        combination with 'obj_or_path' to get the object(s) to be copied.
        If 'overwrite' is True, existing objects with the same name are overwritten
        in the target folder.
        For further information on the input arguments, see method 'get_obj'.

        Returns a list of the created copy/copies.

        See also 'copy_single_obj'
        """
        obj = self.handle_pf_object_or_path_input(
            obj_or_path,
            condition=condition,
            parent_folder=parent_folder,
            error_if_non_existent=error_if_non_existent,
            include_subfolders=include_subfolders)
        target_folder = self.handle_single_pf_object_or_path_input(
            target_folder)
        if overwrite:
            for object_to_be_copied in obj:
                self.delete_obj(object_to_be_copied.GetAttribute("loc_name"),
                                parent_folder=target_folder, error_if_non_existent=False)
        # AddCopy() accepts a list of objects, but then it returns the target
        # folder object and not the copied objects. Therefore, it is iterated through the
        # objects.
        copied_obj = []
        for o in obj:
            copied_obj.append(target_folder.AddCopy(o))
        return copied_obj


    def copy_single_obj(self, 
                        obj_or_path:Union[PFGeneral, str], 
                        target_folder:Union[PFGeneral, PFFolder, str], 
                        overwrite:bool = True,
                        new_name:str = None, 
                        parent_folder:Union[PFGeneral, PFFolder, str] = None, error_if_non_existent:bool = True):
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
        obj = self.handle_single_pf_object_or_path_input(
            obj_or_path,
            parent_folder=parent_folder,
            error_if_non_existent=error_if_non_existent)
        target_folder = self.handle_single_pf_object_or_path_input(
            target_folder)
        if overwrite:
            if not new_name:
                self.delete_obj(obj.GetAttribute("loc_name"),
                                parent_folder=target_folder, error_if_non_existent=False)
            else:
                self.delete_obj(f"{new_name}.*",
                                parent_folder=target_folder, error_if_non_existent=False)
        if new_name:
            return target_folder.AddCopy(obj, new_name)
        else:
            return target_folder.AddCopy(obj)
 
 
 ##################
 # Delete
 ##################
    def delete_obj(self, obj_or_path, condition=None, parent_folder=None, error_if_non_existent=True,
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
            o.Delete()
            # 'IsDeleted' seems to be the savest way to check whether an object has been deleted.
            if not o.IsDeleted():
                active_study_case = self.app.GetActiveStudyCase()
                if active_study_case:
                    active_study_case.Deactivate()
                    o.Delete()
                    active_study_case.Activate()

                if not o.IsDeleted():
                    try:
                        o.Deactivate()
                        o.Delete()
                    except (AttributeError):  # raised when o cannot be deactivated
                        raise TypeError(f"Object {o} cannot be deleted.")

                    if not o.IsDeleted():
                        raise TypeError(f"Object {o} cannot be deleted.")


    def clear_folder(self, folder:Union[PFGeneral, PFFolder, str] = None):
        """
        Clear all objects inside folder (including hidden objects).
        """
        folder = self._folder if not folder else self.handle_single_pf_object_or_path_input(folder)
        self.delete_obj("*",
                        parent_folder=folder,
                        include_subfolders=True,
                        error_if_non_existent=False)

 
##################
# Attributes
##################
    def get_attr(self, 
                 obj:Union[PFGeneral, str], 
                 attr:str, 
                 parent_folder:Union[PFGeneral, PFFolder, str] = None) -> Union[int|float|str|PFGeneral|list]:
        """Get the value of an attribute of an object.
        'obj' can be a path (string) or a Powerfactory object.
        'attr' can be a string or a list of strings.
        If parent_folder is specified, the path is relative to 
        this folder.

        Example:
         pfbi.get_attr(terminal_1,"systype")
        """
        if isinstance(obj, str):
            obj = self.get_single_obj(obj, parent_folder=parent_folder)
        try:
            if not isinstance(attr, list):
                return obj.GetAttribute(attr)
            else:
                attr_values = dict()
                for attribute in attr:
                    attr_values[attribute] = obj.GetAttribute(attribute)
                return attr_values
        except (AttributeError) as e:
            raise powfacpy.PFAttributeError(obj, e, self)


    def get_attr_by_path(self, path_with_attr:str):
        head_tail = os_path.split(path_with_attr)
        return self.get_attr(head_tail[0], head_tail[1])


    def set_attr(self, 
                 obj:Union[PFGeneral, str], 
                 params:dict, 
                 parent_folder:Union[PFGeneral, PFFolder, str]=None):
        """Set the attribute(s) of an object. 
        obj: PowerFactory object or its path (string).
        If 'parent_folder' is specified, the path is relative to 
        this folder.
        params: dictionary {parameter1:value1, parameter2:value2,..}.
        """
        obj = self.handle_single_pf_object_or_path_input(
            obj, parent_folder=parent_folder)
        for attr, value in params.items():
            try:
                obj.SetAttribute(attr, value)
            except (TypeError) as e:
                raise powfacpy.PFAttributeTypeError(obj, attr, e, self)
            except (AttributeError) as e:
                raise powfacpy.PFAttributeError(obj, e, self)


    def set_attr_by_path(self, path_with_attr:str, value):
        """
        path_with_attr: path of object plus the attribute name
        Example:
          pfbi.set_attr_by_path(self,
            "Library\\Dynamic Models\\Linear_interpolation\\desc",["description"])
          Here 'desc' is the name of the attribute.  
        """
        head_tail = os_path.split(path_with_attr)
        self.set_attr(head_tail[0], {head_tail[1]: value})


##################
# handle
##################
    def handle_inclusion_of_subfolders(
        self, 
        path:str, 
        parent_folder:Union[PFGeneral, PFFolder,str], 
        error_if_non_existent:bool) -> Union[list, PFGeneral]:
        """If subfolders are included, 'GetChildren' must
        be used instead of 'GetContents'. 'GetChildren'
        requires the input to be splitted between path and object name.
        """
        try:
            path_folder_list = path.split('\\')
            head, tail = '\\'.join(path_folder_list[:-1]), path_folder_list[-1]
        except (AttributeError):
            raise TypeError("Path must be of type string.")
        if head:
            new_parent_folder = parent_folder.GetContents(head)
            if new_parent_folder:
                parent_folder = new_parent_folder[0]
            else:
                return self.handle_non_existing_obj(head, parent_folder, error_if_non_existent)
        return parent_folder.GetChildren(1, tail, 1)

    
    def handle_non_existing_obj(self, 
                                path:str, 
                                parent_folder:Union[PFGeneral, PFFolder, str], error_if_non_existent:bool) -> list:
        """Handles the attempted access to a non existent object.
        """
        if not error_if_non_existent:
            return []
        else:
            exists_bool, existing_path, non_existing_child = self.path_exists(
                path, parent_folder, return_info=True)
            raise powfacpy.PFPathError(non_existing_child, existing_path)


    def handle_condition_of_obj_not_met(self, 
                                        path:str, 
                                        obj:Union[PFGeneral, PFFolder], 
                                        error_if_non_existent) -> list:
        """Handles the attempted access to an object with a certain condition
        that does not exist.
        """
        if not error_if_non_existent:
            return []
        else:
            head, tail = os_path.split(path)
            raise powfacpy.PFNonExistingObjectError(
                obj[0].GetParent(), tail, condition=True)


    def _handle_possible_attribute_not_set_error(
        self,
        possibly_not_secified_attr:str,
        attribute_description: str,
        e):
        """Handles exception if an AttributeError was raised in a
        method call on an attribute of a powfacpy class.
        """
        if not possibly_not_secified_attr:
            raise powfacpy.PFAttributeNotSetError(attribute_description)
        else:
            raise AttributeError(e)
    

    def handle_pf_object_or_path_input(
        self, 
        obj_or_path:Union[PFGeneral, str], 
        condition:bool=None, 
        parent_folder:Union[PFGeneral, PFFolder, str]=None,
        error_if_non_existent:bool=True, 
        include_subfolders:bool=False) -> PFGeneral:
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
        if isinstance(obj_or_path, str):
            return self.get_obj(obj_or_path, condition=condition,
                                parent_folder=parent_folder,
                                error_if_non_existent=error_if_non_existent,
                                include_subfolders=include_subfolders)
        elif not isinstance(obj_or_path, Iterable):
            return [obj_or_path]
        else:  # If all former conditions are False, it is assumed that the
            # input already was a list of PF object(s).
            return obj_or_path


    def handle_single_pf_object_or_path_input(
        self, 
        obj:Union[PFGeneral, str], 
        parent_folder:Union[PFGeneral, PFFolder, str] = None,
        error_if_non_existent:bool = True):
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
            return self.get_single_obj(obj, parent_folder=parent_folder,
                                       error_if_non_existent=error_if_non_existent)
        elif isinstance(obj, Iterable):
            elements_count = len(obj)
            if obj:
                first_obj_type = type(obj[0])
                try:
                    first_obj_path = self.get_path_of_object(obj[0])
                    msg_obj = (f"The first element is of type {first_obj_type} and its "
                               f"path is {first_obj_path}.")
                except (AttributeError):
                    msg_obj = f"The first element is of type {first_obj_type}."
                msg = (f"Expected a PowerFactory object or a path string. Instead an "
                       f"iterable of length {elements_count} is given. {msg_obj}")
                raise TypeError(msg)
            else:
                msg = (f"Expected a PowerFactory object or a path string. Instead an "
                       f"empty object of type '{type(obj).__name__}' is given.")
                raise TypeError(msg)
        else:  # If all former conditions are False, it is assumed that the
            # input already was a PF object.
            return obj


    def path_exists(self, 
                    path:str, 
                    parent:Union[PFGeneral, PFFolder, str]=None, 
                    return_info:bool=False):
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
        existing_path = ""
        child = parent
        for child_name in splitted_path:
            child = child.GetContents(f"{child_name}")
            if child:
                child = child[0]
                existing_path = f"{existing_path}\\{child.loc_name}"
            else:
                if not return_info:
                    return False
                else:
                    parent_path = parent.GetFullName()
                    parent_path = PFStringManipulation._remove_class_names(
                        parent_path)
                    existing_path = f"{parent_path}{existing_path}"
                    non_existent_child_name = child_name
                    return False, existing_path, non_existent_child_name
        return True
    
    
    def get_path_of_object(self, obj:PFGeneral) -> str:
        """
        Returns path relative to active project without class names.
        """
        return PFStringManipulation._format_full_path(str(obj), self.app)


    def get_path_of_object_with_class_names(self, obj:PFGeneral) -> str:
        obj = self.handle_single_pf_object_or_path_input(obj)
        return str(obj)


    def get_path_of_obj_with_class_names_relative_to_project(
        self, 
        obj:Union[PFGeneral, PFFolder, str]):
        obj = self.handle_single_pf_object_or_path_input(obj)
        return PFStringManipulation._get_path_inside_project_from_full_path(str(obj), self.app)
    

    def _replace_special_PF_characters_in_path_string(self, path:str):
        """Replaces special characters '$(ExtDataDir)','$(WorkspaceDir)','$(InstallationDir)'
        in a path string with their actual directories.
        """
        if "$(ExtDataDir)" in path:
            project_settings = self.get_project_settings()
            ext_data_dir = self.get_attr(project_settings, "extDataDir")
            path = path.replace("$(ExtDataDir)", ext_data_dir)
        path = path.replace("$(WorkspaceDir)",
                            self.app.GetWorkspaceDirectory())
        return path.replace("$(InstallationDir)", self.app.GetInstallationDirectory())


    def get_path_between_objects(
        self, 
        obj_high:Union[PFGeneral, PFProject, str], 
        obj_low:Union[PFGeneral, PFProject, str]) -> str:
        """Returns the path between two objects in the database.
        Arguments:
          object_high: Object higher in the hierarchy.
          object_low: Object lower in the hierarchy. 
        """
        obj_high = self.handle_single_pf_object_or_path_input(obj_high)
        obj_high = PFStringManipulation._format_full_path(str(obj_high), self.app)
        obj_low = self.handle_single_pf_object_or_path_input(obj_low)
        obj_low = PFStringManipulation._format_full_path(str(obj_low), self.app)
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

    
    def is_pf_class(self, class_name:str) -> bool:
        """Checks if class_name is a valid PF class (using the class ID).
        """
        return self.app.GetClassId(class_name) != 0
    
    
    def is_container(self, obj:Union[PFGeneral, PFFolder, str]):
        """Checks whether a PF object is a container. It is assumed
        that an object is a container if it has the attribute 'contents'.
        """
        obj = self.handle_single_pf_object_or_path_input(obj)
        return obj.HasAttribute("contents")
    

    def get_project_settings(self):
        """Returns project settings object.
        """
        project_settings_folder = self.get_single_obj("*.SetFold")
        return self.get_single_obj("*.SetPrj", parent_folder=project_settings_folder)    


class PFProject(PFFolder):
    
    def __init__(self, pf_app: PFApp):
        if pf_app:
            self.app:PFApp = pf_app
        else:
            raise TypeError("The input app is of type 'NoneType'. Maybe the PowerFactory app was not loaded correctly.") 
        
    
    @property
    def _folder(self):
        return self.get_active_project()    
    
    
    def get_first_level_folder(self, folder_type:str) -> PFGeneral:
        """Returns folder on first level of PF database.
        Currently the folder of the active user ('folder'='user') 
        or the global library ('folder'='global library') can be accessed.
        """
        if folder_type == "user":
            return self.get_active_user_folder()
        elif folder_type == "global library":
            return self.app.GetGlobalLibrary()
        else:
            raise TypeError(f"The first level folder {folder_type} is not valid. Use one of these: 'user', 'global library'.")


    def get_from_study_case(self, 
                            class_name: str, 
                            if_not_unique: str = "warning", if_no_study_case:str = "error") -> PFGeneral:
        '''Returns objects from active study case like the PF built-in function app.GetFromStudyCase(). 
        Additionally, this function outputs a warnings or errors if there is more than one object found and if no study case is activated.

        Arguments:
          class_name: class name of the object ('Class'), optionally preceded by an object name without wildcards and a dot ('Name.Class')
          if_not_unique: set to "warning" or "error" or None, depending on the wanted behavior if the returned object is not unique.
          if_no_study_case: set to "warning" or "error" or None, depending on the wanted behavior if no study case is active.
        Returns:
          Found or created object.
        '''
        study_case = self.app.GetActiveStudyCase()
        object = self.app.GetFromStudyCase(class_name)

        if not study_case:
            if if_no_study_case == "warning":
                warn("No study case activated. PowerFactory creates object of class_name in tmp folder, outside any study case.")
            elif if_no_study_case == "error":
                raise powfacpy.PFNoActiveStudyCaseError()

        if if_not_unique:
            if not '.' in class_name:
                search_string = "*." + class_name
            all_objects_of_this_class = self.get_obj(
                search_string, parent_folder=object.GetParent(), include_subfolders=False)
            if len(all_objects_of_this_class) > 1:
                parent_path = self.get_path_of_object(object.GetParent())
                if if_not_unique == "warning":
                    warn(f"The returned {class_name} object is not unique in its folder / in its study case: '{parent_path}'. Make sure that the correct {class_name} object is used.")
                if if_not_unique == "error":
                    raise TypeError(f"The returned {class_name} object is not unique in its folder / in its study case: '{parent_path}'")
        return object


    def get_active_project(self) -> IntPrj:
        """Returns the currently active project and throws an
        error if no prject has been activated.
        """
        active_project = self.app.GetActiveProject()
        if active_project:
            return active_project
        else:
            raise powfacpy.PFNotActiveError("a project")


    def get_active_user_folder(self) -> IntUser:
        """Return the folder of the active user.
        """
        parent = self.get_active_project()
        while not parent.GetClassName() == "IntUser":
            parent = parent.GetParent()
        return parent


    def get_active_networks(self, 
                            error_if_no_network_is_active:bool=True) -> ElmNet:
        """Get active networks/grids.  
        """
        grids = self.app.GetCalcRelevantObjects(
            ".ElmNet")  # This also returns the summary grid in the study case
        # Delete the summary grid which is in the study case
        grids[:] = [grid for grid in grids if not grid.GetParent().GetClassName()
                    == "IntCase"]
        if error_if_no_network_is_active and not grids:
            raise powfacpy.PFNotActiveError("a network (ElmNet).")
        return grids    
    
    
    def activate_study_case(self, path:str) -> IntCase:
        """Activate study case under path.
        """
        study_case = self.get_single_obj(path)
        study_case.Activate()
        return study_case


    def add_results_variable(self, 
                             obj:Union[PFGeneral, str], 
                             variables:list[str], 
                             results_obj:ElmRes=None):
        """Adds variables of the object to the PowerFactory results object (ElmRes)
        obj: PowerFactory object or its path
        """
        if not results_obj:
            results_obj = self.get_from_study_case("ElmRes")
        else:
            results_obj = self.handle_single_pf_object_or_path_input(
                results_obj)
        obj = self.handle_single_pf_object_or_path_input(obj)
        if isinstance(variables, str):
            variables = [variables]
        for var in variables:
            results_obj.AddVariable(obj, var)
        results_obj.Load()
        return results_obj
    

    def clear_elmres_from_objects_with_status_deleted(
        self, results_obj:ElmRes = None):
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


    def get_parameter_value_string(self, 
                                   parameters:dict, 
                                   delimiter=" ") -> str:
        param_value_string = ""
        for parname, path_with_par in parameters.items():
            value = self.get_attr_by_path(path_with_par)
            param_value_string += parname + "=" + str(value) + delimiter
        return param_value_string[:-len(delimiter)]  # omit last delimiter


    def create_comtrade_obj(self, 
                            file_path: str, 
                            parent_folder:Union[PFGeneral, str] = None) -> IntComtrade:
        """Add an IntComtrade that refers to file_path (*.cfg).
        The objects are stored in a folder "Comtrade" in the currently active
        study case, unless a parent_folder is provided. A new object is only
        created if there exists no object yet that points to the same file
        (f_name attribute is the file path). The file name is used for the
        new object name (without the .cfg ending).
        """
        if parent_folder:
            parent_folder = self.handle_single_pf_object_or_path_input(
                parent_folder)
        else:
            parent_folder = self.app.GetFromStudyCase("Comtrade.IntFolder")

        intcomtrade:IntComtrade = self.get_obj("*.IntComtrade",
                                   parent_folder=parent_folder,
                                   condition=lambda x: getattr(
                                       x, "f_name") == file_path,
                                   error_if_non_existent=False)
        if not intcomtrade:
            _, file_name = os_path.split(file_path)
            intcomtrade = self.create_in_folder(
                file_name.replace(".cfg", "") + ".IntComtrade",
                parent_folder,
                overwrite=False,
                use_existing=False)
            intcomtrade.f_name = file_path
        else:
            intcomtrade = intcomtrade[0]
        # intcomtrade.Load() probably not required
        return intcomtrade


    @staticmethod
    def replace_headers_of_csv_file_with_number_of_colums(file_path:str) -> int:
        """Replaces the first row (headers) of a csv file with its number of
        columns. This is needed for import of csv files to PF using ElmFile.
        """
        with open(file_path+".csv") as read_file, open(file_path + ".temp", "w") as write_file:
            columns_of_first_row = read_file.readline().split(",")
            if columns_of_first_row[-1] == "\n":
                columns_of_first_row = columns_of_first_row[:-1]
            # Minus one because first column is time and should not be counted.
            number_of_columns = len(columns_of_first_row)-1
            write_file.write(str(number_of_columns)+"\n")
            row = read_file.readline()
            while row:
                write_file.write(row)
                row = read_file.readline()
        replace(file_path + ".temp", file_path+".csv")
        return number_of_columns


    @staticmethod
    def insert_row_with_number_of_columns_in_csv_file(file_path:str) -> int:
        """Gets the number of columns of the first row in a csv file and
        inserts a row (first row) with this number in the first column.
        This is needed for ElmFile to read csv files.
        """
        with open(file_path+".csv") as read_file, open(file_path + ".temp", "w") as write_file:
            first_row = read_file.readline()
            columns_of_first_row = first_row.split(",")
            if columns_of_first_row[-1] == "\n":
                columns_of_first_row = columns_of_first_row[:-1]
            # Minus one because first column is time and should not be counted.
            number_of_columns = len(columns_of_first_row)-1
            write_file.write(str(number_of_columns)+"\n")
            write_file.write(first_row)
            row = read_file.readline()
            while row:
                write_file.write(row)
                row = read_file.readline()
        replace(file_path + ".temp", file_path+".csv")
        return number_of_columns


class PFBaseInterface(PFProject):
    pass


class PFStringManipulation:

    @staticmethod
    def replace_between_characters(char1, char2, replacement: str, original: str):
        """
        Example:
          Calling      
            powfacpy.PFStringManipulation.replace_between_characters(
              '.', 
              '\\', 
              '\\', 
              'username.IntUser\\pow.facpy.\\powfacpy.tests.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_base_interface\\Grid.ElmNet\\Terminal HV 1.ElmTerm'
          would give the output:
            'username\\pow.facpy\\powfacpy.tests\\Network Model\\Network Data\\test_base_interface\\Grid\\Terminal HV 1' 
          Note the behavior when there are several '.' in between '\\' 
          -> then the replacement starts after the last '.'
        """
        new_string = ""
        is_after_char_1 = False
        string_between_char_1_occurrences = ""
        for c in original:
            if c == char1:
                is_after_char_1 = True
                new_string += string_between_char_1_occurrences
                string_between_char_1_occurrences = ""
            elif c == char2:
                if is_after_char_1:
                    new_string += replacement
                else:
                    new_string += c
                string_between_char_1_occurrences = ""
                is_after_char_1 = False
            if is_after_char_1:
                string_between_char_1_occurrences += c
            elif not c == char2:
                new_string += c
        return new_string

    @staticmethod
    def _remove_class_names(path):
        return PFStringManipulation.replace_between_characters('.', '\\', '\\', path)

    @staticmethod
    def _get_path_inside_project_from_full_path(path: str, pf_app):
        """
        Takes the full path (including user and project) and returns the path 
        relative to the currently active project.
        Example:
          input path:  \\username.IntUser\\powfacpy_base.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\Grid.ElmNet\\Terminal 1.ElmTerm</l3>
          output: Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\Grid.ElmNet\\Terminal 1.ElmTerm
        """
        project_name = pf_app.GetActiveProject().loc_name + '.IntPrj\\'
        path = PFStringManipulation.truncate_until(path, project_name)
        # In case a closing tag occurs at the end of the path </l3> (e.g. when
        # str() is called on a PF object) make sure this is removed.
        if path[-1] == ">":
            path = path[0:path.rfind("<")]
        return path

    @staticmethod
    def truncate_until(original: str, string_pattern: str):
        """
        Truncate all characters until (and including) the occurence of string_pattern
        in original.
        """
        return original[original.find(string_pattern)+len(string_pattern):]

    @staticmethod
    def truncate_beginning(original: str, string_pattern: str):
        """
        Truncate string_pattern if it occurs at the beginning of the
        original string. Otherwise return original string.
        """
        index_where_pattern_begins = original.find(string_pattern)
        if index_where_pattern_begins == 0:
            return original[index_where_pattern_begins+len(string_pattern):]
        else:
            return original

    @staticmethod
    def _format_full_path(path, pf_app):
        """
        Takes the full path (including user and project) and returns the path 
        relative to the currently active project. Deletes class information.
        Example:
          input path:  \\username.IntUser\\powfacpy_base.IntPrj\\Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\Grid.ElmNet\\Terminal 1.ElmTerm
          output: Network Model\\Network Data\\Grid\\Terminal 1 
        """
        path = PFStringManipulation._get_path_inside_project_from_full_path(
            path, pf_app)
        return PFStringManipulation._remove_class_names(path)

    @staticmethod
    def _format_variable_name(name: str) -> str:
        """
        Takes PF-generated csv export variable name and returns shortened version.
        Example:
          name: 's:u0 in kV'
          output: 's:u0' 
        """
        return name.split(" ", 1)[0].replace("\"", "").replace("\n", "")  # get rid of description and quotation marks

    @staticmethod
    def handle_path(path):
        """Checks if path starts with \ (not accepted by most PF methods)
        and also if 'path' is of type string.
        """
        try:
            if not path[0] == "\\":
                return path
            else:
                return path[1:]
        except (TypeError):
            raise TypeError("Path must be of type string.")

    @staticmethod
    def replace_outside_or_inside_of_strings_in_a_string(
            string: str,
            replacements: dict,
            outside=True):
        """This method replaces parts of a string but only in the sections
        of the original string that are either outside of strings. This is best
        explained by example:
        "p HV load >= 2 and 'This is a string inside the string'"
        In this string the part 'This is a string inside the string'
        is a string inside the original string and no replacements are
        made in this part.

        Arguments:
          - string: The string that will be adjusted
          - replacements: key-value pairs of matching strings and their replacement
        """
        if outside:
            modulo_result = 0
        else:
            modulo_result = 1
        string = PFStringManipulation.split_but_keep_delimiter(string, "'")
        for n, part_of_string in enumerate(string):
            if n % 2 == modulo_result:  # Even elemnts store the parts that are outside strings
                for par_name, var_name in replacements.items():
                    part_of_string = part_of_string.replace(par_name, var_name)
                    string[n] = part_of_string
        return "".join(string).strip()

    @staticmethod
    def split_but_keep_delimiter(string: str, delimiter: str):
        """Uses the split() method to separate a string acoording
        to a delimiter, but keeps the delimiter in the
        separated strings (it is suprising that this is not optional
        in the split() method).
        Example:
          split_but_keep_delimiter(
            "p HV load >= 2 and (control 1 == 'A' and control 2 != 'S')",
            delimiter: "'")
          returns 
            ["p HV load >= 2 and (control 1 == '", "A'", " and control 2 != '", "S'", ')']
        """
        split_strings_list = [part + delimiter
                              for part in string.split(delimiter)]
        split_strings_list[-1] = split_strings_list[-1].rstrip(delimiter)
        return split_strings_list


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
        studycase_contents = powfacpy.PFTranslator.\
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
        name = powfacpy.PFTranslator.\
            _get_language_dependent_name_from_studycase(
                studycase=studycase,
                english_name="Graphics Board.SetDesktop",
                german_name="Grafiksammlung.SetDesktop",
            )
        return name

    @staticmethod
    def get_result_object_name_from_studycase(studycase):
        name = powfacpy.PFTranslator.\
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


def set_attr_of_obj(obj, attributes: dict):
    """Set attributes of object.
    The difference to set_attr of PFBaseInterface is that
    this method only accepts PF objects (and not path strings)
    and is slightly more performant.
    """
    for attr, value in attributes.items():
        obj.SetAttribute(attr, value)


def set_attr_of_objects(objects: Iterable, attributes: Iterable):
    """Set attributes of multiple objects.
    """
    for obj in objects:
        set_attr_of_obj(obj, attributes)


def set_attr_of_child(parent, child: str, attributes: dict):
    """Set attributes of a child object in parent.
    Just syntactic sugar.
    """
    child = parent.GetContents(child)[0]
    for attr, value in attributes.items():
        child.SetAttribute(attr, value)
