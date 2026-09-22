# Proof ledger — sixth Markov revision

Statements are ordinary mathematical proofs in native TeX, not proof-assistant formalizations. Compiled numbers and pages in both editions are recorded in the build receipt.

## Dependencies

```
metric bounded distortion + primitive admissibility + stationary cylinder law
 + monotone renewal weights + finite-delay observable
  -> strict prefix-attachment decrease (even for equal suffix masses)
  -> balanced admissible tree / bounded unary chains / fixed dilation
  -> observable orbit cylinder separation / off-image quantization converse
  -> exact suffix closure / actual finite register realization
  + retained v4 general posterior-orbit converse
  -> matched Markov-renewal finite profile

Hölder Gibbs and geometric potentials + exponential tail rate
  -> admissible upper convolution + endpoint lower bounds
  -> two pressure roots + summability + tilted Gibbs lower bounds
  -> derived squared-error exponent

Parry measure + equal geometric ratio + polynomially modified renewal tail
  -> equal-depth profile / exact graph growth
  -> critical power-log, log-log and bounded factors / uniform windows

true stationary posterior recursion + conditional fourth-mean contraction
  -> inward finite compander / uniform fourth moments
  -> recursive uniform-in-time upper + full-history orthogonal lower
  -> matched whole-register excess without minorization

current A2 known-mark Poisson protocol
  -> jitter TV comparison / physical grid-boundary crossings
  -> Gaussian histogram reconstruction / overflow tail
  -> joint sample and finite-alphabet deficiency bound
```

## Statements and scope

| Label | Actual proof work | Required qualifications |
|---|---|---|
| `lem:v6-suffix-energy` | Telescopes decreasing weights; scale submultiplicativity; stationarity; positive legal conditional masses. | Mass need not strictly decrease. Prefix is nonempty. Both renewal ratio bounds are used. |
| `lem:v6-balanced` | Maximal-energy splitting; child comparability; primitive graph gives bounded unary chains and exponentially many fixed-length descendants. | Exact degree count replaces the regular full-tree identity. Fixed dilation, not exact same-leaf optimizer. |
| `lem:v6-cylinders` | Delayed outputs recover the snowflake orbit distance; physical gaps give separation after the common prefix. | Strong physical separation remains required. General constant/unobservable f is not included. |
| `lem:v6-realization` | Disjoint Hilbert tubes permit arbitrary off-image centres; strict energy forces suffix closure; store and shift actual tree vertices. | All internal vertices, unary nodes and empty word are persistent states. |
| `thm:v6-profile` | Previous lemmas plus full retained general posterior-orbit converse. | All randomized/time-dependent machines in the lower class; stationary deterministic upper; long-time average risk for the renewal process. |
| `lem:v6-partition` | Concavity separates suffix sum; incompatible joins dropped only for an upper bound; spatial and terminal terms lower-bound. | No full-shift factorization across forbidden edges. |
| `thm:v6-pressure` | Root monotonicity from positive conditional probabilities and primitive branching; all-word summability; zero-pressure Gibbs measures. | Exponential tail rate gives an exponent. Temporal lower uses q'<q before taking a limit, so polynomial tail factors are not suppressed. |
| `cor:v6-markov-matrix` | Admissible edge potential and Perron theorem. | Powers are entrywise on legal entries; structural zeros stay zero also at s=0. |
| `ex:v6-delay` | Planar similarities, golden-mean graph, one-step delay reconstruction. | Scalar output is noninjective, but the delay vector is quantitative. |
| `thm:v6-critical` | Parry cylinder mass and word counts; fixed-depth state upper and Hilbert-tube lower; harmonic sum asymptotics. | Equal ratios and the specified renewal family; no claim to classify all Gibbs critical corrections. |
| `thm:v6-window` | Uniform Riemann sums / endpoint truncation / summable domination / geometric tail estimates. | Exact limit of the finite profile, not exact optimal leading coefficient. |
| `thm:v6-filter` | True full-history mean orthogonality; fixed-time M-centre lower; inward companding; conditional L4 and L2 recursion bounds. | Stationary mean has L4 moment and positive density on a cube; mean recursion is an explicit assumption. No common-reference kernel assumed. |
| `cor:v6-gaussian` | Gaussian projection and Riccati contraction verify the exact mean recursion, positive mean density and moments; translated kernels disprove every fixed-step global minorizer. | Nonzero stable autoregression, positive process and observation variances. Constants deteriorate near loss of contraction. |
| `thm:v6-interface` | Exact state/event pairing and register bijections. | Event alphabet finite. Continuous free decoder side information is not covered by a finite factor. |
| `thm:v6-a2-budget` | Direct count likelihood comparison; deterministic physical quantization; parameter-independent reverse histogram kernel and Gaussian overflow control. | Fixed known marks, centre, matrices and compact local parameter set. Sufficient alphabet bound only. Covariance conditioning not uniform across rank degeneration. |

## Constants and distinctions

The profile constants depend on the graph, metric distortion, gaps, legal conditional mass lower bound, observable delay and weight-ratio bounds. Dimension is part of the geometric input, not a hidden claim of dimension-uniform constants. The pressure theorem requires a bounded cylinder approximation to an additive Hölder logarithmic scale. Uniformity in a critical window fixes kappa and confines q to a compact subinterval of (0,1).

The posterior theorem's explicitly displayed bound is `d(1+K4/(1-rho))^4 / [n^2(1-rho)^2]` for `(2n-1)^d` states. It controls the accumulated recursive error, not just the distortion of quantizing a precomputed exact mean. The exact mean at negative times is used only for coupling in the proof; it is not initially stored by the machine.

The A2 experiment's comparison jitter is not supplied to the physical encoder. A prescribed M must permit `J=floor((M-1)^(1/r))` with mesh `2R/J<=1`. Overflow costs one additional label. Small budgets outside this comparison regime are not silently assigned its asymptotic bound.

## Preservation

Both editions include the full v4 posterior-orbit theorem they invoke. The complete edition includes every preceding v5/v4/v3/v2 quantitative body and the first-edition foundational bodies. Original introductions and editions remain unchanged; v5's introduction is also retained in the complete view with its own labels. Preservation establishes identity, not independent validation of old proofs. Current A2 source copies are consultation inputs, not compiled as axioms or imported into the new proof.

## Finite diagnostics

`verify.py` tests rational forbidden-transition word identities, renewal-energy drop, balanced suffix trees with unary nodes, transfer-matrix roots, critical-window sums, inward compander inequalities, Riccati floors and exact finite-interface counts. Eight wrong variants must be rejected in ordinary and optimized Python. These finite checks cannot verify the infinite-dimensional quantifiers, Gibbs existence theorem or asymptotic proofs. The build verifies source identity, complete label resolution and stable typesetting separately.
