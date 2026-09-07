# Proof dependencies for v20

The controlling source and report are pinned in README.md. This ledger is a navigation aid, not a correctness certificate.

| New result | Inputs | Actual conclusion |
| --- | --- | --- |
| `lem:kernel-moment-chart` | Full support; finite-dimensional continuous product spaces; L2 projection | The constrained moment image is open and convex, with explicit positive density coordinates |
| `thm:exact-kernel` | Previous lemma; retained full-support moment lemma and containment theorem; polynomial nonvanishing | Exact kernel iff feasibility and full quotient-pencil column rank; locally dense positive witnesses; finite grid and finite-atom mixture witnesses |
| `prop:forced-kernel` | Orthogonal projection and small annihilation-preserving positive tilts | Common forced kernel equals multiplication closure; closure is idempotent |
| `prop:block-kernels` | Independent block masses and imbalances; polynomial interpolation and factor theorem | Explicit classification and positive physical witnesses; the eight-point nonexact case is included |
| `cor:kernel-history-rank` | Exact-kernel theorem; augmented evidence rank; inverse chart with kernel-coordinate integration | Attainable constrained normalized rank and unconditional acquired mass |

The monomial center remains the chain `lem:leja-scales` -> `lem:newton-attainment` plus `lem:tame-rectangle` -> `thm:intrinsic-checkpoint` -> `thm:intrinsic-streaming`. The arrows do not suppress dependencies: actual acquisition mass, whole-image covering, and temporal compatibility each require their own argument. The raw-update denominator and finite-horizon accumulated-error recurrence remain essential.

The affine and analytic consequences remain `lem:v18-projective-law` plus `lem:v18-thick-linear` -> `thm:v18-affine-classification`, then `thm:v19-covariance-realization` and `lem:v19-analytic-orders` -> `thm:v19-analytic-memory`. The latter is not a general multi-step degeneration theorem. The integer-envelope inverse uses the complete unbounded budget curve after a forward law has been proved.

All inherited formal blocks are retained byte-identically. The new theorem's determinant rank is the maximum rank on an annihilation slice; the old theorem's optimized nullity describes the minimum rank over all full-support priors. These are different optimizations and are not conflated.
