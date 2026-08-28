# CM2 Gate 1: true-graph full-cross and transport assault

Date: 2026-07-15 (Asia/Shanghai)  
Scope: explicit QNL-to-connector transition at the certified true-graph vertex  
Frozen inputs: v51/v52 and all predecessor certificates were read, not edited  
Final split verdict: **FULL-CROSS CERTIFIED / TRANSPORTED TWISTING OPEN**

## 1. Executive verdict

The four-face full-cross layer requested after the true two-graph Krawczyk
root is now certified.  The certificate propagates a genuine two-dimensional
QNL eigen-rectangle through the full 24-collision word.  Both parameter faces
exit opposite connector-unstable faces, while the entire transverse
graph-tube, including both of its faces, remains strictly between the two
connector-stable faces.  The complete tube has one immutable first-hit word.

The endpoint transition derivatives in both directions are also certified at
the actual graph vertex.  This does **not** yet certify transported twisting.
The missing object is a finite closed dwell/shadowing orbit joining the
inbound stable endpoint near the connector to its outbound involuted endpoint.
The frozen connector matrix is based at the periodic point; multiplying it
between off-center endpoint transports before that finite loop is validated
would be a base-point error.

| layer | status |
|---|---:|
| actual invariant graphs | **CERTIFIED (predecessors)** |
| true transverse heteroclinic root | **CERTIFIED (predecessor)** |
| sharper correlated graph Krawczyk | **CERTIFIED** |
| four preconditioned graph-face signs | **CERTIFIED** |
| physical 24-collision four-face full-cross | **CERTIFIED** |
| reverse full-cross strip by exact reversibility | **CERTIFIED** |
| actual endpoint transition derivatives | **CERTIFIED** |
| finite closed common-vertex dwell loop | **OPEN** |
| four transported twisting wedges | **OPEN / FAIL-CLOSED** |

## 2. The correlation repair

The earlier true-graph certificate placed an unknown graph ordinate into two
independent physical-coordinate remainders.  That was sufficient for
existence, but it made the root box and every attempted full-cross tube much
wider than the actual dynamics.

The new script retains the ordinate as an independent Taylor variable.  In
QNL eigen-coordinates,

```text
(a,b) -> (s,p)=(a+b, k_A(a-b)),
```

and similarly at the connector.  At every collision it propagates

```text
z(delta_1,delta_2) = c + L delta + R
```

with a two-column affine part.  Thus the cancellation between angle and
momentum belonging to one eigen-coordinate is never broken.  The derivative
is propagated by a separately recentered variational enclosure.  The only
information used about the unknown graph functions is the already-certified

```text
|h_A(t)| <= t^2,       |h_A'(t)| <= 1e-4,
|h_B(u)| <= 0.01 u^2,  |h_B'(u)| <= 1e-8.
```

With a fixed rational preconditioner, the same actual graph root is now
enclosed in outward Arb boxes approximately

```text
|t-t0| <= 7.17e-27,
|u-u0| <= 4.81e-30.
```

The Krawczyk image is much smaller:

```text
|K_t-t0| <= 4.45e-28,
|K_u-u0| <= 6.22e-31.
```

The true-graph matching determinant remains strictly positive,

```text
det DF = 6.815572776013e14 +/- 56.1.
```

This sharpening is a consequence of preserving the graph-ordinate
correlation; it does not assume a fitted value of either invariant graph.

## 3. Independent four graph-face signs

Let `C` be the fixed rational Krawczyk preconditioner and
`G(t,u)=C F(t,u)`.  On

```text
|t-t0| <= 1e-20,   |u-u0| <= 1e-23,
```

the interval derivative satisfies

```text
DG = [[1 +/- 1.42e-14,       +/- 2.38e-13],
      [      +/- 2.23e-17, 1 +/- 3.73e-16]].
```

Direct mean-value evaluation on the four faces gives

```text
G_1(t-) = -1.000000e-20 +/- 2.76e-28 < 0,
G_1(t+) = +1.000000e-20 +/- 2.76e-28 > 0,
G_2(u-) = -1.000000e-23 +/- 4.31e-31 < 0,
G_2(u+) = +1.000000e-23 +/- 4.31e-31 > 0.
```

This is an independent Poincare--Miranda face audit.  It is not used as a
substitute for the physical strip calculation below.

## 4. Explicit physical source and target rectangles

The certified source rectangle in QNL eigen-coordinates is

```text
S_A = {|t-t0| <= 1e-20, |b| <= 2.1e-18}.
```

