# Audit, source coverage and reproduction — A2 v42

Date: September 14, 2026. This document accompanies [REFEREE_REPORT.md](REFEREE_REPORT.md). It distinguishes authenticated repository observations, fresh source analysis, inherited findings and locally executed finite diagnostics. No claim below is a certificate for all recursive manuscript inputs.

## 1. Frozen source and branch selection

The reviewed repository is `TrillionniumFoundation/theta-theory`. The actual author revision is `revision/a2-v42-native-source-referee-response-2026-09-14`, commit `6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad`, tree `fb689bc8487a1d6b9522dc5270282edd7bee8691`, committed September 14, 2026 at 02:36:47 UTC.

The other discovered branch `revision/a2-v42-source-matched-native-delivery-2026-09-14` points to `e162532115071265cf73b97a5069f33628347cfe`, the preceding v41 referee report. The review target was selected from actual commit contents and ancestry, not branch-name ordering alone.

The authenticated comparison from v41 submission `c730a60bbc8af2a4c6e432813c31dccc897828e7` to the reviewed source is ahead by three commits and behind by zero, with sixteen changed paths. Five paths are the preceding review package; eleven are author-side additions or modifications. See the [immutable comparison](https://github.com/TrillionniumFoundation/theta-theory/compare/c730a60bbc8af2a4c6e432813c31dccc897828e7...6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad). The intermediate source-infrastructure commit is `4d78f5d3850cfae79df6b13c30176e9c64222efe`.

The [native entry](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/main.tex) was read in full. Its GitHub-reported blob identity is `1ab0293dfbc619e2d216f0de77145ee8b90e72f4`. Its literal direct inputs include the preamble and bibliography; the source and current entries retain the declared 54 direct inputs and 36 auxiliary-wrapper inputs. These are not a claim that all recursively included files were downloaded, hashed locally, compiled or audited.

## 2. Source map and actual reading coverage

All S-source file links below pin the reviewed commit. “Read in full” refers to the named file, not every dependency it invokes. Where a long connector response was truncated, the covered portion or completing retrieval is explicitly recorded.

| ID | Immutable source | Fresh coverage |
|---|---|---|
| S01 | [README.md](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/README.md) | Current root navigation; read in full. |
| S02 | [papers/A2-v17-boundary-information-coarsening/README.md](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/README.md) | Current manuscript navigation; read in full. |
| S03 | [papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V42.md](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V42.md) | Current response; read in full, together with VERIFICATION_V42.md (linked below). Author-side verification statements are not represented as fresh referee executions. |
| S04 | [reviews/a2-v41-independent-harsh-top4-2026-09-13/REFEREE_REPORT.md](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/reviews/a2-v41-independent-harsh-top4-2026-09-13/REFEREE_REPORT.md) | Previous report: initial returned text and a separate retrieval of lines 115–192 complete the report. Its tests and favorable findings remain inherited. |
| S06 | [papers/A2-v17-boundary-information-coarsening/v4/10_boundary_layers.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/v4/10_boundary_layers.tex) | Read in two overlapping ranges, 1–240 and 240 to end. Weighted half-line construction, trace-norm factorization, moving-sublevel integration, and subsequent stated consequences. Earlier localization/phase-volume dependencies were not independently reconstructed in full. |
| S07 | [papers/A2-v17-boundary-information-coarsening/article/23f_single_offset_law_inverse_v42.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/23f_single_offset_law_inverse_v42.tex) | Freshly examined the density theorem, stability, finite-flight inverse and detailed global theorem/proof. The long initial response truncates in the final scope paragraph, after the substantive global proof. |
| S08 | [papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v27.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v27.tex) | Read overlapping ranges 1–220, 220–520, and 470 to end; the last range completes the truncated middle response. Weighted inverse, finite envelope, smooth remainders, homogeneous isolation, block recursion and tangent isomorphism. |
| S09 | [papers/A2-v17-boundary-information-coarsening/article/23b_intrinsic_multichannel_rigidity_v28.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/23b_intrinsic_multichannel_rigidity_v28.tex) | Read signature-symmetry lemma, gluing definitions/classification, cycle-holonomy lemma and rooted-tree criterion. Long response truncates during the subsequent known-lattice corollary; no complete end-of-file audit claimed. |
| S10 | [papers/A2-v17-boundary-information-coarsening/article/23b1_signature_rigid_rerooting_v40.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/23b1_signature_rigid_rerooting_v40.tex) | Read in full; analytic reduction, path reversal and common-frame consequence. |
| S11 | [papers/A2-v17-boundary-information-coarsening/article/23d_rank_two_lattice_recovery_v24.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/23d_rank_two_lattice_recovery_v24.tex) | Read in full; unmetrized deck group, rank-two anchoring and lattice/Gram recovery. |
| S12 | [papers/A2-v17-boundary-information-coarsening/article/23e_signature_stability_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/23e_signature_stability_v25.tex) | Freshly examined hypotheses, finite embedding theorem, noisy matching lemma, gluing persistence and compact inverse-modulus argument. The response truncates in the final finite-modulus proof; no claim to have read further unseen text. |
| S13 | [papers/A2-v17-boundary-information-coarsening/article/18a_vector_boundary_information_v26.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/18a_vector_boundary_information_v26.tex) | Freshly examined density assumptions, collar moments, support-exclusive mass, common-collar equivalence and uniform LAN proof. Response truncates at the beginning of the contiguity proof. Later finite-likelihood, moment and loss arguments are not certified anew. |
| S14 | [papers/A2-v17-boundary-information-coarsening/article/18a1_compact_experiments_v32.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/18a1_compact_experiments_v32.tex) | Read in full; finite-net lemma, compact moving-support Gaussian theorem and fixed-window corollary. The cited finite-experiment and physical-transfer dependencies were not all reproved. |
| S15 | [papers/A2-v17-boundary-information-coarsening/article/18c1_endpoint_time_deficiency_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/18c1_endpoint_time_deficiency_v25.tex) | Read through end (requested lines 1–260); layer/bulk/corner bounds, both kernels, count exceptions and projective interpretation. |
| S16 | [papers/A2-v17-boundary-information-coarsening/article/01_introduction_v41.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/01_introduction_v41.tex) | Initial text plus lines 280 to end complete the relevant introduction. Also examined the returned portion of v5/references_v41.tex, not the entire bibliography. The direct-position benchmark and acquisition scope are assessed here as stated, not freshly reproved in their separate chapters. |
| S17 | [papers/A2-v17-boundary-information-coarsening/article/20_boundary_compatibility.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/20_boundary_compatibility.tex) | Lines 1–230: symmetrized energy profile, Volterra uniqueness and differentiated stability, beginning of finite-jet formulation. Supplementary check, not a certification of the entire scalar-information workstream. |
| S18 | [papers/A2-v17-boundary-information-coarsening/article/02_finite_results.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/02_finite_results.tex) | Read in full; threshold/variance theorem statements and declared scope, not all their referenced proofs. |
| S21 | [papers/A2-v17-boundary-information-coarsening/article/99_auxiliary_compendium_v19.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/article/99_auxiliary_compendium_v19.tex) | Read the full wrapper with 36 literal inputs. The auxiliary chapters themselves were not all fetched or audited in this round. |

Additional source for S03: [VERIFICATION_V42.md](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/VERIFICATION_V42.md) was read in full. It explicitly records an open C2 checkpoint. Additional source for S16: [references_v41.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad/papers/A2-v17-boundary-information-coarsening/v5/references_v41.tex); bibliographic entries were checked only to the extent described above and in the primary-literature section below.

Selected GitHub-reported blob identities are retained in SOURCE_EVIDENCE.json. These are metadata returned by authenticated file reads. They are not presented as locally computed hashes of an unavailable complete checkout. In particular, the author's programmatic statement-identity comparison between the new and old single-offset chapters was not rerun by this review.

### Unexamined or inherited dependencies

The complete native companion, all 36 auxiliary inputs, the full finite-itinerary localization and phase-volume chain, all anchored realization and stopped-transfer arguments, the complete count–endpoint experiment, and every minimax application were not freshly audited. The global acquisition and direct-position benchmark are described in the current introduction and addressed in the previous report, but their separate detailed chapters were not reread in this round. This report must not be cited as a new line-by-line certification of them.

Fresh mathematical emphasis is on the v42 common-frame composition and its signature prerequisites, the nonlinear relative law and smooth jet inverse, finite-signature stability, the moving-support compact-net step, and the complete two-sided Poisson comparison. The previous report remains a separately attributed historical assessment, not a substitute for accessible proofs.

## 3. S05 — fresh exact-head hosted evidence

The following endpoints were actually queried through the authenticated GitHub connector:

- [Runs for the exact source](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs?head_sha=6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad&per_page=10).
- [Run 34799807519 jobs](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34799807519/jobs).
- [Run 34799807519 artifacts](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34799807519/artifacts).

| Field | Observed value |
|---|---|
| Workflow | A2 v42 source-pinned native submission |
| Run | `34799807519` |
| Source head | `6b30aaacf7db2b5df3ae3771a5b2d1f0ba1b18ad` |
| Event / attempt | push / 1 |
| Run conclusion | failure |
| Job | `103840001543`, native |
| Job start / completion | 2026-09-14T02:37:00Z / 2026-09-14T02:37:03Z |
| Executed steps | `[]` |
| Runner ID / name | `0` / empty string |
| Artifact total | `0` |

[Human-readable run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34799807519). SOURCE_EVIDENCE.json preserves a compact transcription of the relevant returned fields, not the complete raw API responses. The author's initial ledger instead records run `34798984887` at the earlier infrastructure head `4d78f5d3850cfae79df6b13c30176e9c64222efe`; its mathematical source predates activation of the new chapter.

The exact-head result establishes no executed compiler command or output. It does not identify why the runner failed before any step, and it does not establish a mathematical or TeX defect. No billing, infrastructure or compiler diagnosis is inferred. It also supplies no complete native-delivery evidence. Thus C2 remains open on the fresh record as well as on the author's checkpoint.

## 4. S19 — local source/build boundary

A local single-branch clone was attempted with the actual author branch and failed with inability to resolve `github.com`. No complete local repository checkout was obtained. The environment exposes TeX tools, but their availability was not turned into a complete native main/companion build. No successful native compiler invocation, complete-main PDF, page count or rendered-page review is claimed.

Authenticated connector reads, unlike the attempted local clone, did succeed. They supplied the files and metadata listed above. This distinction prevents a network failure from being misreported as inaccessible repository content or as a failed manuscript compilation. No claim is made that compilation is impossible in another environment.

The review branch adds reports and diagnostic evidence only. It is not a manuscript-revision branch and does not close an author-side delivery item by asserting that a mathematical diagnostic ran.

## 5. S20 — independently executed finite diagnostics

Files: [independent_checks.py](independent_checks.py), [RESULTS.json](RESULTS.json), [EXECUTION.txt](EXECUTION.txt).

Actual command, run from the local review-output directory:

```sh
python independent_checks.py --output RESULTS.json > EXECUTION.txt 2>&1
```

Exit status: **0**. Environment: Python **3.13.5**, NumPy **2.3.5**, SciPy **1.17.0**. These are observed local runtime versions, not a recommendation about current package releases. Script SHA-256:

```text
d417e11d165d084e7fdb1d17a9b83a433c67e42c12019a5d54b1915ec50d8033
```

The script is a new independent implementation with no network I/O and no imports from the manuscript's code. Assertions are part of the tests; run Python normally, not with `-O`. Floating-point residuals and quadrature results can vary slightly with platform. The rational and combinatorial portions are exact. The output explicitly sets `native_manuscript_compiled` and `PDF_visually_inspected` to false.

### Diagnostic definitions

The rational density test uses $d=3/2$, $S(x)=x^2/2+x^3/7+x^4/11$, $B(x)=1+x/5+x^2/9$, and an arbitrary positive normalizing factor $13/7$. It checks the four-density identity at 625 rational pairs and recovers the action and relative amplitude at 25 points for each of three nonzero anchors. This is an interior factorization test; no claim that the chosen arbitrary constant normalizes a global density is needed.

The reroot test enumerates all labelled trees on one through six vertices using Prüfer codes. For every original root, every assignment of rigid vertices containing the original parent vertices, and every rigid proposed new root, it checks that all new parent vertices are rigid. It also rejects the deliberate symmetric-leaf counterexample to an unrestricted reroot assertion. This is the finite combinatorial abstraction; analyticity and the signature-symmetry equivalence are checked in the source proof, not proved by enumeration.

The Green test multiplies the displayed compressed infinite Green kernel by the finite tridiagonal Hessian in six asymmetric/symmetric configurations. The last row is excluded because it omits the infinite neighbor. The maximum tested interior residual is approximately $4.44\times10^{-16}$.

The nonlinear test uses 80 exact Euclidean flight edges, fixed terminal endpoint zero, analytic tridiagonal Hessians and Newton solves. Baseline gap is $0.9$, curvatures $(0.55,1.6)$, cubic jets $(0.3,-0.2)$ and quartic jets $(0.4,0.25)$. A fifth jet $0.35$ is added at one type. The test compares signed averages of action differences divided by $u^5$ at $|u|=0.1,0.05,0.025$ with the envelope block coefficient, for both starting types and both varied types. It tests a fifth-degree smooth perturbation preserving four jets; it is not a test of arbitrary flat variations or the full infinite theorem.

For the Poisson layer, use $w=1-u^2-v^2$, ceiling $w-z/k$, and exact normalizing density factor $2/[\pi(1-z/k)^2]$. The layer has $R=3$, with $z=-1,0,1$ and $k=100,400,1600$. The code calculates the scaled-layer intensity difference including the $r=0$ corner and verifies its $O(k^{-1})$ budget. A **separate** normalized mean-zero tilt $1+\beta zu/k$, $\beta=1/4$, of the reference bulk checks the one-record $O(k^{-2})$ squared-Hellinger budget. It is not claimed to be the conditional bulk of the preceding constant-amplitude ceiling model. A final tilt of order $k^{-1/4}$ deliberately violates the manuscript's relative bulk hypothesis and exhibits the failure of a trace-only product bound.

These tests can detect finite algebraic, parity, combinatorial and scaling mistakes. They cannot certify all smoothness estimates, analytic continuation, compact-class uniformity or the complete statistical experiment.

## 6. Primary literature checked on September 14, 2026

This is a bounded verification of the comparisons used in the report, based on primary abstract pages and revision notices. It is not an exhaustive novelty search or a fresh referee review of the external papers' full proofs. No external PDF was analyzed for this report.

| ID | Primary source | Verified comparison |
|---|---|---|
| L1 | Florio–Leguil, [Smooth conjugacy classes of 3D Axiom A flows, arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), June 3, 2021 | The revision notice removes an earlier open-billiard spectral-rigidity assertion after an error in Proposition 3.1; the abstract retains the smooth-conjugacy application. |
| L2 | De Simoi–Kaloshin–Leguil, [Marked Length Spectral determination of analytic chaotic billiards with axial symmetries, arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), August 17, 2022 | Analytic open billiards, non-eclipse, and stated symmetry/genericity hypotheses; marked lengths determine geometry. Related journal DOI: 10.1007/s00222-023-01191-8. |
| L3 | Finamore–Leguil, [A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards, arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1), October 21, 2025 | The stated finite-horizon Sinai result uses an enriched marked length spectrum. The retrieved current page lists v1 only. |
| L4 | Meister–Reiß, [Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors, arXiv:1101.5248v1](https://arxiv.org/abs/1101.5248v1), January 27, 2011 | Nonregular regression is compared in Le Cam's sense with Poisson experiments encoding the boundary in intensity supports. |

No inference that these observation maps dominate, are dominated by, or are equivalent to the manuscript's signed channel-law map is made without a reduction. The report's significance judgment is explicitly evaluative and separate from the verified descriptions.

## 7. Evidence boundary

The source review, finite diagnostics and Actions observations support the specific findings of the report. They do not establish a complete typeset submission, universal proof correctness, experimental confirmation of a physical table, or actual journal acceptance. The review should be cited with its pinned source, date and scope rather than as an unrestricted certificate.
