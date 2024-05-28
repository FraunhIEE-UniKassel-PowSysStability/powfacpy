"""Classes for interaction with the PF database. Based on folders from where downstream objects can accessed (see class PFFolder). The class PFActiveProject inherits from PFFolder and adds some functionality for the active project.

Also contains the class PFStringManipulation for string manipulation.

The acronym 'PF' is used for 'PowerFactory'.
"""
from __future__ import annotations
from collections.abc import Iterable
from typing import Union, Callable, Generator
from os import path as os_path
from functools import partial

from icecream import ic

import powfacpy
from powfacpy.pf_class_protocols import PFApp, PFGeneral, IntFolder, IntPrj, SetPrj, SetFilt
from powfacpy.string_manipulation import PFStringManipulation



class PFFolder():
    """Class for interacting with folders in the PowerFactory database (any folder in the hierarchy).
    
    The class is very large and has methods to (you can search for sections):
        - Get objects (search for '# Get') 
        - Create objects (search for '# Create')
        - Copy objects (search for '# Copy')
        - Delete objects (search for '# Delete')
        - Get/set attributes (search for '# Attributes')
        - Utils to handle user input etc. (search for '# Handle')
        - Utils to handle path strings (search for '# Path')
        - Other functionality (search for '# Other')
    
    The class is large to have a convenient interface with a lot of functionality to interact with the PF database (at the cost of the clarity of the code unfortunately)
    """
    
    def __init__(self, folder:Union[PFGeneral, str], pf_app:PFApp):
        if pf_app:
            self.app:PFApp = pf_app
        else:
            raise TypeError("The input app is of type 'NoneType'. Maybe the PowerFactory app was not loaded correctly.")   
        self._folder = self.app.GetActiveProject()
        if not self._folder:
            self._folder = self.app.GetCurrentUser()
        self._folder:PFGeneral = self._handle_single_pf_object_or_path_input(folder)
       
    
    def __getitem__(self, obj:str) -> PFGeneral:
        """Allows to call 'get_obj' (without optional arguments, i.e. subfolders are included) using brakets.
         
        Example: terminals = folder_instance['*.ElmTerm']
            where folder_instance is an instance of this class.

        Args:
            obj (str): Object(s) to search for

        Returns:
            PFGeneral: Pointers to object(s) from the PF database
        """
        return self.get_obj(obj, include_subfolders=True)
    
    
    def __iter__(self) -> Generator:
        for obj in self.get_obj("*", 
                                include_subfolders=False, error_if_non_existent=False):
            yield obj  
            
    
    def __str__(self) -> str:
        return str(self._folder)   
    
    
    def __len__(self) -> int:
        return len(self._folder.GetContents("*"))   
         

##################
# Reimplemenatation of methods of PF folder/container objects (to mimic the behavior of powerfactory.DataObject).
##################        
        
    def GetContents(self, name:str, recursive:int=0) -> list[PFGeneral]:
        return self._folder.GetContents(name, recursive)
        
    
    def GetChildren(self, hiddenMode:int, filter:str, subfolders:int) -> list[PFGeneral]:
        return self._folder.GetChildren(hiddenMode, filter, subfolders) 
    
    
    def GetAttribute(self, attr:str) -> Union[int|float|str|PFGeneral|list]:
        return  self._folder.GetAttribute(attr)
    
    
    def SetAttribute(self, attr:str, value:Union[int|float|str|PFGeneral|list]) -> None:
        return self._folder.SetAttribute(attr, value)    
    
    
    def GetParent(self) -> PFGeneral:
        return self._folder.GetParent()  
    
    
    def CreateObject(self, 
                     className:str, 
                     objectNameParts:Union[int, str]="") -> PFGeneral:
        return self._folder.CreateObject(className, objectNameParts)
    
    
    def Delete(self) -> int:
        return self._folder.Delete()      
        
    
    def AddCopy(self, 
                objectToCopy:list[PFGeneral] | PFGeneral, 
                partOfName: Union[str, int] ="") -> PFGeneral:
        return self._folder.AddCopy(objectToCopy, partOfName)    
        
    
    def GetFullName(self) -> str:
        return self._folder.GetFullName()     
    
       
