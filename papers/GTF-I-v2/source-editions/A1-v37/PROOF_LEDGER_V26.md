# A1 v26 proof ledger

This is the actual versioned ledger requested in E25.2. All paths below are relative to `papers/A1-english-v26/`. A label identifies a statement and its adjacent complete proof, not a certification of its correctness. The controlling v25 report is retained at `review-basis-v25/REFEREE_REPORT.md`.

## Principal dependencies retained

| Mathematical obligation | Active source and labels | Use in this revision |
|---|---|---|
| Actual acquisition, complete confluent flags and positive scaled coordinate recovery | `text/collision_flags.tex`, `lem:newton-attainment`, `lem:leja-scales`; `core/03_transversality.tex` | No replacement by fixed-calibration rank; zero scales are never inverted. |
| Whole-image upper bound, every integer budget and one causal filter | `text/collision_direct.tex`, `thm:intrinsic-checkpoint`, `thm:intrinsic-streaming` | The scalar classification remains active and supplies the retained upper bound. |
| Product geometry with each edge's cap; arbitrary-centre tensor recovery | `v25/graph_model.tex`, `eq:v25-tensor-metric`, `prop:v25-fixed-order` | Inherited deterministic product law, not counted as new. |
| Two-sided acquired command chart | `v25/adaptive_proof.tex`, `lem:v25-regular-box` | The upper pushforward density survives arbitrary measurable restrictions. |
| Qualitative adaptive theorem, including the stronger order-prefix oracle | `v25/graph_model.tex`, `thm:v25-adaptive`; full proof in `v25/adaptive_proof.tex` | Retained byte-identically. The new quantitative theorem does not silently inherit the stronger oracle. |
| Bit inversion and original two-resolution star | `v25/graph_consequences.tex`, `cor:v25-graph-bits`, `cor:v25-star` | Retained; the full phase law extends the analysis of the same experiment. |

## New statements and complete proofs

| Label | Active source | Inputs and discharge |
|---|---|---|
| `lem:v26-finite-selection` | `v26/selection.tex` | Common subprobability + union bound + layer-cake integration. The expectation of a maximum is converted to the maximum of expectations only via the sum divided by the number of checkpoints. |
| `thm:v26-network-selection` | `v26/selection.tex` | Every selected path meets every separator. Small-loss mass is bounded before conditioning on the path; minimize separator capacity, integrate the tail, then average independent seeds. |
| `prop:v26-flow` | `v26/selection.tex` | Vertex splitting, a finite large arc capacity, compactness of real flows and the residual-cut proof. Ford–Fulkerson is credited. |
| `lem:v26-first-block` | `v26/capacity.tex` | Actual first-word evidences and independent edge tapes. Completion commands/reports marginalize to one. Product density records the exact common-event mass and each selected block's density ratio. |
| `thm:v26-separator` | `v26/capacity.tex` | Only M prediction vectors at a fixed visited set, arbitrary-centre affine recovery and the acquired-block subprobability. Apply the network-selection theorem on the subset lattice. The decoder is the original visited-set/label decoder, not a free-prefix decoder. |
| `cor:v26-profile-recovery` | `v26/capacity.tex` | Cuts with profile at least Q form a separator. The retained factorial Leja/Vandermonde comparison gives an explicit sufficient inequality for the lower-bound constant. |
| `prop:v26-dynamic` | `v26/phases.tex` | Induction on subset size and minimax predecessor identity; backtracking yields an order. Complexity is for supplied real cut costs. |
| `thm:v26-phases` | `v26/phases.tex` | Finite analytic contact orders, no cancellation in absolute determinant products, uniform bounded-error bit inversion, and finite affine arrangements. Includes fixed-order regret on an entire resolution interval. |
| `cor:v26-starphase` | `v26/phases.tex` | Exact comparison of the four partition types of the existing 24-trial detector experiment. Four phases, a nonconvex slope drop, and interval regret coefficient 1 versus endpoint coefficient 1/2. |

## Quantifier and scope audit

The infimum is always over one common controller. Coding seeds are independent of the acquisition tapes and are fixed only for a uniform bound that is subsequently integrated. The decoder's current-query randomness may be pre-sampled for the finite menu without supplying history-correlated storage. No trace-conditional product law is asserted. Every allocation retains the individual edge cap, and only positive determinant products enter an inverse. The graph size, local density constants, query-recovery norms and common-event mass remain explicit; no graph-size-uniform adaptivity gap is claimed.

The full companion entry point `companions.tex`, its original input files, and the historical derivation tree are retained. They are not new premises of the separator or phase proofs. This ledger is a navigation aid; the proofs are in the mathematical source, not deferred here.
