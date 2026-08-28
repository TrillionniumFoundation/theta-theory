# C71 C65 child × C69c H1 strata intersection — design audit v1

Status: **DESIGN FROZEN; EXECUTION AND PUBLICATION DISABLED; ZERO CREDIT**.

## Audited inputs and semantic boundary

- C69c corrected-result and its independent cold bundle close the source universe as
  `20,879 = 2,356 decisions + 18,523 blockers`, with two proof-only cover rows.
  C69c is a corrected descriptor authority for sealed zero-credit sidecar bytes, not
  an installed task/terminal authority. Its 2,356 rows are source-level candidate
  graphs and may not be retroactively called terminal.
- The C65 aggregate producer and dual-cold verifier schemas are now drafted, but the
  formal 64/64 aggregate, v2 self-test, post-publication replay and manifest are not
  frozen at this design capture. Therefore the skeleton contains an empty exact C65
  pin map. Its first test rejects before deriving a dependent ledger path or invoking
  a reader. A later pin-fill changes the skeleton SHA and requires review.
- C70-L remains an independent global obstruction: 744/1,042 edges and 971/1,044
  corridors are blocked; source seams are 0/16 ready. C71 neither reads nor overrides
  C70-L. Face/corner/source-grazing/multi-graph and large-component readiness remain
  explicit blockers.

## Exact join and child lineage

The only join is `C61_aggregate_leaf_row_sha256`. Every C65 aggregate child must join
exactly one C69c decision or blocker row from the complete 20,879-row source partition.
The child must also agree on pair index and 21-bit source path.

The child box is rebuilt from the C61 source box and the exact suffix of the C65 child
path. At each bit the widest exact rational coordinate among `(t,p,s)` is bisected at
its exact midpoint; first-axis tie break is `(t,p,s)`. The shared dyadic face owner is
the lower-bit child. Rebuilt payload must equal the C65 aggregate payload byte for byte,
and both the aggregate-row and original shard-row hashes remain bound.

C65 dispositions are not overwritten:

- `STRICT_TERMINAL` and `COLLISION3_READY` are carried with no H1 reclassification.
- Only `COLLISION2_HANDOFF` children under a C69c decision source are eligible for a
  local H1 recomputation.
- C69c blocker sources yield only fail-closed C71 blockers.

## Per-child independent 384-bit proof

C69c source certificates are references, never copied conclusions. For each eligible
child, the approved pinned Round185 kernel is invoked anew at 384 bits.

1. Evaluate `H1=n1_x^2-n1_y^2` over the **entire child box**. A strictly negative or
   positive interval proves a single local open slab.
2. Otherwise deterministically search graph axes. A graph is accepted only with a
   uniform strict full-box graph-axis derivative, opposite strict signs on both
   **complete relative faces**, and an interval-Newton image that is a strict interior
   self-map over every transverse parameter.
3. If one uniform self-map is unavailable, a finite transverse cover is permitted only
   when its exact boxes form a complete prefix-free Kraft-one partition and each cover
   member independently satisfies the same derivative/face/Newton conditions.
4. Center, corner, edge or endpoint samples alone never prove a slab or graph.

The local semantic partition is exactly `H1<0`, `H1=0`, `H1>0`. It is pairwise
disjoint and complete on the already half-open C65 child domain. The unique typed graph
carrier has zero full-dimensional Kraft weight. Owner composition is:

`C65 lower-bit shared-face owner → C71 negative half-open H1<=0 graph owner`.

Failure of any full-box condition remains a blocker; no fallback sampling or inferred
inheritance is allowed.

## Closed result boundary

Even a locally proved child reports `global_consumption_ready=false`. All C71 rows,
summaries and any future result lock `formal_credit=whole_parent_credit=D02_gate_credit=
terminal_disposition_credit=0`; candidate authority is false; runtime/canonical/seals
remain untouched. This successor is evidence for a later global consumer only.

## Static audit

- 8/8 pure static tests pass, including fail-before-reader with unfrozen C65 pins,
  longest-axis box replay, lower-bit owner recording, prefix-free rejection and exact
  source partition arithmetic.
- Python AST parses; there is no C69 producer/wrapper import and no filesystem write
  call. `--execute` unconditionally rejects. `--preflight` currently rejects before
  reading evidence. No formal run or publication was performed.
- Contract object: `6254452873fbc57e4dd5275e5e293e169d875bdb72a833713be8253527b21f97`.
- Closed-schemas object: `b15e7b0eb53490acefcac5837c83659196e81a6c68340433e29564d168c3b045`.
- Skeleton source SHA: `7368acd4437cc089157406649750d7117b08be978f492194d3ddc8332683a2cf`.

Required next action: after C65 aggregate + dual-cold + v2 self-test + replay + manifest
freeze, create a reviewed pin-filled successor version; run two isolated, byte-identical
zero-credit builds and a separate no-producer numerical verifier with coherent attacks.
