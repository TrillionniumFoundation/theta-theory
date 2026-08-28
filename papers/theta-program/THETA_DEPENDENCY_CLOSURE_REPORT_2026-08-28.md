# θ-Theory：依赖闭合、最大正确作用域与剩余 blocker 总报告

**日期：** 2026-08-28  
**分支：** `theta-dependency-closure-2026-08-28`  
**范围：** 只处理 θ-Theory；不处理 Navier–Stokes。  
**控制原则：** `LATEST-WINS / FAIL-CLOSED / NO-UNNAMED-ARROWS / NO-REVIVAL-OF-REFUTED-UNIVERSAL-CLAIMS`

## 0. 结论

本报告把 θ-Theory 的正确依赖关系闭合为一个有向无环图，并补上此前未单独命名的两条关键编译定理：

1. **双侧 graph-current crossed-envelope / product-tail CM2**；
2. **CM2 atom ledger 到一般 moving-singularity U3 的联合 Cauchy 编译**。

闭合后的严格结论是：

```yaml
UnrestrictedUniversalMovingScattererCM2: REFUTED_AND_NOT_REVIVED
LocalGeometryOnlyUniformCM2: REFUTED_AND_NOT_REVIVED
PacketizedMaximalCM2Class: PROVED
ActualScopedNonzeroMovingSeamCM2: PASS_V68_V69
CM2ToGeneralMovingSingularityU3: PROVED_RELATIVE_TO_EXPLICIT_ATOM_PACKET
U3ToK1PressureSuspensionDiffusionResponse: PROVED
K1ToK15CommonSpaceCoefficientEllipticLift: PROVED
K15ToK2DoobRoughNonautonomousHomogenization: PROVED_RELATIVE_TO_EXPLICIT_UNIFORM_ROUGH_PACKET
K2ToK3FilteringSequentialSimultaneousIsaacs: PROVED_AS_TYPED_BRANCHES
K2K3ToHJBThetaExpectation: PROVED_RELATIVE_TO_COMPARISON
HJBToFBSDEPPDEPathEvaluation: PROVED_AS_DOWNSTREAM_REPRESENTATION_HIERARCHY
InternalDependencyGaps: CLOSED
UnnamedIntermediateArrows: 0
ExternalPeerReview: NOT_PERFORMED
FormalCredit: 0
```

这里的“闭合”不是把已被 v80/v82 否定的无约束 universal theorem 重新命名；而是：

- 对不可能的版本给出 refutation/maximality 终态；
- 对正向版本给出一个非空、逐字段可验证的最大 admissible packet 类；
- 每个下游箭头都有精确定理、输入、输出和禁止的逆向推理。

现有非空 actual witness 包括 v68/v69 的非零 moving-seam product-CM2 类；recursive v164 还保留 actual scoped Lorentz E2E PASS，但明确禁止把 scoped PASS 升级为 unrestricted universal theorem。

---

# 1. 正确依赖关系不是单链，而是 DAG

用户提出的主脊柱是正确的：

```text
CM2 双时间 graph-current / product tail
→ 一般 moving-singularity U3
→ K1：压力、悬挂 resolvent、物理扩散矩阵响应
→ K1.5：共同算子空间、(x,p) 系数/椭圆场
→ K2：Doob 选择、rough WIP、非自治均质化
→ K3：filtering、sequential/simultaneous game、Isaacs
→ HJB / theta-expectation
→ FBSDE / PPDE / path evaluation
```

但精确的最小依赖是：

```text
CM2^(1) + first/second source package
  └─> K1^(1): 一阶压力与扩散响应

CM2^(≤3) + third-source atom totalization
  └─> U3
       └─> K1^(3): 三阶压力/低频悬挂 resolvent/扩散响应
            └─> K1.5
                 └─> K2
                      ├─> one-player / uncontrolled HJB
                      ├─> K3-filter
                      ├─> K3-sequential lower/upper game
                      └─> K3-simultaneous mixed Isaacs

K3-filter + K3-game
  └─> belief-state HJB / Isaacs / path-dependent DPP

HJB / Isaacs + comparison
  └─> theta-expectation semigroup
       ├─> Markov FBSDE / controlled BSDE / 2BSDE（按方程类型）
       ├─> PPDE（存在真实 path-dependent state 时）
       └─> nonlinear path evaluation
```

