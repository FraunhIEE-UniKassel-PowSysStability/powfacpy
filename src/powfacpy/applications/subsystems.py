from __future__ import annotations

from functools import cached_property
from collections.abc import Iterator

import numpy as np
import pandas as pd

from powfacpy.applications.application_base import ApplicationBase

from powfacpy.pf_classes.protocols import (
    ElmZone,
    ElmTerm,
    ElmLne,
    ElmDsl,
    ElmSecctrl,
    PFGeneral,
)
from powfacpy.exceptions import PFInterfaceError
from powfacpy.pf_classes.elm.sym import SynchronousMachine
from powfacpy.pf_classes.elm.dsl import (
    get_dsl_models_info_sorted_by_block_definition,
    export_dsl_model_info_to_csv,
)
from powfacpy.general_helpers import get_indices
from powfacpy.pf_classes.elm.grouping_types import ElmAreaOrZone, AreaOrZone
from powfacpy.pf_classes.elm.zone import Zone
from powfacpy.pf_classes.elm.area import Area


class SubSystem(Zone, ApplicationBase):
    """Subsystem of a larger power system. This is the grouping class of powfacpy to extend the functionality of zones and areas in PowerFactory."""

    @property
    def name(self) -> str:
        return self._obj.loc_name

    @cached_property
    def load_flow(self) -> SubSystemLoadFlow:
        return SubSystemLoadFlow(self)

    @cached_property
    def topology(self) -> SubSystemTopology:
        return SubSystemTopology(self)

    @cached_property
    def dynamic_models(self) -> SubSystemDynamicModels:
        return SubSystemDynamicModels(self)

    @cached_property
    def dynamics(self) -> SubSystemDynamics:
        """Inertia, power margins and load/generation of the subsystem."""
        return SubSystemDynamics(self)

    def __init__(self, grouping: ElmAreaOrZone, pf_app=False, cached=False) -> None:
        if grouping.GetClassName() == "ElmZone":
            Zone.__init__(self, grouping)
        else:
            Area.__init__(self, grouping)
        ApplicationBase.__init__(self, pf_app, cached)

    def __eq__(self, other) -> bool:
        return self._obj == other._obj

    def __hash__(self) -> int:
        return hash(self._obj)

    def get_load_flow_state(
        self, execute_load_flow: bool = True, format: str | None = "pandas"
    ):
        """Compute the load-flow state and return it in `format`.

        The results are also cached on `self.load_flow` (`total_power_loads`,
        `total_power_generation`, `total_power_exchange`).
        """
        return self.load_flow.get_load_flow_state(
            execute_load_flow=execute_load_flow, format=format
        )


