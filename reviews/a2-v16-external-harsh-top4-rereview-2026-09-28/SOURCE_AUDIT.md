# Source audit for the external A2 v16 rereview

## 1. Reviewed repository object

Repository: `TrillionniumFoundation/theta-theory`  
Article: Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
Paper directory: `papers/A2-v16-intrinsic-boundary-rigidity`

The review is pinned to Git objects rather than inferred from branch names:

- latest revision branch: `revision/a2-v16-intrinsic-boundary-rigidity-2026-09-28`;
- equivalent source alias: `revision/a2-v16-referee-copy-2026-09-28`;
- latest revision head: `9b0f76a32d1296b4035b52e43a38b3e3ffb50f18`;
- latest repository tree: `db18329d561f7f2011e668a7517fe53938331859`;
- mathematical checkpoint: `36642945db6d1c3a10a73826d658ac90e01b09bd`;
- checkpoint repository tree: `3c6e3814da6a20b1910f1d3fdecd2ce051221906`;
- checkpoint paper tree: `16622a158c054df5a98912c5adbf2b2c874b4fca`.

No `revision/a2-v17...` branch existed at the review cutoff. Both v16 aliases resolved to the same latest head.

The review branch

`review/a2-v16-external-harsh-top4-rereview-2026-09-28`

was created directly from `9b0f76a...`. This review adds files only under

`reviews/a2-v16-external-harsh-top4-rereview-2026-09-28/`.

No author manuscript, prior report, revision branch, workflow, supplement or unrelated paper is modified by the review.

## 2. Preceding reviewed chain

The current source pins identify:

- frozen v15 review head: `3de6ab93a81e76f35ccf507f8815852ea4c981f6`;
- qualified v15 mathematical commit: `00f27ebd0071d75504995b61f9a15c67f896188f`;
- qualified v15 paper tree preserved at `history/v15-reviewed`: `db84120af7be42acd785a9bc8d87dc6c652ee8d9`;
- complete smooth-theory tree preserved under `complete`: `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`.

The latest v15 report requested eight corrections: precise naming of the framed information category, an honest account of the count-only quotient problem, broader literature comparison, a standalone lower-jet filtration lemma, a precise analytic continuation lemma, formal supplement status, strict separation of endpoint compression from counts, and commit-bound hosted reproducibility.

Version 16 addresses all eight at source level. The report in this review therefore evaluates the new theorem rather than repeating the v15 objections as though no revision occurred.

## 3. Current source identity

`PUBLICATION.json` records:

- published core tree: `647752522037690bb019c58d422b52e04ac9395f`;
- published tools tree: `c76c95f1f34b7137220d9090609d6a5f1a02867b`;
- `main.tex` blob: `83033c5a8d297ecf416477725063963cabcd52b4`;
- `references.tex` blob: `a22e50472e6c21812fa9bc94bbcfccf2e24639e2`;
- local source-manifest SHA-256: `9312252b1a9f7f08322d4a28b2a18778026ba764fe6bd87537cb03538cb95c16`.

`SOURCE_PINS.json` records the following retained v15 core blobs:

| Current v16 path | Retained blob |
|---|---|
| `core/02_local_law.tex` | `ead6f0334962bf7c4c6768ed829b4f6069231ff7` |
| `core/03_asymmetric_inverse.tex` | `3f4443c109b2ebb698803d4af296cd61250bc8f2` |
| `core/04_physical_observation.tex` | `05f0342a86638594d25a75aaba112d6223b53b9f` |
| `core/05_relative_laws.tex` | `16888b97102aefcfd23c21eec12bad5902bffd02` |

The review treated those files as retained dependencies and concentrated its new proof audit on the intrinsic calibration, filtration, analytic image identity, registered global reconstruction, count fibers and intrinsic experiment transfer.

## 4. Files read in detail

The following current files were read in full or in all theorem-bearing ranges relevant to the review:

- `main.tex`;
- `core/00_intrinsic_setting.tex`;
- `core/02_local_law.tex`;
- `core/03_asymmetric_inverse.tex`;
- `core/04_physical_observation.tex`;
- `core/05_relative_laws.tex`;
- `core/06_intrinsic_calibration.tex`;
- `core/07_filtered_arclength.tex`;
- `core/08_global_rigidity.tex`;
- `core/09_count_fibers.tex`;
- `core/10_intrinsic_experiments.tex`;
- `references.tex`;
- `README.md`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `PROVENANCE.md`;
- `PUBLICATION.json`;
- `SOURCE_PINS.json`;
- `SUPPLEMENT_STATUS.md`;
- `tools/verify_exact.py`;
- `tools/run_validation.py`;
- `.github/workflows/a2-v16-verify.yml`.

