# CM2 Gate 5 Round 58：同 owner ledger、H/J join 与 positive transport 边界

日期：2026-07-20

## 结论先行

本叶把 Round 57 的条件接口尽可能接回现有 physical owner/root fields。真实
推进不是把某个发散风险改名为“有限”，而是明确构造出当前冻结字段上**确实
存在的同 law 对象**，并精确定位它距离 physical field 还差什么。

1. Round 50/54 已足以在实际 finite Borel owner/root law `nu` 上构造
   Borel、extended-valued 的 dyadic clearance ledger：

   ```text
   m_k=nu{a in A_col:K(a)=k},
   M_clock=sum_k w_Z^r_k m_k in [0,infinity].
   ```

   这不是抽象替代 law，而是实际 owner law 的 restriction，且有 exact Abel
   tail identity

   ```text
   M_clock
   =w_Z^r_0 nu(A_col)
    +sum_(j>=0)(w_Z^r_(j+1)-w_Z^r_j)nu{K>j}.
   ```

   所有 finite truncations 都有限并单调逼近它；但极限有限仍未认证。

2. Round 57 的 `D_a,A_a,g_a` 路线不能直接用 Round 54 的“constant collar
   density”物理化。Round 53 的 owner law 是“每个 parent `W` 取一个 root
   atom，再对 outer parent law 积分”，不是沿 collar coordinate 的密度。
   Round 54 的 `E_a` 是人为把 root atom 铺成 uniform collar；其 density 正是

   ```text
   D_ext(a)=ell(a)^(-1).
   ```

   因而聚合它得到

   ```text
   integral D_ext dnu
   =integral ell^-1 dnu
   =sum_k 2^(k+1)m_k
   =Z_col,
   ```

   正好是现有未闭的 raw collar debt，且比最优 weak moment 更强。把它当免费
   density 会循环论证。

3. 现有 frozen chain 能构造 `K` marginal，不能构造 physical
   clearance/horizon joint law。最小正确扩展是

   ```text
   H(a)=可用的连续 compatible 9148-collision blocks 数，
   J(a)=1 iff Round54 labelled word 正是 Round42 O_s^9148 chain，
   Lambda=(K,H,J)_#(nu|A_col).
   ```

   对“可恢复就恢复，否则支付 raw debt”的 canonical positive policy，exact
   criterion 是

   ```text
   Q_policy
   =integral 1_{J=1,H>=r_K} C_rec w_Z^r_K dnu
    +integral 1_{J=0 or H<r_K} 2^(K+1)dnu
   <infinity.
   ```

   Round 51 的“所有 finite regular suffixes registry”不是实际 sampled
   horizon；Round 54 的 `K_word` 与 Round 42 的 `O_s^9148` 也尚无 domain、
   killed-bit、owner/event/side/word-cell 和 output 全相等的 frozen statement。

4. 给出同一 physical marginal 的 sharp two-completion separator。只在
   `K=2n` 放质量 `m_n=2^(-(n+1))`，令 `B=14`、full `A_col`。两个 completion
   保持 owner/root、clearance、rank law 完全相同：

   ```text
   aligned completion: J=1, H=r_K,
   short completion:   J=0, H=0.
   ```

   因 `r_(2n)<=2n+1` 且 `w_Z^2/2<1`，aligned recovered moment 满足

   ```text
   sum_n m_n w_Z^r_(2n)
   <=(w_Z/2)/(1-w_Z^2/2)<infinity.
   ```

   而 short raw debt 为

   ```text
   sum_n m_n 2^(K+1)=sum_n 2^n=infinity.
   ```

   所以任何只读 frozen `K` marginal 的 theorem 都不可能推出 hybrid suffix；
   `H/J` joint law 是信息论上不可删除的字段。

