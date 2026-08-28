# CM2 Gate 5 Round 59：统一无限 clearance、七位 operator join 与 Jordan anchors

日期：2026-07-20

## 结论先行

本叶没有把 `A_col` 的 restriction 偷换成全物理 law，也没有用人工 uniform
collar density 或 signed cancellation 支付 positive debt。最强真实升级是把
Round 58 分开的 coverage 与 clearance moment 两个门合并为同一个 physical
extended-tail 判据，并把 operator join 与 positive anchors 压成不可再删的最小
字段。

在实际 finite Borel owner/root law `nu` 上定义

```text
Kbar(a)=K(a),       a in A_col,
Kbar(a)=infinity,   a not in A_col,
a_k=w_Z^r_k,        a_infinity=infinity.
```

令

```text
Fbar_j=nu{Kbar>j}
      =nu(A_col^c)+nu{a in A_col:K(a)>j}.
```

则每个有限截断都有 exact Abel identity

```text
M_N=integral a_(min(Kbar,N)) dnu
   =a_0 nu(total)+sum_(j=0)^(N-1)(a_(j+1)-a_j)Fbar_j,
```

且由单调收敛

```text
Mbar=lim_N M_N=integral a_Kbar dnu.
```

因此

```text
Mbar<infinity
iff nu(A_col^c)=0 and integral_(A_col)w_Z^r_K dnu<infinity.
```

这一个 extended moment 同时检测 full coverage 与最优 clock moment；不再允许
“restricted moment 很小”掩盖未覆盖 owner mass。

由于 `r_k=ceil(beta(k+1))` 且 `0<beta<1`，定义 active clock set

```text
S={j:r_(j+1)=r_j+1}.
```

只有 `j in S` 时 Abel increment 非零，并且严格等于

```text
a_(j+1)-a_j=(w_Z-1)w_Z^r_j.
```

故最强 exact tail criterion 是

```text
Mbar<infinity
iff sum_(j in S) w_Z^r_j Fbar_j<infinity.
```

该 series 有限本身已经强迫 `Fbar_j->0`，从而自动强迫 full coverage。它仍是
物理接口而不是物理结论：当前 frozen rows 没有给这条 series 的上界。

严格状态保持：

```text
Gate 5 maturity = 10/18
complete 18-field blocks = 0
complete composite gates = 0/5
CM2 = NO-GO_FOR_CLAIM
```

## 一、依赖与实际 owner law

本叶 append-only hash-pin：Round 25 physical-root theorem、Round 42 numerical
`C24` Growth block、Round 49--58 全部 Gate-5 owner/collar/suffix 叶，共 `12`
个 manifest。

冻结链实际给出：

- Round 50：standard-Borel 全局 owner/root registry 与 finite Borel law；
- Round 54：Borel `A_col={d_other>0}`、`K`、`ell`、labelled `E/K_word/Tr`；
- Round 56：最短 exact-gamma clock `r_K`；
- Round 58：restricted extended Abel ledger，但 coverage、moment、`H/J` 与
  positive anchor 仍未认证。

因此 `Kbar` 是实际 owner law 上的 Borel extended mark，并非 abstract model
law。`a_infinity=infinity` 只通过有限截断与 Tonelli/单调收敛使用；证明中没有
进行 `infinity-infinity` 运算。

## 二、active-clock Dini 临界线

令 `alpha_opt=beta log_2(w_Z)`。由于

```text
beta(k+1)<=r_k<beta(k+1)+1,
```

`w_Z^r_k` 与 `2^(alpha_opt k)` 只差固定正因子。但精确 Abel ledger 还可删除
`r` 不增长的 plateau indices，得到上面的 active set `S`。

### 精确临界族

对 `p>0` 和 `0<c<=w_Z^r_0` 定义

```text
Fbar_j=c/[w_Z^r_j (j+1)^p],
Fbar_-1=1,
m_(j+1)=Fbar_j-Fbar_(j+1).
```

`r_j` 非降且 `(j+1)^p` 严增，所以 `m_(j+1)>=0`；`Fbar_j->0`，故这是 full
coverage probability tail。对 active `j`，Abel term 精确化为

```text
(a_(j+1)-a_j)Fbar_j
=c(w_Z-1)/(j+1)^p.
```

又

```text
#(S intersect [0,N))=r_N-r_0,
```

所以 `S` 的渐近密度是 `beta>0`。结论严格为：

```text
clock moment finite iff p>1.
```

特别地，pure critical exponential envelope `Fbar_j<=c/w_Z^r_j` 和
`Fbar_j->0` 仍不够；`p=1` 是 full-coverage harmonic divergence。

### 所有 polynomial moments 仍不够

在 `n>=1` 取

```text
m_n=1/[100 n w_Z^r_n],
```

剩余质量放在 `K=0`。由 `alpha_opt>0.0012`，总尾质量 `<0.071`；这确实是
probability law。它可保留 full `A_col`、`B=14`、所有 polynomial `K`
moments，甚至令所有 future join bits 为真且 recovery capacity `R>=r_K`，可是

