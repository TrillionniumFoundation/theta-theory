# θ-Theory five-paper proof series

This directory is the proof-facing reorganization of the θ-Theory program.  It
is built on the controlling dependency document
`../../THETA_DEPENDENCY_CLOSURE_REPORT_2026-08-28.md` and excludes the
Navier--Stokes program.

## Series map

1. `paper-I-cm2-u3/`: bilateral graph-current CM2, finite-DQ, graded
   third-source totalization, moving-singularity U3, an actual open
   four-branch/three-seam witness, and the maximality/no-go boundary;
2. `paper-II-pressure-diffusion/`: higher pressure response, low-frequency
   suspension resolvents, physical diffusion response, smooth common operator
   realization, coefficient lift, and ellipticity;
3. `paper-III-rough-theta/`: frozen Doob selection, uniform enhanced WIP,
   nonautonomous rough homogenization, HJB convergence, and the
   theta-expectation semigroup;
4. `paper-IV-filter-games/`: filtering, initial-layer belief collapse,
   sequential games, simultaneous relaxed games, mixed Isaacs limits, and
   belief/path-state DPP;
5. `paper-V-representations/`: downstream typed representations: calibrated
   Feynman--Kac laws, FBSDEs, controlled/randomized BSDEs, convex 2BSDE versus
   nonconvex game/nonlinear-MP branches, PPDEs, and path evaluations.

Every paper directory contains:

- `MANUSCRIPT.md`: internal proof draft;
- `BLOCKER_CLOSURE.md`: explicit blocker ledger and scope boundary;
- `INTERFACE.md`: exact named imports, exports, and non-exports.

Normative technical files:

- Paper II: `TECHNICAL_NOTE_RENEWAL.md`, with distinct suspension entry and
  exit operators;
- Paper III: `TECHNICAL_APPENDIX_DPP_COMPARISON.md`, proving the actual
  four-branch monotone DPP, consistency, comparison, HJB convergence, and
  theta-semigroup;
- Paper IV: `TECHNICAL_APPENDIX_GAME_SCHEME.md`, proving the actual lower/upper
  sequential schemes and relaxed mixed-Isaacs scheme.

## Actual scoped end-to-end witness

The single scoped witness used throughout the series is deliberately explicit:

```text
open four-branch / three-moving-seam deterministic family
  -> graded product-CM2 and U3
  -> twisted pressure, low-frequency suspension, positive diffusion
  -> Bernoulli/Doob full-scale martingale characteristics
  -> actual monotone one-player HJB and theta-expectation
  -> exact bounded filtering
  -> actual lower/upper sequential and relaxed mixed-Isaacs limits
  -> typed downstream representations under their stated regularity windows
```

This is not advertised as an unrestricted universal moving-scatterer theorem or
as a nonconjugate specular-Sinai theorem.

## Control and audit files

- `FIVE_PAPER_CLOSURE_STATUS.md`: controlling series status;
- `THEOREM_INTERFACE_MANIFEST.yaml`: machine-readable P1--P5 dependency graph;
- `HOSTILE_PROOF_AUDIT.md`: three-round hostile audit and repaired findings;
- `FIVE_PAPER_VERIFICATION_RECEIPT.json`: structural and execution boundary;
- repository-root `tools/verify_theta_five_paper_series.py`: fail-closed
  structural verifier.

Process/provenance language belongs in the ledgers and audit files, not in a
future submission-facing extraction.

## Strict status semantics

`CLOSED` means that every implication internal to the stated theorem scope has
an explicit hypothesis, theorem, and proof.  It does not mean that a stronger
system class has been silently verified.  In particular:

- unrestricted universal moving-scatterer CM2 remains refuted;
- the positive CM2/U3 theorem is on an explicit packetized admissible class;
- a nonconjugate specular-Sinai instantiation is a stronger theorem outside the
  current claim, not an unnamed assumption;
- full-scale nonautonomous homogenization requires a compatible enhanced-WIP
  modulus or a direct triangular-characteristics theorem; qualitative uniform
  WIP alone gives a cofinal diagonal result;
- filter contraction alone does not erase the initial belief from slow values;
  a vanishing slow initial layer is also required;
- sequential and simultaneous games are permanently distinct;
- mixed Isaacs equality does not imply a pure saddle;
- weighted noncompact, fully path-dependent, and branch-specific stochastic
  representation results retain their explicit theorem packets;
- FBSDE, controlled BSDE, 2BSDE, nonlinear martingale problem, and PPDE are
  typed branches, not interchangeable conclusions.

## Dependency order

```text
Paper I CM2/U3
  -> Paper II pressure/suspension/diffusion/common-space coefficients
       -> Paper III Doob-selected rough homogenization and theta-HJB
            -> Paper IV filtering and games (optional typed fan-out)
                 -> Paper V downstream representations

Paper III theta-HJB
  -----------------------------------------------> Paper V
```

Paper IV is not needed for the uncontrolled or one-player result of Paper III.
Paper V is never used to prove Papers I--IV.

## Verification and review boundary

The structural verifier is separate from mathematical proof.  A full verifier
run against a checked-out branch is required before merge.  These are internal
mathematical proof drafts; they have not received external specialist review,
do not certify mathematical correctness externally, and grant no formal
theorem credit.  Historical v83/v164 and old three-paper source bytes are
unchanged.
