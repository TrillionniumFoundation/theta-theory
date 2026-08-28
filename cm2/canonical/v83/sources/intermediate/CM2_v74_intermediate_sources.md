# CM2 v74 exact intermediate sources

<!-- BEGIN EMBEDDED v74-report CM2_v74_hepta_development_report_2026-08-27.md SHA256=e9d6a34afad697244332580d847820dd0e0345d950e0b41df38a51e25cc142ac BYTES=1929 -->
# CM2 v74 Hepta Development Execution Report

## Result

The seven remaining BG2--BG8 fields have been converted from open labels into an executable, acyclic development pipeline with strict stage contracts, candidate compilers, numerical gates, a non-minting packet observer, repository overlay, schemas, examples, deterministic packaging, independent verification and hostile tests.

## Implemented

- BG2 raw immutable occurrence/coarea/owner/side candidate compiler;
- BG3 reverse standardisation contract;
- BG4 forward grazing-skip standardisation contract;
- BG5 bidirectional ORGW trace/rooted-domain contract;
- BG6 optimal crossed-rate solver and perturbation-stability radius;
- BG7 finite-DQ rectangular-l1 contract;
- BG8 full-flow CRCC/Kac/roof/observable contract;
- anti-cycle and same-occurrence digest enforcement;
- proof-bundle verifier and release verifier;
- hepta repository overlay with Makefile, schemas and examples.

## Verification

```text
v73 baseline:                  60/60 PASS
v74 local source context:     121/121 PASS
v74 hepta overlay context:    121/121 PASS
v74 fresh release context:    121/121 PASS
v74 repeated assertions:      363/363 PASS
build/replay gates:              6/6 PASS
```

Both the proof bundle and the complete release were built twice and were byte-identical.

## Truth boundary

```yaml
actual_BG2_to_BG8: NOT_SUPPLIED
actual_independent_scatterer_rectangular_CM2: NOT_PROVED
actual_independent_scatterer_full_flow_response: NOT_PROVED
first_truth_changing_blocker: BG2_ACTUAL_GLOBAL_IMMUTABLE_SAME_OCCURRENCE_ATLAS
local_formal_credit: 0
D02_unlock: false
cm2_claim_credit: 0
```

The BG2 compiler emits a candidate geometry ledger. It does not convert example rows or self-declared evidence into an actual theorem. The packet observer can report schema completeness, but actual theorem readiness remains false until independent mathematical proof/review is supplied.
<!-- END EMBEDDED v74-report CM2_v74_hepta_development_report_2026-08-27.md -->

<!-- BEGIN EMBEDDED v74-plan CM2_v74_hepta_development_plan_2026-08-27.md SHA256=541ec729216f89721a7f3ec9e3b81c196acbffecf0922c1984463cc14f5d379b BYTES=11426 -->
# CM2 v74：Hepta（BG2–BG8）深化、细化、优化与下一步开发计划

**版本定位：** v74-hepta-development-overlay  
**基线：** CM2 v73 bi-standard / ORGW / crossed-rate-gap  
**作用域：** independently moving specular dispersing-Sinai scatterer 的 rectangular CM2 与 full physical-time response  
**硬语义：** latest-wins、fail-closed、append-only、reference/observation 不铸造数学真值或 formal credit

## 0. 本版完成了什么

v73 已把剩余 truth-changing object 压缩成 BG2–BG8 七个 actual 字段，但七个字段仍只是开放标签。v74 把它们改造成一条可执行、可并行、可数值拒绝、可独立重放的开发流水线：

```text
BG2 immutable same-occurrence atlas
  ├─> BG3 reverse/source standardisation
  └─> BG4 forward/target grazing-skip standardisation
          BG3 + BG4 + BG2
              -> BG5 bidirectional ORGW trace/rooted domain
              -> BG6 strict rate window
              -> BG7 finite-DQ rectangular l1
              -> BG8 CRCC full physical-time response
```

本版同时实际开发了：

