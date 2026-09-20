"""`ModelicaModel`: builds and compiles a PowerFactory Modelica model type (`TypMdl`) from a spec or a `.mo` file.
"""

from __future__ import annotations

from warnings import warn

from powfacpy.applications.application_base import ApplicationBase
from powfacpy.pf_classes.protocols import ElmMdl, PFApp, PFGeneral, TypMdl
from powfacpy.exceptions import PFModelicaCompilationError
from powfacpy.applications.modelica.spec import (
    ModelicaModelSpec,
    ModelicaVariable,
    _BASE_TYPE_CODE,
    _BASE_TYPE_NAME,
    _METHOD_CODE,
    _METHOD_NAME,
    _VARIABILITY_CODE,
    _VARIABILITY_NAME,
    _first,
)


class ModelicaModel(ApplicationBase):
    """Create, compile and read back PowerFactory Modelica model types ('TypMdl') and their instances ('ElmMdl').

    This is the PowerFactory-facing half of the module (see the module docstring for the full picture). Give `create_model_type` a `ModelicaModelSpec` - from a parsed `.mo` file or built in Python - and it writes every declaration column and equation field of a new `TypMdl` and compiles it, raising `PFModelicaCompilationError` (with the PowerFactory output-window messages) if `Check()` or `Compile()` fails. `create_model` then instantiates it as an `ElmMdl`, and `read_model_type` goes the other way, turning an existing `TypMdl` back into a `ModelicaModelSpec`.

    Needs an active project; the `TypMdl` is created in that project's dynamic-models library folder (`get_dynamic_models_folder`) by default.
    """

    def __init__(
        self, pf_app: PFApp | None | bool = False, cached: bool = False
    ) -> None:
        super().__init__(pf_app, cached)

    # ---- folders ---------------------------------------------------- #
    def get_dynamic_models_folder(self) -> PFGeneral:
        """The project's dynamic-models library folder (`app.GetProjectFolder("blk")`). Its display name varies by project / language ('Dynamic Models', 'User Defined Models', ...); TypMdl objects can only be created here or in a subfolder of it."""
        folder = self.app.GetProjectFolder("blk")
        if folder is None:
            raise FileNotFoundError(
                "the active project has no dynamic-models folder "
                "(app.GetProjectFolder('blk') returned None)"
            )
        return folder

    # ---- model type ----------------------------------------------- #
    def create_model_type(
        self,
        spec: ModelicaModelSpec,
        folder: PFGeneral | str | None = None,
        *,
        flatten: bool = True,
        compile: bool = True,
        overwrite: bool = True,
    ) -> TypMdl:
        """Create the `TypMdl` for `spec` and (optionally) compile it.

        This is the step that turns a parsed `.mo` file (or a hand-built spec) into a usable PowerFactory Modelica model type: it creates the `TypMdl`, sets `modMethod`, fills the input / output / parameter / state / internal declaration tables and the equation (or algorithm) fields, then runs `Check()` and `Compile()`.

        Args:
            spec: the model description.
            folder: target folder (must be 'Dynamic Models' or a subfolder); defaults to `get_dynamic_models_folder()`.
            flatten: apply `spec.flattened()` first (unroll for-loops / arrays). Leave True unless the spec is already scalar-only.
            compile: run `TypMdl.Compile()` and raise `PFModelicaCompilationError` on failure. If False, only `Check()` is run.
            overwrite: replace an existing TypMdl of the same name in `folder`.

        Returns:
            TypMdl: the created (and compiled) model type.
        """
        if flatten:
            spec = spec.flattened()
        folder = (
            self.get_dynamic_models_folder()
            if folder is None
            else self.act_prj._handle_single_pf_object_or_path_input(folder)
        )
        if overwrite:
            self.act_prj.delete_obj(
                f"{spec.name}.TypMdl", parent_folder=folder, error_if_non_existent=False
            )
        typ: TypMdl = folder.CreateObject("TypMdl", spec.name)
        if typ is None:
            raise RuntimeError(
                f"PowerFactory refused to create '{spec.name}.TypMdl' in "
                f"'{self.act_prj.get_path_of_object(folder)}' - "
                f"the folder must be 'Dynamic Models' or a subfolder of it"
            )

        typ.SetAttribute("modMethod", _METHOD_CODE[spec.method])
        if spec.description:
            typ.SetAttribute("desc", [spec.description])
        if spec.author:
            typ.SetAttribute("author", spec.author)

        self._write_variable_table(typ, "input", spec.inputs, with_variability=True)
        self._write_variable_table(typ, "output", spec.outputs, with_variability=True)
        self._write_variable_table(typ, "param", spec.parameters, value_field="default")
        self._write_variable_table(typ, "state", spec.states, value_field="start")
        self._write_variable_table(typ, "inter", spec.internals, value_field="start")

        if spec.method == "hybrid":
            typ.SetAttribute("initEquation", list(spec.init_equations))
            typ.SetAttribute("equation", list(spec.equations))
        else:
            typ.SetAttribute("initAlgorithm", list(spec.init_equations))
            typ.SetAttribute("algorithm", list(spec.equations))

        self._check_or_compile(typ, spec.name, compile)
        return typ

    def _write_variable_table(
        self,
        typ: TypMdl,
        prefix: str,
        variables: list[ModelicaVariable],
        *,
        with_variability: bool = False,
        value_field: str = "start",
    ) -> None:
        """Write one declaration table of a TypMdl.

        String columns (name/unit/description/size + default|start) are set as whole lists; the numeric-enum columns (base type, variability) must be set element by element (`SetAttribute("inputType:0", 0)`), whole-list writes to them are silently ignored by PowerFactory.
        """
        if not variables:
            return
        typ.SetAttribute(f"{prefix}Name", [v.name for v in variables])
        typ.SetAttribute(f"{prefix}Unit", [v.unit for v in variables])
        typ.SetAttribute(f"{prefix}Desc", [v.description for v in variables])
        typ.SetAttribute(f"{prefix}Size", [v.size for v in variables])
        typ.SetAttribute(f"{prefix}Min", [v.minimum for v in variables])
        typ.SetAttribute(f"{prefix}Max", [v.maximum for v in variables])
        value_attr = "paramDefault" if prefix == "param" else f"{prefix}Start"
        typ.SetAttribute(
            value_attr, [getattr(v, "default" if prefix == "param" else "start") for v in variables]
        )
        for i, v in enumerate(variables):
            typ.SetAttribute(f"{prefix}Type:{i}", _BASE_TYPE_CODE[v.base_type])
            if with_variability:
                typ.SetAttribute(
                    f"{prefix}Variability:{i}", _VARIABILITY_CODE[v.variability]
                )

    def _check_or_compile(self, typ: TypMdl, name: str, compile: bool) -> None:
        self.app.ClearOutputWindow()
        if typ.Check() != 0:
            raise PFModelicaCompilationError(name, self._output_window_messages())
        if not compile:
            return
        self.app.ClearOutputWindow()
        # second arg overrideModel=1: replace an already compiled model at the same location
        if typ.Compile("", 1) != 0:
            raise PFModelicaCompilationError(name, self._output_window_messages())

    def _output_window_messages(self) -> list[str]:
        try:
            content = self.app.GetOutputWindow().GetContent()
        except Exception:
            return []
        return [str(line).replace("\n", " ") for line in content]

    # ---- model instance ----------------------------------------- #
    def create_model(
        self,
        model_type: TypMdl | str,
        parent_folder: PFGeneral | str | None = None,
        *,
        name: str | None = None,
        parameters: dict[str, float | int | bool] | None = None,
        overwrite: bool = True,
    ) -> ElmMdl:
        """Create a Modelica Model ('ElmMdl') instance referencing `model_type`.

        Args:
            model_type: the TypMdl (or its path).
            parent_folder: where to create the ElmMdl; defaults to the network data folder.
            name: instance name; defaults to the type name.
            parameters: `{param_name: value}` scalar parameter values to set on the instance. Setting these only works once PowerFactory has populated the instance's parameter list from the (compiled) type; a warning is issued for any name that cannot be set, and array parameters (which reference IntMat objects) are not handled here.
            overwrite: replace an existing ElmMdl of the same name.
        """
        model_type = self.act_prj._handle_single_pf_object_or_path_input(model_type)
        parent_folder = (
            self.act_prj.network_data_folder
            if parent_folder is None
            else self.act_prj._handle_single_pf_object_or_path_input(parent_folder)
        )
        name = name or model_type.loc_name
        if overwrite:
            self.act_prj.delete_obj(
                f"{name}.ElmMdl",
                parent_folder=parent_folder,
                error_if_non_existent=False,
            )
        model: ElmMdl = parent_folder.CreateObject("ElmMdl", name)
        model.SetAttribute("typ_id", model_type)
        unset = []
        for param_name, value in (parameters or {}).items():
            try:
                if not model.HasAttribute(param_name):
                    raise AttributeError(param_name)
                model.SetAttribute(param_name, value)
            except Exception:
                unset.append(param_name)
        if unset:
            warn(
                f"could not set parameter(s) {unset} on '{name}' - open the model dialog "
                f"once or set them after the type's parameter list is populated",
                stacklevel=2,
            )
        return model

    # ---- read back --------------------------------------------- #
    def read_model_type(self, model_type: TypMdl | str) -> ModelicaModelSpec:
        """Reconstruct a `ModelicaModelSpec` from an existing `TypMdl` (the editable declarations, not the compiled cache)."""
        typ = self.act_prj._handle_single_pf_object_or_path_input(model_type)
        method = _METHOD_NAME.get(int(typ.GetAttribute("modMethod")), "hybrid")

        def read_table(prefix: str, has_variability: bool, value_field: str) -> list:
            names = typ.GetAttribute(f"{prefix}Name") or []
            units = typ.GetAttribute(f"{prefix}Unit") or []
            descs = typ.GetAttribute(f"{prefix}Desc") or []
            sizes = typ.GetAttribute(f"{prefix}Size") or []
            types = typ.GetAttribute(f"{prefix}Type") or []
            varis = typ.GetAttribute(f"{prefix}Variability") or [] if has_variability else []
            values = (
                typ.GetAttribute("paramDefault" if prefix == "param" else f"{prefix}Start")
                or []
            )
            out = []
            for i, nm in enumerate(names):
                out.append(
                    ModelicaVariable(
                        name=nm,
                        base_type=_BASE_TYPE_NAME.get(int(types[i]) if i < len(types) else 0, "Real"),
                        variability=_VARIABILITY_NAME.get(
                            int(varis[i]) if i < len(varis) else 1, "continuous"
                        ),
                        size=sizes[i] if i < len(sizes) else "",
                        unit=units[i] if i < len(units) else "",
                        description=descs[i] if i < len(descs) else "",
                        **{
                            value_field: values[i] if i < len(values) else "",
                        },
                    )
                )
            return out

        init_attr, eq_attr = (
            ("initEquation", "equation")
            if method == "hybrid"
            else ("initAlgorithm", "algorithm")
        )
        return ModelicaModelSpec(
            name=typ.loc_name,
            method=method,
            inputs=read_table("input", True, "start"),
            outputs=read_table("output", True, "start"),
            parameters=read_table("param", False, "default"),
            states=read_table("state", False, "start"),
            internals=read_table("inter", False, "start"),
            init_equations=list(typ.GetAttribute(init_attr) or []),
            equations=list(typ.GetAttribute(eq_attr) or []),
            description=_first(typ.GetAttribute("desc")),
        )
