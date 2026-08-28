# C61s12 aggregate v1 stage — rejected

Status: `REJECTED_INCOMPLETE_C57_CARRY__NO_RESULT_OBJECT__ZERO_CREDIT`

The first aggregate attempt stopped fail-closed at the 12-parent Kraft check because it combined the C58 terminal carry and C61 outputs but omitted the 462 earlier C57 terminal leaves. It produced no aggregate v1 result object and cannot be used as an authority, checkpoint, census source, or credit source.

The three stage files are retained only for forensic byte history:

- `aggregate_leaf_ledger_v1.jsonl.gz`: `2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2`
- `aggregate_source_summary_v1.jsonl.gz`: `477a60ace952d70dd81f46a97cb6ebf38797a3ec90e72eda7f6a67455fb789d7`
- `aggregate_parent_summary_v1.jsonl.gz`: `9ceffb7310338057cfe71a4ae1e2c98d2c485d81cdef906532a801f457a38d64`

The first two byte streams happen to match their v2 counterparts because their computations precede the failed parent merge. They remain excluded transactionally: only the v2 filenames, v2 result object, and final v2 manifest may be consumed.

Formal credit, whole-parent credit, and D02 gate credit are all zero. No runtime or canonical state was written.
