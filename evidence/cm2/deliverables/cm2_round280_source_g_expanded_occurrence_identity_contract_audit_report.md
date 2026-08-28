# CM2 Round280：expanded occurrence identity contract 独立审计（严格 ZERO CREDIT）

## 结论

Round280 preview 的图计数仍可作为 **local component-DSU preview** 使用，但其中
两条 occurrence 语义假设与冻结的 Rounds265/266 contract 冲突，现正式
fail-closed 否决：

1. `atom graph quotient precedes occurrence identity assignment`：否决；
2. `one connected atom-graph class = one expanded occurrence`：否决。

冻结 contract 是：

> expanded occurrence 是一个经独立证明的本地 positive-open 3D region row
> identity；普通 common-face、true-seam adjacency 只作用于 component DSU，
> 不折叠 occurrence identity。

因此，Round279 的 `295,976` 个未绑定 canonical atoms 是 `295,976` 个潜在
新 occurrence rows，而不是 Round280 的 `75,588` 个 unanchored graph
classes。正式 credit 仍为零。

## 冻结证据

### 1. 历史 occurrence identity 一直按本地正开 region row

- Round174 对每个满足全套 strict 条件的正三维 child 生成唯一
  `resolved-3d` row，并记录 `physical_open_subset_positive=True`
  （source lines 5–14, 968–987）。
- Round179 对一次 dyadic split 释放的每个 strict regular child 单独生成
  `resolved-child` row（source lines 7–9, 608–640）。
- Round204 对每个 local wall region 单独生成 `region_row_id`，并要求
  `strict_open_region=True`、`positive_coordinate_volume=True`
  （source lines 1529–1547）。
- Round208 对每个 factor-region 单独保留 `candidate_region_id` 作为
  `region_row_id`，要求 `strict_open_3D_region_exists=True` 并发放一次
  local signature credit（source lines 466–507）。

这些来源合计形成 R266 的冻结 occurrence frontier：

- R174：`72,500`
- R179：`17,192`
- R204：`736`
- R208：`36,040`
- 总计：`126,468`

### 2. face glue 从未 collapse occurrence identity

Round265 明确：

- 把全部 `72,500` 个 R174 rows 各自作为 initially separate seeds
  （source lines 4–9, 633–669）；
- 对 `169,064` 条 safe faces 做 DSU union；
- union 后仍逐条重建 `126,468` occurrence frontier
  （source lines 1010–1028, 1229–1267）。

Round266 再加入 `2,652` 条 curved face edges，使 component quotient
`63,812 → 63,224`，但 occurrence frontier 仍为 `126,468`；统一 member
frontier逐项写入 `member_identity_preserved=True`
（source lines 1229–1263, 1401–1421）。

所以正面积 face path 证明的是 component connectivity，不是 occurrence
identity equality。

### 3. Round279 已完成唯一允许的现有 alias contraction

Round279：

- `332,020` source signature rows；
- 按 `(Round182 leaf, complete signature)` canonicalize 为 `332,016` atoms；
- 差额正好是 `4` 个 Round271 artificial W-tail `t`-split aliases；
- `36,040` atoms 保留既有 R208 occurrence anchor；
- 其余 `295,976` 明确标为 new occurrence-region atom candidates；
- `330,724` common-face rows 仍全部为零 occurrence/component credit。

这 4 个 alias 已在 atom ledger 之前收缩。不存在“任意 face-connected atoms
都可继续 identity collapse”的冻结授权。

## 可直接供 producer/verifier 执行的 deterministic rule

### Occurrence identity

1. 保留 R266 全部 `126,468` 既有 `local_occurrence_row_id`，不得改写或合并。
2. Round279 atom 若有唯一 R208 anchor，则映射到该既有 occurrence ID。
3. 每个无 anchor 的 Round279 canonical atom 独立作为一个 new-occurrence
   candidate。
4. 新 ID 固定为：

   `source-g-expanded-occurrence:SHA256(canonical([`
   `ROUND279_CANONICAL_ATOM_LOCAL_OCCURRENCE_V1,`
   `canonical_atom_id, atom_row_sha256, Round182_leaf_row_id,`
   `signature_sha256, sorted_source_signature_row_ids,`
   `frozen_true_support_boxes]))`

5. identity contraction 只允许来自显式的
   `EXACT_SAME_POSITIVE_OPEN_REGION_ALIAS` certificate。普通 common face、
   Round268 true seam 与 Jx/Jy 均不是 alias。

由此：

- singleton canonical-atom class 在该 atom 通过物理 promotion 后才等于一个
  occurrence；
- multi-atom class 是多个 occurrences 的 component-connectivity class；
- multi-anchor class 只给 component union evidence，所有既有 anchor identities
  原样保留。