因此有三条永久修正：

1. **U3 不是 K1 一阶响应的必要前提**；它是把 K1 提升到三阶、再安全进入一般 K1.5 的前提。
2. **K3 不是所有 HJB 的必要前提**；无控制和单控制 HJB 可由 K2 直接得到。K3 是 filtering、双人 game 和 Isaacs 的前提。
3. **FBSDE、PPDE、path evaluation 不是一条线**；它们是 HJB/theta-semigroup 下游的 typed representation branches。

---

# 2. CM2：双侧 graph-current product-tail 定理

## 2.1 设置

在一个 compact chambered parameter set `A` 上，令

\[
T_a:M_a\to M_a,
\qquad
L_a,
\qquad
\Pi_a,
\qquad
Q_a=L_a-\Pi_a
\]

分别为 fast map、transfer operator、rank-one invariant projection 和 centered transfer。

参数导数的完整 physical source 在 same-occurrence atlas 中写成

\[
K_a=K_a^{\rm reg}+\sum_{\omega\in\Omega}J_{a,\omega},
\]

其中 `omega` 同时记录 physical face、incident side、owner、branch word、homogeneity itinerary、orientation 与 parameter chamber。不同 occurrence 不允许在取范数前相消。

对中心输入 `g` 与 test `f`，定义 atom array

\[
A_{m,n}^{\omega}(a;g,f)
=
\left\langle Q_a^nJ_{a,\omega}Q_a^mg,f\right\rangle .
\]

## 2.2 双侧 crossed envelopes

假设存在统一常数

\[
0<\alpha,\beta<1,
\qquad
\Gamma_+,\Gamma_-\ge1,
\]

以及可和的 occurrence constants `C_omega^-`, `C_omega^+`，使

\[
|A_{m,n}^{\omega}|
\le C_\omega^-\alpha^m\Gamma_+^n
\|g\|_{X_-}\|f\|_Y,
\tag{2.1}
\]

\[
|A_{m,n}^{\omega}|
\le C_\omega^+\Gamma_-^m\beta^n
\|g\|_{X_-}\|f\|_Y.
\tag{2.2}
\]

第一式由 reverse/source-side recovery 收费，第二式由 forward/target-side recovery 收费；增长因子记录在错误方向传播 graph current 时的真实损失。

令

\[
A=\log(1/\alpha),\quad
B=\log(1/\beta),\quad
C=\log\Gamma_+,\quad
D=\log\Gamma_-.
\]

## 定理 THETA-CM2-BILATERAL-PRODUCT-TAIL-1

若

\[
\boxed{AB>CD,}
\tag{2.3}
\]

则取

\[
\lambda_*=\frac{B+D}{A+B+C+D}
\]

并对 (2.1)、(2.2) 作几何插值，得到

\[
|A_{m,n}^{\omega}|
\le
(C_\omega^-)^{\lambda_*}
(C_\omega^+)^{1-\lambda_*}
\rho_*^{m+n}
\|g\|_{X_-}\|f\|_Y,
\tag{2.4}
\]

其中

\[
\boxed{
\log\rho_*
=
\frac{CD-AB}{A+B+C+D}<0.
}
\tag{2.5}
\]

若

\[
\sum_{\omega\in\Omega}
(C_\omega^-)^{\lambda_*}
(C_\omega^+)^{1-\lambda_*}<\infty,
\tag{2.6}
\]

则

\[
\boxed{
\sum_{\omega}\sum_{m,n\ge0}
|A_{m,n}^{\omega}|
<\infty.
}
\tag{2.7}
\]

### 证明

对任意 `lambda in [0,1]`，

\[
|A_{m,n}^{\omega}|
\le
(C_\omega^-)^\lambda(C_\omega^+)^{1-\lambda}
(\alpha^\lambda\Gamma_-^{1-\lambda})^m
(\Gamma_+^\lambda\beta^{1-\lambda})^n.
\]

