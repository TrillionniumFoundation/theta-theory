# CM2 Gate 4 finite-`s` common-mesh and recovery assault

Date: 2026-07-16

## Verdict

This assault strictly certifies three layers on the complete parameter window
`|s|<=1/400`:

1. one moving-endpoint collar/rank/mesh rule for all 64 maximal physical rows;
2. an explicit finite-`s` initial standard-family constant
   `C_mesh=69986663973833932800`;
3. uniform one-time controlled stopped-parent recovery for each fixed `s`,
   with a depth-plus-recovery exponential moment for some `gamma>0`.

It does **not** certify Gate 4.  The uniform Growth Lemma constants are
theorem-supplied but not numerically evaluated, so the final propagated
`C_fw,C_rev,q` remain nonnumeric.  Native dynamical stopping antichains,
hereditary recovery after repeated indicator cuts, and registration of the
moving dyadic endpoints in the Gate 3 common DQ atlas also remain open.

## 1. Complete finite-`s` endpoint and core cover

The replay imports the certified 64 maximal connected event rows over the full
parameter window.  Each row is parameterized by inward angular distance from
its two moving analytic boundaries.

### Moving endpoint collars

The common inward collar is `1/48`.  It is divided initially into 32 exact
angular cells per endpoint, then adaptively in `s`.  Arb interval arithmetic at
384-bit precision certifies all 128 endpoint incidences:

| endpoint kind | count | strict inward derivative lower bound |
|---|---:|---:|
| source grazing | 32 | `9/10` |
| parameter polarity | 16 | `1/6` |
| earlier occlusion | 16 | `1/16` |
| later miss switch | 64 | `1/32` |

Every nonactive incidence scale on these collars is strictly larger than
`2^-20`.  The cover has 20,104 leaves, maximum `s`-subdivision depth 5, and
digest

```text
09f59ea2a1b1381187245e0160287554d9f122b02e087fe63857f51c041319cf
```

### Moving cores

Every row has angular width strictly larger than `1/16`; removing a `1/48`
collar at each end leaves a core of width strictly larger than `1/48`.  The
core replay uses 64 exact `s` cells per row and 16 initial normalized angular
cells, with adaptive angular refinement.  All of

```text
cp_source, |u_y|, cp_miss^2, left-boundary germ, right-boundary germ
```

are strictly larger than `2^-20` on every core box.  The cover has 110,336
leaves, maximum angular subdivision depth 6, and digest

```text
c34e6b0fedf0a9ca6303a72e4e06bbfaa65f8478965d6087d8519f67ec8a2a3f
```

The left- and right-anchored core formulas are pointwise identical.  Anchoring
each half at its nearest analytic endpoint removes a harmless interval
dependency that otherwise obscures the positive collar margin.

## 2. Uniform rank tail and one-collision geometric costs

Define the finite-`s` rank by

```text
B_s=20 on the core,
B_s=max(20,ceil(log2(1/scale_s))) on the unique active endpoint collar.
```

The collars are pairwise disjoint.  The four endpoint estimates give, for
every `s` and every integer `b>=20`,

```text
sum_e m_{e,s}{B_s>b} <= (4839232/3125) 4^-b.
```

Consequently

```text
integral 2^B_s dm_s <= 43293270343755613/25600000
```

before the standard-family boundary normalization.  The previously certified
chart/test, log-density, and carrier-C2 charges propagate uniformly to

```text
C_fw^(geom)(s,a), C_rev^(geom)(s,a) <= 204 * 2^B_s(a).
```

This is only the one-collision geometric subcost, not the complete numerical
forward/reverse cost.

## 3. Explicit density-regular mesh

For a zero-endpoint shell of rank `b>=20`, use

```text
delta_b = 2^-ceil(3(b+1)/2).
```

The replay uses the uniform bounds

```text
carrier shell length <= 2^17 2^-b,
density <= 23 2^-b,
|d log rho/dr| <= 52/scale,
delta_b^2 <= 2^-3(b+1).
```

Pairing the even and odd shells gives the exact convergent one-endpoint
boundary series

```text
Z_endpoint <= 23(1536+2^-19) = 18522046487/524288.
```

On a row core,

```text
mass > (4/25) 2^-20 2^-20 (1/16-2/48)/3
     = 1/989560464998400.
```

Thus every fixed-`s`, depth-`K`, one-time stopped atom has both oriented
standard-family boundaries bounded by

```text
Z_{s,fw}(K,j), Z_{s,rev}(K,j)
    <= 69986663973833932800 * 2^K.
```

This is a fully numerical initial `C_mesh`; the mesh rule is common in `s`,
while its dyadic endpoints move with the coordinates `u_{e,s}`.

