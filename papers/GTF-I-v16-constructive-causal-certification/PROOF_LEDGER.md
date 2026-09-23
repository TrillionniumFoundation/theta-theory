# Proof ledger — v16

Stable labels locate proofs in both views. This is a proof map, not independent correctness certification.

| Label / source | Exact assumptions | Conclusion / proof mechanism |
|---|---|---|
| `thm:v16-dual`, nonlinear-testing.tex | Finite rational marked instruments; fixed private, hidden or visible finite signature; full finite tests with empty event; polynomial row parameterization | Monotone endogenous power-testing dual; uniform gap; complete strict positive polynomial certificates without convexification |
| `lem:v16-bernstein` | Rational polynomial on a finite cube | Exact coefficient identity and explicit O(1/n) degree-elevation error via replacement/no-replacement coupling |
| `cor:v16-algorithm` | Same finite fixed-signature setting; rational strict levels | Dovetailed lower identity certificates and executable rational upper tables converge; no polynomial complexity claim |
| `prop:v16-gap` | Two singleton-source report times; width one; correlated binary target; singleton mark/control | Exact private and visible error sqrt(2)-1; hidden two-selector error zero; constant mixed tests fail |
| `thm:v16-collective`, collective-hard-spheres.tex | Equal-mass hard spheres on square torus; full equilibrium; Gaussian velocities; global reversal interventions | Nonconserved collision-domain collective observable; every generator power; exact positive Gram residual; k+1 distinct mean functions at time k |
| `thm:v16-taylor` | Fixed horizon; positive Gaussian noise; L2-bounded preparation; actual initial mark | Explicit Taylor bound and square-root mean-function-count feedback bound; computable Gram and specified marked cylinder integration |
| `thm:v16-exactphysical` | Singleton initial reports; source independent noise; actual initial sign mark; target cos-angle Gaussian report; equilibrium | Exact all-budget marked deficiency, matching test and stateless witness; heat-equation sign argument and absolutely convergent series |
| `cor:v16-numerical` | N=2, side 10, Delta=1/2, sigma=1 | Exact rational interval around 0.205809122888; nonzero residual 2 pi^2/25; explicit Taylor marked error <3e-11 |
| `thm:v16-main`, physical-testing.tex | Fixed finite signature; computable finite rational stateless marked presentations with vanishing errors | Polynomial lower / executable upper certificates of original physical deficiency at original budget; terminating interval procedure |
| `thm:v16-exponential` | Same marked transcript; TV bound; bounded payoff; positive logarithmic scale | Sharp logarithmic transfer, common-policy optimal-value transfer, and effective exponential accuracy schedule |

## Dependency structure

`thm:v16-dual` uses the retained finite intrinsic-deficiency parametrization, plus the fully proved power-mean and Bernstein lemmas. It does not use a false convex private minimax. `prop:v16-gap` demonstrates the missing convex test separation; its finite rational checker certifies 2/5, while its analytic proof gives the exact sqrt(2)-1 value.

`thm:v16-collective` uses classical a.e. hard-sphere flow existence and explicit momentum conservation. `thm:v16-taylor` supplies norm and integration operations for this concrete class. `thm:v16-main` consumes these operations, the retained v15 quantization and marked-prefix rationalization, the retained same-budget comparison, and the new polynomial lower certificate. `thm:v16-exponential` uses the same marked law comparison before policy optimization.

## Retained and unresolved material

All v15 canonical mathematical sections are imported unchanged. The complete development retains every predecessor label and body. The compact/nonfinite, endogenous-task, regenerative, operator and historical results are not counted as newly proved in v16.

No arbitrary nonlinear kinetic action, particle-uniform hierarchy corrector, generic efficient collision solver, fixed-degree exact equality algorithm, or exhaustive priority result is claimed. The original Norberg and Paull–Unger proof-level comparison remains unverified. A new report on the latest-named v15-r2 branch was unavailable at the recorded checks.
