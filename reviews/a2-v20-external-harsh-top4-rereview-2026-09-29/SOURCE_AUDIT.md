# Source audit for the external A2 v20 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
Paper directory: `papers/A2-v20-canonical-channel-rigidity`

The reviewed object is identified by Git object rather than by branch-name chronology:

- revision branch: `revision/a2-v20-canonical-channel-rigidity-2026-09-29`;
- equivalent alias: `revision/a2-v20-referee-copy-2026-09-29`;
- commit: `c376e802e6e86735888dcd685f987c7a8f475903`;
- repository tree: `7e948d1bb13ab02cfde808bf8d2a395f383c012d`;
- parent: `d2744e3cd159cdbf926359fea1f9322e847280ad`;
- author commit date: 28 September 2026;
- manuscript date: 29 September 2026.

Both v20 aliases resolved to the same commit when this review began. No later A2 revision branch was present.

The review branch

`review/a2-v20-external-harsh-top4-rereview-2026-09-29`

was created directly from the reviewed author commit. This review adds files only under

`reviews/a2-v20-external-harsh-top4-rereview-2026-09-29/`.

No manuscript source, author revision ref, prior review, or unrelated paper is modified.

## 2. Prior report and response chain

The parent of v20 is the frozen v19 external-review commit

`d2744e3cd159cdbf926359fea1f9322e847280ad`.

The controlling report is preserved at

`reviews/a2-v19-external-harsh-top4-rereview-2026-09-28/REFEREE_REPORT.md`

with blob

`fab60c145fc19e45d1c25b67acb2c3837f8232f6`.

That report reviewed author commit

`2f51ac5a2ab72deceb21c23084ca3062056edb4c`.

The v20 source pins record the same report commit, report blob, reviewed author commit, and reviewed v19 archive tree. The v20 `RESPONSE_TO_REFEREES.md` addresses the v19 report point by point.

## 3. Active source map

The primary driver is `main.tex`. Its active mathematical inputs are:

1. `core/01_setting.tex`;
2. `core/02_local.tex`;
3. `core/03_descent.tex`;
4. `core/04_stability.tex`;
5. `core/06_canonical.tex`;
6. `core/05_comparison.tex`.

The principal new chapter is `core/06_canonical.tex`. It contains:

- obstruction descent for obstructed shortest bridges;
- bounded-range lifted-graph connectivity;
- generation of the full period lattice by all quotient cycles;
- the all-cycle determinantal index;
- the physical `2/3/5` nonprimitive-pair example;
- complete-catalogue whole-table rigidity;
- stable all-cycle locking and the finite-histogram extension.

`core/01_setting.tex` has been revised to state the new information contract and the new catalogue theorems.

The following four v19 mathematical inputs remain active with their original Git blob identities:

| File | Retained blob |
|---|---|
| `core/02_local.tex` | `f389f30844487e78137752faf4f79bbbbd6797ed` |
| `core/03_descent.tex` | `e8306a346b12211755e7bb04388d1c6c48957116` |
| `core/04_stability.tex` | `94cd77010d2c797114319b9b7421cb2e528acbff` |
| `core/05_comparison.tex` | `447e8bec209bb431b3cc674e8f093bf1b52a682f` |

The source checker verifies those blob identities rather than trusting copied filenames.

## 4. Retained volumes

The v20 package preserves three earlier source objects:

