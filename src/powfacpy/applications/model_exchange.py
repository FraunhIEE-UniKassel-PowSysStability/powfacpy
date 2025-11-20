"""
This module provides an interface to import/export data in CGMES format.
"""

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_classes.protocols import PFApp, CimArchive, ElmNet, PFGeneral
from typing import Union

class CGMES(ApplicationBase):
    """Interface for CGMES integration in PowerFactory."""

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)
        self.import_archive_name: str = "archive_imported"
        self.export_archive_name: str = "archive_exported"
        self.file_to_archive_tool: str = "cgmes_file_to_archive"
        self.archive_to_file_tool_name: str = "cgmes_archive_to_file"
        self.archive_to_grid_tool_name: str = "cgmes_archive_to_grid"
        self.grid_to_archive_tool_name: str = "cgmes_grid_to_archive"
        self.exported_zip_name: str = "cgmes_profiles"
        self.cgmes_version: str = "CGMES 3.0.0"
        self._all_profiles: str = "eq tp ssh sc sv dy dl gl"

    @property
    def archive_folder(self):
        return self.act_prj.app.GetProjectFolder("cim")

    # Import methods

    def _create_cim_to_grid_tool(self):
        """Returns the CIM to Grid tool object .ComCimtogrid."""
        cim_to_grid_tool = self.act_prj.create_in_folder(
            self.archive_to_grid_tool_name + ".ComCimtogrid",
            self.act_prj.app.GetActiveStudyCase(),
            use_existing=True,
        )
        return cim_to_grid_tool

    def _convert_file_to_archive(self, file_path: str, name: str) -> CimArchive:
        """Convert a .zip CGMES file to a PowerFactory .CimArchive object. Returns the .CimArchive object."""
        file_to_archive_tool = self.act_prj.create_in_folder(
            self.file_to_archive_tool + ".ComCimdbimp",
            self.act_prj.app.GetActiveStudyCase(),
            use_existing=True,
        )
        file_to_archive_tool.iopt_target = 2
        archive = self._create_archive(name=name)
        file_to_archive_tool.targetPath = archive
        file_to_archive_tool.fileName = file_path
        file_to_archive_tool.Execute()
        return archive

    def _convert_archive_to_grid(self, cim_archive: CimArchive) -> ElmNet:
        """Convert a PowerFactory .CimArchive to a grid. Returns None."""
        grid = self.act_prj.create_in_folder(
            "temp_grid.ElmNet", self.act_prj.network_data_folder
        )
        cim_to_grid_tool = self._create_cim_to_grid_tool()
        cim_to_grid_tool.sourcePath = cim_archive
        cim_to_grid_tool.dependencies = None
        cim_to_grid_tool.partial = 0
        cim_to_grid_tool.pGrid = [grid]  # TODO find out if grid has to be given
        cim_to_grid_tool.Execute()
        return grid

    def cgmes_import(self, input_path: str):
        """Converts CGMES .zip files to a PowerFactory grid.

        Args:
            input_path (str): Path to the CGMES .zip archive, containing xml profiles.

        Returns:
            None
        """
        archive = self._convert_file_to_archive(input_path, self.import_archive_name)
        return self._convert_archive_to_grid(archive)

    def update_profiles(self, update_file_path: str, base_archive: CimArchive | str):
        """Includes new SSH (and DL) profiles into an already imported grid.

        Args:
            update_file_path (str): Path to the CGMES .zip archive, containing profiles for updating (SSH and optionally DL).
            base_archive (CimArchive | str) Base .CimArchive which the already imported grid has been created from.

        Returns:
            None
        """
        base_archive = self.act_prj._handle_single_pf_object_or_path_input(base_archive)
        update_profiles_archive = self._convert_file_to_archive(
            update_file_path, self.import_archive_name+"_update"
        )
        cim_to_grid_tool = self._create_cim_to_grid_tool()
        cim_to_grid_tool.sourcePath = update_profiles_archive
        cim_to_grid_tool.dependencies = base_archive
        cim_to_grid_tool.partial = 1
        profiles_in_update_file = [
            file.loc_name.split("_")[-2]
            for file in update_profiles_archive.GetContents()
        ]
        self._set_profiles_of_cim_tool(cim_to_grid_tool, profiles=self._all_profiles, state=False)
        self._set_profiles_of_cim_tool(
            cim_to_grid_tool, profiles=" ".join(profiles_in_update_file), state=True
        )
        # cim_to_grid_tool.pGrid = [grid] # TODO find out if grid has to be given
        cim_to_grid_tool.Execute()
        return None

    # Export methods

    def _create_grid_to_cim_tool(self):
        """Returns the Grid to CIM tool object .ComGridtocim."""
        grid_to_cim_tool = self.act_prj.create_in_folder(
            self.grid_to_archive_tool_name + ".ComGridtocim",
            self.act_prj.app.GetActiveStudyCase(),
            use_existing=True,
        )
        grid_to_cim_tool.cAuthority = ["Authority1"]  # TODO this probably isn't general
        grid_to_cim_tool.cSelected = [
            1
        ]  # TODO this probably isn't general (should all grids be selected? or actually only the first one?) --> get project with >1 grid and get to run properly
        grid_to_cim_tool.version = self.cgmes_version
        return grid_to_cim_tool

    def _create_archive(self, name):
        """Create a PowerFactory .CimArchive object. Returns the .CimArchive object."""
        archive = self.act_prj.create_in_folder(
            name + ".CimArchive",
            self.archive_folder,
            use_existing=False,
            overwrite=True,
        )
        return archive

    def _set_profiles_of_cim_tool(self, cim_tool, profiles: str, state: bool):
        """Sets the profiles of PowerFactory .ComCimtogrid or .ComGridtocim tools listet in profiles to state.
        Args:
            cim_tool (str): .ComCimtogrid or .ComGridtocim tool.
            profiles (str): String of CGMES profiles to be set in the tool, separeted by single spaces (e.g. 'ssh dl').
            state (bool): State to set the selected profiles to (True=checked, False=unchecked).
        Returns:
            None
        """
        cim_tool = self.act_prj._handle_single_pf_object_or_path_input(cim_tool)
        for profile in profiles.split(" "):
            cim_tool.SetAttribute("convert" + profile.upper(), state)
        return None

    def _convert_grid_to_archive(self, selected_profiles: str = "all"):
        """Convert a PowerFactory grid to a .CimArchive. Returns the archive.
        Args:
            selected_profiles (str): String with CGMES profiles to be generated, separeted by single spaces (e.g. 'ssh dl', 'tp'). 'all' selects all profiles.
        Returns:
            None
        """
        grid_to_cim_tool = self._create_grid_to_cim_tool()

        if selected_profiles == "all":
            grid_to_cim_tool.partial = 0  # convert all profiles
        else:
            grid_to_cim_tool.partial = 1  # convert selected profiles
            self._set_profiles_of_cim_tool(grid_to_cim_tool, self._all_profiles, False)
            self._set_profiles_of_cim_tool(grid_to_cim_tool, selected_profiles, True)

        grid_to_cim_tool.iopt_target = 1  # existing archive
        archive = self._create_archive(
            name="_".join(
                [self.export_archive_name, selected_profiles.replace(" ", "_")]
            )
        )
        grid_to_cim_tool.targetPath = archive
        grid_to_cim_tool.Execute()
        return archive


    def _set_attr_as_list_or_single(self, obj: PFGeneral, attr:str, val: Union[list, str, float]):
        """Some attributes need to be set wrapped inside lists in older PF versions, while they must not be lists in newer versions. 

        This function parses the value accordingly.

        Args:
            obj (PFGeneral): object
            attr (str): attribute to be set
            val (Union[list, str, float]): value to be set
        """        
        attr_is_list = isinstance(obj.GetAttribute(attr), list)
        val_is_list = isinstance(val, list)
        if attr_is_list and not val_is_list:
            val = [val]
        self.act_prj.set_attr(obj, {attr: val})


    def _convert_archive_to_file(self, archive, output_path: str, as_zip: bool = True):
        """Convert a PowerFactory .CimArchive object to a file. Returns None.
        Args:
            archive (PowerFactory .CimArchive object): archive to be converted and saved as a file.
            output_path (str): Path to desired output folder (without file name).
            as_zip (bool): save as .zip file if as_zip, else save as .xml files.

        Returns:
            None
        """
        archive = self.act_prj._handle_single_pf_object_or_path_input(archive)
        cim_export_tool = self.act_prj.create_in_folder(
            self.archive_to_file_tool_name + ".ComCimdbexp",
            self.act_prj.app.GetActiveStudyCase(),
            use_existing=True,
        )
        self._set_attr_as_list_or_single(cim_export_tool, "targetFolder", output_path)            
        if as_zip:
            cim_export_tool.zipModels = 0
            self._set_attr_as_list_or_single(cim_export_tool, "archiveName", self.exported_zip_name)
        else:
            cim_export_tool.zipModels = 2
        cim_export_tool.sourcePath = archive
        cim_export_tool.Execute()
        return None

    def cgmes_export(
        self, output_path: str, selected_profiles: str = "all", as_zip: bool = True
    ):
        """Exports selected CGMES profiles of active grid.
        Args:
            output_path (str): Path to desired output folder (without file name).
            selected_profiles (str): String with CGMES profiles to be exported, separeted by single spaces (e.g. 'ssh dl' or 'tp'). 'all' selects all profiles.
            as_zip (bool): save as .zip file if as_zip, else save as .xml files.

        Returns:
            None
        """
        print(
            "Info: The CGMES export can trigger error messages in the PowerFactory output window, but these do not usually affect the correctness of the exported data."
        )
        archive = self._convert_grid_to_archive(selected_profiles=selected_profiles)
        self._convert_archive_to_file(archive, output_path, as_zip=as_zip)
        return None
