from typing import Any, Callable, Generator
import math

import numpy as np
from icecream import ic
from powfacpy.applications.application_base import ApplicationBase
from powfacpy.applications.dynamic_simulation import DynamicSimulation
from powfacpy.applications.results import Results
from powfacpy.pf_classes.protocols import (
    PFGeneral,
)
from trimes.base import resample


class Variant(ApplicationBase):
    """Create variations for parameter studies (not to confuse with the  variation (IntScheme) class of PF)."""

    @property
    def min(self) -> float:
        return self.par_range[0]

    @property
    def max(self) -> float:
        return self.par_range[1]

    @property
    def objs(self) -> list:
        "Shortcut to get all PF objects"
        if isinstance(self.objs_and_attr, list):
            return self.objs_and_attr[0]
        elif isinstance(self.objs_and_attr, dict):
            return list(self.objs_and_attr.keys())

    @property
    def number_of_objs(self) -> int:
        return len(self.objs)

    def __init__(self, pf_app=False, cached=False) -> None:
        super().__init__(pf_app, cached)

        # Settings
        self.name: str
        "Name of variation"
        self.objs_and_attr: dict[PFGeneral, str] | list
        "The PF objects and their attributes to which the parameter variants are applied. Can be a dict with objects (keys) and attributes (values) or a list where the first element is a list of objects and the second element is the attribute (which is shared by all objects)."
        self.par_range: list[float]
        "The parameter range."
        self.steps: int
        "The number of steps (in the parameter range)."
        self.value_calculation: str = "equal"
        "Specifies how the values are calculated. Options are 'equal', 'multiply', 'add'. 'equal' means that the values are just set in PF. 'multiply' means that the attribute values are calculated by multiplying by the default value. 'add' means the attribute values are calculated by adding to the default value."
        self.variation_type: str = "const"
        "Specifies how the parameter values are set for the various PF objects. 'const' means that the same parameter value is set for all PF objects. 'gradient' means that there is a gradient for values that starts at the first object and ends at the last."

        self.preprocessing_step: Callable | None = None
        """Function that is called at each step before the simulation. Must be defined as a function with one input argument. This argument is a dict that gives access to the following data:
        - "variant": variant
        - "var_num": current variant number
        - "step_num": current step number
        - "sim_num": current total simulation number
        """
        self.postprocessing_step: Callable | None = None
        """Function that is called at each step after the simulation. Must be defined as a function with one input argument. This argument is a dict that gives access to the following data:
        - "sim_res": DataFrame with simulation results of step
        - "variant": variant
        - "var_num": current variant number
        - "sim_num": current total simulation number
        - "step_num": current step number
        
        IMPORTANT: If the simulation results are changed, the function must return them.        
        """
        self.default_values: dict = {}
        "Default values (values) for PF objects, attributes (keys)."

        # Autsomatically assigned attributes
        self.values: dict
        "List of values (values) of PF objects, attributes (keys) for all parameter sets"
        self.names_for_each_value: list[str] = []

    def initialize(self) -> None:
        if not self.default_values:  # Use current values in PF
            self.default_values.update(self.get_current_values_of_all_attr_in_pf())
        self.values = self.get_values()
        self.names_for_each_value = self.get_name_for_each_step()

    def get_name_for_each_step(self, use_calculated_vales: bool = False) -> list[str]:
        """Get a list of names for each steps. The names consist of 'self.name' and the value of the step (if the values of the targeted PF objects differ, the value of the first object in 'self.values' is used).

        Args:
            use_calculated_vales (bool): If True, the calculated values are used, else the values as specified by the user are used. Relevant if self.value_calculation is 'multiply' or 'add. Defaults to False.

        Returns:
            list[str]: list of names
        """
        if self.value_calculation in ["multiply", "add"] and not use_calculated_vales:
            # To get the values as specified by the user, the values are calculated as if 'self.value_calculation = "equal"'
            value_calculation = self.value_calculation
            self.value_calculation = "equal"
            values = list(self.get_values().values())[0]
            self.value_calculation = value_calculation
        else:
            values = list(self.values.values())[0]
        return [
            f"{self.name}={format_sig_no_sci(val)}" for val in values
        ]  # Format numerics

    def get_values(self) -> dict[PFGeneral, Any]:
        """Get the values of each PF object for each step.

        Returns:
            dict[PFGeneral, Any]: PF objects, attributes (keys) and list of values (values)
        """
        if self.variation_type == "const":  # values for all objects are the same
            values = np.broadcast_to(
                np.linspace(self.min, self.max, self.steps),
                (self.number_of_objs, self.steps),
            )
        elif self.variation_type == "gradient":  # calculate gradients
            grad_start_objs = np.linspace(self.min, self.max, self.number_of_objs)
            values = np.array(
                [
                    np.linspace(grad_start_objs[n], grad_start_objs[-n - 1], self.steps)
                    for n in range(len(grad_start_objs))
                ]
            )
        # create dict (keys are obj, attr and values are their values at each step)
        if isinstance(self.objs_and_attr, list):
            values = {
                (obj, self.objs_and_attr[1]): values[n, :]
                for n, obj in enumerate(self.objs_and_attr[0])
            }
        else:
            values = {
                (obj, attr): values[n, :]
                for n, (obj, attr) in enumerate(self.objs_and_attr.items())
            }
        # multiply or add to default values
        if self.value_calculation == "multiply":
            values = {k: v * self.default_values[k] for k, v in values.items()}
        elif self.value_calculation == "add":
            values = {k: v + self.default_values[k] for k, v in values.items()}
        return values

    def get_list_of_objs_and_attr(self) -> list:
        """Get list of obj, attr tuples.

        Returns:
            list: list of obj, attr tuples
        """
        if isinstance(self.objs_and_attr, list):
            return [(obj, self.objs_and_attr[1]) for obj in self.objs_and_attr[0]]
        else:
            return list(self.objs_and_attr.items())

    def get_current_values_of_all_attr_in_pf(self) -> dict:
        """Get the current (in PF) attribute values of all PF objects.

        Returns:
            dict: PF objects, attributes (keys) and attribute values (values)
        """
        return {
            (obj, attr): obj.GetAttribute(attr)
            for obj, attr in self.get_list_of_objs_and_attr()
            if not isinstance(obj, str)
        }

    def set_values_in_pf(self, step_num: int) -> None:
        """Set the attribute values of the step in PF

        Args:
            step_num (int): step number
        """
        for (obj, attr), values in self.get_values().items():
            if not isinstance(obj, str):
                obj.SetAttribute(attr, values[step_num])

    def set_default_values(self) -> None:
        """Reset the default attribute values in PF."""
        for (obj, attr), val in self.default_values.items():
            if not isinstance(obj, str):
                obj.SetAttribute(attr, val)

    def execute_preprocessing_step(self, pre_post_process_dict: dict) -> None:
        if self.preprocessing_step is not None:
            self.preprocessing_step(pre_post_process_dict)

    def execute_postprocessing_step(self, pre_post_process_dict: dict) -> None:
        if self.postprocessing_step is not None:
            return self.postprocessing_step(pre_post_process_dict)
        else:
            return pre_post_process_dict["sim_res"]


