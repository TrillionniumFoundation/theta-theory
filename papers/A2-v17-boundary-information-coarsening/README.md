# A2 v45 — complete native revision for independent review

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · September 14, 2026

[Complete main PDF — 235 pages](../../deliveries/a2-v45/2f064b86b4e071d24ad671f4dc652d7de32a56a4/main.pdf) · [Complete companion — 7 pages](../../deliveries/a2-v45/2f064b86b4e071d24ad671f4dc652d7de32a56a4/two_collision.pdf) · [Full native TeX](main.tex) · [Frozen native source ZIP](../../deliveries/a2-v45/2f064b86b4e071d24ad671f4dc652d7de32a56a4/native-source.zip) · [Response to the v44 report](RESPONSE_TO_REFEREE_V45.md) · [Completed verification](VERIFICATION_V45.md) · [Preservation and dependencies](PRESERVATION_AND_DEPENDENCIES_V45.md).

## Review target and executed delivery

The current revision is **v45**, on `revision/a2-v45-review-ready-2026-09-14`. The directory name `A2-v17` is historical. Actual compiled source: `2f064b86b4e071d24ad671f4dc652d7de32a56a4`, author branch `revision/a2-v45-generic-finite-channel-rigidity-2026-09-14`. Successful native/publication run: `34829418911`, attempt 1. Products and fetched-object attestation: `e10c054655c452b2d3b5edf49e439ab2154772fe`, products branch `revision/a2-v45-native-products-34829418911-1`. Final navigation descends from that commit and does not alter the TeX or native products.

The delivery retains 39 actual artifact/evidence files in Git, not only in temporary Actions attachments. The [attestation](../../deliveries/a2-v45/2f064b86b4e071d24ad671f4dc652d7de32a56a4/COMMITTED_OBJECTS_VERIFIED.json) identifies the fetched products commit and individual Git blob/SHA-256 identities. The full article and companion compiled from frozen source, with no unresolved references, missing glyphs or overfull boxes. The hosted main has six underfull vertical-box notices. All 242 pages match the separate local build in extracted text and 72-dpi raster pixels; actual readable-resolution visual scope is recorded in the ledger.

## Mathematical revision

Introductory Theorem 1.3 and the complete new [Section 18](article/23j_generic_finite_channel_rigidity_v45.tex), pages 78–85, address the breadth reservation in the latest report. Theorem 18.3 proves that every positively separated periodic strictly convex table admits N+1 clear selected channels for N obstacle orbits, using obstruction descent, a spanning tree and two independent deck-cycle gains. Proposition 18.6 proves open dense obstacle asymmetry in the relative support topology. Theorem 18.7 then determines the full analytic periodic table and its Euclidean lattice from the N+1 onsets and 2N+2 same-type signed limiting endpoint laws at one known positive offset. Proposition 18.8 gives explicit arbitrary-N recovered-image registration and displacement-cochain reconstruction.

The selected graph need not be a specular multi-channel orbit; tangent third obstacles are excluded by the descent proof. The N+1 count is minimal for the connected two-cycle mechanism, not for arbitrary inverse sensors. Marked channel selection is not unmarked discovery. No inter-channel registration, supplied curvatures, support coefficients or lattice metric enter the intrinsic data. Image-stage stability is not promoted to an effective law-to-complete-boundary rate. Corollary 18.9 retains the original charged pilot, fixed design and uniform regularity assumptions for compact-family physical reconstruction.

All 216 inherited theorem-style environments and 22 remarks remain active, as do the v44 nonsymmetric realization, every prior proof module, all three mathematical parts, the direct-position benchmark and the complete companion. Ten theorem-style environments are added. The exact old main, active manifest and old navigation are in `history/v44-review-baseline/`; the pre-delivery v45 checkpoint is in `history/v45-source-checkpoint/`.

## Referee scope and reproduction

The addressed [v44 report](../../reviews/a2-v44-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md) is frozen at `c984b5a5f0dee0e3a9c78264ff7b5136272fec72`. Its remaining objection was significance, not a new fatal defect established in the inspected core. The response offers a broader theorem, not a promise of acceptance. Independent mathematical and editorial assessment remains necessary.

Run `tools/check_revision_v45.py` and `tools/check_skeleton_v45.py` normally and under optimized Python; compare their JSON outputs. Run `tools/build_submission.py --output-dir <empty-directory-outside-paper>` from a committed checkout with the native toolchain installed. The [completed ledger](VERIFICATION_V45.md) supplies exact provenance, hashes, diagnostics, limitations and visual coverage. A1, all historical derivations, reports and previous delivery directories remain unchanged.
