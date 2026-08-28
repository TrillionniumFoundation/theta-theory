# CM2 Round249 — Exact-Key Quotient-Fibre Frontier Rebuild

## Result

- Assigned all `94,444` mixed-sheet quotient components to exactly one of the `116` observed exact keys.
- Verified memberwise exact-key purity for every assignment:
  - `8,148` inherited Round244 components enriched through Round248;
  - `86,296` new unseeded Round248 wall components.
- The assignments cover `150,876` materialized members: `17,192` resolved occurrences plus `133,684` virtual strata.
- Rebuilt all `116 / 116` exact-key quotient-fibre inventories with exact commitments for components, occurrences, unattached occurrences, and known blocks.

## Fibre Frontier

- Seeded quotient components: `440`; unseeded quotient components: `94,004`.
- Known-connectivity blocks: `7,388`, appearing on `24` keys.
- New Round248 wall components appear on `92` keys.
- The known-block and new-wall key sets intersect on `16` keys, cover `100` keys in union, and leave `16` keys in neither set.
- Every one of the `116` keys still has at least one unattached occurrence and at least one unseeded inherited component.
- No exact-key fibre is globally exhausted.

## Remaining Occurrence Deficits

- `16,444` Round179 resolved-child occurrences across all `116` keys.
- `736` Round204 strict-open-region occurrences across `12` keys.
- `588` Round208 strict-open-region occurrences across `24` keys.
- Total without known-block incidence remains `17,768`; total with incidence remains `36,200 / 53,968`.

## Verification

- Independent verifier status: `PASS_INDEPENDENT_ROUND249`.
- The verifier does not import or execute the producer.
- It independently reconstructs all `94,444` component assignments and all `116` fibre-frontier rows from pinned Rounds179 and 244–248.
- Hash seeds `249071` and `249929` reproduce byte-identical producer and verifier outputs.

## Strict Boundary

- Round249 grants complete quotient-fibre inventory credit, not global occurrence-fibre exhaustion.
- All `94,444` quotient components remain known-connectivity lower bounds with maximality unproved.
- Maximal physical components remain `0 / 53,968`; exhausted exact-key fibres remain `0 / 116`; global dispositions remain `0 / 224,580`.
- Gate5 remains `10 / 18`; CM2 remains `NO-GO_FOR_CLAIM`.

## Required Next

Close the `16,444` Round179, `736` Round204, and `588` Round208 occurrence deficits against the key-pure quotient while saturating physical adjacency before any maximal-component or global-fibre promotion.
