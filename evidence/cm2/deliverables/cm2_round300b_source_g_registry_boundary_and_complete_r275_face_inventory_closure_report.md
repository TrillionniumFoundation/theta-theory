# Round300-B registry-boundary and complete-R275 face inventory closure

## Verdict

`PASS_FORMAL_FULL_FACE_INVENTORY_CLOSED`

Round300-B independently accounts for both remaining audited face scopes:

- 6,616 exact R292-to-base-registry boundary faces;
- 55,932 exact complete-R275 region common faces;
- 62,548 total face rows, with zero unresolved rows.

Every accepted row carries an exact rational positive-area guided patch and
two exact rational positive-volume side corridors. Every active graph factor
is replayed on the patch and its relevant corridor. Every rejected row carries
either an exact same-factor/opposite-strict-side exclusion or an exact
whole-face empty-support extrema certificate.

## Physical classification

| Channel | Raw faces | Accepted | Exact exclusions | Unresolved |
|---|---:|---:|---:|---:|
| R292 → base registry | 6,616 | 6,600 | 16 | 0 |
| Complete R275 frontier | 55,932 | 36,140 | 19,792 | 0 |
| Total | 62,548 | 42,740 | 19,808 | 0 |

The 19,792 R275 exclusions consist of 12,608 exact
same-factor/opposite-strict-side rows and 7,184 exact whole-face empty-support
rows. The boundary channel's 16 exclusions are whole-face empty-support rows.

## Edge projection and exact accounting

- 78,616 deduplicated accepted face/pair witness rows;
- 15,056 exact self-endpoint incidences, all zero edge credit;
- 4,288 accepted boundary pairs;
- 34,628 accepted complete-R275 pairs;
- 2,776 pairs witnessed by both Round300-B channels;
- 36,140 distinct accepted pair union;
- 42,476 duplicate raw witnesses beyond the first witness per pair;
- 25,724 pairs suppressed because already present in pinned prior channels;
- 2,824 boundary pairs new beyond R295A/R296/R297/R299C;
- 7,592 complete-R275 pairs incrementally new beyond the same prior union and
  the boundary channel;
- 10,416 canonical novel component-edge pairs.

Pair acceptance is existential: a rejected local face never negates a
separate accepted physical witness for the same unordered endpoint pair.
Endpoint cross-products that repeat the same face/pair are represented once
with exact multiplicity, rather than being counted as new edges.

The canonical novel-pair commitment is
`24d6e890200f8c87799f916d94af2a0c32e2ed3dcc2e67d831df1b1efeaf5add`.

## Independence

The verifier treats the producer only as the fixed byte string
`e760511408ac78e627155f55671b3e2e8d6f9b1b8163a82ffac65230b10fa93d`.
It does not import, execute, tokenize, or parse it.

Before opening candidate ledgers, the verifier reconstructs the complete
source state from sealed R275/R287/R292/R294 inputs, all 421,804 base registry
supports, and all prior pair sets. Its boundary enumeration uses its own exact
interval index and its R275 enumeration uses an independently constructed
lower-boundary index. It then:

1. proves exact equality of the independently enumerated 62,548-row scope;
2. rechecks every patch, corridor, factor state, exclusion, and nonclaim;
3. rebuilds the raw, self/exclusion, duplicate/prior, and canonical ledgers;
4. requires exact candidate-object equality after reconstruction.

The earlier zero-credit Round299C-boundary and Round299D diagnostic artifacts
are neither imported nor read. The pinned Round299C signed-face canonical pair
ledger is consumed only as a prior-channel deduplication set; Round300-B does
not rely on it for any face proof.

## Attacks

Both verifier runs rejected all 36 attacks:

- 21 semantic/coordinated-reconstruction attacks;
- strict duplicate-key, trailing-token, NaN, and BOM JSON attacks;
- concatenated-member, trailing-byte, noncanonical-mtime, and duplicate-key
  gzip attacks;
- symlink, hardlink, directory, and parent-escape path attacks;
- coordinated row/ledger/result re-sign attacks.

The identical attack-results commitment is
`4798ddda2fe5e1a08e336949844bdc61d6e76f7d91146114ebae3c85bf320943`.

## Dual-seed replay

- `round300b-alpha`: PASS in 912.48 seconds, peak RSS 11,642,344 KiB;
- `round300b-beta`: PASS in 907.72 seconds, peak RSS 11,641,244 KiB.

The seed-invariant projection of status, census, all five reconstructed
commitments, attack results, and strict nonclaims is identical:
`aaef8e141e49cbe81f4e5f910d769ee5ffe47da6b5acec51a4028aa4e2284db5`.

## Strict nonclaims

The 10,416 canonical rows receive component-edge credit only. Round300-B
awards zero occurrence-identity, DSU-rank, maximality, fibre, global
disposition, and CM2 credit. Pair count must not be interpreted as DSU rank
reduction. Final rank and component counts require the separately sealed,
order-independent full DSU.

