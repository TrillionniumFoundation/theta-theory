# CM2 Gate 3: deep scaled-source and critical-resultant closure

Date: 2026-07-16 (Asia/Shanghai)  
Frozen input: fourteenth-pass endpoint-scaled/resultant frontier  
Strict verdict: **all 1,536 old and 2,048 deep source-tagged rectangles now
have coordinatewise containment ledgers; the 2,048 deep rectangles become
immutable after the scaled `c_p` witness is injected; all 12 coarse critical
rectangles are replaced by strict-sign exclusions or 888 transverse candidate
graphs; 151,500 interval-geometry rectangles, 1,052 untyped graphs, complete
current, DQ/MT_DQ/FACE, and Gate 3 remain `NOT_CERTIFIED`**

## 1. Exact source containment and downstream replay

The old artifact certified positivity on canonical endpoint bands but did not
export each terminal record.  This pass enumerates only the dyadic leaves
inside the 32 geometric source-grazing row bands and replays the frozen
384-bit terminal test.

At depth `(5,3)` it recovers exactly the frozen total of 1,536 source-tagged
records.  They lie on 24 rows; every record equals its canonical `t` band of
width `1/1024` and its canonical `v` cell of width `1/64`.  Hence the explicit
distinct list, whose count equals the frozen aggregate total, exhausts the old
source-tagged family.

At depth `(6,4)` it similarly recovers exactly 2,048 records on 16 rows.  Each
record is contained coordinatewise in one old canonical `(t,v)` parent cell.
There are 1,024 such old parents and exactly two deep source-tagged children
per parent.  The remaining eight old source-tagged rows became strict under
the frozen deeper replay and need no override.

Only after this containment check, the cancellation-free factorized endpoint
witness is injected locally.  The ordinary frozen pipeline is then continued:

```text
miss_delta -> miss_root_gap -> candidate -> owner
```

All 2,048 records become strict immutable owner components.  No graph and no
positive-width terminal record is added.  Their fixed-`s` terminal width is
constant, including the closed `v=1` endpoint, and equals `1/128`.  Therefore
the simultaneous fail-closed width can now be reduced legitimately from
`603/1024` to `595/1024`; this is a ledger subtraction, not an inference from
aggregate box counts.

## 2. Exhaustive treatment of the 12 critical rectangles

The 12 coarse boxes contain 444 conservatively possible candidate functions
(the symmetric box counts are 25, 33, and 53).  A raw second-derivative natural
interval on the coarse boxes is too dependent and can be `nan`; it is not used
as evidence.

Instead, each candidate is selectively subdivided.  On every descendant the
simultaneous system

```text
Delta = 0,   Delta_t = 0
```

is treated fail-closed.  A leaf is discarded only if `Delta` has a strict
sign.  Otherwise it is retained as a possibly empty transverse candidate
graph only if `Delta_t` has a strict sign.  If neither test succeeds, the
second-order identity

```text
det D_(t,s)(Delta,Delta_t) = -Delta_s Delta_tt
                           = -4 r^2 w_s w_tt
```

is available as a regular-value test; in this replay no leaf needs that last
route.

The exhaustive result is:

```text
coarse boxes                                      12
coarse possible candidate functions              444
selective audit calls                            3196
Delta-strict excluded leaves                      932
strict-Delta_t transverse graph leaves            888
regular-fold leaves                                 0
unresolved leaves                                   0
```

Thus no simultaneous `(Delta,Delta_t)` zero remains on the 12 coarse boxes.
They contribute no positive-width terminal box.  The 888 graph leaves have
normalized slope upper one each, but are not promoted to physical-first
owners.  Together with the frozen 164 untyped charts, the conservative
untyped count is now 1,052.

The frozen genuine partial current is unchanged, with TV upper `518152320`.
A safe candidate-graph fixed-s ledger is obtained by adding all 888 new leaves
to the frozen maxima:

