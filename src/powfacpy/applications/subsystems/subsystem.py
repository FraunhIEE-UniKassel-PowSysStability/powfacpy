"""`SubSystem`: the grouping class (a zone extended with helper objects) and its topology helper.
"""

from __future__ import annotations

from functools import cached_property

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_classes.protocols import ElmTerm, ElmLne
from powfacpy.general_helpers import get_indices
from powfacpy.pf_classes.elm.grouping_types import ElmAreaOrZone, AreaOrZone
from powfacpy.pf_classes.elm.zone import Zone
from powfacpy.pf_classes.elm.area import Area
from powfacpy.applications.subsystems.dynamics import SubSystemDynamicModels, SubSystemDynamics
from powfacpy.applications.subsystems.load_flow import SubSystemLoadFlow


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
