# CM2 Gate 3: final graph typing and complete future side-owner current

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: endpoint-scaled deep frontier, cancellation-free interval
frontier, and critical-graph exclusion stack  
Strict verdict: **all 1,052 predecessor untyped candidate graphs are now
resolved and the finite-s future side-owner current is complete, with total
variation at most `518152320`.  Global strong DQ, branch-record `MT_DQ`,
physical `FACE_2CUT/FACE_TIME`, and Gate 3 remain `NOT_CERTIFIED`.**

## 1. Exact recovery of the older 164 graphs

An independent 64-row frozen replay located the only nonzero rows at
`8,15,36,51`, not at the four rows suggested by the old depth-five ledger.
Each true row contains exactly 41 graphs, with 15
`additional_ambiguous_candidate_may_precede` and 26 graph-cover records.

This append-only certificate replays all 256 independent initial cells of
each true row.  The cells are parallelized only after the frozen row is
split: every decision is a pure function of one box and its dyadic
descendants, calls are additive, and records are canonically sorted before
hashing.  The result matches all four predecessor per-row digests and the
aggregate exactly:

```text
target rows                                      8,15,36,51
initial-cell tasks per row                              256
audit calls per row                                  39648
graphs per row                                          41
total exported graphs                                  164
coordinate ledger SHA  fc05d693e7f7419644f07cd268ee7355e940761f2bde962cf4651025a31b50e4
```

The endpoint-scaled frozen total is also 164 with failure split `60+104`, so
the coordinate export exhausts the compact predecessor aggregate.

## 2. Owner typing and strict preemption

At eight additional depths in each normalized coordinate, the 164 input
charts produce:

```text
typing audit calls                                  8908
conditionally physical-first leaves                  100
strict-Delta excluded descendants                   2372
direct nonphysical-time descendants                    0
remaining order-failure descendants                 2064
```

Blind refinement is not used beyond this point.  The 2,064 residual boxes
form an open order-failure region.  On every full closed box, the certificate
recomputes all distinct solid-target candidates and accepts an earlier root
only when the frozen positive-root branch proves:

```text
full-box discriminant > 0,
positive near root < 3,
upper(other positive near root)
    < lower(candidate tangent projection).
```

On the candidate zero subset its tangency time is exactly the projection.
Thus the existence of any such earlier collision excludes the candidate
from being a physical first future face; uniqueness of the preempting owner
is unnecessary.  All 2,064 boxes satisfy this strict inequality.  No
untyped descendant remains.

## 3. Complete current

Combining the 100 newly typed leaves with the 41,344 predecessor physical
charts gives 41,444 conditionally physical-first graph charts.  The 888
critical graphs were already shown to be empty or nonphysical, and the
151,500 interval-geometry boxes have zero positive-width remainder.

The frozen candidate-atlas fixed-s outer was computed on the complete
physical-plus-1,052-candidate family, before the new classifications:

```text
candidate graph count upper per fixed s                 592
normalized absolute slope-sum upper                   51404
current TV upper = 2*(126/5)*200*51404           518152320.
```

Refining, typing, or strictly excluding those same candidate charts cannot
increase this outer.  Therefore the marked future side-owner current is now
complete with TV at most `518152320`.

## 4. DQ/MT_DQ/FACE boundary

The completed current closes the remaining finite-s depth-two geometric
input.  On a compact set uniformly separated from every singular/current
graph for `|s|<=epsilon`, inside one fixed physical-record component, a
fixed-gauge, s-independent C1 source/test scalar pairing has the ordinary
finite analytic branch DQ by differentiation under the integral.

This local fixed-record scalar-pairing statement is not an operator-norm or
global component-restriction theorem.  The following remain open:

```text
fixed strong-space invariance on all branch restrictions
one common moving atlas for every (L,m,n)
dynamic branch-test BL convergence and all iterated boundary-Z bounds
finite-s regular/face/product/response convergence on that atlas
physical word depth and propagated q domination before cancellation
no-|s|^-1 per-depth FACE bound, multiplicity ledger, and deep tail
physical-current/proper-family matching and bilinear FACE_TIME lift.
```

Hence strong DQ, branch-record `MT_DQ`, physical `FACE_2CUT/FACE_TIME`, and
Gate 3 remain fail-closed.

## 5. Replay

```bash
PY=/tmp/cm2-flint-venv/bin/python
PYTHONPATH=deliverables CM2_WORKERS=48 $PY \
  deliverables/cm2_gate3_remaining_graph_complete_current_frontier_verifier.py \
  --replay --integrity-only
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_remaining_graph_complete_current_frontier_verifier.py \
  --self-test
# Deliberately exits 2 because strong DQ/MT_DQ/FACE and Gate 3 remain open.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_remaining_graph_complete_current_frontier_verifier.py
```
