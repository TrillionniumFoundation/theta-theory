# CM2 Gates 2/5: selected-component reachability pruning

Date: 2026-07-17 (Asia/Shanghai)  
Strict verdict: **the selected component
`7359148d...b5` has a one-interval, contracting component-local
characteristic theorem; this is not a full-key field and Gates 2/5 remain
`NOT_CERTIFIED`.**

## Exact full-window pruning

For the selected `G:E -> W[0,0]` branch write `a=1/2+s`,
`c=sqrt(1-t^2)`,

```text
A=a*c+t/2-9/25,  B=c/2-a*t,
T=c_p B-p A,     p_1=T/(4/25).
```

If `t<=0`, then `B>7/20`, `|A|<29/80`, hence
`T>179/800>6/125`.  If `0<=t<=1/2`, then
`c>43/50`, `B>143/800`, `|A|<157/400`, hence

```text
T > 833/16000 = 6/125 + 13/3200.
```

Thus target centrality `|p_1|<3/10` forces `t>1/2`, uniformly for
`|s|<=1/400`.  Consequently `pi/6<theta<pi/4`, `|phi|<pi/6`, and both
coordinates of the outgoing velocity are positive.

The source point has `x>63/250,y>9/50`; the target contact lies in

```text
x in (27/80,53/80), y in (17/50,33/50).
```

The segment is coordinatewise increasing inside the open unit square, so it
crosses no transparent wall.  The three other nearby gray lifts have strict
squared-distance margins

```text
G[1,0]: 2673/160000,
G[0,1]: 1547/31250,
G[1,1]: 3197/32000.
```

All other white lifts are excluded by one coordinate distance greater than
`4/25`; all remaining gray lifts are farther still, and the outgoing ray
cannot re-enter the convex source.  Therefore `W[0,0]` is automatically the
strict first solid collision.  Moreover the target `(-1,-1)` chart dot is
strictly greater than `19/20-3/10=13/20`.

Hence on the pruned physical predicate `P` the 402-entry over-ledger reduces
to

```text
G:E source chart AND |p_0|<3/10 AND |p_1|<3/10.
```

This statement concerns physical word/owner/wall/chart predicates.  It does
not claim that every raw algebraic equality in the over-ledger is nonzero
outside the physical role in which that equality was introduced.

## Why the pruned predicate is the selected component

The interval conclusion needs the full two-dimensional predicate to be one
connected component, not merely interval intersections for an outer set.  For
each fixed `s`, after the quadrant forcing above, put

```text
D=(1/2,1/sqrt(2))_t x (-3/10,3/10)_p,
P={(t,p) in D: |T(t,p)|<6/125}.
```

On `D`, with `a in [199/400,201/400]` and `7/10<c<9/10`,

```text
A>953/4000,       |B|<161/800,
partial_p T < -13277/76000 < 0,
partial_t T < -11/64 < 0.
```

The derivative bounds follow directly from

```text
partial_p T=-(p/c_p)B-A,
partial_t T=-c_p(a+t/(2c))+p(at/c-1/2),
```

using `c_p>19/20`, `|p/c_p|<6/19`, and `t/c<1`.  The three decisive side
signs are

```text
T(t,-3/10) > 2759/40000 > 6/125,
T(1/2,p)   > 833/16000  > 6/125,
lim_{t->1/sqrt(2)} T(t,3/10)
             < -2759/40000 < -6/125.
```

Thus `V(t)=T(t,3/10)` is continuous and strictly decreasing and crosses
`+6/125` and then `-6/125` exactly once.  The nonempty `t` projection of `P`
is a single open interval.  For every such `t`, strict monotonicity in `p`
makes the fibre a single open interval; its two endpoints are continuous by
the uniform implicit-function bound.  Joining each point vertically to the
continuous midpoint section proves that `P` is path connected.

The frozen full-window corridor contains the original positive seed and lies
strictly inside the exact word/chart/homogeneity predicate.  Since every
other physical word/chart predicate is automatic on `P`, this connected `P`
is exactly the seeded maximal component `M`, rather than merely an outer
superset of it.

## One interval and contraction

Now that `P=M` is established, intersect it with a canonical unstable graph.
The source chart and source-central restrictions are intervals.  The
target-central restriction is also an interval because the frozen exact
positive-entry Birkhoff matrix gives

```text
d phi_1/d r_0 = -(C+D V)/c_1 < 0.
```

Their intersection is one interval.  Therefore

```text
selected-component multiplicity <=1,
Z_*(1_M F) <= (2000/1999) Z_*(F),
b_core=(2000/1999)*(360134800/360493663)
      =720269600000/720626832337
      =1-357232337/720626832337 <1.
```

This certifies a contracting **selected-component-local field-7 seed only**.
It is not asserted for the other 23 seeded components, other components of
the same word key, or the full 441,280-key registry.  It constructs no stable
quotient, reverse weights, PPE, complete 18-field block, Kac or phase lift.

## Replay

```bash
PY=/tmp/cm2-flint-venv/bin/python
PYTHONPATH=deliverables $PY -m py_compile \
  deliverables/cm2_gate25_selected_component_reachability_pruning_cert.py \
  deliverables/cm2_gate25_selected_component_reachability_pruning_verifier.py
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_selected_component_reachability_pruning_verifier.py \
  --replay --integrity-only
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_selected_component_reachability_pruning_verifier.py \
  --self-test
# Expected exit 2.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_selected_component_reachability_pruning_verifier.py
```
