# CM2 Round 95 — centered reverse-coordinate interval coverage

Date: 2026-07-22 (Asia/Shanghai)

Round 95 replaces the dependency-blown direct reverse interval calculation by
a branch-pinned Arb dual/mean-form Taylor model for the projective map
`q -> (t,p)`.  Every intermediate square root is centered before propagation,
so source-grazing singularities are handled by a one-sided dyadic exhaustion.

The complete Round94 physical-prefix registry contains 10,205 probe gaps on 65
rays.  All gaps are covered:

```text
input gaps:                         10,205
centered interval leaves:           11,759
fully covered rays:                  65/65
unresolved leaves:                       0
maximum endpoint split depth:          105
```

The last depth is used only on 15 source-grazing endpoint leaves.  The initial
plain interval model left 298 radicand failures; operationwise centered mean
forms reduced these to one endpoint leaf on each of 15 rays, and one-sided
depth-120 exhaustion closed all of them.

## Strict boundary

The centered reverse map is now interval-covered, but projecting its image to
an axis-aligned `(t,p)` rectangle discards the strong one-dimensional
correlation.  Such rectangles cannot certify the second owner.  Therefore the
next proof layer must propagate the same `q` dual symbol directly through the
first-owner, second-owner, and third-competitor root comparisons.  Round 95
does not yet install the complete physical-face quotient or any RN/Gate-5 row.

Independent 640-bit replay preserves all counts and per-ray signatures;
3/3 hostile semantic mutations, duplicate JSON keys, and nonfinite values are
rejected.

