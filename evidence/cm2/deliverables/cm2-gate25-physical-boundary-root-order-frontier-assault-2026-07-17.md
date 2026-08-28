# CM2 Gates 2/5: physical boundary-root reduction and ordering frontier

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the fifteenth-round 24 seeded implicit maximal components,
selected-homoclinic incidence, global tangency transversality, oriented slope
and numeric invariant-family stacks were read only  
Strict verdict: **the 394/402 raw predicate over-ledgers are reduced to
285/289 physical boundary-branch roots per canonical curve, every such root
is isolated and weakly orderable, and all 24 positive seeded maximal
components receive a finite component-local unnormalised characteristic-`Z`
bound.  The bound is not contracting and is not a full-key field; Gates 2 and
5 remain `NOT_CERTIFIED`.**

## 1. Raw owner equalities versus physical owner boundaries

The frozen maximal-component registry used an intentionally overcomplete
owner ledger.  A source chart has either 55 or 57 candidate target disks.  It
registered, for every candidate,

```text
discriminant=0, near root=0, near root=3,
```

and, for every competitor, equality with the selected near root.  Thus it
counted `4N-1`, namely 219 or 227 raw owner predicates.

The physical exact-first-owner boundary is smaller.  Every pair of distinct
lifted closed disks is strictly disjoint.  The exact worst squared separation
margin is

```text
36337/160000 > 0.
```

Consequently a positive ray root cannot be equal for two distinct targets,
and a distinct target cannot have root zero at a source collision.  The
certified physical first flight is always strictly below three; a competitor
crossing the artificial horizon at three cannot change a word whose selected
first collision occurs earlier.  Therefore the physical boundary loses

```text
N root-zero predicates + N root-three predicates + (N-1) owner ties.
```

Only the candidate tangencies remain.  One discriminant equality is the
union of its two signed tangent orientations, so the physical owner-boundary
branch upper is `2N`: 110 on a W-source row and 114 on a G-source row.

The removal of `root=3` is bound directly to the frozen full-window horizon
audit: its manifest records the explicit SYZ horizon `(3,1/512)`, strict
positive penetration slack, and that every open length-three segment already
meets a scatterer.  Hence the physical first flight is strictly `tau<3` on
the complete parameter window.

This is a reduction of the *physical boundary grammar*, not a claim that the
discarded algebraic functions never vanish outside their physical role.

## 2. Uniform root isolation and weak ordering

Work on a fixed `s` fibre in Birkhoff coordinates `(r,phi)`.  A canonical
unstable graph satisfies

```text
V=dphi/dr > 25/9.
```

This inequality is bound directly to the frozen invariant-cone field
`25/9<V=dphi/dr<4108425/145348<29`, including strict forward invariance and
positive recurrence denominators.

Every nonvertical physical branch in the word ledger is stable-oriented:

```text
candidate signed tangency:
  dphi/dr = -kappa_0-c_0/ell_T < -25/9;

target endpoint / target chart seam, r_1=constant:
  dphi/dr = -kappa_0-c_0/tau < -25/9;

target momentum face, phi_1=constant:
  dphi/dr = -kappa_0-kappa_1*c_0/(tau*kappa_1+c_1) < -25/9;

forward ray through integer corner at time lambda:
  dphi/dr = -kappa_0-c_0/lambda < -25/9;

coordinate velocity zero:
  dphi/dr = -kappa_0 <= -25/9.
```

The denominators are positive on the corresponding physical branches.
Source endpoint and source-chart cuts are `r=constant`; source momentum faces
are horizontal.  Hence every active physical branch meets one canonical
unstable graph in at most one isolated root.  The stable/unstable slope gap is
strictly greater than `50/9`.

The 44 endpoint-on-integer-wall equalities also have at most one root in the
declared endpoint charts.  A white disk stays at least `199/400` from a
vertical integer wall and `1/2` from a horizontal one, both greater than its
radius `4/25`.  A gray disk has radius `9/25<1`; an integer wall meeting it
must pass through the corresponding integer center coordinate.  A fixed
source normal chart or fixed target open semicircle contains at most one of
the resulting endpoint positions.

Thus all physical roots admit a weak total order by source `r`.  Simultaneous
predicate roots are coalesced into one geometric cut.  No curve-by-curve
numeric sequence is claimed: the theorem uniformly isolates and bounds the
roots for the arbitrary canonical curve supplied to the operator.

