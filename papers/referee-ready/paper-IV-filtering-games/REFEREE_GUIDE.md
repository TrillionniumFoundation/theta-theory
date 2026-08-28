# Referee guide — Paper IV

## Central claims

The paper proves strategy-tree-uniform filter stability and separates the
sequential, mixed simultaneous, and pure Isaacs limits.  It supplies actual
bounded and weighted noncompact deterministic models.

## Suggested audit order

1. Check the Bayes expansion constant `2 g_+/g_-` under the paper's total
   variation convention.
2. Verify the observation-gap product `C_B rho^{r_*}<1` and the pathwise
   strategy-tree iteration.
3. Audit the geometric convolution estimate under slow/control perturbations.
4. Check that the initial-layer theorem, not merely a finite geometric sum,
   removes dependence on the initial belief.
5. In the weighted branch, audit separately the Lyapunov moment ball,
   prediction contraction, Bayes regularity, and PDE comparison fields.
6. Verify that sequential order is retained in the two consistency limits.
7. Check the relaxed mixed minimax theorem and that no pure conclusion is
   inferred from it.
8. Audit the proof that compact pure Isaacs equality is equivalent to a pure
   saddle.
9. Check measurable selection of the saddle correspondence.
10. For the noncompact theorem, verify strong monotonicity and cancellation of
    all mixed Hessian terms.
11. Audit the actual four-branch monotone schemes and the one-step
    prior-forgetting identity.
12. Audit the Gaussian weighted filter's exact transition and posterior moment
    estimates.

## Imported hypothesis

Paper III supplies control-uniform homogenized characteristics.  No stochastic
representation theorem is used to prove a game or filtering limit.

## Permanent scope boundaries

- Filter contraction is not the same as initial-belief value collapse.
- Lyapunov control is not the same as weighted HJB comparison.
- Sequential lower and upper values need not coincide.
- Mixed Isaacs equality is not a pure saddle theorem.
- A belief-state problem is not projected to a finite-dimensional or path-free
  equation without a sufficient-statistic proof.

## Specialist review split

A filtering specialist should focus on Sections 2--5 and 11.  A stochastic
control/game specialist should focus on Sections 6--10.  A viscosity specialist
should independently audit all comparison-dependent convergence statements.
