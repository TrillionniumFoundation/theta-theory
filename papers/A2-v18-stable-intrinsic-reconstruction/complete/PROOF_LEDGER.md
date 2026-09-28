# A2 v14 proof ledger

The full v13 native tree is frozen at `history/v13-reviewed`, Git tree
`ee946ef91770778839f15c8c35416d401e99ea1c`. All its active results and proofs remain
in the current main manuscript. This ledger lists the additional arguments.

| Source label | Statement and proof | Main dependencies | Verification distinction |
|---|---|---|---|
| `lem:v14-mixed-normal-form` | Fixed-box mixed-boundary solution and normalized derivative estimate | Supplied analytic normal form; uniform contraction; analytic logarithm; Cauchy estimates | Exact differentiation checks are finite diagnostics, not a proof of the analytic estimates |
| `prop:v14-physical-normal-form` | Exact physical flux, common-box factorization and action limit | Canonical transverse charts; preceding lemma; inversion and two-form identity | Nonconstant shear example checks the projection calculation |
| `cor:v14-amplitude-identification` | Stable/unstable projection interpretation of the normalized half-line amplitudes | Same analytic physical problem in both forward constructions; normalization and uniqueness of limits | No normal-form existence theorem for arbitrary smooth families is inferred |
| `thm:v14-rank` | Equivalence of regular tangent rank, finite evaluations and local bi-Lipschitz observation | Finite-dimensional duality; inverse-function argument; analytic identity theorem where invoked | Not a claim that every finite-dimensional family has full rank |
| `cor:v14-observable-quotient` | Constant-rank local observation quotient represented by finitely many means | Submersion chart; identical tangent kernels | Exact local factorization, not noisy statistical sufficiency |
| `prop:v14-free-area` | Independent physical area and contact coordinates | Retained support family and triangular jet Jacobian; strictly signed exact area derivative | Actual analytic billiard family, not abstract profile perturbations |
| `thm:v14-area-windows` | Unknown area and finite contact jets from `2M-1` positive two-flight windows, with regular confidence/risk bounds | Retained finite-flight inverse; shared-intercept Vandermonde; controlled remainder; physical alternatives | Fixed family/order/windows; no full-profile or growing-order minimax theorem |

There is also a worked canonical-shear remark. Its charts have determinant one;
the resulting relative amplitude is nonconstant even for constant `Delta`. This
illustrates the projection dependence and is not a general billiard realization
claim. The normal-form benchmark is credited to the prior referee memorandum.
The rank argument is an elementary general principle; the physical unknown-area
construction and window design provide the direct response to the data objection.
