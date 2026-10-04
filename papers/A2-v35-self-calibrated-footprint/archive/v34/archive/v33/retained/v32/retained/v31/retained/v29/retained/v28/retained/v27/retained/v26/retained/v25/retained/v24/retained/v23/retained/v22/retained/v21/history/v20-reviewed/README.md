# A2 v20 — canonical short channels and all-cycle rigidity

Qian Qi · 29 September 2026

**Intrinsic marked boundary laws and rigidity of periodic dispersing billiards** is the primary manuscript (`main.tex`, 21 pages in the actual local build). This revision responds to the latest v19 report at `d2744e3cd159cdbf926359fea1f9322e847280ad`, reviewing author commit `2f51ac5a2ab72deceb21c23084ca3062056edb4c`. It retains the topic and the requested Annals/Acta/Inventiones/JAMS mathematical target.

## Main results and reading order

Start with Theorem 1.4 and Section 5. Lemma 5.1 replaces an obstructed shortest bridge by strictly shorter pairs. The finite set of periodic gap types makes this a terminating induction. Theorem 5.2 proves that all clear shortest normal bridges of gap less than R form a connected lifted graph whenever R exceeds twice the obstacle covering radius. Its cycles generate the entire period lattice. This geometric theorem requires neither analyticity nor asymmetric shapes and does not require finite horizon.

Theorem 5.4 uses all recovered cycle vectors rather than searching for a primitive pair. Their normalized pair determinants have integer gcd q, the index of their full generated group in the period lattice. This sharpens the algebraic candidate bound to the divisor sum of q. Proposition 5.5 gives actual analytic tables with pair indices 2, 3, 5: no observed pair is primitive, but the complete cycle group is.

Theorem 5.6 combines geometric completeness with the retained local inverse and analytic image matching. On the analytic asymmetric, pairwise noncongruent class, a complete short-channel catalogue determines the whole table and unmarked period group without a designed connected primitive network, obstacle identities, incidence labels or integer copy labels. Theorem 5.8 gives conditional finite-histogram stability with all-cycle integer locking and no primitive-pair hypothesis.

Completeness is an acquisition assumption, not inferred from an incomplete list. The local contact origin, selected return branch, paired absolute times and coherent within-record reversal remain marked. The density functions and growing histograms are function-valued observations, not two scalars. The statistical theorem retains explicit compact analytic, physical, shape and symmetry margins, onset brackets and regular catalogue charts. It claims neither efficient search nor a minimax rate. No exact analytic count-only conclusion is inferred.

## Preserved mathematics

Four v19 core files remain active byte-for-byte. The original local, finite-index, prime-index ambiguity, primitive-class statistical and literature-comparison proofs remain in the primary. Section 1 is expanded around its retained statements, and Section 5 is new. The exact entire v19 manuscript is archived at `history/v19-reviewed` with native tree `57d8eff44d32a07445db7e0a041eea5d6125bdd0`.

Supplement R is the complete v18 paper at `retained/v18`, tree `3c558d7799e9e49812e7bab98320d3a98e7f7418`. Supplement S and its auxiliary document are at `complete`, tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`. All inputs, earlier moment/count/relative-law arguments and historical material are retained. Existing repository papers and reviews are not edited. See `SUPPLEMENT_MAP.md`.

## Reproduction and actual evidence

Run `python3 tools/validate_v20.py` for the primary. In a real checkout with the preserved volumes, run `python3 tools/validate_v20.py --all-volumes --require-checkout`. Requirements are Python 3.10+, NumPy/SciPy, latexmk, an amsart-capable LaTeX installation and Poppler pdfinfo.

The actual local primary run passed 65,469 finite diagnostics: 43,897 from the unchanged inherited checker on this source and 21,572 from the new checker. Normal and optimized Python outputs were identical. The inherited 90 nonlinear stationary-ray curvature comparisons had maximum absolute error 1.2312545871751013e-08. The 21-page primary compiled without final TeX warnings, undefined references or overfull/underfull boxes. Its mathematical and tool manifest was unchanged. The finite checks are not counts of independent theorems and do not certify infinite proofs.

This was source-content execution, not an authenticated Git checkout, and the retained volumes were not rebuilt locally. `verification/local/receipt.json` records null checkout/run fields. `verification/local-execution.tar.xz` contains that exact receipt, every command log and the final TeX log. `PUBLICATION_BINDING.json` binds their hashes to the published native sources. Runtime timestamps are retained as observed rather than changed to match the manuscript date.

The read-only v20 GitHub workflow checks out its exact triggering SHA, verifies retained trees, reruns the primary and retained diagnostics, and builds the primary plus Supplements R, S and the auxiliary document. It archives actual logs and PDFs, including failures. A workflow definition or queued run is not a hosted pass. No hosted full-package success, human proof audit, formal proof certificate or journal decision is asserted by this README.
