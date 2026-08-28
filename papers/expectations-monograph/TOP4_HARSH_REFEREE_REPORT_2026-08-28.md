# 顶级综合数学期刊标准严苛审稿意见

## 稿件识别

- 稿件：`main.tex`
- 标题：*A Conditional Theory of theta-Expectations from Deterministic Billiards*
- 审阅快照：`main` at `08aac05e51577bcd2f2ec5a6aef2a960a8d3ef9d`
- 审阅日期：2026-08-28
- 审阅标准：以 Annals / Inventiones / JAMS / Acta 级别的正确性、原创性、概念集中度和证明自足性为基准
- 编辑建议：**Reject；不建议按 ordinary major revision 处理。若将来重投，应作为一篇数学目标完全不同的新稿件。**

## 一、给编辑的结论

这部稿件的优点是作者最终明确承认其结论是一个“conditional reduction”：普通有限视界色散台球几何并不推出后文所需的 mixing、suspension non-lattice、moving-boundary response、mechanically compatible prelimit 和 uniform homogenization；这些内容被集中写成五项解析 admissibility package。问题在于，这五项并非技术性边界条件，而正是文章标题和摘要所暗示的“从确定性台球第一性原理构造 theta-expectation”所需要证明的全部核心困难。

因此，当前主定理在逻辑上大致是：**假设台球已经具有足以完成响应、正确子、极限闭合和比较原理的全部性质，则可以按照标准 perturbed-test / viscosity 流程得到相应 HJB 半群。** 这可以作为研究计划、条件性框架或长篇技术路线图，但还不是顶级综合期刊所要求的第一性原理定理，也不是一个已经实例化的抽象定理：仓内没有给出一个真正 moving、nonconjugate 的具体台球/机械端口，同时验证 A1--A5 并闭合所需全部一致常数。

更严重的是，拆分出的三篇论文和 CM2 控制树反向暴露了总论依赖链并未闭合：Paper 1 明确保留一般 re-insertion、双时间条件混合和 moving-flow graph/symbol theorem 为开放输入；Paper 2 却把这些内容作为已证明的 companion theorem 使用；CM2 最新控制状态又明确记录 actual admissible classwide CM2 仍需要 actual local packets，且所有实际实例化缺口并未闭合。总论不能同时把这些内容写成“假设”、把它们当作“已由 Paper 1 导出”，又把最终结论宣传为从台球第一性原理得到。

我的结论是：**稿件在当前形态下不具备可接受的核心定理。** 它不是差几处引理，而是研究对象、主结论和依赖关系需要重新确定。

## 二、我认为稿件中真正有价值的部分

1. 作者已经停止把普通正曲率、有限视界或 compactness 当作自动蕴含 uniform response / Dolgopyat / homogenization 的理由。这种 fail-closed 的态度是正确的。
2. 稿件努力区分几何输入、谱输入、moving-boundary response、机械 prelimit 和 viscosity closure，依赖图比早期“统一理论”式写法更诚实。
3. 对 singular collision map、各向异性空间、moving traces、Green--Kubo 系数和 nonlinear semigroup 的接口性整理，作为研究纲领可能有参考价值。
4. 将 BSDE / Girsanov 表示明确放在 HJB 导出之后，而不是作为微观推导工具，逻辑方向原则上正确。

这些优点不足以弥补以下致命问题。

## 三、致命数学问题

### 1. A1--A5 不是辅助假设，而是目标定理的主体

摘要把五项性质作为 analytic admissibility package。按正文的依赖说明：

- A1 提供统一谱间隙、约化 resolvent 和混合；
- A2 提供 suspension 非格性 / Dolgopyat 型频率控制；
- A3 提供 moving-singularity derivative、trace complexity summability 和 differentiated resolvent words；
- A4 提供与机械端口一致的 prelimit HJ 问题；
- A5 提供 compactness、contact selection、residual control、half-relaxed passage 和 comparison closure。

这些五项合在一起已经包含了从微观动力学到宏观 HJB 的全部难点。特别是 A3 和 A5 几乎分别等价于“响应理论可用”和“homogenization 可完成”。在没有一个实际系统验证这些假设之前，主定理的数学内容主要是一个依赖清单，而非新的 first-principles theorem。

顶刊不能接受通过把最困难的命题改名为 admissibility 来闭合证明。作者必须证明这些条件，或者彻底放弃“from deterministic billiards / first-principles construction”的主张，把文章改写成一个抽象的条件性稳定性定理，并清楚说明与现有 deterministic homogenization / viscosity perturbed-test 文献相比的新内容到底是什么。

### 2. 没有非平凡的 actual instantiation

当前仓内能确认的正例主要是：

- exact conjugacy / rigid translation 一致性例子；
- 由显式 invariant flux differentiation 产生的 radial invariant-source benchmark；
- 二阶 complete assembly 后的 source-specific recovery；
- 一系列 obstruction 和 conditional compiler。