5. signed OT 到 positive collar/cemetery 的边界也被闭成 exact identity。
   对任意 nonnegative Borel charge `a` 与任何 coupling `pi`，

   ```text
   integral [a(y+)+a(y-)] dpi
   =integral a dmu+ + integral a dmu-.
   ```

   这个 positive cost 与 coupling 无关，取 OT infimum 不会降低它。signed
   displacement 只能控制 `J=mu+-mu-`；若要转移 positive moment，至少还需一个
   已有限的 positive anchor moment 与 pointwise transport inequality。

   精确 separator 取

   ```text
   mu_n+=mu_n-=2^-n delta_(x_n),
   B_n=14,
   d_n=2^(-n^2).
   ```

   则每个 record 都有 `J_n=0`、`d_n^OT=0`，所有 signed weighted resolvents
   恒为零；可是每一 sign 的 positive optimal-clearance charge

   ```text
   sum_n 2^-n d_n^(-alpha_opt)
   =sum_n 2^(alpha_opt n^2-n)
   =infinity.
   ```

   把两边送到同一 cemetery-labelled atom，signed cemetery current 仍为零，
   positive total variation/weighted cemetery charge 仍发散。因此 signed OT
   不推出 positive F10，也不推出 strong cemetery。

严格状态保持：

```text
Gate5 maturity = 10/18
complete 18-field blocks = 0
complete composite gates = 0/5
CM2 = NO-GO_FOR_CLAIM
```

## 一、冻结链的逐叶字段审计

本叶 hash-pin Round 49--57 的完整 owner/collar/suffix chain 与 Round 42
numerical C24 block，共 `10` 个 manifest。

| leaf | 已有字段 | 对 owner clock 仍缺 |
|---|---|---|
| Round 49 | fixed-record typed measures；suffix-product nonimplication | joint insertion/suffix law |
| Round 50 | global standard-Borel owner-deduplicated root registry | finite all-depth aggregate |
| Round 51 | all finite regular suffix branch registry | selected compatible horizon 与 physical operator embedding |
| Round 52 | fixed-insertion constant-one source-rank `4^-b` tail | all-time sum；`B` 与 clearance `K` 比较 |
| Round 53 | root atom over outer parent law | along-collar AC density |
| Round 54 | Borel `A_col,d,K,ell,E/Tr` 与 immutable labels | `A_col` coverage；aggregate collar debt |
| Round 55 | conditional delayed recovery 与 exact required tags | same-operator join；compatible horizon |
| Round 56 | pointwise minimal `r_K` | same-law moment；post-recovery join |
| Round 57 | negative-moment equivalence；hybrid/OT frontier | physical finiteness；`H/J`；positive lift |
| Round 42 | exact `O_s^9148` Growth recurrence | Gate-5 collar domain 与全标签 equality |

一个需要明确冻结的类型边界是：Round 52 的 `B` 是 source incidence rank；
Round 54/56 的 `K` 是 full-word clearance dyadic level。旧文件没有
`K<=cB+C`、`B<=cK+C` 或任何 joint tail。固定 `B=14` 的 Round 57 separator
已证明二者不能靠字段名相似就合并。

## 二、实际 owner law 上的 extended ledger

Round 50 给出 standard-Borel global owner registry；Round 54 在其
collar-admissible restriction 上给出 Borel `d`、least dyadic selector `K` 和
`ell=2^(-(K+1))`。Round 56 的 `r_K` 是 integer-valued deterministic function，
故复合后仍 Borel。

因此无需 density、uniform complexity 或 countable atomic disintegration，
便能定义实际 law 的 pushforward

```text
kappa=K_#(nu|A_col),  m_k=kappa({k}).
```

这是真实升级：旧 frontier 不再只说“如果有一个 tail”；现在 tail measure
本身在 physical registry 上已经 well-typed。

### Exact Abel identity

令 `a_k=w_Z^r_k`。逐点有

```text
a_K=a_0+sum_(j=0)^(K-1)(a_(j+1)-a_j).
```

Tonelli 给出

```text
integral a_K dnu
=a_0 nu(A_col)
 +sum_(j>=0)(a_(j+1)-a_j)nu{K>j}.
```

