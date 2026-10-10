# A2-DYN revision 67 — revised manuscript and referee response

Date: 10 October 2026.

## Read the revision

The complete manuscript is [main.tex](papers/A2-DYN-v67-referee-response/main.tex). Read the [point-by-point response](papers/A2-DYN-v67-referee-response/RESPONSE_TO_REFEREE.md), [short proof route](papers/A2-DYN-v67-referee-response/JOURNAL_ROUTE.md), [proof ledger](papers/A2-DYN-v67-referee-response/PROOF_LEDGER.md), and [specialist audit map](papers/A2-DYN-v67-referee-response/SPECIALIST_AUDIT_MAP.md).

Paper: Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*. The original family, section, exact actual-return labels, arithmetic kernel and unrestricted pointwise target are unchanged.

## Frozen provenance

- Reviewed author commit: `e96761c0b12dbc46c187f4aeb4ee8d537863dec5`.
- Complete reviewed paper tree: `fdf737e94888a540c05d86c458d77b500895e713`.
- Controlling external review commit: `31eae1cab4ac138d0d9c892cb76c63286cb73307`.
- Controlling report: `reviews/a2-dyn-v66-external-top4-review-2026-10-10/REFEREE_REPORT.md`, blob `e3e06c75e0b6a73b613c944223423c0dc03b3854`.
- Initial source-preserving remote checkpoint: `bc7ee926738df71c09abdf81f01a50d55c3fe451`.
- Final revision-67 complete paper tree: `266c432351a184e230b7e4df4f970c9d9f87208c`.
- Ordinary source payload tree, excluding the root manifest: `406dfc9ba6935c18e0128c3e387c6c61b5fee957`.

The paired branches are `revision/a2-dyn-v67-referee-response-2026-10-10` and `revision/a2-dyn-v67-referee-copy-2026-10-10`. They are intended to share the same final source commit, without changing any old manuscript or review branch.

## Mathematical revision

New modules 143--145 prove relative exact-label angular stability on explicit finite-jet strata, ordered zero-width physical trace concentration on each such stratum, and an ordered essential-height bound for the corresponding original-source caustic collars. The proof uses positive absorption before the collision limit; it does not assume concentration of the larger reversible trace. A positive weighted condition-number tail quantifies the remaining passage to all seam charts.

The full physical tail bound, complete first-incidence height and positive complementary clearance height remain unproved. The revision does not claim the unrestricted pointwise endpoint, unrestricted same-roof consequences, independent human verification or journal acceptance from these new component results.

## Preservation and reproducibility

All 142 inherited core modules, all 194 inherited Python files, all six inherited appendix files and the bibliography are byte-identical. Every one of the 1,895 inherited mathematical labels remains compiled; the revision has 145 core modules and 1,928 labels. The preceding abstract and introduction are compiled verbatim in a marked appendix, and the full old main and replaced metadata are separately archived.

Run `bash papers/A2-DYN-v67-referee-response/build.sh`. The qualification workflow is `.github/workflows/a2-dyn-v67-qualification.yml`. It freezes the exact checkout, reviewed paper tree and review blob, verifies preservation and finite diagnostics in normal and optimized Python, compiles the full manuscript with shell escape disabled, and renders the actual new theorem pages. Its artifact includes the PDF, logs, receipts and exact source archive. Read the actual GitHub run conclusions; this index does not predeclare a successful remote execution or a continuum proof certificate.
