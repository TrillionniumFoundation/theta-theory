# CM2 Round306 C43B0 five-sole-deficit formal closure contract and independent-audit design v1

Date: 2026-08-11 (Asia/Shanghai)

## Scope and authority boundary

This is a read-only design audit. It creates no runtime object, receipt, token,
seal, pointer, or D02 credit. It does not promote C43B0.

The installed input authority is C42 f1:

- candidate token `c42-p391-formal-producer-20260811T044500Z-f1`;
- candidate object `a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2`;
- independent-audit token `c42-independent-audit-20260811T052900Z-p391-f1`;
- independent-audit object `85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c`;
- authority-seal object `b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460`;
- installation-receipt object `c5f2eb78a0d9d717326bc57fb14df823ab3c5181e3e613a0327425c5e33e784e`.

The formal baseline is therefore 574 paired coarse cells terminal, 287 of 862
representatives whole, 1,150 unresolved paired continuations, and 575
representatives remaining. C43B0 must bind the installed C42 pointers, seal,
receipt, candidate, audit, and the C41 lineage beneath them. A candidate built
against C42 f2 or a pre-install review directory is invalid even if payload bytes
happen to match.

The read-only inputs reviewed here are:

- `cm2_round306c43b0_d02_zero_surface_shard_planner_v1.py`, SHA-256
  `a7c22208b859979ee4cc9ccd460865d0fee517d2348ca3d59322cc5da90f0522`;
- `cm2_round306c43b0_d02_sole_deficit_adaptive_pilot_v1.py`, SHA-256
  `00c03e5a9f869a917649d49137f2aece69357e0e9a073e59f9e2d990b0365609`;
- the installed C41/C42 ledgers and the C39/C40/Round185 routing sources.

## What the pilot establishes, and what it does not

A fresh read-only pilot at adaptive depth 3 and 15 routes per pair returned
object `be681c7d...ad656`. It evaluated 23 exact routes, made 9 exact dyadic
splits, and produced 14 terminal representative leaves with relative Kraft sum
1 for every source. It produced no checkpoint and no collision-3-ready leaf.

| pair | C41 residual path | terminal suffixes | leaf count | deepest added depth | split census | observed strict route |
|---:|---|---|---:|---:|---|---|
| 97 | `111111111` | `0,10,11` | 3 | 2 | `p:1,t:1` | C2 absolute-owner mismatch, selected `G[1,0]` |
| 211 | `111111111` | `0,10,11` | 3 | 2 | `p:1,t:1` | C2 absolute-owner mismatch, selected `G[1,0]` |
| 592 | `000000000` | `0,1` | 2 | 1 | `p:1` | C1 official-word mismatch |
| 664 | `010101010` | `0,100,101,11` | 4 | 3 | `p:2,t:1` | C1 official-word mismatch |
| 715 | `101010101` | `0,1` | 2 | 1 | `t:1` | C1 official-word mismatch |

The observed C1 mismatch witness for pair 592 is
`gate5-word:431440:3e449d100d596d6c2ae507a7808071e800eb9a6e7a22a6e32edbc572ac74bae7`.
Pairs 664 and 715 use
`gate5-word:375295:fd379e90338a3c2065c81d708ca28afe51ff86cbb9df6c606e7758eb2ace0015`.
For the C2 leaves, the currently exposed official key has ordinal 290575,
word-key id
`gate5-word:290575:5e5950ce63693dc08790f017f8e5cc79eb8aa776ff4c53c10a60b27a161178b2`,
and row SHA-256
`5e5950ce63693dc08790f017f8e5cc79eb8aa776ff4c53c10a60b27a161178b2`.

This is strong feasibility evidence, but it is not a formal closure. In
particular, the pilot stores only the routed classification/witness and sparse
C2 data. C41 terminal ambient rows likewise do not materialize the complete C1
candidate proof, complete C2 candidate census, closed-face restrictions, global
incidence owners, or reflected proof. A formal producer must recompute and
materialize those objects; it may not promote the pilot JSON or infer a theorem
from the class-name prefix `EXCLUDED_`.

## Safe target discovery and generalization

The producer must derive the tranche, then assert its observed identity. It must
not begin from a hard-coded five-element allow-list.

1. Capture the installed C42 authority transaction by descriptor-bound stable
   reads.
2. Rebuild the C43B0 planner census from C42/C41.
3. Select exactly the representatives satisfying all of:
   `zero-surface B0`, `whole-pair-gain`, `pair_b0_task_count == 1`, and not the
   already-closed C42 pair 391.
4. Require that the derived sorted set is exactly `{97,211,592,664,715}`.
5. Derive each unique C41 residual row, path, exact box, row hash, ambient-leaf
   identity, and parent fraction from the installed ledgers. The pilot constants
   are regression guards, not sources of truth.

