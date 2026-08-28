# Referee guide — Paper III, revision v4

## Central claims

The paper proves a full-sequence rough homogenization theorem and constructs a
theta-semigroup from the exact finite collision recursion of the same
nonconjugate moving system used upstream.

## Suggested audit order

1. **Exact innovations:** verify conditional uniformity for a predictable
   parameter and the Doob-selected width realization.
2. **Geometric lift:** check the one-half diagonal, symmetric Chen identity,
   moment tightness, and identification of any antisymmetric compensator.
3. **Endogenous recursion:** verify adaptedness of `A_k=Theta(X_k)` and
   convergence of the predictable bracket to the state-dependent integral.
4. **Full-sequence versus block route:** check that the actual proof uses
   predictable characteristics and that the block theorem requires the stated
   accumulated error condition.
5. **Sharp rate:** check both Brownian-bridge levels and the distance-to-
   polygonal-subspace lower bound in the declared fractional-Sobolev rough
   metric.
6. **Microscopic DPP:** derive the finite branch log-sum-exp operator directly
   from the deterministic collision innovations.
7. **Consistency:** verify centering, covariance, logarithmic cumulant, and the
   uniform third-moment remainder.
8. **HJB convergence:** check monotonicity, stability, half-relaxed limits,
   Cole--Hopf comparison, and the terminal sign.
9. **Controlled branch:** check uniformity in controls and dynamic
   concatenation.
10. **Theta-independence:** verify the directional conditional exponential
    identity and its iteration.

## High-risk proof locations

- exact conditional independence when the parameter is slow-state dependent;
- tightness and identification of the step-two martingale lift;
- full-sequence martingale-problem uniqueness;
- local uniform consistency of the state-dependent collision recursion;
- the claimed analytic lower bound in the sharp rough rate.

## Permanent scope

The actual collision theorem is full-sequence and nonautonomous.  The separate
block theorem explicitly needs a quantitative frozen rate.  The paper does not
infer pointwise viscosity inequalities from a transfer-operator pairing.

A report should distinguish the martingale/rough theorem, the deterministic
actualization, the HJB scheme, and the theta-independence structure.
