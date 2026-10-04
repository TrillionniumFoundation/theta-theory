# Proof ledger — A2 v41

The preservation baseline is the complete active union of the reviewed v40 article and supplement at `c5593b05546889f436ce858c327670d080aae204`. The new revision addresses review `24baf07cf2952668d61881c727cc6417e952c76e`.

## Counts and preservation

| Object | v40 baseline | v41 active union |
| --- | ---: | ---: |
| TeX inputs, deduplicated | 40 | 46 |
| Mathematical labels | 402 | 456 |
| Formal result blocks | 95 | 113 |
| Complete proof bodies | 92 | 110 |

All baseline labels remain, and all 92 baseline proof bodies are byte-identical. The two documents share only their label-free preamble and bibliography. Both are compiled; the supplement is an active source dependency. The validator derives the baseline from both reviewed entrypoints, rather than from an older single-file snapshot.

## Exact proof additions

| Result label | File | Proof supplied |
| --- | --- | --- |
| `lem:positive-convolution-support` | `core/24_measure_support.tex` | Positive compact-measure support addition; Tonelli passage through planar null sets. |
| `prop:singular-support-components` | same | Exact physical/open-strip comparison, arbitrary-law supports, local finiteness, connected components and matching. |
| `cor:singular-support-ae-periods` | same | Finite translation operations on a.e. classes and equality of a.e., pointwise and geometric period groups. |
| `lem:nonsmooth-arc-support` | `core/25_nonsmooth_curvature.tex` | Closed-hemisphere support maxima through convex interval sections. |
| `lem:nonsmooth-surface-atoms` | same | Distributional positivity; exposed-face formulas for one-sided derivatives; atom mass equals face length. |
| `lem:nonsmooth-jordan-chord` | same | Exact negative chord masses, mutually singular Jordan parts and canonical support recovery. |

The six additions are inserted before the corresponding support and calibration results in the exact section, outside every baseline proof body. The exact hypotheses and complete translation fiber are unchanged.

## Finite geometric additions

| Result label | File | Proof supplied |
| --- | --- | --- |
| `lem:two-field-collar-details` | `core/26_finite_geometry_details.tex` | Fixed collar, candidate conjunction, free shifted starts with a numerical margin, and conditional error probability. |
| `lem:two-field-strip-details` | same | Injective parameter rectangle at grazing points and area at least `c r^3`. |
| `lem:two-field-grid-details` | same | Interior footprint cap, positive-record cap mass and uniform grid approximation conditional on each hidden displacement. |
| `lem:two-field-assignment-details` | same | Numeric distance enclosures, component identification, complete aperture cutoff and shared hull concentration. |
| `lem:two-field-plateau-details` | same | Explicit signed moment matrix, plateau existence and curvature-atom mass error. |

This is primary Appendix A. The sufficient exponent remains `Q_pair = (gamma + 9/2)s/(s - 2)` for `s = 6 + beta`. No density modulus, extra direction or shorter flight is introduced.

## Finite probability additions

| Result label | File | Proof supplied |
| --- | --- | --- |
| `lem:moment-protected-cutoff` | `core/27_moment_factor_details.tex` | Rational cutoff equal to one on the entire selected component and zero on every other component. |
| `lem:moment-rational-factor` | same | Rational outer polygon, true uniform-factor variation error, exact rational moments and correct area normalization. |
| `lem:moment-shared-quadrature` | same | Shared occupation estimates and boundary-cell quadrature for arbitrary compact probabilities. |
| `lem:moment-explicit-conditioning` | same | Factorial amplification and an explicit `Lambda_m`. |
| `lem:moment-positive-programme` | same | Padded rational grid, feasible comparison probability, rational optimizer and propagated transport error. |
| `cor:moment-positive-compression` | same | At most `binom(4m+2,2)` positive atoms with the same fitted moments and error guarantee. |
| `prop:moment-complete-budget` | same | Complete allocation of geometric, sampling and fitting errors, confidence, coordinates and finite output. |

This is primary Appendix B. The law stage still works for arbitrary compact probabilities conditional on the stated geometric estimates; the joint uniform bound uses the declared finite geometric class. Its rate remains a sufficient exponential bound. Local spatial prediction and the stronger BV-density conclusions retain their distinct norms and assumptions.

## Classical and historical ingredients

The full supplement interface is stated in `core/29_supplement_interface.tex`, including every relevant input and output. Its references point to the preserved coarse, radial, cap, smoothing and period proofs. `core/28_theorem_comparison.tex` and `LITERATURE_AUDIT.md` distinguish the collision-specific identities from classical support measures, geometric factorization, deconvolution and transport tools.

The finite-prefix identity originates in the earlier A2 derivations. The v40 two-support cancellation and finite inverse remain attributed to their original place in that chain. The new proofs clarify and strengthen that chain without substituting another observation model or deleting its preceding results.

## Verification boundary

The exact-source receipt records source hashes, both input closures, baseline preservation, diagnostics and final TeX evidence. It does not convert finite diagnostics into a continuum proof certificate. The five specialist-review entry points are recorded in `SPECIALIST_REVIEW_BRIEF.md`.
