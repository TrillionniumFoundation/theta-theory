# Response to the referee: A2-DYN revision 25

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v25-referee-response`  
**Controlling report:** `reviews/a2-dyn-v24-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Report commit / Git blob:** `92a8236e149c79c797fa85dacf5953e69b8960ff` / `9f58ef5d84b9e91d5eadd8d4a49317158db695e0`  
**Reviewed author baseline:** `c1d6940a875f501ee1957204e81772df7b9b39d6`  
**Baseline ordinary paper tree:** `f15ab9854d022319db374f8ce38f4e6a4273dd84`  
**Date:** 7 October 2026

We thank the referee for the substantive review of the recovered damped-unsmoothing arguments and the multiscale fixed-count revision. The new revision preserves the physical family, actual section, joint record, all preceding theorems, and the raw mixed-density objective. Its main addition is a prescribed-count Fourier theorem with independently chosen coordinate widths, based on a high-order damped removal of smoothing. It is stated as Theorem O and proved in full in two new sections. A new appendix supplies the requested dependency chart.

The preceding isotropic band is retained, not replaced by an elongated box. The central comparison is proved on their union. The new result controls an additional four-dimensional frequency region beyond that band, without count averaging or division by its volume. It does not assert that this union contains the entire farther isotropic annulus.

## A. Further fixed-count complementary frequencies

### A.1. Fixed arbitrary-order residual moments

`lem:all-small-mass-moments` proves, for each fixed integer P and each centered small-mass BV residual u,

`E|S_m u|^(2P) <= C_P sum_{b=1}^P (m delta)^b L_delta^(2P-b)`.

This follows from the already proved small-mass cumulants by the finite moment-partition identity. A partition with b nonsingleton blocks contributes exactly b factors of m delta and logarithmic exponent 2P-b. All terms are kept, including the b=1 connected term. No convergence of an infinite cumulant series, factorial control uniform in P, or growing-order limit is assumed.

`thm:high-order-damped-unsmoothing` then retains all residual degrees through 2P-1 inside a fully damped chronological word. The mark and the residuals are smoothed at the fine scale epsilon; the twist still uses only the coarse scale delta. With spectral degree Q fixed independently of P, the bound contains:

- a damped term `C M_a epsilon^(-4P) (1+m|z|)^(2P-1) exp(-c m|z|^2)`;
- fine insertion and residual-replacement errors;
- the full small-mass moment sum multiplied by `M_a |z|^(2P)`.

Repeated multiplier times and endpoint marks are included as zero-length powers. The sum of twisted power lengths is exactly m. At P=2 this recovers the inherited cubic theorem with the same epsilon^(-8) loss and both fourth-moment terms.

### A.2. Separate-width theorem and explicit feasibility

For rescaled half-width exponents theta_i, write theta_* = max theta_i and Theta = sum theta_i. The new fixed-count theorem applies when

`min theta_i >= 1/200`, `theta_* < 1/10`, and `Theta + theta_* < 1/4`.

Its raw integral over the box outside the original small central ball is at most

`C (M_a n^(-eta) + V_a n^(-sigma))`,

for any fixed `0 < eta <= 1/4 - Theta - theta_*`, with sigma increased by choosing a finer multiplier scale. These are integrals of the actual transform at the prescribed count n and mark k, with the full raw n^2 factor. The four-dimensional Jacobian is kept exactly.

The proof supplies a nonempty parameter choice, not only formal inequalities. Choose

`2 theta_* < alpha < 1/4 - theta_*/2`,

then fixed P,Q such that

`P(alpha-2 theta_*) > Theta+eta`,

`(Q-1)(1/2-theta_*) > 2 alpha(Q+1)`.

The two ends of the alpha interval are ordered precisely when theta_*<1/10. The fine exponent beta is chosen afterward to dominate all fixed polynomial residual factors. Every choice is made before n varies.

This separates the four-dimensional volume cost from the largest frequency cost. It is a sufficient family of estimates, not an optimality result or a claim about the full isotropic endpoint.

### A.3. A concrete flight-time extension

Theorem O uses

`theta=(1/100,1/100,1/100,9/100)`,

with coarse exponent `alpha=19/100`, residual moment parameter `P=16`, spectral degree `Q=29`, and fine exponent `beta=20`. The residual Taylor degree is 31; it is deliberately distinct from spectral degree 29.

The physical region is

`|u_1|,|u_2|,|s| <= 2 n^(-49/100)`, `|b| <= 2 n^(-41/100)`.

The rescaled half-widths are `2 n^(1/100)` in the first three coordinates and `2 n^(9/100)` in the flight-time coordinate. On this box outside `|z|<2 n^(-99/200)`, the exact prescribed-count estimate is

`n^2 integral |Phi_n^(mark,a)| <= C (M_a n^(-1/40) + V_a n^(-497/25))`.

The analytic margins are 3/100 and 2/25. The fine residual exponent is 159/100; the leading residual and integrated stopping exponents are both 1/25. The logarithm of degree 16 in the paired residual is absorbed by the strict margin to 1/40. The other fifteen moment terms have faster powers and their own fixed logarithms.

