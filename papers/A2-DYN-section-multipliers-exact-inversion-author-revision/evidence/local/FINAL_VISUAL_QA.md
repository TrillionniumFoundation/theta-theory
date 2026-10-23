# Final visual QA of the native A2-DYN author revision

## Result and frozen identity

No clipping, unreadable mathematical glyphs, equation-number overlap, obscured headers, broken tables or material margin defects were observed in the inspected pages of the identified 271-page native PDF. This is a separate internal author-side layout check, not a new referee report or independent human specialist certification. No repository source was edited in this inspection.

| Item | Recorded identity |
|---|---|
| Article | `papers/A2-DYN-section-multipliers-exact-inversion-author-revision` |
| PDF | `build/publication-local/native/main.pdf` |
| PDF SHA-256, independently read before and after inspection | `eadbce178543727a68058aa85f94c8f02b5e6a1e3879a392b85a7bfc46a185e6` |
| PDF size and extent | 2,118,501 bytes; 271 pages; US Letter |
| Mathematical source SHA-256 recorded by the corresponding validation summary | `a1b162cec833de28f138c2ba1e353b39be9a6d1d21a4398480afa8c7b38f9bd2` |
| Coverage | Pages **1–8, 239–253, and 271**: **24 pages** |

## Inspection method and actual coverage

All 24 selected pages were directly viewed as original-resolution images in the preceding 271-page candidate, PDF SHA-256 `98d6ed0e207170678fc10a8e740e94c6c6e291f2ce81877d10bf1fc7458e26a5`. The last source edit made the original raw-target supremum ranges explicit in module 334.

Both PDFs were then independently rendered with the same PyMuPDF 1.26.6 settings (`get_pixmap(dpi=132, alpha=False)`) and their exact pixel buffers compared on all 24 selected pages. Only page **246** changed; the other 23 selected pages were pixel-identical between those two PDFs. The publication PDF's pages **245–253** were additionally viewed directly at original resolution, including the changed page 246 and all new fixed-window and endpoint arguments. Thus unchanged-page inspection is carried forward by verified pixel identity, not by assuming that matching filenames or titles imply matching layouts.

`FINAL_VISUAL_QA.json` records the exact directly viewed/reviewed page sets, prior candidate identity, pixel comparisons and individual image hashes. The earlier 269-page second-integration inspection is historical intermediate evidence only and is not used as a claim that every page of this publication PDF was checked.

## Page-specific findings

| Pages | Material and checks | Observation |
|---|---|---|
| 1 | Title, abstract, opening contents, date/classification/keywords and footer | Title hierarchy and abstract are legible; notes and contents are separated; no clipping. |
| 2–5 | Full contents and opening introduction | Dense entries, updated subsection numbers and page references remain readable and within margins. |
| 6–8 | Contribution/status statements, source identities, physical model, exact event and arithmetic target | Source hashes wrap; displayed model/reference formulas and their equation numbers are unobscured. |
| 239–242 | Section 77 multiplier/norm geometry and transfer formula | Integral, derivative, norm and exponent notation is readable; running headers and theorem/proof continuations are consistent. |
| 243–245 | Historical attribution, exact interval inverse, sharp tail, label sum and conditional denominator | Fourier displays, piecewise tail and ratio estimate fit the text block; no equation-number collision. |
| 246 | Final explicit raw-target parameter ranges, bridge quantities, Proposition 78.5 and new subsection | The added ranges are fully visible. The long inequality (78.11), superscripts, aligned quantities and following text remain inside the margins; no vertical or horizontal overflow was observed. |
| 247–248 | Lemma 78.6 and Proposition 78.7: reference derivative and evaluated fixed-window bridge | Gaussian derivative integrals, compactness/damping formula, global supremum and ordered-limit displays are legible. Normal theorem continuation across pages has no clipped content. |
| 249–253 | Endpoint first-image proof, all-flight kernel, reversal, positive-width critical coefficient and Appendix A transition | Long sums, flight indices, normalization factors, critical-sector inequalities, inherited-result distinctions and appendix table remain readable and within margins. |
| 271 | Complete bibliography and final scope text | Journal details, source identities and wrapped URL are visible without overprinting or clipping. |

## Limits

Pages **9–238 and 254–270 were not visually inspected** in this pass. This report therefore does not claim full visual inspection of all 271 pages. It does not certify the mathematical proofs, the original raw pointwise local limit theorem, the inverse theorem, long-time limits, or external expert acceptance. Compilation and visual legibility are separate evidence from mathematical validity. Hyperlinks and every cross-reference were not interactively exercised. The result applies only to the exact PDF hash above; a later changed build needs its own identity check.