##################
# Get
##################
    def get_obj(self, 
                path: str, 
                condition: Callable = None, 
                parent_folder: Union[PFGeneral, PFFolder, str] = None, 
                error_if_non_existent: bool = True,
                include_subfolders: bool = False) -> list[PFGeneral]:
        """Get the PowerFactory object(s) under 'path'. By default, 'path' is relative to 'self._folder' (or the active project folder for instances of PFActiveProject). 
        
        See also 'get_unique_obj'.

        Args:
            path (str): path to object(s), can contain wildcards ("*") after the last "\"
            
            condition (Callable, optional): filter for attributes etc.; example: "condition = lambda x : getattr(x,"uknom")==110; defaults to None
            
            parent_folder (Union[PFGeneral, PFFolder, str], optional): specify a parent folder/container (or its path) from where the search is started ('path' is then relativ to 'parent_folder'); defaults to _folder/the active project folder for instances of PFActiveProject
            
            error_if_non_existent (bool, optional): raise exception if no objects are found; defaults to True
            
            include_subfolders (bool, optional): include subfolders in the search; defaults to True

        Raises:
            TypeError: If 'path' is not a string

        Returns:
            list[PFGeneral]: List with PF objects

        Examples:
          pfbi.get_obj("Network Model\\Network Data\\Grid\\Terminal 1")
          
        The path can also start with "\\" and contain wildcards after last "\\":
          get_obj("\\Network Model\\Network Data\\Grid\\*.ElmTerm")
        
        With condition:   
          pfbi.get_obj("Network Model\\Network Data\\Grid\\*.ElmTerm"",
            condition = lambda x : getattr(x,"uknom")==110)

        Note that you can also use "r" at the beginning of the string
        argument to use single "\".  
        """
        parent_folder = self._folder if not parent_folder else self._handle_single_pf_object_or_path_input(parent_folder, include_subfolders=False)
        
        if not include_subfolders:
            try:
                obj = parent_folder.GetContents(path)
            except (RuntimeError):
                raise TypeError("Path must be of type string.")
        else:
            obj = self._handle_inclusion_of_subfolders(
                path, parent_folder, error_if_non_existent)
        if not obj:
            return self._handle_non_existing_obj(path, parent_folder, error_if_non_existent)
        if condition:
            obj_with_condition = self.get_by_condition(obj, condition)
            if obj_with_condition:
                return obj_with_condition
            else:
                return self._handle_condition_of_obj_not_met(path, parent_folder, error_if_non_existent)
        else:
            return obj    

    
    def get_obj_including_subfolders(
                self, 
                path: str, 
                condition: Callable=None, 
                parent_folder: Union[PFGeneral, PFFolder, str] = None, 
                error_if_non_existent: bool = True,
                include_subfolders: bool = False) -> list[PFGeneral]:
        """Call 'get_obj' including subfolders."""
        return self.get_obj(path,
                            condition=condition,
                            parent_folder=parent_folder,
                            error_if_non_existent=error_if_non_existent,
                            include_subfolders=True)
        
    
    def get_obj_partial(self, *args, **kwargs) -> Callable:
        """Partial evaluation of 'get_obj'.
        
        Returns a callable to get_obj.
        
        Example: a = get_obj_lazy("path\\to\\obj", error_if_non_existent=False)
                 a() # This calls 'get_obj' with given arguments
                 
        For further information arguments etc. see 'get_obj'.         
        """
        return partial(self.get_obj, *args, **kwargs)
        
    
    def get_unique_obj(self, 
                       path:str, 
                       parent_folder: Union[PFGeneral, PFFolder, str] = None, error_if_non_existent:bool = True,
                       include_subfolders:bool = False) -> PFGeneral:
        """Get unique PowerFactory object under 'path'. 
        
        Use this method if you want to access one single unique object.
        This method is an alterntive to 'get_obj' and returns the unique object instead of a list (that needs to be accessed with '[0]'). It also checks whether the found object is unique (only one object is found).  
        
        This method is equal to get_single_obj and was added because the method
        name fits better to what the method does (i.e. to get a unique object and to throw an error if the object is not unique).
        
        Args:
            path (str): path to object(s); can contain wildcards ("*") after the last "\"
                
            condition (Callable, optional): filter for attributes etc.; example: "condition = lambda x : getattr(x,"uknom")==110; defaults to None
                
            parent_folder (Union[PFGeneral, PFFolder, str], optional):  
            specify a parent folder/container (or its path) from where the search is started ('path' is then relativ to 'parent_folder'); defaults to _folder/the active project folder for instances of PFActiveProject
                
            error_if_non_existent (bool, optional): raise exception if no objects are found; defaults to True
                
            include_subfolders (bool, optional): include subfolders in the search; defaults to False

        Raises:
            TypeError: If 'path' is not a string or if several objects were found. 

        Returns:
            PFGeneral: PF object
        """
        return self.get_single_obj(path, 
                                   parent_folder=parent_folder,
                                   error_if_non_existent=error_if_non_existent,
                                   include_subfolders=include_subfolders)


    def get_single_obj(self, 
                       path:str, 
                       parent_folder:Union[PFGeneral, PFFolder, str] = None, error_if_non_existent:bool = True,
                       include_subfolders:bool = False) -> PFGeneral:
        """Get unique PowerFactory object under 'path'. 
        
        Use this method if you want to access one single unique object.
        This method is an alterntive to 'get_obj' and returns the unique object instead of a list (that needs to be accessed with '[0]'). It also checks whether the found object is unique (only one object is found).  
        
        Args:
            path (str): path to object(s); 
            can contain wildcards ("*") after the last "\"
                
            condition (Callable, optional): 
            filter for attributes etc.; example: "condition = lambda x : getattr(x,"uknom")==110; 
            defaults to None
                
            parent_folder (Union[PFGeneral, PFFolder, str], optional):  
            specify a parent folder/container (or its path) from where the search is started ('path' is then relativ to 'parent_folder');
            defaults to _folder/the active project folder for instances of PFActiveProject
                
            error_if_non_existent (bool, optional): 
            raise exception if no objects are found;
            defaults to True
                
            include_subfolders (bool, optional): 
            include subfolders in the search;
            defaults to True

        Raises:
            TypeError: 
            If 'path' is not a string.
            If several objects were found. 

        Returns:
            PFGeneral: PF object
        """    
        obj = self.get_obj(path, 
                           parent_folder=parent_folder,
                           error_if_non_existent=error_if_non_existent,
                           include_subfolders=include_subfolders)
        if obj:
            if len(obj) < 2:
                return obj[0]
            else:
                if parent_folder:     
                    parent_folder_str = f" in '{self.get_path_of_object(parent_folder)}'" 
                else:
                    parent_folder_str = ""
                raise TypeError(f"The path {path+parent_folder_str} is not a unique object. Did you use wildcards ('*')? This method only returns single unique objects.")
        else:
            return None


    def get_multiple_obj_from_similar_sub_directories(
        self, 
        parent_folders:Union[list[PFGeneral], str], 
        sub_path:str) -> list[PFGeneral]:
        """Get multiple objects that are in a similar subdirectory relativ to
        their parent folders

        Args:
            parent_folders (Union[list[PFGeneral], str]): parent folders
            
            sub_path (str): 
                path within the parent folders (string). Must be  unique (don't use placeholders '*')

        Returns:
            list[PFGeneral]: list of PF objects

        Example:
          If you want to get the "All calculation" objects of all the study cases in the study case folder, use
            'self.get_multiple_obj_from_similar_sub_directories(
              'Study Cases\\','All calculations')'    
        """
        if isinstance(parent_folders, str):
            parent_folders = self.get_obj(parent_folders)
        objs = []
        for parent in parent_folders:
            parent = self._handle_single_pf_object_or_path_input(parent)
            objs.append(self.get_single_obj(sub_path, parent_folder=parent))
        return objs


    def get_upstream_obj(self,
                         start_obj_or_path:Union[PFGeneral, str],
                         condition:Callable,
                         error_if_non_existent:bool=True) -> PFGeneral:
        """Get upstream object that meets the condition.
        
        Searches upstream in the PF database hierarchy.

        Args:
            start_obj_or_path (Union[PFGeneral, str], optional): Object/folder (or its path) to start from
                
            condition (Callable): Condition for the searched object  
              
            error_if_non_existent (bool, optional): If True, an exception is raised if no upstream object is found. Defaults to True.

        Returns:
            PFGeneral: The PF object found
        """        
        start_obj_or_path = self._folder if not start_obj_or_path else self._handle_single_pf_object_or_path_input(start_obj_or_path)
        obj_or_path = start_obj_or_path.GetParent()
        if obj_or_path:
            if condition(obj_or_path):
                return obj_or_path
            else:
                return self.get_upstream_obj(obj_or_path, condition, error_if_non_existent=error_if_non_existent)
        else:
            if error_if_non_existent:
                raise Exception(
                    "There is no upstream object that fullfills the condition.")
            else:
                return None
    

    def get_by_condition(self, 
                         objects:list[PFGeneral], 
                         condition:Callable) -> list[PFGeneral]:
        """Get objects (from a list of objects) which satisfy 'condition'.

        Args:
            objects (list[PFGeneral]): list of objects
            condition (Callable): e.g. lambda function

        Raises:
            powfacpy.PFAttributeError: If 'condition' queries attributes which an item in 'objects' does not have.
            TypeError: ToDo

        Returns:
            list[PFGeneral]: PF objects
        
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
                object_str = self.get_path_of_object(obj)
                raise TypeError(f"{e}. Maybe an unexpected type is used "
                                f"for attribute of object '{object_str}'.")
        return objects_true


##################
# Create
##################
    def create_by_path(self, path:str, overwrite:bool=True) -> PFGeneral:
        """Create an object by specifying its path (including the class at the end) and return the object.

        Args:
            path (str): path including class name at th end
            overwrite (bool, optional): Overwrite extisting object. Defaults to True.

        Raises:
            TypeError: If 'path' is not a string

        Returns:
            PFGeneral: The created object

        Example:
          pfbi.create_by_path('Library\\Dynamic Models\\dummy.BlkDef') 
        """
        try:
            folder_path, obj_name_incl_class = path.rsplit('\\', 1)
        except (AttributeError):
            raise TypeError("The argument 'path' must be of type string.")
        folder = self.get_single_obj(folder_path)
        return self.create_in_folder(obj_name_incl_class, folder, overwrite=overwrite)


    def create_in_folder(self, 
                         obj:str,
                         folder:Union[PFGeneral, PFFolder, str] = None, 
                         overwrite:bool = True, 
                         use_existing:bool = False) -> PFGeneral:
        """Create an object inside a folder and return the object.

        Args:
            obj (str): obj including class, e.g. 'model.BlkDef'
            
            folder (Union[PFGeneral, PFFolder, str], optional): Target folder. Defaults to None (i.e. 'self._folder')
            
            overwrite (bool, optional): objects with the same name will be overwritten. Defaults to True.
            
            use_existing (bool, optional): 
                Only relevant if 'overwrite' is False.
                If use_existing is False and an object with the same name exists, a new object with "(1)"/"(2)".. in its loc_name is created.
                If use_existing is True and an object with the same name exists, the method just returns the existing object.
                Defaults to False.
                
        Raises:
            TypeError: If 'obj' is not a string

        Returns:
            PFGeneral: The created object

        Example:
          pfbi.create_in_folder("dummy2.BlkDef", "Library\\Dynamic Models",)
        """
        folder = self._folder if not folder else self._handle_single_pf_object_or_path_input(folder)
        try:
            obj_name, _, class_name = obj.rpartition('.')
        except (AttributeError):
            raise TypeError("The argument 'obj' must be of type string.")
        if overwrite:
            self.delete_obj(obj, 
                            parent_folder=folder,
                            include_subfolders=False,
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
        """Create a directory of folders ('IntFolder') if the directory does not exist yet.

        Args:
            directory (str): path with folders
                Example: 'folder1\\folder2\\folder3'
            
            parent_folder (Union[PFGeneral, PFFolder, str], optional): Folder to start from. Defaults to None.

        Returns:
            IntFolder: the folder in the lowest subdirectory.  
        """
        if not self.path_exists(directory, parent=parent_folder):
            folder = self._folder if not parent_folder else parent_folder
            folder_names = directory.split("\\")
            for folder_name in folder_names:
                if not self.path_exists(folder_name, parent=folder):
                    folder = self.create_in_folder(
                        folder_name + ".IntFolder", folder)
                else:
                    folder = self.get_single_obj(
                        folder_name, 
                        parent_folder=folder, 
                        include_subfolders=False)
            return folder
        else:
            return self.get_single_obj(directory, 
                                       parent_folder=parent_folder,
                                       include_subfolders=False)
    
    
    def create_filter_obj(
        self,
        name: str, 
        folder: str | PFGeneral,
        object_filter: str,
        look_in: PFGeneral | str,
        expression: str, 
        include_subfolders: bool = True,
        only_calc_relevant_obj: bool = False,
        overwrite = True,
        use_existing = False) -> SetFilt:
        """Create filter object (SetFilt)

        Args:
            name (str): Name of filter object.
            
            folder (PFGeneral | PFFolder | str): target folder where filer is created.
        
            object_filter (str): Object/class filter (parameter 'objset'). Class names sparated by commas, e.g. '*.ElmTerm, *.ElmLne'.
            
            look_in (PFGeneral | str): Folder from which search is started (parameter 'pstart').
            
            expression (str): filter expression (parameter 'expr'), e.g. 'uknom>100.and.uknom<380.and.iUsage=0'
            
            include_subfolders (bool, optional): Include subfolders in search. Defaults to True.
            
            only_calc_relevant_obj (bool, optional): Search only for calc. relevant objects. Defaults to True.
            
            overwrite (bool, optional): Overwrite possible existing filter object. Defaults to True.
            
            use_existing (bool, optional): See description of 'create_in_folder' in 'PFFolder' class of powfacpy. Defaults to False.

        Returns:
            SetFilt: Filter object
        """ 
        
        filter_obj: SetFilt = self.create_in_folder(
            name + ".SetFilt", 
            folder=folder,
            overwrite=overwrite, 
            use_existing=use_existing)
        look_in = self._handle_single_pf_object_or_path_input(look_in)
        filter_obj.objset =  [object_filter]
        filter_obj.expr = expression
        filter_obj.pstart = look_in  
        filter_obj.isubfold = include_subfolders
        filter_obj.icalcrel = only_calc_relevant_obj
        return filter_obj
        
        
               


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
                 include_subfolders:bool=False) -> list[PFGeneral]:
        """Copy object(s) to 'target_folder'. 
        
        Uses 'get_obj' to get the objects under 'obj_or_path'. Source and target must be in the active project (otherwise use PasteCopy(), see scripting reference)
        
        See also 'copy_single_obj'.

        Args:
            obj_or_path (Union[PFGeneral, str]): 
                Objects to be copied (get_object is used)
                
            target_folder (Union[PFGeneral, PFFolder, str]): 
                Folder to which objects are copied
                
            overwrite (bool, optional): 
                Overwrite existing objects. Defaults to True.
                
            condition (Callable, optional): 
                Condition used in 'get_obj' for the source objects . Defaults to None.
                
            parent_folder (Union[PFGeneral, PFFolder, str], optional): 
                refers to the source folder and is used in combination with 'obj_or_path' to get the object(s) to be copied. Defaults to  None (i.e. '_folder'/active project is used).
                
            error_if_non_existent (bool, optional): 
                Raise error if no (source) objects are found. Defaults to True.
                
            include_subfolders (bool, optional): 
                Include subfolder in search for source objects. Defaults to False.

        Returns:
            list[PFGeneral]: Copied objects
        """
        obj = self._handle_pf_object_or_path_input(
            obj_or_path,
            condition=condition,
            parent_folder=parent_folder,
            error_if_non_existent=error_if_non_existent,
            include_subfolders=include_subfolders)
        target_folder = self._handle_single_pf_object_or_path_input(
            target_folder)
        if overwrite:
            for object_to_be_copied in obj:
                self.delete_obj(object_to_be_copied.GetAttribute("loc_name"),
                                parent_folder=target_folder, error_if_non_existent=False)
        # AddCopy() accepts a list of objects, but then it returns the target folder object and not the copied objects. Therefore, it is iterated through the objects.
        copied_obj = []
        for o in obj:
            copied_obj.append(target_folder.AddCopy(o))
        return copied_obj


    def copy_single_obj(self, 
                        obj_or_path:Union[PFGeneral, str], 
                        target_folder:Union[PFGeneral, PFFolder, str], 
                        overwrite:bool = True,
                        new_name:str = None, 
                        parent_folder:Union[PFGeneral, PFFolder, str] = None, error_if_non_existent:bool = True) -> PFGeneral:
        """Copy a single PF object to 'target_folder'
        
         Uses 'get_unique_obj' to get the object under 'obj_or_path'. Source and target must be in the active project (otherwise use PasteCopy(), see scripting reference)
        
        See also 'copy_obj'.

        Args:
            obj_or_path (Union[PFGeneral, str]): 
                Object to be copied (get_unique_object is used)
                
            target_folder (Union[PFGeneral, PFFolder, str]): 
                Folder to which object is copied
                
            overwrite (bool, optional): 
                Overwrite existing objects. Defaults to True.
                
            new_name (str, optional): 
                New name (if different to original). Defaults to None.
                
            parent_folder (Union[PFGeneral, PFFolder, str], optional): 
                refers to the source folder and is used in combination with 'obj_or_path' to get the object(s) to be copied. Defaults to  None (i.e. '_folder'/active project is used).
                
            error_if_non_existent (bool, optional): 
                Raise error if no (source) objects are found. Defaults to True.
                
            include_subfolders (bool, optional): 
                Include subfolder in search for source objects. Defaults to False.

        Returns:
            PFGeneral: Copied object/existing object if overwrite is False
        """
        obj = self._handle_single_pf_object_or_path_input(
            obj_or_path,
            parent_folder=parent_folder,
            error_if_non_existent=error_if_non_existent)
        target_folder = self._handle_single_pf_object_or_path_input(
            target_folder)
        if overwrite:
            if not new_name:
                self.delete_obj(obj.GetAttribute("loc_name"),
                                parent_folder=target_folder,
                                include_subfolders=False,
                                error_if_non_existent=False)
            else:
                self.delete_obj(f"{new_name}.*",
                                parent_folder=target_folder,
                                include_subfolders=False,
                                error_if_non_existent=False)
        else:
            existing_obj = self.get_single_obj(obj.GetAttribute("loc_name"),
                                parent_folder=target_folder, error_if_non_existent=False)  
            if existing_obj:
                return existing_obj      
        if new_name:
            return target_folder.AddCopy(obj, new_name)
        else:
            return target_folder.AddCopy(obj)
 
 
##################
# Delete
##################
    def delete_obj(self, 
                   obj_or_path:Union[PFGeneral, str], 
                   condition:Callable = None, 
                   parent_folder:Union[PFGeneral, str] = None, error_if_non_existent:bool = True,
                   include_subfolders:bool = False):
        """Delete PF object(s).
        
        In a first step, the objects are retrieved using the 'get_obj'
        method. In a second step, they are deleted. For further info on the input arguments, see the `get_obj` method. Checks whether objects were really deleted, otherwise tries to deactivate the object and then delete it.

        Args:
            obj_or_path (Union[PFGeneral, str]): objects to be deleted.
            
            condition (Callable, optional): 
                Condition for retrieved object(s). Defaults to None.
                
            parent_folder (Union[PFGeneral, str], optional): 
                Parent folder used in 'get_obj'. Defaults to None.
                
            error_if_non_existent (bool, optional): 
                Throw exception if not objects found. Defaults to True.
                
            include_subfolders (bool, optional): Search also in subfolders. Defaults to False.

        Raises:
            TypeError: If an object cannot be deleted.
        """
        obj = self._handle_pf_object_or_path_input(obj_or_path,
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
        """Clear all objects inside folder (including hidden objects).

        Args:
            folder (Union[PFGeneral, PFFolder, str], optional): Folder/ container objects or its path. Defaults to None (i.e. '_folder'/active project).
        """
        folder = self._folder if not folder else self._handle_single_pf_object_or_path_input(folder)
        self.delete_obj("*",
                        parent_folder=folder,
                        include_subfolders=False,
                        error_if_non_existent=False)

 
##################
# Attributes
##################
    def get_attr(self, 
                 obj:Union[PFGeneral, str], 
                 attr:str, 
                 parent_folder:Union[PFGeneral, PFFolder, str] = None) -> Union[int|float|str|PFGeneral|list]:
        """Get the value of an attribute of an object.

        Args:
            obj (Union[PFGeneral, str]): object or its path
            attr (str): attribute name
            parent_folder (Union[PFGeneral, PFFolder, str], optional):  
                - parent folder of object. Defaults to None.

        Raises:
            powfacpy.PFAttributeError: If ojbect does not have the specified attribute

        Returns:
            Union[int|float|str|PFGeneral|list]: Attribute value  
        
        Example:
            get_attr(terminal_1, "systype")
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


    def get_attr_by_path(self, path_with_attr:str) -> Union[int|float|str|PFGeneral|list]:
        """Get attribute using the path including the atrribute name

        Args:
            path_with_attr (str): path including the atrribute name
            Example: 'user\\project\\path\\to\\object\\m:Psum:bus1'

        Returns:
            Union[int|float|str|PFGeneral|list]: Attribute value  
        """
        head_tail = os_path.split(path_with_attr)
        return self.get_attr(head_tail[0], head_tail[1])


    def set_attr(self, 
                 obj:Union[PFGeneral, str], 
                 params:dict, 
                 parent_folder:Union[PFGeneral, PFFolder, str]=None) -> None:
        """Set the attribute(s) of an object.

        Args:
            obj (Union[PFGeneral, str]): PF object
            params (dict): atttributes and their values (e.g. {'parameter1':value1, 'parameter2':value2,..})
            parent_folder (Union[PFGeneral, PFFolder, str], optional): Parent folder object. Defaults to None.

        Raises:
            powfacpy.PFAttributeTypeError: If the type of an attribute value is wrong
            powfacpy.PFAttributeError: If an object does not have th especified attribute
        """
        obj = self._handle_single_pf_object_or_path_input(
            obj, parent_folder=parent_folder)
        for attr, value in params.items():
            try:
                obj.SetAttribute(attr, value)
            except (TypeError) as e:
                raise powfacpy.PFAttributeTypeError(obj, attr, e, self)
            except (AttributeError) as e:
                raise powfacpy.PFAttributeError(obj, e, self)


    def set_attr_by_path(self, 
                         path_with_attr:str, 
                         value:Union[int|float|str|PFGeneral|list]):
        """Set attribute using the path including the attribute name.

        Args:
            path_with_attr (str): path to ojbect with attribute name at the end
            value (Union[int | float | str | PFGeneral | list]): attribute value

        Example:
          set_attr_by_path(
                "Library\\Dynamic Models\\Linear_interpolation\\desc", 
                ["description"])
          Here 'desc' is the name of the attribute.  
        """
        head_tail = os_path.split(path_with_attr)
        self.set_attr(head_tail[0], {head_tail[1]: value})


