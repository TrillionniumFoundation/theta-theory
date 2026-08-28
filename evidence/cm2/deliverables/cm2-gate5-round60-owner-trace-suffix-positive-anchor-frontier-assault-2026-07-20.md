# CM2 Gate 5 Round 60：owner-trace crosswalk、suffix predicates 与 positive hybrid frontier

日期：2026-07-20

## 结论先行

本叶没有把 collision-area 零测偷换成 singular owner-trace 零测，也没有把
Round 52 的 forward/reverse orientation 账本重命名成 Round 54 的 Jordan
`mu_plus/mu_minus`。严格状态仍为

```text
Gate 5 maturity = 10/18
complete 18-field blocks = 0
complete composite gates = 0/5
CM2 = NO-GO_FOR_CLAIM
```

本轮有四个真实的 Gate-5 子层推进。

第一，Round 50 与 Round 54 的 immutable owner token 已做成 exact Borel
projection：Round 54 只比 Round 50 多一个 `word-cell`，其余六个字段与 root
坐标无损保留。Round 25 的七类 transverse/isolated-root theorem 仍没有
curve-by-curve numeric root rows，也没有 Round-50 `event/primitive` tokens，所以
Round25→Round50 exact root-ID crosswalk 不能虚构。

第二，`A_col^c` 的物理障碍被按 owner signature 分层，并给出两条互不偷换的
路线：pure collar 路线需要 `nu(A_col^c)=0`；conditional hybrid 路线允许
complement 有正质量，但必须先提供 `A_col` 上的 Borel `R`，并在 `A_col^c` 上
用同一 owner law 的 measurable nonnegative positive trace/cemetery anchor 支付；
它绝不在那里读取未定义的 `K` 或 `R`。

第三，七个 suffix bits 的 predicate definitions 已全部 materialize。但只有
`L_id,L_word,L_C24,L_horizon` 的 Borel 性在冻结 registry 上无条件成立；
`L_input,L_operator,L_output` 仍缺共同的 canonical-input、kernel-evaluation 与
output-code Borel maps。因此 `R` 是 exact conditional Borel construction，不是
已完成的 physical recovery field。

第四，Round 52 确实支付了每个 fixed insertion time 的 orientation-positive
rank/F10 anchors，Round 54 也支付了每个 fixed marked Jordan pair 的 unweighted
mass。可是依赖链没有 pin

```text
abs(lambda_j) <= m_occ,j^owner
```

在同一 immutable law/charge 上，也没有证明所需 weighted charge 被 `H_j/M_j`
保持。因此 weighted Jordan-variation/common-mode anchors 仍未认证，complete
positive F10 与 strong cemetery 均不升格。

## 一、Round50→Round54 exact owner-token crosswalk

Round 50 的 candidate token 是

```text
t50=(restriction-id,time-j,physical-event-signature,
     primitive-key,connected-rank-0,side-label).
```

Round 54 的 same-ID token 是

```text
t54=(restriction-id,time-j,physical-event-signature,
     primitive-key,connected-rank-0,side-label,word-cell).
```

定义 `pi_50(t54)` 为只忘掉最后一个 `word-cell`。逐字段 crosswalk 为：

| position | Round 50 | Round 54 | action |
|---:|---|---|---|
| 0 | restriction-id | restriction-id | retain |
| 1 | time-j | time-j | retain |
| 2 | physical-event-signature | physical-event-signature | retain |
| 3 | primitive-key | primitive-key | retain |
| 4 | connected-rank-0 | connected-rank-0 | retain |
| 5 | side-label | side-label | retain |
| 6 | — | word-cell | forget under `pi_50` |

在固定 `word-cell` 内，lift `t50→t54` 是 injective。Round 54 的 joint labelled
carrier 还显式保留 `omega` 与完整 record label，所以两个物理 collar 的像即使
重叠也不会被误合并。由此得到

```text
Round50→Round54 same-ID crosswalk: CERTIFIED_EXACT_BOREL_PROJECTION.
```

这一步不能向前冒充 Round25→Round50 root-ID equality。Round 25 冻结的是：

- 七种 branch types；
- 每条 active branch 至多一个 isolated root；
- slope gap 严格大于 `50/9`；
- simultaneous branch roots coalesce；
- weak source-`r` ordering。

但该 manifest 同时明确

```text
curve_by_curve_numeric_root_sequence_materialized = false.
```

