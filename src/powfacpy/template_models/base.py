"""`TemplateModel` base class and the registry the matcher iterates over."""

from __future__ import annotations

from abc import ABC
from functools import cached_property

from powfacpy.pf_classes.protocols import BlkDef, ElmComp, ElmDsl, PFGeneral

#: every concrete `TemplateModel` decorated with `@register` lands here
TEMPLATE_MODELS: list[type["TemplateModel"]] = []


def register(cls: type["TemplateModel"]) -> type["TemplateModel"]:
    """Class decorator - add a `TemplateModel` subclass to `TEMPLATE_MODELS`."""
    TEMPLATE_MODELS.append(cls)
    return cls


class TemplateModel(ABC):
    """Base class for an applied dynamic-model template in a grid.

    A `TemplateModel` wraps the composite model (`ElmComp`) that was built from a
    template, plus - via `network_element` - the network element it controls.
    Concrete subclasses add domain methods (`get_inertia_constant`, ...).

    Matching (used by `TemplateMatcher`) is driven by the class attributes:

    - `TEMPLATE_LOC_NAMES`: `loc_name`s of the source `IntTemplate`(s).
    - `FRAME_BLKDEF_NAMES`: acceptable `loc_name`s of the composite model's frame.
    - `SIGNATURE_BLKDEF_NAMES`: `loc_name`s of the block definition(s) that
      uniquely identify this template among the wired DSL models.
    - `NETWORK_ELEMENT_CLASSES`: PF classes of the controlled element.
    """

    TEMPLATE_LOC_NAMES: tuple[str, ...] = ()
    FRAME_BLKDEF_NAMES: tuple[str, ...] = ()
    SIGNATURE_BLKDEF_NAMES: tuple[str, ...] = ()
    NETWORK_ELEMENT_CLASSES: tuple[str, ...] = ()

    def __init__(
        self,
        composite_model: ElmComp,
        network_element: PFGeneral | None = None,
    ) -> None:
        if composite_model.GetClassName() != "ElmComp":
            raise TypeError(
                f"expected an ElmComp, got {composite_model.GetClassName()}"
            )
        self.composite_model = composite_model
        self._network_element = network_element

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.composite_model.GetFullName()!r})"

    # ------------------------------------------------------------------ #
    # structure
    # ------------------------------------------------------------------ #
    @cached_property
    def frame(self) -> BlkDef | None:
        """The composite model's frame (`typ_id`)."""
        return self.composite_model.typ_id

    @cached_property
    def slots(self) -> dict[str, PFGeneral | None]:
        """`{slot_name: assigned_element_or_None}` of the composite model."""
        return {
            slot.loc_name: elm
            for slot, elm in zip(
                self.composite_model.pblk, self.composite_model.pelm
            )
        }

    @cached_property
    def dsl_models(self) -> list[ElmDsl]:
        """The `ElmDsl` models wired into the composite model."""
        return [
            elm
            for elm in self.slots.values()
            if elm is not None and elm.GetClassName() == "ElmDsl"
        ]

    @cached_property
    def network_element(self) -> PFGeneral | None:
        """The controlled network element (e.g. `ElmGenstat`, `ElmSym`).

        Taken from the constructor argument, otherwise the first slot element
        whose class is in `NETWORK_ELEMENT_CLASSES` (or a generic generator set).
        """
        if self._network_element is not None:
            return self._network_element
        classes = self.NETWORK_ELEMENT_CLASSES or (
            "ElmGenstat",
            "ElmSym",
            "ElmAsm",
            "ElmVsc",
            "ElmPvsys",
        )
        for elm in self.slots.values():
            if elm is not None and elm.GetClassName() in classes:
                return elm
        return None

    def dsl_by_blkdef(self, *blkdef_loc_names: str) -> ElmDsl | None:
        """First wired `ElmDsl` whose block definition is one of `blkdef_loc_names`."""
        wanted = set(blkdef_loc_names)
        for dsl in self.dsl_models:
            if dsl.typ_id is not None and dsl.typ_id.loc_name in wanted:
                return dsl
        return None

    def dsl_in_slot(self, *slot_name_fragments: str) -> ElmDsl | None:
        """Wired `ElmDsl` in the first slot whose name contains one of the fragments."""
        fragments = tuple(f.lower() for f in slot_name_fragments)
        for name, elm in self.slots.items():
            if (
                elm is not None
                and elm.GetClassName() == "ElmDsl"
                and any(f in name.lower() for f in fragments)
            ):
                return elm
        return None

    @staticmethod
    def parameter(dsl: ElmDsl, name: str, default: float | None = None) -> float | None:
        """Read a DSL parameter, returning `default` if it is missing."""
        if dsl is None or not dsl.HasAttribute(name):
            return default
        return dsl.GetAttribute(name)

    # ------------------------------------------------------------------ #
    # common quantities (subclasses may override)
    # ------------------------------------------------------------------ #
    @cached_property
    def rated_apparent_power_MVA(self) -> float | None:
        """Rated apparent power of the controlled element, in MVA."""
        elm = self.network_element
        if elm is None:
            return None
        for attr in ("sgn", "Sn", "sgini"):
            if elm.HasAttribute(attr):
                return elm.GetAttribute(attr)
        return None

    def is_grid_forming(self) -> bool:
        """Whether this template models a grid-forming unit (default: True)."""
        return True
