# General Theta Foundations I — revision 28

**Robust Saddles, Causal Memory, and Validation Order**  
Qian Qi · 24 September 2026

This revision responds to both reviews of revision 27: the latest pipeline-aware r12 at `63f52685341e0121f5494c63768bf53999f3c6c5` and r11 at `ebd325871e0706d1346780b6c00503d9246b72dc`. The reviewed manuscript is frozen at `7a659e0a2a41cd91f1f6f4ddc3b01c50a77882e3`. The new work branch descends from r12. All predecessor manuscripts, their reports, and historical pipeline files retain their original paths and contents.

[Canonical English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to both reports](RESPONSE_TO_REFEREE.md) · [Theorem locations](evidence/THEOREM_LOCATIONS.json) · [Executed build receipt](evidence/BUILD_RECEIPT.json)

[Complete mathematical manuscript](complete-manuscript.pdf) · [Complete preserved development](complete-development.pdf) · [Reproducible source archive](evidence/SUBMISSION_SOURCES.zip)

## Principal results

The exact two-preparation saddle and minimum decision width five extend to a full-support target rectangle. Its diagonal marked masses are `(1+gamma)/4-kappa, (1-gamma)/4-kappa, (1-gamma)/4-kappa, (1+gamma)/4-kappa`, and all four other atoms have mass kappa. The parameter range is `6/25 <= gamma <= 13/50`, `0 <= kappa <= 1/1000`. The exact root, saddle value, response, global lower factorization and full posterior sign table are proved in `positive-noise-saddle.tex`.

The original Brownian collision target belongs to this family **exactly**, not just approximately: with conditional sensor-error probability e, write `mu1=E[e]`, `mu2=E[e^2]`. Then `gamma=1/4-mu1/2` and `kappa=(mu1-mu2)/2`. Conditional independence of the report windows is retained; unconditional independence is not assumed. Preparation reflection and independence of the center-of-mass mark justify the formula. Every original target with `9/10 <= d <= 11/10` and **`0 < sigma <= 1/24`** lies in the proved rectangle. Thus exact decision memory five holds on the entire original stated noise range, with an explicit saddle rather than an unevaluated compactness gap.

For every positive kappa in this rectangle, the exact minimum peak across **all twenty externally declared, internally order-preserving clocked validation interleavings** is twelve. Precisely the two serial orders attain twelve; every other order requires at least fourteen. The lower bounds cover stochastic encoders, frozen stochastic gates and event selection. They use actual future-output channels and avoid treating a random zero-mean output as deterministic zero. `facial-scheduling.tex` states the general contact-forced cut certificate used in this proof.

For the ideal target, the reverse serial order has exact peak ten. At any positive kappa it has exact peak twelve. This is a support-boundary discontinuity in exact memory, while the target law and the statistical value vary continuously. The ideal optimum over all twenty orders is not identified with the reverse-serial value ten. A report-dependent scheduler is also a different controlled interface: it is not included in the fixed-clock optimization.

For unknown target calibration and finite fair-bit sampling, `prop:physical-acquisition` gives explicit confidence, score-error, counter and coin-workspace bounds. The exact state numbers themselves use the article's known-target atomic stochastic-row convention; finite-bit exactness of an algebraic coin is not asserted.

## Reproduction

Use Python 3.11+, SymPy 1.14.0, PyMuPDF 1.26.7 and a LaTeX installation with AMS, Latin Modern, microtype, geometry, booktabs, mathtools and hyperref. From the repository root:

```sh
python papers/GTF-I-v28-causal-response/verify.py
python -O papers/GTF-I-v28-causal-response/verify.py
python papers/GTF-I-v28-causal-response/build.py
```

The assembly pins the v27 main Git blob to `7339ba992cb3c2bf14fead1e02938f52bb68eaea`. It verifies recovery of the preceding mathematical body and preserves all its modules. In the new copy of `saddle-realization.tex`, the elementary resource-loss identity is separated into a proposition; the contact/realization theorem and its proof remain. The split is reversibly checked. No old source is edited.

The build runs v28, v27, v26, v25 and v24 regressions in ordinary and optimized Python; executes negative controls in both modes; compiles three times; rejects undefined references and overfull boxes; and appends the unaltered predecessor volumes. Every appended page is compared for text identity, with representative raster comparisons. The source ZIP contains exact rebuild inputs and no standalone fonts. The workflow publishes native source first and records that exact source commit separately from its trigger and artifact commits.

## Reading and scope

The main new chain is `positive-noise-saddle.tex -> physical-noise-law.tex -> validation-order.tex`, with `facial-scheduling.tex` supplying the general simultaneous-realization certificate. The introductory theorem hierarchy distinguishes these results from the fully retained ideal, all-N, revelation, autonomous and transport developments.

The stable label `thm:all-clock-orders` fixes its scheduler quantifier. The parameter rectangle is an explicit symmetric full-support family, not an arbitrary ball in the seven-dimensional simplex. No sharp large-N expansion, all finite-N prior-support classification, optimal report-dependent scheduler, or closure of independent A2/B4/C2 gates is inferred. Executed checks support reproducibility; they do not constitute independent proof certification, priority clearance, or a journal decision.
