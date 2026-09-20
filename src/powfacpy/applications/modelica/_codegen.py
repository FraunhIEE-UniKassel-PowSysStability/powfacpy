"""Pure-Python helpers that turn a Modelica model description into text: variable declarations, array literals and `for`-loop unrolling of equations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from powfacpy.applications.modelica.spec import ModelicaVariable


def _declare(v: ModelicaVariable, prefix: str = "") -> str:
    is_parameter = prefix.startswith("parameter")
    decl = f"{prefix}{v.base_type} {v.name}"
    if v.is_array:
        decl += f"[{v.size.strip().strip('[]').strip()}]"
    mods = []
    if v.unit:
        mods.append(f'unit="{v.unit}"')
    if v.start and not is_parameter:
        mods.append(f"start={v.start}")
    if v.minimum:
        mods.append(f"min={v.minimum}")
    if v.maximum:
        mods.append(f"max={v.maximum}")
    if mods:
        decl += "(" + ", ".join(mods) + ")"
    if is_parameter and v.default:
        decl += f" = {v.default}"
    if v.description:
        decl += f' "{v.description}"'
    return decl + ";"


def _split_array_literal(literal: str, n: int) -> list[str]:
    """'{1, 2, 3}' -> ['1','2','3']; '' -> ['']*n; a scalar -> [scalar]*n."""
    literal = literal.strip()
    if not literal:
        return [""] * n
    if literal.startswith("{") and literal.endswith("}"):
        parts = _split_top_level(literal[1:-1])
        if len(parts) != n:
            raise ValueError(f"array literal {literal!r} has {len(parts)} entries, expected {n}")
        return [p.strip() for p in parts]
    return [literal] * n


def _split_top_level(s: str) -> list[str]:
    """Split on commas that are not inside braces/parens."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch in "{(":
            depth += 1
        elif ch in ")}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return parts


_FOR_RE = re.compile(r"^\s*for\s+(\w+)\s+in\s+([^:]+):([^:]+)\s+loop\s*$")


_END_FOR_RE = re.compile(r"^\s*end\s+for\s*;\s*$")


def _flatten_equations(
    lines: list[str],
    int_params: dict[str, int],
    array_names: set[str],
    array_lengths: dict[str, int],
) -> list[str]:
    """Unroll `for i in a:b loop ... end for;`, then rewrite `x[k]`/`sum(x)` for array names."""
    unrolled = _unroll_for_loops(lines, int_params)
    return [_rewrite_array_access(ln, array_names, array_lengths) for ln in unrolled]


def _unroll_for_loops(lines: list[str], int_params: dict[str, int]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        m = _FOR_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        var, lo_s, hi_s = m.group(1), m.group(2).strip(), m.group(3).strip()
        lo = int_params.get(lo_s, _int_or_none(lo_s))
        hi = int_params.get(hi_s, _int_or_none(hi_s))
        if lo is None or hi is None:
            raise ValueError(f"cannot unroll {lines[i].strip()!r} - range must be integers or Integer parameters")
        depth, body = 1, []
        i += 1
        while i < len(lines):
            if _FOR_RE.match(lines[i]):
                depth += 1
            elif _END_FOR_RE.match(lines[i]):
                depth -= 1
                if depth == 0:
                    i += 1
                    break
            body.append(lines[i])
            i += 1
        body = _unroll_for_loops(body, int_params)  # nested loops
        for k in range(lo, hi + 1):
            for bl in body:
                out.append(_substitute_index(bl, var, k))
    return out


def _substitute_index(line: str, var: str, value: int) -> str:
    return re.sub(rf"\b{re.escape(var)}\b", str(value), line)


def _rewrite_array_access(line: str, array_names: set[str], array_lengths: dict[str, int]) -> str:
    """`x[3]` -> `x_3` for known arrays; `sum(x)` -> `(x_1 + x_2 + ... + x_n)`."""

    def sum_repl(m: re.Match) -> str:
        name = m.group(1)
        if name not in array_lengths:
            return m.group(0)
        n = array_lengths[name]
        return "(" + " + ".join(f"{name}_{k}" for k in range(1, n + 1)) + ")"

    line = re.sub(r"\bsum\(\s*(\w+)\s*\)", sum_repl, line)

    def idx_repl(m: re.Match) -> str:
        name, idx = m.group(1), m.group(2).strip()
        if name in array_names and idx.lstrip("-").isdigit():
            return f"{name}_{idx}"
        return m.group(0)

    return re.sub(r"\b(\w+)\[\s*([^\]]+)\s*\]", idx_repl, line)


def _int_or_none(s: str) -> int | None:
    try:
        return int(s)
    except ValueError:
        return None
