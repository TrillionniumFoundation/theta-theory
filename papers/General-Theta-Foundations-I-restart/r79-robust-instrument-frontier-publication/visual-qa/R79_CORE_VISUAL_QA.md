# R79 core-proof visual QA

## Scope and artifact identity

This is an internal author-production visual check of the twelve rendered manuscript pages listed below. Each page image was actually opened with `view_image` and visually inspected. Image generation or PDF text extraction alone was not treated as a visual check. The assignment was limited to typography, equation placement, page and line breaks, readability, and obvious clipping; it did not reopen the mathematical proof audit.

- Source commit recorded by the render receipt: `90cae2f5aca243b39d3a2194a4d6e0696671a101`.
- PDF inspected through its page renders: `/workspace/scratch/b8655e579b01/r79_verified_build/General_Theta_Foundations_I_R79.pdf`.
- PDF SHA-256, independently recomputed with `sha256sum`: `a3fd7fbe25f008a7c430c52d9963807570a018d27009301111ecb5dc02131518`.
- Render receipt: `/workspace/scratch/b8655e579b01/r79_visual_qa/RENDER_RECEIPT.json`. Its manuscript PDF hash and source commit agree with the identity above.
- Image directory: `/workspace/scratch/b8655e579b01/r79_visual_qa/`.

## Images actually viewed

The page numbers below are both the rendered manuscript page numbers and the suffixes of the individual images. All twelve were viewed individually at the image tool's displayed resolution, rather than only in contact sheets.

| Page | Exact image filename | Visual findings |
| --- | --- | --- |
| 9 | `manuscript-page-009.png` | Cost definitions and equations (3.5)–(3.8), Theorem 3.1, and its proof fit within the text area. Displayed mathematics, theorem numbering, and running header are legible. |
| 10 | `manuscript-page-010.png` | Theorem 3.1 proof ending, invariant-corner and reachability displays (3.9)–(3.10), and Lemma 3.2 are readable. Theorem 3.3 starts near the foot and continues normally on page 11; no content is clipped. |
| 11 | `manuscript-page-011.png` | Support, cost, and budget displays (3.11)–(3.13), the quantified display (3.14), and the surrounding proofs have adequate separation. Long formula lines remain within the margins. |
| 12 | `manuscript-page-012.png` | Algebraic-proof ending, scope text, and Example 3.5 are readable. The example's last paragraph continues onto page 13 without a truncated line. |
| 13 | `manuscript-page-013.png` | Example 3.6, the section 4 heading, attribution and supplement references, and restart equations (4.1)–(4.2) render correctly. Theorem 4.1 continues on page 14. |
| 14 | `manuscript-page-014.png` | Restart bounds (4.3)–(4.4), the proof and its closing symbol, normalized-instrument notation, and distance formulas (4.5)–(4.6) are legible and do not collide. |
| 15 | `manuscript-page-015.png` | Lemma 4.2, formulas (4.7)–(4.8), and Theorem 4.3's bounds (4.9)–(4.11) fit cleanly, including equation numbers and the zero-instrument-error qualification. |
| 16 | `manuscript-page-016.png` | The stability proof, aligned bounds, scope paragraph, and Corollary 4.4 with (4.12)–(4.13) are readable. The corollary's proof begins on the next page after a complete statement. |
| 17 | `manuscript-page-017.png` | Corollary 4.4's proof, including the controller-history explanation, and Corollary 4.5 with (4.14)–(4.16) are readable. The positive-success statement continues normally into its proof on page 18. |
| 18 | `manuscript-page-018.png` | The resolvent calculation, its two-line operator identity, exact scalar comparison (4.17), closing proof symbol, and section 5 heading are clear. Equation numbering does not encroach on the formulas. |
| 19 | `manuscript-page-019.png` | Proposition 5.1, the three memory values, lower-bound displays, and the complete proof are readable. The final explanatory paragraph continues normally onto page 20. |
| 20 | `manuscript-page-020.png` | The previous paragraph's continuation, section 6 heading, reset-instrument displays (6.1)–(6.2), and the paired variational displays (6.3)–(6.4) fit within the page. Theorem 6.1 continues beyond this page, outside this check's scope. |

## Result

**PASS within the stated twelve-page visual scope.** No obvious clipping, overlapping text, missing or replacement glyphs, equation-number collisions, unreadable formulas, unresolved `??` references, or header/body collisions were observed. Dense mathematical paragraphs remain legible. The normal theorem and proof continuations across page boundaries do not require a source change on visual grounds. No source file was altered during this check.

The images were sufficiently clear to inspect the displayed formulas; no PDF-text fallback was needed. The actual PDF file was read for its SHA-256 identity, independently of the render receipt.

## Limitations

This note covers only manuscript pages 9–20 at the rendered resolution. It does not claim visual inspection of the rest of the 59-page manuscript, the supplement, the retained companion, or print output. The theorem continuation after page 20 was not inspected here. Other production checks are recorded separately.

This is an internal author visual-QA record, not an independent referee report, external expert assessment, new proof verification, formal proof certificate, bibliography/priority audit, or editorial decision. The source commit identity is the one recorded in the build/render materials; this note independently confirms the PDF bytes and the actual page-image inspection, not a separate rebuild of that commit.
