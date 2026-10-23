# R80 two-location supplement: visual production QA

**Result:** no blocking visual or formatting defect found in the seven assigned pages.

## Artifact identity and coverage

- Associated strict-build source commit: `c0ac246181c2f4214e3e830952386adffb7d82df`.
- PDF: `General_Theta_Foundations_I_R80_Supplement.pdf`.
- PDF SHA-256, independently checked against the actual built PDF bytes: `14553246ed4f807a1382a9a78419008dbc658fad1bff714c11628c9815c5354b`.
- Pages actually opened and visually viewed: **1, 2, 3, 4, 5, 6, and 7**, inclusive, with no page omitted.
- Viewed inputs: `r80_visual_qa/supplement-page-001.png` through `supplement-page-007.png`, rendered at 110 dpi; each image is 935 by 1210 pixels.
- Review type: internal author-AI production QA. No source or PDF edits were made.

## Page findings

| Page | Visually checked content | Finding |
|---|---|---|
| 1 | Title, author, abstract, scope paragraph, start of S1, definitions, footer | Legible hierarchy and consistent margins. The final definition continues normally onto page 2; no clipping or footer collision. |
| 2 | Word costs, classical attribution, Lemma S1.1, cases display, frequency limit, exchange formula | Equations S1.1-S1.4 and their numbers are intact and aligned. Cases, subscripts, superscripts, Greek letters, and brackets render clearly. |
| 3 | Logarithmic strip, survival identities, compactness and separation proof | Equations S1.5-S1.6 fit within the text block. Multiline proof and page continuation show no lost or overlapping lines. |
| 4 | Endpoint-prior argument, tie mixture, Lemma S1.2, start of Theorem S1.3 | Equation S1.7, theorem displays, and proof-ending squares are intact. The theorem continues coherently onto page 5. |
| 5 | Explicit constants, bound S1.9, irrational obstruction, rational implementation, start of quantitative proof | The constants occupy two balanced display lines. Fractions, floors, powers, and conditional-mixture notation are legible; no margin overflow is visible. |
| 6 | Survival bound, counted-prefix argument, Corollary S1.4, rational cap, start of Example S1.5 | Equations S1.10-S1.11 and proof endings render cleanly. The example has substantive text before its continuation onto page 7. |
| 7 | Completion of Example S1.5 and S1 scope statement; visible transition to S2 | The complete two-location section ends cleanly. The S2 heading, ensuing text, and visible displays also show no clipping or glyph defect. |

Across all seven images, I observed no clipped text, overlapping elements, missing-glyph boxes, broken equation alignment, or unresolved reference placeholders. Alternating running headers and page numbers are consistent. Paragraph and proof continuations across the inspected page boundaries are readable.

## Limits

This inspection concerns the rendered production quality of the identified PDF on pages 1-7 at the stated raster resolution. It does not certify mathematical correctness, bibliographic priority, formal proof verification, independent human referee approval, editorial suitability, or unviewed pages. Mathematical proof audits and exact-arithmetic diagnostics are separate records and are not inferred from this visual inspection.
