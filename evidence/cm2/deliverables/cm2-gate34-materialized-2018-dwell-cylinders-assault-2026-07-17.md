# CM2 Gate 4: materialized 2018 dwell and fixed-core refutation

Date: 2026-07-17 (Asia/Shanghai)  
Mode: append-only, fail-closed, 8192-bit Arb interval replay  
Strict verdict: **the four previously existential 2018-step regular dwell
subcylinders now have the explicit common half-width `2^-8000`.  However,
all four boxes strictly leave the frozen 24-core at the first post-core
collision.  Therefore their ordinary regular trajectories cannot directly
realize powers of the fixed open operator `O=T_* o M_core`.  Gate 4 remains
open.**

## 1. Materialized boxes

For each of the two frozen occurrences and each hit/miss side, the certificate
uses the frozen base point and parameter magnitude `|h|=2^-300`, then expands
both base `z` and parameter magnitude by the common half-width

```text
r=2^-8000.
```

All four two-dimensional boxes lie strictly inside the old `2^-220` core-hit
charge.  The labelled coordinate volume is exactly

```text
4*(2r)*(2r)=2^-15996.
```

The candidate common radius `2^-6000` was rejected when its Arb enclosure no
longer maintained the frozen speed lower bound.  It is not promoted.

## 2. Full interval replay

On every entire box, 8192-bit Arb verifies

```text
strict source-to-core entrance:                     4 branches,
strict terminal frozen-core membership:             4 branches,
post-core regular collisions per branch:                  2018,
total interval-validated post-core collisions:             8072,
unique first-collision decisions:                    8072/8072,
flight times in (0,2):                               8072/8072,
collision cosines >1/1000:                           8072/8072.
```

Thus the former statement “positive radius exists by continuity” is upgraded
to four explicit dyadic boxes.

## 3. Fixed-core operator obstruction

The scalar coefficient `b_core` belongs to the substochastic operator

```text
O=T_* o M_core,
```

which clips to the frozen 24-core before every physical step.  Regularity of
an unconstrained orbit does not imply survival under repeated `M_core`.

The same interval replay proves that the first collision after each strict
core entrance is strictly outside every one of the 24 core rectangles.  The
failure time is therefore exactly one post-core collision on all four boxes.

```text
DIRECT IDENTIFICATION OF REGULAR DWELL WITH O^2018: REFUTED ON 4 BOXES
DIRECT IDENTIFICATION WITH O^12108:                 REFUTED ON 4 BOXES
```

This does not refute a future induced first-return operator.  It refutes only
the direct attachment of the existing fixed one-step core multiplier to these
ordinary regular trajectories.

## 4. Corrected frontier

```text
EXPLICIT POSITIVE 2018-DWELL CYLINDERS:               4 CERTIFIED
COMMON HALF-WIDTH:                              2^-8000 CERTIFIED
INTERVAL-VALIDATED POST-CORE COLLISIONS:             8072 CERTIFIED
FIRST POST-CORE EXIT FROM FROZEN CORE:                 4/4 CERTIFIED

ALL 128 BRANCHES HAVE MATERIALIZED 2018 DWELL:      NOT CERTIFIED
12108 FIELD-7 DWELL:                                NOT CERTIFIED
SAME-INTERVAL TWO-VIEW IDENTIFICATION:              NOT CERTIFIED
INDUCED CORE FIRST-RETURN OPERATOR:                  NOT CERTIFIED
COMMON STRONG RECOVERY OPERATOR:                    NOT CERTIFIED
GATE 3 / GATE 4 / GATE 5:                          NOT CERTIFIED
```

## 5. Replay

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_materialized_2018_dwell_cylinders_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_materialized_2018_dwell_cylinders_verifier.py \
  --self-test
```

The verifier rejects `31/31` hostile mutations.  Live mode exits `2` because
the physical induced operator and the composite gates remain open.
