# Response to the substantive referee: A2-DYN revision 29

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v29-referee-response`  
**Controlling report:** `reviews/a2-dyn-v26-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Report commit / blob:** `20337e845157a833fe770687ea98f337788fa586` / `f75e48fa7276be7be654c61afe3cc276ba44d514`  
**Immediate parent:** `b9b976cd93df7513018f03dea0df5ffe80920e01` (v28 source snapshot)  
**Mathematical/source baseline:** staged v27 ordinary paper tree `ae335b52f013e3569e4a6b79b899cfc00e26b8e4`  
**Date:** 7 October 2026

We thank the referee for separating the common raw correction, prescribed-count Fourier complement, and relative physical-event problem. The repository contains a v27 window revision and a v28 snapshot of that source, but no later substantive report was found in the inspected A2-DYN review branches. We therefore continue the v26 report from the latest retained source rather than invent a v27 or v28 review. The snapshot is not presented as an earlier successful article qualification.

The v27 source has been checked against its exact v26 baseline, with its complete window and section-start arguments retained. The present new result is Theorem T: a stationary physical window denominator, relative event comparison, and conditional-law comparison at finer mesoscopic resolution. We keep the title, physical family, return section, joint record, and raw microscopic endpoint. The suggestion to replace that endpoint by a specialist-paper topic is not adopted.

## A. Prescribed-count complement: what is advanced and what is not

Theorem `thm:wide-collision-band` proves a full isotropic band on the deterministic collision clock, with rescaled radius `C m^(9/100)` and physical radius `C m^(-41/100)`. It applies to bounded-BV initial collision functions. Its integrated Gaussian error is `O(m^(-3/280) sqrt(log m))` at a fixed regularity budget.

The proof explicitly removes only the stopping loss because no return stopping occurs in this transform. It uses the inherited damped-unsmoothing theorem with residual order `P=40`, spectral order `Q=29`, coarse scale `m^(-19/100)/4` and fine scale `m^(-50)/4`. The residual polynomial has degree 79 and at most 80 smooth insertions. The largest integrated residual-moment power is `-1/25`, leaving margin `41/1400` over the retained central rate; every block number, including the connected `b=1` term, is included. Both analytic damping inequalities have strict positive margins. These are fixed, not growing, orders.

This estimate is not described as a new prescribed-return-count domain. Theorem P's shape restrictions and Theorem Q's cutoff cancellation remain exactly as in the reviewed article. Balanced unresolved return directions, compact nonzero/peripheral frequencies, growing roof frequencies and the far-roof splice remain required for the full prescribed-count complement. The new collision band is used at the physical clock through explicit coupling, rather than asserted to control the return transform at frequencies where stopping is expensive.

## B. The common signed raw correction

The retained v27 Theorem R provides an actual size estimate for the signed window integral of one common correction, rather than only the difference between cutoffs. We checked and preserve its endpoint-safe envelopes, positivity argument, mixed-grid normalization and count-coordinate separation. The absolute value remains outside the integral. It does not imply the pointwise common correction requested in the report.

No pointwise raw correction or isolated absolute edge estimate is claimed by Theorem T. The new stationary denominator is obtained from a collision-clock probability estimate, not from a false inference that the common signed raw correction has become small in essential supremum. The exact coherent density identity remains part of the original microscopic program.

## C. Long-time preparation and derivative budget

All finite-count critical/singular extraction and residual-inversion modules remain unchanged. The new proof uses no estimate for the inverse-coarea second derivative sum at a linear cutoff. It neither infers such a sum from collision moments nor hides its dependence on germ radii, singular coalescence or weight complexity. That pointwise microscopic responsibility remains. The physical window theorem is proved independently of that derivative budget, at the stated finite Fourier resolution.

## D. A denominator under the actual stationary law

Theorem `thm:projected-collision-windows` treats standardized output half-widths `m^(-2/25)`. It augments the three-dimensional output by a fourth coordinate, integrates a four-dimensional Fourier estimate, and truncates the fourth coordinate at `T=m^(1/400)`. The fixed 128th moment pays the discarded tail. The three relevant powers are `3/280-1/400=23/2800`, `9/100-2/25=1/100`, and `128/400-6/25=2/25`. The Gaussian envelope calculation preserves decay in the fourth coordinate and does not pay an unnecessary truncation factor in the boundary terms. Discrete endpoint values are handled by the inherited envelope construction.

