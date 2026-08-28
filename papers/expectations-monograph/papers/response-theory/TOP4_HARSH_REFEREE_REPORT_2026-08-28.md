# 顶级综合数学期刊标准严苛审稿意见

## 稿件识别

- 稿件：`main.tex`
- 标题：*Conormal Source Modules, Recovery, and Obstructions for Finite-Horizon Dispersing Billiards with Moving Singularities*
- 审阅快照：`main` at `08aac05e51577bcd2f2ec5a6aef2a960a8d3ef9d`
- 审阅日期：2026-08-28
- 编辑建议：**Reject in present form。可以在实质性拆分、降格主张并补足一个真正非共轭正例后，以新稿重投。**

## 一、给编辑的总体评价

这篇稿件是五篇中数学边界写得最诚实的一篇。作者明确区分：

- Demers--Zhang 型 dynamical strong bundle `B_U` 上的实际谱间隙；
- 只用于 parameter traces、并不声称 transfer invariant 的 positive flux-seed scale `D_U`；
- label-resolved conormal source module；
- complete assembly 后的 strong recovery；
- conditional S1--S3 abstract propagation；
- continuous-time moving-family theorem 尚不存在。

稿件也给出若干可能有价值的负结果：point atoms 不属于普通 weak space、周期点原子妨碍 generic decay、moving-face gluing defect 的 split surjectivity、有限对称性不能自动给出 Ward cancellation、local primitive 受到无限族 periodic-orbit sums 约束。这些内容若被严格压缩和放进自然函数空间，可能形成一篇有意义的 obstruction paper。

但以当前标题、摘要和“response package”定位衡量，稿件没有证明一般 moving-singularity response。无条件正结果几乎全部来自两类特殊机制：

1. 显式 invariant flux 的一阶/二阶微分，因而 complete source 自动写成 `(I-L) rho_j`；
2. exact conjugacy / rigid translation，使 moving face 在所选 trivialization 中根本不出现。

作者自己承认一般 nonconjugate prescribed correlation source、eventwise re-insertion、双时间 conditional mixing、moving-flow graph domain 和 symbol estimate仍未解决。因而这不是“完成的 moving-singularity response theory”，而是：一个复杂的 source bookkeeping framework、若干二阶不变量恒等式、若干 no-go theorem，以及一个把主要困难列成 certificates 的条件性 appendix。

顶级综合期刊不能接受以大量新定义和 theorem labels 掩盖“核心正定理尚不存在”的状态。我的建议是拒稿，但保留作者将 obstruction 部分重写为一篇短而清楚的新论文的可能性。

## 二、值得肯定的方面

1. 稿件不再把 `D_U` 的强响应范数误称为 transfer invariant，也不再把 point/face currents 送进普通 Demers--Zhang resolvent。
2. 作者明确承认 raw historical terminal labels 可以线性积累，并区分 historical state 与 assembly-first reset。
3. radial reset 的证明不再偷用 generic R3，而是在 assembled current 上利用显式 flux jets 和 grazing mass `O(2^{-4M})`。
4. 对 exact conjugacy、differentiated invariance、independently prescribed source 三类例子的逻辑身份区分得较清楚。
5. no-go 部分试图排除“有限维调参、对称性、局部 Noether charge、有限记忆 label rule”自动产生所需 Ward identity 的可能性。

这些修正提高了诚实性，但也使核心结论的实际有限性非常清楚。

## 三、致命问题

### 1. 标题和主包装仍远强于实际无条件定理

`thm:main_response_package` 的实际内容是 static averages、source-specific radial recovery、assembly-first scalar reset、exact-current / exact-conjugacy benchmarks 和 obstruction。稿件并未证明：

- 对一般 compact moving-scatterer family 的 invariant measure / correlation linear response；
- 对独立指定 smooth observable 的 nonconjugate susceptibility；
- 在 repeated insertion 下闭合的 response module；
- moving-flow 的共同 graph domain、high-frequency symbol theorem 或 regularity-loss theorem；
- Paper 2 所进口的 generic moving-singularity and multi-response package。

因此“response package”只能理解为“若 source 已经通过 complete recovery certificate，则之后如何计算”的框架，而不是证明该 certificate 对物理 response tree 成立。标题至少应改成明确的“source modules and obstructions”，摘要应删除任何可能让读者误以为一般 response 已建立的措辞。

### 2. 最主要的 nonconjugate radial 正例是 differentiated invariance 的代数恒等式

径向膨胀中，稿件使用显式 invariant density jets，并得到

`G_1 = B_1 rho_0 = (I-L_0) rho_1`,

`G_2 = B_2 rho_0 + 2 B_1 rho_1 = (I-L_0) rho_2`。

