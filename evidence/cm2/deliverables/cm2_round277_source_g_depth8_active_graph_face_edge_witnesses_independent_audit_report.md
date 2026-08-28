# CM2 Round277 depth-8 active-graph witness independent audit

Status: `PASS_INDEPENDENT_ZERO_CREDIT_AUDIT`

## Verdict

The explicit witness ledger was consumed as inert bytes and audited row by
row against the frozen 32,668-candidate depth-8 residual universe.  No local
false positive or remaining candidate-level false negative was found:

- **32,416** regular active-side witnesses passed;
- **252** `p=+/-1` endpoint-wedge witnesses passed;
- **32,668 / 32,668** exact positive-area face patches passed;
- **65,336 / 65,336** positive-volume inward corridors passed;
- residual candidate edges in this frozen depth-8 universe: **0**.

This verdict is strictly local.  It grants no occurrence, component, rank,
quotient, maximality, fibre, disposition, seam, or `Jx/Jy` credit.

## Exact candidate partition

The audit independently checked that:

- the source residual ledger contains 32,668 unique candidate indices;
- the materialized ledger contains exactly the same sorted indices, with no
  duplicate or orphan;
- the 252 endpoint-wedge indices are byte-for-byte the same set as the prior
  252 fail-closed active-graph tail indices;
- the other 32,416 indices are exactly the prior regular active-side set;
- the two sets are disjoint and exhaustive.

This is the required distinction between the two stages:

1. The active-side strategy probe reported a strict requested extremal side,
   but did not itself materialize a face edge.
2. The current witness ledger gives an exact rational positive-area face
   patch and two exact positive-volume inward corridors for every row.

Only the second object is an explicit local geometric witness.  It is still
zero-credit until occurrence atoms, provenance, and the formal DSU producer
and verifier are frozen.

## Row-by-row geometric checks

For every row, the independent audit:

- rebuilt its candidate leaf pair, chart, target, face axis, face coordinate,
  overlap rectangle, and requested complete-signature hash;
- parsed every rational coordinate canonically;
- checked two strictly positive tangential widths and containment in the
  common face of both incident leaf closures;
- recomputed the full Round174 dynamic signature on the entire closed face
  patch;
- reconstructed the depth-8 source cell from its exact refinement path;
- checked the named single active reason on that source cell;
- reconstructed the dyadic tangent shrink or endpoint inward thickening and
  matched it byte-for-byte to the recorded patch;
- for endpoint rows, recomputed the requested signature on the strict
  `p=+/-1` boundary segment before accepting its positive-area inward wedge;
- reconstructed both dyadic normal widths from the incident leaf spans;
- checked exact leaf containment, one negative-side and one positive-side
  orientation, positive normal width, identical tangential patch, and the
  requested full signature on each corridor.

The active-reason census was:

- outgoing-chart seam: **31,372**;
- wall `X=-1,0,1`: **172, 304, 172**;
- wall `Y=-1,0,1`: **172, 304, 172**.

For all 1,296 wall witnesses, the source factor on the selected source cell
was independently strict: **648 negative + 648 positive**.

## Double-active and exact-zero safety

The earlier active-cell replay contained 256 cells where the source and hit
wall factors both remained active.  They belong to 64 candidate groups.
The audit confirms the following strict interpretation:

- all 256 cells remain fail-closed at cell level;
- none is used as an absence certificate;
- none is used as the source cell for a materialized witness;
- all 64 affected candidate groups are accepted only through a separate
  source-strict positive face patch and two corridors.

Exact-zero tangent derivatives were also separately replayed.  All 35,328
such terminal cells arise from target-`G` geometry and the exact algebraic
identity `d/ds=0`: target-`G` centers and the relevant outgoing/hit factors
are independent of `s`.  This is not an interval-overwrap shortcut.  Of
those cells, 35,072 have strict extremal certificates; the 256 double-active
wall cells remain fail-closed.

## False-positive / false-negative verdict

- local false positives in the 32,668 explicit witness rows: **none found**;
- candidate-level false negatives remaining in the frozen 32,668 depth-8
  residual universe: **none**;
- unresolved cell-level absences promoted from finite depth, endpoint
  singularity, or double-active overwrap: **none**.

The result does not assert that every active arrangement cell has been
globally disposed.  It proves the narrower fact needed here: every frozen
candidate edge has at least one explicit same-signature positive face patch
with matching open corridors on both incident sides.

## Artifacts and hashes

- witness ledger SHA256:
  `8a29604c937ea63fd1274ded5b131a3de8717b026aa576926e0d035754985f43`
- witness rows SHA256:
  `5812c98882e67cc199f474f8252e3c2edee06df700bfc521ff9c3497e38aeea7`
- independent audit source SHA256:
  `ce45fe36c1910eb3f9d80e146ed8fceec119f1911e1806289de6b7c74e0e81ed`
- independent audit result SHA256:
  `afe5db516939ff4dfb654ccb9ca260da2a5f8812d4865069d0be857b264ff4ad`
- wall source-factor audit result SHA256:
  `93b45ed1633b0255dda4b8cc09b94cfa3d10ad2162ba29fd32513f37a404809f`
- exact-zero derivative audit result SHA256:
  `b7d72d65c068603f32c4ef2b2d2a5f1cbdb091927226a9f226880ce883f5bf0d`
- structural partition audit result SHA256:
  `403cf17e8857dd98ed297b1818ba6378abf501ae95cbd97d82b303557045ce35`

Strict state remains:

- expanded-occurrence credit: **0**;
- component-edge / rank-reduction credit: **0**;
- maximality credit: **0**;
- CM2: `NO-GO_FOR_CLAIM`.
