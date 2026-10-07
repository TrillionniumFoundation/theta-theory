# A2-DYN — revision 29

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. The controlling report is the substantive v26 report at `20337e845157a833fe770687ea98f337788fa586` (blob `f75e48fa7276be7be654c61afe3cc276ba44d514`). The immediate remote parent is the v28 snapshot `b9b976cd93df7513018f03dea0df5ffe80920e01`, which contains the v27 ordinary paper tree `ae335b52f013e3569e4a6b79b899cfc00e26b8e4`. That snapshot was source transport, not a new qualified mathematical revision. We retain and validate the v27 window proofs rather than discard or duplicate them.

## New results

Theorem T proves a stationary physical window denominator and relative comparison with actual deterministic-return and last-return events. The probability is asymptotic to `8 t^(-6/25) g_{V_R}(xi)`. The relative symmetric difference and conditional total variation are `O(t^(-23/2800) sqrt(log(2+t)))`. Physical coordinate half-widths are `t^(21/50)` and use the exact integer displacement and collision intervals.

The two new proof modules are `core/59_stationary_collision_band.tex` and `core/60_stationary_physical_conditioning.tex`. A full isotropic **collision-clock** band of rescaled radius `m^(9/100)` follows from fixed orders `P=40`, `Q=29`, without a return stopping error. Projection uses four-dimensional envelopes and a fixed 128th-moment truncation, not a Fourier-plane trace. Equilibrium is represented by the actual return suspension: the section origin is roof-length biased, while the current outgoing collision has bounded-BV density `tau_R / mean(tau_R)`. The two densities are never interchanged. Uniform high-moment coupling and an exact denominator give the relative event theorem on the same stationary probability space.

All 58 inherited core modules, all 55 inherited Python files, the bibliography and all old mathematical labels remain byte-identical or retained as applicable. Only five precisely recorded edits modify `main.tex`; all inherited proofs are unchanged. The original raw mixed-density target, pointwise common correction, prescribed-count complement, long-time density-derivative budget and microscopic conditioning requirements remain visible.

## Verification

Run `bash papers/A2-DYN-v29-referee-response/build.sh`. The read-only exact-SHA workflow checks complete baseline/source hashes, the exact edit replay, all inherited labels and modules, normal and optimized finite diagnostics, native TeX, and a clean scoped source tree. Dynamic receipts bind the source to the workflow SHA, run ID and PDF hash. Numerical/algebraic tests and successful typesetting are not continuum proof certification or independent human review.

See `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md`, `STATIONARY_WINDOW_INPUT_MAP.md`, and `VALIDATION.md`.
