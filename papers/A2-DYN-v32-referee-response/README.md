# A2-DYN revision 32

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The full article is `main.tex`. This revision responds to the v31 report at `ea8b02f156b1d99633443103ae5e88eb96a89fce`, from author source `c0b184a89ff3d38675d0bc90a9e60b584476e5c3`. It retains the original model, record, raw microscopic target and every inherited theorem.

Theorem W adds positive finite-band reconstruction on the original trajectory space. The new source-geometric section makes the collision differential, all-candidate guard, chart coefficients and boundary zero extensions self-contained, then extends the positive extraction to the actual stationary entrance law. The second new section proves a global mixed-L1 approximation and a microscopic event-measure approximation uniform against all bounded measurable trajectory statistics. No selector derivative or BV norm is needed for this finite-band formula.

The event likelihood lies between zero and one. Its normalization gives conditional total-variation bounds with the exact denominator explicitly present. Singleton lattice labels and shrinking roof intervals are retained. The bandwidth has `log B_n=O(n log n)`, not polynomial size. These are reconstruction theorems; the remaining finite complement is not evaluated by a Gaussian, and global L1 approximation is not the pointwise raw LLT.

Run `bash papers/A2-DYN-v32-referee-response/build.sh`. The read-only workflow qualifies the ordinary committed source at its exact SHA. `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md`, `POSITIVE_MICROSCOPIC_INPUT_MAP.md`, `INHERITED_EDITS.json`, and `SOURCE_MANIFEST.json` document the mathematics, preservation and execution boundaries. Dynamic receipts and render summaries are build artifacts, not proof certificates.
