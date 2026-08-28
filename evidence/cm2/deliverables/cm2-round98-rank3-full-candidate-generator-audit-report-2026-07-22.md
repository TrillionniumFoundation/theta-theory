# CM2 Round 98 — full-candidate generator-consumption audit

Date: 2026-07-22 (Asia/Shanghai)

## Critical finding

`cm2_round92_rank3_competitor_event_isolation_cert.py` creates
`translated_candidate_ids(...)` as a generator, tests
`tangent_target not in candidate_ids`, and then iterates the same generator.
Python membership testing consumes the generator through the tangent target.
Every candidate preceding that target is therefore omitted from the later root
order loop.

Across the historical Round93/94 point registry, the omitted prefix contains
between 15 and 57 candidate IDs per probe.

## Corrected full-table replay

Round 98 materializes the translated candidate sequence before membership
testing and replays every omitted and retained third candidate at 512 bits:

```text
audited probes:                         10,112
  Round93 probes:                        8,320
  Round94 transferred probes:            1,792
corrected physical probes:               1,536
corrected occluded probes:               8,576
rays with at least one corrected occlusion: 57/65
rays whose audited probes all remain physical: 8/65
```

Independent 640-bit replay preserves the complete per-probe status and earlier
candidate histogram.

## Invalidation boundary

The following claims are withdrawn:

- Round93's `8,320/8,320` physical-prefix probe conclusion;
- Round94's transferred physical-prefix terminal census;
- the interpretation of Round95 intervals as physical prefixes.

Round95's branch-pinned reverse-coordinate coverage remains valid as an
**algebraic branch** statement.  Round96 was the first layer to materialize the
full candidate table and its large third-competitor residual was a symptom of
this bug, not merely a difficult near-root estimate.

No global gate had been promoted by Rounds 93--97, so the strict gate vector
and `CM2=NO-GO_FOR_CLAIM` remain unchanged.

## Required rebuild

Rebuild the rank-three exterior continuation from the last trusted registered
ports using an immutable tuple candidate table.  Terminate each branch at its
first corrected earlier-owner event, then reconstruct the physical face
quotient.  A regression check must assert that candidate membership does not
change the iterable later traversed.

