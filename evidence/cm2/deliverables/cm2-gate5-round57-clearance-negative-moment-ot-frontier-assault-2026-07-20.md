# CM2 Gate 5 Round 57：clearance 负矩、hybrid suffix 与截断最优运输前沿

日期：2026-07-20

## 结论先行

本叶没有把任意有限 Borel owner law 偷换成有界密度，也没有让 signed
cancellation 支付 positive F10/cemetery。它完成了三项严格推进，并给出一个
直接命中冻结字段的非蕴含反例。

1. Round 56 的最优 collar emission moment 不再只用几何 tail 表述；它与
   **同一个实际 owner law** 上的极低阶负矩严格双向等价：

   ```text
   M_clock=sum_k w_Z^r_k m_k < infinity
   iff
   M_neg=integral min(1,d_other)^(-alpha_opt) dnu < infinity,

   alpha_opt=0.0012406563164308641348787500994058785...
   ```

   这把 physical weak-clearance 的第一缺口压缩成一个精确标量，而不是
   “需要某个 tail”的模糊接口。临界指数处还得到 sharp Dini 判据。

2. “每个 level 都有无界 suffix horizon”不是抽象定理的必要形式。把 level
   `k` 分成可等到 `r_k` 的 long 部分与 horizon 不足的 short 部分，只需

   ```text
   C_rec sum_k w_Z^r_k m_k^long
   +sum_k 2^(k+1)m_k^short < infinity.
   ```

   long 部分做 Round-56 recovery，short 异常部分直接支付 raw collar debt。
   这是更弱、更可核的 joint clearance/horizon 接口；物理同算子绑定和 short
   debt 目前仍未给出。

3. 在一个 immutable physical record/rank 内，把 Round-55 的 sync/product
   coupling 再压缩为截断 cost `c=min(2,d)` 的最优运输值

   ```text
   d_p^OT=inf_pi integral c d pi.
   ```

   则

   ```text
   ||J_p||_(BL*) <= d_p^OT
                 <= min(d_p^sync,d_p^product)=d_p^best.
   ```

   flip 模型中 `d_OT=0<d_best=1/2<d_sync=1`，所以这是对 Round-55 best
   witness 的真实严格改进。加权闭合只需 `sum w_Z^p d_p^OT<∞`，不必有统一
   `delta_sync<1/w_Z` 几何率；临界率乘 `(p+1)^-2` 已足够。

但冻结的 physical fields 仍不能支付这些新接口。延伸 Round-54 的精确
separator，取 `p_n=2^-n`、`B_n=14`、每个 record 只有一个 other boundary、
`d_n=2^(-n^2)`。它具有 full `A_col` mass、零 clearance 集为空、有限
`Z_parent,B=2^14`，并满足比 Round-52 `4^-b` 更强的 rank tail；可是

```text
sum_n p_n d_n^(-alpha_opt)
 =sum_n 2^(alpha_opt n^2-n)
 =infinity.
```

因此 fixed-insertion rank tail、全部有限 rank moments、逐 record 有限边界数
和正 clearance 仍不推出 physical weak-clearance moment。

严格状态保持：

```text
Gate5 maturity = 10/18
complete 18-field blocks = 0
complete composite gates = 0/5
CM2 = NO-GO_FOR_CLAIM
```

## 冻结输入

本叶 append-only pin 四个 manifest：

- Round 52 fixed-insertion same-ID owner rank-tail transfer：
  `ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b`；
- Round 54 collar / pairing / directional-BV：
  `87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5`；
- Round 55 synchronised pairing / delayed collar：
  `ff54ad55f1e065ccf390f83a83cc6135aa22f0cabc7753fd700b38e05af1701c`；
- Round 56 optimal collar recovery clock：
  `c2d872c1f430bae123f9c4171bd459cd11d12e6cc15425521777da71047c2479`。

冻结精确常数为

```text
gamma=(2000/1999)(1+48*9148)(900337/901685)^9148,
rho=(111718729/111718750)^9148,
w_Z=(1+rho^-1)/2,
beta=log(2)/log(1/gamma),
alpha_opt=beta log_2(w_Z).
```

