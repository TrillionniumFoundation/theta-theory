# A2-DYN revision 33

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. Theorem X and core modules 67--68 analyze the original stationary physical singleton event `(W_R(t),C_R(t))=(k,m)` directly, retaining both within-flight cell corrections and the true initial age. A flight-age overlap gives a uniform second-derivative **measure** bound for the time profiles, absolute Fourier inversion, and a pointwise far-frequency error `C/B` independent of the prescribed physical collision count. The central three-dimensional Gaussian term is evaluated at rate `m^(-11/700) sqrt(log m)`. A polynomial bandwidth `B_m=m^(P+3/2)` leaves one explicit finite signed middle integral on the physical local scale.

A positive likelihood on the original stationary trajectory has absolute source-TV error `C/B` against every bounded measurable selector. Normalization still requires the selected denominator. The finite signed middle integral is not claimed small, and the full four-coordinate return LLT is not claimed proved. `REFEREE_STATUS.md` separates these remaining responsibilities from the new direct physical tail theorem.

Baseline: `f63fb5101c8bcf6202abf4468d703be6242923a1` (v32), ordinary paper tree `d6462c94e0cb7a702bf4e46e60da0440fb94a5ac`. Controlling report: v32 at `c41e23ea3494aaa40502aed990c6d46b9bce1153`. The new branches start from that review commit, retaining the report and all previous paper directories.

All 66 inherited core files, 71 Python files and the bibliography are byte-identical. The five main-text edits are exactly replayed by `INHERITED_EDITS.json`; the v32 abstract is preserved in `HISTORICAL_ABSTRACT_v32.md`. No inherited theorem label is removed.

Build: `bash papers/A2-DYN-v33-referee-response/build.sh`. The read-only exact-SHA workflow verifies and archives source, runs normal and optimized finite checks, compiles the full paper and renders proof pages. Dynamic receipts contain the exact source SHA and PDF hash. Compilation and finite checks are not continuum proof certification.
