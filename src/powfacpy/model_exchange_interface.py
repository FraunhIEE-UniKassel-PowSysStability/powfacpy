import sys
sys.path.insert(0, r'.\src')
import powfacpy
import numpy as np


class PFModelExchangeInterface(powfacpy.PFBaseInterface):
  def __init__(self, app):
    super().__init__(app)


  def _cgmes_import_profiles(self, file_name, CGMES_ARCHIVE_NAME='cgmes_profiles'):
     cim_import = self.create_in_folder(
        self.app.GetActiveStudyCase(), 
        'cim_import.ComCimdbimp', 
        use_existing=True, overwrite=False)
     cim_import.iopt_target = 1
     cim_import.targetName = CGMES_ARCHIVE_NAME
     cim_import.fileName = file_name
     cim_import.Execute()

     cim_folder = self.get_unique_obj('CIM Model.IntPrjfolder')
     return self.get_unique_obj(
        CGMES_ARCHIVE_NAME+'.CimArchive', parent_folder=cim_folder)


  def _cgmes_convert_profiles_to_grid_model(self, cgmes_profiles):
    cim_to_grid = self.create_in_folder(
      self.app.GetActiveStudyCase(), 
      'cim_to_grid.ComCimtogrid', 
      use_existing=True, overwrite=False)
    cim_to_grid.sourcePath = cgmes_profiles
    cim_to_grid.partial = 1
    cim_to_grid.convertEQ = 1
    cim_to_grid.convertTP = 1
    cim_to_grid.convertSSH = 1
    cim_to_grid.convertSV = 0
    cim_to_grid.Execute()


  def cgmes_import(self, file_name):
    profiles = self._import_cgmes_profiles(file_name)
    self._cgmes_convert_profiles_to_grid_model(profiles)


  # Export functions

  def _create_grid_to_cim_tool(self):
    grid_to_cim_tool = self.create_in_folder(self.app.GetActiveStudyCase(), 'grid_to_cim.ComGridtocim', use_existing=True)
    grid_to_cim_tool.cAuthority = ['Authority1'] # TODO this probably isn't general
    grid_to_cim_tool.cSelected = [1] # TODO this probably isn't general
    grid_to_cim_tool.version = 'CGMES 3.0.0'
    return grid_to_cim_tool


  def _create_cim_archive(self):
    cim_archive_folder = self.create_in_folder(self.app.GetActiveProject(), 'cim_model.IntPrjfolder', use_existing=True, overwrite=False)
    cim_archive_folder.iopt_typ = 'cim'
    cim_archive = self.create_in_folder(cim_archive_folder, 'cim_archive.CIMArchive', use_existing=False, overwrite=True)
    return cim_archive


  def _cgmes_convert_grid_to_archive(self, selected_profiles='all'):
    grid_to_cim_tool = self._create_grid_to_cim_tool()

    def set_profiles(grid_to_cim_tool, profiles, state):
      for profile in profiles.split(' '):
        grid_to_cim_tool.SetAttribute('convert'+profile.upper(), state)

    if selected_profiles == 'all':
      grid_to_cim_tool.partial = 0 # convert all profiles
    else:
      grid_to_cim_tool.partial = 1 # convert selected profiles
      ALL_PROFILES = 'eq tp ssh sc sv dy dl gl'
      set_profiles(grid_to_cim_tool, ALL_PROFILES, False)
      set_profiles(grid_to_cim_tool, selected_profiles, True)

    grid_to_cim_tool.iopt_target = 1 # existing archive
    cim_archive = self._create_cim_archive()
    grid_to_cim_tool.targetPath = cim_archive
    grid_to_cim_tool.Execute()
    return cim_archive


  def _cgmes_convert_archive_to_file(self, cim_archive, output_path, as_zip=True):
    cim_export_tool = self.create_in_folder(self.app.GetActiveStudyCase(), 'cim_export.ComCimdbexp', use_existing=True)
    cim_export_tool.targetFolder = [output_path]
    if as_zip:
      cim_export_tool.zipModels = 0
      cim_export_tool.archiveName = ['cgmes_profiles']
    else:
      cim_export_tool.zipModels = 2
    cim_export_tool.sourcePath = cim_archive
    cim_export_tool.Execute()


  def cgmes_export(self, output_path, selected_profiles='all', as_zip=True):
    '''selected profiles can be given in a string, separated by single spaces, e.g. 'eq ssh sv'
    '''
    archive = self._cgmes_convert_grid_to_archive(selected_profiles=selected_profiles)
    self._cgmes_convert_archive_to_file(archive, output_path, as_zip=as_zip)


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