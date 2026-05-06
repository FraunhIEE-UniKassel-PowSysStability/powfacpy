Module powfacpy.applications.networks
=====================================

Classes
-------

`Networks(pf_app: powfacpy.pf_classes.protocols.PFApp | None | bool = False, cached: bool = False)`
:   Class for interface with power system networks and their elements.

    ### Ancestors (in MRO)

    * powfacpy.applications.application_base.ApplicationBase

    ### Methods

    `copy_grid(self, grid_or_path, target_folder, new_name, parent_folder=None, error_if_non_existent=True, overwrite=True, use_existing=False)`
    :   Copying a grid is not trivial in PF because the graphical network objects need to be copied and assigned manually as this is not done automatically.

    `get_connected_terminal(self, element)`
    :

    `get_cubicles_of_terminal(self, terminal: powfacpy.pf_classes.protocols.ElmTerm, only_calc_relevant=False) ‑> list[powfacpy.pf_classes.protocols.StaCubic]`
    :

    `get_elements_connected_to_terminal(self, terminal, only_calc_relevant: bool = False)`
    :

    `get_parent_grid(self, obj_or_path)`
    :

    `get_vacant_cubicle_of_terminal(self, terminal, new_cubicle_name=None) ‑> powfacpy.pf_classes.protocols.StaCubic`
    :   Gets the first vacant cubicle found in a terminal (i.e. nothing is connected
        to this cubicle).
        If there is no vacant cubicle, a new cubicle is created.
        
        Arguments:
          terminal: ElmTerm
          new_cubicle_name: Name  that is set for the found or created cubicle