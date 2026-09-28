# Source audit for the external A2 v19 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
Primary directory: `papers/A2-v19-intrinsic-network-descent`

The reviewed mathematical source is pinned by Git object rather than by branch naming:

- revision branch: `revision/a2-v19-intrinsic-network-descent-2026-09-28`;
- equivalent source alias: `revision/a2-v19-referee-copy-2026-09-28`;
- commit: `2f51ac5a2ab72deceb21c23084ca3062056edb4c`;
- repository tree: `bb540dea1085da7ff4e7fcfcbca36be282b77a1f`;
- commit date: 28 September 2026;
- commit title: `A2 v19: recover unlabelled incidence and covolume-calibrated period lattices`.

Both v19 revision aliases resolved to the same commit. A fresh branch search immediately before review publication found no later `revision/a2-v20...` branch.

The review branch

`review/a2-v19-external-harsh-top4-rereview-2026-09-28`

was created directly from the reviewed v19 commit. The review adds files only under

`reviews/a2-v19-external-harsh-top4-rereview-2026-09-28/`.

No manuscript source, author revision branch, earlier review directory, or unrelated paper was changed.

## 2. Controlling previous report and chronology

The v19 commit has parent

`e727a7ac9b73b6928ecc194d74628125159d49cf`.

That object is the final commit of

`review/a2-v18-external-harsh-top4-rereview-2026-09-28`.

The frozen v18 report blob is

`2eed40e9151ee67ea1e92e1b4e2869df326e4f30`.

The reviewed v18 author checkpoint was

`0708f67908355e9881d1993b42bcc698b0c350c6`.

Thus the source chain used in this rereview is:

1. v18 author checkpoint `0708f679...`;
2. v18 external review branch head `e727a7ac...`;
3. v19 author revision `2f51ac5a...`;
4. the new v19 review branch created from that exact author revision.

Version 19 is one commit ahead of the controlling v18 report and is a real mathematical response, not a branch alias of the previous manuscript.

## 3. Active primary source

The v19 primary is a fifteen-page self-contained article built from:

- `main.tex`;
- `core/01_setting.tex`;
- `core/02_local.tex`;
- `core/03_descent.tex`;
- `core/04_stability.tex`;
- `core/05_comparison.tex`;
- `references.tex`.

The principal new mathematical content is:

1. exact local equivalence between two active endpoint densities and `(W,A)`;
2. shape-separated incidence recovery from an unlabelled multiset of records;
3. covolume recovery from free area and one obstacle area per recovered class;
4. finite-index lattice classification by row Hermite normal form;
5. primitive whole-table uniqueness;
6. exact prime-index physical ambiguities;
7. finite-histogram recovery with stable incidence and integer locking;
8. theorem-level comparison with boundary-distance, lens, obstacle travelling-time, volume, and marked-length results.

The local two-density inverse and Schur-complement curvature formulas were introduced in v18 and are restated and proved in the focused v19 primary. The new global descent and statistical propagation are not merely metadata.

## 4. Retained volumes and source identities

`SOURCE_PINS.json` records:

- new primary core tree: `8142b7f5deac0b75b0ef7f259d1ede5310a28728`;
- retained v18 paper tree: `3c558d7799e9e49812e7bab98320d3a98e7f7418`;
- retained complete Supplement S tree: `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`;
- controlling review commit: `e727a7ac9b73b6928ecc194d74628125159d49cf`;
- controlling report blob: `2eed40e9151ee67ea1e92e1b4e2869df326e4f30`;
- SHA-256 bindings for the new mathematical and validation files.

The repository listing of `retained/v18` agrees with the retained-tree structure recorded by the revision: its primary `main.tex`, fourteen-file `core` tree, tools, proof extract, references, and complete subtree are present. The root `complete` subtree is separately pinned as Supplement S.

`PUBLICATION_BINDING.json` records the primary main and references blobs, tools tree, local receipt tree, local source-manifest digest, local PDF digest, and both retained native trees. It explicitly states that the local execution was source-content execution rather than an authenticated checkout.

These arrangements are substantially stronger than the incomplete v18 delivery. They preserve old evidence with its original scope rather than rewriting it as a v19 pass.

