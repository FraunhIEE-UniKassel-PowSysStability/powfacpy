from __future__ import annotations
from warnings import warn
from typing import Union, Callable, Literal
from os import path as os_path
from functools import cached_property
from collections.abc import Iterable

import powfacpy.base.folder
from powfacpy.base.monitored_variables import MonitoredVariables
from powfacpy.base.projects import Projects
from powfacpy.base.study_cases import StudyCases
from powfacpy.exceptions import (
    PFNoActiveStudyCaseError,
    PFNotActiveError,
    PFInvalidLoadFlow,
    PFAttributeNotSetError,
)
from powfacpy.pf_classes.protocols import (
    PFApp,
    PFGeneral,
    ElmRes,
    ElmNet,
    IntComtrade,
    IntScenario,
    IntUser,
    IntCase,
    IntEvt,
    ComLdf,
    IntMon,
    IntVersion,
    IntPrj,
    IntScheme,
    SetTime,
    SetColscheme,
)


#: Read-only accessors backed by an ``app.<method>(*args)`` call. Single source
#: of truth - installed as ``property`` on ``ActiveProject`` and as
#: ``functools.cached_property`` on ``ActiveProjectCached`` by
#: ``_install_app_accessors`` (called right after each class body). All of these
#: are stable for the lifetime of an active project, so caching them is safe.
_APP_ACCESSORS: dict[str, tuple] = {
    "network_model_folder": ("GetProjectFolder", "netmod"),
    "network_data_folder": ("GetProjectFolder", "netdat"),
    "operation_scenarios_folder": ("GetProjectFolder", "scen"),
    "variations_folder": ("GetProjectFolder", "scheme"),
    "study_cases_folder": ("GetProjectFolder", "study"),
    "equipment_type_lib_folder": ("GetProjectFolder", "equip"),
    "library_folder": ("GetProjectFolder", "lib"),
    "scripts_folder": ("GetProjectFolder", "scripts"),
    "templates_folder": ("GetProjectFolder", "templ"),
    "zones_folder": ("GetDataFolder", "ElmZone"),
    "areas_folder": ("GetDataFolder", "ElmArea"),
    "boundaries_folder": ("GetDataFolder", "IntBoundary"),
    "circuits_folder": ("GetDataFolder", "IntCircuit"),
    "feeders_folder": ("GetDataFolder", "IntFeeder"),
    "active_user_folder": ("GetCurrentUser",),
    "global_library_folder": ("GetGlobalLibrary",),
}


def _install_app_accessors(cls, wrapper) -> None:
    """Install `_APP_ACCESSORS` on `cls`, wrapped in `wrapper`
    (`property` for `ActiveProject`, `cached_property` for `ActiveProjectCached`).
    """
    for name, (getter, *args) in _APP_ACCESSORS.items():

        def accessor(self, _getter=getter, _args=tuple(args)):
            return getattr(type(self).app, _getter)(*_args)

        accessor.__name__ = name
        accessor.__qualname__ = f"{cls.__qualname__}.{name}"
        accessor.__doc__ = f"`app.{getter}({', '.join(map(repr, args))})`"
        descriptor = wrapper(accessor)
        set_name = getattr(descriptor, "__set_name__", None)
        if set_name is not None:
            set_name(cls, name)
        setattr(cls, name, descriptor)


