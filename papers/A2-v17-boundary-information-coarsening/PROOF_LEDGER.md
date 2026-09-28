# Proof ledger — A2 v17

The following additions are integrated into `main.tex`. All previous statements and proof modules remain active.

| Statement | Source | Essential proof step | Printed scope |
|---|---|---|---|
| Logarithmic boundary information, `thm:v17-boundary-information` | `article/18_boundary_information.tex` | Coarea coefficient, controlled truncated score, likelihood expansion, bounded overlap integral | Normalized `C^3` linearly vanishing densities with a compact regular support boundary; nonzero boundary coefficient for the critical profile |
| Coarea moment bounds, `lem:v17-coarea` | Same | Collar flow and level-set integral | Uniform strict regularity/positivity bounds; support-exclusive mass of order `t^2` |
| Intrinsic coefficient, `rem:v17-invariance` | Same | Exact invariance under positive changes of defining function | No logarithmic criticality claimed when the coefficient vanishes |
| Exact cap information, `lem:v17-cap-information` | `article/19_endpoint_critical.tex` | Determinant-one whitening, residual integration, exact angular moment | Either flight parity, unequal contact curvatures, same fixed-table finite/boundary pair |
| Sharp endpoint tangent experiment, `thm:v17-endpoint-tangent` | Same | Information coefficient one and `zeta_j ~ 2 q_j` | Conditional and raw independent preparations; subcritical, critical and supercritical regimes |
| Physical endpoint transition, `thm:v17-endpoint-physical` | Same | Retained tangent TV estimate, product telescoping and critical subsampling | Positive offsets with `omega(d_j)=o(q_j^2 log(1/q_j))`; explicit nonempty smooth/even regimes |
| Strict observation hierarchy, `cor:v17-coarsening-hierarchy` | Same | New endpoint profile, old full-record exact support profile, exact success-mass cancellation | Same physical pair and preparation count; no unknown-table equivalence claimed |
| Random-hazard mixture, `cor:v17-random-hazard` | `article/32_random_hazard.tex` | Tight hazard sum, logarithmic remainder, bounded products | Capped policies and vanishing physical error budget; limit under the common-history law |

## Dependence on retained derivations

The new general information theorem is proved directly. The physical application uses the exact alternating Jacobi whitening and common success mass from `v7/10_critical_experiments.tex`, the uniform tangent approximation in `lem:v7-tangent`, and the full-record supercritical subsampling argument in `article/30_supercritical.tex`. These in turn use the relative geometric construction and physical residual-time measure in `v3/10_geometry_action.tex`, `v3/20_integration.tex`, `v4/10_boundary_layers.tex`, and `v6/10_experiment_transfer.tex`. The old full-record erasure limit is not renamed as a new result.

The new theorem does not replace any hypothesis in the geometric inverse, Abel inverse, pilot, or finite-dimensional/minimax appendices. Finite checks of determinant cancellation and cap integrals are diagnostics, not proofs of the retained billiard estimates or of asymptotic limit theorems.
