# CM2 one-hundred-twenty-third direct assault

Date: 2026-07-23  
Result: **110/110 semantic mutations and 15/15 strict-JSON mutations rejected.**

## Test contract

Every semantic mutant is applied to a deep copy of the final Round123
certificate.  The verifier recomputes every affected nested row digest and
the outer result digest before checking the mutation.  The assault therefore
tests the closed mathematical contract rather than relying on a stale
envelope hash.

The labels below are copied in canonical verification order.  They exactly
match the `semantic_attack_labels` and `strict_JSON_attack_labels` arrays in
the frozen verification artifact.

## Semantic mutations

```text
schema_mutation
unknown_result_field
precision_downgrade
root_depth_downgrade
upstream_pin_mutation
upstream_pin_delete
status_fail_closed
round121_result_pin
round122_certificate_pin
round122_fields_add_F14
coordinate_a3
coordinate_U3_orientation
coordinate_actual_owner
coordinate_actual_chart
coordinate_length_claim
coordinate_derivative_inflate
stage3_root_delete
stage3_root_duplicate
stage3_root_reorder
stage3_root_level
stage3_root_equation
stage3_root_bracket
stage3_root_left_sign
stage3_root_derivative_inflate
stage3_root_lower_owner
stage3_root_numeric_identity
unknown_stage3_root_field
stage3_cell_delete
stage3_cell_duplicate
stage3_cell_endpoint
stage3_cell_right_closed
stage3_cell_left_owns_cut
stage3_cell_terminal_flag
merged_cut_delete
merged_cut_duplicate
merged_cut_reorder
merged_cut_origin
merged_cut_stage
merged_cut_overlap
merged_min_gap_inflate
output_fragment_delete
output_fragment_duplicate
output_fragment_id
output_fragment_child
output_fragment_natural_index
output_fragment_recut_id
output_fragment_length_fake
output_fragment_gap_inflate
output_fragment_right_closed
output_fragment_equal_mass
partition_delete
partition_output_count
partition_output_ids
partition_mass_identity
partition_fragment_multiplier
partition_inverse_length_multiplier
leg_output_delete
leg_output_duplicate
leg_actual_target
leg_actual_chart
leg_orientation_flip
leg_derivative_inflate
leg_separation_inflate
leg_output_member_count
leg_output_member_delete
leg_output_length_fake
leg_same_key_F10
leg_b3_collision_angle
theorem_alpha
theorem_normalization
theorem_regular_density_cone
theorem_pushforward_J
theorem_conditional_density
theorem_recurrence_wrong_parentheses
theorem_equal_mass
theorem_F10_pays_F14
theorem_family_multiplier
theorem_F14_value_33
theorem_F14_margin_drop_delta
theorem_roof_factor_five
theorem_generic_34_to_fifth
theorem_direct_bound_product
theorem_signed_factor_two
theorem_cancellation
F14_slot_delete
F14_slot_duplicate
F14_slot_field
F14_slot_value
F14_slot_key
F14_slot_roof
F14_slot_leg
F14_slot_same_key_F10
F14_slot_F10_pays
F14_slot_roof_multiplier
F14_slot_b3_collision_angle
combined_slot_count_2016
combined_fields_add_F15
count_ledger_fragment_count
count_ledger_slot_count
maturity_inflate
install_F15
install_F17
install_F18
global_gate_inflate
complete_block_inflate
gate5_block_inflate
CM2_inflate
strict_nonclaim_delete
scope_inflate
bool_as_precision
```

These attacks cover:

- certificate schema, precision, root depth, status, byte pins, closed fields,
  and frozen Round121/Round122 inputs;
- the third-collision coordinate, owner, chart, orientation, derivative, and
  total adapted length;
- deletion, duplication, reordering, relabelling, rebracketing, or
  mis-owning any third-output root or natural cell;
- deletion, duplication, reordering, origin changes, overlaps, and virtual
  spacing improvements in the 215-cut merge;
- deletion, duplication, cross-child wiring, fake lengths, endpoint ownership,
  equal-mass assumptions, and fragment-count multipliers in the 216-member
  properization;
- deletion or cross-wiring of child partitions and the 72 physical-leg
  output rows;
- changing the accepted density cone, conditional Jacobian or normalization,
  the authoritative recurrence, mass conservation, or Jordan extension;
- replacing the family-level mass-weighted inverse-length estimate by a
  fragment-count multiple;
- lowering the one-step value to 33, dropping its exact `delta` term, charging
  F10 zero, or confusing the direct path bound with the generic product;
- multiplying by five symbolic roof levels or treating the bypass `b3` as a
  collision angle;
- deleting, duplicating, relabelling, re-roofing, re-staging, or cross-wiring
  an F14 full-key slot;
- turning 216 fragments into source slots, adding F15, inflating local/global
  maturity, completing a block, or promoting CM2;
- strict scope, nonclaim, type, and boolean-as-integer attacks.

## Strict JSON mutations

```text
top_duplicate_key
deep_duplicate_key
NaN
Infinity
negative_Infinity
JSON_float
JSON_exponent
top_array
top_null
negative_zero
oversized_integer
BOM
unpaired_surrogate
bool_as_integer
noncanonical_fraction
```

Closed schemas, duplicate-key rejection, non-finite and float-token
rejection, canonical integer/fraction rules, Unicode validation, and
boolean-versus-integer separation remain active.

## Canonical contract after assault

The unchanged canonical certificate independently verifies with:

```text
exact analytic b seeds                  1
actual common children                 24
third-output internal cuts            192
third-output natural cells            193
merged internal cuts                  215
third-output fragments                216
input child partitions                 24
physical-leg output rows               72
new F14 full-key slots                120
combined child-local slots           1800
F14 one-step value                     34
generic three-leg composition       39304
direct exact-seed path bound           34
child-local fields             F1-F14,F16 = 15/18
F15/F17/F18                  NOT_INSTALLED
global Gate5                         10/18
complete blocks                          0
Gate5 blocks                             0
CM2                           NO-GO_FOR_CLAIM
```
