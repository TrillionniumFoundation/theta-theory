# CM2 Round248 — Wall Finite-Key Retained Quotient

## Result

- Materialized all `2,640` Round236 wall retained roots and closed the remaining Round239 interface frontier.
- Reconstructed exactly `88,936` positive-volume bulk pieces:
  - `12,200` Round234 exact resolved descendants;
  - `76,656` Round235 single-endpoint graph-side branches;
  - `48` Round236 double-endpoint arrangement branches;
  - `32` Round236 crossing-discharge bulks.
- Materialized exactly `38,360` lower-dimensional wall sheets:
  - `38,328` single-endpoint graph sheets;
  - `32` source/target sheets from the `16` double-endpoint boxes.
- Every endpoint sheet is half-open owned by the event-absent bulk because endpoint event time is outside the open interval `(0,1)`.
- The positive-volume piece count and candidate exact-key set are conserved independently for every root: `408` one-key, `2,216` two-key, and `16` three-key roots.

## Physical Contacts

- Every wall root has exactly one positive-area contact to its resolved sibling.
- `2,632` contacts use an exact Round234 dyadic descendant face.
- The remaining `8` `p`-interface contacts use independently certified `256`-bit dyadic corridors.
- All `8` interval contacts close at `p` depth `1`, `t` depth `1`, on the lower `t` side.
- Exact key equality alone supplies no edge; every accepted edge has a positive-area face and, where needed, a strict positive-volume corridor.

## Quotient Delta

- New wall virtual-stratum nodes: `127,296`.
- New mixed-sheet edges: `41,000`.
- New unseeded conservative quotient components: `86,296`, containing `124,656` nodes.
- New-component size histogram: `47,952` of size `1`, `38,328` of size `2`, and `16` of size `3`.
- Cumulative virtual-stratum nodes: `133,684`.
- Cumulative mixed-sheet edges: `47,388`.
- Conservative mixed-sheet quotient components: `94,444`, comprising `8,148` inherited components and `86,296` new unseeded components.
- Newly touched inherited components: `1,480`; overlap with previously touched inherited components: `0`; cumulative touched inherited components: `5,760 / 8,148`.
- New occurrence-to-known-block incidences: `0`; occurrence incidence remains `36,200 / 53,968`.
- Remaining Round239 unaccepted-interface frontier: `0`.

## Verification

- Independent verifier status: `PASS_INDEPENDENT_ROUND248`.
- The verifier does not import or execute the producer.
- It independently reconstructs all `88,936` bulks, `38,360` sheets, `2,640` contacts, `2,640` root commitments, all inherited-component enrichments, and the `86,296`-component commitment.
- It reruns all `8` strict interval contacts with the frozen `256`-bit kernel.
- Hash seeds `248071` and `248929` reproduce byte-identical producer and verifier outputs.

## Strict Boundary

- Closing all `8,500` Round239 unaccepted interfaces is local retained-stratum coverage, not global occurrence incidence or fibre exhaustion.
- The `94,444` quotient components are conservative known-connectivity lower bounds, not certified maximal physical components.
- Known-connectivity blocks remain `7,388`.
- Maximal physical components remain `0 / 53,968`; exhausted exact-key fibres remain `0 / 116`; global dispositions remain `0 / 224,580`.
- Gate5 remains `10 / 18`; CM2 remains `NO-GO_FOR_CLAIM`.

## Required Next

Rebuild all `116` exact-key fibres over the expanded mixed-sheet quotient, then prove component maximality and close the remaining occurrence incidence without treating local interface closure or key equality as global glue.
