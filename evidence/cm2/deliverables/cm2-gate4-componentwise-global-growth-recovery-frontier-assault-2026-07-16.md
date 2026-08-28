# CM2 Gate 4 componentwise global Growth/recovery frontier assault

Date: 2026-07-16 (Asia/Shanghai)

## Verdict

This assault closes the contraction-weighted **global one-step** join that was
missing from the twelfth-round Gate-4 frontier.  It does so without identifying
the 35,024 horizon boxes with collision components and without charging all 448
conservative candidate rows as physical branches.

For every fixed `|s|<=1/400` and every invariant-cone unstable curve of
Euclidean phase-space length at most

```text
delta_1 = 1/37724355673552103994,
```

there is at most one central homogeneity child globally.  With the enlarged
homogeneity cutoff `k0=6121`, every high-strip child of all at most 153 true
continuity components has one combined tail strictly below `1/5`.  Therefore

```text
Xi_1(delta_1)
 < 144000/180337 + 1/5
 = 900337/901685
 = 1 - 1348/901685
 < 1.
```

This is the requested compressed typed
`component multiplicity x inverse expansion` join and a strict global
one-step weighted Growth contraction.  It is neither the old single-branch
`q_branch` nor the final same-occurrence CM2 `q`.

The full numerical Growth-Lemma recovery constants remain open.  In
particular, the frozen distortion constant applies only to the 128 initial
oriented carriers, not to every iterated standard curve.  Hence no value is
assigned to `C_p`, `vartheta_p`, `A0`, `A1`, `C_fw`, `C_rev`, or the final
`q`.  No unnormalised/reweighted native recovery theorem is manufactured.

```text
TYPED COMPONENTWISE GROWTH JOIN:                    CERTIFIED_COMPRESSED
GLOBAL ONE-STEP WEIGHTED GROWTH CONTRACTION:        CERTIFIED
FULL NUMERIC GROWTH-LEMMA CONSTANTS:                NOT CERTIFIED
NUMERIC C_p,vartheta_p:                             NOT CERTIFIED
UNNORMALISED/REWEIGHTED NATIVE RECOVERY:            NOT CERTIFIED
COMPLETE NUMERIC C_fw,C_rev,FINAL q:                 NOT CERTIFIED
GATE 4:                                              NOT CERTIFIED
```

Evidence:

- `deliverables/cm2_gate4_componentwise_global_growth_recovery_frontier_cert.py`;
- `deliverables/cm2_gate4_componentwise_global_growth_recovery_frontier_verifier.py`;
- `deliverables/cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json`;
- `deliverables/cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.sha256`.

## 1. Frozen inputs and the corrected type map

The four counts used in the old diagnostic have different types.

| Count | Exact role in this assault |
|---:|---|
| `35,024` | ambient position-direction witness boxes proving `tau<3`; used only through that uniform scalar bound |
| `448` | conservative `(source chart,target lift)` owner candidates; not physical children |
| `288` | chart-quotiented raw signed tangency sheets: 152 for a gray source and 136 for a white source |
| `153` | maximum number of true continuity components of one curve after its at most 152 physical raw-sheet intersections |

The certificate independently replays the exact rational candidate reduction,
including the frozen per-chart digests:

```text
G:E,G:W,G:N,G:S = 57 each,
W:E,W:W,W:N,W:S = 55 each,
total chart candidates = 448.
```

Quotienting chart duplication gives

```text
76 gray-source owner targets + 68 white-source owner targets = 144 owners,
2 signed sheets per owner = 288 raw sheets.
```

No horizon leaf is assigned a collision-curve ID.  No candidate is charged
merely because it survived the horizon/outgoing-halfspace pruning.  Given a
concrete short curve `W`, the physical join is generated in this order:

```text
(s,source,W)
 -> visible intersections with the 288 raw sheets
 -> ordered true continuity components (W,j)
 -> unique first-visible owner T(W,j)
 -> target homogeneity child
 -> multiplicity and adapted inverse expansion.
```

