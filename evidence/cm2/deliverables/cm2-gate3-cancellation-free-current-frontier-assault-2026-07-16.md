# CM2 Gate 3: cancellation-free miss frontier and immutable branch records

Date: 2026-07-16 (Asia/Shanghai)  
Frozen input: fifteenth-pass deep scaled/resultant Gate-3 frontier  
Strict verdict: **all 151,500 frozen `interval_geometry_exception` leaves are
reconstructed exactly, their miss discriminants and first-root gaps are
certified by cancellation-free endpoint identities, and their finite
downstream replay ends in 156,108 immutable owner leaves with no graph and no
positive-width terminal; the fixed-`s` positive-width outer is therefore
reduced from `595/1024` to zero.  The surviving 1,052 old/untyped graph charts,
complete physical current, strong DQ/MT_DQ/FACE, and Gate 3 remain
`NOT_CERTIFIED`.**

## 1. Exact reconstruction of the 151,500 leaves

The frozen manifest exported only the aggregate count, area and fixed-`s`
width of its interval-exception class.  This append-only layer reconstructs
the actual depth-`(6,4)` coordinates without changing the old stack.

Exactly 32 of the 64 occurrence rows have a unique
`physical_later_miss_switch_boundary` whose descriptor `other` equals that
row's frozen `miss_target`.  On each such row the replay audits 512 of the
2,048 deep `t` cells adjacent to that endpoint and all 128 parameter cells.
Every retained leaf is checked to fail the frozen code at the same operation:

```text
sqrt_miss_delta,  miss_delta = r_m^2-w_m^2,
```

not in a curve-normal, tangent-flight or future-candidate operation.  The
result consists of 151,500 distinct half-open leaves.  Because every one is a
genuine frozen terminal leaf and their number equals the frozen aggregate,
this explicit coordinate ledger exhausts the old class.  Its SHA is recorded
in the JSON certificate.

## 2. Cancellation-free miss discriminant

Let `N` be the oriented common-tangent normal at the matching endpoint,
`T` the tangent target, `M` the miss target, and `Q` the source point.  The
descriptor construction gives the exact identities

```text
N.(M-T) = epsilon_other*r_m - epsilon_target*r_T,
N.(T-Q) = epsilon_target*r_T.
```

With the frozen tangent orientation this implies

```text
w(0,s) = sigma*r_m,  sigma=epsilon_other.
```

For inward angular distance `x>0`, put

```text
F(x,s)=r_m-sigma*w(x,s).
```

The small factor is not evaluated by subtracting two nearly equal interval
balls.  Instead every leaf uses

```text
F(x,s)=x integral_0^1 partial_x F(theta*x,s) dtheta,
```

with `partial_x F` enclosed on the full rectangle
`0<=theta*x<=x_max`.  Its sign is strict on all 151,500 input leaves.  The
second factor is also strict, so

```text
Delta_m = F(2*r_m-F) > 0.
```

Endpoint multiplication is used for positive balls; this avoids the harmless
negative radius edge that midpoint-radius multiplication can acquire for a
highly asymmetric small factor.  Only `Delta_m.value` is tightened.  The
natural AD enclosures `Delta_m.dt` and `Delta_m.ds` are retained, so the
subsequent square root, reflection and candidate derivatives remain rigorous.

The exact common-tangent algebra is independently guarded on all 32 active
rows at `s=0`; every rounded `w-sigma*r_m` ball contains zero and every target
tangent flight is strictly greater than `1/10`.  These are consistency guards,
not a numerical inference of the endpoint identity.

## 3. Cancellation-free first-root gap

Write `h=ell-ell_T`.  The direct root-time subtraction is replaced by

```text
h-sqrt(Delta_m)
 = (h^2-Delta_m)/(h+sqrt(Delta_m)).
```

On every rescued rectangle `h`, the numerator and the denominator are all
strictly positive on the full closed box.  Thus the miss collision is before
the tangent target uniformly, without relying on cancellation between nearby
root times.

