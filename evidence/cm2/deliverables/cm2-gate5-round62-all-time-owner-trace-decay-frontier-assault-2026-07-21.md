# CM2 Gate 5 Round 62：all-time owner registry、trace-strata 与 weighted positive frontier

日期：2026-07-21

## 结论先行

本叶没有把 fixed-`j` 的有限性偷加成 all-time sum，也没有删除 immutable
`time-j` 后把不同 Duhamel insertion 冒充同一事件。严格状态保持

```text
Gate 5 maturity = 10/18
complete 18-field blocks = 0
complete composite gates = 0/5
CM2 = NO-GO_FOR_CLAIM
```

本轮有三项严格推进。

第一，在每个 actual fixed-`j` regular owner law 上，source endpoint exact
grazing 子层已证明为零。Round 39 的 raw coarea tail

```text
m_occ{B>b} <= (9158592/6875) 4^(-b)
```

以及 source-marked copy 投影后的 measure domination
`(pi_src)_#m_j^own<=m_occ` 给出

```text
m_j^own{eta=0}=0,
nu_j{retained eta=0}=0.
```

corner/simultaneous physical events 在 regular owner domain 内也已按冻结定义排除。
但这不等于 `A_col` full coverage：artificial/homogeneity/chart/endpoint exact cuts
及 source 非掠射但 future/full-word clearance 为零的 accumulation 仍未认证 null；
此前送入 cemetery 的 corner/simultaneous-event charge 也没有被本轮支付。

第二，构造了一个 canonical minimal time-labelled all-insertion registry：

```text
X_all = disjoint_union_(j>=0) ({j} x X_j).
```

`j` 是 Round 50 physical-event signature 的 immutable coordinate。其 injective
Borel recoding/同构当然同样合法；精确要求是任何合法 owner quotient 都必须保留
`j` 或等价 immutable insertion coordinate。不同 insertion times 代表不同物理
insertion/Duhamel terms，不能 cross-time collapse/deduplicate。对

```text
c_j = integral_(A_col^c) C_bad,j^bi dnu_j
```

定义 time-labelled weighted measure，得到 exact criterion 与 outer Abel identity

```text
Xi_bad^w(X_all)<infinity
iff sum_j w_Z^j c_j<infinity,

sum_j w_Z^j c_j
=T_0+(w_Z-1)sum_(n>=1)w_Z^(n-1)T_n,
T_n=sum_(j>=n)c_j.
```

现有 actual bound 只对每个 `j` 给同一个常数，没有任何 decay，所以 RHS 仍未
认证 finite。精确 separator 取

```text
b_j=w_Z^(-j)/(j+1).
```

则 `sum b_j<infinity`，每个 fixed-`j` anchor finite，甚至未加权 all-time law
finite，但

```text
sum_j w_Z^j b_j=sum_j 1/(j+1)=infinity.
```

每个 event 的 immutable `time-j` 不同，合法 owner minimization 不会合并它们。

第三，fixed-`j` 的 Abel、raw-`Z_col`/power-Orlicz 与 Jordan identities 已提升为
time-labelled direct sum 上的 exact extended identities。它们把缺口压成三个
独立的正 series，但没有提供任何 finite RHS：

```text
outer active-clock series,
outer raw-Z_col / power-Orlicz series,
outer Jordan variation / common-mode / complement series.
```

一个更强 separator 可令每个 `j` 上 `A_col` full、`K=0`、`R=infinity`、七个
suffix bits 全真，且 total unweighted mass finite；outer `w_Z^j` clock/raw-Z/
Orlicz 仍按 harmonic series 发散。因此即使未来一次性补齐五个 suffix 真值，
也不能替代真实的 insertion-time decay。

## 一、冻结依赖与参数域

本叶 hash-pin Round 39、50、52、54、59、61 Gate-5 manifests，以及 Round 61
aggregate：

```text
Round61 report SHA
b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b

Round61 recursive ledger SHA
2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265
```

actual trace/owner assertions remain at base `s=0`. All-time direct sums below are
exact interfaces on those actual fixed-time laws, or explicitly labelled logical
separators. No separator is claimed to be a new billiard realization. Old artifacts
are untouched.

## 二、actual complement trace 的可删与不可删子层

### 2.1 Source endpoint exact grazing is null

On the positive raw endpoint coarea law, Round 39 defines the endpoint rank by

```text
B=max(14,ceil(log2(1/eta))).
```

For every finite integer `b`, `{eta=0}` is contained in `{B>b}`. Hence continuity
from above and the certified tail give

```text
m_occ{eta=0}
<=lim_(b->infinity)(9158592/6875)4^(-b)=0.
```

Round 52's `m_j^own` lives on a disjoint source-marked copy, and its projection to
the raw source coordinate is measure-dominated by the same `m_occ`; therefore this
nullity transfers to every fixed `j`. Round 61's map
`q_j` retains endpoint/root coordinates and the rank. If

