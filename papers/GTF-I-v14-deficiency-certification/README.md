# General Theta Foundations I — v14

Full English intrinsic-deficiency revision with original-budget local testing certificates and active graph-residual realization. The parent is the already-published v13, not a reconstructed v11 or a replacement of another working branch. The controlling report remains the latest v12 report identified when work began.

## Manuscripts

`main.tex` builds the focused five-section article as `paper.pdf`. `development.tex` builds `complete-development.pdf`, retaining the full prior mathematics and introductions. All v13 canonical mathematical sections are imported unchanged. The new proofs are `local-certificates.tex` and `residual-certificates.tex`.

Read `RESPONSE_TO_REFEREE.md` for E12.1–E12.8 and technical comments 12.1–12.12; `PROOF_LEDGER.md` for hypotheses; `PRESERVATION_DIFF.md` for the exact preservation map. `HISTORY_AUDIT.md`, `PIPELINE_GRAPH.json` and `REPOSITORY_SNAPSHOT.json` distinguish historical derivation, actual mathematical edges and a frozen remote observation. The full-original Norberg/Paull–Unger priority audit remains unresolved, as `LITERATURE_COMPARISON.md` states.

## Reproduce the source-bound build

From the repository root, with Python 3.12 and LaTeX installed:

```sh
python -m pip install -r papers/GTF-I-v14-deficiency-certification/requirements.txt
# Debian/Ubuntu: texlive-latex-extra texlive-fonts-recommended lmodern poppler-utils
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python papers/GTF-I-v14-deficiency-certification/build.py
```

The build identifies its actual checkout, checks all pinned source files, compiles both views to stable labels, runs the new and inherited diagnostics, checks all 717 predecessor labels and archives the entire source closure. Local extracted-archive runs are identified as local; they do not claim a remote commit. The dedicated workflow publishes only to the v14 work branch.

## Exact local certificate tool

`certify.py` accepts rational separately affine tests on stochastic rows. Each JSON test has `terms`, a list of `[coefficient, [[row, coordinate], ...]]`; coefficients are exact rational strings. A monomial may use at most one coordinate from each row. The input `row_sizes` fixes the original row alphabets. The code rejects non-stochastic upper witnesses, missing covering cells, incorrect vertex inequalities and modified input hashes.

```sh
python papers/GTF-I-v14-deficiency-certification/certify.py make input.json certificate.json --mesh 4
python papers/GTF-I-v14-deficiency-certification/certify.py check input.json certificate.json
```

The checker independently enumerates the entire cover and evaluates every required rational vertex inequality. Explicit enumeration limits fail rather than silently emitting a partial certificate. `verify.py` generates four concrete certificates, inputs and checked results in `evidence/LOCAL_CERTIFICATES.json`; the two-symbol delayed identity has exact private width-one deficiency 1/2. The non-dyadic bilinear example illustrates convergent, not necessarily finite exact, endpoints.

This program verifies a supplied polynomial problem; compiling a physical process into the complete test family is a separate modeling step. It does not implement real quantifier elimination, automatically certify physical Gram integrals, or prove the general analytic theorems. The matrix experiments in `verify.py` are floating-point regressions explicitly separated from the exact rational certificate checks.

## Review status

The proofs are offered for renewed independent review. A successful build, correct example certificate, or source hash is not an independent analytic proof certificate or journal acceptance. No full historical kinetic target is claimed closed by the new linear microscopic residual bound.
