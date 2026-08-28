# CM2 Gate 1: true two-graph Krawczyk continuation

Date: 2026-07-15 (Asia/Shanghai)  
Scope: explicit QNL-to-connector heteroclinic vertex on the fixed solid section  
Frozen inputs: v51/v52 and their manifests were read and verified, not edited  
Final Gate 1 status: **PARTIAL CERTIFICATION / FULL-CROSS STILL OPEN**

## 1. Executive verdict

The last affine-vs-invariant-manifold gap in the shooting calculation is now
closed.  A 500-bit Arb certificate proves that the ten-collision image of the
actual local unstable manifold of QNL meets the inverse-fourteen-collision
image of the actual local stable manifold of the connector transversely.

| layer | status |
|---|---:|
| actual `W^u_loc(QNL)` | **CERTIFIED** |
| actual `W^s_loc(connector)` | **CERTIFIED** |
| correlation-preserving 10+14 replay | **CERTIFIED** |
| true two-graph interval Jacobian | **CERTIFIED** |
| true two-graph Krawczyk inclusion | **CERTIFIED** |
| explicit transverse heteroclinic vertex | **CERTIFIED** |
| four-face full crossing at that vertex | **OPEN** |
| common-magnet transported twisting | **OPEN** |

Thus the old warning “the matching seed uses only eigentangents” is retired.
This does **not** close the full Gate 1 magnet claim: no rectangle has yet had
all four face inequalities certified, and no closed common-vertex loop has
had all four transported wedge signs certified.

## 2. Exact problem and certified inputs

Let the two already-certified invariant graphs be

```text
gamma_A(t) = (t,h_A(t)),
|t| <= 2e-9, |h_A(t)| <= t^2, |h_A'(t)| <= 1e-4,

gamma_B(u) = (h_B(u),u),
|u| <= 3e-12, |h_B(u)| <= 0.01 u^2, |h_B'(u)| <= 1e-8.
```

The matching function on the gray solid-collision section is

```text
F(t,u) = T^10 gamma_A(t) - T^-14 gamma_B(u).
```

The second leg is evaluated exactly as `T^-14=I T^14 I`, with the certified
palindromic connector word.  The certificate imports and checks the graph
radii, quadratic constants and derivative bounds from the two predecessor
scripts, so a silent change of any graph class fails closed.

## 3. Why this replay preserves correlation

Ordinary interval propagation lost the shooting parameter at each collision
and produced artificial terminal widths of order `1e-2`.  The new script
keeps, after every collision, a scalar Taylor model

```text
z_i(delta) = c_i + a_i delta + R_i,
```

where `delta` is the original shooting parameter.  At a collision map `f_i`
it evaluates fresh interval bounds for `Df_i` and `D^2f_i` on the reachable
state tube and updates

```text
c_{i+1} = f_i(c_i),
a_{i+1} = Df_i(c_i) a_i,
|R_{i+1}| <= |Df_i(X_i)| |R_i|
             + 1/2 |D^2f_i(X_i)| (|a_i|r+|R_i|)^2.
```

The unknown graph value is placed in `R_0`.  A separate recentered
variational enclosure propagates the uncertainty from `h_A'` or `h_B'`:

```text
d_i = d_i^0 + E_i,
|E_{i+1}| <= |Df_i(X_i)| |E_i|
              + |D^2f_i(X_i)| rad(X_i) |d_i^0|.
```

Consequently the terminal value enclosure and every column of `DF(X)` refer
to the same original parameter; no raw terminal state box is used as a
matching proof.

The Krawczyk set `X` has outward Arb half-widths approximately

```text
|t-t0| <= 4.01e-17,
|u-u0| <= 4.01e-20.
```

For additional protection against construction-radius ambiguity, the
Jacobian replay is evaluated on the strictly larger explicit model radii
`8e-17` and `8e-20`; the script checks that these cover the actual Arb boxes.

## 4. Certified numerical output

The tangent-root center used only as the Krawczyk base point is

```text
t0 = -1.396101069259116746830594312272814391980086...e-9,
u0 =  2.186137101021440040809485447235070543249790...e-12.
```

The actual-graph center residual is enclosed by

```text
|F_theta(t0,u0)| <= 3.65e-12,
|F_p(t0,u0)|     <= 8.90e-12.
```

The true-graph interval Jacobian is enclosed by

```text
[[ 4.68e5 +/- 5.99e2,  -2.986135e8 +/- 5.72e1],
 [ 1.141e6 +/- 6.65e2,  7.287971e8 +/- 4.65e1]],
```

and its determinant satisfies the strict enclosure

```text
det DF(X) = 6.82e14 +/- 7.16e11,
```

so in particular it is positive and bounded away from zero.  With a fixed
rational preconditioner, the Krawczyk image has radii

```text
rad K_t <= 8.56e-18 < 4.01e-17,
rad K_u <= 1.33e-20 < 4.01e-20.
```

Both components are contained in the interiors of `X`.  Hence there is a
unique zero of the actual two-graph matching function in `X`, and the
intersection is transverse.

The largest state-tube radii in the two recentered replays are only

```text
QNL leg       <= 3.36e-11,
connector leg <= 2.10e-11.
```

This is the quantitative removal of the old `1e-2` raw-wrapping artifact.

## 5. Physical-word and first-hit audit

All 24 declared collisions are evaluated on the entire Taylor tubes.  The
joint strict margins are

```text
minimum flight          > 0.1871067,
minimum discriminant    > 0.0102643,
minimum incidence       > 0.6332062,
minimum clearance       > 0.2228385.
```

Every canonical endpoint stays in `(-3/2,3/2)^2`; every cumulative endpoint
stays in the open unit square, so there is no transparent-wall crossing.
The frozen `[-3,3]^2` lift registry is exhausted at every flight, with omitted
coordinate gap at least two.  Thus the declared word is a first-hit word on
the full Krawczyk tube, rather than merely at its center.

## 6. Strict stopping line

The result proves an explicit transverse heteroclinic vertex between the two
actual finite manifold images.  It does not by itself prove a magnet
full-cross.  The remaining finite tasks are:

1. choose quantitative source/target rectangles about the certified root;
2. propagate both parameter faces and both transverse graph-tube faces;
3. certify four strict exit/entry inequalities with the same first-hit word;
4. close the common-vertex loop derivative and re-evaluate the four transported
   twisting wedges on those rectangles.

Until those are complete the labels remain

```text
FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED
TRANSPORTED_TWISTING: NOT CERTIFIED
```

## 7. Reproduction

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate1_true_graph_krawczyk_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_true_graph_krawczyk_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_qnl_unstable_graph_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_connector_stable_graph_cert.py
sha256sum -c \
  deliverables/cm2-gate1-true-graph-krawczyk-manifest-2026-07-15.sha256
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

All three positive certificates exit zero.  The frozen v51/v52 files are
unchanged.
