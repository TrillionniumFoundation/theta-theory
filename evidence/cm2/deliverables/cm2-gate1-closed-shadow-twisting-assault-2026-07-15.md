# CM2 Gate 1 closed-shadow transported-twisting assault

Date: 2026-07-15  
Model: frozen centered rational fixed-section pilot  
Scope: finite closed shadow loop after the certified true-graph full crossing  
Status: **shadow loop/wedges CERTIFIED; strict QNL-fiber holonomy typing OPEN**

## 1. Result

The missing finite dwell/shadowing route now exists and is certified.  A
900-bit Arb interval-Newton calculation gives a unique reversible shooting
root

```text
a_* in -8.2937621943296019634374270464521040562...e-15 +/- 3.60e-200,
p_*=0.
```

Starting there, the 48-collision half word

```text
Q^10 B^2
```

ends again on the time-reversal line `p=0`.  Here `Q` denotes one
two-solid-collision QNL return and `B` denotes one
fourteen-solid-collision/period-eight fixed-section connector cycle.  The
stored ten-collision `QNL_FORWARD_WORD` is `Q^5`.  Exact billiard
reversibility reflects the half word and produces the closed word

```text
Q^10 B^4 Q^10,
```

with 96 solid collisions and zero cumulative lattice lift.

The dynamically typed factorisation is

```text
A_out * H_BA * B_out * B_in * H_AB * A_in.
```

The middle `B_out * B_in` is a positive connector dwell of two complete
connector cycles, or 28 solid collisions.  `A_in,A_out` are the necessary
five-QNL-return outer dwells.  They are not cosmetic: an exact noncentral
point on `W^s(B)` cannot be sent by finitely many connector returns directly
to its involuted point on `W^u(B)`.  The closed object must be a nearby
shadowing orbit, and closure also requires the QNL-side dwell.

## 2. It uses the already-certified full-cross branch

After `A_in`, the exact shadow orbit lies strictly in the source rectangle
of `cm2_gate1_full_cross_transport_cert.py`.  In QNL eigen-coordinates,

```text
a_source - t_full-cross = -2.4892976627...e-35,
b_source                = -4.9270443526...e-20.
```

The certified source half-widths are

```text
|a-t_full-cross| < 1e-20,
|b|              < 2.1e-18.
```

Following the exact 24-collision `H_AB` word from that same endpoint gives
the connector coordinates

```text
x_in = -5.9742689208951...e-27,
y_in =  2.186137101021440040806762675...e-12.
```

These lie strictly in the certified connector target rectangle

```text
|x| < 1e-8,
|y-u_full-cross| < 1e-14.
```

One connector block reaches the reversible midpoint

```text
x_mid = y_mid = 2.03362263524278336745...e-20.
```

Reflection supplies the second dwell block and hence sends
`(x_in,y_in)` to `(y_in,x_in)`.  The reverse full-cross then supplies
`H_BA`.  Thus this is not a product of a connector matrix based at its
periodic point with unrelated endpoint matrices; it is one physical closed
orbit crossing the predecessor's source and target rectangles.

## 3. Root and physical-word certificate

For the half-endpoint momentum `f(a)`, the certificate proves

```text
f'(a) = 2.2199703455161725986...e27 > 1e22
```

throughout the declared root box and verifies the strict interval-Newton
inclusion.  On the entire half-root box it also obtains

```text
minimum flight        > 0.18710678118,
minimum discriminant  > 0.01026432354,
minimum incidence     > 0.63320623699,
minimum clearance     > 0.22283858113.
```

Every collision point stays in the open fundamental square.  All gray and
white lifts in `[-3,3]^2` are checked on every flight, and the frozen exact
exterior-lift bound handles the complement.  The reverse half inherits the
same strict margins.  A separate full-word point replay contains zero in
both closing residuals and finishes at cumulative lift `(0,0)`; exact
closure itself comes from the interval root plus reversibility, not from
that point diagnostic.

The frozen radii `9/25` and `4/25` are recreated as the same exact rational
Arb objects after precision is raised from the predecessor's 400 bits to
900 bits.  This avoids importing 400-bit rounding radii into the much
longer hyperbolic replay.  No table parameter, root seed, v51/v52 artefact,
or predecessor certificate is modified.

## 4. Same-orbit derivative chain

All forward matrices are evaluated successively at interval boxes
containing consecutive endpoints of the exact half orbit:

```text
D_half = D B_in * D H_AB * D A_in.
```

The script checks overlap of this chain-rule product with a direct
48-collision derivative, entry by entry.  The paired reverse matrices are
then obtained only from the exact relation

```text
D(I F^{-1} I) = S (D F)^{-1} S,
S = diag(1,-1),
```

at the corresponding reflected endpoints.  Since every regular billiard
collision preserves `ds wedge dp`, each segment has determinant one and its
fourth entry is reconstructed from that exact identity.  The complete
six-factor product is checked against the correlated half-map formula.

