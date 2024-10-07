from typing import Callable

from powfacpy.pf_classes.protocols import PFGeneral

def cache_attr(obj: PFGeneral, attr: str):
    obj.__dict__[attr] = obj.__getattr__(attr) 
        
def cache_attrs(
    obj: PFGeneral, 
    attrs: list[str]):
    for attr in attrs:
        obj.__dict__[attr] = obj.__getattr__(attr)        
      
def cache_method(obj: PFGeneral, method: str):
    return_val = getattr(obj, method)()
    obj.__dict__[method] = lambda: return_val
      
def cache_methods(
    obj: PFGeneral, 
    methods: list[str]):
    for method in methods:
        cache_method(obj, method)

