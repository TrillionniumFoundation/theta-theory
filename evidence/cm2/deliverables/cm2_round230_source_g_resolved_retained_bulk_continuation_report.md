# CM2 Round230 — source-G resolved/retained bulk continuation

Date: 2026-07-27

## Verdict

`PASS_PARTIAL_FORMAL_ROUND230`

Round230 exhausts the frozen `8,960` Round220 one-step resolved/retained
interfaces against materialized Round208 retained-side regions. It certifies
`784` strict non-event positive-area local bulk continuation patches on `448`
interface stars and derives `464` new known-block incidences. These incidences
are not membership, physical-component assignments, maximality, or global
exact-key dispositions.

## Exact census

- normal-form absence references: `8,976`;
- interfaces with Round208 materialization: `460`;
- relevant Round208 regions: `1,536`;
- exact face candidates: `1,512`;
- accepted patches: `784` (`400` t, `384` p);
- wrong-side/factor rejects: `728`;
- remote full-signature references without face overlap: `12`;
- stars: `448` (`444` block-backed, `4` sheetless-only).

Every accepted patch has equality of all ten immutable return-signature
fields, an exact positive-area face, and strict equal Round186/Round208
HPLUS/HMINUS signs on the whole patch.

The frozen Round211→Round225 sheet incidence seeds `444` resolved-child
incidences and `20` sheetless Round208-region incidences inside mixed stars.
The Round229 frontier therefore moves from `35,432 / 18,536` attached /
unattached to `35,896 / 18,072`. All `53,968` post-frontier rows and `116`
per-key rows are frozen.

## Coverage and limits

Exact star coverage ratios are t-axis `276 × 1/64`, `44 × 1/32`,
`4 × 9/64`; p-axis `112 × 1/64`, `8 × 1/32`, `4 × 1`. Only four stars
cover a whole one-step interface. No maximal-component credit follows.

The independent verifier pins Rounds 179, 208, 211, 220, 225, and 229,
rebuilds all interfaces, independently evaluates the pinned Round186 interval
kernel, and binds every accepted/rejected/star/delta/post/key row. Result:
`PASS_INDEPENDENT_ROUND230`.

## Frozen hashes

- producer: `6b9bac3fd7da301bffb73b0545cc16505df84f69c4f496075cbb146157377cbb`;
- certificate: `88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73`;
- certificate result: `325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e`;
- verifier: `e2fdd802ab5d2ccb0d99483da4aed5cff96004c4c6c04518ac9a80cbafe79d72`;
- verification: `a48df50b6ffd38f096dbbeece6e6f1707a69ce08313ae302c993aac5d34fca0c`;
- verification result: `051c32a9a338eab20b729cc4e6bc5706ca0a4c3a439dbf80a05f9564da85bbdb`.

Both producer and verifier cold replays are deterministic.

## Gate impact and next route

The core global gate remains open: maximal assignments `0/53,968`, exhausted
key fibres `0/116`, source-G exact-key dispositions `0/224,580`, Gate 5
`10/18` with zero complete blocks, CM2 `NO-GO_FOR_CLAIM`.

Next: materialize deeper retained event/common-refinement strata for the
`18,072` unattached occurrences, starting from the `8,512` interfaces with no
accepted current Round208 patch. Only after retained-stratum exhaustion can
the `7,404` known blocks be tested for maximality and all `116` fibres rebuilt.
