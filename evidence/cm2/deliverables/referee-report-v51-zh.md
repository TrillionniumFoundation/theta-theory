# Referee Report on *The Two-Time Moving-Defect Problem for Dispersing Billiards* (v51)

## 编辑建议

**Reject in present form; encourage resubmission only as a fundamentally new manuscript.**

这不是一次常规 major revision 能解决的问题。稿件研究的问题重要，局部技术也有价值，但标题所指的 moving-billiard CM2 结论尚未在任何明确、非空的标准 full-boundary dispersing-billiard 类上得到无条件证明。当前最强的全局结果是一个高度条件化的 assembly implication；其最困难的算子微分、非集中、physical/source 匹配、乘积时间衰减及浅/深尾一致可积性，均以 interface/gate 的形式进入假设。补齐这些输入会新增论文的核心数学，而不是补写证明细节。

## 审阅范围与客观核查

- 审阅对象为 `deliverables/cm2-bridge-note-v51.tex`。
- 源文 13,505 行，约 68,000 个空格分词；编译后为 157 页。
- 摘要约 2,110 词（L36–259）。全文有 198 个 definition/theorem/proposition/lemma/corollary/remark 环境和 709 个标签。
- 核心 “Conditional pathwise quantitative CM2 criterion” 到 L8842 才出现，约为 PDF 第 101 页。
- LaTeX 可正常编译；第二遍后没有 unresolved references。
- 我运行了随稿的 `cm2_fixed_section_qnl_cert.py`，它确实精确复现了 pilot 的 \(\mathfrak A=-325/72\)、determinant-one identities 和 noncoaxial eigenline obstruction。因此以下意见不是基于排版失败或代码无法运行，而是针对主结果的逻辑内容与可发表性。

## 论文试图完成什么

稿件的目标是对移动散射体产生的 first transfer-operator defect 证明二时间估计
\[
|\langle Q^nK_VQ^mg,f\rangle|
\le C\tau^m\vartheta^n\|g\|_{C^r}\|f\|_{C^r},
\]
从而控制无限 correlation susceptibility 的逐项微分与双重求和交换。作者将 defect 拆成 regular、graph face、product-current 和 response 四种类型，并建立一套 stopping/tree/source/clock/energy/recovery bookkeeping，最后在 H1–H5 下组装 CM2。

这个研究方向有潜在顶刊价值；问题是本文尚未把这套架构闭合到一个真正的 moving billiard theorem。

## Major comments

### 1. 没有 nonvacuous billiard CM2 主定理

文章自己对此披露得很诚实：

- 摘要明确说 global block atlas、aggregate marked-depth ledger、all-depth weighted PPE，以及 fixed section 到标准 full-boundary collision map 的转移均未证明，并且不提出无条件 generic circular-table 或 relative-translation 结论（L253–257）。
- relative-translation theorem 最后仍要求 “all remaining hypotheses” 全部成立，并明确称自己是 “an interface reduction, not a nonvacuity theorem”（L10423–10432）。
- fixed-section pilot 的 complement-of-entry-box ledger 及其 all-depth atlas、terminal jet、matching、recovery ledger 仍只是 certification target（L11950–11978）。
- 即使 `FS_CERT` 将来成立，所得也是 fixed-section CM2，不是论文开头定义的标准 full-boundary collision map（L11937–11948）；这两个对象之间的五重 bridge 仍未证明（L12182–12196）。

所以，若标题被理解为“解决 moving dispersing billiards 的 CM2 问题”，主张没有证明；若只理解为抽象充分条件，则需要重新定位，并证明这些条件显著弱于结论、数量有限、且至少有一个完整应用。

### 2. 多个核心 interface 已包含结论级输入

这不是单纯“假设很多”，而是部分最困难结论被换名放入假设。

