# Final native PDF: scoped independent visual QA

**Result: passed within the inspected scope.** No clipping, overlapping text or equations, missing-glyph boxes, or unresolved theorem/equation labels were observed in the rendered pages listed below. No native source or PDF was modified.

## Exact PDF and scope

- Source: `/workspace/scratch/35c64a3513c5/final-execution-322/native/main.pdf`
- SHA-256: `8eb1f67c250590ee5dc6c78994f710743ad5bf2f442c5071f7c0d60671235efb`
- PDF metadata: 211 pages, 612 by 792 points, US Letter, PDF 1.5, unencrypted; title *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*, author Qian Qi.
- Visually inspected pages: **1–5, 177–194, and 206–211**, totaling **29 distinct pages**.
- The inspection used actual Poppler-rendered PNGs at 110 dpi. Five contact sheets cover pages 1–4, 177–182, 183–188, 189–194 and 206–211. Page 5 and formula-intensive pages 180, 183, 188, 193, 210 and 211 were additionally inspected as individual images at their full rendered resolution.

This is a typography and rendering inspection of the identified pages. It is not an exhaustive visual inspection of the other 182 pages and is not mathematical certification. The prior proof reconstruction and mathematical execution records are separate evidence.

## Page-specific observations

| Material | PDF pages | Actual visual observations |
|---|---:|---|
| Title, abstract, full introduction | 1–5 | The two-line title is centered; author, abstract, introduction and first-page notes are separated cleanly. Introduction formulas and their tags fit the text block. Long source identifiers wrap inside the margins. The continuation on page 5 and transition to Section 1 are readable. |
| Native 319, Section 62 | 177–179 | Theorem 62.1, Lemma 62.2 and Theorem 62.3 are visibly distinguished. The positive optical recurrence, weighted overlap sum and equations (62.1)–(62.5) have legible signs, fractions and right-side tags. The transition to Section 63 does not leave an isolated heading. |
| Native 320, Sections 63–64 | 179–185 | The multiline constants (63.1)–(63.3), Jacobian variation, momentum derivative and radial-turning formulas are clear. The long Section 64 heading fits. Theorem 64.1, the normalization (64.1) and the depth sum (64.3) show no tag collisions or clipped operators. Proof continuations across pages are conventional and readable. |
| Native 321, Section 65 | 185–190 | The affine family, class definitions, reciprocal Jacobians and all-class capacity statement are legible. The multiple display lines (65.13)–(65.16) retain adequate spacing and separate tags. The full-pressure decomposition (65.19) and the transition to Section 66 fit inside the text block. |
| Native 322, Section 66 | 190–194 | Lemmas 66.1–66.2 and Theorem 66.3 have resolved labels. The common-clearance and limiting-half-sum displays are readable. The long all-mark estimate (66.5), including both sums and the normalization, fits on its line with a separate right-hand tag. The proof ending and Appendix A transition on page 194 are clean. |
| Dependency/reference appendices | 206–210 | Appendix headings H–L, cross-references, normalization formulas and citation locators render without clipping or overlap. The current dependency notes on page 210 distinguish the new theorem references clearly. |
| Bibliography | 211 | All nine entries, commit identifiers and the final URL remain inside the margins and are readable. Entry [1] has loose justified word spacing; this is the minor nonblocking observation described below. |

Running headers, alternating author/title headings, page numbers, theorem styles and proof-ending squares are consistent across the inspected ranges.

## Exact commands and retained evidence

The initial metadata command was:

```bash
pdfinfo /workspace/scratch/35c64a3513c5/final-execution-322/native/main.pdf
```

The full text and bounding-box extractions were run from
`/workspace/scratch/35c64a3513c5`:

```bash
pdftotext -layout /workspace/scratch/35c64a3513c5/final-execution-322/native/main.pdf /workspace/scratch/35c64a3513c5/final-pdf-qa/main-layout.txt
```

```bash
pdftotext -bbox-layout /workspace/scratch/35c64a3513c5/final-execution-322/native/main.pdf final-pdf-qa/main-bbox.xhtml
```

Each selected page was actually rendered with an individual command of the following form; **all 29 complete argument lists and their successful return codes are recorded in `render-execution.json`**:

```bash
pdftoppm -f 193 -l 193 -r 110 -png -singlefile /workspace/scratch/35c64a3513c5/final-execution-322/native/main.pdf /workspace/scratch/35c64a3513c5/final-pdf-qa/page-193
```

The five contact sheets were assembled from those PNGs with Pillow, with explicit page captions. `render-execution.json` records their page lists and dimensions. `rendered-image-sha256.json` identifies the actual page images and contact sheets inspected.

The original final compilation log was read without alteration. It contains no overfull-hbox or missing-character messages and no unresolved-reference warning. There are three underfull-hbox warnings in the first bibliography entry and one font-expansion ordering warning. The loose spacing on page 211 is visible but does not make content unreadable; no corresponding visible glyph defect was found. The exact excerpt is preserved in `final-log-layout-excerpt.txt`. No corrective native edit was indicated by this scoped inspection.

The supplementary text-bounds check found zero extracted words outside the PDF media box and zero `??` reference tokens on the selected pages. Its detailed page extents are in `bbox-observations.json`; these checks support but do not replace the visual inspection. The first strict XML parse of Poppler's extracted XHTML rejected a non-XML control token. The unchanged extraction was then read with the standard-library HTML parser; this auxiliary parser issue and the successful fallback are recorded. It was not treated as evidence of a rendered missing glyph.

`VISUAL_QA_RESULT.json` contains the machine-readable result, the exact inspected page lists, the PDF hash, observed limits and nonblocking typography notes.
