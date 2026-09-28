# Historical derivation audit — A2 v19

## Review base and preservation rule

This revision starts from the latest independent review branch `review/a2-v18-independent-harsh-top4-2026-09-11`, whose reviewed report is `reviews/a2-v18-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`. The revision branch is `revision/a2-v19-signed-endpoint-rigidity-2026-09-11`. Earlier A2 directories, historical reports, verification tools and proof modules are retained; v19 changes the active theorem hierarchy and adds proofs rather than deleting earlier results to evade review comments.

The active manuscript directory keeps its historical filesystem name `papers/A2-v17-boundary-information-coarsening/` so that the large retained source graph does not have to be duplicated. `ACTIVE_SOURCE_MANIFEST_V19.md` is the authoritative v19 source map.

## Material re-audited for C18-E1: general contact rigidity

The new signed-endpoint theorem is based on four already proved ingredients.

1. `v3/10_geometry_action.tex` fixes a common transverse coordinate and writes the facing graphs as `(-psi_0(u),u)` and `(g+psi_1(v),v)`. The one-flight length therefore contains `psi_b` with its full signed argument; odd graph jets are not geometrically absent.
2. `article/01c_geometric_setup_v18.tex` and the Part I relative-law proof construct the half-line actions `S_b` and positive amplitudes `B_b`, with uniform `C^k` convergence of the finite stationary excess action to `S_0 \oplus S_p`.
3. `article/23_two_contact_rigidity.tex` proves the earlier highest-jet envelope calculation for even jets. Its key mechanism is triangularity: at the first order at which a new graph jet can enter, one evaluates the pure new homogeneous boundary term on the linear half-line orbit; lower nonlinear corrections cannot modify that leading new degree.
4. `article/29_two_flight_benchmark.tex` independently verifies the same stationary-envelope bookkeeping in a finite two-flight calculation and shows that the independent-contact direction remains visible even at equal curvatures.

The v19 extension does not assume an unproved inversion of the scalar energy profile. It changes the observation: after residual time is integrated out, the *signed endpoint law* has support `S_b(u)+S_b(v)<d`. Positivity of `B_b` makes the support threshold itself observable, so the slice `v=0` recovers the unsymmetrized action `S_b(u)`. The odd-jet information is therefore present before the scalar endpoint coordinate is integrated out.

For a half-line orbit started at type `b`, the linear coefficients from the historical Jacobi recurrence are `varrho^i` on even sites and `frak r_b varrho^i` on odd sites. Repeating the reviewed envelope calculation for a graph jet of arbitrary degree `n>=3` gives the last-jet block

```
[[coth(n gamma), frak_r_0^n csch(n gamma)],
 [frak_r_1^n csch(n gamma), coth(n gamma)]]
```

with `frak_r_0 frak_r_1=1`. Its determinant is exactly one by `coth^2-csch^2=1`. This is the new mathematical step which removes individual evenness from local labelled contact rigidity. The leading geometry is not supplied: the observed onset gives `g`, and `S_b''(0)` gives both contact curvatures through the exact historical half-line Hessian formula.

## Material re-audited for C18-E2: unknown-geometry statistics

The fixed-table v17/v18 endpoint experiment remains correct but did not make geometry a statistical parameter. The v19 local experiment is built from:

- `article/18_boundary_information_v18.tex`: the scalar coarea proof for a linearly vanishing density `a_t(w_t)_+`, including truncated second/third/fourth score moments, independent thinning and the retained failure atom;
- `article/19_endpoint_critical.tex`: the exact billiard endpoint density and positive-offset physical transfer;
- `article/29_two_flight_benchmark.tex`: a finite-window physical inverse and parametric `N^{-1}` risk result on supplied finite-dimensional families;
- `v5/50_self_calibration.tex`: a charged physical self-calibration construction for onset/gap and leading curvature information.

`article/18a_vector_boundary_information_v19.tex` polarizes the scalar coarea calculation. The scalar coefficient becomes the matrix `J_Sigma = integral a_0 V V^T/|grad w_0|`, and the same truncation yields a multivariate LAN expansion. The Gaussian shift gives the efficient score estimator and the sharp local quadratic minimax value. For the billiard family, `V` is the derivative of the signed endpoint support function `d-S_0-S_p`. The new signed-rigidity theorem proves that the collection of these support velocities separates every nonzero direction in a fixed finite contact-jet model, and compactness reduces the separating family to finitely many positive offsets.

Thus the v19 statistical statement is not obtained by relabelling the fixed-table finite-versus-boundary test: the unknown table is the local parameter.

## Mechanical referee items

- The lattice translation in the channel label has been renamed from `lambda` to `ell`; `lambda=varrho^2` is reserved for the return multiplier.
- The formal setup now states explicitly that all geometric derivatives in the relative theorem are taken in the centered coordinates `t=j g_e(xi)+d`, holding `d` fixed rather than physical time.
- The direct appendix input list has been collected in `article/99_auxiliary_compendium_v19.tex`. This changes navigation only; the retained mathematical modules still compile into the manuscript.
- Root and manuscript README files, the v19 active-source manifest, proof ledger, literature audit and referee response are revision-specific rather than inherited v17 metadata.

## Scope of this audit

This note records the derivation path actually used for v19 and the historical checks made against the live repository. It is not a proof-assistant certificate. The new mathematical claims must be judged from the displayed proofs in `article/23a_signed_endpoint_rigidity_v19.tex` and `article/18a_vector_boundary_information_v19.tex`, together with their cited dependencies.