Lemma `lem:stationary-length-bias` supplies the exact stationary normalization. In the return-suspension coordinates `(y,s)`, the probability is `(c*/mean(tau_R)) dnu_R^*(y) ds` on `0 <= s < tau_R^*(y)`. The marginal of `y` is `tau_R^*/mean(tau_R^*)`, which is generally unbounded. The current outgoing collision, in contrast, has density `tau_R/mean(tau_R)` relative to `nu`, with uniformly bounded supremum and BV norms. The two are different length biases. The new proof gives their tower identity directly and never assumes that the first density belongs to the second's regularity class.

The resulting stationary physical probability is

`P_R(A_t^phys) = 8 t^(-6/25) g_{V_R}(xi) [1+O(t^(-23/2800) sqrt(log(2+t)))]`.

The event uses the unmodified displacement/collision-count intervals at the deterministic observation time. Its physical half-width is `t^(21/50)`, compared with `t^(23/50)` in the retained section-start result. This is a finer mesoscopic theorem under the actual equilibrium law, not a fixed-label raw denominator.

## E. Relative physical-event replacement on one probability space

Theorem `thm:stationary-physical-windows` compares four exact events on the same stationary suspension: the deterministic-collision reference, the deterministic-return reference from the actual preceding section origin, the actual last completed return, and the physical observation at time `t`. No independent new section point is sampled.

For collision-to-physical coupling, high collision moments control the inverse flight clock, with a deterministic window `t^(5/8)` and error threshold `t^(3/8)`. For return-to-physical coupling, the retained section-start estimate is transferred through the actual roof bias using Cauchy--Schwarz and a higher fixed moment order. The bias has a uniform exponential tail. Initial and final partial returns are retained and estimated. Independence of the clocks, ages and records is never used.

On the resulting good set the standardized vectors differ by at most `C t^(-1/8)`. The symmetric difference of the events is contained in a Gaussian-controlled shell between enlarged and contracted boxes plus an exceptional event. Relative to the proved denominator, the errors are `t^(-9/200)`, `t^(-23/2800) sqrt(log t)` and `t^(-2+6/25)`. This proves the displayed relative rate, not merely an absolute clock estimate.

The conditional initial measures are consequently close in total variation. The conclusion applies to every common bounded statistic of the whole trajectory, without requiring it to be a single-return BV insertion. It does not identify a conditioned Brownian limit. The additional bounded path-selection corollary states explicitly the lower bound still needed for its weighted denominator; arbitrary rare path weights are not silently admitted.

The original microscopic physical event, with its original fixed-label/time resolution, is not replaced by these windows. The full weighted raw denominator and its relative microscopic replacement remain separate targets. What is newly established is both a denominator and relative event comparison for a precise finer window class under the correct stationary initial law.

## F. Specialist checks and presentation comments

The new proof imports no new theorem beyond the already stated collision splitting, fixed-order moments, damping, exact suspension normalization and endpoint-safe envelopes. Its load-bearing points for independent review are the fixed 80-factor word, elimination of the collision stopping loss, four-dimensional projection/truncation, the distinct physical length biases, exceptional-set transfer, and division by the actual stationary denominator. Finite checks do not certify those continuum arguments.

All twenty presentation comments were tracked. The sharp region and smooth cutoff remain distinct; both frequency scales, fixed expansion orders and the connected residual term stay visible. The third-coordinate count separation, signed density identity before norms, weight-class intersection and collision/induced Cesaro distinction are retained. A new main-text roadmap connects the Gaussian/moment package, extraction, Theorems N--Q, signed window Theorem R, section-start Theorem S and stationary Theorem T. No graphical illustration is needed to state or prove the distinction between the new collision ball and the retained return cross. Publication metadata does not claim journal acceptance or independent proof certification.

## G. Source preservation and qualification

Every one of the 58 inherited core files, all 55 inherited Python files, and the bibliography is byte-identical to the frozen v27 tree. All 763 inherited labels remain. Only five exact replacements in the main article add revision identity, the stationary abstract sentences, Theorem T, the two inputs and the roadmap. No inherited theorem or proof is deleted. The local baseline check verifies the v27 tree against the reviewed v26 source; the new verifier checks the v27 baseline tree itself and the exact new source.

The final read-only workflow checks and compiles ordinary committed source at one exact SHA, runs normal and optimized checks, rejects unresolved references and overfull boxes, and emits a dynamic receipt with run ID, source hashes and PDF hash. A source snapshot or staging execution is not used as evidence of a final build. The new proof is submitted for substantive re-review of the same raw mixed-density program.
