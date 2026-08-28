# Paper II theorem interface

## Imports

- `P1-CM2`
- `P1-FDQ`
- `P1-U3`
- `P1-RWORDS`

The imported response acts on the Paper-I graded ladder.  No blanket
`main_response_package` is used.

## Exports

- `P2-COMMON`: smooth quadratic finite-atlas common operator realization.
- `P2-PRESSURE3`: `C^3` twisted pressure and reduced spectral data.
- `P2-SUSP0`: low-frequency suspension resolvent response.
- `P2-PHYS`: physical drift, covariance, diffusion, and parameter response.
- `P2-COEFF`: `C^{3,alpha}` `(x,p)` coefficient fields.
- `P2-ELL`: uniform ellipticity under explicit noncoboundary and rank margins.
- `P2-ACTUAL-4B`: actual positive-diffusion four-branch package.

## Non-exports

- a full high-frequency moving-family flow graph domain;
- an HJB theorem;
- a Doob-selected rough WIP.
