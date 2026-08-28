# CM2 Gate 4 native stopping and repeated-recovery assault

Date: 2026-07-16 (Asia/Shanghai)

## Verdict

This assault replaces the auxiliary product mark at the **record-algebra**
level by a full-mass, query-independent prefix antichain in the actual
physical row mass coordinate.  It also proves that this native replacement
cannot inherit the finite normalization/recovery moment of the product
extension: the required moment diverges before any billiard recovery clock is
charged.

It further gives exact one-cut and repeated-cut countermodels and reduces the
numeric Growth-Lemma gap to its unevaluated leaf constants.  Consequently:

```text
NATIVE PHYSICAL-MASS-COORDINATE PREFIX ANTICHAIN:         CERTIFIED
NATIVE DEPTH-PLUS-RECOVERY MOMENT:                        NOT CERTIFIED
HEREDITARY REPEATED-INDICATOR RECOVERY:                   NOT CERTIFIED
COMPLETE NUMERIC C_fw/C_rev/q:                            NOT CERTIFIED
GATE 4:                                                   NOT CERTIFIED
```

The global result therefore remains unconditional CM2 `NO-GO`.

## 1. Read-only inputs

The replay binds the frozen manifests for:

- the finite-`s` moving endpoint/core mesh and one-time recovery;
- the auxiliary product depth kernel;
- the controlled dyadic interval algebra;
- the all-row bidirectional carrier-`C2` and log-density costs.

In particular, throughout `|s|<=1/400`, every one-time physical depth-`d`
mass-coordinate atom already has both oriented standard-family
representations with

```text
Z_fw/mu, Z_rev/mu <= C_mesh 2^d,
C_mesh = 69986663973833932800.
```

All old manifests, v51/v52, the continuous log, and memory were read only.

## 2. A genuinely native prefix antichain

For a maximal physical occurrence `e` at fixed `s`, let

```text
u=u_(e,s)(theta)
  =m_(e,s)((left_s,theta))/m_(e,s)(row_s) in (0,1).
```

This is the physical cumulative-mass coordinate of the corrected common row
law.  Use its binary filtration.  Read pairs of bits until the first pair
different from `00`.  If it occurs after `K` leading `00` pairs, call the
nonzero pair `q in {01,10,11}`.  Equivalently,

```text
S_K=[4^(-(K+1)),4^-K),
m(S_K)=(3/4)4^-K.                                      (2.1)
```

Once `K` is known, read `K` further payload bits `j`.  The complete record is

```text
(e,s,K,q,j),  0<=j<2^K.                               (2.2)
```

The code words `(00)^K q` are prefix-free.  The code stopping time is
`2K+2`; after the payload the leaf depth is

```text
D_K=3K+2.                                              (2.3)
```

There are `3*2^K` leaves at level `K`, each one a single half-open dyadic
interval of physical mass `2^(-(3K+2))`.  Their union is `S_K`.  The shells
are disjoint and

```text
sum_(K=0)^N m(S_K)=1-4^(-(N+1)),
sum_(K>=0) m(S_K)=1.                                  (2.4)
```

Only `u=0` is left, with zero physical mass.  Thus this is a measurable
full-mass antichain in the physical row coordinate, not an externally
randomized product extension.  The record is selected before orientation,
product time, mode, and final test.  Because both oriented views are views of
the same corrected occurrence measure, they use exactly the same
`(e,s,K,q,j)` restriction.

This is a **physical mass-coordinate stopping antichain**.  It is not called
an orbit-return-word stopping antichain: no first-return cylinder or
trajectory hazard has been constructed.

## 3. Exact native-charge obstruction

The product extension could sample `K` externally and then restrict a
physical interval only to depth `K`.  It therefore had

```text
E_product[2^K]=3/2.                                    (3.1)
```

A deterministic physical code must encode `K` in the same coordinate it
later restricts.  For (2.2), the actual physical leaf depth is `D_K=3K+2`,
so the level-`K` charge is

