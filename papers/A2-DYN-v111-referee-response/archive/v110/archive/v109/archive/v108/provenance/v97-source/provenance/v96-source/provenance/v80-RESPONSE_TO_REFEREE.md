# Response to the external report on A2-DYN revision 79

**Author:** Qian Qi. **Revision:** 80, 11 October 2026.

**Controlling report:** `reviews/a2-dyn-v79-external-top4-review-2026-10-11/REFEREE_REPORT.md`, commit `6764d25a4e3aaeb826d4ec24a12a55d16989d9e2`, blob `dd7a2e7ee91757cdb253eaf8e605cd330ca11e3f`.

**Frozen author baseline:** `be7d5f2c076b73b3da254d36b1268d3cb842ea6a`, paper tree `6d41a1dbb1b0ed702e7445aaac476c87258b7ab8`. This revision descends from the controlling review commit, which in turn descends directly from that author SHA. It preserves all 182 inherited cores and the complete preceding article.

We thank the referee for distinguishing an exact transport identity from an actual roof-height estimate. The principal new result is a singular *volume* insertion theorem. It sums all inverse-incidence scales on the original exact-label source, rather than charging the thin corridor to another pointwise bad source. Its optical consequence estimates the full inverse-twist loss and genuine grazing starting mass when the initial endpoint momentum is bounded away from criticality. The initial critical source and nongrazing outgoing flux still require separate estimates. The original pointwise theorem, labels, source normalization, guard, arithmetic classes and actual-return interpretation are unchanged.

## 1. Complete true-exit height — request 1; report §§13–16

Theorem `thm:v80-noncritical-optical` proves a collision-normalized `C r/a` bound for the sum of complete optical loss and *genuine grazing initial exit mass*, restricted only by initial `|g|>=a`. No internal incidence corridor is imposed. At a grazing exit the optical density tends to zero, but its positive starting density is paid by negative optical variation. The proof does not set the inverse forward Jacobian to one or infer that zero physical boundary density means zero starting mass.

For nongrazing exits, Theorem `thm:v80-boundary-reduction` bounds the starting mass by the outgoing physical flux plus the same controlled singular drift. It therefore accounts for the compression cost in the boundary pullback quantitatively. It does not declare the outgoing flux small. The resulting full endpoint budget retains critical initial mass and nongrazing flux as unproved height estimates. Thus this request is advanced, not marked fully closed.

## 2. Complete inverse-twist height and the thin incidence source — request 2; §§10–12,15.2

Module 183 proves a superlinear marked-incidence estimate. In the established convention a density is relative to invariant collision measure; a real-frequency physical power has modulus one. A homogeneous stable curve meeting `c<s` has length `O(s^(3/2))` because quadratic homogeneity strips have width `O(k^-3)` and incidence `O(k^-2)`. There is no extra cosine factor in the weak norm.

A fixed refinement near every unit-modulus peak permits interpolation exponent `7/8`. The continued eigenvector is not assigned physical modulus one: it is approximated by a finite physical power with the remainder controlled separately. The two chronological cases yield amplitudes `s^(21/16)` and `s^(161/128)`, both stronger than `s^(5/4)`. The real characteristic function also has the independent cap `nu(c<s)<=s^2`. Retaining that cap on the finite-count spectral remainder is essential.

Module 184 integrates the capped estimate by positive layer cake to obtain actual `c^-a 1_{c<s}` insertions for every `0<a<5/4`, including `a=1`. The cap makes the error integrable all the way to zero incidence *before* taking the collision limit. The leading inverse-incidence thin contribution is `O(s^(1/4))` at every previously fixed roof width. Summing the geometric depth weights gives a uniform fixed-width bound for the complete source `1+sum q0^depth/c_i`, including all physical words and original exact labels.

This is the missing singular-insertion type of input identified in §15.2 of the report; it is now derived rather than imported from a bounded-multiplier theorem. Its use in optical drift proves the `C r/a` height bound at every internal incidence scale. It does not remove the initial `|g|>=a` restriction. The complete inverse-twist flag remains false while the critical initial source is unestimated.

## 3. Separation of mechanisms — request 3

Grazing means at least one internal incidence tends to zero at the first exit. Simultaneous failures are assigned to that class when this condition holds. Every other finite exit is nongrazing. These classes are disjoint, and their starting sources are kept separate from surviving optical loss until the common nonnegative variation bound is applied. Signed occupation currents do not subtract any positive starting mass. Section and competing-hit boundaries remain in the nongrazing flux whenever no incidence vanishes.

