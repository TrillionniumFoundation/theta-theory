# CM2 Round229 — source-G global occurrence-to-known-block frontier

Date: 2026-07-27

## Verdict

`PASS_PARTIAL_FORMAL_ROUND229`

Round229 materializes and independently verifies every local 3D occurrence in
the frozen Round216 source-G universe.  It proves an exact incidence
crosswalk from Round208 region sides through Round211 sheets to Round225
known-connectivity blocks where such an ID chain exists.  It does not treat
that incidence as 3D block membership or as a maximal physical-component
assignment.

## Exact occurrence census

The complete local occurrence universe has `53,968` rows:

| gauge | rows | known-block incidence |
|---|---:|---:|
| Round179 resolved children | 17,192 | 0 |
| Round204 strict open regions | 736 | 0 |
| Round208 strict open regions | 36,040 | 35,432 |
| **total** | **53,968** | **35,432** |

Round208 satisfies the exact identity

`36,040 = 2 × 17,716 + 608`.

The `17,716` Round211 sheets have `35,432` distinct owner/shadow region-side
IDs, all of which join uniquely to Round208.  The remaining `608` Round208
regions are sheetless.  Consequently:

- occurrences with an exact Round225 known-block incidence: `35,432`;
- occurrences without any known-block incidence: `18,536`
  (`17,192 + 736 + 608`);
- maximal physical-component assignments: `0 / 53,968`.

## Key purity and contact closure

All `17,716` Round211 sheets have exactly one Round225 assignment.  The
assignments reconstruct `7,404` known-connectivity blocks, and every block
has official-key cardinality exactly one:

- key-pure known blocks: `7,404`;
- mixed-key known blocks: `0`;
- official keys with sheet/block incidence: `24 / 116`;
- official keys without sheet/block incidence: `92 / 116`.

The independent verifier also reconstructs the `7,252` Round225 added
contact pairs:

- Round223 exact p/s TRACE pairs: `7,016`;
- Round224 exact partial-contact TRACE pairs: `236`;
- cross-key contact pairs: `0`;
- remaining frozen known-contact frontier: `0`;
- proved-ABSENT rows remain nonedges.

This closes the contact universe frozen by Rounds 211–225.  It does not prove
that future retained event strata are exhausted.

## Round216 blocker delta

The following Round216 obligations are now closed in their exact scopes:

- Round179 coordinate boundary atlas:
  `17,192 / 17,192` children, with `103,152` faces, `206,304` edges, and
  `137,536` corners;
- all those Round220 boundary rows are coordinate-only, with event-sheet
  incidence and physical-glue credit both zero;
- exact p/s contact frontier: `7,932 / 7,932`;
- partial contact frontier: `264 / 264`;
- Round220 rejected-coordinate pool: `9,830 / 9,830` excluded as an
  event-trace source;
- Round227 Jx/Jy symmetry partners: `35,432` directed partners, all
  non-glue;
- Round228 materialized-sheet atlas overlap: zero source-seam candidates and
  zero unclassified channels.

The global occurrence-fibre obligation is not closed:

- globally exhausted observed key fibres: `0 / 116`;
- source-G exact-key dispositions: `0 / 224,580`;
- maximal physical-component credit: `0`.

## Exact resolved-to-retained frontier

Round229 also freezes all `8,960` Round220 resolved↔retained one-step
interfaces:

- interfaces whose retained child appears in Round208: `460`;
- interfaces with coordinate-only references to one or more Round225 known
  blocks: `456`;
- interfaces reaching only sheetless Round208 regions: `4`;
- interfaces with no Round208 materialization: `8,500`;
- referenced Round208 region sides: `1,536`;
- referenced Round211 sheets: `740`;
- exact event-trace bridges: `0`;
- physical union credit: `0`.

These `456` block references are coordinate lineage only.  The verifier
rejects any attempt to turn parent/chart/key equality, coordinate adjacency,
or a one-step interface into a physical edge.

## Independent verification

The verifier:

- never imports or executes the producer;
- pins and strictly parses Rounds 179, 204, 208, 211, 216, 220, 225, 226,
  227, and 228;
- independently rebuilds all three Round229 ledgers;
- checks every row closure and every ledger row/ID/hash digest;
- reconstructs Round225 membership from the assignment table and compares it
  to the formal block ledger;
- rejects `12/12` semantic promotion/forgery attacks, including one fully
  re-signed compound attack;
- rejects `16/16` strict-JSON attacks and `8/8` path/file attacks.

Producer seeds `229041` and `229777` emitted identical result and certificate
hashes.  Verifier seeds `229919` and `229041` emitted identical verification
bytes.

## Frozen hashes

- producer:
  `2518319a103acacc0b6a3dbdd165d9cefd3656d6c323063094daa598bede454c`;
- certificate:
  `c4152f4764ed7fe977046ef728e8257344803433053e06c0ac11ec68b86ff11a`;
- certificate result:
  `936e140d7113dbdd565f4b1a9381de3b90313e7198266c1950532b80ba153230`;
- verifier:
  `0e8245faa5e6d1e52310f0ce1545062a4de62b59dca7692b5bebd6d4c1ff397f`;
- verification:
  `f570c2148256087687d0b35baebc14bd64c99cdd60326e96fcb320e31605968a`;
- verification result:
  `dce1ea3733b78b1f476da80953380a679924a09c94e86bd9e0584a1695875e86`.

## Strict limitation and next gate

The `7,404` blocks remain key-pure known-connectivity blocks, not maximal
physical components.  D02 remains `BLOCKED`, Gate5 remains `10/18`, complete
18-field blocks remain `0`, and unconditional CM2 remains
`NO-GO_FOR_CLAIM`.

The next shortest core gate is to classify all `8,960`
resolved↔retained interfaces by exact event-trace/common-refinement evidence,
then attach or exclude the `18,536` occurrences that presently have no known
block incidence.  Only after the full retained-stratum universe and all
`116` occurrence fibres are independently exhausted can any global
exact-key disposition be credited.
