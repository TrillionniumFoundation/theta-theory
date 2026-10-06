# A2-DYN, revision 25

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

**Entry:** `main.tex`. **Controlling report:** v24 at `92a8236e149c79c797fa85dacf5953e69b8960ff`. **Author baseline:** `c1d6940a875f501ee1957204e81772df7b9b39d6`; ordinary paper tree `f15ab9854d022319db374f8ce38f4e6a4273dd84`.

Theorem O adds prescribed-count Fourier cancellation with different widths in the four physical coordinates. A fixed arbitrary-order damped residual expansion yields a feasible region `max theta_i < 1/10`, `sum theta_i + max theta_i < 1/4`, with explicit integrated rates. A concrete box reaches physical flight-time frequency `2 n^(-41/100)` and transverse frequencies `2 n^(-49/100)`. Its annular raw integral is `O(M_a n^(-1/40)+V_a n^(-497/25))`; the central comparison on its union with the old isotropic ball retains the original rate and variation budget. This is a prescribed-count integral with the full raw n^2 factor, not an average or a full-isotropic-annulus claim.

New source:

- `core/52_high_order_damped_unsmoothing.tex`: all fixed small-mass even moments, explicit heterogeneous cumulant comparison, and high-order corrected chronological words.
- `core/53_anisotropic_fixed_count_bands.tex`: separate-width theorem, concrete flight-time extension, same-event bound, and exact coordinatewise-kernel raw identity.
- `core/54_dependency_guide.tex`: appendix separating proved conclusions from remaining raw estimates.

All 51 inherited core files, all inherited Python files, and the bibliography are unchanged. Six exact replacements in `main.tex` are recorded in `INHERITED_EDITS.json`. The original title, family, true section, four-coordinate record, raw mixed-density endpoint, and all inherited theorem labels remain.

The full fixed-count complement, long-time raw derivative budget, active-kernel edge smallness, weighted exact denominator, and relative physical-event comparison are not marked proved by this revision. `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md`, and `HIGH_ORDER_INPUT_MAP.md` give the exact scope and dependencies.

Run `bash papers/A2-DYN-v25-referee-response/build.sh` in a full checkout. The exact-source workflow checks normal/optimized diagnostics, compiles the complete article without shell escape, and archives the event source and dynamic receipt. CI is source/build evidence, not a continuum proof certificate or journal decision.
