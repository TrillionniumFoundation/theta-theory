# CM2 one-hundred-twenty-second direct assault

Date: 2026-07-23  
Result: **120/120 semantic mutations and 15/15 strict-JSON mutations rejected.**

## Test contract

Every semantic mutant is applied to a deep copy of the Round122 certificate.
The changed nested row digests and the envelope result digest are recomputed
before verification.  The tests therefore attack the closed mathematical
contract, not a stale outer SHA.

## Semantic mutations

The independent verifier rejects the following 120 uniquely labelled cases:

```text
collar_widen
collar_text_widen
source_G_moves
W_shift_axis
cut_guard_false
cut_pair_guard_false
round121_modified
round121_digest
physical_core_row_delete
physical_stage_row_delete
candidate_census_168
candidate_stage_census
candidate_total_census
legacy_grammar_63
old_Q2_reuse
new_rank3_census_false
physical_margin_inflate_candidate_tangency
physical_margin_inflate_coordinate_velocity_zero
physical_margin_inflate_core_face
physical_margin_inflate_integer_corner_ray
physical_margin_inflate_owner_gap
physical_margin_inflate_root_sign
physical_margin_inflate_source_chart_seam
physical_margin_inflate_source_endpoint_wall
physical_margin_inflate_source_homogeneity
physical_margin_inflate_target_chart_seam
physical_margin_inflate_target_endpoint_wall
physical_margin_inflate_target_homogeneity
physical_minimum_zero
physical_incidence_nonzero
physical_residual_nonzero
five_grammar_delete
five_grammar_swap_kind
five_grammar_nonempty
seven_grammar_delete
seven_grammar_audit_key
seven_grammar_nonempty
moving_face_delete
moving_face_duplicate
moving_face_reorder
moving_face_stage
moving_face_natural_j
moving_face_equation
moving_face_endpoint
moving_face_bracket
moving_face_Fx_sign
moving_face_Fx_inflate
moving_face_Fx_lower_zero
moving_face_Fs_shrink
moving_face_Fxx_shrink
moving_face_Fxs_shrink
moving_face_Fss_shrink
moving_face_xprime_improve
moving_face_xsecond_improve
moving_face_unique_false
moving_face_order_false
moving_face_separation_improve
moving_face_F8_improve
moving_face_F8_formula
moving_face_kappa
moving_face_cone
moving_face_F9_improve
moving_face_F12_path
moving_face_F12_improve
moving_face_as_physical
outer_face_delete
outer_Fx_zero
outer_Fx_noncanonical
outer_owner
outer_as_physical
trace_delete
trace_side
trace_child
trace_as_physical
incidence_delete
incidence_face_swap
incidence_two_faces_false
F7_bare_Xi
F7_density
F7_product
F7_roof_factor
F8_theorem_improve
F9_stage1_improve
F9_stage2_improve
F10_nonzero
F11_tight_seed_value
F11_roof_factor
F12_bound_improve
F13_nonzero
F16_nonzero
dynamic_F11_seed_value
dynamic_F11_diagnostic_used
slot_delete
slot_reorder
slot_key
slot_field
slot_roof
slot_subbranch
slot_child
slot_face_pair_F9
slot_bare_Xi
slot_F7_density
slot_roof_factor
slot_F11_source
combined_fields_add_F14
upstream_pin
precision_downgrade
count_ledger
maturity_inflate
global_gate_inflate
F14_install
complete_block_inflate
gate5_block_inflate
CM2_inflate
nonclaim_delete
scope_inflate
schema_mutation
unknown_result_field
bool_as_precision
unknown_moving_row_field
```

These attacks cover:

- widening or changing the exact dyadic collar and movement law;
- mutating the frozen Round121 seed, guards or result digest;
- deleting physical audit rows or replacing the complete `169`-candidate
  rank-3 census by old Q2/time-2 identifiers;
- virtually improving any of the twelve strict physical margins;
- deleting or changing the five-face and seven-boundary grammars;
- deleting, duplicating, reordering or relabelling any of the 23 moving
  implicit faces;
- changing an implicit equation, root bracket, derivative sign, jet bound,
  graph uniqueness, face order or pair separation;
- deleting either stationary outer face, zeroing its exact `1/10^90`
  derivative or supplying a noncanonical fraction;
- conflating artificial recut faces or traces with physical singular faces;
- deleting or swapping traces and child-face incidence rows;
- installing bare Xi as F7, changing the density factor, or adding a
  transparent-wall F7/F11 factor;
- virtual improvement of F8, F9, F11 or F12;
- nonzero F10/F13/F16 on a typed-empty physical face family;
- substituting the tight along-seed F11 diagnostics for the authoritative
  full-phase envelopes;
- deleting, reordering or cross-wiring full-key slots, faces, roofs,
  subbranches or children;
- installing F14, inflating local/global maturity, completing a block or
  promoting CM2;
- pin, precision, type, schema, scope, count and strict-nonclaim attacks.

## Strict JSON mutations

The strict parser rejects:

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

Closed schemas, duplicate-key rejection, float-token rejection, canonical
integer/fraction rules, boolean-versus-integer separation and Unicode
validation remain active.

## Final state under assault

After all mutations, the unchanged canonical certificate independently
verifies with:

```text
exact analytic b seeds        1
common actual children        24
physical face instances       0
moving artificial faces       23
stationary outer faces         2
artificial one-sided traces   48
new full-key slots            960
combined full-key slots       1680
child-local fields            F1-F13 and F16 = 14/18
F14/F15/F17/F18               NOT_INSTALLED
global Gate5                  10/18
complete blocks               0
CM2                           NO-GO_FOR_CLAIM
```
