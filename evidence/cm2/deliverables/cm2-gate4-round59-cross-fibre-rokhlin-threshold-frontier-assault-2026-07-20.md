# CM2 Round 59 Gate 4 — cross-fibre Rokhlin / landing-threshold frontier

Date: 2026-07-20  
Strict status: **the Round-58 physical landing threshold is not closed.  A
new exact separator proves that even an aggregate normalized landing boundary
strictly below `C_p`, an almost-minimal full `D_land` moment, ambient
properness, high common mass and `D_cap=0` do not imply the required
fibrewise inequality.  The exact first-return graph does, however, already
supply a tagged Borel branch inverse and a measure-typed lossless weak
Rokhlin reconditioning.  Thus one of the seven Gate-2-to-Gate-4 semantic rows is now
certified, while the physical product/holonomy/conditional-density/boundary
and strong-assembly rows remain absent.  Gate 4 and CM2 remain open.**

## 1. Frozen input and the direct route

Round 58 proves, within each fixed

```text
(y, physical landing chart, immutable physical restriction ID),
```

that the maximal connected positive components attain

```text
J_land,min(y)=sum_C kappa_y(C)/ell(C),
```

and that the exact unshifted landing is proper exactly when

```text
J_land,min(y)<C_p h(y)                                  (1.1)
```

for almost every positive outer fibre.  It also proves

```text
J_land,min,total<infinity,
integral h(y) 2^D_land(y) dlambda(y)<infinity.
```

The first Round-59 attack was therefore to trace every Round-41--58 affine
and Growth constant and test whether the enormous value

```text
C_p=4*10^90*360493663/358863
```

could convert a global numerical bound into (1.1).  It cannot: (1.1) is an
almost-everywhere conditional statement, while all available affine joins
are integrated statements.  The following exact model makes the distinction
sharp even if the global ratio is already far below `C_p`.

## 2. Positive-bad-fibre separator with arbitrarily good aggregate boundary

Put

```text
H=999/1000,
N=floor(C_p)+1.
```

Use two outer fibres, both with identity first return at time one on a full
unit half-open interval.  The full ambient return on either fibre is proper.

On the good fibre retain one interval of length and mass `H`, with one gap of
length `1/1000`.  Then

```text
J_good=1,
z_good=J_good/H=1000/999<C_p,
D_good=0.
```

On the bad fibre retain `N` equal intervals of total length and mass `H`,
separated by `N-1` true positive gaps of total length `1/1000`.  All
half-open owners are unique and all pieces remain in one immutable physical
chart/ID.  Round 58's minimal-component theorem gives

```text
J_bad=N,
z_bad=N/H=1000N/999>C_p.
```

Since `N<C_p+1` and `C_p` is much larger than one,

```text
C_p<z_bad<2C_p.
```

The strict Round-58 dyadic definition therefore gives `D_bad=2`: one dyadic
step cannot cross the strict boundary and two steps can.

For any integer `m>=2`, assign the bad fibre outer weight

```text
epsilon_m=1/(mN)>0.
```

The aggregate quantities are exactly

```text
J_total
 =(1-epsilon_m)J_good+epsilon_m J_bad
 =1+1/m-1/(mN),

H_total=999/1000,

integral h 2^D
 =999/1000 * (1+3/(mN)).                       (2.1)
```

Thus `J_total/H_total<C_p`, and as `m` grows the aggregate normalized
boundary tends to the good value `1000/999`; the full dyadic moment tends to
`999/1000`.  Nevertheless the improper fibre has positive common mass

```text
epsilon_m*999/1000>0.
```

A piecewise-translation reference reassembler places each marker on one
reference interval.  Two identical reference orientations have

```text
J_cap=2,
z_cap=2000/999<C_p,
D_cap=0.
```

Consequently none of the following implies (1.1):

- finite `J_land,min,total`;
- even the stronger global inequality `J_land,min,total<C_p H_total`;
- a full `D_land` dyadic moment arbitrarily close to its minimum;
- high common mass and a tiny deleted mass;
- an ambient proper identity return;
- finite `J_cap` and `D_cap=0`.

This is a logical exact-standard-family nonimplication model, not a claim
that the billiard realizes this fragmentation.  Its purpose is to eliminate
the last aggregate-to-fibre shortcut.  A genuine direct proof must use new
pointwise physical landing geometry, not a stronger integrated affine
constant.

