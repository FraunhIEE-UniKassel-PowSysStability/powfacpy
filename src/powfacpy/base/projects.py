"""Project-lifecycle operations: versions, `.pfd` / `.dz` import & export, templates.

One of the composed helpers `ActiveProject` delegates to (see
`ActiveProject.projects`). The `ActiveProject` methods (`import_project`,
`export_to_pfd`, `get_project_version`, `create_project_version`,
`rollback_project_to_previous_version`, `import_dz_file`, `reactivate_project`,
`reset_default_units`, `add_template_from_global_library`) stay as thin
forwarders so the public API is unchanged.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from powfacpy.exceptions import PFInterfaceError
from powfacpy.pf_classes.protocols import (
    ComPfdimport,
    IntPrj,
    IntVersion,
    PFGeneral,
)

if TYPE_CHECKING:
    from powfacpy.base.active_project import ActiveProject


class Projects:
    """Versions, `.pfd`/`.dz` import & export, template import for the active project."""

    def __init__(self, active_project: "ActiveProject") -> None:
        self._act_prj = active_project

    # --- versions --------------------------------------------------------- #
    def get_version(self, version_name: str) -> IntVersion | None:
        """Get a stored project version (`IntVersion`) by name, or None."""
        ap = self._act_prj
        version = ap.get_by_condition(
            ap._obj.GetVersions(), lambda x: x.loc_name == version_name
        )
        if version:
            return version[0]

    def create_version(self, version_name: str, overwrite: bool = True) -> None:
        """Snapshot the current project state as a version."""
        ap = self._act_prj
        version = self.get_version(version_name)
        if version and overwrite:
            version.Delete()
        ap.app.WriteChangesToDb()
        ap._obj.CreateVersion(version_name)

    def rollback_to_version(self, version_name: str) -> None:
        """Roll the project back to a stored version."""
        ap = self._act_prj
        project = ap._obj
        version = self.get_version(version_name)
        try:
            project.Deactivate()
            version.Rollback()
        finally:
            project.Activate()

    # --- import / export ------------------------------------------------- #
    def import_pfd(
        self,
        file_path: str,
        target_folder_in_active_user: str | PFGeneral | None = None,
        keep_current_project_activated: bool = True,
    ) -> IntPrj:
        """Import a project from a `.pfd` file (see `ActiveProject.import_project`)."""
        ap = self._act_prj
        try:
            if keep_current_project_activated:
                initial_project = ap._obj
                initial_study_case = ap.get_active_study_case()
            pfd_import: ComPfdimport = ap.get_from_study_case("ComPfdimport")
            if not file_path[-4:] == ".pfd":
                file_path += ".pfd"
            pfd_import.g_file = file_path
            if target_folder_in_active_user:
                if isinstance(target_folder_in_active_user, str):
                    pfd_import.g_target = ap.get_unique_obj(
                        target_folder_in_active_user,
                        parent_folder=ap.get_active_user_folder(),
                    )
                else:
                    pfd_import.g_target = target_folder_in_active_user
            else:
                pfd_import.g_target = ap.get_active_user_folder()
            pfd_import.Execute()
            # 'GetActiveProject()' is not reliable here - PowerFactory does not
            # necessarily activate the imported project as a side effect of the
            # import. Get it from the command's own record of what it imported.
            imported_project: IntPrj = next(
                (
                    obj
                    for obj in pfd_import.GetImportedObjects()
                    if obj.GetClassName() == "IntPrj"
                ),
                ap.app.GetActiveProject(),
            )
        finally:
            if keep_current_project_activated:
                imported_project.Deactivate()
                initial_project.Activate()
                initial_study_case.Activate()
            else:
                imported_project.Activate()
        return imported_project

    def export_pfd(
        self,
        file_path: str,
        objects: PFGeneral | str | list[PFGeneral | str] | None = None,
    ) -> str:
        """Export the project (or given objects) to a `.pfd` file (see `ActiveProject.export_to_pfd`)."""
        ap = self._act_prj
        if not file_path.endswith(".pfd"):
            file_path += ".pfd"
        if objects is None:
            export_objects = [ap._obj]
        else:
            if isinstance(objects, str) or not isinstance(objects, Iterable):
                objects = [objects]
            export_objects = [
                ap._handle_single_pf_object_or_path_input(obj) for obj in objects
            ]
        pfd_export = ap.get_from_study_case("ComPfdexport")
        pfd_export.SetAttribute("g_file", file_path)
        pfd_export.SetAttribute("g_objects", export_objects)
        if pfd_export.Execute() != 0:
            raise PFInterfaceError(
                f"exporting to '{file_path}' failed - check the PowerFactory output window"
            )
        return file_path

    def import_dz(
        self, file_path: str, target_folder: PFGeneral | None = None
    ) -> list:
        """Import a `.dz` file (e.g. a template). Returns `[errorCode, importedObjects]`."""
        ap = self._act_prj
        if target_folder is None:
            target_folder = ap.get_active_project()
        return ap.app.ImportDz(target_folder, file_path)

    def add_template_from_global_library(
        self, template_name: str | list[str], target_folder: PFGeneral | None = None
    ) -> PFGeneral:
        """Copy a template from the global library into the active project."""
        ap = self._act_prj
        if target_folder is None:
            target_folder = ap.templates_folder
        templates = ap.get_from_global_library(template_name)
        return ap.copy_obj(templates, target_folder)

    # --- (re)activation -------------------------------------------------- #
    def reactivate(self) -> None:
        """Deactivate and reactivate the active project."""
        project = self._act_prj._obj
        project.Deactivate()
        project.Activate()

    def reset_default_units(self) -> None:
        """Clear `Settings\\Units` and reactivate so the default units take effect."""
        self._act_prj.clear_folder(r"Settings\Units")
        self.reactivate()
