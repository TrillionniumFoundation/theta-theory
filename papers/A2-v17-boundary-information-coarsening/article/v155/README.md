# A2 revision 155 — referee reading entry

Branch: `revision/a2-v155-boundary-fibres-referee-2026-09-25`.

Controlling report: `reviews/a2-v153-materialized-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md` at `52ebb8183433ad398f61958219b2af809f721824`, the report on the complete materialized v153 article. This revision preserves the complete v154 at `a3a59510072f8d012f4436807c83c66d1475573d` and adds two general theorems.

## Manuscripts

[Paper I: reconstruction](reconstruction.pdf) · [complete source](reconstruction.tex)

[Paper II: divisor-incidence fibres and spectral power-zero schemes](divisor-geometry.pdf) · [complete source](divisor-geometry.tex)

[Preservation master](geometry.pdf) · [complete source](geometry.tex)

The two companion papers implement the report's separation request. Each source contains its companion reference map, so it compiles without external auxiliary files. Mathematical dependencies on the other paper are explicitly cited, not presented as absent. The complete master keeps every earlier mathematical block and label. The previous introduction is archived in `PREVIOUS_FRONTMATTER_V154.tex`.

## New results and response

[Point-by-point response](RESPONSE_TO_V153_REPORT.md).

Paper II Theorem 12.1 determines the entire quadratic coefficient section of every reciprocal fibre `F_(g,k)(W)` for `g >= k >= 2`. Theorem 13.2 identifies all spectral Fitting ideals of any complex pencil as power-zero ideals in one such section. Corollary 13.4 expresses the inherited native fixed-spectrum closure order in these reciprocal coordinates. Classical determinant-power apolar and orthogonal-orbit inputs are explicitly attributed.

[Build receipt](BUILD_RECEIPT_V155.json) · [Preservation audit](NONDELETION_V155.json) · [Paper allocation](PAPER_MAP_V155.json) · [Exact checks](EXACT_CHECKS_V155.json) · [Actually rerun predecessor checks](INHERITED_V154_CHECKS_RERUN.json).

Rebuild from the repository root:

```sh
python3 papers/A2-v17-boundary-information-coarsening/article/v155/check_v155.py
python3 papers/A2-v17-boundary-information-coarsening/article/v155/assemble_v155.py --build
```

Requires Python with SymPy, pdfLaTeX with the standard AMS/Latin Modern packages, and Poppler utilities. The build checks the exact v154 source hash before assembly. The historical 28-check suite is not claimed to have been rerun. Finite tests are not universal proof certificates. Ballico 1993 remains documentary-open; no theorem-level historical priority conclusion or journal acceptance is claimed.
