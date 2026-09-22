# General Theta Foundations
## 因果实验、可达信息几何与分类型归约：公理、对象、态射和首批通用定理

**研究总纲 v0.1 · 2026-09-22**  
**性质：建议采用的数学基础规范与详细研究纲要。**

本总纲将可直接证明的基础命题、已有论文中带条件的结果、以及尚需完成的新研究目标分开。它不是期刊录用意见、形式化证明证书，也不声称下列经典概率与统计结果是新发现。新的研究任务在于：把真实可达性、全局及奇异几何、因果实现、有限资源和不同渐近尺度放在同一套明确类型的结构中，并证明有内容的连接定理。

本次源材料基线为 A1 v37 的不可变提交 `90465076589f5e5c69227d624f278c47744f1c1d`、A2 v112 的数学源提交 `0c696736e6ec22259c730672f61ebd8ef0d95460`，以及旧 C2 的历史提交 `c04845b6613208406703695c9c184ae461f95805`。这里固定基线是为了使数学比较可复查，并不据此断言仓库以后没有更新。下文对源稿中的一般定理采用其明示条件；没有把本次接口审阅当作对所有历史证明的重新认证。

---

# 0. 总论：先固定研究对象，再讨论其几何

建议将 General Theta Foundations 的中心问题确定为：

> 在一个明确给定的、可干预且因果的实验中，哪些未来预测能够从真实历史获得；这些预测在全局、局部和奇异处呈现怎样的几何；哪些实验归约能够在明确资源与误差预算下传递预测、推断、压力、率函数和记忆结构？

它不是“所有系统拥有同一个率函数”，也不是“某个矩阵秩决定全部统计与动力学行为”。

基础顺序应为

\[
\boxed{\text{正实验核＋准备机制＋可执行测试＋因果性＋资源接口}}
\]

\[
\Downarrow
\]

\[
\boxed{\text{路径分布、预测商、实际获得的分布和可达集合}}
\]

\[
\Downarrow\quad\text{在不同附加条件下}
\]

\[
\boxed{\text{信息度量、奇异几何、量化曲线、压力、LDP、动力学记忆}}.
\]

这里的“通用”是同一命题适用于满足其条件的一整类对象，而不是任何对象自动具有所有结构。

## 0.1 必须修正的五项简化

**第一，Fisher 信息与协方差不是底层公理中的独立输入。** 它们必须来自已给定的参数化分布或指定随机目标；否则可以任意附加一个矩阵，却没有对应的实验解释。

**第二，导数降秩集只描述一阶退化。** 它不等于全局不可辨识集，也不完整描述高阶接触和有限分辨率困难。

**第三，随机后处理不等于确定性映射。** 随机后处理后的后验通常是原后验的条件重心，而不是原预测集合的逐点像；压力的后拉也一般不是线性的。

**第四，Fisher 信息保留不等于全局充分性。** 需要真实的参数无关恢复核才能作充分性结论。Pollard 对此给出过明确反例和二次均方可微解释。[W3]

**第五，统计信息单调性不自动推出预测内存单调性。** 内存比较必须给出因果模拟器并计入其状态；相对各自完整历史的预测遗憾也不是同一个统计风险。

---

# 1. 术语、类型与量纲

| 记号 | 含义 | 不得混同的对象 |
|---|---|---|
| \(\lambda\in\Lambda\) | 未知模型参数 | 已知校准、随机隐藏状态 |
| \(x_t\in X_t\) | 隐藏物理状态 | 观察者实际保留的编码 |
| \(h_t\in H_t\) | 可见历史，含动作和报告 | 未来报告或未记录的失败 |
| \(\alpha\) | 实验策略 | 对未知真参数有直接访问的规则 |
| \(\pi_t\) | 明确准备/先验下的后验 | 对所有参数同时有效的频率学派统计量 |
| \(s_t\in S_t\) | 对指定未来任务足够的预测状态 | 必然有限维的流形 |
| \(\nu_t\) | 实际准备及探索策略产生的状态分布 | 人为挑选的均匀几何测度 |
| \(\mathcal V_t\) | 未来可执行测试的线性空间 | 自动乘法封闭的交换代数 |
| \(\mathcal I_\lambda\) | 参数 score 的 Fisher 信息 | 任意目标的协方差 |
| \(\Sigma\) | 已指定随机向量的协方差 | 无条件等于 \(\mathcal I^{-1}\) 的矩阵 |
| \(J\) | 指定序列及速度下的 LDP 率函数 | 单次实验的 Fisher 信息 |
| \(\beta>0\) | 指数/风险敏感参数 | 未注明的样本量或 LDP 速度 |
| \(a_N\to\infty\) | 大偏差速度 | 随机停止次数本身 |
| \(M_t\) | 时间 \(t\) 可保留的标签数 | 浮点位数、总计算空间或历史磁带 |
| \(b_t=\lceil\log_2M_t\rceil\) | 持久标签的比特预算 | 免费读写的任意实数 |

## 1.1 必须保留两条不同的映射

预测几何的映射是

\[
H_t\longrightarrow S_t\xrightarrow{\Pi_t}\mathbb R^{q_t},
\]

其中 \(\Pi_t\) 表示对未来任务的条件预测。

统计可辨识性的映射是

\[
\Lambda\longrightarrow\prod_{\alpha}\mathcal P(H_N),
\qquad
\lambda\longmapsto(P_{\lambda}^{\alpha})_\alpha.
\]

有限特征或接触数据还给出第三种映射

\[
\mathsf O:\Lambda\longrightarrow\mathcal Z.
\]

\(D\Pi_t\)、分布族的 score 导数、\(D\mathsf O\) 是三个不同的导数。只有在建立可观测性、充分性或具体实现定理后，才可比较其秩、核和尺度。

## 1.2 先验依赖与全参数有效性

频率学派层保留整个 \((P_\lambda)_\lambda\)。算法不能读取真 \(\lambda\)。

贝叶斯层需另给先验 \(\eta\in\mathcal P(\Lambda)\)，并将 \((\lambda,x_t)\) 作为联合隐藏状态。后验与实际获得的分布由该准备生成。某个固定先验下的预测商不自动成为全参数族的最小充分统计量。

---

# 2. 基础公理 A0–A5

这些公理固定研究语言，不把谱隙、LDP、有限维可压缩性或奇异性分类偷偷写成前提。

## A0. 可测类型与可见接口

\(\Lambda,X_t,A_t,Y_{t+1}\) 取标准 Borel 空间。时间首先取离散有限或可数序列；连续物理时间可以作为报告中的时钟增量，连续时间极限另设非爆炸、路径正则性和一致性条件。

可见历史为动作、观测和已公开资源记录组成的序列。若可用动作依赖历史，动作可用性及剩余预算必须是可见状态的一部分；不能把拥有不同合法后续实验的历史判为等价。

标准 Borel 是保证常规条件分布等可测工具可用的基础类别；不是紧性、光滑性或有限维假设。[W1]

## A1. 正的规范化实验核

给定准备族 \(\mu_\lambda\in\mathcal P(X_0)\) 和联合可测核

