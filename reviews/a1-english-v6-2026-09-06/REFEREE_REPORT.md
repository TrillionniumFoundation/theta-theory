# Referee report — A1, English revision 6

**Manuscript:** *Sparse observation algebras and finite-horizon memory*  
**Author named in the submission:** Qian Qi  
**Review date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation:** **REJECT at the requested general-mathematics-journal level in its present form.**

This is an AI-assisted referee-style assessment requested by the repository owner, not a report commissioned by any named journal. Independent checking means fresh source examination and separately written diagnostics, not an independent human appointment or formal verification. The recommendation concerns this submission, not the viability of the research program.

## 1. Submission identity and the extent of this review

```
repository:       TrillionniumFoundation/theta-theory
revision branch:  revision/a1-english-v6-sparse-sensor-streaming-2026-09-06
submission SHA:   750a65ef62422e81307b4a61fd891ee42fa2639e
repository tree:  5ea8e5e75084aa71ce1ee1b16c3c1aaa157f20e1
principal source: papers/A1-english-v6/main.tex
review parent:    171a7e20470d7e83a5b6b614f60a3434fd3145d7
```

The submission was committed at 2026-09-06 01:02:08 UTC. Branch discovery and a repeat head lookup identified v6, rather than either v4 branch or v5. The report uses immutable source identities throughout. All section paths below are relative to `papers/A1-english-v6/`; theorem numbers refer to the freshly compiled 16-page principal manuscript, while labels are the controlling anchors.

I read the principal source, all seven sections and the bibliography; the response, proof ledger, README and source manifest; the author diagnostic program; and the relevant v5 referee assessment. All nine principal TeX files and the author test script were reconstructed locally from connector-returned text and independently matched to their Git blob hashes. The principal manuscript was freshly compiled. All 16 pages were rendered and examined in contact sheets; pages 6, 10 and 15 were additionally inspected at enlarged resolution. The final build had no unresolved references, undefined citations or overfull boxes; two underfull-box notices remained.

The author suite was freshly rerun: **101/101 checks**, including its one family of **1,057 positive mixed minors**. A separately written program, importing no author code, completed **108/108 checks**. These are different executions with different scopes, not 209 proofs. See [referee_checks.py](referee_checks.py), [INDEPENDENT_DIAGNOSTICS.json](INDEPENDENT_DIAGNOSTICS.json), [EXECUTION_REPORT.json](EXECUTION_REPORT.json) and [REVIEW_MANIFEST.json](REVIEW_MANIFEST.json).

This is not a fresh audit or compilation of the complete legacy companion or the eleven-paper program. The retained historical material is not implicitly approved. The claim-by-claim assessment covers all **15 principal result labels**, as well as the two operative definitions: [CLAIM_AUDIT.md](CLAIM_AUDIT.md).

## 2. Executive judgment

**V6 is a genuine mathematical advance over v5. Its central sparse transversality theorem is not merely the old saturated-polynomial calculation with new notation. Its finite-state construction really is online. Its collision-bit comparison now uses a common total-risk baseline.** Any review that simply repeats the opposite v5 objections would be inaccurate.

I found **no blocking counterexample or unfilled essential proof step** in the principal statements under their printed restrictions. In particular, the formula

\[
d_A(n,m)=\min\{n(|A|-1),|mA|-1\}
\]

has a substantive attainable-witness proof, not a generic-position assumption. The normalized derivative loses exactly one rank. The online quantizer does not secretly reread the exact prefix. The randomized-code lower bound retains failure evidence. The small-amplitude finite-state threshold has a valid finite-partition proof. These positive findings should not be disguised by the negative publication recommendation.

My objection is instead to the **strength of the contribution demonstrated at the requested level**. The manuscript now isolates an attractive exact theorem for positive one-parameter monomial experiments. Its principal new input is the explicitly attainable binomial product tangent, paired with classical strict moment positivity. The Hilbert-function examples, fixed-horizon quantization exponent, approximate dynamic programming and four-symbol risk enumeration are correct consequences, but they do not independently provide several additional major structural advances. Once those standard mechanisms are separated, the submission has not yet made a compelling case that this exact rank theorem, with its present consequences, constitutes an exceptional general-mathematics result.

