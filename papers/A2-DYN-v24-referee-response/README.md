# A2-DYN revision 24

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete ordinary-source article is `main.tex`. This revision continues the latest substantive v22 referee report, retaining the recovered v23 mathematical source rather than overwriting or duplicating its branch. The title, physical family, actual return section, joint record and raw mixed-density endpoint are unchanged.

## New mathematics

Theorem N and `core/50_multiscale_stopping.tex` prove a fourth-root actual stopping estimate in every fixed finite moment. Dyadic clock-deviation shells replace one global exceptional set. In particular, the normalized L2 stopping error and actual covariance error are `O(n^(-1/4))`. The proof at second moment needs only fourth collision moments and the cumulative-return tail. A marked cumulant argument also proves every fixed Gaussian polynomial moment, with separate supremum and variation costs, at any one actual return mark.

`core/51_rate_preserving_band.tex` combines this comparison with the retained damped cubic unsmoothing. The fixed-count raw-normalized annulus extends to physical support radius `2n^(-633/1400)`, or rescaled radius `2n^(67/1400)`, while the enlarged integrated Gaussian comparison retains the original `n^(-3/280) sqrt(log(2+n))` supremum-norm rate and `n^(-9/175)` variation rate. The exact weighted raw budget is recomputed with the new kernel. The same-event conditional result therefore retains the original probability and variation budget on the wider band.

All 49 inherited core files, all inherited Python scripts and the bibliography are unchanged. Theorem M and its two proof sections remain present as the staged contribution on which the new comparison builds. Five exact introduction edits are replayed from the frozen source. No existing author or review branch is rewritten.

## Read and reproduce

`RESPONSE_TO_REFEREE.md` answers the latest report item by item. `MULTISCALE_INPUT_MAP.md` and `PROOF_LEDGER.md` identify the proof dependencies. `INHERITED_EDITS.json` records the exact main-file changes; `SOURCE_MANIFEST.json` identifies every ordinary source file and the immutable baseline tree.

Run `bash papers/A2-DYN-v24-referee-response/build.sh`. The read-only final workflow checks the exact event source, normal and optimized finite diagnostics, retained geometry checks, native TeX and a dynamic build receipt. Finite calculations and compilation are not continuum proof certification.

The farther fixed-count complement, long-time raw second-derivative sum, local extracted-edge estimate, weighted raw denominator asymptotic and relative physical-event replacement remain explicit mathematical requirements. They are not removed from the organizing raw LLT.
