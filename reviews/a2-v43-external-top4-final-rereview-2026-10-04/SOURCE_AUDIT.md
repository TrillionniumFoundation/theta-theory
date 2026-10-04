# Source audit for the external final A2 v43 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Reviewed directory: `papers/A2-v43-journal-package`

The reviewed source is frozen by Git object:

- author branch: `revision/a2-v43-journal-package-2026-10-04`;
- equivalent referee-copy branch: `revision/a2-v43-referee-copy-2026-10-04`;
- reviewed commit: `4557df22f5c72bc80943690ecd6c2e39de3734ab`;
- repository tree: `39b947dbdf40a7019b0c31c1aca8d83372f661cc`.

Both revision branches resolve to the same commit. No later A2 revision branch was present when the review was frozen.

The review branch

`review/a2-v43-external-top4-final-rereview-2026-10-04`

was created directly from the reviewed author commit. Review additions are confined to

`reviews/a2-v43-external-top4-final-rereview-2026-10-04/`.

No manuscript source, author branch, workflow, prior review, retained paper, or unrelated path is modified.

## 2. Controlling chronology

The v43 author commit descends directly from the completed v42 external review:

- controlling review branch: `review/a2-v42-external-top4-rereview-2026-10-04`;
- controlling review commit: `74787c9c353b72983fe1bb43af467e31d3eb0f2a`;
- controlling report blob: `c4a0504e38ab944a0b301d4183eebf53c831d360`;
- reviewed v42 author commit: `fffc85d4da8c8ee6369833369d564b1cffabc63d`;
- reviewed v42 paper tree: `be6f133ceb1924243165076b2aaec4801a80c9c1`.

The v42 report recommended minor revision and acceptance after four author-side corrections plus an independent human specialist verification. Version 43 addresses the author-side items and explicitly records that the human verification is not complete.

## 3. Files and interfaces inspected

The audit read the current:

- `main.tex` and `companion.tex`;
- `core/00j_two_field_introduction.tex`;
- `core/21_two_field_rigidity.tex`;
- `core/22_two_field_finite.tex`;
- `core/23_two_field_law.tex`;
- `core/24_measure_support.tex`;
- `core/25_nonsmooth_curvature.tex`;
- `core/26_finite_geometry_details.tex`;
- `core/27_moment_factor_details.tex`;
- `core/28_theorem_comparison.tex`;
- `core/29_supplement_interface.tex`;
- `core/30_linear_moment_acquisition.tex`;
- `README.md`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `SPECIALIST_REVIEW_BRIEF.md`;
- `SUBMISSION_MAP.md`;
- `SOURCE_AUDIT.md`;
- `SOURCE_PINS.json`;
- `JOURNAL_INTERFACE.json`;
- `tools/qualify_v43.py` and current diagnostics;
- `.github/workflows/a2-v43-verify.yml`.

It also read the complete v42 referee report and inspected the exact-SHA workflow artifact.

## 4. Closure of the author-side minor revisions

### Default acquisition

The abstract, introduction, finite-law theorem, resource summary, response, and proof ledger all make the signed-record term

`N_geom(c a_m,delta/2) + C a_m^(-2) log(Cm/delta)`

the default current bound. The `C m^2 a_m^(-4)` all-node construction is retained and explicitly labelled as the deterministic alternative.

### Current front matter

All unprefixed front matter describes v43. Historical v41/v42 material is placed under provenance paths and excluded from the journal-facing archive.

### Data-model separation

The abstract and introduction distinguish exact whole-plane fields, finite bits, `W_1` law recovery, local spatial `L^1` prediction, `BV`-based uniform prediction, exact periods, and finite period decisions with a positive patch margin.

### Frozen package

`JOURNAL_INTERFACE.json` fixes source hashes, label ownership, cross-document references, the dependency graph, and the paired PDF names. The primary exact theorem has no supplement theorem dependency. The finite interface is explicit and unchanged from the reviewed source.

### Human specialist status

`SPECIALIST_REVIEW_BRIEF.md` says “Status: not performed.” No source or receipt claims otherwise.

## 5. Proof preservation

The v42 active union contained 467 labels, 116 formal result blocks, and 113 proof bodies. The v43 qualification records:

- 469 active labels;
- 116 formal result blocks;
- 113 proof bodies;
- all 467 reviewed labels retained;
- all 113 reviewed proof bodies byte-identical.

The exact theorem files and frozen supplement interface match their reviewed v42 source hashes. The statement-level changes promote the default budget and add editorial navigation without altering the reviewed proof hypotheses.

## 6. Exact-source workflow and artifact

Workflow:

- path: `.github/workflows/a2-v43-verify.yml`;
- run ID: `37210951299`;
- head SHA: `4557df22f5c72bc80943690ecd6c2e39de3734ab`;
- status: `completed`;
- conclusion: `success`.

All stages succeeded: exact checkout, committed-source capture before environment installation, exact source/proof/diagnostic qualification, both PDF builds, stable cross-document auxiliaries, and evidence archive.

Artifact:

- ID: `11306587365`;
- name: `A2-v43-4557df22f5c72bc80943690ecd6c2e39de3734ab-1`;
- digest: `sha256:3170908bc2be6eed37007e5b128d2d2a65def8e8f2eaa107a28d4d834992f22e`.

## 7. Receipt audit

The downloaded artifact records:

- schema: `a2-v43-qualification-1`;
- status: `passed`;
- exact commit qualified: true;
- source captured and unchanged: true;
- journal interface frozen: true;
- cross-document auxiliaries stable: true;
- primary: 47 pages, no final TeX findings, SHA-256 `fdce6a7fa0c37e8c9b0840180071a26ecabfa03a6c558c2d9e98e759b82d6909`;
- companion: 86 pages, no final TeX findings, SHA-256 `02d6cf960d9d13ec5ae4d4cf239c37ab41d114e6ab4b9dce96fb4a43c0d90d8d`;
- journal package: 61 members, paired PDFs, current front matter only, SHA-256 `d7e59b52aadafe74f4a27daf5b31e8dc0db1ad8a7bfbd9c951558238d26a5fba`;
- main document: 14 TeX inputs, 147 labels, 37 proof bodies;
- companion: 35 TeX inputs, 322 labels, 76 proof bodies;
- mathematical inputs have one document owner;
- retained v41 diagnostics: 661,187 checks;
- retained v42 diagnostics: 73,933 checks;
- v43 contract tests: 17 rejected mutations, all passed;
- formal proof certificate: false;
- physical sensor executed: false;
- human specialist review: false.

## 8. Independent review diagnostics

The review's `verify_review.py` imports no author module and uses only the Python standard library. Normal and optimized executions are byte-identical at SHA-256

`1af7568f3e209fba4c16c683cd3e72b7cea6d56b35b8018270966ad946b9da1b`.

It records 140,888 checks. The finite exact models cover the endpoint identity, finite prefix inverse and stability, protected first exit, signed records, shared moment acquisition, factor-moment inversion, conditioning, resource hierarchy, and dependency acyclicity.

These diagnostics do not certify continuum proofs, the TeX build, a physical apparatus, a human specialist review, or a journal decision.

## 9. Audit conclusion

The reviewed object is unambiguous and source-qualified. The four author-side v42 minor revisions are closed, and no regression was found in the preserved mathematical core. The independent human specialist check remains openly unperformed and should be supplied through the editorial process. The final report recommends acceptance without further author-side revision, subject to that editorial verification.
