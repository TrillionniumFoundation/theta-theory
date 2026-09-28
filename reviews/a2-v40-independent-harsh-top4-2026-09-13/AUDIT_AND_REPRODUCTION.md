# Audit coverage and reproduction ledger — A2 v40

## 1. Immutable review boundary

Repository: `TrillionniumFoundation/theta-theory`.

Reviewed commit: `070aa946fb28001916ad1bbd3503afa5f6cae3b3`; tree: `2f51a70d20a9a398ec46fec6ed2e131ba155760a`; author/committer timestamp: `2026-09-13T09:36:53Z`.

Submission branch: `revision/a2-v40-native-audited-submission-2026-09-13`.

The branch initially resolved to v39 commit `dd0e5aefd49d200652afc3fc3f29f7a6f38ae326`, tree `e936d5f6f463ea51f7f4cccb862de9216d4c258d`. During the review it advanced to the above v40 commit. The target was updated and then rechecked; the later checkpoint still resolved to `070aa946…`. The report makes no assertion about commits pushed after this boundary.

The direct commit comparison is one commit ahead, zero behind, and reports exactly two paths: `main.tex` (revision metadata and one new input) and the added `article/23b1_signature_rigid_rerooting_v40.tex` (66 lines). Consequently the inherited sources read at `dd0e5ae…` are identical in the reviewed v40 snapshot. This is an API diff-based source identity finding, not a recursive native build certificate.

The preceding v39 report was retrieved from `review/a2-v39-external-harsh-top4-2026-09-13`; its head was verified as `788cfbd08e30d795ffabef77b166d43ab01caaac`. It reviews `dd0e5ae…`. The new review branch is based on the reviewed submission, not on an assumption that the author's branch contains that referee branch.

## 2. Source register and read coverage

All links below are immutable. Except S01 and the explicitly separate report/workflow sources, paths are in the reviewed v40 tree. Inherited text was read at the parent and transferred only after the exact two-path comparison. Mathematical labels, rather than generated section numbers or unseen PDF page numbers, are used in the report.

### S01 — revision delta and identity