```text
sum_n m_n w_Z^r_n=(1/100)sum_n 1/n=infinity.
```

因此 perfect suffix join 也不能替代 tail moment。

### Orlicz 等价

对单个 finite owner law 与 extended nonnegative variable `X=a_Kbar`，
de la Vallée-Poussin 给出 exact equivalence：

```text
Mbar<infinity
iff exists increasing convex Phi:[0,infinity)->[0,infinity),
    Phi(t)/t -> infinity,
    integral Phi(X)dnu<infinity.
```

并有离散 Abel 形式

```text
integral Phi(X)dnu
=Phi(a_0)nu(total)
 +sum_j[Phi(a_(j+1))-Phi(a_j)]Fbar_j.
```

这是对一个 fixed law 的存在性等价，不是 uniform physical Orlicz bound；当前
manifest 没有提供可用 `Phi` 或 RHS 上界。

## 三、Round 25 不能直接闭 `A_col` coverage

Round 25 的确证明：在每个 fixed finite physical word/canonical unstable graph
上，每条 active physical boundary branch 至多一个 isolated root，稳定/不稳定
slope gap 严格大于 `50/9`，simultaneous physical roots 被 coalesce。

但它没有接上 Round 54 coverage，原因有两层。

第一，Round 50/54 的 owner token 没有 pin Round 25 component/root ID；“都是
physical root”不是 immutable same-ID equality。

第二，即使补了该 ID join，Round 54 的 `d_other` 还读取 fixed word 中全部
singularity、homogeneity、owner、hole 与 chart cuts。Round 25 的 finite
physical-root theorem 不控制在 grazing root 处积聚的非物理 homogeneity cuts。
collision-area nullity也不能推出 singular owner-root trace nullity。

精确分解为

```text
A_col^c={d_other=0}=N_coinc union N_acc,
```

其中 `N_coinc` 是 anchor 同时落在另一 registered boundary，`N_acc` 是不同
other cuts 在 anchor 积聚。有限测度连续性给出最短 nullity ledger：

```text
nu(A_col^c)=lim_(m->infinity)nu{d_other<2^-m}.
```

所以 full coverage 当且仅当该 limit 为零。

ordinary subregistry 上有一个 pointwise 正结论：若 exact same-ID owner root
位于 compact nongrazing chart，远离 endpoint/coincidence，且 full-word
nonphysical cuts 局部有限，则 `d_other>0`。但该 subregistry 的 owner-trace mass
并未冻结。

为避免把 logical separation 冒充新 billiard orbit，本叶的 accumulation
separator 明确只是**兼容冻结字段的 logical model**：保留一个 isolated
transverse physical root 和 slope gap，不放其他 physical root，同时让
nonphysical cut coordinates `c=1/n^2` 向 root 积聚。Round 25 所有
physical-root conclusions 都成立，但 `d_other=0`。它不是声称当前物理台球实现
了人为 cuts；它证明现有字段逻辑上不足。

coverage 最短仍需：

1. Round25→Round50/54 immutable root-ID equality；
2. grazing、endpoint、coincidence owner-trace nullity；
3. 所有 nonphysical full-word cuts 的局部有限/分离。

## 四、Round 54→Round 42 的七位 exact join

“同一个 scalar Growth constant”不足以让两个 operator composition well-typed。
本轮把 Boolean `J` 分解为七个逐块 bit：

| bit | 含义 | 当前状态 |
|---|---|---|
| `L_id` | immutable restriction/owner/event/side/word-cell 保留 | Round54 已认证 |
| `L_word` | fixed-word collar killed bit 恒定且 `K_trace=Tr K_word E` | Round54 已认证 |
| `L_input` | labelled collar family 正是 Round42 canonical input domain | 未认证 |
| `L_C24` | 9148 个 intermediate killed bits 等于 C24 policy | 未认证 |
| `L_operator` | block `K_word` 等于 `O_s^9148` 的对应正 restriction | 未认证 |
| `L_output` | output carrier/density/IDs 无 recut 或 renormalisation 地成为下一输入 | 未认证 |
| `L_horizon` | actual owner record 选择足够多 consecutive joined blocks | 未认证 |

令 `J_b` 是七位乘积。只在 `A_col` owner subregistry（也就是 `K` 真正有定义
的地方）定义 stopping mark

```text
R(a)=sup{q>=0:J_0(a)=...=J_(q-1)(a)=1},   a in A_col.
```

若七个 predicates 都在该 `A_col` subregistry 上 Borel，则 countable
initial-run tests 使 `R` 在那里 Borel。为避免在 `A_col^c` 上使用未定义的
`K`，把 policy cost 扩张为

```text
C_policy(a)=infinity,                                  a in A_col^c,
C_policy(a)=C_rec w_Z^r_K,                             a in A_col, R>=r_K,
C_policy(a)=2^(K+1),                                   a in A_col, R<r_K.
```

其 exact positive criterion 为

