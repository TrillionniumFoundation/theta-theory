# Paper II theorem interface

## Imports

Required general inputs:

- `P1-CM2`
- `P1-FDQ`
- `P1-U3`
- `P1-RWORDS`

Optional actual specular channel:

- `P1-SINAI-RADIAL-U3`

The imported response acts on the Paper-I graded ladder. No blanket
`main_response_package` is used. The radial import is restricted to the
invariant-projector and exact-coboundary channels declared by Paper I.

## Exports

- `P2-COMMON`: smooth quadratic finite-atlas common operator realization.
- `P2-PRESSURE3`: `C^3` twisted pressure and reduced spectral data.
- `P2-SUSP0`: low-frequency suspension resolvent response.
- `P2-PHYS`: physical drift, covariance, diffusion, and parameter response.
- `P2-COEFF`: `C^{3,alpha}` `(x,p)` coefficient fields.
- `P2-ELL`: uniform ellipticity under explicit noncoboundary and rank margins.
- `P2-ACTUAL-4B`: actual positive-diffusion four-branch package.
- `P2-BDL-HF-FAMILY`: uniform full high-frequency resolvent for a compact
  moving billiard family carrying `BDL-FAMILY-WITNESS-v1`, together with
  ordered-composition parameter derivatives on certified graded source
  channels; normative proof:
  `../../maximal-strengthening/MOVING_FAMILY_HIGH_FREQUENCY_BDL.md`.

## Scope of the high-frequency export

`P2-BDL-HF-FAMILY` contains:

1. strict local BDL witness openness;
2. compact finite-cover uniformization;
3. a fixed quadratic-atlas operator realization;
4. a uniform high-frequency resolvent strip;
5. parameter derivatives only for declared graded generator letters;
6. an actual all-frequency nonconjugate radial exact-coboundary channel.

## Non-exports

- one universal scalar grazing weight making every deformation letter bounded
  on one ungraded domain;
- an HJB theorem;
- a Doob-selected rough WIP.

The first item is closed by the consecutive-collision grazing-weight-ratio
no-go theorem, not left as an unnamed blocker.
