# Proof and dependency ledger — A2 v43

**Current source:** `papers/A2-v43-journal-package`.
**Reviewed baseline:** v42 at `fffc85d4da8c8ee6369833369d564b1cffabc63d`.
**Controlling review:** `74787c9c353b72983fe1bb43af467e31d3eb0f2a`.

## Exact chain: primary only

| Stage | Stable labels | Required input and output |
|---|---|---|
| Occupation | `lem:two-field-prefix` | Pointwise endpoint identity, bounded diameter and gap; finite translated-field inverse. |
| Arbitrary-law supports | `lem:positive-convolution-support`, `prop:singular-support-components`, `cor:singular-support-ae-periods` | Nonnegative compact measures, convex support and separation; matched supports and a.e. representatives. |
| Nonsmooth calibration | `lem:nonsmooth-arc-support`, `lem:nonsmooth-surface-atoms`, `lem:nonsmooth-jordan-chord` | Strict convexity without smoothness; exposed-face atoms and exact chord recovery. |
| Joint identification | `thm:two-field-rigidity`, `cor:two-field-fiber` | Calibrated geometry and known-factor convolution; full canonical law, translation fiber, responses and period group. |

These stages have no `H-` reference to a supplement result. Their three source
files `21_two_field_rigidity.tex`, `24_measure_support.tex`, and
`25_nonsmooth_curvature.tex` are unchanged from v42. Strict convexity and convex
support remain exact hypotheses; finite smoothness priors are not inserted.

## Finite chain and default implementation

| Stage | Stable labels | Dependency |
|---|---|---|
| Geometry | `thm:two-field-finite-geometry`, `cor:two-field-finite-cloud` | Own two-command acquisition, primary Appendix A and the frozen finite supplement interface. |
| Common factor | `lem:moment-rational-factor`, `lem:moment-explicit-conditioning`, `lem:moment-positive-programme`, `cor:moment-positive-compression` | Accurate rational geometry and occupation moments; positive sparse law with controlled `W_1` error. |
| Default moments | `lem:protected-linear-prefix`, `thm:linear-moment-sampling` | Complete protected expanded component; signed two-bit records, arbitrary-law quadrature and simultaneous concentration. |
| Default joint bound | `eq:two-field-joint-default-cost`, `cor:linear-joint-budget` | Geometry, default moments and common positive factor; `N_geom(c a_m,delta/2)+C a_m^(-2) log(Cm/delta)`. |
| Retained alternative | `lem:two-field-finite-moments`, `eq:two-field-joint-decomposed-cost`, `prop:moment-complete-budget` | Deterministic all-node design and the same factor mechanism; larger moment term. |
| Prediction | `cor:two-field-finite-prediction`, `cor:two-field-finite-density` | Geometry and `W_1`; local spatial `L^1`, with a separate `BV` prior for the stronger norms. |

The finite-law theorem prints both implementations. Its retained proof first
establishes the deterministic alternative and common factor construction.
The signed-record theorem then supplies the alternative moment input, and
Corollary `cor:linear-joint-budget` proves the default budget. No inference
uses the improved bound as a premise for itself. `JOURNAL_INTERFACE.json`
records this dependency as an acyclic graph.

## Frozen supplement interface

`core/29_supplement_interface.tex`, including `tab:finite-interface`, remains
unchanged. It prints the conditions and outputs for cap mass, complete coarse
components, normals, bisection/radial interpolation, signed smoothing and
period locking. All `H-` and `M-` references retain their label names and
owners. `main.tex` and `companion.tex` share only label-free preamble and
bibliography; all mathematical inputs have one document owner.

## Preservation and checkable scope

The v42 active union contains 47 TeX inputs, 467 labels, 116 formal theorem,
lemma, proposition or corollary blocks, and 113 proof bodies. This revision
retains every label and every proof body verbatim. The new default-budget
equation and the data-model table add labels, not mathematical results.
The native receipt recomputes these counts and checks both entry points.
Earlier v41 and v40 preservation is also checked in publication mode.
Historical files have not been discarded to obtain the counts.

The current assertions are classical written proofs, not proof-assistant
certificates. Ordinary/optimized numerical diagnostics and source-contract
mutation tests address their explicitly bounded finite and editorial scopes.
The separate specialist-review condition remains open.
