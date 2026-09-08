# A1 English v19 — complete referee revision

**Attainable information geometry in positive experiments**, Qian Qi.

Controlling report: `reviews/a1-english-v18-independent-2026-09-07/REFEREE_REPORT.md` at `e5fff530c95a4f3aa1163a2087838ff2795f052b`.
Reviewed submission: `be8effe038608bef255fa97318a9ee3b4434af2d`.
Revision branch: `revision/a1-english-v19-rectangular-and-degeneration-2026-09-07`.

The entry point is `main.tex`; the compiled manuscript is `main.pdf`.
This is the complete English manuscript, not an addendum or a replacement of the collision results. All 99 v18 proof blocks, 102 theorem/lemma/proposition/corollary statements, and their labels remain in the compiled text with identical bytes. Ten additional results have complete proofs. The historical v18 source snapshot is independently pinned by its original Git manifest blob.

## Mathematical revision

`sections/rectangular_attainment.tex` proves a compact-space product-cone criterion for all-full-support rectangular pairing rank, a kernel/rank alternative with actual full-support witnesses, an exact dominated-prior singular margin, and a posterior-history consequence. The five-point physical example is genuinely rectangular: no fixed evidence-preserving square subpairing has the same universal property.

`sections/covariance_degenerations.tex` realizes every sufficiently small rectangular covariance matrix, and every scaled analytic matrix germ, by priors in one fixed positive experiment with fixed queries and density between 1/2 and 3/2 of a fixed full-support probability. Determinantal orders yield the joint integer-budget/analytic-arc law, all its phase transitions, and the operational recovery of its orders. Every ordered nonnegative integral list of allowed length is realized.

The finite matrix/sign criteria of Banaji–Pantea and Müller et al., and the classical Smith/singular-value orders discussed by Kaveh–Makhnatch, are explicitly attributed in the introduction, main sections, bibliography and `sections/pairing_comparison.tex`. The mathematical claims separate those inputs from the physical realization and memory conclusions. The square theorem and its full proof are retained.

`RESPONSE_TO_REFEREE.md` gives the point-by-point response. `PROOF_LEDGER_V19.md` identifies every added result and its dependencies. `HISTORICAL_DERIVATION_MAP_V19.md` records the historical arguments actually used. The existing historical records remain available unchanged in `history/v18/` and in the prior manuscript directory.

## Reproduction

Use Python 3.13, SymPy 1.14.0, pdfLaTeX with the standard AMS/LaTeX packages and Latin Modern, and `pdfinfo` from Poppler. Install the symbolic dependency with `python -m pip install sympy==1.14.0`.

```sh
python manifest.py
python build.py --prepare-only
python validate.py
```

The full validator runs the inherited v10–v15, v17 and v18 suites, the new exact v19 suite, an actual inverse-proof mutation against standalone preparation, and the three-pass full PDF build. `validation/EXECUTION_REPORT.json` and `BUILD_REPORT.json` are execution receipts, not promises about a later build. A source author deliberately updating files can regenerate the deterministic current-source manifest with `python manifest.py --write`; this does not alter either pinned historical manifest.

The advertised standalone mode now calls the same historical source checker as the full validator **before** reconstructing a baseline. It anchors `sections/operational_reconstruction.tex` independently to the original v17 manifest as well as to v18. A change to a proof in that source is rejected rather than being copied into both sides of a preservation comparison.

All diagnostics are finite identity/source/build checks. They do not constitute formal proof verification, an independent referee endorsement, or a guarantee of acceptance at any journal. The new results are submitted for renewed scrutiny; no acceptance decision is represented as a mathematical conclusion.