## 4. Explicit common finite horizon

The old 35,024-leaf standard-section cover is replayed while retaining a
dyadic penetration margin.  Every leaf has a rational witness time in
`[3/4,3]` and squared slack into a fixed disk core strictly larger than

```text
delta = 2^-19 = 1/524288.
```

No refinement beyond the frozen 35,024 leaves is needed; maximum binary depth
is 14.  Since every physical radius is at most `9/25<1`, the physical
incidence factor satisfies the conservative bound

```text
sin^2(incidence) > delta/(9/25)
                 = 25/4718592
                 > (1/512)^2.
```

Hence the compact table path lies in one explicit Stenlund--Young--Zhang
finite-horizon class with

```text
(t,phi)=(3,1/512),  tau_bar_min=1/25,
curvature in [25/9,25/4].
```

The horizon leaf digest is

```text
b34c66989be6bb2c738eb8185096a1903a96c108d316d768978cd7514d77d6c7
```

## 5. Uniform one-time recovery

The theorem is applied on the usual solid-boundary collision section
`N=G disjoint-union W`.  For each fixed `s`, use the canonical fixed-obstacle
gauge and the constant configuration sequence

```text
K_s,K_s,K_s,...,       T_s=F_{K_s,K_s}.
```

This does not identify the transparent/fixed-section map with the
source-target moving-configuration map `F_{K',K}`.

Stenlund--Young--Zhang, *Dispersing billiards with moving scatterers*,
[arXiv:1210.0011v4](https://arxiv.org/abs/1210.0011), Lemma 12 and Lemma 16,
provide constants `C_p>1` and `0<vartheta_p<1`, uniform over the configuration
class, such that

```text
Z_n/mu <= C_p/2 (1 + vartheta_p^n Z_0/mu).
```

With the explicit initial `C_mesh`, set

```text
A0 = ceil(log(C_mesh)/|log(vartheta_p)|)+1,
A1 = ceil(log(2)/|log(vartheta_p)|).
```

Then both orientations obey

```text
R_fw+R_rev <= 2A0+2A1 K.
```

Combining this with the certified depth law
`P(K)=(3/4)4^-K` gives

```text
E[2^K exp(gamma(R_fw+R_rev))] < infinity
for every 0<gamma<log(2)/(2A1).
```

For each fixed `s`, the one-time `(K,j)` atom is cut using `u_{e,s}`.  Forward
and reverse orientations share the same fixed-`s` restricted measure and the
same `(s,K,j)` record.

## 6. Exact scope boundary

Certified:

- finite-`s` moving endpoint collars and core cover;
- common-in-`s` mesh rule with moving endpoints;
- explicit numerical initial `C_mesh`;
- uniform one-time controlled stopped-parent recovery;
- the depth-plus-recovery exponential moment for some `gamma>0`;
- uniform numerical one-collision geometric coefficient 204.

Not certified:

- numerical values of the theorem constants `C_p,vartheta_p`, hence numerical
  `A0,A1` and complete propagated `C_fw,C_rev,q`;
- native dynamical stopping antichains;
- hereditary recovery under repeated indicator cuts;
- registration of the moving dyadic endpoints in the Gate 3 common DQ atlas,
  or common branch-record MT_DQ;
- physical prefix/suffix constants and all three CM2 norm lifts;
- Gates 3, 4, or 5.

Thus the strict global result remains **unconditional CM2 NO-GO**.

## 7. Reproducibility and fail-closed behavior

Certificate and verifier:

```text
deliverables/cm2_gate45_finite_s_common_mesh_recovery_cert.py
deliverables/cm2_gate45_finite_s_common_mesh_recovery_verifier.py
deliverables/cm2-gate45-finite-s-common-mesh-recovery-manifest-2026-07-16.json
```

Run with `python-flint==0.9.0`:

```bash
PY=/tmp/cm2-flint-venv/bin/python
$PY -m py_compile \
  deliverables/cm2_gate45_finite_s_common_mesh_recovery_cert.py \
  deliverables/cm2_gate45_finite_s_common_mesh_recovery_verifier.py
$PY deliverables/cm2_gate45_finite_s_common_mesh_recovery_verifier.py \
  --replay --integrity-only
$PY deliverables/cm2_gate45_finite_s_common_mesh_recovery_verifier.py \
  --self-test
$PY deliverables/cm2_gate45_finite_s_common_mesh_recovery_verifier.py
```

The first two verifier modes exit 0.  The live default prints the three local
certifications, then prints the missing propagated numerical costs and Gate 4
as `NOT_CERTIFIED`, and exits 2.

