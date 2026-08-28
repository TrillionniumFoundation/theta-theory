# Round214 source-G physical component join/dedup feasibility spike

## Verdict

`BOUNDED_DUPLICATE_INCIDENCE_QUOTIENT__PHYSICAL_COMPONENT_JOIN_INCOMPLETE__ZERO_PROMOTION`

Round211's 17,716 sheet, 20,456 curve-incidence, and 40,912
endpoint-incidence rows admit a nontrivial **same-occurrence exact
duplicate-incidence quotient**.  They do **not** yet admit a defensible full
physical-component quotient.

The safe quotient uses only:

1. the same frozen occurrence and parent;
2. the same active factor, owner, target lift, wall word, roof, and signature
   core;
3. an exact shared `t`-face rectangle carrying the same explicit curve
   incidence; or
4. an exact endpoint carrier already materialized by the `t±` curve rows.

It never joins rows merely because boxes touch or signature cores match.
Strict Arb zero witnesses on `p/s` faces are reported only as
nonpromotional feasibility evidence because Round208/Round211 do not
materialize `p/s` internal-face incidence IDs.  Exact carriers spanning two
different occurrences are also left unmerged because there is no explicit
cross-occurrence common-refinement/glue row.

No whole-leaf, whole-origin, whole-tube, global-component, or exact-key
disposition credit is issued.

## Artifacts and reproducibility

- Probe:
  `cm2_round214_source_g_physical_component_join_dedup_feasibility_probe.py`
  - SHA256:
    `d074aa045637ce1bb31768fa551bdb73ceda6a58c760cafe3dbf92faa7c922fe`
- Canonical stdout document SHA256:
  `9a90e2f01cf03b263803298ba1977c9ecfa6e70778698ea13e28a7fdcbc071d7`
- Result SHA256:
  `ddc12c8e625a5a65cc8e445d97ee89e64429a6c729efe32778a092f7e6521d09`
- Canonical stdout size: `156,006` bytes
- `PYTHONHASHSEED=214051`: exit `0`
- `PYTHONHASHSEED=214052`: exit `0`
- The two stdout byte streams are identical.
- Arb precision: 256 bits.

The probe pins and checks:

- Round211 source:
  `9e8874672150d7585316524a7724070f4543e231de5481d1c1dfbd00ddc65a02`
- Round211 certificate:
  `bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f`
- Round211 result:
  `3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b`
- Round209 probe:
  `dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f`
- Round186 factor evaluator:
  `5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64`
- Round208 certificate:
  `4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938`
- Round204 certificate:
  `e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818`

Every formal Round211 row is joined back to its pinned Round209 probe row ID
and row hash before any census is performed.  The Round211 producer is not
imported or executed.

## Safe duplicate-incidence quotient

These are quotient **blocks**, not claimed physical components.

| dimension | input incidences | safe blocks | safe reductions | block-size histogram |
|---|---:|---:|---:|---|
| 2D sheet | 17,716 | 12,156 | 5,560 | `1:7600, 2:4104, 3:152, 4:284, 5:12, 64:4` |
| 1D curve | 20,456 | 14,680 | 5,776 | `1:9812, 2:4496, 3:84, 4:276, 5:8, 64:4` |
| 0D endpoint | 40,912 | 30,876 | 10,036 | `1:21472, 2:9052, 3:72, 4:280` |

Membership hashes:

- sheet blocks:
  `7a679aca24e025463e0739485e2b0b5f6b4b11746d343f91b0743060623f56f8`
- curve blocks:
  `388cf14fb2103fe8149411fb37de9ee0be7618c73831e22d805d87f7cd74f891`
- endpoint blocks:
  `e810a52cd88248490d60ebc0f6715a87c7aed78bfd816c765fd905e7dbf19cc5`

The safe graph contains 4,260 explicit same-occurrence exact `t`-face curve
duplicate joins.

For comparison, ignoring the occurrence boundary would produce:

- 13,492 exact curve carriers:
  - multiplicity 1: 6,528
  - multiplicity 2: 6,964
  - cross-occurrence carriers: 2,704
