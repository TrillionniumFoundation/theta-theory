# CM2 Eighty-First Direct Assault — 2026-07-21

## Scope

Round 81 executes the shortest continuation from Round 80:

1. replace blind dyadic refinement of the 373 difficult rank-three symmetry
   representatives by centered second-order Taylor enclosures and strict
   monotone-corner certification;
2. extract connected local root patches inside every certified root-bearing
   representative tube;
3. reconstruct the complete fixed-`s=0` depth-two DCEL from the certified
   boundary endpoint order and nonintersection atlas;
4. recover every cyclic cell boundary word and test the finite cellular
   commuting square without renaming it the official all-depth Gate 4.

## Rank-Three Centered-Taylor Resolution

The prior adaptive resolver left 373 representative tubes with 85,078
unresolved leaves.  The Round-81 resolver uses a centered Taylor enclosure,
centered gradient bounds, parameterized interval Newton, and strict
monotone-corner extrema.  It closes all 373 representatives with:

- 26,922 interval box tests;
- maximum subdivision depth 5;
- 9,912 unique certified root slabs;
- 272 root-bearing representatives;
- 101 strict false-tube representatives;
- 0 unresolved representatives and 0 unresolved leaves.

After symmetry expansion, the difficult representatives contribute 664
root-bearing physical components and 340 false components.  Together with the
532 already complete graph components from Round 80, the full 1,536-component
seed registry is partitioned exactly as

`1536 = 532 + 664 + 340`.

This closes the carrier-existence classification, not the complete rank-three
face atlas.  Grouping root slabs by closure overlap produces 417 connected
local patches in representative tubes and 1,248 patches after symmetry
expansion.  Cross-tube joining and physical endpoint/intersection certification
remain open.

## Complete Fixed-Depth DCEL

The depth-two DCEL uses the certified order of all stationary, R1, R2, and
time-two tangency endpoints together with the certified noncrossing relations.
It recovers:

- exact f-vector `(V,E,F)=(392,532,164)`;
- Euler identity `392-532+164=24`;
- exact labels `R1=16`, `R2=16`, `Q2=132`;
- 164/164 exact cyclic boundary words;
- 132/132 exact Q2 cyclic boundary words.

The induced cellular chain certificate verifies `partial_1 partial_2 = 0`
cellwise on all 164 cells.  The 532 edges split into 376 stationary exterior
edges and 156 internal physical crosscuts: 32 R1, 32 R2, and 92 tangency.  All
156 internal traces occur twice with opposite orientation, so the duplicate
trace cost before total variation is exactly zero.

This certifies the finite fixed-`s=0` depth-two cellular commuting square.  It
does not certify the same-key stable/material crosswalk or an all-depth family,
so the official Gate-4 score is not promoted.

## RN Frontier

The Round-80/Round-77 finite rank-1/2 RN ledger remains valid with 64 certified
return-face rows.  Rank-three tangency subdivision faces are not renamed return
faces.  There is still no certified rank-three return-face RN row, uniform
rank-transition tail contraction, or all-rank RN summability theorem.

## Cold Audit

The centered-Taylor resolver, root-patch extractor, DCEL generator, cellular
chain certificate, integration manifest, and hostile verifier were rerun from
cold state under `python-flint==0.9.0`; all 6 outputs were byte-identical.  The
independent verifier rejects 16/16 hostile semantic mutations and 4/4 strict
JSON attacks, and verifies every input pin.  All Round-81 Python sources compile
successfully.  The accompanying SHA-256 list pins every Round-81 source,
certificate, audit, and this report.

## Strict State

- Gate 4: `1/7`.
- Gate 5: `10/18`, complete blocks `0`.
- Complete composite gates: `0/5`.
- CM2: `NO-GO_FOR_CLAIM`.

## Next Shortest Route

Join the 1,248 local rank-three root patches across overlapping carrier tubes,
certify their physical endpoints and pairwise intersections, and build the
complete rank-three face quotient.  Only after those faces acquire genuine
F8/F9/F10/F13/F16 and RN return rows should the computation test a physical
rank-transition contraction and an all-rank summability bound.  In parallel,
the fixed-depth DCEL must be lifted to a same-key all-depth stable/material
crosswalk before Gate 4 can be promoted.
