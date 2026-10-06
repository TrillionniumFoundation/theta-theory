# Response to the latest referee: A2-DYN revision 18

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v18-referee-response`  
**Controlling report:** `reviews/a2-dyn-v16-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Report commit / blob:** `b0b7ddfcd90f493e02254742b33174e9108fc5a7` / `805f04cd60d144bc6321ce3f4304ebe1cda34999`  
**Immediate author baseline:** `253f7c56de1f198ff9bd5e13fa2009baf4551495` (revision 17)  
**Date:** 6 October 2026

We thank the referee for identifying the distinction between first variation of finite collision records and second derivatives of their raw pushforward densities. The already landed v17 revision addresses the return spectral parameter and provides a finite-rank operator reconstruction. We continue from that source. The principal new work addresses the different raw branch-extraction requirement in Sections 10 and 13.C of the report.

Theorem I and two complete new sections prove a full finite-physical-count extraction, including every singular itinerary boundary, and place it in an exact inversion identity for the original central raw density. The title, physical family, actual section, four-coordinate record and raw mixed-density endpoint are unchanged. All previous mathematical modules and theorem labels remain. No separate referee report on v17 was located in the branch set inspected for this revision; the present response does not invent one.

## A. Actual operators, peripheral phases and reconstruction

The exact arbitrary return-phase lift, local joint defect theorem, C/h grid reconstruction, orthogonal residual comparison and finite-rank peripheral resolvent from v17 are retained. The distinction between an exact lift for every return phase and a quantitative estimate only in its specified joint neighborhood remains explicit. These are neither an anisotropic realization of the full induced twist nor a proof of a full-circle mesh-uniform power estimate.

The new raw extraction does not attempt to obtain those operator conclusions from a density preparation theorem. Instead it constructs the edge-subtracted Fourier remainder that any successful complementary-frequency argument must actually estimate.

## B. Complementary frequencies and a corrected finite-count inversion

For each count restriction the constructed remainder now has an integrable mixed Fourier transform, not just a conditional integrability premise. Its far-roof integral is bounded by `2(2 pi)^3 A2/B`, where A2 is the actual sum of the L1 second derivatives of the residual time densities. This is a finite-count analytical estimate; its n- and radius-dependence is displayed rather than suppressed.

The collision count is an observed lattice coordinate. Consequently the restricted and unrestricted raw densities agree exactly at every label with count at most L. A linear cutoff `L_n=ceil(lambda n)`, `lambda>c*^(-1)+1`, covers any fixed central window for large n.

The new exact identity is

`p = K_n*mu + (e^L-K_n*E^L) + inverse[(1-chi_n) Qhat^L] - K_n*T^L`

on that window, where `T^L=mu-mu^L`. The high-count convolution must not be omitted: convolution spreads the omitted labels. Its normalized central size is nevertheless `O(n^(-P))` for every P, because those labels are separated by a distance proportional to n and the proof kernel is Schwartz. A separate bound from the true cumulative-return tail is `C n^(1/50) exp(an-cL)`, valid on the entire mixed space. Both arguments and the factor `n^(1/50)` are proved explicitly.

The physical cutoff remains `2 n^(-99/200)`, with rescaled radius `2 n^(1/200)`. The new raw error inequality combines the already proved central Gaussian rate, its Gaussian tail, the count correction, the exact local edge correction, the finite complementary residual integral and `n^2 A2/(pi B)`. The last three quantities are the remaining uniform long-time estimates. Thus the new far-roof bound is not mislabeled as a complete complementary-frequency theorem; the annulus, compact nonzero torus band and growing frequencies below B remain visible.

## C. Complete critical and singular raw extraction

### C.1. Integrate the full finite graph

The argument uses the whole finite collision graph from the inherited finite-record lemma, with the actual first-admissible-hit conditions and the exact section-membership tests at every collision. All words below the count cutoff are included. The integration domain therefore contains the effects of regular critical points, grazing, competing roots, return-membership boundaries and generated image boundaries.

The existence of a density is proved by the physical word coarea argument with the actual `1/(4 pi c*)` section normalization. The regular critical-word theorem and isolated Morse jumps were already in the historical manuscript; we retain them and do not claim their classification as new.

For each lattice label the cumulative flight-time distribution is a parameterized integral of a bounded globally subanalytic function over this complete domain. Cluckers--Miller's stability-under-integration theorem makes it constructible. One-variable differentiation, justified on an analytic partition, gives a constructible representative of the raw time density. No inverse Jacobian is extended through a singular boundary.

