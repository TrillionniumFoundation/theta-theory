# Response to the referee on A1 English v22

**Revised manuscript:** *Attainable information geometry in positive experiments*, Qian Qi, English v23.  
**Controlling report:** `reviews/a1-english-v22-harsh-independent-2026-09-07/REFEREE_REPORT.md`, commit `325e89b9c012830cbd219fec0cff7c52b8e8d321`.  
**Reviewed manuscript:** `papers/A1-english-v22/`, commit `5f745a863dac637496bd5eb20341f12cecb71ab1`.  
**Revision branch:** `revision/a1-english-v23-collision-spine-saturated-proof-2026-09-07`.  
**Date:** 7 September 2026.

We thank the referee for distinguishing the mathematical findings from the editorial judgment, and for identifying the saturated-geometry reduction. The revision addresses E22.1–E22.4 directly. The collision classification is the principal result; the algebra theorem is a separate, prior-uniform saturated application. Neither its hypotheses nor those of any inherited theorem have been weakened. All inherited theorem, lemma, proposition, corollary and proof blocks remain in the active article. An alternative proof has changed its narrative location, not its content.

The revision does not claim that an editorial decision follows from satisfying a finite list of requests. Its contribution argument is expressed in hypotheses, conclusions and proof obligations rather than theorem counts or a claim of generality unsupported by the theorems.

## E22.1 — Theorem-level contribution and indispensable proof spine

**Locations:** abstract; Introduction, subsection `sec:contribution-v23` ("What the classification determines"); principal Theorem `thm:resolution-main`; retained acquisition/collision and causal-transfer arguments.

The Introduction now states explicitly what the principal theorem determines for a fixed full-support prior, a fixed finite horizon and a compact strictly ordered one-step exponent chamber: a single two-sided operational error profile, uniform through additive collisions, with the volume products truncated at the dimension actually acquired from the past. The new subsection distinguishes three obligations: establishing which confluent prefixes are acquired with positive mass under one actual exploration law; covering the complete attainable image, not only a tangent patch or its affine hull; and implementing all checkpoint budgets with one causal retained-state filter in the physical prediction norm. A covering theorem alone supplies none of the first obligation or the experiment-specific causal verification, and a stability upper bound alone supplies no matching finite-label converse.

The concrete example with exponent alphabet `{0,1,3}`, one acquisition and two remaining observations has five nonconstant future coordinates but acquired dimension two. Away from collisions the resulting small-scale exponent is `M^(-1)`, rather than the `M^(-2/5)` obtained by treating the state as a full five-dimensional ellipsoid. This illustrates the role of the acquired-dimensional truncation without adding a differently named general theorem. The calculation is also checked in `tests/verify_v23.py`.

The classical covering, quantization and perturbation mechanisms are explicitly credited. In particular, accumulation of quantization errors in nonlinear filtering is not presented as a new principle. The novelty asserted for the principal result is the particular collision-uniform experiment-level classification and its acquisition geometry, not a new general metric-entropy inequality. The exact-kernel, inversion and implementation developments are retained with their own hypotheses; their presence is not counted as proof of the significance of the principal theorem. The article's mathematical reach is stated positively and precisely, without asserting an unproved unbounded-horizon or arbitrary-prior extension of the monomial result.

## E22.2 — Direct comparison with nonlinear-filter quantization

**Locations:** Appendix G, subsection `sec:filter-quantization-comparison`; new bibliography entries `PagesPham2005` and `PagesSagna2018`; `LITERATURE_VERIFICATION_V23.md`.

The comparison now includes Pagès–Pham (2005) and Pagès–Sagna (2018), rather than relying only on finite-window and approximate-information-state literature. We inspected the accessible Section 6, Theorem 6.3 and Remark 6.4 of the cited Pagès–Sagna preprint version. The Pagès–Pham publisher abstract and bibliographic record were accessible, but not the full publisher text; no claim of full-text inspection is made.

| Comparison | Explicit distinction in the revision |
|---|---|
| Compressed object | Quantized hidden-signal grids and a propagated conditional probability vector versus a codebook of complete predictive states. |
| Charged resource | A grid cardinality is not identified with the number of possible retained posterior labels. The latter is the resource charged here; a vector of real weights is not free persistent state. |
| Observation model | The cited filtering bounds concern discrete-time observations of a Markov signal under their printed regularity/integrability assumptions. The present applications specify positive controlled experiments and their physical query menus. |
| Error norm | Approximation of normalized conditional expectations of test functions is distinguished from excess prediction loss for the fixed physical menu. No inverse-covariance whitening is introduced. |
| Upper and lower bounds | Quantization/stability supplies an upper mechanism; the present two-sided law additionally uses an actual acquisition distribution to prove a converse for arbitrary finite-label codes. |
| Degeneration | The algebra law is uniform over priors and rank loss under bounded multiplication coefficients. The monomial collision law fixes its full-support prior. Neither uniformity is attributed to, or ruled out for, another theorem without a reduction. |

