"""`SubSystemContainer`: manages several subsystems of one project.
"""

from __future__ import annotations

from collections.abc import Iterator
import numpy as np
import pandas as pd

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_classes.protocols import ElmZone, ElmTerm, PFGeneral
from powfacpy.general_helpers import get_indices
from powfacpy.applications.subsystems.subsystem import SubSystem


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
