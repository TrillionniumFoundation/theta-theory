# CM2 v65 全量剩余 blocker 攻坚报告

## 结论

本轮没有继承 v64 的“发布层已经闭合”判断，而是从干净解包环境重新执行。结果发现 v64 工件包遗漏五个测试依赖 schema：干净解包运行得到 **35 failed / 106 passed**。补回缺失 schema 后，历史回归恢复为 **141/141 PASS**。在此基础上新增 60 个 v65 hostile tests，最终自包含发布包为 **201/201 PASS**。

这只关闭 reference protocol、分发完整性和内部类型 blocker。它不改变 r63bd controlling truth：`formal_global_closure_credit=0`、`D02_unlock=false`、`CM2=NO-GO_FOR_CLAIM`。

## 新闭合的 blocker

### 1. 发布包不自包含

修复为 exact file anti-join、SHA/bytes/mode/nlink、AST local-import/HERE-relative dependency scan、Python/外部包版本锁、fresh temporary extraction、isolated pytest、运行前后字节一致。

### 2. authority 只验证 summary，不验证 raw chain

新 verifier 从同一 held root 直接读取 bootstrap、policy、threshold-signed trusted time、challenge、hermetic execution、transparency、canonical root、decision 和 journal。七阶段的 time/challenge/decision sequence 连续，nonce 唯一，transparency head 严格逐阶段延伸，leaf 必须处于新追加右子树。

### 3. terminal reviewer 自引入与本地铸 credit

新 terminal observer 使用外部固定 reviewer store；签名绑定 store digest、packet id、scope、proof/audit digests，并执行 threshold、有效期和 revocation。所有本地输出的 granted credit 固定为 0。

### 4. D02 关键字段只是字符串，terminal 后还能继续

新 actual-bundle observer 使用 held-dirfd strict I/O 和 typed evidence index。D02-A/B/C 的 owner/history/root-order/incidence/margin 等字段必须引用实际 proof object digest。D02-B terminal marker 后的任意同行续写立即拒绝。

### 5. U3 八字段可复用同一工件

八字段现在绑定八个不同 artifact name/digest；每个对象声明准确 field id、actual/no-producer、proof、independent verifier、attack ledger、terminal replay。H1-H5 的 union 必须覆盖全部八字段。

### 6. JSON/path/整数边界不统一

统一拒绝 duplicate key、NaN/Infinity、float、non-NFC、surrogate、控制字符、Boolean-as-integer、symlink ancestor、mount crossing、hard link、mode drift、read-time mutation。authority、terminal 与 actual bundle 在消费语义前还执行 held-root recursive exact-tree anti-join，任何未声明文件/目录都拒绝。

## 机械结果

- 历史 v64 regression：141/141 PASS
- v65 end-to-end authority：11/11 PASS
- v65 terminal readiness：11/11 PASS
- v65 actual bundle：11/11 PASS
- v65 strict I/O：10/10 PASS
- v65 self-contained release：13/13 PASS
- 总计：201/201 PASS
- TeX：15,344 lines / 713,181 bytes
- PDF：183 pages
- labels：811 unique / 0 duplicate
- refs：1,296 / 0 undefined
- citations：0 missing
- LaTeX warnings / overfull / underfull：0 / 0 / 0

## 仍未提供的 truth-changing 对象

1. real immutable r63bd deliverables/runtime namespaces；
2. externally authorized production C79g successor and canonical writer transaction；
3. production D02-A/B/C, D03, D04, Gate5 and clean-room bytes；
4. actual moving-singularity/U3 mathematical proof packets；
5. externally precommitted reviewer/authority roots and fresh signed events。

因此，本轮最强诚实状态是：截至 v65 hostile audit，当前材料能合法修复的内部 blocker 已闭合；实际和外部对象未提供，不能宣称无条件 CM2。
