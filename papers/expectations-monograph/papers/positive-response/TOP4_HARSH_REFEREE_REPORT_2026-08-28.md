# 顶级综合数学期刊标准严苛审稿意见

## 稿件识别

- 稿件：`cm2-bridge-note.tex`
- 标题：*The Two-Time Moving-Defect Problem for Dispersing Billiards — Pair-safe selection lifts, occurrencewise propagated currents, product-time face control, global incidence Cauchy, two-cutoff convergence, and a strongly conditional pathwise CM2 criterion*
- 稿件自标版本：2026-07-14，version 50，`Working note`
- 审阅仓库快照：`main` at `08aac05e51577bcd2f2ec5a6aef2a960a8d3ef9d`
- 审阅日期：2026-08-28
- 编辑建议：**Reject / not suitable for peer review as a journal article。当前文件不是 controlling mathematical manuscript，而且其正向结论的实际 nonvacuity 未建立。**

## 一、给编辑的结论

这份文件不能按普通论文审稿，首先因为它不是仓库的最新数学状态。目录中的 TeX 仍是 version 50；仓库 controlling stage 已经是 v82/v83。最新控制索引明确记录：

- `UnrestrictedUniversalMovingScattererCM2: REFUTED_EXACTLY`；
- `LocalGeometryOnlyUniformCM2: REFUTED_BY_ACTUAL_BILLIARD_SPECTRAL_OBSTRUCTION`；
- `UMS_v3_PacketizedUniversalImplication: PROVED`；
- `ActualUniformAdmissibleClasswideCM2: ACTUAL_LOCAL_PACKETS_REQUIRED`；
- `AllPositiveActualInstantiationGapsClosed: false`；
- `V79ActualPromotion: WITHDRAWN_LATEST_WINS`；
- `FormalCredit: 0`；
- `ExternalPeerReview: NOT_PERFORMED`。

因此，version 50 的 theorem posture 已被后续工作实质改写：universal positive claim 被反驳，local-geometry-only 路线被实际谱障碍阻断，剩余正结果是 packetized conditional implication，而 actual local packets 尚未构造完成。一个被后续 canonical tree撤回或降格的旧 working note不能作为投稿稿件。

即使只按 version 50 自身审查，正文也不是一个已经实例化的 CM2 theorem。摘要明确把最困难的估计作为 primitive inputs：actual-SRB physical polynomial escape、native stopping、complete weighted energy、joint cemetery moments、parent-kernel reverse-Hölder、selection-safe occurrence/carrier likelihood、endpoint upper-scale tails、product-time positive face envelope或 recovered signed core、two-cutoff face convergence、normalized shallow/deep recovery、pathwise jet tails等。若这些输入成立，后续 global Cauchy / Tonelli / dominated convergence bookkeeping可能产生 CM2；但这些输入正是需要对实际台球证明的主要内容。

稿件还明确承认 fixed-section two-disk pilot没有证明 global block atlas、rare-cell regularity、all-depth weighted PPE，也没有证明从 fixed section到标准 full-boundary collision map的 transfer。故当前结果是一个极其复杂的条件性 compiler，而不是 dispersing billiards 的正向 CM2 theorem。

我的建议不是 major revision，而是停止把 version 50 当作论文。作者应从 v82/v83 控制树中提取一个稳定、有限、可审的数学结果：最可能是精确反驳 theorem、谱障碍 theorem，或 packetized abstract implication。任何正向 actual CM2 论文必须先给出至少一个明确物理 table family的 local packet实例。

## 二、可能有价值的内容