This is not a claim that a short proof cannot be important, that the whole theorem is already in the literature, or that every paper must handle arbitrary factor spaces. I have not established an earlier theorem identical to Theorem 3.3. The significance judgment is necessarily a judgment. Here it is supported by the narrow form of the new structural input and by the absence of a quantitatively substantial consequence of the new sparse directions, rather than by an invented mathematical defect.

A new deduction in [TECHNICAL_NOTE.md](TECHNICAL_NOTE.md) makes the latter issue precise. With a fixed prior, five trials and a uniformly positive detector, an arbitrarily small change in an exponent changes the exact peak dimension from four to five. Nevertheless a four-dimensional-model code gives a uniform bound

\[
\mathcal R_{M,5}^{\theta}\le C\{M^{-1/2}+\theta^2\}.
\]

Thus the asymptotic dimension jump does not itself quantify the operational importance of the added direction, even without a long horizon or a vanishing positivity margin. This **does not contradict v6**, which correctly allows calibration-dependent constants. It identifies what an exact rank law leaves unresolved at finite resolution.

## 3. Disposition of the preceding referee requirements

| V5 item | V6 disposition | Present assessment |
|---|---|---|
| E1: go beyond saturated polynomial spaces | Arbitrary finite nonnegative real exponent sets; explicit binomial tangent and prior-independent mixed pairing | Substantively addressed. This is a class-wide theorem, not merely the reviewer's isolated sparse example. |
| E2: checkpoint coding is not sequential finite-state filtering | Reachable representatives; index-only updates after every report; accumulated quantization error; matching lower power in one prescribed exploration experiment | Addressed for the printed streaming prediction problem. The separate control statement is an upper bound only, as declared. |
| E3: rare probes undermine horizon-uniform useful-memory claims | Zero forecast bound retained explicitly; constants declared nonuniform | The overinterpretation is removed. A horizon-uniform theorem has not been proved and is not claimed. |
| E4: compare one target and one Bayes baseline at finite memory | Exact raw/erased partition risks for every state budget; positive four-state gain; smaller-budget threshold | Addressed in the explicitly separate uncensored two-cartridge experiment. |
| P1–P2: future-only policies and task memory | Definitions and summaries now separate old prefixes, independent seeds and payoff automata | Addressed. |
| P3: sharp exponent versus sharp constants | Distinction and conditioning limits stated in the principal text | Addressed. |
| P4–P5: stale review language and two different erasure operations | Stable attribution in the principal narrative; archival material distinguished; raw postprocessing separated from comparator intervention | Addressed in the principal text. |

These closures are real. They must not be reopened as if the additions did not exist. They also do not constitute a promise of acceptance: the resulting theorem and its consequences must now be evaluated on their own merits.

## 4. Mathematical audit of the central argument

### 4.1 Attainability and the future test space

**Anchors:** Lemma 2.1, Proposition 2.3; `sections/02_experiments.tex`, lines 19–99.

A surjective linear calibration map sends the interior of the rejection cube to a neighborhood of the constant half-failure function in `W_A`. The fixed right inverse proves that each displayed perturbation is realized by one command independent of the unknown parameter. The categorical realization is positive and normalized; it is appropriately not advertised as a mechanical derivation for every sparse exponent set.

Products of a spanning list of actually attainable failures span `W_A^m`. Conversely, each word of a fixed future feedback rule has a product likelihood in that space. Integrating an independent policy seed preserves the conclusion. This proves both directions of operational equivalence. The common rule cannot read distinct old prefixes or a prefix-dependent seed; Definition 2.2 now says so. No unconditional independence of trials is substituted for independence conditional on the shared parameter.

The result is about observable future laws. It does not remove a payoff automaton or cover arbitrary losses inspecting the hidden parameter. The manuscript now handles this boundary correctly.

### 4.2 The binomial tangent is the genuinely new step

