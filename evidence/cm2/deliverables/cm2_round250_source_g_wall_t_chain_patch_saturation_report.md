# CM2 Round250 — Wall t-Chain Patch Saturation

## Result

- Reconstructed all `50,576` Round248 wall-chain cells and their `47,936` internal t-boundaries.
- Certified `11,824` same-signature adjacent-cell boundaries by explicit two-sided positive-volume patches at 256-bit precision.
- Rejected the remaining `36,112` boundaries because their full return signatures differ; no key-only glue was used.
- Added exactly `11,824` physical adjacency edges to the mixed-sheet quotient.
- Reduced the conservative known-connectivity quotient from `94,444` to `82,620` components.

## Patch Census

- `11,184` accepted boundaries use a depth-1 t-split with the full base patch.
- `640` accepted boundaries use a depth-1 t-split with the lower-left base quadrant.
- Exact common patch-area sum: `36,751 / 102,400`.
- Exact left and right corridor-volume sums: `8,467,149 / 209,715,200,000` each.
- All accepted edges reduce quotient rank and lie inside the `2,640` inherited wall contact classes.
- No accepted edge creates a new-only wall-chain cycle.

## Saturated Quotient

- Cumulative virtual-stratum nodes remain `133,684`.
- Cumulative physical adjacency edges increase from `47,388` to `59,212`.
- `15,680` wall nodes attach to inherited components:
  - `14,464` positive-volume wall bulks;
  - `1,216` half-open wall sheets.
- The remaining `111,616` wall nodes form `74,472` new saturated wall components:
  - `74,472` bulk nodes;
  - `37,144` sheet nodes.
- The final quotient has `440` seeded and `82,180` unseeded components.

## Fibre Refresh

- Rebuilt all `116 / 116` exact-key quotient-fibre inventories after saturation.
- Every quotient component remains memberwise exact-key pure.
- No exact-key fibre is globally exhausted.
- Occurrence incidence remains `36,200 / 53,968`; the unresolved occurrence deficit remains `17,768`.

## Verification

- Independent verifier status: `PASS_INDEPENDENT_ROUND250`.
- The verifier does not import or execute the producer.
- It independently reconstructs all wall cells and boundaries, reruns every accepted 256-bit two-sided patch, rebuilds the DSU quotient, and refreshes all `116` fibre rows.
- Hash seeds `250071` and `250929` reproduce byte-identical producer and verifier outputs.

## Strict Boundary

- Round250 grants additional physical known-connectivity and refreshed quotient-fibre inventory credit.
- The `82,620` quotient components remain lower bounds on physical components; maximality is unproved.
- Exact-key equality alone is never used as glue.
- Maximal physical components remain `0 / 53,968`; exhausted exact-key fibres remain `0 / 116`; global dispositions remain `0 / 224,580`.
- Gate5 remains `10 / 18`; CM2 remains `NO-GO_FOR_CLAIM`.

## Required Next

Materialize the remaining within-cell and p-interface physical adjacency for the `74,472` new wall components, then close the `16,444` Round179, `736` Round204, and `588` Round208 occurrence deficits before any maximal-component or global-fibre promotion.