1. 稿件正确意识到 two-time moving defect不能由单时间 cone trace estimate或虚构的 nuclear graph-current表示自动控制。
2. 区分 current centering与 test-side adjoint、概率 bad-event clock与 additive source incidence、weak convergence与 uniform majorant，是概念上必要的。
3. 采用 complete positive tree、first-failure cemetery labels、occurrence-marked source space和 global incidence Cauchy，试图避免逐 occurrence开平方和重复计数，方向上有一定价值。
4. 稿件明确指出 fixed negative-pressure subsystem不能由 conditional normalization产生 full physical cover，这一纠错是重要的。
5. two-cutoff策略、low/intermediate/ultra-high Fourier分区和 endpoint upper-scale ledger，可能成为未来实际证明的一部分。
6. 后续 canonical stages得到的“universal claim精确反驳”和“actual billiard spectral obstruction”，若证明完整，可能比旧正向 working note更接近可发表结果。

这些优点目前被版本失效、假设堆叠和 actual nonvacuity缺失所压倒。

## 三、致命问题

### 1. 投稿文件不是 source of truth

`cm2-bridge-note.tex` 自标 version 50，而仓库采用 `LATEST-WINS / FAIL-CLOSED / NO-FALSE-CM2-CLAIM`，controlling substantive stage为 v82。任何审稿必须以 controlling theorem statement为对象；否则审稿人可能接受一个后来已被作者自己反驳或撤回的命题。

最低要求是：

1. 删除或明确 archive version 50；
2. 从 v82/v83重建一份单一 LaTeX 稿；
3. 在标题页列出 exact theorem status；
4. 删除所有 withdrawn promotion；
5. 明确区分 exact source、reconstruction和 chronology-only material。

在这一步完成前，数学审稿没有稳定对象。

### 2. 正向 theorem 的假设几乎就是 CM2 本身

摘要列出的 primitive interfaces包含：

- exact actual-SRB physical polynomial escape at prescribed depth；
- pair energy derived from an exact unselected product reference；
- complete weighted-energy tree及 full-product `L^{p_W}` moment；
- joint cemetery-envelope moment；
- normalized parent-kernel reverse-Hölder on every frozen parent；
- source-incidence complexity gaps；
- selection-safe joint occurrence--carrier likelihood；
- post-propagation carrier domination；
- exhaustive main-clock coverage；
- endpoint upper-scale tilted survivor tail；
- product-time positive face envelope，或 recovered signed core加 unrecovered positive tail；
- normalized shallow/deep recovery moments；
- pathwise jet-tail / Remez-valency条件。

这些不是容易验证的局部几何条件，而是对长时间、两时间、选择后、倾斜后、source-weighted dynamics的精确大偏差与恢复估计。它们的联合强度与目标 CM2 majorant非常接近。

作者必须给出一张严格的 non-circularity table：每个 assumption从哪些更原始、独立、已证明的台球定理推出；不得把“存在 uniform CM2 envelope”“所有 selected source tails可和”换名后作为 hypothesis。当前 manuscript没有完成这一证明。

### 3. actual-SRB physical polynomial escape 是核心开放门，而非技术输入

稿件正确否定了从 fixed negative-relative-pressure clean subsystem推导 physical cover的错误路线，随后直接假设实际 SRB 下所需的 physical polynomial escape。这个 estimate恰恰控制高频相位的 near-stationary set，是整个 central band argument的核心。

“Leclerc native coordinate + cutting modulo fixed-degree polynomials”只能提供局部或条件结构；要得到 moving billiard在 logarithmic resolving depth上的 uniform actual-SRB estimate，还需处理：

- singularity cuts和 homogeneity itineraries；
- parameter-dependent phase jets；
- bad return/grazing cells；
- branch complexity；
- selection bias与 source weighting；
- all contexts的 uniformity。

在没有实际证明时，CM2 theorem只是 conditional on the missing CM2 mechanism。

### 4. parent-kernel reverse-Hölder 与 joint cemetery moments没有实际来源

稿件区分 global complete-tree moment和每个 frozen parent上的 conditional reverse-Hölder，这是正确的；但后者强得多。它要求在实际、split、cemetery、source-incidence parents上，对归一化 kernel统一控制条件尾部。

同样，joint cemetery-envelope moment并不能由各 marginal `L^p` bounds自动推出。稿件把这两项列为 interfaces，却没有从 billiard coupling、distortion或 growth lemma导出。它们正是 selection后避免指数损失和 source likelihood爆炸所需的关键。

