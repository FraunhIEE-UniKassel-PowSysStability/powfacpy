"""Type aliases for the grouping classes (Area / Zone).

These live in their own module rather than in `grouping_base.py` because
`grouping_base` defines `AreaZoneBase`, which `area.py` and `zone.py` use as a
base class - so `grouping_base` importing `Area` / `Zone` back would be a circular
import (and one that breaks when `area` / `zone` is the first module imported).
"""

from __future__ import annotations

from typing import TypeAlias

from powfacpy.pf_classes.protocols import ElmArea, ElmZone
from powfacpy.pf_classes.elm.area import Area
from powfacpy.pf_classes.elm.zone import Zone

#: an `ElmArea` or `ElmZone` (raw PowerFactory object)
ElmAreaOrZone: TypeAlias = ElmArea | ElmZone
#: an `Area` or `Zone` (powfacpy wrapper object)
AreaOrZone: TypeAlias = Area | Zone
