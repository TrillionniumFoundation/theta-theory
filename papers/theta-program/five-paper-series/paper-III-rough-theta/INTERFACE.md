# Paper III theorem interface

## Imports

Required coefficient inputs:

- `P2-COMMON`
- `P2-PRESSURE3`
- `P2-SUSP0`
- `P2-PHYS`
- `P2-COEFF`
- `P2-ELL`

Optional all-frequency flow input:

- `P2-BDL-HF-FAMILY`

The cotangent/tilt signal is external at the microscopic-selection stage. The
unknown HJB solution is not an input to the imported frozen operators.

## Exports

- `P3-DOOB`: frozen normalized selected kernels.
- `P3-RWIP`: enhanced WIP with a compatible modulus or direct
  triangular-array characteristics.
- `P3-RWIP-OPTIMAL-WETA-P`: matching upper and lower rate
  `N^{-(1/2-eta)}` for the actual four-branch enriched walk in the declared
  step-two fractional-Sobolev rough-path KR metric, with
  `1/p<eta<1/2`; normative proof:
  `../../maximal-strengthening/OPTIMAL_ENHANCED_WIP_RATE.md`.
- `P3-NAHOM`: nonautonomous homogenized characteristics.
- `P3-HJB`: uncontrolled or one-player viscosity limit under the named DPP and
  comparison packet.
- `P3-THETA`: time-consistent theta-expectation semigroup.
- `P3-NONCONVEX`: explicit nonconvex/non-subadditive branch.
- `P3-ACTUAL-4B`: actual full-scale Bernoulli four-branch realization through
  its monotone DPP, viscosity comparison, HJB limit, and theta-semigroup; see
  `TECHNICAL_APPENDIX_DPP_COMPARISON.md`.

## Optimal-rate scope

The word `optimal` in `P3-RWIP-OPTIMAL-WETA-P` is topology-specific. The
matching lower bound comes from unresolved Brownian bridge defects of any
mesh-affine path. Endpoint smooth-test distance retains the separate
`N^{-1/2}` exponent. No topology-free universal rate is exported.

The optimal rate gives the explicit full-scale block window

\[
\frac{2}{1+(1/2-\eta)}<\kappa<2,
\qquad m_\epsilon=\epsilon^{-\kappa}.
\]

## Non-exports

- filter stability;
- a two-player Isaacs theorem;
- a stochastic representation theorem;
- a quantitative rate from qualitative WIP alone;
- a topology-free “best” enhanced-WIP exponent.