**Anchors:** Lemmas 3.1–3.2; `sections/03_transversality.tex`, lines 5–88.

At distinct small positive `c_i`, the factors `(1+c_i t^D)/2` lie inside the actual command cube. Writing `z=t^D`, their complementary products `P_i(z)` form a basis through degree `n-1`, by evaluation at the distinct formal roots `-1/c_i`. Those evaluations are polynomial algebra, not forbidden negative physical parameter values.

Variations in the endpoint monomials give `1,z,...,z^n`; each interior exponent `a` contributes `t^a, t^a z,...,t^a z^(n-1)`. The exponent strings do not collide because `0<a<D`. Consequently the *whole* differential image, not just an included subspace, has `n(r-1)+1` independent monomials. This observation survives arbitrary real exponent gaps and is considerably better than the v5 saturated-space argument.

The mixed-moment lemma then applies to two different ordered exponent sets. Generalized Vandermonde positivity follows from exponential zero counting and the Wronskian sign; determinant integration gives a nonnegative integrand. Full support supplies positive mass on separated ordered intervals, hence strict positivity, even without a density. The possible endpoint zero is harmless by continuity. I found no reversal of determinant signs or illicit positive-density assumption.

These are clean proofs. The total-positivity mechanism is classical and acknowledged; the relevant contribution is finding an attainable product tangent to which it applies uniformly over the declared class.

### 4.3 Normalization, genericity and minimal encoding

**Anchors:** Theorems 3.3–3.4; `sections/03_transversality.tex`, lines 90–196.

Let `L` include the constant test, `Z=mu(P)>0`, and `p=L(P)/Z`. The derivative on the product tangent is

\[
Z^{-1}\{LQ-p\,e_0(LQ)\}.
\]

The vector `p` belongs to the image of `L` and has constant coordinate one. The second map therefore has kernel *exactly* its span on that image. This justifies losing exactly one dimension, rather than subtracting one from an unrelated ambient dimension.

Independent factor rescalings supply the past-side upper bound, and the number of future tests supplies the other bound. A maximal Jacobian minor nonzero at the witness has a nonzero polynomial numerator in command coordinates. The stated genericity follows. There is no assertion of uniform conditioning. The inverse-function construction uses a ball in selected output coordinates and a graph lift; it does not falsely place a flat ball in a curved prediction manifold.

For the lower continuous-encoding bound, sufficiency forces injectivity on that section. Invariance of domain gives the obstruction without requiring a continuous decoder. The upper encoding stores either normalized chronological factors or future moments. It is explicitly a history encoding and need not identify equivalent factorizations; the usual quotient-embedding objection consequently does not apply.

The one-switch causal realization is also valid. After the switch, the indices `s+a` required by the next Bayes update are in the old future sumset, and its denominator is bounded below by the report margin. Prior moments in `NA` suffice at the switch. These are genuine global upper states, not merely local charts.

### 4.4 Observation algebra: correct, but not a new Hilbert-function theory

**Anchors:** Proposition 4.1 and Corollary 4.2.

The three-generator kernel is the principal homogeneous binomial ideal printed in the paper. Equal-degree monomial collisions differ by integer multiples of the primitive relation; cancelling common monomials and using the difference-of-powers identity proves generation. The dimension subtraction yields the stated Hilbert function. Irrational ratios eliminate additive collisions. The example `A={0,2,5}` and its asymmetric profile are correct and properly attributed.

The identification of an iterated sumset cardinality with a graded Hilbert function is established mathematics, not a second new structural theorem of this submission; the author says this. Elias, Proposition 2.3 and the preceding construction, gives precisely this correspondence [L1]. What v6 adds is its attainable-past pairing with the future space. The distinction should remain central in any claim of novelty.

## 5. Sequential and finite-state results

### 5.1 The upper filter is genuinely online, within its resource model

**Anchors:** Definition 5.1, Lemma 5.2, Theorem 5.3.

Each representative is reachable. Applying an admitted input to it produces another reachable exact state, so the subsequent quantizer is used inside its domain. This avoids the familiar infeasible-moment problem. Positivity controls denominators on the line segments needed for the derivative bounds: interpolated normalized factors remain positive, and interpolated moment vectors represent posterior mixtures.

