# θ-Theory five-paper proof series

This directory is the proof-facing reorganization of the θ-Theory program.  It
is built on the controlling dependency document
`../../THETA_DEPENDENCY_CLOSURE_REPORT_2026-08-28.md` and excludes the
Navier--Stokes program.

The five manuscripts are:

1. `paper-I-cm2-u3/`: bilateral graph-current CM2, finite-DQ, third-source
   totalization, moving-singularity U3, and the maximality/no-go boundary;
2. `paper-II-pressure-diffusion/`: higher pressure response, low-frequency
   suspension resolvents, physical diffusion response, common operator
   realization, coefficient lift, and ellipticity;
3. `paper-III-rough-theta/`: frozen Doob selection, uniform enhanced WIP,
   nonautonomous rough homogenization, HJB convergence, and the
   theta-expectation semigroup;
4. `paper-IV-filter-games/`: filtering, belief collapse, sequential games,
   simultaneous relaxed games, mixed Isaacs limits, and belief/path-state DPP;
5. `paper-V-representations/`: the downstream typed representation hierarchy:
   calibrated linearizations, FBSDEs, controlled/randomized BSDEs, 2BSDE or
   nonlinear martingale-problem branches, PPDEs, and path evaluations.

Each directory contains a manuscript proof draft and a separate blocker
closure ledger.  Process/provenance language belongs only in the ledgers, not
in a future submission-facing extraction.

## Strict status semantics

`CLOSED` means that every implication internal to the stated theorem scope has
an explicit hypothesis, theorem, and proof.  It does not mean that a stronger
system class has been silently verified.  In particular:

- unrestricted universal moving-scatterer CM2 remains refuted;
- the positive CM2/U3 theorem is on an explicit packetized admissible class;
- the v68/v69 open moving-seam family is an actual nonzero witness;
- a nonconjugate specular-Sinai instantiation is a stronger future theorem, not
  an unnamed assumption;
- quantitative full-scale nonautonomous homogenization requires a compatible
  enhanced-WIP modulus; mere qualitative uniform WIP gives only a diagonal
  subsequence unless an additional rate argument is supplied;
- sequential and simultaneous games are permanently distinct;
- FBSDE, controlled BSDE, 2BSDE, and PPDE representations are typed branches,
  not interchangeable conclusions.

## Dependency order

```text
Paper I CM2/U3
  -> Paper II pressure/suspension/diffusion/common-space coefficients
       -> Paper III Doob-selected rough homogenization and theta-HJB
            -> Paper IV filtering and games (optional typed fan-out)
                 -> Paper V downstream representations
```

Paper IV is not needed for the uncontrolled or one-player result of Paper III.
Paper V is never used to prove Papers I--IV.

## Review boundary

These are internal mathematical proof drafts.  They have not received external
specialist review and grant no formal theorem credit.  Historical v83/v164
source bytes are unchanged.
