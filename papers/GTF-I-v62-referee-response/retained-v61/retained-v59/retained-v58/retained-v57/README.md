# General Theta Foundations I — Revision 57

**Stochastic Realization, Finite Quotients, and Uniform Orbit Geometry**

This continuation starts from already published v56 `5c3b3fb9ab878748f58462e065850d0a5cbbc2f6` and responds to the latest located v55/r37 report. The earlier v56 structural results are inherited and preserved, not represented as newly created here.

## Reading order

Read `paper.pdf` / `main.tex`, then `RESPONSE_TO_REFEREE.md`. The opening theorem map separates stationary, clocked, boundary, quantitative and finite-encoding assumptions. Sections `16-uniform-orbits.tex`, `17-matrix-orbits.tex`, `18-extreme-endpoint.tex`, and `19-positive-precision.tex` contain the new proofs. Compiled theorem numbers and pages are in `evidence/THEOREM_LOCATIONS.json`.

The general orbit theorem distinguishes all-centroid small-ball exponents from target-orbit dimension. Full legal density-matrix outputs in SU(d) have near-matching width exponent d-1, with an exact positive upper realization at strict amplitude. At pure amplitude a fixed algebraic free alphabet and a specified transcendental seed have exact width 2*3^N-1, whereas every fixed positive subcritical error has polynomial width. The exact orbit-profile theorem is elementary and independent of spectral gap. A Gram-factor compiler supplies rational PSD decoders and explicit precision/fair-bit bounds for supplied encoded machines.

## Preservation and reproduction

`retained-v56/` contains all 145 predecessor native files byte-for-byte, including all nested history. Every predecessor active mathematical label remains in the main article. The builder produces the new article and six retained documents; none is a hidden forward dependency of an omitted new proof.

Dependencies: Python 3.11, SymPy 1.14.0, PyMuPDF 1.26.7, and a LaTeX installation containing amsart, lmodern, microtype and the packages in `main.tex`.

```
python check_revision.py
python -O check_revision.py
python build.py --check-isolated
```

`evidence/BUILD_RECEIPT.json` records the actual source commit, finite assertion counts, seven PDF checks and the independent native-only rebuild. `evidence/CORE_SOURCES.zip` rebuilds without repository or network access once dependencies are installed. `evidence/REFEREE_PACKAGE.zip` includes all PDFs, source archive, response, audits and evidence.

Finite regression does not certify universal theorems, spectral gap, matrix freeness, external priority or journal acceptance. The logarithmic nonabelian gap, legal decoder restrictions, transcendental seed, and distinction from a scalar exact endpoint are explicit. Independent A/B/C/D pipeline closure flags remain false.