这同时是必要充分判据，没有 `D/A/g` 的额外损失，也避免把 physical law
改成模型 Lebesgue law。但旧 manifest 没有 RHS tail 的可加 bound，故
`M_clock<infinity` 仍为 `NOT_CERTIFIED`。

### Coverage 与 moment 是独立门

`M_clock` 只在 `A_col` restriction 上定义 recovery 成本。完整 positive bridge
至少还要：

```text
nu(A_col^c)=0
```

或把 `A_col^c` 送入一个已认证的 strong positive cemetery。

两门逻辑独立：

- Round 57 separator 有 full `A_col`，但 `M_clock=infinity`；
- 若 `A_col` 为空，则 restricted `M_clock=0`，但全部 owner mass 未覆盖。

因此“restricted moment finite”不能替代 coverage，“full coverage”也不能替代
moment。

## 三、`D/A/g` 的正确物理 typing

Round 53 的实际 transverse owner trace 是

```text
nu(A)=integral 1_A(xi(W)) dlambda(W),
```

其中每个 parent `W` 上是一个 root atom。对完整 owner/root record 条件化后，
沿 collar coordinate 得到的是 Dirac root，不是 `dnu_a/dc<=D_a`。

若改用 Round 54 `E_a`，它确实在人工 collar 上产生 normalized Lebesgue
kernel，但其 density 是 `ell^-1`，聚合即 missing raw `Z_col`。因此这一选择
不会给出比 Round 57 negative moment 更弱的入口。

可合法的 conditional theorem 必须先建立一个较粗的 Borel chart base
`(b,lambda)` 和 genuine conditional kernel `nu_b(dc)`，再证明

```text
dnu_b/dc <= D_b,
Leb{dist(c,E_b)<epsilon} <= A_b epsilon^eta,
delta_b(c) >= g_b dist(c,E_b)^q,

C_pull
=integral D_b A_b g_b^(-eta/q) dlambda(b)
<infinity,

eta/q>alpha_opt.
```

于是

```text
nu{delta<t}<=C_pull t^(eta/q)
```

并关闭 `M_clock`。这个 kernelized 版本允许 continuous owner base，也保留完整
owner IDs；但以下四个字段均未冻结：

1. common coarsened chart/disintegration；
2. actual conditional absolute continuity；
3. full-word boundary Minkowski constants；
4. pullback-gap lower bound 与联合常数可积性。

## 四、`K/H/J` 是最小 positive policy carrier

只知道 `K` 无法判断某个 collar 是否真的能执行 recovery。还必须记录：

- `H`：insertion 后连续可执行的 exact 9148-collision blocks 数；
- `J`：Round 54 labelled word 是否逐标签等于 Round 42 operator chain。

这里“same operator”不只是两边都有形如

```text
Z(next)<=gamma Z+Z0 mass
```

的 scalar inequality。若一个 contraction 只定义在 disjoint tagged carrier，
它的 constants 完全相同，也不能作用于 collar payload。必须验证同一
restriction/owner/event/side/word-cell、同 killed bits、同 domain、同 output。

Round 54 已保留这些 labels，是未来 join 的必要基础；但 Round 42 manifest
没有把其 `O_s^9148` domain equality 接到该 label tuple。Round 51 的 suffix
registry 也只是“存在所有 finite branches”的标准 Borel catalog，不是 actual
law 上的 `H` selection 或 joint distribution。

two-completion separator 进一步证明，这不是证法技术问题，而是缺少真实信息：
保持全部旧 marginal 不变，只改变 `H/J` completion，就能让 policy ledger 一边
有限、一边发散。

## 五、signed transport 到 positive charge 的 exact 边界

Round 57 的 `d_OT` 是 signed BL route 的最优 scalar witness。它通过

```text
|phi(y+)-phi(y-)|
```

利用 cancellation；positive F10/cemetery 需要的却是

```text
a(y+)+a(y-).
```

对任意 coupling，后者积分等于两个 marginal moments 之和，所以不存在通过
“更好的 coupling”减少 positive debt 的余地。

