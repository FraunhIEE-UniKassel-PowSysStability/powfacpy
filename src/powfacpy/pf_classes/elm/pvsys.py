from __future__ import annotations

from powfacpy.pf_classes.protocols import ElmPvsys
from powfacpy.pf_classes.elm.elm_base import (
    ElmBase,
    SinglePortBase,
    ElmPlantControlledBase,
)


class PVSystem(ElmBase, SinglePortBase, ElmPlantControlledBase):
    """Wrapper for `ElmPvsys` (PV system).

    The dispatch, limit and rating helpers are provided by `SinglePortBase`; the plant-model helpers by `ElmPlantControlledBase`. Note `ElmPvsys` has no `cSubCategory` and its `mode_inp` field is labelled "Operating Point Reactive Power/Voltage: Input Mode".
    """

    __slots__ = ()

    def __init__(self, obj: ElmPvsys) -> None:
        super().__init__(obj)
        self._obj: ElmPvsys

    def __new__(cls, *args, **kwargs) -> ElmPvsys | PVSystem:
        """Implemented only to add type hints for the created instance."""
        instance = super().__new__(cls)
        return instance
