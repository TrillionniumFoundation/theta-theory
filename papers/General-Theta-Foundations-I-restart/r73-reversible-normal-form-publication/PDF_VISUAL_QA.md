# General Theta Foundations I — PDF layout QA

**Result: no visible layout defect detected in the inspected scope.** The three strict PDFs are directly byte-for-byte identical to the draft PDFs used for the completed visual inspection. Their final identities are therefore bound to source commit `e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b` without repeating identical renders.

| PDF | Pages | SHA-256 |
|---|---:|---|
| General_Theta_Foundations_I_R73.pdf | 26 | `718e9f5b6f30883ab8faa9380c23d92aa5a4d00e593805f371d01bdb84bc27eb` |
| General_Theta_Foundations_I_R73_Supplement.pdf | 143 | `2c21d462cdd9bc4b7d273e8741405454f630ad9b2fac819540a175e467e5d4fb` |
| General_Theta_Foundations_I_R73_Retained_Companion_R58.pdf | 37 | `5bdbe05bcb4955fc4dca36265457675fb94ef86c0ae5c54fd711548f5758c3a3` |

## Completed coverage

All **206 pages** rendered with Poppler at 80 dpi and have recorded PNG and raw RGB pixel SHA-256 fingerprints. All **19 contact sheets** were visually inspected. **18 complete pages** were additionally inspected at 150 dpi: main 1, 8–12, 14, 16–18; supplement 1–2, 103, 112; companion 1, 6, 14–15. This includes all covers, central theorem statements/proofs, the supplement's table and plot, and the qubit formula across the main article's ordinary page continuation.

The all-page text probes found zero out-of-page text spans, zero replacement characters, zero unresolved `??` text markers, and no empty or anomalously short pages. Every listed font is embedded and has a Unicode map.

## Documented extraction limitation

PyMuPDF extracted 18 NUL characters at math-extension delimiter locations on 12 pages. Every one of those locations was inspected in a 150-dpi crop. The parentheses/delimiters are visibly present. Independent Poppler text extraction contains no NUL or replacement character. This is recorded as a PDF-to-Unicode extraction limitation; it is not treated as a visible missing-glyph defect or silently discarded.

## Records and scope

`VISUAL_QA_DRAFT.json` records the full render/probe data and the completed draft visual coverage. `VISUAL_QA_FINAL.json` binds those observations and all page fingerprints to the strict PDFs, successful strict build receipt, source commit and source tree. `ZOOM_INDEX.json` and `NUL_EXTRACTION_PROBE.json` identify the enlarged views and anomaly crops. All output stayed within this QA directory; no manuscript source was changed.

The scrutiny is an AI visual/layout assessment. Every page was seen at contact-sheet scale; selected pages and all flagged glyphs were enlarged. It is not human mathematical referee assessment, full-size line-by-line scrutiny of every page, formal proof verification, priority certification, or an editorial decision.