这当然可以是正确且有用的 current identity，但它并没有解决一般 source recovery：右端 primitive `rho_j` 已由显式 invariant flux 预先给出，所有 face/point cancellation 只需在 complete differentiated invariance identity 中成立。类似地，`thm:radial_table_velocity_benchmark` 明确把 source 定义为 `(partial_s L_s) rho_s`，于是 primitive 又由 `partial_s rho_s` 自动给出，susceptibility 通过 telescoping 完成。

这类例子验证了 bookkeeping 与不变量微分的一致性，却没有构造一个独立指定的 correlation density，也没有证明 singular source 经动力学传播后自行 recovery。把它作为“genuinely nonconjugate response theorem”的主要正证据，会严重夸大数学进展。

### 3. assembly-first reset 回避而非解决 label-resolved dynamical closure

`thm:uniform_postassembly_radial_tail` 先将所有历史 label 组装成

`(I-L_0^N) rho_j`

再嵌入 regular coordinate，并把 terminal coordinate按定义设为零。证明明确承认：raw historical label state 不等于这个 reset state；`S Q` 会忘掉 labels 和 terminal data。

这可以定义一个标量计算协议，但不是原 source process 在模块中的闭合定理。若下一次 response insertion 依赖历史 branch/terminal information，reset 可能改变后续导数。要把它用于无限 susceptibility 或 higher response，作者必须证明：

1. reset 与所有未来物理 insertion 相容，而不仅与当前 scalar pairing 相容；
2. 不同 block decompositions 给出同一结果；
3. reset errors 在所有 future words 上有统一可和界；
4. summable primitive/reset bounds 由实际台球证明，而不是作为 `prop:certified_scalar_assembly_reset` 的输入。

目前 countable assembly-first theorem 把这些关键性质作为条件，因此不能替代 eventwise closure。

### 4. conditional S1--S3 certificates 基本等价于缺失的主定理

`ass:response_scale_dynamics` 前的文字明确说：这些 certificates 不由前面的 fixed-atlas calculation 推出，也不用于 radial reset。S1--S3 所要求的 transfer mapping、triangular recovery、re-insertion / decay 正是一般 moving-singularity response 所需的核心。

在这种情况下，Appendix B 的 abstract implication 是“若已有足够强的响应空间和 recovery certificates，则可递归传播”。这在逻辑上没有问题，但原创性必须与已有抽象 perturbation calculus 比较，而且绝不能作为 Paper 2 的已验证输入。当前三篇论文的 dependency interface 把 conditional theorem 当成 actual theorem，是不可接受的。

### 5. 实际 weighted primitive domain 不具备 transfer invariance

稿件构造了 `L^infinity`-anchored、branch-cocycle-weighted trace orbit domain，并证明 closability、direct-limit refinement 和某些 radial memberships；但它明确不声称 `L`-invariance。没有 invariance 就不能把该空间作为可反复迭代的 response domain。

这会直接限制：

- moving trace 在任意等待长度后的重插入；
- resolvent words 的统一定义；
- higher-order source tree；
- 双时间 correlation differentiation。

作者通过 source-specific complete assembly 规避这一点，但这意味着一般 response theory仍未建立。顶刊不能把一个不能承载目标动力学的 trace space视为完成的 functional framework。

### 6. obstruction 的“genericity”只在定制 graph topology 中成立

split-surjective gluing map、open dense complement 和 infinite-codimension kernel 是稿件最可能有独立价值的内容。但目前这些命题被放在专门构造的 weighted local-potential / Poisson-pullback graph class 上。作者自己声明不对全部普通 `C^r` observables 作 Baire claim。

因此必须回答：

- 该 graph class 在自然 observable topology 中是否稠密、闭合或连续嵌入？
- right inverse 是否对应实际物理 perturbations，而不仅是抽象 trace profiles？
- `E phi - L E phi` 的两根 presentation 是否依赖所选 atlas / extension operator？
- infinite codimension 是在哪个 Banach 空间中的 codimension？换一个等价自然范数是否保持？

如果这些问题没有解决，稿件不能用“generic obstruction”作广泛物理结论。可发表版本应把拓扑限定写进每个 theorem title 和 abstract，而不是只在风险备忘录中说明。

### 7. uniform-family spectral input不能只靠 fixed-table theorem 编号

稿件说 uniform Demers--Zhang input 与 2013 年若干定理逐一匹配。这种 crosswalk 不等于 uniformization proof。对 moving compact family，需要逐项证明共同：

- homogeneity strips、cone constants、one-step expansion、distortion；
- growth lemma 和 complexity bounds；
- strong/weak norms与 compact embedding；
- peripheral spectrum的简单性和 period-one reduction；
- spectral radius / Lasota--Yorke constants的 uniform margin；
- transported fibers之间的可比较性。

如果正文已经有完整证明，应将其压缩成一个明确的 uniform theorem 和逐项 lemma，而不是混在 79 个 numbered environments 中。如果只是引用 fixed-table 结果加 compactness，则不足以排除谱隙在参数族上退化。

### 8. `second_order_poisson_recovery_criterion` 把强 remainder 作为假设

该 proposition 的 sufficiency 依赖

