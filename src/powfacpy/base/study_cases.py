"""Create study cases, variations and scenarios in the active project.

One of the composed helpers `ActiveProject` delegates to (see
`ActiveProject.study_cases`). The `ActiveProject` methods `create_study_case`,
`create_variation`, `create_scenario`, `create_parallel_variation_for_study_case`
and `create_parallel_scenario_for_study_case` stay as thin forwarders so the
public API is unchanged.

Not to be confused with `powfacpy.applications.study_cases.StudyCases`, the
higher-level parametric study-case tool built on top of this.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from powfacpy.base import string_manipulation as strman
from powfacpy.pf_classes.protocols import (
    IntCase,
    IntScenario,
    IntScheme,
    PFGeneral,
)

if TYPE_CHECKING:
    from powfacpy.base.active_project import ActiveProject


class StudyCases:
    """Create study cases and their parallel variations / scenarios."""

    def __init__(self, active_project: "ActiveProject") -> None:
        self._act_prj = active_project

    def create(
        self,
        name: str,
        copy_from: IntCase | str | None = None,
        parent_folder: PFGeneral | str | None = None,
        create_variation: bool = False,
        create_scenario: bool = False,
        overwrite: bool = True,
        use_existing: bool = False,
        activate: bool = True,
    ) -> IntCase | list[IntCase | IntScheme | IntScenario]:
        """Create a study case and optionally a parallel variation and/or scenario.

        Args:
            name: name (used for the case and the variation/scenario).
            copy_from: case to copy from. Defaults to None (create an empty case).
            parent_folder: folder object, or a name/path (created if missing). A
                path with ``\\`` is relative to the project root; a bare name is a
                subfolder of the study cases folder. Defaults to the study cases folder.
            create_variation / create_scenario: also create a parallel one.
            overwrite / use_existing: see `Folder.create_in_folder`.
            activate: activate the case (and variation/scenario).

        Returns:
            the case, or ``[case, variation?, scenario?]`` if any were requested.
        """
        ap = self._act_prj
        if parent_folder is None:
            parent_folder = ap.study_cases_folder
        elif isinstance(parent_folder, str):
            if "\\" in parent_folder:
                # a path with separators is resolved relative to the project root
                parent_folder = ap.create_by_path(
                    parent_folder + ".IntFolder", overwrite=False, use_existing=True
                )
            else:
                # a bare name is a subfolder of the study cases folder
                parent_folder = ap.create_directory(
                    parent_folder, parent_folder=ap.study_cases_folder
                )
        if copy_from is None:
            case = ap.create_in_folder(
                name + ".IntCase",
                parent_folder,
                overwrite=overwrite,
                use_existing=use_existing,
            )
        else:
            case = ap.copy_single_obj(
                copy_from,
                target_folder=parent_folder,
                new_name=name,
                overwrite=overwrite,
                use_existing=use_existing,
            )
        if activate:
            case.Activate()
        if not create_variation and not create_scenario:
            return case
        returned_objs = [case]
        if create_variation:
            returned_objs.append(
                self.create_parallel_variation(
                    case, overwrite=overwrite, activate=activate
                )
            )
        if create_scenario:
            returned_objs.append(
                self.create_parallel_scenario(
                    case, overwrite=overwrite, activate=activate
                )
            )
        return returned_objs

    def _folder_of_case_inside_study_cases_folder(
        self, case: IntCase | None
    ) -> str | None:
        """Path of the subfolder the study case sits in, relative to the study cases folder."""
        ap = self._act_prj
        path_inside = strman.truncate_until(
            ap.get_path_of_object(case), ap.study_cases_folder.loc_name + "\\"
        )
        if "\\" not in path_inside:
            return None
        return "".join(path_inside.split("\\")[:-1])

    def create_parallel_variation(
        self, case: IntCase | str, overwrite: bool = True, activate: bool = True
    ) -> IntScheme:
        """Create a variation for `case`, mirroring its subfolder into the variations folder."""
        ap = self._act_prj
        case = ap._handle_single_pf_object_or_path_input(case)
        subfolder = self._folder_of_case_inside_study_cases_folder(case)
        if subfolder:
            parent_folder = ap.create_directory(subfolder, ap.variations_folder)
        else:
            parent_folder = ap.variations_folder
        return self.create_variation(
            name=case.loc_name,
            parent_folder=parent_folder,
            overwrite=overwrite,
            activate=activate,
        )

    def create_parallel_scenario(
        self, case: IntCase | str, overwrite: bool = True, activate: bool = True
    ) -> IntScenario:
        """Create a scenario for `case`, mirroring its subfolder into the scenarios folder."""
        ap = self._act_prj
        case = ap._handle_single_pf_object_or_path_input(case)
        subfolder = self._folder_of_case_inside_study_cases_folder(case)
        if subfolder:
            parent_folder = ap.create_directory(
                subfolder, ap.operation_scenarios_folder
            )
        else:
            parent_folder = ap.operation_scenarios_folder
        return self.create_scenario(
            name=case.loc_name,
            parent_folder=parent_folder,
            overwrite=overwrite,
            activate=activate,
        )

    def create_variation(
        self,
        name: str,
        parent_folder: str | PFGeneral = None,
        name_expansion_stage: str = "Expansion Stage",
        activationTime: int = 0,
        activate: int = 1,
        overwrite: bool = True,
    ) -> IntScheme:
        """Create a variation (`IntScheme`) including one expansion stage."""
        ap = self._act_prj
        if not parent_folder:
            parent_folder = ap.variations_folder
        variation = ap.create_in_folder(
            name + ".IntScheme", parent_folder, overwrite=overwrite
        )
        variation.NewStage(name_expansion_stage, activationTime, activate)
        return variation

    def create_scenario(
        self,
        name: str,
        parent_folder: str | PFGeneral = None,
        activate: bool = True,
        overwrite: bool = True,
    ) -> IntScenario:
        """Create an operation scenario (`IntScenario`)."""
        ap = self._act_prj
        if not parent_folder:
            parent_folder = ap.operation_scenarios_folder
        scenario: IntScenario = ap.create_in_folder(
            name + ".IntScenario", parent_folder, overwrite=overwrite
        )
        if activate:
            scenario.Activate()
        return scenario
