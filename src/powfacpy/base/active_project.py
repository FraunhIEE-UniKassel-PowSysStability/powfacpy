from __future__ import annotations
from warnings import warn
from typing import Union, Callable
from os import path as os_path
from warnings import warn
from functools import cached_property

from icecream import ic

import powfacpy
from powfacpy.base.folder import Folder
import powfacpy.exceptions
from powfacpy.pf_class_protocols import (
    PFApp,
    PFGeneral,
    ElmRes,
    ElmNet,
    IntComtrade,
    IntUser,
    IntCase,
    IntEvt,
    ComLdf,
    IntMon,
    IntVersion,
    ComPfdimport,
    IntPrj,
    IntScheme,
    SetTime,
    SetColscheme,
)


class ActiveProject(Folder):
    """Interface to the currently active project."""

    app: PFApp

    def __init__(self, pf_app: PFApp | None | bool = False):
        if pf_app:
            self.__class__.app = pf_app
        elif pf_app is None:
            raise TypeError(
                "The input app is of type 'NoneType'. Maybe the PowerFactory app was not loaded correctly."
            )

    def __new__(cls, *args, **kwargs) -> IntPrj | ActiveProject:
        """Required to provide type hints ('IntPrj | ActiveProject')"""
        instance = super().__new__(cls)
        return instance

    @property
    def _obj(self) -> IntPrj:
        return self.get_active_project()

    @property
    def network_model_folder(self):
        return self.__class__.app.GetProjectFolder("netmod")

    @property
    def network_data_folder(self):
        return self.__class__.app.GetProjectFolder("netdat")

    @property
    def operation_scenarios_folder(self):
        return self.__class__.app.GetProjectFolder("scen")

    @property
    def variations_folder(self):
        return self.__class__.app.GetProjectFolder("scheme")

    @property
    def study_cases_folder(self):
        return self.__class__.app.GetProjectFolder("study")

    @property
    def equipment_type_lib_folder(self):
        return self.__class__.app.GetProjectFolder("equip")

    @property
    def library_folder(self):
        return self.__class__.app.GetProjectFolder("lib")

    @property
    def scripts_folder(self):
        return self.__class__.app.GetProjectFolder("scripts")

    @property
    def templates_folder(self):
        return self.__class__.app.GetProjectFolder("templ")

    @property
    def zones_folder(self):
        return self.__class__.app.GetDataFolder("ElmZone")

    @property
    def areas_folder(self):
        return self.__class__.app.GetDataFolder("ElmArea")

    @property
    def boundaries_folder(self):
        return self.__class__.app.GetDataFolder("IntBoundary")

    @property
    def circuits_folder(self):
        return self.__class__.app.GetDataFolder("IntCircuit")

    @property
    def feeders_folder(self):
        return self.__class__.app.GetDataFolder("IntFeeder")

    @property
    def versions_folder(self):
        return self.get_unique_obj("*.IntVersionman")

    def get_active_study_case(
        self, error_if_no_active_case: bool = True
    ) -> IntCase | None:
        """Get the currently active study case. Control whether error should be raised if no case is active.

        Args:
            error_if_no_active_case (bool, optional): If True, raise exception if no case is active. If False, return none. Defaults to True.

        Raises:
            powfacpy.PFNoActiveStudyCaseError: When no case is active.

        Returns:
            IntCase: The active study case | None
        """
        case = self.__class__.app.GetActiveStudyCase()
        if case or not error_if_no_active_case:
            return case
        else:
            raise powfacpy.exceptions.PFNoActiveStudyCaseError()

    def get_from_study_case(
        self, name: str, if_not_unique: str = "warning", if_no_study_case: str = "error"
    ) -> PFGeneral:
        """Get objects from active study case (similar to PF built-in function 'app.GetFromStudyCase()').

        Additionally, this method prints a warning or raises an exception if there is more than one object found in the study case and if no study case is activated.

        Args:
            name (str): class name of the object (e.g. 'ElmRes'), optionally preceded by an object name without wildcards and a dot (e.g. 'All Calcualations.ElmRes')

            if_not_unique (str, optional): Warn ('warning') or raise exception ('error') if there are more than one objects of class 'class_name'. Defaults to "warning".

            if_no_study_case (str, optional): Warn ('warning') or raise exception ('error') if no study case is active. Defaults to "error".

        Raises:
            powfacpy.PFNoActiveStudyCaseError: No study case activated
            TypeError: More than one object was found

        Returns:
            PFGeneral: Found or created object
        """
        object = self.__class__.app.GetFromStudyCase(name)

        if if_no_study_case and not self.__class__.app.GetActiveStudyCase():
            if if_no_study_case == "warning":
                warn(
                    "No study case activated. PowerFactory creates object of class_name in tmp folder, outside any study case."
                )
            elif if_no_study_case == "error":
                raise powfacpy.exceptions.PFNoActiveStudyCaseError()

        if if_not_unique and self.is_pf_class(name):
            name = "*." + name
            all_objects_of_this_class = self.get_obj(
                name, parent_folder=object.GetParent(), include_subfolders=False
            )
            if len(all_objects_of_this_class) > 1:
                parent_path = self.get_path_of_object(object.GetParent())
                if if_not_unique == "warning":
                    warn(
                        f"The returned {name} object is not unique in the  study case: '{parent_path}'. Make sure that the correct {name} object is used."
                    )
                if if_not_unique == "error":
                    raise TypeError(
                        f"The returned {name} object is not unique in its folder / in its study case: '{parent_path}'"
                    )
        return object

    def get_results_obj_from_initial_conditions_calc(self) -> ElmRes:
        """Get results object (ElmRes) from the initial conditions calculation object (ComInc).

        This is the results object where results from time domain (RMS/EMT) simulation are written to.

        Returns:
            ElmRes: ElmRes object
        """
        return self.get_from_study_case("ComInc", if_not_unique="error").p_resvar

    def get_events_folder_from_initial_conditions_calc(self) -> IntEvt:
        """Get events folder (IntEvt) from the initial conditions calculation object (ComInc).

        This folder is used for the events in dynamic time domain simulation (RMS/EMT).

        Returns:
            IntEvt: Events folder.
        """
        return self.get_from_study_case("ComInc", if_not_unique="error").p_event

    def get_calc_relevant_obj(
        self,
        obj_str: str,
        condition: Callable = lambda x: True,
        error_if_non_existent=True,
        includeOutOfService: int = 1,
        topoElementsOnly: int = 0,
        bAcSchemes: int = 0,
    ) -> list[PFGeneral]:
        """Wraps the method 'GetCalcRelevantObjects' (see PF scripting reference) and adds optional arguments similar to 'get_obj'.

        Args:
            obj_str (str): name including class of object(s) (NOT their path)

            condition (Callable, optional): See get_obj. Defaults to lambda x:True.

            error_if_non_existent (bool, optional): See get_obj. Defaults to True.

            From scripting reference:

            includeOutOfService (int, optional): Flag whether to include out of service objects. Defaults to 1.

            topoElementsOnly (int, optional): Flag to filter for topology relevant objects only. Defaults to 0.

            bAcSchemes (int, optional): Flag to include hidden objects in active schemes. Defaults to 0.

        Returns:
            list[PFGeneral]: Found object(s)
        """
        objs = self.__class__.app.GetCalcRelevantObjects(
            obj_str, includeOutOfService, topoElementsOnly, bAcSchemes
        )
        if not objs:
            return self._handle_non_existing_obj(
                obj_str, self.get_active_project(), error_if_non_existent
            )
        if condition:
            obj_with_condition = self.get_by_condition(objs, condition)
            if obj_with_condition:
                return obj_with_condition
            else:
                return self._handle_condition_of_obj_not_met(
                    obj_str, self.get_active_project(), error_if_non_existent
                )
        else:
            return objs

    def add_results_variable(
        self,
        obj: PFGeneral | str | list[PFGeneral | str],
        variables: str | list[str],
        results_obj: ElmRes | None = None,
    ) -> ElmRes:
        """Add variable(s) of 'obj' to the monitored variables in of result object.

        Args:

            obj (PFGeneral | str | list[PFGeneral | str]): PF object or its path

            variables (list[str]): variable names

            results_obj (ElmRes, optional): Results object. Defaults to None (ElmRes from active study case is used).

        Returns:
            ElmRes: the results object
        """
        if results_obj is None:
            results_obj = self.get_from_study_case("ElmRes")
        else:
            results_obj = self._handle_single_pf_object_or_path_input(results_obj)
        obj = self._handle_pf_object_or_path_input(obj)
        if isinstance(variables, str):
            variables = [variables]
        for o in obj:
            for var in variables:
                results_obj.AddVariable(o, var)
        results_obj.Load()
        return results_obj

    def add_variable_selection_obj_to_results_obj(
        self,
        name,
        results_obj: ElmRes,
        class_name: str = None,
        variables: list[str] = [],
    ) -> IntMon:
        """Add a variable selection object (IntMon) to a result object (ElmRes).

        Args:
            name (str): Name of IntMon
            results_obj (ElmRes): Results object
            class_name (str, optional): 'classnm' parameter of IntMon. Defaults to None.
            variables (list[str], optional): 'vars' parameter of IntMon. Defaults to [].

        Returns:
            IntMon: varible selection object
        """
        variable_selection_obj: IntMon = self.create_in_folder(
            name + ".IntMon", results_obj
        )
        if class_name:
            variable_selection_obj.classnm = class_name
        if variables:
            variable_selection_obj.vars = variables
        return variable_selection_obj

    def get_first_level_folder(self, folder_type: str) -> PFGeneral:
        """Get folder on first level of PF database.

        Args:
            folder_type (str): The folder of the active user ('user') or the global library ('global library') can be accessed.

        Raises:
            TypeError: Invalid folder_type input

        Returns:
            PFGeneral: first level folder
        """
        if folder_type == "user":
            return self.__class__.app.GetCurrentUser()
        elif folder_type == "global library":
            return self.__class__.app.GetGlobalLibrary()
        else:
            raise TypeError(
                f"The first level folder {folder_type} is not valid. Use one of these: 'user', 'global library'."
            )

    def get_active_user_folder(self) -> IntUser:
        """Get folder of active user."""
        return self.__class__.app.GetCurrentUser()

    def get_active_networks(self, error_if_no_network_is_active: bool = True) -> ElmNet:
        """Get active networks/grids."""
        grids = self.__class__.app.GetCalcRelevantObjects(
            ".ElmNet"
        )  # This also returns the summary grid in the study case
        # Delete the summary grid which is in the study case
        grids[:] = [
            grid for grid in grids if not grid.GetParent().GetClassName() == "IntCase"
        ]
        if error_if_no_network_is_active and not grids:
            raise powfacpy.exceptions.PFNotActiveError("a network (ElmNet).")
        return grids

    def get_diagram_color_scheme(self) -> SetColscheme:
        return self.GetContents("*.SetFold\\*.IntColouring\\*.SetColscheme")[0]

    def activate_study_case(self, path: str) -> IntCase:
        """Activate study case under path."""
        study_case = self.get_unique_obj(path, include_subfolders=False)
        study_case.Activate()
        return study_case

    def clear_elmres_from_objects_with_status_deleted(
        self, results_obj: ElmRes | None = None
    ):
        """Deletes all objects from a results object (ElmRes) that have the
        status deleted (i.e. attribute 'obj_id' is deleted).
        """
        if not results_obj:
            results_obj = self.get_from_study_case("ElmRes")
        obj_in_elmres = results_obj.GetContents("*")
        for o in obj_in_elmres:
            obj_id = o.obj_id
            if obj_id.IsDeleted():
                o.Delete()

    def clear_elmres(self, results_obj: ElmRes = None):
        """Clear all results variables from results object (ElmRes).

        Args:
            results_obj (ElmRes, optional): Results object. Defaults to None (get elmres from study case).
        """
        if not results_obj:
            results_obj = self.get_from_study_case("ElmRes")
        self.clear_folder(results_obj)

    def get_parameter_value_string(self, parameters: dict, delimiter=" ") -> str:
        """Get string with parameters and their values.

        Args:
            parameters (dict): parameters (keys) and values (values)
            Example: {'P': 2.5, 'Q': 0}

            delimiter (str, optional): Delimiter between parameter value pairs. Defaults to " ".

        Returns:
            str: parameter value string (e.g. 'P = 2.5 Q = 0')
        """
        param_value_string = ""
        for parname, path_with_par in parameters.items():
            value = self.get_attr_by_path(path_with_par)
            param_value_string += parname + "=" + str(value) + delimiter
        return param_value_string[: -len(delimiter)]  # omit last delimiter

    def create_comtrade_obj(
        self, file_path: str, parent_folder: Union[PFGeneral, str] = None
    ) -> IntComtrade:
        """Add an IntComtrade that refers to file_path (*.cfg).
        The objects are stored in a folder "Comtrade" in the currently active
        study case, unless a parent_folder is given. A new object is only
        created if there exists no object yet that points to the same file
        ('f_name' attribute is the file path). The file name is used for the
        new object name (without the .cfg ending).
        """
        if parent_folder:
            parent_folder = self._handle_single_pf_object_or_path_input(parent_folder)
        else:
            parent_folder = self.__class__.app.GetFromStudyCase("Comtrade.IntFolder")

        intcomtrade: IntComtrade | None = self.get_obj(
            "*.IntComtrade",
            parent_folder=parent_folder,
            condition=lambda x: getattr(x, "f_name") == file_path,
            error_if_non_existent=False,
        )
        if not intcomtrade:
            _, file_name = os_path.split(file_path)
            intcomtrade = self.create_in_folder(
                file_name.replace(".cfg", "") + ".IntComtrade",
                parent_folder,
                overwrite=False,
                use_existing=False,
            )
            intcomtrade.f_name = file_path
        else:
            intcomtrade = intcomtrade[0]
        # intcomtrade.Load() probably not required
        return intcomtrade

    def create_variation(
        self,
        name: str,
        parent_folder: str | PFGeneral = None,
        name_expansion_stage: str = "Expansion Stage",
        activationTime: int = 0,
        activate: int = 1,
        overwrite: bool = True,
    ) -> IntScheme:
        """Create variation (including one expansion stage).

        Args:
            name (str): Name of variation
            parent_folder (str | PFGeneral, optional): Parent folder where variation is created. Defaults to None (i.e. variations folder).
            name_expansion_stage (str, optional): Name of. Defaults to "Expansion Stage".
            activationTime (int, optional): UTC time
            activate (int, optional): If 1, expansion stage is activated. If 0, expansion stage is not activated. Defaults to 1.

        Returns:
            IntScheme: The created variation object
        """
        if not parent_folder:
            parent_folder = self.variations_folder
        variation = self.create_in_folder(
            name + ".IntScheme", parent_folder, overwrite=overwrite
        )
        variation.NewStage(name_expansion_stage, activationTime, activate)
        return variation

    def execute_load_flow(self, params: dict = {}) -> int:
        comldf: ComLdf = self.get_from_study_case("ComLdf")
        self.set_attr(comldf, params=params)
        return comldf.Execute()

    def mark_in_graphics(
        self, elms: list[PFGeneral] | PFGeneral, searchOpenedDiagramsOnly: int = 0
    ) -> None:
        if not isinstance(elms, list):
            elms = list(elms)
        self.__class__.app.MarkInGraphics(elms, searchOpenedDiagramsOnly)

    def _handle_possible_attribute_not_set_error(
        self, possibly_not_secified_attr: str, attribute_description: str, error_message
    ):
        """Handles the exception if in a method call (of this class) an AttributeError is raised because of an attribute of this class is not set (i.e. is None).

        Example:
            A method uses self.active_case and active_case is None.
        """
        if not possibly_not_secified_attr:
            raise powfacpy.exceptions.PFAttributeNotSetError(attribute_description)
        else:
            raise AttributeError(error_message)

    def get_project_version(self, version_name: str) -> IntVersion | None:
        """Get (previous) version of project.

        Args:
            version_name (str): Name (loc_name) of version

        Returns:
            IntVersion | None: Version object
        """
        version = self.get_by_condition(
            self._obj.GetVersions(), lambda x: x.loc_name == version_name
        )
        if version:
            return version[0]

    def create_project_version(self, version_name: str, overwrite: bool = True) -> None:
        """Create a version of current state of the project.

        Uses 'CreateVersion'. New version will be added to top level versions folder of project.

        Args:
            version_name (str): Name (loc_name) of version

            overwrite (bool, optional): Overwrite existing version with same name. Defaults to True.
        """
        version = self.get_project_version(version_name)
        if version and overwrite:
            version.Delete()
        self.__class__.app.WriteChangesToDb()
        self._obj.CreateVersion(version_name)

    def rollback_project_to_previous_version(self, version_name: str) -> None:
        """Rollback to previous project version (IntVersion in versions folder).

        Args:
            version_name (str): Name (loc_name) of version.
        """
        active_project = self._obj
        version = self.get_project_version(version_name)
        try:
            active_project.Deactivate()
            version.Rollback()
        finally:
            active_project.Activate()

    def import_project(
        self,
        file_path: str,
        target_folder_in_active_user: str | PFGeneral | None = None,
        keep_current_project_activated: bool = True,
    ) -> IntPrj:
        """Import a project (.pfd file)

        Args:
            file_path (str): Windows path
            target_folder_in_active_user (str | PFGeneral | None, optional): Target folder for project import in active user. Defaults to None.
            keep_current_project_activated (bool, optional): If True, the initial project and study case remain active.If False, the imported project will be active after import. Defaults to True.

        Returns:
            IntPrj: Imported project
        """
        try:
            if keep_current_project_activated:
                initial_project = self._obj
                initial_study_case = self.get_active_study_case()
            pfd_import: ComPfdimport = self.get_from_study_case("ComPfdimport")
            if not file_path[-4:] == ".pfd":
                file_path += ".pfd"
            pfd_import.g_file = file_path
            if target_folder_in_active_user:
                if isinstance(target_folder_in_active_user, str):
                    pfd_import.g_target = self.get_unique_obj(
                        target_folder_in_active_user,
                        parent_folder=self.get_active_user_folder(),
                    )
                else:
                    pfd_import.g_target = target_folder_in_active_user
            else:
                pfd_import.g_target = self.get_active_user_folder()
            pfd_import.Execute()
            imported_project: IntPrj = self.__class__.app.GetActiveProject()
        finally:
            if keep_current_project_activated:
                imported_project.Deactivate()
                initial_project.Activate()
                initial_study_case.Activate()
        return imported_project

    def import_dz_file(
        self, file_path: str, target_folder: PFGeneral | None = None
    ) -> list:
        """Import a .dz file (e.g. a template).

        Args:
            file_path (str): path of .dz file
            target_folder (PFGeneral | None, optional): target folder. Defaults to None (active project).

        Returns:
            list: [int errorCode, list importedObjects]
        """
        if target_folder is None:
            target_folder = self.get_active_project()
        return self.app.ImportDz(target_folder, file_path)

    def set_time_using_year(self, year):
        settime: SetTime = self.get_from_study_case("SetTime")
        average_seconds_per_year = 31556952
        approximate_time_in_seconds_since_1970 = (
            year - 1970
        ) * average_seconds_per_year
        settime.SetTimeUTC(approximate_time_in_seconds_since_1970)


