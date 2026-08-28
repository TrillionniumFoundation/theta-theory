# Paper III — referee revision v4

**Controlling source:** `main.tex`  
**Controlling bibliography:** `references.bib`  
**Round-four frozen copies:** `main-round4.tex`, `references-round4.bib`

Title: *Exact-Innovation Rough Homogenization and Microscopic Construction of Theta-Semigroups from Nonconjugate Collision Dynamics*.

Build from this directory:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

The paper uses the same nonconjugate moving collision map as Papers I--II.  It
proves exact predictable innovations, the canonical geometric enhanced
martingale limit, endogenous state-dependent homogenization, a pointwise
microscopic entropic DPP, a controlled risk-sensitive HJB limit, and forward
theta-independence.

No response derivative is substituted for an invariance principle, and no
anisotropic pairing is upgraded to point evaluation.
