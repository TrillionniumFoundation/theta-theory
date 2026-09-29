# Source audit for the external A2 v21 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
Paper directory: `papers/A2-v21-finite-aperture-persistent-rigidity`

The reviewed object is pinned by Git identity:

- author branch: `revision/a2-v21-finite-aperture-persistent-rigidity-2026-09-29`;
- equivalent source alias: `revision/a2-v21-referee-copy-2026-09-29`;
- author commit: `5ab3be483386dab1b2f53575f47dbf7aebd92bd3`;
- repository tree: `6c185f711874fc65a344d6b42ed2768c6c0ff08d`;
- commit date: 29 September 2026;
- commit title: `A2 v21: finite-aperture acquisition and persistent saturated-witness rigidity`.

Both v21 revision aliases resolved to this same commit when the review began. A branch search found no `revision/a2-v22...` branch at that time.

The review branch

`review/a2-v21-external-harsh-top4-rereview-2026-09-29`

was created directly from the author commit. This review adds files only below

`reviews/a2-v21-external-harsh-top4-rereview-2026-09-29/`.

No manuscript source, author branch, earlier report, workflow, permission, or unrelated paper is changed.

## 2. Frozen report chain

The author source has parent

`40e9f1beaf49bf7f870f2f6f73ac027feab1a84e`,

the head of

`review/a2-v20-external-harsh-top4-rereview-2026-09-29`.

That report reviewed v20 author commit

`c376e802e6e86735888dcd685f987c7a8f475903`

and report blob

`d5adb7728eff4dbc8d69cf07937de73b5ecb445f`.

The v21 source pins record:

- frozen review commit `40e9f1be...`;
- reviewed v20 author commit `c376e802...`;
- reviewed v20 paper tree `3b34e4156b3ff621df9c1a3fb8aece4c66f1f07b`;
- retained v20 mathematical core tree `2bfb749b8dd15464e96fdf252cb09b4ad5794165`;
- retained v18 tree `3c558d7799e9e49812e7bab98320d3a98e7f7418`;
- retained smooth-theory tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`.

The complete reviewed v20 paper is preserved under `history/v20-reviewed`. The previous v18 paper remains Supplement R and the smooth relative-law manuscript remains Supplement S. Historical receipts are treated as historical evidence rather than as current v21 execution.

## 3. Active source map

The primary article is entered through `main.tex`. Its active mathematical inputs are:

1. `core/00_new_results.tex`;
2. `core/01_setting.tex`;
3. `core/02_local.tex`;
4. `core/03_descent.tex`;
5. `core/04_stability.tex`;
6. `core/06_canonical.tex`;
7. `core/07_aperture_persistence.tex`;
8. `core/05_comparison.tex`.

The unusual numerical order is deliberate: the new canonical catalogue and aperture theorems are placed before the final comparison section.

The six files `core/01_setting.tex` through `core/06_canonical.tex` have the retained v20 Git blob identities listed by the source validator. The two active additions are:

- `core/00_new_results.tex`, the headline theorem summary;
- `core/07_aperture_persistence.tex`, the new finite-aperture, orbit-key, sparse-witness, persistence, cutoff-crossing, local statistical and proximity/visibility chapter.

The front matter, references and repository ledgers are revised for v21. Earlier mathematics is not silently deleted or replaced by a plan.

## 4. New mathematical content inspected

The rereview read the following v21 files in detail:

- `main.tex`;
- `core/00_new_results.tex`;
- `core/07_aperture_persistence.tex`;
- the retained `core/04_stability.tex` sections used by the new estimator;
- the retained `core/06_canonical.tex` all-cycle and stable-saturation results;
- `RESPONSE_TO_REFEREES.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `PROOF_LEDGER.md`;
- `SOURCE_PINS.json`;
- `PUBLICATION_BINDING.json`;
- `README.md`;
- `references.tex`;
- `tools/verify_v21.py`;
- `tools/validate_v21.py`;
- `.github/workflows/a2-v21-verify.yml`;
- `verification/local/receipt.json`.

The v20 `REFEREE_REPORT.md` and its source audit were read against the new response. The review also checked the relevant primary bibliographic records for the relative-neighborhood and visibility-complex comparisons.

## 5. Mathematical deltas confirmed

### 5.1 Intrinsic period quotient

The new source defines the full translation group of the physical obstacle union and proves that it equals the period lattice on the asymmetric pairwise shape-separated class. It introduces normalized records and whole-pair geometric keys and proves that exact key equality is equivalent to membership in one undirected translation orbit.

### 5.2 Finite aperture

Using bounds `r<=r0`, `diam<=D0`, `rho*<=rho0` and `R>2rho0`, the new theorem derives the aperture radius

`B = rho0 + D0 + (r0-1)(R+2D0) + xi`.

