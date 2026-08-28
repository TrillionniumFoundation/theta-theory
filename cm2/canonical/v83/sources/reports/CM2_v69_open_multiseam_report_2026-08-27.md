# CM2 v69：开放多 seam 非零 moving-singularity 双时间机制与完整 finite-DQ 闭合

**日期：** 2026-08-27  
**作用域：** `CM2_OPEN_FOUR_BRANCH_MOVING_SEAM_PINBALL_V69`  
**结果：** `PASS_OPEN_CLASS_NONZERO_MOVING_SEAM_CM2_AND_L1_DQ_V69`

---

## 0. 结论先行

v68 已经证明一个两支受控 pinball 模型上的非零 moving-singularity CM2，但它仍只解决一个特殊基点上的 derivative array。v69 对剩余的三个实质 blocker 做了全量推进：

1. 从两支单 seam 升级为 **四支、三条内部 seam 同时移动**的参数族；
2. 从单一基点估计升级为整个参数区间上的 **统一乘积 CM2**；
3. 从 derivative array 的绝对可和升级为 **完整 finite-difference 两时间阵列在 \(\ell^1(\mathbb N^2)\) 中收敛**；
4. 给出三条物理 moving seam 的 **same-occurrence saltus 分解**，与固定 coordinate cut atom 永久分型；
5. 重建 scoped D02-A/B/C 和八字段 actual U3 packet；
6. 用独立 standard-library verifier、28 项 hostile tests、双构建字节一致性和 fresh-extraction replay 全量复核。

严格终态为：

```yaml
ScopedOpenMultiSeamCM2:
  status: PASS
  actual_controlled_billiard_family: true
  ambient_open_admissible_parameter_interval: (-1/10, 1/5)
  uniform_proof_interval: [-1/40, 1/40]
  branch_count: 4
  moving_physical_seams: 3
  physical_seam_sides: 6
  source_nonzero_for_every_parameter: true
  product_two_time_bound: true
  absolute_double_sum: true
  uniform_full_l1_finite_DQ_array_convergence: true
  same_occurrence_saltus: true
  scoped_D02_unresolved: 0
  U3_fields: 8

SpecularDispersingSinaiCM2:
  status: NOT_CLAIMED

FullPhysicalTimeRoofResponse:
  status: NOT_CLAIMED

UniversalMovingScattererCM2:
  status: NOT_CLAIMED

ExternalPeerReview:
  status: NOT_PERFORMED

LocalExternalAuthorityCredit:
  value: 0
```

---

# 1. 显式开放参数 billiard family

在平坦 cylinder

\[
\mathcal Q=(\mathbb R/\mathbb Z)\times[0,1]
\]

上，底壁碰撞后将速度重置为竖直向上。顶壁按位置所属 branch，选择一个确定性 winding lift 并将粒子送往底壁。

定义四个 branch weights：

\[
\begin{aligned}
w_1(a)&=\frac1{10}+a, &
w_2(a)&=\frac15+2a,\\
w_3(a)&=\frac3{10}-a, &
w_4(a)&=\frac25-2a.
\end{aligned}
\]

它们恒满足

\[
\sum_{i=1}^4 w_i(a)=1.
\]

全部 weights 为正的开放参数区间是

\[
-\frac1{10}<a<\frac15.
\]

统一 theorem 在其内部紧子区间

\[
I=\left[-\frac1{40},\frac1{40}\right]
\]

上证明。

累积 seams 为

\[
s_1=\frac1{10}+a,
\qquad
s_2=\frac3{10}+3a,
\qquad
s_3=\frac35+2a.
\]

所以三条内部 seam 的速度分别为

\[
1,\,3,\,2,
\]

全部非零。

在第 \(i\) 支上：

\[
T_a(x)=\frac{x-s_{i-1}(a)}{w_i(a)}\pmod1.
\]

顶壁使用 winding offsets

```text
0, 2, 4, 6
```

来实现四条不同的 outgoing physical directions。每条 seam 的左极限 target lift 与右极限 target lift 相差一，因此反射律在物理方向上真实跳跃。

在 \(I\) 上：

