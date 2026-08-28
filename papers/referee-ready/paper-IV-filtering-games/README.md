# Paper IV — referee revision v4

**Controlling source:** `main.tex`  
**Controlling bibliography:** `references.bib`  
**Round-four frozen copies:** `main-round4.tex`, `references-round4.bib`

Title: *Noncompact Filtering, Curvature-Compensated Pure Isaacs Games, and Deterministic Multiscale Limits*.

Build from this directory:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

The paper proves a genuinely noncompact refresh--autoregressive filter with
strict posterior contraction and an invariant moment ball.  It introduces a
curvature-compensation variational inequality that forces a unique pure saddle
on closed convex, possibly noncompact controls.  Lower and upper collision-game
schemes converge separately to the same pure Isaacs value, followed by a
continuous-time feedback verification.

The nonconvex Hamiltonian is computed from the actuator-energy saddle; it is
not inserted as a primitive polynomial.