1. `MT_DQ`（L398–617）直接要求差分商的 exact typed decomposition、uniform strong bounds、limiting operator、response convergence、face-current BL\(^*\) convergence、boundary tightness 以及 moving-test convergence。对 moving singularities 而言，这正是算子微分存在性的核心。
2. `FACE_TIME_CM2` 直接假设 propagated master envelope 以 \(e^{-c\max\{m,n\}}\) 衰减，并假设 pairing 由该质量控制（L710–729）；Lemma L839–863 随后主要只做求和和 \(\max\{m,n\}\ge(m+n)/2\)。
3. 替代的 `FACE_TIME_REC` 仍直接假设 recovered cells 的 centered correlation exponential bound 和 unrecovered exponential tail（L752–832）。
4. `FACE_2CUT` 直接要求没有 \(|s|^{-1}\) 损失的 positive per-depth estimate（L624–690）；这正是 growing-depth uniform integrability 的困难部分。
5. `PPE_N` 直接要求 actual-SRB prescribed-depth polynomial small-ball、amplitude-tilted small-ball、conditional mark moments 和 finite-\(s\) uniformity（L2966–3092）。
6. `SHCOL_env`、`TAIL_env+` 和 `NREC_deep` 又输入了浅层/深层所需的指数尾与 recovery-weighted 同阶尾（L7625–7845）。
7. `PHYS_TEST_LIFT`、`PHYS_TREE_MATCH`、`PROP_Q_MATCH` 要求抽象 source tree 与实际 physical current 之间的 exact scalar identity、exact Radon–Nikodym identity、record-preserving pushforward 和 propagated domination（L4203–4230、L8514–8697）。这正是抽象 bookkeeping 能否控制真实 billiard current 的关键桥。

最明显的是 `FS_CERT` 的 FS8：它直接要求 FS1–FS7 尚未提供的所有 H1–H5 条件成立（L11872–11889），然后 completion theorem 再由 `FS_CERT` 推出 fixed-phase CM2（L11937–11947）。逻辑上这是一个真命题，但几乎没有 nonvacuity 内容，且 “certificate/completion” 的命名容易让读者误以为具体模型已经认证完毕。

### 3. 至少有一个进入主证明的实质性错误

Proposition “Local scaled physical face density”（L5948–6007）从 normalized density 与
\[
[\log\widehat\rho_Q]_\alpha\le C\operatorname{Mark}(Q)
\]
推出
\[
C^{-1}\operatorname{Mark}(Q)^{-1}
\le \widehat\rho_Q\le C\operatorname{Mark}(Q).
\]
按书面假设，这个 polynomial lower bound 不成立。取 \([-1,1]\) 上归一化密度
\[
\rho_L(u)=\frac{L e^{L(u-1)}}{1-e^{-2L}}.
\]
则 \([\log\rho_L]_1=L\)，故可令 \(\operatorname{Mark}\asymp1+L\)，但
\[
\inf\rho_L\asymp Le^{-2L}\ll(1+L)^{-1}.
\]
归一化与 log-Hölder 常数至多给出指数型 ratio control；要得到稿件中的 polynomial two-sided bound，必须额外加入 uniform distortion，或把 Mark 定义为包含相应指数。该 proposition 被主定理 H5（L8976–8979）、central phase estimate（L6302–6330）和 off-diagonal mapping（L7191ff.）调用，不能视为无关旁支。

### 4. 还有三处明确的书面 correctness gaps

- **Observable multiplier（L7153–7188）**：证明取 \(C_m=2\|g\|_\infty\)，但正密度的 log-Hölder 常数包含 \([g\circ T^{-m}]_\alpha/\|g\|_\infty\)，不受声明的、与 \(g\) shape 无关的 bound 控制。取 \(C_m\asymp\|g\|_{C^\alpha}\) 可修复这一部分。此外从 \(H_0\le Ce^{\chi m}\operatorname{Mark}\) 进入固定 cone 的时间还应包含 \(O(\log\operatorname{Mark})\)，不仅是 \(O(m)\)。
- **Mixed-cylinder criterion（L1369–1388）**：证明直接写 \(\widehat K=\sum_{i,j\ge1}D_i^-D_j^+\widehat K\)。这需要 past/future conditional expectations 的适当 commutation、两套 filtration 的 exhaustivity，以及目标 projective norm 中的收敛；书面假设没有这些条件。double centering 本身不推出该双 martingale expansion。
- **Fourier reduction（L1431–1470）**：命题假设没有 low-frequency cylinder-mixing 输入，证明 L1457–1460 却直接调用 “centering and cylinder mixing”。作者说明该 preliminary proposition 不用于最终证明，但错误的正式命题仍应修正或删除。

另外，\(\mathcal U_0\) 在 L1141–1160 使用而未定义；\(Y_+\) 的 norm 到 L1193 才被 “schematically” 描述，却已进入前面的正式 bridge theorem。这些属于可修的形式问题，但也说明现稿尚未达到可逐项核验的定稿状态。

