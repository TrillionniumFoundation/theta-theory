# Response to the substantive referee: A2-DYN revision 31

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v31-referee-response`  
**Controlling review:** `reviews/a2-dyn-v30-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Review commit / blob:** `cbe93c16bfde35e40b0de647c17d91939cfd6cc1` / `5a92130e7ef47c27cd77d34337e02c02205eccc2`  
**Qualified author baseline:** `a8b400deb4c262bee2978aec3e19cc68aa5439e2`  
**Frozen baseline paper tree:** `7e47c9606ea21b79836319a7fa25d34bdf2a4b3c`  
**Date:** 7 October 2026

We thank the referee for the cumulative review of modules 57--62 and for distinguishing the mesoscopic bridge theorem from the microscopic raw endpoint. This revision returns to the raw-density side of the argument. Its main addition is an exact geometric extraction with a quantified small removed measure and an explicit long-time derivative budget for a new residual. It yields a finite-band inversion formula for the full actual law at fixed lattice labels and bounded roof intervals. These intervals need not grow with the return count.

The title, physical family, actual return section, joint record and microscopic target are unchanged. We retain all earlier window and bridge theorems, without expanding their scope. Theorem V summarizes the new results; complete proofs appear in Sections 55--56, in `core/63_geometric_raw_regularization.tex` and `core/64_microscopic_finite_band_inversion.tex`.

## 18.1. The prescribed-return complement

The new finite integral is explicitly the transform of the full **prescribed-return law**, not the deterministic-collision law:

`I_B(ell,I) = (2*pi)^(-4) integral_{T^3 x [-B,B]} exp(-i u.ell) H_I(b) mu_hat_n^w(u,b) du db`.

Here `H_I(b)=integral_I exp(-i b t)dt`, all three lattice coordinates in `ell` are fixed, and the weight is the original exact weight. Theorem `thm:microscopic-finite-band-reduction` bounds the difference between this finite integral and the actual interval probability. At a linear physical-count cutoff, polynomial regularity budgets allow any prescribed error `O(n^(-P-2))`, with `log B_n=O(n log n)`.

The integral is not yet evaluated as a Gaussian main term plus a small complementary contribution. Balanced small frequencies, compact nonzero torus frequencies, peripheral return phases and the growing roof band below this cutoff remain part of that calculation. We therefore do not claim to have closed the full complementary integral. What is advanced is its far-roof interface at the original fixed-label interval resolution: the infinite integral has a rigorously quantified finite replacement, rather than a cutoff chosen from an uncontrolled jet constant.

## 18.2. The common pointwise correction

Equation `eq:geometric-common-raw-ledger` expresses the same intrinsic correction `R_chi=p^L-K_chi*mu^L` using the new exact extraction. It separates the removed density, its low-frequency convolution, the finite complementary residual integral and the far-roof residual inverse. The table immediately following the equation records each estimate and its exact scope.

The convolution of the removed measure is bounded by its total variation times the kernel supremum. The residual far-roof inverse is bounded by the explicit derivative budget divided by `pi B`. Those terms can be made small quantitatively. The removed density itself has only an `L1` estimate, not a small essential supremum; it may be tall on a very small set. The finite complementary integral also remains to be controlled. Thus neither a small total variation nor microscopic interval inversion is incorrectly promoted to the pointwise common-remainder estimate.

The earlier power--logarithm extraction and coherent cutoff transport are retained. The new extraction is an alternative exact decomposition of the same measure, not an alteration of the record. Its signed identity can still be used to preserve cancellations between the terms that remain to be estimated.

## 18.3. A new long-time derivative budget, before coarea

This is the main new proof.

### A. Uniform transversality of the total roof

For a regular physical word, write the derivative of `T_R^m` in `(alpha,p)` coordinates as `[[A_m,B_m],[C_m,D_m]]`. The positive one-collision differential has determinant one. Both initial row ratios are at most `1+R_+/ell_0=53/6`; a positive matrix product preserves that ratio bound. Hence `B_m` never vanishes and `0<A_m/B_m<=53/6`, independently of the word length and its interior incidences.

The exact action identity then gives

`partial_alpha L_m - (A_m/B_m) partial_p L_m = -R p`.

Consequently `|grad L_m|>=c|p|` uniformly. Removing one thin normal strip in the initial state controls all regular roof critical points simultaneously. The explicitly displayed vector field `X_m=-(Rp)^(-1)(partial_alpha-(A_m/B_m)partial_p)` satisfies `X_m L_m=1`. No critical-value separation or inverse-coarea jet expansion is used.

### B. A cutoff covering every possible first-hit singularity

The one-collision cutoff removes grazing, section boundaries and zeros of every candidate disk discriminant, not just the selected disk's discriminant. This last distinction includes the side of a tangency where the tangent disk is no longer the first hit.

In bounded rational charts for the boundary angle and outgoing angle, each discriminant has a positive bounded denominator and a polynomial numerator of degree at most eight. Its coefficient norm is bounded below uniformly over the radius interval. The paper proves an elementary two-variable polynomial sublevel lemma by one-variable interpolation and Fubini. It gives the safe exponent `1/16`. The other cutoffs remove only finitely many strips.

Multiplying these one-collision cutoffs along all collision times through `L`, and adding the initial normal cutoff, removes measure at most `C(L+1) epsilon^(1/16)`. This estimate follows from invariance and a union bound, not from multiplying a small per-word mass by an uncontrolled word count. The cutoff is zero on both sides of every finite itinerary and section-decision boundary. Its fixed-order derivatives and those of the transverse field are bounded by `exp(C(L+1)log(C/epsilon))`.

