# A2-DYN revision 74

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas** — Qian Qi.

The manuscript remains about the original exact-displacement, collision-count and roof-time law for actual returns. Its section, normalization, full physical source and arithmetic transition kernel are unchanged.

## Reading order

`main.tex` is the journal-form article: an explicit physical integration family, level-matched short-excursion inequalities, the original endpoint budget, and same-roof normalization. `supplement.tex` compiles all 163 inherited core modules, all 12 appendices and the inherited bibliography. `provenance/` preserves the previous masters and overwritten metadata. Nothing in the historical mathematics is deleted to obtain the shorter article.

`RESPONSE_TO_REFEREE.md` answers both v73 reports. `PROOF_LEDGER.md` distinguishes proved deterministic/fixed-count results from the still-needed collision-uniform dynamical estimate. `SOURCE_MANIFEST.json` is the sole active claim-status authority; the three active status projections are checked against it during qualification. Other retained historical input maps are provenance for their named interfaces, not competing publication-status documents.

## New mathematics

Modules 164–167 give the algebraic half-angle and full physical graph, a same-level component bound sharper than the paired Jordan minimum, a sharp integrated coefficient 1/8, a length-tail identity, an ordered scalar-error comparison, and the precise downstream implication. The length-tail power estimate is a sufficient hypothesis, not a claimed Lorentz estimate. The full pointwise raw local limit theorem is not marked proved.

## Frozen sources

The author baseline is `39575228f055862103edbebdd984bd6764fa0ad9`, paper tree `995790396ccb81e24a97949b7d0143b222ad4b20`. The controlling rereview is `e31a74560d86082da1c2f2ef55c513343cfd41a0`, report blob `28d7999c60fc0083f99ffcb8550a932057af5b8f`. The earlier corrected v73 review at `246d5e723648d51f20dcfd4632bbaf8f34aedeb4`, blob `d4115fea5cbebf1ea9788c1da7300da70736e810`, is also addressed and preserved in provenance.

The response and referee-copy refs are listed in the manifest and must resolve to the same final author SHA. The exact qualifying SHA is recorded at runtime, avoiding a self-referential versioned commit field.

## Build

Run `bash build.sh` in an exact Git checkout. The build is read-only with respect to tracked sources, uses no TeX shell escape, compiles the supplement first, imports only mathematical cross-reference labels, then compiles the journal. Source preservation, rational fixtures, six inherited checks, stabilized references, all-167-module recorder coverage and PDF page geometry are checked. Generated PDFs and evidence are uploaded by the v74 qualification workflow.

For a materialized, hash-verified baseline artifact outside a complete Git checkout, use `bash build.sh --local`. This mode is forbidden in CI and does not claim an exact remote checkout. See `VALIDATION.md` and `LOCAL_FULL_BUILD_RECORD.md` for the evidence boundary.
