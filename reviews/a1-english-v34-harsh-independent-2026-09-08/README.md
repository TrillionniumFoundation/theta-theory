# A1 v34 — independent harsh referee review

Reviewed manuscript: `03a4788efb3cf643bc2cd60257c5ed290bb0570d`.  
New review branch: `review/a1-english-v34-harsh-independent-2026-09-08`.

Read [REFEREE_REPORT.md](REFEREE_REPORT.md) for the full English report, theorem-level findings and primary-source comparisons.

## 本轮结论

**Major revision：当前稿件不建议按数学四大标准接收。** 这不是发现主定理错误后的拒稿结论。本轮未建立针对已审查核心证明链或新增有限检测器定理的致命反例。

v34 已落实其控制性 v33 报告允许的路线：将碰撞分类作为主贡献，将 Blackwell 后处理、有限矩递推和净化作为一般实现理论。不能在作者选择这一路线后，再把新增多 checkpoint 最优结构定理当作累加的必交条件。

主要剩余任务是将主碰撞定理与更接近的聚簇 Vandermonde 谱及超分辨率文献逐定理比较，并完成当前 v34 原生正文与 companion 的完整构建验证。报告不声称相关文献已经证明 A1，也不把明确标注的 smoke test 判为造假。35/159 页是历史 v33 页数，不是本轮独立确定的 v34 页数。

本轮实际重跑作者 v34 检查程序，普通模式与 `python -O` 输出一致，哈希与仓库记录吻合。另行编写的核心几何程序通过 298 项精确检查，其中包括 64 个完整合流混合矩配对系统、精确碰撞与近切向配置，以及碰撞树动态规划和穷举的比较。

## Reproduce

From this review directory, using Python 3.10+ and the standard library:

```sh
python audit/author_verify_revision.py > /tmp/a1-v34-author.json
python -O audit/author_verify_revision.py > /tmp/a1-v34-author-O.json
cmp /tmp/a1-v34-author.json /tmp/a1-v34-author-O.json
cmp /tmp/a1-v34-author.json audit/AUTHOR_DIAGNOSTICS_REPLAY.json
python audit/independent_core_checks.py > /tmp/a1-v34-core.json
python -O audit/independent_core_checks.py > /tmp/a1-v34-core-O.json
cmp /tmp/a1-v34-core.json /tmp/a1-v34-core-O.json
cmp /tmp/a1-v34-core.json audit/INDEPENDENT_CORE_CHECKS.json
```

The author script is identical to Git blob `9a7e45be79d15e3efa31664908346a8f1ffd5362`. Its output is identical to the manuscript's `v34/DIAGNOSTICS.json`. The independent core checks use a uniform latent prior for their exact integrals; they do not prove uniformity over a chamber or the theorem for every singular prior.

`AUDIT_MANIFEST.json` records hashes, actual executions and coverage limits. No independent full native v34 TeX build, manuscript PDF inspection, complete companion proof audit, global controller optimization, GitHub Actions pass or formal proof-assistant verification is claimed. This is an owner-requested AI-assisted referee-style assessment, not a journal commission. Only this new review directory is added; existing manuscripts and review branches are preserved.