### C. All-label second derivatives without a cell-count loss

For a fixed product of bounded-BV return-state marks, smooth each mark before composing it with its actual return. The total source error is `C epsilon V`; no BV norm of a long pullback is presumed. Define the residual by pushing forward the smoothly weighted, whole-itinerary cutoff. The difference from the exact finite-count law is the extracted measure.

On each regular initial piece the actual return count, lattice label and collision index of every mark are fixed. Both density derivatives are pushforwards of divergences in the field `X_m`. No boundary terms occur because the cutoff vanishes on neighborhoods of all relevant boundaries. The source pieces are disjoint. Summing the absolute source integrals over all words and output labels therefore pays the area of the initial cylinder, not the number of cells.

The resulting estimates are

`||E_epsilon||_TV <= C_q [epsilon V + M(L+1)epsilon^(1/16)]`,

`A_{2,epsilon} = sum_ell ||partial_t^2 q_epsilon(ell,.)||_1 <= C_q M exp(C_q(L+1)log(C_q/epsilon))`.

For the original weight one, both terms are positive. For complex or signed marks the exact decomposition and variation estimates remain valid. All first-hit, grazing, return-decision and dynamically generated singular-image contributions are retained in the extracted measure; none is silently omitted.

### D. Linear cutoffs and a genuine far-roof estimate

At `L_n=ceil(lambda n)` with `lambda>a/c`, choose `epsilon_n=epsilon_0 n^(-d)` for a fixed sufficiently large `d`. The removed variation, including the high-count tail, is `O(n^(-P-4))`, while the residual second-derivative bound has logarithm `O(n log n)`. The paper gives a formula for `B_n` from this proved upper bound; it does not use an unknown measured value of `A_2`.

The pointwise residual tail is at most `A_{2,epsilon}/(pi B)`. For a time-interval probability its tail is at most `A_{2,epsilon}/(pi B^2)`. Replacing the residual by the full law inside the finite interval integral costs only `O(delta log(1+B|I|))`, not `O(delta B)`, because `|H_I(b)|<=min(|I|,2/|b|)`. This is why a polynomially small removed measure suffices at a bandwidth whose logarithm is `O(n log n)`.

The new bound is for a different exact residual. We have not proved the same bound for the inherited power--logarithm jet residual, nor have we proved a compatible finite-band spectral estimate all the way to `B_n`. Those two assertions are not hidden in the notation of the new theorem.

## 18.4. Weighted microscopic denominator and physical-event replacement

The geometric theorem applies to a fixed product of bounded-BV functions at specified actual return marks, including repeated marks, with explicit product and variation budgets. It does not require those functions to be subanalytic. For a single mark, the raw extraction and inherited Fourier estimates therefore have a common BV input class without the earlier additional finite-record condition for this alternative extraction.

The microscopic finite-band formula fixes the three lattice labels and allows bounded time intervals, including shrinking intervals. Its error is absolute. It does not supply a positive Gaussian denominator, and it does not by itself compare the original physical-time event with the completed-return event. The multi-return BV class is not silently identified with arbitrary path selectors or exact physical-time indicators. Theorem U still concerns fixed interior cylinder selectors with physical endpoint half-width `t^(21/50)`.

## 18.5. Imports and independent specialist verification

The added geometric input is the ordinary one-collision differential. It is written explicitly, checked by changing from arc-length/outgoing-angle coordinates, and referenced to Stenlund--Young--Zhang, Section 3.1. The remainder uses existing exact action, finite horizon, BV smoothing, invariance and cumulative-return tails. The polynomial sublevel estimate, cutoff construction, source-side integration by parts and microscopic inversion are proved in the new text.

The most important independent checks are the all-candidate tangency guard, uniform rational degree and coefficient bound, zero extension across all finite branches, derivative supports, and the summation over disjoint source pieces. The finite diagnostics do not certify these continuum assertions. No independent human specialist review is claimed.

## Presentation comments 1--13

The source chronology and all inherited scopes are retained. Theorem U remains explicitly mesoscopic. The new theorem is identified as a prescribed-return **finite-band reduction**, not a proved complementary estimate. Signed-window bounds keep the absolute value outside the integral. The three levels of cutoff transition, signed averages and pointwise correction remain separate.

All previous fixed block counts, expansion orders, coarse/fine tightness payments and stationary length-bias distinctions remain unchanged. Fixed cylinder selector hypotheses are unchanged. A new main-text paragraph groups the narrative into collision inputs, raw inversion and physical conditioning without deleting the inherited theorem statements. The final raw equation now has its own term-by-term ledger in the mathematical text. Execution and proof status remain separate.

## Source preservation and qualification

All 62 inherited core files and all 63 inherited Python files are byte-identical to the qualified v30 baseline. All 813 inherited mathematical labels remain. Six exact main/bibliography edits add revision identity, the new abstract sentences, Theorem V, its two inputs, the conceptual roadmap and one primary reference. Earlier bibliography entries remain unchanged. The exact edit ledger is replayed by the verifier.

Normal and optimized finite checks cover the canonical collision matrix, 100 positive matrix products, the degree-eight rational discriminants, divergence signs, the strict long-time exponent budgets, and 72 high-precision actual physical words of lengths 1, 2, 4 and 8. Negative controls retain the distinction between small mass and small density and reject an unconverted angle-coordinate determinant. These are diagnostics, not a mathematical certificate.

Final qualification builds ordinary committed source at one exact SHA and records the run identity, source hashes, PDF hash and proof-page renders. Neither the initial review-export job nor a source transport is presented as the final qualification. The new raw-geometric results are offered for further substantive review of the same microscopic endpoint.
