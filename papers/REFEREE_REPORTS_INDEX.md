# Independent Referee Reports — Eleven-Paper Theta-Theory Tree

## Review target

These reports review the SHA-256-pinned eleven-paper clean-main source tree:

```text
566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2
```

The reports were prepared independently from the manuscript source, proof dependencies, theorem statements, and upstream source-only review packages. They are editorial assessments, not author rebuttals and not build receipts. Successful compilation, checksum verification, or finite-dimensional regression tests do not certify the novel analytic interfaces.

The repository's current `main` was not modified. This review branch targets the staged eleven-paper tree because the current `main` still represents a different five-paper active series.

## Editorial outcome

All eleven manuscripts receive **Reject** at the standard of *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the American Mathematical Society*. “Reject” does not mean every formula is wrong. It means that the manuscript, as submitted, lacks a proved central theorem of the claimed scope, contains a statement-level obstruction, or is not sufficiently original as a standalone top-journal paper.

| Paper folder | Recommendation | Principal blocker |
|---|---:|---|
| `A1-exact-benchmarks` | **Reject** | Correct elementary Bernoulli/baker benchmark, but mechanical typing and theta-selection claims are not earned; top-journal novelty is absent. |
| `A2-sinai-homological-pressure` | **Reject** | The uniform billiard spectral/local-limit packet is unproved; local finite-dimensional large deviations do not yield the claimed projective LDP. |
| `A3-full-empirical-path-ldp` | **Reject** | The countable-code, singularity-shielded approximation, and random-time Palm contraction needed for the full path LDP are not established. |
| `A4-history-memory-universal-pressure` | **Reject** | Only abstract Yosida and conditional-tower identities are proved; the Sinai-specific generator, tangent, and universal pressure are assumed or inherited. |
| `B1-microcanonical-preparation` | **Reject** | The central fixed-parameter microcanonical-to-grand-canonical log-Laplace transfer is false for an allowed time-zero source. |
| `B2-collision-clusters-dynamic-ldp` | **Reject** | Decorating cluster edges does not prove a joint LDP for actual collisions; topology, exponential tightness, and the lower bound are missing. |
| `B3-hamilton-boltzmann-cotangents` | **Reject** | The claimed unique cotangent pair is false because of an unquotiented gauge; the Gaussian tangent remains formal. |
| `B4-nonlinear-kinetic-semigroups` | **Reject** | The exact history tower is tautological; no infinite-dimensional semigroup convergence/comparison theorem is proved, and B1/B2 are load-bearing. |
| `C1-information-risk-sensitive-saddles` | **Reject** | The preparation-error accumulation diverges under the stated scaling, and the Isaacs equation changes an initial-preparation game into adaptive control. |
| `C2-cotangent-rigidity-tangent-representations` | **Reject** | The paper changes parent platforms while invoking contraction, overstates pressure differentiability, and inherits the unproved A3/A4 interfaces. |
| `D1-deterministic-theta-contractions` | **Reject** | The pressure Hessian omits the Boltzmann–Grad speed factor; the stochastic tangent/BSDE claims are not derived from hard spheres. |

Each folder contains a standalone `REFEREE_REPORT.md`.

## Cross-paper dependency findings

1. **A3 is not closed.** Consequently A4's universal-pressure claims and C2's path-rate contraction/rigidity claims cannot be treated as established.
2. **B1 contains a direct counterexample to its load-bearing transfer theorem.** Consequently the microcanonical diagonal claims in B4 and D1 do not follow.
3. **B2 does not prove the collision-marked dynamic LDP.** Consequently B3's deterministic cotangent interpretation and the B4/D1 kinetic hierarchy remain formal.
4. **C1 changes the control problem.** An initial preparation choice is not equivalent to pointwise adaptive Isaacs optimization.
5. **D1 has a normalization error at the first displayed hierarchy.** For a scaled pressure `(1/mu) log E exp(mu Theta)`, the second derivative is `mu * Cov`, not the unscaled covariance.

## Review method and limits

The audit applied the following tests:

- exact matching of theorem claims to proved hypotheses;
- construction and topology of every claimed LDP/contraction;
- type consistency across symbolic, collision, physical-time, history, kinetic, and stochastic platforms;
- scaling and normalization checks;
- hidden imported packets and circular dependencies;
- counterexample testing of universal statements;
- novelty and standalone-paper threshold.

The reports do not make a plagiarism finding and do not attempt a complete literature-priority determination. They identify the minimum mathematical defects that prevent acceptance on the claimed standard.
