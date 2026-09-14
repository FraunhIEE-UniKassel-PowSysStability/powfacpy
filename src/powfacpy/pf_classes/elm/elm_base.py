from __future__ import annotations

"""
Base classes for elm.
"""

import warnings
from abc import ABC
from typing import Callable
from powfacpy.exceptions import PFInvalidCondition, PFInterfaceError
from powfacpy.pf_classes.protocols import ElmComp, PFGeneral, ElmNet
from powfacpy.base.base import BaseChildStatic
from powfacpy.base.active_project import ActiveProject



class ElmBase(BaseChildStatic):
    __slots__ = ()

    def __init__(self, obj: PFGeneral) -> None:
        super().__init__(obj)

    def set_out_of_service(self):
        self._obj.outserv = 1

    def set_into_service(self):
        self._obj.outserv = 0

    def get_parent_grid(self) -> ElmNet:
        act_prj = ActiveProject()
        return act_prj.get_upstream_obj(
            self._obj, lambda x: x.GetClassName() == "ElmNet"
        )


class SinglePortBase(ABC):
    """Mixin for network elements with a single terminal connection and an active/reactive power dispatch (`ElmSym`, `ElmGenstat`, `ElmPvsys`, ...).

    Always mixed together with `ElmBase`, so `self._obj` is the wrapped PowerFactory object.

    The dispatch and limit setters operate per parallel unit, i.e. they write `pgini`/`qgini`/`sgn` as is (consistent with PowerFactory and with the `p`/`q` properties). Use `powfacpy.pf_classes.elm.unit_collection.UnitCollection` to work with station/plant totals.
    """

    __slots__ = ()

    @property
    def terminal(self):
        return self.bus1.cterm

    @property
    def number_of_parallel_units(self) -> int:
        return self._obj.ngnum

    @property
    def p(self):
        return self._obj.pgini

    @p.setter
    def p(self, p: float):
        self._obj.pgini = p

    @property
    def q(self) -> float:
        return self._obj.qgini

    @q.setter
    def q(self, q: float):
        self._obj.qgini = q

    @property
    def rated_apparent_power(self) -> float:
        """Rated apparent power [MVA] of the whole station (parallel units included)."""
        return self._obj.sgn * self._obj.ngnum

    # ---- dispatch -----------------------------------------------------------
    def set_power_dispatch(
        self,
        active_power: float,
        reactive_power: float | None = None,
        *,
        power_factor: float | None = None,
        capacitive: bool = False,
        adapt_limits: bool = True,
    ) -> None:
        """Set the active power dispatch setpoint, optionally with reactive power or power factor.

        `active_power` and `reactive_power` are per parallel unit (written to `pgini`/`qgini`).

        Args:
            active_power: Active power setpoint `pgini` [MW].

            reactive_power: Reactive power setpoint `qgini` [Mvar]. Mutually exclusive with `power_factor`. Switches `mode_inp` to "PQ".

            power_factor: Power factor `cosgini`. Mutually exclusive with `reactive_power`. Switches `mode_inp` to "PC".

            capacitive: Only relevant together with `power_factor`: whether the power factor is capacitive/overexcited (sets `pf_recap`).

            adapt_limits: Widen the active and reactive power operational limits (`Pmax_uc`/`Pmin_uc`, `cQ_min`/`cQ_max`) when the setpoint falls outside. Never narrows them. Defaults to True.
        """
        if reactive_power is not None and power_factor is not None:
            raise PFInterfaceError(
                "Pass either 'reactive_power' or 'power_factor', not both."
            )
        obj = self._obj
        # Widen the limits before writing the setpoints: PowerFactory clamps
        # 'qgini' to the reactive power operational limits on assignment.
        if adapt_limits:
            self._adapt_active_power_limits(active_power)
            if reactive_power is not None:
                self._adapt_reactive_power_limits(reactive_power)
        obj.pgini = active_power
        if power_factor is not None:
            obj.mode_inp = "PC"
            obj.cosgini = abs(power_factor)
            obj.pf_recap = 1 if capacitive else 0
        elif reactive_power is not None:
            obj.mode_inp = "PQ"
            obj.qgini = reactive_power

    def scale_power_dispatch(self, factor: float, *, adapt_limits: bool = True) -> None:
        """Scale the active and reactive power dispatch setpoints by `factor` (keeps the power factor)."""
        self.set_power_dispatch(
            self._obj.pgini * factor,
            self._obj.qgini * factor,
            adapt_limits=adapt_limits,
        )

    # ---- operational limits -----------------------------------------------
    def get_active_power_operational_limits(self) -> tuple[float, float]:
        """(`Pmin_uc`, `Pmax_uc`) [MW]."""
        return self._obj.Pmin_uc, self._obj.Pmax_uc

    def set_active_power_operational_limits(
        self, minimum: float, maximum: float
    ) -> None:
        self._obj.Pmin_uc = minimum
        self._obj.Pmax_uc = maximum

    def get_reactive_power_operational_limits(self) -> tuple[float, float]:
        """(`cQ_min`, `cQ_max`) [Mvar]."""
        return self._obj.cQ_min, self._obj.cQ_max

    def set_reactive_power_operational_limits(
        self, minimum: float, maximum: float
    ) -> None:
        obj = self._obj
        if obj.HasAttribute("iqtype") and obj.iqtype == 1:
            warnings.warn(
                f"'{obj.loc_name}': reactive power limits were configured to be taken "
                "from the machine type ('iqtype' = 1); switching to element limits."
            )
            obj.iqtype = 0
        obj.cQ_min = minimum
        obj.cQ_max = maximum

    def _adapt_active_power_limits(self, active_power: float) -> None:
        minimum, maximum = self.get_active_power_operational_limits()
        widened = (min(minimum, active_power), max(maximum, active_power))
        if widened != (minimum, maximum):
            self.set_active_power_operational_limits(*widened)

    def _adapt_reactive_power_limits(self, reactive_power: float) -> None:
        if self._obj.pQlimType is not None:
            warnings.warn(
                f"'{self._obj.loc_name}' has a reactive power capability curve "
                "('pQlimType'); not adapting its reactive power limits automatically."
            )
            return
        minimum, maximum = self.get_reactive_power_operational_limits()
        widened = (min(minimum, reactive_power), max(maximum, reactive_power))
        if widened != (minimum, maximum):
            self.set_reactive_power_operational_limits(*widened)

    def _scale_active_power_limits(self, ratio: float) -> None:
        """Scale the active power operational limits (`Pmin_uc` / `Pmax_uc`) by `ratio`.

        The reactive power operational limits are stored per unit of `sgn` and therefore already track a rating change - only the active power limits (absolute MW) need scaling.
        """
        minimum, maximum = self.get_active_power_operational_limits()
        self.set_active_power_operational_limits(minimum * ratio, maximum * ratio)

    # ---- rated power ------------------------------------------------------
    def _check_type_writable(self, copy_shared_type: bool) -> None:
        """Raise if a setter that modifies this element's type cannot be applied. No-op by default; `SynchronousMachine` overrides it (its rating and inertia live on a possibly shared `TypSym`)."""
        del copy_shared_type

    def set_rated_apparent_power(
        self,
        apparent_power: float,
        *,
        scale_setpoints: bool = False,
        scale_limits: bool = False,
        scale_step_up_transformer: bool = False,
        copy_shared_type: bool = False,
    ) -> None:
        """Set the rated apparent power [MVA] of the whole station.

        Args:
            apparent_power: New station rating; `sgn` is set to `apparent_power / ngnum`.

            scale_setpoints: Also scale the active/reactive power dispatch setpoints by the same ratio.

            scale_limits: Also scale the active power operational limits (`Pmin_uc` / `Pmax_uc`) by the same ratio, so the unit's headroom relative to its rating is preserved.

            scale_step_up_transformer: Also resize the unit's step-up transformer to the new rating (`rescale_step_up_transformer`, `margin=0.0`).

            copy_shared_type: Ignored here; only meaningful for elements whose rating lives on a shared type (see `SynchronousMachine`).
        """
        del copy_shared_type
        old = self.rated_apparent_power
        self._obj.sgn = apparent_power / self._obj.ngnum
        if old:
            ratio = apparent_power / old
            if scale_limits:
                self._scale_active_power_limits(ratio)
            if scale_setpoints:
                self.scale_power_dispatch(ratio)
        if scale_step_up_transformer and self.get_step_up_transformer() is not None:
            self.rescale_step_up_transformer()

    def scale_rated_apparent_power(
        self,
        factor: float,
        *,
        scale_setpoints: bool = False,
        scale_limits: bool = False,
        scale_step_up_transformer: bool = False,
        copy_shared_type: bool = False,
    ) -> None:
        self.set_rated_apparent_power(
            self.rated_apparent_power * factor,
            scale_setpoints=scale_setpoints,
            scale_limits=scale_limits,
            scale_step_up_transformer=scale_step_up_transformer,
            copy_shared_type=copy_shared_type,
        )

    # ---- step-up transformer -------------------------------------------
    def get_step_up_transformer(self):
        """The two-winding transformer (`ElmTr2`) directly on the unit's terminal, or `None`.

        A unit typically has exactly one step-up transformer; the first one found is returned.
        """
        from powfacpy.pf_classes.elm.term import Terminal

        connected = Terminal(self.terminal).get_connected_elements(
            condition=lambda x: x.GetClassName() == "ElmTr2"
        )
        return connected[0] if connected else None

    def rescale_step_up_transformer(
        self, *, margin: float = 0.0, copy_shared_type: bool = True
    ):
        """Resize the unit's step-up transformer to the unit's rating times `(1 + margin)`.

        Args:
            margin: fractional headroom over the unit's rated apparent power - `0.0` (default) gives an equal rating, `0.15` a 15 % larger transformer (e.g. for reactive power supply).

            copy_shared_type: give the transformer a private `TypTr2` copy first if its type is shared (default True - transformer types are almost always shared across a fleet).

        Returns:
            TransformerTwoWinding | None: the resized transformer, or `None` if the unit has no step-up transformer.
        """
        from powfacpy.pf_classes.elm.tr2 import TransformerTwoWinding

        transformer = self.get_step_up_transformer()
        if transformer is None:
            warnings.warn(
                f"'{self._obj.loc_name}' has no step-up transformer; nothing to rescale."
            )
            return None
        wrapped = TransformerTwoWinding(transformer)
        wrapped.set_rated_apparent_power(
            self.rated_apparent_power * (1.0 + margin),
            copy_shared_type=copy_shared_type,
        )
        return wrapped