Its transverse half-width strictly contains the whole actual unstable graph
segment, since

```text
sup_{S_A} |h_A(t)| < 1.949099e-18 < 2.1e-18.
```

The target connector rectangle is

```text
R_B = {|x| <= 1e-8, |u-u0| <= 1e-14}.
```

It lies inside the certified connector stable-graph domain and contains that
graph with enormous margin:

```text
sup_{R_B} |h_B(u)| < 4.824e-26 < 1e-8.
```

For the exact 24-collision transition `H_AB`, the correlation-preserving
Taylor replay proves the strict face inequalities

```text
x(H_AB(t-,b)) = -1.8095880e-7 +/- 6.61e-15 < -1e-8,
x(H_AB(t+,b)) = +1.8095880e-7 +/- 6.61e-15 > +1e-8,

u0-1e-14 < u(H_AB(S_A)) < u0+1e-14.
```

The last enclosure has outward radius below `9.63e-15`.  Both transverse
source faces `b=-2.1e-18` and `b=+2.1e-18` separately satisfy the same strict
entry inequalities.  Hence the image of `S_A` is a full horizontal crossing
of `R_B`, not merely a one-dimensional manifold intersection.

Exact reversibility supplies the opposite transition strip: if the image
strip is restricted to its crossing of `R_B`, applying the billiard
involution to it and to the four inherited faces gives a forward
connector-to-QNL full-cross.  This assertion is about the inherited
curvilinear strip; it does not claim that every point of the ambient target
rectangle follows the reverse word.

## 5. Uniform physical word

The entire two-parameter source rectangle is propagated, not just its centre.
All 24 declared collisions have the same first-hit word and satisfy

```text
minimum flight        = 0.18711 +/- 5.92e-6,
minimum discriminant  = 0.01026432355 +/- 5.91e-12,
minimum incidence     = 0.633206237 +/- 1.58e-10,
minimum clearance     = 0.22283858114 +/- 4.04e-12.
```

The largest physical state radius is below `4.40e-7`.  Every cumulative
endpoint stays in the open fundamental square, and the frozen `[-3,3]^2`
lift registry is exhausted on every flight.  Thus the boundary inequalities
and the word certificate refer to the same Taylor tube.

## 6. What is transported, and what is not

On a box containing the actual graph root, the transition derivative
`D H_AB` is enclosed in QNL-to-connector eigen-coordinates.  Direct interval
composition resolves its first three entries.  The fourth entry suffers the
usual interval cancellation, so it is reconstructed from the exact identity

```text
det D H_AB = k_A/k_B.
```

This follows because every regular billiard collision preserves
`ds wedge dp`, while the two eigen-coordinate changes have determinants
`-2 k_A` and `-2 k_B`.  The resulting fourth entry is strictly positive,

```text
(D H_AB)_{22} = 5.6e-14 +/- 5.61e-16.
```

The remaining entries have the strict sign pattern

```text
(D H_AB)_{11} > 0,  (D H_AB)_{12} < 0,
(D H_AB)_{21} < 0,  (D H_AB)_{22} > 0.
```

The reverse endpoint derivative is then rigorously obtained from

```text
D H_BA = D I_A (D H_AB)^(-1) D I_B,
```

where `D I` swaps the stable and unstable eigen-coordinates.

These are actual endpoint transports.  They still do not form a closed
common-vertex loop.  An inbound point on `W^s(B)` approaches the connector
periodic point, whereas the reverse transition leaves from the involuted
point on `W^u(B)`.  A finite periodic/shadowing orbit must be validated that
enters on the first strip, spends a declared number of connector returns, and
exits on the second strip.  Only the derivative of that finite loop may be
inserted into the four Perron-line wedges.

Consequently the correct stopping labels are

```text
FULL_CROSS_COMMON_VERTEX: CERTIFIED
ACTUAL_VERTEX_TRANSITION_DERIVATIVE: CERTIFIED
CLOSED_COMMON_VERTEX_LOOP_DERIVATIVE: NOT CERTIFIED
TRANSPORTED_TWISTING: NOT CERTIFIED
```

In particular, the four large untransported margins in the frozen v52
certificate have not been relabelled as common-vertex wedges.

## 7. Reproduction

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate1_full_cross_transport_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_full_cross_transport_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_true_graph_krawczyk_cert.py
sha256sum -c \
  deliverables/cm2-gate1-full-cross-transport-manifest-2026-07-15.sha256
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

The new certificate and all three invariant-graph/root predecessors exit
zero.  The frozen v51/v52 artifacts are unchanged.
