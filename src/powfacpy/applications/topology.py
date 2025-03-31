from typing import Callable

from icecream import ic

from powfacpy.pf_classes.elm.boundary import Boundary
from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_classes.protocols import (
    PFApp,
    PFGeneral,
    ElmZone,
    ElmBoundary,
    ElmArea,
)


class Topology(ApplicationBase):

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)

    def create_zone(
        self,
        name: str,
        elms: list[PFGeneral],
        color: int = 2,
        parent_folder: str | PFGeneral = None,
        overwrite: bool = True,
    ) -> ElmZone:
        if not parent_folder:
            parent_folder = self.act_prj.zones_folder
        zone: ElmZone = self.act_prj.create_in_folder(
            name + ".ElmZone", parent_folder, overwrite=overwrite
        )

        zone.icolor = color
        for elm in elms:
            elm.cpZone = zone
        return zone

    def create_area(
        self,
        name: str,
        elms: list[PFGeneral],
        color: int = 2,
        parent_folder: str | PFGeneral = None,
        overwrite: bool = True,
    ) -> ElmZone:
        if not parent_folder:
            parent_folder = self.act_prj.areas_folder
        area: ElmArea = self.act_prj.create_in_folder(
            name + ".ElmArea", parent_folder, overwrite=overwrite
        )

        area.icolor = color
        for elm in elms:
            elm.cpArea = area
        return area

    def create_boundary_using_intermediate_zone(
        self,
        name: str,
        elms: list[PFGeneral],
        exclude_node_elms: Callable | None = None,
        color: int = 2,
        parent_folder: PFGeneral | str | None = None,
        overwrite: bool = True,
    ) -> ElmBoundary:
        """Create boundary (ElmBoundary) that includes 'elms'. A zone is created as an intermediate step.

        Warning: If there are existing zones in the network model those might be changed if 'elms' are included (because elements can only be part of one zone). To avoid this use 'create_boundary_without_changing_initial_zones' instead.

        Args:
            name (str): Name of boundary created

            elms (list[PFGeneral]): Network elements contained in boundary
            exclude_node_elms (Callable | None, optional): Condition to select elements to be excluded from the interior (e.g. `lambda x: x.GetClassName() == "ElmLod" to exclude all ElmLod). Defaults to None.

            color (int, optional): Color of boundary shown in single line diagram. Defaults to 2.

            parent_folder (PFGeneral | str | None, optional): PArent folder where boundary is created. Defaults to None (i.e. default boundary folder).

            overwrite (bool, optional): Overwrite existing boundary with same name. Defaults to True.

        Returns:
            ElmBoundary: Boundary object created.
        """
        if parent_folder:
            parent_folder = self.act_prj._handle_single_pf_object_or_path_input(
                parent_folder
            )
        else:
            parent_folder = self.act_prj.boundaries_folder
        dummy_zone = self.create_zone(name, elms)
        try:
            if overwrite:
                self.act_prj.delete_obj(
                    name, parent_folder=parent_folder, error_if_non_existent=False
                )
            boundary: ElmBoundary = dummy_zone.DefineBoundary(0)
            if parent_folder:
                parent_folder.Move(boundary)
            if exclude_node_elms:
                boundary = Boundary(boundary)
                boundary.exclude_node_elms_by_condition(exclude_node_elms)
                boundary = boundary._obj
            boundary.icolor = color
        finally:
            dummy_zone.Delete()
        return boundary

    def create_boundary_without_changing_initial_zones(
        self,
        name: str,
        elms: list[PFGeneral],
        exclude_node_elms: Callable | None = None,
        color: int = 2,
        parent_folder: PFGeneral | str | None = None,
        overwrite: bool = True,
    ) -> ElmBoundary:
        """Create boundary (ElmBoundary) that includes 'elms'. A zone is created as an intermediate step.

        In comparison to 'create_boundary_using_intermediate_zone', this methods avoids altering existing zones by creating an intermediate variation.

        Args:
            name (str): Name of boundary created

            elms (list[PFGeneral]): Network elements contained in boundary
            exclude_node_elms (Callable | None, optional): Condition to select elements to be excluded from the interior (e.g. `lambda x: x.GetClassName() == "ElmLod" to exclude all ElmLod). Defaults to None.

            color (int, optional): Color of boundary shown in single line diagram. Defaults to 2.

            parent_folder (PFGeneral | str | None, optional): PArent folder where boundary is created. Defaults to None (i.e. default boundary folder).

            overwrite (bool, optional): Overwrite existing boundary with same name. Defaults to True.

        Returns:
            ElmBoundary: Boundary object created.
        """
        if parent_folder:
            parent_folder = self.act_prj._handle_single_pf_object_or_path_input(
                parent_folder
            )
        else:
            parent_folder = self.act_prj.boundaries_folder
        variation = self.act_prj.create_variation("dummy")
        dummy_zone: ElmZone = self.create_zone("dummy", elms)
        try:
            if overwrite:
                self.act_prj.delete_obj(
                    name, parent_folder=parent_folder, error_if_non_existent=False
                )
            boundary: ElmBoundary = dummy_zone.DefineBoundary(0)
            if exclude_node_elms:
                boundary = Boundary(boundary)
                boundary.exclude_node_elms_by_condition(exclude_node_elms)
            cubicles = boundary.cubicles
            orientations = boundary.ciorient
        finally:
            variation.Deactivate()
            variation.Delete()
            boundary = self.act_prj.create_in_folder(
                name + ".ElmBoundary", folder=parent_folder
            )
            for cub, orientation in zip(cubicles, orientations):
                boundary.AddCubicle(cub, orientation)
            boundary.icolor = color
            if parent_folder:
                parent_folder.Move(boundary)
        return boundary
