# Response to the English-v3 referee — A1 English revision 4.0

**Controlling report:** `reviews/a1-english-v3-2026-09-05/REFEREE_REPORT.md`, commit `574f2315a136d8b401644d8a3eeeb93c87887010`.  
**Reviewed manuscript:** `025a9b3fdfd9ffa86e6ae2924f8b5e5b1b58ddd6`.  
**New manuscript:** `papers/A1-english-v4/main.tex`, September 6, 2026.

We accept the two local scope corrections and the request for structural mathematical content beyond the coherent cubic example. The revision reorganizes the principal theorem around attainable rank, solved costly gates and a quantitative detector hierarchy. The mechanical preparation, positive likelihood, retained failures, exact state, attained control and fixed-controller response are preserved and rederived in the new main text. We do not treat the preceding report's positive findings as independent certification of the new results.

## M1 — Smooth trajectories do not make arbitrary Borel reports smooth

**Change:** Appendix A, Theorem A.3 (`thm:chamber-repair`).

The trajectory conclusion now concerns event times, one-sided states and terminal **states**. A report has the same regularity only for a specified jointly `C^r` reporting map with uniform bounds. The distributional assertion fixes the reporting manifold and Sobolev scale; use of an ambient embedding carries its ambient dimension in the Sobolev condition. The proof explicitly composes the smooth map after the finite-event argument.

The report's no-event threshold example is included and correctly excluded by the readout hypothesis. The transported/weighted preparation, integrable derivative-product envelopes and normalizer derivatives are retained. We do not “repair” the statement by restricting preparations to fixed measures alone.

## M2 — Five coordinates are not a universal intrinsic dimension

**Change:** Section 3, Lemma 3.1 and Remark 3.3 (`lem:body`, `rem:dimension`), main theorem and abstract.

The body is stated as a compact convex subset of `R^5`, with a five-coordinate representation. The constant-payoff/zero-reward example is explicitly displayed: the fifth integrand is a linear combination of the first four, so that instance lies in a four-dimensional hyperplane. This correction is separate from the genuinely sharp likelihood-state dimension theorem.

The optional interface clarification is also implemented: Theorem A.2 labels dotted bulk terms as Eulerian derivatives at fixed spatial position and includes the explicit external-boundary flux, zero at a fixed outer boundary. Both internal physical density traces remain present.

## E1 — Engineered cubic closure needs a structural or robust class theorem

**Changes:** Theorem 2.3 (`thm:rank`), Theorem 2.4 (`thm:amplification`), Theorems 5.1–5.2 (`thm:model-error`, `thm:hierarchy`).

We agree that the collision shell provides an exact internal radius measurement and that the cubic is chosen by the detector, not forced by billiard dynamics. This observation is used constructively. For a normalized polynomial channel, define the range `V` of integration against its raw likelihood and its coefficient rank `r`. Theorem 2.3 identifies the attainable relative interior, proves the iff criterion for full polynomial rank, supplies a Gram right inverse and an explicit interior radius, and gives a quantitative rank-persistence condition inside the fixed polynomial class. The product dimension is `n(r-1)`, not merely the full-rank substitution of `q` for `3`. The proof separates the Lipschitz/Hausdorff upper bound from a locally embedded coprime-factor lower stratum and the continuous-state obstruction.

The physical specialization quantifies a new contrast at the **same fixed mode**: passive likelihood dimension `n` versus selectable censoring dimension `3n`. Its explicit coefficient cube shows why the exact rank becomes ill-conditioned near zero amplitude; at zero amplitude the active/passive dimensions are `2n` and zero. No information increase by a fixed garbling is inferred.

Theorem 5.2 then addresses nonpolynomial detector changes rather than pretending rank persistence implies exact polynomial persistence. Bernstein mixtures of positive detector rows preserve normalization, positive margins and physical inverse-CDF realization. Placement/no-hit masses remain unchanged, all attempts remain counted, and common gates remain legal. Uniform complete-policy comparison yields explicit regret, degree and lookup-size bounds. The `C^2` refinement improves the degree rate from `m^{-1/2}` to `m^{-1}`. Continuous detectors without those constants still have a uniform-modulus convergence statement.

## E2 — Compare Bernstein arithmetic and beta representations accurately

**Change:** Appendix B.1 and bibliography; Theorem 2.3 separates the rank result from the coefficient algorithm.

Farouki–Rajan's Bernstein arithmetic and the Petrone–Wasserman Bernstein/beta connection are now explicit primary-source comparisons. Neither multiplication in Bernstein form nor the beta-mixture identity is claimed as the main invention. Moment-body geometry is also distinguished from the lift-zonoid background, and the expected-total-cost assumptions in Feinberg–Kasyanov–Zgurovsky are not substituted for our multiplicative criterion.

