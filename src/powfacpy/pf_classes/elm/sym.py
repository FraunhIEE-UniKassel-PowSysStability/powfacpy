from __future__ import annotations

from fnmatch import fnmatch
from typing import Callable

import numpy as np

from powfacpy.base.active_project import ActiveProjectCached
from powfacpy.pf_classes.protocols import ElmSym, PFGeneral, TypSym, ElmTerm, ElmDsl
from powfacpy.pf_classes.elm.elm_base import (
    ElmBase,
    SinglePortBase,

)
from powfacpy.pf_classes.elm.elm_base import ElmPlantControlledBase
from powfacpy.pf_classes.elm.term import Terminal
from powfacpy.result_variables import ResVar
from powfacpy.engineering_helpers import get_weighted_average
from powfacpy.exceptions import PFInterfaceError

LDF = ResVar.LF_Bal


class SynchronousMachine(ElmBase, SinglePortBase, ElmPlantControlledBase):

    __slots__ = ()

    def __init__(self, obj: ElmSym) -> None:
        super().__init__(obj)
        self._obj: ElmSym

    def __new__(cls, *args, **kwargs) -> ElmSym | SynchronousMachine:
        """Implemented only to add type hints for the created instance.

        Returns:
            ElmSym | SynchronousMachine: New instance
        """
        instance = super().__new__(cls)
        return instance

    @property
    def ratedS(self) -> float:
        "Apparent power [MVA]. Parallel machines are considered. 'ratedS' is CGMES conform."
        return self._obj.typ_id.sgn * self._obj.ngnum

    @property
    def rated_apparent_power(self) -> float:
        return self.ratedS

    def get_machines_sharing_type(self) -> list[ElmSym]:
        """Other calculation-relevant machines (`ElmSym` / `ElmAsm`) that use the same `TypSym`.

        Changing the type in place (e.g. its rated power) would affect all of them.

        Only the active network is considered - `TypSym.GetReferences()` also
        returns variation-stage shadows of the machine itself, which are not
        separate machines.
        """
        machine_type: TypSym = self._obj.typ_id
        if machine_type is None:
            return []
        type_name = machine_type.GetFullName()
        own_name = self._obj.GetFullName()
        act_prj = ActiveProjectCached()
        machines = act_prj.get_calc_relevant_obj(
            "*.ElmSym", error_if_non_existent=False
        ) + act_prj.get_calc_relevant_obj("*.ElmAsm", error_if_non_existent=False)
        return [
            machine
            for machine in machines
            if machine.GetFullName() != own_name
            and machine.typ_id is not None
            and machine.typ_id.GetFullName() == type_name
        ]

    def _check_type_writable(self, copy_shared_type: bool) -> None:
        """Raise if the machine's `TypSym` cannot be modified in place.

        For `ElmSym` the rating (`sgn`) and the inertia (`h`) live on the machine type. If that type is shared with other machines, changing it would silently affect all of them, so type-changing setters raise unless `copy_shared_type` is True.
        """
        obj = self._obj
        if obj.typ_id is None:
            raise PFInterfaceError(
                f"'{obj.loc_name}' has no machine type ('typ_id'); its type cannot be modified."
            )
        others = self.get_machines_sharing_type()
        if others and not copy_shared_type:
            names = ", ".join(sorted(o.loc_name for o in others))
            raise PFInterfaceError(
                f"The type '{obj.typ_id.loc_name}' of '{obj.loc_name}' is shared with "
                f"{len(others)} other machine(s) ({names}). Pass copy_shared_type=True "
                "to give this machine a private copy of its type first."
            )

    def _writable_type(self, copy_shared_type: bool) -> TypSym:
        """Return the machine's `TypSym`, ready to be modified in place.

        Runs `_check_type_writable`; if the type is shared and `copy_shared_type` is True, the machine is first given a private copy of its type (next to the original) and that copy is returned and re-pointed to via `typ_id`.
        """
        self._check_type_writable(copy_shared_type)
        machine_type: TypSym = self._obj.typ_id
        if self.get_machines_sharing_type():
            act_prj = ActiveProjectCached()
            # not use_existing: several machines can share both a type and a
            # loc_name (a fleet built from one template), and use_existing would
            # then hand them all the same "copy" - collapsing the private types
            # back into one. A name clash instead auto-suffixes "(1)", "(2)".
            machine_type = act_prj.copy_single_obj(
                machine_type,
                machine_type.GetParent(),
                new_name=f"{machine_type.loc_name} ({self._obj.loc_name})",
                overwrite=False,
                use_existing=False,
            )
            self._obj.typ_id = machine_type
        return machine_type

    def make_type_private(self) -> TypSym:
        """Give the machine a private copy of its `TypSym` if it currently shares one.

        The copy is created next to the original and `typ_id` is re-pointed to it. Returns the machine's type (the copy, or the original if it was already private). Call this once - e.g. on a fleet built from a single template - before setting each machine's rating or inertia individually.
        """
        return self._writable_type(copy_shared_type=True)

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

        For `ElmSym` the rating (`sgn`) lives on the machine type (`TypSym`). If that type is shared with other machines, changing it in place would silently re-rate all of them, so this raises unless `copy_shared_type` is True - in which case the machine is first given a private copy of its type.

        Args:
            apparent_power: New station rating; the type's `sgn` is set to `apparent_power / ngnum`.

            scale_setpoints: Also scale the active/reactive power dispatch setpoints by the same ratio.

            scale_limits: Also scale the active power operational limits (`Pmin_uc` / `Pmax_uc`) by the same ratio.

            scale_step_up_transformer: Also resize the machine's step-up transformer to the new rating.

            copy_shared_type: Give the machine a private copy of its type before changing the rating (required when the type is shared).
        """
        obj = self._obj
        machine_type = self._writable_type(copy_shared_type)
        old = machine_type.sgn * obj.ngnum
        machine_type.sgn = apparent_power / obj.ngnum
        if old:
            ratio = apparent_power / old
            if scale_limits:
                self._scale_active_power_limits(ratio)
            if scale_setpoints:
                self.scale_power_dispatch(ratio)
        if scale_step_up_transformer and self.get_step_up_transformer() is not None:
            self.rescale_step_up_transformer()

    def set_inertia(
        self,
        inertia_constant_seconds: float,
        *,
        copy_shared_type: bool = False,
    ) -> None:
        """Set the inertia constant H [s] of the machine type (`TypSym.h`).

        H is per unit of the type's rated apparent power. Like the rating, it
        lives on the (possibly shared) `TypSym`, so this raises for a shared type
        unless `copy_shared_type` is True.

        Args:
            inertia_constant_seconds: new H [s].

            copy_shared_type: give the machine a private copy of its type first
                (required when the type is shared).
        """
        self._writable_type(copy_shared_type).h = inertia_constant_seconds

    def scale_inertia(
        self, factor: float, *, copy_shared_type: bool = False
    ) -> None:
        """Scale the inertia constant H by `factor` (see `set_inertia`)."""
        machine_type = self._writable_type(copy_shared_type)
        machine_type.h = machine_type.h * factor

    @property
    def H_in_seconds_based_on_Snom(self) -> float:
        "Inertia constant [s]"
        return self._obj.typ_id.h

    @property
    def H_in_MWs(self) -> float:
        "Inertia constant [MWs]"
        return self._obj.typ_id.h * self.ratedS

    @property
    def J(self) -> float:
        "Moment of Inertia [kgm^2]. Parallel machines are considered."
        obj = self._obj
        return obj.typ_id.J * obj.ngnum

    def get_averaged_internal_reactance(
        self, base_apparent_power_MVA: float | None = None
    ) -> float:
        """Get average of the d-and q-axis internal reactances:
        xG = 0.5 (x''d + x''q)

        Returns:
            float: internal reactance [pu]
        """
        typ: TypSym = self._obj.typ_id
        x = 0.5 * (typ.xdss + typ.xqss)
        if base_apparent_power_MVA is None:
            return x
        else:
            return x / (self.ratedS / base_apparent_power_MVA)

    def get_averaged_internal_susceptance(
        self, base_apparent_power_MVA: float | None = None
    ) -> float:
        return 1 / self.get_averaged_internal_reactance(base_apparent_power_MVA)

    def get_approximate_internal_voltage(self) -> complex:
        """Get approximate internal voltage from power supply, terminal voltage and internal reactance.

        This is one way a system operator could approximate the internal voltage based on measurements at the point of connection.

        Returns:
            complex: approximate internal voltage
        """
        p = self._obj.GetAttribute(LDF.ElmSym.m_Psum_bus1.value) / self.ratedS
        q = self._obj.GetAttribute(LDF.ElmSym.m_Qsum_bus1.value) / self.ratedS
        terminal: ElmTerm = self._obj.bus1.cterm
        u_bus = terminal.GetAttribute("m:ur") + 1j * terminal.GetAttribute("m:ui")
        x = self.get_averaged_internal_reactance()
        return u_bus + (q * x + 1j * p * x) / u_bus

    def get_H_in_seconds(self, base_apparent_power_MVA: float | None = None) -> float:
        "Inertia constant [s]"
        if base_apparent_power_MVA is None:
            return self._obj.typ_id.h
        else:
            return self._obj.typ_id.h * (self.ratedS / base_apparent_power_MVA)

    def get_connecting_transformer(
        self, transformer_class: str = "ElmTr*"
    ) -> PFGeneral:
        """Gets the next trafo (compared to GetStepupTransformer which requires a voltage level to stop the search)

        Args:
            transformer_class (str, optional): _description_. Defaults to "ElmTr2".

        Returns:
            PFGeneral: _description_
        """
        return Terminal(self.bus1.cterm).get_connected_elements(
            condition=lambda x: fnmatch(x.GetClassName(), transformer_class)
        )[0]

    def get_terminal_of_transformer_hv_side(
        self, transformer_class: str = "ElmTr*"
    ) -> ElmTerm:
        return self.get_connecting_transformer(transformer_class).bushv.cterm

    def add_external_station_controller(
        self,
        parent_folder: PFGeneral | None = None,
        controlled_terminal: ElmTerm | None = None,
    ) -> None:
        """Add external station controller.

        Args:
            parent_folder (PFGeneral | None, optional): Parent folder of station controller. Defaults to None (same folder as ElmSym is used).
            controlled_terminal (ElmTerm | None, optional): target terminal. Defaults to None.

        Returns:
            _type_: _description_
        """
        if parent_folder is None:
            parent_folder = self._obj.GetParent()
        act_prj = ActiveProjectCached()
        station_ctrl = act_prj.create_in_folder(
            self._obj.loc_name + " station ctrl.ElmStactrl", parent_folder
        )
        self._obj.c_pstac = station_ctrl
        if controlled_terminal is not None:
            station_ctrl.rembar = controlled_terminal
        return station_ctrl

    def get_governor(self, error_if_non_existent: bool = True) -> ElmDsl:
        list_with_one_obj = self.get_network_elements_of_plant_model(
            lambda x: x.typ_id.loc_name.startswith("gov_"),
            error_if_non_existent=error_if_non_existent,
        )
        if list_with_one_obj:
            return list_with_one_obj[0]
        else:
            return None

    def get_avr(self, error_if_non_existent: bool = True) -> ElmDsl:
        list_with_one_obj = self.get_network_elements_of_plant_model(
            lambda x: x.typ_id.loc_name.startswith("avr_"),
            error_if_non_existent=error_if_non_existent,
        )
        if list_with_one_obj:
            return list_with_one_obj[0]
        else:
            return None

    def get_pss(self, error_if_non_existent: bool = True) -> ElmDsl:
        list_with_one_obj = self.get_network_elements_of_plant_model(
            lambda x: x.typ_id.loc_name.startswith("pss_"),
            error_if_non_existent=error_if_non_existent,
        )
        if list_with_one_obj:
            return list_with_one_obj[0]
        else:
            return None

    @staticmethod
    def get_cgmes_mapping():
        return {"inertia": "h"}


def weight_by_apparent_power_of_synchronous_machines(
    values: list[float],
    synchronous_machines: list[SynchronousMachine] | list[ElmSym],
    return_sum_of_weights: bool = False,
) -> float:
    if not isinstance(synchronous_machines[0], SynchronousMachine):
        synchronous_machines = [SynchronousMachine[sm] for sm in synchronous_machines]
    values = np.array(values)
    apparent_power = np.array([sm.ratedS for sm in synchronous_machines])
    return get_weighted_average(
        values, apparent_power, return_sum_of_weights=return_sum_of_weights
    )