The proof derives a lattice covering-radius bound from the retained complete clear-bridge theorem. It then shows that every bridge midpoint coset has a representative in the aperture. A padded disk contains all endpoint and blocking bodies relevant to the scan.

### 5.3 Sparse saturated witnesses

The new subgroup argument starts from a spanning tree and an independent cycle pair of index `n`. Each added cycle outside the current group reduces the remaining index to a proper divisor. The resulting witness has at most

`r+1+floor(log2 n)`

records.

### 5.4 Persistence and bifurcation

The witness branches persist with positive gap, clearance, curvature, twist and experimental margins. Only the witness is protected. An explicit asymmetric one-orbit family makes a surplus `(1,2)` bridge cross the cutoff while the horizontal and vertical witness loops remain.

### 5.5 Varying-remainder stability

The new local statistical theorem accepts qualified unlabelled lists of varying cardinality, provided every reference witness orbit is retained. Exact reference key neighborhoods select witness records after physical-pair fitting. Unused edges can be born, die, be repeated, or lose visibility without entering the estimator.

### 5.6 Literature comparison

The source now gives theorem-specific comparisons with Toussaint, Jaromczyk--Toussaint and Pocchiola--Vegter. It credits the classical shorter-neighbor idea and distinguishes normal billiard bridges from tangent free bitangents.

## 6. Independent diagnostics

The review's `verify_review.py` is independent of every author verification module. It uses exact integer/rational arithmetic and a fixed seed. Its successful run produced 23,945 checks:

| Group | Checks |
|---|---:|
| outside generator exists | 1,775 |
| proper divisor and halving | 1,775 |
| saturation reached | 1,200 |
| logarithmic step bound | 1,200 |
| witness edge-count bound | 6,000 |
| relative-graph component equality | 1,000 |
| pair-key translation invariance | 3,000 |
| pair-key reversal invariance | 3,000 |
| normalized cycle-minor persistence | 2,000 |
| aperture coset representative | 2,700 |
| packing identity | 81 |
| covering-range controls | 50 |
| witness saturation controls | 50 |
| basis edges below cutoff | 50 |
| surplus-edge cutoff pattern | 50 |
| rate balance and subdominant term | 14 |
| **Total** | **23,945** |

These diagnostics test finite algebraic and combinatorial consequences only. They do not certify analytic continuation, physical bridge selection, the infinite periodic geometry, Borel minimization, or editorial novelty.

## 7. Author validation and workflow status

The author local receipt reports:

- execution kind `source_content_not_git_checkout`;
- 43,928 retained-base checks;
- 26,734 v21 checks;
- 70,662 total primary finite checks;
- identical normal and optimized output for both suites;
- a warning-free 29-page primary build;
- no GitHub run ID or source commit in the local execution.

This scope is accurately described in the source. It is not mislabeled as an authenticated checkout or hosted pass.

The current read-only workflow is

`.github/workflows/a2-v21-verify.yml`.

It checks out `${{ github.sha }}`, runs `tools/validate_v21.py --all-volumes --require-checkout`, and uploads current and local evidence even on failure.

The run bound to the reviewed SHA is:

- run ID `36535427881`;
- workflow `A2 v21 exact-source full-package verification`;
- head SHA `5ab3be483386dab1b2f53575f47dbf7aebd92bd3`;
- state at final review check: `queued`;
- conclusion at final review check: `null`.

Accordingly this audit records the local primary build and the existence of a suitable exact-source workflow, but not a completed hosted v21 all-volume pass. The successful v20 run is not transferred to v21.

## 8. Limits of this audit

This is a targeted external top-four rereview, not formal verification of the entire retained programme. It concentrates on:

1. the new orbit-key and finite-aperture claims;
2. the sparse witness subgroup bound;
3. persistence under unused-edge bifurcation;
4. the local varying-list statistical theorem;
5. response to the v20 information and literature objections;
6. top-four significance after those corrections.

No exhaustive priority search was performed. The review did not independently compile the full package or re-prove every theorem in Supplements R and S. Finite diagnostics and workflows are not proof certificates.

## 9. Audit conclusion

The reviewed source is unambiguous, the new branch is isolated, and v21 is a genuine theorem-level revision. The six v20 mathematical core files are retained, while the new aperture/persistence chapter is active in the primary article.

The unknown quotient, full-catalogue topology freeze, cutoff-crossing example and requested proximity/visibility comparison have been substantively addressed. No fatal counterexample was found in the new core. The remaining negative recommendation in `REFEREE_REPORT.md` concerns the richness of the sensor, geometry-aware acquisition oracle, local witness prior, global genericity and four-journal conceptual threshold rather than a claim that v21 is a metadata-only revision or contains an identified false headline formula.
