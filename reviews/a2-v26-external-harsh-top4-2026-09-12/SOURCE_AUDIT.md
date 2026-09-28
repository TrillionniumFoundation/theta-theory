# Source and execution audit — A2 v26 external review

## Frozen baseline

Repository: `TrillionniumFoundation/theta-theory` (private, read through the authorized GitHub connector).  
Author branch: `revision/a2-v26-single-offset-law-inverse-top4-2026-09-12`.  
Reviewed commit: `cefd89084682cc2e31d730eab1a4b8d8eaac0bbe`.  
Tree: `53d4ad26fcc4a84f427ef75ddb92b59c99c08d83`.  
Commit time: September 12, 2026, 01:58:15 UTC.  
Immediate parent: `157b246098f4a87f610ceb09337cbc3602b4cf48`.  
Prior v25 review ancestor: `47057587d104074f0e1dde54c1d5d6abb629378f`.  
Prior reviewed v25 author manuscript: `3143762fc98373f93dbb8884c5ece005229ca50b`.

Revision branches were inspected, including the continuation of the branch-search result. The latest located v26 branch was rechecked before publication of the report and still pointed to the reviewed SHA. The baseline is A2, not frozen statistical A1 v36. The comparison to the prior review reports two commits ahead, zero behind, and twelve changed files.

## Scope of mathematical reading

Let `P = papers/A2-v17-boundary-information-coarsening`.

The v26 mathematical delta comprises seven new modules. All were examined; the introduction was read across the commit diff and its later source range, and other long sources were retrieved in ranges as needed. The main entry point was read in full. The following blob identifiers pin that reading:

| Source | Git blob |
|---|---|
| `P/main.tex` | `a71285b0c1363c6aa950cde8fc498019a9478064` |
| `P/article/01_introduction_v26.tex` | `2d3496bbcc170f377143962c82058fe689559f6f` |
| `P/article/23f_single_offset_law_inverse_v26.tex` | `35f538eea4415951d1572cd9db76fdff429afa0a` |
| `P/article/18a_vector_boundary_information_v26.tex` | `352994ee96dec59bcc780bfa5ed6eace46b2025e` |
| `P/article/18c_full_endpoint_time_information_v26.tex` | `66aa7c911961b2f9b16c1d2d8cad292c19ba5c66` |
| `P/article/18f_domination_and_position_comparison_v26.tex` | `348d0b16179f2185d15f68807880db223f26ac30` |
| `P/article/29b_direct_position_benchmark_v26.tex` | `4f04d70a231008f8fb961a7282dbd3a5e02e2b0b` |

The complete `P/article/25b_augmented_global_reconstruction_v26.tex` mathematical text was also examined at the reviewed commit. Its response display truncated the blob metadata, so this audit does not invent a full blob hash. The immutable commit and exact path identify it unambiguously.

Selected inherited dependencies were examined, not the complete historical source graph:

* `23a_signed_endpoint_rigidity_v22.tex`, lines 1–450, blob `facc0674006967debca05ab4196002e8a7f5b886`: weighted half-line inverse, finite envelope, jet filtration, determinant blocks, fixed-order tangent inverse, and beginning of the final analytic argument.
* `25a_common_observables_v25.tex`, retrieved range through line 270, covering the common record, localization, capped pilot, projection, continuity and test implementation. The tool display cut off at the end of the last proof; no claim of reading omitted trailing material is made.
* `23e_signature_stability_v25.tex`, retrieved range through line 280, covering finite embeddings, noisy unique matching, gluing persistence and the compact-inverse argument. The tool display cut off near the end of that argument.
* `18_boundary_information_v18.tex`, lines 1–230, blob `28219d2513645b49a3ba307fb475fa4d5870a6a8`: scalar assumptions, collar moments, support-exclusive mass and critical likelihood proof.

The v25 referee report was read across its initial response and the later source range 180–380. Root and manuscript README files, commit/delta metadata, and the v26 changed-source diagnostic record were read. These materials are evidence about provenance and preceding objections, not mathematical certification.

## Important exclusions

There was no fresh proof-level audit of every input under `main.tex`, of the entire relative-operator construction, of the complete `99_auxiliary_compendium_v19.tex`, or of all historical branches. In particular the separately inherited `18c1_endpoint_time_deficiency_v25.tex` was not reread completely in this review; the v26 endpoint–time section's explicit dependence on it was examined and preserved in the report's qualification.

