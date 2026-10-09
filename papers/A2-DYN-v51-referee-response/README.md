# A2-DYN revision 51

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

This is a complete manuscript, not the revision-50 source-freeze charter. The active source is `main.tex`. It retains all 107 revision-49 core modules, all 135 inherited Python files, the bibliography, both inherited compiled theorem appendices, and every inherited mathematical label. It adds two proof modules and an article-level input map.

The parent review is `e951b35077f020ae7e5ac711510e49be1faeb4ef` (the revision-50 submission-status report). The substantive mathematical baseline is revision 49 at `f3174ed1e7e339aa9c4bb5bd716a24653080c7dd`, and its controlling mathematical report is `11520f4876ca9033c0a0abfbdb0041e1f85c260e`.

## New mathematics

The complete raw error is uniformly approximated, after the collision limsup at each fixed reconstruction band, by the **positive** physical remainder, with error `O(B^(-1/192))`. This proves an arithmetic pointwise lower local law for the unmodified exact-index density. It does not assert a two-sided pointwise law. The remaining two-sided criterion is now equivalent to positive essential-height smallness of incidence and clearance separately, rather than an unanalysed cancellation between their signed corrections.

On positive arithmetic targets, the lower law gives microscopic denominator lower bounds for arbitrary measurable roof sets, including sets shrinking after the count is chosen. On fixed windows with a pointwise positive transition reference, the exact conditional roof law dominates an asymptotically full copy of that reference. Reverse likelihood and reverse relative-entropy discrepancies tend to zero. No single-roof path bridge or forward likelihood bound is claimed.

## Read and build

The two new sections are `core/108_positive_remainder_lower_law.tex` and `core/109_exact_roof_minorization.tex`. The introduction states the lower theorem next to the retained full-source local-variation theorem. `RESPONSE_TO_REFEREE.md` answers both the procedural v50 report and the substantive v49 report. `SPECIALIST_AUDIT_MAP.md` and the compiled input appendix separate inherited continuum inputs from the new real-analysis argument.

Run `bash papers/A2-DYN-v51-referee-response/build.sh` in a checkout. The read-only workflow runs the baseline and new verifiers, normal/optimized finite checks, native TeX, and label-based page renders. Only the dynamic receipt records the actual event SHA, run ID, PDF hash and source tree. Build success is not a continuum proof certificate.
