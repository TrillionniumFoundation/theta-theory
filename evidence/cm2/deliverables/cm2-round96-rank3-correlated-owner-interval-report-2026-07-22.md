# CM2 Round 96 — correlated owner/competitor interval frontier

Date: 2026-07-22 (Asia/Shanghai)

Round 96 propagates one centered projective `q` symbol through the reverse
three-collision chain and tests competitors by strict clearance from the
selected flight segment.  Current-obstacle zero roots are excluded at each
departure, as required for an outgoing convex billiard ray.

On the 10,205 Round95 base gaps:

```text
first+second owner certified:       10,180
representation-boundary residuals:     25
third-competitor certified:          1,552
third-competitor residuals:           8,628
```

The 25 representation residuals are 15 centered source-grazing radicands and
10 chart-seam boxes already resolved by the finer Round95 leaf registry; Round
96 deliberately records the depth-zero base-gap frontier rather than silently
reusing those subdivisions.

All substantive residuals are in the third-competitor layer.  They involve
only ten translated lifts:

`G[1,1]`, `G[1,0]`, `W[1,0]`, `G[0,1]`, `W[0,1]`, `G[0,0]`,
`G[1,-2]`, `G[1,2]`, `G[2,-1]`, and `G[2,1]`.

The simple whole-segment clearance test is sufficient on 1,552 gaps but is too
strong on 8,628 gaps: those candidates may intersect the infinite supporting
line while their near root still lies after the designated tangent target.
The lawful next step is a centered near-root order comparison for these ten
candidate families, not deeper blind subdivision.

Independent 640-bit replay preserves the full per-ray and per-candidate
residual signature; 3/3 semantic mutations and malformed JSON are rejected.

No face quotient or gate is promoted.

