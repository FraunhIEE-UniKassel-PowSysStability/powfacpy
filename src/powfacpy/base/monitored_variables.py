"""Manage the monitored variables / contents of a PowerFactory results object (`ElmRes`).

This is one of the composed helpers `ActiveProject` delegates to (see the
`ActiveProject.monitored_variables` property). The corresponding `ActiveProject`
methods (`add_results_variable`, `clear_results_variables`, ...) stay as thin
forwarders so the public API is unchanged.

Not to be confused with `powfacpy.result_variables` (the `ResVar` enums of
result-variable name strings).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from powfacpy.pf_classes.protocols import ElmRes, IntMon, PFGeneral

if TYPE_CHECKING:
    from powfacpy.base.active_project import ActiveProject


class MonitoredVariables:
    """Add/remove monitored variables and clear results objects (`ElmRes`)."""

    def __init__(self, active_project: "ActiveProject") -> None:
        self._act_prj = active_project

    def _resolve_results_obj(self, results_obj: ElmRes | str | None) -> ElmRes:
        """Default to the `ElmRes` of the active study case; otherwise resolve the input."""
        if results_obj is None:
            return self._act_prj.get_from_study_case("ElmRes")
        return self._act_prj._handle_single_pf_object_or_path_input(results_obj)

    def add(
        self,
        obj: PFGeneral | str | list[PFGeneral | str],
        variables: str | list[str],
        results_obj: ElmRes | None = None,
    ) -> ElmRes:
        """Add variable(s) of `obj` to the monitored variables of a results object.

        Args:
            obj: PF object(s) or path(s).
            variables: variable name(s).
            results_obj: results object. Defaults to None (`ElmRes` of the active study case).

        Returns:
            ElmRes: the results object.
        """
        results_obj = self._resolve_results_obj(results_obj)
        obj = self._act_prj._handle_pf_object_or_path_input(obj)
        if isinstance(variables, str):
            variables = [variables]
        for o in obj:
            for var in variables:
                results_obj.AddVariable(o, var)
        results_obj.Load()
        return results_obj

    def clear(self, results_obj: ElmRes | None = None) -> None:
        """Delete all variable selection objects (`IntMon`) from a results object."""
        results_obj = self._resolve_results_obj(results_obj)
        for intmon in results_obj.GetContents("*.IntMon"):
            intmon.Delete()

    def add_variable_selection_obj(
        self,
        name: str,
        results_obj: ElmRes,
        class_name: str | None = None,
        variables: list[str] | None = None,
    ) -> IntMon:
        """Add a variable selection object (`IntMon`) to a results object (`ElmRes`).

        Args:
            name: name of the `IntMon`.
            results_obj: results object.
            class_name: `classnm` parameter of the `IntMon`. Defaults to None.
            variables: `vars` parameter of the `IntMon`. Defaults to None.

        Returns:
            IntMon: variable selection object.
        """
        variable_selection_obj: IntMon = self._act_prj.create_in_folder(
            name + ".IntMon", results_obj
        )
        if class_name:
            variable_selection_obj.classnm = class_name
        if variables:
            variable_selection_obj.vars = variables
        return variable_selection_obj

    def clear_elmres(self, results_obj: ElmRes | None = None) -> None:
        """Clear all contents of a results object (`ElmRes`)."""
        results_obj = self._resolve_results_obj(results_obj)
        self._act_prj.clear_folder(results_obj)

    def clear_elmres_from_deleted_objects(
        self, results_obj: ElmRes | None = None
    ) -> None:
        """Delete entries of a results object whose referenced object (`obj_id`) is deleted."""
        results_obj = self._resolve_results_obj(results_obj)
        for entry in results_obj.GetContents("*"):
            if entry.obj_id.IsDeleted():
                entry.Delete()
