# A1 v33 — second independent review

Controlling manuscript: `e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c`.
Review branch: `review/a1-english-v33-harsh-second-independent-2026-09-08`.

Read [REFEREE_REPORT.md](REFEREE_REPORT.md) for the full assessment and source ledger.
The recommendation is rejection at the requested four-journal level, based on the significance analysis, **not** on an established fatal counterexample to the new named v33 theorems.
This is an owner-requested AI-assisted referee-style report, not a journal commission.

## 本轮结论

v33 确有实质修复：共同失败报告的可实现域、精确矩控制器公式、平均风险净化、多面体标量化规则及原模型连续控制证书均经过具体审计。报告不再重复“原模型缺失”“证书未执行”“没有本轮完整构建记录”等已解决问题。

主要保留意见是：新增控制器层与碰撞几何的联系仍主要通过通用有限检测器递推、有限积分净化、紧致性以及已有风险界的代入实现；原模型多时刻最优控制结构尚未由这些表示定理得到刻画。这是顶刊贡献判断，不是把有效定理判成错误。

## Reproduce the executed checks

From this review directory, using Python 3.10+ and the standard library only:

```sh
python audit/author_certify_instance.py > /tmp/v33-author.json
python -O audit/author_certify_instance.py > /tmp/v33-author-O.json
cmp /tmp/v33-author.json /tmp/v33-author-O.json
cmp /tmp/v33-author.json audit/AUTHOR_CERTIFICATE_REPLAY.json
python audit/independent_checks.py > /tmp/v33-independent.json
python -O audit/independent_checks.py > /tmp/v33-independent-O.json
cmp /tmp/v33-independent.json /tmp/v33-independent-O.json
cmp /tmp/v33-independent.json audit/INDEPENDENT_CHECKS.json
```

The author script is a byte-identical copy of reviewed Git blob `36d5f623f4452d55ed79e606d095a7db8a865d91`; its output hash matches the manuscript's session receipt. The independent script performs 101 checks: a three-stage exact occupancy/risk comparison, 64 deterministic one-step rules against 81 support functionals, and a separately derived continuum certificate calculation.

The three-stage check uses an atomic prescribed command law admitted by the general moment theorem. It is not an atomless purification test or a global controller optimizer. The high-precision logarithmic calculation is a diagnostic, not a directed interval proof.

`AUDIT_MANIFEST.json` records exact hashes and verification limits. The referee inspected the author's current full-volume build records but did not independently compile or visually inspect the complete 35-page main and 159-page companion. No formal proof-assistant or GitHub Actions pass is claimed. Existing manuscript and review branches are preserved.
