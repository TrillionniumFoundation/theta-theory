# Source, execution, and coverage audit — A2 v35

This audit accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). It separates authenticated repository observations, inspected mathematical arguments, author-reported execution claims, and independently executed finite diagnostics. It does not certify uninspected material.

## 1. Immutable identities

| Role | Identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Author branch reviewed | `revision/a2-v35-referee-integration-native-verification-2026-09-13` |
| Reviewed commit | `1c50ef04fc2863b4744b5312b539cb68265054f3` |
| Reviewed root tree | `adb6e3539ded98487636a0fe2e8f961c17383e01` |
| Author v34 predecessor | `127f9334f15c5fb12307bd691973d1eb44e499e8` |
| Addressed v33 review commit | `d51c06689ba540711b2f890beb35eb235dba13e4` |
| Submission reviewed by that v33 report | `b577cffcb3ca5597cb4905269bea9de3bd4ead38` |
| New report branch | `review/a2-v35-external-harsh-top4-2026-09-13` |

The author commit timestamp is `2026-09-12T23:37:08Z`, corresponding to September 13, 2026, 01:37:08 Europe/Amsterdam. The printed manuscript date is September 13. Branch names and version labels were not substituted for immutable source identities.

The repository was accessed through the authenticated GitHub connector. Public web browsing was used only for the external literature below, not as a substitute for private repository access. No repository administration, merge, manuscript edit, or previous-review edit was requested for this report.

For a manuscript path below, its immutable source URL is formed from:

`https://github.com/TrillionniumFoundation/theta-theory/blob/1c50ef04fc2863b4744b5312b539cb68265054f3/`

All paper-relative paths below have prefix `papers/A2-v17-boundary-information-coarsening/`. This historical directory name is retained in the author source.

## 2. Source keys and examination coverage

### S1 — commit identity and actual revision delta

Authenticated reads resolved the author branch to the reviewed SHA and retrieved its commit metadata. The compact comparison of v34 `127f9334...` with v35 `1c50ef04...` returned two commits ahead, zero behind, eighteen changed paths, and no deleted path. Only the active main and vector chapter change among active TeX sources. Historical copies and imported v33 review files are not new active mathematical chapters.

Canonical comparison:

`https://github.com/TrillionniumFoundation/theta-theory/compare/127f9334f15c5fb12307bd691973d1eb44e499e8...1c50ef04fc2863b4744b5312b539cb68265054f3`

### S2 — current navigation

Both root `README.md` and the paper's `README.md` were fetched at the reviewed SHA. Both identify v35, the current response and verification files, and the distinction between the addressed v33 report and the intervening v34 author source. This supports closure of I1. It does not establish an actual complete-main execution.

### S3 — assembled native entry and auxiliary inventory

`main.tex` and `article/99_auxiliary_compendium_v19.tex` were read. The native entry preserves the relative-law, intrinsic inverse, local-experiment, and global-acquisition parts; it includes the retained `article/18a2_likelihood_tilting_moments_v34.tex`. The main's direct inputs and the 36 listed auxiliary inputs remain active. The exact 52-input preservation assertion is also part of the author's current response; the version comparison shows no other active input-source modifications in v35.

**Coverage limitation:** reading the input inventory is not reading all auxiliary proofs. No complete recursive-source build or all-file label/reference audit was independently executed here.

### S4 — response, execution record, and preceding review

The current `RESPONSE_TO_REFEREE_V35.md` and `VERIFICATION_V35.md` were read. The recommendation, issue table, finite/compact discussion, and substantial portions of the preceding `reviews/a2-v33-external-harsh-top4-2026-09-13/REFEREE_REPORT.md` were inspected. Its previous favorable assessments were not adopted as independent proof certificates. The current review is pinned to the v35 source, not the prior report's target.

The companion PDF and author-diagnostic hashes printed in `VERIFICATION_V35.md` are **author-reported metadata**. This review did not retrieve those products, compile the companion, or rerun `tools/check_revision_v35.py`. The newly executed diagnostics below are a different script with a different purpose.

### S5 — vector information and the actual v34/v35 repair

Inspected source:

- `article/18a_vector_boundary_information_v26.tex`
- `article/18a2_likelihood_tilting_moments_v34.tex`

The vector chapter was read in ranges to avoid response truncation. The reviewed arguments include the collar moments, support-exclusive mass, common-collar kernels, LAN expansion, finite-likelihood comparison, identifiable quotient, and the v35 alternative mean/centered fourth moment. Relevant labels are `lem:v22-vector-collar`, `lem:v22-common-collar-equivalence`, `lem:v22-dominated-lan`, `lem:v33-finite-likelihood`, `thm:v22-vector-boundary-gaussian`, `eq:v35-one-mark-expansion`, `eq:v35-alternative-mean`, `eq:v35-centered-fourth`, and `prop:v34-tilting-moments`.

