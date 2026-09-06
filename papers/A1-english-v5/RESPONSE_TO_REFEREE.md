# Response to the controlling A1 English v4 report

**Report:** `review/a1-english-v4-harsh-referee-2026-09-06`, commit `58796c768d14c280020d05916feb946db8fb25ab`.

**Reviewed source:** `e4b10bf7acebf38dbcfb466b3ee4cf30bb77b381`, `papers/A1-english-v4/`.

**Revision:** A1 English v5, `papers/A1-english-v5/`.

The report found no new blocking counterexample in the 22 principal claims under their printed assumptions, but rejected their claimed significance at the intended journal level. We have not treated “no blocking error found” as acceptance, nor answered the substantive objection by lowering the intended standard. The revision changes the mathematical center: a restricted attainable experiment now supports a sharp finite-horizon decision-state and finite-memory law, with a removal test that changes its exponent. The validated earlier mathematics is retained in full.

The R-identifiers below index this response; they are not invented referee finding numbers.

## R1. A list of valid additions is not a central mathematical contribution

The former main narrative treated attainable rank, policy existence, approximation and an adaptive numerical separation as four parallel additions. The new `thm:decision-main` states one linked result. Its proof chain is:

fixed finite calibration → open attainable factors → attainable posterior patch → exact future decision quotient → observable score metric → matching memory–regret bounds → same-protocol sign ablation.

The central files are `sections/12_calibrated_rank.tex` through `sections/15_mark_value.tex`. The new abstract and introduction explain this question directly. The broader positive filter, response and full control apparatus remain in the paper and are summarized by the retained closure statements in Appendix B.

This is a substantive replacement of the central argument, not a claim that additional theorem counts alone answer the editorial judgment. Whether the resulting connection merits the intended journals remains a matter for the next independent assessment.

## R2. Unrestricted gates and programmable readout make attainability too unconstrained

`thm:calibrated-rank` fixes T, epsilon and phase, fixes the detector firmware, releases only placement failure/no collision/positive collision bit/negative collision bit, and allows only four lookup acceptance probabilities. The controller sees neither the physical collision coordinate nor its radius, nor a continuous angular output. A single fixed internal threshold realizes the collision bit, so the central class does not need an arbitrary inverse-CDF programming choice.

The four physical probabilities are computed explicitly. Their coefficient matrix has determinant of absolute value 4 T² epsilon / a0³. The complete attainable failure set is exactly the image of the finite cube; its right inverse is a four-entry command independent of the unknown radius. This is a restricted interface, not a characterization of all imaginable instruments. The full Borel comparator theorem is retained as a separate broader apparatus result rather than silently deleted.

## R3. The qn state lower bound is about complete likelihoods, not finite decisions

`thm:decision-quotient` identifies the exact equivalence relation for m future cartridges after n observations. Common future feedback policies have degree-qm word probabilities. A finite set of actually executed all-failure probes spans those polynomials. Full support of the prior makes the polynomial Gram form definite, and the resulting linear map from the attainable degree-qn posterior patch has rank q min(n,m).

Both directions are proved. The upper bound represents every attainable history, while the lower bound uses a continuous local section to a positive-probability all-failure family. `thm:causal-horizon` provides the shrinking-moment update and the profile q min(n,N−n), including its changeover from polynomial coefficients. Past commands are not kept on an uncharged auxiliary tape.

This does **not** replace the qn full-likelihood theorem for arbitrary continuous G(R,d). The observable-future task and the latent-parameter loss class are distinguished explicitly. A stated polynomial terminal loss has its own sufficient degree bound; no lower bound is inferred merely from its nominal degree.

## R4. An exact continuous dimension does not establish approximate or finite-bit performance

`lem:score-metric` fixes an observable Brier-score experiment before compression. The independent query is revealed **after** the state is stored. It selects a nonadaptive sequence of m physical commands; only that sequence is executed, with all cartridges counted. Its excess risk is the squared Euclidean distance between probe forecasts divided by the finite menu size.

`thm:memory-rate` proves both bounds for all finite M-symbol codes, including discontinuous encoders, private randomization, and a fresh public seed independent of the entire past. A grid gives the upper bound. A volume lower bound on an attainable d-ball gives d/(d+2) times rho²/s times M^(−2/d), even for randomized codes. The lower-bound ball can be certified by a finite calibration/moment Jacobian and an explicit contraction estimate. `thm:continuous-regret` separately gives a positive lower regret threshold for k<d continuous real coordinates.

The memory resource is checkpoint history storage. The proof does not count immutable calibration/codebook data or global computation as free physical hardware. It does not assume that repeated lossy streaming updates inherit the single-checkpoint bound. Its constants are fixed-model constants, not uniform over vanishing amplitude, concentrated priors or growing horizons.

`thm:average-memory-rate` additionally fixes a single independent uniform-command exploration rule before the first cartridge. A submersion chart and the retained failure evidence give an unconditional uniform-ball minorization, hence the same matching expected-regret exponent. The same four-entry exploration law works before and after sign erasure. The old command-generation seed is charged; it is not fresh public coding randomness. A finite preselected command alphabet would have finitely many prefixes and a different eventual exact-code regime, which is expressly not confused with this continuous-command protocol.

## R5. The old adaptive witness survives the binary ablation unchanged

