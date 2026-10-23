# R80 core proof span: visual production QA

## Artifact and scope

- Source commit: `c0ac246181c2f4214e3e830952386adffb7d82df`.
- PDF: `r80_verified_build/General_Theta_Foundations_I_R80.pdf`.
- PDF SHA-256, independently rechecked for this note: `b5079f2cf21c487af8aa961a9afcdf930c5b5454a94cbbca1dd864ed50437368`.
- Pages actually opened and visually inspected: **20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, and 32** (13 pages, inclusive).
- Inspection input: the 110-dpi page rasters `r80_visual_qa/manuscript-page-020.png` through `manuscript-page-032.png`. Every listed image was opened with `view_image` at original detail and viewed individually within labeled batches. Rendering or text extraction alone was not counted as inspection.

The inspected span includes the end of the inherited Lipschitz result, the complete new square-root sharpness proof, the complete arbitrary-finite-location search classification and resource bounds, and the start of the retained exact hidden-model memory example.

## Findings

**No blocking production defect was found in these pages.** There is one minor cosmetic wrap, recorded below.

| Pages | Actual visual findings |
|---|---|
| 20-22 | The scalar success table, sharpness constants, six controller parameters, positive-polynomial identity, endpoint discussion, and opposite-orientation formulas are legible. No formula, equation number, or text extends outside the visible text block or collides with another element. |
| 23-25 | The derivative signs, coercivity estimates, matching-controller formulas, lower-limit inequalities, and final arithmetic-geometric-mean bound display correctly. Superscripts, subscripts, radicals, fractions, and proof-ending marks are visible. Page breaks retain the continuation of the argument without severing a display. |
| 26-28 | The finite-search data, fallback, word-cost formula, greedy indices, exchange vector, tail/frequency estimates, convex-saddle proof, and projected-support lemma are readable. **Minor cosmetic issue on page 26:** the introductory sentence of Lemma 6.1 wraps the single word “row” onto its own line immediately before equation (6.2). The mathematical content is clear and no text is clipped. |
| 29-31 | The arithmetic equivalence, class-frequency formula, counted first-step mixture (including the explicit zero-probability-row convention), prior floor, exponential memory bound, and rational sufficient label cap all render correctly. The split rate-constant and label-cap displays have readable alignment and remain clear of their equation numbers and margins. The reference to supplement Section S1 is visible. |
| 32 | The conclusion of the new search section and transition to the retained hidden-model memory example are clean. The golden-ratio value display and its proof formulas are readable, with no observed collision, clipping, or missing mathematical glyph. |

Headers, page numbers, theorem/proof typography, and body margins are consistent throughout the inspected range. No missing-glyph boxes, unreadable alignments, broken radicals, overlapping labels, or substantive change of mathematical meaning caused by typesetting was observed. Ordinary paragraph continuations across pages remain intelligible.

## Limits and status

This is **author-side AI production QA** of the specified artifact and page range. It is not an independent human referee report, mathematical proof verification, formal verification, or editorial assessment. The observation about preserved mathematical meaning concerns visible typesetting only; it does not certify the correctness of the propositions or their proofs. Other manuscript pages and the supplement were outside this note's assigned inspection scope.

The minor single-word wrap is a nonblocking cosmetic finding. No source files were edited during this inspection. This note applies to the exact PDF hash above; a subsequent rebuild with a different PDF hash requires the relevant rendered pages to be inspected again before transferring these findings.