Thus the component ID is relative to the actual curve being tested, as it must
be.  The compressed theorem below supplies the uniform multiplicities needed
to sum the infinitely many homogeneity ranks without materializing an
impossible finite list of all short curves.

## 2. A numerical central-to-tangency collar

Fix one source obstacle, orient `W` so that `dr>0`, and write

```text
25/9 < V=dphi/dr < 29.
```

For a selected target `T`, set

```text
d=a_T-q(r),
w=u_perp dot d,
Delta_T=R_T^2-w^2=R_T^2 c_1^2.
```

Along a physical branch, `tau<3`, hence

```text
|d| < 3+9/25 = 84/25.
```

Moreover `|d'|=1`, `|u_perp'|=|kappa+V|`, and
`kappa<=25/4`.  Exact rational arithmetic gives

```text
|w'|
 < 1 + (84/25)(25/4+29)
 = 2986/25,

|Delta_T'|
 < 2(9/25)(2986/25)
 = 53748/625.                                      (2.1)
```

For cutoff `k0=6121`, a central child satisfies the standard central-strip
inequality

```text
c_1 > 1/(2 k0^2).
```

Since every target radius is at least `4/25`, its discriminant obeys

```text
Delta_T
 > (4/25)^2 /(4 k0^4)
 = 4/(625 k0^4).                                    (2.2)
```

Equations (2.1)--(2.2) imply that a central point is separated in source
`r` from any selected tangency endpoint of the same true branch by more than

```text
[4/(625 k0^4)] / [53748/625]
 = 1/(13437 k0^4)
 = 1/18862177836776051997.                           (2.3)
```

Euclidean phase-space arclength dominates absolute `r` displacement.

## 3. Grazing-only occlusions cannot evade the collar

One extra case must be controlled.  A central background owner can disappear
because a new target enters at tangency, while the new target remains entirely
in high strips; later a central background owner can reappear.  In that case
one must not incorrectly apply (2.3) to the background target.

The two signed tangency directions to one target at the same source point are
separated by

```text
2 asin(R_T/|d|) > 2/21.                              (3.1)
```

The frozen minimum free flight and cone bounds give

```text
|d_r(phi_W-phi_tan)|
 < 29 + 25/4 + 800000/36337
 = 8323517/145348.                                   (3.2)
```

Therefore crossing both signed sheets of one target costs more than

```text
(2/21)/(8323517/145348)
 = 41528/24970551.                                   (3.3)
```

This is vastly larger than (2.3).

The remaining topological input is exact.  Target disks are pairwise strictly
disjoint, so two positive first roots cannot be equal.  Between two central
owner blocks, either an adjacent central owner reaches a selected tangency
endpoint, or a grazing-only intervening owner enters and later leaves, forcing
both of its signed sheets to be crossed.  Chart seams are representation
boundaries and are not physical cuts.

Taking half the smaller collar,

```text
delta_1
 = 1/(2*13437*k0^4)
 = 1/37724355673552103994,                            (3.4)
```

proves:

```text
length(W)<=delta_1  =>  at most one central child globally. (3.5)
```

This is the explicit sheet-separation/incidence theorem requested by the old
weighted-join diagnostic.

## 4. The global high-strip tail

On one true continuity component, the image is an unstable graph and meets
each horizontal homogeneity strip at most once.  On `H_(+/-k)` the already
certified adapted inverse expansion is

```text
norm(DT_s^-1)_* < 4/k^2.
```

There are at most 153 true components.  Hence all high children of all true
components satisfy one single global estimate:

```text
sum_(j<=153) sum_(sign=+/-) sum_(k>=6121) 4/k^2
 < 153*8/(6121-1)
 = 1224/6120
 = 1/5.                                              (4.1)
```

