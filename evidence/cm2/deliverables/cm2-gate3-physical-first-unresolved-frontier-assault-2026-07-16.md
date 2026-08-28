# CM2 Gate 3: physical-first graph/current and unresolved-cause assault

Date: 2026-07-16 (Asia/Shanghai)  
Frozen input: twelfth-pass finite-`s` future-candidate outer atlas  
Strict verdict: **a conditionally physical-first analytic graph family, a
strictly nonempty root-arc subfamily, its genuine partial marked current, and
an exact terminal-cause decomposition are certified; the remaining positive
fixed-`s` intercept, complete owner atlas/current, strong-space DQ, `MT_DQ`,
`FACE_2CUT/FACE_TIME`, and Gate 3 remain `NOT_CERTIFIED`**

## 1. Pointwise-identical nearest-endpoint replay

The frozen outer atlas used the left moving endpoint to parameterize every
row box.  Near `t=1`, the natural interval expression repeats the same
endpoint data through `left + width = right` and creates avoidable dependency.
The new certificate uses the pointwise-identical two-anchor formula

```text
t<=1/2: theta = theta_left  + trim + (width-2 trim)t,
t>=1/2: theta = theta_right - trim - (width-2 trim)(1-t).
```

Every initial cell and descendant lies in one exact half, so no box crosses
the anchor seam; the common point `t=1/2` has the same value and derivatives
from both analytic formulas.  The twelfth-pass files remain byte-for-byte frozen.  The
new replay keeps their finite resolution (`5` additional `t` levels and `3`
parameter levels); the attempted `8/6` exploratory refinement was explicitly
discarded after it proved unsuitable for a bounded replay and contributes no
frozen claim.

## 2. Why rectangular bracketing was too strong

A slanted zero graph normally enters a dyadic rectangle through a horizontal
edge.  Requiring opposite signs on both vertical edges for the *entire*
parameter slab therefore leaves a positive rectangular outer cover even when

```text
Delta_candidate(t,s)=0,
partial_t Delta_candidate != 0
```

already defines a unique analytic graph (possibly empty) inside that chart.
The new registry assigns half-open ownership in both coordinates,
`[t0,t1)` and `[v0,v1)`, with only the last endpoint closed.  It registers the
**actual** `Delta=0` subset, not the surrounding rectangle.  An empty graph
chart contributes zero boundary and zero current.

This is a zero-width fixed-`s` statement.  The normalized coordinate

```text
v=(400s+1)/2
```

is still only a parameter coordinate, not a probability variable.  All
two-dimensional `(t,v)` areas below remain nonphysical parameter bookkeeping.
The artificial rectangular `t`-boundary also remains separate from the
future physical boundary/current.

## 3. Physical-first owner typing

On a candidate graph, its tangency time is its projection `P_i`.  A graph is
typed conditionally physical-first only when the replay proves, on the full
chart,

```text
0 < P_i < r_alt < 3,
```

where `r_alt` is one unique miss-side alternative owner.  It also proves that
`r_alt` precedes every other possible root.  Importantly, a competitor is not
discarded merely because its discriminant is strictly positive: if its
near-root enclosure crosses zero, its dependency-free lower root remains a
blocker.

The two physical traces are then

```text
grazing-hit at candidate i,
first miss-side collision at alt.
```

The full materialization obtains

```text
conditionally physical-first graph charts             27,356
strictly nonempty physical-first root arcs               7,122
untyped candidate graph charts                              368

maximum conditional physical charts on one fixed-s slice     478
maximum nonempty root arcs on one fixed-s slice                144
```

The first number deliberately includes possibly empty charts and is not
called a nonempty-root count.  The second count consists of charts with a
strict existence witness (in particular the full-slab bracketed roots).

## 4. Genuine partial marked current

On the actual zero subset of every conditionally physical-first chart, define

```text
J_s(Phi)
 = sum_i [partial_s Delta_i/|partial_t Delta_i|] rho_e(t_i,s)
   {Phi(grazing-hit_i)-Phi(first-miss-side-owner_i)}.
```

The sign is essential.  If `g_i(s)` is the root graph, then

```text
partial_s Delta_i/|partial_t Delta_i|
 = -sign(partial_t Delta_i) dg_i/ds.
```

Thus a chart with `partial_t Delta_i>0` has the hit trace on its increasing-`t`
side and contributes the negative of graph velocity times hit-minus-miss; a
chart with `partial_t Delta_i<0` has the hit trace on its decreasing-`t` side
and contributes the graph velocity itself.  The replay records both strict
orientations separately:

```text
partial_t Delta_i < 0 charts                         13,678
partial_t Delta_i > 0 charts                         13,678
```

The normalized row-law density satisfies `rho_e<=126/5`.  The chart records give

```text
max fixed-s sum |dt_i/dv| ceiling       2,938,
|dt/ds| = 200 |dt/dv|,
```

hence the genuine two-trace current on this certified subfamily has

```text
||J_s||_TV <= 2*(126/5)*200*2938 = 29,615,040.
```

