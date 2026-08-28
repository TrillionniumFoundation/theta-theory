# Round299-A Source-G refined-occurrence official-key binding closure

## Outcome

Round299-A passes as an **independently verified, append-only official-key
binding closure** for all 9,404 Round294 refined occurrences. It neither
rewrites an occurrence identity nor merges any raw key.

The exact binding census is:

| binding class | rows | distinct keys |
|---|---:|---:|
| key already present in the pre-refined Round294 universe | 8,212 | 36 |
| new raw key from a pinned Round275 local-return signature | 1,192 | 8 |
| total | 9,404 | 44 |

The 1,192 new-key rows split equally: each of the eight new raw keys has
exactly 149 binding rows and 149 refinement member cells. The raw observed key
universe therefore changes from 116 to 124. This is an enlarged denominator,
not an eight-key merge into the former 116-key universe.

## Frozen input contract

The producer exhausts and byte-pins five sealed upstream manifests:

| package manifest | SHA-256 |
|---|---|
| Round275 complete reverse-rechart materialization | `a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669` |
| Round282 strict true-seam normal-corridor probe | `c93d7982b036126ea4fcae761316d86863051d19c9fa9a3008b82ef9c6d44081` |
| Round285 true-seam safe-pairing contract probe | `260065c2a0253516ebda73ba68db8bd76cd3d6e68fade0535d81b77e1471b952` |
| Round292 R287-registry overlap exhaustion probe | `4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870` |
| Round294 occurrence-registry atomic promotion | `90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131` |

The selected source artifacts are independently pinned inside the producer:

| selected artifact | SHA-256 |
|---|---|
| Round275 certificate | `e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386` |
| Round282 ledger | `6d94bce99b3ea57b8a568707705d9f16833cfba28b242a6dabb2de5933f6509e` |
| Round285 ledger | `92462778ad249c5aff2d7a8d0205efa288ccaf191ab8a419c8b6f58a18dfcc1e` |
| Round292 ledger | `8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab` |
| Round294 registry ledger | `c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb` |

Every member named by each sealed manifest is hash-checked before
construction. Input paths must be HERE-only regular, non-symlink,
single-hardlink files. JSON decoding is duplicate-free, finite, and integral.

## Exact source-to-binding reconstruction

The producer revalidates 13,788 Round275 regions, 11,852 Round292 refinement
cells, 9,404 Round292 refined components, and all 431,208 Round294 registry
rows. The full Round294 row, row-ID, row-hash, and occurrence-ID commitments
are recomputed before the 9,404 refined rows are selected.

For every selected occurrence it closes the exact join among:

1. the existing Round294 occurrence ID and frozen null-key registry row;
2. the Round292 refined-component ID and row hash;
3. the pinned Round275 region ID and row hash;
4. the complete ten-field local-return-signature hash and preimage; and
5. every refinement member ID, exact transformed open cell, exact volume,
   source row hash, chart, owner, and signature hash.

The output has 9,404 distinct occurrence IDs, 9,404 distinct Round292
component IDs, 9,404 distinct Round275 region IDs, and covers exactly 10,252
refinement member cells. Join mismatch count is zero. Binding-row occurrence
ID rewrite count and key-merge count are both zero.

The complete 44-key binding-count histogram is:

```text
4:8, 10:4, 12:4, 149:8, 240:4, 241:4, 312:8, 918:4
```

## Why the eight raw keys remain distinct

The eight new-key ordinals and their unique old-universe wall-transition
sibling ordinals are:

| new ordinal | wall-transition sibling ordinal |
|---:|---:|
| 11,829 | 11,820 |
| 12,814 | 12,805 |
| 76,840 | 76,830 |
| 77,825 | 77,815 |
| 124,111 | 124,110 |
| 131,991 | 131,990 |
| 182,227 | 182,225 |
| 190,107 | 190,105 |

Each sibling relation is an `X:0` or `Y:0` wall transition. It differs in
exactly six signature fields: official key ID, official key ordinal, official
key row, ordered integer wall events, roof, and signed wall word. A graph-wall
transition is not a transported key equivalence.

The eight keys occupy 1,192 Round275 regions: 168 strict regions and 1,024
regular graph-crossing regions. Across all distinct Round275 local signatures,
no other raw key has the same transported six-field physical payload.

The Round282-to-Round285 side audit independently reconstructs 152 patches,
2,660 corridor-region occurrences, and 2,636 distinct corridor regions. Side
count/hash mismatch count is zero, and incidence of all eight new keys is
zero. Round285 therefore supplies no transported-equivalence evidence for a
new-to-old or new-to-new key merge.

