# CM2 Gate 5 Round 55：synchronised pairing / delayed collar 严格前沿

日期：2026-07-20

## 结论先行

本叶新增三个可严格认证的推进，但不完成新的 Gate-5 字段：

1. Round 54 的 normalized-product coupling 是一个合法见证。对同一 Jordan 源点同时运行 hit/miss kernel，还可构造无选择定理的 source-synchronised coupling。两种 cost 不可全序；取二者最小值得到一个不劣于 Round 54、且有时严格更好的 signed bounded-Lipschitz 估计。
2. `A_col` 满 trace 质量、`{d=0}` 零质量、甚至只有一个解析横截交点，仍不推出 `Z_col<∞`。这里给出每个 dyadic level 恰好贡献 `2` 的显式反例。
3. 把 level `k` 的 collar 债务延迟 `k+1` 个相同的 Round-42 numerical C24 Growth block 后，其债务降到统一的 `O(m_k)`。聚合所需条件因此可从强矩
   `Σ 2^(k+1)m_k<∞`
   降为弱矩
   `Σ w_Z^(k+1)m_k<∞`，
   精确临界为 `alpha_*=log_2(w_Z)`。

仍缺 physical same-source rate、physical weak clearance moment、Round54 collar word 与 Round42 C24 operator 的 same-operator join，以及任意 `k` 所需的剩余 suffix horizon。因此状态严格保持：

```text
Gate5 maturity = 10/18
complete 18-field blocks = 0
complete composite gates = 0/5
CM2 = NO-GO_FOR_CLAIM
```

## 冻结输入

本叶只直接读取并 pin 两个冻结 manifest：

- Round 54 Gate 5 collar/pairing/BV frontier：
  `87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5`
- Round 42 numerical C24 Growth block：
  `86a63f3fa7b5b9cd7569bda0caf07d6e3637ba01eb0a3e2fdae9a9ba1c4a9db4`

Round 54 固定了 dyadic selector

```text
k(omega)=min{k>=0:2^(-k)<=min(1,d(omega))},
ell(omega)=2^(-(k(omega)+1)).
```

同时留下 `nu(A_col)` 和 `Z_col` 未知，并以 normalized product

```text
pi=(mu^+ tensor mu^-)/m
```

作为 canonical coupling。Round 42 固定了

```text
z_{r+1} <= gamma z_r + Z0 m_r,
gamma=(2000/1999)(1+48*9148)(900337/901685)^9148,
0.4999 < gamma < 1/2,
w_Z=(1+rho^(-1))/2,
rho=(111718729/111718750)^9148.
```

依赖的 hash、字段和上述精确算术在 cert 构建时重放；任一漂移均 fail closed。

## 一、同源同步 hit/miss coupling

### 1. 定理

在一个固定 immutable physical source record/rank 内，写 Jordan 分解

```text
lambda=lambda^+-lambda^-.
```

令 `H_x,M_x` 分别为同一源点 `x` 上的 hit/miss Borel Markov kernels，并令

```text
mu^+ = H lambda^+ + M lambda^-,
mu^- = M lambda^+ + H lambda^-.
```

定义

```text
pi_sync
 = integral H_x tensor M_x d lambda^+(x)
 + integral M_x tensor H_x d lambda^-(x).
```

则直接对 cylinder functions 积分可得

```text
(pr_1)_* pi_sync = mu^+,
(pr_2)_* pi_sync = mu^-,
mass(pi_sync) = |lambda|(source).
```

这是两个既定 Borel kernels 的 product 与 parameter integral，不涉及 measurable selection，也不会跨 source record 或 rank 配对。

对 `||phi||_BL=max(||phi||_∞,Lip(phi))`，

```text
|phi(y_H)-phi(y_M)|
 <= min(2,d(y_H,y_M)) ||phi||_BL.
```

因此

```text
||J_p||_(BL*) <= d_p^sync,
d_p^sync = integral min(2,d(y_H,y_M)) d pi_p^sync.
```

Round-54 product coupling 同时给出 `||J_p||_(BL*)<=d_p^product`。因此可安全合并为

```text
d_p^best=min(d_p^product,d_p^sync),
||J_p||_(BL*)<=d_p^best.
```

`d_p^best` 才是全局不劣于 Round-54 product witness 的 bound；本叶不宣称 `d_p^sync<=d_p^product`。

若 `H_x=delta_{h(x)}`、`M_x=delta_{m(x)}`，右端精确化为

```text
integral min(2,d(h(x),m(x))) d|lambda|(x).
```

这把下一步物理输入压缩成“同一源点的 hit/miss image separation”，无需控制无关源点之间的 product-support 直径。

### 2. product coupling 非尖锐反例

取 source `{0,1}`，`lambda=(delta_0+delta_1)/2`，target metric `d(0,1)=1`，并取 deterministic `H=M=identity`。则

```text
J=(H-M)lambda=0,
d_sync=0.
```

但 Round-54 normalized product 是 `lambda tensor lambda`，两个 off-diagonal 原子各质量 `1/4`，所以 product cost 恰为 `1/2`。