Adaptive traversal must be semantic, not budget-defined:

- use the pinned Round166 longest-axis rule, exact rational bisection, and pinned
  tie order;
- stop only at a proved terminal exclusion or a fully materialized
  collision-3-ready handoff;
- for this formal tranche, require every leaf to be terminal excluded and require
  zero checkpoint and zero collision-3-ready leaves;
- treat maximum depth and route count only as post-termination assertions. If a
  budget is hit before semantic termination, fail closed and publish nothing;
- derive leaf paths, classes, and counts from a fresh traversal, then assert the
  observed profile of 14 leaves and 9 splits. Expected paths must never steer the
  traversal.

## Mathematical certificate obligations

### C1 official-word mismatch leaves

Each of the eight representative C1 leaves (2 for pair 592, 4 for pair 664,
2 for pair 715) needs one certificate over the entire closed leaf box. At
minimum it must materialize:

1. the exact C38/C39 source binding, reconstructed box, active-target universe,
   and ordered collision-one candidate records;
2. a unique first collision-one owner equal to the frozen owner, with every
   competing root disposition and every strict comparison/margin;
3. the H1 enclosure, proof that `0` is excluded from H1 on the closed box, the
   selected strict side, and outgoing chart `W`;
4. existence of the outgoing state and all data used by translation-normalized
   official-word construction;
5. the calculated official word row, ordinal, canonical row hash and word-key id,
   plus the expected C42 lineage word-key id;
6. a literal inequality of those canonical word-key ids, with both operands
   bound by hash;
7. root-order, discriminant, homogeneity, wall, endpoint and seam evidence proving
   that the word construction is defined and constant on the entire closed box.

The current `stage_two_route` return tuple is insufficient by itself: it exposes
only the final word id and collision number. The formal producer must expose the
underlying closed-box certificate. If any face contains H1=0, a root-order tie,
an undefined outgoing state, or an official-word seam, the ambient leaf is not
closed by its interior mismatch; that face remains zero-credit until separately
owned and certified.

### C2 absolute-owner mismatch leaves

Each of the six representative C2 leaves (3 each for pairs 97 and 211) needs one
certificate over the entire closed leaf box. At minimum it must materialize:

1. the complete collision-one state and proof that the C2 geometry is defined;
2. the ordered 55-candidate C2 universe, each candidate disposition, and an exact
   census whose sum is 55;
3. the unique selected absolute C2 owner and the strict root-order/margin data
   making that selection uniform on the closed box;
4. both allowed expected owners derived from the original/reflected C42 lineage,
   and the proof that selected `G[1,0]` is neither allowed owner;
5. outgoing chart, official key, near-root interval, axis-endpoint certificates,
   clean-wall record, and all surface-error fields;
6. explicit statements that no unresolved discriminant/root-sign candidate and
   no unowned wall, face or corner was hidden by the owner-mismatch return.

As in C42, `selected_owner not in expected_by_owner` is only the last logical
step. The certificate must first prove that the selected owner is unique and
constant on the entire closed box and that the expected-owner table is the exact
installed lineage table.

## Required artifact contract

All JSONL ledgers must use canonical JSON, deterministic sort keys, per-row
semantic SHA-256 values, gzip with pinned headers, and descriptor-bound
pre/post stable reads. Row counts below are exact where the pilot fixes the
combinatorics; global-incidence counts must be derived rather than guessed.

### 1. `exact_sources.jsonl.gz` — exactly 5 rows

One row per derived pair, sorted by pair index. Each row binds:

- C42 pointer bytes and hashes, candidate/audit tokens and objects, authority
  seal, installation receipt, C41 candidate/audit/receipt/manifest, and all
  producer source hashes;
- C42's 862-parent row for the pair and its row hash;
- the exact C41 ambient residual row and all C41 boundary/C2/outgoing-H1 outer
  rows that name it;
- the C38/C39 source identity, exact box, residual path, source fraction
  `1/512`, and zero prior C34 credit for this remainder;
- the proof that there is exactly one residual descendant for this parent after
  C42.

### 2. `adaptive_splits.jsonl.gz` — exactly 9 rows

One row per deterministic split. It records the parent path/box/fraction, split
axis, exact midpoint, child paths/boxes/fractions, half-open ownership rule,
source-row hash, and child route-row hashes. It also binds the longest-axis and
tie-rule calculation. Child union, disjoint half-open interiors, closed-cover
equality, and exact fraction conservation are required row invariants.

### 3. `closed_leaf_certificates.jsonl.gz` — exactly 28 rows

Use a single canonical order `(pair_index, orientation, path)`: 14 representative
closed leaves and 14 explicitly materialized reflected closed leaves. Every row
contains the full C1 or C2 certificate described above, not merely a class name.
It also contains the source fraction and relative leaf fraction; the absolute
fractions for each orientation must sum to `1/512`.

