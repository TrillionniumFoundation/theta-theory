# Main manuscript draft02: rendered PDF layout QA

## Scope and identity

This is author-team AI **layout QA**, not mathematical proof verification,
human review, an external referee report, or an editorial decision. No source
file was edited by this reviewer.

- PDF: `/workspace/scratch/f856e3d63ac5/r76-build/draft02/General_Theta_Foundations_I_R76.pdf`
- SHA256: `d9500c5fdfc072933a54bef875644c95fa761d6bcfd23ccd86279a0aeb08bbaa`
- File size: 615,412 bytes.
- Page count: 35; every page is 612 by 792 points, unrotated US Letter.
- Recorded completion: 2026-10-21 13:36:40 UTC.
- Reviewer task: `/root/r76_structural_math`.
- Workflow: the PDF skill was read and followed for read-only visual inspection.
  Poppler rendered all pages; Pillow assembled contact sheets. No image
  generation or PDF content rewriting was used.

## What was actually viewed

All 35 pages were rendered at 144 dpi to 1224 by 1584 PNGs in
`pages-144dpi/`. Nine 2-by-2 contact sheets in `contact-sheets/` present each
page at 612 by 792 pixels with an external page label. Every contact sheet
was opened and visually examined through the image-viewing tool:

| Contact sheet | Pages visually examined |
| --- | --- |
| `pages-01-04.png` | 1, 2, 3, 4 |
| `pages-05-08.png` | 5, 6, 7, 8 |
| `pages-09-12.png` | 9, 10, 11, 12 |
| `pages-13-16.png` | 13, 14, 15, 16 |
| `pages-17-20.png` | 17, 18, 19, 20 |
| `pages-21-24.png` | 21, 22, 23, 24 |
| `pages-25-28.png` | 25, 26, 27, 28 |
| `pages-29-32.png` | 29, 30, 31, 32 |
| `pages-33-35.png` | 33, 34, 35 |

The following **21 pages were also individually opened at the original
144-dpi render dimensions**, rather than examined only as thumbnails:

- Pages 10–13: new convex-specification normal form, attained optimization,
  robust multiplicity inequalities, prime-orbit corollary and the opening
  of the mean–contrast section.
- Pages 14–18: simultaneous-positivity inequality and proof, the piecewise
  boundary, synthesis equivalence, boundary factorization and rigidity,
  the exact symmetric-group law, and its physical realization.
- Pages 20–24: rare-excursion lemma, sharp expected-cost calculation, return
  geometry, the coupling proof, finite-alphabet state count, explicit
  qubit return weights and overflow-depth/error displays.
- Pages 25–27: physical-dictionary lower, its constants and packing proof,
  leading-order asymptotic, golden phase, rational-rotation upper, and
  the transition into the retained causal transfer theorem.
- Pages 32–35: all reference entries, including the isolated final entry.

Other pages were examined on their contact sheets only; no individual
full-page inspection is claimed for those pages. This receipt does not claim
visual inspection of any different later PDF merely because its filename is
similar.

## Observed result

No page-edge clipping, overlapping mathematical displays, missing-glyph
boxes, illegible equation numbers, broken page headers, or corrupted
reference glyphs was seen. The new long displays fit inside the page area
and remain readable at the individual render scale. In particular,
equations (4.8), (5.1), (5.8)–(5.12), and (7.1)–(7.17) were visually
checked in their page context. Equation (5.10) is wide, with a relatively
short gap before its tag, but its content and tag remain distinct and
unclipped. Theorem and proof continuations across page boundaries are
readable; no heading is stranded by itself.

The title, author, abstract, page numbers, running headers, section hierarchy,
theorem fonts, and proof-end symbols are consistently rendered. The
references' DOI/arXiv strings and long URL lines are readable and contained
within the page area. Their bibliographic correctness was not re-audited
as part of this layout task.

### Findings requiring disposition

| ID | Page | Finding | Suggested action | Severity |
| --- | --- | --- | --- | --- |
| MAIN-D02-01 | 11 | The infimum subscript renders `pure-start controllerson at most M labels`; the adjacent text fragments omit the separating space. | Insert a space inside the first text fragment or an intentional substack line break in `sections/45-convex-specifications.tex`. | Minor typography defect; reported to root. |
| MAIN-D02-02 | 35 | The last page contains only reference [80], a two-line Li 1980 entry, leaving nearly the entire page blank. | Consider a bibliography-only spacing or page-break adjustment that keeps this entry on the preceding page. | Nonblocking layout polish; reported to root. |

The first finding was confirmed against the source display containing
`\text{pure-start controllers}\text{on at most }`. Neither finding changes
a mathematical statement. This draft is therefore **inspected with two
minor findings**, not recorded as a defect-free final artifact.

## Supplementary checks and stored evidence

`pdfinfo.txt`, `pdffonts.txt`, and `pdftoppm-version.txt` preserve the actual
tool outputs. Poppler completed rendering all 35 pages with return code zero
and no stderr diagnostics. All listed PDF fonts are embedded. Text extraction
found no literal `??` unresolved-reference markers and no empty text pages;
these checks supplement rather than replace the visual inspection.

`RENDER_MANIFEST.json` fixes the PDF hash and SHA256 of every rendered page
and contact sheet. `TEXT_AND_METADATA_CHECKS.json` records page dimensions
and the limited extraction checks. `VISUAL_QA_RECEIPT.json` records the
actual inspection coverage and findings in a machine-readable form.

If the final strict PDF is byte-identical to the input hash above, the
rendered inspection applies directly, with the same findings. If its bytes
differ, compare page renders and inspect the changed pages; source or build
success alone does not establish that a later layout was visually checked.
