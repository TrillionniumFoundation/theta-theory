# Source audit for the external A2 v40 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Reviewed directory: `papers/A2-v40-joint-response`

The reviewed source is identified by Git objects:

- author branch: `revision/a2-v40-joint-response-2026-10-04`;
- equivalent referee-copy branch: `revision/a2-v40-referee-copy-2026-10-04`;
- reviewed commit: `c5593b05546889f436ce858c327670d080aae204`;
- repository tree: `1e794c5161114d34a4d46e6e5b5cb50567dfc731`.

Both revision names resolve to the same commit. No later A2 revision branch was present when the review was frozen.

The review branch

`review/a2-v40-external-harsh-top4-rereview-2026-10-04`

was created directly from the author commit. Review additions are confined to

`reviews/a2-v40-external-harsh-top4-rereview-2026-10-04/`.

No author source, revision branch, workflow, prior review, retained paper, or unrelated path is modified.

## 2. Controlling chronology

The v40 author commit is based directly on the completed v39 review:

- controlling review commit: `790654161f2f069fb4d1d1ee18bfe86ea5290d74`;
- reviewed v39 author commit: `f815a7acdb5c03e03b9996fc7052b405db66936d`.

The v40 source manifest pins the complete reviewed v39 paper and review trees and earlier retained A2 trees. The exact-source validator checks preservation against the actual reviewed v39 input closure, not merely an older manuscript snapshot.

The v40 package contains two journal documents:

- `main.tex`, the focused primary article;
- `companion.tex`, the technical companion retaining the complete reviewed v39 programme.

The primary and companion use separate label prefixes for cross-document references and are compiled together until their auxiliary files stabilize.

## 3. Files inspected in detail

The audit read the current:

- `main.tex`;
- `companion.tex`;
- `core/00j_two_field_introduction.tex`;
- `core/21_two_field_rigidity.tex`;
- `core/22_two_field_finite.tex`;
- `core/23_two_field_law.tex`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_DERIVATION_AUDIT.md`;
- `INDEPENDENT_SOURCE_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `README.md`;
- `SOURCE_PINS.json`;
- `SUBMISSION_MAP.md`;
- the shared preamble and bibliography;
- `tools/verify_v40.py`;
- `tools/test_contract_v40.py`;
- `tools/validate_v40.py`;
- `.github/workflows/a2-v40-verify.yml`.

It also read the controlling v39 referee package and the retained v39 exact, finite, period, and statistical results needed to distinguish new from inherited claims.

## 4. Mathematical deltas confirmed

### 4.1 Two fixed-field exact inverse

The new principal data are the two whole-plane forward mean fields for one fixed positive vector and its opposite, both under the same unknown stationary law. A finite endpoint-prefix formula recovers occupation. The supports of occupation and the two collision fields give an exact support cancellation that removes the unknown footprint and leaves an obstacle-minus-chord support function. Signed curvature atoms recover the chord and obstacle. A compact occupation convolution then identifies the complete probability law.

### 4.2 Broadened exact class

The exact theorem requires strict convexity but no boundary smoothness or positive curvature bound. The compact launch probability may be atomic, singular, or supported on a point or segment, provided its support is convex. The only size comparison is `t + diam(A) < d`.

### 4.3 Complete fiber and response completion

The exact ambiguity is a common translation of obstacle configuration and launch law. The two fields determine every other finite-length forward response and the full obstacle translation-period group.

### 4.4 Finite two-command geometry

On a quantitative smooth class, the same fixed commands reconstruct the centered footprint and geometry in `C^2`. The sufficient exponent is

`Q_pair=((gamma+9/2)s)/(s-2)`.

The finite proof includes a two-direction rare boundary test, cap acquisition from positive nominal records, stable extraction of the contact chord, support smoothing, and retained period locking.

### 4.5 Finite probability and prediction

Finite occupation moments and a positive rational moment-fitting programme yield a finitely supported probability estimate in `W_1`. The sufficient cost is exponential in `epsilon^{-1} log(1/epsilon)`. This output predicts all bounded-length responses in local spatial `L^1`. Under a known bounded-variation prior on the zero-extended density, the manuscript additionally obtains density `L^1` recovery and uniform raw-response prediction on bounded windows.

## 5. Exact-source workflow audit

The exact-head workflow is

`.github/workflows/a2-v40-verify.yml`.

The final run is:

