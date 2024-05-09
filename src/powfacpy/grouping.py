from __future__ import annotations
import sys
from typing import Iterable, Union
from fnmatch import fnmatch
from collections.abc import Generator, Callable
from math import inf

from icecream import ic

sys.path.insert(0, r'.\src')
import powfacpy
from powfacpy.pf_class_protocols import *




class PFSet():
  
  def __init__(self, set:SetSelect) -> None:
    self.set:SetSelect = set
    
  def get_all_elements(self):
    return self.set.All()  
  
  
class GroupOfObjects():
  
  def __init__(self, objects:Iterable[PFGeneral] | Callable) -> None:
    self.objs = objects
     
    
  @property
  def objs(self) -> Iterable[PFGeneral]:
    if self._objs:
      return self._objs
    else:
      return self._call_objs()
    
    
  @objs.setter
  def objs(self, objects:Iterable[PFGeneral] | Callable):
    if isinstance(objects, Callable):
      self._call_objs:Callable = objects
      self._objs:Iterable[PFGeneral] = []
    else:  
      self._objs:Iterable[PFGeneral] = objects
      
                  
  def __iter__(self):
    for o in self.objs:
      yield o
  
  
  def __getitem__(self, obj) -> Union[list[PFGeneral], PFGeneral]:
    return self.get_by_loc_name_with_class(obj)    
  
  
  def cache(self):
    self._objs = self._call_objs()
    
  
  def free_cache(self):
    self._objs = [] 
    
  
  def freeze(self):
    self._objs = set(self._objs)
  
  
  def append(self, obj:PFGeneral):
    self.objs.append(obj)
  
  
  def get_by_loc_name(self, obj:str) -> filter:
    return filter(lambda x: fnmatch(x.loc_name, obj), self.objs) 
    
    
  def get_by_loc_name_with_class(self, obj:str) -> filter:
    return filter(lambda x: fnmatch(x.loc_name + "." + x.GetClassName(), obj), self.objs)  
    
  
  def get_by_path_in_project(self, obj:str, pf_app) -> filter:
    return filter(
      lambda x: fnmatch(
      powfacpy.PFStringManipulation.format_full_path(str(x), pf_app), obj), 
      self.objs)
    
  
  def filter(self, function:Callable):
    return filter(function, self.objs)  
 

class Subsystem():

  def __init__(self, 
               elms:list[PFGeneral] = [],
               name:str = "",
               parent:Subsystem = None) -> None:
    self.name: str = name
    self.elms: list[PFGeneral] = elms
    self.parent: Subsystem = parent
    self.children: list[Subsystem] = []
    self.categories: list[str] = []

  
  def add_subsystem(self, subsystem: Subsystem):
    self.children.append(subsystem)
    self.elms = set(self.elms) - set(subsystem.elms)
  
  
  def get_subsystems(self, 
                     include: Callable[[Subsystem], bool] = lambda x: True,
                     stop_at: Callable[[Subsystem], bool] = lambda x: False, 
                     depth = inf, 
                     start_depth = 0) -> Generator[Subsystem]:
    if depth > 0:
      for ss in self.children:
        if start_depth < 1:
          if not stop_at(ss): 
            if include(ss):
              yield ss
            for subsubsystem in ss.get_subsystems(include,
                                                  stop_at,
                                                  depth=depth-1,start_depth=start_depth-1):
              yield subsubsystem
  
  
  def get_subsytems_by_names(self, 
                             names, 
                             stop_at_names, 
                             depth:int = inf, 
                             start_depth = 0) -> Generator[Subsystem]:
    return self.get_subsystems(lambda x: x.name in names, 
                        lambda x: x.name in stop_at_names)
    
  
  def get_subsystems_by_categories(self, 
                                   categories: list[str], 
                                   stop_at_categories: list[str], 
                                   depth:int = inf, 
                                   start_depth = 0) -> Generator[Subsystem]:
    categories_fun = lambda x: any([x in categories for x in self.categories])
    stop_at_categories_fun = lambda x: any([x in stop_at_categories for x in self.categories])
    return self.get_subsystems(categories_fun, 
                        stop_at_categories_fun,
                        depth,
                        start_depth) 
    
  
  def get_subsystems_by_all_categories(
    self, 
    categories: list[str], stop_at_categories: list[str], 
    depth:int = inf, 
    start_depth = 0) -> Generator[Subsystem]:
      
    categories_fun = lambda x: all([x in categories for x in self.categories])
    stop_at_categories_fun = lambda x: any([x in stop_at_categories for x in self.categories])
    return self.get_subsystems(categories_fun, 
                        stop_at_categories_fun,
                        depth,
                        start_depth)
  
  
  def get_all_subsystems(self) -> Generator[Subsystem]:
    for ss in self.children:
      yield ss
      for subsubsystem in ss.get_all_subsystems():
        yield subsubsystem
        
  
  def get_all_elms(self) -> Generator[PFGeneral]:
    for elm in self.elms:
      yield elm
    for ss in self.get_all_subsystems():
      for elm in ss.get_all_elms():
        yield elm      
                
        
  def is_in_elms_of(self, 
                    subsystem:Subsystem, 
                    depth:int = inf,
                    start_depth:int = 0):

    if start_depth < 1 and all([x in subsystem.elms for x in self.elms]):
      return subsystem
    elif depth > 0:
      for ss in subsystem.children:
        found_ss = self.is_in_elms_of(ss, 
                                      depth=depth-1, start_depth=start_depth-1)  
        if found_ss:
          return found_ss        
    return None
  
     
  def get_elements_incl_children(self) -> list:
    elements = self.internal_elements
    for subsys in self.children:
      elements += subsys.get_elements_incl_children()
    return elements  
    

class PFZoneInterface(powfacpy.PFActiveProject):
  
  def __init__(self, 
               pf_app: powfacpy.PFApp, 
               elms:list[PFGeneral] = []) -> None:
    super().__init__(pf_app)
    self.zone_obj:ElmZone
    
  
  # def create_zone(self, elms) -> None:
       
    
  
    