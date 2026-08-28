# CM2 Round277 depth-8 active-graph face-edge closure probe

Status: `PASS_INDEPENDENT_ZERO_CREDIT_PROBE`

## Purpose

The depth-8 safe-pruned replay left 32,668 same-signature positive-common-face
candidate edges.  A finite-depth miss was never interpreted as an absence.
This continuation instead reused the Round274/275 active-factor normal form and
then materialized an explicit strict witness for every candidate edge.

## Exact active-factor strategy

Every depth-8 terminal cell is treated in one of these ways:

1. A strict complete signature different from the requested signature is
   pruned on that certified closed cell.
2. A single outgoing-chart or integer-wall equality with strict tangent
   derivatives is reduced to a coordinate-monotone graph.  Strict extremal
   signs classify the cell as a regular graph crossing or a zero-set absence.
3. Exact-zero tangent derivatives are treated as structural independence, not
   interval uncertainty.
4. Source/hit double-factor wall cells and `p=+/-1` square-root derivative
   endpoints remain fail-closed at cell level unless another certified cell
   already supplies the requested edge witness.

The complete cell census over the 32,668 geometric face groups is:

- strict different-signature cells: **644,088**
- regular monotone graph cells: **89,384**
- zero-set absence cells by strict extrema: **138,448**
- `p=+/-1` tangent-derivative endpoint cells retained fail-closed:
  **27,580**
- source/hit double-factor cells retained fail-closed: **256**

At edge level, 32,416 candidates already had the requested signature on a
strict active-factor side.  The remaining 252 candidates were exactly four
symmetric `G:N/G:S -> W` families at `p=+/-1`.

## Explicit positive-area materialization

An extremal point alone was not accepted as an edge witness.  Each of the
32,416 regular candidates was shrunk to a positive rational face rectangle on
which the frozen Round174 evaluator certifies the entire requested signature.
The deepest tangent shrink used was 22.

For each of the 252 endpoint candidates, a strict requested boundary segment
at `p=+/-1` was first certified.  That segment was then thickened inward in the
`p` direction until the evaluator certified a positive-area rational wedge.
The deepest endpoint inward depth was 33.  Acceptance therefore does not rely
on a limit argument or on declaring an unresolved endpoint absent.

Every face patch was additionally thickened in the common-face normal
direction into both incident leaves.  The result is:

- input depth-8 residual candidates: **32,668**
- regular active-side positive patches: **32,416**
- `p=+/-1` endpoint-wedge positive patches: **252**
- total strict positive-area face patches: **32,668**
- correctly oriented inward corridor witnesses: **65,336**
- remaining fail-closed candidate edges: **0**

The independent verifier rebuilt the frozen candidate universe and evaluator,
then checked exact face containment, positive tangential area, complete
signature equality, leaf containment, one negative-side corridor, one
positive-side corridor, and positive normal width.  It passed **32,668 /
32,668** rows and **65,336 / 65,336** corridors.

## Combined Round277 probe census

Together with the corrected depth-4 and depth-8 patch probes:

- depth-4 patch/corridor witnesses: **240,932**
- additional depth-8 patch/corridor witnesses: **57,124**
- active-graph/endpoint continuation witnesses: **32,668**
- total candidate face edges with explicit patch and two corridors:
  **330,724 / 330,724**
- total inward corridor witnesses: **661,448**
- candidate-edge residual: **0**

This is still a probe-level local geometry result.  It does not itself
materialize the 295,976 unmaterialized occurrence-region atom candidates,
contract the four artificial W-tail aliases, union the DSU, attach the 152
true-seam patches, or prove component maximality.

Strict non-promotion remains:

- expanded-occurrence credit: **0**
- component-edge credit: **0**
- maximality credit: **0**
- `Jx/Jy` glue credit: **0**
- CM2: `NO-GO_FOR_CLAIM`

## Frozen probe artifacts

- active-graph strategy:
  `cm2_round277_source_g_depth8_residual_active_graph_strategy_probe.py`
- active-graph result SHA256:
  `b4d810725e2f2ec761f9819c41ad477db0e25fc35e3c12ddd1e1ec8a3ac57308`
- patch/corridor materializer:
  `cm2_round277_source_g_depth8_active_graph_patch_corridor_materialization_probe.py`
- materializer result SHA256:
  `e04f0906f9d8b3b4bd16d553a4edacf3a8d20b5b6828467d38f64d30ee475f75`
- witness ledger SHA256:
  `8a29604c937ea63fd1274ded5b131a3de8717b026aa576926e0d035754985f43`
- witness rows SHA256:
  `5812c98882e67cc199f474f8252e3c2edee06df700bfc521ff9c3497e38aeea7`
- independent verifier:
  `cm2_round277_source_g_depth8_active_graph_patch_corridor_materialization_probe_verifier.py`
- verification result SHA256:
  `feeebccb84012be31ce6b16971588116ff1a48fde8162ecc2e79377a83105dae`

## Next safe dependency order

1. Formalize the four W-tail artificial-split alias witnesses.
2. Materialize the 295,976 occurrence-region atoms with their complete
   provenance and true support.
3. Freeze the 330,724 face witnesses with a producer/verifier pair and only
   then apply their DSU rank reductions.
4. Apply Round275 reverse-rechart regions, bind the 152 true-seam patches, and
   recompute the final quotient.
5. Only after that proceed to frontier maximality, 116 exact-key fibres, and
   the 224,580 dispositions.
