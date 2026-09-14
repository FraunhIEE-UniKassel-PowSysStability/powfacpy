"""Deprecated - import from `powfacpy.pf_classes.protocols` instead.

Kept only as a backwards-compatible re-export; nothing in powfacpy uses it.
"""

from warnings import warn as _warn

from powfacpy.pf_classes.protocols import *  # noqa: F401,F403

_warn(
    "'powfacpy.pf_class_protocols' is deprecated; "
    "import from 'powfacpy.pf_classes.protocols' instead.",
    DeprecationWarning,
    stacklevel=2,
)
