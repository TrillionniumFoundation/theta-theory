# A2 v7 revision for renewed independent review

The materialized manuscript is `papers/A2-v7-critical-boundary-experiments/main.tex`.

**Title:** Relative boundary laws and statistical reconstruction in periodic dispersing billiards.  
**Author:** Qian Qi. **Date:** September 9, 2026.  
**Revision branch:** `revision/a2-v7-critical-boundary-experiments-2026-09-09`.  
**Manuscript tree:** `ec45463bb01f2a9b7e64022136294952e4ce265a`.

The controlling referee report is at `f1728f5d96ea01b1326daf9a6a36352b2e270be1`, in `reviews/a2-v6-relative-transfer-harsh-independent-2026-09-09/`. The reviewed author baseline is `4ca186258c92dcbc75accc4eb576e307cc612189`. This revision is based on the review commit and preserves all existing repository paths. The new paper directory clones the complete remote v6 manuscript tree; it is not a pointer-only submission.

Start with `papers/A2-v7-critical-boundary-experiments/RESPONSE_TO_REFEREE_V7.md`. The same directory contains `PROOF_LEDGER_V7.md`, `SOURCE_PINS_V7.json`, `VERIFICATION_V7.json`, the unchanged controlling report under `review-basis-v6/`, and reproducible build and diagnostic scripts under `tools-v7/`.

## Mathematical changes

V6-R1: Section 1.6 and Table 1 specify the observation, supplied information, unknowns, topology, cost, and uniform variables for each experiment.

V6-R2 and R3: Theorems 7.1 and 7.3 prove the unequal-contact, both-parity quadratic overlap and the actual positive-offset joint testing limit. With `q_j = exp(-j gamma)`, the exact tangent separation is `(2/pi) arcsin(q_j)`. Conditional scaling `k_j q_j -> b` with `k_j sqrt(d_j) -> 0`, or raw scaling `n_j p0_j q_j -> b` with `n_j p0_j sqrt(d_j) -> 0`, gives total variation `1-exp(-2b/pi)` and equal-prior testing error `exp(-2b/pi)/2`. The even-contact remainder improves from `sqrt(d)` to `d`. These are fixed-table simple binary experiments, not unknown-table simulation or a sharp nonlinear fixed-offset rate claim.

Theorem 20.2 proves a physical weighted-exposure and adaptive Bernoulli-query lower bound; its shrinking-offset, bounded-flight scope is explicit. Theorem 21.2 acquires the previously supplied shrinking gap bracket from a fixed local interval, caps all later waiting times, and includes coarse search, fine calibration, and amplitude acquisition in the sufficient fixed-m rate `C_m epsilon^(-(6+6/m)) log(C_m/eta)`. Its wider initial offsets are not folded into the narrower lower-bound claim.

V6-R4: Lemma 8.1 specifies and proves a Borel exact compact minimizing selection; the pilot root convention is also measurable. All old mathematical proof inputs remain active in their original order; the new manuscript adds five source inputs and preserves the independent two-collision companion.

## Observed verification

The clean local build produced a 72-page article and 7-page companion, with no unresolved references or overfull boxes. Nonfatal font-expansion and underfull-box notices are recorded. Both PDFs were rendered and inspected. Article PDF SHA-256: `3d33e675c7545326816a5ed6849af14703885cfd2dda30c5df23317fbbc33331`. Companion SHA-256: `48f608d2ce80478f8c7acdcb6da7028ab3e8aa977772320d66064cf912b58506`.

The new diagnostic script passed 134 checks (98 exact, 36 ordinary floating); the unchanged controlling referee script passed 190 (162 exact, 28 ordinary floating); the unchanged v6 author script passed 147 (112 exact, 35 ordinary floating). Each normal/optimized output pair was byte-identical in the recorded environment. These are local finite diagnostics, not remote CI, physical billiard simulation, interval arithmetic, formal proof, or journal-acceptance certificates. Full run outputs and compiled PDFs are supplied in the portable revision packet; the repository contains the complete buildable source and compact verification evidence.