```text
G_src,j={a:retained eta(a)=0},
```

then

```text
nu_j(G_src,j)
=m_j^own(q_j^(-1)G_src,j)=0.
```

This is an actual same-law result, not collision-volume nullity imported onto a
singular trace.

### 2.2 Regular-domain absence versus cemetery payment

Round 50/52 send corners and simultaneous physical events to the labelled cemetery
before owner minimization. Therefore that stratum is absent inside `m_j^own` and
`nu_j`. This is a domain statement only. It does not prove that the pre-removal
physical trace has zero mass or finite strong-cemetery charge.

### 2.3 What remains in `A_col^c`

The following pieces remain open:

- exact artificial homogeneity/chart/endpoint/owner-cut coincidence;
- later-stage or full-word homogeneity accumulation with source `eta>0`;
- future singular preimage accumulation and owner-boundary accumulation;
- the pre-regularization corner/simultaneous-event cemetery law.

Thus

```text
source endpoint-grazing subtrace: CERTIFIED_NULL,
global A_col-complement nullity:  NOT_CERTIFIED.
```

## 三、canonical all-insertion owner registry

For every fixed insertion time `j`, let `X_j` denote the Round 61 actual owner/root
record space. Define

```text
X_all=disjoint_union_(j>=0)({j}xX_j).
```

A countable disjoint union of standard-Borel spaces is standard Borel. This is a
canonical minimal implementation, not the unique possible encoding: any injective
Borel recoding/isomorphic carrier is equally valid. The invariant requirement is
that the full Round-54 token and `j`, or an equivalent immutable insertion
coordinate, remain recoverable. The legal owner rule is still the Round-50 rule:
minimize only among representations of the same physical-event signature. Since
that signature contains `time-j`, two different insertion times are never
duplicates.

Deleting `j` would change the operator: in the Duhamel expansion the terms at
different insertion positions are distinct even if their geometric endpoint labels
happen to coincide. Therefore

```text
cross-j owner deduplication = ILLEGAL.
```

The unweighted direct sum

```text
nu_all=sum_j delta_j tensor nu_j on X_all
```

is sigma-finite. Its finiteness is not asserted.

## 四、all-time complement RN/F10 ledger

Round 61 provides, for each fixed `j`,

```text
C_bad,j^bi=d xi_j^bi/dnu_j,
c_j=integral_(A_col^c)C_bad,j^bi dnu_j
   <2395081816467609/880000.
```

Define the extended positive measure

```text
Xi_bad^w
=sum_j w_Z^j delta_j tensor
  [1_(A_col^c) C_bad,j^bi nu_j].
```

Positivity and the disjoint time labels give exactly

```text
Xi_bad^w(X_all)=sum_j w_Z^j c_j.
```

No density comparison across different laws is used. If

```text
T_n=sum_(j>=n)c_j,
```

finite summation by parts followed by monotone convergence gives

```text
sum_j w_Z^j c_j
=T_0+(w_Z-1)sum_(n>=1)w_Z^(n-1)T_n
```

in `[0,infinity]`. A useful sufficient interface is

```text
c_j<=C kappa^j,
w_Z kappa<1,
```

which yields `sum w_Z^j c_j<=C/(1-w_Z kappa)`. The threshold is sharp for a
geometric sequence. No actual `kappa` is available.

The harmonic separator is deliberately stronger than merely repeating the uniform
bound. Put one distinct time-labelled event at every `j` and give it charge

```text
b_j=w_Z^(-j)/(j+1).
```

Then

```text
sum_j b_j <= sum_j w_Z^(-j)<infinity,
sum_j w_Z^j b_j=sum_j 1/(j+1)=infinity.
```

Thus even finite unweighted all-time mass plus every fixed-time F10 anchor does not
pay the frozen outer weight.

## 五、outer clearance, raw `Z_col` 与 power-Orlicz

On each actual `nu_j|A_col`, retain the Round 61 definitions

```text
Y_j=w_Z^r_K,
q_col=1/alpha_opt,
Phi(t)=t^q_col,
Z_col,j=integral 2^(K+1)dnu_j.
```

The pointwise two-sided inequality is independent of `j`, so Tonelli gives the
outer exact equivalence

```text
sum_j w_Z^j Z_col,j<infinity
iff
sum_j w_Z^j integral Phi(Y_j)dnu_j<infinity.
```

Likewise, with

```text
S={k:r_(k+1)=r_k+1},
F_(j,k)=nu_j{K>k},
```

the exact double Abel identity is

```text
sum_j w_Z^j integral Y_j dnu_j
=sum_j w_Z^j[
   w_Z^r_0 nu_j(A_col)
  +(w_Z-1)sum_(k in S)w_Z^r_k F_(j,k)
 ].
```

This is an extended identity, not a finite estimate.

For the local-perfect separator, use mass `b_j=w_Z^(-j)/(j+1)` and set, on every
time-labelled record,

