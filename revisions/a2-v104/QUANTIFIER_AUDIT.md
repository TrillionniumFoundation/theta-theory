# A2 v104 — proof-level quantifier audit

Audited source: `ff20178a3ac04712ceed5eb333e1ba3e1c518b74`.

| Issue | Exact statement used in v104 | Statement not inferred |
|---|---|---|
| Clock ratios | For each fixed clock index there exists a separating partner; compact families use a finite cover of locally chosen pairs (B.1) | Every pair separates, or one pair works uniformly on the whole family |
| Finite-sheet extraction | A polynomial finite map with isolated interior central fibre and the displayed polar-gap bounds yields all inverse sheets (2.2) | Every polynomial singularity satisfies those bounds |
| Discriminant approach | A positive tube is allowed to shrink at a different order, with inverse derivative bounds tested on it (2.2, 2.6) | Uniform inverse derivatives across a vanishing untested gap |
| Uniformity | Compact metric bounds and uniform slope/radius/residual inequalities give a uniform relative estimate (2.3) | Pointwise Puiseux convergence is automatically uniform in every parameter |
| Exact cancellation | The two-sided estimate is relative to the exact affine residual; zero distance is equivalent to one exact branch residual vanishing (2.2) | Equal nonzero leading costs determine the finite-time winning branch |
| Intrinsic data | The full leading residual set and tensor envelope are independent of inverse presentation (2.2–3.1) | A minimal semidefinite lift, or all sheets, are recoverable from the envelope alone |
| Endpoint classification | Fully visible representations in every endpoint dimension have the stated global minimum and complete minimal-dimensional fibre (4.3) | All nonvisible fibres or all larger nonminimal representations are classified |
| Visibility | A nonempty open positive-spanning class exists for each endpoint dimension (4.4) | Full visibility is generic over every positive definite block matrix |
| Coordinate deletion | The reduced minimizer's missing KKT inequality is necessary and sufficient for deleting that coordinate (4.5) | Repeated deletion always finds the global minimum in every representation |
| Native quotient image | Paired-contrast models have exactly the tensor-span dimension and spherical normalized secants (5.1) | Every higher-degree binary-mixture pattern has the same dimension |
| Fixed experiment | Contrasts and the Hellinger metric stay fixed while unknown centre masses vary (5.1–5.2) | The metric is independently adjusted without changing the probability model |
| Oracle input | The family and pattern are known, but the unknown numerical centre is not supplied | Query lower bounds still apply when the exact centre law already determines Q |
| Adaptive lower bound | Worst-case deterministic exact-query recovery; the transcript adversary needs no continuous selection rule (5.1) | A randomized, noisy-query, or empirical sample-complexity lower bound |
| Statistical interpretation | Labelled efficient Gaussian quotient experiments are equivalent iff Q agrees (6.1) | Unknown nuisance samples can be simulated, or exact ray queries equal observations |
| Root-pattern transitions | Fixed-pattern results and the explicit pullback X=h^2 distinguish first/second-order coordinates (5.3, 6.2) | The marking and constants remain uniform through every collision or boundary change |
| Real accessibility | Each ratio uses a retained real orthant face with a displayed positive-time transverse arc (A.2–A.3) | A formal or complex exceptional divisor is automatically feasible |
| Validation | Native principal compile and finite symbolic examples passed locally | Universal theorems are formally verified, or the full queued archival job succeeded |

The source preserves previous statements under their original assumptions; this audit records the operative v104 claims and the explicit clock erratum. It is a proof-scope record, not an independent referee acceptance certificate.
