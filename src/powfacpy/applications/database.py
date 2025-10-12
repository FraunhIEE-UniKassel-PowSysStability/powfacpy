"""
The database interface is helpful to interact with larger numbers
of PF objects in the database (getting, setting, storing or comparing
attributes).
One use case is for example to define a set of standard parameters for a
larger model. Using the interface, one can easily get, store (e.g. in a json file) and later reset a set of parameters.

ToDo: Add tutorial for this interface (when there is more functionality).
"""

from __future__ import annotations

import sys
from fnmatch import fnmatchcase
from typing import Callable, Iterable, Any, OrderedDict
import importlib, inspect
import copy

import pandas as pd
import numpy as np
from icecream import ic


from powfacpy.applications.application_base import ApplicationBase
from powfacpy.base.string_manipulation import PFStringManipulation
from powfacpy.pf_classes.protocols import (
    PFGeneral,
    PFApp,
)


class Database(ApplicationBase):

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)

    def get_object_attributes(
        self,
        objs: Iterable[PFGeneral],
        class_attributes: dict = None,
        keys_are_pf_obj: bool = True,
        truncated_path: str = "",
        values_are_pf_obj: bool = True,
    ) -> dict[str, dict[str, str]]:
        """
        Get dictionary with attributes of objects.
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
            truncated_path = "Network Model\\Network Data"
            # then 'Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_database_interface\\Grid.ElmNet\\AC Voltage Source.ElmVac'
            # becomes (first part truncated):
            'test_database_interface\\Grid.ElmNet\\AC Voltage Source.ElmVac"
            ```

            values_are_pf_obj (bool, optional): If True and if the value of an attribute is a PF object, it will be used as a value in the returned dictionary. Otherwise its path is returned. Defaults to True.

        Returns:
            dict[str, dict[str, str]]: PF objects' data
            Example:
            ```
            {
                "Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_database_interface\\Grid.ElmNet\\AC Voltage Source.ElmVac": {
                        "loc_name": "AC Voltage Source",
                        "bus1": "Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_database_interface\\Grid.ElmNet\\Terminal HV 1.ElmTerm\\Cub_1.StaCubic",
                        "outserv": 0
                },
                "Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_database_interface\\Grid.ElmNet\\Terminal HV 1.ElmTerm\\Cub_1.StaCubic": {
                        "loc_name": "Cub_1"
                },
            }
            ```
        """
        if not class_attributes:
            class_attributes = {
                "*": []
            }  # no relevant attributes -> get only keys (object paths)
        if truncated_path:  # include class names in truncated_path
            truncated_path = self.act_prj.get_path_of_obj_with_class_names(
                truncated_path
            )

        obj_attr_dict = {}
        for obj in objs:
            if not keys_are_pf_obj:
                key = self.act_prj.get_path_of_obj_with_class_names(obj)
                if truncated_path:
                    key = PFStringManipulation.truncate_until(
                        key, truncated_path + "\\"
                    )
            else:
                key = obj
            obj_attr_dict[key] = {}
            for class_name in class_attributes.keys():
                if fnmatchcase(
                    obj.GetClassName(), class_name
                ):  # fnmatch allows to use wildcards ("*")
                    for attr in class_attributes[class_name]:
                        val = self._handle_attribute_type_for_reading(
                            obj, attr, not values_are_pf_obj
                        )
                        if not (val is False):
                            obj_attr_dict[key][attr] = val
        return obj_attr_dict

    def set_pf_obj_attribute_values(
        self, obj_attr_dict: dict, added_path: None | str = None
    ) -> None:
        """
        Writes the data of a dict to the PF database
        (the dict can be created e.g. with 'get_object_attributes').
        There are two options for the format of the dict:
        - keys: PF object or path, values: dict[attr, value]
        - keys: tuple(PF object or path, attr ), values: value

        Arguments:
          obj_attr_dict (dict): data
          added_path (str): Assumes that the objects' path is relative to a parent folder inside the project. Adds 'added_path' to the paths .
        """
        if not isinstance(list(obj_attr_dict)[0], tuple):
            for obj, attr_key_val in obj_attr_dict.items():
                obj = self._handle_obj_type(obj, added_path=added_path)
                for attr, value in attr_key_val.items():
                    obj, attr = self._handle_attribute_type_for_writing(obj, attr)
                    value = self._handle_value_type(obj, attr, value)
                    self.act_prj.set_attr(obj, {attr: value})
        else:
            for (obj, attr), value in obj_attr_dict.items():
                obj = self._handle_obj_type(obj, added_path=added_path)
                obj, attr = self._handle_attribute_type_for_writing(obj, attr)
                value = self._handle_value_type(obj, attr, value)
                self.act_prj.set_attr(obj, {attr: value})

    def _handle_obj_type(
        self, obj: PFGeneral | str, added_path: None | str = None
    ) -> PFGeneral:
        """Converts obj specified by their path to the actual PF object. 

        Args:
            obj (PFGeneral | str): _description_
            added_path (None | str, optional): Added path prefix. Defaults to None.

        Returns:
            PFGeneral: object
        """ """"""
        if isinstance(obj, str):
            if added_path is not None:
                obj = added_path + "\\" + obj
            obj = self.act_prj.get_unique_obj(obj, include_subfolders=False)
        return obj

    def _handle_value_type(self, obj: PFGeneral, attr: str, value: Any):
        """Converts path strings in attribute values to PF objects.

        Args:
            obj (PFGeneral): PF object
            attr (str): attribute
            value (Any): value of attribute

        Returns:
            PF object | str:
        """
        if isinstance(value, str) and not isinstance(
            obj.GetAttributeType(attr), str
        ):  # Then the true attribute type is a PF object
            return self.act_prj.get_unique_obj(value)
        else:
            return value

    def _handle_attribute_type_for_reading(
        self,
        obj: PFGeneral,
        attr: str,
        paths_are_used_for_obj: bool = False,
        truncated_path: str = "",
    ) -> PFGeneral | str:
        """
        Various ways to handle attributes which are PF objects (i.e. a PF object holds another PF object as an attribute, e.g. a 'type') when
        reading from the PF database.

        PF objects can be read as
          - a PF object (pf_obj_handling="original_pf_obj")
          - the path of the object (pf_obj_handling="path", default)

        Arguments:
            obj (PFGeneral): PF object
            attr (str): Attribute of the object
            paths_are_used_for_obj (bool, optional): If True, the path of the object is returned instead of the object itself. Defaults to False.
            truncated_path: If 'paths_are_used_for_obj' is True, then 'truncated_path' is truncated from the beginning of the object's path. Defaults to "".

        Returns:
            PFGeneral | str: PF object or its path
        """
        attr = attr.split(".")
        attr_value = obj
        for a in attr:
            if attr_value is None:
                return False
            attr_value = self.act_prj.get_attr(attr_value, a)
        if isinstance(attr_value, (str, int, float)) or not attr_value:
            return attr_value
        else:  # Then it must be a PF object
            if not paths_are_used_for_obj:
                return attr_value
            else:
                if truncated_path:
                    return self.act_prj.get_path_of_obj_with_class_names(truncated_path)
                else:
                    return self.act_prj.get_path_of_obj_with_class_names(attr_value)

    def _handle_attribute_type_for_writing(
        self, obj: PFGeneral, attr: str
    ) -> tuple[PFGeneral, str]:
        """If the attr contains '.' (reference to another obj), return the referenced object and its attribute name. Otherwise just return the input arguments

        Args:
            obj (PFGeneral): PF object
            attr (str): attribute

        Returns:
            tuple[PFGeneral, str]: _description_
        """
        if "." in attr:
            attr = attr.split(".")
            for a in attr[0:-1]:
                obj = self.act_prj.get_attr(obj, a)
            attr = attr[-1]
        return obj, attr

    def make_loc_name_unique(
        self,
        pf_classes: list,
        objs: Iterable[PFGeneral] | None = None,
        suffix_separator: str = "_",
    ) -> dict[str, int]:
        """Change duplicate loc_name of calculation relevant objects of the same class to ensure that they are unique. Number the loc_name with a suffix '_n' where n is the count. Useful for example when loc_name are used as keys in a dict or labels in DataFrames (e.g. when exporting to pandapower format).

        Args:
            pf_classes (Iterable[str] | str, optional): Classes to be considered. Defaults to "Elm*".

        Returns:
            dict[str, int]:
                keys: loc_names of objects;
                values: number of occurrences of loc_name in the original dataset.
        """

        def count_and_rename_objs() -> None:
            for obj in objs:
                name_with_class = obj.loc_name + "." + obj.GetClassName()
                if not name_with_class in obj_count.keys():
                    obj_count[name_with_class] = 1
                else:
                    obj_count[name_with_class] += 1
                    obj.loc_name = (
                        obj.loc_name + f"{suffix_separator}{obj_count[name_with_class]}"
                    )

        obj_count = {}
        if objs is not None:
            count_and_rename_objs()
        else:
            all_pf_classes = []
            for pf_class in pf_classes:
                all_pf_classes += self.get_class_names(pf_class)
            objs = []
            for class_name in all_pf_classes:
                objs += self.act_prj.app.GetCalcRelevantObjects(f"*.{class_name}")
            count_and_rename_objs()
        return obj_count

    def get_class_names(self, name: str = "*") -> list[str]:
        """Get match cases of 'name' with all PF classes from powfacpy.pf_classes.protocols."""
        class_names = []
        for cls_name, _cls in inspect.getmembers(
            importlib.import_module("powfacpy.pf_classes.protocols"), inspect.isclass
        ):
            if fnmatchcase(cls_name, name):
                class_names.append(cls_name)
        return class_names


