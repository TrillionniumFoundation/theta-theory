# CM2 v63 根信任、非铸造与有向 Frostman 终端归并报告

**日期：** 2026-08-26  
**控制 predecessor：** `b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab`（r63bd）  
**策略：** latest-wins / append-only / fail-closed / reference 不得晋升 production

## 0. 控制结论

本轮继续攻击了“外部实际性”与 terminal PPE 的最后内部语义。完成的不是一个 synthetic positive bundle，而是一个**默认不能生产 credit 的非铸造 observer**：分布式源码没有任何 production bootstrap key，所有 reference 输出的 literal granted credit 均为零。

```yaml
InternalMathematicalReduction: CLOSED_THROUGH_V55
RootedActualityProtocol: CLOSED_REFERENCE_IMPLEMENTATION_V63
FutureCodedGraphFrostmanCriterion: CLOSED_REFERENCE_ONLY
ReferenceAndHostileTests: 75/75_PASS

ProductionBootstrapRoots: UNCONFIGURED
RealR63bdBytes: NOT_MOUNTED
RealC79gSuccessor: NOT_EXECUTED
D02A: NOT_EXECUTED
D02B: NOT_EXECUTED
D02C: NOT_EXECUTED
D03: UNAUTHORIZED
D04: NOT_MINTED
Gate5: 10/18
CompleteGlobalBlocks: 0
FreshCleanRoom: NOT_EXECUTED
ActualMathPackets: NOT_SUPPLIED

CM2: NO_GO_FOR_CLAIM
formal_global_closure_credit: 0
D02_unlock: false
cm2_claim_credit: 0
```

## 1. 新 hostile blockers 与修复

### 1.1 自选根信任

旧设计把 anchor 文件和 expected anchor SHA 同时交给同一命令行调用者。候选可自行生成 key/anchor/digest；“文件位于 workspace 外”并不产生预存信任。

v63 修复：

- production root 只能来自候选产生前预置在独立测量源码中的离线 bootstrap 公钥；
- policy 必须满足离线阈值签名、版本下限与有效期；
- distributed reference build 的 root 常量为空，所以 production 模式硬拒绝。

### 1.2 freshness 与 replay

单个非空 `signed_at` 字段可无限重放。v63 引入：

- 256-bit nonce；
- 不超过 600 秒的 challenge window；
- monotone sequence；
- 同 tree head 绑定的 fresh revocation statement；
- witness-signed previous-to-current checkpoint transition。

### 1.3 递归 snapshot 与路径攻击

一层目录检查看不到 nested symlink。v63 通过 held dirfd 递归计算 snapshot digest，拒绝：

```text
symlink / device / FIFO / socket
hard-linked regular file
repeated directory inode
file drift during read
device or mount crossing
```

### 1.4 verifier 自哈希循环

不能把包含自身的 verifier chain SHA 再硬编码到自身源码。v63 只预置离线 bootstrap 公钥和最低 policy version；bootstrap-signed policy 绑定实际 verifier measurement，measurement 再由独立 attestation 与 transparency log 复核。

### 1.5 revocation 不得从 inclusion 自动推出

Transparency inclusion 与 signed tree head 只证明“被记录”，不证明 key 当前未撤销。v63 将 fresh threshold-signed revocation statement 的 digest 放入同一 tree head，并由独立 witness threshold 签名 previous/current checkpoint transition。

### 1.6 local observer 不得二次铸造

v63 把外部 decision 的正值放入 `observed_*` 字段；local receipt 的字面字段恒为：

```text
receipt_granted_formal_global_closure_credit = 0
receipt_granted_D02_unlock = false
receipt_granted_cm2_claim_credit = 0
```

外部 threshold decision 与 journal 才是可能的 authority 对象。

## 2. Future-coded graph-directed Frostman/PPE

终端 projective coordinate 采用 future-coded pullback：

\[
\nu_i=\sum_{e:i\to j}p_e(\phi_e)_*\nu_j,
\qquad x_n=\phi_{e_n}(x_{n+1}).
\]

