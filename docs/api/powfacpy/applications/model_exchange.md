Module powfacpy.applications.model_exchange
===========================================
This module provides an interface to import/export data in CGMES format.

Classes
-------

`CGMES(pf_app: powfacpy.pf_classes.protocols.PFApp | None | bool = False, cached: bool = False)`
:   Interface for CGMES integration in PowerFactory.

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Instance variables

    `archive_folder`
    :

    ### Methods

    `cgmes_export(self, output_path: str, selected_profiles: str = 'all', as_zip: bool = True)`
    :   Exports selected CGMES profiles of active grid.
        Args:
            output_path (str): Path to desired output folder (without file name).
            selected_profiles (str): String with CGMES profiles to be exported, separeted by single spaces (e.g. 'ssh dl' or 'tp'). 'all' selects all profiles.
            as_zip (bool): save as .zip file if as_zip, else save as .xml files.
        
        Returns:
            None

    `cgmes_import(self, input_path: str)`
    :   Converts CGMES .zip files to a PowerFactory grid.
        
        Args:
            input_path (str): Path to the CGMES .zip archive, containing xml profiles.
        
        Returns:
            None

    `update_profiles(self, update_file_path: str, base_archive: powfacpy.pf_classes.protocols.CimArchive | str)`
    :   Includes new SSH (and DL) profiles into an already imported grid.
        
        Args:
            update_file_path (str): Path to the CGMES .zip archive, containing profiles for updating (SSH and optionally DL).
            base_archive (CimArchive | str) Base .CimArchive which the already imported grid has been created from.
        
        Returns:
            None