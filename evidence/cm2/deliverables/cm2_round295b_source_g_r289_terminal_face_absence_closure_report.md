# Round295-B — R289 terminal-face absence closure

Status: **PASS** for the bounded Round295-B closure.  The previously partial
R289 terminal-face relations now have an exact, zero-frontier disposition.
This does **not** promote a CM2 claim: Gate5 remains `10/18`, D02 remains
`BLOCKED`, and CM2 remains `NO-GO_FOR_CLAIM`.

## Exact result

- Reconstructed R289 relations: **9,528**.
- Baseline: **8,844** whole physical, **396** partial, **288**
  graph-separated.
- Corrected: **9,236** physical relations (**8,844** whole + **392** mixed)
  and **292** absent relations (**4** wholly wrong-signed empty + **288**
  graph-separated).
- Formal existing-occurrence physical-incidence bindings: **11,448**, with
  one unique Round294 target per physical subcell and **10,956** distinct
  per-relation target references.
- The 396 coarse gaps refine into **468** exact wrong-signed empty-side
  pieces over **440** distinct Round286 cells.
- Per-gap piece multiplicity: `1×348`, `2×24`, `3×24`.
- Empty sign pairs: negative/negative `236`, positive/positive `232`; every
  pair is strictly opposite the desired active-factor side.
- Round286 coordinate occupancy: `0×316`, `1×152`.  Occupancy one never
  creates an occurrence or binding.
- Reuse: **28** cells occur twice without interior double counting; **4**
  cells contribute exactly half of their full face.
- Exact wrong-signed empty area: `351/409600`.
- Remaining R289 terminal-face frontier: **0 cells**, area `0`.

The ledger is a four-table atomic package:

1. 9,528 corrected relation dispositions;
2. 11,448 existing physical-incidence bindings;
3. 468 wrong-signed empty-side no-binding proofs;
4. 288 graph-separated no-binding proofs.

## Physical coordinate rule

Every terminal comparison uses the independently recomputed interval

`physical_t² = coordinate_t² ∩ (1 - source_guard_t²)`.

Raw signed `t` is never compared.  Round174/Round179 source-guard boxes are
therefore explicit byte-pinned inputs in addition to the prescribed
Round286/Round287 terminal dispositions.

## Independent verification

The verifier does not import or execute the producer and never opens any
Round293 artifact.  Before opening the current result or ledger, it:

1. reconstructs all 9,528 relation rectangles from Round268/Round275/
   Round280/Round282/Round283;
2. compares that reconstruction to the frozen Round289 relation table;
3. rebuilds physical terminal support and strict empty cells from
   Round174/Round179/Round286/Round287/Round288/Round292A;
4. byte-pins the complete sealed Round294 package, including its manifest;
5. constructs the full expected four-table candidate object.

Two independent hash seeds produced byte-identical verification JSON.
All **53/53** semantic, re-signed, malformed JSON/gzip, and path-substitution
attacks were rejected.  The suite covers raw-`t`, occupancy-one false binds,
sign reversal, clipped-as-empty, erasure of the four whole-empty relations,
gap-to-occurrence/alias, omitted W2/W3 refinement, reused-cell double
counting, half-cell inflation, Jx/Jy/signature glue, forged area, and every
forbidden seam/component/DSU/maximality/fibre/global credit.

## Strict nonpromotion

- Round295-B adds **zero occurrence IDs** and **zero representation aliases**.
- The formal registry remains **431,208** rows.
- Seam edge, component union, DSU rank reduction, maximality, fibre, global,
  and Jx/Jy same-point glue credits are all **zero**.
- Post-Round294 quotient count remains `null`; expanded-registry DSU status
  remains `NOT_REBUILT`.
- Legacy `63,224` is historical only and is not asserted as the current
  post-Round294 quotient.
- The number `152` denotes directed endpoint cells, never seam edges.

## File seals

- producer: `c970371a5e05a76d22cd41accf98848784413f9ce2c937a3dff47c43b763b86a`
- ledger: `1714945c470607a68c9fb5e323319899faabd187ecbccd00d266ea6f9361007c`
- result file: `b10c5caf9813887b06f2ed49796e02befc8abdc048e6909c2146bfc120e6334a`
- result embedded: `278036958403818507e96c72bbc94cfa0cbbe50a6f0984aecb64125795974536`
- verifier: `648ce97bba19272f2dc26f268d40c12a2dd686ade6a32d273b0b8b371707eaa8`
- verification file: `f823fd7c7a34d39163bc887d6544ea670915e9ecb93fc2a94947f4ee777180a1`
- verification embedded:
  `471e44c13d9c6594c2182185ae5e269746ded6184a6f0d802f629e8287039063`

