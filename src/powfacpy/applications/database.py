"""
The database interface is helpful to interact with larger numbers
of PF objects in the database (getting, setting, storing or comparing
attributes).
One use case is for example to define a set of standard parameters for a
larger model. Using the interface, one can easily get, store (e.g. in a json file) and later reset a set of parameters.

ToDo: Add tutorial for this interface (when there is more functionality).
"""

import sys
from fnmatch import fnmatchcase
from typing import Iterable
import importlib, inspect

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
        truncated_path: str = "",
        pf_obj_handling: str = "path",
    ) -> dict[str, dict[str, str]]:
        """
        Get dictionary with attributes of objects.
        The keys of the dictionary are the paths of the objects.
        The values are dictionaries with keys (attribute names) and values (attribute values).

        Args:
            objs(Iterable[PFGeneral]): Iterable with PF objects.

            class_attributes(dict, optional): dictionary with keys (class names) and values (iterable with attribute names). To control which attributes are relevant for a class. The class names can contain wildcards ("*"). Defaults to None.
            Example:
            ```python
            {
                "ElmTr2": ["typ_id"],
                "*": ["loc_name", ],
                "ElmVac": ["bus1", "outserv"],
            }
            ```
            -> "loc_name" is relevant for every class

            truncated_path(str, optional): If specified, this path is truncated from the keys (object paths). Defaults to "".
            Example:
            ```
            truncated_path = "Network Model\\Network Data"
            # then 'Network Model.IntPrjfolder\\Network Data.IntPrjfolder\\test_database_interface\\Grid.ElmNet\\AC Voltage Source.ElmVac'
            # becomes (first part truncated):
            'test_database_interface\\Grid.ElmNet\\AC Voltage Source.ElmVac"
            ```

            pf_obj_handling (str, optional): If the value of an attribute is a PF object, there are several options on how to read the attribute (please see _handle_attribute_type_for_reading). Defaults to "path".

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
            obj_path = self.act_prj.get_path_of_obj_with_class_names(obj)
            if truncated_path:
                obj_path = PFStringManipulation.truncate_until(
                    obj_path, truncated_path + "\\"
                )
            obj_attr_dict[obj_path] = {}
            for class_name in class_attributes.keys():
                if fnmatchcase(
                    obj.GetClassName(), class_name
                ):  # fnmatch allows to use wildcards ("*")
                    for attr in class_attributes[class_name]:
                        obj_attr_dict[obj_path][attr] = (
                            self._handle_attribute_type_for_reading(
                                obj, attr, pf_obj_handling
                            )
                        )
        return obj_attr_dict

    def set_object_attributes(self, obj_attr_dict: dict, added_path: str = "") -> None:
        """
        Takes a dict with keys (object paths) and values (dict with attributes
        and their values) and writes the data to the PF database.
        (the dict can be created e.g. with 'get_object_attributes')

        Arguments:
          obj_attr_dict (dict): data

          added_path (str): Assumes that the object paths are relative to a parent folder inside the project. Adds added_path to the paths.
        """
        for obj, attr_key_val in obj_attr_dict.items():
            if added_path:
                obj = added_path + "\\" + obj
            obj = self.act_prj.get_unique_obj(obj, include_subfolders=False)
            for attr, value in attr_key_val.items():
                if isinstance(value, str):
                    if not isinstance(
                        obj.GetAttributeType(attr), str
                    ):  # Then a PF object is expected
                        value_pf_obj = self.act_prj.get_unique_obj(
                            value, error_if_non_existent=False, include_subfolders=False
                        )
                        if value_pf_obj:
                            value = value_pf_obj
                self.act_prj.set_attr(obj, {attr: value})

    def _handle_attribute_type_for_reading(
        self, obj: PFGeneral, attr: str, pf_obj_handling="path", truncated_path=""
    ) -> PFGeneral | str:
        """
        Various ways to handle attributes which are PF objects (i.e. a PF object holds another PF object as an attribute, e.g. a 'type') when
        reading from the PF database.

        PF objects can be read as
          - a PF object (pf_obj_handling="original_pf_obj")
          - the path of the object (pf_obj_handling="path")

        Arguments:
            obj (PFGeneral): PF object
            attr (str): Attribute of the object
            pf_obj_handling (str, optional): see above. Defaults to "path".
            truncated_path: If pf_obj_handling="path", then 'truncated_path' is truncated from the beginning of the object's path. Defaults to "".

        Returns:
            PFGeneral | str: PF object or its path
        """
        attr_value = self.act_prj.get_attr(obj, attr)
        if isinstance(attr_value, (str, int, float)) or not attr_value:
            return attr_value
        else:  # Then it must be a PF object
            if pf_obj_handling == "path":
                if truncated_path:
                    truncated_path = self.act_prj.get_path_of_obj_with_class_names(
                        truncated_path
                    )
                return self.act_prj.get_path_of_obj_with_class_names(attr_value)
            elif pf_obj_handling == "original_pf_obj":
                return attr_value

    def make_loc_name_of_calc_relevant_objects_unique(
        self, pf_classes: Iterable[str] | str = "Elm*"
    ) -> dict[str, int]:
        if not isinstance(pf_classes, Iterable):
            pf_classes = self.get_class_names(pf_classes)
        for class_name in pf_classes:
            objs: list[PFGeneral] = self.act_prj.app.GetCalcRelevantObjects(
                f"*.{class_name}"
            )
            loc_names_count = {}
            for obj in objs:
                if not obj.loc_name in loc_names_count.keys():
                    loc_names_count[obj.loc_name] = 0
                else:
                    loc_names_count[obj.loc_name] += 1
                    obj.loc_name = obj.loc_name + f"_{loc_names_count[obj.loc_name]}"
        return loc_names_count

    def get_class_names(self, name: str = "*") -> list[str]:
        class_names = []
        for cls_name, _cls in inspect.getmembers(
            importlib.import_module("powfacpy.pf_classes.protocols"), inspect.isclass
        ):
            if fnmatchcase(cls_name, name):
                class_names.append(cls_name)
        return class_names

    # Todo: define standard class attributes
    def get_standard_class_attributes():
        return {"ElmTerm": ["Unom"]}