```text
A_col=true,
K=0,
R=infinity,
all seven suffix bits=true.
```

Every fixed-time clock/raw-Z/Orlicz value is finite and the unweighted total mass is
finite. Each outer weighted series is a nonzero constant times the harmonic series.
Therefore the missing all-time decay is independent of clearance and suffix
properisation.

## 六、suffix、Jordan 与 strong cemetery

Round 61's typing remains exact:

```text
seven suffix predicates Borel: 7/7,
universal values:               2 true / 5 open,
physical R>=r_K:                NOT_CERTIFIED.
```

No new universal value is asserted. The five open bits remain

```text
L_input, L_C24, L_operator, L_output, L_horizon.
```

For any nonnegative Borel time-dependent integrand `phi_j`, the measure-lattice identity extends by
Tonelli to

```text
sum_j w_Z^j integral phi_j d(mu_j^++mu_j^-)
=sum_j w_Z^j integral phi_j d|J_j|
 +2 sum_j w_Z^j integral phi_j d(mu_j^+ wedge mu_j^-).
```

The two positive series are independent:

- variation mode:
  `mu_j^+=b_j delta_0`, `mu_j^-=b_j delta_1`;
- common mode:
  `mu_j^+=mu_j^-=b_j delta_0`;

where `b_j=w_Z^(-j)/(j+1)`. In either mode the unweighted positive mass is finite,
while the relevant weighted series is harmonic. In common mode `J_j=0`, so signed
cancellation gives no positive bound.

Round 61's forward/reverse RN densities remain orientation-positive cost laws. They
are not identified with the Round-54 Jordan marginals or the same charge. Strong
cemetery therefore still needs three genuinely separate payments:

```text
weighted variation,
weighted common mode,
weighted A_col-complement charge.
```

## 七、pinned obstruction 与最新技术审计

Round 52's null-survivor face-tower countermodel remains binding: collision survivor
mass may decay like `rho^p`, while a collision-null face keeps trace mass one. Hence
fixed-`j` finiteness yields no trace recurrence with `kappa<1`.

Even if a trace-mass rate `rho^p` were added, an `L^q` owner charge with `q<=2`
only gives

```text
kappa=rho^(1-1/q)>=sqrt(rho)>2rho/(1+rho)=w_Z^(-1),
```

which misses the frozen threshold. A valid route needs a real same-owner
trace/coarea recurrence, or `q>2` together with trace-survivor decay, or separately
typed legal cancellation.

Latest official-source checks through 2026-07-21 found no direct import:

- `arXiv:2604.19671v2` starts from already-standard families and uses survival-mass
  normalization; it does not control this singular time-labelled owner trace;
- `arXiv:2606.19621v2` does not convert signed inter-sign transport into weighted
  positive Jordan/common-mode moments.

No external theorem is imported into the certificate.

## 八、严格状态与 continuation

```text
source endpoint-grazing null on fixed-j regular law: CERTIFIED
global A_col complement nullity:                     NOT_CERTIFIED

canonical minimal time-labelled implementation:      CERTIFIED
cross-j owner deduplication:                          CERTIFIED_ILLEGAL
all-time weighted complement anchor:                 NOT_CERTIFIED

outer active-Abel identity:                           CERTIFIED_EXTENDED_IDENTITY
outer raw-Z / power-Orlicz:                           CERTIFIED_EXACT_IFF
physical finite Abel/raw-Z/Orlicz RHS:                NOT_CERTIFIED

suffix Borel typing / universal truth:                7/7 / 2 true + 5 open
physical R>=r_K:                                      NOT_CERTIFIED

all-time Jordan split:                                CERTIFIED_EXTENDED_IDENTITY
weighted variation/common mode:                       NOT_CERTIFIED / NOT_CERTIFIED
strong positive cemetery:                             NOT_CERTIFIED

Gate5 maturity / blocks:                              10/18 / 0
Gate5 / CM2:                                          NOT_CERTIFIED / NO-GO_FOR_CLAIM
```

Shortest continuation:

1. prove an actual decay row for the time-labelled source charges, e.g.
   `c_j<=C kappa^j` with `w_Z kappa<1`, without deleting `time-j`;
2. prove nullity/finite direct charge for the remaining artificial/future/full-word
   complement strata and for the pre-regularization cemetery;
3. bound the double active-Abel series or the equivalent outer raw-`Z_col`/
   power-Orlicz series;
4. prove the five suffix values and `R>=r_K` on the actual law;
5. pin the orientation and Jordan source laws with the same charge, then separately
   sum variation, common mode and complement.

## 九、机验

The companion certificate/verifier checks strict JSON, all dependency and Round-61
aggregate pins, source-tail nullity typing, time-label non-deduplication, outer Abel
and harmonic arithmetic, Orlicz/Jordan exact interfaces, deterministic replay,
producer reemit, leaf-wise hostile mutations, SHA ledger and default fail-closed
exit `2`.
