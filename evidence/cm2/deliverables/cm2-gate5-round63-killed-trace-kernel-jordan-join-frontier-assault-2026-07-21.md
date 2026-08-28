# CM2 Gate 5 Round 63：killed trace-kernel、cost-Jordan join 与 complement small-gap frontier

日期：2026-07-21

## 结论先行

本叶没有找到 actual same-owner insertion-time contraction，因此严格状态保持

```text
Gate 5 maturity = 10/18
complete 18-field blocks = 0
complete composite gates = 0/5
CM2 = NO-GO_FOR_CLAIM
```

本轮有三项严格推进。

第一，fixed-`j` 与 all-time 之间的缺口被压成一个保持 immutable insertion
lineage 的正 killed trace-kernel/Lyapunov drift 接口。令 `Lambda_j` 是 time slice
`E_j` 上的正 debt law，`K_j:E_j -> SubProb(E_(j+1))`，且

```text
Lambda_(j+1) <= Lambda_j K_j,
K_j V_(j+1) <= kappa V_j,
V_j>=1,
Lambda_0(V_0)<infinity,
w_Z kappa<1.
```

则

```text
sum_j w_Z^j Lambda_j(1)
 <= Lambda_0(V_0)/(1-w_Z kappa)<infinity.
```

`j` 没有被删除：kernel 只把 lineage 从 slice `j` 送到 `j+1`，direct-sum
registry 仍保留每一个 insertion coordinate。one-point killed kernel
`K_j(1)=kappa` 证明阈值 `w_Z kappa<1` sharp；identity/shift-covariant 正 law
则每层 charge 恒定，因 `w_Z>1` 必然发散。现有冻结输入没有构造 `K_j`、`V_j`
或 drift row；Round 52 collision-null face tower 正对应“collision survivor 衰减，
trace kernel 在 face 上不杀质量”的反例，所以 collision `rho^j` 不能替代该接口。

第二，在 actual fixed-`j` owner law 上，将 Round 61 的两组 orientation-positive
F10 cost measures 真正放进同一个 measure lattice：

```text
xi_j^f=C_bad,j^f nu_j,
xi_j^r=C_bad,j^r nu_j,
J_j^cost=xi_j^f-xi_j^r,
lambda_j^cost=xi_j^f wedge xi_j^r.
```

于是逐 `j` 有 exact identity

```text
xi_j^f+xi_j^r=|J_j^cost|+2 lambda_j^cost,
|J_j^cost|(X_j)+2 lambda_j^cost(X_j)
 <2395081816467609/880000.
```

限制到 `A_col^c` 后恒等式仍成立，因此 fixed-`j` complement variation、common
mode 与 total positive charge 均已支付。该对象严格命名为
`orientation-cost Jordan law`：它不是 Round 54 actual signed-flux hit/miss
`J_p`，不能据此升级 physical positive F10 或 strong cemetery。all-time 仍需要
上述正 drift；common mode 不能用 signed telescope 消失。

第三，`A_col^c` 被进一步拆成可验收的同律 rows。由于
`xi_j^f,xi_j^r << nu_j`，Round 62 已证的 source exact-grazing nullity 自动升级为
零 F10 cost。其余部分为

```text
N_cut^rem = countable union of remaining exact-cut coincidences,
N_acc     = {every registered gap is positive, but their infimum is zero},
pre-regularization cemetery.
```

若 `C_(j,m)` 枚举 exact cuts，则 positivity 给出

```text
chi_j(N_cut^rem)=0 iff chi_j(C_(j,m))=0 for every m.
```

若

```text
A_(j,k)={all registered gaps positive and inf_m d_(j,m)<=2^(-k)},
```

则 `A_(j,k)` 递减到 `N_acc`，故

```text
chi_j(N_acc)=lim_(k->infinity) chi_j(A_(j,k)).
```

这给出 exact small-gap tail interface，但 frozen source-rank tail只控制 source
`eta`，不控制 later/full-word `d_other`；剩余两层与 pre-regularization cemetery
仍未支付。