class ElmPlantControlledBase(ABC):
    """Elm that can be part of DSL frame (has attribute 'c_pmod' that points to a composite frame, i.e. a plant model)."""

    __slots__ = ()

    @property
    def composite_frame(self) -> ElmComp:
        return self._obj.c_pmod

    @composite_frame.setter
    def composite_frame(self, frame: ElmComp) -> None:
        self._obj.c_pmod = frame

    def get_network_elements_of_plant_model(
        self, condition: Callable | None = None, error_if_non_existent: bool = True
    ) -> list[PFGeneral]:
        """
        Get network elements of plant model (composite frame) on condition.

        Args:
            condition (Callable | None, optional): Condition to select network elements, e.g. 'lambda x: x.typ_id.loc_name.startswith("gov_")' to get governors. Defaults to None.
            error_if_non_existent (bool, optional): Raise exception if no objects that satisfy condition are found. Defaults to True.

        Raises:
            PFInvalidCondition: If no objects that satisfy condition are found.

        Returns:
            list[PFGeneral]: Network elements
        """
        # Imported lazily: 'comp' imports back from this module.
        from powfacpy.pf_classes.elm.comp import CompositeModel

        elmcomp = CompositeModel(self.composite_frame)
        if condition is None:
            return elmcomp.get_network_elms()
        netelms = []
        for netelm in elmcomp.get_network_elms():
            if netelm and condition(netelm):
                netelms.append(netelm)
        if error_if_non_existent and not netelms:
            raise PFInvalidCondition("No network element found.")
        return netelms