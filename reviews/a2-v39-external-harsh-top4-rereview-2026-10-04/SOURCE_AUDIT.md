# Source audit for the external A2 v39 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Reviewed directory: `papers/A2-v39-response-rigidity`

The reviewed source is frozen by Git object:

- author branch: `revision/a2-v39-response-rigidity-2026-10-04`;
- equivalent referee-copy branch: `revision/a2-v39-referee-copy-2026-10-04`;
- reviewed commit: `f815a7acdb5c03e03b9996fc7052b405db66936d`;
- repository tree: `3d26fc322785102d5eda2964bdfd94fdaacf0fc7`;
- active core tree: `113a60e9545374aee5ae6fd80b14f4fedf8e8ed6`.

Both revision branches resolve to the same commit. No later A2 revision branch was present when the review was frozen.

The review branch `review/a2-v39-external-harsh-top4-rereview-2026-10-04` was created directly from the reviewed author commit. Review additions are confined to `reviews/a2-v39-external-harsh-top4-rereview-2026-10-04/`. No manuscript source, author branch, workflow, prior review, retained paper, or unrelated path is modified.

## 2. Controlling chronology

The reviewed v39 commit is based directly on the completed v38 external review:

- controlling review commit: `5dd7a7e346a9d31d7541efe791335d4e965cadb0`;
- controlling review directory tree: `91797dde92b95cbaa36d3ef5f543fee025268855`;
- controlling report blob: `a36a7218e4f07f0f4bb6bf137e04cf608e804936`;
- reviewed v38 author commit: `a346669928e5147cf2c0ef86c3bc2a455b512d14`;
- reviewed v38 paper tree: `36a5f28721e4aa336dba7a2eb0d07132589cd301`.

The v39 manifest also pins retained v34--v37 paper and review trees. The validator reports that all 265 labels active in the reviewed v38 primary remain active and that all 66 reviewed proof bodies remain byte-identical. The v39 primary has 322 labels, 79 formal theorem/lemma/proposition/corollary blocks, and 76 proof environments.

## 3. Files inspected

The audit read the current:

- `main.tex`;
- `core/00_setting.tex`;
- `core/00h_single_law_overview.tex`;
- `core/19_single_law_rigidity.tex`;
- `core/19a_one_resolved_component.tex`;
- `core/20_single_law_finite.tex`;
- `core/16_sharp_stationary.tex` and `core/16a_shrinking_upper.tex`;
- `core/05_comparison.tex`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `README.md`;
- `SOURCE_PINS.json`;
- `SUBMISSION_MAP.md`;
- `references.tex`;
- `tools/verify_v39.py`;
- `tools/test_contract_v39.py`;
- `tools/validate_v39.py`;
- `.github/workflows/a2-v39-verify.yml`.

It also read the controlling v38 referee package and the retained exact-response, finite-stencil, homothetic, isotropic, and known-disk minimax sections needed to distinguish new from inherited claims.

## 4. Mathematical deltas

### 4.1 Single-law directional-germ inverse

The principal theorem uses one unknown stationary density and raw forward means only. Data comprise all centers, all directions, and arbitrarily short positive lengths. The short-flight limit is an entering-boundary integral. Applying `partial_theta^2+1` produces a positive sum of translated copies of the same density at antipodal contacts. Under uniform copy separation, one component recovers the centered footprint, complete centered density, and a boundary contact; all component centers over all directions recover all boundaries.

### 4.2 Fiber, response completion, and periods

The recovered canonical triple determines every finite-length raw response. Equality of germs is equivalent to a common translation of the configuration and launch law. The germ's translation-period group equals the obstacle period group.

### 4.3 One-resolved-obstacle extension

The uniform width condition is replaced by `diam A<d` and the existence of one obstacle with diameter larger than `diam A`. A minimum-area angular support component supplies a pure density copy. The odd germ gives the distributional occupation gradient; bounded continuity and zero infimum fix the additive constant. Support cancellation recovers every obstacle, including those with overlapping antipodal copies.

### 4.4 Finite forward-only geometry