- 22,320 exact endpoint carriers:
  - multiplicity 1: 9,532
  - multiplicity 2: 9,788
  - multiplicity 3: 196
  - multiplicity 4: 2,804
  - cross-occurrence carriers: 6,684

Those cross-occurrence carriers are evidence for the next glue construction,
not permission to merge now.

## Face-contact census

There are 15,540 positive-area compatible face contacts:

| axis/contact | same occurrence | cross origin/occurrence | total |
|---|---:|---:|---:|
| exact `t` face | 4,260 | 2,704 | 6,964 |
| partial `t` face | 0 | 320 | 320 |
| exact `p` face | 0 | 5,840 | 5,840 |
| partial `p` face | 0 | 324 | 324 |
| exact `s` face | 2,080 | 12 | 2,092 |
| **total** | **6,340** | **9,200** | **15,540** |

Only the 4,260 exact same-occurrence `t`-face joins have all required explicit
incidence data in the present boundary.

The nonpromotional feasibility split is:

- 4,260 safe explicit same-occurrence `t`-face duplicates;
- 2,704 cross-occurrence exact curve-carrier candidates;
- 4,648 strict Arb active-factor zero witnesses;
- 3,664 exact endpoint-carrier candidates outside the safe occurrence
  quotient;
- 264 unresolved partial positive-area contacts.

The 644 partial positive-area contacts split exactly as:

- 300 strict zero witnesses;
- 80 exact endpoint-carrier candidates;
- 264 unresolved (`p=144`, `t=120`).

The 264 unresolved-row digest is:
`fce311f4f4c4c382d3edba6c3e808891a04c580f90693fee043cde1ea326d1c5`.
Every unresolved row remains fail-closed.

There are also lower-dimensional box contacts (`dimension=0` or `1`), but
box contact alone is never an edge in the safe quotient.  Only an exact
materialized endpoint carrier can identify such incidences.

## U|U nonmerge audit

- U|U sheet rows: 88
- two-curve leaves: 76
- one-curve/other-face-absent leaves: 12
- safe-quotient joins between the lower and upper curve of the same U|U
  leaf: 0
- curve-pair intersection credit: 0

Thus the 76 strictly ordered and disjoint lower/upper curve pairs remain
separate.  No shared signature or carrier hash collapses them.

## Thirty-six local ordinals

Round211 touches 24 outgoing local exact-key ordinals.  Round204 touches 12
separate wall-return ordinals.  The sets are disjoint and their union has 36
ordinals.

- Round211 24-ordinal SHA256:
  `7b9394fd0da52793cb900cb82a26f7456d4097159b00f6fcf7a09bf14dc1f58c`
- Round204 12-ordinal SHA256:
  `b6a4be44c82676bbef4e07ce1125ab862b1b8dd794e06dd45394a2e2a87cf855`
- 36-ordinal union SHA256:
  `5ba4d5186ddb7ddb1868957f83af9d5224dbddaa619ecfedf1cdc51f7bc03763`
- safe quotient blocks joining distinct outgoing ordinals: 0

This is a local ordinal audit only.  It proves no global exact-key fibre is
exhausted.

## First missing frontier

A full physical-component producer is premature.  The next formal boundary
must materialize:

1. `p/s` internal-face active-factor zero-trace incidence IDs, with the two
   incident leaves and exact restricted geometry;
2. explicit cross-occurrence common-refinement/glue IDs;
3. partial-face curve restrictions, including endpoint-to-curve-interior
   joins where one leaf boundary is a strict subface of another; and
4. an independent component verifier that rebuilds those rows before reading
   the claimed quotient.

Until those rows exist, the safe block counts above must not be called
physical-component counts.

## Credit boundary

- formal component-deduplication credit: 0
- whole-leaf credit: 0
- whole-origin credit: 0
- whole-original-tube credit: 0
- global component credit: 0
- global exact-key disposition credit: 0
- source-G global dispositions: `0 / 224,580`
- D02: unchanged `BLOCKED`
- Gate5: unchanged `10/18`
- CM2: unchanged `NO-GO`