[Reviewed commit](https://github.com/TrillionniumFoundation/theta-theory/commit/070aa946fb28001916ad1bbd3503afa5f6cae3b3) · [complete comparison](https://github.com/TrillionniumFoundation/theta-theory/compare/dd0e5aefd49d200652afc3fc3f29f7a6f38ae326...070aa946fb28001916ad1bbd3503afa5f6cae3b3) · [native main](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/main.tex).

Coverage: complete commit delta and metadata; predecessor native entry and its full input list. The added v40 input and revision metadata were checked in the complete patch. The abstract is unchanged by this delta.

### S02 — new rerooting proof

[article/23b1_signature_rigid_rerooting_v40.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/article/23b1_signature_rigid_rerooting_v40.tex).

Blob `a658cbed21f80dd1b79b97e0c026b2127833a239`. Complete 66-line source read. Main target: `lem:v40-signature-rigid-rerooting` and its application paragraph.

### S03 — analytic signatures and periodic gluing

[article/23b_intrinsic_multichannel_rigidity_v28.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/article/23b_intrinsic_multichannel_rigidity_v28.tex).

Blob `7930d5deac7c53c50aef2e90f90aeb426c10a77d`. Main definitions and proofs examined, with a separate closing-range retrieval. Targets: `lem:v23-signature-symmetry`, gluing constraints/admissibility, `thm:v23-intrinsic-table-rigidity`, `lem:v23-cycle-holonomy`, and the rooted-tree definition and corollaries.

### S04 — metric-free lattice and table determination

[article/23d_rank_two_lattice_recovery_v24.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/article/23d_rank_two_lattice_recovery_v24.tex).

Blob `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c`. Complete source examined. Targets: common-frame definition, metric-free holonomy, `thm:v24-lattice-gram-recovery`, `thm:v24-uncalibrated-periodic-rigidity`.

### S05 — common-orientation quotient

[article/23h_global_orientation_quotient_v29.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/article/23h_global_orientation_quotient_v29.tex).

Blob `ac9938ee655b8b63f069a0c79c467d227eca5ab1`. Complete source examined: orientation character, gluing equivariance, two-sector quotient, holonomy/stability statement, and folded-record distinction. The separately cited transported-anchor extension was not fully rederived in this round.

### S06 — finite analytic signature stability

[article/23e_signature_stability_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/article/23e_signature_stability_v25.tex).

Blob `62a9df01937f97a33d405426842f25e85b1358b0`. Main source and closing range examined. Targets: uniform finite embedding, unique noisy match, graph propagation, compact inverse modulus, and the explicit distinction between a product-metric tail and an analytic-continuation rate.

### S07 — nonlinear half-line factorization

[v4/10_boundary_layers.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/v4/10_boundary_layers.tex).

Blob `892a88e37a24e591fa525013c41910c791e28e73`. Lines 1–245 examined: Green normalization, half-line construction, trace perturbation and principal factorization proof through its exponential comparison. This is not a claim to have re-read every later section in this file or every earlier finite-geometry dependency.

### S08 — signed jet inverse

[article/23a_signed_endpoint_rigidity_v27.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v27.tex).

Blob `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e`. Read in overlapping ranges 1–235, 235–520, and 500 through the end. Coverage includes theorem, quadratic recovery, weighted inverse, finite envelope, smooth remainder factorization, homogeneous isolation, last-jet block, tangent isomorphism, and completion. The density four-ratio inverse is described in the introduction and prior report; its separate full chapter was not re-audited here.

### S09 — two-speed count–endpoint experiment

[article/18d_count_endpoint_multirate_v32.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/article/18d_count_endpoint_multirate_v32.tex).

Blob `6014dec05ec24fe67a2d59062ea94e96d0518f0f`. Main source and range 255 through the end examined. Count likelihood expansion, exact waiting-law comparison, product decomposition, fast mark removal, and cap/transfer composition checked. Several cited local physical realization, transfer, finite-likelihood and compact-endpoint lemmas remain dependencies rather than newly rederived results.

### S10 — two-sided moving-ceiling comparison

[article/18c1_endpoint_time_deficiency_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/article/18c1_endpoint_time_deficiency_v25.tex).

Blob `e03e7eb7e450e6c467f898444d8b72b5fddfd093`. Complete source examined. Targets: explicit bulk relative bound, layer/corner estimates, forward and reverse kernels, projective interpretation. The broader endpoint–time application has not been independently rebuilt from every prerequisite.

### S11 — common domination and observed-type position comparison

[article/18f_domination_and_position_comparison_v27.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/article/18f_domination_and_position_comparison_v27.tex).

Coverage: common-reference proposition, dominated-input/disjoint-output lemma, observed-type dichotomy and its proof, matched-time remark, and visible explicit examples. The fetch was truncated at the end of the final example discussion; no coverage of unseen trailing material is claimed.

### S12 — principal claims and bibliography

[article/01_introduction_v27.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/article/01_introduction_v27.tex) · [v5/references_v25.tex](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/v5/references_v25.tex).

Coverage: introductory relative-law and single-offset statements, global observation protocol, physical/position benchmark distinction, and visible local-information discussion; the long introduction fetch was truncated later in that discussion. Bibliographic entries for the cited comparisons were read. This is not an exhaustive audit of all references or a priority search.

### S13–S14 — stale current entries

S13: [root README](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/README.md), blob `3dea5fd278c24291822aaaa49feb6781d28898fc`.

S14: [paper README](https://github.com/TrillionniumFoundation/theta-theory/blob/070aa946fb28001916ad1bbd3503afa5f6cae3b3/papers/A2-v17-boundary-information-coarsening/README.md), blob `dd02e43f8ceb40631e87ad4dfcd3b12a76453383`.

Both retrieved in full at the predecessor and unchanged in the complete v40 delta. They designate v38 and explicitly state C2 is open. Their reports of earlier software regressions, fixtures and a seven-page companion build are author evidence, not fresh referee executions.

### S15 — preceding referee report

[The v39 report](https://github.com/TrillionniumFoundation/theta-theory/blob/788cfbd08e30d795ffabef77b166d43ab01caaac/reviews/a2-v39-external-harsh-top4-2026-09-13/REFEREE_REPORT.md), blob `28e808050a46340f395cbaaa3bc88fe52deca475`.

Read in a main fetch and a separate range 155–340. Its C2 and R39-I1 dispositions are directly relevant. Its positive results about compact experiments, original-alternative moments and global acquisition are not silently converted into fresh executions or an exhaustive audit in this round.

### S16–S17 — fresh workflow metadata

S16: [runs filtered by v40 head](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs?head_sha=070aa946fb28001916ad1bbd3503afa5f6cae3b3&per_page=10) returned `{"total_count":0,"workflow_runs":[]}`. This query did not filter to pull-request events. It is a metadata observation at retrieval time, not a proof that no local build exists anywhere.

S17: [v39 run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34748124986), [job metadata](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34748124986/jobs), and [artifact metadata](https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34748124986/artifacts). Freshly observed: one job `103699693209`, conclusion `failure`, `steps: []`, `runner_id: 0`, and zero artifacts. These refer to v39 commit `dd0e5ae…`, not v40. No executed TeX command or cause of failure is established by this metadata.

## 3. External primary sources

These arXiv abstract/version records were consulted on September 13, 2026. No full-paper proof comparison or PDF analysis is claimed. The report uses them for bounded statements about the data maps and recorded results, not to claim subsumption or a proof gap in A2.

- **L1:** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4). The record describes analytic open non-eclipse billiards, with symmetry/genericity conditions. Related publication DOI: `10.1007/s00222-023-01191-8`.
- **L2:** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1), October 21, 2025. The record describes an enriched marked length spectrum and finite-horizon Sinai billiards.
- **L3:** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), June 3, 2021. The current record states the smooth-conjugacy consequence and explicitly records removal of the earlier open-billiard spectral-rigidity result after a mistake in Proposition 3.1. Earlier broader claims are not used as established geometric rigidity.
- **L4:** A. Meister and M. Reiss, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, [arXiv:1101.5248v1](https://arxiv.org/abs/1101.5248v1), January 27, 2011. The record describes equivalence to Poisson processes containing the target curve as a support boundary.

## 4. Actual independent execution

The final script has SHA-256 `550cddf5fb5b759155fdeb0418b61b50d43937ce8a6dabd697e366b2d39d560f`.

The two executions were started at `2026-09-13T09:44:11.727593+00:00` and `2026-09-13T09:44:12.495128+00:00`, using Python 3.13.5. Both returned zero; both stderr streams were empty. The stdout SHA-256 was identical in both modes: `a4261c52a25bb309129e4a79226e7d7af0eb923095242ad7f5ff5c75fcabef77`. The canonical identical stdout is archived as `RESULTS.json`; a second identical payload and empty stderr files need not be duplicated in Git. `EXECUTION.json` records their generated local filenames and hashes.

Reproduce from the review directory:

```sh
python3 independent_checks.py > normal.json
python3 -O independent_checks.py > optimized.json
cmp normal.json optimized.json
```

The script uses the Python standard library and explicit exceptions. It imports no repository mathematics. Its tests are:

| Control | Executed scope |
|---|---|
| Half-line Green kernel | 768 exact rational recurrence/unit-jump cases, both contact parities |
| Last-jet blocks | 108 exact rational determinant and inverse checks |
| Lattice and reflection | Four exact examples including nonprimitive marked cycle matrices |
| Geometric waiting laws | 15 Hellinger-bound checks; maximum computed ratio to bound about 0.947856 |
| Quadratic moving-ceiling model | 12 exact layer/corner calculations; bulk laws coincide in this model |
| Rerooting | All 146 labelled trees on at most five vertices, 3,134 valid original root/rigidity assignments, 11,741 reroot checks |
| Negative controls | Symmetric new-root failure when its required hypothesis is dropped; bulk separation despite unchanged trace when the stronger bulk bound is dropped |

The negative controls are not counterexamples to the manuscript. The final script was rerun in both modes after adding the v40 rerooting check and updating the reviewed source identity. Its inherited algebra/probability controls were unchanged by the author's two-path revision.

## 5. Limitations and repository-write scope

This review did not materialize a full checkout, execute the author's regression suite, build the native main or companion, inspect any native PDF, or certify recursive source completeness. A local Git transport attempt failed because hostname resolution was unavailable; repository reads and writes used the connected GitHub tool. This did not prevent the source audit or the independent local controls.

Not freshly exhaustive: the full auxiliary compendium; all finite-itinerary and flux dependencies; the complete single-offset density chapter; the transported-anchor extension; all physical-realization and stopped-transfer dependencies; every compact local Gaussian likelihood lemma; and the complete charged global-acquisition proof. The prior report's discussion of those subjects is identified as prior evidence, not substituted for a new proof audit.

The review writes only a new review directory on a new branch. It does not edit the manuscript, overwrite prior reports, merge a branch, change permissions, or act for a journal. The report, this ledger, the independent script, canonical results, and execution record form the review deliverable.
