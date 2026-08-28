# C60-L static existing-edge owner/history query report v1

## Strict conclusion

`PASS_FULL_ACTIVE_UNIVERSE_INCIDENCE_1042_OF_1042__GEOMETRIC_OWNER_UNIQUE_911__OWNER_TIE_131__FAIL_CLOSED_HISTORY_COMPATIBILITY_0_OF_1042__ZERO_CREDIT`

C60-L implements the C59-defined no-producer
`STATIC_EXISTING_EDGE_TWO_ENDPOINT_OWNER_HISTORY_QUERY`.  It consumes all
1,042 frozen requests and supports canonical rationals, the exact
`-1/sqrt(2)` / `+1/sqrt(2)` source boundaries, and cross-chart seam entities.

Exact result:

- full active universe: 91,879 C41 rows / 183,758 physical occurrences;
- 183,700 rational and 58 algebraic-boundary occurrences;
- 1,042/1,042 edges have complete two-sided incidence and complete endpoint
  cell coverage;
- 13,103 exact positive-length incidence atoms;
- geometric owner unique under the frozen C50a rule: 911 edges;
- geometric owner nonunique under that same rule: 131 edges;
- occurrence-1 owner/history-compatible overall PASS: 0;
- overall fail-closed: 1,042;
- formal and D02 credit: 0.

## Full-universe incidence

For every C41 ambient row the implementation reconstructs both physical
occurrences directly from the C41 exact box, falling back to the pinned C32
exact cell envelope only for the 29 two-sided algebraic rows.  It indexes the
four exact box faces by chart, axis and exact rational/algebraic coordinate.

Each intra-chart C59 face is atomized at every active-universe incidence
breakpoint.  Each source seam is atomized after applying its frozen two-chart
contact definition and physical-p span.  Exact comparisons with
`±1/sqrt(2)` are made by sign and a rational-square comparison against `1/2`;
no floating-point approximation is used.

Every one of the 13,103 atoms has exactly two incident active occurrences and
the incident cells are exactly the two requested endpoint cells.

## Frozen owner rule and the 131 ties

The owner rule is unchanged:

`UNIQUE_LEXICOGRAPHIC_MINIMUM_SEMANTIC_PATH`

Under this rule, 911 edges have a unique owner on every atom.  The other 131
edges contain 345 atoms on which the two incident occurrences have the same
minimum semantic path; every such tie has exactly two winners.  These split
as 115 intra-chart faces and all 16 source seams.

This is nonuniqueness of the frozen rule itself on the reconstructed static
edge incidence set.  C60-L does not add a side, pair, physical-ID or history
tie-break.  A future rule change would require an explicitly versioned,
mathematically justified occurrence-aware owner rule and independent audit;
it cannot be inferred from C50a pair1.

## Why overall history compatibility remains zero

C60-L verifies that each request binds the exact C35 occurrence-1 projection
and that both endpoint C38-C41 lineage sequence roots are present and closed.
Those facts do not supply either missing semantic relation:

1. edge atom -> C35 occurrence-1 semantic identity;
2. endpoint C38-C41 lineage row -> edge-atom incidence identity.

Without those maps, geometric incidence and owner uniqueness cannot prove
that both endpoint histories transport the same occurrence-1 continuation.
Therefore all 1,042 overall decisions remain fail-closed, including the 911
geometrically owner-unique edges.

## Required next

Two independent obligations remain:

1. materialize the edge-atom to occurrence-1 and endpoint-lineage semantic
   crosswalks, then replay all 1,042 requests;
2. for the 131 tied edges, either show the tied histories are disjoint under
   that crosswalk or freeze and independently justify a new occurrence-aware
   owner rule.  No arbitrary tie-break is legal.

## Independent verification

`PASS_INDEPENDENT_FULL_UNIVERSE_183758_OCCURRENCES__13103_ATOMS__1042_COMPLETE__911_UNIQUE__131_FROZEN_RULE_TIES__0_HISTORY_PASS__20_OF_20_ATTACKS__ZERO_CREDIT`

The independent verifier imported or executed no C60 producer.  It rebuilt
all 76,832 C32 cells, 91,879 C41 ambient rows, 183,758 physical occurrences,
1,042 request atomizations, 13,103 atom rows, and 1,042 decisions.  It
confirmed the unchanged owner rule, rejected any arbitrary tie-break, passed
20/20 coherent reclosed attacks, and reproduced identical verification bytes
on two full runs.  C53 and canonical snapshots remained unchanged.

## Core hashes

- query implementation: `48a3dc7ac7d3edd5fe951f81fcbb4e60e44e5a263939792cd28385dac9191296`
- incidence-atom ledger: `4b2cd8115221cbc9b58bda8ec450b2d0415bbfaf7baac5127837dd24b7a85ac6`
- edge-decision ledger: `63996a66fe80ca982a0ecd4c9ec5e6025c39078a58e5b1f9aff5516dc5c046f8`
- result file: `c7e0b66dca03fd155428b6f81e26cf53e4f6f917ae4bf28a87dcab4004012315`
- result object: `9548a0687e5fd74d9964e4d98275b0fde39029765e823379b5f87032d2663568`
- independent verifier: `2350c615f6e027084d3e859010fa36547d128e0f716dfb1ba5a9eee4985358c6`
- independent verification file: `1bf82a5d099698e3dec8532780f9bca4e1489db8a4aa7853984a4a3dd6d2ee0e`
- independent verification object: `c5da39d3aca3d6d07aad91c56e56df74d56b0a0099434b5d4e15a7a49da526a7`

## Formal boundary

No C50a producer was called or modified.  No runtime authority, pointer,
claim, seal, canonical file, predecessor or old deliverable was written or
changed.  C53 remains `f62483c8...6aeeb3`, canonical remains
`922fc5d0...b99b57`, D02 remains blocked, and CM2 remains
`NO-GO_FOR_CLAIM`.