Possibly empty charts contribute zero.  Half-open chart ownership prevents
double counting at dyadic boundaries.  This is still a **partial** current:
the `368` untyped graph charts and the terminal positive-width boxes below are
not silently assigned physical marks.

For the union of all registered actual candidate-zero graphs, including the
untyped charts, the conservative full-slab fixed-`s` chart sweep gives the
following upper bounds (possibly empty charts are retained in the sweep):

```text
maximum graph charts on one slice                         486
Lebesgue rho-collar linear coefficient                    972
row-law weighted linear coefficient                  122472/5.
```

This zero-intercept coefficient applies to the registered graph family, not
to the still-unresolved terminal boxes.

All fixed-`s` sweeps explicitly include the closed endpoint `v=1`
(`s=1/400`).  Its direct ledgers are below the global maxima:

```text
conditional physical charts / slope sum                 474 / 592
candidate graphs / slope sum                             480 / 600
nonempty physical arcs                                           126
terminal boxes / terminal t-width                     1,444 / 361/256.
```

## 5. Exact remaining positive intercept

The old finite-resolution sweep had

```text
maximum unresolved fixed-s t-width          1031/512,
row-law positive intercept                  64953/1280.
```

The new full replay makes `1,209,088` strict audit calls and leaves

```text
terminal boxes                                          93,080
maximum terminal boxes on one fixed-s slice              1,492
maximum terminal fixed-s t-width                        373/256
row-law positive intercept                 (126/5)(373/256)
                                               = 23499/640.
```

Thus the positive width falls by

```text
1031/512 - 373/256 = 285/512,
```

about `27.64%`.  It is not zero, so the complete future-candidate boundary
law remains `NOT_CERTIFIED`.

The terminal causes are now exhaustive:

| fail-closed cause | boxes | nonphysical `(t,v)` area | maximum fixed-`s` width |
|---|---:|---:|---:|
| interval geometry exception | 79,660 | `19915/16384` | `625/512` |
| candidate zero with `partial_t Delta` containing zero | 11,884 | `2971/16384` | `7/32` |
| source incidence `c_p` not strict | 1,536 | `3/128` | `3/128` |

The three per-cause fixed-`s` maxima occur at different parameter slices and
must not be added; the direct simultaneous sweep is the certified `373/256`.
The first cause is computational interval failure, not a proof of a physical
singularity.  The second is the analytic candidate critical-root frontier,
not yet a physically typed singularity.  The third is a first-layer incidence
dependency that must be rebound to the endpoint-rank atlas or refined with an
endpoint-scaled coordinate.

## 6. What is and is not closed

Certified:

```text
nearest-endpoint finite-s replay                         CERTIFIED
terminal unresolved cause decomposition                 CERTIFIED
conditionally physical-first graph-chart family         CERTIFIED
strictly nonempty physical-first root-arc subfamily      CERTIFIED
genuine partial physical marked current and TV bound     CERTIFIED
registered candidate-zero graph-family fixed-s Z         CERTIFIED
```

Not certified:

```text
zero-intercept complete future-candidate boundary Z      NOT_CERTIFIED
complete root-isolated side-owner atlas                  NOT_CERTIFIED
complete physical future current                         NOT_CERTIFIED
strong-source invariance of component restrictions       NOT_CERTIFIED
operator-norm depth-two DQ / branch-record MT_DQ          NOT_CERTIFIED
physical FACE_2CUT / FACE_TIME                           NOT_CERTIFIED
Gate 3                                                   NOT_CERTIFIED
```

The next exact attack is:

1. rebind the `79,660` interval-exception boxes to the frozen endpoint/core
   atlas using endpoint-scaled analytic coordinates;
2. resolve the `11,884` critical boxes by a two-variable Jacobian/resultant
   test, isolating transverse graph crossings and genuine codimension-two
   junctions;
3. type the `368` remaining graph charts by side owners;
4. assemble the root-isolated owner components and prove strong restriction
   invariance;
5. close operator DQ, branch-record `MT_DQ`, `FACE_2CUT`, and `FACE_TIME`.

## 7. Replay and fail-closed behavior

```bash
PY=/tmp/cm2-flint-venv/bin/python

$PY -m py_compile \
  deliverables/cm2_gate3_physical_first_unresolved_frontier_cert.py \
  deliverables/cm2_gate3_physical_first_unresolved_frontier_verifier.py

CM2_WORKERS=32 PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_physical_first_unresolved_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_physical_first_unresolved_frontier_verifier.py \
  --self-test

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_physical_first_unresolved_frontier_verifier.py
```

The corrected clean full materialization completed in `13:51.11` with exit
zero; the independent verifier replay completed in `13:48.97`, reproduced
internal digest
`1faed7744462e3c16e0072d81520d32d9bf34f4c2904e541641cd044f0aa1164`,
and printed `INTEGRITY: PASS`.  Its sixteen semantic
mutations recompute the internal replay digest before validation, so they are
rejected by their intended typing/arithmetic/completion guards rather than by
a stale digest.  Live mode prints every unsupported completion as
`NOT_CERTIFIED` and exits `2` by design.
