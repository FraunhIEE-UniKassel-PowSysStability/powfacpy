"""Path-string helpers for a `Folder`.

One of the composed helpers `Folder` delegates to (see the `Folder.paths`
property). Every `Folder` path method (`get_path_of_object`,
`get_full_path_of_object`, `get_path_of_object_in_active_project`, ...) stays as
a thin forwarder so the public API is unchanged.

`with_class_names=True` keeps the PowerFactory class suffixes
(`Grid.ElmNet\\Terminal.ElmTerm`); the default strips them.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from powfacpy.base import string_manipulation as strman
from powfacpy.pf_classes.protocols import PFGeneral

if TYPE_CHECKING:
    from powfacpy.base.folder import Folder


class Paths:
    """Build the path of a PowerFactory object relative to different roots."""

    def __init__(self, folder: "Folder") -> None:
        self._folder = folder

    def _full_name(self, obj: PFGeneral | str) -> str:
        return self._folder._handle_single_pf_object_or_path_input(obj).GetFullName()

    @staticmethod
    def _strip_classes(path: str, with_class_names: bool) -> str:
        return path if with_class_names else strman.remove_class_names(path)

    def _relative_to(
        self, obj: PFGeneral | str, base_full_name: str, with_class_names: bool
    ) -> str:
        return self._strip_classes(
            strman.truncate_beginning(self._full_name(obj), base_full_name),
            with_class_names,
        )

    def of(self, obj: PFGeneral | str, with_class_names: bool = False) -> str:
        """Path relative to the folder object (`Folder._obj`)."""
        return self._relative_to(
            obj, self._folder._obj.GetFullName(), with_class_names
        )

    def absolute(self, obj: PFGeneral | str, with_class_names: bool = False) -> str:
        """Full path in the PowerFactory database."""
        return self._strip_classes(self._full_name(obj), with_class_names)

    def in_active_project(
        self, obj: PFGeneral | str, with_class_names: bool = False
    ) -> str:
        """Path relative to the active project (empty base if no project is active)."""
        active_project = self._folder.app.GetActiveProject()
        base = active_project.GetFullName() if active_project else ""
        return self._relative_to(obj, base, with_class_names)

    def in_current_user(
        self, obj: PFGeneral | str, with_class_names: bool = False
    ) -> str:
        """Path relative to the current (active) user."""
        return self._relative_to(
            obj, self._folder.get_current_user().GetFullName(), with_class_names
        )

    def between(
        self, obj_high: PFGeneral | str, obj_low: PFGeneral | str
    ) -> str:
        """Path from `obj_high` (higher in the hierarchy) down to `obj_low`."""
        high = self.of(obj_high)
        return self.of(obj_low).split(high)[1][1:]

    def format_full_path(self, path: str, with_class_names: bool = False) -> str:
        """Turn a full database *path string* into one relative to the active project.

        Like `in_active_project` but takes a raw string (with class suffixes, and
        possibly a trailing `</l3>` from `str(pf_object)`) instead of an object.
        """
        relative = strman.get_path_inside_active_project_from_full_path(
            path, self._folder.app
        )
        return relative if with_class_names else strman.remove_class_names(relative)

    def expand_special_characters(self, path: str) -> str:
        """Replace `$(ExtDataDir)` / `$(WorkspaceDir)` / `$(InstallationDir)` with their directories."""
        folder = self._folder
        if "$(ExtDataDir)" in path:
            path = path.replace(
                "$(ExtDataDir)", folder.get_external_data_directory()
            )
        path = path.replace("$(WorkspaceDir)", folder.get_workspace_directory())
        return path.replace(
            "$(InstallationDir)", folder.get_installation_directory()
        )