The error recurrence

\[
e_{n+1}\le L_n e_n+C M^{-1/D_A(N)}
\]

accounts for every preceding lossy update, including the factor-to-moment changeover. A finite horizon permits its iteration without any stability-in-time hypothesis. Squaring the Lipschitz prediction error gives the printed exponent. Calling this only checkpoint compression would now be wrong.

The resource is nevertheless an index between input symbols. The known clock, real-valued commands, exact calibration, finite program and temporary arithmetic are excluded from the charged resource. Representatives in nonempty compact-set cells are selected existentially. The paper explicitly disclaims effective synthesis and finite-precision implementation. Hence the result is an existence theorem for finite-state transducers with specified read-only real functions, not a Turing-space, circuit-size or executable finite-precision theorem. This is a scope boundary, not a hidden contradiction. The heading “constructive” is stronger than necessary unless this convention is repeated nearby.

### 5.2 The lower bound closes the sequential exponent, not general optimal-control complexity

**Anchor:** Theorem 5.4.

The exploration commands are fixed in distribution before selecting the filter. On the all-failure prefix, the joint command density contains the actual evidence, bounded below by `eta^n`. A local coordinate change in selected predictions and complementary command coordinates yields the required subprobability minorization. No exact real command is assigned positive point mass.

At the checkpoint every streaming filter is an `M`-message encoder. Conditional-mean forecasts leave at most `M` centers, and private encoder randomization cannot improve on the nearest center. The projected-ball volume bound gives `d rho^2/(d+2) M^(-2/d)`. Fixing fresh independent public randomness and averaging is legitimate. Retaining an old exploration seed would not be legitimate, and is expressly excluded.

This proves the matching exponent for the prescribed prediction experiment, with a streaming upper implementation. It does not prove the memory required by an optimal exploration policy or by all control objectives. The author no longer makes that inference. Classical approximate-information-state work already develops recursive state approximations and dynamic-programming loss transfer [L2]; it does not by itself prove this sparse dimension or this lower bound.

### 5.3 The additive-control upper bound is sound but is not a matching decision law

**Anchor:** Theorem 5.5.

Compactness and continuity give attained maximizing actions. Lipschitz continuity is needed in state, not differentiability of the optimizer or of the reward in the action. The reward is state-independent, so the printed hypothesis is adequate. Greedy actions at representatives and Bellman telescoping yield `C'_N M^(-1/D_A(N))`. There is no missing optimizer derivative.

The absence of a control lower bound is declared, not an error. It does mean that the two matching prediction powers must not be presented as a matched control-complexity result. Finite-window control under filter stability [L3] is a related but different regime; neither that literature nor the present fixed-horizon proof is a substitute for the other.

## 6. Common-risk collision-bit result

**Anchors:** Section 6, Theorem 6.1 and Corollary 6.2.

The short-time geometry counts every attempted ambient insertion. Disk separation and convexity justify at most one collision. The collision flux is `2TR/a`, and the four probabilities are positive and normalized under the stated bounds. The coefficient determinant is `4T^2 epsilon/a^3` in absolute value. The internal exact-coordinate detector is a declared apparatus idealization, not an unknown parameter handed to the controller; it is also not a proof of physical measurement complexity.

The new experiment genuinely compares one target `Y` and one total Bayes-risk baseline. With `p_x=mu k_x` and `z_x=mu(k_x h)`, conditional expectation gives

\[
R_M=\mu h-\max_{|\mathcal Q|\le M}\sum_{B\in\mathcal Q}z_B^2/p_B.
\]

Randomization can be removed by fixing forecasts, assigning each symbol to a best forecast, and reoptimizing block means. For three states exactly one raw pair need be merged, while the erased alphabet is lossless. This proves the stated pair-cost identity, and four states realize the full strictly positive gain.

