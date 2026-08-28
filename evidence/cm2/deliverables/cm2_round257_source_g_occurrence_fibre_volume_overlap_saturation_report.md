# CM2 Round257 — Occurrence-Fibre Volume-Overlap Saturation

## Result

- Reconstructed exact rational open-box containers for all `53,968` local occurrences: `17,192` Round179, `736` Round204, and `36,040` Round208 rows.
- Reconciled every same-chart, same-exact-key pair exposed by a strict x-axis sweep: `729,700` candidates across all `116` keys.
- Rejected `581,592` candidates at the y intersection and `130,392` at the z intersection because the corresponding intersection width is nonpositive.
- Found `17,716` strict positive-volume box overlaps. Every one is already internal to a single Round256 quotient component.
- Found zero cross-component strict positive-volume box overlaps, hence zero new rank-reducing edges in this channel.
- The unified lower-bound quotient remains `74,012` components; `16,204` of them carry at least one occurrence.

## Independent Verification

- The verifier does not import or execute the producer.
- It independently reloads the pinned Round179, Round204, Round208, and Round256 inputs, reconstructs all geometry, repeats the exact rational sweep, and reproduces every positive-overlap and per-key audit row.
- Independent status: `PASS_INDEPENDENT_ROUND257`.
- Hash seeds `257071` and `257929` reproduce byte-identical producer and verifier outputs.

## Strict Boundary

- Round257 exhausts only the same-chart, same-key strict positive-volume container-overlap channel.
- A positive overlap of containers is not promoted to new physical glue unless it crosses components; no such pair exists.
- Zero-volume face contacts, transformed-face contacts, and cross-chart transitions are not promoted by this round.
- Maximal physical-component assignments remain `0 / 53,968`; exhausted exact-key fibres remain `0 / 116`; global dispositions remain `0 / 224,580`.
- Gate5 remains `10 / 18`; CM2 remains `NO-GO_FOR_CLAIM`.

## Required Next

Enumerate distinct-component same-chart boundary-face contacts and accept only those with an exact positive-area common refinement plus strict two-sided return-signature corridors. After that channel is reconciled, audit pinned same-point cross-chart transitions before any maximality promotion.
