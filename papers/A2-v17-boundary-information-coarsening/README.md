# A2 v44 — complete native revision for independent review

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · September 14, 2026

The directory name `A2-v17` is historical. The current author revision is **v44**, on `revision/a2-v44-nonsymmetric-realization-2026-09-14`.

[Complete native article](main.tex) · [Seven-page native companion](two_collision.tex) · [Response to referee](RESPONSE_TO_REFEREE_V44.md) · [Verification, source and products](VERIFICATION_V44.md) · [Preservation and dependencies](PRESERVATION_AND_DEPENDENCIES_V44.md).

## Mathematical revision

The native article retains the relative nonlinear forward law, smooth finite-remainder signed inverse, single-offset amplitude-free density inversion, analytic image determination, intrinsic signature matching, common-frame rank-two reconstruction, all local experiments, observable calibration, physical reconstruction and complete auxiliary proofs.

The added [Section 17](article/23i_nonsymmetric_periodic_realization_v44.tex) supplies the integrated geometric demonstration requested in R43-S1. Theorem 17.1 constructs a nonsymmetric two-obstacle periodic family with four selected channels, disjoint curvature ranges, all-obstacle separation greater than 43/10 and third-obstacle clearance at least 383/200. Proposition 17.2 recovers relative frames from the second and third support harmonics of already recovered curve images. Corollary 17.3 composes eight signed laws and four gaps into full marked-table and lattice determination. Proposition 17.4 proves persistence in an infinite-dimensional analytic neighborhood. An [introductory subsection](article/01e_realization_overview_v44.tex) explains its place in the argument without replacing the earlier introduction.

The construction parameters and harmonic coefficients are not additional observations. Registration stability is stated only after complete curve images are recovered; no effective analytic-continuation rate is inferred. The direct-position benchmark and all preparation costs remain in the manuscript.

## Referee and delivery provenance

The [latest addressed report](../../reviews/a2-v43-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md) is frozen at `6f7de242000a7db2bf473276b8e1792104c7cd42`. It reviews source `22d9b930a426cdb2c62984a5a3e5875e95e05e79`, built in Actions run `34813913830`, and products `edd95683ee57965ff8cd82cee1462a478d06ae39`.

The v43 native main and companion genuinely existed. Its incorrect Git-retention receipt and stale navigation are addressed separately from mathematics. The replacement [retention implementation](tools/retain_native_v44.py) distinguishes artifact-copy hashes, index verification and post-publication committed-object verification. The [execution ledger](VERIFICATION_V44.md) records which of these steps actually ran and identifies the final products.

## Reproduction

From a Git checkout, run `python3 -B papers/A2-v17-boundary-information-coarsening/tools/check_revision_v44.py` and `python3 -B papers/A2-v17-boundary-information-coarsening/tools/check_realization_v44.py`; repeat under `python3 -O -B` and compare JSON. With the installed native TeX toolchain, use `tools/build_submission.py --output-dir <empty-directory-outside-the-paper>`. It freezes committed source, builds the companion before the complete main, checks generated-input provenance and retains raw evidence. Compilation is not a mathematical or all-page visual certificate.

The [unchanged v43 main](history/v43-review-baseline/main.tex) and old navigation entries are preserved. Earlier reports, derivations, A1 and other workstreams remain in the repository.
