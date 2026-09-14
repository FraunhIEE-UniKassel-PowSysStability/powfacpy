model LoadSheddingController
  "Stepwise under-frequency / RoCoF load-shedding controller for one PowerFactory ElmLod.

   One instance per load. Latching only (no automatic load restoration). Each stage
   sheds a fraction of THIS load's instantaneous power. Intended composite-model wiring:

     f      <-- bus electrical frequency        n:fehz        [Hz]
     pLoad  <-- load active power                m:Psum:bus1   [MW]
     qLoad  <-- load reactive power              m:Qsum:bus1   [Mvar]
     dpext  --> ElmLod.Pext                                    [MW]
     dqext  --> ElmLod.Qext                                    [Mvar]

   Sign convention: ElmLod.Pext is assumed to be added to the load (Pext > 0 means
   more load). If your PowerFactory version uses the opposite convention, negate
   dpext / dqext.

   This is standard Modelica but also written to fit PowerFactory's Modelica subset
   (Hybrid method): der() only on protected state variables, `der(x) = (u-x)/T` form,
   every state assigned once in `initial equation`, no parameter start values. Import
   it with `powfacpy.applications.modelica.ModelicaModel.create_model_type(
   ModelicaModelSpec.from_modelica('.../LoadSheddingController.mo'))`, which unrolls
   the `for` loops / arrays before creating the TypMdl.
  "

  // ------------------------------------------------------------------
  // Under-frequency stages (definite time)
  // ------------------------------------------------------------------
  parameter Integer nStage = 4 "number of under-frequency stages";
  parameter Real fLevel[nStage] = {49.0, 48.8, 48.6, 48.4} "stage pickup frequency [Hz]";
  parameter Real fDelay[nStage] = {0.10, 0.10, 0.10, 0.10} "stage definite-time delay [s]";
  parameter Real fFrac[nStage] = {0.10, 0.10, 0.15, 0.15} "stage shed fraction of this load [-]";

  // ------------------------------------------------------------------
  // RoCoF stages (extension, disabled by default)
  // ------------------------------------------------------------------
  parameter Boolean useRocof = false "enable df/dt stages";
  parameter Integer nRstage = 1 "number of df/dt stages";
  parameter Real rLevel[nRstage] = {-1.0} "stage pickup df/dt [Hz/s] (negative)";
  parameter Real rDelay[nRstage] = {0.15} "stage definite-time delay [s]";
  parameter Real rFrac[nRstage] = {0.10} "stage shed fraction of this load [-]";
  parameter Real fRocofArm = 49.8 "df/dt stages are armed only while f < fRocofArm [Hz]";
  parameter Real Trocof = 0.10 "low-pass time constant for the df/dt estimate [s]";

  // ------------------------------------------------------------------
  // General
  // ------------------------------------------------------------------
  parameter Boolean enable = true "master enable";
  parameter Real fNom = 50.0 "nominal frequency [Hz]";
  parameter Real Tmeas = 0.02 "load-power measurement filter time constant [s]";
  parameter Real Tbrk = 0.02 "breaker operating time constant [s]";
  parameter Real kShedMax = 0.95 "maximum total shed fraction [-]";

  // ------------------------------------------------------------------
  // Interface
  // ------------------------------------------------------------------
  input Real f "measured bus frequency [Hz] (n:fehz)";
  input Real pLoad "measured load active power [MW] (m:Psum:bus1)";
  input Real qLoad "measured load reactive power [Mvar] (m:Qsum:bus1)";
  output Real dpext "additive active power -> ElmLod.Pext [MW]";
  output Real dqext "additive reactive power -> ElmLod.Qext [Mvar]";
  output Real rocof "estimated df/dt [Hz/s] (monitoring)";

protected
  Real kShed(start = 0) "total shed fraction [-] (a state: PowerFactory forbids der() on an output; monitor as s:kShed)";
  Real fFilt "filtered frequency for the df/dt estimate [Hz]";
  Real pMeasF "filtered load active power [MW]";
  Real qMeasF "filtered load reactive power [Mvar]";
  Real pIntr "load active power without the shedding injection [MW] (monitoring)";
  Real qIntr "load reactive power without the shedding injection [Mvar] (monitoring)";
  Real den "1 - kShed, floored to 1 - kShedMax [-]";
  Real fTmr[nStage](each start = 0) "under-frequency stage timers [s]";
  Real rTmr[nRstage](each start = 0) "df/dt stage timers [s]";
  Boolean fArm[nStage] "under-frequency stage picked up";
  Boolean rArm[nRstage] "df/dt stage picked up";
  Boolean fTrip[nStage](each start = false) "under-frequency stage tripped (latched)";
  Boolean rTrip[nRstage](each start = false) "df/dt stage tripped (latched)";
  Real fCon[nStage] "under-frequency stage shed contribution [-]";
  Real rCon[nRstage] "df/dt stage shed contribution [-]";
  Real kTarget "commanded shed fraction before the breaker lag [-]";

initial equation
  // every state must be assigned exactly once here (PowerFactory Hybrid requirement)
  fFilt = f;
  pMeasF = pLoad;
  qMeasF = qLoad;
  kShed = 0;
  for i in 1:nStage loop
    fTmr[i] = 0;
  end for;
  for j in 1:nRstage loop
    rTmr[j] = 0;
  end for;

equation
  // ---- measurement filters (der(x) on the LHS: required by PowerFactory) ----
  der(pMeasF) = (pLoad - pMeasF) / Tmeas;
  der(qMeasF) = (qLoad - qMeasF) / Tmeas;

  // ---- filtered df/dt estimate from the (ideal) bus frequency ----
  der(fFilt) = (f - fFilt) / Trocof;
  rocof = (f - fFilt) / Trocof;

  // ---- under-frequency stages: definite time, latching ----
  for i in 1:nStage loop
    fArm[i] = enable and (f < fLevel[i]);
    der(fTmr[i]) = if fArm[i] then 1 else 0;
    when not fArm[i] then
      reinit(fTmr[i], 0);
    end when;
    when fArm[i] and (fTmr[i] >= fDelay[i]) then
      fTrip[i] = true;
    end when;
    fCon[i] = if fTrip[i] then fFrac[i] else 0;
  end for;

  // ---- df/dt stages: definite time, latching, supervised by fRocofArm ----
  for j in 1:nRstage loop
    rArm[j] = enable and useRocof and (rocof <= rLevel[j]) and (f < fRocofArm);
    der(rTmr[j]) = if rArm[j] then 1 else 0;
    when not rArm[j] then
      reinit(rTmr[j], 0);
    end when;
    when rArm[j] and (rTmr[j] >= rDelay[j]) then
      rTrip[j] = true;
    end when;
    rCon[j] = if rTrip[j] then rFrac[j] else 0;
  end for;

  // ---- aggregate shed command + breaker operating lag ----
  kTarget = min(kShedMax, sum(fCon) + sum(rCon));
  der(kShed) = (kTarget - kShed) / Tbrk;

  // ---- shed a fraction kShed of THIS load's instantaneous (intrinsic) power ----
  // pLoad already contains dpext, so the intrinsic load is reconstructed as
  //   pIntr = pMeasF - dpext,   with   dpext = -kShed * pIntr
  // which solves to the explicit (loop-free) expression below.
  den = max(1 - kShed, 1 - kShedMax);
  dpext = -kShed / den * pMeasF;
  dqext = -kShed / den * qMeasF;
  pIntr = pMeasF - dpext;
  qIntr = qMeasF - dqext;

end LoadSheddingController;
