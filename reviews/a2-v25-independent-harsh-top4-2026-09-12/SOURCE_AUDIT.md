# Source and execution audit for the A2 v25 review

## Immutable source control

Repository: `TrillionniumFoundation/theta-theory` (accessed through the authorized GitHub connector).

Reviewed branch: `revision/a2-v25-observable-calibration-signature-top4-2026-09-12`.

Reviewed commit: `3143762fc98373f93dbb8884c5ece005229ca50b`.

Reviewed root tree: `49533eaab9713370aecd69940a914dc5bc57cffe`.

Previous review tip: `8129defd970bbc1e011bb480b70603d39a31324d`.

Previous reviewed manuscript: `c35b31b1924a1621374eab72ee60e4cb5ab37df5`.

GitHub's comparison returned twenty commits ahead, zero behind, and eighteen changed files between the previous review tip and the reviewed v25 head. The new review branch was created from the exact reviewed commit, not from the default branch or an older manuscript. The review adds files only below `reviews/a2-v25-independent-harsh-top4-2026-09-12/`.

The native directory retains its historical name, `papers/A2-v17-boundary-information-coarsening`; that name is not the manuscript version. In the tables below `P` abbreviates this directory.

## Newly activated mathematical sources inspected

The complete text of the eight newly activated v25 mathematical modules below was inspected through the connector. Truncated returns were supplemented by line-range reads. Inspection of source is not execution of a source-graph checker.

| Source relative to P | Git blob returned by the connector |
|---|---|
| `main.tex` | `43f0acac5e8858df81e6c5c389f0c5adde05ac96` |
| `article/01_introduction_v25.tex` | `95e35a4673578d404221c86c9bdaab7b8d540fcd` |
| `article/01a_protocol_scope_v25.tex` | `3e19ab73be61d9e9c7997eec4fdb208ab963f13d` |
| `article/18c1_endpoint_time_deficiency_v25.tex` | `e03e7eb7e450e6c467f898444d8b72b5fddfd093` |
| `article/23e_signature_stability_v25.tex` | `62a9df01937f97a33d405426842f25e85b1358b0` |
| `article/25a_common_observables_v25.tex` | `82df03f99c1d6ac322161381e063d2f107f048ed` |
| `article/25b_augmented_global_reconstruction_v25.tex` | `df57b1fd46429349255a46779daf8446632520a0` |
| `article/25c_analytic_variation_bundles_v25.tex` | `e2eb1b88ab3944c033984162d1f0c5164d8c2b67` |
| `article/29a_signed_one_flight_benchmark_v25.tex` | `8aebfdef0afa1574dec884b26905cd1024a4364d` |

Also read: root README; `P/ACTIVE_SOURCE_MANIFEST_V25.md`; `P/RESPONSE_TO_REFEREE_V25.md`; `P/VERIFICATION_V25.md`. The substantive preceding v24 report was inspected, including its detailed M1–M3 arguments and further technical requests. A complete byte-level audit of its trailing bibliography was not performed.

## Selected inherited dependencies inspected

| Source relative to P | Coverage | Git blob |
|---|---|---|
| `article/23a_signed_endpoint_rigidity_v22.tex` | Lines 1–450: stated inverse, weighted construction, envelope, homogeneous isolation, jet blocks and tangent inverse | `facc0674006967debca05ab4196002e8a7f5b886` |
| `article/23d_rank_two_lattice_recovery_v24.tex` | Complete source | `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c` |
| `article/23b_intrinsic_multichannel_rigidity_v23.tex` | Lines 1–190: data, signatures, gluing definitions and classification | `0146f25a95d9cdb92cb09f4b6916d4d153cedeaf` |
| `article/18a_vector_boundary_information_v22.tex` | Lines 1–220: density setup, support-exclusive mass, common collar, stated LAN setup | `f0f79ad0bd3ccbb91c3e0b374d355d917e253162` |
| `article/02_finite_results.tex` | Complete statement module, not all historical proof dependencies | `7b5a66b2a5c6de8a3f1711f8a87278dbcb3eaae9` |

No claim is made to have independently verified every retained appendix, the entire old relative-operator proof chain, or every local LAN and count-experiment proof. The report distinguishes provisional credit to inspected mechanisms from certification of all inherited results.

## Native build inspection

The exact-head Actions query returned run `34662232834`, named `A2 v25 complete native build`, on the reviewed branch and commit. Its observed status was `queued`, with null conclusion. The returned creation/update timestamps were `2026-09-12T00:37:08Z` and `2026-09-12T00:37:09Z`.

No complete native build was executed in this review. No PDF page count, PDF hash, unresolved-reference count, or successful complete source-graph check is asserted. The private source was readable through the connector, but a local Git checkout attempt could not resolve the GitHub host. No inference about repository permission failure or a LaTeX failure follows from that environmental limitation.

The author's verification record says that its 337-case run used `--math-only`, rather than the full recursive source modes. This review did not rerun that author's script. Its claimed execution is therefore attributed to the author's record, not counted as independently repeated evidence.

## Independently executed diagnostics

Runtime: Python 3.13.5. Standard library only; no network, manuscript imports, randomness, or `assert` statements.

Executed commands:

```sh
python independent_checks.py > INDEPENDENT_CHECKS.json
python -O independent_checks.py > INDEPENDENT_CHECKS.optimized.json
cmp INDEPENDENT_CHECKS.json INDEPENDENT_CHECKS.optimized.json
```

All succeeded. The two output files were byte-identical. Only one copy of the identical JSON output needs to be committed. There are 126 cases, as enumerated in the output; a case may contain several individual checks.

Script SHA-256: `a9ae0911fa17c7547c6ffd656eb755f8cc2953232d158fb27cecdce3a9e8cdd9`.

The examples verify selected exact identities, interpolation scaling, finite jet-evaluation ranks, and support/domination witnesses. The circle witness is local and registered, not a signature-rigid global billiard counterexample. The oval calculation verifies the displayed positive curvature-radius lower bound, not realization of a whole periodic network. The finite computations neither prove nor disprove the full manuscript.

## External-source scope

The primary arXiv records for De Simoi–Kaloshin–Leguil (1905.00890), Finamore–Leguil (2510.18983), and Meister–Reiss (1101.5248) were checked for the limited comparisons and bibliographic information in the report. No exhaustive novelty search, complete proof audit of those papers, or PDF analysis is claimed. All theorem-level objections to v25 are grounded in the pinned repository sources or in calculations supplied directly in the report.
