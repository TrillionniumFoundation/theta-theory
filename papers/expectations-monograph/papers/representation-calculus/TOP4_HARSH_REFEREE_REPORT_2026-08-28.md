# 顶级综合数学期刊标准严苛审稿意见

## 稿件识别

- 稿件：`main.tex`
- 标题：*Representation Calculus for theta-Expectations*
- 审阅快照：`main` at `08aac05e51577bcd2f2ec5a6aef2a960a8d3ef9d`
- 审阅日期：2026-08-28
- 编辑建议：**Reject。即使暂时接受 Paper 2 的 HJB 半群，本稿的主要“表示定理”仍多为条件性恒等式、同义反复或一般不成立的稳定性断言，原创性也远未达到顶级综合期刊标准。**

## 一、给编辑的结论

这篇六页稿件的基本思想是：先固定一个 nonlinear HJB solution `u`，沿该解对 PDE 作 payoff-dependent 线性化，随后把得到的线性抛物算子表示为扩散、Itô/BSDE 和某种“Cameron--Martin--Girsanov”平移。正确版本的第一步是标准线性化，第二步是标准 Feynman--Kac / martingale problem，第三步的 Itô 恒等式也属常规。

然而当前稿件不仅缺乏顶刊级新意，还含有数个硬错误：

1. 它输入的 HJB 符号与 Paper 2 实际写出的方程相反；
2. linearized representation 先假设所需的一阶展开，因而没有证明半群可微；
3. viscosity regularization 的收敛不能推出 derivative semigroup 的收敛；
4. 当 `sigma=sigma(x,p)` 时，`Z=sigma(x,p)^T p` 不是通过逐点矩阵求逆即可解出 `p` 的线性关系；
5. 所谓 Cameron--Martin--Girsanov theorem 只是对 HJB 系数做代数替换，没有任何测度变换；
6. robust-pricing envelope 只是对一族已解 PDE 取 supremum，没有动态规划、measurable selection或 time consistency theorem。

这些问题使 main representation package 不成立。更根本地，即使全部修正，得到的也主要是“在一个已知光滑解附近，PDE 的方向导数满足线性方程，并可用相应扩散表示”的经典事实，尚未显示足够原创性或深度。

## 二、稿件中合理的出发点

1. 作者正确强调：一般 nonlinear generator不可能由一个 payoff-independent classical martingale problem对所有 tests同时表示。
2. 稿件明确区分 gradient `p` 与 BSDE integrand `Z`，意识到二者不应混用。
3. 作者承认所有概率表示都是 post-derivation，并不用于证明 deterministic billiard HJB。
4. payoff-calibrated law依赖 decoupling field `u`，这种依赖应当被明确记录。

但当前公式没有把这些原则落实成正确的新定理。

## 三、致命问题

### 1. 输入 PDE 与 Paper 2 的输出 PDE 不是同一个方程

Paper 3 假设

`-u_t - tr(D(x,grad u) D2u) - H(x,grad u) = 0`。

Paper 2 则定义

`Hcal(x,p,X)=-tr(D(x,p)X)-H(x,p)`

并写

`u_t + Hcal(x,Du,D2u)=0`，

即

`u_t - tr(D D2u)-H=0`。

二者的扩散项和 Hamiltonian项在乘去整体符号后并不一致。Paper 3 的 `prop:parabolic_orientation_ledger` 只验证了本稿内部符号，没有验证它来自 Paper 2。

因此 `ass:theta_semigroup_input` 并不是 companion paper 的 theorem input；整篇 representation calculus没有表示 Paper 2 所导出的对象。必须先在两个仓内文件中统一 PDE，并重做所有线性化、Itô drift、BSDE driver和 shift formula。

### 2. `thm:linearized_representation` 没有证明可微性

定理假设：

`u^delta = u + delta v + o(delta)` locally uniformly。

然后把这一展开代入 PDE，得出 `v` 满足线性化方程。这只是“若导数存在，则它满足形式线性化”的必要条件，不是 semigroup differentiability theorem。

要得到真正的表示定理，作者至少要证明：

- solution map `phi -> u` 在指定 Banach spaces之间 Gâteaux / Fréchet 可微；
- difference quotient有统一估计和 compactness；
- nonlinear coefficients 对 `p` 的 remainder可控；
- degenerate parabolic case的 uniqueness足以识别极限；
- terminal perturbation `eta` 的 admissible class和导数范数。

当前 theorem把最重要的结论写进假设，随后只做一行形式微分。它不能支撑“representation calculus package”。

### 3. `thm:regularized_diffusion_representation` 一般不成立

稿件声称：若 viscosity solution `u` 是 uniformly parabolic regularizations `u^epsilon` 的局部一致极限，则相应 calibrated linear diffusion semigroups也收敛到原 degenerate HJB semigroup的 derivative representation。证明引用 viscosity stability和“stability of the linearized coefficients”。

这是不成立的推理。局部一致收敛 `u^epsilon -> u` 不蕴含：