\[
K_t^\lambda(dx',dy,dc\mid x,a),
\qquad K_t^\lambda\ge0,
\qquad K_t^\lambda(X_{t+1}\times Y_{t+1}\times\mathcal C\mid x,a)=1.
\]

\(c\) 是本次资源增量或物理时钟记录；资源值取约定的可加非负空间。损失、终止和“没有成功报告”均可通过明确的符号表示。

不要求每个报告的概率严格大于零。A1 中用于统一 Bayes 更新界的 \(\kappa>0\) 属于后续定量条件，不能成为所有确定性系统的排除条件。

确定性动力学由 Dirac 核表示。概率可来自初始准备、随机机制或观测通道，不假定确定性物理系统必须另加噪声。允许把必要的完整微观过去纳入隐藏状态，因此核表述不是对某个预先选定的有限宏观变量强加 Markov 闭合；后者仍须另外证明。

## A2. 因果控制与随机化

策略必须具有形式

\[
\alpha_t(da\mid h_t),
\]

仅依赖已经公开的历史、已知校准及允许的独立随机化。对未来报告或未知真参数的访问被排除。

停止规则是可见过滤下的停止时刻。为证明平均下界选取的探索策略必须事先固定，且不能随待评估编码器改变。

## A3. 测试的可执行性与后续闭合

\(\mathcal Q_t\) 指定时间 \(t\) 以后合法实验及其有界报告/终端读出。每项测试附带其动作、观测、时间和成本含义。

测试体系包含常数与所需报告事件，并在合法的一步延续、有限随机选择和适用的有界单调极限下闭合。令 \(\mathcal V_t\) 为相应的测试线性空间。

离散报告时定义正算子

\[
(\mathsf T_{t,a,y}f)(x)
=\int f(x')\,K_t(dx',\{y\}\mid x,a).
\]

若 \(f\in\mathcal V_{t+1}\)，则合法拉回 \(\mathsf T_{t,a,y}f\in\mathcal V_t\)。一般报告用事件 instrument 或条件核表达，而不是对连续单点事件直接除以零概率。

动态实验一般由算子词组成。只有静态潜变量与相应条件独立重复观测结构成立时，才可将这些算子简化成似然函数的交换乘法。

## A4. 实际准备与完整记账

所有“平均风险”“获得的质量”和“稀有事件成本”均相对于明确的路径分布。一次成功前的失败、校准阶段、终止标记与再准备操作都属于实际实验。

条件实验与原始实验是不同对象。把事件 \(E\) 上的条件分布作为对象时，必须同时交代 \(P(E)\) 和实现该条件实验的协议；不能以条件化抹去成本。

## A5. 资源与态射的可执行性

区分持久标签、临时工作空间、程序只读常量、校准精度、原始准备次数和物理时钟。常量若取决于未知参数，则不是免费校准。

任何归约模拟器都必须交代其内部状态及预算传递。若模拟器需保留 \(R_t\) 个状态，目标算法保留 \(M_t\) 个状态，则串行实现的直接预算上界是 \(R_tM_t\)，而非 \(M_t\)。

这里只规定算法模型和代价计算规则；不先验断言任何最优内存单调性。

---

# 3. 三种对象：原始实验、可达预测对象、任务化几何对象

## 3.1 原始实验对象

定义

\[
\mathfrak E
=\left(\Lambda,(X_t,A_t,Y_{t+1},K_t^\lambda)_t,
(\mu_\lambda)_\lambda,\mathcal Q,\mathcal C\right).
\]

它不包含尚未导出的 Fisher 度量、率函数或有限维流形。不同模型可以拥有不同隐藏空间，不要求存在一个所有物理平台共有的微观状态空间。

## 3.2 正测度与归一化预测对象

在固定准备下，令 \(b_t\) 表示未归一化后验或 instrument 更新后的正测度，\(Z_t=b_t(1)\)。离散报告时

\[
b_{t+1}(f)=b_t(\mathsf T_{t,a_t,y_{t+1}}f).
\]

在 \(Z_t>0\) 时令 \(\pi_t=b_t/Z_t\)。未来测试预测为

\[
\Pi_t(\pi_t)(f)=\pi_t(f),\qquad f\in\mathcal V_t.
\]

定义观测等价关系

\[
\pi\equiv_t\widetilde\pi
\iff \pi(f)=\widetilde\pi(f)\quad\forall f\in\mathcal V_t,
\]

并附加相同的合法后续动作签名。

**实现约定。** 实际 posterior 空间 \(\mathcal P(\Lambda\times X_t)\) 是安全的标准 Borel 实现。最小预测商可首先作为上述等价类或 evaluation image 定义。需要其成为标准 Borel 状态机时，必须验证可数决定测试、像与更新的可测实现条件。有限字母有限时域下此问题直接消失；紧连续有限维实现也可直接验证。底层不承诺任意可测商都是光滑或标准 Borel。

零证据处保留零测度，不指定任意“规范后验”。边界上的连续化、投影方向或 blow-up 是额外的拓扑研究，而非 Bayes 公式的自动延拓。

## 3.3 可达预测几何

在已验证的状态实现 \(s_t:H_t\to S_t\) 上，定义

\[
\nu_t=(s_t)_\#P^{\alpha^{\rm expl}},
\qquad
\mathsf A_t=\{\Pi_t(s):s\text{ 可由合法历史到达}\}.
\]

应区分合法可达集合、特定探索 law 的支持和全体形式允许的参数集合。它们一般不同。

选择有限实际测试 \(q_1,\ldots,q_m\) 及实际选择权重 \(w_j>0\)，得到

\[
p_t(s)=\big(\sqrt{w_j}\,\mathbb E[q_j\mid s]\big)_{j=1}^m.
\]

欧氏度量来自明确的平方损失及测试选择，而不是任意的、随退化发散的 whitening。

## 3.4 任务对象

任务必须声明它是预测还是参数推断：

\[
\mathfrak T^{\rm pred}=(\mathcal Q_t,w,\ell,\alpha^{\rm expl}),
\qquad
\mathfrak T^{\rm est}=(\tau:\Lambda\to\mathcal Z,\ell,\mathcal A).
\]

预测遗憾相对于完整历史的条件最优预测；估计风险相对于同一个真实目标 \(\tau(\lambda)\)。不能用前者的单调性代替后者，或反过来。

---

# 4. 态射：不能用一个模糊箭头包办所有归约

## 4.1 参数重标记

若 \(r:\Lambda'\to\Lambda\)，拉回实验为 \(P'_{\lambda'}=P_{r(\lambda')}\)。只有双射且具有相应正则性时才是坐标同构。非单射参数化引入表示冗余，不能称为数据压缩。

## 4.2 因果实验模拟态射

\(\Gamma:\mathfrak E\to\mathfrak F\) 表示可用 \(\mathfrak E\) 实现 \(\mathfrak F\)。它由以下数据组成：

- 参数无关、非预见的报告转换器 \(G\)，以及其明确内部状态；
- 目标策略到源策略的因果提升 \(\mathsf L_\Gamma\)；
- 合法动作、时钟、任务读出和成本对应；
- 单调资源传递上界 \(\rho_\Gamma\)。

要求对每个参数和每个目标策略均有

\[
G_\#P_{\mathfrak E,\lambda}^{\mathsf L_\Gamma\alpha}
=P_{\mathfrak F,\lambda}^{\alpha}.
\]

转换器可以随机化，但不能读取 \(\lambda\) 或未来。若声称不增加内存，还必须证明 \(\rho_\Gamma\) 在该资源上为恒等或有明确更小上界。

同一参数空间下，这给出一个带资源证书的因果实验范畴。不同参数空间通过 4.1 的基变换连接，避免把物理量名称不同的两个实验直接宣布等价。默认路径预算是逐路径上界；若使用期望预算或尾概率预算，证书须另标注，复合时使用同一种预算语义。

## 4.3 确定性精确状态归约

更强的实现是给定 \(r_t:X_t\to X'_t\)、报告映射 \(g_t\) 和动作提升 \(\iota_t:A'_t\to A_t\)，满足

\[
(r_{t+1},g_t)_\#K_t^\lambda(\cdot\mid x,\iota_t a')
=K_t'^\lambda(\cdot\mid r_t x,a'),
\]

以及初始准备兼容、成本和读出匹配。这是可检查的一步核等式。路径 law、期望及有限时间算子的相容性由它推导，不另将这些结论塞进态射定义。

它通常比“某个统计量在一个固定时刻保留信息”强得多。

## 4.4 充分性、等价性与因果等价性

固定实验族的后处理 \(Q_\lambda=P_\lambda G\) 若存在参数无关恢复核 \(R\) 使 \(Q_\lambda R=P_\lambda\)，则两实验在该参数族上可互相模拟。

但终端恢复核可能使用完整数据；它不一定能在线实现。因此另定义双向因果等价与给定资源下的双向因果等价。

贝叶斯固定先验下的恢复核、对全部 \(\lambda\) 有效的恢复核、终端恢复与逐时因果恢复必须分别标注。[W2]

## 4.5 近似态射

在指定参数域与策略类上定义

\[
\varepsilon(\Gamma)=
\sup_{\lambda,\alpha}
\left\|G_\#P_{\mathfrak E,\lambda}^{\mathsf L_\Gamma\alpha}
-P_{\mathfrak F,\lambda}^{\alpha}\right\|_{\rm TV},
\]

约定 \(\|P-Q\|_{\rm TV}=\sup_B|P(B)-Q(B)|\)。这是某个已给出模拟器的缺陷；对全部允许模拟器取下确界才得到相应 deficiency。

近似态射以 \((\varepsilon,\rho)\) 为证书。总变差缺陷适用于有界决策风险；大偏差、导数、弱收敛等不同层需使用相应强度的证书，不能互相替代。

---

# 5. 首批通用定理 T01–T12

## T01. 路径实现与确定性嵌入

**条件：** A0–A2，有限或可数离散时域。

**结论：** 每个参数 \(\lambda\) 与每个因果策略 \(\alpha\) 唯一确定一致路径 law，有限时域表达为

\[
P_\lambda^\alpha(dx_0,da_0,dx_1,dy_1,\ldots)
=\mu_\lambda(dx_0)\prod_t\alpha_t(da_t\mid h_t)
K_t^\lambda(dx_{t+1},dy_{t+1}\mid x_t,a_t).
\]

以 Dirac 核替换确定性演化，不改变其原始轨道 law。

**证明。** 有限时域逐次积分；规范化保证每一步总质量为一，并保证边缘一致。可数时域使用标准核扩张构造。Dirac 情形积分就是沿既定轨道代入。唯一性由柱事件上的一致性确定。

**地位：** 经典概率核构造；本理论的价值在明确物理与观察类型，而不是重新命名该构造。

## T02. 预测商的最小性与因果闭合

**条件：** A3 的测试覆盖全部拟保留未来任务，且在一步延续下闭合。先在有限报告情形表述；一般情形以相应 instrument 和可测实现条件表达。