## 5. Files inspected

The rereview inspected in detail:

- `main.tex`;
- all five `core/*.tex` files;
- `references.tex`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `SOURCE_PINS.json`;
- `PUBLICATION_BINDING.json`;
- `README.md`;
- `SUPPLEMENT_MAP.md`;
- `tools/validate_v19.py`;
- the v19 verification script and local receipt;
- `.github/workflows/a2-v19-verify.yml`;
- the retained v18 source layout;
- the controlling v18 referee report.

The mathematical audit concentrated on the new incidence/covolume/Hermite descent, the physical ambiguity construction, and the finite-data propagation, while checking their dependence on the retained local inverse.

## 6. Local author evidence

The checked-in local receipt reports:

- execution kind: `source_content_not_git_checkout`;
- scope: `primary_only`;
- 43,864 finite diagnostics;
- identical normal and optimized Python outputs;
- 90 nonlinear stationary curvature comparisons;
- maximum recorded curvature error approximately `1.2312545871751013e-08`;
- successful fifteen-page primary build;
- no final TeX diagnostics;
- unchanged mathematical/tool source manifest;
- null Git commit, GitHub run, and triggering-SHA fields.

This is legitimate local source-content evidence. It is not an authenticated commit-bound build and did not rebuild Supplements R or S.

## 7. Hosted workflow state

The revision adds

`.github/workflows/a2-v19-verify.yml`.

The workflow:

- checks out the exact triggering SHA;
- runs `tools/validate_v19.py --all-volumes --require-checkout`;
- verifies the retained native trees;
- reruns new and retained diagnostics;
- builds the primary and retained submission volumes;
- uploads logs, receipts, PDFs, pins, and failures.

The corresponding run at the final review check was:

- run ID: `36439719156`;
- head SHA: `2f51ac5a2ab72deceb21c23084ca3062056edb4c`;
- workflow: `A2 v19 exact-source full-package verification`;
- status: `queued`;
- conclusion: `null`.

Accordingly, this review does not report a successful hosted full-package build. The workflow definition and local primary receipt do not substitute for its eventual execution result.

## 8. Independent finite diagnostics

The review's `verify_review.py` imports no author code and uses exact rational arithmetic. Normal and optimized executions produced identical output with SHA-256

`9d9b05ccffeb937939b33948fabcf885ac9f6e6db3c7ec2780decfb911d73a1e`.

It performs 33,934 checks covering:

| Group | Checks |
|---|---:|
| Local curvature, foot speed, and margins | 3,600 |
| Cubic two-density quotient, flux, and reversal | 2,880 |
| HNF, quotient index, annihilation, dual membership, divisor counts | 21,131 |
| Prime-index lattices and corridor residue controls | 3,595 |
| Incidence permutation and edgewise reversal | 256 |
| Cell inversion, rates, calibrated indices, and integer locking | 4,134 |
| **Total** | **33,934** |

The script checks finite identities and bookkeeping only. It does not verify:

- the Liouville/residual-time density formula;
- analytic continuation on the physical class;
- existence and isolation of all selected channels;
- the measurable compact-prior estimator;
- the complete retained mathematical programme;
- literature novelty;
- a TeX build;
- journal-level significance.

## 9. Limits of the audit

This is a targeted external top-four rereview, not a formal verification of every retained theorem. It focused on whether the v18 objections were actually answered and whether the new v19 global theorem is correct in its stated information category.

No exhaustive priority search was performed. The literature audit is theorem-specific. No independent complete primary-plus-supplements build was obtained. The hosted workflow had no conclusion at review time. The review does not certify every proof in Supplements R and S.

## 10. Audit conclusion

The reviewed source is unambiguously pinned. Version 19 is the latest A2 revision found, is a substantive response to the latest v18 report, and preserves the prior paper and smooth-theory volumes by explicit native identities.

The new global descent appears mathematically coherent in its actual analytic, asymmetric, shape-separated, connected, covering, and primitive scope. The review's negative recommendation is a top-four naturality and significance judgment, together with qualifications about genericity, information richness, conditional stability, and unfinished hosted qualification. It is not a finding that v19 is merely v18 under a new branch name or that a fatal algebraic counterexample has been located.
