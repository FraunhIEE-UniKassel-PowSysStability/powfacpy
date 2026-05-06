Module powfacpy.pf_classes.protocol_generator
=============================================
Create protocol classes for all python classes in the PF python scripting reference pdf file (by running this python module). See output module 'pf_class_protocols' which is used in powfacpy. If you run this module a new module is created ('pf_class_protocols_new'). You can then delete the old one and rename the new file.

IMPORTANT: If you miss a class please add it to the 'missing_classes_that_are_not_in_scripting_reference' list below.

This module is not used by other modules of powfacpy and has the sole purpose of creating the protocols.

Classes
-------

`Empty()`
:   This empty class is used to get the generic attributes that every python object has (e.g. using 'dir(class_instance)').
    For the PF class protocols, these attributes are not added to the protocol classes of the PowerFactory objects.

`PFClassesProtocolGenerator(app)`
:   Generate protocol classes for PF classes from the PF python scripting reference.
    
    Args:
        folder (Union[PFGeneral, str]): folder object or path in active project (or in active user if no project is active)
        pf_app (PFApp | None | bool, optional): Powerfactory app (returned by GetApplication). Defaults to False (does not default to None because None is returned by GetApplication if something goes wrong; Therefore, None should raise an exception).
    
    Raises:
        TypeError: When pf_app is None. See explanation of argument 'pf_app'.

    ### Ancestors (in MRO)

    * powfacpy.base.active_project.ActiveProject
    * powfacpy.base.folder.Folder
    * powfacpy.base.base.BaseObjectStatic

    ### Methods

    `create_pf_class_protocols(self) ‑> None`
    :   Main method of this class.

    `get_all_class_names_from_scripting_reference(self) ‑> list[str]`
    :   Uses a .txt file to which the TOC of the python scripting reference pdf document was copied (includes the class names).
        Iterates all words from the TOC and checks if they are PF class names.
        
        Returns:
            list[str]: PF class names

    `get_class_attribute_definitions(self, pf_obj) ‑> str`
    :   Get definitions of class attributes (data attributes and methods) of a PF object.
        
        Args:
            pf_obj: PF object
        
        Returns:
            str: definitions of all attributes of the class of the object

    `get_class_definition(self, pf_obj) ‑> str`
    :   Get string with the definition of a protocol class for a PF object.
        Example: 'class ElmTr2(Protocol):'
        
        Args:
            pf_obj: PF object
        
        Returns:
            str: class definition

    `get_general_class_string(self)`
    :   Add class with 'general methods' (see Section 'General Methods' in scripting reference). All other classes (except for PFApp) inherit from this class.

    `get_general_methods(self)`
    :   General methods from python scripting reference.

    `get_pf_objects(self, pf_class_names: list[str]) ‑> list`
    :   Get instances of the PF classes in 'pf_class_names'.
        
        Creates a new project and tries to create each class in one of the folders in the project. Some objects can only be created inside certain folders. Hence, the procedure is done twice to ensure that the folders are present (i.e. create folders in first run, use those folders to create the specific objects in the second run).
        Finally, further objects that cannot be created in this way are added.
        
        Args:
            pf_class_names (list[str]): _description_
        
        Returns:
            pf_class_objects: list of powerfactory class instances/objects
            pf_class_objects_not_found: list of objects that could not be found/created