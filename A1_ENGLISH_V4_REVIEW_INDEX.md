# A1 English revision 4.0 — next referee entrance

[Open the complete revision package](papers/A1-english-v4/README.md) · [Point-by-point response](papers/A1-english-v4/RESPONSE_TO_REFEREE.md) · [Main LaTeX](papers/A1-english-v4/main.tex) · [Proof ledger](papers/A1-english-v4/PROOF_LEDGER.md)

**Qian Qi · September 6, 2026**

**A1: Realizable Mechanical Experiments, Path Selection, and Response**  
*Selection rank, solved costly readout gates, and a quantitative positive-polynomial hierarchy for controlled detectors*

## Review target and ancestry

The new branch is `revision/a1-english-v4-structural-robust-control-2026-09-06`. It descends directly from the latest v3 referee commit `574f2315a136d8b401644d8a3eeeb93c87887010`. The controlling report is preserved at [its original path](reviews/a1-english-v3-2026-09-05/REFEREE_REPORT.md); the [reviewed v3 source](papers/A1-english-v3/) and its historical foundations remain unchanged.

The submitted principal source tree is **`7dcf0be42486cb7ad7a0e9de7d2ae3d6395ed72a`**. All 24 files in that subtree, including the source manifest, were verified by recomputing the canonical Git tree locally and matching the independently fetched remote tree SHA. The source compiled and tested locally is therefore byte-identical to this uploaded principal tree.

## Mathematical revision

The central new material is the normalized polynomial-channel coefficient-rank criterion and `n(r-1)` product dimension; the physical passive-`n` / selectable-`3n` contrast and explicit attainable coefficient radius; the solved positive-cost last-cartridge arc gate and four-candidate mode optimization; and a physically realizable positive-polynomial approximation hierarchy with complete adaptive-policy regret and explicit degree/lookup bounds. The smooth-readout and intrinsic-body-dimension formulations are corrected. Earlier bias, interface-trace and preparation repairs remain explicit. Referee-derived endpoint and model-error arguments are attributed to that report.

## Actual validation and reproduction

The new suite passed **17/17 local diagnostics**. A separate exact rational interval certificate establishes the strict costly-gate advantage over all report-blind gates. Three no-shell-escape LaTeX passes produced a **25-page** principal PDF with no undefined references/citations, missing characters or overfull boxes in the final log. Render inspection and the source/PDF hashes are recorded under [validation](papers/A1-english-v4/validation/).

This branch contains ordinary source, response, proof/dependency maps, executable checks and local execution receipts. Rebuild the PDF from the package directory with `python build_and_verify.py`. A local PDF was supplied with the conversation delivery; a GitHub-hosted PDF binary and a successful GitHub Actions run are **not** claimed. The previous author/referee test suites were not rerun or counted as these 17 tests.

Finite tests and successful compilation are not formal verification or an independent referee acceptance. The new main text is self-contained and exposes its general proofs for renewed assessment. No merge into main, deletion of historical material, or modification of an existing review branch is part of this publication.