The old central rate `n^(-3/280) sqrt(log n)` and separated variation cost `n^(-9/175)` hold on the box and on its union with the entire preceding isotropic ball of radius `2 n^(67/1400)`. The flight-time exponent 9/100 is strictly larger than 67/1400. Thus the union contains new frequencies while preserving all previously proved ones. The full isotropic rescaled ball of radius n^(1/10), compact nonzero torus regions, full peripheral regimes, and growing/far-roof splice are not claimed covered.

## B. Long-time finite-count preparation

The exact finite-count extraction remains unchanged. The new higher moments are moments of a bounded collision sum, not second derivatives of a pushed-forward density. They neither bound germ radii and coalescing critical values uniformly at L_n proportional to n nor bound the complete `A_2(n,L_n,R,w)` sum. The full long-time preparation estimate requested by the referee remains a separate analytical responsibility. Its source, weight, count, and parameter dependence are retained in the new raw inequality.

## C. Active-kernel local edge correction

The coordinatewise cutoff is defined by `chi_n^box(omega)=product_i chi_0(omega_i/B_{n,i})`. The new raw corollary defines `E^box` and `C^box` with this exact kernel immediately before use. It does not borrow either quantity from an earlier isotropic cutoff or identify the box kernel with the union of two Fourier supports.

The count-support correction is recomputed: `n^2 product_i B_{n,i}=n^(3/25)` and `n B_{n,3}=n^(51/100)`. It is therefore bounded by `C_J M_a n^(3/25-51J/100)` and is smaller than any fixed inverse power after selecting the fixed Schwartz order J. The missing Gaussian tail is `C M_a exp(-c n^(1/50))`.

The combined edge correction `n^2 E^box`, finite-band residual integral, and far-roof term `n^2 A_2/(pi B)` remain explicit. The local edge term may be infinite before uniform germ estimates. The new identity is not claimed to prove its asymptotic smallness.

## D. Weighted raw denominators

All new Fourier statements use the same bounded-BV single actual-return insertion, with the unnormalized restricted collision measure and mass alpha_a. The raw corollary additionally requires finite-record admissibility of that exact weight. It does not identify this intersection class with arbitrary L2 weights in count averages or with the downstream physical indicators.

The same-event central comparison on the enlarged union is divided by the identical event probability. It preserves the previous sufficient conditions `beta_0<3/280` and `beta_0+kappa_0<9/175`. This is not a raw-scale exact denominator asymptotic, which still requires the weighted outer, preparation and edge estimates for the actual observation class.

## E. Relative physical-event replacement

No physical event is replaced in this revision. The prior Lq clock comparisons and the new high-order residual moments do not assert a relative symmetric-difference bound under an exact rare lattice constraint. The original lattice coordinate, continuous time window, and required denominator scale remain in the physical conditioning task.

## F. Specialist verification and external inputs

The new argument introduces no external collision-space theorem. It uses the existing BV smoothing lemma, fixed-order connected-correlation estimates, real-frequency damping, multiscale stopping, and exact count-localized extraction. `HIGH_ORDER_INPUT_MAP.md` records the dependency and scale used at every step. The existing external maps remain intact. The cumulant identity is finite algebra; the normal-approximation survey cited in the bibliography is not used as a substitute for a uniform all-orders theorem.

The next substantive review should examine the fixed-order small-mass partition sum, the chronology of up to 32 smooth multipliers, the independence of the two expansion degrees, the separate-width exponent inequalities, and the new count-kernel calculation. Finite checks and native compilation do not certify these continuum operator inputs or supply independent human review.

## Presentation comments 1--20

The recovered v23 history is retained in `HISTORICAL_DERIVATION_AUDIT.md`, with its ordinary tree distinguished from its assembly-only branch. All earlier modules and Theorems A--N remain unchanged. The actual mark remains prescribed, and the earlier moderate/far clock-tail split and fixed-order quantifiers are preserved.

The requested heterogeneous cumulant calculation is now explicit in `lem:heterogeneous-cumulant-comparison`: it expands the change of every partition product and gives the centered four-variable example with one marked factor. The parity definition remains beside the moment discussion. The distinction between the collision absolute covariance series and induced Cesaro identity is preserved.

The new proofs keep coarse scale delta, fine scale epsilon, spectral degree Q, residual parameter P and Schwartz order J separate. Both physical and rescaled widths appear beside every new frequency conclusion. The old small-ball and isotropic theorems are retained. The new theorem is explicitly a box/union estimate rather than a full-annulus statement. It does not use the spectral Cauchy limit at growing test frequency.

The raw corollary recomputes its active-kernel edge term and count-separation powers, preserves the finite-record weight restriction, and uses extended-real inequalities when required. Appendix `app:dependency-guide` gives the requested chart separating proved outputs, their inputs, and the remaining raw requirements. The exact edit ledger records every inherited change; successful CI remains execution evidence, not publication or proof certification.

## Source preservation and qualification

The revision inherits all 51 core modules and every inherited Python source byte-for-byte, as well as the unchanged bibliography. Only six exact replacements in `main.tex` add the new synopsis, proof-route pointers, source inputs and revision identity. Three new core files contain the two complete mathematical sections and the dependency appendix. The verifier checks the exact baseline paper tree, all old labels, every file hash, and the controlling report blob. Normal and optimized finite checks must agree; the read-only exact-SHA workflow builds the full article and emits a run-bound PDF receipt. No future workflow is predeclared successful here.