The small-amplitude proof is not invalidated by equal sign means at amplitude zero. A split of equal means between distinct optimal centers would force a tie. Moving one sign and reoptimizing the vacated block strictly improves the risk; that block still contains an extreme tag. Equal centers merely give the suboptimal one-state risk. The finitely many strictly positive gaps then persist for small positive amplitude. Thus the exact zero gain for `M=1,2,3` is established, not only numerically suggested.

The author's physical interval calculation was freshly rerun and yields

\[
5.6376025880993289137312813786859719\,10^{-13}
<\Delta<
5.6376025880993289137312813786859720\,10^{-13}.
\]

This is the uniform-prior instance with `T=epsilon=1/20`; the enclosure uses the actual physical constants. It must not be described as a sizable practical advantage. More importantly for the synthesis, the finite-partition theorem depends on four weighted scalar means, not on the sparse product-tangent classification or a growing-horizon online state. It resolves the previous comparison objection, but does not by itself supply a quantitative consequence of the new algebraic directions.

## 7. Remaining major concerns at the requested level

### E1. The novelty claim must stand on the pairing theorem, not on the number of attached consequences

The strongest new ingredient is Lemma 3.2 coupled to Lemma 3.1 and the exact normalization step. That is an elegant, useful theorem. The other principal consequences follow from explicit bookkeeping, finite-dimensional compactness, elementary covering, dynamic programming and finite scalar partitions once this ingredient is available. The paper gives no new sumset-growth bound or inverse theorem, no new general quantization principle, and no new comparison-of-experiments principle. Its acknowledgments are appropriately candid.

My assessment is that the current presentation does not yet establish why the resulting pairing theorem changes a substantial mathematical problem outside the constructed experiment, or yields a comparably strong consequence within it. This is the primary publication objection. It is not a demand to enlarge the parameter space merely for its own sake, and it is not a claim that classical ingredients preclude original synthesis.

### E2. Rank classifies exact distinguishability, not resolved predictive directions

Section 5.1 correctly preserves the rare-probe bound and calibration-dependent constants. The issue is broader than rare probes. The accompanying technical note proves a five-trial, uniformly positive near-collision example: `A_theta={0,1,2+theta}` has peak dimension five for every small positive `theta`, while `A_0` has peak four. A base-model filter nevertheless has regret at most `C(M^(-1/2)+theta^2)` in all these experiments, under the same command and query labels.

As a consequence, any lower constant in a bound `c_theta M^(-2/5)` valid for every `M` must satisfy `c_theta <= C' theta^(2/5)`. This is an upper restriction on a possible constant, not its sharp asymptotic. The balancing scale of the two upper terms is not claimed to be an optimal crossover.

The paper's nonuniformity disclaimer already permits this. The deduction is therefore not an erratum request. It demonstrates precisely why cardinality of the future sumset alone does not yet deliver a robust finite-resolution memory explanation. Adding another exact exponent set will not resolve that distinction. A quantitative theorem, or a substantially consequential exact application, would change the assessment more than further dimension examples.

### E3. The two operational successes remain distinct

The streaming theorem uses a continuously randomized input experiment and a spanning rare-event query family. The common-risk theorem uses one finite raw observation and a different target, with finite partition optimization. Both are legitimate, and both now have correct resource accounting. They do not jointly prove that the new sparse information directions confer a nondegenerate finite-memory advantage in an evolving decision problem. The weaker additive-control upper bound does not fill that particular gap.

This is a limitation of the claimed synthesis, not a missing assumption in any printed theorem. A future submission need not solve every possible extension; it should make one compelling central contribution rather than rely on the accumulated breadth of separate correct statements.

## 8. Smaller corrections and reproducibility points

**P1. Update the published sumset reference.** Eliahou–Mazumdar is not only a 2020 preprint: the publication is *Journal of Algebra* 593 (2022), 274–294, DOI `10.1016/j.jalgebra.2021.11.019` [L4]. The existing preprint citation is identifiable, so this is bibliographic maintenance, not a priority violation.

**P2. Clarify “constructive.”** State next to Theorem 5.3 that the representatives and read-only transition functions are supplied existentially from the exact model. Do not imply a computable synthesis algorithm from finite-precision exponent or moment data. The body already provides the necessary caveat.

