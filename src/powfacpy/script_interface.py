"""Provides classes to interface python script objects (ComPython)
and to create an embedded script in the PF database based on a
python package. Used for example to add powfacpy to the embedded
script of a ComPython object to avoid having to install powfacpy,
which is an obstacle for some users without experience in coding 
or with pip.
"""

import sys
sys.path.insert(0, r'.\src')
import powfacpy
import warnings
from os import path as os_path
import os
import shutil


class PFComPythonObjectInterface(powfacpy.PFBaseInterface):
  """Interface to python script objects.
  """

  def __init__(self, app): 
    super().__init__(app) 

  def create_file_from_embedded_script(self, out_file, compython):
    """Create a .py file from an embedded script.
    """
    compython = self.handle_single_pf_object_or_path_input(compython)
    # The xScript attribute is a list with all lines of the script
    TextFileProcessor.create_file_from_list_of_lines(out_file, compython.xScript)

  def set_embedded_script_from_file(self, compython, file):
    """Set the embedded script based on a .py file.
    """
    compython = self.handle_single_pf_object_or_path_input(compython)
    compython.xScript = TextFileProcessor.get_list_of_lines_of_file(file)

  def merge_file_into_embedded_script(self,
    compython,
    inserted_file:str,
    start_after_line,
    end_before_line):
    """Merge a file into an embedded script between the starting 
    and ending lines.
    The start and end lines can either be integers (line numbers) or
    string matches.
    """
    compython = self.handle_single_pf_object_or_path_input(compython)
    temporary_dir = "powfacpy_temp"
    os.makedirs(temporary_dir,exist_ok=True)
    try:
      embedded_script_original_file = temporary_dir + r"\embedded_script_original.py"
      self.create_file_from_embedded_script(embedded_script_original_file, compython)
      merged_file = temporary_dir + r"\merged.py"
      TextFileProcessor.merge_into_file(embedded_script_original_file,
        inserted_file, merged_file, start_after_line, end_before_line)
      self.set_embedded_script_from_file(compython, merged_file)  
    finally:
      # Delete temporary directory
      shutil.rmtree(temporary_dir)  

  def merge_package_into_embedded_script(self,
    compython,
    init_file,
    start_after_line,
    end_before_line):
    """Merge a whole package into an embedded script between the starting 
    and ending lines.
    The start and end lines can either be integers (line numbers) or
    string matches.
    """
    temporary_dir = "powfacpy_temp"  
    os.makedirs(temporary_dir)
    try:
      compython = self.handle_single_pf_object_or_path_input(compython)
      merged_package_file = temporary_dir + r"\merged_package.py"
      PythonFileInterface.merge_package_into_single_file(init_file, merged_package_file)
      original_embedded_script_file = temporary_dir + r"\original_embedded_script.py"
      self.create_file_from_embedded_script(original_embedded_script_file, compython)
      merged_package_into_embedded_file = temporary_dir + r"\merged_package_into_embedded.py"
      TextFileProcessor.merge_into_file(original_embedded_script_file,
        merged_package_file,
        merged_package_into_embedded_file,
        start_after_line,
        end_before_line)
      self.set_embedded_script_from_file(compython, merged_package_into_embedded_file)  
    finally:
      # Delete temporary directory
      shutil.rmtree(temporary_dir)

  def merge_powfacpy_package_into_single_file(self, out_file):
    init_file = os.path.dirname(__file__) + r"\__init__.py"
    PythonFileInterface.merge_package_into_single_file(init_file, out_file)


class PythonFileInterface():
  """Interface for .py files and python packages.
  """
  # ToDo: Convert notebooks to scripts (delete magic etc.)

  @staticmethod
  def read_init_file_of_package(path_of_init_file: str):
    """Reads the __init__.py file of a python package and returns
    the paths of the .py files the package uses and the name of the package.
    For now, only lines with the syntax
      'from example import *'
    are considered (i.e. this method does not work with all packages, but for example 
    with powfacpy)    
    """
    # The dir of the __init__.py file is also the directory of the files of the packages
    dir_of_all_files,_ = os_path.split(path_of_init_file)
    # The name of the package is the name of the parent folder of the __init__.py file 
    name_of_package = dir_of_all_files.split("\\")[-1] 
    file_paths= []
    with open(path_of_init_file, 'r') as init_file:
      for line in init_file:
        if line.startswith("from "):
          line = line.replace("from ","").replace(".","")
          file, imported_content = line.split(" import ")
          if not "*" in imported_content:
            falsely_read_line = line.split("import")[0] + "import *"
            warnings.warn(f"Cannot read <{line}>. Instead <{falsely_read_line}> is read.")
          file_paths.append(dir_of_all_files + "\\" + file + ".py")
    return file_paths, name_of_package

  @staticmethod
  def merge_package_into_single_file(init_file:str, out_file:str):
    """Merges all .py files of a package into a single file.
    Arguments:
      init_file: path of __init__.py of package
      out_file: path of file created  
    """
    package_files, package_name = PythonFileInterface.read_init_file_of_package(init_file)     
    merged_package_file = out_file
    replaced_chars = {package_name + ".":""}
    ignored_lines = {"import " + package_name:""} 
    TextFileProcessor.merge_files(package_files,
      merged_package_file,
      ignored_lines,
      replaced_chars)

