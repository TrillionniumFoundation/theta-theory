# A2 v44 — complete native revision for independent review

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · September 14, 2026

[Complete main PDF — 228 pages](../../deliveries/a2-v44/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6/main.pdf) · [Complete companion PDF — 7 pages](../../deliveries/a2-v44/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6/two_collision.pdf) · [Complete TeX article](main.tex) · [Companion source](two_collision.tex) · [Response to referee](RESPONSE_TO_REFEREE_V44.md) · [Executed verification and full provenance](VERIFICATION_V44.md) · [Preservation and dependencies](PRESERVATION_AND_DEPENDENCIES_V44.md).

## Current review target and executed delivery

The directory name `A2-v17` is historical. The current revision is **v44**, on `revision/a2-v44-review-ready-2026-09-14`; the author branch is `revision/a2-v44-nonsymmetric-realization-2026-09-14`, and the products branch is `revision/a2-v44-native-products-34820671440-1`.

The **compiled source** is `b229bfa2df2962ea2ebfd0fb2fd11531036d33a6`. Actions run **34820671440**, attempt 1, completed both native compilation and post-publication verification successfully. The frozen products/attestation commit is `fbcf3175f0a13ec3c8508ff16b6deb6d5da2d4d9`. Subsequent delivery navigation does not change the TeX or PDFs. The native main is 228 pages and the companion seven; both PDFs and their raw evidence are in Git, not only in expiring Actions artifacts.

The [new v44 attestation](../../deliveries/a2-v44/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6/COMMITTED_OBJECTS_VERIFIED.json) verifies 41 artifact/evidence files. The [v43 repair attestation](../../deliveries/a2-v43-repaired/22d9b930a426cdb2c62984a5a3e5875e95e05e79/COMMITTED_OBJECTS_VERIFIED.json) verifies all 37 original artifact files, including the 13 previously omitted ignored products. Verification reads fetched committed Git blobs rather than trusting the working tree. The original incorrect receipt remains unchanged as historical evidence.

## Mathematical revision

The native article retains the relative nonlinear forward law, smooth finite-remainder signed inverse, single-offset amplitude-free density inversion, analytic image determination, intrinsic signature matching, common-frame rank-two reconstruction, all local experiments, observable calibration, physical reconstruction and complete auxiliary proofs.

The added [Section 17](article/23i_nonsymmetric_periodic_realization_v44.tex) supplies the integrated geometric demonstration requested in R43-S1. Theorem 17.1 constructs a nonsymmetric two-obstacle periodic family with four selected channels, disjoint curvature ranges, all-obstacle separation greater than 43/10 and third-obstacle clearance at least 383/200. Proposition 17.2 recovers relative frames from the second and third support harmonics of already recovered curve images. Corollary 17.3 composes eight signed laws and four gaps into full marked-table and lattice determination. Proposition 17.4 proves persistence in an infinite-dimensional analytic neighborhood. An [introductory subsection](article/01e_realization_overview_v44.tex) explains its place in the argument without replacing the earlier introduction.

The construction parameters and harmonic coefficients are not additional observations. Registration stability is stated only after complete curve images are recovered; no effective analytic-continuation rate is inferred. The direct-position benchmark and all preparation costs remain in the manuscript. All 212 inherited theorem-style environments remain active and four are added.

## Referee and verification scope

The [addressed v43 report](../../reviews/a2-v43-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md) is frozen at `6f7de242000a7db2bf473276b8e1792104c7cd42`. It reviews source `22d9b930a426cdb2c62984a5a3e5875e95e05e79`, built in Actions run `34813913830`, and products `edd95683ee57965ff8cd82cee1462a478d06ae39`.

The current [execution ledger](VERIFICATION_V44.md) records hosted and local builds, 97 matched active TeX inputs, ordinary/optimized finite diagnostics, the negative retention control, native product hashes and actual post-push verification. Main pages 1, 8, 9 and 72–77 received readable-resolution visual examination; all seven companion pages received a contact-sheet overview. All 235 pages match the separate local build in normalized extracted text and 72-dpi raster pixels. This is not an all-page mathematical or readable-resolution visual certificate. The hosted main has four underfull vertical-box notices and no unresolved references, missing glyphs or overfull boxes.

## Reproduction

From a Git checkout, run `python3 -B papers/A2-v17-boundary-information-coarsening/tools/check_revision_v44.py` and `python3 -B papers/A2-v17-boundary-information-coarsening/tools/check_realization_v44.py`; repeat under `python3 -O -B` and compare JSON. With the installed native TeX toolchain, use `tools/build_submission.py --output-dir <empty-directory-outside-the-paper>`. It freezes committed source, builds the companion before the complete main, checks generated-input provenance and retains raw evidence. For the exact published PDF provenance, check out the compiled source commit above; later navigation-only commits are not falsely described as that build's source.

The [unchanged v43 main](history/v43-review-baseline/main.tex), old navigation entries and [v44 source-checkpoint ledger](history/v44-source-checkpoint/VERIFICATION_V44.md) are preserved. Earlier reports, derivations, A1 and other programme workstreams remain in the repository.
