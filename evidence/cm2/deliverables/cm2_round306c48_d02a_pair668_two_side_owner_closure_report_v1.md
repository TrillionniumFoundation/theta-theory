# C48 D02-A pair-668 two-side owner-closure candidate v1

Date: 2026-08-11 (Asia/Shanghai)

Status: `PASS_C48_PAIR668_TWO_SIDE_ROUTE_MARGIN_AND_FULL_UNIVERSE_OWNER_CANDIDATE_CLOSED__PENDING_INDEPENDENT_AUDIT__ZERO_FORMAL_CREDIT`

C48 closes one candidate task only. It does not install a pointer, change C42,
modify canonical status, or award formal D02-A credit.

## Frozen predecessor and successor chain

- C47 result object: `c57bc2711dbc7dad13178643b26f5722d48db703598d3238bfd98aa254e4f9f4`
- C47 frontier checkpoint: `6ed628697caf0feb81a0dc5428e1a27bf472c2ec59496556dcffa60ba5ddba5e`
- C46 shard 2: `c46-d02a-shard:538ecddfbdd47c229c2e6ed2c62285bcea0b93a101832eef5ea849656c34dd28`
- C46 shard task count: 514; selected pair-668 task is index 0.
- C46 generation-0 checkpoint: `8c0029650c5dfd460e4ed721ded69e004220522bcf2c51d70859547430e018b7`
- C48 generation-1 successor: `bbd909cad5a5d0b9cc44362be6acb26d527f86edc1b8191c06a246a514c9c984`
- States 1 through 513 are copied byte-for-byte from rebuilt generation 0.

## Exact two-side routing and margins

The logical prefix-free frontier is `0, 10, 11`, with exact Kraft sum one on
each physical side. All six routes terminate at strict collision-two owner
mismatch:

- representative owner `G[1,0]`, outgoing chart `N`, word ordinal 290575;
- reflected owner `G[1,1]`, outgoing chart `S`, word ordinal 291560;
- reflected physical paths `1010001001`, `10100010001`, and `10100010000`.

Each margin certificate records the whole-box collision-one root records, the
strict H1 side, a strict center collision-two root order, strict screening of
every unresolved full-box competitor, and positive exact obstacle-boundary
separation preventing root-order crossing. Direct whole-box near-root
interval separation was not claimed where its enclosures overlap.

## Full-universe codimension ownership

The producer scans all 91,879 frozen C41 ambient rows and materializes both
physical occurrences: 183,758 baseline occurrences, of which 183,700 have
exact rational boxes. It removes the two selected predecessor occurrences and
inserts six C48 occurrences, yielding a 183,762-occurrence overlay.

The selected frontier has, per physical side:

- 10 unique atomic face entities and 13 leaf-face atom occurrences;
- 8 unique corner entities and 12 leaf-corner occurrences;
- one selected-frontier internal three-way T-junction.

All 20 face atoms have exactly two full-universe incidents. All 16 corner
entities pass four-quadrant germ coverage. Every face and corner has a unique
lexicographic-minimum C41 semantic-path owner.

## Accounting and strict stop

- Frozen C41 logical residual outers: 33,642.
- Installed-C42 logical closed tasks: 1.
- Authoritative pending before C48: 33,641.
- Additional C48 candidate closed tasks pending audit: 1.
- Candidate pending after C48: 33,640 (67,280 physical-side occurrences).
- Coarse formal authority remains `574 paired / 1,150 unresolved / 575 reps`.
- D02-A remains incomplete; D02-B/D02-C/D03 are not promoted or started here.
- Formal credit remains zero until the independent C48 audit passes.

## Validation

- Producer source SHA-256: `a16d8802288c021d6d153942df15c7e7f0078628f5fb2c29eb927c6e9b94a7b8`.
- Candidate file SHA-256: `5f356dd0b1bb9ded56548a8b046f2401ad59bf706c253d44dd151649035d283e`.
- Candidate object SHA-256: `61de17d0a8122a4a03af34cf832cd717fdb715cd9c4cd2fac4162bdab8ddceab`.
- `py_compile`: PASS.
- Pure self-test: 7/7 PASS; object `909a4d0dc9ba24fe15f76ffb2d9b02cacaa8b6fe2aee0ab5a2819b498f34c24a`.
- Full materialization: PASS with exact predecessor, route, margin, owner,
  conservation, reflection, and 514-state successor checks.
