# Five-paper blocker and maximal-strengthening closure status

**Date:** 2026-08-28  
**Scope:** θ-Theory only  
**Branch:** `theta-maximal-strengthening-closure-2026-08-28`

## Controlling interpretation

The series closes the internal proof DAG at the maximal correct scope.  An
impossible unrestricted statement is closed by refutation/maximality; a
positive statement is closed by proving it on an explicit packet class and by
exhibiting a nonempty actual subclass.  No stronger system verification is
hidden inside the word `general`.

The five items previously listed as outside-theorem strengthening work now
have actual positive theorems, exact maximality/no-go results where the fully
unrestricted version is false, and named P1--P5 exports.

```yaml
paper_I:
  title: Bilateral graph-current mixing and higher response
  actual_nonzero_witness: open_four_branch_three_seam_family
  product_CM2: CLOSED
  finite_DQ_l1: CLOSED
  graded_response_ladder: CLOSED_X5_TO_X1
  third_source_totalization: CLOSED
  CM2_to_U3: CLOSED
  actual_nonconjugate_specular_radial_U3:
    invariant_projector_U_infinity: CLOSED
    exact_coboundary_twisted_U_infinity: CLOSED
    nonconjugacy: CLOSED_BY_PERIOD_TWO_MULTIPLIER
  generic_geometry_only_noncoboundary_U3: CLOSED_BY_REFUTATION_AND_MAXIMALITY
  unrestricted_universal_claim: CLOSED_BY_REFUTATION

paper_II:
  title: Higher pressure response and physical diffusion
  twisted_pressure_C3: CLOSED_RELATIVE_TO_PAPER_I_PACKET
  low_frequency_suspension_resolvent: CLOSED_WITH_ENTRY_EXIT_OPERATORS
  physical_time_root: CLOSED
  diffusion_response: CLOSED
  common_operator_space: CLOSED_BY_SMOOTH_QUADRATIC_ATLAS_STABILIZATION
  xp_coefficient_lift: CLOSED
  ellipticity: CLOSED_RELATIVE_TO_NONCOBOUNDARY_AND_COUPLING_RANK
  actual_four_branch_positive_diffusion: CLOSED
  compact_moving_family_high_frequency_BDL: CLOSED_RELATIVE_TO_STRICT_WITNESS_PACKET
  graded_high_frequency_parameter_derivatives: CLOSED
  actual_radial_all_frequency_coboundary_channel: CLOSED
  universal_single_scalar_grazing_weight_domain: CLOSED_BY_REFUTATION

paper_III:
  title: Doob-selected rough homogenization and theta-expectation
  no_feedback_Doob_selector: CLOSED
  uniform_martingale_rough_package: CLOSED
  full_scale_nonautonomous_limit: CLOSED_WITH_COMPATIBLE_MODULUS_OR_DIRECT_CHARACTERISTICS
  qualitative_uniform_WIP_only: COFINAL_DIAGONAL_RESULT
  actual_four_branch_full_scale: CLOSED
  fractional_Sobolev_rough_rate:
    topology: step_two_W_eta_p_KR
    upper_exponent: one_half_minus_eta
    lower_exponent: one_half_minus_eta
    status: OPTIMAL_IN_DECLARED_TOPOLOGY
  topology_free_optimal_rate: CLOSED_BY_TYPING_NO_GO
  explicit_block_window: CLOSED
  actual_four_branch_HJB_theta: CLOSED
  explicit_nonconvex_non_subadditive_example: CLOSED

paper_IV:
  title: Filtering and Isaacs limits
  bounded_filter_contraction: CLOSED
  initial_belief_value_collapse: CLOSED_WITH_VANISHING_SLOW_INITIAL_LAYER
  weighted_filter_packet: CLOSED
  actual_unbounded_weighted_filter: CLOSED
  sequential_lower_upper_values: CLOSED
  simultaneous_mixed_Isaacs: CLOSED
  unrestricted_general_pure_saddle: CLOSED_BY_MATCHING_PENNIES_REFUTATION
  pure_saddle_iff_pure_Isaacs: CLOSED
  measurable_pure_selector: CLOSED
  strong_concave_convex_unique_saddle: CLOSED
  actual_four_branch_pure_Isaacs_game: CLOSED
  belief_state_HJB: CLOSED

paper_V:
  title: Representation calculus for theta-expectations
  no_single_linear_law_obstruction: CLOSED
  payoff_calibrated_linearization: CLOSED
  typed_FBSDE_control_BSDE_2BSDE_PPDE: CLOSED
  actual_noncompact_delay_state: CLOSED
  actual_entire_window_payoff: CLOSED
  stationary_weighted_filter_to_path_average: CLOSED
  actual_segment_DPP: CLOSED
  horizontal_shift_path_equation: CLOSED
  actual_BSDE_path_evaluation: CLOSED
  reverse_use_to_prove_HJB: FORBIDDEN

series:
  actual_scoped_chain_through_theta: CLOSED
  actual_scoped_chain_through_mixed_Isaacs: CLOSED
  actual_scoped_chain_through_pure_Isaacs: CLOSED
  actual_weighted_noncompact_filter: CLOSED
  actual_noncompact_path_evaluation: CLOSED
  former_outside_theorem_strengthenings: 5
  former_outside_theorem_strengthenings_closed: 5
  internal_unnamed_arrows: 0
  stale_unconditional_imports: REMOVED
  circular_dependencies: 0
  hostile_base_audit_rounds: 3
  hostile_strengthening_audit: COMPLETE
  external_peer_review: NOT_PERFORMED
  mathematical_proof_certified_externally: false
  formal_credit: 0
```

