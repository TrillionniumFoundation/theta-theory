# A1 v28 — localized acquisition and size-uniform memory

**Principal manuscript:** `main.tex`  
**Complete companion:** `companions.tex`  
**Revision branch:** `revision/a1-english-v28-localized-acquisition-2026-09-08`  
**Response:** `RESPONSE_TO_REFEREE.md`  
**Proof map:** `PROOF_LEDGER.md`

This revision answers the independent v26 report pinned at review commit `19fbf4fe0e7495afd537de73a63670a9cf5616e0`, which examined submission `a2e5d3737085241137211f1cf21393d5bcafa1ce`. It is based on the already existing v27 revision at `49dd2eddb09017c91eede14358cb873fe666f3cf`; that revision's contributions are retained, not republished as new v28 discoveries.

## Mathematical addition

A localized acquisition theorem replaces simultaneous regularity of every edge by regular witnesses on every cut of a compulsory level. It uses actual selected-edge subprobability densities before adaptive restriction and bounds the loss at one fixed boundary. Finite decoder side information is counted explicitly.

For independent copies of a fixed scalar experiment, a separately specified enlarged query menu retains the original tensor task with probability one half and adds local tests from the same exact future test space. All remaining raw trials are executed for either query type. On linear-size graph families satisfying the printed balanced-cut expansion condition, optimal persistent bits have order `|V| b(epsilon,a)` with constants uniform in graph size, calibration and sufficiently small resolution. The upper filter quantizes each edge only once. The paper proves existence of the required multigraph families and a joint graph-growth/calibration-collision corollary.

This is not an exact sharp cutwidth coefficient, a graph-uniform theorem for the tensor-only loss, or a result for arbitrary sparse graph families. Those are not substituted for the stated theorem. The original tensor-only results remain active and unchanged.

## Complete native source and preservation

Unlike a sibling-dependent overlay, this directory contains the complete inherited v26 native source tree, the v27 mathematical modules and the v28 addition. `main.tex` has no `../A1-english-v26` input dependency. The full companion is retained. The builder generates the inherited companion bibliography in a separate staging tree; it does not rewrite the principal bibliography or any source module.

`baseline-v26-main.tex`, `baseline-v27-main.tex`, `PROOF_LEDGER_V26.md`, `PROOF_LEDGER_V27.md` and `review-basis-v26/REFEREE_REPORT.md` preserve the relevant entry points, proof maps and controlling report. `provenance/v10-scheduling.tex` is the consulted original scheduling derivation. Earlier root-level v26 diagnostics and build receipts copied with the native tree are historical, not current verification results. Use only the explicitly versioned v28 records to determine current execution status.

`NATIVE_SOURCE_RECORD_V28.json` contains immutable Git identities. The original repository directories `papers/A1-english-v26`, `papers/A1-english-v27` and the v26 review directory remain unchanged. From a repository checkout their preservation can be checked with:

```sh
git diff --exit-code 49dd2eddb09017c91eede14358cb873fe666f3cf HEAD -- \
  papers/A1-english-v26 papers/A1-english-v27 \
  reviews/a1-english-v26-harsh-independent-2026-09-07
```

## Executed finite checks

```sh
cd papers/A1-english-v28
python3 diagnostics_v28.py --output validation/DIAGNOSTICS_V28.json
python3 -O diagnostics_v28.py > validation/DIAGNOSTICS_V28_OPTIMIZED.json
cmp validation/DIAGNOSTICS_V28.json validation/DIAGNOSTICS_V28_OPTIMIZED.json
```

The supplied session executed 6,600 explicit checks, with byte-identical normal and optimized output. They include exact graph-retention probabilities, genuinely nonconstant selected paths and losses, selected-edge marginalization, tail integration, the dimension-dependent factor 16, tensor damping, collision profiles and the graph construction's crossing means. Explicit exceptions enforce the checks. The count is a reproducibility record, not proof certification.

## Prepare and build the full native volumes

With Python 3.10+ and the TeX packages in `preamble.tex`:

```sh
python3 build.py --prepare-only
python3 build.py
```

All generated files go under `build-v28/`. `BUILD_RECORD_V28.json` records pinned-source verification, diagnostics, active-source label/citation checks and the actual TeX pass results. The full build uses five alternating passes of the principal article and companion, exporting only each volume's own theorem labels. An explicitly recorded staging-only conversion handles older `xr-hyper` without importing foreign bibliography numbers. No historical materializer is allowed to restore an earlier `main.tex`.

A successful native build still requires subsequent visual inspection of both PDFs. A missing engine, failed pass, unresolved citation/reference or overfull box is recorded as failure, not acceptance. The nine-page `new-results-extract.tex` validation target contains only the new modules and explicit inherited-reference locators; it is not the full principal manuscript.

## Session status

The new mathematical source was compiled as a nine-page extract and visually inspected. The full native two-volume build was **not executed** in this session. A GitHub Actions source-export attempt (run `34161161920`) failed without available step logs; the cause was not established. `validation/SESSION_RECORD_V28.json` records these boundaries. The workflow retained on the revision branch uses only `workflow_dispatch`; no subsequent run is represented as successful.

The next review should assess the full source, the point-by-point response and the nine new formal statements. No merge, approval, branch-protection change or permission change is part of this revision. The previous editorial significance judgment is not marked resolved by the author or by the diagnostic count.