The inequality is strict because the integral tail estimate for
`sum k^-2` is strict.  The number `1/5` is therefore a strict upper envelope,
not an attained tail.

The enlarged central strip is connected.  By (3.5) it has global multiplicity
at most one, and its inverse expansion is strictly below

```text
theta = 144000/180337.                               (4.2)
```

Combining (4.1)--(4.2) gives

```text
Xi_1(delta_1)
 < theta + 1/5
 = 900337/901685
 < 1,                                                (4.3)

1-Xi_1 upper envelope margin = 1348/901685.          (4.4)
```

The typed compressed rows are therefore:

| Parent/child type | Owner | Multiplicity | Inverse-expansion upper |
|---|---|---:|---:|
| central `H_0(k0=6121)` | unique first-visible `T(W,j)` | `<=1` globally | `144000/180337` |
| `H_(sign,k)`, `k>=6121` | unique first-visible `T(W,j)` | `<=153` per sign and rank | `4/k^2` |

Every true cut and every homogeneity cut is counted once.  This closes the
previous aggregate nonidentifiability by a theorem carrying the missing join
information; it does not fabricate a row-level physical atlas from candidate
digests.

## 5. What (4.3) does and does not certify

Certified now:

1. an exact typed audit from horizon witness to candidate owner and raw sheet;
2. an explicit short-curve ID contract and physical component ID contract;
3. `delta_1=1/37724355673552103994`;
4. at most one central child globally;
5. one global high-strip tail `<1/5` across all true branches;
6. the strict global one-step weighted sum (4.3).

Not certified:

1. an invariant numerical `C2` curvature ceiling `D_std` for every iterated
   standard curve;
2. the resulting all-standard-curve homogeneous log-Jacobian distortion
   constant;
3. a numerical regular-density constant and additive Growth recurrence;
4. explicit `C_p,vartheta_p`, followed by `A0,A1`;
5. propagated `C_fw,C_rev` and the final same-occurrence `q`.

The frozen `6000000000000` distortion constant applies to 128 initial
oriented carriers only.  The global frozen certificate explicitly leaves
arbitrary iterated standard-curve distortion open.  Thus (4.3) is a genuine
new `theta_*` input, but it is not by itself a numerical recovery theorem.

In particular, the notation is guarded as follows:

```text
old q_branch = local one-true-branch diagnostic,
new 900337/901685 = global one-step Xi upper at delta_1,
final q = still-missing CM2 same-occurrence propagated cost.
```

## 6. Unnormalised/reweighted recovery frontier

The finite-cemetery no-go has not been widened.  It applies only to the
normalized cumulative-`u` interface with separate leafwise `p_a^-1` charging.
It does not refute an unnormalised or reweighted family theorem.

However, none of the frozen manifests supplies the five fields needed to use
that escape:

1. a record-preserving unnormalised standard-family representation;
2. finite unnormalised boundary `Z` after every actual cut;
3. a numerical inequality
   `Z_un(TF)<=a Z_un(F)+b mass(F)` with `a<1`;
4. a query-independent merge/reweight rule preserving occurrence labels;
5. a charged-moment bound before any leafwise normalization.

The newly certified (4.3) is a necessary contraction input for item 3 but
does not supply the missing curvature, density, or record-preserving
functional interface.  Therefore unnormalised/reweighted native recovery
remains `NOT_CERTIFIED`, honestly outside the finite-cemetery obstruction.

## 7. Replay and fail-close contract

```bash
PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_componentwise_global_growth_recovery_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_componentwise_global_growth_recovery_frontier_verifier.py \
  --self-test

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_componentwise_global_growth_recovery_frontier_verifier.py
```

Replay/integrity exits `0`.  The mutation suite rejects 15 independent
changes and exits `0`.  Default live execution exits `2`, because numerical
`C_p,vartheta_p`, native recovery, propagated costs, and Gate 4 remain open.

All twelfth-round files are read-only dependencies and were not modified.
