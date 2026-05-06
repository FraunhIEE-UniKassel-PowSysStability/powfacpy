Module powfacpy.applications.database
=====================================
The database interface is helpful to interact with larger numbers
of PF objects in the database (getting, setting, storing or comparing
attributes).
One use case is for example to define a set of standard parameters for a
larger model. Using the interface, one can easily get, store (e.g. in a json file) and later reset a set of parameters.

ToDo: Add tutorial for this interface (when there is more functionality).

Classes
-------

`Database(pf_app: PFApp | None | bool = False, cached: bool = False)`
:   Base class for applications. Allows to create versions with
    - ActiveProjectCached (recommended when only one project stays active)
    - or ActiveProject (recommended when the active project may change)

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Methods

    `get_class_names(self, name: str = '*') ‑> list[str]`
    :   Get match cases of 'name' with all PF classes from powfacpy.pf_classes.protocols.

    `get_object_attributes(self, objs: Iterable[PFGeneral], class_attributes: dict = None, keys_are_pf_obj: bool = True, truncated_path: str = '', values_are_pf_obj: bool = True) ‑> dict[str, dict[str, str]]`
    :   Get dictionary with attributes of objects.
        The keys of the dictionary are PF objects or their path.
        The values are dictionaries with keys (attribute names) and values (attribute values).
        
        Args:
            objs(Iterable[PFGeneral]): Iterable with PF objects.
        
            class_attributes(dict, optional): dictionary with keys (class names) and values (iterable with attribute names) to control which attributes are relevant for a class. The class names can contain wildcards ("*"). The attributes can contain '.' to reference objects (e.g. to a referenced type object: 'typ_id.Tan'). Defaults to None.
        
            Example:
            ```python
            {
                "ElmTr2": ["typ_id"],
                "*": ["loc_name", ],
                "ElmVac": ["bus1", "outserv"],
            }
            ```
            -> "loc_name" is relevant for every class
        
            keys_are_pf_obj (str, optional): If True, keys are PF objects, otherwise their paths are used as keys. Defaults to False.
        
            truncated_path(str, optional): If specified, this path is truncated from the keys (object paths). Defaults to "".
            Example:
            ```
            truncated_path = "Network Model\Network Data"
            # then 'Network Model.IntPrjfolder\Network Data.IntPrjfolder\test_database_interface\Grid.ElmNet\AC Voltage Source.ElmVac'
            # becomes (first part truncated):
            'test_database_interface\Grid.ElmNet\AC Voltage Source.ElmVac"
            ```
        
            values_are_pf_obj (bool, optional): If True and if the value of an attribute is a PF object, it will be used as a value in the returned dictionary. Otherwise its path is returned. Defaults to True.
        
        Returns:
            dict[str, dict[str, str]]: PF objects' data
            Example:
            ```
            {
                "Network Model.IntPrjfolder\Network Data.IntPrjfolder\test_database_interface\Grid.ElmNet\AC Voltage Source.ElmVac": {
                        "loc_name": "AC Voltage Source",
                        "bus1": "Network Model.IntPrjfolder\Network Data.IntPrjfolder\test_database_interface\Grid.ElmNet\Terminal HV 1.ElmTerm\Cub_1.StaCubic",
                        "outserv": 0
                },
                "Network Model.IntPrjfolder\Network Data.IntPrjfolder\test_database_interface\Grid.ElmNet\Terminal HV 1.ElmTerm\Cub_1.StaCubic": {
                        "loc_name": "Cub_1"
                },
            }
            ```

    `make_loc_name_unique(self, pf_classes: list = ['Elm*'], objs: Iterable[PFGeneral] | None = None, suffix_separator: str = '_') ‑> dict[str, int]`
    :   Change duplicate loc_name of calculation relevant objects of the same class to ensure that they are unique. Number the loc_name with a suffix '_n' where n is the count. Useful for example when loc_name are used as keys in a dict or labels in DataFrames (e.g. when exporting to pandapower format).
        
        Args:
            pf_classes (Iterable[str] | str, optional): Classes to be considered. Defaults to ["Elm*"].
            objs (Iterable[PFGeneral] | None): Selection ob objects to be considered. Defaults to None (all calculation relevant).
            suffix_separator (str): Suffix used to change duplicate names. Defaults to "_".
        
        Returns:
            dict[str, int]:
                keys: loc_names of objects;
                values: number of occurrences of loc_name in the original dataset.

    `set_pf_obj_attribute_values(self, obj_attr_dict: dict, added_path: None | str = None) ‑> None`
    :   Writes the data of a dict to the PF database
        (the dict can be created e.g. with 'get_object_attributes').
        There are two options for the format of the dict:
        - keys: PF object or path, values: dict[attr, value]
        - keys: tuple(PF object or path, attr ), values: value
        
        Arguments:
          obj_attr_dict (dict): data
          added_path (str): Assumes that the objects' path is relative to a parent folder inside the project. Adds 'added_path' to the paths .

`DatabaseDict(database_dict: dict, pf_app: PFApp | None | bool = False, cached: bool = False)`
:   Dictionary with
        - keys: PF objects or their path
        - values: dictionaries with object attribute names (keys) and attribute values (values)
    
    With convenience methods to set the values in PF (and store original values), etc.

    ### Ancestors (in MRO)

    * builtins.dict
    * powfacpy.applications.application_base.ApplicationBase

    ### Methods

    `get_obj_attribute_strings(self, truncate: None | str = None) ‑> list[str]`
    :   Get list of object attribute strings.
        
        Args:
            truncate (None | str, optional): Truncate prefix from resulting path. Defaults to None.
        
        Returns:
            list[str]: object attribute strings

    `keys_to_obj_attr_str(self, truncate: None | str = None, inplace: bool = False) ‑> powfacpy.applications.database.DatabaseDict`
    :   Transform PF objects in keys to strings containing object paths and attributes.
        
        Args:
            truncate (None | str, optional): Truncate prefix from resulting path. Defaults to None.
            inplace (bool, optional): If True, this dict is modified. Defaults to False (return modified dict).
        
        Returns:
            DatabaseDict: modified dict

    `obj_to_str(self, truncate: None | str = None, inplace: bool = False) ‑> powfacpy.applications.database.DatabaseDict`
    :   Transform PF objects in keys to path strings (PF objects in values of attributes are not affected).
        
        Args:
            truncate (None | str, optional): Truncate prefix from resulting path. Defaults to None.
            inplace (bool, optional): If True, this dict is modified. Defaults to False (return modified dict).
        
        Returns:
            DatabaseDict: modified dict

    `reset(self, new_dict: dict) ‑> None`
    :   Reset dict.
        
        Args:
            new_dict (dict): replacement dict

    `set_pf_obj_values(self, values: Iterable) ‑> None`
    :   Set attribute values of PF objects in PF database using 'values'.
        
        Args:
            values (Iterable): Values (order must be aligned with the order of the keys in the dict)

    `set_values_of_dict(self, values: Iterable) ‑> None`
    :   Set attribute values of PF objects in dict using 'values'.
        
        Args:
            values (Iterable): Values (order must be aligned with the order of the keys in the dict)

    `set_values_of_dict_in_pf(self) ‑> None`
    :   Set values of DatabaseDict in PF objects.

    `set_values_of_dict_in_pf_and_store_original(self) ‑> None`
    :   Set values of DatabaseDict in PF objects and store the original values in this dict.