若无 actual proof，后续 Hölder degradation和 global Cauchy只是形式上正确的 bookkeeping。

### 5. product-time face control仍被作为假设

标题突出“product-time face control”，但摘要最终要求：

“either a product-time positive face-envelope or a recovered signed core with an unrecovered positive tail”。

这不是对 product-time face term的证明，而是把两种足以控制它的结果作为备选输入。对于真正 moving physical face，构造这样的 envelope / recovered core正是双时间难题。

应当把论文主定理改写为明确的 abstract implication：若存在 P1--Pk packet，则 CM2成立；然后单独证明一个实际 packet。没有后者，不应在标题中声称解决 dispersing billiards的 two-time moving-defect problem。

### 6. fixed-section pilot不能支撑 full collision-map theorem

摘要承认 two-disk fixed-section pilot只证明：

- typed direct/entry/exit block product rule；
- artificial tangency trace cancellation；
- positive-mass local entry/exit current；
- compact incoming fibres到 initial standard families。

同时明确没有证明：

- global block atlas；
- rare-cell regularity；
- all-depth weighted PPE；
- fixed section到 standard full-boundary collision map的 transfer。

这些缺口会影响 every-depth branch ownership、endpoint labels、return phases和 source incidence。局部 pilot不能作为 actual moving-scatterer CM2 nonvacuity example。

### 7. relative translation只“reduce to gates”，没有通过 gates

稿件对 fixed-radius relative translation声称将六个最难 interface降到三个 geometric gates：prescribed-depth jet/rough gate、exact coarea physical/source likelihood、oriented face recovery with weighted tails。把 blocker压缩为三个 blocker不是证明。

要构成正例，作者必须为一个具体 table、明确参数区间、所有 relevant branches证明这三个 gate，给出可检查常数和 strict exponent window。当前没有。

### 8. measure-trivializing gauge施加了强而不透明的范围限制

正文要求每个 collision component的 normalized mass vector保持不变：

`|∂O_{s,i}| / sum_j |∂O_{s,j}|` independent of `s`，

以构造 `A_s^* mu_s=mu_0`。这对 fixed-radius translations可以成立，但对一般 radial deformation或独立 scatterer shape changes通常不成立。因而 theorem scope远窄于“genuine motion of dispersing scatterers”。

作者必须明确：

- 哪些物理 deformation满足 component-mass constraint；
- 若不满足，product-current correction如何改变；
- gauge choice是否影响 CM2 object；
- 是否可通过额外 density conjugation处理 mass transfer，而不是排除大部分 family。

### 9. two-cutoff convergence依赖所有常数在 `L(s)~log(1/|s|)` 下统一

从 fixed finite singularity refinement过渡到 growing depth需要：

- difference quotients在弱 current topology逐项收敛；
- boundary mass对 branch-generated tests统一；
- intermediate triangular band有 `s`-uniform positive coarea/return bound且无 `|s|^{-1}` loss；
- deep remainder在增长 depth下仍可和；
- shallow/deep recovery的 normalization constants统一。

稿件把这些内容分散成 multiple interfaces。若任一常数随 depth增长，dominated convergence就失效。必须给出一个单一 theorem，明确所有指数不等式和 strict margins，并证明存在非空参数区域。当前版本的“clock--passage matrix”主要是 ledger，不是 actual inequality proof。

### 10. analytic / circular pathwise jet-tail条件没有被实例化

稿件承认 qualitative transversality不够，并要求 fiberwise Remez/valency或 circular quantitative jet condition。这是正确的边界；但 finite-branch jet surjectivity不推出 all-depth sublevel estimate。对实际 circular table，需要证明相位随完整 itinerary的 jet不退化，并控制 grazing/return singularities。

当前只是保留“circular families retain the quantitative jet condition”。这仍是 assumption，不是 circular-table theorem。

### 11. source kernels的 measure-theoretic architecture与实际 transfer current之间缺少识别定理

