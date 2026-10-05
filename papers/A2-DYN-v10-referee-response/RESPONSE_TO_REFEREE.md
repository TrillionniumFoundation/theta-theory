# Response to the referee on A2-DYN revision 9

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revised source:** `papers/A2-DYN-v10-referee-response`  
**Controlling report:** `reviews/a2-dyn-v9-external-top4-review-2026-10-05/REFEREE_REPORT.md`  
**Report commit / blob:** `8448e718a22658c94dcb654b52c69b44f9889fe1` / `14539536556fc1d041cc30917296708084146259`  
**Reviewed author source:** `872f8695670373a3ca67ff84841a1ea38ed64227`  
**Date:** 5 October 2026

We thank the referee for distinguishing the proved collision-compensation and Gaussian chain from the remaining raw-density estimates. We retain the original title, physical family, four-coordinate record and raw mixed-density endpoint. All twenty-four mathematical core files of the reviewed version are preserved byte for byte, and all remain included. The revision is a complete article, not a renamed source or a response supplement.

The principal new result is an integrated major-arc estimate for the actual first-return record. The previous compact-rescaled-frequency conclusion is replaced, for this step of the argument, by an L1 estimate on a polynomially expanding ball. With `v` denoting the rescaled Fourier variable, Theorem B and Theorem 21.3 prove

`sup_R integral_{|v|<=2 n^(1/200)} |C_n,R(v)-exp(-v^T D_R v/2)| dv <= C n^(-3/280) sqrt(log(2+n))`.

The theorem also covers complex initial insertions with uniform supremum and initial-coordinate BV bounds. It does not presume a spectral realization of the induced operator. The proof exposes all frequency factors before integration, uses the exact compensation identity, and retains the physical stopping error. Corollary 21.4 then uses this proved central integral in an exact raw inversion formula. The additional nondegeneracy, complementary-frequency and raw-edge hypotheses are stated expressly rather than attributed to the new theorem.

## Responses to the essential work in Section 12

### 1. Periodic-evaluable regularity and uniform nondegeneracy

The distinction in the report is retained. The collision and induced coboundaries in Theorem 15.6 of the inherited chain are L2 identities and do not select values at periodic points. The new major-arc theorem only uses the established positive semidefinite covariance, and its proof remains valid at a singular matrix. Positive definiteness appears as an additional assumption in Corollary 21.4, exactly where an integrable four-dimensional Gaussian density is required.

This revision does not claim to have proved the missing regular representative. The measurable Livsic results cited in the article cannot be applied to the section discontinuities without checking their regularity and dynamical hypotheses. In particular, the periodic rank calculation is not applied to an arbitrary representative of an L2 class.

### 2. Actual induced anisotropic family

The new analysis advances the central part of this requirement by a different, fully proved route: Lemma 21.1 uses only the genuine collision spectral family, Proposition 21.2 performs exact stopping, and Theorem 21.3 integrates the resulting estimate. This removes a fixed-neighborhood induced spectral expansion from the central hypothesis of the new raw inversion route. It does not remove the need for complementary-frequency estimates.

The collision, damped renewal and direct-block identities remain included with their original scope. We do not identify an L1 isometry or an Lp-to-Lq block operator with a quasi-compact induced endomorphism. Fredholm control, phase reconstruction and the large-frequency induced estimates are not claimed supplied by the growing-band result.

### 3. Complete raw branch decomposition

All previous individual critical-word calculations, exact edge terms and residual criteria are retained. Appendix A formalizes BV of the **initial-coordinate one-collision functions**; it does not claim BV or second variation of the **pushed-forward density**. Corollary 21.4 requires residual integrability and the local edge corrections for the actual full measure. No physical word, singular boundary or competing-root contribution is dropped by this reformulation. The quantitative full branch sum remains to be established.

### 4. Frequency splice and actual constants

The new central balance is explicit and has a verified nonempty range:

`0<epsilon<1/134`, `10epsilon<theta<(1/2-7epsilon)/6`.

The integrated smoothing, cubic and stopping margins are respectively

`theta/2-5epsilon`, `1/2-6theta-7epsilon`, `1/5-5epsilon`.

At `(epsilon,theta)=(1/200,1/14)` they are `3/280`, `51/1400`, and `7/40`. These inequalities include the four-dimensional volume loss; they are not just pointwise exponent checks.

This is a central-band balance, not the still-unproved intermediate/outer splice. Remark 21.5 explicitly notes that the new physical radius `n^-1/2+1/200` is smaller than `n^-2/5`. Thus the older outer-tail condition does not cover the remaining annulus. Corollary 21.4 states the stronger complementary integral needed by its own cutoff. Both original inversion theorems and their original hypotheses remain present.

### 5. Weighted inserted local limits and exact conditioning

The new theorem proves a weighted **central integral** for a specific nontrivial class: complex initial collision-coordinate insertions supported in the section with uniform supremum and BV bounds. The proof smooths this insertion, tracks its distribution-space norm, and estimates all changes using its absolute value. It also covers n-dependent choices with the same norm bound.

It is not an assertion about arbitrary terminal or multiple-time insertions. Nor does it supply the complementary raw tail for the indicated initial class. Corollary 21.4 identifies the exact remaining residual and edge conditions for that class. The statement about changing an exact conditioning event is unchanged: a relative symmetric-difference estimate cannot be deduced from weak convergence or a same-event logarithmic path error.

## Responses to the proof-presentation work

### 6. Semialgebraic BV argument

