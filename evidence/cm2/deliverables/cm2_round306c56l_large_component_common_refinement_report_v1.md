# C56-L large-component exact common-refinement report v1

## Strict conclusion

`PASS_EXACT_1124_CELL_CORRIDOR_SEPARATOR_AND_1852352_KEY_REFINEMENT_LEDGER__FAIL_CLOSED_ZERO_WHOLE_CELL_CREDIT__EDGEWISE_MARGIN_OWNER_HISTORY_TRANSPORT_MISSING`

C56-L closes the inventory and crosswalk gap for the two 850-cell C55-B
components.  It does **not** close a dynamic continuation.  The exact current
answer is:

- 1,124 current-unresolved physical cells, paired by 562 C55-A blocker rows;
- 33,319 unique post-C53 logical C41 tasks, shared by the two reflected
  physical sides;
- 1,648 frozen C35 occurrences with their exact C36 margin-row bindings;
- 1,852,352 = 1,124 x 1,648 deterministic cell/occurrence refinement keys;
- 1,044 cells have an explicit shortest face/seam corridor in the
  current-unresolved induced atlas graph to a strict-open anchor;
- 80 cells form 22 exact separator islands (40 cells and 11 islands in each
  large component);
- formal `CONNECTED_TO_KNOWN` closures: 0;
- formal remaining cells in this scope: 1,124;
- formal credit and `D02_gate_credit`: 0.

The refinement keys are exact and exhaustive as a factorized crosswalk.  They
are not claimed to be a proved geometric/dynamic common refinement: C36 is
explicitly scoped to `DUAL_R139_SEED_COLLARS_ONLY`.  No producer is permitted
to promote atlas adjacency to known-sheet continuation without transporting
margin, owner, and history through every edge and every occurrence stratum.

## Exact component partition

Each large component has the same independently reconstructed census:

| component | unresolved cells | corridor cells | separator cells | islands | max corridor steps | refinement keys |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 562 | 522 | 40 | 11 | 118 | 926,176 |
| 1 | 562 | 522 | 40 | 11 | 118 | 926,176 |
| total | 1,124 | 1,044 | 80 | 22 | 118 | 1,852,352 |

The component-0 anchor is
`c32-compact-cell:a0f300f64940c475459c683f467a3757f056f62cf3cdc45aa7f673159b82aba1`.
The component-1 reflected anchor is
`c32-compact-cell:ffe621a305b922247f25f35540bb407facbdb3fcb1a1a77f9ac5cbf5ad72389a`.

Every corridor row contains its ordered exact face/seam steps, C55-B edge-row
hash, upstream row hash, face/seam identifier, dimension, gluing proof kind,
and exact geometry.  Every separator-island row contains the complete exact
cut ledger and its non-unresolved boundary-disposition census.

## Primary residual-class accounting

The counts below are for the two large components only.  “Tasks” are unique
logical post-C53 C41 rows, not doubled physical-side bindings.

| primary C55-A residual class | cells | corridor | island | tasks | refined keys | formally closed | remaining |
|---|---:|---:|---:|---:|---:|---:|---:|
| `C1_REGULAR_MULTI_GRAPH` | 516 | 500 | 16 | 14,404 | 850,368 | 0 | 516 |
| `COLLISION2_H2_FACTOR` | 212 | 194 | 18 | 7,246 | 349,376 | 0 | 212 |
| `H1_GRAPH_OR_BOUNDARY` | 104 | 72 | 32 | 3,077 | 171,392 | 0 | 104 |
| `COLLISION2_WALL_ENDPOINT` | 82 | 82 | 0 | 3,215 | 135,136 | 0 | 82 |
| `COLLISION2_POINT_WINNER_NONSTRICT` | 72 | 64 | 8 | 1,768 | 118,656 | 0 | 72 |
| `COLLISION2_ACTIVE_DELTA_1` | 68 | 68 | 0 | 3,529 | 112,064 | 0 | 68 |
| `ALGEBRAIC_H0_SEAM_RECHART` | 58 | 58 | 0 | 29 | 95,584 | 0 | 58 |
| `SOURCE_RADICAL_STEREOGRAPHIC_ENDPOINT` | 6 | 6 | 0 | 48 | 9,888 | 0 | 6 |
| `C1_OUTGOING_H1_FACTOR` | 6 | 0 | 6 | 3 | 9,888 | 0 | 6 |
| **total** | **1,124** | **1,044** | **80** | **33,319** | **1,852,352** | **0** | **1,124** |

