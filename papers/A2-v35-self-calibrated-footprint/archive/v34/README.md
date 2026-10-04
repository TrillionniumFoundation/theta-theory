# A2 v34 — calibration experiments and fixed-footprint reconstruction

Qian Qi · 4 October 2026

**Primary article:** *Scalar collision laws and recognition of periodic dispersing billiards*, `main.tex`. The actual local build has 28 pages. This revision answers the latest v33 report at `3d825951afb2c2bd1da258de8648287c046cdc13`, which reviewed author head `245a2bf5d13b72d81ef85b784e9fcb2dd88ca490`. The title, scalar collision topic and requested Annals/Acta/Inventiones/JAMS target are retained.

## Main mathematical change

Theorem 1.4 (proved as Theorem 9.6) gives finite reconstruction under a fixed calibrated convex launch support K and an unknown stationary density j. The density may be biased and nonsymmetric; it is only required to satisfy the specified lower bound near the boundary of K. The controller sees pooled attempted collision bits, not the realized launch points, direct membership labels or the density. For s=6+beta and boundary-mass exponent gamma, its attempted-bit upper bound has power ((2gamma+3)s+1)/(s-2). At gamma=0 this is (3s+1)/(s-2). No optimality of this new power is asserted.

Lemma 9.1 identifies the positive components of the recovered occupation as C+(-K). Lemma 9.2 supplies a uniform overlap/mass lower bound. Proposition 9.3 gives a density-independent inverse modulus, including comparison of two different unknown stationary densities. Lemma 9.4 replaces a depth-linear error accumulation by the Green bound for exit from a fixed aperture. These yield the finite query, boundary reconstruction, footprint subtraction and primitive-period recognition.

Theorem 8.2 retains the adversarial bounded-error converse with explicit controller-uniform quantifiers (8.4). Its two admissible implementation maps need not agree. Corollary 9.7 shows why a fixed stochastic spread in the calibrated stationary model has no positive resolution floor. This is a distinction between two uncertainty classes for the same sensor, not a universal physical resolution law. Nominal position precision, footprint calibration, known smoothness and the positive nonperiod-patch margin remain explicit resources.

## One article; complete history preserved

The journal source package contains only `main.tex`, `references.tex` and the twelve active core files. All ten reviewed v33 proof chapters and all their result labels remain active. Six chapters are byte-identical; the others receive scope clarifications, the new overview or literature/architecture edits. No old theorem is replaced by a weaker theorem.

`archive/v33/` is the exact entire reviewed manuscript tree `213cecf77265c5ebea98791a99126b9def5d25f0`, including its nested historical volumes and previous evidence. This archive is repository history, not sixteen required journal supplements. The new primary proofs do not input or depend on it. `SUBMISSION_MAP.md` gives both reading routes.

## Reproduction and actual evidence

Requirements: Python 3.10+, mpmath, NumPy, SciPy and Shapely (for the retained suites), latexmk, amsart/Latin Modern/microtype and Poppler pdfinfo. From this directory run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_v34.py
# Exact checkout qualification (substitute the actual revision commit):
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_v34.py --require-checkout --expected-commit <COMMIT>
```

The actual local run passed 5,886 new finite diagnostics and 21 new publication-contract tests. It reran 117,772 retained v33 diagnostics plus 36 contract tests, and 11,647 retained v32 diagnostics plus 42 contract tests. Every ordinary/optimized pair agreed byte-for-byte. The 28-page primary has no final TeX warnings, unresolved references or overfull/underfull boxes. All rendered pages were inspected. The complete archived Git tree and the new mathematical/tool manifest were unchanged.

The local run is source-content execution, not a checkout of the new revision; its commit/run fields are null. The archived baseline was independently bound to the successful v33 hosted artifact, whose outer digest and native tree were verified. No old hosted receipt is relabelled as a v34 pass. The read-only v34 workflow must supply its own exact-SHA result. Local receipts are in `verification/local/`; hosted outputs are in the corresponding run artifact. Historical volumes are integrity-checked and selected suites rerun, not rebuilt or included in the one-article journal archive.

Finite diagnostics and compilation are not continuum proof certificates, physical apparatus tests, exhaustive priority claims or an editorial decision.
