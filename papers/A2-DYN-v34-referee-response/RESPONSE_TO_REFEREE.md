# Response to the referee: A2-DYN revision 34

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Controlling review:** `reviews/a2-dyn-v33-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Review commit / report blob:** `9fc2f553168a589e043be73e0354900d5559f433` / `5159113603f557e654792626bf88c2aa5396e3c9`  
**Reviewed v33 source:** `13af9a5795503671a18b5c261e79d61e87ae8bd6`  
**Frozen v33 ordinary paper tree:** `42ba62ef825d1e555f6c6bf83e647792bba67de8`  
**New active directory:** `papers/A2-DYN-v34-referee-response`  
**Date:** 7 October 2026.

We thank the referee for separating the exact stationary inversion from a local limit theorem. In revision 33 the signed middle term was precisely the missing term, not an already negligible remainder. Revision 34 supplies a dynamical and order-preserving argument for the full original stationary probability. The original four-coordinate return problem, its title, physical family, and all inherited mathematical statements remain in the article. We do not identify the physical fixed-count theorem with the distinct raw return-density theorem.

## 1. The entire physical signed middle complement

**New result:** `thm:stationary-microscopic-LLT` proves the original stationary local law

` t^(3/2) P_R(W_R(t)=k, C_R(t)=m) = g_{V_R}(xi) + o(1) `

uniformly in the radius and on every fixed physical central compact set. `cor:stationary-middle-vanishes` then proves vanishing of the full signed inverse in the report, for the explicit polynomial bandwidth `B_m=m^(P+3/2)`; `P=1` gives `m^(5/2)`. Its domain includes the entire noncentral spatial torus and every intermediate roof frequency up to the cutoff. No resonance is omitted.

The proof does not assume this vanishing or derive it from small global mass. It first evaluates the complete positive probability, by the mechanism in Section 2 below, and only then subtracts the already proved Gaussian-plus-complement identity. Nor does it assert an absolute integral bound for the modulus of the middle transform. This is a qualitative, uniform signed estimate; no unsupported polynomial rate for the new `o(1)` is claimed.

## 2. The dynamical mechanism and the order of limits

The new three-module chain is:

- **Module 69:** exact unsmoothed collision spectrum on each bounded frequency set;
- **Module 70:** the mixed collision local limit with both endpoints, obtained by positive Fourier envelopes;
- **Module 71:** the original stationary singleton theorem, the entire signed complement, and normalized conditioning.

The first step is not a quotation of a spatial local limit theorem as a theorem for the joint displacement and roof. `lem:backward-flight-multiplier` places the preceding-flight record on the image side of the collision operator. Its discontinuities are backward collision singularities, transverse to stable curves, and its root coordinate is uniformly one-half Holder. The piecewise multiplier criterion of Demers--Pene--Zhang then gives a genuine analytic realization of the unsmoothed three-coordinate collision twist. Equation `eq:exact-collision-endpoint-pairing` displays the adopted transfer convention explicitly.

The decisive new norm check is `lem:collision-action-weights`. The action identity telescopes the roof sum on a regular connector into two endpoint integrals of the bounded collision action form. On inverse stable pieces it gives a uniform Lipschitz weight; on the actual matched unstable connectors and the trimmed graph pairing it gives a small difference of the two weights. `prop:bounded-band-LY` checks the weak, strong stable, and unstable estimates individually. It retains the exponential stable-to-unstable cross coefficient, chooses the block length first, and chooses the equivalent-norm coefficient afterwards. The nondecaying phase variation in the stable estimate is charged to the weak norm, not falsely placed in a contracting leading coefficient.

A peripheral vector is shown to be a bounded physical density by the finite-dimensional Cesaro projection of smooth densities. Its phase equation is excluded by the inherited complete measurable physical phase theorem. The compact-frequency power estimate therefore follows only after quasi-compactness, weak parameter continuity, and physical peripheral exclusion have been checked on the same family.

For each fixed Fourier bandwidth, the exact spectral pairing yields the endpoint-weighted central inverse and suppresses its noncentral compact complement. Beurling--Selberg upper and lower interval envelopes preserve order on the actual positive source. The proof takes the collision count to infinity first, and then the fixed bandwidth to infinity. It never substitutes a growing `B_m` into an estimate whose constants were only proved for fixed `B`.

Finally the local measure of `(initial state, centered roof sum, terminal state)` evaluates the actual age-overlap kernel. Both cell offsets remain in the exact lattice constraint. The overlap is bounded, compactly supported in its time variable, and continuous outside explicit null singular/cell-crossing sets. The parameter-varying test step is proved with uniform convergence off small fixed neighborhoods and a local mass bound; mere pointwise convergence is not used. The summed amplitude is exactly `bar_tau_R^2`, yielding the physical covariance Jacobian already checked in revision 33.

## 3. Weighted physical statements and selected denominators

`thm:stationary-endpoint-selected-LLT` evaluates the Gaussian amplitude for bounded regular functions of the initial and terminal collision state and flight age. The amplitude is the product of their stationary means. Fixed indicator classes are included under the explicit null-boundary and uniform exceptional-neighborhood conditions. Nonnegative endpoint selectors with uniformly positive product mean have a selected denominator of order `t^(-3/2)`.

`cor:normalized-physical-band` combines the newly proved unselected denominator with the inherited `C/B` source-total-variation estimate. At `B_m=m^(P+3/2)`, the normalized conditional measures differ by `O(m^(-P))` on the original trajectory space, uniformly against all bounded measurable tests. The same statement holds after multiplication by the regular positive endpoint selectors with a proved selected denominator.

These two assertions are deliberately distinct. The Gaussian amplitude is evaluated for the stated endpoint class. The arbitrary-selector assertion is total-variation comparison of two posterior measures; it is not a universal Gaussian amplitude or a positive denominator for every rare path event. The microscopic Gaussian bridge for general macroscopic path selectors is not established by this revision.

## 4. The original four-coordinate actual-return LLT

The four-coordinate return law is not replaced by the physical fixed-count law. All 68 inherited core modules are retained byte-for-byte, including the raw return inversion theorem, critical-edge extraction, common correction, return-frequency criteria, and weighted interfaces. The new image-side collision operator contains the bounded displacement--roof triple, not the discontinuous section occupation or the unbounded induced twist.

The complete pointwise raw return correction and full return-frequency complement have not been proved by the new argument. The metadata leaves those specific claims false. The positive flight-age overlap supplies a direct physical local theorem; it does not automatically supply a density regularizer for the four-coordinate return record. This is the remaining substantive obligation for the original organizing raw-density theorem, rather than a change of topic or a declaration that it cannot be solved.

## 5. Route to microscopic physical conditioning

The route now used for the stationary microscopic endpoint is direct: collision dynamics, compact-frequency spectrum, endpoint local measures, exact age overlap, positive physical denominator, and normalization of the original-trajectory likelihood. It requires no preceding-section event replacement and no invocation of an unproved return LLT. The actual initial age and the initial and terminal cell corrections are kept throughout. Earlier mesoscopic return and conditional path results remain in their stated classes.

## 6. Independent verification and proof boundary

The new collision action estimates, the bounded-band Lasota--Yorke extension, the peripheral-density argument and the varying-overlap local-measure step are the principal points for the next independent specialist audit. No independent human review has been obtained in this author revision. Normal and optimized diagnostics check finite algebra and source identity; they do not certify the continuum dynamics or the local limit theorem.

## 7. Exposition and all eight technical comments

The front matter now has a substantially shorter abstract and one leading theorem. The full A--X synopsis, with all statements, notation and proofs, is moved to an included mathematical appendix. The entire previous main source and abstract are retained under `provenance/`; duplicated historical roadmaps are not placed before the proof. No inherited mathematical label is removed. Theorem X is entitled “Exact inversion and Gaussian-plus-complement reduction,” while the new leading theorem states the actual local law.

The exact endpoint transfer identity is displayed in module 69. The dependence of `J_*` on the chosen fixed cell and uniform horizon is stated once at the beginning of module 71. The physical time second derivative remains a finite measure, not a `W^(2,1)` derivative. The new theorem separates collision-central and physical-central uniformity and explicitly fixes the bandwidth in the signed-complement assertion. The prior denominator equivalence remains true but is no longer used as a substitute for a proof. The covariance normalization and stationary endpoint means are displayed. The finite diagnostics are not used as evidence for continuum middle-frequency dynamics.

The source and native build are qualified at their exact remote SHA. The successful v33 run is baseline evidence only; dynamic v34 receipts identify its own run, source tree and PDF hash. This packet is an author revision for further substantive review, not a journal acceptance or a formal proof certificate.