\[
\min_{a,i}w_i(a)=\frac3{40},
\qquad
\rho:=\max_{a,i}w_i(a)=\frac9{20},
\]

从而

\[
\inf |T_a'|\ge\frac{20}{9}>1.
\]

---

# 2. 新工具一：固定 cut 上的 weighted-partition variation

定义 circular cut variation：

\[
\operatorname{Var}_{\mathbb T}(u)
=
\int_0^1|u'(x)|\,dx
+
|u(0+)-u(1-)|.
\]

定义 fixed-cut Sobolev scale：

\[
X_r=
\{u:u|_{(0,1)}\in W^{r,1}(0,1)\},
\]

\[
\|u\|_{X_r}
=
\|u\|_1
+
\sum_{j=0}^{r-1}
\operatorname{Var}_{\mathbb T}(u^{(j)}).
\]

令 \(Y=X_1=BV_{\rm cut}\)。

核心代数 lemma 是：若 \(b_i\ge0\)、\(b_*=\max b_i\)、\(V_i\ge|\Delta_i|\)，则

\[
\sum_i b_iV_i+
\left|\sum_i b_i\Delta_i\right|
\le
b_*
\left(
\sum_iV_i+
\left|\sum_i\Delta_i\right|
\right).
\]

它将每个 inverse branch 上的 interior variation 与输出 coordinate-cut jump 同时收费，并给出：

\[
\operatorname{Var}_{\mathbb T}
\left(
\sum_i b_i u(s_{i-1}+w_i y)
\right)
\le
(\max_i b_i)
\operatorname{Var}_{\mathbb T}(u).
\]

由于

\[
(\mathcal L_a h)^{(j)}
=
\sum_iw_i(a)^{j+1}
 h^{(j)}(s_{i-1}(a)+w_i(a)y),
\]

统一得到：

\[
\operatorname{Var}_{\mathbb T}((\mathcal L_a h)^{(j)})
\le
\rho^{j+1}
\operatorname{Var}_{\mathbb T}(h^{(j)}).
\]

若 \(h\) 中心化，则：

\[
\boxed{
\|Q_a^m h\|_{X_r}
\le
2\rho^m\|h\|_{X_r},
\quad r=2,3,
}
\]

以及

\[
\boxed{
\|Q_a^n u\|_Y
\le
2\rho^n\|u\|_Y.
}
\]

这条工具使 moving seams 不再迫使证明在每个参数后重建新的函数空间 cut。

---

# 3. 非零 moving-seam source

令 tangent 与累积 tangent 为

\[
v=(1,2,-1,-2),
\qquad
A=(0,1,3,2,0).
\]

设

\[
\psi_i^a(y)=s_{i-1}(a)+w_i(a)y,
\qquad
r_i(y)=A_{i-1}+v_i y.
\]

Perron operator 为

\[
(\mathcal L_a h)(y)
=
\sum_{i=1}^4w_i(a)h(\psi_i^a(y)).
\]

参数导数是

\[
\boxed{
(K_a h)(y)
=
\sum_{i=1}^4
\left[
 v_i h(\psi_i^a(y))
 +w_i(a)r_i(y)h'(\psi_i^a(y))
\right].
}
\]

所有 \(\mathcal L_a\) 保持 Lebesgue 质量，因此

\[
\Pi K_a=0.
\]

## 3.1 Same-occurrence saltus identity

令 \(J(u)=u(0+)-u(1-)\)。逐 branch 对齐同一 endpoint occurrence，得到：

\[
\begin{aligned}
J(K_ah)
={}&v_1h(0+)-v_4h(1-)\\
&+
\sum_{k=1}^3
\left[
(v_{k+1}-v_k)h(s_k)
+A_k(w_{k+1}-w_k)h'(s_k)
\right].
\end{aligned}
\]

第一行是固定 coordinate cut atom；第二行恰为三条 moving physical seams：

