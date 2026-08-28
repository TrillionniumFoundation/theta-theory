# CM2 Gate 4/5 round-29 same-ID weighted/induced frontier assault

Date: 2026-07-18 (Asia/Shanghai)  
Status: append-only strict leaf; no aggregate, root, prior round, log or memory modified

## Verdict

This leaf performs the strict connectability audit that must precede any
numerical `C_fw/C_rev/q`, weighted-tail, cemetery or induced strong
Lasota--Yorke promotion.  It closes one genuinely nonempty finite same-origin
skeleton and freezes four exact type barriers.

```text
FINITE Q2 SAME-ORIGIN COMPONENT/MASS/RESTRICTION/
  HOMOGENEITY/F5/F6 SKELETON:                    CERTIFIED 114006
FINITE R1 FIRST-RETURN COMPONENT ANCHORS:         CERTIFIED 4216
ACTUAL PARENT-CURVE RECUT INSTANCES:                         0
COMMON STANDARD-FAMILY RECOVERY CARRIERS:                    0
NUMERICAL C_fw / C_rev / q:                                  0
PHYSICAL FIRST-RETURN q ROWS READY FOR TAIL SUM:              0
SURVIVOR-CONDITIONED OR GLOBAL PHYSICAL Lp ENVELOPE:          0
STRONG CEMETERY CHARGE:                                      0
INDUCED STRONG LASOTA--YORKE:                    NOT CERTIFIED
GATE 4 / GATE 5:                                 NOT CERTIFIED
CM2:                                              NO-GO FOR CLAIM
```

Evidence:

- `deliverables/cm2_gate45_round29_same_id_weighted_induced_frontier_cert.py`;
- `deliverables/cm2_gate45_round29_same_id_weighted_induced_frontier_verifier.py`;
- `deliverables/cm2-gate45-round29-same-id-weighted-induced-frontier-manifest-2026-07-18.json`;
- `deliverables/cm2-gate45-round29-same-id-weighted-induced-frontier-manifest-2026-07-18.sha256`.

## 1. Strongest nonempty same-origin finite subledger

The round-28 nonempty registry exhausts the frozen strict finite `Q2-inner`
source registry.  It has one depth-zero adaptive cell per time-two origin:

```text
origin Q2 atom count                         114006
nonempty Q2 adaptive component cells        114006
adaptive wall recut histogram          {0: 114006}
finite unresolved wall outer count               0
parameter-averaged coordinate-base mass
                                    5257799/5120000000
```

On the same exhaustive frozen origin registry, the round-28 homogeneous
branch-rule payload has:

```text
two-step physical homogeneity children      114006
canonical recut branch-rule IDs              228012
exact symbolic collision-area mass rows      114006
common Borel fw/rev restriction IDs           114006
F5 universal branch-rule slots                114006
F6 universal branch-rule slots                114006
```

The exact universal bounds are

```text
F5: ||(D T^2|E^u)^-1|| < 20736000000/32521433569 < 1,
F6: osc(log J^u T^2)   < 3/100000.
```

Therefore `114006` nonempty same-origin finite rows now carry a component
cell, mass/restriction identities, physical homogeneity children and the F5/F6
branch-rule theorem.  This is the strongest currently legal finite strong
skeleton.

It is deliberately not called a numerical strong operator payload.  The
228,012 recut IDs are rules quantified over a future parent standard curve;
the number of actual `recut-instance:(rule,parent-W,j)` records is zero.  A
Borel restriction of a two-dimensional collision cell is not a
standard-family recovery carrier.  The invariant area Jacobian `1` is not the
one-dimensional unstable Jacobian.  These three distinctions are immutable.

## 2. The decisive level mismatch: Q2 is not Rn

The arbitrary-`n` physical ledger has the exact disjoint level identity

```text
Q_(n-1) = R_n disjoint_union Q_n              modulo collision-null faces.
```

The 114,006 rows above are `Q_2` survivor cells: they avoid C24 at collision
times one and two.  They are not `R_n` first-return summands.  Consequently
even a future numerical cost on all 114,006 Q2 rows would be a finite
survivor payload; it could not be inserted directly into

```text
W_n = sum_(j>n,k) q_(j,k)
```

as a first-return charge.  The certified direct Q2-to-`R_n` charge join count
is exactly zero by level type, not by a failed string-ID match.

There are 4,216 nonempty finite `R1-inner` first-return component anchors,
with parameter-averaged coordinate-base mass

```text
6473/256000000.
```

They have candidate-local maturity `13/18`, but F14--F18, common strong
recovery carriers and numerical first-return `C_fw/C_rev/q` all remain zero.
Nor do these finite inner anchors enumerate the complete limiting `R1` or
arbitrary-`n` first-return registry.

## 3. Exact weighted-tail connectability audit

The round-28 transfer theorem remains valid.  With

```text
A = 550000/147,
r = 111718729/111718750,
S_n < A r^floor(n/N_open),
```

a same-ID survivor-conditioned `L^p` envelope would preserve the factor `r`,
and a global `L^p` envelope would preserve an exponentially degraded factor.
No such physical hypothesis is currently instantiated.

The six required interfaces and their exact current states are:

