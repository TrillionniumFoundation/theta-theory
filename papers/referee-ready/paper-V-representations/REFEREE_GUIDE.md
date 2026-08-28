# Referee guide — Paper V

## Central claims

The paper proves a typed representation hierarchy for theta-expectations and
constructs two complete path-dependent actual models.  It also proves that one
payoff-independent classical Markov law cannot represent a genuinely nonlinear
semigroup.

## Suggested audit order

1. Verify the single-law linearity obstruction.
2. Check the generator orientation and the exact residual term in the
   jet-calibrated linear equation.
3. Audit the Feynman--Kac exponential signs and the factor
   `sigma sigma^T=2a`.
4. Check the relation `Z=sigma^T Du`; reject any direct identification of `Z`
   with the HJB gradient.
5. Audit the division between semilinear FBSDE, control/randomized BSDE, game,
   convex 2BSDE, and nonconvex second-order branches.
6. In the entropic path model:
   - verify the deterministic Gaussian-shift prelimit;
   - check the pure saddle and coefficient `c=1/(2mu)-1/(2nu)`;
   - check the Cole--Hopf transform;
   - check the completed-square verification inequalities;
   - check the quadratic BSDE exponential formula;
   - check the cylindrical approximation step for the integral-plus-maximum
     terminal payoff.
7. In the volatility branch:
   - verify convergence of controlled predictable quadratic variations;
   - check stability under concatenation of the law family;
   - audit PPDE comparison hypotheses;
   - check aggregation/minimality in the 2BSDE representation.
8. Verify that every Girsanov use occurs only after a law has been fixed.

## Imported hypothesis

The paper assumes that an upstream DPP and comparison theorem have already
identified the relevant HJB/Isaacs/path value.  It does not prove any upstream
spectral or homogenization result.

## Permanent scope boundaries

- A payoff-calibrated diffusion depends on the solved payoff and is not one law
  for the full nonlinear semigroup.
- A control or game value is not automatically a classical FBSDE.
- A generic nonconvex second-order Isaacs equation is not automatically a
  2BSDE.
- A PPDE is not reduced to a finite-dimensional PDE without a sufficient
  statistic.
- The actual 2BSDE branch is the convex volatility-control model, not the pure
  drift game.

## Specialist review split

The calibration and Markov BSDE sections should be reviewed by a BSDE expert;
the actual path game and PPDE by a functional-Itô/PPDE expert; and the
volatility branch by a second-order BSDE specialist.