## 一、冻结依赖与重放

本叶 hash-pin 并重放：

- Round 62 aggregate report 与 15-row recursive ledger；
- Round 62 Gate-5 leaf、SHA ledger 与 independent audit；
- Gate-5 Round 39/50/52/54/61 manifests。

核心递归 pins：

```text
Round62 aggregate report SHA
873557a6653a826700d5daf11e8b118f5ddca1cf911e085f9c20aa591ab2136f

Round62 recursive ledger SHA
e54b5a1de2b4bddf0c7589b77997b1f28284040b64b31fdfbf58af9e73233bac

Round62 Gate5 manifest / ledger SHA
ddbe8545e6471977ac7bd06b584717cbe7ffeeb62df2ac3baeb8cb70f0ad27d9
ce399f98596b9906eb89d1bd68b80d5f49a5ed29471ba2b8d9648c250a805e61

Round62 audit manifest / ledger SHA
19a02d00e2ac85849f6197054166e193e1d4e3433c21505fd4bfd2b450faea20
32504c8eda5125d11a460199c3471158720127bf2bc1081664a8a20747c7a414
```

actual assertions remain at base `s=0`. Old artifacts are untouched.

## 二、time-labelled killed trace-kernel theorem

### 2.1 Typed carrier

For every insertion time `j`, let `E_j` be a standard-Borel positive debt
carrier. It may be the disjoint sector union of

```text
complement F10,
clock / raw-Z / power-Orlicz,
orientation-cost variation,
orientation-cost common mode,
pre-regularization cemetery.
```

The full all-time carrier remains

```text
E_all=disjoint_union_(j>=0)({j}xE_j).
```

A legal `K_j` maps slice `j` to slice `j+1`, preserves every frozen immutable
non-time owner/root/event label required by the lineage, and updates the explicit
insertion coordinate. It is not a quotient identifying two time slices.

### 2.2 Positive drift theorem

Let `Lambda_j` be finite positive measures on `E_j`; let `K_j` be sub-Markov
kernels; let `V_j:E_j->[1,infinity]` be Borel. Assume

```text
Lambda_(j+1)(A) <= integral K_j(x,A)dLambda_j(x),
K_j V_(j+1)(x) <= kappa V_j(x),
Lambda_0(V_0)<infinity.
```

Then positivity gives inductively

```text
Lambda_j(V_j)<=kappa^j Lambda_0(V_0),
Lambda_j(1)<=Lambda_j(V_j).
```

For `w_Z kappa<1`, Tonelli therefore yields

```text
sum_j w_Z^j Lambda_j(1)
 <=sum_j (w_Z kappa)^j Lambda_0(V_0)
 =Lambda_0(V_0)/(1-w_Z kappa).
```

The theorem works sectorwise or after taking the positive tagged sum of all debts.
It does not use cancellation.

### 2.3 Sharpness and stationarity obstruction

On a one-point carrier, set `V=1`, let `K` retain mass `kappa`, and start from
`Lambda_0=delta_*`. Then `Lambda_j(1)=kappa^j`, so

```text
sum_j w_Z^j Lambda_j(1)<infinity iff w_Z kappa<1.
```

At equality the partial sums are `N+1`; above equality they grow geometrically.
For `K=Id` or any shift-covariant charge-preserving lineage with nonzero charge
`c`, every layer has mass `c` and the weighted sum diverges. Thus stationarity,
time homogeneity, re-encoding of `j`, or owner covariance is not a decay theorem.

### 2.4 Why the actual row is absent

Round 52 only provides a fixed-`j` bound uniform in `j`. It does not provide

```text
nu_(j+1)<=nu_j K_j,
Lambda_(j+1)<=Lambda_j K_j,
K_j V_(j+1)<=kappa V_j.
```

Its exact logical face tower has collision survivor mass `rho^j` but a
collision-null trace face of constant mass. On that face the only natural positive
kernel is charge-preserving (`kappa=1`), while `w_Z>1`. Therefore collision-SRB
survival cannot be imported onto this singular trace.

