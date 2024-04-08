import sys
from typing import Iterable, Union
from fnmatch import fnmatch

from icecream import ic

sys.path.insert(0, r'.\src')
import powfacpy
from powfacpy.pf_class_protocols import *


class GroupOfObjects():
  
  def __init__(self, objects:list[PFGeneral]) -> None:
    self.objs:list[PFGeneral] = objects
    
  
  def __iter__(self):
    for o in self.objs:
      yield o
  
  
  def __getitem__(self, obj) -> Union[list[PFGeneral], PFGeneral]:
    return self.get_by_loc_name_with_class(obj)     
  
  
  def append(self, obj:PFGeneral):
    self.objs.append(obj)
  
  
  def get_by_loc_name(self, obj:str) -> filter:
    return filter(lambda x: fnmatch(x.loc_name, obj), self.objs) 
    
    
  def get_by_loc_name_with_class(self, obj:str) -> filter:
    return filter(lambda x: fnmatch(x.loc_name + "." + x.GetClassName(), obj), self.objs)  
    
  
  def get_by_path_in_project(self, obj:str, pf_app) -> filter:
    return filter(
      lambda x: fnmatch(
      powfacpy.PFStringManipulation._format_full_path(str(x), pf_app), obj), 
      self.objs)
    