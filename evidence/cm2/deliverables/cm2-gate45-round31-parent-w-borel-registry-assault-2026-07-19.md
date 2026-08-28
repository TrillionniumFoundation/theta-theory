# CM2 Gate 4/5 round 31: actual parent-W Borel registry

Date: 2026-07-19  
Status: **parameterized actual parent-W registry certified; Gate 4/5 remain open**

The former zero-instance blocker came from asking for a finite list of curves
inside a two-dimensional Q2 restriction. The correct object is a standard
Borel parameterized registry. On each fixed parameter fibre and each of the
114,006 Q2 atoms, define

```text
phi(r)=4r+b,    p(r)=sin(4r+b).
```

The intercept is uniquely `b=arcsin(p)-4r`. Hence every atom point belongs to
one leaf, and each leaf intersects a rectangular atom in either the empty set
or one connected interval. Its phase slope is exactly 4, strictly inside the
certified invariant cone

```text
25/9 < dphi/dr < 4108425/145348 < 29.
```

Partition every oriented leaf intersection at deterministic Euclidean
arclength multiples of `1e-90`. These cells are far shorter than the certified
small-curve threshold `1/37724355673552103994`, have phase-graph C2 seminorm
zero, and carry IDs

```text
parent-W:(time2-atom-id):(s,b):(natural-short-cell-k).
```

Joining these IDs to the 228,012 Q2 branch rules produces the actual
parameterized recut-instance key

```text
(branch-rule-id,parent-W-id,natural-index-j).
```

For each image parent of adapted length `L`, the registry fixes the
instance-level formulas `ceil(L/1e-90)` natural cells and
`max(ceil(L/1e-90)-1,0)` internal recut endpoints. This is the correct F7
endpoint numerator on each actual parameterized instance; its
family-integrated numeric charge is still absent.

This resolves the typed existence/identity blocker without inventing a finite
curve count. It does not yet price F7 boundary characteristic charges or
construct connected nonempty physical face pieces and their numerical
coarea/trace rows. F14--F18 remain absent, Gate 5 remains open, and CM2 remains
no-go.