class SubSystemLoadFlow:
    """Load (power) flow properties of subsystem.

    The `total_power_*` attributes are populated by `get_load_flow_state`.
    """

    def __init__(self, parent: SubSystem) -> None:
        self.parent = parent
        self.total_power_loads: complex | None = None
        self.total_power_generation: complex | None = None
        self.total_power_exchange: complex | None = None

    def get_load_flow_state(
        self, execute_load_flow: bool = True, format: str | None = "pandas"
    ) -> None:
        """Get load flow results of subsystem.

        Includes total load/generation, power exchange etc.

        Args:
            execute_load_flow (bool, optional): _description_. Defaults to True.
            format (str | None, optional): Format of the returned results. Options are 'pandas', 'dict' or None. Defaults to "pandas".
        """
        if execute_load_flow:
            self.parent.act_prj.execute_load_flow()
        self.total_power_loads = self.parent.load_flow_total_power_loads_in_MVA()
        self.total_power_generation = (
            self.parent.load_flow_total_power_generation_in_MVA()
        )
        self.total_power_exchange = self.parent.load_flow_total_power_exchange_in_MVA()
        if format is None:
            return None
        elif format == "pandas":
            return pd.DataFrame(
                {
                    "total_power_loads": self.total_power_loads,
                    "total_power_generation": self.total_power_generation,
                    "total_power_exchange": self.total_power_exchange,
                },
                index=[self.parent.name],
            )
        elif format == "dict":
            return {
                "total_power_loads": self.total_power_loads,
                "total_power_generation": self.total_power_generation,
                "total_power_exchange": self.total_power_exchange,
            }

    # ------------------------------------------------------------------ #
    # power margins
    # ------------------------------------------------------------------ #
    def _dispatchable_generators(self) -> list:
        return self.parent.get_internal_elms(
            lambda x: x.GetClassName()
            in ("ElmSym", "ElmGenstat", "ElmPvsys", "ElmVsc")
        )

    def get_power_margins(self, execute_load_flow: bool = True) -> pd.DataFrame:
        """Upward / downward active-power headroom [MW] per internal generator.

        `upward_margin = P_max - P`, `downward_margin = P - P_min`, where `P` is
        the load-flow active power and `P_max` / `P_min` are the operational
        limits configured on the element (`P_max` / `Pmax_uc`, `P_min` /
        `Pmin_uc`). The limits are only as meaningful as the model - a machine
        dispatched outside its configured limits yields a negative margin.

        Args:
            execute_load_flow: run a load flow first so `P` is up to date.

        Returns:
            pd.DataFrame: one row per generator with columns ``name``, ``class``,
            ``P_MW``, ``P_max_MW``, ``P_min_MW``, ``upward_margin_MW``,
            ``downward_margin_MW``.
        """
        if execute_load_flow:
            self.parent.act_prj.execute_load_flow()
        rows = []
        for gen in self._dispatchable_generators():
            p = _first_attr(gen, "m:P:bus1", "pgini", default=np.nan)
            p_max = _first_attr(gen, "P_max", "Pmax_uc", "Pmax", default=np.nan)
            p_min = _first_attr(gen, "P_min", "Pmin_uc", "Pmin", default=0.0)
            rows.append(
                {
                    "name": gen.loc_name,
                    "class": gen.GetClassName(),
                    "P_MW": p,
                    "P_max_MW": p_max,
                    "P_min_MW": p_min,
                    "upward_margin_MW": p_max - p,
                    "downward_margin_MW": p - p_min,
                }
            )
        return pd.DataFrame(
            rows,
            columns=[
                "name",
                "class",
                "P_MW",
                "P_max_MW",
                "P_min_MW",
                "upward_margin_MW",
                "downward_margin_MW",
            ],
        )

    # ------------------------------------------------------------------ #
    # secondary (power-frequency) control
    # ------------------------------------------------------------------ #
    #: 'iexchange' ("Exchange for") enum of `ElmSecctrl`: Grid / Boundary / Zone / Area
    _EXCHANGE_FOR = {"ElmZone": 2, "ElmArea": 3}

    def create_secondary_controller(
        self,
        name: str | None = None,
        parent_folder: PFGeneral | None = None,
        *,
        synchronous_machines: bool = False,
        batteries: bool = False,
        wind: bool = False,
        pv: bool = False,
        attr: dict | None = None,
    ) -> ElmSecctrl:
        """Create a secondary (power-frequency) controller (`ElmSecctrl`) for the subsystem.

        Thin wrapper around `StaticCalc.create_secondary_controller`. Set automatically so the controller regulates this subsystem's own interchange: `iexchange` ("Exchange for", -> "Zone" or "Area") and `pPmeas` ("Boundary/Zone/Area", -> the subsystem's grouping object). Everything else (`i_net`, `psetp`, `Kpf`, ...) is left at its PowerFactory default - configure it yourself or pass it via `attr`.

        The controlled machines (`psym`) are collected from the subsystem's internal units, one category per flag that is set.

        Args:
            name: `loc_name` of the controller. Defaults to ``"<subsystem> secondary controller"``.

            parent_folder: folder to create it in. Defaults to the `ElmNet` of the subsystem's first internal terminal.

            synchronous_machines: add the internal synchronous generators (`get_internal_sg`) to `psym`.

            batteries: add the internal battery storage units (`get_internal_bess`).

            wind: add the internal wind units (`get_internal_wind`).

            pv: add the internal PV units (`get_internal_pv`).

            attr: further attributes (name -> value) to set on the `ElmSecctrl`.

        Returns:
            ElmSecctrl: the created controller.
        """
        from powfacpy.applications.static_calc import StaticCalc

        subsystem = self.parent
        controlled: list[PFGeneral] = []
        if synchronous_machines:
            controlled += subsystem.get_internal_sg()
        if batteries:
            controlled += subsystem.get_internal_bess()
        if wind:
            controlled += subsystem.get_internal_wind()
        if pv:
            controlled += subsystem.get_internal_pv()

        if name is None:
            name = f"{subsystem.name} secondary controller"
        if parent_folder is None:
            parent_folder = self._grid_for_new_objects()

        attributes = {
            "iexchange": self._EXCHANGE_FOR[subsystem._obj.GetClassName()],
            "pPmeas": subsystem._obj,
        }
        if attr:
            attributes.update(attr)

        return StaticCalc(subsystem.app).create_secondary_controller(
            name=name,
            parent_folder=parent_folder,
            controlled_objs=controlled or None,
            attr=attributes,
        )

    def _grid_for_new_objects(self) -> PFGeneral:
        """The `ElmNet` to create subsystem-level objects in (grid of the first internal terminal)."""
        act_prj = self.parent.act_prj
        for terminal in self.parent.get_internal_elms_of_class("ElmTerm"):
            grid = act_prj.get_upstream_obj(
                terminal,
                lambda x: x.GetClassName() == "ElmNet",
                error_if_non_existent=False,
            )
            if grid is not None:
                return grid
        raise PFInterfaceError(
            f"Could not determine a grid for '{self.parent.name}'; pass "
            "'parent_folder' explicitly."
        )

    def upward_power_margin_MW(self, execute_load_flow: bool = True) -> float:
        """Total upward active-power headroom [MW] of the subsystem's generators."""
        return float(
            np.nansum(
                self.get_power_margins(execute_load_flow)["upward_margin_MW"]
            )
        )

    def downward_power_margin_MW(self, execute_load_flow: bool = True) -> float:
        """Total downward active-power headroom [MW] of the subsystem's generators."""
        return float(
            np.nansum(
                self.get_power_margins(execute_load_flow)["downward_margin_MW"]
            )
        )