1. 七阶段 DAG 与各阶段的 primitive input、行级字段、退出门、hostile tests；
2. strict canonical JSON proof bundle、self-hash、manifest、只读树、anti-symlink/hardlink verifier；
3. BG2 原始几何账本编译器；
4. BG6 最优 crossed-rate 与不确定性稳定窗口求解器；
5. actual packet schema observer；即使七字段全部自报为绿，也只能输出 schema-complete，不能本地授予数学结论或 formal credit；
6. hepta repository overlay、Makefile、schemas、examples 与独立测试。

## 1. 开发原则

### 1.1 一条 immutable occurrence spine

BG2 生成唯一的 `occurrence_registry_digest`。BG3–BG8 必须原样继承该 digest；以下操作全部 fail closed：

- presentation cut 导致 occurrence rekey；
- reverse 与 forward 使用不同 owner；
- finite-DQ 参数改变 occurrence ID；
- flow 层回头补造 collision occurrence；
- 一侧 graph current 借用另一侧 evidence。

### 1.2 几何、动力、速率、参数极限、物理时间永久分层

```text
BG2 = geometry / coarea / owner / side
BG3–BG4 = one-sided physical regeneration and decay
BG5 = weighted trace/rooted domain
BG6 = numerical bunching/rate decision
BG7 = parameter difference quotient and rectangular l1 limit
BG8 = suspension generator, roof, Kac and inverse-Laplace
```

任何 downstream conclusion 不得反向作为 upstream antecedent。

### 1.3 候选编译与 actual proof 分离

本地工具可以：

- 规范化原始几何行；
- 计算 occurrence digest；
- 检查 owner/side/coarea；
- 聚合 rate constants；
- 计算严格速率 margin；
- 检查 finite-DQ 与 flow packet 的 schema。

本地工具不能仅凭 JSON 自声明：

```text
actual rectangular CM2 = proved
actual full-flow response = proved
formal credit = 1
```

即使一个 packet 的七字段都满足结构验证，本地输出仍固定为：

```yaml
mathematical_packet_schema_observed_complete: true
actual_rectangular_CM2_observed_ready: false
actual_full_flow_response_observed_ready: false
requires_independent_mathematical_review: true
local_formal_credit: 0
```

## 2. Hepta 七阶段详细开发计划

## BG2 — Global immutable same-occurrence atlas

### 原始输入

- 参数化 scatterer geometry；
- hit/tangency equations；
- side orientation；
- owner rule；
- source/target chart 与 branch word；
- coarea Jacobian 上下界；
- common phase realization digest。

### 规范行

```text
occurrence_id
occurrence_digest
family_id
physical_face_id
side
owner_id
source_chart / target_chart
parameter_interval
coarea_lower / coarea_upper
source_word / target_word
evidence_digest
```

### 退出门

```text
occurrence_count > 0
owner_conflict_count = 0
side_incomplete_count = 0
coarea_nonpositive_count = 0
parameter_key_drift_count = 0
coarea_uniform_lower_bound > 0
```

### 已开发

`cm2_v74_bg2_atlas_compiler.py` 可从 canonical raw atlas 输入生成候选 ledger，检查 exact two-side pairing、owner uniqueness、positive coarea 与 immutable digest。它输出 `CANDIDATE_ONLY_EXTERNAL_MATHEMATICAL_REVIEW_REQUIRED`，不伪造 actual status。

## BG3 — Reverse/source-side standardisation

### 目标

把每个 BG2 source-side current 分解成同一 law 上的 signed proper families，并证明统一：

```text
boundary Z moment
recovery-time moment
ordinary source-side decay alpha < 1
```

### 退出门

- BG2 occurrence coverage 精确全覆盖；
- positive/negative Jordan parts 使用同一未选择 law；
- stopped conditional moment，而不是 deterministic-time 平均；
- `alpha` 在全部 occurrence 与参数窗口上一致；
- owner/source word 不漂移。

### 并行化

BG3 与 BG4 可在 BG2 冻结后并行；二者不得互相引用结论。

