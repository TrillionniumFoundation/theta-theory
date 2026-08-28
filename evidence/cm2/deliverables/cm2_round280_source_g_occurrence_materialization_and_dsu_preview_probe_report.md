# CM2 Round280：atom-graph occurrence 语义与 DSU 预演（严格 ZERO CREDIT）

## 结论

Round280 已对 Round279 的 canonical atom / common-face edge 冻结包完成全量
schema、provenance、exact-key、existing-occurrence binding 与 DSU 预演审计。

最重要的语义结论是：

> `295,976` 个没有 Round208 occurrence anchor 的 canonical atoms **不能逐个自动提升**
> 为 expanded occurrences。必须先按 `330,724` 条已认证正面积 patch edges 对
> `332,016` 个 atoms 取 connected graph quotient，再讨论 occurrence identity。

因此本轮没有生成任何正式新 occurrence ID，也没有发放 component union、
maximality、fibre 或 disposition credit。

## 冻结输入

Round266：

- certificate SHA256：
  `2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf`
- independent verification SHA256：
  `a6436c716cbbe74f0195e2d87f4084a28ca2a2e27b9fe5eeb98b6835df92b75b`
- frozen frontier：`63,224` components、`126,468` occurrences、`116` exact keys

Round279：

- result SHA256：
  `628b07e56a6aa7ecdbdfde95f184a3a3c0ad1eb5a5addb84588e960a87af1677`
- certificate SHA256：
  `ef60a40cc05d47b3d899b73169017bee8e246583ce51a5b543f1b1a1047f064e`
- atom ledger SHA256：
  `283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe`
- edge ledger SHA256：
  `bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695`
- verifier SHA256：
  `93665f5968b17844a34587df9080f240e40e65cd62e54a4445e2714e20455635`
- independent verification SHA256：
  `a4cd7a96a43a9011e223d230c9f604f567fa56f1b095403cf802261daab5de21`
- full dynamic verification：`330,724 / 330,724` edges PASS，`19 / 19`
  semantic attacks rejected

本轮没有读取或应用 Round268 的 `152` 个 true-seam patches，也没有使用任何
`Jx/Jy` same-point relation。

## atom provenance 与既有 occurrence 绑定

`332,016` 个 canonical atoms 全部逐项保留：

- `origin_row_id`
- `Round182_occurrence_row_id`
- `Round182_leaf_row_id`
- source signature row IDs
- complete 10-field signature SHA256
- official exact-key ID / ordinal
- frozen exact true-support box

全部 true-support boxes 都是严格正体积、位于其 frozen Round182 leaf 内；其中
`332,012` 个为 whole-leaf support，`4` 个为 Round271 W-tail 的严格 frozen
subbox support。

`36,040 / 36,040` 个 Round208-backed atoms 均唯一命中 Round266 occurrence
frontier，并逐项通过：

- occurrence source 为 `ROUND208_REGION`
- source geometry row ID 等于 Round208 region ID
- exact box SHA256 一致
- complete signature SHA256 一致
- source chart、official key ID / ordinal 一致
- Round266 component exact-key purity一致

剩余 `295,976` 个 rows 只保留为 unbound atom candidates；其
`new_expanded_occurrence_id` 明确为 `null`。

## complete atom graph quotient

对 `332,016` atoms 加入 Round279 的全部 `330,724` 条 local common-face edges：

- distinct atom endpoint pairs：`330,724`
- graph rank reductions：`239,896`
- graph-redundant edges：`90,828`
- connected atom-graph classes：`92,120`
- exact-key purity：全部 PASS
- collar atom universe 覆盖 `108` 个 exact keys；Round266 的另外 `8` 个 keys
  在 anchor frontier 中原样守恒，总计仍为 `116`

`92,120` 个 classes 的 anchor census：

- 有至少一个既有 Round208 occurrence anchor：`16,532`
- 完全无既有 occurrence anchor：`75,588`
- 单一既有 occurrence anchor：`7,396`
- 多个既有 occurrence IDs：`9,136`
- 跨多个 Round266 components：`4,512`
- 单 class 最大 atom 数：`64`
- 单 class 最大 occurrence anchor 数：`64`
- 单 class 最大 Round266 component 数：`4`

atom census：

- anchored atoms：`199,272`
- unanchored atoms：`132,744`

`75,588` 个 unanchored classes 的大小分布：

- `21,160` 个 singleton atom classes
- `54,428` 个 nontrivial connected classes
- size 2：`53,308`
- size 3：`420`
- size 4：`356`
- size 5：`56`
- size 6：`148`
- size 7：`80`
- size 8：`28`
- size 9：`4`
- size 10：`20`
- size 12：`8`

它们只能称作“provisional new-occurrence candidate classes”，不能称作已经新增的
`75,588` 个 expanded occurrences；后者仍需最终 seam quotient 与 occurrence
identity contract。

## anchor-only DSU preview

仅使用 anchored atom classes 给出的 component-union relations，从 Round266 的
`63,224` 个 components 出发：

- requested anchor relations：`5,568`
- 独立 preview rank reductions：`2,072`
- local-glue anchor groups：`61,152`
- unanchored atom classes：`75,588`
- 不含 Round268 seams 的 provisional component count：
  `61,152 + 75,588 = 136,740`

这里的 `2,072` 和 `136,740` 都是 **ZERO-CREDIT preview arithmetic**：

- `2,072` 不能写入正式 DSU rank ledger；
- `136,740` 不是最终 quotient；
- `75,588` 不是正式 expanded-occurrence count；
- Round268 的 `152` 个 true-seam patches 仍可能 attach/merge classes；
- multiple-anchor classes 证明正维 connectivity，但并不自动证明多个既有
  occurrence IDs 应被折叠成同一个 occurrence identity。

## 正式提升的最小充分条件

进入正式 occurrence/component promotion 前至少还必须：

1. 把 expanded occurrence 明确定义为 certified positive-open support graph 的
   connected component，而不是“一 atom 一 occurrence”。
2. 在 final occurrence identity 赋值前，把 Round275 reverse-rechart 结果与
   Round268 的 `152` 个 true-seam channels 纳入 complete admissible adjacency
   universe。
3. 重新证明 seam quotient 后每个 unanchored class 仍非空、正开且 exact-key
   pure。
4. 对 multiple-anchor classes 给出明确 contract：既有 occurrence IDs 是一个
   occurrence 的历史碎片，还是仅 component-connected 的不同 occurrences。
5. 完成 Round267 lower-stratum physical disposition；nominal provenance 不得自动
   获得 occurrence/component credit。

## 严格非提升

- formal new expanded occurrences：`0`
- formal component union credit：`0`
- formal DSU rank reduction credit：`0`
- maximality：`0 / 63,224`
- fibres：`0 / 116`
- dispositions：`0 / 224,580`
- Jx/Jy same-point glue：`0`
- Gate5：`10 / 18`
- D02：`BLOCKED`
- CM2：`NO-GO_FOR_CLAIM`

## 产物

- `cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe.py`
- `cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe_result.json`
- `cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe_atom_bindings.json.gz`
- `cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe_atom_graph_classes.json.gz`
- `cm2_round280_source_g_occurrence_materialization_and_dsu_preview_probe_provisional_components.json.gz`

Result object SHA256：
`e3aab261f28c441dc9bb44f0ad8c9bba1616bc0e4977ba37abe7705675a6a7d1`。

