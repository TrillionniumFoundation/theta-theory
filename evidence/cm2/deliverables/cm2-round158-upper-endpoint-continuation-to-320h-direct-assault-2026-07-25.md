# CM2 Round158 — direct assault record

Date: 2026-07-25

Rejected semantic and document mutations:

```text
delete_row
survive
invent_event
disconnect
claim_terminal
close_D02
authorize_D03
promote_gate5
create_block
promote_CM2
tamper_adjacency
tamper_inheritance
tamper_census
wrong_status
extra_field
type_confusion
nested_type_confusion
claim_continuation_complete
tamper_corridor
tamper_scale
tamper_next_gate
wrapper_wrong_schema
wrapper_result_sha
wrapper_extra_key
coherent_row_tamper
coherent_first_seam_tamper
coherent_census_total_tamper
coherent_row_reorder
```

The strict parser also rejects duplicate-key JSON, a UTF-8 BOM, a non-object
top level, NaN, NUL, invalid UTF-8, trailing garbage, finite floating-point
JSON (`1.0`) and overflow floating-point JSON (`1e400`).

Final result: `28/28` semantic/document attacks and `9/9` strict JSON/encoding
attacks rejected.
