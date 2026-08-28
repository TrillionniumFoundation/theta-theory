# CM2 Gate 3 endpoint-identity collar refinement

Date: 2026-07-15  
Arithmetic: 192-bit Arb (`python-flint==0.9.0`)  
Verdict: **one major collar class strictly reduced; maximal rows and global DQ remain open**

## 1. Scope

This is an independent refinement of the depth-nine global physical-subrow
atlas.  It uses exactly the same 384 active signed chart sheets, source-wise
first-hit candidate universe, full 162-lift miss registry, subdivision and
physical labels.  It does not edit or weaken the predecessor certificate.

The separate bulk `Jx` coarea pairing is not repeated here.  This report is
only about the previously unresolved endpoint and polarity collars.

## 2. The redundant endpoint tests

Write `n` for the unit source normal and `j=(-n_y,n_x)` for the oriented
unit tangent.  The tangent construction has

\[
 u=\frac{\ell d+\varepsilon r_T(d_y,-d_x)}{|d|^2},
 \qquad \ell^2=|d|^2-r_T^2.
\]

The two summands in the numerator are orthogonal, hence

\[
 |u|^2=1,
 \qquad c_p=u\cdot n,
 \qquad p=u\cdot j,
 \qquad c_p^2+p^2=1.
\]

Therefore the already-required strict condition `cp>0` automatically gives
`-1<p<1`; separately testing the two inequalities for the interval `p`
only creates dependency width.  Likewise the strict positive radicand used
to construct `ell` already implies `ell>0`.

Removing only these logically redundant tests reduces the endpoint collar
from

\[
 \frac{15573}{51200}
 \quad\hbox{to}\quad
 \frac{1461}{25600}.
\]

The exact removed area is

\[
 \frac{12651}{51200},
 \qquad
 \frac{12651/51200}{15573/51200}=\frac{4217}{5191}
 \approx81.24\%.
\]

No `tau=3` endpoint box remains: every genuine endpoint collar left by the
refined classifier is a source-grazing `cp=0` collar.

## 3. Exact coarea sign factorisation

On every outgoing row, `cp>0` and `ell>0`.  Thus

\[
 \operatorname{sign}\!\left(
   \eta\varepsilon\frac{c_pu_y}{\ell}
 \right)
 =\operatorname{sign}(\eta\varepsilon u_y).
\]

The refined certificate determines polarity from the right-hand factor,
rather than from a wide interval product/quotient.  This removes a further
`17/102400` of artificial polarity collar while preserving the identical
physical coarea sign.

## 4. Refined full atlas

Across all 384 active sheets, the exact depth-nine ledger is now:

| class | boxes | exact parameter area |
|---|---:|---:|
| physical immutable subrow | 11,812 | `5569/25600` |
| strict empty, non-outgoing | 10,084 | `154539/102400` |
| strict empty, occluded | 16,084 | `8235/4096` |
| genuine source-grazing endpoint | 23,376 | `1461/25600` |
| first-visibility collar | 3,192 | `399/51200` |
| miss-owner collar | 14,720 | `23/640` |
| polarity collar | 816 | `51/25600` |

The exact partition is

\[
 \frac{5569}{25600}
 +\frac{180207}{51200}
 +\frac{5263}{51200}
 =\frac{96}{25}.
\]

Relative to the predecessor, total unresolved area drops from

\[
 \frac{35721}{102400}
 \quad\hbox{to}\quad
 \frac{5263}{51200}.
\]

The reduction is `5039/20480`, i.e. the exact fraction `25195/35721`
(`70.53%`) of the old unresolved area.  Certified physical area grows by
`1061/25600`.  The complete labels/components grow from 60 to 64 and still
form 16 exact four-element `Jx/Jy` orbits with zero polarity-weighted
parameter area.  This last statement is only the parameter bulk symmetry;
the separately certified physical bulk coarea pushforward is outside this
artifact's scope.

## 5. Source-grazing normal forms

Let `C=a-c_source`,

\[
 A=C\cdot n-r_S,
 \qquad B=C\cdot j.
\]

At `cp=0`, the radical tangent equation reduces exactly to

\[
 A=\sigma r_T,
 \qquad \sigma=-\varepsilon\operatorname{sign}(B).
\]

Thus the boundary is the smooth scalar equation

\[
 F(z,s)=A(z,s)-\sigma r_T=0.
\]

For 16,304 of the 23,376 endpoint boxes, covering exact area
`1019/25600`, the certificate proves:

- fixed nonzero sign of `B`;
- fixed nonzero sign of `partial_z F`;
- strict opposite signs of both `F` and `cp` on the two `z` faces.

Each such box contains exactly one transverse graph `z=z(s)`.  These boxes
cover the exact fraction `1019/1461` (`69.75%`) of the genuine endpoint
collar.  The remaining edge/corner or derivative-degeneracy area is only
`221/12800`.

This normal-form subatlas identifies the zero-measure boundary geometry, but
does not yet certify one uniform first-visibility/miss-owner label on every
outgoing curved half-box.  Accordingly it is not deducted from the global
unresolved physical-row ledger.

## 6. Fail-closed boundary

This result does **not** certify:

- the remaining `221/12800` source-grazing edge/corner pieces;
- uniform event labels on all outgoing sides of the certified curved graphs;
- maximal connected rows across the remaining collars;
- quotienting rows across the eight chart seams;
- the all-sheet DQ or physical scalar matching outside already certified bulk;
- unconditional CM2.

## 7. Reproduction

```bash
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_endpoint_identity_refinement_cert.py

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_endpoint_identity_refinement_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_endpoint_identity_refinement_verifier.py \
  --self-test

# Deliberately exits 2 while maximal rows/global DQ remain open.
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_endpoint_identity_refinement_verifier.py
```

Artifacts:

- `cm2_gate3_endpoint_identity_refinement_cert.py`;
- `cm2-gate3-endpoint-identity-refinement-manifest-2026-07-15.json`;
- `cm2_gate3_endpoint_identity_refinement_verifier.py`;
- `cm2-gate3-endpoint-identity-refinement-manifest-2026-07-15.sha256`.