| # | Required interface | Current state |
|---:|---|---|
| 1 | positive-mass `R_n` component at fixed `s` | 4,216 finite `R1-inner` anchors only |
| 2 | actual parent-curve recuts plus one common fw/rev strong carrier | 0 |
| 3 | numerical once-charged `C_fw,C_rev,c=q/m` | 0 |
| 4 | uniform fixed-`s` survivor-conditioned/global `L^p` envelope | 0 |
| 5 | numerical strong singular-cemetery charge | 0 |
| 6 | common-space induced F14--F18 operator block | 0 |

There is an additional measure-typing obstruction.  The finite registry's
globally summed rational quantity is a parameter-averaged coordinate-base
mass.  The weighted transfer theorem quantifies every fixed
`|s|<=1/400`.  An averaged finite mass does not imply a uniform fixed-`s`
strong moment; a disintegration or direct fixed-s supremum estimate is still
required.

Thus the current counts are exactly

```text
uniform survivor-conditioned physical Lp envelopes       0
global physical first-return Lp envelopes                 0
compatible pointwise physical envelopes                   0
physical Rn q-density rows ready for the tail sum          0
```

## 4. Exact mass-zero/strong-cemetery nonimplication

Collision-SRB nullity alone cannot fill the strong cemetery slot.  The leaf
freezes an exact one-dimensional standard-family countermodel.

Start from the uniform standard pair on `[0,1]` and cut at

```text
S_N={j/(N+1): 1<=j<=N}.
```

For every finite `N`, `Leb(S_N)=0`.  Its complement has `N+1` intervals,
each of length and weight `1/(N+1)`.  For the usual boundary functional,

```text
Z_N = sum_components weight/length = N+1 -> infinity.
```

The certificate replays this identity at
`N=1,2,4,8,16,32,64` using exact fractions.  Hence

```text
collision-null singular/core-boundary mass = 0
```

does not imply zero, finite or summable characteristic-cut boundary `Z`,
coarea trace or dynamic-test charge.  This is a logical nonimplication, not a
claim that the CM2 physical strong cemetery must diverge.  A summable
singularity-complexity theorem or a direct trace/Z estimate on the same
strong carrier could still close it.

## 5. Why the numerical recovery stack still does not assemble

The following constants remain fully certified:

```text
D_std < 30000000,
vartheta_p = 360134800/360493663 < 1,
A0 = 301500,
A1 = 1005,
native gamma = 1/12060.
```

They apply to phase-typed standard curves and to the precisely declared
one-time or levelwise recovery contracts.  They do not manufacture the
missing parent-curve IDs, repeated physical indicator boundary numerator, or
same-ID `R_n` recovery history.  In particular:

- a fixed auxiliary product depth mark is not a physical first-return
  history;
- a theorem for each predeclared finite restart count `H` is not an
  unbounded-return recovery theorem;
- the open coefficient for `O=L M_C` is not an induced coefficient for
  `R_n=M_C L(M_Cc L)^(n-1)M_C`;
- `||R||_L1=1` and invariant area Jacobian `1` are not strong-space
  Lasota--Yorke coefficients.

The induced assembly therefore remains:

```text
measurable induced L1 Perron norm                         1
weighted first-return excursion tail          NOT CERTIFIED
strong cemetery charge                        NOT CERTIFIED
complete F14--F18 common operator blocks                   0
common fw/rev strong space and restriction     NOT CERTIFIED
induced strong Lasota--Yorke                    NOT CERTIFIED
```

## 6. Technology boundary

No external theorem is imported by this leaf.  The latest matched sources
remain useful blueprints but do not replace the missing C24 same-ID physical
interfaces:

- arXiv:`2604.19671v2` uses the special geometry of a small
  boundary-position hole; its survivor-conditioned recovery does not cover
  this parameter-uniform union of phase-space rectangles or supply its
  branchwise strong cemetery/induced constants;
- arXiv:`2606.10155v1` supplies relevant transfer-operator and regular-density
  technology but no theorem instantiating the missing actual recut, face,
  fixed-s `L^p`, cemetery and common-space records.

References:

- <https://arxiv.org/abs/2604.19671v2>
- <https://arxiv.org/abs/2606.10155v1>

## 7. Shortest next physical route

The highest-leverage order is now exact:

1. on the finite R1 and Q2 component cells, instantiate actual
   `(branch-rule,parent-W,j)` recut records and charge F7 for every physical
   word/recut boundary;
2. refine the remaining chart seams and enumerate connected physical face
   ranks with numerical coarea/trace bounds;
3. build one common fw/rev standard-family carrier and fixed-s numerical
   `C_fw/C_rev/q` row on the same immutable component ID;
4. extend that construction to arbitrary return depth and prove the
   survivor-conditioned `L^p` envelope;
5. separately charge the singular/corner cemetery in the same strong norm;
6. assemble F14--F18 and only then derive the induced strong coefficient.

## 8. Replay and fail-close contract

Use `.venv-neurips/bin/python`:

```text
cm2_gate45_round29_same_id_weighted_induced_frontier_verifier.py --integrity-only
  AUDIT_MODE: PASS

cm2_gate45_round29_same_id_weighted_induced_frontier_verifier.py --replay
  AUDIT_MODE: PASS

cm2_gate45_round29_same_id_weighted_induced_frontier_verifier.py --self-test
  HOSTILE_TESTS: 101/101 PASS

cm2_gate45_round29_same_id_weighted_induced_frontier_verifier.py
  exits 2
```

The live exit remains `2` because numerical `C_fw/C_rev/q`, the physical
weighted excursion/cemetery tail, F14--F18 and the induced strong
Lasota--Yorke coefficient remain open.
