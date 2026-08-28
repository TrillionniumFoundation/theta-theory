# CM2 round306c56c B-side full per-origin projection report

Date: 2026-08-12 (CST)

## Verdict

C56-C closes the non-mathematical C55-C input blocker
`B_NO_INERT_76832_PER_ROW_PROJECTION_FOR_SECOND_FULL_RECONSTRUCTION`.
It materializes an inert, closed, ordered B-side projection for all 76,832
Source-W origins and an independent verifier reconstructs every row byte for
byte without importing or executing an upstream producer.

The mathematical result does not change:

```text
75,388 EARLIEST_PREFIX_EXCLUDED
   296 TYPED_EVENT_GRAPH
     0 CONNECTED_TO_KNOWN
     0 SOURCE_GRAZING_OR_CEMETERY
 1,148 UNRESOLVED_R1648_CONTINUATION
76,832 total

positive_terminal_enabled = false
formal_credit             = 0
D02_credit                = 0
```

## Projection

The ledger is ordered lexicographically by Source-W origin key.  Every row
binds the exact C32 physical chart/box, C33 row, optional C34 typed-event row,
C53 effective checkpoint, disposition or explicit unresolved reason, and its
own row hash.

All 1,724 ordinary rows additionally bind their C55-B cell and component rows,
complete sorted incident-glue hash list and sequence, reflection partner and
pair, current disposition, and known-sheet anchor role.  The 24 singleton
components also bind their corresponding C56s row.  The remaining 74,812
excluded and 296 typed rows retain their exact C33/C34 evidence.

```text
projection file       c5a79b946171ba5f60b6ef471aba5b8eb835547eb37e8019589ed06ada203a5c
row sequence          34ddd0ab69024cac1a9662833f4f641eb7ec5db26887108562c61413ac9aab21
result file/object    deeea5f7...17509 / 063a006d...d7ad6
```

## Independent audit

The independent verifier consumes the producer source only as inert AST and
bytes, reconstructs the same projection directly from C32/C33/C34, C53,
C55-B and C56s, and compares all 76,832 complete row objects.  It also runs
22/22 coherent semantic and filesystem/JSON attacks, including re-signed
checkpoint, credit, terminal, census, proof, component, singleton and glue
forgeries plus duplicate JSON, NaN, symlink, hardlink and TOCTOU rejection.

```text
producer source        44db2feea410f8c6b88cd71a916e2fb7abf12b432de515301a25f7a16ae8b29c
independent verifier   bb7c8d4b9b8111b64cd76829f2f9f76a2102f89b1e43a787ea90e1f3c1eb57a6
verification object    92f1ee5969ad43a016f5774aab1c1e428ac05aa34499d248e8b8fd271e9423b2
self-test object        caa51af60fd5a22cc6212528933c5747ccea21642f0816738c9c9b0698fb2ac4
```

C56-C creates no runtime, canonical, pointer, claim, receipt, authority or
seal writes.  The next blockers are mathematical: 1,124 cells in two anchored
components still lack whole-component common refinement, and 24 singleton
components lack the global whole-cell dynamic continuation/exterior decider.