- `grad u^epsilon -> grad u`；
- `D2 u^epsilon -> D2u`；
- `partial_p D(x,grad u^epsilon) D2u^epsilon` 收敛；
- nonlinear solution maps的导数收敛；
- differentiation与 `epsilon -> 0` 交换。

在退化极限中，smooth approximations可以形成 boundary layers、gradient concentrations或 nonunique linearized limits。要成立，需要强得多的 uniform `C^{1,2}` / Sobolev estimates、semiconcavity、Mosco/graph convergence或独立的 tangent equation stability theorem。

`ass:representation_window` 若直接假设“viscosity-regularized degenerate representation”存在，则定理成为循环定义；若不假设，则证明错误。该 theorem必须删除或完全重建。

### 4. `Z=sigma(x,p)^T p` 的反演错误

稿件写：当 `sigma^T` 在 relevant jet region 可逆时，

`p=(sigma^T)^{-1} Z`。

但这里 `sigma` 本身依赖 `p`：

`Z = sigma(x,p)^T p`。

逐点矩阵 `sigma(x,p)^T` 对固定 `p` 可逆，只能说明给定该 `p` 时矩阵可逆；它不能把未知的 `p` 从 `Z` 中显式解出。需要研究非线性映射

`F_x(p)=sigma(x,p)^T p`。

至少必须假设并证明 `F_x` 在相关区域是单射且有光滑逆，例如 Jacobian

`D_p F_x(p)=sigma(x,p)^T + [D_p sigma(x,p)^T]p`

一致可逆，并控制其像。仅有 `D(x,p)>0` 不足以保证这一点。

因此 `thm:fbsde_representation` 中 driver

`g(t,x,Z)=H(x,p)-b^u(t,x)·p`, `p=(sigma^T)^{-1}Z`

通常没有定义。即使沿已知解轨道可以把 `p=grad u(t,X_t)` 代入并得到一个 Itô identity，也不能把它提升成以 `(t,x,Z)` 为自变量的标准 BSDE driver。

### 5. 所谓 FBSDE 表示是已知解上的 Itô 恒等式，不是闭合 FBSDE

forward SDE 的系数 `b^u,a^u` 已依赖完整 decoupling field `u` 和 `D2u`。因此必须先解出 HJB，才能写出 forward law。随后定义

`Y_t=u(t,X_t)`, `Z_t=sigma^T grad u`

并应用 Itô 公式，当然得到一个 BSDE identity。

这不是一个可独立求解、可反向表示 nonlinear semigroup 的 FBSDE system；它只是对已知 smooth solution的随机化。若作者坚持称为“representation”，必须明确它不提供 existence、uniqueness、numerical scheme或 probabilistic construction，并与 classical nonlinear Feynman--Kac / four-step scheme文献精确比较。当前主 theorem把它包装成新的 representation hierarchy，过度陈述。

### 6. “Cameron--Martin--Girsanov formula”并非 Girsanov theorem

`thm:nonlinear_cm_formula` 定义

`D^h(x,p)=D(x,p+h)`,

`H^h(x,p)=H(x,p+h)-H(x,h)`，

然后通过加减项得到一个 defect `Lambda_h`。这是纯代数恒等式。文中没有：

- 基准概率测度和新测度；
- adapted drift shift；
- stochastic exponential；
- Cameron--Martin space；
- Novikov/Kazamaki条件；
- Radon--Nikodym derivative；
- expectation identity。

因此不能命名为 Cameron--Martin--Girsanov formula。在线性二次特例中 defect出现 `p^T a h`，也只说明 PDE 中多了 drift-like 项；从这一项到 Girsanov测度变换仍需完整 stochastic theorem。

更进一步，`h(t,x)` 是任意向量场。把 HJB gradient变量替换为 `p+h` 并不等价于对 payoff作 Cameron--Martin平移；除非 `h` 是某个标量 potential 的梯度并处理额外的 `h_t,Dh,D2` 项，否则甚至没有自然的函数变换来源。

建议删除该命名，将结果降为“algebraic Hamiltonian shift identity”，或真正证明一个 calibrated diffusion laws之间的 Girsanov theorem。

### 7. shift notation本身不一致

定义称 `h=h(t,x)`，但写 `H^h(x,p)`、`D^h(x,p)`，省略时间依赖；`Lambda_h(t,x,p,X)` 又恢复 `t`。若 `h` 随时间和空间变化，任何由变换 `u -> u+psi` 产生的 PDE identity都会出现 `partial_t psi`、`D2psi` 等项。当前公式只是重新定义一个新 operator，而不是 semigroup之间的 transformation formula。

### 8. `thm:linearity_obstruction` 的结论被过度推广

从同一 law下 `f,g,f+g` 的 martingale property可以推出 generator drift沿该 law的 occupation measure为零；要得到整个 test class和所有 `(t,x)` 上的 additivity，还需要：