standard-Borel marked source space、positive component kernels、Radon--Nikodym carrier ratios和 occurrence-constant polarity可以防止抽象计数错误。但必须证明每个真实 finite-difference defect都可唯一或至少一致地嵌入该 architecture，并且：

- decomposition可测；
- envelope integrable；
- polarity不会因 branch refinement改变；
- owner partition与 resolution clock覆盖全部 current mass；
- recombination精确恢复原 operator quotient；
- 不同合法 decomposition给出同一 bound。

当前大量定义和 ledger没有替代这一从 billiard operator到 marked kernel的 representation theorem。

### 12. canonical status本身已否定旧 universal posture

最新控制树不是简单说“还差一点”。它说 unrestricted universal CM2被精确反驳，local-geometry-only uniform CM2被 actual spectral obstruction反驳，v79 actual promotion被撤回。任何新稿必须把这些负结果放在主 theorem map最前面。

如果 version 50 的某些 theorem statements与这些 refutations冲突，它们必须删除，而不能依靠“strongly conditional”字样继续保留。条件性陈述只有在 assumptions可同时满足且有 nonempty class时才有数学意义；当前 `AllPositiveActualInstantiationGapsClosed: false` 说明这一 nonvacuity尚未完成。

### 13. hash、archive和 verifier不提供 theorem credit

v83 tree对 source bytes、terminal packages和 manifests的 SHA-256验证很有档案价值，但它只证明文件完整和 provenance一致。它不验证：

- assumption consistency；
- analytic inequalities；
- hidden circularity；
- actual billiard instantiation；
- theorem proof。

控制索引正确写了 `FormalCredit: 0` 和 `ExternalPeerReview: NOT_PERFORMED`。投稿稿件不能把 deterministic verifier、package PASS或 archived exactness写成数学证据。

### 14. 文稿不可读且不可审

标题过长；摘要本身接近一篇报告长度，包含数十个未定义 interfaces；TeX 源约 580 KB，仍标为 working note。一个顶刊 referee需要在前十页看到：

1. 精确定义 CM2；
2. 一个稳定主定理；
3. 最小假设；
4. actual class或明确 nonvacuity theorem；
5. proof architecture；
6. 与已知结果的比较。

当前版本把 theorem、proof ledger、修错历史、未来路线和版本控制混合在一起，无法进行标准同行评审。

## 四、可发表性拆分建议

### A. 最可能立即形成论文的负结果

从 controlling v82/v83提取：

- unrestricted universal moving-scatterer CM2 的精确反例/反驳；
- local-geometry-only uniform CM2 的 actual billiard spectral obstruction；
- 为什么 fixed clean subsystem、conditional normalization或 local finite jets不足以给出 physical cover。

若这些证明自足、反例具体，这可能是一篇清楚且重要的 obstruction paper。

### B. 抽象 packetized implication

将 `UMS_v3_PacketizedUniversalImplication` 写成纯抽象 theorem：

- 只保留有限 packet list；
- 明确每个 packet的输入/输出空间和常数；
- 证明 compiler无循环；
- 给出 sharp exponent inequalities；
- 不声称 actual billiards已实例化。

这可以作为技术框架，但 venue和影响力需按抽象新意判断。

### C. actual positive paper

必须首先完成一个明确 family，例如 fixed-radius relative translation或具体 circular deformation，并证明：

- actual-SRB PPE；
- source likelihood / carrier domination；
- parent-conditional moments；
- product-time face packet；
- shallow/deep recovery；
- full-boundary transfer；
- strict common exponent window。

只有此时才能宣称 moving-scatterer CM2 正定理。

## 五、最终建议

**Reject / not a reviewable journal manuscript。** version 50 已被仓库自己的 v82/v83 controlling status实质取代；其正向结论仍以等价强度的 long-time packets为假设，且没有 actual billiard实例。建议废止当前投稿形态，从最新控制树中重新提取一篇稳定的负结果或严格限定的 abstract packet theorem。