```text
m(S_K) 2^D_K
  =(3/4)4^-K 2^(3K+2)
  =3*2^K.                                              (3.2)
```

Hence, through cutoff `N`,

```text
sum_(K=0)^N m(S_K)2^D_K
  =3(2^(N+1)-1) -> infinity.                           (3.3)
```

Even stopping only on the shell, without payload `j`, cannot fix this:
normalizing `S_K` costs `m(S_K)^-1`, and each level contributes exactly one,
so the cutoff charge is `N+1`.

This is an instance of a general exact identity.  If a native stopped law is
a countably infinite partition into positive-mass atoms `A_i`, and the
required stopped-parent normalization cost is at least `1/mu(A_i)`, then

```text
E[mu(A)^-1]
  =sum_i mu(A_i) mu(A_i)^-1
  =sum_i 1
  =infinity.                                               (3.4)
```

In particular, if level `K` has `2^K` positive-mass native leaves, that level
contributes exactly `2^K` to (3.4), independently of how small its total
level mass `w_K` is.  No faster choice of native level tail repairs leafwise
inverse-mass normalization.

The product kernel avoids (3.4) precisely because `K` is an external mark.
Conditional on that mark, the physical row is cut into `2^K` atoms and pays
the conditional normalization `2^K`; averaging pays
`sum_K w_K 2^K=3/2`.  It does **not** pay the inverse joint-atom mass
`(w_K 2^-K)^-1`.  Identifying those two constructions would be an invalid
change of measure.

Thus the native antichain replaces the auxiliary product **record algebra**,
but not its finite charged recovery moment.  Possible escape routes are: keep
all stopped leaves as one unnormalized/reweighted family and prove a global
`Z` recovery theorem without leafwise normalization; use a finite antichain
with a quantitatively charged cemetery; or change the Gate-4 cost interface.
None is currently certified.  This conclusion is independent of the still
unknown numerical billiard recovery constants.

## 4. Repeated characteristic cuts: two exact countermodels

### 4.1 One indicator can have infinite boundary `Z`

On the unit interval with uniform density, let

```text
U=union_(n>=1) (2^-n, 2^-n+2^(-2n-2)).                (4.1)
```

The intervals are disjoint and `mu(U)=1/12`.  After normalizing the
restriction, every component contributes `1/mu(U)=12` to the
standard-family boundary functional.  Since there are countably many
components,

```text
Z(1_U mu / mu(U))=infinity.                            (4.2)
```

Therefore arbitrary characteristic multiplication does not preserve the
finite-`Z` standard-family class, even for a smooth initial density and an
open indicator.

### 4.2 Consecutive finite cuts can destroy uniform properness

Starting from `[0,1]`, at every generation retain the first and last quarter
of every current interval.  After `h` cuts there are `2^h` components, each
of length `4^-h`, total retained mass `2^-h`, and normalized weight `2^-h`
per component.  Consequently

```text
Z_h=2^h * (2^-h)/(4^-h)=4^h.                          (4.3)
```

Thus even finite-component indicators need a recovery wait or an explicit
boundary-charge registry between consecutive cuts.  A one-time Growth Lemma
cannot be silently reused hereditarily.

## 5. Maximum strict repeated-cut layer

There is a valid finite registered restart schema.  Fix a finite number `H`
of cuts and assume every actual restriction has already been represented as
a finite regular standard family satisfying

```text
Z_i/mu_i <= C_mesh 2^K_i.                              (5.1)
```

Preserve the occurrence record, recover both oriented views to properness,
and only then admit the next cut.  With the theorem-supplied constants from
the tenth round,

```text
R_total <= 2H A0 + 2A1 sum_(i=1)^H K_i.               (5.2)
```

For fixed `H` and auxiliary product depths, exact factorization gives

