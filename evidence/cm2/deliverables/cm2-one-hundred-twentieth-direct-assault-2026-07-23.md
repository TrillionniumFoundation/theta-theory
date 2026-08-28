# CM2 one-hundred-twentieth direct assault

Date: 2026-07-23  
Result: **49/49 semantic mutations and 15/15 strict-JSON mutations rejected.**

## Test contract

Every semantic mutant is applied to a deep copy of the certificate.  Nested
row/recut/slot digests and the envelope result digest are recomputed when the
mutated layer requires it.  The suite therefore tests the mathematical and
schema contract rather than merely relying on a stale SHA mismatch.

## Semantic mutations

The verifier rejects the following 49 uniquely labelled cases:

```text
gate5_global_upgrade
child_F5_upgrade
child_F7_upgrade
actual_recut_registry_forgery
actual_recut_count_forgery
F5_F6_slot_install_forgery
complete_block_forgery
gate5_block_forgery
cm2_upgrade
finite_child_forgery
round31_domain_reuse
child_registry_erasure
parent_count_mutation
family_count_mutation
rank_maturity_upgrade
residual_forgery
connected_rank_mutation
natural_boundary_capture
middle_H0_erasure
recut_F5_frontier_forgery
slot_field_swap
unknown_top
unknown_result
unknown_row
unknown_leaf
unknown_generator
unknown_recut
unknown_slot
parent_row_deleted
parent_row_duplicated
resigned_derivative_lower_inflation
resigned_derivative_sign_flip
resigned_middle_H0_lower_inflation
resigned_chart_margin_inflation
resigned_fixed_b_derivative_inflation
generator_family_deleted
generator_family_duplicated
F1_F4_slot_deleted
F1_F4_slot_duplicated
exact_b_decimal_hash_ambiguity
Round31_parent_W_ID_reuse
natural_boundary_owner_override
source_c0_zero_capture
third_coordinate_zero_capture
BYPASS_b3_as_collision_angle
BYPASS_actual_winner_H0_erasure
roof_two_duplicated_chart_pair
bare_collision_chart_without_type
target_chart_lost_owner_index
```

These cases cover claim escalation, parent/generator/slot census corruption,
re-signed quantitative forgery, exact-b and angular-lift identity errors,
natural/artificial boundary theft, BYPASS winner confusion, roof-two wall
chart collapse, namespace loss, unknown fields and nested schema changes.

## Strict JSON mutations

The strict parser rejects:

```text
duplicate_top_key
duplicate_nested_key
duplicate_deep_key
nan
positive_infinity
negative_infinity
json_float
overflowing_float
negative_zero
top_level_array
top_level_null
utf8_bom
unpaired_high_surrogate
unpaired_low_surrogate
oversized_integer
```

The certificate and verification accept only closed object schemas, reject
duplicate keys and nonfinite/float tokens, and do not permit non-object
envelopes or malformed Unicode payloads.

## Final state under assault

After all mutations, the unchanged canonical certificate independently
verifies with:

```text
child-local fields  F1-F4 = 4/18
F5-F18              NOT_INSTALLED
actual image recuts 0
global Gate5        10/18
complete blocks     0
CM2                 NO-GO_FOR_CLAIM
```

