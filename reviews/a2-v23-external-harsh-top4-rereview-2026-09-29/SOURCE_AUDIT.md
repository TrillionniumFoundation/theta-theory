# Source audit for the external A2 v23 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Reference-free certification from intrinsic boundary laws*  
Paper directory: `papers/A2-v23-sequential-record-discovery`

The reviewed object is identified by Git objects rather than by branch-name chronology:

- revision branch: `revision/a2-v23-sequential-record-discovery-2026-09-29`;
- equivalent source alias: `revision/a2-v23-referee-copy-2026-09-29`;
- reviewed commit: `b3453e025f01f0e1089878f8dd4bf57fc15f3aab`;
- reviewed tree: `73fc4caff9d1a9c6d77e434181299b66c7b2efef`;
- mathematical checkpoint: `76436dbdb071c0fe6f013568b1e507f22d7054ff`;
- commit date: 29 September 2026.

Both v23 revision aliases resolved to the reviewed commit. No later A2 revision branch was found when this review branch was created.

The review branch

`review/a2-v23-external-harsh-top4-rereview-2026-09-29`

was created directly from the reviewed commit. It adds files only below

`reviews/a2-v23-external-harsh-top4-rereview-2026-09-29/`.

No author source, revision branch, previous review, or unrelated paper is modified.

## 2. Revision chronology

The mathematical checkpoint has parent

`ecfe49c9ab244ade504c9a727a4d110f72db4433`,

the final commit of the external v22 review branch. That report reviewed author commit

`ef51836da1744fc4a7133e3a3fd0e85848c73dc6`.

The v23 revision therefore starts from the latest frozen report. Its source pins identify:

- preserved reviewed v22 tree: `65c432ddf3233b4931a15e1ee86cbc051503e682`;
- preserved complete smooth-law tree: `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`;
- controlling v22 review commit: `ecfe49c9ab244ade504c9a727a4d110f72db4433`;
- controlling report blob: `c6a72684714f01f99f0600fff1413a85c87c39a9`.

The author head consists of the mathematical checkpoint followed by one publication/evidence commit. The latter adds response and ledger files, source pins, validation tools, local execution evidence, and the exact-SHA workflow. It does not alter the mathematical core from the checkpoint.

## 3. Active source inspected

The rereview inspected the complete v23 primary, with detailed attention to:

- `main.tex`;
- `core/01_setting.tex`;
- `core/02_local.tex`;
- `core/03_completeness.tex`;
- `core/04_reference_free.tex`;
- `core/05_normalization.tex`;
- `core/06_catalogue.tex`;
- `core/07_sequential.tex`;
- `core/08_comparison.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `README.md`;
- `SOURCE_PINS.json`;
- `PUBLICATION_BINDING.json`;
- `SUPPLEMENT_MAP.md`;
- `tools/validate_v23.py`;
- `tools/verify_v23.py`;
- `tools/retained_verify_v19.py`;
- `verification/local/receipt.json`;
- `.github/workflows/a2-v23-verify.yml`.

The latest v22 report and its exact source chronology were also read.

The following v22 mathematical files are retained with unchanged Git blobs:

- `core/02_local.tex`: `f389f30844487e78137752faf4f79bbbbd6797ed`;
- `core/03_completeness.tex`: `604a40b3ed7aaae544c8fe58d4f66cdaee9eaeea`;
- `core/04_reference_free.tex`: `60b4234d4f68caae7259b4bd5fac53c9b9ec34a2`.

The principal v23 additions are the revised setting and the new normalization, catalogue, sequential, and comparison chapters.

## 4. Mathematical deltas confirmed

### 4.1 Unknown-cell phase preparation

The revision no longer assumes exact access to an unknown fundamental cell. It samples laboratory positions in a growing square, rejects solid positions, samples a uniform direction after a free launch, and uses a periodic record gate. The boundary-tile argument gives total-variation error of order `L^{-1}`. Rejected launch attempts and all gate failures are counted.

### 4.2 Preparation bias in the finite experiment

The total-variation preparation error is converted into finite cell-mass error before the quadratic histogram reconstruction. The resulting density error contains the additional term `tau_L h^{-4}`. The prescribed growth of the laboratory square balances that term with the ordinary `C^{2,beta}` bias.

### 4.3 Sequential catalogue growth

The principal theorem now permits one adaptive genuine-record proposal per epoch, retains an unboundedly growing list, and revalidates it with fresh preparations. It does not begin with a supplied fixed complete list.

### 4.4 Explicit discovery assumptions

The paper formalizes conditional record hazards and proves the standard exponential absence bound. It extracts a saturated witness of size at most

`r_0 + 1 + floor(log_2 Q)`

without assuming a primitive cycle pair.

### 4.5 Concrete geometric producer

The retained finite-aperture scanner is converted into a randomized producer with an explicit ordered-pair proposal probability. Its access is stated explicitly: complete-body listing and representation, shortest-pair and blocker tests, local-margin certification, and periodic-gate installation. It is not claimed to arise from unmarked trajectories.

### 4.6 Anytime stopping

The revision uses fresh conditional validation and a summable error budget over epochs. It proves simultaneous correctness of all certificates and the actual stopping time. Under divergent witness hazards it stops almost surely; under a uniform positive hazard it gives an explicit stopping tail and finite expected launch cost.

These additions are active inputs of `main.tex`; they are not detached notes.

## 5. Author local evidence

The committed local receipt records a successful **source-content**, **primary-only** run. It is not an authenticated Git checkout. It reports:

- 7,230 new finite diagnostics;
- 3,635 selected retained checks;
- identical normal and optimized Python output;
- 90 nonlinear stationary-ray curvature comparisons;
- maximum absolute curvature error `1.2312545871751013e-08`;
- a 23-page primary PDF;
- no final TeX warnings, unresolved references, overfull boxes, or underfull boxes in the primary log;
- no execution of the physical scanner;
- no formal proof certificate.

The local receipt binds the source-content manifest, PDF hash, and log hash, but its `source_commit`, `source_tree`, `github_sha`, and `github_run_id` fields are null by design.

## 6. Hosted exact-source execution

The repository contains a read-only exact-triggering-SHA workflow:

`.github/workflows/a2-v23-verify.yml`.

It checks out the triggering commit and runs

`python3 tools/validate_v23.py --all-volumes --require-checkout`.

GitHub Actions run `36548594191` was bound to the reviewed SHA and completed with conclusion `failure`. The checkout and dependency-installation steps succeeded. The validation/build step failed; the evidence upload succeeded.

The uploaded artifact was inspected. Its `verification/current/receipt.json` records:

- execution kind: `git_checkout`;
- scope: `all_declared_volumes`;
- source commit and GitHub SHA equal to the reviewed commit;
- source tree equal to the reviewed tree;
- both retained tree pins verified;
- v23 normal/optimized diagnostics identical;
- primary v23 build passed with 23 pages and no final diagnostics;
- retained v22 primary passed with 17 pages and no final diagnostics;
- retained v21 primary passed with 29 pages and no final diagnostics;
- retained v18 primary built successfully as a 36-page PDF but its log contained one final diagnostic:

`Overfull \vbox (1.88753pt too high) has occurred while \output is active`.

The validator therefore recorded

`retained/v22/retained/v21/retained/v18/main.tex: final TeX diagnostics remain`

and exited with failure before inspecting the two final retained Supplement S entry documents. All TeX compilation commands reached up to that point exited zero.

This is a reproducibility and delivery failure under the repository's strict warning-free policy. It is not a proof counterexample. It also means that neither the manuscript nor this review may describe v23 as having a successful hosted exact-SHA full-package qualification.

## 7. Independent review diagnostics

The review's `verify_review.py` imports no author verification code. Normal and optimized Python executions produced identical output. It performs 112,766 finite checks in exact rational arithmetic or deterministic finite floating-point comparisons.

The groups cover:

- square boundary strips and mixture constants;
- free-launch acceptance and Chernoff budgets;
- total-variation contraction under gates;
- histogram and preparation-bias balancing;
- adaptive and uniform hazard products;
- coupon and stopping-tail union bounds;
- subgroup-index halving and witness length;
- producer pair probabilities;
- completion-defect identities and zero characterization;
- epoch preparation and launch budgets;
- expected-cost tail integrability.

The independent script does not run the geometric scanner, install a periodic gate, perform analytic continuation, build the manuscripts, certify the full proof, or decide publication priority.

## 8. Limits of this audit

This was a targeted top-four rereview, not a formal verification of the multi-volume programme. It concentrated on:

1. whether v23 actually answers the v22 acquisition and normalization objections;
2. whether the finite-square and histogram inequalities are correct;
3. whether the witness, hazard, producer, and anytime arguments are logically coherent;
4. whether the theorem's operational access is stated honestly;
5. whether the source and execution evidence supports the claims made for it;
6. whether the resulting package reaches the requested editorial benchmark.

The audit did not re-prove every retained theorem. No exhaustive novelty or priority search was performed. The exact failure artifact was used only to identify the recorded qualification failure. Finite diagnostics are not a mathematical proof certificate.

## 9. Audit conclusion

The reviewed object is unambiguous and reproducibly pinned. Version 23 is a real mathematical revision. It adds an operational large-square preparation, a growing genuine-record model, explicit arrival assumptions, a concrete geometric-oracle producer, and an anytime stopping theorem.

No fatal counterexample was found in the new finite preparation, discovery, or stopping arguments. The exact-source workflow is correctly bound to the author SHA, but its first hosted run failed the strict retained-volume TeX-diagnostic gate. The negative recommendation in `REFEREE_REPORT.md` is primarily a top-four information-category and conceptual-significance judgment, not a claim that the new v23 core merely renames v22 or contains a known fatal algebraic error.