# Specialist proof review brief — A2 v41

This brief makes the five proof-review requests in §11.7 of the v40 referee report concrete for the next reviewer. It is a review brief, not a completed assessment. No human specialist review is claimed by its presence.

## Review object and mathematical scope

Review the matched `A2-v41-primary.pdf` and `A2-v41-companion.pdf`, their journal-source archive and the exact author SHA in the qualification receipt. Record the full SHA in any report so that later source changes cannot be confused with the reviewed object.

The exact datum is two whole-plane spatial mean fields for the fixed vectors `te,-te`, under the same unknown stationary probability. Obstacles are nonempty, locally finite, compact, strictly convex planar bodies with nonempty interiors, bounded diameter and gap `d`. The compact convex launch support `A` obeys `t+diam(A)<d`. The exact law can be singular, including an atomic law whose topological support is a convex set. The precise closed-solid/free-contact bit convention is part of the data model.

The finite theorem uses the separately stated smoothness, curvature, boundary-mass and strict separation priors, plus the whole-patch nonperiod margin or a protected complete finite aperture. Its two command vectors stay fixed. Exact uniqueness and the finite stability estimates are separate conclusions.

## 1. Singular-law support decomposition

Read `lem:positive-convolution-support`, `prop:singular-support-components` and `cor:singular-support-ae-periods` in `core/24_measure_support.tex`, together with `lem:two-field-prefix`.

Please verify the support equality for positive measures, the Tonelli passage for planar null sets, the exact `0<s<=t` physical strip convention, endpoint continuity for nonsmooth strictly convex bodies, local finiteness after a compact expansion, connectedness with a lower-dimensional support, and the stated separation/incidence bounds. Check that a.e. equivalence is used only where appropriate and that boundary atoms remain in the physical means. Confirm the finite-prefix operation on a.e. classes and the equality of the three period groups.

## 2. Arc cancellation and negative atoms

Read `lem:nonsmooth-arc-support`, `lem:nonsmooth-surface-atoms` and `lem:nonsmooth-jordan-chord` in `core/25_nonsmooth_curvature.tex`, then the existing calibration and exact rigidity theorems.

Please check both closed hemispheres of the arc identity, including transverse directions and corners; the positivity of `h''+h` as a measure; the one-sided derivative formulas and exposed-face atom mass; the distinction between atoms, corners and singular continuous curvature; the coefficient and orientation of the two chord atoms; and mutual singularity in the Jordan decomposition. Confirm the Steiner placement of all components and the precise common-translation fiber. The final Fourier division is an exact finite-measure uniqueness argument only.

## 3. Tangential two-direction acquisition

Read `lem:two-field-rare` and Appendix A's `lem:two-field-collar-details`.

Please check the outer tangent disk, the prior-fixed collar, the rational normal tolerance, inclusion of every true maximizing candidate, the `11t^2/16` free-start reserve and exclusion of other obstacles. Verify the exterior zero candidate and the interior lower bound for every candidate, which together justify the conjunction rule. The zero assertion is made at the actual nominal target; rounding affects the intended radial bisection ambiguity. Check conditional confidence under adaptive fresh preparations.

## 4. Cap probability, grids and complete components

Read `lem:two-field-hulls` and Appendix A's strip, grid and assignment lemmas, followed by its signed plateau lemma.

Please check the injective grazing parameter rectangle and `c r^3` strip area; the footprint rectangle's area and depth; the product cap probability; the order of conditioning before grid quadrature; and every boundary cell, including those with a center exactly on a boundary. Check the distance enclosure and `g-2t` reserve, the completeness cutoff and fragment exclusion, and the reuse of nominal records over support directions. For the chord mass, inspect the signed moment matrix and its determinant, the plateau's treatment of the atom-location error, and the smoothing exponent balance.

## 5. Estimated factor and positive probability output

Read the finite law theorem and Appendix B, `core/27_moment_factor_details.tex`.

Please check the complete pointwise cutoff, the common coordinate box, the rational outer polygon construction, normalization by physical area, exact triangle moments and uniform-factor variation error. Verify spatial quadrature for arbitrary compact laws, the triangular factorial bound and tensor approximation. Check that the padded grid contains a quantized comparison law, that irrational comparison weights legitimately bound the rational programme, and that the optimizer has a genuine positive convolution factor. Inspect the full propagated error, rational weight compression preserving all moments, confidence allocation and observation/coordinate budget. The representation length and arithmetic for the final weights are separate resources.

## Requested report format

For each area, state whether the proof is correct as written, correct after a specified local correction, or requires a specified missing argument. Identify every objection by theorem label and the exact mathematical inference at issue. Give any counterexample with all hypotheses and boundary conventions checked. Distinguish a mathematical gap from a requested expository expansion, a resource-model question, and a literature comparison.

Please also assess whether the primary's visible supplement interface contains every hypothesis needed from that volume and whether the theorem-level comparisons describe the relevant prior results accurately. The finite diagnostic output may be used to reproduce explicit examples; it should not be substituted for this proof review.
