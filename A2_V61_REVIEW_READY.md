# A2 revision 61 — complete delivery and guide for the next referee

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 16, 2026

## 1. Frozen objects and branch roles

| Object | Immutable identity or branch |
|---|---|
| Addressed referee report | `396bb28e17ba9944af5ff89a2db601412eeb95ee` |
| Reviewed v60 mathematical source | `1a55bfb1102c3eab9cdcd6a292c5ef9070ea14a5` |
| Revised v61 mathematical source | `71e0bd6306f54466728c2e6e781bb0f422c5cfb0` |
| Revised manuscript subtree | `ee2d39dbce4dce4d972ec1a281af1df9aaf44d4a` |
| Source branch | `revision/a2-v61-relative-mechanism-2026-09-16` |
| Native workflow / attempt / artifact | `35043311589` / `1` / `10426471183` |
| Published products commit checked by the native attestation | `3bb9ee14856a5787e532f1c76e6f09fc98767a7e` |
| Products plus fetched-object attestation | `0c2f77ddb87ad755963930215e8637fc7f1f1f6f` |
| Products branch | `revision/a2-v61-native-products-35043311589-1` |
| Review-ready branch | `revision/a2-v61-review-ready-2026-09-16` |

The review-ready branch descends from the products-and-attestation commit. Its added index and receipts are outside the manuscript source subtree and do not change the mathematical input to the completed build. The historical manuscript directory remains `papers/A2-v17-boundary-information-coarsening/`; the active revision is 61.

## 2. Complete manuscripts

All links below lead to retained Git objects, not expiring Actions-only artifacts.

| Entry | PDF | Pages | Git blob |
|---|---|---:|---|
| Principal article | [rigidity.pdf](deliveries/a2-v61/71e0bd6306f54466728c2e6e781bb0f422c5cfb0/rigidity.pdf) | 119 | `20933282dc3abee2acb910854a79a0a392c7e772` |
| Full technical manuscript | [main.pdf](deliveries/a2-v61/71e0bd6306f54466728c2e6e781bb0f422c5cfb0/main.pdf) | 294 | `004f34e0625164d6de6668e98aa0f86494a3dcee` |
| Two-collision companion | [two_collision.pdf](deliveries/a2-v61/71e0bd6306f54466728c2e6e781bb0f422c5cfb0/two_collision.pdf) | 7 | `dae9697f40bcac775d7dd6aa26144af0181adc75` |

The [native source archive](deliveries/a2-v61/71e0bd6306f54466728c2e6e781bb0f422c5cfb0/native-source.zip) contains all 753 frozen manuscript files and its source manifest. The build report, raw logs, recorder inputs, generated-auxiliary provenance, preservation results and post-push Git-object attestation are retained alongside the PDFs.

SHA-256 values:

```text
rigidity.pdf       9ebcc7869b1b7d25f5cc573d9288f4c07ccefe623df3a2cea3052356d7a1da18
main.pdf           c10119eadcf29c93967d7e3aab447c0a65f1265ceae3827d69d6593c200fbefa
two_collision.pdf  b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1
native-source.zip  81a733a228b6815e78a175e41ce1a108570f140e6356756744ff286087658b21
outer Actions ZIP  8a08c96bbaaae1a9fc15c4f292bb899c0b7cfab25ac286b6e696eafd699e8b56
```

## 3. The revision and the requested reassessment

The [point-by-point response](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V61.md) covers R60-M1–M5, R60-C1–C3, R60-E1–E2 and R60-D1–D4. The report accepts the three v60 statements in its scoped examination and establishes no new mandatory core error. Its principal reservation concerns exceptional significance. The response does not transform that judgment into a false claim of a repaired mathematical gap.

The revised principal introduction distinguishes the long-flight limit at fixed positive excess time from a quadratic small-offset approximation. It centers exact cofactor normalization, two-ended trace-class control and the actual-smooth stationary-envelope inverse. It brings the existing finite-flight inverse and the realized nonlinear-information comparison into the account of the mechanism. The complete analytic inverse and conditional real-observation result remain at their stated strengths; scalar continuation and smoothing are not presented as an unrelated second breakthrough.

