from __future__ import annotations

from typing import Callable

from icecream import ic

import powfacpy.pf_classes.elm.boundary
from powfacpy.pf_classes.elm.term import Terminal
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
                boundary = powfacpy.pf_classes.elm.boundary.Boundary(boundary)
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
                boundary = powfacpy.pf_classes.elm.boundary.Boundary(boundary)
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

    def create_boundary_from_bus_branch(
        self,
        name: str,
        bus_branch: dict,
        to_branch: bool = True,
        color: int = 2,
        parent_folder: str | PFGeneral = None,
        overwrite: bool = True,
    ) -> ElmBoundary:
        """Create a boundary by specifying buses (terminals) and branches (connected to the buses).

        Args:
            name (str): name of boundary

            bus_branch (dict): keys are the buses (terminals) as path strings or PF objects. Values are a list of one or more branch elements (e.g. lines) as path strings or PF objects which are connected with the bus.

            to_branch (bool, optional): Direction of boundary is towards branch (or towards terminal). Defaults to True.

            color (int, optional): Color of boundary shown in single line diagram. Defaults to 2.

            parent_folder (PFGeneral | str | None, optional): Parent folder where boundary is created. Defaults to None (i.e. default boundary folder).

            overwrite (bool, optional): Overwrite existing boundary with same name. Defaults to True.

        Returns:
            ElmBoundary: The boundary created.
        """
        if to_branch:
            to_branch = 0
        else:
            to_branch = 1
        if parent_folder is None:
            parent_folder = self.act_prj.boundaries_folder
        boundary = self.act_prj.create_in_folder(
            name + ".ElmBoundary", parent_folder, overwrite=overwrite
        )
        for term, branches in bus_branch.items():
            term = Terminal(self.act_prj._handle_single_pf_object_or_path_input(term))
            for branch in branches:
                branch = self.act_prj._handle_single_pf_object_or_path_input(branch)
                cub = term.get_cubicle_of_connected_elm(branch)
                boundary.AddCubicle(cub, to_branch)
        boundary.icolor = color
        return boundary

    def create_zone_from_boundary_bus_branch(
        self,
        name: str,
        bus_branch: dict,
        to_branch: bool = True,
        color: int = 2,
        parent_folder: str | PFGeneral = None,
        overwrite: bool = True,
    ) -> ElmZone:
        """Create a zone via intermediate boundary and by specifying buses (terminals) and branches (connected to the buses).

        Args:
            name (str): name of zone

            bus_branch (dict): keys are the buses (terminals) as path strings or PF objects. Values are a list of one or more branch elements (e.g. lines) as path strings or PF objects which are connected with the bus.

            to_branch (bool, optional): Direction of boundary is towards branch (or towards terminal). Defaults to True.

            color (int, optional): Color of boundary shown in single line diagram. Defaults to 2.

            parent_folder (PFGeneral | str | None, optional): Parent folder where zone is created. Defaults to None (i.e. default zone folder).

            overwrite (bool, optional): Overwrite existing boundary with same name. Defaults to True.
        Returns:
            ElmZone: _description_
        """
        boundary = powfacpy.pf_classes.elm.boundary.Boundary(
            self.create_boundary_from_bus_branch(
                name, bus_branch, to_branch=to_branch, overwrite=False
            )
        )
        zone = boundary.create_zone(
            name, parent_folder, color=color, overwrite=overwrite
        )
        boundary._obj.Delete()
        return zone
