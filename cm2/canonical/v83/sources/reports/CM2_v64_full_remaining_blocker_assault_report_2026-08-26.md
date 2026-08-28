# CM2 v64 全量剩余 blocker 攻坚报告

**生成时间（UTC）：** 2026-08-26T15:00:48Z  
**控制前序：** `r63bd / b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab`  
**策略：** `LATEST-WINS / FAIL-CLOSED / APPEND-ONLY / NO-FALSE-CM2-CLAIM`

## 0. 结论

本轮从 v63 的可执行源码出发，重新做 hostile theorem/protocol audit，而不是重复接受 v63 的“内部已闭合”结论。审计复现并修复了以下新 blocker：

1. challenge 没有严格绑定 policy workspace、terminal envelope 和 predecessor scope；
2. external decision 没有严格绑定已经验证的 policy id/version；
3. C79g pre-D02 authorization、D02 global closure 和最终 CM2 claim 可被一次性混铸；
4. authority journal 可以从零 head 截断重启；
5. journal timestamp 可以回滚；
6. adverse event 的 scope 与 target decision 可以错配；
7. v63 graph-directed Frostman 证明没有把全深度 stopping-antichain packing 常数显式化。

以上内部缺口均在 v64 reference successors 中修复并有负向测试。严格正式状态仍是：

```yaml
CM2: NO_GO_FOR_CLAIM
formal_global_closure_credit: 0
D02_unlock: false
D02_started: false
D03: UNAUTHORIZED
D04: NOT_MINTED
Gate5: 10/18
complete_global_blocks: 0
fresh_five_gate_clean_room: NOT_EXECUTED
```

这不是因为又遗漏了一条可由 Markdown 或 synthetic fixture 生成的箭头，而是因为真实 r63bd predecessor bytes、真实 runtime namespaces、production D02 ledgers 和 actual mathematical packets 不在当前工作区中。

## 1. v64 rooted ingress

活动实现：`cm2_rooted_ingress_verifier_v64.py`

新增约束：

- strict canonical JSON：拒绝 duplicate keys、NaN/Infinity、finite float、non-NFC 和 control characters；
- policy id/version floor 与 controlling checkpoint 固定；
- role key ids 和 public keys 全局互斥；
- challenge 同时绑定 scope、workspace、previous decision、candidate、terminal envelope、trusted time；
- hermetic receipt 同时绑定 challenge/policy/scope/workspace/candidate/evidence/snapshot/verifier measurement；
- non-root、zero capabilities、`no_new_privs`、no ptrace/network/dynamic code、read-only snapshot、fs-verity/IMA；
- transparency inclusion、append-only consistency、fresh signed tree head、witness threshold 和 fresh revocation；
- local verifier 始终输出 zero-credit observation。

测试：`16/16 PASS`。

SHA-256：`1cf049161340d29f41afa0df1e3591c52c442a0eb70e5f0220fe834ff19a8ea7`

## 2. 七阶段 authority credit lattice

活动实现：`cm2_scoped_authority_chain_verifier_v64.py`

唯一合法阶段：

```text
C79G_PRE_D02_AUTH
  -> D02_GLOBAL
  -> D03_PASS
  -> D04_REGISTRY
  -> GATE5_GLOBAL
  -> FIVE_GATE_CLEAN_ROOM
  -> CM2_CLAIM
```

关键语义：

- C79g 只允许 `c79g_pre_d02_credit=1` 和 `D02_unlock=true`；
- D02 closure、D03、D04、Gate5、clean-room 和 CM2 claim 逐阶段累积；
- `cm2_claim_credit=1` 只允许在第七阶段；
- decision 必须绑定 policy、ingress receipts、candidate/evidence、previous decision digest 和 checkpoint；
- final decision 额外绑定 terminal candidate 和 math packet root；
- dedicated decision keys 与 journal keys；
- policy 固定 previous journal head，禁止从零重启；
- journal decision order 必须与 scope lattice 一致；
- timestamp 单调，head freshness 有上限；
- 任意 well-typed later rejection/revocation/supersession 都使 positive chain fail closed；
- adverse scope/target 错配本身即拒绝；
- local observation 永不二次铸造 credit。

活动 exact seven-stage 测试：`20/20 PASS`。另一个早期 two-stage v64 experiment 已在 latest-wins manifest 中标为 superseded，不是活动 authority verifier。

SHA-256：`bdc0d586182796d08b6d0065a70a9f5a98df37538791307cefd699f8ab2c7b3a`

## 3. All-depth stopping-antichain Frostman/PPE

活动实现：`cm2_stopping_antichain_frostman_verifier_v64.py`

v63 只检查有限 graph 的 primitive、sibling disjointness 和 edge inequality。v64 显式定义 first-crossing stopping antichain：

```text
A_i(r) = { w : a_w <= r < a_parent(w) }
```

令 `a_* = min_e a_e`，则每个 stopping cylinder 满足：