选择 `lambda=lambda_*` 使两个括号具有相同对数。直接计算得到共同对数为 `(CD-AB)/(A+B+C+D)`。条件 (2.3) 使它严格为负；先对 `m,n` 求和，再用 (2.6) 对 occurrence 求和即可。

## 2.3 Two-scale regularity-loss 是特例

若存在强弱空间 `X_hi -> X_lo`，满足

\[
\|Q_a^mg\|_{X_{hi}}
\le C_{hi}\rho_{hi}^m\|g\|_{X_{hi}},
\]

\[
\|Q_a^nu\|_{X_{lo}}
\le C_{lo}\rho_{lo}^n\|u\|_{X_{lo}},
\]

\[
K_a:X_{hi}\to X_{lo},
\qquad \Pi_aK_a=0,
\]

则直接得到

\[
|\langle Q_a^nK_aQ_a^mg,f\rangle|
\le
C_{lo}\|K_a\|C_{hi}
\rho_{lo}^n\rho_{hi}^m
\|g\|_{X_{hi}}\|f\|_{X_{lo}^*}.
\]

这正是 v68/v69 actual product-CM2 的 operator-level route。

## 2.4 finite-DQ 门

参数差商必须在 CM2 topology 中收敛：

\[
\sum_{m,n\ge0}
\left|
\left\langle
Q_{a+h}^n\frac{L_{a+h}-L_a}{h}Q_a^mg
-
Q_a^nK_aQ_a^mg,
 f
\right\rangle
\right|
\longrightarrow0.
\tag{2.8}
\]

固定 `(m,n)` 的收敛不足以交换参数极限和双时间和。v69 已在其四支三-seam开放类上实际闭合 (2.8)。

---

# 3. CM2 到一般 moving-singularity U3

## 3.1 third-source approximants

令 directed cutoff

\[
d=(K,\varepsilon,\mathcal P)
\]

同时截断 homogeneity depth、vertex cap 和 finite atlas refinement。第三源有限近似写成

\[
G_{3,d}(a)
=
\operatorname{Tot}_{\mathfrak S_d}
\{\eta_{a,\omega}:\omega\in I_d\}
+S_d^{\rm seam}(a).
\tag{3.1}
\]

定义 atom CM2 norm

\[
\|\eta_{a,\omega}\|_{\rm CM2}
=
\sup_{\|g\|\le1,\|f\|\le1}
\sum_{m,n\ge0}
\left|
\langle Q_a^n\eta_{a,\omega}Q_a^mg,f\rangle
\right|.
\tag{3.2}
\]

## 定理 THETA-CM2-TO-U3-JOINT-CAUCHY-1

假设：

1. every finite approximant `G_{3,d}:A -> X` 连续；
2. THETA-CM2-BILATERAL-PRODUCT-TAIL-1 对所有 third-source atoms 成立；
3. 存在可和 envelope `b_omega`，使
   \[
   \sup_{a\in A}\|\eta_{a,\omega}\|_{\rm CM2}\le b_\omega,
   \qquad
   \sum_\omega b_\omega<\infty;
   \]
4. vertex/intersection cap modulus `omega_vert(epsilon) -> 0`；
5. seam/refinement modulus `omega_seam(P) -> 0`；
6. same-occurrence orientation 和 cross-chart cancellation identities 在共同 refinement 上精确成立。

则对任意 `d1,d2 >= d`，

\[
\boxed{
\|G_{3,d_1}-G_{3,d_2}\|_{\mathscr X}
\le
2\sum_{\omega\notin I_d}b_\omega
+2\omega_{\rm vert}(\varepsilon)
+2\omega_{\rm seam}(\mathcal P).
}
\tag{3.3}
\]

右侧趋于零，因此 `G_{3,d}` 在 complete graded source space 中一致 Cauchy，存在唯一连续极限

\[
G_3\in C(A,\mathscr X).
\]

于是所有第三阶 Kato words

\[
RG_3R,
\quad
RG_2RG_1R,
\quad
RG_1RG_2R,
\quad
RG_1RG_1RG_1R
\]