```text
candidate graph count upper                       1480
normalized slope-sum upper                       52292
Lebesgue Z linear coefficient                     2960
row-law Z linear coefficient                     74592
```

These are conservative graph-atlas bounds, not a complete physical current.

## 3. Remaining interval frontier

No cancellation-free full-window classification was obtained for the
151,500 `interval_geometry_exception` rectangles.  They remain unchanged:

```text
positive-width terminal boxes                   151500
nonphysical parameter-area upper cover      37875/65536
uniform fixed-s positive t-width outer        595/1024
```

The two-dimensional area is only parameter bookkeeping.  It is not physical
mass.  Since the fixed-s intercept is still positive, complete current,
operator DQ, branch-record MT_DQ, `FACE_2CUT`, and `FACE_TIME` are not
certified.

## 4. Latest-technology applicability audit

The official arXiv record and paper text for arXiv:2607.13785v1 (Haibo Lu,
*Local Uniform Finite Cyclicity of the H_14^3 Semihyperbolic Hemicycle*) were
checked.  Its stopped-first-hit strategy is useful as an analogy, but its
Propositions 4/8 and Theorem 10 assume analytic planar ODE flow boxes, strict
flow/Lyapunov coordinates, a finite equilibrium-sector alphabet, and a
one-intersection property for labelled corner or invariant-half-branch
orbits.  Its root-scale theorems count zeros of retained analytic
Liénard-Dulac return words; the final cyclicity bound is existential.

The paper explicitly notes that sorting divider points on fixed
one-dimensional cuts does not assert finite-component control for arbitrary
transported finite-smooth faces.  It therefore supplies no direct lemma for
the billiard `(Delta,Delta_t)` boxes, interval physical-first typing, current,
or DQ.  It was not used to remove or reclassify any box.

## 5. Exact remaining boundary

Certified:

```text
old/deep source-record coordinatewise containment             CERTIFIED
2,048 deep source records -> immutable owner components       CERTIFIED
12 critical boxes -> exclusions / strict-dt graphs            CERTIFIED
updated positive-width frontier and candidate-Z bounds         CERTIFIED
```

Not certified:

```text
151,500 interval-geometry rectangles                          NOT_CERTIFIED
physical-first typing of 1,052 untyped graph charts           NOT_CERTIFIED
complete side-owner current                                   NOT_CERTIFIED
strong component restriction DQ / branch-record MT_DQ         NOT_CERTIFIED
physical FACE_2CUT / FACE_TIME                                NOT_CERTIFIED
Gate 3                                                        NOT_CERTIFIED
```

The next exact attack is cancellation-free miss-discriminant/root-gap
evaluation on the 151,500 rectangles, followed by owner typing of the 1,052
untyped graphs and complete current/DQ/MT_DQ/FACE assembly.

## 6. Replay and fail-close

```bash
PY=/tmp/cm2-flint-venv/bin/python

PYTHONPATH=deliverables CM2_WORKERS=32 $PY -m py_compile \
  deliverables/cm2_gate3_deep_scaled_resultant_frontier_cert.py \
  deliverables/cm2_gate3_deep_scaled_resultant_frontier_verifier.py

PYTHONPATH=deliverables CM2_WORKERS=32 $PY \
  deliverables/cm2_gate3_deep_scaled_resultant_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_deep_scaled_resultant_frontier_verifier.py \
  --self-test

# Deliberately exits 2 while complete current/DQ/MT_DQ/FACE remain open.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_deep_scaled_resultant_frontier_verifier.py
```

Artifacts:

- `cm2_gate3_deep_scaled_resultant_frontier_cert.py`;
- `cm2_gate3_deep_scaled_resultant_frontier_verifier.py`;
- `cm2-gate3-deep-scaled-resultant-frontier-manifest-2026-07-16.json`;
- `cm2-gate3-deep-scaled-resultant-frontier-manifest-2026-07-16.sha256`.
