Module powfacpy.pf_classes.blk.slot
===================================

Classes
-------

`Slot(obj: BlkSlot)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic

    ### Instance variables

    `input_signals: list[str]`
    :

    `lower_limitation_input: list[str]`
    :

    `name: str`
    :

    `output_signals: list[str]`
    :

    `upper_limitation_input: list[str]`
    :

    ### Methods

    `get_signal_type(self, signal_types: list[str]) ‑> None`
    :   TODO explain
        
        Args:
            signal_types (list[str]): _description_
        
        Returns:
            _type_: _description_

    `get_signal_type_name_mapping(self) ‑> dict[str, str]`
    :

    `read_attribute_that_is_string_in_list(self, attr: str) ‑> list[str]`
    :   Read attributes that are returned by PF in inconvenient format as a string (with comma separation) in a list (e.g. '[s1, s2, s3]'). Return a list with all values as items instead (e.g. [s1, s2, s3]).
        
        Args:
            attr (str): attribute name
        
        Returns:
            list[str]: list with all values as items