# Referee Report — Round 20 (No-Revision Reconsideration)

**Paper:** C1 — *Typed Control, Information, and Saddle Envelopes for Kinetic Cotangent Phases*  
**Branch inspected:** `revision/round19-referee-positive-closure-11paper-2026-09-02`  
**Branch head inspected:** `4eb32f8ff66dbb93edaabcf96d8c62bf06f13bc2`  
**Active mathematical source:** `ROUND17_POSITIVE_CLOSURE.tex`  
**Active source blob:** `4bcea1167c4abe33090619c0190e554e5b89045a`  
**Prior detailed report:** `REFEREE_REPORT_ROUND18_GPT56_PRO.md`  
**Date:** 2 September 2026  
**Editorial recommendation:** **REJECT WITHOUT RECONSIDERATION**

## 1. Reconsideration status

The declared revision branch contains no altered C1 source. The filtering model, chart hypotheses, zero-evidence construction, DPP, LAN, and Bernstein–von Mises argument are byte-for-byte unchanged. No new model-specific observation theorem or triangular-array likelihood analysis has been added.

## 2. Unresolved fatal defects

### 2.1. The hidden transition/observation model remains incompletely typed

The object `\Lambda_\pi^a(dx,dy)=\pi(dx)K^a(x,dy)` records an old state and an observation unless `K^a` secretly includes a transition to `x'`; the manuscript later conditions an `x'` that is not present in the displayed kernel. Prediction, observation timing, control timing, and the exact belief update are therefore not defined.

### 2.2. The regular chart still omits the domination used in its proof

The stability proof embeds both joint kernels in a fixed dominating state measure `m_0(dx)\nu(dy)`. The chart definition supplies only observation domination in `y`; beliefs in `\mathcal P_W(E)` can be mutually singular in `x`. A fixed `m_0`, density bounds relative to it, and closure under the prediction step are additional strong hypotheses. Without them, the displayed `L^1` comparison of posteriors is not valid on the stated belief class.

### 2.3. The chart is not derived from the upstream models

A2, B1, and B2 do not provide the claimed `W_y^{s,1}` density regularity, uniform positive evidence lower bound, and hidden-state derivative bounds for arbitrary finite-cylinder or particle/contact observations. Source derivatives are not Sobolev derivatives in the observed value. Available low-order derivatives may not even reach `s>\dim Y`. The statement that atomic observations become exponentially equivalent after smoothing lacks a coupling, a superexponential estimate, and stability of posterior values under that smoothing.

### 2.4. The global state and DPP remain undefined

The zero measure has no intrinsic projective direction. A blow-up at zero requires an explicitly topologized space of approach directions and transition maps between overlapping charts. The disjoint union `\mathcal Z` is not proved standard Borel or Polish. The relaxed-control space, admissible correspondence, measurable graph, controlled kernel, reward semicontinuity, and exponential integrability required for measurable selection and risk-sensitive dynamic programming are not specified.

### 2.5. Finite-coordinate and statistical conclusions still overreach

A finite coordinate system on one compact belief set does not prove value approximation without forward invariance, uniform transition stability over controls, and a quantitative Bellman error recursion. The risk-sensitive Bellman operator is not automatically a strict sup-norm contraction.

For statistics, QMD at each fixed `\varepsilon` is insufficient for a local shift of order `\mu_\varepsilon^{-1/2}` in a triangular array. One needs a uniform likelihood-ratio remainder, information convergence, contiguity, and a Lindeberg/local asymptotic quadratic theorem. A score CLT alone does not provide the quadratic likelihood term. Bernstein–von Mises additionally requires posterior concentration, tests away from the local chart, prior-tail control, and—under adaptive strategies—uniform policy-dependent likelihood theory. None is proved.

## 3. Editorial consequence

A genuine revision must specify the hidden transition/observation kernel, add exact common domination to the chart, verify that chart for each microscopic model, construct a measurable global belief state, and separate uniform triangular-array LAN from the posterior-concentration proof. The inspected branch contains none of this.

## 4. Recommendation

**Reject without reconsideration.** The regular filtering and statistical theorems remain unsupported.