**P3. State measurability conventions once.** Explicitly take randomized continuation and transition rules to be Borel kernels on their stated domains. This is the natural interpretation of the probability calculations; it is a useful formal clarification rather than a discovered failure of a constructed rule.

**P4. Preserve the present distinction between a history encoding and a quotient chart.** The chronological-factor upper state may carry redundant factorization information. There is nothing wrong with that; removing the caveat would create an unnecessary global-topology claim.

**P5. Keep numerical tests in their correct role.** The author streaming fixture exercises actual index-only updates on a finite menu. It does not test the continuous-input asymptotic lower theorem. The independent sparse fixtures check exact changes of representation along several report words, not all possible online quantizers. Both test suites explicitly delimit their scope.

The organization and typesetting of the new principal text are materially improved. Relegating the unchanged historical proofs to a clearly marked companion is not an objectionable deletion. There is no need to restore stale review-relative prose to the principal narrative.

## 9. Literature checks and originality boundary

These are targeted primary-source comparisons, not an exhaustive priority search. None is asserted to contain the entire A1 theorem.

**[L1]** J. Elias, *Sumsets and projective curves*, arXiv:2202.00590v1, Section 2, especially Definition 2.2 and Proposition 2.3; published in *Mediterranean Journal of Mathematics* 19 (2022), article 177. The inspected primary HTML explicitly identifies the monomial algebra's degree components with sumsets. It supports the classical status of that ingredient, not a prior proof of attainable transversality. Primary text: `https://arxiv.org/html/2202.00590v1`.

**[L2]** J. Subramanian, A. Sinha, R. Seraj and A. Mahajan, *Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems*, JMLR 23(12) (2022), 1–83. The primary journal abstract describes recursively updated information states and approximate dynamic programs with policy-loss bounds. Primary record: `https://jmlr.org/papers/v23/20-1165.html`.

**[L3]** A. Kara and S. Yüksel, *Near Optimality of Finite Memory Feedback Policies in Partially Observed Markov Decision Processes*, JMLR 23(11) (2022), 1–46. The primary abstract concerns finite windows, finite action/observation sets and filter-stability bounds. It is not the present fixed-horizon, continuous-command rate theorem. Primary record: `https://jmlr.org/papers/v23/20-1152.html`.

**[L4]** S. Eliahou and E. Mazumdar, *Iterated sumsets and Hilbert functions*, arXiv:2006.08998v3; *Journal of Algebra* 593 (2022), 274–294. The preprint abstract and linked DOI were inspected; the published bibliographic data are also recorded in the same authors' primary AIF article, DOI `10.5802/aif.3674`, reference 3. Primary records: `https://arxiv.org/abs/2006.08998` and `https://aif.centre-mersenne.org/articles/10.5802/aif.3674/`.

Classical positivity and quantization are also acknowledged in the manuscript's Pinkus and Graf–Luschgy references. This review checks the actual printed positivity and covering arguments rather than invoking an unverified theorem number from either book. Correct attribution is a strength; it does not automatically settle the depth or significance of the new synthesis.

## 10. Final recommendation and what would change it

**Reject at the requested four-journal level in the present form.** The principal mathematics appears internally sound on this audit, and v6 resolves the substantial E1, E2 and E4 defects in the earlier synthesis. The rejection is not based on their continued absence, on a false formula, or on the desire to reject an AI-assisted manuscript.

A materially different assessment would require a stronger demonstration of the importance of the new attainable-pairing theorem. That could be a genuinely substantial exact consequence or a quantitative result connecting resolved predictive directions to constrained sequential decisions. These are alternatives, not a demand to solve every extension or append the technical note as another theorem and declare the review closed. A sharper exposition of an already present consequence could also matter; enlarging the archive or the test count alone would not.

The complete existing proof record should remain available. The present report provides concrete closed issues, a checked proof inventory, a new analytic stress test and reproducible finite evidence for the next round. It makes no impossibility claim about further development and no guarantee that an undiscovered mathematical error or earlier equivalent result does not exist.