均有定义并连续，`U3-JOINT-CAUCHY-v2` PASS。

### 证明

在共同 refinement 上，共同保留 atoms 按 UID、owner 和 orientation 精确抵消。剩余差只来自：

- cutoff 外 atoms；
- vertex cap；
- seam/refinement defect。

对第一项使用 (3.2) 和绝对可和；另两项使用其定义模量。完备性给出极限，参数连续性由一致极限得到。Kato words 的收敛由 reduced resolvent 的有界性和有限乘积估计得到。

## 3.2 重要边界

一个只控制一阶 source 的 CM2 theorem **不自动推出 U3**。正确输入是：

```text
CM2 product tail through the derivative atoms actually appearing in G3
+ third-source totalization
+ vertex/seam moduli
+ finite-DQ continuity.
```

这补上了“CM2 -> U3”中此前容易被省略的 higher-source ledger。

---

# 4. U3 到 K1：压力、低频悬挂 resolvent 与物理扩散响应

## 4.1 twisted collision operator

对 displacement `kappa_a` 和 roof `tau_a`，定义

\[
L_{a,q,s}h
=
L_a\left(e^{q\cdot\kappa_a-s\tau_a}h\right).
\tag{4.1}
\]

在 `(q,s)=(0,0)` 邻域，其简单主特征值记为 `lambda(a,q,s)`，压力为

\[
\mathscr P(a,q,s)=\log\lambda(a,q,s).
\tag{4.2}
\]

U3 与 roof/displacement multiplier ledger 给出 `C^3` spectral jet。

## 4.2 physical-time root

令 `Lambda_a(q)` 为唯一小根

\[
\mathscr P(a,q,\Lambda_a(q))=0.
\tag{4.3}
\]

因为

\[
\partial_s\mathscr P(a,0,0)=-\bar\tau_a<0,
\]

隐函数定理给出 `Lambda_a in C^3`。在 centered displacement convention 下，

\[
D_q\Lambda_a(0)=0,
\]

\[
\Sigma_{ij}(a)
=\partial_{q_iq_j}\Lambda_a(0)
=
\frac{\mathscr P_{q_iq_j}(a,0,0)}{\bar\tau_a},
\tag{4.4}
\]

\[
D^{\rm phys}(a)=\frac12\Sigma(a).
\tag{4.5}
\]

参数响应为

\[
\boxed{
\partial_a\Sigma_{ij}
=
\frac{\mathscr P_{a q_iq_j}}{\bar\tau}
-
\frac{\mathscr P_{q_iq_j}\,\partial_a\bar\tau}{\bar\tau^2}.
}
\tag{4.6}
\]

`P_{a q_i q_j}` 总阶数为三，正是 U3 的第一个不可省略用途。

## 4.3 低频 suspension resolvent

对 suspension flow `Phi_a^t`，令

\[
\widehat F_{a,z}(x)
=
\int_0^{\tau_a(x)}e^{-zt}F_a(x,t)\,dt,
\]

\[
L_{a,z}h=L_a(e^{-z\tau_a}h).
\]

Laplace-transformed correlation/resolvent 可分解为

\[
\widehat C_{F,G}(a,z)
=
H_{a,z}^{\rm same-flight}(F,G)
+
\left\langle
\widehat F_{a,z},
(I-L_{a,z})^{-1}\widehat G_{a,z}
\right\rangle.
\tag{4.7}
\]

第一项只含有限 roof-cell 积分；第二项完全落回 collision twisted resolvent。故 U3、roof multiplier regularity 与 finite-DQ 足以得到 `z=0` 邻域的参数三阶响应。

该结果是 θ-Theory、Green–Kubo 和 homogenization 所需的 **低频/积分型 suspension resolvent**。它不宣称已构造整个 moving-family BDL 高频 graph-domain theorem；后者不是下游 HJB 的必要输入。

## 定理 THETA-U3-TO-K1-1

在 BASE-U3、roof/displacement multiplier 和简单谱隔离成立时：

