Module powfacpy.result_variables_parser
=======================================
Module to create result variables enumeration classes (see 'result_variables.py). The module with the enumeration classes is created by running this file.
The module is self contained and has only this purpose. It is usually not used by powfacpy users.

Classes
-------

`ResultVariablesParser()`
:   Read (parse) the result variables of PowerFactory .IntMon objects and create enumeration classes (for code completion etc.). The classes are written to the file under 'path_python_res_var_file'. The .txt files under 'path_pf_res_var_txt_files' were created manually by copying from the PF output window when clicking on 'Variable List' in the dialogue of an .IntMon file.
    Please have a look at these files for further understanding.

    ### Methods

    `create_results_variables_python_file(self)`
    :   Main method to create the results variables enumeration classes by reading from the .txt files under 'path_pf_res_var_txt_files' and writing to the python file under 'path_python_res_var_file'.
        In the output python file, a nested class with the hierarchy
        ResVar -> simulation type -> Elm class
        is created.

    `get_results_variables_module_docstring(self)`
    :

    `is_line_with_variable(self, line)`
    :   Lines with variables are identified by the colon and line length. A typical line looks like this:
        m:I2:bus1                kA     Negative-Sequence Current, Magnitude

    `write_elm_class_in_simulation_type(self, elm_class: str, in_file, out_file, pf_sim_type: str)`
    :   Write an elm class to the output python file for a specific simulation type. Iterates through the lines of the .txt file until it finds the simulation type. Then writes all its variables to the python files. Breaks the loop as soon as the next simualtion type is reached.

    `write_variable_line(self, line, used_attr, out_file)`
    :   Write one variable to the output python file.
        Splits the line (that was read in) according to two (or more) empty spaces, that separate attribute, unit (optional) and description.
        The same attributes can occur several times in the simulation type in the .txt file, so already used attributes ('used_attr') are ignored.