## 4. Legal limits — request 4

The peak refinement is fixed and independent of collision count and grazing thresholds. On every fixed auxiliary roof band the error retains its physical cap; the infinite layer-cake integral is completed before either limit. The width and initial critical threshold are fixed before the collision limsup. The auxiliary band is enlarged afterwards, and the outer reconstruction parameter last. No growing Fourier band or width depending on collision count is used.

The initial-critical Abel inequality is stated only as an extended nonnegative inequality. Fixed-width concentration is explicitly not used to bound its singular initial-roof convolution. This prevents a hidden exchange of the small-width and collision limits.

## 5. Mixed-coordinate cubic calculation — request 5

The physical-normalization subsection of module 184 records the convention in one place: endpoints are angles; internal variables are oriented arclengths; the internal Hessian is `D_c A D_c`; an endpoint lift has arclength component `R u`. Differentiated stationarity annihilates all purely internal variations in the cubic identity. The circle contributes arclength derivatives of sizes `R^-1` and `R^-2`. These are the same coordinates as the retained module-180 calculation; no endpoint angle is silently treated as arclength.

## 6. Common target-direction coarea versions — request 6

Lemma `lem:v80-common-coarea` supplies a countable flow-box construction on the actual disjoint regular physical pieces. A Borel assignment is used only for summation, not as a stopping rule. Change of variables is applied to the full survivor graph `(x,h)->(Phi_h x,h)` and disintegrated over `(F,h)`. A countable determining algebra identifies the kernel measures outside one joint null set; the resulting equality then holds for all nonnegative Borel weights. Truncated singular insertions and their positive limits use those same kernels. The permitted parameter ordering remains `sup_R esssup_t`.

## 7. Optical normalization — request 7

Module 184 checks `omega=|K_0m|/R=R c_0 c_m/y_m` directly against endpoint first variation `F_alpha0=-R p_0`. The internal incidence squares cancel in the corner Schur complement; two endpoint angle changes contribute `R^2`, followed by division by `R` in the momentum derivative. One- and two-flight formulas are recorded. Tangent orientation changes only conjugate the internal Hessian by diagonal signs. Finite rational tests check the same low-dimensional identities without claiming to certify the continuum optical calculation.

## 8. Explicit exit exhaustion — request 8

The common-kernel lemma constructs precompact regular domains from finite unions of rational flow-box rectangles. Roof-constant faces are transverse; angle-constant faces have zero flux; corners have zero transverse measure. The outside-source plus first-exit expression is the decreasing indicator that the entire forward segment is not contained in the domain. Every compact surviving segment eventually lies in an exhaustion domain. The limit is taken at fixed collision count, never exchanged with the normalized limsup. Nongrazing boundary flux is defined on one-sided physical faces with backward lifetime selecting the first exit, not a later re-entry.

## 9. Independent specialist review — request 9

No independent human review has been obtained in this work. The updated specialist map identifies the density convention and homogeneous weak gain, fixed peak refinement, capped singular layer cake, optical normalization, grazing initial-mass accounting, common kernels and the remaining critical/surface estimates. Native builds and finite fixtures are not described as mathematical certification. The new arguments remain available for external specialist scrutiny.

## 10. Journal and supplement — request 10

The journal states the original problem, the exact inherited analytic interfaces, the singular-insertion and optical results, and their proofs. The complete v79 article is retained in the supplement; all 182 inherited modules and their original files are preserved. The assembled historical article resolves its former external supplement references internally, without editing its source snapshot. Source receipts, author status and validation evidence remain outside the journal narrative. No alternate topic, weakened smoothed target or substitute journal objective is introduced.

## Qualification and exact scope

The new qualification workflow pins both the v79 paper tree and the controlling v79 report blob. It checks all inherited sources and snapshots, agreement of normal and optimized diagnostics, complete native journal/supplement builds, all 185 core files in the recorder union, stable references and PDF geometry. Successful v79 runs are baseline evidence only; the v80 run IDs and results must be read at the final v80 author SHA.

The primary raw pointwise theorem and its unconditional path, clock and likelihood consequences are not marked proved. The new mathematical gain is the complete singular volume-source estimate and its all-incidence optical/grazing consequence away from initial criticality, together with a paid nongrazing pullback. The two remaining source heights are stated explicitly in the final endpoint budget.
