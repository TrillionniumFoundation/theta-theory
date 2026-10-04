# A2-DYN v1 — source and adversarial proof audit

## Frozen sources

The base is `af2390e3073acf8ccd90b10d7566e30cbf18c425`, the completed final
referee-style review of A2-GEOM v43. Its author is
`4557df22f5c72bc80943690ecd6c2e39de3734ab`. This revision adds a separate
A2-DYN directory and workflow; no earlier paper or report is edited.

Primary historical derivation inputs read:

- `revision/round17-referee-final/A2_MATRIX_COEFFICIENT_RAW_LLT.tex`;
- `A2_ROUND11_PERIODIC_CERTIFICATE.json`;
- `workstreams/2026-09-08-next-step/README.md`;
- `workstreams/2026-09-08-next-step/research/A2_Two_Collision_Response.tex`;
- the A2 v43 primary/supplement and final review described in the frozen source.

## Corrections supported by actual arguments

The old periodic JSON gives orbit names, assigned record summaries, roof
intervals and residual claims, but no reconstructible angle boxes or complete
interval equations. It is preserved, not promoted to a proof. The new winding
certificate starts from a physical reflection equation and checks a finite
exhaustive third-obstacle list with an analytical bound outside that list.

Periodic roof and lattice phases must be handled simultaneously. The new
unimodular matrix includes the induced return period as a fourth column;
its proved implication is explicitly at zero roof frequency. Periodic
averages exclude a constant continuous roof coboundary, but that alone does
not prove full joint nonarithmeticity or positive definite covariance.

Consecutive flights are functions of two initial section coordinates, not
independent integration variables. The optical action correctly eliminates
interior contacts. Its positive Schur complement produces nonzero density
jumps and explains a raw `1/|b|` boundary term. In fact all regular critical
words are normal-to-normal minima, unique for their center sequences, and
their individual jumps have an explicit exponential upper bound. This does
not control critical-value clustering or singular itinerary boundaries.

The old global L1 mechanism is false for the explicit inducing set constructed
here. The proof uses the `(0,0,2n)` component's nonzero right jump, not a numerical
Fourier experiment. The repair subtracts and then exactly restores explicit
edges. Its residual criterion keeps the original density and central target.
The high-frequency constants must satisfy an actual compatibility inequality;
letting the number of integrations grow without controlling its derivative
constants is insufficient.

## Adversarial checks and their limits

The certificate uses only exact fractions, integer square-root enclosures and
Taylor remainders. Floating decimals in its output are displays of proved
rational bounds. The independent suite separates exact matrix, suspension and
frequency algebra from floating ray-tracing Hessian checks. Both normal and
optimized Python executions must agree. The tests reject a sample incompatible
frequency budget. The program never emits `full_billiard_LLT_verified=true`.

Source qualification verifies exact committed bytes, the entire allowed diff,
explicit open-stage flags, compilation without shell escape, references and
PDF checksums. Passing it certifies that these checks ran on those sources,
not that every continuum proof is formally verified. This is an author-side
adversarial audit, not an independent referee report. The current mathematical
arguments should be reviewed, especially the physical Hessian/critical-word
classification and the separation between a single edge and a complete sum.
