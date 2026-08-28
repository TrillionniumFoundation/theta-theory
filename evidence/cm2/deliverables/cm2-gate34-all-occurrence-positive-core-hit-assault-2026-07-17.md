# CM2 Gates 3/4: all-occurrence positive core-hit cylinders

Date: 2026-07-17 (Asia/Shanghai)  
Mode: append-only, fail-closed, binary64 proposal plus independent Arb admission  
Strict verdict: **all 64 maximal reference occurrences and all 128 oriented
hit/miss branches now possess an explicit positive all-scale cylinder ending
in a strict frozen-core interior.  This is not a normalized physical hit
fraction, a first-stopping theorem, a cemetery estimate, or a strong recovery
operator.  Gates 3 and 4 remain open.**

## 1. Complete charged registry

The frozen two-occurrence result is imported unchanged.  A deterministic
binary64 shooter proposes one finite collision word for each of the other 62
occurrences.  Floating output has proposal status only.  Each proposed word is
then independently replayed on both actual-parameter sides with 2048-bit Arb.

The admitted registry is

```text
maximal reference occurrences:                    64/64,
oriented hit/miss branches:                     128/128,
new Arb-validated occurrences/branches:          62/124,
new unique regular suffix/post-suffix flights:       800,
maximum certified core-entrance word length:          20.
```

Every listed collision is the unique first collision on the entire parameter
box, and every terminal state lies strictly inside one frozen core rectangle.

## 2. Explicit cylinders

The common base-coordinate and parameter half-width power varies by
occurrence:

```text
power 80:   32 occurrences,
power 100:   8 occurrences,
power 120:  16 occurrences,
power 180:   2 occurrences,
power 200:   4 occurrences,
power 220:   2 frozen occurrences.
```

The post-suffix entrance-word histogram is

```text
2:22, 3:10, 4:8, 7:8, 8:4, 9:4, 16:2, 19:4, 20:2.
```

The labelled base-parameter coordinate volume of the 64 cylinders satisfies

```text
2^-153 < V_labelled < 2^-152.
```

This coordinate volume is not identified with collision-SRB mass.

## 3. Strict boundary

The result certifies one positive box per reference occurrence, not the whole
maximal row.  Intermediate states were not materialized as first visits to the
core complement, so the displayed word length is an entrance bound rather
than a first core stopping time.  No normalized hit fraction, quantitative
cemetery tail, post-core dwell, or common strong-space operator follows.

```text
POSITIVE ALL-SCALE CORE-HIT OCCURRENCES:           64 CERTIFIED
POSITIVE ALL-SCALE ORIENTED BRANCHES:             128 CERTIFIED
MAXIMUM CORE-ENTRANCE WORD LENGTH:                 20 CERTIFIED

FIRST CORE STOPPING TIME:                          NOT CERTIFIED
NORMALIZED SELECTED CORE-HIT FRACTION:              NOT CERTIFIED
POST-CORE 2018/12108 DWELL:                        NOT CERTIFIED
COMMON STRONG DQ/MT_DQ/FACE/RECOVERY:              NOT CERTIFIED
GATE 3 / GATE 4:                                   NOT CERTIFIED
```

## 4. Replay

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_all_occurrence_positive_core_hit_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_all_occurrence_positive_core_hit_verifier.py \
  --self-test
```

The verifier rejects `31/31` hostile mutations.  Live mode exits `2` because
the composite gates remain open.