### S6 — compact Gaussian and waiting-count arguments

Inspected source:

- `article/18a1_compact_experiments_v32.tex`
- `article/18d_count_endpoint_multirate_v32.tex`

The compact-net lemma and moving-boundary modulus were read in full. The count chapter's rates, score derivatives, Hellinger comparison, declared observation, and product proof were examined; the fetch truncates near the final inherited physical-transfer conclusion. The complete upstream anchored-realization and raw-physical chapters were not independently rederived. The report's favorable count assessment is conditional on those printed inherited physical-transfer hypotheses.

### S7 — forward local geometry and relative factorization

Inspected source portions:

- `v3/10_geometry_action.tex`: geometric localization, quadratic Jacobi reduction, weighted bridge construction, and the available trace-log derivative argument.
- `v4/10_boundary_layers.tex`: half-line construction and the complete central two-boundary factorization argument, including endpoint block truncation and relative determinant comparison.

The latter fetch truncates in the subsequent physical limiting-law section. These readings do not constitute a complete fresh audit of every physical flux integral, differentiated operator extension, or offset-coordinate transfer. The exact finite recurrence/Schur tests in D1 supplement, but do not replace, the analytical examination.

### S8 — signed all-order and single-offset density inverses

Inspected source:

- `article/23a_signed_endpoint_rigidity_v27.tex`, read in overlapping ranges through its final proof.
- `article/23f_single_offset_law_inverse_v26.tex`, including its fixed-order stability qualifications and conditional global composition.

The weighted inverse, finite-truncation envelope, smooth-remainder factorization, homogeneous isolation, determinant-one recursion, fixed-order tangent bound, density cancellation, anchor choice, and finite-flight interior norm statements were examined. The report does not infer an infinite-order conditioning estimate from determinant one.

**Global classification limitation:** the complete intrinsic incidence/gluing theorem, rank-two lattice recovery proof, signature stability, and global-orientation quotient were not freshly reconstructed from all of their own modules in this round. Their stated role and hypotheses were checked through the introduction, inverse composition, and acquisition argument. The report explicitly withholds independent certification of that entire dependency chain.

### S9 — adaptive transfer, calibration, and global statistical implementation

Inspected source:

- `article/17_adaptive_experiments_v31.tex`
- `article/17a_measurable_physical_coupling_v31.tex`
- `article/25a_common_observables_v25.tex`
- `article/25b_augmented_global_reconstruction_v26.tex`

The adaptive stopping/coupling proof and measurable physical coupling were read. The calibration grid, localization, capped scans, gap/frame error, observation space, and test-bias argument were examined; the final few lines of the calibration file's last proof were truncated in the fetch. The global finite-test selection, finite-template estimator, cap/concentration argument, diagonal consistency, and fresh-stage budget implementation were read. The underlying geometric compact inverse modulus was used at its declared scope, not independently reproved here.

### S10 — contribution and observation-level presentation

`article/01_introduction_v27.tex` was read through its concluding related-work and organization sections. `v5/references_v25.tex` was inspected for the cited literature and provenance entries. The direct planar-position benchmark and the observed-contact information dichotomy were considered at the introduction's stated scope, **not independently rederived from their full separate proof modules**. The review does not certify the full Poisson layer/bulk/corner comparison or the companion's proof.

## 3. Selected exact source blobs

These are Git blob SHA-1 identifiers returned by authenticated file reads, not PDF SHA-256 hashes.

