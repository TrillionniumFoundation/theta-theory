# Source audit for the external A2 v42 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Reviewed directory: `papers/A2-v42-proof-completion`

The reviewed source is frozen by Git object:

- author branch: `revision/a2-v42-proof-completion-2026-10-04`;
- equivalent referee-copy branch: `revision/a2-v42-referee-copy-2026-10-04`;
- reviewed commit: `fffc85d4da8c8ee6369833369d564b1cffabc63d`;
- repository tree: `600400c320eefa60a237ce4a21a928f02aa3fdee`;
- active core tree: `072e7e15ba32468ba71a25ce9aaaebe47c61c890`.

Both revision branches resolve to the same commit. No A2 v43 revision branch existed when the review was frozen.

The review branch

`review/a2-v42-external-top4-rereview-2026-10-04`

was created directly from the reviewed author commit. Review additions are confined to

`reviews/a2-v42-external-top4-rereview-2026-10-04/`.

No manuscript source, author revision branch, workflow, prior review, retained paper, or unrelated path is modified.

## 2. Controlling chronology

The immediate author source is A2 v41:

- commit: `d81e4053bfba1703c4086ea8f9c69ed32c3537b6`;
- paper tree: `254376f3ceee96b7f7ce24010fd9c62d7cde7f69`.

The controlling external report is the v40 rereview:

- review commit: `24baf07cf2952668d61881c727cc6417e952c76e`;
- reviewed v40 author commit: `c5593b05546889f436ce858c327670d080aae204`;
- controlling recommendation: major revision with reconsideration at the requested top-four benchmark.

Version 41 addresses the seven concrete requests in that report. Version 42 preserves the v41 package and adds the protected first-exit and shared signed-record moment-acquisition chain.

The validator reports preservation of the complete v40 and v41 active unions. In particular:

- all 402 v40 labels remain active;
- all 92 v40 proof bodies are retained byte-identically;
- all 456 v41 labels remain active;
- all 110 v41 proof bodies are retained byte-identically.

The current active union has 467 mathematical labels, 116 formal result blocks, and 113 proof bodies.

## 3. Active documents and new inputs

The journal package contains two compiled documents:

1. `main.tex`, the primary article;
2. `companion.tex`, the technical companion.

The primary article contains the complete exact two-field proof, finite geometry, finite law and prediction results, the continuum and quantitative appendices added in v41, and the v42 linear acquisition section. The companion retains the earlier localized, stationary, calibration, directional-germ, period-recognition, and benchmark programme.

The principal v41 inputs retained in the primary are:

- `core/24_measure_support.tex`;
- `core/25_nonsmooth_curvature.tex`;
- `core/26_finite_geometry_details.tex`;
- `core/27_moment_factor_details.tex`;
- `core/28_theorem_comparison.tex`;
- `core/29_supplement_interface.tex`.

The new v42 mathematical input is:

- `core/30_linear_moment_acquisition.tex`.

The audit also read:

- `core/21_two_field_rigidity.tex`;
- `core/22_two_field_finite.tex`;
- `core/23_two_field_law.tex`;
- `V42_RESPONSE_TO_REFEREES.md`;
- `V42_AUDIT.md`;
- `README.md`;
- the v41 proof/literature/history ledgers retained for provenance;
- the v42 source manifest and qualification tools;
- the exact-SHA workflow and artifact.

## 4. Mathematical deltas confirmed

### 4.1 Singular-law supports

The support statements use supports of positive measures and apply to arbitrary compact probabilities, including atomic, singular-continuous, point-supported, and segment-supported laws. Positive convolution support, null-set passage through convolution, connected components, local finiteness, and incidence matching are proved explicitly.

### 4.2 Nonsmooth strict convexity

The incoming-arc support identity is proved through convex interval sections. The planar support measure is constructed distributionally; its atom at a normal equals the length of the exposed face. Strict convexity therefore gives a nonatomic obstacle contribution without assuming smoothness. The negative Jordan part of the observable support difference recovers the contact chord.

### 4.3 Quantitative finite geometry

The v41 additions supply explicit collar constants, a tangential two-direction test, strip-ball lower bounds, arbitrary-law grid quadrature, obstacle assignment, complete-component cutoffs, a signed plateau, curvature-atom mass extraction, and finite support smoothing.

### 4.4 Positive finite law recovery

