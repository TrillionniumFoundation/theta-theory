# CM2 Gate 5 Round 56：optimal collar recovery clock 严格前沿

日期：2026-07-20

## 结论先行

本叶沿 Round-55 collar debt 主线做了一个严格但不升字段的推进：不再只用
`gamma<1/2` 选择安全时钟 `r=k+1`，而是使用冻结的精确 numerical C24
收缩系数，求出逐层最短恢复时钟

```text
r_k=min{r>=0:gamma^r 2^(k+1)<=1}
   =ceil(beta(k+1)),
beta=log(2)/log(1/gamma)<1.
```

该时钟逐层最小，因此对任何递增 emission weight 也是逐层最便宜的合法
时钟。对几何 clearance tail `m_k=C 2^(-alpha k)`，所需临界指数从

```text
alpha_55=log_2(w_Z)
```

严格降到

```text
alpha_opt=beta log_2(w_Z)<alpha_55.
```

同时，本叶核了标准 inverse-square shell 的潜在 physical weak-clearance
路线：在同一 collar 坐标中，边界点 `x_k=k^-2` 的 `epsilon` 邻域只有
`O(epsilon^(2/3))` 长度。若实际同一 owner trace law 在该坐标中有统一
有界密度，且 full-word 其他边界数与 pullback gap 有统一控制，则
`alpha=2/3` 会远超所需临界值。

但冻结的 Round-54 输入只把 trace law 定型为可连续的任意有限 Borel
measure，并未给 collar-coordinate density；`d_other` 还同时包含 fixed word
中的所有 singularity、homogeneity、owner 与 hole boundary。全 owner-record
的统一 pullback gap 和额外边界复杂度也没有冻结。因此 `2/3` 只是一条
严格的条件路线，不能冒充 physical weak-clearance theorem。

严格状态保持：

```text
Gate5 maturity = 10/18
complete 18-field blocks = 0
complete composite gates = 0/5
CM2 = NO-GO_FOR_CLAIM
```

## 冻结输入

本叶 append-only pin 两个旧 manifest：

- Round 55 synchronised pairing / delayed collar：
  `ff54ad55f1e065ccf390f83a83cc6135aa22f0cabc7753fd700b38e05af1701c`；
- Round 54 collar pairing / directional BV：
  `87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5`。

Round 55 冻结了

```text
z_(k,0)=2^(k+1)m_k,
z_(k,r+1)<=gamma z_(k,r)+Z0 m_(k,r),
m_(k,r)<=m_k,

gamma=(2000/1999)(1+48*9148)(900337/901685)^9148,
0.4999<gamma<1/2.
```

Round 54 冻结了 `d_other` 的完整物理范围、任意有限 Borel owner/root law、
`A_col` 质量未知与 `Z_col` 未知。这些字段和 SHA 在 cert 构建时重放；任一
漂移都 fail closed。

## 一、精确最短恢复时钟

### 1. 逐层推导

对 level `k` 迭代 `r` 个相同的 compatible C24 blocks：

```text
z_(k,r)
 <=gamma^r 2^(k+1)m_k
   +Z0(1-gamma^r)/(1-gamma)m_k.
```

要把 inherited initial-debt term 降到不超过 `m_k`，充要条件是

```text
gamma^r 2^(k+1)<=1.
```

因为 `0<gamma<1`，最小整数解恰为

```text
r_k=ceil(beta(k+1)),
beta=log(2)/log(1/gamma).
```

于是

```text
z_(k,r_k)<=C_rec m_k,
C_rec=1+Z0/(1-gamma).
```

若另一时钟 `s_k` 也满足同一 inherited-debt 验收，则必有
`s_k>=r_k`。因此对任意 `w>1`，逐层都有

```text
w^(s_k)m_k>=w^(r_k)m_k.
```

这证明 `r_k` 不只是可行时钟，而是该验收标准下的 pointwise minimal
clock；没有把一个更短但不收缩的 schedule 偷换进 ledger。

### 2. 数值审计

120-digit replay 的前缀为

```text
gamma = 0.4999208855127157913660046706058806115637447433649505204197...
beta  = 0.9997717578875635395264334017740554984542370979858220580920...
```

并冻结 rational bracket

```text
9997717578875635395/10^19
 < beta <
9997717578875635396/10^19.
```

第一处真实节省发生在 `k=4381`：

```text
r_k=k+1,  0<=k<=4380,
r_4381=4381<4382.
```

若列出几个检查点：

| `k` | Round-55 `k+1` | optimal `r_k` | saved |
|---:|---:|---:|---:|
| 4380 | 4381 | 4381 | 0 |
| 4381 | 4382 | 4381 | 1 |
| 4382 | 4383 | 4382 | 1 |
| 8762 | 8763 | 8761 | 2 |
| 10000 | 10001 | 9999 | 2 |

每行都独立在 log 坐标重放