**结论：** 两个已准备的后验在 \(\mathcal V_t\) 上相等，当且仅当对这些合法未来实验给出相同读出 law。对概率为正的下一报告，更新在预测等价类上良定义：

\[
\pi'(f)=
\frac{\pi(\mathsf T_{t,a,y}f)}{\pi(\mathsf T_{t,a,y}1)}.
\]

任何确定性历史统计量 \(r_t(h)\) 若足够完成全部这些未来任务，则最小预测状态是 \(r_t\) 的函数；相应可测实现成立时，因子也是可测的。

**证明。** 闭合性保证分子分母均只用等价类已知的测试值。归纳给出每个未来报告词的概率；单调类延拓到其生成的事件。反向由测试定义直接成立。若两历史具有相同 \(r_t\)，其预测必须相同，因此 \(r_t\) 的每个纤维包含于预测等价类，从而存在唯一的商因子。有限情形无可测障碍；标准 Borel 最小实现需验证第 3.2 节的条件。

**限制：** 这不是“任意有限几个矩都足够”。也不自动证明商是光滑流形或有限状态集。

**经典接口：** 因果状态/最小预测表示是既有研究主题；此处加入控制、任务选择、实际准备与资源类型。[W4]

## T03. 因果模拟的复合、误差与风险传递

**条件：** \(\Gamma_1:\mathfrak E\to\mathfrak F\)、\(\Gamma_2:\mathfrak F\to\mathfrak G\) 为上述因果模拟器；误差对所需参数与策略统一。

**结论：** 串行复合仍为因果模拟，且

\[
\varepsilon(\Gamma_2\circ\Gamma_1)
\le\varepsilon(\Gamma_1)+\varepsilon(\Gamma_2),
\qquad
\rho_{\Gamma_2\circ\Gamma_1}
=\rho_{\Gamma_1}\circ\rho_{\Gamma_2}
\]

是有效预算上界。若逐步条件核误差至多 \(e_t\)，则有限时域缺陷至多 \(\sum_te_t\)，并以 1 截断。

对共同目标和 \(0\le\ell\le L\) 的决策任务，

\[
\mathfrak R_{\mathfrak E}(\rho_\Gamma(B))
\le\mathfrak R_{\mathfrak F}(B)+L\varepsilon(\Gamma).
\]

**证明。** 两模拟器按时间交错执行，其联合内部状态形成实现；因果性由每一步仅读过去保持。核的总变差收缩性与三角不等式给出缺陷界。逐步界用 telescoping 替换一项条件核，或通过每一步最大耦合和并集界证明。有界损失的期望差至多 \(L\|P-Q\|_{\rm TV}\)；在源上运行模拟器加目标算法并取下确界，得到风险界。

**资源解释。** 若模拟器保留 \(R_t\) 个状态，复合有限状态机可用 \(R_tM_t\) 标签，而不必等于最优数量。该界是构造上界，不是最优内存等式。

## T04. 后验重心、凸序与相对熵单调性

**条件：** 固定共同准备；隐藏目标 \(Z\)、原始观测 \(Y\)、后处理 \(W\) 满足 \(Z\to Y\to W\)。

**结论：** 对任意有界目标测试 \(f\)，

\[
\mathbb E[f(Z)\mid W]
=\mathbb E[\mathbb E[f(Z)\mid Y]\mid W].
\]

因此对有限预测向量 \(p_Y,p_W\)，

\[
p_W=\mathbb E[p_Y\mid W],
\quad
\mathbb E\varphi(p_W)\le\mathbb E\varphi(p_Y)
\]

对可积凸函数成立。这是后验 law 的凸序，而不是预测状态集合的逐点映射。

对参数无关核 \(G\) 与 \(P\ll Q\)，

\[
D(PG\|QG)\le D(P\|Q).
\]

存在条件分布且熵有限时更有

\[
D(P\|Q)=D(PG\|QG)
+\int D(P(dx\mid w)\|Q(dx\mid w))\,(PG)(dw).
\]

**证明。** 第一式是条件独立与塔式法则，第二式是条件 Jensen。熵公式对联合分布 \(P(dx)G(dw\mid x)\)、\(Q(dx)G(dw\mid x)\) 作链式分解；联合熵等于 \(D(P\|Q)\)。

**充分性推论。** 若有支配基准 \(P_0\)，所有 \(P_\lambda\ll P_0\)，相应有限熵对每个 \(\lambda\) 都取等号，则可取共同恢复核 \(P_0(dx\mid w)\)。没有这些兼容条件，不从孤立的一个等号推出全族结论。

## T05. 信息损失的条件协方差表示

**条件：** 参数族在所考察点二次均方可微，或有限正概率模型具有足够可交换微分条件；\(G\) 不依赖未知参数。设原 score 为 \(s_\lambda(Y)\)。

**结论：**

\[
s_\lambda^G(W)=\mathbb E_\lambda[s_\lambda(Y)\mid W],
\]

\[
\boxed{
\mathcal I_\lambda-\mathcal I_\lambda^G
=\mathbb E_\lambda\operatorname{Cov}_\lambda(s_\lambda(Y)\mid W)
\succeq0.}
\]

特定方向 \(v\) 的信息无损，当且仅当 \(v^Ts_\lambda\) 可由 \(W\) 表示（几乎处处）。

**证明。** 在有限正概率模型中，对 \(q_\lambda(w)=\sum_y p_\lambda(y)G(w\mid y)\) 微分并除以 \(q_\lambda(w)\)，得到条件均值 score。对 score 用全协方差公式即得。一般二次均方可微版本通过条件期望的 \(L^2\) 收缩控制余项；具体结果可接 Pollard 的定理。[W3]

**严格限制。** 信息相等是局部 score 保留，不是全局充分性。参数重标记下用 \(Dr^T\mathcal I Dr\)；随机目标的推前协方差、参数 Fisher 的后拉和压力 source Hessian 的协方差是不同公式。

## T06. 归一化响应配对与观测乘积的精确纤维

### T06a. 归一化响应

**条件：** \(\pi\) 为概率，\(f,g\) 有界，令

\[
\pi_u(dx)=\frac{e^{ug(x)}\pi(dx)}{\pi(e^{ug})}.
\]

**结论：**

\[
\left.\frac{d}{du}\pi_u(f)\right|_{u=0}
=\pi(fg)-\pi(f)\pi(g)=\operatorname{Cov}_\pi(f,g).
\]

对于一般光滑正似然，\(g\) 取其对所用参数的对数导数，得到同样的中心化配对。

**证明。** 分子分母求导并使用 \(\pi(1)=1\)。有界性给出合法的积分微分交换。

### T06b. 乘积观测纤维

**条件：** 在实交换函数代数中取有限维空间 \(V\)，它包含所观测的全部乘积。给定 \(U_1,\ldots,U_L\) 且 \(U_\nu U_\nu\subset V\)。未知对象是 \(\ell\in\Omega\subset V^*\)，\(\Omega\) 在 \(V^*\) 中开；正性可作为开域条件。观测为各 \(U_\nu\) 上的双线性形式 \(B_\nu(f,g)=\ell(fg)\)。

置

\[
W=\sum_\nu\operatorname{span}\{fg:f,g\in U_\nu\}\subset V.
\]

**结论：**

\[
\operatorname{Fib}(\ell)=(\ell+W^\perp)\cap\Omega,
\quad
\dim\operatorname{Fib}_{\rm loc}=\dim V-\dim W.
\]

恢复全部 \(\ell\) 当且仅当 \(W=V\)。若未知仅在较小仿射子空间中变化，维数应改为其方向空间与 \(W^\perp\) 交的维数。

**证明。** 两个观测相等恰好意味着差泛函在全部生成乘积上为零。开域保证小幅不可见扰动仍在允许集合中。其余是秩–零化度公式。

**A1/A2 接口。** T06a 解释 A1 中实际获得方向与未来测试的协方差配对；T06b 解释 A2 接触信息的乘法对偶。两者共享正泛函与测试结构，但不能因此合并成无条件相同的统计实验。[R1–R3]

**高阶扩展的边界。** 若实验确实测量 \(\ell(f_1\cdots f_m)\)，同样的零化子结论适用。不能仅把 \(\operatorname{Sym}^2\) 改写成 \(\operatorname{Sym}^m\)，就认定距离函数的第 \(m\) 阶 jet 给出该实验。

## T07. Checkpoint 预测遗憾恰为量化问题

**条件：** 固定实际历史 law；测试在编码后独立抽取，平方损失；预测向量 \(p_t(h)\in\mathbb R^q\)，其 law 为 \(\nu\)。编码与解码允许独立随机化，但总持久标签数不超过 \(M\)。

**结论：**

\[
\boxed{
R_M^{\rm chk}=
\inf_{c_1,\ldots,c_M}
\int\min_j\|p-c_j\|^2\,\nu(dp).}
\]

测试预测被限制在闭凸可行读出集时，中心可投影回该集合。

