# Inputs for the new peripheral and compression theorems

No additional external theorem is imported in revision 17. The following are the exact inherited dependencies and the newly proved steps.

The endpoint improvement uses the centered second moment of the bounded collision compensation from `core/22_collision_covariance.tex`, and the diffusive spectral word and smoothing constants from `core/36_near_origin_defects.tex`. Both endpoint factors are bounded by one. Removing their phases is therefore controlled in the stationary integral by `|w| ||S_ell h||_2`, not by `ell |w| ||h||_infinity`. This is the source of the quadratic regularity budget.

The constant-phase argument uses the bounded-BV collision covariance estimate applied to the real and imaginary parts of a centered unit phase. A deterministic time after the mixing threshold is selected with cosine at most `-3/4`. The characteristic integral over that time is compared with one by the centered collision second moment. The pure collision-constant direction is treated explicitly.

The complex-function argument uses the modulus-variance estimate and circle-truncation lemma of `core/35_quantitative_phase_defects.tex`. No positive lower modulus, pointwise phase representative or distribution-space reconstruction is assumed.

The exact return lift uses the true tower partition and norm formulas of `core/37_actual_return_defects.tex`, together with the identity `h_3=1-eta/c*`. The extra phase is constant on strictly positive ages; its BV norm is uniform. The finite-age approximation of the full lift uses the same genuine return tail and finite-record first-variation bound as in v16.

The finite-rank operator uses the actual unitary twisted Koopman map, not an independently sampled transition process. Its cell integrals include the full unbounded return record. Reconstruction is an elementary uniform estimate for piecewise constant functions on the five original section rectangles. Orthogonal decomposition of a physical residual yields the compressed residual comparison without an eigenvector normality hypothesis.

The finite-time consistency estimate uses an exact projection telescope. The phase cut off at a collision count is expanded into finite binary visit words, so all membership jumps are counted through the inherited finite-record lemma. The cumulative-return tail from `core/20_cumulative_returns.tex` gives the omitted-event error.

There is no imported theorem asserting that these finite-rank spectra converge to an anisotropic spectrum or that a local peripheral resolvent gives the entire Fourier tail. Those are distinct estimates in the original raw inversion problem.