## Maximality clauses

The following stronger formulations are false or ill-typed and therefore are
not counted as open gaps:

1. finite-horizon specular geometry alone implies generic noncoboundary U3;
2. one scalar pointwise grazing weight gives one ungraded moving-flow domain
   for every deformation;
3. an enhanced-WIP rate is “optimal” without naming a topology and test class;
4. mixed minimax implies a pure saddle;
5. a fast belief variable may be retained in a path PPDE without its limiting
   generator.

Each item has a counterexample, obstruction, or corrected maximal theorem in
`papers/theta-program/maximal-strengthening/`.

## New theorem exports

```text
P1-SINAI-RADIAL-U3
P2-BDL-HF-FAMILY
P3-RWIP-OPTIMAL-WETA-P
P4-PURE-ISAACS-MAXIMAL
P4-WEIGHTED-NONCOMPACT-ACTUAL
P5-PATH-ACTUAL
```

The weighted/path construction also forms the series-level bundle
`P4-P5-WEIGHTED-PATH-ACTUAL`.

## Normative files

- `../maximal-strengthening/MAXIMAL_STRENGTHENING_STATUS.md`
- `../maximal-strengthening/SPECULAR_SINAI_RADIAL_U3.md`
- `../maximal-strengthening/MOVING_FAMILY_HIGH_FREQUENCY_BDL.md`
- `../maximal-strengthening/OPTIMAL_ENHANCED_WIP_RATE.md`
- `../maximal-strengthening/PURE_STRATEGY_ISAACS.md`
- `../maximal-strengthening/WEIGHTED_NONCOMPACT_PATH_ACTUALIZATION.md`
- `../maximal-strengthening/HOSTILE_STRENGTHENING_AUDIT.md`
- `THEOREM_INTERFACE_MANIFEST.yaml`
- five per-paper interfaces, blocker ledgers, and strengthening appendices.

## Import policy

Every paper imports only named outputs from upstream papers.  No manuscript
may import the old blanket response label.  Every downstream claim must name
the exact export ID and preserve its source-specific, topology-specific,
high-frequency, pure/mixed, weighted, and path-state scope.

## Review boundary

All results are internal proof drafts.  External expert review, novelty review,
full bibliography verification, and journal LaTeX preparation have not been
performed and are not replaced by structural verification.