**证明。** 条件平方损失分解为 Bayes 损失加预测均值的平方误差。给定标签，以解码器均值替代随机解码不会增加误差。任何向 \(M\) 个中心的随机分配不优于最近中心；反向用最近中心编码达到同一值。对独立公开随机种子条件化后，每个固定代码本的风险都不小于右侧下确界，故随机代码本也不能改善该下确界。

**结论含义。** 平均内存曲线依赖集合与测度二者。相同 reachable set 不足以固定平均误差。该命题不将编码计算时间、参数估计或在线实现免费化。代码本针对已声明的准备实验选择；逐个未知真参数分别优化的等式不提供一个对整族共同有效的代码本，后者须保留相应 minimax 量词。

## T08. 量化误差的因果实现与传播

**条件：** 已有可测可达状态空间 \((S_t,d_t)\)；共同当前输入下更新满足

\[
d_{t+1}(F_{t,a,y}s,F_{t,a,y}\widetilde s)
\le L_t d_t(s,\widetilde s),
\]

且对所用代表状态更新合法；每个 \(S_t\) 有至多 \(M_t\) 个可达代表的覆盖，半径 \(r_t(M_t)\)。物理读出在 \(d_t\) 下 Lipschitz。

**结论：** 更新代表再量化构成一个真正在线的有限状态机，

\[
e_t\le
\sum_{j=1}^t\left(\prod_{i=j}^{t-1}L_i\right)r_j(M_j).
\]

每个因果编码也都是该时刻的 checkpoint 编码，故最大 checkpoint 平均遗憾至少是相应 T07 下界的最大值。

**证明。** 一步三角不等式给出 \(e_{t+1}\le L_te_t+r_{t+1}\)，从 \(e_0=0\) 归纳。算法仅保留当前代表的标签。合法性与可测性由上述假设及有限中心的固定 tie rule 保证。

**无限时域推论。** 若这些条件统一成立、\(L_t\le\rho<1\)、\(r_t\le r\)，则 \(e_t\le r/(1-\rho)\)。有限时域的 \(C_N\) 不能在没有这种稳定性时改称统一常数。

**A1 型各向异性推论。** 若进一步已证明全局有限格式覆盖、实际获得的各层正质量，以及碰撞处稳定的原始更新，则

\[
Q_t(M)=\max_{1\le\ell\le p_t}
\left(\frac{\prod_{i=1}^{\ell}s_{t,i}}{M}\right)^{2/\ell}
\]

可同时控制 checkpoint 风险和固定时域因果风险的阶。这是 A1 的 G/A/C 结果的接入位置，而不是仅由矩阵奇异值推出的通用结论。[R1]

**控制边界。** 上述传播先比较同一输入序列下的状态。编码改变动作时，还需闭环稳定性或 T03 的策略模拟；不能直接宣布相同控制遗憾界。

## T09. 指数后拉、压力与熵对偶

**条件：** Markov 核 \(G:X\rightsquigarrow Y\)，有界可测 \(f\)，\(\beta>0\)。

定义

\[
\mathcal T_{G,\beta}f(x)
=\beta^{-1}\log\int e^{\beta f(y)}G(dy\mid x).
\]

**结论一：** 对 \(H:Y\rightsquigarrow Z\)，

\[
\mathcal T_{GH,\beta}
=\mathcal T_{G,\beta}\circ\mathcal T_{H,\beta}.
\]

**结论二：** 对 \(\mathcal P_{P,\beta}(f)=\beta^{-1}\log P(e^{\beta f})\)，

\[
\boxed{
\mathcal P_{PG,\beta}(f)
=\mathcal P_{P,\beta}(\mathcal T_{G,\beta}f).}
\]

若 \(G\) 为确定性映射 \(g\)，\(\mathcal T_{G,\beta}f=f\circ g\)。随机情形一般不等于 \(Gf\)。

**结论三：**

\[
\mathcal P_{P,\beta}(f)
=\sup_{Q\ll P}\{Qf-\beta^{-1}D(Q\|P)\}.
\]

极值由 \(dQ_f/dP=e^{\beta f}/P(e^{\beta f})\) 取得。微分满足

\[
D\mathcal P_{P,\beta}(f)[u]=Q_f u,
\qquad
D^2\mathcal P_{P,\beta}(f)[u,v]
=\beta\operatorname{Cov}_{Q_f}(u,v).
\]

**证明。** 前两式直接指数化后使用核积分的复合。对偶由

\[
D(Q\|Q_f)=D(Q\|P)-\beta Qf+\log P(e^{\beta f})\ge0
\]

得到；在 \(Q=Q_f\) 取等。导数由有界函数下的积分求导得到。

**地位：** 指数积分–相对熵对偶是经典结果，原动力学与风险敏感控制可以在此接入。[W6] 此处给出证明以固定符号、\(\beta\) 因子和随机后处理规则，而非提出优先权声明。

**随机后拉的二阶链式推论。** 令 \(h=\mathcal T_{G,\beta}f\)，并定义

\[
P^h(dx)=\frac{e^{\beta h(x)}P(dx)}{P(e^{\beta h})},
\qquad
G_f(dy\mid x)=\frac{e^{\beta f(y)}G(dy\mid x)}{G(e^{\beta f})(x)}.
\]

则 \(P^hG_f\) 正是联合 law \(P(dx)G(dy\mid x)\) 经 \(e^{\beta f(y)}\) 倾斜后的 law，且

\[
D\mathcal T_{G,\beta}(f)[u]=G_fu,
\qquad
D^2\mathcal T_{G,\beta}(f)[u,v]
=\beta\operatorname{Cov}_{G_f}(u,v).
\]

因此压力的复合二阶导数恰为

\[
\beta\operatorname{Cov}_{P^h}(G_fu,G_fv)
+\beta\mathbb E_{P^h}\operatorname{Cov}_{G_f}(u,v)
=\beta\operatorname{Cov}_{P^hG_f}(u,v).
\]

证明仅需上面的求导式与全协方差公式。这给出了“正核—压力—响应协方差”的精确联结，同时明确保留通道内部的条件波动项；没有把随机通道误当成确定性后拉。


## T10. 全局纤维、奇异模量与统计下界

**条件：** 指定观测模型和目标 \(\tau\)。对确定性特征映射 \(\mathsf O:\Lambda\to\mathcal Z\) 定义