## 4. Downstream owner replay

After the two strict prerequisite witnesses are injected locally, the frozen
candidate/owner routine is resumed.  Only a finite anisotropic continuation
is allowed: at most six additional `t` levels and, if ever needed, two
additional parameter levels.  The clean replay actually reaches only

```text
maximum t depth                    8
maximum parameter depth            4
rescued/refinement audit calls 160716
final leaves                   156108
immutable owner leaves         156108
candidate graph leaves              0
positive-width terminals            0.
```

Consequently the interval-exception class contributes no analytic future
face, no marked current, and no physical `FACE_2CUT` or `FACE_TIME` charge.
The artificial dyadic refinement edges are bookkeeping edges, not physical
faces.  The complete coordinate/owner branch-record ledger is frozen by SHA.

This closes the last positive-width Gate-3 terminal class:

```text
frozen interval boxes                         151500
frozen fixed-s positive t-width outer       595/1024
remaining positive-width terminal boxes            0
new fixed-s positive t-width outer                  0
zero-intercept complete future candidate boundary   yes.
```

The two-dimensional `37875/65536` number from the predecessor was only a
nonphysical parameter cover.  It is not relabelled as physical mass here.

## 5. Exact remaining boundary

The new immutable class adds no graph, so the predecessor graph/current
frontier is unchanged:

```text
conditionally physical-first graph charts       41344
strictly nonempty physical root arcs              11678
surviving untyped candidate graph charts           1052
safe fixed-s candidate graph count upper            1480
safe normalized slope-sum upper                    52292
partial genuine marked-current TV upper        518152320.
```

The 1,052 charts are the 164 frozen untyped charts plus 888 strict-`Delta_t`
critical-refinement leaves.  Until every one has a unique physical-first
miss-side owner, the marked current is partial.  The immutable branch ledger
alone does not prove invariance of the three CM2 strong spaces, operator DQ,
branch-record `MT_DQ`, or global `FACE_2CUT/FACE_TIME`.

Certified:

```text
exact coordinates/stage of all 151,500 old exceptions          CERTIFIED
cancellation-free miss Delta and root-gap on every leaf         CERTIFIED
all rescued descendants -> immutable owner branch records       CERTIFIED
zero positive-width future-candidate intercept                  CERTIFIED
zero current/FACE contribution from this resolved class         CERTIFIED
```

Not certified:

```text
physical-first owner typing of the surviving 1,052 graphs       NOT_CERTIFIED
complete side-owner current                                     NOT_CERTIFIED
global strong DQ / branch-record MT_DQ                           NOT_CERTIFIED
global physical FACE_2CUT / FACE_TIME                            NOT_CERTIFIED
Gate 3                                                          NOT_CERTIFIED
```

## 6. Replay and fail-close

```bash
PY=/tmp/cm2-flint-venv/bin/python

PYTHONPATH=deliverables CM2_WORKERS=32 $PY -m py_compile \
  deliverables/cm2_gate3_cancellation_free_current_frontier_cert.py \
  deliverables/cm2_gate3_cancellation_free_current_frontier_verifier.py

PYTHONPATH=deliverables CM2_WORKERS=32 $PY \
  deliverables/cm2_gate3_cancellation_free_current_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_cancellation_free_current_frontier_verifier.py \
  --self-test

# Deliberately exits 2 while complete current/DQ/MT_DQ/FACE remain open.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_cancellation_free_current_frontier_verifier.py
```

Artifacts:

- `cm2_gate3_cancellation_free_current_frontier_cert.py`;
- `cm2_gate3_cancellation_free_current_frontier_verifier.py`;
- `cm2-gate3-cancellation-free-current-frontier-manifest-2026-07-16.json`;
- `cm2-gate3-cancellation-free-current-frontier-manifest-2026-07-16.sha256`.
