# Paper 2 Submission Package Checklist

Current package shape:

- Single manuscript: `main.tex` inputs `technical-appendix.tex`.
- Retained submission PDF: `theta-expectation-hjb.pdf`.
- Bibliography: `main.bbl`, generated from `../../reference.bib`.
- Planning/audit files kept out of the submitted package:
  `theorem-inventory.md`, `risk-register.md`, `execution-plan.md`,
  `extraction-checklist.md`, `compile-status.md`, and
  `referee-risk-memo.md`.

## Target Venue Posture

Default target family for Paper 2:

- Primary fit: probability/PDE/control venues that accept deterministic
  homogenization and viscosity-solution arguments.
- Candidate target families: `AAP`, `PTRF`, `AIHP`, `ARMA`, `SICON`, and
  adjacent PDE/control journals after Paper 1's companion status is fixed.

Submission posture:

- Active posture is a single PDF with technical appendices.
- Keep Paper 1 as an imported first-principles response theorem, not as an
  unproved black-box assumption.
- Keep singular-billiard response proofs out of Paper 2.
- Keep BSDE, Girsanov, and Cameron-Martin representation formulae out of the
  proof of the HJB limit; they remain downstream material for Paper 3.
- Keep the concrete nonconvex port in the main text because it answers the
  likely referee demand for an inspectable example.

## File Naming

Working source names:

- Article source: `main.tex`.
- Appendix source: `technical-appendix.tex`.
- Bibliography file for source submission: `main.bbl`.

Submission-facing PDF:

- `theta-expectation-hjb.pdf`.

If source upload is required:

- Upload `main.tex`, `technical-appendix.tex`, and `main.bbl`.
- If the venue requires BibTeX source instead of `.bbl`, copy
  `../../reference.bib` into the source bundle and adjust the bibliography path
  according to the venue instructions.

## Compile Commands

From `papers/theta-expectation-hjb/`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Fast rebuild after `main.bbl` is current:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## QA Gates

Before packaging:

- `theta-expectation-hjb.pdf` is built from `main.tex` and
  `technical-appendix.tex`.
- `main.bbl` is current and included in source-submission options.
- `main.log` and `main.blg` have no fatal errors.
- No undefined references or citations.
- No undefined control sequences.
- No rerun warnings.
- No overfull boxes.
- Only underfull box warnings remain.
- `theta-expectation-hjb.pdf` page count and SHA are recorded.
- Submission-facing source scan has no internal source-line tags, workspace
  paths, extraction macros, placeholder/process markers, or visible
  separate-package wording in `main.tex` or `technical-appendix.tex`.
- BSDE/Girsanov/Cameron-Martin material appears only as excluded downstream
  representation material, not as proof input.

Current checked state:

- `theta-expectation-hjb.pdf`: 27 pages, 482590 bytes.
- `main.tex`: 37029 bytes.
- `technical-appendix.tex`: 69578 bytes.
- `main.bbl`: 1534 bytes.
- SHA256 `theta-expectation-hjb.pdf`:
  `c8c55404f9464029fd8f3f7454f4756d0daa465fe381b0187bffa1944a8c9cf7`.
- Last clean check: 2026-07-09 16:31 Asia/Shanghai.
- Logs clean for fatal/error/undefined citation/reference/undefined control
  sequence/overfull/rerun warnings.
- Submission-facing scan over `main.tex` and `technical-appendix.tex` is clean
  for local process markers, master-source line tags, workspace paths,
  extraction macros, and separate-package wording.

## Packaging Options

PDF-only submission:

- Upload `theta-expectation-hjb.pdf` as the manuscript.

Source submission:

- Upload `main.tex`, `technical-appendix.tex`, and `main.bbl`.
- Include standard LaTeX dependencies only if the venue system lacks them.
- Use `reference.bib` only if the venue explicitly asks for BibTeX source.

## Remaining Pre-Submission Edits

- Choose the target venue and journal style.
- Decide whether to cite Paper 1 as companion manuscript, preprint, or
  submitted companion once its external file name is fixed.
- Freeze theorem labels used in the Paper 1 import table.
- Decide whether the visible title should retain `theta-Expectations` or be
  changed to venue-preferred notation.