The first line is the requested regular-multi-graph priority result: 500 of
516 physical cells have an exact atlas corridor, while 16 lie in separator
islands.  None receives whole-cell credit because the dynamic transport
premise is absent.

## Frozen downstream producer contracts

Corridor branch (1,044 cells):

1. consume the exact ordered C56-L corridor steps;
2. common-refine every step against all 1,648 C35 occurrence rows and their
   exact C36 margin bindings;
3. prove edgewise margin, absolute-owner, split-decision/history, chart/core,
   and half-open-face transport;
4. prove coverage and mutual exclusion for every child stratum;
5. only then evaluate whole-cell `CONNECTED_TO_KNOWN`.

Separator branch (80 cells / 22 islands):

1. consume the complete C56-L exact cut ledger;
2. resolve typed-event, formal-exclusion, source-grazing, and exterior sides
   with an independent strict event/exterior decider;
3. prove component adjacency/known-sheet anchoring or a terminal exterior
   class on every refined stratum;
4. do not infer disconnected exterior merely from atlas-graph isolation.

## Independent verification

The no-producer verifier independently reconstructed and checked:

- all 1,124 physical-cell witnesses;
- both shortest-path BFS trees and the maximum distance 118;
- all 22 separator components and their exact boundary cuts;
- all 33,319 C41 task bindings against the full frozen C41 routed ledger;
- all 1,852,352 refinement rows, including self-hash, order, C35/C36 binding,
  C36 collar scope, blocker class, and zero-credit locks;
- 16/16 coherent attacks fail-closed;
- C53 global head and canonical status bytes remained unchanged.

Independent status:

`PASS_INDEPENDENT_NO_PRODUCER_RECONSTRUCTION__1124_CELLS__22_ISLANDS__33319_TASKS__1852352_REFINEMENT_ROWS__16_OF_16_ATTACKS_FAIL_CLOSED__ZERO_CREDIT`

## Core hashes

- producer: `6533e7766378fd4f652cd8616470e60bedcd76f6ee40e292d2b355e45f55a338`
- result file: `99e5fc0019ae21e7bc68d0c2b997ed62e9c47b28fd47d366237b0c06b1d82601`
- result object: `0ab2c1ea9086db7f05d9b0c7f96d4348b0b2d8c9f54b47bd8e57aa570133a637`
- cell corridor/separator ledger: `3338a3fee7efe31bfae6b3abab77e3b3cc1c2a51fafb8e93d7a626c24803275d`
- separator-island ledger: `4e137710af14deffdd59ef9995825186c981b6a6a2ee4c24d4b8a05941dc1c00`
- post-C53 logical-task ledger: `6893e360b3ffc205147efa3786f1a05c1b67c1556e6195733549a7da5540fb6a`
- cell/occurrence refinement ledger: `af0b7af618b0a9db0a3e0e48285fe635610b76b2afdeeb8344c23b16e3f345d4`
- component summary ledger: `3f114177ac0c7527fc0398849710a73a53d069aac05415ef38d3b24192e3f608`
- independent verifier: `ff408d0a1b2ec9af31aa200ddb18f32881f74137249119d973b8b0bdbeaec645`
- independent verification file: `4a3d90843ee1401b32ef02af3eb5eb9ffdee773c4abeb0d096b9bcfe6e3ae6f2`
- independent verification object: `c793495f11962757a1e1ac55539ee7260d59d7e084662eb954a8a973466a70a5`

## Formal boundary

No runtime authority, pointer, seal, canonical file, or predecessor artefact
was written or changed.  The installed four-class census remains
`75,388 exclusions + 296 typed + 0 connected + 0 grazing/cemetery + 1,148 unresolved = 76,832`.
CM2 remains `NO-GO_FOR_CLAIM`.