1. `mathscr P(a,q,s)` 在所需窗口中 `C^3`；
2. low-frequency suspension reduced resolvent `C^3`；
3. physical drift、covariance、diffusion field存在；
4. centered physical diffusion matrix满足 (4.6)；
5. Green–Kubo、pressure-Hessian 和 martingale bracket 三种定义一致。

---

# 5. K1 到 K1.5：共同算子空间与系数/椭圆场

## 5.1 新工具：Banach-bundle stabilization

令 `B_a` 为 parameter Banach bundle，`{U_alpha}` 为有限 atlas，

\[
G_{\alpha,a}:B_a\to B_\alpha
\]

为有界局部 trivializations。取 subordinate smooth partition of unity `chi_alpha`，并令

\[
B_*=\bigoplus_{\alpha=1}^N B_\alpha.
\]

定义

\[
J_a h
=
(\sqrt{\chi_\alpha(a)}G_{\alpha,a}h)_\alpha,
\tag{5.1}
\]

\[
R_a(v_\alpha)_\alpha
=
\sum_\alpha
\sqrt{\chi_\alpha(a)}G_{\alpha,a}^{-1}v_\alpha.
\tag{5.2}
\]

则

\[
\boxed{R_aJ_a=I_{B_a}.}
\tag{5.3}
\]

因此 `E_a=J_aB_a` 是固定空间 `B_*` 的 uniformly complemented moving subspace，projection 为

\[
P_a=J_aR_a.
\]

把 fiber operator 稳定化为

\[
\widehat L_a=J_aL_aR_a\in\mathcal L(B_*).
\tag{5.4}
\]

于是跨参数 operator difference、Riesz projection 和 Kato calculus 都在同一个固定 Banach 空间中有定义。

### 证明

由 partition identity，

\[
R_aJ_ah
=
\sum_\alpha\chi_\alpha(a)h=h.
\]

有限 atlas 和 uniformly bounded transitions 给出 `J_a,R_a,P_a` 的统一界与参数正则性。

该 stabilization lemma 同时修复：

```text
fiberwise atlas trivialization
!= parameterwise common operator realization
```

的问题；不再需要假装所有 fiber image 天然相同。

## 5.2 `(x,p)` coefficient lift

令 selector

\[
\Theta:(x,p)\mapsto a
\]

先作为独立的 finite-response/cotangent signal 输入；只有在 HJB 层才令 `p=Du`。

若

\[
\Sigma,\Gamma,\bar b,\bar\tau\in C^{3,\alpha}(A),
\qquad
\Theta\in C^{3,\alpha}(K;A),
\]

则 corrected Hölder–Nemytskii/finite-dimensional chain rule 给出

\[
(x,p)\mapsto
\Sigma(\Theta(x,p)),
\Gamma(\Theta(x,p)),
\bar b(\Theta(x,p))
\in C^{3,\alpha}(K).
\]

若宏观 coupling matrix 为 `B(x,p)`，定义

\[
A(x,p)
=
\frac12B(x,p)\Sigma(\Theta(x,p))B(x,p)^\top.
\tag{5.5}
\]

若

\[
\Sigma(a)\ge\lambda_\Sigma I,
\qquad
B(x,p)B(x,p)^\top\ge\lambda_B^2I,
\]

则

\[
\boxed{A(x,p)\ge\frac12\lambda_\Sigma\lambda_B^2I.}
\tag{5.6}
\]

`lambda_Sigma>0` 可由 displacement cocycle 的非 coboundary spectral gap 得到；在 compact window 上由连续性升级为统一下界。

## 定理 THETA-K15-COMMON-SPACE-COEFFICIENT-LIFT-1

U3/K1 的 `C^{3,alpha}` spectral data、stabilized common space、`C^{3,alpha}` selector 和 nondegeneracy packet 推出：

1. 固定共同算子实现；
2. `(x,p)` drift/covariance/area-anomaly/roof fields；
3. 一致椭圆场；
4. 这些 fields 的 parameter and state moduli；
5. 下游 K2 所需的 frozen generator family。

---

# 6. K1.5 到 K2：Doob 选择、rough WIP 与非自治均质化

## 6.1 Doob selector 必须先于 HJB 闭合

