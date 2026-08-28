# CM2 Gate 5 Round 61：complement RN anchor、七位 Borel codes 与 power-Orlicz frontier

日期：2026-07-20

## 结论先行

本叶不把 fixed-`j` 的正量偷加成 all-time sum，不把 Round 52 的
forward/reverse orientation costs 改名为 Round 54 Jordan marginals，也不把
parent-`W`、collision-SRB 或 Round-42 standard-family `Z` 换成 raw collar
`Z_col`。严格总状态保持

```text
Gate 5 maturity = 10/18
complete 18-field blocks = 0
complete composite gates = 0/5
CM2 = NO-GO_FOR_CLAIM
```

本轮有三个真实推进。

第一，在**实际 fixed-insertion owner law** 上，Round 52 的正 owner-selected
source law 经 Round 54 的 root/collar Borel map 推成 `ν_j`。forward、reverse
及 bidirectional F10 cost-weighted pushforward 均绝对连续于同一个 `ν_j`；其
Radon--Nikodym 密度给出 `A_col^c` 上实际、同律、Borel、`L¹` 有限的
`C_bad,j`。将该 complement 推向保留 endpoint/root、owner token、word-cell 与
time-`j` 的 labelled cemetery atom，不改变质量或正 charge。这个结论只在一个
固定 `j` 成立；现有 bound 对 `j` 无衰减，不能求和。

第二，actual collar input、word/C24 kernels 与 labelled outputs 已放进共同的
standard-Borel code spaces，并用 countable separating generator 编码。于是七个
suffix predicates 全部是无条件 Borel，`R` 也在 `A_col` 上无条件 Borel：

```text
Borel predicate typing: 7/7 CERTIFIED
universal values:        2 true + 5 open
R Borel:                 CERTIFIED
R >= r_K:                NOT_CERTIFIED
```

第三，raw collar `Z_col` 与 optimal clock 的一个显式 power-Orlicz moment 在
**同一 owner law** 上严格双向等价。若

```text
Y=w_Z^r_K,
q_col=log(2)/(beta log(w_Z))=1/alpha_opt,
Phi(t)=t^q_col,
```

则逐点有

```text
2^(K+1) <= Phi(Y) < w_Z^q_col 2^(K+1).
```

因此 `Z_col<∞` 当且仅当 `∫Phi(Y)dν_j<∞`。这是 explicit physical Orlicz
criterion，不是 finite RHS：现有冻结对象中没有任何同律 finite `Z_col` 可与它
连接，active Abel、raw `Z_col` 及 Orlicz moment 仍全部未认证有限。

## 一、递归依赖与冻结基线

本叶 hash-pin：

- Round 39 的 actual raw occurrence coarea/F10 law；
- Round 50 的 global standard-Borel owner registry；
- Round 52 的 fixed-insertion owner-positive transfer；
- Round 54 的 Borel `A_col,d,K,ell,E/Tr` collar law；
- Round 56 的 optimal exact-`gamma` clock；
- Round 59 的 unified Abel/Jordan frontier；
- 经 Round-60 独审修正后的 Gate-5 manifest；
- Round-60 aggregate report、recursive ledger 与 Gate-5 SHA sidecar。

Round-60 aggregate report SHA 为

```text
ef3f2739a7a0ed8c91e82400c05564f97f0c3326ebc1373764b51bbd48f04212,
```

recursive ledger SHA 为

```text
5f6c90735cbb74ec7b36f6c1d2b012ccccaafa40793d291dfcb6a0e212044e9e.
```

旧文件没有修改。

## 二、actual fixed-`j` owner law 与 `A_col^c` submeasure

固定一个 insertion time `j`。Round 52 在 disjoint source-marked union 上已经
给出

```text
m_j^own
=sum_a 1_(E_(j,a)^owner intersect R_(j,a)^reg) m_occ,
```

并明确不对 `j` 求和。先按 Round 54 的 half-open `word-cell` 做可数互斥细分，
再施加 Borel root/collar map `q_j`。`q_j` 保留

```text
(restriction-id,time-j,physical-event-signature,primitive-key,
 connected-rank-0,side-label,word-cell)
```

以及 endpoint/root coordinates。定义

```text
nu_j=(q_j)_# m_j^own.
```

这不是“任取一个有限 Borel law”。它是从 Round-52 actual positive coarea law
出发、经同一 owner/root registry 得到的 Round-54 law 实例。Round50→54 的
projection 只忘 `word-cell`；构造 `ν_j` 时不忘它，所以 distinct labelled fibres
不被合并。

Round 54 已证明 `A_col={d_other>0}` Borel。故

