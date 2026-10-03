# Source audit for the external A2 v28 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Reference-free certification from intrinsic boundary laws*  
Directory: `papers/A2-v28-local-period-recognition`

The reviewed source is identified by Git object:

- revision branch: `revision/a2-v28-local-period-recognition-2026-10-03`;
- equivalent alias: `revision/a2-v28-referee-copy-2026-10-03`;
- author commit: `3ac2df58d175010f338dd6ae8af84158c1590d20`;
- repository tree: `c3afed66d39b03ea05b72fde9be13ee03b3e82b9`;
- parent/base v27 commit: `f230e014911f3b7104db0ec742969789ed5a88c9`.

Both v28 branches resolved to the same author commit at review freeze. No `revision/a2-v29...` branch was found when the review branch was created.

The new branch

`review/a2-v28-external-harsh-top4-rereview-2026-10-03`

was created directly from the author commit. This review adds files only under

`reviews/a2-v28-external-harsh-top4-rereview-2026-10-03/`.

No manuscript source, author workflow, retained volume, previous review or unrelated paper is modified.

## 2. Chronology

The controlling external report is:

- branch: `review/a2-v26-external-harsh-top4-rereview-2026-10-03`;
- report commit: `24b9c5f6a586a35975e6f6b67d25ec431390f57a`;
- report blob: `49d522f04930a0c4d9b3fd3ac3c555a8895596eb`;
- reviewed v26 author commit: `8c6f1113296c5401258ff052e5ce734fabfb3909`.

A2 v27 was an intervening author revision, not a retrieved external review. Its author head is

`f230e014911f3b7104db0ec742969789ed5a88c9`.

Version 28 is one commit ahead of that head. The v28 response correctly distinguishes the already completed v27 fixed-aperture theorem from the genuinely new repeated-motif period-recognition result.

## 3. Preserved source

`SOURCE_PINS.json` records the complete retained v27 paper tree as

`c9e18bc786b795e61a6ed8c0048249bb14713a04`.

The following inherited active core blobs are preserved byte-for-byte:

- `core/00_fixed_aperture.tex` — `a9395a44330d0d09326ce0b9c8730243ae26b143`;
- `core/01_setting.tex` — `7e09436c00b11ee4d4b3c4daaea88038fa3a471e`;
- `core/02_collision_clouds.tex` — `11088fbc956dd1e2de5a62509e39deddfb64cc3f`;
- `core/03_recognition.tex` — `844bbf8307cf7d0848443c4e1c00aba08da990b4`;
- `core/04_smooth_certificate.tex` — `a06bafa41e34144d29d2ffcacd93f4ad6659f11d`;
- `core/05_sequential.tex` — `c19c8aaa48742c57ac4b3a40875a8ea4d97af538`;
- `core/06_comparison.tex` — `6414457e08768bbe60bd73f2aa6dbd8235bb2cc6`;
- `core/07_compensated_clouds.tex` — `3ed79efd099015410cd41ddd0148ca2fcc79bab2`.

The only new active mathematical core is:

- `core/00_local_period_recognition.tex` — blob `45891d4aa0b112434aacba86dcfd825cf8626ac7`.

The primary `main.tex` activates the new section before all eight retained cores.

## 4. Files inspected in detail

Current v28 source:

- `main.tex`;
- `core/00_local_period_recognition.tex`;
- `core/00_fixed_aperture.tex`;
- `core/03_recognition.tex` at the inherited clearance correction;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORICAL_AND_LITERATURE_AUDIT.md`;
- `README.md`;
- `DELIVERY_STATUS.md`;
- `SOURCE_PINS.json`;
- `references.tex`;
- `tools/verify_v28.py`;
- `tools/validate_v28.py`;
- `tools/test_validation_contract.py`;
- `.github/workflows/a2-v28-verify.yml`.

Predecessor and report chain:

- v27 fixed-aperture source at commit `f230e014...`;
- the complete v26 external report at commit `24b9c5...`;
- retained source and qualification metadata pinned by v28.

## 5. Mathematical delta confirmed

Version 28 makes the following genuine changes relative to the v27 author source.

1. It removes individual translation-type separation from the exact fixed-aperture route.
2. It allows repeated congruent bodies and arbitrary body symmetries.
3. It treats the supplied bounded period presentation as possibly nonprimitive.
4. It introduces a two-sided finite central-patch criterion for membership in the intrinsic full translation group.
5. It proves `[Pi:Lambda_0] <= r_0`, recovers the primitive orbit count and computes primitive free area after full-group recovery.
6. It supplies a uniform finite-confidence theorem on patch-mismatch classes.
7. It supplies pointwise eventual recovery when the numerical mismatch margin is unknown.
8. It gives a repeated-disk symmetry-jump example demonstrating the failure of uniform discrete stability without such a margin.

These are active inputs of `main.tex`, not unattached notes.

## 6. Hosted exact-source qualification

The exact-source workflow is

`.github/workflows/a2-v28-verify.yml`.

For the reviewed author SHA:

- run ID: `37128373358`;
- workflow: `A2 v28 exact-source eleven-document qualification`;
- status: `completed`;
- conclusion: `success`;
- head SHA: `3ac2df58d175010f338dd6ae8af84158c1590d20`.

The job record confirms successful completion of:

1. exact triggering-SHA checkout;
2. fail-closed entry-point checks;
3. installation of the mathematical build environment;
4. exact-source qualification of all eleven declared documents;
5. source-bound evidence archival; and
6. artifact upload.

The resulting artifact is:

- artifact ID: `11276051085`;
- name: `A2-v28-3ac2df58d175010f338dd6ae8af84158c1590d20`;
- digest: `sha256:48ea5bfedee38bcbfe85674b008bdfeb2dd0faf4a43fd5f030a75d877d47abf9`.

The author's local snapshot is separately and correctly labelled as non-hosted. It reports eleven documents with page counts

`30, 24, 18, 22, 15, 23, 17, 29, 35, 7, 133`,

113,969 new finite checks, 25 validation-contract checks and no final primary TeX diagnostics.

## 7. Independent diagnostics

The review's `verify_review.py` imports no author code and performs 136,740 finite checks. It covers exact periodic motifs, two-sided patch/global-period equivalence, primitive multiplicity, noisy patch comparison, rational/Hermite arithmetic, cutoff inequalities, smoothing exponents and the repeated-disk symmetry jump.

Ordinary and optimized Python output agree. The script does not run a TeX build or physical sensor and is not a proof certificate.

## 8. Audit limits

This was a targeted top-four rereview. It concentrated on:

1. whether v28 genuinely removes the repeated-shape/nonprimitive-presentation assumption;
2. whether the central-patch criterion implies a global period;
3. whether the accepted bounded list generates the full period group;
4. whether the finite noisy classification and rational locking are coherent;
5. whether exact, uniform-noisy and pointwise claims are properly separated; and
6. whether the corrected package meets the requested editorial threshold.

The review did not formally re-prove every theorem in the retained multi-volume programme, execute a physical apparatus, or conduct an exhaustive priority search.

## 9. Source-audit conclusion

The reviewed object is unambiguous and reproducibly pinned. Version 28 is a real mathematical revision. The exact retained v27 source is preserved, and the hosted exact-SHA eleven-document qualification succeeds.

The negative editorial recommendation in `REFEREE_REPORT.md` is therefore not based on source ambiguity or failed delivery. It is based on the information category, the bounded-periodic prior, the patch-margin requirement for uniform noise, manuscript architecture and the exceptional significance threshold requested by the author.