Even a hypothetical trace mass `rho^j` plus the certified `L^q`, `q<=2`, charge
would give `kappa>=sqrt(rho)>w_Z^(-1)`. The frozen threshold still fails.

## 三、actual fixed-`j` orientation-cost Jordan join

Round 61 constructs on the same actual owner/root law `nu_j` the finite positive
measures

```text
xi_j^f=C_bad,j^f nu_j,
xi_j^r=C_bad,j^r nu_j,
```

with strict upper bounds

```text
xi_j^f(X_j) <395304765824751/220000,
xi_j^r(X_j) <162772550633721/176000,
xi_j^f(X_j)+xi_j^r(X_j)
             <2395081816467609/880000.
```

The lattice of finite measures supplies

```text
J_j^cost=xi_j^f-xi_j^r,
lambda_j^cost=xi_j^f wedge xi_j^r,
xi_j^f+xi_j^r=|J_j^cost|+2lambda_j^cost.
```

Consequently

```text
|J_j^cost|(X_j)<2395081816467609/880000,
lambda_j^cost(X_j)<162772550633721/176000.
```

For every Borel `A`, restriction to `A` preserves the same identity. In particular
on `A_col^c`, fixed-time variation, common mode, and complement total are finite.
The Round-61 labelled cemetery pushforward preserves the positive total charge.
No claim is made that a noninjective pushforward preserves Jordan parts separately.

This join is useful but typed narrowly:

```text
actual fixed-j orientation-F10-cost Jordan join: CERTIFIED,
Round54 signed physical hit/miss Jordan identification: NOT CERTIFIED,
all-time weighted variation/common/complement: NOT CERTIFIED.
```

The killed trace-kernel theorem would pay all three if applied to their positive
tagged sum. No such physical kernel/drift is installed.

## 四、`N_cut`、`N_acc` 与 cemetery

Put

```text
chi_j=1_(A_col^c)(xi_j^f+xi_j^r).
```

Because `xi_j^f,xi_j^r<<nu_j`, the actual source exact-grazing set `G_src,j`
satisfies

```text
nu_j(G_src,j)=0
implies xi_j^f(G_src,j)=xi_j^r(G_src,j)=chi_j(G_src,j)=0.
```

This upgrades Round 62's mass-null subtrace to zero orientation-cost F10 charge.

For the other exact coincidences, take a countable Borel enumeration
`C_(j,m)` after removing `G_src,j`. Positivity gives the exact criterion

```text
chi_j(N_cut^rem)=0
iff chi_j(C_(j,m))=0 for every m.
```

No same-law transversal zero-set theorem is pinned for those artificial,
homogeneity, chart, owner or later-word cuts.

For accumulation, let `d_(j,m)>0` denote every registered individual gap and

```text
A_(j,k)={all m:d_(j,m)>0, and inf_m d_(j,m)<=2^(-k)}.
```

The sets decrease to `N_acc`, hence continuity from above gives

```text
chi_j(N_acc)=lim_k chi_j(A_(j,k)).
```

Thus a same-law bound `chi_j(A_(j,k))<=C_j tau^k`, `tau<1`, would prove
fixed-`j` nullity; a drift-compatible bound on `C_j` would pay the all-time sum.
Neither row exists. The source rank `B` only sees source `eta` and cannot be renamed
as full-word `d_other`.

Corner/simultaneous physical events are absent inside the already-regular owner
domain. Their pre-regularization removed law lies outside `nu_j`; no positive mass,
variation/common-mode, or all-time cemetery bound is certified for it.

## 五、clearance、suffix 与 all-time debt

Round 62's exact extended identities remain valid:

```text
outer active-Abel identity,
outer raw-Z_col / power-Orlicz finiteness iff,
outer Jordan/common-mode identity.
```