### 正式提升每个 unbacked atom 的最小条件

每个 atom 必须逐项证明：

1. 从冻结 source-signature provenance cachelessly 重构；
2. 支撑是非空、connected、positive-open 的真实 3D physical region；
3. 完整 10-field signature 与 exact key 在整个认证支撑上严格不变；
4. true source-chart owner 正确，并有严格正体积 rational inner support；
5. 与既有 `126,468` occurrence frontier 的任何同物理重叠均被精确处置：
   exact alias 或严格不重叠，不能凭 signature/hash 猜测；
6. 新 atoms 两两不存在未处置的 same-positive-open-region 重复；
7. 仅 4 个已冻结 W-tail aliases 可预先收缩；
8. 独立 cacheless verifier 重建全部 candidate/alias partition，并攻击
   occurrence、alias、face、path、Jx/Jy forged credit。

若 `295,976/295,976` 全部通过，候选 occurrence census 才是
`126,468 + 295,976 = 422,444`。这只是条件式算术，目前正式 count 仍为
`126,468`。

## DSU 与 seam 的正确依赖顺序

1. 先固定/物化 occurrence identity nodes；
2. 每个 Round279 atom 唯一映射到一个 occurrence node；
3. 将 `330,724` common-face witnesses 作为 component edges；
4. 将 Round275 reverse-rechart transition cover 精确 incident-bind 到
   occurrence/atom nodes；
5. 将 Round268 的 `152` 个 true-seam patches 作为 2D same-point
   component edges；
6. 重建 exact-key-pure DSU 与最终 component IDs；
7. 最后进入 maximality。

因此跨 chart 有两种不同语义：

- **positive-volume same-physical overlap / duplicate representation**：
  在 occurrence counting 前做 identity dedup；
- **Round268 2D true-seam boundary patch**：
  occurrence identities 固定后做 component glue。

Jx/Jy 在两种语义中均为零 same-point credit。

## Round275 的 13,788 regions

Round275 物化了 `5,288 + 8,500 = 13,788` 个 connected adjacent-chart
positive-volume cover rows，但 source 明确写入 `occurrence_credit=0`，且这些
rows 来自此前被拒绝的 `880` coordinate guards。

当前不能直接宣称：

`126,468 + 295,976 + 13,788 = 436,232`。

每个 Round275 positive-open piece 必须先在以下三类中唯一落位：

1. `EXACT_ALIAS_OF_EXISTING_OCCURRENCE_OR_ROUND279_ATOM`：只作同物理表示
   witness，不新增 occurrence；
2. `STRICTLY_NEW_DISJOINT_POSITIVE_OPEN_SUPPORT`：通过上述 atom promotion
   条件后可新增一个 occurrence；
3. `PARTIAL_OVERLAP_OR_OUTER_ENCLOSURE_ONLY`：先精确细分为 disjoint physical
   partition，继续 fail-closed。

所以 Round275 当前授权新增 occurrence 数为 `0`；其最终新增数只能由完整
same-physical overlap/dedup ledger 决定，不能使用 raw row count。

## 对 Round280 preview 的保留与撤销

保留为零信用 component 算术：

- canonical atoms：`332,016`
- local face edges：`330,724`
- graph classes：`92,120`
- local preview old-component rank reductions：`2,072`
- seam 前 provisional component count：`136,740`

撤销 occurrence 解释：

- `75,588` 不能作为 new occurrence count；
- anchored class 中的 `163,232` 个 unbacked atoms 不能被一个 anchor 自动吸收；
- `92,120` class quotient 不先于 local occurrence identity；
- true seam 不折叠 occurrence identity。

## 严格状态

- formal new expanded occurrences：`0`
- expanded occurrences：`126,468`
- quotient components：`63,224`
- maximality：`0/63,224`
- fibres：`0/116`
- dispositions：`0/224,580`
- Jx/Jy same-point glue：`0`
- Gate5：`10/18`
- D02：`BLOCKED`
- CM2：`NO-GO_FOR_CLAIM`

## 产物与复放

- audit source：
  `cm2_round280_source_g_expanded_occurrence_identity_contract_audit.py`
- result：
  `cm2_round280_source_g_expanded_occurrence_identity_contract_audit_result.json`
- result object SHA256：
  `007a10d4da0d72a0fb57b91e026b8c703d4cd7daf38dcde0f97885a1e53f6354`
- result file SHA256：
  `873974c8b343961f9e7c1674a946681749a3c0267bc57a1ccc147ccd21b3bdfc`
- source SHA256：
  `ed0435b9ae4627d9b703c6afe92f3f7f3c1aa01bb631d3c3c30e55dfff1786d8`

`PYTHONHASHSEED=17` 与 `211` 输出及 result bytes 完全一致。
