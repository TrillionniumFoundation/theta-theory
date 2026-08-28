# θ-Theory：面向数学四大的论文拆分架构

**日期：** 2026-08-28  
**依赖基线：** `THETA_DEPENDENCY_CLOSURE_REPORT_2026-08-28.md`  
**结论：** 建议形成 **4 篇旗舰论文 + 1 篇 representation companion**，而不是沿用当前“response / HJB / representation”三篇粗拆分。

## 0. 总原则

数学四大通常不会因为一个项目覆盖层级多而自动提高评价；相反，每篇稿件必须有：

1. 一个可以一句话说清的中心定理；
2. 一个不可替代的新数学机制；
3. 完整、独立、无条件或作用域极清楚的 actual theorem；
4. 不依赖另一篇未公开草稿中的 unnamed interface；
5. 对领域外编辑也可见的概念后果。

因此不得把 compiler、packet schema、HJB、filter、FBSDE 和所有应用塞进一篇 200 页 monograph；也不得把一个中心证明切成大量互相依赖的短稿。

---

# 1. Flagship I：Moving Singularities, Bilateral Graph Currents and CM2/U3

## 建议题目

**Bilateral graph-current mixing and higher response for dynamical systems with moving singularities**

## 核心内容

- same-occurrence graph-current atlas；
- reverse/source 与 forward/target 双侧 recovery；
- crossed-envelope strict rate gap `AB > CD`；
- product-tail CM2；
- finite-DQ `l1(N^2)` convergence；
- CM2 atom ledger 到 U3 joint Cauchy；
- refinement/coarea/vertex/seam invariance；
- unrestricted universal CM2 的精确 no-go/maximality；
- 至少一个 `K != 0` actual moving-singularity class；
- 若完成，加入 nonconjugate specular Sinai actual class。

## 一句话中心定理

> 对满足可逐字段验证的双侧 recovery 与严格 rate-gap 条件的 moving-singularity systems，graph-current parameter derivative 具有绝对可和的双时间 product tail，并由此得到三阶 spectral response；该条件在最大性意义下不能由局部几何自动删除。

## 建议篇幅

`80–130` 页，proof appendices 可另放 online supplement，但核心 graph-current 和 U3 proof 必须在主稿。

## 四大定位

- 若含 **nonconjugate specular dispersing billiard** 的 actual theorem：优先 `Annals / Acta / Inventiones`；
- 若只有 packet theorem + pinball/scoped examples：更像强专业期刊稿，不宜直接以四大为唯一目标。

## 不应放入

- HJB；
- filtering/game；
- BSDE/PPDE；
- K2 rough homogenization。

---

# 2. Flagship II：Pressure, Suspension Resolvents and Physical Diffusion Response

## 建议题目

**Higher pressure response and physical diffusion for suspensions over moving-singularity dynamics**

## 核心内容

- `C^3` twisted transfer spectral jet；
- pressure and reduced resolvent Kato formulae；
- physical-time implicit root `P(a,q,Lambda_a(q))=0`；
- low-frequency suspension resolvent via roof-cell/renewal reduction；
- Green–Kubo = pressure Hessian = martingale bracket；
- physical diffusion response formula；
- Banach-bundle stabilization/common operator realization；
- `(x,p)` coefficient lift；
- spectral non-coboundary criterion and uniform ellipticity。

## 一句话中心定理

> 三阶 moving-singularity response 控制物理时间压力根与低频悬挂 resolvent，从而给出物理扩散矩阵及其参数响应，并在固定共同算子空间上生成光滑一致椭圆的 `(x,p)` coefficient field。

## 建议篇幅

`70–110` 页。

## 四大定位

- `Inventiones / JAMS` 最匹配；
- 若 common-space stabilization 与 physical-time root 形成跨领域的完整新框架，可冲 `Acta`。

## 不应放入

- general filtering；
- two-player game；
- representation calculus。

---

# 3. Flagship III：Doob-Selected Rough Homogenization and theta-Expectation

## 建议题目

**Doob-selected rough homogenization and nonlinear expectations from deterministic fast dynamics**

## 核心内容

- frozen Doob selector；
- uniform martingale-coboundary package；
- enhanced rough WIP and area anomaly；
- initial-law forgetting；
- parameter switching/freezing；
- nonautonomous rough homogenization；
- effective HJB for uncontrolled/one-player control；
- comparison and theta-expectation semigroup；
- explicit nonconvex/non-subadditive example；
- actual billiard/Lorentz instantiation using Flagship II coefficients。

## 一句话中心定理

> 一个由 deterministic hyperbolic dynamics 产生、由外生 cotangent signal Doob-selected 的非自治系统，在 rough-path 层均质化为状态依赖扩散，并生成一个一般非凸、非次线性的 time-consistent theta-expectation。

## 建议篇幅

`80–120` 页。

## 四大定位

- 若 theorem 同时解决 uniform enhanced WIP、nonautonomous homogenization 和新的 nonlinear expectation class：`Annals / JAMS / Inventiones`；
- 这是整个项目最有可能成为对外“旗舰叙事”的一篇。

