# CM2 Round230 — source-G resolved/retained bulk continuation

Date: 2026-07-27

## Verdict

`PASS_PARTIAL_FORMAL_ROUND230`

Round230 exhausts the frozen set of `8,960` Round220 one-step
resolved/retained interfaces for exact positive-area contact with the
materialized Round208 retained-side regions.  It certifies `784` strict
non-event local bulk continuation patches on `448` interface stars and
derives `464` new known-block incidences.  These incidences are not block
membership, physical-component assignments, maximality, or global exact-key
dispositions.

## Exact bridge census

- frozen resolved/retained interfaces: `8,960`;
- normal-form absence references: `8,976`;
- interfaces with Round208 retained-side materialization: `460`;
- relevant Round208 regions: `1,536`;
- exact positive-area face candidates: `1,512`;
- accepted local bulk patches: `784` (`400` t-faces, `384` p-faces);
- wrong-side/factor-incompatible rejects: `728`;
- remote full-signature references without exact face overlap: `12`;
- bridge stars: `448` (`444` block-backed, `4` sheetless-only).

Every accepted patch has exact equality of all ten immutable return-signature
fields, an exact positive-area shared box face, strict Round186 HPLUS/HMINUS
signs on the whole patch, and equality with the Round208 region signs.

## Incidence delta

The frozen Round211-to-Round225 sheet incidence is the only seed:

- direct sheet-backed accepted patches: `728`;
- sheetless accepted patches: `56`;
- new resolved-child known-block incidences: `444`;
- new sheetless Round208-region incidences propagated inside mixed certified
  bridge stars: `20`;
- total new occurrence incidences: `464`;
- distinct Round225 blocks reached by those stars: `440`.

The Round229 occurrence frontier changes from `35,432` attached and `18,536`
unattached to `35,896` attached and `18,072` unattached.  All `53,968`
post-frontier rows and all `116` per-key rows are explicitly frozen.

## Coverage and limits

Accepted patch coverage is deliberately local.  The `448` stars have exact
coverage ratios:

- t-axis: `276 × 1/64`, `44 × 1/32`, `4 × 9/64`;
- p-axis: `112 × 1/64`, `8 × 1/32`, `4 × 1`.

Only four stars cover a whole one-step interface.  Even there, the
certificate does not promote the local continuation into maximal physical
component credit.  The remaining `8,512` interfaces have no accepted patch
in the currently materialized Round208 stratum.

## Independent verification

The independent verifier does not import or execute the producer.  It pins
and strictly parses Rounds 179, 208, 211, 220, 225, and 229; independently
rebuilds all `8,960` interfaces; evaluates the frozen Round186 interval
factor kernel on every exact face; reconstructs the accepted, rejected,
bridge-star, incidence-delta, post-occurrence, and per-key universes; and
checks every ledger row closure and aggregate digest.

Result: `PASS_INDEPENDENT_ROUND230`.

## Frozen hashes

- producer: `6b9bac3fd7da301bffb73b0545cc16505df84f69c4f496075cbb146157377cbb`;
- certificate: `88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73`;
- certificate result: `325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e`;
- verifier: `e2fdd802ab5d2ccb0d99483da4aed5cff96004c4c6c04518ac9a80cbafe79d72`;
- verification: `a48df50b6ffd38f096dbbeece6e6f1707a69ce08313ae302c993aac5d34fca0c`;
- verification result: `051c32a9a338eab20b729cc4e6bc5706ca0a4c3a439dbf80a05f9564da85bbdb`.

Producer and verifier cold replays reproduce the same result and certificate
hashes byte-for-byte.

## Gate impact and required next

Round230 reduces the no-incidence frontier by `464`, but it does not close
the core global gate:

- maximal physical-component assignments: `0 / 53,968`;
- globally exhausted observed key fibres: `0 / 116`;
- source-G exact-key dispositions: `0 / 224,580`;
- Gate 5: `10 / 18`, complete blocks `0`;
- CM2: `NO-GO_FOR_CLAIM`.

The next highest-value route is to materialize deeper retained event strata
for the `18,072` still-unattached occurrences, beginning with the `8,512`
one-step interfaces that have no current accepted Round208 patch.  Any new
contact must be certified as an event/common-refinement channel rather than
coordinate adjacency.  Only after retained-stratum exhaustion can the
`7,404` known blocks be tested for maximality and all `116` exact-key fibres
be independently rebuilt.
