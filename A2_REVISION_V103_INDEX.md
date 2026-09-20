# A2 v103 — finite-sheet metric contact and spectral quotients

**Revision branch:** `revision/a2-v103-finite-sheet-metric-quotients-2026-09-20`.

**Controlling review:** `review/a2-v102-independent-harsh-top4-2026-09-20`, commit `8054ae5d5c318b7e59f9ad42545ae27b416bec09`.

**Principal source commit:** `b50fbbe0ce30856bd1b10cd66ab70351fd8f4295`. **Native-build source commit:** `618b0b098654f53e61a782138272349df92d16ad`.

## Manuscript and response

[New self-contained principal source](papers/A2-v17-boundary-information-coarsening/article/v103/paper.tex) · [Point-by-point response to R102.1–R102.8](revisions/a2-v103/RESPONSE_TO_REFEREE.md) · [Full content-preservation map](revisions/a2-v103/CONTENT_PRESERVATION.md)

The principal, *Finite-sheet metric contact and spectral quotients of polynomial observations*, has 18 pages in the locally compiled native PDF. Its proof sequence is:

| Result | Location | Added conclusion |
|---|---|---|
| Finite-sheet metric structure | Theorem 2.2; Corollary 2.3 | Exact closed semidefinite lift, exposed tensor faces, polynomial realization and products |
| Coupled cancellation and its envelopes | Theorems 3.1–3.2; Corollary 3.3; Theorem 3.6 | Several fast equations, vector residuals, competing inverse sheets, exact cancellation walls and positive-probability realization |
| Whole-model spectral limit | Lemmas 4.1–4.2; Theorem 4.3 | Explicit inverse, uniform cluster bounds, feasible construction and both Hausdorff inclusions |
| Native Hellinger information | Theorems 5.1–5.3 | Rational moments, dimension-based query bounds, and an exact three-query theorem with clocks and weights fixed |
| Endpoint quotient classification | Theorems 6.1–6.2 | Finite equality test, geometric range, canonical value-function data and complete one-endpoint equivalence classes |
| Real feasible presentation | Theorem A.1; Proposition A.2 | Proper-surjective analytic construction, accessible real faces, and the classical exponent/unit calculation |

The fixed-experiment native Jacobian has determinant **933885 modulo 1000003**. The independent design-variation minor is **230039 modulo 1000003**. Appendix B and the exact checker give the arithmetic. These are finite exact certificates, not numerical rank guesses.

## Preserved volumes

[Principal wrapper](papers/A2-v17-boundary-information-coarsening/rigidity_v103.tex) · [Complete v102 supporting article](papers/A2-v17-boundary-information-coarsening/rigidity_v103_supporting.tex) · [Full historical archive](papers/A2-v17-boundary-information-coarsening/rigidity_v103_archive.tex) · [Complete volume wrapper](papers/A2-v17-boundary-information-coarsening/rigidity_v103_complete.tex)

All previous mathematical and review files are inherited unchanged. The archive contains the complete v102 article and its complete earlier source graph; the complete v103 volume adds the new principal once. No earlier branch or main is changed by this revision.

## Evidence and native build status

[Exact diagnostics](revisions/a2-v103/EXACT_DIAGNOSTICS.json) · [Local validation](revisions/a2-v103/LOCAL_VALIDATION.json) · [Source manifest](revisions/a2-v103/SOURCE_MANIFEST.json)

The local handoff bundle contains the principal PDF and its complete native log; their hashes are recorded in the local validation file.

The new principal and its wrapper were compiled locally with pdfLaTeX/latexmk. Their rendered pages agree. The final logs contain no undefined references/citations, multiply-defined labels, overfull or underfull boxes, or LaTeX warnings. The principal, checker and native-builder source blobs were read back from GitHub and match the local bytes.

The full-graph workflow was triggered as run **35504308437** at source commit **618b0b098654f53e61a782138272349df92d16ad**. **Its last observed status during preparation of this index was queued; no full-graph native success is claimed.** The local principal build is not the full archive build. R102.8's full-runtime evidence remains pending the actual successful receipt.

After an actual successful run, the branch-scoped workflow publishes `revisions/a2-v103/native/RUNTIME_RECEIPT.json`, the four PDFs and native logs. The receipt records the compiled source commit, not the later artifact-only commit. A later documentation-only commit does not invalidate unchanged source hashes, but it is not asserted to have compiled its own hash.

To reproduce from a checkout with Python, SymPy, latexmk and the required TeX packages:

```sh
python3 scripts/check_a2_v103.py --output /tmp/a2-v103-exact.json
python3 scripts/build_a2_v103.py --dry-run
python3 scripts/build_a2_v103.py
```

For a principal-only native build, run `latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v103.tex` from `papers/A2-v17-boundary-information-coarsening/`. The full builder instead traverses and binds the inherited graph, checks preservation, and emits a full receipt only after success.
