from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_class_protocols import PFApp, StaCubic
from powfacpy.pf_classes.protocols import ElmTerm


class Networks(ApplicationBase):
    """Class for interface with power system networks and their elements."""

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)

    def get_vacant_cubicle_of_terminal(
        self, terminal, new_cubicle_name=None
    ) -> StaCubic:
        """Gets the first vacant cubicle found in a terminal (i.e. nothing is connected
        to this cubicle).
        If there is no vacant cubicle, a new cubicle is created.

        Arguments:
          terminal: ElmTerm
          new_cubicle_name: Name  that is set for the found or created cubicle
        """
        terminal = self.act_prj._handle_single_pf_object_or_path_input(terminal)
        cubicles = self.get_cubicles_of_terminal(terminal)
        for cubicle in cubicles:
            if cubicle.obj_id == None:
                if new_cubicle_name:
                    cubicle.loc_name = new_cubicle_name
                return cubicle
        if not new_cubicle_name:
            cubicle_already_exists = True
            cub_num = len(cubicles) + 1
            while cubicle_already_exists is not None:
                new_cubicle_name = "Cub_" + str(cub_num)
                cubicle_already_exists = self.act_prj.get_unique_obj(
                    new_cubicle_name,
                    parent_folder=terminal,
                    error_if_non_existent=False,
                )
                cub_num += 1
        return self.act_prj.create_in_folder(
            new_cubicle_name + ".StaCubic", terminal, overwrite=False
        )

    def get_cubicles_of_terminal(
        self, terminal: ElmTerm, only_calc_relevant=False
    ) -> list[StaCubic]:
        if not only_calc_relevant:
            # GetConnectedCubicles() does not return vacant cubicles so it cannot cannot be used to get all cubicles
            return self.act_prj.get_obj(
                "*",
                parent_folder=terminal,
                condition=lambda x: x.GetClassName() == "StaCubic",
                error_if_non_existent=False,
            )
        else:
            return terminal.GetCalcRelevantCubicles()

    def get_elements_connected_to_terminal(
        self, terminal, only_calc_relevant: bool = False
    ):
        cubicles = self.get_cubicles_of_terminal(
            terminal, only_calc_relevant=only_calc_relevant
        )
        elements = []
        for cub in cubicles:
            if cub.obj_id is not None:
                elements.append(cub.obj_id)
        return elements

    def get_connected_terminal(self, element):
        return element.bus1.cterm

    def copy_grid(
        self,
        grid_or_path,
        target_folder,
        new_name,
        parent_folder=None,
        error_if_non_existent=True,
        overwrite=True,
        use_existing=False,
    ):
        """Copying a grid is not trivial in PF because the graphical network objects need to be copied and assigned manually as this is not done automatically."""
        grid_to_be_copied = self.act_prj._handle_single_pf_object_or_path_input(
            grid_or_path
        )
        new_grid = self.act_prj.copy_single_obj(
            grid_to_be_copied,
            target_folder,
            overwrite=overwrite,
            use_existing=use_existing,
            new_name=new_name,
            parent_folder=parent_folder,
            error_if_non_existent=error_if_non_existent,
        )
        new_network_diagram = self.act_prj.copy_single_obj(
            grid_to_be_copied.pDiagram,
            self.act_prj.app.GetProjectFolder("dia"),
            new_name=new_name,
            overwrite=overwrite,
            use_existing=use_existing,
        )
        graphical_net_objects = self.act_prj.get_obj(
            "*.IntGrf", parent_folder=new_network_diagram, include_subfolders=True
        )
        for graphical_net_obj in graphical_net_objects:
            element = graphical_net_obj.pDataObj
            path_in_grid = self.act_prj.get_path_between_objects(
                grid_to_be_copied, element
            )
            graphical_net_obj.pDataObj = self.act_prj.get_unique_obj(
                path_in_grid, parent_folder=new_grid
            )
        new_network_diagram.pDataFolder = new_grid
        new_grid.pDiagram = new_network_diagram
        return new_grid

    def get_parent_grid(self, obj_or_path):
        obj_or_path = self.act_prj._handle_single_pf_object_or_path_input(obj_or_path)
        return self.act_prj.get_upstream_obj(
            obj_or_path, lambda x: x.GetClassName() == "ElmNet"
        )
