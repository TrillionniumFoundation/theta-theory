# Independent internal visual QA of the A2-DYN native manuscript

## Scope and identity

This is a separate author-side layout inspection, not a referee report, a mathematical proof audit, or an independent human specialist certification. No repository source was edited in performing this check.

The inspected **intermediate** PDF is `build/second-integration/native/main.pdf` in `papers/A2-DYN-section-multipliers-exact-inversion-author-revision`:

- PDF SHA-256: `f88d5f98875066e3aa3128bf51c1d1a7b45470d8920a2c0379b9394bca283128`.
- Size: 2,103,778 bytes; 269 pages; US Letter (612 by 792 points).
- Actual page images viewed at their original 1121 by 1450 pixel resolution: **1–8, 239–251, and 269**, for **22 pages total**.
- Page 5's two first contents entries were additionally inspected in an enlarged crop to confirm their complete subsection numbers.
- Image identities and page numbers are recorded in `visual-qa-independent-evidence.json`.

The source author subsequently announced changes to module 334's inherited-result attribution and the fixed-window bridge. Those changes were not present in this snapshot. This inspection must not be represented as visual approval of a later PDF merely because its title or filename is the same. Final-source inspection is pending a frozen build and its new page mapping.

## Actual observations

| Inspected PDF pages | Material inspected | Visual result |
|---|---|---|
| 1 | Title, author, abstract, opening contents, date/classification/keywords, page footer | Legible title and abstract; clean margins; no collision between the contents and first-page notes; visible page number. |
| 2–5 | Remaining contents and beginning of introduction | Section titles, page references, appendix entries and indentation remain readable. The long contents are dense but do not clip or overlap. The subsection numbers 79.2 and 79.3 on page 5 are fully printed; an initial reduced-display ambiguity was resolved by the enlarged crop. |
| 6–8 | Contribution/status discussion, source identities, physical model, exact records, arithmetic reference and target | Text, inline source hashes and displayed formulas remain within the text block. No equation-number collision, missing glyph or overlapping header was observed. |
| 239–242 | Transition from inherited weak operator result to section 77; norm qualification, geometry, multiplier and moving-section statements | Superscripts, norm subscripts, integral signs, fraction bars, theorem labels and displayed equation numbers are readable. Normal paragraph/theorem continuations across page breaks are visible without clipping. |
| 243–246 | Section 78: exact interval inversion, full tail, all-label summation, normalization, conditional denominator, initial raw bridge | Multiline Fourier integrals, piecewise tail function, conditional ratio and long normalized inequality fit the available width. The tables of quantities are aligned; no equation label obscures mathematics. |
| 247–250 | Section 79: first-image constants and density, selected kernel, reversal proof, positive-width critical coefficient and original guard sum | Mathematical indices and exponents remain legible. Long formulas and theorem statements remain within margins; section/subsection hierarchy and proof-ending symbols are consistent. |
| 251 | End of new critical discussion and transition to Appendix A | Appendix heading, inherited-result explanation, finite table and formulas are readable; the source-path text wraps without crossing the page edge. |
| 269 | Final bibliography entries | Author names, journal information and wrapped URL are visible; no clipping or overprinting was observed. The partially filled final page is ordinary end matter. |

**Result for this inspected snapshot:** no clipping, unreadable mathematical glyphs, overlapping equations, obscured equation numbers, broken headers or material margin defects were observed in the 22 viewed pages. The document is dense mathematical typesetting, with normal theorem/proof continuation across page boundaries.

## Limits

Pages 9–238 and 252–268 were not visually inspected in this pass. The two overview montages were not used as a substitute for reading individual page images. This report does not claim that all 269 pages were visually checked, that all hyperlinks or cross-references were exercised, that the complete proof chain is valid, or that a successful PDF render establishes the raw local limit theorem. Any later edit that changes pagination or new proof content needs inspection against its own frozen PDF identity.
