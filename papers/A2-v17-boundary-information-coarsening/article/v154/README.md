# A2 revision 154 — referee entry

**Manuscript:** Finite failure schemes and the reconstruction of quadratic pencils.  
**Branch:** `revision/a2-v154-intrinsic-compactification-homological-fibres-2026-09-25`.  
**Controlling complete-materialized v153 report:** `52ebb8183433ad398f61958219b2af809f721824`.

Read [the complete PDF](geometry.pdf), [standalone LaTeX](geometry.tex), and [point-by-point response](RESPONSE_TO_V153_REPORT.md). These generated article files are published only after the native build has succeeded. A source-module commit alone is not a completed review object.

Part I adds the intrinsic polarization compatibility and projective coarse moduli completion, then the spectral divisor-fibre tower recovering Segre elementary divisors. Part II retains the normalization and conductor theorems and adds full squarefree Betti numbers, a uniform determinant-apolar quotient, and the whole first multivariate two-factor fibre's type and weighted resolution. The inherited relative, curve, recognition, rigidification and spectral arguments remain in the complete article. No earlier branch is modified.

Source modules: `front-v154.tex`, `moduli-v154.tex`, `homological-v154.tex`, `formal-details-v154.tex`, and `references-v154.tex`. `assemble_v154.py` uses the hash-locked complete v153 source, normalizes two historical label aliases in the new module, and retains every inherited mathematical block unchanged. The former opening text is archived separately; it is not silently lost.

Reproduce from the repository root:

```sh
D=papers/A2-v17-boundary-information-coarsening/article/v154
python3 "$D/check_v154.py"
python3 "$D/assemble_v154.py" --build
```

Dependencies: Python 3, SymPy, pdfLaTeX with AMS/Latin Modern/microtype/booktabs packages, and Poppler. The workflow installs them in an isolated Actions runner. See [build receipt](BUILD_RECEIPT_V154.json), [preservation audit](NONDELETION_V154.json), and [exact calculations](EXACT_CHECKS_V154.json).

The finite F22 calculation is exact computer-assisted algebra over the rationals. The general theorems are justified by the written proofs and identified classical inputs, not by finite testing. The four v153 check families are rerun; the older historical 28-check suite is not claimed as rerun. Ballico 1993 remains unavailable at theorem/proof level. The projective completion is a coarse GIT space, not a properness assertion for the full stack or a universal-algebra assertion on that coarse space.
