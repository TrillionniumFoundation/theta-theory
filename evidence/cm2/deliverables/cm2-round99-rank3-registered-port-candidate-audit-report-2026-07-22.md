# CM2 Round 99 — immutable registered-port candidate audit

Date: 2026-07-22

## Scope

Round 99 replays all 3,212 Round87 non-source registered ports from their frozen continuation slabs.  It replaces the consumed `translated_candidate_ids(...)` generator with an immutable complete tuple before membership testing or competitor iteration.

## Corrected census

- Audited registered ports: **3,212 / 3,212**.
- Historical locally physical ports: **945**.
- Corrected locally physical ports: **120**.
- Corrected locally nonphysical ports: **3,092**.
- Historical physical labels changed to earlier-owner occlusion: **825**.
- Corrected event partition:
  - behind second owner: **980**;
  - after `TAU_MAX`: **432**;
  - occluded by an earlier third owner: **1,680**;
  - physical next tangency: **120**.
- The historical membership test consumed between **1 and 57** candidates before the subsequent loop.

The 120 surviving ports occupy exactly **12 oriented projective branches**: four branches with 16 ports each and eight branches with 7 ports each.

## Consequences

The following inputs are withdrawn:

- the Round87 set of 945 locally physical registered ports;
- the Round89 projective gap closure built from those ports;
- the Round90 tracked residual closure built from the Round89 branches.

Round98 already withdrew the later Round93–97 physical-prefix interpretations.  Round95 remains usable only for its algebraic `q -> (t,p)` reverse-coordinate coverage.

No global gate is rolled back because none of these rounds promoted a gate.  The strict gate vector remains Gate1 open, Gate2 `0/17`, Gate3 open, Gate4 `1/7`, Gate5 `10/18` with zero complete blocks, composite `0/5`; CM2 remains `NO-GO_FOR_CLAIM`.

## Verification

- Producer precision: **512 bits**.
- Independent replay precision: **640 bits**.
- Full audit-row digest and all summary histograms agree.
- Hostile semantic mutations rejected: **3/3**.
- Strict JSON rejects duplicate keys and nonfinite constants.
- Python compilation and SHA-256 inventory pass.

## Next strict step

Treat the 120 surviving ports as the only trusted registered-port seeds.  For every incident historical registered arc whose opposite endpoint was corrected to occluded, isolate the first equality between the designated tangent flight and the immutable-table earliest competitor flight.  Those certified occlusion endpoints, together with genuine source-boundary endpoints, are required before rebuilding the rank-3 physical face quotient.

