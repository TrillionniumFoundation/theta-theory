# C61s12 aggregate v3 stage — rejected

Status: `REJECTED_RESULT_SERIALIZATION_NAME_COLLISION__NO_RESULT_OBJECT__ZERO_CREDIT`

The fresh v3 parent replay correctly used schema-specific disposition accessors and completed all 12 Kraft/census rows. Before result publication, however, a local helper named `disposition` shadowed the aggregate disposition-census dictionary. Canonical JSON serialization rejected the function value, so no v3 result file or object was created.

All v3 stage ledgers are excluded from the final inventory and manifest. They are forensic failed-stage bytes only and are not consumed by v4.

The v4 transaction renames the helper to `row_disposition` and requires an in-memory canonical serialization plus object-hash replay before publishing any result bytes.

Formal credit, whole-parent credit, and D02 gate credit are zero. No runtime or canonical state was written.
