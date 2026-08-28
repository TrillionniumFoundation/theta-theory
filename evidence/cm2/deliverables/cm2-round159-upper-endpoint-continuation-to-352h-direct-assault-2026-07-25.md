# CM2 Round159 — direct assault record

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
tamper_verification_inheritance
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
coherent_inheritance_tamper
coherent_verification_inheritance_tamper
coherent_atlas_count_tamper
coherent_continuation_count_tamper
coherent_internal_adjacency_tamper
coherent_census_components_and_total_tamper
```

The strict parser also rejects duplicate-key JSON, a UTF-8 BOM, a non-object
top level, NaN, a raw NUL, invalid UTF-8, trailing garbage, finite
floating-point JSON (`1.0`), overflow floating-point JSON (`1e400`), an escaped
NUL, a lone high surrogate and a lone low surrogate.

Final result: `35/35` semantic/document attacks and `12/12` strict
JSON/encoding attacks rejected.
