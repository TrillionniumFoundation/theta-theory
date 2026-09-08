# A1 v35 — independent referee assessment

Reviewed manuscript: `02a19f2ddb83cf68bfbf8361c137613e2ffd3925`.  
Review branch: `review/a1-english-v35-harsh-independent-2026-09-08`.

Read [REFEREE_REPORT.md](REFEREE_REPORT.md) for the full assessment, theorem-level audit, source ledger and bounded requests.

**Recommendation: minor revision, with a favorable publication assessment for the main article.** This is an owner-requested, AI-assisted referee-style report, not a decision or commission from a journal.

## 本轮结论

本轮不再延续已解决的主要拒稿理由。v35 对完整谱文献、超分辨率 minimax 文献及当前原生构建作出了实质回应。新增外幂谱乘积命题的重复节点、最小采样长度和固定带宽边界经具体审计，未发现致命错误。主贡献仍是原有的可达碰撞分类，不是新加的比较命题或检查次数。

报告建议有利于发表的小修，仅要求在“同一未来谱”例子中固定共同归一化 H，并局部重申 crossover 是比较量级而非最优控制器的精确转变阈值。不要求另加多 checkpoint 最优控制定理，也不把历史 companion 的全部结论一并认证。

当前构建回执列出的 80 个 TeX 源对象已与稿件提交核对一致。审稿人没有独立重新编译原生全文或视觉检查稿件 PDF；回执检查、源对象核验和数学证明审查是不同证据。

## Reproduce the executed diagnostics

Use Python 3.10+ with `sympy` and `mpmath`. The inherited finite-cell and core programs use the standard library. From this directory:

```sh
python audit/inherited_finite_cell_checks.py > /tmp/a1-v35-cell.json
python -O audit/inherited_finite_cell_checks.py > /tmp/a1-v35-cell-O.json
cmp /tmp/a1-v35-cell.json /tmp/a1-v35-cell-O.json
cmp /tmp/a1-v35-cell.json audit/FINITE_CELL_REPLAY.json
python audit/inherited_core_checks.py > /tmp/a1-v35-core.json
python -O audit/inherited_core_checks.py > /tmp/a1-v35-core-O.json
cmp /tmp/a1-v35-core.json /tmp/a1-v35-core-O.json
cmp /tmp/a1-v35-core.json audit/CORE_REPLAY.json
python audit/author_spectral_checks.py > /tmp/a1-v35-author.json
python -O audit/author_spectral_checks.py > /tmp/a1-v35-author-O.json
cmp /tmp/a1-v35-author.json /tmp/a1-v35-author-O.json
cmp /tmp/a1-v35-author.json audit/AUTHOR_SPECTRAL_REPLAY.json
python audit/independent_v35_checks.py > /tmp/a1-v35-independent.json
python -O audit/independent_v35_checks.py > /tmp/a1-v35-independent-O.json
cmp /tmp/a1-v35-independent.json /tmp/a1-v35-independent-O.json
cmp /tmp/a1-v35-independent.json audit/INDEPENDENT_V35_CHECKS.json
```

The first three scripts are byte-identical copies of published source blobs; their historical metadata remains unchanged. The fourth was written for this assessment. The inherited core's 298 checks, the author's new comparison diagnostics, and this referee's 200 boundary checks have distinct coverage and are not combined into a claim of proof verification. Floating-point SVD outputs may vary with dependency versions; recorded outputs are tied to the versions in `AUDIT_MANIFEST.json`.

`audit/SOURCE_IDENTITY_CHECK.json` records the unchanged-tree check against the current build receipt. `audit/REPLAY_EXECUTIONS.json` records actual program executions. `AUDIT_MANIFEST.json` binds the supplied report, scripts and outputs by content hashes and states the verification limits.

No full companion re-audit, formal proof assistant, GitHub Actions pass, exhaustive controller optimizer, or independent native PDF build is claimed. The review branch adds only this new directory; it does not alter manuscripts or existing branches.
