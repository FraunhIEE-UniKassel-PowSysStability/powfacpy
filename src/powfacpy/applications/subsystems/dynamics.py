"""Dynamic models, synchronous machines and dynamic properties of a subsystem such as inertia and frequency-control margins.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from functools import cached_property
import numpy as np
import pandas as pd

from powfacpy.pf_classes.protocols import ElmTerm, ElmDsl
from powfacpy.pf_classes.elm.sym import SynchronousMachine
from powfacpy.pf_classes.elm.dsl import get_dsl_models_info_sorted_by_block_definition, export_dsl_model_info_to_csv

if TYPE_CHECKING:
    from powfacpy.applications.subsystems.subsystem import SubSystem


class SubSystemDynamicModels:
    """Subsystem dynamic models (e.g. synchronous machines, governors, controllers)."""

    def __init__(self, parent: SubSystem) -> None:
        self.parent = parent

    @cached_property
    def synchronous_machines(self) -> SubSystemSynchronousMachines:
        return SubSystemSynchronousMachines(self)


class SubSystemSynchronousMachines:
    """Synchronnous machines and their controllers in the subsystem."""

    def __init__(self, parent: SubSystemDynamicModels) -> None:
        self.parent = parent

    @cached_property
    def root_subsystem(self) -> SubSystem:
        return self.parent.parent

    @cached_property
    def synchronous_machines(self) -> list:
        return self.root_subsystem.get_internal_elms_of_class("ElmSym")

    @cached_property
    def synchronous_machines_powfacpy(self) -> list[SynchronousMachine]:
        """Get synchronous machines as powfacpy objects."""
        return [SynchronousMachine(sm) for sm in self.synchronous_machines]

    @cached_property
    def governors(self) -> list[ElmDsl | None]:
        """Get governors"""
        return [
            sm.get_governor(error_if_non_existent=False)
            for sm in self.synchronous_machines_powfacpy
        ]

    @cached_property
    def avrs(self) -> list[ElmTerm]:
        """Get automatic voltage regulators (AVR)"""
        return [
            sm.get_avr(error_if_non_existent=False)
            for sm in self.synchronous_machines_powfacpy
        ]

    @cached_property
    def pss(self) -> list[ElmDsl]:
        """Get power system stabilizers (PSS)"""
        return [
            sm.get_pss(error_if_non_existent=False)
            for sm in self.synchronous_machines_powfacpy
        ]

    def get_governor_info(
        self,
        average: str | None = "apparent_power_weighted",
    ) -> None:
        return get_dsl_models_info_sorted_by_block_definition(
            self.governors,
            parent_elms=self.synchronous_machines,
            average=average,
        )

    def get_avr_info(
        self,
        average: str | None = "apparent_power_weighted",
    ) -> None:
        return get_dsl_models_info_sorted_by_block_definition(
            self.avrs,
            parent_elms=self.synchronous_machines,
            average=average,
        )

    def get_pss_info(
        self,
        average: str | None = "apparent_power_weighted",
    ) -> None:
        return get_dsl_models_info_sorted_by_block_definition(
            self.pss,
            parent_elms=self.synchronous_machines,
            average=average,
        )

    def export_info_to_csv(self, path: str) -> None:
        export_dsl_model_info_to_csv(self.get_governor_info(), f"{path}/governors")
        export_dsl_model_info_to_csv(self.get_avr_info(), f"{path}/avrs")
        export_dsl_model_info_to_csv(self.get_pss_info(), f"{path}/pss")


class SubSystemDynamics:
    """Dynamics-related aggregate quantities of a subsystem: inertia, power
    margins, load / generation - relevant e.g. for frequency stability and
    intentional islanding.

    Inertia is collected per dynamic unit: directly from the type for
    synchronous machines (`ElmSym`), and - for grid-forming converters
    (`ElmGenstat` / `ElmVsc` / `ElmPvsys` with a grid-forming control) - via
    `powfacpy.template_models` (the controller's template is identified and its
    `get_kinetic_energy_MWs` used). Converters whose template is not recognised
    are reported with `inertia_MWs = NaN`.
    """

    NOMINAL_FREQUENCY_HZ = 50.0

    def __init__(self, parent: SubSystem) -> None:
        self.parent = parent

    # ------------------------------------------------------------------ #
    # inertia
    # ------------------------------------------------------------------ #
    @cached_property
    def _synchronous_machine_rows(self) -> list[dict]:
        rows = []
        for sm in self.parent.dynamic_models.synchronous_machines.synchronous_machines_powfacpy:
            s = sm.ratedS
            h = sm.get_H_in_seconds()
            rows.append(
                {
                    "name": sm._obj.loc_name,
                    "class": "ElmSym",
                    "S_MVA": s,
                    "H_s": h,
                    "inertia_MWs": h * s,
                    "grid_forming": True,
                    "template": "ElmSym/TypSym",
                }
            )
        return rows

    @cached_property
    def _converter_rows(self) -> list[dict]:
        from powfacpy.template_models import TemplateMatcher

        matcher = TemplateMatcher(app=self.parent.app)
        rows = []
        for conv in self.parent.get_grid_forming_converters():
            composite_model = (
                conv.c_pmod if conv.HasAttribute("c_pmod") else None
            )
            row = {
                "name": conv.loc_name,
                "class": conv.GetClassName(),
                "S_MVA": conv.GetAttribute("sgn")
                if conv.HasAttribute("sgn")
                else np.nan,
                "H_s": np.nan,
                "inertia_MWs": np.nan,
                "grid_forming": True,
                "template": None,
            }
            if composite_model is not None:
                match = matcher.identify(composite_model)
                model = match.build(network_element=conv)
                if model is not None:
                    row["template"] = type(model).__name__
                    row["H_s"] = model.get_equivalent_inertia_constant()
                    row["inertia_MWs"] = model.get_kinetic_energy_MWs()
                elif match.library_template_paths:
                    # template recognised but no powfacpy class -> no inertia
                    row["template"] = match.library_template_paths[0]
            rows.append(row)
        return rows

    def get_inertia_details(self) -> pd.DataFrame:
        """Per-unit inertia table (synchronous machines and grid-forming converters)."""
        rows = self._synchronous_machine_rows + self._converter_rows
        return pd.DataFrame(
            rows,
            columns=[
                "name",
                "class",
                "S_MVA",
                "H_s",
                "inertia_MWs",
                "grid_forming",
                "template",
            ],
        )

    def synchronous_machine_inertia_MWs(self) -> float:
        return float(np.nansum([r["inertia_MWs"] for r in self._synchronous_machine_rows]))

    def converter_inertia_MWs(self) -> float:
        return float(np.nansum([r["inertia_MWs"] for r in self._converter_rows]))

    def total_inertia_MWs(self) -> float:
        """Total stored kinetic energy [MW s] (synchronous + grid-forming converter)."""
        return self.synchronous_machine_inertia_MWs() + self.converter_inertia_MWs()

    def inertia_constant_on_base(self, base_MVA: float) -> float:
        """System inertia constant `H = sum(H_i * S_i) / base_MVA` [s]."""
        return self.total_inertia_MWs() / base_MVA

    # ------------------------------------------------------------------ #
    # summary
    # ------------------------------------------------------------------ #
    def get_state(
        self, execute_load_flow: bool = True, format: str | None = "pandas"
    ) -> pd.DataFrame | dict | None:
        """Single-row summary of the subsystem's dynamics state (inertia,
        margins, load / generation)."""
        load_flow = self.parent.get_load_flow_state(
            execute_load_flow=execute_load_flow, format="dict"
        )
        total_generation = load_flow["total_power_generation"].real
        state = {
            "total_load_MW": load_flow["total_power_loads"].real,
            "total_generation_MW": total_generation,
            "power_exchange_MW": load_flow["total_power_exchange"].real,
            "synchronous_inertia_MWs": self.synchronous_machine_inertia_MWs(),
            "converter_inertia_MWs": self.converter_inertia_MWs(),
            "total_inertia_MWs": self.total_inertia_MWs(),
            "inertia_constant_on_generation_s": (
                self.total_inertia_MWs() / total_generation
                if total_generation
                else np.nan
            ),
            "upward_power_margin_MW": self.parent.load_flow.upward_power_margin_MW(
                execute_load_flow=False
            ),
            "downward_power_margin_MW": self.parent.load_flow.downward_power_margin_MW(
                execute_load_flow=False
            ),
        }
        if format == "dict":
            return state
        if format == "pandas":
            return pd.DataFrame(state, index=[self.parent.name])
        return None
