from __future__ import annotations

from functools import cached_property
from abc import ABC, abstractmethod
from collections.abc import Iterator


import numpy as np
import pandas as pd
from icecream import ic

from powfacpy.applications.application_base import ApplicationBase


from powfacpy.pf_class_protocols import ElmZone, ElmTerm, ElmLne
from powfacpy.pf_classes.elm.sym import SynchronousMachine
from powfacpy.pf_classes.elm.dsl import (
    get_dsl_models_info_sorted_by_block_definition,
    export_dsl_model_info_to_csv,
)
from powfacpy.general_helpers import get_indices
from powfacpy.pf_classes.elm.grouping_base import ElmAreaOrZone, AreaOrZone
from powfacpy.pf_classes.elm.zone import Zone
from powfacpy.pf_classes.elm.area import Area


class SubSystem(Zone, ApplicationBase):
    """Subsystem of a larger power system. This is the grouping class of powfacpy to extend the functionality of zones and areas in PowerFactory."""

    @property
    def name(self) -> str:
        return self._obj.loc_name

    @property
    def load_flow(self) -> SubSystemLoadFlow:
        if self._load_flow is None:
            self._load_flow = SubSystemLoadFlow(self)
        return self._load_flow

    @property
    def topology(self) -> SubSystemTopology:
        if self._topology is None:
            self._topology = SubSystemTopology(self)
        return self._topology

    @property
    def dynamic_models(self) -> SubSystemDynamicModels:
        if self._dynamic_models is None:
            self._dynamic_models = SubSystemDynamicModels(self)
        return self._dynamic_models

    def __init__(self, grouping: ElmAreaOrZone, pf_app=False, cached=False) -> None:
        class_name = grouping.GetClassName()
        if class_name == "ElmZone":
            super(SubSystem, self).__init__(grouping)
        else:
            Area.__init__(grouping, pf_app, cached)
        ApplicationBase.__init__(self, pf_app, cached)
        self._load_flow: SubSystemLoadFlow | None = None
        self._topology: SubSystemTopology | None = None
        self._dynamic_models: SubSystemDynamicModels | None = None

    def __eq__(self, other) -> bool:
        return self._obj == other._obj

    def __hash__(self) -> int:
        return hash(self._obj)

    def get_load_flow_state(
        self, execute_load_flow: bool = True, format: str | None = "pandas"
    ) -> SubSystemLoadFlow:
        self._load_flow: SubSystemLoadFlow = SubSystemLoadFlow(self)
        return self._load_flow.get_load_flow_state(
            execute_load_flow=execute_load_flow, format=format
        )


class SubSystemLoadFlow:
    """Load (power) flow properties of subsystem."""

    def __init__(self, parent: Subsystem) -> None:
        self.parent = parent
        self.total_power_loads: complex
        self.total_power_generation: complex
        self.total_power_exchange: complex

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


class SubSystemTopology:

    @cached_property
    def terminals(self) -> list[ElmTerm]:
        return self.parent.get_internal_elms_of_class("ElmTerm")

    @cached_property
    def lines(self) -> list[ElmLne]:
        return self.parent.get_internal_elms_of_class("ElmLne")

    def __init__(self, parent: Subsystem) -> None:
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

    @cached_property
    def synchronous_machines(self) -> SubSystemTopology:
        if self._synchronous_machines is None:
            self._synchronous_machines = SubSystemSynchronousMachines(self)
        return self._synchronous_machines

    def __init__(self, parent: Subsystem) -> None:
        self.parent = parent
        self._synchronous_machines: SubSystemSynchronousMachines | None = None


class SubSystemSynchronousMachines:
    """Synchronnous machines and their controllers in the subsystem."""

    @cached_property
    def root_subsystem(self) -> list[ElmTerm]:
        return self.parent.parent

    @cached_property
    def synchronous_machines(self) -> list[ElmTerm]:
        return self.root_subsystem.get_internal_elms_of_class("ElmSym")

    @cached_property
    def synchronous_machines_powfacpy(self) -> list[SynchronousMachine]:
        """Get synchronous machines as powfacpy objects."""
        return [SynchronousMachine(sm) for sm in self.synchronous_machines]

    @cached_property
    def governors(self) -> list[ElmTerm]:
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

    def __init__(self, parent: Subsystem) -> None:
        self.parent = parent

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


class SubSystemContainer(ApplicationBase):
    """Container for multiple subsystems, e.g. to analyze the power exchange between them."""

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
    ) -> np.array | pd.DataFrame:
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
