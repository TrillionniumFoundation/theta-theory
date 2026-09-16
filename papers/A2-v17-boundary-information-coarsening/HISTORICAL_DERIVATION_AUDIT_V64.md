# Historical derivation audit — revision 64

Baseline: actual v63 mathematical source `f5517519440b897707ddc60deeafba19e86bb5a5`, subtree `b042811c7ceb2c5fd841b2a03ab0b8c232c39dce`. Latest report: review commit `493196e4f6f1d9a46c062df0e3669c3ca26c4fcc`.

This is a targeted dependency audit for a new periodic-itinerary extension, not a claim of a new line-by-line audit of all 433 inherited PDF pages. The downloaded native artifact was source-checked against all 784 frozen files before revision. The full historical corpus remains in the revision.

## Sources directly used

| Retained source | Role in this revision |
|---|---|
| `v3/10_geometry_action.tex` | Physical stationary finite chains, Jacobi/cofactor normalization, fixed collar. |
| `v3/20_integration.tex` | Full-phase flux and residual-time integration; conditional law alone does not determine acceptance mass. |
| `v4/10_boundary_layers.tex` | Complete weighted half-lines and two-ended trace-class comparison; the direct geometric starting point for the new proof. |
| `article/16_hyperbolic_coordinates.tex` and `article/16b_determinant_transport.tex` | Existing analytic-chart comparison and actual-smooth identification of the amplitude with a scalar stable linearizing density. This identification was already proved for alternating channels and is not falsely presented as a new v64 discovery. |
| `article/23a_signed_endpoint_rigidity_v27.tex` | Actual-smooth jet factorization and stationary-envelope cancellation; the new forward theorem does not replace this inverse. |
| `article/23f_single_offset_law_inverse_v42.tex` | Existing amplitude-free law inverse and fixed-order finite-flight estimate; neither is reintroduced as a new result. |
| `article/23a2_analytic_contact_inverse_v59.tex`, `article/23a3_conditional_observation_inverse_v60.tex` | Retained complete local analytic inverse and smaller-disc conditional observation interface; no general-periodic inverse is inferred from them. |
| `article/23f2_finite_experiment_analytic_inverse_v62.tex`, `article/25a_common_observables_v25.tex` | Retained realizable-law fitting, complete target, physical position pilot, all-history corrected timing and confidence budgets. |
| Both active introductions, principal structural statements, v63 response/index/literature record | Current main claims, attribution, editorial issue and precise source routing. |

## What is new and what is inherited

The old proof uses a two-periodic normal reference with an explicit hyperbolic Green formula. The new proof derives a periodic Jacobi form directly from the actual nongrazing chord geometry, using the normal cosines to scale arclength. A strictly positive diagonal surplus supplies a walk expansion for finite and half-line Green operators, including reflected terms. It therefore does not assume a supplied analytic canonical normal form, and it allows unequal flight lengths and oblique incidence.

The determinant normalization and summable two-end comparison are the same analytical mechanism, extended to this geometric domain. Their full proof is printed in the new module rather than asserted by analogy. The nonlinear connected-action and stable-return formulas are transparent consequences of that relative estimate. The accepted literature comparison and existing scalar-linearization attribution are preserved.

A new issue appears outside normal incidence: the edge action has nonzero first endpoint derivatives. A telescoping linear gauge is harmless for stationarity and twist, but changes residual physical time unless restored. The new physical law explicitly restores it. A three-periodic orbit among three disks and nearby nonsymmetric realizations verify that this distinction occurs in actual tables.

The retained geometric inverse, analytic-germ estimates, global reconstruction, finite-fiber examples and statistical catalogue are not weakened or re-proved under a different experiment. No conclusion is silently transferred from a two-contact channel to an arbitrary itinerary.

## Retention audit

The five inherited modified paths are `main.tex`, `rigidity.tex`, `article/00_structural_introduction_v48.tex`, `journal/00_principal_introduction_v61.tex`, and the manuscript `README.md`. Their exact original bytes are archived. All other 779 inherited files are unchanged. All 127 original active inputs remain, with two v64 active additions. All prior review materials and native deliveries are inherited from the review-branch parent; no default-branch, A1 or review-branch content is rewritten.

The theorem proofs, rather than preservation totals or finite tests, must carry the new mathematical assertions. The next referee should examine in particular the geometric Hessian scaling, exact transfer/cofactor match, finite-to-half-line trace comparison, restored oblique clock terms, and the physical realization.
