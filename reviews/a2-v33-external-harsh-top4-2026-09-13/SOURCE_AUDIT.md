# A2 v33 source, coverage and execution audit

Report date: September 13, 2026. This audit accompanies `REFEREE_REPORT.md` and defines the scope of its findings. It is not an author revision or a certificate of the entire manuscript.

## 1. Immutable review target and ancestry

Repository: `TrillionniumFoundation/theta-theory`.

Reviewed branch: `revision/a2-v33-finite-experiment-integration-top4-2026-09-13`.

Reviewed commit: `b577cffcb3ca5597cb4905269bea9de3bd4ead38`.

Reviewed tree: `425e794b942e4da497e51c0003fb98748e0019a9`.

Commit timestamp returned by GitHub: `2026-09-12T16:52:29Z`. The manuscript and branch use a September 13 version date; this is not the commit timestamp.

Parent review commit: `8b7643b6e8fc3e07d85bf1452e6d4838c3222a0b`.

Previous assembled author submission: `a4fe5c11f18070fc03d878ba683e014b48e921af`.

Review branch created directly from the reviewed commit: `review/a2-v33-external-harsh-top4-2026-09-13`.

All source paths below refer to the reviewed commit, not to the moving branch head. Define `P = papers/A2-v17-boundary-information-coarsening`. The immutable source root is [the reviewed tree](https://github.com/TrillionniumFoundation/theta-theory/tree/b577cffcb3ca5597cb4905269bea9de3bd4ead38).

The report and diagnostics are to be added only under this new review directory. They do not amend any manuscript, README, historical report, workflow, branch protection or permission. No merge or pull-request approval is part of this review.

## 2. Authenticated revision delta

GitHub comparison of parent review `8b7643b6e8fc3e07d85bf1452e6d4838c3222a0b` with submission `b577cffcb3ca5597cb4905269bea9de3bd4ead38` returned: ahead by one, behind by zero, twelve changed paths, no deleted file.

The active changes are `P/main.tex`, `P/article/01_introduction_v27.tex`, `P/article/18a_vector_boundary_information_v26.tex`, `P/article/18b_raw_physical_multirate_v22.tex`, and `P/article/18d_count_endpoint_multirate_v32.tex`.

Historical additions are root `README_PRE_V33.md`, `P/README_PRE_V33.md`, and five files under `P/history/v32/`: the prior main and the four changed article files.

Neither root `README.md` nor `P/README.md` was changed. Their actual contents were fetched independently and both still identify v32. No new v33 response or verification file appears in this revision delta. This observation concerns the authenticated delta and the active navigation; it is not an exhaustive search for every historical record in the repository.

## 3. Source keys and inspection coverage

| Key | Immutable path or resource | Coverage and use |
|---|---|---|
| S1 | Commit/ancestry metadata and authenticated parent-to-submission comparison | Target identification, timestamp and twelve-path delta |
| S2 | `P/main.tex` | Full source read: title, v33 identity, abstract, active inputs and appendix entry |
| S3 | `README.md` | Full source read: stale active v32 identity and navigation |
| S4 | `P/article/01_introduction_v27.tex` | Full text read in two ranges: theorem claims, observation hierarchy, new compact integration and significance comparisons |
| S5 | `P/article/18a_vector_boundary_information_v26.tex` | Full text read in consecutive ranges: collar and LAN estimates, new finite-likelihood lemma, Gaussian normalization, compact references, alternative-risk paragraph and Hellinger stability |
| S6 | `P/article/18a1_compact_experiments_v32.tex` | Full text read: finite-net kernels, moduli, singular Gaussian range and fixed-window compact corollary |
| S7 | `P/article/18d_count_endpoint_multirate_v32.tex` | Text read with overlapping and closing-range fetches: success expansion, exact waiting laws, finite likelihood application, product kernels, caps, finite transfer and explicit transverse output |
| S8 | `P/article/18b_raw_physical_multirate_v22.tex` | Lines 307 through end inspected, including the changed fixed-window theorem and stopped/pilot transfer statements. Earlier realization, design and density-reduction proofs in this file were not freshly rederived |
| S9 | `P/article/18c1_endpoint_time_deficiency_v25.tex` | Full text read: support and relative-bulk hypotheses, layer and corner bounds, forward and reverse kernels, batch and projective interpretation |
| S10 | `P/article/23e_signature_stability_v25.tex` | Full text read including closing range: finite uniform embedding, C2 noisy matching, graph propagation, compact inverse modulus and its qualifications |
| S11 | `P/article/25b_augmented_global_reconstruction_v26.tex` | Separator, template, capped acquisition and increasing-order/budget arguments read; conditional use of earlier calibration and inverse results explicitly retained |
| S12 | `P/article/23f1_equivariant_density_extension_v29.tex` | Full text read: transported anchor, off-model formula domain, same-sector stability and finite-jet equivariance |
| S13 | `P/article/23h_global_orientation_quotient_v29.tex` | Full text read: tagged lattice orientation, common reflection, gluing equations, quotient stability and distinction from folded records |
| S14 | `P/README.md` | Full text read: stale v32 branch, source/review chain, response and verification pointers |
| S15 | `P/VERIFICATION_V32.md` | Full text read: explicit C2 nonclosure, isolated five-page fixture and prospective native execution record; these are author-reported prior executions, not executions by this reviewer |
| S16 | `.github/workflows/a2-v32-native-build.yml` | Full text read: push filter restricted to v32, native targets, source/product retention and intended commands |
| S17 | `P/article/99_auxiliary_compendium_v19.tex` | Complete input list read; thirty-six active auxiliary inputs identified. Their individual proofs were not collectively audited |
| S18 | `P/v7/30_count_lower_bounds.tex` | One active appendix spot-checked: conditional indistinguishability input, stopped adaptive entropy bound and two-point risk lower bound; physical family construction remains an imported dependency |
| S19 | Actions branch/run/job/artifact queries described below | Direct execution-status evidence, not manuscript compilation |
| S20 | `reviews/a2-v32-external-harsh-top4-2026-09-12/REFEREE_REPORT.md` | Previous dispositions and requested M1–M3 response examined, including its stated review limitations |

Selected Git blob identities returned by the authenticated file fetches:

| Source | Git blob SHA |
|---|---|
| S2 | `afb1ef7c3ca0e6f767b7ecf1a53d356a97c3dc5d` |
| S3 | `f971281eac847ad2078bd8122672b95bd43707f1` |
| S4 | `4bf96b3ad9f77c0671a7142e8f4baad3db3f560b` |
| S5 | `c036b730155d55420b92980a20abd40812ba7811` |
| S6 | `176e2588344ce0646ed47c09c64f371d6d16a045` |
| S7 | `6014dec05ec24fe67a2d59062ea94e96d0518f0f` |
| S8 | `c593b7b656b197bc2b063a99a282dfae3567ac91` |
| S9 | `e03e7eb7e450e6c467f898444d8b72b5fddfd093` |
| S10 | `62a9df01937f97a33d405426842f25e85b1358b0` |
| S12 | `f90531eae71f43486029a7dd042c249627aa22b8` |
| S13 | `ac9938ee655b8b63f069a0c79c467d227eca5ab1` |
| S14 | `a5dc1d9bef6bf3e49ae57e771b0c7ffc10b49c30` |
| S15 | `8a4aa69d0fd10faabbba6bd3c3c7461fa5447b36` |
| S16 | `e5aa0d0cc7edf3aceb34c869b7f280a16de77f4f` |
| S17 | `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` |
| S18 | `22f4488967560b36d17b3ac7ca664d9e50dfbd14` |
| S20 | `6398eda3ef920e8cc92653ac0f219b5649045499` |

The immutable commit plus full path also pins S11; no unobserved blob identity is supplied for it.

## 4. Explicit exclusions from certification

The report does not certify every active manuscript theorem. In particular, this round did not independently reconstruct all finite stationary bridges, Green/cofactor formula foundations, nonlinear relative factorization estimates, all-order half-line envelope arguments, physical calibration proofs, complete analytic incidence classification, direct-position benchmark, companion manuscript or auxiliary chapters. Their statements and uses are distinguished from the modules checked in detail.

The previous report's positive relative-law and all-order contact-inverse assessments are historical evidence of that earlier review's scope, not new proof verification by this round. Similarly, checking the algebra of orientation transport does not certify every geometric realization in the gluing space.

No complete native source graph was assembled locally. No full-native `main.tex` or `two_collision.tex` compilation was attempted by this reviewer. No manuscript PDF, bibliography-resolution log or complete typeset page count was inspected or certified. No unresolved-reference count for the current native manuscript is asserted. The sixteen external labels mentioned in S15 belong to the author's explicitly isolated v32 fixture, not to a newly tested v33 main.

## 5. Authenticated execution observations

The GET query

```text
https://api.github.com/repos/TrillionniumFoundation/theta-theory/actions/runs?branch=revision%2Fa2-v33-finite-experiment-integration-top4-2026-09-13&per_page=5
```

returned `total_count: 0` and an empty workflow-run list. This is a branch-filtered Actions observation, not a claim that an unrecorded local build cannot exist.

For the existing v32 run `34701204570`, fresh connected-tool reads returned:

```json
{
  "run_id": 34701204570,
  "latest_returned_job_id": 103583939776,
  "job_name": "native-build",
  "status": "completed",
  "conclusion": "failure",
  "steps_returned_by_job_step_query": [],
  "artifacts_returned_by_run_artifact_query": []
}
```

The calls used were `fetch_workflow_run_jobs`, `fetch_workflow_job_steps` and `fetch_workflow_run_artifacts`. The wrappers return the latest attempt/first page as documented. The job identifier differs from `103573170687` in S20, which described an earlier attempt. The new observations do not establish why the service did not execute steps, and do not establish a LaTeX failure. They are not a build of submission `b577cffcb3ca5597cb4905269bea9de3bd4ead38`.

Some generic GET routes were rejected by the connector's approved-path validation, including a direct job route. No contents or execution result was inferred from those rejected requests. No service settings, permissions or workflow files were changed to manufacture evidence.

## 6. Independently executed diagnostics

Environment actually used: Python 3.13.5. The script uses the standard library and explicit `require` checks rather than optimizable assertions.

Commands actually executed in the local review directory:

```sh
python3 diagnostics.py > diagnostics.json
python3 -O diagnostics.py > diagnostics.optimized.json
cmp diagnostics.json diagnostics.optimized.json
```

Both executions passed and their outputs were byte-identical. The optimized duplicate is omitted from the repository because it contains exactly the same bytes.

Recorded SHA-256 values:

```text
513d57c9a97ff5cfc9bc69c0dbf63e2d17be636c55eaf0a9158125bae301c5b1  diagnostics.py
4e36f2f26c430c44cef43c3848d72cbf0fc0dd77e5f7e2ba292241cc53b3236e  diagnostics.json
```

Local `git hash-object` values, also matched to the blobs created through GitHub:

```text
7c25d792516d580761466f442dc52385364d376d  diagnostics.py
aad01b86b83647b7e89aa7e3ff0d8f031e182682  diagnostics.json
```

The diagnostics cover finite normalized likelihood couplings and their total-variation bound; lost likelihood mass when limit normalization is removed; failure of finite-to-compact inference without a modulus; exact geometric and negative-binomial affinities; a corner-mass scaling identity; the nonzero bulk score information of an excluded O(k^-1/2) perturbation; an abstract C0 matching witness; and illustrative compatible rate sequences.

Exact rational equalities, mathematical witness arguments and floating-point rate illustrations are distinguished. In particular, the displayed finite rate values are not asserted already equal to their limits. The witnesses deliberately remove hypotheses present in the paper and do not constitute physical-table counterexamples. Running this script does not verify the source graph, prove any global billiard theorem, or close C2.

## 7. Literature check

The report's L1–L3 were checked through primary arXiv abstract/version pages. The comparison is limited to the stated setting, assumptions, observation maps and broad nonregular/Poisson connection. No full external proof or exhaustive priority audit was conducted, and no external PDF was inspected. The report asserts no later publication status for the 2025 preprint. These limitations apply equally to favorable and adverse novelty assessments.

## 8. Result interpretation

M1–M3 are closed; E1 remains closed for the stated compact local experiments. I1 is reopened as a current-version delivery regression. C2 remains unverified. R1 is a local, explicitly repairable moment-proof clarification, not a fatal counterexample. Positive module findings and passing diagnostics must not be promoted into a certificate for the complete article. Conversely, absent build evidence must not be promoted into a proof of mathematical falsehood.
