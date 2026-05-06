Module powfacpy.base.folder
===========================
Classes for interaction with the PF database. Based on folders from where downstream objects can accessed (see class Folder). The class PFActiveProject inherits from Folder and adds some functionality for the active project.

Also contains the class PFStringManipulation for string manipulation.

The acronym 'PF' is used for 'PowerFactory'.

Classes
-------

`Folder(folder: Union[PFGeneral, str], pf_app: PFApp | None | bool = False)`
:   Class for interacting with folders in the PowerFactory database (any folder in the hierarchy).
    
    The class is very large and has methods to (you can search for sections):
        - Get objects (search for '# Get')
        - Create objects (search for '# Create')
        - Copy objects (search for '# Copy')
        - Delete objects (search for '# Delete')
        - Get/set attributes (search for '# Attributes')
        - Utils to handle user input etc. (search for '# Handle')
        - Utils to handle path strings (search for '# Path')
        - Other functionality (search for '# Other')
    
    The class is large to have a convenient interface with a lot of functionality to interact with the PF database (at the cost of the clarity of the code unfortunately).
    
    Note that 'app' is a class attribute, i.e. it is shared by all instances. This is convenient because there is only one 'app' object provided by 'powerfactory.GetApplication()'
    
    Args:
        folder (Union[PFGeneral, str]): folder object or path in active project (or in active user if no project is active)
        pf_app (PFApp | None | bool, optional): Powerfactory app (returned by GetApplication). Defaults to False (does not default to None because None is returned by GetApplication if something goes wrong; Therefore, None should raise an exception).
    
    Raises:
        TypeError: When pf_app is None. See explanation of argument 'pf_app'.

    ### Ancestors (in MRO)

    * powfacpy.base.base.BaseObjectStatic

    ### Descendants

    * powfacpy.base.active_project.ActiveProject

    ### Class variables

    `app: powfacpy.pf_classes.protocols.PFApp`
    :   The type of the None singleton.

    ### Static methods

    `get_loc_name_with_class(objects: Union[PFGeneral, list[PFGeneral]]) ‑> str | list[str]`
    :   Get local name (loc_name) including class.
        
        Args:
            objects (Union[PFGeneral, list[PFGeneral]]): PF objects(s)
        
        Returns:
            Union[str, list[str]]: local name(s)

    ### Instance variables

    `folder_obj`
    :

    `obj: PFGeneral`
    :

    ### Methods

    `AddCopy(self, objectToCopy: list[PFGeneral] | PFGeneral, partOfName: Union[str, int] = '') ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :

    `CreateObject(self, className: str, objectNameParts: Union[int, str] = '') ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :

    `Delete(self) ‑> int`
    :

    `GetAttribute(self, attr: str) ‑> int | float | str | powfacpy.pf_classes.protocols.PFGeneral | list`
    :

    `GetChildren(self, hiddenMode: int, filter: str, subfolders: int) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :

    `GetContents(self, name: str, recursive: int = 0) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :

    `GetFullName(self) ‑> str`
    :

    `GetParent(self) ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :

    `SetAttribute(self, attr: str, value: Union[int | float | str | PFGeneral | list]) ‑> None`
    :

    `clear_folder(self, folder: Union[PFGeneral, Folder, str] = None)`
    :   Clear all objects inside folder (including hidden objects).
        
        Args:
            folder (Union[PFGeneral, Folder, str], optional): Folder/ container objects or its path. Defaults to None (i.e. '_folder'/active project).

    `copy_obj(self, obj_or_path: Union[PFGeneral, str, list[PFGeneral]], target_folder: Union[PFGeneral, Folder], overwrite: bool = True, condition: Callable = None, parent_folder: Union[PFGeneral, Folder, str] = None, error_if_non_existent: bool = True, include_subfolders: bool = False) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Copy object(s) to 'target_folder'.
        
        Uses 'get_obj' to get the objects under 'obj_or_path'. Source and target must be in the active project (otherwise use PasteCopy(), see scripting reference)
        
        See also 'copy_single_obj'.
        
        Args:
            obj_or_path (Union[PFGeneral, str]):
                Objects to be copied (get_obj is used for strings)
        
            target_folder (Union[PFGeneral, Folder, str]):
                Folder to which objects are copied
        
            overwrite (bool, optional):
                Overwrite existing objects. Defaults to True.
        
            condition (Callable, optional):
                Condition used in 'get_obj' for the source objects . Defaults to None.
        
            parent_folder (Union[PFGeneral, Folder, str], optional):
                refers to the source folder and is used in combination with 'obj_or_path' to get the object(s) to be copied. Defaults to  None (i.e. '_folder'/active project is used).
        
            error_if_non_existent (bool, optional):
                Raise error if no (source) objects are found. Defaults to True.
        
            include_subfolders (bool, optional):
                Include subfolder in search for source objects. Defaults to False.
        
        Returns:
            list[PFGeneral]: Copied objects

    `copy_project(self, project_or_path_in_current_user: PFGeneral | str | None = None, target_folder_or_path_in_current_user: PFGeneral | str | None = None, overwrite: bool = True, use_existing: bool = False, new_name: str = None, error_if_non_existent: bool = True) ‑> powfacpy.pf_classes.protocols.IntPrj`
    :

    `copy_single_obj(self, obj_or_path: Union[PFGeneral, str], target_folder: Union[PFGeneral, Folder, str], overwrite: bool = True, use_existing: bool = False, new_name: str = None, parent_folder: Union[PFGeneral, Folder, str] = None, error_if_non_existent: bool = True) ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :   Copy a single PF object to 'target_folder'
        
         Uses 'get_unique_obj' to get the object under 'obj_or_path'. Source and target must be in the active project (otherwise use PasteCopy(), see scripting reference)
        
        See also 'copy_obj'.
        
        Args:
            obj_or_path (Union[PFGeneral, str]):
                Object to be copied (get_unique_obj is used for strings)
        
            target_folder (Union[PFGeneral, Folder, str]):
                Folder to which object is copied
        
            overwrite (bool, optional):
                Overwrite existing objects. Defaults to True.
        
            use_existing (bool, optional):
                If an object with the same name exists, a new object with "(1)"/"(2)".. in its loc_name is created.
                If use_existing is True and an object with the same name exists, the method just returns the existing object.
                Defaults to False.
        
            new_name (str, optional):
                New name (if different to original). Defaults to None.
        
            parent_folder (Union[PFGeneral, Folder, str], optional):
                refers to the source folder and is used in combination with 'obj_or_path' to get the object(s) to be copied. Defaults to  None (i.e. '_folder'/active project is used).
        
            error_if_non_existent (bool, optional):
                Raise error if no (source) objects are found. Defaults to True.
        
            include_subfolders (bool, optional):
                Include subfolder in search for source objects. Defaults to False.
        
        Returns:
            PFGeneral: Copied object/existing object if overwrite is False

    `create_by_path(self, path: str, overwrite: bool = True, use_existing: bool = False) ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :   Create an object by specifying its path (including the class at the end) and return the object.
        
        Args:
            path (str): path including class name at the end.
            overwrite (bool, optional): Overwrite existing object. Defaults to True.
        
        Raises:
            TypeError: If 'path' is not a string
        
        Returns:
            PFGeneral: The created object
        
        Example:
          pfbi.create_by_path('Library\Dynamic Models\dummy.BlkDef')

    `create_directory(self, directory: str, parent_folder: Union[PFGeneral, Folder, str] = None) ‑> powfacpy.pf_classes.protocols.IntFolder`
    :   Create a directory of folders ('IntFolder') if the directory does not exist yet.
        
        Similar to 'mkdir' command in Windows.
        
        Args:
            directory (str): path with folders
                Example: 'folder1\folder2\folder3'
        
            parent_folder (Union[PFGeneral, Folder, str], optional): Folder to start from. Defaults to None.
        
        Returns:
            IntFolder: the folder in the lowest subdirectory.

    `create_filter_obj(self, name: str, folder: str | PFGeneral, object_filter: str, look_in: PFGeneral | str, expression: str, include_subfolders: bool = True, only_calc_relevant_obj: bool = False, overwrite=True, use_existing=False) ‑> powfacpy.pf_classes.protocols.SetFilt`
    :   Create filter object (SetFilt)
        
        Args:
            name (str): Name of filter object.
        
            folder (PFGeneral | Folder | str): target folder where filer is created.
        
            object_filter (str): Object/class filter (parameter 'objset'). Class names sparated by commas, e.g. '*.ElmTerm, *.ElmLne'.
        
            look_in (PFGeneral | str): Folder from which search is started (parameter 'pstart').
        
            expression (str): filter expression (parameter 'expr'), e.g. 'uknom>100.and.uknom<380.and.iUsage=0'
        
            include_subfolders (bool, optional): Include subfolders in search. Defaults to True.
        
            only_calc_relevant_obj (bool, optional): Search only for calc. relevant objects. Defaults to True.
        
            overwrite (bool, optional): Overwrite possible existing filter object. Defaults to True.
        
            use_existing (bool, optional): See description of 'create_in_folder' in 'Folder' class of powfacpy. Defaults to False.
        
        Returns:
            SetFilt: Filter object

    `create_in_folder(self, obj: str, folder: PFGeneral | Folder | str = None, overwrite: bool = True, use_existing: bool = False) ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :   Create an object inside a folder and return the object.
        
        Args:
            obj (str): obj including class, e.g. 'model.BlkDef'
        
            folder (Union[PFGeneral, Folder, str], optional): Target folder. Defaults to None (i.e. 'self._obj')
        
            overwrite (bool, optional): objects with the same name will be overwritten. Defaults to True.
        
            use_existing (bool, optional):
                If an object with the same name exists, a new object with "(1)"/"(2)".. in its loc_name is created.
                If use_existing is True and an object with the same name exists, the method just returns the existing object.
                Defaults to False.
        
        Raises:
            TypeError: If 'obj' is not a string
        
        Returns:
            PFGeneral: The created object
        
        Example:
          folder.create_in_folder("dummy2.BlkDef", "Library\Dynamic Models",)

    `delete_obj(self, obj_or_path: Union[PFGeneral, str], condition: Callable = None, parent_folder: Union[PFGeneral, str] = None, error_if_non_existent: bool = True, include_subfolders: bool = False)`
    :   Delete PF object(s).
        
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

    `get_active_project(self) ‑> powfacpy.pf_classes.protocols.IntPrj`
    :   Get currently active project. Throw an error if no project is active.

    `get_attr(self, obj: Union[PFGeneral, str], attr: str, parent_folder: Union[PFGeneral, Folder, str] = None) ‑> int | float | str | powfacpy.pf_classes.protocols.PFGeneral | list`
    :   Get the value of an attribute of an object.
        
        Args:
            obj (Union[PFGeneral, str]): object or its path
            attr (str): attribute name
            parent_folder (Union[PFGeneral, Folder, str], optional):
                - parent folder of object. Defaults to None.
        
        Raises:
            PFAttributeError: If ojbect does not have the specified attribute
        
        Returns:
            Union[int|float|str|PFGeneral|list]: Attribute value
        
        Example:
            get_attr(terminal_1, "systype")

    `get_attr_by_path(self, path_with_attr: str) ‑> int | float | str | powfacpy.pf_classes.protocols.PFGeneral | list`
    :   Get attribute using the path including the atrribute name
        
        Args:
            path_with_attr (str): path including the atrribute name
            Example: 'user\project\path\to\object\m:Psum:bus1'
        
        Returns:
            Union[int|float|str|PFGeneral|list]: Attribute value

    `get_by_condition(self, objects: list[PFGeneral], condition: Callable) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Get objects (from a list of objects) which satisfy 'condition'.
        
        Args:
            objects (list[PFGeneral]): list of objects
            condition (Callable): e.g. lambda function
        
        Raises:
            PFAttributeError: If 'condition' queries attributes which an item in 'objects' does not have.
            TypeError: ToDo
        
        Returns:
            list[PFGeneral]: PF objects
        
        Example:
          pfbi.get_by_condition(list_of_objects, lambda x : getattr(x,"uknom")==110)

    `get_current_user(self)`
    :

    `get_external_data_directory(self) ‑> str`
    :

    `get_full_path_of_object(self, obj: Union[PFGeneral, Folder]) ‑> str`
    :   Get full path in PF database without class names.
        
        Args:
            obj (PFGeneral): PF object
        
        Returns:
            str: path

    `get_full_path_of_object_with_class_names(self, obj: Union[PFGeneral, Folder, str]) ‑> str`
    :   Get path in PF database including class names.
        
        Args:
            obj (PFGeneral): PF object
        
        Returns:
            str: path

    `get_installation_directory(self) ‑> str`
    :

    `get_multiple_obj_from_similar_sub_directories(self, parent_folders: Union[list[PFGeneral], str], sub_path: str) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Get multiple objects that are in a similar subdirectory relativ to
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
              'Study Cases\','All calculations')'

    `get_obj(self, path: str, condition: Callable | None = None, parent_folder: Union[PFGeneral, Folder, str] | None = None, error_if_non_existent: bool = True, include_subfolders: bool = False) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Get the PowerFactory object(s) under 'path'. By default, 'path' is relative to 'self._obj' (or the active project folder for instances of PFActiveProject).
        
        See also 'get_unique_obj'.
        
        Args:
            path (str): path to object(s), can contain wildcards ("*") after the last ""
        
            condition (Callable, optional): filter for attributes etc.; example: "condition = lambda x : getattr(x,"uknom")==110; defaults to None
        
            parent_folder (Union[PFGeneral, Folder, str], optional): specify a parent folder/container (or its path) from where the search is started ('path' is then relative to 'parent_folder'); defaults to _folder/the active project folder for instances of PFActiveProject
        
            error_if_non_existent (bool, optional): raise exception if no objects are found; defaults to True
        
            include_subfolders (bool, optional): include subfolders in the search; defaults to True
        
        Raises:
            TypeError: If 'path' is not a string
        
        Returns:
            list[PFGeneral]: List with PF objects
        
        Examples:
          pfbi.get_obj("Network Model\Network Data\Grid\Terminal 1")
        
        The path can also start with "\" and contain wildcards after last "\":
          get_obj("\Network Model\Network Data\Grid\*.ElmTerm")
        
        With condition:
          pfbi.get_obj("Network Model\Network Data\Grid\*.ElmTerm"",
            condition = lambda x : getattr(x,"uknom")==110)
        
        Note that you can also use "r" at the beginning of the string
        argument to use single "".

    `get_obj_including_subfolders(self, path: str, condition: Callable | None = None, parent_folder: Union[PFGeneral, Folder, str] | None = None, error_if_non_existent: bool = True) ‑> list[powfacpy.pf_classes.protocols.PFGeneral]`
    :   Call 'get_obj' including subfolders.

    `get_obj_partial(self, *args, **kwargs) ‑> Callable`
    :   Partial evaluation of 'get_obj'.
        
        Returns a callable to get_obj.
        
        Example: a = get_obj_lazy("path\to\obj", error_if_non_existent=False)
                 a() # This calls 'get_obj' with given arguments
        
        For further information arguments etc. see 'get_obj'.

    `get_path_between_objects(self, obj_high: Union[PFGeneral, Folder, str], obj_low: Union[PFGeneral, Folder, str]) ‑> str`
    :   Get path between two objects in the PF database.
        
        Args:
            obj_high (Union[PFGeneral, Folder, str]): object higher in the hierarchy
            obj_low (Union[PFGeneral, Folder, str]): object lower in the hierarchy
        
        Returns:
            str: path between

    `get_path_of_obj_with_class_names(self, obj: Union[PFGeneral, Folder, str]) ‑> str`
    :   Get path relative to 'self._obj' including class names.
        
        Args:
            obj (Union[PFGeneral, Folder, str]): PF object
        
        Returns:
            str: path

    `get_path_of_object(self, obj: Union[PFGeneral, Folder]) ‑> str`
    :   Get path relative to 'self._obj' without class names.
        
        Args:
            obj (PFGeneral): PF object
        
        Returns:
            str: path

    `get_path_of_object_in_active_project(self, obj: Union[PFGeneral, Folder, str]) ‑> str`
    :   Get path relative to active project without class names.
        
        Args:
            obj (PFGeneral): PF object
        
        Returns:
            str: path

    `get_path_of_object_in_active_project_with_class_names(self, obj: Union[PFGeneral, Folder, str]) ‑> str`
    :   Get path relative to active project including class names.
        
        Args:
            obj (Union[PFGeneral, Folder, str]): PF object or its path
        
        Returns:
            str: path

    `get_path_of_object_in_current_user(self, obj: Union[PFGeneral, Folder, str]) ‑> str`
    :   Get path relative to current (active) user without class names.
        
        Args:
            obj (Union[PFGeneral, Folder, str]): PF object or its path
        
        Returns:
            str: path

    `get_path_of_object_in_current_user_with_class_names(self, obj: Union[PFGeneral, Folder, str]) ‑> str`
    :   Get path relative to current (active) user including class names.
        
        Args:
            obj (Union[PFGeneral, Folder, str]): PF object or its path
        
        Returns:
            str: path

    `get_project_settings(self) ‑> powfacpy.pf_classes.protocols.SetPrj`
    :   Get project settings object.

    `get_single_obj(self, path: str, parent_folder: Union[PFGeneral, Folder, str] = None, error_if_non_existent: bool = True, include_subfolders: bool = False) ‑> powfacpy.pf_classes.protocols.PFGeneral | None`
    :   DEPRECATED: Use 'get_unique_obj' instead.
        
        Get unique PowerFactory object under 'path'.
        
        Use this method if you want to access one single unique object.
        This method is an alternative to 'get_obj' and returns the unique object instead of a list (that needs to be accessed with '[0]'). It also checks whether the found object is unique (only one object is found).
        
        Args:
            path (str): path to object(s);
            can contain wildcards ("*") after the last ""
        
            condition (Callable, optional):
            filter for attributes etc.; example: "condition = lambda x : getattr(x,"uknom")==110;
            defaults to None
        
            parent_folder (Union[PFGeneral, Folder, str], optional):
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

    `get_unique_obj(self, path: str, parent_folder: Union[PFGeneral, Folder, str] = None, error_if_non_existent: bool = True, include_subfolders: bool = False) ‑> powfacpy.pf_classes.protocols.PFGeneral | None`
    :   Get unique PowerFactory object under 'path'.
        
        Use this method if you want to access one single unique object.
        This method is an alternative to 'get_obj' and returns the unique object instead of a list (that needs to be accessed with '[0]'). It also checks whether the found object is unique (only one object is found).
        
        Args:
            path (str): path to object(s);
            can contain wildcards ("*") after the last ""
        
            condition (Callable, optional):
            filter for attributes etc.; example: "condition = lambda x : getattr(x,"uknom")==110;
            defaults to None
        
            parent_folder (Union[PFGeneral, Folder, str], optional):
            specify a parent folder/container (or its path) from where the search is started ('path' is then relative to 'parent_folder');
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

    `get_upstream_obj(self, start_obj_or_path: Union[PFGeneral, str], condition: Callable, error_if_non_existent: bool = True) ‑> powfacpy.pf_classes.protocols.PFGeneral`
    :   Get upstream object that meets the condition.
        
        Searches upstream in the PF database hierarchy.
        
        Args:
            start_obj_or_path (Union[PFGeneral, str], optional): Object/folder (or its path) to start from
        
            condition (Callable): Condition for the searched object
        
            error_if_non_existent (bool, optional): If True, an exception is raised if no upstream object is found. Defaults to True.
        
        Returns:
            PFGeneral: The PF object found

    `get_workspace_directory(self) ‑> str`
    :

    `is_container(self, obj: Union[PFGeneral, Folder, str]) ‑> bool`
    :   Checks whether a PF object is a container. It is assumed
        that an object is a container if it has the attribute 'contents'.

    `is_pf_class(self, class_name: str) ‑> bool`
    :   Checks if class_name is a valid PF class (using the class ID).

    `move_obj(self, obj_or_path: Union[PFGeneral, str, list[PFGeneral]], target_folder: Union[PFGeneral, Folder, str], overwrite: bool = True, condition: Callable = None, parent_folder: Union[PFGeneral, Folder, str] = None, error_if_non_existent: bool = True, include_subfolders: bool = False) ‑> int`
    :   Move object(s) to 'target_folder'.
        
        Uses 'get_obj' to get the objects under 'obj_or_path'. Target must be in the active project.
        
        See also 'move_single_obj'.
        
        Args:
            obj_or_path (Union[PFGeneral, str]):
                Objects to be moved (get_obj is used for strings)
        
            target_folder (Union[PFGeneral, Folder, str]):
                Folder to which objects are moved
        
            overwrite (bool, optional):
                Overwrite existing objects. Defaults to True.
        
            condition (Callable, optional):
                Condition used in 'get_obj' for the source objects . Defaults to None.
        
            parent_folder (Union[PFGeneral, Folder, str], optional):
                refers to the source folder and is used in combination with 'obj_or_path' to get the object(s) to be moved. Defaults to  None (i.e. '_folder'/active project is used).
        
            error_if_non_existent (bool, optional):
                Raise error if no (source) objects are found. Defaults to True.
        
            include_subfolders (bool, optional):
                Include subfolder in search for source objects. Defaults to False.
        
        Returns:
            bool: 0 on success, 1 on error

    `move_single_obj(self, obj_or_path: Union[PFGeneral, str], target_folder: Union[PFGeneral, Folder, str], overwrite: bool = True, parent_folder: Union[PFGeneral, Folder, str] = None, error_if_non_existent: bool = True, include_subfolders: bool = False) ‑> int`
    :   Move single PF object to 'target_folder'.
        
        Uses 'get_obj' to get the objects under 'obj_or_path'. Target must be in the active project.
        
        See also 'move_obj'.
        
        Args:
            obj_or_path (Union[PFGeneral, str]):
                Object to be moved (get_unique_obj is used for strings)
        
            target_folder (Union[PFGeneral, Folder, str]):
                Folder to which objects are moved
        
            overwrite (bool, optional):
                Overwrite existing objects. Defaults to True.
        
            parent_folder (Union[PFGeneral, Folder, str], optional):
                refers to the source folder and is used in combination with 'obj_or_path' to get the object(s) to be moved. Defaults to  None (i.e. '_folder'/active project is used).
        
            error_if_non_existent (bool, optional):
                Raise error if no (source) objects are found. Defaults to True.
        
            include_subfolders (bool, optional):
                Include subfolder in search for source objects. Defaults to False.
        
        Returns:
            bool: 0 on success, 1 on error

    `path_exists(self, path: str, parent: Union[PFGeneral, Folder, str] = None, return_info: bool = False) ‑> bool`
    :   Check if the path exists.
        
        Args:
            path (str): path
        
            parent (Union[PFGeneral, Folder, str], optional): Parent folder where search is started. Defaults to None (i.e. 'self._obj').
        
            return_info (bool, optional): information about where the path is
            corrupted is returned. Defaults to False.
        
        Raises:
            powfacpy.PFPathInputError: If path is invalid.
        
        Returns:
            bool: True if path exists

    `set_attr(self, obj: Union[PFGeneral, str], params: dict, parent_folder: Union[PFGeneral, Folder, str] = None) ‑> None`
    :   Set the attribute(s) of an object.
        
        Args:
            obj (Union[PFGeneral, str]): PF object
            params (dict): attributes and their values (e.g. {'parameter1':value1, 'parameter2':value2,..})
            parent_folder (Union[PFGeneral, Folder, str], optional): Parent folder object. Defaults to None.
        
        Raises:
            PFAttributeTypeError: If the type of an attribute value is wrong
            PFAttributeError: If an object does not have the specified attribute

    `set_attr_by_path(self, path_with_attr: str, value: Union[int | float | str | PFGeneral | list])`
    :   Set attribute using the path including the attribute name.
        
        Args:
            path_with_attr (str): path to ojbect with attribute name at the end
            value (Union[int | float | str | PFGeneral | list]): attribute value
        
        Example:
          set_attr_by_path(
                "Library\Dynamic Models\Linear_interpolation\desc",
                ["description"])
          Here 'desc' is the name of the attribute.