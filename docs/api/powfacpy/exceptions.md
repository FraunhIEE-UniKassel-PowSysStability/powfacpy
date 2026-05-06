Module powfacpy.exceptions
==========================

Classes
-------

`PFAttributeError(obj, msg_raised, pf_active_project: powfacpy.base.active_project.ActiveProject)`
:   Attempt to access an invalid attribute of a PF object.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFAttributeNotSetError(attribute_description)`
:   Attempt to access an attribute of a powfacpy class instance,
    but it was not specified.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFAttributeTypeError(obj, attr, msg_raised, pf_active_project)`
:   Attempt to set an invalid type for the attribute of a PF object.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFCaseStudyParameterValueDefinitionError(par_name, values)`
:   Number of parameter values is not the same for every parameter.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFInconsistentParamValueOfDSLModelInCompositeModel(param_name, composite_model)`
:   Attempt to create a dictionary with parameter names and values of DSL
    models in a composite model, but the DSL models have different values for
    the same parameter.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFInterfaceError(*args, **kwargs)`
:   There should always be a base class (that inherits
    from 'Exception') for all custom errors/exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * powfacpy.exceptions.PFAttributeError
    * powfacpy.exceptions.PFAttributeNotSetError
    * powfacpy.exceptions.PFAttributeTypeError
    * powfacpy.exceptions.PFCaseStudyParameterValueDefinitionError
    * powfacpy.exceptions.PFInconsistentParamValueOfDSLModelInCompositeModel
    * powfacpy.exceptions.PFInvalidCondition
    * powfacpy.exceptions.PFInvalidLoadFlow
    * powfacpy.exceptions.PFNoActiveStudyCaseError
    * powfacpy.exceptions.PFNonExistingObjectError
    * powfacpy.exceptions.PFNotActiveError
    * powfacpy.exceptions.PFObjectAttributeTypeError
    * powfacpy.exceptions.PFPathError
    * powfacpy.exceptions.PFPathInputError

`PFInvalidCondition(msg='')`
:   There should always be a base class (that inherits
    from 'Exception') for all custom errors/exceptions.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFInvalidLoadFlow(msg='')`
:   There should always be a base class (that inherits
    from 'Exception') for all custom errors/exceptions.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFNoActiveStudyCaseError()`
:   No active study case found.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFNonExistingObjectError(folder, obj, condition=False, include_subfolders=False)`
:   Attempt to access PF object (optional: with a specific condition) that does not exist.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFNotActiveError(obj_str)`
:   Unexpected inactive PF object.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFObjectAttributeTypeError(obj, msg_raised, pf_active_project)`
:   Unexpected type of a PF object attribute (e.g. 'None' type).

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFPathError(non_existing_child, existing_path)`
:   Attempt to access invalid path in PF database.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException

`PFPathInputError(path)`
:   Invalid input for a PF path.

    ### Ancestors (in MRO)

    * powfacpy.exceptions.PFInterfaceError
    * builtins.Exception
    * builtins.BaseException