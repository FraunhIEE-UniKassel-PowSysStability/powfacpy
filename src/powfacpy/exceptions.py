"""Custom exceptions for powfacpy."""

from __future__ import annotations

from typing import TYPE_CHECKING

from powfacpy.base import string_manipulation as strman

if TYPE_CHECKING:
    from powfacpy.base.active_project import ActiveProject


class PFInterfaceError(Exception):
    """There should always be a base class (that inherits
    from 'Exception') for all custom errors/exceptions.
    """

    pass


class PFAttributeError(PFInterfaceError):
    """Attempt to access an invalid attribute of a PF object."""

    def __init__(
        self,
        obj,
        msg_raised,
        pf_active_project: ActiveProject,
    ):
        if obj:
            object_str = pf_active_project.get_path_of_object(obj)
        else:
            object_str = str(obj)  # e.g. when obj is 'None'
        self.message = f"Unexpected attribute of object '{object_str}': {msg_raised}."
        super().__init__(self.message)


class PFObjectAttributeTypeError(PFInterfaceError):
    """Unexpected type of a PF object attribute (e.g. 'None' type)."""

    def __init__(self, obj, msg_raised, pf_active_project):
        object_str = pf_active_project.get_path_of_object(obj)
        self.message = f"Unexpected attribute of object '{object_str}': {msg_raised}."
        super().__init__(self.message)


class PFAttributeTypeError(PFInterfaceError):
    """Attempt to set an invalid type for the attribute of a PF object."""

    def __init__(self, obj, attr, msg_raised, pf_active_project):
        object_str = pf_active_project.get_path_of_object(obj)
        self.message = f"The attribute '{attr}' of the object '{object_str}' is of unexpected type: {msg_raised}."
        super().__init__(self.message)


class PFNonUniqueObjectError(PFInterfaceError, TypeError):
    """More than one PF object matched where a single unique object was expected.

    Inherits from ``TypeError`` as well so that existing ``except TypeError``
    handlers keep working (this used to be a plain ``TypeError``).
    """

    def __init__(self, path: str, parent_folder_str: str = ""):
        self.message = (
            f"The path '{path}{parent_folder_str}' is not a unique object. "
            "Did you use wildcards ('*')? This method only returns single unique objects."
        )
        super().__init__(self.message)


class PFPathError(PFInterfaceError):
    """Attempt to access invalid path in PF database."""

    def __init__(self, non_existing_child, existing_path):
        if non_existing_child[-1] == ".":
            pf_bug_msg = "The name ends with a '.' and there is a PF bug for such names. You need to add another dot at the end ('..')."
        else:
            pf_bug_msg = ""
        self.message = f"'{non_existing_child}' does not exist in '{existing_path}'. {pf_bug_msg}"
        super().__init__(self.message)


class PFPathInputError(PFInterfaceError):
    """Invalid input for a PF path."""

    def __init__(self, path):
        self.message = (
            f"The path '{path}' is invalid or empty. Please don't start "
            + f"the path with '\\'."
        )
        super().__init__(self.message)


class PFNonExistingObjectError(PFInterfaceError):
    """Attempt to access PF object (optional: with a specific condition) that does not exist."""

    def __init__(self, folder, obj, condition=False, include_subfolders=False):
        folder_str = strman.remove_html_tags_from_path(str(folder))
        folder_str = strman.remove_class_names(folder_str)
        if include_subfolders:
            msg_subfolder = " (and its subfolders)"
        else:
            msg_subfolder = ""
        msg = f"The folder '{folder_str}'{msg_subfolder} does not contain any object or path named '{obj}'"
        if condition:
            msg = msg + " with specified condition"
        self.message = msg
        super().__init__(self.message)


class PFNotActiveError(PFInterfaceError):
    """Unexpected inactive PF object."""

    def __init__(self, obj_str):
        self.message = f"Please activate {obj_str}."
        super().__init__(self.message)


class PFNoActiveStudyCaseError(PFInterfaceError):
    """No active study case found."""

    def __init__(self):
        self.message = "No active study case found. Please activate one."
        super().__init__(self.message)


class PFAttributeNotSetError(PFInterfaceError):
    """Attempt to access an attribute of a powfacpy class instance,
    but it was not specified.
    """

    def __init__(self, attribute_description):
        self.message = (
            f"Attempt to access {attribute_description}, " "but it was not set."
        )
        super().__init__(self.message)


class PFCaseStudyParameterValueDefinitionError(PFInterfaceError):
    """Number of parameter values is not the same for every parameter."""

    def __init__(self, par_name, values):
        self.message = (
            f"Incorrect number of values defined for parameter '{par_name}'. "
            f"Only {len(values)} values were defined."
        )
        super().__init__(self.message)


class PFInconsistentParamValueOfDSLModelInCompositeModel(PFInterfaceError):
    """Attempt to create a dictionary with parameter names and values of DSL
    models in a composite model, but the DSL models have different values for
    the same parameter.
    """

    def __init__(self, param_name, composite_model):
        self.message = (
            f"The parameter '{param_name}' takes on different values in "
            f"the DSL models of the composite model '{composite_model}'. "
            "Therefore, creating a single dictionary with correct parameter "
            "values for all DSL models is not possible."
        )
        super().__init__(self.message)


class PFInvalidCondition(PFInterfaceError):

    def __init__(self, msg="") -> None:
        self.message = f"No object found that satisfies condition. {msg}"
        super().__init__(self.message)


class PFInvalidLoadFlow(PFInterfaceError):

    def __init__(self, msg="") -> None:
        self.message = f"No valid load flow results. {msg}"
        super().__init__(self.message)


class PFInvalidResultExport(PFInterfaceError):

    def __init__(self, msg="") -> None:
        self.message = f"The simulation results could not be exported. Please check if the simulation executed correctly. \n\n {msg}"
        super().__init__(self.message)


class PFModelicaCompilationError(PFInterfaceError):
    """A Modelica model type ('TypMdl') failed to check or compile."""

    def __init__(self, model_name: str, messages: list[str] | None = None) -> None:
        detail = ("\n" + "\n".join(messages)) if messages else ""
        self.message = f"Modelica model type '{model_name}' did not compile.{detail}"
        super().__init__(self.message)


class PFEigenvalueMismatchError(PFInterfaceError):
    """Two eigenvalue-related sets that should correspond 1:1 (e.g. for
    tracking or computing a sensitivity) have different lengths or indexes."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class PFEigenvalueTrackingError(PFInterfaceError):
    """Eigenvalue tracking could not find a unique one-to-one mapping between
    a reference and a scrambled eigenvalue set."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class PFEnumValueError(PFInterfaceError):
    """An enumeration attribute was given a label that is not one of its options."""

    def __init__(
        self, class_name: str, attr: str, value, options: dict[int, str]
    ) -> None:
        choices = (
            ", ".join(f"{code}={label!r}" for code, label in options.items())
            or "unknown"
        )
        self.message = (
            f"{value!r} is not a valid value for the enumeration attribute "
            f"'{attr}' of '{class_name}'. Options: {choices}."
        )
        super().__init__(self.message)