class TextFileProcessor():
  """Processes plain text files (e.g. .txt or .py)
  """
  
  @staticmethod
  def merge_files(
    in_files: list,
    out_file: str,
    replace_line_if_startswith: dict = None,
    replace_chars: dict = None):
    """Merges several files into one. 
    Optionally replaces lines and chars.
    Arguments:
      in_files: list of input file paths
      out_file: output file path
      replace_line_if_startswith: dict to replace lines that 
        start with key with value
      replace_chars: dict to replace chars in key with value 
    """
    if not out_file.endswith(".py"):
      out_file = out_file + ".py"
    with open(out_file, 'w') as outfile:
      for fname in in_files:
        with open(fname) as infile:
          for line in infile:
            line = TextFileProcessor._replace_line(line,
              replace_line_if_startswith, replace_chars)
            if line:
              outfile.write(line)
          outfile.write("\n \n")

  @staticmethod
  def _replace_line(
    line: str,
    replace_line_if_startswith: dict = None,
    replace_chars: dict = None):
    """Handle replacements in line.
    """
    if replace_line_if_startswith:
      for start, replacement in replace_line_if_startswith.items():
        if line.startswith(start):
          line = replacement
          break
    if replace_chars:
      for replaced_char, replacement in replace_chars.items():
        line = line.replace(replaced_char, replacement)
    return line    

  @staticmethod
  def merge_into_file(
    target_file:str,
    inserted_file:str,
    out_file:str,
    start_after_line,
    end_before_line):
    """
    Creates a new file where one file is merged into another.
    Searches for start_after_line and end_before_line in target_file
    and replaces everything in between with inserted_file.
    The start and end lines can either be integers (line numbers) or
    string matches.
    """
    with open(out_file, 'w') as outfile:
      with open(target_file,'r') as sourcefile:
        start_line_was_reached = False
        end_line_was_reached = False
        line_count = 0
        for line in sourcefile:
          line_count = line_count + 1
          if not start_line_was_reached:
            outfile.write(line)
            if TextFileProcessor._line_is_reached(line, line_count, start_after_line):
              with open(inserted_file,'r') as insfile:
                outfile.write(insfile.read())
              outfile.write("\n")	
              start_line_was_reached = True
          elif TextFileProcessor._line_is_reached(line, line_count, end_before_line):		
            end_line_was_reached = True
          if end_line_was_reached:
            outfile.write(line)			
    if not start_line_was_reached:
      raise Exception(f"The spefified starting line for merging \n" +
        f"\"\n{start_after_line}\" \n was not found in the file {target_file}.")


  @staticmethod
  def _line_is_reached(current_line: str,
                      current_line_count:int,
                      condition):
    """Checks if a line is reached based upon a condition that can
    either be a line number or a string match.
    """
    if isinstance(condition, int):
      if current_line_count == condition:
        return True
      else:
        return False
    elif isinstance(condition, str):
      if current_line.rstrip() == condition:
        return True
      else:
        return False			

  @staticmethod
  def get_list_of_lines_of_file(file):
    """Reads all lines into a python list.
    """
    lines = []
    with open(file,'r') as f:
      for line in f:
        lines.append(line.rstrip()) # Omit line break and whitespace at the end 
    return lines

  @staticmethod
  def create_file_from_list_of_lines(out_file, lines):
    
    with open(out_file,"w") as f:
      for line in lines:
        f.write(line + "\n")  

  @staticmethod
  def process_file(
    in_file: str,
    out_file: str,
    replace_line_if_startswith: dict = None,
    replace_chars: dict = None,
    ):
    """Replaces chars and lines that start with a certain string.
    """
    with open(in_file,"r") as infile:
      with open(out_file,"w") as outfile:
        for line in infile:
          line = TextFileProcessor._replace_line(
              line,
              replace_line_if_startswith,
              replace_chars)
          if line:
            outfile.write(line)

  @staticmethod
  def extract_from_file(
    source_file: str,
    out_file: str,
    start_after_line,
    end_before_line):
    """Extracts the content between two lines from a file and writes
    to a new file.
    The start and end lines can either be integers (line numbers) or
    string matches.
    """
    with open(source_file,"r") as sourcefile:
      with open(out_file,"w") as outfile:
        start_line_was_reached = False
        end_line_was_reached = False
        line_count = 0
        for line in sourcefile:
          line_count = line_count + 1
          if not start_line_was_reached:
            if TextFileProcessor._line_is_reached(line, line_count, start_after_line):
              start_line_was_reached = True
          elif not end_line_was_reached:
            if TextFileProcessor._line_is_reached(line, line_count, end_before_line):		
              end_line_was_reached = True
            else:
              outfile.write(line)
  


  





