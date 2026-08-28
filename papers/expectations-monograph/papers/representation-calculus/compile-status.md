# Compile Status: Paper 3 representation calculus

- Last checked: 2026-07-09 07:39 CST
- Target: `main.tex`
- Command: `main.bbl` unchanged from the previous clean BibTeX build;
  `pdflatex -interaction=nonstopmode -halt-on-error main.tex` run twice after
  the sign/application pass
- Output PDF retained for submission: `representation-calculus.pdf`
- PDF pages: 6
- PDF bytes: 286530
- SHA256:
  `4cfa46f73edfce134c037b0e2963ca091d55a1ed89961638b4b9ddc03be6ade5`

## Result

The Paper 3 representation-calculus draft compiles as a single article with
bibliography.

## Log hygiene

- Undefined references: none found in the final log scan.
- Undefined citations: none found in the final log scan.
- Undefined control sequences: none found.
- Fatal errors: none found.
- LaTeX errors: none found.
- BibTeX warnings: none found after changing `PardouxPeng1992` to an
  `@incollection` entry in `../../reference.bib`.
- Overfull boxes: none found.
- Submission-facing source scan over `main.tex` is clean for internal
  source-line tags, workspace paths, extraction macros, and placeholder/process
  markers.

## Current scope

This is a representation-calculus draft.  It states the dependency on Paper 2,
fixes the linearity obstruction, gives the payoff-calibrated linearization, and
records the calibrated diffusion, BSDE, and semigroup-level Girsanov
statements.  It now also includes a representation-window assumption, a
gradient-versus-BSDE-integrand lemma, a post-derivation calibration guardrail,
a terminal-value sign-convention ledger, a short robust-pricing stress
illustration, a journal-facing theorem map, and a standard stochastic-analysis
bibliography.  It now also has a submission package checklist,
referee-risk memo, and retained submission PDF.  Final venue-specific
positioning remains future work.
