# Stationary-window input map

The new proof is contained in core modules 59 and 60. No additional external theorem is assumed.

1. **Collision splitting and regular data:** `lem:collision-spectral-input`, `lem:physical-bv`, `lem:explicit-frequency-error`. The external collision-space import is Demers--Zhang (bibliography DZ), already mapped in `COLLISION_INPUT_MAP.md` and the norm appendix. Its official arXiv record is 1210.1261. This map does not reinterpret the paper's abstract as verification of all imported norm estimates.
2. **Damped finite-order words:** `thm:high-order-damped-unsmoothing`, `cor:finite-jet-damping`, `lem:all-small-mass-moments`. Fixed orders 40 and 29, residual degree 79, at most 80 insertions; the constants are not uniform as those orders grow. Every nonsingleton block count 1 through 40 is included.
3. **Exact windows:** `lem:window-interval-envelopes`, `eq:box-lower-envelope` in retained v27 module 57. The Beurling--Selberg construction is proved there, including endpoint values; no extremality claim or new theorem is needed. A four-dimensional probability law with three discrete coordinates is never assigned a Lebesgue density merely to use this envelope.
4. **Moments and projection:** `lem:fixed-even-maximal` at fixed order 128; bounded initial density domination; augmented matrices with uniformly bounded inverses; true four-dimensional changes of frequency variables. The discarded-coordinate tail is divided by the shrinking output volume explicitly.
5. **Stationary normalization:** `prop:induced-suspension` and the Kac tower identity. The normalization is `mean(return roof)=mean(collision roof)/c*`; collision roof bias is bounded-BV, return roof bias need not be. `thm:exponential-return` controls the latter by Holder transfer, not by an assumed variation norm.
6. **Physical coupling:** positive uniform lower free flight, bounded one-flight roof and labels, high collision moments, retained `prop:physical-window-coupling` at a higher fixed exceptional exponent, and the exact initial/final partial-return contributions.
7. **Relative conditioning:** positivity of the actual denominator; event inclusions between enlarged/contracted boxes; subtraction before normalization. All four events and their conditional measures are on the same stationary return suspension.

Numerical tests below verify algebraic margins and finite tower identities. They do not establish a continuum spectral gap, universal high-order bounds or microscopic raw-density regularity.