The killed trace-kernel theorem gives a single legal sufficient route: put each
positive debt in its own tagged sector of `Lambda_j` and establish the same drift.
It does not make the frozen RHS finite by itself.

Suffix typing remains

```text
seven predicates Borel: 7/7,
universal values:        2 true / 5 open,
physical R>=r_K:         NOT_CERTIFIED.
```

The five open bits remain

```text
L_input, L_C24, L_operator, L_output, L_horizon.
```

If `J_b` is the seven-bit product, then the Borel first-failure cells

```text
F_b={J_0=...=J_(b-1)=1, J_b=0}
```

partition finite failures, and

```text
{R<r_K}=disjoint_union_b (F_b intersect {b<r_K}).
```

No frozen theorem makes those cells empty. Even an arbitrarily strong positive
decay row would pay their charge but would not prove the requested universal
pointwise truth.

## 六、最新技术审计

Official arXiv/API checks through 2026-07-21 found no theorem that supplies the
missing same-owner trace drift:

- `arXiv:2604.19671v2` treats a Sinai billiard with small holes starting from
  already-standard families and survival normalization; it does not construct this
  singular owner/coarea trace kernel or its Lyapunov drift.
- `arXiv:2412.04615v3` develops operator-renewal escape/hitting asymptotics for
  nonuniformly hyperbolic/open systems, with applications stated for one-dimensional
  nonuniformly expanding systems; it does not identify the CM2 owner trace law.
- `arXiv:2606.19621v2` concerns signed inter-sign optimal transport regularity; it
  does not pay positive common mode or complement cemetery.

No external theorem is imported into the certificate.

## 七、严格状态

```text
source exact-grazing mass/F10 cost:                CERTIFIED_ZERO_FIXED_J
remaining N_cut exact-zero rows:                   NOT_CERTIFIED
N_acc same-law small-gap tail:                     NOT_CERTIFIED
pre-regularization cemetery:                       NOT_CERTIFIED

time-labelled killed trace-kernel drift theorem:   CERTIFIED_EXACT_CONDITIONAL
actual K_j / V_j / kappa<w_Z^-1:                   NOT_CERTIFIED
stationary/identity-kernel shortcut:                CERTIFIED_FALSE_BY_SEPARATOR

fixed-j orientation-cost Jordan join:              CERTIFIED
fixed-j cost variation/common/complement finite:   CERTIFIED
Round54 physical signed-flux Jordan alignment:      NOT_CERTIFIED
all-time weighted variation/common/complement:      NOT_CERTIFIED

outer active-Abel/raw-Z/Orlicz finite RHS:          NOT_CERTIFIED
suffix Borel typing / universal truth:              7/7 / 2 true + 5 open
physical R>=r_K:                                    NOT_CERTIFIED
positive F10 / strong cemetery:                     NOT_CERTIFIED

Gate5 maturity / blocks:                            10/18 / 0
Gate5 / CM2:                                        NOT_CERTIFIED / NO-GO_FOR_CLAIM
```

## 八、下一最短路线

1. materialize actual time-slice kernels `K_j` on the owner trace lineage and a
   weight `V_j` satisfying `K_jV_(j+1)<=kappa V_j`, `w_Zkappa<1`;
2. prove same-law zero-set rows for every remaining `N_cut` signature and a
   quantitative small-gap tail for `N_acc`;
3. attach complement, clearance/Orlicz, cost-Jordan and pre-cemetery sectors to the
   same positive drift, with no signed cancellation of common mode;
4. prove the five suffix values and `R>=r_K` independently of summability;
5. identify the actual orientation-cost Jordan law with the requested Round-54
   physical signed-flux charge, or provide a separately typed lawful bridge.

## 九、机验

The companion certificate/verifier checks strict JSON, dependency and recursive
pins, exact rational F10 sums, measure-lattice Jordan arithmetic, killed-kernel
geometric replay including the sharp boundary, complement decreasing-tail rows,
deterministic replay, producer reemit, leaf-wise hostile mutations, SHA sidecar and
default fail-closed exit `2`.
