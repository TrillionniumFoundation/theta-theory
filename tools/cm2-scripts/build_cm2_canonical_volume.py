#!/usr/bin/env python3
"""Build a canonical, latest-wins CM2 handoff volume.

This is an editorial merger.  It never edits the source report or any runtime
artifact.  The exact source bodies are copied byte-for-byte into a new Desktop
file and then checked by digest after construction.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from pathlib import Path


ROOT = Path("/home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572")
DESKTOP = Path("/home/qian-qi/桌面")
REPORT = DESKTOP / "CM2_无条件攻坚全量审计报告_2026-08-26.md"
OUT = DESKTOP / "CM2_无条件攻坚_Canonical_Latest-Wins_非递归单一总卷_through_r63bd_2026-08-26.md"
THETA_TOTAL = Path("/home/qian-qi/下载/theta_theory_navier_stokes_initial_md_all_chat_canonical_latest_nonrecursive_through_v11120_2026-08-26.md")
THETA_RECURSIVE = Path("/home/qian-qi/下载/theta_theory_recursive.md")
ARTICLE_ROOT = Path("/home/qian-qi/hepta-paper-assets/submission/AoM/A_Theory_of__Expectations")

CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
REPORT_SHA_EXPECTED = "7c5377103255796d36568f49e51a7d15d13e0a2d946f1ee00087bc96d1afc110"
THETA_TOTAL_SHA_EXPECTED = "add16c7ef289b4756e1def42f65a684b9e01e902567a14779c002026ecfa602c"
THETA_RECURSIVE_SHA_EXPECTED = "afa3dac37ad8704fa2e1b226f21706ed435ba7f32a7a35770f6f16674e084a2a"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path) -> bytes:
    return path.read_bytes()


def line_count(data: bytes) -> int:
    if not data:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def rel(path: Path) -> str:
    """Use a stable absolute path in the handoff, without resolving symlinks."""
    return str(path)


def stat_row(path: Path) -> dict[str, object]:
    data = read(path)
    return {
        "path": path,
        "bytes": len(data),
        "lines": line_count(data),
        "sha": digest(data),
    }


def markdown_table(rows: list[dict[str, object]], headers: tuple[str, ...]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
    return "\n".join(out)


def exact_marker(row: dict[str, object], label: str) -> bytes:
    return (
        f"<!-- BEGIN EXACT {label}: {rel(row['path'])}; "
        f"SHA256={row['sha']}; BYTES={row['bytes']}; LINES={row['lines']} -->\n"
    ).encode("utf-8")


def end_marker(row: dict[str, object], label: str) -> bytes:
    return f"\n<!-- END EXACT {label}: {rel(row['path'])} -->\n".encode("utf-8")


def excerpt(path: Path, ranges: list[tuple[int, int]]) -> str:
    lines = read(path).decode("utf-8").splitlines()
    chunks: list[str] = []
    for start, end in ranges:
        if start < 1 or start > len(lines):
            continue
        end = min(end, len(lines))
        chunks.append(f"# lines {start}-{end}\n" + "\n".join(lines[start - 1 : end]))
    return "\n\n".join(chunks)


def selected_memory_paths() -> list[Path]:
    pattern = re.compile(
        r"cm2|five.?gate|c79g|moving[- ]face|source[- ]g|source[- ]w|"
        r"susceptibility|q2(?:/reset)?|canonical-authority",
        re.IGNORECASE,
    )
    paths: list[Path] = []
    for path in sorted((ROOT / "memory").glob("*.md")):
        data = read(path)
        if pattern.search(data.decode("utf-8", errors="replace")):
            paths.append(path)
    return paths


def article_paths() -> list[Path]:
    names = [
        "draft/three-paper-split-plan.md",
        "draft/three-paper-content-coverage-audit.md",
        "paper_discussion_summary.md",
        "papers/positive-response/cm2-bridge-note.tex",
        "papers/response-theory/main.tex",
        "papers/theta-expectation-hjb/main.tex",
        "papers/representation-calculus/main.tex",
    ]
    return [ARTICLE_ROOT / name for name in names]


def build_wrapper(
    generated: str,
    report_row: dict[str, object],
    article_rows: list[dict[str, object]],
    memory_rows: list[dict[str, object]],
    theta_rows: list[dict[str, object]],
    deliverable_count: int,
) -> str:
    article_manifest = markdown_table(
        [
            {
                "Role": "predecessor/source",
                "File": rel(row["path"]),
                "Bytes": row["bytes"],
                "Lines": row["lines"],
                "SHA-256": row["sha"],
            }
            for row in article_rows
        ],
        ("Role", "File", "Bytes", "Lines", "SHA-256"),
    )
    memory_manifest = markdown_table(
        [
            {
                "File": rel(row["path"]),
                "Bytes": row["bytes"],
                "Lines": row["lines"],
                "SHA-256": row["sha"],
            }
            for row in memory_rows
        ],
        ("File", "Bytes", "Lines", "SHA-256"),
    )
    theta_manifest = markdown_table(
        [
            {
                "Role": row["role"],
                "File": rel(row["path"]),
                "Bytes": row["bytes"],
                "Lines": row["lines"],
                "SHA-256": row["sha"],
            }
            for row in theta_rows
        ],
        ("Role", "File", "Bytes", "Lines", "SHA-256"),
    )

    theta_excerpt = excerpt(
        THETA_RECURSIVE,
        [(1, 18), (1093, 1110), (1250, 1262), (3677, 3686), (27630, 27645), (28025, 28135), (169460, 169490)],
    )

    return rf'''# CM2“无条件”攻坚：初始问题 + 全部实质审计推进
# Canonical Latest-Wins 非递归单一总卷 through r63bd

**Generated:** `{generated}`  
**Edition:** `INITIAL-CM2-PROBLEM + ALL-SUBSTANTIVE-AUDIT-CONTINUATIONS / CONTROLLING-r63bd / SINGLE-ENTRY / NONRECURSIVE-MERGE`  
**Policy:** `LATEST-WINS / FAIL-CLOSED / PRESERVE-PROVENANCE / NO-FALSE-CM2-CLAIM / APPEND-ONLY`  
**Nature:** `EDITORIAL CONSOLIDATION / NO NEW AUTHORITY / NO NEW MATHEMATICAL THEOREM CLAIMED BY THIS MERGE`  
**Controlling checkpoint:** `{CHECKPOINT}`

> 这份卷是为了让后续更强模型能一次获得 CM2 的问题起源、证明依赖、历轮攻坚、失败原因、证据分层、当前物理状态和唯一合法后续计划。它不制造新的数学定理、authority、manifest、seal、rejection 或 D02 credit。
>
> `PART I` 是本卷的控制性解释；`PART II` 逐字嵌入桌面上的原始全量审计报告；`PART III` 嵌入前置论文/bridge 的 exact source body；`PART IV` 嵌入与 CM2 直接相关的 durable-memory provenance。嵌入历史中的旧 `PASS`、`CLOSED`、`GO`、版本号和计划不能覆盖本卷的 `r63bd` terminal state。
>
> 本卷不是聊天界面的逐字 transcript。重复的“按最新 plan 冲”、过程播报、上传通知和重复链接不机械复制；它们产生的实质内容由 exact audit body、source manifest、memory provenance 和本卷的 latest-wins ledger 承载。

---

# PART I — CONTROLLING CM2 MASTER BODY

以下第 `0–14` 节是本卷的控制性、非递归、latest-wins 解释层。它把问题起源、论文依赖、CM2 数学桥、证据/authority 语义、历轮推进和当前终态集中到一个入口；它不产生新的 authority、数学定理或 credit。

# 0. 当前 latest-wins truth state

```yaml
Document:
  ControllingRound: r63bd
  EffectiveCheckpoint: {CHECKPOINT}
  GeneratedLocal: {generated}
  Edition: INITIAL_CM2_PROBLEM_PLUS_ALL_SUBSTANTIVE_AUDIT_CONTINUATIONS
  MergeNature: EDITORIAL_ONLY_NO_NEW_AUTHORITY
  Policy: LATEST_WINS_FAIL_CLOSED_PRESERVE_PROVENANCE_APPEND_ONLY

CM2:
  claim: UNCONDITIONAL_CM2_GLOBAL_CLOSURE_CERTIFICATE
  status: NO-GO_FOR_CLAIM
  formal_global_closure_credit: 0
  D02_unlock: false
  D02_started: false
  canonical_pointer_written: false
  later_rejection_present: true
  current_rejection: r63bd

StaticAndStandaloneEvidence:
  source_schema_contract_transition_launcher_static_gates: 34/34
  schema_definitions: 46
  schema_references: 242
  unresolved_schema_references: 0
  exact_attack_census: 137/137
  candidate_public_unresolved: 0
  successor_rows: 76832
  Kraft_parents: 862
  candidate_and_verification_bytes_inode_independent: true
  terminal_replay: PASS_STANDALONE
  formal_credit_granted_by_these: false

TailChain:
  D02A_pending_tasks: 33638
  D02B_target_representatives: 7463
  D02B_target_physical_sides: 14926
  D02B_collision_limit: 1648
  D02C_target: 862_PARENT_KRAFT_PLUS_76832_FOUR_CLASS_CENSUS_PLUS_FORMAL_UNRESOLVED_ZERO
  D03: UNAUTHORIZED
  D04: NOT_MINTED
  Gate5: 10/18
  complete_global_blocks: 0
  fresh_five_gate_clean_room: NOT_EXECUTED

TruthBoundary:
  candidate_public_unresolved_zero_is_formal_zero: false
  transient_virtual_root_is_persisted_authority: false
  static_pass_is_runtime_authorization: false
  local_or_branch_closure_is_global_closure: false
  CM2_claim_permitted: false
```

**当前控制性一句话：** 大量局部、候选和负向审计已经可复核；但没有可持久化、可独立 replay、且没有 later rejection 的 canonical positive authority，所以 C79g 仍为 `NO-GO`，D02 及尾链锁定，不能宣称 CM2。

---

# 1. 文档定位、范围和阅读契约

## 1.1 这份卷要解决的交接问题

桌面原报告已经是一次完整的 CM2 审计汇总，但它以“审计报告”形式组织。更强模型在继续攻坚时还需要先知道：

1. CM2 从哪个科学/数学母问题中产生；
2. 三篇前置文章各自负责哪一段，哪些只是接口骨架；
3. CM2 bridge 为什么是 Paper 1→Paper 2 的上游瓶颈；
4. five-gate、Source-G/Source-W、C79g、D02 是数学对象、证据对象还是授权对象；
5. 哪些历史 `PASS` 只在 local、conditional、candidate 或 relative-rule-set 作用域内；
6. 现在究竟可以做什么，哪些动作在 fail-closed 规则下明确禁止。

本卷把这些内容放在 exact audit body 之前，便于模型先建立正确的类型和依赖，再读取细节。

## 1.2 控制规则

- 本卷第 `0–14` 节和最后的 `FINAL CONTROLLING INTERPRETATION` 控制当前解释。
- `PART II` 的原报告是 exact source；它的字节不在本次合并中改写。
- `PART III/IV` 是 provenance；其中较早的条件定理、候选结果、旧版本和已撤回结论只能用于 source archaeology。
- 后续编号的 `RETRACTED / CORRECTED / SUPERSEDED / FORBIDDEN / LATEST-WINS` 覆盖较早同类断言，但不会删除历史字节。
- 任何 `PASS` 必须连同作用域、输入假设、是否 actual、是否 persisted、是否有 later rejection 一起读取。
- 本卷不把“报告中列出的文件”当作当前工作区一定可访问；路径和 digest 是 provenance 线索，实际复核仍需对照文件系统。

## 1.3 重要的负声明

这不是把 CM2 改名成 theta-theory，也不是把 theta 的形式闭合改写成 CM2 positive。它只把现有信息整理成一个更适合模型摄入的 canonical dossier。

---

# 2. CM2 的起源问题：先有哪个母问题，为什么会出现 CM2

## 2.1 科学母问题

原始研究线想从确定性的有限视界 Sinai/Lorentz 台球出发，而不是把随机扩散或非线性期望作为原始输入：

```text
deterministic billiard geometry
  → singular collision map / physical-time suspension
  → transfer operators and resolvent response
  → moving-boundary / moving-singularity response
  → cell problem and Green–Kubo coefficients
  → deterministic homogenization
  → gradient-dependent (possibly nonconvex) HJB
  → theta-expectation nonlinear semigroup
  → downstream payoff-dependent BSDE / Girsanov representation
```

其科学意图是：微观层确定、可逆、几何驱动；粗粒化后出现扩散、时间方向和可能非次可加的宏观评价。这里的“first principles”是推导优先级，而不是声称所有台球、所有移动散射体或一般 3D NSE 自动满足同一普适定理。

## 2.2 为什么早期结果不够

早期稿件有局部正 bump、非 coboundary 周期轨道、renewal/holonomy、moving-face、q2/reset 和 susceptibility 公式，但这些对象之间存在几个不能靠文字顺滑跳过的接口：

- 固定 section、碰撞边界、物理时间悬挂流和各向异性 Banach 空间是否真的 intertwine；
- moving face 微分产生的是 conormal/graph current，而不是普通光滑密度；
- forward 与 reverse 两侧的恢复是否针对同一个 occurrence、同一个 owner、同一个 fibre；
- first-hit/event ownership、coarea、DQ、same-parent 和单次 q 收费是否全局一致；
- finite-depth 或 branch-local 的 unresolved=0 是否能升级为 arbitrary-depth、all-plaque、connected-exterior 的 formal unresolved=0；
- 候选结果、验证器结果和真正 canonical authority 是否分离。

## 2.3 CM2 在数学上从哪里冒出来

对 moving singularity 的无限 susceptibility 求导时，核心形式不是一个普通的一次相关，而是双时间对象。需要类似：

\[
\left|\langle Q^n K_V Q^m g,f\rangle\right|
  \le C\,\tau^m\vartheta^n\,\lVert g\rVert\,\lVert f\rVert,
  \qquad 0<\tau,\vartheta<1.
\]

仅有 `C(τ^m+ϑ^n)` 的加法型估计不够：对 `m,n` 双重求和时不能保证绝对可和。因而需要完整双中心化、past/future recovery、同一 occurrence 的两侧 graph-current 传播和可求和的联合尾界。这个跨时间双向桥后来被命名为 **CM2**。

CM2 因此不是 Paper 3 之后的附加模块，也不是单独的“形式 gate”；它是 Paper 1 moving-singularity response 能否安全成为 Paper 2 输入的上游接口。

## 2.4 为什么后来必须做成 five-gate + C79g

“写出双时间公式”仍不等于对真实 nonconjugate moving-scatterer 证明它。必须把数学责任和证据责任同时落到可审计对象上：

```text
local source / periodic witness / face current
  → owner / fibre / same-occurrence / transition ledger
  → branch and component closure
  → independent no-producer reconstruction
  → persisted canonical authority
  → D02 tail and fresh clean-room
```

five-gate 检查实际对象是否覆盖 topology、stable quotient/kernel、strong return/current、landing join/same-occurrence q 和 support/Kac/Wiener/Abel-Orlicz 等字段；C79g 则是把这些分支性证据合并为一个可以授权或拒绝的全局 consumer。它们同时是数学接口的实例化和证据治理层，不是 theta-expectation 的另一种定义。

---

# 3. CM2 之前拆出的三篇文章：它们各自说什么

## 3.1 拆分的原因和依赖顺序

原母稿约 247 页，同时承担三类不同审稿负担：奇异台球几何/响应、确定性均质化与 HJB/theta、以及下游 BSDE/Girsanov 表示。因此拆分是按证明责任和读者群划分，不是降低 first-principles 主张：

```text
Paper 1: primitive billiard response theory
    → Paper 2: deterministic theta-expectation / nonconvex HJB
        → Paper 3: post-derivation representation calculus
```

Paper 2 依赖 Paper 1 的 verified response package；Paper 3 依赖 Paper 2 已得到的 nonlinear semigroup。

## 3.2 Paper 1 — Response Theory

负责微观动力学到可微响应：

```text
scatterer geometry / specular law
  → singular collision map
  → homogeneity strips, cones, growth, distortion
  → anisotropic Banach spaces / Lasota–Yorke
  → map spectral gap / suspension resolvent
  → moving-singularity trace and response
  → multi-response bounds / regularity-loss budget
```

其目标是给 Paper 2 一个可调用的 response theorem，而不是在 Paper 1 内部完成 HJB。后续审查把“计划中的普适 response package”和“已经真正证明的范围”分开：radial inflation 等 source-specific、低阶、assembly-first 结果有工作性；一般 nonconjugate moving-scatterer 的 all-branch response tree、continuous-time moving-family symbol 和完整高阶 trace 仍未闭合。

## 3.3 Paper 2 — Theta-expectation / HJB

把 Paper 1 的 response interface 当输入，走：

```text
response package + deterministic finite-response mechanical action
  → corrector / Green–Kubo tensor
  → effective H(x,p)
  → viscosity homogenization
  → nonconvex HJB
  → theta-expectation semigroup
```

它讨论 `D(x,p)`、Hamiltonian、半松弛极限、比较原理、非凸性和非次可加性。若 moving-response 接口只是 conditional，Paper 2 就不能独立宣布整条 first-principles 链无条件完成。

## 3.4 Paper 3 — Representation Calculus

这是下游表示理论：

```text
derived nonlinear semigroup
  → fixed-payoff linearization
  → calibrated diffusion / carré-du-champ
  → BSDE
  → Cameron–Martin / Girsanov
```

BSDE/Girsanov 不构成台球到 HJB 的原始机制；它们不会替代 moving-face response，也不会解除 CM2。

## 3.5 拆分稿的真实完整性边界

后来的 coverage audit 发现：三篇抽取稿是接口/证明骨架和选定 proof spine，不是母稿的字节或内容保真复制。母稿有约 `517` 个 labels、`312` 个 theorem-like blocks；抽取稿只保留选定接口。因此不能把“三篇文章都有文件”误读成“三篇普适定理都已独立闭合”。

## 3.6 CM2 bridge note 的地位

CM2 bridge note 是拆分之后为补 Paper 1→Paper 2 缺口单独创建的正响应研究笔记，不是第三篇文章，也不是宏观 HJB 的替代品。其历次版本反复经过 referee-style rejection、条件化和路线删除；它的诚实结论是：在显式 H1–H5、SS、FT、FZ、QT 等实际输入下可以陈述 conditional/pathwise criterion，但不能把这些输入默认为任意 billiard 自动满足。

---

# 4. 与 `theta_theory_recursive.md` 的关系和区别

## 4.1 对应关系（不是等号）

| 前置对象 | recursive 对应 | 精确关系 |
|---|---|---|
| Paper 1 response theory | Scale 0/I + K1/U3 | recursive 把 source、共同空间、压力/扩散和 U3 分开；一般 moving-singularity U3 仍需 actual packet |
| CM2 bridge | K1/U3 内的双时间 graph-current 子问题 | CM2 是具体的双时间衰减/ownership 桥，不等于整个 U3，也不等于 K1.5/K2 |
| Paper 2 HJB/theta | K1 → K1.5 → K2 → K3 → HJB | recursive 增加系数提升、Doob 选择、rough WIP、filter/game 信息结构 |
| Paper 3 representation | HJB → FBSDE/PPDE/dynamic evaluation | recursive 扩展路径依赖、过滤和 Isaacs，但仍将表示放在推导之后 |
| 三篇投稿依赖图 | recursive 数学 DAG 的粗粒度投影 | 前者按论文边界切，后者按“下一层必须由上一层产生”切 |

## 4.2 recursive 真正改严的地方：反馈必须被推导

旧 Paper 2 的 Scale III 已把 `L_fast(Theta(x,∇u^ε))` 写进起始方程，逻辑上更接近“假设微观梯度反馈，再得到 HJB”。recursive 架构要求先由 Scale I/II 产生叶片装配、不变测度、经验流作用量和 Doob tilt；只有在 `π_(x,p)` 集中到 `δ_(Theta(x,p))` 时，才可恢复单值 selector。这是因果顺序的修复，不只是把 Paper 2 写长。

## 4.3 recursive 多出的层

- `K1.5`：把微观响应提升为 `(x,p)` 上的系数/椭圆场；
- `K2`：先选择 Doob 系综，再做外层 WIP/非自治均质化，处理无 reset 跟踪、rough path 和 area anomaly；
- `K3`：区分 soft observation、exact filtering、sequential/simultaneous control、mixed Isaacs 与 pure saddle；
- terminal primitive packets：把内部文字不能生成的 actual fact 交给真实系统数据义务；
- 独立 research-certificate 链：R2 bytes、签名、授权根和 replay，且不与数学 theorem 混同。

## 4.4 recursive 没有凭空产生什么

v164 明确区分：

```text
Syntax / type = COMPLETE
Compiler coverage = COMPLETE_FOR_ALL_LIVE_FRONTIERS
Rule saturation = PASS_RELATIVE_TO_RULESET_V164
Actual scoped Lorentz E2E = ACTUAL_THEORY_PASS
General U3 / finite ALG / infinite ALG / weighted K3-HJB
  = TERMINAL_ACTUAL_PACKET_REQUIRED
Actual universal Lorentz theorem = PRIMITIVE_SYSTEM_PACKETS_REQUIRED
R2 trust = EXTERNAL_ARTIFACT_PACKET_REQUIRED
```

因此 recursive 的“全层级闭合”是 obligation classification 和 producer coverage 的闭合，不是 universal theorem，也不是 C79g positive authority。

## 4.5 最终替代判断

- 作为内部研究架构、依赖图和 soundness 账本，recursive 可以取代三篇文章作为 master roadmap，而且更诚实、更明确。
- 作为 Paper 1 的一般 nonconjugate moving-singularity/CM2 actual proof，不能取代。
- 作为 C79g 的 persisted canonical authority，不能取代。
- 它没有 `C79g`、`formal_global_closure_credit`、`D02_unlock` 或 canonical-authority 接口；其偶然出现的 `CM2` 是数学符号（例如 `CM2^k`）时，也不是本协议。

## 4.6 相关 theta 文件当前状态（只作对照）

`theta_theory_navier_stokes_initial_md_all_chat_canonical_latest_nonrecursive_through_v11120_2026-08-26.md` 的控制状态仍为 `remaining_original_truth_core_count=1`、`General3DNavierStokesRegularity=NOT_PROVED`、`AllPhysicalGapsClosed=false`；v11120 的 TIPR_OCM same-parent octave-current no-reuse、full-tail Oseen rigidity、pressure/Reynolds/LEI/root/graph/radial/spectral provenance 和 actual suitable ancestry 仍是 open frontier。

---

# 5. CM2 术语、证据等级和接受语义

## 5.1 四种证据等级

1. **Formal authority**：规范路径持久化、原子提交/fsync、独立 replay 找回，并同时满足 credit、D02、canonical pointer、无 later rejection。
2. **Standalone evidence**：候选/验证器独立重算、字节和 inode 可核对，但不授予 formal credit。
3. **Static proof**：AST/token/schema/contract/transition/launcher 边界闭合；它只说明允许如何运行。
4. **Rejection/supersession**：失败不可原地修补；产生新后继/拒绝，旧字节保留。

## 5.2 两个不能混用的 unresolved

`candidate/public unresolved=0` 只说明候选层的 `76,832` rows 已被四类 census 归档；`formal/global unresolved=0` 还要求全局 owner/fibre/transition、权威 root、canonical pointer、独立 replay 和无后置拒绝。两者不是同一个布尔量。

## 5.3 Five-gate 正式含义

| Gate | 责任 | r63bd 正式状态 |
|---|---|---|
| G1 | topology / all-plaque / affine tangent | 没有可导入的全局 all-plaque closure |
| G2 | stable quotient / kernel / Frostman / RN | formal promotion `0/17`，joint law 未闭合 |
| G3 | strong return / Q-R-Piola-MT_DQ | 没有 arbitrary-depth physical owner/return closure |
| G4 | landing join / same-occurrence q | 只有 local `1/7`，不能升格全局 |
| G5 | support / Kac / Wiener / Abel-Orlicz / 18 fields | global `10/18`，complete global block `0` |
| composite | 五门合并与权威 | `0/5`，未形成正权威 |

`local 18/18` 不等于 global 18/18；它只表示有限候选字段齐全。

## 5.4 C79g 四项 AND 正门

```text
formal_global_closure_credit = 1
AND D02_unlock = true
AND canonical pointer persisted and independently replayable
AND no later rejection
```

任何 transient stdout、virtual root、candidate census 或“3 项已经有了”都不能抵扣缺失项。

## 5.5 尾链依赖

```text
C79g positive wrapper
  → D02-A: 33,638 tasks
  → D02-B: 7,463 reps / 14,926 sides through collision 1,648
  → D02-C: 862-parent Kraft + 76,832 four-class census + formal unresolved=0
  → D03
  → D04
  → Gate5 18/18 + at least one complete global block
  → fresh five-gate clean-room
  → only then CM2 claim
```

---

# 6. 全部攻坚历程的阶段地图

下表是控制摘要；每个阶段的逐项数字、hash 和失败原因在 `PART II` exact report 及 `PART IV` memory archive 中保留。

| 时段/轮次 | 主要责任 | 关键推进 | 永久边界 |
|---|---|---|---|
| 2026-07-10 | response-theory referee repair | 固定表/移动流、conormal source、BDL、S1–S3 作用域重划 | 一般 moving family 的 transverse response 仍 conditional |
| 2026-07-11–07-14，CM2 bridge v8–v51 | 双时间桥、QNL、renewal、q2/reset、物理 SRB | local bump、周期 witness、双中心化和若干可行性路线 | generic nonconjugate all-order gluing/infinite susceptibility 未闭合 |
| R1–R61，07-15–07-20 | five-gate 初始攻坚 | local graph、tail、周期环、Borel、kernel、landing join | composite `0/5`，G5 global `10/18`，G2 `0/17` |
| R62–R87，07-21–07-22 | RN/holonomy、fixed-depth rank-3 registry | 端口、曲线、tail、physical face 预审与严格拒绝 | 有限深度不推出 arbitrary-depth；Gate1/2/3 未认证 |
| R88–R123，07-22–07-23 | face/port/trace | 纠正 generator-consumption bug；120 trusted physical ports；12 faces/108 links | physical face 不能仅凭 endpoint/coordinate identity 获得 global credit |
| R124–R160，07-23–07-25 | local 18/18 与厚度 atlas | `[0,100000]` finite atlas、531,139 tests 等 | mechanical upper-tail limitation |
| R161–R204，07-25–07-27 | Source-W/G owner 与 seam | corridor 推到 `2.5e15h`；大量 owner/incidence ledger | component membership、maximality、exact-key fibre 仍未全局闭合 |
| R205–R241，07-27 | occurrence frontier | 53,968 occurrence universe、local owner/contact、known connectivity | incidence ≠ membership/maximality/global fibre |
| R242–R263，07-28 | DSU、交界、跨图连接 | 53,968 rows assigned、components/curved faces 大量重算 | Source-G global exact-key dispositions `0/224,580` |
| R264–R293，07-28–07-30 | occurrence identity/reverse rechart | expanded occurrences、lower-dimensional terminal lineages、reverse tails | nominal support ≠ explicit physical existence |
| R294–R306 + C0–C31，07-30–08-10 | Source-G/W upstream authority | C30q10 W remainder、C27R2/C29 子账本、D02 boundary | 子权威不等于 C79g canonical positive |
| C32–C54，08-10 以后 | D02 收缩 | four-chart atlas、Kraft、collision continuation、1,148 unresolved frontier | branch/candidate closure 仍不等于 formal global |
| C55–C78 | staged blocker oracles | 110,904 strict exclusions + 23,251 cemetery；C78 branch-local bridge | actual C3 dispositions `0`，global only conditional reductions |
| C79g v2–v16r2/r63a–r63bd | authority protocol and cold surface | 34/34 static、137/137 attacks、双候选/验证、76,832 rows | virtual root 未持久化；r63bd permanent zero-credit rejection |

## 6.1 历史阶段的统一读法

每一轮都要区分四件事：

```text
what was computed
≠ what was independently verified
≠ what was persisted as authority
≠ what was allowed to unlock the next tail
```

这四层混在一起，正是早期“看起来已经闭合”与严格 CM2 claim 之间的主要风险。

---

# 7. r63bd：当前证据面和唯一致命阻断

## 7.1 已完成的静态/standalone 面

- 34/34 source/schema/contract/transition/launcher gates；schema `46` defs / `242` refs / `0` unresolved。
- exact8 physical freeze 已 pin；manifest 是第九，outer 是第十且最后。
- 双 seed/no-producer、137/137 attack census、bytes/inode 独立性、terminal replay 均有 standalone evidence。
- candidate 面覆盖 `76,832` successor rows、`862` parents、`1,148` overlay rows；四类 census 为 `75,432 + 1,390 + 10 + 0`，candidate public unresolved=`0`。
- candidate/verification/completion namespace 的目录/成员权限和 `nlink` 约束已独立记录；producer 未被 consumer 打开或执行。

这些事实证明“审计和候选计算做过”，但不授予正式 global closure credit。

## 7.2 正门仍是 0/4

| 必要字段 | 实际 r63bd |
|---|---|
| `formal_global_closure_credit=1` | `0` |
| `D02_unlock=true` | `false` |
| canonical pointer persisted/replayable | `false` |
| no later-rejection | `false`，已有 r63bd rejection |

## 7.3 根因：transient virtual root，没有 writer

当前 cold launcher 的 `cold_root()` 可以在内存/held stdout 中构造带有 `formal_global_closure_credit=1`、`D02_unlock=true` 的 root，但同一对象明确写着 `root_is_virtual_and_must_not_be_persisted=true`。`run_authorize_child()` 只向 `positive_output_fd` 写 raw bytes；没有把 positive root 写入规范 canonical path，也没有独立 pointer replay。

因此：

```text
stdout transient formal=1/D02=true
  ≠ persisted canonical positive authority
```

另有 declared generic path 与 r63bd physical namespace 的投影不一致，且 `postrename_semantic_gate_or_publication_performed=false`。这个 mismatch 必须由新 successor 显式修复，不能 retag 或覆盖 generic seal。

## 7.4 r63bd rejection

```yaml
status: PERMANENT_FAIL_CLOSED_REJECTION__ZERO_CREDIT
reason: ORPHANED_OR_INCOMPLETE_C79G_V16R2_SURFACE
formal_global_closure_credit: 0
D02_unlock: false
D02_started: false
canonical_pointer_written: false
raw_file_sha256: e5ceb0c0220a72c1314558cdcf7c4b777aa368f6756a6aa197b23acc977905b8
object_sha256: d551bc395aefc5d84e7bb531abdecb52fd051941464881bf1f5fd6297485ae51
```

generic seal、前序 candidate、verification、completion 和 rejection 字节均必须保持 append-only。

---

# 8. append-only、路径和拒绝链不变式

## 8.1 不变式

- r63am→r63bd 和全部前序后继只追加，不覆盖历史字节。
- generic authority seal 不覆盖；r63bd physical namespace 与 generic declared path 分离记录。
- 目录 `0555`、成员 `0444`、`nlink=1` 等物理属性必须独立检查。
- exact8 → manifest → outer 顺序不能变；outer 之前不得发布完成语义。
- held fd、memfd seal、source/consumer exec bytes、terminal replay 使用 exact equality，不以 subset 代替。
- producer/consumer 必须 no-producer；验证器不能偷偷消费 producer 的内存结果。
- 任何失败铸造新 rejection/supersession；绝不原地 patch、retag-only、delete、reuse。

## 8.2 典型历史拒绝类别

```text
v3/v4   exact10、supersession shape、prepublication、arity/pathname
v5      CREDIT_OUTER_PRECOMMIT / malformed authority shape
v6/v7   seal/lock continuity、OOM/runtime boundary
v8/v9   launcher regression、proof-shape drift
v10     colon/prefix witness、full-root fingerprint
v11     dual-validator divergence
v12/v13 rejected prepublication / supersession shape
v14-v16 static/runtime repair without legal positive authority
v16r2   static reject、anchor-only、design-only redesign
r63ar   root fingerprint false
r63as   static-only
r63at   live_v6 exact10 pin
r63au   inherited r34 full-root fingerprint drift
r63bd   orphaned/incomplete C79g surface; permanent zero-credit rejection
```

这些拒绝不是“失败日志噪声”，而是证明系统没有把失败改写成成功的 provenance。

---

# 9. 已真正证明的内容与不可声称的内容

## 9.1 已证明/可复核（在各自作用域内）

1. 早期 bridge-note 的 conditional 边界、反例和多次路线撤回真实存在。
2. R1–R263 大量 finite-depth、face、seam、DSU、owner、transition 和 replay ledger 可独立复核。
3. Source-W formal remainder、Source-G C27R2/C29 子账本已分别封存为上游子权威。
4. r63bd static checker A/B 为零 failure；schema、contract、transition、launcher 的物理冻结顺序已 pin。
5. 双 candidate/双 verification 的字节和 inode 独立性、137/137 fail-closed、76,832-row public census、862-parent closure 和 terminal replay 有落盘 evidence。
6. append-only、held-fd、mode/nlink、fsync/rename 约束和 generic seal 不覆盖有明确字段或记录。

## 9.2 尚未证明/绝不能声称

1. 没有 persisted canonical positive authority；virtual root 不算 root。
2. 没有 formal credit=1、D02 unlock 或无 later-rejection head。
3. candidate public unresolved=0 不是 formal global unresolved=0。
4. 没有一次性完成 D02 所需的 arbitrary-depth、all-plaque、双生成器 outer atlas、全局 owner/fibre/connected-exterior 和 joint RN/selection-safe law。
5. D02-A/B/C、D03、D04、Gate5 global 18/18、fresh clean-room 都未完成。
6. “无条件 CM2”“CM2 已完成”“D02 已解锁”均没有当前证据支持。

---

# 10. 唯一 truth-changing 后续计划

当前 `r63am/r63bd` 修复范围内没有合法的“再跑一次”动作。继续必须是一个真正的新 protocol/schema successor，不是 cosmetic retag。

## 阶段 A：冻结旧链

1. 保留 r63al→r63bd 全部历史字节、candidate、verification、completion、authority seal、rejection。
2. 不覆盖 generic seal，不删除/重命名旧 namespace。
3. 在新 schema 显式声明 generic declared path ↔ round-specific physical path 的双向映射。

## 阶段 B：实现可审计的 persisted canonical-authority writer

新 writer 必须让正 root 从物理文件系统真实存在并可独立找回：

- root schema/contract 同时写入 formal credit、D02 unlock、canonical pointer、no-later-rejection 证明；
- 持有并校验目标 parent dirfd（例如 `O_PATH|O_NOFOLLOW`），固定 inode/path identity；
- stage → file fsync → atomic rename/commit → parent fsync；
- rename 后执行 semantic gate/publication，并把 `postrename_semantic_gate_or_publication_performed` 置真；
- 独立 reader 只从 canonical pointer replay，不依赖 stdout、进程内对象或 virtual root；
- crash/restart、duplicate invocation、wrong path、symlink/path traversal、partial namespace、later rejection、mode/nlink 攻击全部 fail closed；
- source component 不得在提交后继续存在；destination inode/bytes 必须与 pre-rename 预检一致；
- writer 与 producer、consumer、双 verifier 解耦，不能用 writer 代替数学/global evidence。

## 阶段 C：按硬顺序重跑

```text
34/34 static gates
  → exact8 physical freeze
  → manifest ninth
  → outer tenth and last
  → dual-seed/no-producer reconstruction
  → 137 attacks
  → bytes/inode equality
  → terminal replay
  → persisted positive wrapper replay proves all four C79g fields
  → D02-A
  → D02-B
  → D02-C
  → D03
  → D04
  → Gate5 18/18 + one complete global block
  → fresh five-gate clean-room
  → only then CM2 claim
```

任何一步失败都铸造新 rejection/supersession，不原地修补；四项 C79g 正门未同时为真时，不启动 D02 尾链。

## 明确禁止

- 把 transient `formal=1/D02=true` stdout 写成已落盘；
- 把 candidate public unresolved=0 写成 formal unresolved=0；
- 有 later rejection 时声称 positive head；
- 修改旧 seal/rejection、删除旧 namespace 或 retag-only 伪造 successor；
- C79g 未过时预跑 D02、D03、D04、Gate5 或 clean-room。

---

# 11. 给后续更强模型的交接指令

建议按以下顺序摄入，而不是从历史末尾任意抽取：

1. 先读本卷 `0–2`，建立“母问题 → CM2 双时间桥 → 证据/授权层”的类型。
2. 再读 `3–4`，明确三篇文章、bridge note 和 recursive 架构的依赖与非等价关系。
3. 再读 `5–8`，固定 acceptance semantics、r63bd 根因和 append-only 边界。
4. 再读 `9–10`，区分已证明、未证明和唯一可执行计划。
5. 最后读 `PART II` exact report；需要追溯某轮时再查 `PART IV` memory provenance 和 `PART III` source bundle。

模型在提出任何新动作前，必须先回答：

```text
它修复的是数学 primitive、证据 ledger、还是 authority persistence？
它是否改变 declared↔physical path 映射？
它是否会触碰旧字节？
它是否在 C79g 正门之前偷偷启动尾链？
失败时新对象的 rejection/supersession 如何落盘？
```

如果不能逐项回答，输出只能是设计建议，不能写成已完成事实。

---

# 12. exact source manifest 与完整性边界

## 12.1 桌面原审计报告（本卷 PART II 的 exact base）

{markdown_table([
        {"Role": "EXACT_CANONICAL_AUDIT_BASE", "File": rel(report_row["path"]), "Bytes": report_row["bytes"], "Lines": report_row["lines"], "SHA-256": report_row["sha"]}
    ], ("Role", "File", "Bytes", "Lines", "SHA-256"))}

它在本卷中只出现一次；本卷不会以编辑方式重写其内部字节。

## 12.2 前置论文与 CM2 bridge source bundle（PART III）

{article_manifest}

这些文件用于恢复“CM2 之前的文章架构和 bridge 研究原貌”。它们的历史条件结论不覆盖 r63bd。

## 12.3 theta 对照文件（不嵌入完整 3.3 MB recursive body）

{theta_manifest}

`theta_theory_recursive.md` 的关键状态摘录如下；完整文件仍在上表路径，需另行作为对照输入时可直接提供。

```text
{theta_excerpt}
```

## 12.4 Durable-memory provenance（PART IV）

本卷选择所有命中 CM2 关键术语的本地 durable-memory Markdown 文件，逐文件保留其原始字节。它们不是逐字聊天 transcript；它们是历史状态摘要和审计线索。总计 `{len(memory_rows)}` 个文件。原始 memory corpus 的其他文件不被本卷假定与 CM2 相关。

{memory_manifest}

## 12.5 deliverables 范围

当前工作区内名称命中 `cm2`/`c79g`/`C79`/`round306c` 的 deliverable 文件约 `{deliverable_count}` 个；本卷不把数千个原始工件全部复制进单一 Markdown，而在 exact report 第 9 节保留关键入口和复核命令。需要某个具体工件时，必须按路径和 digest 只读取回，不能把“文件存在”当作已经通过。

---

# 13. 建议的只读复核与 exact-body 提取

```bash
cd /home/qian-qi/.openclaw/workspaces/telegram-bot-8449317572
sha256sum /home/qian-qi/桌面/CM2_无条件攻坚全量审计报告_2026-08-26.md
sha256sum /home/qian-qi/桌面/CM2_无条件攻坚_Canonical_Latest-Wins_非递归单一总卷_through_r63bd_2026-08-26.md
sha256sum /home/qian-qi/下载/theta_theory_recursive.md
find .cm2-runtime/c79g-v16r2r63bd-* -maxdepth 1 -type f -printf '%m %n %f\\n' | sort
```

本卷的 exact body marker 包含 source path、SHA-256、bytes 和 lines。提取时按对应 `BEGIN EXACT ...` 与 `END EXACT ...` 之间的字节计算 digest；不要把 marker 本身计入 source digest。

---

# 文档结构

本卷采用与 theta canonical 总卷相同的“控制状态 → 来源清单 → 导航/规则 → 主体解释 → exact source bundle”单入口组织：

1. `PART I / 第 0–14 节`：latest-wins 控制状态、问题起源、为什么需要 CM2、三篇前置文章、CM2 bridge、递归 theta 对照、证据分层、时间线、当前阻断和唯一后续计划。
2. `PART II`：桌面原始报告的逐字 exact body，作为 CM2 审计事实底稿。
3. `PART III`：拆分计划、coverage audit、discussion summary、Paper 1/2/3 和 CM2 bridge 的逐字 exact source body。
4. `PART IV`：按文件名排序的 CM2 相关 durable-memory 原文，作为历史 provenance；其旧状态不覆盖第 0 节的 terminal truth。
5. 每个 exact source 都带路径、SHA-256、bytes、lines marker；下游模型可按 marker 独立提取和验 hash。

---

# 14. FINAL CONTROLLING INTERPRETATION

```text
CM2 origin:
  moving-singularity derivative of infinite susceptibility
  → genuine two-time past/future bridge
  → global owner/fibre/transition and authority problem

Current r63bd:
  static and standalone evidence: substantially closed
  persisted canonical positive authority: absent
  formal credit: 0
  D02: locked
  later rejection: present
  CM2 claim: forbidden

Only legal continuation:
  new persisted canonical-authority protocol/schema successor
  → static → exact8 → manifest → outer → dual replay
  → four C79g gates true and replayable
  → serial D02 tail → D03 → D04 → Gate5 → clean-room
```

> **最终控制结论：** `theta_theory_recursive.md` 可以作为更严格的内部研究架构和路线图；三篇文章和 CM2 bridge 可以作为依赖与历史来源；但截至 r63bd，没有任何一个替代物生成了 CM2 所需的 persisted canonical positive authority。无条件 CM2 仍是 `NO-GO_FOR_CLAIM`。

---

# PART II — EXACT CANONICAL DESKTOP AUDIT REPORT (r63bd)

本部分是桌面原报告的逐字 exact source。其内部第 0–10 节是该报告当时的控制摘要；在本卷语义下，必须服从本卷第 0 节和最终 terminal interpretation。

'''


def main() -> None:
    if not REPORT.exists():
        raise SystemExit(f"missing source report: {REPORT}")
    report_row = stat_row(REPORT)
    if report_row["sha"] != REPORT_SHA_EXPECTED:
        raise SystemExit(f"source report digest changed: {report_row['sha']} != {REPORT_SHA_EXPECTED}")

    article_rows = [stat_row(path) for path in article_paths() if path.exists()]
    if len(article_rows) != 7:
        raise SystemExit(f"expected 7 article/source files, found {len(article_rows)}")
    memory_rows = [stat_row(path) for path in selected_memory_paths()]
    theta_rows = [
        dict(stat_row(THETA_TOTAL), role="RELATED_THETA_TOTAL"),
        dict(stat_row(THETA_RECURSIVE), role="RELATED_THETA_RECURSIVE"),
    ]
    if theta_rows[0]["sha"] != THETA_TOTAL_SHA_EXPECTED:
        raise SystemExit("theta total digest changed")
    if theta_rows[1]["sha"] != THETA_RECURSIVE_SHA_EXPECTED:
        raise SystemExit("theta recursive digest changed")

    deliverable_count = sum(
        1
        for path in (ROOT / "deliverables").rglob("*")
        if path.is_file() and re.search(r"cm2|c79g|C79|round306c", path.name)
    )
    generated = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(timespec="seconds")
    wrapper = build_wrapper(generated, report_row, article_rows, memory_rows, theta_rows, deliverable_count)

    chunks: list[bytes] = [wrapper.encode("utf-8")]
    report_body = read(REPORT)
    chunks.extend([exact_marker(report_row, "CANONICAL_AUDIT_BASE"), report_body, end_marker(report_row, "CANONICAL_AUDIT_BASE")])

    chunks.append("\n# PART III — EXACT PREDECESSOR PAPER / CM2-BRIDGE SOURCE BUNDLE\n\n".encode("utf-8"))
    chunks.append(
        "本部分保留前置文章、拆分计划、coverage audit 和 CM2 bridge 的 exact source bytes；它们只作历史/provenance。\n\n".encode("utf-8")
    )
    for row in article_rows:
        chunks.extend([exact_marker(row, "PREDECESSOR_SOURCE"), read(row["path"]), end_marker(row, "PREDECESSOR_SOURCE")])

    chunks.append("\n# PART IV — SELECTED CM2-RELEVANT DURABLE-MEMORY ARCHIVE\n\n".encode("utf-8"))
    chunks.append(
        "以下文件按文件名排序、各嵌入一次；旧状态只作 provenance，latest-wins 控制见本卷第 0 节。\n\n".encode("utf-8")
    )
    for row in memory_rows:
        chunks.extend([exact_marker(row, "DURABLE_MEMORY_PROVENANCE"), read(row["path"]), end_marker(row, "DURABLE_MEMORY_PROVENANCE")])

    output = b"".join(chunks)
    OUT.write_bytes(output)

    # Verify exact source slices by using the same marker framing we wrote.
    checks = [(report_row, "CANONICAL_AUDIT_BASE")] + [(row, "PREDECESSOR_SOURCE") for row in article_rows] + [
        (row, "DURABLE_MEMORY_PROVENANCE") for row in memory_rows
    ]
    for row, label in checks:
        begin = exact_marker(row, label)
        end = end_marker(row, label)
        start = output.index(begin) + len(begin)
        stop = output.index(end, start)
        embedded = output[start:stop]
        if embedded != read(row["path"]):
            raise SystemExit(f"embedded source mismatch: {row['path']}")
        if digest(embedded) != row["sha"]:
            raise SystemExit(f"embedded digest mismatch: {row['path']}")

    # A machine-readable sidecar is deliberately not written: the Markdown
    # itself is the handoff artifact, and adding another authority-like file
    # would be misleading.  Print only local construction facts for the caller.
    print(json.dumps({
        "output": str(OUT),
        "bytes": len(output),
        "lines": line_count(output),
        "sha256": digest(output),
        "exact_sources": len(checks),
        "memory_sources": len(memory_rows),
        "article_sources": len(article_rows),
        "deliverable_count": deliverable_count,
        "report_sha256": report_row["sha"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