We agree with the report's exact binary reduction. The nominal optimizing policies use only no collision versus its complement, and their difference is an acceptance-cost saving. The old theorem is not rewritten as evidence that the mark or cubic state causes that gain. Its full Borel reduction, 64-pair table, exact inequalities, full-support transfer and lower bound greater than 11/10000 remain in `sections/11_adaptive_advantage.tex` without deletion. The appended mechanism paragraph makes this distinction explicit.

The replacement structural removal test uses the **same four-entry command convention, same 4^m query words, same prior, same score and same n+m cartridge budget** with and without the collision sign. The erased device averages its two collision command entries before comparison and does not release the sign. The attainable degree falls from three to two. Thus the exact decision dimension and the sharp finite-memory exponent change in the very same score protocol. A richer observation needing more memory is not presented as a loss of free-memory information value.

## R6. A genuine benefit should not be only a saved acceptance multiplier

`thm:zero-cost-gain` consumes two cartridges with g=1 in both experiments and no acceptance cost. After the first record the forecaster predicts whether the second placement fails. Retaining the first collision sign has exact gain

Delta_bit = (2 T mu1 / a0) (epsilon v / a0)^2 / [cbar(1−cbar)],

where v is the variance of R² under the first-hit posterior and cbar is the first-hit sign probability. Full support makes v positive. The gain vanishes when epsilon is zero. The proof optimizes over all measurable forecasts using conditional means; it is not a sampled-menu comparison. Its underlying comparison-of-experiments principle is classical and is credited. The new point is the same calibrated bit's explicit connection to the rank and memory laws, not a claim that conditional variance is new or that this narrow-interval gain must be numerically large.

## R7. The referee's rank-r extension includes common factors

`thm:rank-deficient` includes the n(r−1) result for a fixed r-dimensional factor space with an arbitrary common polynomial divisor. The proof removes the common divisor, selects exact-degree pairwise coprime factors by avoiding proper evaluation kernels, computes the multiplication differential, normalizes, and supplies the local section and continuous-state lower bound. Individually normalized factors give a matching representation. The rank-one case is explicit.

This extension and its argument are attributed to report Section 7. We do not claim it for arbitrary unions of mode-dependent factor spaces or count it as the independent answer to the report's significance objection.

## R8. Two collision arcs extend beyond the last cartridge

`thm:all-stage-arcs` incorporates report Section 8 with explicit attribution. An optimal failure-branch continuation is frozen; the accepted homogeneous continuation is convex in cos(y−theta), whereas the frozen failure term is affine. Pointwise endpoint selection gives at most two arcs and cannot reduce the already optimal value. Finite chronological integration of the previously selected Borel feedback proves the joint Borel construction. This avoids an unsupported measurable selection on an unspecified space of policies.

The original exact last-cartridge formula remains in the manuscript. Neither the extension nor the finite lookup theorem is described as a polynomial-time global controller synthesis result.

## R9. Robustness must preserve an experiment and respect its scope

The original normalized positive Bernstein surrogate, exact preservation of physical flag masses, common-history coupling, payoff-oscillation factor and two-policy regret comparison are retained. The same-degree finite calibration perturbation observation in the new memory section preserves the exponent only when positivity, normalization and rank persist. Nonpolynomial perturbations are covered by the older complete-policy bounds, not by an unjustified exact rank statement. No rare-history posterior or derivative robustness is inferred from small total variation alone.

## R10. Classical mechanisms, attribution and significance are different questions

The revised introduction distinguishes established predictive states, Bernstein arithmetic and mixtures, convex POMDP continuation, finite-code quantization, Borsuk–Ulam, comparison of experiments, flux and saltation from the new attainable finite-horizon calculation. Primary publication records for the added comparisons were checked. The finite-code exponent mechanism is not claimed as a new general quantization theorem; what is proved here is its exact attainable decision dimension and calibrated common-protocol realization.

The repository report's two extensions are explicitly credited. This revision does not certify exhaustive priority or journal acceptance.

## R11. Preserve the mathematics but separate the review diary

The revision descends from the exact review HEAD. Its entire reviewed v4 directory is additionally retained byte-for-byte as `retained-v4/`, including foundations, all mathematical source, tests, old receipts and the old prose. Ten current component source blobs containing the 20 inherited component statements are unchanged. The two closure overview labels remain in Appendix B. The stability formulas and proofs remain, while the historical validation narrative is not used as current mathematical evidence.

The branch/version response, proof ledger, source identities and validation status are in repository documents rather than the new main introduction. The original provenance appendix remains available in the retained directory; it has not been erased. No main, review or prior revision branch is overwritten, and no part of the eleven-paper historical program is claimed freshly verified by this focused revision.

## R12. Evidence and next referee obligations

The new finite diagnostics were executed: **50/50 passed**, with exact symbolic or rational arithmetic. They check calibration, finite probe spans, polynomial moment ranks, product differentials, causal moment identities, Brier identities, ball-volume constants, and an outward physical positive-gain enclosure. Some finite span tests use an explicitly labelled rational calibration proxy; they are not substituted for the physical determinant proof. The latest referee program was read, but neither its 39 checks nor inherited author counts are claimed as rerun.

These tests are not the proofs of the all-budget statements. The next referee should examine the operational-equivalence definition, the attainable local section, the no-side-information/randomization clauses, the quantitative ball, the lower-bound averaging argument, the causal changeover and the same-query erasure convention. Full-paper compilation, if performed, has a separate generated build receipt; no old PDF build is reported as a new one.