因此 Round-54 估计没有错，但其 product-support rate 不是必要条件；在这个模型里 synchronised witness 严格更好，且 `d_best=0`。

### 3. synchronised coupling 也可更差

仍取 source `{0,1}` 与均匀正律，但令 `H=identity`、`M=flip`，即 `M(0)=1,M(1)=0`。两个 image marginals 仍都是均匀律，故

```text
J=(H-M)lambda=0.
```

同源同步 pairing 总把 `x` 配到 `1-x`，所以

```text
d_sync=1.
```

normalized product 的 cost 仍为 `1/2`。因此 sync 与 product 不存在全局次序；此例中 `d_best=1/2`。

### 4. constant cancellation 仍不给 rate

对所有 `p` 取一个质量一的源原子，令 `h_p=0,m_p=1`。则

```text
J_p=delta_0-delta_1,
||J_p||_(BL*)=d_p^sync=1.
```

所以 equal mass 与 `J_p(1)=0` 不推出任何 `delta_sync<1`。只有实际物理估计

```text
d_p^sync <= C_sync delta_sync^p,
w_Z delta_sync < 1
```

才给

```text
sum_p w_Z^p ||J_p||_(BL*)
 <= C_sync/(1-w_Z delta_sync).
```

该 rate 本叶明确为 `NOT_CERTIFIED`；signed BL pairing 也不能支付 positive F10 或 cemetery mass。

## 二、解析横截满质量仍可有无限 `Z_col`

取 owner/root parameter `t in (-1,1)`，概率律 `nu=dt/2`。选定 anchor boundary `b_0(t)=0`，另一个解析 boundary 为

```text
b_1(t)=t.
```

二者只在 `t=0` 有一个横截交点，无 grazing 或 countable homogeneity accumulation。令 clearance

```text
d(t)=|t|.
```

于是

```text
A_col=(-1,1)\{0},
nu(A_col)=1,
nu({d=0})=0.
```

对 `k>=1`，Round-54 selector 的 level 是

```text
C_k={2^(-k)<=|t|<2^(-(k-1))}.
```

其质量与 collar length 分别是

```text
m_k=nu(C_k)=2^(-k),
ell_k=2^(-(k+1)).
```

故每层的 inverse-length debt 恰为

```text
m_k/ell_k=2,
Z_col=sum_(k>=1)2=infinity.
```

等价地，对 `0<|t|<1` 有

```text
|t|/4 < ell(t) <= |t|/2,
2/|t| <= ell(t)^(-1) < 4/|t|,
```

所以出现对数发散。

若所有 parent curve 长度为一、owner rank 固定为 `B=14`，则 parent debt 仍只有

```text
Z_parent=1,
Z_parent,B=2^14=16384.
```

因此以下三项都不足以安装 Round-53 proper trace bridge：

- `nu(A_col)>0`；
- `nu(A_col)=nu(total)`；
- clearance 的零集仅由有限个解析横截交点组成。

`A_col` 质量与 `Z_col` 必须分开验收。

## 三、dyadic debt-level delayed recovery

### 1. 条件定理

令

```text
C_k={omega:k(omega)=k},
nu_k=nu|C_k,
m_k=mass(nu_k).
```

Round-54 constant-density extension 在 level `k` 的初始债务是

```text
z_(k,0)=2^(k+1)m_k.
```

条件性地假设：

1. 实际 Round-54 labelled killed-word collar output 正是 Round-42 positive killed C24 operator `O_s^9148` 的合法输入；
2. owner ID 不丢失，不出现未登记 boundary cut；
3. level `k` 在 insertion 后还保留至少 `k+1` 个相容的 9148-collision blocks；
4. killing 下 `m_(k,r)<=m_k`。

逐次应用 Round-42 recurrence：

```text
z_(k,r+1)<=gamma z_(k,r)+Z0 m_(k,r)
```

得到

```text
z_(k,k+1)
 <= gamma^(k+1)2^(k+1)m_k
    + Z0(1-gamma^(k+1))/(1-gamma)m_k.
```

因为 `2 gamma<1`，

```text
z_(k,k+1)<C_rec m_k,
C_rec=1+Z0/(1-gamma).
```

这是真正的 layerwise debt contraction，但不是 one-step physical trace contraction。

### 2. 弱 clearance moment

把 level `k` 的 recovered payload 在第 `k+1` 个 block 发出，得到精确 ledger

```text
sum_k w_Z^(k+1) z_(k,k+1)
 < C_rec sum_k w_Z^(k+1)m_k.
```

所以只需

```text
M_col,w=sum_k w_Z^(k+1)m_k<infinity.
```

在上节横截模型中，`m_k=2^(-k)`，于是

```text
Z_col=infinity,
M_col,w=sum_(k>=1)w_Z^(k+1)2^(-k)
       =w_Z^2/(2-w_Z)<infinity.
```

这严格证明 delayed ledger 所需矩比即时 `Z_col` 弱。

### 3. clearance tail 与精确临界

若

```text
nu({0<d<t}) <= C_d t^alpha,  0<t<=1,
mass(nu)=M,
```

则 `k>=1` 时

```text
m_k<=C_d 2^(-alpha(k-1)).
```

