# CM2 Round285 — true-seam safe-pairing contract probe

Status: **PASS PROBE — 0/152 FORMAL SEAM EDGES — ZERO CREDIT**

Round285 independently freezes the endpoint-pairing semantics needed after the
24 remaining outgoing-arrangement tails close.  It joins the frozen Round268
true-seam patches, the complete Round275 rechart-region universe, Round279 atom
incidence, the corrected Round280 occurrence identity contract, the Round282
normal corridors, and the Round284 occurrence-overlap dispositions.

## Exact seam census

- Round268 true-seam patches: `152`;
- directed endpoints: `304`;
- distinct Round182 seam-owner rows: `272`;
- owner reuse degrees: `248×1`, `16×2`, `8×3`;
- all `152` owner pairs are unique;
- repeated-owner patch interiors have zero positive-area overlap;
- patch areas: `72×1/12800`, `48×1/25600`, `32×1/6400`.

Round282 currently supplies:

- `128/152` full bidirectional geometric corridor covers;
- `24/152` arrangement tails;
- `264/304` full directed sides;
- `40/304` partial directed sides.

The tails are symmetric: each of the four true cyclic seams has six.  Sixteen
patches have two partial sides and eight have one partial side.  Eight tails
already have one matching transported return payload on both sides; sixteen
have a `1↔2` payload partition and must be cut by the outgoing-zero graph.

## Why the 128 geometric patches still receive no DSU credit

The 128 full patches contain:

- `256` directed endpoints;
- `536` strict corridor records;
- `512` distinct Round275 regions;
- `148` exact disjoint `p×s` cells;
- `496` distinct raw left/right region pairs.

Round284 classifies the 512 incident regions as:

- `504` new-disjoint candidates whose occurrence IDs are not issued;
- `8` partial-overlap regions requiring exact refinement;
- `0` terminal aliases.

The 496 raw pairs split as:

- `488` new-candidate/new-candidate;
- `4` new-candidate/partial-overlap;
- `4` partial-overlap/new-candidate.

Against Round279 atom relations, the same pairs are:

- `472` `0|0`;
- `8` `0|1`;
- `8` `1|0`;
- `4` `0|2+`;
- `4` `2+|0`.

No pair has an atom relation on both sides.  More importantly, containment,
positive-volume overlap, common-face contact, shared parent, shared signature,
or graph connectivity never proves occurrence identity under the corrected
Round280 contract.

All 128 full patches do pass the transported physical-return comparison.
Their raw official key IDs and full signature hashes are chart-local and
therefore disjoint across the seam.  The required transported payload—
target chart/lift, outgoing cell, wall events, roof, and signed wall word—is
identical on both sides, with the source chart changed by the exact rechart.

## Frozen safe-pairing contract

1. Only a frozen Round268 patch on one of the four true cyclic source seams is
   admissible.  `Jx/Jy` is never a same-point seam transition.
2. Each patch must be partitioned into exact, disjoint, half-open `p×s` cells.
   The cells must conserve the patch with no gap or positive-area overlap.
3. Every cell side needs a strict connected normal corridor carrying a
   constant complete dynamic signature.
4. Raw chart-local key/signature equality is neither required nor sufficient.
   Exact registry transport and equality of the physical return payload are
   required.
5. Every incident Round275 region must terminate as either:
   `EXACT_SAME_POSITIVE_OPEN_REGION_ALIAS`, or
   `STRICTLY_NEW_DISJOINT_OCCURRENCE`.
6. Partial or nested positive-volume overlap must be exactly refined before
   either terminal disposition is issued.
7. Round279 common faces create component connectivity only.  Only the four
   already frozen W-tail aliases may precontract occurrence identity.
8. A true seam never collapses occurrence identity.  Its final component-edge
   key is
   `(patch_id, cell_id, left_occurrence_id, right_occurrence_id)`.
9. All distinct incident occurrences are retained.  One patch does not imply
   one edge or one DSU rank reduction.
10. Credit is the independently replayed DSU union delta after exact edge
    deduplication.

Thus closing only the 24 geometry tails would make the geometry census
`152/152`, but formal seam edges would remain `0/152` until occurrence
disposition and cell-to-occurrence binding are complete.

## Replay and hashes

Seeds `285071` and `285929` produced byte-identical result and deterministic
GZIP ledger files.  `gzip -t`, ledger row conservation, and the result-object
digest all pass.

- producer SHA256:
  `29103cecceddeb35549a93f6c6a0ab9c586c6e03972fa9e513eec1330c830e34`
- result file SHA256:
  `132d6ab861b1ffb0e718d6e79136db8a5acd4b53dafde5b02dcdcc4ad019e6b0`
- result object SHA256:
  `29f982794e8d22b1b5d94e343837fb4c61cdc8989057b77776b866c7219b09f1`
- ledger file SHA256:
  `92462778ad249c5aff2d7a8d0205efa288ccaf191ab8a419c8b6f58a18dfcc1e`
- ledger rows SHA256:
  `34c32e9b81789439f22358d0667105f231440fffb3b534665c2f6961edf5ac49`

## Strict non-promotion

Formal occurrence, component edge, DSU rank, maximality, fibre, global
disposition, and `Jx/Jy` credits are all zero.  The strict baseline remains
quotient `63,224`, expanded occurrences `126,468`, maximality `0/63,224`,
fibres `0/116`, dispositions `0/224,580`, Gate5 `10/18`, D02 blocked, and CM2
`NO-GO_FOR_CLAIM`.