### 5. 论文开头的对象与 concrete pilot 的对象并不相同

开篇只处理固定 component-mass vector 的 gauge，并排除独立半径变化、一般独立边界模态、second shape defects 和 unassembled point atoms（L263–307）。固定-gauge operator CM2 也不等于 material/Eulerian physical susceptibility；后者需要另一个 observable-transport theorem（L618–621）。

随后 concrete pilot 改为 Stenlund fixed section。稿件自己指出它不是标准 collision map（L12182–12190）。因此当前标题、摘要和 theorem naming 容易让读者高估结论范围。scope 限制应在标题、摘要第一段和主定理之前明确出现。

### 6. 创新贡献尚未从 proof ledger 中分离出来

本文可能真正有独立价值的模块包括：

- stable-leaf cone control 不控制 transverse trace 的局部反例（L1044–1087）；
- graph current 与 marginal product-current 的类型区分及 double-centering bookkeeping；
- recovery-window summability、three-region reduction 和 global incidence Cauchy；
- regular tangency 的 square-root gluing/current tightness；
- rational pilot 上精确 QNL witness \(\mathfrak A=-325/72\) 及局部 finite-type seed；
- bounded roof 不自动转移 phase CM2 的反例。

但这些模块尚未被组织成一个清晰的、已完成的新定理。特别是 exact QNL script 认证的是局部 algebraic seed，不是 all-parent weighted PPE，更不是 global CM2 certificate。

### 7. 现有篇章结构阻断正常外审

摘要长约 2,110 词，之后没有 Introduction，而是直接进入 “The exact target”。主定理在约第 101 页；依赖总表到 L12284 才出现；最后还有 133 个 obstruction tests（L12447ff.）。全文混合了 theorem、assumption、research gate、countermodel、proof audit 和未来工作，读者很难判断一个 acronym 是定义、已经证明的性质，还是未完成任务。

顶刊版本至少需要：

1. 200–250 词摘要；
2. 6 页以内的 Introduction，清楚列出 novelty 和 literature gap；
3. 第 1–2 页提供 “proved / assumed / open” 状态表；
4. 主定理置于前 10 页，并在其前给出依赖图；
5. Definition 只定义对象，把 decay/moment/convergence 条件改列为 Assumptions；
6. 删除大部分工程式 acronym；
7. 把 marked-kernel/clock ledger、133 tests 和未完成 programme 移至 companion note 或在线 supplement。

## 优点

- 作者对 moving singularity 中可能出现的类型错误、错误 conditioning、moving-depth 极限和假 cone bridge 非常敏感。
- 文稿对“文献提供什么、本文证明什么、什么仍未完成”总体上相当诚实。
- exact pilot geometry、局部 block-current assembly 和 QNL seed 是可信且可能有后续价值的技术基础。
- 计算证书采用 exact arithmetic，实测可运行，不依赖数值容差。

这些优点支持“完成后值得重新审视”，但不足以改变当前编辑决定。

## 建议的重构路线

作者必须二选一：

### 路线 A：真正的应用定理

在一个明确非空的标准 full-boundary moving-billiard 类上，闭合至少以下输入：

- `MT_DQ` 的 moving-face difference-quotient existence/convergence；
- all-depth weighted PPE；
- global block-current atlas 与 physical/source exact matching；
- face-time product decay；
- shallow/deep marked recovery ledger；
- fixed-section 到 full-boundary map 的 response transfer。

然后给出无条件 CM2，并明确推出相应 susceptibility/linear-response theorem。

### 路线 B：抽象 assembly theorem

把条件压缩成少数几个自然、互相独立、可验证的数学假设；证明一个 40–60 页以内的抽象定理；至少给出一个完整非平凡应用。删除所有暗示 concrete nonvacuity 已完成的 theorem/certificate 命名。

explicit pilot/QNL、长篇 kernel ledger 和 obstruction catalogue 可分别成为 companion papers 或 supplement。

## 给编辑的最终判断

这是一份技术上非常认真、也很有研究潜力的 working note，但不是一篇已经完成的 top-journal article。核心缺失与真实 correctness gap 都不是局部修订可解决的。我的建议是 **reject rather than major revision**；只有在补齐 nonvacuity、修正上述命题并彻底拆分重写后，才适合作为新稿重新投稿。
