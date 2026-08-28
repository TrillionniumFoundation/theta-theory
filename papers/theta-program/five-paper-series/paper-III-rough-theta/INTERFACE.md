# Paper III theorem interface

## Imports

- `P2-COMMON`
- `P2-PRESSURE3`
- `P2-SUSP0`
- `P2-PHYS`
- `P2-COEFF`
- `P2-ELL`

The cotangent/tilt signal is external at the microscopic-selection stage.  The
unknown HJB solution is not an input to the imported frozen operators.

## Exports

- `P3-DOOB`: frozen normalized selected kernels.
- `P3-RWIP`: enhanced WIP with a compatible modulus or direct
  triangular-array characteristics.
- `P3-NAHOM`: nonautonomous homogenized characteristics.
- `P3-HJB`: uncontrolled or one-player viscosity limit.
- `P3-THETA`: time-consistent theta-expectation semigroup.
- `P3-NONCONVEX`: explicit nonconvex/non-subadditive branch.
- `P3-ACTUAL-4B`: actual full-scale Bernoulli four-branch realization.

## Non-exports

- filter stability;
- a two-player Isaacs theorem;
- a stochastic representation theorem;
- full-scale homogenization from qualitative WIP alone.
