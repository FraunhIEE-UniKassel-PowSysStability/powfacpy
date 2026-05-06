Module powfacpy.pf_classes.blk.definition
=========================================
The name 'def' is not allowed for python modules, so the module is named 'definition'.

Classes
-------

`BlockDefinition(obj: BlkDef)`
:   Base child class (in object oriented sense - not like in GetParent()) to be used in combination with instances of PF objects (stored in '_obj'). The '__getattribute__' and '__setattr__' methods are overloaded to resemble the behavior of inheriting from the PF object. That means that all methods/data attributes of '_obj' are available and further attributes/methods can be added by any class that inherits from 'BaseChildStatic'.
    
    In addition, functionality is added to cache attributes and methods (the data is stored in '_obj' because 'BaseChildStatic' is static, i.e. it has no '__dict__' attribute because of the static slots).
    
    '__slots__' is required to inherit the slots from 'BaseObjectStatic' (i.e. '__slots__ = "_obj"').

    ### Ancestors (in MRO)

    * powfacpy.base.base.BaseChildStatic
    * powfacpy.base.base.BaseObjectStatic

    ### Instance variables

    `equations: list[str]`
    :

    `input_signals: list[str]`
    :

    `lower_limitation_parameters: list[str]`
    :

    `name: str`
    :

    `output_signals: list[str]`
    :

    `parameters: list[str]`
    :

    `states: list[str]`
    :

    `title: str`
    :

    `upper_limitation_parameters: list[str]`
    :

    ### Methods

    `export_block_diagram(self, target_dir: str = '.\\', file_name: str = '', format: str = 'svg') ‑> tuple[str, int]`
    :   Export grapic of block diagram.
        
        Args:
            target_dir (str, optional): Target directory. Defaults to ".".
            file_name (str, optional): file name. Defaults to "".
            format (str, optional): graphic format. Defaults to "svg".
        
        Returns:
            tuple[str, int]: _description_

    `get_attr_property_mapping(self) ‑> dict[str, typing.Callable]`
    :

    `get_attribute_info(self) ‑> dict[str, typing.Any]`
    :   Get attribute values for attributes defined in 'get_attr_property_mapping'.
        
        Returns:
            dict[str, Any]: _description_

    `get_blkdefs_of_subblocks(self, macros_and_graphical_separately: bool = False) ‑> dict`
    :   Get block definitions of subblocks.
        
        Args:
            macros_and_graphical_separately (bool, optional): If true, blockdefs that are macros and blockdefs that are graphical models are returned separately. Defaults to False.
        
        Returns:
            dict: dict with block references as keys and blockdefs as values or, if 'macros_and_graphical_separately' is true, a dict with keys 'Macros' and 'Graphical' and according values is returned.

    `get_blkrefs(self) ‑> list[powfacpy.pf_classes.protocols.BlkRef]`
    :

    `get_info(self) ‑> dict`
    :   Get default information:
        - attributes defined in method 'get_attr_property_mapping'
        - blockdefs of subblocks
        - Further attributes (see method body)
        
        Returns:
            dict: dict with default information.

    `get_mapping(self, blkrefs_blkdefs_dict: dict[BlkRef, BlkDef]) ‑> dict`
    :   Get mapping of parameter and state names between block references and block definitions. The parameter and state names can differ (e.g. when the same name occurs in several block references of a block definition).
        
        Args:
            blkrefs_blkdefs_dict (dict[BlkRef, BlkDef]): dict with blkrefs as keys and respective blkdefs as values.
        
        Returns:
            dict: blkrefs as keys and name mapping (tuples) as values

    `get_signal_type_name_mapping(self) ‑> dict[str, str]`
    :

    `read_attribute_that_is_string_in_list(self, attr: str) ‑> list[str]`
    :   PF returns some attribute values as strings (with commas as separators). Use this method to get the values as a list of strings.
        
        Args:
            attr (str): attribute name
        
        Returns:
            list[str]: values as a list of strings