class ActiveProject(powfacpy.base.folder.Folder):
    """Interface to the currently active project."""

    app: PFApp

    def __init__(self, pf_app: PFApp | None | bool = False):
        if pf_app:
            self.__class__.app = pf_app
        elif pf_app is None:
            raise TypeError(
                "The input app is of type 'NoneType'. Maybe the PowerFactory app was not loaded correctly."
            )

    @property
    def _obj(self) -> IntPrj:
        return self.get_active_project()

    @property
    def load_flow_command(self) -> ComLdf:
        return self.get_from_study_case("ComLdf")

    # The app accessors (network_model_folder, study_cases_folder, zones_folder,
    # active_user_folder, global_library_folder, ...) are installed from the
    # _APP_ACCESSORS table right after this class - as plain 'property' here and
    # as 'cached_property' on ActiveProjectCached. They also serve as attribute
    # aliases for the method-style getters (get_active_user_folder() etc.).

    @property
    def versions_folder(self):
        return self.get_unique_obj("*.IntVersionman")

    @property
    def active_study_case(self) -> IntCase | None:
        """Alias of `get_active_study_case(error_if_no_active_case=False)`.

        Not in `_APP_ACCESSORS` / never cached - it changes on study-case activation.
        """
        return self.__class__.app.GetActiveStudyCase()

    @property
    def stored_attr(self) -> dict:
        """DatabaseDict to store and reset attributes of PF objects."""
        try:
            return self._stored_attr
        except AttributeError:
            from powfacpy.applications.database import (
                DatabaseDict,
            )  # import here to avoid circular import

            self._stored_attr = DatabaseDict({})
            return self._stored_attr

    def set_attr_resettable(
        self,
        obj: PFGeneral | str,
        params: dict,
        parent_folder: PFGeneral | powfacpy.base.folder.Folder | str = None,
    ) -> None:
        """Set attributes of an object, remembering the value from before the *first* call.

        Call `reset_stored_attr()` afterwards to restore those remembered values.
        Calling this method several times for the same object/attribute keeps the
        value seen on the first call (so a later reset restores the true original,
        not the value in between).

        Args:
            obj (PFGeneral | str): PF object or its path
            params (dict): parameter names (keys) and values (values)
            parent_folder (PFGeneral | Folder | str, optional): parent folder of object. Defaults to None.
        """
        obj = self._handle_single_pf_object_or_path_input(obj, parent_folder=parent_folder)
        for attr, new_val in params.items():
            stored = self.stored_attr.get(obj)
            if stored is None:
                self._stored_attr[obj] = {attr: self.get_attr(obj, attr)}
            elif attr not in stored:
                stored[attr] = self.get_attr(obj, attr)
            # else: the original was already remembered on an earlier call - keep it
            obj.SetAttribute(attr, new_val)

    def reset_stored_attr(
        self, flush_memory: bool = False, store_current_values: bool = False
    ) -> None:
        """Reset the original values stored when calling 'set_attr_resettable'.

        Args:
            flush_memory (bool, optional): Stored values will be deleted. Defaults to False.
            store_current_values (bool, optional): Current values will be written to the dictionary of the stored values. Defaults to False.
        """
        if not store_current_values:
            self.stored_attr.set_values_of_dict_in_pf()
            if flush_memory:
                del self._stored_attr
        else:
            self.stored_attr.set_values_of_dict_in_pf_and_store_original()

    def get_active_study_case(
        self, error_if_no_active_case: bool = True
    ) -> IntCase | None:
        """Get the currently active study case. Control whether error should be raised if no case is active.

        Args:
            error_if_no_active_case (bool, optional): If True, raise exception if no case is active. If False, return none. Defaults to True.

        Raises:
            PFNoActiveStudyCaseError: When no case is active.

        Returns:
            IntCase: The active study case | None
        """
        case = self.__class__.app.GetActiveStudyCase()
        if case or not error_if_no_active_case:
            return case
        else:
            raise PFNoActiveStudyCaseError()

    def get_from_study_case(
        self,
        class_name: str,
        if_not_unique: Literal["warning", "error"] | None = "warning",
        if_no_study_case: Literal["warning", "error"] | None = "error",
    ) -> PFGeneral:
        """Get objects from active study case (similar to PF built-in function 'app.GetFromStudyCase()').

        Additionally, this method prints a warning or raises an exception if there is more than one object found in the study case and if no study case is activated.

        Args:
            class_name (str): class name of the object (e.g. 'ElmRes'), optionally preceded by an object name without wildcards and a dot (e.g. 'All Calcualations.ElmRes')

            if_not_unique ('warning' | 'error' | None, optional): Warn, raise, or do nothing if there is more than one object of class 'class_name'. Defaults to "warning".

            if_no_study_case ('warning' | 'error' | None, optional): Warn, raise, or do nothing if no study case is active. Defaults to "error".

        Raises:
            ValueError: Invalid 'if_not_unique' / 'if_no_study_case' value
            PFNoActiveStudyCaseError: No study case activated
            TypeError: More than one object was found

        Returns:
            PFGeneral: Found or created object
        """
        for arg_name, arg_value in (
            ("if_not_unique", if_not_unique),
            ("if_no_study_case", if_no_study_case),
        ):
            if arg_value and arg_value not in ("warning", "error"):
                raise ValueError(
                    f"{arg_name}={arg_value!r} - expected 'warning', 'error' or None."
                )
        obj = self.__class__.app.GetFromStudyCase(class_name)

        if if_no_study_case and not self.__class__.app.GetActiveStudyCase():
            if if_no_study_case == "warning":
                warn(
                    "No study case activated. PowerFactory creates object of class_name in tmp folder, outside any study case."
                )
            elif if_no_study_case == "error":
                raise PFNoActiveStudyCaseError()

        if if_not_unique and self.is_pf_class(class_name):
            class_name = "*." + class_name
            all_objects_of_this_class = self.get_obj(
                class_name, parent_folder=obj.GetParent(), include_subfolders=False
            )
            if len(all_objects_of_this_class) > 1:
                parent_path = self.get_path_of_object(obj.GetParent())
                if if_not_unique == "warning":
                    warn(
                        f"The returned {class_name} object is not unique in the  study case: '{parent_path}'. Make sure that the correct {class_name} object is used: {obj}."
                    )
                if if_not_unique == "error":
                    raise TypeError(
                        f"The returned {class_name} object is not unique in its folder / in its study case: '{parent_path}'."
                    )
        return obj

    def reactivate_study_case(self) -> None:
        case = self.get_active_study_case()
        case.Deactivate()
        case.Activate()

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
        condition: Callable | None = None,
        error_if_non_existent=True,
        includeOutOfService: int = 1,
        topoElementsOnly: int = 0,
        bAcSchemes: int = 0,
    ) -> list[PFGeneral]:
        """Wraps the method 'GetCalcRelevantObjects' (see PF scripting reference) and adds optional arguments similar to 'get_obj'.

        Warning: If 'obj_str' contains several objects separated by comma, the order of the returned objects may differ from the order in the string.

        Args:
            obj_str (str): name including class of object(s) (NOT their path)

            condition (Callable | None, optional): See get_obj. Defaults to lambda x:True.

            error_if_non_existent (bool, optional): See get_obj. Defaults to True.

            includeOutOfService (int, optional): Flag whether to include out of service objects. Defaults to 1. (Copied from scripting reference)

            topoElementsOnly (int, optional): Flag to filter for topology relevant objects only. Defaults to 0. (Copied from scripting reference)

            bAcSchemes (int, optional): Flag to include hidden objects in active schemes. Defaults to 0. (Copied from scripting reference)

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
        if condition is not None:
            obj_with_condition = self.get_by_condition(objs, condition)
            if obj_with_condition:
                return obj_with_condition
            else:
                return self._handle_condition_of_obj_not_met(
                    obj_str, self.get_active_project(), error_if_non_existent
                )
        else:
            return objs

    @cached_property
    def monitored_variables(self) -> MonitoredVariables:
        """Helper to manage the monitored variables / contents of results objects (`ElmRes`)."""
        return MonitoredVariables(self)

    def add_results_variable(
        self,
        obj: PFGeneral | str | list[PFGeneral | str],
        variables: str | list[str],
        results_obj: ElmRes | None = None,
    ) -> ElmRes:
        """Add variable(s) of 'obj' to the monitored variables of a results object.

        Forwards to `self.monitored_variables.add` - see `MonitoredVariables`.
        """
        return self.monitored_variables.add(obj, variables, results_obj)

    def clear_results_variables(
        self,
        results_obj: ElmRes | None = None,
    ) -> None:
        """Delete all variable selection objects (`IntMon`) from a results object.

        Forwards to `self.monitored_variables.clear` - see `MonitoredVariables`.
        """
        return self.monitored_variables.clear(results_obj)

    def add_variable_selection_obj_to_results_obj(
        self,
        name,
        results_obj: ElmRes,
        class_name: str = None,
        variables: list[str] = [],
    ) -> IntMon:
        """Add a variable selection object (`IntMon`) to a results object (`ElmRes`).

        Forwards to `self.monitored_variables.add_variable_selection_obj` - see `MonitoredVariables`.
        """
        return self.monitored_variables.add_variable_selection_obj(
            name, results_obj, class_name, variables
        )

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

    def get_global_library_folder(self) -> PFGeneral:
        return self.__class__.app.GetGlobalLibrary()

    def get_from_global_library(self, name: str | list[str]) -> PFGeneral:
        """Get object(s) from global library.

        Args:
            name (str): name(s) of object(s) to get from global library (used for 'GetContents').

        Returns:
            PFGeneral: Object(s) from global library
        """
        global_lib = self.get_global_library_folder()
        if not isinstance(name, list):
            return global_lib.GetContents(name, 1)
        else:
            return [global_lib.GetContents(obj_name, 1) for obj_name in name]

    def get_project_directory(self) -> str:
        """Get the project directory (for related files).

        Returns:
            str: Path
        """
        return self._obj.projectDirectory

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
            raise PFNotActiveError("a network (ElmNet).")
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
        """Delete entries of a results object (`ElmRes`) whose referenced object (`obj_id`) is deleted.

        Forwards to `self.monitored_variables.clear_elmres_from_deleted_objects`.
        """
        return self.monitored_variables.clear_elmres_from_deleted_objects(results_obj)

    def clear_elmres(self, results_obj: ElmRes = None):
        """Clear all contents of a results object (`ElmRes`).

        Forwards to `self.monitored_variables.clear_elmres`.
        """
        return self.monitored_variables.clear_elmres(results_obj)

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

    @cached_property
    def study_cases(self) -> StudyCases:
        """Helper to create study cases, variations and scenarios (see `StudyCases`)."""
        return StudyCases(self)

    def create_study_case(
        self,
        name: str,
        copy_from: IntCase | str | None = None,
        parent_folder: PFGeneral | str | None = None,
        create_variation: bool = False,
        create_scenario: bool = False,
        overwrite: bool = True,
        use_existing=False,
        activate: bool = True,
    ) -> IntCase | list[IntCase | IntScheme | IntScenario]:
        """Create a study case (+ optional parallel variation/scenario). See `StudyCases.create`."""
        return self.study_cases.create(
            name,
            copy_from=copy_from,
            parent_folder=parent_folder,
            create_variation=create_variation,
            create_scenario=create_scenario,
            overwrite=overwrite,
            use_existing=use_existing,
            activate=activate,
        )

    def _get_path_of_folder_of_study_case_inside_study_cases_folder(
        self, case: IntCase | None
    ) -> str | None:
        """See `StudyCases._folder_of_case_inside_study_cases_folder`."""
        return self.study_cases._folder_of_case_inside_study_cases_folder(case)

    def create_parallel_variation_for_study_case(
        self, case: IntCase | str, overwrite: bool = True, activate: bool = True
    ) -> IntScheme:
        """See `StudyCases.create_parallel_variation`."""
        return self.study_cases.create_parallel_variation(
            case, overwrite=overwrite, activate=activate
        )

    def create_parallel_scenario_for_study_case(
        self, case: IntCase | str, overwrite: bool = True, activate: bool = True
    ) -> IntScenario:
        """See `StudyCases.create_parallel_scenario`."""
        return self.study_cases.create_parallel_scenario(
            case, overwrite=overwrite, activate=activate
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
        """Create a variation (including one expansion stage). See `StudyCases.create_variation`."""
        return self.study_cases.create_variation(
            name,
            parent_folder=parent_folder,
            name_expansion_stage=name_expansion_stage,
            activationTime=activationTime,
            activate=activate,
            overwrite=overwrite,
        )

    def create_scenario(
        self,
        name: str,
        parent_folder: str | PFGeneral = None,
        activate: bool = True,
        overwrite: bool = True,
    ) -> IntScenario:
        """Create an operation scenario. See `StudyCases.create_scenario`."""
        return self.study_cases.create_scenario(
            name, parent_folder=parent_folder, activate=activate, overwrite=overwrite
        )

    def execute_load_flow(self, params: dict = {}) -> int:
        """Execute load flow.

        Args:
            params (dict, optional): Parameter and values for the load flow calculation object (ComLdf). Defaults to {}.

        Returns:
            int: Return value of ComLdf.Execute()
            - 0 OK
            - 1 Load flow failed due to divergence of inner loops.
            - 2 Load flow failed due to divergence of outer loops.
        """
        comldf: ComLdf = self.get_from_study_case("ComLdf")
        self.set_attr(comldf, params=params)
        return comldf.Execute()

    def has_valid_load_flow_results(self) -> bool:
        return self.app.IsLdfValid() != 0

    def check_load_flow_results(self, when_invalid: str = "error") -> bool:
        """
        Check whether load flow results in PF are present and valid and raise exception, warning or execute load flow if not.

        Args:
            when_invalid (str, optional): If load flow results are invalid, 'error' (raises exception), 'warning' raises warning, 'execute' executes load flow and raises exception if results are invalid. Defaults to "error".

        Raises:
            PFInvalidLoadFlow: When load flow results are invalid and 'when_invalid'= 'error' or 'execute' and results are invalid.

        Returns:
            bool: True only when results are valid.
        """
        if self.app.IsLdfValid() != 0:
            return True
        if when_invalid == "execute":
            valid = self.execute_load_flow()
            if valid != 0:
                raise PFInvalidLoadFlow()
            return True
        elif when_invalid == "warning":
            warn("No valid load flow results.", UserWarning)
            return False
        else:
            raise PFInvalidLoadFlow()

    def mark_in_graphics(
        self, elms: list[PFGeneral] | PFGeneral, searchOpenedDiagramsOnly: int = 0
    ) -> None:
        if not isinstance(elms, list):
            elms = [elms] if not isinstance(elms, Iterable) else list(elms)
        self.__class__.app.MarkInGraphics(elms, searchOpenedDiagramsOnly)

    def _handle_possible_attribute_not_set_error(
        self, possibly_not_secified_attr: str, attribute_description: str, error_message
    ):
        """Handles the exception if in a method call (of this class) an AttributeError is raised because of an attribute of this class is not set (i.e. is None).

        Example:
            A method uses self.active_case and active_case is None.
        """
        if not possibly_not_secified_attr:
            raise PFAttributeNotSetError(attribute_description)
        else:
            raise AttributeError(error_message)

    @cached_property
    def projects(self) -> Projects:
        """Helper for project versions, `.pfd`/`.dz` import & export, templates (see `Projects`)."""
        return Projects(self)

    def get_project_version(self, version_name: str) -> IntVersion | None:
        """Get a stored project version by name. See `Projects.get_version`."""
        return self.projects.get_version(version_name)

    def create_project_version(self, version_name: str, overwrite: bool = True) -> None:
        """Snapshot the current project state as a version. See `Projects.create_version`."""
        return self.projects.create_version(version_name, overwrite=overwrite)

    def rollback_project_to_previous_version(self, version_name: str) -> None:
        """Roll the project back to a stored version. See `Projects.rollback_to_version`."""
        return self.projects.rollback_to_version(version_name)

    def import_project(
        self,
        file_path: str,
        target_folder_in_active_user: str | PFGeneral | None = None,
        keep_current_project_activated: bool = True,
    ) -> IntPrj:
        """Import a project (.pfd file). See `Projects.import_pfd`."""
        return self.projects.import_pfd(
            file_path,
            target_folder_in_active_user=target_folder_in_active_user,
            keep_current_project_activated=keep_current_project_activated,
        )

    def export_to_pfd(
        self,
        file_path: str,
        objects: PFGeneral | str | list[PFGeneral | str] | None = None,
    ) -> str:
        """Export to a `.pfd` file (counterpart of `import_project`). See `Projects.export_pfd`."""
        return self.projects.export_pfd(file_path, objects)

    def import_dz_file(
        self, file_path: str, target_folder: PFGeneral | None = None
    ) -> list:
        """Import a .dz file (e.g. a template). See `Projects.import_dz`."""
        return self.projects.import_dz(file_path, target_folder)

    def set_time_using_year(self, year):
        settime: SetTime = self.get_from_study_case("SetTime")
        average_seconds_per_year = 31556952
        approximate_time_in_seconds_since_1970 = (
            year - 1970
        ) * average_seconds_per_year
        settime.SetTimeUTC(approximate_time_in_seconds_since_1970)

    def reset_default_units(self) -> None:
        """Reset the default units of the active project. See `Projects.reset_default_units`."""
        return self.projects.reset_default_units()

    def reactivate_project(self) -> None:
        """Deactivate and activate the active project. See `Projects.reactivate`."""
        return self.projects.reactivate()

    def add_template_from_global_library(
        self, template_name: str | list[str], target_folder: PFGeneral | None = None
    ) -> PFGeneral:
        """Add a template from the global library to the active project. See `Projects.add_template_from_global_library`."""
        return self.projects.add_template_from_global_library(
            template_name, target_folder
        )

    def duplicate_to_restore_attributes(
        self,
        obj: PFGeneral | str,
        attr: str | list[str],
        parent_folder: PFGeneral | powfacpy.base.folder.Folder | str = None,
        suffix_of_duplicate: str = "_COPY",
    ) -> PFGeneral:
        obj = self._handle_single_pf_object_or_path_input(
            obj, parent_folder=parent_folder
        )
        name_of_copy = obj.loc_name + suffix_of_duplicate
        copy_of_obj = self.get_unique_obj(
            name_of_copy, parent_folder=obj.GetParent(), error_if_non_existent=False
        )
        if copy_of_obj:
            if not isinstance(attr, list):
                obj.SetAttribute(attr, copy_of_obj.GetAttribute(attr))
            else:
                for a in attr:
                    obj.SetAttribute(a, copy_of_obj.GetAttribute(a))
        else:
            self.copy_single_obj(obj, obj.GetParent(), new_name=name_of_copy)

    def clear_output_window(self) -> None:
        self.app.ClearOutputWindow()


_install_app_accessors(ActiveProject, property)


class ActiveProjectCached(ActiveProject):
    """Caches the properties. Should be used only with one active project (the caching fails after a different project has been activated)."""

    @cached_property
    def _obj(self):
        return self.get_active_project()

    @cached_property
    def versions_folder(self):
        return self.get_unique_obj("*.IntVersionman")


# `active_user_folder` / `global_library_folder` become cached here (session-
# stable). `active_study_case` stays a plain property - it must always reflect
# the currently active case.
_install_app_accessors(ActiveProjectCached, cached_property)
