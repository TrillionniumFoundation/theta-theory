#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import gzip, hashlib, json, re, shutil, tarfile, tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CANONICAL = REPO / 'canonical' / 'CM2_无条件攻坚_Canonical_Latest-Wins_非递归单一总卷_through_r63bd_2026-08-26.md'
SOURCES = HERE / 'sources'
REPORTS_DIR = SOURCES / 'reports'
MASTER_NAME = 'CM2_v83_Canonical_LatestWins_AllChat_Through_v82_2026-08-28.md'
SOURCE_BUNDLE_NAME = 'CM2_v83_canonical_all_chat_source_bundle_2026-08-28.tar.gz'
RELEASE_PACKAGE_NAME = 'CM2_v83_canonical_all_chat_release_package_2026-08-28.tar.gz'

REPORT_ORDER = [
'CM2_v52_full_derivation_report_2026-08-26.md',
'CM2_v55_full_remaining_blocker_assault_report_2026-08-26.md',
'CM2_v63_full_terminal_reconciliation_report_2026-08-26.md',
'CM2_v64_full_remaining_blocker_assault_report_2026-08-26.md',
'CM2_v65_full_remaining_blocker_assault_report_2026-08-27.md',
'CM2_v67_similarity_scoped_reconstruction_report_2026-08-27.md',
'CM2_v68_nonzero_moving_singularity_report_2026-08-27.md',
'CM2_v69_open_multiseam_report_2026-08-27.md',
'CM2_v70_specular_universality_frontier_report_2026-08-27.md',
'CM2_v70_specular_graph_flow_assault_report_2026-08-27.md',
'CM2_v71_rectangular_maximality_report_2026-08-27.md',
'CM2_v75V2_radial_graph_flow_report_2026-08-27.md',
'CM2_v76_exact_gate_magnet_collar_report_2026-08-28.md',
'CM2_v77_bilateral_tangent_family_report_2026-08-28.md',
'CM2_v78_tangent_bunching_balanced_band_report_2026-08-28.md',
'CM2_v79_unnormalized_reversible_closure_report_2026-08-28.md',
'CM2_v80_universal_maximality_report_2026-08-28.md',
'CM2_v81_universal_irreducibility_report_2026-08-28.md',
'CM2_v81_bilateral_rate_gap_report_2026-08-28.md',
'CM2_v81_universal_rate_gap_report_2026-08-28.md',
'CM2_v82_terminal_universal_classification_report_2026-08-28.md',
]
STAGES = [
('r63bd baseline','Initial canonical dossier','NO-GO; formal authority absent; D02 locked',CANONICAL.name),
('v52','Formal-closure successor','Internal limit-exchange, pair-energy, Kac/Wiener repairs; actual packets still absent',REPORT_ORDER[0]),
('v55','Evidence-complete closure','Verifier and persistence protocols hardened; actual runtime/D02/proof packets absent',REPORT_ORDER[1]),
('v63','Rooted non-minting and directed Frostman','External root trust and future-coded Frostman repaired; no actual credit',REPORT_ORDER[2]),
('v64','Scoped authority chain and stopping antichain','Seven-stage credit lattice and all-depth packing repaired',REPORT_ORDER[3]),
('v65','Self-contained release and E2E authority','Release isolation, reviewer roots, D02 terminal semantics and U3 field separation repaired',REPORT_ORDER[4]),
('v67','Similarity-scoped reconstruction','Actual but zero-source scoped CM2; does not solve nonzero source',REPORT_ORDER[5]),
('post-v67','Scope evaluation','Scoped unconditional zero-source PASS; nonzero source and full-flow still open','CHAT_ONLY_v67_scope_evaluation.md'),
('v68','Nonzero pinball model','First explicit scoped nonzero moving-seam product-CM2',REPORT_ORDER[6]),
('v69','Open multi-seam class','Uniform open-parameter nonzero source and finite-DQ l1 convergence',REPORT_ORDER[7]),
('v70-A','Specular universality frontier','Unrestricted arbitrary motion and all-seed recovery refuted; new graph/flow compilers',REPORT_ORDER[8]),
('v70-B','Specular graph-flow assault','Full first-order shape/roof calculus and exact no-go boundaries',REPORT_ORDER[9]),
('v71','Rectangular maximality','Diagonal cancellation shortcut refuted; signed-schedule compiler introduced',REPORT_ORDER[10]),
('v72 V3','Tangent cocycle/rate-gap','Abstract bilateral tangent compilers closed; actual TG2-TG8 remained open','CHAT_ONLY_v72_reconstruction.md'),
('v75 V2','Gate/Frostman/Roof-Fubini frontier','False face-to-gate promotion rejected; actual RN/minorization first blocker',REPORT_ORDER[11]),
('v76','Exact gate/magnet/collar','Local exact gate closed; direct parent floor and orientation-free collar refuted',REPORT_ORDER[12]),
('v77','Bilateral tangent family','Reversible finite-DQ transposition and root-ratio tangent split; global disintegration still open',REPORT_ORDER[13]),
('v78','Tangent bunching/balanced band','Root-ratio and Holder-density shortcuts rejected; H/T/G route compiler',REPORT_ORDER[14]),
('v79','Unnormalized reversible candidate closure','Claimed scoped TG2-TG8 closure, later withdrawn by v80 audit',REPORT_ORDER[15]),
('v80','Universal maximality audit','Unrestricted universal theorem refuted; v79 actual promotion withdrawn; UMS packet introduced',REPORT_ORDER[16]),
('v81-A','Universal irreducibility','UMS fields tested by countermodels',REPORT_ORDER[17]),
('v81-B','Bilateral rate gap','Sharp moving-spike/rate-gap and bilateral-domain compilers',REPORT_ORDER[18]),
('v81-C','Universal rate-gap packet v2','Merged packetized universal route',REPORT_ORDER[19]),
('v82','Terminal universal classification','Unrestricted theorem false; UMS-v3 compiler and fieldwise irreducibility complete; actual packets required',REPORT_ORDER[20]),
]

