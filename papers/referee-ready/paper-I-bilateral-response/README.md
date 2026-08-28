# Paper I — referee revision v4

**Controlling source:** `main.tex`  
**Controlling bibliography:** `references.bib`  
**Round-four frozen copies:** `main-round4.tex`, `references-round4.bib`

Title: *Bilateral Response, Symbolic Desingularization, and All-Order Spectral Jets for Nonconjugate Moving Collision Dynamics*.

Build from this directory:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

The paper has two positive actual classes:

1. an explicit nonconjugate symplectic Markov collision map with all-order
   moving-seam response, arbitrary-source susceptibility, and exact
   predictable innovations;
2. analytic no-eclipse open dispersing billiards, treated on a fixed symbolic
   space by symbolic desingularization.

The controlling theorem does not use differentiated invariance, exact
coboundaries, an assembly reset, or the old S1--S3 certificates.