- complete reviewed v19 archive: `history/v19-reviewed`, tree `57d8eff44d32a07445db7e0a041eea5d6125bdd0`;
- Supplement R, the complete v18 article: `retained/v18`, tree `3c558d7799e9e49812e7bab98320d3a98e7f7418`;
- Supplement S, the complete smooth-theory volume: `complete`, tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`.

The primary article describes these as supplementary mathematical claims included in the submission package, not as independently published or accepted articles.

## 5. Source pins and publication binding

`SOURCE_PINS.json` enumerates every active primary mathematical input and verification tool by SHA-256. It also binds:

- the four retained active blobs;
- the v19 report and reviewed author source;
- the complete v19 archive tree;
- the Supplement R tree;
- the Supplement S tree.

`PUBLICATION_BINDING.json` records the primary source blobs, primary PDF hash, final TeX log hash, source-manifest hash, and local execution-archive hash. It correctly states that the local run was source-content execution rather than an authenticated checkout.

The source manifest includes:

- `main.tex`;
- `references.tex`;
- all six active `core/*.tex` files;
- `tools/validate_v20.py`;
- `tools/verify_v19.py`;
- `tools/verify_v20.py`.

The validator rejects missing or additional active primary/tool files relative to the manifest.

## 6. Local execution evidence

The archived local receipt is

`verification/local/receipt.json`.

It reports:

- execution kind: source content, not Git checkout;
- status: passed;
- scope: primary only;
- inherited v19 checks: 43,897;
- new v20 checks: 21,572;
- total finite checks: 65,469;
- normal and optimized output agreement for both suites;
- warning-free primary build;
- primary length: 21 pages;
- primary PDF SHA-256: `6b901ce537abc2e663a7df12eb55d399242d9eeb39b501f4c1d18236a61695d2`.

The receipt does not claim a Git commit identity or a full retained-volume build. This limitation is stated rather than hidden.

## 7. Exact-source hosted qualification

The workflow is

`.github/workflows/a2-v20-verify.yml`.

It is read-only and triggers only on the v20 author branch and relevant v20 paths. It checks out `${{ github.sha }}` with credentials persistence disabled, installs the build environment, and runs

`python3 tools/validate_v20.py --all-volumes --require-checkout`.

The validator, in exact-checkout/all-volume mode, verifies:

1. a clean tracked checkout;
2. equality of the triggering SHA and actual checkout SHA;
3. every primary/tool SHA-256 pin;
4. every retained active Git blob;
5. the complete v19 archive tree;
6. the Supplement R tree;
7. the Supplement S tree;
8. normal/optimized agreement for v19 and v20 diagnostics;
9. the v20 primary build;
10. retained v18 diagnostic suites;
11. the Supplement R build;
12. the Supplement S main and auxiliary builds;
13. that qualification changes no tracked or mathematical source.

The exact workflow run was:

- run ID: `36452685537`;
- head SHA: `c376e802e6e86735888dcd685f987c7a8f475903`;
- status: `completed`;
- conclusion: `success`;
- job ID: `109031105402`;
- runner: `ubuntu-24.04`;
- all validation and artifact steps: successful.

The archived workflow artifact was:

- artifact ID: `10986523940`;
- name: `A2-v20-c376e802e6e86735888dcd685f987c7a8f475903`;
- size: 3,811,117 bytes;
- digest: `sha256:d29520ae547761381723bc9ad57697ba9de357428cf64d1ae9061a8acac95d0e`;
- expiration date: 28 October 2026.

This closes the hosted full-package delivery issue recorded in the v19 report. It remains execution and source-identity evidence, not a mathematical proof certificate.

## 8. Files inspected for the rereview

The rereview read the following current files in detail:

- `main.tex`;
- `core/01_setting.tex`;
- `core/02_local.tex`;
- `core/03_descent.tex`;
- `core/04_stability.tex`;
- `core/05_comparison.tex`;
- `core/06_canonical.tex`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `SOURCE_PINS.json`;
- `PUBLICATION_BINDING.json`;
- `SUPPLEMENT_MAP.md`;
- `references.tex`;
- `tools/validate_v20.py`;
- `tools/verify_v20.py`;
- `verification/local/receipt.json`;
- `.github/workflows/a2-v20-verify.yml`.

The review also read the complete v19 referee report and the retained v19 mathematical sections on local inversion, finite-index descent, stability, and literature comparison.

## 9. Scope of the audit

The audit concentrated on:

1. whether v20 really closes the v19 coverage and primitive-pair objections;
2. whether obstruction descent terminates and preserves lifted endpoints;
3. whether the covering-radius argument proves lifted connectivity;
4. whether quotient paths generate the full deck lattice;
5. whether the all-cycle gcd formula has the claimed normalization;
6. whether the `2/3/5` example is a genuine strict extension;
7. whether stable saturation avoids forming integer groups from raw noisy vectors;
8. whether the exact-source workflow genuinely passed at the reviewed commit;
9. whether the new theorem reaches the requested editorial benchmark.

This was not a formal verification of every retained theorem in Supplements R and S. No exhaustive novelty or priority search was performed. Independent finite diagnostics cannot certify the infinite geometric theorem, analytic continuation, physical acquisition, or journal-level significance.

## 10. Audit conclusion

The reviewed source is unambiguous, pinned, and isolated. Version 20 is a real mathematical revision. The exact-source full-package workflow has passed on the reviewed commit. The v19 coverage, primitive-pair, lattice-attribution, and hosted-build objections are substantively addressed.

The negative recommendation in `REFEREE_REPORT.md` is therefore not based on stale source, failed qualification, or a known fatal formula. It rests on the information contract, strong global genericity and acquisition priors, missing closest proximity/visibility-graph comparison, and the exceptional significance threshold requested by the author.