Appendix A now contains three separate statements. Lemma A.1 gives a fixed finite candidate-center set using the physical horizon and an explicit lattice-count bound. Proposition A.2 states uniform two-dimensional slicing, derives the distributional derivatives by Fubini and integration by parts, and includes endpoint jumps for zero extension. Proposition A.3 explains the fixed rational angular atlas, partition-of-unity gluing, chart-boundary treatment, square-root entry roots and moving rectangle perimeters. Parameter derivatives are not assumed. The concise inherited proof is kept, while the detailed proof is now independently readable.

### 7. Collision-space embedding

Lemma A.4 states the smooth relative-density bound, multiplier bound, test pairing and the smoothed initial-vector estimate in one place. Its proof maps to Demers–Zhang Sections 3.2–3.3, equations (3.11)–(3.13), and checks the weak, stable and matched-curve terms separately. It emphasizes the reference-measure convention: a smooth density `a` represents `a dnu`; one must not insert an additional cosine factor. The retained `COLLISION_INPUT_MAP.md` documents the geometric reparametrization and collision-space source hypotheses. An independent specialist check of that import is still not replaced by a build audit.

### 8. Multi-twist finite-dimensional proof

Lemma B.1 gives an explicit bound for the chronological product, with initial-vector factor `delta^-2`, principal amplitude error `delta^-4 sum|z_j|`, cubic error `delta^-6 sum m_j|z_j|^3`, and complementary error `delta^-2 sum rho^m_j`. The proof expands the finite product and telescopes projectors without introducing a spurious `delta^-2q` loss.

Corollary B.2 substitutes the functional scale. Zero blocks are omitted as identity operators before expansion. Deterministic short increments of length `o(n)` are treated by the actual collision L2 interval estimate, leaving the other increments at their original times. They are not assigned an unjustified long-time complementary decay.

### 9. Coarse-grid tightness

Proposition B.4 isolates the interpolation argument. It treats a fractional block, adjacent blocks, and a general three-piece decomposition by the L4 triangle inequality. Its constants do not grow with the number of coarse blocks. It also gives the deterministic fine/coarse difference and an endpoint convention that extends a full block past the horizon. The previously established fourth moment and residual maximal bound then give tightness of the original process.

### 10. Literature comparison

The introduction now compares tower and invariance-principle Gaussian theory, collision perturbation theory, and cell-index LLTs with the present joint record. Young, Melbourne–Nicol, Demers–Zhang, Szasz–Varju and Demers–Pene–Zhang are cited for their corresponding results, not as sources of the unproved joint raw LLT. The stated contribution is the quantitative, moving-radius central analysis of an actual unbounded induced record through collision compensation, now in an integrated band suitable for exact inversion. We do not claim that existence of billiard CLTs is new.

### 11. Organization and endpoint

The article is not replaced by a specialist Gaussian paper or a different topic. Theorem A remains the synopsis of the established Gaussian chain. Theorem B makes the new central-integral contribution visible at the beginning. A dependency-oriented introduction directs the reader to the periodic geometry, compensation, central band, exact inversion and two proof-detail appendices. Historical proofs and all raw-density criteria remain included. Source provenance and revision responses are kept in supporting files rather than inserted into theorem proofs.

### 12. Independent review

No independent human dynamics review has been obtained in this revision. The manuscript is delivered for subsequent review with the controlling report pinned by commit and blob, complete source, a proof ledger and native-build evidence. Neither finite diagnostics nor a successful workflow is presented as specialist approval or a continuum proof certificate.

## Responses to the technical comments in Section 13

1. **Covariance wording:** Theorem A and the new Theorem B retain positive semidefiniteness. Corollary 21.4 explicitly assumes the additional positive lower bound it needs.
2. **Notation:** `Gamma_R`, `D_R` and the physical covariance remain distinct; no visit-count variable is renamed to one of them.
3. **Frequencies:** Theorem B and the definition (21.1) distinguish rescaled `v` from physical `omega=v/sqrt(n)`; the proof and final remark record both cutoff radii.
4. **Initial density embedding:** Lemma A.4 gives the one reusable norm bound cited in Lemma 21.1 and Lemma B.1.
5. **Complex fourth derivative:** Lemma B.3 records the uniform complementary bound on the complex disk before Cauchy's inequality; no bound on the full principal power for arbitrary complex frequency is asserted.
6. **Zero and short blocks:** Corollary B.2 treats them separately, with their original chronological locations preserved.
7. **Matrix square roots:** Lemma B.5 proves norm continuity on bounded positive semidefinite matrices by uniform polynomial approximation and couples the Brownian laws, including singular limits.
8. **L2 representatives:** The inherited theorem selects no pointwise periodic representative; the new introduction, corollary and ledger preserve this boundary.
9. **Renewal diagram:** It is preserved byte for byte and is not promoted to an anisotropic extension at the undamped boundary.
10. **Different variation norms:** Appendix A and Remark 21.5 distinguish initial-coordinate first variation from second distributional derivatives of residual densities.
11. **Physical-time scope:** The unconditioned displacement/collision functional theorem is preserved without being strengthened to a raw density or an exactly conditioned bridge.
12. **Theorem map and preservation:** The introduction and appendices add a dependency-oriented reading path; all twenty-four inherited core files remain included and byte-identical.

## Delivery and verification

The complete native article has 69 pages, 27 mathematical core inclusions, 91 proof environments and 266 labels. Normal and optimized finite diagnostics agree; source preservation and reference checks pass. The finite tests include every polynomial exponent in the new integrated bound, the analytic-radius restrictions, the strict feasibility threshold, the physical cutoff comparison and fractional interpolation inequalities, alongside the retained physical compensation/counting diagnostics.

These checks do not establish covariance nondegeneracy, an induced high-frequency space or a global coarea branch sum. The revision advances the declared raw problem by proving its integrated central-frequency input and exposing the supporting Gaussian arguments, while leaving those remaining analytical requirements visible for mathematical review.
