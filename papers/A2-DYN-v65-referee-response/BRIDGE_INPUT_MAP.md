# Inputs to the conditional physical bridge theorem

This map describes dependencies of the new proofs, not additional assumptions or proof certification.

| New step | Retained input | Precise use |
|---|---|---|
| Uniform central chronological product | Local collision splitting and smooth perturbation (`15`, `23`); BV smoothing and small-mass variance (`22`) | At a mixed boundary use the difference of the two projections, including zero-length blocks. Total length controls the all-complementary word. |
| Joint outer collision band | Fixed spectral jets (`46`), small-mass cumulants and high-order unsmoothing (`48`, `52`), wide collision band (`59`) | Residual order 40, spectral order 29, at most 80 multipliers plus a fixed number of segment boundaries. No growing expansion order. |
| Endpoint plus path characteristics | Endpoint-safe envelopes (`57`), augmented-coordinate projection (`59`) | Integrate four endpoint frequencies and remove the fourth coordinate using the 128th moment. Replace an oscillatory numerator by its modulus bound, not by positivity of that numerator. |
| Conditioned coarse-grid tightness | New uniform joint characteristic comparison | Three blocks, eighth-order trigonometric probe, grids to `log_2(m)/200`; frequencies to `m^(1/1600)` and union error `m^(-9/2800)*sqrt(log m)`. |
| Inside-cell tightness | Fixed even collision maximal moments (`43`) and actual endpoint lower bound (`59`) | The 128th moment pays both the number of cells and the denominator `m^(-6/25)`; remaining exponent is `3/40`. |
| Physical path coupling | Exact stationary length biases and observation coupling (`60`); bounded one-flight horizon and positive minimum flight length | Union over deterministic physical integer times; no independence of ages, clocks, or sums. |
| Other endpoint events | Stationary relative event comparison (`60`) | Push forward the same conditioned initial measure by the same physical path. |
| Concrete weighted denominator | Gaussian bridge interior covariance; conditional functional limit | A finite-dimensional Gaussian box integral gives a positive uniform cylinder factor. Hard path indicators are treated by a Gaussian boundary-null argument. |

No new external theorem is imported. The Gaussian bridge formula, the trigonometric test, dyadic chaining, and conditional tightness are proved in the added text. The research comparison with random-walk bridge principles does not license importing independence, a Markov transition density, or a microscopic local limit into this deterministic billiard proof.

The remaining microscopic fixed-return complement, pointwise signed raw correction, long-time inverse-coarea derivative budget and microscopic physical-event replacement remain those of the inherited manuscript. None is inferred from the bridge theorem.
