# CM2 Gate 3: critical graph coordinate export and physical-future exclusion

Date: 2026-07-16 (Asia/Shanghai)  
Frozen input: cancellation-free interval-frontier stack  
Strict verdict: **the 888 conservative critical graph leaves are exported
coordinate by coordinate and all are removed from the physical future-face
frontier: 840 have strict `Delta` sign on the tighter mean-value enclosure and
48 have a strict nonphysical tangent time.  They contribute zero current and
zero FACE charge.  The surviving untyped count falls from 1,052 to 164;
complete current, DQ/MT_DQ/FACE and Gate 3 remain `NOT_CERTIFIED`.**

## 1. Exact coordinate replay

The frozen fifteenth stack retained only hashes for the descendants of its
444 critical-candidate tasks.  This append-only pass repeats the identical
finite subdivision and explicitly exports every leaf:

```text
coarse candidate tasks                 444
critical audit calls                  3196
strict-Delta excluded leaves           932
strict-Delta_t conservative graphs     888
regular folds                            0
unresolved leaves                        0.
```

The 888 graph coordinates, candidates, derivative enclosures and normalized
slope ceilings have their own immutable ledger SHA in the manifest.

## 2. Re-evaluation of the conservative graphs

The predecessor called a leaf a graph whenever its natural `Delta` enclosure
met zero and `Delta_t` had a strict sign.  That was a safe outer cover, not a
claim that a zero or physical collision existed.

On the same full closed rectangles, a dependency-reduced first-order
mean-value enclosure gives:

```text
Delta has strict sign                            840
Delta may meet zero but tangent time is <0         48
physical-first graph                               0
untyped graph retained                              0.
```

The second class is excluded physically only because its entire candidate
tangent-time projection is strictly behind the current collision.  No claim
is made from a merely ambiguous time interval.  Thus the full 888-leaf class
contains no physical future face and contributes exactly zero to the marked
current, `FACE_2CUT`, and `FACE_TIME`.

## 3. Updated graph/current frontier

Removing the conservative all-slice charge of 888 graphs restores the
pre-critical bounds:

```text
surviving untyped graphs                              164
fixed-s candidate graph count upper                   592
fixed-s normalized slope-sum upper                  51404
Lebesgue Z linear coefficient                       1184
row-law Z linear coefficient                    149184/5
partial genuine marked-current TV upper        518152320.
```

The remaining 164 charts belong to the older physical-first frontier, whose
compact manifest retained only per-row hashes rather than coordinates.  They
must be replayed/exported and then assigned a strict physical-first owner or
a strict nonphysical exclusion before the current can be called complete.

## 4. Fail-close boundary

Certified:

```text
coordinates of all 888 critical graph leaves             CERTIFIED
840 empty by strict Delta                                 CERTIFIED
48 nonphysical by strict negative tangent time            CERTIFIED
zero current/FACE contribution from the 888-leaf class    CERTIFIED
```

Not certified:

```text
classification of the older 164 untyped charts            NOT_CERTIFIED
complete side-owner current                               NOT_CERTIFIED
global strong DQ / branch-record MT_DQ / FACE             NOT_CERTIFIED
Gate 3                                                    NOT_CERTIFIED
```

## 5. Replay

```bash
PY=/tmp/cm2-flint-venv/bin/python
PYTHONPATH=deliverables CM2_WORKERS=32 $PY \
  deliverables/cm2_gate3_critical_graph_owner_typing_frontier_verifier.py \
  --replay --integrity-only
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_critical_graph_owner_typing_frontier_verifier.py \
  --self-test
# Deliberately exits 2 while the 164/current/DQ/MT_DQ/FACE remain open.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_critical_graph_owner_typing_frontier_verifier.py
```