它没有给出 Round-50 physical-event signature、primitive key 或逐 root rows。
root theorem 与 immutable root-ID registry 是不同类型。

## 二、`A_col` coverage 的 exact trace frontier

Round 50 在 owner minimization 前已把 physical corners 与 simultaneous physical
events 送入 cemetery。对剩余 regular owner law，Round 54 的 designated anchor
face 从 `d_other` 中排除。因此可以精确写成

```text
A_col^c = N_cut union N_acc,
```

其中：

- `N_cut`：owner root 与另一个 nonphysical chart/homogeneity/hole cut 同坐标；
- `N_acc`：这些 other cuts 在 owner root 处积聚，典型位置是 grazing/tangency
  strata。

所以 pure collar full coverage 的 exact criterion 是

```text
nu(A_col^c)=nu(N_cut union N_acc)=0.
```

Round50→54 token crosswalk 排除了 ID 漂移，却不提供这个 trace-nullity。特别是
owner/root law 是 singular coarea/trace law；即使 grazing set 对二维 collision
area 为零，也不能推出它对 owner trace 为零。

一个 sharp frozen-field logical separator 是：保留一个 unique transverse
physical owner root 与完整 exact `t50/t54` crosswalk，把 owner-trace atom 放在一条
excluded homogeneity cut 上。该 artificial cut 不是第二个 physical event，所以
不触犯 Round 50 的 simultaneous-event cemetery rule；但 `d_other=0`，从而

```text
nu(A_col^c)=1.
```

这不是声称实际 billiard 实现了该原子 law；它严格证明当前字段不能推出
coverage。

按五类 physical event signature，实际 complement mass 均未冻结：

| owner stratum | possible complement mechanism | actual trace mass |
|---|---|---|
| source core clipping | endpoint/chart-cut coincidence | NOT_CERTIFIED |
| intermediate C24 preimage | homogeneity coincidence/accumulation | NOT_CERTIFIED |
| terminal C24 preimage | homogeneity coincidence/accumulation | NOT_CERTIFIED |
| collision singularity/owner change | tangency/grazing or owner-cut coincidence | NOT_CERTIFIED |
| moving occurrence | grazing/full-word boundary accumulation | NOT_CERTIFIED |

因此下一步不能把 full coverage 当作唯一合法物理路线。

## 三、`A_col + A_col^c` conditional exact positive hybrid iff

Round 59 的 pure collar policy 在 `A_col^c` 上赋 `infinity`，所以其有限性确实
强迫 full coverage。本轮增加不要求这个结论的最小 hybrid policy。

这个 accounting theorem 明确以两个尚未认证的接口为条件：

1. 三组 code-map interfaces 已补齐，使 `R` 在 `A_col` 上 Borel；
2. `C_bad` 是 `A_col^c` 上同一 owner law 的 measurable nonnegative charge。

在这些 supplied hypotheses 下，只在 `A_col` 上定义 `K,R`，并在 complement
上使用独立 typed `C_bad`，定义

```text
C_hyb
=1_Acol [
    1_{R>=r_K} C_rec w_Z^r_K
   +1_{R< r_K} 2^(K+1)
  ]
 +1_{A_col^c} C_bad.
```

这里先判断 registry branch，再读取字段；`A_col^c` 分支不扩张、不伪造、也不
比较 `K/R`。在上述两个 measurability hypotheses 下，由 positivity/Tonelli，
conditional exact iff 为

```text
integral C_hyb dnu < infinity
iff
  integral_{A_col,R>=r_K} C_rec w_Z^r_K dnu < infinity,
  integral_{A_col,R< r_K} 2^(K+1) dnu < infinity,
  integral_{A_col^c} C_bad dnu < infinity.
```

所以在两个 measurability interfaces 补齐后，`nu(A_col^c)>0` 本身不排除完整
hybrid theorem；真正必须补的是同一 owner law 上的 positive complement
anchor。其最小字段是：

1. immutable owner/event/side/word signature 与 Borel complement stratum；
2. 同一 stratum 的 positive trace 或 cemetery carrier；
3. nonnegative F10/cemetery charge `C_bad` 及有限积分；
4. 跨所有 insertion times 的 deduplicated positive assembly。

当前 `C_bad` integral 与 actual complement mass 都未认证。

## 四、active Abel / Orlicz audit

Round 59 的 exact active criterion 保持：

```text
Mbar<infinity
iff sum_{j in S} w_Z^r_j Fbar_j<infinity,
S={j:r_(j+1)=r_j+1}.
```