- run ID: `37199933345`;
- head SHA: `c5593b05546889f436ce858c327670d080aae204`;
- status: `completed`;
- conclusion: `success`.

All stages succeeded:

1. exact triggering-commit checkout;
2. source capture before build-environment installation;
3. installation of the article and companion build environment;
4. exact-source, finite-diagnostic, and two-document qualification;
5. binding of successful execution evidence;
6. upload of receipt, logs, pinned source, primary, and companion.

Artifact metadata:

- artifact ID: `11302741601`;
- name: `A2-v40-c5593b05546889f436ce858c327670d080aae204-1`;
- digest: `sha256:abfc63698ea4bbcc7c9bc175955c5a68a7ba8364ddf14f89327d84b507d29519`.

## 6. Receipt audit

The downloaded artifact contains both PDFs, both final TeX logs and recorders, build-round logs, mathematical and contract diagnostics, source pins, a journal-source archive, a repository-source archive, the validation receipt, and the run binding.

The receipt records:

- status: `passed`;
- exact commit qualified: true;
- source commit: `c5593b05546889f436ce858c327670d080aae204`;
- primary pages: 23;
- companion pages: 85;
- current labels: 402;
- current formal result blocks: 95;
- current proof bodies: 92;
- reviewed v39 labels retained: 322 of 322;
- reviewed v39 formal blocks retained: 79 of 79;
- reviewed v39 proof bodies retained byte-identically: 76 of 76;
- author finite diagnostics: 656,744;
- ordinary/optimized diagnostic output identical;
- cross-document auxiliaries stable over the final two build rounds;
- final TeX findings: none;
- formal proof certificate: false;
- physical sensor executed: false.

Important hashes include:

- primary PDF: `6bef02a47cbea835d640832c222b728bcb62bd6fabde5be11b0c1fbf69785f3a`;
- companion PDF: `284c9bf0dd9782e721ca2650d3c7b0aa3e9765813d5ee05337819ef027975d76`;
- journal-source archive: `e5d3d1a3102d2f0e9d6942ebb0dcbe6eb6454a4d1944594cd385f5e3b2fe9930`;
- repository-source archive: `b6984de582f60f1a58ae4fa30fcba31b4bf78879cf1d2b7a7642d5a3aabe5edc`;
- author finite-diagnostic output: `95f3b4b6db34e56d99ef4bce83f115551df05fc59de5f69d28dea4ed3950d67b`.

The source package is therefore reproducibly qualified at the reviewed head. This is not a formal proof certificate.

## 7. Independent finite diagnostics

The review's `verify_review.py` imports no author module and uses only the Python standard library. Ordinary and optimized executions are byte-identical at SHA-256

`24f20fd8d36e196a1b0adc7551ffbc27a2d5ea7aa4b8ffcc71f2f4434d374d00`.

It records 108,428 checks. The principal groups cover:

- endpoint-bit and prefix identities;
- finite-prefix perturbation bounds;
- support-arc sums and three-support cancellation;
- negative chord signatures in noncircular support models;
- exact Fourier quotient recovery in compact model families;
- bivariate triangular moment inversion and its factorial stability bound;
- signed finite-command estimators;
- finite geometry, probability, and density-resource exponents.

These diagnostics are finite algebra and explicit models. They do not certify the continuum support decomposition, nonsmooth surface-area measures, infinite configurations, statistical cap acquisition, or physical controls.

## 8. Limits of the audit

This was a focused top-four rereview, not formal verification of both complete documents. The audit concentrated on:

1. source identity and preservation;
2. the endpoint-prefix inverse;
3. collision-support matching and footprint cancellation;
4. negative curvature atoms and canonical geometry;
5. exact compact-law factorization;
6. finite geometry, finite law recovery, and prediction;
7. the significance and journal architecture of the combined package.

The most delicate points for independent human review are the arbitrary-singular-law support statements, nonsmooth strict-convex curvature decomposition, tangential rare-query geometry, cap probability and finite-grid hull acquisition, and perturbation of the moment factor in the positive finite-law reconstruction.

No exhaustive literature or priority search was performed. No physical collision apparatus was executed.

## 9. Audit conclusion

The reviewed object is unambiguous and source-qualified. Version 40 is a real mathematical revision and a major conceptual simplification of the data. No fatal counterexample was found in the audited core. The major-revision recommendation in `REFEREE_REPORT.md` reflects proof-audit, literature-positioning, and journal-architecture requirements, not a source-delivery defect or a claim that the theorem package failed to respond.