# Response to the v25 referee: A2-DYN revision 26

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v26-referee-response`  
**Controlling report:** `reviews/a2-dyn-v25-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Report commit / blob:** `b9d11ff3bc2c08bb7410d93d3128d847e277cc08` / `c24a1e7273ad3be3a233c9b3e55d32660659e9ee`  
**Reviewed v25 author SHA:** `4c07267338175932688a20a6021dae1b602074a0`  
**Reviewed ordinary paper tree:** `5c5378441102a155ccbf76f4b7f18d426390d3a9`  
**Date:** 7 October 2026

We thank the referee for the detailed analysis of the arbitrary fixed-order theorem, the coordinatewise frequency geometry, and the raw extraction. The revision retains the physical problem and every inherited core result. It makes two connected additions: one fixed-count estimate on a larger nonrectangular region, and a quantitative theorem transporting the same signed raw correction between the old and new cutoffs. The latter addresses the concern in presentation comment 20 that successive frequency extensions should not create disconnected raw interfaces.

The new statements are Theorems P and Q. Both have full proofs in `core/55_shape_adaptive_fixed_count.tex` and `core/56_coherent_raw_cutoff_transport.tex`. No external theorem about a new billiard realization or all-order analyticity is imported.

## A. The prescribed-count complementary region

### A.1 A uniform estimate for measurable shapes

Theorem `thm:shape-volume-criterion` replaces a fixed four-width vector by three geometric bounds: maximal rescaled radius `C n^(9/100)`, volume `C n^(41/175)`, and first radial moment `C n^(67/280)`. It proves the raw-normalized integral outside the original central ball is at most

`C[M_a n^(-3/280) + V_a n^(-5559/175)]`.

The constant is simultaneous for every measurable shape with those bounds, even when the shape depends on n. It does not apply a fixed-exponent theorem to n-dependent exponents without controlling its constants.

The proof uses the inherited high-order damped theorem with fixed P=26 (residual Taylor degree 51), Q=29 (spectral degree), coarse scale n^(-19/100)/4, and fine scale n^(-32)/4. Analytic margins are 3/100 and 2/25. The worst residual block has margin 9/350, exceeding the required 3/280 by 3/200. All block counts 1 through 26 are retained. The fine multiplier scale is not inserted in the twisted operator.

### A.2 A single nonrectangular domain

Let a_n=2 n^(1/200), U_n=n^(9/100), and T_n=n^(67/280)/log(2+n)^3. Include all dyadic boxes with coordinate scales lambda_i=a_n 2^(j_i) satisfying `(product lambda_i) max lambda_i <= T_n` and `max lambda_i <= U_n`.

The number of integer tuples at sum-plus-maximum t is O((t+1)^3). Summing their weighted volumes costs log(2+n)^3, and exactly that loss is paid in T_n. This proves the required volume and first-moment bounds with no additional logarithm in the final rate. The same P and Q work for the entire union.

This region adds axial frequencies of physical order n^(-41/100) in every coordinate, including both displacements and collision count, not only flight time. It also adds genuinely mixed directions; for example the rescaled exponent vector (1/25,1/25,1/25,1/20) is eventually contained. The entire preceding isotropic ball and roof box are retained explicitly in the union, with the original central error.

### A.3 What this does not yet prove

The region is not the complete isotropic ball of rescaled radius n^(1/10). A vector with all four coordinates of order n^(3/50) remains outside it and both retained sets. Compact nonzero torus frequencies, full peripheral regimes and growing/far roof frequencies still require control. We do not label the new theorem a complete complementary integral or describe a nonrectangular union as a larger sphere.

## B. Long-time derivative sum at linear count cutoff

The genuine A_2(n,L_n,R,w), with L_n proportional to n, is not bounded by the dyadic argument or the collision moment estimates. Its full prepared-germ budget remains present in the new raw identity with coefficient n^2/(pi B). The new cutoff-transport theorem avoids introducing a second uncontrolled derivative budget merely to compare two cutoffs, but does not establish the first one. All finite-preparation and regular-critical calculations remain unchanged.

## C. Active-kernel local edge correction

The new kernel is a nonnegative frequency subsum of a product dyadic partition. Its count-coordinate tail is proved directly, with the physical base count scale 2 n^(-99/200). It gives