### 4. `reflection_transport.jsonl.gz` — exactly 14 rows

One row per representative leaf, paired with exactly one reflected leaf. Each
row must materialize the exact Jy map, reflected parent/cell/source identities,
endpoint-order convention, path transport, chart/owner/word transformations,
and hashes of both full certificates. Reflection must be recomputed; copying the
representative class name or using a label-only symmetry assertion is forbidden.

### 5. `internal_strata_incidence.jsonl.gz` — derived complete census

There are exactly 9 representative split interfaces and 9 reflected split
interfaces before exact physical-key deduplication. For every interface, record
the exact segment, all terminal descendant leaves incident to it, the lower-bit
owner, direct closed-face restriction proofs, and both endpoints. Enumerate and
deduplicate all vertices created where split interfaces meet source sides or
other split interfaces. Each vertex needs its complete incident-leaf list,
canonical owner, and direct point recomputation.

This ledger may use one row per split interface plus embedded endpoint rows, or
separate face/vertex ledgers. In either representation, its derived census and a
Merkle-style ordered row-hash sequence must be reported. Nine split rows alone
are not a lower-strata proof.

### 6. `source_face_owner_incidence.jsonl.gz` — exactly 20 source-side slots

Each of the five representative source rectangles contributes four exterior
side obligations. A row may pair the representative side with its reflected
side, following the C42 convention, but both restrictions must be explicit.
For every exact face key:

- enumerate all globally incident C41 ambient cells plus the C42 and C43 deltas;
- directly recompute the closed-face restriction;
- choose the canonical owner by the pinned global owner rule;
- prove every incident cell needed by the owner decision is terminal after the
  C43 delta.

Physical-key deduplication may reduce the number of unique geometric faces, but
it must not reduce the 20 source-side obligations or silently drop an incidence.
If an adjacent ambient cell remains residual and owns a required face, the
corresponding representative parent cannot receive whole-cell credit.

### 7. `source_corner_owner_incidence.jsonl.gz` — exactly 20 source-corner slots

Apply the same rule to four corners for each of five sources, with explicit
reflected point restrictions. Rebuild the global incident census and directly
evaluate every point. Interior split vertices belong in the internal-strata
ledger; source corners belong here. Hash-only references to a face row are not a
point proof.

### 8. `representative_parent_conservation.jsonl.gz` — exactly 862 rows

Rebuild all 862 rows from the installed C42 baseline. Do not publish a five-row
delta ledger alone.

- The 857 unaffected rows must be semantically identical to C42 and must bind
  the exact C42 row hash.
- Each target row starts with C42 terminal fraction `511/512`, adds an exact
  representative gain `1/512`, finishes at terminal fraction `1`, unresolved
  fraction `0`, and materializes both representative and reflected closures.
- Relative Kraft for each target source is exactly 1 and absolute Kraft is
  exactly `1/512`; the paired C34 common credit is exactly 2.
- C42 pair 391 must remain unchanged. Any mutation of its row is fatal.

### 9. `round144_census.json` and strict nonpromotion lock

If and only if every obligation above passes, the exact proposed delta is:

| quantity | installed C42 | formal C43B0 result |
|---|---:|---:|
| whole representatives | 287 | 292 |
| remaining representatives | 575 | 570 |
| paired coarse cells terminal | 574 | 584 |
| earliest-prefix excluded | 75,386 | 75,396 |
| typed-event graph | 296 | 296 |
| unresolved | 1,150 | 1,140 |
| total | 76,832 | 76,832 |

The result must still say `unresolved_zero=false`, `D02=BLOCKED_BY_1140_...`,
`D03=UNAUTHORIZED`, `D04=NOT_MINTED`, `Gate5=10/18`, and
`CM2=NO-GO_FOR_CLAIM`. The producer must set
`producer_output_is_authority=false` and `authority_pointer_installed=false`.

### 10. Manifest, result, execution receipt and no-authority guarantee

The candidate directory must contain a complete root manifest, its companion
hash, canonical result object/self-hash, strict nonpromotion lock, and a
descriptor-bound execution receipt. The producer must refuse to run if any C43
pointer already exists and must never install one. Publication to a candidate
directory uses no-replace semantics, fsyncs all files and directories, and
records the invocation identity. Independent audit is a later, separately
published object.

## Independent auditor contract

The auditor must be a separate source file and must not import the C43 producer.
It may reuse lower-level frozen mathematical primitives only after pinning their
source hashes. Its acceptance sequence is:

1. open and retain file descriptors for installed C42 pointers/seal/receipt,
   candidate files, and all lineage files; perform stable pre/post reads;
