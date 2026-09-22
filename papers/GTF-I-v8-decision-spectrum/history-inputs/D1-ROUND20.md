# Referee Report — Round 20 (No-Revision Reconsideration)

**Paper:** D1 — *Rigidity and Universal Contractions of Hard-Sphere Kinetic Cotangents*  
**Branch inspected:** `revision/round19-referee-positive-closure-11paper-2026-09-02`  
**Branch head inspected:** `4eb32f8ff66dbb93edaabcf96d8c62bf06f13bc2`  
**Active mathematical source:** `ROUND17_POSITIVE_CLOSURE.tex`  
**Active source blob:** `389122a6a7cbaa471d10f9bbc3314dff140af05e`  
**Prior detailed report:** `REFEREE_REPORT_ROUND18_GPT56_PRO.md`  
**Date:** 2 September 2026  
**Editorial recommendation:** **REJECT WITHOUT RECONSIDERATION**

## 1. Reconsideration status

No revised D1 source appears on the Round-Nineteen branch. The latent-phase assumptions, posterior state, controlled aggregation formula, zero-free chart, Gaussian mixture, and contraction theorem are unchanged. The prior detailed report remains controlling.

## 2. Unresolved fatal defects

### 2.1. The latent-phase experiment is still assumed rather than derived

The paper starts with a finite positive label `J` and conditional laws `P_{\varepsilon,j}` whose mixture is exactly the physical law. It does not construct such a measurable partition or extension for either platform. Recurrent coding components need not form a finite physical partition, and source/preparation choices for hard spheres are alternative experiments or controls, not mutually exclusive latent events of one experiment. The principal object of the paper is therefore postulated.

### 2.2. Upstream component LDPs and common scaling remain unavailable

The finite-mixture LDP is elementary under genuine component LDPs at one speed and compatible weight asymptotics. A3 and B2 do not prove those inputs, and D1 supplies no phase-conditioned exponential tightness or normalization theorem. Superexponentially small components or differing speeds would require a different statement.

### 2.3. `(x,\rho)` remains an insufficient information state

When phases have distinct hidden dynamics or filters, future likelihoods depend on the phase-conditioned posterior state for each component, not merely a common physical state and scalar phase weights. A sufficient state generally contains `(\rho_j,\pi_t^j)_j` together with any unnormalized likelihood variables. The manuscript neither defines a common component state space nor proves lumpability. Common domination and measurable likelihood increments are also absent.

### 2.4. The controlled log-sum formula still optimizes with forbidden information

If `S_t^j` already optimizes over controls separately in each component, then

`\log\sum_j \rho_j \exp\{\theta S_t^j h\}`

allows a different optimizer for every hidden phase. In the actual partially observed mixture, the controller does not know `J` and must use one shared observation-based policy. Optimizing and summing over latent phases do not commute. The displayed value is generally the value for a controller who observes the phase. A correct DPP must retain all phase-conditioned beliefs and optimize a single admissible policy after forming the fixed-policy mixture likelihood.

### 2.5. The zero-free and Gaussian theorems remain defective

The Rouché argument is valid only after assuming a uniform dominant-term expansion with a remainder less than half the leading term. That expansion is essentially the difficult model-specific theorem and is not supplied by A2/A3 or B1/B2.

The Gaussian theorem assumes `\sqrt{a_\varepsilon}(TX_\varepsilon-m_j)\Rightarrow N(0,\Sigma_j)` but states a limit involving `N(m_j,\Sigma_j)` without defining a random variable having that scaling. The unscaled variable converges to `m_j`; the centered scaled variable has mean zero. The theorem also uses `\gamma_*` without defining it, and component prior weights alone do not determine every posterior or conditioned tie weight when saddle determinants and event likelihoods contribute.

### 2.6. The phase-aware contraction theorem still assumes its difficult commutations

Ordinary contraction gives the finite-labelled rate formula. Shrinking-event conditioning, pressure differentiation, Gaussian tangent limits, posterior aggregation under shared control, and memory/cotangent commutation require separate uniform local theorems. Referring to C2 does not prove them, since C2's own functor theorem is unverified.

## 3. Editorial consequence

Only the exact phase-cost sign identity and the conditional finite-mixture LDP survive as elementary statements. A genuine model paper must first construct the latent experiment, use a sufficient information state and common policy, prove component analytic and LDP inputs, and correct the Gaussian scaling. No such revision has been submitted.

## 4. Recommendation

**Reject without reconsideration.** The manuscript remains a synthesis of assumed components with an incorrect controlled aggregation and an inconsistent second-order limit.