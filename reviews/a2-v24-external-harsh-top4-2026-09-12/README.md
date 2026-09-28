# A2 v24 — independent harsh top-four review

**Recommendation:** reject in the present form; substantial mathematical repair required before a fresh top-four assessment.

This is an author-requested AI-assisted independent referee-style report, not a journal-commissioned review or an editorial decision.

## Read first

[REFEREE_REPORT.md](REFEREE_REPORT.md) contains the full assessment, the preceding R3 closure matrix, precise source/theorem references, three principal proof objections, additional technical corrections, an analytic convex-oval witness, a signed one-flight benchmark, and conditions for the next review.

The report distinguishes demonstrated failures of particular implications from unproved theorem-level steps. It does **not** claim a counterexample to the complete analytic rigidity theorem. It credits the new rank-two lattice formula, Poisson reverse kernel, and intrinsic count quotient rather than repeating already addressed objections.

## Immutable review target

- Repository: `TrillionniumFoundation/theta-theory`.
- Source branch: `revision/a2-v24-uniform-physical-global-top4-2026-09-11`.
- Source commit: `c35b31b1924a1621374eab72ee60e4cb5ab37df5`.
- Previous manuscript comparison commit: `55b2d3b41acd3e0beb7e9071c13e54637137f9ad`.
- Review branch: `review/a2-v24-external-harsh-top4-2026-09-12`, created directly from the source commit.
- Date: September 12, 2026.
- Active manuscript directory: `papers/A2-v17-boundary-information-coarsening` despite the historical v17 directory name.

The review branch adds only files in this review directory. It does not revise mathematical claims in the manuscript, move the source revision branch, merge into main, or change repository policies.

## Independent reproducible diagnostics

The standard-library program [independent_diagnostics.py](independent_diagnostics.py) was executed under Python 3.13.5, normally and with optimization enabled. The two JSON outputs matched byte for byte. The checked program blob was read back from GitHub and matched the locally executed file.

From this directory:

```sh
python independent_diagnostics.py > /tmp/a2-v24-review-normal.json
python -O independent_diagnostics.py > /tmp/a2-v24-review-optimized.json
cmp /tmp/a2-v24-review-normal.json /tmp/a2-v24-review-optimized.json
cmp DIAGNOSTIC_RESULTS.json /tmp/a2-v24-review-normal.json
```

The checks do not use Python `assert`, so optimization does not disable them. They import no manuscript code and perform no repository writes.

| Diagnostic | Cases | Meaning |
|---|---:|---|
| Last-jet blocks | 100 | Exact rational determinant, inverse and half-line multiplicity sums |
| Rank-two lattice recovery | 6 | Exact recovery and Gram invariance, including non-unimodular marked pairs |
| Hyperbolic curvature derivative | 6 | Positive formula checked against finite differences |
| Leading action-Hessian/onset distinction | 2 | Same leading action Hessian at different gaps; not equal full-law examples |
| Finite-signature witness | 6 | Paired scalar signatures on an analytic convex oval; the report gives the analytical argument |
| Signed one-flight reconstruction | 20 | Exact local reconstruction algebra in the mixed-type observation model |

Committed execution output: [DIAGNOSTIC_RESULTS.json](DIAGNOSTIC_RESULTS.json).

SHA-256 of the executed script:

```text
de6bd7a788990161159333728e04b10032b718a9ea628297b9b763d7c35fdb5c
```

SHA-256 of the recorded JSON output:

```text
13531ce38650e10d4870058fdd7926b39e2b380635cdf87da4fb1ed879f637b9
```

Git blob identifiers computed locally for cross-checking the committed files:

```text
independent_diagnostics.py  f0c72f99433261888d6d8aabc096fe819c3d8f79
DIAGNOSTIC_RESULTS.json     e16c1656c77e238c0bf48d7a94025d97d702a79f
```

These diagnostics are not a proof certificate, a complete regression test of the manuscript, or evidence that the global physical theorem has been established.

## Principal v24 modules examined

Paths below are relative to the active manuscript directory and are pinned to the source commit above.

| Module | Git blob SHA |
|---|---|
| `article/01_introduction_v24.tex` | `213d0351c828f7a0b44c83092c459038fcd5ba8d` |
| `article/18c1_endpoint_time_deficiency_v24.tex` | `74c7ad1620c571da6b05ad9ba834d0f328c274ba` |
| `article/18d1_intrinsic_count_geometry_v24.tex` | `3dcfb2ec57ec9b6c1a5caecc5453a2028cc97f72` |
| `article/23d_rank_two_lattice_recovery_v24.tex` | `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c` |
| `article/23e_quantitative_gluing_stability_v24.tex` | `8920be04936e0f0e3173798ffe0cd5883712da76` |
| `article/25a_uniform_physical_global_v24.tex` | `f913aa42c35f95b4ab1953ab4fb5316551fbeca0` |

The source comparison against the preceding manuscript was ahead by eleven commits and behind by zero. It identified the new mathematical files, main-file changes, the response/prior-report records, and the native-build workflow. Inherited dependencies checked selectively include the signed all-order inverse, intrinsic gluing, fixed-coordinate realization, finite-to-boundary transfer, the local count model, the endpoint-time expansion, onset calibration, and the short-flight geometry. See the full report for precise links and labels.

## Mechanical verification boundary

At inspection, exact-head GitHub Actions run `34608745010` (`A2 v24 complete native build`) had job `103293603377` (`native-build`) still **queued**, with null conclusion and no executed-step result returned. This is neither a build success certificate nor a TeX failure.

No native build of the entire exact-head source graph, full unresolved-reference audit, or PDF inspection was performed in this review. The old auxiliary compendium was not exhaustively re-proved. The repository root README was stale, so revision selection used branch and source metadata instead.
