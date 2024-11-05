from abc import ABC, abstractmethod

import math

import powfacpy
from powfacpy.pf_class_protocols import *
from powfacpy.result_variables import ResVar



rms_bal = ResVar.RMS_Bal
lf_bal = ResVar.LF_Bal


class PFElm(ABC, PFGeneral):
  
  def __init__(self, pf_obj) -> None:
    self.pf_obj:PFGeneral = pf_obj 
    
  def set_out_of_service(self):
    self.pf_obj.outserv = 1    
    
  def set_into_service(self):
    self.pf_obj.outserv = 0   
  
  def get_bus_index_of_terminal(self, connected_terminal:ElmTerm):
    self.get_connected_elms_ordered().index(connected_terminal)
 

class StandardLoadFlowElm(ABC):
  
  def __init__(self) -> None:
    self.pf_obj:ElmSym | ElmGenstat

############################
# S
############################
  @property
  def S_nom(self) -> float:
    return self.pf_obj.sgn
  
  
  @S_nom.setter
  def S_nom(self, S_nom:float):
    self.pf_obj.sgn = S_nom
    
  
  @property
  def S(self) -> float:
    return math.sqrt(self.P**2 + self.Q**2)
 
 
  @property
  def s_pu(self) -> float:
    return math.sqrt(self.P**2 + self.Q**2)/self.S_nom    
  
  
  def scale_s(self, factor:float):
    self.scale_p(factor)
    self.scale_q(factor)    

############################
# P
############################   
  @property  
  def P(self) -> float:
    return self.pf_obj.pgini
  
  
  @P.setter
  def P(self, P:float):
    self.pf_obj.pgini = P
    
  
  @property 
  def p_pu(self) -> float:
    return self.pf_obj.pgini/self.S_nom
  
  
  @p_pu.setter
  def p_pu(self, p_pu:float) -> None:
    self.pf_obj.pgini = p_pu * self.S_nom
  
  
  @property
  def P_max(self) -> float:
    return self.pf_obj.Pmax_uc
  
  
  @property
  def p_max_pu(self) -> float:
    return self.P_max/self.S_nom
  
  
  @property
  def P_min(self) -> float:
    return self.pf_obj.Pmin_uc
  
  @property
  def p_min_pu(self) -> float:
    return self.P_min/self.S_nom


  def get_P_margin(self) -> tuple[float, float]:
    return self.P_min - self.P, self.P_max - self.P
      
      
  def get_p_margin_pu(self) -> tuple[float, float]:
    return self.p_min_pu - self.p_pu, self.p_max_pu - self.p_pu  
  

  def scale_p(self, factor:float):
    self.pf_obj.pgini *= factor  
    
      
  def set_p_and_adapt_limits(self, p_pu):
    self.pf_obj.pgini = p_pu
    P_MW = p_pu*self.pf_obj.typ_id.sgn
    if P_MW > self.pf_obj.Pmax_uc:
      self.pf_obj.Pmax_uc = P_MW
    elif P_MW < self.pf_obj.Pmin_uc:  
      self.pf_obj.Pmin_uc = P_MW  
  
############################
# Q
############################  
  @property
  def Q(self) -> float:
    return self.pf_obj.qgini
  

  @Q.setter
  def Q(self, Q:float) -> None:
    self.pf_obj.qgini = Q   
  
  
  @property
  def q_pu(self) -> float:
    return self.pf_obj.qgini/self.S_nom


  @q_pu.setter   
  def q_pu(self, q_pu:float) -> None:
    self.pf_obj.qgini = q_pu * self.S_nom
  
  
  @property
  def Q_max(self) -> float:
    return self.pf_obj.cQ_max
  
  
  @property
  def q_max_pu(self) -> float:
    return self.pf_obj.cQ_min
  
  
  @property
  def Q_min(self) -> float:
    return self.pf_obj.Qmin_uc
  
  
  @property
  def q_min_pu(self) -> float:
    return self.pf_obj.q_min

  
  def get_Q_margin(self) -> tuple[float, float]:
    return self.Q_min - self.Q, self.Q_max - self.Q
  
  
  def get_q_margin_pu(self) -> tuple[float, float]:
    return self.q_min_pu - self.q_pu, self.q_max_pu - self.q_pu

  
  def scale_q(self, factor:float):
    self.pf_obj.qgini *= factor 
    
  
  def set_q_and_adapt_limits(self, q_pu):
    self.pf_obj.qgini = q_pu
    if q_pu > self.pf_obj.qmax:
      self.pf_obj.q_max = q_pu
    elif q_pu > self.pf_obj.qmin:  
      self.pf_obj.q_min = q_pu     
      
