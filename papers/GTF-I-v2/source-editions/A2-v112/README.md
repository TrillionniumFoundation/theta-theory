# A2 revision 112

**Recovery of information metrics: multiplication failure schemes**

Principal manuscript: `paper.tex` (29 pages in the local native build). Its complete inputs are the six files in `parts/` and `references.tex`. The mathematical source contains no review-process narrative.

Revision branch: `revision/a2-v112-components-schemes-quantitative-experiments-2026-09-21`.
Controlling report: `reviews/a2-v111-independent-harsh-top4-2026-09-21/REFEREE_REPORT.md`, commit `cafc6c1bd403dae4acc66177fb43feee54c02b1d`.
Reviewed v111 mathematical source: `1e21bcbe1741c9fb67a8b3fabe0f6bc20cfdb559`; reviewed head `f7c55b929c8750a98c9219803863e746968a423d`.

## Mathematical changes

Theorem 5.1 supplies a structural theory in the additional range c >= 8, k >= 2c+1, L*c*(c+1)/2 >= 2k-1. Writing a=L*c*(c+1)/2-2k+2 and b=L*c-3:

- a<b: the entire maximal-minor scheme is integral and Cohen--Macaulay, with a nondegenerate-Hankel principal component.
- a=b: it is reduced and Cohen--Macaulay with precisely 1+2^(L-1) components, one nondegenerate and the others signed secant varieties.
- b<a: exactly 2^(L-1) maximal-dimensional components, all rational signed secant varieties, generically corank one and scheme-smooth. No classification of smaller or embedded excess components is asserted.

The residual multiplication identity explains the wall and proves generic scheme smoothness. The expected-codimension cycle is computed by the classical determinantal formula. Real native strata give local conditioning exponents. The original full-range codimension theorem and sharp native threshold are preserved.

Lemma 10.1 proves an explicit O(N^(-1/5)) jittered-Poisson total-variation bound. Theorem 10.3 supplies a deterministic finite-precision score protocol with two-sided Le Cam error O(N^(-1/5) + 1/(sqrt(N)*eta) + eta). Proposition 10.4 identifies the full exposure tangent model's nuisance quotient. Known marks, local centring and nuisance scope remain explicit.

Read `RESPONSE_TO_R111.md` for all 34 detailed comments, `LITERATURE_AUDIT.md` for the examined primary literature and priority scope, and `PRESERVATION_AND_DEPENDENCIES.md` for the dependency graph and historical preservation.

## Build

Local principal-only check (requires the sibling v111 sources, SymPy, latexmk, pdfLaTeX and pdfinfo):

```sh
python3 build_review.py --local
```

Full repository source-bound check:

```sh
python3 papers/A2-v17-boundary-information-coarsening/article/v112/build_review.py
```

The full check verifies additions-only relative to the exact R111 review commit, pins the inherited v111/v110/v109/v108/v104 source blobs, checks all 68 inherited labels and three byte-identical mathematical parts, reruns the inherited diagnostics, checks strict endpoint gaps and signed-incidence tangent examples, and compiles v112 with unchanged v111/v110/v109/v108 companions. A receipt is written only after successful execution. Principal undefined references, duplicate labels, and overfull boxes cause failure.

`evidence/local-receipt.json` is principal-only evidence and must not be substituted for `evidence/ci-receipt.json`. The latter binds the mathematical source commit, input hashes, workflow run and five compiled volumes. The later bot commit contains generated evidence only. A workflow definition alone is not a successful build.

Finite arithmetic diagnostics and a clean build are not formal verification of the universal theorems, a priority certificate, or a prediction of an editorial decision. The theorem proofs are in the article; the scope of each stronger conclusion is stated in its hypotheses.
