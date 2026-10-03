# Source audit for the external A2 v26 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Reference-free certification from intrinsic boundary laws*  
Active manuscript directory: `papers/A2-v26-adaptive-recognition`

The reviewed source is identified by Git objects:

- revision branch: `revision/a2-v26-collision-certification-2026-10-03`;
- equivalent alias: `revision/a2-v26-referee-copy-2026-10-03`;
- reviewed head: `8c6f1113296c5401258ff052e5ce734fabfb3909`;
- reviewed tree: `fafe34398d8373736634b8c045c3063dc4c997cb`;
- mathematical checkpoint: `23a0ac311f6864807a3d538f3658ff07d341c269`;
- commit date: 3 October 2026.

No later A2 revision branch was present when this review branch was created.

The review branch

`review/a2-v26-external-harsh-top4-rereview-2026-10-03`

was created directly from the reviewed head. The review adds files only below

`reviews/a2-v26-external-harsh-top4-rereview-2026-10-03/`.

No author source, workflow, retained tree, previous report, revision branch or unrelated paper is edited.

## 2. Mathematical source freeze

A direct comparison from the mathematical checkpoint to the reviewed head is one commit ahead. The only added files are:

- `DELIVERY_STATUS.md`;
- `MATHEMATICAL_SOURCE_PINS.json`;
- `README.md`;
- `RESPONSE_TO_REFEREES.md`.

No active `.tex` source is changed by that final delivery commit.

`MATHEMATICAL_SOURCE_PINS.json` records:

- mathematical commit `23a0ac311f6864807a3d538f3658ff07d341c269`;
- controlling v25 report commit `aec09874d30f06dcbac1d1b7858fe96364f9d8d7`;
- v25 report blob `d826e120dd684da5504f7975c9b1387ea8d38434`;
- retained v25 tree `c48d900f6596eea1e8df1f729481674fb1bf6175`;
- complete supplement tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`;
- SHA-256 pins for every active core file, `main.tex` and `references.tex`.

The final comparison and pin file therefore give an unambiguous mathematical object even though the final branch contains a later response/provenance commit.

## 3. Current files inspected

The rereview read:

- `main.tex`;
- `core/01_setting.tex`;
- `core/02_collision_clouds.tex`;
- `core/03_recognition.tex`;
- `core/04_smooth_certificate.tex`;
- `core/05_sequential.tex`;
- `core/06_comparison.tex`;
- `core/07_compensated_clouds.tex`;
- `references.tex`;
- `README.md`;
- `RESPONSE_TO_REFEREES.md`;
- `DELIVERY_STATUS.md`;
- `MATHEMATICAL_SOURCE_PINS.json`;
- `.github/workflows/a2-v26-verify.yml`.

The rereview also inspected the controlling v25 referee report, the v26 branch chronology, the exact-head Actions run and job steps, and primary sources used for the literature comparison.

## 4. Principal v26 deltas

### 4.1 Boundary and solid-distance queries are removed

The new experiment records collision positions and times from resettable spatial launches. It no longer takes boundary heights, derivatives, normals, arclength, body labels, periods or distance-to-solid values as deterministic sensor outputs.

### 4.2 Complete bodies are sampled

First-hit point clouds and convex hulls reconstruct complete encountered convex bodies in bounded laboratory regions. The global theorem no longer analytically continues a short contact germ.

### 4.3 The global class is finite smooth

The primary theorem uses a fixed C^{6,β} compact class. A positive-kernel construction also gives a weaker local regularity route. Smooth nonanalytic perturbations are allowed.

### 4.4 Recognition is quantitative

The complete-pair support fingerprint has an explicit mesh size and separation threshold determined by numerical shape, symmetry, distance and geometry margins. There is no unknown analytic-continuation exponent in the descriptor.

### 4.5 Geometry is freshly revalidated

Raw proposals are retained, but every epoch reconstructs their clouds, branch validity, registry, signs and endpoint coordinates anew. No erroneous old statistical label is permanent.

### 4.6 The retained inverse is integrated with cloud geometry

The endpoint-law action inverse, rational period recovery and completion defect are retained, but complete bodies and incidence are supplied by collision clouds rather than analytic continuation.

### 4.7 Compensated smoothing improves launch exponents

The mathematical checkpoint adds a signed fourth-order kernel under the already stated six-derivative bound. It improves the per-cloud geometric exponent from 3/2 to 3/4 and the cumulative launch exponent from 11/2 to 19/4 while retaining the certificate and stopping tail.

## 5. Hosted evidence audit

The reviewed head triggered GitHub Actions run `37118534591`, workflow `A2 v26 exact-source review package`.

The run completed successfully in the GitHub status sense. Its successful operations were:

1. exact triggering-SHA checkout;
2. native Git source archive and checkout identity;
3. collection of available evidence;
4. artifact upload.

The following operations were skipped:

1. build-tool installation;
2. `validate_v26.py --all-volumes --require-checkout`.

The skip occurred because `papers/A2-v26-adaptive-recognition/tools/validate_v26.py` is absent. The workflow explicitly falls back to a bootstrap status with:

- scope `source_archive_only`;
- `full_package_qualified: false`.

The author delivery note agrees with this reading. It says the attempted validation-script write was blocked, the scripts are not installed on the remote branch, the local execution was not a Git checkout, and full-package validation remains pending.

The local evidence claimed by the author is:

- 7,453 finite assertions;
- ordinary/optimized agreement;
- 18-page primary;
- no final TeX diagnostics;
- source-content execution only;
- no retained-volume rebuild.

This rereview records those claims but does not promote them to exact-head full-package qualification.

## 6. Independent diagnostics

The review's `verify_review.py` imports no author module. It uses exact integer/rational arithmetic except for finite exponential and power-sum comparisons. Ordinary and optimized Python output agree.

It checks finite portions of:

- the normal-distance Hessian;
- first-hit coupon and square-preparation bounds;
- convex-hull support and capped-distance stability;
- positive and compensated smoothing rates;
- fingerprint constants and registry thresholds;
- translation invariance;
- rational subgroup recovery and Hermite indices;
- the completion defect;
- density bandwidth balances;
- sequential hazard and resource exponents.

Total checks: **199,456**.

The script does not certify compactness, uniform physical margins, actual collision acquisition, the complete proofs, literature priority, a TeX build or a journal decision.

## 7. Limits of this audit

This is a targeted top-four rereview of the v26 delta and the retained principal inverse chain. It is not a formal re-proof of every result in the multi-volume archive.

No physical sensor was executed. No end-to-end numerical implementation was run. No exhaustive literature or priority search was performed. The independent checks support only finite algebra, finite inequalities and the presentation observation recorded in the report.

## 8. Source-audit conclusion

The latest A2 object is unambiguous. The mathematical source is frozen at the pinned checkpoint and the final author head adds only response/provenance files. Version 26 is a genuine mathematical revision.

The remote workflow authenticates and archives the exact final source, but it does not qualify the manuscript or retained volumes because the validation driver is absent and the qualification steps were skipped. That limitation is accurately disclosed by the author and is not the principal basis for the top-four rejection.