`||(I-L_s)(h_0+s h_1+s^2 h_2/2)-g_s||_{B_U}=o(s^2)`。

这已经是 canonical primitive 二阶可微性所需的主要 operator Taylor estimate。再加上 `q_1,q_2` 已被假设 centered strong 且具有 certified reset，结论几乎是应用 uniform resolvent 的形式推论。它可以作为 criterion，但不能被计入证明实际 physical source 满足二阶 response。

Paper 2 却将类似 result 当作一般 coefficient differentiability engine，这是依赖过度使用。

### 9. exact conjugacy 例子不含 moving-face cancellation

rigid translation 示例在 exact conjugacy trivialization 中使 operator、source 和 primitive 全部固定，`q_1=q_2=0`。作者已经正确说明这不是 moving-face theorem。既然如此，它不能用于证明任何 nonconjugate moving boundary 的 nonvacuity，也不能支撑摘要中一般性的“recovery”印象。

一篇正向 response paper 至少需要一个独立指定 observable，使 moving face真实出现并通过结构性恒等式取消，而不是因坐标共轭消失。

### 10. continuous-time 部分只有边界和 obstruction

题目与应用链需要 suspension flow response，但正文只保留 fixed-table BDL input 和三项 obstruction，并明确没有 moving-family graph-domain / symbol theorem。Paper 2 却声称进口 suspension Laplace contour、smooth deterministic response 和 moving singularity response来定义连续时间 correctors。这一接口不能成立。

若本稿只研究 collision map，应彻底删除 flow-oriented packaging；若要支撑连续时间 HJB，则必须新增实际 moving-family flow theorem。

### 11. 论文体量和结构掩盖主线

67 页、79 个 numbered environments、两个大型 appendix、多个 benchmarks、no-go results、conditional calculus 和 flow boundary塞进一稿，使审稿人难以判断哪些是新定理，哪些是定义、恒等式、criterion 或自我限制声明。编译成功、无 undefined labels、hash 一致都不影响这一数学问题。

建议将稿件至少拆成：

1. **Source-module and obstruction paper**：只保留自然函数空间中的 module、recovery equivalence、point-atom obstruction、gluing/periodic-orbit obstruction；
2. **Radial benchmark note**：明确定位为 invariant-source identities and assembly-first scalar calculus，不宣称一般 response；
3. 将 conditional S1--S3 framework 放入未来真正实例化后再发表。

## 四、逐项定理审查结论

| 结果 | 审稿判断 |
|---|---|
| `thm:primitive_spectral_resolvent` | 需要完整 uniform-family proof，不能仅靠 fixed-table crosswalk |
| `thm:radial_inflation_second_order_recovery` | 可能正确，但本质是显式 invariant flux 微分；意义需降格 |
| `thm:blockwise_second_order_invariant_recovery` | 主要是 differentiated finite-time invariance identity；不是 general source recovery |
| `thm:uniform_postassembly_radial_tail` | 证明的是 assembled scalar tail；没有 historical module closure |
| `thm:countable_assembly_first_susceptibility` | 关键 summability / reset compatibility 仍为条件 |
| `thm:independent_flux_conjugate_correlation_source` | exact-conjugacy consistency check，不是 moving-face正例 |
| `thm:radial_table_velocity_benchmark` | invariance-generated exact current；telescoping benchmark |
| `prop:second_order_poisson_recovery_criterion` | 合理 criterion，但 strong remainder和 recovery 已被假设 |
| gluing / symmetry / periodic-orbit no-go results | 最有潜力；必须在自然 topology 中单独重写 |
| conditional S1--S3 calculus | 不得被下游论文当作实际台球定理 |

## 五、达到可重投水平的最低要求

1. 重新命名并缩小主张；清楚区分 actual theorem、criterion、benchmark、obstruction 和 open problem。
2. 提供一个独立指定、真正 nonconjugate、moving-face 非零的 correlation source，并证明至少一阶 susceptibility，而不是由 invariant identity 或 exact conjugacy 自动 telescoping。
3. 证明未来 insertion 与 assembly reset 的相容性，或明确只做单次/固定块 scalar identity。
4. 将 uniform-family spectral theorem写成可逐项核验的自足证明。
5. 把 obstruction results 移到自然 observable / perturbation topology，或严格限制其解释。
6. 删除 Paper 2 所依赖但本稿未证明的 generic response接口；三篇论文的 theorem labels必须逐条一致。
7. 不要在同一篇文章中同时承载 collision map正定理、flow open problems、抽象 conditional calculus 和全部 no-go machinery。

## 六、最终建议

**Reject。** 当前稿件最强的成果是若干 source-module / obstruction theorem 和显式 invariant-source benchmark；它没有完成一般 moving-singularity response。经过彻底拆分和重新定位后，其中一部分可能成为有价值的专门论文，但当前版本不符合顶级综合数学期刊对主定理强度和概念集中度的要求。