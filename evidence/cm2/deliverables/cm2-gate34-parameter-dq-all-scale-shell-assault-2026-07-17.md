# CM2 Gates 3/4: actual-parameter all-scale recovery germs

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: corrected depth-one fixed-gauge DQ and the nineteenth-round
phase-angle shells  
Strict verdict: **the moving-parameter transverse Jacobian is exact on all 64
open maximal occurrence rows.  One positive-width patch in every occurrence
admits actual physical hit/miss recovery germs for every
`0<|h|<=1/65536`.  This closes the phase-angle-versus-parameter gap locally,
but not the full-row tubular atlas, strong grazing pushforward, 24-core
entrance, or Gates 3/4.**

## 1. Exact parameter displacement

Hold the source collision coordinate fixed while translating the physical
white centre by `h`.  In the tangent outgoing frame, every candidate centre
satisfies exactly

```text
ell_j(h) = ell_j + eta_j u_x h,
w_j(h)   = w_j   - eta_j u_y h.
```

For the tangent target, `w_T=epsilon R_T`, hence

```text
Delta_T(h)=2 eta epsilon R_T u_y h-u_y^2 h^2.
```

Comparison with a frozen phase-angle perturbation gives the first-order
clearance identification

```text
d alpha / dh = eta u_y / ell_T.
```

The tangent graph itself has

```text
dp_tangent/dh = -eta cp u_y/ell_T,
signed face coarea = eta epsilon cp u_y/ell_T.
```

The collision coordinate is `dr dp`; therefore the corrected positive face
law has one power of `cp`:

```text
R_source cp |u_y|/ell_T dtheta.
```

The superseded `cp^2` density is explicitly excluded from this chain.

## 2. Actual all-scale parameter germs

For each of the 64 occurrence rows, adaptive 512-bit Arb replay selects one
base patch and proves the physical itineraries for every

```text
0 < |h| <= 1/65536.
```

The sign convention is now the actual moving parameter:

```text
hit side:  sign(h)=corrected coarea polarity,
miss side: sign(h)=-corrected coarea polarity.
```

The hit discriminant factors as a positive linear factor times `|h|`; the
miss discriminant has the opposite strict sign.  The grazing square root is
bounded by `1/256`, so the replay includes the zero-scale limit without
taking an Arb square root of a ball whose lower endpoint rounds below zero.

Adaptive base half-widths are

```text
1/1024:  40 rows,
1/2048:  16 rows,
1/4096:   4 rows,
1/16384:  4 rows.
```

The 64 labelled patches have total `(z,s)` coordinate area
`2833/16777216`; both parameter sides through radius `1/65536` have labelled
coordinate volume `2833/549755813888`.  No invariant-mass interpretation is
claimed for these coordinate totals.

## 3. Physical FACE-time seeds

Against the complete 161-candidate local universe on each leg, every germ
has

```text
hit:  source -> tangent target -> fixed miss target,
miss: source ------------------> fixed miss target.
```

Thus the selected physical collision-time offset is exactly one.  Both sides
land in the same regular suffix chart, with

```text
successor cos(phi) > 1/20,
successor |p|      < 999/1000,
each owner flight  < 2.
```

This is a local `FACE_TIME` seed.  It is not yet the common strong-space
`FACE_TIME` operator or its summability estimate.

## 4. Strict frontier

The exact Jacobian is global on each open maximal row, but the finite Arb
shells cover one selected patch per occurrence.  Endpoint collars and the
remaining points of every maximal row have not been assembled into a full
tubular atlas.  Consequently no bounded grazing pushforward follows.

The regular suffix states have not been transported to the first one of the
24 contracting collision rectangles, and no `2018/12108` hidden-recut audit
has been performed.  The common strong Banach space remains absent.

```text
PARAMETER-ANGLE JACOBIAN ON 64 OPEN ROWS:       CERTIFIED
SELECTED ACTUAL-PARAMETER ALL-SCALE GERMS:      64 CERTIFIED
ORIENTED ACTUAL-PARAMETER TUBE GERMS:          128 CERTIFIED
SELECTED PHYSICAL FACE-TIME OFFSET:              1 CERTIFIED
FULL-BOUNDARY ALL-SCALE TUBULAR ATLAS:           NOT CERTIFIED
BOUNDED STRONG-SPACE GRAZING PUSHFORWARD:         NOT CERTIFIED
FIRST 24-CORE DESTINATION:                        NOT CERTIFIED
NATIVE 2018/12108 NO-RECUT DWELL:                 NOT CERTIFIED
GATE 3:                                           NOT CERTIFIED
GATE 4:                                           NOT CERTIFIED
```