并保留所有旧 frontier：owner/root law 只是任意有限 Borel law；physical
weak-clearance、Round54/Round42 same-operator、unbounded suffix 与 physical
same-source rate 全部为 `NOT_CERTIFIED`。

## 一、最优 clock moment 与 clearance 负矩严格等价

在实际 `nu|A_col` 上令

```text
delta(omega)=min(1,d_other(omega)) in (0,1].
```

Round-54 selector 是满足

```text
2^(-k)<=delta<2^(-(k-1)), k>=1,
delta=1, k=0
```

的最小 dyadic level。Round 56 的 clock 为

```text
r_k=ceil(beta(k+1)).
```

由 ceiling 与 dyadic cell 两侧直接得到逐点界

```text
w_Z^beta delta^(-alpha_opt)
 <= w_Z^r_k
 <  w_Z^(beta+1) 2^alpha_opt delta^(-alpha_opt).
```

积分即得

```text
w_Z^beta M_neg
 <= M_clock
 <  w_Z^(beta+1)2^alpha_opt M_neg.
```

所以这是 finiteness 的双向等价，不只是一个充分条件。它也说明微小的
`alpha_opt` 仍不能由“有限 measure”自动支付：任意正阶负矩都可能发散。

### layer cake 与临界 Dini 边界

Tonelli 给出 exact identity

```text
M_neg
=nu(A_col)
 +alpha_opt integral_0^1
    t^(-alpha_opt-1) nu{delta<t} dt.
```

因此：

- 若 `nu{delta<t}<=C t^eta` 且 `eta>alpha_opt`，则

  ```text
  M_neg<=nu(A_col)+alpha_opt C/(eta-alpha_opt).
  ```

- 在临界 `eta=alpha_opt`，若

  ```text
  nu{delta<t}
  <=C t^alpha_opt/(log(e/t))^(1+epsilon),
  ```

  则

  ```text
  M_neg<=nu(A_col)+alpha_opt C/epsilon.
  ```

- `F(t)=t^alpha_opt/log(e/t)` 是一个合法 probability CDF，且对应负矩
  对数发散。这证明 Dini 的 log power `1` 是 sharp 边界，不能把临界纯
  power tail 冒充可积性。

## 二、比 uniform density/complexity 更弱的 recordwise pullback 判据

写实际 owner law 为 `nu=sum_a nu_a`。在 record `a` 的 collar coordinate
`c` 中，假设

```text
dnu_a/dc <= D_a,
Leb{dist(c,E_a)<epsilon} <= A_a epsilon^eta,
delta_a >= g_a dist(c,E_a)^q,  0<g_a<=1.
```

那么

```text
nu_a{delta_a<t}
 <=D_a A_a g_a^(-eta/q) t^(eta/q).
```

所以只需

```text
C_pull=sum_a D_a A_a g_a^(-eta/q)<infinity,
eta/q>alpha_opt.
```

这严格弱于分别要求全 record uniform `D`、uniform boundary count 和
uniform bi-Lipschitz pullback gap：三个量都可随 record 增长，只要它们的
联合常数在真实 owner 权重下可加。

对 Round-56 inverse-square shell 的 abstract `eta=2/3`，容许

```text
q < (2/3)/alpha_opt
  = 537.3499959961045533537631613645977625...
```

仍有极大指数余量。真正缺的不是 exponent 大小，而是**同一物理 law** 的
`D_a,A_a,g_a` 及其可加性。冻结文件没有这些字段，故不升格。

## 三、fixed rank tail 不推出最优 weak-clearance

对 `n>=1` 取 disjoint records `a_n`：

```text
p_n=2^(-n),
parent length=1,
B_n=14,
d_n=2^(-n^2).
```

每个 record 只放一个 other analytic boundary，pullback 取 identity。于是

```text
sum_n p_n=1,
nu(A_col)=1,
nu{d=0}=0,
Z_parent=1,
Z_parent,B=2^14.
```

由于 `B=14` 恒定，

```text
nu{B>b}=0, b>=14,
integral 2^(qB)dnu=2^(14q)<infinity
```

对每个有限 `q` 都成立。这比 Round-52 fixed-insertion `4^-b` upper tail 更强。

但 selector level 为 `k_n=n^2`，且

