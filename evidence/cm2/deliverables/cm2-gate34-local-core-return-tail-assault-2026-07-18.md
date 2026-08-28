# CM2 Gate 4: local post-core return and finite-horizon tail

Date: 2026-07-18 (Asia/Shanghai)  
Mode: append-only, fail-closed, 8192-bit Arb interval replay  
Strict verdict: **three of the four materialized `2^-8000` source-current
boxes have strict finite first returns to the frozen 24-core, while the fourth
is a strict excursion survivor through time 2018.  This is a local labelled
coordinate ledger, not the full induced operator or a global cemetery tail;
Gate 4 remains open.**

## 1. Whole-box first returns

Starting at each strict core entrance, every one of the `4*2018=8072`
post-core states is classified against all 24 core rectangles.  No interval
classification is unresolved.

```text
occ:c5fde0378e6e76eec93a0ceb | hit
    first return 545 -> core:a968ac5f...; another core hit at 1604,

occ:c5fde0378e6e76eec93a0ceb | miss
    first return 1531 -> core:2b055512b...,

occ:f2b4833eb8dccd403eec3485 | hit
    no core return through 2018,

occ:f2b4833eb8dccd403eec3485 | miss
    first return 649 -> core:918cc822d....
```

All `8072` collisions remain unique and regular on their entire boxes.  The
classification ledger contains `8068` strict outside-core states and four
strict core re-entry states.

## 2. Exact local labelled-coordinate tail

The four boxes have equal labelled coordinate volume `2^-15998`.  On their
labelled disjoint union only, the exact tail of

```text
tau_C^+ = inf{n>=1:T^n(x) belongs to C_24}
```

is

```text
0 <= n <= 544:       P_label(tau_C^+>n) = 1,
545 <= n <= 648:     P_label(tau_C^+>n) = 3/4,
649 <= n <= 1530:    P_label(tau_C^+>n) = 1/2,
1531 <= n <= 2018:   P_label(tau_C^+>n) = 1/4.
```

The finite-return labelled volume is `3*2^-15998`; the unresolved survivor
volume is `2^-15998`.  The singular-cemetery fraction through this finite
horizon is zero because every listed collision is regular.

## 3. Scope guard

These are `(z,h)` source-current parameter boxes.  For fixed `h`, each is a
one-dimensional source curve inside a core chart; it is not a full
two-dimensional collision-core rectangle.  Therefore the three returning
cylinders do not define a complete induced transfer branch.  The survivor is
only `tau_C^+>2018`; it is not certified nonreturning cemetery.

```text
LOCAL FIRST-RETURN CURRENT CYLINDERS:                 3 CERTIFIED
LOCAL tau_C^+>2018 SURVIVOR BOXES:                   1 CERTIFIED
LOCAL LABELLED RETURN FRACTION BY 2018:            3/4 CERTIFIED
SINGULAR CEMETERY THROUGH 2018 ON FOUR BOXES:         0 CERTIFIED

FULL 24-CORE INDUCED OPERATOR:                  NOT CERTIFIED
GLOBAL COLLISION-SRB EXCURSION/CEMETERY TAIL:    NOT CERTIFIED
NEW STRONG LASOTA--YORKE COEFFICIENT:            NOT CERTIFIED
COMMON TWO-VIEW RESTRICTION:                     NOT CERTIFIED
NATIVE GLOBAL 2018/12108 DWELL:                  NOT CERTIFIED
GATE 3 / GATE 4 / GATE 5:                       NOT CERTIFIED
```

The old fixed-core coefficient `b_core` is not reused: all four source boxes
leave the core at the first post-core collision, so their ordinary excursion
itineraries are outside the domain of repeated fixed-core clipping.

## 4. Replay

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_local_core_return_tail_verifier.py --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_local_core_return_tail_verifier.py --self-test
```

Replay and integrity pass.  The verifier rejects `43/43` hostile mutations;
live mode exits `2` by the unchanged Gate-4 verdict.
