"""Python interfaces to PowerFactory dynamic-model templates.

Each concrete class wraps an *applied* dynamic unit (a composite model plus its
network element) that was built from a known template - from the global
DIgSILENT library or a user library - and exposes information that is otherwise
buried in the DSL controllers (e.g. the inertia of a grid-forming converter).

`powfacpy.template_models.matcher.TemplateMatcher` detects which template (if
any) a composite model in a grid corresponds to and returns the matching class.

Sub-packages mirror the folder structure of the source library, e.g.
`digsilent_library/grid_forming_converters/` <-> ``Templates\\Grid-forming Converters``.
"""

from powfacpy.template_models.base import TemplateModel, TEMPLATE_MODELS, register

# importing the concrete classes populates TEMPLATE_MODELS via @register
from powfacpy.template_models.digsilent_library import grid_forming_converters  # noqa: F401

from powfacpy.template_models.matcher import MatchResult, TemplateMatcher
from powfacpy.template_models.library_index import (
    LibraryTemplateIndex,
    LibraryTemplateMatch,
)

__all__ = [
    "TemplateModel",
    "TEMPLATE_MODELS",
    "register",
    "MatchResult",
    "TemplateMatcher",
    "LibraryTemplateIndex",
    "LibraryTemplateMatch",
]