############################
# U
############################
  @property  
  def u(self, u_pu:float) :
    return self.pf_obj.usetp
    
  
  @u.setter  
  def u(self, u_pu:float) :
    self.pf_obj.usetp = u_pu   
    
  
  def set_dispatch_input_mode(self, mode):
    self.mode_inp = mode
    
  
      
class StaticGenerator(PFElm, StandardLoadFlowElm):
  
  def __init__(self, pf_obj: ElmGenstat) -> None:
    self.pf_obj: ElmGenstat = pf_obj  
    
    
  def set_short_circuit_impedance_uk(self, uk) -> None: 
    self.pf_obj.uk = uk 
    

  def get_connected_elms_ordered(self) -> list[PFGeneral]:
    return [self.pf_obj.bus1.cterm] 
    
 
  
class SynchronousMachine(PFElm, StandardLoadFlowElm):
  
  def __init__(self, pf_obj:ElmSym) -> None:
    self.pf_obj:ElmSym = pf_obj 
  
  @property  
  def S_nom(self) -> float:
    return self.pf_obj.typ_id.sgn 
  
  @S_nom.setter
  def S_nom(self, S_nom:float) -> None:
    """
    Changes type

    Args:
        s (_type_): _description_
    """
    self.pf_obj.typ_id.sgn = S_nom
    
  def set_local_controller_mode_for_load_flow(self,mode):
    self.av_mode = mode 
    
  def get_connected_elms_ordered(self) -> list[PFGeneral]:
    return [self.pf_obj.bus1]  



class Line(PFElm):

  def __init__(self, pf_obj:ElmLne) -> None:
    self.pf_obj:ElmLne = pf_obj
  
  def get_connected_elms_ordered(self) -> list[PFGeneral]:
    return [self.pf_obj.bus1.cterm, self.pf_obj.bus2.cterm] 
  
  def get_P_res_var_lf_bal(self,
                           bus_index: int | slice = slice(0,None)):
    return [lf_bal.ElmLne.m_Psum_bus1.value, 
            lf_bal.ElmLne.m_Psum_bus2.value][bus_index]
  
  def get_Q_res_var_lf_bal(self,
                           bus_index: int | slice = slice(0,None)):
    return [lf_bal.ElmLne.m_Qsum_bus1.value, 
            lf_bal.ElmLne.m_Qsum_bus2.value][bus_index]
  
  def get_P_res_var_rms_bal(self, 
                            bus_index: int | slice = slice(0,None)):
    return [rms_bal.ElmLne.m_Psum_bus1.value, 
            rms_bal.ElmLne.m_Psum_bus2.value][bus_index]
  
  def get_Q_res_var_rms_bal(self,
                            bus_index: int | slice = slice(0,None)):
    return [rms_bal.ElmLne.m_Qsum_bus1.value, 
            rms_bal.ElmLne.m_Qsum_bus2.value][bus_index]
  
  
class Transformer2Winding(PFElm):

  def __init__(self, pf_obj: ElmTr2) -> None:
    self.pf_obj:ElmTr2 = pf_obj
    
  def get_connected_elms_ordered(self) -> list[PFGeneral]:
    return [self.pf_obj.bushv.cterm, self.pf_obj.buslv.cterm] 
  
  def get_P_res_var_rms_bal(self, 
                            bus_index: int | slice = slice(0,None)):
    return [rms_bal.ElmTr2.m_Psum_bushv.value, 
            rms_bal.ElmTr2.m_Psum_buslv][bus_index]
  
  def get_Q_res_var_rms_bal(self,
                            bus_index: int | slice = slice(0,None)):
    return [rms_bal.ElmTr2.m_Qsum_bushv.value, 
            rms_bal.ElmTr2.m_Qsum_buslv.value][bus_index]
  

