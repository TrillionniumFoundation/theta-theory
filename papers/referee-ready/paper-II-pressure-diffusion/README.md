# Paper II — referee revision v4

**Controlling source:** `main.tex`  
**Controlling bibliography:** `references.bib`  
**Round-four frozen copies:** `main-round4.tex`, `references-round4.bib`

Title: *Pressure, Physical Diffusion, and Uniform Full-Frequency Suspension Response for Moving Collision Systems*.

Build from this directory:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

The paper proves the common-space stabilization, physical pressure root,
symmetrized Green--Kubo identity, oriented renewal theorem, and two actual
full-frequency moving-family results:

1. an explicit Diophantine branch-roof theorem for the nonconjugate moving
   collision map;
2. a temporal-shear/Dolgopyat theorem for analytic no-eclipse moving open
   billiards.

It also proves the exact triangular Lorentz finite-horizon interval
`sqrt(3)/4 < r < 1/2`.