```text
gamma^r_k 2^(k+1)<=1
 <gamma^(r_k-1)2^(k+1).
```

## 二、严格改进的 clearance 临界指数

用 optimal clock 发出 recovered level，得到

```text
sum_k w_Z^r_k z_(k,r_k)
 <=C_rec sum_k w_Z^r_k m_k.
```

由 ceiling 的上下界

```text
w_Z^(beta(k+1))
 <=w_Z^r_k
 <w_Z^(beta(k+1)+1)
```

可知在几何模型

```text
m_k=C_m 2^(-alpha k)
```

中，optimal ledger 收敛当且仅当

```text
w_Z^beta 2^(-alpha)<1,
alpha>alpha_opt:=beta log_2(w_Z).
```

数值为

```text
alpha_opt
 =0.0012406563164308641348787500994058785435503487052788922737...

alpha_55
 =0.0012409395510954121047151792824672764586084379169905547644...
```

并 pin

```text
12406563164308641/10^19
 < alpha_opt <
12406563164308642/10^19.
```

这是严格改进，不是小数显示误差。取显式

```text
alpha=0.0012408=1551/1250000
```

则

```text
w_Z^beta 2^(-alpha)
 =0.9999999004061441201535075635... <1,

w_Z 2^(-alpha)
 =1.0000000967294530072455403459... >1.
```

所以该几何 tail 的 optimal-clock ledger 收敛，而 Round-55 `k+1`
geometric ledger 发散。临界等号 `alpha=alpha_opt` 时，下侧 ceiling
比较产生不衰减项，因此 sharpness 也已验收。

同一模型的原始 collar debt 满足

```text
sum_k 2^(k+1)m_k<infinity iff alpha>1.
```

故存在完整的严格区域

```text
alpha_opt<alpha<=1,
```

其中 raw collar debt 发散，但 optimal delayed emission moment 收敛。

## 三、有限 horizon 能控制 mass，不自动控制 debt

若只有 `H` 个 compatible blocks，可恢复的最大 level 是

```text
K_H=floor(H/beta-1),
r_k<=H iff k<=K_H.
```

例如：

| `H` | `K_H` | recovered level count |
|---:|---:|---:|
| 4380 | 4379 | 4380 |
| 4381 | 4381 | 4382 |
| 8761 | 8762 | 8763 |
| 10000 | 10001 | 10002 |

若 `m_k<=C_m2^(-alpha k)`、`alpha>0`，则未恢复质量有严格公式

```text
sum_(k>K_H)m_k
 <=C_m 2^(-alpha(K_H+1))/(1-2^(-alpha))
 =O(2^(-alpha H/beta)).
```

但未恢复 inverse-length debt 是

```text
sum_(k>K_H)2^(k+1)m_k.
```

只有 `alpha>1` 时它才有限并衰减。对几何模型中的
`0<alpha<=1`，每个有限 `H` 的该 tail 都是无限的。于是

```text
small unrecovered mass != small unrecovered Z/debt.
```

这条 separator 说明不能用有限 horizon 的 mass estimate 偷换
Round-55 尚缺的任意 level suffix/debt ledger。

## 四、inverse-square homogeneity shell 的 `2/3` 条件路线

在抽象同一 collar coordinate `c in [0,1]` 上，取边界点

```text
x_k=k^-2,  k>=1,
x_infinity=0.
```

相邻 gap 为

```text
Delta_k=x_k-x_(k+1)
       =(2k+1)/(k^2(k+1)^2)
       =Theta(k^-3).
```

对 `0<epsilon<=1`，令

```text
N=ceil(epsilon^(-1/3)).
```

前 `N` 个 boundary neighborhood 总长度至多 `2N epsilon`；其余所有
boundary 都落入 accumulating tail `[0,N^-2+epsilon]`。因此

```text
Leb{dist(c,{0,x_1,x_2,...})<epsilon}
 <=2N epsilon+N^-2+epsilon
 <=6 epsilon^(2/3).
```

若**同一个实际 owner trace law** 在此坐标中有密度上界 `D`，则

```text
nu{0<d<epsilon}<=6D epsilon^(2/3).
```

再有 `J` 个统一有限的其他 boundary points，只增加
`2JD epsilon`，所以 `2/3` 指数保持。因为

```text
2/3>alpha_55>alpha_opt,
```

这些 same-law hypotheses 若成立，会直接支付 weak-clearance moment。

### 为什么本轮不能 physical promotion

Round-54 的冻结字段逐字说明：

1. `nu_j` 只是 owner/root standard-Borel base 上的任意有限 Borel
   measure，可有连续或离散 disintegration；没有相对 collar coordinate
   的 `L^infinity` density；
2. `d_other` 取到 fixed word 内下一个其他 singularity、homogeneity、owner
   或 hole boundary，不只是模型中的 `x_k`；