这些都没有给出一个独立指定的、真正 nonconjugate moving-scatterer correlation source，并验证总论需要的全套多时间响应、uniform coefficient regularity、prelimit closure 和 homogenization。exact conjugacy 会把 moving-face 项在所选 trivialization 中直接消掉；differentiated invariance 则把 primitive 预先写成 `(I-L) rho'`。二者都不能充当一般机械端口的实例化。

一篇以“从确定性台球产生 nonlinear expectation”为主张的文章，至少必须展示一个完整具体模型，而不是只给可验证条件的目录。

### 3. 总论、Paper 1、Paper 2 与 CM2 的依赖关系互相矛盾

总论把 response 和 homogenization closure列为假设；Paper 2 将 Paper 1 的一般 moving-singularity response、trace insertion、multi-response 和 regularity-loss package 当作已证明接口；然而 Paper 1 自己明确声明：

- 一般 nonconjugate prescribed correlation source 尚未构造；
- generic re-insertion theorem 尚未证明；
- moving-family flow graph domain / symbol estimate 尚未证明；
- 双时间 singular-profile conditional mixing 仍是开放输入；
- higher radial response 必须是 complete-assembly specific。

与此同时，`canonical/CM2_UNIFIED_TREE_INDEX.md` 的 controlling status 写明：unrestricted universal moving-scatterer CM2 被精确反驳；local-geometry-only uniform CM2 被实际谱障碍反驳；actual uniform admissible classwide CM2 仍需要 actual local packets；`AllPositiveActualInstantiationGapsClosed: false`。

因此当前 dependency DAG 不是 closed DAG。Paper 2 不能把 Paper 1 明确没有证明的内容进口为定理，总论也不能据此宣称第一性原理链条已经完成。

### 4. HJB 的时间方向和符号在拆分稿之间不一致

Paper 2 定义

`Hcal(x,p,X) = -tr(D(x,p)X) - H(x,p)`

并写终端值问题

`u_t + Hcal(x,Du,D2u) = 0`。

这等价于 `u_t - tr(D D2u) - H = 0`。对终端数据作反向时间 `tau=T-t` 后得到 `U_tau + tr(D D2U) + H = 0`，其扩散方向与标准前向抛物方程相反。

Paper 3 则使用

`-u_t - tr(D D2u) - H = 0`，

即 `u_t + tr(D D2u) + H = 0`，并在其 sign ledger 中采用这一方向。两篇稿件实际上表示不同的 PDE。总论必须先固定唯一的时间约定、degenerate ellipticity 约定和 semigroup 定义，再逐一定理重做符号检查。当前错误会影响 comparison、short-time expansion、BSDE drift 和所谓 Cameron--Martin shift 的全部公式。

### 5. Green--Kubo 扩散张量的定义和正定性没有被充分证明

稿件采用一侧时间相关积分来定义 `D`，随后断言其 symmetric positive semidefinite。对非可逆确定性流，单侧矩阵相关积分一般不自动对称；应明确取对称部分或等价的双侧协方差，并证明积分收敛、坐标无关、正半定以及参数连续性。若使用 correlation Hilbert factorization，还必须构造同一个可比较的 Hilbert bundle，并证明平方根/因子在参数上的定量模，而不能仅从 `D` 连续就宣称所需的 Hilbert--Schmidt 控制。

这是 HJB 抛物性和 comparison 的基础，不是可留给 notation ledger 的细节。

### 6. 从各向异性配对收敛到局部一致/a.e. state 收敛的跃迁没有证明

主线反复使用“paired anisotropic topology”“admissible density bundle”“Liouville-a.e. identification”，但 HJB viscosity solution 是点态/局部一致概念。要从分布或对偶配对收敛得到 half-relaxed limit，需要明确：

- prelimit unknown 到底是相空间上的函数、分布还是等价类；
- 最大点/接触点如何在 singular branches 上选择；
- paired inequality 如何产生点态 viscosity inequality；
- grazing set 附近如何排除 mass escape；
- countable density basis 如何推出同一零测集外的 statewise convergence；
- branchwise oscillation modulus 的来源和对参数/尺度的一致性。

当前证明多以一句“compactness prevents escape”“density basis plus oscillation”代替上述步骤。A5 若直接假设这些结论，则主定理再次变成同义反复；若不假设，则证明不完整。

### 7. 所谓 concrete nonconvexity 是被端口直接写入，而非由台球动力学产生

拆分稿中的具体端口把

`V = V0 - lambda eta (p·e)^2 + kappa eta (p·e)^4 + ...`

作为 primitive read-out 直接指定。只要允许任意 `p` 依赖的 action read-out，选择负二次系数当然会制造局部非凸 Hamiltonian。这没有说明 nonconvexity 是台球响应产生的，也没有显示机械端口满足独立的 Hamiltonian / symplectic / work reciprocity 约束。

此外，所谓 dominance certificate 依赖未实际计算的 Paper 1 response constants；将 `lambda` 选得足够大只是参数化地压倒未知误差，并非台球轨道上的可核验实例。

