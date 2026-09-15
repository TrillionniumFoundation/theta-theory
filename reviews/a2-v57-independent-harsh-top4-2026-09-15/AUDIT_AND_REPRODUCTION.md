# A2 v57: independent audit and reproduction ledger

Date: September 15, 2026. This ledger supports `REFEREE_REPORT.md`; it is not a mathematical proof certificate or a commissioned journal decision.

## 1. Acquisition and immutable source identity

The latest identified review-ready revision was A2 v57. The new review branch starts at `bd6c4f04cbdf5a306653098c9840dca2b4989e7a`, the head of `revision/a2-v57-review-ready-2026-09-15`. The actual compiled source is `e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6`.

The authorized GitHub connector downloaded native workflow artifact **10393060381**, run **34959437980**, attempt **1**. The outer artifact ZIP has SHA-256:

`45b4a5525012e4323fc5940b61304c949b7f2a968cfa5bf597a2dd97cfe80186`

Its `native-source.zip` has SHA-256:

`dc12048b3c70aa5a95be1b6f56ada157b0908481ed90d22069d68ed4861c9dd8`

GitHub's Git-tree endpoint was independently queried using the compiled commit and manuscript path:

`https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/trees/e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6:papers/A2-v17-boundary-information-coarsening`

It resolved to **`1c11e890bdd5a96381b9a803ade7588eff5c04b9`**. Reconstructing the tree from every archived source file, its Git blob identity, path and manifest mode gives the same SHA. The source identity is not inferred from the directory's historical v17 name or from the workflow preparation commit.

The same native products are retained in the reviewed repository under `deliveries/a2-v57/e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6/`.

## 2. Independent source and build checks

`verify_delivery.py` checks all 679 frozen files by byte length, SHA-256 and Git blob hash, checks the archive's manifest against the delivered manifest, reconstructs the manuscript tree, checks the active-manifest entries against those frozen files, and verifies 45 build-report evidence entries. The active manifests contain 110 main, 41 principal and one companion input, with 120 distinct paths. These counts are manifest counts, not an independent theorem count or a claim to have semantically resolved every TeX dependency.

The script was written for this review. It imports no author's checker. Its default source check is pinned to the compiled v57 commit. Its explicit exceptions continue to operate under optimized Python.

Fresh complete builds used:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
  -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' ENTRY.tex
```

The order was `two_collision`, `main`, then `rigidity`. All three builds completed successfully. The generated results are in `DELIVERY_VERIFICATION.json`.

| Entry | Pages | Text mismatch pages | 72-dpi RGB mismatch pages | PDF byte identity |
|---|---:|---:|---:|---|
| Companion | 7 | 0 | 0 | No |
| Full manuscript | 283 | 0 | 0 | No |
| Principal article | 106 | 0 | 0 | No |

The comparison uses the same local renderer for both native and rebuilt PDFs. It compares every page's extracted text, image dimensions and RGB samples. It does not claim byte-identical PDFs or cross-renderer invariance.

The checked log patterns returned no undefined-reference, undefined-citation, missing-character, overfull-box or LaTeX-error matches. There was one principal underfull-vbox notice and three full-manuscript notices; the companion had none. Those notices are retained in the result rather than silently labelled a warning-free build.

Actual visual inspection was limited to principal pages 3, 19, 44, 87 and 99, and full page 192. The sampled text and formulas were readable without observed clipping. All-page computational equality is not all-page visual inspection.

## 3. Independent finite mathematical controls

`check_local_mechanisms.py` uses exact rational arithmetic and symbolic calculations. It checks 750 geometrically admissible last-jet blocks at orders 3 through 32; determinant, inverse, a uniform infinity-norm bound, exponential approach to the identity, and endpoint/interior geometric-series multiplicities are tested. It also checks signed four-density recovery with a nonzero cubic term, the mixed log derivative, the fourth graph/support coefficient, the area-preserving family's first area derivatives and quartic information coefficient, a determinant-six gain matrix, and 30 pilot-grid configurations.

The polynomial density is an algebraic diagnostic, not an asserted billiard realization. The rational gain-matrix example is a cochain control, not an additional realized table. General proofs and their scope are stated in the referee report, not inferred from finitely many checks.

The ordinary and optimized runs produced byte-identical JSON. The result is `INDEPENDENT_CHECKS.json`.

## 4. Reproduction

Extract the native workflow artifact into a directory called `artifact`. Use a fresh output directory: the source verifier refuses to overwrite an existing `rebuild` directory. With Python, SymPy, PyMuPDF, latexmk and the required TeX packages available, run:

```sh
mkdir -p audit-run
python verify_delivery.py artifact --rebuild \
  --output audit-run/DELIVERY_VERIFICATION.json
python check_local_mechanisms.py --output audit-run/INDEPENDENT_CHECKS.json
python -O check_local_mechanisms.py > audit-run/INDEPENDENT_CHECKS_OPTIMIZED.json
cmp audit-run/INDEPENDENT_CHECKS.json audit-run/INDEPENDENT_CHECKS_OPTIMIZED.json
```

The environment used here was Python 3.13.5, SymPy 1.14.0, PyMuPDF 1.26.7, latexmk 4.86, and pdfTeX 1.40.26 from TeX Live 2025/dev/Debian. Reproduction does not require network access once the artifact and dependencies are present. The build script emits the three full build logs beside its output JSON.

SHA-256 values of the executed local scripts and resulting JSON:

| File | SHA-256 |
|---|---|
| `verify_delivery.py` | `64b2f2996bf7c1f6968db3e08fa2ce1364d1caf16f2d34bd9c30f925eadd4c3c` |
| `check_local_mechanisms.py` | `ada1b1cb787ca7c5fd498aec0098cf65fee5cd1a7cf574568312245b67cb7be6` |
| `DELIVERY_VERIFICATION.json` | `7d35319e9ac44c439340d6db927c882a4cc6a3e040a325b14fb00a42502284fb` |
| `INDEPENDENT_CHECKS.json` | `45e54479ddecd76784752f022f6599c92ecee09590ba77a57565873aefd31e1f` |

## 5. Mathematical scope and repository scope

The report's source keys identify the fresh mathematical reading. The expanded acquisition audit concerns the common-record calibration, the direct physical capped-estimation argument and the increasing-order compact-inverse construction. It does not freshly certify the entire earlier complete-transcript comparison theory. The separate two-table example and the full companion mathematics are not newly certified here. Neither a passing finite script nor a rebuilt PDF proves trace-class estimates, all-order smooth factorization, analytic continuation, probability bounds or global rigidity.

Only new files in `reviews/a2-v57-independent-harsh-top4-2026-09-15/` are intended to be added on the new review branch. The revision source, native products, old reports, A1, default branch, permissions, protections and unrelated workstreams are not edited by this review. No merge or pull-request approval is part of this delivery.
