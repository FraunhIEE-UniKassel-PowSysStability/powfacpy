"""Protocol classes for (almost) all PowerFactory classes in the python scripting reference pdf file (and more). Protocol classes are helpful for example for type hints where they can be used just like 'normal' implementations of classes.
"""

from typing import Protocol


class PFGeneral(Protocol):
    """Class with general methods (see Section 'General Methods' in scripting reference. All other classes (except for PFApp) inherit from this class)."""

    def GetAttributeLength(*args): ...

    def GetChildren(*args): ...

    def GetContents(*args): ...

    def GetSupplyingTransformers(*args): ...

    def GetAttributeType(*args): ...

    def GetUnom(*args): ...

    def ReportNonAsciiCharacters(*args): ...

    def IsInFeeder(*args): ...

    def GetZeroImpedance(*args): ...

    def PurgeUnusedObjects(*args): ...

    def SetAttribute(*args): ...

    def SwitchOff(*args): ...

    def GetCubicle(*args): ...

    def PasteCopy(*args): ...

    def GetClassName(*args): ...

    def GetCombinedProjectSource(*args): ...

    def CreateObject(*args): ...

    def GetParent(*args): ...

    def IsDeleted(*args): ...

    def GetAttributeUnit(*args): ...

    def AddCopy(*args): ...

    def Move(*args): ...

    def GetSupplyingSubstations(*args): ...

    def GetAttribute(*args): ...

    def GetAttributes(*args): ...

    def GetReferences(*args): ...

    def IsReducible(*args): ...

    def SwitchOn(*args): ...

    def GetSupplyingTrfstations(*args): ...

    def IsNode(*args): ...

    def IsCalcRelevant(*args): ...

    def SetAttributeShape(*args): ...

    def SetAttributeLength(*args): ...

    def HasResults(*args): ...

    def MarkInGraphics(*args): ...

    def GetNode(*args): ...

    def IsObjectModifiedByVariation(*args): ...

    def GetSystemGrounding(*args): ...

    def Energize(*args): ...

    def SearchObject(*args): ...

    def HasAttribute(*args): ...

    def WriteChangesToDb(*args): ...

    def IsOutOfService(*args): ...

    def IsShortCircuited(*args): ...

    def ReplaceNonAsciiCharacters(*args): ...

    def ShowModalSelectTree(*args): ...

    def ContainsNonAsciiCharacters(*args): ...

    def IsNetworkDataFolder(*args): ...

    def GetOwner(*args): ...

    def ShowEditDialog(*args): ...

    def GetAttributeDescription(*args): ...

    def GetImpedance(*args): ...

    def IsEnergized(*args): ...

    def IsHidden(*args): ...

    def Isolate(*args): ...

    def Delete(*args): ...

    def GetInom(*args): ...

    def IsObjectActive(*args): ...

    def ReportUnusedObjects(*args): ...

    def GetRegion(*args): ...

    def GetControlledNode(*args): ...

    def GetConnectedElements(*args): ...

    def GetOperator(*args): ...

    def IsEarthed(*args): ...

    def GetConnectionCount(*args): ...

    def GetAttributeShape(*args): ...

    def GetFullName(*args): ...

    def SetAttributes(*args): ...

    def CopyData(*args): ...


class PFApp(Protocol):
    __version__: str

    def ActivateProject(*args): ...

    def ClearOutputWindow(*args): ...

    def ClearRecycleBin(*args): ...

    def CloseTableReports(*args): ...

    def CommitTransaction(*args): ...

    def ConvertGeometryStringToMDL(*args): ...

    def CreateFaultCase(*args): ...

    def CreateProject(*args): ...

    def DecodeColour(*args): ...

    def DefineTransferAttributes(*args): ...

    def EchoOff(*args): ...

    def EchoOn(*args): ...

    def EncodeColour(*args): ...

    def ExecuteCmd(*args): ...

    def FlushOutputWindow(*args): ...

    def GetActiveCalculationStr(*args): ...

    def GetActiveNetworkVariations(*args): ...

    def GetActiveProject(*args): ...

    def GetActiveScenario(*args): ...

    def GetActiveScenarioScheduler(*args): ...

    def GetActiveStages(*args): ...

    def GetActiveStudyCase(*args): ...

    def GetAllUsers(*args): ...

    def GetBorderCubicles(*args): ...

    def GetBrowserSelection(*args): ...

    def GetCalcRelevantObjects(*args): ...

    def GetClassDescription(*args): ...

    def GetClassId(*args): ...

    def GetCurrentDiagram(*args): ...

    def GetCurrentScript(*args): ...

    def GetCurrentSelection(*args): ...

    def GetCurrentUser(*args): ...

    def GetCurrentZoomScaleLevel(*args): ...

    def GetDataFolder(*args): ...

    def GetDiagramSelection(*args): ...

    def GetFlowOrientation(*args): ...

    def GetFromStudyCase(*args): ...

    def GetGlobalLibrary(*args): ...

    def GetGraphicsBoard(*args): ...

    def GetInstallDir(*args): ...

    def GetInstallationDirectory(*args): ...

    def GetInterfaceVersion(*args): ...

    def GetLanguage(*args): ...

    def GetLocalLibrary(*args): ...

    def GetMem(*args): ...

    def GetOutputWindow(*args): ...

    def GetProjectFolder(*args): ...

    def GetRandomNumber(*args): ...

    def GetRandomNumberEx(*args): ...

    def GetRecordingStage(*args): ...

    def GetSettings(*args): ...

    def GetStudyTimeObject(*args): ...

    def GetSummaryGrid(*args): ...

    def GetTableReports(*args): ...

    def GetTempDir(*args): ...

    def GetTemporaryDirectory(*args): ...

    def GetTouchedObjects(*args): ...

    def GetTouchingExpansionStages(*args): ...

    def GetTouchingStageObjects(*args): ...

    def GetTouchingVariations(*args): ...

    def GetUserManager(*args): ...

    def GetUserSettings(*args): ...

    def GetWorkingDir(*args): ...

    def GetWorkspaceDirectory(*args): ...

    def Hide(*args): ...

    def ImportDz(*args): ...

    def ImportSnapshot(*args): ...

    def InvertMatrix(*args): ...

    def IsAttributeModeInternal(*args): ...

    def IsAutomaticCalculationResetEnabled(*args): ...

    def IsFinalEchoOnEnabled(*args): ...

    def IsLdfValid(*args): ...

    def IsNAN(*args): ...

    def IsRmsValid(*args): ...

    def IsScenarioAttribute(*args): ...

    def IsShcValid(*args): ...

    def IsSimValid(*args): ...

    def IsWriteCacheEnabled(*args): ...

    def LicenceHasModule(*args): ...

    def LoadProfile(*args): ...

    def OutputFlexibleData(*args): ...

    def PostCommand(*args): ...

    def PrintError(*args): ...

    def PrintInfo(*args): ...

    def PrintPlain(*args): ...

    def PrintWarn(*args): ...

    def Rebuild(*args): ...

    def ReloadProfile(*args): ...

    def ResGetData(*args): ...

    def ResGetDescription(*args): ...

    def ResGetFirstValidObject(*args): ...

    def ResGetFirstValidObjectVariable(*args): ...

    def ResGetFirstValidVariable(*args): ...

    def ResGetIndex(*args): ...

    def ResGetMax(*args): ...

    def ResGetMin(*args): ...

    def ResGetNextValidObject(*args): ...

    def ResGetNextValidObjectVariable(*args): ...

    def ResGetNextValidVariable(*args): ...

    def ResGetObject(*args): ...

    def ResGetUnit(*args): ...

    def ResGetValueCount(*args): ...

    def ResGetVariable(*args): ...

    def ResGetVariableCount(*args): ...

    def ResLoadData(*args): ...

    def ResReleaseData(*args): ...

    def ResSortToVariable(*args): ...

    def ResetCalculation(*args): ...

    def RndExp(*args): ...

    def RndGetMethod(*args): ...

    def RndGetSeed(*args): ...

    def RndNormal(*args): ...

    def RndSetup(*args): ...

    def RndUnifInt(*args): ...

    def RndUnifReal(*args): ...

    def RndWeibull(*args): ...

    def SaveAsScenario(*args): ...

    def SearchObjectByForeignKey(*args): ...

    def SelectToolbox(*args): ...

    def SetAttributeModeInternal(*args): ...

    def SetAutomaticCalculationResetEnabled(*args): ...

    def SetEnableUserBreak(*args): ...

    def SetFinalEchoOnEnabled(*args): ...

    def SetGraphicUpdate(*args): ...

    def SetGuiUpdateEnabled(*args): ...

    def SetInterfaceVersion(*args): ...

    def SetOutputWindowState(*args): ...

    def SetProgressBarUpdatesEnabled(*args): ...

    def SetRandomSeed(*args): ...

    def SetRescheduleFlag(*args): ...

    def SetShowAllUsers(*args): ...

    def SetUserBreakEnabled(*args): ...

    def SetWriteCacheEnabled(*args): ...

    def Show(*args): ...

    def ShowModalBrowser(*args): ...

    def ShowModalSelectBrowser(*args): ...

    def ShowModelessBrowser(*args): ...

    def SplitLine(*args): ...

    def StatFileGetXrange(*args): ...

    def StatFileResetXrange(*args): ...

    def StatFileSetXrange(*args): ...

    def UpdateTableReports(*args): ...

    def __getattr__(*args): ...


class ElmArea(PFGeneral):
    InterPset: float
    "Consider Interchange Schedule: Scheduled Active Power Interchange"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cimRdfId: list
    "RDF ID"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iInterChg: int
    "Consider Interchange Schedule"
    iSchemeStatus: int
    "Scheme Status"
    icolor: int
    "Colour"
    isConsSpinReserve: int
    "Min. spinning reserve constraint"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    spinReserve: float
    "Min. spinning reserve constraint: Spinning reserve"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CalculateInterchangeTo(*args): ...

    def CalculateVoltInterVolt(*args): ...

    def CalculateVoltageLevel(*args): ...

    def DefineBoundary(*args): ...

    def GetAll(*args): ...

    def GetBranches(*args): ...

    def GetBuses(*args): ...

    def GetObjs(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmAsm(PFGeneral):
    EDS: float
    "Stochastic Model for Generation: Expectancy of derated states"
    FAY: float
    "Stochastic Model for Generation: Full Availability Expectancy"
    FOE: float
    "Stochastic Model for Generation: Forced Outage Expectancy"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    IkWDmax: float
    "Steady-state short-circuit current contribution: Maximum current"
    IkWDmin: float
    "Steady-state short-circuit current contribution: Minimum current"
    Iks: float
    "Fault Contribution: Transient Short-Circuit Current"
    Inom: float
    "Nominal Current"
    Irated: float
    "Harmonic Current Injections: Rated Current"
    Irze: list
    "Rated current of grounding"
    Jme: float
    "Mechanical load: Moment of Inertia"
    Kfactor: float
    "Fault Contribution: K Factor"
    Kpf: float
    "Dispatch: Prim. frequency bias"
    P_max: float
    "Active power: Ratings: Max."
    PmaxInv: float
    "Separate consumption mode: Max."
    PmaxInvPU: float
    "Separate consumption mode: Max."
    Pmax_uc: float
    "Active power operational limits: Max."
    Pmax_ucPU: float
    "Active power operational limits: Max."
    PminInv: float
    "Separate consumption mode: Min."
    PminInvPU: float
    "Separate consumption mode: Min."
    Pmin_uc: float
    "Active power operational limits: Min."
    Pmin_ucPU: float
    "Active power operational limits: Min."
    Pngrel: float
    "Stochastic Model for Generation: Based on rated active power (Pr)"
    Pnom: float
    "Active power operational limits: Pr(rated)"
    QtargetBase: int
    "Optimisation of reactive power reserve: Base:Reactive power limits:Rated apparent power"
    QtargetRPR: float
    "Optimisation of reactive power reserve: Q target value"
    Re: float
    "Internal grounding impedance: Resistance, Re"
    T1ph: float
    "Switch after"
    Tbypass: float
    "Reactor: Bypass after"
    Tstaroff: float
    "Auto transformer: Release star contactor after"
    Tyd: float
    "Switch to 'D' after"
    Xe: float
    "Internal grounding impedance: Reactance, Xe"
    aCategory: str
    "Plant Category"
    aSubCategory: str
    "Subcategory"
    allowConsumMode: int
    "Separate consumption mode"
    allowGenMode: int
    "Separate generation mode"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    autotap: float
    "Auto transformer: Tap:85:65:50"
    av_mode: str
    "Local controller"
    availFactor: float
    "Availability Factor"
    avgCosts: float
    "Average costs"
    avgCostsUc: float
    "Piecewise linearisation for LP: Average costs"
    beta: float
    "Wind Model Weibull Distribution for Wind Speed: Beta"
    bus1: object
    "Terminal"
    bus1n: object
    "Neutral conductor: Neutral"
    bustp: str
    "Bus type:AS:PQ"
    bustpc: str
    "Corresponding bus type:"
    cCategory: str
    "Plant Category"
    cDisplayName: str
    "Display Name"
    cIsDiscreteCtrlP: int
    "Restriction to discrete active power values"
    cIsMustRunUC: int
    "Additional constraints for controls: Must run"
    cIsPcurrAllowed: int
    "Allow current active power value"
    cJ: float
    "Mechanical load: Moment of Inertia from Type"
    cJtot: float
    "Mechanical load: Total Moment of Inertia"
    cOperSpeed: float
    "Slip Settings: Operating speed"
    cQ_max: float
    "Reactive power operational limits: Maximum"
    cQ_min: float
    "Reactive power operational limits: Minimum"
    cStorage: object
    "Generator usage: Storage model"
    cSubCategory: str
    "Subcategory"
    cTypHmc: str
    "Harmonic Current Injections: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    cVecDiscreteCtrlPvals: list
    "Valid active power values"
    c_pmdm: object
    "Mechanical load: Mdm"
    c_pmod: object
    "Model"
    c_pstac: object
    "External station controller"
    ccost: list
    "Costs"
    cfixedCosts: float
    "Consumption mode: Fixed costs"
    cgnd: int
    "Internal grounding impedance: Star Point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    chr_p: list
    "Slip Settings: Active Power"
    chr_slip: list
    "Slip Settings: slip"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cnwsamples: int
    "Wind Model Time Series Characteristics: Annual Samples: Number of Samples"
    coldStartTime: float
    "Start-up costs: Cold-start time"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    consumCosts: float
    "Consumption mode: Consumption costs"
    cosgini: float
    "Dispatch: Power factor"
    cosgini_a: float
    "Actual Dispatch: Power Factor (act.)"
    costColdStart: float
    "Start-up costs: Cold-start costs"
    costCurtailment: float
    "Costs for curtailment"
    costRedispatchDown: float
    "Additional redispatch costs: Downward active power redispatch costs"
    costRedispatchP: float
    "Redispatch costs for active power change"
    costRedispatchQ: float
    "Redispatch costs for reactive power change"
    costRedispatchUp: float
    "Additional redispatch costs: Upward active power redispatch costs"
    costShutDown: float
    "Shut-down costs"
    cost_up: float
    "Start-up costs: Warm-start costs"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpower: list
    "Power"
    crotor: list
    "Additional rotor resistance"
    crradd: float
    "Additional rotor resistance"
    crrspeed: float
    "Speed"
    crrtime: float
    "Time"
    cspeed: list
    "Speed"
    ctagtot: float
    "Mechanical load: Total Acceleration Time Const."
    ctime: list
    "Time"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    ddroop: float
    "Voltage Droop: Droop"
    desc: list
    "Description"
    discMethCostOp: int
    "Piecewise linearisation for LP"
    dispatch: int
    "Generator Dispatch"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    drawInrush: int
    "Time-Overcurrent plot: Draw Inrush Current"
    drawStall: int
    "Time-Overcurrent plot: Draw Thermal Overload"
    dsecres: float
    "Reserve"
    efficiencyCurveConsum: object
    "Efficiency: Efficiency curve (consumption)"
    efficiencyCurveGen: object
    "Efficiency: Efficiency curve (generation)"
    efficiencyLPconsum: float
    "Efficiency: Used efficiency (consumption)"
    efficiencyLPgen: float
    "Efficiency: Used efficiency (generation)"
    fixed: int
    "Must run"
    fixedCosts: float
    "Fixed costs"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    genShiftKey: float
    "Generation shift key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    gratio: float
    "Mechanical load: Gear ratio"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iHmcType: int
    "Harmonic Current Injections: Harmonic Model:Norton Equivalent:Ideal Current Source:Impedance"
    iInterPol: int
    "Approximation:Spline:Piecewise linear:Polynomial:Hermite"
    iNoShcContr: int
    "No Short-Circuit Contribution"
    iOPFCPmax: int
    "Active power operational limits: Max."
    iOPFCPmin: int
    "Active power operational limits: Min."
    iOPFCQmax: int
    "Reactive power operational limits: Max."
    iOPFCQmin: int
    "Reactive power operational limits: Min."
    iSchemeStatus: int
    "Scheme Status"
    iShcModel: int
    "Short-Circuit Model:Equivalent synchronous machine:Dynamic voltage support:Doubly fed asynchronous generator"
    iStartMethod: int
    "Motor starting method"
    iTrigg: int
    "Triggered by..."
    iUseStart: int
    "Use motor starting method"
    iWDmax: float
    "Initial symmetrical short-circuit current contribution: Max. instantaneous short-circuit current, iWDmax"
    iWindGen: int
    "Wind generator"
    i_mot: int
    "Generator/Motor"
    i_pset: int
    "State Estimation: Estimate active power"
    i_qset: int
    "State Estimation: Estimate reactive power"
    i_rem: int
    "Remote control"
    iconfed: int
    "Static converter-fed drive"
    ictpg: int
    "Controls: Active Power"
    ictqg: int
    "Controls: Reactive Power"
    icurref: int
    "Harmonic Current Injections: Harmonic currents referred to"
    idfig: int
    "Machine type"
    ignd: int
    "Star Point:&0&grounded:&2&isolated"
    iintgnd: int
    "Neutral conductor: N-Connection:None:At terminal (ABC-N):Separate terminal"
    imax: float
    "Fault Contribution: Max. Current"
    iopt_slip: int
    "Slip Settings"
    iopt_windm: int
    "Wind Model: Wind Model"
    is4SpinReserve: int
    "Consider for region spinning reserve"
    isConsCostOp: int
    "Operating costs"
    isConsCostsRedispatch: int
    "Additional redispatch costs"
    isConsShutDownCost: int
    "Shut-down costs"
    isConsStartUpCost: int
    "Start-up costs"
    isConstrRamp: int
    "Ramp rate constraints"
    isConstrUpDown: int
    "Start-up/shut-down time constraints"
    isCtrlFixedToLdfVal: int
    "Additional constraints for controls: Fix controls to Load Flow values"
    isCtrlP: int
    "Controls: Active power"
    isCtrlPplacement: int
    "Optimise active power"
    isCtrlQ: int
    "Controls: Reactive power"
    isDiscreteCtrlP: int
    "Restriction to discrete active power values"
    isDispatchable: int
    "Generator Dispatch"
    isLimPmax: int
    "Active power operational limits: Max."
    isLimPmin: int
    "Active power operational limits: Min."
    isLimQmax: int
    "Reactive power operational limits: Max."
    isLimQmin: int
    "Reactive power operational limits: Min."
    isMustRunUC: int
    "Additional constraints for controls: Must run"
    isPcurrAllowed: int
    "Restriction to discrete active power values: Allow current active power value"
    isRPR: int
    "Optimisation of reactive power reserve"
    isVRE: int
    "Generator usage: Generator usage:Single thermal generation unit:Variable renewable energy source (VRE):Coupled with storage model:Part of Virtual Power Plant"
    iv_mode: int
    "Local controller"
    kWD: float
    "Initial symmetrical short-circuit current contribution: Factor kappaWD"
    limRampDown: float
    "Ramp rate constraints: Ramp-down limit"
    limRampDownPU: float
    "Ramp rate constraints: Ramp-down limit"
    limRampShutDown: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampShutDownPU: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampStartUp: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampStartUpPU: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampUp: float
    "Ramp rate constraints: Ramp-up limit"
    limRampUpPU: float
    "Ramp rate constraints: Ramp-up limit"
    loc_name: str
    "Name"
    mdTradd: list
    "Variable rotor resistance"
    mdmex: float
    "Mechanical load: Exponent"
    mdmlp: float
    "Mechanical load: Proportional factor"
    mean: float
    "Wind Model Weibull Distribution for Wind Speed: Mean"
    minDownTime: float
    "Start-up/shut-down time constraints: Minimum down-time"
    minUpTime: float
    "Start-up/shut-down time constraints: Minimum up-time"
    mode_inp: str
    "Dispatch: Input mode"
    mode_pgi: int
    "Model:Active power input:Wind speed input"
    monof: int
    "Operation mode"
    ngnum: int
    "Number of: parallel machines"
    numBreakpointsCostOp: int
    "Piecewise linearisation for LP: Number of breakpoints"
    oid_: int
    "ObjectID"
    outServPzero: int
    "Out of service when active power is zero"
    outserv: int
    "Out of Service"
    pBMU: object
    "Virtual Power Plant"
    pCharYrMW: list
    "Wind Model Time Series Characteristics: Annual Samples: Time Series Characteristics of Active Power Contribution (MW)"
    pCharYrWS: list
    "Wind Model Time Series Characteristics: Annual Samples: Time Series Characteristics for Wind Speed (m/s)"
    pFlicker: object
    "Flicker Contribution: Flicker Coefficients"
    pGRStoch: object
    "Stochastic Model for Generation: Stochastic Model"
    pMeteostat: object
    "Wind Model: Meteo Station (Correlation)"
    pOpCostCurve: object
    "Operating costs: Generator cost curve"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pPowerCrv: object
    "Wind Power Curve"
    pQPcurve: object
    "Q(P)-Characteristic: Q(P)-curve"
    pQlimType: object
    "Reactive power operational limits: Capability curve"
    pStorage: object
    "Storage model"
    p_cub: object
    "Controlled branch (Cubicle)"
    p_direc: int
    "Dispatch: Power direction:P>=0:P<0"
    pblocktrf: object
    "Externally modelled unit transformer: Unit transformer"
    penaltyCosts: float
    "Penalty costs"
    pf_recap: int
    "Dispatch: Power factor:ind.:cap."
    pf_recap_a: str
    "Actual Dispatch: Power Factor Ind/Cap (act.)"
    pgini: float
    "Dispatch: Active power"
    pgini_a: float
    "Actual Dispatch: Active Power (act.)"
    pginisum: float
    "Active power"
    phmc: object
    "Harmonic Current Injections: Harmonic Currents"
    phtech: int
    "Technology"
    pid_: int
    "ProjectID"
    pmaxratf: float
    "Active power: Ratings: Rating factor"
    pmini: float
    "Mechanical power"
    pmode: int
    "Input mode:Electrical power:Mechanical power:Mechanical torque"
    polyDegree: int
    "Polynomial degree"
    priority: int
    "Merit Order"
    q_max: float
    "Reactive power operational limits: Max."
    q_min: float
    "Reactive power operational limits: Min."
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qgini: float
    "Dispatch: Reactive power"
    qgini_a: float
    "Actual Dispatch: Reactive Power (act.)"
    r0iec: float
    "Zero sequence short-circuit impedance: Resistance, r0"
    r2iec: float
    "Negative sequence short-cicuit impedance: Resistance, r2"
    ratedStr: float
    "Reactor: Rated apparent power"
    root_id: object
    "Original Location"
    rxWD: float
    "Initial symmetrical short-circuit current contribution: Ratio RWD/XWD"
    scaleQmax: float
    "Reactive power operational limits: Scaling factor (max.)"
    scaleQmin: float
    "Reactive power operational limits: Scaling factor (min.)"
    searchBlockTrf: int
    "Externally modelled unit transformer"
    sernum: str
    "Serial Number"
    sgini: float
    "Dispatch: Apparent power"
    sgini_a: float
    "Actual Dispatch: Apparent Power (act.)"
    shcDeadband: int
    "Voltage deadband"
    slipset: float
    "Slip Settings: Slip"
    smoothfac: float
    "Smoothing factor"
    speed1ph: float
    "Switch at speed >="
    speedbyp: float
    "Reactor: Bypass at speed >="
    speedsoff: float
    "Auto transformer: Release star contactor at speed >="
    speedyd: float
    "Switch to 'D' at speed >="
    stowind: int
    "Wind Model"
    tid_: int
    "TimeID"
    tstart: float
    "Time-Overcurrent plot: Starting Time"
    typ_id: object
    "Type"
    uDeadband: float
    "Voltage deadband: Deadband"
    usetp: float
    "Dispatch: Voltage"
    usp_max: float
    "Voltage setpoint limits: Max. voltage setpoint"
    usp_min: float
    "Voltage setpoint limits: Min. voltage setpoint"
    variance: float
    "Wind Model Weibull Distribution for Wind Speed: Variance"
    vecBreakpointsP: list
    "Piecewise linearisation for LP: Power"
    vecCostRedispatchDown: list
    "Costs"
    vecCostRedispatchUp: list
    "Costs"
    vecDiscreteCtrlPvals: list
    "Restriction to discrete active power values: Valid active power values"
    vecPowerRedispatchDown: list
    "Redispatch"
    vecPowerRedispatchUp: list
    "Redispatch"
    vecStartUpCosts: list
    "Start-up costs: Start-up costs"
    vecStartUpTimes: list
    "Start-up costs: Down-time"
    windspeed: float
    "Dispatch: Wind speed"
    windspeed_a: float
    "Actual Dispatch: Wind speed (act.)"
    x0iec: float
    "Zero sequence short-circuit impedance: Reactance, x0"
    x2iec: float
    "Negative sequence short-cicuit impedance: Reactance, x2"
    xmtini: float
    "Mechanical torque"
    xmtn: float
    "Rated mechanical torque"
    xrea: float
    "Reactor: Reactance"

    def AttributeType(*args): ...

    def CalcEfficiency(*args): ...

    def GetAvailableGenPower(*args): ...

    def GetElecTorque(*args): ...

    def GetGroundingImpedance(*args): ...

    def GetMechTorque(*args): ...

    def GetMotorStartingFlag(*args): ...

    def GetStepupTransformer(*args): ...

    def HasReferences(*args): ...

    def IsPQ(*args): ...

    def __getattr__(*args): ...


class ElmAsmsc(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    IkWDmax: float
    "Steady-state short-circuit current contribution: Maximum current"
    IkWDmin: float
    "Steady-state short-circuit current contribution: Minimum current"
    Iks: float
    "Fault Contribution: Transient Short-Circuit Current"
    Inom: float
    "Nominal Current"
    Irated: float
    "Harmonic Current Injections: Rated Current"
    Irze: list
    "Rated Current of Grounding"
    Kd: float
    "Kd: d-Axis, Proportional Gain"
    Kfactor: float
    "Fault Contribution: K Factor"
    Kq: float
    "Kq: q-Axis, Proportional Gain"
    Pmmax: float
    "Max Pulse Width Modulation Index"
    Pngrel: float
    "Stochastic Model for Generation: Based on rated active power (Pr)"
    Re: float
    "Internal Grounding Impedance: Resistance, Re"
    Td: float
    "Td: d-Axis, Integration Time Constant"
    Tq: float
    "Tq: q-Axis, Integration Time Constant"
    Urot: float
    "Rated Slip Ring Voltage"
    Xe: float
    "Internal Grounding Impedance: Reactance, Xe"
    aCategory: str
    "Plant Category"
    aSubCategory: str
    "Subcategory"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    beta: float
    "Wind Model Weibull Distribution for Wind Speed: Beta"
    bus1: object
    "Terminal AC"
    bus2: object
    "Terminal R"
    cCategory: str
    "Plant Category"
    cDisplayName: str
    "Display Name"
    cOperSpeed: float
    "Operating speed"
    cSubCategory: str
    "Subcategory"
    cTypHmc: str
    "Harmonic Current Injections: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    c_pmod: object
    "Model"
    cgnd: int
    "Internal Grounding Impedance: Star Point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cnwsamples: int
    "Wind Model Time Series Characteristics: Annual Samples: Number of Samples"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cv: float
    "Cv"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iHmcType: int
    "Harmonic Current Injections: Harmonic Model:Norton Equivalent:Current Source:Impedance"
    iNoShcContr: int
    "No Short-Circuit Contribution"
    iSchemeStatus: int
    "Scheme Status"
    iShcModel: int
    "Short-Circuit Model:Equivalent synchronous machine:Dynamic voltage support:Doubly fed asynchronous generator"
    iWDmax: float
    "Initial symmetrical short-circuit current contribution: Max. instantaneous short-circuit current, iWDmax"
    iWindGen: int
    "Wind Generator"
    iZoneBus: int
    "Zone"
    i_conv: int
    "Use Integrated PWM Converter"
    i_ctrl: int
    "Use Built-In Current Controller"
    i_feedback: int
    "Rotor Flux Feed-Back"
    i_mot: int
    "Generator/Motor"
    iconfed: int
    "Static converter-fed drive"
    icurref: int
    "Harmonic Current Injections: Harmonic currents referred to"
    ignd: int
    "Star Point:&0&grounded:&2&isolated"
    imax: float
    "Fault Contribution: Max. Current"
    iopt_windm: int
    "Wind Model: Wind Model"
    kWD: float
    "Initial symmetrical short-circuit current contribution: Factor kappaWD"
    loc_name: str
    "Name"
    mdmex: float
    "Mechanical Load: Exponent"
    mdmlp: float
    "Mechanical Load: Proportional Factor"
    mean: float
    "Wind Model Weibull Distribution for Wind Speed: Mean"
    monof: int
    "Operation Mode"
    ngnum: int
    "Number of: parallel Machines"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCharYrMW: list
    "Wind Model Time Series Characteristics: Annual Samples: Time Series Characteristics of Active Power Contribution (MW)"
    pCharYrWS: list
    "Wind Model Time Series Characteristics: Annual Samples: Time Series Characteristics for Wind Speed (m/s)"
    pFlicker: object
    "Flicker Contribution: Flicker Coefficients"
    pGRStoch: object
    "Stochastic Model for Generation: Stochastic Model"
    pMeteostat: object
    "Wind Model: Meteo Station (Correlation)"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pPowerCrv: object
    "Wind Model: Wind Power Curve"
    p_pctrl: object
    "Controlled Flow"
    pblocktrf: object
    "Externally modelled unit transformer: Unit transformer"
    pgini: float
    "Active Power"
    phmc: object
    "Harmonic Current Injections: Harmonic Currents"
    pid_: int
    "ProjectID"
    qgini: float
    "Reactive Power"
    r0iec: float
    "Zero sequence short-circuit impedance: Resistance, r0"
    r2iec: float
    "Negative sequence short-cicuit impedance: Resistance, r2"
    rcrow: float
    "Rotor-Bypass Settings: Crow-Bar Resistance"
    root_id: object
    "Original Location"
    rxWD: float
    "Initial symmetrical short-circuit current contribution: Ratio RWD/XWD"
    searchBlockTrf: int
    "Externally modelled unit transformer"
    sernum: str
    "Serial Number"
    shcDeadband: int
    "Voltage deadband"
    slipset: float
    "Slip"
    stowind: int
    "Wind Model"
    tid_: int
    "TimeID"
    tstart: float
    "Starting Time"
    typ_id: object
    "Type"
    uDeadband: float
    "Voltage deadband: Deadband"
    variance: float
    "Wind Model Weibull Distribution for Wind Speed: Variance"
    x0iec: float
    "Zero sequence short-circuit impedance: Reactance, x0"
    x2iec: float
    "Negative sequence short-cicuit impedance: Reactance, x2"
    xcrow: float
    "Rotor-Bypass Settings: Crow-Bar Reactance"

    def AttributeType(*args): ...

    def GetAvailableGenPower(*args): ...

    def GetGroundingImpedance(*args): ...

    def GetStepupTransformer(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmBbone(PFGeneral):
    cBbFOR: float
    "Backbone data: Forced outage rate of Backbone"
    cBbLength: float
    "Backbone data: Length of Backbone"
    cBbOrder: int
    "Backbone data: Order"
    cMeanCs: float
    "Backbone data: Mean cross section"
    cMinCs: float
    "Backbone data: Minimum cross section on Backbone"
    cTieOpen: object
    "Tie Open Point"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBbOrder: int
    "Order"
    iCalcMeth: int
    "Calculation method"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pBbEnd: object
    "End"
    pBbStart: object
    "Start"
    pathLoad: float
    "Calculated path load"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CheckBbPath(*args): ...

    def GetBbOrder(*args): ...

    def GetCompleteBbPath(*args): ...

    def GetFOR(*args): ...

    def GetMeanCs(*args): ...

    def GetMinCs(*args): ...

    def GetTieOpenPoint(*args): ...

    def GetTotLength(*args): ...

    def HasGnrlMod(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmBmu(PFGeneral):
    Pmax: float
    "Active power operational limits: Max."
    PmaxConsum: float
    "Separate consumption mode: Max."
    Pmin: float
    "Active power operational limits: Min."
    PminConsum: float
    "Separate consumption mode: Min."
    Psum: float
    "Max. Active Power Sum"
    PsumAct: float
    "Actual Active Power Sum"
    Ptot: float
    "Active Power Setpoint"
    Qmax: float
    "Reactive power operational limits: Max."
    Qmin: float
    "Reactive power operational limits: Min."
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    available_fix: list
    "Available"
    avgCostsUc: float
    "Piecewise linearisation for LP: Average costs"
    cConsumWeightCostSum: float
    "Consumption costs"
    cCostShutDownSum: float
    "Shut-down costs"
    cDiscMethCostOp: int
    "Piecewise linearisation for LP"
    cDisplayName: str
    "Display Name"
    cFixedCostSum: float
    "Fixed costs"
    cLimRampDownSum: float
    "Ramp rate constraints: Ramp-down limit"
    cLimRampShutDownSum: float
    "Ramp rate constraints: Shut-down ramp limit"
    cLimRampStartUpSum: float
    "Ramp rate constraints: Start-up ramp limit"
    cLimRampUpSum: float
    "Ramp rate constraints: Ramp-up limit"
    cMinDownTimeMach: float
    "Start-up/shut-down time constraints: Minimum down-time"
    cMinUpTimeMach: float
    "Start-up/shut-down time constraints: Minimum up-time"
    cNumCtrlsUc: int
    "Unit Commitment: Number of controllable machines"
    cNumDispMachAutoDisp: int
    "Automatic Dispatch: Number of dispatchable machines"
    cNumFixedMachAutoDisp: int
    "Automatic Dispatch: Number of non-dispatchable machines"
    cNumMachQds: int
    "Quasi-Dynamic Simulation: Number of machines for storage model"
    cPenaltyCostWeightSum: float
    "Penalty costs"
    cPowerDistrMethod: int
    "Power distribution"
    cPratedSum: float
    "Restriction to discrete active power values: Pr(rated)"
    cPsumMax: float
    "Active power operational limits: Max."
    cPsumMaxConsum: float
    "Separate consumption mode: Max."
    cPsumMin: float
    "Active power operational limits: Min."
    cPsumMinConsum: float
    "Separate consumption mode: Min."
    cQsumMax: float
    "Reactive power operational limits: Max."
    cQsumMin: float
    "Reactive power operational limits: Min."
    cStorage: object
    "Storage model"
    cSumCostCurtailment: float
    "Costs for curtailment: Costs for curtailment"
    cSumCostRedispDown: float
    "Additional redispatch costs: Downward active power redispatch costs"
    cSumCostRedispQ: float
    "Additional redispatch costs: Redispatch costs for reactive power change"
    cSumCostRedispUp: float
    "Additional redispatch costs: Upward active power redispatch costs"
    cUserDefIndex: int
    "User defined Index"
    ccost: list
    "Operating costs: Costs"
    cfixedCosts: float
    "Consumption mode: Fixed costs"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    colCtrlFixedToLdfVal: list
    "Fix controls to Load Flow values"
    colCtrlP: list
    "Active powercontrol"
    colCtrlQ: list
    "Reactive powercontrol"
    colGenShiftKey: list
    "Generationshift key"
    colGenUsageBmu: list
    "Generatorusage"
    colMachine: list
    "Machine"
    colNomPower: list
    "Rated Power"
    colPrated: list
    "Rated Active Power"
    coldStartTime: float
    "Start-up costs: Cold-start time"
    consumCosts: float
    "Consumption mode: Consumption costs"
    consumMode: int
    "Separate consumption mode"
    contents: list
    "Scripts"
    costColdStart: float
    "Start-up costs: Cold-start costs"
    costCurtailment: float
    "Costs for curtailment: Costs for curtailment"
    costRedispatchDown: float
    "Additional redispatch costs: Downward active power redispatch costs"
    costRedispatchQ: float
    "Additional redispatch costs: Redispatch costs for reactive power change"
    costRedispatchUp: float
    "Additional redispatch costs: Upward active power redispatch costs"
    costShutDown: float
    "Shut-down costs: Shut-down costs"
    cost_up: float
    "Start-up costs: Warm-start costs"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpower: list
    "Operating costs: Power"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    discMethCostOp: int
    "Piecewise linearisation for LP"
    distr_mod: int
    "Distribution Mode"
    fixed: list
    "Must run"
    fixedCosts: float
    "Operating costs: Fixed costs"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAdjustQ: int
    "Adjust Reactive Power accordingly"
    iInterPol: int
    "Operating costs: Approximation:Spline:Piecewise linear:Polynomial:Hermite"
    iNoReserve: int
    "Exclude from reserve allocation"
    iSchemeStatus: int
    "Scheme Status"
    isBmuCurtailCosts: int
    "Costs for curtailment"
    isBmuPlims: int
    "Active power operational limits"
    isBmuQlims: int
    "Reactive power operational limits"
    isConsCostOp: int
    "Operating costs"
    isConsCostsRedispatch: int
    "Additional redispatch costs"
    isConsShutDownCost: int
    "Shut-down costs"
    isConsStartUpCost: int
    "Start-up costs"
    isConstrRamp: int
    "Ramp rate constraints"
    isConstrUpDown: int
    "Start-up/shut-down time constraints"
    isCtrlP: int
    "Controls: Active power"
    isCtrlQ: int
    "Controls: Reactive power"
    isDiscreteCtrlP: int
    "Restriction to discrete active power values"
    isLimPmax: int
    "Active power operational limits: Max."
    isLimPmin: int
    "Active power operational limits: Min."
    isLimQmax: int
    "Reactive power operational limits: Max."
    isLimQmin: int
    "Reactive power operational limits: Min."
    isMustRunUC: int
    "Controls: Must run"
    isPcurrAllowed: int
    "Restriction to discrete active power values: Allow current active power value"
    isRespectLims: int
    "Power distribution: Respect individual operational machine limits"
    limRampDown: float
    "Ramp rate constraints: Ramp-down limit"
    limRampShutDown: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampStartUp: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampUp: float
    "Ramp rate constraints: Ramp-up limit"
    loc_name: str
    "Name"
    machines_disp: list
    "Dispatchable Machines"
    machines_fix: list
    "Non-Dispatchable Machines"
    merit_order: list
    "Merit Order"
    minDownTime: float
    "Start-up/shut-down time constraints: Minimum down-time"
    minUpTime: float
    "Start-up/shut-down time constraints: Minimum up-time"
    numBreakpointsCostOp: int
    "Piecewise linearisation for LP: Number of breakpoints"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOpCostCurve: object
    "Operating costs: Generator cost curve"
    pStorage: object
    "Storage model"
    penaltyCosts: float
    "Operating costs: Penalty costs"
    pid_: int
    "ProjectID"
    plantUsage: int
    "Power plant usage:Thermal generation unit:Variable renewable energy source (VRE):Coupled with storage model"
    polyDegree: int
    "Operating costs: Polynomial degree"
    powerDistrMethod: int
    "Power distribution"
    priority: int
    "Virtual Power Plant, Merit Order"
    root_id: object
    "Original Location"
    smoothfac: float
    "Operating costs: Smoothing factor"
    tid_: int
    "TimeID"
    vecBreakpointsP: list
    "Piecewise linearisation for LP: Power"
    vecCostRedispatchDown: list
    "Costs"
    vecCostRedispatchUp: list
    "Costs"
    vecDiscreteCtrlPvals: list
    "Restriction to discrete active power values: Valid active power values"
    vecPowerRedispatchDown: list
    "Redispatch"
    vecPowerRedispatchUp: list
    "Redispatch"
    vecStartUpCosts: list
    "Start-up costs: Start-up costs"
    vecStartUpTimes: list
    "Start-up costs: Down-time"

    def Apply(*args): ...

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def Update(*args): ...

    def __getattr__(*args): ...


class ElmBoundary(PFGeneral):
    InterPset: float
    "Consider Interchange Schedule: Scheduled Active Power Interchange"
    PlimDecrease: float
    "Active power limits for Unit Commitment: Max. active boundary flow decrease"
    PlimIncrease: float
    "Active power limits for Unit Commitment: Max. active boundary flow increase"
    QlimDecrease: float
    "Reactive power limits for Unit Commitment: Max. reactive boundary flow decrease"
    QlimIncrease: float
    "Reactive power limits for Unit Commitment: Max. reactive boundary flow increase"
    allowCntConstrFiltP: int
    "Active power limits for Unit Commitment: Allow contingency filtering by number of critical constraints"
    allowCntConstrFiltQ: int
    "Reactive power limits for Unit Commitment: Allow contingency filtering by number of critical constraints"
    allowMarginFiltP: int
    "Active power limits for Unit Commitment: Allow filtering by constraint margin"
    allowMarginFiltQ: int
    "Reactive power limits for Unit Commitment: Allow filtering by constraint margin"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    branches: list
    "Branch"
    buses: list
    "Busbar"
    cAllowCntConstrFilt: int
    "Active power limits for Unit Commitment: Allow contingency filtering by number of critical constraints"
    cAllowMarginFilt: int
    "Active power limits for Unit Commitment: Allow filtering by constraint margin"
    cDisplayName: str
    "Display Name"
    cIsSepCntConstrType: int
    "Active power limits for Unit Commitment: Separate constraint type for contingencies"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    ciorient: list
    "Orientation"
    cntConstrTypeP: int
    "Active power limits for Unit Commitment: Contingency-constraint type:Off:Soft constraint"
    cntConstrTypeQ: int
    "Reactive power limits for Unit Commitment: Contingency-constraint type:Off:Soft constraint"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cubicles: list
    "Boundary Cubicle"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    headfold: list
    "Head Folder"
    iComDate: int
    "Commissioning Date"
    iInterChg: int
    "Consider Interchange Schedule"
    iNeutral: int
    "Topological search: consider neutral wire connections"
    iOPFCpsummax: int
    "Active Power Limits: Max. Active Boundary Flow"
    iOPFCpsummin: int
    "Active Power Limits: Min. Active Boundary Flow"
    iOPFCqsummax: int
    "Reactive Power Limits: Max. Reactive Boundary Flow"
    iOPFCqsummin: int
    "Reactive Power Limits: Min. Reactive Boundary Flow"
    iSchemeStatus: int
    "Scheme Status"
    iSimTemp: int
    "Temp"
    iSwitchStates: int
    "Interior Region: Topological search: Stop at open breakers"
    icolor: int
    "Colour"
    iorient: list
    "Orientation"
    isLimDecreaseP: int
    "Active power limits for Unit Commitment: Max. decrease"
    isLimDecreaseQ: int
    "Reactive power limits for Unit Commitment: Max. decrease"
    isLimIncreaseP: int
    "Active power limits for Unit Commitment: Max. increase"
    isLimIncreaseQ: int
    "Reactive power limits for Unit Commitment: Max. increase"
    isLimPmax: int
    "Active power limits for Unit Commitment: Max."
    isLimPmin: int
    "Active power limits for Unit Commitment: Min."
    isLimQmax: int
    "Reactive power limits for Unit Commitment: Max."
    isLimQmin: int
    "Reactive power limits for Unit Commitment: Min."
    isMaxLoadSoftNlinP: int
    "Active power limits for Unit Commitment: Penalty costs for soft constraints"
    isMaxLoadSoftNlinQ: int
    "Reactive power limits for Unit Commitment: Penalty costs for soft constraints"
    isPlimsRel: int
    "Active power limits for Unit Commitment"
    isQlimsRel: int
    "Reactive power limits for Unit Commitment"
    isSepCntConstrTypeP: int
    "Active power limits for Unit Commitment: Separate constraint type for contingencies"
    isSepCntConstrTypeQ: int
    "Reactive power limits for Unit Commitment: Separate constraint type for contingencies"
    isSoftPConstr: int
    "Active Power Limits: Soft constraint (AC OPF only)"
    isSoftPConstrUC: int
    "Active power limits for Unit Commitment: Soft constraint"
    isSoftQConstr: int
    "Reactive Power Limits: Soft constraint (AC OPF only)"
    isSoftQConstrUC: int
    "Reactive power limits for Unit Commitment: Soft constraint"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pid_: int
    "ProjectID"
    psummax: float
    "Active Power Limits: Max. Total Active Power Limit"
    psummin: float
    "Active Power Limits: Min. Total Active Power Limit"
    qsummax: float
    "Reactive Power Limits: Max. Total Reactive Power Limit"
    qsummin: float
    "Reactive Power Limits: Min. Total Reactive Power Limit"
    root_id: object
    "Original Location"
    scalingFacSoftConstrCostP: float
    "Active power limits for Unit Commitment Penalty costs for soft constraints: Cost scaling factor"
    scalingFacSoftConstrCostQ: float
    "Reactive power limits for Unit Commitment Penalty costs for soft constraints: Cost scaling factor"
    scalingFacSoftConstrOpfP: float
    "Active Power Limits: Weighting factor for soft constraint penalty"
    scalingFacSoftConstrOpfQ: float
    "Reactive Power Limits: Weighting factor for soft constraint penalty"
    sernum: str
    "Serial Number"
    tid_: int
    "TimeID"

    def AddCubicle(*args): ...

    def AttributeType(*args): ...

    def CalcShiftedReversedBoundary(*args): ...

    def Clear(*args): ...

    def GetInterior(*args): ...

    def HasReferences(*args): ...

    def IsSplitting(*args): ...

    def Resize(*args): ...

    def Update(*args): ...

    def __getattr__(*args): ...


class ElmBranch(PFGeneral):
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Repair duration"
    ContRating: float
    "Continuous rating: Rating"
    FOD: float
    "Failures Branch Failures: Forced Outage Duration"
    FOE: float
    "Failures Branch Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures Branch Failures: Forced Outage Rate"
    GPScoords: list
    "Geographical Position"
    PostRating: float
    "Post-fault continuous rating: Rating"
    PreRating: float
    "Pre-fault continuous rating: Rating"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal i"
    bus2: object
    "Terminal j"
    cDisplayName: str
    "Display Name"
    cIsConform: int
    "Branch is conformant for short-circuit calculation."
    cIsInfoOk: int
    "Resulting Variables Ok"
    cLength4Shc: float
    "Length of branch (for short-circuit calculation)."
    cTerm0: str
    "Terminal 0"
    cTerm1: str
    "Terminal 1"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    circuit: object
    "Circuit"
    containsDCEquip: int
    "Contains DC equipment"
    contents: list
    "Contents"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cshcLne: object
    "Affected Line"
    cshcloc: float
    "Short-Circuit Location"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    fshcloc: float
    "Short-Circuit Location"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iDatCon0: int
    "Connection 1"
    iDatCon1: int
    "Connection 2"
    iSchemeStatus: int
    "Scheme Status"
    iperfect: int
    "Failures: Ideal component"
    ishcbrch: int
    "Available"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pDiagram: object
    "Diagram"
    pLimComp: object
    "Continuous rating: Limiting Component"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pPreLimComp: object
    "Pre-fault continuous rating: Limiting Component"
    pPreRating: object
    "Pre-fault continuous rating: Thermal Rating"
    pRating: object
    "Continuous rating: Thermal Rating"
    pStoch: object
    "Failures: Element model"
    p_conn0: object
    "Connection 1"
    p_conn1: object
    "Connection 2"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def Update(*args): ...

    def __getattr__(*args): ...


class ElmCabsys(PFGeneral):
    adc: list
    "Wave propagation, DC"
    adcFR: list
    "Wave propagation, DC"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    c_aAtDC: float
    "Wave propagation, DC"
    c_adc: list
    "Wave propagation, DC"
    c_dist: int
    "Line Model: Distributed Parameter"
    c_lumped: int
    "Line Model: Lumped Parameter (PI)"
    c_pTa: list
    "Travel time"
    c_pTad: float
    "Travel time"
    c_pa: int
    "A, Number of poles:"
    c_pz: int
    "Number of poles:"
    c_pzs: list
    "Surge impedance"
    c_rmsErrorA_ULM: float
    "RMS error for A"
    c_rmsErrorY_ULM: float
    "RMS error for Yc"
    c_rmsErrorZ_ULM: float
    "RMS error for Zc"
    cdisp_col: list
    "Display data for phase matrix index"
    cdisp_eig: list
    "Display data for eigenvalue"
    cdisp_row: list
    "Display data for phase matrix row"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    ci_model: int
    "Line Model"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dbg_fullBodeIntegral: int
    "Vector fitting: Full Bode integral"
    dbg_largePolesToConst: int
    "Vector fitting: Replace large poles by constants"
    dcCorr: int
    "Vector fitting: Apply DC correction"
    delayIdx: list
    "Delay index"
    desc: list
    "Description"
    disp_col: int
    "Display data for phase matrix index"
    disp_eig: int
    "Display data for eigenvalue"
    disp_mode: int
    "Display Propagation Function Data for Mode"
    disp_row: int
    "Display data for phase matrix row"
    dpolar: list
    "Polarity"
    dtmp: list
    "Passivity settings"
    fd_fit: int
    "Vector fitting: Fit"
    fd_model: int
    "Vector fitting: Line Model"
    fmax: float
    "Vector fitting: Max. frequency"
    fmin: float
    "Vector fitting: Min. frequency"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    ftau: float
    "Line Parameters Calculation: Frequency for parameter approx."
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    grpPoles: list
    "Poles per group"
    iSchemeStatus: int
    "Scheme Status"
    i_dist: int
    "Line Model"
    i_model: int
    "Line Model"
    internalDataLayout: int
    "Internal data layout"
    iopt_tem: int
    "Line Parameters Calculation: Temperature Dependency"
    iterVFA: int
    "Vector fitting: Max. number of iterations"
    iterVFZ: int
    "Vector fitting: Max. number of iterations"
    loc_name: str
    "Name"
    maxErrVFA: float
    "Vector fitting: RMS error"
    maxErrVFY: float
    "Vector fitting: RMS error"
    maxErrVFZ: float
    "Vector fitting: RMS error"
    maxResPoleRatioA: float
    "Max. residue-pole ratio"
    maxResPoleRatioZ: float
    "Max. residue-pole ratio"
    methodVFA: int
    "Vector fitting: Number of poles:Increase and flip unstable poles:Increase until rms met"
    methodVFZ: int
    "Vector fitting: Number of poles:Increase and flip unstable poles:Increase until rms met"
    oid_: int
    "ObjectID"
    outputPoles: int
    "Vector fitting: Output poles"
    outserv: int
    "Out of Service"
    pRoute: object
    "Route"
    pTa: list
    "Travel Time"
    pa: list
    "Wave Propagation"
    passivity: int
    "Passivity correction"
    pid_: int
    "ProjectID"
    plines: list
    "Circuit"
    polesA: list
    "Poles"
    polesA_Im: list
    "Poles of A (Im)"
    polesA_Re: list
    "Poles of A (Re)"
    polesVFA: int
    "Vector fitting: Max. number of poles"
    polesVFZ: int
    "Vector fitting: Max. number of poles"
    polesY_Im: list
    "Poles of Yc (Im)"
    polesY_Re: list
    "Poles of Yc (Re)"
    polesZ_Im: list
    "Poles of Zc (Im)"
    polesZ_Re: list
    "Poles of Zc (Re)"
    pys: list
    "Surge Admittance"
    pzs: list
    "Surge Impedance"
    resA_Im: list
    "Residues of Zc (Im)"
    resA_Re: list
    "Residues of Zc (Re)"
    resY_Im: list
    "Residues of Yc (Im)"
    resY_Re: list
    "Residues of Yc (Re)"
    resZ_Im: list
    "Residues of Zc (Im)"
    resZ_Re: list
    "Residues of Zc (Re)"
    root_id: object
    "Original Location"
    stMarginA: float
    "Vector fitting: Stability margin"
    stMarginZ: float
    "Vector fitting: Stability margin"
    strategy: int
    "Unstable poles:0"
    summandDelayIdx: list
    "Delay index for summand"
    tid_: int
    "TimeID"
    tmat: list
    "Transformation Matrix Tv"
    tuneDelays: int
    "Vector fitting: Fine-tune delays"
    typ_id: object
    "Cable Definition"
    useDCcorr: int
    "Apply DC correction"
    useZorY: int
    "Used fit"
    writeMats: int
    "Write out matrices"
    zerosA: list
    "Zeros"

    def AttributeType(*args): ...

    def FitParams(*args): ...

    def GetLineCable(*args): ...

    def HasReferences(*args): ...

    def Update(*args): ...

    def __getattr__(*args): ...


class ElmComp(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    contents: list
    "Contents"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pblk: list
    "Slots"
    pelm: list
    "Net Elements"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    typ_id: object
    "Frame"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def SlotUpdate(*args): ...

    def Slotupd(*args): ...

    def __getattr__(*args): ...


class ElmCoup(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Inom: float
    "Nominal Current"
    InomPre: float
    "Pre-fault nominal current"
    Tb: float
    "Break Time"
    Tclear: float
    "Fault Clearing Time"
    Tprot: float
    "Protection Tripping Time"
    Tswitch: float
    "Fault Separation/ Power Restoration: Time to actuate switch"
    aUsage: str
    "Switch Type"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal i"
    bus2: object
    "Terminal j"
    cDisplayName: str
    "Display Name"
    cTswitch: float
    "Fault Separation/ Power Restoration: Time to open remote controlled switch"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    ciScenarioType: int
    "Scenario Type"
    cimRdfId: list
    "RDF ID"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBay: object
    "Bay"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    ctrl_type: int
    "Fault Separation/ Power Restoration: Sectionalising:Remote Controlled (Stage 1):Indicator of Short Circuit (Stage 2):Manual (Stage 3)"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deltaFlow: float
    "Max. active power change"
    deltaFlowrel: float
    "Max. active power change"
    dep_protOver: float
    "Failure Data for Protection: Unnecessary backup protection maloperation"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iComDate: int
    "Commissioning Date"
    iExclRA: int
    "Excluded from Running Arrangement"
    iNeutInter: int
    "Switch interrupts neutral wire"
    iNoOpt: int
    "Exclude from optimisation"
    iNormOpenSwt: int
    "Normally open switch"
    iResDir: int
    "Fault Separation/ Power Restoration: Power Restoration"
    iRestore: int
    "Use as power restoration switch"
    iSchemeStatus: int
    "Scheme Status"
    iSep: int
    "Fault Separation/ Power Restoration: Switch can be opened during restoration"
    iZoneBus: int
    "Zone"
    idetail: int
    "Detailed for calculation"
    isclosed: int
    "Actual State:open:closed"
    limitRevFlow: int
    "Limit reversed flow"
    loc_name: str
    "Name"
    logEnvCurve: int
    "Log TRV envelope:No:For first opening event only:For all opening events"
    nneutral: int
    "No. of Neutrals:0:1"
    nphase: int
    "No. of Phases:1:2:3"
    oid_: int
    "ObjectID"
    on_off: int
    "Closed"
    outserv: int
    "Out of Service"
    pCBrating: object
    "Ratings"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pRating: object
    "Thermal Rating"
    pid_: int
    "ProjectID"
    prot_fail: float
    "Failure Data for Protection: Circuit breaker fails to open"
    reclAttempts: int
    "Fault clearance: Maximum number of reclosing attempts"
    rel_hasProt: int
    "Fault clearance: Consider as switch with protection device"
    rel_hasRecl: int
    "Fault clearance: Consider as switch with automatic reclosing device"
    revFlowChk: int
    "Relevant for the reversed power flow analysis"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    shownValues: int
    "Value representation"
    spon_prot_f: float
    "Failure Data for Protection: Frequency of spurious protection operation"
    spon_prot_t: float
    "Independent unnecessary open: Time to close"
    t_del_a: float
    "Scatter: Phase a"
    t_del_b: float
    "Scatter: Phase b"
    t_del_c: float
    "Scatter: Phase c"
    t_del_n: float
    "Scatter: Neutral"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"

    def AttributeType(*args): ...

    def Close(*args): ...

    def GetRemoteBreakers(*args): ...

    def HasReferences(*args): ...

    def IsBreaker(*args): ...

    def IsClosed(*args): ...

    def IsOpen(*args): ...

    def Open(*args): ...

    def __getattr__(*args): ...


class ElmDsl(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    configScript: object
    "Configuration Script"
    contents: list
    "Events"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    matrix: list
    "Characteristics"
    matrix2: list
    "Two Dimensional Characteristics"
    oarrmat: list
    "Array/Matrix"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    parameterNames: list
    "Parameter Names"
    params: list
    "Parameter"
    parnam: list
    "Parameter Names"
    pelm: list
    "Net Element"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    signal: list
    "Signal Name"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"

    def AttributeType(*args): ...

    def ExportToClipboard(*args): ...

    def ExportToFile(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmFeeder(PFGeneral):
    Iset: float
    "Load Scaling: Current"
    Isetr: float
    "Load Scaling: Current, ph. 1"
    Isets: float
    "Load Scaling: Current, ph. 2"
    Isett: float
    "Load Scaling: Current, ph. 3"
    Pset: float
    "Load Scaling: Active Power"
    Psetr: float
    "Load Scaling: Active Power, ph. 1"
    Psets: float
    "Load Scaling: Active Power, ph. 2"
    Psett: float
    "Load Scaling: Active Power, ph. 3"
    Qset: float
    "Load Scaling: Reactive Power"
    Qsetr: float
    "Load Scaling: Reactive Power, ph. 1"
    Qsets: float
    "Load Scaling: Reactive Power, ph. 2"
    Qsett: float
    "Load Scaling: Reactive Power, ph. 3"
    Sset: float
    "Load Scaling: Apparent Power"
    Ssetr: float
    "Load Scaling: Apparent Power, ph. 1"
    Ssets: float
    "Load Scaling: Apparent Power, ph. 2"
    Ssett: float
    "Load Scaling: Apparent Power, ph. 3"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cPhaseWise: int
    "Load Scaling: Phasewise input"
    cUserDefIndex: int
    "User defined Index"
    cbranch: object
    "Location: Branch"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciConn: int
    "Connected"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    ciRadial: int
    "Radial"
    cimRdfId: list
    "RDF ID"
    ciorient: int
    "Location: Orientation:--> Branch:--> Busbar"
    cn_bus: object
    "Location: Busbar"
    cosphiset: float
    "Load Scaling: Power Factor, cos(phi)"
    cosphisetr: float
    "Load Scaling: Power Factor, cos(phi), ph. 1"
    cosphisets: float
    "Load Scaling: Power Factor, cos(phi), ph. 2"
    cosphisett: float
    "Load Scaling: Power Factor, cos(phi), ph. 3"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpParFeed: object
    "Parallel Feeder"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpTrfFeed: object
    "Feeding Transformer"
    cpZone: object
    "Zone"
    ctrlType: int
    "Control type"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    dpl1: float
    "dpl1"
    dpl10: float
    "dpl10"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    dpl6: float
    "dpl6"
    dpl7: float
    "dpl7"
    dpl8: float
    "dpl8"
    dpl9: float
    "dpl9"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    i_scale: int
    "Load Scaling: First setpoint"
    i_scalepf: int
    "Load Scaling: Second setpoint"
    icolor: int
    "Colour"
    ilVolt: int
    "Terminate feeder when encountering lower voltage levels"
    iorient: int
    "Orientation:--> Branch:--> Busbar"
    ipfdir: int
    "Consider active power flow direction"
    irVolt: int
    "Terminate feeder when encountering higher voltage levels"
    loc_name: str
    "Name"
    maxVdrop: float
    "Limits for Voltage Change relative to Feeding Point: Maximum allowed Voltage Drop"
    maxVrise: float
    "Limits for Voltage Change relative to Feeding Point: Maximum allowed Voltage Rise"
    n_2wt: int
    "No. of 2-w Trfs."
    n_3wt: int
    "No. of 3-w Trfs."
    n_4wt: int
    "No. of 4-w Trfs."
    n_asm: int
    "No. of asyn. Machines"
    n_bar: int
    "No. of Busbars"
    n_cust: int
    "Total number of customers"
    n_lne: int
    "No. of Lines"
    n_lod: int
    "No. of Loads"
    n_pvs: int
    "No. of PV Systems"
    n_stg: int
    "No. of Static Generators"
    n_sym: int
    "No. of syn. Machines"
    n_term: int
    "No. of Terminals"
    obj_bus: int
    "Direction"
    obj_id: object
    "Cubicle"
    oid_: int
    "ObjectID"
    operRadial: int
    "Feeder is supposed to be operated radially."
    outserv: int
    "Out of Service"
    pf_recapset: int
    "Load Scaling: Power Factor:ind.:cap."
    pf_recapsetr: int
    "Load Scaling: Power Factor, ph. 1:ind.:cap."
    pf_recapsets: int
    "Load Scaling: Power Factor, ph. 2:ind.:cap."
    pf_recapsett: int
    "Load Scaling: Power Factor, ph. 3:ind.:cap."
    pid_: int
    "ProjectID"
    preDefIniSc: int
    "User defined initial scale"
    root_id: object
    "Original Location"
    scale0: float
    "Load Scaling: Scaling Factor"
    scale10r: float
    "Load Scaling: Scaling Factor, ph. 1"
    scale10s: float
    "Load Scaling: Scaling Factor, ph. 2"
    scale10t: float
    "Load Scaling: Scaling Factor, ph. 3"
    scale1rini: float
    "Initial value for control 1, ph. 1"
    scale1sini: float
    "Initial value for control 1, ph. 2"
    scale1tini: float
    "Initial value for control 1, ph. 3"
    scale2rini: float
    "Initial value for control 2, ph. 1"
    scale2sini: float
    "Initial value for control 2, ph. 2"
    scale2tini: float
    "Initial value for control 2, ph. 3"
    scalePhaseWise: int
    "Load Scaling: Phasewise scaling"
    scaleini: float
    "Initial value for control 1"
    scalephiini: float
    "Initial value for control 2"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CalcAggrVarsInRadFeed(*args): ...

    def GetAll(*args): ...

    def GetBranches(*args): ...

    def GetBuses(*args): ...

    def GetNodesBranches(*args): ...

    def GetObjs(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmFile(PFGeneral):
    Variable: list
    "Variable"
    afac: list
    "Factor a"
    approx: int
    "Approximation:constant:linear"
    bfac: list
    "Factor b"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    f_name: str
    "Filename"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    icol: list
    "Column j"
    iopt_imp: int
    "Import from"
    iopt_tini: int
    "Load Flow Time"
    loc_name: str
    "Name"
    object: list
    "Element"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pid_: int
    "ProjectID"
    prim: str
    "P or S"
    results: object
    "Results"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    tini: float
    "Load Flow Time: Load Flow Time"
    variable: list
    "Variable"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def LoadFile(*args): ...

    def SaveFile(*args): ...

    def __getattr__(*args): ...


class ElmFilter(PFGeneral):
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures Double Earth Fault: Repair duration"
    FOD: float
    "Failures: Forced Outage Duration"
    FOE: float
    "Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures: Forced Outage Rate"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Irze: list
    "Rated current of grounding"
    QF: float
    "Design parameter: Quality factor QF"
    QF1: float
    "Design parameter: Quality factor 1"
    QF2: float
    "Design parameter: Quality factor 2"
    Re: float
    "Internal grounding impedance: Resistance, Re"
    Xe: float
    "Internal grounding impedance: Reactance, Xe"
    acost: float
    "Annual cost"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal"
    bus1n: object
    "Neutral conductor: Neutral"
    c1: float
    "Layout parameter: Capacitance C1"
    c2: float
    "Layout parameter: Capacitance C2"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    capsa: str
    "Vector group:Y:D:YN"
    ccap: float
    "Layout parameter: Capacitance C"
    cgnd: int
    "Internal grounding impedance: Star point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    ctech: int
    "Technology"
    cutot: float
    "Design parameter: Rated current"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fcharC: object
    "Frequency dependence of capacitors: C(f)"
    fcharC1: object
    "Frequency dependence of capacitors: C1(f)"
    fcharC2: object
    "Frequency dependence of capacitors: C2(f)"
    fcharL: object
    "Frequency dependence of R-L elements: L(f)"
    fcharL1: object
    "Frequency dependence of R-L elements: L1(f)"
    fcharL2: object
    "Frequency dependence of R-L elements: L2(f)"
    fcharR: object
    "Frequency dependence of R-L elements: Rs(f)"
    fcharR1: object
    "Frequency dependence of R-L elements: Rs1(f)"
    fcharR2: object
    "Frequency dependence of R-L elements: Rs2(f)"
    fcharRp: object
    "Frequency dependence of parallel resistances: Rp(f)"
    fcharRp1: object
    "Frequency dependence of parallel resistances: Rp1(f)"
    fcharRp2: object
    "Frequency dependence of parallel resistances: Rp2(f)"
    flttype: int
    "Filter type:Single-tuned:HP Second order:HP Third order:HP C-type:Double-tuned type 1:Double-tuned type 2:Double-tuned type 3:Double-tuned type 4"
    fnom: float
    "Nominal frequency"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    fres: float
    "Design parameter: Resonant frequency"
    fres1: float
    "Design parameter: Resonant frequency 1"
    fres2: float
    "Design parameter: Resonant frequency 2"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    harmPgeC: float
    "Frequency dependence of capacitors: Capacitance C"
    harmPgeC1: float
    "Frequency dependence of capacitors: Capacitance C1"
    harmPgeC2: float
    "Frequency dependence of capacitors: Capacitance C2"
    harmPgeL: float
    "Frequency dependence of R-L elements: Inductance L"
    harmPgeL1: float
    "Frequency dependence of R-L elements: Inductance L1"
    harmPgeL2: float
    "Frequency dependence of R-L elements: Inductance L2"
    harmPgeR: float
    "Frequency dependence of R-L elements: Resistance Rs"
    harmPgeR1: float
    "Frequency dependence of R-L elements: Resistance Rs1"
    harmPgeR2: float
    "Frequency dependence of R-L elements: Resistance Rs2"
    harmPgeRp: float
    "Frequency dependence of parallel resistances: Parallel resistance Rp"
    harmPgeRp1: float
    "Frequency dependence of parallel resistances: Parallel resistance Rp1"
    harmPgeRp2: float
    "Frequency dependence of parallel resistances: Parallel resistance Rp2"
    iComDate: int
    "Commissioning Date"
    iSchemeStatus: int
    "Scheme Status"
    ignd: int
    "Star point:grounded:compensated:isolated"
    iintgnd: int
    "Neutral conductor: N-connection:None:At terminal (ABC-N):Separate terminal"
    iperfect: int
    "Failures: Ideal component"
    l1: float
    "Layout parameter: Inductance L1"
    l2: float
    "Layout parameter: Inductance L2"
    loc_name: str
    "Name"
    lrea: float
    "Layout parameter: Inductance L"
    manuf: str
    "Failures: Manufacturer"
    mode_inp: int
    "Input mode:Default:Design parameter:Layout parameter"
    nflph: int
    "Phases:1:2:3"
    nres: float
    "Design parameter: Tuning order"
    nres1: float
    "Design parameter: Tuning order 1"
    nres2: float
    "Design parameter: Tuning order 2"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pStoch: object
    "Failures: Element model"
    phtech: int
    "Technology"
    pid_: int
    "ProjectID"
    qtotn: float
    "Design parameter: Rated reactive power"
    root_id: object
    "Original Location"
    rp1: float
    "Layout parameter: Parallel resistance Rp1"
    rp2: float
    "Layout parameter: Parallel resistance Rp2"
    rpara: float
    "Layout parameter: Parallel resistance Rp"
    rs1: float
    "Layout parameter: Resistance Rs1"
    rs2: float
    "Layout parameter: Resistance Rs2"
    rsrea: float
    "Layout parameter: Resistance Rs"
    sOpComment: list
    "Operator comment"
    sernum: str
    "Failures: Serial Number"
    systp: int
    "System Type:&0&AC:&2&AC/BI"
    tid_: int
    "TimeID"
    ufltnom: float
    "Rated voltage"

    def AttributeType(*args): ...

    def GetGroundingImpedance(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmGenstat(PFGeneral):
    EDS: float
    "Stochastic Model for Generation: Expectancy of derated states"
    FAY: float
    "Stochastic Model for Generation: Full Availability Expectancy"
    FOE: float
    "Stochastic Model for Generation: Forced Outage Expectancy"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Ik: float
    "Fault Contribution: Steady-State Shc. Current"
    IkPFmax: float
    "Steady-state short-circuit current contribution: Maximum current"
    IkPFmin: float
    "Steady-state short-circuit current contribution: Minimum current"
    IkWDmax: float
    "Steady-state short-circuit current contribution: Maximum current"
    IkWDmin: float
    "Steady-state short-circuit current contribution: Minimum current"
    Iks: float
    "Fault Contribution: Transient Short-Circuit Current"
    Ikss: float
    "Max. Fault Contribution: Subtransient Short-Circuit Current"
    Ikss1PF: float
    "Initial symmetrical short-circuit current contribution: Single-phase faults, Ik1PF"
    Ikss2PF: float
    "Initial symmetrical short-circuit current contribution: Two-phase faults, Ik2PF"
    Ikss3PF: float
    "Initial symmetrical short-circuit current contribution: Three-phase faults, Ik3PF"
    Inom: float
    "Nominal Current"
    Irated: float
    "Harmonic Source: Rated Current"
    Irze: list
    "Rated Current of Grounding"
    Kd: float
    "Current controller: Kd: d-Axis, proportional gain"
    Kfactor: float
    "Fault Contribution: K Factor"
    Ki_plli: float
    "Current PLL: Integration Gain"
    Ki_pllu: float
    "Voltage PLL: Integration Gain"
    Kp_plli: float
    "Current PLL: Proportional Gain"
    Kp_pllu: float
    "Voltage PLL: Proportional Gain"
    Kpf: float
    "Dispatch: Prim. Frequency Bias"
    Kq: float
    "Current controller: Kq: q-Axis, proportional gain"
    P_max: float
    "Active Power: Rating: Max."
    Pcu: float
    "Series reactor: Copper losses"
    PmaxInv: float
    "Separate consumption mode: Max."
    PmaxInvPU: float
    "Separate consumption mode: Max."
    Pmax_a: float
    "Pmax(act.)"
    Pmax_uc: float
    "Active Power Operational Limits: Max."
    Pmax_ucPU: float
    "Active Power Operational Limits: Max."
    PminInv: float
    "Separate consumption mode: Min."
    PminInvPU: float
    "Separate consumption mode: Min."
    Pmin_a: float
    "Pmin(act.)"
    Pmin_uc: float
    "Active Power Operational Limits: Min."
    Pmin_ucPU: float
    "Active Power Operational Limits: Min."
    Pngrel: float
    "Stochastic Model for Generation: Based on rated active power (Pr)"
    Pnom: float
    "Active Power Operational Limits: Pr(rated)"
    Qfu_max: float
    "Q(V)-Characteristic: Q max"
    Qfu_min: float
    "Q(V)-Characteristic: Q min"
    Qmax_a: float
    "Qmax(act.)"
    Qmin_a: float
    "Qmin(act.)"
    QtargetBase: int
    "Optimisation of reactive power reserve: Base:Reactive power limits:Rated apparent power"
    QtargetRPR: float
    "Optimisation of reactive power reserve: Q target value"
    R0hmc: float
    "Norton Equivalent: Resistance, R0h"
    R0toR1: float
    "Series reactor: R0/R1 ratio"
    R1hmc: float
    "Norton Equivalent: Resistance, R1h"
    R2hmc: float
    "Norton Equivalent: Resistance, R2h"
    Sk: float
    "Fault Contribution: Steady-State Short-Circuit Level"
    Sks: float
    "Fault Contribution: Transient Short-Circuit Level"
    Skss: float
    "Max. Fault Contribution: Subtransient Short-Circuit Level"
    T1_plli: float
    "Current PLL: Low-Pass Filter Time Constant"
    T1_pllu: float
    "Voltage PLL: Low-Pass Filter Time Constant"
    Td: float
    "Current controller: Td: d-Axis, integration time constant"
    Tdelay: float
    "Current source model: Delay time constant"
    Tondelay: float
    "Min. operation voltage: Switch-on delay"
    Tq: float
    "Current controller: Tq: q-Axis, integration time constant"
    X0hmc: float
    "Norton Equivalent: Reactance, X0h"
    X0toX1: float
    "Series reactor: X0/X1 ratio"
    X1hmc: float
    "Norton Equivalent: Reactance, X1h"
    X2hmc: float
    "Norton Equivalent: Reactance, X2h"
    aCategory: str
    "Plant Category"
    aSubCategory: str
    "Subcategory"
    allowConsumMode: int
    "Separate consumption mode"
    allowGenMode: int
    "Separate generation mode"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    av_mode: str
    "Local Controller"
    availFactor: float
    "Availability Factor"
    avgCosts: float
    "Average costs"
    avgCostsUc: float
    "Piecewise linearisation for LP: Average costs"
    beta: float
    "Wind Model Weibull Distribution for Wind Speed: Beta"
    bus1: object
    "Terminal"
    bus1n: object
    "Neutral Conductor: Neutral"
    bustp: str
    "Corresponding Bus Type:"
    cCategory: str
    "Plant Category"
    cDisplayName: str
    "Display Name"
    cIsDiscreteCtrlP: int
    "Restriction to discrete active power values"
    cIsMustRunUC: int
    "Additional constraints for controls: Must run"
    cIsPcurrAllowed: int
    "Allow current active power value"
    cQ_max: float
    "Reactive Power Operational Limits: Maximum"
    cQ_min: float
    "Reactive Power Operational Limits: Minimum"
    cStorage: object
    "Generator usage: Storage model"
    cSubCategory: str
    "Subcategory"
    cTypHmc: str
    "Harmonic Source: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    cVecDiscreteCtrlPvals: list
    "Valid active power values"
    c_pCtrlHV: object
    "Controlled HV-busbar"
    c_pmod: object
    "Model"
    c_psecc: object
    "External Secondary Controller"
    c_pstac: object
    "External Station Controller"
    ccost: list
    "Costs"
    cfixedCosts: float
    "Consumption mode: Fixed costs"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    ciScenarioType: int
    "Scenario Type"
    cimRdfId: list
    "RDF ID"
    cnwsamples: int
    "Wind Model Time Series Characteristics: Annual Samples: Number of Samples"
    coldStartTime: float
    "Start-up costs: Cold-start time"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    consumCosts: float
    "Consumption mode: Consumption costs"
    cosgini: float
    "Dispatch: Power Factor"
    cosgini_a: float
    "Actual Dispatch: Power Factor (act.)"
    cosn: float
    "Ratings: Rated Power Factor"
    costColdStart: float
    "Start-up costs: Cold-start costs"
    costCurtailment: float
    "Costs for curtailment"
    costRedispatchDown: float
    "Additional redispatch costs: Downward active power redispatch costs"
    costRedispatchP: float
    "Redispatch costs for active power change"
    costRedispatchQ: float
    "Redispatch costs for reactive power change"
    costRedispatchUp: float
    "Additional redispatch costs: Upward active power redispatch costs"
    costShutDown: float
    "Shut-down costs"
    cost_up: float
    "Start-up costs: Warm-start costs"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpower: list
    "Power"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    ddroop: float
    "Voltage Droop: Droop"
    ddroopoe: float
    "Q(V)-Characteristic: Droop (overexcited)"
    ddroopue: float
    "Q(V)-Characteristic: Droop (underexcited)"
    desc: list
    "Description"
    discMethCostOp: int
    "Piecewise linearisation for LP"
    dispatch: int
    "Generator Dispatch"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    dsecres: float
    "Reserve"
    efficiencyCurveConsum: object
    "Efficiency: Efficiency curve (consumption)"
    efficiencyCurveGen: object
    "Efficiency: Efficiency curve (generation)"
    efficiencyLPconsum: float
    "Efficiency: Used efficiency (consumption)"
    efficiencyLPgen: float
    "Efficiency: Used efficiency (generation)"
    fcharr0: object
    "Norton Equivalent: Frequency-dependence, r0h(f)"
    fcharr1: object
    "Norton Equivalent: Frequency-Dependence, r1h(f)"
    fcharr2: object
    "Norton Equivalent: Frequency-Dependence, r2h(f)"
    fcharx0: object
    "Norton Equivalent: Frequency-dependence, x0h(f)"
    fcharx1: object
    "Norton Equivalent: Frequency-Dependence, x1h(f)"
    fcharx2: object
    "Norton Equivalent: Frequency-Dependence, x2h(f)"
    fixed: int
    "Must run"
    fixedCosts: float
    "Fixed costs"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    genShiftKey: float
    "Generation shift key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iDelay: int
    "Current source model: dq-reference angle delay (if dq-reference signals not connected)"
    iInterPol: int
    "Approximation:Spline:Piecewise linear:Polynomial:Hermite"
    iNoShcContr: int
    "No Short-Circuit Contribution"
    iOPFCPmax: int
    "Active Power Operational Limits: Max."
    iOPFCPmin: int
    "Active Power Operational Limits: Min."
    iOPFCQmax: int
    "Reactive Power Operational Limits: Max."
    iOPFCQmin: int
    "Reactive Power Operational Limits: Min."
    iSchemeStatus: int
    "Scheme Status"
    iShcModel: int
    "Short-Circuit Model:Equivalent synchronous machine:Dynamic voltage support:Doubly fed asynchronous generator:Full size converter"
    iSimModel: int
    "Model:According to connected input signals:Current source:Voltage source:Constant impedance:Constant power"
    iUseNegSeqAngle: int
    "Negative sequence: Current source model: Use negative sequence angle for negative sequence current source"
    iUseZsr: int
    "Negative sequence: Use series reactor impedance, if negative sequence voltage signals are connected"
    iWDmax: float
    "Initial symmetrical short-circuit current contribution: Max. instantaneous short-circuit current, iWDmax"
    iconfed: int
    "Static Converter-Fed Drive"
    ictpg: int
    "Controls: Active Power"
    ictqg: int
    "Controls: Reactive Power"
    icurref: int
    "Harmonic Source: Harmonic currents referred to"
    iearthed: int
    "Earthed"
    iestp: int
    "State Estimation: Estimate Active Power"
    iestq: int
    "State Estimation: Estimate Reactive Power"
    imax: float
    "Fault Contribution: Max. Current"
    installCost: float
    "General costs: Installation costs"
    iopt_tdr: int
    "Q(V)-Characteristic: Different droop values"
    iopt_windm: int
    "Wind Model: Wind Model"
    ip_ctrl: int
    "Reference Machine"
    is4SpinReserve: int
    "Consider for region spinning reserve"
    isConsCostOp: int
    "Operating costs"
    isConsCostsRedispatch: int
    "Additional redispatch costs"
    isConsShutDownCost: int
    "Shut-down costs"
    isConsStartUpCost: int
    "Start-up costs"
    isConstrRamp: int
    "Ramp rate constraints"
    isConstrUpDown: int
    "Start-up/shut-down time constraints"
    isCtrlFixedToLdfVal: int
    "Additional constraints for controls: Fix controls to Load Flow values"
    isCtrlP: int
    "Controls: Active power"
    isCtrlPplacement: int
    "Optimise active power"
    isCtrlQ: int
    "Controls: Reactive power"
    isDiscreteCtrlP: int
    "Restriction to discrete active power values"
    isLimPmax: int
    "Active Power Operational Limits: Max."
    isLimPmin: int
    "Active Power Operational Limits: Min."
    isLimQmax: int
    "Reactive Power Operational Limits: Max."
    isLimQmin: int
    "Reactive Power Operational Limits: Min."
    isMustRunUC: int
    "Additional constraints for controls: Must run"
    isPcurrAllowed: int
    "Restriction to discrete active power values: Allow current active power value"
    isRPR: int
    "Optimisation of reactive power reserve"
    isVRE: int
    "Generator usage: Generator usage:Single thermal generation unit:Variable renewable energy source (VRE):Coupled with storage model:Part of Virtual Power Plant"
    iv_mode: int
    "Local Controller"
    kWD: float
    "Initial symmetrical short-circuit current contribution: Factor kappaWD"
    lifeSpan: float
    "Expected life span"
    limRampDown: float
    "Ramp rate constraints: Ramp-down limit"
    limRampDownPU: float
    "Ramp rate constraints: Ramp-down limit"
    limRampShutDown: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampShutDownPU: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampStartUp: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampStartUpPU: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampUp: float
    "Ramp rate constraints: Ramp-up limit"
    limRampUpPU: float
    "Ramp rate constraints: Ramp-up limit"
    loc_name: str
    "Name"
    maintenCost: float
    "General costs: Maintenance costs"
    mean: float
    "Wind Model Weibull Distribution for Wind Speed: Mean"
    minDownTime: float
    "Start-up/shut-down time constraints: Minimum down-time"
    minUpTime: float
    "Start-up/shut-down time constraints: Minimum up-time"
    mode_inp: str
    "Dispatch: Input Mode"
    mode_pgi: int
    "Model:Active power input:Wind speed input"
    ngnum: int
    "Number of: parallel units"
    nneutral: int
    "Neutral Conductor: N-Connection:None:At terminal (ABC-N):Separate terminal"
    nphase: int
    "No. of Phases"
    numBreakpointsCostOp: int
    "Piecewise linearisation for LP: Number of breakpoints"
    oid_: int
    "ObjectID"
    originalValue: float
    "Original value"
    outServPzero: int
    "Out of service when active power is zero"
    outserv: int
    "Out of Service"
    pBMU: object
    "Virtual Power Plant"
    pCharYrMW: list
    "Wind Model Time Series Characteristics: Annual Samples: Time Series Characteristics of Active Power Contribution (MW)"
    pCharYrWS: list
    "Wind Model Time Series Characteristics: Annual Samples: Time Series Characteristics for Wind Speed (m/s)"
    pFlicker: object
    "Flicker Coefficients"
    pGRStoch: object
    "Stochastic Model for Generation: Stochastic Model"
    pMeteostat: object
    "Wind Model: Meteo Station (Correlation)"
    pOpCostCurve: object
    "Operating costs: Generator cost curve"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pPowerCrv: object
    "Wind Power Curve"
    pQPcurve: object
    "Q(P)-Characteristic: Q(P)-Curve"
    pQlimType: object
    "Reactive Power Operational Limits: Capability Curve"
    pStorage: object
    "Storage model"
    pSubModel: object
    "Submodel"
    p_direc: int
    "Dispatch: Power Direction:P>=0:P<0"
    p_over: float
    "cosphi(P)-Characteristic Overexcited: Active Power"
    p_under: float
    "cosphi(P)-Characteristic Underexcited: Active Power"
    pblocktrf: object
    "Externally modelled unit transformer: Unit transformer"
    penaltyCosts: float
    "Penalty costs"
    pf_over: float
    "cosphi(P)-Characteristic Overexcited: Min. Power Factor"
    pf_recap: int
    "Dispatch: Power Factor:ind.:cap."
    pf_recap_a: str
    "Actual Dispatch: Power Factor Ind/Cap (act.)"
    pf_under: float
    "cosphi(P)-Characteristic Underexcited: Min. Power Factor"
    pgini: float
    "Dispatch: Active Power"
    pgini_a: float
    "Actual Dispatch: Active Power (act.)"
    phiini: float
    "Dispatch: Angle"
    phmc: object
    "Harmonic Source: Harmonic Currents"
    phtech: int
    "Technology:3PH:3PH-E:1PH PH-E:1PH PH-N:1PH PH-PH"
    pid_: int
    "ProjectID"
    pinput: int
    "Interpretation of input signals: Active Power signal:in MW:in p.u. based on Snom:in p.u. based on Pnom"
    pmaxratf: float
    "Active Power: Rating: Rating Factor"
    polyDegree: int
    "Polynomial degree"
    priority: int
    "Merit Order"
    psutype: str
    "Power station unit type"
    q_max: float
    "Reactive Power Operational Limits: Max."
    q_min: float
    "Reactive Power Operational Limits: Min."
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qgini: float
    "Dispatch: Reactive Power"
    qgini_a: float
    "Actual Dispatch: Reactive Power (act.)"
    qinput: int
    "Interpretation of input signals: Reactive Power signal:in Mvar:in p.u. based on Snom:in p.u. based on Pnom:as cos(phi)"
    r0: float
    "Zero sequence: Resistance, r0"
    r0hmc: float
    "Norton Equivalent: Resistance, r0h"
    r0iec: float
    "Zero sequence short-circuit impedance: Resistance, r0"
    r1hmc: float
    "Norton Equivalent: Resistance, r1h"
    r2: float
    "Negative sequence: Resistance r2"
    r2hmc: float
    "Norton Equivalent: Resistance, r2h"
    r2iec: float
    "Negative sequence short-circuit impedance: Resistance, r2"
    r2shc: float
    "Negative sequence short-circuit impedance: Resistance, r2"
    root_id: object
    "Original Location"
    rtox: float
    "Max. Fault Contribution: R to X'' ratio"
    rxWD: float
    "Initial symmetrical short-circuit current contribution: Ratio RWD/XWD"
    sOpComment: list
    "Operator Comment"
    scale0: float
    "Dispatch: Scaling Factor"
    scale0_a: float
    "Actual Dispatch: Scaling Factor (act.)"
    scaleQmax: float
    "Reactive Power Operational Limits: Scaling Factor (max.)"
    scaleQmin: float
    "Reactive Power Operational Limits: Scaling Factor (min.)"
    scrapValue: float
    "Scrap value"
    searchBlockTrf: int
    "Externally modelled unit transformer"
    sernum: str
    "Serial Number"
    sgini: float
    "Dispatch: Apparent Power"
    sgini_a: float
    "Actual Dispatch: Apparent Power (act.)"
    sgn: float
    "Ratings: Rated Apparent Power"
    shcDeadband: int
    "Voltage deadband"
    smoothfac: float
    "Smoothing factor"
    stowind: int
    "Wind Model"
    tds: float
    "Time Constants: Td'"
    tdss: float
    "Time Constants: Td''"
    tid_: int
    "TimeID"
    uDeadband: float
    "Voltage deadband: Deadband"
    udeadblow: float
    "Q(V)-Characteristic Voltage Dead Band: Lower Voltage Limit"
    udeadbup: float
    "Q(V)-Characteristic Voltage Dead Band: Upper Voltage Limit"
    uk: float
    "Series reactor: Short circuit impedance"
    umin: float
    "Min. operation voltage: Switch-off threshold"
    uonthr: float
    "Min. operation voltage: Switch-on threshold"
    usetp: float
    "Dispatch: Voltage"
    usp_max: float
    "Voltage Setpoint Limits: Max. Voltage Setpoint"
    usp_min: float
    "Voltage Setpoint Limits: Min. Voltage Setpoint"
    variance: float
    "Wind Model Weibull Distribution for Wind Speed: Variance"
    vecBreakpointsP: list
    "Piecewise linearisation for LP: Power"
    vecCostRedispatchDown: list
    "Costs"
    vecCostRedispatchUp: list
    "Costs"
    vecDiscreteCtrlPvals: list
    "Restriction to discrete active power values: Valid active power values"
    vecPowerRedispatchDown: list
    "Redispatch"
    vecPowerRedispatchUp: list
    "Redispatch"
    vecStartUpCosts: list
    "Start-up costs: Start-up costs"
    vecStartUpTimes: list
    "Start-up costs: Down-time"
    windspeed: float
    "Dispatch: Wind speed"
    windspeed_a: float
    "Actual Dispatch: Wind speed (act.)"
    x0: float
    "Zero sequence: Reactance, x0"
    x0hmc: float
    "Norton Equivalent: Reactance, x0h"
    x0iec: float
    "Zero sequence short-circuit impedance: Reactance, x0"
    x1hmc: float
    "Norton Equivalent: Reactance, x1h"
    x2: float
    "Negative sequence: Reactance x2"
    x2hmc: float
    "Norton Equivalent: Reactance, x2h"
    x2iec: float
    "Negative sequence short-circuit impedance: Reactance, x2"
    x2shc: float
    "Negative sequence short-circuit impedance: Reactance, x2"
    xtor: float
    "Max. Fault Contribution: X'' to R ratio"

    def AttributeType(*args): ...

    def CalcEfficiency(*args): ...

    def Derate(*args): ...

    def Disconnect(*args): ...

    def GetAvailableGenPower(*args): ...

    def GetGroundingImpedance(*args): ...

    def GetStepupTransformer(*args): ...

    def HasReferences(*args): ...

    def IsConnected(*args): ...

    def Reconnect(*args): ...

    def ResetDerating(*args): ...

    def __getattr__(*args): ...


class ElmGndswt(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Irze: list
    "Rated Current of Grounding"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iComDate: int
    "Commissioning Date"
    iSchemeStatus: int
    "Scheme Status"
    idetail: int
    "Detailed for calculation"
    loc_name: str
    "Name"
    nneutral: int
    "No. of Neutrals:0:1"
    nphase: int
    "No. of Phases:1:2:3"
    oid_: int
    "ObjectID"
    on_off: int
    "Closed"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"

    def AttributeType(*args): ...

    def Close(*args): ...

    def GetGroundingImpedance(*args): ...

    def HasReferences(*args): ...

    def IsClosed(*args): ...

    def IsOpen(*args): ...

    def Open(*args): ...

    def __getattr__(*args): ...


class ElmLne(PFGeneral):
    B0: float
    "Susceptance B0"
    B1: float
    "Susceptance B1"
    C0: float
    "Capacitance C0"
    C1: float
    "Capacitance C1"
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures Double Earth Fault: Repair duration"
    FOD: float
    "Failures Sustained Line Failures: Forced Outage Duration"
    FOE: float
    "Failures Sustained Line Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures Sustained Line Failures: Forced Outage Rate"
    G0: float
    "Conductance G0"
    G1: float
    "Conductance G1"
    GPScoords: list
    "Geographical Position"
    Ice: float
    "Resulting Values: Earth-Fault Current, Ice"
    Imaxlim: float
    "Max. permissible current"
    Inom: float
    "Resulting Values: Nominal Current"
    InomPre: float
    "Pre-fault nominal current"
    Inom_a: float
    "Resulting Values: Nominal Current (act.)"
    Irated: float
    "Type Parameters: Rated Current"
    Ldc: float
    "Resulting Values: Inductance, Ldc"
    NrCust: int
    "Number of connected customers"
    R0: float
    "Resulting Values: Zero Seq. Resistance, R0"
    R1: float
    "Resulting Values: Pos. Seq. Resistance, R1"
    R1_tmax: float
    "Pos. Seq. Resistance at Max. Operating Temperature, R1 at tmax"
    ReRl: float
    "Earth Factor, Re/Rl"
    Ta0: float
    "Travel Time, Mode 0"
    Ta1: float
    "Travel Time, Mode 1"
    Ta2: float
    "Travel Time, Mode 2"
    Top: float
    "Operating Temperature"
    Unom: float
    "Rated Voltage"
    X0: float
    "Resulting Values: Zero Seq. Reactance, X0"
    X1: float
    "Resulting Values: Pos. Seq. Reactance, X1"
    XeXl: float
    "Earth Factor, Xe/Xl"
    Z1: float
    "Resulting Values: Pos. Seq. Impedance, Z1"
    a0dc: float
    "Results of Line Parameters Calculation: Wave Propagation, DC, Mode 0"
    a1dc: float
    "Results of Line Parameters Calculation: Wave Propagation, DC, Mode 1"
    a2dc: float
    "Results of Line Parameters Calculation: Wave Propagation, DC, Mode 2"
    adc: list
    "Wave propagation, DC"
    adcFR: list
    "Wave propagation, DC"
    allowCntConstrFilt: int
    "Constraint Filtering: Allow contingency filtering by number of critical constraints"
    allowMarginFilt: int
    "Constraint Filtering: Allow filtering by constraint margin"
    alpha: float
    "Medium diffusivity"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    armTyp: int
    "Type Parameters: Armour Type:AWA:SWA"
    asys: int
    "Installation Conditions: Clearance :Touching:1x Cable Diameter:d <= 0.125 m:0.125 m < d <= 0.25 m:0.25 m < d <= 0.5 m:0.5 m < d <= 1.0 m"
    b0Sbasepu: float
    "b0 (Sbase)"
    bSbasepu: float
    "b (Sbase)"
    boltResOn: int
    "Bolted joint"
    bus1: object
    "Terminal i"
    bus2: object
    "Terminal j"
    cAllowCntConstrFilt: int
    "Constraint Filtering: Allow contingency filtering by number of critical constraints"
    cAllowMarginFilt: int
    "Constraint Filtering: Allow filtering by constraint margin"
    cCab: int
    "Line is a cable"
    cDisplayName: str
    "Display Name"
    cIsSepCntConstrType: int
    "Max. loading constraint for contingencies: Separate constraint type"
    cIsSepCntMaxAllowedLoading: int
    "Max. loading constraint for contingencies: Separate max. allowed loading"
    cNrCust: int
    "Definition of Line Load: Number of Customers"
    cSav: float
    "Definition of Line Load: Average Load"
    cSmax: float
    "Definition of Line Load: Max. Load"
    cTa0_rms: float
    "Results of line parameter calculation: Travel time, mode 0"
    cTa1_rms: float
    "Results of line parameter calculation: Travel time, mode 1"
    cTa2_rms: float
    "Results of line parameter calculation: Travel time, mode 2"
    cUserDefIndex: int
    "User defined Index"
    c_Ta0: float
    "Results of Line Parameters Calculation: Travel Time, Mode 0"
    c_Ta1: float
    "Results of Line Parameters Calculation: Travel Time, Mode 1"
    c_Ta2: float
    "Results of Line Parameters Calculation: Travel Time, Mode 2"
    c_aAtDC: float
    "Wave propagation, DC"
    c_adcULM: float
    "Wave propagation, DC"
    c_pCompi: object
    "Compensation i"
    c_pCompj: object
    "Compensation j"
    c_pTadULM: float
    "Travel time"
    c_pa0: int
    "Results of Line Parameters Calculation: A0, N Poles"
    c_pa1: int
    "Results of Line Parameters Calculation: A1, N Poles"
    c_pa2: int
    "Results of Line Parameters Calculation: A2, N Poles"
    c_paULM: int
    "A, Number of poles:"
    c_pcond: object
    "Conductor Type"
    c_pcoup: list
    "Coupled Line"
    c_ptow: object
    "Line Couplings"
    c_pysULM: float
    "Surge admittance"
    c_pz0: int
    "Results of Line Parameters Calculation: Z0, N Poles/Zeros"
    c_pz1: int
    "Results of Line Parameters Calculation: Z1, N Poles/Zeros"
    c_pz2: int
    "Results of Line Parameters Calculation: Z2, N Poles/Zeros"
    c_rmsErrorA_ULM: float
    "RMS error for A"
    c_rmsErrorY_ULM: float
    "RMS error for Y"
    c_za0: int
    "Results of Line Parameters Calculation: A0, N Zeros"
    c_za1: int
    "Results of Line Parameters Calculation: A1, N Zeros"
    c_za2: int
    "Results of Line Parameters Calculation: A2, N Zeros"
    ca0dc_rms: float
    "Results of line parameter calculation: Wave propagation, DC, mode 0"
    ca1dc_rms: float
    "Results of line parameter calculation: Wave propagation, DC, mode 1"
    ca2dc_rms: float
    "Results of line parameter calculation: Wave propagation, DC, mode 2"
    cb_expsun: int
    "Environment Conditions: Exposed to direct sunlight"
    ccosphi: float
    "Definition of Line Load: Power Factor"
    cdisp_col: list
    "Display data for phase matrix index"
    cdisp_row: list
    "Display data for phase matrix row"
    cfshcloc: float
    "Short-Circuit Location"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    ci_model: int
    "Line Model"
    cimRdfId: list
    "RDF ID"
    cka0_rms: float
    "Wave propagation constant"
    cka1_rms: float
    "Wave propagation constant."
    cka2_rms: float
    "Wave propagation constant."
    ckz0_rms: float
    "Results of line parameter calculation: Surge impedance, HF, mode 0."
    ckz1_rms: float
    "Results of line parameter calculation: Surge Impedance, HF, mode 1."
    ckz2_rms: float
    "Results of line parameter calculation: Surge Impedance, HF, mode 2."
    clnedf: float
    "Derating Factor"
    cmeth: str
    "Old Reference Method"
    cmethChr: str
    "Reference Method"
    cmethChrBs: str
    "Reference Method"
    cmethChrNfc: str
    "Reference Method"
    cmethChrNfcmv: str
    "Reference Method"
    cnm_elm: float
    "Line"
    cnm_typ: float
    "Type"
    cntConstrType: int
    "Max. loading constraint for contingencies: Contingency-constraint type:Off:Soft constraint"
    cntMaxAllowedLoading: float
    "Max. loading constraint for contingencies: Max. allowed loading in Contingencies"
    commissionDate: str
    "Commissioning Date"
    conTrain: list
    "Train"
    conTrainPos: list
    "Train position"
    condMat: int
    "Type Parameters: Conductor Material:Aluminium:Copper:Aldrey (AlMgSi):Aluminium-Steel:Aldrey-Steel"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cshcloc: float
    "Short-Circuit Location"
    cubsecs: list
    "Sections/Line Loads/Compensation"
    cvaltyp: int
    "According to Standard"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dataExtValue: list
    "Value"
    dbg_fullBodeIntegral: int
    "Vector fitting: Full Bode integral"
    dbg_largePolesToConst: int
    "Vector fitting: Replace large poles by constants"
    dcCorr: int
    "Vector fitting: Apply DC correction"
    delayIdx: list
    "Delay index"
    desc: list
    "Description"
    disp_col: int
    "Display data for phase matrix index"
    disp_row: int
    "Display data for phase matrix row"
    dist_a: float
    "Line loop inductance: Distance between cables"
    dline: float
    "Parameters: Length of Line"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    dryingoutavoid: int
    "Soil drying-out avoided"
    ducts: int
    "Number of Ducts"
    earthReturn: int
    "Earth return formula:Carson:Deri-Semlyen"
    fd_model: int
    "Line Parameters Calculation: Line Model"
    fline: float
    "Parameters: Derating Factor"
    fmax: float
    "Line Parameters Calculation: Max. Frequency of Parameter Fitting"
    fmin: float
    "Line Parameters Calculation: Min. Frequency of Parameter Fitting"
    fold_id: object
    "In Folder"
    forTrainSim: int
    "Line for train simulation"
    for_name: str
    "Foreign Key"
    fshcloc: float
    "Short-Circuit Location"
    ftau: float
    "Line Parameters Calculation: Frequency for Travel-Time Estimation"
    ftau_rms: float
    "Frequency for travel-time estimation"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    grpPoles: list
    "Poles per group"
    iAreaBus: int
    "Area"
    iComDate: int
    "Commissioning Date"
    iOPFCload: int
    "Max. loading constraint"
    iSchemeStatus: int
    "Scheme Status"
    iSpecLoc: int
    "Specific Cable Location"
    iZoneBus: int
    "Zone"
    i_const_rms: int
    "Line model: Travelling wave"
    i_dist: int
    "Line Model"
    i_ldlv: int
    "Line Load"
    i_model: int
    "Line Model"
    icond: int
    "Bunched in Air, on Surface, Embedded or Enclosed"
    if_depth: float
    "Installation Conditions: Depth of Laying"
    inAir: int
    "Parameters: Laying:Ground:Air"
    induct: int
    "Cable in Duct"
    initypset: int
    "Missing Type"
    internalDataLayout: int
    "Internal data layout"
    iopt_dir: str
    "Installation Conditions: Arrangement"
    iopt_engine: int
    "Installation Conditions: Cables for powering mobile gear with drum winding"
    iopt_grp: int
    "Installation Conditions: Grouping:Single Layer on Wall, Floor or Unperforated Tray:Single Layer Fixed Directly under Wooden or Masonry Ceiling"
    iopt_laid: int
    "Laid on:Perforated trays:Unperforated trays:Ladders, Supports or Cleats"
    iopt_ord: str
    "Installation Conditions: Cable Formation"
    iopt_tem: int
    "Line Parameters Calculation: Temperature Dependency"
    iopt_tem_rms: int
    "Line parameter calculation: Temperature dependency"
    iopt_turns: int
    "Installation Conditions: Drum winding with multiple turns"
    iperfect: int
    "Failures: Ideal component"
    isConstrLoading: int
    "Max. loading constraint for Unit Commitment"
    isConstrLoadingPlacement: int
    "Max. loading constraint for Optimal Equipment Placement"
    isMaxLoadSoftNlin: int
    "Penalty costs for soft constraints"
    isSepCntConstrType: int
    "Max. loading constraint for contingencies: Separate constraint type"
    isSepCntMaxAllowedLoading: int
    "Max. loading constraint for contingencies: Separate max. allowed loading"
    ishclne: int
    "Available"
    isoMat: int
    "Type Parameters: Insulation Material:PVC:XLPE/EPR:Mineral:Paper"
    iterVFA: int
    "Vector fitting: Max. number of iterations"
    iterVFY: int
    "Vector fitting: Max. number of iterations"
    ka0: float
    "Wave Propagation Constant"
    ka1: float
    "Wave Propagation Constant."
    ka2: float
    "Wave Propagation Constant."
    ktrto: int
    "Transposition"
    kz0: float
    "Results of Line Parameters Calculation: Surge Impedance, HF, Mode 0."
    kz1: float
    "Results of Line Parameters Calculation: Surge Impedance, HF, Mode 1."
    kz2: float
    "Results of Line Parameters Calculation: Surge Impedance, HF, Mode 2."
    loadfactor: float
    "Load factor (lf)"
    loc_name: str
    "Name"
    lossAssign: int
    "Loss assignment:according to grouping:uniformly distributed:to Terminal i:to Terminal j"
    lossModel_emt: int
    "Loss model:R/4 at both ends; R/2 in the middle:R/2 at both ends"
    lossModel_rms: int
    "Line model: Loss model:R/2 at both ends"
    maxErrVFA: float
    "Vector fitting: RMS error"
    maxErrVFY: float
    "Vector fitting: RMS error"
    maxResPoleRatioA: float
    "Max. residue-pole ratio"
    maxResPoleRatioY: float
    "Max. residue-pole ratio"
    maxload: float
    "Thermal Loading Limit: Max. loading"
    mediumTemp: float
    "Medium mean temperature"
    meth: str
    "Installation Conditions: Reference Method"
    meth_bs: str
    "Installation Conditions: Reference Method"
    meth_nfc: str
    "Installation Conditions: Reference Method"
    meth_nfcmv: str
    "Installation Conditions: Reference Method"
    methodVFA: int
    "Vector fitting: Number of poles:Increase and flip unstable poles:Increase until rms met"
    methodVFY: int
    "Vector fitting: Number of poles:Increase and flip unstable poles:Increase until rms met"
    minResTrainDist: float
    "Min. resolution of train distances"
    nconTrains: int
    "No. of trains"
    nlnum: int
    "Number of: parallel Lines"
    nlsim: int
    "Enable for Contingency Analysis"
    npara: int
    "Installation Conditions: Grouped Cables"
    occupCoeff: float
    "Installation Conditions: Occupation coefficient"
    oid_: int
    "ObjectID"
    outputPoles: int
    "Vector fitting: Output poles"
    outserv: int
    "Out of Service"
    pCondCir: object
    "Type of phase conductors"
    pCondGnd: object
    "Type of earth conductors"
    pCondN: object
    "Type of neutral conductors"
    pMeteo: object
    "Parameters: Meteo. Station"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pRating: object
    "Parameters: Thermal Rating"
    pStoch: object
    "Failures: Element model"
    pTa: list
    "Travel Time"
    pTypStoch: object
    "Failures: Type model"
    pa: list
    "Wave Propagation"
    pa0: list
    "Poles, A0"
    pa1: list
    "Poles, A1"
    pa2: list
    "Poles, A2"
    phiz1: float
    "Resulting Values: Pos. Seq. Impedance, Angle"
    pid_: int
    "ProjectID"
    polesA_Im: list
    "Poles of A (Im)"
    polesA_Re: list
    "Poles of A (Re)"
    polesVFA: int
    "Vector fitting: Max. number of poles"
    polesVFY: int
    "Vector fitting: Max. number of poles"
    polesY_Im: list
    "Poles of Y (Im)"
    polesY_Re: list
    "Poles of Y (Re)"
    pys: list
    "Surge Admittance"
    pz0: list
    "Poles, Mode 0"
    pz1: list
    "Poles, Mode 1"
    pz2: list
    "Poles,Mode 2"
    qurs_A: float
    "Joint cross-section"
    r0Sbasepu: float
    "r0 (Sbase)"
    r0mSbasepu: list
    "r0m (Sbase)"
    rSbasepu: float
    "r (Sbase)"
    rearth: float
    "Earth resistivity"
    resA_Im: list
    "Residues of Z (Im)"
    resA_Re: list
    "Residues of Z (Re)"
    resY_Im: list
    "Residues of Y (Im)"
    resY_Re: list
    "Residues of Y (Re)"
    root_id: object
    "Original Location"
    sagCir: float
    "Max.sag, phase conductors"
    sagGnd: float
    "Max.sag, earth conductors"
    scalingFacSoftConstrCost: float
    "Penalty costs for soft constraints: Cost scaling factor"
    scalingFacSoftConstrOpf: float
    "Max. loading constraint: Weighting factor for soft constraint penalty"
    sernum: str
    "Serial Number"
    shMat: int
    "Type Parameters: Sheath Insulation:PVC:XLPE/EPR"
    soilThermRes: float
    "Environment Conditions: Soil thermal resistivity"
    soilThermResdry: float
    "Dry soil thermal resistivity"
    soiltyp: int
    "Environment Conditions: Soil Type:Underwater:Very Moist:Moist:Normal:Dry:Very Dry"
    solar_rad: float
    "Solar radiation intensity"
    stMarginA: float
    "Vector fitting: Stability margin"
    stMarginY: float
    "Vector fitting: Stability margin"
    summandDelayIdx: list
    "Delay index for summand"
    temp_env: float
    "Environment Conditions: Ambient temperature"
    thetaX: float
    "Critical temperature of soil"
    thick_d: float
    "Bolted joint resistance: Joint thickness"
    tid_: int
    "TimeID"
    tmat: list
    "Transformation Matrix"
    tolBode: float
    "Line Parameters Calculation: Tolerance for Bode Approximation"
    trans_ff: float
    "Failures Transient Faults: Transient Fault Frequency"
    trays: int
    "Installation Conditions: Number of Trays/Ducts"
    tuneDelays: int
    "Vector fitting: Fine-tune delays"
    txt_typ: str
    "Type of Line"
    typ_id: object
    "Type"
    typ_res: int
    "Index of cable type stored in results vector"
    useDCcorr: int
    "Apply DC correction"
    windvelocity: float
    "Wind velocity"
    x0Sbasepu: float
    "x0 (Sbase)"
    x0mSbasepu: list
    "x0m (Sbase)"
    xSbasepu: float
    "x (Sbase)"
    za0: list
    "Zeros, A0"
    za1: list
    "Zeros, A1"
    za2: list
    "Zeros, A2"
    zz0: list
    "Zeros, Zl0"
    zz1: list
    "Zeros, Z1"
    zz2: list
    "Zeros, Z2"

    def AreDistParamsPossible(*args): ...

    def AttributeType(*args): ...

    def CreateFeederWithRoutes(*args): ...

    def FitParams(*args): ...

    def GetIthr(*args): ...

    def GetType(*args): ...

    def GetY0m(*args): ...

    def GetY1m(*args): ...

    def GetZ0m(*args): ...

    def GetZ1m(*args): ...

    def GetZmatDist(*args): ...

    def HasReferences(*args): ...

    def HasRoutes(*args): ...

    def HasRoutesOrSec(*args): ...

    def IsCable(*args): ...

    def IsNetCoupling(*args): ...

    def MeasureLength(*args): ...

    def SetDetailed(*args): ...

    def __getattr__(*args): ...


class ElmLnesec(PFGeneral):
    B1: float
    "Susceptance B1"
    C0: float
    "Capacitance C0"
    C1: float
    "Capacitance C1"
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures Double Earth Fault: Repair duration"
    FOD: float
    "Failures Line Failures: Forced Outage Duration"
    FOE: float
    "Failures Line Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures Line Failures: Forced Outage Rate"
    Ice: float
    "Resulting Values: Earth-Fault Current, Ice"
    Imaxlim: float
    "Max. permissible current"
    Inom: float
    "Resulting Values: Nominal Current"
    Inom_a: float
    "Resulting Values: Nominal Current (act.)"
    Irated: float
    "Type Parameters: Rated Current"
    R0: float
    "Resulting Values: Zero Seq. Resistance, R0"
    R1: float
    "Resulting Values: Pos. Seq. Resistance, R1"
    Top: float
    "Operating Temperature"
    Unom: float
    "Rated Voltage"
    X0: float
    "Resulting Values: Zero Seq. Reactance, X0"
    X1: float
    "Resulting Values: Pos. Seq. Reactance, X1"
    Z1: float
    "Resulting Values: Pos. Seq. Impedance, Z1"
    alpha: float
    "Neher-McGrath: Medium diffusivity"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    armTyp: int
    "Type Parameters: Armour Type:AWA:SWA"
    asys: int
    "Installation Conditions: Clearance :Touching:1x Cable Diameter:d <= 0.125 m:0.125 m < d <= 0.25 m:0.25 m < d <= 0.5 m:0.5 m < d <= 1.0 m"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    cb_expsun: int
    "Environment Conditions: Exposed to direct sunlight"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    clnedf: float
    "Derating Factor"
    cmeth: str
    "Old Reference Method"
    cmethChr: str
    "Reference Method"
    cmethChrBs: str
    "Reference Method"
    cmethChrNfc: str
    "Reference Method"
    cmethChrNfcmv: str
    "Reference Method"
    commissionDate: str
    "Commissioning Date"
    condMat: int
    "Type Parameters: Conductor Material:Aluminium:Copper:Aldrey (AlMgSi):Aluminium-Steel:Aldrey-Steel"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cvaltyp: int
    "According to Standard"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dataExtValue: list
    "Value"
    desc: list
    "Description"
    dline: float
    "Topology: Length"
    doc_id: object
    "Additional Data"
    dryingoutavoid: int
    "Soil drying-out avoided"
    ducts: int
    "Number of Ducts"
    fline: float
    "Topology: Derating Factor"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iComDate: int
    "Commissioning Date"
    iSchemeStatus: int
    "Scheme Status"
    iSpecLoc: int
    "Specific Cable Location"
    icond: int
    "Bunched in Air, on Surface, Embedded or Enclosed"
    if_depth: float
    "Installation Conditions: Depth of Laying"
    inAir: int
    "Topology: Laying:Ground:Air"
    index: float
    "Index"
    induct: int
    "Cable in Duct"
    initypset: int
    "Missing Type"
    iopt_dir: str
    "Installation Conditions: Arrangement"
    iopt_engine: int
    "Installation Conditions: Cables for powering mobile gear with drum winding"
    iopt_grp: int
    "Installation Conditions: Grouping:Single Layer on Wall, Floor or Unperforated Tray:Single Layer Fixed Directly under Wooden or Masonry Ceiling"
    iopt_laid: int
    "Laid on:Perforated trays:Unperforated trays:Ladders, Supports or Cleats"
    iopt_ord: str
    "Installation Conditions: Cable Formation"
    iopt_turns: int
    "Installation Conditions: Drum winding with multiple turns"
    iperfect: int
    "Failures: Ideal component"
    isoMat: int
    "Type Parameters: Insulation Material:PVC:XLPE/EPR:Mineral:Paper"
    loadfactor: float
    "Neher-McGrath: Load factor (lf)"
    loc_name: str
    "Name"
    mediumTemp: float
    "Neher-McGrath: Medium mean temperature"
    meth: str
    "Installation Conditions: Reference Method"
    meth_bs: str
    "Installation Conditions: Reference Method"
    meth_nfc: str
    "Installation Conditions: Reference Method"
    meth_nfcmv: str
    "Installation Conditions: Reference Method"
    npara: int
    "Installation Conditions: Grouped Cables"
    occupCoeff: float
    "Installation Conditions: Occupation coefficient"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pRating: object
    "Topology: Thermal Rating"
    pStoch: object
    "Failures: Element model"
    pTypStoch: object
    "Failures: Type model"
    phiz1: float
    "Resulting Values: Pos. Seq. Impedance, Angle"
    pid_: int
    "ProjectID"
    rellen: float
    "Topology: Start of Section"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    shMat: int
    "Type Parameters: Sheath Insulation:PVC:XLPE/EPR"
    soilThermRes: float
    "Environment Conditions: Soil thermal resistivity"
    soilThermResdry: float
    "Dry soil thermal resistivity"
    soiltyp: int
    "Environment Conditions: Soil Type:Underwater:Very Moist:Moist:Normal:Dry:Very Dry"
    solar_rad: float
    "Solar radiation intensity"
    temp_env: float
    "Environment Conditions: Ambient temperature"
    thetaX: float
    "Critical temperature of soil"
    tid_: int
    "TimeID"
    trans_ff: float
    "Failures Transient Faults: Transient Fault Frequency"
    trays: int
    "Installation Conditions: Number of Trays/Ducts"
    txt_typ: str
    "Topology: Type of Line"
    typ_id: object
    "Type"
    typ_res: int
    "Index of cable type stored in results vector"
    windvelocity: float
    "Neher-McGrath: Wind velocity"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def IsCable(*args): ...

    def __getattr__(*args): ...


class ElmMdl(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    arrayName: list
    "Parameter"
    arrayObject: list
    "Array/Matrix"
    cDisplayName: str
    "Display Name"
    cMax: list
    "Max"
    cMin: list
    "Min"
    cUserDefIndex: int
    "User defined Index"
    carrayDesc: list
    "Description"
    carrayName: list
    "Name"
    carrayUnit: list
    "Unit"
    cattrDesc: list
    "Description"
    cattrUnit: list
    "Unit"
    cfmuType: int
    "FMU Type"
    charact: list
    "Charact."
    checksum: list
    "Checksum"
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    clockPeriod: float
    "Sampling options: Sampling period"
    clockRate: float
    "Sampling options: Sampling rate"
    clockSampling: int
    "Sampling options"
    configScript: object
    "Configuration Script"
    contents: list
    "Events"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fmuCoSimMethod: int
    "FMU Co-Simulation calculation method"
    fmuCsPeriod: float
    "Sampling options: Sampling period"
    fmuCsRate: float
    "Sampling options: Sampling Rate"
    fmuCsSampling: int
    "Sampling options"
    fmuType: int
    "FMU Type"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    forceSlowFmuPfmu: int
    "Use as standard FMU/PFMU"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    parameterNames: list
    "Parameter Names"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    subSampleFactor: int
    "Sub sampling factor"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"

    def AttributeType(*args): ...

    def ExportToClipboard(*args): ...

    def ExportToFile(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmNec(PFGeneral):
    Curn: float
    "Rated Current (Ie=3*I0)"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Irze: list
    "Rated Current of Grounding"
    Ithlim: float
    "Rated Short-Time Thermal Current (3*I0)"
    R0: float
    "Zero Sequence Resistance"
    Re: float
    "Internal Grounding Impedance: Resistance, Re"
    Tkr: float
    "Rated Short-Circuit Duration"
    Unom: float
    "Rated Voltage"
    X0: float
    "Zero Sequence Reactance"
    Xe: float
    "Internal Grounding Impedance: Reactance, Xe"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal"
    bus1n: object
    "Neutral Conductor: Neutral"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    cgnd: int
    "Internal Grounding Impedance: Star Point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpeter: int
    "Internal Grounding Impedance: Petersen Coil"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fcharL0: object
    "Frequency Dependency L0"
    fcharLe: object
    "Frequency Dependency Le"
    fcharR0: object
    "Frequency Dependency R0"
    fcharRe: object
    "Frequency Dependency Re"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iComDate: int
    "Commissioning Date"
    iSchemeStatus: int
    "Scheme Status"
    ignd: int
    "Star Point:&0&grounded:&2&isolated"
    iintgnd: int
    "Neutral Conductor: N-Connection:None:At terminal (ABC-N):Separate terminal"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def GetGroundingImpedance(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmNet(PFGeneral):
    InterPset: float
    "Consider Interchange Schedule: Scheduled Active Power Interchange"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cimRdfId: list
    "RDF ID"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    dpl1: float
    "dpl1"
    dpl10: float
    "dpl10"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    dpl6: float
    "dpl6"
    dpl7: float
    "dpl7"
    dpl8: float
    "dpl8"
    dpl9: float
    "dpl9"
    fictborder: int
    "Fictitious border grid"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frnom: float
    "Nominal Frequency"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iInterChg: int
    "Consider Interchange Schedule"
    iSchemeStatus: int
    "Scheme Status"
    icolor: int
    "Colour"
    isConsSpinReserve: int
    "Min. spinning reserve constraint"
    isummary: int
    "flag for summary grid"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    owner: str
    "Owner"
    pDiagram: object
    "Diagram"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    spinReserve: float
    "Min. spinning reserve constraint: Spinning reserve"
    tid_: int
    "TimeID"

    def Activate(*args): ...

    def AttributeType(*args): ...

    def CalculateInterchangeTo(*args): ...

    def CalculateVoltInterVolt(*args): ...

    def CalculateVoltageLevel(*args): ...

    def Deactivate(*args): ...

    def DefineBoundary(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmPvsys(PFGeneral):
    EDS: float
    "Stochastic Model for Generation: Expectancy of derated states"
    Ebh_a: float
    "Direct Horizontal Irradiance (act.)"
    Ebpv_a: float
    "Direct Irradiance, PV Panel (act.)"
    Edh_a: float
    "Diffuse Horizontal Irradiance (act.)"
    Edpv_a: float
    "Diffuse Irradiance, PV Panel (act.)"
    Egh_a: float
    "Global Horizontal Irradiance (act.)"
    Egpv_a: float
    "Global Irradiance, PV Panel (act.)"
    Erpv_a: float
    "Reflected Irradiance, PV Panel (act.)"
    FAY: float
    "Stochastic Model for Generation: Full Availability Expectancy"
    FOE: float
    "Stochastic Model for Generation: Forced Outage Expectancy"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Ik: float
    "Fault Contribution: Steady-State Shc. Current"
    IkPFmax: float
    "Steady-state short-circuit current contribution: Maximum current"
    IkPFmin: float
    "Steady-state short-circuit current contribution: Minimum current"
    Iks: float
    "Fault Contribution: Transient Short-Circuit Current"
    Ikss: float
    "Max. Fault Contribution: Subtransient Short-Circuit Current"
    Ikss1PF: float
    "Initial symmetrical short-circuit current contribution: Single-phase faults, Ik1PF"
    Ikss2PF: float
    "Initial symmetrical short-circuit current contribution: Two-phase faults, Ik2PF"
    Ikss3PF: float
    "Initial symmetrical short-circuit current contribution: Three-phase faults, Ik3PF"
    Inom: float
    "Nominal Current"
    Irated: float
    "Harmonic Source: Rated Current"
    Irze: list
    "Rated Current of Grounding"
    Kd: float
    "Current controller: Kd: d-Axis, proportional gain"
    Kfactor: float
    "Fault Contribution: K Factor"
    Ki_plli: float
    "Current PLL: Integration Gain"
    Ki_pllu: float
    "Voltage PLL: Integration Gain"
    Kp_plli: float
    "Current PLL: Proportional Gain"
    Kp_pllu: float
    "Voltage PLL: Proportional Gain"
    Kpf: float
    "Operating Point Active Power: Prim. Frequency Bias"
    Kq: float
    "Current controller: Kq: q-Axis, proportional gain"
    P_max: float
    "Active Power: Rating: Max."
    Pcu: float
    "Series reactor: Copper losses"
    PmaxInv: float
    "Separate consumption mode: Max."
    PmaxInvPU: float
    "Separate consumption mode: Max."
    Pmax_a: float
    "Pmax(act.)"
    Pmax_uc: float
    "Active Power Operational Limits: Max."
    Pmax_ucPU: float
    "Active Power Operational Limits: Max."
    PminInv: float
    "Separate consumption mode: Min."
    PminInvPU: float
    "Separate consumption mode: Min."
    Pmin_a: float
    "Pmin(act.)"
    Pmin_uc: float
    "Active Power Operational Limits: Min."
    Pmin_ucPU: float
    "Active Power Operational Limits: Min."
    Pngrel: float
    "Stochastic Model for Generation: Based on rated active power (Pr)"
    Pnom: float
    "Active Power Operational Limits: Pr(rated)"
    Qfu_max: float
    "Q(V)-Characteristic: Q max"
    Qfu_min: float
    "Q(V)-Characteristic: Q min"
    Qmax_a: float
    "Qmax(act.)"
    Qmin_a: float
    "Qmin(act.)"
    QtargetBase: int
    "Optimisation of reactive power reserve: Base:Reactive power limits:Rated apparent power"
    QtargetRPR: float
    "Optimisation of reactive power reserve: Q target value"
    R0hmc: float
    "Norton Equivalent: Resistance, R0h"
    R0toR1: float
    "Series reactor: R0/R1 ratio"
    R1hmc: float
    "Norton Equivalent: Resistance, R1h"
    R2hmc: float
    "Norton Equivalent: Resistance, R2h"
    RelEff_a: float
    "Relative Efficiency (act.)"
    Sk: float
    "Fault Contribution: Steady-State Short-Circuit Level"
    Sks: float
    "Fault Contribution: Transient Short-Circuit Level"
    Skss: float
    "Max. Fault Contribution: Subtransient Short-Circuit Level"
    T1_plli: float
    "Current PLL: Low-Pass Filter Time Constant"
    T1_pllu: float
    "Voltage PLL: Low-Pass Filter Time Constant"
    Tamb: float
    "Environment Factors: Ambient Temperature"
    Tamb_a: float
    "Amb. Temp. (act.)"
    Td: float
    "Current controller: Td: d-Axis, integration time constant"
    Tdelay: float
    "Current source model: Delay time constant"
    Tondelay: float
    "Min. operation voltage: Switch-on delay"
    Tq: float
    "Current controller: Tq: q-Axis, integration time constant"
    X0hmc: float
    "Norton Equivalent: Reactance, X0h"
    X0toX1: float
    "Series reactor: X0/X1 ratio"
    X1hmc: float
    "Norton Equivalent: Reactance, X1h"
    X2hmc: float
    "Norton Equivalent: Reactance, X2h"
    aCategory: str
    "Plant Category"
    albedo: float
    "Environment Factors: Ground Albedo"
    albedo_a: float
    "Albedo (act.)"
    allowConsumMode: int
    "Separate consumption mode"
    allowGenMode: int
    "Separate generation mode"
    anginc_a: float
    "Angle of Incidence (act.)"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    av_mode: str
    "Local Controller"
    availFactor: float
    "Availability Factor"
    avgCosts: float
    "Average costs"
    avgCostsUc: float
    "Piecewise linearisation for LP: Average costs"
    bus1: object
    "Terminal"
    bus1n: object
    "Neutral Conductor: Neutral"
    bustp: str
    "Corresponding Bus Type:"
    cCategory: str
    "Plant Category"
    cDisplayName: str
    "Display Name"
    cGPSlat: float
    "System Geographical Location: Latitude"
    cGPSlon: float
    "System Geographical Location: Longitude"
    cIsDiscreteCtrlP: int
    "Restriction to discrete active power values"
    cIsMustRunUC: int
    "Additional constraints for controls: Must run"
    cIsPcurrAllowed: int
    "Allow current active power value"
    cQ_max: float
    "Reactive Power Operational Limits: Maximum"
    cQ_min: float
    "Reactive Power Operational Limits: Minimum"
    cStorage: object
    "Generator usage: Storage model"
    cTypHmc: str
    "Harmonic Source: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    cVecDiscreteCtrlPvals: list
    "Valid active power values"
    c_pCtrlHV: object
    "Controlled HV-busbar"
    c_pmod: object
    "Model"
    c_psecc: object
    "External Secondary Controller"
    c_pstac: object
    "External Station Controller"
    ccost: list
    "Costs"
    cfixedCosts: float
    "Consumption mode: Fixed costs"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    coldStartTime: float
    "Start-up costs: Cold-start time"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    consumCosts: float
    "Consumption mode: Consumption costs"
    cosgini: float
    "Operating Point Reactive Power/Voltage: Power Factor"
    cosgini_a: float
    "Actual Operating Point: Power Factor (act.)"
    cosini: float
    "Power Factor"
    cosn: float
    "Ratings: Rated Power Factor"
    costColdStart: float
    "Start-up costs: Cold-start costs"
    costCurtailment: float
    "Costs for curtailment"
    costRedispatchDown: float
    "Additional redispatch costs: Downward active power redispatch costs"
    costRedispatchP: float
    "Redispatch costs for active power change"
    costRedispatchQ: float
    "Redispatch costs for reactive power change"
    costRedispatchUp: float
    "Additional redispatch costs: Upward active power redispatch costs"
    costShutDown: float
    "Shut-down costs"
    cost_up: float
    "Start-up costs: Warm-start costs"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpower: list
    "Power"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    ddroop: float
    "Voltage Droop: Droop"
    ddroopoe: float
    "Q(V)-Characteristic: Droop (overexcited)"
    ddroopue: float
    "Q(V)-Characteristic: Droop (underexcited)"
    desc: list
    "Description"
    dhi: float
    "Irradiance on the Horizontal Plane: Direct Horizontal Irradiance"
    dhi_a: float
    "Direct Horizontal Irradiance (act.)"
    discMethCostOp: int
    "Piecewise linearisation for LP"
    dispatch: int
    "Generator Dispatch"
    dni: float
    "Irradiance on the Horizontal Plane: Direct Normal Irradiance"
    dni_a: float
    "Direct Normal Irradiance (act.)"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    dsecres: float
    "Reserve"
    efficiencyCurveConsum: object
    "Efficiency: Efficiency curve (consumption)"
    efficiencyCurveGen: object
    "Efficiency: Efficiency curve (generation)"
    efficiencyLPconsum: float
    "Efficiency: Used efficiency (consumption)"
    efficiencyLPgen: float
    "Efficiency: Used efficiency (generation)"
    fcharr0: object
    "Norton Equivalent: Frequency-dependence, r0h(f)"
    fcharr1: object
    "Norton Equivalent: Frequency-Dependence, r1h(f)"
    fcharr2: object
    "Norton Equivalent: Frequency-Dependence, r2h(f)"
    fcharx0: object
    "Norton Equivalent: Frequency-dependence, x0h(f)"
    fcharx1: object
    "Norton Equivalent: Frequency-Dependence, x1h(f)"
    fcharx2: object
    "Norton Equivalent: Frequency-Dependence, x2h(f)"
    fixed: int
    "Must run"
    fixedCosts: float
    "Fixed costs"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    genShiftKey: float
    "Generation shift key"
    ghi: float
    "Irradiance on the Horizontal Plane: Global Horizontal Irradiance"
    ghi_a: float
    "Global Horizontal Irradiance (act.)"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iDelay: int
    "Current source model: dq-reference angle delay (if dq-reference signals not connected)"
    iInterPol: int
    "Approximation:Spline:Piecewise linear:Polynomial:Hermite"
    iNoShcContr: int
    "No Short-Circuit Contribution"
    iOPFCPmax: int
    "Active Power Operational Limits: Max."
    iOPFCPmin: int
    "Active Power Operational Limits: Min."
    iOPFCQmax: int
    "Reactive Power Operational Limits: Max."
    iOPFCQmin: int
    "Reactive Power Operational Limits: Min."
    iSchemeStatus: int
    "Scheme Status"
    iShcModel: int
    "Short-Circuit Model:&0&Equivalent synchronous machine:&1&Dynamic voltage support:&3&Full size converter"
    iSimModel: int
    "Model:According to connected input signals:Current source:Voltage source:Constant impedance:Constant power"
    iUseNegSeqAngle: int
    "Negative sequence: Current source model: Use negative sequence angle for negative sequence current source"
    iUseZsr: int
    "Negative sequence: Use series reactor impedance, if negative sequence voltage signals are connected"
    iconfed: int
    "Static Converter-Fed Drive"
    ictpg: int
    "Controls: Active Power"
    ictqg: int
    "Controls: Reactive Power"
    icurref: int
    "Harmonic Source: Harmonic currents referred to"
    idisp: int
    "Generator Dispatch"
    iearthed: int
    "Earthed"
    iestp: int
    "State Estimation: Estimate Active Power"
    iestq: int
    "State Estimation: Estimate Reactive Power"
    imax: float
    "Fault Contribution: Max. Current"
    inveff: float
    "Inverter: Efficiency Factor"
    iopt_dif: int
    "Irradiance on the Horizontal Plane: Diffuse Irradiance Data:Louche et.al. Model:Spencer Model:Erbs Model:Lam-Li Model:Reindl et.al. Model:Orgill-Holands Model:Liu-Jordan Model:Bougler Model"
    iopt_dir: int
    "Irradiance on the Horizontal Plane: Direct Irradiance Data:Hourly Data, Horizontal (DHI):Hourly Data, Normal (DNI)"
    iopt_glo: int
    "Irradiance on the Horizontal Plane: Global Irradiance Data:Adnot-Bourges et.al. Model:Kasten-Czeplak Model:Robledo-Soler Model:Haurwitz Model:Berges-Duffie Model:Hourly Clearness Index:Hourly Data (GHI)"
    iopt_rad: int
    "Irradiance on the Horizontal Plane: Specified Components:Global + Direct:Global + Diffuse:Direct + Diffuse"
    iopt_tdr: int
    "Q(V)-Characteristic: Different droop values"
    ip_ctrl: int
    "Reference Machine"
    is4SpinReserve: int
    "Consider for region spinning reserve"
    isConsCostOp: int
    "Operating costs"
    isConsCostsRedispatch: int
    "Additional redispatch costs"
    isConsShutDownCost: int
    "Shut-down costs"
    isConsStartUpCost: int
    "Start-up costs"
    isConstrRamp: int
    "Ramp rate constraints"
    isConstrUpDown: int
    "Start-up/shut-down time constraints"
    isCtrlFixedToLdfVal: int
    "Additional constraints for controls: Fix controls to Load Flow values"
    isCtrlP: int
    "Controls: Active power"
    isCtrlPplacement: int
    "Optimise active power"
    isCtrlQ: int
    "Controls: Reactive power"
    isDiscreteCtrlP: int
    "Restriction to discrete active power values"
    isLimPmax: int
    "Active Power Operational Limits: Max."
    isLimPmin: int
    "Active Power Operational Limits: Min."
    isLimQmax: int
    "Reactive Power Operational Limits: Max."
    isLimQmin: int
    "Reactive Power Operational Limits: Min."
    isMustRunUC: int
    "Additional constraints for controls: Must run"
    isPcurrAllowed: int
    "Restriction to discrete active power values: Allow current active power value"
    isRPR: int
    "Optimisation of reactive power reserve"
    isVRE: int
    "Generator usage: Generator usage:Single thermal generation unit:Variable renewable energy source (VRE):Coupled with storage model:Part of Virtual Power Plant"
    iv_mode: int
    "Local Controller"
    kt: float
    "Irradiance on the Horizontal Plane: Clearness Index"
    kt_a: float
    "Clearness Index (act.)"
    ktc_a: float
    "Calculated Clearness Index"
    limRampDown: float
    "Ramp rate constraints: Ramp-down limit"
    limRampDownPU: float
    "Ramp rate constraints: Ramp-down limit"
    limRampShutDown: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampShutDownPU: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampStartUp: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampStartUpPU: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampUp: float
    "Ramp rate constraints: Ramp-up limit"
    limRampUpPU: float
    "Ramp rate constraints: Ramp-up limit"
    loc_name: str
    "Name"
    minDownTime: float
    "Start-up/shut-down time constraints: Minimum down-time"
    minUpTime: float
    "Start-up/shut-down time constraints: Minimum up-time"
    mode_inp: str
    "Operating Point Reactive Power/Voltage: Input Mode"
    mode_pgi: int
    "Model:Active Power Input:Solar Calculation"
    mount: int
    "Orientation and Tilt: Mounting System:Fixed/Stationary:Dual Axis Tracking System:Horizontal Single Axis Tracking System:Vertical Single Axis Tracking System"
    ngnum: int
    "Number of: Parallel Inverters"
    nneutral: int
    "Neutral Conductor: N-Connection:None:At terminal (ABC-N):Separate terminal"
    nphase: int
    "No. of Phases"
    npnum: int
    "Number of: Panels per Inverter"
    numBreakpointsCostOp: int
    "Piecewise linearisation for LP: Number of breakpoints"
    oid_: int
    "ObjectID"
    orient: float
    "Orientation and Tilt: Orientation Angle"
    orient_a: float
    "Orientation Angle (act.)"
    outServPzero: int
    "Out of service when active power is zero"
    outserv: int
    "Out of Service"
    pBMU: object
    "Virtual Power Plant"
    pFlicker: object
    "Flicker Coefficients"
    pGRStoch: object
    "Stochastic Model for Generation: Stochastic Model"
    pOpCostCurve: object
    "Operating costs: Generator cost curve"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pQPcurve: object
    "Q(P)-Characteristic: Q(P)-Curve"
    pQlimType: object
    "Reactive Power Operational Limits: Capability Curve"
    pStoch: object
    "Stochastic model"
    pStorage: object
    "Storage model"
    pSubModel: object
    "Submodel"
    p_over: float
    "cosphi(P)-Characteristic Overexcited: Active Power"
    p_under: float
    "cosphi(P)-Characteristic Underexcited: Active Power"
    pblocktrf: object
    "Externally modelled unit transformer: Unit transformer"
    penaltyCosts: float
    "Penalty costs"
    pf_over: float
    "cosphi(P)-Characteristic Overexcited: Min. Power Factor"
    pf_recap: int
    "Operating Point Reactive Power/Voltage: Power Factor:ind.:cap."
    pf_recap_a: str
    "Actual Operating Point: Power Factor Ind/Cap (act.)"
    pf_under: float
    "cosphi(P)-Characteristic Underexcited: Min. Power Factor"
    pfrecap: int
    "Power Factor Ind/Cap"
    pgini: float
    "Operating Point Active Power: Active Power"
    pgini_a: float
    "Actual Operating Point: Active Power (act.)"
    pginirnd: float
    "Active Power for Probabilistic Analysis"
    phiini: float
    "Operating Point Reactive Power/Voltage: Angle"
    phmc: object
    "Harmonic Source: Harmonic Currents"
    phtech: int
    "Technology:3PH:3PH-E:1PH PH-E:1PH PH-N:1PH PH-PH"
    pid_: int
    "ProjectID"
    pini: float
    "Active Power"
    pinput: int
    "Interpretation of input signals: Active Power signal:in kW:in p.u. based on Snom:in p.u. based on Pnom"
    pmaxratf: float
    "Active Power: Rating: Rating Factor"
    polyDegree: int
    "Polynomial degree"
    priority: int
    "Merit Order"
    psutype: str
    "Power station unit type"
    q_max: float
    "Reactive Power Operational Limits: Max."
    q_min: float
    "Reactive Power Operational Limits: Min."
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qgini: float
    "Operating Point Reactive Power/Voltage: Reactive Power"
    qgini_a: float
    "Actual Operating Point: Reactive Power (act.)"
    qini: float
    "Reactive Power"
    qinput: int
    "Interpretation of input signals: Reactive Power signal:in kvar:in p.u. based on Snom:in p.u. based on Pnom:as cos(phi)"
    r0: float
    "Zero sequence: Resistance, r0"
    r0hmc: float
    "Norton Equivalent: Resistance, r0h"
    r0iec: float
    "Zero sequence short-circuit impedance: Resistance, r0"
    r1hmc: float
    "Norton Equivalent: Resistance, r1h"
    r2: float
    "Negative sequence: Resistance r2"
    r2hmc: float
    "Norton Equivalent: Resistance, r2h"
    r2iec: float
    "Negative sequence short-circuit impedance: Resistance, r2"
    r2shc: float
    "Negative sequence short-circuit impedance: Resistance, r2"
    root_id: object
    "Original Location"
    rtox: float
    "Max. Fault Contribution: R to X'' ratio"
    sOpComment: list
    "Operator Comment"
    scale0: float
    "Operating Point: Scaling Factor"
    scale0_a: float
    "Actual Operating Point: Scaling Factor(act.)"
    scaleQmax: float
    "Reactive Power Operational Limits: Scaling Factor (max.)"
    scaleQmin: float
    "Reactive Power Operational Limits: Scaling Factor (min.)"
    searchBlockTrf: int
    "Externally modelled unit transformer"
    sernum: str
    "Serial Number"
    sgini_a: float
    "Actual Operating Point: Apparent Power (act.)"
    sgn: float
    "Ratings: Rated Apparent Power"
    shcDeadband: int
    "Voltage deadband"
    shfdiff: float
    "Environment Factors: Shading Factor (Diffuse)"
    shfdiff_a: float
    "Shading Factor (Diff.) (act.)"
    shfdir: float
    "Environment Factors: Shading Factor (Direct)"
    shfdir_a: float
    "Shading Factor (Dir.) (act.)"
    smoothfac: float
    "Smoothing factor"
    solalt_a: float
    "Solar Altitude Angle (act.)"
    tds: float
    "Time Constants: Td'"
    tdss: float
    "Time Constants: Td''"
    tid_: int
    "TimeID"
    tilt: float
    "Orientation and Tilt: Tilt Angle"
    tilt_a: float
    "Tilt Angle (act.)"
    timezone: str
    "System Geographical Location: Time Zone (Offset)"
    typ_id: object
    "Type"
    uDeadband: float
    "Voltage deadband: Deadband"
    udeadblow: float
    "Q(V)-Characteristic Voltage Dead Band: Lower Voltage Limit"
    udeadbup: float
    "Q(V)-Characteristic Voltage Dead Band: Upper Voltage Limit"
    uk: float
    "Series reactor: Short circuit impedance"
    umin: float
    "Min. operation voltage: Switch-off threshold"
    uonthr: float
    "Min. operation voltage: Switch-on threshold"
    usetp: float
    "Operating Point Reactive Power/Voltage: Voltage"
    usp_max: float
    "Voltage Setpoint Limits: Max. Voltage Setpoint"
    usp_min: float
    "Voltage Setpoint Limits: Min. Voltage Setpoint"
    vecBreakpointsP: list
    "Piecewise linearisation for LP: Power"
    vecCostRedispatchDown: list
    "Costs"
    vecCostRedispatchUp: list
    "Costs"
    vecDiscreteCtrlPvals: list
    "Restriction to discrete active power values: Valid active power values"
    vecPowerRedispatchDown: list
    "Redispatch"
    vecPowerRedispatchUp: list
    "Redispatch"
    vecStartUpCosts: list
    "Start-up costs: Start-up costs"
    vecStartUpTimes: list
    "Start-up costs: Down-time"
    x0: float
    "Zero sequence: Reactance, x0"
    x0hmc: float
    "Norton Equivalent: Reactance, x0h"
    x0iec: float
    "Zero sequence short-circuit impedance: Reactance, x0"
    x1hmc: float
    "Norton Equivalent: Reactance, x1h"
    x2: float
    "Negative sequence: Reactance x2"
    x2hmc: float
    "Norton Equivalent: Reactance, x2h"
    x2iec: float
    "Negative sequence short-circuit impedance: Reactance, x2"
    x2shc: float
    "Negative sequence short-circuit impedance: Reactance, x2"
    xtor: float
    "Max. Fault Contribution: X'' to R ratio"

    def AttributeType(*args): ...

    def CalcEfficiency(*args): ...

    def Derate(*args): ...

    def Disconnect(*args): ...

    def GetAvailableGenPower(*args): ...

    def GetGroundingImpedance(*args): ...

    def HasReferences(*args): ...

    def IsConnected(*args): ...

    def Reconnect(*args): ...

    def ResetDerating(*args): ...

    def __getattr__(*args): ...


class ElmRelay(PFGeneral):
    actset: int
    "Active Settings Group"
    application: int
    "Application:Main Protection:Backup Protection"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    cat_curr: int
    "Overcurrent"
    cat_diff: int
    "Differential"
    cat_dir: int
    "Directional"
    cat_dist: int
    "Distance"
    cat_freq: int
    "Frequency"
    cat_volt: int
    "Voltage"
    cbranch: object
    "Location: Branch"
    cbranchid: int
    "Cubicle index of connected branch"
    ccat_curr: int
    "Considered for protection coordination: Overcurrent"
    ccat_diff: int
    "Considered for protection coordination: Differential"
    ccat_dir: int
    "Considered for protection coordination: Directional"
    ccat_dist: int
    "Considered for protection coordination: Distance"
    ccat_freq: int
    "Considered for protection coordination: Frequency"
    ccat_volt: int
    "Considered for protection coordination: Voltage"
    ccategory: str
    "Main function:"
    cctprim: float
    "Current/Voltage Transformer Settings: CT Primary"
    cctsec: float
    "Current/Voltage Transformer Settings: CT Secondary"
    ccub: object
    "Cubicle"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cn_bus: object
    "Location: Busbar"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    contents: list
    "Contents"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpCt: object
    "Current Transformer"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpShc: object
    "Fault current limits: Short-circuit command"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpVt: object
    "Voltage Transformer"
    cpZone: object
    "Zone"
    ctprim: float
    "CT Primary"
    ctsec: float
    "CT Secondary"
    cvtprim: float
    "Current/Voltage Transformer Settings: VT Primary"
    cvtsec: float
    "Current/Voltage Transformer Settings: VT Secondary"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    dev_no: int
    "Device Number"
    doc_id: object
    "Additional Data"
    efaultmaxi: float
    "Fault current limits: Max. earth fault current"
    efaultmini: float
    "Fault current limits: Min. earth fault current"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iComDate: int
    "Commissioning Date"
    iSchemeStatus: int
    "Scheme Status"
    isSubRelay: int
    "Sub-relay"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pReference: object
    "Location: Reference"
    pdiselm: list
    "Net Elements"
    pelm: list
    "Net Elements"
    phfaultmaxi: float
    "Fault current limits: Max. phase fault current"
    phfaultmini: float
    "Fault current limits: Min. phase fault current"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    sw_settingsGroups: list
    "Active settings groups in StationWare"
    td_bR: float
    "Resistance"
    td_bRC: float
    "Measured Resistance"
    td_bX: float
    "Reactance"
    td_bXC: float
    "Measured Reactance"
    td_bZ: float
    "Impedance"
    td_bZC: float
    "Measured Impedance"
    td_blim: int
    "End of Path"
    td_bobj: object
    "Step"
    td_bphi: float
    "Angle"
    td_bphiC: float
    "Measured Angle"
    td_bpos: float
    "Position"
    td_btpbk: float
    "Tripping + Breaker Time (Step)"
    td_btrip: float
    "Tripping Time (Step)"
    td_cnt: int
    "Number of tripped Steps"
    td_fR: float
    "Resistance"
    td_fRC: float
    "Measured Resistance"
    td_fX: float
    "Reactance"
    td_fXC: float
    "Measured Reactance"
    td_fZ: float
    "Impedance"
    td_fZC: float
    "Measured Impedance"
    td_flim: int
    "End of Path"
    td_fobj: object
    "Step"
    td_fphi: float
    "Angle"
    td_fphiC: float
    "Measured Angle"
    td_fpos: float
    "Position"
    td_ftpbk: float
    "Tripping + Breaker Time (Step)"
    td_ftrip: float
    "Tripping Time (Step)"
    tid_: int
    "TimeID"
    typ_id: object
    "Relay Type"
    vtprim: float
    "VT Primary"
    vtsec: float
    "VT Secondary"
    zratio: float
    "Impedance Ratio"

    def AttributeType(*args): ...

    def CalculateMaxFaultCurrents(*args): ...

    def CheckRanges(*args): ...

    def GetCalcRX(*args): ...

    def GetMaxFdetectCalcI(*args): ...

    def GetSlot(*args): ...

    def HasReferences(*args): ...

    def IsStarted(*args): ...

    def SetImpedance(*args): ...

    def SetMaxI(*args): ...

    def SetMaxIearth(*args): ...

    def SetMinI(*args): ...

    def SetMinIearth(*args): ...

    def SetOutOfService(*args): ...

    def SetTime(*args): ...

    def SlotUpdate(*args): ...

    def __getattr__(*args): ...

    def slotupd(*args): ...


class ElmRes(PFGeneral):
    FileType: str
    "File type"
    TpTetris: int
    "Faulted phases:"
    avgStep: float
    "Info: Average step size:"
    cActivePower: float
    "Active Power"
    cAllRegNum: int
    "Info: Number of transactions:"
    cAutoBMW: int
    "Automatically created of Boundary"
    cContingency: object
    "Contingency"
    cFFTstep: str
    "Info: Step size:"
    cFilename: str
    "File name"
    cFlowNum: int
    "Info: Number of flowgates:"
    cFnom: float
    "Nominal Frequency"
    cHeaderSize: int
    "Header size"
    cLdfMethod: str
    "Load Flow method:"
    cOpScenNum: int
    "Info: Number of operation scenarios:"
    cOrigCurve: object
    "Analysed curve"
    cPosStep: str
    "Info: Average position step size:"
    cStudyBus: object
    "Study Bus"
    cab_meth: int
    "Method:&0&International Standard:&1&Cable Reinforcement:&2&Ampacity Calculation"
    calTp: int
    "Default for"
    calTpCoord: int
    "Usage:Coordination:Audit:Distance Settings:Topology:Overcurrent Settings:Load Flow:Short-Circuit"
    calTpFlowDecomp: int
    "Method:Decomposition:Power exchange analysis"
    calTpHrmMethod: int
    "Load Flow method"
    calTpSto: int
    "Method:Monte Carlo:Quasi-Monte Carlo"
    calTpStoCom: int
    "Command:Load Flow:Optimal Power Flow:Dynamic Simulation"
    calTpStoLdfMethod: int
    "Load Flow method"
    calTpStoOpfMethod: int
    "Optimisation method"
    calTpStoSimMethod: int
    "Simulation type"
    calTpSub: int
    "Method:&0&AC Load Flow:&1&DC Load Flow"
    calTpSwp: int
    "Method:AC Load Flow, balanced:AC Load Flow, unbalanced:DC Load Flow (linear)"
    calTpTop: int
    "Usage:&0&Before Optimisation:&1&After Optimisation"
    cases: list
    "Cases"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cnttime: int
    "Info: Study time"
    cnumCase: int
    "Info: Number of cases:"
    cnumEigen: int
    "Info: Number of eigenvalues:"
    cnumFFT: int
    "Info: Number of harmonic orders:"
    cnumFrq: int
    "Info: Number of frequencies:"
    cnumHmOd: int
    "Info: Number of Harmonic Orders:"
    cnumcont: int
    "Info: Number of contingencies:"
    cnumfiles: int
    "Info: Number of result files"
    cnumrow: int
    "Info: Number of rows:"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    csteps: str
    "Info: Average step size:"
    ctimeph: int
    "Info: Number of time phases:"
    ctotrow: int
    "Info: Total number of rows:"
    ctricnt: int
    "Info: Points of time:"
    cvars: int
    "Info: Number of variables:"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    df_meth: int
    "Method:&0&PTDF (ComPtdf):&1&Sensitivities:&2&LODF:&3&Sensitivities (Cnt.)"
    f_name: str
    "Database Id"
    f_pcl: str
    "Protocol file Id"
    fileSize: int
    "File size:"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    header: list
    "Headlines"
    host_meth: int
    "Method:&0&DER Capacity:&1&Spare Load Capacity"
    iSchemeStatus: int
    "Scheme Status"
    keyDouble: float
    "Linked double value"
    keyDouble1: float
    "Linked double value 1"
    keyType: int
    "Type of the key for sub-result file"
    loc_name: str
    "Name"
    monitorFreq: float
    "Frequency"
    monitorStep: float
    "Sample period"
    oid_: int
    "ObjectID"
    pObjs: list
    "Used objects"
    pResElm: object
    "Fault location"
    pResElm2: object
    "Linked element 2"
    pXObjs: list
    "Extra objects"
    pid_: int
    "ProjectID"
    powpark_meth: int
    "Method:&0&Basic Analysis:&1&Time-series Analysis:&2&Probabilistic Analysis"
    powpark_sub: int
    "Sub-result:&0&Losses Analysis:&1&Losses Curves:&2&Samples/Time Points:&3&Energy Yield"
    rew: int
    "Rewrite every"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    trg_pmax: float
    "Trigger-Times: Max."
    trg_post: float
    "Trigger-Times: Post-"
    trg_pre: float
    "Trigger-Times: Pre-"
    unit: str
    "Info: Unit"
    upd: int
    "Create new file every"
    usedfor: str
    "Saving time"

    def AddVariable(*args): ...

    def AddVars(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def Close(*args): ...

    def ExecuteLoadingCommand(*args): ...

    def FindColumn(*args): ...

    def FindMaxInColumn(*args): ...

    def FindMaxOfVariableInRow(*args): ...

    def FindMinInColumn(*args): ...

    def FindMinOfVariableInRow(*args): ...

    def FinishWriting(*args): ...

    def Flush(*args): ...

    def GetColumnValues(*args): ...

    def GetDescription(*args): ...

    def GetFirstValidObject(*args): ...

    def GetFirstValidObjectVariable(*args): ...

    def GetFirstValidVariable(*args): ...

    def GetNextValidObject(*args): ...

    def GetNextValidObjectVariable(*args): ...

    def GetNextValidVariable(*args): ...

    def GetNumberOfColumns(*args): ...

    def GetNumberOfRows(*args): ...

    def GetObj(*args): ...

    def GetObject(*args): ...

    def GetObjectValue(*args): ...

    def GetRelCase(*args): ...

    def GetSubElmRes(*args): ...

    def GetUnit(*args): ...

    def GetValue(*args): ...

    def GetVariable(*args): ...

    def HasReferences(*args): ...

    def Init(*args): ...

    def InitialiseWriting(*args): ...

    def Load(*args): ...

    def Release(*args): ...

    def SetAsDefault(*args): ...

    def SetObj(*args): ...

    def SetSubElmResKey(*args): ...

    def SortAccordingToColumn(*args): ...

    def Write(*args): ...

    def WriteDraw(*args): ...

    def __getattr__(*args): ...


class ElmShnt(PFGeneral):
    B0toB1: float
    "Zero sequence admittance: B0/B1 ratio"
    Bg: float
    "Terminal to Ground Capacitance (per Step): Susceptance to Ground"
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures Double Earth Fault: Repair duration"
    FOD: float
    "Failures: Forced Outage Duration"
    FOE: float
    "Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures: Forced Outage Rate"
    G0toG1: float
    "Zero sequence admittance: G0/G1 ratio"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Irze: list
    "Rated Current of Grounding"
    Kctrl: float
    "Controller Sensitivity dq/dv"
    Lwidth: float
    "Hysteresis: Loop width"
    PsiresA: float
    "Residual flux: Residual flux, ph. A"
    PsiresB: float
    "Residual flux: Residual flux, ph. B"
    PsiresC: float
    "Residual flux: Residual flux, ph. C"
    Qact: float
    "Controller: Actual Reactive Power"
    Qmax: float
    "Controller: Max. Rated Reactive Power"
    R0toR1: float
    "Zero sequence impedance: R0/R1 ratio"
    Re: float
    "Internal Grounding Impedance: Resistance, Re"
    Tctrl: float
    "Controller Time Constant"
    X0toX1: float
    "Zero sequence impedance: X0/X1 ratio"
    Xe: float
    "Internal Grounding Impedance: Reactance, Xe"
    aFrolich: float
    "Frolich equation coefficient a"
    acost: float
    "Annual Cost"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    availFactor: float
    "Availability Factor"
    bFrolich: float
    "Frolich equation coefficient b"
    bcap: float
    "Layout Parameter (per Step): Susceptance"
    bus1: object
    "Terminal"
    bus1n: object
    "Neutral Conductor: Neutral"
    c1: float
    "Layout Parameter (per Step): Capacitance C1"
    c2: float
    "Layout Parameter (per Step): Capacitance C2"
    cConBus: object
    "Connected terminal"
    cDisplayName: str
    "Display Name"
    cFrolich: float
    "Frolich equation coefficient c"
    cNamLev: str
    "Name of Load Level"
    cNumLev: int
    "Number of Load Levels"
    cPhInfo: str
    "Phases:"
    cPsiresC: float
    "Residual flux: Residual flux, ph. C"
    cTapLev: int
    "Tap Position for Load Level"
    cUserDefIndex: int
    "User defined Index"
    c_pctrl: object
    "Shunt Controller"
    capsa: str
    "Vector Group:Y:D:YN"
    ccap: float
    "Layout Parameter (per Step): Capacitance"
    cgnd: int
    "Internal Grounding Impedance: Star Point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cknee: float
    "Knee Current"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpCtrlNode: object
    "Target Node"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    ctech: int
    "Technology"
    cucap: float
    "Design Parameter (per Step): Rated Current, C"
    curea: float
    "Design Parameter (per Step): Rated Current, L"
    cutot: float
    "Design Parameter (per Step): Rated Current, L-C"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fcharC: object
    "Frequency Dependence of Capacitor: C(f)"
    fcharC0: object
    "Frequency Dependence of Capacitor: C0(f)"
    fcharC1: object
    "Frequency Dependence of Capacitor: C1(f)"
    fcharC2: object
    "Frequency Dependence of Capacitor: C2(f)"
    fcharL: object
    "Frequency Dependence of R-L Element: L(f)"
    fcharL0: object
    "Frequency Dependence of R-L Element: L0(f)"
    fcharR: object
    "Frequency Dependence of R-L Element: Rs(f)"
    fcharR0: object
    "Frequency Dependence of R-L Element: Rs0(f)"
    fcharRp: object
    "Frequency Dependence of Parallel Resistance: Rp(f)"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    fres: float
    "Design Parameter (per Step): Resonant Frequency"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    gparac: float
    "Layout Parameter (per Step): Parallel Conductance"
    grea: float
    "Design Parameter (per Step): Quality Factor (at fn)"
    greaf0: float
    "Design Parameter (per Step): Quality Factor (at fr)"
    harmPgeC: float
    "Frequency Dependence of Capacitor: Capacitance"
    harmPgeC0: float
    "Frequency Dependence of Capacitor: Zero-sequence Cap."
    harmPgeC1: float
    "Frequency Dependence of Capacitor: Capacitance 1"
    harmPgeC2: float
    "Frequency Dependence of Capacitor: Capacitance 2"
    harmPgeL: float
    "Frequency Dependence of R-L Element: Inductance"
    harmPgeL0: float
    "Frequency Dependence of R-L Element: Zero-sequence Ind."
    harmPgeR: float
    "Frequency Dependence of R-L Element: Resistance"
    harmPgeR0: float
    "Frequency Dependence of R-L Element: Zero-sequence Res."
    harmPgeRp: float
    "Frequency Dependence of Parallel Resistance: Parallel Resistance"
    iComDate: int
    "Commissioning Date"
    iFinalSlope: int
    "Set final slope (peak values)"
    iFit: int
    "Data fitting:Piecewise linear:Frolich:Modified Frolich"
    iHyster: int
    "Hysteresis: Model:None:History Independent"
    iIntTapCtrl: int
    "Use Integrated Tap Controller"
    iInterPol: int
    "Interpolation:spline:piecewise linear"
    iLimb: int
    "Core:&3&3 Limb:&5&5 Limb"
    iQorient: int
    "Orientation:+Q:-Q"
    iResFlux: int
    "Residual flux"
    iSchemeStatus: int
    "Scheme Status"
    iTaps: int
    "According to Measurement Report"
    iZeConfig: int
    "Internal Grounding Impedance: Configuration:Per step:Common"
    i_cont: int
    "Tap Changer:discrete:continuous"
    i_opt: int
    "Controls: Use Controller for OPF optimisation"
    i_optCont: int
    "Controls: Control Mode:discrete:continuous"
    i_rem: int
    "Remote Control"
    ignd: int
    "Star Point:grounded:compensated:isolated"
    iintgnd: int
    "Neutral Conductor: N-Connection:None:At terminal (ABC-N):Separate terminal"
    ilcph: int
    "Phase:a:b:c:a-b:b-c:c-a:Pos.Seq."
    imldc: str
    "Control Mode"
    iperfect: int
    "Failures: Ideal component"
    isCtrlShnt: int
    "Tap Control for Unit Commitment"
    isCtrlShntCont: int
    "Tap Control for Unit Commitment: Control Mode:discrete:continuous"
    iswitch: int
    "Switchable"
    itrmt: int
    "Type"
    ksat: int
    "Saturation Exponent"
    loc_name: str
    "Name"
    mTaps: list
    "Tap: Measurement Report"
    manuf: str
    "Manufacturer"
    mode_inp: str
    "Input Mode"
    mseFrolich: float
    "Frolich equation, mean squared error"
    ncapa: int
    "Controller: Act.No. of Step"
    ncapx: int
    "Controller: Max. No. of Steps"
    nres: float
    "Design Parameter (per Step): Tuning Order"
    nshph: int
    "Phases:1:2:3"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pStoch: object
    "Failures: Element model"
    p_cub: object
    "Q Controlled at"
    p_rem: object
    "Controlled Node"
    penaltyCosts: float
    "Controls: Penalty costs per tap deviation"
    pf_recap_mn: int
    "Power Factor:ind.:cap."
    pf_recap_mx: int
    "Power Factor:ind.:cap."
    pfsetp_mn: float
    "Lower Power Factor Limit"
    pfsetp_mx: float
    "Upper Power Factor Limit"
    pgrad: float
    "Design Parameter (per Step): Degree"
    phtech: int
    "Technology"
    pid_: int
    "ProjectID"
    psi0: float
    "Knee Flux"
    qcapn: float
    "Design Parameter (per Step): Rated Reactive Power, C"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qrean: float
    "Design Parameter (per Step): Rated Reactive Power, L"
    qsetp_mn: float
    "Lower Reactive Power Limit"
    qsetp_mx: float
    "Upper Reactive Power Limit"
    qtotn: float
    "Design Parameter (per Step): Rated Reactive Power, L-C"
    rlrea: float
    "Layout Parameter (per Step): Inductance"
    root_id: object
    "Original Location"
    rpara: float
    "Layout Parameter (per Step): Parallel Resistance"
    rrea: float
    "Layout Parameter (per Step): Resistance"
    sOpComment: list
    "Operator Comment"
    satcue: list
    "Current (RMS)"
    satcur: list
    "Current (peak)"
    satflux: list
    "Flux (peak)"
    satvol: list
    "Voltage (RMS)"
    sernum: str
    "Serial Number"
    shtype: int
    "Shunt Type"
    smoothfac: float
    "Smoothing Factor"
    systp: int
    "System Type:AC:DC:AC/BI"
    tandc: float
    "Design Parameter (per Step): Loss Factor, tan(delta)"
    tid_: int
    "TimeID"
    uset_mode: int
    "Setpoint:local:bus target voltage"
    usetp_mn: float
    "Lower Voltage Limit"
    usetp_mx: float
    "Upper Voltage Limit"
    ushnm: float
    "Rated Voltage"
    xmair: float
    "Saturated Reactance"
    xrea: float
    "Layout Parameter (per Step): Reactance"
    xreapu: float
    "Linear Reactance"
    xsatFrolich: float
    "Frolich equation saturated reactance (p.u.)"

    def AttributeType(*args): ...

    def GetGroundingImpedance(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmStactrl(PFGeneral):
    Qdroop: float
    "Enable Droop: Droop"
    Qdroopoe: float
    "Q(V)-Characteristic: Droop (overexcited)"
    Qdroopue: float
    "Q(V)-Characteristic: Droop (underexcited)"
    Qmax: float
    "Q(V)-Characteristic: Qmax"
    Qmin: float
    "Q(V)-Characteristic: Qmin"
    Srated: float
    "Enable Droop: Rated Reactive Power"
    Tctrl: float
    "Reactive Power Distribution: Controller Time Constant"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    cconn: int
    "Connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    commissionDate: str
    "Commissioning Date"
    consQdisp: int
    "Reactive Power Distribution: Consider reactive power dispatch"
    constr: int
    "Year of Construction"
    cosphi_char: int
    "PF-Control:Const. cosphi:cosphi(P)-Characteristic:cosphi(V)-Characteristic"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpCtrlNode: object
    "Controlled Node: Target Node"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cvgen: list
    "Voltage Setpoint"
    cvgenmax: list
    "Max. Voltage"
    cvgenmin: list
    "Min. Voltage"
    cvqq: list
    "Reactive Power Percentage"
    dReserve: float
    "Minimum Control Reserve"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    ddroop: float
    "Enable Droop: Droop"
    ddroopoe: float
    "Q(V)-Characteristic: Droop (overexcited)"
    ddroopue: float
    "Q(V)-Characteristic: Droop (underexcited)"
    deltaV: float
    "Enable Droop: delta(V)"
    deltaVoe: float
    "Q(V)-Characteristic: delta(V) (overexcited)"
    deltaVue: float
    "Q(V)-Characteristic: delta(V) (underexcited)"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iComDate: int
    "Commissioning Date"
    iOPFCqsummax: int
    "Max. Total Reactive Power Limit"
    iOPFCqsummin: int
    "Min. Total Reactive Power Limit"
    iQorient: int
    "Orientation:+Q:-Q"
    iSchemeStatus: int
    "Scheme Status"
    iTrfCtrl: int
    "Reactive Power Distribution: Step-up Transformer Control:None:HV-Side:LV-Side"
    i_ctrl: int
    "Control Mode"
    i_droop: int
    "Enable Droop"
    i_phase: int
    "Phase:Pos.Seq.:Average:a:b:c:a-b:b-c:c-a"
    i_uest: int
    "Estimate Voltage Setpoint"
    i_uopt: int
    "Optimise Voltage Setpoint"
    imode: int
    "Reactive Power Distribution"
    iopt_tdr: int
    "Q(V)-Characteristic: Different droop values"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pQPcurve: object
    "Q(P)-Characteristic: Q(P)-Curve"
    pQmeas: object
    "Enable Droop: Q measured at"
    p_cub: object
    "Control Q at"
    p_over: float
    "cosphi(P)-Characteristic Overexcited: Active Power"
    p_under: float
    "cosphi(P)-Characteristic Underexcited: Active Power"
    pf_over: float
    "cosphi(P)-Characteristic Overexcited: Min. Power Factor"
    pf_recap: int
    "Power Factor:ind.:cap."
    pf_under: float
    "cosphi(P)-Characteristic Underexcited: Min. Power Factor"
    pfsetp: float
    "Power Factor"
    pid_: int
    "ProjectID"
    psym: list
    "Machines"
    qsetp: float
    "Q Setpoint"
    qsummax: float
    "Max. Total Reactive Power Limit"
    qsummin: float
    "Min. Total Reactive Power Limit"
    qu_char: int
    "Q-Control:Const. Q:Q(V)-Characteristic:Q(P)-Characteristic"
    refbar: object
    "Q(V)-Characteristic: Reference Node"
    rembar: object
    "Controlled Node: Controlled Node"
    root_id: object
    "Original Location"
    sOpComment: list
    "Operator Comment"
    selAutoUn: float
    "Controlled Node: Busbar Search Criteria >="
    selBus: int
    "Controlled Node"
    sernum: str
    "Serial Number"
    tansetp: float
    "tan(phi)"
    tid_: int
    "TimeID"
    u_over: float
    "cosphi(V)-Characteristic Overexcited: Voltage"
    u_under: float
    "cosphi(V)-Characteristic Underexcited: Voltage"
    udeadblow: float
    "Q(V)-Characteristic Voltage Dead Band: Lower Voltage Limit"
    udeadbup: float
    "Q(V)-Characteristic Voltage Dead Band: Upper Voltage Limit"
    uset_mode: int
    "Controlled Node: Setpoint:Station Controller:bus target voltage"
    usetp: float
    "Controlled Node: Voltage Setpoint"
    vqq: list
    "Reactive Power Percentage"

    def AttributeType(*args): ...

    def GetControlledHVNode(*args): ...

    def GetControlledLVNode(*args): ...

    def GetStepupTransformer(*args): ...

    def HasReferences(*args): ...

    def Info(*args): ...

    def __getattr__(*args): ...


class ElmSubstat(PFGeneral):
    AccessTime: float
    "Access Times of Switches: Access Time"
    BoxDepth: float
    "Dimensions of enclosure: Depth"
    BoxHeight: float
    "Dimensions of enclosure: Height"
    BoxWidth: float
    "Dimensions of enclosure: Width"
    CondGap: float
    "Conductor Gap"
    DcBoxType: int
    "Enclosure type:Panelboard:LV switchgear:MV switchgear"
    Electrodes: str
    "Electrode configuration"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Hmax: float
    "Hmax"
    LocAccTime: float
    "Access Times of Switches: Local Access Time"
    Unom: float
    "Nominal Voltage"
    WorkDist: float
    "Working Distance"
    Xfactor: float
    "Distance Factor"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUnom: float
    "Nominal Voltage"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cimRdfId: list
    "RDF ID"
    constr: int
    "Year of Construction"
    contents: list
    "Contents"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBoxed: int
    "Enclosure:Open air:Boxed"
    iSchemeStatus: int
    "Scheme Status"
    icolor: int
    "Colour"
    isRaActive: int
    "Running arrangement active"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pArea: object
    "Default Area"
    pDiagram: object
    "Diagram"
    pOperator: object
    "Default Operator"
    pOwner: object
    "Default Owner"
    pRA: object
    "Running Arrangement: Running Arrangement"
    pSwSc: object
    "Switching Rules: Active Rules"
    pZone: object
    "Default Zone"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sShort: str
    "Short Name"
    sType: str
    "Type"
    stoLoad: object
    "Load Distribution Curve: Distribution Curve"
    tid_: int
    "TimeID"

    def ApplyAndResetRA(*args): ...

    def AttributeType(*args): ...

    def GetSplit(*args): ...

    def GetSplitCal(*args): ...

    def GetSplitIndex(*args): ...

    def GetSuppliedElements(*args): ...

    def HasReferences(*args): ...

    def OverwriteRA(*args): ...

    def ResetRA(*args): ...

    def SaveAsRA(*args): ...

    def SaveAsSwSc(*args): ...

    def SetRA(*args): ...

    def __getattr__(*args): ...


class ElmSvs(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Inom: float
    "Nominal Current"
    Irated: float
    "Harmonic Current Injections: Rated Current"
    Qdroop: float
    "Enable droop: Droop"
    Qfixcap: float
    "MSC: Q per capacitor (<0)"
    Qmax_a: float
    "Qmax(C)"
    Qmin_a: float
    "Qmin(L)"
    QtargetBase: int
    "Base:Reactive power limits:Rated apparent power"
    QtargetRPR: float
    "Q target value"
    R0: float
    "Resistance, R0"
    Re: float
    "Resistance, Re"
    Srated: float
    "Enable droop: Rated reactive power"
    X0: float
    "Reactance, X0"
    Xe: float
    "Reactance, Xe"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    availFactor: float
    "Availability Factor"
    bus1: object
    "Terminal"
    cDisplayName: str
    "Display Name"
    cTypHmc: str
    "Harmonic Current Injections: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    c_pmod: object
    "Model"
    c_pstac: object
    "External station controller"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    copfQmax1: float
    "Reactive power limits: Max. react. power limit at 0.9 p.u."
    copfQmax2: float
    "Reactive power limits: Max. react. power limit at 1 p.u."
    copfQmax3: float
    "Reactive power limits: Max. react. power limit at 1.1 p.u."
    copfQmin1: float
    "Reactive power limits: Min. react. power limit at 0.9 p.u."
    copfQmin2: float
    "Reactive power limits: Min. react. power limit at 1 p.u."
    copfQmin3: float
    "Reactive power limits: Min. react. power limit at 1.1 p.u."
    copfVolt1: float
    "Reactive power limits: Voltage: 0.9 p.u."
    copfVolt2: float
    "Reactive power limits: Voltage: 1 p.u."
    copfVolt3: float
    "Reactive power limits: Voltage: 1.1 p.u."
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpCtrlNode: object
    "Target node"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    ddroop: float
    "Enable droop: Droop"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iOPFCQmax: int
    "Reactive power limits: Max. react. power limit"
    iOPFCQmin: int
    "Reactive power limits: Min. react. power limit"
    iSchemeStatus: int
    "Scheme Status"
    i_ctrl: int
    "Control mode"
    i_det: int
    "TCR model"
    i_droop: int
    "Enable droop"
    i_int: int
    "Ideal SVS"
    i_qini: int
    "State Estimation: Estimate reactive power"
    i_rem: int
    "Remote control"
    i_sctrl: int
    "Balanced/Unbalanced control"
    i_udeadb: int
    "Voltage dead band"
    iconn: int
    "Connection mode of capacitors:Y:D:YN"
    ictsv: int
    "Reactive power as control"
    icurref: int
    "Harmonic Current Injections: Harmonic currents referred to"
    isRPR: int
    "Optimisation of reactive power reserve"
    ivcop: int
    "Phase:a-b:b-c:c-a:Average:Pos.seq."
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    maxorder: int
    "Maximum harmonic order"
    nfixcap: int
    "MSC: Number of capacitors"
    nncap: int
    "Actual values: Act. number of capacitors"
    nxcap: int
    "TSC: Max. number of capacitors"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pQmeas: object
    "Enable droop: Q measured at"
    pSubModel: object
    "Submodel"
    p_cub: object
    "Control Q at"
    p_rem: object
    "Controlled node"
    pcu: float
    "Maximum copper losses"
    phmc: object
    "Harmonic Current Injections: Harmonic currents (TCR)"
    pid_: int
    "ProjectID"
    q0: float
    "Reactive power"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qmax: float
    "TCR: Q of reactance (>0)"
    qmin: float
    "TSC: Q per capacitor (<0)"
    qsetp: float
    "Q Setpoint"
    root_id: object
    "Original Location"
    sOpComment: list
    "Operator comment"
    sernum: str
    "Serial Number"
    tcrmax: float
    "TCR: Max. limit"
    tcrqact: float
    "Actual values: Act. value of TCR"
    tid_: int
    "TimeID"
    udeadblow: float
    "Voltage dead band: Lower voltage limit"
    udeadbup: float
    "Voltage dead band: Upper voltage limit"
    uset_mode: int
    "Setpoint:local:bus target voltage"
    usetp: float
    "Voltage setpoint"

    def AttributeType(*args): ...

    def GetStepupTransformer(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmSym(PFGeneral):
    EDS: float
    "Stochastic Model for Generation: Expectancy of derated states"
    FAY: float
    "Stochastic Model for Generation: Full Availability Expectancy"
    FOE: float
    "Stochastic Model for Generation: Forced Outage Expectancy"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Inom: float
    "Nominal Current"
    Irze: list
    "Rated Current of Grounding"
    Jme: float
    "Mechanical load: Moment of inertia"
    Kpf: float
    "Dispatch: Prim. Frequency Bias"
    P_max: float
    "Active Power: Rating: Max."
    P_min: float
    "Min."
    Pctrl: int
    "Active power control: Active power steps:fixed:continuous:1:2:3:4:5:6:7:8:9:10"
    PmaxInv: float
    "Separate consumption mode: Max."
    PmaxInvPU: float
    "Separate consumption mode: Max."
    Pmax_a: float
    "Pmax(act.)"
    Pmax_uc: float
    "Active Power Operational Limits: Max."
    Pmax_ucPU: float
    "Active Power Operational Limits: Max."
    PminInv: float
    "Separate consumption mode: Min."
    PminInvPU: float
    "Separate consumption mode: Min."
    Pmin_a: float
    "Pmin(act.)"
    Pmin_uc: float
    "Active Power Operational Limits: Min."
    Pmin_ucPU: float
    "Active Power Operational Limits: Min."
    Pngrel: float
    "Stochastic Model for Generation: Based on rated active power (Pr)"
    Pnom: float
    "Active Power Operational Limits: Pr(rated)"
    Qmax_a: float
    "Qmax(act.)"
    Qmin_a: float
    "Qmin(act.)"
    QtargetBase: int
    "Optimisation of reactive power reserve: Base:Reactive power limits:Rated apparent power"
    QtargetRPR: float
    "Optimisation of reactive power reserve: Q target value"
    Tstart: float
    "Time-overcurrent plot: Starting Time"
    aCategory: str
    "Plant Category"
    aSubCategory: str
    "Subcategory"
    allowConsumMode: int
    "Separate consumption mode"
    allowGenMode: int
    "Separate generation mode"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    av_mode: str
    "Local Controller"
    availFactor: float
    "Availability Factor"
    avgCosts: float
    "Average costs"
    avgCostsUc: float
    "Piecewise linearisation for LP: Average costs"
    beta: float
    "Wind Model Weibull Distribution for Wind Speed: Beta"
    bus1: object
    "Terminal"
    bus1n: object
    "Neutral Conductor: Neutral"
    bustp: str
    "Corresponding Bus Type:"
    cCategory: str
    "Plant Category"
    cDisplayName: str
    "Display Name"
    cIsDiscreteCtrlP: int
    "Restriction to discrete active power values"
    cIsMustRunUC: int
    "Additional constraints for controls: Must run"
    cIsPcurrAllowed: int
    "Allow current active power value"
    cQ_max: float
    "Reactive Power Operational Limits: Maximum"
    cQ_min: float
    "Reactive Power Operational Limits: Minimum"
    cStorage: object
    "Generator usage: Storage model"
    cSubCategory: str
    "Subcategory"
    cTypHmc: str
    "Harmonic Load Flow: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    cVecDiscreteCtrlPvals: list
    "Valid active power values"
    c_pCtrlHV: object
    "Controlled HV-busbar"
    c_pmdm: object
    "Mechanical load: Mdm"
    c_pmod: object
    "Model"
    c_psecc: object
    "External Secondary Controller"
    c_pstac: object
    "External Station Controller"
    cap_P: list
    "Act.Power"
    cap_Qmn: list
    "Min."
    cap_Qmx: list
    "Max."
    ccost: list
    "Costs"
    cfixedCosts: float
    "Consumption mode: Fixed costs"
    cgnd: int
    "Internal Grounding Impedance: Star Point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cnwsamples: int
    "Wind Model Time Series Characteristics: Annual Samples: Number of Samples"
    coldStartTime: float
    "Start-up costs: Cold-start time"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    consumCosts: float
    "Consumption mode: Consumption costs"
    cosgini: float
    "Dispatch: Power Factor"
    cosgini_a: float
    "Actual Dispatch: Power Factor (act.)"
    cosimModel: int
    "Used for Co-simulation"
    costColdStart: float
    "Start-up costs: Cold-start costs"
    costCurtailment: float
    "Costs for curtailment"
    costRedispatchDown: float
    "Additional redispatch costs: Downward active power redispatch costs"
    costRedispatchP: float
    "Redispatch costs for active power change"
    costRedispatchQ: float
    "Redispatch costs for reactive power change"
    costRedispatchUp: float
    "Additional redispatch costs: Upward active power redispatch costs"
    costShutDown: float
    "Shut-down costs"
    cost_up: float
    "Start-up costs: Warm-start costs"
    costp: float
    "Costs per MW"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpower: list
    "Power"
    cq_max: float
    "Reactive Power Operational Limits: Max."
    cq_min: float
    "Reactive Power Operational Limits: Min."
    ctag: float
    "Mechanical load: Acceleration time const. from type"
    ctagtot: float
    "Mechanical load: Total acceleration time const."
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    ddroop: float
    "Voltage Droop: Droop"
    desc: list
    "Description"
    discMethCostOp: int
    "Piecewise linearisation for LP"
    dispatch: int
    "Generator Dispatch"
    doc_id: object
    "Additional Data"
    dphi: float
    "Change of phi effect on stability (RMS - Standard model) (for testing only)"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    drawInrush: int
    "Time-overcurrent plot: Draw Inrush Current"
    drawStall: int
    "Time-overcurrent plot: Draw Thermal Overload"
    dsecres: float
    "Reserve"
    efdBaseRatio: float
    "Excitation system: Efd base ratio"
    efficiencyCurveConsum: object
    "Efficiency: Efficiency curve (consumption)"
    efficiencyCurveGen: object
    "Efficiency: Efficiency curve (generation)"
    efficiencyLPconsum: float
    "Efficiency: Used efficiency (consumption)"
    efficiencyLPgen: float
    "Efficiency: Used efficiency (generation)"
    fixed: int
    "Must run"
    fixedCosts: float
    "Fixed costs"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    genShiftKey: float
    "Generation shift key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    gratio: float
    "Mechanical load: Gear ratio"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iHmcType: int
    "Harmonic Load Flow: Harmonic Model:Thevenin Equivalent:Ideal Voltage Source:Impedance"
    iInterPol: int
    "Approximation:Spline:Piecewise linear:Polynomial:Hermite"
    iOPFCPmax: int
    "Active Power Operational Limits: Max."
    iOPFCPmin: int
    "Active Power Operational Limits: Min."
    iOPFCQmax: int
    "Reactive Power Operational Limits: Max."
    iOPFCQmin: int
    "Reactive Power Operational Limits: Min."
    iSchemeStatus: int
    "Scheme Status"
    iWindGen: int
    "Wind Generator"
    i_avr: int
    "Use integrated AVR for motor starting"
    i_cap: int
    "User defined Capability Curve"
    i_mot: int
    "Generator/Motor"
    i_prty: int
    "Active power control: Priority"
    i_spin: int
    "Spinning if circuit-breaker is open"
    ictpg: int
    "Controls: Active Power"
    ictqg: int
    "Controls: Reactive Power"
    iestp: int
    "State Estimation: Estimate Active Power"
    iestq: int
    "State Estimation: Estimate Reactive Power"
    ifdBaseType: str
    "Excitation system: Excitation base mode"
    ifdBaseValue: float
    "Ifd base current"
    ignd: int
    "Star Point:&0&grounded:&2&isolated"
    iintgnd: int
    "Neutral Conductor: N-Connection:None:At terminal (ABC-N):Separate terminal"
    iopt_windm: int
    "Wind Model: Wind Model"
    ip_ctrl: int
    "Reference Machine"
    iqtype: int
    "Reactive Power Operational Limits: Use limits specified in type"
    is4SpinReserve: int
    "Consider for region spinning reserve"
    isConsCostOp: int
    "Operating costs"
    isConsCostsRedispatch: int
    "Additional redispatch costs"
    isConsShutDownCost: int
    "Shut-down costs"
    isConsStartUpCost: int
    "Start-up costs"
    isConstrRamp: int
    "Ramp rate constraints"
    isConstrUpDown: int
    "Start-up/shut-down time constraints"
    isCtrlFixedToLdfVal: int
    "Additional constraints for controls: Fix controls to Load Flow values"
    isCtrlP: int
    "Controls: Active power"
    isCtrlPplacement: int
    "Optimise active power"
    isCtrlQ: int
    "Controls: Reactive power"
    isDiscreteCtrlP: int
    "Restriction to discrete active power values"
    isLimPmax: int
    "Active Power Operational Limits: Max."
    isLimPmin: int
    "Active Power Operational Limits: Min."
    isLimQmax: int
    "Reactive Power Operational Limits: Max."
    isLimQmin: int
    "Reactive Power Operational Limits: Min."
    isMustRunUC: int
    "Additional constraints for controls: Must run"
    isPcurrAllowed: int
    "Restriction to discrete active power values: Allow current active power value"
    isRPR: int
    "Optimisation of reactive power reserve"
    isVRE: int
    "Generator usage: Generator usage:Single thermal generation unit:Variable renewable energy source (VRE):Coupled with storage model:Part of Virtual Power Plant"
    iv_mode: int
    "Local Controller"
    limRampDown: float
    "Ramp rate constraints: Ramp-down limit"
    limRampDownPU: float
    "Ramp rate constraints: Ramp-down limit"
    limRampShutDown: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampShutDownPU: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampStartUp: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampStartUpPU: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampUp: float
    "Ramp rate constraints: Ramp-up limit"
    limRampUpPU: float
    "Ramp rate constraints: Ramp-up limit"
    loc_name: str
    "Name"
    mdmex: float
    "Mechanical load: Exponent"
    mdmlp: float
    "Mechanical load: Proportional Factor"
    mean: float
    "Wind Model Weibull Distribution for Wind Speed: Mean"
    minDownTime: float
    "Start-up/shut-down time constraints: Minimum down-time"
    minUpTime: float
    "Start-up/shut-down time constraints: Minimum up-time"
    mode_inp: str
    "Dispatch: Input Mode"
    mode_pgi: int
    "Model:Active power input:Wind speed input"
    ngnum: int
    "Number of: parallel Machines"
    numBreakpointsCostOp: int
    "Piecewise linearisation for LP: Number of breakpoints"
    oid_: int
    "ObjectID"
    outServPzero: int
    "Out of service when active power is zero"
    outserv: int
    "Out of Service"
    pBMU: object
    "Virtual Power Plant"
    pCharYrMW: list
    "Wind Model Time Series Characteristics: Annual Samples: Time Series Characteristics of Active Power Contribution (MW)"
    pCharYrWS: list
    "Wind Model Time Series Characteristics: Annual Samples: Time Series Characteristics for Wind Speed (m/s)"
    pFlicker: object
    "Flicker Contribution: Flicker Coefficients"
    pG: float
    "Range of Voltage Regulation (+/-)"
    pGRStoch: object
    "Stochastic Model for Generation: Stochastic Model"
    pMeteostat: object
    "Wind Model: Meteo Station (Correlation)"
    pOpCostCurve: object
    "Operating costs: Generator cost curve"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pPowerCrv: object
    "Wind Power Curve"
    pQPcurve: object
    "Q(P)-Characteristic: Q(P)-Curve"
    pQlimType: object
    "Reactive Power Operational Limits: Capability Curve"
    pStoch: object
    "Stochastic model"
    pStorage: object
    "Storage model"
    p_direc: int
    "Dispatch: Power Direction:P>=0:P<0"
    penaltyCosts: float
    "Penalty costs"
    pf_recap: int
    "Dispatch: Power Factor:ind.:cap."
    pf_recap_a: str
    "Actual Dispatch: Power Factor Ind/Cap (act.)"
    pgini: float
    "Dispatch: Active Power"
    pgini_a: float
    "Actual Dispatch: Active Power (act.)"
    phiini: float
    "Dispatch: Angle"
    phmc: object
    "Harmonic Load Flow: Harmonic Voltages"
    phtech: int
    "Technology"
    pid_: int
    "ProjectID"
    pmaxratf: float
    "Active Power: Rating: Rating Factor"
    polyDegree: int
    "Polynomial degree"
    priority: int
    "Merit Order"
    q_max: float
    "Reactive Power Operational Limits: Max."
    q_min: float
    "Reactive Power Operational Limits: Min."
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qgini: float
    "Dispatch: Reactive Power"
    qgini_a: float
    "Actual Dispatch: Reactive Power (act.)"
    resy: float
    "Internal Grounding Impedance: Resistance, Re"
    rf_st: float
    "Use integrated AVR for motor starting: Starting field resistance"
    root_id: object
    "Original Location"
    sOpComment: list
    "Operator Comment"
    scaleQmax: float
    "Reactive Power Operational Limits: Scaling Factor (max.)"
    scaleQmin: float
    "Reactive Power Operational Limits: Scaling Factor (min.)"
    sernum: str
    "Serial Number"
    sgini: float
    "Dispatch: Apparent Power"
    sgini_a: float
    "Actual Dispatch: Apparent Power (act.)"
    smoothfac: float
    "Smoothing factor"
    speed_th: float
    "Use integrated AVR for motor starting: Trigger excitation at speed"
    speedinit: float
    "Initial speed"
    stowind: int
    "Wind Model"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    usetp: float
    "Dispatch: Voltage"
    usp_max: float
    "Voltage Setpoint Limits: Max. Voltage Setpoint"
    usp_min: float
    "Voltage Setpoint Limits: Min. Voltage Setpoint"
    variance: float
    "Wind Model Weibull Distribution for Wind Speed: Variance"
    ve_const: float
    "Use integrated AVR for motor starting: Constant field voltage"
    ve_rated: float
    "Use integrated AVR for motor starting: Rated field voltage"
    vecBreakpointsP: list
    "Piecewise linearisation for LP: Power"
    vecCostRedispatchDown: list
    "Costs"
    vecCostRedispatchUp: list
    "Costs"
    vecDiscreteCtrlPvals: list
    "Restriction to discrete active power values: Valid active power values"
    vecPowerRedispatchDown: list
    "Redispatch"
    vecPowerRedispatchUp: list
    "Redispatch"
    vecStartUpCosts: list
    "Start-up costs: Start-up costs"
    vecStartUpTimes: list
    "Start-up costs: Down-time"
    windspeed: float
    "Dispatch: Wind speed"
    windspeed_a: float
    "Actual Dispatch: Wind speed (act.)"
    xesy: float
    "Internal Grounding Impedance: Reactance, Xe"

    def AttributeType(*args): ...

    def CalcEfficiency(*args): ...

    def Derate(*args): ...

    def Disconnect(*args): ...

    def GetAvailableGenPower(*args): ...

    def GetGroundingImpedance(*args): ...

    def GetMotorStartingFlag(*args): ...

    def GetStepupTransformer(*args): ...

    def HasReferences(*args): ...

    def IsConnected(*args): ...

    def Reconnect(*args): ...

    def ResetDerating(*args): ...

    def __getattr__(*args): ...


class ElmTerm(PFGeneral):
    AccessTime: float
    "Access Times of Switches: Access Time"
    BoxDepth: float
    "Dimensions of enclosure: Depth"
    BoxHeight: float
    "Dimensions of enclosure: Height"
    BoxWidth: float
    "Dimensions of enclosure: Width"
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures Double Earth Fault: Repair duration"
    CondGap: float
    "Conductor gap"
    DcBoxType: int
    "Enclosure type:Panelboard:LV switchgear:MV switchgear"
    Electrodes: str
    "Electrode configuration"
    FOD: float
    "Failures: Forced Outage Duration"
    FOE: float
    "Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures: Forced Outage Rate"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Iac_t: float
    "A.C. Component of Short-Circuit Current"
    LocAccTime: float
    "Access Times of Switches: Local Access Time"
    NodeName: str
    "Node Name"
    NomIn: float
    "Sum of feeding cables or Smallest feeding cable"
    NomOut: float
    "Sum of leaving cables or Biggest leaving cable"
    UcteNodeName: str
    "Ucte Node Name"
    Vtarget: float
    "Voltage Control: Target Voltage"
    WorkDist: float
    "Working distance"
    Xfactor: float
    "Distance factor"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cAccessTime: float
    "Access Times of Switches: Access Time"
    cBoxDepth: float
    "Depth"
    cBoxHeight: float
    "Height"
    cBoxWidth: float
    "Width"
    cBoxed: int
    "Enclosure:Open air:Boxed"
    cCapShnt: object
    "ComCapo Shunt"
    cCondGap: float
    "Conductor gap"
    cConsis: float
    "Consistency Status:NOT OK:  OK"
    cDcBoxType: int
    "Enclosure type:Panelboard:LV switchgear:MV switchgear"
    cDisplayName: str
    "Display Name"
    cElectrodes: list
    "Electrode configuration"
    cIntInStat: int
    "Internal Node in Substation"
    cLocAccTime: float
    "Access Times of Switches: Local Access Time"
    cPosLne: float
    "Nominal Voltage: Position on Line"
    cStatName: str
    "Station/Name"
    cUserDefIndex: int
    "User defined Index"
    cWorkDist: float
    "Working distance"
    cXfactor: float
    "Distance factor"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciBusbarCon: int
    "Connection Status"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBay: object
    "Equipment Data: Bay"
    cpBranch: object
    "Branch"
    cpBusbar: object
    "Busbar"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cubics: list
    "Cubicles"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    dvmax: float
    "Voltage Control: Delta V max"
    dvmin: float
    "Voltage Control: Delta V min"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAccessLoc: int
    "Accessible Location"
    iBayEnd: int
    "Bay end"
    iBoxed: int
    "Enclosure:Open air:Boxed"
    iComDate: int
    "Commissioning Date"
    iEarth: int
    "Earthed"
    iOPFCvmax: int
    "Voltage limits: Upper Voltage Limit"
    iOPFCvmin: int
    "Voltage limits: Lower Voltage Limit"
    iPriority: int
    "Priority for connectivity tracing"
    iSchemeStatus: int
    "Scheme Status"
    iSection: int
    "Section"
    iSubstatDef: int
    "Equipment Data"
    iTopoPrio: int
    "Tie Open Point Optimisation: Priority"
    iUsage: int
    "Usage:Busbar:Junction Node:Internal Node"
    i_t: float
    "Short-circuit current (instantaneous)"
    idc_t: float
    "D.C. Component of Short-Circuit Current"
    ik_t: float
    "Upper Envelope of Short-Circuit Current"
    ikl_t: float
    "Lower Envelope of Short-Circuit Current"
    iminus: int
    "Nominal Voltage: DC-Polarity:positive (+):negative (-):neutral"
    iperfect: int
    "Failures: Ideal component"
    isSoftConstr: int
    "Voltage limits: Soft constraint"
    isshc: int
    "Short-Circuit Bus"
    ivpriority: int
    "Voltage Control: Priority"
    loc_name: str
    "Name"
    nneutral: int
    "No of Neutrals:0:1"
    nphase: int
    "No of Phases"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pArea: object
    "Area"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pStoch: object
    "Failures: Element model"
    pTypStoch: object
    "Failures: Type model"
    pZone: object
    "Zone"
    phtech: int
    "Phase Technology:ABC:ABC-N:BI:BI-N:2PH:2PH-N:1PH:1PH-N:N"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    systype: int
    "System Type:AC:DC:AC/BI"
    tid_: int
    "TimeID"
    tinter: float
    "End of interruption"
    tstart: float
    "Start of interruption"
    typ_id: object
    "Type"
    u_minph: float
    "Phase Voltage (Min)"
    uknom: float
    "Nominal Voltage: Line-Line"
    unknom: float
    "Nominal Voltage: Line-Ground"
    vmax: float
    "Steady State Voltage Limits: Upper Voltage Limit"
    vmin: float
    "Steady State Voltage Limits: Lower Voltage Limit"
    vstep_bus: float
    "Voltage Step Change Limits: Busbar Fault"
    vstep_change: int
    "Voltage Step Change Limits"
    vstep_n1: float
    "Voltage Step Change Limits: n-1"
    vstep_n2: float
    "Voltage Step Change Limits: n-2"
    vtarget: float
    "Voltage Control: Target Voltage"

    def AttributeType(*args): ...

    def GetBusType(*args): ...

    def GetCalcRelevantCubicles(*args): ...

    def GetConnectedBrkCubicles(*args): ...

    def GetConnectedCubicles(*args): ...

    def GetConnectedMainBuses(*args): ...

    def GetConnectionInfo(*args): ...

    def GetEquivalentTerminals(*args): ...

    def GetMinDistance(*args): ...

    def GetNextHVBus(*args): ...

    def GetNodeName(*args): ...

    def GetSepStationAreas(*args): ...

    def GetShortestPath(*args): ...

    def HasCreatedCalBus(*args): ...

    def HasReferences(*args): ...

    def IsElectrEquivalent(*args): ...

    def IsEquivalent(*args): ...

    def IsInternalNodeInStation(*args): ...

    def UpdateSubstationTerminals(*args): ...

    def __getattr__(*args): ...


class ElmTr2(PFGeneral):
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures Double Earth Fault: Repair duration"
    Cc0_hl: float
    "Consider Capacitances: Capacitance HV-LV, 0-Sequence"
    Cc1_hl: float
    "Consider Capacitances: Capacitance HV-LV, 1-Sequence"
    Cg_h: float
    "Consider Capacitances: Capacitance HV-Ground"
    Cg_l: float
    "Consider Capacitances: Capacitance LV-Ground"
    FOD: float
    "Failures Transformer Failures: Forced Outage Duration"
    FOE: float
    "Failures Transformer Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures Transformer Failures: Forced Outage Rate"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Ib_lv: float
    "Values for LV-Side: Highest Operating Current"
    InomPre_h: float
    "HV-Side, Pre-fault Nominal Current"
    InomPre_l: float
    "LV-Side, Pre-fault Nominal Current"
    Inom_h: float
    "HV-Side, Nominal Current"
    Inom_h_a: float
    "HV-Side, Nominal Current (act.)"
    Inom_l: float
    "LV-Side, Nominal Current"
    Inom_l_a: float
    "LV-Side, Nominal Current"
    Irze: list
    "Rated Current of Grounding"
    Kpart: float
    "Participation factor"
    Kpart2: float
    "Participation factor"
    Kpctrl: float
    "Controller Sensitivity dtap/dP"
    Kpctrl2: float
    "Controller Sensitivity dtap/dP"
    Kqctrl: float
    "Controller Sensitivity dtap/dQ"
    Kqctrl2: float
    "Controller Sensitivity dtap/dQ"
    PsiresA: float
    "Residual flux: Phase A"
    PsiresB: float
    "Residual flux: Phase B"
    PsiresC: float
    "Residual flux: Phase C"
    Ptolerance: float
    "Tolerance (+/-)"
    Ptolerance2: float
    "Tolerance (+/-)"
    Snom: float
    "Nominal Power"
    Snom_a: float
    "Nominal Power (act.)"
    Tctrl: float
    "Controller Time Constant"
    Tctrl2: float
    "Controller Time Constant"
    Ub_lv: float
    "Values for LV-Side: Highest Operating Voltage"
    Ubqmin_hv: float
    "Values for HV-Side (only for Unit Transformer): Minimum Operating Voltage"
    Vtolerance: float
    "LDC/Current Compounding Compensation: Tolerance (+/-)"
    Vtolerance2: float
    "LDC/Current Compounding Compensation: Tolerance (+/-)"
    allowCntConstrFilt: int
    "Constraint Filtering: Allow contingency filtering by number of critical constraints"
    allowMarginFilt: int
    "Constraint Filtering: Allow filtering by constraint margin"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    availFactor: float
    "Availability Factor"
    bSbasepu: float
    "b (Sbase)"
    bushv: object
    "HV-Side"
    bushvn: object
    "Neutral Conductor: HV-Neutral"
    buslv: object
    "LV-Side"
    buslvn: object
    "LV-Neutral"
    cAllowCntConstrFilt: int
    "Constraint Filtering: Allow contingency filtering by number of critical constraints"
    cAllowMarginFilt: int
    "Constraint Filtering: Allow filtering by constraint margin"
    cCtrlTapCont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    cCtrlTapContOpf: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    cDisplayName: str
    "Display Name"
    cIsSepCntConstrType: int
    "Max. loading constraint for contingencies: Separate constraint type"
    cIsSepCntMaxAllowedLoading: int
    "Max. loading constraint for contingencies: Separate max. allowed loading"
    cOptOnlyPre: int
    "Controls for Optimal Power Flow: Optimise in DC OPF:Pre- and post-fault position:Only pre-fault position"
    cPsiresC: float
    "Residual flux: Phase C"
    cUserDefIndex: int
    "User defined Index"
    c_plcc: object
    "External LCC Controller"
    c_pstac: object
    "External Station Controller"
    c_ptapc: object
    "External Tap Controller"
    cgnd_h: int
    "Internal Grounding Impedance, HV Side: Star Point:Connected:Not connected"
    cgnd_l: int
    "Internal Grounding Impedance, LV Side: Star Point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cneutcon: int
    "Neutral Conductor: N-Connection"
    cntConstrType: int
    "Max. loading constraint for contingencies: Contingency-constraint type:Off:Soft constraint"
    cntMaxAllowedLoading: float
    "Max. loading constraint for contingencies: Max. allowed loading in Contingencies"
    coldloadtab2: list
    "Values"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cosphib_lv: float
    "Values for LV-Side: Power factor"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpCtrlNode: object
    "Target Node"
    cpCtrlNode2: object
    "Target Node"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpeter_h: int
    "Internal Grounding Impedance, HV Side: Petersen Coil"
    cpeter_l: int
    "Internal Grounding Impedance, LV Side: Petersen Coil"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    drawInr: int
    "Time-overcurrent plot: Draw Inrush Current"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    fr_coldload: int
    "Time-overcurrent plot: Cold load curve"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iIntTapCtrl: int
    "Tap Changer 1, Measurement Table: Use Integrated Tap Controller"
    iMeasLoc: int
    "Tap Changer 1, Measurement Table: Measured at"
    iOPFCload: int
    "Max. loading constraint"
    iPpart: int
    "Active power participation"
    iPpart2: int
    "Active power participation"
    iResFlux: int
    "Residual flux"
    iSchemeStatus: int
    "Scheme Status"
    iTaps: int
    "Tap Changer 1: According to Measurement Report"
    iZoneBus: int
    "Zone"
    i_auto: int
    "Auto Transformer"
    i_cont: int
    "Tap Changer:discrete:continuous"
    i_cont2: int
    "Tap Changer:discrete:continuous"
    i_eahv: int
    "HV-side, phase 2 internally grounded"
    i_ealv: int
    "LV-side, phase 2 internally grounded"
    i_hvcon: int
    "HV-side, phase 2 connected"
    i_lvcon: int
    "LV-side, phase 2 connected"
    i_rem: int
    "Remote Control"
    i_rem2: int
    "Remote Control"
    i_tapini: int
    "State Estimation: Estimate Tap 1 Position"
    i_tapini2: int
    "Estimate Tap 2 Position"
    i_uopt: int
    "Controls for Optimal Power Flow: Tap Changer 1:Off:On:Part of external Tap Controller"
    i_uopt2: int
    "Tap Changer 2"
    i_uoptCont: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    i_uoptCont2: int
    "Control Mode:discrete:continuous"
    iansish: int
    "Time-overcurrent plot: ANSI Curve Shift"
    iblock: int
    "Unit Transformer"
    icomp: int
    "LDC/Current Compounding Compensation: Compounding:apparent current:active current:reactive current:apparent power:active power:reactive power"
    icomp2: int
    "LDC/Current Compounding Compensation: Compounding:apparent current:active current:reactive current:apparent power:active power:reactive power"
    ifc: int
    "Forced Cooling Enabled"
    ifrqft: int
    "Time-overcurrent plot: Frequent Fault ( >10(5)/lifetime, Category II(III) )"
    ignd_h: int
    "Star Point:grounded:compensated:isolated"
    ignd_l: int
    "Star Point:grounded:compensated:isolated"
    iintgnd: int
    "Neutral Connection"
    ilcph: int
    "Phase:a:b:c:a-b:b-c:c-a:Pos.Seq."
    ilcph2: int
    "Phase:a:b:c:a-b:b-c:c-a:Pos.Seq."
    ildc: int
    "Compensation:none:internal (LDC) line drop compensation:external (LDC) line drop compensation:current compounding"
    ildc2: int
    "Compensation:none:internal (LDC) line drop compensation:external (LDC) line drop compensation:current compounding"
    ilt_op: int
    "Long-term operating conditions before short-circuit are known"
    imldc: str
    "Control Mode:V:P:Q"
    imldc2: str
    "Control Mode:V:P:Q"
    ionlyPre: int
    "Controls for Optimal Power Flow: Optimise in DC OPF:Pre- and post-fault position:Only pre-fault position"
    iopt_hf: int
    "Consider Capacitances"
    iperfect: int
    "Failures: Ideal component"
    isConstrLoading: int
    "Max. loading constraint for Unit Commitment"
    isConstrLoadingPlacement: int
    "Max. loading constraint for Optimal Equipment Placement"
    isCtrlTap: int
    "Controls for Unit Commitment: Tap Changer 1:Off:On:Part of external Tap Controller"
    isCtrlTapCont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    isCtrlTapPlacement: int
    "Controls for Optimal Equipment Placement: Position of tap 1"
    isMaxLoadSoftNlin: int
    "Penalty costs for soft constraints"
    isSepCntConstrType: int
    "Max. loading constraint for contingencies: Separate constraint type"
    isSepCntMaxAllowedLoading: int
    "Max. loading constraint for contingencies: Separate max. allowed loading"
    ldcct: float
    "LDC/Current Compounding Compensation: Current Transformer Rating"
    ldcct2: float
    "LDC/Current Compounding Compensation: Current Transformer Rating"
    ldcpt: float
    "LDC/Current Compounding Compensation: Voltage Transformer Ratio"
    ldcpt2: float
    "LDC/Current Compounding Compensation: Voltage Transformer Ratio"
    ldcrs: float
    "LDC/Current Compounding Compensation: Rset"
    ldcrs2: float
    "LDC/Current Compounding Compensation: Rset"
    ldcxs: float
    "LDC/Current Compounding Compensation: Xset"
    ldcxs2: float
    "LDC/Current Compounding Compensation: Xset"
    loc_name: str
    "Name"
    lossAssign: int
    "Loss assignment:according to grouping:uniformly distributed:to HV-Side:to LV-Side"
    mTaps: list
    "Tap Changer 1, Measurement Table: Measurement Report"
    maxload: float
    "Thermal Loading Limit: Max. loading"
    nntap: int
    "Tap Changer 1: Tap Position"
    nntap2: int
    "Tap Changer 2: Tap Position"
    nntapabs: int
    "Absolute Tap Position"
    ntnum: int
    "Number of: parallel Transformers"
    ntrcn: int
    "Automatic Tap Changing"
    ntrcn2: int
    "Automatic Tap Changing"
    oid_: int
    "ObjectID"
    optap2max: int
    "Operational limits for tap changer Tap Changer 2: Maximum Position"
    optap2min: int
    "Operational limits for tap changer Tap Changer 2: Minimum Position"
    optaplimit: int
    "Operational limits for tap changer"
    optapmax: int
    "Operational limits for tap changer Tap Changer 1: Maximum Position"
    optapmin: int
    "Operational limits for tap changer Tap Changer 1: Minimum Position"
    outserv: int
    "Out of Service"
    pMeteo: object
    "Meteo. Station"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pRating: object
    "Thermal Rating"
    pStoch: object
    "Failures: Element model"
    pTypStoch: object
    "Failures: Type model"
    pVccurve: object
    "LDC/Current Compounding Compensation: V-Control-Curve"
    pVccurve2: object
    "LDC/Current Compounding Compensation: V-Control-Curve"
    p_cub: object
    "Controlled Branch (Cubicle)"
    p_cub2: object
    "Controlled Branch (Cubicle)"
    p_pmeas: object
    "P measured at"
    p_pmeas2: object
    "P measured at"
    p_rem: object
    "Controlled Node"
    p_rem2: object
    "Controlled Node"
    penaltyCosts: float
    "Controls for Optimal Power Flow: Penalty costs per Tap deviation"
    pid_: int
    "ProjectID"
    pldc: object
    "LDC/Current Compounding Compensation: External LDC"
    pldc2: object
    "LDC/Current Compounding Compensation: External LDC"
    psetp: float
    "Active Power Setpoint"
    psetp2: float
    "Active Power Setpoint"
    psp_low: float
    "Lower Active Power Bound"
    psp_low2: float
    "Lower Active Power Bound"
    psp_up: float
    "Upper Active Power Bound"
    psp_up2: float
    "Upper Active Power Bound"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qsetp: float
    "Reactive Power Setpoint"
    qsetp2: float
    "Reactive Power Setpoint"
    qsp_low: float
    "Lower Reactive Power Bound"
    qsp_low2: float
    "Lower Reactive Power Bound"
    qsp_up: float
    "Upper Reactive Power Bound"
    qsp_up2: float
    "Upper Reactive Power Bound"
    r0Sbasepu: float
    "r0 (Sbase)"
    rSbasepu: float
    "r (Sbase)"
    ratfac: float
    "Rating Factor"
    re0tr_h: float
    "Internal Grounding Impedance, HV Side: Resistance, Re"
    re0tr_l: float
    "Internal Grounding Impedance, LV Side: Resistance, Re"
    root_id: object
    "Original Location"
    sOpComment: list
    "Operator Comment"
    scalingFacSoftConstrCost: float
    "Penalty costs for soft constraints: Cost scaling factor"
    scalingFacSoftConstrOpf: float
    "Max. loading constraint: Weighting factor for soft constraint penalty"
    sernum: str
    "Serial Number"
    strf1: float
    "Load Current"
    t2ldc: int
    "Controlled Node is at:HV:LV:EXT"
    t2ldc2: int
    "Controlled Node is at:HV:LV"
    tapctrl: object
    "Tap Controller"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    uset_mode: int
    "Setpoint:local:bus target voltage"
    uset_mode2: int
    "Setpoint:local:bus target voltage"
    usetp: float
    "Voltage Setpoint"
    usetp2: float
    "Voltage Setpoint"
    usp_low: float
    "Lower Voltage Bound"
    usp_low2: float
    "Lower Voltage Bound"
    usp_up: float
    "Upper Voltage Bound"
    usp_up2: float
    "Upper Voltage Bound"
    x0Sbasepu: float
    "x0 (Sbase)"
    xSbasepu: float
    "x (Sbase)"
    xe0tr_h: float
    "Internal Grounding Impedance, HV Side: Reactance, Xe"
    xe0tr_l: float
    "Internal Grounding Impedance, LV Side: Reactance, Xe"

    def AttributeType(*args): ...

    def CreateEvent(*args): ...

    def GetGroundingImpedance(*args): ...

    def GetSuppliedElements(*args): ...

    def GetTapPhi(*args): ...

    def GetTapRatio(*args): ...

    def GetZ0pu(*args): ...

    def GetZpu(*args): ...

    def HasReferences(*args): ...

    def IsQuadBooster(*args): ...

    def NTap(*args): ...

    def __getattr__(*args): ...


class ElmTr3(PFGeneral):
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures Double Earth Fault: Repair duration"
    Cc0_hm: float
    "Consider Capacitances Winding to Winding, 0-Sequence: HV-MV"
    Cc0_lh: float
    "Consider Capacitances Winding to Winding, 0-Sequence: LV-HV"
    Cc0_ml: float
    "Consider Capacitances Winding to Winding, 0-Sequence: MV-LV"
    Cc1_hm: float
    "Consider Capacitances Winding to Winding, 1-Sequence: HV-MV"
    Cc1_lh: float
    "Consider Capacitances Winding to Winding, 1-Sequence: LV-HV"
    Cc1_ml: float
    "Consider Capacitances Winding to Winding, 1-Sequence: MV-LV"
    Cg_h: float
    "Consider Capacitances Winding to Ground: HV-Ground"
    Cg_l: float
    "Consider Capacitances Winding to Ground: LV-Ground"
    Cg_m: float
    "Consider Capacitances Winding to Ground: MV-Ground"
    FOD: float
    "Failures Transformer Failures: Forced Outage Duration"
    FOE: float
    "Failures Transformer Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures Transformer Failures: Forced Outage Rate"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Inom_h: float
    "HV-Side, Nominal Current"
    Inom_h_a: float
    "HV-Side, Nominal Current (act.)"
    Inom_l: float
    "LV-Side, Nominal Current"
    Inom_l_a: float
    "LV-Side, Nominal Current (act.)"
    Inom_m: float
    "MV-Side, Nominal Current"
    Inom_m_a: float
    "MV-Side, Nominal Current (act.)"
    Irze: list
    "Rated Current of Grounding"
    Kpart: float
    "Participation factor"
    Kpart2: float
    "Participation factor"
    Kpctrl: float
    "Controller Sensitivity dtap/dP"
    Kpctrl2: float
    "Controller Sensitivity dtap/dP"
    Kqctrl: float
    "Controller Sensitivity dtap/dQ"
    Kqctrl2: float
    "Controller Sensitivity dtap/dQ"
    PsiresA: float
    "Residual flux: Phase A"
    PsiresB: float
    "Residual flux: Phase B"
    PsiresC: float
    "Residual flux: Phase C"
    Ptolerance: float
    "Tolerance (+/-)"
    Ptolerance2: float
    "Tolerance (+/-)"
    Snom_h: float
    "HV-Side, Nominal Power"
    Snom_h_a: float
    "Thermal Rating: HV-Side, Nom.Power (act.)"
    Snom_l: float
    "LV-Side, Nominal Power"
    Snom_l_a: float
    "Thermal Rating: LV-Side, Nom.Power (act.)"
    Snom_m: float
    "MV-Side, Nominal Power"
    Snom_m_a: float
    "Thermal Rating: MV-Side, Nom.Power (act.)"
    Tctrl: float
    "Controller Time Constant"
    Tctrl2: float
    "Controller Time Constant"
    Vtolerance: float
    "LDC/Current Compounding Compensation: Tolerance (+/-)"
    Vtolerance2: float
    "LDC/Current Compounding Compensation: Tolerance (+/-)"
    allowCntConstrFilt: int
    "Constraint Filtering: Allow contingency filtering by number of critical constraints"
    allowMarginFilt: int
    "Constraint Filtering: Allow filtering by constraint margin"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    availFactor: float
    "Availability Factor"
    bSbasepu: float
    "b (Sbase)"
    bushv: object
    "HV-Side"
    bushvn: object
    "Neutral Conductor: HV-Neutral"
    buslv: object
    "LV-Side"
    buslvn: object
    "LV-Neutral"
    busmv: object
    "MV-Side"
    busmvn: object
    "Neutral Conductor: MV-Neutral"
    cAllowCntConstrFilt: int
    "Constraint Filtering: Allow contingency filtering by number of critical constraints"
    cAllowMarginFilt: int
    "Constraint Filtering: Allow filtering by constraint margin"
    cCtrlTapHVCont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    cCtrlTapHVContOpf: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    cCtrlTapLVCont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    cCtrlTapLVContOpf: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    cCtrlTapMVCont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    cCtrlTapMVContOpf: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    cDisplayName: str
    "Display Name"
    cIsSepCntConstrType: int
    "Max. loading constraint for contingencies: Separate constraint type"
    cIsSepCntMaxAllowedLoading: int
    "Max. loading constraint for contingencies: Separate max. allowed loading"
    cOptOnlyPre: int
    "Controls for Optimal Power Flow: Optimise in DC OPF:Pre- and post-fault position:Only pre-fault position"
    cPsiresC: float
    "Residual flux: Phase C"
    cUserDefIndex: int
    "User defined Index"
    c_plcc: object
    "External LCC Controller"
    c_pstac: object
    "External Station Controller"
    c_ptapc: object
    "External Tap Controller"
    cgnd_h: int
    "Internal Grounding Imp., HV Side: Star Point:Connected:Not connected"
    cgnd_l: int
    "Internal Grounding Imp., LV Side: Star Point:Connected:Not connected"
    cgnd_m: int
    "Internal Grounding Imp., MV Side: Star Point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cneutcon: int
    "Neutral Conductor: N-Connection"
    cntConstrType: int
    "Max. loading constraint for contingencies: Contingency-constraint type:Off:Soft constraint"
    cntMaxAllowedLoading: float
    "Max. loading constraint for contingencies: Max. allowed loading in Contingencies"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpCtrlNode: object
    "Target Node"
    cpCtrlNode2: object
    "Target Node"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpeter_h: int
    "Internal Grounding Imp., HV Side: Petersen Coil"
    cpeter_l: int
    "Internal Grounding Imp., LV Side: Petersen Coil"
    cpeter_m: int
    "Internal Grounding Imp., MV Side: Petersen Coil"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    drawInr: int
    "Time-overcurrent plot: Draw Inrush Current"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    fr_coldload: int
    "Time-overcurrent plot: Cold Load Curve"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iIntTapCtrl: int
    "Tap: Use Integrated Tap Controller"
    iMeasLoc: int
    "Tap: Measured at:HV-Side:MV-Side:LV-Side"
    iMeasTap: int
    "Tap: for Tap at:HV-Side:MV-Side:LV-Side"
    iOPFCload: int
    "Max. loading constraint"
    iPpart: int
    "Active power participation"
    iPpart2: int
    "Active power participation"
    iResFlux: int
    "Residual flux"
    iSchemeStatus: int
    "Scheme Status"
    iTaps: int
    "Tap: According to Measurement Report"
    iZoneBus: int
    "Zone"
    i_auto_hl: int
    "Auto Transformer:none:HV-LV:HV-MV:MV-LV"
    i_cont: int
    "Tap Changer:discrete:continuous"
    i_cont2: int
    "Tap Changer:discrete:continuous"
    i_eahv: int
    "HV-side: Phase 2 internally grounded"
    i_ealv: int
    "LV-side: Phase 2 internally grounded"
    i_eamv: int
    "MV-side: Phase 2 internally grounded"
    i_hvcon: int
    "HV-side: Phase 2 connected"
    i_lvcon: int
    "LV-side: Phase 2 connected"
    i_mvcon: int
    "MV-side: Phase 2 connected"
    i_neuthv: int
    "HV-side: Neutral Connection"
    i_neutlv: int
    "LV-side: Neutral Connection"
    i_neutmv: int
    "MV-side: Neutral Connection"
    i_rem: int
    "Remote Control"
    i_rem2: int
    "Remote Control"
    i_tapini_h: int
    "State Estimation: Estimate Tap Position HV-Side"
    i_tapini_l: int
    "State Estimation: Estimate Tap Position LV-Side"
    i_tapini_m: int
    "State Estimation: Estimate Tap Position MV-Side"
    i_tapoptCont_h: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    i_tapoptCont_l: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    i_tapoptCont_m: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    i_tapopt_h: int
    "Controls for Optimal Power Flow: Tap Position HV-Side:Off:On:Part of external Tap Controller"
    i_tapopt_l: int
    "Controls for Optimal Power Flow: Tap Position LV-Side:Off:On:Part of external Tap Controller"
    i_tapopt_m: int
    "Controls for Optimal Power Flow: Tap Position MV-Side:Off:On:Part of external Tap Controller"
    iansish: int
    "Time-overcurrent plot: ANSI Curve Shift"
    iblock: int
    "Unit Transformer"
    icomp: int
    "LDC/Current Compounding Compensation: Compounding:apparent current:active current:reactive current:apparent power:active power:reactive power"
    icomp2: int
    "LDC/Current Compounding Compensation: Compounding:apparent current:active current:reactive current:apparent power:active power:reactive power"
    ictrlside: int
    "Controller for tap at:HV-Side:MV-Side:LV-Side"
    ictrlside2: int
    "Controller for tap at:&-1&not defined:&0&HV-Side:&1&MV-Side:&2&LV-Side"
    ifc: int
    "Forced Cooling Enabled"
    ifrqft: int
    "Time-overcurrent plot: Frequent Fault ( >10(5)/lifetime, Category II(III) )"
    ignd_h: int
    "Star Point:grounded:compensated:isolated"
    ignd_l: int
    "Star Point:grounded:compensated:isolated"
    ignd_m: int
    "Star Point:grounded:compensated:isolated"
    iintgnd: int
    "External Star Point"
    ilcph: int
    "Phase:a:b:c:a-b:b-c:c-a:Pos.Seq."
    ilcph2: int
    "Phase:a:b:c:a-b:b-c:c-a:Pos.Seq."
    ildc: int
    "Compensation:none:external (LDC) line drop compensation:current compounding"
    ildc2: int
    "Compensation:none:external (LDC) line drop compensation:current compounding"
    imldc: str
    "Control Mode:V:P:Q"
    imldc2: str
    "Control Mode:V:P:Q"
    input_cl: list
    "Values"
    ionlyPre: int
    "Controls for Optimal Power Flow: Optimise in DC OPF:Pre- and post-fault position:Only pre-fault position"
    iopt_hf: int
    "Consider Capacitances"
    iperfect: int
    "Failures: Ideal component"
    isConstrLoading: int
    "Max. loading constraint for Unit Commitment"
    isConstrLoadingPlacement: int
    "Max. loading constraint for Optimal Equipment Placement"
    isCtrlTapHV: int
    "Controls for Unit Commitment: Tap Position HV-Side:Off:On:Part of external Tap Controller"
    isCtrlTapHVCont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    isCtrlTapHVPlacement: int
    "Controls for Optimal Equipment Placement: Tap Position HV-Side"
    isCtrlTapLV: int
    "Controls for Unit Commitment: Tap Position LV-Side:Off:On:Part of external Tap Controller"
    isCtrlTapLVCont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    isCtrlTapLVPlacement: int
    "Controls for Optimal Equipment Placement: Tap Position LV-Side"
    isCtrlTapMV: int
    "Controls for Unit Commitment: Tap Position MV-Side:Off:On:Part of external Tap Controller"
    isCtrlTapMVCont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    isCtrlTapMVPlacement: int
    "Controls for Optimal Equipment Placement: Tap Position MV-Side"
    isMaxLoadSoftNlin: int
    "Penalty costs for soft constraints"
    isSepCntConstrType: int
    "Max. loading constraint for contingencies: Separate constraint type"
    isSepCntMaxAllowedLoading: int
    "Max. loading constraint for contingencies: Separate max. allowed loading"
    iwinding: int
    "Time-overcurrent plot: Create Curve for:HV-MV:HV-LV:MV-LV"
    loc_name: str
    "Name"
    lossAssign: int
    "Loss assignment:according to grouping:uniformly distributed:to HV-Side:to MV-Side:to LV-Side"
    mTaps: list
    "Tap: Measurement Report"
    maxload: float
    "Thermal Loading Limit: Max. loading"
    n3tap_h: int
    "Tap HV-Side: Act. Position"
    n3tap_l: int
    "Tap LV-Side: Act. Position"
    n3tap_m: int
    "Tap MV-Side: Act. Position"
    n3tapabs_h: int
    "Act. Position absolute"
    n3tapabs_l: int
    "Act. Position absolute"
    n3tapabs_m: int
    "Act. Position absolute"
    nt3nm: int
    "Number of: parallel Transformers"
    ntrcn: int
    "Automatic Tap Changing"
    ntrcn2: int
    "Automatic Tap Changing"
    oid_: int
    "ObjectID"
    optaplimit: int
    "Operational limits for tap changer"
    optapmax_h: int
    "Operational limits for tap changer Tap HV-Side: Maximum Position"
    optapmax_l: int
    "Operational limits for tap changer Tap LV-Side: Maximum Position"
    optapmax_m: int
    "Operational limits for tap changer Tap MV-Side: Maximum Position"
    optapmin_h: int
    "Operational limits for tap changer Tap HV-Side: Minimum Position"
    optapmin_l: int
    "Operational limits for tap changer Tap LV-Side: Minimum Position"
    optapmin_m: int
    "Operational limits for tap changer Tap MV-Side: Minimum Position"
    outserv: int
    "Out of Service"
    pMeteo: object
    "Thermal Rating: Meteo. Station"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pRating: object
    "Thermal Rating"
    pRating_h: object
    "Thermal Rating: HV-Side"
    pRating_l: object
    "Thermal Rating: LV-Side"
    pRating_m: object
    "Thermal Rating: MV-Side"
    pStoch: object
    "Failures: Element model"
    pT_h: str
    "Tap HV-Side: Voltage Range"
    pT_l: str
    "Tap LV-Side: Voltage Range"
    pT_m: str
    "Tap MV-Side: Voltage Range"
    pTypStoch: object
    "Failures: Type model"
    pVccurve: object
    "LDC/Current Compounding Compensation: V-Control-Curve"
    pVccurve2: object
    "LDC/Current Compounding Compensation: V-Control-Curve"
    p_cub: object
    "Controlled Branch (Cubicle)"
    p_cub2: object
    "Controlled Branch (Cubicle)"
    p_pmeas: object
    "P measured at"
    p_pmeas2: object
    "P measured at"
    p_rem: object
    "Controlled Node"
    p_rem2: object
    "Controlled Node"
    penaltyCosts: float
    "Controls for Optimal Power Flow: Penalty costs per Tap deviation"
    pid_: int
    "ProjectID"
    pldc: object
    "LDC/Current Compounding Compensation: External LDC"
    pldc2: object
    "LDC/Current Compounding Compensation: External LDC"
    psetp: float
    "Active Power Setpoint"
    psetp2: float
    "Active Power Setpoint"
    psp_low: float
    "Lower Active Power Bound"
    psp_low2: float
    "Lower Active Power Bound"
    psp_up: float
    "Upper Active Power Bound"
    psp_up2: float
    "Upper Active Power Bound"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qsetp: float
    "Reactive Power Setpoint"
    qsetp2: float
    "Reactive Power Setpoint"
    qsp_low: float
    "Lower Reactive Power Bound"
    qsp_low2: float
    "Lower Reactive Power Bound"
    qsp_up: float
    "Upper Reactive Power Bound"
    qsp_up2: float
    "Upper Reactive Power Bound"
    r0Sbasepu_h: float
    "r0(HV) (Sbase)"
    r0Sbasepu_hm: float
    "r0(HV-MV) (Sbase)"
    r0Sbasepu_l: float
    "r0(LV) (Sbase)"
    r0Sbasepu_lh: float
    "r0(LV-HV) (Sbase)"
    r0Sbasepu_m: float
    "r0(MV) (Sbase)"
    r0Sbasepu_ml: float
    "r0(MV-LV) (Sbase)"
    rSbasepu_h: float
    "r(HV) (Sbase)"
    rSbasepu_hm: float
    "r(HV-MV) (Sbase)"
    rSbasepu_l: float
    "r(LV) (Sbase)"
    rSbasepu_lh: float
    "r(LV-HV) (Sbase)"
    rSbasepu_m: float
    "r(MV) (Sbase)"
    rSbasepu_ml: float
    "r(MV-LV) (Sbase)"
    ratfac_h: float
    "Thermal Rating: HV-Side"
    ratfac_l: float
    "Thermal Rating: LV-Side"
    ratfac_m: float
    "Thermal Rating: MV-Side"
    re0h: float
    "Internal Grounding Imp., HV Side: Resistance, Re"
    re0l: float
    "Internal Grounding Imp., LV Side: Resistance, Re"
    re0m: float
    "Internal Grounding Imp., MV Side: Resistance, Re"
    root_id: object
    "Original Location"
    sOpComment: list
    "Operator Comment"
    scalingFacSoftConstrCost: float
    "Penalty costs for soft constraints: Cost scaling factor"
    scalingFacSoftConstrOpf: float
    "Max. loading constraint: Weighting factor for soft constraint penalty"
    sernum: str
    "Serial Number"
    t3ldc: int
    "Controlled Node is at:HV:MV:LV:EXT"
    t3ldc2: int
    "Controlled Node is at:HV:MV:LV"
    tapctrl: object
    "Tap Controller"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    uset_mode: int
    "Setpoint:local:bus target voltage"
    uset_mode2: int
    "Setpoint:local:bus target voltage"
    usetp: float
    "Voltage Setpoint"
    usetp2: float
    "Voltage Setpoint"
    usp_low: float
    "Lower Voltage Bound"
    usp_low2: float
    "Lower Voltage Bound"
    usp_up: float
    "Upper Voltage Bound"
    usp_up2: float
    "Upper Voltage Bound"
    x0Sbasepu_h: float
    "x0(HV) (Sbase)"
    x0Sbasepu_hm: float
    "x0(HV-MV) (Sbase)"
    x0Sbasepu_l: float
    "x0(LV) (Sbase)"
    x0Sbasepu_lh: float
    "x0(LV-HV) (Sbase)"
    x0Sbasepu_m: float
    "x0(MV) (Sbase)"
    x0Sbasepu_ml: float
    "x0(MV-LV) (Sbase)"
    xSbasepu_h: float
    "x(HV) (Sbase)"
    xSbasepu_hm: float
    "x(HV-MV) (Sbase)"
    xSbasepu_l: float
    "x(LV) (Sbase)"
    xSbasepu_lh: float
    "x(LV-HV) (Sbase)"
    xSbasepu_m: float
    "x(MV) (Sbase)"
    xSbasepu_ml: float
    "x(MV-LV) (Sbase)"
    xe0h: float
    "Internal Grounding Imp., HV Side: Reactance, Xe"
    xe0l: float
    "Internal Grounding Imp., LV Side: Reactance, Xe"
    xe0m: float
    "Internal Grounding Imp., MV Side: Reactance, Xe"

    def AttributeType(*args): ...

    def CreateEvent(*args): ...

    def GetGroundingImpedance(*args): ...

    def GetSuppliedElements(*args): ...

    def GetTapPhi(*args): ...

    def GetTapRatio(*args): ...

    def GetTapZDependentSide(*args): ...

    def GetZ0pu(*args): ...

    def GetZpu(*args): ...

    def HasReferences(*args): ...

    def IsQuadBooster(*args): ...

    def NTap(*args): ...

    def __getattr__(*args): ...


class ElmTr4(PFGeneral):
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures Double Earth Fault: Repair duration"
    FOD: float
    "Failures Transformer Failures: Forced Outage Duration"
    FOE: float
    "Failures Transformer Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures Transformer Failures: Forced Outage Rate"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Inom_h0: float
    "HV-Side, Nominal Current"
    Inom_h0_a: float
    "HV-Side, Nominal Current (act.)"
    Inom_l1: float
    "LV1-Side, Nominal Current"
    Inom_l1_a: float
    "LV1-Side, Nominal Current (act.)"
    Inom_l2: float
    "LV2-Side, Nominal Current"
    Inom_l2_a: float
    "LV2-Side, Nominal Current (act.)"
    Inom_l3: float
    "LV3-Side, Nominal Current"
    Inom_l3_a: float
    "LV3-Side, Nominal Current (act.)"
    Irze: list
    "Rated Current of Grounding"
    Kpart: float
    "Participation factor"
    Kpctrl: float
    "Controller Sensitivity dtap/dP"
    Kqctrl: float
    "Controller Sensitivity dtap/dQ"
    PsiresA: float
    "Residual flux: Phase A"
    PsiresB: float
    "Residual flux: Phase B"
    PsiresC: float
    "Residual flux: Phase C"
    Ptolerance: float
    "Tolerance (+/-)"
    Snom_h0: float
    "HV-Side, Nominal Power"
    Snom_h0_a: float
    "Thermal Rating: HV-Side, Nom.Power (act.)"
    Snom_l1: float
    "LV1-Side, Nominal Power"
    Snom_l1_a: float
    "Thermal Rating: LV1-Side, Nom.Power (act.)"
    Snom_l2: float
    "LV2-Side, Nominal Power"
    Snom_l2_a: float
    "Thermal Rating: LV2-Side, Nom.Power (act.)"
    Snom_l3: float
    "LV3-Side, Nominal Power"
    Snom_l3_a: float
    "Thermal Rating: LV3-Side, Nom.Power (act.)"
    Tctrl: float
    "Controller Time Constant"
    Vtolerance: float
    "LDC/Current Compounding Compensation: Tolerance (+/-)"
    allowCntConstrFilt: int
    "Constraint Filtering: Allow contingency filtering by number of critical constraints"
    allowMarginFilt: int
    "Constraint Filtering: Allow filtering by constraint margin"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    availFactor: float
    "Availability Factor"
    bSbasepu: float
    "b (Sbase)"
    bush0: object
    "HV-Side"
    busl1: object
    "LV1-Side"
    busl2: object
    "LV2-Side"
    busl3: object
    "LV3-Side"
    cAllowCntConstrFilt: int
    "Constraint Filtering: Allow contingency filtering by number of critical constraints"
    cAllowMarginFilt: int
    "Constraint Filtering: Allow filtering by constraint margin"
    cCtrlTapHVCont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    cCtrlTapHVContOpf: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    cCtrlTapLV1Cont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    cCtrlTapLV1ContOpf: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    cCtrlTapLV2Cont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    cCtrlTapLV2ContOpf: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    cCtrlTapLV3Cont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    cCtrlTapLV3ContOpf: int
    "Controls for Optimal Power Flow: Control Mode:discrete:continuous"
    cDisplayName: str
    "Display Name"
    cIsSepCntConstrType: int
    "Max. loading constraint for contingencies: Separate constraint type"
    cIsSepCntMaxAllowedLoading: int
    "Max. loading constraint for contingencies: Separate max. allowed loading"
    cOptOnlyPre: int
    "Controls for Optimal Power Flow: Optimise in DC OPF:Pre- and post-fault position:Only pre-fault position"
    cPsiresC: float
    "Residual flux: Phase C"
    cUserDefIndex: int
    "User defined Index"
    c_plcc: object
    "External LCC Controller"
    c_pstac: object
    "External Station Controller"
    c_ptapc: object
    "External Tap Controller"
    cgnd_hv0: int
    "Internal Grounding Imp., HV Side: Star Point:Connected:Not connected"
    cgnd_lv1: int
    "Internal Grounding Imp., LV1 Side: Star Point:Connected:Not connected"
    cgnd_lv2: int
    "Internal Grounding Imp., LV2 Side: Star Point:Connected:Not connected"
    cgnd_lv3: int
    "Internal Grounding Imp., LV3 Side: Star Point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cntConstrType: int
    "Max. loading constraint for contingencies: Contingency-constraint type:Off:Soft constraint"
    cntMaxAllowedLoading: float
    "Max. loading constraint for contingencies: Max. allowed loading in Contingencies"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpCtrlNode: object
    "Target Node"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpeter_hv0: int
    "Internal Grounding Imp., HV Side: Petersen Coil"
    cpeter_lv1: int
    "Internal Grounding Imp., LV1 Side: Petersen Coil"
    cpeter_lv2: int
    "Internal Grounding Imp., LV2 Side: Petersen Coil"
    cpeter_lv3: int
    "Internal Grounding Imp., LV3 Side: Petersen Coil"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    drawInr: int
    "Time-overcurrent plot: Draw Inrush Current"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    fr_coldload: int
    "Time-overcurrent plot: Cold Load Curve"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iIntTapCtrl: int
    "Use Integrated Tap Controller"
    iOPFCload: int
    "Max. loading constraint"
    iPpart: int
    "Active power participation"
    iResFlux: int
    "Residual flux"
    iSchemeStatus: int
    "Scheme Status"
    iZoneBus: int
    "Zone"
    i_cont: int
    "Tap Changer:discrete:continuous"
    i_rem: int
    "Remote Control"
    i_tapini_hv0: int
    "State Estimation: Estimate Tap Position HV-Side"
    i_tapini_lv1: int
    "State Estimation: Estimate Tap Position LV1-Side"
    i_tapini_lv2: int
    "State Estimation: Estimate Tap Position LV2-Side"
    i_tapini_lv3: int
    "State Estimation: Estimate Tap Position LV2-Side"
    i_tapoptCont_hv0: int
    "Controls for Optimal Power Flow: Control Mode HV-Side:discrete:continuous"
    i_tapoptCont_lv1: int
    "Controls for Optimal Power Flow: Control Mode LV1-Side:discrete:continuous"
    i_tapoptCont_lv2: int
    "Controls for Optimal Power Flow: Control Mode LV2-Side:discrete:continuous"
    i_tapoptCont_lv3: int
    "Controls for Optimal Power Flow: Control Mode LV3-Side:discrete:continuous"
    i_tapopt_hv0: int
    "Controls for Optimal Power Flow: Tap Position HV-Side:Off:On:Part of external Tap Controller"
    i_tapopt_lv1: int
    "Controls for Optimal Power Flow: Tap Position LV1-Side:Off:On:Part of external Tap Controller"
    i_tapopt_lv2: int
    "Controls for Optimal Power Flow: Tap Position LV2-Side:Off:On:Part of external Tap Controller"
    i_tapopt_lv3: int
    "Controls for Optimal Power Flow: Tap Position LV3-Side:Off:On:Part of external Tap Controller"
    iansish: int
    "Time-overcurrent plot: ANSI Curve Shift"
    icomp: int
    "LDC/Current Compounding Compensation: Compounding:apparent current:active current:reactive current:apparent power:active power:reactive power"
    ictrlside: int
    "Controller for tap at:HV-Side:LV1-Side:LV2-Side:LV3-Side"
    ifc: int
    "Forced Cooling Enabled"
    ifrqft: int
    "Time-overcurrent plot: Frequent Fault ( >10(5)/lifetime, Category II(III) )"
    ignd_hv0: int
    "Star Point:grounded:compensated:isolated"
    ignd_lv1: int
    "Star Point:grounded:compensated:isolated"
    ignd_lv2: int
    "Star Point:grounded:compensated:isolated"
    ignd_lv3: int
    "Star Point:grounded:compensated:isolated"
    ilcph: int
    "Phase:a:b:c:a-b:b-c:c-a:Pos.Seq."
    ildc: int
    "Compensation:none:external (LDC) line drop compensation:current compounding"
    imldc: str
    "Control Mode:V:P:Q"
    input_cl: list
    "Values"
    ionlyPre: int
    "Controls for Optimal Power Flow: Optimise in DC OPF:Pre- and post-fault position:Only pre-fault position"
    iperfect: int
    "Failures: Ideal component"
    isConstrLoading: int
    "Max. loading constraint for Unit Commitment"
    isConstrLoadingPlacement: int
    "Max. loading constraint for Optimal Equipment Placement"
    isCtrlTapHV: int
    "Controls for Unit Commitment: Tap Position HV-Side:Off:On:Part of external Tap Controller"
    isCtrlTapHVCont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    isCtrlTapHVPlacement: int
    "Controls for Optimal Equipment Placement: Tap Position HV-Side"
    isCtrlTapLV1: int
    "Controls for Unit Commitment: Tap Position LV1-Side:Off:On:Part of external Tap Controller"
    isCtrlTapLV1Cont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    isCtrlTapLV1Placement: int
    "Controls for Optimal Equipment Placement: Tap Position LV1-Side"
    isCtrlTapLV2: int
    "Controls for Unit Commitment: Tap Position LV2-Side:Off:On:Part of external Tap Controller"
    isCtrlTapLV2Cont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    isCtrlTapLV2Placement: int
    "Controls for Optimal Equipment Placement: Tap Position LV2-Side"
    isCtrlTapLV3: int
    "Controls for Unit Commitment: Tap Position LV3-Side:Off:On:Part of external Tap Controller"
    isCtrlTapLV3Cont: int
    "Controls for Unit Commitment: Control Mode:discrete:continuous"
    isCtrlTapLV3Placement: int
    "Controls for Optimal Equipment Placement: Tap Position LV3-Side"
    isMaxLoadSoftNlin: int
    "Penalty costs for soft constraints"
    isSepCntConstrType: int
    "Max. loading constraint for contingencies: Separate constraint type"
    isSepCntMaxAllowedLoading: int
    "Max. loading constraint for contingencies: Separate max. allowed loading"
    iwinding: int
    "Time-overcurrent plot: Create Curve for:HV-LV1:HV-LV2:HV-LV3:LV1-LV2:LV1-LV3:LV2-LV3"
    loc_name: str
    "Name"
    lodt3: str
    "Type Load"
    lossAssign: int
    "Loss assignment:according to grouping:uniformly distributed:to HV-Side:to LV1-Side:to LV2-Side:to LV3-Side"
    maxload: float
    "Thermal Loading Limit: Max. loading"
    nt3rl: list
    "Pointer to relays"
    nt4nm: int
    "Number of: parallel Transformers"
    ntap_h0: int
    "Tap HV-Side: Act. Position"
    ntap_l1: int
    "Tap LV1-Side: Act. Position"
    ntap_l2: int
    "Tap LV2-Side: Act. Position"
    ntap_l3: int
    "Tap LV3-Side: Act. Position"
    ntapabs_h0: int
    "Act. Position absolute"
    ntapabs_l1: int
    "Act. Position absolute"
    ntapabs_l2: int
    "Act. Position absolute"
    ntapabs_l3: int
    "Act. Position absolute"
    ntrcn: int
    "Automatic Tap Changing"
    oid_: int
    "ObjectID"
    optaplimit: int
    "Operational limits for tap changer"
    optapmax_h0: int
    "Operational limits for tap changer Tap HV-Side: Maximum Position"
    optapmax_l1: int
    "Operational limits for tap changer Tap LV1-Side: Maximum Position"
    optapmax_l2: int
    "Operational limits for tap changer Tap LV2-Side: Maximum Position"
    optapmax_l3: int
    "Operational limits for tap changer Tap LV3-Side: Maximum Position"
    optapmin_h0: int
    "Operational limits for tap changer Tap HV-Side: Minimum Position"
    optapmin_l1: int
    "Operational limits for tap changer Tap LV1-Side: Minimum Position"
    optapmin_l2: int
    "Operational limits for tap changer Tap LV2-Side: Minimum Position"
    optapmin_l3: int
    "Operational limits for tap changer Tap LV3-Side: Minimum Position"
    outserv: int
    "Out of Service"
    pMeteo: object
    "Thermal Rating: Meteo. Station"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pRating_hv0: object
    "Thermal Rating: HV-Side"
    pRating_lv1: object
    "Thermal Rating: LV1-Side"
    pRating_lv2: object
    "Thermal Rating: LV2-Side"
    pRating_lv3: object
    "Thermal Rating: LV3-Side"
    pStoch: object
    "Failures: Element model"
    pT_hv0: str
    "Tap HV-Side: Voltage Range"
    pT_lv1: str
    "Tap LV1-Side: Voltage Range"
    pT_lv2: str
    "Tap LV2-Side: Voltage Range"
    pT_lv3: str
    "Tap LV3-Side: Voltage Range"
    pTypStoch: object
    "Failures: Type model"
    pVccurve: object
    "LDC/Current Compounding Compensation: V-Control-Curve"
    p_cub: object
    "Controlled Branch (Cubicle)"
    p_pmeas: object
    "P measured at"
    p_rem: object
    "Controlled Node"
    penaltyCosts: float
    "Controls for Optimal Power Flow: Penalty costs per Tap deviation"
    pid_: int
    "ProjectID"
    pldc: object
    "LDC/Current Compounding Compensation: External LDC"
    psetp: float
    "Active Power Setpoint"
    psp_low: float
    "Lower Active Power Bound"
    psp_up: float
    "Upper Active Power Bound"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qsetp: float
    "Reactive Power Setpoint"
    qsp_low: float
    "Lower Reactive Power Bound"
    qsp_up: float
    "Upper Reactive Power Bound"
    r0Sbasepu_h0l1: float
    "r0(HV-LV1) (Sbase)"
    r0Sbasepu_h0l2: float
    "r0(HV-LV2) (Sbase)"
    r0Sbasepu_h0l3: float
    "r0(HV-LV3) (Sbase)"
    r0Sbasepu_hv0: float
    "r0(HV) (Sbase)"
    r0Sbasepu_l1l2: float
    "r0(LV1-LV2) (Sbase)"
    r0Sbasepu_l1l3: float
    "r0(LV1-LV3) (Sbase)"
    r0Sbasepu_l2l3: float
    "r0(LV2-LV3) (Sbase)"
    r0Sbasepu_lv1: float
    "r0(LV1) (Sbase)"
    r0Sbasepu_lv2: float
    "r0(LV2) (Sbase)"
    r0Sbasepu_lv3: float
    "r0(LV3) (Sbase)"
    rSbasepu_h0l1: float
    "r(HV-LV1) (Sbase)"
    rSbasepu_h0l2: float
    "r(HV-LV2) (Sbase)"
    rSbasepu_h0l3: float
    "r(HV-LV3) (Sbase)"
    rSbasepu_hv0: float
    "r(HV) (Sbase)"
    rSbasepu_l1l2: float
    "r(LV1-LV2) (Sbase)"
    rSbasepu_l1l3: float
    "r(LV1-LV3) (Sbase)"
    rSbasepu_l2l3: float
    "r(LV2-LV3) (Sbase)"
    rSbasepu_lv1: float
    "r(LV1) (Sbase)"
    rSbasepu_lv2: float
    "r(LV2) (Sbase)"
    rSbasepu_lv3: float
    "r(LV3) (Sbase)"
    ratfac_h0: float
    "Thermal Rating: HV-Side"
    ratfac_l1: float
    "Thermal Rating: LV1-Side"
    ratfac_l2: float
    "Thermal Rating: LV2-Side"
    ratfac_l3: float
    "Thermal Rating: LV3-Side"
    re0hv0: float
    "Internal Grounding Imp., HV Side: Resistance, Re"
    re0lv1: float
    "Internal Grounding Imp., LV1 Side: Resistance, Re"
    re0lv2: float
    "Internal Grounding Imp., LV2 Side: Resistance, Re"
    re0lv3: float
    "Internal Grounding Imp., LV3 Side: Resistance, Re"
    root_id: object
    "Original Location"
    sOpComment: list
    "Operator Comment"
    scalingFacSoftConstrCost: float
    "Penalty costs for soft constraints: Cost scaling factor"
    scalingFacSoftConstrOpf: float
    "Max. loading constraint: Weighting factor for soft constraint penalty"
    sernum: str
    "Serial Number"
    t4ldc: int
    "Controlled Node is at:HV:LV1:LV2:LV3:EXT"
    tapctrl: object
    "Tap Controller"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    uset_mode: int
    "Setpoint:local:bus target voltage"
    usetp: float
    "Voltage Setpoint"
    usp_low: float
    "Lower Voltage Bound"
    usp_up: float
    "Upper Voltage Bound"
    x0Sbasepu_h0l1: float
    "x0(HV-LV1) (Sbase)"
    x0Sbasepu_h0l2: float
    "x0(HV-LV2) (Sbase)"
    x0Sbasepu_h0l3: float
    "x0(HV-LV3) (Sbase)"
    x0Sbasepu_hv0: float
    "x0(HV) (Sbase)"
    x0Sbasepu_l1l2: float
    "x0(LV1-LV2) (Sbase)"
    x0Sbasepu_l1l3: float
    "x0(LV1-LV3) (Sbase)"
    x0Sbasepu_l2l3: float
    "x0(LV2-LV3) (Sbase)"
    x0Sbasepu_lv1: float
    "x0(LV1) (Sbase)"
    x0Sbasepu_lv2: float
    "x0(LV2) (Sbase)"
    x0Sbasepu_lv3: float
    "x0(LV3) (Sbase)"
    xSbasepu_h0l1: float
    "x(HV-LV1) (Sbase)"
    xSbasepu_h0l2: float
    "x(HV-LV2) (Sbase)"
    xSbasepu_h0l3: float
    "x(HV-LV3) (Sbase)"
    xSbasepu_hv0: float
    "x(HV) (Sbase)"
    xSbasepu_l1l2: float
    "x(LV1-LV2) (Sbase)"
    xSbasepu_l1l3: float
    "x(LV1-LV3) (Sbase)"
    xSbasepu_l2l3: float
    "x(LV2-LV3) (Sbase)"
    xSbasepu_lv1: float
    "x(LV1) (Sbase)"
    xSbasepu_lv2: float
    "x(LV2) (Sbase)"
    xSbasepu_lv3: float
    "x(LV3) (Sbase)"
    xe0hv0: float
    "Internal Grounding Imp., HV Side: Reactance, Xe"
    xe0lv1: float
    "Internal Grounding Imp., LV1 Side: Reactance, Xe"
    xe0lv2: float
    "Internal Grounding Imp., LV2 Side: Reactance, Xe"
    xe0lv3: float
    "Internal Grounding Imp., LV3 Side: Reactance, Xe"

    def AttributeType(*args): ...

    def CreateEvent(*args): ...

    def GetGroundingImpedance(*args): ...

    def GetSuppliedElements(*args): ...

    def GetTapPhi(*args): ...

    def GetTapRatio(*args): ...

    def GetTapZDependentSide(*args): ...

    def GetZ0pu(*args): ...

    def GetZpu(*args): ...

    def HasReferences(*args): ...

    def IsQuadBooster(*args): ...

    def NTap(*args): ...

    def __getattr__(*args): ...


class ElmTrain(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cosaux: float
    "Auxiliary Power: Auxiliary Power Factor"
    cosini: float
    "Traction/Recuperation: Power Factor"
    cosini_a: float
    "cos(phi)(act.)"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iComDate: int
    "Commissioning Date"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    location: object
    "Location for train simulation: Location"
    mode_inp: str
    "Traction/Recuperation: Input Mode"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    paux: float
    "Auxiliary Power: Auxiliary Active Power"
    paux_a: float
    "Paux(act.)"
    pf_coninj: int
    "Traction/Recuperation: Power Factor:Q consumption:Q injection"
    phtech: str
    "Technology"
    pid_: int
    "ProjectID"
    pini: float
    "Traction/Recuperation: Active Power"
    pini_a: float
    "P(act.)"
    position: float
    "Location for train simulation: Position"
    qini: float
    "Traction/Recuperation: Reactive Power"
    qini_a: float
    "Q(act.)"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    speed: float
    "Traction/Recuperation: Speed"
    speed_a: float
    "Speed(act.)"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def SetPosition(*args): ...

    def __getattr__(*args): ...


class ElmTrb(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Inom_h: float
    "HV-Side, Nominal Current"
    Inom_h_a: float
    "HV-Side, Nominal Current (act.)"
    Inom_l: float
    "LV-Side, Nominal Current"
    Inom_l_a: float
    "LV-Side, Nominal Current"
    Irze: float
    "Rated Current of Grounding"
    Snom: float
    "Nominal Power"
    Snom_a: float
    "Nominal Power (act.)"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bushv1: object
    "Terminal HVi"
    bushv2: object
    "Terminal HVj"
    buslv: object
    "Terminal LV"
    buslv2: object
    "Terminal LVj"
    buslvn: object
    "Neutral Conductor: LV-Neutral"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    cgnd_l: int
    "Grounding Impedance, LV Side: Star Point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cneutcon: int
    "Neutral Conductor: N-Connection"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpeter_l: int
    "Grounding Impedance, LV Side: Petersen Coil"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iComDate: int
    "Commissioning Date"
    iSchemeStatus: int
    "Scheme Status"
    iZoneBus: int
    "Zone"
    ignd_l: int
    "Star Point:grounded:compensated:isolated"
    iintgnd: int
    "Neutral Connection"
    loc_name: str
    "Name"
    maxload: float
    "Thermal Loading Limit: Max. Loading"
    nphases: int
    "No. of Phases:1:3"
    ntnum: int
    "Number of: parallel Transformers"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pMeteo: object
    "Meteo. Station"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pRating: object
    "Thermal Rating"
    pid_: int
    "ProjectID"
    ratfac: float
    "Rating Factor"
    re0tr_l: float
    "Grounding Impedance, LV Side: Re"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    xe0tr_l: float
    "Grounding Impedance, LV Side: Xe"

    def AttributeType(*args): ...

    def GetGroundingImpedance(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmTrfstat(PFGeneral):
    AccessTime: float
    "Access Times of Switches: Access Time"
    BoxDepth: float
    "Dimensions of enclosure: Depth"
    BoxHeight: float
    "Dimensions of enclosure: Height"
    BoxWidth: float
    "Dimensions of enclosure: Width"
    CondGap: float
    "Conductor Gap"
    DcBoxType: int
    "Enclosure type:Panelboard:LV switchgear:MV switchgear"
    Electrodes: str
    "Electrode configuration"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    LocAccTime: float
    "Access Times of Switches: Local Access Time"
    Unom: float
    "Nominal Voltage"
    WorkDist: float
    "Working Distance"
    Xfactor: float
    "Distance Factor"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUnom: float
    "Nominal Voltage"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cimRdfId: list
    "RDF ID"
    constr: int
    "Year of Construction"
    contents: list
    "Contents"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBoxed: int
    "Enclosure:Open air:Boxed"
    iSchemeStatus: int
    "Scheme Status"
    icolor: int
    "Colour"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pArea: object
    "Default Area"
    pBusbar: object
    "Busbar"
    pDiagram: object
    "Diagram"
    pOperator: object
    "Default Operator"
    pOwner: object
    "Default Owner"
    pSwSc: object
    "Switching Rules: Active Rules"
    pZone: object
    "Default Zone"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sShort: str
    "Short Name"
    sType: str
    "Type"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def GetSplit(*args): ...

    def GetSplitCal(*args): ...

    def GetSplitIndex(*args): ...

    def GetSuppliedElements(*args): ...

    def HasReferences(*args): ...

    def SaveAsSwSc(*args): ...

    def __getattr__(*args): ...


class ElmVac(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Ikd: float
    "Steady-State Shc. Current: Ikd"
    Irze: list
    "Rated Current of Grounding"
    Kpf: float
    "Prim. Frequency Bias"
    Ksf: float
    "Sec. Frequency Bias"
    L0: float
    "Frequency Dependencies: Inductance, L0"
    L1: float
    "Frequency Dependencies: Inductance, L1"
    L2: float
    "Frequency Dependencies: Inductance, L2"
    Pgen: float
    "Generated Power: Active Power"
    Pload: float
    "Load, P,Q = const.: Active Power"
    Pzload: float
    "Load, Z = const.: Active Power"
    Qgen: float
    "Generated Power: Reactive Power"
    Qload: float
    "Load, P,Q = const.: Reactive Power"
    Qzload: float
    "Load, Z = const.: Reactive Power"
    R0: float
    "Zero Sequence: Resistance, R0"
    R1: float
    "Positive Sequence: Resistance, R1"
    R1s: float
    "Positive Sequence Transient: Resistance, R1s"
    R2: float
    "Negative Sequence: Resistance, R2"
    Rext: float
    "Extended Ward: Resistance"
    Unnom: float
    "Nominal Voltage: Line-Ground"
    Unom: float
    "Nominal Voltage: Line-Line"
    X0: float
    "Zero Sequence: Reactance, X0"
    X1: float
    "Positive Sequence: Reactance, X1"
    X1s: float
    "Positive Sequence Transient: Reactance, X1s"
    X2: float
    "Negative Sequence: Reactance, X2"
    Xext: float
    "Extended Ward: Reactance"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    c_pmod: object
    "Model"
    c_psecc: object
    "Ext. Secondary Controller"
    cfreqs: list
    "Frequency"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    contbar: object
    "Positive Sequence: Controlled Node"
    cosimCtrlType: int
    "Control type for co-simulation model."
    cosimModel: int
    "Used for Co-simulation"
    cospreld: float
    "Preload Conditions: Power Factor"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    curpreld: float
    "Preload Conditions: Current"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dphidf: float
    "Frequency Sweep Calculation only: Spectral Density of Voltage Angle"
    dudf: float
    "Frequency Sweep Calculation only: Spectral Density of Voltage Magnitude"
    fcharL0: object
    "Frequency Dependencies: L0(f)"
    fcharL1: object
    "Frequency Dependencies: L1(f)"
    fcharL2: object
    "Frequency Dependencies: L2(f)"
    fcharR0: object
    "Frequency Dependencies: R0(f)"
    fcharR1: object
    "Frequency Dependencies: R1(f)"
    fcharR2: object
    "Frequency Dependencies: R2(f)"
    fchardphi: object
    "Frequency Sweep Calculation only: Frequency Dependency"
    fchardu: object
    "Frequency Sweep Calculation only: Frequency Dependency"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    freq: float
    "Frequency"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iFreZ: int
    "Use Frequency Related Impedance for X/R Ratio Calculation"
    iHmcType: int
    "Type of Harmonic Voltages"
    iPossibleSlack: int
    "Can be considered as a potential slack"
    iSchemeStatus: int
    "Scheme Status"
    ifreq: float
    "Frequency/Nominal Frequency"
    ifreqs: list
    "Harm. Order"
    ifreqs_iec2: list
    "Harm. Order"
    itype: int
    "Type:Voltage Source:Ideal RC-Source:Ward Equivalent:Extended Ward Equivalent"
    iztreqz: int
    "Positive Sequence: Transient = Subtransient Impedance"
    leadFinput: int
    "Parameter event can be applied to: Frequency input:F0Hz (in Hz):f0 (in p.u.)"
    leadUinput: int
    "Parameter event can be applied to: Voltage input"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    matZ: list
    "Frequency related impedances (Positive, Negative and Zero sequence)"
    nphase: int
    "No. of Phases:1:2:3"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    p_phictrl: object
    "Positive Sequence External Controller for: Angle Control"
    p_uctrl: object
    "Positive Sequence External Controller for: Voltage Control"
    phiSlackRef: float
    "Used for Co-simulation: Initial rotor angle"
    phiiniRef: float
    "Used for Co-simulation: Initial angle of bus voltage"
    phisetp: float
    "Positive Sequence: Voltage, Angle"
    phisetp0: float
    "Zero Sequence: Voltage, Angle"
    phisetp2: float
    "Negative Sequence: Voltage, Angle"
    pid_: int
    "ProjectID"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    tds: float
    "Time Constants: Td'"
    tdss: float
    "Time Constants: Td''"
    tid_: int
    "TimeID"
    u0_mag: list
    "u0, Mag."
    u0_phase: list
    "u0, Ang."
    u1_mag: list
    "u1, Mag."
    u1_phase: list
    "u1, Ang."
    u2_mag: list
    "u2, Mag."
    u2_phase: list
    "u2, Ang."
    umag_iec1: list
    "U_h"
    umag_iec2: list
    "U_h"
    usetp: float
    "Positive Sequence: Voltage, Magnitude"
    usetp0: float
    "Zero Sequence: Voltage, Magnitude"
    usetp2: float
    "Negative Sequence: Voltage, Magnitude"

    def AttributeType(*args): ...

    def GetGroundingImpedance(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmVoltreg(PFGeneral):
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures Double Earth Fault: Repair duration"
    FOD: float
    "Failures Transformer failures: Forced Outage Duration"
    FOE: float
    "Failures Transformer failures: Forced Outage Expectancy"
    FOR1: float
    "Failures Transformer failures: Forced Outage Rate"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Inom: float
    "Nominal current"
    InomPre: float
    "Pre-fault nominal current"
    Inom_a: float
    "Nominal current (act.)"
    Irze: list
    "Rated current of grounding"
    RevThresh: float
    "Reverse power operation: Current deadband (+/-)"
    Snom: float
    "Nominal Power"
    Snom_a: float
    "Nominal Power (act.)"
    Tctrl: float
    "Controller, tap changer: Controller time constant"
    allowCntConstrFilt: int
    "Constraint Filtering: Allow contingency filtering by number of critical constraints"
    allowMarginFilt: int
    "Constraint Filtering: Allow filtering by constraint margin"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    availFactor: float
    "Availability Factor"
    busl: object
    "L-Side"
    buss: object
    "S-Side"
    bussl: object
    "Neutral conductor: SL-Neutral"
    cAllowCntConstrFilt: int
    "Constraint Filtering: Allow contingency filtering by number of critical constraints"
    cAllowMarginFilt: int
    "Constraint Filtering: Allow filtering by constraint margin"
    cDisplayName: str
    "Display Name"
    cInom: float
    "Tap changer: Continuous current rating at selected voltage control range"
    cIsSepCntConstrType: int
    "Max. loading constraint for contingencies: Separate constraint type"
    cIsSepCntMaxAllowedLoading: int
    "Max. loading constraint for contingencies: Separate max. allowed loading"
    cUserDefIndex: int
    "User defined Index"
    cgnd: int
    "Internal grounding impedance: Star point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cneutcon: int
    "Neutral conductor: N-Connection"
    cntConstrType: int
    "Max. loading constraint for contingencies: Contingency-constraint type:Off:Soft constraint"
    cntMaxAllowedLoading: float
    "Max. loading constraint for contingencies: Max. allowed loading in Contingencies"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dutap: float
    "Tap changer: Additional voltage per tap"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iComDate: int
    "Commissioning Date"
    iIntTapCtrl: int
    "Tap changer: Use integrated tap controller"
    iOPFCload: int
    "Max. loading constraint"
    iRevPQ: int
    "Reverse power operation"
    iSchemeStatus: int
    "Scheme Status"
    iZoneBus: int
    "Zone"
    i_cont: int
    "Controller, tap changer: Tap changer:discrete:continuous"
    i_pcReglim: int
    "Tap changer: Limited voltage control range"
    i_tapini: int
    "State Estimation: Estimate tap position"
    i_uopt: int
    "Controls for Optimal Power Flow: Tap Changer"
    i_uoptCont: int
    "Controls for Optimal Power Flow: Control mode:discrete:continuous"
    ictrlModRev: int
    "Reverse power operation: Control mode:Locked forward:Bidirectional:Co-generation:Q-bidirectional"
    igang: int
    "Tap changer: Gang operated taps"
    ignd: int
    "Star point:grounded:isolated"
    iintgnd: int
    "Neutral connection"
    ilcph: int
    "Controller, tap changer: Phase:a:b:c:a-b:b-c:c-a:Pos.Seq."
    ildc: int
    "Controller, tap changer: Line drop compensation (LDC):none:internal"
    ildcRev: int
    "Reverse power operation: Line drop compensation (LDC):none:internal"
    ildc_lm: int
    "Controller, tap changer: Voltage limit"
    installCost: float
    "Costs: Installation costs"
    ionlyPre: int
    "Controls for Optimal Power Flow: Optimise in DC OPF:Pre- and post-fault position:Only pre-fault position"
    iperfect: int
    "Failures: Ideal component"
    isConstrLoading: int
    "Max. loading constraint for Unit Commitment"
    isConstrLoadingPlacement: int
    "Max. loading constraint for Optimal Equipment Placement"
    isCtrlTap: int
    "Tap Changer"
    isCtrlTapCont: int
    "Tap Changer: Control Mode:discrete:continuous"
    isCtrlTapPlacement: int
    "Controls for Optimal Equipment Placement: Position of tap 1"
    isMaxLoadSoftNlin: int
    "Penalty costs for soft constraints"
    isSepCntConstrType: int
    "Max. loading constraint for contingencies: Separate constraint type"
    isSepCntMaxAllowedLoading: int
    "Max. loading constraint for contingencies: Separate max. allowed loading"
    ldc_deadband: float
    "Controller, tap changer: Deadband"
    ldc_lmlow: float
    "Controller, tap changer: Lower"
    ldc_lmup: float
    "Controller, tap changer: Upper"
    ldcct: float
    "Controller, tap changer: Current transformer rating"
    ldcpt: float
    "Controller, tap changer: Voltage transformer ratio"
    ldcrs: float
    "Controller, tap changer: Rset"
    ldcrsRev: float
    "Reverse power operation: Rset"
    ldcrxcomp: int
    "Controller, tap changer: Internally adjust Rset, Xset for closed- and open-delta configurations"
    ldcxs: float
    "Controller, tap changer: Xset"
    ldcxsRev: float
    "Reverse power operation: Xset"
    lifeSpan: float
    "Expected life span"
    loc_name: str
    "Name"
    lossAssign: int
    "Loss assignment:according to grouping:uniformly distributed:to S-Side:to L-Side"
    maintenCost: float
    "Costs: Maintenance costs"
    maxload: float
    "Thermal loading limit: Max. loading"
    nntap1: int
    "Tap changer: Tap 1 position"
    nntap2: int
    "Tap changer: Tap 2 position"
    nntap3: int
    "Tap changer: Tap 3 position"
    ntrcn: int
    "Controller, tap changer: Automatic tap changing"
    oid_: int
    "ObjectID"
    originalValue: float
    "Original value"
    outserv: int
    "Out of Service"
    pMeteo: object
    "Meteo. Station"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pRating: object
    "Thermal rating"
    pStoch: object
    "Failures: Element model"
    pTypStoch: object
    "Failures: Type model"
    pcReglim: int
    "Tap changer: Limit (in % of max. range):100%:87.5%:75%:62.5%:50%"
    pcReglimMin: int
    "Tap changer: Limit (in % of max. range):100%:87.5%:75%:62.5%:50%"
    penaltyCosts: float
    "Controls for Optimal Power Flow: Penalty costs per Tap deviation"
    pid_: int
    "ProjectID"
    ratfac: float
    "Rating factor"
    re0: float
    "Internal grounding impedance: Resistance, Re"
    root_id: object
    "Original Location"
    sOpComment: list
    "Operator comment"
    scalingFacSoftConstrCost: float
    "Penalty costs for soft constraints: Cost scaling factor"
    scalingFacSoftConstrOpf: float
    "Max. loading constraint: Weighting factor for soft constraint penalty"
    scrapValue: float
    "Scrap value"
    sernum: str
    "Serial Number"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    usetp: float
    "Controller, tap changer: Voltage setpoint"
    usetpRev: float
    "Reverse power operation: Voltage setpoint"
    usp_low: float
    "Controller, tap changer: Lower voltage bound"
    usp_lowRev: float
    "Reverse power operation: Lower voltage bound"
    usp_up: float
    "Controller, tap changer: Upper voltage bound"
    usp_upRev: float
    "Reverse power operation: Upper voltage bound"
    xe0: float
    "Internal grounding impedance: Reactance, Xe"

    def AttributeType(*args): ...

    def CreateEvent(*args): ...

    def GetGroundingImpedance(*args): ...

    def GetZpu(*args): ...

    def HasReferences(*args): ...

    def NTap(*args): ...

    def __getattr__(*args): ...


class ElmXnet(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Irze: list
    "Rated Current of Grounding"
    K: float
    "Operation Point: Secondary Frequency Bias"
    Kpf: float
    "Operation Point: Primary Frequency Bias"
    L0: float
    "Frequency Dependencies: Inductance, L0"
    L1: float
    "Frequency Dependencies: Inductance, L1"
    L2: float
    "Frequency Dependencies: Inductance, L2"
    MaxS: float
    "Active Power Operational Limits: Max."
    Pctrl: int
    "Active power control: Active power steps:fixed:continuous:1:2:3:4:5:6:7:8:9:10"
    PmaxInv: float
    "Separate consumption mode: Max."
    PmaxInvPU: float
    "Separate consumption mode: Max."
    Pmax_ucPU: float
    "Active Power Operational Limits: Max."
    PminInv: float
    "Separate consumption mode: Min."
    PminInvPU: float
    "Separate consumption mode: Min."
    Pmin_uc: float
    "Active Power Operational Limits: Min."
    Pmin_ucPU: float
    "Active Power Operational Limits: Min."
    Pnom: float
    "Active Power Operational Limits: Pn"
    QtargetBase: int
    "Optimisation of reactive power reserve: Base:Reactive power limits:Rated apparent power"
    QtargetRPR: float
    "Optimisation of reactive power reserve: Q target value"
    R0: float
    "Frequency Dependencies: Resistance, R0"
    R1: float
    "Frequency Dependencies: Resistance, R1"
    R2: float
    "Frequency Dependencies: Resistance, R2"
    Re: float
    "Internal Grounding Impedance: Resistance, Re"
    SkV: float
    "Short-Circuit Power at Normal Operation: Short-Circuit Power, Sk"
    Xe: float
    "Internal Grounding Impedance: Reactance, Xe"
    aCategory: str
    "Plant Category"
    allowConsumMode: int
    "Separate consumption mode"
    allowGenMode: int
    "Separate generation mode"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    avgCosts: float
    "Average Costs"
    avgCostsUc: float
    "Piecewise linearisation for LP: Average costs"
    bus1: object
    "Terminal"
    bus1n: object
    "Neutral Conductor: Neutral"
    bustp: str
    "Bus Type:PQ:PV:SL"
    cCategory: str
    "Plant Category"
    cDisplayName: str
    "Display Name"
    cIsDiscreteCtrlP: int
    "Restriction to discrete active power values"
    cIsMustRunUC: int
    "Additional constraints for controls: Must run"
    cIsPcurrAllowed: int
    "Allow current active power value"
    cQ_max: float
    "Reactive Power Operational Limits: Max."
    cQ_min: float
    "Reactive Power Operational Limits: Min."
    cStorage: object
    "Generator usage: Storage model"
    cUserDefIndex: int
    "User defined Index"
    cVecDiscreteCtrlPvals: list
    "Valid active power values"
    c_psecc: object
    "External Secondary Controller"
    c_pstac: object
    "External Station Controller"
    ccost: list
    "Costs"
    cfixedCosts: float
    "Operating costs: Fixed costs"
    cfreqs: float
    "Frequency"
    cgnd: int
    "Internal Grounding Impedance: Star Point:Connected:Not connected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cmax: float
    "Max. Values: c-Factor (max.)"
    cmin: float
    "Min. Values: c-Factor (min.)"
    cmonth: float
    "No load costs (monthly)"
    coldStartTime: float
    "Start-up costs: Cold-start time"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    consumCosts: float
    "Consumption mode: Consumption costs"
    cosgini: float
    "Operation Point: Power Factor"
    cosn: float
    "Power Factor"
    cospreld: float
    "Max. Values Preload Conditions: Power Factor"
    cospreldmin: float
    "Min. Values Preload Conditions: Power Factor"
    costColdStart: float
    "Start-up costs: Cold-start costs"
    costCurtailment: float
    "Costs for curtailment"
    costRedispatchDown: float
    "Additional redispatch costs: Downward active power redispatch costs"
    costRedispatchP: float
    "Redispatch costs for active power change"
    costRedispatchQ: float
    "Redispatch costs for reactive power change"
    costRedispatchUp: float
    "Additional redispatch costs: Upward active power redispatch costs"
    costShutDown: float
    "Shut-down costs"
    cost_up: float
    "Start-up costs: Warm-start costs"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpCtrlNode: object
    "Operation Point: Target Node"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cpeter: int
    "Internal Grounding Impedance: Petersen Coil"
    cpower: list
    "From"
    curpreld: float
    "Max. Values Preload Conditions: Current"
    curpreldmin: float
    "Min. Values Preload Conditions: Current"
    cused: int
    "Use for calculation"
    cusedhrm: int
    "Use for calculation"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    discMethCostOp: int
    "Piecewise linearisation for LP"
    dispatch: int
    "Generator Dispatch"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    ecost: float
    "Energy Cost"
    efficiencyCurveConsum: object
    "Efficiency: Efficiency curve (consumption)"
    efficiencyCurveGen: object
    "Efficiency: Efficiency curve (generation)"
    efficiencyLPconsum: float
    "Efficiency: Used efficiency (consumption)"
    efficiencyLPgen: float
    "Efficiency: Used efficiency (generation)"
    fcharL0: object
    "Frequency Dependencies: L0(f)"
    fcharL1: object
    "Frequency Dependencies: L1(f)"
    fcharL2: object
    "Frequency Dependencies: L2(f)"
    fcharR0: object
    "Frequency Dependencies: R0(f)"
    fcharR1: object
    "Frequency Dependencies: R1(f)"
    fcharR2: object
    "Frequency Dependencies: R2(f)"
    fixed: int
    "Must run"
    fixedCosts: float
    "Generation costs: Fixed costs"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    genShiftKey: float
    "Generation shift key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iHmcType: int
    "Type of Harmonic Voltages"
    iInterPol: int
    "Approximation:Piecewise linear:Hermite"
    iOPFCPmax: int
    "Active Power Operational Limits: Max."
    iOPFCPmin: int
    "Active Power Operational Limits: Min."
    iOPFCQmax: int
    "Reactive Power Operational Limits: Max."
    iOPFCQmin: int
    "Reactive Power Operational Limits: Min."
    iSchemeStatus: int
    "Scheme Status"
    i_prty: int
    "Active power control: Priority"
    ictpg: int
    "Controls: Active Power"
    ictqg: int
    "Controls: Reactive Power"
    ifreqs: list
    "Harm. Order"
    ifreqs_iec2: list
    "Harm. Order"
    ignd: int
    "Star Point:grounded:compensated:isolated"
    iintgnd: int
    "Neutral Conductor: N-Connection:None:At terminal (ABC-N):Separate terminal"
    ikss: float
    "Max. Values: Short-Circuit Current Ik''max"
    ikssmin: float
    "Min. Values: Short-Circuit Current Ik''min"
    ip_ctrl: int
    "Secondary Controller (Slack)"
    is4SpinReserve: int
    "Consider for region spinning reserve"
    isConsCostOp: int
    "Operating costs"
    isConsCostsRedispatch: int
    "Additional redispatch costs"
    isConsShutDownCost: int
    "Shut-down costs"
    isConsStartUpCost: int
    "Start-up costs"
    isConstrRamp: int
    "Ramp rate constraints"
    isConstrUpDown: int
    "Start-up/shut-down time constraints"
    isCtrlFixedToLdfVal: int
    "Additional constraints for controls: Fix controls to Load Flow values"
    isCtrlP: int
    "Controls: Active power"
    isCtrlPplacement: int
    "Optimise active power"
    isCtrlQ: int
    "Controls: Reactive power"
    isDiscreteCtrlP: int
    "Restriction to discrete active power values"
    isLimPmax: int
    "Active Power Operational Limits: Max."
    isLimPmin: int
    "Active Power Operational Limits: Min."
    isLimQmax: int
    "Reactive Power Operational Limits: Max."
    isLimQmin: int
    "Reactive Power Operational Limits: Min."
    isMustRunUC: int
    "Additional constraints for controls: Must run"
    isPcurrAllowed: int
    "Restriction to discrete active power values: Allow current active power value"
    isRPR: int
    "Optimisation of reactive power reserve"
    isVRE: int
    "Generator usage: Generator usage:Single thermal generation unit:Variable renewable energy source (VRE):Coupled with storage model:Part of Virtual Power Plant"
    iv_mode: int
    "Voltage Controller Mode"
    limRampDown: float
    "Ramp rate constraints: Ramp-down limit"
    limRampDownPU: float
    "Ramp rate constraints: Ramp-down limit"
    limRampShutDown: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampShutDownPU: float
    "Ramp rate constraints: Shut-down ramp limit"
    limRampStartUp: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampStartUpPU: float
    "Ramp rate constraints: Start-up ramp limit"
    limRampUp: float
    "Ramp rate constraints: Ramp-up limit"
    limRampUpPU: float
    "Ramp rate constraints: Ramp-up limit"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    minDownTime: float
    "Start-up/shut-down time constraints: Minimum down-time"
    minUpTime: float
    "Start-up/shut-down time constraints: Minimum up-time"
    mode_inp: str
    "Operation Point: Input Mode"
    numBreakpointsCostOp: int
    "Piecewise linearisation for LP: Number of breakpoints"
    oid_: int
    "ObjectID"
    outServPzero: int
    "Out of service when active power is zero"
    outserv: int
    "Out of Service"
    pBMU: object
    "Virtual Power Plant"
    pOpCostCurve: object
    "Operating costs: Generator cost curve"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pQlimType: object
    "Reactive Power Operational Limits: Capability Curve"
    pStorage: object
    "Storage model"
    p_direc: int
    "Operation Point: Power Direction:P>=0:P<0"
    p_uctrl: object
    "Operation Point: Reference Busbar"
    penaltyCosts: float
    "Penalty costs"
    pf_recap: int
    "Operation Point: Power Factor:ind.:cap."
    pgini: float
    "Operation Point: Active Power"
    phiini: float
    "Operation Point: Angle"
    pid_: int
    "ProjectID"
    priority: int
    "Merit Order"
    psikV: float
    "Short-Circuit Power at Normal Operation: Impedance Angle, psik"
    q_max: float
    "Max."
    q_min: float
    "Min."
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qgini: float
    "Operation Point: Reactive Power"
    r0tx0: float
    "R0/X0 max."
    r0tx0kV: float
    "Short-Circuit Power at Normal Operation: R0/X0"
    r0tx0min: float
    "R0/X0 min."
    rntxn: float
    "Max. Values: R/X Ratio (max.)"
    rntxnmin: float
    "Min. Values: R/X Ratio (min.)"
    root_id: object
    "Original Location"
    round: float
    "Smoothing factor"
    sOpComment: list
    "Operator Comment"
    scaleQmax: float
    "Reactive Power Operational Limits: Scaling Factor (max.)"
    scaleQmin: float
    "Reactive Power Operational Limits: Scaling Factor (min.)"
    sernum: str
    "Serial Number"
    sgini: float
    "Operation Point: Apparent Power"
    snom: float
    "Nominal Apparent Power"
    snss: float
    "Max. Values: Short-Circuit Power Sk''max"
    snssmin: float
    "Min. Values: Short-Circuit Power Sk''min"
    tag: float
    "Acceleration Time Constant"
    tds: float
    "Transient Time Constants: Td'"
    tdss: float
    "Subtransient Time Constants: Td''"
    tid_: int
    "TimeID"
    tqs: float
    "Transient Time Constants: Tq'"
    tqss: float
    "Subtransient Time Constants: Tq''"
    u0_mag: list
    "u0, Mag."
    u0_phase: list
    "u0, Ang."
    u1_mag: list
    "u1, Mag."
    u1_phase: list
    "u1, Ang."
    u2_mag: list
    "u2, Mag."
    u2_phase: list
    "u2, Ang."
    umag_iec1: list
    "U_h"
    umag_iec2: list
    "U_h"
    uset_mode: int
    "Setpoint:local:bus target voltage"
    usetp: float
    "Operation Point: Voltage Setpoint"
    vecBreakpointsP: list
    "Piecewise linearisation for LP: Power"
    vecCostRedispatchDown: list
    "Costs"
    vecCostRedispatchUp: list
    "Costs"
    vecDiscreteCtrlPvals: list
    "Restriction to discrete active power values: Valid active power values"
    vecPowerRedispatchDown: list
    "Redispatch"
    vecPowerRedispatchUp: list
    "Redispatch"
    vecStartUpCosts: list
    "Start-up costs: Start-up costs"
    vecStartUpTimes: list
    "Start-up costs: Down-time"
    x0tx1: float
    "Max. Values Impedance Ratio: X0/X1 max."
    x0tx1kV: float
    "Short-Circuit Power at Normal Operation: X0/X1"
    x0tx1min: float
    "Min. Values Impedance Ratio: X0/X1 min."
    xd: float
    "Synchronous Reactances: xd"
    xds: float
    "Transient Reactances: xd'"
    xntrn: float
    "Max. Values: X/R Ratio (max.)"
    xntrnmin: float
    "Min. Values: X/R Ratio (min.)"
    xq: float
    "Synchronous Reactances: xq"
    xqs: float
    "Transient Reactances: xq'"
    z2tz1: float
    "Max. Values Impedance Ratio: Z2/Z1 max."
    z2tz1kV: float
    "Short-Circuit Power at Normal Operation: Z2/Z1"
    z2tz1min: float
    "Min. Values Impedance Ratio: Z2/Z1 min."

    def AttributeType(*args): ...

    def CalcEfficiency(*args): ...

    def Disconnect(*args): ...

    def GetGroundingImpedance(*args): ...

    def GetStepupTransformer(*args): ...

    def HasReferences(*args): ...

    def Reconnect(*args): ...

    def __getattr__(*args): ...


class ElmZone(PFGeneral):
    InterPset: float
    "Consider Interchange Schedule: Scheduled Active Power Interchange"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cimRdfId: list
    "RDF ID"
    cpHeadFold: object
    "Head Folder"
    curscale: float
    "Load Scaling Factor"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iInterChg: int
    "Consider Interchange Schedule"
    iSchemeStatus: int
    "Scheme Status"
    icolor: int
    "Colour"
    isConsSpinReserve: int
    "Min. spinning reserve constraint"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    spinReserve: float
    "Min. spinning reserve constraint: Spinning reserve"
    tid_: int
    "TimeID"
    windscale: float
    "Wind Generation Scaling Factor"

    def AttributeType(*args): ...

    def CalculateInterchangeTo(*args): ...

    def CalculateVoltInterVolt(*args): ...

    def CalculateVoltageLevel(*args): ...

    def DefineBoundary(*args): ...

    def GetAll(*args): ...

    def GetBranches(*args): ...

    def GetBuses(*args): ...

    def GetObjs(*args): ...

    def HasReferences(*args): ...

    def SetLoadScaleAbsolute(*args): ...

    def __getattr__(*args): ...


class StaCt(PFGeneral):
    Rs: float
    "Detailed Model: Sec. Winding Resistance"
    Sburd: float
    "Detailed Model Actual Burden: Apparent Power"
    Vs: float
    "Detailed Model Saturation Parameter: Saturation Voltage"
    Zburd: float
    "Detailed Model Actual Burden: Impedance"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bmsat: float
    "Detailed Model Saturation Parameter: Saturated Admittance"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    cbranch: object
    "Location: Branch"
    ccratio: str
    "Additional Cores: Complete Ratio"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    ciorient: int
    "Configuration: Orientation:--> Branch:--> Busbar"
    cn_bus: object
    "Location: Busbar"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cosburd: float
    "Detailed Model Actual Burden: Power Factor"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cratio: str
    "Additional Cores: Ratio"
    cratio_ct: str
    "Additional Cores: Complete ratio, CT"
    curmg: float
    "Detailed Model Saturation Parameter: (Exc. current)/(Rated current)"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iComDate: int
    "Commissioning Date"
    iSchemeStatus: int
    "Scheme Status"
    iconsat: int
    "Detailed Model"
    iorient: int
    "Orientation:--> Branch:--> Busbar"
    iphase: int
    "Configuration: No. Phases:1:2:3"
    it2p1: int
    "Configuration: Phase 1"
    it2p2: int
    "Configuration: Phase 2:a:b:c"
    itrmt: int
    "Detailed Model: Saturation Model"
    ksat: float
    "Detailed Model Saturation Parameter: Exponent"
    loc_name: str
    "Name"
    nameplate: str
    "Nameplate"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pbranch: object
    "Location: Reference"
    pid_: int
    "ProjectID"
    ptapset: float
    "Tap selection: Primary"
    root_id: object
    "Original Location"
    rphase: int
    "Configuration: Phase rotation:a-b-c:b-c-a:c-a-b:b-a-c:c-b-a:a-c-b"
    seccts: list
    "Additional Cores"
    sernum: str
    "Serial Number"
    stapcon: str
    "Configuration: Connection:Y:D"
    stapset: float
    "Tap selection: Secondary"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    vec_core: list
    "Additional Cores"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def SetPrimaryTap(*args): ...

    def __getattr__(*args): ...


class StaCubic(PFGeneral):
    actPhase: str
    "Actual phase(s)"
    cBrkmea: object
    cBusBar: object
    "Connected Node"
    cDisplayName: str
    "Display Name"
    cImea: object
    cMajorNodes: list
    "Connected Major Nodes"
    cPhInfo: str
    "Phases:"
    cPmea: object
    cQmea: object
    cTapmea: object
    cUserDefIndex: int
    "User defined Index"
    cVmea: object
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpCB: object
    "Circuit-Breaker"
    cpCts: object
    "Current Transformer"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpRelays: object
    "Relays"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cterm: object
    "Terminal"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    elm_brc: object
    "Connected with element or branch"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iNode: int
    "node number for internal station topology"
    iSchemeStatus: int
    "Scheme Status"
    iStopFeed: int
    "Terminate feeder at this point"
    iType: int
    "internal used for position"
    it2p1: int
    "Phase 1"
    it2p2: int
    "Phase 2"
    it2p3: int
    "Phase 3"
    loc_name: str
    "Name"
    nphase: int
    "No of Phases:"
    obj_bus: int
    "Bus Index"
    obj_id: object
    "Connected with"
    obj_out: object
    "Connected with"
    oid_: int
    "ObjectID"
    pIntObjs: list
    "Internal Elements"
    pNodeStat: object
    "Station or terminal"
    pid_: int
    "ProjectID"
    position: int
    "Position"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def GetAll(*args): ...

    def GetBranch(*args): ...

    def GetConnectedMajorNodes(*args): ...

    def GetConnections(*args): ...

    def GetNearestBusbars(*args): ...

    def GetPathToNearestBusbar(*args): ...

    def HasReferences(*args): ...

    def IsClosed(*args): ...

    def IsConnected(*args): ...

    def __getattr__(*args): ...


class StaExtbrkmea(PFGeneral):
    Ext: list
    "Measurement: External"
    Int: list
    "Measurement: Internal"
    Swtmea: int
    "Measurement: Position"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cswitch: object
    "Effective Meas. Element"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    i_use: int
    "Measurement: Use"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pid_: int
    "ProjectID"
    pswitch: object
    "Remote Measurement Point"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtcmdmea(PFGeneral):
    Cal: float
    "Measurement: Calc."
    Mea: str
    "Measurement: Command"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    ccubic: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCalObj: object
    "Get calculated value from: Object"
    pCalObjSim: object
    "Get calculated value from: Sim Object"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pcubic: object
    "Remote Measurement Point"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varCal: str
    "Get calculated value from: Variable Name"
    varCalSim: str
    "Get calculated value from: Variable Name"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def CreateEvent(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtdatmea(PFGeneral):
    Cal: float
    "Measurement: Calc."
    CalVal: float
    "Calculated Value, internal"
    CalValExt: float
    "Calculated Value, external"
    Dif: float
    "Measurement: Deviation"
    Ext: list
    "Measurement: External"
    Int: list
    "Measurement: Internal"
    Mea: float
    "Measurement: Raw Value"
    Multip: float
    "Measurement: Multiplicator"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cMeaVal: float
    "Measurement: Measurement Value"
    cUserDefIndex: int
    "User defined Index"
    ccubic: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deadband: float
    "Measurement: OPC deadband"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    i_dat: int
    "Measurement: DAT type"
    i_mode: int
    "Measurement: Mode"
    i_use: int
    "Measurement: Use"
    iopt_execCom: int
    "Get calculated value from: Execute Command"
    iopt_execComSim: int
    "Get calculated value from: Execute Command"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCalObj: object
    "Get calculated value from: Object"
    pCalObjSim: object
    "Get calculated value from: Sim Object"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pcubic: object
    "Remote Measurement Point"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varCal: str
    "Get calculated value from: Variable Name"
    varCalSim: str
    "Get calculated value from: Variable Name"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def CreateEvent(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtfmea(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cMeaVal: float
    "Measurement: Measurement Value"
    cUserDefIndex: int
    "User defined Index"
    cbusbar: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deadband: float
    "Measurement: OPC deadband"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    errBadData: int
    "Detailed Error Description: Bad measurement"
    errConsDir: int
    "Detailed Error Description: Consistent active power flow direction at each side of branch"
    errOutOfService: int
    "Detailed Error Description: Measurement out of service"
    errRedundant: int
    "Detailed Error Description: Redundant measurement for observability"
    errStatus: int
    "Detailed Error Description: Input status of measurement disallows calculation"
    errUnneededPseudo: int
    "Detailed Error Description: Unneeded pseudo-measurement"
    error: int
    "Error description Code"
    fcal: float
    "Measurement: Calc. Frequency"
    fdif: float
    "Measurement: Frequency Deviation"
    fmea: float
    "Measurement: Frequency"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pbusbar: object
    "Remote Measurement Point"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtfuelmea(PFGeneral):
    Fuelcal: float
    "Measurement: Calc. Fuel"
    Fueldif: float
    "Measurement: Fuel Deviation"
    Fuelmea: float
    "Measurement: Fuel"
    Multip: float
    "Measurement: Multiplicator"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cMeaVal: float
    "Measurement: Measurement Value"
    cUserDefIndex: int
    "User defined Index"
    ccubic: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pcubic: object
    "Remote Measurement Point"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtimea(PFGeneral):
    IActcal: float
    "Calc. Act. Curr."
    IActdif: float
    "Act. Curr. Dev. (rated)"
    IActdif_abs: float
    "Act. Curr. Dev. (abs)"
    IActdif_mea: float
    "Act. Curr. Dev. (meas.)"
    IMagncal: float
    "Calc. Curr. Magn."
    IMagndif: float
    "Curr. Magn. Dev. (rated)"
    IMagndif_abs: float
    "Curr. Magn. Dev. (abs)"
    IMagndif_mea: float
    "Curr. Magn. Dev. (meas.)"
    IReactcal: float
    "Calc. React. Curr."
    IReactdif: float
    "React. Curr. Dev. (rated)"
    IReactdif_abs: float
    "React. Curr. Dev. (abs)"
    IReactdif_mea: float
    "React. Curr. Dev. (meas.)"
    Imea: float
    "Measurement: Current"
    Multip: float
    "Measurement: Multiplicator"
    RedundanceGrpAct: int
    "Detailed Error Description: Equivalence class (active current measure)"
    RedundanceGrpMagn: int
    "Detailed Error Description: Redundancy equivalence class (magnitude measure)"
    RedundanceGrpReact: int
    "Detailed Error Description: Equivalence class (reactive current measure)"
    RedundanceLevelAct: int
    "Detailed Error Description: Level of redundancy (active current measure)"
    RedundanceLevelMagn: int
    "Detailed Error Description: Level of redundancy (magnitude measure)"
    RedundanceLevelReact: int
    "Detailed Error Description: Level of redundancy (reactive current measure)"
    Snom: float
    "Rated Current"
    SnomAct: float
    "Ratings Active Current: Rated Current"
    SnomMagn: float
    "Ratings Current, Magnitude: Rated Current"
    SnomReact: float
    "Ratings Reactive Current: Rated Current"
    accuracy: float
    "Accuracy Class"
    accuracyAct: float
    "Ratings Active Current: Accuracy Class"
    accuracyMagn: float
    "Ratings Current, Magnitude: Accuracy Class"
    accuracyReact: float
    "Ratings Reactive Current: Accuracy Class"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cIsValid: int
    "Is Valid"
    cMeaValAct: float
    "Mea. Act. Curr."
    cMeaValMagn: float
    "Mea. Curr. Magn."
    cMeaValReact: float
    "Mea. React. Curr."
    cObjFun: float
    "Objective function"
    cObjFunAct: float
    "Obj. func. act"
    cObjFunMagn: float
    "Obj. func. magn."
    cObjFunReact: float
    "Obj. func. react"
    cUserDefIndex: int
    "User defined Index"
    ccubic: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cosphi: float
    "Measurement: Power Factor"
    cosphical: float
    "Calc. Power Factor"
    cosphidif: float
    "Power Factor Deviation"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deadband: float
    "Measurement: OPC deadband"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    errBadData: int
    "Detailed Error Description: Bad measurement"
    errBadDataAct: int
    "Detailed Error Description: Bad active current measure"
    errBadDataMagn: int
    "Detailed Error Description: Bad magnitude measure"
    errBadDataReact: int
    "Detailed Error Description: Bad reactive current measure"
    errConsDir: int
    "Detailed Error Description: Consistent active power flow direction at each side of branch"
    errExcNomLoading: int
    "Detailed Error Description: Branch loadings exceed nominal values"
    errExcNomLoss: int
    "Detailed Error Description: Large branch losses"
    errFlwIfOpn: int
    "Detailed Error Description: Large branch flows on open ended branches"
    errNdSumP: int
    "Detailed Error Description: Node sum checks for P"
    errNdSumQ: int
    "Detailed Error Description: Node sum checks for Q"
    errNegLoss: int
    "Detailed Error Description: Negative losses on passive branches"
    errOutOfService: int
    "Detailed Error Description: Measurement out of service"
    errRedundant: int
    "Detailed Error Description: Redundant measurement for observability"
    errRedundantAct: int
    "Detailed Error Description: Redundant active current measure"
    errRedundantMagn: int
    "Detailed Error Description: Redundant magnitude measure"
    errRedundantReact: int
    "Detailed Error Description: Redundant reactive current measure"
    errStatus: int
    "Detailed Error Description: Input status of measurement disallows calculation"
    errUnneededPseudo: int
    "Detailed Error Description: Unneeded pseudo-measurement"
    error: int
    "Error description Code"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    iUseAct: int
    "Usage: Measure Active Current"
    iUseMagn: int
    "Usage: Measure Current Magnitude"
    iUseReact: int
    "Usage: Measure Reactive Current"
    i_gen: int
    "Measurement: Orientation"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pcubic: object
    "Remote Measurement Point"
    pf_recapr: int
    "Measurement: Power Factor:ind.:cap."
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtpfmea(PFGeneral):
    Multip: float
    "Measurement: Multiplicator"
    Pfcal: float
    "Measurement: Calc. Power Factor"
    Pfdif: float
    "Measurement: Pow. Factor Deviat."
    Pfmea: float
    "Measurement: Power Factor"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cMeaVal: float
    "Measurement: Measurement Value"
    cUserDefIndex: int
    "User defined Index"
    ccubic: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    i_gen: int
    "Measurement: Orientation"
    iopt_mea: int
    "Measurement Of"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pcubic: object
    "Remote Measurement Point"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtpmea(PFGeneral):
    Multip: float
    "Measurement: Multiplicator"
    Pcal: float
    "Measurement: Calc. Active Power"
    Pdif: float
    "Measurement: Power Deviation (rated)"
    Pdif_abs: float
    "Measurement: Power Deviation (abs)"
    Pdif_mea: float
    "Measurement: Power Deviation (meas.)"
    Pmea: float
    "Measurement: Active Power"
    RedundanceGrp: int
    "Detailed Error Description: Equivalence class (of redundant measure)"
    RedundanceLevel: int
    "Detailed Error Description: Level of redundancy"
    Snom: float
    "Ratings: Power Rating"
    accuracy: float
    "Ratings: Accuracy Class"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cIsValid: int
    "Is Valid"
    cMeaVal: float
    "Measurement: Measurement Value"
    cObjFun: float
    "Measurement: Objective function"
    cUserDefIndex: int
    "User defined Index"
    ccubic: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deadband: float
    "Measurement: OPC deadband"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    errBadData: int
    "Detailed Error Description: Bad measurement"
    errConsDir: int
    "Detailed Error Description: Consistent active power flow direction at each side of branch"
    errExcNomLoading: int
    "Detailed Error Description: Branch loadings exceed nominal values"
    errExcNomLoss: int
    "Detailed Error Description: Large branch losses"
    errFlwIfOpn: int
    "Detailed Error Description: Large branch flows on open ended branches"
    errNdSumP: int
    "Detailed Error Description: Node sum checks for P"
    errNdSumQ: int
    "Detailed Error Description: Node sum checks for Q"
    errNegLoss: int
    "Detailed Error Description: Negative losses on passive branches"
    errOutOfService: int
    "Detailed Error Description: Measurement out of service"
    errRedundant: int
    "Detailed Error Description: Redundant measurement for observability"
    errStatus: int
    "Detailed Error Description: Input status of measurement disallows calculation"
    errUnneededPseudo: int
    "Detailed Error Description: Unneeded pseudo-measurement"
    error: int
    "Error description Code"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    i_gen: int
    "Measurement: Orientation"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pcubic: object
    "Remote Measurement Point"
    pid_: int
    "ProjectID"
    pseudo: int
    "Used as Pseudo-Measurement"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtqmea(PFGeneral):
    Multip: float
    "Measurement: Multiplicator"
    Qcal: float
    "Measurement: Calc. React. Power"
    Qdif: float
    "Measurement: Power Deviation (rated)"
    Qdif_abs: float
    "Measurement: Power Deviation (abs)"
    Qdif_mea: float
    "Measurement: Power Deviation (meas.)"
    Qmea: float
    "Measurement: Reactive Power"
    RedundanceGrp: int
    "Detailed Error Description: Equivalence class (of redundant measure)"
    RedundanceLevel: int
    "Detailed Error Description: Level of redundancy"
    Snom: float
    "Ratings: Power Rating"
    accuracy: float
    "Ratings: Accuracy Class"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cIsValid: int
    "Is Valid"
    cMeaVal: float
    "Measurement: Measurement Value"
    cObjFun: float
    "Measurement: Objective function"
    cUserDefIndex: int
    "User defined Index"
    ccubic: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deadband: float
    "Measurement: OPC deadband"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    errBadData: int
    "Detailed Error Description: Bad measurement"
    errConsDir: int
    "Detailed Error Description: Consistent active power flow direction at each side of branch"
    errExcNomLoading: int
    "Detailed Error Description: Branch loadings exceed nominal values"
    errExcNomLoss: int
    "Detailed Error Description: Large branch losses"
    errFlwIfOpn: int
    "Detailed Error Description: Large branch flows on open ended branches"
    errNdSumP: int
    "Detailed Error Description: Node sum checks for P"
    errNdSumQ: int
    "Detailed Error Description: Node sum checks for Q"
    errNegLoss: int
    "Detailed Error Description: Negative losses on passive branches"
    errOutOfService: int
    "Detailed Error Description: Measurement out of service"
    errRedundant: int
    "Detailed Error Description: Redundant measurement for observability"
    errStatus: int
    "Detailed Error Description: Input status of measurement disallows calculation"
    errUnneededPseudo: int
    "Detailed Error Description: Unneeded pseudo-measurement"
    error: int
    "Error description Code"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    i_gen: int
    "Measurement: Orientation"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pcubic: object
    "Remote Measurement Point"
    pid_: int
    "ProjectID"
    pseudo: int
    "Used as Pseudo-Measurement"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtsmea(PFGeneral):
    Serr: float
    "Error"
    Sldf: float
    "Last Calculated"
    Smea: float
    "Apparent Power"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    ccubic: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pcubic: object
    "Remote Measurement Point"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExttapmea(PFGeneral):
    Exttap: list
    "Ext. Tap"
    Tap: list
    "Measurement: PF Tap"
    Tapcal: float
    "Measurement: Calc. Tap"
    Tapmea: int
    "Measurement: Tap position"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cobject: object
    "Effective Meas. Element"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    i_tap: int
    "Operation Mode"
    i_tapCmd: int
    "Tap Changer Command"
    i_tapOpCh: int
    "Tap Operation Mode"
    i_tapOpCmd: int
    "Tap Operation Mode Cmd."
    loc_name: str
    "Name"
    obj_bus: int
    "Bus Index"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pid_: int
    "ProjectID"
    pobject: object
    "Remote Measurement Point"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def CreateEvent(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtv3mea(PFGeneral):
    Multip1: float
    "Measurement 1 (L1-L2): Multiplicator"
    Multip2: float
    "Measurement 2 (L2-L3): Multiplicator"
    Multip3: float
    "Measurement 3 (L3-L1): Multiplicator"
    Ucal1: float
    "Measurement 1 (L1-L2): Calc. Voltage"
    Ucal2: float
    "Measurement 2 (L2-L3): Calc. Voltage"
    Ucal3: float
    "Measurement 3 (L3-L1): Calc. Voltage"
    Udif1: str
    "Measurement 1 (L1-L2): Voltage Deviation"
    Udif2: str
    "Measurement 2 (L2-L3): Voltage Deviation"
    Udif3: str
    "Measurement 3 (L3-L1): Voltage Deviation"
    Umea1: float
    "Measurement 1 (L1-L2): Measured Voltage"
    Umea2: float
    "Measurement 2 (L2-L3): Measured Voltage"
    Umea3: float
    "Measurement 3 (L3-L1): Measured Voltage"
    UmeaTag1: str
    "Measurement 1 (L1-L2): TagName 1"
    UmeaTag2: str
    "Measurement 2 (L2-L3): TagName 2"
    UmeaTag3: str
    "Measurement 3 (L3-L1): TagName 3"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cMeaVal1: float
    "Measurement 1 (L1-L2): Measurement Value"
    cMeaVal2: float
    "Measurement 2 (L2-L3): Measurement Value"
    cMeaVal3: float
    "Measurement 3 (L3-L1): Measurement Value"
    cUserDefIndex: int
    "User defined Index"
    cbusbar: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus1: int
    "Status: Status"
    iStatus2: int
    "Status: Status"
    iStatus3: int
    "Status: Status"
    iUse1: int
    "Use"
    iUse2: int
    "Use"
    iUse3: int
    "Use"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pbusbar: object
    "Remote Measurement Point"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaExtvmea(PFGeneral):
    Multip: float
    "Measurement: Multiplicator"
    RedundanceGrp: int
    "Detailed Error Description: Equivalence class (of redundant measure)"
    RedundanceLevel: int
    "Detailed Error Description: Level of redundancy"
    Ucal: float
    "Measurement: Calc. Voltage"
    Udif: float
    "Measurement: Voltage Deviation"
    Umea: float
    "Measurement: Measured Voltage"
    accuracy: float
    "Ratings: Accuracy Class"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cIsValid: int
    "Is Valid"
    cMeaVal: float
    "Measurement: Measurement Value"
    cObjFun: float
    "Measurement: Objective function"
    cUserDefIndex: int
    "User defined Index"
    cValueTmp: float
    "Tmp Value"
    cbusbar: object
    "Effective Meas. Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deadband: float
    "Measurement: OPC deadband"
    delSet: float
    "Deviation from Measurement"
    desc: list
    "Description"
    errBadData: int
    "Detailed Error Description: Bad measurement"
    errConsDir: int
    "Detailed Error Description: Consistent active power flow direction at each side of branch"
    errExcNomLoading: int
    "Detailed Error Description: Branch loadings exceed nominal values"
    errExcNomLoss: int
    "Detailed Error Description: Large branch losses"
    errFlwIfOpn: int
    "Detailed Error Description: Large branch flows on open ended branches"
    errNdSumP: int
    "Detailed Error Description: Node sum checks for P"
    errNdSumQ: int
    "Detailed Error Description: Node sum checks for Q"
    errNegLoss: int
    "Detailed Error Description: Negative losses on passive branches"
    errOutOfService: int
    "Detailed Error Description: Measurement out of service"
    errRedundant: int
    "Detailed Error Description: Redundant measurement for observability"
    errStatus: int
    "Detailed Error Description: Input status of measurement disallows calculation"
    errUnneededPseudo: int
    "Detailed Error Description: Unneeded pseudo-measurement"
    error: int
    "Error description Code"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iStatus: int
    "Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCtrl: object
    "Controller"
    pObject: object
    "Controlled Object"
    pbusbar: object
    "Remote Measurement Point"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sTagID: str
    "TagID"
    tid_: int
    "TimeID"
    varName: str
    "Variable Name"
    variabName: str
    "Variable Name"

    def AttributeType(*args): ...

    def CopyExtMeaStatusToStatusTmp(*args): ...

    def GetMeaValue(*args): ...

    def GetStatus(*args): ...

    def GetStatusTmp(*args): ...

    def HasReferences(*args): ...

    def InitTmp(*args): ...

    def IsStatusBitSet(*args): ...

    def IsStatusBitSetTmp(*args): ...

    def ResetStatusBit(*args): ...

    def ResetStatusBitTmp(*args): ...

    def SetMeaValue(*args): ...

    def SetStatus(*args): ...

    def SetStatusBit(*args): ...

    def SetStatusBitTmp(*args): ...

    def SetStatusTmp(*args): ...

    def UpdateControl(*args): ...

    def UpdateCtrl(*args): ...

    def __getattr__(*args): ...


class StaSwitch(PFGeneral):
    BrkIbload: float
    "Loading (Interrupting)"
    BrkIpload: float
    "Loading (Peak)"
    Brkload: float
    "Loading"
    BrkmaxIb: float
    "Max. Breaking Current"
    BrkmaxIp: float
    "Max. Peak Short-Circuit Current"
    Con1: int
    "internal node number for Connection 1"
    Con2: int
    "internal node number for Connection 2"
    Tclear: float
    "Fault Clearing Time"
    Tprot: float
    "Protection Tripping Time"
    Tswitch: float
    "Power Restoration: Time to actuate switch"
    aUsage: str
    "Switch Type"
    cConBus1: object
    "Element i"
    cConBus2: object
    "Element j"
    cDisplayName: str
    "Display Name"
    cTswitch: float
    "Power Restoration: Time to open remote controlled switch"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    ciScenarioType: int
    "Scenario Type"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpCts: object
    "Current Transformer"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpRelays: object
    "Relays"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    ctrl_type: int
    "Power Restoration: Sectionalising:Remote Controlled (Stage 1):Indicator of Short Circuit (Stage 2):Manual (Stage 3)"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deltaFlow: float
    "Max. active power change"
    deltaFlowrel: float
    "Max. active power change"
    dep_protOver: float
    "Failure Data for Protection: Unnecessary backup protection maloperation"
    desc: list
    "Description"
    fold_id: object
    "in Cubicle"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iEarth: int
    "Earthed"
    iExclRA: int
    "Excluded from Running Arrangement"
    iNeutInter: int
    "Switch interrupts neutral wire"
    iNoOpt: int
    "Exclude from optimisation"
    iNormOpenSwt: int
    "Normally open switch"
    iResDir: int
    "Power Restoration: Power Restoration:Independent of Direction:Branch to Node:Node to Branch:Do not use for power restoration"
    iRestore: int
    "Use as power restoration switch"
    iSchemeStatus: int
    "Scheme Status"
    iSep: int
    "Power Restoration: Switch can be opened during restoration"
    iUse: int
    "Type of Usage"
    idetail: int
    "Detailed for calculation"
    isclosed: int
    "Actual State:open:closed"
    limitRevFlow: int
    "Limit reversed flow"
    loc_name: str
    "Name"
    logEnvCurve: int
    "Log TRV envelope:No:For first opening event only:For all opening events"
    oid_: int
    "ObjectID"
    on_off: int
    "Closed"
    pid_: int
    "ProjectID"
    prot_fail: float
    "Failure Data for Protection: Circuit breaker fails to open"
    reclAttempts: int
    "Fault clearance: Maximum number of reclosing attempts"
    rel_hasProt: int
    "Fault clearance: Consider as switch with protection device"
    rel_hasRecl: int
    "Fault clearance: Consider as switch with automatic reclosing device"
    revFlowChk: int
    "Consider in the reversed power flow analysis"
    root_id: object
    "Original Location"
    shownValues: int
    "Value representation"
    spon_prot_f: float
    "Failure Data for Protection: Frequency of spurious protection operation"
    spon_prot_t: float
    "Independent unnecessary open: Time to close"
    t_del_a: float
    "Scatter: Phase a"
    t_del_b: float
    "Scatter: Phase b"
    t_del_c: float
    "Scatter: Phase c"
    t_del_n: float
    "Scatter: Neutral"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"

    def AttributeType(*args): ...

    def Close(*args): ...

    def HasReferences(*args): ...

    def IsClosed(*args): ...

    def IsOpen(*args): ...

    def Open(*args): ...

    def __getattr__(*args): ...


class ComAddlabel(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciLevel: float
    "Confidence Interval: Level"
    colour: int
    "Colour"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_ex: int
    "Remove existing labels"
    iopt_filt: int
    "Search window"
    iopt_var: str
    "Label"
    legend: str
    "Legend"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    stepSizeDots: int
    "Search window: Points"
    stepSizeVals: float
    "Search window: Width"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComAddon(PFGeneral):
    IntDesc: list
    "Description"
    IntExpr: list
    "Value"
    IntName: list
    "Name"
    IntType: list
    "Type"
    IntUnit: list
    "Unit"
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Variable Definitions and Script"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    key: str
    "Module Key"
    loc_name: str
    "Name"
    name: str
    "Module Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    script: object
    "Script"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CreateModule(*args): ...

    def DefineDouble(*args): ...

    def DefineDoubleMatrix(*args): ...

    def DefineDoublePerConnection(*args): ...

    def DefineDoubleVector(*args): ...

    def DefineDoubleVectorPerConnection(*args): ...

    def DefineInteger(*args): ...

    def DefineIntegerPerConnection(*args): ...

    def DefineIntegerVector(*args): ...

    def DefineIntegerVectorPerConnection(*args): ...

    def DefineObject(*args): ...

    def DefineObjectPerConnection(*args): ...

    def DefineObjectVector(*args): ...

    def DefineObjectVectorPerConnection(*args): ...

    def DefineString(*args): ...

    def DefineStringPerConnection(*args): ...

    def DeleteModule(*args): ...

    def Execute(*args): ...

    def FinaliseModule(*args): ...

    def GetActiveModule(*args): ...

    def HasReferences(*args): ...

    def ModuleExists(*args): ...

    def SetActiveModule(*args): ...

    def __getattr__(*args): ...


class ComAmpacity(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cout: object
    "Print report after calculation: Report"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dbgOn: int
    "Detailed (full output of analysed command)"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    fr_initIc: int
    "Initial current rating calculation"
    frmShc: int
    "Short-circuit duration"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iadiabshc: int
    "Calculate adiabatic short-circuit rating"
    iopt_chng: int
    "Modifications"
    iopt_cmd: int
    "Modify derating factor of lines"
    iopt_geoG: int
    "Geometric factor analytically determined"
    iopt_method: int
    "Method"
    iopt_rep: int
    "Print report after calculation"
    iopt_sel: int
    "Selection"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pRes: object
    "Results"
    p_selection: object
    "Selection: Cables"
    p_selectlay: object
    "Selection: Cable layout"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    tshc: float
    "Short-circuit duration: Duration"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def ExecuteAmpacityCalc(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComAuditlog(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    filename: str
    "File name"
    filter: int
    "Time filter for Report and Export"
    filterEndTime: int
    "Time filter for Report and Export: End time"
    filterStartTime: int
    "Time filter for Report and Export: Start time"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_command: str
    "Command"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Check(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComBoundary(PFGeneral):
    addoptions: str
    "Additional Parameters"
    bndfoldname: object
    "Target folder"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    copt_select: int
    "Boundary definition"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frm_select: int
    "Boundary composition"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iFiNet: int
    "Use fictitious border network"
    iLineDist: int
    "Choice of the border inside a branch (*.ElmBranch): Prefer the longest line modelled as distributed parameters"
    iSchemeStatus: int
    "Scheme Status"
    iopt_inter: int
    "Assign selected branch elements to interior region"
    iopt_select: int
    "Boundary definition"
    iopt_split: int
    "Define only splitting boundaries"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pBranches: object
    "Boundary composition: Selection"
    pFiBorder: object
    "Use fictitious border network: Border network"
    pRegions: object
    "Boundary composition: Selection"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetCreatedBoundaries(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComCapo(PFGeneral):
    accStates: float
    "Accuracy"
    addoptions: str
    "Additional Parameters"
    cCapAdd: float
    "After Optimisation"
    cCapAll: float
    "New Capacitors"
    cCapBef: float
    "Before Optimisation"
    cCostAftP: float
    "Power Losses"
    cCostAftT: float
    "Total"
    cCostAftV: float
    "Voltage Violations"
    cCostBefP: float
    "Power Losses"
    cCostBefT: float
    "Total"
    cCostBefV: float
    "Voltage Violations"
    cCostNwSh: float
    "Costs of new capacitors"
    cCostSavP: float
    "Power Losses"
    cCostSavT: float
    "Total"
    cCostSavV: float
    "Voltage Violations"
    caccStates: float
    "Accuracy"
    cecost: float
    "Energy Costs: Energy Cost"
    cendtime: int
    "End Time"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Available Capacitors"
    cpHeadFold: object
    "Head Folder"
    cshntmxsteps: int
    "Max.Step"
    cstarttime: int
    "Start Time"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    ecost: float
    "Energy Costs: Energy Cost"
    endtime: int
    "End Time"
    feeder: object
    "Feeder"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_anl: int
    "Sensitivity Analysis"
    iopt_app: int
    "Optimisation Approach"
    iopt_bus: int
    "Candidate Buses"
    iopt_char: int
    "Consider Load Characteristics"
    iopt_clim: int
    "Constraints: Total Reactive Power of all Capacitors"
    iopt_con: int
    "Optimisation"
    iopt_cost: int
    "Energy Costs: Take from External Grid"
    iopt_draw: int
    "Draw the installed capacitors"
    iopt_fixn: int
    "Available Capacitors"
    iopt_ldf: int
    "Network Representation"
    iopt_lev: int
    "Method"
    iopt_lims: int
    "Limit number of load states"
    iopt_meth: int
    "Method"
    iopt_newchar: int
    "Load States"
    iopt_out: int
    "Print report after optimisation"
    iopt_prob: int
    "Ignore load states with a small probability"
    iopt_trea3ph: int
    "Treatment of 3-phase capacitors"
    loc_name: str
    "Name"
    maxiter: int
    "Iteration Control: Maximum Number of Iterations"
    maxmvar: float
    "Constraints: Maximum"
    maxtime: float
    "Iteration Control: Maximum Execution Time"
    min_prob: float
    "Ignore load states with a small probability: Minimum Probability"
    num_states: int
    "Limit number of load states: Maximum number"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    percent: float
    "Candidate Buses: Candidate Buses"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    shntcost: list
    "Cost"
    shntignored: list
    "Ignored"
    shntmxsteps: list
    "Max. No. of Steps"
    shntqstep: list
    "Q per Step"
    shntswitch: list
    "Switchable"
    shnttech: list
    "Technology"
    starttime: int
    "Start Time"
    tid_: int
    "TimeID"
    tridisc: object
    "Discrete Scale and Trigger"
    vectime: object
    "Time Vector"
    vmax: float
    "Constraints: Upper Voltage Limit"
    vmaxLim: float
    "Voltage Tolerance: Higher Limit"
    vmin: float
    "Constraints: Lower Voltage Limit"
    vminLim: float
    "Voltage Tolerance: Lower Limit"
    weight: float
    "Penalty Factors for Voltage Deviation: Factor for Deviation from 1 p.u."
    weight2: float
    "Penalty Factors for Voltage Deviation: Additional Factor outside range [vmin,vmax]"

    def AttributeType(*args): ...

    def ConnectShuntToBus(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def LossCostAtBusTech(*args): ...

    def TotalLossCost(*args): ...

    def __getattr__(*args): ...


class ComCimdbexp(PFGeneral):
    addoptions: str
    "Additional Parameters"
    archiveName: list
    "Export as: Archive name"
    cFormat: list
    "Format"
    cSequence: list
    "Escape sequence"
    cValue: list
    "Value"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    escapeSequences: list
    "Sequence"
    fileName: str
    "File name"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    selectedFormats: list
    "Selected"
    selectedModels: list
    "Selected"
    sourcePath: object
    "Source data"
    targetFolder: list
    "Target folder"
    tid_: int
    "TimeID"
    zipModels: int
    "Export as"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComCimdbimp(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fileName: str
    "File name"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_target: int
    "Import into"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    targetName: str
    "Import into: Name"
    targetPath: object
    "Import into: Path"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def ImportAndConvert(*args): ...

    def __getattr__(*args): ...


class ComCimvalidate(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sourcePath: object
    "CIM Archives or Models"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetClassType(*args): ...

    def GetDescriptionText(*args): ...

    def GetInputObject(*args): ...

    def GetModel(*args): ...

    def GetModelId(*args): ...

    def GetNumberOfValidationMessages(*args): ...

    def GetObject(*args): ...

    def GetObjectId(*args): ...

    def GetProfile(*args): ...

    def GetSeverity(*args): ...

    def GetType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComConreq(PFGeneral):
    Uc_bdew: float
    "Agreed service voltage, Uc"
    Uc_dachcz: float
    "Declared supply voltage, Uc"
    Uc_vde4110: float
    "Agreed service voltage, Uc"
    addoptions: str
    "Additional Parameters"
    advLimits: int
    "Definition of limits"
    cLimits: list
    "Limit/value"
    cUnits: list
    "Unit"
    calcHrmRes: int
    "Resonances: Consideration of resonances:None:Approximate:Generalised"
    calcLoading: int
    "Loading of Network Components"
    calcMaxShc: int
    "Max. Short-Circuit Current"
    calcSVChg: int
    "Sudden Voltage Changes"
    calcVChg: int
    "Admissible Voltage Changes"
    cfrmCndTemp: int
    "User-defined conductor temperature (short-circuit)"
    cfrmSkvCalc: int
    "Network short-circuit power and impedance angle calculation"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    condTempHv: float
    "User-defined conductor temperature (short-circuit): Temperature"
    condTempLv: float
    "User-defined conductor temperature (short-circuit): Temperature"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    detailedOutput: int
    "Detailed output"
    errLoading: int
    "Error"
    errMaxShc: int
    "Error"
    errSVChg: int
    "Error"
    errVChg: int
    "Error"
    flickerCalc: int
    "Flicker strength of voltage changes"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frmCndTemp: int
    "User-defined conductor temperature (short-circuit)"
    frmSkvCalc: int
    "Network short-circuit power and impedance angle calculation"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    ioptHrm3: int
    "Calculations: Harmonics, interharmonics and supraharmonics"
    ioptSigVolt: int
    "Calculations: Signal voltages"
    iopt_CommNotch: int
    "Calculations: Commutation notches"
    iopt_CommNotch_bdew: int
    "Calculations: Commutation notches"
    iopt_CommNotch_vde: int
    "Calculations: Commutation notches"
    iopt_CommNotch_vde4110: int
    "Calculations: Commutation notches"
    iopt_Flk_bdew: int
    "Flicker"
    iopt_Flk_vde: int
    "Calculations: Flicker"
    iopt_Flk_vde4110: int
    "Calculations: Flicker"
    iopt_Hrm: int
    "Calculations: Harmonics"
    iopt_HrmAll_bdew: int
    "Calculations: Harmonics, interharmonics and audio-frequency ripple control"
    iopt_HrmAll_vde: int
    "Calculations: Harmonics, interharmonics and audio-frequency ripple control"
    iopt_HrmAll_vde4105: int
    "Calculations: Harmonics, interharmonics and supraharmonics"
    iopt_HrmAll_vde4110: int
    "Calculations: Harmonics, interharmonics and supraharmonics"
    iopt_Interhrm: int
    "Calculations: Interharmonic voltages"
    iopt_Loading_bdew: int
    "Calculations: Loading of network components"
    iopt_Loading_vde: int
    "Calculations: Loading of network components"
    iopt_Loading_vde4110: int
    "Calculations: Loading of network components"
    iopt_MaxShc_bdew: int
    "Calculations: Maximum short-circuit current"
    iopt_MaxShc_vde: int
    "Calculations: Maximum short-circuit current"
    iopt_MaxShc_vde4110: int
    "Calculations: Maximum short-circuit current"
    iopt_MinSkV_vde4105: int
    "Calculations: Minimum short-circuit power at junction point"
    iopt_MinSkV_vde4110: int
    "Calculations: Minimum short-circuit power at junction point"
    iopt_Q_vde4110: int
    "Reactive power"
    iopt_Report: int
    "Report"
    iopt_SVChg_vde4105: int
    "Calculations: Rapid voltage changes"
    iopt_SVChg_vde4110: int
    "Calculations: Sudden voltage changes"
    iopt_Unbal_vde4110: int
    "Unbalance"
    iopt_VChgFlk: int
    "Calculations: Voltage changes and flicker"
    iopt_VChgFlk_bdew: int
    "Calculations: Sudden voltage changes and flicker"
    iopt_VChgFlk_vde: int
    "Calculations: Rapid voltage changes and flicker"
    iopt_VChg_bdew: int
    "Calculations: Admissible voltage changes"
    iopt_VChg_vde: int
    "Calculations: Permissible voltage changes"
    iopt_VChg_vde4110: int
    "Calculations: Admissible voltage change"
    iopt_VRise: int
    "Calculations: Slow voltage change (generating stations only)"
    iopt_VUnbal: int
    "Calculations: Voltage unbalance"
    iopt_VUnbal_vde: int
    "Calculations: Voltage unbalance"
    iopt_grid: int
    "Resonances (HV networks only): Grid contains mostly:Cables:Overhead lines"
    iopt_hrmLims: int
    "Detailed output"
    iopt_hvres: int
    "Resonances (HV networks only): Consideration of resonances:None:Approximate"
    iopt_lims: int
    "Resonances (HV networks only): Calculation of emission limits:Simplified:General"
    iopt_mde: int
    "Method:According to D-A-CH-CZ:According to BDEW, 4th Supplement:According to VDE-AR-N 4100/4105:According to VDE-AR-N 4110"
    iopt_simplifiedHrm_vde4105: int
    "Simplified calculation of harmonic current limits"
    iopt_simplifiedHrm_vde4110: int
    "Simplified calculation of harmonic current limits"
    iopt_vde4105MV: int
    "Assessment of plants in MV networks"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    opScenTyp: object
    "Resonances (HV networks only): Operation Scenario for calculation of SkV_akt"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    pubEdition: int
    "Edition:&0&3:&1&2"
    root_id: object
    "Original Location"
    selFeeders: object
    "Considered feeder(s)"
    supIntNodes: int
    "Suppress output for internal nodes"
    tid_: int
    "TimeID"
    year_pub4105: int
    "Published:2018:2011"
    year_pub4110: int
    "Published:2018"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComContingency(PFGeneral):
    BBFault: int
    "Busbar Fault"
    Elms: list
    "Name"
    IntState: list
    "State"
    addoptions: str
    "Additional Parameters"
    cStepByStep: int
    "Step by step execution in trace (one step -> one event)"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cluster: int
    "Load States: Cluster"
    cn_k: list
    "Contingency Order"
    contents: list
    "Events"
    cpHeadFold: object
    "Head Folder"
    dType: list
    "Failure Type"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    failType: list
    "Failure Type"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_evts: str
    "Events used for this Contingency"
    loc_name: str
    "Name"
    maintProb: float
    "Additional probability for dealing with maintenance"
    n_k: int
    "Contingency Order"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    outserv: int
    "Not analysed"
    pCase: object
    "Fault Case"
    pid_: int
    "ProjectID"
    prob_maint: float
    "Probability that this is in maintenance"
    restore: str
    "Switch/Load Events: System Restoration"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    year: int
    "Load States: Year"

    def AttributeType(*args): ...

    def ContinueTrace(*args): ...

    def CreateRecoveryInformation(*args): ...

    def Execute(*args): ...

    def GetGeneratorEvent(*args): ...

    def GetInterruptedPowerAndCustomersForStage(*args): ...

    def GetInterruptedPowerAndCustomersForTimeStep(*args): ...

    def GetLoadEvent(*args): ...

    def GetNumberOfGeneratorEventsForTimeStep(*args): ...

    def GetNumberOfLoadEventsForTimeStep(*args): ...

    def GetNumberOfSwitchEventsForTimeStep(*args): ...

    def GetNumberOfTimeSteps(*args): ...

    def GetObj(*args): ...

    def GetSwitchEvent(*args): ...

    def GetTimeOfStepInSeconds(*args): ...

    def GetTotalInterruptedPower(*args): ...

    def HasReferences(*args): ...

    def JumpToLastStep(*args): ...

    def RemoveEvents(*args): ...

    def StartTrace(*args): ...

    def StopTrace(*args): ...

    def __getattr__(*args): ...


class ComCoordreport(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_diaCurr: int
    "Overcurrent protection settings: Create Time-Overcurrent Plot"
    iopt_diaDist: int
    "Distance protection settings: Create Time-Distance Plot"
    iopt_repCurr: int
    "Overcurrent protection settings: Create report"
    iopt_repDist: int
    "Distance protection settings: Create report"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    p_pathCurr: object
    "Overcurrent protection settings: Path selection"
    p_pathDist: object
    "Distance protection settings: Path selection"
    p_res: object
    "Result selection: Result file"
    pid_: int
    "ProjectID"
    reportCurr: int
    "Overcurrent protection settings"
    reportDist: int
    "Distance protection settings"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def DevicesToReport(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def HasResultsForDirectionalBackup(*args): ...

    def HasResultsForFuse(*args): ...

    def HasResultsForInstantaneous(*args): ...

    def HasResultsForNonDirectionalBackup(*args): ...

    def HasResultsForOverload(*args): ...

    def HasResultsForOverreach(*args): ...

    def HasResultsForShortCircuit(*args): ...

    def HasResultsForZone(*args): ...

    def MaxZoneNumberFor(*args): ...

    def ResultForDirectionalBackupVariable(*args): ...

    def ResultForFuseVariable(*args): ...

    def ResultForInstantaneousVariable(*args): ...

    def ResultForMaxCurrent(*args): ...

    def ResultForNonDirectionalBackupVariable(*args): ...

    def ResultForOverloadVariable(*args): ...

    def ResultForOverreachVariable(*args): ...

    def ResultForShortCircuitVariable(*args): ...

    def ResultForZoneVariable(*args): ...

    def TopologyForDirectionalBackupVariable(*args): ...

    def TopologyForFuseVariable(*args): ...

    def TopologyForInstantaneousVariable(*args): ...

    def TopologyForMaxCurrent(*args): ...

    def TopologyForNonDirectionalBackupVariable(*args): ...

    def TopologyForOverloadVariable(*args): ...

    def TopologyForOverreachVariable(*args): ...

    def TopologyForShortCircuitVariable(*args): ...

    def TopologyForZoneVariable(*args): ...

    def TransferDirectionalBackupResultsTo(*args): ...

    def TransferNonDirectionalBackupResultsTo(*args): ...

    def TransferOverreachResultsTo(*args): ...

    def TransferResultsTo(*args): ...

    def TransferZoneResultsTo(*args): ...

    def __getattr__(*args): ...


class ComDllmanager(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    file: str
    "File Name"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_action: str
    "Action"
    iopt_type: str
    "DLL Type"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def Report(*args): ...

    def __getattr__(*args): ...


class ComDpl(PFGeneral):
    IntDesc: list
    "Description"
    IntExpr: list
    "Value"
    IntName: list
    "Name"
    IntResDesc: list
    "Description"
    IntResExpr: list
    "Value"
    IntResName: list
    "Name"
    IntResType: list
    "Type"
    IntResUnit: list
    "Unit"
    IntType: list
    "Type"
    IntUnit: list
    "Unit"
    ResultStr: list
    "Result String"
    addoptions: str
    "Additional Parameters"
    author: str
    "Author"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciLicenceReq: int
    "Licence required (DIG only)"
    company: str
    "Company"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    display3rdParty: list
    "Third Party Licence"
    displayCompanyCode: list
    "Third Party Licence (will only be applied after encryption!): Company Code"
    displayModule: list
    "Third Party Licence (will only be applied after encryption!): Module"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    isRemoteScriptSet: int
    "A remote script is set."
    loc_name: str
    "Name"
    modifytime: int
    "Last Modified"
    obj: object
    "object"
    obj_desc: list
    "Description"
    obj_id: list
    "object"
    obj_name: list
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    script_id: object
    "Remote script"
    sel_id: object
    "General Selection"
    shortDesc: str
    "Short Description"
    tid_: int
    "TimeID"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"
    version: str
    "Version"
    xDesc: list
    "Long Description"
    xNotes: list
    "Release Notes"
    xScript: list
    "Code"

    def AttributeType(*args): ...

    def CheckSyntax(*args): ...

    def Encrypt(*args): ...

    def Execute(*args): ...

    def GetExternalObject(*args): ...

    def GetInputParameterDouble(*args): ...

    def GetInputParameterInt(*args): ...

    def GetInputParameterString(*args): ...

    def HasReferences(*args): ...

    def IsEncrypted(*args): ...

    def ResetThirdPartyModule(*args): ...

    def SetExternalObject(*args): ...

    def SetInputParameterDouble(*args): ...

    def SetInputParameterInt(*args): ...

    def SetInputParameterString(*args): ...

    def SetThirdPartyModule(*args): ...

    def __getattr__(*args): ...


class ComFlickermeter(PFGeneral):
    N: int
    "Calculation Settings: Observation Periods"
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    col_Sep: str
    "File Input: Separator for columns"
    cpHeadFold: object
    "Head Folder"
    cvariable: list
    "Variable"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dec_Sep: str
    "File Input: Decimal separator"
    decseprtr: str
    "Decimal separator"
    element: list
    "Element"
    f_name: str
    "File Input: Filename"
    fc: float
    "Parameter Definitions: Cut-off Frequency"
    fcalib: float
    "Parameter Definitions: Scaling Factor"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iColName: list
    "Variable Name"
    iColNum: list
    "Column Number"
    iColSelVar: list
    "Calculate Pst"
    iSchemeStatus: int
    "Scheme Status"
    iopt_Report: int
    "Report"
    iopt_csep: int
    "File Input: Separator for columns"
    iopt_imp: int
    "File Input: Import data from:COMTRADE:Comma Separated Values (*.csv):PowerFactory Measurement File:User Defined Text File:Result File"
    iopt_plt: int
    "Calculation Settings: Calculate Plt"
    iopt_resamp: int
    "Signal Settings: Resample Data"
    iopt_sep: int
    "File Input: Use system separators"
    iopt_sig: int
    "Signal Settings: Signal Type"
    iopt_tstart: int
    "Signal Settings: Specify Start Time"
    loc_name: str
    "Name"
    newSampRate: float
    "Signal Settings: New Sampling Rate"
    offset: float
    "Parameter Definitions: Filter Offset"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pResfile: object
    "File Input: Result File"
    p_resvar: object
    "Result Variables"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sampRateTol: float
    "Constant Sampling Rate: Tolerance"
    separator: str
    "Separator for columns"
    tid_: int
    "TimeID"
    tshort: float
    "Calculation Settings: Observation Period:1:5:10:15"
    tstart: float
    "Signal Settings: Start Time"
    variable: list
    "Variable"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComGenrelinc(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    crndNumGen: list
    "Global random number generator: Actually used method:"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    day_1: int
    "Time Dependent Data Days: Monday"
    day_2: int
    "Time Dependent Data Days: Tuesday"
    day_3: int
    "Time Dependent Data Days: Wednesday"
    day_4: int
    "Time Dependent Data Days: Thursday"
    day_5: int
    "Time Dependent Data Days: Friday"
    day_6: int
    "Time Dependent Data Days: Saturday"
    day_7: int
    "Time Dependent Data Days: Sunday"
    dbg_avtimes: int
    "Show available time points"
    dbg_basic: int
    "Show basic information"
    dbg_colgen: list
    "Object"
    dbg_colpmx: list
    "Value"
    dbg_drtimes: int
    "At each iteration...: Show drawn times"
    dbg_grid: int
    "At each iteration...: Show aggregated values per grid"
    dbg_iter: int
    "At each iteration...: Show generation/demand values per machine"
    dbg_mach: int
    "At each iteration...: Show generation/demand values per parallel machine"
    dbg_only4it: int
    "At each iteration...: Only for iteration"
    dbg_storeit: int
    "At each iteration...: Store generation results (for specified single iteration)"
    dbg_system: int
    "At each iteration...: Show aggregated values per system"
    dbg_timechk: int
    "Check available time points"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hour_end1: int
    "Time Dependent Data Time Intervals: To"
    hour_end2: int
    "Time Dependent Data Time Intervals: To"
    hour_end3: int
    "To"
    hour_str1: int
    "Time Dependent Data Time Intervals: From"
    hour_str2: int
    "Time Dependent Data Time Intervals: From"
    hour_str3: int
    "Time Dependent Data Time Intervals: From"
    iSchemeStatus: int
    "Scheme Status"
    i_rndseed: int
    "Global random number generator: Seed"
    iopt_asc: int
    "Report"
    iopt_intrvl2: int
    "Time Dependent Data Time Intervals: Interval 2:"
    iopt_intrvl3: int
    "Time Dependent Data Time Intervals: Interval 3:"
    iopt_load: int
    "Demand Consideration"
    iopt_maint: int
    "Consider Maintenance Plans"
    iopt_network: int
    "Consider Network Constraints"
    iopt_resdraw: int
    "Results: MC Draws"
    iopt_rnd: int
    "Global random number generator: Seeding type:Automatic:User defined"
    lastSeed: list
    "Global random number generator: Last used seed"
    loc_name: str
    "Name"
    lossesP: float
    "Network: System Losses"
    month_01: int
    "Time Dependent Data Months: January"
    month_02: int
    "Time Dependent Data Months: February"
    month_03: int
    "Time Dependent Data Months: March"
    month_04: int
    "Time Dependent Data Months: April"
    month_05: int
    "Time Dependent Data Months: May"
    month_06: int
    "Time Dependent Data Months: June"
    month_07: int
    "Time Dependent Data Months: July"
    month_08: int
    "Time Dependent Data Months: August"
    month_09: int
    "Time Dependent Data Months: September"
    month_10: int
    "Time Dependent Data Months: October"
    month_11: int
    "Time Dependent Data Months: November"
    month_12: int
    "Time Dependent Data Months: December"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    p_resdist: object
    "Results: Distribution"
    p_resdraw: object
    "Results: MC Draws"
    pid_: int
    "ProjectID"
    rndNumGen: int
    "Global random number generator: Method:"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    updateRng: int
    "Global random number generator: Update global random number generator"
    year_study: int
    "Time Dependent Data: Year of Study"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetCurrentIteration(*args): ...

    def GetMaxNumIterations(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComGridtocim(PFGeneral):
    addoptions: str
    "Additional Parameters"
    asDifference: int
    "Profile conversion: Create difference models"
    asReduced: int
    "Profile conversion: Create bus-branch model"
    authorityDesc: list
    "Model description: Description"
    authorityVersion: str
    "Model description: Version"
    cAuthority: list
    "Authority URI"
    cBoundary: list
    "Boundary"
    cSelected: list
    "Selected"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    convertDL: int
    "Profiles to convert: Diagram Layout"
    convertDY: int
    "Profiles to convert: Dynamics"
    convertEQ: int
    "Profiles to convert: Equipment"
    convertGL: int
    "Profiles to convert: Geographical Location"
    convertSC: int
    "Profiles to convert: Short Circuit"
    convertSSH: int
    "Profiles to convert: Steady State Hypothesis"
    convertSV: int
    "Profiles to convert: State Variables"
    convertTP: int
    "Profiles to convert: Topology"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dependencies: object
    "Create models in: Additional Archives"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_target: int
    "Create models in"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    partial: int
    "Profile conversion"
    pid_: int
    "ProjectID"
    profileFlag: int
    "Profile Filter"
    root_id: object
    "Original Location"
    selectedGrids: list
    "Selected"
    targetName: str
    "Create models in: Name"
    targetPath: object
    "Create models in: Target Archive"
    tid_: int
    "TimeID"
    version: str
    "Profile version"

    def AssignCimRdfIds(*args): ...

    def AttributeType(*args): ...

    def ConvertAndExport(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def SetAuthorityUri(*args): ...

    def SetBoundaries(*args): ...

    def SetGridsToExport(*args): ...

    def __getattr__(*args): ...


class ComHostcap(PFGeneral):
    Uneutral: float
    "Neutral voltage"
    addObjs2Transfer: object
    "Additional objects to transfer"
    addoptions: str
    "Additional Parameters"
    antisland: float
    "Anti-islanding level"
    brkFusCoord: float
    "Breaker/fuse co-ordination"
    brkReach: float
    "Breaker reduction of reach"
    busVoltLimitsOn: int
    "Consider Voltage Limits"
    caseNum: str
    "Case number"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    constChkScope: int
    "Constraints check"
    contents: list
    "Contents"
    coptVrisedrop: int
    "Voltage drop/rise"
    coptnewlod: int
    "Connect new load to the busbar"
    coptvolunbal: int
    "Voltage unbalance"
    cpHeadFold: object
    "Head Folder"
    creduceFeeders: int
    "Reduce feeders"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dbgOn: int
    "Detailed debug output:Low:High"
    derpf: float
    "DER power factor"
    dfliclt: float
    "Long-term flicker disturbance factor (continuous operation)"
    dflicst: float
    "Short-term flicker disturbance factor (continuous operation)"
    dindhd: float
    "Individual harmonic magnitude"
    dthd: float
    "Total harmonic voltage distortion"
    dthdint: float
    "Integer harmonics"
    feedVolt: float
    "Feeder voltage"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frIterMethd: int
    "Step size algorithm"
    frmConnNewLod: int
    "Connect new load to the busbar"
    frmVolTypChk: int
    "3-phase (ABC) voltage check"
    frwFlowContr: float
    "Forward flow fault current contribution"
    fuseCurrChng: float
    "Fuse current change"
    globalFeederLimit: int
    "Option"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iEnableParal: int
    "Parallel computation"
    iLoad: int
    "Option"
    iSchemeStatus: int
    "Scheme Status"
    iSysTyp: int
    "Calculation method"
    iVolt: int
    "Option"
    if_load: float
    "Option: Maximum thermal loading of components"
    if_volmax: float
    "Option: Upper limit of allowed voltage"
    if_volmin: float
    "Option: Lower limit of allowed voltage"
    inclFeederStartNode: int
    "Include feeder starting terminal"
    initStep: float
    "Initial conditions: Initial step size"
    initType: int
    "Initialisation of load flow"
    iopt1phs: int
    "1-ph fault"
    iopt2phs: int
    "2-ph fault"
    iopt3phs: int
    "3-ph fault"
    ioptAntisl: int
    "Anti-islanding level"
    ioptBrkreach: int
    "Breaker reduction of reach"
    ioptDerObj: int
    "Connected DER"
    ioptFflow: int
    "Forward flow fault current contribution"
    ioptFlicker: int
    "Flicker"
    ioptFusecurr: int
    "Fuse current change"
    ioptGenNodeOnly: int
    "Only consider terminals where generator already connected"
    ioptIndFeeder: int
    "Ignore terminals which are not part of a feeder"
    ioptLoads: int
    "Consideration of loads"
    ioptLodNodeOnly: int
    "Only consider terminals where load already connected"
    ioptModGrid: int
    "Apply changes to grid"
    ioptOnlyBuses: int
    "Consider specific terminals only"
    ioptPqual: int
    "Constraints: Power quality limits"
    ioptProt: int
    "Constraints: Protection limits"
    ioptProtElm: int
    "Considered protection devices"
    ioptRevFlow: int
    "Reversed power flow"
    ioptShcContr: int
    "Total fault contribution"
    ioptTrip: int
    "Relay/fuse tripping"
    ioptUsrLod: int
    "Consider user-defined load selection"
    ioptVoltages: int
    "Voltages"
    iopt_Feeder: int
    "Voltage drop/rise"
    iopt_Uneutral: int
    "Neutral voltage"
    iopt_action: int
    "Processing Actions"
    iopt_allmsgs: int
    "Print all messages"
    iopt_applycontr: int
    "Constraints check"
    iopt_ign: int
    "Ignore all constraints for nominal voltage..."
    iopt_inckss: int
    "Incremental contribution to the short-circuit current"
    iopt_innodes: int
    "List ignored internal nodes"
    iopt_lodcons: int
    "Constraints: Thermal limits"
    iopt_lth: int
    "Long-term flicker disturbance factor (continuous operation)"
    iopt_newlod: int
    "Connect new load to the busbar"
    iopt_shc: int
    "Constraints: Short-circuit contribution limits"
    iopt_shcmodel: int
    "Short-circuit contribution: Short-circuit model"
    iopt_skipbcviol: int
    "Ignore elements with base-case violations"
    iopt_sth: int
    "Short-term flicker disturbance factor (continuous operation)"
    iopt_sumvarschk: int
    "Check summary variables only (fast check)"
    iopt_thdi: int
    "Integer harmonics"
    iopt_thdst: int
    "Total harmonic voltage distortion"
    iopt_ufeeddrop: int
    "Feeder voltage drop"
    iopt_ufeedrise: int
    "Feeder voltage rise"
    iopt_volchng: int
    "Permissible voltage change (from no DER to full DER)"
    iopt_volcons: int
    "Constraints: Voltage limits"
    iopt_volunbal: int
    "Voltage unbalance"
    ioptpmax: int
    "User-defined active power limits"
    ioptshccalc: int
    "Short-circuit calculation"
    isOutGrpObjs: int
    "Group reported objects for compact output"
    ivolchnggens: int
    "Generators to be switched off"
    ivoltreg: int
    "Voltage regulator tap change"
    loc_name: str
    "Name"
    lodpf: float
    "Connect new load to the busbar: Power factor"
    lodsScaling: int
    "Load scaling factor"
    maxIter: float
    "Convergence criteria: Max. number of iterations"
    maxVdrop: float
    "Option: Maximum Voltage Drop"
    maxVrise: float
    "Option: Maximum Voltage Rise"
    maxctap: int
    "Voltage regulator tap change: Max. allowed number of taps (capacitor)"
    maxtap: int
    "Voltage regulator tap change: Max. allowed number of taps (regulator)"
    minCalcPt4Par: int
    "Parallel computation: Minimum number of calculation objects"
    minStep: float
    "Convergence criteria: Min. step size"
    notopo: int
    "No topology rebuild"
    numObj4Slave: int
    "Parallel computation: Package size for parallel process"
    objective: int
    "Calculation objective"
    oid_: int
    "ObjectID"
    optVrisedrop: int
    "Voltage drop/rise"
    optcosphi: int
    "Power factor attribute"
    order: float
    "Order"
    outputType: int
    "Output per iteration"
    pDer1p: object
    "1-phase DER element"
    pDer3p: object
    "3-phase DER element"
    pHctyp: object
    "Harmonics contribution: Harmonic currents"
    pHflick: object
    "Harmonics contribution: Flicker coefficients"
    pProt: object
    "Considered protection devices: Protection device(s)"
    pResult: object
    "Results"
    paralSet: int
    parallelSetting: object
    "Parallel computation: Parallel computation settings"
    pchkelms: object
    "Constraints check: Selection"
    pf_MODE: int
    "Power factor:inductive:capacitive"
    pfl_MODE: int
    "Power factor:inductive:capacitive"
    pid_: int
    "ProjectID"
    plodini: float
    "Connect new load to the busbar: Initial active power"
    pmax: float
    "User-defined active power limits: Final generated power"
    pmin: float
    "User-defined active power limits: Initial generated power"
    reduceFeeders: int
    "Reduce feeders"
    root_id: object
    "Original Location"
    rtox: float
    "Short-circuit contribution: R/X"
    selBus: object
    "Busbar selection (optional)"
    selLod: object
    "Loads selection (optional)"
    selObj: object
    "Hosting sites"
    sel_filter: object
    "Generators to be switched off: Generators"
    shckss: float
    "Contribution factor"
    symBrktrip: float
    "Sympathetic breaker tripping"
    tid_: int
    "TimeID"
    timeTriggersOff: int
    "Ignore time trigger"
    totShcContr: float
    "Total fault contribution"
    totshc: float
    "Short-circuit contribution"
    vlevhi: float
    "Ignore all constraints for nominal voltage...: > (above)"
    vlevlow: float
    "Ignore all constraints for nominal voltage...: < (below)"
    voltchng: float
    "Permissible voltage change (from no DER to full DER): Max. voltage change"
    voltunbal: float
    "Voltage unbalance: Max. voltage unbalance factor"

    def AttributeType(*args): ...

    def CalcMaxHostedPower(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComImport(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    datapartLabel: str
    "Labels"
    datapartLabels: list
    "Partial import: Labels"
    datasetLabel: str
    "Dataset import: Label"
    dbAddParam: str
    "Import from: Additional ODBC Parameters"
    dbDatabase: str
    "Import from: Database"
    dbDriverName: str
    "Import from: ODBC Driver Name"
    dbInfo: str
    "Import from: e.g."
    dbPassword: str
    "Import from: Password"
    dbSchema: str
    "Import from: Schema Name"
    dbServer: str
    "Import from: DB Service"
    dbUser: str
    "Import from: User"
    dgsFormat: str
    "Source"
    dgsFormatIdx: int
    "Import from: Format"
    fFile: str
    "Import from: Name"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    generalKey: list
    "Key"
    generalValue: list
    "Value"
    globTypeLib: object
    "Global type library"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_check: int
    "Import from: Replace non-printable characters"
    iopt_cpylib: int
    "Import from Library: Copy Library into Project"
    iopt_fkey: int
    "Use foreign keys"
    iopt_noxsd: int
    "Import from: No Schema Validation"
    iopt_prj: int
    "Import into"
    iopt_schema: int
    "Import from: Use Schema"
    iopt_switch: int
    "Import from: Create Switch inside Cubicle"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    openGraphics: int
    "Open single line diagram(s)"
    order: float
    "Order"
    pAddPrj: object
    "Import into: Name"
    pDatabase: object
    "Import from: From Configuration"
    pid_: int
    "ProjectID"
    predeflib: object
    "Import from Library: Predefined Library"
    prjTemplate: object
    "Import into: Project Template"
    root_id: object
    "Original Location"
    targname: str
    "Import into: Name"
    targpath: object
    "Import into: in"
    tid_: int
    "TimeID"
    useDatapart: int
    "Partial import"
    useDataset: int
    "Dataset import"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetCreatedObjects(*args): ...

    def GetModifiedObjects(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComInc(PFGeneral):
    addoptions: str
    "Additional Parameters"
    allowedBusErrLv: float
    "Max. acceptable equation error: Bus equations (LV)"
    allowedBusErrLv_emt: float
    "Max. acceptable equation error: Bus equations (LV)"
    allowedBusErrMv: float
    "Max. acceptable equation error: Bus equations (MV)"
    allowedBusErrMv_emt: float
    "Max. acceptable equation error: Bus equations (MV)"
    allowedErrAllGridEq: float
    "Grid error threshold to recompute Jacobian matrix"
    alpha_emt: float
    "Integration: Damping factor"
    alpha_rms: float
    "Integration: Damping factor"
    automaticCompilation: int
    "DSL: Automatic compilation"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciopt_sample: int
    "Record results"
    ckres: float
    "Event: Resolution factor (with respect to smallest step)"
    cloadSnap: int
    "Load snapshot at initialisation"
    com_init: int
    "Interface: Send and receive after initialisation"
    com_inter: float
    "Interface Update: Interval"
    copt_adapt: int
    "Automatic step size adaptation"
    copt_coiref: int
    "Reference"
    copt_fastcon: int
    "Simplifications: Fast connection of A-stable models outputs"
    copt_lt: int
    "A-stable integration algorithm"
    copt_net: int
    "Network representation"
    copt_real: int
    "Real-time simulation"
    copt_reinc: int
    "Reinitialise algebraic equations at interruption"
    copt_sim: int
    "Simulation method"
    cpHeadFold: object
    "Head Folder"
    crndNumGen: list
    "Global random number generator: Actually used method:"
    ctstart: float
    "Start time"
    cvoltLevHv: float
    "Max. acceptable equation error: >"
    cvoltLevLv: float
    "Max. acceptable equation error: >"
    cvoltLevMv: float
    "Max. acceptable equation error: >"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    ddtemt_max: float
    "Maximum increase of step size"
    ddtgrd_max: float
    "Maximum increase of step size"
    dtemt: float
    "Integration step size: Electromagnetic transients"
    dtemt_max: float
    "Integration step size: Maximum step size"
    dtgrd: float
    "Integration step size: Electromechanical transients"
    dtgrd_max: float
    "Integration step size: Maximum step size"
    dtout: float
    "Output sampling step"
    dtout_emt: float
    "Output sampling step"
    erreq: float
    "Max. acceptable equation error: Network model equations"
    erreq_emt: float
    "Max. acceptable equation error: Network model equations"
    errinc: float
    "Minimum prediction error"
    errmax: float
    "Maximum prediction error"
    errseq: float
    "Integration: Maximum error for dynamic model equations"
    errsm: float
    "Max. acceptable equation error: Bus equations (HV)"
    errsm_emt: float
    "Max. acceptable equation error: Bus equations (HV)"
    fdec: float
    "Speed factor: decrease"
    finc: float
    "Speed factor: increase"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iReuseLdf: int
    "Reuse previous load flow results"
    iSchemeStatus: int
    "Scheme Status"
    i_deldirect: int
    "DSL: Fast direct interpolation of buffers (delay and movingavg)"
    i_multincw: int
    "Initialisation: Issue warnings for multiple initialisation of signals"
    i_rndseed: int
    "Global random number generator: Seed"
    i_sedirect: int
    "DSL: Direct application of events"
    iac: int
    "Integration: Apply AC-adaptation"
    iinftag: int
    "Consider inertias as infinite"
    iopt_action: int
    "Processing Actions"
    iopt_adapt: int
    "Automatic step size adaptation"
    iopt_adaptadv: int
    "Advanced step size algorithm"
    iopt_adaptreset: int
    "Reset automatic step size at interruption"
    iopt_all: int
    "A-stable integration algorithm: Apply to all elements"
    iopt_coiref: int
    "Reference"
    iopt_conn: int
    "A-stable integration algorithm: Apply per element and composite model"
    iopt_dfrotx: int
    "Calculate maximum rotor angle deviation (dfrotx)"
    iopt_dis: int
    "Interface: Distributed simulation"
    iopt_eulmax: int
    "Integration formula restoration steps after reset"
    iopt_expref: int
    "Reference system calculation method"
    iopt_fastchk: int
    "Simplifications: Fast convergence check"
    iopt_fastcon: int
    "Simplifications: Fast connection of A-stable models outputs"
    iopt_fastout: int
    "Simplifications: Fast computation of outputs"
    iopt_fastsol: int
    "Simplifications: Fast independent solution of network and dynamic models"
    iopt_int: int
    "Interface: Update"
    iopt_load: int
    "Snapshot selection"
    iopt_locref: int
    "Reference system area"
    iopt_lt: int
    "A-stable integration algorithm"
    iopt_net: str
    "Network representation"
    iopt_only: int
    "A-stable integration algorithm: Apply per element"
    iopt_outofstep: int
    "Synchronous machine out of step detection"
    iopt_partinc: int
    "Initialisation: Enable partial initialisation in case of deadlock"
    iopt_real: int
    "Real-time simulation"
    iopt_reinc: int
    "Reinitialise algebraic equations at interruption"
    iopt_reinf: int
    "Event: Reset integration formula after reinitialisation of algebraic equations"
    iopt_rnd: int
    "Global random number generator: Seeding type:Automatic:User defined"
    iopt_sample: int
    "Record results"
    iopt_save: int
    "Save snapshot via event"
    iopt_show: int
    "Verify initial conditions"
    iopt_sim: str
    "Simulation method"
    iopt_simscn: int
    "Active"
    iopt_solvinc: int
    "Initialisation: Solve dynamic model equations at initialisation"
    iopt_startmax: int
    "Use maximum step size at start"
    iopt_sync: int
    "Enforced synchronisation"
    iopt_vdhnm: int
    "Simplified Newton method"
    ipolate: int
    "Behaviour at user-defined events"
    itrjx: int
    "Iteration: Iteration limit to recompute Jacobian matrix"
    itrlx: int
    "Iteration: Maximum number of iterations"
    itrmx: int
    "Event: Maximum number of repeat event loops"
    itrmxdisc: int
    "Event: Maximum number of discrete event iterations"
    itrmxint: int
    "Event: Maximum number of zero-length interruptions"
    itrmxmin: int
    "Event: Maximum number of reschedule event loops"
    kres: float
    "Event: Resolution factor (with respect to smallest step)"
    lastSeed: list
    "Global random number generator: Last used seed"
    loadSnap: int
    "Load snapshot at initialisation"
    loc_name: str
    "Name"
    mult_out: int
    "Record results: Sampling ratio (output step to integration step)"
    mult_out_emt: int
    "Record results: Sampling ratio (output step to integration step)"
    ninc: int
    "Delay for step size increase (number of steps)"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    outofstepdet: float
    "Synchronous machine out of step detection: Detection angle"
    outputstep: float
    "Record results: Output sampling step"
    p_event: object
    "Selection of simulation events: Events"
    p_resvar: object
    "Result variables"
    p_simscn: object
    "Modules"
    pid_: int
    "ProjectID"
    reincEvtType: int
    "Event types:All:Interruptions"
    reincIter: int
    "Reinitialisation Iteration:Reinitialise in each discrete event iteration step:Reinitialise after discrete event iteration completed"
    rndNumGen: int
    "Global random number generator: Method"
    root_id: object
    "Original Location"
    rt_factor: float
    "Synchronisation with system time: Ratio between real time and calculation time"
    rt_inter: float
    "Synchronisation with system time: Time interval used for synchronisation"
    sigbuf: int
    "Signal buffer"
    snapFile: str
    "Snapshot selection: File"
    snapPath: str
    "Save snapshot via event: Directory"
    solveInitDisc: int
    "Solve discrete states at initialisation"
    syncperiod: float
    "Enforced synchronisation: Period"
    syncresult: int
    "Write results only at synchronised point in time"
    tcemt: float
    "Time constant for EMT simulation"
    tcgrd: float
    "Time constant for RMS simulation"
    tid_: int
    "TimeID"
    tstart: float
    "Start time"
    tsync: float
    "Buffer size"
    updateRng: int
    "Global random number generator: Update global random number generator"

    def AttributeType(*args): ...

    def CompileDynamicModelTypes(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def ZeroDerivative(*args): ...

    def __getattr__(*args): ...


class ComLdf(PFGeneral):
    PostContTime: float
    "Time Phase: Post Contingency Time (End of Time Phase)"
    Sfix: float
    "Fixed Load"
    Sin: float
    "Installed Power"
    Svar: float
    "Max. Power per Customer"
    addoptions: str
    "Additional Parameters"
    allowedBusErrLv: float
    "Max. Acceptable Load Flow Error: Bus Equations (LV)"
    allowedBusErrMv: float
    "Max. Acceptable Load Flow Error: Bus Equations (MV)"
    bPlim4constP: int
    "Considered Models for Active Power Limits: Limit active power also for const. P machines"
    bPlimAsm: int
    "Considered Models for Active Power Limits: Asynchronous machine"
    bPlimGenst: int
    "Considered Models for Active Power Limits: Static generator"
    bPlimPWM: int
    "Considered Models for Active Power Limits: PWM converter"
    bPlimSym: int
    "Considered Models for Active Power Limits: Synchronous machine"
    bQlim4constQ: int
    "Considered Models for Reactive Power Limits: Limit reactive power also for const. Q machines"
    bQlimAsm: int
    "Considered Models for Reactive Power Limits: Asynchronous machine"
    bQlimGenst: int
    "Considered Models for Reactive Power Limits: Static generator"
    bQlimPWM: int
    "Considered Models for Reactive Power Limits: PWM converter"
    bQlimSlack: int
    "Considered Models for Reactive Power Limits: Reference machine"
    bQlimSvs: int
    "Considered Models for Reactive Power Limits: Static Var system"
    bQlimSym: int
    "Considered Models for Reactive Power Limits: Synchronous machine"
    bQlimXnet: int
    "Considered Models for Reactive Power Limits: External grid"
    cLimScaleOff: int
    "Consider reactive power limits scaling factor"
    cPbalancing: int
    "Balancing"
    cPlim4constPOff: int
    "Considered Models for Active Power Limits: Limit active power also for const. P machines"
    cPlimAsmOff: int
    "Considered Models for Active Power Limits: Asynchronous machine"
    cPlimGenstOff: int
    "Considered Models for Active Power Limits: Static generator"
    cPlimPWMOff: int
    "Considered Models for Active Power Limits: PWM converter"
    cPlimSymOff: int
    "Considered Models for Active Power Limits: Synchronous machine"
    cQlim4constQOff: int
    "Considered Models for Reactive Power Limits: Limit reactive power also for const. Q machines"
    cQlimAsmOff: int
    "Considered Models for Reactive Power Limits: Asynchronous machine"
    cQlimGenstOff: int
    "Considered Models for Reactive Power Limits: Static generator"
    cQlimPWMOff: int
    "Considered Models for Reactive Power Limits: PWM converter"
    cQlimSlackOff: int
    "Considered Models for Reactive Power Limits: Reference machine"
    cQlimSvsOff: int
    "Considered Models for Reactive Power Limits: Static Var system"
    cQlimSymOff: int
    "Considered Models for Reactive Power Limits: Synchronous machine"
    cQlimXnetOff: int
    "Considered Models for Reactive Power Limits: External grid"
    cSav: float
    "Average Power"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    codePlim: int
    "P limits"
    codeQlim: int
    "Q limits"
    copt_apdist: int
    "Active Power Control"
    copt_net: int
    "Calculation Method"
    copt_tem: int
    "Temperature Dependency: Line/Cable Resistances: at"
    cosfix: float
    "Power Factor of Fixed Load"
    cosvar: float
    "Power Factor of Variable Part"
    cpHeadFold: object
    "Head Folder"
    ctemperature: int
    "Temperature Dependency: Line/Cable Resistances: Temperature"
    cvoltLevHv: float
    "Max. Acceptable Load Flow Error: >"
    cvoltLevLv: float
    "Max. Acceptable Load Flow Error: >"
    cvoltLevMv: float
    "Max. Acceptable Load Flow Error: >"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    erreq: float
    "Max. Acceptable Load Flow Error: Model Equations"
    errlf: float
    "Max. Acceptable Load Flow Error: Bus Equations (HV)"
    fa: float
    "Utilisation Factor"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    ginf: float
    "Coincidence Factor (ginf)"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iFromSaved: int
    "Starting point: Start from saved results"
    iInterChg: int
    "Interchange Schedule"
    iInterType: int
    "Interchange Schedule: Consider Interchange Schedules for..."
    iItAlgStag: int
    "Iteration step size: Break if no progress in X iterations"
    iKeepCalc: int
    "Maintain load flow results if calculation fails"
    iPST_at: int
    "Active Power Regulation: Automatic tap adjustment of phase shifters"
    iPbalancing: int
    "Balancing"
    iPostCont: int
    "Time Phase"
    iResType: int
    "Starting point: Source:from memory:from a file"
    iSchemeStatus: int
    "Scheme Status"
    iShowOutLoopMsg: int
    "Show 'Outer Loop' messages"
    iStepAdapt: int
    "Iteration step size"
    iTempLoads: int
    "Temperature Dependent Load Scaling"
    iTrimStep: int
    "Iteration step size: Trim unreasonable Newton-Raphson steps"
    i_power: int
    "Load Flow Method"
    i_volt: int
    "Consider coincidence of low-voltage loads: Voltage Drop Analysis"
    iavailfact: int
    "Consider Availability Factors"
    ictrlx: int
    "Max. Number of Iterations: Outer Loop"
    ign_comp: int
    "Ignore Composite Elements"
    ign_mdb: list
    "OoS Objects"
    imaxPHSstep: int
    "Max. tap changes per iteration: for phase shifting transformers:oo:1:2:3:4:5:6:7:8:9:10"
    imaxtstep: int
    "Max. tap changes per iteration: for transformers, shunts:oo:1:2:3:4:5:6:7:8:9:10"
    iopt_apdist: int
    "Active Power Control"
    iopt_asht: int
    "Voltage and Reactive Power Regulation: Automatic tap adjustment of shunts"
    iopt_at: int
    "Voltage and Reactive Power Regulation: Automatic tap adjustment of transformers"
    iopt_chctr: int
    "Check Control Conditions"
    iopt_check: int
    "Reports"
    iopt_fl: int
    "Flat Start"
    iopt_fls: int
    "Load Options: Feeder Load Scaling"
    iopt_igntow: int
    "Modelling Method of Towers:with in/output signals:ignore couplings:equation in lines"
    iopt_initOPF: int
    "Use this load flow for initialisation of OPF"
    iopt_iph: int
    "Ignore transformer phase shift"
    iopt_lev: int
    "Automatic Model Adaptation for Convergence"
    iopt_lim: int
    "Voltage and Reactive Power Regulation: Consider reactive power limits"
    iopt_limScale: int
    "Consider reactive power limits scaling factor"
    iopt_lod: int
    "Voltage dependent loads in Post Fault analysis"
    iopt_maxibus: int
    "Calculate max. current at busbars"
    iopt_net: int
    "Calculation Method"
    iopt_noinit: int
    "Starting point: Start from last calculated results if available"
    iopt_notopo: int
    "No Topology Rebuild"
    iopt_optaplim: int
    "Consider operational limits for tap changer"
    iopt_plim: int
    "Active Power Regulation: Consider active power limits"
    iopt_pq: int
    "Load Options: Consider Voltage Dependency of Loads"
    iopt_prot: int
    "Consider Protection Devices:none:all:main:backup"
    iopt_show: int
    "Show Convergence Progress Report"
    iopt_sim: int
    "Consider coincidence of low-voltage loads"
    iopt_spar: int
    "Calculate Power at Risk"
    iopt_stamode: int
    "Station Controller:Standard:Gen HV-Ctrl:Gen LV-Ctrl"
    iopt_tem: int
    "Temperature Dependency: Line/Cable Resistances: at"
    iopt_trainsim: int
    "Train simulation"
    iprimctrl: int
    "Consider Primary Controllers"
    itapopt: int
    "Method:direct:stepped"
    itrlx: int
    "Max. Number of Iterations: Newton-Raphson Iteration"
    krelax: float
    "Min. Controller Relaxation Factor"
    loadmax: float
    "Max. Loading of Edge Element"
    loc_name: str
    "Name"
    maxDivOuterLoops: int
    "Break, if Newton-Raphson diverges in first X outer loops"
    maxPhaseShift: float
    "Max. transformer phase shift"
    maxQlimTrans: int
    "Automatic detection of repeated reactive power limitations: Number of transitions"
    maxTapTrans: int
    "Automatic detection of tap hunting: Number of transitions"
    modelLevel: int
    "Model level"
    nsteps: int
    "Max. Number of Iterations: Number of Steps"
    numNewtonIters: list
    "Number of Newton iterations"
    numOuterLoops: int
    "Number of outer loops"
    num_conv: int
    "Show Convergence Progress Report: Number of reported buses/models per iteration"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    p_event: object
    "Events"
    phiini: float
    "Reference Bus: Angle"
    pid_: int
    "ProjectID"
    relax: float
    "Iteration step size: Relaxation Factor"
    rembar: object
    "Reference Bus: Reference Busbar"
    resFile: str
    "Starting point: File"
    root_id: object
    "Original Location"
    scGenFac: float
    "Scaling by category: Generation"
    scLoadFac: float
    "Scaling by category: Loads"
    scMotFac: float
    "Scaling by category: Motors"
    scPnight: float
    "Scaling by category: Night storage heaters"
    temperature: float
    "Temperature Dependency: Line/Cable Resistances: Temperature"
    tid_: int
    "TimeID"
    totNumNewtonIters: int
    "Sum of Newton iterations (of all outer loops)"
    tres: float
    "Event-Resolution"
    utr_init: int
    "Voltage magnitude initialisation: Voltage magnitude initialisation:Use voltage setpoint at reference busbar:Consider ratio of rated to nominal voltage:Consider ratio of rated to nominal voltage for all branches except transformers:Consider ratio of rated to nominal voltage for transformers only"
    vlmax: float
    "Upper Limit of Allowed Voltage"
    vlmin: float
    "Lower Limit of Allowed Voltage"
    zoneScale: int
    "Zone scaling"

    def AttributeType(*args): ...

    def CheckControllers(*args): ...

    def DoNotResetCalc(*args): ...

    def EstimateOutage(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def IsAC(*args): ...

    def IsBalanced(*args): ...

    def IsDC(*args): ...

    def PrintCheckResults(*args): ...

    def SetOldDistributeLoadMode(*args): ...

    def __getattr__(*args): ...


class ComLink(PFGeneral):
    addoptions: str
    "Additional Parameters"
    cReadValueInit: int
    "Initialise read items with OPC server's values"
    charact: list
    "Charact."
    chardel: str
    "Character Delimiter:;:,"
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deadband: float
    "Deadband Usage: Deadband"
    fFile: str
    "Name"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iEngineID: int
    "Engine ID"
    iSchemeStatus: int
    "Scheme Status"
    idReplacement: str
    "TagID Placeholder"
    iopt_db: int
    "DB Synchronisation"
    iopt_deadb: int
    "Deadband Usage"
    iopt_lastfile: int
    "Read the last file from folder"
    iopt_link: int
    "Link To"
    iopt_report: int
    "Reports"
    iopt_reset: int
    "Reset Statuses"
    isLinkStarted: int
    "Link started?"
    loc_name: str
    "Name"
    noise: float
    "Noise"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pDataSets: object
    "Import Data"
    pDataSets2: object
    "Export Data"
    pDataSets3: object
    "DigPF Data"
    pid_: int
    "ProjectID"
    qBad: int
    "BAD"
    qBadCommFail: int
    "BAD: Comm Failure"
    qBadConfigErr: int
    "BAD: Configuration Error"
    qBadDevFail: int
    "BAD: Device Failure"
    qBadLastVal: int
    "BAD: Last Known Value"
    qBadNonSpec: int
    "BAD: Non-specific"
    qBadNotCon: int
    "BAD: Not Connected"
    qBadOutServ: int
    "BAD: Out of Service"
    qBadSensFail: int
    "BAD: Sensor Failure"
    qBadWaiting: int
    "BAD: Waiting for Initial Data"
    qGood: int
    "Neglect data in SE calculation if OPC quality is: GOOD"
    qGoodLocOver: int
    "Neglect data in SE calculation if OPC quality is GOOD: Local Override"
    qGoodNonSpec: int
    "Neglect data in SE calculation if OPC quality is GOOD: Non-specific"
    qUncerLastVal: int
    "Neglect data in SE calculation if OPC quality is UNCERTAIN: Last Usable Value"
    qUncerNonSpec: int
    "Neglect data in SE calculation if OPC quality is UNCERTAIN: Non-specific"
    qUncerNotAcc: int
    "Neglect data in SE calculation if OPC quality is UNCERTAIN: Sensor Not Accurate"
    qUncerSubNorm: int
    "Neglect data in SE calculation if OPC quality is UNCERTAIN: Sub-Normal"
    qUncerUnitExc: int
    "Neglect data in SE calculation if OPC quality is UNCERTAIN: Engineering Units Exceeded"
    qUncertain: int
    "Neglect data in SE calculation if OPC quality is: UNCERTAIN"
    repoptions: str
    "Alarm Object Identifier"
    root_id: object
    "Original Location"
    sComName: str
    "Computer Name"
    sProgID: str
    "Prog ID"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def LoadMicroSCADAFile(*args): ...

    def ReceiveData(*args): ...

    def SendData(*args): ...

    def SentDataStatus(*args): ...

    def SetOPCReceiveQuality(*args): ...

    def SetSwitchShcEventMode(*args): ...

    def __getattr__(*args): ...


class ComMerge(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    conApproval: int
    "Compare Options: Consider Approval Information"
    conflictMode: int
    "Merge: Assign"
    consAdded: int
    "Compare Options: Search correspondents for added objects"
    consCim: int
    "Compare Options: Consider CIM data"
    consDataExt: int
    "Compare Options: Consider Data Extensions"
    consOpd: int
    "Consider Operational Data"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    identifyByFKey: int
    "Compare Options: Identify correspondents by foreign key"
    identifyByName: int
    "Compare Options: Identify correspondents always by name/rules"
    iopt_3way: int
    "Compare: 2nd"
    loc_name: str
    "Name"
    merge: int
    "Merge"
    minThresh: float
    "Compare Options: Ignore differences <"
    name_base: str
    "Compare: as"
    name_mod1: str
    "Compare: as"
    name_mod2: str
    "Compare: as"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    target_2way: int
    "Merge: into"
    target_3way: int
    "Merge: into"
    tid_: int
    "TimeID"
    top_base: object
    "Compare: Base"
    top_mod1: object
    "Compare: 1st"
    top_mod2: object
    "Compare: 2nd"
    travmode: int
    "Compare Options: Depth :Only chosen Object :Chosen and contained Objects"

    def AttributeType(*args): ...

    def CheckAssignments(*args): ...

    def Compare(*args): ...

    def CompareActive(*args): ...

    def CompareRecording(*args): ...

    def Execute(*args): ...

    def ExecuteRecording(*args): ...

    def ExecuteWithActiveProject(*args): ...

    def GetCorrespondingObject(*args): ...

    def GetModification(*args): ...

    def GetModificationResult(*args): ...

    def GetModifiedObjects(*args): ...

    def HasReferences(*args): ...

    def Merge(*args): ...

    def PrintComparisonReport(*args): ...

    def PrintModifications(*args): ...

    def Reset(*args): ...

    def SetAutoAssignmentForAll(*args): ...

    def SetObjectsToCompare(*args): ...

    def ShowBrowser(*args): ...

    def WereModificationsFound(*args): ...

    def __getattr__(*args): ...


class ComMot(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    i_volt: int
    "Successful Starting Criterion for Simplified Models: Voltage Drop based on..."
    iopt_asc: int
    "Report"
    iopt_dflt: int
    "Simulation Method: User defined simulation settings"
    iopt_dss: int
    "Simulation Method: User defined simulation settings"
    iopt_maxv: int
    "Simulation Type: Use settings for Max. Voltage Drop"
    iopt_net: int
    "Simulation Method: Network Representation"
    iopt_rms: int
    "Simulation Method: RMS values (Electromechanical Transients)"
    iopt_styp: int
    "Simulation Type"
    iopt_thl: int
    "Check Thermal Limits of Cables and Transformers"
    iopt_view: int
    "Display results for:"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pMonBars: object
    "Monitoring: Additional Terminals"
    pMonCabs: object
    "Check Thermal Limits of Cables and Transformers: Additional Equipment"
    pMotor: object
    "Motor(s)"
    p_resrms: object
    "Results"
    p_resst: object
    "Report: Results"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    selected: list
    "Selected Elements"
    tid_: int
    "TimeID"
    time: float
    "Simulation Method: Simulation Time"
    tolspeed: float
    "Successful Starting Criterion for Simplified Models: Max. Speed Tolerance"
    tolvolt: float
    "Successful Starting Criterion for Simplified Models: Max. Voltage Drop"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetMotorConnections(*args): ...

    def GetMotorSwitch(*args): ...

    def GetMotorTerminal(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComNmink(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cntNameDef: int
    "Naming of created contingencies or fault cases"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    fr_elm: int
    "Network Components"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSaveto: int
    "Fault case folder"
    iSchemeStatus: int
    "Scheme Status"
    iopt_cmd: int
    "Creation of Contingencies"
    iopt_lev: int
    "Outage Level"
    iopt_lne: int
    "Network Components: Lines/cables"
    iopt_n1: int
    "Outage Level: n-1 cases"
    iopt_n2: int
    "Outage Level: n-2 cases"
    iopt_nc: int
    "Outage Level: n-k cases of mutually coupled lines/cables"
    iopt_scap: int
    "Network Components: Series Capacitors"
    iopt_sreac: int
    "Series Reactors"
    iopt_sym: int
    "Network Components: Generators"
    iopt_trf: int
    "Network Components: Transformers"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    optSel: int
    "Network Components: Create Cases for:Whole system:Selection:Filtered Elements"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sel_filter: object
    "Network Components: Filter"
    sel_folder: object
    "Fault case folder: Selected folder"
    sel_user: object
    "Network Components: Set"
    tid_: int
    "TimeID"

    def AddRef(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def Execute(*args): ...

    def GenerateContingenciesForAnalysis(*args): ...

    def GetAll(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComOmr(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_feed: int
    "Determine Optimal Manual Restoration for"
    loc_name: str
    "Name"
    num_level: int
    "Max. Number of Restoration Levels"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    order_BB: int
    "Backbone Order (Max.)"
    pid_: int
    "ProjectID"
    ref_comsh: object
    "Report: Output"
    ref_ldf: object
    "Load Flow"
    ref_selfeed: object
    "Determine Optimal Manual Restoration for: Feeders"
    res_out: int
    "Report"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    val_pwr: float
    "Min. Power in Pocket"
    val_wght: float
    "Penalty Factor: Branches end at Manual Switch"
    val_wght1: float
    "Penalty Factor: Non-Backbone Branches (Level I)"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetFeeders(*args): ...

    def GetOMR(*args): ...

    def GetRegionCount(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComOpc(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deadband: float
    "Deadband Usage: Deadband"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iPort: int
    "Server Port"
    iSchemeStatus: int
    "Scheme Status"
    idReplacement: str
    "TagID Placeholder"
    iopt_StorLoc: int
    "Storage location"
    iopt_auth: int
    "Authentication mode"
    iopt_db: int
    "DB Synchronisation"
    iopt_deadb: int
    "Deadband Usage"
    iopt_link: int
    "Link To"
    iopt_mode: int
    "Credentials"
    iopt_serverV: int
    " Verify server certificate"
    iopt_type: int
    "Mode"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    rootPath: str
    "Path to root element"
    root_id: object
    "Original Location"
    sComputerUrl: str
    "Server top - level URL"
    sPassword: str
    "Password"
    sServerName: str
    "Server sub - level URL"
    sSslCaRevoc: str
    "Revoked certificate storage"
    sSslCaTrust: str
    "Trusted certificate storage"
    sSslCertPath: str
    "Certificate"
    sSslIsRevoc: str
    "Revoked issuer certificate storage"
    sSslIsTrust: str
    "Trusted issuer certificate storage"
    sSslPkPass: str
    "Private key password"
    sSslPkPath: str
    "Private key"
    sUserName: str
    "Username"
    sWinStorName: str
    "Name of certificate folder"
    sWinThumbpr: str
    "Certificate thumbprint"
    tagSet: object
    " Points to transfer"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetCertificatePath(*args): ...

    def HasReferences(*args): ...

    def ReceiveData(*args): ...

    def SendData(*args): ...

    def __getattr__(*args): ...


class ComOutage(PFGeneral):
    BBFault: int
    "Busbar Fault"
    Branches: object
    "Branch"
    Couplers: list
    "Open"
    CouplersClose: list
    "Close"
    Elms: list
    "Name"
    Faults: list
    "Fault Location"
    IntState: list
    "State"
    Nodes: list
    "Name"
    addoptions: str
    "Additional Parameters"
    cFaultElm: object
    "Fault location"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cluster: int
    "Cluster"
    cn_k: list
    "Fault Type"
    contents: list
    "Events"
    cpCase: object
    "Fault Case"
    cpGroup: object
    "Fault Group"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iNoSupply: int
    "DC Generation/Demand:not changed:changed:changed by element not in table"
    iOneSide: int
    "Use equation at branch side (index)"
    iPsensOnly: int
    "Use P-sensitivities only"
    iSchemeStatus: int
    "Scheme Status"
    idynamic: int
    "Dynamic contingency"
    iopt_evts: str
    "Events used for this Contingency"
    loc_name: str
    "Name"
    n_k: int
    "Contingency Order"
    number: int
    "Number"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    outserv: int
    "Not analysed"
    pCase: object
    "Fault Case"
    pSWSC: list
    "Switch Scheme"
    pid_: int
    "ProjectID"
    restore: str
    "System Restoration"
    root_id: object
    "Original Location"
    studyTime: int
    "Study time of dynamic contingency"
    tid_: int
    "TimeID"
    year: int
    "Year"

    def AttributeType(*args): ...

    def ContinueTrace(*args): ...

    def Execute(*args): ...

    def ExecuteTime(*args): ...

    def GetObject(*args): ...

    def HasReferences(*args): ...

    def RemoveEvents(*args): ...

    def SetObjs(*args): ...

    def StartTrace(*args): ...

    def StopTrace(*args): ...

    def __getattr__(*args): ...


class ComPfdimport(PFGeneral):
    activatePrj: int
    "Import options: Activate project after import"
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    codepage: list
    "Import options: Text encoding"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    g_bases: list
    "Base projects and versions in original database"
    g_contents: list
    "File information: Contents"
    g_created: int
    "File information: Date and Time"
    g_creator: str
    "File information: Exported by"
    g_file: str
    "File information: PFD file"
    g_licinfo: list
    "(DIGSIDONGLE only) Licence information"
    g_noobjs: int
    "File information: Number of records"
    g_noprjs: int
    "File information: Number of projects"
    g_path: list
    "File information: Original Path"
    g_refs: list
    "File information: Missing or unreadable referenced objects"
    g_sourceVersion: str
    "File information: Source version"
    g_target: object
    "Import options: New Path"
    g_version: str
    "File information: Target version"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetImportedObjects(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComPrjconnector(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    identAttribute: str
    "Identify terminals by"
    loc_name: str
    "Name"
    method: str
    "Connection method"
    obj: str
    "Object Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    variationName: str
    "Store connections in Variation"
    vnodeGrid: object
    "Virtual nodes grid"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetSuccesfullyConnectedItems(*args): ...

    def GetUnsuccesfullyConnectedItems(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComProtgraphic(PFGeneral):
    addoptions: str
    "Additional Parameters"
    cCurrents: int
    "Create diagrams for: Currents"
    cDirAngles: int
    "Create diagrams for: Directional angles"
    cImpedances: int
    "Create diagrams for: Impedances"
    cReachBrushes: list
    "Brush Style"
    cReachDevices: list
    "Device"
    cReactances: int
    "Create diagrams for: Reactances"
    cSweep: object
    "Short-circuit sweep: Command"
    cSweepDevices: list
    "Device"
    cUpdatePages: list
    "Plot page"
    cVoltages: int
    "Create diagrams for: Voltages"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    createVars: int
    "Create diagrams for"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    devices: object
    "Protection devices: Selection"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_action: int
    "Action"
    iopt_pages: int
    "Update diagrams"
    loc_name: str
    "Name"
    loopSelection: int
    "Create diagrams for: Loop selection:&1&Phase-Earth:&2&Phase-Phase:&3&All"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    path: object
    "Path"
    pid_: int
    "ProjectID"
    reachBrushes: list
    "Brush Style"
    reachColours: list
    "Colour"
    reachDevices: list
    "Protection devices for reach colouring"
    reachWidth: float
    "Width factor"
    reachZones: list
    "Zone"
    reference: int
    "Create diagrams for: Reference frame:Secondary:Primary"
    root_id: object
    "Original Location"
    sweepDevices: list
    "Protection devices for sweep diagrams"
    thresholds: int
    "Create diagrams for: Add tripping thresholds"
    tid_: int
    "TimeID"
    updatePages: list
    "Plot pages"

    def AddToUpdatePages(*args): ...

    def AttributeType(*args): ...

    def ClearUpdatePages(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComPvcurves(PFGeneral):
    addoptions: str
    "Additional Parameters"
    calcCont: int
    "Consider contingencies"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    critFactor: float
    "Critical factor"
    critGrad: float
    "Critical gradient"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    debugOut: int
    "Show detailed output"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frIterMethd: int
    "Step size algorithm"
    frLoads: int
    "Scale loads"
    frScaleini: int
    "Initial load scaling"
    frSel_Busb: int
    "Record terminal results"
    frStepsize: int
    "Step size definition"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iniStepsize: float
    "Step size definition: Initial step size"
    iopt_clc: int
    "Calculation"
    loc_name: str
    "Name"
    maxIter: int
    "Step size definition: Maximum iterations"
    maxStepsize: float
    "Step size definition: Maximum step size"
    minStepsize: float
    "Step size definition: Minimum step size"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pInputCont: object
    "Consider contingencies: Contingency Analysis"
    pSel_Busb: object
    "Record terminal results: "
    pSel_Load: object
    "Scale loads: "
    pid_: int
    "ProjectID"
    results: object
    "Record terminal results: Results"
    root_id: object
    "Original Location"
    scaleMot: int
    "Scale loads: Scale motors"
    scaleNegLod: int
    "Scale loads: Scale negative loads"
    scaleini: float
    "Initial load scaling: Multiplication factor"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def FindCriticalBus(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComPython(PFGeneral):
    IntDesc: list
    "Description"
    IntExpr: list
    "Value"
    IntName: list
    "Name"
    IntResDesc: list
    "Description"
    IntResExpr: list
    "Value"
    IntResName: list
    "Name"
    IntResType: list
    "Type"
    IntResUnit: list
    "Unit"
    IntType: list
    "Type"
    IntUnit: list
    "Unit"
    addoptions: str
    "Additional Parameters"
    author: str
    "Author"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    company: str
    "Company"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    filePath: str
    "Script file"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    interfaceVersion: int
    "Interface Version:&1&1:&2&2"
    isRemoteScriptSet: int
    "A remote script is set."
    loc_name: str
    "Name"
    modifytime: int
    "Last Modified"
    obj_desc: list
    "Description"
    obj_id: list
    "Object"
    obj_name: list
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    scriptSourceChoice: int
    "Python Script"
    script_id: object
    "Remote script"
    shortDesc: str
    "Short Description"
    tid_: int
    "TimeID"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"
    version: str
    "Version"
    xDesc: list
    "Long Description"
    xNotes: list
    "Release Notes"
    xScript: list
    "Embedded Code"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetExternalObject(*args): ...

    def GetInputParameterDouble(*args): ...

    def GetInputParameterInt(*args): ...

    def GetInputParameterString(*args): ...

    def HasReferences(*args): ...

    def SetExternalObject(*args): ...

    def SetInputParameterDouble(*args): ...

    def SetInputParameterInt(*args): ...

    def SetInputParameterString(*args): ...

    def __getattr__(*args): ...


class ComRed(PFGeneral):
    addoptions: str
    "Additional Parameters"
    category: int
    "Subgroup generators: According to model type and plant category"
    charact: list
    "Charact."
    chkThrsh: float
    "Check equivalent results: Threshold for check"
    chr_name: str
    "Characteristic Name"
    cldf_rep: int
    "Equivalent model for power injection"
    cleanSub: int
    "Clean up empty substations and bays"
    considerSubPart: int
    "Schur topology optimisation settings: Consider subpartitions for optimisation"
    contents: list
    "Contents"
    copt_group: int
    "Aggregation of nonlinear elements"
    copt_new: int
    "Representation of equivalent"
    cpHeadFold: object
    "Head Folder"
    ctrlType: int
    "Subgroup generators: According to local controller"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    debugMode: int
    "Debug mode:Off:Calculate and output statistics:Write matrices:Advanced (plot graphs etc.)"
    debugRunMode: int
    "Only calculate reduced admittance matrix"
    elmRetain: object
    "Reduction of nonlinear elements: Additional elements"
    fixedNumPartitions: int
    "Schur topology optimisation settings: Number of partitions"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    genCategory: list
    "Category"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iCalcType: int
    "Calculation type:Load Flow:Quasi-Dynamic Simulation"
    iCheckSig: int
    "Signals to be checked"
    iChkSim: int
    "Check equivalent results: Check simulation results after reduction"
    iCoheOnly: int
    "Stop after coherency identification"
    iCoher: int
    "Coherency identification method"
    iControl: int
    "Create controllers for equivalent generators"
    iDisturb: int
    "Disturbance"
    iFicNet: int
    "Use fictitious border network"
    iFreqImp: int
    "Calculate equivalent parameters at all frequencies"
    iHdlPV: int
    "Use Extended Ward Equivalent for PV Boundary Nodes"
    iKeepNoise: int
    "Keep temporarily created noise elements"
    iLoad: int
    "Reduction of nonlinear elements: Loads:Retain all:Reduce all"
    iNegR: int
    "Handling of negative resistance"
    iOptBrch: int
    "Minimisation of equivalent branches"
    iOptBrchDbg: int
    "User defined parameters for minimisation of equivalent branches"
    iRedPart: int
    "To be reduced:Interior of the boundary:Exterior of the boundary"
    iSchemeStatus: int
    "Scheme Status"
    iSimPlot: int
    "Check equivalent results: Generate curve comparison plot"
    iStaGen: int
    "Reduction of nonlinear elements: Static generators:Retain all:Retain all voltage controlled:Reduce all"
    iSvs: int
    "Reduction of nonlinear elements: SVS:Retain all:Retain all voltage controlled:Reduce all"
    iSynGen: int
    "Reduction of nonlinear elements: Synchronous generators:Retain all:Retain all voltage controlled:Reduce all"
    iType: int
    "Reduction type"
    iWithPSTs: int
    "Creation of phase shifters for loop flows"
    identMethod: int
    "Optimisation method"
    identMethodLdf: int
    "Optimisation method"
    ignoreSign: int
    "Ignore active power flow direction"
    ildfMode: int
    "Load flow method:AC, balanced:DC"
    ildf_rep: int
    "Equivalent model for power injection"
    initR: float
    "Initial value of equivalent impedance: Resistance"
    initX: float
    "Initial value of equivalent impedance: Reactance"
    iopt_012: int
    "Calculate short-circuit equivalent: Asymmetrical representation"
    iopt_chk: int
    "Check equivalent results: Check load flow results after reduction"
    iopt_chkY: int
    "Check equivalent admittance"
    iopt_group: int
    "Aggregation of nonlinear elements"
    iopt_ldf: int
    "Calculate load flow equivalent"
    iopt_method: int
    "Method"
    iopt_new: int
    "Representation of equivalent"
    iopt_rep: int
    "Report Detail Level:Brief:Detailed:Full"
    iopt_save: int
    "Check deviation of operating point: Save original operating point to result file"
    iopt_shc: int
    "Calculate short-circuit equivalent"
    loc_name: str
    "Name"
    locations: list
    "Minimisation of interchange mismatch: Locations"
    lodType: int
    "Subgroup loads: According to load classification"
    loopUbFacs: int
    "Schur topology optimisation settings: Loop over unbalance factors"
    maxBrchImp: float
    "Mutual impedance: Ignore above"
    maxDist: int
    "Coherency identification method: Distance ratio threshold (max/avg)"
    maxPercentForPart: float
    "Schur topology optimisation settings: Max. num partitions (in perc. of reduce nodes)"
    maxUbFac: float
    "Schur topology optimisation settings: Maximal unbalance factor"
    minCorr: float
    "Coherency identification method: Correlation threshold"
    minUbFac: float
    "Schur topology optimisation settings: Min unbalance factor"
    nParam: list
    "Parameters to be tuned: Number of parameters: %d"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    out_msg: int
    "Show detailed output"
    pBound: object
    "Boundary"
    pInc: object
    "Initial Conditions"
    pIntMon: list
    "Signals"
    pRegions: object
    "Regions"
    pSim: object
    "Simulation"
    pTemplate: object
    "Template"
    p_ficNet: object
    "Use fictitious border network: Border network"
    paramIdent: int
    "Parameter Identification:"
    pid_: int
    "ProjectID"
    reiBusperStat: int
    "Single equivalent bus per substation"
    removeCon: int
    "Schur topology optimisation settings: Remove connections to equ. generator / load during optimisation"
    rmin: float
    "Min. Resistance rmin"
    root_id: object
    "Original Location"
    simMethod: int
    "Simulation method"
    subcategory: int
    "Subgroup generators: According to model type, plant category and subcategory"
    templates: list
    "Template"
    tid_: int
    "TimeID"
    topoOptAlg: int
    "Schur topology optimisation settings: Optimisation method:OLD:OLD2:ACTUAL"
    ubFacStep: float
    "Schur topology optimisation settings: Unbalance factor step"
    upBoundR: float
    "Upper bound of equivalent impedance: Resistance"
    upBoundX: float
    "Upper bound of equivalent impedance: Reactance"
    useFixedNumPartitions: int
    "Schur topology optimisation settings: Use fixed number of partitions"
    useOrigTermName: int
    "Additionally retained terminals: Use original names"
    var: str
    "Monitored signal"
    weight: list
    "Minimisation of interchange mismatch: Weight"
    weightFactor: int
    "Schur topology optimisation settings: Weight factor"
    weightNodes: int
    "Schur topology optimisation settings: Apply node weights according to communication with retain part"
    weightSummand: int
    "Schur topology optimisation settings: Weight summand"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def LdfEquivalentVerification(*args): ...

    def ReductionInMemory(*args): ...

    def ResetReductionInMemory(*args): ...

    def SimEquivalentVerification(*args): ...

    def __getattr__(*args): ...


class ComRel3(PFGeneral):
    AccessTime: float
    "Switching time for stage 2 and 3: Access Time to Substation"
    FisrRCSTime: float
    "Time to operate the first RCS"
    RCSMaxEvts: int
    "Switching time for remote controlled switches: Maximum number of switch actions"
    RCSTimeAvg: float
    "Switching time for remote controlled switches: Time between two RCS switch events"
    RCSdectime: float
    "Switching time for remote controlled switches: Time to decide restoration strategy"
    accStates: float
    "Accuracy"
    addObjs2Transfer: object
    "Parallel computation of contingencies: Additional objects to transfer"
    addOutLoops: int
    "Enhanced restoration"
    addoptions: str
    "Additional Parameters"
    boundaryConstr: int
    "Consider Boundary Constraints outside feeders"
    calcTime: int
    "Calculation time period: Calculation Point Time"
    calcYear: int
    "Calculation time period: Calculation Year"
    caseNum: str
    "Case number"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cond_lmax: float
    "Calculation of Loadshedding in Transmission Networks: Only consider branch if loading before shedding exceeds"
    considerRecl: int
    "Calculation of SAIFI/SAIDI according to IEEE 1366: Enhanced consideration of automatic reclosing devices"
    contents: list
    "Conting."
    cpHeadFold: object
    "Head Folder"
    createCont: int
    "Automatic Contingency Definition"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dep_protOver: int
    "Automatic Contingency Definition: Backup protection maloperation"
    detailedOutput: int
    "Show detailed output of initial load flow and top-level feeders."
    distrStates: object
    "Current Load Distribution States"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBackwRecover: int
    "Supplying substations: Backward recovery:Do not allow:Allow but prefer standard recovery:Allow with user-defined preference:Allow and prefer"
    iBusbarTransfer: int
    "Supplying substations: Busbar transfer:Simple reconnection:Optimised without additional meshes:Optimised with and without meshes"
    iCntRep: int
    "Number of Contingency cases in report"
    iEnableParal: int
    "Parallel computation of contingencies"
    iSchemeStatus: int
    "Scheme Status"
    ieee1366SAIFI: int
    "Calculation of SAIFI/SAIDI according to IEEE 1366: Do not consider interruptions shorter than or equal to"
    ioptRestore: int
    "Automatic Power Restoration"
    ioptSeparate: int
    "Fault Separation"
    iopt_2: int
    "Automatic Contingency Definition: Independent second failures"
    iopt_LS: int
    "Update/creation of States"
    iopt_ShowEvt: int
    "Define Event Objects"
    iopt_action: int
    "Processing Actions"
    iopt_avg: int
    "Calculate Average Switching Time"
    iopt_avgRCS: int
    "Calculate Average Switching Time for RCS"
    iopt_bar: int
    "Automatic Contingency Definition: Busbars / terminals"
    iopt_bcv: int
    "Stop calculation if base case is overloaded"
    iopt_cb4Prot: int
    "Fault Clearance Breakers: Use switches with protection device"
    iopt_cfin: int
    "Failures, correction of forced outage rate: fa' = fa/pa"
    iopt_cfrem: int
    "Failures, correction of forced outage rate: Distribute remaining rates:Off:On All:On n-2:On n-1"
    iopt_clc: int
    "Calculation"
    iopt_clus: int
    "Define Load States"
    iopt_common: int
    "Automatic Contingency Definition: Common mode"
    iopt_cpall: int
    "Correction of Probability:Mode 1:Mode 2:Mode 3:Mode 4"
    iopt_cross: int
    "Automatic Contingency Definition: Double earth faults"
    iopt_eice: int
    "Costs for energy not supplied"
    iopt_eicl: int
    "Costs for loads"
    iopt_evt: int
    "Switching:renew events:execute listed events"
    iopt_evts: int
    "Events created during restoration"
    iopt_fcb: str
    "Fault Clearance Breakers"
    iopt_gens: int
    "Automatic Contingency Definition: Generators"
    iopt_glob: int
    "Global Thermal Constraints"
    iopt_hmax: int
    "Scale to average load (HMAX/8760)"
    iopt_ign: int
    "Ignore all constraints for..."
    iopt_ldSet: int
    "Consider Thermal Constraints (Loading): Option"
    iopt_lims: int
    "Limited number"
    iopt_line: int
    "Automatic Contingency Definition: Lines / cables"
    iopt_load: int
    "Consider Thermal Constraints (Loading)"
    iopt_loads: int
    "Load Variations"
    iopt_locCst: int
    "Costs for loads: Cost curve (tariff)"
    iopt_maint: int
    "Consider Maintenance"
    iopt_mode: int
    "Mode:Monte-Carlo:State Enumeration"
    iopt_net: int
    "Network"
    iopt_net1: int
    "Network"
    iopt_noncorr: int
    "Ignore Load Correlation"
    iopt_out: int
    "Automatic Contingency Definition"
    iopt_prio: int
    "Load/Generator Priorities"
    iopt_prot: int
    "Automatic Contingency Definition: Protection/switching failures"
    iopt_prt4Prot: int
    "Fault Clearance Breakers"
    iopt_rep: int
    "Report"
    iopt_rndseed: int
    "Random numbers:auto:A:B:C:D:E:F:G:H:I:K"
    iopt_sec: int
    "Switching procedures for fault separation/power restoration: Consider Sectionalising (Stages 1-3)"
    iopt_shunt: int
    "Automatic Contingency Definition: Shunts/Filters/Ser. Impedances"
    iopt_swt: int
    "By switching actions"
    iopt_time: int
    "Switching procedures for fault separation/power restoration"
    iopt_trf: int
    "Automatic Contingency Definition: Transformers"
    iopt_type: int
    "Method"
    iopt_vdSet: int
    "Consider Voltage Drop/Rise: Option"
    iopt_vdrop: int
    "Consider Voltage Drop/Rise"
    iopt_vlSet: int
    "Consider Voltage Limits: Option"
    iopt_vol: int
    "Consider Voltage Limits"
    levConf: float
    "Confidence"
    loadTariff: object
    "Costs for loads Cost curve (tariff): Tariff"
    loadmax: float
    "Consider Thermal Constraints (Loading): Maximum thermal loading of components"
    loc_name: str
    "Name"
    manMaxEvts: int
    "Switching time for stage 2 and 3: Maximum number of switch actions"
    manTime: float
    "Switching time for stage 2 and 3: Time to operate manual switch"
    manTimeAvg: float
    "Switching time for stage 2 and 3: Average time to operate manual switch"
    maxVdrop: float
    "Consider Voltage Drop/Rise: Maximum Voltage Drop"
    maxVrise: float
    "Consider Voltage Drop/Rise: Maximum Voltage Rise"
    maxld_n1: float
    "Maximum thermal loading of edge element"
    maxld_nk: float
    "n-k; k>=2"
    minTasks4Par: int
    "Parallel computation of contingencies: Minimum number of contingencies"
    mxErr: float
    "Max. error"
    mxN: int
    "Max. runs"
    mxldany: float
    "Global Thermal Constraints: Maximum Loading of Other Components"
    mxldcab: float
    "Global Thermal Constraints: Maximum Loading of Cables"
    mxldlne: float
    "Global Thermal Constraints: Maximum Loading of Overhead Lines"
    mxldtrf: float
    "Global Thermal Constraints: Maximum Loading of Transformers"
    num_states: int
    "Max. number of load states"
    oid_: int
    "ObjectID"
    optSel: int
    "Automatic Contingency Definition: Selection:Whole System:User Defined"
    optimize: int
    "Tie Open Point Optimisation: Optimisation:Disabled:Enabled without load transfer:Enabled with load transfer"
    optimize1: int
    "Tie Open Point Optimisation: Stage 1:Disabled:Enabled without load transfer:Enabled with load transfer"
    optimize2: int
    "Tie Open Point Optimisation: Stage 2:Disabled:Enabled without load transfer:Enabled with load transfer"
    optimize3: int
    "Tie Open Point Optimisation: Stage 3:Disabled:Enabled without load transfer:Enabled with load transfer"
    order: float
    "Order"
    ovl_relax: float
    "Stop calculation if base case is overloaded: Relax constraints of initially overloaded elements by"
    p_event: object
    "Events"
    p_resenum: object
    "Results"
    p_resvar: object
    "Results"
    paralSet: int
    parallelSetting: object
    "Parallel computation of contingencies: Parallel computation settings"
    pid_: int
    "ProjectID"
    reclimLoad: float
    "Max. thermal loading of components"
    refTime: int
    "Load Variations: Reference time for characteristics"
    restoration: list
    "Optimal Power Restoration Settings per Stage"
    root_id: object
    "Original Location"
    sel_backwRec: object
    "Supplying substations: Substations preferring backw. recovery"
    sel_grid: object
    "Grid"
    sel_user: object
    "Automatic Contingency Definition: Selection"
    spon_protOver: int
    "Automatic Contingency Definition: Spurious protection operation"
    states: object
    "Current Load States"
    tRemoteCB: float
    "Time to actuate remote controlled switches"
    t_end: int
    "Stop year"
    t_start: int
    "Start year"
    tid_: int
    "TimeID"
    timePeriod: int
    "Calculation time period"
    totTariff: object
    "Costs for energy not supplied: Tariff"
    traceDelay: int
    "Trace Functionality (Jump to Last Step): Time delay in animation"
    upd_time: float
    "Post contingency time for order identification"
    use_existing: int
    "Calculate existing contingencies"
    vlevconst: float
    "Ignore all constraints for...: Nominal voltage below or equal to"
    vlmax: float
    "Upper limit of allowed voltage"
    vlmax_ldf: float
    "Consider Voltage Limits: Upper limit of allowed voltage"
    vlmin: float
    "Lower limit of allowed voltage"
    vlmin_ldf: float
    "Consider Voltage Limits: Lower limit of allowed voltage"
    vmax_n1: float
    "Upper limit of allowed voltage"
    vmax_nk: float
    "Max. (n-k; k>=2)"
    vmax_step: float
    "Max. voltage step; Contingency to base case"
    vmin_n1: float
    "Lower limit of allowed voltage"
    vmin_nk: float
    "Min. (n-k; k>=2)"

    def AnalyseElmRes(*args): ...

    def AttributeType(*args): ...

    def ExeEvt(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def OvlAlleviate(*args): ...

    def RemoveEvents(*args): ...

    def RemoveOutages(*args): ...

    def ValidateConstraints(*args): ...

    def __getattr__(*args): ...


class ComRelpost(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    comRel3: object
    "Reliability calculation"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frLoads: int
    "Calculate contributions to load interruptions"
    frOutput: int
    "Create report for component classes"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pSelObj: object
    "Calculate contributions to load interruptions: "
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CalcContributions(*args): ...

    def Execute(*args): ...

    def GetContributionOfComponent(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComRelreport(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_3ca: int
    "ASCII Report: Node interruptions"
    iopt_3comp: int
    "ASCII Report: Contribution of component classes"
    iopt_3in: int
    "ASCII Report: Load interruptions"
    iopt_3ss: int
    "ASCII Report: System Summary"
    iopt_mde: int
    "Output as"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    reportTitle: object
    "ASCII Report: Title of report"
    root_id: object
    "Original Location"
    tab_ASIDI: int
    "Tabular report of Contributions Contributions to: ASIDI"
    tab_ASIFI: int
    "Tabular report of Contributions Contributions to: ASIFI"
    tab_EIC: int
    "Tabular report of Contributions Contributions to: EIC"
    tab_ENS: int
    "Tabular report of Contributions Contributions to: ENS"
    tab_SAIDI: int
    "Tabular report of Contributions Contributions to: SAIDI"
    tab_SAIFI: int
    "Tabular report of Contributions Contributions to: SAIFI"
    tabularReport: int
    "Tabular report of Contributions"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetContingencies(*args): ...

    def GetContributionOfComponent(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComRes(PFGeneral):
    addoptions: str
    "Additional Parameters"
    cStep: float
    "Step size"
    cfrom: float
    "Interval: from"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciopt_head: int
    "Column header: Variable"
    ciopt_real: int
    "Time format"
    ciopt_sec: int
    "Time format"
    col_Sep: str
    "Use system separators: Separator for columns"
    cpHeadFold: object
    "Head Folder"
    cscl_start: float
    "Shift time: New start time"
    cto: float
    "Interval: to"
    cvariable: list
    "Variable selection: Variable"
    dSampling: float
    "Sampling frequency"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    database: object
    "Database"
    dec_Sep: str
    "Use system separators: Decimal separator"
    decseprtr: str
    "Decimal separator"
    element: list
    "Variable selection: Element"
    f_name: str
    "File name"
    filter: list
    "Filters"
    filtered: int
    "Interval: Filters"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    funAutoSampling: int
    "Automatic sampling from function objects"
    funSamplingRate: float
    "Samplingrate for function objects"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSampling: int
    "Sampling frequency"
    iSchemeStatus: int
    "Scheme Status"
    iopt_csel: int
    "Variable selection"
    iopt_exp: int
    "Export to"
    iopt_fkey: int
    "Use foreign key"
    iopt_hdct: int
    "Variable"
    iopt_head: int
    "Variable"
    iopt_honly: int
    "Object header only"
    iopt_inloc: int
    "Column header: Export from"
    iopt_locn: int
    "Column header: Element"
    iopt_newx: int
    "Points in Time"
    iopt_rscl: int
    "Shift time"
    iopt_sep: int
    "Use system separators"
    iopt_sort: int
    "Variable selection: Sorting"
    iopt_time: int
    "Time Format"
    iopt_tsel: int
    "Interval: User-defined interval"
    iopt_vars: int
    "Export"
    loc_name: str
    "Name"
    nsteps: int
    "Interval: n"
    numberFormat: int
    "Number format"
    numberPrecisionFixed: int
    "Decimal places"
    numberPrecisionScientific: int
    "Significant digits"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pResult: object
    "Export from"
    pid_: int
    "ProjectID"
    r_from: list
    "Interval: from"
    r_to: list
    "Interval: to"
    resultobj: list
    "Variable selection: Result object"
    root_id: object
    "Original Location"
    scl_start: float
    "Shift time: New start time"
    scols: str
    "Columns"
    separator: str
    "Separator for columns"
    tablename: list
    "Table name"
    tid_: int
    "TimeID"
    timeRefObj: object
    "Time ref."
    timeSclObj: object
    "Leading object"
    to: float
    "Interval: to"
    variable: list
    "Variable"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def ExportFullRange(*args): ...

    def FileNmResNm(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComShc(PFGeneral):
    Lf: float
    "Fault Impedance: Inductance, Lf"
    Rf: float
    "Fault Impedance: Resistance, Rf"
    Rfle: float
    "Fault Impedance: Resistance, Rf(L-E)"
    Rfll: float
    "Fault Impedance: Resistance, Rf(L-L)"
    Rjoint: float
    "Joint resistance for lines: Joint resistance"
    Ta: float
    "Calculate Using: Break Time"
    Tdc: float
    "Time Tdc"
    Tk: float
    "Short-Circuit Duration: Fault Clearing Time (Ith)"
    Tk_dc: float
    "Short-Circuit Duration: Short-circuit duration (Tk)"
    UnomACFed: int
    "Nominal Voltage of AC Feeder"
    Xf: float
    "Fault Impedance: Reactance, Xf"
    Xfle: float
    "Fault Impedance: Reactance, Xf(L-E)"
    Xfll: float
    "Fault Impedance: Reactance, Xf(L-L)"
    addoptions: str
    "Additional Parameters"
    ansi_30c: int
    "Calculate: 30 Cycle Current"
    ansi_int: int
    "Calculate: Interrupting Current"
    ansi_lvc: int
    "Low-Voltage Current"
    ansi_mom: int
    "Calculate: Momentary Current"
    ansi_sys: int
    "Calculate: System"
    ansipref: float
    "Pre-fault Voltage"
    bypasscap: int
    "Bypass Series Capacitance"
    cfac: float
    "Voltage factor c: Equivalent voltage source factor"
    cfacMax: float
    "For max. short-circuit current calculation"
    cfacMin: float
    "For min. short-circuit current calculation"
    cfac_dc: float
    "Initialisation: Pre-fault voltage factor"
    cfac_def: int
    "User defined c factor"
    cfac_full: float
    "Initialisation: Voltage factor c"
    cfac_min: float
    "Equivalent voltage source factor"
    cfac_use: int
    "Used:global:local"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    curerr: float
    "Current Iteration: Acceptable Current Error"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBrkTime: int
    "Short-Circuit Duration: Used Break Time:global:min. of local:local"
    iEnhancedZf: int
    "Fault Impedance: Enhanced Fault Impedance Definition"
    iIgnLneCap: int
    "Ignore positive sequence data: Capacitance of Lines"
    iIgnLoad: int
    "Ignore positive sequence data: Loads"
    iIgnShnt: int
    "Ignore positive sequence data: Shunts/Filters and SVS"
    iIgnTrfMag: int
    "Ignore positive sequence data: Magnetising current of transformers"
    iIksForProt: int
    "Calculate relay tripping with:Subtransient Values:Transient Values:Mixed Mode"
    iMotor4Min: int
    "Consider motors for min. short-circuit calculation"
    iOhlMod: int
    "Overhead Line Modelling: Phase Matrices"
    iSchemeStatus: int
    "Scheme Status"
    i_autopsu: int
    "Power Station Unit Detection: Automatic"
    i_lvtol: int
    "Max. Voltage Tolerance for LV-Systems:6:10"
    i_lvtolDc: int
    "Max. Voltage Tolerance for LV-Systems:6:10"
    i_p2pgf: int
    "Phases:a,b:b,c:c,a"
    i_p2psc: int
    "Phases:a-b:b-c:c-a"
    i_pspgf: int
    "Phase:a:b:c"
    iecDc_pub: int
    "Published:2016:2001:1990"
    iec_pub: int
    "Published:2016:2001:1990"
    ignMVInfeed: int
    "Ignore MV Infeeds"
    iinftag: int
    "Assume Inertia as infinite"
    iiterMethod: int
    "Current Iteration"
    ildfinit: int
    "Initialisation: Load Flow Initialisation"
    ildfinitdc: int
    "Load Flow Initialisation"
    ionlysubtrans: int
    "Skip transient calculation"
    iopt_Using: int
    "Approximate equivalent rectifier resistance value"
    iopt_allbus: int
    "Fault Location: At:User Selection:Busbars and Junction Nodes:All Busbars"
    iopt_asc: int
    "Show Output"
    iopt_brc: int
    "Calculate max. Branch Currents = Busbar Currents"
    iopt_calc: int
    "Grid Identification"
    iopt_calcAcImp: int
    "Calculate AC Network Impedance"
    iopt_cdef: int
    "Voltage factor c"
    iopt_check: int
    "Verification"
    iopt_cnf: int
    "Multiple Faults"
    iopt_cur: int
    "Calculate"
    iopt_dfr: int
    "Short-Circuit at Branch/Line: Fault Distance from"
    iopt_idc: int
    "Decaying Aperiodic Component (idc): Using Method:B:C:C'"
    iopt_ikdig: int
    "Calculate Ik:Ignore Motor Contributions:DIgSILENT Method:Without Motors"
    iopt_jointres: int
    "Joint resistance for lines"
    iopt_loopres: int
    "Apply line loop impedance"
    iopt_mde: int
    "Method"
    iopt_meth61363: int
    "Calculate Using"
    iopt_mot: int
    "Asynchronous Motors"
    iopt_out: int
    "Show Output: Output as"
    iopt_peak: str
    "Peak Short-Circuit Current (ip): Using Method:B:C(1):C(012):-"
    iopt_peak_full: str
    "Peak, DC Currents, R/X ratio (ip, ib, idc): Using Method:B:C(1):C(012):-"
    iopt_plot: int
    "Create plots"
    iopt_popt: int
    "Create plots: Show:only short-circuit current at faulted terminal:all short-circuit current contributions"
    iopt_preload: int
    "Preload Condition"
    iopt_prot: int
    "Consider Protection Devices:none:all:main:backup"
    iopt_saveRes: int
    "Store Results"
    iopt_shc: str
    "Fault Type"
    iopt_tap: int
    "Consider Transformer Taps"
    iopt_tdef: int
    "Conductor Temperature: User Defined"
    loadIb: float
    "Check Devices: Max. Loading (Interrupting)"
    loadIp: float
    "Check Devices: Max. Loading (Peak)"
    loadIth: float
    "Check Devices: Max. Loading (Thermal)"
    loc_name: str
    "Name"
    maxgenvol: float
    "Power Station Unit Detection: Consider generators <"
    maxiter: int
    "Current Iteration: Max. number of Iterations"
    maxlenpsu: float
    "Power Station Unit Detection: Maximum search distance over lines <"
    nacdmode: int
    "NACD Mode:Interpolated:Predominant:All Remote:All Local"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pDCRes: object
    "Results"
    p_cfactor: object
    "Voltage factor c: Table"
    p_event: object
    "Fault Location: Short-Circuits"
    p_simres: object
    "Create plots: Results"
    p_simres_emt: object
    "Simulation Results"
    pabs: float
    "Short-Circuit at Branch/Line: Absolute:"
    pid_: int
    "ProjectID"
    ppro: float
    "Short-Circuit at Branch/Line: Relative:"
    prot_chcur: str
    "Currents/Voltages for"
    root_id: object
    "Original Location"
    shcobj: object
    "Fault Location: User Selection"
    temp: float
    "Conductor Temperature: Temperature"
    tid_: int
    "TimeID"
    transtime: float
    "Subtransient Time"
    xtor_calc: int
    "X/R Calculation:Separate R and X:Complex"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def ExecuteRXSweep(*args): ...

    def GetFaultType(*args): ...

    def GetOverLoadedBranches(*args): ...

    def GetOverLoadedBuses(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComShctrace(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    deltaT: float
    "Settings: Simultaneous Trip Tolerance"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    p_event: object
    "Short-Circuit: Events"
    p_shc: object
    "Short-Circuit: Command"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def BlockSwitch(*args): ...

    def Execute(*args): ...

    def ExecuteAllSteps(*args): ...

    def ExecuteInitialStep(*args): ...

    def ExecuteNextStep(*args): ...

    def GetBlockedSwitches(*args): ...

    def GetCurrentTimeStep(*args): ...

    def GetDeviceSwitches(*args): ...

    def GetDeviceTime(*args): ...

    def GetNonStartedDevices(*args): ...

    def GetStartedDevices(*args): ...

    def GetSwitchTime(*args): ...

    def GetTrippedDevices(*args): ...

    def HasReferences(*args): ...

    def NextStepAvailable(*args): ...

    def __getattr__(*args): ...


class ComSim(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cominc: object
    "Initial conditions"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dtstop: float
    "Stop time: Relative"
    dynw: int
    "Internal Dynamic Model warnings"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iTrialMsg: int
    "Display messages during trial step (do check text)"
    iopt_action: int
    "Processing Actions"
    iopt_auto: int
    "Display in output window: Display automatic step size adaptation events"
    iopt_dbev: int
    "Display in output window: Display internal DSL events"
    iopt_dslw: int
    "Internal Dynamic Model warnings"
    iopt_show: int
    "Display in output window: Display result variables"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    tstop: float
    "Stop time: Absolute"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetSimulationTime(*args): ...

    def GetTotalWarnA(*args): ...

    def GetTotalWarnB(*args): ...

    def GetTotalWarnC(*args): ...

    def GetViolatedScanModules(*args): ...

    def HasReferences(*args): ...

    def LoadSimulationState(*args): ...

    def LoadSnapshot(*args): ...

    def SaveSimulationState(*args): ...

    def SaveSnapshot(*args): ...

    def __getattr__(*args): ...


class ComSimoutage(PFGeneral):
    PostContTime: float
    "Calculation Settings: Post Contingency Time (End of Time Phase)"
    PostContTime1: float
    "Calculation Settings: Post Contingency Time (End of Time Phase)"
    PostContTime2: float
    "Calculation Settings: Post Contingency Time (End of Time Phase)"
    PostContTime3: float
    "Calculation Settings: Post Contingency Time (End of Time Phase)"
    SleepTime: int
    "Sleep time in main loop of master"
    addObjs2Transfer: object
    "Settings for Parallel Computation: Additional objects to transfer"
    addSumResults: int
    "Element and variable selection: Record additional result variables"
    addoptions: str
    "Additional Parameters"
    bIgnoreTime: list
    "Definition of Study Times: Ignore"
    blockSize: int
    "Settings for Parallel Computation: Package Size for Optimised Method"
    blockSizeDC: int
    "Settings for Parallel Computation: Package Size for Optimised Method"
    caseNum: list
    "Contingency Number"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    copt_Linear: int
    "Calculation Method"
    copt_cntldf: int
    "Recording filters for contingency voltage results: Base Case versus Contingency Load Flow"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    diffLoadBase: float
    "Recording filters for contingency loading results: Do not record if the absolute change in loading is below"
    diffLoadRestr: int
    "Recording filters for contingency loading results: Do not record if the absolute change in loading is below"
    diffVoltBase: float
    "Recording filters for contingency voltage results: Do not record if the absolute change in voltage is below"
    diffVoltRestr: int
    "Recording filters for contingency voltage results: Do not record if the absolute change in voltage is below"
    dynamicCase: int
    "Dynamic contingencies"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    forceStd: int
    "Always use standard method"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iACDCCombine: int
    "AC/DC Combined (hidden)"
    iBusFaultProc: int
    "Handling of busbar fault"
    iConsSwSc: int
    "Consider Switching Rules of Substations"
    iDynamicMode: int
    "Contingencies to be calculated"
    iEnableParal: int
    "Parallel Computation of AC Contingencies"
    iEnableParalDC: int
    "Parallel Computation of DC Contingencies"
    iEnableParalTS: int
    "Parallel Computation of Time Sweep"
    iEnableTS: int
    "Calculate Time Sweep"
    iIgnCriticalBC: int
    "Criteria for AC recalculation of critical cases: Ignore components that are overloaded in base case"
    iMsgOutput: int
    "Output per Contingency Case"
    iNewTopo: int
    "Topology rebuild"
    iOk: int
    "Ok flag"
    iPerformOpt: int
    "Contingency Analysis for specific region"
    iQBEffMeth: int
    "Calculate Quad Booster Effectiveness: Calculation method"
    iRecalcBase: int
    "Contingency Analysis for specific region: Recalculate base case load flow for the whole system"
    iRedUnsupplied: int
    "Node Reduction Mode: Additionally remove unsupplied components"
    iSchemeStatus: int
    "Scheme Status"
    iShowDebug: int
    "Display debug information"
    iStopIfOverLd: int
    "Stop contingency analysis if any thermal loading constraint is violated."
    iStopIfVlim: int
    "Stop contingency analysis if any voltage constraint is violated."
    iUpdt: int
    "Update Contingencies before running calculation"
    i_gensens: int
    "Calculate Generator Effectiveness"
    i_qbsens: int
    "Calculate Quad Booster Effectiveness"
    iopt_Linear: int
    "Calculation Method"
    iopt_Shw: int
    "Print report for each contingency"
    iopt_action: int
    "Processing Actions"
    iopt_asc: int
    "Print summary report"
    iopt_cntldf: int
    "Base Case versus Contingency Load Flow"
    iopt_cnttime: int
    "Calculation Settings: Consider Specific Time Phase"
    iopt_evts: int
    "Recording filters for contingency voltage results: Method:Single Time Phase:Multiple Time Phases"
    iopt_init: int
    "Initialisation of Contingencies"
    iopt_method: int
    "Calculation Method"
    iopt_noloss: int
    "Assume loss-free components"
    iopt_record: int
    "Recording filters for contingency loading results: Do not record if the base case loading is above"
    isPlannedOutages: int
    "Planned outages"
    loadmax: float
    "Limits for recording: Record thermal loadings above"
    loadmax_nk: float
    "Limits for recording: Record thermal loadings above"
    loc_name: str
    "Name"
    maxLoad: float
    "Criteria for AC recalculation of critical cases: Thermal loading of components exceeds"
    maxLoadAbs: float
    "Criteria for AC recalculation of critical cases: Thermal loading of components exceeds"
    maxLoadBase: float
    "Recording filters for contingency loading results: Do not record if the base case loading is above"
    maxVoltBase: float
    "Recording filters for contingency voltage results: Do not record if the absolute base case voltage is above"
    maxVoltRestr: int
    "Recording filters for contingency voltage results: Do not record if the absolute base case voltage is above"
    maxld_nk: float
    "n-k; k>=2"
    minCntcyAC: int
    "Settings for Parallel Computation: Minimum number of contingencies"
    minCntcyDC: int
    "Settings for Parallel Computation: Minimum number of contingencies"
    minCtParal: int
    "Settings for Parallel Computation: Minimum number of defined study times"
    minVoltBase: float
    "Recording filters for contingency voltage results: Do not record if the absolute base case voltage is below"
    minVoltRestr: int
    "Recording filters for contingency voltage results: Do not record if the absolute base case voltage is below"
    numDegree: int
    "Contingency Analysis for specific region: Region extension by k-neighbourhood"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pFilter: object
    "Dynamic contingencies: Filters"
    pRegion: object
    "Contingency Analysis for specific region: Monitored region"
    p_rescnt: object
    "Element and variable selection: AC-Results"
    p_rescntDC: object
    "Element and variable selection: DC-Results"
    parallelSetting: object
    "Parallel computation settings"
    pid_: int
    "ProjectID"
    rasActive: int
    "Consider Remedial Action Schemes (RAS)"
    rasOutput: int
    "Output per Contingency Case: Show triggered RAS for each contingency in output window"
    recLimit_nk: int
    "Limits for recording: Different limits for n-1 and n-k (k>1)"
    recTermLoad: int
    "Record busbars/terminals with a loading above"
    root_id: object
    "Original Location"
    scrCritComb: int
    "Criteria for AC recalculation of critical cases: Combined loading criteria"
    scrCritSimple: int
    "Criteria for AC recalculation of critical cases: Simple loading criterion"
    screenRecOnly: int
    "Criteria for AC recalculation of critical cases: Screen only recorded elements"
    screeningMeth: int
    "Screening Method"
    sensMethod: int
    "Linearised method:Direct method:Backsubstitution (AC only)"
    sensThreshBra: float
    "Sensitivity threshold used for linearised method: Minimal considered branch sensitivity"
    sensThreshBus: float
    "Sensitivity threshold used for linearised method: Minimal considered bus sensitivity"
    setExclude: object
    "Criteria for AC recalculation of critical cases: Components to be ignored"
    stdBlockSize: int
    "Settings for Parallel Computation: Package Size for Standard Method"
    stdBlockSizeDC: int
    "Settings for Parallel Computation: Package Size for Standard Method"
    stepLoad: float
    "Criteria for AC recalculation of critical cases: Relative change of loading exceeds"
    studyTime: list
    "Definition of Study Times: Study Time"
    termLoadThres: float
    "Also record busbars/terminals with a loading above"
    tid_: int
    "TimeID"
    timePhases: list
    "Time Phases"
    upd_time: float
    "Post contingency time for order identification"
    useSensMethod: int
    "Use linearised method where applicable"
    vlmax: float
    "Limits for recording: Record if absolute voltage is above"
    vlmax_nk: float
    "Limits for recording: Record if absolute voltage is above"
    vlmin: float
    "Limits for recording: Record if absolute voltage is below"
    vlmin_nk: float
    "Limits for recording: Record if absolute voltage is below"
    vmax_nk: float
    "Max. (n-k; k>=2)"
    vmax_step: float
    "Limits for recording: Record voltage step changes above"
    vmax_step_nk: float
    "Limits for recording: Record voltage step changes above"
    vmin_nk: float
    "Min. (n-k; k>=2)"

    def AddCntcy(*args): ...

    def AddContingencies(*args): ...

    def AddRas(*args): ...

    def AttributeType(*args): ...

    def ClearCont(*args): ...

    def CreateFaultCase(*args): ...

    def Execute(*args): ...

    def ExecuteAndCheck(*args): ...

    def GetNTopLoadedElms(*args): ...

    def HasReferences(*args): ...

    def MarkRegions(*args): ...

    def RemoveAllRas(*args): ...

    def RemoveContingencies(*args): ...

    def RemoveRas(*args): ...

    def Reset(*args): ...

    def SetLimits(*args): ...

    def Update(*args): ...

    def __getattr__(*args): ...


class ComSvgexport(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    coordType: int
    "Coordinates"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fileName: str
    "SVG File"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    objects: list
    "Object"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    projection: str
    "Coordinates: Projection Type"
    root_id: object
    "Original Location"
    scaleCoord: int
    "Coordinates: Export to Version < 22"
    tid_: int
    "TimeID"
    utmZone: list
    "Coordinates: UTM-Zone (e.g. 32N)"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def SetFileName(*args): ...

    def SetObject(*args): ...

    def SetObjects(*args): ...

    def __getattr__(*args): ...


class ComSvgimport(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fileName: str
    "SVG File"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    object: object
    "Object"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def SetFileName(*args): ...

    def SetObject(*args): ...

    def __getattr__(*args): ...


class ComTasks(PFGeneral):
    addObjs2Transfer: object
    "Parallel computation: Additional objects to transfer"
    addoptions: str
    "Additional Parameters"
    caseNum: str
    "Package index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dbSyncTime: float
    "Database changes of parallel processes: Database synchronisation time"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iEnableParal: int
    "Parallel computation"
    iSchemeStatus: int
    "Scheme Status"
    iopt_action: int
    "Processing actions"
    isForcedDbSync: int
    "Database changes of parallel processes: Database synchronisation time"
    listCases: int
    "Selection of commands/additional results: Study case"
    loc_name: str
    "Name"
    minTasks4Par: int
    "Parallel computation: Minimum number of packages"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    outMsgMode: int
    "Output per package"
    parMethod: int
    "Distribute packages"
    parallelSetting: object
    "Parallel computation: Parallel computation settings"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    transDbChanges: int
    "Database changes of parallel processes"
    vecCases: list
    "Selection of study cases: Study cases"
    vecCasesIgn: list
    "Selection of study cases: Ignore"

    def AppendCommand(*args): ...

    def AppendStudyCase(*args): ...

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetCommandsForStudyCase(*args): ...

    def GetNumberOfCommandsForStudyCase(*args): ...

    def GetNumberOfStudyCases(*args): ...

    def GetStudyCases(*args): ...

    def HasReferences(*args): ...

    def IsAdditionalResultsFlagSetForCommand(*args): ...

    def IsCommandIgnored(*args): ...

    def IsStudyCaseIgnored(*args): ...

    def RemoveCmdsForStudyCaseRow(*args): ...

    def RemoveCommand(*args): ...

    def RemoveStudyCase(*args): ...

    def RemoveStudyCases(*args): ...

    def SetAdditionalResultsFlagForCommand(*args): ...

    def SetIgnoreFlagForCommand(*args): ...

    def SetIgnoreFlagForStudyCase(*args): ...

    def SetResultsFolder(*args): ...

    def __getattr__(*args): ...


class ComTececo(PFGeneral):
    CalcPoints: int
    "Calculation Points: Calculate"
    ColCosts: list
    "Costs for Losses: Costs"
    ColHmax: list
    "Costs for Losses: Hmax"
    CostsLLoss: float
    "Costs for losses: Costs for Losses (Load)"
    CostsnLLoss: float
    "Costs for losses: Costs for Losses (no Load)"
    DateUserDef: list
    "Calculation Points: Date"
    End: int
    "Calculation Points Calculation Period: End"
    InitAddCosts: float
    "Additional annual costs"
    InterestRate: float
    "Additional Settings: Calculatory Interest Rate"
    Start: int
    "Calculation Points Calculation Period: Start"
    addObjs2Transfer: object
    "Parallel computation: Additional objects to transfer"
    addoptions: str
    "Additional Parameters"
    caseNum: str
    "Case number"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frm_Interrupt: int
    "Interruption Costs"
    frm_LineOut: int
    "Interruption Costs - Costs for Outages on Lines/Cables"
    frm_Losses: int
    "Losses"
    frm_Report: int
    "Report"
    frm_SubOut: int
    "Interruption Costs - Costs for Outages in Substations"
    frm_Tie: int
    "Optimise Tie Open Points"
    frm_UserCosts: int
    "User-defined Costs"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iCreated: int
    "ComTececo Command has already been created"
    iEnableParal: int
    "Parallel computation"
    iLdGrowth: int
    "Additional Settings: Incorporate load growth"
    iSchemeStatus: int
    "Scheme Status"
    iTolerance: int
    "Additional Settings: Tolerance for Calculation Points (in days)"
    iUseSel: int
    "Costs for losses: Consider user-defined set of substations/feeders only"
    iopt_action: int
    "Processing Actions"
    loc_name: str
    "Name"
    minCalcPt4Par: int
    "Parallel computation: Minimum number of calculation points"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    outputType: int
    "Output"
    pComStatsim: object
    "Losses: Quasi-Dynamic Simulation"
    pDPL: object
    "User-defined Costs: Cost Assessment Script"
    pRel3: object
    "Interruption Costs: Reliability Assessment"
    pRel3SubOut: object
    "Interruption Costs - Costs for Outages in Substations: Reliability Assessment"
    pRes: object
    "Results"
    pSel: object
    "Costs for losses: Selection"
    pTie: object
    "Optimise Tie Open Points: Tie Open Point Optimisation"
    paralSet: int
    parallelSettings: object
    "Parallel computation: Parallel computation settings"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def UpdateTablesByCalcPeriod(*args): ...

    def __getattr__(*args): ...


class ComTececocmp(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    isCalcComTececo: int
    "Tasks: Run Techno-economical calculations"
    isCreateSummaryPlots: int
    "Tasks: Create plots for summary results"
    isCreateSummaryRes: int
    "Tasks: Create summary result file"
    isCreateTimesweepPlots: int
    "Tasks: Create plots for timesweep results"
    isCreateTimesweepRes: int
    "Tasks: Create timesweep result files in study cases"
    isPltEIC: int
    "Results to plot: Net present value of expected interruption costs"
    isPltInvCosts: int
    "Results to plot: Net present value of investments"
    isPltLossCosts: int
    "Results to plot: Net present value of costs for losses"
    isPltTotCosts: int
    "Results to plot: Net present value of total costs"
    isPltUserDefCosts: int
    "Results to plot: Net present value of user-defined costs"
    isVerifyEqualCmdSettings: int
    "Tasks: Verify equality of underlying command settings"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pBaseCase: object
    "Selection of study cases: Base case"
    pResultFile: object
    "Summary results"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    vecCases: list
    "Selection of study cases: Study cases"
    vecCasesIgn: list
    "Selection of study cases: Ignore"

    def AppendStudyCase(*args): ...

    def AttributeType(*args): ...

    def CalcDiscountedEstimatedPaybackPeriod(*args): ...

    def CalcEstimatedPaybackPeriod(*args): ...

    def CalcInternalRateOfReturn(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def RemoveStudyCases(*args): ...

    def __getattr__(*args): ...


class ComTransfer(PFGeneral):
    addoptions: str
    "Additional Parameters"
    bcOvlods: int
    "Continue calculation if base case is overloaded"
    bcOvvols: int
    "Continue calculation if base case has voltage violations"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dIncrmnt: float
    "Initial conditions: Initial step size"
    dInitScale: float
    "Initial conditions: Initial scaling factor"
    dTolerance: float
    "Convergence criteria: Min. step size"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    flowcheck: int
    "Measured transfer capacity"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iCntcon: int
    "Contingency constrained"
    iCntres: int
    "Show contingency analysis report for the last feasible solution"
    iFicNet: int
    "Use fictitious border network"
    iGensFrm: int
    "Generator scaling mode"
    iGensel: int
    "Generators"
    iLoad: int
    "Option"
    iLodsFrm: int
    "Loads"
    iSave: int
    "Save Results"
    iScaleMod: int
    "Scaling elements"
    iSchemeStatus: int
    "Scheme Status"
    iStopIter: int
    "Convergence criteria: Max. number of iterations"
    iVolt: int
    "Option"
    if_load: float
    "Option: Maximum thermal loading of components"
    if_volmax: float
    "Option: Upper limit of allowed voltage"
    if_volmin: float
    "Option: Lower limit of allowed voltage"
    ioptIgn: int
    "Ignore all constraints for..."
    iopt_Palim: int
    "Consider active power limits"
    iopt_lodcons: int
    "Consider thermal constraints"
    iopt_method: int
    "Calculation Method"
    iopt_pf: int
    "Keep constant power factor"
    iopt_scen: int
    "Last feasible solution"
    iopt_selreg: int
    "Consider constraints only for selected objects"
    iopt_volcons: int
    "Consider voltage limits"
    isScaleGen: int
    "Generators"
    isScaleLod: int
    "Loads"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    ovl_relax: float
    "Continue calculation if base case is overloaded: Relax constraints by"
    ovv_relax: float
    "Continue calculation if base case has voltage violations: Relax constraints by"
    pResults: object
    "Results"
    p_GenSet: object
    "Generators: Generator set"
    p_LodSet: object
    "Loads: Load set"
    p_boundary: object
    "User defined elements: Boundary"
    p_cntcmd: object
    "Contingency constrained: Contingency Analysis"
    p_cntrep: object
    "Show contingency analysis report for the last feasible solution: Contingency analysis report"
    p_expElms: object
    "User defined elements: Exporting elements"
    p_ficNet: object
    "Use fictitious border network: Border network"
    p_fromReg: object
    "Interconnection regions: Exporting region"
    p_impElms: object
    "User defined elements: Importing elements"
    p_scenario: object
    "Last feasible solution: Operation scenario location"
    p_toReg: object
    "Interconnection regions: Importing region"
    pid_: int
    "ProjectID"
    psel_elms: object
    "Consider constraints only for selected objects: Selection"
    root_id: object
    "Original Location"
    tcadef: int
    "Transfer capacity definition"
    tid_: int
    "TimeID"
    vlevconst: float
    "Ignore all constraints for...: Nominal voltage below or equal to"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetTransferCalcData(*args): ...

    def HasReferences(*args): ...

    def IsLastIterationFeasible(*args): ...

    def __getattr__(*args): ...


class ComUcte(PFGeneral):
    addoptions: str
    "Options: Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_con: str
    "File Type"
    iopt_dacf: int
    "Options: Import for DACF process"
    iopt_iqlims: int
    "Options: Ignore reactive power limits for generators"
    iopt_nlod2gen: int
    "Options: Convert negative loads to generators"
    iopt_prj: int
    "Import into"
    iopt_qforpv: int
    "Use Q value for PV generators"
    iopt_tr2zpu: int
    "Options: Convert transformer equivalent to common impedance"
    loc_name: str
    "Name"
    netsubfolder: str
    "Options: Network Data Subfolder"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pAddPrj: object
    "Name"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    targname: str
    "Folder"
    targpath: object
    "in"
    tid_: int
    "TimeID"
    uctenames: list
    "File Type: File Names"
    uctname: str
    "UCTE Data"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def SetBatchMode(*args): ...

    def __getattr__(*args): ...


class ComUcteexp(PFGeneral):
    addoptions: str
    "Options: Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    gridenable: list
    "Enable"
    iSchemeStatus: int
    "Scheme Status"
    iUseChrName: int
    "Options: Use first character of characteristic name as branch 'Order Code'"
    ibranchconv: int
    "Options: Export branch as single equivalent line"
    iopt_con: str
    "File Type"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    uctename: str
    "File Type: UCTE Data"
    uctevmin: float
    "Options: Export UCTE voltage >="

    def AttributeType(*args): ...

    def BuildNodeNames(*args): ...

    def DeleteCompleteQuickAccess(*args): ...

    def Execute(*args): ...

    def ExportAndInitQuickAccess(*args): ...

    def GetConnectedBranches(*args): ...

    def GetFromToNodeNames(*args): ...

    def GetOrderCode(*args): ...

    def GetUcteNodeName(*args): ...

    def HasReferences(*args): ...

    def InitQuickAccess(*args): ...

    def QuickAccessAvailable(*args): ...

    def ResetQuickAccess(*args): ...

    def SetGridSelection(*args): ...

    def __getattr__(*args): ...


class ComWktimp(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    datapartLabel: str
    "Partial import: Labels"
    datasetLabel: str
    "Dataset import: Label"
    dbAddParam: str
    "Import from: Additional ODBC Parameters"
    dbDatabase: str
    "Import from: Database"
    dbDriverName: str
    "Import from: ODBC Driver Name"
    dbInfo: str
    "Import from: e.g."
    dbPassword: str
    "Import from: Password"
    dbServer: str
    "Import from: DB Service"
    dbUser: str
    "Import from: User"
    fFile: str
    "Import from: Name"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    generalKey: list
    "Key"
    generalValue: list
    "Value"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_update: int
    "Diagram Creation Mode:Create:Extend"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pAddPrj: object
    "Import into: Existing Project"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    useDatapart: int
    "Partial import"
    useDataset: int
    "Dataset import"
    wktFormat: str
    "Source"
    wktFormatIdx: int
    "Import from: Format"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def GetCreatedObjects(*args): ...

    def GetModifiedObjects(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class SetCluster(PFGeneral):
    PeakLoad: list
    "Peak"
    PeakUnit: list
    "Unit"
    accStates: float
    "Accuracy"
    cendtime: int
    "End Time"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cluster: list
    "Clusters"
    cpHeadFold: object
    "Head Folder"
    cstarttime: int
    "Start Time"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    elmType: list
    "Element type"
    first_yr: int
    "Year"
    flags: int
    "Flags for settings used upon creation"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    isGens: int
    "Generators are included in the clusters."
    last_yr: int
    "End Time"
    load: list
    "Elements"
    load_plot: object
    "Displayed load"
    loc_name: str
    "Name"
    numloads: int
    "Number of Loads"
    numstates: int
    "Number of States"
    oid_: int
    "ObjectID"
    ph_info: list
    "Phase"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    show_load: object
    "Displayed load"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CalcCluster(*args): ...

    def GetNumberOfClusters(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class SetColscheme(PFGeneral):
    alarm: list
    "Criterion"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cAlarm: int
    "2. Alarm:  "
    cColouring: int
    "3. Other:  "
    cEnergizing: int
    "1. Energising Status:  "
    cGroup: int
    "3. Other:  "
    cUseAlarm: int
    "2. Alarm"
    cUseColouring: int
    "3. Other"
    cUseEnergizing: int
    "1. Energising Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    colouring: list
    "Criterion"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    energizing: list
    "1. De-energised"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    udefColouring: list
    "User-defined Filter"

    def AttributeType(*args): ...

    def GetAlarmColouringMode(*args): ...

    def GetColouringMode(*args): ...

    def GetEnergisingColouringMode(*args): ...

    def HasReferences(*args): ...

    def SetColouring(*args): ...

    def SetFilter(*args): ...

    def __getattr__(*args): ...


class SetDatabase(PFGeneral):
    cacheExpiration: int
    "Cache options: Expiration time"
    cacheFrame: list
    "Cache options"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    db_database: list
    "Database name"
    db_odbc_driver: list
    "ODBC driver"
    db_password: str
    "Password"
    db_schema: list
    "Database schema"
    db_service: list
    "Server"
    db_user: list
    "Username"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    parameters: list
    "Additional parameters"
    path: list
    "Additional directory for PATH"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    system: str
    "Database system"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def EmptyCache(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class SetDeskpage(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Sequence"
    pConts: list
    "Contents ..."
    pGrph: object
    "Graphic"
    pageStateStr: list
    "Page state (hidden)"
    pid_: int
    "ProjectID"
    rZoomLBX: float
    "Zoom coordinates Left Bottom: X"
    rZoomLBY: float
    "Y"
    rZoomRTX: float
    "Right Top: X"
    rZoomRTY: float
    "Right Top: Y"
    root_id: object
    "Original Location"
    selectedInTabGroup: int
    "Is selected window in tab group"
    showSearchField: int
    "Show search field"
    tabGroupIndex: int
    "Tab group"
    tid_: int
    "TimeID"
    viewportHeight: int
    "Viewport height (pixel)"
    viewportWidth: int
    "Viewport width (pixel)"
    visible: int
    "Visible"

    def AttributeType(*args): ...

    def Close(*args): ...

    def HasReferences(*args): ...

    def Show(*args): ...

    def __getattr__(*args): ...


class SetDesktop(PFGeneral):
    Objectx: list
    "Element"
    Pages: list
    "Contents ..."
    PlotTyp: object
    "Default type for plots"
    Variablex: list
    "Variable"
    auto_xscl: int
    "Axis: Auto Scale"
    charact: list
    "Charact."
    chart: int
    "Axis: Chart"
    chr_name: str
    "Characteristic Name"
    colour1: int
    "Cursors: Colour 1"
    colour2: int
    "Cursors: Colour 2"
    cpHeadFold: object
    "Head Folder"
    curveTracking: int
    "Display curve values in balloon help"
    dSplit: float
    "Scrollbar Position"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    descx: list
    "User defined Legend"
    drel: float
    "Axis: Start Value"
    editcmd: int
    "Command Button:Execute command:Open command"
    fit: int
    "Axis: Adapt Scale"
    floatingGroupGeometry: str
    "Group window geometry"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iShown: int
    "Active Page"
    iopt_col: int
    "Use Curve Colours for Labels"
    iopt_onl: int
    "While Simulation is running"
    iopt_tim: int
    "x Axis Variable"
    iopt_tim1: int
    "x-Axis variable"
    iorder: int
    "Sequence of Desktops"
    last: float
    "Axis: Range"
    loc_name: str
    "Name"
    map: int
    "Axis: Scale"
    max: float
    "Axis Limits: Maximum"
    min: float
    "Axis Limits: Minimum"
    oid_: int
    "ObjectID"
    pObjx: object
    "Element"
    pRes: object
    "User defined Results"
    pfm_default: int
    "PFM-default plots"
    pfm_type: list
    "Type of plot"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sh_tit: int
    "Show Title"
    tabSplitGeometry: str
    "Tab split geometry"
    tid_: int
    "TimeID"
    trg: float
    "Trigger"
    trigger: float
    "Axis Adapt Scale: Trigger"
    width1: int
    "Cursors: Width 1"
    width2: int
    "Cursors: Width 2"
    xgrid: int
    "Grid Lines"
    xgrid_count: int
    "Grid Lines: Count"
    xgrid_item: str
    "Reference"

    def AddPage(*args): ...

    def AttributeType(*args): ...

    def Close(*args): ...

    def DoAutoScaleX(*args): ...

    def Freeze(*args): ...

    def GetActivePage(*args): ...

    def GetCanvasSize(*args): ...

    def GetPage(*args): ...

    def HasReferences(*args): ...

    def IsFrozen(*args): ...

    def IsOpened(*args): ...

    def RemovePage(*args): ...

    def SetAdaptX(*args): ...

    def SetAutoScaleX(*args): ...

    def SetResults(*args): ...

    def SetScaleX(*args): ...

    def SetViewArea(*args): ...

    def SetXVar(*args): ...

    def Show(*args): ...

    def Unfreeze(*args): ...

    def WriteWMF(*args): ...

    def ZoomAll(*args): ...

    def __getattr__(*args): ...


class SetDistrstate(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cluster: list
    "Clusters"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    numstates: int
    "Number of States"
    numstations: int
    "Number of Stations"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    plotStat: object
    "Displayed Station"
    root_id: object
    "Original Location"
    show_stat: object
    "Displayed station"
    stations: list
    "Stations"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CalcCluster(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class SetFilt(PFGeneral):
    autodesc: list
    "Description"
    autofilter: list
    "Filter"
    autovarname: list
    "Parameter"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cobjset: str
    "Object Filter"
    color: int
    "Colour"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    expr: list
    "Expression"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iautocol: int
    "Automatic Colouring"
    ibinsgl: int
    "whose Connections (Busbars, Terminals) are drawn"
    icalcrel: int
    "Relevant Objects for Calculation"
    icase: int
    "Case sensitive"
    icolbr: int
    "Colouring Branches like Nodes"
    icoups: int
    "Interconnecting Branches:None:Grid:Zone:Area"
    iopt_sgl: int
    "Single Line Option"
    ireg: int
    "Regular Expression"
    isrchstr: int
    "Search literally"
    istopmatch: int
    "Stop at matching Folder"
    isubfold: int
    "Include Subfolders"
    iword: int
    "Whole words only"
    loc_name: str
    "Name"
    objset: list
    "Object Filter"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    outserv: int
    "Out of Service"
    pGraphic: object
    "Graphic"
    pid_: int
    "ProjectID"
    pstart: object
    "Look in"
    root_id: object
    "Original Location"
    sInFold: list
    "Search Folders"
    tid_: int
    "TimeID"
    varName: str
    "in Parameter (empty: all)"

    def AttributeType(*args): ...

    def Get(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class SetLevelvis(PFGeneral):
    Internals: list
    "Contents ..."
    aLevList: str
    "Selected layer for actions"
    aSymList: str
    "Object"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iArrow: int
    "Power flow direction arrows: Direction represents"
    iBackgroundBrightness: int
    "Brightness (-100..100)"
    iBackgroundSaturation: int
    "Saturation (-100..100)"
    iBackgroundType: int
    "Background type"
    iForWhat: int
    "Target"
    iGenCol: int
    "Circle Colour"
    iGens: int
    "Generation Circles"
    iKRatio: int
    "Keep aspect ratio"
    iLayoutNorm: int
    "Show normally open switches"
    iLayoutTieOpt: int
    "Show Tie Open Points"
    iLodCol: int
    "Circle Colour"
    iLodTot: int
    "Load Type"
    iLods: int
    "Load Circles"
    iMapProvider: int
    "Provider"
    iMapType: int
    "Map layer"
    iNormOpenCol: int
    "Normally open switches: Colour"
    iNormOpenFill: int
    "Normally open switches: Fill"
    iPQS: int
    "Displayed variable"
    iRecloseCol: int
    "Reclose switches: Colour"
    iRecloseFill: int
    "Reclose switches: Fill"
    iRmtSubCol: int
    "Remotely controlled substations: Colour"
    iSchemeStatus: int
    "Scheme Status"
    iSclBackLim: int
    "Minimum scale 1 :"
    iSetBGr: int
    "Set position and size"
    iShwCircSub: int
    "Substations"
    iShwCircTrf: int
    "Secondary Substations"
    iStandbyCol: int
    "Open standby switches: Colour"
    iStandbyFill: int
    "Open standby switches: Fill"
    iTieOptCol: int
    "Tie open points: Colour"
    iTieOptFill: int
    "Tie open points: Fill"
    loc_name: str
    "Name"
    localMapEpsgCode: int
    "EPSG:"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    rBGLBotX: float
    "X"
    rBGLBotY: float
    "Y"
    rBGRTopX: float
    "X"
    rBGRTopY: float
    "Y"
    rCircScal: float
    "Scaling Factor for Load and Generation Circles"
    rNormOpenSzFac: float
    "Normally open switches: Size factor"
    rNormOpenWd: float
    "Normally open switches: Line width"
    rPrioCols: list
    "Colour"
    rPrioScals: list
    "Scaling Factor"
    rRecloseSzFac: float
    "Reclose switches: Size factor"
    rRecloseWd: float
    "Reclose switches: Line width"
    rStandbySzFac: float
    "Open standby switches: Size factor"
    rStandbyWd: float
    "Open standby switches: Line width"
    rTieOptSzFac: float
    "Tie open points: Size factor"
    rTieOptWd: float
    "Tie open points: Line width"
    root_id: object
    "Original Location"
    sBackFilNam: str
    "File"
    showFuses: int
    "Lines: Fuses in bays"
    showLdfAnimation: int
    "Power flow direction arrows: Show animation"
    symbolConnArrows: int
    "Lines: Connection arrows"
    symbolConnNamesBlock: int
    "Block diagram: Connection names"
    symbolConnNumbersBlock: int
    "Block diagram: Connection numbers"
    symbolConnPoints: int
    "Lines: Connection points"
    symbolLdfArrows: int
    "Power flow direction arrows"
    symbolLineComp: int
    "Lines: Line compensations"
    symbolLineSecLoads: int
    "Lines: Sections and line loads"
    symbolNormOpenSwitches: int
    "Normally open switches"
    symbolPhases: int
    "Lines: Phases"
    symbolReclosers: int
    "Reclose switches"
    symbolRemoteStations: int
    "Remotely controlled substations"
    symbolStandbySwitches: int
    "Open standby switches"
    symbolTapPositions: int
    "Transformers, machines, shunts: Tap positions"
    symbolTieOpenPoints: int
    "Tie open points"
    symbolVectorGroups: int
    "Transformers, machines, shunts: Vector groups"
    tid_: int
    "TimeID"

    def AdaptWidth(*args): ...

    def Align(*args): ...

    def AttributeType(*args): ...

    def ChangeFont(*args): ...

    def ChangeLayer(*args): ...

    def ChangeRefPoints(*args): ...

    def ChangeWidthVisibilityAndColour(*args): ...

    def HasReferences(*args): ...

    def Mark(*args): ...

    def Reset(*args): ...

    def __getattr__(*args): ...


class SetParalman(PFGeneral):
    ParalTyp: int
    "Parallel computing method"
    SlaveNum: int
    "Max. number of processes on local machine"
    affinity: list
    "CPU index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    host: str
    "Master host name or IP"
    iAssignCPU: int
    "Assign specific affinity to each process"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    maxCore: list
    "Max. number of processes on local machine: Available logical cores"
    oid_: int
    "ObjectID"
    p_CptGrp: object
    "Computer group"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    trsf_mod: int
    "Communication method"
    useCore: list
    "Max. number of processes on local machine: Max. processes"

    def AttributeType(*args): ...

    def GetNumSlave(*args): ...

    def GetTransfType(*args): ...

    def HasReferences(*args): ...

    def SetNumSlave(*args): ...

    def SetTransfType(*args): ...

    def __getattr__(*args): ...


class SetPath(PFGeneral):
    c_brfirst: object
    "First Branch"
    c_brlast: object
    "Last Branch"
    c_first: object
    "First Busbar"
    c_last: object
    "Last Busbar"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    icolor: int
    "Colour"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AllBreakers(*args): ...

    def AllClosedBreakers(*args): ...

    def AllOpenBreakers(*args): ...

    def AllProtectionDevices(*args): ...

    def AttributeType(*args): ...

    def Create(*args): ...

    def GetAbsDistance(*args): ...

    def GetAll(*args): ...

    def GetBranches(*args): ...

    def GetBuses(*args): ...

    def GetImpedanceAtPos(*args): ...

    def GetNodeIndex(*args): ...

    def GetPathFolder(*args): ...

    def GetRelay(*args): ...

    def HasReferences(*args): ...

    def NextRelayBranch(*args): ...

    def __getattr__(*args): ...


class SetPrj(PFGeneral):
    Sbase: float
    "Base Apparent Power"
    applyAutomatically: int
    "Planned Outages: Consider automatically upon study case activation"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    clenexp: str
    "Lines/Cables Length unit, m"
    cpHeadFold: object
    "Head Folder"
    cspqexp: str
    "Loads/Asyn. and DC Machines P, Q, S unit, VA,W,var"
    cspqexpgen: str
    "Static Generators/Synchr. Machines P, Q, S unit, VA,W,var"
    currency: str
    "Currency unit"
    customEpsgCode: int
    "EPSG:"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    defaultPlotColourPalette: object
    "Default colour palette"
    defaultPlotStyle: object
    "Default plot style"
    degreePrec: int
    "Degree (angle) decimal places"
    diagramSearchAttribs: list
    "Additional attributes to include in diagram search (comma separated list): ."
    displayNameMode: int
    "Display name: Mode:Show element name only:Prepend parent element:Prepend site and/or substation name"
    drawingToolbarStateBlock: list
    "Drawing toolbar state (block diagrams)"
    drawingToolbarStateGeographic: list
    "Drawing toolbar state (geographic diagrams)"
    drawingToolbarStateModelica: list
    "Drawing toolbar state (Modelica pages)"
    drawingToolbarStatePlot: list
    "Drawing toolbar state (plot pages)"
    drawingToolbarStateSchematic: list
    "Drawing toolbar state (schematic diagrams)"
    dudevother: float
    "Nominal Voltage Check Max. allowed deviation from Terminal voltage: for other Elements"
    dudevtrf: float
    "Nominal Voltage Check Max. allowed deviation from Terminal voltage: for Transformers"
    dunomelne: float
    "Nominal Voltage Check Max. allowed difference over Lines/Switches/Fuses: for Lines"
    dunomeswt: float
    "Nominal Voltage Check Max. allowed difference over Lines/Switches/Fuses: for Switches and Fuses"
    energyPrec: int
    "Energy decimal places"
    extDataDir: str
    "External Data Directory: External Data Directory"
    fold_id: object
    "In Folder"
    fontBlkLabBra: int
    "Font-ID for signal labels"
    fontBlkLabNod: int
    "Labels for block labels"
    fontBlkTitle: int
    "Font-ID for Title and Legends"
    fontSglLabBra: int
    "Font-ID for branch labels"
    fontSglLabNod: int
    "Font-ID for node labels"
    fontSglResBra: int
    "Font-ID for branch results"
    fontSglResNod: int
    "Font-ID for node results"
    fontSglTitle: int
    "Font-ID for title and legends"
    fontsStr: list
    "Fonts"
    for_name: str
    "Foreign Key"
    frnom: float
    "Default frequency"
    geoBoundsEast: float
    "WGS-84 bounds: east"
    geoBoundsNorth: float
    "WGS-84 bounds: north"
    geoBoundsSouth: float
    "WGS-84 bounds: south"
    geoBoundsWest: float
    "WGS-84 bounds: west"
    geoCoordinateSystem: int
    "Coordinate system"
    gmin: float
    "Min. Conductance gmin"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAutoOutOfServ: int
    "Automatic Out of Service Detection"
    iAutoSlack: int
    "Settings for slack assignment: Auto slack assignment:Method 1:Method 2:off"
    iBBAlgo: int
    "Standard beach ball algorithm"
    iBayInNewStat: int
    "Insertion of new substations: Insert substations with bays"
    iCalcSymComp: int
    "Calculation of symmetrical components for untransposed lines"
    iConsLocalOpts: int
    "Consider local Opt*"
    iDispNames: int
    "Names in plot legends"
    iEndTime: int
    "End Time"
    iFlowOrient: int
    "Flow Orientation:Mixed Mode:Load Oriented:Generator Oriented"
    iIsolateBrkOnly: int
    "Switching Actions: Isolate opens circuit-breakers only"
    iIsolateWithEarth: int
    "Switching Actions: Isolate with earthing"
    iPlannedOutOrder: int
    "Planned Outages: Application sequence"
    iSchemeStatus: int
    "Scheme Status"
    iShowInactElts: int
    "Variations: Show inactive elements from other variations"
    iStartTime: int
    "Start Time"
    iStatus: int
    "Status:Draft:Issued"
    iSuppliedElmsAlgo: int
    "Determination of supplying transformers: Considered transformers:&2&All:&0&Only those located in stations:&3&Only voltage controlling ones:&1&Only voltage controlling ones, located in stations"
    iSwitchAmbiguous: int
    "Switch on performs forced closing in ambiguous situations"
    iSwtTypGrThan: int
    "When connecting component to busbar create: If nominal voltage >= threshold create"
    iSwtTypSmThan: int
    "When connecting component to busbar create: If nominal voltage < threshold create"
    iTowEarthRed: int
    "Earth wire reduction of towers"
    ilenunit: int
    "Units"
    iopt_switch: int
    "When connecting component to busbar create"
    ldfAmpExp: str
    "Load Flow and Simulation: Ampere, A"
    ldfAmpPrec: int
    "Load Flow and Simulation: Decimal places"
    ldfPowerExp: str
    "Load Flow and Simulation: W, VA, var"
    ldfPowerPrec: int
    "Load Flow and Simulation: Decimal places"
    ldfVoltExp: str
    "Load Flow and Simulation: Volt, V"
    ldfVoltPrec: int
    "Load Flow and Simulation: Decimal places"
    lneLoadingCalc: int
    "Consider line compensation current for line loading calculation"
    loc_name: str
    "Name"
    maxJumpTo: int
    "Max. number of entries in to-labels"
    oid_: int
    "ObjectID"
    onForNoneFBcon: int
    "Settings for slack assignment: Auto slack assignment for areas without connection to fictitious border grid"
    otherPrec: int
    "Decimal places for other units"
    outages: int
    "Planned Outages: Creation"
    overviewDetails: list
    "Category detail level displayed in project overview window"
    perUnitPrec: int
    "Per unit (p.u.) decimal places"
    percentPrec: int
    "Percent (%) decimal places"
    pid_: int
    "ProjectID"
    prefShowSite: int
    "Prefer site name"
    refMachinePrio: int
    "Settings for slack assignment: Priority for Reference Machines:Rated Power:Active Power Capability:Active Power Reserve"
    rmin: float
    "Min. Resistance rmin"
    root_id: object
    "Original Location"
    sBordSym: list
    "Border Symbol"
    sDefSym: list
    "Default Symbol"
    sSiteTypes: list
    "Site Types"
    sSubstTyp: list
    "Substation Types"
    sSymbol: list
    "Symbol"
    shcAmpExp: str
    "Short-Circuit: Ampere, A"
    shcAmpPrec: int
    "Short-Circuit: Decimal places"
    shcPowerExp: str
    "Short-Circuit: W, VA, var"
    shcPowerPrec: int
    "Short-Circuit: Decimal places"
    shcVoltExp: str
    "Short-Circuit: Volt, V"
    shcVoltPrec: int
    "Short-Circuit: Decimal places"
    showDiaextdata: int
    "External Data Directory: Display reminder after file selection"
    showJumpTo: int
    "Show jump-to labels at graphically half-connected lines"
    showSiteName: int
    "Display name: Show site name"
    showSubStatName: int
    "Display name: Show substation name"
    thrWrnLength: float
    "Line couplings: Allowable difference in lengths of lines"
    tid_: int
    "TimeID"
    useNewPlotFramework: int
    "Use new plot framework"
    voltLevCB: float
    "When connecting component to busbar create: Threshold:"
    voltLevHv: float
    "HV voltage level"
    voltLevMv: float
    "MV voltage level"
    ymodmin: float
    "Threshold Impedance for Z-model"

    def AttributeType(*args): ...

    def GetFontID(*args): ...

    def HasReferences(*args): ...

    def SetFontFor(*args): ...

    def __getattr__(*args): ...


class SetScenario(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Check(*args): ...

    def Default(*args): ...

    def HasReferences(*args): ...

    def Print(*args): ...

    def __getattr__(*args): ...


class SetSelect(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iused: int
    "Used for"
    iusedSub: int
    "Type"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AddRef(*args): ...

    def All(*args): ...

    def AllAsm(*args): ...

    def AllBars(*args): ...

    def AllBreakers(*args): ...

    def AllClosedBreakers(*args): ...

    def AllElm(*args): ...

    def AllLines(*args): ...

    def AllLoads(*args): ...

    def AllOpenBreakers(*args): ...

    def AllSym(*args): ...

    def AllTypLne(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def GetAll(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class SetTime(PFGeneral):
    cDate: str
    "Date"
    cTime: str
    "Time"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    datetime: int
    "Date and Time"
    day: int
    "Day"
    dayofweek: int
    "Details: Day of Week:Monday:Tuesday:Wednesday:Thursday:Friday:Saturday:Sunday"
    dayofyear: int
    "Details: Day of Year"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hour: int
    "Hour"
    hourofyear: int
    "Details: Hour of Year"
    iSchemeStatus: int
    "Scheme Status"
    isleapyear: int
    "Details: Leap Year"
    loc_name: str
    "Name"
    min: int
    "Minute"
    month: int
    "Month"
    oid_: int
    "ObjectID"
    outserv: int
    "Ignore Time Trigger"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sec: int
    "Second"
    tid_: int
    "TimeID"
    week: int
    "Details: Week"
    year: int
    "Year"

    def AttributeType(*args): ...

    def Date(*args): ...

    def HasReferences(*args): ...

    def SetTime(*args): ...

    def SetTimeUTC(*args): ...

    def Time(*args): ...

    def __getattr__(*args): ...


class SetUser(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    confirmTabClose: int
    "Tabbed Document Interface: Show confirmation dialog when closing diagrams"
    cpHeadFold: object
    "Head Folder"
    customDate: list
    "Localisation: x"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    diagramWindowMargin: int
    "General options: Diagram window margin"
    dmColumnWidths: list
    "Data Manager Column Widths"
    dmFaves: list
    "Favourites"
    drwToolBarLibraryZoom: float
    "Drawing Toolbar Zoom Factor"
    drwToolBarShHd: int
    "Drawing Toolbox: Show group headers"
    drwToolBarShLbls: int
    "Drawing Toolbox: Show element labels"
    editorColors: list
    "Editor colour settings"
    enableMsgFilter: int
    "Enable message filter"
    exportModBy: int
    "Export/Import Data (DZ/DZS): Export 'Modified by'"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    graphicDebug: int
    "DIgSILENT Internal: Graphic debug mode"
    graphicFlushFrameTime: int
    "DIgSILENT Internal: Include flush in frame time"
    graphicPageBackgroundColour: int
    "Background colours: Graphic page"
    gridColour: int
    "Grid representation: Grid colour"
    gridDotColour: int
    "Grid representation: Grid colour"
    gridStyle: int
    "Grid representation: Style:no grid:grid lines:dots:crosses"
    iActUseCore: int
    "Actual number of processes to be used"
    iAllowHousek: int
    "Allow housekeeping task to operate when user is connected"
    iAscBin: int
    "Export/Import Data (DZ/DZS): Binary Data (e.g. Results):not included:included:file name only"
    iAskDel: int
    "Browser: Confirm Delete Action"
    iAuto1Br: int
    "Place Branch Objects with One Connection Automatically"
    iAutoGrp: int
    "Open graphics board on study case activation"
    iAutoSav: int
    "Browser: Save Data Automatically (tabular Input)"
    iAutoSaveSc: int
    "Operation Scenario: Save active Operation Scenario automatically"
    iAutoScroll: int
    "Automatic Scrolling"
    iAutoSort: int
    "Data Manager: Sort Automatically"
    iAutoZ: int
    "Mark in graphic: Zoom-in on marked elements"
    iAutocomp: int
    "Options: Enable Autocomplete"
    iColChaVar: int
    "Parameter with Characteristics"
    iColDistrVar: int
    "Parameter with Distributions"
    iColFlexVar: int
    "Flexible Data Parameter"
    iColOPVar: int
    "Operation Scenario Parameter"
    iConfirmMsgDel: int
    "Show confirmation dialog before clearing messages"
    iCoordmm: int
    "Coordinate Output at Statusbar in mm"
    iCoreInput: int
    "Actual number of processes to be used: Number of processes"
    iCustomDate: int
    "Localisation: Use Custom Format for Date and Time:"
    iEditFilt: int
    "Edit Filter before Execute"
    iFloatDay: int
    "Floating Licence Validity (Days)"
    iInitialFreeze: int
    "General options: Open diagrams in freeze mode on study case activation"
    iIntervalSc: int
    "Operation Scenario: Save Interval"
    iInvResults: int
    "Retention of results after network change"
    iMarkCol: int
    "Mark in graphic: Colour"
    iMarkInGrf: int
    "Mark in graphic"
    iMigrateSc: int
    "Operation Scenario: Automatically migrate to current configuration during activation"
    iModGrf: int
    "General options: Show Edit Graphic Object in context menu"
    iMultBrowse: int
    "Data Manager: Use multiple Data Manager"
    iMultNmm: int
    "Data Manager: Use multiple Network Model Manager"
    iPrDateTime: int
    "Message Format"
    iPrErr: int
    "Displayed messages: Errors"
    iPrInf: int
    "Displayed messages: Information"
    iPrLngName: int
    "Message Format: Full object names"
    iPrOthers: int
    "Displayed messages: Others"
    iPrPcl: int
    "Displayed messages: Events"
    iPrWrg: int
    "Displayed messages: Warnings"
    iProfile: int
    "System Stage Profile:All:Revisions Only:No System Stages"
    iRecBin: int
    "Export/Import Data (DZ/DZS): Export References to Deleted Objects"
    iRemLastObj: int
    "Data Manager: Remember last selected object"
    iRszBr: int
    "General options: Allow Resizing of branch objects"
    iSchemeStatus: int
    "Scheme Status"
    iShowBackup: int
    "Confirmation dialogs: Show backup reminder dialog"
    iShowExample: int
    "Show 'Example' dialog at startup"
    iShowExit: int
    "Confirmation dialogs: Show 'Exit' dialog"
    iShowHid: int
    "Hidden Folders"
    iShowRecNot: int
    "Confirmation dialogs: Show 'Variation is recording' notification"
    iShowRemoveCont: int
    "Confirmation dialogs: Show 'Remove Contingencies' confirmation in Contingency Analysis"
    iShowWelcome: int
    "Welcome Dialog"
    iSnapVi: int
    "General options: Snap Textboxes"
    iTreeAll: int
    "All Folders"
    iTreeB: int
    "Model Definition"
    iTreeC: int
    "Cubicle"
    iTreeL: int
    "Lines"
    iTreeS: int
    "Stations"
    iUpdateCheckIv: int
    "Check for application updates: Update check interval"
    iUpdateChkLast: int
    "Check for application updates: Date of last check"
    iautoind: int
    "Options: Enable Auto Indent"
    ibsatsol: int
    "Options: Enable Backspace at Start of Line"
    icalcupdsgl: int
    "Update graphic while simulation is running"
    idecisep: int
    "Localisation: Decimal Symbol"
    ilinenumbers: int
    "Options: Show Line Numbers"
    inumtabs: int
    "Options: Tab size"
    iopt_updCheck: int
    "Check for application updates"
    isSendFullPrj: int
    "Transfer complete project to all processes"
    ishowmargin: int
    "Options: Show Selection Margin"
    itabs_: int
    "Options: Tabs"
    iviewwhites: int
    "Options: View Blanks and Tabs"
    limitStationDiagrams: int
    "Limit number of open site and substation diagrams"
    lineWidthScaleExport: float
    "Line width scaling factor for export/printing"
    loc_name: str
    "Name"
    markInGraphicMarkers: int
    "Mark in graphic: Highlight small elements using additional markers"
    markOpacity: float
    "Mark in graphic: Opacity"
    markSameWords: int
    "Options: Enable Same-word Highlighting"
    maxStationDiagrams: int
    "Limit number of open site and substation diagrams: Maximum page count"
    maxZoomScaleGPS: int
    "Mark in graphic Zoom-in on marked elements: Maximum scale in GPS diagrams"
    maxZoomSchematic: int
    "Mark in graphic Zoom-in on marked elements: Maximum zoom in schematic diagrams"
    modelPageBackgroundColour: int
    "Background colours: Model"
    modelTypePageBackgroundColour: int
    "Background colours: Model type"
    msgTextFilter: list
    "Contained text"
    msgTextFilter2: list
    "Contained text"
    off_ids: int
    "Id contingent size"
    off_idsWarn: int
    "Id contingent warning threshold"
    oid_: int
    "ObjectID"
    pProfile: object
    "Used Profile"
    pTbar: list
    "Toolbar"
    pTbox: list
    "Toolbox"
    pTboxgr: list
    "Toolbox Group"
    p_glfold: object
    "Custom Library: Used Library"
    parallelSet: object
    "Parallel computation settings"
    petloc: int
    "Cursor"
    pfm_shell: int
    "Communicates with PFM Shell"
    pid_: int
    "ProjectID"
    prioChaVar: int
    "Priority:1:2:3"
    prioColour: str
    "Colour Prio"
    prioDistrVar: int
    "Priority:1:2:3"
    prioOPVar: int
    "Priority:1:2:3"
    procTimeOut: int
    "Max. waiting time for process response"
    ptopn: str
    "last path used in open dialog box"
    pwKamikaze: int
    "Use network settings from configuration"
    pwPassword: list
    "Password"
    pwPasswordEdit: str
    "Password"
    pwSelection: str
    "Last selection"
    pwService: str
    "Service Endpoint"
    pwUsername: str
    "Username"
    rMinTextSz: float
    "General options: Show text only if height will be at least"
    rZoomAccl: float
    "Acceleration of Zooming and Panning: Acceleration Factor"
    root_id: object
    "Original Location"
    sIgnoredUpdates: list
    "Versions ignored in update check"
    showResetCalc: int
    "Confirmation dialogs: Show 'Reset Calculation' confirmation dialog"
    showTabIcon: int
    "Tabbed Document Interface: Show tab icons"
    showmod: int
    "Selected Modules"
    tabPosition: int
    "Tabbed Document Interface: Tab position:top:bottom"
    tcalcupdsgl: float
    "Update graphic while simulation is running: update every"
    tid_: int
    "TimeID"
    tool_advan: int
    "Advanced Toolbar"
    tool_advanVI: int
    "Advanced Toolbar"
    windowBackgroundColour: int
    "Background colours: Window"

    def AttributeType(*args): ...

    def GetNumProcesses(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class SetVipage(PFGeneral):
    Objectx: list
    "Element"
    UsedDia: object
    "Used by Dialog"
    Variablex: list
    "Variable"
    Vis: list
    "Plots"
    auto_xscl: int
    "Scale: Auto Scale"
    charact: list
    "Charact."
    chart: int
    "Scale: Chart"
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    descx: list
    "User defined Legend"
    drel: float
    "Scale: Start Value"
    fit: int
    "Scale: Adapt Scale"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_add: str
    "Arrangement"
    iopt_move: int
    "Plots can be moved"
    iopt_rsz: int
    "Plots can be resized"
    iopt_tim: int
    "x Axis Variable"
    iopt_tim1: int
    "x-Axis variable"
    iopt_trans: int
    "Background: Graphics are transparent"
    isDownMigrated: int
    "Has been down migrated"
    last: float
    "Scale: Range"
    loc_name: str
    "Name"
    map: int
    "Scale: Scale"
    max: float
    "Scale Limits: Maximum"
    min: float
    "Scale Limits: Minimum"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pObjx: object
    "Element"
    pRes: object
    "Results"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sBackFilNam: str
    "Background: Filename"
    selectedInTabGroup: int
    "Is selected window in tab group"
    style: str
    "Plot style: Used"
    tabGroupIndex: int
    "Tab group"
    tid_: int
    "TimeID"
    trg: float
    "Scale Adapt Scale: Trigger"
    use_x: int
    "Use local x-Axis"
    visible: int
    "Visible"
    xgrid: int
    "Grid Lines"
    xgrid_count: int
    "Grid Lines: Count"
    xgrid_item: str
    "Reference"

    def AttributeType(*args): ...

    def Close(*args): ...

    def CreateVI(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def GetOrInsertPlot(*args): ...

    def GetVI(*args): ...

    def HasReferences(*args): ...

    def InsertPlot(*args): ...

    def MigratePage(*args): ...

    def SetAdaptX(*args): ...

    def SetAutoScaleX(*args): ...

    def SetResults(*args): ...

    def SetScaleX(*args): ...

    def SetStyle(*args): ...

    def SetTile(*args): ...

    def SetXVar(*args): ...

    def Show(*args): ...

    def __getattr__(*args): ...


class BlkDef(PFGeneral):
    algloop: int
    "Initialisation: Allow iterative solver at initialisation"
    autoCompCheckSum: list
    "Automatic compilation checksum"
    cCheckSum: list
    "DSL info: Checksum:"
    cInput: list
    "Variables: Input signals"
    cIntern: list
    "Variables: Internal variables"
    cOutput: list
    "Variables: Output signals"
    cParams: list
    "Variables: Parameters"
    cStates: list
    "Variables: State variables"
    cUsage: int
    "Usage"
    cdisName: list
    "Display name"
    cdlllevel: int
    "Classification: DLL level:"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    configScript: object
    "Initialisation: Configuration Script"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    disName: str
    "Model type: Display name"
    display3rdParty: list
    "Third Party Licence (will only be applied after encryption): Third Party Module"
    displayCopyright: list
    "Copyright"
    displayModule: list
    "Compilation options: Module"
    elm_name: list
    "Model Name"
    fDllName: str
    "Model type: DLL-file"
    fMatlab: str
    "Model type: M-file"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    i_autoinc: int
    "Initialisation: Automatic calculation of initial conditions"
    i_partinc: int
    "Initialisation: Partial initialisation in case of deadlock"
    iecTa: float
    "IEC61400-27 Interface: Sample time"
    intVersion: str
    "Version"
    interpo: int
    "Interpolation of internal variables"
    iopt_modtyp: int
    "Model type"
    isCompiled: int
    "Compiled model"
    isLinear: int
    "Classification: Linear"
    isMacro: int
    "Model type: Macro"
    isMatlab: int
    "MATLAB"
    level: int
    "Classification: DSL level:&0&0:&1&1:&2&2:&3&3:&4&4:&5&5:&6&6:&7&7"
    loc_name: str
    "Name"
    maxerror: float
    "Iterative solver options: Max. error"
    maxiteration: int
    "Iterative solver options: Max. number of iterations"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sAddEquat: list
    "Additional equations"
    sAddInter: list
    "Additional internal variables"
    sAddParam: list
    "Additional parameters"
    sAuthor: list
    "Compilation options: Author"
    sCompany: list
    "Compilation options: Company"
    sCopyright: list
    "Compilation options: Copyright"
    sInput: list
    "Variables: Input signals"
    sInterf: list
    "Extended additional equations"
    sIntern: list
    "Variables: Internal variables"
    sLowLimInp: list
    "Limiting parameters/input signals Lower limitation: Input signals"
    sLowLimPar: list
    "Limiting parameters/input signals Lower limitation: Parameters"
    sOutput: list
    "Variables: Output signals"
    sPSSEParam: list
    "Parameter mapping"
    sParams: list
    "Variables: Parameters"
    sStates: list
    "Variables: State variables"
    sTitle: str
    "Title"
    sUpLimInp: list
    "Limiting parameters/input signals Upper limitation: Input signals"
    sUpLimPar: list
    "Limiting parameters/input signals Upper limitation: Parameters"
    sVersion: list
    "Compilation options: Version"
    tid_: int
    "TimeID"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"
    usage: int
    "Usage"

    def AttributeType(*args): ...

    def CalculateCheckSum(*args): ...

    def Check(*args): ...

    def Compile(*args): ...

    def Encrypt(*args): ...

    def GetCheckSum(*args): ...

    def HasReferences(*args): ...

    def Pack(*args): ...

    def PackAsMacro(*args): ...

    def ResetThirdPartyModule(*args): ...

    def SetThirdPartyModule(*args): ...

    def __getattr__(*args): ...


class BlkSig(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    emt_rst: int
    "EMT Simulation unbalanced"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iconfrom: int
    "Connected with Output: Connection Type:unknown:Input:Output:Lower Limit:Upper Limit"
    iconto: int
    "Connected with Input: Connection Type:unknown:Input:Output:Lower Limit:Upper Limit"
    indep: int
    "Independent of Module"
    inodfrom: int
    "Connected with Output: Variable"
    inodto: int
    "Connected with Input: Variable"
    ldf_rst: int
    "Load flow unbalanced"
    ldf_sym: int
    "Load flow balanced"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    pnodfrom: object
    "Connected with Output: of"
    pnodto: object
    "Connected with Input: of"
    rms_rst: int
    "RMS Simulation unbalanced"
    rms_sym: int
    "RMS Simulation balanced"
    root_id: object
    "Original Location"
    shc_rst: int
    "VDE/IEC Short-Circuit unbalanced"
    shc_sym: int
    "VDE/IEC Short-Circuit balanced"
    shcf_rst: int
    "Complete Short-Circuit unbalanced"
    shcf_sym: int
    "Complete Short-Circuit balanced"
    tid_: int
    "TimeID"
    value: float
    "Current Value"

    def AttributeType(*args): ...

    def GetFromSigName(*args): ...

    def GetToSigName(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ChaVecfile(PFGeneral):
    afac: float
    "Values from File: Factor a"
    approx: int
    "Approximation:constant:linear:polynomial:spline:hermite"
    bfac: float
    "Values from File: Factor b"
    cexponent: str
    " U"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    clines: int
    "No. of readings"
    col_Sep: str
    "File Settings: Separator for columns"
    cpHeadFold: object
    "Head Folder"
    curval: float
    "Current Value"
    curval_t: list
    "Current Value"
    dat_src: str
    "Data source"
    datacol: int
    "Values from File: Data Column"
    dec_Sep: str
    "File Settings: Decimal separator"
    decseprtr: str
    "Decimal separator"
    degree: int
    "Polynomial Degree"
    desc: list
    "Description"
    exponent: str
    "Exponent"
    f_name: str
    "File Settings: Filename"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    icol: int
    "Data Column"
    iopt_csep: int
    "File Settings: Separator for columns"
    iopt_file: int
    "File Settings: Format:Comma Separated Values (*.csv):PowerFactory Measurement File:User Defined Text File"
    iopt_sep: int
    "File Settings: Use system separators"
    loc_name: str
    "Parameter"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    scale: object
    "Scale"
    separator: str
    "Separator for columns"
    status: int
    "Error Status"
    tid_: int
    "TimeID"
    timecol: int
    "Values from File: Time Column"
    usage: int
    "Usage:relative in %:relative:absolute"
    useExponent: int
    "Unit"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def Update(*args): ...

    def __getattr__(*args): ...


class CimModel(PFGeneral):
    charact: list
    "Charact."
    cimClass: str
    "Class information: Type"
    classNS: str
    "Class information: Namespace"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    diff: int
    "Class information: Difference model"
    fold_id: object
    "In Folder"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    resID: str
    "Resource ID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def DeleteParameterAtIndex(*args): ...

    def GetAttributeEnumerationType(*args): ...

    def GetModelsReferencingThis(*args): ...

    def GetParameterCount(*args): ...

    def GetParameterNamespace(*args): ...

    def GetParameterValue(*args): ...

    def HasParameter(*args): ...

    def HasReferences(*args): ...

    def RemoveParameter(*args): ...

    def SetAssociationValue(*args): ...

    def SetAttributeEnumeration(*args): ...

    def SetAttributeValue(*args): ...

    def __getattr__(*args): ...


class CimObject(PFGeneral):
    about: int
    "Class information: Description"
    charact: list
    "Charact."
    cimClass: str
    "Class information: Type"
    classNS: str
    "Class information: Namespace"
    cpHeadFold: object
    "Head Folder"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    resID: str
    "Resource ID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def DeleteParameterAtIndex(*args): ...

    def GetAttributeEnumerationType(*args): ...

    def GetObjectsReferencingThis(*args): ...

    def GetObjectsWithSameId(*args): ...

    def GetParameterCount(*args): ...

    def GetParameterNamespace(*args): ...

    def GetParameterValue(*args): ...

    def GetPfObjects(*args): ...

    def HasParameter(*args): ...

    def HasReferences(*args): ...

    def RemoveParameter(*args): ...

    def SetAssociationValue(*args): ...

    def SetAttributeEnumeration(*args): ...

    def SetAttributeValue(*args): ...

    def __getattr__(*args): ...


class GrpPage(PFGeneral):
    autoLayoutMode: int
    "Page auto layout:off:vertical:grid"
    backgroundImage: str
    "Background Image"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    colourPalette: object
    "Colour palette"
    cpHeadFold: object
    "Head Folder"
    curveAreaAlignment: int
    "Curve area alignment:off:shared axes only:all plots on page"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    legacyStyleName: str
    "Style (legacy)"
    loc_name: str
    "Name"
    numLayoutColumns: int
    "Num columns"
    oid_: int
    "ObjectID"
    order: float
    "Sequence"
    pConts: list
    "Contents ..."
    pid_: int
    "ProjectID"
    plotStyle: object
    "Style"
    resultFile: object
    "Results"
    root_id: object
    "Original Location"
    selectedInTabGroup: int
    "Is selected window in tab group"
    tabGroupIndex: int
    "Tab group"
    tid_: int
    "TimeID"
    viewportHeight: int
    "Viewport height (pixel)"
    viewportWidth: int
    "Viewport width (pixel)"
    visible: int
    "Visible"
    zoomAreaBottom: float
    "Y"
    zoomAreaLeft: float
    "Zoom Area Left Bottom: X"
    zoomAreaRight: float
    "Right Top: X"
    zoomAreaTop: float
    "Right Top: Y"

    def AttributeType(*args): ...

    def ChangeStyle(*args): ...

    def DoAutoScale(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def GetOrInsertCurvePlot(*args): ...

    def GetOrInsertDiscreteBarPlot(*args): ...

    def GetOrInsertModalAnalysisPlot(*args): ...

    def GetOrInsertVectorPlot(*args): ...

    def GetOrInsertXYPlot(*args): ...

    def GetPlot(*args): ...

    def HasReferences(*args): ...

    def RemovePage(*args): ...

    def SetAutoScaleModeX(*args): ...

    def SetAutoScaleModeY(*args): ...

    def SetLayoutMode(*args): ...

    def SetResults(*args): ...

    def SetScaleTypeX(*args): ...

    def SetScaleTypeY(*args): ...

    def SetScaleX(*args): ...

    def SetScaleY(*args): ...

    def Show(*args): ...

    def __getattr__(*args): ...


class IntAddonvars(PFGeneral):
    advanced: list
    "More..."
    allowedValues: list
    "Allowed values"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    classname: str
    "Classname"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    datatype: list
    "Type"
    description: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    initial: list
    "Initial Value"
    loc_name: str
    "Name"
    longDesc: list
    "Long Description"
    maxValue: list
    "Maximum value"
    minValue: list
    "Minimum value"
    name: list
    "Name"
    oid_: int
    "ObjectID"
    percon: list
    "Per Connection"
    pid_: int
    "ProjectID"
    resultingName: str
    "Resulting Name"
    root_id: object
    "Original Location"
    shortDesc: str
    "Short Description"
    size: list
    "Initial size/rows"
    size2: list
    "Initial column count"
    tid_: int
    "TimeID"
    unit: list
    "Unit"

    def AddDouble(*args): ...

    def AddDoubleMatrix(*args): ...

    def AddDoubleVector(*args): ...

    def AddInteger(*args): ...

    def AddIntegerVector(*args): ...

    def AddObject(*args): ...

    def AddObjectVector(*args): ...

    def AddString(*args): ...

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def RemoveParameter(*args): ...

    def SetConstraint(*args): ...

    def __getattr__(*args): ...


class IntCase(PFGeneral):
    DPL_sel: object
    "DPL selection"
    absThreshJac: float
    "Bifactorisation control: Absolute threshold"
    absThreshOpt: float
    "Bifactorisation control: Absolute threshold"
    absThreshSim: float
    "Bifactorisation control: Absolute threshold"
    cActCalc: str
    "Current Calculation"
    cPrjName: str
    "Name of Project"
    cRecStName: str
    "Name of Recording Expansion Stage"
    cScenName: str
    "Name of Active Scenario"
    caexpshc: str
    "Ampere, A"
    campexp: str
    "Ampere, A"
    charact: list
    "Charact."
    chkThreshJac: float
    "Bifactorisation control: Check threshold"
    chkThreshOpt: float
    "Bifactorisation control: Check threshold"
    chkThreshSim: float
    "Bifactorisation control: Check threshold"
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    cpProject: object
    "Project"
    cpScenario: object
    "Active Scenario"
    cpexpshc: str
    "W,VA,var"
    cpowexp: str
    "W,VA,var"
    cvexpshc: str
    "Volt, V"
    cvoltexp: str
    "Volt, V"
    dErrTol: float
    "Error tolerance for linear equations"
    dErrTolAutoInit: float
    "Automatic error tolerance adaption: Initial error tolerance for linear equations"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    defThreshJac: float
    "Bifactorisation control: Defer threshold"
    defThreshOpt: float
    "Bifactorisation control: Defer threshold"
    defThreshSim: float
    "Bifactorisation control: Defer threshold"
    deltaDiffMethSim: float
    "Calculation of state variable Jacobians: Numerical step size"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iDropThresh: int
    "ILU: Drop element if smaller 10^X"
    iEquiSystem: int
    "Equilibrate all matrices"
    iErrTolAuto: int
    "Automatic error tolerance adaption"
    iLevOfFill: int
    "ILU: Level of fill"
    iLinSolve: int
    "Solution of linear equations"
    iMaxNumIterIS: int
    "Max. number of iterations"
    iNumAnaLdf: int
    "Calculation of partial derivatives"
    iNumAnaOpfSe: int
    "Calculation of Hessian"
    iPostProcess: int
    "Topological processing: Calculate results for all breakers"
    iPreCondAlg: int
    "Calculation of factorisation"
    iPreCondMeth: int
    "Preconditioning method"
    iRedBrkMode: int
    "Topological processing: Breaker reduction:Any suitable:Any suitable, except circuit-breakers:None:Enhanced mode"
    iRunParalIS: int
    "Parallelised calculation"
    iSchemeStatus: int
    "Scheme Status"
    iStudyDate: int
    "Study Date"
    iStudyTime: int
    "Study Time"
    iUseBlockJac: int
    "Representation"
    iUseBlockOpt: int
    "Representation"
    iUseBlockSim: int
    "Representation"
    idefault: int
    "Use as default"
    isIterSolver4DcLdf: int
    "Apply iterative solution method in DC Load Flow based calculations"
    loc_name: str
    "Name"
    numAnaOpfSeJac: int
    "Calculation of Jacobians"
    numDeltaHesse: float
    "Calculation of Hessian: Numerical step size"
    numDiffMethSim: int
    "Calculation of state variable Jacobians"
    oid_: int
    "ObjectID"
    owner: str
    "Owner"
    pRecSstage: object
    "Recording Expansion Stage"
    pid_: int
    "ProjectID"
    relThreshJac: float
    "Bifactorisation control: Relative threshold"
    relThreshOpt: float
    "Bifactorisation control: Relative threshold"
    relThreshSim: float
    "Bifactorisation control: Relative threshold"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    toolbars: list
    "Toolbar"
    toolboxes: list
    "Toolbox"
    toolboxgroups: list
    "Toolbox Group"
    useStableBlockFac: int
    "Bifactorisation control: Stable block factorisation"
    useStableBlockFacOpt: int
    "Bifactorisation control: Stable block factorisation"
    useStableBlockFacSim: int
    "Bifactorisation control: Stable block factorisation"

    def Activate(*args): ...

    def ApplyNetworkState(*args): ...

    def ApplyStudyTime(*args): ...

    def AttributeType(*args): ...

    def Consolidate(*args): ...

    def Deactivate(*args): ...

    def HasReferences(*args): ...

    def SetStudyTime(*args): ...

    def __getattr__(*args): ...


class IntComtrade(PFGeneral):
    AnCh: int
    "Number of analogue channels"
    Binary: int
    "Binary Data"
    DigCh: int
    "Number of digital channels"
    Samples: int
    "Number of samples"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "User defined Results"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    f_name: str
    "File"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    orgname: list
    "Filename"
    pid_: int
    "ProjectID"
    recDate: str
    "Date of first sample"
    recDay: int
    "Day"
    recMonth: int
    "Month"
    recYear: int
    "Year"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    timeZone: str
    "Time Zone"
    trgDate: str
    "Trigger Date"
    trgDay: int
    "Day"
    trgMonth: int
    "Month"
    trgYear: int
    "Year"
    triggerCount: int
    "Triggers: Events"
    triggerId: str
    "Triggers: ID"
    triggerIndex: int
    "Triggers: Displayed event"
    triggerMeasure: str
    "Triggers: Measurement Name"
    triggerSignal: str
    "Triggers: Signal Name"
    triggerThreshold: float
    "Triggers: Threshold"
    triggerTime: str
    "Triggers: Time"
    triggerType: str
    "Triggers: Type"
    triggerUnit: str
    "Triggers: Unit"

    def AttributeType(*args): ...

    def ConvertToASCIIFormat(*args): ...

    def ConvertToBinaryFormat(*args): ...

    def FindColumn(*args): ...

    def FindMaxInColumn(*args): ...

    def FindMinInColumn(*args): ...

    def GetAnalogueDescriptions(*args): ...

    def GetColumnValues(*args): ...

    def GetDescription(*args): ...

    def GetDigitalDescriptions(*args): ...

    def GetNumberOfAnalogueSignalDescriptions(*args): ...

    def GetNumberOfColumns(*args): ...

    def GetNumberOfDigitalSignalDescriptions(*args): ...

    def GetNumberOfRows(*args): ...

    def GetObjectValue(*args): ...

    def GetSignalHeader(*args): ...

    def GetUnit(*args): ...

    def GetValue(*args): ...

    def GetVariable(*args): ...

    def HasReferences(*args): ...

    def Load(*args): ...

    def Release(*args): ...

    def SortAccordingToColumn(*args): ...

    def __getattr__(*args): ...


class IntComtradeset(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "User defined Results"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dataObjs: list
    "COMTRADE File Info"
    endDate: int
    "Info: Date and time of last sample"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    samples: int
    "Info: Number of samples"
    startDate: int
    "Info: Date and time of first sample"
    stepsize: float
    "Info: Average Step Size"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def FindColumn(*args): ...

    def FindMaxInColumn(*args): ...

    def FindMinInColumn(*args): ...

    def GetAnalogueDescriptions(*args): ...

    def GetColumnValues(*args): ...

    def GetDescription(*args): ...

    def GetDigitalDescriptions(*args): ...

    def GetNumberOfAnalogueSignalDescriptions(*args): ...

    def GetNumberOfColumns(*args): ...

    def GetNumberOfDigitalSignalDescriptions(*args): ...

    def GetNumberOfRows(*args): ...

    def GetObjectValue(*args): ...

    def GetSignalHeader(*args): ...

    def GetUnit(*args): ...

    def GetValue(*args): ...

    def GetVariable(*args): ...

    def HasReferences(*args): ...

    def Load(*args): ...

    def Release(*args): ...

    def SortAccordingToColumn(*args): ...

    def __getattr__(*args): ...


class IntDataset(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    i_use: int
    "Use"
    ival: int
    "Value"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pObj: object
    "Object"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AddRef(*args): ...

    def All(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def GetAll(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class IntDocument(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    f_name: str
    "Filename"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pObj: object
    "Related to"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sSize: list
    "Size of embedded file"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Export(*args): ...

    def HasReferences(*args): ...

    def Import(*args): ...

    def Reset(*args): ...

    def View(*args): ...

    def __getattr__(*args): ...


class IntDplmap(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iSize: int
    "Size"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Clear(*args): ...

    def Contains(*args): ...

    def First(*args): ...

    def GetValue(*args): ...

    def HasReferences(*args): ...

    def Insert(*args): ...

    def Next(*args): ...

    def Remove(*args): ...

    def Size(*args): ...

    def Update(*args): ...

    def __getattr__(*args): ...


class IntDplvec(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iSize: int
    "Size"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Clear(*args): ...

    def Get(*args): ...

    def HasReferences(*args): ...

    def IndexOf(*args): ...

    def Insert(*args): ...

    def Remove(*args): ...

    def Size(*args): ...

    def Sort(*args): ...

    def __getattr__(*args): ...


class IntEvt(PFGeneral):
    calTp: int
    "Calculation type"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Events"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iContOrder: int
    "Contingency Order"
    iOrder: int
    "Contingency Order: order"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mod_cnt: int
    "Calculation types: Contingency Analysis"
    mod_shc: int
    "Calculation types: Short-Circuit"
    mod_sim: int
    "Calculation types: Simulation"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    shcEvts: int
    "Always create switch events to clear the faults"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CreateCBEvents(*args): ...

    def HasReferences(*args): ...

    def RemoveSwitchEvents(*args): ...

    def __getattr__(*args): ...


class IntExtaccess(PFGeneral):
    cCheckUrl: str
    "Test-URL"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sPermissions: list
    "Allowed address patterns"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CheckUrl(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class IntGate(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    conditions: list
    "Trigger: Trigger"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    expression: list
    "Expression"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    negate: list
    "Trigger: Negate"
    oid_: int
    "ObjectID"
    oneGate: int
    "Trigger: Logical gate to combine triggers:And:Or"
    oneOrUser: int
    "Gate definition"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AddTrigger(*args): ...

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class IntGrf(PFGeneral):
    Internals: list
    "Contents ..."
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iCol: int
    "Colour"
    iCollapsed: int
    "Imploded View"
    iIndLS: int
    "Line Style"
    iLevel: int
    "Layer"
    iOrtho: int
    "Orthogonal Connection Lines"
    iRot: int
    "Rotation"
    iSchemeStatus: int
    "Scheme Status"
    iVis: int
    "Visible"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pDataObj: object
    "Net Data Object"
    pid_: int
    "ProjectID"
    rCenterX: float
    "X-Position"
    rCenterY: float
    "Y-Position"
    rSizeX: float
    "X-Size"
    rSizeY: float
    "Y-Size"
    root_id: object
    "Original Location"
    sAttr: list
    "Attributes"
    sSymNam: str
    "Symbol Name"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def MoveToLayer(*args): ...

    def Orthogonalise(*args): ...

    def SnapToGrid(*args): ...

    def __getattr__(*args): ...


class IntGrfgroup(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def ClearData(*args): ...

    def Export(*args): ...

    def HasReferences(*args): ...

    def Import(*args): ...

    def __getattr__(*args): ...


class IntGrflayer(PFGeneral):
    actionTargetObjectType: int
    "Target parent element type"
    actionTargetSymbolDesc: str
    "Target parent element type: Object"
    allowInteraction: int
    "Elements: Elements are selectable"
    backgroundImageFile: str
    "Background image: File"
    bayBrushStyle: int
    "Show bays: Brush Style"
    bayColor: int
    "Show bays: Colour"
    bayLineStyle: int
    "Show bays: Line style"
    bayLineWidth: float
    "Show bays: Line width"
    bayOpacity: int
    "Show bays: Opacity"
    bayShow: int
    "Show bays"
    cElementLayer: int
    "Net elements, annotations, text boxes"
    cGeoLayer: int
    "Geographic map"
    cImageLayer: int
    "Background image"
    cSystemLayer: int
    "System layer"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    decimalsPQ: int
    "Arrows: Number of decimal places"
    defineMaxGeographicScale: int
    "Maximum geographic scale"
    defineMaxZoom: int
    "Zoom-dependent visibility: Maximum zoom level"
    defineMinGeographicScale: int
    "Minimum geographic scale"
    defineMinZoom: int
    "Zoom-dependent visibility: Minimum zoom level"
    drawPlotBackground: int
    "Draw plot background"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hostCapCircleScale: float
    "Hosting capacity: Circle scaling factor"
    hostingCapColor: int
    "Hosting capacity: Circle colour"
    iInvariant: int
    "Elements are zoom-invariant"
    iSchemeStatus: int
    "Scheme Status"
    iSetImageRect: int
    "Background image: Set position and size"
    iVis: int
    "Visible"
    imageBottomLeftX: float
    "Background image Left bottom: X"
    imageBottomLeftY: float
    "Background image Left bottom: Y"
    imageBrightness: int
    "Adjust bitmaps: Brightness (-100..100)"
    imageOpacity: int
    "Adjust bitmaps: Opacity"
    imageSaturation: int
    "Adjust bitmaps: Saturation (-100..100)"
    imageTopRightX: float
    "Right top: X"
    imageTopRightY: float
    "Right top: Y"
    interArrowsShow: int
    "Arrows"
    interBrushStyle: int
    "Nodes: Brush style"
    interColorP: int
    "Arrows: Colour for P"
    interColorQ: int
    "Arrows: Colour for Q"
    interNodesLineStyle: int
    "Nodes: Line style"
    interNodesLineWidth: float
    "Nodes: Line width"
    interNodesShow: int
    "Nodes"
    interPQ: int
    "Arrows: Direction according to"
    interSizeFactor: float
    "Arrows: Scaling factor"
    isNetworkTargetLayer: int
    "Elements: Target layer for graphic representation of network elements"
    isTargetLayer: int
    "Target layer"
    keepImageRatio: int
    "Background image: Keep aspect ratio"
    layerColour: int
    "Colour"
    layerId: int
    "Layer ID"
    layerType: int
    "Layer type"
    loadGenCircleScale: float
    "General settings: Scaling factor for load and generation circles"
    loadGenForSubstats: int
    "General settings: Show circles for substations and sites"
    loadGenForTrafStats: int
    "General settings: Show circles for secondary substations"
    loadGenGenColor: int
    "Generation circles: Circle colour"
    loadGenLoadColor: int
    "Load circles: Circle colour"
    loadGenLoadType: int
    "Load circles: Load type"
    loadGenOpacity: int
    "General settings: Circle Opacity"
    loadGenPQS: int
    "Displayed variable"
    loadGenPrioColsR: list
    "Colour"
    loadGenPrioScalsR: list
    "Scaling factor"
    loadGenShowGens: int
    "Generation circles"
    loadGenShowLoads: int
    "Load circles"
    loc_name: str
    "Name"
    localMapCatalogFile: str
    "Map configuration: Catalogue file"
    localMapEpsgCode: int
    "EPSG:"
    localMapScaleLimit: int
    "Map configuration: Minimum scale 1 :"
    mapLayer: int
    "Map configuration: Map layer"
    mapProvider: int
    "Map configuration: Provider"
    mapProviderUrl: object
    "Map configuration: Service URL"
    maxGeographicScale: int
    "Zoom-dependent visibility: Maximum geographic scale (value)"
    maxZoomSchematic: int
    "Zoom-dependent visibility: Maximum zoom level (value)"
    minGeographicScale: int
    "Zoom-dependent visibility: Minimum geographic scale (value)"
    minZoomSchematic: int
    "Zoom-dependent visibility: Minimum zoom level (value)"
    multiMapLayerConfStr: list
    "Multi map layer config string"
    oid_: int
    "ObjectID"
    pIntGrfnet: object
    "Default diagram fonts: Text box settings"
    pid_: int
    "ProjectID"
    plotBackgroundColor: int
    "Draw plot background: Colour"
    plotBackgroundOpacity: float
    "Draw plot background: Opacity"
    processImages: int
    "Adjust bitmaps"
    rOrder: float
    "Drawing order"
    root_id: object
    "Original Location"
    showColorLegend: int
    "Show colour legend"
    showHostingCap: int
    "Hosting capacity"
    showResultLegend: int
    "Show result legend"
    siteBrushStyle: int
    "Show sites: Brush Style"
    siteColor: int
    "Show sites: Colour"
    siteLineStyle: int
    "Show sites: Line style"
    siteLineWidth: float
    "Show sites: Line width"
    siteOpacity: int
    "Show sites: Opacity"
    siteShow: int
    "Show sites"
    systemLayer: int
    "System layer"
    tid_: int
    "TimeID"

    def AdaptWidth(*args): ...

    def Align(*args): ...

    def AttributeType(*args): ...

    def ChangeFont(*args): ...

    def ChangeLayer(*args): ...

    def ChangeRefPoints(*args): ...

    def ChangeWidthVisibilityAndColour(*args): ...

    def ClearData(*args): ...

    def Export(*args): ...

    def ExportToVec(*args): ...

    def HasReferences(*args): ...

    def Import(*args): ...

    def ImportFromVec(*args): ...

    def Mark(*args): ...

    def Reset(*args): ...

    def __getattr__(*args): ...


class IntGrfnet(PFGeneral):
    Internals: list
    "Contents ..."
    PrjList: str
    "GPS projection"
    allowFontsIndivTBs: int
    "Allow individual fonts for text boxes"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cColFrame: int
    "Diagram colouring"
    cDrawFormat: str
    "Format"
    cDrawOrient: int
    "Drawing orientation"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cimRdfId: list
    "RDF ID"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    defaultViewArea: object
    "Default view area"
    fold_id: object
    "In Folder"
    fontBraLabel: int
    "Font-ID  for branch labels"
    fontBraRes: int
    "Font-ID for branch results"
    fontNodLabel: int
    "Font-ID for node labels"
    fontNodRes: int
    "Font-ID for node results"
    fontTitle: int
    "Font-ID for title and legends"
    for_name: str
    "Foreign Key"
    frTrOut: int
    "Coordinate output transformation (A*x+b)"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iArrow: int
    "Direction arrow mode"
    iBeachB: int
    "Beach ball representation of composite nodes"
    iBraZoomLim: int
    "Geographic scale thresholds for visibility of: edge elements, except lines (1/x)"
    iCabDash: int
    "Line style for cables"
    iCrSwts: int
    "Create switches when connecting to busbar"
    iFrmNamBra: int
    "Labels Branches: Show frame"
    iFrmNamNod: int
    "Labels Nodes: Show frame"
    iFrmResBra: int
    "Results Branches: Show frame"
    iFrmResNod: int
    "Results Nodes: Show frame"
    iFrmSwt: int
    "Display frame around switches"
    iFrzPerm: int
    "Write protected"
    iGPS: int
    "Geographical data from network elements (zoom independent diagram)"
    iKRatio: int
    "Keep ratio"
    iLEOZoomLim: int
    "Geographic scale thresholds for visibility of: switch state boxes at line ends (1/x)"
    iLayZoomLim: int
    "annotation elements (deprecated: please use layer settings instead)"
    iLevel: int
    "Current graphic layers (legacy)"
    iMBBSwt: int
    "Show connected busbars as small dots in simplified substation representation"
    iMeasureLength: int
    "Re-adjust length of line when making graphical changes"
    iNoSwitch: int
    "Not visible if results are shown"
    iOHLDash: int
    "Line style for overhead lines"
    iPhasTec: int
    "Default phase technologies for terminals"
    iPrefBraC: int
    "Prefer branch coordinates"
    iScalFac: int
    "Use scaling factor for computation of distances"
    iSchemeStatus: int
    "Scheme Status"
    iSclBackLim: int
    "Minimum scale 1 :"
    iSetBGr: int
    "Set size of background image"
    iShowBC: int
    "Show bus couplers"
    iShowCoupTBs: int
    "Results: Always show result boxes of detailed couplers"
    iShowIndLS: int
    "Allow individual line style"
    iShowIndLW: int
    "Allow individual line width"
    iShowLL: int
    "Show coordinates in latitude/longitude"
    iShowLineTB: int
    "Show line from general text boxes to referenced objects"
    iShowNavi: int
    "Allow navigation pane to be shown"
    iShowScl: int
    "Show scale"
    iSimplf: int
    "Simplified representation of bus couplers and tie breakers"
    iSmallRes: int
    "Results: Space saving representation on connection lines"
    iStump: int
    "Branch off type"
    iSwitch: int
    "Switch state symbol at connection end"
    iTBZoomLim: int
    "text (1/x)"
    iTooltip: int
    "Show tooltip on network elements"
    iTrNam: int
    "Labels: Background"
    iTrans: int
    "Results: Background"
    iType: int
    "Diagram Type"
    iUTrSet: int
    "User coordinate space"
    loc_name: str
    "Name"
    maxTooltipObjs: int
    "Show tooltip on network elements: Maximum number of shown elements"
    oid_: int
    "ObjectID"
    ortho_on: int
    "Drawing aids: Line routing"
    pColScheme: object
    "Diagram colouring: Colouring Scheme"
    pColVI: object
    "Diagram colouring: Used colouring scheme"
    pDataFolder: object
    "Target folder for network elements"
    pid_: int
    "ProjectID"
    prjSettings: object
    "Project settings"
    rBGLBotX: float
    "X"
    rBGLBotY: float
    "Y"
    rBGRTopX: float
    "X"
    rBGRTopY: float
    "Y"
    rBraDistFac: float
    "Distance factor for one-port devices"
    rBraSzFac: float
    "Size factor for: edge elements"
    rBraSzFacSGL: float
    "Size factor for: edge elements"
    rDefOffBr: float
    "Offset factor when drawing one-port devices"
    rGPSLineWd: float
    "Line width"
    rGridFak: float
    "Grid-factor"
    rGridX: float
    "Horizontal grid size"
    rGridY: float
    "Vertical grid size"
    rLBotX: float
    "X"
    rLBotXc: float
    "World coordinate space Left bottom: X"
    rLBotY: float
    "Y"
    rLBotYc: float
    "World coordinate space Left bottom: Y"
    rLEOSzFac: float
    "Size factor for: line end symbols"
    rLEOSzFacSGL: float
    "Size factor for: line end symbols"
    rLlodSzFac: float
    "Size factor for: line loads, compensations and section transitions"
    rMBBConWid: float
    "Size factor for: connection circles on simplified substations"
    rNodWid: float
    "Node width factor"
    rOffSemOrt: float
    "Drawing aids: Semi-orthogonal offset"
    rRTopX: float
    "X"
    rRTopXc: float
    "World coordinate space Right top: X"
    rRTopY: float
    "Y"
    rRTopYc: float
    "World coordinate space Right top: Y"
    rScalFac: float
    "1 :"
    rScaleX: float
    "X"
    rScaleY: float
    "Y"
    rSiteSzFac: float
    "Size factor for: sites"
    rSiteSzFacSGL: float
    "Size factor for: sites"
    rSubSzFac: float
    "Size factor for: substations"
    rSubSzFacSGL: float
    "Size factor for: substations (beach ball representation)"
    rTermSzFac: float
    "Size factor for: terminals"
    rTermSzFacSGL: float
    "terminals"
    rTransX: float
    "X"
    rTransY: float
    "Y"
    rTxtSzFac: float
    "Size factor for: text"
    rULBotX: float
    "User coordinate space Left bottom: X"
    rULBotY: float
    "User coordinate space Left bottom: Y"
    rURTopX: float
    "User coordinate space Right top: X"
    rURTopY: float
    "User coordinate space Right top: Y"
    rVoltLev: float
    "Voltage level default"
    rWSpace: float
    "Margin at full zoom"
    rXFak: float
    "X transformation factor"
    rYFak: float
    "Y transformation factor"
    rZoomLBX: float
    "X-zoom left bottom"
    rZoomLBY: float
    "Y-zoom left bottom"
    rZoomRTX: float
    "X-zoom right top"
    rZoomRTY: float
    "Y-zoom right top"
    root_id: object
    "Original Location"
    sAttr: list
    "Options"
    sBackFile: list
    "Catalogue file"
    sBordSym: list
    "Border symbol"
    sDefSiteSym: list
    "Default site symbol"
    sDefSym: list
    "Default substation symbol"
    sSiteBordSym: list
    "Border symbol"
    sSiteSymbol: list
    "Symbol"
    sSiteTyp: list
    "Site Type"
    sSubstTyp: list
    "Substation Type"
    sSymFile: str
    "Symbol file"
    sSymbol: list
    "Symbol"
    showSearchField: int
    "Show search field"
    snap_on: int
    "Drawing aids: Snap elements to grid"
    symbolComponentMask: int
    "Visible symbol components (mask)"
    tid_: int
    "TimeID"
    usePrjFonts: int
    "Use fonts from project settings"

    def AttributeType(*args): ...

    def Close(*args): ...

    def HasReferences(*args): ...

    def SetFontFor(*args): ...

    def SetLayerVisibility(*args): ...

    def SetSymbolComponentVisibility(*args): ...

    def Show(*args): ...

    def __getattr__(*args): ...


class IntIcon(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    transpColor: int
    "Define colour as transparent"
    transpColorBlue: int
    "Define colour as transparent: blue"
    transpColorGreen: int
    "Define colour as transparent: green"
    transpColorRed: int
    "Define colour as transparent: red"

    def AttributeType(*args): ...

    def Export(*args): ...

    def HasReferences(*args): ...

    def Import(*args): ...

    def __getattr__(*args): ...


class IntMat(PFGeneral):
    ColLabels: list
    "Col labels"
    M: list
    "Matrix"
    RowLabels: list
    "Row labels"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iec_tab: str
    "Table"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def ColLbl(*args): ...

    def Get(*args): ...

    def GetColumnLabel(*args): ...

    def GetColumnLabelIndex(*args): ...

    def GetNumberOfColumns(*args): ...

    def GetNumberOfRows(*args): ...

    def GetRowLabel(*args): ...

    def GetRowLabelIndex(*args): ...

    def HasReferences(*args): ...

    def Init(*args): ...

    def Invert(*args): ...

    def Multiply(*args): ...

    def NCol(*args): ...

    def NRow(*args): ...

    def Resize(*args): ...

    def RowLbl(*args): ...

    def Save(*args): ...

    def Set(*args): ...

    def SetColumnLabel(*args): ...

    def SetRowLabel(*args): ...

    def SizeX(*args): ...

    def SizeY(*args): ...

    def SortToColum(*args): ...

    def SortToColumn(*args): ...

    def __getattr__(*args): ...


class IntMon(PFGeneral):
    cDevice: list
    "Component"
    cIdent: list
    "Identifier"
    cPhase: list
    "Phase"
    cUnit: list
    "Unit"
    cforms: list
    "Format"
    charact: list
    "Charact."
    cheader: list
    "Customised Header"
    chr_name: str
    "Characteristic Name"
    classnm: str
    "Class Name"
    cpHeadFold: object
    "Head Folder"
    csample: list
    "Sample"
    cvariables: list
    "Variable"
    dat_src: str
    "Data source"
    filtbus: str
    "Variable filter: Bus and Phase"
    filtvar: str
    "Variable Name"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_all: int
    "Display All"
    iopt_loc: int
    "internal: Add Keywords to Bus List"
    iopt_out: int
    "Display Values during Simulation in Output Window (see Simulation Command)"
    iopt_rec: int
    "Consider Recording Limits"
    iopt_var: int
    "Variable filter: Variable Set"
    loc_name: str
    "Name"
    obj_id: object
    "Object"
    objname: list
    "Element"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    setFilt: object
    "Element filter"
    tid_: int
    "TimeID"
    vars: list
    "Complete List of Selected Variables"

    def AddVar(*args): ...

    def AddVars(*args): ...

    def AttributeType(*args): ...

    def ClearVars(*args): ...

    def GetVar(*args): ...

    def HasReferences(*args): ...

    def NVars(*args): ...

    def PrintAllVal(*args): ...

    def PrintVal(*args): ...

    def RemoveVar(*args): ...

    def __getattr__(*args): ...


class IntOutage(PFGeneral):
    Ptrans: float
    "Active Power Transfer"
    Qtrans: float
    "Reactive Power Transfer"
    Sksstrans: float
    "Subtransient Short-Circuit Level Transfer"
    Skstrans: float
    "Transient Short-Circuit Level Transfer"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cObjGenDerat: object
    "Derated Generator"
    cObjLoadTransf: object
    "Source of Load Demand Transfer"
    cObjOutage: object
    "Outaged Element"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    endtime: int
    "End Time"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    ftrans: float
    "Power Transfer"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iType: int
    "Outage Type"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Ignored"
    pObj: object
    "Outaged Element"
    pTrans: object
    "Destination of Load Demand Transfer"
    pid_: int
    "ProjectID"
    pmaxratf: float
    "MW reductions"
    root_id: object
    "Original Location"
    starttime: int
    "Start Time"
    stateconsistent: int
    "Correctly reflected"
    tid_: int
    "TimeID"
    transinputtype: int
    "Value Type:relative:absolute"

    def Apply(*args): ...

    def ApplyAll(*args): ...

    def AttributeType(*args): ...

    def Check(*args): ...

    def CheckAll(*args): ...

    def HasReferences(*args): ...

    def IsInStudyTime(*args): ...

    def IsInStudytime(*args): ...

    def ResetAll(*args): ...

    def __getattr__(*args): ...


class IntPlannedout(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    components: list
    "Components"
    contents: list
    "Events"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    endtime: int
    "End Time"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Ignored"
    pid_: int
    "ProjectID"
    priority: int
    "Priority"
    recsettings: list
    "Settings"
    recurrence: int
    "Recurrent"
    root_id: object
    "Original Location"
    starttime: int
    "Start Time"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def SetRecurrence(*args): ...

    def __getattr__(*args): ...


class IntPlot(PFGeneral):
    XGridHlp: int
    "Grid x-Axis: Help"
    XGridMain: int
    "Grid x-Axis: Main"
    YGridHlp: int
    "Grid y-Axis: Help"
    YGridMain: int
    "Grid y-Axis: Main"
    auto_yscl: int
    "y-Axis: Auto Scale"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    cy_map: int
    "y-Axis: Scaling"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mxpos: int
    "Ticks x-Axis: Main"
    mypos: int
    "Ticks y-Axis: Main"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sh_off: int
    "y-Axis Adapt Scale: Show Deviation from Offset"
    tid_: int
    "TimeID"
    txpos: int
    "Ticks x-Axis: Small"
    typos: int
    "Ticks y-Axis: Small"
    y_fit: int
    "y-Axis: Adapt Scale"
    y_map: int
    "y-Axis: Scale"
    y_max: float
    "y-Axis Limits: Maximum"
    y_min: float
    "y-Axis Limits: Minimum"
    y_off: float
    "y-Axis Adapt Scale: Offset"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def SetAdaptY(*args): ...

    def SetAutoScaleY(*args): ...

    def SetScaleY(*args): ...

    def __getattr__(*args): ...


class IntPrjfolder(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_date: int
    "Data Date"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    filter: str
    "Class Filter"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_icon: str
    "Icon"
    iopt_typ: str
    "Folder Type"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    recnetdatonly: int
    "Record Network Data folder only"
    root_id: object
    "Original Location"
    share: int
    "Sharing"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def GetProjectFolderType(*args): ...

    def HasReferences(*args): ...

    def IsProjectFolderType(*args): ...

    def __getattr__(*args): ...


class IntQlim(PFGeneral):
    MatQmaxpu: list
    "Matrix for Qmax"
    MatQminpu: list
    "Matrix for Qmin"
    MatrixQmax: list
    "Matrix for Qmax"
    MatrixQmin: list
    "Matrix for Qmin"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cap_P: list
    "Active Power"
    cap_Ppu: list
    "Active Power"
    cap_Qmn: list
    "Min. React. Pow."
    cap_Qmnpu: list
    "Min. React. Pow."
    cap_Qmx: list
    "Max. React. Pow."
    cap_Qmxpu: list
    "Max. React. Pow."
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    inputmod: int
    "Input Model"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    psetpoin: list
    "P-setpoints"
    psetpoinpu: list
    "P-setpoints"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    volevel: list
    "Voltage Level"
    volevelpu: list
    "Voltage Level"
    voltagedep: int
    "Consider voltage dependent limits"

    def AttributeType(*args): ...

    def GetQlim(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class IntRas(PFGeneral):
    availability: list
    "Availability"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    eventList: int
    "Remedial actions executed if trigger is true Create remedial actions: :Switch Event:Dispatch Event:Tap Event:Power Transfer Event:Load Event"
    events: list
    "Remedial actions executed if trigger is true: Remedial actions"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hasAvailability: int
    "Active only at a certain time"
    iRepeat: int
    "RAS can be triggered more than once per Contingency"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    oneGate: int
    "Trigger: Logical Gate to combine triggers:And:Or"
    outserv: int
    "Out of service"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sequenceNr: int
    "RAS Sequence-Nr"
    tid_: int
    "TimeID"
    triggers: list
    "Trigger: Trigger"

    def AddEvent(*args): ...

    def AddTrigger(*args): ...

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def IsValid(*args): ...

    def __getattr__(*args): ...


class IntRunarrange(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iEndTime: int
    "End Time"
    iSchemeStatus: int
    "Scheme Status"
    iStartTime: int
    "Start Time"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pSubstat: object
    "Substation"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def GetSwitchStatus(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class IntScenario(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAcIncremental: int
    "Include incremental subset in activation"
    iCurConfig: int
    "Based on current scenario configuration"
    iModified: int
    "Modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sShort: str
    "Short Name"
    tid_: int
    "TimeID"

    def Activate(*args): ...

    def Apply(*args): ...

    def ApplySelective(*args): ...

    def AttributeType(*args): ...

    def Deactivate(*args): ...

    def DiscardChanges(*args): ...

    def GetObjects(*args): ...

    def GetOperationValue(*args): ...

    def HasReferences(*args): ...

    def ReleaseMemory(*args): ...

    def Save(*args): ...

    def SetOperationValue(*args): ...

    def __getattr__(*args): ...


class IntScensched(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAcIncremental: int
    "Include incremental subsets in scenario activation"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pScenario: list
    "Operating Scenario"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tEndTime: list
    "End Time"
    tStartTime: list
    "Start Time"
    tid_: int
    "TimeID"

    def Activate(*args): ...

    def AttributeType(*args): ...

    def Deactivate(*args): ...

    def DeleteRow(*args): ...

    def GetScenario(*args): ...

    def GetStartEndTime(*args): ...

    def HasReferences(*args): ...

    def SearchScenario(*args): ...

    def __getattr__(*args): ...


class IntScheme(PFGeneral):
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iEndTime: int
    "Restricted Validity Period: End Time"
    iSchemeStatus: int
    "Scheme Status"
    iStartTime: int
    "Restricted Validity Period: Start Time"
    iValPeriod: int
    "Restricted Validity Period"
    icolor: int
    "Colour"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sRepres: list
    "Representative"
    tFromAc: int
    "Activation Time: starting"
    tToAc: int
    "Activation Time: completed"
    tid_: int
    "TimeID"

    def Activate(*args): ...

    def AttributeType(*args): ...

    def Consolidate(*args): ...

    def Deactivate(*args): ...

    def GetActiveScheduler(*args): ...

    def HasReferences(*args): ...

    def NewStage(*args): ...

    def __getattr__(*args): ...


class IntSscheduler(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def Activate(*args): ...

    def AttributeType(*args): ...

    def Deactivate(*args): ...

    def HasReferences(*args): ...

    def Update(*args): ...

    def __getattr__(*args): ...


class IntSstage(PFGeneral):
    AddCosts: float
    "Costs for expansion: Additional costs"
    InvCosts: float
    "Costs for expansion: Investment costs"
    LifeSpan: int
    "Commercial equipment value: Expected life span"
    OrigVal: float
    "Commercial equipment value: Original value"
    ScrVal: float
    "Commercial equipment value: Scrap value"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cActTime: int
    "Effective Activation Time"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iExclude: int
    "Exclude from Activation"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Target"
    tAcTime: int
    "Activation Time"
    tid_: int
    "TimeID"
    weekOfActivation: int
    "Week (Activation)"

    def Activate(*args): ...

    def AttributeType(*args): ...

    def CreateStageObject(*args): ...

    def EnableDiffMode(*args): ...

    def GetScheme(*args): ...

    def GetVariation(*args): ...

    def HasReferences(*args): ...

    def IsExcluded(*args): ...

    def PrintModifications(*args): ...

    def ReadValue(*args): ...

    def WriteValue(*args): ...

    def __getattr__(*args): ...


class IntSubset(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    classFilter: str
    "Class Filter"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iCount: int
    "Number of Elements"
    iExcluded: int
    "Exclude grid from recording"
    iSchemeStatus: int
    "Scheme Status"
    iSize: list
    "Memory Size"
    iType: int
    "Type:&0&undefined:&1&Virtual Power Plant:&2&Demand:&3&Generation:&4&Switch:&5&RA:&6&Tap:&7&Voltage:&8&Feeder:&9&Zone:&10&Compensation:&12&Out-of-Service:&13&External Measurement:&11&Other:&14&Grid:&15&Incremental"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pGrid: object
    "Grid"
    paraminfo: list
    "Parameter Information"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def Apply(*args): ...

    def ApplySelective(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def GetConfiguration(*args): ...

    def GetObjects(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class IntThrating(PFGeneral):
    ContRating: float
    "Continuous Rating"
    MyMatrix: list
    "Short term ratings"
    PostRating: float
    "Post-fault continuous rating"
    PreRating: float
    "Pre-fault continuous rating"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    configSolar: list
    "Solar irradiance (GHI): Solar irradiance (GHI)"
    configTa: list
    "Ambient temperature: Ambient temperature"
    configWind: list
    "Wind speed: Wind speed"
    contRatMat: list
    "Continuous Rating"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    duration: list
    "Consider short term ratings: Duration"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_unit: int
    "Unit:MVA:kA:%"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    optSolar: int
    "Solar irradiance (GHI)"
    optTa: int
    "Ambient temperature"
    optWind: int
    "Wind speed"
    pid_: int
    "ProjectID"
    preload: list
    "Consider short term ratings: Preload"
    root_id: object
    "Original Location"
    table_valid: int
    "Consider short term ratings"
    tid_: int
    "TimeID"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"

    def AttributeType(*args): ...

    def GetCriticalTimePhase(*args): ...

    def GetRating(*args): ...

    def HasReferences(*args): ...

    def Resize(*args): ...

    def __getattr__(*args): ...


class IntUrl(PFGeneral):
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    geoBoundsEast: float
    "Map Service Configuration Specify geographic map bounds: east"
    geoBoundsNorth: float
    "Map Service Configuration Specify geographic map bounds: north"
    geoBoundsSet: int
    "Map Service Configuration: Specify geographic map bounds"
    geoBoundsSouth: float
    "Map Service Configuration Specify geographic map bounds: south"
    geoBoundsWest: float
    "Map Service Configuration Specify geographic map bounds: west"
    geoSearchProviderType: int
    "Geographic search provider"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    httpAccessDataSet: int
    "Map Service Configuration: Specify HTTP access data"
    httpPassword: str
    "Map Service Configuration Specify HTTP access data: Password"
    httpUsername: str
    "Map Service Configuration Specify HTTP access data: Username"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mapProjection: str
    "Map Service Configuration: Preferred projection"
    mapReverseAxes: int
    "Map Service Configuration: Reverse axes of projection space"
    mapServerProtocol: int
    "Map Service Configuration: Map server protocol:WMTS 1.0.0:WMS 1.1.1:WMS 1.3.0:XYZ (Slippy Map)"
    oid_: int
    "ObjectID"
    pObj: object
    "Related to"
    pid_: int
    "ProjectID"
    resourceType: int
    "Resource type:Generic:Map Service:Geographic Search Provider"
    root_id: object
    "Original Location"
    sUrl: str
    "Address"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def View(*args): ...

    def __getattr__(*args): ...


class IntVec(PFGeneral):
    V: list
    "Vector"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Get(*args): ...

    def HasReferences(*args): ...

    def Init(*args): ...

    def Max(*args): ...

    def Mean(*args): ...

    def Min(*args): ...

    def Resize(*args): ...

    def Save(*args): ...

    def Set(*args): ...

    def Size(*args): ...

    def Sort(*args): ...

    def __getattr__(*args): ...


class IntVecobj(PFGeneral):
    V: list
    "Vector"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    classFilter: list
    "Class Filter"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    infolder: list
    "In Folder"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    vecSize: int
    "Size"

    def AttributeType(*args): ...

    def Get(*args): ...

    def HasReferences(*args): ...

    def Resize(*args): ...

    def Save(*args): ...

    def Search(*args): ...

    def Set(*args): ...

    def Size(*args): ...

    def __getattr__(*args): ...


class IntVersion(PFGeneral):
    approval: int
    "Complete project approval for versioning required"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Content"
    cpHeadFold: object
    "Head Folder"
    creation: int
    "Point in Time"
    creator: str
    "Created by"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dbid: int
    "Internal database id"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    notify: int
    "Notify users of derived projects"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def CreateDerivedProject(*args): ...

    def GetDerivedProjects(*args): ...

    def GetHistoricalProject(*args): ...

    def HasReferences(*args): ...

    def Rollback(*args): ...

    def __getattr__(*args): ...


class IntViewbookmark(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hotkey: int
    "Hotkey"
    hotkeySelectBox: int
    "Hotkey: New hotkey:   :CTRL+1:CTRL+2:CTRL+3:CTRL+4:CTRL+5:CTRL+6:CTRL+7:CTRL+8:CTRL+9"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pDiagram: object
    "Diagram"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    viewAreaBottom: float
    "View Area: Bottom"
    viewAreaLeft: float
    "View Area: Left"
    viewAreaRight: float
    "View Area: Right"
    viewAreaTop: float
    "View Area: Top"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def JumpTo(*args): ...

    def UpdateFromCurrentView(*args): ...

    def __getattr__(*args): ...


class PltAxis(PFGeneral):
    Internals: list
    "Contents ..."
    axisDateFormat: int
    "Date format"
    axisDimension: int
    "Axis dimension"
    axisFrequencyUnit: int
    "Frequency Unit"
    axisIndex: int
    "Axis index"
    axisLineColor: int
    "Axis line colour"
    axisLineStyle: int
    "Axis line style"
    axisLineWidth: int
    "Axis line width"
    axisMode: int
    "Axis mode:Default:Time:Date and time:Frequency:Discrete (net elements):XY plot"
    axisTimeOfDayFormat: int
    "Time of day format"
    axisTimeUnit: int
    "Time unit"
    centreOrigin: int
    "Scale to Contents: Centre origin"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    discreteTextAngle: float
    "Font Style: Text angle"
    fold_id: object
    "In Folder"
    fontID: int
    "Font-ID"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    keepTicksCongruent: int
    "Keep tick marks congruent with first axis"
    labelColor: int
    "Font Style: Label colour"
    labelOffset: float
    "Font Style: Label offset"
    limitMinimumToOrigin: int
    "Scale to Contents: Limit minimum to origin if possible"
    loc_name: str
    "Name"
    majorGridlineColor: int
    "Line Style: Gridline colour"
    majorGridlineStyle: int
    "Line Style: Gridline style"
    majorGridlineWidth: int
    "Line Style: Gridline width"
    majorTickCount: int
    "Tick Mark Positions: Major tick count"
    majorTickExtent: int
    "Line Style: Tick extent:None:Outside:Inside:Both sides"
    majorTickStep: float
    "Tick Mark Positions: Major tick step size"
    majorTickTimeStep: int
    "Tick Mark Positions: Major tick step size"
    majorTickTimeUnit: int
    "Tick Mark Positions: Unit:Milliseconds:Seconds:Minutes:Hours:Days:Months:Years"
    minorGridlineColor: int
    "Line Style: Gridline colour"
    minorGridlineStyle: int
    "Line Style: Gridline style"
    minorGridlineWidth: int
    "Line Style: Gridline width"
    minorTickCount: int
    "Tick Mark Positions: Minor tick count"
    minorTickExtent: int
    "Line Style: Tick extent:None:Outside:Inside:Both sides"
    minorTickStep: float
    "Tick Mark Positions: Minor tick step size"
    minorTickTimeStep: int
    "Tick Mark Positions: Minor tick step size"
    minorTickTimeUnit: int
    "Tick Mark Positions: Unit:Milliseconds:Seconds:Minutes:Hours:Days:Months:Years"
    numExponentCase: int
    "Number Format: Exponent character:'e':'E'"
    numFormatDecimals: int
    "Number Format: Decimals"
    numFormatDigits: int
    "Number Format: Digits (maximum)"
    numFormatMode: int
    "Number Format: Format:concise:fixed decimals:scientific"
    numFormatShowPlus: int
    "Number Format: Show sign for positive values"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    rangeDateTimeMax: int
    "Time Period: End"
    rangeDateTimeMaxMs: int
    "Milliseconds"
    rangeDateTimeMin: int
    "Time Period: Start"
    rangeDateTimeMinMs: int
    "Milliseconds"
    rangeExponentMax: int
    "Range (exponents): Maximum 1e"
    rangeExponentMin: int
    "Range (exponents): Minimum 1e"
    rangeMax: float
    "Range: Maximum"
    rangeMin: float
    "Range: Minimum"
    root_id: object
    "Original Location"
    scaleDuringLivePlot: int
    "Scale to Contents: Scale during live plotting"
    scaleOnDataChange: int
    "Scale to Contents: Scale when calculation data changes"
    scaleRelativeMargin: int
    "Scale to Contents: Relative margin"
    scaleType: int
    "Scale Type"
    showUnit: int
    "Font Style: Show unit (if unique)"
    tickPositionFrame: int
    "Tick Mark Positions"
    tickReferenceValue: float
    "Tick Mark Positions: Reference value"
    tid_: int
    "TimeID"
    useAutoTickSettings: int
    "Tick Mark Positions: Determine tick positions automatically"
    vectorCoords: int
    "Representation of Coordinates"

    def AttributeType(*args): ...

    def DoAutoScale(*args): ...

    def HasReferences(*args): ...

    def SetFont(*args): ...

    def __getattr__(*args): ...


class PltComplexdata(PFGeneral):
    autoPositionCurveArea: int
    "Curve Area Position (mm): Auto-Position Curve Area"
    borderColor: int
    "Border and Background: Border colour"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    colourPalette: object
    "Colour palette"
    commonResultFile: object
    "Data Source: Result file"
    complexVariable: list
    "Complex Variable"
    cpHeadFold: object
    "Head Folder"
    curveAreaBottom: float
    "Curve Area Position (mm): Bottom"
    curveAreaLeft: float
    "Curve Area Position (mm): Left"
    curveAreaRight: float
    "Curve Area Position (mm): Right"
    curveAreaTop: float
    "Curve Area Position (mm): Top"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dataSourceType: int
    "Data Source"
    dataTableColour: list
    "Colour"
    dataTableElement: list
    "Element"
    dataTableLabel: list
    "Description"
    dataTableLineStyle: list
    "Style"
    dataTableLineWidth: list
    "Width"
    dataTableResultElement: list
    "Element"
    dataTableResultFile: list
    "Result File"
    dataTableTrafoOperator: list
    "Operation"
    dataTableTrafoVariable: list
    "Transformation Variable"
    dataTableVariable: list
    "Complex Variable"
    dataTableVisible: list
    "Visible"
    drawArrowHeads: int
    "Plot Features: Draw arrow heads"
    drawBorder: int
    "Border and Background: Draw border"
    enableUnitAutoScaling: int
    "Determine unit scales automatically"
    enableVectorTrafo: int
    "Plot Features: Vector transformation"
    fillBackground: int
    "Border and Background: Fill background"
    fillColor: int
    "Border and Background: Fill colour"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_dataSourceResultFile: int
    "Data Source: Result file"
    iopt_dataSourceVariables: int
    "Data Source: Element variables"
    labelFontColor: int
    "Label Font: Colour"
    labelFontID: int
    "Font-ID"
    loc_name: str
    "Name"
    numExponentCase: int
    "Number Format: Exponent character:'e':'E'"
    numFormatDecimals: int
    "Number Format: Decimals"
    numFormatDigits: int
    "Number Format: Digits (maximum)"
    numFormatMode: int
    "Number Format: Format:concise:fixed decimals:scientific"
    numFormatShowPlus: int
    "Number Format: Show sign for positive values"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    showAllPhases: int
    "Show all phases"
    tid_: int
    "TimeID"
    timePoint: float
    "Time Point Selection: Time Point"
    timePointCursor: object
    "Time Point Selection: Cursor"
    transformationVariable: list
    "Transformation Variable"
    unitScalingTableScale: list
    "Scale"
    unitScalingTableUnit: list
    "Unit"
    useIndividualResults: int
    "Data Source: Select results individually per vector"
    vectorLabels: int
    "Plot Features: Vector labels:None:Automatic:Coordinates, Polar:Coordinates, Cartesian:Phase Only"

    def AddVector(*args): ...

    def AttributeType(*args): ...

    def ChangeColourPalette(*args): ...

    def ClearVectors(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class PltDataseries(PFGeneral):
    Internals: list
    "Contents ..."
    autoPositionCurveArea: int
    "Curve Area Position (mm): Auto-Position Curve Area"
    autoSearchResultFile: int
    "Data Source: Auto-search results"
    borderColor: int
    "Border and Background: Border colour"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    colourPalette: object
    "Colour palette"
    cpHeadFold: object
    "Head Folder"
    curveAngleStore: list
    "Angle"
    curveAreaBottom: float
    "Curve Area Position (mm): Bottom"
    curveAreaLeft: float
    "Curve Area Position (mm): Left"
    curveAreaRight: float
    "Curve Area Position (mm): Right"
    curveAreaTop: float
    "Curve Area Position (mm): Top"
    curveFunctionStore: list
    "Function object"
    curveStackingMode: int
    "Curve stacking"
    curveStackingSelector: int
    "Plot Features: Stacking mode:Values:Absolute values:Relative values:Percentage"
    curveTableAngle: list
    "Angle"
    curveTableAxisIndexX: list
    "X-Axis"
    curveTableAxisIndexY: list
    "Y-Axis"
    curveTableColor: list
    "Colour"
    curveTableElement: list
    "Element"
    curveTableElementX: list
    "Element X-Axis"
    curveTableFillStyle: list
    "Fill Style"
    curveTableFunction: list
    "Function"
    curveTableLabel: list
    "Label"
    curveTableLineStyle: list
    "Line Style"
    curveTableLineWidth: list
    "Line Width"
    curveTableNormValue: list
    "Nom.Val."
    curveTableNormValueX: list
    "Nom.Val. X"
    curveTableNormalise: list
    "Normalise"
    curveTableNormaliseX: list
    "Normalise X"
    curveTableResultFile: list
    "Result File"
    curveTableSampleMarker: list
    "Sample Marker"
    curveTableShape: list
    "Curve Shape"
    curveTableVariable: list
    "Variable"
    curveTableVariableX: list
    "Variable X-Axis"
    curveTableVisible: list
    "Visible"
    curveVariableStore: list
    "Variable Y-Axis"
    curveVariableStoreX: list
    "Variable X-Axis"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dataTransformationMode: int
    "Plot Features: "
    dateRangeMax: int
    "End time"
    dateRangeMaxMs: int
    "Milliseconds"
    dateRangeMin: int
    "Start time"
    dateRangeMinMs: int
    "Milliseconds"
    discreteBarAxisElements: list
    "Elements"
    discreteBarAxisPath: object
    "Path"
    drawBorder: int
    "Border and Background: Draw border"
    drawDirectionArrows: int
    "Plot Features: Draw direction arrows"
    enableCurveShapes: int
    "Plot Features: Additional curve shapes"
    enableCurveStacking: int
    "Plot Features: Curve stacking"
    enableDataTrafo: int
    "Plot Features: Data transformation"
    fillBackground: int
    "Border and Background: Fill background"
    fillColor: int
    "Border and Background: Fill colour"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    harmonicLimits: list
    "Harmonic Limits: Show"
    harmonicLimitsFillColor: int
    "Harmonic Limits: Style"
    harmonicLimitsFillStyle: int
    "Harmonic Limits: Style"
    harmonicStandard: list
    "Harmonic Limits: Standard"
    iSchemeStatus: int
    "Scheme Status"
    labelFontColor: int
    "Label Font: Colour"
    labelFontID: int
    "Font-ID"
    loc_name: str
    "Name"
    normalisationUnit: int
    "Normalisation Unit"
    numExponentCase: int
    "Number Format: Exponent character:'e':'E'"
    numFormatDecimals: int
    "Number Format: Decimals"
    numFormatDigits: int
    "Number Format: Digits (maximum)"
    numFormatMode: int
    "Number Format: Format:concise:fixed decimals:scientific"
    numFormatShowPlus: int
    "Number Format: Show sign for positive values"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    resultOriginLabel: list
    resultTypeFilter: str
    "Data Source: Calculation type"
    root_id: object
    "Original Location"
    showHarmonicFundFrequency: int
    "Plot Features: Show fundamental frequency"
    showTotalHarmonicDistortion: int
    "Plot Features: Show corresponding THD or THF"
    specifyByDate: int
    "Specify time range: Use date format"
    specifyTimeRange: int
    "Specify time range"
    tid_: int
    "TimeID"
    timeRangeMax: float
    "Specify time range: End time"
    timeRangeMin: float
    "Specify time range: Start time"
    useAxisTextFormat: int
    "Use text format settings from axes for curve labels"
    useIndividualResults: int
    "Data Source: Select results individually per curve"
    userSelectedResultFile: object
    "Data Source: User-defined result file"

    def AddCurve(*args): ...

    def AddXYCurve(*args): ...

    def AttributeType(*args): ...

    def ChangeColourPalette(*args): ...

    def ClearCurves(*args): ...

    def GetDataSource(*args): ...

    def GetIntCalcres(*args): ...

    def HasReferences(*args): ...

    def RemoveCurve(*args): ...

    def __getattr__(*args): ...


class PltLegend(PFGeneral):
    Internals: list
    "Contents ..."
    alwaysShowUnits: int
    "Text Format: Always show units"
    borderColor: int
    "Border and Background: Border colour"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    drawBorder: int
    "Border and Background: Draw border"
    fillBackground: int
    "Border and Background: Fill background"
    fillColor: int
    "Border and Background: Fill colour"
    floatingPosBottom: float
    "Floating Position (mm): Bottom"
    floatingPosLeft: float
    "Floating Position (mm): Left"
    floatingPosRight: float
    "Floating Position (mm): Right"
    floatingPosTop: float
    "Floating Position (mm): Top"
    fold_id: object
    "In Folder"
    fontColor: int
    "Text Format: Font colour"
    fontID: int
    "Font-ID"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    includeOnlyDrawnCurves: int
    "Positioning and Layout: Include only drawn curves"
    layoutMode: int
    "Positioning and Layout: Layout:automatic:columns:horizontal"
    lineSpacingFactor: float
    "Text Format: Line spacing"
    loc_name: str
    "Name"
    margin: float
    "Positioning and Layout: Margin"
    maxRelativeSize: float
    "Positioning and Layout: Maximum size"
    numColumns: int
    "Positioning and Layout: Num columns"
    oid_: int
    "ObjectID"
    padding: float
    "Positioning and Layout: Padding"
    pid_: int
    "ProjectID"
    position: int
    "Positioning and Layout: Position:floating:top left:top centre:top right:bottom left:bottom centre:bottom right:left:right"
    reverseItemOrder: int
    "Positioning and Layout: Reverse item order"
    root_id: object
    "Original Location"
    showLegend: int
    "Show legend"
    tid_: int
    "TimeID"
    useShortVarDesc: int
    "Text Format: Use short variable description"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def SetFont(*args): ...

    def __getattr__(*args): ...


class PltLinebarplot(PFGeneral):
    Internals: list
    "Contents ..."
    axisVisibilityX: int
    "Axis Visibility: Show bottom X-Axis"
    axisVisibilityX2: int
    "Axis Visibility: Show top X-Axis"
    axisVisibilityY: int
    "Axis Visibility: Show left Y-Axis"
    axisVisibilityY2: int
    "Axis Visibility: Show right Y-Axis"
    borderColor: int
    "Border and Background: Border colour"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    drawBorder: int
    "Border and Background: Draw border"
    elementPaddingBottom: float
    "Element Padding (mm): Bottom"
    elementPaddingLeft: float
    "Element Padding (mm): Left"
    elementPaddingRight: float
    "Element Padding (mm): Right"
    elementPaddingTop: float
    "Element Padding (mm): Top"
    fillBackground: int
    "Border and Background: Fill background"
    fillColor: int
    "Border and Background: Fill colour"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pageOrderIndex: int
    "Page Order"
    pid_: int
    "ProjectID"
    plotAreaBottom: float
    "Plot Position on Page (mm): Bottom"
    plotAreaLeft: float
    "Plot Position on Page (mm): Left"
    plotAreaRight: float
    "Plot Position on Page (mm): Right"
    plotAreaTop: float
    "Plot Position on Page (mm): Top"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    xAxis2Sharing: int
    "Top X-Axis: X-Axis Sharing"
    xAxisSharing: int
    "Bottom X-Axis: X-Axis Sharing"
    yAxis2Sharing: int
    "Right Y-Axis: Y-Axis Sharing"
    yAxisSharing: int
    "Left Y-Axis: Y-Axis Sharing"

    def AttributeType(*args): ...

    def ChangeStyle(*args): ...

    def DoAutoScale(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def GetAxisX(*args): ...

    def GetAxisY(*args): ...

    def GetDataSeries(*args): ...

    def GetLegend(*args): ...

    def GetTitleObject(*args): ...

    def HasReferences(*args): ...

    def SetAutoScaleModeX(*args): ...

    def SetAutoScaleModeY(*args): ...

    def SetAxisSharingLevelX(*args): ...

    def SetAxisSharingLevelY(*args): ...

    def SetScaleTypeX(*args): ...

    def SetScaleTypeY(*args): ...

    def SetScaleX(*args): ...

    def SetScaleY(*args): ...

    def __getattr__(*args): ...


class PltTitle(PFGeneral):
    Internals: list
    "Contents ..."
    borderColor: int
    "Border and Background: Border colour"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    drawBorder: int
    "Border and Background: Draw border"
    fillBackground: int
    "Border and Background: Fill background"
    fillColor: int
    "Border and Background: Fill colour"
    floatingPosLeft: float
    "Floating Position (mm): Left"
    floatingPosTop: float
    "Floating Position (mm): Top"
    fold_id: object
    "In Folder"
    fontColor: int
    "Text Format: Font colour"
    fontID: int
    "Font-ID"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    margin: float
    "Positioning and Layout: Margin"
    oid_: int
    "ObjectID"
    padding: float
    "Positioning and Layout: Padding"
    pid_: int
    "ProjectID"
    position: int
    "Positioning and Layout: Position:floating:top left:top centre:top right:bottom left:bottom centre:bottom right:left:right"
    root_id: object
    "Original Location"
    showTitle: int
    "Title: Show title"
    tid_: int
    "TimeID"
    titleString: list
    "Title: Title"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def SetFont(*args): ...

    def __getattr__(*args): ...


class PltVectorplot(PFGeneral):
    Internals: list
    "Contents ..."
    axisVisibilityX: int
    "Axis Visibility: Show X-Axis"
    axisVisibilityY: int
    "Axis Visibility: Show Y-Axis"
    borderColor: int
    "Border and Background: Border colour"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    createVectorPlot: int
    "Create Vector Plot"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    drawBorder: int
    "Border and Background: Draw border"
    elementPaddingBottom: float
    "Element Padding (mm): Bottom"
    elementPaddingLeft: float
    "Element Padding (mm): Left"
    elementPaddingRight: float
    "Element Padding (mm): Right"
    elementPaddingTop: float
    "Element Padding (mm): Top"
    fillBackground: int
    "Border and Background: Fill background"
    fillColor: int
    "Border and Background: Fill colour"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pageOrderIndex: int
    "Page Order"
    pid_: int
    "ProjectID"
    plotAreaBottom: float
    "Plot Position on Page (mm): Bottom"
    plotAreaLeft: float
    "Plot Position on Page (mm): Left"
    plotAreaRight: float
    "Plot Position on Page (mm): Right"
    plotAreaTop: float
    "Plot Position on Page (mm): Top"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def ChangeStyle(*args): ...

    def DoAutoScale(*args): ...

    def GetAxisX(*args): ...

    def GetAxisY(*args): ...

    def GetComplexData(*args): ...

    def GetLegend(*args): ...

    def GetTitleObject(*args): ...

    def HasReferences(*args): ...

    def SetAutoScaleModeX(*args): ...

    def SetAutoScaleModeY(*args): ...

    def SetScaleX(*args): ...

    def SetScaleY(*args): ...

    def __getattr__(*args): ...


class RelChar(PFGeneral):
    Ipset: float
    "Input Setting"
    Ipsetr: float
    "Input Setting"
    ModFrame: int
    "Enable TCC modifiers"
    ResetT: float
    "Reset Delay"
    Tadder: float
    "Enable TCC modifiers: Time Adder"
    Tpset: float
    "Enable TCC modifiers: Time Dial"
    Tshift: float
    "Time Shift"
    cDisplayName: str
    "Display Name"
    cIpsetU: str
    "Unit"
    cIpsetrU: str
    "Unit"
    cResetT: float
    "Reset Delay"
    cTadder: float
    "Enable TCC modifiers: Time Adder"
    cUserDefIndex: int
    "User defined Index"
    c_sfansi: str
    "ANSI Symbol:"
    c_sfiec: str
    "IEC Symbol:"
    c_type: str
    "Measure Type:"
    calcuse: int
    "Compute Time Using"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cminresptime: float
    "Enable TCC modifiers: Min. Response Time"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpIpset: float
    "Input Setting"
    cpIpsetU: str
    "Unit"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    ctratio: str
    "Current Transformer Ratio"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    idir: int
    "Tripping Direction"
    loc_name: str
    "Name"
    minresptime: float
    "Enable TCC modifiers: Min. Response Time"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pcharac: object
    "Characteristic"
    pid_: int
    "ProjectID"
    resetdis: int
    "Reset Characteristic"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    udeftmax: float
    "Max. Time"
    udeftmin: float
    "Min. Time"
    vtratio: str
    "Voltage Transformer Ratio"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def SetCurve(*args): ...

    def __getattr__(*args): ...


class RelToc(PFGeneral):
    Ipset: float
    "Current Setting"
    Ipsetr: float
    "Current Setting"
    ModFrame: int
    "Enable TCC modifiers"
    ResetT: float
    "Reset Delay"
    Tadder: float
    "Enable TCC modifiers: Time Adder"
    Tpset: float
    "Enable TCC modifiers: Time Dial"
    Trelblock: float
    "Consider Blocking: Release Blocking Time"
    Tshift: float
    "Time Shift"
    cDisplayName: str
    "Display Name"
    cResetT: float
    "Reset Delay"
    cTadder: float
    "Enable TCC modifiers: Time Adder"
    cUserDefIndex: int
    "User defined Index"
    c_sfansi: str
    "ANSI Symbol:"
    c_sfiec: str
    "IEC Symbol:"
    c_type: str
    "Measure Type:"
    calcuse: int
    "Compute Time Using"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cminresptime: float
    "Enable TCC modifiers: Min. Response Time"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpIpset: float
    "Current Setting"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    ctratio: str
    "Current Transformer Ratio"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iacceptblock: int
    "Consider Blocking"
    idir: int
    "Tripping Direction"
    loc_name: str
    "Name"
    minresptime: float
    "Enable TCC modifiers: Min. Response Time"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pcharac: object
    "Characteristic"
    pid_: int
    "ProjectID"
    resetdis: int
    "Reset Characteristic"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    udeftmax: float
    "Max. Time"
    udeftmin: float
    "Min. Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def SetCurve(*args): ...

    def __getattr__(*args): ...


class RelZpol(PFGeneral):
    CompAngle0: float
    "Comp. angle zero seq."
    CompAngle2: float
    "Comp. angle neg. seq."
    IFsub: int
    "Substitute for IF:3I0:3I2"
    PcompLtg: float
    "Mutual Earth Factor: Earth Current Ratio"
    PcompRatio: float
    "Mutual Earth Factor: Earth Current Ratio"
    ReRl: float
    "Earth Factor: Re / Rl"
    RmRl: float
    "Mutual Earth Factor: Rm / Rl"
    Tmem: float
    "Memory Time"
    XeXl: float
    "Earth Factor: Xe / Xl"
    XmXl: float
    "Mutual Earth Factor: Xm / Xl"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    c_auto: int
    "Used Impedance"
    c_k0desc: str
    "Earth factor representation:"
    c_pol: str
    "Polarisation Method:"
    c_type: str
    "Polarisation Unit:"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    complexrepr: int
    "Earth Factor: Show as complex number"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSCompenLine: int
    "Series compensation"
    iSchemeStatus: int
    "Scheme Status"
    iencircmem: int
    "Circular memory"
    irelpol: int
    "Polarisation Method:Self:Cross (Quadrature):Cross (Quad L-L):Positive Sequence:Self, ground compensated"
    k0: float
    "Earth Factor: k0"
    k0m: float
    "Mutual Earth Factor: k0m"
    lineangle: float
    "Earth Factor: Line angle"
    loc_name: str
    "Name"
    memreset: float
    "Memory use reset threshold"
    memuse: float
    "Memory use threshold"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    phik0: float
    "Earth Factor: Angle"
    phik0m: float
    "Mutual Earth Factor: Angle"
    pid_: int
    "ProjectID"
    pol2k: float
    "2nd Polarising factor"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"

    def AssumeCompensationFactor(*args): ...

    def AssumeReRl(*args): ...

    def AssumeXeXl(*args): ...

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ScnFreq(PFGeneral):
    charact: list
    "Charact."
    conscn: int
    "Detection of multiple violations"
    cpHeadFold: object
    "Head folder"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dtscn: float
    "Time step"
    fmax: float
    "Frequency: Maximum limit"
    fmaxgrad: float
    "Frequency gradient: Maximum limit"
    fmin: float
    "Frequency: Minimum limit"
    fmingrad: float
    "Frequency gradient: Minimum limit"
    fnom: float
    "Nominal frequency"
    fold_id: object
    "In folder"
    for_name: str
    "Foreign Key"
    freqlist: str
    "Scan measurement: Nominal frequency"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    htscn: int
    "Activation time: Hours"
    iopt_actscn: int
    "Action"
    iopt_opt: int
    "Scan measurement"
    loc_name: str
    "Name"
    location: int
    "Scan location"
    mtscn: int
    "Activation time: Minutes"
    oid_: int
    "ObjectID"
    outserv: int
    "Ignored"
    pid_: int
    "ProjectID"
    root_id: object
    "Original location"
    simscanobj: object
    "Scan location: User selection"
    stopError: int
    "Action: Stop with error"
    stscn: float
    "Activation time: Seconds"
    tid_: int
    "TimeID"
    timewindowGrad: float
    "Scan measurement: Time window"
    triggerObj: object
    "Action: Trigger"

    def AttributeType(*args): ...

    def GetLimit(*args): ...

    def GetNumberOfViolations(*args): ...

    def GetValue(*args): ...

    def GetVariable(*args): ...

    def GetViolatedElement(*args): ...

    def GetViolationTime(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ScnFrt(PFGeneral):
    cclassnm: str
    "Scan location: Class name"
    charact: list
    "Charact."
    classnm: str
    "Scan location: Class name"
    conscn: int
    "Multiple fault detections"
    conscnH: int
    "Multiple fault detection"
    cpHeadFold: object
    "Head folder"
    curve_tu: list
    "Time"
    curve_tuH: list
    "Time"
    curve_u: list
    "Value"
    curve_uH: list
    "Value"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dtscn: float
    "Time step"
    duration: float
    "Duration"
    durationH: float
    "Duration"
    fold_id: object
    "In folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    htscn: int
    "Activation time: Hours"
    iopt_actscn: int
    "Action"
    iopt_elmTerm: int
    "Variable"
    iopt_printMes: int
    "Display messages"
    iopt_scanType: int
    "Limit curve type"
    iopt_unbFault: int
    "Unbalanced fault detection"
    iopt_unbViol: int
    "Unbalanced violation"
    loc_name: str
    "Name"
    location: int
    "Scan location"
    minDuration: float
    "Multiple fault detections: Minimum duration"
    minDurationH: float
    "Multiple fault detection: Minimum duration"
    mtscn: int
    "Activation time: Minutes"
    oid_: int
    "ObjectID"
    outserv: int
    "Ignored"
    param: list
    "Variable: Variable"
    pid_: int
    "ProjectID"
    reigniThres: float
    "Multiple fault detections: Reignition threshold"
    reigniThresH: float
    "Multiple fault detection: Reignition threshold"
    root_id: object
    "Original location"
    simscanobj: object
    "Scan location: User selection"
    stopError: int
    "Action: Stop with error"
    stscn: float
    "Activation time: Seconds"
    tid_: int
    "TimeID"
    triggerObj: object
    "Action: Trigger"
    unitTxt: str
    "Variable: Unit"
    vinitial: float
    "Activation threshold"
    vinitialH: float
    "Activation threshold"
    voltlist: str
    "Unbalanced network representation: Scanned voltages"

    def AttributeType(*args): ...

    def GetLimit(*args): ...

    def GetNumberOfViolations(*args): ...

    def GetValue(*args): ...

    def GetVariable(*args): ...

    def GetViolatedElement(*args): ...

    def GetViolationTime(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ScnSpeed(PFGeneral):
    charact: list
    "Charact."
    cpHeadFold: object
    "Head folder"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dtscn: float
    "Activation time: Time step"
    fold_id: object
    "In folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    htscn: int
    "Activation time: Hours"
    iopt_actscn: int
    "Action"
    loc_name: str
    "Name"
    location: int
    "Scan location"
    mtscn: int
    "Activation time: Minutes"
    oid_: int
    "ObjectID"
    outserv: int
    "Ignored"
    pid_: int
    "ProjectID"
    root_id: object
    "Original location"
    simscanobj: object
    "Scan location: User selection"
    smax: float
    "Speed settings: Maximum limit"
    smin: float
    "Speed settings: Minimum limit"
    stopError: int
    "Action: Stop with error"
    stscn: float
    "Activation time: Seconds"
    tid_: int
    "TimeID"
    triggerObj: object
    "Action: Trigger"

    def AttributeType(*args): ...

    def GetLimit(*args): ...

    def GetNumberOfViolations(*args): ...

    def GetValue(*args): ...

    def GetVariable(*args): ...

    def GetViolatedElement(*args): ...

    def GetViolationTime(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ScnSync(PFGeneral):
    charact: list
    "Charact."
    cpHeadFold: object
    "Head folder"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dtscn: float
    "Activation time: Time step"
    fold_id: object
    "In folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    htscn: int
    "Activation time: Hours"
    iopt_actscn: int
    "Action"
    loc_name: str
    "Name"
    location: int
    "Scan location"
    mtscn: int
    "Activation time: Minutes"
    oid_: int
    "ObjectID"
    outserv: int
    "Ignored"
    pid_: int
    "ProjectID"
    root_id: object
    "Original location"
    simscanobj: object
    "Scan location: User selection"
    stopError: int
    "Stop with error"
    stscn: float
    "Activation time: Seconds"
    tid_: int
    "TimeID"
    triggerObj: object
    "Action: Trigger"

    def AttributeType(*args): ...

    def GetLimit(*args): ...

    def GetNumberOfViolations(*args): ...

    def GetValue(*args): ...

    def GetVariable(*args): ...

    def GetViolatedElement(*args): ...

    def GetViolationTime(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ScnVar(PFGeneral):
    cclassnm: str
    "Scan location: Class name"
    charact: list
    "Charact."
    classnm: str
    "Scan location: Class name"
    conscn: int
    "Detection of multiple violations"
    cpHeadFold: object
    "Head folder"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dtscn: float
    "Activation time: Time step"
    fold_id: object
    "In folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    htscn: int
    "Activation time: Hours"
    iopt_actscn: int
    "Action"
    loc_name: str
    "Name"
    location: int
    "Scan location"
    maxlim: float
    "Settings: Maximum limit"
    maxunit: str
    "Settings: Maximum limit, unit"
    minlim: float
    "Settings: Minimum limit"
    minunit: str
    "Settings: Minimum limit, unit"
    mtscn: int
    "Activation time: Minutes"
    oid_: int
    "ObjectID"
    oscila: int
    "Continuous scan"
    outserv: int
    "Ignored"
    p_scnobj: object
    "User selection"
    param: list
    "Variable"
    pid_: int
    "ProjectID"
    root_id: object
    "Original location"
    simscanobj: object
    "Scan location: User selection"
    stopError: int
    "Stop with error"
    stscn: float
    "Activation time: Seconds"
    tid_: int
    "TimeID"
    triggerObj: object
    "Action: Trigger"

    def AttributeType(*args): ...

    def GetLimit(*args): ...

    def GetNumberOfViolations(*args): ...

    def GetValue(*args): ...

    def GetVariable(*args): ...

    def GetViolatedElement(*args): ...

    def GetViolationTime(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ScnVolt(PFGeneral):
    charact: list
    "Charact."
    conscn: int
    "Detection of multiple violations"
    cpHeadFold: object
    "Head folder"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dtscn: float
    "Time step"
    fold_id: object
    "In folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    htscn: int
    "Activation time: Hours"
    iopt_actscn: int
    "Action"
    iopt_opt: int
    "Scan measurement"
    iopt_recType: int
    "Recovery thresholds"
    iopt_vl: int
    "Voltage"
    iopt_vr: int
    "Combined threshold for violation and recovery detection"
    loc_name: str
    "Name"
    location: int
    "Scan location"
    mtscn: int
    "Activation time: Minutes"
    oid_: int
    "ObjectID"
    oscila: int
    "Continuous scan"
    outserv: int
    "Ignored"
    pid_: int
    "ProjectID"
    root_id: object
    "Original location"
    simscanobj: object
    "Scan location: User selection"
    stopError: int
    "Stop with error"
    stscn: float
    "Activation time: Seconds"
    tid_: int
    "TimeID"
    timewindowGrad: float
    "Scan measurement: Time window"
    triggerObj: object
    "Action: Trigger"
    tvmax: float
    "Voltage: Duration (max. limit)"
    tvmin: float
    "Voltage: Duration (min. limit)"
    tvrec: float
    "Recovery thresholds: Maximum allowed time below threshold"
    tvrecmax: float
    "Recovery thresholds: Duration below threshold"
    tvrecmin: float
    "Recovery thresholds: Duration above threshold"
    vmax: float
    "Voltage: Maximum limit"
    vmaxGrad: float
    "Voltage gradient: Maximum limit"
    vmin: float
    "Voltage: Minimum limit"
    vminGrad: float
    "Voltage gradient: Minimum limit"
    voltlist: str
    "Unbalanced network representation: Scanned voltages"
    vrec: float
    "Recovery thresholds: Recovery threshold"
    vrecmax: float
    "Recovery thresholds: Recovery threshold"
    vrecmin: float
    "Recovery thresholds: Recovery threshold"

    def AttributeType(*args): ...

    def GetLimit(*args): ...

    def GetNumberOfViolations(*args): ...

    def GetValue(*args): ...

    def GetVariable(*args): ...

    def GetViolatedElement(*args): ...

    def GetViolationTime(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class StoMaint(PFGeneral):
    Duration: list
    "Duration"
    Elms: list
    "Name"
    Start: int
    "Begin"
    StartTime: list
    "Start Time"
    cEnd: str
    "Time Range: End"
    cStart: str
    "Time Range: Begin"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_def: str
    "Elements"
    iopt_in: str
    "Input Mode"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Ignore Schedule"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def SetElms(*args): ...

    def __getattr__(*args): ...


class TypAsmo(PFGeneral):
    Ibase: float
    "Base current"
    J: float
    "Moment of inertia"
    Tbase: float
    "Base torque"
    Tcold: float
    "Stall time: Cold"
    Thot: float
    "Stall time: Hot"
    Tinrush: float
    "Inrush peak current: Max. time"
    a: float
    "Turns ratio aux./main"
    aiazn: float
    "Consider transient parameter: Locked rotor current (Ilr/In)"
    aiaznshc: float
    "Impedance input: Locked rotor current (Ilr/In)"
    amazn: float
    "Locked rotor torque"
    amkzn: float
    "Torque at stalling point"
    amstl: float
    "Torque at saddle point"
    anend: float
    "Rated speed"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    aslkp: float
    "Slip at stalling point"
    asstl: float
    "Slip at saddle point"
    cansitp: str
    "ANSI type"
    charact: list
    "Charact."
    chp: float
    "Power"
    chr_name: str
    "Characteristic Name"
    coazn: float
    "cos(phi) locked rotor"
    cosn: float
    "Rated power factor"
    cpHeadFold: object
    "Head Folder"
    cr: float
    "Capacitor-run capacitance"
    crmshc: float
    "Impedances: Resistance Rm"
    crrotshc: float
    "Impedances: Rotor resistance Rr"
    crstrshc: float
    "Impedances: Stator resistance Rs"
    cs: float
    "Capacitor-start capacitance"
    ctdc: float
    "Time constants: Tdc"
    ctmss: float
    "Time constants: Tm"
    cxdssshc: float
    "Impedances: Reactance Xm"
    cxrotshc: float
    "Impedances: Rotor reactance Xr"
    cxstrshc: float
    "Impedances: Stator reactance Xs"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    effic: float
    "Efficiency at rated operation"
    fcharlss: object
    "Frequency dependence of: Inductance L''(f)"
    fcharrstr: object
    "Frequency dependence of: Stator resistance Rs(f)"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frequ: float
    "Nominal frequency"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    i_1pModel: int
    "Startup model:&0&Split-phase:&1&Capacitor-start:&2&Capacitor-start, capacitor-run"
    i_cage: int
    "Rotor"
    i_cdisp: int
    "Operating cage/Rotor data: Consider current displacement (squirrel cage rotor)"
    i_freqVar: int
    "Effect of frequency variation (only for Doubly Fed Induction Machine)"
    i_mode: int
    "Input mode"
    i_optpn: int
    "Power rating"
    i_sat: int
    "Main flux saturation:&0&No saturation:&1&Quadratic (SG10/SG12):&2&Exponential (SG10/SG12):&3&Tabular input"
    i_trans: int
    "Consider transient parameter"
    iansitp: int
    "ANSI type:Auto detection:> 1000 at <= 1800(1500):> 250 at 3600/3000:50-1000 at <=1800(1500):50-250 at 3600(3000):< 50 (Std C37):< 50 (Std 141)"
    iinrush: float
    "Inrush peak current: Ratio Ip/In"
    ishcmax: float
    "Maximum subtransient short-circuit current"
    islp: float
    "Current"
    istt: int
    "Status of ESB Calculation"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    mslp: float
    "Torque"
    n_cdisp: int
    "Order of R-L approximation"
    nphase: int
    "No. of phases:1:3"
    nppol: int
    "No of pole pairs"
    nslty: int
    "Connection:D:Y:YN"
    oid_: int
    "ObjectID"
    pgn: float
    "Power rating: Rated mechanical power"
    pid_: int
    "ProjectID"
    puSI: int
    "Current/Torque values in:p.u.:S.I."
    r0: float
    "Operating cage/Rotor data: Resistance RrA1"
    r1: float
    "Operating cage/Rotor data: Resistance RrA2"
    root_id: object
    "Original Location"
    rr: float
    "Capacitor-run resistance"
    rrs1: float
    "Slip dependent part of RrA at slip=1"
    rrsn: float
    "Slip dependent part of RrA at rated slip"
    rrtrA: float
    "Operating cage/Rotor data: Rotor resistance RrA"
    rrtrA0: float
    "Operating cage/Rotor data: Resistance RrA0"
    rrtrB: float
    "Starting cage: Rotor resistance RrB"
    rs: float
    "Capacitor-start resistance"
    rstr: float
    "Stator resistance Rs"
    rstr_aux: float
    "Stator res. aux. winding"
    rstrshc: float
    "Impedance input: Stator resistance Rs"
    rtox: float
    "Consider transient parameter: R/X locked rotor"
    rtoxshc: float
    "Impedance input: R/X locked rotor"
    rzero: float
    "Zero sequence: Resistance"
    satIm: list
    "Saturation parameter: No load current"
    satSmoothFac: float
    "Saturation parameter: Curve smoothing factor"
    satV: list
    "Saturation parameter: Term. voltage"
    sg10: float
    "Saturation parameter: SG10"
    sg12: float
    "Saturation parameter: SG12"
    sgn: float
    "Power rating: Rated apparent power"
    slp: float
    "Slip"
    tab_ISI: list
    "Current"
    tab_Ipu: list
    "Current"
    tab_TSI: list
    "Torque"
    tab_Tpu: list
    "Torque"
    tab_eff: list
    "Efficiency"
    tab_pf: list
    "Power Factor"
    tab_w: list
    "Speed"
    tag: float
    "Acceleration time constant"
    tid_: int
    "TimeID"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"
    ugn: float
    "Rated voltage"
    x0: float
    "Operating cage/Rotor data: Reactance XrA1"
    x1: float
    "Operating cage/Rotor data: Reactance XrA2"
    xdssshc: float
    "Impedance input: Locked rotor reactance"
    xm: float
    "Mag. reactance Xm"
    xmrtr: float
    "Rotor leakage reac. Xrm"
    xrs1: float
    "Slip dependent part of XrA at slip=1"
    xrsn: float
    "Slip dependent part of XrA at rated slip"
    xrtrA: float
    "Operating cage/Rotor data: Rotor reactance XrA"
    xrtrA0: float
    "Operating cage/Rotor data: Reactance XrA0"
    xrtrB: float
    "Starting cage: Rotor reactance XrB"
    xstr: float
    "Stator reactance Xs"
    xstr_aux: float
    "Stator reac. aux. winding"
    xtorshc: float
    "Impedance input: X/R locked rotor"
    xzero: float
    "Zero sequence: Reactance"

    def AttributeType(*args): ...

    def CalcElParams(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class TypCtcore(PFGeneral):
    Ithr: float
    "Rated short-time current (1s)"
    Snom: list
    "Snom"
    Vmax: list
    "Vmax"
    Zb: list
    "Zb"
    aclimit: list
    "Accuracy limitfactor"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    cratios: list
    "Resulting ratio"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_sat: str
    "Accuracy parameters according to"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    prirat: float
    "Current ratings: Primary"
    raclass: list
    "Accuracy class"
    ratios: list
    "Ratio"
    root_id: object
    "Original Location"
    secrat: float
    "Current ratings: Secondary"
    tid_: int
    "TimeID"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"

    def AddRatio(*args): ...

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def RemoveRatio(*args): ...

    def RemoveRatioByIndex(*args): ...

    def __getattr__(*args): ...


class TypLne(PFGeneral):
    Ices: float
    "Parameters per Length Zero Sequence: Earth-Fault Current"
    InomAir: float
    "Rated Current (in air)"
    Ithr: float
    "Rated Short-Time (1s) Current (Conductor)"
    alpha: float
    "Parameters per Length 1,2-Sequence: Temperature Coefficient"
    aohl_: str
    "Cable / OHL"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bett: float
    "Operating Temp."
    bline: float
    "Parameters per Length 1,2-Sequence: Susceptance B'"
    bline0: float
    "Parameters per Length Zero Sequence: Susceptance B0'"
    bnline: float
    "Parameters per Length, Neutral: Susceptance Bn'"
    bpnline: float
    "Parameters per Length, Phase-Neutral Coupling: Susceptance Bpn'"
    carmour: int
    "Cable Design Parameter With Sheath: Armoured Cable"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cline: float
    "Parameters per Length 1,2-Sequence: Capacitance C'"
    cline0: float
    "Parameters per Length Zero Sequence: Capacitance C0'"
    cnline: float
    "Parameters per Length, Neutral: Capacitance Cn'"
    cohl_: int
    "Cable / OHL:Cable:Overhead Line"
    cpHeadFold: object
    "Head Folder"
    cpnline: float
    "Parameters per Length, Phase-Neutral Coupling: Capacitance Cpn'"
    cscreen: int
    "Cable Design Parameter With Sheath: Radial Cable Screen"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fcharC0: object
    "Frequency Dependency of Zero-Sequence Capacitance: C0'(f)"
    fcharC1: object
    "Frequency Dependency of Pos.-Sequence Capacitance: C1'(f)"
    fcharL0: object
    "Frequency Dependencies of Zero-Sequence Impedance: L0'(f)"
    fcharL1: object
    "Frequency Dependencies of Pos.-Sequence Impedance: L1'(f)"
    fcharR0: object
    "Frequency Dependencies of Zero-Sequence Impedance: R0'(AC)(f)"
    fcharR1: object
    "Frequency Dependencies of Pos.-Sequence Impedance: R1'(AC)(f)"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    fr_sheath: int
    "Cable Design Parameter: With Sheath"
    frnom: float
    "Nominal Frequency"
    gline: float
    "Parameters per Length 1,2-Sequence: Conductance G'"
    gline0: float
    "Parameters per Length Zero Sequence: Conductance G0'"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    imiso: int
    "Cable Design Parameter: Insulation Material:PVC:XLPE:Mineral:Paper:EPR"
    iopt_cnd: str
    "Cable Design Parameter: Cable Cores"
    iopt_inp: str
    "Input Option Temperature Dependency for LDF, RMS and EMT calculations"
    iopt_inpshc: str
    "Input Option Temperature Dependency for Complete SHC only"
    lcost: float
    "Line Cost"
    lline: float
    "Parameters per Length 1,2-Sequence: Inductance L'"
    lline0: float
    "Parameters per Length Zero Sequence: Inductance L0'"
    lnline: float
    "Parameters per Length, Neutral: Inductance Ln'"
    loc_name: str
    "Name"
    lodln: str
    "Type of Load"
    lpnline: float
    "Parameters per Length, Phase-Neutral Coupling: Inductance Lpn'"
    manuf: str
    "Manufacturer"
    miso: str
    "Insulation Material"
    mlei: str
    "Parameters per Length 1,2-Sequence: Conductor Material"
    nlnph: int
    "Phases:1:2:3"
    nneutral: int
    "Number of Neutrals:0:1"
    oid_: int
    "ObjectID"
    pStoch: object
    "Stochastic model"
    picln: float
    "Inrush Peak Current: Ratio Ip/In"
    pid_: int
    "ProjectID"
    pitln: float
    "Inrush Peak Current: Maximum Time"
    qurs: float
    "Nominal Cross Section"
    rectancond: int
    "Rectangular Conductor"
    rlin1: float
    "Loop Resistance  (sev)"
    rline: float
    "Parameters per Length 1,2-Sequence: AC-Resistance R'(20C)"
    rline0: float
    "Parameters per Length Zero Sequence: AC-Resistance R0'"
    rline_tmax: float
    "Parameters per Length 1,2-Sequence: AC-Resistance R' at max. operating temperature"
    rnline: float
    "Parameters per Length, Neutral: AC-Resistance Rn'"
    root_id: object
    "Original Location"
    rpnline: float
    "Parameters per Length, Phase-Neutral Coupling: AC-Resistance Rpn'"
    rtemp: float
    "Max. End Temperature"
    shins: int
    "Cable Design Parameter With Sheath: Sheath Insulation Material"
    shtyp: int
    "Cable Design Parameter With Sheath: Sheath Type:Non-Metallic:Metallic"
    side_b: float
    "Rectangular Conductor: Height (b)"
    side_d: float
    "Rectangular Conductor: Width (d)"
    slin1: float
    "Rated Current (1.)"
    slin2: float
    "Load Current (*In)"
    sline: float
    "Rated Current"
    systp: int
    "System Type:AC:DC"
    tid_: int
    "TimeID"
    tline: float
    "Parameters per Length 1,2-Sequence: Ins. Factor"
    tline0: float
    "Parameters per Length Zero Sequence: Ins. Factor"
    tmax: float
    "Parameters per Length 1,2-Sequence: Max. Operating Temperature"
    touchExp: int
    "Cable Design Parameter: Exposed to touch"
    twcln: float
    "Ratio It/In"
    twtln: float
    "Maximum Time"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"
    uline: float
    "Rated Voltage"
    xlin1: float
    "Loop Reactance (sev)"
    xline: float
    "Parameters per Length 1,2-Sequence: Reactance X'"
    xline0: float
    "Parameters per Length Zero Sequence: Reactance X0'"
    xnline: float
    "Parameters per Length, Neutral: Reactance Xn'"
    xpnline: float
    "Parameters per Length, Phase-Neutral Coupling: Reactance Xpn'"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def IsCable(*args): ...

    def __getattr__(*args): ...


class TypMdl(PFGeneral):
    aCategory: str
    "Category"
    algorithm: list
    "Algorithm after first tick"
    annotation: list
    "Annotation"
    author: list
    "Author"
    autoCompCheckSum: list
    "Automatic compilation checksum"
    blockAnnot: list
    "Annotation"
    blockDesc: list
    "Description"
    blockName: list
    "Name"
    blockParams: list
    "Parameters"
    blockTypeRef: list
    "Type"
    cCategory: str
    "Category"
    cCheckSum: list
    "Checksum"
    cCheckSumFMU: list
    "DLL"
    cGlobalAdditionalDataHash: list
    "Global additional data hash"
    cGlobalAnnotationHash: list
    "Global annotation hash"
    cGlobalAutoCompHash: list
    "Global automatic compilation hash"
    cGlobalBlockParamHash: list
    "Global block parametrisation hash"
    cGlobalEquationHash: list
    "Global equations' hash"
    cGlobalParameterHash: list
    "Global parametrisation hash"
    cauthor: list
    "Author"
    ccopyright: list
    "Copyright"
    cdesc: list
    "Description"
    cfilePath: str
    "Compiled model: File path"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cinputAll: list
    "Inputs"
    cinputDesc: list
    "Description"
    cinputMax: list
    "Max"
    cinputMin: list
    "Min"
    cinputName: list
    "Name"
    cinputSize: list
    "Size(s)"
    cinputStart: list
    "Start"
    cinputType: list
    "Base Type"
    cinputUnit: list
    "Unit"
    cinputVariability: list
    "Variability"
    cinterDesc: list
    "Description"
    cinterMax: list
    "Max"
    cinterMin: list
    "Min"
    cinterName: list
    "Name"
    cinterSize: list
    "Size(s)"
    cinterStart: list
    "Start"
    cinterType: list
    "Base Type"
    cinterUnit: list
    "Unit"
    configScript: object
    "Initialisation: Configuration Script"
    connectAnnot: list
    "Annotation"
    connectFirstBlock: list
    "First model"
    connectFirstConnector: list
    "First connector"
    connectSecondBlock: list
    "Second model"
    connectSecondConnector: list
    "Second connector"
    contents: list
    "Contents"
    copyright: list
    "Copyright"
    coutputAll: list
    "Outputs"
    coutputDesc: list
    "Description"
    coutputMax: list
    "Max"
    coutputMin: list
    "Min"
    coutputName: list
    "Name"
    coutputSize: list
    "Size(s)"
    coutputStart: list
    "Start"
    coutputType: list
    "Base Type"
    coutputUnit: list
    "Unit"
    coutputVariability: list
    "Variability"
    cpHeadFold: object
    "Head Folder"
    cparamAll: list
    "Parameters"
    cparamDefault: list
    "Default"
    cparamDesc: list
    "Description"
    cparamMax: list
    "Max"
    cparamMin: list
    "Min"
    cparamName: list
    "Name"
    cparamSize: list
    "Size(s)"
    cparamType: list
    "Base Type"
    cparamUnit: list
    "Unit"
    cstateDesc: list
    "Description"
    cstateMax: list
    "Max"
    cstateMin: list
    "Min"
    cstateName: list
    "Name"
    cstateSize: list
    "Size(s)"
    cstateStart: list
    "Start"
    cstateType: list
    "Base Type"
    cstateUnit: list
    "Unit"
    ctypemetadata_version: list
    "Version"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    equation: list
    "Equations"
    filePath: str
    "File path"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    i_partinc: int
    "Partial initialisation in case of deadlock"
    initAlgorithm: list
    "Algorithm at first tick"
    initEquation: list
    "Initial equations"
    inputAnnot: list
    "Annotation"
    inputDesc: list
    "Description"
    inputMax: list
    "Max"
    inputMin: list
    "Min"
    inputName: list
    "Name"
    inputSize: list
    "Size(s)"
    inputStart: list
    "Start"
    inputType: list
    "Base Type"
    inputUnit: list
    "Unit"
    inputVariability: list
    "Variability"
    interDesc: list
    "Description"
    interMax: list
    "Max"
    interMin: list
    "Min"
    interName: list
    "Name"
    interSize: list
    "Size(s)"
    interStart: list
    "Start"
    interType: list
    "Base Type"
    interUnit: list
    "Unit"
    isEncrypted: int
    "Encrypted model flag"
    level: int
    "Model level"
    loc_name: str
    "Name"
    logFmuNames: list
    "Names"
    logFmuVals: list
    "FMU: On/Off"
    modMethod: int
    "Method:&0&Hybrid Method:&1&Clocked"
    modelType: int
    "Compiled model"
    noArrayFmu: int
    "Do not consider arrays"
    oid_: int
    "ObjectID"
    outputAnnot: list
    "Annotation"
    outputDesc: list
    "Description"
    outputMax: list
    "Max"
    outputMin: list
    "Min"
    outputName: list
    "Name"
    outputSize: list
    "Size(s)"
    outputStart: list
    "Start"
    outputType: list
    "Base Type"
    outputUnit: list
    "Unit"
    outputVariability: list
    "Variability"
    paramDefault: list
    "Default"
    paramDesc: list
    "Description"
    paramMax: list
    "Max"
    paramMin: list
    "Min"
    paramName: list
    "Name"
    paramSize: list
    "Size(s)"
    paramType: list
    "Base Type"
    paramUnit: list
    "Unit"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    showDef: int
    "Language specification: Show default/start values of parameters/variables in Variable Declarations"
    showMinMax: int
    "Language specification: Show minimum/maximum values of variables in Variable Declarations"
    singleInstanceType: int
    "Single-instance type"
    stateDesc: list
    "Description"
    stateMax: list
    "Max"
    stateMin: list
    "Min"
    stateName: list
    "Name"
    stateSize: list
    "Size(s)"
    stateStart: list
    "Start"
    stateType: list
    "Base Type"
    stateUnit: list
    "Unit"
    tid_: int
    "TimeID"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"

    def AttributeType(*args): ...

    def Check(*args): ...

    def Compile(*args): ...

    def HasReferences(*args): ...

    def Pack(*args): ...

    def __getattr__(*args): ...


class TypQdsl(PFGeneral):
    author: str
    "Author"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    company: str
    "Company"
    cpHeadFold: object
    "Head Folder"
    csigVarName: list
    "Variable name"
    ctrlLdf: list
    "Control actions for Load Flow"
    ctrlQds: list
    "Control actions for Quasi-Dynamic Simulation"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    display3rdParty: list
    "Third Party Licence"
    displayModule: list
    "Third Party Licence (will only be applied after encryption!): Module"
    eqLdf: list
    "Load flow equations"
    eqQds: list
    "Quasi-dynamic equations"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    init: list
    "Initialisation"
    isLinearModel: int
    "Linear model"
    loc_name: str
    "Name"
    modifytime: int
    "Last Modified"
    objDesc: list
    "Description"
    objName: list
    "Name"
    objType: list
    "Usage"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    resDesc: list
    "Description"
    resName: list
    "Name"
    resUnit: list
    "Unit"
    root_id: object
    "Original Location"
    shortDesc: str
    "Short Description"
    sigBusName: list
    "Bus/Phase name"
    sigClassName: list
    "Class name"
    sigName: list
    "Name"
    sigType: list
    "Usage"
    sigVarName: list
    "Variable name"
    tid_: int
    "TimeID"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"
    varDesc: list
    "Description"
    varName: list
    "Name"
    varType: list
    "Variable type"
    varUnit: list
    "Unit"
    version: str
    "Version"
    xDesc: list
    "Long Description"
    xNotes: list
    "Release Notes"

    def AttributeType(*args): ...

    def Encrypt(*args): ...

    def HasReferences(*args): ...

    def IsEncrypted(*args): ...

    def ResetThirdPartyModule(*args): ...

    def SetThirdPartyModule(*args): ...

    def __getattr__(*args): ...


class TypTr2(PFGeneral):
    Lwidth: float
    "Magnetising Reactance Hysteresis: Loop width"
    aFrolich: float
    "Frolich equation coefficient a"
    ansiclass: str
    "Class:OA:FA:FOA"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bFrolich: float
    "Frolich equation coefficient b"
    bm1: float
    "Frequency dependencies of magnetising admittance: 1/lm"
    cFrolich: float
    "Frolich equation coefficient c"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cknee: float
    "Knee Current"
    cpHeadFold: object
    "Head Folder"
    curmg: float
    "Magnetising Impedance: No Load Current"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dphitap: float
    "Tap Changer 1: Additional Angle per Tap"
    dphitap2: float
    "Tap Changer 2: Additional Angle per Tap"
    dutap: float
    "Tap Changer 1: Additional Voltage per Tap"
    dutap2: float
    "Tap Changer 2: Additional Voltage per Tap"
    eddypc: float
    "Data for K-factor, Factor-K, FHL and skin effect: Ratio: winding eddy current-/copper losses"
    fcharbm: object
    "Frequency dependencies of magnetising admittance: 1/lm(f)"
    fchargm: object
    "Frequency dependencies of magnetising admittance: gm(f)"
    fcharl0: object
    "Frequency dependencies of zero sequence impedance: l0(f)"
    fcharl1: object
    "Frequency dependencies of positive sequence impedance: l1(f)"
    fcharr0: object
    "Frequency dependencies of zero sequence impedance: r0(f)"
    fcharr1: object
    "Frequency dependencies of positive sequence impedance: r1(f)"
    fdtr2r: str
    "Internal"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frnom: float
    "Nominal Frequency"
    gm1: float
    "Frequency dependencies of magnetising admittance: gm"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iFinalSlope: int
    "Magnetising Reactance: Set final slope (peak values)"
    iFit: int
    "Magnetising Reactance: Data fitting:Piecewise linear:Frolich:Modified Frolich"
    iHyster: int
    "Magnetising Reactance Hysteresis: Model:None:History Independent"
    iIntDelta: int
    "Vector Group: Internal Delta Winding"
    iIntPola: int
    "Magnetising Reactance: Interpolation:spline:piecewise linear"
    iInterPol: int
    "Magnetising Reactance: Interpolation:spline:piecewise linear"
    iLimb: int
    "Magnetising Reactance: Core:&3&3 Limb:&5&5 Limb"
    iSchemeStatus: int
    "Scheme Status"
    iTapLoading: int
    "Tap dependent rating: Configuration:No dependency (constant current):Full Capacity Below Normal (FCBN):Reduced Capacity Below Normal (RCBN)"
    it0mt: int
    "Type"
    itapch: int
    "Tap Changer 1"
    itapch2: int
    "Tap Changer 2"
    itapzdep: int
    "Tap dependent impedance"
    itratioadpt: int
    "Transformer Ratio Adaptation"
    itrdl: float
    "Distribution of Leakage Reactances (p.u.): x,Pos.Seq. HV-Side"
    itrdl_lv: float
    "Distribution of Leakage Reactances (p.u.): x,Pos.Seq. LV-Side"
    itrdr: float
    "Distribution of Leakage Resistances (p.u.): r,Pos.Seq. HV-Side"
    itrdr_lv: float
    "Distribution of Leakage Resistances (p.u.): r,Pos.Seq. LV-Side"
    itrldf: int
    "Magnetising Reactance: Type"
    itrmt: int
    "Magnetising Reactance: Type"
    itrtype: int
    "Transformer Type:Liquid-Immersed:Dry-Type"
    ksat: int
    "Magnetising Reactance: Saturation Exponent"
    l0pu: float
    "Frequency dependencies of zero sequence impedance: Inductance l0"
    l1pu: float
    "Frequency dependencies of positive sequence impedance: Inductance l1"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    mseFrolich: float
    "Frolich equation, mean squared error"
    nntap0: int
    "Tap Changer 1: Neutral Position"
    nntap02: int
    "Tap Changer 2: Neutral Position"
    nt2ag: float
    "Vector Group: Phase Shift"
    nt2ph: int
    "Technology"
    ntpmn: int
    "Tap Changer 1: Minimum Position"
    ntpmn2: int
    "Tap Changer 2: Minimum Position"
    ntpmx: int
    "Tap Changer 1: Maximum Position"
    ntpmx2: int
    "Tap Changer 2: Maximum Position"
    oid_: int
    "ObjectID"
    oltc: int
    "On-load Tap Changer"
    oltc2: int
    "On-load Tap Changer 2"
    pStoch: object
    "Stochastic model"
    pT: str
    "Voltage Range"
    pcutmn: float
    "Tap dependent impedance: Pcu (min. tap)"
    pcutmx: float
    "Tap dependent impedance: Pcu (max. tap)"
    pcutr: float
    "Positive Sequence Impedance: Copper Losses"
    pfe: float
    "Magnetising Impedance: No Load Losses"
    phitr: float
    "Tap Changer 1: Phase of du"
    phitr2: float
    "Tap Changer 2: Phase of du"
    pict1: float
    "Inrush Peak Current: Ratio Ip/In (1)"
    pict2: float
    "Inrush Peak Current: Ratio Ip/In (2)"
    pid_: int
    "ProjectID"
    pitt1: float
    "Inrush Peak Current: Max. Time (1)"
    pitt2: float
    "Inrush Peak Current: Max. Time (2)"
    psi0: float
    "Magnetising Reactance: Knee Flux"
    r0delta: float
    "Delta Winding, r0"
    r0pu: float
    "Zero Sequence Impedance: Resistance r0"
    r0pu_hlo: float
    "Zero Sequence Impedance: HV-Resistance r0 (LV open)"
    r0pu_hls: float
    "Zero Sequence Impedance: HV-Resistance r0 (LV short-circuit)"
    r0pu_lho: float
    "Zero Sequence Impedance: LV-Resistance r0 (HV open)"
    r0putmn: float
    "Tap dependent impedance: r0 (min. tap)"
    r0putmx: float
    "Tap dependent impedance: r0 (max. tap)"
    r1pu: float
    "Positive Sequence Impedance: Resistance r1"
    r1putmn: float
    "Tap dependent impedance: r1 (min. tap)"
    r1putmx: float
    "Tap dependent impedance: r1 (max. tap)"
    root_id: object
    "Original Location"
    rtox0_n: float
    "Zero Sequence Magnetising Impedance: Mag. R/X"
    satcue: list
    "Magnetising Reactance: Current (RMS)"
    satcur: list
    "Magnetising Reactance: Current (peak)"
    satflux: list
    "Magnetising Reactance: Flux (peak)"
    satvol: list
    "Magnetising Reactance: Voltage (RMS)"
    smoothf: float
    "Magnetising Reactance: Smoothing Factor"
    smoothfac: float
    "Magnetising Reactance: Smoothing Factor"
    strn: float
    "Rated Power"
    strnfc: float
    "Rated Power (forced cooling)"
    tap_side: int
    "Tap Changer 1: at Side:HV:LV"
    tap_side2: int
    "Tap Changer 2: at Side:HV:LV"
    tapchtype: int
    "Tap Changer 1: Type:Ratio/Asym. Phase Shifter:Ideal Phase Shifter:Sym. Phase Shifter"
    tapchtype2: int
    "Tap Changer 2: Type:Ratio/Asym. Phase Shifter:Ideal Phase Shifter"
    tid_: int
    "TimeID"
    tr2cn_h: str
    "Vector Group: HV-Side:Y :YN:Z :ZN:D"
    tr2cn_l: str
    "Vector Group: LV-Side:Y :YN:Z :ZN:D"
    twct2: float
    "Ratio It/In"
    twtt2: float
    "Max. Time"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"
    uk0_hlo: float
    "Zero Sequence Impedance: HV-SHC-Voltage uk0 (LV open)"
    uk0_hls: float
    "Zero Sequence Impedance: HV-SHC-Voltage uk0 (LV short-circuit)"
    uk0_lho: float
    "Zero Sequence Impedance: LV-SHC-Voltage uk0 (HV open)"
    uk0delta: float
    "Delta Winding, uk0"
    uk0rtmn: float
    "Tap dependent impedance: Re(uk0) (min. tap)"
    uk0rtmx: float
    "Tap dependent impedance: Re(uk0) (max. tap)"
    uk0tmn: float
    "Tap dependent impedance: uk0 (min. tap)"
    uk0tmx: float
    "Tap dependent impedance: uk0 (max. tap)"
    uk0tr: float
    "Zero Sequence Impedance: Short-Circuit Voltage uk0"
    ukrtmn: float
    "Tap dependent impedance: Re(uk) (min. tap)"
    ukrtmx: float
    "Tap dependent impedance: Re(uk) (max. tap)"
    uktmn: float
    "Tap dependent impedance: uk (min. tap)"
    uktmx: float
    "Tap dependent impedance: uk (max. tap)"
    uktr: float
    "Positive Sequence Impedance: Short-Circuit Voltage uk"
    uktrr: float
    "Positive Sequence Impedance: SHC-Voltage (Re(uk)) ukr"
    ur0_hlo: float
    "Zero Sequence Impedance: HV-SHC-Voltage Re(uk0) (LV open)"
    ur0_hls: float
    "Zero Sequence Impedance: HV-SHC-Voltage Re(uk0) (LV short-circuit)"
    ur0_lho: float
    "Zero Sequence Impedance: LV-SHC-Voltage Re(uk0) (HV open)"
    ur0delta: float
    "Delta Winding, Re(uk0)"
    ur0tr: float
    "Zero Sequence Impedance: SHC-Voltage (Re(uk0)) uk0r"
    utrn_h: float
    "Rated Voltage: HV-Side"
    utrn_l: float
    "Rated Voltage: LV-Side"
    vecgrp: str
    "Vector Group: Name"
    x0delta: float
    "Delta Winding, x0"
    x0pu: float
    "Zero Sequence Impedance: Reactance x0"
    x0pu_hlo: float
    "Zero Sequence Impedance: HV-Reactance x0 (LV open)"
    x0pu_hls: float
    "Zero Sequence Impedance: HV-Reactance x0 (LV short-circuit)"
    x0pu_lho: float
    "Zero Sequence Impedance: LV-Reactance x0 (HV open)"
    x0putmn: float
    "Tap dependent impedance: x0 (min. tap)"
    x0putmx: float
    "Tap dependent impedance: x0 (max. tap)"
    x0tor0: float
    "Zero Sequence Impedance: Ratio X0/R0"
    x0tor0delta: float
    "Delta Winding, X0/R0"
    x0tor0tmn: float
    "Tap dependent impedance: X0/R0 (min. tap)"
    x0tor0tmx: float
    "Tap dependent impedance: X0/R0 (max. tap)"
    x1pu: float
    "Positive Sequence Impedance: Reactance x1"
    x1putmn: float
    "Tap dependent impedance: x1 (min. tap)"
    x1putmx: float
    "Tap dependent impedance: x1 (max. tap)"
    xmair: float
    "Magnetising Reactance: Saturated Reactance"
    xmlin: float
    "Magnetising Reactance: Linear Reactance"
    xsatFrolich: float
    "Frolich equation saturated reactance (p.u.)"
    xtor: float
    "Positive Sequence Impedance: Ratio X/R"
    xtortmn: float
    "Tap dependent impedance: X/R (min. tap)"
    xtortmx: float
    "Tap dependent impedance: X/R (max. tap)"
    xtr0_hlo: float
    "Zero Sequence Impedance: HV-Ratio X0/R0 (LV open)"
    xtr0_hls: float
    "Zero Sequence Impedance: HV-Ratio X0/R0 (LV short-circuit)"
    xtr0_lho: float
    "Zero Sequence Impedance: LV-Ratio X0/R0 (HV open)"
    zx0hl_h: float
    "Distribution of Zero Sequ. Leakage-Impedances: z, Zero Sequ. HV-Side"
    zx0hl_l: float
    "Distribution of Zero Sequ. Leakage-Impedances: z, Zero Sequ. LV-Side"
    zx0hl_n: float
    "Zero Sequence Magnetising Impedance: Mag. Impedance/uk0"

    def AttributeType(*args): ...

    def GetZeroSequenceHVLVT(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class VisBdia(PFGeneral):
    AutoBrs: int
    "Automatic: Brush"
    AutoCol: int
    "Automatic: Colour"
    Brush: list
    "Brush Style"
    Color: list
    "Colour"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    ResFile: list
    "Result File"
    Stack: float
    "Priority Level"
    Utils: list
    "Contents"
    aleg: str
    "User Label"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    ileg: int
    "Label"
    ishort: int
    "Standard Legend uses"
    limits: str
    "Show"
    loc_name: str
    "Name"
    nupd: int
    "Number of values between update"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pObjs: list
    "Element"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sObjs: list
    "Object"
    shw_leg: int
    "Show Legend"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    userdesc: list
    "Variable Description"
    xvar: str
    "Variable: x"
    y_fit: int
    "Scale: Adapt Scale"
    y_map: int
    "Scale: Scale"
    y_max: float
    "Scale Limits: Maximum"
    y_min: float
    "Scale Limits: Minimum"
    yvar: str
    "Variable: y"

    def AddObjs(*args): ...

    def AddResObjs(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def HasReferences(*args): ...

    def SetScaleY(*args): ...

    def SetXVariable(*args): ...

    def SetYVariable(*args): ...

    def __getattr__(*args): ...


class VisDraw(PFGeneral):
    AutoCol: int
    "Automatic: Colour"
    AutoStl: int
    "Automatic: Line Style"
    AutoWdt: int
    "Automatic: Line Width"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    ResFile: list
    "Result File"
    Stack: float
    "Priority Level"
    Utils: list
    "Contents"
    aleg: str
    "Frame: User Label"
    autos: int
    "Auto Scale"
    cIdx: list
    "Curve index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    distance: int
    "Distance"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gColor: list
    "Colour"
    gObjs: list
    "Element"
    gStyle: list
    "Style"
    gWidth: list
    "Width"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAll: int
    "Range of Results: Complete"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    icircles: int
    "Representation of Coordinates"
    ileg: int
    "Frame: Label"
    impResName: str
    "Sub-Result Name"
    ishort: int
    "Standard Legend uses"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pPath: object
    "Path"
    pid_: int
    "ProjectID"
    result: object
    "Branch impedance calculation: Results"
    root_id: object
    "Original Location"
    scale: list
    "Scale"
    shownResult: list
    "Branch impedance calculation: Displayed"
    shw_arr: int
    "Show direction arrows for curves"
    shw_leg: int
    "Show Legend"
    tickDist: int
    "Distance between Ticks"
    tid_: int
    "TimeID"
    tmax: float
    "Range of Results: Maximum"
    tmin: float
    "Range of Results: Minimum"
    typ_id: object
    "Type"
    unit: list
    "Unit"
    userdesc: list
    "Description"
    vColor: list
    "Colour"
    vObjs: list
    "Element"
    vStyle: list
    "Style"
    vVarX: list
    "x-Variable"
    vVarY: list
    "y-Variable"
    vWidth: list
    "Width"
    x_end: int
    "x-Max."
    x_start: int
    "x-Min."
    xvar: list
    "x-Variable"
    y_end: int
    "y-Max."
    y_start: int
    "y-Min."
    yvar: list
    "y-Variable"

    def AddRelay(*args): ...

    def AddRelays(*args): ...

    def AttributeType(*args): ...

    def CentreOrigin(*args): ...

    def Clear(*args): ...

    def DoAutoScaleOnAll(*args): ...

    def DoAutoScaleOnCharacteristics(*args): ...

    def DoAutoScaleOnImpedances(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class VisHrm(PFGeneral):
    AutoCol: int
    "Automatic: Colour"
    AutoStl: int
    "Automatic: Line Style"
    AutoWdt: int
    "Automatic: Line Width"
    Color: list
    "Colour"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Mag: list
    "Magnitude"
    Phi: list
    "Angle"
    Position: list
    "Position"
    ResFile: list
    "Result File"
    Stack: float
    "Priority Level"
    Style: list
    "Style"
    Utils: list
    "Contents"
    Width: list
    "Width"
    aleg: str
    "User Label"
    auto_xscl: int
    "Scale: Auto Scale"
    auto_yscl: int
    "Scale: Auto Scale"
    cIdx: list
    "ID for Curve (used for Labels)"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    ileg: int
    "Label"
    iopt_tim: int
    "Time Unit"
    ishort: int
    "Standard Legend uses"
    isteps: int
    "Draw Steps"
    loc_name: str
    "Name"
    mag: list
    "Magnitude"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pObjs: list
    "Element"
    phi: list
    "Angle"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sh_off: int
    "Scale Adapt Scale: Show Deviation from Offset"
    shw_leg: int
    "Show Legend"
    tid_: int
    "TimeID"
    typ_id: object
    "Scale: Type"
    use_x: int
    "Scale: Use local xAxis"
    use_y: int
    "Scale: Use local Axis"
    userdesc: list
    "Variable Description"
    x_fit: int
    "Scale: Adapt Scale"
    x_map: int
    "Scale: Scale"
    x_max: float
    "Scale Limits: Maximum"
    x_min: float
    "Scale Limits: Minimum"
    x_trg: float
    "Scale Adapt Scale: Trigger"
    xgrid: int
    "Grid Lines"
    xgrid_count: int
    "Count"
    xgrid_item: str
    "Reference"
    y_fit: int
    "Scale: Adapt Scale"
    y_max: float
    "Scale Limits: Maximum"
    y_min: float
    "Scale Limits: Minimum"
    y_off: float
    "Scale Adapt Scale: Offset"

    def AttributeType(*args): ...

    def Clear(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def GetDataSource(*args): ...

    def GetScaleObjX(*args): ...

    def GetScaleObjY(*args): ...

    def HasReferences(*args): ...

    def SetAutoScaleX(*args): ...

    def SetAutoScaleY(*args): ...

    def SetCrvDesc(*args): ...

    def SetDefScaleX(*args): ...

    def SetDefScaleY(*args): ...

    def __getattr__(*args): ...


class VisMagndiffplt(PFGeneral):
    AutoCol: int
    "Automatic: Colour"
    AutoStl: int
    "Automatic: Line Style"
    AutoWdt: int
    "Automatic: Line Width"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    Stack: float
    "Priority Level"
    Utils: list
    "Contents"
    aleg: str
    "User Label"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gColor: list
    "Colour"
    gObjs: list
    "Element"
    gSplit: list
    "Split Relay"
    gStyle: list
    "Style"
    gWidth: list
    "Width"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    ileg: int
    "Label"
    iopt_sgl: int
    "Show Section of Single Line Graphic"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sglGrp: object
    "Show Section of Single Line Graphic: Graphic"
    shw_leg: int
    "Show Legend"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    x_fit: int
    "x-Scale: Adapt Scale"
    x_max: float
    "x-Scale Limits: Maximum"
    x_min: float
    "x-Scale Limits: Minimum"
    y_fit: int
    "y-Scale: Adapt Scale"
    y_max: float
    "y-Scale Limits: Maximum"
    y_min: float
    "y-Scale Limits: Minimum"

    def AddRelay(*args): ...

    def AddRelays(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def HasReferences(*args): ...

    def Refresh(*args): ...

    def __getattr__(*args): ...


class VisOcplot(PFGeneral):
    AutoCol: int
    "Automatic: Colour"
    AutoStl: int
    "Automatic: Line Style"
    AutoWdt: int
    "Automatic: Line Width"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    Stack: float
    "Priority Level"
    Utils: list
    "Contents"
    aleg: str
    "User Label"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gColor: list
    "Colour"
    gObjs: list
    "Element"
    gRes: list
    "Result File"
    gSplit: list
    "Split Relay"
    gStyle: list
    "Style"
    gWidth: list
    "Width"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    ileg: int
    "Label"
    iopt_sgl: int
    "Show Section of Single Line Graphic"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pPath: object
    "Path"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sglGrp: object
    "Show Section of Single Line Graphic: Graphic"
    shw_leg: int
    "Show Legend"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    x_fit: int
    "x-Scale: Adapt Scale"
    x_map: int
    "x-Scale: Scale"
    x_max: float
    "x-Scale Limits: Maximum"
    x_min: float
    "x-Scale Limits: Minimum"
    y_fit: int
    "y-Scale: Adapt Scale"
    y_map: int
    "y-Scale: Scale"
    y_max: float
    "y-Scale Limits: Maximum"
    y_min: float
    "y-Scale Limits: Minimum"

    def AddRelay(*args): ...

    def AddRelays(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def HasReferences(*args): ...

    def Refresh(*args): ...

    def __getattr__(*args): ...


class VisPath(PFGeneral):
    AutoCol: int
    "Automatic: Colour"
    AutoStl: int
    "Automatic: Line Style"
    AutoWdt: int
    "Automatic: Line Width"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    Stack: float
    "Priority Level"
    UnomFilt: int
    "Display Filter: Show only nodes with Nominal Voltage between"
    UnomMax: float
    "Display Filter: and max."
    UnomMin: float
    "Display Filter: min."
    Utils: list
    "Contents"
    Variable: list
    "Variable"
    aleg: str
    "User Label"
    cVar: str
    "Branch Colouring: Variable"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    colvmax: int
    "Branch Colouring: "
    colvmin: int
    "Branch Colouring: "
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    feeder: list
    "Feeder"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gColor: list
    "Colour"
    gStyle: list
    "Style"
    gWidth: list
    "Width"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    ileg: int
    "Label"
    iopt_bus: int
    "Show Node Names"
    iopt_lim: int
    "Display Filter: Ignore nodes with a y-value smaller than"
    iopt_lvu: int
    "Display min/max voltages of low voltage grid in Loads"
    iopt_par: int
    "Branch Colouring: Parallel Branches"
    iopt_ufilt: int
    "Nodes Filter:None:Ignore all smaller:Ignore all greater:only with"
    iopt_x: int
    "x-Scale: x-Axis"
    iopt_xrel: int
    "x-Scale: Relative to Start Node"
    lim_low: float
    "Display Filter: y"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pSelect: object
    "Feeder"
    pStartNode: object
    "Start Node"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    shw_leg: int
    "Show Legend"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    ufiltset: float
    "Nominal Voltage"
    vmax: float
    "Branch Colouring: Upper Limit"
    vmin: float
    "Branch Colouring: Lower Limit"
    xVar: str
    "x-Scale: Variable"
    x_fit: int
    "x-Scale: Adapt Scale"
    x_max: float
    "x-Scale Limits: Maximum"
    x_min: float
    "x-Scale Limits: Minimum"
    y_fit: int
    "y-Scale: Adapt Scale"
    y_map: int
    "y-Scale: Scale"
    y_max: float
    "y-Scale Limits: Maximum"
    y_min: float
    "y-Scale Limits: Minimum"

    def AttributeType(*args): ...

    def Clear(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def HasReferences(*args): ...

    def SetAdaptX(*args): ...

    def SetAdaptY(*args): ...

    def SetScaleX(*args): ...

    def SetScaleY(*args): ...

    def __getattr__(*args): ...


class VisPcompdiffplt(PFGeneral):
    AutoCol: int
    "Automatic: Colour"
    AutoStl: int
    "Automatic: Line Style"
    AutoWdt: int
    "Automatic: Line Width"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    Stack: float
    "Priority Level"
    Utils: list
    "Contents"
    aleg: str
    "User Label"
    autos: int
    "Axis: Auto Scale"
    cIdx: list
    "Curve index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    distance: int
    "Axis: Distance"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gColor: list
    "Colour"
    gObjs: list
    "Element"
    gStyle: list
    "Style"
    gWidth: list
    "Width"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    icircles: int
    "Representation of Coordinates"
    ileg: int
    "Label"
    iopt_sgl: int
    "Show Section of Single Line Graphic"
    ishort: int
    "Axis: Standard Legend uses"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    scale: list
    "Axis: Scale"
    sglGrp: object
    "Show Section of Single Line Graphic: Graphic"
    shw_leg: int
    "Show Legend"
    tickDist: int
    "Distance between Ticks"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    unit: list
    "Axis: Unit"
    x_end: int
    "x-Max."
    x_start: int
    "Axis: x-Min."
    y_end: int
    "y-Max."
    y_start: int
    "Axis: y-Min."

    def AddRelay(*args): ...

    def AddRelays(*args): ...

    def AttributeType(*args): ...

    def CentreOrigin(*args): ...

    def Clear(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class VisPlot(PFGeneral):
    AutoBrs: int
    "Automatic: Brush Style"
    AutoCol: int
    "Automatic: Colour"
    AutoStl: int
    "Automatic: Line Style"
    AutoWdt: int
    "Automatic: Line Width"
    Brush: list
    "Brush Style"
    Color: list
    "Colour"
    Depth: int
    "Visible"
    Elements: list
    "Elements"
    FrmVis: int
    "Frame"
    Height: list
    "Height"
    Objectx: list
    "Element"
    Position: list
    "Position"
    ResFile: list
    "Result File"
    Stack: float
    "Priority Level"
    Style: list
    "Style"
    Utils: list
    "Contents"
    Variable: list
    "Variable"
    Variablex: list
    "Variable"
    Width: list
    "Width"
    aleg: str
    "Frame: User Label"
    auto_xscl: int
    "Auto Scale"
    auto_yscl: int
    "Auto Scale"
    cIdx: list
    "ID for Curve (used for Labels)"
    cfunction: list
    "Function"
    charact: list
    "Charact."
    chart: int
    "Chart"
    chr_name: str
    "Characteristic Name"
    commonResults: object
    "Results: Common Results"
    cpHeadFold: object
    "Head Folder"
    cy_map: int
    "Scaling"
    dDistAScale: float
    "Auto Scale: Margin"
    dIsNom: list
    "Norm"
    dStep: float
    "Resolution: Step Size"
    dValNom: list
    "Nom.Value"
    dat_src: str
    "Data source"
    descx: list
    "User defined Legend"
    drawarea: int
    "Draw area below curve"
    drel: float
    "Start Value"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    fullLimits: list
    "Limits"
    funObj: list
    "Function object"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    ileg: int
    "Frame: User defined"
    iopt_fund: str
    "Fund. Frequency"
    iopt_nom: str
    "Normalised Values"
    iopt_rep: int
    "Representation"
    iopt_results: int
    "Results"
    iopt_thds: int
    "Display corresponding THD or THF"
    iopt_tim: int
    "x Axis Variable"
    iopt_tim1: int
    "x Variable"
    iopt_view: int
    "Presentation"
    is_path: int
    "Diagram shows"
    isample: int
    "Resolution"
    ishort: int
    "Legend: Standard Legend uses"
    isteps: int
    "Presentation: Draw Steps"
    itRef: int
    "Results used for time reference"
    last: float
    "Range"
    limit: str
    "Harmonic Limits: Show"
    limits: str
    "Show"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pObjs: list
    "Element"
    pObjx: object
    "Element"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sh_off: int
    "Adapt Scale: Show Deviation from Offset"
    show_title: int
    "Display plot name"
    show_x: int
    "Display x-Axis"
    show_y: int
    "Display y-Axis"
    shw_arr: int
    "Show direction arrows for curves"
    shw_leg: int
    "Legend: Position:None:Bottom:Right"
    src_y: int
    "Axis"
    standard: str
    "Harmonic Limits: Standard"
    summate: int
    "Summate curve values (in reverse order; bottom top)"
    tRef: list
    "Time Ref."
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    use_x: int
    "Axis"
    use_y: int
    "Use local Axis"
    usedfor: str
    "Results Type"
    userdesc: list
    "Variable Description"
    vPath: object
    "Path"
    variable: list
    "Variable"
    x_fit: int
    "Adapt Scale"
    x_map: int
    "Scaling"
    x_max: float
    "Maximum"
    x_min: float
    "Minimum"
    x_trg: float
    "Adapt Scale: Trigger"
    xgrid: int
    "Grid Lines"
    xgrid_count: int
    "Grid Lines: Count"
    xgrid_item: str
    "Reference"
    y_fit: int
    "Adapt Scale"
    y_map: int
    "Scaling"
    y_max: float
    "Maximum"
    y_min: float
    "Minimum"
    y_off: float
    "Adapt Scale: Offset"

    def AddResVars(*args): ...

    def AddVars(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def GetDataSource(*args): ...

    def GetIntCalcres(*args): ...

    def GetScaleObjX(*args): ...

    def GetScaleObjY(*args): ...

    def HasReferences(*args): ...

    def SetAdaptX(*args): ...

    def SetAdaptY(*args): ...

    def SetAutoScaleX(*args): ...

    def SetAutoScaleY(*args): ...

    def SetCrvDesc(*args): ...

    def SetDefScaleX(*args): ...

    def SetDefScaleY(*args): ...

    def SetScaleX(*args): ...

    def SetScaleY(*args): ...

    def SetXVar(*args): ...

    def __getattr__(*args): ...


class VisPlot2(PFGeneral):
    AutoCol: int
    "Automatic (y1/y2): Colour"
    AutoStl: int
    "Automatic (y1/y2): Line Style"
    AutoWdt: int
    "Automatic (y1/y2): Line Width"
    Color: list
    "Colour"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    ResFile: list
    "Result File"
    Stack: float
    "Priority Level"
    Style: list
    "Style"
    Utils: list
    "Contents"
    Variable: list
    "Variable"
    Variablex: list
    "Variable"
    Width: list
    "Width"
    aleg: str
    "Frame: User Label"
    auto_xscl: int
    "Auto Scale"
    auto_yscl: int
    "Auto Scale (y1/y2)"
    cColor: int
    "Colour"
    cColor2: int
    "Colour"
    cIdx: list
    "ID for Curve (used for Labels)"
    cResFile: list
    "Result File"
    cResFile2: list
    "Result File"
    cStyle: list
    "Style"
    cStyle2: list
    "Style"
    cVariable: list
    "Variable"
    cVariable2: list
    "Variable"
    cWidth: list
    "Width"
    cWidth2: list
    "Width"
    cdIsNom: list
    "Norm"
    cdIsNom2: list
    "Norm"
    cdValNom: list
    "Nom.Value"
    cdValNom2: list
    "Nom.Value"
    charact: list
    "Charact."
    chart: int
    "Chart"
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    cpObjs: list
    "Element"
    cpObjs2: list
    "Element"
    cuserdesc: list
    "Variable Description"
    cuserdesc2: list
    "Variable Description"
    dDistAScale: float
    "Auto Scale (y1/y2): Margin"
    dIsNom: list
    "Norm"
    dValNom: list
    "Nom.Value"
    dat_src: str
    "Data source"
    descx: list
    "User defined Legend"
    drel: float
    "Start Value"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iPlot: list
    "Axis Index"
    iSchemeStatus: int
    "Scheme Status"
    ileg: int
    "Frame: User defined"
    iopt_nom: str
    "Normalised Values"
    iopt_tim: int
    "x Axis Variable"
    iopt_tim1: int
    "x Variable"
    iopt_y2: int
    "Use second y Axis, Scale"
    ishort: int
    "Legend: Standard Legend uses"
    isteps: int
    "Draw Steps"
    last: float
    "Range"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pObjs: list
    "Element"
    pObjx: object
    "Element"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    show_title: int
    "Display plot name"
    shw_arr: int
    "Show direction arrows for curves"
    shw_leg: int
    "Legend: Position:None:Bottom:Right"
    src_y: int
    "Axis"
    src_y2: int
    "Axis"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    use_x: int
    "Axis"
    use_y: int
    "Use local Axis"
    use_y2: int
    "Use local Axis"
    usedfor: str
    "Results Type"
    userdesc: list
    "Variable Description"
    x_fit: int
    "Adapt Scale"
    x_map: int
    "Scaling"
    x_max: float
    "Maximum"
    x_min: float
    "Minimum"
    x_trg: float
    "Adapt Scale: Trigger"
    xgrid: int
    "Grid Lines"
    xgrid_count: int
    "Grid Lines: Count"
    xgrid_item: str
    "Reference"
    y2_fit: int
    "Adapt Scale"
    y2_max: float
    "Maximum"
    y2_min: float
    "Minimum"
    y2_off: float
    "Adapt Scale: Offset"
    y_fit: int
    "Adapt Scale"
    y_map: int
    "Scaling (y1/y2)"
    y_max: float
    "Maximum"
    y_min: float
    "Minimum"
    y_off: float
    "Adapt Scale: Offset"

    def AddResVars(*args): ...

    def AddVars(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def DoAutoScaleY2(*args): ...

    def GetDataSource(*args): ...

    def GetScaleObjX(*args): ...

    def GetScaleObjY(*args): ...

    def HasReferences(*args): ...

    def SetAdaptX(*args): ...

    def SetAdaptY(*args): ...

    def SetAutoScaleX(*args): ...

    def SetAutoScaleY(*args): ...

    def SetCrvDesc(*args): ...

    def SetDefScaleX(*args): ...

    def SetDefScaleY(*args): ...

    def SetScaleX(*args): ...

    def SetScaleY(*args): ...

    def SetXVar(*args): ...

    def ShowY2(*args): ...

    def __getattr__(*args): ...


class VisPlottz(PFGeneral):
    AutoCol: int
    "Automatic: Colour"
    AutoStl: int
    "Automatic: Line Style"
    AutoWdt: int
    "Automatic: Line Width"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    Stack: float
    "Priority Level"
    Utils: list
    "Contents"
    aleg: str
    "User Label"
    cRef: object
    "Reference Relay, Forward: Used one"
    cRefB: object
    "Reference Relay, Backward: Used One"
    cfCirc: list
    "Circular"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    cres: object
    "Results"
    dat_src: str
    "Data source"
    fCirc: list
    "Circular"
    fColor: list
    "Colour"
    fObjs: list
    "Element"
    fStyle: list
    "Style"
    fWidth: list
    "Width"
    fit: int
    "y-Scale: Adapt Scale"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    iTbrk: int
    "Consider Breaker Opening Time"
    ileg: int
    "Label"
    ilne_over: int
    "Overreach Zones: Line Style"
    iopt_dia: str
    "Diagrams"
    iopt_mod: str
    "Method"
    iopt_over: int
    "Overreach Zones: Representation:like zones:show:ignore"
    iopt_unit: str
    "x-Unit"
    leg_bus: int
    "Show Legend: Include Terminal/Station Name"
    leg_numcol: int
    "Show Legend: Number of columns"
    loc_name: str
    "Name"
    max: float
    "y-Scale Limits: Maximum"
    min: float
    "y-Scale Limits: Minimum"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pPath: object
    "Path"
    pRef: object
    "Reference Relay, Forward: Relay"
    pRefB: object
    "Reference Relay, Backward: Relay"
    p_res: object
    "Results"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sglGrp: object
    "Show Section of Single Line Graphic: Graphic"
    shownResult: list
    "Displayed"
    shw_bus: int
    "Hide names of busbars without relays"
    shw_leg: int
    "Show Legend"
    shw_sgl: int
    "Show Section of Single Line Graphic"
    subResName: str
    "Sub-Result Name"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    xfit: int
    "x-Scale: Adapt Scale"
    xmax: float
    "x-Scale Limits: Maximum"
    xmaxb: float
    "x-Scale Limits: Maximum"
    xmin: float
    "x-Scale Limits: Minimum"
    xminb: float
    "x-Scale Limits: Minimum"

    def AddRelay(*args): ...

    def AddRelays(*args): ...

    def AttributeType(*args): ...

    def Clear(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class VisVec(PFGeneral):
    AutoCol: int
    "Automatic: Colour"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    Stack: float
    "Priority Level"
    Utils: list
    "Contents"
    Var: list
    "Complex Variable"
    aleg: str
    "User Label"
    autos: int
    "Axis: Auto Scale"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    iallph: int
    "Show all phases in plot (otherwise only selected phase)"
    icircles: int
    "Representation of Coordinates"
    ilabel: int
    "Label of Vectors"
    ileg: int
    "Label"
    ishort: int
    "Standard Legend uses"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pObj: list
    "Element"
    pid_: int
    "ProjectID"
    polar: list
    "Coordinates"
    root_id: object
    "Original Location"
    scale: list
    "Axis: Scale"
    shw_leg: int
    "Show Legend"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    unit: list
    "Axis: Unit"
    userdesc: list
    "Description"
    vColor: list
    "Colour"
    vStyle: list
    "Style"
    vWidth: list
    "Width"
    xVar: list
    "Real Part/Magnitude"
    x_end: int
    "x - Max."
    x_start: int
    "Axis: x - Min."
    yVar: list
    "Imaginary Part/Angle"
    y_end: int
    "y - Max."
    y_start: int
    "Axis: y - Min."

    def AttributeType(*args): ...

    def CentreOrigin(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class VisVecres(PFGeneral):
    AutoCol: int
    "Automatic: Colour"
    Color: list
    "Colour"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    Stack: float
    "Priority Level"
    Style: list
    "Style"
    Utils: list
    "Contents"
    Variable: list
    "Variable"
    Width: list
    "Width"
    aleg: str
    "User Label"
    autos: int
    "Axis: Auto Scale"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    cursor: object
    "Cursor"
    dat_src: str
    "Data source"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBordFont: int
    "Font for frame label"
    iSchemeStatus: int
    "Scheme Status"
    icircles: int
    "Representation of Coordinates"
    ilabel: int
    "Label of Vectors"
    ileg: int
    "Label"
    ishort: int
    "Legend: Standard Legend uses"
    loc_name: str
    "Name"
    msg_name: list
    "%s-%s"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pObj: list
    "Element"
    pid_: int
    "ProjectID"
    polar: list
    "Coordinates"
    resObj: list
    "Results"
    root_id: object
    "Original Location"
    scale: list
    "Axis: Scale"
    shw_leg: int
    "Legend: Position:None:Bottom:Right"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"
    unit: list
    "Axis: Unit"
    userdesc: list
    "Description"
    variable: list
    "Variable"
    x_end: int
    "x - Max."
    x_start: int
    "Axis: x - Min."
    y_end: int
    "y - Max."
    y_start: int
    "Axis: y - Min."

    def AttributeType(*args): ...

    def CentreOrigin(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class VisXyplot(PFGeneral):
    AutoCol: int
    "Automatic: Colour"
    AutoStl: int
    "Automatic: Line Style"
    AutoWdt: int
    "Automatic: Line Width"
    Depth: int
    "Visible"
    FrmVis: int
    "Frame"
    Position: list
    "Position"
    ResFile: list
    "Result File"
    Stack: float
    "Priority Level"
    Utils: list
    "Contents"
    aleg: str
    "User Label"
    auto_x: int
    "x-Axis: Auto Scale"
    auto_y: int
    "y-Axis: Auto Scale"
    cIdx: list
    "ID for Curve (used for Labels)"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dIsNom: list
    "Norm"
    dIsNomX: list
    "Norm X"
    dValNom: list
    "Nom.Value"
    dValNomX: list
    "Nom.Value X"
    dat_src: str
    "Data source"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAll: int
    "Show whole Time Range"
    iArrow: int
    "Show Vector"
    iBordFont: int
    "Font for frame label"
    iObjx: int
    "Show x-Element in Table"
    iSchemeStatus: int
    "Scheme Status"
    iVector: int
    "Diagram shows"
    ileg: int
    "Label"
    iopt_nom: str
    "Nom. Values"
    ishort: int
    "Standard Legend uses"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_Scale: object
    "Scale"
    pid_: int
    "ProjectID"
    pxObj: list
    "Element x-Axis"
    pyObj: list
    "Element y-Axis"
    root_id: object
    "Original Location"
    shw_arr: int
    "Show direction arrows for curves"
    shw_leg: int
    "Show Legend"
    tid_: int
    "TimeID"
    tmax: float
    "Range: Maximum"
    tmin: float
    "Range: Minimum"
    typ_id: object
    "Type"
    unit: list
    "Unit"
    use_loc: int
    "Use local Scales"
    usedfor: str
    "Results Type"
    userdx: list
    "Description X-Var."
    userdy: list
    "Description Y-Var."
    vColor: list
    "Colour"
    vStyle: list
    "Style"
    vWidth: list
    "Width"
    xVar: list
    "Var. x-Axis"
    x_fit: int
    "x-Axis: Adapt Scale"
    x_map: int
    "x-Axis: Scale"
    x_max: list
    "x-Maximum"
    x_min: list
    "x-Minimum"
    x_off: list
    "x-Offset"
    xvar: list
    "Var. x-Axis"
    yVar: list
    "Var. y-Axis"
    y_fit: int
    "y-Axis: Adapt Scale"
    y_map: int
    "y-Axis: Scale"
    y_max: list
    "y-Maximum"
    y_min: list
    "y-Minimum"
    y_off: list
    "y-Offset"
    yvar: list
    "Var. y-Axis"

    def AttributeType(*args): ...

    def Clear(*args): ...

    def DoAutoScaleX(*args): ...

    def DoAutoScaleY(*args): ...

    def GetDataSource(*args): ...

    def HasReferences(*args): ...

    def SetCrvDescX(*args): ...

    def SetCrvDescY(*args): ...

    def __getattr__(*args): ...


class IntFolder(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cimRdfId: list
    "RDF ID"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    filter: str
    "Filter"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iopt_sys: int
    "System"
    iopt_typ: int
    "Folder Type"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    owner: str
    "Owner"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmSite(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cimRdfId: list
    "RDF ID"
    contents: list
    "Contents"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pDiagram: object
    "Diagram"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sType: str
    "Type"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComVstab(PFGeneral):
    addoptions: str
    "Additional Parameters"
    calcBoundSens: int
    "Calculate boundary sensitivity between adjacent regions"
    calcDiaElms: int
    "Diagonal elements only"
    calcHvdc: int
    "Sensitivities / Distribution factors: Sensitivity to HVDC"
    calcLodf: int
    "Sensitivities / Distribution factors: Line Outage Distribution Factors"
    calcModal: int
    "Modal/Eigenvalue Analysis"
    calcPtdf: int
    "Sensitivities / Distribution factors: Busbar"
    calcRegionSens: int
    "Calculate regional sensitivities"
    calcShiftKeySens: int
    "Injection based on generation shift key (GSK)"
    calcTapChg: int
    "Sensitivities / Distribution factors: Phase Shift/Tap Change"
    ccalcPtdf: int
    "Sensitivities / Distribution factors: Busbar"
    ccalcRegionSens: int
    "Calculate regional sensitivities"
    cdpflim: float
    "Consider recording thresholds for branches: dP/dP"
    cdtplim: float
    "Consider recording thresholds for branches: dP/dtap"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciopt_method: int
    "Calculation method"
    considerAllGskGens: int
    "Consider generators with the setting 'Out of service when active power is zero'"
    considerThresh: int
    "Consider recording thresholds"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    cshwAllSensVars: int
    "Calculate all sensitivity variables"
    ctrfSensMeth: int
    "Calculation method for transformer tap sensitivities"
    danlim: float
    "Consider recording thresholds for terminals: Angle change (w.r.t. power or tap)"
    danlimi: float
    "Consider recording thresholds for terminals: Angle change (w.r.t. current sequence)"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dbgOn: int
    "Debug mode"
    dpflim: float
    "Consider recording thresholds for branches: dP/dP, dQ/dP, dP/dQ, dQ/dQ"
    dpflimi: float
    "Consider recording thresholds for branches: dP/di_seq, dQ/di_seq"
    dtplim: float
    "Consider recording thresholds for branches: dP/dtap, dQ/dtap"
    dvolim: float
    "Consider recording thresholds for terminals: Voltage change (w.r.t. power or tap)"
    dvolimi: float
    "Consider recording thresholds for terminals: Voltage change (w.r.t. current sequence)"
    factors4bus: int
    "Power change"
    factors4conv: int
    "Power change"
    factors4trf: int
    "Tap change"
    filename: str
    "File name"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frmElmFilt4Res: int
    "Elements for results"
    frmLimitsBrc: int
    "Consider recording thresholds for branches"
    frmLimitsBus: int
    "Consider recording thresholds for terminals"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iExport: int
    "Export results to Comma Separated Values (*.csv) file"
    iSchemeStatus: int
    "Scheme Status"
    i_nr: int
    "Modal/Eigenvalue Analysis: Number of Eigenvalues"
    ignoreReds: int
    "Elements for results: Calculate sensitivities for reducible elements"
    iopt_method: int
    "Calculation method"
    iopt_mod: int
    "Calculation type"
    isContSens: int
    "Consider contingencies"
    isLinearCont: int
    "Consider contingencies: Use linearised AC calculation"
    isResultFile: int
    "Recording of results"
    loc_name: str
    "Name"
    lodflim: float
    "Consider recording thresholds for branches: Min. Line Outage Distribution Factors"
    obj_bus: int
    "User-defined 3-/4-winding transformer control side: Bus Index"
    oid_: int
    "ObjectID"
    optRep: int
    "Output"
    order: float
    "Order"
    pComSimoutage: object
    "Consider contingencies: Contingency Analysis"
    pFictitiousGrid: object
    "Use fictitious border network: Border network"
    pResult: object
    "Result file: Results"
    p_bus: object
    "Sensitivities / Distribution factors: Busbar(s)"
    p_hvdc: object
    "Sensitivities / Distribution factors: HVDC(s)"
    p_tr: object
    "Sensitivities / Distribution factors: Transformer(s)/Tap-Controller(s)"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    set_mode: int
    "Modal/Eigenvalue Analysis: Display Results for Mode"
    setfilter: object
    "Elements for results: Element filter"
    shwAllSensVars: int
    "Calculate all sensitivity variables"
    tapDirection: int
    "Tap direction"
    taplimtrfs: int
    "Consider transformers at max. or min. tap position."
    tid_: int
    "TimeID"
    trfSensMeth: int
    "Calculation method for transformer tap sensitivities"
    useFictitiousGrid: int
    "Use fictitious border network"
    usrtrside: int
    "User-defined 3-/4-winding transformer control side"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComQvcurves(PFGeneral):
    P_Step: float
    "Active Power Iteration: Step size"
    VoltageStep: float
    "Voltage iteration: Step size"
    addoptions: str
    "Additional Parameters"
    calcCont: int
    "Consider contingencies"
    calcType: int
    "Calculation"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    controlOut: int
    "Detailed output: Deactivated voltage controllers"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    debugOut: int
    "Detailed output: Voltage iterations"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frActiveP: int
    "Additional active power injection"
    frCalcStart: int
    "Voltage range"
    frStepsize: int
    "Voltage iteration"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    iniP: float
    "Active Power Iteration: Minimum"
    iniVoltage: float
    "Voltage iteration: Maximum voltage"
    ldfOut: int
    "Detailed output: Messages of initial Load Flow of each curve"
    listP: list
    "Active Power"
    loc_name: str
    "Name"
    maxIter: int
    "Maximum iterations"
    minusVolt: float
    "Voltage iteration: Minimum: Base case voltage minus"
    noStopCalc: int
    "Voltage iteration: Continue if load flow of the maximum (initial) voltage did not converge"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pInputCont: object
    "Consider contingencies: Contingency Analysis"
    pStudyBB: object
    "Analysed nodes"
    pid_: int
    "ProjectID"
    plusVoltage: float
    "Voltage iteration: Maximum: Base case voltage plus"
    results: object
    "Results"
    root_id: object
    "Original Location"
    stopVolt: float
    "Voltage iteration: Minimum voltage"
    targetP: float
    "Active Power Iteration: Maximum"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComMod(PFGeneral):
    MP_alg: int
    "Direct construction of A-matrix (as in V13.2)"
    ResultFile: object
    "Results"
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cinitMode: int
    "Operating point for calculation"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dirMatl: str
    "Output to Matlab files: in Directory"
    epsIdent: float
    "Identification of eigenvalues: consider identical if distance smaller"
    erreq: float
    "Iteration Control: Maximum Error of Model Equations"
    errsm: float
    "Iteration Control: Maximum Iteration Error of Nodal Equations"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iChkEVecs: int
    "Omit eigenvalues if eigenvector-transformation fails."
    iDirectA: int
    "Direct construction of A-matrix (as in V13.2)"
    iEValMatl: int
    "Output to Matlab files: Eigenvalues"
    iExtra: int
    "Solve implicit system"
    iGnrlMode: int
    "Initialisation of Arnoldi Iteration"
    iLEVMatl: int
    "Output to Matlab files: Left Eigenvectors (Controllability)"
    iLeft: int
    "Calculate: Left Eigenvectors (Controllability)"
    iPart: int
    "Calculate: Participation Factors"
    iPartMatl: int
    "Output to Matlab files: Participation Factors"
    iQRorQZ: int
    "Algorithm"
    iREVMatl: int
    "Output to Matlab files: Right Eigenvectors (Observability)"
    iRight: int
    "Calculate: Right Eigenvectors (Observability)"
    iSchemeStatus: int
    "Scheme Status"
    iSparse: int
    "Use spectral transformation"
    iSysMatsMatl: int
    "Output to Matlab files: System Matrices"
    i_nr: int
    "Number of Eigenvalues"
    ignoreAbove: float
    "Recording filter for eigenvalues: Max. magnitude"
    ignoreBelow: float
    "Recording filter for eigenvalues: Min. magnitude"
    initMode: int
    "Operating point for calculation"
    iopt_met: int
    "Calculation Method"
    iopt_noevec: int
    "Calculate Eigenvalues only"
    iopt_which: int
    "Selection of eigenvalues closest to RP"
    isRecMaxDampRat: int
    "Recording filter for eigenvalues: Max. damp. ratio"
    isRecMaxImag: int
    "Recording filter for eigenvalues: Max. imag. part"
    isRecMaxMagn: int
    "Recording filter for eigenvalues: Max. magnitude"
    isRecMaxReal: int
    "Recording filter for eigenvalues: Max. real part"
    isRecMinDampRat: int
    "Recording filter for eigenvalues: Min. damp. ratio"
    isRecMinImag: int
    "Recording filter for eigenvalues: Min. imag. part"
    isRecMinMagn: int
    "Recording filter for eigenvalues: Min. magnitude"
    isRecMinReal: int
    "Recording filter for eigenvalues: Min. real part"
    isRecOscModesOnly: int
    "Recording filter for eigenvalues: Oscillatory modes only"
    isRecUnstabModesOnly: int
    "Recording filter for eigenvalues: Unstable modes only"
    isShowFilteredEvals: int
    "Report filtered out eigenvalues in output window"
    loc_name: str
    "Name"
    maxDampRat: float
    "Recording filter for eigenvalues: Max. damp. ratio"
    maxDampedFreq: float
    "Recording filter for eigenvalues: Max. frequency"
    maxImag: float
    "Recording filter for eigenvalues: Max. imag. part"
    maxReal: float
    "Recording filter for eigenvalues: Max. real part"
    minDampRat: float
    "Recording filter for eigenvalues: Min. damp. ratio"
    minDampedFreq: float
    "Recording filter for eigenvalues: Min. frequency"
    minImag: float
    "Recording filter for eigenvalues: Min. imag. part"
    minReal: float
    "Recording filter for eigenvalues: Min. real part"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    outputType: int
    "Output"
    pInitCond: object
    "Operating point for calculation: Initial conditions"
    pid_: int
    "ProjectID"
    repBufferAndExtDll: int
    "Report models containing buffers, time-discrete variables or external functions"
    repConstantStates: int
    "Report state variables that are assumed to be constant at current operating point"
    root_id: object
    "Original Location"
    shiftDampFreq: float
    "Complex reference point (RP): Damped frequency:"
    shifti: float
    "Complex reference point (RP): Imaginary part:"
    shiftr: float
    "Complex reference point (RP): Real part:"
    tid_: int
    "TimeID"
    tol: float
    "Eigenvalue convergence tolerance"
    useBalancing: int
    "Apply algorithm for improved conditioning"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmSecctrl(PFGeneral):
    Kpf: float
    "Active Power Exchange: Frequency Bias"
    Pexmax: float
    "Economic Dispatch: Maximum Power Interchange"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cmo: int
    "Merit Order"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Active Power Exchange: Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cvpp: list
    "Active Power Percentage"
    dReserve: float
    "Economic Dispatch: Minimum Control Reserve"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iComDate: int
    "Commissioning Date"
    iOPFCpsummax: int
    "Max. Total Active Power Limit"
    iOPFCpsummin: int
    "Min. Total Active Power Limit"
    iSchemeStatus: int
    "Scheme Status"
    i_net: int
    "Control Mode"
    i_pest: int
    "Estimate Area Exchange Flow"
    i_popt: int
    "Optimise Area Exchange Flow"
    iexchange: int
    "Active Power Exchange: Exchange for"
    imode: int
    "Active Power Distribution"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pPmeas: object
    "Active Power Exchange: Boundary/Zone/Area"
    pid_: int
    "ProjectID"
    psetp: float
    "Active Power Exchange: Power Setpoint"
    psummax: float
    "Max. Total Active Power Limit"
    psummin: float
    "Min. Total Active Power Limit"
    psym: list
    "Machines"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    rembar: object
    "Busbar for Frequency Measurement"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    tid_: int
    "TimeID"
    vpp: list
    "Active Power Percentage"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmLod(PFGeneral):
    Bc_hv: float
    "HV Capacitance"
    Bc_lv: float
    "Additional LV Capacitance"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Iks: float
    "Fault Contribution Scalable Fault Contribution: Transient Short-Circuit Current"
    Iksfix: float
    "Fault Contribution Fixed Fault Contribution: Transient Short-Circuit Level"
    Iksfixmin: float
    "Fixed Fault Contribution: Transient Short-Circuit Level"
    Ikss: float
    "Fault Contribution Scalable Fault Contribution: Subtransient Short-Circuit Current"
    Ikssfix: float
    "Fault Contribution Fixed Fault Contribution: Subtransient Short-Circuit Level"
    Ikssfixmin: float
    "Fault Contribution Fixed Fault Contribution: Subtransient Short-Circuit Level"
    Inom: float
    "Nominal Current"
    Irated: float
    "Harmonic Current Injections: Rated Current"
    NrCust: int
    "Number of connected customers"
    OptCost: int
    "Interruption costs: Unit"
    Sks: float
    "Fault Contribution Scalable Fault Contribution: Transient Short-Circuit Level"
    Sksfix: float
    "Fault Contribution Fixed Fault Contribution: Transient Short-Circuit Level"
    Sksfixmin: float
    "Fixed Fault Contribution: Transient Short-Circuit Level"
    Skss: float
    "Fault Contribution Scalable Fault Contribution: Subtransient Short-Circuit Level"
    Skssfix: float
    "Fault Contribution Fixed Fault Contribution: Subtransient Short-Circuit Level"
    Skssfixmin: float
    "Fault Contribution Fixed Fault Contribution: Subtransient Short-Circuit Level"
    Strat: float
    "Consider Load Transformer: Rated Power"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal"
    cBasedOn: float
    "based on"
    cDisplayName: str
    "Display Name"
    cTrans: float
    "Load shedding/transfer (Transmission Option): Resulting"
    cTypHmc: str
    "Harmonic Current Injections: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    classif: str
    "Load Classification:Agricultural:Domestic:Commercial:Industrial"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    coslini: float
    "Operating Point: Power Factor"
    coslini_a: float
    "cos(phi)(act.)"
    coslinir: float
    "Phase 1: Power Factor"
    coslinir_a: float
    "Ph 1:cos(phi)(act.)"
    coslinis: float
    "Phase 2: Power Factor"
    coslinis_a: float
    "Ph 2:cos(phi)(act.)"
    coslinit: float
    "Phase 3: Power Factor"
    coslinit_a: float
    "Ph 3:cos(phi)(act.)"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    ctotIks: float
    "Fault Contribution: Total contribution (transient)"
    ctotIksmin: float
    "Total contribution (transient)"
    ctotIkss: float
    "Fault Contribution: Total contribution (subtransient)"
    ctotIkssmin: float
    "Fault Contribution: Total contribution (subtransient)"
    ctotSks: float
    "Fault Contribution: Total contribution (transient)"
    ctotSksmin: float
    "Total contribution (transient)"
    ctotSkss: float
    "Fault Contribution: Total contribution (subtransient)"
    ctotSkssmin: float
    "Fault Contribution: Total contribution (subtransient)"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    dudropLVfeed: float
    "LV Voltage Changes: Maximum Voltage Drop (LV Grid)"
    duriseLVfeed: float
    "LV Voltage Changes: Maximum Voltage Rise (LV Grid)"
    fSCDF: float
    "Interruption costs: Scaling factor"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iLoadTrf: int
    "Consider Load Transformer"
    iSchemeStatus: int
    "Scheme Status"
    iShedding: int
    "Controls: Allow load shedding"
    i_normPQext: int
    "Pext, Qext input signals normalised to load flow voltage"
    i_pini: int
    "State Estimation Active/Reactive Power: Estimate Active Power"
    i_prty: int
    "Priority"
    i_qini: int
    "State Estimation Active/Reactive Power: Estimate Reactive Power"
    i_rem: int
    "Remote Control"
    i_scale: int
    "Operating Point: Adjusted by Load Scaling"
    i_scaleini: int
    "State Estimation Scaling Factor: Estimate Scaling Factor"
    i_sym: int
    "Balanced/Unbalanced"
    icurref: int
    "Harmonic Current Injections: Harmonic currents referred to"
    iecShcModel: int
    "Fault Contribution: Short-Circuit Model:Static converter-fed drive:Equivalent synchronous machine"
    iecfltcont: int
    "Fault Contribution"
    ilini: float
    "Operating Point: Current"
    ilini_a: float
    "I(act.)"
    ilinir: float
    "Phase 1: Current"
    ilinir_a: float
    "Ph 1:I(act.)"
    ilinis: float
    "Phase 2: Current"
    ilinis_a: float
    "Ph 2:I(act.)"
    ilinit: float
    "Phase 3: Current"
    ilinit_a: float
    "Ph 3:I(act.)"
    iopt_type: int
    "Allow Load-Ramp Event"
    isCtrlLdShed: int
    "Controls for Unit Commitment: Allow load shedding"
    loc_name: str
    "Name"
    mode_inp: str
    "Input Mode"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pSCDF: object
    "Interruption costs: Tariff"
    pTrans: object
    "Load shedding/transfer (Transmission Option): Alternative Supply (Load)"
    p_cub: object
    "Controlled Branch (Cubicle)"
    p_direc: int
    "Operating Point: Power Direction:P>=0:P<0"
    p_direcr: int
    "Phase 1: Power Direction:P>=0:P<0"
    p_direcs: int
    "Phase 2: Power Direction:P>=0:P<0"
    p_direct: int
    "Phase 3: Power Direction:P>=0:P<0"
    pcontract: float
    "Contracted Active Power"
    pf_recap: int
    "Operating Point: Power Factor:ind.:cap."
    pf_recapr: int
    "Phase 1: Power Factor:ind.:cap."
    pf_recaps: int
    "Phase 2: Power Factor:ind.:cap."
    pf_recapt: int
    "Phase 3: Power Factor:ind.:cap."
    phmc: object
    "Harmonic Current Injections: Harmonic Currents"
    phtech: str
    "Technology"
    pid_: int
    "ProjectID"
    plini: float
    "Operating Point: Active Power"
    plini_a: float
    "P(act.)"
    plinir: float
    "Phase 1: Active Power"
    plinir_a: float
    "Ph 1:P(act.)"
    plinis: float
    "Phase 2: Active Power"
    plinis_a: float
    "Ph 2:P(act.)"
    plinit: float
    "Phase 3: Active Power"
    plinit_a: float
    "Ph 3:P(act.)"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    qlini: float
    "Operating Point: Reactive Power"
    qlini_a: float
    "Q(act.)"
    qlinir: float
    "Phase 1: Reactive Power"
    qlinir_a: float
    "Ph 1:Q(act.)"
    qlinis: float
    "Phase 2: Reactive Power"
    qlinis_a: float
    "Ph 2:Q(act.)"
    qlinit: float
    "Phase 3: Reactive Power"
    qlinit_a: float
    "Ph 3:Q(act.)"
    r0: float
    "Consider Load Transformer: r0"
    r1Sbasepu: float
    "r1(shc) (Sbase)"
    r2Sbasepu: float
    "r2(shc) (Sbase)"
    ramp_type: int
    "Allow Load-Ramp Event"
    root_id: object
    "Original Location"
    rtox: float
    "Fault Contribution: R to X'' ratio"
    rtoxmin: float
    "Fault Contribution: R to X'' ratio"
    scale0: float
    "Operating Point: Scaling Factor"
    scale0_a: float
    "Scaling Factor(act.)"
    sernum: str
    "Serial Number"
    shed: int
    "Load shedding/transfer (Transmission Option): Shedding steps:infinite:1:2:3:4:5:6:7:8:9:10"
    shedcost: float
    "Costs: Costs for load shedding"
    shedmax: float
    "Load shedding constraints for apparent power: Max. load shedding"
    shedmin: float
    "Load shedding constraints for apparent power: Min. load shedding"
    slini: float
    "Operating Point: Apparent Power"
    slini_a: float
    "S(act.)"
    slinir: float
    "Phase 1: Apparent Power"
    slinir_a: float
    "Ph 1:S(act.)"
    slinis: float
    "Phase 2: Apparent Power"
    slinis_a: float
    "Ph 2:S(act.)"
    slinit: float
    "Phase 3: Apparent Power"
    slinit_a: float
    "Ph 3:S(act.)"
    tid_: int
    "TimeID"
    trans: float
    "Load shedding/transfer (Transmission Option): Transferable"
    typ_id: object
    "Type"
    u0: float
    "Operating Point: Voltage"
    x0: float
    "Consider Load Transformer: x0"
    x1sSbasepu: float
    "x1'(shc) (Sbase)"
    x1ssSbasepu: float
    "x1''(shc) (Sbase)"
    x2Sbasepu: float
    "x2(shc) (Sbase)"
    xt: float
    "Load Transformer Reactance"
    xtor: float
    "Fault Contribution: X'' to R ratio"
    xtormin: float
    "Fault Contribution: X'' to R ratio"
    zonefact: float
    "Zone Scaling Factor:"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmIac(PFGeneral):
    B0: float
    "Zero Sequence: Internal Susceptance, B0"
    B1: float
    "Positive Sequence: Internal Susceptance, B1"
    B2: float
    "Negative Sequence: Internal Susceptance, B2"
    G0: float
    "Zero Sequence: Internal Conductance, G0"
    G1: float
    "Positive Sequence: Internal Conductance, G1"
    G2: float
    "Negative Sequence: Internal Conductance, G2"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Inom: float
    "Nominal Current"
    Ir: float
    "Rated Current"
    Irated: float
    "Harmonic Current Injections: Rated Current"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal"
    cDisplayName: str
    "Display Name"
    cTypHmc: str
    "Harmonic Current Injections: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    c_pmod: object
    "Model"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cosimModel: int
    "Used for Co-simulation"
    cosini: float
    "Positive Sequence: Power Factor"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dcurdf: float
    "Frequency Sweep Calculation only: Spectral Density of Current Magnitude"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dphidf: float
    "Frequency Sweep Calculation only: Spectral Density of Current Angle"
    fchardcur: object
    "Frequency Sweep Calculation only: Frequency Dependency"
    fchardphi: object
    "Frequency Sweep Calculation only: Frequency Dependency"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iSchemeStatus: int
    "Scheme Status"
    i_cap: int
    "Positive Sequence: Reactive Power:inductive:capacitive"
    icurref: int
    "Harmonic Current Injections: Harmonic currents referred to"
    isetp: float
    "Positive Sequence: Current Setpoint"
    isetp0: float
    "Zero Sequence: Current, Magnitude"
    isetp2: float
    "Negative Sequence: Current, Magnitude"
    leadFinput: int
    "Parameter event can be applied to: Frequency input:F0Hz (in Hz):f0 (in p.u.)"
    leadIinput: int
    "Parameter event can be applied to: Current input"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    nphase: int
    "No. of Phases:1:3"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    phisetp0: float
    "Zero Sequence: Current, Angle"
    phisetp2: float
    "Negative Sequence: Current, Angle"
    phmc: object
    "Harmonic Current Injections: Harmonic Currents"
    pid_: int
    "ProjectID"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    root_id: object
    "Original Location"
    sernum: str
    "Serial Number"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmLodlv(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    NrCust: int
    "Number of Customers"
    OptCost: int
    "Interruption costs: Unit"
    UtilFactor: float
    "Load per customer: Utilisation Factor"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal"
    cDisplayName: str
    "Display Name"
    cHasPartLod: int
    "Partial Loads Present"
    cNrCust: int
    "Load per customer: Number of Customers"
    cPartLod: list
    "Partial Loads:"
    cPmaxLV: float
    "Active power, P, with coincidence"
    cPrCust: float
    "Load per customer: P/Customer"
    cPsumLV: float
    "Resulting values: Active power, P, theoretical"
    cSav: float
    "Load per customer: Average Load"
    cSmax: float
    "Load per customer: Max. Load per Customer"
    cSmaxLV: float
    "Resulting values: Apparent power, S, with coincidence"
    cSsumLV: float
    "Resulting values: Apparent power, S, theoretical"
    cTrans: float
    "Load shedding/transfer (Transmission Option): Resulting"
    cUserDefIndex: int
    "User defined Index"
    ccosphi: float
    "Load per customer: Power Factor"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    classif: str
    "Load Classification:Agricultural:Domestic:Commercial:Industrial"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    coslini: float
    "Base Load: Power Factor, cos(phi)"
    coslini_a: float
    "cos(phi)(act.)"
    coslinir: float
    "Base Load Phase 1: Power Factor, cos(phi)"
    coslinir_a: float
    "Ph 1:cos(phi)(act.)"
    coslinis: float
    "Base Load Phase 2: Power Factor, cos(phi)"
    coslinis_a: float
    "Ph 2:cos(phi)(act.)"
    coslinit: float
    "Base Load Phase 3: Power Factor, cos(phi)"
    coslinit_a: float
    "Ph 3:cos(phi)(act.)"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cplinia: float
    "Base Load: P, Load"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    dudropLVfeed: float
    "LV Voltage Changes: Maximum Voltage Drop (LV Grid)"
    duriseLVfeed: float
    "LV Voltage Changes: Maximum Voltage Rise (LV Grid)"
    elini: float
    "Base Load: Yearly Energy"
    fSCDF: float
    "Interruption costs: Scaling factor"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iBaseIsMax: int
    "Individual power consumption: Use consumption as:Theoretical sum:Maximum per customer:Maximum with coincidence:Average (value for ginf)"
    iCoincFrom: int
    "Coincidence definition: Used coincidence definition:From type:Individual:None"
    iComDate: int
    "Commissioning Date"
    iLV: int
    "Coincidence definition: Consider coincidence"
    iSchemeStatus: int
    "Scheme Status"
    iShedding: int
    "Controls: Allow load shedding"
    i_prty: int
    "Priority"
    i_scale: int
    "Base Load: Adjusted by Load Scaling"
    i_scalep: int
    "Adjusted by Load Scaling"
    i_sym: int
    "Base Load: Balanced/Unbalanced:Balanced:Unbalanced"
    iintgnd: int
    "External Star Point"
    ilini: float
    "Base Load: Current, I"
    ilini_a: float
    "I(act.)"
    ilinir: float
    "Base Load Phase 1: Current, I"
    ilinir_a: float
    "Ph 1:I(act.)"
    ilinis: float
    "Base Load Phase 2: Current, I"
    ilinis_a: float
    "Ph 2:I(act.)"
    ilinit: float
    "Base Load Phase 3: Current, I"
    ilinit_a: float
    "Ph 3:I(act.)"
    indivPower: int
    "Individual power consumption"
    iopt_inp: int
    "Base Load: Input Mode"
    iopt_type: int
    "Allow Load-Ramp Event"
    isCtrlLdShed: int
    "Controls: Allow load shedding"
    loc_name: str
    "Name"
    lodparts: list
    "Partial Loads"
    nphase: int
    "No. of Phases:1:2:3"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pCoincDef: object
    "Coincidence definition: Individual coincidence definition"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pProfile: object
    "Base Load: Consumption Profile"
    pProfileRnd: float
    "Active Power for Probabilistic Analysis, P"
    pSCDF: object
    "Interruption costs: Tariff"
    pTrans: object
    "Load shedding/transfer (Transmission Option): Alternative Supply (Load)"
    pTypCoincDef: object
    "Coincidence definition: Coincidence definition from type"
    pcontract: float
    "Contracted Active Power"
    peakCorrFac: float
    "Individual power consumption: Additional scaling factor"
    pf_recap: int
    "Base Load: Power Factor:ind.:cap."
    pf_recapr: int
    "Base Load Phase 1: Power Factor:ind.:cap."
    pf_recaps: int
    "Base Load Phase 2: Power Factor:ind.:cap."
    pf_recapt: int
    "Base Load Phase 3: Power Factor:ind.:cap."
    phtech: int
    "Technology"
    pid_: int
    "ProjectID"
    plini: float
    "Base Load: Active Power, P"
    plini_a: float
    "P(act.)"
    plinir: float
    "Base Load Phase 1: Active Power, P"
    plinir_a: float
    "Ph 1:P(act.)"
    plinis: float
    "Base Load Phase 2: Active Power, P"
    plinis_a: float
    "Ph 2:P(act.)"
    plinit: float
    "Base Load Phase 3: Active Power, P"
    plinit_a: float
    "Ph 3:P(act.)"
    pnight: float
    "Night Storage Heater: P"
    pnight_a: float
    "P(night)(act.)"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    root_id: object
    "Original Location"
    scale0: float
    "Base Load: Scaling Factor"
    scale0_a: float
    "Scaling Factor(act.)"
    sernum: str
    "Serial Number"
    shed: int
    "Load shedding/transfer (Transmission Option): Shedding steps:infinite:1:2:3:4:5:6:7:8:9:10"
    shedcost: float
    "Costs: Costs for load shedding"
    shedmax: float
    "Constraints: Max. load shedding"
    shedmin: float
    "Constraints: Min. load shedding"
    slini: float
    "Base Load: Apparent Power, S"
    slini_a: float
    "S(act.)"
    slinir: float
    "Base Load Phase 1: Apparent Power, S"
    slinir_a: float
    "Ph 1:S(act.)"
    slinis: float
    "Base Load Phase 2: Apparent Power, S"
    slinis_a: float
    "Ph 2:S(act.)"
    slinit: float
    "Base Load Phase 3: Apparent Power, S"
    slinit_a: float
    "Ph 3:S(act.)"
    tid_: int
    "TimeID"
    trans: float
    "Load shedding/transfer (Transmission Option): Transferable"
    typ_id: object
    "Type"
    ulini: float
    "Base Load: Voltage, U(L-L)"
    ulini_a: float
    "U(L-L)(act.)"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmLodmv(PFGeneral):
    CCEarFr: float
    "Failures of Transformer Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures of Transformer Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures of Transformer Double Earth Fault: Repair duration"
    FOD: float
    "Failures of Transformer Transformer Failures: Forced Outage Duration"
    FOE: float
    "Failures of Transformer Transformer Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures of Transformer Transformer Failures: Forced Complete Outage Rate"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Iksfix: float
    "Fault Contribution Fixed Fault Contribution: Transient Short-Circuit Level"
    Iksgen: float
    "Fault Contribution Scalable Fault Contribution for Generation: Transient Short-Circuit Current"
    Ikslod: float
    "Fault Contribution Scalable Fault Contribution for Load: Transient Short-Circuit Current"
    Ikssfix: float
    "Fault Contribution Fixed Fault Contribution: Subtransient Short-Circuit Level"
    Ikssgen: float
    "Fault Contribution Scalable Fault Contribution for Generation: Subtransient Short-Circuit Current"
    Iksslod: float
    "Fault Contribution Scalable Fault Contribution for Load: Subtransient Short-Circuit Current"
    Inom: float
    "Nominal Current"
    Irated: float
    "Harmonic Current Injections: Rated Current"
    NrCust: int
    "Number of connected customers"
    Pcu: float
    "Series Reactor: Copper Losses"
    Sksfix: float
    "Fault Contribution Fixed Fault Contribution: Transient Short-Circuit Level"
    Sksgen: float
    "Fault Contribution Scalable Fault Contribution for Generation: Transient Short-Circuit Level"
    Skslod: float
    "Fault Contribution Scalable Fault Contribution for Load: Transient Short-Circuit Level"
    Skssfix: float
    "Fault Contribution Fixed Fault Contribution: Subtransient Short-Circuit Level"
    Skssgen: float
    "Fault Contribution Scalable Fault Contribution for Generation: Subtransient Short-Circuit Level"
    Sksslod: float
    "Fault Contribution Scalable Fault Contribution for Load: Subtransient Short-Circuit Level"
    Srated: float
    "Rated Power"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bus1: object
    "Terminal"
    cDisplayName: str
    "Display Name"
    cTrans: float
    "Load shedding/transfer (Transmission Option): Resulting"
    cTypHmc: str
    "Harmonic Current Injections: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    ci_sym: int
    "Balanced/Unbalanced"
    cimRdfId: list
    "RDF ID"
    classif: str
    "Load Classification:Agricultural:Domestic:Commercial:Industrial"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cosgini: float
    "Operating Point: cos(phi), Generation"
    cosgini_a: float
    "cos(phi)(act.), Gen."
    cosginir: float
    "Phase 1: cos(phi), Generation"
    cosginir_a: float
    "Ph 1:cos(phi)(act.), Gen."
    cosginis: float
    "Phase 2: cos(phi), Generation"
    cosginis_a: float
    "Ph 2:cos(phi)(act.), Gen."
    cosginit: float
    "Phase 3: cos(phi), Generation"
    cosginit_a: float
    "Ph 3:cos(phi)(act.), Gen."
    coslini: float
    "Operating Point: cos(phi), Load"
    coslini_a: float
    "cos(phi)(act.)"
    coslinir: float
    "Phase 1: cos(phi), Load"
    coslinir_a: float
    "Ph 1:cos(phi)(act.)"
    coslinis: float
    "Phase 2: cos(phi), Load"
    coslinis_a: float
    "Ph 2:cos(phi)(act.)"
    coslinit: float
    "Phase 3: cos(phi), Load"
    coslinit_a: float
    "Ph 3:cos(phi)(act.)"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteo: object
    "Meteo Station"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    cplinia: float
    "Operating Point: P, Load"
    csrated: float
    "Rated Power"
    ctotIks: float
    "Fault Contribution: Total Transient Fault Contribution"
    ctotIkss: float
    "Fault Contribution: Total Subtransient Fault Contribution"
    ctotSks: float
    "Fault Contribution: Total Transient Fault Contribution"
    ctotSkss: float
    "Fault Contribution: Total Subtransient Fault Contribution"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    dsdtemp: float
    "Temperature Gradient"
    dudropLVfeed: float
    "LV Voltage Changes: Maximum Voltage Drop (LV Grid)"
    dudropTrf: float
    "Voltage Change over Transformer: Transformer Voltage Drop in Consumption Case"
    duriseLVfeed: float
    "LV Voltage Changes: Maximum Voltage Rise (LV Grid)"
    duriseTrf: float
    "Voltage Change over Transformer: Transformer Voltage Rise in Production Case"
    elini: float
    "Operating Point: Yearly Energy"
    fSCDF: float
    "Interruption costs: Scaling factor"
    fcharr1: object
    "Norton Equivalent: Frequency-Dependence, r1(f)"
    fcharx1: object
    "Norton Equivalent: Frequency-Dependence, x1(f)"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    gscale: float
    "Operating Point: Generation Scaling Factor"
    gscale_a: float
    "Gen. Scaling Factor(act.)"
    iComDate: int
    "Commissioning Date"
    iSchemeStatus: int
    "Scheme Status"
    iShedding: int
    "Controls: Allow load shedding"
    i_csrc: int
    "Load Model"
    i_prty: int
    "Priority"
    i_pure: int
    "Load Model"
    i_scale: int
    "Operating Point: Adjusted by Load Scaling"
    i_sym: int
    "Balanced/Unbalanced"
    icurref: int
    "Harmonic Current Injections: Harmonic currents referred to"
    iopt_type: int
    "Allow Load-Ramp Event"
    iperfect: int
    "Failures of Transformer: Ideal component"
    isCtrlLdShed: int
    "Controls: Allow load shedding"
    loc_name: str
    "Name"
    mode_inp: str
    "Input Mode"
    nntap: int
    "Tap: Tap Position"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pMeteo: object
    "Meteo Station"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pProfile: object
    "Operating Point: Consumption Profile"
    pProfileRnd: float
    "Active Power for Probabilistic Analysis, P"
    pSCDF: object
    "Interruption costs: Tariff"
    pStoch: object
    "Failures of Transformer: Element model"
    pTrans: object
    "Load shedding/transfer (Transmission Option): Alternative Supply (Load)"
    pTypStoch: object
    "Failures of Transformer: Type model"
    pcontract: float
    "Contracted Active Power"
    pf_recap: int
    "Operating Point: cos(phi), Load:ind.:cap."
    pf_recapr: int
    "Phase 1: cos(phi), Load:ind.:cap."
    pf_recaps: int
    "Phase 2: cos(phi), Load:ind.:cap."
    pf_recapt: int
    "Phase 3: cos(phi), Load:ind.:cap."
    pfg_recap: int
    "Operating Point: cos(phi), Generation:ind.:cap."
    pfg_recapr: int
    "Phase 1: cos(phi), Generation:ind.:cap."
    pfg_recaps: int
    "Phase 2: cos(phi), Generation:ind.:cap."
    pfg_recapt: int
    "Phase 3: cos(phi), Generation:ind.:cap."
    pgini: float
    "Operating Point: P, Generation"
    pgini_a: float
    "Pgen(act.)"
    pginir: float
    "Phase 1: P, Generation"
    pginir_a: float
    "Ph 1:Pgen(act.)"
    pginis: float
    "Phase 2: P, Generation"
    pginis_a: float
    "Ph 2:Pgen(act.)"
    pginit: float
    "Phase 3: P, Generation"
    pginit_a: float
    "Ph 3:Pgen(act.)"
    pgrd: float
    "Capacitive/Inductive Reactive Power: QL/QC"
    phmc: object
    "Harmonic Current Injections: Harmonic Currents"
    phtech: str
    "Technology"
    pid_: int
    "ProjectID"
    plini: float
    "Operating Point: P, Load"
    plini_a: float
    "P(act.)"
    plinir: float
    "Phase 1: P, Load"
    plinir_a: float
    "Ph 1:P(act.)"
    plinis: float
    "Phase 2: P, Load"
    plinis_a: float
    "Ph 2:P(act.)"
    plinit: float
    "Phase 3: P, Load"
    plinit_a: float
    "Ph 3:P(act.)"
    qcq: float
    "Capacitive/Inductive Reactive Power: QC/Q"
    qdslCtrl: object
    "Quasi-Dynamic Model"
    r1hmc: float
    "Norton Equivalent: Resistance, r1"
    r2: float
    "Negative Sequence Impedance: Resistance r2"
    root_id: object
    "Original Location"
    rtox: float
    "Fault Contribution: R to X'' ratio"
    scale0: float
    "Operating Point: Load Scaling Factor"
    scale0_a: float
    "Scaling Factor(act.)"
    sernum: str
    "Serial Number"
    sgini: float
    "Operating Point: S, Generation"
    sgini_a: float
    "Sgen(act.)"
    sginir: float
    "Phase 1: S, Generation"
    sginir_a: float
    "Ph 1:Sgen(act.)"
    sginis: float
    "Phase 2: S, Generation"
    sginis_a: float
    "Ph 2:Sgen(act.)"
    sginit: float
    "Phase 3: S, Generation"
    sginit_a: float
    "Ph 3:Sgen(act.)"
    shed: int
    "Load shedding/transfer (Transmission Option): Shedding steps:infinite:1:2:3:4:5:6:7:8:9:10"
    shedcost: float
    "Costs: Costs for load shedding"
    shedmax: float
    "Constraints: Max. load shedding"
    shedmin: float
    "Constraints: Min. load shedding"
    slini: float
    "Operating Point: S, Load"
    slini_a: float
    "S(act.)"
    slinir: float
    "Phase 1: S, Load"
    slinir_a: float
    "Ph 1:S(act.)"
    slinis: float
    "Phase 2: S, Load"
    slinis_a: float
    "Ph 2:S(act.)"
    slinit: float
    "Phase 3: S, Load"
    slinit_a: float
    "Ph 3:S(act.)"
    tid_: int
    "TimeID"
    trans: float
    "Load shedding/transfer (Transmission Option): Transferable"
    typ_id: object
    "Type"
    uk: float
    "Series Reactor: Short Circuit Impedance"
    x1hmc: float
    "Norton Equivalent: Reactance, x1"
    x2: float
    "Negative Sequence Impedance: Reactance x2"
    xtor: float
    "Fault Contribution: X'' to R ratio"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmSind(PFGeneral):
    CCEarFr: float
    "Failures Double Earth Fault: Frequency of single earth faults"
    CCEarProb: float
    "Failures Double Earth Fault: Conditional probability of a second earth fault"
    CCEarRepMu: float
    "Failures Double Earth Fault: Repair duration"
    Curn: float
    "Ratings: Rated Current"
    FOD: float
    "Failures: Forced Outage Duration"
    FOE: float
    "Failures: Forced Outage Expectancy"
    FOR1: float
    "Failures: Forced Outage Rate"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Inom: float
    "Nominal Current"
    InomPre: float
    "Pre-fault nominal current"
    Lf: float
    "Frequency Dependencies: Inductance, L"
    Lf0: float
    "Frequency Dependencies: Inductance, L0"
    Lwidth: float
    "Hysteresis: Loop width"
    Pcu: float
    "Impedance: Copper Losses"
    PsiresA: float
    "Residual flux: Residual flux, ph. A"
    PsiresB: float
    "Residual flux: Residual flux, ph. B"
    PsiresC: float
    "Residual flux: Residual flux, ph. C"
    R0toR1: float
    "Zero sequence impedance: R0/R1 ratio"
    Rf: float
    "Frequency Dependencies: Resistance, R"
    Rf0: float
    "Frequency Dependencies: Resistance, R0"
    Sn: float
    "Ratings: Rated Power"
    X0toX1: float
    "Zero sequence impedance: X0/X1 ratio"
    Zd: float
    "Impedance: Impedance (absolute) Zd"
    aFrolich: float
    "Frolich equation coefficient a"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bFrolich: float
    "Frolich equation coefficient b"
    bus1: object
    "Terminal i"
    bus2: object
    "Terminal j"
    cDisplayName: str
    "Display Name"
    cFrolich: float
    "Frolich equation coefficient c"
    cPsiresC: float
    "Residual flux: Residual flux, ph. C"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    cknee: float
    "Knee Current"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    emtLinSig: int
    "Variable inductance/reactance via input signals"
    fcharL: object
    "Frequency Dependencies: L(f)"
    fcharL0: object
    "Frequency Dependencies: L0(f)"
    fcharR: object
    "Frequency Dependencies: R(f)"
    fcharR0: object
    "Frequency Dependencies: R0(f)"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iFinalSlope: int
    "Set final slope (peak values)"
    iFit: int
    "Data fitting:Piecewise linear:Frolich:Modified Frolich"
    iHyster: int
    "Hysteresis: Model:None:History Independent"
    iInterPol: int
    "Interpolation:spline:piecewise linear"
    iLimb: int
    "Core:&3&3 Limb:&5&5 Limb"
    iResFlux: int
    "Residual flux"
    iSchemeStatus: int
    "Scheme Status"
    iZoneBus: int
    "Zone"
    iperfect: int
    "Failures: Ideal component"
    itrmt: int
    "Type"
    ksat: int
    "Saturation Exponent"
    loc_name: str
    "Name"
    lossAssign: int
    "Loss assignment:according to grouping:uniformly distributed:to Terminal i:to Terminal j"
    lrea: float
    "Impedance: Inductance, L"
    manuf: str
    "Manufacturer"
    maxload: float
    "Thermal Loading Limit: Max. Loading"
    mseFrolich: float
    "Frolich equation, mean squared error"
    nphases: int
    "Phases:1:3"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pRating: object
    "Thermal Rating"
    pStoch: object
    "Failures: Element model"
    pid_: int
    "ProjectID"
    psi0: float
    "Knee Flux"
    root_id: object
    "Original Location"
    rrea: float
    "Impedance: Resistance, R"
    satcue: list
    "Current (RMS)"
    satcur: list
    "Current (peak)"
    satflux: list
    "Flux (peak)"
    satvol: list
    "Voltage (RMS)"
    sernum: str
    "Serial Number"
    smoothfac: float
    "Smoothing Factor"
    systp: int
    "System Type:AC:DC:AC/BI"
    tid_: int
    "TimeID"
    ucn: float
    "Ratings: Rated Voltage"
    uk: float
    "Impedance: Short-Circuit Voltage uk"
    ukr: float
    "Impedance: Short-Circuit Voltage (Re(uk)) ukr"
    xmair: float
    "Saturated Reactance"
    xrea: float
    "Impedance: Reactance, X"
    xreapu: float
    "Linear Reactance"
    xsatFrolich: float
    "Frolich equation saturated reactance (p.u.)"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmVsc(PFGeneral):
    Cdc: float
    "Cell capacitor"
    Cfilt: float
    "2nd-Harmonic Filter: Capacitance, Cfilt"
    Cvalve: float
    "Transistor/diode parameter: Snubber capacitance"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Gdoff: float
    "Antiparallel diodes: Off-conductance"
    Goff: float
    "Transistor/diode parameter: Off-conductance"
    Gvalve: float
    "Transistor/diode parameter: Snubber conductance"
    IkPFmax: float
    "Steady-state short-circuit current contribution: Maximum current"
    IkPFmin: float
    "Steady-state short-circuit current contribution: Minimum current"
    Iks: float
    "Fault contribution: Transient short-circuit current"
    Ikss: float
    "Max. fault contribution: Subtransient short-circuit current"
    Ikss1PF: float
    "Initial symmetrical short-circuit current contribution: Single-phase faults, Ik1PF"
    Ikss2PF: float
    "Initial symmetrical short-circuit current contribution: Two-phase faults, Ik2PF"
    Ikss3PF: float
    "Initial symmetrical short-circuit current contribution: Three-phase faults, Ik3PF"
    Inom: float
    "Nominal Current (AC)"
    Inomdc: float
    "Nominal Current (DC)"
    Irated: float
    "Harmonic source: Rated Current"
    K: float
    "DC-voltage dependent P-droop: K"
    Kd: float
    "Use integrated current controller: Kd: d-axis, proportional gain"
    Kfactor: float
    "Fault contribution: K factor"
    Kpart: float
    "Active power participation: Participation factor"
    Kpf: float
    "Prim. frequency bias"
    Kpphi: float
    "Angle difference dependent P-droop: Kpphi"
    Kq: float
    "Use integrated current controller: Kq: q-axis, proportional gain"
    Lac: float
    "Voltage source parameters: AC inductance"
    Larm: float
    "Arm reactor: Inductance, Larm"
    Ldc: float
    "Voltage source parameters: DC inductance"
    Lfilt: float
    "2nd-Harmonic Filter: Inductance, Lfilt"
    NmmcSM: int
    "Number of submodules per arm"
    P_max: float
    "Max."
    Pcu: float
    "Series reactor: Copper losses"
    Pmax_uc: float
    "Active power operational limits: Max."
    Pmin_uc: float
    "Active power operational limits: Min."
    Pmmax: float
    "Consider modulation index limit: Max. PWM factor"
    Pnold: float
    "Losses: No-load losses"
    Pnom: float
    "Active power operational limits: Pr(rated)"
    Qmax_a: float
    "Qmax(act.)"
    Qmin_a: float
    "Qmin(act.)"
    R0hmc: float
    "Norton equivalent: Resistance, R0h"
    R0toR1: float
    "Series reactor: R0/R1 ratio"
    R0toR1ac: float
    "Voltage source parameters: R0/R1 ratio"
    R1hmc: float
    "Norton equivalent: Resistance, R1h"
    R2hmc: float
    "Norton equivalent: Resistance, R2h"
    Rac: float
    "Voltage source parameters: AC resistance"
    Rarm: float
    "Arm reactor: Resistance, Rarm"
    Rdc: float
    "Voltage source parameters: DC resistance"
    Rdon: float
    "Antiparallel diodes: On-resistance"
    Ron: float
    "Transistor/diode parameter: On-resistance"
    Sks: float
    "Fault contribution: Transient short-circuit level"
    Skss: float
    "Max. fault contribution: Subtransient short-circuit level"
    Snom: float
    "Ratings: Rated power"
    Td: float
    "Use integrated current controller: Td: d-axis, integration time constant"
    Tdeadtime: float
    "Dead time"
    Tq: float
    "Use integrated current controller: Tq: q-axis, integration time constant"
    Tsampling: float
    "Sampling period"
    Unom: float
    "Ratings: Rated AC-voltage"
    Unomdc: float
    "Ratings: Rated DC-voltage (DC)"
    X0hmc: float
    "Norton equivalent: Reactance, X0h"
    X0toX1: float
    "Series reactor: X0/X1 ratio"
    X0toX1ac: float
    "Voltage source parameters: X0/X1 ratio"
    X1hmc: float
    "Norton equivalent: Reactance, X1h"
    X2hmc: float
    "Norton equivalent: Reactance, X2h"
    Xd: float
    "Commutation reactance"
    aCategory: str
    "Category"
    aSubCategory: str
    "Subcategory"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    busac: object
    "Terminal AC"
    busdm: object
    "Terminal DC-"
    busdp: object
    "Terminal DC+"
    cCategory: str
    "Category"
    cDisplayName: str
    "Display Name"
    cLarm1: float
    "2nd-Harmonic Filter: Inductance, Larm1"
    cQ_max: float
    "Reactive power limits: Max."
    cQ_min: float
    "Reactive power limits: Min."
    cSubCategory: str
    "Subcategory"
    cTypHmc: str
    "Harmonic source: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    c_pmod: object
    "Model"
    c_psecc: object
    "Ext. secondary controller"
    c_pstac: object
    "External station controller"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cictrltp: int
    "const.V:const.I:const.V (deprecated)"
    cimRdfId: list
    "RDF ID"
    commissionDate: str
    "Commissioning Date"
    considerPset: int
    "Angle difference dependent P-droop: Consider active power setpoint"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    ddroop: float
    "AC Voltage Droop: Droop"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fcharr0: object
    "Norton equivalent: Frequency-dependence, r0h(f)"
    fcharr1: object
    "Norton equivalent: Frequency-dependence, r1h(f)"
    fcharr2: object
    "Norton equivalent: Frequency-dependence, r2h(f)"
    fcharx0: object
    "Norton equivalent: Frequency-dependence, x0h(f)"
    fcharx1: object
    "Norton equivalent: Frequency-dependence, x1h(f)"
    fcharx2: object
    "Norton equivalent: Frequency-dependence, x2h(f)"
    fmod: float
    "Modulation frequency"
    fmodMmc: float
    "Modulation: Modulation frequency"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iArmFilt: int
    "2nd-Harmonic Filter"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iNoShcContr: int
    "No short-circuit contribution"
    iPpart: int
    "Active power participation"
    iPphidrp: int
    "Angle difference dependent P-droop"
    iQorient: int
    "Orientation:+P/Q flow:-P/Q flow"
    iSchemeStatus: int
    "Scheme Status"
    iShcModel: int
    "Short-circuit model:Equivalent synchronous machine:Dynamic voltage support:const.V:const.I:Full size converter"
    iThiPWM: int
    "Third harmonic injection"
    iVIsource: int
    "Independent AC and DC voltage/current source model"
    iVacMax: int
    "Consider modulation index limit"
    iWindGen: int
    "Wind generator model"
    iZarmDCside: int
    "Consider arm reactor on DC side"
    iZoneBus: int
    "Zone"
    i_acdc: int
    "Control mode:Vac-phi:Vdc-phi:PWM-phi:Vdc-Q:P-Vac:P-Q:Vdc-Vac:P-cos(phi):Vdc-cos(phi)"
    i_ctrl: int
    "Use integrated current controller"
    i_det: int
    "Model"
    i_mod: int
    "Modulation"
    iconfed: int
    "Static converter-fed drive"
    ictrltp: int
    "Model"
    icurref: int
    "Harmonic source: Harmonic currents referred to"
    idroop: int
    "DC-voltage dependent P-droop"
    imax: float
    "Fault contribution: Max. current"
    isCtrlFixedToLdfVal: int
    "Fix controls to Load Flow values"
    isCtrlP: int
    "Controls: Active Power"
    isCtrlQ: int
    "Controls: Reactive Power"
    isLimPmax: int
    "Active power operational limits: Max."
    isLimPmaxOPF: int
    "Active power operational limits: Max."
    isLimPmin: int
    "Active power operational limits: Min."
    isLimPminOPF: int
    "Active power operational limits: Min."
    isLimQmax: int
    "Reactive power limits: Max."
    isLimQmaxOPF: int
    "Reactive power limits: Max."
    isLimQmin: int
    "Reactive power limits: Min."
    isLimQminOPF: int
    "Reactive power limits: Min."
    isOpfCtrlP: int
    "Controls: Active Power"
    isOpfCtrlQ: int
    "Controls: Reactive Power"
    ivacdroop: int
    "AC-Voltage Droop:none:Q-Droop:Iq-Droop"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    mmcCmod: float
    "Submodule capacitance"
    mmcGcap: float
    "Capacitor parallel conductance"
    mmcModType: int
    "Modulation"
    mmcModel: int
    "MMC model:Controlled voltage source:Average value:Aggregate arm:Detailed equivalent circuit"
    nparnum: int
    "Number of: parallel converters"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pFlicker: object
    "Flicker coefficients"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pQlimType: object
    "Reactive power limits: Capability curve"
    pSubModel: object
    "Submodel"
    p_b1phiu: object
    "Angle difference dependent P-droop: Remote AC busbar"
    p_b2phiu: object
    "Angle difference dependent P-droop: Local AC busbar"
    p_pctrl: object
    "Controlled flow"
    p_pmeas: object
    "Active power participation: P(AC) measured at"
    p_uctrl: object
    "Controlled node (AC)"
    p_uctrldc: object
    "Controlled node (DC)"
    pblocktrf: object
    "Externally modelled unit transformer: Unit transformer"
    penaltyCosts: float
    "Penalty costs for redispatch"
    pf_recap: int
    "Power factor:ind.:cap."
    pfsetp: float
    "Power factor"
    phisetp: float
    "Phase setpoint"
    phmc: object
    "Harmonic source: Harmonic injections"
    phmcv: object
    "Harmonic source: Harmonic voltages"
    pid_: int
    "ProjectID"
    pmd_max: float
    "Upper limit of Pmd"
    pmd_min: float
    "Lower limit of Pmd"
    pmq_max: float
    "Upper limit of Pmq"
    pmq_min: float
    "Lower limit of Pmq"
    pmsetp: float
    "PWM factor"
    priority: int
    "Merit Order"
    psetp: float
    "Active power setpoint"
    psutype: str
    "Power station unit type"
    q_max: float
    "Reactive power limits: Max."
    q_min: float
    "Reactive power limits: Min."
    qsetp: float
    "Reactive power setpoint"
    r0: float
    "Additional zero sequence impedance: Resistance, r0"
    r0hmc: float
    "Norton equivalent: Resistance, r0h"
    r0iec: float
    "Zero sequence short-circuit impedance: Resistance, r0"
    r1hmc: float
    "Norton equivalent: Resistance, r1h"
    r2: float
    "Additional negative sequence impedance: Resistance, r2"
    r2hmc: float
    "Norton equivalent: Resistance, r2h"
    r2iec: float
    "Negative sequence short-circuit impedance: Resistance, r2"
    r2shc: float
    "Negative sequence short-circuit impedance: Resistance, r2"
    resLossFactor: float
    "Losses: Resistive loss factor"
    root_id: object
    "Original Location"
    rtox: float
    "Max. fault contribution: R to X'' ratio"
    sampling: int
    "Switch events:Precise crossing time:Fixed sampling period"
    scaleQmax: float
    "Reactive power limits: Scaling factor (max.)"
    scaleQmin: float
    "Reactive power limits: Scaling factor (min.)"
    searchBlockTrf: int
    "Externally modelled unit transformer"
    sernum: str
    "Serial Number"
    shcDeadband: int
    "Voltage deadband"
    swtLossFactor: float
    "Losses: Switching loss factor"
    tid_: int
    "TimeID"
    uDeadband: float
    "Voltage deadband: Deadband"
    uk: float
    "Series reactor: Short circuit impedance"
    usetp: float
    "AC voltage setpoint"
    usetpdc: float
    "DC voltage setpoint"
    usp_max: float
    "AC Voltage Droop Voltage setpoint limits: Max. voltage setpoint"
    usp_min: float
    "AC Voltage Droop Voltage setpoint limits: Min. voltage setpoint"
    vsctype: int
    "Converter type:Two-level converter:Half-bridge type MMC:Full-bridge type MMC"
    x0: float
    "Additional zero sequence impedance: Reactance, x0"
    x0hmc: float
    "Norton equivalent: Reactance, x0h"
    x0iec: float
    "Zero sequence short-circuit impedance: Reactance, x0"
    x1hmc: float
    "Norton equivalent: Reactance, x1h"
    x2: float
    "Additional negative sequence impedance: Reactance, x2"
    x2hmc: float
    "Norton equivalent: Reactance, x2h"
    x2iec: float
    "Negative sequence short-circuit impedance: Reactance, x2"
    x2shc: float
    "Negative sequence short-circuit impedance: Reactance, x2"
    xtor: float
    "Max. fault contribution: X'' to R ratio"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmVscmono(PFGeneral):
    Cdc: float
    "Cell capacitor"
    Cfilt: float
    "2nd-Harmonic Filter: Capacitance, Cfilt"
    Cvalve: float
    "Transistor/diode parameter: Snubber capacitance"
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Gdoff: float
    "Antiparallel diodes: Off-conductance"
    Goff: float
    "Transistor/diode parameter: Off-conductance"
    Gvalve: float
    "Transistor/diode parameter: Snubber conductance"
    IkPFmax: float
    "Steady-state short-circuit current contribution: Maximum current"
    IkPFmin: float
    "Steady-state short-circuit current contribution: Minimum current"
    Iks: float
    "Fault contribution: Transient short-circuit current"
    Ikss: float
    "Max. fault contribution: Subtransient short-circuit current"
    Ikss1PF: float
    "Initial symmetrical short-circuit current contribution: Single-phase faults, Ik1PF"
    Ikss2PF: float
    "Initial symmetrical short-circuit current contribution: Two-phase faults, Ik2PF"
    Ikss3PF: float
    "Initial symmetrical short-circuit current contribution: Three-phase faults, Ik3PF"
    Inom: float
    "Nominal Current (AC)"
    Inomdc: float
    "Nominal Current (DC)"
    Irated: float
    "Harmonic source: Rated Current"
    K: float
    "DC-voltage dependent P-droop: K"
    Kd: float
    "Use integrated current controller: Kd: d-axis, proportional gain"
    Kfactor: float
    "Fault contribution: K factor"
    Kpart: float
    "Active power participation: Participation factor"
    Kpf: float
    "Prim. frequency bias"
    Kpphi: float
    "Angle difference dependent P-droop: Kpphi"
    Kq: float
    "Use integrated current controller: Kq: q-axis, proportional gain"
    Lac: float
    "Voltage source parameters: AC inductance"
    Larm: float
    "Arm reactor: Inductance, Larm"
    Ldc: float
    "Voltage source parameters: DC inductance"
    Lfilt: float
    "2nd-Harmonic Filter: Inductance, Lfilt"
    NmmcSM: int
    "Number of submodules per arm"
    P_max: float
    "Max."
    Pcu: float
    "Series reactor: Copper losses"
    Pmax_uc: float
    "Active power operational limits: Max."
    Pmin_uc: float
    "Active power operational limits: Min."
    Pmmax: float
    "Consider modulation index limit: Max. PWM factor"
    Pnold: float
    "Losses: No-load losses"
    Pnom: float
    "Active power operational limits: Pr(rated)"
    Qmax_a: float
    "Qmax(act.)"
    Qmin_a: float
    "Qmin(act.)"
    R0hmc: float
    "Norton equivalent: Resistance, R0h"
    R0toR1: float
    "Series reactor: R0/R1 ratio"
    R0toR1ac: float
    "Voltage source parameters: R0/R1 ratio"
    R1hmc: float
    "Norton equivalent: Resistance, R1h"
    R2hmc: float
    "Norton equivalent: Resistance, R2h"
    Rac: float
    "Voltage source parameters: AC resistance"
    Rarm: float
    "Arm reactor: Resistance, Rarm"
    Rdc: float
    "Voltage source parameters: DC resistance"
    Rdon: float
    "Antiparallel diodes: On-resistance"
    Ron: float
    "Transistor/diode parameter: On-resistance"
    Sks: float
    "Fault contribution: Transient short-circuit level"
    Skss: float
    "Max. fault contribution: Subtransient short-circuit level"
    Snom: float
    "Ratings: Rated power"
    Td: float
    "Use integrated current controller: Td: d-axis, integration time constant"
    Tdeadtime: float
    "Dead time"
    Tq: float
    "Use integrated current controller: Tq: q-axis, integration time constant"
    Tsampling: float
    "Sampling period"
    Unom: float
    "Ratings: Rated AC-voltage"
    Unomdc: float
    "Ratings: Rated DC-voltage (DC)"
    X0hmc: float
    "Norton equivalent: Reactance, X0h"
    X0toX1: float
    "Series reactor: X0/X1 ratio"
    X0toX1ac: float
    "Voltage source parameters: X0/X1 ratio"
    X1hmc: float
    "Norton equivalent: Reactance, X1h"
    X2hmc: float
    "Norton equivalent: Reactance, X2h"
    Xd: float
    "Commutation reactance"
    aCategory: str
    "Category"
    aSubCategory: str
    "Subcategory"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    busac: object
    "Terminal AC"
    busdc: object
    "Terminal DC"
    cCategory: str
    "Category"
    cDisplayName: str
    "Display Name"
    cLarm1: float
    "2nd-Harmonic Filter: Inductance, Larm1"
    cQ_max: float
    "Reactive power limits: Max."
    cQ_min: float
    "Reactive power limits: Min."
    cSubCategory: str
    "Subcategory"
    cTypHmc: str
    "Harmonic source: Type of Harmonic Sources"
    cUserDefIndex: int
    "User defined Index"
    c_pmod: object
    "Model"
    c_psecc: object
    "Ext. secondary controller"
    c_pstac: object
    "External station controller"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cictrltp: int
    "const.V:const.I:const.V (deprecated)"
    cimRdfId: list
    "RDF ID"
    commissionDate: str
    "Commissioning Date"
    considerPset: int
    "Angle difference dependent P-droop: Consider active power setpoint"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    ddroop: float
    "AC Voltage Droop: Droop"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fcharr0: object
    "Norton equivalent: Frequency-dependence, r0h(f)"
    fcharr1: object
    "Norton equivalent: Frequency-dependence, r1h(f)"
    fcharr2: object
    "Norton equivalent: Frequency-dependence, r2h(f)"
    fcharx0: object
    "Norton equivalent: Frequency-dependence, x0h(f)"
    fcharx1: object
    "Norton equivalent: Frequency-dependence, x1h(f)"
    fcharx2: object
    "Norton equivalent: Frequency-dependence, x2h(f)"
    fmod: float
    "Modulation frequency"
    fmodMmc: float
    "Modulation: Modulation frequency"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iArmFilt: int
    "2nd-Harmonic Filter"
    iAstabint: int
    "A-stable integration algorithm"
    iComDate: int
    "Commissioning Date"
    iNoShcContr: int
    "No short-circuit contribution"
    iPpart: int
    "Active power participation"
    iPphidrp: int
    "Angle difference dependent P-droop"
    iQorient: int
    "Orientation:+P/Q flow:-P/Q flow"
    iSchemeStatus: int
    "Scheme Status"
    iShcModel: int
    "Short-circuit model:Equivalent synchronous machine:Dynamic voltage support:const.V:const.I:Full size converter"
    iThiPWM: int
    "Third harmonic injection"
    iVIsource: int
    "Independent AC and DC voltage/current source model"
    iVacMax: int
    "Consider modulation index limit"
    iWindGen: int
    "Wind generator model"
    iZarmDCside: int
    "Consider arm reactor on DC side"
    iZoneBus: int
    "Zone"
    i_acdc: int
    "Control mode:Vac-phi:Vdc-phi:PWM-phi:Vdc-Q:P-Vac:P-Q:Vdc-Vac:P-cos(phi):Vdc-cos(phi)"
    i_ctrl: int
    "Use integrated current controller"
    i_det: int
    "Model"
    i_mod: int
    "Modulation"
    iconfed: int
    "Static converter-fed drive"
    ictrltp: int
    "Model"
    icurref: int
    "Harmonic source: Harmonic currents referred to"
    idroop: int
    "DC-voltage dependent P-droop"
    imax: float
    "Fault contribution: Max. current"
    isCtrlFixedToLdfVal: int
    "Fix controls to Load Flow values"
    isCtrlP: int
    "Controls: Active Power"
    isCtrlQ: int
    "Controls: Reactive Power"
    isLimPmax: int
    "Active power operational limits: Max."
    isLimPmaxOPF: int
    "Active power operational limits: Max."
    isLimPmin: int
    "Active power operational limits: Min."
    isLimPminOPF: int
    "Active power operational limits: Min."
    isLimQmax: int
    "Reactive power limits: Max."
    isLimQmaxOPF: int
    "Reactive power limits: Max."
    isLimQmin: int
    "Reactive power limits: Min."
    isLimQminOPF: int
    "Reactive power limits: Min."
    isOpfCtrlP: int
    "Controls: Active Power"
    isOpfCtrlQ: int
    "Controls: Reactive Power"
    ivacdroop: int
    "AC-Voltage Droop:none:Q-Droop:Iq-Droop"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    mmcCmod: float
    "Submodule capacitance"
    mmcGcap: float
    "Capacitor parallel conductance"
    mmcModType: int
    "Modulation"
    mmcModel: int
    "MMC model:Controlled voltage source:Average value:Aggregate arm:Detailed equivalent circuit"
    nparnum: int
    "Number of: parallel converters"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pFlicker: object
    "Flicker coefficients"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pQlimType: object
    "Reactive power limits: Capability curve"
    pSubModel: object
    "Submodel"
    p_b1phiu: object
    "Angle difference dependent P-droop: Remote AC busbar"
    p_b2phiu: object
    "Angle difference dependent P-droop: Local AC busbar"
    p_pctrl: object
    "Controlled flow"
    p_pmeas: object
    "Active power participation: P(AC) measured at"
    p_uctrl: object
    "Controlled node (AC)"
    p_uctrldc: object
    "Controlled node (DC)"
    pblocktrf: object
    "Externally modelled unit transformer: Unit transformer"
    penaltyCosts: float
    "Penalty costs for redispatch"
    pf_recap: int
    "Power factor:ind.:cap."
    pfsetp: float
    "Power factor"
    phisetp: float
    "Phase setpoint"
    phmc: object
    "Harmonic source: Harmonic injections"
    phmcv: object
    "Harmonic source: Harmonic voltages"
    pid_: int
    "ProjectID"
    pmd_max: float
    "Upper limit of Pmd"
    pmd_min: float
    "Lower limit of Pmd"
    pmq_max: float
    "Upper limit of Pmq"
    pmq_min: float
    "Lower limit of Pmq"
    pmsetp: float
    "PWM factor"
    priority: int
    "Merit Order"
    psetp: float
    "Active power setpoint"
    psutype: str
    "Power station unit type"
    q_max: float
    "Reactive power limits: Max."
    q_min: float
    "Reactive power limits: Min."
    qsetp: float
    "Reactive power setpoint"
    r0: float
    "Additional zero sequence impedance: Resistance, r0"
    r0hmc: float
    "Norton equivalent: Resistance, r0h"
    r0iec: float
    "Zero sequence short-circuit impedance: Resistance, r0"
    r1hmc: float
    "Norton equivalent: Resistance, r1h"
    r2: float
    "Additional negative sequence impedance: Resistance, r2"
    r2hmc: float
    "Norton equivalent: Resistance, r2h"
    r2iec: float
    "Negative sequence short-circuit impedance: Resistance, r2"
    r2shc: float
    "Negative sequence short-circuit impedance: Resistance, r2"
    resLossFactor: float
    "Losses: Resistive loss factor"
    root_id: object
    "Original Location"
    rtox: float
    "Max. fault contribution: R to X'' ratio"
    sampling: int
    "Switch events:Precise crossing time:Fixed sampling period"
    scaleQmax: float
    "Reactive power limits: Scaling factor (max.)"
    scaleQmin: float
    "Reactive power limits: Scaling factor (min.)"
    searchBlockTrf: int
    "Externally modelled unit transformer"
    sernum: str
    "Serial Number"
    shcDeadband: int
    "Voltage deadband"
    swtLossFactor: float
    "Losses: Switching loss factor"
    tid_: int
    "TimeID"
    uDeadband: float
    "Voltage deadband: Deadband"
    uk: float
    "Series reactor: Short circuit impedance"
    usetp: float
    "AC voltage setpoint"
    usetpdc: float
    "DC voltage setpoint"
    usp_max: float
    "AC Voltage Droop Voltage setpoint limits: Max. voltage setpoint"
    usp_min: float
    "AC Voltage Droop Voltage setpoint limits: Min. voltage setpoint"
    vsctype: int
    "Converter type:Two-level converter:Half-bridge type MMC:Full-bridge type MMC"
    x0: float
    "Additional zero sequence impedance: Reactance, x0"
    x0hmc: float
    "Norton equivalent: Reactance, x0h"
    x0iec: float
    "Zero sequence short-circuit impedance: Reactance, x0"
    x1hmc: float
    "Norton equivalent: Reactance, x1h"
    x2: float
    "Additional negative sequence impedance: Reactance, x2"
    x2hmc: float
    "Norton equivalent: Reactance, x2h"
    x2iec: float
    "Negative sequence short-circuit impedance: Reactance, x2"
    x2shc: float
    "Negative sequence short-circuit impedance: Reactance, x2"
    xtor: float
    "Max. fault contribution: X'' to R ratio"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ElmZpu(PFGeneral):
    GPSlat: float
    "Geographical Position: Latitude / Northing"
    GPSlon: float
    "Geographical Position: Longitude / Easting"
    Sn: float
    "Rated Power"
    ag: float
    "Transformer Equivalent: Additional Phase Shift"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bi0_pu: float
    "Zero-Sequence conductance and susceptance: Susceptance i"
    bi0s_pu: float
    "Zero-Sequence conductance and susceptance: Susceptance i"
    bi2_pu: float
    "Negative-Sequence conductance and susceptance: Susceptance i"
    bi2s_pu: float
    "Negative-Sequence conductance and susceptance: Susceptance i"
    bi_pu: float
    "Positive-Sequence conductance and susceptance: Susceptance i"
    bis_pu: float
    "Positive-Sequence conductance and susceptance: Susceptance i"
    bj0_pu: float
    "Zero-Sequence conductance and susceptance: Susceptance j"
    bj0s_pu: float
    "Zero-Sequence conductance and susceptance: Susceptance j"
    bj2_pu: float
    "Negative-Sequence conductance and susceptance: Susceptance j"
    bj2s_pu: float
    "Negative-Sequence conductance and susceptance: Susceptance j"
    bj_pu: float
    "Positive-Sequence conductance and susceptance: Susceptance j"
    bjs_pu: float
    "Positive-Sequence conductance and susceptance: Susceptance j"
    bus1: object
    "Terminal i"
    bus2: object
    "Terminal j"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cimRdfId: list
    "RDF ID"
    commissionDate: str
    "Commissioning Date"
    constr: int
    "Year of Construction"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    dpl1: float
    "dpl1"
    dpl2: float
    "dpl2"
    dpl3: float
    "dpl3"
    dpl4: float
    "dpl4"
    dpl5: float
    "dpl5"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gi0_pu: float
    "Zero-Sequence conductance and susceptance: Conductance i"
    gi0s_pu: float
    "Zero-Sequence conductance and susceptance: Conductance i"
    gi2_pu: float
    "Negative-Sequence conductance and susceptance: Conductance i"
    gi2s_pu: float
    "Negative-Sequence conductance and susceptance: Conductance i"
    gi_pu: float
    "Positive-Sequence conductance and susceptance: Conductance i"
    gis_pu: float
    "Positive-Sequence conductance and susceptance: Conductance i"
    gj0_pu: float
    "Zero-Sequence conductance and susceptance: Conductance j"
    gj0s_pu: float
    "Zero-Sequence conductance and susceptance: Conductance j"
    gj2_pu: float
    "Negative-Sequence conductance and susceptance: Conductance j"
    gj2s_pu: float
    "Negative-Sequence conductance and susceptance: Conductance j"
    gj_pu: float
    "Positive-Sequence conductance and susceptance: Conductance j"
    gjs_pu: float
    "Positive-Sequence conductance and susceptance: Conductance j"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAreaBus: int
    "Area"
    iCapParallel: int
    "Consider resistive and capacitive parts in parallel"
    iComDate: int
    "Commissioning Date"
    iFreZ: int
    "Use Frequency Related Impedance for X/R Ratio Calculation"
    iSchemeStatus: int
    "Scheme Status"
    iZoneBus: int
    "Zone"
    iZshc: int
    "Use same impedance as for load flow"
    iequalz: int
    "Use equal Impedances (zij = zji)"
    iy2eqy1: int
    "Use Admittance y2 = y1"
    iy2eqy1s: int
    "Use Admittance y2 = y1"
    iz2eqz1: int
    "Use Impedance z2 = z1"
    iztreqz: int
    "Transient = Subtransient Impedance"
    loc_name: str
    "Name"
    manuf: str
    "Manufacturer"
    matZ: list
    "Frequency related impedances i->j (Positive, Negative and Zero sequence)"
    matZ1: list
    "Frequency related impedances j->i (Positive, Negative and Zero sequence)"
    nphases: int
    "Phases:1:3"
    nphshift: int
    "Transformer Equivalent: Nominal Phase Shift"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pOperator: object
    "Operator"
    pOwner: object
    "Owner"
    pid_: int
    "ProjectID"
    r0_pu: float
    "Zero-Sequence Impedance i-j: Real Part"
    r0_pu_ji: float
    "Zero-Sequence Impedance j-i: Real Part"
    r0s_pu: float
    "Zero-Sequence Impedance i-j: Real Part"
    r0s_pu_ji: float
    "Zero-Sequence Impedance j-i: Real Part"
    r2_pu: float
    "Negative-Sequence Impedance i-j: Real Part"
    r2_pu_ji: float
    "Negative-Sequence Impedance j-i: Real Part"
    r2s_pu: float
    "Negative-Sequence Impedance i-j: Real Part"
    r2s_pu_ji: float
    "Negative-Sequence Impedance j-i: Real Part"
    r_pu: float
    "Positive-Sequence Impedance i-j: Real Part"
    r_pu_ji: float
    "Positive-Sequence Impedance j-i: Real Part"
    root_id: object
    "Original Location"
    rs_pu: float
    "Subtransient Positive-Sequence Impedance i-j: Real Part"
    rs_pu_ji: float
    "Subtransient Positive-Sequence Impedance j-i: Real Part"
    rstr_pu: float
    "Transient Positive-Sequence Impedance i-j: Real Part"
    rstr_pu_ji: float
    "Transient Positive-Sequence Impedance j-i: Real Part"
    sernum: str
    "Serial Number"
    tid_: int
    "TimeID"
    uratio: float
    "Transformer Equivalent: Tap Ratio"
    x0_pu: float
    "Zero-Sequence Impedance i-j: Imaginary Part"
    x0_pu_ji: float
    "Zero-Sequence Impedance j-i: Imaginary Part"
    x0s_pu: float
    "Zero-Sequence Impedance i-j: Imaginary Part"
    x0s_pu_ji: float
    "Zero-Sequence Impedance j-i: Imaginary Part"
    x2_pu: float
    "Negative-Sequence Impedance i-j: Imaginary Part"
    x2_pu_ji: float
    "Negative-Sequence Impedance j-i: Imaginary Part"
    x2s_pu: float
    "Negative-Sequence Impedance i-j: Imaginary Part"
    x2s_pu_ji: float
    "Negative-Sequence Impedance j-i: Imaginary Part"
    x_pu: float
    "Positive-Sequence Impedance i-j: Imaginary Part"
    x_pu_ji: float
    "Positive-Sequence Impedance j-i: Imaginary Part"
    xs_pu: float
    "Subtransient Positive-Sequence Impedance i-j: Imaginary Part"
    xs_pu_ji: float
    "Subtransient Positive-Sequence Impedance j-i: Imaginary Part"
    xstr_pu: float
    "Transient Positive-Sequence Impedance i-j: Imaginary Part"
    xstr_pu_ji: float
    "Transient Positive-Sequence Impedance j-i: Imaginary Part"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class StaPll(PFGeneral):
    Ki: float
    "PI integration gain"
    Kp: float
    "PI proportional gain"
    Ksogi: float
    "SOGI proportional gain"
    T1: float
    "Low-pass filter time constant"
    bw: float
    "Notch filter for oscillations at double nominal angular frequency: Bandwidth"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fmax: float
    "Upper frequency limit"
    fmin: float
    "Lower frequency limit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iSchemeStatus: int
    "Scheme Status"
    i_block: int
    "Voltage dependent blocking"
    i_dw: int
    "Voltage dependent blocking: Set the angular frequency deviation to zero when blocked"
    i_model: int
    "PLL based on:SRF:SOGI/DSOGI"
    i_norm: int
    "Input voltage normalisation"
    i_notch: int
    "Notch filter for oscillations at double nominal angular frequency"
    loc_name: str
    "Name"
    measuredPh: int
    "Measured phase:a:b:c:a-n:b-n:c-n"
    nphase: int
    "No. of phases:1:3"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pbusbar: object
    "Measurement point"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"
    umin: float
    "Voltage dependent blocking: Blocking voltage"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class TypSym(PFGeneral):
    Ikd: float
    "Steady-state shc. current: Ikd"
    J: float
    "Inertia: Moment of inertia J"
    Q_max: float
    "Reactive power limits: Maximum value"
    Q_min: float
    "Reactive power limits: Minimum value"
    Tcold: float
    "Stall time: Cold"
    Tdc: float
    "Time constants: Tdc"
    Thot: float
    "Stall time: Hot"
    Tinrush: float
    "Inrush peak current: Max. time"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bname: str
    "bus name (only for compatib.)"
    cTdc: float
    "Time constants: Tdc"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cosn: float
    "Rated power factor"
    cpHeadFold: object
    "Head Folder"
    curTab: list
    "Stator leakage reactance: Current"
    curk: float
    "Steady-state shc. current: 3-phase Ik3p"
    curk1p: float
    "Steady-state shc. current: 1-phase Ik1p"
    curk2p: float
    "Steady-state shc. current: 2-phase Ik2p"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    depSmoothFac: float
    "Stator leakage reactance: Dependency curve smoothing factor"
    desc: list
    "Description"
    dkd: float
    "Damping torque coefficient"
    doc_id: object
    "Additional Data"
    dpe: float
    "Damping torque coefficient based on power"
    dpu: float
    "Turbine shaft friction torque coefficient"
    fcharl0: object
    "Zero sequence data: l0(f)"
    fcharl2: object
    "Negative sequence data: l2(f)"
    fcharlss: object
    "Subtransient reactances: l''(f)"
    fcharr0: object
    "Zero sequence data: r0(f)"
    fcharr2: object
    "Negative sequence data: r2(f)"
    fcharrstr: object
    "Stator resistance: rs(f)"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    frequ: float
    "Inertia: Nominal frequency"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    h: float
    "Inertia: Inertia constant H (rated to Sgn)"
    hpn: float
    "Inertia: Inertia constant H (rated to Pgn)"
    iSchemeStatus: int
    "Scheme Status"
    iTdcManual: int
    "Time constants: Enter Tdc manually"
    i_exactConv: int
    "Exact conversion of time constants"
    i_extModel: int
    "Model"
    i_speedD: int
    "Speed deviation based on"
    i_speedVar: int
    "Effect of speed variation"
    i_trans: int
    "Use frequency transfer functions"
    i_xl: int
    "Stator parameters: xl is current dependent"
    i_xme2: int
    "Consider negative sequence torque"
    iamort: int
    "with amortisseur windings"
    ifd: list
    "Saturation parameter: ie"
    ifdq: list
    "Saturation parameter: ie"
    iinrush: float
    "Inrush peak current: Ratio Ip/In"
    iner_inp: str
    "Inertia: Input mode"
    iopt_data: int
    "Input parameters"
    isat: int
    "Main flux saturation:&0&No saturation:&1&Quadratic (SG10/SG12):&3&Exponential (SG10/SG12):&2&Tabular input"
    isatSalient: int
    "Saturation:d- and q-axis (flux magnitude):d-axis (flux magnitude):d- and q-axis (flux components):d-axis (flux component, d-axis)"
    iturbo: int
    "Rotor type"
    iuseXdk: int
    "Steady-state shc. current: Ik instead of reactances"
    iusesat: int
    "Subtransient reactances: Use saturated value"
    loc_name: str
    "Name"
    lss: float
    "Subtransient reactances: l''"
    manuf: str
    "Manufacturer"
    model_inp: str
    "Model"
    nphase: int
    "No. of phases:1:3"
    nslty: int
    "Connection:D:Y:YN"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    polepairs: int
    "Inertia: No. of pole pairs"
    psim: float
    "Permanent magnet: Rotor flux"
    q_max: float
    "Reactive power limits: Maximum value"
    q_min: float
    "Reactive power limits: Minimum value"
    r0sy: float
    "Zero sequence data: Resistance r0"
    r1d: float
    "Rotor d-axis parameters: r1d"
    r1de: float
    "Rotor d-axis parameters: r1de"
    r1q: float
    "Rotor q-axis parameters: r1q"
    r1qe: float
    "Rotor q-axis parameters: r1qe"
    r2d: float
    "Rotor d-axis parameters: r2d"
    r2q: float
    "Rotor q-axis parameters: r2q"
    r2sy: float
    "Negative sequence data: Resistance r2"
    r3q: float
    "Rotor q-axis parameters: r3q"
    rfd: float
    "Rotor d-axis parameters: rfd"
    rfde: float
    "Rotor d-axis parameters: rfde"
    rgf: float
    "Fictitious resistance"
    root_id: object
    "Original Location"
    rstr: float
    "Stator parameters: rstr"
    satse: list
    "Saturation parameter: SG(u)"
    satseq: list
    "Saturation parameter: SG(u)"
    satur: int
    "For single fed short-circuit: Machine type IEC909/IEC60909"
    satv: list
    "Saturation parameter: Term. voltage"
    satvq: list
    "Saturation parameter: Term. voltage"
    sg10: float
    "Saturation parameter: SG10"
    sg10q: float
    "Saturation parameter: SG10 q-axis"
    sg12: float
    "Saturation parameter: SG12"
    sg12q: float
    "Saturation parameter: SG12 q-axis"
    sgn: float
    "Rated apparent power"
    slipmin: float
    "Threshold for slip dependency: Minimum slip"
    smoothFac: float
    "Saturation parameter: Smoothing factor"
    t1d: float
    "d-axis time constants: t1d"
    t1q: float
    "q-axis time constants: t1q"
    t2d: float
    "d-axis time constants: t2d"
    t2q: float
    "q-axis time constants: t2q"
    t3d: float
    "d-axis time constants: t3d"
    t3q: float
    "q-axis time constants: t3q"
    t4d: float
    "d-axis time constants: t4d"
    t4q: float
    "q-axis time constants: t4q"
    t5d: float
    "d-axis time constants: t5d"
    t5q: float
    "q-axis time constants: t5q"
    t6d: float
    "d-axis time constants: t6d"
    t6q: float
    "q-axis time constants: t6q"
    t7d: float
    "d-axis time constants: t7d"
    t8d: float
    "d-axis time constants: t8d"
    tag: float
    "Inertia: Acceleration time const. Tag (rated to Pgn)"
    tags: float
    "Inertia: Acceleration time const. Tag (rated to Sgn)"
    tds: float
    "Transient time constants: Td'"
    tds0: float
    "Transient time constants: Td0'"
    tdss: float
    "Subtransient time constants: Td''"
    tdss0: float
    "Subtransient time constants: Td0''"
    tid_: int
    "TimeID"
    tqs: float
    "Transient time constants: Tq'"
    tqs0: float
    "Transient time constants: Tq0'"
    tqss: float
    "Subtransient time constants: Tq''"
    tqss0: float
    "Subtransient time constants: Tq0''"
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"
    ugn: float
    "Rated voltage"
    x0sy: float
    "Zero sequence data: Reactance x0"
    x1d: float
    "Rotor d-axis parameters: x1d"
    x1dc: float
    "Rotor d-axis parameters: x1dc"
    x1de: float
    "Rotor d-axis parameters: x1de"
    x1q: float
    "Rotor q-axis parameters: x1q"
    x1qc: float
    "Rotor q-axis parameters: x1qc"
    x1qe: float
    "Rotor q-axis parameters: x1qe"
    x2d: float
    "Rotor d-axis parameters: x2d"
    x2q: float
    "Rotor q-axis parameters: x2q"
    x2sy: float
    "Negative sequence data: Reactance x2"
    x3q: float
    "Rotor q-axis parameters: x3q"
    xad: float
    "Mutual reactances: xad"
    xaq: float
    "Mutual reactances: xaq"
    xd: float
    "Synchronous reactances: xd"
    xds: float
    "Transient reactances: xd'"
    xdsat: float
    "For single fed short-circuit: Reciprocal of short-circuit ratio (xdsat)"
    xdss: float
    "Subtransient reactances: xd''"
    xdsss: float
    "Subtransient reactance: saturated value xd''sat"
    xfd: float
    "Rotor d-axis parameters: xfd"
    xfde: float
    "Rotor d-axis parameters: xfde"
    xl: float
    "Stator parameters: xl"
    xlTab: list
    "Stator leakage reactance: xl"
    xq: float
    "Synchronous reactances: xq"
    xqs: float
    "Transient reactances: xq'"
    xqss: float
    "Subtransient reactances: xq''"
    xrl: float
    "Rotor mutual reactances: xrld"
    xrl2d: float
    "Rotor d-axis parameters: xrl2d"
    xrlq: float
    "Rotor mutual reactances: xrlq"
    xstr: float
    "xstr"
    xtor: float
    "Stator resistance: Ratio X/R"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class TypLod(PFGeneral):
    Prp: float
    "Static portion"
    aP: float
    "Voltage dependence P: Coefficient aP"
    aQ: float
    "Voltage dependence of Q: Coefficient aQ"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    bP: float
    "Voltage dependence P: Coefficient bP"
    bQ: float
    "Voltage dependence of Q: Coefficient bQ"
    cP: float
    "Voltage dependence P: Coefficient cP"
    cQ: float
    "Voltage dependence of Q: Coefficient cQ"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cloddy: int
    "Percentage: Dynamic"
    clodst: int
    "Percentage: Static (const z)"
    cnm: str
    "Connection:YN:D"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    doc_id: object
    "Additional Data"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    i_csrc: int
    "Load model"
    i_nln: int
    "Model dependence:&0&Linear:&1&Nonlinear voltage, linear frequency:&2&Nonlinear:&3&Nonlinear, regulated"
    i_pure: int
    "Load model"
    iintgnd: int
    "External star point"
    kpf: float
    "Frequency dependence: Coefficient kpf"
    kpu: float
    "Voltage dependence P: Exponent e_cP"
    kpu0: float
    "Voltage dependence P: Exponent e_aP"
    kpu1: float
    "Voltage dependence P: Exponent e_bP"
    kqf: float
    "Frequency dependence: Coefficient kqf"
    kqu: float
    "Voltage dependence of Q: Exponent e_cQ"
    kqu0: float
    "Voltage dependence of Q: Exponent e_aQ"
    kqu1: float
    "Voltage dependence of Q: Exponent e_bQ"
    loc_name: str
    "Name"
    loddy: int
    "Percentage: Dynamic"
    lodst: int
    "Percentage: Static (const Z)"
    manuf: str
    "Manufacturer"
    nlnph: int
    "Phases:1:2:3"
    oid_: int
    "ObjectID"
    pfc: float
    "Power factor correction"
    pgrd: float
    "Capacitive/Inductive reactive power: QL/QC"
    phtech: int
    "Technology"
    pid_: int
    "ProjectID"
    qcq: float
    "Capacitive/Inductive reactive power: QC/Q"
    root_id: object
    "Original Location"
    systp: int
    "System type:AC:DC"
    t1: float
    "Time constants: Delay"
    tid_: int
    "TimeID"
    tpf: float
    "Time constants: P frequency dep."
    tpu: float
    "Time constants: P voltage dep."
    tqf: float
    "Time constants: Q frequency dep."
    tqu: float
    "Time constants: Q voltage dep."
    typemetadata_changeLog: list
    "Change Log"
    typemetadata_key: list
    "Type Key"
    typemetadata_version: list
    "Version"
    udmax: float
    "Voltage limits: Upper"
    udmin: float
    "Voltage limits: Lower"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class BlkSlot(PFGeneral):
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    element: object
    "Element"
    filtmod: str
    "Filter for: Class Name"
    filtnam: str
    "Filter for: Model Name"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    isAutom: int
    "Classification: Automatic, model will be created"
    isLinear: int
    "Classification: Linear"
    isLocal: int
    "Classification: Local, model must be stored inside"
    isMain: int
    "Classification: Main Slot"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Sequence"
    outserv: int
    "Out of Service"
    pDsl: object
    "Type"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sInput: list
    "Variables: Input Signals"
    sLowLimInp: list
    "Lower Limitation: Limiting Input Signals"
    sOutput: list
    "Variables: Output Signals"
    sUpLimInp: list
    "Upper Limitation: Limiting Input Signals"
    tid_: int
    "TimeID"
    typ_id: object
    "Net Element"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class BlkSum(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iInput0: int
    "Invert ..: Input 0"
    iInput1: int
    "Invert ..: Input 1"
    iInput2: int
    "Invert ..: Input 2"
    iInput3: int
    "Invert ..: Input 3"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sInput0: str
    "Sign at Input 0"
    sInput1: str
    "Sign at Input 1"
    sInput2: str
    "Sign at Input 2"
    sInput3: str
    "Sign at Input 3"
    sNum0: str
    "Number of Input 0"
    sNum1: str
    "Number of Input 1"
    sNum2: str
    "Number of Input 2"
    sNum3: str
    "Number of Input 3"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class BlkRef(PFGeneral):
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    cdisName: str
    "Display name"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Sequence"
    outserv: int
    "Out of Service"
    param: list
    "Parameter"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sIntern: list
    "Variables: Internal Variables"
    sLowLimPar: list
    "Limiting Parameter: Lower Limitation"
    sParams: list
    "Variables: Parameters"
    sStates: list
    "Variables: State Variables"
    sUpLimPar: list
    "Limiting Parameter: Upper Limitation"
    state: list
    "State Variable"
    tid_: int
    "TimeID"
    typ_id: object
    "Type"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class StaPqmea(PFGeneral):
    Gfll: float
    "FLL proportional gain"
    Ksogi: float
    "FLL SOGI proportional gain"
    Snom: float
    "Power rating"
    cDisplayName: str
    "Display Name"
    cUserDefIndex: int
    "User defined Index"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciDist: int
    "Distance from infeed in number of buses"
    ciDistAll: int
    "Distance from infeed in number of buses including switches"
    ciDistAllRoot: int
    "Distance from first infeed in number of buses including switches"
    ciDistRoot: int
    "Distance from first infeed in number of buses"
    ciEarthed: int
    "Earthed"
    ciEnergized: int
    "Energized"
    ciLater: int
    "Lateral Index"
    ciOutaged: int
    "Planned Outage"
    clockPeriod: float
    "Update outputs: Calculation (update) cycle of outputs"
    cpArea: object
    "Area"
    cpBranch: object
    "Branch"
    cpFeed: object
    "Feeder"
    cpGrid: object
    "Grid"
    cpHeadFold: object
    "Head Folder"
    cpMeteostat: object
    "Meteo Station"
    cpOperator: object
    "Operator"
    cpOwner: object
    "Owner"
    cpSite: object
    "Site"
    cpSubstat: object
    "Substation"
    cpSupplySubstation: object
    "Supplying Substation"
    cpSupplyTransformer: object
    "Supplying Transformer"
    cpSupplyTrfStation: object
    "Supplying Secondary Substation"
    cpZone: object
    "Zone"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAstabint: int
    "A-stable integration algorithm"
    iFreq: int
    "Frequency calc.:Use nominal frequency:Phase angle derivative:Frequency-locked loop:Fast fourier transformation"
    iSchemeStatus: int
    "Scheme Status"
    iValues: int
    "Output values:Instantaneous:RMS phasors (DFT), symmetrical comp. and frequency"
    i_interOutput: int
    "Update outputs: Interpolate outputs"
    i_mode: int
    "Output base:Equivalent to MVA value:Power rating of connected element:User-defined power rating"
    i_orient: int
    "Orientation:Load oriented:Generator oriented:Orientation of connected element"
    it2p: int
    "Measured phase:a:b:c:a-n:b-n:c-n"
    loc_name: str
    "Name"
    nominalFreq: float
    "Samples and frequency: Nominal frequency"
    nphase: int
    "No. of phases:1:3"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    pcubic: object
    "Measurement point"
    pid_: int
    "ProjectID"
    rateLim: float
    "FLL frequency rate limiter"
    root_id: object
    "Original Location"
    samplesForUpdate: int
    "Update outputs: Calculate (update) outputs every"
    samplesPerPeriod: int
    "Samples and frequency: Number of samples per period"
    samplesPerWindow: int
    "Samples and frequency: Number of samples for FFT window"
    samplingFreq: float
    "Samples and frequency: Sampling frequency"
    tid_: int
    "TimeID"
    windowLength: float
    "Samples and frequency: FFT window length for calculation"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class CimArchive(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def ConvertToBusBranch(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class ComCimtogrid(PFGeneral):
    addoptions: str
    "Additional Parameters"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    convertDL: int
    "Profiles to convert: Diagram Layout"
    convertDY: int
    "Profiles to convert: Dynamics"
    convertEQ: int
    "Profiles to convert: Equipment"
    convertGL: int
    "Profiles to convert: Geographical Location"
    convertSC: int
    "Profiles to convert: Short Circuit"
    convertSSH: int
    "Profiles to convert: Steady State Hypothesis"
    convertSV: int
    "Profiles to convert: State Variables"
    convertTP: int
    "Profiles to convert: Topology"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dependencies: object
    "Additional Archives"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    order: float
    "Order"
    pGrid: list
    "Grid"
    partial: int
    "Profile conversion"
    pid_: int
    "ProjectID"
    profileFlag: int
    "Profile Filter"
    root_id: object
    "Original Location"
    selectedMas: list
    "Selected"
    sourcePath: object
    "Source Archives"
    tid_: int
    "TimeID"

    def AttributeType(*args): ...

    def Execute(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtLod(PFGeneral):
    cAbsP: float
    "New Load Value: Active Power"
    cAbsQ: float
    "New Load Value: Reactive Power"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Loads"
    cpHeadFold: object
    "Head Folder"
    dP: float
    "Proportional Load Step: Active Power"
    dQ: float
    "Proportional Load Step: Reactive Power"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    iStage: int
    "Event for: Stage"
    iopt_load: int
    "Event for"
    iopt_src: int
    "Source:Default:Load Shedding:Load Transfer"
    iopt_type: int
    "Event of Load"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    newP: float
    "New Load Value: Active Power"
    newQ: float
    "New Load Value: Reactive Power"
    oid_: int
    "ObjectID"
    opt_evt: int
    "Type of Event"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    p_target: object
    "Event for: Load"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    t_ramp: float
    "Event of Load: Ramp Duration"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtOutage(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    i_value: int
    "Value of output signals after outage"
    i_what: int
    "Type of Outage Event"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    p_target: object
    "Element"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtParam(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    eventHandling: int
    "Event handling:OFF:INTER_EVENT:INTER_EVENT_EXACT_TIME:PRECISE_LANDING_EVENT:REPEAT_EVENT:MIN_EVENT:POSTPROC_EVENT:INVALID_EVENT:CTRL_S_EVENT"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    i_sysmat: int
    "Recompute system matrix"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    p_target: object
    "Element"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"
    value: str
    "New Value"
    variable: str
    "Name of Variable"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtShc(PFGeneral):
    L_f: float
    "Fault Impedance: Inductance"
    R2X_f: float
    "Fault Impedance: R/X ratio"
    R_f: float
    "Fault Impedance: Resistance"
    X2R_f: float
    "Fault Impedance: X/R ratio"
    X_f: float
    "Fault Impedance: Reactance"
    Z_f: float
    "Fault Impedance: Impedance"
    ZfaultInp: int
    "Fault Impedance: Input:Resistance, Reactance:Impedance, Angle:Impedance, X/R:Impedance, R/X"
    ang_f: float
    "Fault Impedance: Angle"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    effectedLne: object
    "Affected line"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iApplyShc: int
    "Apply Fault"
    iSchemeStatus: int
    "Scheme Status"
    i_clearShc: int
    "For EMT-Simulation only: Clear Short-Circuit"
    i_p2pgf: int
    "Phases:a,b:b,c:c,a"
    i_p2psc: int
    "Phases:a-b:b-c:c-a"
    i_pspgf: int
    "Phase:a:b:c"
    i_shc: int
    "Fault Type"
    lneshcbus: int
    "Bus index for shc at line"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    p_target: object
    "Object"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    shcLocation: float
    "Fault Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtSwitch(PFGeneral):
    Ilim: float
    "Current threshold (abs.)"
    Ulim: float
    "Voltage threshold (abs.)"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    ctrl_type: int
    "Used in Step:Unknown:Maintenance:Protection:Substation Automation:Remote Controlled (Stage 1):Indicator of Short Circuit (Stage 2):Manual (Stage 3)"
    d_2ndph: float
    "Scheme: Second phase trigger"
    d_3rdph: float
    "Scheme: Third phase trigger"
    d_nph: float
    "Scheme: Neutral delay"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    i_a: int
    "Phase a"
    i_allph: int
    "All phases"
    i_b: int
    "Phase b"
    i_c: int
    "Phase c"
    i_halfw: int
    "Consider half wave:Positive and negative:Positive only:Negative only"
    i_inst: int
    "Trigger closing at"
    i_larlow: int
    "Larger or lower than threshold:Larger:Lower"
    i_n: int
    "Neutral"
    i_open: int
    "Trigger opening at"
    i_phase: int
    "Scheme: Trigger on phase"
    i_scheme: int
    "Scheme"
    i_switch: int
    "Action"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    p_switch: object
    "Circuit-Breaker"
    p_target: object
    "Breaker or Element"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    target: str
    "Breaker or Element found in Slot"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"
    v_lim: float
    "Amplitude threshold"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtSym(PFGeneral):
    addmt: float
    "Additional Torque"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    newS: float
    "Maximal Apparent Power"
    oid_: int
    "ObjectID"
    outNgnum: int
    "Machine on Outage"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    p_sym: object
    "Synchronous Machine"
    p_target: object
    "Synchronous Machine"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtGen(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dP: float
    "Change power: Active Power"
    dQ: float
    "Change power: Reactive Power"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    p_target: object
    "Element"
    pid_: int
    "ProjectID"
    powerChange: int
    "Change power"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtTap(PFGeneral):
    bus: int
    "Tap Action: for Tap at"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    i_tap: int
    "Tap Action"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    ntap: int
    "Tap Action: Tap"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    p_target: object
    "Shunt or Transformer"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtStop(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtSave(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtMessage(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    sMsg: list
    "Message"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtTransfer(PFGeneral):
    P_Portion: list
    "Active Power"
    Q_Portion: list
    "Reactive Power"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    p_source: object
    "Source"
    p_to: list
    "Elements"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    scPortion: list
    "Short-Circuit"
    seq: int
    "Sequence"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtPresync(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_elmsym: object
    "Reference Machine"
    p_from: object
    "Event defined by:"
    p_target: object
    "Breaker"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtTrigger(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iActive: int
    "Save File"
    iSchemeStatus: int
    "Scheme Status"
    iSource: int
    "Source"
    iStart: float
    "Starting Time of Real-Time Simulation"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    p_target: object
    "Results"
    pid_: int
    "ProjectID"
    reason: list
    "Source"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class EvtStep(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dhrtime: float
    "Execution Time: Relative"
    dmtime: int
    "Execution Time: Relative"
    dtime: float
    "Execution Time: Relative"
    dtset: float
    "Integration step size"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    hrtact: float
    "Execution Time: Now"
    hrtime: int
    "Execution Time: Absolute"
    iSchemeStatus: int
    "Scheme Status"
    loc_name: str
    "Name"
    mtact: int
    "Execution Time: Now"
    mtime: int
    "Execution Time: Absolute"
    oid_: int
    "ObjectID"
    outserv: int
    "Out of Service"
    p_from: object
    "Event defined by:"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    tDateTime: int
    "Execution Time"
    tact: float
    "Execution Time: Now"
    tid_: int
    "TimeID"
    time: float
    "Execution Time: Absolute"
    tottime: float
    "Time"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...


class IntPrj(PFGeneral):
    CTLimit: int
    "COMTRADE Data File import limit: Maximum Number of Files"
    CTLimitNum: int
    "COMTRADE Data File import limit: Max. number of files"
    ComTradeUp: int
    "COMTRADE Data: Import Synchronisation"
    Sbase: float
    "Base Apparent Power"
    UpRepeat: int
    "COMTRADE Data Import Synchronisation: Repeat every"
    appr_modby: str
    "Approval Information: Modified by"
    appr_modif: int
    "Approval Information: Modified"
    appr_status: int
    "Approval Information: Status"
    archiveDate: int
    "Archiving: Date archived"
    archivedBy: list
    "Archiving: Archived by"
    archivingComments: list
    "Archiving: Archiving comments"
    base_versionId: int
    "Base project: Version Id"
    cEndTime: int
    "End Time"
    cStartTime: int
    "Start Time"
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    ciNodeCount: int
    "Licence Relevant Nodes: Number of Nodes"
    clenexp: str
    "Lines/Cables Length unit, m"
    close_plots: int
    "Close all open plots at measurement start"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    cspqexp: str
    "Loads/Asyn. Machines P, Q, S unit, VA,W,var"
    ctdDays: int
    "COMTRADE Data: Days"
    ctdEnd: int
    "To"
    ctdStart: int
    "From"
    ctdTime: int
    "COMTRADE Data: Restricted Import"
    currency: str
    "Currency Unit"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    der_baseproject: object
    "Base project: Project"
    der_baseversion: object
    "Base project: Used version"
    der_baseversion2: object
    "New base version: Most recent version"
    der_mergeNtf: int
    "Disable notification at activation"
    der_mergeNtfTime: int
    "New base version: Notify from"
    der_noUpdates: int
    "New base version: Ignore all new versions"
    desc: list
    "Description"
    fkey_prefix: list
    "Foreign key prefix"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gmin: float
    "Min. Conductance gmin"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iAutoOufOfServ: int
    "Automatic Out of Service Detection"
    iAutoSlack: int
    "Auto slack assignment:Method 1:Method 2"
    iBuildNo: int
    "Migrated to Build"
    iCalcSymComp: int
    "Calculation of symmetrical components for untransposed lines"
    iEndTime: int
    "End Time"
    iFlowOrient: int
    "Flow Orientation:Mixed Mode:Load Oriented:Generator Oriented"
    iSchemeStatus: int
    "Scheme Status"
    iStartTime: int
    "Start Time"
    iStatus: int
    "Status:Draft:Issued"
    iTowEarthRed: int
    "Tower: Earth wire reduction (0=V132, 1=V14)"
    icreation: int
    "Creation timestamp"
    ilenunit: int
    "Units"
    lastNotifiedVersionTime: int
    "Last notified version timestamp"
    loc_name: str
    "Name"
    migrationPriority: int
    "Migration Priority:Low:Medium:High"
    migrationStatus: str
    "Migration status"
    objectId: int
    "Object ID"
    offlineMode: str
    "Subscription Mode"
    offlineSynchtime: int
    "Date of last synchronisation"
    oid_: int
    "ObjectID"
    onlineDig_open: int
    "Open online plot (binary bars) at measurement start"
    online_open: int
    "Open online plot (curve) at measurement start"
    optionNotifyAgain: int
    "New base version: Notify Again"
    pCase: object
    "Last open Study Case"
    pMigrPrj: object
    "Migrated Project"
    pPrjSettings: object
    "Settings: Project Settings"
    pfm_auto_path: object
    "Automatically executed Scripts"
    pfm_data_path: object
    "Data"
    pfm_dsm: int
    "PFM-System:&0&None:&2&Master Station:&3&Local Access Station"
    pfm_files: str
    "COMTRADE Data: Data Path"
    pfm_func_path: object
    "Functions"
    pfm_online: object
    "Online plot (curve)"
    pfm_onlineDig: object
    "Online plot (binary bars)"
    pfm_plots_path: object
    "Plots"
    pfm_statname: str
    "Station Name"
    pid_: int
    "ProjectID"
    projectId: int
    "Project ID"
    project_id: list
    "Project"
    project_mapped: list
    "Mapped to folder"
    rmin: float
    "Min. Resistance rmin"
    root_id: object
    "Original Location"
    share_a: list
    "Sharing access level"
    share_allowCopy: int
    "Other users may copy this project"
    share_g: list
    "Groups"
    share_lockingUsers: str
    "Locked by"
    st_activationdate: int
    "Options: Date of last activation"
    st_prjdel: int
    "Options: Housekeeping project deletion"
    st_prjdeldays: int
    "Options Housekeeping project deletion: Project retention period"
    st_purgeauto: int
    "Options: Automatic purging"
    st_purgeautoprd: int
    "Options Automatic purging: Automatic purging interval"
    st_purgedate: int
    "Options: Date of last purging"
    st_rec_all: int
    "Statistics: Total number of records"
    st_rec_current: int
    "Statistics:    Records for current state"
    st_rec_date: int
    "Statistics: Statistics date"
    st_rec_purgeable: int
    "Statistics:    Purgeable records"
    st_rec_recbin: int
    "Statistics:    Records inside recycle bin"
    st_rec_retention: int
    "Statistics:    Records in retention hold"
    st_rec_versions: int
    "Statistics:    Records in versions"
    st_retention: int
    "Options: Object history retention period (before purge)"
    st_undodate: int
    "Options: Minimum date for new versions"
    tags: str
    "Tags"
    tid_: int
    "TimeID"
    timestampId: int
    "Timestamp ID"
    version_id: list
    "Version"
    ymodmin: float
    "Threshold Impedance for Z-model"

    def Activate(*args): ...

    def AddProjectToCombined(*args): ...

    def AddProjectToRemoteDatabase(*args): ...

    def Archive(*args): ...

    def AttributeType(*args): ...

    def BeginDataExtensionModification(*args): ...

    def CanAddProjectToRemoteDatabase(*args): ...

    def CanSubscribeProjectReadOnly(*args): ...

    def CanSubscribeProjectReadWrite(*args): ...

    def ClearInvalidReferences(*args): ...

    def CopyDataExtensionFrom(*args): ...

    def CreateVersion(*args): ...

    def Deactivate(*args): ...

    def EndDataExtensionModification(*args): ...

    def GetDerivedProjects(*args): ...

    def GetExternalReferences(*args): ...

    def GetGeoCoordinateSystem(*args): ...

    def GetLatestVersion(*args): ...

    def GetVersions(*args): ...

    def HasExternalReferences(*args): ...

    def HasReferences(*args): ...

    def LoadData(*args): ...

    def MergeToBaseProject(*args): ...

    def Migrate(*args): ...

    def NormaliseCombined(*args): ...

    def PackExternalReferences(*args): ...

    def Purge(*args): ...

    def PurgeObjectKeys(*args): ...

    def RemoveProjectFromCombined(*args): ...

    def Restore(*args): ...

    def SetGeoCoordinateSystem(*args): ...

    def SubscribeProjectReadOnly(*args): ...

    def SubscribeProjectReadWrite(*args): ...

    def TransformGeoCoordinates(*args): ...

    def TransformToGeographicCoordinateSystem(*args): ...

    def UnsubscribeProject(*args): ...

    def UpdateStatistics(*args): ...

    def UpdateToDefaultStructure(*args): ...

    def UpdateToMostRecentBaseVersion(*args): ...

    def __getattr__(*args): ...


class IntUser(PFGeneral):
    ai: int
    "Artificial Intelligence"
    allowFloat: int
    "Floating Licence Generation"
    allowMaster: int
    "Usage of third party licence masterkey"
    anaredefas: int
    "Corporate Modules: ANAREDE/ANAFAS Export"
    arcflash: int
    "Arc-Flash Analysis"
    bPublicArea: int
    "Publishing user"
    c37: int
    "C37 Simulation Interface"
    cabOpt: int
    "Cable Analysis"
    charact: list
    "Charact."
    check_adv: int
    "Advanced Mode"
    chr_name: str
    "Characteristic Name"
    cimEentso: int
    "CIM: CIM Import/Export (ENTSO-E Profile)"
    cimEentsoCorp: int
    "CIM: CIM Import/Export (ENTSO-E Profile) - corp."
    cimIentso: int
    "CIM: CIM Import (ENTSO-E Profile)"
    conrequest: int
    "Connection Request Assessment"
    contents: list
    "Contents"
    contingency: int
    "Contingency Analysis"
    cosim: int
    "Co-Simulation Interface"
    cpHeadFold: object
    "Head Folder"
    crypt: int
    "Corporate Modules: DPL/DSL/QDSL Encryption"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Description"
    dataExtUnit: list
    "Unit"
    dataTT: int
    "Database Transfer Tool"
    desc: list
    "Description"
    disabledSolverIds: list
    "Disabled Solver ids"
    dist: int
    "Distance Protection"
    distr: int
    "Distribution Network Tools"
    econom: int
    "Economic Analysis Tools"
    enableParal: int
    "Allow Parallel Computing"
    enabled: int
    "Enable user account"
    enabledFrom: int
    "Enable user account Restrict in time: Enabled from"
    enabledTo: int
    "Enable user account Restrict in time: Enabled to"
    expires: int
    "Enable user account: Restrict in time"
    fmuexp: int
    "Corporate Modules: FMU Model Export"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    forcePwChange: int
    "Force password change"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    harm: int
    "Power Quality and Harmonic Analysis"
    iActUseCore: int
    "Actual number of processes to be used"
    iCoreInput: int
    "Actual number of processes to be used: Number of processes"
    iSchemeStatus: int
    "Scheme Status"
    integral: int
    "Corporate Modules: Integral Export"
    iopt_package: str
    "Package Type"
    lastLogon: int
    "Last logon"
    lastPwChange: int
    "Last change"
    ldf: int
    "Load Flow Analysis"
    loc_name: str
    "User name"
    lvnet: int
    "Low Voltage Analysis"
    masterstation: int
    "PFM Master Station"
    maxFloatDays: int
    "Max. Borrow Time (days):"
    motstart: int
    "Motor Starting Functions"
    muld: int
    "Corporate Modules: Multi-User Database"
    netred: int
    "Network Reduction"
    numberOfLogons: int
    "Number of logons"
    oid_: int
    "ObjectID"
    opc: int
    "OPC Interface"
    opfact: int
    "Optimal Power Flow: OPF (Economic Dispatch)"
    opfreact: int
    "Optimal Power Flow: OPF (Reactive Power Optimisation)"
    paramid: int
    "System Parameter Identification"
    pid_: int
    "ProjectID"
    probAnalysis: int
    "Probabilistic Analysis"
    prot: int
    "Time-Overcurrent Protection"
    psse: int
    "Corporate Modules: PSS/E Export"
    pwCatLowerCase: int
    "Enforce password quality: Lowercase Letters (e.g. a, b, c, ...)"
    pwCatNumbers: int
    "Enforce password quality: Digits (e.g. 1, 2, 3, ...)"
    pwCatSymbols: int
    "Enforce password quality: Symbols (e.g. %, -, *, ...)"
    pwCatUpperCase: int
    "Enforce password quality: Uppercase Letters (e.g. A, B, C, ...)"
    pwChangeEnabled: int
    "Enforce regular password changes"
    pwChangeInterval: int
    "Enforce regular password changes: Every"
    pwLength: int
    "Enforce password quality: Minimum length"
    pwQualityEnabled: int
    "Enforce password quality"
    pwUserSpecEnabled: int
    "Enable user specific settings"
    qdynsim: int
    "Quasi-Dynamic Simulation"
    reli: int
    "Reliability Analysis Functions"
    requireServerAuth: int
    "Force Authentication Server usage"
    root_id: object
    "Original Location"
    script: int
    "Scripting and Automation"
    sessionIdleTimerEnabled: int
    "Enable user-specific idle settings: Close application when idle session"
    sessionIdleTimerInterval: int
    "Enable user-specific idle settings Close application when idle session: Time interval"
    sessionIdleTimerUserSpecific: int
    "Enable user-specific idle settings"
    shc: int
    "Fault Analysis"
    smallsig: int
    "Small Signal Stability (Eigenvalue Analysis)"
    stab: int
    "Stability Analysis Functions (RMS)"
    stabemt: int
    "Electromagnetic Transients (EMT)"
    staest: int
    "State Estimation"
    status: str
    "Session status"
    sysaccount: str
    "System Account"
    tececo: int
    "Techno-Economical Analysis"
    tid_: int
    "TimeID"
    transmission: int
    "Transmission Network Tools"
    unitcomm: int
    "Unit Commitment and Dispatch Optimisation"
    user_id: int
    "User ID"
    user_name: str
    "Full name"
    userhash: str
    "User hash"
    users: list
    "Permitted Users"

    def AttributeType(*args): ...

    def HasReferences(*args): ...

    def Purge(*args): ...

    def SetPassword(*args): ...

    def TerminateSession(*args): ...

    def __getattr__(*args): ...


class IntLibrary(PFGeneral):
    charact: list
    "Charact."
    chr_name: str
    "Characteristic Name"
    contents: list
    "Contents"
    cpHeadFold: object
    "Head Folder"
    dat_src: str
    "Data source"
    dataExtDesc: list
    "Options: Description"
    dataExtUnit: list
    "Options: Unit"
    desc: list
    "Description"
    fold_id: object
    "In Folder"
    for_name: str
    "Foreign Key"
    gnrl_modby: str
    "Object modified by"
    gnrl_modif: int
    "Object modified"
    iSchemeStatus: int
    "Scheme Status"
    icreation: int
    "Creation timestamp"
    loc_name: str
    "Name"
    oid_: int
    "ObjectID"
    pid_: int
    "ProjectID"
    root_id: object
    "Original Location"
    share_lockingUsers: str
    "Locked by"
    sharing_access: list
    "Sharing access level"
    sharing_group: list
    "Groups"
    st_activationdate: int
    "Options: Date of last activation"
    st_purgeauto: int
    "Options: Automatic purging"
    st_purgeautoprd: int
    "Options Automatic purging: Automatic purging interval"
    st_purgedate: int
    "Options: Date of last purging"
    st_rec_all: int
    "Statistics: Total number of records"
    st_rec_current: int
    "Statistics:    Records for current state"
    st_rec_date: int
    "Statistics: Statistics date"
    st_rec_purgeable: int
    "Statistics:    Purgeable records"
    st_rec_recbin: int
    "Statistics:    Records inside recycle bin"
    st_rec_retention: int
    "Statistics:    Records in retention hold"
    st_rec_versions: int
    "Statistics:    Records in versions"
    st_retention: int
    "Options: Object history retention period (before purge)"
    st_undodate: int
    "Options: Minimum date for new versions"
    tid_: int
    "TimeID"

    def Activate(*args): ...

    def AttributeType(*args): ...

    def Deactivate(*args): ...

    def HasReferences(*args): ...

    def __getattr__(*args): ...