```text
a_* r < a_w <= r.
```

若 inverse physical-slope chart 把目标小球拉回到长度至多 `2 L r` 的 interval，则每 chart 最多相交

```text
M_L = ceil(2 L / a_*) + 2
```

个 stopping cylinders。由 cylinder Gibbs upper bound 和 `q_e <= a_e^beta`：

```text
nu_i(J) <= C_G M_L r^beta.
```

对最多 `N_ch` 个 charts 和 complete nonnegative amplitude `M`，若

```text
E[M^p | F_parent] <= K_p,   p > 1,
```

则：

```text
E[M 1{|S-t|<=r} | F_parent]
  <= K_p^(1/p) (C_G N_ch M_L)^(1/p') r^(beta/p').
```

reference rational packet 的 exact 结果为：

```text
beta = 1/2
p = 2
available weighted beta = 1/4
minimum contraction = 1/3
charts = 3
inverse Lipschitz = 2
M_L = 14 per chart
raw constant upper = 84
actual_billiard_binding = false
credit = 0
```

测试：`14/14 PASS`。

SHA-256：`5e43adb0b56990977d7481c301b2e170ca074c0650d09b38eedb3b004d7ba038`

## 4. 全量机械验证

本轮重跑历史 active/superseded regression suites 与 v64 suites：

```text
12 suites
141 tests
141/141 PASS
```

完整日志：`CM2_v64_all_tests.log`  
日志 SHA-256：`17139b6a913c949c0606a4b129bfbdc39eb0b6a148fd7a2b2b05c14d99e83603`

## 5. 数学主文 v64

生成：

- `cm2-bridge-note-v64-scoped-journal-antichain-terminal.tex`
- `cm2-bridge-note-v64-scoped-journal-antichain-terminal.pdf`

静态/排版结果：

```text
TeX lines:                 15,069
TeX bytes:                 699,381
unique labels:             796
references:                1,290
undefined references:      0
bibliography items:        45
missing citation keys:     0
control characters:        0
PDF pages:                 179
LaTeX warnings:            0
overfull boxes:             0
underfull boxes:            0
PDF preflight:             PASS
baseline pages 1/80/160:   pixel-identical to v63
new pages 173-179:         rendered and visually inspected
```

```text
TeX SHA-256: 100e7cb64b90f0e45a342ffdbc6e1953a745f46d5c33743d66c7d3b0d208def9
PDF SHA-256: bb12178bd0606f5e9f0b385b554980b9d49bcd75be8794fd20da8607d32a3032
```

## 6. 最新文献边界复核

本轮重新核对的一手结果可提供相邻组件：

- Furstenberg measure 的 Frostman information（紧支撑 i.i.d. SIP matrix products）；
- finite mixing symbolic base 上 typical/fiber-bunched cocycle 的 transfer-operator/Gibbs 结构；
- sequential dispersing billiards 的 projective cones、memory loss 与 limit-law machinery；
- moving scatterer sequences 的统计稳定性与 memory loss；
- discontinuous perturbation/small-hole response 的标准族或条件响应工具。

这些结果没有一篇直接同时给出本项目需要的 moving-face current、immutable occurrence/source/RN matching、actual stopped-parent complete amplitude、future slope identity、production D02 geometry 和 section-to-full response packet。故它们缩短证明路线，但不能替代 actual packet。

## 7. 真实工件 preflight

对当前 `/mnt/data` 和 Library 的只读检查：

```text
required r63bd deliverables: 9
found/pass:                  0
required runtime paths:      8
found/pass:                  0
status: BLOCKED_MISSING_OR_DRIFTED_REAL_ARTIFACTS
```

Library 的非模型生成文件只有 canonical CM2 总卷、`theta_theory_recursive.md` 和一个旧 theta/Navier-Stokes master；没有隐藏的 r63bd deliverables/runtime archive。

所以本轮没有且不能合法执行：

```text
real C79g successor
D02-A 33,638 tasks
D02-B 7,463 reps / 14,926 sides / collision 3-1648
D02-C 862 Kraft parents / 76,832 census / formal unresolved=0
D03
D04
same-key Gate5 18/18
fresh five-gate clean-room
actual general-moving-singularity U3 packet
```

## 8. 最终状态

```yaml
InternalDerivationAndProtocolGapsIdentifiedThroughV64: CLOSED
RealR63bdBytes: NOT_SUPPLIED
RealC79gPersistedAuthority: NOT_EXECUTED
D02Tail: LOCKED
ActualMathPackets: NOT_SUPPLIED
formal_global_closure_credit: 0
D02_unlock: false
cm2_claim_credit: 0
CM2: NO_GO_FOR_CLAIM
```

这里的 `CLOSED` 只指截至 v64 hostile audit 已识别、且能由现有材料合法修复的内部类型/协议/推导缺口。它不把缺失的真实系统事实、运行字节或外部 authority event 改名为内部证明。