```text
log_2[p_n d_n^(-alpha_opt)]
 =alpha_opt n^2-n.
```

符号在 `n=807` 后转正并趋向 `+infinity`：

| `n` | `alpha_opt n^2-n` |
|---:|---:|
| 805 | `-1.023690544889268995...` |
| 806 | `-0.024993219119146873...` |
| 807 | `0.976185419283836975...` |
| 1000 | `240.656316430864134...` |
| 2000 | `2962.625265723456539...` |

因此负矩项本身趋向无穷，最优 clock moment 也由双向等价发散。这个模型是
冻结字段的 logical nonimplication，不声称实际 billiard law 发散；它证明
下一步必须提供 clearance/gap 与 owner 权重的联合信息。

## 四、long/short hybrid suffix ledger

令 `H(omega)` 是 insertion 后实际可用的 compatible C24 block horizon。
在 level `k` 上分成

```text
L_k={H>=r_k},
S_k={H<r_k}.
```

在 long 部分，若 Round54 collar word 与 Round42 `O_s^9148` 已按相同
owner/event/side/word-cell ID 完整绑定，则

```text
Q_long
 <=C_rec sum_k w_Z^r_k m_k^long.
```

short 部分不假装已经 recovery；保留原 collar 并支付

```text
Q_short=sum_k 2^(k+1)m_k^short.
```

于是

```text
Q_hybrid
 <=C_rec sum_k w_Z^r_k m_k^long
   +sum_k 2^(k+1)m_k^short.
```

这说明 deterministic all-level infinite horizon 可以被一个更弱的 joint
exceptional-debt theorem 代替。它也保留 Round-56 的警告：只控制
`sum m_k^short` 不够；short **mass** 不能替代 short **debt**。

当前 physical registry 没有：

1. long 部分的 Round54/Round42 same-operator 逐字 join；
2. `H` 与 clearance level 的同 law joint ledger；
3. short 部分 direct collar debt 的可积性；
4. recovery 后进入同一个 fixed physical norm/operator block 的 join。

因此 hybrid theorem 仍是 conditional frontier。

## 五、截断最优运输严格改进 Round-55 coupling

在一个 immutable record/rank `p` 内，Round 55 已有 equal-mass marginals
`mu_p^+,mu_p^-`。令

```text
c(y+,y-)=min(2,d(y+,y-)),
d_p^OT=inf_{pi in Couplings(mu_p^+,mu_p^-)} integral c d pi.
```

对 `||phi||_BL=max(||phi||_infinity,Lip(phi))`，任一 coupling 都有

```text
|J_p(phi)|
 <= integral |phi(y+)-phi(y-)| d pi
 <= ||phi||_BL integral c d pi.
```

取 inf 得

```text
||J_p||_(BL*)<=d_p^OT.
```

Round-55 sync 与 product 都是 admissible coupling，故

```text
d_p^OT<=d_p^best.
```

这里只用 scalar infimum；没有宣称连续 record 参数上的 measurable optimal
coupling kernel，也没有把它偷换成 positive Markov operator。

### 严格例

在 `{0,1}` 上取 uniform `lambda`、`H=identity`、`M=flip`。则

```text
mu^+=mu^-=uniform,
d_OT=0,
d_product=1/2,
d_sync=1.
```

所以 `d_OT<d_best=1/2`，并修复了 sync/product witness 在 `J=0` 时仍可能
保持正 cost 的松弛。

### 加权条件无需 subcritical 几何率

exact sufficient interface 是

```text
sum_p w_Z^p d_p^OT<infinity.
```

例如

```text
d_p^OT<=w_Z^(-p)/(p+1)^2
```

给出

```text
sum_p w_Z^p d_p^OT
 <=sum_p 1/(p+1)^2
 <2.
```

而该序列对任何 `delta<1/w_Z`、有限 `C` 都不满足
`d_p^OT<=C delta^p`，因为

```text
[w_Z^(-p)/(p+1)^2]/delta^p
 =(1/(w_Z delta))^p/(p+1)^2 -> infinity.
```

因此 Round-55 的 uniform geometric rate 是方便的充分条件，不是闭合
signed BL resolvent 的必要形式。

