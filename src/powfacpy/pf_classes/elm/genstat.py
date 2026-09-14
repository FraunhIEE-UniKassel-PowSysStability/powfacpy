from __future__ import annotations

from powfacpy.pf_classes.protocols import ElmGenstat
from powfacpy.pf_classes.elm.elm_base import (
    ElmBase,
    SinglePortBase,
    ElmPlantControlledBase,
)


class StaticGenerator(ElmBase, SinglePortBase, ElmPlantControlledBase):
    """Wrapper for `ElmGenstat` (static generator).

    In PowerFactory `ElmGenstat` models non-synchronous units - PV, wind, battery storage, fuel cells, ... - distinguished by their plant category (`aCategory`). The dispatch, limit and rating helpers are provided by `SinglePortBase`; the plant-model helpers by `ElmPlantControlledBase`.
    """

    __slots__ = ()

    def __init__(self, obj: ElmGenstat) -> None:
        super().__init__(obj)
        self._obj: ElmGenstat

    def __new__(cls, *args, **kwargs) -> ElmGenstat | StaticGenerator:
        """Implemented only to add type hints for the created instance."""
        instance = super().__new__(cls)
        return instance
