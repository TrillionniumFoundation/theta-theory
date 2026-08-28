# CM2 Round242 — Outgoing Graph Existence Stratum Materialization

## Result

- Audited all `3,136` post-Round240 `OUTGOING_SEAM_GRAPH_SHARED_KEY` interfaces.
- Replaced the Round233 “regular graph if present” status with an exhaustive existence disposition:
  - `2,872` roots have no outgoing-seam zero set on the whole retained root.
  - `264` roots contain a certified positive-2D unique graph patch.
- The zero-absence roots are covered by `8,400` strict dyadic base-partition leaves.
- The `264` graph patches use the frozen rule `E or W owns; N or S excludes`.
- No graph-existence root remains unresolved.

## Method

- Every root has a strict `t` derivative and a strict `p` derivative.
- Roots with a strict `s` derivative use deterministic `p/s` alternating splits.
- Other roots use deterministic `p`-only splits while retaining the full closed `s` interval.
- Same strict signs on both `t` faces prove zero absence.
- Opposite strict signs on the two `t` faces, together with the strict `t` derivative, prove one unique graph point over every point of a positive-area closed base rectangle.
- Maximum local split depth reached is `15`; the configured hard limit is `24`.

## Verification

- Independent verifier status: `PASS_INDEPENDENT_ROUND242`.
- The verifier does not import or execute the Round242 producer.
- It rebuilds all `3,136` root dispositions, all `8,400` zero-absence leaves, and all `264` transition patches.
- Hash seeds `242071` and `242929` reproduce byte-identical producer and verifier output.

## Strict Boundary

- The `264` rows are local positive-2D transition patches, not exhaustive whole-root zero sets.
- New known-block incidences: `0`.
- Global incidence remains `35,908 / 53,968`; unattached occurrences remain `18,060`.
- Maximal physical components: `0 / 53,968`.
- Exhausted exact-key fibres: `0 / 116`.
- Gate5 remains `10/18`.
- CM2 remains `NO-GO_FOR_CLAIM`.

## Required Next

Map only physically certified positive-area or positive-volume contacts into the mixed-sheet quotient. Exact-key equality alone remains forbidden as glue.