```text
nu_j^bad=1_(A_col^c) nu_j
```

是同一 owner law 上的实际有限 Borel submeasure。把 complement 精确拆成互斥两
部分：

```text
N_cut = union of exact coincidences with registered other cuts,
N_acc = {all registered gaps >0 but their infimum is 0},
A_col^c=N_cut disjoint_union N_acc.
```

这个分解没有证明两部分为零。collision-area grazing nullity 仍不能导入 singular
owner trace。当前得到的是：actual bad submeasure 已物理化且 finite；它的精确
mass、是否为零以及 full coverage 均未知。

最弱的 positive mass anchor 已自动成立：

```text
C_bad,j^mass=1 on A_col^c,
integral C_bad,j^mass dnu_j^bad
<=nu_j(total)<=m_occ(total)<8064/5.
```

这只支付 mass，不冒充 F10。下一节构造真实 F10 anchor。

## 三、cost-weighted pushforward 的 RN 密度

令 `c_f,c_r>=0` 是 Round 52 已冻结的 forward/reverse orientation F10 costs。
在同一个 fixed-`j` source law 上定义

```text
xi_j^f(A)  = integral_(q_j^-1 A) c_f dm_j^own,
xi_j^r(A)  = integral_(q_j^-1 A) c_r dm_j^own,
xi_j^bi    = xi_j^f+xi_j^r.
```

若 `ν_j(A)=0`，则 `m_j^own(q_j^-1 A)=0`，所以三个 weighted pushforwards 也在
`A` 上为零。因此

```text
xi_j^f << nu_j,
xi_j^r << nu_j,
xi_j^bi << nu_j.
```

owner/root base 是 standard Borel，故可取 Borel RN versions

```text
C_bad,j^f  = d xi_j^f/dnu_j,
C_bad,j^r  = d xi_j^r/dnu_j,
C_bad,j^bi = C_bad,j^f+C_bad,j^r.
```

它们是 actual same-law densities，不是跨 law domination。positivity 与
Round-52 fixed-`j` bounds 给出

```text
integral C_bad,j^f dnu_j
  <395304765824751/220000,

integral C_bad,j^r dnu_j
  <162772550633721/176000,

integral C_bad,j^bi dnu_j
  <2395081816467609/880000,
```

且前两常数之和精确等于第三个。限制到 `A_col^c` 只会减少这些正积分。由此
得到

```text
fixed-j same-law positive complement F10 anchor: CERTIFIED.
```

在 complement 上定义 deterministic Borel kernel

```text
omega -> dagger_(t54(omega),endpoint/root,j).
```

cemetery label carrier 是 immutable token space、连续 endpoint/root chart 与
fixed insertion index 的 standard-Borel product，不是可数 atom list。带着
`C_bad,j^bi` 作 mark 推前，只在 fixed-`j` 意义下保持 marked mass 与 F10
integral。这是

```text
fixed-j labelled cemetery pushforward: CERTIFIED_CHARGE_PRESERVING.
```

它不是 strong cemetery：

- 没有跨 `j` 的 deduplicated assembly；
- bound 对 `j` 是 uniform constant，没有 decay；
- `w_Z>1`，所以把 constant bound 直接乘 `w_Z^j` 后求和必发散；
- 它没有把 orientation costs 识别成 Jordan marginals。

## 四、七位 suffix 的共同 standard-Borel codes

### 4.1 Code spaces

令 `A` 为 Round-54 actual collar records 的 countable disjoint union。每个记录
带有

```text
s, t54, block index, root/endpoint chart, orientation, ell,
finite killed-word code, retained omega.
```

`A` 是 standard Borel。令 `X` 为 labelled collision state 加 labelled cemetery
sector；cemetery sector 是 token 与连续 endpoint/root label spaces 的
standard-Borel product，而不是可数 atom 集。`X` 仍是 standard Borel，
subprobability kernels 构成 evaluation standard-Borel space `SubProb(X)`。

固定一个 countable separating algebra `{D_m}`：在各 collision charts 中使用
rational rectangles；在 labelled cemetery 的 standard-Borel tuple space 上，
先作 Borel embedding 到 `[0,1]`，再取有理区间/柱集生成元，不逐原子加入。对
standard-Borel subprobabilities，全部 `{D_m}` evaluations 是
separating/injective：坐标全部相等当且仅当 kernels 相等。一个 finite labelled
kernel 由 immutable labels 与序列

```text
(K(D_m))_(m>=0)
```

编码。

### 4.2 Input/operator/output maps

Round 54 的 Borel collar kernel 给出

```text
C_in(a)
=(t54,chart,orientation,endpoints,ell,(E_a(D_m))_m).
```