The submitted contribution is the attainable-family rank/conditioning analysis, physical passive/active comparison, solved costly control problem and quantitative realizable detector hierarchy. The comparison is targeted, not an assertion that an exhaustive priority search has proved every component unprecedented.

## E3 — Prove actual control structure and performance

**Changes:** Theorem 3.4, Theorem 4.1 and Proposition 4.2.

The endpoint result is incorporated first, with the referee's attribution preserved. The new final-cartridge problem has two continuous positive terminal payoffs and a genuine positive acceptance cost, represented by a multiplier `alpha < 1` on every accepted component. Its optimal collision gate is an explicitly solved circular arc; placement and no-hit components are selected as entire components. The integrated value is expressed using a closed positive-part cosine integral.

The remaining mode search is also solved: maximum detector amplitude, one of the two time endpoints, and phase rotation. Four candidate fallback-decision/time values, determined by eight posterior payoff moments, suffice. This does not require a gate grid or a numerical optimizer.

The example at `T=1/20`, `epsilon=1`, `alpha=999/1000` has optimal value approximately `1.02748308057`, compared with the best report-blind value approximately `1.02667640392`. Exact rational interval arithmetic proves the gap exceeds `8e-4`, not just that a floating estimate is positive. Convexity in a constant gate proves comparison against **every** report-blind gate, including randomized acceptance probabilities. A full-support prior perturbation retains a gap above `7e-4`. We state the comparator precisely: this is not described as a temporal adaptive advantage at a one-cartridge horizon.

## G1 — Credit and prove the referee-derived endpoint theorem

**Change:** Theorem 3.4 (`thm:endpoint`).

The positive homogeneous continuation functional is a supremum of linear functionals of an unnormalized parameter measure and hence convex. The accepted term is linear in the gate and the failed measure affine. Layer-cake decomposition, command continuity and right continuity of strict level sets prove every threshold below one is optimal for an optimal fractional gate. Thresholding the already selected Borel representative at `1/2` gives an optimal Borel endpoint feedback rule.

The proof explicitly credits the v3 report. It assumes no extra nonlinear gate cost or cross-command gate constraint. It does not assert finite acceptance-interval complexity for arbitrary horizons; that stronger boundary conclusion is proved for the specified costly last-stage problem only.

## S1 — Separate physical model change from coefficient roundoff

**Change:** Section 5, with arithmetic stability separately in Section 6.4.

The sine-amplitude perturbation is retained as a diagnostic: its fourth derivative is nonzero, so it has no exact cubic cutoff. We do not label it a counterexample to the original specified kernel. The raw total-variation formula is derived explicitly.

The referee's linear finite-budget comparison is credited. The new proof also records `1-(1-epsilon_0)^N` via coupled histories, the joint parameter/history version, and regret for an approximate-model policy with an added optimization error `tau`. The hierarchy then turns that comparison into actual degree and finite-table requirements for a positive class of physically implemented detectors. There is no uniform rare-history posterior claim.

## Earlier repairs and historical derivations retained

The biased objective remains `D(Q||P)-QB`, not bare entropy in the presence of a free retained bias. The moving-interface formula retains both density traces. Preparation weights, transports and normalization are differentiated explicitly. The ideal geometric record remains distinct from the regular positive detector; short cartridges are not represented as a long uninterrupted billiard orbit. Zero-evidence continuity is proved only for the probability-weighted continuation. All failed attempts are charged and all censoring is observed.

The complete principal v3 mathematical source and the latest report were read. Focused reuse of the companion hybrid and whole-preparation sections, the round-twelve historical audit, and the round-seventeen local exact primitive/pointer derivation is recorded with paths and blob identities. We do not import historical global quotient, conormal, spectral or CLT claims as unexamined proof inputs.

## Execution and what remains for independent review

The new local suite executed **17/17** diagnostics successfully. The separate exact rational certificate also ran successfully. Three no-shell-escape LaTeX passes produced a **25-page** PDF without undefined references/citations, missing characters or overfull boxes in the final log. Render inspection is recorded separately. We did not rerun the referee's v3 20-check suite or the preceding author's 39 checks, and do not count their historical PASS records as ours.

A developmental run of the rational script initially hit Python's large-integer string-conversion limit while serializing exact endpoints, after its mathematical assertions; the receipt now serializes outward-rounded rational endpoints on a `10^-24` grid. The complete final execution passed. An initial LaTeX overfull provenance line was corrected. Publication byte-identity checking also caught one local carriage-return escape in a TeX subscript; it was corrected and the suite and strict build rerun before final publication.

The general proofs and their mathematical significance are now submitted for the next referee assessment. Reproducibility receipts do not decide the requested journal standard. This revision responds by proving and exposing stronger positive results, not by withdrawing the operational objective or replacing it with a no-go statement.
