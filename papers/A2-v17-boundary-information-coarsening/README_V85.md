# A2 v85 — Action rigidity from selective observations

Author: Qian Qi. Revision date: September 18, 2026.

Branch: `revision/a2-v85-finite-noisy-geometric-rigidity-2026-09-18`.

## Manuscript for renewed review

The principal submission is **[rigidity_v85.tex](rigidity_v85.tex)**. The title, abstract, introduction and new proofs are in [article/v85](article/v85). It uses one canonical [principal body](article/v85/principal_body.tex).

The **[expanded edition](rigidity_v85_full.tex)** contains that identical principal body followed by every companion input retained in the v84 expanded edition. It preserves the historical derivations, rather than serving as a second principal submission.

The **[response to the referee](RESPONSE_TO_REFEREE_V85.md)** answers major comments M1–M10 and technical comments T1–T15, with theorem-level locations. It states which results are new, which classical ingredients are used, and which observation assumptions each conclusion retains.

## Controlling versions

The revision answers `reviews/a2-v84-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md` at review commit **`372f5235c3fad2c5a9734bb7649261de207dbf1b`**. The reviewed v84 manuscript is at **`b3da64f38742459620d624ea9a565abb3550aba9`**, on `revision/a2-v84-secant-detector-space-2026-09-18`.

The new branch starts from the review commit, not from an older revision or an unrelated default-branch state. Thus the report and reviewed source remain in its ancestry. The remote comparison from that review commit through source-and-workflow commit `7d0e32dc065466a35006b4338c0560fd62a2bcc4` contains only added files and zero deletions. No v84 or historical source file was changed. The new introduction retains the preceding sharp action statements and proofs; the other principal modules are included unchanged. All previous companion inputs remain in the expanded edition.

## Main mathematical changes

| Result | Proof location |
|---|---|
| Finite classification of regularly separating rational-derivative detector spaces by integer-residue and double-pole tests; maximal admissible enlargements under principal-part closure; uniform pole-budget clock designs | [07_polar_structure.tex](article/v85/07_polar_structure.tex), `thm:v85-polar`, `cor:v85-maximal`, `thm:v85-budget` |
| Finite-record action confidence sets valid even at singular channels, without an inverse constant or supplied channel signal floor; explicit finite-grid realization | [08_confidence_sets.tex](article/v85/08_confidence_sets.tex), `thm:v85-confidence`, `prop:v85-grid` |
| Finite noisy boundary observations yield a C2 metric certificate after a boundary-fixing pullback; endpoint-dependent unknown reference delays and arbitrary nuisance variation between sampled sites are allowed | [09_finite_geometry.tex](article/v85/09_finite_geometry.tex), `thm:v85-geometric` |
| Matching parametric geometric risk bounds and a genuine metric realization of the missing-clock ambiguity, establishing the sharp q+3 clock threshold for the variable-reference class | [10_sharp_geometric_experiments.tex](article/v85/10_sharp_geometric_experiments.tex), `thm:v85-parametric-risk`, `thm:v85-geometric-clock` |
| Fixed raw-attempt budgets with failures and observed acceptance counts; closed compact classes and the precise inverse modulus for the inherited covering theorem | [11_raw_acquisition.tex](article/v85/11_raw_acquisition.tex), `thm:v85-raw` |

The integrated argument is

`finite categorical records -> action confidence intervals -> boundary-distance constraints -> uniform boundary-distance error -> C2 metric error modulo boundary-fixing diffeomorphisms`.

If `w_h` is the largest observed action-interval width on a boundary mesh of diameter `h`, the metric certificate is `C_geom (w_h + 2 L h)^mu`. Its geometric input is the stated local stability theorem of Stefanov–Uhlmann, with the s-injective reference, neighbourhood and high-regularity bounds explicit. The original exact continuum theorem for all simple surfaces and a constant reference arm remains unchanged. The new finite noisy theorem does not claim that local metric stability has been proved for an unrestricted geometric class.

The finite-dimensional geometric prior has matching mean squared parameter risk of order `N^{-1}`. The full boundary-mesh rate is a sufficient upper rate, not labelled nonparametric minimax. The clock lower bound uses actual scaled simple metrics with endpoint-dependent reference delays; it is not asserted for the smaller constant-reference class. These distinctions identify the mathematical content of the results rather than weakening the inherited conclusions.

## Historical and literature dependencies

The revision uses the v84 complete polynomial fibre, exact scalar and spectral inverses, compact inverse construction, covering recovery, observed return domains and boundary-distance reduction. It also revisits the v79 action-risk and raw-preparation-cost arguments; in particular retained readout counts and all raw attempts are not conflated. The v77–v82 companion modules remain available with their original apparatus and regularity assumptions.

The added theorem-level comparisons cover Sontag's analytic experiment-count theory, Alberti–Santacesaria's finite-measurement inverse theory, Ling–Strohmer's bilinear self-calibration, Nguyen–Zhang's permutation-synchronization experiment, and Stefanov–Uhlmann's boundary-distance stability. Bibliographic metadata and the geometric theorem statement were checked against primary author, publisher or preprint sources. Classical observable-operator, Chebyshev, Prony, covering-space and exact-lift ingredients remain attributed. The paper does not claim new general tensor decomposition or a new proof of the cited boundary-rigidity theorem.

## Verification actually completed

[verification/verify_v85.py](verification/verify_v85.py) was executed locally with `--algebra-only`. Its actual output is [verification/v85_algebra_checks.json](verification/v85_algebra_checks.json). The checked script has SHA-256 `5becdebbfb0dce64a1fce7d0d205a389fcedf17e49bc3bc97d4e2e7542858767`.

The run passed the 54-charge construction, all 256 saturated-space masks on the four-pole test set, a nonsaturated-space check, the geometric scaling-fibre construction for q = 0, 1, 2, 4, 200 forward-model checks, and a nonsingular finite geometric design. In the fibre checks the largest scalar residual was approximately `3.56e-15`, and the largest projective-matrix residual was approximately `3.34e-16`. The extra clock distinguished all tested alternatives. These finite checks guard formulas and constructions; they do not certify the universal theorems or replace the proofs.

The remote additive comparison described above has also been checked. The script's complete input-graph, label, bibliography and mathematical-block preservation mode is provided for execution in a full checkout. **That full source-check mode and the two native TeX builds had not completed at the time this README was committed. No successful v85 PDF build, rendered-page inspection, or passed CI result is claimed here.** The initially triggered source-export job was still queued with no artifact. Native build results must be read from the actual workflow logs and artifacts, not inferred from the existence of the workflow file or this manuscript.

## Reproduction

From this directory, with Python 3.10 or later, NumPy, SciPy, TeX Live and latexmk installed:

```sh
python3 verification/verify_v85.py --base "$PWD" --output verification/v85_full_checks.json
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v85.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v85_full.tex
```

The full check validates principal inputs, labels and citation keys, verifies preservation of the old mathematical blocks in the rewritten introductory module, and verifies all inherited companion inputs. It records source hashes. The branch-specific workflow `.github/workflows/a2-v85-manuscript.yml` performs these checks before building both editions and rejects unresolved references or citations. Its artifact includes the exact source commit, sources, validation output and available native logs. Only a successful native build writes the PDFs back to this revision branch. Neither compilation nor the finite test output is a claim of independent mathematical approval.
