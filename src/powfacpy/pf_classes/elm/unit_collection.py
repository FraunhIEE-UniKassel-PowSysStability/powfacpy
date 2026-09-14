from __future__ import annotations

from typing import Iterator

from powfacpy.pf_classes.protocols import PFGeneral
from powfacpy.pf_classes.class_conversion import convert_pf_obj_to_powfacpy
from powfacpy.exceptions import PFInterfaceError


class UnitCollection:
    """A set of dispatchable single-port units (`ElmSym` / `ElmGenstat` / `ElmPvsys`) that belong to the same grouping and category (e.g. all PV systems of a zone).

    Iterating or indexing a `UnitCollection` yields the raw PowerFactory objects, so it is a drop-in for the list returned by `GroupingBase.get_internal_*`. The power and rating methods act on the whole set.

    The `total_*` quantities and the `distribute` / `scale_to_total` options work with station totals: a unit's contribution is its per-unit setpoint times its number of parallel units (`ngnum`).
    """

    __slots__ = ("_elements", "_powfacpy_objects")

    def __init__(self, elements: list[PFGeneral]) -> None:
        self._elements: list[PFGeneral] = list(elements)
        self._powfacpy_objects = [
            convert_pf_obj_to_powfacpy(element) for element in self._elements
        ]

    # ---- list-like --------------------------------------------------------
    def __iter__(self) -> Iterator[PFGeneral]:
        return iter(self._elements)

    def __len__(self) -> int:
        return len(self._elements)

    def __getitem__(self, index):
        return self._elements[index]

    def __bool__(self) -> bool:
        return bool(self._elements)

    def __eq__(self, other) -> bool:
        if isinstance(other, UnitCollection):
            return self._elements == other._elements
        return self._elements == other

    def __repr__(self) -> str:
        return f"UnitCollection({[o.loc_name for o in self._elements]})"

    @property
    def elements(self) -> list[PFGeneral]:
        """The raw PowerFactory objects."""
        return list(self._elements)

    @property
    def powfacpy_objects(self) -> list:
        """The powfacpy wrappers (`SynchronousMachine` / `StaticGenerator` / `PVSystem`)."""
        return list(self._powfacpy_objects)

    # ---- totals ----------------------------------------------------------
    @property
    def total_active_power(self) -> float:
        """Sum of the active power dispatch setpoints [MW] (parallel units included)."""
        return sum(o._obj.pgini * o._obj.ngnum for o in self._powfacpy_objects)

    @property
    def total_reactive_power(self) -> float:
        """Sum of the reactive power dispatch setpoints [Mvar] (parallel units included)."""
        return sum(o._obj.qgini * o._obj.ngnum for o in self._powfacpy_objects)

    @property
    def total_rated_power(self) -> float:
        """Sum of the rated apparent powers [MVA] (parallel units included)."""
        return sum(o.rated_apparent_power for o in self._powfacpy_objects)

    # ---- dispatch ------------------------------------------------------
    def set_power_dispatch(
        self,
        active_power: float,
        reactive_power: float | None = None,
        *,
        power_factor: float | None = None,
        capacitive: bool = False,
        distribute: bool = False,
        adapt_limits: bool = True,
    ) -> None:
        """Set the dispatch of every unit in the collection.

        By default the given values are written to every unit (per unit). With `distribute=True` they are interpreted as collection totals and split equally among the units.

        See `SinglePortBase.set_power_dispatch` for `power_factor`, `capacitive` and `adapt_limits`.
        """
        count = len(self._powfacpy_objects)
        if not count:
            return
        for unit in self._powfacpy_objects:
            if distribute:
                parallel = unit._obj.ngnum
                unit_active = active_power / count / parallel
                unit_reactive = (
                    None
                    if reactive_power is None
                    else reactive_power / count / parallel
                )
            else:
                unit_active, unit_reactive = active_power, reactive_power
            unit.set_power_dispatch(
                unit_active,
                unit_reactive,
                power_factor=power_factor,
                capacitive=capacitive,
                adapt_limits=adapt_limits,
            )

    def scale_power_dispatch(self, factor: float, *, adapt_limits: bool = True) -> None:
        """Scale the active and reactive dispatch setpoints of every unit by `factor`."""
        for unit in self._powfacpy_objects:
            unit.scale_power_dispatch(factor, adapt_limits=adapt_limits)

    def scale_to_total(
        self,
        total_active_power: float,
        total_reactive_power: float | None = None,
        *,
        base: str = "current",
        adapt_limits: bool = True,
    ) -> None:
        """Re-dispatch the units so their totals match the given values.

        `base` selects how the totals are shared out:

        - "current": proportional to each unit's present active power dispatch (raises if all are zero).
        - "rated": proportional to each unit's rated apparent power.

        `total_reactive_power`, if given, is shared out with the same weights.
        """
        if base == "current":
            weights = [
                o._obj.pgini * o._obj.ngnum for o in self._powfacpy_objects
            ]
        elif base == "rated":
            weights = [o.rated_apparent_power for o in self._powfacpy_objects]
        else:
            raise PFInterfaceError(
                f"'base' must be 'current' or 'rated', got {base!r}."
            )
        total_weight = sum(weights)
        if not total_weight:
            raise PFInterfaceError(
                f"Cannot share out the total with base={base!r}: the weights sum to zero."
            )
        for unit, weight in zip(self._powfacpy_objects, weights):
            share = weight / total_weight
            parallel = unit._obj.ngnum
            unit_active = total_active_power * share / parallel
            unit_reactive = (
                None
                if total_reactive_power is None
                else total_reactive_power * share / parallel
            )
            unit.set_power_dispatch(
                unit_active, unit_reactive, adapt_limits=adapt_limits
            )

    # ---- operational limits -----------------------------------------
    def set_active_power_operational_limits(
        self, minimum: float, maximum: float
    ) -> None:
        """Set the active power operational limits (`Pmin_uc` / `Pmax_uc`) [MW] on every unit."""
        for unit in self._powfacpy_objects:
            unit.set_active_power_operational_limits(minimum, maximum)

    def set_reactive_power_operational_limits(
        self, minimum: float, maximum: float
    ) -> None:
        """Set the reactive power operational limits (`cQ_min` / `cQ_max`) [Mvar] on every unit."""
        for unit in self._powfacpy_objects:
            unit.set_reactive_power_operational_limits(minimum, maximum)

    # ---- rated power --------------------------------------------------
    def make_types_private(self) -> None:
        """Give every unit that shares an equipment type its own private copy.

        Only `SynchronousMachine` (`ElmSym`) has a shareable unit type; other unit classes carry their rating on the element. Call this once before setting per-unit rating / inertia across a fleet built from one template (see `SynchronousMachine.make_type_private`).
        """
        for unit in self._powfacpy_objects:
            make_private = getattr(unit, "make_type_private", None)
            if make_private is not None:
                make_private()

    def make_step_up_transformer_types_private(self) -> None:
        """Give every unit's step-up transformer its own private `TypTr2` copy.

        Transformer types are almost always shared across a fleet; call this once before rerating the plants individually.
        """
        for unit in self._powfacpy_objects:
            transformer = unit.get_step_up_transformer()
            if transformer is not None:
                convert_pf_obj_to_powfacpy(transformer).make_type_private()

    def rescale_step_up_transformers(
        self, *, margin: float = 0.0, copy_shared_type: bool = True
    ) -> None:
        """Resize every unit's step-up transformer to that unit's rating times `(1 + margin)` (see `SinglePortBase.rescale_step_up_transformer`).

        Units with no step-up transformer are skipped silently.
        """
        for unit in self._powfacpy_objects:
            if unit.get_step_up_transformer() is not None:
                unit.rescale_step_up_transformer(
                    margin=margin, copy_shared_type=copy_shared_type
                )

    def set_rated_power(
        self,
        apparent_power: float,
        *,
        distribute: bool = False,
        scale_setpoints: bool = False,
        scale_limits: bool = False,
        scale_step_up_transformer: bool = False,
        copy_shared_type: bool = False,
    ) -> None:
        """Set the rated apparent power [MVA] of every unit.

        With `distribute=True` the given value is a collection total split equally among the units. See `SinglePortBase.set_rated_apparent_power` for the other arguments.
        """
        count = len(self._powfacpy_objects)
        if not count:
            return
        self._check_types_writable(copy_shared_type)
        for unit in self._powfacpy_objects:
            target = apparent_power / count if distribute else apparent_power
            unit.set_rated_apparent_power(
                target,
                scale_setpoints=scale_setpoints,
                scale_limits=scale_limits,
                scale_step_up_transformer=scale_step_up_transformer,
                copy_shared_type=copy_shared_type,
            )

    def scale_rated_power(
        self,
        factor: float,
        *,
        scale_setpoints: bool = False,
        scale_limits: bool = False,
        scale_step_up_transformer: bool = False,
        copy_shared_type: bool = False,
    ) -> None:
        """Scale the rated apparent power of every unit by `factor`."""
        self._check_types_writable(copy_shared_type)
        for unit in self._powfacpy_objects:
            unit.scale_rated_apparent_power(
                factor,
                scale_setpoints=scale_setpoints,
                scale_limits=scale_limits,
                scale_step_up_transformer=scale_step_up_transformer,
                copy_shared_type=copy_shared_type,
            )

    def _check_types_writable(self, copy_shared_type: bool) -> None:
        """Pre-flight so a type change is not applied to only part of the collection."""
        for unit in self._powfacpy_objects:
            unit._check_type_writable(copy_shared_type)