The principal local theorem, all global finite-fiber and proper-asymmetry conclusions, unknown-origin/window reconstruction, differential kernel, immersed-model scalar coordinates and the full acquisition/statistical catalogue remain. The acquisition application continues to import full Theorem F.47.3 substantively, including its additional hypotheses. No unmarked channel-discovery, ordinary marked-length equivalence or globally finite-scalar recovery theorem is added by implication.

The [author-side cover letter](papers/A2-v17-boundary-information-coarsening/COVER_LETTER_V61.md) makes the affirmative significance case. The [historical proof audit](papers/A2-v17-boundary-information-coarsening/HISTORICAL_DERIVATION_AUDIT_V61.md) records which modules were read and used. The [dependency declaration](papers/A2-v17-boundary-information-coarsening/journal/DEPENDENCY_LEDGER_V61.md) and [primary-source comparison](papers/A2-v17-boundary-information-coarsening/LITERATURE_CHECK_V61.md) record the retained distinctions. These author-side documents are not part of the principal mathematical prose and do not imply a commissioned journal review.

## 4. Preservation and reproducibility

Every one of the 739 inherited frozen manuscript paths remains. Of these, 736 are byte-identical in place. The changed inherited files are only `main.tex`, `rigidity.tex` and the manuscript `README.md`. The original two TeX entry files are preserved exactly in `history/v60-review-baseline/`; the original principal introduction remains unchanged at its existing path.

The new principal introduction is selected in place of the old introduction, with all of the old introduction's mathematical statement/proof environments retained verbatim. No theorem/proof module is modified. The union of active TeX inputs remains 123: 113 for the full manuscript, 44 for the principal article and one for the companion, with overlaps. These counts describe the input graph, not the number of independent theorems.

The native build and publication jobs both passed. The preservation checker produces identical normal and optimized Python output. The downloaded artifact was checked for all 753 frozen file lengths, SHA-256 values and Git blobs; all 45 build-report evidence entries were verified; all 123 active source bytes agree with the local candidate. The native retention attestation verifies the fetched published Git objects. Successful build and preservation checks do not certify mathematical correctness or exceptional significance.

The preceding run `35043080259` stopped before typesetting because the new checker used `git ls-tree` from a nested working directory without `--full-tree` for an already-selected subtree. The fix added `--full-tree` and a non-vacuity guard for expected baseline keys. This checker-only fix changed no mathematical source. The successful completed run is `35043311589`.

## 5. Typesetting and visual coverage

The final logs contain no undefined references or citations, missing-character reports, overfull boxes or LaTeX errors. There is one underfull-box notice in the principal article and three in the full manuscript; the companion has none. All 420 native PDF pages agree with the local build in extracted text. The native and local PDF bytes are not claimed identical.

Actual visual inspection covered principal pages 1–9 and full technical pages 1–2, including the changed abstracts, introduction and nearby transitions. Those 11 pages are pixel-identical between the inspected local build and native products under the same renderer at 90 dpi. Native principal pages 3 and 7 and full technical page 1 were additionally opened at 108 dpi. No clipping, overlap or unreadable mathematical display was seen on those pages. This is not an all-page visual inspection. The structured results are [LOCAL_DELIVERY_VERIFICATION.json](deliveries/a2-v61/71e0bd6306f54466728c2e6e781bb0f422c5cfb0/LOCAL_DELIVERY_VERIFICATION.json).

This revision concentrated its reading on the relative/action chain and the realized comparison needed for R60-E1. It is not a fresh line-by-line verification of the complete 420-page corpus. The next referee should assess the revised mechanism-centered case and the preserved mathematical claims, not infer acceptance from revision numbering or delivery certificates. A1, prior reports and the default branch are untouched.
