# θ-Theory current status — maximal strengthening closure

**Date:** 2026-08-28  
**Scope:** θ-Theory only; Navier–Stokes is excluded.  
**Branch:** `theta-maximal-strengthening-closure-2026-08-28`  
**Base:** `theta-five-paper-closure-2026-08-28@0abb452732ec9e5a748904ad77800bdcaa00248b`  
**Policy:** `LATEST-WINS / FAIL-CLOSED / ACTUAL-OR-MAXIMALITY / NO-UNNAMED-ARROWS / NO-REVIVAL-OF-REFUTED-UNIVERSAL-CLAIMS`

## Controlling status

```yaml
UnrestrictedUniversalMovingScattererCM2: REFUTED_EXACTLY
LocalGeometryOnlyUniformCM2: REFUTED
MaximalPacketizedCM2Class: PROVED
ActualScopedNonzeroMovingSeamCM2: PASS_OPEN_FOUR_BRANCH_THREE_SEAM_CLASS

PaperI_CM2_U3:
  product_tail: CLOSED
  finite_DQ_l1: CLOSED
  graded_ladder: CLOSED_X5_TO_X1
  actual_open_four_branch_U3: CLOSED
  actual_nonconjugate_specular_radial_invariant_U_infinity: CLOSED
  actual_nonconjugate_specular_radial_coboundary_twisted_U_infinity: CLOSED
  generic_geometry_only_noncoboundary_specular_U3: REFUTED

PaperII_K1_K15_BDL:
  pressure_C3: CLOSED
  low_frequency_suspension: CLOSED_WITH_ENTRY_EXIT_OPERATORS
  physical_diffusion_response: CLOSED
  common_operator_realization: CLOSED
  coefficient_and_ellipticity: CLOSED
  compact_family_high_frequency_BDL: CLOSED_RELATIVE_TO_STRICT_WITNESS_PACKET
  graded_high_frequency_parameter_derivatives: CLOSED
  actual_radial_all_frequency_channel: CLOSED
  universal_single_scalar_grazing_weight_domain: REFUTED

PaperIII_K2_Theta:
  Doob_selection: CLOSED_WITH_NO_FEEDBACK
  enhanced_WIP: CLOSED
  nonautonomous_homogenization: CLOSED
  optimal_rate_topology: STEP_TWO_FRACTIONAL_SOBOLEV_W_ETA_P
  optimal_rate_test_distance: STEIN_DIRICHLET_SIGMA_ETA_P
  optimal_rate_safe_range: P_GT_6_AND_ONE_THIRD_LT_ETA_MINUS_ONE_OVER_P_AND_ETA_LT_ONE_HALF
  optimal_rate_upper: N_POWER_MINUS_ONE_HALF_PLUS_ETA
  optimal_rate_lower: N_POWER_MINUS_ONE_HALF_PLUS_ETA
  full_Lipschitz_KR_exact_rate: NOT_CLAIMED
  topology_or_test_class_free_optimal_rate: NOT_A_WELL_TYPED_CLAIM
  actual_four_branch_HJB_theta: CLOSED
  nonconvex_non_subadditive_branch: CLOSED

PaperIV_K3:
  bounded_filter: CLOSED
  weighted_noncompact_filter_actual: CLOSED
  sequential_values: CLOSED
  mixed_Isaacs: CLOSED
  unrestricted_general_pure_saddle: REFUTED_BY_MATCHING_PENNIES
  pure_saddle_iff_pure_Isaacs: CLOSED
  strong_concave_convex_unique_saddle: CLOSED
  actual_four_branch_pure_Isaacs: CLOSED
  belief_HJB: CLOSED

PaperV_Representations:
  single_linear_law_obstruction: CLOSED
  typed_representations: CLOSED
  actual_noncompact_delay_path_state: CLOSED
  actual_entire_window_payoff: CLOSED
  actual_segment_DPP_and_path_equation: CLOSED
  actual_BSDE_path_evaluation: CLOSED
  reverse_use_to_prove_HJB: FORBIDDEN

ActualScopedChainThroughTheta: CLOSED
ActualScopedChainThroughMixedIsaacs: CLOSED
ActualScopedChainThroughPureIsaacs: CLOSED
ActualWeightedNoncompactFilter: CLOSED
ActualNoncompactPathEvaluation: CLOSED
FormerOutsideTheoremStrengtheningItems: 5
FormerOutsideTheoremStrengtheningItemsClosed: 5
InternalDependencyGaps: CLOSED
UnnamedIntermediateArrows: 0
ExternalPeerReview: NOT_PERFORMED
MathematicalProofCertifiedExternally: false
FormalCredit: 0
```

