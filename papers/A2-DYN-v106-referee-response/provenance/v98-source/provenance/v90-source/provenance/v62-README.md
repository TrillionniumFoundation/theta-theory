# A2-DYN, revision 62

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. This revision responds to the latest external report, revision 60 at `47263fb3033b4545ed3b1e96646f56c9812e7de4`, and continues the complete revision-61 author source at `3fb563abbef5a119164cc92a360e6e8434e0d92b`. The v61 author advance is retained rather than repeated or overwritten.

## New physical results

`core/133_finite_type_clearance_coarea.tex` proves a positive essential-height bound for the original first-clearance source on actual roof-fiber finite-type strata. At order r the bound is `C_r A_r^m a^(-1)(epsilon/b)^(1/r)`, with explicit lower thresholds for the roof pivot and the r-th derivative along its level curve. In particular the second-order result includes rank-zero fold contacts on a regular roof fiber. Every uncovered source point remains in an exact positive remainder.

`core/134_clearance_caustic_localization.tex` constructs the physical-side clearance caustic in parameter–roof space. At a fixed collision count and positive incidence threshold it has finitely many values at each radius, with an exponential component-count bound. A compact semialgebraic separation inequality gives the original coarea denominator off its neighborhood. The resulting raw-error formula retains the exact caustic source, including roof-critical contacts and physical-side seam limits. A separate tube-measure estimate gives a source-mass bound, not a height estimate.

These results concern the original circular Lorentz sources and retain the exact return, displacement and collision labels, the image mark j+1, and later incidence defects after a first clearance. They do not replace the source by the correlated Markov model. The finite-count constants and the dependence of the separation exponent on m and the incidence threshold remain visible. Neither ordered Lorentz central-height limit is marked proved.

## Complete source and review route

All 132 inherited core files, all 179 inherited Python files and all compiled appendices remain byte-identical. All 1761 old mathematical labels and the A–X synopsis remain compiled. Fourteen revision-61 editorial files are archived verbatim. The bibliography is append-only. The new full manuscript includes 134 numbered core modules.

Read `JOURNAL_ROUTE.md` for the direct proof route and `RESPONSE_TO_REFEREE.md` for the itemized response to 24.1–24.9. `SPECIALIST_AUDIT_MAP.md` separates the new finite-type/coarea arguments from their inherited continuum inputs.

Run `bash papers/A2-DYN-v62-referee-response/build.sh`. The exact-source workflow verifies the frozen baseline, report, inherited sources, mathematical labels, ordinary payload tree and read-only workflow, then performs normal and optimized finite checks and native typesetting. Dynamic receipts identify the execution SHA and actual PDF. Source qualification is not an independent specialist proof audit.
