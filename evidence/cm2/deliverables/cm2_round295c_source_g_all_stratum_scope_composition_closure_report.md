# Round295-C Source-G all-stratum scope composition closure

## Outcome

Round295-C passes as the atomic composition of the sealed Round294,
Round295-A, and Round295-B scope.  It closes both outstanding bounded
frontiers without issuing any occurrence, seam, component, or DSU credit:

| frontier | before | after |
|---|---:|---:|
| Round291 physical-witness gaps | 576 | 0 |
| Round289 terminal-face gaps | 396 | 0 |
| composed all-stratum unresolved scope | — | 0 |

The output has two atomic tables: 9,528 canonical Round289 relation rows and
an eight-row all-stratum inventory.

## Fail-closed Round289 target normalization

Round295-B's field named `formal_Round294_occurrence_id` contains two
different kinds of value.  Round295-C does not copy that field as an
occurrence oracle.  It streams all 431,208 Round294 registry rows, independently
constructs the unique `source_row_id -> registry_occurrence_id` map, and
normalizes every one of the 11,448 physical child rows.

| normalization class | rows | unique targets |
|---|---:|---:|
| converted Round294 source-row IDs | 5,292 | 3,424 |
| already canonical registry-occurrence IDs | 6,156 | 356 |
| overlap between target sets | — | 0 |
| final canonical target universe | 11,448 | 3,780 |

All 3,780 normalized targets occur in the complete Round294 registry.  Their
prefix census is 3,728 `source-g-expanded-occurrence`, 32
`round182-collar-leaf`, and 20 `round179-resolved-child`.

The number 5,784 is not the Round295-C/B target count.  It belongs only to
the later Round296 combined strict-plus-B seam-endpoint universe.

## Canonical relation closure

There is exactly one output row for each Round289 relation:

| canonical disposition | relations |
|---|---:|
| whole physical | 8,844 |
| mixed physical and wrong-signed empty | 392 |
| wholly wrong-signed empty | 4 |
| graph-separated absence | 288 |
| total physical relations | 9,236 |
| total absent relations | 292 |

The relation rows reference all 11,448 normalized physical children, all 468
wrong-signed no-binding children, and all 288 graph-separated no-binding
children exactly once.  Every relation independently recomputes its rational
rectangle area and proves

```text
relation area = physical area + wrong-signed empty area + graph-separated area
```

with zero remaining relation scope.

The relation table contains 24 distinct Round268 patch IDs and 40 distinct
`(patch, side)` pairs.  Separately, the sealed Round295-B result records 152
directed endpoint cells and zero formal seam edges.  These are distinct
censuses: directed endpoint cells are not edges.  Only Round296 may pair and
promote the complete 152 true-seam edges.

## Eight-row all-stratum inventory

| slot | channel | rows/references |
|---:|---|---:|
| 1 | Round294 occurrence registry | 431,208 |
| 2 | representation bindings plus aliases | 46,564 = 46,288 + 276 |
| 3 | Round291 physical incidence | 113,452 rows / 225,304 refs |
| 4 | Round291 absence/no-binding | 28,016 |
| 5 | canonical Round289 relations | 9,528 |
| 6 | normalized Round289 physical incidence | 11,448 |
| 7 | Round289 wrong-signed absence | 468 |
| 8 | Round289 graph-separated absence | 288 |

The physical-incidence channel total is 124,900 and the no-binding evidence
channel total is 28,772.  These are bookkeeping sums only: the channels remain
provenance-distinct and are not merged as identities or occurrences.  Every
inventory row contains independently recomputed row-ID, row-hash, and full-row
commitments.

The 111,852 Round291 two-target incidence rows remain zero-credit incidence
evidence in Round295-C.  They may become candidate component-adjacency edges
only in a later all-stratum DSU after pair deduplication and subsumption
against already sealed ordinary/seam edges; they are never identity aliases.

## Independent verification and attacks

The verifier never imports or executes the Round295-C producer.  Before
opening either candidate file it independently:

1. byte-pins the sealed Round294, Round295-A, and Round295-B packages;
2. streams and recommits all 431,208 registry and 46,288 prior binding rows;
3. reconstructs the exact target-normalization function and census;
4. reconstructs all 9,528 relation rows and exact area equations; and
5. rebuilds all eight inventory rows and the deterministic candidate bytes.

Both verifier seeds pass with identical bytes.  All 36 attacks are rejected:
29 fully re-signed semantic mutations and seven duplicate/nonfinite/NUL JSON,
malformed GZIP, symlink, hardlink, and lexical path-traversal attacks.

## Artifact commitments

| artifact | SHA-256 |
|---|---|
| producer | `49331a2b311d659dc3ee10cdb3afbc8137af50e99238d93591f69f663f74f8a2` |
| ledger | `24000c3f370d2ec9805dd9ecf0ad1e4fdc63c1a380d194d056cac92e28bb98d2` |
| result | `4d14262636260c96af56f0f7d0f0147c8d93bb2261c92c2b6ce6bb2758d2f71f` |
| verifier | `aa332e5c279a8e71e89dcc53ce4cc27b13dcd02e5f8b741c244fdc539ac11ded` |
| verification | `4e37a5639fdc574d7a1d58e0dd3529780e379b17e39e2e48a2705bea1890a96c` |
| attack suite | `f767766fc080ccfb383b4943beff76b08b663b81bd1c9f650e57731441bcafe2` |

The embedded result, verification, and attack-suite commitments are,
respectively, `adb82bbacdf62d63c659921c4b4da7aaba35676c2cdf80f2e7ed06966c5d44a5`,
`2f17dfb41ae55b4475566a0568729ec420e24872ac72eb688891f4042864b8ab`,
and `b30747f1b4b528c95393bd5ef8f67ba73edd265f155affbb3fb4c7d3efc8cb07`.

## Strict nonpromotion

The registry remains 431,208 rows; the only representation delta relative to
Round294 is the already sealed 276 Round295-A aliases.  Round295-C gives zero
new-occurrence, seam-edge, component-union, DSU-rank, Jx/Jy, maximality,
fibre, and global-disposition credit.

The expanded-registry DSU is still `NOT_REBUILT`, the quotient count remains
null, and legacy 63,224 remains historical only.  Gate5 stays 10/18, D02 is
blocked, and CM2 remains no-go for claim.
