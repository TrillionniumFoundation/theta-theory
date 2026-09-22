# Historical derivations used in v22

## Version anchors

The controlling source is the v21 review branch at `36910a7c6fd08e5ad2e8e10db7c2d8c71c463de8`, not an earlier v17–v20 report. The examined manuscript is `papers/A1-english-v21/` at `7c44bdccc91667c583b5d5cbcff3f8d9160a57d6`. Its published workflow artifact was retrieved, unpacked, and matched against the repository's main-source and manifest Git blobs. All 748 manifest source hashes were checked. This establishes identity, not a new audit of every archived derivation.

## Derivations consulted and their mathematical uses

- `core/02_experiments.tex` and `core/03_transversality.tex`: actual command realizability, evidence-normalized histories, future test spaces, mixed-moment positivity, the binomial product tangent, and raw remaining-moment updates. They identify exactly where E21.1's interval, extremal exponent and sumset definitions are needed. Their theorem and proof text is retained unchanged.
- `core/06b_collision_geometry.tex`, its generated flags/consequences, and `sections/collision_transfer_application.tex`: the distinction between all-history geometry, complete acquired flags and causal updates; these retain the monomial main proof. E21.2 changes only the two consequence citations after generated source reconstruction.
- `sections/causal_transfer.tex`: the fixed-horizon geometric-to-causal implication, including independent coding randomness, reachable representatives, actual integer budgets and the accumulated error recurrence. The new theorem verifies these hypotheses in a second class; it does not rename them as new assumptions.
- `sections/affine_geometry.tex`: exact projective coordinates, the physical covariance invariant, acquired density and the integer-budget ellipsoid law. Its one-step identity is generalized to all acquired likelihood products using a uniformly bounded coefficient multiplication rule.
- `sections/positive_history.tex`: the distinction between a local history section and unconditional acquired mass. The new proof integrates an open set of complementary command coordinates and includes the report-word probability explicitly.
- `sections/structural_classification.tex`: command-polynomial whole-image geometry and the difference between a fixed-rank exponent and a profile uniform through rank loss. The new product coordinates provide the uniform ellipsoidal scales missing from a rank count alone.
- `sections/exact_kernels.tex`, `sections/kernel_feasibility.tex` and the latest report's corresponding audit: exact realization on a constrained full-support slice remains distinct from containment, forced kernels, and a global causal law. The repaired criterion is retained without modification; no claim that it proves the new covariance geometry is made.

The earlier v19–v21 historical maps, v17 inverse source anchor and prior preservation chains remain available. This revision does not claim to have independently re-proved every archived paper in the eleven-paper program.

## Preservation

The original v21 directory, review files and previous revision directories are unchanged. The v22 tree copies every manifest-listed inherited source. Replaced front matter and build scripts are archived verbatim under `history/v21-editorial/`. Generated TeX is reconstructed from a temporary copy of the pinned v21/v20 source chain. All 122 inherited statement blocks survive byte-for-byte; only the two explicitly registered proof citations change. All other inherited proof blocks and all old labels survive.

The only repository additions are the new revision material, its branch-scoped materialization/validation workflow and its final v22 output directory. Main, branch protection, permissions, prior workflows and review branches are not edited.
