# A2 revision 88 — referee re-review entry point

**Branch:** `revision/a2-v88-projective-polynomial-rigidity-2026-09-19`  
**Review baseline:** `976d23ef269126e68dd90c4c9d3184ee67ff0b54`  
**Reviewed v87 source:** `4304524ff671bf1ff57217b3d288923405c7ca03`  
**Author:** Qian Qi  
**Title:** *Projective polynomial observations: normalization, spectrum, and singular inference*.

## Manuscript

The self-contained principal article is `papers/A2-v17-boundary-information-coarsening/rigidity_v88.tex`. It inputs `article/v88/paper.tex`, `polynomial.tex`, `residues.tex`, `algorithm.tex`, `statistics.tex`, `relations.tex`, and `references.tex` under the same manuscript directory. The local native output is 16 pages. This source commit does not claim that a compiled PDF has already been committed by GitHub Actions; the workflow records that separately when it actually runs.

## Mathematical changes

Theorem 1.1 gives the degree-d normalization operator, the gcd/nullity characterization, positive normalization fibres, a sharp worst-case 2d+1 clock count, and an additive one-sided spectral modulus. Theorem 3.2 gives an observable inverse-pencil residue condition, its zero set and semicontinuity, and a stronger affine inverse. Theorem 4.1 constructs a direct estimator with that modulus. Theorems 5.2 and 5.4 give honest inference and sharp risk/diameter orders on the observable signal classes, including adaptive-design lower bounds. The affine results of v87 remain explicit consequences or retained constructions, not discarded cases.

## Response and audit

Read `reviews/a2-v88-response-to-v87-2026-09-19/RESPONSE_TO_REFEREE.md` for the point-by-point response, `LITERATURE_AUDIT.md` for the closest-predecessor comparison, and `PRESERVATION_AND_SUBMISSION_BOUNDARY.md` for the old-to-new theorem map. Every inherited path is unchanged. The historical companion remains available but is not a proof dependency of the principal article.

## Reproduction

From `papers/A2-v17-boundary-information-coarsening/`:

```sh
python3 verification/verify_v88.py --review-base 976d23ef269126e68dd90c4c9d3184ee67ff0b54 --output /tmp/a2-v88-verification.json
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v88.tex
```

Python requires NumPy and SymPy. Native compilation requires AMS/Latin Modern/microtype/mathtools/hyperref and latexmk; the new branch-specific workflow installs the corresponding TeX Live packages. `verification/reconstruct_v88.py` is the executable point estimator; it does not compute the global residual confidence region.

Actual local evidence is in `verification/v88-local-verification.json` and `verification/v88-local-build.json`. The latter binds the build to exact Git blob and SHA-256 source digests, and records the PDF and log hashes. These records state explicitly which preservation check was not run in the manuscript-only local workspace. The workflow `.github/workflows/a2-v88-manuscript.yml` independently checks preservation, recompiles, uploads diagnostics, and commits its generated PDF and source-pinned build evidence to this revision branch on success.

The local build has no unresolved citations/references, duplicate labels or overfull boxes; all 16 rendered pages were inspected. Symbolic and numerical diagnostics are finite checks, not formal proof certification. Independent mathematical and editorial review remains the purpose of this branch. Nothing here merges the revision into the default branch or declares an acceptance decision.