2. independently rebuild the five-pair target discovery from C41/C42;
3. independently reconstruct every source row and source fraction;
4. independently run the semantic adaptive traversal, preferably in two fresh
   processes with different scheduling/seeds, and require identical canonical
   trees and bytes;
5. recompute all 28 closed leaf proofs from the exact boxes, including ordered
   candidate universes, strict margins, owner/word evidence, and reflected boxes;
6. independently enumerate internal split strata, all global face incidences,
   all global point incidences, and their owners against the complete 91,879-row
   C41 ambient-leaf ledger plus installed C42 and candidate C43 deltas;
7. rebuild all 862 conservation rows and the 76,832 census without trusting
   candidate aggregates;
8. verify manifest, gzip/container bytes, row sequences, object self-hashes,
   execution receipt, no-authority fields, and absence of C43 pointers;
9. perform cold replay and terminal byte replay after coherent attacks;
10. stable-read every captured authority input again before publishing an
    audit-only object.

The auditor must reject a candidate if it can prove only the open interiors.
Closed leaf, internal split face, source face, point, reflection, global owner,
Kraft, and parent-census claims are a single conjunctive transaction.

## Minimum coherent attack suite

At least the following 54 mutations should each be applied to a fully
self-consistent copied candidate with downstream hashes/manifests recomputed.
Every attack must fail closed for the intended semantic reason, not merely due
to a stale checksum.

1. Replace installed C42 f1 token with f2.
2. Change the C42 candidate object pin.
3. Change the C42 audit object pin.
4. Change the C42 authority-seal object pin.
5. Change the C42 installation-receipt object pin.
6. Replace a C41 parent row with another pair's row.
7. Add pair 391 to the target tranche.
8. Remove pair 97 from the target tranche.
9. Replace one target with a non-sole-deficit pair.
10. Change a derived C41 residual path.
11. Change a source fraction from `1/512`.
12. Duplicate one exact-source row.
13. Change a split axis.
14. Change a split midpoint by one rational unit.
15. Swap the two child paths.
16. Change the lower-bit half-open owner.
17. Make child boxes overlap.
18. Leave a gap between child boxes.
19. Change one child fraction while preserving the displayed aggregate.
20. Drop one split row.
21. Duplicate one terminal leaf.
22. Remove one terminal leaf.
23. Introduce a prefix-overlapping leaf path.
24. Reorder leaves against the canonical order.
25. Forge relative Kraft as 1 after changing a depth.
26. Change a C1 leaf to the C2 exclusion class.
27. Change a C2 leaf to the C1 exclusion class.
28. Change a C1 official word id.
29. Change a C1 official-word ordinal or row hash.
30. Change the expected C1 lineage word id.
31. Remove the C1 H1 nonzero proof.
32. Make a C1 H1 enclosure contain zero.
33. Remove a C1 root-order or outgoing-state proof.
34. Change the selected C2 owner from `G[1,0]`.
35. Insert `G[1,0]` into the expected-owner table.
36. Change a C2 candidate id or candidate order.
37. Change the C2 candidate census total from 55.
38. Make one C2 strict margin contain zero.
39. Remove a C2 endpoint or clean-wall certificate.
40. Mark an unresolved discriminant candidate as no-real.
41. Drop one representative closed leaf but retain its reflected leaf.
42. Change the Jy-reflected box endpoint order.
43. Change a reflected owner/word/chart transform.
44. Point a transport row at the wrong representative leaf.
45. Drop one internal split interface.
46. Assign an internal interface to the upper-bit child.
47. Remove one incident descendant from an internal interface.
48. Drop one source exterior face.
49. Omit a globally incident ambient cell from a face row.
50. Change a global face owner.
51. Drop one source corner or internal vertex.
52. Omit a globally incident cell from a point row.
53. Replace a direct point proof with a face-row hash reference.
54. Grant whole-parent credit while one face/point owner remains residual.

The production suite should additionally mutate pair 391, drift one of the 857
unchanged parent rows, omit/reorder an 862-parent row, report unresolved 1,139 or
1,141, mark `unresolved_zero=true`, mark D02 PASS, set producer authority true,
install a pointer, corrupt a gzip header, swap a manifest member, alter the
execution receipt, perform an fd/TOCTOU replacement, and force cold-replay byte
divergence.

## Strict conclusion

The five-pair tranche is a plausible short formal closure: the current exact
router finds a finite 14-leaf all-terminal cover with exact Kraft conservation.
The remaining risk is not route discovery. It is proof materialization and
lower-strata ownership. The formal C43B0 producer is acceptable only if it proves
closed boxes, every internal and exterior face, every required point, the full
Jy-reflected cover, global incidence ownership, all 862 parent rows, and the
76,832 census in one fail-closed candidate transaction. Until an independent
auditor passes that transaction and a later authority installer commits it, the
installed formal count remains C42's 574 paired / 1,150 unresolved.
