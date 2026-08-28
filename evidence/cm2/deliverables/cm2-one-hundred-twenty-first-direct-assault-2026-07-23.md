# CM2 one-hundred-twenty-first direct assault

Date: 2026-07-23  
Result: **79/79 semantic mutations and 15/15 strict-JSON mutations rejected.**

## Test contract

Every semantic mutant is applied to a deep copy of the certificate.  The
affected nested row digests and the envelope result digest are recomputed
before verification.  These are therefore re-signed contract and mathematical
attacks, not stale-SHA checks.

## Semantic mutations

The independent verifier rejects the following 79 uniquely labelled cases:

```text
global_gate_upgrade
child_maturity_upgrade
complete_block_forgery
gate5_block_forgery
cm2_upgrade
F7_upgrade
seed_count_forgery
count_bool_as_int
residual_root_forgery
slot_count_forgery
strict_scope_widening
old_angular_lift
decimal_seed_ID
seed_parent_swap
anchor_partial_t_inflation
anchor_partial_t_sign_flip
source_H0_erasure
source_c0_orientation_flip
source_b3_orientation_flip
source_adapted_density_mutation
source_adapted_identity_mutation
source_slope_four_erasure
source_theta_coefficient_mutation
source_phi_coefficient_mutation
source_b3_formula_mutation
source_adapted_coordinate_formula_mutation
slope_intercept_enclosure_shift
stage_orientation_flip
adapted_normal_only
BYPASS_designated_owner
BYPASS_b3_collision_angle
area_Jacobian_as_F5
wall_adds_Jacobian
F5_path_virtual_improvement
F6_path_not_summed
common_right_endpoint_closed
common_rank_bool_as_int
common_stage_index_swap
common_length_inflation
refined_b3_as_angle
recut_right_endpoint_closed
recut_strict_lower_equal_length
recut_coordinate_mutation
recut_adapted_lower_mutation
recut_adapted_upper_mutation
endpoint_numeric_ID
endpoint_owner_swap
endpoint_derivative_inflation
slot_F5_virtual_improvement
slot_field_index_bool_as_int
slot_roof_bool_as_int
slot_roof_out_of_range
slot_recut_mismatch
upstream_pin_mutation
nonreduced_fraction
zero_denominator_fraction
negative_denominator_fraction
leading_zero_fraction
wrong_type_count
wrong_type_endpoint_stage
wrong_type_slot_roof
endpoint_deleted
endpoint_duplicated
endpoint_reordered
recut_deleted
common_child_deleted
refined_subbranch_duplicated
slot_deleted
slot_reordered
strict_nonclaim_deleted
unknown_result_field
unknown_endpoint_field
unknown_slot_field
unknown_pin_row
missing_result_field
missing_endpoint_field
anchor_bracket_shift
U2_derivative_enclosure_shrink
endpoint_bracket_shift
```

These attacks cover:

- Gate5, complete-block and CM2 claim escalation;
- exact-seed identity, anchor-root, angular-lift and slope-four corruption;
- whole-source membership, orientation and adapted-density corruption;
- use of the designated BYPASS miss in place of the actual G-winner;
- `b3` misuse as a collision angle and area Jacobian `1` misuse as F5;
- image orientation, adapted-coordinate and stage-length corruption;
- endpoint deletion, duplication, reordering, bracket movement and false
  uniqueness/derivative improvements;
- recut ownership, endpoint openness, natural index and common-rank errors;
- refined-subbranch, roof-level, slot and materialized-input mismatches;
- F5/F6 virtual improvement and transparent-wall extra-factor forgery;
- unknown/missing nested fields, wrong types, boolean-as-integer and
  noncanonical fractions.

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

Closed object schemas, duplicate-key rejection, float-token rejection,
canonical integer/fraction rules and Unicode validation all remain active.

## Final state under assault

After all mutations, the unchanged canonical certificate independently
verifies with:

```text
exact analytic b seeds   1
stage recuts             26
pullback cuts            23
common actual children   24
child-local fields       F1-F6 = 6/18
F7-F18                   NOT_INSTALLED
global Gate5             10/18
complete blocks          0
CM2                      NO-GO_FOR_CLAIM
```