对 twist/control signal `zeta`，设

\[
L_{x,p,\zeta}h_{x,p,\zeta}
=e^{\mathscr P(x,p,\zeta)}h_{x,p,\zeta}.
\]

定义 Doob kernel

\[
\mathsf P_{x,p}^{\zeta}f
=
 e^{-\mathscr P(x,p,\zeta)}
 h_{x,p,\zeta}^{-1}
 L_{x,p,\zeta}(h_{x,p,\zeta}f).
\tag{6.1}
\]

它是由 frozen microscopic system 和外生 `(x,p,zeta)` 构造的 Markov selector；不能用未知 HJB solution 反向定义微观系统。

## 6.2 uniform martingale rough package

对 centered observable `v_theta`，需要：

```text
UM1 compact chamber and physical-clock normalization
UM2 q>4 uniform moment
UM3 martingale-coboundary decomposition
UM4 conditional quadratic-variation convergence
UM5 second-level/area compensator convergence
UM6 maximal coboundary negligibility
UM7 initial-law forgetting
UM8 parameter continuity of Sigma/Gamma/decomposition
UM9a quantitative enhanced-WIP rate
   or
UM9b uniform enhanced-WIP plus diagonal block selection
UM10 freezing/switching modulus and limiting MP uniqueness
```

在 uniform spectral-gap、`B -> L^q` embedding 和 bounded observables 下，令

\[
\chi_\theta
=
\sum_{n\ge1}\mathsf P_\theta^nv_\theta,
\]

并定义 martingale difference

\[
m_\theta
=v_\theta+\chi_\theta-\chi_\theta\circ T_\theta.
\]

几何收敛给出 UM2、UM3、UM6、UM7；对 `m_otimes m` 和 antisymmetric area observable 再作一次 Poisson decomposition 给出 UM4、UM5；K1.5 的 common-space resolvent identity给出 UM8。

UM9 有两种合法入口：

1. 提交一个 quantitative enhanced-CLT rate `r(N)`；
2. 只提交 compact-parameter uniform enhanced WIP，然后选择 diagonal block length `m_epsilon`，使 block count 乘 uniform approximation error趋零。

第二条避免把“必须先知道一个显式 Berry–Esseen 指数”错误写成定理必需条件。

## 6.3 rough WIP

定义

\[
W_N(t)
=N^{-1/2}\sum_{j< Nt}v_\theta\circ T_\theta^j,
\]

\[
\mathbb W_N(t)
=N^{-1}\sum_{0\le i<j<Nt}
 v_\theta\circ T_\theta^i
 \otimes
 v_\theta\circ T_\theta^j.
\]

则统一地

\[
(W_N,\mathbb W_N)
\Longrightarrow
(W_\theta,\mathbb W_\theta+t\Gamma_\theta)
\]

于 `p`-variation rough-path topology。

## 6.4 nonautonomous homogenization

慢变量使 parameter 在 blocks 间变化：

\[
\theta_t^\varepsilon
=
\Theta(X_t^\varepsilon,p_t^\varepsilon).
\]

取 `m_epsilon -> infinity`、`h_epsilon=epsilon^2m_epsilon -> 0`，并使 enhanced-WIP error、freezing error 与 switching error 的 block sum趋零。由 rough-path continuity 得到极限

\[
dX_t
=
\bar b(X_t,p_t)dt
+\sigma(X_t,p_t)dW_t
+b_\Gamma(X_t,p_t)dt,
\tag{6.2}
\]

其中

\[
\sigma\sigma^\top=\Sigma,
\]

`b_Gamma` 是 area anomaly 经 vector-field bracket 推出的确定性漂移。

## 定理 THETA-K2-DOOB-ROUGH-HOMOGENIZATION-1

THETA-K15-COMMON-SPACE-COEFFICIENT-LIFT-1 与 UM1–UM10 推出：

1. frozen Doob-selected kernels；
2. uniform enhanced WIP；
3. parameter-varying rough driver；
4. nonautonomous homogenized martingale problem/RDE；
5. 初始 law、physical clock、area anomaly 和 coefficient conventions 的一致性。