### C.2. Extract every second-derivative singularity

One-variable constructible preparation yields convergent Puiseux-log germs. At a one-sided singular value they are sums of `x^(j/q) (log x)^k` with analytic coefficient series. After collecting equal exponents, L1 integrability excludes all nonzero terms with exponent at most minus one.

The extraction removes every remaining term with exponent at most one, using C2 piecewise-polynomial cutoffs. The remainder is bounded, with its first two derivatives, by `C x^(beta-a)(1+|log x|^K)` for some beta greater than one and a=0,1,2. Both value and first-derivative traces vanish. Distributional integration by parts therefore leaves no point mass or derivative of a point mass, and the exact remainder belongs to W^{2,1}.

Constants and slopes are intentionally extracted. A one-sided constant or slope can have zero classical second derivative inside its interval while retaining a nonzero boundary distribution. Fractional powers and logarithmic terms are treated by the same rule. The proof estimates the derivative of the cancellation remainder, not the difference of two separately integrable derivatives when those derivatives diverge.

### C.3. Actual finite derivative sum, and its remaining growth estimate

Only finitely many lattice components occur below the cutoff, so the sum of residual L1 second-derivative norms is finite. The article gives an explicit budget from the actual germ coefficients, cutoff widths, remainder exponents and regular-interval derivative integrals. These data include all finite branches rather than only the previously selected periodic or critical words.

This closes the structural extraction and residual-integrability problem for every fixed n,L,R. It does not yet provide a bound for that budget uniform in R as n and L increase. The preparation theorem supplies no such dynamical growth rate, and compactness cannot be used to bypass collisions of singular values or vanishing cutoff widths. The required long-time estimate and the local edge estimates appear as the explicit remaining terms of the new raw error formula.

## D. Weighted exact conditioning

The structural theorem permits bounded finite-record subanalytic weights, including finite initial, intermediate and terminal observation conditions up to the nth actual return. This is more general in time placement than a single mark, but narrower in spatial regularity than arbitrary BV. Neither inclusion is silently assumed.

The finite extraction and count-localized identity use exactly the original weight and its unchanged denominator. A multiple-time subanalytic indicator does not automatically receive the inherited single-mark central Gaussian estimate. Weighted complementary bounds, local edge estimates and the relative comparison needed for the exact physical observation remain separate tasks. No rare event is replaced in the proof.

## E. Independent review and the added input

The new external input is precisely the Cluckers--Miller constructible integration/preparation theorem, identified in `RAW_EXTRACTION_INPUT_MAP.md` with the exact hypotheses and theorem numbers. The passage to a one-variable derivative, convergent jet subtraction, boundary-trace cancellation, Fourier bounds and count-localized identity are proved in the paper.

The next review should check the full finite graph and its chart normalization, applicability of constructible integration to the stated weights, the convergent Puiseux-log form, the exponent-one endpoint rule and the exact high-count convolution correction. Independent human specialist review and formal proof certification are not claimed.

## F. Topic, presentation and source preservation

The article continues the same raw mixed-density problem rather than substituting a different topic or venue-specific endpoint. Theorems A--H remain, and Theorem I is an additional theorem directed at the raw branch requirement. All fourteen technical comments in the controlling report remain covered by the retained v17 distinctions and the new scope statements: physical/spectral/kernel frequencies, both annulus scales, the exact tower conventions, initial-coordinate versus raw-density derivatives, the actual unchanged event, and the difference between finite reconstruction and full operator powers.

All 39 inherited core files and all 28 inherited Python files are byte-identical. All 459 previous mathematical labels and all 14 old bibliography entries remain. Six exact changes in main.tex and references.tex update the revision identity, consolidate the abstract, and add the theorem synopsis, proof route, new inputs and one primary source. The abstract consolidation changes no theorem or proof; all detailed conclusions remain in the article. `INHERITED_EDITS.json` replays these changes, and the manifest hashes the actual files. The completed article is stored as ordinary source, not generated by its qualification workflow.

The read-only exact-SHA workflow executes normal and optimized finite checks and native typesetting, and emits a dynamic run-bound receipt. The finite model checks are regression tests for the jet and inversion formulas, not a proof of continuum billiard estimates. The new source is offered for substantive re-review of the same raw-density objective.
