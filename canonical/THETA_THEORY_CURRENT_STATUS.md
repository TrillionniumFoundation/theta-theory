# θ-Theory current status — five-paper closure control page

**Date:** 2026-08-28  
**Scope:** θ-Theory only; Navier–Stokes is excluded.  
**Branch:** `theta-five-paper-closure-2026-08-28`  
**Policy:** `LATEST-WINS / FAIL-CLOSED / NO-UNNAMED-ARROWS / NO-REVIVAL-OF-REFUTED-UNIVERSAL-CLAIMS`

## Controlling status

```yaml
UnrestrictedUniversalMovingScattererCM2: REFUTED_EXACTLY
LocalGeometryOnlyUniformCM2: REFUTED
MaximalPacketizedCM2Class: PROVED_IN_DEPENDENCY_CLOSURE_REPORT
ActualScopedNonzeroMovingSeamCM2: PASS_OPEN_FOUR_BRANCH_THREE_SEAM_CLASS
ActualScopedLorentzE2E: PASS_IN_RECURSIVE_V164_SCOPE
ActualUniversalLorentzTheorem: NOT_CLAIMED

PaperI_CM2_U3:
  product_tail: CLOSED
  finite_DQ_l1: CLOSED
  graded_ladder: CLOSED_X5_TO_X1
  actual_U3_witness: OPEN_FOUR_BRANCH_CLASS

PaperII_K1_K15:
  pressure_C3: CLOSED_RELATIVE_TO_PAPER_I
  low_frequency_suspension: CLOSED_WITH_ENTRY_EXIT_OPERATORS
  physical_diffusion_response: CLOSED
  common_operator_realization: CLOSED_BY_SMOOTH_QUADRATIC_ATLAS
  coefficient_and_ellipticity: CLOSED
  actual_four_branch_positive_diffusion: CLOSED

PaperIII_K2_Theta:
  Doob_selection: CLOSED_WITH_NO_FEEDBACK
  enhanced_WIP: CLOSED_WITH_MODULUS_OR_DIRECT_CHARACTERISTICS
  nonautonomous_homogenization: CLOSED
  general_HJB_and_theta: CLOSED_RELATIVE_TO_NAMED_DPP_COMPARISON_PACKET
  actual_four_branch_monotone_DPP: CLOSED
  actual_four_branch_HJB_theta: CLOSED
  actual_full_scale_symbolic_model: PASS
  explicit_nonconvex_non_subadditive_branch: CLOSED

PaperIV_K3:
  filtering: CLOSED_WITH_BAYES_GAP_AND_INITIAL_LAYER
  general_sequential_and_mixed_games: CLOSED_RELATIVE_TO_NAMED_DPP_COMPARISON_PACKET
  actual_four_branch_sequential_limits: CLOSED
  actual_four_branch_mixed_Isaacs: CLOSED
  pure_saddle: EXTRA_TYPED_CERTIFICATE
  belief_and_path_state_branches: CLOSED
  actual_hidden_symbol_model: PASS

PaperV_Representations:
  single_linear_law_obstruction: CLOSED
  calibrated_Feynman_Kac: CLOSED
  FBSDE_control_BSDE_2BSDE_PPDE_typing: CLOSED
  post_calibration_Girsanov: CLOSED
  reverse_use_to_prove_HJB: FORBIDDEN

ActualScopedChainThroughTheta: CLOSED
ActualScopedChainThroughMixedIsaacs: CLOSED
InternalDependencyGaps: CLOSED
UnnamedIntermediateArrows: 0
HostileProofAuditRounds: 3
ExternalPeerReview: NOT_PERFORMED
MathematicalProofCertifiedExternally: false
FormalCredit: 0
```

## Meaning of closure

1. Impossible unrestricted claims are closed by counterexample/maximality and
   are not revived.
2. Positive general theorems are stated on explicit packetized admissible
   classes.
3. A nonzero open moving-seam system verifies the complete finite-order
   Paper-I/II packet.  Its Bernoulli/Doob realization verifies full-scale K2,
   an actual monotone one-player DPP and theta-HJB, exact bounded filtering,
   sequential lower/upper schemes, and a relaxed mixed-Isaacs scheme.
4. Every cross-paper arrow has a named P1--P5 interface; old blanket response
   imports are forbidden.
5. Stronger system-specific theorems not used by the series are outside the
   claim rather than hidden assumptions.

## Correct dependency DAG

```text
Paper I: bilateral graph-current CM2 + finite-DQ + U3
  -> Paper II: pressure / low-frequency suspension / diffusion / common space
       -> Paper III: Doob-selected rough homogenization / HJB / theta
            -> Paper IV (optional typed fan-out): filter / games / Isaacs
                 -> Paper V: typed downstream representations

Paper III HJB/theta
  -----------------------------------------------> Paper V
```

Permanent corrections:

- U3 is not needed for first-order K1, but is needed for the third-order mixed
  pressure derivative used by the general K1.5 lift.
- Qualitative uniform enhanced WIP alone gives a cofinal diagonal result; a
  compatible modulus or direct triangular characteristics are needed for a
  full-scale nonautonomous theorem.
- K3 is not needed for an uncontrolled or one-player HJB.
- Filter contraction alone does not erase the initial belief from values; a
  vanishing slow initial layer is also required.
- Mixed Isaacs equality does not imply a pure saddle.
- FBSDE, controlled BSDE, 2BSDE, nonlinear martingale problem, and PPDE are
  typed downstream branches, not interchangeable conclusions.

## Controlling files

- `papers/theta-program/THETA_DEPENDENCY_CLOSURE_REPORT_2026-08-28.md`
- `papers/theta-program/theta_dependency_packet_v1.yaml`
- `papers/theta-program/five-paper-series/README.md`
- `papers/theta-program/five-paper-series/FIVE_PAPER_CLOSURE_STATUS.md`
- `papers/theta-program/five-paper-series/THEOREM_INTERFACE_MANIFEST.yaml`
- `papers/theta-program/five-paper-series/HOSTILE_PROOF_AUDIT.md`
- five `MANUSCRIPT.md`, five `BLOCKER_CLOSURE.md`, and five `INTERFACE.md`
- Paper-II renewal note, Paper-III actual DPP/comparison appendix, and
  Paper-IV actual game-scheme appendix
- `tools/verify_theta_five_paper_series.py`

The verifier source is structurally separate from mathematical proof.  A full
verifier run against a checked-out branch is required before merge.  The
series has not received external specialist review and grants no external
correctness certificate.

Historical v83/v164 and old three-paper source bytes remain unchanged.
