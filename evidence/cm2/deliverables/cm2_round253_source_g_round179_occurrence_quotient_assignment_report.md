# CM2 Round253 — Round179 Occurrence Quotient Assignment

## Result

- Assigned all `17,192 / 17,192` Round179 resolved-child occurrences to exactly one saturated Round252 mixed-sheet quotient component.
- The assignments touch `7,932` Round252 components and all `116` observed exact keys.
- Exactly `748` occurrences map to seeded components and retain their already-certified known-block incidence.
- The other `16,444` occurrences map to unseeded components and receive no known-block or maximality promotion.
- The seeded/unseeded split is exactly identical to the prior attached/unattached occurrence split.

## Frontier Rebuild

- Rebuilt the full `53,968`-row occurrence frontier with an explicit quotient-component assignment field.
- Round179 assignment is complete; Round204 (`736`) and Round208 (`36,040`) remain outside this assignment scope.
- `80 / 116` exact keys now have complete all-gauge occurrence assignment because their local occurrence universe contains only Round179 rows.
- Known-block incidence remains `36,200 / 53,968`; no new incidence is claimed.

## Verification

- Independent verifier status: `PASS_INDEPENDENT_ROUND253`.
- The verifier does not import or execute the producer.
- It independently reconstructs the Round244→Round251→Round252 component lineage, all `17,192` assignments, the full occurrence frontier, and all `116` key rows.
- Hash seeds `253071` and `253929` reproduce byte-identical producer and verifier outputs.

## Strict Boundary

- Quotient-component assignment is not known-block membership and is not maximal-component assignment.
- The `16,444` unseeded Round179 assignments remain occurrence-to-lower-bound-component facts only.
- Maximal physical components remain `0 / 53,968`; exhausted exact-key fibres remain `0 / 116`; global dispositions remain `0 / 224,580`.
- Gate5 remains `10 / 18`; CM2 remains `NO-GO_FOR_CLAIM`.

## Required Next

First merge the four pairs of Round252 quotient components that carry the same already-certified known-block ID. Then assign the resulting uniquely seeded quotient components to the `2,020` compatible Round208 occurrences. The remaining `34,020` Round208 and `736` Round204 occurrences require new explicit physical bridges.