No complete native checkout, recursive whole-tree label/reference audit, full manuscript build, PDF analysis, or author's diagnostic-suite rerun was executed. No PDF page numbers, page counts, unresolved-reference counts or formal proof certificates are asserted.

The primary literature records in the report were checked online for the limited observation/hypothesis comparisons. They were not all reread at proof level, and the search is not claimed exhaustive.

## Findings and their status

| ID | Nature | Evidence / result |
|---|---|---|
| R1 | False-as-written auxiliary proposition | An even two-flight design starting on the fixed obstacle violates the asserted position singularity and common-nondomination conclusions. At matching endpoint-only record levels scalar and raw position laws have inverse parameter-independent maps. |
| R2 | Smooth/formal-jet clarification | The infinite Taylor equality is not valid for arbitrary smooth graphs. Finite remainders and the supplied envelope argument repair the intended finite-jet statement. |
| R3 | Submission integration and verification | README pointers remain v25; no new response/manifest in the v26 delta; exact-head workflow has no executed steps. |
| Positive finding | Single-offset inverse | Algebra and fixed-order interior stability are consistent in the inspected model; density-norm and sample-level assertions are distinguished. |
| Positive finding | Prior benchmark and budget repairs | Same-observation graph interpolation is now included, and the selected budget stage is explicitly restarted. |
| Optional strengthening | Corrected varying-obstacle experiment | The dominated-input/disjoint-support argument in the report gives deficiency exactly one for every finite positive sample size on an uncountable homothety interval. |
| Optional illustration | Support versus density | A support-preserving convex action gauge is constructed in the functional model, without claiming a physical-table realization. |

R1 is a missing observed-type hypothesis, not a refutation of the main inverse or the global two-type reconstruction. R2 is not evidence that the intended smooth finite-jet theorem is false. Optional results are not new mandatory acceptance conditions.

## Native workflow evidence

Run `34666361925`: `A2 v26 complete native build`, push event, head `cefd89084682cc2e31d730eab1a4b8d8eaac0bbe`, completed with `failure`.

Job `103478925267`: `native-build`, `steps: []`, `runner_id: 0`, empty runner name, label `ubuntu-24.04`; started at 01:58:33 UTC and completed at 01:58:35 UTC on September 12, 2026.

Read endpoints:

* `https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs?head_sha=cefd89084682cc2e31d730eab1a4b8d8eaac0bbe&per_page=20`
* `https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs/34666361925/jobs`

This proves no build step ran in that job, not that LaTeX failed or that a particular infrastructure cause was identified. The author record's `native_recursive_graph` value is `not_checked_in_this_mode`.

## Independently executed finite diagnostics

Program: `diagnostics/check_v26_referee.py`  
Result: `diagnostics/results.json`  
Python: 3.13.5  
Script SHA-256: `21833d91c202b91bf8d9f45d8964d562858ae4926ed0ab080f612d6ed71cc025`  
Git blob of executed script: `93ad02adfe8f9aa914e36ac6fb29f64c1833c547`.

The script was run in ordinary and optimized mode; output files were compared byte for byte and matched. The Git blob hash calculated from the local executed bytes agrees with the uploaded blob SHA. The script does not use `assert` for checks. The extra optimized output is not duplicated in this packet because it is byte-identical to the recorded result.

Reproduce from this directory:

```sh
python3 diagnostics/check_v26_referee.py > /tmp/a2-v26-review-normal.json
python3 -O diagnostics/check_v26_referee.py > /tmp/a2-v26-review-optimized.json
cmp /tmp/a2-v26-review-normal.json /tmp/a2-v26-review-optimized.json
```

There are 347 finite cases: 75 density inversions, 72 determinant blocks, 121 support-gauge grid cases, 27 numerical two-flight configurations, 12 interpolation scalings and 40 restarted budgets. The continuum counterargument and the measure-theoretic deficiency proof are in the report; finite cases are not their proof.

The author's 3343 cases are only an inspected author record here, not an independent rerun. No CI rerun, workflow modification, repository permission change, manuscript modification, deletion, merge, or journal-status change is part of this review packet. It adds review material on a separate branch based on the pinned author commit.
