# Round 45: response to the Round 44 referee report

Controlling report: `REFEREE_REPORT_ROUND44_GPT56_PRO_HARSH.md`, commit
`9417c8d9ed14f8a8c4ba538435bf29837630b0ae`.
The reviewed predecessor was `1a96a07f12c69ec4390d9848e05e29ffc808f479`.
The new canonical article is `ROUND45_REVISION.tex`; every input is ordinary
source under `round45/`. Historical reports and manuscripts remain provenance,
not the active publication unit.

## Mathematical response

| Objection | Revision and proof location |
|---|---|
| M1: false shallow-depth exponent composition | `inverse_stability.tex` replaces both inconsistent calculations by one inverse with `L_J=Q^{64(J+1)^2}`. The moment and Gram exponents add to at most `53(J+1)^2`, at every depth. Every scale, modulus, posterior rate and confidence threshold uses this same constant. |
| M2: missing washout derivative polynomial | `infinite_jacobi.tex`, lemma `lem:washout-derivatives`, retains the common base decay rate in the ordered Duhamel integrals. It includes `(1+log(i+1))^{|alpha|}` and proves summability with any smaller positive power margin. The undifferentiated likelihood uses its own envelope. |
| M3: nonexistent zero-time diagnostic cell | `growing_depth_uncertainty.tex`, `thm:honest-jacobi-cylinders`, requires precisely the `R_J` positive cells. The origin is a deterministic exact value. The statement covers both protocols. |
| M4: condition audit only sketched | `prop:effective-gram-reconstruction` specifies induced matrix infinity norms, polynomial coefficient one-norms, every linear-solve and quadratic-form bound, denominator lower bounds, and ratio/square-root constants. The logarithmic prefactor audit is displayed through `4400 F (J+1)^3`, dominated by `A_0=5000F`. |
| M5: no finite-n shrinking-net argument | `prop:finite-n-field-concentration` proves the score and conditional-square probability bound, including empirical absolute noise and interpolation. `thm:finite-n-posterior-separation` retains numerator, denominator and transient constants. Explicit coordinate cylinders provide an upper bound on minus log prior mass. `thm:growing-depth-recovery` applies these bounds at the shrinking separation. |
| M6: no policy-uniform no-washout field control | `linear_time_protocol.tex` defines `d_*`, proves its common convolution bound, and verifies every hypothesis of the finite-n result. The triangular coupling is explicit. `thm:adaptive-laplace-tracking` additionally follows the complete conditional-information sequence and identifies full LDPs along convergent subsequences. The information floor is not misidentified as the actual rate under arbitrary baselines. |

The condition calculation is stronger asymptotically than the proposed cubic
jet exponent: it gives a quadratic jet exponent and a cubic depth exponent
in the sampled response separation. Consequently the concrete sufficient
regime improves from `J_n=o((log n)^(1/5))` to
`J_n=o((log n)^(1/3))`, with an explicit shrinking coefficient radius.
This remains a sufficient result, not a minimax-optimality claim.

The confidence proof now uses stopped nonnegative exponential
supermartingales. It never assumes that conditioning on an adaptive visit
count leaves a Gaussian sum. Allocation over all cells and visit counts
provides a single time-uniform frequentist coverage event. These sets are
not called posterior credible sets. All operator conclusions are explicitly
exponentially weighted.

## Publication and verification

The revision source is committed before distribution artifacts are added.
`round45/SOURCE_MANIFEST.json` hashes every article input, this response,
the proof ledger, historical map, tests, verifier and the sole read-only
review workflow. The verifier executes no source generator and checks the
hashes again after tests and compilation.

A distribution receipt identifies the immutable source commit and the exact
PDF and log hashes. It is necessarily a descendant of that source commit:
a Git commit cannot contain its own SHA as file content. The source manifest
is unchanged between the source commit and the distribution receipt commit.
This separates a source freeze from artifact publication without a circular
self-hash claim. The publication record states the actual status; a queued
or failed runner is never counted as a passed check.

## Interpretation

The mathematical arguments above are supplied for a new independent review.
The exact-arithmetic tests check finite examples and several all-depth
polynomial inequalities, not the entire analytic proof. No proof-assistant
certification or independent referee acceptance is claimed. The referee's
venue assessment and suggestions of optimality, unweighted operator recovery,
and a nonparametric Bernstein--von Mises theorem are not conclusions of this
paper and are not relabeled as completed theorems.
