# General Theta Foundations I — Revision 93, response to R60

**Primary:** *Finite-Use Discrimination Geometry of Ordered Quantum Measurements*.

**Current directory:** [`papers/GTF-I-v93-spectral-rigidity`](papers/GTF-I-v93-spectral-rigidity).

The controlling external report is v90/R60 at `cf13712c54e9ef0c9c54a240b1f26efc78cc3568`, with companion proof/pipeline audit `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. Their frozen copies remain unchanged. The immediate published predecessor is v92 at `a7081ca8cfb1df8f6369a5820e4f3b5027b66ca2`, native source `33811525dd80dbc3c0c70059114fb779e9ac9c84`. The paper topic and four-leading-general-mathematics-journal objective are retained.

## Manuscripts

| Object | File | Pages | Reading role |
|---|---|---:|---|
| Current primary | [paper.pdf](papers/GTF-I-v93-spectral-rigidity/paper.pdf) | 72 | Start here; new results in Section 19 |
| Current linked supplement | [BINARY_SUPPLEMENT.pdf](papers/GTF-I-v93-spectral-rigidity/BINARY_SUPPLEMENT.pdf) | 87 | Current dependency proofs and auxiliary consequences |
| Independent structural article | [STRUCTURAL_PAPER.pdf](papers/GTF-I-v93-spectral-rigidity/STRUCTURAL_PAPER.pdf) | 41 | Source unchanged; not a premise of the new theorems |
| Complete research edition | [COMPLETE_REVISION.pdf](papers/GTF-I-v93-spectral-rigidity/COMPLETE_REVISION.pdf) | 284 | Entire mathematical record, not a second submission |

The initial journal-facing package is the primary and its linked current supplement, with their source and reproducibility instructions. The [journal package](papers/GTF-I-v93-spectral-rigidity/evidence/JOURNAL_PACKAGE.zip) and [research package](papers/GTF-I-v93-spectral-rigidity/evidence/RESEARCH_PACKAGE.zip) serve these different purposes.

## Substantive changes and genealogy

The general finite-experiment normal form, attained variational/dual principles and equal-prior experiment were already published in v91. The dimension-preserving two-cut hierarchy was already published in v92. These are retained, not recounted as new v93 results. The covariance/support, fixed-tube, complete-profile and hard quadratic-budget results remain active and retain their separate quantifiers.

New primary Section 19 contains six numbered results:

| Printed result | Source label | Content |
|---|---|---|
| Theorem 19.1 | `thm:initialspectra93` | The complete set of initial Gram matrices attaining the equal-prior rank-r optimum is exactly `rho <= I/r`; an attaining commuting projection decomposition uses at most d terms. |
| Corollary 19.2 | `cor:threecuts93` | Adding a separately counted first reference gives the exact three-cut minimum-dimension formula; fixed-subspace preparations attain both priors without feedback. |
| Lemma 19.3 | `lem:projectionstability93` | An explicit centered-swap deficit controls both branch Grams' squared trace distances to a common normalized rank-r projection, including singular and unequal-rank factors. |
| Corollary 19.4 | `cor:nearoptimalframes93` | Near-optimal reward forces approximate initial projection decompositions with explicit averaged and tail estimates. |
| Proposition 19.5 | `prop:spectralloss93` | The distance to the capped spectral set is exactly `2 tr(rho-I/r)_+`, yielding a quantitative necessary reward loss. |
| Proposition 19.6 | `prop:qubitpinching93` | The exceptional qubit/rank-one equality face is commutation with a pure factor, including commuting mixed factors; an exact pinching identity replaces a false common-pure-state conclusion. |

The new source module is `sections/86-initial-spectra-and-rank-rigidity.tex`. Its archival source number is not its printed primary section number. The generated [theorem-location record](papers/GTF-I-v93-spectral-rigidity/evidence/THEOREM_LOCATIONS.json) supplies exact printed theorem and page numbers in each edition.

For clarity, write `s=min(q,k,ell)` for the first-reference, old-receiver and fresh-reference dimension bounds. On the fixed finite once-selected basis family, the exact equal-prior value is

```
P_eq = 1/2 + t^2 (d s - 1)/(2 d s (d+1)).
```

The latent device is selected once for both calls, not independently redrawn. The three dimensions are measured at the stated cuts; the theorem does not impose an all-times total-workspace bound or remove the reset cut. The initial-spectrum characterization applies to a specified pure first acquisition through its Gram matrix. The quantitative common-projection conclusion excludes `(d,r)=(2,1)` and the pinching proposition handles that endpoint separately. Gram weights are not substituted for hypothesis-dependent branch probabilities. Calibrated score errors must be included before applying a spectral-loss inference.

The [point-by-point response](papers/GTF-I-v93-spectral-rigidity/RESPONSE_TO_REFEREE.md) addresses R01–R15 and D01–D30. The [new derivation ledger](papers/GTF-I-v93-spectral-rigidity/PIPELINE_DERIVATION_V93.md), [history audit](papers/GTF-I-v93-spectral-rigidity/HISTORY_AND_PIPELINE_AUDIT.md), and [primary-source comparison](papers/GTF-I-v93-spectral-rigidity/LITERATURE_AUDIT.md) identify dependencies and the exact contribution boundary. Standard projection convexity, fidelity inequalities, spectral clipping and the interval construction are not claimed as new standalone mechanisms.

## Actual source and publication

- Native source: `2595ee56f70138c58b1924591d32e09cbad31381`, branch `revision/general-theta-foundations-i-v93-native-source-2026-10-06`.
- Artifact-only publication: `3b660839818d6ef676da72fb6e9969501be4e59a`, branch `revision/general-theta-foundations-i-v93-publication-2026-10-06`.
- Response branch: `revision/general-theta-foundations-i-v93-r60-spectral-rigidity-2026-10-06`.
- Successful source/publication run: `37427322455`, job `112149833855`.
- Native artifact: `11395264793`, SHA-256 `8c8f6a9efddb88422724145b135a2e9438d9b912cee7a3e9eaedaf8563550663`.
- Publication artifact: `11395498709`, SHA-256 `cef4dafa053fc318b733be20c664875d899c0ebfea53ec2e49a2f2843b57cca8`.

The workflow first pushed the native source, then built and independently reconstructed it, then pushed its artifact-only publication child. No failed predecessor workflow is used as current qualification. No existing review branch or unrelated paper directory was changed.

## Executed checks and preservation

The [build receipt](papers/GTF-I-v93-spectral-rigidity/evidence/BUILD_RECEIPT.json) records 841 native source files, 35 regression suites with identical normal/optimized results, an isolated complete native reconstruction and a standalone journal reconstruction. All four document logs have no unresolved citations/references and no recorded overfull/underfull boxes. Raw log matches are preserved rather than rewritten as a blanket warning-free claim.

All 815 predecessor native files survive at their active paths or in exact predecessor audit copies. Every predecessor mathematical section is byte-identical and remains active; 1,068 predecessor complete-edition labels and the structural source graph are retained. There is no new relocation. The complete edition's previous long abstract is retained as its opening synopsis while the actual abstract is shortened.

The new regression distinguishes exact fixtures, deterministic numerical sanity checks and negative controls. It does not promote finite replay to proof of the continuum theorems, independent priority clearance or physical-reset calibration. The all-matrix arguments are written in Section 19.

## Exact final-head reconstruction

The metadata-only `GENERAL_THETA_FOUNDATIONS_I_V93_FINAL_HEAD_REQUEST.json` is a request, not a successful receipt. The `final-head` job in `.github/workflows/gtf-v93-revision.yml` checks out its exact triggering SHA with read-only contents permission and no persisted write credentials. It executes

```sh
python papers/GTF-I-v93-spectral-rigidity/build_revision.py --verify-published
```

and reconstructs both native and journal packages, verifies source/artifact identities, and uploads `gtf93-exact-final-head-<SHA>`. Only an observed successful job and matching `verified_head` receipt qualify that final SHA. The review-ready alias `revision/general-theta-foundations-i-v93-spectral-rigidity-review-ready-2026-10-06` is assigned only after that receipt is observed; no receipt is committed back to the head it verifies.

R60 R06 / pipeline P05 still requires independent human specialist priority assessment; none is represented by this revision. The original report remains available for reconsideration, not redescribed as journal acceptance. The separate A2/B4/C2/eleven-paper/whole-Theta analytic closure flags remain false without changing their objectives.
