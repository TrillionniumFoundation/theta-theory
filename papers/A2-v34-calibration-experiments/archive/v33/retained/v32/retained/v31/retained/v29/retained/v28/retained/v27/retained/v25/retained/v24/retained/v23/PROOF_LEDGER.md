# A2 v23 proof and assumption ledger

Controlling report: v22 at ecfe49c9ab244ade504c9a727a4d110f72db4433. This ledger records claims and dependencies; it is not independent proof certification.

| Result | Input and conclusion | Proof dependency and limit |
|---|---|---|
| Theorem 1.1 / 7.1 | Growing genuine catalogue; time-uniform soundness and finite stopping under discovery hazards | Sections 2–6, conditional fresh samples, summable validation failures. The producer must be valid; arbitrary fitted gates are not certified physical. |
| Proposition 5.1 | Free-position rejection in a laboratory square; quotient TV error O(1/L) | Exact periodic tile mixture. Requires a periodic record gate and known diameter/area bounds; no cell coordinates or mixing. |
| Lemma 5.2 | Finite biased histograms to a C2 density estimate | Cell Bernstein bounds, quadratic reproduction, partition of unity. TV bias is amplified by h^-4; no smooth density-bias assumption. |
| Lemma 6.1 | At most r0+1+floor(log2 Q) records suffice | Tree, two independent cycles, integer index halving. No primitive recorded pair required. |
| Lemma 6.3 | Adaptive arrival tail | Iterated conditional absence probabilities and a finite union. Divergent cumulative hazards are needed for termination, not for soundness. |
| Proposition 6.4 | Randomized finite-aperture geometric producer with explicit hazard | Body-list, exact shortest-pair, blocker and periodic-gate oracle. Obstruction descent and path lifting are proved in text. Not acquired from unmarked trajectories. |
| Proposition 6.5 | Pointwise local-margin exhaustion | Fixed finite witness eventually belongs to a certified level; per-level precision plus Borel–Cantelli. No uniform rate or finite expected-cost claim for this exhaustion. |
| Theorem 7.1 cost | O(m4) free samples through epoch m; finite expected launch count for p>0 | Negative-binomial launch cost and a k^-6 tail. Counts proposals separately, not analytic-oracle bit complexity or apparatus travel time. |
| Corollary 7.2 | Geometric scan stops correctly by a stated epoch with high probability | The producer hazards and simultaneous accuracy event, not full-catalogue enumeration. |

Three unchanged active source files contain the complete local inverse, exact certificate and reference-free arithmetic from v22. Their Git blobs are pinned. Every old result remains in the exact retained/v22 tree and its nested companions.

## Delicate points checked in the written proofs

1. The TV norm controls probabilities of cells after periodic postprocessing; it does not by itself control derivatives of a raw density.
2. Free-location rejection is not return-success conditioning. Hidden bodies still affect the target normalization.
3. A single-copy gate is nonperiodic and is not covered by the laboratory-square proposition.
4. Current-epoch error, not the cumulative earlier error budget, enters the stopping tail. The all-epoch event is used separately for correctness.
5. The proposal is chosen before validation, and each pilot-dependent histogram uses fresh samples. Adaptively selecting the final component needs no further union bound on the simultaneous event.
6. A producer can remain noninformative forever without invalidating soundness. The stated hazard condition is the premise for termination.
7. Rational decoding precedes the missing-area test; an unresolved decoding withholds certification.
8. All model constants may depend on the full uniform class. Reference-free does not mean universal over analytic tables.

Finite exact tests and selected retained nonlinear ray diagnostics support displayed algebra only. They do not execute the physical geometric oracle, prove analytic continuation, certify priority or replace mathematical review.