The frozen v15 `REFEREE_REPORT.md`, `SOURCE_AUDIT.md`, `LITERATURE_AUDIT.md` and verification record were also consulted to distinguish resolved objections from genuinely remaining ones.

## 5. Mathematical changes confirmed

### 5.1 Intrinsic observation

The source now defines a boundary-arclength endpoint subprobability law, including failures, modulo one simultaneous reversal. It expressly distinguishes this from reflected averaging, edgewise sign choices and count-only observation.

### 5.2 Leading-geometry recovery

The source derives the gap from onset, each curvature from a quadratic arclength difference moment, and the free area from the common leading mass coefficient. The resulting leading-coordinate map has a displayed nonzero analytic Jacobian.

### 5.3 Filtered all-parity inverse

A standalone residual-flux filtration lemma gives the exact first variation before scaling, controls the moving domain and explains why the intrinsic arclength mark has the same highest odd block as its Cartesian linearization. The argument permits arbitrary lower asymmetric jets.

### 5.4 Analytic image continuation

A separate embedded-real-analytic-submanifold identity lemma replaces the previous informal continuation paragraph.

### 5.5 Registered whole-table theorem

A finite connected channel network with coherent intrinsic contact registration and full-rank integer cycle labels is used to place every obstacle and recover the unknown lattice basis. Open physical examples and a rank-one shear control are included.

### 5.6 Count-only fibers

The manuscript proves positive-dimensional finite count fibers in analytic physical families, constructs compatible all-order formal fibers and smooth physical realizations, and explicitly separates these facts from the unresolved exact analytic count-germ problem.

### 5.7 Intrinsic finite-window transfer

The marked finite-window experiment is transferred to intrinsic arclength. The source continues to state that the endpoint sensor is used before private binary compression and that the result is not count-only.

## 6. Independent review diagnostics

`verify_review.py` is independent of `tools/verify_exact.py` and imports no manuscript code. It uses exact rational arithmetic and a separate truncated-series implementation. It checks:

- exact inversion of the local Hessian;
- difference and sum quadratic moment formulas;
- curvature and area recovery;
- the leading-coordinate Jacobian after dividing by the common positive factor;
- the first nonzero coefficient of the nonlinear arclength variation in the presence of arbitrary lower coefficients;
- the intrinsic arclength cubic coefficient;
- lattice recovery with unimodular and nonunimodular cycle matrices;
- fixed-covolume shear controls;
- spanning-tree gauge removal and independent cycle labels;
- jet, window and count-fiber dimensions;
- simultaneous-reflection parity.

The executed result contains 3,115 passing checks. The script makes no claim about analytic continuation, the nonlinear first-hit geometry, Borel extension convergence beyond the stated formal series diagnostics, or the source build.

## 7. Author evidence and hosted status

The local receipt reports:

- 5,844 exact finite diagnostics;
- identical normal and optimized Python output;
- a 21-page primary build;
- no final TeX warnings or bad-box diagnostics;
- unchanged source/tool hashes.

The source correctly classifies this as a source-content run in a container directory rather than an authenticated Git checkout. The receipt has null commit/tree fields by design. Supplement S was preserved but not rebuilt in that local execution.

The read-only hosted workflow is `.github/workflows/a2-v16-verify.yml`. At the final review check:

- run ID: `36395491597`;
- triggering SHA: `9b0f76a32d1296b4035b52e43a38b3e3ffb50f18`;
- status: `queued`;
- conclusion: `null`.

The review therefore does not report a successful commit-bound full-package hosted build.

## 8. Audit limits

This was a targeted external rereview of the latest mathematical increment, not a formal verification of every retained theorem in Supplement S. In particular:

- no independent full TeX build was completed;
- no nonlinear billiard trajectory simulation was used;
- no exhaustive literature or priority search was performed;
- no stability theorem for analytic continuation or registered network reconstruction was inferred;
- finite algebra diagnostics were not substituted for the all-order geometric proof;
- author-produced source evidence was not relabelled as independent proof certification.

## 9. Source-audit conclusion

The reviewed source is unambiguous and reproducibly pinned. Version 16 is a genuine mathematical revision, not a renamed v15 source. It preserves the preceding manuscript and supplement while adding active intrinsic and global proofs. The review branch is isolated from all author branches.

The concrete v15 correction requests are closed at source level. The negative recommendation in `REFEREE_REPORT.md` is consequently a new assessment of the naturality, scope and top-four significance of the v16 theorem, not a claim that the authors failed to submit a revision or that a fatal formula error has been found.