在 `A_col` 外用一个显式 sentinel totalize；这不在那里读取 `K`。

finite compositions 与 C24 restrictions of Borel deterministic collision
kernels 仍是 Borel sub-Markov kernels。因此每个 `m` 上

```text
a -> K_word(a,D_m),
a -> (O_s^9148|C24)(a,D_m)
```

均 Borel。Round-54 labelled collar 在 fixed word 中保持单一 regular branch 且
保留 `omega`；故 output 可由 image chart/orientation/endpoints、rational
subinterval density integrals 与 immutable IDs 编码。这些坐标都是 kernel
evaluations，确定 density a.e.。next-input 使用同一个 `C_in` schema；不存在时用
同一个 sentinel。

于是 kernel equality 与 output/input equality 均是 countable coordinate
equalities 的交，Borel 性不再条件化。

### 4.3 精确结果

| bit | Borel | universal value |
|---|---|---|
| `L_id` | CERTIFIED | true |
| `L_word` | CERTIFIED | true |
| `L_input` | CERTIFIED | NOT_CERTIFIED |
| `L_C24` | CERTIFIED | NOT_CERTIFIED |
| `L_operator` | CERTIFIED | NOT_CERTIFIED |
| `L_output` | CERTIFIED | NOT_CERTIFIED |
| `L_horizon` | CERTIFIED | NOT_CERTIFIED |

令 `J_b` 为 block `b` 的七 bits 乘积，

```text
R(a)=sup{q>=0:J_0(a)=...=J_(q-1)(a)=1}.
```

则

```text
{R>=q}=intersection_(b<q){J_b=1},
{R=infinity}=intersection_(q>=1){R>=q},
```

所以 `R` Borel。`K` 是 Borel integer mark，因此 `{R>=r_K}` 也 Borel。

这只关闭 typing。一个 Borel record 仍可能：collar 太短而不满足 canonical input
threshold；中间 C24 bit 失败；两个 operator kernels 不相等；output 与 next input
不匹配；或 horizon 小于 `r_K`。所以

```text
all-seven value: 2 true / 5 open,
physical R>=r_K: NOT_CERTIFIED.
```

## 五、fixed-`j` positive hybrid 的精确升级

现在 `R` 的 Borel typing 与 actual `C_bad,j^bi` 均已构造，不再是 supplied
measurability hypotheses。在 fixed `j` 上定义

```text
C_hyb,j
=1_Acol [
   1_{R>=r_K} C_rec w_Z^r_K
  +1_{R<r_K} 2^(K+1)
 ]
 +1_(A_col^c) C_bad,j^bi.
```

registry guard 是强制的：先测试 `A_col`，只有在该 branch 内才能读取 `K,R`；
complement 只读取 RN density 与 immutable label。positivity/Tonelli 给出 exact
iff：`∫C_hyb,j<∞` 当且仅当 long、short 与 complement 三项均有限。

本轮已支付

```text
complement term: CERTIFIED_FINITE_AT_FIXED_J.
```

仍未支付

```text
long recovery term: NOT_CERTIFIED,
short raw debt term: NOT_CERTIFIED.
```

因此 full fixed-`j` policy 尚未认证 finite，更没有 all-insertion hybrid。

## 六、raw collar 与 explicit power-Orlicz 的同律等价

在同一个 `ν_j|A_col` 上写

```text
r_K=ceil(beta(K+1)),
Y=w_Z^r_K,
alpha_opt=beta log(w_Z)/log(2),
q_col=1/alpha_opt=log(2)/(beta log(w_Z)).
```

`q_col` 约为 `806`，严格大于 `1`。取

```text
Phi(t)=t^q_col.
```

它是 increasing convex superlinear Orlicz function。由

```text
beta(K+1)<=r_K<beta(K+1)+1
```

得到

```text
2^(K+1)
=(w_Z^(beta(K+1)))^q_col
<=Phi(w_Z^r_K)
<w_Z^q_col 2^(K+1).
```

故有 exact same-law iff

```text
Z_col=integral 2^(K+1)dnu_j<infinity
iff
integral Phi(Y)dnu_j<infinity.
```

任一边 finite 都蕴含 optimal clock moment `∫Y<∞`。反向不成立；clock moment 的
临界 clearance exponent 只有 `alpha_opt≈0.001240656316...`，raw collar 要求的
指数是 `1`。

截断 `K_N=min(K,N)` 有显式 finite bound

```text
integral Phi(w_Z^r_KN)dnu_j
<w_Z^q_col 2^(N+1)nu_j(A_col),
```

但该 bound 随 `N` 增长，没有 uniform limit。

