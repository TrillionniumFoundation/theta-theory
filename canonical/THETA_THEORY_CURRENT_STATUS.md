# θ-Theory current status — dependency-closure control page

**Date:** 2026-08-28  
**Scope:** θ-Theory only; Navier–Stokes is excluded.  
**Branch:** `theta-dependency-closure-2026-08-28`  
**Policy:** `LATEST-WINS / FAIL-CLOSED / NO-UNNAMED-ARROWS / NO-REVIVAL-OF-REFUTED-UNIVERSAL-CLAIMS`

## Controlling status

```yaml
UnrestrictedUniversalMovingScattererCM2: REFUTED_EXACTLY
LocalGeometryOnlyUniformCM2: REFUTED
MaximalPacketizedCM2Class: PROVED_IN_DEPENDENCY_CLOSURE_REPORT
ActualScopedNonzeroMovingSeamCM2: PASS_V68_V69
ActualScopedLorentzE2E: PASS_IN_RECURSIVE_V164_SCOPE
ActualUniversalLorentzTheorem: NOT_CLAIMED
CM2ToU3Compiler: PROVED_RELATIVE_TO_EXPLICIT_THIRD_SOURCE_ATOM_PACKET
U3ToK1: PROVED
K1ToK15: PROVED
K15ToK2: PROVED_RELATIVE_TO_UNIFORM_MARTINGALE_ROUGH_PACKET
K2ToK3: PROVED_AS_TYPED_FILTER_SEQUENTIAL_SIMULTANEOUS_BRANCHES
K2K3ToHJBTheta: PROVED_RELATIVE_TO_TYPED_COMPARISON
HJBThetaToRepresentations: PROVED_AS_DOWNSTREAM_TYPED_BRANCHES
InternalDependencyGaps: CLOSED
UnnamedIntermediateArrows: 0
ExternalPeerReview: NOT_PERFORMED
FormalCredit: 0
```

“Closed” has the following strict meaning:

1. impossible unrestricted claims are closed by counterexample/maximality and are not revived;
2. the positive theorem is stated on an explicit nonempty packetized admissible class;
3. every downstream arrow has named inputs, outputs and a theorem interface;
4. stronger system-specific instantiations not covered by the packet are outside the theorem, rather than hidden assumptions or unnamed gaps.

## Correct dependency DAG

```text
CM2 bilateral graph-current/product tail
  -> moving-singularity U3
       -> K1 C3 pressure / low-frequency suspension resolvent / physical diffusion response
            -> K1.5 common operator realization / (x,p) coefficient and elliptic fields
                 -> K2 Doob selection / enhanced rough WIP / nonautonomous homogenization
                      -> uncontrolled or one-player HJB
                      -> K3 filtering
                      -> K3 sequential lower/upper games
                      -> K3 simultaneous relaxed Isaacs game
                           -> HJB / Isaacs / belief-state HJB or path-dependent PPDE
                                -> theta-expectation
                                     -> typed FBSDE / controlled BSDE / 2BSDE / PPDE / path evaluation
```

Permanent dependency corrections:

- U3 is not needed for first-order K1, but is needed for the third-order pressure response used by the general K1.5 lift.
- K3 is not needed for an uncontrolled or one-player HJB.
- filtering, sequential games and simultaneous games are parallel typed branches.
- FBSDE, controlled BSDE, 2BSDE and PPDE are parallel downstream representations, not a single implication chain.

## Controlling new files

1. `papers/theta-program/THETA_DEPENDENCY_CLOSURE_REPORT_2026-08-28.md`
2. `papers/theta-program/theta_dependency_packet_v1.yaml`
3. `papers/theta-program/THETA_TOP_FOUR_PAPER_ARCHITECTURE_2026-08-28.md`

Historical v83 and v164 source bytes remain unchanged. This page controls only the new θ-Theory dependency interpretation on the named branch; it grants no external review or journal acceptance status.
