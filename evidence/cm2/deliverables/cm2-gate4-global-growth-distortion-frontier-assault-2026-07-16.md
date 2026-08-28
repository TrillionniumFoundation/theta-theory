# CM2 Gate 4 global Growth/distortion frontier assault

Date: 2026-07-16 (Asia/Shanghai)

## Verdict

This assault closes three numerical leaves that were still qualitative in the
eleventh-round Gate 4 frontier:

1. an all-table one-step true-singularity complexity bound;
2. an all-physical-branch `D2T_s` grazing-weight envelope;
3. a one-step homogeneous log-`r`-Jacobian distortion constant on all 128
   already certified oriented occurrence carriers.

The resulting executable branch-sum bound is much larger than one.  It is not
a Growth-Lemma contraction.  The numerical invariant curvature ceiling for
arbitrary iterated standard curves, a finite-`s` `delta_n` root-separation
ledger, and a genuinely weighted true-singularity sum remain absent.  Thus no
value is assigned to `C_p`, `vartheta_p`, `C_fw`, `C_rev`, or `q`, and Gate 4
remains open.

```text
NUMERIC TRUE-SINGULARITY COMPLEXITY:                   CERTIFIED
ALL-PHYSICAL-BRANCH D2T GRAZING WEIGHT:                CERTIFIED
128-CARRIER ONE-STEP LOG-r-JACOBIAN DISTORTION:        CERTIFIED
NUMERIC GLOBAL GROWTH CONTRACTION:                     NOT CERTIFIED
NUMERIC C_p,vartheta_p,C_fw,C_rev,q:                   NOT CERTIFIED
GATE 4:                                                NOT CERTIFIED
```

Evidence:

- `deliverables/cm2_gate4_global_growth_distortion_frontier_cert.py`;
- `deliverables/cm2_gate4_global_growth_distortion_frontier_verifier.py`;
- `deliverables/cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.json`;
- `deliverables/cm2-gate4-global-growth-distortion-frontier-manifest-2026-07-16.sha256`.

## 1. Frozen finite universe and true-singularity complexity

The 35,024-leaf horizon cover gives `tau<3` uniformly on
`|s|<=1/400`.  The exact first-hit reduction retains 448 of the 1,296
chart/target rows.  After quotienting the four normal charts, the possible
target unions have cardinalities

```text
gray source: 76,
white source: 68.
```

Each target circle has at most two signed tangent orientations.  The old owner
registry's global count

```text
2*76+2*68=288
```

is replayed exactly.

For every such tangent sheet, elementary circular geometry gives

```text
d phi_tan / d r = -kappa_source-cp_source/ell_T < -25/9.       (1.1)
```

An admissible unstable graph has slope `V>25/9`.  Hence one unstable graph
intersects one lifted signed tangent sheet at most once.  A curve based on one
source obstacle therefore meets at most

```text
max(2*76,2*68)=152                                      (1.2)
```

true singularity sheets and has at most 153 true continuity components after
one collision.  The deliberately crude iterated component bound is `153^n`.
This is a global finite complexity leaf; it does not assert that all 152 sheets
are simultaneously physical or intersected.

The previous one-true-continuity-branch homogeneity sum is

```text
q_branch < 900337/901685.
```

Applying it to all 153 possible components gives the first executable global
upper bound

```text
Xi_1 <= 153*(900337/901685)
     = 137751561/901685
     = 152.771268... > 1.                              (1.3)
```

Iteration gives only

```text
Xi_n <= (137751561/901685)^n.                           (1.4)
```

Thus the finite universe alone does not close Growth.  Equation (1.3) is a
strict diagnostic: the missing input is a physical contraction-weighted
multiplicity ledger, not another unweighted target count.

## 2. All-branch second derivatives of the billiard map

On every physical continuity branch of a fixed table `T_s`, write
`c_i=cos(phi_i)`.  Since both obstacles are circles, their curvatures are
constant along a branch and the exact Birkhoff matrix is

```text
D T_s = -c_1^-1
  [[tau*kappa_0+c_0, tau],
   [tau*kappa_0*kappa_1+kappa_0*c_1+kappa_1*c_0,
    tau*kappa_1+c_1]].                                  (2.1)
```

Using `tau<3`, `kappa_i<=25/4`, and `c_i<=1`, the four numerator bounds are

```text
[79/4, 3, 2075/16, 79/4].                              (2.2)
```

Differentiating the flight identity and (2.1) gives

```text
|partial_r tau|   < 21/c_1,       |partial_phi tau| < 3/c_1,
|partial_r c_1|   < 130/c_1,      |partial_phi c_1| < 20/c_1. (2.3)
```

