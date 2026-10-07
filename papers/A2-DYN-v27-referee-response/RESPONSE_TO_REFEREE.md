# Response to the latest referee: A2-DYN revision 27

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revised directory:** `papers/A2-DYN-v27-referee-response`  
**Controlling report:** `reviews/a2-dyn-v26-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Report commit / blob:** `20337e845157a833fe770687ea98f337788fa586` / `f75e48fa7276be7be654c61afe3cc276ba44d514`  
**Reviewed author baseline:** `6a790b65b48f57d264dbc7871bd1ae46571c2662`  
**Baseline ordinary paper tree:** `6101fe93f514d9586658d748e08a0ffd6c610044`  
**Date:** 7 October 2026

We thank the referee for distinguishing a bound for the common raw correction from a bound for a change between cutoffs. This revision establishes a size estimate for the common correction tested on actual unsmoothed windows, proves the corresponding rare-event denominators, and makes a relative comparison with observations at deterministic physical time. The added conclusions are Theorems R and S. Neither is identified with the remaining microscopic raw local limit theorem.

The title, Lorentz family, actual section, joint four-coordinate record, and raw mixed-density objective are unchanged. All 56 inherited core modules and every inherited theorem label are retained. No claim is replaced by a different topic, and the suggestion to lower the submission target or reorganize around a specialist endpoint is not adopted. The author revision advances explicit parts of the original program while distinguishing its new theorems from its remaining proof obligations.

## A. Remaining prescribed-count Fourier complement

We retain the measurable-shape theorem and its explicit dyadic cross with the same fixed expansion orders and constants. The cross is not re-described as the full isotropic one-tenth ball. The new results use only Fourier boxes contained in the already proved union, at a prescribed return count, with no frequency averaging over that count.

The new mechanism is order-preserving Fourier approximation of an exact window indicator. Lemma `lem:window-interval-envelopes` reconstructs the Beurling--Selberg envelopes, proves the sign inequality from the sinc-squared partition, establishes Fourier support distributionally, and verifies the endpoint values. The last check matters for the three discrete coordinates. The multidimensional minorant is a product of majorants minus a sum of nonnegative error terms, not a generally false product of minorants.

This converts the known integrated characteristic estimate into an actual window probability estimate. It does not extend the full Fourier complement. Balanced unresolved frequencies, compact/peripheral regimes, growing roof frequencies, and the far-roof splice remain requirements of the original pointwise raw theorem.

## B. A size estimate for the common signed raw correction

Theorem `thm:averaged-common-raw-remainder` is not another transport theorem. For any one retained cutoff, a central observation box `B`, and the exact finite extraction at a linear count cutoff, it proves

`(n^2 / m(B)) | integral_B R_chi^{a,L_n} dm |`

`<= C [ E_n(a) + M_a sum_i (b_i h_i)^(-1) + M_a n^(-P) ]`.

Here `m` is counting measure times Lebesgue measure, `h_i` are standardized observation half-widths, `b_i` are rescaled coordinate bandwidths whose product box lies in the proved Fourier union, and

`E_n(a)=M_a n^(-3/280) sqrt(log(2+n)) + V_a n^(-9/175)`.

The absolute value is outside the integral. This estimates the common correction itself as a signed average; it does not estimate its absolute integral or essential supremum.

The argument is direct. Positive Fourier envelopes first bound the exact probability of the unsmoothed box. The full-law low-frequency convolution has the same Gaussian mass by the inherited integrated estimate. The high-count measure has no mass in the central box, and its convolution is controlled using the actual third-coordinate count gap. Subtraction in the exact density identity gives the stated bound. Positive and negative parts of real and imaginary insertions extend the result to the original complex marked weight class intersected with finite-record admissibility.

A concrete consequence has standardized half-width `n^(-1/25)` in each coordinate and therefore physical half-width `n^(23/50)`. The normalized signed average is `O(M_a n^(-11/1400) sqrt(log n) + V_a n^(-9/175))`. This is a genuine size bound beyond cutoff independence. It does not imply `n^2 ||R_chi||_infinity -> 0`; local oscillation at finer resolution remains an additional responsibility.

## C. Long-time density preparation

The new common-correction estimate does not use `A_2(n,L_n,R,w)`. It preserves cancellation and uses positivity instead of separate absolute edge and residual estimates. Thus no new long-time density-jet bound is needed for the proved signed window average.

The estimate does not remove the need for a far-roof or equally strong local argument in the microscopic theorem. The finite-count preparation, all singular and image-boundary contributions, and their genuine long-time dependence remain intact. In particular, the new moment argument is not presented as a bound for inverse-coarea second derivatives.

## D. Actual unsmoothed denominators

Theorem `thm:unsmoothed-window-denominator` applies directly to bounded-BV marked functions. For a nonnegative mark, its amplitude is its exact mass `alpha_a`, and its relative error is controlled by `E_n(a)/alpha_a + sum_i (b_i h_i)^(-1)`. There is no additional reciprocal loss from the volume of the observation window. For complex marks the absolute estimate is obtained by positive-part decomposition; a complex amplitude is never used as a probability denominator.

The proof compares the continuous Gaussian integral with its actual mixed lattice/time Gaussian mass and pays the grid error `sum_{i<=3}(sqrt(n) h_i)^(-1)`. The integer endpoints are not replaced by a continuous law.

For the original section law and four equal half-widths `n^(-1/25)`, the exact probability is

`16 n^(-4/25) g_{D_R}(xi) [1+O(n^(-11/1400) sqrt(log n))]`.

This is a denominator theorem for a genuinely rare, unsmoothed event. It does not assert a denominator at one fixed lattice label: the resolution condition fails for a singleton when every available bandwidth is `o(sqrt(n))`.

For the physical application, Lemma `lem:projected-window-denominator` obtains a three-dimensional denominator without restricting a four-dimensional L1 Fourier bound to a measure-zero plane. It adjoins a fourth coordinate, truncates that coordinate at `T=n^(1/400)`, applies four-dimensional envelopes, and removes the truncation with the already proved 64th moment. The Gaussian envelope error uses its decay in the fourth coordinate rather than paying a spurious factor `T` in every boundary term. All matrix, moment and exponent constants are uniform in the radius.

## E. Relative comparison at deterministic physical time

Theorem `thm:relative-physical-window` makes a relative comparison between three different events on the same section-start probability space: the projected record at `n_R(t)=floor(c*t/mean(tau_R))`, the projected record at the actual last completed-return index, and the actual displacement/collision fluctuations measured at deterministic physical time `t`.

The proof first derives a maximal centered return-window estimate from fixed moments and invariance. An inverse-clock window of size `t^(5/8)` and a centered-increment threshold `t^(3/8)` then yield, for every fixed `P`, a coupling failure probability `O_P(t^(-P))`. The unfinished return is handled by a union bound using its actual exponential tail. No induced mixing or conditional independence is assumed.

For exact three-dimensional boxes with physical half-width `t^(23/50)`, the probability of each event equals

`8 t^(-3/25) g_{V_R}(xi) [1+O(t^(-11/1400) sqrt(log t))]`.

Their symmetric difference divided by the proved return-event denominator is `O(t^(-11/1400) sqrt(log t))`. The corresponding conditional initial laws converge in total variation at this rate; hence every common bounded path statistic can be transferred. The proof compares enlarged and contracted boxes instead of applying an unavailable Fourier estimate to an unresolved thin boundary slab.

This is a relative, not merely absolute, physical-event comparison with a verified denominator. Its scope is explicit: a section-start law and the stated mesoscopic integer/time windows. The stationary-suspension, fixed-label and exact microscopic constraints of the original downstream raw application are not declared covered. No event in that application is silently replaced by one of the new windows.

## F. Independent verification and imports

The new interval-envelope argument is written out, including support, mass and endpoint conventions. Carneiro--Vaaler's primary paper is cited for provenance of the classical construction, not as a new billiard theorem. The dynamical inputs are the inherited fixed-count Fourier estimates, uniform ellipticity, all fixed actual-return moments, return-map invariance, and exponential return tails. No new anisotropic multiplier or distribution-to-function reconstruction is assumed.

The main expert verification targets are the order-preserving tensor minorant, the mixed-grid comparison, the signed-average normalization, the four-dimensional projection/truncation budget, the deterministic return-window maximum, and the actual physical clock comparison. Source checks, finite numerical tests and successful typesetting are not independent continuum proof certification.

## Presentation comments 1--20

Comments 1--9 and 13--16 are retained literally in their original mathematical modules: measurable shape versus concrete cross, incomplete one-tenth ball, physical/rescaled coordinates, fixed expansion orders and connected block, dyadic logarithm, cutoff versus sharp indicator, third-coordinate count separation, weight-class intersections, same-event versus changed-event conditioning, and collision summability versus induced Cesaro covariance. The new section defines the common correction through the existing exact identity before using its integral, and consistently places the absolute value outside that integral (comments 10--13). The original extended-real absolute quantities are not subtracted.

The manuscript abstract states the new scope and the remaining microscopic endpoint. Its previous version is preserved as `HISTORICAL_ABSTRACT_v26.md`, alongside the already retained historical abstract (comments 17--18). A compact verification roadmap has been added in the main text (comment 20). The optional diagram in comment 19 is not necessary to any proof; the inherited explicit inner/outer region descriptions remain, and the new windows display both frequency and observation scales.

## Source preservation and qualification

All 56 inherited core files and all 52 inherited Python files are byte-identical. Every old theorem label and bibliography entry remains. Six exact edits to the main article and bibliography are replayed by the verifier. The new proof modules are `core/57_unsmoothed_window_remainders.tex` and `core/58_relative_physical_windows.tex`. `SOURCE_MANIFEST.json` records actual hashes, baseline identity and the controlling report blob. The final qualification workflow is read-only and builds ordinary committed source; no assembly runs during that qualification.

This revision supplies real denominator, signed-average and relative physical-window theorems while retaining the full original raw local limit objective. It does not claim that the remaining microscopic common remainder, complete complement, long-time derivative budget or fixed-label conditional endpoint has been proved.