## Independent verifier and attack rejection

The independent verifier reconstructs the entire expected candidate before it
opens the Round299-A ledger or result. It streams and recommits all 431,208
Round294 registry rows, rebuilds the 9,404 binding rows from the pinned
Round275/Round292/Round294 sources, and independently replays the Round282 to
Round285 nonmerge evidence.

The verifier treats the producer only as the inert fixed byte string with
SHA-256 `a8e8d46c8ff13c2315868a982a3b394af7629cbb3cd76eda772b2c442a9f8f59`.
It does not import, execute, or parse the producer as Python, and it does not
use the candidate ledger or result as an expected-row oracle.

The independent attack suite records:

```text
33 rejected / 0 accepted
28 fully reclosed semantic attacks
5 strict JSON/GZIP/path/file-object attacks
all_33_attacks_independently_rejected = true
```

The persisted independent commitments are:

```text
attack-suite file SHA-256
2a6b4b320dc3caac321a8bc73747240acfbb638e42dad605f7546d9912e69957

attack-suite self-closure
972f019be81f8cb3ab52d41a6b252070d3b8682423ba204d2b71b0a3c02b6642

verification file SHA-256
3a3ab65fdd6b5bd00062e1cebbd141e1c38bded7d920705a83a57ba24db0f27d

verification self-closure
a6db2ff40098c3d818014f17f31e9e57c123c20c3a9bd65733a068c002f15644
```

## Result closure order and deterministic replay

The ledger is closed and deterministically compressed first. Its file hash is
then embedded in the result. All result fields, including producer-only attack
scope and strict nonpromotion, are fixed before `result_sha256` is computed.
The result is not mutated afterward. The attack suite is constructed only
after that final result closure.

Producer seeds `299101` and `299929` generated byte-identical ledger, result,
and producer self-attack files. Independent-verifier seeds/hash seeds `299311`
and `299929` generated identical attack-suite and verification commitments.
The exact replay commands and comparisons are recorded in the separate
cold-replay document.

## Formal credit and nonpromotion boundary

Only append-only key-binding metadata moves:

| credit/state | Round299-A value |
|---|---:|
| refined-occurrence official-key binding credit | 9,404 |
| raw observed key-universe delta | 8 |
| new-occurrence credit | 0 |
| occurrence-alias credit | 0 |
| component-union credit | 0 |
| DSU rank-reduction credit | 0 |
| Jx/Jy same-point glue credit | 0 |
| maximality credit | 0 |
| exact-fibre credit | 0 |
| global-disposition credit | 0 |
| raw-key merge credit | 0 |

Round299-A does not rebuild the component DSU, compute a post-binding
component count, certify maximality, exhaust exact key fibres, assign a global
disposition, unblock D02, or promote CM2. D02 remains blocked and CM2 remains
no-go for claim.

The next core gates are:

1. freeze every remaining legitimate component-edge channel and rebuild the
   component DSU;
2. recompute component-key incidence over the 124-key raw universe; and
3. exhaust the exact-key fibre denominator before any maximality or global
   disposition promotion.

## Final package artifact pins

| artifact | SHA-256 |
|---|---|
| producer | `a8e8d46c8ff13c2315868a982a3b394af7629cbb3cd76eda772b2c442a9f8f59` |
| independent verifier | `8284650153f6dd933f493249f6af1c778fc1622639d465202ce752ea8935b215` |
| binding ledger file | `ffea8120af2179990d5c9e7ff385193e2c5a08bed161cf5b570aa28b1f8b1ee0` |
| result file | `4835bab4ebe7afc0da8d00395f83f881dd2aaf31e0697994fed54dc7d86302f5` |
| result self-closure | `5a3cece69ad8f7737b8f80ca6828d34da969de1a22d56af5f6ed422356d88233` |
| independent attack-suite file | `2a6b4b320dc3caac321a8bc73747240acfbb638e42dad605f7546d9912e69957` |
| independent attack-suite self-closure | `972f019be81f8cb3ab52d41a6b252070d3b8682423ba204d2b71b0a3c02b6642` |
| independent verification file | `3a3ab65fdd6b5bd00062e1cebbd141e1c38bded7d920705a83a57ba24db0f27d` |
| independent verification self-closure | `a6db2ff40098c3d818014f17f31e9e57c123c20c3a9bd65733a068c002f15644` |
