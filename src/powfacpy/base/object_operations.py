"""Copy, move and delete PowerFactory objects for a `Folder`.

One of the composed helpers `Folder` delegates to (see the `Folder.objects`
property). The `Folder` methods `copy_obj`, `copy_single_obj`, `move_obj`,
`move_single_obj`, `delete_obj` and `clear_folder` stay as thin forwarders so the
public API is unchanged.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Union

from powfacpy.pf_classes.protocols import PFGeneral

if TYPE_CHECKING:
    from powfacpy.base.folder import Folder


class ObjectOperations:
    """Copy, move and delete objects relative to a folder (see `Folder.objects`)."""

    def __init__(self, folder: "Folder") -> None:
        self._folder = folder

    def copy(
        self,
        obj_or_path: Union[PFGeneral, str, list[PFGeneral]],
        target_folder: Union[PFGeneral, Folder],
        overwrite: bool = True,
        condition: Callable = None,
        parent_folder: Union[PFGeneral, Folder, str] = None,
        error_if_non_existent: bool = True,
        include_subfolders: bool = False,
    ) -> list[PFGeneral]:
        """Copy object(s) to 'target_folder'.

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
        """
        obj = self._folder._handle_pf_object_or_path_input(
            obj_or_path,
            condition=condition,
            parent_folder=parent_folder,
            error_if_non_existent=error_if_non_existent,
            include_subfolders=include_subfolders,
        )
        target_folder = self._folder._handle_single_pf_object_or_path_input(target_folder)
        if overwrite:
            for object_to_be_copied in obj:
                self._delete_existing_in_target(object_to_be_copied, target_folder)
        # AddCopy() accepts a list of objects, but then it returns the target folder object and not the copied objects. Therefore, it is iterated through the objects.
        copied_obj = []
        for o in obj:
            copied_obj.append(target_folder.AddCopy(o))
        return copied_obj

    def copy_single(
        self,
        obj_or_path: Union[PFGeneral, str],
        target_folder: Union[PFGeneral, Folder, str],
        overwrite: bool = True,
        use_existing: bool = False,
        new_name: str = None,
        parent_folder: Union[PFGeneral, Folder, str] = None,
        error_if_non_existent: bool = True,
    ) -> PFGeneral:
        """Copy a single PF object to 'target_folder'

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
        """
        obj = self._folder._handle_single_pf_object_or_path_input(
            obj_or_path,
            parent_folder=parent_folder,
            error_if_non_existent=error_if_non_existent,
        )
        target_folder = self._folder._handle_single_pf_object_or_path_input(target_folder)
        if use_existing:
            existing_name = (
                f"{new_name}.{obj.GetClassName()}"
                if new_name
                else self._folder.get_loc_name_with_class(obj)
            )
            existing_obj = self._folder.get_unique_obj(
                existing_name,
                parent_folder=target_folder,
                error_if_non_existent=False,
            )
            # never return the source itself (target folder may be the source's folder)
            if existing_obj and existing_obj != obj:
                return existing_obj
        elif overwrite:
            self._delete_existing_in_target(obj, target_folder, new_name=new_name)
        if new_name:
            return target_folder.AddCopy(obj, new_name)
        else:
            return target_folder.AddCopy(obj)

    def move(
        self,
        obj_or_path: Union[PFGeneral, str, list[PFGeneral]],
        target_folder: Union[PFGeneral, Folder, str],
        overwrite: bool = True,
        condition: Callable = None,
        parent_folder: Union[PFGeneral, Folder, str] = None,
        error_if_non_existent: bool = True,
        include_subfolders: bool = False,
    ) -> int:
        """Move object(s) to 'target_folder'.

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
        """
        obj = self._folder._handle_pf_object_or_path_input(
            obj_or_path,
            condition=condition,
            parent_folder=parent_folder,
            error_if_non_existent=error_if_non_existent,
            include_subfolders=include_subfolders,
        )
        target_folder = self._folder._handle_single_pf_object_or_path_input(target_folder)
        if overwrite:
            for object_to_be_copied in obj:
                self._delete_existing_in_target(object_to_be_copied, target_folder)
        return target_folder.Move(obj)

    def move_single(
        self,
        obj_or_path: Union[PFGeneral, str],
        target_folder: Union[PFGeneral, Folder, str],
        overwrite: bool = True,
        parent_folder: Union[PFGeneral, Folder, str] = None,
        error_if_non_existent: bool = True,
        include_subfolders: bool = False,
    ) -> int:
        """Move single PF object to 'target_folder'.

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
        """

        obj = self._folder._handle_single_pf_object_or_path_input(
            obj_or_path,
            parent_folder=parent_folder,
            error_if_non_existent=error_if_non_existent,
            include_subfolders=include_subfolders,
        )
        target_folder = self._folder._handle_single_pf_object_or_path_input(target_folder)
        if overwrite:
            self._delete_existing_in_target(obj, target_folder)
        return target_folder.Move(obj)

    def delete(
        self,
        obj_or_path: Union[PFGeneral, str],
        condition: Callable = None,
        parent_folder: Union[PFGeneral, str] = None,
        error_if_non_existent: bool = True,
        include_subfolders: bool = False,
    ):
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
        if obj_or_path:
            obj = self._folder._handle_pf_object_or_path_input(
                obj_or_path,
                condition=condition,
                parent_folder=parent_folder,
                error_if_non_existent=error_if_non_existent,
                include_subfolders=include_subfolders,
            )
            for o in obj:
                o.Delete()
                # 'IsDeleted' seems to be the savest way to check whether an object has been deleted.
                if not o.IsDeleted():
                    active_study_case = self._folder.__class__.app.GetActiveStudyCase()
                    if active_study_case:
                        active_study_case.Deactivate()
                        o.Delete()
                        active_study_case.Activate()

                    if not o.IsDeleted():
                        try:
                            o.Deactivate()
                            o.Delete()
                        except AttributeError:  # raised when o cannot be deactivated
                            raise TypeError(f"Object {o} cannot be deleted.")

                        if not o.IsDeleted():
                            raise TypeError(f"Object {o} cannot be deleted.")

    def _delete_existing_in_target(
        self,
        obj_or_name: PFGeneral | str,
        target_folder: PFGeneral | Folder,
        new_name: str | None = None,
    ) -> None:
        """Delete an object of the same name and class already present in `target_folder`.

        Shared 'overwrite' helper for `create_in_folder` / `copy_obj` /
        `copy_single_obj` / `move_obj` / `move_single_obj`. Does nothing (and
        raises no error) if no such object exists.

        Args:
            obj_or_name: a PF object (its `loc_name` + class are used) or a
                `"name.Class"` string.
            target_folder: folder to delete from.
            new_name: if given (and `obj_or_name` is an object), match this name
                instead of the object's own `loc_name`.
        """
        if isinstance(obj_or_name, str):
            name_with_class = obj_or_name
        elif new_name:
            name_with_class = f"{new_name}.{obj_or_name.GetClassName()}"
        else:
            name_with_class = self._folder.get_loc_name_with_class(obj_or_name)
        self.delete(
            name_with_class,
            parent_folder=target_folder,
            include_subfolders=False,
            error_if_non_existent=False,
        )

    def clear(self, folder: Union[PFGeneral, Folder, str] = None):
        """Clear all objects inside folder (including hidden objects).

        Args:
            folder (Union[PFGeneral, Folder, str], optional): Folder/ container objects or its path. Defaults to None (i.e. '_folder'/active project).
        """
        folder = (
            self._folder._obj
            if not folder
            else self._folder._handle_single_pf_object_or_path_input(folder)
        )
        self.delete(
            "*",
            parent_folder=folder,
            include_subfolders=False,
            error_if_non_existent=False,
        )
