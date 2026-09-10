# A2 v11 proof and information ledger

| Result | Hypotheses and observation | Conclusion | Proof location |
| --- | --- | --- | --- |
| General relative physical law (retained) | Separated positive-curvature smooth periodic channels, no general symmetry or finite-horizon condition | Nonlinear actions and normalized flux factorize with uniform fixed-order derivatives | `v3/10_geometry_action.tex`, `v3/20_integration.tex`, `v4/10_boundary_layers.tex`, `v5/15_differentiated_operators.tex` |
| Full energy inverse and compatibility (retained) | Two labelled even limiting laws with normalization | Both full symmetrized energy profiles and predicted odd law | `article/20_boundary_compatibility.tex` |
| Theorem 10.1 | Normalized C3 profiles, common first-derivative bound | Two-sided nonlinear Abel-flux stability, exact affine nullspace, mixed bound | `article/21_abel_stability.tex` |
| Proposition 10.2 | Fixed nontrivial abstract smooth profile ball | Exact monomial multiplier and C2 instability; no physical lower bound | Same file; report benchmark credited |
| Theorem 13.1 / Corollary 13.2 | Known calibration; labelled binary physical preparations; K_m and relative C3 certificate | Error h^(m-5/2)+tau^j+t h^(-5/2)+delta; sufficient exponent 2+6/(m-5/2)+gamma/abs(log tau) | `article/26_abel_acquisition.tex` |
| Lemma 13.3 | Only m-point positive stencils and common regularity | Globally smooth reconstruction; separate approximation, smooth-bias and scalar-noise bounds | Same file; no endpoint observations |
| Theorem 14.1 | Independent pilot, clipped boxes, upper gap error, fixed collar margin, uniform C3,1 flux bound | Calibration contributes alpha+j*zeta+j*rho without negative mesh powers | `article/27_profile_calibration.tex` |
| Lemma 14.2 | Unknown smooth finite-flight remainders; known coarse bracket and positive class bounds; flight numbers 1,2 | Charged upper gap and area/multiplier calibration, cost xi^(-2-2/m) times the stated log | Same file; noisy bisection and positive-node extrapolation |
| Theorem 14.3 | General relative physical class plus the stated common pilot/profile bounds; actual g,A,gamma unknown | Full-profile recovery on [0,D], including origin; deterministic box-uniform exponent with gamma_+ | Same file; independent stages and explicit pilot charge |
| Endpoint and finite-dimensional benchmarks (retained) | Their own specified observations, families, losses and bounded-flight restrictions | Their previously proved conclusions, including sharp finite-dimensional rates | All original active files and appendices retained |

## Analytic points checked in the new proofs
The Abel forcing is estimated in its weighted form instead of dividing by sqrt(x). The endpoint term of the transform is explicit. The mixed geometric-mean bound is not used as a discrepancy norm. The interpolator is globally smooth. Its first stencil has no zero node. The bridge and calibration errors are smooth functions, not arbitrary nodal errors. The Bernoulli variance uses the small physical probability. The pilot gap is one-sided, the target subcollar has a fixed positive margin, and estimates are clipped even on failed pilot outcomes. The bisection charge is deterministic. No calibration theorem from an exact-family model is imported.

## Boundaries of the conclusions
The finite dictionary is Borel but no running-time bound is claimed. The sufficient exponent depends on a supplied relative convergence certificate and, in the uniform unknown-normalization theorem, a supplied upper multiplier bound. Labels and coarse class bounds are not removed. The abstract C2 alternatives have not been realized as billiards. Full-profile recovery is not arbitrary asymmetric graph recovery. No full-profile minimax lower bound, optimal endpoint Holder space, complete physical image theorem, or journal acceptance is asserted.

## Preservation and verification
All 176 reviewed active formal environments survive byte-identically in their previous relative input order; 16 new formal environments give 192 total. This counts both statements and proofs and is not a theorem-certification count. The unchanged original companion remains separately buildable. See `VERIFICATION.json` for actual clean-build and suite outcomes. Each finite suite was run normally and with Python optimization; suites overlap. Neither tests nor compilation constitute formal proof verification or a remote CI result.
