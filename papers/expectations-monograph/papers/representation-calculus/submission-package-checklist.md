# Paper 3 Submission Package Checklist

Current package shape:

- Single manuscript: `main.tex`.
- Retained submission PDF: `representation-calculus.pdf`.
- Bibliography: `main.bbl`, generated from `../../reference.bib`.
- Planning/audit files kept out of the submitted package:
  `theorem-inventory.md`, `risk-register.md`, `execution-plan.md`,
  `extraction-checklist.md`, `compile-status.md`, and
  `referee-risk-memo.md`.

## Target Venue Posture

Default target family for Paper 3:

- Probability/stochastic-analysis framing: `SPA`, `AAP`, `EJP`.
- Control/PDE framing: `SICON` or adjacent PDE/control venues.
- Finance-facing framing: `Finance and Stochastics` after expanding the short
  robust-pricing/model-uncertainty stress illustration if needed.

Submission posture:

- Keep the paper explicitly downstream of Paper 2's HJB/theta-expectation
  theorem.
- Treat BSDE, calibrated diffusion, and Girsanov formulae as fixed-payoff
  representations, not as primitive derivations.
- Keep singular-billiard response and deterministic homogenization proofs out
  of Paper 3.
- Keep the `Z=\sigma^\top\nabla u` convention visible in the BSDE section.
- Keep the robust-pricing illustration as a calibrated stress test, not as a
  primitive market model.

## File Naming

Working source names:

- Source: `main.tex`.
- Bibliography file for source submission: `main.bbl`.

Submission-facing PDF:

- `representation-calculus.pdf`.

If source upload is required:

- Upload `main.tex` and `main.bbl`.
- If the venue requires BibTeX source instead of `.bbl`, copy
  `../../reference.bib` into the source bundle and adjust the bibliography path
  according to the venue instructions.

## Compile Commands

From `papers/representation-calculus/`:

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
```

## QA Gates

Before packaging:

- `representation-calculus.pdf` is built from `main.tex`.
- `main.bbl` is current and included in source-submission options.
- `main.log` and `main.blg` have no fatal errors.
- No undefined references or citations.
- No BibTeX warnings.
- No overfull boxes.
- `representation-calculus.pdf` page count is recorded.
- Retained submission PDF matches the latest checked build.
- Source scan has no internal source-line tags, workspace paths, extraction
  macros, or placeholder/process markers.
- BSDE/Girsanov/Cameron-Martin material appears only as downstream
  representation material, not as proof input for Paper 2.

Current checked state:

- `representation-calculus.pdf`: 6 pages, 286530 bytes.
- `main.tex`: 20375 bytes.
- `main.bbl`: 1433 bytes.
- SHA256 `representation-calculus.pdf`:
  `4cfa46f73edfce134c037b0e2963ca091d55a1ed89961638b4b9ddc03be6ade5`.
- Last clean check: 2026-07-09 07:39 Asia/Shanghai.
- Logs clean for fatal/error/undefined citation/reference/overfull/BibTeX
  warnings.
- Submission-facing scan over `main.tex` is clean for local process markers,
  master-source line tags, workspace paths, and extraction macros.

## Packaging Options

PDF-only submission:

- Upload `representation-calculus.pdf` as the manuscript.

Source submission:

- Upload `main.tex` and `main.bbl`.
- Include standard LaTeX dependencies only if the venue system lacks them.
- Use `reference.bib` only if the venue explicitly asks for BibTeX source.

## Remaining Pre-Submission Edits

- Choose probability/stochastic-analysis versus control/PDE framing.
- Decide whether to expand the robust-pricing/model-uncertainty example after
  a target venue is chosen.
- Decide how Paper 2 will be cited once its external preprint/submission name
  is fixed.
- Freeze the exact notation for theta-expectation in the title if the target
  venue dislikes lowercase Greek transliteration.
