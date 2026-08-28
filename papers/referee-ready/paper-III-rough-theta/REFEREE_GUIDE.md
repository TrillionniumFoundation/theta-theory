# Referee guide — Paper III

## Central claims

The paper constructs a nonautonomous diffusion and an HJB/theta semigroup from
frozen Doob-selected deterministic dynamics.  It distinguishes a quantitative
block route from a direct martingale-array route and proves a sharp Gaussian
benchmark in a full rough Wasserstein metric.

## Suggested audit order

1. Verify that the Doob selector uses only external frozen data and does not
   depend on the unknown HJB solution.
2. Audit the spectral derivation of the Gordin decomposition, bracket, area
   anomaly, initial-law forgetting, and parameter modulus.
3. Check the first- and second-level coboundary removal in the enhanced WIP.
4. Check Proposition 4.2: qualitative uniform convergence yields only a
   diagonal theorem.
5. For the sharp-rate theorem, audit separately:
   - Brownian first-level bridge scaling;
   - the Chen decomposition and second-level bridge estimate;
   - closedness of the mesh-polygonal subspace;
   - the fractional Poincare lower bound;
   - Kantorovich duality.
6. Verify the accumulated block condition and the exponent window
   `2/(1+delta)<kappa<2`.
7. Audit the predictable-characteristics proof for the slowly varying
   four-branch Bernoulli model.
8. Check the monotonicity/consistency/comparison argument for HJB convergence.
9. Check the short-time proof of non-subadditivity for the explicit nonconvex
   Hamiltonian.

## Imported hypothesis

Paper II supplies smooth frozen physical coefficients and a fixed common
operator realization.  This paper does not use filtering, game values, BSDEs,
or PPDE representations as inputs.

## Permanent scope boundaries

- A qualitative frozen WIP is not a quantitative full-scale theorem.
- The sharp exponent is tied to the declared fractional-Sobolev rough
  Wasserstein metric; it is not metric-free.
- The actual four-branch nonautonomous proof uses direct predictable
  characteristics and does not depend on the Gaussian sharp-rate theorem.
- K3 filtering and games are optional downstream branches, not prerequisites
  for the one-player HJB/theta result.

## Specialist points

The second-level bridge estimate and the lower fractional-Poincare estimate are
particularly suitable for independent rough-path review.  The viscosity section
should be reviewed independently by a PDE/control specialist.
