# CM2 Round157 — direct assault record

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
coherent_row_reorder
```

Duplicate-key JSON, UTF-8 BOM, non-object top level, NaN, NUL, invalid UTF-8,
trailing garbage and floating-point JSON are also rejected.

Final result: `26/26` semantic/document attacks and `8/8` strict JSON/encoding
attacks rejected.