```text
nu(A_col^c)=0
and integral_(A_col) [
  1_{R>=r_K} C_rec w_Z^r_K
 +1_{R<r_K} 2^(K+1)
] dnu < infinity.
```

等价地，这是 `integral C_policy dnu<infinity`。因此这个 policy criterion
本身也强迫 full `A_col` coverage；它没有在坏集合上偷偷调用 `K`。

Round 51 的 all-finite-regular-suffix catalog 不选择 actual seven-bit initial
run；一个 disjoint tagged domain 上相同 scalar recurrence 也不能把
`L_input/L_operator` 改为真。因此 physical `R` 尚未构造。

## 五、positive Jordan anchors 的 exact identity

对 finite positive marginals `mu_plus,mu_minus`，在 measure lattice 中令

```text
lambda=mu_plus wedge mu_minus,
J=mu_plus-mu_minus.
```

则有 exact positive identity

```text
mu_plus+mu_minus=abs(J)+2 lambda.
```

所以对任意 nonnegative Borel charge `a`，

```text
integral a dmu_plus+integral a dmu_minus
=integral a dabs(J)+2 integral a dlambda.
```

这给出 positive F10/cemetery 的必要充分接口：weighted Jordan-variation
moment 和 weighted common-mode moment 必须都有限。signed BL/OT 既不控制
unbounded `a` 下的 `abs(J)`，也完全看不见 `lambda`。

一个 positive anchor 加 transport 可以合法搬运，但必须有 pointwise charge
inequality：若某 coupling 上

```text
a(y_plus)<=C a(y_minus)+L c(y_plus,y_minus)
```

且 `mu_minus` 的 `a`-moment 与该 coupling 的 `c`-cost 都有限，则 `mu_plus`
moment 有限。

仅“one anchor + finite transport cost”仍不够。精确 separator 取

```text
mu_minus=delta_y0,   a(y0)=1,
mu_plus=sum_(n>=1)2^-n delta_xn,
c(xn,y0)=2^-n,       a(xn)=2^(2n).
```

则 anchor moment 为 `1`，transport cost `sum 4^-n<infinity`，但

```text
integral a dmu_plus=sum 2^n=infinity.
```

Round 58 的 zero-signed separator 是另一极端：`mu_plus=mu_minus` 时
`J=abs(J)=0`，但 `lambda=mu_plus` 可以有无限 weighted moment。两者共同证明
positive Jordan anchors 不能删除。

## 六、最新官方技术检索

2026-07-20 通过 `export.arxiv.org` API 复核：

- `arXiv:2606.10155v1`，*Recent Progress in the Application of Transfer
  Operators to Dispersing Billiards*；
- `arXiv:2606.19621v2`，*Regularity of the positional penalization function in
  inter-sign optimal transport on real measures*，API updated
  `2026-07-17T10:16:59Z`。

前者不生成 actual owner-clearance tail、singular trace coverage 或七位
operator join；后者不把 inter-sign cancellation 转成 unbounded positive
Jordan anchors。没有外部 theorem 被导入 certificate dependency。

## 七、严格边界与 continuation

```text
unified Kbar ledger:                         CERTIFIED_BOREL_EXTENDED_VALUED
unified coverage+clock Abel criterion:       CERTIFIED_EXACT_IFF
active Dini / Orlicz interfaces:             CERTIFIED_EXACT

physical A_col full coverage:                NOT_CERTIFIED
physical same-law clock moment finite:       NOT_CERTIFIED
physical tail/Orlicz bound:                  NOT_CERTIFIED
physical recovery capacity R:                NOT_CERTIFIED
physical Round54/Round42 operator join:       NOT_CERTIFIED
physical hybrid suffix schedule:             NOT_CERTIFIED
weighted Jordan-variation anchor:            NOT_CERTIFIED
weighted common-mode anchor:                 NOT_CERTIFIED
positive F10 / strong cemetery:              NOT_CERTIFIED

Gate5 maturity / complete blocks:            10/18 / 0
Gate5 / CM2:                                 NOT_CERTIFIED / NO-GO_FOR_CLAIM
```

下一条最短物理路线已经压成三项：

1. 直接估计 unified `Fbar_j` active Abel series；这一步同时解决 coverage 与
   optimal clock moment，或等价提供一个 physical Orlicz bound；
2. 在 actual owner law 上构造七位 predicates 与 Borel recovery capacity `R`，
   然后分别估计 long recovery 与 short raw debt；
3. 对 positive F10/cemetery 分别证明 weighted `abs(J)` 与 common-mode
   `lambda` moments，或给一个 marginal anchor 加合法 pointwise transport
   inequality。

## 八、机验

本叶完成 syntax、`12/12` dependency pins、strict JSON、independent arithmetic
replay、deterministic result replay、manifest byte-identical reemit、hostile
mutation rejection、SHA ledger 与默认 fail-closed 入口。精确计数见冻结
manifest/SHA sidecar；cert 与 verifier 默认均 exit `2`。
