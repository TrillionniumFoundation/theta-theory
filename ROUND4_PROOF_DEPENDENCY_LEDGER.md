# Round-four proof dependency ledger

Status: **PASS**

The order below is computed from the declared DAG; a cycle fails the gate.

| Node | Controlling paper | Dependencies | Load-bearing theorem labels |
|---|---|---|---|
| `A1` | `A1-exact-benchmarks` | none | `thm:r3-a1-impact`, `thm:r3-a1-calibration` |
| `A2` | `A2-sinai-homological-pressure` | none | `lem:r3-a2-atlas`, `thm:r3-a2-high`, `thm:r3-a2-llt` |
| `B2-GC` | `B2-collision-clusters-dynamic-ldp` | none | `lem:r3-b2-generating`, `thm:r3-b2-gc-cluster`, `thm:r3-b2-source-continuation`, `thm:r3-b2-gc-ldp` |
| `A3` | `A3-full-empirical-path-ldp` | A2 | `thm:r3-a3-block`, `thm:r3-a3-collision-ldp`, `thm:r3-a3-cotangent` |
| `B1` | `B1-microcanonical-preparation` | B2-GC | `lem:r3-b1-convex`, `thm:r3-b1-coefficient`, `thm:r3-b1-transfer` |
| `A4` | `A4-history-memory-universal-pressure` | A2, A3 | `thm:r3-a4-memory`, `thm:r3-a4-memory-decay`, `thm:r3-a4-nonlinear`, `thm:r3-a4-tangent` |
| `B2-MC` | `B2-collision-clusters-dynamic-ldp` | B2-GC, B1 | `thm:r3-b2-mc-ldp` |
| `B3` | `B3-hamilton-boltzmann-cotangents` | B1, B2-MC | `thm:r3-b3-duality`, `thm:r3-b3-gauge`, `thm:r3-b3-gaussian` |
| `B4` | `B4-nonlinear-kinetic-semigroups` | B2-MC, B3 | `lem:r3-b4-corrector`, `thm:r3-b4-generator`, `thm:r3-b4-comparison`, `thm:r3-b4-micro` |
| `C1` | `C1-information-risk-sensitive-saddles` | B2-MC, B3, B4 | `thm:r3-c1-adaptive`, `thm:r3-c1-filter`, `thm:r4-c1-lan` |
| `C2` | `C2-cotangent-rigidity-tangent-representations` | A1, A2, A3, A4, B2-MC, B3, B4 | `thm:r3-c2-strict`, `thm:r3-c2-girsanov`, `thm:r3-c2-memory` |
| `D1` | `D1-deterministic-theta-contractions` | B1, B2-MC, B3, B4, C2 | `thm:r3-d1-commutation`, `thm:r3-d1-likelihood`, `thm:r3-d1-triangle` |

## Non-circular hard-sphere order

`B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`

## Non-circular Sinai order

`A2 -> A3 -> A4 -> C2 -> D1`, with the independent A1 platform entering C2 only through its typed map.