## Meaning of closure

Closure has three admissible forms:

1. **actual theorem:** a concrete deterministic system satisfies every field of
   the theorem packet;
2. **packet theorem:** the implication is proved from explicit hypotheses and
   no hypothesis is hidden under the word `general`;
3. **maximality/refutation:** a stronger unrestricted statement is false, and
   the counterexample plus strongest valid replacement theorem are proved.

Accordingly, matching pennies closes the unrestricted pure-saddle request by
refutation and identifies pure Isaacs equality as the exact criterion.  The
split-surjective moving-face defect closes geometry-only generic specular U3 by
maximality, while the radial invariant/coboundary channels provide actual
positive U-infinity.  The grazing-weight-ratio obstruction excludes one
ungraded universal BDL domain, while the compact witness-bundle theorem supplies
the full valid high-frequency result.

The optimal rough rate is also fail-closed: the exact `N^{-(1/2-eta)}` order is
proved in the regular Stein--Dirichlet test distance actually controlled by the
quantitative argument, with a smooth midpoint-bridge lower test in the same
class.  It is not relabelled as an exact full Lipschitz--KR rate.

## Correct strengthened DAG

```text
Paper I bilateral CM2/U3
  + actual nonconjugate radial specular invariant/coboundary U-infinity
    -> Paper II pressure/diffusion/common space
       + compact moving-family high-frequency BDL bundle
         -> Paper III Doob-selected rough homogenization
            + topology-and-test-class-optimal four-branch enhanced-WIP rate
              -> HJB / theta-expectation
                -> Paper IV filtering and games
                   + actual weighted noncompact filter
                   + pure-Isaacs exact classification and actual saddle
                     -> Paper V typed representations
                        + actual noncompact delay-path DPP/PPDE/BSDE.
```

## Permanent boundaries

- The radial specular theorem is source-specific; generic centered
  noncoboundary pressure U3 still requires the bilateral third-source packet.
- Compact-family BDL uniformity requires strict local witnesses before the
  compact finite-cover argument.
- “Optimal WIP rate” always names both its path topology and its quantitative
  test class; the full Lipschitz--KR exact rate is outside the current export.
- Mixed minimax never implies a pure saddle without pure Isaacs or an
  equivalent structural certificate.
- The fast weighted filter is averaged before the delay-path limit; the segment
  PPDE includes the horizontal shift generator and does not retain an untyped
  belief coordinate.

## Controlling files

- `papers/theta-program/maximal-strengthening/MAXIMAL_STRENGTHENING_STATUS.md`
- `papers/theta-program/maximal-strengthening/maximal_strengthening_packet_v1.yaml`
- the five normative strengthening proof files in that directory;
- `papers/theta-program/maximal-strengthening/HOSTILE_STRENGTHENING_AUDIT.md`
- `papers/theta-program/five-paper-series/FIVE_PAPER_CLOSURE_STATUS.md`
- `papers/theta-program/five-paper-series/THEOREM_INTERFACE_MANIFEST.yaml`
- five updated interfaces and blocker ledgers;
- five per-paper strengthening appendices.

Historical v83/v164 and the earlier five-paper source bytes remain available as
provenance.  The present branch controls only the latest θ-Theory
interpretation.  It has not received external specialist review and grants no
external correctness certificate.