def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def line_count(data: bytes) -> int:
    return data.count(b'\n') + (0 if not data or data.endswith(b'\n') else 1)

def extract_reports() -> dict[str, bytes]:
    found: dict[str, bytes] = {}
    for name in REPORT_ORDER:
        path = REPORTS_DIR / name
        if not path.exists():
            raise RuntimeError(f'missing report: {path}')
        found[name] = path.read_bytes()
    extras = {p.name for p in REPORTS_DIR.glob('*.md')} - set(REPORT_ORDER)
    if extras:
        raise RuntimeError(f'unregistered reports: {sorted(extras)}')
    return found

def extract_chat_notes() -> dict[str, bytes]:
    data = (SOURCES / 'chat_only_notes.md').read_bytes()
    pattern = re.compile(
        br'<!-- BEGIN RECONSTRUCTED CHAT NOTE: ([^>]+) -->\n(.*?)<!-- END RECONSTRUCTED CHAT NOTE: \1 -->\n',
        re.S,
    )
    return {m.group(1).decode('utf-8'): m.group(2) for m in pattern.finditer(data)}

def tar_deterministic(out: Path, entries: list[tuple[Path, str]]) -> None:
    with out.open('wb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0, compresslevel=9) as gz:
            with tarfile.open(fileobj=gz, mode='w', format=tarfile.PAX_FORMAT) as tf:
                for src, arc in sorted(entries, key=lambda x: x[1]):
                    info = tf.gettarinfo(str(src), arcname=arc)
                    info.uid = info.gid = 0
                    info.uname = info.gname = ''
                    info.mtime = 0
                    info.mode = 0o644 if info.isfile() else 0o755
                    if info.isfile():
                        with src.open('rb') as f:
                            tf.addfile(info, f)
                    else:
                        tf.addfile(info)

def build_master(reports: dict[str, bytes], notes: dict[str, bytes]) -> Path:
    canonical = CANONICAL.read_bytes()
    parts: list[bytes] = []
    def add(x: str | bytes) -> None:
        parts.append(x.encode('utf-8') if isinstance(x, str) else x)
    add(f'''---
title: "CM2 v83：最初 Canonical MD、后续全部实质聊天与 v82 终端分类的 Latest-Wins 单一总卷"
version: "v83-editorial-canonical-all-chat-through-v82"
generated_local: "2026-08-28"
language: "zh-CN"
source_initial_canonical: "{CANONICAL.name}"
source_initial_canonical_bytes: {len(canonical)}
source_initial_canonical_sha256: "{sha_bytes(canonical)}"
latest_substantive_version: "v82-terminal-universal-classification"
merge_policy: "latest-wins; fail-closed; preserve provenance; exact source embeddings; repeated continuation directives and progress-only chatter consolidated; no new authority or mathematical theorem synthesized by this editorial merge"
github_target: "TrillionniumFoundation/theta-theory"
---

# CM2 v83：Canonical Latest-Wins All-Chat 总卷

## 0. 本版性质

本文件整理：

1. 最初的 CM2 canonical Markdown 全文；
2. r63bd 之后聊天中形成的全部可取得实质报告；
3. 没有独立附件的两个重要聊天阶段，以明确标注的重建摘要保存；
4. v52--v82 的状态、测试、manifest 与包裹索引；
5. v82 latest-wins 终端分类。

本文件不是逐字聊天 transcript。重复的“按最新 plan 全量冲”指令、过程播报和上传通知被归并；其产生的数学、反例、状态变化与工件由下方 exact report bodies 和版本索引承载。`RECONSTRUCTED_FROM_CHAT_FINAL` 条目不是原附件字节，不得当作 exact source。

本版是 **editorial consolidation**：不制造新的数学定理、formal credit、GitHub authority、D02 credit 或外部同行评审事实。

## 1. Latest-wins 控制状态（through v82）

```yaml
UnrestrictedUniversalMovingScattererCM2:
  status: REFUTED_EXACTLY

LocalGeometryOnlyUniformCM2:
  status: REFUTED_BY_ACTUAL_BILLIARD_SPECTRAL_OBSTRUCTION

BilateralDomainReversalCompiler:
  status: PROVED

MesoscopicFiniteDQ_L1_Compiler:
  status: PROVED_SHARP

UMS_v3_PacketizedUniversalCompiler:
  status: PROVED

UMS_v3_FieldwiseIrreducibility:
  status: PROVED_UP_TO_EQUIVALENT_REPLACEMENT

ActualUniformAdmissibleClasswideCM2:
  status: ACTUAL_LOCAL_PACKETS_REQUIRED

V79ActualTG3_TG8Pass:
  status: WITHDRAWN_LATEST_WINS

OriginalR63bdFormalCredit:
  value: 0

ExternalPeerReview:
  status: NOT_PERFORMED
```

### 1.1 最强诚实结论

- 字面 unrestricted arbitrary-motion universal positive theorem 已被有限/无限视界穿越反例关闭。
- 仅靠局部曲率、飞行长度和光滑性不能生成 class-wide uniform spectral rate。
- 最大可真的 universal statement 是：任何实际提交统一 UMS-v3 packet（或逐字段等价 replacement）的 compact admissible class，都可由已证明 compiler 得到 rectangular CM2、finite-DQ `l1(N^2)` 收敛，以及其声明的 physical-time response。
- 尚未提供某一整个 admissible class 的 UMS-v3 actual local packets，因此 actual class-wide positive PASS 不能由本编辑合并产生。

## 2. Supersession 规则

```text
v82 terminal classification
> v81 rate-gap / irreducibility branches
> v80 universal maximality and v79 withdrawal
> v79 candidate actual closure
> v78 and earlier frontier reports
> initial r63bd canonical truth for its historical checkpoint
```

历史 `PASS/CLOSED` 必须按其原作用域读取。特别是 v79 的 scoped actual promotion 已由 v80 hostile audit 撤回；v82 控制 universal 终态。

## 3. 后续聊天实质阶段索引

| Stage | 主题 | Latest-wins 结果 | Source |
|---|---|---|---|
''')
    for stage, theme, result, source in STAGES:
        add(f'| `{stage}` | {theme} | {result} | `{source}` |\n')
    add('''
## 4. User-directive consolidation

后续聊天的用户指令主要属于以下递进目标：

```text
审阅原 MD 并规划
→ 全量冲内部 blocker
→ 自建 D02 / proof packets
→ 从 zero-source 转向 nonzero moving singularity
→ 从 controlled pinball 转向 specular dispersing Sinai
→ rectangular collision-map CM2
→ full physical-time response
→ independently moving scatterer
→ unrestricted universal theorem
→ terminal universal classification
```

重复 continuation 指令不逐字堆叠；每次产生的实质结果均映射到上表 source。这样保留全部研究内容，同时避免递归复制聊天噪声。

## 5. Package 与可重放边界

本发布包含 canonical master、原始 canonical MD 的 exact copy、v52--v82 reports、chat-only notes、status 与 SHA manifests。旧历史二进制包不递归嵌套；报告与当前 package 足以重建本阅读入口。

---

# PART II — POST-r63bd EXACT REPORT BODIES

以下报告按版本/路线顺序原字节嵌入。其内部状态服从本卷第 1--2 节的 latest-wins 规则。

''')
    for name in REPORT_ORDER:
        body = reports[name]
        add(f'\n<!-- BEGIN EXACT REPORT: {name}; SHA256={sha_bytes(body)}; BYTES={len(body)}; LINES={line_count(body)} -->\n')
        add(body)
        if not body.endswith(b'\n'):
            add('\n')
        add(f'<!-- END EXACT REPORT: {name} -->\n')
    add('''
---

# PART III — CHAT-ONLY RECONSTRUCTED STAGES

这些条目没有独立附件字节；只作为聊天内容导航，明确不冒充 exact source。

''')
    for name in ['CHAT_ONLY_v67_scope_evaluation.md', 'CHAT_ONLY_v72_reconstruction.md']:
        body = notes[name]
        add(f'\n<!-- BEGIN RECONSTRUCTED CHAT NOTE: {name}; SHA256={sha_bytes(body)} -->\n')
        add(body)
        if not body.endswith(b'\n'):
            add('\n')
        add(f'<!-- END RECONSTRUCTED CHAT NOTE: {name} -->\n')
    add(f'''
---

# PART IV — EXACT INITIAL CANONICAL MD

下面逐字嵌入最初 canonical 文件。其 r63bd 状态是历史 checkpoint；后续 interpretation 服从本卷开头的 v82 latest-wins supplement。

<!-- BEGIN EXACT INITIAL CANONICAL: {CANONICAL.name}; SHA256={sha_bytes(canonical)}; BYTES={len(canonical)}; LINES={line_count(canonical)} -->
''')
    add(canonical)
    if not canonical.endswith(b'\n'):
        add('\n')
    add(f'<!-- END EXACT INITIAL CANONICAL: {CANONICAL.name} -->\n')
    out = HERE / MASTER_NAME
    out.write_bytes(b''.join(parts))
    return out

def main() -> None:
    if not CANONICAL.exists():
        raise SystemExit(f'missing canonical source: {CANONICAL}')
    reports = extract_reports()
    notes = extract_chat_notes()
    master = build_master(reports, notes)
    status = HERE / 'CM2_v83_latest_status.json'
    if not status.exists():
        shutil.copy2(SOURCES / 'CM2_v83_latest_status.json', status)

    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        source_root = td / 'source'
        source_root.mkdir()
        shutil.copy2(CANONICAL, source_root / CANONICAL.name)
        for name, body in reports.items():
            (source_root / name).write_bytes(body)
        for name, body in notes.items():
            (source_root / name).write_bytes(body)
        shutil.copy2(SOURCES / 'README.md', source_root / 'README.md')
        shutil.copy2(SOURCES / 'CM2_v83_latest_status.json', source_root / 'CM2_v83_latest_status.json')
        source_bundle = HERE / SOURCE_BUNDLE_NAME
        tar_deterministic(source_bundle, [(p, p.name) for p in source_root.iterdir() if p.is_file()])

    catalog = {
        'generated': '2026-08-28',
        'scope': 'cm2/canonical/v83',
        'artifacts': [],
    }
    for p in sorted([master, status, HERE / SOURCE_BUNDLE_NAME] + list(SOURCES.glob('*'))):
        if p.is_file():
            catalog['artifacts'].append({'path': str(p.relative_to(HERE)), 'bytes': p.stat().st_size, 'sha256': sha_file(p)})
    catalog_path = HERE / 'artifact_catalog.json'
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    sums_paths = [master, HERE / SOURCE_BUNDLE_NAME, status, catalog_path, SOURCES / 'README.md']
    sums = HERE / 'SHA256SUMS.txt'
    sums.write_text('\n'.join(f'{sha_file(p)}  {p.name}' for p in sums_paths) + '\n', encoding='utf-8')

    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        release_files = [master, HERE / SOURCE_BUNDLE_NAME, status, catalog_path, sums, SOURCES / 'README.md']
        release_package = HERE / RELEASE_PACKAGE_NAME
        tar_deterministic(release_package, [(p, p.name) for p in release_files])

    manifest_paths = [master, HERE / SOURCE_BUNDLE_NAME, HERE / RELEASE_PACKAGE_NAME, status, catalog_path, sums]
    manifest = HERE / 'CM2_v83_publication_manifest.sha256'
    manifest.write_text('\n'.join(f'{sha_file(p)}  {p.name}' for p in manifest_paths) + '\n', encoding='utf-8')

    # Exact embedding self-check.
    data = master.read_bytes()
    if sha_bytes(CANONICAL.read_bytes()) not in data.decode('utf-8', errors='ignore'):
        raise RuntimeError('canonical SHA missing from master')
    print(json.dumps({
        'master': {'bytes': master.stat().st_size, 'sha256': sha_file(master)},
        'source_bundle': {'bytes': (HERE / SOURCE_BUNDLE_NAME).stat().st_size, 'sha256': sha_file(HERE / SOURCE_BUNDLE_NAME)},
        'release_package': {'bytes': (HERE / RELEASE_PACKAGE_NAME).stat().st_size, 'sha256': sha_file(HERE / RELEASE_PACKAGE_NAME)},
        'reports': len(reports),
        'chat_notes': len(notes),
    }, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
