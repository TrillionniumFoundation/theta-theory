# θ-Theory maximal strengthening closure status

**Date:** 2026-08-28  
**Scope:** θ-Theory only; Navier–Stokes excluded.  
**Branch:** `theta-maximal-strengthening-closure-2026-08-28`  
**Base:** `theta-five-paper-closure-2026-08-28@0abb452732ec9e5a748904ad77800bdcaa00248b`  
**Policy:** `LATEST-WINS / FAIL-CLOSED / ACTUAL-OR-MAXIMALITY / NO-HIDDEN-STRENGTHENING / NO-REVIVAL-OF-REFUTED-UNIVERSAL-CLAIMS`

## Controlling result

The five items formerly classified as strengthening work are closed in the
maximal mathematically correct sense: each item is resolved by an actual
system theorem, an exact impossibility/maximality theorem, or both. A false
unrestricted version is not counted as an open lemma after it has been
refuted and replaced by the strongest valid theorem.

```yaml
specular_Sinai_U3:
  export: P1-SINAI-RADIAL-U3
  ambient_family: actual_nonconjugate_specular_finite_horizon_radial_family
  nonconjugacy_witness: changing_period_two_multiplier
  invariant_projector_U_infinity: PROVED_BY_DIFFERENTIATED_INVARIANCE
  exact_coboundary_twisted_U_infinity: PROVED_BY_GAUGE_CONJUGACY
  moving_singularity_complete_assembly_through_order_three: PROVED
  generic_noncoboundary_all_source_U3: REFUTED_AS_GEOMETRY_ONLY_CLAIM
  maximal_scope: source_specific_complete_assembly_or_explicit_bilateral_packet

moving_family_BDL:
  export: P2-BDL-HF-FAMILY
  compact_family_uniform_high_frequency_resolvent: PROVED_RELATIVE_TO_EXPLICIT_UNIFORM_BDL_WITNESS
  witness_openness_and_finite_cover_uniformization: PROVED
  fixed_common_operator_bundle: PROVED_BY_QUADRATIC_ATLAS_STABILIZATION
  parameter_resolvent_derivative_formula_through_order_three: PROVED_ON_GRADED_SOURCE_CHANNELS
  actual_radial_coboundary_all_frequency_channel: PROVED_BY_GAUGE_CONJUGACY
  universal_single_pointwise_weight_domain: REFUTED_BY_GRAZING_WEIGHT_RATIO
  maximal_scope: uniform_fibrewise_BDL_plus_certified_graded_parameter_channels

optimal_enhanced_WIP_rate:
  export: P3-RWIP-OPTIMAL-WETA-P
  topology: step_two_fractional_Sobolev_rough_path_W_eta_p
  range: one_over_p_less_than_eta_less_than_one_half
  upper_rate_actual_four_branch: N_power_minus_one_half_plus_eta
  lower_rate_piecewise_linear_class: SAME_ORDER
  status: OPTIMAL_EXPONENT_PROVED_IN_DECLARED_TOPOLOGY
  endpoint_smooth_metric_rate: N_power_minus_one_half_when_third_cumulant_nonzero
  universal_topology_free_optimal_rate: REFUTED_AS_ILL_TYPED

pure_strategy_Isaacs:
  export: P4-PURE-ISAACS-MAXIMAL
  unrestricted_general_existence: REFUTED_BY_MATCHING_PENNIES
  compact_continuous_equivalence: pure_saddle_iff_pure_Isaacs_equality
  measurable_selector: PROVED_UNDER_CARATHEODORY_DATA_AND_NONEMPTY_SADDLE_SET
  strong_concave_convex_class: UNIQUE_PURE_SADDLE_PROVED
  actual_four_branch_control_game: UNIQUE_PURE_SADDLE_PROVED
  mixed_to_pure_without_certificate: FORBIDDEN

weighted_noncompact_filter:
  export: P4-WEIGHTED-NONCOMPACT-ACTUAL
  deterministic_fast_base:
    - four_branch_moving_seam
    - countable_full_branch_unbounded_innovations
    - two_sided_uniform_Bernoulli_shift
  noncompact_hidden_state: contractive_AR1_with_unbounded_support
  polynomial_Lyapunov: PROVED
  weighted_filter_moment_ball: PROVED
  weighted_filter_contraction: PROVED_WITH_OBSERVATION_GAP

path_actualization:
  export: P5-PATH-ACTUAL
  bundle: P4-P5-WEIGHTED-PATH-ACTUAL
  filter_to_path_coupling: stationary_filter_average
  centered_filter_slow_drift_error: O_L2_epsilon
  path_state: finite_delay_window_in_C_minus_delta_zero
  delay_homogenization: PROVED_FOR_ADDITIVE_FAST_DRIVER
  pure_path_game: PROVED_BY_STRONG_CONCAVE_CONVEX_HAMILTONIAN
  segment_horizontal_shift_generator: INCLUDED
  path_DPP: PROVED
  semilinear_segment_PPDE: PROVED_RELATIVE_TO_TYPED_COMPARISON_PACKET
  BSDE_path_evaluation: PROVED
  actual_weighted_path_chain: NONEMPTY_AND_COMPLETE

closure:
  former_strengthening_blockers: 5
  former_strengthening_blockers_closed: 5
  closed_by_actual_theorem: 5
  closed_by_maximality_or_refutation: 4
  unnamed_arrows: 0
  circular_dependencies: 0
  stronger_claims_hidden_as_assumptions: 0
  external_peer_review: NOT_PERFORMED
  mathematical_proof_certified_externally: false
  formal_credit: 0
```

## Meaning of the five closures

1. **Specular Sinai U3.** The actual nonconjugate radial family has an
   all-order invariant-projector response and an all-order exact-coboundary
   twisted response. The generic noncoboundary all-source theorem remains false
   without an explicit bilateral/current packet; that failure is a maximality
   theorem, not an unnamed gap.
2. **Moving-family BDL.** Full high-frequency BDL bounds are uniformized over
   compact billiard families by a robust witness packet and finite-cover
   argument. Parameter derivatives are proved on graded source channels. A
   single scalar pointwise grazing weight for every deformation is excluded by
   the consecutive-collision ratio obstruction.
3. **Enhanced-WIP rate.** “Optimal” is fixed to a precise rough-path topology.
   The four-branch Bernoulli realization has matching upper and lower exponent
   `1/2-eta`; no topology-free universal exponent is claimed.
4. **Pure Isaacs.** General pure-saddle existence is false. The exact
   compact-action equivalence and strong concave-convex theorem close the
   correct general theory, and an actual four-branch pure game is supplied.
5. **Weighted/path actualization.** A deterministic product extension supplies
   an unbounded hidden state and actual weighted filter. Its stationary filter
   observable is averaged into a noncompact delay diffusion, followed by a
   pure path game, segment DPP, path equation with horizontal shift, and BSDE
   evaluation.

## Normative files

- `SPECULAR_SINAI_RADIAL_U3.md`
- `MOVING_FAMILY_HIGH_FREQUENCY_BDL.md`
- `OPTIMAL_ENHANCED_WIP_RATE.md`
- `PURE_STRATEGY_ISAACS.md`
- `WEIGHTED_NONCOMPACT_PATH_ACTUALIZATION.md`
- `maximal_strengthening_packet_v1.yaml`
- `HOSTILE_STRENGTHENING_AUDIT.md`

These files are internal proof drafts. Structural verification, symbolic
checks, and source hashes do not substitute for external specialist review.
