# Source audit for the external A2 v22 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Reference-free certification from intrinsic boundary laws*  
Primary directory: `papers/A2-v22-reference-free-certified-recovery`

The reviewed object is identified by immutable Git objects:

- revision branch: `revision/a2-v22-reference-free-certified-recovery-2026-09-29`;
- equivalent source alias: `revision/a2-v22-referee-copy-2026-09-29`;
- reviewed commit: `ef51836da1744fc4a7133e3a3fd0e85848c73dc6`;
- reviewed repository tree: `cca7d5a3c6fb4028982e92f8c9a84d145ed302d3`;
- mathematical checkpoint: `3c6c6d6667d9a0506dc3de472498f21a4cb550d1`;
- commit date: 29 September 2026.

Both v22 revision aliases resolved to the same author commit when this review was frozen. No A2 v23 revision branch was present. The author head is one commit ahead of the mathematical checkpoint and adds the response, source binding, validation tools, local evidence, and exact-SHA workflow without altering the mathematical core introduced at the checkpoint.

The review branch

`review/a2-v22-external-harsh-top4-rereview-2026-09-29`

was created directly from the reviewed author head. It adds files only under

`reviews/a2-v22-external-harsh-top4-rereview-2026-09-29/`.

No author manuscript, revision branch, previous review, workflow on an author branch, or unrelated paper was edited by this review.

## 2. Prior report and retained source

The current source pins identify:

- latest frozen review commit: `b263abc35b2aacb038185d66c5cb13f488d3fe93`;
- reviewed v21 author commit: `5ab3be483386dab1b2f53575f47dbf7aebd92bd3`;
- v21 review report blob: `38f9de41c756221a86718e897ec548faecbfcff5`;
- exact preserved v21 paper tree: `a13f1cabd3bc11214bc92ecb6fb49ea51fde87bb`;
- exact preserved v18 tree: `3c558d7799e9e49812e7bab98320d3a98e7f7418`;
- complete historical supplement tree: `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`.

The v21 source is retained at

`papers/A2-v22-reference-free-certified-recovery/retained/v21`.

The validator requires that path to resolve to the pinned v21 tree in a real Git checkout before it will qualify the all-volume package. This is stronger than trusting a directory name or a source-content archive.

The v21 report's principal unresolved issues were:

1. a finite set of successful local inverses did not certify that no obstacle orbit was unseen;
2. observed cycle vectors did not certify that they generated the full period group;
3. the noisy theorem used a known reference witness/table neighborhood;
4. candidate cell area was at risk of being calibrated from visible bodies before coverage was established;
5. the scanner and statistical theorem still relied on strong physical access and compact-class assumptions.

Version 22 responds directly to the first four. The fifth remains relevant to the top-four assessment.

## 3. Current source layout inspected

### 3.1 Primary mathematical source

The active primary entry is `main.tex`, which includes:

- `core/01_setting.tex` — observation contract and headline theorems;
- `core/02_local.tex` — retained two-density local inverse and stability;
- `core/03_completeness.tex` — exact assembly and completion defect;
- `core/04_reference_free.tex` — reference-free noisy clustering and subgroup recovery;
- `core/05_statistics.tex` — finite histograms and hidden-area testing;
- `core/06_acquisition_comparison.tex` — exact/noisy/acquisition distinctions;
- `references.tex`.

The current core tree is

`bb15108f89805bb5e994738e50e3bbb47ae9c2f0`.

The current tools tree is

`d0ca14238af0a4887b77a998137bcf040bfc8765`.

The primary is designed as a 17-page theorem-led article. Earlier A2 material remains in the preserved v21 and nested supplement trees rather than being silently treated as re-proved by the new core.

### 3.2 Provenance and response files

The rereview read:

- `RESPONSE_TO_REFEREES.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `PROOF_LEDGER.md`;
- `SUPPLEMENT_MAP.md`;
- `SOURCE_PINS.json`;
- `PUBLICATION_BINDING.json`;
- `README.md`.

These files distinguish the mathematical checkpoint, publication/delivery commit, local execution, exact-source workflow, retained volumes, and formal-proof limitations.

### 3.3 Validation source

The rereview inspected:

- `tools/validate_v22.py`;
- `tools/verify_v22.py`;
- `tools/verify_local_basis.py`;
- `tools/certificate.py`;
- `.github/workflows/a2-v22-verify.yml`.

The source manifest in `SOURCE_PINS.json` covers the complete current primary source and all four current validation tools by SHA-256. The checkout-bound validator compares this manifest with the working sources, checks the preserved v21 tree, binds every current file to its committed Git blob, runs normal and optimized diagnostics, builds the primary, and, in all-volume mode, builds the retained v21, v18, auxiliary, and smooth-supplement entry documents.

## 4. Mathematical deltas confirmed

Version 22 contains the following active theorem-level additions relative to the frozen v21 source.

### 4.1 Exact completion certificate

For a connected observed component, recovered complete analytic images identify the visible body types. Tree placement and non-tree edges give physical cycle displacements and their subgroup `Gamma`. The quantity

`covol(Gamma) - A - sum(visible body areas)`

is proved to equal the sum of a period-index defect and the area of invisible types. This supplies a zero-if-and-only-if certificate of simultaneous type coverage and period saturation.

### 4.2 Omission-safe exact stopping

All records, repetitions, loops, and reverse returns may be retained. Exact enumeration of finite subsets stops only when a connected rank-two component has zero defect. Arbitrary omissions cannot make an incomplete exact component pass.

### 4.3 Reference-free noisy assembly

Recovered complete shapes are clustered using a uniform shape-separation gap, rather than neighborhoods of a supplied reference table. A tree and cycle vectors are selected from the observed multigraph. No reference witness or edge-key catalogue is an input.

### 4.4 Discrete subgroup recovery before calibration

Bounds on the number and diameter of body types, recorded gaps, and cell covolume yield bounded physical cycle vectors and a finite denominator bound. Exact rational coordinates and an integer column group are recovered before the area equation is used. Hermite reduction gives the observed subgroup and its covolume.

### 4.5 Robust defect decision

A positive lower bound for cell covolume and every obstacle area creates a uniform defect gap. The estimated subgroup covolume, recovered free area, and recovered visible-body areas therefore support a fixed fail-closed threshold.

### 4.6 Finite histograms and hidden-area scale

The paper combines multinomial endpoint histograms, local quadratic cell-average reconstruction, conditional analytic continuation, shape matching, subgroup recovery, and the defect test. A separate fixed-window physical subexperiment proves the `N^{-1/2}` hidden-area decision scale.

These additions are present in the active primary source and are not merely plans in the response document.

## 5. Independent diagnostic scope

The review's `verify_review.py` imports no author verification module and uses only Python's standard library. It checks finite displayed arithmetic for:

| Diagnostic group | Checks |
|---|---:|
| completion identity | 4,550 |
| completion nonnegativity | 4,550 |
| completion zero criterion | 4,550 |
| rational cycle coordinates | 4,900 |
| denominator bounds | 5,600 |
| determinantal subgroup indices | 1,400 |
| unimodular invariance | 2,100 |
| rational separation | 2,626 |
| hidden-area signal | 64 |
| hidden-area inversion | 64 |
| Bernoulli-KL envelope | 64 |
| KL nonnegativity | 64 |
| histogram balance | 6 |
| linear-term comparison | 6 |
| **Total** | **30,544** |

Normal and optimized Python executions produced identical JSON output.

The script does not check the analytic continuation proof, physical branch realization, compactness, scanner production of records, source preservation, TeX, statistical measurability, or editorial significance.

## 6. Author local evidence

The committed local receipt records:

- execution kind: `source_content_not_git_checkout`;
- scope: `primary_only`;
- 5,110 new finite checks;
- 3,635 explicitly selected retained local checks;
- 90 nonlinear stationary-curvature comparisons within the retained subset;
- identical normal and optimized output;
- a warning-free 17-page primary build;
- no Git source commit, source tree, GitHub SHA, or GitHub run ID;
- `formal_proof_certificate: false`.

The primary PDF SHA-256 in the binding is

`b81b2a39f577647f36201a9f5a0db89c990f3a86b9a5a16fefaab2df4cb18659`.

The local receipt is useful source-content evidence. It is not an authenticated exact-commit checkout and does not qualify the retained all-volume package.

## 7. Hosted workflow status

The current branch contains `.github/workflows/a2-v22-verify.yml`. The workflow:

1. checks out `${{ github.sha }}` with credentials disabled;
2. installs the stated TeX/Python environment;
3. runs `tools/validate_v22.py --all-volumes --require-checkout`;
4. uploads current and local receipts, build products, and source pins even on failure.

The workflow run associated with the reviewed SHA is:

- run ID: `36541269616`;
- workflow: `A2 v22 exact-source full-package verification`;
- triggering SHA: `ef51836da1744fc4a7133e3a3fd0e85848c73dc6`;
- status at final review check: `queued`;
- conclusion at final review check: `null`.

Accordingly, this review does not report a hosted exact-head all-volume pass. The branch contains the mechanism for such a pass, not a completed result at review time.

## 8. Limits of this audit

This was a targeted external top-four rereview. It concentrated on:

- whether v22 really answers the v21 omission and reference-witness objections;
- correctness of the completion identity and fail-closed logic;
- correctness of the bounded-denominator subgroup reconstruction;
- the distinction between certification and acquisition;
- the information category and uniform priors;
- the finite histogram and hidden-area claims;
- source and workflow binding.

The review did not independently re-prove every theorem in the retained v21/v18/smooth-supplement chain. It did not complete an independent TeX build, run an exhaustive novelty search, or certify that every physical scanner assumption is realizable uniformly. The finite diagnostic script is not a formal proof certificate.

## 9. Audit conclusion

The reviewed source is unambiguously frozen. Version 22 is a real mathematical revision, not a branch alias or metadata-only delivery. It preserves the reviewed v21 source and adds active proofs of an exact omission-safe completion certificate and reference-free noisy subgroup/defect recovery.

No fatal counterexample was found in the new v22 core. The remaining negative recommendation in `REFEREE_REPORT.md` concerns the richness of the observation, the absence of a general acquisition theorem, the strong compact-class priors, unresolved natural data problems, multi-volume architecture, and the requested top-four conceptual threshold. It is not a claim that the paper failed to address the concrete v21 objections.