# Research plan: computational falsification of the billiard-to-HJB chain

**Scope.** No external dataset is mounted or required. All observations will be deterministic simulations of finite-horizon periodic dispersing billiards and the manuscript's compact finite-response port. Raw configurations, trajectories, collision logs, and derived arrays will be versioned with hashes.

## Claims and tests

| ID | Falsifiable claim | Test and metric | Pass criterion |
|---|---|---|---|
| C1 | Centered billiard correlations are summable and yield a positive-semidefinite Green--Kubo tensor. | Estimate correlation tails, integrated autocorrelation, and both correlation-sum and block-displacement estimates of $D$; report minimum eigenvalue and relative estimator gap. | Tail fits exponential better than power-law by AIC; eigenvalue $\ge-3$ bootstrap SE; estimator gap $<10\%$. |
| C2 | Effective coefficients respond smoothly to regular table/port perturbations. | Compare centered finite differences of $D,H$ at steps $h, h/2, h/4$ with tangent/Ulam-resolvent derivatives. | Derivative discrepancy decreases monotonically and final relative error $<10\%$. |
| C3 | The prelimit deterministic value converges to the derived HJB solution. | For $\varepsilon\in\{1/4,1/8,1/16,1/32\}$, compare on a common grid using $L^\infty$, relative $L^2$, and observed log--log slope. | Both errors decrease for the last three levels and finest relative $L^2<5\%$. |
| C4 | An admissible odd--even port produces nonconvexity and non-subadditivity. | Estimate the smallest eigenvalue of $D_p^2H$ and defect $\Delta=H(p+q)-H(p)-H(q)$ with bootstrap CIs. | Some preregistered point has upper CI $<0$ for the eigenvalue and another has lower CI $>0$ for $\Delta$. |

## Implementation and data

- Build `experiments/` modules for event-driven specular collisions, grazing-safe root finding, port deformation, trajectory/checkpoint I/O, Ulam transfer matrices, Green--Kubo/block estimators, monotone finite-difference HJB, prelimit characteristics, and bootstrap/report generation.
- Use three geometries (symmetric, asymmetric, near-grazing stress case), three regular port amplitudes, $10^7$ post-burn-in collisions per configuration, and fixed seeds **1103, 2207, 3301, 4409, 5501** (seeds select initial conditions/bootstrap only). Record energy drift, collision residual, horizon bounds, grazing-strip index, and effective sample size.
- Unit tests: specular energy conservation, reversibility away from singularities, centering, Ulam mass conservation, monotone-scheme convergence on constant-coefficient heat and manufactured HJB solutions.

## Baselines and ablations

- Baselines: frozen-table/no-port billiard; time-shuffled observables; block-displacement versus Green--Kubo $D$; linear heat equation and HJB with $H=0$.
- Ablate moving-boundary response, full-gradient work terms, second corrector, and high homogeneity strips. Report coefficient and convergence-error changes; no ablation may replace the primary model.

## Stopping and decision rule

Stop after all five seeds reach the collision budget and the finest two discretizations, or earlier for numerical invalidity (energy drift $>10^{-8}$, collision residual $>10^{-10}$, effective sample size $<500$, or failed mass conservation $>10^{-10}$). Any failed pass criterion falsifies its computational claim; report failures without retuning thresholds. One preregistered rerun is allowed only after a documented implementation bug.