因此

```text
M_col,w
 <= w_Z M + C_d w_Z^2/(1-w_Z 2^(-alpha))
```

只要

```text
w_Z 2^(-alpha)<1.
```

对 geometric dyadic tail，此条件也是必要条件，所以精确临界是

```text
alpha_*=log(w_Z)/log(2),
alpha>alpha_*.
```

100-digit audit 给出

```text
rho = 0.99828190933694809886411788853012533545331164619068555079775414287641294187073930...
w_Z = 1.0008605237894138765897146028349873755211408539187825640882461208404113331033567...
alpha_* = 0.0012409395510954121047151792824672764586084379169905547644177744147103665103379368...
```

并 pin rational bracket

```text
12409395510954121/10^19
 < alpha_*
 < 12409395510954122/10^19.
```

典型 codimension-one transverse tail `alpha=1` 远在临界之上；但“解析横截”本身若没有作用到同一个 physical trace law、同一 owner registry，并不能自动给该 tail estimate。

## 四、必须 fail close 的物理 joins

本叶的 delayed theorem 只在以下验收全部通过后才能接到 physical trace resolvent：

1. **same law / same ID**：tail `m_k` 必须来自实际 trace law，且 owner/event/side/word-cell ID 与 Round-54 collar 完全相同；不能用几何面积或另一 disintegration 代替。
2. **same operator**：`K_word` 必须逐字绑定到 Round-42 的 positive killed C24 `O_s^9148`；形式相似的 recurrence 不计。
3. **suffix horizon**：每个 level `k` 必须真的还有 `k+1` 个相容 blocks；固定有限 word 不自动满足。短 horizon 部分需要单独 ledger。
4. **mass monotonicity**：每层 killing 后必须保持 `m_(k,r)<=m_k`，且不得跨层复制质量。
5. **weak moment**：给出 exact same trace law 上的数值 tail 常数 `C_d,alpha`，并验证 `alpha>alpha_*`。
6. **post-recovery join**：recovered layer 还需进入同一 fixed norm/operator block；本叶只控制 emission ledger，不宣称完整 F10/F13/F17 或 cemetery。

任一项缺失时，`quantitative_trace_survivor_contraction` 与 `unconditional_trace_resolvent` 都保持 `NOT_CERTIFIED`。

## 五、最新 normal-trace 技术审计（不升格）

审计了 Christopher Irving：

- `arXiv:2503.09536v2`，*On the normal trace space of extended divergence-measure fields*；
- v2 日期 `2026-05-29`；
- <https://arxiv.org/abs/2503.09536v2>。

相关结果把 extended divergence-measure field 的 normal trace 放入 `AE(partial E)`（bounded-Lipschitz functions 的 predual）；对 locally uniformly quasiconvex、特别是 Lipschitz domains，normal-trace map 是 onto，并存在 bounded、未必 linear 的 right inverse；另有 `DM^1` analogue。

这为 Round-54 signed BV/current sublayer 提供了很自然的 fixed BL trace target，但不提供：

- positive Markov extension；
- linear right inverse；
- same-ID killed-word intertwining；
- billiard-specific numeric constants；
- physical source 的 divergence-measure membership；
- image-separation `rho` rate。

该论文因此只作为 bibliographic technology audit，不 vendored、不进入 hash dependency，也不给 Gate-5 field credit。

## 六、机验与 hostile acceptance

新增文件：

- `cm2_gate5_round55_synchronised_pairing_delayed_collar_cert.py`
- `cm2_gate5_round55_synchronised_pairing_delayed_collar_verifier.py`
- `cm2-gate5-round55-synchronised-pairing-delayed-collar-manifest-2026-07-20.json`
- 本报告
- 四文件 SHA ledger

verifier 分三层：

1. 在 `resolve()` 前拒绝 manifest leaf symlink，并逐项重查每个 dependency 的存在性、原路径非 symlink、同目录与 SHA；
2. 定理、反例、精确有理算术、strict nonpromotion 的直接语义重放；
3. deterministic producer replay。

验收命令：

```bash
python cm2_gate5_round55_synchronised_pairing_delayed_collar_cert.py --summary
python cm2_gate5_round55_synchronised_pairing_delayed_collar_verifier.py --integrity-only
python cm2_gate5_round55_synchronised_pairing_delayed_collar_verifier.py --replay
python cm2_gate5_round55_synchronised_pairing_delayed_collar_verifier.py --self-test
python cm2_gate5_round55_synchronised_pairing_delayed_collar_verifier.py --reemit
```

预期分别返回 `0`；hostile/self-test 为 `127/127`，其中包含 internal manifest symlink、missing dependency、dependency symlink、dependency SHA 漂移与跨目录 dependency name；reemit 必须 byte-identical。

默认入口仍 fail close：

```bash
python cm2_gate5_round55_synchronised_pairing_delayed_collar_cert.py
python cm2_gate5_round55_synchronised_pairing_delayed_collar_verifier.py
```

两者都必须返回 exit `2`；`2` 表示包有效但数学门未关闭，不是 verifier failure。解析、SHA、依赖、语义或 replay 失败返回 exit `1`。
