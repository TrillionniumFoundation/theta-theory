# General Theta Foundations I — Revision 94, R60 response

**Primary manuscript:** *Finite-Use Discrimination Geometry of Ordered Quantum Measurements*.

**Current directory:** [`papers/GTF-I-v94-spectral-value`](papers/GTF-I-v94-spectral-value).

The controlling external report is v90/R60 at `cf13712c54e9ef0c9c54a240b1f26efc78cc3568`, with companion proof/pipeline audit `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. Both are frozen verbatim in the current directory. The immediate published predecessor is v93, `3b660839818d6ef676da72fb6e9969501be4e59a`, not v90. This revision retains the paper's topic and four-leading-general-mathematics-journal objective and continues the already published v91–v93 response.

## Manuscripts and first reading

| Object | File | Pages | Role |
|---|---|---:|---|
| Primary | [paper.pdf](papers/GTF-I-v94-spectral-value/paper.pdf) | 78 | Current article; start here |
| Current linked supplement | [BINARY_SUPPLEMENT.pdf](papers/GTF-I-v94-spectral-value/BINARY_SUPPLEMENT.pdf) | 87 | Dependency proofs and auxiliary results |
| Independent structural article | [STRUCTURAL_PAPER.pdf](papers/GTF-I-v94-spectral-value/STRUCTURAL_PAPER.pdf) | 41 | Unchanged active structural source |
| Complete research edition | [COMPLETE_REVISION.pdf](papers/GTF-I-v94-spectral-value/COMPLETE_REVISION.pdf) | 289 | Full mathematical archive, not a second submission |

The [point-by-point response](papers/GTF-I-v94-spectral-value/RESPONSE_TO_REFEREE.md) covers R01–R15 and D01–D30 and distinguishes the inherited v93 arguments from the new Section 20. The [derivation map](papers/GTF-I-v94-spectral-value/PIPELINE_DERIVATION_V94.md), [history audit](papers/GTF-I-v94-spectral-value/HISTORY_AND_PIPELINE_AUDIT.md), and [primary-source comparisons](papers/GTF-I-v94-spectral-value/LITERATURE_AUDIT.md) give the dependency and literature routes.

## New mathematical result and printed locations

The predecessor identified which initial Grams attain a resource bound. Revision 94 evaluates the entire prescribed-initial spectrum for the specified biased shared-basis experiment. It holds the first acquisition pure and fixed, derives the rank-constrained fresh optimizer rather than assuming it uniform, evaluates the rank-capped concave envelope, and constructs an attaining instrument on the actual initial Schmidt support.

| Printed result | Visible heading page | Content |
|---|---:|---|
| Theorem 20.1 | 65 | Exact value at every prescribed pure initial Gram |
| Lemma 20.2 | 66 | Secular concavity and strict Schur concavity |
| Lemma 20.3 | 66 | Rank-constrained fresh-Gram optimization, including singular supports |
| Lemma 20.4 | 67 | Evaluation of rank-capped spectral envelopes; at most d commuting atoms |
| Corollary 20.5 | 69 | Exact no-message value and necessary/sufficient strict-message criterion |
| Corollary 20.6 | 69 | Exact spectral deficit and initial-rank saturation; statement continues on page 70 |

These are heading pages extracted from and visually checked in the submitted `paper.pdf`, not guessed from auxiliary anchors. All of the new proofs on pages 65–70 and the cover were rendered and inspected. Source module `sections/87-exact-initial-spectral-values.tex` compiles as Primary Section 20.

With `L=2(d+1)-t^2`, `p_E=(d+1)/L`, and `r=min(k,ell)`, the value is

```
P^b_{k,ell}(rho) = p_E + t^2 H_r(rho)/(2L),
H_r(rho) = chi(q^(r)(lambda(rho))),
chi(u) = lambda_max(sqrt(u)sqrt(u)^* - diag(u)).
```

Here `q^(r)` is the least rank-r majorant defined in (20.3). The optimum is realized with at most d receiver outcomes, using the same instrument after every device label. No classically resolved replacement of the initial pure acquisition is used. In the comparison with full old receiver dimension d and fresh dimension r, forbidding a receiver message gives the leading-spectrum value `p_E+t^2 chi(lambda_1,...,lambda_r)/(2L)`. At `t>0` a receiver message is strictly useful exactly when `2<=r<rank(rho)`. The normalized two-outcome d=3 example with spectrum `(3/4,1/8,1/8)` gives gain `t^2(2 sqrt(3)-sqrt(6))/(16(8-t^2))`.

This new exact evaluation uses the specified biased prior and the once-selected finite device family. The equal-prior hierarchy, general arbitrary-experiment variational/dual principles, and fixed-tube local profile laws remain active with their original quantifiers. No universal fixed-pair strict-gap or unrestricted all-time workspace classification is inferred. Majorization, ensemble transformations and concave-envelope mechanisms are credited to their established antecedents; independent human priority clearance is not claimed.

## Exact source and publication

- Native source: `24f48c90d6bcc1eae1d4c38ac5195405ac21da7d`, alias `revision/general-theta-foundations-i-v94-native-source-2026-10-06`.
- Artifact-only publication: `0919ff61895716ea3de1d6a0f2a6a291935764d0`, alias `revision/general-theta-foundations-i-v94-publication-2026-10-06`.
- Response branch: `revision/general-theta-foundations-i-v94-r60-spectral-value-2026-10-06`.

Actions run `37434181477`, job `112171851601`, completed successfully. It pushed the native commit before typesetting, then built and pushed the artifact-only publication without a force update. Its publication artifact is `11398637145`, SHA-256 `365f957d06cc06905ac4d24cc2ac998afc0149a444ca38295e512a455ffc9dee`. The artifact was downloaded and its digest, native/publication identifiers and four PDF hashes were checked against the submitted files.

The [build receipt](papers/GTF-I-v94-spectral-value/evidence/BUILD_RECEIPT.json) records 870 native files and **36 regression suites**, all successful normally and under `python -O`, with identical outputs. The new spectral suite separately records 755 exact checks, 600 deterministic numerical sanity checks and 12 negative controls. Complete isolated reconstruction matches native files, regression results, page text and page rasters. The standalone journal package also reconstructs independently.

All 841 predecessor native files remain in their active paths or byte-identical predecessor audit paths; all 87 predecessor mathematical section files are byte-identical. The 1,088 predecessor complete-edition labels, 256 primary labels and 116 structural labels remain active. No section was relocated in this revision. There are no unresolved references/citations or reported overfull/underfull boxes. Raw LaTeX diagnostics are preserved, rather than redescribed as a blanket warning-free claim.

Native archive SHA-256: `2cd40f076f0855c73d9f400efd193671aec01810c015fd4b6ff1bba62ffeef69`.
Source inventory SHA-256: `9ddf94599c51ab348d6e29038ffe7b285e4adc6fd3086cf8037e26f596bca60b`.

## Final-head verification and independent replay

`GENERAL_THETA_FOUNDATIONS_I_V94_FINAL_HEAD_REQUEST.json` is a metadata-only verification request, not a success certificate. The `final-head` job in `.github/workflows/gtf-v94-revision.yml` checks out the exact triggering SHA with read-only permissions and no persisted write credentials, runs the command below, checks `status=success`, `read_only=true` and `verified_head` equal to that SHA, and uploads `gtf94-exact-final-head-<SHA>`. The review-ready alias is assigned only after this separate job and its matching receipt are observed. No receipt is committed back to the head it verifies.

```sh
python papers/GTF-I-v94-spectral-value/build_revision.py --verify-published
```

The [initial journal package](papers/GTF-I-v94-spectral-value/evidence/JOURNAL_PACKAGE.zip) contains only the primary, its one current supplement, their active sources and reproducibility material. The [research package](papers/GTF-I-v94-spectral-value/evidence/RESEARCH_PACKAGE.zip) retains the complete archive. The independent structural article is not silently included as another initial journal submission.

R60 R06 / pipeline P05 remains an external human specialist priority-assessment request; no such opinion has been obtained. Reconstruction and finite arithmetic are not continuum proofs, physical calibration, human signatures, or journal acceptance. Main, review branches and unrelated papers were not changed. The independent A2/B4/C2/eleven-paper/whole-Theta analytic obligations remain distinct from these finite-dimensional theorems.