| Path | Git blob |
|---|---|
| Root `README.md` | `54cc54e6e7e300c9107316329b414c18b0c05cdd` |
| Paper `README.md` | `95b9ca8ec7334fd66c0a56c10846575ba2b27cc0` |
| `main.tex` | `d21ea5c3c3926890505a8e44683b8e5de91e9d8b` |
| `RESPONSE_TO_REFEREE_V35.md` | `51df83923023e225274e8fcd59750b405e600186` |
| `VERIFICATION_V35.md` | `cb5ddd37d744e65f1108e4d5da4692fb1a915909` |
| `article/18a_vector_boundary_information_v26.tex` | `8ff3ce7334954d6544555e9867a12fa805ca5ea0` |
| `article/18a2_likelihood_tilting_moments_v34.tex` | `a8658275503f4eed5ebbae675710e4a8392a39a5` |
| `article/18a1_compact_experiments_v32.tex` | `176e2588344ce0646ed47c09c64f371d6d16a045` |
| `article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `article/23f_single_offset_law_inverse_v26.tex` | `35f538eea4415951d1572cd9db76fdff429afa0a` |
| `v3/10_geometry_action.tex` | `bbfcaa2d01c229ec0147d5305352b536397842ae` |
| `article/17_adaptive_experiments_v31.tex` | `a3864877e478297153efc6f2779e188cc819bcbd` |
| `article/17a_measurable_physical_coupling_v31.tex` | `93eddb2d5b383c1f31a8190552080ef8fa8602d9` |
| `article/01_introduction_v27.tex` | `4bf96b3ad9f77c0671a7142e8f4baad3db3f560b` |
| `article/99_auxiliary_compendium_v19.tex` | `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` |

Every other cited source remains identified by the full reviewed commit and its exact path; no truncated blob identifier is substituted for a full one.

## 4. C1 — directly observed hosted execution

The following REST resources were read through the authenticated connector on September 13, 2026:

- `https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs?head_sha=1c50ef04fc2863b4744b5312b539cb68265054f3&per_page=10`
- `https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34725901237/jobs`
- The dedicated workflow-artifacts action for repository `TrillionniumFoundation/theta-theory`, run `34725901237`.

Observed run: `A2 v35 complete native submission`, run ID `34725901237`, exact head SHA as above, completed/failure. The job `complete-native`, ID `103639833518`, had `steps: []`, `runner_id: 0`, empty runner name, start `2026-09-12T23:37:24Z`, completion `2026-09-12T23:37:28Z`. The artifact list was empty.

Canonical run page:

`https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34725901237`

The repository-wide generic artifacts endpoint was rejected by the connector; the run-specific dedicated artifact query succeeded and is the evidence used. No failure cause was inferred. No workflow was rerun or modified in this review. No native main or companion compilation, PDF-page inspection, or comprehensive TeX-reference audit was executed by this referee round.

## 5. D1 — independently executed diagnostics

The supplied `diagnostics.py` uses only the Python standard library and explicit `require` checks, which remain active under optimization. Commands executed successfully in this review:

```sh
python diagnostics.py > diagnostics.json
python -O diagnostics.py > diagnostics_optimized.json
cmp diagnostics.json diagnostics_optimized.json
```

Both execution modes returned success and produced byte-identical JSON. The duplicate optimized output need not be retained because its bytes are identical. The exact source and output SHA-256 hashes are:

| Product | SHA-256 |
|---|---|
| `diagnostics.py` | `6bdc23cbae8e95dec5424eff7912a63d4f7595eb0a93e0cf19302b0baf0ca759` |
| `diagnostics.json` | `4df7d0bbf5b60115ad6c6d6327b1e31a26a71c71142e3bb303cce16419825452` |

Checks cover 25 exact rational four-density ratios and five signed reconstructions; twelve exact finite Schur complements; 162 exact half-line Green recurrence entries; last-jet blocks at orders 3–16; explicit moving-disk mean and reference-moment budgets; and three finite negative-binomial affinity comparisons. Floating-point outputs are finite diagnostics, not rigorous asymptotic error certificates. The moving-disk family is not asserted to be physically realized by the billiard model. The arbitrary normalizer in the rational density example cancels algebraically; that example makes no global-normalization claim.

These checks do **not** reproduce the author's 24-check script, establish all infinite-dimensional bounds, verify global analytic gluing, or compile the manuscript. Source-file hashes identify artifacts, not mathematical truth.

## 6. External primary-source comparison

The following primary abstract/metadata pages were checked on September 13, 2026. Full proofs of these external papers were not audited in this round. Their limited use is to verify the scope of comparison, not establish exhaustive originality.

**L1.** De Simoi, Kaloshin, and Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*. The primary page describes finitely many strictly convex analytic obstacles, a non-eclipse condition, and symmetry/genericity assumptions. It lists arXiv v4 dated August 17, 2022 and a related journal DOI.  
`https://arxiv.org/abs/1905.00890`

**L2.** Finamore and Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*. The retrieved page lists v1, October 21, 2025, and describes finite-horizon Sinai billiards determined up to isometry by an enriched marked length spectrum. No unverified journal-acceptance claim is made.  
`https://arxiv.org/abs/2510.18983`

**L3.** Meister and Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*. The primary page states Le Cam equivalence with two independent Poisson point processes whose intensity-support boundaries encode the target curve. It lists v1, January 27, 2011.  
`https://arxiv.org/abs/1101.5248`

No comparison here identifies those observation maps with the manuscript's signed transverse-law data. No absence-of-prior-work claim is inferred from this limited search.
