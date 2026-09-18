# A2 revision 82 — referee entry

## Exact identity

**Title:** *Action rigidity with selective detection*  
**Branch:** `revision/a2-v82-selective-detector-rigidity-2026-09-18`  
**Mathematical source commit:** `80133d376cc28cc8f2555f58324a3285f9dcfb67`  
**Inherited source head:** `8315577eeb8dcc711c4c1c89fc804d132be2e52e`  
**Controlling review head:** `2edd50e3f97228432ab3c7a1e1f11618f8f45a09`

The controlling report is the v80 report in `reviews/a2-v80-calibrated-records-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md`. The existing v81 revision was inspected and inherited rather than relabelled as new work. This is a new substantive v82 revision, not a new independent review.

## Reading order

The [complete integrated manuscript](papers/A2-v17-boundary-information-coarsening/rigidity_v82.tex) is the full submission source. The [self-contained core reading edition](papers/A2-v17-boundary-information-coarsening/rigidity_v82_core.tex) contains all new proofs and is not a substitute for the retained companions. Both use the same [principal article](papers/A2-v17-boundary-information-coarsening/article/v82/principal.tex).

The [point-by-point response](revisions/a2-v82/RESPONSE_TO_REFEREE.md) covers M1–M20 and T1–T15. The [proof/dependency ledger](revisions/a2-v82/PROOF_LEDGER.md) distinguishes inherited arguments, new conclusions and retained hypotheses. The [verification record](revisions/a2-v82/VERIFICATION.md) states exactly which checks were executed.

## Mathematical change

Five projective clock matrices identify absolute generating actions despite unknown branchwise log-affine detection, unknown visible component count, endpoint-dependent uncalibrated independent readings and missing scalar masses. The result includes complete continuous-gauge classification, action coincidences separated by detector rates, a finite-degree extension and explicit clock obstructions. A fixed-source nonconvex three-sheet return system realizes the crossed-action case. All substantive v81 inputs remain active in the full entry.

This does not assert a canonical unmarked billiard theorem, recovery through unobserved caustics, a discovered global section/phase cover, arbitrary hidden-component discovery or a sharp geometric sampling rate. Those hypotheses are not silently removed from the retained results.

## Build and provenance

The **10-page core** was natively compiled and visually inspected. **15 algebra/regression checks passed.** The core source graph is recorded in `revisions/a2-v82/core-source-graph.json`. The complete integrated manuscript was **not natively built locally**; the native workflow compiles both entries on the exact checkout and records a source-matched artifact only when it actually runs successfully.

Core PDF SHA-256: `ce2eae0f787aaf249f617c2150d96a1c8bf5fdae9ae2eadbb3c63201f50b77dc`.

Reproduction from a checkout with Python NumPy/SciPy/SymPy, latexmk and the required TeX packages:

```bash
bash scripts/build_a2_v82.sh
```

The old README is archived byte-exactly as `revisions/a2-v82/README_before_v82.md`. Historical manuscript and review files, the default branch and prior revision branches are unchanged. A delivery commit may add only handoff/checking materials after the pinned mathematical commit; the scientific source identity above remains the comparison target.