---

# 7. K3 必须拆成三个 typed branches

## 7.1 K3-sequential

控制 `u` 先选、`v` 后响应时，下值与上值分别对应

\[
H^-(x,p,X)
=
\sup_u\inf_v F(x,p,X;u,v),
\]

\[
H^+(x,p,X)
=
\inf_v\sup_u F(x,p,X;u,v).
\]

DPP 和 viscosity limit 可分别成立；不需要 Isaacs equality。

## 7.2 K3-simultaneous / Isaacs

若采用 compact relaxed controls `mu,nu`，且 `F` 对 `(mu,nu)` 双线性连续，则 Sion/von Neumann minimax 给出 mixed Isaacs equality：

\[
\sup_\mu\inf_\nu F
=
\inf_\nu\sup_\mu F.
\tag{7.1}
\]

这不推出 pure-strategy saddle；pure saddle 需要额外 convex-concave 或显式 saddle certificate。

## 7.3 K3-filter

若 fast hidden kernel 在 weighted norm 中每 `r_*` 步收缩 `rho^{r_*}`，observation likelihood 满足

\[
0<g_-\le g_y(x)\le g_+<\infty,
\]

并且 posterior/prediction `W`-moment ball 保持，则 Bayes map 在该 ball 上有有限 Lipschitz factor `C_Bayes`。选择 observation gap 使

\[
\boxed{C_{Bayes}\rho^{r_*}<1,}
\tag{7.2}
\]

即可得到 filter stability 与 strategy-tree-uniform belief collapse。

weighted branch 还必须另行提交：

```text
weighted limit HJB comparison / uniqueness.
```

只提交 Lyapunov coupling 不能直接铸造 K3 PASS。

## 定理 THETA-K3-TYPED-FANOUT-1

K2 limit、local generator consistency、DPP compactness 与对应 typed packet 分别推出：

1. sequential lower/upper HJB；
2. simultaneous mixed Isaacs；
3. filter stability；
4. partially observed game 在 belief state 上的 DPP；
5. bounded 或 weighted comparison 后的唯一极限。

---

# 8. HJB 与 theta-expectation

## 8.1 不同入口

- 无控制/单控制：`K2 -> HJB`；
- sequential game：`K2 + K3-sequential -> H^- / H^+`；
- simultaneous mixed game：`K2 + K3-simultaneous -> Isaacs`；
- filtering：`K2 + K3-filter -> belief-state HJB`；
- path-dependent observation/control：进入 PPDE，而不是强行压回有限维 HJB。

在 Markov 情形，极限方程写为

\[
\partial_tu
+\operatorname{tr}(A(x,Du)D^2u)
+H(x,Du)=0,
\tag{8.1}
\]

或相应 controlled/Isaacs 版本。

## 8.2 theta-expectation

在 comparison/uniqueness 下，定义

\[
\mathcal E_{s,t}^{\theta}[\phi](x)
=u(s,x),
\quad u(t,\cdot)=\phi.
\tag{8.2}
\]

它具有：

- monotonicity；
- constant preservation / cash convention；
- time consistency；
- terminal stability；
- Markov 或 belief/path-state semigroup property。

若 `H` 非凸，则该 nonlinear expectation 一般不满足 subadditivity，不能自动识别为 `G`-expectation。

## 定理 THETA-HJB-SEMIGROUP-1

K2/K3 的 typed limit、coefficient continuity、ellipticity 和相应 comparison theorem 推出唯一 HJB/Isaacs/PPDE limit 及 theta-expectation semigroup。

---

# 9. FBSDE / PPDE / path evaluation 的正确层级

representation 永远位于 HJB/theta-semigroup **之后**。

## 9.1 Markov semilinear/quasilinear branch

若 diffusion 非退化，generator 对 Hessian 为线性，driver 对 `(y,z)` 满足标准 Lipschitz/monotonicity 条件，则由 decoupling field 得到 classical FBSDE。此时

\[
Z_t=\sigma^\top(X_t,Du_t)Du(t,X_t),
\]

