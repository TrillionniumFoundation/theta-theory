# CM2 Gates 3/4: charged 2018-step regular-dwell witnesses

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the four positive core-hit branches and the abstract
same-interval `2018`-step dwell contraction  
Strict verdict: **each charged branch contains a positive open subcylinder
whose selected point has 2018 consecutive strict regular post-core
collisions.  This is a local physical no-collision-singularity dwell witness,
not the global native dwell schedule or a common-strong-space operator.**

## 1. Validated point itineraries

On each charged branch choose the interior parameter magnitude

```text
|h|=2^-300 < 2^-220.
```

After replaying the already certified core entrance, an 8192-bit Arb audit
validates the next `2018` first collisions.  A floating pilot proposes each
target only; Arb independently proves that target is strictly hit, every
retained competitor is strictly later, every flight lies in `(0,2)`, and
every collision cosine is strictly above `1/1000`.

Totals are

```text
4 oriented branch points,
2018 post-core regular collisions per branch,
8072 validated regular collisions,
4 immutable itinerary SHA-256 digests.
```

## 2. Positive open subcylinders

Every validated itinerary is a finite system of strict analytic collision
inequalities at an interior `(z,h)` point.  Continuity gives a positive open
parameter subcylinder on which the same complete `2018`-step itinerary holds.
Thus four positive local no-singularity subcylinders exist.

Their radii are not materialized.  Therefore this result provides neither a
quantitative retained fraction nor a weighted injection estimate.

## 3. Relation to the scalar dwell block

The frozen scalar arithmetic remains

```text
b_core^2018 < 3/8,
one same-interval shell cut plus one block < 45/64.
```

The local regular itineraries do not prove that the fixed-core multiplier
survives on the entire subcylinder for all 2018 steps, identify the same
physical interval in both orientation views, or embed the range in one
common strong space.  Hence no native operator composition is promoted.

## 4. Strict frontier

```text
POSITIVE OPEN 2018-REGULAR SUBCYLINDERS:             4 CERTIFIED
VALIDATED POST-CORE REGULAR COLLISIONS:           8072 CERTIFIED

MATERIALIZED SUBCYLINDER RADII:                    NOT CERTIFIED
FIXED-CORE MULTIPLIER SURVIVAL FOR 2018 STEPS:      NOT CERTIFIED
SAME-INTERVAL TWO-VIEW SHELL IDENTIFICATION:        NOT CERTIFIED
GLOBAL NATIVE 2018 DWELL SCHEDULE:                  NOT CERTIFIED
POST-CORE 12108-STEP NO-RECUT DWELL:                NOT CERTIFIED
COMMON STRONG-SPACE RECOVERY OPERATOR:              NOT CERTIFIED
GATE 3 / GATE 4 / GATE 5:                         NOT CERTIFIED
```

The independent replay passes, the fail-closed verifier rejects `25/25`
hostile mutations, and live mode exits `2`.