3. 没有全 insertion time / 全 owner record 统一的 pullback gap
   bi-Lipschitz comparison；
4. 没有统一额外 boundary count `J`；
5. `nu(A_col)` 的正质量或满质量仍是 `NOT_CERTIFIED`。

因此本叶只认证

```text
inverse-square shell epsilon^(2/3) lemma: CERTIFIED_CONDITIONAL
physical same-law bounded density:         NOT_CERTIFIED
physical full-word boundary complexity:    NOT_CERTIFIED
physical weak clearance moment:            NOT_CERTIFIED
```

这既保留了最短可行路线，也拒绝把标准 shell 几何施加到另一条 law 上。

## 五、仍缺的核心 joins

即使未来关闭 physical weak-clearance moment，仍必须分别验收：

1. Round-54 labelled collar output 与 Round-42 positive killed C24
   `O_s^9148` 是同一个 operator、同一 owner/event/side/word-cell ID；
2. level `k` 确实有 `r_k` 个 compatible suffix blocks，或有可支付的
   short-horizon debt remainder；
3. killing 不跨层复制 mass；
4. recovered payload 进入同一 fixed physical operator/norm block；
5. signed pairing 仍需 physical same-source image rate；signed BL
   cancellation 不能支付 positive F10 或 cemetery；
6. F17 仍需 all-input physical directional-BV/current source bound、same-ID
   artificial-boundary cancellation 与真实 fixed-slot embedding。

任一缺失时，以下全部保持 `NOT_CERTIFIED`：

```text
quantitative trace-survivor contraction,
unconditional trace resolvent,
complete all-face F10,
strong F13,
F14/F15/F17/F18,
strong cemetery,
Gate 5.
```

## 六、机验与 hostile acceptance

新增 append-only 文件：

- `cm2_gate5_round56_optimal_collar_recovery_clock_frontier_cert.py`
- `cm2_gate5_round56_optimal_collar_recovery_clock_frontier_verifier.py`
- `cm2-gate5-round56-optimal-collar-recovery-clock-frontier-manifest-2026-07-20.json`
- 本报告
- 四文件 SHA ledger

verifier 验收：

1. unresolved manifest/dependency leaf 在 `resolve()` 前拒绝 symlink，并逐项
   重查本地 regular file、同目录和 SHA；
2. 独立重算 exact gamma、`rho,w_Z`、120-digit logs、rational brackets、
   `r_k/K_H` rows、shell cover rows 与所有 strict nonpromotion；
3. 在 log coordinate 验证 clock minimality，避免构造数亿 bit 的有理数幂；
4. deterministic producer replay 与 byte-identical re-emission；
5. hostile mutations `109/109` 全拒绝，包括 duplicate JSON key、
   `NaN/Infinity`、manifest/dependency symlink、missing dependency、SHA drift
   与跨目录 dependency name。

验收命令：

```bash
python cm2_gate5_round56_optimal_collar_recovery_clock_frontier_cert.py --summary
python cm2_gate5_round56_optimal_collar_recovery_clock_frontier_verifier.py --integrity-only
python cm2_gate5_round56_optimal_collar_recovery_clock_frontier_verifier.py --replay
python cm2_gate5_round56_optimal_collar_recovery_clock_frontier_verifier.py --self-test
python cm2_gate5_round56_optimal_collar_recovery_clock_frontier_verifier.py --reemit
```

上述显式验收均返回 `0`。默认入口继续 fail close：cert 与 verifier 都返回
exit `2`；`2` 表示包有效但数学门未关闭，解析/依赖/SHA/语义/replay 错误返回
exit `1`。

## 七、严格状态与下一步

本轮真实新增：

```text
exact-gamma pointwise minimal recovery clock: CERTIFIED
strictly improved sharp alpha_opt threshold:  CERTIFIED
finite-horizon mass/debt phase frontier:       CERTIFIED
inverse-square shell 2/3 tail lemma:            CERTIFIED_CONDITIONAL
```

未新增 Gate-5 global field：

```text
physical weak clearance law:                   NOT_CERTIFIED
Round54/Round42 same-operator join:             NOT_CERTIFIED
unbounded compatible suffix schedule:          NOT_CERTIFIED
physical same-source pairing rate:              NOT_CERTIFIED
complete F10/F13/F14/F15/F17/F18:               NOT_CERTIFIED
Gate5 maturity / complete blocks:               10/18 / 0
complete composite gates:                       0/5
CM2:                                            NO-GO_FOR_CLAIM
```

最短 continuation 是：在**同一个 owner trace law 和同一 full-word
registry** 上证明 collar-coordinate density、homogeneity pullback gap 与其他
boundary complexity，先关闭 `alpha>alpha_opt`；然后分别关闭 same-operator 和
`r_k` suffix schedule。若这些物理绑定做不到，应转回 same-source paired-image
rate 或 all-input vector-current F17，而不能给本叶虚增字段。