## 3. The exact graph already has a Borel branch inverse

Round 57's raw common law lives on a countable half-open registry carrying

```text
(n, R_n path, source/parent/restriction ID, recut owner),
```

and satisfies

```text
Q_cap(x)=T_s^n x,
T_s^j x notin C_s for 1<=j<n,
T_s^n x in C_s.
```

On one tagged regular `R_n` branch, `T_s^n` is injective and its inverse is
`T_s^{-n}`.  The domain is standard Borel; hence Lusin--Souslin makes the
tagged image Borel and its inverse Borel.  Taking the countable union over
the retained branch tags gives, modulo the already pinned null cemetery,

```text
(tag,landing) -> (tag,T_s^{-n}(landing)).              (3.1)
```

This is the branch-inverse row requested in item 6 of the Round-58 seven-field
join.  It preserves the original `n`, path, immutable ID and half-open owner.

More generally, let

```text
q: landing -> U
```

be a Borel map into a standard-Borel quotient `U`, hence generating a
countably generated Borel partition of the **physical landing coordinate**,
and put

```text
eta=(q o pr_landing)_# Gamma_cap.
```

The standard-Borel disintegration theorem supplies a probability kernel
`u -> Gamma_u`, defined only `eta`-almost everywhere, such that for every
Borel graph event `A`,

```text
Gamma_cap(A)=integral Gamma_u(A) deta(u).              (3.2)
```

This is not division by the singleton mass `eta({u})`; in particular,
`eta({u})` may be zero for `eta`-almost every `u`.

Let `S_u` be the tagged graph relation over `q(landing)=u`.  Then

```text
Gamma_u(S_u)=1
```

for `eta`-almost every `u`.  Hence, for those `u`, the identities

```text
landing=T_s^n(source)
```

hold `Gamma_u`-almost surely with the same tags, because the original measure
already has that support.  Equation (3.2) reassembles exactly the same
graph **measure**, so the once-charge bookkeeping encoded by that measure is
unchanged.  It makes no pointwise claim that individual raw points are
deleted, retained or duplicated.  The source/physical-landing endpoint and tag identities are
preserved only in this `eta`-a.e. / `Gamma_u`-a.s. sense.  Conditional values
chosen on an `eta`-null quotient set are arbitrary and carry no certified
endpoint, tag or normalization meaning.

This certifies a **weak same-graph reconditioning theorem**.  It does not say
that `q` is an actual unstable-product partition, nor that its conditionals
are regular proper standard families.  Those are the remaining physical and
strong-space requirements.

## 4. Quantitative physical product-rectangle bridge

The seven-field join can be sharpened to one elementary numerical inequality
once a real target product registry exists.

Fix an actual physical target unstable plaque of adapted length `L(u)>0`.
Suppose the common target conditional has the same physical landing points
and the form

```text
kappa_u=f_u 1_E ds,
```

where every length below, including `L`, `|E|` and component length in `Z`,
uses the same adapted arclength `ds`, and:

```text
E has at most F(u) connected interval components,
|E|>=theta(u)L(u),
0<d_-(u)<=f_u<=d_+(u)<=R(u)d_-(u).
```

For every maximal component `C` of `E`,

```text
mass(C)/|C|<=d_+.
```

Therefore

```text
J_u<=F d_+,
h_u>=d_- theta L,
z_u=J_u/h_u<=F R/(theta L).                           (4.1)
```

The strict sufficient physical inequality is

```text
F(u)R(u)<C_p theta(u)L(u)                             (4.2)
```

almost everywhere.  Together with the tagged inverse (3.1) and a strong
restriction/assembly theorem, (4.2) produces a proper physical landing at
the original time `n`.  Its reassembled graph measure is the original
once-charged graph, and the endpoint, first-hit, ID and path identities hold
measure-almost everywhere.  No recovery collision is added.

For an arithmetic magnitude check only, take

```text
F=153,
R=2000/1999,
theta=1/2,
L=1/12800.
```

Then

```text
F R/(theta L)=7833600000/1999<C_p.                   (4.3)
```