class ParameterStudy(ApplicationBase):
    """Parameter studies using Variants."""

    def __init__(self, pf_app=False, cached=False) -> None:
        super().__init__(pf_app, cached)
        self.variants: list[Variant]
        "Variants considered in this study"
        self.all_objs_and_attr: list
        "List of tuples with all PF objects and attributes of all variants "
        # self.results_variables: list
        # "List of tuples with PF objects and their monitored results variables"
        self.default_values: dict
        "Default values (values) of PF objects, attributes (keys)"
        self.values: dict
        "List of values for all variants (values) of PFobjects, attributes (keys)"
        self.preprocessing_variant: None | Callable = None
        """Function that is called before each variant is simulated. Must be defined as a function with one input argument. This argument is a dict that gives access to the following data:
        - "variant": variant
        - "var_num": current variant number
        - "sim_num": current total simulation number
        """
        self.preprocessing_step: None | Callable = None
        """Function that is called at each step of the variants BEFORE the simulation. Must be defined as a function with one input argument. This argument is a dict that gives access to the following data:
        - "variant": variant
        - "var_num": current variant number
        - "sim_num": current total simulation number
        - "step_num": current step number
        """
        self.postprocessing_step: None | Callable = None
        """Function that is called at each step of the variants AFTER the simulation. Must be defined as a function with one input argument. 
        This argument is a dict that gives access to the following data:
        - "sim_res": DataFrame with simulation results of step
        - "variant": variant
        - "var_num": current variant number
        - "sim_num": current total simulation number
        - "step_num": current step number
        
        IMPORTANT: If the simulation results are changed, the function must return them.
        """
        self.default_values: dict = {}
        "Default values (values) for PF objects, attributes (keys)."

    def initialize(self) -> None:
        if not self.default_values:
            self.default_values = self.get_default_values()
        self.values = self.get_all_values()

    def get_all_objs_and_attr(self, sort: bool = True, cache: bool = False) -> list:
        """Get list of tuples with all PF objects and their attribute.

        Args:
            cache (bool, optional): If True, the list is stored in 'self.all_objs_and_attr'. Defaults to False.

        Returns:
            list: list of tuples with all PF objects and their attribute
        """
        all_objs_and_attr = []
        for var in self.variants:
            all_objs_and_attr += var.get_list_of_objs_and_attr()
        all_objs_and_attr = list(set(all_objs_and_attr))
        if sort:

            def sort_key(x) -> str:
                if isinstance(x[0], str):
                    return x[0]
                else:
                    return x[0].loc_name

            all_objs_and_attr.sort(key=sort_key)
        if cache:
            self.all_objs_and_attr = all_objs_and_attr
        return all_objs_and_attr

    def get_current_values_of_all_attr_in_pf(self) -> dict[tuple, Any]:
        """Get the current (in PF) attribute values of all PF objects.

        Returns:
            dict: PF objects, attributes (keys) and attribute values (values)
        """
        all_objs_and_attr = self.get_all_objs_and_attr()
        return {
            (obj, attr): obj.GetAttribute(attr)
            for obj, attr in all_objs_and_attr
            if not isinstance(obj, str)
        }

    def get_all_values(self) -> dict:
        """Get values of PF object attributes for all variants.

        Returns:
            dict: Tuple of PF object, attribute (keys) and (flat) list of attribute values for all variants (values).
        """
        all_values = {k: [] for k in self.get_all_objs_and_attr()}
        for obj_and_attr, values in all_values.items():
            for var in self.variants:
                val = var.values.get(obj_and_attr)
                if val is not None:
                    values += list(val)
                else:  # use default value
                    values += [self.default_values[obj_and_attr]] * var.steps
        all_values = {k: np.array(v) for k, v in all_values.items()}
        return all_values

    def step_generator(
        self, set_values_in_pf: bool = True
    ) -> Generator[tuple[dict, str]]:
        for variant in self.variants:
            for step_num, name in enumerate(variant.names_for_each_value):
                values = {}
                for (obj, attr), vals in variant.values.items():
                    value = vals[step_num]
                    values[(obj, attr)] = value
                    if set_values_in_pf and not isinstance(obj, str):
                        obj.SetAttribute(attr, value)
                yield values, name

    def execute_dynamic_simulations(
        self,
    ) -> dict:
        """Execute dynamic simulations for all steps of all variants. Allows functions calls for pre- and postprocessing (the functions take all local variables as input arguments).

        Args:
            sample_time (float): resample simulation results

        Returns:
            dict: simulation result DataFrames (values) of all simulations (keys are names of simulations)
        """
        pfds = DynamicSimulation()
        pfri = Results()
        pfri.pf_objects_in_labels = True
        all_sim_res = {}
        sim_num = 0
        self.set_default_values()
        for variant in self.variants:
            try:
                self.execute_preprocessing_variant(locals())
                for step_num, name in enumerate(variant.names_for_each_value):
                    self.execute_preprocessing_step(locals())
                    variant.execute_preprocessing_step(locals())
                    for (obj, attr), val in variant.values.items():
                        if not isinstance(obj, str):
                            obj.SetAttribute(attr, val[step_num])
                    pfds.initialize_and_run_sim()
                    sim_res = pfri.export_to_pandas()
                    sim_res_processed = variant.execute_postprocessing_step(locals())
                    if sim_res_processed is not None:
                        sim_res = sim_res_processed
                    sim_res_processed = self.execute_postprocessing_step(locals())
                    if sim_res_processed is not None:
                        sim_res = sim_res_processed
                    all_sim_res[name] = sim_res
                    sim_num += 1
            finally:
                variant.set_default_values()
        return all_sim_res

    def get_values_of_variant(
        self,
        variant: Variant | int | str,
        step_num: int | None = None,
    ) -> dict:
        """Get the attribute values of all PF objects for one of the variants.

        Args:
            variant (Variant | int | str): The variant instance, the variant index or the variant name.
            step_num (int | None, optional): If given, only the value of this step is returned. Defaults to None.

        Returns:
            dict: Tuple of PF objects, attributes (keys) and attribute values (values)
        """
        variant = self.get_variant(variant)
        if step_num is not None:
            return {
                (obj, attr): values[step_num]
                for (obj, attr), values in variant.values.items()
            }
        else:
            return {
                (obj, attr): values for (obj, attr), values in variant.values.items()
            }

    def set_values_in_pf(
        self,
        variant: Variant | int | str,
        step_num: int,
        reset_default_values: bool = True,
    ) -> None:  # TODO use above for simulations
        """Set attribute values of all PF objects of a variant in PowerFactory for a certain step number.

        Args:
            variant (Variant | int | str): The variant instance, the variant index or the variant name.
            step_num (int): step number
            reset_default_values (bool, optional): If True, all the default values are initially reset. Defaults to True.
        """
        if reset_default_values:
            self.set_default_values()
        variant = self.get_variant(variant)
        variant.set_values_in_pf(step_num)

    def set_default_values(self) -> None:
        """Set default values of all variants."""
        [var.set_default_values() for var in self.variants]

    def get_default_values(self) -> dict:
        """Get all default attribute values of all variants.

        Returns:
            dict: tuple of PF object, attribute (keys) and attribute values (values)
        """
        default_values = {}
        for var in self.variants:
            default_values.update(var.default_values)
        return default_values

    def get_variant(self, variant: Variant | int | str) -> Variant:
        """Get variant.

        Args:
            variant (Variant | int | str): If the input is the variant instance already, just returns it. If it is an int it is assumed to be the index. If at is a string it is assumed to be the name.

        Returns:
            Variant: variant
        """
        if isinstance(variant, Variant):
            return variant
        elif isinstance(variant, int):
            return self.variants[variant]
        elif isinstance(variant, str):
            return [var for var in self.variants if var.name == variant][0]

    def execute_preprocessing_variant(self, pre_post_process_dict) -> None:
        if self.preprocessing_variant is not None:
            self.preprocessing_variant(pre_post_process_dict)

    def execute_preprocessing_step(self, pre_post_process_dict) -> None:
        if self.preprocessing_step is not None:
            self.preprocessing_step(pre_post_process_dict)

    def execute_postprocessing_step(self, pre_post_process_dict: dict) -> None:
        if self.postprocessing_step is not None:
            return self.postprocessing_step(pre_post_process_dict)
        else:
            return pre_post_process_dict["sim_res"]

    def get_all_names(self) -> list[str]:
        """Get names of all simulations/steps.

        Returns:
            list[str]: list of names
        """
        names = []
        for variant in self.variants:
            for name in variant.names_for_each_value:
                names.append(name)
        return names


def format_sig_no_sci(x, sig=3) -> str:
    """Format figure to three significant digits"""
    if x == 0:
        return "0"

    # Determine digits before decimal
    digits = int(math.floor(math.log10(abs(x)))) + 1
    decimals = max(sig - digits, 0)

    return f"{x:.{decimals}f}"