| seam | \(h(s_k)\) 系数 | \(h'(s_k)\) 系数 |
|---|---:|---:|
| \(s_1\) | \(1\) | \(1/10+a\) |
| \(s_2\) | \(-3\) | \(3/10-9a\) |
| \(s_3\) | \(-1\) | \(1/5-2a\) |

每条 atom 都与 D02-B 中的同一 seam、同一左右 branch 和同一 winding trace 绑定；禁止 selection 后重新 key。

## 3.2 全参数非零见证

定义 quintic step：

\[
H(t)=
\begin{cases}
0,&t\le0,\\
10t^3-15t^4+6t^5,&0<t<1,\\
1,&t\ge1.
\end{cases}
\]

取

\[
h_*(x)=
H(40(x-1/20))
H(40(3/20-x)).
\]

它在

\[
[3/40,1/8]
\]

上等于一，在 \((1/20,3/20)\) 外为零。对所有 \(a\in I\)，第一 seam 始终位于 plateau，而另外两条 seam 与 coordinate cut 都在 support 外。因此

\[
\boxed{J(K_a h_*)=1}
\]

对所有 \(a\in I\) 成立。

所以不是“基点 source 偶然非零”，而是：

\[
\boxed{K_a\ne0\quad\text{for every }a\in I.}
\]

---

# 4. 统一 source norm

精确系数 ledger 给出：

\[
\|K_ah\|_1
\le
\frac{40}{3}\|h\|_1
+4\operatorname{Var}_{\mathbb T}(h),
\]

以及

\[
\operatorname{Var}_{\mathbb T}(K_ah)
\le
8\|h\|_1
+
\frac{129}{10}
\operatorname{Var}_{\mathbb T}(h)
+
\frac{27}{10}
\operatorname{Var}_{\mathbb T}(h').
\]

因此

\[
\boxed{
\|K_ah\|_Y
\le
26\|h\|_{X_2}.
}
\]

显示系数的真实最大值是

\[
\frac{64}{3}<26.
\]

---

# 5. 新工具二：Two-scale regularity-loss CM2

设：

\[
\|Q^m g\|_{X_{\rm hi}}
\le
C_{\rm hi}\rho_{\rm hi}^m
\|g\|_{X_{\rm hi}},
\]

\[
\|Q^n u\|_{X_{\rm lo}}
\le
C_{\rm lo}\rho_{\rm lo}^n
\|u\|_{X_{\rm lo}},
\]

并有

\[
K:X_{\rm hi}\to X_{\rm lo},
\qquad
\Pi K=0.
\]

则：

\[
\boxed{
|\langle Q^nKQ^mg,f\rangle|
\le
C_{\rm lo}\|K\|C_{\rm hi}
\rho_{\rm lo}^n\rho_{\rm hi}^m
\|g\|_{X_{\rm hi}}
\|f\|_{X_{\rm lo}^*}.
}
\]

这个工具允许 source 损失一个 regularity scale；past 和 future 仍分别收费，因此不需要把加法型 bound 冒充双和可和。

在 v69 中取：

```text
X_hi = X2
X_lo = Y = BV_cut
C_hi = C_lo = 2
rho_hi = rho_lo = 9/20
||K_a|| <= 26
```

得到：

\[
\boxed{
|\langle Q_a^nK_aQ_a^mg,f\rangle|
\le
104
\left(\frac9{20}\right)^{m+n}
\|g\|_{X_2}\|f\|_\infty.
}
\]

完整双和：

\[
\boxed{
\sum_{m,n\ge0}
|\langle Q_a^nK_aQ_a^mg,f\rangle|
\le
\frac{41600}{121}
\|g\|_{X_2}\|f\|_\infty.
}
\]

这在整个 \(I\) 上统一成立。

---

# 6. 精确非零 matrix element

取

\[
g(x)=\cos(10\pi x).
\]

在 \(a=0\) 时：

\[
\begin{aligned}
K_0g(y)={}&
\cos(\pi y)-\pi y\sin(\pi y)\\
&-2\cos(2\pi y)+2\pi(2y+1)\sin(2\pi y)\\
&+\cos(3\pi y)-3\pi(y-3)\sin(3\pi y)\\
&-2\cos(4\pi y)+8\pi(y-1)\sin(4\pi y).
\end{aligned}
\]

它的 cyclic saltus 是

\[
4.
\]

独立 verifier 以标准库实现的 \(\mathbb Q(i)[\pi,\pi^{-1}]\) Laurent algebra 精确重算：

\[
\boxed{
\int_0^1(K_0g)^2dy
=
48\pi^2-rac{13506587}{88200}>0.
}
\]

因此 CM2 array 在

\[
(m,n)=(0,0)
\]

就有真实非零元素。

---

# 7. 新工具三：完整 finite-DQ 两时间阵列的 \(\ell^1\) 闭合

对任意 \(a,a+b\in I\)，定义

\[
D_{a,b}=rac{\mathcal L_{a+b}-\mathcal L_a}{b},
\]

\[
B_{a,b}(m,n)
=
\langle
 Q_{a+b}^nD_{a,b}Q_{a+b}^mg,
 f
\rangle,
\]

\[
B_a(m,n)
=
\langle
 Q_a^nK_aQ_a^mg,
 f
\rangle.
\]

再次对 source 求参数导数：

\[
\partial_aK_ah
=
\sum_i
\left[
2v_ir_i h'(\psi_i^a)
+w_ir_i^2h''(\psi_i^a)
\right].
\]

全区间系数 ledger 给出：

\[
\sup_a\|K_a\|_{X_3\to X_2}\le40,
\]

\[
\sup_a\|\partial_aK_a\|_{X_3\to Y}\le210,
\]

\[
\sup_a\|K_a\|_{Y\to L^1}\le14.
\]

从而：

\[
\sup_{a,a+b\in I}
\|D_{a,b}-K_a\|_{X_3\to Y}
\le105|b|,
\]

\[
\sup_{a,a+b\in I}
\|\mathcal L_{a+b}-\mathcal L_a\|_{X_3\to X_2}
\le40|b|,
\]

\[
\sup_{a,a+b\in I}
\|\mathcal L_{a+b}-\mathcal L_a\|_{Y\to L^1}
\le14|b|.
\]

又因为

\[
D_{a,b}
=
\int_0^1K_{a+tb}\,dt,
\]

所以

\[
\|D_{a,b}\|_{X_2\to Y}\le26.
\]

## 7.1 Finite-head convergence

对固定 \(M\)，用 telescoping 分解：

\[
Q_{a+b}^m-Q_a^m
=
\sum_{j=0}^{m-1}
Q_{a+b}^{m-1-j}
(Q_{a+b}-Q_a)
Q_a^j,
\]

并分别使用 \(X_3\to X_2\)、\(X_3\to Y\)、\(Y\to L^1\) 的 operator differences，得到：

\[
\sup_{\substack{a,a+b\in I\\m,n\le M}}
|B_{a,b}(m,n)-B_a(m,n)|
\to0.
\]

## 7.2 Uniform tail

有限差商阵列与 derivative 阵列都由同一个可和 array 控制：

\[
104
\left(\frac9{20}\right)^{m+n}
\|g\|_{X_3}\|f\|_\infty.
\]

先选 \(M\) 使 square 之外的共同 tail 小，再对有限 square 使用 finite-head convergence，得到：

\[
\boxed{
\sup_{a,a+b\in I}
\sum_{m,n\ge0}
|B_{a,b}(m,n)-B_a(m,n)|
\to0.
}
\]

这一步关闭了 v68 尚未覆盖的 moving-spike blocker：逐项收敛现在真正升级为完整双和的 \(\ell^1\) 收敛。

---

# 8. Scoped D02

## D02-A

四条实际 full branches：

```text
B1 B2 B3 B4
```

全部 unique owner、full target image、exact inverse、positive Jacobian 和 unresolved=0。

```yaml
D02A_rows: 4
D02A_unresolved: 0
```

## D02-B

三条 moving seams 各有 LEFT/RIGHT 两个物理 winding traces：

```yaml
moving_seams: 3
physical_sides: 6
post_terminal_rows: 0
unresolved: 0
```

每一 side 绑定同一 seam index、同一 adjacent branch 和同一 saltus source。

## D02-C

完整 prefix code：

```text
00 01 10 11
```

满足：

\[
4\cdot2^{-2}=1.
\]

四条 inverse branches 覆盖整个 target：

```yaml
parent_count: 1
formal_unresolved: 0
```

---

# 9. 八字段 actual U3 packet

八个独立哈希工件分别提供：

1. actual parameterized singular geometry/atlas；
2. actual nonzero source family；
3. orbit/cell totalization 与 Kraft；
4. source/target norm binding；
5. direct source estimate；
6. summable joint \((m,n)\) tail；
7. parameter modulus、seam compatibility 和 same-occurrence identity；
8. initial law 与 collision-map domain scope。

状态：

```text
ACTUAL_OPEN_CLASS_NONZERO_SOURCE_U3_PACKET_COMPLETE_V69
```

八个 field artifact digest 两两不同。

---

# 10. 验证结果

独立 verifier 不 import generator，且只使用 Python standard library。它重算：

- exact file set、modes、nlink、anti-symlink 和 manifest；
- canonical JSON、duplicate-key、nonfinite-number 和 self-hash；
- 四个 weights、开放 positivity interval、统一紧区间和 expansion；
- 三条 seams、六个 physical sides 和 exact saltus coefficients；
- source norm、strong-continuity、second-derivative 和 DQ constants；
- exact nonzero witness integral；
- D02-A/B/C；
- U3 distinctness 与 scope anti-escalation。

## 10.1 Hostile tests

本地 suite：

\[
\boxed{28/28\ \text{PASS}.}
\]

攻击覆盖：

```text
hidden file
symlink
manifest digest
branch image
seam velocity
seam saltus coefficient
zero-source replacement
source-norm underclaim
witness mutation
uniform-rate mutation
product/double-sum constant corruption
finite-DQ conclusion/remainder corruption
same-occurrence rekey
D02-A unresolved
D02-B post-terminal row
Kraft corruption
U3 aliasing
universal/specular/original-scope escalation
local credit escalation
parameter interval drift
noncanonical JSON
duplicate key
writable file
```

## 10.2 Dual build

两个独立 parent directories 中使用相同 output basename 重建；目录逐文件一致，deterministic gzip/tar 逐字节一致：

```text
PASS_DUAL_BUILD_BYTE_IDENTICAL_V69
```

## 10.3 Fresh extraction

从最终 data bundle tar 解压到空目录后：

```text
independent verifier: PASS
fresh hostile suite: 28/28 PASS
```

因此观察到的 validation gates 为：

```yaml
local_test_executions: 28
fresh_data_bundle_test_executions: 28
fresh_complete_release_test_executions: 28
data_bundle_dual_build_gate: 1
data_bundle_fresh_verifier_gate: 1
complete_release_dual_build_gate: 1
complete_release_manifest_gate: 1
complete_release_fresh_verifier_gate: 1
total_observed_validation_gates: 89
all_pass: true
```

---

# 11. 科学边界

| 命题 | 状态 |
|---|---|
| 实际 deterministic controlled pinball family | **PROVED** |
| 开放 admissible parameter interval | **PROVED** |
| 紧区间上 uniform four-branch theorem | **PROVED** |
| 三条 moving physical seams | **PROVED** |
| 每个参数处 source 非零 | **PROVED** |
| 非零 saltus 与非零 matrix element | **PROVED** |
| uniform product CM2 | **PROVED** |
| full \(\ell^1\) finite-DQ array convergence | **PROVED** |
| same-occurrence seam decomposition | **PROVED** |
| scoped D02/U3 | **CLOSED** |
| specular reflection | **NOT CLAIMED** |
| dispersing Sinai graph-current theorem | **NOT CLAIMED** |
| full physical-time roof response | **NOT CLAIMED** |
| universal moving-scatterer CM2 | **NOT CLAIMED** |
| external peer review | **NOT PERFORMED** |
| external authority credit | **0** |

因此，v69 内部不再存在 v68 后识别出的三个 blocker：

```text
single-base-only
single-seam-only
termwise-DQ-only
```

它们分别被：

```text
uniform open parameter class
three moving same-occurrence seams
full l1 finite-DQ closure
```

取代。

剩余的 specular dispersing-Sinai graph-current 与 full suspension response 是更强的 theorem scope，而不是 v69 已声明结果内部尚缺的证明步骤。