class DatabaseDict(dict, ApplicationBase):

    def __init__(
        self,
        database_dict,
        pf_app: PFApp | None | bool = False,
        cached: bool = False,
    ) -> None:
        ApplicationBase.__init__(self, pf_app, cached)
        dict.__init__(self, database_dict)

    def reset(self, new_dict: dict) -> None:
        """Reset dict.

        Args:
            new_dict (dict): replacement dict
        """
        self.clear()
        self.update(new_dict)

    def obj_to_str(
        self, truncate: None | str = None, inplace: bool = False
    ) -> DatabaseDict:
        """Transform PF objects in keys to path strings (PF objects in values of attributes are not affected).

        Args:
            truncate (None | str, optional): Truncate prefix from resulting path. Defaults to None.
            inplace (bool, optional): If True, this dict is modified. Defaults to False (return modified dict).

        Returns:
            DatabaseDict: modified dict
        """
        d_new = {}
        for obj, val in self.items():
            if not isinstance(obj, str):
                obj = self.act_prj.get_path_of_object_in_active_project(obj)
            if truncate is not None:
                obj = obj.removeprefix(truncate)
            d_new[obj] = val
        if inplace:
            self.reset(d_new)
        return DatabaseDict(d_new)

    def keys_to_obj_attr_str(
        self, truncate: None | str = None, inplace: bool = False
    ) -> DatabaseDict:
        """Transform PF objects in keys to strings containing object paths and attributes.

        Args:
            truncate (None | str, optional): Truncate prefix from resulting path. Defaults to None.
            inplace (bool, optional): If True, this dict is modified. Defaults to False (return modified dict).

        Returns:
            DatabaseDict: modified dict
        """
        d_strings = self.obj_to_str(truncate=truncate)
        d_new = {}
        for obj, dict_attr_val in d_strings.items():
            for attr, val in dict_attr_val.items():
                d_new[obj + "\\" + attr] = val
        if inplace:
            self.reset(d_new)
        return DatabaseDict(self.app, d_new)

    def get_obj_attribute_strings(self, truncate: None | str = None) -> list[str]:
        """Get list of object attribute strings.

        Args:
            truncate (None | str, optional): Truncate prefix from resulting path. Defaults to None.

        Returns:
            list[str]: object attribute strings
        """
        dbd = self.keys_to_obj_attr_str(truncate=truncate)
        return list(dbd.d.keys())

    def set_pf_obj_values(self, values: Iterable) -> None:
        """Set attribute values of PF objects in PF database using 'values'.

        Args:
            values (Iterable): Values (order must be aligned with the order of the keys in the dict)
        """
        for n, (obj, attr) in enumerate(self.keys()):
            obj.SetAttribute(attr, values[n])

    def set_values_of_dict(self, values: Iterable) -> None:
        """Set attribute values of PF objects in dict using 'values'.

        Args:
            values (Iterable): Values (order must be aligned with the order of the keys in the dict)
        """
        n = 0
        for obj, dict_attr_val in self.items():
            for attr in dict_attr_val.keys():
                self[obj][attr] = values[n]

    def set_values_of_dict_in_pf(self) -> None:
        """Set values of DatabaseDict in PF objects."""
        for obj, dict_attr_val in self.items():
            for attr, val in dict_attr_val.items():
                obj.SetAttribute(attr, val)

    def set_values_of_dict_in_pf_and_store_original(self) -> None:
        """Set values of DatabaseDict in PF objects and store the original values in this dict."""
        for obj, dict_attr_val in self.items():
            for attr, val in dict_attr_val.items():
                old_value = obj.GetAttribute(attr)
                obj.SetAttribute(attr, val)
                dict_attr_val[attr] = old_value

    def set_selected_values(
        self, obj_attr_val: dict, set_in_dict: bool = True, set_in_pf: bool = True
    ) -> None:
        """Set the values of attributes of objects in this dict and/or in PF.

        Args:
            obj_attr_val (dict): dict with keys (objects or class names, then values are set for all objects of the class) and values (dict with attributes and values)
            Example:
            ```python
            {
                ("ElmLod","plini"): {
                    "min": 0,
                    "max": lambda x: x.plini * 0.9,
                },
                ("ElmLod","qlini"): {
                    "min": 0,
                    "max": 0.5,
            }
            ```
            set_in_dict (bool, optional): If True, the values are set in this dict. Defaults to True.
            set_in_pf (bool, optional): If True, the values are set in the PF database. Defaults to True.
        """
        if set_in_dict and set_in_pf:
            set_fun = lambda obj, set_attr, val: (
                obj.SetAttribute(set_attr, val),
                self[obj].update({set_attr: val}),
            )
        elif set_in_dict:
            set_fun = lambda obj, set_attr, val: self[obj].update({set_attr: val})
        elif set_in_pf:
            set_fun = lambda obj, set_attr, val: obj.SetAttribute(set_attr, val)
        else:
            return None

        self._set_val(obj_attr_val, set_fun)

    def _set_val(self, obj_attr_val: dict, set_fun: Callable) -> None:
        """Set values in obj_attr_val.

        Args:
            obj_attr_val (dict): dict with keys (objects or class names, then values are set for all objects of the class) and values (dict with attributes and values)
            set_fun (Callable): function to set the values in the dict and/or PF.
        """
        for (set_obj, set_attr), val in obj_attr_val.items():
            objs = self.get_obj_with_attr(set_obj, set_attr)
            for obj in objs:
                if isinstance(val, Callable):
                    val = val(obj)
                elif isinstance(val, dict):
                    for attr, dict_val in val.items():
                        if isinstance(dict_val, Callable):
                            val[attr] = dict_val(obj)
                        else:
                            val[attr] = dict_val
                set_fun(obj, set_attr, val)

    def get_obj_with_attr(self, obj_or_class, attr) -> bool:
        """Get an object thats has an attribute ('attr') from this dict.

        Args:
            obj_or_class (PFGeneral | str): PF object or class name
            attr (str): _description_

        Returns:
            list[PFGeneral]: List of PF objects found in dict
        """
        if isinstance(obj_or_class, str):
            objs = []
            for obj, dict_attr_val in self.items():
                if obj.GetClassName() == obj_or_class and attr in dict_attr_val.keys():
                    objs.append(obj)
            return objs
        else:
            for obj, dict_attr_val in self.items():
                if obj in self.keys() and attr in dict_attr_val.keys():
                    return [obj]
        return []

    def _keys_are_object_attr_tuples(self) -> bool:
        return isinstance(list(self)[0], tuple)


