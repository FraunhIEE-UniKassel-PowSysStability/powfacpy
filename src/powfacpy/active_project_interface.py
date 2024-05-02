from __future__ import annotations
from warnings import warn
from os import replace
from typing import Union, Callable
from os import path as os_path
from warnings import warn

import powfacpy
from powfacpy.pf_class_protocols import PFApp, PFGeneral, ElmRes, ElmNet, IntComtrade, IntUser, IntCase, IntEvt, ElmZone, ComLdf
from powfacpy.folders_interface import PFFolder


class PFActiveProject(PFFolder):
    """Interface to the currently active project.
    """

    def __init__(self, pf_app: PFApp):
        if pf_app:
            self.app: PFApp = pf_app
        else:
            raise TypeError(
                "The input app is of type 'NoneType'. Maybe the PowerFactory app was not loaded correctly.")

    @property
    def _folder(self):
        return self.get_active_project()

    @property
    def network_model_folder(self):
        return self.app.GetProjectFolder("netmod")

    @property
    def network_data_folder(self):
        return self.app.GetProjectFolder("netdat")

    @property
    def operation_scenarios_folder(self):
        return self.app.GetProjectFolder("scen")

    @property
    def variations_folder(self):
        return self.app.GetProjectFolder("scheme")

    @property
    def study_cases_folder(self):
        return self.app.GetProjectFolder("study")

    @property
    def equipment_type_lib_folder(self):
        return self.app.GetProjectFolder("equip")

    @property
    def library_folder(self):
        return self.app.GetProjectFolder("lib")

    @property
    def scripts_folder(self):
        return self.app.GetProjectFolder("scripts")

    @property
    def templates_folder(self):
        return self.app.GetProjectFolder("templ")

    @property
    def zones_folder(self):
        return self.app.GetDataFolder("ElmZone")

    @property
    def areas_folder(self):
        return self.app.GetDataFolder("ElmArea")

    @property
    def boundaries_folder(self):
        return self.app.GetDataFolder("IntBoundary")

    @property
    def circuits_folder(self):
        return self.app.GetDataFolder("IntCircuit")

    @property
    def feeders_folder(self):
        return self.app.GetDataFolder("IntFeeder")
    
    def get_active_study_case(
        self, 
        error_if_no_active_case: bool = True) -> IntCase | None:
        """Get the currently active study case. Control whether error should be raised if no case is active.

        Args:
            error_if_no_active_case (bool, optional): If True, raise exception if no case is active. If False, return none. Defaults to True.

        Raises:
            powfacpy.PFNoActiveStudyCaseError: When no case is active.

        Returns:
            IntCase: The active study case | None
        """
        case = self.app.GetActiveStudyCase()
        if case or not error_if_no_active_case:
            return case
        else:
            raise powfacpy.PFNoActiveStudyCaseError()
            
    def get_from_study_case(self,
                            class_name: str,
                            if_not_unique: str = "warning", if_no_study_case: str = "error") -> PFGeneral:
        """Get objects from active study case (similar to PF built-in function 'app.GetFromStudyCase()').

        Additionally, this method prints a warning or raises an exception if there is more than one object found in the study case and if no study case is activated.

        Args:
            class_name (str): class name of the object (e.g. 'ElmRes'), optionally preceded by an object name without wildcards and a dot (e.g. 'All Calcualations.ElmRes')

            if_not_unique (str, optional): Warn ('warning') or raise exception ('error') if there are more than one objets of class 'class_name'. Defaults to "warning".

            if_no_study_case (str, optional): Warn ('warning') or raise exception ('error') if no study case is active. Defaults to "error".

        Raises:
            powfacpy.PFNoActiveStudyCaseError: No study case activated
            TypeError: More than one object was found

        Returns:
            PFGeneral: Found or created object
        """
        study_case = self.app.GetActiveStudyCase()
        object = self.app.GetFromStudyCase(class_name)

        if not study_case:
            if if_no_study_case == "warning":
                warn("No study case activated. PowerFactory creates object of class_name in tmp folder, outside any study case.")
            elif if_no_study_case == "error":
                raise powfacpy.PFNoActiveStudyCaseError()

        if if_not_unique:
            if not '.' in class_name:
                search_string = "*." + class_name
            all_objects_of_this_class = self.get_obj(
                search_string, parent_folder=object.GetParent(), include_subfolders=False)
            if len(all_objects_of_this_class) > 1:
                parent_path = self.get_path_of_object(object.GetParent())
                if if_not_unique == "warning":
                    warn(
                        f"The returned {class_name} object is not unique in its folder / in its study case: '{parent_path}'. Make sure that the correct {class_name} object is used.")
                if if_not_unique == "error":
                    raise TypeError(
                        f"The returned {class_name} object is not unique in its folder / in its study case: '{parent_path}'")
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

    def get_calc_relevant_obj(self,
                              obj_str: str,
                              condition: Callable = lambda x: True,
                              error_if_non_existent = True,
                              includeOutOfService: int = 1,
                              topoElementsOnly: int = 0,
                              bAcSchemes: int = 0) -> list[PFGeneral]:
        """Wraps the method 'GetCalcRelevantObjects' (see PF scripting reference) and adds optional arguments similar to 'get_obj'.

        Args:
            obj_str (str): name inlcuding class of object(s) (NOT their path)
            
            condition (Callable, optional): See get_obj. Defaults to lambdax:True.
            
            error_if_non_existent (bool, optional): See get_obj. Defaults to True.
            
            From scripting reference:
            
            includeOutOfService (int, optional): Flag whether to include out of service objects. Defaults to 1.
            
            topoElementsOnly (int, optional): Flag to filter for topology relevant objects only. Defaults to 0.
            
            bAcSchemes (int, optional): Flag to include hidden objects in active schemes. Defaults to 0.

        Returns:
            list[PFGeneral]: Found object(s)
        """    
        objs = self.app.GetCalcRelevantObjects(obj_str,
                                               includeOutOfService,
                                               topoElementsOnly,
                                               bAcSchemes)
        if not objs:
            return self._handle_non_existing_obj(
                obj_str, 
                self.get_active_project(), 
                error_if_non_existent)
        if condition:
            obj_with_condition = self.get_by_condition(objs, condition)
            if obj_with_condition:
                return obj_with_condition
            else:
                return self._handle_condition_of_obj_not_met(obj_str, self.get_active_project(), error_if_non_existent)
        else:
            return objs 

    def add_results_variable(self,
                             obj: PFGeneral | str | list[PFGeneral | str],
                             variables: str | list[str],
                             results_obj: ElmRes = None) -> ElmRes:
        """Add variables of 'obj' to the monitored variables of result object.

        Args:
        
            obj (PFGeneral | str | list[PFGeneral | str]): PF object or its path
            
            variables (list[str]): variable names
            
            results_obj (ElmRes, optional): Results object. Defaults to None (ElmRes from active study case is used).

        Returns:
            ElmRes: the results object
        """
        if not results_obj:
            results_obj = self.get_from_study_case("ElmRes")
        else:
            results_obj = self._handle_single_pf_object_or_path_input(
                results_obj)
        obj = self._handle_pf_object_or_path_input(obj)
        if isinstance(variables, str):
            variables = [variables]
        for o in obj:     
            for var in variables:
                results_obj.AddVariable(o, var)
        results_obj.Load()
        return results_obj

    def get_first_level_folder(self, folder_type: str) -> PFGeneral:
        """Get folder on first level of PF database.

        Args:
            folder_type (str): The folder of the active user ('user') or the global library ('global library') can be accessed.

        Raises:
            TypeError: Invalid folder_tpe input

        Returns:
            PFGeneral: first level folder
        """
        if folder_type == "user":
            return self.app.GetCurrentUser()
        elif folder_type == "global library":
            return self.app.GetGlobalLibrary()
        else:
            raise TypeError(
                f"The first level folder {folder_type} is not valid. Use one of these: 'user', 'global library'.")

    def get_active_user_folder(self) -> IntUser:
        """Get folder of active user.
        """
        return self.app.GetCurrentUser()

    def get_active_networks(
            self,
            error_if_no_network_is_active: bool = True) -> ElmNet:
        """Get active networks/grids.  
        """
        grids = self.app.GetCalcRelevantObjects(
            ".ElmNet")  # This also returns the summary grid in the study case
        # Delete the summary grid which is in the study case
        grids[:] = [grid for grid in grids if not grid.GetParent().GetClassName() == "IntCase"]
        if error_if_no_network_is_active and not grids:
            raise powfacpy.PFNotActiveError("a network (ElmNet).")
        return grids

    def activate_study_case(self, path: str) -> IntCase:
        """Activate study case under path.
        """
        study_case = self.get_single_obj(path, include_subfolders=False)
        study_case.Activate()
        return study_case

    def clear_elmres_from_objects_with_status_deleted(
            self,
            results_obj: ElmRes = None):
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

    def get_parameter_value_string(self,
                                   parameters: dict,
                                   delimiter=" ") -> str:
        """Get string with parameters and their values.

        Args:
            parameters (dict): parameters (keys) and values (values)
            Example: {'P': 'user\\project\\path\\to\\object\\m:Psum:bus1'}

            delimiter (str, optional): Delimiter between parameter value pairs. Defaults to " ".

        Returns:
            str: parameter value string (e.g. 'P = 2.5')
        """
        param_value_string = ""
        for parname, path_with_par in parameters.items():
            value = self.get_attr_by_path(path_with_par)
            param_value_string += parname + "=" + str(value) + delimiter
        return param_value_string[:-len(delimiter)]  # omit last delimiter

    def create_comtrade_obj(self,
                            file_path: str,
                            parent_folder: Union[PFGeneral, str] = None) -> IntComtrade:
        """Add an IntComtrade that refers to file_path (*.cfg).
        The objects are stored in a folder "Comtrade" in the currently active
        study case, unless a parent_folder is given. A new object is only
        created if there exists no object yet that points to the same file
        ('f_name' attribute is the file path). The file name is used for the
        new object name (without the .cfg ending).
        """
        if parent_folder:
            parent_folder = self._handle_single_pf_object_or_path_input(
                parent_folder)
        else:
            parent_folder = self.app.GetFromStudyCase("Comtrade.IntFolder")

        intcomtrade: IntComtrade = self.get_obj("*.IntComtrade",
                                                parent_folder=parent_folder,
                                                condition=lambda x: getattr(
                                                    x, "f_name") == file_path,
                                                error_if_non_existent=False)
        if not intcomtrade:
            _, file_name = os_path.split(file_path)
            intcomtrade = self.create_in_folder(
                file_name.replace(".cfg", "") + ".IntComtrade",
                parent_folder,
                overwrite=False,
                use_existing=False)
            intcomtrade.f_name = file_path
        else:
            intcomtrade = intcomtrade[0]
        # intcomtrade.Load() probably not required
        return intcomtrade
    
    def create_zone(self, 
                    name: str, 
                    elms: list[PFGeneral],
                    color: int = 2,
                    parent_folder: str | PFGeneral = None) -> ElmZone:
        if not parent_folder:
            parent_folder = self.zones_folder
        elmzone: ElmZone = self.create_in_folder(
            name + ".ElmZone", parent_folder)
        elmzone.icolor = color
        for elm in elms:
            elm.cpZone = elmzone
        return elmzone
    
    def execute_load_flow(self, params: dict = {}) -> int:
        comldf: ComLdf = self.get_from_study_case("ComLdf")  
        self.set_attr(comldf, params=params)  
        return comldf.Execute()
        
    def mark_in_graphics(self, 
                         elms: list[PFGeneral] | PFGeneral,
                         searchOpenedDiagramsOnly: int = 0) -> None:
        if not isinstance(elms, list):
            elms = list(elms)
        self.app.MarkInGraphics(elms, searchOpenedDiagramsOnly)
     
    def _handle_possible_attribute_not_set_error(
            self,
            possibly_not_secified_attr: str,
            attribute_description: str,
            error_message):
        """Handles the exception if in a method call (of this class) an AttributeError is raised because of an attribute of this class is not set (i.e. is None).

        Example:
            A method uses self.active_case and active_case is None.
        """
        if not possibly_not_secified_attr:
            raise powfacpy.PFAttributeNotSetError(attribute_description)
        else:
            raise AttributeError(error_message)

    @staticmethod
    def replace_headers_of_csv_file_with_number_of_colums(file_path: str) -> int:
        """Replaces the first row (headers) of a csv file with its number of
        columns. This is needed for import of csv files to PF using ElmFile.
        """
        with open(file_path+".csv") as read_file, open(file_path + ".temp", "w") as write_file:
            columns_of_first_row = read_file.readline().split(",")
            if columns_of_first_row[-1] == "\n":
                columns_of_first_row = columns_of_first_row[:-1]
            # Minus one because first column is time and should not be counted.
            number_of_columns = len(columns_of_first_row)-1
            write_file.write(str(number_of_columns)+"\n")
            row = read_file.readline()
            while row:
                write_file.write(row)
                row = read_file.readline()
        replace(file_path + ".temp", file_path+".csv")
        return number_of_columns

    @staticmethod
    def insert_row_with_number_of_columns_in_csv_file(file_path: str) -> int:
        """Gets the number of columns of the first row in a csv file and
        inserts a row (first row) with this number in the first column.
        This is needed for ElmFile to read csv files.
        """
        with open(file_path+".csv") as read_file, open(file_path + ".temp", "w") as write_file:
            first_row = read_file.readline()
            columns_of_first_row = first_row.split(",")
            if columns_of_first_row[-1] == "\n":
                columns_of_first_row = columns_of_first_row[:-1]
            # Minus one because first column is time and should not be counted.
            number_of_columns = len(columns_of_first_row)-1
            write_file.write(str(number_of_columns)+"\n")
            write_file.write(first_row)
            row = read_file.readline()
            while row:
                write_file.write(row)
                row = read_file.readline()
        replace(file_path + ".temp", file_path+".csv")
        return number_of_columns


class PFBaseInterface(PFActiveProject):
    """Please use the class PFActiveProject instead.
    """

    def __init__(self, pf_app: PFApp):
        warn(f'{self.__class__.__name__} will be deprecated. Please use the class PFActiveProject instead',
             DeprecationWarning, stacklevel=2)
        super().__init__(pf_app)
