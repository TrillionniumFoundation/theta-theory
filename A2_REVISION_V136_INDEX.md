# A2 v136 — uniform support and functorial reconstruction

Branch: `revision/a2-v136-functorial-support-reconstruction-2026-09-23`.

Controlling report: `reviews/a2-v135-independent-harsh-top4-r2-2026-09-23/REFEREE_REPORT.md`, commit `9fb3a5b9b27d4f6c6df2f3e557b4fc709c3a546d`.
Additional independent report: `reviews/a2-v135-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, commit `9f246bef692ee715851c4b200041c5cfe76da7d9`.
Reviewed manuscript: `003fb13458c8ed11e2973963493a662f31c700c0`.

## Referee reading order

All revised manuscript files are in `papers/A2-v17-boundary-information-coarsening/article/v136/`.

1. [Principal article](papers/A2-v17-boundary-information-coarsening/article/v136/geometry.pdf): the complete smooth-locus inverse proof, the new arbitrary-dimensional contraction/support theorems, and both intrinsic descent repairs.
2. [Response to both v135 reports](papers/A2-v17-boundary-information-coarsening/article/v136/RESPONSE_TO_REFEREES_V135.md), [literature audit](papers/A2-v17-boundary-information-coarsening/article/v136/LITERATURE_AUDIT_V136.md), and [issue matrix](papers/A2-v17-boundary-information-coarsening/article/v136/ISSUE_MATRIX.json).
3. [Technical supplement](papers/A2-v17-boundary-information-coarsening/article/v136/supplement.pdf), preserving the primary-boundary, specialization, and ambient-pencil theory.
4. [Complete archival manuscript](papers/A2-v17-boundary-information-coarsening/article/v136/complete.pdf), [source manifest](papers/A2-v17-boundary-information-coarsening/article/v136/PROVENANCE_MANIFEST.json), and [executed build receipt](papers/A2-v17-boundary-information-coarsening/article/v136/evidence/BUILD_RECEIPT.json).

The principal article, not the combined archive, is the primary reading object. Every PDF has complete editable LaTeX sources. Both reviewed reports are copied with immutable provenance into `v136/review_inputs/` by the assembler.

## Mathematical revision

The determinant-twisted map `j_n: det(V) tensor Sym^n(V) -> exterior^n Sym^2(V)` now has an all-ranks contraction-kernel theorem for every `n >= 2`, including the exceptional scalar kernel in even dimensions. Its exact support formula proves uniqueness of the component-pencil point for every `n >= 4` whenever the Jacobian has at least three essential variables, compatibly with arbitrary base change. This is an extension of the algebraic inverse mechanism; intrinsic abstract failure-scheme readout remains asserted in dimension four only.

The principal geometric proof now constructs a regular, then constant, projective coordinate change from the oriented relative Segre bundle. The residual coefficient space is recovered by an intrinsic graded ideal quotient, with the determinant line and its twists explicit. The theorem for **every basepoint-free smooth-Jacobian web** is retained without an extra genericity restriction.

All 254 predecessor mathematical labels remain compiled. Modified predecessor sources are also preserved verbatim in the history directory. Eleven exact scripts include 27 finite all-ranks certificates in dimensions 2 through 7; finite computations are not presented as formal certificates of the structural proofs.

## Documentary boundary

The direct Landsberg–Ottaviani and Sheridan exterior/skew-flattening formulations are compared at their actual statements. Ballico 1993 was inspected at the publisher's first page, but its complete article and the requested six-axis theorem-level comparison remain **documentary-open**. Neither historical nonanticipation nor acceptance by a journal is claimed.

## Reproduction and publication

Run `python revisions/a2-v136/unpack.py`, `python revisions/a2-v136/assemble.py`, then `bash papers/A2-v17-boundary-information-coarsening/article/v136/build.sh` from the repository root. The checksummed transport expands into readable overlays. The branch-specific workflow verifies immutable inputs, executes all eleven scripts, compiles three PDFs, checks preservation, and publishes only on this revision branch.

Local preflight: principal article 30 pages; supplement 66 pages; complete archive 92 pages. All build checks passed; no overfull boxes or out-of-page text blocks were detected. This local preflight is distinct from the remote run recorded below.

<!-- REMOTE_BUILD_START -->
Remote build completed successfully: [GitHub Actions run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/35834394351).

Source commit: `6827ef5933a66fc920a9cb39737e4597e5561f19`.

PDF pages: geometry 30, supplement 66, complete 92. All eleven exact-script executions, source-preservation checks, reference checks, and PDF-bounds checks passed. Full details and hashes are in the source-bound build receipt.
<!-- REMOTE_BUILD_END -->
