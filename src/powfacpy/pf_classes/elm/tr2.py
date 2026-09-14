from __future__ import annotations

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import ElmTr2, TypTr2
from powfacpy.pf_classes.elm.elm_base import ElmBase
from powfacpy.exceptions import PFInterfaceError


class TransformerTwoWinding(ElmBase):
    """Wrapper for `ElmTr2` (two-winding transformer).

    The rating and the impedance live on the `TypTr2` type, which is often shared across several transformers. The shared-type handling mirrors `SynchronousMachine`: `make_type_private`, a `copy_shared_type` flag, and a raise when a type-changing setter would silently affect other transformers.

    Adds rating scaling (for rerating a plant equivalent together with its unit) and tap / ratio helpers.
    """

    __slots__ = ()

    def __init__(self, obj: ElmTr2) -> None:
        super().__init__(obj)
        self._obj: ElmTr2

    def __new__(cls, *args, **kwargs) -> ElmTr2 | TransformerTwoWinding:
        """Implemented only to add type hints for the created instance."""
        instance = super().__new__(cls)
        return instance

    # ---- rating / type --------------------------------------------------
    @property
    def rated_apparent_power(self) -> float:
        """Rated apparent power [MVA] (parallel transformers included)."""
        return self._obj.typ_id.strn * self._obj.ntnum

    def get_transformers_sharing_type(self) -> list[ElmTr2]:
        """Other calculation-relevant `ElmTr2` that use the same `TypTr2`.

        Changing the type in place (e.g. its rated power) would affect all of them.
        """
        transformer_type: TypTr2 = self._obj.typ_id
        if transformer_type is None:
            return []
        type_name = transformer_type.GetFullName()
        own_name = self._obj.GetFullName()
        act_prj = ActiveProjectCached()
        return [
            transformer
            for transformer in act_prj.get_calc_relevant_obj(
                "*.ElmTr2", error_if_non_existent=False
            )
            if transformer.GetFullName() != own_name
            and transformer.typ_id is not None
            and transformer.typ_id.GetFullName() == type_name
        ]

    def _check_type_writable(self, copy_shared_type: bool) -> None:
        obj = self._obj
        if obj.typ_id is None:
            raise PFInterfaceError(
                f"'{obj.loc_name}' has no transformer type ('typ_id'); its type cannot be modified."
            )
        others = self.get_transformers_sharing_type()
        if others and not copy_shared_type:
            names = ", ".join(sorted(o.loc_name for o in others))
            raise PFInterfaceError(
                f"The type '{obj.typ_id.loc_name}' of '{obj.loc_name}' is shared with "
                f"{len(others)} other transformer(s) ({names}). Pass copy_shared_type=True "
                "to give this transformer a private copy of its type first."
            )

    def _writable_type(self, copy_shared_type: bool) -> TypTr2:
        """Return the transformer's `TypTr2`, ready to be modified in place.

        Runs `_check_type_writable`; if the type is shared and `copy_shared_type` is True, the transformer is first given a private copy of its type (next to the original) and that copy is returned and re-pointed to via `typ_id`.
        """
        self._check_type_writable(copy_shared_type)
        transformer_type: TypTr2 = self._obj.typ_id
        if self.get_transformers_sharing_type():
            act_prj = ActiveProjectCached()
            # not use_existing: several transformers can share both a type and a
            # loc_name (a fleet built from one template), and use_existing would
            # then hand them all the same "copy" - collapsing the private types
            # back into one. A name clash instead auto-suffixes "(1)", "(2)".
            transformer_type = act_prj.copy_single_obj(
                transformer_type,
                transformer_type.GetParent(),
                new_name=f"{transformer_type.loc_name} ({self._obj.loc_name})",
                overwrite=False,
                use_existing=False,
            )
            self._obj.typ_id = transformer_type
        return transformer_type

    def make_type_private(self) -> TypTr2:
        """Give the transformer a private copy of its `TypTr2` if it currently shares one.

        Returns the transformer's type (the copy, or the original if it was already private).
        """
        return self._writable_type(copy_shared_type=True)

    def set_rated_apparent_power(
        self, apparent_power: float, *, copy_shared_type: bool = False
    ) -> None:
        """Set the rated apparent power [MVA] (`TypTr2.strn`).

        The short-circuit voltage (`uktr` %) is kept, and the copper / iron losses (`pcutr`, `pfe`) are scaled with the rating, so the per-unit impedance and losses are preserved on the new rating.

        Args:
            apparent_power: new rating; `strn` is set to `apparent_power / ntnum`.

            copy_shared_type: give the transformer a private copy of its type before changing the rating (required when the type is shared).
        """
        transformer_type = self._writable_type(copy_shared_type)
        old = transformer_type.strn * self._obj.ntnum
        transformer_type.strn = apparent_power / self._obj.ntnum
        if old:
            ratio = apparent_power / old
            for loss_attribute in ("pcutr", "pfe"):
                if transformer_type.HasAttribute(loss_attribute):
                    transformer_type.SetAttribute(
                        loss_attribute,
                        transformer_type.GetAttribute(loss_attribute) * ratio,
                    )

    def scale_rated_apparent_power(
        self, factor: float, *, copy_shared_type: bool = False
    ) -> None:
        self.set_rated_apparent_power(
            self.rated_apparent_power * factor, copy_shared_type=copy_shared_type
        )

    # ---- tap / ratio --------------------------------------------------
    @property
    def tap_position(self) -> int:
        """Tap-changer 1 position (`nntap`)."""
        return self._obj.nntap

    @tap_position.setter
    def tap_position(self, position: int) -> None:
        self._obj.nntap = position

    @property
    def neutral_tap_position(self) -> int:
        """Neutral tap position (`TypTr2.nntap0`)."""
        return self._obj.typ_id.nntap0

    @property
    def tap_range(self) -> tuple[int, int]:
        """(min, max) tap position (`TypTr2.ntpmn`, `TypTr2.ntpmx`)."""
        transformer_type = self._obj.typ_id
        return transformer_type.ntpmn, transformer_type.ntpmx

    @property
    def tap_step_percent(self) -> float:
        """Voltage change per tap step [%] (`TypTr2.dutap`)."""
        return self._obj.typ_id.dutap

    @property
    def tap_side(self) -> str:
        """Side the tap changer acts on: ``"HV"`` or ``"LV"`` (`TypTr2.tap_side`)."""
        return "HV" if self._obj.typ_id.tap_side == 0 else "LV"

    @property
    def nominal_voltage_ratio(self) -> float:
        """`utrn_h / utrn_l` [-] (nominal, ignoring the tap position)."""
        transformer_type = self._obj.typ_id
        return transformer_type.utrn_h / transformer_type.utrn_l

    @property
    def voltage_ratio(self) -> float:
        """Off-nominal voltage ratio [-] including the current tap position.

        Assumes a ratio-type tap changer (`tapchtype = 0`).
        """
        transformer_type = self._obj.typ_id
        tap_factor = 1.0 + (
            (self._obj.nntap - transformer_type.nntap0)
            * transformer_type.dutap
            / 100.0
        )
        if transformer_type.tap_side == 0:  # HV
            return (transformer_type.utrn_h * tap_factor) / transformer_type.utrn_l
        return transformer_type.utrn_h / (transformer_type.utrn_l * tap_factor)

    def set_tap_position(self, position: int) -> None:
        """Set the tap-changer 1 position (`nntap`), clamped to the type's range."""
        low, high = self.tap_range
        self._obj.nntap = max(low, min(high, position))

    def reset_tap(self) -> None:
        """Set the tap to its neutral position (`TypTr2.nntap0`)."""
        self._obj.nntap = self._obj.typ_id.nntap0

    def set_automatic_tap_control(self, enabled: bool) -> None:
        """Enable / disable the automatic tap changer (`ElmTr2.ntrcn`)."""
        self._obj.ntrcn = 1 if enabled else 0
