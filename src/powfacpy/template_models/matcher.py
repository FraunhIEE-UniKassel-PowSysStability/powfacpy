"""Detect which template a composite model in a grid was built from.

Templates applied to a grid - especially "packed" ones - carry no link back to
the library, so detection is heuristic. `TemplateMatcher` offers several checks
of increasing effort and confidence:

- ``"linked"``     - the frame / DSL block definitions still live under the
  global library (``\\Lib.IntLibrary\\...``). Cheap, only works for non-packed.
- ``"signature"``  - a wired DSL model references a block definition whose
  ``loc_name`` is one of the template's `SIGNATURE_BLKDEF_NAMES`. Robust to
  renaming the composite model / DSL element, not to editing the block library.
- ``"strict"``     - additionally the frame name and the signature block's
  parameter-name set match the template's.

`identify()` returns the best `MatchResult` (or one with ``template_class=None``).

The signature checks above only recognise templates that have a `TemplateModel`
class. To additionally learn *which library template* an arbitrary composite
model came from - even one without a Python class - pass a `LibraryTemplateIndex`
(or an ``app``); every `MatchResult` then carries `library_template_paths`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from powfacpy.pf_classes.protocols import ElmComp
from powfacpy.template_models.base import TEMPLATE_MODELS, TemplateModel

Level = Literal["linked", "signature", "strict"]

_GLOBAL_LIBRARY_PREFIX = "\\Lib.IntLibrary\\"


@dataclass
class MatchResult:
    """Outcome of `TemplateMatcher.identify` for one composite model.

    Attributes:
        composite_model: the `ElmComp` that was matched.
        template_class: the `TemplateModel` subclass that matched, or None if
            none of the registered classes did.
        confidence: rough score in ``[0.0, 1.0]`` for the `template_class`
            match (0.0 when `template_class` is None).
        level: the check that produced the match - ``"linked"`` / ``"signature"``
            / ``"strict"`` - or None.
        evidence: free-form dict of what was inspected (wired block definitions,
            frame name match, the library frame name, ...); useful for
            debugging a match or a non-match.
        library_template_paths: GUI paths of the library template(s) the
            composite model was built from, filled in only when the matcher was
            given a `LibraryTemplateIndex` (or an ``app``). Independent of
            `template_class` - a template with no Python class still gets named
            here. More than one path means a family of variants sharing a frame.
    """

    composite_model: ElmComp
    template_class: type[TemplateModel] | None
    confidence: float  # 0.0 - 1.0
    level: Level | None
    evidence: dict = field(default_factory=dict)
    library_template_paths: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        """True if a `TemplateModel` class matched."""
        return self.template_class is not None

    def build(self, network_element=None) -> TemplateModel | None:
        """Instantiate the matched `TemplateModel`.

        Args:
            network_element: the controlled network element (`ElmGenstat`,
                `ElmSym`, ...) to bind to the model; if None the model finds it
                among its own slots.

        Returns:
            TemplateModel | None: the instantiated model, or None if no
            `template_class` matched.
        """
        if self.template_class is None:
            return None
        return self.template_class(self.composite_model, network_element)


class TemplateMatcher:
    """Match composite models against the registered `TemplateModel` classes."""

    def __init__(
        self,
        template_classes: list[type[TemplateModel]] | None = None,
        app=None,
        library_index=None,
    ) -> None:
        """
        Args:
            template_classes: the `TemplateModel` subclasses to match against;
                defaults to every class registered via `@register` (i.e. all of
                `powfacpy.template_models.TEMPLATE_MODELS`).
            app: a PowerFactory application. If given (and `library_index` is
                not), a `LibraryTemplateIndex` is created from it so every
                `MatchResult` also carries `library_template_paths`. Omit to
                skip library-template detection entirely.
            library_index: a ready `LibraryTemplateIndex` to use instead of
                building one from `app` (e.g. to share one across matchers).
        """
        if template_classes is None and not TEMPLATE_MODELS:
            # make sure the concrete classes have registered themselves
            import powfacpy.template_models  # noqa: F401
        self.template_classes = (
            list(template_classes)
            if template_classes is not None
            else list(TEMPLATE_MODELS)
        )
        if library_index is None and app is not None:
            from powfacpy.template_models.library_index import LibraryTemplateIndex

            library_index = LibraryTemplateIndex(app)
        self.library_index = library_index

    # ------------------------------------------------------------------ #
    def identify(
        self, composite_model: ElmComp, level: Level = "signature"
    ) -> MatchResult:
        """Best match for `composite_model` among the template classes.

        Args:
            composite_model: the applied `ElmComp` to identify.
            level: the strongest check to attempt - ``"linked"`` (frame still
                under the global library), ``"signature"`` (a wired DSL block
                definition identifies the template; the default), or
                ``"strict"`` (also the frame name and parameter-name set).
                Weaker checks are always tried too; a stronger `level` only
                enables the extra ones.

        Returns:
            MatchResult: `template_class` is None if nothing matched. If the
            matcher has a `library_index`, `library_template_paths` and the
            ``"library_frame"`` evidence key are filled in regardless of the
            class match.
        """
        best = MatchResult(composite_model, None, 0.0, None)
        for template_class in self.template_classes:
            result = self._score(composite_model, template_class, level)
            if result.confidence > best.confidence:
                best = result
        if self.library_index is not None:
            library_match = self.library_index.identify(composite_model)
            best.library_template_paths = list(library_match.template_paths)
            best.evidence.setdefault("library_frame", library_match.frame_name)
        return best

    def identify_all(
        self, composite_models: list[ElmComp], level: Level = "signature"
    ) -> list[MatchResult]:
        return [self.identify(cm, level) for cm in composite_models]

    # ------------------------------------------------------------------ #
    def _score(
        self,
        composite_model: ElmComp,
        template_class: type[TemplateModel],
        level: Level,
    ) -> MatchResult:
        frame = composite_model.typ_id
        wired_dsl = [
            elm
            for slot, elm in zip(composite_model.pblk, composite_model.pelm)
            if elm is not None and elm.GetClassName() == "ElmDsl"
        ]
        wired_blkdef_names = {
            dsl.typ_id.loc_name for dsl in wired_dsl if dsl.typ_id is not None
        }
        evidence: dict = {"wired_block_definitions": sorted(wired_blkdef_names)}

        signature_hit = bool(
            set(template_class.SIGNATURE_BLKDEF_NAMES) & wired_blkdef_names
        )
        frame_hit = (
            frame is not None
            and frame.loc_name in template_class.FRAME_BLKDEF_NAMES
        )

        # --- linked -------------------------------------------------------
        linked = frame is not None and frame.GetFullName().startswith(
            _GLOBAL_LIBRARY_PREFIX
        )
        if linked and signature_hit:
            evidence["frame_full_name"] = frame.GetFullName()
            return MatchResult(
                composite_model, template_class, 1.0, "linked", evidence
            )

        if level == "linked":
            return MatchResult(composite_model, None, 0.0, None, evidence)

        # --- signature --------------------------------------------------
        if not signature_hit:
            return MatchResult(composite_model, None, 0.0, None, evidence)
        evidence["signature_block_definitions"] = sorted(
            set(template_class.SIGNATURE_BLKDEF_NAMES) & wired_blkdef_names
        )

        if level == "signature":
            confidence = 0.9 if frame_hit else 0.75
            return MatchResult(
                composite_model, template_class, confidence, "signature", evidence
            )

        # --- strict ---------------------------------------------------
        signature_dsl = next(
            (
                dsl
                for dsl in wired_dsl
                if dsl.typ_id is not None
                and dsl.typ_id.loc_name in template_class.SIGNATURE_BLKDEF_NAMES
            ),
            None,
        )
        params_ok = self._parameter_names_match(signature_dsl, template_class)
        evidence["frame_name_match"] = frame_hit
        evidence["parameter_names_match"] = params_ok
        if frame_hit and params_ok:
            return MatchResult(
                composite_model, template_class, 0.98, "strict", evidence
            )
        return MatchResult(composite_model, None, 0.0, None, evidence)

    @staticmethod
    def _parameter_names_match(
        signature_dsl, template_class: type[TemplateModel]
    ) -> bool:
        expected = getattr(template_class, "SIGNATURE_PARAMETER_NAMES", None)
        if not expected or signature_dsl is None or signature_dsl.typ_id is None:
            return bool(expected) is False  # no expectation -> vacuously ok
        raw = signature_dsl.typ_id.GetAttribute("sParams") or []
        actual = set(
            p.strip()
            for entry in raw
            for p in (entry.split(",") if "," in entry else [entry])
        )
        return set(expected).issubset(actual)