class DatabaseDictForParameterStudies(DatabaseDict):

    def __init__(self, database_dict: dict, pf_app=False, cached=False) -> None:
        super().__init__(database_dict, pf_app, cached)
        if not isinstance(self.get_first_key(), tuple):
            self._keys_to_obj_attr_tuples()
            self.replace_composite_attributes(inplace=True)

    def get_first_key(self) -> Any:
        return next(iter(self.keys()))

    def set_values_of_dict_in_pf(self) -> None:
        """Set values of DatabaseDict in PF objects."""
        for (obj, attr), val in self.items():
            obj.SetAttribute(attr, val)

    def get_deepcopy(self) -> DatabaseDictForParameterStudies:
        deepc = DatabaseDictForParameterStudies(self.copy())
        deepc.values = copy.deepcopy(list(deepc.values()))
        return deepc

    def set_selected_values(
        self, obj_attr_val: dict, set_in_dict: bool = True, set_in_pf: bool = True
    ) -> None:
        """Set the values of attributes of objects in this dict and/or in PF.

        Args:
            obj_attr_val (dict): dict with keys (objects or class names, then values are set for all objects of the class) and values (dict with attributes and values)
            Example:
            ```python
            {
                ("ElmLod","plini"): {
                    "min": 0,
                    "max": lambda x: x.plini * 0.9,
                },
                ("ElmLod","qlini"): {
                    "min": 0,
                    "max": 0.5,
            }
            ```
            set_in_dict (bool, optional): If True, the values are set in this dict. Defaults to True.
            set_in_pf (bool, optional): If True, the values are set in the PF database. Defaults to True.
        """
        if set_in_dict and set_in_pf:
            set_fun = lambda obj, set_attr, val: (
                obj.SetAttribute(set_attr, val),
                self.update({(obj, set_attr): val}),
            )
        elif set_in_dict:
            set_fun = lambda obj, set_attr, val: self.update({(obj, set_attr): val})
        elif set_in_pf:
            set_fun = lambda obj, set_attr, val: obj.SetAttribute(set_attr, val)
        else:
            return None
        self._set_val(obj_attr_val, set_fun)

    def get_obj_with_attr(
        self, obj_or_class: PFGeneral | str, attr: str
    ) -> list[PFGeneral]:
        """Get an object thats has an attribute ('attr') from this dict.

        Args:
            obj_or_class (PFGeneral | str): PF object or class name
            attr (str): _description_

        Returns:
            list[PFGeneral]: List of PF objects found in dict
        """
        if isinstance(obj_or_class, str):
            objs = []
            for (obj, dict_attr), _ in self.items():
                if obj.GetClassName() == obj_or_class and attr == dict_attr:
                    objs.append(obj)
            return objs
        else:
            for (obj, dict_attr), _ in self.items():
                if obj == obj_or_class and attr in dict_attr:
                    return [obj]
        return []

    def values_to_tuples(self, attributes: Iterable) -> tuple[tuple]:
        l = [()] * len(self.keys())
        for n, val_dict in enumerate(self.values()):
            t = []
            for key, val in val_dict.items():
                if key in attributes:
                    t.append(val)
            l[n] = tuple(t)
        return l

    def _keys_to_obj_attr_tuples(self) -> None:
        d_new = {
            (obj, attr): value
            for obj, attr_and_value in self.items()
            for attr, value in attr_and_value.items()
        }
        self.reset(d_new)

    def replace_composite_attributes(self, inplace: bool = False) -> None:
        """Must be of tuple form"""
        d_new = {}
        pfdi = Database()
        for (obj, attr), val in self.items():
            obj, attr = pfdi._handle_attribute_type_for_writing(obj, attr)
            d_new[obj, attr] = val
        if inplace:
            self.reset(d_new)
        return DatabaseDictForParameterStudies(d_new)

    def to_pandas_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self)

    def obj_to_str(
        self,
        truncate: None | str = None,
    ) -> DatabaseDictForParameterStudies:
        """Only in keys, not in values of attributes"""
        d_new = {}
        for (obj, attr), val in self.items():
            if not isinstance(obj, str):
                obj = self.act_prj.get_path_of_object_in_active_project(obj)
            if truncate is not None:
                obj = obj.removeprefix(truncate)
            d_new[(obj, attr)] = val
        return d_new

    def keys_to_obj_attr_str(
        self,
        truncate: None | str = None,
    ) -> dict:
        d_strings = self.obj_to_str(truncate=truncate)
        d_new = {}
        for (obj, attr), val in d_strings.items():
            d_new[obj + "\\" + attr] = val
        return d_new