全量读取冻结 owner/root manifests 后，没有发现任何数值 `Fbar_j` rows、
summable envelope、explicit physical Orlicz function 或 finite raw `Z_col`。
因此 fixed-law de la Vallée-Poussin existence 仍不能当作 uniform bound。

最短 direct tail interface 是给出 active `j` 上的 `epsilon_j>=0`：

```text
Fbar_j <= epsilon_j w_Z^(-r_j),
sum_{j in S} epsilon_j < infinity.
```

另有一个可用但更强的冻结桥。由于

```text
1<w_Z<2,
r_K=ceil(beta(K+1))<=K+1,
ell(K)=2^(-(K+1)),
```

逐点有

```text
w_Z^r_K < 2^(K+1)=ell(K)^(-1).
```

所以

```text
Z_col=integral_{A_col}ell^(-1)dnu<infinity
```

会立即支付 optimal clock moment。遗憾的是 Round 54 正是把该 raw collar debt
标为未认证；不能倒过来宣布它有限。

## 五、七位 suffix predicate typing

本轮把七个 definitions 全部显式化：

| bit | exact predicate | frozen Borel status | universal value |
|---|---|---|---|
| `L_id` | immutable owner/event/side/word-cell equality | CERTIFIED | true |
| `L_word` | Round54 half-open killed-word intertwining | CERTIFIED | true |
| `L_input` | collar code lies in Round42 canonical input schema | CONDITIONAL on input code map | unknown |
| `L_C24` | 9148 intermediate bits equal C24 survivor bits | CERTIFIED predicate | unknown |
| `L_operator` | `K_word=O_s^9148|C24` on determining algebra | CONDITIONAL on both kernel evaluation maps | unknown |
| `L_output` | output carrier/density/IDs equal next input | CONDITIONAL on output/input code maps | unknown |
| `L_horizon` | record-length plus consecutive block/ID test | CERTIFIED predicate | unknown |

`L_operator` 的关键 red-team guard 是：对 countable determining algebra
`{A_m}`，kernel equality 的确可写成 countable intersection；但它只有在两边

```text
a -> K_word(a,b;A_m),
a -> O_s^9148(a,b;A_m)
```

都是 Borel evaluation maps 时才是 Borel predicate。Round 42/54 没有在同一个
code registry 上冻结这两个 maps。因此本叶不把该条件证明写成事实。

最小 code-map interface 为：

1. actual collar record 到 Round42 canonical-input 的 standard-Borel code map；
2. 上面两组 kernel evaluations 对所有 `m` 的 Borel 性；
3. output 与 next-input carrier/density/ID 的 Borel code maps。

一旦这三个接口补齐，令

```text
J_b=product of seven bits,
R(a)=sup{q>=0:J_0(a)=...=J_(q-1)(a)=1},  a in A_col.
```

则

```text
{R>=q}=intersection_{b<q}{J_b=1},
{R=infinity}=intersection_{q>=1}{R>=q},
```

从而 `R` Borel。当前严格状态是

```text
seven predicate definitions: CERTIFIED
unconditional Borel bits:     4/7
conditional Borel bits:       3/7
Borel R on A_col:              CONDITIONAL_SCHEMA
all seven bits true:           NOT_CERTIFIED
R>=r_K physical bound:         NOT_CERTIFIED
```

## 六、positive anchors 的第二次类型红队

Round 52 对每个 fixed insertion time `j`，在所有 finite regular owner-selected
records 的 disjoint marked union 上认证：

```text
integral 2^B                       < 23253221519103/880000,
forward orientation F10 charge    < 395304765824751/220000,
reverse orientation F10 charge    < 162772550633721/176000,
bidirectional orientation charge  < 2395081816467609/880000.
```

并且 exact arithmetic 为

```text
395304765824751/220000
+162772550633721/176000
=2395081816467609/880000.
```

这些是实际 positive orientation anchors，不能抹掉。

但 Round 54 的 Jordan pair 是另一种 typed construction：把 physical signed
source flux 写成

```text
lambda=lambda_plus-lambda_minus,
mu_plus =H lambda_plus+M lambda_minus,
mu_minus=M lambda_plus+H lambda_minus.
```

它冻结的是

```text
mu_plus(total)=mu_minus(total)=abs(lambda)(source)<=8064/5,
```

