# Compile Status: Paper 2 theta-expectation/HJB

- Last checked: 2026-07-09 16:31 CST
- Target: `main.tex` with `technical-appendix.tex`
- Command: three successful runs of
  `pdflatex -interaction=nonstopmode -halt-on-error main.tex` after merging the
  former technical proof details into appendices
- Output PDF retained for submission: `theta-expectation-hjb.pdf`
- PDF pages: 27
- PDF bytes: 482590
- SHA256:
  `c8c55404f9464029fd8f3f7454f4756d0daa465fe381b0187bffa1944a8c9cf7`

## Result

Paper 2 is now a single integrated article PDF.  `main.tex` carries the article
body and imports `technical-appendix.tex` before the bibliography.  There is no
separate technical appendix PDF in the active package.

## Log hygiene

- Undefined references: none found in the final log scan.
- Undefined citations: none found in the final log scan.
- Undefined control sequences: none found.
- Fatal errors: none found.
- Rerun warnings: none found after the final stability pass.
- Overfull boxes: none found.
- Remaining typography warnings: underfull boxes in compact theorem-map,
  imported-interface rows, and appendix tables.
- Submission-facing source scan over `main.tex` and `technical-appendix.tex` is
  clean for internal source-line tags, workspace paths, extraction macros,
  placeholder/process markers, and visible separate-package wording.

## Current scope

This file records the integrated article after adding:

- the corrector hierarchy;
- the deterministic residual identity with contact-jet freezing, scale
  cancellation, order-one split, and anisotropic residual bounds;
- the contact-frozen perturbed-test lemma;
- the sub/supersolution residual proof;
- the main homogenization proof using paired envelopes, comparison closure, and
  Liouville-a.e. identification;
- the comparison modulus and comparison/uniqueness theorem;
- the full doubled-variable comparison proof for the terminal-value HJB;
- a concrete finite-horizon triangular Lorentz cell;
- explicit smooth bump functions for the two deformation modes and observable;
- the dominance inequality for the nonconvexity coefficient;
- the Paper 2 bibliography/provenance pass for viscosity comparison,
  half-relaxed stability, perturbed-test homogenization, and nonlinear
  expectation terminology;
- integrated technical appendices with the finite-response micro-action ledger,
  endpoint-jet realization, endpoint reciprocity, exact prelimit action graph,
  specular endpoint variation, moving-boundary trace ledger, contact-frozen and
  recursive corrector hierarchy, branch residual constant ledger, full branch
  residual checks, four-scale residual identity, smooth approximation closure,
  half-relaxed viscosity passage, synchronized doubled-variable comparison,
  coefficient comparison ledger, Green-Kubo correlation Hilbert factorization,
  terminal-value stability, concrete nonconvex parameter window and recipe,
  dimensionless parameter audit table, normalized numerical certificate and
  stability margin, and nonconvexity/subadditivity algebra.
