import sys
sys.path.insert(0, r'.\src')
import powfacpy
import numpy as np

class PFCgmesInterface(powfacpy.PFBaseInterface):
  """Interface for CGMES integration in PowerFactory."""
  def __init__(self, app):
    super().__init__(app)
    self.ARCHIVE_NAME = 'cgmes_archive'
    self.ARCHIVE_FOLDER_NAME = 'cgmes_archive_folder'
    self.FILE_TO_ARCHIVE_TOOL_NAME = 'cgmes_file_to_archive'
    self.ARCHIVE_TO_FILE_TOOL_NAME = 'cgmes_archive_to_file'
    self.ARCHIVE_TO_GRID_TOOL_NAME = 'cgmes_archive_to_grid'
    self.GRID_TO_ARCHIVE_TOOL_NAME = 'cgmes_grid_to_archive'
    self.EXPORTED_ZIP_NAME = 'cgmes_profiles'
    self.CGMES_VERSION = 'CGMES 3.0.0'
    self._ALL_PROFILES = 'eq tp ssh sc sv dy dl gl'
  
  # Import functions TODO

  def _create_cim_to_grid_tool(self):
    """Returns the CIM to Grid tool object .ComCimtogrid."""
    cim_to_grid_tool = self.create_in_folder(self.app.GetActiveStudyCase(), self.ARCHIVE_TO_GRID_TOOL_NAME+'.ComCimtogrid', use_existing=True)
    return cim_to_grid_tool


  def _convert_file_to_archive(self, file_path, name):
    """Convert a .zip file to a PowerFactory .CimArchive object. Returns the .CimArchive object."""
    file_to_archive_tool = self.create_in_folder(self.app.GetActiveStudyCase(), 
                                            self.FILE_TO_ARCHIVE_TOOL_NAME+'.ComCimdbimp', 
                                            use_existing=True)
    file_to_archive_tool.iopt_target = 2
    archive = self._create_archive(name='_'.join([self.ARCHIVE_NAME, name]))
    file_to_archive_tool.targetPath = archive
    file_to_archive_tool.fileName = file_path
    file_to_archive_tool.Execute()
    return archive


  def _convert_archive_to_grid(self, cim_archive):
    """Convert a PowerFactory .CimArchive to a grid. Returns None."""
    cim_to_grid_tool = self._create_cim_to_grid_tool()
    cim_to_grid_tool.sourcePath = cim_archive
    cim_to_grid_tool.dependencies = None
    cim_to_grid_tool.partial = 0
    # cim_to_grid_tool.pGrid = [grid] # TODO find out if grid has to be given
    cim_to_grid_tool.Execute()
    return None
  

  def cgmes_import(self, input_path:str):
    """Converts CGMES .zip files to a PowerFactory grid. 

        Args:
            input_path (str): Path to the CGMES .zip archive, containing xml profiles.

        Returns:
            None
        """
    archive = self._convert_file_to_archive(input_path, 'imported')
    self._convert_archive_to_grid(archive)
    return None


  def update_profiles(self, update_file_path:str, base_archive):
    """Includes new SSH (and DL) profiles into an already imported grid. 

        Args:
            update_file_path (str): Path to the CGMES .zip archive, containing profiles for updating (SSH and optionally DL).
            base_archive (PowerFactory.DataObject|str) Base .CimArchive which the already imported grid has been created from.  
            
        Returns:
            None
        """
    base_archive = self.handle_single_pf_object_or_path_input(base_archive)
    update_profiles_archive = self._convert_file_to_archive(update_file_path, 'imported_profiles_for_update')
    cim_to_grid_tool = self._create_cim_to_grid_tool()
    cim_to_grid_tool.sourcePath = update_profiles_archive
    cim_to_grid_tool.dependencies = base_archive
    cim_to_grid_tool.partial = 1
    profiles_in_update_file = [file.loc_name.split('_')[-2] for file in update_profiles_archive.GetContents()]
    self._set_profiles_of_cim_tool(cim_to_grid_tool, self._ALL_PROFILES, False)
    self._set_profiles_of_cim_tool(cim_to_grid_tool, ' '.join(profiles_in_update_file), True)
    # cim_to_grid_tool.pGrid = [grid] # TODO find out if grid has to be given
    cim_to_grid_tool.Execute()
    return None


  # Export functions

  def _create_grid_to_cim_tool(self):
    """Returns the Grid to CIM tool object .ComGridtocim."""
    grid_to_cim_tool = self.create_in_folder(self.app.GetActiveStudyCase(), self.GRID_TO_ARCHIVE_TOOL_NAME+'.ComGridtocim', use_existing=True)
    grid_to_cim_tool.cAuthority = ['Authority1'] # TODO this probably isn't general
    grid_to_cim_tool.cSelected = [1] # TODO this probably isn't general (should all grids be selected? or actually only the first one?) --> get project with >1 grid and get to run properly
    grid_to_cim_tool.version = self.CGMES_VERSION
    return grid_to_cim_tool


  def _get_archive_folder(self):
    """Get or create the folder for PowerFactory .CimArchive objects. Returns the folder."""
    archive_folder = self.create_in_folder(self.app.GetActiveProject(), 
                                               self.ARCHIVE_FOLDER_NAME+'.IntPrjfolder', 
                                               use_existing=True, overwrite=False)
    archive_folder.iopt_typ = 'cim'
    return archive_folder
  

  def _create_archive(self, name):
    """Create a PowerFactory .CimArchive object. Returns the .CimArchive object."""
    archive_folder = self._get_archive_folder()
    archive = self.create_in_folder(archive_folder, 
                                        name+'.CimArchive', 
                                        use_existing=False, overwrite=True)
    return archive


  def _set_profiles_of_cim_tool(self, cim_tool, profiles:str, state:bool):
    """Sets the profiles of PowerFactory .ComCimtogrid or .ComGridtocim tools listet in profiles to state.
    Args:
        cim_tool (str): .ComCimtogrid or .ComGridtocim tool.
        profiles (str): String of CGMES profiles to be set in the tool, separeted by single spaces (e.g. 'ssh dl').
        state (bool): State to set the selected prfiles to (True=checked, False=unchecked).
    Returns:
        None
    """
    cim_tool = self.handle_single_pf_object_or_path_input(cim_tool)
    for profile in profiles.split(' '):
      cim_tool.SetAttribute('convert'+profile.upper(), state)
    return None


  def _convert_grid_to_archive(self, selected_profiles:str='all'):
    """Convert a PowerFactory grid to a .CimArchive. Returns the archive.
    Args:
        selected_profiles (str): String with CGMES profiles to be generated, separeted by single spaces (e.g. 'ssh dl', 'tp'). 'all' selects all profiles.
    Returns:
        None
    """
    grid_to_cim_tool = self._create_grid_to_cim_tool()

    if selected_profiles == 'all':
      grid_to_cim_tool.partial = 0 # convert all profiles
    else:
      grid_to_cim_tool.partial = 1 # convert selected profiles
      self._set_profiles_of_cim_tool(grid_to_cim_tool, self._ALL_PROFILES, False)
      self._set_profiles_of_cim_tool(grid_to_cim_tool, selected_profiles, True)

    grid_to_cim_tool.iopt_target = 1 # existing archive
    archive = self._create_archive(name='_'.join([self.ARCHIVE_NAME, 'exported', selected_profiles.replace(' ', '_')]))
    grid_to_cim_tool.targetPath = archive
    grid_to_cim_tool.Execute()
    return archive


  def _convert_archive_to_file(self, archive, output_path:str, as_zip:bool=True):
    """Convert a PowerFactory .CimArchive object to a file. Returns None.
    Args:
        archive (PowerFactory .CimArchive object): archive to be converted and saved as a file.
        output_path (str): Path to desired output folder (without file name).
        as_zip (bool): save as .zip file if as_zip, else save as .xml files.
    
    Returns:
        None
    """
    archive = self.handle_single_pf_object_or_path_input(archive)
    cim_export_tool = self.create_in_folder(self.app.GetActiveStudyCase(), 
                                            self.ARCHIVE_TO_FILE_TOOL_NAME+'.ComCimdbexp', 
                                            use_existing=True)
    cim_export_tool.targetFolder = [output_path]
    if as_zip:
      cim_export_tool.zipModels = 0
      cim_export_tool.archiveName = [self.EXPORTED_ZIP_NAME,]
    else:
      cim_export_tool.zipModels = 2
    cim_export_tool.sourcePath = archive
    cim_export_tool.Execute()
    return None


  def cgmes_export(self, output_path:str, selected_profiles:str='all', as_zip:bool=True):
    """Exports selected CGMES profiles of active grid.
    Args:
        output_path (str): Path to desired output folder (without file name).
        selected_profiles (str): String with CGMES profiles to be exported, separeted by single spaces (e.g. 'ssh dl', 'tp'). 'all' selects all profiles.
        as_zip (bool): save as .zip file if as_zip, else save as .xml files.
    
    Returns:
        None
    """
    archive = self._convert_grid_to_archive(selected_profiles=selected_profiles)
    self._convert_archive_to_file(archive, output_path, as_zip=as_zip)
    return None
  