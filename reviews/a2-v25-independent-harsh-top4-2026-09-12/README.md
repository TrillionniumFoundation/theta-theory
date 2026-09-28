# A2 v25：独立严格审稿材料

本目录对应 `revision/a2-v25-observable-calibration-signature-top4-2026-09-12` 的固定提交：

`3143762fc98373f93dbb8884c5ece005229ca50b`

审稿分支：`review/a2-v25-independent-harsh-top4-2026-09-12`。

## 结论

**以 Annals / Inventiones / JAMS / Acta 为目标：当前版本建议拒稿，实质性重构后重新评估。**

这不是期刊正式决定，而是作者要求的 AI 辅助独立 referee-style review。报告不把前轮已修复的问题继续列为缺陷，也不声称发现了推翻 v25 新全局一致性定理的反例。

v25 对公共观测与校准、包含 gap 的统计判别、有限 signature 的局部唯一匹配、兼容解析变分模型、pilot 与最终 flight number 的选择顺序，以及反向 Poisson 核的 bulk 条件，均有实质性修复。

剩余核心问题是：新全局实验保留精确二维端点位置，因此已直接提供未知边界上的几何样本。报告给出同样只用长偶数桥、同样计入失败准备成本的局部图函数插值路线。该路线能够绕开半无限作用量反演来取得有限 contact jets。因此，仅强调最小 flight number 趋于无穷，仍不足以说明新全局 flagship 相对于这种直接采样路线的数学增量。这是原创性与核心定理定位问题，而不是一致性定理的反例。

另一个确定的错误是：文中将“不对基准分布绝对连续”称为“整个统计族非支配”。显式标量密度族受 Lebesgue 测度加原子支配；有限条带 Poisson 族也有公共 Poisson 包络支配律。报告给出具体公式，并说明修正不必推翻已有 collar 和核比较证明。

完整 native build 在审查时仍未核验成功；排队中的工作流不构成编译通过，也不能被说成 LaTeX 失败。

## 文件

- `REFEREE_REPORT.md`：完整英文审稿报告，含前轮问题闭合表、直接几何采样基准、统计支配性纠正及下一轮要求。
- `ISSUE_LEDGER.json`：区分已修复问题、重大科学定位问题、确定表述错误和构建核验门槛。
- `SOURCE_AUDIT.md`：固定源、实际阅读范围、未完成的核验及执行记录。
- `independent_checks.py`：独立有限诊断脚本，不导入作者代码。
- `INDEPENDENT_CHECKS.json`：实际执行的 126 个检验结果。

## 复现独立诊断

从本目录运行：

```sh
python independent_checks.py > checks-normal.json
python -O independent_checks.py > checks-optimized.json
cmp checks-normal.json checks-optimized.json
```

本轮已在 Python 3.13.5 执行，普通与优化模式输出逐字节一致。脚本不用 `assert`。这些有限检验不是完整证明认证、全仓库审计或 native 编译结果。

本目录仅新增审稿材料；不修改或删除论文，不合并至主分支。