class SubSystemTopology:

    @cached_property
    def terminals(self) -> list[ElmTerm]:
        return self.parent.get_internal_elms_of_class("ElmTerm")

    @cached_property
    def lines(self) -> list[ElmLne]:
        return self.parent.get_internal_elms_of_class("ElmLne")

    def __init__(self, parent: SubSystem) -> None:
        self.parent = parent

    def get_indices_of_terminals(self, terminals_superset: list[ElmTerm]) -> list[int]:
        """Get indices of the terminals inside the subsystem in a terminal superset (e.g. all terminals of the whole system).

        Args:
            terminals_superset (list[ElmTerm]): Superset of terminals

        Returns:
            list[int]: list of indices of the terminals inside the subsystem in the terminal superset
        """
        return get_indices(self.terminals, terminals_superset)

    def is_neighbor(self, grouping: ElmAreaOrZone | AreaOrZone | SubSystem) -> bool:
        """Check if another subsystem/grouping is physically connected to this subsystem (by calculating the power exchange).

        Args:
            grouping (ElmAreaOrZone | AreaOrZone | Subsystem): Potential neighboring subsystem/grouping

        Returns:
            bool: true if the other subsystem/grouping is a neighbor, false otherwise
        """
        if isinstance(grouping, SubSystem):
            grouping = grouping._obj
        return self.parent.is_neighbor(grouping)


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


def _first_attr(obj, *names: str, default=None):
    for name in names:
        if obj.HasAttribute(name):
            value = obj.GetAttribute(name)
            if value is not None:
                return value
    return default


