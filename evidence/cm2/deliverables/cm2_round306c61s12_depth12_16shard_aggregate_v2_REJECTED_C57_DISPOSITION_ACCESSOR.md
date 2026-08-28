# C61s12 aggregate v2 — rejected

Status: `REJECTED_C57_LEAF_DISPOSITION_ACCESSOR__ZERO_CREDIT`

Independent audit rejected aggregate v2 before manifest freeze. Its 12 parent Kraft equations are exact, but its parent census used `row.get("disposition")` for every source schema. C57 leaf rows use `leaf_disposition`, so all 462 carried C57 strict terminals were misclassified as collision-2 rows.

Consequences relative to the correct schema-specific census:

- aggregate terminal count was 462 too small;
- aggregate collision-2 count was 462 too large;
- prefix-freeness and Kraft conservation were unaffected;
- no aggregate v2 credit, authority, manifest, or downstream consumption is permitted.

The v2 result object `423af9275a7b61a853828053bbb6212f4a6a87fbe5176946d3a82f540df6a7f8` and all v2 ledgers are forensic rejected bytes only. The fresh v3 aggregate uses explicit schema branches: C57 `leaf_disposition`; C58/C61 `disposition`.

Formal credit, whole-parent credit, and D02 gate credit are zero. No runtime or canonical state was written.
