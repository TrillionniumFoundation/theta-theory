# A2 revision 110

**Single-contact recovery of information metrics: sharp thresholds and native realization**

Principal source: `paper.tex` (self-contained amsart).
Controlling review commit: `87b63e155dac402ec6a9d0a34f69ff0ba5363fdb`.
Previous reviewed mathematical source: `60999f38f745072d240909fe8c77aee5be2df69a`.
Revision branch: `revision/a2-v110-sharp-threshold-native-realization-2026-09-21`.

The principal result replaces the old sufficient `k=3d+2` construction by the exact native threshold

`k_min(d)=d+ceil((3+sqrt(16d+1))/2)`, for d >= 2.

Read `RESPONSE_TO_R109.md` for the point-by-point changes and `DEPENDENCIES.md` for assumptions and preservation. The abstract rational maximal-rank theorem is classical and explicitly attributed; the native loading submersion, positivity and global fibre separation are proved here.

## Build

From this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error paper.tex
python3 checks.py --output checks-v110.json
```

From a full Git checkout, replay all three review volumes and their source-bound diagnostics:

```sh
python3 papers/A2-v17-boundary-information-coarsening/article/v110/verify.py
```

This also invokes the inherited v109 verifier, which builds the complete v109 and v108 companions and validates their preserved inputs. It needs latexmk, pdfLaTeX, the used LaTeX packages, pdfinfo and the Python dependencies of the inherited scripts. The new v110 checks use only the Python standard library.

For a principal-only source bundle with no Git history:

```sh
python3 verify.py --allow-partial
```

That command deliberately writes `evidence/local-verification.json`, not a full Git-bound receipt. The full command writes `evidence/verification.json` only after all steps pass. Inspect the receipt's `scope`, `source_bound`, `source_commit` and `run_url`; do not infer execution from this README or a queued workflow. Source and evidence commits are separate.

## Preserved companion volumes

The complete `../v109/paper.tex` and `../v108/paper.tex` plus all inherited dependencies remain unchanged. The v110 appendices preserve the corresponding operative statements without deleting the complete old proofs. The original Gaussian-contact experiment remains separate from the new categorical/observed-exposure sampling results.

## Diagnostic scope

The exact checks cover 499 integer threshold cases, 5,476 elementary restricted bases, exhaustive monomial impossibility at two equality thresholds, four globally separated integer loading witnesses at optimal k, independent compression of the raw inverse score matrix, and the rational nonorthogonal normalization identity. Full-rank certificates are nonzero minors modulo 1,000,003; they imply rational full rank for those instances. They do not prove the universal maximal-rank or realization theorem.
