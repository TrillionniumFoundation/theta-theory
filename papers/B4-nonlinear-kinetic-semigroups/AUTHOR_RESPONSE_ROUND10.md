# Author Response — Round Ten

**Referee report:** `REFEREE_REPORT_ROUND9_GPT56_PRO.md`  
**Registered controlling source:** `revision/round10-referee-final/B4_DYNAMIC_ACTION_GRAPH_CORE_COMPARISON.tex`  
**Policy:** positive reconstruction; no headline theorem is replaced by a no-go statement, paper deletion, or silent scope downgrade.

## Blocker-to-proof map

| Referee blocker | Positive reconstruction | Controlling labels |
|---|---|---|
| Law and observable semigroups conflated | Separate microscopic flow, Koopman observables, dual push-forward laws, ensemble log-Laplace values, and the limiting semigroup. | `prop:r10-b4-tower` |
| State resolvent applied to observables | Use the observable Koopman resolvent and its Hille--Yosida graph identity. | `thm:r10-b4-core` |
| Order-j propagator did not close | Solve one terminal equation on the full triangular product hierarchy and prove normal graph summability. | `lem:r10-b4-corrector` |
| Microscopic nonlinear generator ill-typed | State convergence for corrected ensemble pressure derivatives, not for a deterministic law generator. | `thm:r10-b4-hamiltonian` |
| Initial preparation double-counted | The transition action is dynamic only; preparation appears once at the initial boundary. | `thm:r10-b4-action` |
| Comparison penalty either noncoercive or leaves source core | Use a coercive Tataru distance with fixed slope cutoff, send the diagonal scale first and source cutoff second. | `thm:r10-b4-comparison` |
| Truncation limit formal | Use entropy coercivity, exact balance repair, local uniform semigroup convergence, and viscosity stability. | `thm:r10-b4-main` |

## Verification boundary

The response identifies the exact proof locations and the regression mechanism used by the repository verifier.  Compilation and internal hostile checks are reproducibility gates, not substitutes for independent external mathematical review.
