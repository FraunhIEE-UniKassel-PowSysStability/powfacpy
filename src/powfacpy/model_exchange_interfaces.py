import sys
sys.path.insert(0, r'.\src')
import powfacpy
import numpy as np


class PFCgmesInterface(powfacpy.PFBaseInterface):
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
    cim_to_grid_tool = self.create_in_folder(self.app.GetActiveStudyCase(), self.ARCHIVE_TO_GRID_TOOL_NAME+'.ComCimtogrid', use_existing=True)
    return cim_to_grid_tool


  def _convert_file_to_archive(self, file_path, name):
    file_to_archive_tool = self.create_in_folder(self.app.GetActiveStudyCase(), 
                                            self.FILE_TO_ARCHIVE_TOOL_NAME+'.ComCimdbimp', 
                                            use_existing=True)
    file_to_archive_tool.iopt_target = 2
    cim_archive = self._create_cim_archive(name='_'.join([self.ARCHIVE_NAME, name]))
    file_to_archive_tool.targetPath = cim_archive
    file_to_archive_tool.fileName = file_path
    file_to_archive_tool.Execute()
    return cim_archive


  def _convert_archive_to_grid(self, cim_archive):
    # TODO this needs dependencies profiles, see luis code
    cim_to_grid_tool = self._create_cim_to_grid_tool()
    cim_to_grid_tool.sourcePath = cim_archive
    cim_to_grid_tool.dependencies = None
    cim_to_grid_tool.partial = 0
    # cim_to_grid_tool.pGrid = [grid] # TODO find out if grid has to be given
    cim_to_grid_tool.Execute()


  def cgmes_import(self, input_path):
    archive = self._convert_file_to_archive(input_path, 'imported')
    self._convert_archive_to_grid(archive)


  def update_profiles(self, update_file_path:str, base_archive):
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
    pass


  # Export functions

  def _create_grid_to_cim_tool(self):
    grid_to_cim_tool = self.create_in_folder(self.app.GetActiveStudyCase(), self.GRID_TO_ARCHIVE_TOOL_NAME+'.ComGridtocim', use_existing=True)
    grid_to_cim_tool.cAuthority = ['Authority1'] # TODO this probably isn't general
    grid_to_cim_tool.cSelected = [1] # TODO this probably isn't general (should all grids be selected? or actually only the first one?) --> get project with >1 grid and get to run properly
    grid_to_cim_tool.version = self.CGMES_VERSION
    return grid_to_cim_tool


  def _get_cim_archive_folder(self):
    cim_archive_folder = self.create_in_folder(self.app.GetActiveProject(), 
                                               self.ARCHIVE_FOLDER_NAME+'.IntPrjfolder', 
                                               use_existing=True, overwrite=False)
    cim_archive_folder.iopt_typ = 'cim'
    return cim_archive_folder
  

  def _create_cim_archive(self, name):
    cim_archive_folder = self._get_cim_archive_folder()
    cim_archive = self.create_in_folder(cim_archive_folder, 
                                        name+'.CIMArchive', 
                                        use_existing=False, overwrite=True)
    return cim_archive


  def _set_profiles_of_cim_tool(self, grid_to_cim_tool, profiles, state):
    for profile in profiles.split(' '):
      grid_to_cim_tool.SetAttribute('convert'+profile.upper(), state)


  def _convert_grid_to_archive(self, selected_profiles='all'):
    grid_to_cim_tool = self._create_grid_to_cim_tool()

    if selected_profiles == 'all':
      grid_to_cim_tool.partial = 0 # convert all profiles
    else:
      grid_to_cim_tool.partial = 1 # convert selected profiles
      self._set_profiles_of_cim_tool(grid_to_cim_tool, self._ALL_PROFILES, False)
      self._set_profiles_of_cim_tool(grid_to_cim_tool, selected_profiles, True)

    grid_to_cim_tool.iopt_target = 1 # existing archive
    cim_archive = self._create_cim_archive(name='_'.join([self.ARCHIVE_NAME, 'exported', selected_profiles.replace(' ', '_')]))
    grid_to_cim_tool.targetPath = cim_archive
    grid_to_cim_tool.Execute()
    return cim_archive


  def _convert_archive_to_file(self, cim_archive, output_path, as_zip=True):
    cim_export_tool = self.create_in_folder(self.app.GetActiveStudyCase(), 
                                            self.ARCHIVE_TO_FILE_TOOL_NAME+'.ComCimdbexp', 
                                            use_existing=True)
    cim_export_tool.targetFolder = [output_path]
    if as_zip:
      cim_export_tool.zipModels = 0
      cim_export_tool.archiveName = [self.EXPORTED_ZIP_NAME,]
    else:
      cim_export_tool.zipModels = 2
    cim_export_tool.sourcePath = cim_archive
    cim_export_tool.Execute()


  def cgmes_export(self, output_path, selected_profiles='all', as_zip=True):
    '''selected profiles can be given in a string, separated by single spaces, e.g. 'eq ssh sv'
    '''
    archive = self._convert_grid_to_archive(selected_profiles=selected_profiles)
    self._convert_archive_to_file(archive, output_path, as_zip=as_zip)


  # def cgmes_export_all_profiles_one_zip(self, CIM_archive, file_destination):
  #   self.CIM_export.zipModels = 0
  #   self.CIM_export.targetFolder = [file_destination]
  #   self.CIM_export.sourcePath = CIM_archive
  #   self.CIM_export.archiveName = ['All_profiles']
  #   self.CIM_export.Execute()

  # def cgmes_export_ssh_profile(self, CIM_archive, file_destination):
  #   SSH = CIM_archive.GetContents('*_SSH.CimModel')[0]
  #   self.CIM_export.zipModels = 2
  #   self.CIM_export.targetFolder = [file_destination]
  #   self.CIM_export.sourcePath = SSH
  #   self.CIM_export.Execute()