依赖审计没有发现任何可以对齐的同律 finite `Z`：

- Round50 的 parent-`W` `Z_B` 不是 collar inverse-length debt；
- Round42 的 standard-family `Z` 不在 owner/root law 上；
- Round54 明确冻结 `Z_col` 为 uncontrolled；
- Round57/59 separators 允许 full `A_col`、`B=14`、所有 polynomial `K`
  moments finite 而 clock moment divergence；在该模型中 raw `Z_col` 与
  `Phi(Y)` moment 也发散。

所以本轮得到 explicit physical Orlicz criterion，但没有 physical Orlicz bound。

## 七、Jordan 与 all-time 正量的严格边界

本轮 `C_bad,j^f,C_bad,j^r` 是 Round52 orientation-positive cost pushforwards 的
RN densities。它们不是 Round54 的 `mu_plus,mu_minus`。没有 dependency 证明

```text
orientation forward/reverse = Jordan plus/minus.
```

对任何 nonnegative charge `a`，Jordan/common-mode identity 仍为

```text
integral a d(mu_plus+mu_minus)
=integral a d|J|+2 integral a d(mu_plus wedge mu_minus).
```

所以 all-time positive moment 精确等价于分别支付 weighted variation 与
weighted common mode。完整 cemetery 还要第三条独立 series：

```text
sum_j w_Z^j integral_(A_col^c) C_bad,j dnu_j<infinity.
```

现有 fixed-`j` bound 无 decay，三条 series 都不能由本轮求和。共同-mode、互斥
variation-mode separators 继续证明 signed cancellation 与 one-time finiteness 不足。

## 八、最新技术审计

本轮复核：

- `arXiv:2604.19671v2` 演化的是已经标准的 families，并依赖 survivor-mass
  normalization；它不把 arbitrarily thin owner trace 变成 uniformly proper
  collar，也不给 clearance tail；
- `arXiv:2606.19621v2` 的 inter-sign transport 不能把 signed cancellation 变成
  positive Jordan variation/common-mode moments。

未找到 owner/coarea-trace tangency-nullity、physical active-clearance tail、五个
suffix universal values、same-law all-time Jordan decay 或 strong positive
cemetery theorem。没有外部 theorem 导入 certificate dependency。

## 九、严格状态与 continuation

```text
actual fixed-j owner law nu_j:                         CERTIFIED
actual fixed-j A_col-complement submeasure:            CERTIFIED
physical complement value/nullity:                     NOT_CERTIFIED
physical A_col full coverage:                          NOT_CERTIFIED

fixed-j same-law complement mass anchor:               CERTIFIED
fixed-j same-law complement F10 RN anchor:             CERTIFIED
fixed-j labelled cemetery pushforward:                 CERTIFIED_CHARGE_PRESERVING
all-time complement positive anchor:                   NOT_CERTIFIED

all 7 suffix predicates Borel:                         CERTIFIED_7_OF_7
Borel R on A_col:                                      CERTIFIED
universal suffix values:                               2 true / 5 open
physical R>=r_K:                                       NOT_CERTIFIED

raw Z_col <-> explicit power-Orlicz:                   CERTIFIED_EXACT_IFF
physical active Abel / raw Z_col / Orlicz finite:      NOT_CERTIFIED

fixed-j orientation RN anchor:                         CERTIFIED
weighted Jordan variation/common mode:                 NOT_CERTIFIED
all-time positive assembly / strong cemetery:          NOT_CERTIFIED

Gate5 maturity / blocks:                               10/18 / 0
Gate5 / CM2:                                           NOT_CERTIFIED / NO-GO_FOR_CLAIM
```

最短 continuation 是：

1. 对 `N_cut,N_acc` 各 signature 直接估 owner-trace value/nullity；把 fixed-`j`
   RN anchors 升为具有 `w_Z^j` summable decay 的 deduplicated all-time law；
2. 直接证明 active Abel series，或给 finite raw `Z_col`/本轮显式
   `power-Orlicz` RHS；
3. 在 actual records 上逐条证明五个 missing universal values，并给
   `R>=r_K`；
4. 另行 pin Jordan source law 与 orientation law及其 charge preservation，分别
   支付 weighted variation、common mode 与 complement cemetery。

## 十、机验

配套 certificate/verifier 实施 strict JSON、Round-60 aggregate/leaf recursive
pins、独立 clock/Orlicz/F10 arithmetic、same-law RN typing、七位 code-map typing、
hybrid registry guard、deterministic replay、producer reemit、leaf-wise hostile
mutation rejection、SHA ledger 与默认 fail-closed exit `2`。
