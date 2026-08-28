# Referee guide — Paper V, revision v4

## Central claims

The paper proves an intrinsic tangent-law theory for the theta-semigroup,
including a converse characterization, and connects it to the finite
deterministic collision recursions before treating Girsanov, BSDE, PPDE, game,
and second-order branches.

## Suggested audit order

1. **Parabolic IFT:** check the Hölder spaces, composition smoothness, terminal
   operator isomorphism, and derivative equation.
2. **Analytic entropic map:** verify the Banach Nemytskii argument and all
   derivative formulas.
3. **Tangent cocycle:** multiply the Radon--Nikodym kernels and verify the
   nonlinear chain rule.
4. **Static characterization:** derive the measure-valued replicator ODE,
   prove uniqueness, and integrate the ray derivative.
5. **Dynamic characterization:** check that the zero-payoff tangent kernels
   form the base Markov semigroup and that the cocycle yields time consistency.
6. **Microscopic convergence:** verify weak convergence under bounded
   exponential tilting and passage of first/second derivatives and finite-time
   kernels.
7. **Tangent PDE:** check the terminal sign and the coefficient
   `b+theta a Du`.
8. **Girsanov:** derive the stochastic exponential, prove true-martingale
   status, identify the Radon--Nikodym density and changed Brownian drift, and
   distinguish the Novikov and bounded-density/BMO routes.
9. **BSDEs:** verify the quadratic driver and the linear tangent martingale
   under the tilted law; confirm that no `Z -> p` inversion occurs.
10. **Path branch:** check the path DPP, functional Itô formula, exponential
    transform, and path-viscosity comparison.
11. **Pure path game:** audit completion of squares and the relation
    `theta=2c/sigma^2`.
12. **2BSDE branch:** check stability under conditioning/pasting and the
    minimality condition.

## High-risk proof locations

- uniqueness of the probability-valued tangent ODE in the characterization;
- uniformity needed for derivative convergence of microscopic tangent laws;
- BMO justification of the density process outside a bounded-gradient window;
- path-viscosity comparison and stability;
- the precise 2BSDE minimality class.

## Permanent scope

The general parabolic derivative theorem is stated in a uniformly parabolic
classical window.  The entropic actual branch is globally analytic on bounded
payoffs.  The 2BSDE theorem applies to the stable volatility-control family and
is not used to represent a nonconvex Isaacs operator.

A report should distinguish the new characterization/microscopic tangent
results from the downstream standard stochastic representation tools.
