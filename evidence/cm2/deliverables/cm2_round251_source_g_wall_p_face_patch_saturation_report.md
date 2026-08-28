# CM2 Round251 — Wall p-Face Patch Saturation

## Result

- Reconstructed the `50,576` Round248 wall cells inside `2,640` wall roots and audited all same-chart, same-target p-face root pairs.
- Certified `3,240` strict same-signature p-face patches across `408` root pairs by explicit two-sided positive-volume common refinements.
- Added all `3,240` physical adjacency edges; `584` reduce quotient rank and `2,656` are independently certified redundant edges.
- Reduced the conservative mixed-sheet quotient from `82,620` to `82,036` components.

## Patch Census

- Patch-depth histogram: `2,832` at `p1:t0:0:s0:0`, `204` at `p1:t1:0:s0:0`, and `204` at `p1:t1:1:s0:0`.
- Exact common patch-area sum: `5,417,439 / 3,276,800,000`.
- Exact left and right corridor-volume sums: `3,574,161 / 134,217,728,000` each.
- Accepted source-pair classes include resolved descendants, single-endpoint graph cells, and double-endpoint arrangement cells.
- No edge is inferred from key equality, coordinate touch, or signature equality without a strict physical patch.

## Saturated Quotient

- Cumulative virtual-stratum nodes remain `133,684`.
- Cumulative physical adjacency edges increase from `59,212` to `62,452`.
- The final quotient has `440` seeded and `81,596` unseeded components.
- `7,932` quotient components inherit a Round244 seed; `74,104` remain wall-only p-face-saturated components.
- Cumulative virtual-stratum known-block incidences remain `316`.

## Fibre Refresh

- Rebuilt all `116 / 116` exact-key quotient-fibre inventories after p-face saturation.
- Every quotient component remains memberwise exact-key pure.
- No exact-key fibre is globally exhausted.
- Occurrence incidence remains `36,200 / 53,968`; the unresolved occurrence deficit remains `17,768`.

## Verification

- Independent verifier status: `PASS_INDEPENDENT_ROUND251`.
- The verifier does not import or execute the producer.
- It independently reconstructs wall cells and p-face candidates, reruns strict two-sided patch checks, rebuilds the DSU quotient, and refreshes all `116` fibre rows.
- Hash seeds `251071` and `251929` reproduce byte-identical producer and verifier outputs.

## Strict Boundary

- Round251 grants additional physical known-connectivity and refreshed quotient-fibre inventory credit.
- The `82,036` quotient components remain lower bounds on physical components; maximality is unproved.
- Maximal physical components remain `0 / 53,968`; exhausted exact-key fibres remain `0 / 116`; global dispositions remain `0 / 224,580`.
- Gate5 remains `10 / 18`; CM2 remains `NO-GO_FOR_CLAIM`.

## Required Next

Materialize the remaining same-chart wall s-face and cross-root t-face strict patches, then close the `17,768` occurrence deficits before any maximal-component or global-fibre promotion.