已经发生的 finite prefix 必须剥离，不能重复计入终端收缩。对 primitive finite graph、同 source 的 disjoint affine images，以及

\[
p_e\le a_e^\beta,
\]

可得统一 Frostman bound `nu_i(I) <= C |I|^beta`。当 `beta=r/q` 时，reference verifier 精确检查 `p_e^q <= a_e^r`。

若 complete amplitude 具有 stopped-parent conditional `L^p` moment，physical slope map 在 terminal charts 上横截，则 weighted PPE 可用指数为

\[
\beta_{\rm weighted}\le\beta\frac{p-1}{p}.
\]

本轮的 rational two-state reference packet得到：

```text
raw beta = 1/2
amplitude p = 2
available weighted beta = 1/4
claimed weighted beta = 1/4
actual_billiard_binding = false
credit = 0
```

它关闭的是有限图 sufficient criterion，不生成 actual future stationarity、physical slope identity、record-compatible stopped tree 或 complete amplitude moment。

## 3. 机器验证

运行 8 个模块：

```text
C79g persisted authority v1          8
C79g whole-transaction authority v2 11
serial-tail reference verifier       7
actual-bundle verifier v2             9
projective/phase exact verifier       5
terminal closure v55                 10
rooted actuality observer v63        13
future graph Frostman verifier v63   12
---------------------------------------
total                                75
```

结果：`75/75 PASS`，失败和 timeout 均为 0。全部 Python 源码通过 `py_compile`；8 个 v63 JSON schemas 通过 Draft 2020-12 schema validation。

## 4. 数学 successor 与 PDF 审计

新增：

```text
cm2-bridge-note-v63-rooted-nonminting-oriented-terminal.tex
cm2-bridge-note-v63-rooted-nonminting-oriented-terminal.pdf
```

审计：

```text
TeX lines:             14,746
TeX bytes:             685,491
PDF pages:             175
labels:                778 unique / 0 duplicate
references:            1,279 / 0 undefined
LaTeX warnings:        0
overfull boxes:        0
underfull boxes:       0
control characters:    0
```

已渲染第 1、80、160、167--175 页；第 1/80/160 页与 v55 像素完全一致。新页面 ink bounding boxes 保持在安全页边距内。

## 5. 当前真实工作区边界

只读 preflight 对 `/mnt/data` 给出：

```text
required r63bd deliverable files missing: 9
required runtime paths missing:            8
status: BLOCKED_MISSING_OR_DRIFTED_REAL_ARTIFACTS
```

因此本轮不能合法执行新 C79g successor 或 D02。aggregate Markdown、reference packet、测试 key 或本地 observer 均不得替代真实字节。

## 6. 剩余 gap 的唯一分类

当前仍未闭合的对象全部属于 actual/external，而非另一条内部 Markdown 箭头：

1. 独立测量、预置 offline roots 的真实 production verifier/policy；
2. 完整 r63bd predecessor/source/runtime bytes；
3. C79g positive 后的 D02-A 33,638、D02-B 7,463/14,926 到 1,648、D02-C 862/76,832；
4. D03、D04、同一 D04 key 的完整 Gate5 block 与 fresh clean-room；
5. global singular atlas/source/RN、recordwise moments/recovery、future-coded all-depth PPE、independent U3 atom tail、section-to-full phase transfer；
6. 外部 threshold decision、transparency/revocation journal、无 later rejection。

这些对象只有实际进入并通过对应 verifier 后才能改变 truth state。

## 7. 最终状态

```text
all currently identified internally derivable blockers:
  CLOSED THROUGH V63

all actual/external blockers:
  EXPLICITLY TYPED, NOT SUPPLIED

CM2:
  NO_GO_FOR_CLAIM
```

本结论不表示研究问题不可继续；它表示在缺少真实输入时不再把 reference 结果、结构自洽或签名自声明误写成无条件 CM2。