Exact quotient-rule arithmetic then produces the coefficient rows

```text
r derivative:   [10795/4, 411, 295875/16, 11315/4],
phi derivative: [1659/4,   63,  45475/16,  1735/4].    (2.4)
```

Consequently, on every physical branch and every `|s|<=1/400`, including
all branches in the 448-row conservative target universe,

```text
|partial_r (D T_s)_{ij}|   < 18493/c_1^3,
|partial_phi (D T_s)_{ij}| <  2843/c_1^3,
||D2 T_s||_(coordinate infinity) < 42672/c_1^3.        (2.5)
```

This is the requested all-branch `D2T` grazing-weight leaf.  It is not yet an
invariant curvature theorem: using (2.5) naively in the graph-transform
formula loses a factor at grazing, so it cannot by itself supply the missing
numerical `D_std` for every iterate.

## 3. Exact log-`r`-Jacobian derivative

Let an oriented unstable carrier be a graph with

```text
25/9 < V=d phi/d r <29,       |V'|<4949.                (3.1)
```

The 64 physical occurrences give 128 such oriented views after forward or
time-reversed orientation.  Along a fixed branch, the exact projected
Jacobian is

```text
|r_1,W'| = A/c_1,
A=tau*(kappa_0+V)+c_0.                                  (3.2)
```

The finite-`s` flight gap gives

```text
A>2*(25/9)*(36337/800000)=36337/144000.                (3.3)
```

Moreover,

```text
|tau'_W| < (21+3*29)/c_1 =108/c_1,
|A'|     <18683/c_1,
|c_1'|   <(130+20*29)/c_1=710/c_1.                    (3.4)
```

Therefore

```text
|d_r log|r_1,W'||
 < [18683*(144000/36337)+710]/c_1^2
 = (388021610/5191)/c_1^2
 < 74750/c_1^2.                                        (3.5)
```

For later reuse, if an arbitrary standard curve eventually receives a
numerical curvature ceiling `D`, the same replay gives the conditional
formula

```text
C_log(D)=710+(3836+3D)*(144000/36337),
|d_r log|r_1,W'|| < C_log(D)/c_1^2.                    (3.6)
```

## 4. Homogeneity removes the grazing divergence

On a high target strip `H_k`, `k>=41`,

```text
1/[2(k+1)^2] < c_1 < k^-2.                             (4.1)
```

Since the target graph slope is at least `25/9`, its `r`-projection has
length at most

```text
L_k=(9/25)*(2k+1)/(k^2*(k+1)^2).                       (4.2)
```

The inverse projected derivative is at most
`1/[(36337/144000)k^2]`.  Combining (3.5), (4.1), and (4.2), then cubing the
candidate constant to keep the replay rational, gives uniformly for all
`k>=41`

```text
|log(J(x)/J(y))| < 1024000*|r_1(x)-r_1(y)|^(1/3).      (4.3)
```

For the central strip, `c_1>1/(2*41^2)` and one boundary component has
`r`-length less than `396/175`.  The same exact cubed comparison gives

```text
|log(J(x)/J(y))|
 < 6000000000000*|r_1(x)-r_1(y)|^(1/3).                (4.4)
```

Thus (4.4) is one explicit uniform one-step log-`r`-Jacobian distortion
constant for all 128 certified oriented carriers and every target
homogeneity component.  It is intentionally huge but finite and replayable.
It does not claim Euclidean arclength-Jacobian distortion, nor does it claim
the invariant arbitrary-standard-curve distortion needed by the Growth
Lemma.

## 5. Exact remaining boundary

Numerically closed now:

1. true one-step singularity intersections `<=152` and components `<=153`;
2. crude `n`-step true component count `153^n`;
3. every physical branch has the explicit `D2T_s` envelope (2.5);
4. every one of the 128 oriented occurrence carriers has the homogeneous
   log-`r`-Jacobian constants (4.3)--(4.4);
5. a future numerical standard-curve curvature ceiling can be inserted
   directly into (3.6).

Still not certified:

1. a weighted true-singularity sum beating (1.3);
2. finite-`s` root isolation/separation producing an executable `delta_n`;
3. an invariant numerical `D_std` for every iterated standard curve;
4. global `theta_*<1`, regular-density recovery and numerical
   `C_p,vartheta_p`;
5. the propagated `C_fw,C_rev,q` and repeated native recovery.

The strict status is therefore unchanged:

```text
GATE 4: NOT CERTIFIED.
```