- 每个 initial state均有相应 law；
- generator和 drift有足够连续性；
- support / occupation measures覆盖目标区域；
- martingale problem的 domain稳定于加法。

稿件以“varying the initial point gives additivity”一句结束，未写这些假设。核心思想是标准且正确的，但 theorem陈述应精确，且不构成顶刊级原创结果。

### 9. calibrated generator需要二阶解正则性，却没有来源

`b^u` 包含

`partial_p D_ij(x,grad u) partial_ij u`。

Paper 2 只声称 viscosity solution；对 degenerate/nonconvex HJB，一般没有 `C^{1,2}`。`ass:representation_window` 直接假设 smoothness或 smooth regularization limit，但：

- 没有展示任何非平凡 payoff满足该 window；
- 没有 interior regularity theorem；
- 没有处理 boundary of the window / exit times；
- 没有说明 calibrated SDE离开 `K` 后如何继续。

所以正向 representation可能只对一个空或人为选择的 class成立。至少需要给出一个实际系数/ payoff例子和局部 stopping-time版本。

### 10. martingale problem / SDE well-posedness被写成“regular enough”

`thm:smooth_diffusion_representation` 的全部概率内容都被放进“coefficients are regular enough for the martingale problem to be well posed”。这不是 theorem-level assumption。必须明确 Lipschitz / bounded measurable / ellipticity条件、weak或 strong solution、nonexplosion、time-inhomogeneous domain以及 representation的函数空间。

在当前写法下，定理只是引用经典结果的同义改写。

### 11. robust-pricing stress envelope没有任何新的动态结论

定义

`Pi_H phi = sup_{h in H} u^h`

后，proposition只说每个固定 `h` 有其 calibrated representation。并未证明 supremum：

- 满足某个 HJB / Isaacs equation；
- 具有动态一致性；
- 可由 measurable selector实现；
- 是 risk measure或 nonlinear expectation；
- 保持 cash additivity、convexity或 time consistency。

所以“robust pricing”只是解释性标签，而非数学应用。对顶刊文章没有实质贡献。

### 12. 主 package 的原创性不足

修正所有错误后，剩余内容大致是：

- nonlinear PDE solution map的形式导数；
- 线性抛物方程的 diffusion representation；
- 对已知 smooth solution应用 Itô公式；
- 一个 operator shift identity。

这些均是经典工具。稿件没有提出新的 representation theorem、regularity theorem、duality、comparison、martingale characterization或 nonlinear expectation结构。六页稿件远未达到顶级综合期刊的原创性阈值，也很难作为独立研究论文成立。

## 四、逐项定理审查

| 结果 | 审稿判断 |
|---|---|
| `ass:theta_semigroup_input` | 与 Paper 2 符号不一致，且 Paper 2 本身未证明 |
| `thm:linearity_obstruction` | 标准观察；陈述需加 support/domain 假设 |
| `thm:linearized_representation` | 假设导数存在后形式微分；未证明可微性 |
| `thm:smooth_diffusion_representation` | 经典 martingale problem引用；假设“regular enough”不精确 |
| `thm:regularized_diffusion_representation` | 一般错误；viscosity stability不控制 derivatives |
| `lem:gradient_z_conversion` | 当 `sigma` 依赖 `p` 时反演错误 |
| `thm:fbsde_representation` | 已知解上的 Itô恒等式；driver通常未定义为 `Z` 的函数 |
| `prop:parabolic_orientation_ledger` | 内部一致，但与 Paper 2 不一致 |
| `thm:nonlinear_cm_formula` | 代数 shift，不是 CM/Girsanov theorem |
| `prop:robust_pricing_stress_test` | 解释性陈述，无 robust-control theorem |
| `thm:representation_package` | 汇总了未证明/错误/经典结果，不能成立 |

## 五、可重投前的最低要求

1. 先统一 Paper 2 / Paper 3 的 HJB 符号和时间方向。
2. 证明 nonlinear semigroup对 terminal payoff的真实可微性，而不是假设 expansion。
3. 删除 degenerate regularization theorem，除非能给出强导数稳定性证明。
4. 对映射 `p -> sigma(x,p)^T p` 建立可逆性，或把 BSDE限定在 `D` 与 `p` 无关的情形。
5. 将 FBSDE诚实定位为已知 smooth decoupling field上的 Itô representation。
6. 将“Cameron--Martin--Girsanov”改名为 algebraic shift，或补上真正的 measure-change theorem。
7. 给出精确 SDE/martingale problem假设和 stopping/localization机制。
8. 若要独立发表，必须增加一个非经典主定理；仅重写经典线性化和 Itô公式不足以构成研究论文。

## 六、最终建议

**Reject。** 当前稿件的核心结论在数学上不成立，修正后仍主要是标准后处理 calculus，缺乏顶刊级原创性。最合理的处理是把少量正确的 sign/linearization notes并入未来一篇已经证明 HJB theorem 的论文附录，而不是作为独立第三篇文章。