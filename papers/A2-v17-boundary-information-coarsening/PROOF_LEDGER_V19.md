# Proof ledger — A2 v19

This ledger records the active referee-facing theorem chain. It supplements, rather than replaces, the older ledgers preserved in this directory.

| Result | Active source | New in v19 | Principal dependencies | Status / scope |
|---|---|---|---|---|
| Relative boundary law on a fixed collar | `article/01c_geometric_setup_v18.tex`, Part I historical modules | No; retained and notation clarified | alternating Jacobi reduction, nonlinear bridge, trace-class separated end perturbations, common Morse domain | General smooth labelled channel; centered geometric derivatives now explicit |
| Intrinsic scalar determinant transport | retained v14/v15 modules | No | physical first-hit maps, half-line Fredholm determinant | Retained |
| Smooth boundary-energy profile inverse | `article/20_boundary_compatibility.tex` | No | signed Morse change followed by endpoint-sign integration, Volterra convolution | General smooth contacts; intentionally symmetrized invariant |
| Earlier independent-contact jet inverse | `article/23_two_contact_rigidity.tex` | No | half-line envelope identity | Individually even contacts and supplied leading geometry; retained as a coarsened special inverse |
| **Signed-endpoint action and contact rigidity** | `article/23a_signed_endpoint_rigidity_v19.tex` | **Yes** | relative support formula; v3 linear half-line orbit; v12 triangular envelope calculation | General smooth labelled contacts; no evenness; gap from onset, curvatures recovered; all finite jets recursively recovered; analytic germs rigid |
| Direct two-flight finite inverse | `article/29_two_flight_benchmark.tex` | No | finite Schur complement and physical flux | Retained; even-contact finite-window benchmark |
| Scalar logarithmic boundary information | `article/18_boundary_information_v18.tex` | No; retained | coarea collar, truncated score, Hellinger affinity | General one-parameter linearly vanishing moving support |
| Fixed-table endpoint critical experiment | `article/19_endpoint_critical.tex` | No; retained | exact determinant-one whitening, scalar boundary theorem, physical transfer | Sharp finite-vs-boundary comparison for one table |
| **Vector boundary LAN / intrinsic information matrix** | `article/18a_vector_boundary_information_v19.tex` | **Yes** | polarization of scalar coarea moments; multivariate triangular-array CLT; Gaussian-shift limit | Finite-dimensional moving-support families; retained failure atom |
| **Efficient local estimator and sharp quadratic local minimax value** | `article/18a_vector_boundary_information_v19.tex` | **Yes** | LAN likelihood convergence, third lemma, Gaussian-shift minimax theorem | Positive-definite boundary information matrix |
| **Unknown-billiard geometric endpoint experiment** | `article/18a_vector_boundary_information_v19.tex` | **Yes** | endpoint support `d-S_0-S_p`; signed rigidity; finite subcover of tangent sphere; relative-law transfer | Any fixed finite labelled contact-jet family; finite positive endpoint design; actual long finite bridges under accumulated-error condition |
| Abel/profile stability and regularized observation | `article/21_abel_stability.tex`, `22_deautoconvolution.tex`, `28_regularized_observation.tex` | No | Volterra/Abel chain | Retained function-valued inverse results |

## The new rigidity block

For arbitrary degree `n>=3`, after lower graph jets are fixed,

`D_{q_n} s_n = [[coth(n gamma), frak_r_0^n csch(n gamma)], [frak_r_1^n csch(n gamma), coth(n gamma)]]`.

Since `frak_r_0 frak_r_1=1`, the determinant is exactly one. The proof uses the same highest-new-homogeneous-degree envelope mechanism as the reviewed even-jet proof, but the signed endpoint support supplies the unsymmetrized actions and therefore retains odd jets.

## The new statistical matrix

For `f_theta=a_theta(w_theta)_+`, `V=D_theta w_theta|_0`,

`J_Sigma = integral_Sigma a_0 V V^T / |grad w_0| d sigma`.

At `n p_n delta_n^2 log(1/delta_n) -> 1`, the experiment is LAN with this matrix. In a billiard family, `w=d-S_0-S_p`; the signed rigidity theorem shows that the collection of support velocities has trivial common kernel on every fixed finite contact-jet parameter space. Hence a finite positive-offset design has positive-definite summed information.

## Preservation

No earlier mathematical theorem is deleted from the active compilation. The v19 appendix compendium changes source navigation only. Statements with narrower hypotheses remain in place as special cases and as independent consistency checks.