```text
E[2^sum(K_i) exp(gamma R_total)]
 <= exp(2 gamma H A0)
    ((3/4)/(1-exp(2 gamma A1)/2))^H                   (5.3)
```

whenever `0<gamma<log(2)/(2A1)`.

Equation (5.3) is a conditional restart theorem, not physical hereditary
recovery.  The irreducible missing restriction interface is now precise:

```text
every physical branch history + next actual indicator
 -> query-independent record-preserving regular decomposition
 -> finite normalized boundary bound with a uniform charged moment.
```

If the number of cuts is unbounded, a summable tail for `H` is additionally
required.

## 6. Why `C_p,vartheta_p` still cannot be numerical

The finite-`s` geometry is numerical:

```text
tau_min > 36337/800000 > 1/25,
curvature in [25/9,25/4],
finite horizon (3,1/512),
one-collision coefficient 204,
C_mesh=69986663973833932800.
```

The imported proof chains are not numerical:

- Stenlund--Young--Zhang, arXiv:1210.0011v4, Lemma 12 states the
  existence of `C_gr,vartheta_gr` and refers its proof to the fixed-table
  literature.  Its earlier hyperbolicity, homogeneity, curvature,
  distortion, metric-comparison, and regular-density constants are also
  unnamed.
- Their Lemma 16 states the existence of `C_p,vartheta_p` and calls it a
  direct consequence of the Growth Lemma, again without values.
- Canestrari, arXiv:2604.19671v2, Lemmas 6.13--6.14 make the dependency more
  explicit, but still import nonnumeric `theta_*`, `delta_n`, metric,
  distortion, and cone constants before choosing `n_*` and `Z_0`.

The qualitative statement `0<vartheta_p<1` does not determine the recovery
slope

```text
A1=ceil(log(2)/abs(log(vartheta_p))).                  (6.1)
```

For example, `vartheta_p=1/4` gives `A1=1`, while
`vartheta_p=1-2^-20` is equally compatible with the qualitative statement
and forces `A1>=524288`, since

```text
-log(1-2^-20)<1/(2^20-1),  log(2)>1/2.                (6.2)
```

Therefore assigning arbitrary numerical values to `C_p,vartheta_p` would be
an overclaim.  The smallest executable next task is an explicit `n`-step
expansion/cut sum and distortion-ratio certificate on the declared
homogeneity atlas; that would yield numerical Growth constants and only then
numerical propagated `C_fw,C_rev,q`.

## 7. Latest-technology boundary

The current closest tools remain:

1. Stenlund--Young--Zhang, arXiv:1210.0011v4, for uniform one-time
   standard-family recovery on the compact moving-table class;
2. Canestrari, arXiv:2604.19671v2, for an explicit symbolic Growth-Lemma
   dependency chain in the closed billiard;
3. Demers--Liverani, arXiv:2606.10155v1, Problem 8.7, which records the
   general characteristic-function/loss-of-memory restriction problem as
   open.

No inspected result supplies the missing physical restriction regularizer,
the native charged antichain moment, or executable numerical values for all
Growth-Lemma leaves.  The countermodels in Section 4 explain why a general
loss-of-memory theorem cannot be applied after arbitrary selected
indicators.

## 8. Reproducibility and fail-closed behavior

Files:

```text
deliverables/cm2_gate4_native_stopping_repeated_recovery_frontier_cert.py
deliverables/cm2_gate4_native_stopping_repeated_recovery_frontier_verifier.py
deliverables/cm2-gate4-native-stopping-repeated-recovery-frontier-manifest-2026-07-16.json
```

Replay:

```bash
PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_native_stopping_repeated_recovery_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_native_stopping_repeated_recovery_frontier_verifier.py \
  --self-test

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_native_stopping_repeated_recovery_frontier_verifier.py
```

Replay/integrity exits zero.  The self-test rejects nine independent
mutations.  Live default exits `2` because the native charged recovery
moment, hereditary repeated indicators, propagated numerical costs, and
Gate 4 remain unproved.