## 3. Exact count reduction

The transparent-word ledger contributes at most

```text
44 endpoint-on-wall branches
+121 forward integer-corner branches
+  2 coordinate-velocity-zero branches
=167 branches.
```

These numbers are replayed row by row from the frozen grammar, with explicit
assertions for `44`, `121`, `2`, the two source seams, two target seams, four
central homogeneity faces, and the roof-two oriented-wall-chart flag.  The
replayed grammar and its SHA digest are stored in each source-class record;
`167` and `8` are not free-standing constants.

The two source seams, two target seams and four source/target central
homogeneity faces add eight.  Therefore:

```text
G-source row:  2*57 + 167 + 8 = 289 physical roots,
W-source row:  2*55 + 167 + 8 = 285 physical roots.
```

Among the 24 seeded components there are twelve rows of each kind.  Removing
at most `m` points from a curve leaves at most `m+1` open pieces.  Hence the
intersection with any one seeded maximal component has the safe uniform
upper

```text
G-source component: <=290 pieces,
W-source component: <=286 pieces.
```

The selected homoclinic component

```text
7359148da1c43a255f2238d9c831b8638f2c9885035034a5792699c968b2f3b5
```

is a G-source component and receives the same strict `290` upper.

This is not asserted to be sharp.  Many registered wall/corner and tangency
branches do not reach a given component.  Component-local reachability
pruning and a materialized actual root sequence remain the next numerical
step.

## 4. Finite component-local characteristic `Z`

On a canonical parent curve the invariant conditional density obeys

```text
sup rho / inf rho <= 2000/1999.
```

For every retained interval `I`,

```text
q_I/|I| <= (2000/1999) q/|W|.
```

Summing over the preceding component count gives

```text
W-source seeded component: Z_*(1_M F) <= (572000/1999) Z_*(F),
G-source seeded component: Z_*(1_M F) <= (580000/1999) Z_*(F).
```

Thus all 24 positive seeded maximal components, including the selected QNL
component, have a finite unnormalised component-local characteristic bound.

The type restrictions are essential:

- this is one already selected connected maximal component, not the union of
  every component of its word key;
- it is an unnormalised source estimate, not a bound after conditioning on a
  small retained mass;
- no exact active-boundary count is claimed;
- the worst multiplier times the certified physical step is
  `208878184000000/720626832337>1`, so it does not yield Growth contraction;
- it therefore does not fill full-key field 7 or fields 14--17.

## 5. Exact remaining boundary

```text
394/402 RAW-TO-PHYSICAL BOUNDARY REDUCTION:          CERTIFIED
UNIFORM ISOLATED ROOT / WEAK ORDER THEOREM:          CERTIFIED
24 SEEDED COMPONENT-LOCAL FINITE UNNORMALISED Z:     CERTIFIED

CURVE-BY-CURVE NUMERIC ROOT SEQUENCE:                NOT MATERIALIZED
EXACT ACTIVE BOUNDARY COUNT PER SEEDED COMPONENT:    NOT CERTIFIED
FULL-KEY ALL-COMPONENT CHARACTERISTIC Z:             NOT CERTIFIED
CONTRACTING FULL-KEY FIELD 7:                        NOT CERTIFIED
COMPLETE 18-FIELD OPERATOR BLOCK COUNT:              0
STABLE QUOTIENT / rho / p_a / PPE:                   NOT CERTIFIED
GATE 2:                                               NOT CERTIFIED
GATE 5:                                               NOT CERTIFIED
```

The next honest attack is to propagate the positive seed through the ordered
arrangement and discard every physical branch that is unreachable from that
component.  Only an actual-component count small enough to preserve the
physical contraction may be promoted toward Gate-5 field 7.

## 6. Replay

```bash
PY=/tmp/cm2-flint-venv/bin/python
PYTHONPATH=deliverables $PY -m py_compile \
  deliverables/cm2_gate25_physical_boundary_root_order_frontier_cert.py \
  deliverables/cm2_gate25_physical_boundary_root_order_frontier_verifier.py

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_physical_boundary_root_order_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_physical_boundary_root_order_frontier_verifier.py \
  --self-test

# Expected exit 2: Gates 2 and 5 remain fail-closed.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_physical_boundary_root_order_frontier_verifier.py
```