一个可用但必须带 anchor 的 conditional transport lift 是：若某 coupling 上

```text
a(y+) <= C a(y-) + L c(y+,y-),
```

则

```text
integral a dmu+
<=C integral a dmu- + L integral c dpi.
```

这里仍需 `mu-` 的 positive `a`-moment 已有限。OT displacement 只能搬运一个
已有 positive bound，不能从 signed cancellation 创造它。

zero-OT separator 同时保留 full `A_col`、one other boundary、`B=14`、finite
parent `Z_B` 和所有 fixed rank moments，故直接命中 frozen fields；它不是
依靠 rank divergence 或 coverage failure 偷造的反例。

## 六、最新官方技术检索

2026-07-20 通过 `export.arxiv.org` 官方 API 重新检索：

- signed / unbalanced optimal transport；
- dispersing / Sinai billiards / standard families。

新命中的相关条目为：

- `arXiv:2606.19621v2`，*Regularity of the positional penalization function in
  inter-sign optimal transport on real measures*；API `updated` 时间为
  `2026-07-17T10:16:59Z`。

该文研究 matched Jordan masses 下 signed transport 的 feasibility、duality、
positional penalty regularity 与 governing equations。它不把 inter-sign
cancellation cost 变成 unbounded positive collar moment 或 strong cemetery
norm。现有 billiard review / small-hole linear-response sources也没有给出本题
owner-clearance `H/J` joint theorem。因此没有外部 theorem 被提升为 certificate
dependency。

## 七、严格状态与最短 continuation

```text
same-owner extended K ledger:                 CERTIFIED_BOREL_EXTENDED_VALUED
same-owner ledger finite:                     NOT_CERTIFIED
A_col full coverage:                          NOT_CERTIFIED
kernelised D/A/g route:                       CERTIFIED_CONDITIONAL
physical D/A/g joint constant:                NOT_CERTIFIED
minimal K/H/J policy:                         CERTIFIED_CONDITIONAL
physical H joint law:                         NOT_CERTIFIED
Round54/Round42 same-operator J:               NOT_CERTIFIED
physical short raw debt:                      NOT_CERTIFIED
K marginal => hybrid suffix:                  FALSE_BY_SEPARATOR
signed OT => positive F10:                    FALSE_BY_SEPARATOR
signed OT => strong cemetery:                 FALSE_BY_SEPARATOR

Gate5 maturity / complete blocks:             10/18 / 0
Gate5 / CM2:                                  NOT_CERTIFIED / NO-GO_FOR_CLAIM
```

下一步已经压缩为三个不可互相偷代的实物输入：

1. 直接估计 actual `K` tail 的 Abel series，或建立正确的 coarsened-kernel
   `D/A/g` ledger；同时证明 `A_col` coverage；
2. 在同一 owner registry 上加入 Borel `H` 与 exact operator-alignment `J`，
   验证 policy ledger 的 long/short 两个正积分；
3. 对 positive F10/cemetery 单独证明两 Jordan marginals 的 positive weighted
   moment，或提供一个已有 positive anchor moment 加 transport inequality。

signed OT 可以继续用于 signed BL/F13 route，但不再作为 positive tower 的候选
支付手段。

## 八、机验

本叶完成：

```text
syntax:                         2/2 PASS
dependency hash pins:          10/10 PASS
strict JSON:                   duplicate/NaN rejected
deterministic result replay:   PASS
hostile mutations:             97/97 rejected
manifest reemit:               byte-identical
SHA ledger:                    4/4 PASS
default cert/verifier:         exit 2 / exit 2
Gate5 maturity:                10/18
CM2:                           NO-GO_FOR_CLAIM
```

文件：

- `cm2_gate5_round58_owner_ledger_positive_transport_frontier_cert.py`；
- `cm2_gate5_round58_owner_ledger_positive_transport_frontier_verifier.py`；
- `cm2-gate5-round58-owner-ledger-positive-transport-frontier-manifest-2026-07-20.json`；
- 本报告及 SHA ledger。
