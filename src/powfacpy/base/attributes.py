"""Get and set attributes of PowerFactory objects for a `Folder`.

One of the composed helpers `Folder` delegates to (see the `Folder.attributes`
property). The `Folder` methods `get_attr`, `get_attr_by_path`, `set_attr` and
`set_attr_by_path` stay as thin forwarders so the public API is unchanged.
"""

from __future__ import annotations

from os import path as os_path
from typing import TYPE_CHECKING, Union

from powfacpy.exceptions import PFAttributeError, PFAttributeTypeError
from powfacpy.pf_classes.protocols import PFGeneral

if TYPE_CHECKING:
    from powfacpy.base.folder import Folder


class Attributes:
    """Get and set attributes of objects relative to a folder (see `Folder.attributes`)."""

    def __init__(self, folder: "Folder") -> None:
        self._folder = folder

    def get(
        self,
        obj: Union[PFGeneral, str],
        attr: str,
        parent_folder: Union[PFGeneral, Folder, str] = None,
    ) -> Union[int | float | str | PFGeneral | list]:
        """Get the value of an attribute of an object.

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
        """
        if isinstance(obj, str):
            obj = self._folder.get_unique_obj(obj, parent_folder=parent_folder)
        try:
            if not isinstance(attr, list):
                return obj.GetAttribute(attr)
            else:
                attr_values = dict()
                for attribute in attr:
                    attr_values[attribute] = obj.GetAttribute(attribute)
                return attr_values
        except AttributeError as e:
            raise PFAttributeError(obj, e, self._folder)

    def get_by_path(
        self, path_with_attr: str
    ) -> Union[int | float | str | PFGeneral | list]:
        """Get attribute using the path including the atrribute name

        Args:
            path_with_attr (str): path including the atrribute name
            Example: 'user\\project\\path\\to\\object\\m:Psum:bus1'

        Returns:
            Union[int|float|str|PFGeneral|list]: Attribute value
        """
        head_tail = os_path.split(path_with_attr)
        return self.get(head_tail[0], head_tail[1])

    def set(
        self,
        obj: Union[PFGeneral, str],
        params: dict,
        parent_folder: Union[PFGeneral, Folder, str] = None,
        resolve_enum_names: bool = False,
    ) -> None:
        """Set the attribute(s) of an object.

        Args:
            obj (Union[PFGeneral, str]): PF object
            params (dict): attributes and their values (e.g. {'parameter1':value1, 'parameter2':value2,..})
            parent_folder (Union[PFGeneral, Folder, str], optional): Parent folder object. Defaults to None.
            resolve_enum_names (bool, optional): translate a string value that names
                an enumeration option (e.g. ``{"i_mot": "Motor"}``) to its integer
                code before writing it. Off by default. See
                `powfacpy.applications.attribute_metadata.AttributeMetadata`.

        Raises:
            PFAttributeTypeError: If the type of an attribute value is wrong
            PFAttributeError: If an object does not have the specified attribute
        """
        obj = self._folder._handle_single_pf_object_or_path_input(
            obj, parent_folder=parent_folder
        )
        if resolve_enum_names:
            from powfacpy.applications.attribute_metadata import AttributeMetadata

            params = AttributeMetadata(self._folder.app).resolve_enum_names(obj, params)
        for attr, value in params.items():
            try:
                obj.SetAttribute(attr, value)
            except TypeError as e:
                raise PFAttributeTypeError(obj, attr, e, self._folder)
            except AttributeError as e:
                raise PFAttributeError(obj, e, self._folder)

    def set_by_path(
        self, path_with_attr: str, value: Union[int | float | str | PFGeneral | list]
    ):
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
        self.set(head_tail[0], {head_tail[1]: value})