The finite theorem uses stronger quantitative copy separation, obstacle and footprint `C^{6,beta}` bounds, positive curvature, a density boundary-mass lower bound, and protected acquisition apertures. A positive regularized angular response is estimated with finite rational forward commands. The proof controls finite-flight, spatial quadrature, angular quadrature, and command-rounding errors without a density upper bound or continuity modulus.

The sufficient exponent is `Q_gamma=((3 gamma+27/2)s)/(s-2)`. The theorem estimates centered footprint and obstacle geometry in `C^2`; it does not provide finite strong-norm recovery of arbitrary `L^1` density and does not claim minimax optimality.

## 5. Exact-source workflow

The exact-head workflow is `.github/workflows/a2-v39-verify.yml`.

Final run:

- run ID: `37194180565`;
- head SHA: `f815a7acdb5c03e03b9996fc7052b405db66936d`;
- status: `completed`;
- conclusion: `success`.

All stages succeeded: exact checkout, environment installation, source and diagnostics qualification, complete-primary build, evidence binding, and artifact upload.

Artifact:

- ID: `11300382154`;
- name: `A2-v39-f815a7acdb5c03e03b9996fc7052b405db66936d-1`;
- digest: `sha256:6f0d880928ba34e65edcab8b47b27978e62e74650392173da147d970c00dd0b9`.

## 6. Receipt audit

The artifact contains the primary PDF, repository and journal source archives, build logs, source hashes, diagnostics, contract outputs, source pins, receipt, and binding.

The receipt records:

- schema `a2-v39-validation-1`;
- status `passed`;
- exact commit qualified: true;
- primary pages: 85;
- active labels: 322;
- active proof bodies: 76;
- formal result blocks: 79;
- reviewed labels retained: 265 of 265;
- reviewed proof bodies retained byte-identically: 66 of 66;
- author finite mathematical diagnostics: 622,976;
- qualification-contract checks: 66;
- final TeX diagnostics: none;
- formal proof certificate: false;
- physical sensor executed: false.

Important hashes:

- primary PDF: `5f2bbdee93ddeb7a47604c16c5ea015653fcb3f33328a43e79974bfdc777d60b`;
- journal source archive: `629f9bfa0e1ca2087da341578cff690c14f72f8732208bcb772283f1acb6e5ed`;
- repository source archive: `f668f7baa2dc652f0427868377a65e8e16ed402290dbd5f34d16a398ec9d3ece`;
- mathematical diagnostic output: `44990bf0956c28f8a0721c49d09c5d1911dc99ca2c61484e7d6643b3e67b78fb`.

The exact source is reproducibly qualified. This is not formal proof certification.

## 7. Independent diagnostics

The review's `verify_review.py` imports no author module and uses only the Python standard library. Ordinary and optimized executions are byte-identical at SHA-256 `3b2d108539790bc88541e207655fc6d93d362c870e0f0dc62cef29f8a3ab8de5`.

It records 162,863 checks covering:

- the one-sided cosine angular identity;
- compact polynomial-kernel normalization and integration by parts;
- separated translated density copies, support, mass, centered recovery, and common translation;
- strict area increase for unions of distinct translates;
- odd-forward-flux/occupation-gradient signs in exact rectangle models;
- the weak-flight `t/2` coefficient;
- signed importance-sampling expectation, range, and variance;
- displayed finite bias, Bernstein, target-count, command-length, coordinate-mesh, and `nu` exponents.

These are finite identities and models. They do not certify continuum measure supports, infinite configurations, minimum-area selection in full generality, finite quadrature, physical controls, or editorial priority.

## 8. Limits and conclusion

This was a focused top-four rereview, not formal verification of an 85-page programme with 76 proof environments. The most delicate points for independent human review are the continuum support decomposition across directions, minimum-area pure-copy selection, occupation-potential reconstruction, and uniform finite quadrature/support recovery.

No exhaustive priority search was performed. No fatal counterexample was found in the audited core. The negative recommendation in `REFEREE_REPORT.md` is a top-four significance and information-model judgment, not a claim that v39 failed to respond or failed to build.