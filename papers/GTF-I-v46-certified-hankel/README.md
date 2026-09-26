# General Theta Foundations I — Revision 46

**Certified Positive Realization of Numerical Word Experiments**  
Qian Qi · 27 September 2026

**Release state: readable manuscript and response; remote build not completed.** See [publication status](PUBLICATION_STATUS.md). The last observed GitHub Actions run was queued. A tool safety check blocked direct publication of the new verifier program; this release does not disguise that as a successful native-code or artifact publication.

Controlling report: r29, `6e8a9504a1a0820e6195317df885d99aed06c878`, reviewing v43. The inspected published mathematical predecessor is v44, `d7042cf71485f661e27d87d12ffae35a2edfc15c`. The separate v45 draft was staged/queued at the initial survey and is not claimed as mathematically reviewed. This work preserves its frozen base `36f5865f4f3f2e3a28993ffd7e3fb622ca930672` without changing its files.

Work branch: `revision/general-theta-foundations-i-v46-certified-hankel-2026-09-27`. Manual source-review branch: `revision/general-theta-foundations-i-v46-source-review-2026-09-27`. A successful automated referee-ready artifact release is a separate status and is not asserted.

[Complete LaTeX manuscript](main.tex) · [New certificate proofs](finite-horizon-certificates.tex) · [Response to r29](RESPONSE_TO_REFEREE.md) · [Resource conventions](RESOURCE_LEDGER.md)

## Mathematical extension

A finite Gram recursion equals the sum of squared residuals over every seed, word and query. Exact zero certifies all numerical responses; a backward recursion extracts a failed word otherwise. The finite displayed-horizon exact-feasibility problem has a polynomial-size existential-real formula, with stochastic and bounded-decoder constraints imposed explicitly.

Globally optimized even residual moments converge to the actual minimum worst-word error at a specified state profile, with `ell_p <= E <= Q^(1/p) ell_p`. A second, rational-grid construction gives `max(0,e_L-C/L) <= E <= e_L` without adding boundary labels. These bounds concern the actual global error rather than a sum of local defects. They do not provide polynomial-time general minimization or an exact rational optimizer at the boundary.

A four-seed planar example has exact errors `rho/2`, `rho/4`, `0` at one, two and at least three bottleneck labels. A separately stated categorical-output comparison transfers the classical nonnegative-rank complexity and field distinction through explicit normalization; no such hardness is asserted for the fixed planar binary-query subclass.

## Readable source and local delivery

All LaTeX inputs are present in this directory. Compile `main.tex` three times with `pdflatex -interaction=nonstopmode -halt-on-error`. The standard AMS-compatible packages are declared in that file. Local PDF, complete rebuilding sources and locally executed verification receipts are supplied with the conversation. Their existence does not imply that a remote workflow succeeded.

All ten inherited mathematical/program modules are byte-identical to v44. New introductory, comparison and bibliography text distinguishes classical equivalence, tensor/Gram, elimination and nonnegative-factorization tools from the finite constrained certificate formulation. The complete v44 PDF and cumulative archives remain unchanged at their original repository paths and are preserved in the local archival delivery. No original mathematical theorem or historical pipeline is withdrawn. No independent A/B/C/D analytic gate, general arithmetic classification or editorial outcome is declared resolved.
