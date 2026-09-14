"""Detect which global-library template an applied composite model came from.

A template that has been dragged into a grid keeps no reference to the
`IntTemplate` it originated from, so detection has to work from what is left on
the applied `ElmComp`. The most reliable trace is its **frame** (`typ_id`):

- For most library templates the frame block definition is *shared* - it lives
  under ``\\Lib.IntLibrary\\Dynamics\\...`` and the applied composite model
  points straight at it. Matching the frame's full path against an index of all
  library templates then identifies the template (often a small family of
  variants, e.g. the 50 Hz / 60 Hz pair).
- For "packed" templates the frame was copied into the ``IntTemplate`` itself;
  its full path still contains the template name, so the match stays unique.
- Templates whose frame was renamed, or old templates packed from a previous
  PowerFactory version, cannot be matched this way - `identify` then falls back
  to the frame's ``loc_name`` (lower confidence) or reports no match.

`LibraryTemplateIndex` builds the index once (a few seconds - it walks every
``IntTemplate`` under ``Templates``) and caches it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.applications.digsilent_library import DigsilentLibrary
from powfacpy.pf_classes.protocols import ElmComp, PFApp, PFGeneral


@dataclass
class LibraryTemplateMatch:
    """Result of `LibraryTemplateIndex.identify` for one composite model.

    Attributes:
        composite_model: the applied `ElmComp` that was looked up.
        template_paths: GUI paths (relative to the library root, e.g.
            ``r"Templates\\Photovoltaic\\WECC Large-scale PV Plant 110MVA 50Hz"``)
            of every library template whose composite model uses the same frame.
            Empty if nothing matched; more than one entry means the frame is
            shared by a family of templates (typically the 50 Hz / 60 Hz or
            generation / storage variants) that cannot be told apart from the
            frame alone.
        frame_name: ``loc_name`` of the composite model's frame (`typ_id`), or
            None if it has no frame.
        matched_by: how the match was made - ``"frame"`` (the frame block
            definition is the exact one referenced by the template, high
            confidence), ``"frame_name"`` (only the frame's ``loc_name`` matches
            some template, low confidence), or None (no match).
        confidence: rough score in ``[0.0, 1.0]`` - ``1.0`` unique frame match,
            ``0.8`` frame match shared by several templates, ``0.4`` name-only
            match, ``0.0`` no match.
    """

    composite_model: ElmComp
    template_paths: list[str] = field(default_factory=list)
    frame_name: str | None = None
    matched_by: str | None = None  # "frame" | "frame_name" | None
    confidence: float = 0.0

    def __bool__(self) -> bool:
        """True if at least one library template matched."""
        return bool(self.template_paths)

    @property
    def is_unique(self) -> bool:
        """True if exactly one library template matched (no ambiguity)."""
        return len(self.template_paths) == 1


class LibraryTemplateIndex(ApplicationBase):
    """Index of the global library's templates for applied-template detection.

    Build it once per session and reuse it; the two frame indices are computed
    lazily on first `identify` call and then cached on the instance.

    Attributes:
        library: the `DigsilentLibrary` used to enumerate templates and to turn
            template objects into GUI-style paths.

    Example:
        ```python
        index = LibraryTemplateIndex(app)
        for comp in grid.GetContents("*.ElmComp", 1):
            match = index.identify(comp)
            if match:
                print(comp.loc_name, "->", match.template_paths)
        ```
    """

    #: only templates in this branch are indexed (see `DigsilentLibrary`)
    ROOT_DISPLAY_PATH = "Templates"

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        """
        Args:
            pf_app: the PowerFactory application, as accepted by
                `ApplicationBase` - a `powerfactory` app object, None to let
                powfacpy fetch the running one, or False (the default) to reuse
                the app already bound to the `ActiveProject` class.
            cached: if True, use `ActiveProjectCached` (assumes the active
                project never changes); passed through to `ApplicationBase` and
                to the internal `DigsilentLibrary`.
        """
        super().__init__(pf_app, cached)
        self.library = DigsilentLibrary(pf_app, cached)

    # ------------------------------------------------------------------ #
    # the index
    # ------------------------------------------------------------------ #
    @cached_property
    def _templates(self) -> list[PFGeneral]:
        """Every `IntTemplate` under `ROOT_DISPLAY_PATH`, recursively.

        The walk descends only through folders (`IntFolder` / `IntPrjfolder`),
        never into an `IntTemplate`'s own contents, so it stays cheap.

        Returns:
            list[PFGeneral]: the `IntTemplate` objects, in library order.
        """
        root = self.library.get_object(self.ROOT_DISPLAY_PATH)
        found: list[PFGeneral] = []

        def walk(folder: PFGeneral) -> None:
            for child in folder.GetContents():
                class_name = child.GetClassName()
                if class_name == "IntTemplate":
                    found.append(child)
                elif class_name in ("IntFolder", "IntPrjfolder"):
                    walk(child)

        walk(root)
        return found

    @cached_property
    def frame_path_to_templates(self) -> dict[str, list[str]]:
        """Index keyed by the frame block definition's full database path.

        ``{frame.GetFullName(): [template GUI path, ...]}``. A full path is
        unique, so a hit here is a confident match. Built lazily on first
        access (walks every template - a few seconds) and cached.

        Returns:
            dict[str, list[str]]: template GUI paths per frame path, each list
            sorted and de-duplicated.
        """
        return self._build_index(key="full_name")

    @cached_property
    def frame_name_to_templates(self) -> dict[str, list[str]]:
        """Index keyed by the frame block definition's ``loc_name`` only.

        ``{frame.loc_name: [template GUI path, ...]}``. A bare name is not
        unique (many templates reuse names such as ``"Voltage/Frequency
        Generic"``), so this is only a low-confidence fallback for `identify`.
        Built lazily and cached.

        Returns:
            dict[str, list[str]]: template GUI paths per frame ``loc_name``,
            each list sorted and de-duplicated.
        """
        return self._build_index(key="loc_name")

    def _build_index(self, key: str) -> dict[str, list[str]]:
        """Build one of the frame indices.

        Args:
            key: ``"full_name"`` to key by ``frame.GetFullName()``,
                ``"loc_name"`` to key by ``frame.loc_name``.

        Returns:
            dict[str, list[str]]: template GUI paths per frame key, each list
            sorted and de-duplicated.
        """
        index: dict[str, list[str]] = {}
        for template in self._templates:
            template_path = self.library.gui_path(template)
            for composite_model in template.GetContents("*.ElmComp", 1):
                frame = composite_model.typ_id
                if frame is None:
                    continue
                frame_key = (
                    frame.GetFullName() if key == "full_name" else frame.loc_name
                )
                paths = index.setdefault(frame_key, [])
                if template_path not in paths:
                    paths.append(template_path)
        return {k: sorted(v) for k, v in index.items()}

    # ------------------------------------------------------------------ #
    # detection
    # ------------------------------------------------------------------ #
    def identify(self, composite_model: ElmComp) -> LibraryTemplateMatch:
        """Best guess at the library template `composite_model` was built from.

        Tries the full-path index first (`frame_path_to_templates`), then the
        name-only fallback (`frame_name_to_templates`).

        Args:
            composite_model: an applied `ElmComp` (e.g. an `ElmGenstat`'s or
                `ElmSym`'s control composite model in a grid).

        Returns:
            LibraryTemplateMatch: falsy (empty `template_paths`) if the frame is
            missing or matches no library template.
        """
        frame = composite_model.typ_id
        if frame is None:
            return LibraryTemplateMatch(composite_model)
        by_path = self.frame_path_to_templates.get(frame.GetFullName())
        if by_path:
            return LibraryTemplateMatch(
                composite_model,
                list(by_path),
                frame.loc_name,
                "frame",
                1.0 if len(by_path) == 1 else 0.8,
            )
        by_name = self.frame_name_to_templates.get(frame.loc_name)
        if by_name:
            return LibraryTemplateMatch(
                composite_model, list(by_name), frame.loc_name, "frame_name", 0.4
            )
        return LibraryTemplateMatch(
            composite_model, [], frame.loc_name, None, 0.0
        )

    def identify_all(
        self, composite_models: list[ElmComp]
    ) -> list[LibraryTemplateMatch]:
        """`identify` each composite model in a list.

        Args:
            composite_models: the `ElmComp` objects to look up.

        Returns:
            list[LibraryTemplateMatch]: one result per input, same order.
        """
        return [self.identify(cm) for cm in composite_models]

    def identify_in(self, container: PFGeneral) -> list[LibraryTemplateMatch]:
        """`identify` every `ElmComp` found recursively under `container`.

        Args:
            container: an object to search - typically an `ElmNet` (grid), but
                any object with `GetContents` works (e.g. a project folder).

        Returns:
            list[LibraryTemplateMatch]: one result per `ElmComp` found, in the
            order `GetContents` returns them.
        """
        return self.identify_all(container.GetContents("*.ElmComp", 1))