Equation (4.3) is **not** a physical join.  `F=153` and the ratio row occur in
the Round-49 conditional source compact core, while the available Round-25
affine product tile is only a cone-candidate construction, not invariant
stable holonomy and not the Round-57 common landing law.  The test shows that
the obstacle is identity/provenance and conditional geometry, not the size
of the eventual numerical margin.

## 5. Seven-field materialization audit

The Round-58 sufficient interface now has the following exact state:

| # | Physical field | Round-59 state |
|---:|---|---|
| 1 | countable product-rectangle cover of the common landing | `NOT_CERTIFIED` |
| 2 | immutable stable projection and two-sided Borel holonomy Jacobian | `NOT_CERTIFIED` |
| 3 | full-span or quantitatively bounded common fragmentation | `NOT_CERTIFIED` |
| 4 | same-measure unstable conditionals with density/log distortion | `NOT_CERTIFIED` |
| 5 | boundary charge strictly below `C_p` | `NOT_CERTIFIED`; formula (4.2) only |
| 6 | Borel branch inverse retaining `n/path/ID/owner` | `CERTIFIED` |
| 7 | strong restriction and assembly | `NOT_CERTIFIED`; weak graph reassembly only |

Thus the Gate-4 join has `1/7` of these local interface rows actually
certified.  This is not an official Gate-2 maturity promotion: Gate 2 remains
`0/17` because the new row comes from the already exact Gate-4 first-return
graph, not from a stable quotient.

The shortest remaining cross-fibre route is now precise:

1. materialize items 1--4 on the **actual common landing law**;
2. prove the pointwise numerical inequality (4.2);
3. install item 7 for the resulting physical conditional carriers.

The graph inverse and the measure-a.e. endpoint/first-hit/tag identities need
not be reconstructed.

## 6. Latest official-technology audit

The official API and PDF for Climenhaga--Day,
arXiv `2604.25881v1`, *Every finite horizon Sinai billiard map has a unique
measure of maximal entropy*, were checked.  Definition 2.12 gives local
product equivalence for the constructed MME, and Lemma 2.14 preserves their
symbolic Hausdorff leaf measures under symbolic stable holonomy.  This does
not instantiate the present interface:

- the measure is the constructed MME, not the pinned Liouville/SRB common
  landing restriction;
- equivalence supplies no two-sided physical RN constants for that marker;
- there is no common-landing fragmentation or retained-span row;
- no `Z<C_p` boundary charge is derived;
- no join to the tagged `R_n` first-return inverse or strong standard-family
  assembly is supplied.

The Demers--Liverani 2026 transfer-operator survey likewise does not state a
same-time properisation theorem for this marked physical landing.  No
external theorem is promoted.

## 7. Strict frontier

```text
physical J_land,min,total:                         CERTIFIED_FINITE (pinned)
physical full dyadic D_land moment:                CERTIFIED_FINITE (pinned)
fibrewise J_land,min<C_p h a.e.:                   NOT_CERTIFIED
aggregate/moment route to fibrewise threshold:     CERTIFIED_FALSE
tagged Borel first-return branch inverse:           CERTIFIED
weak same-graph Rokhlin reconditioning:             CERTIFIED
seven-field physical landing join:                 1/7; STRONG JOIN OPEN
quantitative product-rectangle bridge:              CERTIFIED_CONDITIONAL
proper physical same-ID first-return landing:       NOT_CERTIFIED
proper physical same-ID first-return kernel:        NOT_CERTIFIED
postlanding intermediate C24 avoidance:             NOT_CERTIFIED
later/repeated recovery-clock moments:              NOT_CERTIFIED
physical q in L^(6/5):                              NOT_CERTIFIED
strong singular/current cemetery:                   NOT_CERTIFIED
Gate 4:                                             NOT_CERTIFIED
complete composite gates:                          0/5
CM2:                                                NO-GO_FOR_CLAIM
```

## 8. Executable evidence

- `cm2_gate4_round59_cross_fibre_rokhlin_threshold_frontier_cert.py`;
- `cm2_gate4_round59_cross_fibre_rokhlin_threshold_frontier_verifier.py`;
- `cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json`;
- `cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.sha256`.

The suite pins all dependencies and this report, independently replays the
two-fibre rational identities, the exact quantitative bridge, the seven-field
audit and the strict no-promotion boundary.  It also performs deterministic
manifest regeneration, byte-identical reemit, hostile mutation rejection,
strict JSON checks and fail-closed default execution.
