# CM2 Gate 3: endpoint-scaled incidence and critical-resultant frontier

Date: 2026-07-16 (Asia/Shanghai)  
Frozen input: thirteenth-pass physical-first/current frontier  
Strict verdict: **a cancellation-free source-incidence lemma is certified on
24 endpoint row-bands / 1,536 parameter cells, and one additional selective level
reduces the critical-root frontier from 11,884 boxes to 12; the remaining
interval exceptions, 2,048 source-tagged descendants pending downstream
classification, 12 numerical resultant boxes, 164 untyped charts,
complete side-owner current, strong DQ/MT_DQ/FACE, and Gate 3 remain
`NOT_CERTIFIED`**

## 1. Cancellation-free endpoint coordinate

Let `C=target-source`, and write the source-grazing endpoint frame as

```text
C = a0 n0 + B0 j0,
a0 = R_source + sigma R_target                 (exact).
```

At inward angular distance `x`, with rotation sign `q`, put

```text
n = cos(x)n0 + q sin(x)j0,
A = C.n - R_source.
```

The small factor is evaluated without subtracting two wide intervals:

```text
A-sigma R_target
  = (cos(x)-1)a0 + q sin(x)B0.                 (1.1)
```

The direct source-incidence expression is rationalized as

```text
c_p = (A^2-R_target^2)
      /(ell A-epsilon R_target B),             (1.2)
```

and its numerator is kept as the two separately signed factors
`(A-sigma R_target)(A+sigma R_target)`.  A pointwise direct-versus-rationalized
midpoint identity is checked on every parameter slab, guarding all frame and
sign conventions.  The common core angular width is strictly `>1/40` and
`<9/4` on every certified slab.

This proves strict `c_p>0` on `24*64=1,536` explicitly constructed canonical
endpoint-band parameter cells:

```text
canonical source-grazing rows                            24
closed parameter cells per row                          64
canonical t-width per row                           1/1024
24-row total canonical fixed-s t-width                 3/128
```

The closed `v=1` endpoint is included.  The frozen terminal records are
available only through hashes and aggregate counts; this artifact does not
freeze each record's `(side,t0,t1,v0,v1)` containment in the canonical bands.
Consequently it does not remove or reclassify the old `1,536` source-tagged
records.

The deeper replay emits `2,048`
source-tagged descendants because its old prerequisite routine exits before
evaluating downstream `miss_delta`, root gap, candidate, owner, or critical
status.  This artifact does **not** freeze a parent-to-child containment
ledger and does not reclassify those descendants.  They remain fail-closed.

## 2. One-level selective replay

Only the unresolved terminal frontier is given one additional normalized
level, from selective depth `(5,3)` to `(6,4)`.  This remains a finite outer
atlas, not a mesh-to-zero extrapolation.  The replay makes `1,722,936` strict
audit calls and obtains:

| frontier | thirteenth pass | deeper replay |
|---|---:|---:|
| conditionally physical-first charts | 27,356 | 41,344 |
| strictly nonempty physical-first arcs | 7,122 | 11,678 |
| untyped candidate charts | 368 | 164 |
| critical-root boxes | 11,884 | 12 |
| interval-exception retained outer-box parameter-area upper cover | `19915/16384` | `37875/65536` |
| interval-exception max fixed-s width | `625/512` | `595/1024` |
| critical retained outer-box parameter-area upper cover | `2971/16384` | `3/65536` |
| critical max fixed-s width | `7/32` | `1/1024` |
| raw fail-closed simultaneous terminal width | `373/256` | `603/1024` |

The interval-exception **box count** is `151,500` because the retained outer
set is subdivided; its retained outer-box parameter-area cover and fixed-s
width both fall by more than one half.  Neither outer parameter area is
interpreted as true singular mass, physical mass, or a certified physical
unresolved area.

The deep replay's full simultaneous terminal width `603/1024` is retained
unchanged.  In particular, this report does **not** subtract the source-tagged
width and does not claim `149/256`: the missing containment/downstream ledger
would be required before such a subtraction.  Zero intercept is not
certified.  The three separate reason maxima would sum to
`595/1024+1/1024+1/128=604/1024`; these are reasonwise envelopes and are not
additive.  The direct union sweep certifies the simultaneous `603/1024` bound.