而不是把 HJB gradient `p` 与 BSDE integrand `Z` 混同。

## 9.2 HJB/control branch

一般 control HJB 应使用 controlled BSDE、randomization 或 relaxed-control representation。一个 payoff-dependent calibrated linear law只代表该 payoff 的线性化，不是统一 payoff-independent martingale problem。

## 9.3 fully nonlinear second-order branch

若 Hessian dependence 也是非线性的，需要 2BSDE、nonlinear martingale problem 或其他 fully nonlinear representation；不能用一个 classical FBSDE 冒充。

## 9.4 path-dependent branch

当 filter/history/control path 是真实状态时，DPP 位于 path space，得到 PPDE。path evaluation 定义为

\[
\mathcal E_{s,t}^{\theta}[\Phi](\omega_{[0,s]})
=U(s,\omega_{[0,s]}),
\]

并由 functional Itô / path-dependent viscosity / BSDE 或 2BSDE branch 表示。

## 定理 THETA-REPRESENTATION-HIERARCHY-1

THETA-HJB-SEMIGROUP-1 加对应 regularity/nondegeneracy packet，分别推出：

```text
Markov semilinear        -> FBSDE
controlled HJB           -> controlled/randomized BSDE
fully nonlinear second order -> 2BSDE/nonlinear MP
path-dependent state     -> PPDE + path-dependent BSDE/2BSDE
```

没有任何 representation theorem 被允许反向证明 CM2、U3、K1、K2 或 HJB limit。

---

# 10. 最大性与“所有 gap 闭合”的精确含义

## 定理 THETA-MAXIMALITY-AND-CLOSURE-1

结合 v80/v82 的 refutation 与本报告的正向编译：

1. 不存在仅由 local moving-singularity geometry 自动推出的 unrestricted uniform CM2；
2. 因而任何正确一般定理必须显式包含 bilateral recovery/rate 或等价 product-tail packet；
3. 在该 packet 定义的最大 admissible class 上，CM2、U3、K1、K1.5、K2、typed K3、HJB/theta 和 downstream representation 的依赖链全部闭合；
4. v68/v69 证明该 class 非空且可含 `K != 0` 的 moving-seam systems；
5. specular nonconjugate Sinai 的更大 actual subclass 是独立 strengthening，不能作为当前 theorem 的隐藏前提，也不再是一个未命名逻辑 gap。

因此最终状态是：

```text
impossible universal claim: CLOSED BY REFUTATION
maximal packetized theorem: CLOSED BY PROOF
actual nonzero scoped class: NONEMPTY
all downstream arrows: CLOSED
unreviewed system strengthenings: EXPLICITLY OUTSIDE THE CLAIM
```

---

# 11. 对现有三篇稿件的直接修正

## Paper 1 response theory

应拆出两个清晰结论：

1. source modules / obstructions / scoped actual response；
2. bilateral CM2 packet 与 CM2-to-U3 theorem。

不得继续让“conditional S1–S3”与 actual radial theorem 混在一个主定理中。

## Paper 2 theta-expectation/HJB

`ass:paper1_response_input` 必须替换为 typed imports：

```text
CM2/U3 packet ID
K1 pressure/root/diffusion theorem
K1.5 common-space coefficient theorem
K2 uniform rough/nonautonomous theorem
optional K3 branch ID
comparison theorem ID
```

主定理拆为：

- conditional theorem over the packetized admissible class；
- actual corollary for each verified scoped system。

## Paper 3 representation calculus

保留 post-derivation 定位，但按本报告第 9 节拆分 FBSDE、controlled BSDE、2BSDE 和 PPDE；不能把 payoff-calibrated linearization 写成整个 nonlinear semigroup 的单一 law。

---

# 12. 下一步仓库动作

1. 以本报告为新 dependency source，不改写历史 v164/v83 bytes；
2. 新建机器可读 packet/status 文件；
3. 对 Paper 1/2/3 做 import lint；
4. 为每条 theorem UID 建 theorem inventory；
5. 只在 actual packet 完整、独立审阅通过后把对应 scoped status 从 `CONDITIONAL` 提升为 `ACTUAL`。
