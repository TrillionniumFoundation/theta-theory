# θ-Theory referee-ready five-paper series

This directory contains five standalone LaTeX manuscripts prepared for external
specialist review.  Each paper is self-contained at the level appropriate for a
companion-paper series: all assumptions used in the paper are restated, all new
arguments are proved in the paper, and any input from an earlier companion is
identified by title rather than by an internal repository token.

## Manuscripts

1. `paper-I-bilateral-response/`
   **Bilateral graph-current mixing and third-order response for systems with
   moving singularities**.
2. `paper-II-pressure-diffusion/`
   **Pressure, suspension resolvents, and physical diffusion under moving
   singularities**.
3. `paper-III-rough-theta/`
   **Doob-selected rough homogenization and nonlinear theta-expectations**.
4. `paper-IV-filtering-games/`
   **Filtering and Isaacs limits for partially observed deterministic
   multiscale games**.
5. `paper-V-representations/`
   **Representation theory for theta-expectations: BSDEs, PPDEs, and pathwise
   games**.

Each folder contains:

- `main.tex`: the referee manuscript;
- `references.bib`: a paper-specific bibliography;
- `README.md`: build instructions and a short scope statement;
- `REFEREE_GUIDE.md`: theorem map, dependency boundary, and suggested audit
  order.

## Build

From any paper folder:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

The manuscripts use `amsart` and standard TeX Live packages only.

## Author and disclosure metadata

The author metadata follows the existing repository manuscripts and must be
confirmed by the human authors before circulation.  The mathematical text is an
internal proof draft.  External peer review, novelty review, and bibliography
verification remain the responsibility of the human authors.  No structural
script or language model output is an external correctness certificate.
