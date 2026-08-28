# CM2 Gates 2/5: all-key maximal-component characteristic boundary

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the 441,280-key return-word envelope, the complete physical
boundary-root grammar, and the invariant standard-curve density cone  
Strict verdict: **the finite unnormalised characteristic-boundary estimate now
covers every candidate key and every maximal connected component, not only
the 24 positive seeds.  Its worst coefficient is not contracting, so the
strong DQ/recovery/PPE/18-field/Kac chain remains fail-closed.**

## 1. The missing set-theoretic step

For a fixed parameter `s` and return-word key `w`, let `D_w(s)` be the open
regular fibre with the declared source chart, selected target, transparent
wall record, and central homogeneity labels.  The preceding root theorem
proved that every physical boundary branch in the exhaustive grammar meets a
canonical unstable curve in at most one isolated point.

That theorem is not seed-dependent.  Both the relative boundary of `D_w(s)`
and the relative boundary of each maximal connected component `M` of
`D_w(s)` lie in the same finite union of:

- signed candidate-tangency sheets;
- endpoint-wall, corner-time, and velocity-zero sheets;
- source/target chart seams; and
- source/target central homogeneity faces.

After coalescing simultaneous roots, deleting `m` boundary points from one
canonical curve leaves at most `m+1` open intervals.  Therefore the union of
all components of a key and every individual maximal component share the
same safe interval upper.  No nonempty-key decision, component enumeration,
or numerical root order is needed for this upper; an empty key contributes
zero.

## 2. Complete key counts and bounds

The four gray source charts each retain 57 targets, and the four white source
charts each retain 55.  Every retained chart-target pair has the frozen 985
candidate wall records.  Hence

```text
gray-source keys:  4*57*985 = 224580,
white-source keys: 4*55*985 = 216700,
all keys:                       441280.
```

The complete physical boundary grammar gives

```text
gray source:  289 roots, at most 290 retained intervals,
white source: 285 roots, at most 286 retained intervals.
```

With the invariant conditional-density ratio `2000/1999`, uniformly for
every `|s|<=1/400`,

```text
Z_*(1_{D_w(s)} F) <= (580000/1999) Z_*(F)  on gray keys,
Z_*(1_{D_w(s)} F) <= (572000/1999) Z_*(F)  on white keys.
```

The same estimates hold with `D_w(s)` replaced by any one of its maximal
connected components.  This closes the previously missing **all-key / all
maximal-component finite characteristic-boundary theorem**.

## 3. Exact nonpromotion

The bound is deliberately not promoted to the remaining interfaces.  After
the certified physical step,

```text
(580000/1999)*(360134800/360493663)
  =208878184000000/720626832337 >1,

(572000/1999)*(360134800/360493663)
  =205997105600000/720626832337 >1.
```

Thus the uniform field-7 characteristic formula is finite but not a Growth
contraction.  Repeating the crude bound through an unbounded number of cuts
would grow exponentially.  It supplies neither a common moving strong-space
atlas nor branch-record `MT_DQ`, `FACE`, hereditary recovery, stable quotient,
PPE, the other 17 operator fields, the three CM2 norm intertwiners, or the
Kac/operator-phase closure.

```text
ALL 441280 KEY CHARACTERISTIC BOUNDS:              CERTIFIED
ALL MAXIMAL COMPONENT CHARACTERISTIC BOUNDS:       CERTIFIED
UNIFORM FINITE FIELD-7 FORMULA:                     CERTIFIED
FIELD-7 GROWTH CONTRACTION:                         NOT CERTIFIED
COMMON STRONG DQ / MT_DQ / FACE:                    NOT CERTIFIED
UNBOUNDED REPEATED RECOVERY:                        NOT CERTIFIED
STABLE QUOTIENT / PPE / COMPLETE 18 FIELDS:         NOT CERTIFIED
THREE NORMS / KAC / OPERATOR PHASE:                 NOT CERTIFIED
GATES 2--5:                                         NOT CERTIFIED
```

## 4. Replay

```bash
PYTHONPATH=deliverables python3 -m py_compile \
  deliverables/cm2_gate25_all_component_characteristic_frontier_cert.py \
  deliverables/cm2_gate25_all_component_characteristic_frontier_verifier.py

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate25_all_component_characteristic_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate25_all_component_characteristic_frontier_verifier.py \
  --self-test

# Expected exit 2: the downstream composite gates remain open.
PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate25_all_component_characteristic_frontier_verifier.py
```