class Transformer3Winding(PFElm):

  def __init__(self, pf_obj:ElmTr3) -> None:
    self.pf_obj: ElmTr3 = pf_obj
    
  def get_connected_elms_ordered(self) -> list[PFGeneral]:
    return [self.pf_obj.bushv.cterm, self.pf_obj.busmv.cterm, self.pf_obj.buslv.cterm] 
 

class Terminal(PFElm):
  
  def __init__(self, pf_obj: ElmTerm) -> None:
    self.pf_obj: ElmTerm = pf_obj 
    
  def get_connected_elms_ordered(self) -> list[PFGeneral]:
    return self.pf_obj.GetConnectedElements()  


class Site(PFElm):
  """Network components including Substations and Branches can be grouped together within a “Site” (ElmSite). This may include Elements such as substations / busbars at different voltage levels.
  (from manual)
  """
  
  def __init__(self, pf_obj: ElmSite) -> None:
    self.pf_obj: ElmSite = pf_obj 
    
  def get_substations(self):
    return self.get_obj("*.ElmSubstat", 
                        parent_folder=self.pf_obj, 
                        condition=lambda x: x.GetClassName() == "ElmSubstat")
    
  def set_area_of_substations(self, area: ElmArea):
    for ss in self.get_substations():
      ss.pArea = area  
      
  def set_zone_of_substations(self, zone: ElmZone):     
    for ss in self.get_substations():
      ss.pZone = zone 


class Area(PFElm):

  def __init__(self, pf_obj: ElmArea) -> None:
    self.pf_obj: ElmArea = pf_obj
    
  def get_P_exchange_res_var_lf_bal() -> str:
    return lf_bal.ElmArea.c_InterP.value
  
  def get_Q_exchange_res_var_lf_bal() -> str:
    return lf_bal.ElmArea.c_InterQ.value
  
  def get_P_exchange_res_var_rms_bal() -> str:
    return rms_bal.ElmArea.c_Pinter.value
  
  def get_Q_exchange_res_var_rms_bal() -> str:
    return rms_bal.ElmArea.c_Qinter.value
  

class Zone(PFElm):

  def __init__(self, pf_obj: ElmZone) -> None:
    self.pf_obj: ElmZone = pf_obj    
  
  @staticmethod
  def get_P_exchange_res_var_lf_bal() -> str:
    return lf_bal.ElmZone.c_InterP.value
  
  @staticmethod
  def get_Q_exchange_res_var_lf_bal() -> str:
    return lf_bal.ElmZone.c_InterQ.value  
  
  @staticmethod
  def get_P_exchange_res_var_rms_bal() -> str:
    return rms_bal.ElmZone.c_Pinter.value
  
  @staticmethod
  def get_Q_exchange_res_var_rms_bal() -> str:
    return rms_bal.ElmZone.c_Qinter.value
  
  def add_results_variable_F_rms_bal_of_all_terminals(
    self, 
    pfp: powfacpy.PFActiveProject) -> None:
    for terminal in self.pf_obj.GetBuses():
      pfp.add_results_variable(terminal, rms_bal.ElmTerm.m_fehz.value)
  
  def add_results_variable_f_rms_bal_of_all_terminals(
    self, 
    pfp: powfacpy.PFActiveProject) -> None:
    for terminal in self.pf_obj.GetBuses():
      pfp.add_results_variable(terminal, rms_bal.ElmTerm.m_fe.value)  
  

    
  
  
# Add new element classes ABOVE
# ------------------------------------------------------------------------------


elm_classes:dict[str, PFGeneral] = {
  "ElmGenstat": StaticGenerator,
  "ElmSym": SynchronousMachine, 
  "ElmLne": Line,  
  "ElmTr2": Transformer2Winding,
  "ElmTr3": Transformer3Winding,
  "ElmTerm": Terminal,
  "ElmSite": Site,
  "ElmArea": Area,
  "ElmZone": Zone,
} 


def create_elm_object(pf_elm_object) -> PFElm:
  class_name:str = pf_elm_object.GetClassName()
  elm_class:PFGeneral = elm_classes.get(class_name)
  if elm_class:
    return elm_class(pf_elm_object)
  else:
    return PFElm(pf_elm_object)