class ActiveProjectCached(ActiveProject):
    """Caches the properties. Should be used only with one active project (the caching fails after a different project has been activated)."""

    @cached_property
    def _obj(self):
        return self.get_active_project()

    @cached_property
    def network_model_folder(self):
        return self.__class__.app.GetProjectFolder("netmod")

    @cached_property
    def network_data_folder(self):
        return self.__class__.app.GetProjectFolder("netdat")

    @cached_property
    def operation_scenarios_folder(self):
        return self.__class__.app.GetProjectFolder("scen")

    @cached_property
    def variations_folder(self):
        return self.__class__.app.GetProjectFolder("scheme")

    @cached_property
    def study_cases_folder(self):
        return self.__class__.app.GetProjectFolder("study")

    @cached_property
    def equipment_type_lib_folder(self):
        return self.__class__.app.GetProjectFolder("equip")

    @cached_property
    def library_folder(self):
        return self.__class__.app.GetProjectFolder("lib")

    @cached_property
    def scripts_folder(self):
        return self.__class__.app.GetProjectFolder("scripts")

    @cached_property
    def templates_folder(self):
        return self.__class__.app.GetProjectFolder("templ")

    @cached_property
    def zones_folder(self):
        return self.__class__.app.GetDataFolder("ElmZone")

    @cached_property
    def areas_folder(self):
        return self.__class__.app.GetDataFolder("ElmArea")

    @cached_property
    def boundaries_folder(self):
        return self.__class__.app.GetDataFolder("IntBoundary")

    @cached_property
    def circuits_folder(self):
        return self.__class__.app.GetDataFolder("IntCircuit")

    @cached_property
    def feeders_folder(self):
        return self.__class__.app.GetDataFolder("IntFeeder")

    @cached_property
    def versions_folder(self):
        return self.get_unique_obj("*.IntVersionman")
