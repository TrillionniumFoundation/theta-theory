# Inputs for the exact physical endpoint calculation

## Geometry and probability

`core/02_physical_records.tex`: physical next-disk lattice label, exact Euclidean flight, invariant collision probability, positive lower flight bound and uniform finite horizon.

`core/13_uniform_physical_clock.tex`: `W_R(t)` is net fundamental-cell displacement and `C_R(t)` counts physical collisions in `(0,t]`.

`core/60_stationary_physical_conditioning.tex`, `lem:stationary-length-bias`: the actual current-collision/age law is `dnu(x) da / mean(tau_R)` on `0<=a<tau_R(x)`. This is a coordinate description of the same equilibrium law, not a replacement initial distribution.

The new proof fixes the same convex polygonal fundamental cell at both endpoints. Uniform horizon gives a fixed finite set of translated cells encountered by one flight. Convexity gives an interval per cell. No new long-itinerary singularity, derivative or product-structure estimate is imported. The initial and final cell offsets remain in the exact event and its amplitudes.

## Central analysis

`core/15_exponential_returns.tex`, `lem:collision-spectral-input`: local uniform collision splitting, smooth multipliers and bounded mass functional.

`core/22_collision_covariance.tex`: mean-preserving smoothing, small-BV residual variance, continuous collision Green--Kubo matrix and covariance approximation.

`core/23_stopped_gaussian.tex`, `lem:smooth-collision-expansion`: the shrinking analytic ball, cubic spectral expansion and projector difference. The new proof uses a deterministic collision clock, so no stopped-time error is invoked.

`core/33_joint_nondegeneracy.tex`: uniform ellipticity. The projected collision covariance and physical covariance are related by a displayed exact linear algebra identity.

`core/66_positive_microscopic_conditioning.tex`: positive kernel, its absolute first moment and the normalization inequality. Only the kernel and normalization are reused; no geometric-removal budget is needed for the original physical endpoint.

## Literature comparison, not an additional proof import

Szász--Varjú (2004), already in the bibliography, concerns the Lorentz-process local theorem. Dolgopyat--Nándori (2020), arXiv:1710.08568v1, Definition 2.2 and Section 2.4, treats base mixing local limits and suspension age decompositions. The new related-work paragraph compares those roles to the exact fixed-count physical age overlap. It does not assume a radius-uniform mixed collision MLCLT from that reference, nor identify such a result with the moving-section four-coordinate raw LLT.

The finite diagnostics test interval convolution, signs, deterministic age evolution, lattice offsets, finite Fourier identities, covariance factors and rational rates. They do not establish any missing middle-frequency dynamical estimate.