\[
\omega_{\mathsf O,\tau}(\delta)
=\sup\{d_\tau(\tau\lambda,\tau\lambda'):
 d_{\mathcal Z}(\mathsf O\lambda,\mathsf O\lambda')\le\delta\}.
\]

**确定性恢复结论：** 若参数域紧、映射连续，从 \(\widehat z\) 作最小距离拟合且
\(d(\widehat z,\mathsf O\lambda)\le\delta\)，则

\[
d_\tau(\widehat\tau,\tau\lambda)\le\omega_{\mathsf O,\tau}(2\delta).
\]

**证明。** 真参数是可行候选，故拟合残差不超过 \(\delta\)；三角不等式给出两真实像之间不超过 \(2\delta\)。代入模量定义。

**统计下界：** 对已经包含 \(N\) 次观测及指定设计的分布族 \(P_{N,\lambda}\)，若

\[
\|P_{N,\lambda_0}-P_{N,\lambda_1}\|_{\rm TV}\le a<1,
\]

则平方距离风险满足

\[
\inf_{\widehat\tau}\sup_{\lambda\in\{\lambda_0,\lambda_1\}}
\mathbb E_\lambda d_\tau(\widehat\tau,\tau\lambda)^2
\ge\frac{1-a}{8}
 d_\tau(\tau\lambda_0,\tau\lambda_1)^2.
\]

**证明。** 将任意估计器转成“选较近目标”的二元检验。误判时距离至少为目标间距离的一半；两个检验错误概率之和至少 \(1-\mathrm{TV}\)，再取两风险均值。

**限制。** 把此下界升级为普适的双边 minimax 等价，需要测试、覆盖、尾部和参数类条件。不能从一个导数秩或一个 Łojasiewicz 指数直接跳到全类最优统计速率。模量与速率之间已有深入经典研究，应作实质比较。[W5]

## T11. 大偏差归约与正规二阶一致性

### T11a. 率函数归约

**条件：** \(P_N\) 在 Polish 空间 \(X\) 上以确定速度 \(a_N\) 满足良好 LDP，\(T:X\to Y\) 连续。

**结论：** \(T_\#P_N\) 具有良好率函数

\[
J_Y(y)=\inf_{T(x)=y}J_X(x).
\]

对有界连续源 \(f\)，Laplace 原理给出

\[
\lim_Na_N^{-1}\log P_N(e^{a_N f})
=\sup_x\{f(x)-J_X(x)\}.
\]

**证明。** 闭集与开集的逆像仍为闭、开，将 LDP 上下界作用于逆像；率的紧子水平集由良好性和连续像得到。Laplace 公式由在紧子水平集上对 \(f\) 有限分层和指数紧控制证明。这是经典 contraction/Laplace 原理，不由基础公理自动生成。[W7]

随机核后处理必须分析联合 law 或另给条件率；不能把 \(J_Y(y)=\inf_{Tx=y}J_X(x)\) 的确定性公式无条件用于随机通道。

### T11b. 正规二次型的 Schur 归约

**条件：** 在正规点的二次变化为 \(\frac12h^THh\)，\(H>0\)，线性读出 \(z=Ah\) 且 \(A\) 满行秩。

**结论：**

\[
\inf_{Ah=z}\tfrac12h^THh
=\tfrac12 z^T(AH^{-1}A^T)^{-1}z.
\]

**证明。** Lagrange 方程给出 \(h=H^{-1}A^T(AH^{-1}A^T)^{-1}z\)，代入即可。

若已另证该 \(H^{-1}\) 为相应高斯极限协方差，那么这与 \(\Sigma\mapsto A\Sigma A^T\) 相容。LDP 单独不保证 CLT、压力可二次微分或其极限可与微分交换。

### T11c. 有标签有限相混合

若有限个分量具有共同速度的良好率 \(J_j\)，且 \(-a_N^{-1}\log w_{N,j}\to c_j\)、\(\min_jc_j=0\)，则带标签 law 的率为 \(c_j+J_j\)，去标签率为

\[
J(x)=\min_j\{c_j+J_j(x)\}.
\]

证明由有限和的上下界得到。动态混合仍须保留更新后的相后验；不能据此把边缘 log-sum 直接称为 Markov 半群。

## T12. 精确动力学闭合与记忆的产生

**精确闭合条件：** 对 Markov 核 \(P\)、状态映射 \(q\)，存在 \(\bar P\) 满足

\[
P(f\circ q)=(\bar Pf)\circ q
\]

对所有必要测试成立。则该预测/状态归约具有兼容的 Markov 演化，其迭代算子和 T09 的指数变换也兼容。

**证明。** 一步恒等式逐次代入，得到所有有限时间恒等式；指数变换先对 \(e^{\beta f}\) 使用同一核恒等式。

**有限维线性记忆定理：** 若

\[
\dot u=A_{PP}u+A_{PQ}v,
\qquad
\dot v=A_{QP}u+A_{QQ}v,
\]

消去 \(v\) 得到

\[
\dot u(t)=A_{PP}u(t)
+A_{PQ}e^{tA_{QQ}}v(0)
+\int_0^t A_{PQ}e^{(t-s)A_{QQ}}A_{QP}u(s)\,ds.
\]

**证明。** 对第二式用常数变易公式，再代入第一式。

由此产生瞬时项、未解析初态的强迫项和记忆核三部分。任何忽略 \(v(0)\) 项的普遍“闭合方程”都需额外初态假设。

**无限维接口。** 无界生成元、闭形式、共同定义域、压缩预解式和记忆核的可积性必须另证。旧 A4/C2 的这些任务仍然存在，不因有限维代数恒等式被取消。[R5]


---

# 6. 真正的统一：四条连接，而不是一个万能不变量

## 6.1 正泛函与归一化是共同出发点

A1 的后验预测与 A2 的矩/接触信息均可写成正泛函对测试的求值。归一化产生协方差配对；可观测乘积的张成空间产生零化子。

但对同一双线性表达式必须追踪它来自哪一种变化：过去命令变化、未知参数变化、源函数倾斜，还是观测读出变化。它们可能给出相似矩阵，却不具有相同的统计或动力学含义。

## 6.2 统计后处理的精确层是 law，不是有限矩阵

统计后处理首先作用于 \(P_\lambda\)。在固定准备下，它使后验成为条件重心；在二次均方可微层，它使 score 成为条件期望；在有界源层，它给出非线性的指数后拉。

这些关系都从同一个核产生，因此具有真正的可组合性。它们并不意味着某个 Fisher 矩阵包含全部可辨识信息。

## 6.3 内存与可达几何的连接依赖实际质量和因果更新

T07 是精确的 checkpoint 恒等式。T08 是可执行的在线构造。想得到 A1 那样的全预算显式尺度曲线，还需逐项验证：全局覆盖、实际质量、更新稳定性。

对平均风险，把一个概率极小的可达几何片区与整个集合等量处理，会给出错误的下界。对在线上界，只画出每个时刻最优代码本而不构造更新，也不够。

## 6.4 长时与物理理论是实现问题，不是定义问题

旧 Sinai/Fourier、hard-sphere/LDP、history/memory 内容继续承担它们本来的数学工作：证明实际对象满足充分强的长时、几何、可积性及谱条件。

General Theta Foundations 把这些结果放进统一接口，并不把其证明工作改成一句“满足范畴公理”。

---

# 7. 奇异几何的正式分层

建议将“theta discriminant”拆成三层，并分别命名。

## 7.1 全局观测纤维与目标商

在给定观测协议族 \(\mathcal A\) 下，定义

\[
\lambda\sim_{\mathcal A}\lambda'
\iff P_\lambda^\alpha=P_{\lambda'}^\alpha
\quad\forall\alpha\in\mathcal A.
\]

目标 \(\tau\) 的全局可辨识要求它在这些等价类上为常量。有限特征版则以 \(\mathsf O(\lambda)=\mathsf O(\lambda')\) 定义，必须注明它较完整 law 等价更粗或相同。

## 7.2 一阶可观测退化集

在已选光滑结构和物理统计度量下定义

\[
\mathfrak D^{\rm feat}_r=\{\lambda:\operatorname{rank}D\mathsf O_\lambda\le r\},
\]

或在分布族的正规层定义

\[
\mathfrak D^{\rm stat}_r=\{\lambda:\operatorname{rank}\mathcal I_\lambda\le r\}.
\]

预测可达映射也可有其独立的 \(\mathfrak D^{\rm acq}_r\)。这些集合只有在已证明的 bridge 下才相等。

## 7.3 有限分辨率与高阶接触

真正控制失稳与非正规统计难度的候选对象是观测距离与目标距离之间的模量、接触阶和适当的局部实验，而非仅有 rank 标签。

代数模型可用 minors、Fitting ideals、normal cones 和 blow-ups；实解析或半代数模型可用可实现弧、赋值和分层。复代数闭包不能替代实际正概率参数域；复分量必须另证有合法实点及物理实现。

**边界上的声明规则：** “generic full rank”“局部单射”“全局唯一纤维”“二次均方可微”“有限样本可估计”“一致稳定”“最优速率”分别是不同结论，逐项证明。

---

# 8. 必须写进正文的边界例子

这些例子不是放弃推广，而是确定哪些额外结构必须被保留。

## E1. 一阶满秩不保证全局单射

\(f(x)=x^2\) 在 \(x=1,-1\) 的导数均不为零，但两点观测相同。一个全局纤维问题不能只靠当地 Jacobian 回答。

## E2. 相同的一阶秩不决定奇异速率

取 \(Y_i=\lambda^r+\xi_i\)，\(\lambda\ge0\)，\(\xi_i\sim N(0,1)\) 独立。所有 \(r\ge2\) 在 \(\lambda=0\) 的均值映射一阶导数均为零。但 \(\lambda\) 的局部分辨率是 \(N^{-1/(2r)}\)。

理由是两点 KL 为 \(N(\lambda^r)^2/2\)，取其为常数得到该尺度；用样本均值的正部取 \(r\) 次根可给出相应局部上界。这不支持用一个 rank 值替代接触阶。

## E3. 相同均值映射、不同噪声度量

若 \(Z\sim N(\lambda,1)\)，观察 \(Y_\epsilon=\epsilon Z\)，则对每个已知 \(\epsilon>0\)，除以 \(\epsilon\) 即恢复原实验，Fisher 信息仍为 1。

若改为 \(\widetilde Y_\epsilon=\epsilon\lambda+\xi\)、\(\xi\sim N(0,1)\)，信息为 \(\epsilon^2\)。两者均值映射相同，但协方差随观测是否一起缩放不同。

这正是不能把 A2 数值逆映射的条件数无条件改写为原始 score 实验的方差罚项的原因；A2 v112 对相关 score 噪声已有明确区分。[R4]

## E4. 统计后处理可能增加精确预测的标签需求

设 \(Z\sim\mathrm{Bernoulli}(1/2)\)，未来目标还是这个隐藏比特。

原始观测 \(X=Z\) 的后验预测只取 0 和 1；两标签可以零遗憾保留全部预测。

后处理 \(Y=X+\xi\)、\(\xi\sim N(0,1)\)，则

\[
\Pr(Z=1\mid Y=y)=\frac{1}{1+e^{1/2-y}},
\]

其 law 在 \((0,1)\) 上连续。任何有限中心量化都有正的平方误差。因此粗化实验虽信息更少，却不能用任何固定有限标签达到它自己完整历史的零预测遗憾。

这里没有违反数据处理不等式：比较的是两个不同 oracle 基准的超额损失。它否定的是无条件的“粗化不增加精确预测内存”。

## E5. 相同可达集合不决定平均量化曲线

合法实验可以有可达预测集合 \([0,1]\)，但某个探索策略只到达一个点，而另一个产生连续分布。前者平均风险可为零，后者存在非平凡量化误差。因此实际探索 law 不能被几何维数替代。

## E6. 均值和协方差不是整个分布

概率 \(P=\frac12\delta_{-1}+\frac12\delta_1\)，与
\(Q=\frac12\delta_0+\frac14\delta_{-\sqrt2}+\frac14\delta_{\sqrt2}\)
具有相同均值 0 和方差 1，但明显不是同一个 law。

同理，有限阶矩/jet 只有在额外可识别模型类中才可能决定全局对象。

## E7. 统计充分性与 Fisher 无损不同

Pollard 讨论的混合族中，存在不充分而保留 Fisher 信息的统计量。[W3] 因此 T05 的等号只能给出局部 score 可测性，不能替代 T04 的完整恢复核。

## E8. 很小的总变差误差仍可改变 LDP

令 \(P_N=\delta_0\)，

\[
Q_N=(1-e^{-a_Nc})\delta_0+e^{-a_Nc}\delta_1,
\qquad c>0.
\]

总变差为 \(e^{-a_Nc}\to0\)，但点 1 的率分别为 \(+\infty\) 与 \(c\)。即使误差指数小，也不保证保留全部率函数；传递完整 LDP 的常见充分条件是相应速度下的超指数好近似。

所以 A2 的局部 Le Cam 近似与 A3 的指数尺度是两项不同的证书。

## E9. 标量压力的凸对偶可丢失非凸相结构

令 \(P_N\) 对所有 \(N\) 均在 \(-1,+1\) 各给一半质量，以速度 \(N\) 看，其率在两点为零、其他点为无穷。线性源的缩放压力为 \(|s|\)，其 Legendre 变换却在整个 \([-1,1]\) 上为零。

因此线性源压力不能无条件恢复非凸率。完整连续源的 Laplace 泛函与仅线性源的 log-MGF 也不能混同；原 D1 的相标签有实质作用。

## E10. 任意状态投影不自动闭合

取确定性三状态系统 \(a\mapsto a\)、\(b\mapsto c\)、\(c\mapsto c\)，观测 \(q(a)=q(b)=0\)、\(q(c)=1\)。相同当前观测 0 对应不同下一观测，所以 \(q\) 不给出完整的 Markov 闭合。完整未来测试会把 \(a,b\) 区分开。

## E11. 有限维乘法封闭不能伪装成任意连续信息理论

若 \(W\subset C(X,\mathbb R)\) 是有限维含 1 的子代数，每个 \(f\in W\) 都满足一个非零多项式，所以 \(f(X)\) 是有限集。选取有限基，联合取值产生有限个 clopen 纤维；用分离这些取值的多项式插值可构造全部纤维指标。因此 \(W\) 本质上是一个有限可观测商上的函数代数。

故一般基础应使用可增长的测试空间和后拉算子体系，而不是要求一切在同一个有限维交换代数里闭合。

## E12. 零证据与变化先验不能被坐标规范化抹去

\(b/Z\) 在 \(Z=0\) 未定义。若需要包括该边界，必须保留正锥或另建带方向的边界实现。固定先验下的代码本亦不能未经证明用于所有先验或未知校准。

---

# 9. 附加结构 R1–R6：它们不是底层公理

| 模块 | 附加条件 | 可获得的结构 | 仍需证明的内容 |
|---|---|---|---|
| R1 可测实现 | 可数决定测试、适当像与可测分解 | 标准 Borel 最小预测实现 | 所有输入的联合可测更新 |
| R2 正规统计 | QMD、可积 score、适当参数域 | Fisher 信息、局部 score 传递 | LAN、效率、极限实验需各自条件 |
| R3 可达度量几何 | 紧性/全局覆盖、实际质量、稳定更新 | T08 和有限预算曲线 | 明确尺度、零尺度及统一常数 |
| R4 奇异几何 | 实解析/半代数或其他可控类别，真实可行域 | 分层、模量、接触/赋值 | 全局纤维、交叉处与高阶恢复 |
| R5 指数极限 | 良好 LDP、速度、指数紧和源尾界 | 率函数、Laplace/压力极限 | 模型自身 LDP；条件化和时间变换 |
| R6 长时与算子 | 非爆炸、混合或收缩、共同算子/形式域 | 无穷历史、记忆、谱响应 | 所有一致估计和极限交换 |

在有多重极限的问题中，应明确 \(N\to\infty\)、碰撞参数 \(\epsilon\to0\)、内存 \(M\to\infty\)、时域 \(T\to\infty\) 的先后或联动。一个固定参数上的极限不能自动加强为联合统一定理。

---

# 10. 广义 Theta 的正式含义与层级

不把 \(\Theta\) 定义成一个宣称包办全部物理意义的标量。建议将它定义为一套以实验为索引的、带任务及资源的归约结构：

\[
\Theta(\mathfrak E;\mathfrak T)
=\left(
\text{未来测试体系},
\text{可达正泛函/预测商},
\text{实际状态 law},
\text{合法因果归约及资源}
\right),
\]

并在 R1–R6 成立时附加相应的派生结构。

| 层 | 正式对象 | 正确的传递方式 |
|---|---|---|
| 实验层 | 核与完整路径 law | 因果核模拟 |
| 预测层 | 未来测试、后验、可达预测 | 确定性相容后拉；随机后处理下的条件重心 |
| 全局辨识层 | 分布族或指定特征的纤维 | 保留观测模型的等价关系 |
| 正规统计层 | score、Fisher 半度量 | 条件期望与信息缺口 |
| 几何层 | 全局覆盖、质量分布、分辨率 | 明确物理度量下的尺度比较 |
| 奇异层 | rank loci、真实纤维、模量、高阶接触 | 具有正则性和可实现性的分层映射 |
| 压力层 | 指数积分/源泛函 | 随机核的非线性指数后拉 |
| LDP 层 | 指定速度的率函数 | 连续映射或经证明的指数近似 |
| 动力学层 | 闭合核、生成元与记忆 | 一步 intertwining 或保留记忆项 |

这是一套分层相容结构，不是同一函数按零阶、一阶、二阶展开就自动产生的万能 Taylor tower。

---

# 11. 新理论真正值得追求的四项核心研究目标

T01–T12 建立可靠基础，但把这些经典结果与直接推论放在一起还不是新理论的完整贡献。新的主定理应从以下四项中产生。

## G1. 真实获得机制下的奇异因果分辨率定理

**问题：** 对超出单项式/有限代数的实验类，从物理参数和合法探索协议直接推出全局尺度、实际获得质量以及无碰撞间隙倒数的稳定更新。

**输入：** 原始核、后续测试、控制域、真实准备，不把最优量化曲线先写成假设。

**输出：** 全预算预测内存曲线，以及经过退化点仍统一的实际因果实现和匹配下界。

**关键证明：** 多尺度获得 chart；补充命令坐标的正体积积分；全图像覆盖；原始状态的正分母更新；同一探索 law 的多时刻下界。

**A1 位置：** A1 的 G/A/C 转移是接口，monomial 与有限代数是已有精细样例，而不是整个一般证明。

## G2. 观测失效几何与物理统计模量的联结

**问题：** 当接触/测试乘积 map 退化时，哪种真实噪声、量化精度和校准协议使该几何真正控制统计难度？

**输入：** 完整噪声 law、未知参数及 nuisance、实际可行设计、有限精度。

**输出：** 不同奇异层上的观测模量、局部极限实验以及在适当模型类中的匹配统计上下界。

**关键证明：** 对相关 score 噪声与独立测量噪声分开分析；未知校准的实际 pilot 成本；实可行弧与非凸纤维；交叉 strata 的联合缩放。

**A2 位置：** 现有乘法 failure scheme 是一个重要模型。完成更多复代数分量分类本身不等于完成本目标；必须补上实际实验与噪声结构。

## G3. 资源—精度—统计误差的统一传递定理

**问题：** 在一个真正在线的实验里，同时限制原始准备次数 \(N\)、持久标签数 \(M\)、校准误差 \(\delta\) 和模拟缺陷 \(\varepsilon\)，如何传递目标风险？

在已建立共同特征距离及相应误差界的模型中，可以尝试证明形如

\[
d_\tau(\widehat\tau,\tau\lambda)
\le\omega\big(C[\text{统计特征误差}+\text{因果量化误差}+\delta]\big)
\]

的高概率界，再通过尾部积分得到风险界。公式中的每项都必须在同一物理特征度量下定义。

**不能先宣称：** 对所有实验，都有“统计项 + 内存项 + 退化项”的一个固定普适幂律或等式。匹配下界需处理多项误差是否由同一最难子实验同时实现。

## G4. 动力学与指数尺度的模型实现定理

**问题：** 什么动力学条件使实验层的因果归约与长时压力、LDP、正规协方差及实际记忆极限相容？

**关键证明：** 参数统一的真实核估计；可达测度的控制；稳定/混合；指数好近似；终端 excursion 和时钟缺陷；共同形式域与强迫项。

**旧 theta 位置：** Sinai、hard sphere、kinetic、belief dynamics 作为非平凡实现平台进入。它们必须逐一验证条件，不被“通用范畴”替代。

---

# 12. 与现有 A1/A2 及原 11 篇的接入表

| 现有材料 | 接入的基础接口 | 可继承的内容 | 不可自动继承的结论 |
|---|---|---|---|
| 新 A1 v37 | T02、T06a、T07、T08、R3 | 可达预测、正似然更新、取得质量、碰撞尺度、因果实现 | 无穷时域统一性、全未知校准统一代码本 |
| 新 A2 v112 | T05、T06b、T10、R4 | 接触纤维、乘法失效、实际实现、特定局部实验 | 任意噪声的相同速率、由高阶 jet 自动得到高阶乘法 |
| 原 A1 benchmark | T01、T06a、R6 | 确定性/混合 Hamiltonian 基准、物理响应 | 由基准直接推出一般谱理论 |
| 原 A2 Sinai | R5、R6、G4 | 参数统一谱/Fourier 与 return/roof 概率输入 | 由新 A2 代数结果代替这些输入 |
| 原 A3 path LDP | T11、R5 | 路径空间率、停止时钟、指数恢复 | 小 TV 或局部 LAN 自动给出完整路径 LDP |
| 原 A4 history/memory | T02、T08、T12、R6 | 真实未来核、稳定记忆、算子/形式实现 | 任意预测投影自动 Markov 化 |
| B1 microcanonical | A4、T09、T11 | 约束准备、条件概率和源依赖正规化 | 条件实验抹去准备代价 |
| B2 collision LDP | T01、T11、R5 | interacting-particle 的真实路径与 contact law | 未证明的几何接触被当成合法随机变量 |
| B3 cotangents | T05、T11b、R2/R6 | joint covariance、balance gauge、切向极限 | LDP Hessian 自动等于已实现协方差 |
| B4 nonlinear semigroups | T09、T12、R6 | 熵控制、Nisio/非线性演化、实际极限 | 完整历史 tower 自动给出密度闭合 |
| C1 belief/control | T02–T05、T08 | 正 belief、证据、决策与控制 | 固定有限矩对任意历史都精确 |
| C2 typed contraction | T03、T05、T09、T11、T12 | 分类型传递思想、共同域意识 | 不同物理平台天然共享一个 rate |
| D1 phases | T09、T11c、T02 | 带标签混合、相后验与正规局部图 | 边缘 log-sum 自动成为动力半群 |

**总体处理：** 保留所有现有成果和历史证明。General Theta Foundations 是共享基础，不是用新编号覆盖旧 A2 的证明职责。旧程序的模型定理和新程序的几何定理通过明确接口连接。

---

# 13. 详细总目录：三卷，而不是在一篇文章里堆全部理论

## Volume I. Causal Experiments and Attainable Information

### Chapter 1. Operational problem and typed notation

给出原始实验、两类任务、参数与后验的区别、失败和校准记录、资源模型。以 E3/E4 说明为什么不能只用 rank 和“信息不增”。

**交付：** A0–A5；原始对象、任务对象的完整定义；符号和量纲表。

### Chapter 2. Positive instruments and actual histories

构造路径 law、未归一化更新、规范化后验。一般 Borel 报告用 disintegration，离散报告给出完全显式公式。说明非预见策略和停止。

**交付：** T01；证据乘法和归一化命题；失败成本的实际实验表达。

### Chapter 3. Future tests and predictive quotients

由可执行 future protocols 定义测试空间；证明商的极小性质和因果闭合。单独讨论可测实现，不默认抽象商是流形。

**交付：** T02；有限字母、紧连续/有限维、一般 Borel 的三个实现说明。

### Chapter 4. Causal morphisms and experiment comparison

给出策略提升、模拟器状态、资源传递和总变差缺陷。区分静态 Blackwell 比较与因果比较。

**交付：** T03；复合、恒等、独立并行的构造；成本和错误预算公式。

### Chapter 5. Bayesian geometry and information loss

证明后验重心、凸序、熵缺口、score 缺口。将充分性与 Fisher 无损分开；对参数域、先验和未知校准分别量化。

**交付：** T04、T05；Bernoulli–Gaussian E4 的完整案例。

### Chapter 6. Attainable prediction and finite memory

从 Brier 遗憾推导量化恒等式，区分 checkpoint 与 causal。给出实际代表更新以及平均质量下界要求。

**交付：** T07、T08；从 A1 接入的完整尺度定理及明确 scope。

### Chapter 7. Normalized response and observation modules

建立 T06a，并说明静态交换乘积只是一般 operator-word 结构的特殊情形。讨论有限代数的有限商性质。

**交付：** A1 获得切向与未来测试之间的普适配对接口。

## Volume II. Singular Observation Geometry and Statistical Resolution

### Chapter 8. Global fibres, gauges and real feasibility

区分 parameter gauge、目标不可辨识、局部导数退化和不同观测协议的纤维。保留正锥及有标签分支。

**交付：** 第 7 节三层几何的正式定义；E1/E2/E6。

### Chapter 9. Product duality and contact experiments

先证明一般 T06b，再进入 Hankel/单项式/块谱模型。每个模型均写出真实实验到观测算子的导出。

**交付：** A2 的接触纤维和一般正泛函表述；不预设更高阶距离 jet 的乘法解释。

### Chapter 10. Rank schemes, real strata and quantitative moduli

分析 failure schemes、normal/conormal、实可实现部分、奇异交叉与 finite-resolution 模量。将设计数值条件数和实际统计信息分别处理。

**交付：** G2 的首个非平凡模型定理；T10 的确定性部分。

### Chapter 11. Finite experiments and singular statistical limits

明确原始数据、独立测量噪声、相关 score、量化和 pilot。先给 Le Cam/TV 核，再导局部极限与匹配下界。

**交付：** T10 统计部分；G2/G3 的模型级上下界和合法模拟器。

## Volume III. Dynamic Realizations, Pressure and Typed Limits

### Chapter 12. Exponential transforms and entropy duality

固定 \(\beta\)、\(a_N\) 和所有正负号；证明随机核的非线性压力后拉；给源导数和条件协方差的链式结构。

**交付：** T09；有限时域风险敏感控制的明确递推。

### Chapter 13. LDP and contraction with preserved scales

先给连续确定性归约，再做随机通道联合率、条件准备和时间变换。明确小 TV 与超指数误差的差别。

**交付：** T11a；G4 的假设清单；E8/E9。

### Chapter 14. Regular tangent compatibility and nonlinear boundaries

推导二次型 Schur 公式，区分 LDP、CLT、LAN 和压力导数。说明 boundary cones、多个极小点和局部图。

**交付：** T11b；经过验证的 covariance/pressure/tangent 对应，而不是概念等同。

### Chapter 15. Closure, hidden history and memory

证明核 lumpability 与有限维记忆恒等式；再接无界算子和闭形式。保留未解析初态项与每个域条件。

**交付：** T12；A4/C2 的物理/算子实现和所需单独证明。

### Chapter 16. Labelled phases and the final synthesis

把相标签作为实际随机变量，给有限混合率和后验演化。列出哪些归约满足哪些层的证书。

**交付：** T11c；分层相容图和完整适用范围表。

---

# 14. 第一篇基础论文的具体形态

建议第一篇题为：

**General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction**

它不应宣称已经完成所有 geometry、kinetic、LDP 理论。主线固定为

\[
\text{真实实验}\to\text{未来预测商}\to\text{因果模拟}\to
\text{有限资源的可达分辨率}.
\]

主文章纳入 A0–A5、T01–T04、T06a、T07–T08，配一个实质性的 A1 类推广或 G1/G3 模型定理。T05 与 T09 可作为解释统一接口的桥梁；大规模代数分量分类和无界算子证明放到后续卷，不用摘要把它们都称为已统一。

**必须有的主结果，而非仅定义集合：** 从原始实验数据直接验证获得质量、全局覆盖和稳定更新，得出真实在线有限预算的匹配界；或证明带反馈和状态预算的非平凡模拟–压缩传递定理，并给出严格超出已有模型的实例。

只重述 Markov categories、Blackwell 和量化恒等式不构成这篇论文的新颖性。对相关文献应逐定理说明新增的是控制、预算、退化统一性还是实际实现。[W1–W5]

---

# 15. 证明依赖与执行顺序

## 15.1 基础依赖图

```text
A0–A2 ──> T01 路径law
A3 + T01 ──> T02 未来预测商
A5 + 模拟器定义 ──> T03 复合/风险/资源
共同准备 + 核后处理 ──> T04 后验重心与KL
T04 + 正规统计条件 ──> T05 score/Fisher
正泛函 + 归一化 ──> T06a 响应配对
明确乘积观测 ──> T06b 精确纤维
T02 + 平方损失 ──> T07 checkpoint量化
T07 + 全局覆盖/实际质量/稳定更新 ──> T08 因果分辨率
正核 + 有界指数源 ──> T09 压力与熵对偶
完整噪声实验 + 目标模量 ──> T10 奇异恢复/统计下界
模型级良好LDP + 连续映射 ──> T11 率归约
核闭合/共同算子域 ──> T12 闭合与记忆
```

## 15.2 第一阶段：冻结对象和比较问题

固定已知/未知参数、任务、成本、准备和观察协议；将旧 A1/A2 中的对象逐项映射进定义。验收不是多一份清单，而是同一符号不再同时指 covariance、Fisher 和 LDP rate。

## 15.3 第二阶段：完成第一组基础证明

为 T01–T12 提供与本纲要一致的正式陈述及证明。一般 Borel 版出现可测选择/商实现问题时，写清所用定理和可测范围；有限模型作为可完全核对的基准，不冒充一般证明。

对所有缺陷界固定 TV 约定、损失范围和策略量词；对所有导数固定定义域和参数；对所有概率事件保留原始质量。

## 15.4 第三阶段：完成两项非平凡接入

A1 接入必须落到 G1：不只把 G/A/C 假设复制一遍，而是从一类新的实际 detector/控制实验验证它们。

A2 接入必须落到 G2：不只计算复 failure variety，而是从真实 noisy/quantized/unknown-calibration protocol 得到统计模量及上下界。

## 15.5 第四阶段：验证至少一个动态实例

先选可完整分析的受控有限状态或其他明确模型，证明因果归约、预测内存、压力和长期极限在其适用范围内相容。再把 Sinai 与 hard-sphere 作为更深的实现平台推进，而不提前领取其结论。

## 15.6 第五阶段：长时与奇异联合极限

明确参数退化、样本增加、时域延长和内存增长的联合标度；给所有常数的依赖。没有这一步，不能把固定紧图上的局部定理宣布成全局统一理论。

---

# 16. 写作与结果验收标准

每个正式主定理必须能回答：

**对象是什么；随机性来自哪里；参数谁知道；控制器看到什么；比较哪一种风险；在哪个范数/拓扑；哪些量趋于极限；常数依赖什么；实际可实现性由哪一条证明提供。**

“通用定理”可以是简单但重要的基础结果；它们必须明确归功于经典来源。真正新的推广放在单独的 theorem 中，不能把所有经典工具的联合使用笼统称为“统一定理已经完成”。

检查重点是数学义务：非零事件质量、全局覆盖、真实物理参数域、因果更新、有限精度、隐藏校准、nonconvex fibres、极限交换。源码保存与编译成功只证明交付可复现，不等于这些义务已经解决。

建议未来的源文件按理论而非审稿轮次组织：

```text
foundations/general-theta/
  00_scope_and_types.tex
  01_experiments_and_axioms.tex
  02_instruments_and_predictive_quotients.tex
  03_causal_morphisms_and_resources.tex
  04_information_and_barycentric_geometry.tex
  05_attainable_resolution.tex
  06_singular_observation_interfaces.tex
  07_pressure_and_entropy.tex
  08_typed_limits_and_memory.tex
  examples/
  references.bib
```

这是建议的组织方式，本次未对远端仓库创建目录、分支或提交。

---

# 17. 来源、归属与审阅范围

## 17.1 仓库来源

**[R1] A1 v37：可达几何到因果内存。**  
`TrillionniumFoundation/theta-theory@90465076589f5e5c69227d624f278c47744f1c1d`  
`papers/A1-english-v37-publication/sections/causal_transfer.tex`  
重点：G/A/C、实际获得质量、固定时域常数、可达代表更新；本总纲 T08 的精细模型接口。

**[R2] A1 v37：正多项式实验结构分类。**  
同一提交，`papers/A1-english-v37-publication/sections/structural_classification.tex`。  
重点：多项式依赖于命令而非潜变量；增广矩阵去证据方向；固定先验的 reachable image 与风险指数。

**[R3] A2 v112：接触纤维与 native 信息模型。**  
`TrillionniumFoundation/theta-theory@0c696736e6ec22259c730672f61ebd8ef0d95460`  
`papers/A2-v17-boundary-information-coarsening/article/v112/parts/01-contact-native.tex`。  
重点：normal compression、乘法对偶、正的参数域、独立设计与同一设计多接触的区别。

**[R4] A2 v112：实际统计实验与局部比较。**  
同一提交，`papers/A2-v17-boundary-information-coarsening/article/v112/parts/04-statistical-experiments.tex`。  
重点：已知 marks、预给中心、target subexperiment、相关 score 噪声、有限精度与 pilot 的范围。这里不把源稿中的全部局部实验结论扩展到全局未知 marks。

**[R5] 旧 C2：typed contraction、共同形式域与压力。**  
`TrillionniumFoundation/theta-theory@c04845b6613208406703695c9c184ae461f95805`  
`papers/C2-cotangent-rigidity-tangent-representations/ROUND17_POSITIVE_CLOSURE.tex`。  
用作历史接口与所需证明义务的来源，非对其所有下游定理的本次重新认证。

## 17.2 学术来源与核查范围

以下将全文/作者稿中核查的具体结果，与仅核实书目信息的历史原文分开。Fritz 的核范畴文本、Pollard 的反例及 score 结论、Varadhan 的 contraction 定理及相对熵变分作者稿用于具体命题核对；Donoho–Liu II/III 与 Blackwell 1953 此次主要核对书目和相关后续原始论文的定位，不声称已对其全文作完整优先权审查。

**[W1] Tobias Fritz.** *A synthetic approach to Markov kernels, conditional independence and theorems on sufficient statistics*. Advances in Mathematics 370 (2020), 107239. arXiv:1908.07021v8.  
关联：核范畴、conditioning、Borel 与一般可测空间的区别。此处的基础概率范畴不作新颖性声明。

**[W2] Tobias Fritz, Tomáš Gonda, Paolo Perrone, Eigil Fjeldgren Rischel.** *Representable Markov Categories and Comparison of Statistical Experiments in Categorical Probability*. Theoretical Computer Science 961 (2023), 113896. arXiv:2010.07416v3.  
关联：Blackwell–Sherman–Stein 和含先验依赖版本的实验比较。经典原文另见 David Blackwell, *Equivalent Comparisons of Experiments*, Annals of Mathematical Statistics 24(2) (1953), 265–272, DOI:10.1214/aoms/1177729032。

**[W3] David Pollard.** *A note on insufficiency and the preservation of Fisher information*. arXiv:1107.3797；公开论文版本讨论 Kagan–Shepp 反例和 QMD 下 score 的条件期望。  
关联：Fisher 无损不能替代统计充分性；T05 的正规统计来源。

**[W4] Cosma Rohilla Shalizi, James P. Crutchfield.** *Computational Mechanics: Pattern and Prediction, Structure and Simplicity*. Journal of Statistical Physics 104 (2001), 817–879. arXiv:cond-mat/9907176.  
关联：最小预测/因果状态的经典背景；不是本框架中全部受控预算结果的现成证明。

**[W5] David L. Donoho, Richard C. Liu.** *Geometrizing Rates of Convergence, II*. Annals of Statistics 19(2) (1991), 633–667, DOI:10.1214/aos/1176348114；以及 Part III, 668–701, DOI:10.1214/aos/1176348115。  
关联：模量与统计难度。另核对 Angelika Rohde, Lukas Steinberger, *Geometrizing rates of convergence under local differential privacy constraints*, Annals of Statistics 48(5) (2020), arXiv:1805.01422：说明噪声/隐私协议改变相关模量，而双边速率需要条件。

**[W6] Paul Dupuis, Hui Wang.** *Subsolutions of an Isaacs equation and efficient schemes for importance sampling*. 公开作者稿 `subsoln_rev1.pdf`，Brown University 作者页面。  
关联：指数积分与相对熵变分公式、控制语义。T09 给出独立短证明以固定本总纲的符号。

**[W7] S. R. S. Varadhan.** *Large Deviations*, Spring 2010 lecture notes, Sections 1–2，尤其 Theorem 2.7。纽约大学作者页面。  
关联：contraction principle、速度与拓扑条件、Laplace 原理的标准背景。

## 17.3 本总纲新提出的部分

新提出的是：本项目采用的 A0–A5 对象/资源接口；将三种几何映射分开的规范；因果模拟器的资源与误差证书；T01–T12 在本项目中的依赖排列；E4 对此前无条件内存单调说法的直接校正；G1–G4 的主定理目标及与现有论文的接入方式。

这些是可供后续全文采用的研究规范。是否构成新的可发表数学贡献，取决于完成 G1–G4 中实际超出既有成果的定理，而不是命名本身。

---

# 18. 最终固定的总纲声明

> General Theta Foundations 以正的因果实验、合法未来测试、真实准备和资源可执行性为基础。它先构造预测商及实际可达几何，再在明确附加条件下构造正规信息、奇异模量、有限内存、压力、率函数和动力学记忆。归约通过可执行核和策略提升定义，各层按照自己的正确传递法则相容。不存在以单一 rank、Fisher 矩阵或标量压力替代全部层次的默认公理。

这保留了新 geometry 路线的广义潜力，同时给旧 theta 的物理、谱、LDP、cotangent 和 memory 工作保留了不可替代的证明位置。
