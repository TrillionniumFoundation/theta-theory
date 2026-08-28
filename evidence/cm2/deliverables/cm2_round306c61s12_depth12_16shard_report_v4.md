# C61s12 depth-twelve 16-shard continuation — final v4

## Strict result

`PASS_COMPLETE_16_SHARD_DEPTH12_AGGREGATE_V4__SCHEMA_SPECIFIC_PARENT_CENSUS__ZERO_FORMAL_CREDIT`

C61s12 consumes exactly the 2,599 frozen C58s2 collision-2 residual leaves through a canonical, mutually exclusive 16-shard assignment. All 16 no-replace shard executions completed before aggregation. Partial shard statistics were never used for credit.

## Assignment and execution

- Independent assignment contract file/object: `7f7efeb0a060fea143c9f6a00b4722f2cc87632bff631feb598c434ca969a418` / `68c6e8a0899c66056724ea29c42949100b2fc6a625865867fd30aacc16d36f7d`.
- Assignment result file/object: `7d6fae044bd194c790dfc5dba077481d47e3e6850455463bfd61c8832e29ca69` / `d1f9549826fa424bd2c29fc217e714527c2e56ac25361e48f31d95aa33536d19`.
- Assignment inventory: `6ad0fe4d52c468de31fb39f72eabd825320eee86b9738f52fb1142da8a1736b4`.
- Assignment preimage: canonical UTF-8 JSON with no trailing newline, lexicographically sorted keys and compact separators: `{"path":P,"source_handoff_ordinal":N}`.
- Shard formula: `int(SHA256(preimage),16) % 16`.
- Assignment coverage: 2,599/2,599, complete and pairwise disjoint.
- Runner: `7788155920c088f769b4a61d66be0c7951495e88f2d3676acca8f93a2ca531e4`.
- Completed shard receipts: 16/16.

## Final census

- Route evaluations: 87,153.
- C61 output leaves: 44,876 = 23,997 strict terminal + 0 collision-3-ready + 20,879 exact collision-2 handoffs.
- Whole C58 input residuals made terminal: 362/2,599.
- Each of the 2,599 source partitions is prefix-free and exactly conserves its input volume.
- Final aggregate result file/object: `06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e` / `05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584`.

The complete 12-parent reconstruction explicitly combines 462 carried C57 terminals, 2,949 carried C58 terminals, and all C61 outputs. Its 48,287 leaves comprise 27,408 strict terminal and 20,879 collision-2 leaves, with zero collision-3-ready leaves. Every parent is prefix-free with exact Kraft sum `1`. No reflection pair or singleton is wholly closed: 0 closed / 24 remaining.

## Independent verification

The final independent audit reconstructed the canonical assignment, all 16 receipts and shard ledgers, the 2,599-source union and mutual exclusion, every source partition, the v4 aggregate ledgers, and the full C57+C58+C61 parent census/Kraft equations.

- Verifier: `0e85c8f732cc9553ecbc8735a439442ee6288edbecd78e940c7ea8c015adc187`.
- Verification file/object: `2dc773d0051cc9668cdf7752fb61ac09f495044f566972faa335fffc509e9fc7` / `066e03be0c41600f5fb5cc2c157fe6e7eb04d1060896dd1acc910b06aab30b24`.
- Self-test file/object: `b5a6ad21006d690637c797e7459363f2d6d8e55ad3abd5c112e817de5f915f32` / `77a6091d60a883826fc4f9e8786128ae6dd9e79bcfc7d8662b9da1ed0262339e`.
- Coherent hostile tests: 40/40 PASS.

## Rejected stages

Three earlier aggregate stages are explicitly rejected and excluded from the final manifest:

- v1: omitted the C57 carried terminals and failed parent Kraft before result publication.
- v2: Kraft was exact, but a generic field accessor misclassified all 462 C57 terminals as collision-2 rows; its result is rejected.
- v3: corrected the census but failed canonical result serialization before result publication due to a local name collision.

Only the three rejection-marker Markdown files are included in the final manifest; no v1–v3 stage ledger or result is included or consumed.

## Formal boundary

C61s12 remains a zero-credit development checkpoint. Formal, whole-parent, and D02 gate credits are zero. No runtime, canonical, pointer, seal, or pre-existing file was written. CM2 remains `NO-GO_FOR_CLAIM`.

The next valid continuation consumes only the 20,879 exact v4 collision-2 residual leaves under a fresh frozen assignment and independent aggregate audit.
