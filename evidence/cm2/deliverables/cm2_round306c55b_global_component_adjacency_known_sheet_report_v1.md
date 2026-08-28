# C55-B global component adjacency and known-sheet anchor report

## Verdict

`PASS_RECONSTRUCTED_COMPONENT_ADJACENCY_AND_TWO_STRICT_OPEN_KNOWN_SHEET_COLLARS__FAIL_CLOSED_1148_CURRENT_UNRESOLVED_CELLS`

C55-B reconstructs the compact-atlas component graph and binds it to the
installed C53 `GLOBAL_COMPOSITE` head.  It does **not** prove global closure.
The two known connected objects are strict open collars inside two 850-cell
components, not proofs that either whole component is connected to the known
sheet.  Component isolation, reflection pairing, coordinate equality, and
origin-key equality receive no terminal credit.

## Frozen authority binding

- C53 global-head file SHA-256:
  `f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3`
- C53 global-head object SHA-256:
  `cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb`
- Effective checkpoint:
  `b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab`
- C55p0 closed-row input contract file SHA-256:
  `0e2a7b713f3c4c007c65a27a42079ca33b024b8489b5dfd149312fcd5702333b`

The ledger also pins C29/C30, C32--C37, C42, Round101, Round102, Round140,
and the C34--C37 independent audits.  C29 is retained as Source-G provenance;
C30/C33 provide Source-W disposition provenance; Round101/102 are scoped
grazing/face-quotient precedents; Round140 supplies only one positive-area
open connected collar and C37 transports it by the exact `Jy` involution.

## Exact reconstruction

The producer and verifier independently consume upstream results and ledgers
as inert bytes.  Neither imports or executes an upstream producer.

- Source-W universe: 76,832 rows.
- C33 formal split: 74,812 excluded and 2,020 resolved nonexcluded.
- C34 live split: 296 typed-event cells and 1,724 ordinary cells.
- Ordinary graph: 3,248 internal intra-chart faces and 28 internal explicit
  source-chart transitions.
- Ordinary components: 26, with size census `850 x 2 + 1 x 24`.
- C37 quotient: 862 ordinary-cell reflection pairs and 13 component pairs.
- Exact component/glue ledger: 5,358 rows, including all 1,024 C32 grazing
  faces, all eight grazing/seam corners, all 336 inherited event faces, and
  every face or seam touching an ordinary cell.
- Current C53 projection: 576 ordinary cells formally excluded and 1,148
  ordinary cells unresolved.

Every cell row carries the exact physical chart, `t/p` box, C32/C33 row pins,
C34 component, C37 reflection partner, C42 parent row, C53 projection, current
disposition, and a self-hash.  Every component row carries explicit sorted
membership, edge/glue row references, anchor path or missing-anchor reason,
current formal partition, and a self-hash.

## Known-sheet anchors and unresolved partition

Exactly two components contain a certified strict open connected collar:

1. the Round140 adaptive open cell inside the C34 seed coarse cell;
2. its exact C37 `Jy`-reflected open collar.

Both anchors are strict subsets, so whole-component connected credit is zero.
The current 1,148 unresolved cells partition exactly and disjointly as:

- `ANCHORED_COMPONENT_WITHOUT_WHOLE_COMMON_REFINEMENT`:
  2 components / 1,124 current unresolved cells;
- `UNANCHORED_SINGLETON_WITHOUT_COMPLETE_EVENT_EXTERIOR_CLOSURE`:
  24 components / 24 current unresolved cells.

All 24 singleton components remain unresolved.  Their isolation after typed
event removal does not prove cemetery or disconnected exterior status.

## Independent audit

- Producer source SHA-256:
  `9cbc390cf4311338a36495b0433bdcccb426a80814787a3ca8d039f1bbcb45f6`
- Result file SHA-256:
  `6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93`
- Result object SHA-256:
  `1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56`
- Independent verifier source SHA-256:
  `82d687987879a963751b8fbf2a2344e0d31b47011d0afd2c407e858f088bf90a`
- Independent verification file SHA-256:
  `42f31f0c158b08651bec97d83d6980f0372353e71cb4f59959f186a329601bae`
- Independent verification object SHA-256:
  `350f076a3dcfaa4424bfb27f2730e876d0f6159baa033c7aafbfaded8c870a68`
- Coherent hostile tests: 16/16 fail closed.

The verifier independently rebuilds membership and connectivity from emitted
explicit face/seam rows, re-correlates all 862 C37/C42/C53 projections,
validates closed schemas and self-hashes, and rechecks the C53 head before and
after.  Runtime writes performed: zero.

## Strict boundary and next requirement

- `global_closure_proved=false`
- `unresolved_zero=false`
- `strict_decider_eligible=false`
- formal credit and `D02_gate_credit`: zero
- CM2 remains `NO-GO_FOR_CLAIM`

The remaining proof obligation is a whole-cell common refinement of all 1,148
current unresolved cells against the complete four-chart R1648 continuation
atlas, with explicit face/corner/source-grazing glue and either a whole-cell
known-sheet anchor or a complete event/exterior disposition proof.  Only an
independent no-producer reconstruction with `unresolved=0` may enable the
global strict decider.
