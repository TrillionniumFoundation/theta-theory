# CM2 Round179 — source-G residual-tube arrangement

Date: 2026-07-26

## Verdict

`CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_RESIDUAL_TUBE_ARRANGEMENT__NO_GLOBAL_DISPOSITION_OR_D02_PROMOTION`

Round179 processes all 62,012 positive-volume 3D residual tubes retained by
Round174.  The result is formally `PARTIAL`: 4,116 original tubes are fully
replaced by bounded strict child pieces, while 57,896 original tubes still
have at least one positive-volume residual child.

The preliminary refinement code was kept in the throwaway spike directory
and marked `PARTIAL`.  The formal producer and verifier were rewritten as
separate deliverables and do not import the spike.

## Exact failure taxonomy

The 62,012 origins belong to 28 exact reason combinations:

- 61,676 single-predicate origins;
- 336 two-predicate origins;
- outgoing-chart seam occurrences: 34,188;
- source-chart seam occurrences: 472;
- integer-wall endpoint/count occurrences: 27,208; and
- interval crossing-time occurrences: 480.

The following reason counts are exactly zero and were independently
reconfirmed: selected-root sign/owner, target grazing/discriminant,
return-time bound, simultaneous-corner order, outgoing-component sign,
finite wall-audit range, and more-than-four-crossing failures.

## One bounded adaptive split

Every Round174 residual box receives one independently selected dyadic split.
The complete child ledger is:

- original tubes fully replaced: 4,116;
- original tubes still partial: 57,896;
- strict local 3D occurrence children: 17,192;
- exact rational source-chart guards: 152;
- retained positive-volume 3D children: 106,680;
- locally observed frozen key ordinals: 116;
- fully replaced-origin key clusters: 96.

The 4,116 number is an original-tube replacement count, not a child count.
The 17,192 resolved children remain local occurrences, and the 152 guards
remain chart-coordinate guards.

Exact coordinate-volume conservation is:

`resolved 257889/524288000`

`+ guard 1239/409600000`

`+ retained 1768407/524288000`

`= input 6337131/1638400000`.

## Analytic normal forms

For every one of the 34,188 outgoing predicates, 256-bit interval
differentiation proves a strict sign for

`∂t(target_normal_x²-target_normal_y²)`.

Derivative sign alone is not treated as existence.  Exact endpoint-sign
classification gives:

- 344 full-base unique regular 2D graphs;
- 3,400 certified empty zero sets; and
- 30,444 regular zero sets if present whose base projection/clipping remains
  overwrapped.

For all 27,688 wall predicates, the exact factorization is

`(source_axis-wall)*(target_axis-wall)=0`.

The source factor is strict nonzero in 26,632 rows and a certified regular
graph in 1,056.  The target factor is strict nonzero in 1,344 rows and a
certified regular graph in 26,344.  Target-face classification consists of
320 full-base graphs, 2,248 zero-absent regular factors, 23,776 face-overwrap
regular factors, plus the 1,344 already strict-nonzero targets.  All 480
crossing-time interval-dependency overwraps are discharged by the exact
endpoint factorization.

All 472 source-chart seams satisfy opposite exact rational signs on the
`t` faces and a strict `4t` derivative, hence are full-base exact 2D graphs.
Their dynamic sides remain dimension-safe and are not promoted wholesale.

## Pair arrangements

Each of the 336 two-predicate origins has an explicit nominal 1D pair
intersection row and a boundary 0D corner candidate.  Existence,
transversality and isolation are not inferred from interval overwrap:

- certified actual pair intersections: 0;
- certified actual boundary corners: 0.

Every 2D, nominal 1D and candidate 0D row carries zero 3D-volume, zero
whole-origin and zero global-disposition credit.

## Independent verification

The independent verifier never imports or executes the Round179 producer.
It rebuilds all nine attachment tables from the pinned Round174 attachment,
reconstructs the complete expected certificate from independent statistics,
and requires full canonical equality.

- attachment bytes compared: 131,273,924;
- full attachment byte equality: PASS;
- full expected certificate equality: PASS;
- re-signed semantic mutations: 33/33 rejected;
- strict JSON/oversize attacks: 10/10 rejected;
- input/output path, type and alias attacks: 11/11 rejected.

Attachment attacks recompute the affected table digest, attachment
result/file digest and certificate digest before validation.  Two cold
replays under `PYTHONHASHSEED=17` and `PYTHONHASHSEED=211` produced
byte-identical verification documents.

## Frozen hashes

- producer: `8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab`
- certificate: `edc2c538dc04a93c2b873f53e07b5c97c6b395a1d107e7ed2de4cf2c4bd35111`
- certificate result: `0f57284c11c617349fe66877552c401f426efafbc75faa08948f099166e9cde3`
- row attachment: `f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42`
- row attachment result: `a5468800c1d89cd307a5a26c608550b04db79c64c562fb12bedb22d6cec308cb`
- independent verifier: `292719cedfb4d5b802bf87a48314b5237f7b4438e4615d124d716f497044e679`
- verification: `37eaa14cd870df64a12c2434deafe5fdead5cec303f5530208f07c11836736bc`
- verification result: `ca2ec32d84edf55919a26f556fd8e9dfc39566ad876b0cb5537168fee2b28229`

## Strict global state

- source-G global exact-key dispositions: `0 / 224,580`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`;
- D02: `BLOCKED`;
- D03 negative oracle: `UNAUTHORIZED`;
- CM2: `NO-GO_FOR_CLAIM`.

The next bounded gate is to clip the 30,444 outgoing and 23,776 wall
face-overwrap graph collars and isolate the 336 pair arrangements with
interval Newton and explicit boundary charts.