`n^2 sup |K_sharp * high_count_tail| <= C_J M_a n^(41/175 - 101J/200)`

on the original central windows. The kernel does not use the larger roof width in place of the third-coordinate scale.

The isolated active edge correction remains explicitly defined immediately before use, with extended-real qualification. We do not infer its smallness from another kernel. Instead the new exact identity compares the sum of edge correction and residual inverse before taking absolute values; that is the more relevant quantity for changes of cutoff in the raw law.

## D. The finite-band residual and exact cutoff transport

For one fixed extraction mu^L=E+Q, define

`R_chi = e - K_chi*E + F^{-1}[(1-chi) Q_hat]`.

Absolute residual inversion proves exactly

`R_chi = p^L - K_chi*mu^L`,

and hence

`R_chi - R_psi = (K_psi-K_chi)*mu^L`.

The changes of E and Q combine into the full law; no separate large coefficient from E survives. The difference is bounded and continuous even when an individual correction has unbounded essential supremum. The almost-everywhere density identity is formed before norms, so no subtraction of two infinite norms is used.

For the dyadic, old box and old isotropic cutoffs, their difference vanishes on the original central ball and is supported in the union of the proved regions. The full-law fixed-count estimates therefore bound the entire normalized signed transition by

`C[M_a n^(-3/280) + V_a n^(-983/350)] + C_P M_a n^(-P)`

on central windows. Exact count-coordinate support bounds the high-count convolution; no estimate of a raw tail density from its total mass is attempted. Under the stronger cumulative-tail slope the comparison is global with an exponential remainder.

This is an unconditional, vanishing bound for the complete change-of-cutoff term. It connects rather than replaces the preceding raw identities. Local smallness of the signed common correction for one of the three kernels is equivalent to its smallness for the other two under the displayed weight budget. Neither isolated edge smallness nor absolute residual-integral smallness follows from a signed cancellation. The absolute finite-band estimate requested by the referee is still a separate obligation.

## E. Weighted raw theory

The Fourier theorem continues to use a single bounded-BV function of an actual marked return. Raw extraction additionally requires finite-record admissibility of c* a composed with that return iterate. The cutoff-transport theorem uses their intersection and the identical weight and extraction on both sides. It establishes neither a new denominator asymptotic nor automatic stability of every physical path indicator under all operations.

For the unchanged marked-state event, division by its exact probability gives the retained central rate on the enlarged union. The old probability and variation budgets remain beta<3/280 and beta+kappa<9/175. This is not a raw denominator theorem.

## F. Relative physical-event replacement

No event is replaced. The exact indicator and its probability remain unchanged. The relative comparison of completed-return and exact physical-time/lattice observations at the raw denominator scale remains required. The new cutoff identity compares different analysis kernels for one measure, not different physical events.

## G. Verification and presentation

All 54 inherited core files, inherited Python files and references.tex are byte-identical. Five exact replacements affect main.tex only; all old labels and Theorems A--O remain. The inherited dependency appendix is retained. The introduction distinguishes the new signed transport theorem from the still-needed absolute edge estimate. The abstract is editorially consolidated to avoid an isolated title page; its full original text is preserved verbatim in HISTORICAL_ABSTRACT.md, and every original mathematical result remains in the article.

The next specialist should check the simultaneous fixed-order constants through order 52, the shape-independent stopping integration, the dyadic shell count, the multiplier scale separation, the mixed lattice/real kernel convention and the sign in the raw correction cancellation. Finite diagnostics test exact exponents, shell counts, partition plateaux, high-count scale bounds and Fourier cancellation identities, including negative controls. They are not continuum proof certification.

Presentation comments 1--19 are preserved explicitly: both frequency scales, separate fixed residual/spectral degrees, connected block b=1, retained old sphere and box, count coordinate third, exact active-kernel definitions, extended-real qualifications, weight-class distinctions, same-event conditioning, Cesaro terminology and exact-source accounting. Comment 20 motivates the new raw-transport theorem. It closes the transition contribution but not the common raw remainder; we state that boundary directly rather than multiplying interfaces or claiming the organizing LLT is finished.

The new exact-SHA workflow is read-only. Static records do not predeclare a future run successful; its dynamic receipt and source artifact bind the actual checked-out SHA, run ID and compiled PDF.
