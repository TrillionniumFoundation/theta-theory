# CM2 Round159 — upper-tail scale-jump feasibility note

Date: 2026-07-25

## Scope

This is a nonpromotional method note. It neither extends the certified
Round159 corridor beyond `352h` nor changes D02, Gate5 or CM2 status.

## Compact initial coordinates

The pinned physical centered-jet map has the exact angular form

```text
A   = asin(t_star) + delta_x / (R_W sqrt(17))
Phi = asin(P_star) + 4 delta_x / sqrt(17) + delta_beta
R_W = 4/25.
```

Writing `delta_x=-u h` and `delta_beta=v h` gives

```text
A   = A_0 - u h / (R_W sqrt(17))
Phi = Phi_0 + h (v - 4u/sqrt(17)).
```

These compact angles are the natural coordinates for a scale jump. The current
E chart cannot be continued to literal infinity: its first negative chart face
is `A=-pi/4`, at the diagnostic estimate

```text
u_E = R_W sqrt(17) (asin(t_star)+pi/4) / h
    approximately 0.5310439404132798 * 2^4296
    = 2^4295.086903... .
```

There is also the exact physical-state symmetry

```text
(delta_x, delta_beta)
  -> (delta_x + 2 pi R_W sqrt(17), delta_beta - 8 pi R_W),
```

which sends `A` to `A+2pi` and leaves `Phi` unchanged. Exterior-sheet
exclusion should therefore be formulated on a fundamental angular domain,
with explicit chart-face gluing, rather than on an unbounded lifted h-unit
strip.

## Exact diagnostic probes

Round159 fully certifies only the eight slabs in `[320,352]h`.

Separately, a frontier-only exact interval probe used

```text
abs(delta_x)/h in [99998,100002]
C24 beta/h          in [280260,280314]
bridge beta/h       in [280314,280690]
D3 beta/h           in [280690,280716].
```

It obtained:

```text
C24 parametric Newton image  [280276.218423..., 280298.333252...]
bridge anchor exclusion      PASS
bridge terminal class        RETURN_AT_3_INNER
D3 parametric Newton image   [280697.133698..., 280708.361808...]
strict Newton-image gap      > 398.8004458 h.
```

This probe is not a full R1648 certificate and is not included in the
certified atlas.

A direct C24 frontier attempt on the macro box

```text
abs(delta_x)/h in [320,100000]
delta_beta/h    in [465,280314]
```

fails with

```text
nonpositive discriminant:[+/- 0.101]
```

The failure is an unresolved interval-wrapping diagnostic, not a typed
physical event. The present first-order affine model is therefore unsuitable
for a one-box macro tail.

## Required scale-jump certificate

The next engine should operate in `(A,Phi)` and use a high-order Taylor model,
validated continuation with QR/Lohner wrapping control, or an equivalent
rigorous enclosure. It must:

1. export every named non-event margin and its parameter sensitivity for
   owner, flight/discriminant, wall, chart, homogeneity, incidence,
   preterminal core and terminal constraints;
2. exclude the intentional C24 zero when selecting the minimum strict margin;
3. prove positive fibre derivatives for both C24 and D3 graphs;
4. prove the correlated slope inequality
   `D_x C_beta - C_x D_beta > 0` together with a positive initial graph gap,
   rather than subtracting two wide quotient enclosures;
5. advance by validated doubling in physical angular radius until the first
   certified chart, owner, wall, core or other event face;
6. construct and type that face before changing charts;
7. cover the compact fundamental angular domain by branch-and-bound, using
   interval Newton/Krawczyk boxes for zero sets and strict-sign or cemetery
   certificates for their complement;
8. re-establish global candidate completeness outside the current local
   radius-four regime.

If the high-order scale jump cannot be closed, exact 4h continuation remains a
valid but deliberately secondary fallback. No web research was required for
this feasibility diagnosis; the local formulas and interval traces identify
the next implementation target directly.
