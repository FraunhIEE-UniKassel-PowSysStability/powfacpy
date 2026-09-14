"""``Templates\\Grid-forming Converters`` - Python interfaces per template.

Importing this package registers every `TemplateModel` subclass below with
`powfacpy.template_models.base.TEMPLATE_MODELS`.
"""

from powfacpy.template_models.digsilent_library.grid_forming_converters._base import (
    GridFormingConverter,
)
from powfacpy.template_models.digsilent_library.grid_forming_converters.droop_controlled_converter import (
    DroopControlledConverter,
)
from powfacpy.template_models.digsilent_library.grid_forming_converters.synchronverter import (
    Synchronverter,
)
from powfacpy.template_models.digsilent_library.grid_forming_converters.virtual_synchronous_machine import (
    VirtualSynchronousMachine,
)
from powfacpy.template_models.digsilent_library.grid_forming_converters.wecc_regfm_a1 import (
    WeccRegfmA1,
)
from powfacpy.template_models.digsilent_library.grid_forming_converters.wecc_regfm_b1 import (
    WeccRegfmB1,
)

__all__ = [
    "GridFormingConverter",
    "DroopControlledConverter",
    "Synchronverter",
    "VirtualSynchronousMachine",
    "WeccRegfmA1",
    "WeccRegfmB1",
]
