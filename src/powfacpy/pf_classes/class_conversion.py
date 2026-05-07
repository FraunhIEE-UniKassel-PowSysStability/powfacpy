from __future__ import annotations


# To avoid circular import issues, this function must appear before the imports
def convert_pf_obj_to_powfacpy(obj: PFGeneral):
    class_name = obj.GetClassName()
    powfacpy_class = pf_to_powfacpy_class_mapping[class_name[0:3]][class_name[3:]]
    return powfacpy_class(obj)


from powfacpy.pf_classes.blk.definition import BlockDefinition
from powfacpy.pf_classes.blk.slot import Slot
from powfacpy.pf_classes.elm.comp import CompositeModel
from powfacpy.pf_classes.elm.dsl import DSLModel
from powfacpy.pf_classes.elm.sym import SynchronousMachine
from powfacpy.pf_classes.protocols import PFGeneral


pf_to_powfacpy_class_mapping = {
    "Elm": {
        "Sym": SynchronousMachine,
        "ElmDsl": DSLModel,
        "ElmComp": CompositeModel,
    },
    "Blk": {
        "Def": BlockDefinition,
        "Slot": Slot,
    },
}
