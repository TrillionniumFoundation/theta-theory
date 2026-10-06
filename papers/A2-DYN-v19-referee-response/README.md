# A2-DYN, revision 19

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. Theorems A--I and all 41 inherited core modules are retained without changing their text. Theorem J and two new sections sharpen finite-record reconstruction and prove central Gaussian and actual moment limits for multiple observations in a growing window of actual returns.

## New results

The finite sign-condition bound used in the original collision graph has both its variable count and its test count linear in the collision length. Keeping its binomial form gives `C exp(C L)`, rather than the coarser `exp(C L log L)`. This yields an exponential first-variation budget, a single-logarithm actual return defect bound, and improved constants in the inherited finite-rank resolvent and finite-time comparison.

For a product of bounded-BV observations at distinct returns in a window of length at most `a log n`, the paper constructs a finite-collision approximation of the whole product and then removes the approximation in the original measure. It proves an integrated central Gaussian comparison on an explicitly positive polynomially growing band and actual first/second moment convergence under the unchanged multiple-time event. A nonempty set of frequency, window-length, variation and rare-event budgets is exhibited without assuming a relation between geometric-complexity and return-tail constants. The original single-mark band is not reduced.

`core/42_exponential_reconstruction.tex` and `core/43_logarithmic_return_windows.tex` contain all new proofs. `RESPONSE_TO_REFEREE.md` maps them to the latest located v16 report. `EXPONENTIAL_WINDOW_INPUT_MAP.md` specifies the primary finite-complexity input and its use.

## Frozen source and chronology

The latest located substantive report is v16 at `b0b7ddfcd90f493e02254742b33174e9108fc5a7`, report blob `805f04cd60d144bc6321ce3f4304ebe1cda34999`. Revision 17 was already ordinary source. At the start of this task the existing v18 branches still pointed to assembly staging commit `cdc8d64784d266153cce0482944ec342d1c70854`; their assembly had produced the exact ordinary paper subtree `e19803bed418d2a1402781124f91737c136b595b`. This subtree was pinned unchanged on the new v19 branch. The frozen baseline is accessible at `68618cdaad6824912b49b505d58c9a9fcb0ab823`, under `papers/A2-DYN-v18-referee-response`. Existing v18 and review refs were not moved by this revision.

The title, physical family, actual section, joint record and raw mixed-density objective remain unchanged. The full complementary Fourier estimate, uniform long-time raw residual derivative and local-edge estimates, and relative event replacement for exact physical observations remain distinct analytical tasks. A conditional central or moment theorem is not called a conditional raw LLT.

## Qualification

Run `bash papers/A2-DYN-v19-referee-response/build.sh` in a checkout. Source hashes, exact inherited edits, all inherited labels and bibliography entries, finite diagnostics in normal and optimized Python, and native typesetting are checked. `.github/workflows/a2-dyn-v19-qualification.yml` qualifies the exact committed ordinary source, read-only, and emits a run-bound receipt and PDF hash. A successful build is not continuum proof certification or journal acceptance.