##################
# Handle
##################
    def _handle_inclusion_of_subfolders(
        self, 
        path:str, 
        parent_folder:Union[PFGeneral, PFFolder, str], 
        error_if_non_existent:bool) -> Union[list, PFGeneral]:
        """Handle the inclusion of subfolders in search for objects.

        If subfolders are included, 'GetChildren' must be used instead of 'GetContents'. 'GetChildren' requires the input to be splitted between path and object name.
        
        Args:
            path (str): Path to object(s)
            
            parent_folder (Union[PFGeneral, PFFolder,str]): Parent folder where search is started
            
            error_if_non_existent (bool): Raise exception if no objects are found

        Raises:
            TypeError: If 'path' is not a string

        Returns:
            Union[list, PFGeneral]: Retrieved objects
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
                return self._handle_non_existing_obj(
                    head, parent_folder, error_if_non_existent)
        return parent_folder.GetChildren(1, tail, 1)

    
    def _handle_non_existing_obj(self, 
                                path:str, 
                                parent_folder:Union[PFGeneral, PFFolder, str], error_if_non_existent:bool) -> list:
        """Handle the attempted access to a non existent object.

        Args:
            path (str): path to object
            
            parent_folder (Union[PFGeneral, PFFolder, str]): search is started from here
            
            error_if_non_existent (bool): raise exception if non existent

        Raises:
            powfacpy.PFPathError: if 'error_if_non_existent' is True

        Returns:
            list: empty list if 'error_if_non_existent' is False
        """
        if not error_if_non_existent:
            return []
        else:
            exists_bool, existing_path, non_existing_child = self.path_exists(
                path, parent_folder, return_info=True)
            raise powfacpy.PFPathError(non_existing_child, existing_path)


    def _handle_condition_of_obj_not_met(
        self, 
        path:str, 
        parent_folder:Union[PFGeneral, PFFolder], 
        error_if_non_existent:bool) -> list | None:
        """Handle the attempted access to an object with a specific condition, when such object(s) were found, but none of them meets the condition.

        Args:
            path (str): path of the object(s)
            
            obj (list[Union[PFGeneral, PFFolder]]): list of objects found using path, but none of them satisfies the condition
            
            error_if_non_existent (bool): raise exception

        Raises:
            powfacpy.PFNonExistingObjectError: If 'error_if_non_existent' is True

        Returns:
            list | None: empty list
        """
        if not error_if_non_existent:
            return []
        else:
            # head, tail = os_path.split(path)
            raise powfacpy.PFNonExistingObjectError(
                parent_folder, path, condition=True)
    

    def _handle_pf_object_or_path_input(
        self, 
        obj_or_path:Union[PFGeneral, str], 
        condition:bool=None, 
        parent_folder:Union[PFGeneral, PFFolder, str]=None,
        error_if_non_existent:bool=True, 
        include_subfolders:bool=False) -> PFGeneral | list[PFGeneral]:
        """Handles the input argument 'obj_or_path' when a method accepts either
          - a path string
          - a PF object
          - an iterable (of PF objects) 
          
        Note: Unfortunately, it cannot be checked whether 'obj' is a PF DataObject, because the module powerfactory is not available.

        See also '_handle_single_pf_object_or_path_input'  

        Args:
            obj_or_path (Union[PFGeneral, str]): see get_obj
            
            condition (bool, optional): see get_obj. Defaults to None.
            parent_folder (Union[PFGeneral, PFFolder, str], optional): see get_obj. Defaults to None.
            
            error_if_non_existent (bool, optional): see get_obj. Defaults to True.
            
            include_subfolders (bool, optional): see get_obj. Defaults to False.

        Returns:
            PFGeneral: 
                - PF object(s) in a list. 
                - If 'obj_or_path' is a path string, it returns the PF object(s) of that path.
                - If 'obj_or_path' is a PF object (or multiple), it does nothing and just returns the object(s).
        """
        if isinstance(obj_or_path, str):
            return self.get_obj(obj_or_path, condition=condition,
                                parent_folder=parent_folder,
                                error_if_non_existent=error_if_non_existent,
                                include_subfolders=include_subfolders)
        elif not isinstance(obj_or_path, Iterable):
            return [obj_or_path]
        elif not isinstance(obj_or_path[0], str):
            return obj_or_path    
        else: 
            objs = []
            for obj in obj_or_path:
                objs += self.get_obj(obj)
            return objs
            


    def _handle_single_pf_object_or_path_input(
        self, 
        obj_or_path:Union[PFGeneral, str], 
        parent_folder:Union[PFGeneral, PFFolder, str] = None,
        error_if_non_existent:bool = True,
        include_subfolders:bool = False) -> PFGeneral:
        """Handles the input argument when a method accepts either
          - a path string
          - or a PF object
          - but NOT an iterable of PF objects (difference to    _handle_pf_object_or_path_input)
          
        Note: Unfortunately, it cannot be checked whether 'obj' is a PF DataObject, because the module powerfactory is not available.

        See also method 'handle_pf_object_path_input'  

        Args:
            obj (Union[PFGeneral, str]): see get_single_obj
            
            parent_folder (Union[PFGeneral, PFFolder, str], optional): get_single_obj. Defaults to None.
            
            error_if_non_existent (bool, optional): get_single_obj. Defaults to True.

        Raises:
            TypeError: If 'obj_or_path' is an iterable (unexpected), a meaningfull error is raised.

        Returns:
            PFGeneral: If 'obj_or_path' is a path string, it returns the PF object of that path.
            If 'obj_or_path' is a PF object, it does nothing and just returns the object.
        """
        if isinstance(obj_or_path, str):
            return self.get_single_obj(
                obj_or_path, 
                parent_folder=parent_folder,
                error_if_non_existent=error_if_non_existent,
                include_subfolders=include_subfolders)
        elif isinstance(obj_or_path, Iterable) and not isinstance(obj_or_path, powfacpy.PFFolder):
            elements_count = len(obj_or_path)
            if obj_or_path:
                first_obj_type = type(obj_or_path[0])
                try:
                    first_obj_path = self.get_path_of_object(obj_or_path[0])
                    msg_obj = (f"The first element is of type {first_obj_type} and its path is {first_obj_path}.")
                except (AttributeError):
                    msg_obj = f"The first element is of type {first_obj_type}."
                msg = (f"Expected a PowerFactory object or a path string. Instead an iterable of length {elements_count} is given. {msg_obj}")
                raise TypeError(msg)
            else:
                msg = (f"Expected a PowerFactory object or a path string. Instead an empty object of type '{type(obj_or_path).__name__}' is given.")
                raise TypeError(msg)
        else:  # If all former conditions are False, it is assumed that the
            # input already was a PF object.
            return obj_or_path


######################
# Paths
######################
    def path_exists(self, 
                    path:str, 
                    parent:Union[PFGeneral, PFFolder, str] = None, 
                    return_info:bool=False) -> bool:
        """Check if the path exists.

        Args:
            path (str): path
            
            parent (Union[PFGeneral, PFFolder, str], optional): Parent folder where search is started. Defaults to None (i.e. 'self._folder').
            
            return_info (bool, optional): information about where the path is
            corrupted is returned. Defaults to False.

        Raises:
            powfacpy.PFPathInputError: If path is invalid.

        Returns:
            bool: True if path exists
        """
        
        parent = self._folder if not parent else self._handle_single_pf_object_or_path_input(parent)
        
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
                    parent_path = PFStringManipulation.remove_class_names(
                        parent_path)
                    existing_path = f"{parent_path}{existing_path}"
                    non_existent_child_name = child_name
                    return False, existing_path, non_existent_child_name
        return True
    
    
    def get_path_of_object(self, obj:Union[PFGeneral, PFFolder]) -> str:
        """Get path relative to 'self._folder' without class names.
        
        Args:
            obj (PFGeneral): PF object

        Returns:
            str: path
        """
        obj = self._handle_single_pf_object_or_path_input(obj)
        return PFStringManipulation.remove_class_names(self.get_path_of_obj_with_class_names(obj))


    def get_path_of_obj_with_class_names(
        self, 
        obj:Union[PFGeneral, PFFolder, str]) -> str:
        """Get path relative to 'self._folder' including class names.

        Args:
            obj (Union[PFGeneral, PFFolder, str]): PF object

        Returns:
            str: path
        """
        _folder_path_without_closing_tag = PFStringManipulation.remove_closing_html_tag_from_path(str(self._folder))
        obj = self._handle_single_pf_object_or_path_input(obj)
        obj_str = PFStringManipulation.remove_closing_html_tag_from_path(str(obj))
        return PFStringManipulation.truncate_beginning(
            obj_str, _folder_path_without_closing_tag)
    

    def get_full_path_of_object(self, obj:Union[PFGeneral, PFFolder]) -> str:
        """Get full path in PF database without class names.

        Args:
            obj (PFGeneral): PF object

        Returns:
            str: path
        """
        obj = self.get_full_path_of_object_with_class_names(obj)
        return PFStringManipulation.remove_class_names(obj)
    
    
    def get_full_path_of_object_with_class_names(
        self, 
        obj:Union[PFGeneral, PFFolder, str]) -> str:
        """Get path in PF database including class names.

        Args:
            obj (PFGeneral): PF object

        Returns:
            str: path
        """
        obj = self._handle_single_pf_object_or_path_input(obj)
        return PFStringManipulation.remove_html_tags_from_path(str(obj))
    
    
    def get_path_of_object_in_active_project(
        self, 
        obj:Union[PFGeneral, PFFolder, str]) -> str:
        """Get path relative to active project without class names.
        
        Args:
            obj (PFGeneral): PF object

        Returns:
            str: path
        """
        obj = self.get_path_of_object_in_active_project_with_class_names(obj)
        return PFStringManipulation.remove_class_names(obj)
    
    
    def get_path_of_object_in_active_project_with_class_names(
        self, 
        obj:Union[PFGeneral, PFFolder, str]) -> str:
        """Get path relative to active project including class names.

        Args:
            obj (Union[PFGeneral, PFFolder, str]): PF object or its path

        Returns:
            str: path
        """
        active_project_path = PFStringManipulation.remove_closing_html_tag_from_path(str(self.app.GetActiveProject()))
        obj = self._handle_single_pf_object_or_path_input(obj)
        obj_str = PFStringManipulation.remove_closing_html_tag_from_path(str(obj))
        return PFStringManipulation.truncate_beginning(
            obj_str, active_project_path)
    

    def _replace_special_PF_characters_in_path_string(self, path:str) -> str:
        """Replaces special characters '$(ExtDataDir)','$(WorkspaceDir)','$(InstallationDir)' in path with their actual directories.
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
        obj_high:Union[PFGeneral, PFFolder, str], 
        obj_low:Union[PFGeneral, PFFolder, str]) -> str:
        """Get path between two objects in the PF database.

        Args:
            obj_high (Union[PFGeneral, PFFolder, str]): object higher in the hierarchy
            obj_low (Union[PFGeneral, PFFolder, str]): object lower in the hierarchy

        Returns:
            str: path between
        """
        obj_high = self._handle_single_pf_object_or_path_input(obj_high)
        obj_high = self.get_path_of_object(obj_high)
        obj_low = self._handle_single_pf_object_or_path_input(obj_low)
        obj_low = self.get_path_of_object(obj_low)
        path = str(obj_low).split(str(obj_high))[1][1:]
        return path


    @staticmethod
    def get_loc_name_with_class(
        objects:Union[PFGeneral, list[PFGeneral]]) -> Union[str, list[str]]:
        """Get local name (loc_name) including class.

        Args:
            objects (Union[PFGeneral, list[PFGeneral]]): PF objects(s)

        Returns:
            Union[str, list[str]]: local name(s)
        """
        is_list = True
        if not type(objects) == list:
            objects = [objects,]
            is_list = False

        loc_name_with_class = []
        for powerfactory_object in objects:
            loc_name_with_class.append(
                powerfactory_object.loc_name
                + '.'
                + powerfactory_object.GetClassName())

        if not is_list:
            loc_name_with_class = loc_name_with_class[0]
        return loc_name_with_class


#####################
# Other
#####################   
    def is_pf_class(self, class_name: str) -> bool:
        """Checks if class_name is a valid PF class (using the class ID).
        """
        return self.app.GetClassId(class_name) != 0
    
    
    def is_container(self, obj:Union[PFGeneral, PFFolder, str]) -> bool:
        """Checks whether a PF object is a container. It is assumed
        that an object is a container if it has the attribute 'contents'.
        """
        obj = self._handle_single_pf_object_or_path_input(obj)
        return obj.HasAttribute("contents")
    

    def get_project_settings(self) -> SetPrj:
        """Get project settings object.
        """
        project_settings_folder = self.get_single_obj("*.SetFold")
        return self.get_single_obj(
            "*.SetPrj", parent_folder=project_settings_folder)  
        
    
    def get_active_project(self) -> IntPrj:
        """Get currently active project. Throw an error if no project is active.
        """
        active_project = self.app.GetActiveProject()
        if active_project:
            return active_project
        else:
            raise powfacpy.PFNotActiveError("a project")      

