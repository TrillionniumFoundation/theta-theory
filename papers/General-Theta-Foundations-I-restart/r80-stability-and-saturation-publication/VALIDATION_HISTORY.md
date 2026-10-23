# Execution history and status boundaries

The final strict `PASS` belongs to source commit `c0ac246181c2f4214e3e830952386adffb7d82df` and the exact source tree in `BUILD_RECEIPT.json`. No source edit occurred during or after that successful run.

The archive also preserves earlier development attempts as their actual statuses:

1. Draft 01 failed the final warning gate on an overlong display in the two-location section. That display was wrapped. This was an uncommitted development build, not the current source verification.
2. Draft 02 failed native LaTeX because a multiple-alignment prior-constant display used `split`. It was changed to `aligned` without changing formulas. Its failure remains recorded.
3. Draft 03 completed the three native documents and generated the actual 267-entry index. Diagnostics were intentionally skipped in explicit draft mode; its receipt is `DRAFT_COMPILE_COMPLETE`, not a committed-source `PASS`.
4. The first strict launch stopped at Git identity because the newly created remote commit object had not yet been imported into the local checkout. GitHub JSON normalizes dates to UTC; reconstructing the exact unsigned raw commit required its original `+0800` timezone representation. The recovered raw payload was accepted only after its Git hash matched exactly. No mathematical source edit was involved. That failed launch is retained separately.
5. The subsequent complete strict run verified the actual local and remote source identity, every preservation invariant, the complete inherited history and fresh delta, all 32 ordinary/optimized diagnostic pairs, three native passes for each PDF, all paired citations/references and current theorem locators. Its receipt is the final `PASS` supplied here.

The ordinary and optimized counts are not doubled when reporting the number of finite checks. Exact finite arithmetic, floating diagnostics, written universal proofs, native execution, visual inspection, hosted CI, human assessment and editorial decisions are distinct evidence categories. Source-specific GitHub Actions readback observed zero runs; the historical R65 successful run remains evidence only for its original SHA.
