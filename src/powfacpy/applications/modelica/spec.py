"""Modelica model description: `ModelicaVariable`, `ModelicaModelSpec` and the parser that reads a `.mo` file into a spec.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from pathlib import Path

from powfacpy.applications.modelica._codegen import (
    _declare,
    _flatten_equations,
    _split_array_literal,
    _split_top_level,
)


BASE_TYPES = ("Real", "Integer", "Boolean")


VARIABILITIES = ("inherited", "continuous", "discrete")


_BASE_TYPE_CODE = {name: i for i, name in enumerate(BASE_TYPES)}


_VARIABILITY_CODE = {name: i for i, name in enumerate(VARIABILITIES)}


_BASE_TYPE_NAME = {i: name for name, i in _BASE_TYPE_CODE.items()}


_VARIABILITY_NAME = {i: name for name, i in _VARIABILITY_CODE.items()}


# TypMdl.modMethod
_METHOD_CODE = {"hybrid": 0, "clocked": 1}


_METHOD_NAME = {0: "hybrid", 1: "clocked"}


@dataclass
class ModelicaVariable:
    """One declared variable of a Modelica model.

    `base_type` is Real | Integer | Boolean. `variability` (inputs/outputs only) is continuous | discrete | inherited. `size` is "" for a scalar or e.g. "n" / "[n]" / "3" for a vector (n may be an Integer parameter name). `default` is used for parameters, `start` for inputs/outputs/states/internals.
    """

    name: str
    base_type: str = "Real"
    variability: str = "continuous"
    size: str = ""
    unit: str = ""
    description: str = ""
    start: str = ""
    default: str = ""
    minimum: str = ""
    maximum: str = ""

    @property
    def is_array(self) -> bool:
        return bool(self.size.strip().strip("[]").strip())

    def array_length(self, int_params: dict[str, int]) -> int:
        token = self.size.strip().strip("[]").strip()
        if not token:
            return 1
        if token.isdigit():
            return int(token)
        if token in int_params:
            return int_params[token]
        raise ValueError(
            f"cannot resolve array size {self.size!r} of {self.name!r} - "
            f"give an integer or an Integer parameter with a default value"
        )


@dataclass
class ModelicaModelSpec:
    """A backend-agnostic description of a Modelica model.

    Maps 1:1 onto the fields of a PowerFactory `TypMdl`: `inputs` / `outputs` / `parameters` / `states` / `internals` are the declaration tables, and for the Hybrid method (`method="hybrid"`, the default) `init_equations` / `equations` are the initial- and dynamic-equation sections, while for the Clocked method (`method="clocked"`) they are the initial- and dynamic-algorithm (statement) sections. Each entry of `init_equations` / `equations` is one line of source.

    Three ways to obtain one: `ModelicaModelSpec.from_modelica(path_or_text)` (best-effort parse of a single-model `.mo` file); construct it directly in Python (see the tutorial - the way to go for anything the parser cannot handle); or `ModelicaModel(app).read_model_type(typ)` (reconstruct it from an existing `TypMdl`).

    `to_modelica()` renders it back to a standalone `.mo` string; `flattened()` returns an equivalent spec with arrays and `for` loops expanded (needed before creating a `TypMdl`, done automatically by `create_model_type`).
    """

    name: str
    method: str = "hybrid"
    inputs: list[ModelicaVariable] = field(default_factory=list)
    outputs: list[ModelicaVariable] = field(default_factory=list)
    parameters: list[ModelicaVariable] = field(default_factory=list)
    states: list[ModelicaVariable] = field(default_factory=list)
    internals: list[ModelicaVariable] = field(default_factory=list)
    init_equations: list[str] = field(default_factory=list)
    equations: list[str] = field(default_factory=list)
    description: str = ""
    author: str = ""

    # ---- introspection ------------------------------------------------- #
    @property
    def all_variables(self) -> list[ModelicaVariable]:
        return [
            *self.inputs,
            *self.outputs,
            *self.parameters,
            *self.states,
            *self.internals,
        ]

    def integer_parameter_values(self) -> dict[str, int]:
        """{name: int(default)} for every Integer parameter that has an integer default - used to resolve array sizes and `for` ranges."""
        out: dict[str, int] = {}
        for p in self.parameters:
            if p.base_type == "Integer" and p.default.strip().lstrip("-").isdigit():
                out[p.name] = int(p.default.strip())
        return out

    # ---- transforms -------------------------------------------------- #
    def flattened(self) -> "ModelicaModelSpec":
        """Return an equivalent spec with no arrays and no `for` loops.

        Array variables `x[n]` become scalars `x_1 ... x_n`; `x[k]` in equations becomes `x_k`; `for i in a:b loop ... end for;` is unrolled; `sum(x)` over a known array becomes `(x_1 + ... + x_n)`. Integer array-size parameters are kept (harmless) but their array uses are resolved.

        Best effort: it handles the constructs typical of relay / controller models (scalar-indexed 1-D arrays, integer ranges). Nested indexing, 2-D arrays and `for` with non-integer ranges are not supported - keep those scalar in the source, or build the `TypMdl` from an already-flat spec.
        """
        sizes = self.integer_parameter_values()

        def expand(vars_: list[ModelicaVariable]) -> list[ModelicaVariable]:
            out: list[ModelicaVariable] = []
            for v in vars_:
                if not v.is_array:
                    out.append(v)
                    continue
                n = v.array_length(sizes)
                defaults = _split_array_literal(v.default, n)
                starts = _split_array_literal(v.start, n)
                for k in range(1, n + 1):
                    out.append(
                        replace(
                            v,
                            name=f"{v.name}_{k}",
                            size="",
                            default=defaults[k - 1],
                            start=starts[k - 1],
                            description=(f"{v.description} [{k}]" if v.description else ""),
                        )
                    )
            return out

        array_names = {v.name for v in self.all_variables if v.is_array}
        array_lengths = {
            v.name: v.array_length(sizes) for v in self.all_variables if v.is_array
        }
        return ModelicaModelSpec(
            name=self.name,
            method=self.method,
            inputs=expand(self.inputs),
            outputs=expand(self.outputs),
            parameters=expand(self.parameters),
            states=expand(self.states),
            internals=expand(self.internals),
            init_equations=_flatten_equations(
                self.init_equations, sizes, array_names, array_lengths
            ),
            equations=_flatten_equations(
                self.equations, sizes, array_names, array_lengths
            ),
            description=self.description,
            author=self.author,
        )

    # ---- codegen ---------------------------------------------------- #
    def to_modelica(self) -> str:
        """Emit a standalone, standard-Modelica `.mo` source string."""
        lines = [f"model {self.name}"]
        if self.description:
            lines[0] += f' "{self.description}"'
        for p in self.parameters:
            lines.append("  " + _declare(p, prefix="parameter "))
        for v in self.inputs:
            lines.append("  " + _declare(v, prefix="input "))
        for v in self.outputs:
            lines.append("  " + _declare(v, prefix="output "))
        if self.states or self.internals:
            lines.append("protected")
            for v in (*self.states, *self.internals):
                lines.append("  " + _declare(v))
        if self.init_equations:
            kw = "initial equation" if self.method == "hybrid" else "initial algorithm"
            lines.append(kw)
            lines += [f"  {e}" for e in self.init_equations]
        kw = "equation" if self.method == "hybrid" else "algorithm"
        lines.append(kw)
        lines += [f"  {e}" for e in self.equations]
        lines.append(f"end {self.name};")
        return "\n".join(lines) + "\n"

    # ---- parsing --------------------------------------------------- #
    @classmethod
    def from_modelica(cls, source: str | Path) -> "ModelicaModelSpec":
        """Best-effort parse of a single-model `.mo` file (path or text).

        Understands `model NAME "desc"` ... `end NAME;`, one declaration per line (`[parameter|input|output] Type name[size] [= default] ["desc"]` with optional `(unit=..., start=..., min=..., max=...)` modifiers), a `protected` section (a variable is a state if `der(<name>)` appears in the equations, otherwise an internal variable), and `initial equation` / `equation` / `initial algorithm` / `algorithm` sections. It does not evaluate expressions or handle multi-line declarations - for anything exotic, build the spec directly.
        """
        text = Path(source).read_text() if _looks_like_path(source) else str(source)
        return _parse_modelica(text)


def _first(value) -> str:
    if isinstance(value, (list, tuple)):
        return value[0] if value else ""
    return value or ""


def _looks_like_path(source) -> bool:
    if isinstance(source, Path):
        return True
    return isinstance(source, str) and "\n" not in source and source.strip().endswith(".mo")


_MODEL_RE = re.compile(r'^\s*(?:model|block|class)\s+(\w+)\s*(?:"([^"]*)")?')


_DECL_RE = re.compile(
    r"""^\s*
    (?P<prefixes>(?:parameter\s+|input\s+|output\s+|constant\s+|discrete\s+|flow\s+|each\s+)*)
    (?P<type>Real|Integer|Boolean)\s+
    (?P<name>\w+)
    (?:\s*\[\s*(?P<size>[^\]]+)\s*\])?
    (?:\s*\(\s*(?P<mods>[^)]*)\s*\))?
    (?:\s*=\s*(?P<default>[^";]+?))?
    (?:\s*"(?P<desc>[^"]*)")?
    \s*;\s*$
    """,
    re.VERBOSE,
)


_SECTION_KEYWORDS = {
    "protected": "protected",
    "public": "public",
    "initial equation": "init_eq",
    "initial algorithm": "init_eq",
    "equation": "eq",
    "algorithm": "eq",
}


def _parse_modelica(text: str) -> ModelicaModelSpec:
    spec = ModelicaModelSpec(name="Model")
    section = "decl"
    visibility = "public"
    method = "hybrid"
    protected_vars: list[ModelicaVariable] = []

    for raw in text.splitlines():
        line = raw.split("//", 1)[0].rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        m = _MODEL_RE.match(line)
        if m and section == "decl":
            spec.name = m.group(1)
            spec.description = m.group(2) or ""
            continue
        end_m = re.match(r"^\s*end\s+(\w+)\s*;\s*$", line)
        if end_m and end_m.group(1) not in ("when", "for", "if", "while"):
            break  # end of the model (`end <ModelName>;`)

        low = stripped.lower()
        if low in _SECTION_KEYWORDS:
            tag = _SECTION_KEYWORDS[low]
            if tag == "protected":
                visibility = "protected"
                section = "decl"
            elif tag == "public":
                visibility = "public"
                section = "decl"
            else:
                section = tag
                if "algorithm" in low:
                    method = "clocked"
            continue

        if section in ("init_eq", "eq"):
            (spec.init_equations if section == "init_eq" else spec.equations).append(stripped)
            continue

        d = _DECL_RE.match(line)
        if not d:
            continue
        prefixes = d.group("prefixes") or ""
        mods = _parse_modifiers(d.group("mods") or "")
        var = ModelicaVariable(
            name=d.group("name"),
            base_type=d.group("type"),
            size=(d.group("size") or "").strip(),
            unit=mods.get("unit", ""),
            description=d.group("desc") or "",
            start=mods.get("start", ""),
            default=(d.group("default") or "").strip(),
            minimum=mods.get("min", ""),
            maximum=mods.get("max", ""),
        )
        if "parameter" in prefixes:
            spec.parameters.append(var)
        elif "input" in prefixes:
            var.variability = "continuous"
            spec.inputs.append(var)
        elif "output" in prefixes:
            var.variability = "continuous"
            spec.outputs.append(var)
        elif visibility == "protected":
            protected_vars.append(var)

    # protected variable is a state if der(name) appears in the equations, else internal
    equation_text = " ".join(spec.equations)
    for var in protected_vars:
        if re.search(rf"\bder\(\s*{re.escape(var.name)}\b", equation_text):
            spec.states.append(var)
        else:
            spec.internals.append(var)
    spec.method = method
    return spec


def _parse_modifiers(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in _split_top_level(text):
        if "=" in part:
            k, _, v = part.partition("=")
            out[k.strip()] = v.strip().strip('"')
    return out