## BG4 — Forward/target-side grazing-skip standardisation

### 目标

允许一个统一有限 skip depth，将 target-side grazing trace 送入 regular proper families，并证明：

```text
uniform_skip_depth < infinity
boundary Z moment < infinity
recovery-time moment < infinity
ordinary target-side decay beta < 1
```

### 退出门

- skip 不是 occurrence-dependent 无界等待；
- 被 skip 的 grazing/cemetery mass 有完整 conservation；
- post-selection 不允许重新 key；
- 所有 BG2 occurrence 全覆盖。

## BG5 — Bidirectional ORGW weighted trace/rooted domain

定义 forward/backward orbit-resolvent grazing weights：

\[
W_\eta^+(x)=\sum_{j\ge0}\eta^j c(T^jx),\qquad
W_\eta^-(x)=\sum_{j\ge0}\eta^j c(T^{-j}x),
\]

其中 `c` 是实际 grazing cost。BG5 必须实际证明：

```text
0 < eta < 1
forward/backward shift identities
finite weighted means
same-occurrence trace bounds
rooted source bounds
Gamma_plus / Gamma_minus honest upper bounds
```

禁止只证明 scalar mean 而不证明 trace/rooted mapping；禁止跨 occurrence 借用权重。

## BG6 — Strict numerical rate window

首选 crossed-envelope route：

\[
|a_{m,n}|\le C_-\alpha^m\Gamma_+^n,
\qquad
|a_{m,n}|\le C_+\Gamma_-^m\beta^n.
\]

令：

\[
A=\log(1/\alpha),\quad B=\log(1/\beta),\quad
C=\log\Gamma_+,\quad D=\log\Gamma_-.
\]

严格窗口为：

\[
\Delta=AB-CD>0.
\]

最优插值参数和共同率为：

\[
\lambda_*=\frac{B+D}{A+B+C+D},
\qquad
\log\rho_*=\frac{CD-AB}{A+B+C+D}<0.
\]

### 新工具：Rate-margin stability

若每个 log-rate 在参数窗口中变化不超过 `epsilon`，则新 margin 至少为：

\[
\Delta-\epsilon(A+B+C+D)-2\epsilon^2.
\]

所以安全半径为：

\[
\epsilon<\frac{-S+\sqrt{S^2+8\Delta}}4,
\qquad S=A+B+C+D.
\]

这条新 compiler 把 BG6 的点态 strict gap 合法接入 BG7 的参数统一 common envelope。

### 已开发

`cm2_v74_bistandard_rate_solver.py` 直接计算：

- exact/高精度 margin；
- 最优 `lambda`；
- 最优 `rho`；
- uncertainty-adjusted robust margin；
- safe log-error radius。

参考输入：

```text
alpha=1/64
beta=1/16
Gamma_plus=Gamma_minus=2
log_error=0.001
```

得到：

```text
strict margin ≈ 11.0504193201
optimal lambda = 5/12
optimal rho ≈ 0.2648657736
robust margin ≈ 11.0420995540 > 0
```

这只是工具自检值，不是实际 billiard rate。

允许的替代路线继续保留：signed tangent、Rademacher square function、orbit-derivative coboundary、tube-trace、Landau higher derivative、holomorphic schedule disk。

## BG7 — Finite-DQ rectangular l1

BG7 不接受：

```text
fixed-(m,n) convergence only
TV-small deep tail without time summation
parameter-dependent occurrence IDs
moving centering convention
```

必须同时提交：

1. finite head 上 uniform DQ convergence；
2. BG6 生成的一个共同 summable tail envelope；
3. `occurrence_drift_count=0`；
4. `owner_drift_count=0`；
5. `centering_drift_count=0`；
6. full rectangular \(\ell^1(\mathbb N^2)\) limit。

## BG8 — Full physical-time CRCC

必须在一个共同 suspension graph domain 上证明：

\[
\dot Y=[A,Y]+G.
\]

其中 commutator 是 transport/roof gauge，`G` 才是真正 physical insertion。必须提交：