## 3. Exact critical resultant

For a candidate target of radius `r`, write

```text
Delta = r^2-w^2,
Delta_t = -2w w_t.
```

At a critical zero, `w=sigma r` and `w_t=0`.  The exact two-variable
Jacobian reduces to

```text
det D_(t,s)(Delta,Delta_t)
  = -Delta_s Delta_tt
  = -4 r^2 w_s w_tt.                            (3.1)
```

The coefficient algebra in (3.1) is certificate-checked.  This gives the
precise next numerical test: certify `w_s w_tt != 0` or isolate every zero of
that product on the `12` remaining boxes.  The present artifact does **not**
claim that interval nonvanishing, does not delete the boxes, and does not
call them harmless codimension-two junctions.

## 4. Current orientation and owner scope

The deeper atlas preserves the genuine partial current on actual zero
subsets:

```text
J_s(Phi)
 = sum_i [partial_s Delta_i/|partial_t Delta_i|] rho_e(t_i,s)
   {Phi(grazing-hit_i)-Phi(first-miss-side-owner_i)}.
```

Equivalently,

```text
partial_s Delta/|partial_t Delta|
 = -sign(partial_t Delta) dt_graph/ds.
```

No absolute-sign simplification is made.  Half-open `(t,v)` ownership and the
closed `v=1` ledger are replayed unchanged.  The `164` untyped charts consist
of `60` additional-ambiguous-owner charts and `104` conservative untyped graph
covers.  They are not assigned marks, so the current remains partial.

## 5. Strict remaining boundary

Certified:

```text
canonical endpoint-band source-cp positivity on 24 endpoint
row-bands / 1,536 parameter cells                             CERTIFIED
one-level selective outer-atlas / partial-current replay
ledger                                                        CERTIFIED
critical-resultant algebraic reduction (3.1)                  CERTIFIED
```

Not certified:

```text
151,500 interval-geometry children                            NOT_CERTIFIED
containment/reclassification of 1,536 old source records      NOT_CERTIFIED
downstream reclassification of 2,048 source-tagged children   NOT_CERTIFIED
numerical resultant nonvanishing on 12 critical boxes         NOT_CERTIFIED
physical typing of 164 candidate graph charts                 NOT_CERTIFIED
complete side-owner current                                   NOT_CERTIFIED
strong component-restriction DQ / branch-record MT_DQ         NOT_CERTIFIED
physical FACE_2CUT / FACE_TIME                                 NOT_CERTIFIED
Gate 3                                                        NOT_CERTIFIED
```

The next exact attack starts by freezing coordinatewise
`(side,t0,t1,v0,v1)` containment for the old source-tagged records and
injecting the scaled-`c_p` lemma into all `2,048` deeper cells before
continuing their `miss_delta`/root-gap/candidate/owner audit.  In parallel it
must rationalize the miss-discriminant and root-gap coordinates on the other
interval-exception children, run (3.1) on the 12 critical boxes, and type the
remaining owners.  Only then can it assemble complete current, strong DQ,
`MT_DQ`, and FACE.

## 6. Replay and fail-close

```bash
PY=/tmp/cm2-flint-venv/bin/python

PYTHONPATH=deliverables CM2_WORKERS=32 $PY -m py_compile \
  deliverables/cm2_gate3_endpoint_scaled_resultant_frontier_cert.py \
  deliverables/cm2_gate3_endpoint_scaled_resultant_frontier_verifier.py

PYTHONPATH=deliverables CM2_WORKERS=32 $PY \
  deliverables/cm2_gate3_endpoint_scaled_resultant_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_endpoint_scaled_resultant_frontier_verifier.py \
  --self-test

# Deliberately exits 2 while complete current/DQ/MT_DQ/FACE remain open.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_endpoint_scaled_resultant_frontier_verifier.py
```

Artifacts:

- `cm2_gate3_endpoint_scaled_resultant_frontier_cert.py`;
- `cm2_gate3_endpoint_scaled_resultant_frontier_verifier.py`;
- `cm2-gate3-endpoint-scaled-resultant-frontier-manifest-2026-07-16.json`;
- `cm2-gate3-endpoint-scaled-resultant-frontier-manifest-2026-07-16.sha256`.
