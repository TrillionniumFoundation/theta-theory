# CM2 Gate 3/4 bulk `Jx` coarea-pairing assault

Date: 2026-07-15  
Verdict: **physical scalar pairing certified on the refined 64-component bulk;
collars/global DQ remain open**

## 1. Upgrade over the parameter-area audit

The endpoint-identity refinement certified 11,812 physical immutable boxes,
64 complete labels and 64 connected subrow components.  Its symmetry audit
proved that the labels form 16 `Jx/Jy` four-orbits and that the exact
parameter areas cancel with polarity.  Parameter area alone is not the
physical coarea coefficient law.

The new certificate replays the entire atlas and constructs the actual
boxwise involution.  It finds exactly

```text
11,812 physical boxes
 5,906 Jx box pairs
    32 Jx component-label pairs.
```

For a source chart box, vertical reflection acts by

```text
s -> -s,
E <-> W,
N -> N with z -> -z,
S -> S with z -> -z,
epsilon -> -epsilon.
```

Every reflected rational box is present with the same adaptive depth and
exactly the reflected complete label.  Applying the involution twice returns
the original box.  The pair registry digest is

`fdf210abfca9017aa80dd28785b2826b1c2199a3e56e34e80608afe0a1e65f01`.

## 2. Exact coarea transformation

Under `Jx`,

\[
 (n_x,n_y)\mapsto(-n_x,n_y),\qquad
 (u_x,u_y)\mapsto(-u_x,u_y),
\]

while flight time `ell`, source cosine `c_p=u·n`, `|dt/dz|`, and the
collision-SRB density are invariant.  The signed parameter coarea used by
the atlas is

\[
 c=\eta\,\epsilon\,c_p\,u_y/\ell.
\]

Since `epsilon` reverses, `c` changes sign.  The absolute `(z,s)` Jacobian
of `Jx` is one, so the positive coefficient measures satisfy exactly

\[
 (J_x)_*m_e=m_{J_xe}.
\]

Thus this is a coefficient-law pairing, not a comparison of rounded masses.

## 3. Consequence and boundary

The 5,906 pairs have opposite scalar roof marks and the same positive
coarea law.  Therefore the physical scalar contribution of the certified
bulk is exactly

\[
 \widehat\mu(\dot r)_{\rm certified\ bulk}=0.
\]

This strengthens the earlier four-row example to all 64 certified refined-bulk
components.

It still does not prove arbitrary-test distributional cancellation:
reflected endpoints are generally different points, so a non-`Jx`-invariant
test need not cancel.  More importantly, the refined atlas leaves the exact
fraction `5263/196608` in unresolved collars and has not quotiented every
chart seam.  Hence none of the following is claimed:

- all physical coarea laws including collars;
- maximal global event rows;
- arbitrary-test current cancellation/global DQ;
- Gate 3, Gate 4, Gate 5, or unconditional CM2.

## 4. Reproduction

```bash
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_bulk_jx_coarea_pairing_cert.py

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_bulk_jx_coarea_pairing_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_bulk_jx_coarea_pairing_verifier.py --self-test

# Expected exit 2 while the collars/global DQ remain open.
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_bulk_jx_coarea_pairing_verifier.py
```