## 不应放入

- partial observation filter 的全部 proof；
- simultaneous two-player Isaacs；
- 2BSDE/PPDE representation 的完整技术。

---

# 4. Flagship IV：Filtering, Games and Isaacs Limits

## 建议题目

**Filtering and Isaacs limits for partially observed deterministic multiscale games**

## 核心内容

- hidden fast dynamics 的 prediction contraction；
- posterior/prediction moment balls；
- weighted Bayes contraction and observation-spacing gate；
- strategy-tree-uniform belief collapse；
- sequential lower/upper values；
- simultaneous mixed game；
- mixed Isaacs equality；
- pure saddle 的额外判据；
- belief-state HJB / path-dependent DPP；
- weighted comparison and uniqueness。

## 一句话中心定理

> 对部分观测的 deterministic fast game，filter stability 与 rough homogenization 可在策略树上一致组合；sequential 与 simultaneous limits 必须分型，而 relaxed simultaneous game 在明确条件下产生 mixed Isaacs 极限。

## 建议篇幅

`70–110` 页。

## 四大定位

- 若 belief collapse、deterministic fast dynamics 与 Isaacs limit 的组合确为首次：`Acta / Annals / JAMS`；
- 若主要是已有 filter/game 技术的组合，应转向概率或控制顶刊，而不是勉强冲四大。

---

# 5. Companion V：FBSDE / PPDE / Path Evaluation

## 建议题目

**Representation calculus for theta-expectations: BSDEs, PPDEs and calibrated path evaluations**

## 核心内容

- representation 永远后于 HJB/theta semigroup；
- Markov semilinear branch -> FBSDE；
- controlled HJB -> controlled/randomized BSDE；
- fully nonlinear second-order branch -> 2BSDE/nonlinear martingale problem；
- belief/history branch -> PPDE；
- payoff-calibrated linearization；
- gradient `p` 与 BSDE integrand `Z` 的转换；
- sign/orientation ledger；
- path evaluation and Girsanov only under the corresponding typed assumptions。

## 建议篇幅

`35–70` 页。

## 投稿定位

除非产生新的 representation theorem，否则不应作为四大主攻稿。更适合作为 Flagship III/IV 的 companion，投概率、随机分析或控制强刊。

---

# 6. 为什么不是现有三篇

当前三篇结构的问题是：

1. `response-theory` 同时承载 actual theorem、conditional calculus、no-go 和 future-flow boundary，主贡献不聚焦；
2. `theta-expectation-hjb` 导入的 Paper 1 interface 曾包含已降级或未导出的 theorem labels；
3. `representation-calculus` 只有很薄的 article body，却承担 FBSDE/Girsanov/finance 等多个方向；
4. CM2/U3 与 K1/K1.5 之间的重大数学突破没有成为独立论文中心；
5. K2 rough homogenization 和 K3 filtering/game 被压成下游接口，无法形成四大级别的可见贡献。

新的 `4+1` 结构使每篇只有一个主定理群，同时完整覆盖依赖链。

---

# 7. 激进与稳健两种投稿组合

## 7.1 稳健方案：5 篇

```text
I   CM2 + U3
II  K1 + K1.5
III K2 + HJB/theta
IV  K3 filtering/games/Isaacs
V   FBSDE/PPDE/path representation
```

这是推荐方案。

## 7.2 激进方案：3 篇超长旗舰 + 1 companion

```text
A  CM2 + U3 + maximality
B  K1 + K1.5 + K2 + theta-HJB
C  K3 filtering/game + belief/path PPDE
D  representation companion
```

只有在所有 actual system packets 已完整、且每篇主稿仍能保持清晰时才采用。否则容易重新退化为 monograph。

---

# 8. 四大投稿顺序

推荐顺序：

1. 先完成 Flagship I，锁定最底层不可替代 theorem；
2. Flagship II 只引用 I 的正式 theorem/preprint，而不是私有 inventory；
3. Flagship III 只引用 II 的 coefficient theorem；
4. Flagship IV 可与 III 并行，但不应反向作为 III 的证明输入；
5. Companion V 最后提交。

不要同时向不同期刊提交同一工作或高度重叠版本。JAMS 当前 author guidance 还限制作者在任意 12 个月内通常最多提交三篇，因此更不应把项目切成大量同时投稿的小稿。

---

# 9. 四大级别的最低门槛

每篇在进入四大 submission queue 前至少需要：

```text
one-sentence theorem
complete actual system class
no conditional import from an unpublished private draft
full theorem dependency map
hostile expert review
independent proof audit
clean bibliography and novelty comparison
no process/provenance language in the manuscript
no hash/verifier result presented as mathematical proof
```

此外，Annals of Mathematics 在 2026-08-24 生效的官方 AI/LLM policy 要求人类作者对全部内容、正确性和引用承担责任；若 AI/LLM 贡献了 idea，应说明该 idea 及其在论文中的位置。该项目的最终投稿稿件必须按当时目标期刊政策进行透明披露，且每一条证明需由作者逐行人工复核。