The discussion does not assert that the cited results already prove the present finite-label classification. Conversely, it does not ignore their much closer approximation mechanism. It identifies the resource and converse questions that would have to be resolved before such a reduction could be claimed.

## E22.3 — Saturated geometry and a direct proof

**Locations:** opening of `sections/algebra_multistep.tex`; Proposition `prop:algebra-saturation` and the direct proof in `sections/algebra_saturated_geometry.tex`; original transfer proof in Appendix D, subsection `sec:algebra-transfer-alternative`.

The finite observable quotient and immediate acquisition saturation are now visible before the algebra theorem. The added proposition proves the uniform sandwich

`m + Sigma(r B_d) subset S_n subset m + Sigma(R B_d)`

for every checkpoint `n >= 1`, with constants independent of the prior and the positive covariance eigenvalues. Consequently the relative dimension is exactly `rank(Sigma)`. On the finite observable quotient this rank is the number of positive-mass parts minus one. The indicator representation is used only for that qualitative statement; its possibly ill-conditioned coefficients do not enter any quantitative constant.

The theorem now has a complete direct proof at its principal location. It uses the existing bounded product chart, genuine acquisition mass and raw update, not semialgebraic covering machinery:

1. A rectangular grid covers the containing covariance ellipsoid. Centers are moved to reachable states in nonempty cells. The proof treats every integer budget, including `M = 1`, and the zero-rank case.
2. The actual, unconditional coefficient distribution dominates a fixed-volume component. Orthogonal rotation and projection give the lower bound for every positive covariance prefix. The command density and selected report-word probability remain included. Arbitrary codebook centers and independent coding randomness are allowed.
3. The physical menu gives the exact squared factor `2^(-2(N-n)) delta^2/(d+1)` multiplying raw-mean squared distance. The scales are covariance eigenvalues, not their square roots.
4. Reachable-state updates followed by reachable-codebook quantization give the error recurrence and its finite-horizon convolution. For the multistage converse the inequalities are applied to each fixed common filter before taking the outer infimum.

The former transfer-based proof is preserved byte-for-byte in the active Appendix D. The change therefore separates the elementary saturated covering step from the delicate collision/acquisition geometry, without discarding either argument or weakening the existing result. The new direct proof and saturation proposition are explanatory mathematical additions requested by the report, not a claim of a third unrelated major application.

## E22.4 — Local risk definitions and quantifier order

**Location:** Definition `def:algebra-risks`, immediately before the unchanged algebra theorem; equations `eq:algebra-local-loss`, `eq:algebra-risk-average`, `eq:algebra-risk-worst`, `eq:algebra-risk-causal-average`, and `eq:algebra-risk-causal-worst`.

The incorrect attribution of the risk infima to the finite-state resource definition is replaced by explicit formulas. The checkpoint average criterion is the infimum of expected physical loss under the one specified command-and-report exploration law. The checkpoint worst-history criterion is the infimum of the supremum over feasible histories, with coding randomness averaged. The causal criteria take the infimum over one common causal filter outside the maximum over checkpoints, with the complete budget vector fixed. The distinction between `inf_F max_n` and `max_n inf_F` is therefore part of the definition, not left to an inferred convention. The finite-state definition is cited only for the retained resource and randomization rules.

## Preservation, verification and limits

`build.py` verifies the pinned v22 source manifest (763 entries), checks the 755 inherited source files outside the eight declared revision files, and recursively compares the complete active TeX routes. It requires every one of the 129 inherited formal statements, 127 inherited proof blocks and 389 inherited labels to remain present. Original versions of the edited source files remain unchanged in the sibling v22 directory and in the parent commit. The alternative transfer proof is included in the compiled article, not merely stored in an unused archive.

`tests/verify_v23.py` supplies exact rational regression checks for covariance/support ranks, integer-budget covering estimates, physical scaling and the quantifier-order distinction. `validate.py` runs the inherited author suites and the new suite, compares normal and optimized runs for v22 and v23, tests rejection of an intentional inherited-proof mutation, and performs a complete three-pass build. The pinned v21 and v22 referee diagnostics are also rerun locally, normally and under optimization. Actual execution results are recorded in `validation/`, `BUILD_REPORT.json` and `PRESERVATION_REPORT.json`; the presence of a script alone is not represented as an executed check.

These source checks and finite computations do not prove the analytic density, covering or optimal-coding statements, do not constitute a formal proof certificate, and do not certify an editorial or priority judgment. The analytic arguments and their precise hypotheses remain in the manuscript for the next referee to examine.

### Publication execution note

The initial GitHub workflow run `34097210136` failed before any job step or runner was assigned; no cause is inferred from the empty job log. This is recorded as an unsuccessful CI attempt, not as a passed test or as a mathematical failure. The revision is published as readable source through direct Git data commits, with the complete local validation receipts. The PDF supplied with the referee package is the locally compiled 125-page v23 article. The compact source manifest expands against the pinned v22 manifest and checks the complete current source set, not only the edited files.
