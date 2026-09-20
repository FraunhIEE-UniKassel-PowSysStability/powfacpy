"""Load flow quantities of a subsystem (`SubSystemLoadFlow`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import numpy as np
import pandas as pd

from powfacpy.pf_classes.protocols import ElmSecctrl, PFGeneral
from powfacpy.exceptions import PFInterfaceError

if TYPE_CHECKING:
    from powfacpy.applications.subsystems.subsystem import SubSystem


def _first_attr(obj, *names: str, default=None):
    for name in names:
        if obj.HasAttribute(name):
            value = obj.GetAttribute(name)
            if value is not None:
                return value
    return default


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
