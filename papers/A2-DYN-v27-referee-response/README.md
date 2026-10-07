# A2-DYN — revision 27

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. This revision continues the latest v26 referee report from reviewed source `6a790b65b48f57d264dbc7871bd1ae46571c2662`. The controlling report is frozen at `20337e845157a833fe770687ea98f337788fa586`, blob `f75e48fa7276be7be654c61afe3cc276ba44d514`.

## New mathematics

Theorem R proves unsmoothed window probabilities and a size bound for the signed window integral of the common raw correction, not merely a difference between two corrections. The proof uses explicit order-preserving bandlimited envelopes with endpoint checks for the three integer coordinates. The common correction is averaged with its cancellation preserved; neither an essential-supremum nor an absolute residual estimate is inferred.

Theorem S proves a genuine relative comparison at deterministic physical time under a section-start law. The event has exact integer displacement/collision-count intervals of physical half-width `t^(23/50)`, with probability asymptotic `8 t^(-3/25) g_{V_R}(xi)`. The physical and deterministic-return events have relative symmetric-difference error `O(t^(-11/1400) sqrt(log t))`, and their conditional laws obey the same total variation bound. The projected denominator is proved by four-dimensional truncation, not an invalid trace of an L1 Fourier estimate.

The new sections are `57_unsmoothed_window_remainders.tex` and `58_relative_physical_windows.tex`. Every inherited core module remains byte-identical. The complete raw microscopic theorem, its pointwise common remainder, full fixed-count Fourier complement, long-time preparation budget, and original fixed-label conditioning requirements remain explicit. New mesoscopic events do not replace those targets.

## Build

Run `bash papers/A2-DYN-v27-referee-response/build.sh` from a repository checkout. It replays the exact inherited edits, checks all source hashes and retained labels, runs normal/optimized finite diagnostics and the historical diagnostic chain, and compiles the entire article. The read-only GitHub workflow archives the exact source, records its SHA/run ID/PDF hash, and renders proof-entry pages. Source qualification is not continuum proof certification.

See `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md`, and `WINDOW_AND_EVENT_INPUT_MAP.md` for the exact claims, dependencies and remaining responsibilities.