还可用 good/bad 分解：若某 admissible coupling 总质量 `m_p`，除 coupling
质量 `b_p` 外都有距离至多 `epsilon_p`，则

```text
d_p^OT<=m_p epsilon_p+2b_p.
```

这允许“多数同源像接近 + 少量坏像质量衰减”的物理证明，而不要求全支撑
uniform separation。

但没有现成物理 estimate 控制 `d_p^OT`、`epsilon_p` 或 `b_p`。此外这仍是
signed BL route，不能支付 positive F10/TV face tower 或 cemetery mass。

## 六、最新官方技术检索

2026-07-20 通过 `export.arxiv.org` 官方 API 检索了 2025--2026 的
dispersing billiards、Sinai billiards linear response、standard families、
moving billiards、normal traces 与 divergence-measure fields。相关最新版本：

- `arXiv:2606.10155v1`，dispersing-billiard transfer-operator review；
- `arXiv:2604.19671v2`，Sinai billiards with small holes linear response；
- `arXiv:2503.09536v2`，extended divergence-measure normal trace / Arens--Eells；
- `arXiv:2607.11467v1`，rough-domain tensor divergence-measure Gauss--Green。

前两者没有给当前同一 owner law 的 clearance 负矩、full-word
pullback-Minkowski 常数或 hit/miss optimal-transport decay；后两者提供 signed
normal-trace/Gauss--Green technology，但没有 positivity、owner IDs、killed C24
same-operator join 或数值 suffix schedule。没有找到可直接升 Gate-5 字段的
官方 theorem，外部文献未作为 certificate dependency。

## 七、严格状态与下一步

```text
optimal-clock / negative-moment equivalence: CERTIFIED
critical Dini clearance frontier:            CERTIFIED
summable pullback-Minkowski route:            CERTIFIED_CONDITIONAL
rank tail => weak clearance:                  FALSE_BY_SEPARATOR
hybrid long/short suffix ledger:              CERTIFIED_CONDITIONAL
truncated OT <= Round55 d_best:                CERTIFIED
critical-polynomial signed-BL route:           CERTIFIED_CONDITIONAL

physical same-law negative clearance moment:  NOT_CERTIFIED
physical owner density/Minkowski constants:    NOT_CERTIFIED
physical pullback-gap summability:             NOT_CERTIFIED
Round54/Round42 same-operator join:             NOT_CERTIFIED
physical unbounded or hybrid suffix ledger:    NOT_CERTIFIED
physical same-source or OT decay:              NOT_CERTIFIED
positive F10 from signed transport:            NOT_CERTIFIED
complete F10/F13/F14/F15/F17/F18:              NOT_CERTIFIED
strong cemetery:                               NOT_CERTIFIED

Gate5 maturity / complete blocks:              10/18 / 0
Gate5 / CM2:                                   NOT_CERTIFIED / NO-GO_FOR_CLAIM
```

最短 continuation 已进一步具体化为二选一：

1. 在同一 owner registry 上直接估计
   `integral min(1,d_other)^(-alpha_opt)dnu`，可使用 recordwise
   `sum D_a A_a g_a^(-eta/q)`，再补 same-operator 与 hybrid suffix joint debt；
2. 在每个 immutable signed record 内估计 `d_p^OT`，或 good/bad
   `m_p epsilon_p+2b_p` 的 `w_Z`-加权和。

任何一条都仍须单独补 post-recovery physical operator、positive F10 与
cemetery；signed cancellation 不跨过正质量边界。

## 八、机验

证书和 verifier 完成：

```text
syntax:                         2/2 PASS
dependency hash pins:          4/4 PASS
strict JSON:                   duplicate/NaN rejected
deterministic result replay:   PASS
hostile mutations:             92/92 rejected
manifest reemit:               byte-identical
default cert/verifier:         exit 2 / exit 2
Gate5 maturity:                10/18
CM2:                           NO-GO_FOR_CLAIM
```

文件：

- `cm2_gate5_round57_clearance_negative_moment_ot_frontier_cert.py`；
- `cm2_gate5_round57_clearance_negative_moment_ot_frontier_verifier.py`；
- `cm2-gate5-round57-clearance-negative-moment-ot-frontier-manifest-2026-07-20.json`；
- 本报告及 SHA ledger。
