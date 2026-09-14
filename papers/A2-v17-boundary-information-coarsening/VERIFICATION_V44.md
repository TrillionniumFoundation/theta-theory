# A2 v44 — completed build, publication and verification ledger

September 14, 2026. This ledger supersedes the source-checkpoint ledger, preserved at `history/v44-source-checkpoint/VERIFICATION_V44.md`. It distinguishes mathematical source, generated products and the final navigation-only delivery commit.

## Frozen identities and actual execution

| Object | Identity |
|---|---|
| Addressed v43 report | `6f7de242000a7db2bf473276b8e1792104c7cd42` |
| Reviewed v43 source | `22d9b930a426cdb2c62984a5a3e5875e95e05e79` |
| Exact compiled v44 source | `b229bfa2df2962ea2ebfd0fb2fd11531036d33a6` |
| Compiled source repository tree | `136c1ed35b5fde452cad5ac9dd322272e05ec13d` |
| Successful native/publication Actions run | `34820671440`, attempt `1` |
| Source Actions artifact | `10337978025` |
| Native Actions artifact | `10338197591` |
| First published products commit | `a2edc3505f47c5d15285c6d16d958acd074621ca` |
| Published attestation commit, verified again after push | `fbcf3175f0a13ec3c8508ff16b6deb6d5da2d4d9` |
| Products repository tree at that commit | `71ce503adaa8b6c63f5b40676eaaed67338fb635` |

[Actual workflow run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34820671440) · [Compiled source](https://github.com/TrillionniumFoundation/theta-theory/commit/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6) · [Published products and attestations](https://github.com/TrillionniumFoundation/theta-theory/commit/fbcf3175f0a13ec3c8508ff16b6deb6d5da2d4d9).

Both jobs, `native` and `publish-verified-products`, completed successfully. The first compiled both unabridged native entries from frozen Git objects. The second recovered the successful new artifact and the original v43 artifact, published their complete contents on a new products branch, fetched it, checked every advertised Git blob, committed the attestations, pushed and fetched again, and reverified both deliveries. This is an executed publication check, not inference from a workflow file.

Current review-ready branch: `revision/a2-v44-review-ready-2026-09-14`. Author branch: `revision/a2-v44-nonsymmetric-realization-2026-09-14`. Products branch: `revision/a2-v44-native-products-34820671440-1`. The final delivery navigation is a descendant of the attestation commit; it changes no active TeX or native delivery object. The PDFs are attributed to the compiled source above, not falsely to a later documentation-only commit.

## Native products

[Complete main PDF](../../deliveries/a2-v44/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6/main.pdf) · [Complete companion PDF](../../deliveries/a2-v44/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6/two_collision.pdf) · [Native source archive](../../deliveries/a2-v44/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6/native-source.zip) · [Raw evidence directory](../../deliveries/a2-v44/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6).

| Product | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| `main.pdf` | 228 | 1775792 | `88928386ef8436bb3fd79b7f1ddee3c0d00a620c189833b5d14afc7a0f8b64fe` |
| `two_collision.pdf` | 7 | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Inner `native-source.zip` | — | 1549844 | `1b65df642d26973b9de895ebe9fe411c53300e3615f3d439fd94e749a6c8d879` |

The downloaded native artifact's evidence hashes were checked locally without mismatch. All 97 active-manifest entries (96 main, one companion) match the separately prepared local active source. The companion-produced auxiliary, imported-generated-input record and main recorder agree on its hash and producer source. The hosted final main log has four underfull vertical-box notices, but no unresolved references/citations, missing-character messages or overfull boxes. The separate local build additionally emitted the shell-escape-disabled epstopdf warning. No literally warning-free claim is made.

## Git retention, including the v43 repair

[New v44 attestation](../../deliveries/a2-v44/b229bfa2df2962ea2ebfd0fb2fd11531036d33a6/COMMITTED_OBJECTS_VERIFIED.json) verifies **41 artifact/evidence files**. [Repaired v43 attestation](../../deliveries/a2-v43-repaired/22d9b930a426cdb2c62984a5a3e5875e95e05e79/COMMITTED_OBJECTS_VERIFIED.json) verifies **37 original artifact files**. These counts exclude the newly generated README, copy receipt and attestation themselves. Both attestations identify the first fetched published commit; the succeeding job step also verified the final fetched attestation commit.

The actual Git trees were read through the authenticated connector after publication. The v44 delivery subtree is `af969940cdd519fcfbc3aa10d4a9986fe0bdd631`; the repaired v43 subtree is `05183fd3c1a4cde6465ffce27eccdcfa26f4fc40`. They contain the promised PDF, `.aux`, `.fls`, `.log`, `.out`, `.toc` where generated, and `.fdb_latexmk` blobs, rather than merely listing their names in a filesystem receipt. For example, the new main PDF blob is `716628d0449622b8aff53a9df88301ec6e5137e4`; the repaired old main PDF blob is `bb59766c37b9913a0e187b5deb58789a86d88687`.

The old incorrect receipt remains unchanged in `deliveries/a2-v43/<old-source>`. The repair is a distinct directory retaining the original bytes, not a substituted new compilation. These Git-committed files no longer depend solely on the 90-day Actions artifact lifetime. An attempted text-only connector fetch of a PDF was rejected as binary; PDF bytes were instead obtained through the authenticated artifact download, and committed presence was checked through Git trees. No unsuccessful binary fetch is treated as a successful PDF retrieval.

## Executed preservation and finite diagnostics

The source-preservation check verifies all 95 baseline manifest entries and the declared additive changes. All 212 inherited theorem-style environments remain active. The only new mathematical inputs are the introductory realization overview and Section 17, containing four new theorem-style results. No duplicates, unresolved static references or unresolved citations were found.

The geometry diagnostic covers 108 parameter cases and 436 contact solves. Its maximum contact residual is `3.0878077872387166e-15`, maximum Gram error `1.0032863428932615e-11`, and maximum redundant-cycle error `1.5895418780872947e-12`. Registration receives only complete edge-image centers and support coefficients, not the generating lattice matrix. Ordinary and optimized Python outputs agree. The inherited adaptive, v32 and v38 diagnostics also passed in the hosted source-pinned build.

The retention negative control reproduced exactly 13 omissions under ordinary staging, then verified all 37 files after force-staging. Deleting the working-tree PDF did not affect verification of committed objects. Normal and optimized outputs agree. This negative control was executed locally and again in the successful publication job.

## Local rebuild and visual coverage

Both full entries were independently compiled locally, companion first, with `latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder` and `pdflatex -no-shell-escape -recorder`. Both commands returned zero. After authenticated download, all **235 pages** matched the local build in whitespace-normalized extracted text and in **72-dpi MuPDF raster pixels**. This is page-text and specified-resolution raster parity, not PDF byte identity or an all-resolution renderer certificate.

Readable-resolution visual inspection covered main pages **1, 8, 9, 72, 73, 74, 75, 76 and 77**, including the new introduction, complete new Section 17 and its transition to the inherited next section. The page-77 native rendering was additionally checked with Poppler `pdftoppm` at 110 dpi. All seven unchanged companion pages were inspected in a contact-sheet overview. All main pages were rendered to overview sheets, but no claim is made that every inherited main page received a new readable-resolution visual inspection. No clipping, overlap, broken mathematical glyphs or missing formula material was identified in the inspected material.

The source-checkpoint ledger and all prior failed or superseded checkpoints remain historical records. Compilation, artifact hashes, finite diagnostics, raster parity and targeted visual examination do not certify all mathematical statements or settle the referee's exceptional-significance judgment. The new construction and its proofs are submitted for independent mathematical review.
