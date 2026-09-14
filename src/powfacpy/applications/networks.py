from __future__ import annotations

from typing import Callable, Iterable
from warnings import warn

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.exceptions import PFInterfaceError
from powfacpy.pf_classes.protocols import ElmNet, ElmTerm, PFApp, PFGeneral, StaCubic

#: every connection attribute a branch element may carry (checked with HasAttribute)
_BRANCH_BUS_ATTRIBUTES: tuple[str, ...] = ("bus1", "bus2", "bushv", "busmv", "buslv")


class Networks(ApplicationBase):
    """Class for interface with power system networks and their elements."""

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        """Args:
        pf_app: the PowerFactory application. ``False`` (default) reuses the
            process-wide application, ``None`` fetches a fresh one, or pass an
            application object directly.
        cached: use the cached `ActiveProject` accessor.
        """
        super().__init__(pf_app, cached)

    def get_vacant_cubicle_of_terminal(
        self,
        terminal: ElmTerm | str,
        new_cubicle_name: str | None = None,
    ) -> StaCubic:
        """Return a free cubicle (`StaCubic`) of a terminal, creating one if needed.

        The first cubicle whose `obj_id` is ``None`` (nothing connected) is
        returned. If every cubicle is occupied a new one is created; its name is
        `new_cubicle_name`, or ``Cub_<n>`` with the lowest free ``n``.

        Args:
            terminal: the `ElmTerm` (or its path) to search.
            new_cubicle_name: name to set on the found or created cubicle
                (default: keep the existing name / auto-name a new one).

        Returns:
            StaCubic: the vacant cubicle.
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
        self, terminal: ElmTerm | str, only_calc_relevant: bool = False
    ) -> list[StaCubic]:
        """Return the cubicles (`StaCubic`) of a terminal.

        Args:
            terminal: the `ElmTerm` (or its path).
            only_calc_relevant: if True, return only calculation-relevant
                cubicles (`GetCalcRelevantCubicles`). If False (default), return
                every cubicle including vacant ones - `GetConnectedCubicles`
                omits vacant cubicles, so a direct child lookup is used instead.

        Returns:
            list[StaCubic]: the cubicles.
        """
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
        self, terminal: ElmTerm | str, only_calc_relevant: bool = False
    ) -> list[PFGeneral]:
        """Return the network elements connected to a terminal (via its cubicles).

        Args:
            terminal: the `ElmTerm` (or its path).
            only_calc_relevant: passed to `get_cubicles_of_terminal`.

        Returns:
            list[PFGeneral]: the connected elements (`obj_id` of the occupied
            cubicles).
        """
        cubicles = self.get_cubicles_of_terminal(
            terminal, only_calc_relevant=only_calc_relevant
        )
        elements = []
        for cub in cubicles:
            if cub.obj_id is not None:
                elements.append(cub.obj_id)
        return elements

    def get_connected_terminal(self, element: PFGeneral) -> ElmTerm:
        """Return the terminal a single-port element is connected to (its `bus1.cterm`).

        Args:
            element: a network element with a `bus1` attribute (`ElmSym`,
                `ElmGenstat`, `ElmLod`, ...).

        Returns:
            ElmTerm: the connected terminal.
        """
        return element.bus1.cterm

    def copy_grid(
        self,
        grid_or_path: ElmNet | str,
        target_folder: PFGeneral | str,
        new_name: str,
        parent_folder: PFGeneral | str | None = None,
        error_if_non_existent: bool = True,
        overwrite: bool = True,
        use_existing: bool = False,
        copy_diagram: bool = True,
        deactivate: bool = False,
    ) -> ElmNet:
        """Copy a grid (`ElmNet`), and by default its single-line diagram too.

        PowerFactory does not do this cleanly on its own:

        - ``AddCopy`` silently does nothing when the source grid is **active**.
          If the first attempt returns nothing, the active study case is briefly
          deactivated for a retry and reactivated afterwards (deactivating the
          *case*, not the grid - toggling an individual grid corrupts the RMS
          calculation state for the rest of the session).
        - the element ``bus1`` / ``bus2`` *views* only exist while a grid is
          active (the connections themselves are stored on the cubicles). The
          copy is therefore always **activated once and flushed** so PowerFactory builds and commits its topology; pass ``deactivate=True`` to switch it back off afterwards.
        - the diagram (`IntGrfnet`) is not copied with the grid, and its
          graphical objects (`IntGrf`) keep pointing at the *original*
          elements; this method copies the diagram and re-points them at the
          copied elements.

        Graphical objects that cannot be re-pointed - decorations without a
        data object, and elements that live in an active variation rather than
        in the grid itself - are left untouched and counted in a warning.

        Args:
            grid_or_path: the `ElmNet` to copy (or its path).
            target_folder: folder for the copied grid.
            new_name: `loc_name` of the copy (also used for the copied diagram).
            parent_folder: folder a string `grid_or_path` is resolved against.
            error_if_non_existent: passed to the object lookup.
            overwrite: overwrite an existing grid / diagram of the same name.
            use_existing: return an existing copy instead of making a new one.
            copy_diagram: also copy and re-link the single-line diagram.
            deactivate: deactivate the copy again after the mandatory
                activate-and-flush (default: leave it active).

        Returns:
            ElmNet: the copied grid.
        """
        grid_to_be_copied = self.act_prj._handle_single_pf_object_or_path_input(
            grid_or_path
        )
        target_folder = self.act_prj._handle_single_pf_object_or_path_input(
            target_folder
        )
        if use_existing:
            existing = self.act_prj.get_unique_obj(
                f"{new_name}.ElmNet",
                parent_folder=target_folder,
                error_if_non_existent=False,
            )
            if existing is not None:
                return existing
        new_grid = self._copy_grid_object(
            grid_to_be_copied,
            target_folder,
            new_name,
            parent_folder=parent_folder,
            error_if_non_existent=error_if_non_existent,
            overwrite=overwrite,
            use_existing=use_existing,
        )
        source_diagram = grid_to_be_copied.pDiagram
        if copy_diagram and source_diagram is not None:
            # `new_grid` is always freshly copied at this point (a reused grid
            # returned early above), so it needs a fresh diagram: `use_existing`
            # here would re-link it to a stale, possibly empty `IntGrfnet` left
            # in the diagrams folder by an earlier run.
            self._copy_and_relink_diagram(
                grid_to_be_copied,
                new_grid,
                source_diagram,
                new_name,
                overwrite=True,
                use_existing=False,
            )
        # always activate once + flush so PowerFactory builds the copy's topology
        # and commits it; the element ``bus1`` / ``bus2`` views only exist while
        # a grid is active (the connections themselves are stored on the cubicles)
        new_grid.Activate()
        self.act_prj.app.WriteChangesToDb()
        if deactivate:
            new_grid.Deactivate()
        return new_grid

    def _copy_grid_object(
        self,
        grid: ElmNet,
        target_folder: PFGeneral,
        new_name: str,
        *,
        parent_folder: PFGeneral | str | None,
        error_if_non_existent: bool,
        overwrite: bool,
        use_existing: bool,
    ) -> ElmNet:
        """Copy just the `ElmNet` object (no diagram).

        `AddCopy` returns nothing when the source grid is active; if that
        happens the active study case is deactivated for one retry and
        reactivated afterwards (never the grid itself - see `copy_grid`).

        Raises:
            PFInterfaceError: if the copy fails even with the study case off, or
                there is no active study case to deactivate for the retry.
        """

        def _copy() -> ElmNet | None:
            return self.act_prj.copy_single_obj(
                grid,
                target_folder,
                overwrite=overwrite,
                use_existing=use_existing,
                new_name=new_name,
                parent_folder=parent_folder,
                error_if_non_existent=error_if_non_existent,
            )

        new_grid = _copy()
        if new_grid is not None:
            return new_grid
        # AddCopy no-ops on an active grid -> retry with the study case off
        active_case = self.act_prj.app.GetActiveStudyCase()
        if active_case is None:
            raise PFInterfaceError(
                f"copying grid '{grid.loc_name}' failed and there is no active "
                "study case to deactivate for a retry."
            )
        active_case.Deactivate()
        try:
            new_grid = _copy()
        finally:
            active_case.Activate()
        if new_grid is None:
            raise PFInterfaceError(
                f"copying grid '{grid.loc_name}' failed even with the study "
                "case deactivated."
            )
        return new_grid

    def _copy_and_relink_diagram(
        self,
        source_grid: ElmNet,
        new_grid: ElmNet,
        source_diagram: PFGeneral,
        new_name: str,
        *,
        overwrite: bool,
        use_existing: bool,
    ) -> PFGeneral:
        """Copy the single-line diagram (`IntGrfnet`) of a grid and re-point its
        graphical objects (`IntGrf`) from the source elements to the copied ones.

        Graphical objects that cannot be re-pointed (decorations without a data
        object, elements added by an active variation) are left untouched and
        reported in a `RuntimeWarning`. The new diagram is cross-linked with
        `new_grid` (`pDataFolder` / `pDiagram`).

        Returns:
            PFGeneral: the copied `IntGrfnet`.
        """
        new_diagram = self.act_prj.copy_single_obj(
            source_diagram,
            source_diagram.GetParent(),
            new_name=new_name,
            overwrite=overwrite,
            use_existing=use_existing,
        )
        unresolved = 0
        for graphical_object in self.act_prj.get_obj(
            "*.IntGrf",
            parent_folder=new_diagram,
            include_subfolders=True,
            error_if_non_existent=False,
        ):
            element = graphical_object.pDataObj
            inside = element is not None and element.GetFullName().startswith(
                source_grid.GetFullName() + "\\"
            )
            if not inside:
                unresolved += element is not None
                continue
            path_in_grid = self._path_inside_grid(source_grid, element)
            copied_element = self.act_prj.get_unique_obj(
                path_in_grid, parent_folder=new_grid, error_if_non_existent=False
            )
            if copied_element is not None:
                graphical_object.pDataObj = copied_element
            else:
                unresolved += 1
        if unresolved:
            warn(
                f"copy_grid: {unresolved} graphical object(s) in the copied "
                f"diagram of '{new_name}' could not be re-linked (decorations, "
                "or elements added by an active variation) and still point at "
                f"'{source_grid.loc_name}'.",
                RuntimeWarning,
            )
        new_diagram.pDataFolder = new_grid
        new_grid.pDiagram = new_diagram
        return new_diagram

    def get_parent_grid(self, obj_or_path: PFGeneral | str) -> ElmNet | None:
        """Return the `ElmNet` a network element lives in, walking up the folder tree.

        Args:
            obj_or_path: the network element (or its path).

        Returns:
            ElmNet | None: the enclosing grid, or ``None`` if the element has no
            `ElmNet` ancestor.
        """
        obj_or_path = self.act_prj._handle_single_pf_object_or_path_input(obj_or_path)
        return self.act_prj.get_upstream_obj(
            obj_or_path,
            lambda x: x.GetClassName() == "ElmNet",
            error_if_non_existent=False,
        )

    # ------------------------------------------------------------------ #
    # single-line diagram geometry
    # ------------------------------------------------------------------ #
    def get_graphical_objects(
        self,
        elements: Iterable[PFGeneral],
        *,
        diagram: PFGeneral | str | None = None,
    ) -> dict[PFGeneral, list[PFGeneral]]:
        """Map each network element to the graphical objects (`IntGrf`) that draw it.

        An element can be drawn in several diagrams and, rarely, more than once in one diagram, so the value is a list (usually of length one).

        Args:
            elements: the network elements (`ElmTerm`, `ElmLne`, ...) to look up.
            diagram: which diagram to search. ``None`` (default) searches the
                ``pDiagram`` of each element's parent grid (`get_parent_grid`); an
                `IntGrfnet` or its path restricts the search to that one diagram.

        Returns:
            ``{element: [IntGrf, ...]}`` - every element in ``elements`` is a key;
            the list is empty when the element is not drawn in the searched
            diagram(s).
        """
        elements = list(elements)
        index: dict[PFGeneral, list[PFGeneral]] = {}
        for diagram_object in self._resolve_diagrams(diagram, elements):
            for graphical_object in diagram_object.GetContents("*.IntGrf", 1):
                data_object = graphical_object.pDataObj
                if data_object is not None:
                    index.setdefault(data_object, []).append(graphical_object)
        return {element: index.get(element, []) for element in elements}

    #: attributes read for the canvas centre of an `IntGrf` (x, y).
    _GRAPHICAL_OBJECT_CENTRE_ATTRIBUTES: tuple[str, str] = ("rCenterX", "rCenterY")

    def get_positions(
        self,
        elements: Iterable[PFGeneral],
        *,
        diagram: PFGeneral | str | None = None,
        aggregate: str = "first",
    ) -> dict[PFGeneral, tuple[float, float]]:
        """Canvas centre ``(x, y)`` of each element's graphical object.

        ``x`` grows to the right; ``y`` follows the diagram's own convention (in
        PowerFactory single-line diagrams larger ``y`` is higher on the page).
        Built on `get_graphical_objects`; intended for node-like elements
        (`ElmTerm`) - a line's graphic is a polyline and may not have a centre.

        Args:
            elements: network elements to locate.
            diagram: see `get_graphical_objects`.
            aggregate: what to return when an element has several graphical
                objects - ``"first"`` or ``"mean"`` (centroid).

        Returns:
            ``{element: (x, y)}`` - elements with no usable graphical object are
            omitted and reported in a warning.
        """
        if aggregate not in ("first", "mean"):
            raise PFInterfaceError("aggregate must be 'first' or 'mean'")
        graphical_objects = self.get_graphical_objects(elements, diagram=diagram)
        positions: dict[PFGeneral, tuple[float, float]] = {}
        without_position: list[PFGeneral] = []
        for element, objects in graphical_objects.items():
            centres = [
                self._graphical_object_centre(graphical_object)
                for graphical_object in objects
            ]
            centres = [centre for centre in centres if centre is not None]
            if not centres:
                without_position.append(element)
            elif aggregate == "first" or len(centres) == 1:
                positions[element] = centres[0]
            else:
                positions[element] = (
                    sum(x for x, _ in centres) / len(centres),
                    sum(y for _, y in centres) / len(centres),
                )
        if without_position:
            names = [element.loc_name for element in without_position[:5]]
            warn(
                f"get_positions: no graphical object for "
                f"{len(without_position)} element(s): {names}"
                + (" ..." if len(without_position) > 5 else ""),
                RuntimeWarning,
            )
        return positions

    def _graphical_object_centre(
        self, graphical_object: PFGeneral
    ) -> tuple[float, float] | None:
        """``(rCenterX, rCenterY)`` of an `IntGrf`, or ``None`` if it has no centre (e.g. a polyline)."""
        if all(
            graphical_object.HasAttribute(attribute)
            for attribute in self._GRAPHICAL_OBJECT_CENTRE_ATTRIBUTES
        ):
            return tuple(
                graphical_object.GetAttribute(attribute)
                for attribute in self._GRAPHICAL_OBJECT_CENTRE_ATTRIBUTES
            )
        return None

    def _resolve_diagrams(
        self,
        diagram: PFGeneral | str | None,
        elements: Iterable[PFGeneral],
    ) -> list[PFGeneral]:
        """The diagrams to search: `diagram` if given, else the `pDiagram` of each element's parent grid (de-duplicated)."""
        if diagram is not None:
            return [self.act_prj._handle_single_pf_object_or_path_input(diagram)]
        diagrams: list[PFGeneral] = []
        for element in elements:
            grid = self.get_parent_grid(element)
            diagram_object = grid.pDiagram if grid is not None else None
            if diagram_object is not None and diagram_object not in diagrams:
                diagrams.append(diagram_object)
        return diagrams

    def rename_branches_after_terminals(
        self,
        branches: Iterable[PFGeneral],
        *,
        prefix: str = "L",
        separator: str = "-",
        short_name: Callable[[str], str] | None = None,
        order_key: Callable[[str], object] | None = None,
    ) -> dict[PFGeneral, str]:
        """Rename branch elements after the two terminals they connect.

        ``<prefix><sep><a><sep><b>``, where ``a`` and ``b`` are the names of the
        terminals on the branch's two ends, passed through ``short_name`` and
        ordered by ``order_key``. Parallel branches that would collide get a
        ``<sep><n>`` suffix.

        Args:
            branches: branch elements - anything with two connected bus attributes
                among ``bus1`` / ``bus2`` / ``bushv`` / ``busmv`` / ``buslv``
                (`ElmLne`, `ElmTr2`, `ElmCoup`, `ElmZpu`, ...).
            prefix: leading token (``"L"`` for lines, ``"T"`` for transformers).
            separator: token separator.
            short_name: maps a terminal ``loc_name`` to the token used in the
                branch name (default: the terminal name unchanged).
            order_key: sort key applied to the two tokens so the result does not
                depend on PowerFactory's ``bus1`` / ``bus2`` order (default: keep
                the branch's own order; pass ``str`` for alphabetical).

        Returns:
            ``{branch: new loc_name}``.
        """
        short_name = short_name or (lambda name: name)
        used: dict[str, int] = {}
        renamed: dict[PFGeneral, str] = {}
        for branch in branches:
            tokens = [
                short_name(terminal.loc_name)
                for terminal in self._branch_terminals(branch)
            ]
            if order_key is not None:
                tokens = sorted(tokens, key=order_key)
            name = separator.join([prefix, *tokens])
            occurrence = used.get(name, 0)
            used[name] = occurrence + 1
            if occurrence:
                name = f"{name}{separator}{occurrence}"
            branch.loc_name = name
            renamed[branch] = name
        return renamed

    def rename_children(
        self,
        container: PFGeneral | str,
        *,
        prefix: str = "",
        suffix: str = "",
        include_subfolders: bool = False,
    ) -> dict[PFGeneral, str]:
        """Add a `prefix` and/or `suffix` to the `loc_name` of a container's children.

        Handy when several copies of the same grid are active in one study case:
        without a distinguishing affix their elements all share names like
        ``Terminal`` / ``General Load`` and cannot be told apart by
        `GetCalcRelevantObjects` or `get_unique_obj`.

        Idempotent - a child whose name already carries the affix is skipped.

        Args:
            container: the `ElmNet` (or its path), or any object with
                `GetContents`.
            prefix: prepended to every child `loc_name`.
            suffix: appended to every child `loc_name`.
            include_subfolders: also rename objects inside sub-folders and
                composite models (default: only the direct children).

        Returns:
            ``{child: new loc_name}`` for the children that were renamed.
        """
        container = self.act_prj._handle_single_pf_object_or_path_input(
            container
        )
        children = (
            container.GetContents("*", 1)
            if include_subfolders
            else container.GetContents()
        )
        renamed: dict[PFGeneral, str] = {}
        for child in children:
            new_name = _affix(child.loc_name, prefix, suffix)
            if new_name is not None:
                child.loc_name = new_name
                renamed[child] = new_name
        return renamed

    def rename_drawn_elements(
        self,
        grid_or_diagram: PFGeneral | str,
        *,
        prefix: str = "",
        suffix: str = "",
    ) -> dict[PFGeneral, str]:
        """Add a `prefix` / `suffix` to the `loc_name` of every element drawn in a diagram.

        Iterates the graphical objects (`IntGrf`) of the single-line diagram and
        renames each one's data object (`pDataObj`) - i.e. only the terminals,
        branches, machines, loads, ... that actually appear on the drawing.
        Cubicles, folders, composite-model internals and decorations without a
        data object are left alone. Idempotent.

        Args:
            grid_or_diagram: an `ElmNet` (its `pDiagram` is used) or an
                `IntGrfnet` directly (or a path to either).
            prefix: prepended to every drawn element's `loc_name`.
            suffix: appended to every drawn element's `loc_name`.

        Returns:
            ``{element: new loc_name}`` for the elements that were renamed.
        """
        obj = self.act_prj._handle_single_pf_object_or_path_input(
            grid_or_diagram
        )
        diagram = obj.pDiagram if obj.GetClassName() == "ElmNet" else obj
        if diagram is None:
            raise PFInterfaceError(
                f"'{obj.loc_name}' has no single-line diagram (pDiagram)."
            )
        renamed: dict[PFGeneral, str] = {}
        for graphical_object in diagram.GetContents("*.IntGrf", 1):
            element = graphical_object.pDataObj
            if element is None or element in renamed:
                continue
            new_name = _affix(element.loc_name, prefix, suffix)
            if new_name is not None:
                element.loc_name = new_name
                renamed[element] = new_name
        return renamed

    def _branch_terminals(self, branch: PFGeneral) -> list[ElmTerm]:
        """The terminals at the connected ends of a branch element (`bus*` cubicles -> `cterm`)."""
        terminals: list[ElmTerm] = []
        for attribute in _BRANCH_BUS_ATTRIBUTES:
            if branch.HasAttribute(attribute):
                cubicle = branch.GetAttribute(attribute)
                if cubicle is not None:
                    terminals.append(cubicle.cterm)
        return terminals

    # ------------------------------------------------------------------ #
    # connecting elements
    # ------------------------------------------------------------------ #
    def connect(
        self, branch: PFGeneral | str, terminal: ElmTerm | str
    ) -> StaCubic:
        """Wire the single disconnected side of a branch element to a terminal.

        `branch` must have exactly one open connection attribute (`bus1` /
        `bus2` / `bushv` / `busmv` / `buslv` equal to ``None``) - e.g. a breaker
        (`ElmCoup`) already wired on one side, or a line with one free end. A
        vacant cubicle of `terminal` is used (a new one is created if none is
        free).

        Args:
            branch: the branch element (or its path) to connect.
            terminal: the `ElmTerm` (or its path) to connect it to.

        Returns:
            StaCubic: the cubicle of `terminal` the branch was wired into.
        """
        branch = self.act_prj._handle_single_pf_object_or_path_input(branch)
        terminal = self.act_prj._handle_single_pf_object_or_path_input(terminal)
        open_attributes = [
            attribute
            for attribute in _BRANCH_BUS_ATTRIBUTES
            if branch.HasAttribute(attribute)
            and branch.GetAttribute(attribute) is None
        ]
        if len(open_attributes) != 1:
            raise PFInterfaceError(
                f"'{branch.loc_name}' ({branch.GetClassName()}) has "
                f"{len(open_attributes)} disconnected cubicle(s) - `connect` "
                "needs exactly one; define an unambiguous connection element."
            )
        cubicle = self.get_vacant_cubicle_of_terminal(terminal)
        branch.SetAttribute(open_attributes[0], cubicle)
        return cubicle

    @staticmethod
    def _path_inside_grid(grid: PFGeneral, element: PFGeneral) -> str:
        """Relative ``"\\"``-joined `loc_name` path of `element` below `grid`.

        Built from `loc_name`s (not `get_path_between_objects`) so a name that
        itself contains ``"/"`` - e.g. ``Breaker/Switch`` - stays one segment.
        """
        segments = []
        node = element
        while node is not None and node != grid:
            segments.append(node.loc_name)
            node = node.GetParent()
        return "\\".join(reversed(segments))



def _affix(name: str, prefix: str, suffix: str) -> str | None:
    """``prefix + name + suffix``, or None if nothing to add / already present."""
    if not (prefix or suffix):
        return None
    already = (not prefix or name.startswith(prefix)) and (
        not suffix or name.endswith(suffix)
    )
    return None if already else f"{prefix}{name}{suffix}"
