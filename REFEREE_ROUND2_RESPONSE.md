# Response to the second independent referee round

## Review object

This revision responds to both `REFEREE_REPORT.md` and
`REFEREE_REPORT_GPT56_PRO.md` in each of the eleven manuscript folders on
`main@ae2fdc16bf1ad4a6b58cca6020a7b8b61236e2ad`.

The revision policy is positive and fail-closed:

- every statement-level counterexample is repaired by replacing the faulty
  formula with a stronger correctly typed theorem;
- model-specific analytic packets are expanded into named lemmas and proofs;
- no reviewed claim is closed by deleting the paper, converting it to a
  no-go statement, or silently relabelling it conditional;
- platform changes, preparation changes, physical-clock changes, and
  optimization changes are explicitly typed;
- external rereview of the exact revision commit remains required.

## Root blockers and repairs

1. **B1 fixed-saddle counterexample.** Replaced by a source-dependent
   constrained pressure obtained through Fourier--Laplace coefficient
   extraction and a reoptimized saddle. The referee's time-zero source test is
   computed exactly and now gives `t a`.

2. **A2 missing vector/roof spectral and local-limit theorem.** Added a finite
   atlas of anisotropic spaces, uniform Lasota--Yorke and multiplier estimates,
   joint complex spectral perturbation, periodic-orbit aperiodicity, a
   lattice--nonlattice local limit theorem, and the ratio-conditioning
   corollary.

3. **A3 missing singularity and random-speed contraction.** Added a finitely
   primitive marked Young code, exponential singularity-frequency estimates,
   exponentially good path approximations, collision/physical Palm
   contraction, finite-rate support, admissible information projection, and a
   closed linear coboundary quotient.

4. **B2 missing actual-collision LDP.** Fixed the incoming orientation,
   proved exact microscopic balance, introduced actual-collision marked
   trajectory polymers, established a factorial source-uniform majorant,
   exponential compact containment, and a constructive local lower bound.

5. **B3 gauge and fluctuation defects.** Replaced the incomplete collision
   invariant quotient by the full adjoint representation gauge, fixed the
   functional spaces with Orlicz duality, included constrained initial
   covariance, and retained the large-deviation-speed factor in pressure
   Hessians.

6. **B4 missing density semigroup.** Defined a weighted density state and
   cylinder core, proved nonlinear-generator convergence, compact containment,
   Hamilton--Jacobi comparison, semigroup convergence, and the
   source-dependent microcanonical diagonal theorem.

7. **C1 divergent block error and changed game.** Added a Poisson-corrector
   telescoping decomposition that makes the accumulated error vanish and
   separated one-time preparation, reward-only control, and adaptive law
   control into three distinct positive theorems.

8. **C2 platform mixing and formal tangents.** Introduced a typed coproduct of
   platform rates, a strict-topology cotangent dual, spectral/cluster pressure
   differentiability, complete rigidity hypotheses, joint likelihood-ratio
   convergence, and a commuting memory diagram.

9. **D1 normalization error.** Corrected
   `D^2 Q_epsilon = mu_epsilon Cov`, formulated the fluctuation covariance on
   the square-root-speed scale, and added a joint mod-Gaussian
   likelihood-ratio theorem.

10. **A1 mechanical and path typing.** Added a common symbolic path space,
    exact pullback typing, a deterministic volume-preserving collision
    suspension, a calibrated work-field theorem, and explicit summable
    resolvent response words.

11. **A4 tautological history closure.** Added a Polish history Feller
    semigroup, a resolvent-defined Mori--Zwanzig memory kernel that does not
    assume generation of `QLQ`, exponential memory decay, a constructed
    nonlinear generator core, and a short-memory diffusion tangent.

## Verification boundary

The revision workflow inserts every addendum into the controlling `main.tex`,
updates the paper-level README and referee guide, verifies theorem/proof
counts, compiles all eleven papers, and commits the materialized revision to
the branch. Passing that workflow is a source/build check, not external
mathematical certification.
