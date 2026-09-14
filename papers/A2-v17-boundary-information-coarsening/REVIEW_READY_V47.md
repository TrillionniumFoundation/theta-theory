# A2 revision 47 — final review-ready entry

**Title:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 14, 2026

## Read the complete revision

[Complete main manuscript — 248 pages](../../deliveries/a2-v47/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/main.pdf)  
[Complete two-collision companion — 7 pages](../../deliveries/a2-v47/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/two_collision.pdf)  
[Complete frozen source archive](../../deliveries/a2-v47/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/native-source.zip)  
[Point-by-point response to the latest v46 report](RESPONSE_TO_REFEREE_V47.md)  
[Historical derivation audit](HISTORICAL_DERIVATION_AUDIT_V47.md)  
[Native evidence and fetched-Git-object verification](../../deliveries/a2-v47/219b39e94b14187561dc3b7e5bdbae49dbd92cc2/)

The historical paper-directory name `A2-v17-boundary-information-coarsening` is not the revision number. Both the main source and its PDF metadata identify revision 47. The linked PDF is the full manuscript, not a standalone supplement and not the older v46 PDF.

## Immutable identities

| Item | Identity |
|---|---|
| Latest report addressed | `reviews/a2-v46-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md` |
| Report commit / branch base | `45b42eee377c7fd3cff81c24c95acb91d6f46ab6` |
| Reviewed v46 native mathematical source | `ab99196fadc20682c1ee44d6bb433a788c7274ab` |
| Final v47 workflow preparation | `344905675ef544080e9d7139d31aa50abdd5f111` |
| **Actual compiled v47 mathematical source** | **`219b39e94b14187561dc3b7e5bdbae49dbd92cc2`** |
| Successful native and publication run | `34843699559`, attempt 1 |
| Native artifact | `10347280538` |
| Published products branch | `revision/a2-v47-native-products-34843699559-1` |
| Verified products head | `ec4d6faa66a96d6242fbb18138071919b267482c` |
| Final review branch | `revision/a2-v47-review-ready-2026-09-14` |

This review branch descends from the verified products head and adds review navigation and verification documentation only. It does not change the compiled mathematical source. The initial v47 run `34843244879` is superseded for review by the run above; the final layout keeps the condition of equation (19.19) with its inequality before the adjacent calibration clarification.

## Changes for the next referee

R46-P1 is addressed beside equation (19.19), on main page 92. The finite-flight bias is explicitly distinguished from timing and chart calibration error, with a cross-reference to the existing same-final-flight pilot.

New Section 19.7–19.9, main pages 94–97, contains Lemmas 19.7–19.8, Theorem 19.9, and Corollary 19.10 with full proofs. It bounds offset error, hard-cell boundary crossing including outer edges, calibration-aware categorical confidence, and a finite jointly chosen grid, same-flight pilot, successful sample size and total preparation cap. The table and unknown marked lattice remain the reconstruction target. Introduction Section 1.9 is on page 10.

The response preserves the report's favorable C1–C4 findings and addresses E1 through the actual mathematical architecture rather than representing an editorial placement judgment as a closed proof obligation. The original nonlinear relative-law and finite-remainder inverse, generic finite-channel theorem, all local experiments, physical reconstruction results, auxiliary material and companion are retained.

## Preservation and reproduction results

The frozen main-plus-companion active-source manifest contains 101 inherited files. Of these, 99 remain byte-identical in place; the other two have exact original Git objects archived under `history/v46-review-baseline/` and only prescribed additive changes. All inherited main input order is retained. The current manifest contains exactly 103 active files, including two new modules. All 233 inherited main theorem-style environments, 22 remarks and 224 proofs remain; four theorem-style environments and four proofs are added. The companion is unchanged.

Both native jobs and both publication/verification jobs of the final run succeeded. The complete companion was built first, followed by the complete main, using native LaTeX with shell escape disabled. The final main has five underfull-box notices, no overfull-box notice and no unresolved reference or citation. The companion has no recorded build warning.

The downloaded final artifact ZIP matches GitHub's SHA-256 digest. All 34 evidence entries listed in the native build report were checked against their bytes and hashes. All 103 active inputs in the source ZIP match both their recorded hashes and the locally built source. The v47 preservation/calibration checks and inherited quantized/adaptive/v32/v38 checks agree under ordinary and optimized Python.

All 248 main pages and all 7 companion pages match the separate local reconstruction in extracted text and in same-renderer 72-dpi pixels. Their PDF byte streams are not asserted identical. Readable-resolution visual inspection covered main pages 1, 2, 10, 92 and 94–97; no clipping, overlapping equations or broken glyphs was observed on those pages. Whole-document pixel comparison is not a claim of individual visual inspection of every page. See `DELIVERY_VERIFICATION_V47.json` for the post-download comparison record.

| Product | Pages | SHA-256 |
|---|---:|---|
| Complete main | 248 | `622ac0d72dc6c6c460d3aaf4375de424a0aff2279d77a306abc1a9c8e14678e5` |
| Complete companion | 7 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Final downloaded artifact ZIP | — | `90d5894ff1761d3260cc2299ed3f66a3229d763d2a61ecf0ead2ca238ccb7458` |

These checks establish source preservation, finite diagnostic reproducibility, successful full native compilation and artifact consistency. They are not a formal mathematical certificate or a journal-acceptance decision. The exact fresh proof-audit scope is recorded in the historical audit; the complete inherited proofs are available for renewed independent review.
