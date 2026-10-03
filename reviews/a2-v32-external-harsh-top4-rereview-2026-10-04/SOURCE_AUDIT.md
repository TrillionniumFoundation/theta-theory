# Source audit for the external A2 v32 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Directory: `papers/A2-v32-adaptive-scalar-boundary`

The reviewed source is identified by Git objects:

- branch: `revision/a2-v32-adaptive-scalar-boundary-2026-10-04`;
- equivalent alias: `revision/a2-v32-referee-copy-2026-10-04`;
- author head: `eeb171d4e00242c9813c10e2124556b2cee480d3`;
- repository tree: `1c36f869ff4e875a0c6c8ecabbd8a38169e47c66`;
- native paper tree: `2a7d949f43dcb7b84d4a85ef8a4436349f615493`;
- mathematical checkpoint: `7044eb0a7e4bfe9c33f67c8d93e006f02d09cedc`;
- commit date: 3 October 2026 UTC;
- paper date: 4 October 2026.

A complete search of A2 revision branches at review time returned no branch later than v32.

The review branch
`review/a2-v32-external-harsh-top4-rereview-2026-10-04`
was created directly from the reviewed author head. It adds files only below
`reviews/a2-v32-external-harsh-top4-rereview-2026-10-04/`.
No author source, retained volume, previous report, workflow, or unrelated paper was edited.

## 2. Controlling report and retained source

The controlling preceding report is:

- branch: `review/a2-v31-external-harsh-top4-rereview-2026-10-04`;
- report commit: `f2e2a13a9a742c412a4b1a59b43388a2ba385bda`;
- report blob: `bf7aed23b625e7a18a77c9f21b47d067f82cb212`;
- reviewed v31 author head: `27d109b0eba6a03d453834ef9da9418446ac637d`.

The v32 checkpoint is based directly on the v31 external-review head.

The exact complete v31 manuscript is retained in v32 at
`papers/A2-v32-adaptive-scalar-boundary/retained/v31`
with tree
`ff74e5124141dc46b0f08f7e38a5cf258b87e642`.
Its active v31 core tree is
`aa9026847310ecd9205fe631b5ed85aa141b70ed`.

## 3. Active files inspected

The rereview inspected:

- `main.tex`;
- `core/00_setting.tex`;
- `core/01_local_queries.tex`;
- `core/02_adaptive_boundary.tex`;
- `core/03_period_recognition.tex`;
- `core/04_information_bound.tex`;
- `core/05_comparison.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `README.md`;
- `SOURCE_PINS.json`;
- `SUBMISSION_MAP.md`;
- `tools/adaptive_scalar.py`;
- `tools/verify_v32.py`;
- `tools/test_contract.py`;
- `tools/validate_v32.py`;
- `verification/local/receipt.json`;
- `.github/workflows/a2-v32-verify.yml`.

The prior v31 report and the retained v31 theorem package were read where needed to distinguish new v32 claims from inherited statements.

## 4. Mathematical delta from v31

Version 32 adds the following active mathematical content.

### 4.1 Local occupation queries

A target occupation value is approximated from a fixed-depth dependency diamond of the killed compass Bellman recursion. Each dependency location uses only two pooled reciprocal Bernoulli means. The number of centers per occupation query is prior-dependent but independent of the localization scale.

### 4.2 Adaptive boundary reconstruction

A fixed coarse acquisition produces complete protected components, interior centers, and isolated radial brackets. Fine reconstruction uses radial bisection with labels that may be arbitrary inside a controlled boundary layer, followed by degree-six interpolation. The resulting attempted-bit upper bound has power
`\nu^{-1/(4+\beta)}`.

### 4.3 Period recognition from the reconstructed patch

The current primary includes the protected-patch zero test, known-margin finite locking, exact bounded-denominator relations, Hermite basis recovery, primitive orbit count, and approximate Euclidean period basis.

### 4.4 Physical binary-information lower bound

An explicit fixed-period two-species packing contains exponentially many `C^{6,\beta}` bodies separated in laboratory `C^2` loss. A binary-transcript leaf argument gives the necessary power
`\nu^{-1/(4+\beta)}` for a uniform deterministic cap at fixed confidence.

## 5. Independent diagnostics

The review's `verify_review.py` imports no author code. Its ordinary and optimized executions are byte-identical. It performs 142,820 checks:

| Group | Checks |
|---|---:|
| reciprocal identities | 86 |
| contact Hessian | 10,880 |
| finite mean-exit and Bellman models | 46,814 |
| dependency and interval propagation | 16,632 |
| relaxed bisection | 51,132 |
| polynomial reproduction/noise | 3,780 |
| exponent and packing algebra | 78 |
| period subgroup arithmetic | 15,925 |
| binary transcript counting | 924 |
| finite query/attempt accounting | 485 |
| **Total** | **142,820** |

The arithmetic is exact integer/rational arithmetic except for explicit finite logarithm comparisons in the resource-accounting checks.

These diagnostics do not certify the continuum geometry, physical instrument, compactness, smooth interpolation estimates, literature novelty, TeX package, or editorial recommendation.

## 6. Author local evidence

The committed local receipt records:

- `status: passed`;
- 11,647 finite mathematical/source checks;
- 42 validation-contract checks;
- identical normal and optimized outputs;
- a 13-page primary;
- no final TeX diagnostics;
- `scope: primary_only`;
- `execution_kind: source_content`;
- no physical sensor execution;
- no formal proof certificate;
- no local claim of hosted full-package qualification.

The source manifest in that receipt agrees with the v32 source-pin manifest.

## 7. Hosted exact-source qualification

Workflow:
`.github/workflows/a2-v32-verify.yml`

Reviewed-head run:

- run ID: `37153403982`;
- head SHA: `eeb171d4e00242c9813c10e2124556b2cee480d3`;
- status: `completed`;
- conclusion: `success`;
- document count: fifteen.

The job successfully completed:

1. exact triggering-SHA checkout;
2. current and retained entry-point checks;
3. dependency installation;
4. all-fifteen-document qualification;
5. native-source and evidence archiving;
6. artifact upload.

The resulting artifact is:

- artifact ID: `11284767618`;
- name: `A2-v32-eeb171d4e00242c9813c10e2124556b2cee480d3`;
- digest: `sha256:7ac54169b32de69ee84f647b17d4552bda98d49aec52ba68adf326a90773f7b1`;
- state at audit: not expired.

The successful hosted run establishes source delivery and compilation evidence. It does not certify the mathematical proofs or apparatus.

## 8. Scope and limits of this audit

This was a targeted external rereview of the new v32 contribution and its dependency chain, not a formal re-proof of every theorem in the nested multi-volume programme.

The audit concentrated on:

1. whether the v31 lower-bound objection was actually answered;
2. the reciprocal-to-membership local-query reduction;
3. the adaptive radial reconstruction and rate balance;
4. protected-patch period recognition;
5. the physical packing and binary-transcript lower bound;
6. exact-source qualification;
7. the requested top-four significance standard.

No exhaustive literature or priority search was performed. No physical sensor was executed. The finite diagnostic script is not a proof certificate.

## 9. Audit conclusion

The source object is unambiguous and reproducibly pinned. Version 32 is a real mathematical revision, preserves the complete reviewed v31 source, and passes its exact-SHA fifteen-document qualification.

The new adaptive upper bound and physical binary lower bound are supported under the stated active sensor contract and prior class. No fatal counterexample was found in the new core. The negative recommendation in `REFEREE_REPORT.md` is a top-four significance judgment, not a source-delivery objection or an assertion that v32 merely renames v31.
