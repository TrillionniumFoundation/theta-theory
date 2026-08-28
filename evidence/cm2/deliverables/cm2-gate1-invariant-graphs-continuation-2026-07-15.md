# CM2 Gate 1 continuation: both local invariant graphs certified

Date: 2026-07-15 (Asia/Shanghai)  
Scope: explicit QNL/connector invariant-manifold layer  
Frozen inputs: v51/v52 and all frozen certificates were read, not edited  
Gate 1 final status: **OPEN / NO-GO FOR FULL-CROSS COMMON VERTEX**

## 1. Executive verdict

The two affine eigentangents used by the previous shooting seed have now
both been upgraded to actual local invariant manifolds:

| layer | status |
|---|---:|
| actual local `W^u(QNL)` | **CERTIFIED** |
| actual local `W^s(connector)` | **CERTIFIED** |
| ten-collision QNL graph-tube physical replay | **CERTIFIED** |
| inverse-fourteen connector graph-tube physical replay | **CERTIFIED** |
| true two-graph matching Krawczyk | **OPEN** |
| explicit common vertex / four-face full crossing | **OPEN** |
| transported twisting at that vertex | **OPEN** |

Thus Gate 1 has advanced past the “eigentangent is not a manifold” blocker,
but it is not yet closed.  The remaining obstruction is now a
correlation-preserving evaluation of the two finite graph images and a true
matching inclusion.

## 2. QNL graph

In QNL eigen-coordinates

```text
s=x+y,   p=k_A(x-y),   k_A=sqrt(gamma_A/beta_A),
```

the 300-bit certificate proves a unique local unstable graph

```text
W^u_loc(QNL) = {(x,h_A(x)): |x|<=2e-9},
|h_A(x)|<=x^2,       |h_A'(x)|<=1e-4.
```

The exact two-collision return is differentiated to second order on the
whole graph domain.  The fail-closed graph-transform bounds are

```text
unstable projection lower       > 11.097,
image Lipschitz constant         < 4.07e-5 < 1e-4,
graph-transform contraction      < 0.0902 < 1,
quadratic image constant         < 1.08e-3 < 1.
```

The full physical word `G0-W0-G0`, its first-hit exhaustion and strict
flight/discriminant/incidence/clearance margins are checked on the entire
domain.  At the shooting abscissa

```text
t=-1.396101069259116746830594312272814e-9
```

the actual graph ordinate satisfies `|h_A(t)|<=1.95e-18`.  Propagating this
whole tube through the immutable ten-collision word preserves every physical
margin.

Detailed report:
`deliverables/cm2-gate1-qnl-invariant-graph-assault-2026-07-15.md`.

## 3. Connector graph by recentered collision jets

Raw interval propagation through fourteen collisions loses parameter
correlation.  The new connector certificate therefore uses a discrete
Taylor-model analogue:

1. at every certified periodic collision it evaluates a fresh two-variable
   second-order Arb jet;
2. it propagates the reachable radius by the mean-value theorem;
3. it composes the Jacobian and Hessian tensors separately;
4. it performs the graph transform only on the preimage core needed to cover
   the requested graph domain.

In connector eigen-coordinates `s=x+y`, `p=k_B(x-y)`, it proves a unique
local unstable graph on

```text
|x| <= 3e-12,
|h_B(x)| <= 0.01 x^2,
|h_B'(x)| <= 1e-8.
```

Only the core `|x|<=4e-20` is needed to cover that target interval, because
the unstable multiplier is about `1.075e8`.  The certified bounds are

```text
core projection image            > 4.2999857e-12 > 3e-12,
image Lipschitz constant          < 4.97e-9 < 1e-8,
graph-transform contraction       < 0.535 < 1,
quadratic image constant          < 0.0012897 < 0.01.
```

The stable-component Hessian has leading enclosure
`B_xx=-2.981e13 +/- 4.12e9`; the huge hyperbolic multiplier still makes the
quadratic graph image small after division by the square of the unstable
projection.

The raw determinant of the wide interval Jacobian is inconclusive because
it discards correlations.  It is not used for acceptance.  Local
invertibility instead uses the exact structural identity: every regular
billiard collision preserves `ds wedge dp`, the fourteen-step return is a
composition of such collisions, and the reciprocal eigen-coordinate changes
cancel.  Hence the determinant is exactly one.  All fourteen collision boxes
are independently proved regular and follow the declared first-hit word.

The target sequence after the gray base point is palindromic and the base
momentum is zero.  Exact billiard reversibility

```text
I T^14 I = T^-14,       I(s,p)=(s,-p)
```

swaps the connector eigen-coordinates.  It therefore converts the validated
unstable graph into the actual stable graph

```text
W^s_loc(connector) = {(h_B(y),y): |y|<=3e-12}.
```

At the old shooting ordinate

```text
u=2.186137101021440040809485447235071e-12
```

the missing unstable coordinate is now rigorously bounded by

```text
|h_B(u)| <= 4.77920e-26.
```

The entire correction tube has been replayed through
`T^-14=I T^14 I`; all fourteen physical collisions and strict margins pass.

## 4. Why the true matching is still fail-closed

Both physical graph tubes replay successfully, but ordinary interval state
propagation gives the terminal boxes

```text
QNL ten-collision leg:       theta +/- 2.16e-2,  p +/- 3.71e-2,
connector inverse-14 leg:    theta +/- 3.94e-4,  p +/- 2.38e-3.
```

These are dependency bounds, not geometric widths.  They are far too wide
for the old affine-root Krawczyk box.  Consequently the scripts deliberately
print

```text
TRUE_HETEROCLINIC_MATCHING: NOT CERTIFIED
FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED
```

The next finite task is sharply identified: carry the shooting parameters
as first/second-order polynomial symbols through the ten and fourteen
collision legs, keep a separate Arb remainder, and apply Krawczyk to

```text
T^10 gamma_A^u(t) - T^-14 gamma_B^s(u).
```

No increase in raw Arb precision can replace that correlation-preserving
Taylor replay.

## 5. Reproduction

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate1_qnl_unstable_graph_cert.py \
  deliverables/cm2_gate1_connector_stable_graph_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_qnl_unstable_graph_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_connector_stable_graph_cert.py
sha256sum -c \
  deliverables/cm2-gate1-invariant-graphs-manifest-2026-07-15.sha256
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

Both positive graph certificates exit zero.  The Gate 1 matching and
full-cross labels remain fail-closed.  The frozen v51/v52 files are unchanged.
