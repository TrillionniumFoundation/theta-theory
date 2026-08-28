# Paper I theorem interface

## Imports

None.

## Exports

- `P1-CM2`: graded product-tail CM2 on the explicit bilateral packet.
- `P1-FDQ`: finite-DQ convergence in the complete two-time `l1` topology.
- `P1-U3`: continuous first three source/operator derivatives on the declared
  graded ladder.
- `P1-RWORDS`: well-typed third-order reduced-resolvent words.
- `P1-ACTUAL-4B`: open four-branch, three-moving-seam actual witness.
- `P1-SINAI-RADIAL-U3`: actual nonconjugate finite-horizon specular radial
  family with all-order differentiated-invariance projector response and
  all-order exact-coboundary twisted response; normative proof:
  `../../maximal-strengthening/SPECULAR_SINAI_RADIAL_U3.md`.

## Scope of the new specular export

`P1-SINAI-RADIAL-U3` is an actual moving-singularity complete-assembly result.
It may be used for invariant-projector and exact-coboundary channels.  A
noncoboundary pressure/diffusion channel must still import `P1-CM2`, `P1-FDQ`,
`P1-U3`, and `P1-RWORDS` with its own third-source atom packet.

## Non-exports

- unrestricted universal moving-scatterer CM2;
- geometry-only generic noncoboundary specular U3;
- an untyped regularity-loss budget.

The generic geometry-only specular claim is closed by the split-surjective
face-defect maximality theorem rather than left as an unnamed blocker.