即 fixed marked pair 的 unweighted `a=1` positive anchor。Round51/52 的
`m_occ` rank/F10 orientation law 没有被依赖字段精确 pin 成 `abs(lambda)`，而且
`2^B` 只被明确标为 envelope，不等于 `sigma_e`。所以不能推出

```text
integral 2^B dmu_plus < infinity,
integral 2^B dmu_minus < infinity,
```

更不能把 forward/reverse 两个方向直接叫作 Jordan `mu_plus/mu_minus`。

把 fixed-j orientation anchors 合法搬到 weighted Jordan/common-mode 的最短
接口是同时证明：

```text
abs(lambda_j) <= m_occ,j^owner
```

在同一个 immutable owner law 上成立，以及目标 charge 被 `H_j/M_j` 保持并受
冻结 orientation F10 charge 支配。

即使补齐这个 fixed-j join，全时 sum 仍缺。现有 bound 对 `j` 是 uniform、没有
decay；对 `w_Z>1` 不能求和。两个 exact logical nonjoin 分别是：

- common mode：每个 `j` 取 `mu_plus=mu_minus`，则 `J_j=0`，但
  `sum_j w_Z^j lambda_j=infinity`；
- variation mode：每个 `j` 取等质量互斥 marginals，则 `lambda_j=0`，但
  `sum_j w_Z^j abs(J_j)=infinity`。

因此全局最短 positive interface 仍是 summable all-insertion owner charge，或

```text
A_j <= C kappa^j,
w_Z*kappa<1,
```

并另行纳入 excluded/cemetery records。

## 七、最新技术审计

最新 official/arXiv 检索没有找到 actual owner-trace clearance tail/nullity、
七位 physical suffix equality、all-time positive owner anchor 或 strong cemetery
定理。

- `arXiv:2606.10155v1` 的 dispersing-billiard transfer-operator review 没有给出
  本任务的 owner/collar code maps 与 quantitative trace tail；
- `arXiv:2606.19621v2` 研究 inter-sign optimal transport regularity，不能把
  signed cancellation 转成 positive Jordan variation/common-mode moments。

没有外部 theorem 导入 certificate dependency。

## 八、严格边界与 continuation

```text
Round50→54 owner-token crosswalk:             CERTIFIED
Round25→50 exact root-ID crosswalk:            NOT_MATERIALIZED

physical A_col full coverage:                  NOT_CERTIFIED
exact A_col/complement positive hybrid iff:    CERTIFIED_CONDITIONAL
physical complement positive anchor:           NOT_CERTIFIED
physical active Abel / Orlicz bound:            NOT_CERTIFIED

seven suffix predicate definitions:            CERTIFIED
all seven predicates Borel on frozen registry: NOT_CERTIFIED (4 true, 3 conditional)
Borel R on A_col:                               CONDITIONAL_SCHEMA
physical all-seven join / R>=r_K:               NOT_CERTIFIED

fixed-j orientation-positive rank/F10 anchors: CERTIFIED
fixed marked unweighted Jordan mass anchor:     CERTIFIED
fixed-j weighted Jordan/common-mode anchors:    NOT_CERTIFIED
global weighted Jordan/common-mode anchors:     NOT_CERTIFIED
complete positive F10 / strong cemetery:        NOT_CERTIFIED

Gate5 maturity / blocks:                        10/18 / 0
Gate5 / CM2:                                    NOT_CERTIFIED / NO-GO_FOR_CLAIM
```

下一条最短路线是：

1. 按 physical event signature 实测 `A_col^c` owner-trace mass；对非零 strata
   直接构造 `C_bad` positive trace/cemetery anchor，而非强迫 full coverage；
2. 提供 active Abel summable envelope，或 finite raw `Z_col`/explicit physical
   Orlicz bound；
3. 补齐 canonical-input、两 kernel evaluation 与 output/input 三组 Borel code
   maps，再证明五个 missing bit 在 actual records 上为真及 `R>=r_K`；
4. pin `abs(lambda_j)` 到同一 owner-selected coarea law 与同一 charge，随后补
   all-insertion decay，分别支付 weighted Jordan variation、common mode 与
   complement cemetery。

## 九、机验

本叶配套 certificate/verifier 实施：strict JSON、append-only dependency hash
pins、independent constant/clock/F10 arithmetic、token projection replay、raw
collar domination、suffix/R sample replay、hybrid typing、deterministic result
replay、byte-identical reemit、hostile leaf mutation rejection、SHA ledger，以及
默认 fail-closed exit `2`。最终计数写入冻结 SHA sidecar。
