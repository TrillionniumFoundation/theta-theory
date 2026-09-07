# Referee Report — Round 20 (No-Revision Reconsideration)

**Paper:** B2 — *Collision-Marked Trajectory Clusters and Joint Dynamic Large Deviations for Deterministic Hard Spheres*  
**Branch inspected:** `revision/round19-referee-positive-closure-11paper-2026-09-02`  
**Branch head inspected:** `4eb32f8ff66dbb93edaabcf96d8c62bf06f13bc2`  
**Active mathematical source:** `ROUND17_POSITIVE_CLOSURE.tex`  
**Active source blob:** `22a545857a73d49993d0388f2bfe1b28643d5673`  
**Prior detailed report:** `REFEREE_REPORT_ROUND18_GPT56_PRO.md`  
**Date:** 2 September 2026  
**Editorial recommendation:** **REJECT WITHOUT RECONSIDERATION**

## 1. Reconsideration status

No revised B2 manuscript is present at the declared branch head. The active source is unchanged and still contains the fatal factorial inconsistency identified previously. There is no corrected connected expansion, no uniform pre-contact atlas, no finite-volume likelihood derivation, and no full LDP proof.

## 2. Unresolved fatal defects

### 2.1. The Green-trace closure and singular-boundary control remain absent

The paper still invokes a divergence-measure-field trace theorem without defining the growing hard-sphere domains, normal trace space, or topology in which incoming traces converge. Sequences of flux measures may concentrate near grazing or multiple-contact strata even though each smooth Liouville law charges them with zero flux. A quantitative nonconcentration estimate uniform in the Boltzmann–Grad limit is indispensable and is not supplied.

### 2.2. The global pre-contact atlas remains unjustified

Nonvanishing of one analytic minor at one witness only proves that the minor is not identically zero on one component. It does not cover every realized component, provide a finite global atlas before compact truncation, or control Łojasiewicz constants as the genealogy, velocity cutoff, and chronology separation vary. The coarea power of `\varepsilon`, flux normalization, and stability of the full reflected future are not derived.

### 2.3. The factorial contradiction remains in the active proof

The source states

`\sum_{|G|=k} W_G^\varepsilon \le k! C^k T^{k-1}`

and then bounds the discarded tail by the supposedly convergent series `\sum_k C^kT^{k-1}`, silently deleting `k!`. As written, the actual factorial series diverges for every positive `T`. If a compensating `1/k!` symmetry factor exists, it must appear in the definition and survive label/genealogy counting. It does not. This invalidates the all-contact majorant, normal convergence, source derivatives, pressure theorem, and every downstream cumulant claim.

### 2.4. Positive recovery is still not proved for the nonlinear reference `A_f`

The perspective entropy is convex in `(A,\Gamma)`, but `A_f` depends quadratically on `f`. Linear mixing and smoothing of `(f,\Gamma)` do not automatically preserve `\Gamma\ll A_f`, bounded relative densities, exact balance, and action convergence. Strict positivity alone does not give quantitative upper and lower bounds for `d\Gamma_n/dA_{f_n}`. The conservative velocity-tail correction is also not constructed.

### 2.5. The microscopic contact tilt remains circular

The displayed likelihood cost is the compensator formula for changing a Poisson random measure intensity. Microscopic hard-sphere contacts are deterministic functions of the random initial configuration. An exponential tilt of initial data has likelihood “source minus finite-volume log normalizer”; the Poisson-type action must be derived in the limit, not assumed as an exact microscopic Radon–Nikodym formula. Using the desired limiting Hamiltonian to justify the microscopic tilt is circular.

### 2.6. The pressure and full LDP remain outlines

A finite-genealogy Lanford expansion does not by itself prove exponential-scale convergence of a marked log-partition function and all connected cumulants. Exponential tightness, goodness, identification of the projective dual with the nonlinear density/contact action, and the microcanonical conditioning transfer are still asserted in one paragraph. The latter also depends on the unproved B1 coefficient theorem.

## 3. Editorial consequence

A valid resubmission must first repair the combinatorial normalization and prove a genuinely summable connected expansion, then establish uniform pre-contact estimates, a noncircular finite-volume tilt, positive rate-density, and complete topology/tightness/rate identification. Nothing of that kind appears on the branch.

## 4. Recommendation

**Reject without reconsideration.** B2 remains the broken root of the hard-sphere dependency chain.