class SubSystemContainer(ApplicationBase):
    """Container for multiple subsystems, e.g. to analyze the power exchange between them or find the branch elements (tie lines, tie transformers, couplers, ...) connecting them (`get_tie_branches`)."""

    @property
    def subsystems(self) -> list[SubSystem]:
        return self._subsystems

    @property
    def elm_zones(self) -> list[ElmZone]:
        # replace with pf grouping object
        return [subs._obj for subs in self._subsystems]

    @property
    def names(self) -> list[str]:
        return [subs._obj.loc_name for subs in self._subsystems]

    @property
    def num_subsystems(self) -> int:
        return len(self._subsystems)

    @property
    def power_exchange(self) -> pd.DataFrame:
        if self._power_exchange is None:
            self.get_power_exchange_in_MVA()
        return self._power_exchange

    @property
    def total_power_loads(self) -> np.ndarray:
        return np.array([subs.total_power_loads for subs in self._subsystems])

    @property
    def total_power_generation(self) -> np.ndarray:
        return np.array([subs.total_power_generation for subs in self._subsystems])

    def __init__(
        self, subsystems: list[SubSystem] | list[ElmZone], pf_app=False, cached=False
    ) -> None:
        super().__init__(pf_app, cached)
        if not isinstance(subsystems[0], SubSystem):
            subsystems = [SubSystem(subsys) for subsys in subsystems]
        self._subsystems = subsystems
        self._power_exchange: pd.DataFrame | None = None
        self._attributes_with_values_for_each_subsystem: list[str] = ["_subsystems"]
        self._attributes_depending_on_all_subsystems: list[str] = ["_power_exchange"]

    def __getitem__(self, key) -> SubSystem:
        return self._subsystems[key]

    def __iter__(self) -> Iterator[SubSystem]:
        return iter(self._subsystems)

    def __len__(self) -> None:
        return len(self._subsystems)

    def delete_subsystem(self, subsystem: int | SubSystem) -> None:
        """Delete subsystem from the container.

        Ensure that all attributes of the container that depend on the subsystems are updated/reset accordingly (e.g. power exchange matrix, total loads/generation etc.).

        Args:
            subsystem (int | SubSystem): subsystem or its index in the container to be deleted
        """
        subsystem = self._subsystem_input_to_index(subsystem)
        for attr in self._attributes_with_values_for_each_subsystem:
            val = self.__getattribute__(attr)
            if val is not None:
                if isinstance(val, np.ndarray):
                    val = np.delete(val, subsystem, axis=0)
                else:
                    del val[subsystem]
                self.__setattr__(attr, val)
        for attr in self._attributes_depending_on_all_subsystems:
            self.__setattr__(attr, None)

    def subsys_to_indices(self, subsys: list[SubSystem]) -> list[int]:
        """Get indices of subsystems.

        Args:
            subsys (list[SubSystem]): subsystems

        Returns:
            list[int]: Indices
        """
        return get_indices(subsys, self._subsystems)

    def get_index_of_subsystem(self, subsys: SubSystem) -> int:
        return self._subsystems.index(subsys)

    def get_power_exchange_in_MVA(
        self,
        execute_load_flow: bool = True,
        format: str = "dataframe",
        value_no_exchange=np.nan + 0j,
    ) -> np.typing.ArrayLike | pd.DataFrame:
        """Get power exchange between subsystems in MVA.

        Args:
            execute_load_flow (bool, optional): If true, execute load flow first to ensure that results are present. Defaults to True.
            format (str, optional): If "dataframe", return a pandas DataFrame; otherwise, return a numpy array. Defaults to "dataframe".
            value_no_exchange (_type_, optional): The value to use for no exchange between subsystems that are not connected. Defaults to np.nan+0j.

        Returns:
            np.array | pd.DataFrame: power exchange.
        """
        if execute_load_flow:
            self.act_prj.execute_load_flow()
        s_exchange = np.full(
            (self.num_subsystems, self.num_subsystems), value_no_exchange
        )
        for m, z1 in enumerate(self.elm_zones):
            for n, z2 in enumerate(self.elm_zones[m + 1 :]):
                if z1.CalculateInterchangeTo(z2) > 0:
                    s_exchange[m, m + n + 1] = z1.GetAttribute(
                        "c:Pinter"
                    ) + 1j * z1.GetAttribute("c:Qinter")
                    s_exchange[m + n + 1, m] = -s_exchange[m, m + n + 1]
        labels = self.names
        self._power_exchange = pd.DataFrame(s_exchange, index=labels, columns=labels)
        self._attributes_depending_on_all_subsystems.append("_power_exchange")
        if format == "dataframe":
            return self._power_exchange
        else:
            return s_exchange

    def get_neighboring_subsystems_in_container(
        self, subsystem: int | SubSystem | ElmZone
    ) -> list[SubSystem]:
        """Get neighbors of 'subsystem' in container.

        Args:
            subsystem (int | SubSystem): subsystem or its index in the container for which the neighbors should be found.

        Returns:
            list[SubSystem]: List of neighboring subsystems.
        """
        subsystem = self._handle_subsystem_input(subsystem)
        self.act_prj.check_load_flow_results(when_invalid="execute")
        return [
            self._subsystems[n]
            for n, subs in enumerate(self._subsystems)
            if not subs == subsystem
            and subsystem._obj.CalculateInterchangeTo(subs._obj) > 0
        ]

    # ------------------------------------------------------------------ #
    # tie branches (topological connections between subsystems)
    # ------------------------------------------------------------------ #
    #: highest cubicle index probed per element (3-winding transformers use
    #: 0-2; generous headroom beyond that in case of unusual multi-terminal
    #: elements).
    _MAX_CUBICLES_PER_ELEMENT = 10

    def get_tie_branches(
        self, element_classes: list[str] | None = None
    ) -> pd.DataFrame:
        """Branch elements connecting two or more subsystems in this container.

        An element qualifies if at least two of its cubicles (`GetCubicle`)
        are attached to terminals (`cterm`) that belong to *different*
        subsystems of this container. This works for any PowerFactory class
        with multiple connection points (`ElmLne`, `ElmTr2`, `ElmTr3`,
        `ElmCoup`, `ElmSind`, ...) without hardcoding branch class names -
        elements with a single cubicle (loads, generators, ...) can never
        qualify, so they are excluded automatically. Restrict the search to
        specific classes with `element_classes`, e.g. `["ElmLne"]` for tie
        *lines* only (see also `get_tie_lines`).

        This is purely topological - based on cubicle/terminal connectivity,
        not load-flow results - so out-of-service elements and zero-flow ties
        are still found. This differs from `is_neighbor` /
        `get_neighboring_subsystems_in_container`, which rely on
        `CalculateInterchangeTo` and therefore need a valid, non-zero power
        flow to detect a connection.

        Args:
            element_classes: restrict to these PowerFactory classes. Defaults
                to None (any class with multiple cubicles).

        Returns:
            pd.DataFrame with one row per tie element: ``element`` (the PF
            object), ``class``, ``name`` and ``subsystems`` (tuple of the
            >= 2 subsystem names it connects).
        """
        terminal_subsystem = self._terminal_to_subsystem_index()
        rows = []
        seen = set()
        for subsystem in self._subsystems:
            for terminal in subsystem.topology.terminals:
                for cubicle in terminal.GetConnectedCubicles():
                    elm = cubicle.obj_id
                    if elm is None or elm in seen:
                        continue
                    seen.add(elm)
                    if element_classes and elm.GetClassName() not in element_classes:
                        continue
                    subsystem_indices = self._connected_subsystem_indices(
                        elm, terminal_subsystem
                    )
                    if len(subsystem_indices) >= 2:
                        rows.append(
                            {
                                "element": elm,
                                "class": elm.GetClassName(),
                                "name": elm.loc_name,
                                "subsystems": tuple(
                                    self.names[i] for i in sorted(subsystem_indices)
                                ),
                            }
                        )
        return pd.DataFrame(rows, columns=["element", "class", "name", "subsystems"])

    def get_tie_lines(self) -> pd.DataFrame:
        """`get_tie_branches` restricted to AC lines (`ElmLne`)."""
        return self.get_tie_branches(element_classes=["ElmLne"])

    def get_tie_branches_between(
        self,
        subsystem_a: int | SubSystem | ElmZone,
        subsystem_b: int | SubSystem | ElmZone,
        element_classes: list[str] | None = None,
    ) -> list[PFGeneral]:
        """Branch elements directly tying `subsystem_a` to `subsystem_b`.

        Convenience filter over `get_tie_branches` for a single pair of
        subsystems.

        Args:
            subsystem_a / subsystem_b: subsystem, its index in the container,
                or its `ElmZone`/`ElmArea`.
            element_classes: restrict to these PowerFactory classes.

        Returns:
            list[PFGeneral]: the connecting elements.
        """
        name_a = self._handle_subsystem_input(subsystem_a).name
        name_b = self._handle_subsystem_input(subsystem_b).name
        ties = self.get_tie_branches(element_classes=element_classes)
        if ties.empty:
            return []
        mask = ties["subsystems"].apply(lambda s: name_a in s and name_b in s)
        return ties.loc[mask, "element"].tolist()

    def _terminal_to_subsystem_index(self) -> dict[ElmTerm, int]:
        """Map every internal terminal of every subsystem to its index in the container."""
        mapping = {}
        for i, subsystem in enumerate(self._subsystems):
            for terminal in subsystem.topology.terminals:
                mapping[terminal] = i
        return mapping

    def _connected_subsystem_indices(
        self, elm: PFGeneral, terminal_subsystem: dict[ElmTerm, int]
    ) -> set[int]:
        """Indices (in this container) of the subsystems `elm` is directly connected to, via its cubicles."""
        indices = set()
        for i in range(self._MAX_CUBICLES_PER_ELEMENT):
            cubicle = elm.GetCubicle(i)
            if cubicle is None:
                break
            subsystem_index = terminal_subsystem.get(cubicle.cterm)
            if subsystem_index is not None:
                indices.add(subsystem_index)
        return indices

    def get_load_flow_state(
        self,
        execute_load_flow: bool = True,
    ) -> pd.DataFrame:
        """Get load flow state of all subsystems in the container.

         Args:
            execute_load_flow (bool, optional): If true, execute load flow first to ensure that results are present. Defaults to True.

        Returns:
            pd.DataFrame: Load flow state of all subsystems in the container.
        """
        if execute_load_flow:
            self.act_prj.execute_load_flow()
        return pd.concat(
            [
                subs.get_load_flow_state(execute_load_flow=False, format="pandas")
                for subs in self._subsystems
            ],
            axis=0,
        )

    def export_synchronous_machines_info_to_csv(self, path: str) -> None:
        for subs in self._subsystems:
            subs.dynamic_models.synchronous_machines.export_info_to_csv(
                f"{path}/{subs.name}"
            )

    def _handle_subsystem_input(
        self, subsystem: int | SubSystem | ElmZone
    ) -> SubSystem:
        if not isinstance(subsystem, SubSystem):
            if isinstance(subsystem, int):
                subsystem = self._subsystems[subsystem]
            else:
                subsystem = SubSystem(subsystem)
        return subsystem

    def _subsystem_input_to_index(self, subsystem: int | SubSystem) -> int:
        """Get index of subsystem.

        Args:
            subsystem (int | SubSystem): Subsystem or its index in the container. If the index is provided, it is returned as is; if the subsystem is provided, its index in the container is returned.

        Returns:
            int: Index of the subsystem in the container.
        """
        if isinstance(subsystem, SubSystem):
            subsystem = self._subsystems.index(subsystem)
        return subsystem
