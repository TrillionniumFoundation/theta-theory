# Round-six internal hostile rereview

**Status:** PASS

The review was run on the exact materialized `ROUND6_POSITIVE_CLOSURE.tex`
files.  It does not infer correctness from compilation or theorem counts.
It checks the proof bodies of the labels which answer the latest explicit
counterexamples and requires the named mechanisms to occur inside those
proofs.

| Paper | Status | Critical proof labels |
|---|---|---|
| `A1-exact-benchmarks` | **PASS** | `prop:r6-a1-work`, `thm:r6-a1-response` |
| `A2-sinai-homological-pressure` | **PASS** | `thm:r6-a2-dolgopyat`, `thm:r6-a2-master-llt` |
| `A3-full-empirical-path-ldp` | **PASS** | `lem:r6-a3-markov`, `thm:r6-a3-collision-ldp` |
| `A4-history-memory-universal-pressure` | **PASS** | `thm:r6-a4-conditional`, `thm:r6-a4-decay`, `thm:r6-a4-volterra` |
| `B1-microcanonical-preparation` | **PASS** | `lem:r6-b1-poisson`, `thm:r6-b1-coefficient` |
| `B2-collision-clusters-dynamic-ldp` | **PASS** | `lem:r6-b2-gramian`, `thm:r6-b2-cyclic`, `thm:r6-b2-gc-ldp` |
| `B3-hamilton-boltzmann-cotangents` | **PASS** | `thm:r6-b3-duality`, `thm:r6-b3-gaussian`, `thm:r6-b3-kernel` |
| `B4-nonlinear-kinetic-semigroups` | **PASS** | `thm:r6-b4-comparison`, `thm:r6-b4-generator` |
| `C1-information-risk-sensitive-saddles` | **PASS** | `lem:r6-c1-bayes`, `thm:r6-c1-lan`, `thm:r6-c1-testing` |
| `C2-cotangent-rigidity-tangent-representations` | **PASS** | `thm:r6-c2-memory`, `thm:r6-c2-optional`, `thm:r6-c2-strict` |
| `D1-deterministic-theta-contractions` | **PASS** | `thm:r6-d1-interchange`, `thm:r6-d1-lan`, `thm:r6-d1-projective` |

All eleven papers pass the counterexample-aware proof-body tests,
including source materialization, full-port work, the A2 three-regime
formula, recession defect mass, transmission zeros, finite-volume
saddles and likelihood centres, trace-class actual-contact control,
two-domain duality, weak-energy comparison, observation-aware Bayes
updates, complete-history optional projections, and projective
steep-pressure lower bounds.