For

```text
H = D_half = [[a,b],[c,d]],  det H=1,
```

the closed derivative is

```text
L = S H^{-1} S H
  = [[ad+bc, 2bd],
     [2ac,    ad+bc]].
```

The certified enclosure is positive and has trace greater than `1e53`, so
the loop is proximal.  Its determinant is exactly one by the displayed
identity.

## 5. Four transported wedges

Let

```text
v_+ = (1,k_A),
v_- = (1,-k_A)
```

be the two QNL Perron lines in the same canonical gray `(s,p)`
trivialisation.  Because the connector word is now an actual closed route
through the full-cross rectangles, these are finite-shadow-basepoint
transported wedges from one same-orbit derivative chain, rather than the old
product of matrices at unrelated endpoints.  Whether they are identified
with a Bonatti--Viana holonomy endomorphism on the exact QNL periodic fiber is
the separate fail-closed typing choice stated below.  Arb proves

```text
det(v_+, L v_+) = -4.0146568962138184860...e28,
det(v_-, L v_+) =  1.4538820777648600323...e54,
det(v_+, L v_-) =  1108.5816546480524866...,
det(v_-, L v_-) = -4.0146568962138184860...e28.
```

The accepted strict thresholds are, respectively,

```text
< -1e28,  > 1e54,  > 1000,  < -1e28.
```

Consequently the finite-shadow labels are now

```text
CLOSED_COMMON_VERTEX_LOOP_WORD: CERTIFIED
SAME_BASEPOINT_DERIVATIVE_CHAIN: CERTIFIED
CLOSED_COMMON_VERTEX_LOOP_DERIVATIVE: CERTIFIED
TRANSPORTED_PINCHING: CERTIFIED
TRANSPORTED_TWISTING: CERTIFIED
FINITE_CLOSED_SAME_ORBIT_SHADOW_LOOP: CERTIFIED
FINITE_SHADOW_TRANSPORTED_TWISTING: CERTIFIED
```

They do **not** by themselves certify the stronger fiber-typing statement

```text
BONATTI_VIANA_QNL_FIBER_HOLONOMY_IDENTIFICATION: NOT CERTIFIED
GATE1_UNCONDITIONAL_TYPICALITY_INPUT: OPEN / FAIL-CLOSED
```

If the final typicality theorem is invoked in the Bonatti--Viana form, its
twisting loop is a stable/unstable holonomy loop whose endomorphism acts on
the fiber over the QNL periodic point itself.  The new matrix `L` acts on
the exactly closed shadow basepoint `z_*`, in the same canonical gray chart,
and its orbit passes through the certified full-cross rectangles.  That is
enough for the finite same-orbit statement proved here, but identifying it
with the QNL-periodic-fiber holonomy endomorphism requires an additional
certified stable/unstable holonomy limit (or a theorem explicitly accepting
the common-chart finite-shadow formulation).  No such theorem choice or
holonomy-limit certificate is silently assumed here.

## 6. Shortest dependency chain and remaining typing choice

The certified chain is exactly:

1. frozen regular QNL and connector periodic words, canonical area, and time
   reversal;
2. certified local invariant graphs and the true-graph `H_AB/H_BA`
   full-cross rectangles;
3. this 900-bit interval-Newton root for one 96-collision closed shadow word;
4. consecutive endpoint derivatives on that word and the four nonzero
   transported wedges at its closed basepoint.

The only further dependency needed for the strict Bonatti--Viana reading is:

5. stable/unstable holonomy identification transporting the shadow-loop
   endomorphism to the exact QNL periodic fiber, with the four wedge signs
   retained there.

Thus the finite shadow route is no longer an obstruction.  The theorem-level
typing choice in item 5 remains fail-closed.

## 7. Scope discipline

This closes the finite geometric/derivative obstruction left by the
predecessor: one actual closed word, one consecutive endpoint chain, and
four strict transported wedges.  It does **not** automatically close the
unconditional Gate 1 typicality input under the strict holonomy-fiber
reading above.  It also does **not** prove Gate 2's full-mass physical
quotient, conditional Gibbs-weight lower bounds, stopped-parent PPE,
normalized amplitude registry, or same-carrier endpoint-amplitude identity.
It also does not supply Gate 3--5 event/DQ/CM2-transfer data.  Those layers
remain separately fail-closed.

## 8. Reproduction

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate1_closed_shadow_twisting_cert.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_closed_shadow_twisting_cert.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_full_cross_transport_cert.py

sha256sum -c \
  deliverables/cm2-gate1-closed-shadow-twisting-manifest-2026-07-15.sha256

sha256sum -c deliverables/cm2-v52-manifest.sha256
```

The new certificate and the frozen full-cross predecessor both exit zero.
The new manifest and the frozen v52 manifest must report every line `OK`.
