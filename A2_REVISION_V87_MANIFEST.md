# A2 revision 87 — projective singular-spectrum theorem

**Revision branch:** `revision/a2-v87-gap-free-singular-quotient-2026-09-19`  
**Report base:** `18de3872c705b5be9582429567877aac8d1a5fbe`  
**Reviewed v86 source:** `bf67e3f33d394c80d7d7daeb51e52de12ec3d180`  
**Date:** 19 September 2026. Existing review/revision branches and the default branch are not rewritten.

## Referee entry points

| Purpose | Path |
| --- | --- |
| Principal article, *Action recovery from projective matrix curves* | `papers/A2-v17-boundary-information-coarsening/rigidity_v87.tex` |
| Self-contained principal source | `papers/A2-v17-boundary-information-coarsening/article/v87/paper.tex` |
| Complete preserved companion | `papers/A2-v17-boundary-information-coarsening/rigidity_v87_companion.tex` |
| New shared-calibration and proof supplements | `papers/A2-v17-boundary-information-coarsening/article/v87/legacy_clarifications.tex` |
| Point-by-point response to the corrected v86 report | `reviews/a2-v87-response-to-v86-2026-09-19/RESPONSE_TO_REFEREE.md` |
| Adversarial predecessor comparison | `reviews/a2-v87-response-to-v86-2026-09-19/LITERATURE_AUDIT.md` |
| Reproducible diagnostics | `papers/A2-v17-boundary-information-coarsening/verification/verify_v87.py` |
| Local source-bound diagnostics and actual native build | `verification/v87-local-verification.json`, `verification/v87-local-build.json`, relative to the paper directory |
| Branch-specific independent native build | `.github/workflows/a2-v87-manuscript.yml` |

The principal article is the renewed-review manuscript, not a wrapper that prepends another regime to v85. The companion is part of the revision package and retains every inherited mathematical input. Read principal Theorem 1.1 and its proof first, then sections 5–7, then companion section 19 for the requested proof details.

## Mathematical delta

For arbitrary fixed latent capacity and rectangular stochastic channels, the principal theorem gives a one-sided spectrum inverse against the closed model, without individual action gaps or a competitor rank floor. It separates the channel product kappa from the projective contrast gamma through theta = kappa gamma/(kappa+gamma). Maximization on exact fibres gives a representation-independent signal. The binary determinant law is a corollary on separated action/reference classes.

The exact two-clock fibre, its three-clock resolution, residual inference and matching singular families belong to one model. Both the weak-channel interaction and full-spectrum-collapse orders are attained; the lower bounds allow adaptive clocks. A separate sixteen-pattern shared-anchor certificate and six proof clarifications strengthen the preserved shared/meromorphic regimes.

## Preservation and build policy

The branch is based on the corrected report, not on a guessed default-branch version. No pre-existing source file is modified or deleted. The new companion directly includes the previous mathematical sources while bypassing the invalid digit-containing control sequences in the old wrappers. It also uses A1, A2, ... appendix numbering to accommodate more than 26 inherited sections.

Local verification checks 47 retained inherited TeX inputs, all 402 inherited cross-reference labels, and byte identity of all 1,764 files in the source archive for the reviewed v86 commit. The principal graph has 40 labels and eight bibliography keys; the companion graph has 408 labels and 45 bibliography keys. Both graphs have no missing/duplicate references or bibliography keys.

Local native output is ten pages for the principal and 122 pages for the companion, with no unresolved references/citations or overfull boxes in the final logs. Those are local build facts. Independent GitHub Actions status is read from the actual run and its `v87-native-*` records; this manifest does not substitute a prediction for a run result. Each native PDF hash belongs to its particular compiler run, not to a claim of cross-distribution bitwise PDF identity.

## Reproduction

From `papers/A2-v17-boundary-information-coarsening`:

```sh
python3 verification/verify_v87.py --base "$PWD" --output /tmp/v87-verification.json
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v87.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v87_companion.tex
```

NumPy, SymPy, a native LaTeX installation with the packages declared in the two frontmatters, latexmk and poppler-utils are sufficient. In a Git checkout, add `--review-base 18de3872c705b5be9582429567877aac8d1a5fbe` after fetching that commit to check additive-only changes. The optional `--archive` flag checks an extracted reviewed-source archive byte-for-byte.

The branch workflow stores its exact compiling commit in `verification/v87-native-source-commit.txt`, records independent source/diagnostic and PDF hashes, publishes build artifacts, and commits generated PDFs/evidence back only to this new revision branch when successful. Local evidence remains separately named. Symbolic/numerical/source diagnostics are not mathematical proof certification, and no editorial acceptance is inferred from a green build.
