# CM2 Round296 Source-G true-seam occurrence-edge ledger closure

## Outcome

Round296 passes as an edge-evidence-only package.  It freezes the exact
occurrence-level edges carried by all 152 positive-area Round268 true-seam
patches:

- 3,444 exact half-open common-refinement cells: 148 full-patch cells and
  3,296 tail-patch cells.
- 48,444 formal true-seam edge rows: 504 on full patches and 47,940 on tail
  patches.
- 15,316 distinct unordered endpoint pairs and 5,784 actual Round294
  occurrence targets.
- zero self-edges, zero edge-key collisions, and every repeated endpoint pair
  across different cells preserved.

This round does not run a DSU, does not consume ordinary-face edges, and does
not compute or report a quotient-component count.  Component, DSU-rank,
Jx/Jy, maximality, fibre, and global-disposition credits remain zero.

## Frozen inputs and reconstruction

The producer and independent verifier byte-pin and exhaust all entries of the
Round268, Round275, Round282, Round285, Round287, Round289, Round294, and full
Round295-B manifests.  The verifier reconstructs the source objects before it
opens any Round296 candidate artifact and never imports or executes the
producer.

For each strict Round282 corridor, the terminal occurrence is selected by the
exact nearest closure distance from the corridor's dyadic seam endpoint
`t²` to the Round294 mapping interval.  The 11,448 Round295-B physical
incidences are then added.  Of their target-reference fields, 5,292 are
Round294 source-row IDs and are independently canonicalized through the
unique Round294 source-row-to-occurrence map; 6,156 are already canonical
Round294 occurrence IDs.  All final endpoints lie in the 431,208-element
formal Round294 registry domain.

The discarded side diagnostic that counted 3,700 strict fragments was not a
source-closed count and is rejected.  It is not used by the certificate.
The exact source-closed fragment audit is:

| Source | Raw evidence | Distinct formal endpoint atoms | Duplicate excess | Multiplicity histogram |
|---|---:|---:|---:|---|
| Round282 strict corridor terminal slices | 3,532 | 3,004 | 528 | 1×2,652; 2×240; 3×48; 4×64 |
| Round295-B physical terminal incidences | 11,448 | 7,584 | 3,864 | 1×5,856; 2×640; 3×40; 4×1,048 |
| Union | 14,980 | 10,588 | 4,392 | 1×8,508; 2×880; 3×88; 4×1,112 |

The atom key is
`(patch, side, exact p-s box, complete payload SHA-256, actual Round294 occurrence ID)`.
There are 352 multiply evidenced strict atoms (880 raw rows, excess 528),
1,728 multiply evidenced Round295-B atoms (5,592 raw rows, excess 3,864),
8,508 singly evidenced atoms, and no cross-source atom overlap.  Raw rows
remain provenance; cell payload-occurrence maps deduplicate formal atoms
before any edge is formed.

## Safe-pairing and negative evidence

All 152 Round285 rows are checked semantically, not merely carried by ID:

- `same_physical_source_point`,
  `Round171_normal_position_velocity_identity`,
  `transported_owner_target_sets_equal`, and
  `owner_shadow_half_open_pair` are true.
- cyclic transition identity agrees with Round268 and the geometry class
  agrees with Round282.
- every Round285 exact cell is positive, cells have disjoint interiors, and
  each patch conserves exact area.
- 464 geometric-pair cells have total area `1139/102400`; 876 uncovered
  arrangement-tail negative cells have total area `141/102400`; together
  they are 1,340 cells of area `1/80`.
- every uncovered cell is explicit negative evidence and contributes zero
  endpoints.

The 468 wrong-sign empty rows and 288 graph-separated rows from Round295-B
remain no-bind evidence and never enter endpoint construction.  Pairing is
allowed only when both sides carry the same complete six-field physical
payload:
`target_chart`, `target_lift`, `outgoing_cell`,
`ordered_integer_wall_events`, `roof`, and `signed_wall_word`.

## Independent verification

The independent verifier reproduces both ledger objects and their
deterministic GZIP bytes exactly, then reproduces the canonical result JSON
exactly.  It enforces HERE-only single-link regular paths, bounded file and
GZIP expansion, duplicate-key-free integer-only JSON, canonical result JSON,
and one GZIP member with no trailing bytes.

All 46 targeted attacks are rejected, including 22 reclosed attacks covering
raw-reference misuse, missing/duplicate canonical maps, external occurrence
IDs, wrong-sign or graph-negative promotion, incomplete/altered payloads,
non-common payload pairing, self-edges, endpoint orientation/key changes,
repeated-pair deduplication, R285 negative-cell promotion, forged fragment
censuses, forged preview counts, DSU/component credit, and a forged quotient.

Producer seeds `296071` and `296997` reproduce identical candidate hashes.
Verifier seeds `296173` and `296991` reproduce identical verification and
attack-suite hashes.  A first verifier replay exposed PID-bearing temporary
paths in diagnostic text; those unsealed artifacts were discarded.  Stable
guard-class error codes were then used and the official dual-seed replay was
byte-identical.

## Sealed artifact hashes

- producer: `7a9771e0896550f597cfd472dafb1a378b33a3e2a02e83414d79cc29962cb843`
- edge ledger: `1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7`
- cell ledger: `c664bcb76b056faac47970a1add9be7ce906dab3212a5ab954a5388d0476ecb8`
- result: `d55d9d8fe13ef98c8f07cdea91a6b5397b7f6715f85ae0f8549832ba59c1498f`
- verifier: `3c223cbfc0e63f225246b9a62729717d8b3ff23b09c2797a3f7c2646e434f6a6`
- verification: `8ec51d83459f2eac3389054b0c08a7c646973d2eac4addb7447cce6210d8b4d5`
- attack suite: `9564e51783d6496d3eaebf725a00581c5a812a6dd6590f6fba354097659ff826`

## Next formal step

A later explicit DSU round must consume all 48,444 true-seam edge rows
together with the separately frozen ordinary-face edges.  Until that happens,
Gate5 remains `10/18`, D02 remains blocked, and CM2 remains no-go for claim.