The factor stage uses a genuine rational polygon probability, degree-independent geometric moment errors, a rational nonnegative fitting programme, explicit moment amplification, and a finite positive compression. It separates exact uniqueness from finite stability.

### 4.5 Linear moment acquisition

The v42 section constructs a rational polygon `Q` around a complete expanded component, stops at its first exit, and obtains a linear pointwise prefix identity. One randomized block uses two fresh collision bits and produces a bounded signed record whose conditional expectation is the component occupation. All moments through the chosen degree share the same blocks. Uniform quadrature for arbitrary compact launch laws and simultaneous concentration give the stated `tau^-2` acquisition cost.

## 5. Exact-source qualification

The exact-head workflow is

`.github/workflows/a2-v42-verify.yml`.

Final run:

- run ID: `37207013500`;
- head SHA: `fffc85d4da8c8ee6369833369d564b1cffabc63d`;
- status: `completed`;
- conclusion: `success`.

All stages succeeded:

1. exact source checkout;
2. committed-source capture before environment installation;
3. document-environment installation;
4. exact commit, proof preservation, finite diagnostics, and both PDF builds;
5. source-bound evidence archive.

Artifact:

- ID: `11305366500`;
- name: `A2-v42-fffc85d4da8c8ee6369833369d564b1cffabc63d-1`;
- digest: `sha256:6ca5231818ecd2c3379a7568301da7912e011d2eb4811ae2a6e8fa08b047fc20`.

## 6. Receipt audit

The downloaded artifact contains both PDFs, source archives, source hashes, diagnostic outputs, build logs, auxiliary-cross-reference records, receipt, and artifact binding.

The receipt records:

- schema: `a2-v42-qualification-1`;
- status: `passed`;
- exact commit qualified: true;
- primary pages: 46;
- companion pages: 86;
- current labels: 467;
- current formal result blocks: 116;
- current proof bodies: 113;
- v41 retained diagnostics: 661,187 checks;
- v42 diagnostics: 73,933 checks;
- final TeX findings: none;
- cross-document auxiliaries: stable;
- formal proof certificate: false;
- physical sensor executed: false;
- independent human specialist review: false.

Important hashes:

- primary PDF: `30a46783f6d455935d5bfc60ed733f2f85662b7bf4997f02ef5e97213f487ea0`;
- companion PDF: `5a7e8621ca05279b663d6763b461a4c49040c74b725ddc1fb8f1d242816f4ec9`;
- journal source archive: `bae02c749a2d35ccb3f97614b07e1aec06fa364f22729a6462ed144d87ae5c46`;
- repository source archive: `0f0f348b864f72ab27aa09f27ba9951af53aeed7ab0b5060c2479423924686dd`.

The exact source is reproducibly qualified. This is not formal proof certification.

## 7. Independent diagnostics

The review's `verify_review.py` imports no author module and uses only the Python standard library. Ordinary and optimized executions are byte-identical at SHA-256

`9c2d66867eaabf7bc3f8d860484d7099070307dfe7b58c7ba4ae69f03bf07d4b`.

It records 65,839 successful checks. The principal groups cover:

- 14,985 endpoint identities;
- 14,985 finite-prefix inversions;
- 1,647 protected-prefix identities;
- 1,647 signed-record expectations;
- 29,808 two-support footprint cancellations;
- 672 singular-law quadrature models;
- 260 triangular factor-moment recoveries;
- 75 signed-curvature Fourier models;
- 550 old-versus-new acquisition comparisons and resource cases.

The checks include negative signed-record expectations and finite atomic laws. They do not certify continuum support decompositions, physical apparatus, the complete infinite-configuration proof, or journal priority.

## 8. Limits and conclusion

This was a focused external top-four rereview, not formal verification of every proof in a 132-page two-document programme. The audit concentrated on:

1. the exact two-field prefix/support/Jordan/Fourier chain;
2. the v40 requested continuum repairs;
3. the finite strip, assignment, chord, and moment-factor arguments;
4. the v42 protected signed-record theorem;
5. source preservation and exact-SHA qualification;
6. the significance of the resulting theorem package.

No exhaustive priority search was performed. No physical collision apparatus was executed. The most delicate arguments for independent human review are the singular support-component theorem, nonsmooth Jordan separation, tangential strip and assignment estimates, protected signed-record quadrature, and positive moment conditioning.

No fatal counterexample was found in the audited core. The recommendation in `REFEREE_REPORT.md` is minor revision with acceptance recommended after the listed corrections and a second specialist confirmation.