```text
common flow domain
generator / A / G digests
zero-waiting endpoint cancellation
Kac centering
roof and observable derivative scope
twisted resolvent common domain
inverse-Laplace integrable envelope
initial-law/domain scope
full continuous rectangular response
```

禁止 roof derivative 在 commutator与 physical source中重复收费。

## 3. 优化后的关键路径与并行资源

```text
T0  baseline freeze and reproducibility
T1  BG2 physical occurrence compiler + raw geometry producer
T2a BG3 reverse standard-family proof
T2b BG4 forward grazing-skip proof
T3  BG5 ORGW weighted graph domain
T4  BG6 numerical feasibility and robustness
T5  BG7 finite-DQ l1 closure
T6  BG8 physical-time closure
T7  independent mathematical review and paper import
```

资源安排：

- `T2a` 与 `T2b` 并行；
- BG6 solver 可持续读取 provisional rates，但只有 BG3–BG5 冻结后才能出 final margin；
- BG7 的 finite-head atlas可与 BG5 开发并行，但 common tail 只能由 BG6 正门接入；
- BG8 的 roof/Kac bookkeeping可提前开发，但 flow theorem必须等待 BG6/BG7。

## 4. Hepta repository integration

建议将本 overlay 解压到 `hepta-paper-assets` 根目录：

```text
papers/positive-response/CM2_V74_HEPTA_DEVELOPMENT_PLAN.md
papers/response-theory/CM2_V74_IMPORT_BOUNDARY.md
tools/cm2_hepta/*.py
schemas/*.json
tests/*.py
examples/*.json
Makefile
```

Paper 1 只能导入 abstract compilers 和明确通过的 actual fields。Paper 2 / theta-expectation-hjb 只有在 BG2–BG8 actual mathematical packet 与独立审阅都通过后才能把 full moving-response package作为上游输入。

## 5. 本版验证

本地与 overlay 两套独立运行均通过：

```text
v74 hepta proof-bundle tests: 103/103
v74 BG2/rate tool tests:       18/18
single-run total:             121/121
```

攻击覆盖：

```text
hidden file / symlink / hardlink / writable evidence
manifest/self-hash/canonical JSON/duplicate key/NaN
DAG reordering/cycle/downstream circular dependency
owner conflict/side alias/coarea sign/key drift
alpha/beta/Gamma underclaim and equality gate
ORGW shift corruption
finite-DQ moving spike/atlas drift/centering drift
CRCC sign/endpoint/Kac/rate corruption
actual claim escalation and formal-credit escalation
```

## 6. 当前真实状态

```yaml
hepta_plan: FROZEN_AND_MACHINE_CHECKABLE
BG2_raw_candidate_compiler: IMPLEMENTED
BG6_rate_solver: IMPLEMENTED
BG2_to_BG8_contracts: IMPLEMENTED
reference_fixture: STRUCTURALLY_COMPLETE_ZERO_CREDIT
actual_BG2_to_BG8: NOT_SUPPLIED
actual_independent_scatterer_rectangular_CM2: NOT_PROVED
actual_independent_scatterer_full_flow_response: NOT_PROVED
first_truth_changing_blocker: BG2
local_formal_credit: 0
```

## 7. 下一次能改变 truth state 的提交

下一份真正有意义的输入不是再增加 abstract theorem，而是：

```text
一个明确 specular radial/normal-graph family
+ 其完整 BG2 raw atlas rows
+ 独立复算的 owner/side/coarea evidence
```

运行：

```bash
python tools/cm2_hepta/cm2_v74_bg2_atlas_compiler.py \
  actual_bg2_raw_atlas.json \
  bg2_candidate.json
```

只有 candidate 经几何证明与独立数学审阅后，才可转换为 `CM2_HEPTA_BG2_ACTUAL_EVIDENCE_V1`。随后 BG3/BG4 才是合法下一阶段。
<!-- END EMBEDDED v74-plan CM2_v74_hepta_development_plan_2026-08-27.md -->
