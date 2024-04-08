"""
 Module to create result variables enumeration classes (see 'result_variables.py). The module with the enumeration classes is created by running this file.
 The module is self contained and has only this purpose. It is usually not used by powfacpy users.
"""

from os import listdir
from icecream import ic


supported_and_unsupported_simulation_types_and_names = {
  "Basic Data balanced:": "Basic", 
  "Basic Data unbalanced:": False, # False means not supported
  "Load Flow AC balanced:": False,
  "Load Flow AC unbalanced:": False,
  "Simulation RMS balanced:": "RMS_Bal",
  "Simulation RMS unbalanced:": "RMS_Unbal",
  "Simulation EMT balanced:": False,
  "Simulation EMT unbalanced:": "EMT",
  "Power Quality/Harmonics balanced:": False,
  "Power Quality/Harmonics unbalanced:": False,
  "Protection unbalanced:": False,  
}


class ResultVariablesParser():
  """Read (parse) the result variables of PowerFactory .IntMon objects and create enumeration classes (for code completion etc.). The classes are written to the file under 'path_python_res_var_file'. The .txt files under 'path_pf_res_var_txt_files' were created manually by copying from the PF output window when clicking on 'Variable List' in the dialogue of an .IntMon file.
  Please have a look at these files for further understanding.
  """
  
  def __init__(self) -> None:
    self.indentation_increment:str = "  "
    self.path_pf_res_var_txt_files:str = r'.\result_variables' 
    self.path_python_res_var_file:str = r'.\src\powfacpy\result_variables.py'
    
  
  def create_results_variables_python_file(self):
    """Main method to create the results variables enumeration classes by reading from the .txt files under 'path_pf_res_var_txt_files' and writing to the python file under 'path_python_res_var_file'.
    In the output python file, a nested class with the hierarchy 
    ResVar -> simulation type -> Elm class 
    is created.
    """
    with open(self.path_python_res_var_file, 'w') as out_file:
      module_docstring = self.get_results_variables_module_docstring()
      out_file.write(module_docstring)
      out_file.write("from aenum import Enum\n\n")
      out_file.write("class ResVar:\n")
      pf_res_var_txt_files = listdir(self.path_pf_res_var_txt_files)
      for pf_sim_type, powfacpy_sim_type in supported_and_unsupported_simulation_types_and_names.items():
        if powfacpy_sim_type:
          out_file.write("\n\n")
          out_file.write(self.indentation_increment + "class "+powfacpy_sim_type+":\n")
          for res_var_file in pf_res_var_txt_files:
            with open(self.path_pf_res_var_txt_files + "//" + res_var_file, 'r') as in_file:
              out_file.write("\n")
              elm_class = res_var_file.split(".")[0]
              self.write_elm_class_in_sumlation_type(elm_class, in_file, out_file, pf_sim_type)
  
      
  def get_results_variables_module_docstring(self):
    module_docstring = f"""\"\"\"
This module provides enumeration classes for results variables of 'Elm' classes (network elements). This is convenient to get results variable strings and supports code completion in your IDE. If you hover over a variable, it's unit and description will be shown.  

This file is automatically created using the .txt files in '{self.path_pf_res_var_txt_files}' and using the module 'results_varaibles_parser'. The .txt files are created by copying from the output window of PF (manually) using the printed results variables when clicking on 'Variable List' in an .IntMon file of an 'Elm' class.

Currently, the following 'Elm' classes are supported: \n
""" 
    pf_res_var_files = listdir(self.path_pf_res_var_txt_files)
    for res_var_file in pf_res_var_files:
      module_docstring += res_var_file.split(".")[0] + "\n"  
    module_docstring += "\nThe follwing simulation types/result variable types are supported:\n\n"
    for pf_simtype,powfacpy_sim_type in supported_and_unsupported_simulation_types_and_names.items():
      if powfacpy_sim_type:
        module_docstring += pf_simtype + " " +powfacpy_sim_type + "\n"
    module_docstring += "\"\"\"\n"
    return module_docstring


  def write_elm_class_in_sumlation_type(self, elm_class:str, in_file, out_file, pf_sim_type:str):
    """Write an elm class to the output python file for a specific simulation type. Iterates through the lines of the .txt file until it finds the simulation type. Then writes all its variables to the python files. Breaks the loop as soon as the next simualtion type is reached.
    """
    out_file.write(2*self.indentation_increment + "class " + elm_class + "(Enum):\n")
    out_file.write(3*self.indentation_increment + "_init_ = 'value __doc__'\n\n") # required for enumeration classes with descriptions for each attribute
    write_variables = False
    for line in in_file:
      line = line.rstrip()
      if line in supported_and_unsupported_simulation_types_and_names:
        if line == pf_sim_type:
          write_variables = True
          used_attr = []
        elif write_variables:
          break  
      if write_variables and self.is_line_with_variable(line):
        self.write_variable_line(line, used_attr, out_file)
          
  
  def is_line_with_variable(self, line):
    """Lines with variables are identified by the colon and line length. A typical line looks like this:
    m:I2:bus1                kA     Negative-Sequence Current, Magnitude
    """
    return len(line) > 1 and line[1] == ":"
          
          
  def write_variable_line(self, line, used_attr, out_file):
    """Write one variable to the output python file. 
    Splits the line (that was read in) according to two (or more) empty spaces, that separete attribute, unit (optional) and description.
    The same attributes can occur several times in the simualtion type in the .txt file, so alreay used attributes ('used_attr') are ignored.
    """
    attr_and_unit_and_description = line.split("  ")
    attr_with_underscores_instead_of_colon = attr_and_unit_and_description[0].replace(":","_")
    if not attr_with_underscores_instead_of_colon in used_attr:
      used_attr.append(attr_with_underscores_instead_of_colon)
      out_line = 3*self.indentation_increment + attr_with_underscores_instead_of_colon + " = " + "\"" + attr_and_unit_and_description[0] + "\", \""
      for n in attr_and_unit_and_description[1:]:
        if n:
          out_line +=  n.rstrip().lstrip() + ", "  # delete leading and trailing whitespace
      out_file.write(out_line[:-2] + "\"\n") # delete last comma 




if __name__ == "__main__":
  parser = ResultVariablesParser()
  parser.create_results_variables_python_file()