如果非凸性是论文的旗舰新现象，作者必须从一个独立给定、物理一致的机械耦合中计算出该符号，而不是把它写进输入。

### 8. 拆分稿中的“具体有限视界三角 Lorentz cell”参数区间错误

Paper 2 取三角晶格最近邻距离为 1，并声称单圆散射体半径

`r0 in (1/(2 sqrt(3)), 1/2)`

即能阻断所有 corridor。该下界不正确。沿最短晶格方向的相邻平行散射体行间距为 `sqrt(3)/2`；水平中线在两行圆心之间距每行 `sqrt(3)/4`。因此只要 `r0 < sqrt(3)/4`，就存在正宽度直 corridor。稿件给出的区间包含大量 infinite-horizon 情形，例如 `r0=0.3`。

这不是措辞问题：具体实例的有限视界、uniform mixing 和所有后续系数都依赖这一几何条件。至少应将严格下界改为 `sqrt(3)/4`（并重新检查端点、变形裕度和其他 primitive directions），再重做 finite-horizon openness 论证。

### 9. 下游 representation calculus 含有一般不成立的命题

总论将 Paper 3 作为下游表示层，但其中至少有以下问题：

- linearized representation 先假设 `u^delta=u+delta v+o(delta)`，没有证明半群可微；
- viscosity solutions 的稳定性不蕴含其导数半群/linearized coefficients 在退化正则化下收敛；
- 当 `sigma=sigma(x,p)` 时，`Z=sigma(x,p)^T p` 不能仅凭每个 `p` 处矩阵可逆就写成 `p=(sigma^T)^{-1}Z`；这是一个非线性隐式方程，需要全局/局部可逆性；
- 所谓 Cameron--Martin--Girsanov theorem 只有 HJB 系数的代数平移，没有概率测度变化、指数鞅、Novikov/Kazamaki 条件或 Radon--Nikodym 密度。

因此总论不能把这些结果当作已建立的完整 representation hierarchy。

### 10. 文稿形态不适合顶级综合期刊

稿件兼具 monograph、proof ledger、研究计划、历史版本说明和三篇拆分稿源库的功能。大量 theorem inventories、dependency prose、internal status 和重复 guardrail 不能替代一条可审的主证明。顶刊审稿不是验证文件是否编译、hash 是否一致、label 是否齐全；这些 QA 只能证明工件完整，不能证明数学正确。

当前正文过宽：singular billiards、anisotropic transfer spaces、moving response、homogenization、nonlinear expectations、BSDE、Girsanov 和数值 certificate 被放进一个统一故事，但没有任何一层达到可独立验收的闭合程度。

## 四、主张—证明核查摘要

| 主张 | 当前证据 | 审稿判断 |
|---|---|---|
| 从有限视界色散台球第一性原理得到 theta-expectation | A1--A5 admissibility package | 未证明；核心内容被假设 |
| 一般 moving-boundary multi-response | Paper 1 conditional S1--S3 / source-specific radial benchmark | 未证明一般情形 |
| 确定性 HJB homogenization | paired residual ledger + A5 | prelimit、接触选择与收敛拓扑未闭合 |
| 具体非凸台球例子 | 任意指定负二次 action read-out | 非凸性被植入输入；具体几何区间还错误 |
| theta-expectation 表示理论 | payoff-calibrated linearization / BSDE / shift | 多处为假设性、同义反复或错误命名 |
| universal / classwide CM2 | 最新 canonical status | 已被反驳或仍需 actual packets |

## 五、可重新投稿前的最低要求

这不是一个可通过局部修补完成的 revision。最低路线只能二选一：

### 路线 A：真正的第一性原理论文

1. 固定一个明确的、非共轭 moving-scatterer family 和独立给定的机械端口。
2. 在同一模型上证明 A1--A5，而不是把它们列为 package。
3. 给出严格的双时间 response/CM2 或另一条足以控制全部系数的机制。
4. 正确定义 prelimit PDE/semigroup，证明 well-posedness 和统一估计。
5. 修正 HJB 时间方向，证明全局 comparison 的结构条件。
6. 从实际机械耦合计算出非凸系数，并提供可复核的数值/解析界。
7. 删除 BSDE/Girsanov 等下游材料，先把一个核心定理做成自足论文。

### 路线 B：诚实的抽象条件性论文

1. 删除“from deterministic billiards”“first-principles construction”等超出结论的措辞。
2. 将系统抽象为满足 A1--A5 的 fast dynamics；把台球仅作为尚待验证的候选例子。
3. 证明一个真正新的 abstract homogenization theorem，并与现有 deterministic homogenization / viscosity literature 精确比较。
4. 将假设压缩为可检查的最小条件，避免把结论本身写入 A5。
5. 不再把未证明的 companion results 写成已验证依赖。

## 六、最终建议

**Reject。** 当前稿件最适合作为内部研究总账和未来计划，而不是提交到顶级综合数学期刊的定稿。作者需要先在五层依赖中的至少一层取得一个新的、具体、非条件、可独立验证的主定理，再围绕该定理重写一篇新论文。