# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r6-operational-transfer-2026-10-07`  
**Reviewed exact branch head:** `86472b72b62184ac542e7ea82c354b2c293ef59e`  
**Reviewed branch root tree:** `ed8cec93e8cabf11abc0c88ab20f9aede90b7465`  
**Mathematical-source commit identified by the final receipt:** `e53a2aafd22bb2e9b8a95172c327da7a618dda00`  
**Build-source commit:** `56df65f55a507d996ef7dc385e4d6d057822ad21`  
**Verified artifact commit:** `f9785976f1ed8a4ce1bd69c20a6751ff2defeb62`  
**Final r6 directory tree:** `e449fa84cb6a83589e8b20831230825c19c2e050`  
**Native source tree recorded by the source audit:** `0b3839c841b02a173745d6d4fb3d997712ea9fe0`  
**Rendered PDF blob / SHA-256:** `7adad97131374b2743ea482263f99365a972f9be` / `7831e587f2d604e134b80bf5ef4f6faaffc7fd860d165e5b12625f6b95a2f3f8`  
**Predecessor external report:** r5 report blob `2caaec0003004c8526d46579d29444c8fd945ac1` on head `cdba4c08b250310ce54b527f3ae1b37f1ffd3d98`  
**Review branch:** `review/general-theta-restart-r6-operational-transfer-external-top4-referee-r6-2026-10-07`  
**Date:** 7 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof certificate, an independent priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not a technical-correctness rejection**. Revision r6 is a substantial mathematical advance over r5. It answers the principal structural criticism of the preceding report more seriously than a routine revision would: strict stability is now required only across a physical block, while the implemented encoder still rounds after every raw report; a fixed relation prevents intermediate rounding from destroying the positivity accumulated by a sparse product; the principal realization now permits state-dependent missingness and unbounded Gaussian likelihood ratios; adaptive termination receives a separate stopped Lyapunov estimate; and the causal-morphism formalism is now fully typed and accompanied by a measurable coupling construction.

In the load-bearing arguments I checked, I did not find an elementary gap invalidating:

- the continuous-instrument predictive-quotient proposition on its stated positive-density domain;
- the exact checkpoint projection and `M`-center formula;
- the block-shadow telescoping argument and its hard-label recursion;
- the relation-robust envelope induction;
- the stopped augmented-Lyapunov estimate;
- the mass-preserving simplex compander;
- the primitive sparse Gaussian block contraction and acquired-density lower bound;
- the completed-domain singular gain calculation and actual finite-depth law;
- the jointly measurable maximal-coupling construction;
- the stopped complete-law comparison; or
- the typed common-risk composition and reverse-certificate implication.

The negative top-four judgment concerns the **level and concentration of the advance**, not an identified fatal error. The central theorem remains a strong sufficient mechanism under a global static cover, a budget-independent relation, uniform all-pair block contraction under the physical law, and relation-robust drift for every adapted admissible perturbation. The sparse Gaussian application is considerably more natural than the r5 gated example, but it is still a tightly regularized known-kernel finite-state class and the matched lower is exposed through a specially designed indexed terminal probe and calibration alternative. The singular application remains an excellent sharpness construction rather than a theorem resolving a recognized natural singular-filtering problem. The paper does not yet give an intrinsic or near-necessary criterion, a broad converse to its stability hypotheses, a matched adaptive-acquisition theorem, or a genuine multi-resource optimal region.

For a strong specialist journal in probability, information theory, nonlinear filtering, stochastic control, quantization, or applied probability, my assessment is **favorable after a focused major revision**. At that level the block transfer theorem, the mass-preserving compander, the sparse Gaussian verification, the exact finite-acquisition singular law, and the stopped/morphism formalism form a coherent and potentially publishable contribution.

---

## 1. Review object, provenance, and pipeline inspected

The current referee-ready head is an evidence-only terminal commit. It records a mathematical-source commit, a later build-environment dependency fix, a hosted artifact commit, and final read-only provenance. I reviewed the exact r6 paper directory at the referee-ready head, not an unpinned working copy.

The inspection included:

- `main.tex`, all seven files under `sections/`, and `references.tex`;
- `README.md`, `REFEREE_RESPONSE.md`, `THEOREM_MAP.md`, `PROOF_LEDGER.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `PIPELINE_DERIVATION.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, `NOTATION_AUDIT.md`, and `PINNED_INPUTS.md`;
- `SOURCE_MANIFEST.json`, `verify.py`, `regression.py`, `build.py`, the committed build receipt, and the final read-only verification record;
- the canonical restart charter, general-foundations outline, realization registry, and `THEOREM_TARGETS.md`;
- the complete r5 external report and the r6 point-by-point response; and
- a targeted independent search for nearby belief-covering, finite-memory POMDP, finite-state-controller, recursive-filter-quantization, approximate-information-state, and zero-delay-coding results, including material published or posted through 2026.

The committed records report a twenty-two-page PDF, twenty-six native source files plus the manifest, nine active TeX inputs, nineteen formal statements, sixty-seven labels, seventy-five cross-references, seventeen bibliography entries, 27,027 finite regression checks per Python mode, eight negative controls, and two isolated rebuilds per environment. The scripts correctly distinguish source-integrity and finite sanity checks from mathematical proof. The final record also says that local and hosted PDF bytes differ across TeX environments while extracted page text and 72-dpi rendered pages agree; this is the appropriate level of reproducibility claim.

I inspected the verification and regression programs themselves. Their checks are relevant to source binding, labels, references, compander arithmetic, singular gain constants, stopped-drift algebra, and selected counterexamples. They are not a substitute for the continuum arguments, and neither the manuscript nor the receipts claim otherwise.

I did not independently re-audit every proof in the frozen v1–v96 archive, every historical referee report, or every realization branch. Preservation of those trees is provenance, not mathematical certification. I also did not treat the successful hosted workflow as evidence of theorem correctness.

The branch search confirms that r6 is the latest `referee-ready/general-theta-restart-*` revision currently present; there is no later r7 referee-ready branch at the time of this review.

---

## 2. Executive assessment of revision r6

Revision r6 is the strongest restart manuscript to date. Its central implication is now, schematically,

```text
prepared raw experiment and executable tests
        +
measurable predictive quotient or direct predictive realization
        +
static relation-preserving M-cover
        +
physical-law all-pair contraction over a raw block
        +
relation-robust candidate drift and within-block moments
        +
charged seed and readout interfaces
        =>
M-label recursion rounded after every physical report
        +
uniform deterministic-time online-risk upper
        +
actual-acquired-law checkpoint converse.
```

This is a genuine theorem, not merely a repackaging of a supplied recursive encoder. The exact block shadow is used only in the proof. Every local rounding insertion is propagated by the pathwise Lipschitz gains. The retained machine stores only a current finite label.

The new obstruction and its resolution are mathematically meaningful. A sparse product may become strictly positive even when each microstep has contraction coefficient one, but ordinary inward rounding can delete a coordinate needed by the future product. The paper therefore separates projective inwardness from componentwise mass preservation. The fixed relation

```text
D(rho) <= D(pi),      rho_i >= pi_i/n
```

is budget independent, is preserved by the compander, and is strong enough to rebuild a positive coordinate floor on a good report block. That mechanism is the clearest new idea in r6.

The sparse Gaussian realization is also materially better than r5's exogenous mixing gate. Missingness is state dependent and therefore informative; the transition matrices may vary with report-adapted actions; one-step projective contraction may fail completely; Gaussian likelihood ratios are unbounded; and the lower bound is derived from an actual positive-probability report block by an explicit Jacobian calculation.

The stopped theorem and the typed morphism section resolve important formal weaknesses of r5. In particular, the manuscript no longer substitutes a random time into a deterministic-time estimate, and it no longer leaves the simulator, clock, strategy lift, stopped task, and complete defect primarily at prose level.

Nevertheless, the top-four issue identified in r5 has not disappeared; it has moved. The paper now has a stronger sufficient theorem and a more natural realization, but it still does not provide an intrinsic theory of when acquired checkpoint geometry is recursively realizable at the same memory order. Nor does it derive a major consequence for a widely studied difficult filtering, control, or coding problem whose answer was previously unknown. The breadth of the title and foundational framing therefore remains larger than the demonstrated mathematical reach.

---

## 3. Response to the r5 report

| r5 issue | r6 assessment |
|---|---|
| Strict one-step all-pair contraction was too restrictive | **Substantially resolved.** Strict contraction is required only over a block; every microstep may be merely nonexpansive, while the encoder still rounds at every raw call. |
| An inward cover could destroy sparse-product positivity | **Resolved in the new mechanism.** A budget-independent relation preserves both projective spread and coordinate mass; the Gaussian compander verifies it explicitly. |
| The filtering example relied on an exogenous gate / exact-hold structure | **Substantially improved.** The new missing report is state dependent and updates the posterior; primitive sparse transitions create contraction only after a report block. |
| Adaptive stopping was outside the theorem | **Partially resolved.** A bounded stopped upper with an occupation/selection cost is proved. Matching arbitrary-stop laws remain open. |
| The morphism formalism was too compressed | **Resolved to a publishable level of formalization.** Transcript spaces, transducer state, strategy lift, clocks, stopping, common task, uniform defect, and resource registers are typed. |
| Jointly measurable maximal coupling needed proof or citation | **Resolved.** A constructive kernel proof is supplied on standard Borel spaces. |
| Condition numbers and finite implementation needed clearer treatment | **Improved substantially.** The condition-number table, interval compander, clipping defect, and separated resource ledger are useful. A complete finite-bit theorem is still absent. |
| Closest theorem-level literature comparison was too narrow | **Improved but not fully resolved.** The cited AIS, finite-window, zero-delay, and recursive-quantization comparisons are useful, but reachable-belief covering, adaptive belief discretization, recent belief-metric covering, and finite-state-controller lines remain missing. |
| A natural hard application or intrinsic characterization was needed for a top-four case | **Not resolved.** The sparse Gaussian application is more natural, but it remains a regularized known-kernel class and does not replace an intrinsic criterion or a major natural-problem theorem. |
| A matched multi-resource region was absent | **Not resolved.** `MRDQ`, workspace, program length, time, and defect are carefully accounted for, but most remain constructive upper coordinates rather than jointly matched intrinsic lower coordinates. |

Revision r6 is therefore not cosmetic. It resolves most of the specialist-publication objections in the prior report. The remaining top-four objection is narrower but still decisive.

---

## 4. Predictive object and quotient

### 4.1 Prepared experiment and strategy model

The paper begins from standard-Borel hidden, action, report, and resource spaces; positive normalized joint kernels; visible-history strategies; and explicit stopping and continuation interfaces. Failures and missing observations are represented as reports rather than silently conditioned away. The distinction between a fixed-prior posterior and a parameter-uniform sufficient statistic is correctly maintained.

The persistent-label model is also materially precise: no observation tape can be reread, no exact posterior is free, public clocks must be declared, controller state is charged separately, and randomized updates do not gain an unbounded data-dependent seed.

### 4.2 Continuous-instrument quotient

Proposition `prop:quotient` is a sufficient measurable-realization theorem. A countable dense family of continuous test evaluations embeds the compact belief domain into a compact metrizable product image. Equal fibers have equal report densities because the constant function belongs to the test space. Positive-density instrument evaluations then show that normalized updates agree on fibers. The use of a perfect quotient map and its product with the report identity is appropriate, and the measurable factorization through a standard-Borel statistic is performed coordinatewise rather than through an unspecified set-theoretic quotient.

I found the proof coherent under its stated assumptions. The manuscript correctly does not normalize at a null report and says that a jointly Borel null-report extension is extra data.

The conceptual limitation should remain prominent: this proposition does not construct the test space, prove compactness for arbitrary experiments, or solve all version problems. It is a convenient sufficient certificate, and applications may instead verify their predictive state directly.

### 4.3 Technical clarification requested

The phrase “compatible with that past” later used in the block theorem should be tied back to a formally named candidate domain or interface fiber. In applications the time, action availability, and any public phase variable accompany the posterior. The general statement should say explicitly whether `S` already includes these coordinates or whether the hypotheses are imposed fiberwise over them.

---

## 5. Audit of the block acquired-geometry theorem

### 5.1 Static cover and admissibility relation

The theorem assumes finite Borel cells and representatives with

```text
c_i in D(v),      d(v,c_i) <= r_M w(v).
```

The relation is fixed independently of the label budget. This is an important structural choice: the theorem does not hide the desired recursive error bound inside an `M`-dependent admissibility definition.

The cover is genuinely static. The online machine is later constructed by applying the physical candidate update and then taking the first covering cell. No recursive machine is part of the cover hypothesis.

### 5.2 Exact block comparison

The block-pair condition compares the true state and an arbitrary candidate under the same physical reports and the same report-driven actions. Individual maps need only be pathwise `L`-Lipschitz. Strict mean-square contraction appears only after `m` steps.

The quantifiers in the robust drift condition are stronger than the behavior of the eventual quantizer: they range over every adapted sequence of relation-preserving perturbations. This prevents circular verification of the theorem from the desired encoder itself.

### 5.3 Block shadow and accumulated rounding

Lemma `lem:block` is the load-bearing argument. At a block start, an exact shadow is initialized at the retained representative and is fed the same physical word. It is never stored by the implementation. Replacing rounding insertions from last to first gives

```text
d(exact shadow endpoint, retained endpoint)
 <= sum_j L^(m-j) local_error_j.
```

The candidate moment bound turns each local error into the common `L^2` radius `Delta`; Minkowski gives `Lambda_m Delta`; the physical-law block-pair inequality controls the true-to-shadow term. This yields

```text
e_{s+m} <= sqrt(kappa) e_s + Lambda_m Delta.
```

The within-block estimate follows by the same telescoping calculation without invoking strict block contraction.

I found no missing independence assumption here. The reports may depend on the true state and on previous report-driven actions; the proof uses the realized word and integrates under the physical law.

### 5.4 Envelope induction

Because first-cell selection respects the fixed relation, the robust endpoint drift applies directly to the retained trajectory. The definitions

```text
H   = max(H_0,b/(1-a)),
H_* = A H+B
```

give the endpoint and pre-rounding second-moment bounds. The theorem then closes the deterministic-time radius with the expected denominators `1-sqrt(kappa)` and `1-a` exposed.

### 5.5 Checkpoint identity and lower bound

The conditional-projection lemma is correct. Conditioning on the full history and independent algorithm randomization leaves the task conditional mean unchanged; label-conditional means remove decoder randomization; and a nearest-center selector gives

```text
R_cp(T,M)=B_T+q_M(nu_T).
```

The actual-submeasure lower is the standard union-of-balls argument, but it is stated at the correct level: the measure is a submeasure of the actual acquired score law, not a formal manifold volume or a latent reference law.

### 5.6 Scope of the theorem

The theorem is a strong sufficient principle, not an intrinsic characterization. Its main restrictions are:

1. a global static cover exists at every budget;
2. one fixed relation must be preserved at every microstep;
3. block contraction is uniform over all declared true/candidate pairs, not merely typical or locally coupled pairs;
4. robust drift must hold for every adapted admissible perturbation;
5. exploration is fixed independently of the prediction encoder; and
6. matching requires a separately verified actual small-ball witness on the same scale.

These restrictions are transparent and mathematically legitimate. They are also the main reason the result does not yet constitute a general classification of finite-memory predictability.

---

## 6. Audit of bounded adaptive termination

The stopped theorem does not make the invalid move of evaluating a deterministic-time estimate at a random index. It defines an augmented block Lyapunov function

```text
V_k = d(S_{km},hat S_{km})^2 + c rho^2 w(hat S_{km})^2
```

and chooses `bar kappa`, `gamma`, `c`, and `c_0` so that

```text
E[V_{k+1} | F_{km}] <= gamma V_k + c_0 rho^2.
```

The Young inequality coefficient and the domination of the envelope term are consistent. Multiplication by predictable continuation indicators and bounded optional summation give both the stopped terminal estimate and the occupation estimate. The passage from block-boundary stopping to an arbitrary raw stopping time uses within-block maxima and pays the expected number of entered blocks.

The first-success example is an appropriate warning: small error at every deterministic time does not control an observation-selected time.

The result should continue to be described as follows:

- it is a bounded-horizon upper;
- every stopped exploration must extend to a declared legal continuation on which the certificate holds;
- the expected block-count term is real and cannot be erased by deterministic-time uniformity;
- a stopping clock or public terminal interface changes the checkpoint information cut; and
- no matching arbitrary-stopping law is proved.

For publication, define `B_tau` and the stopped task map in the theorem statement rather than only by analogy with the deterministic case. A short corollary translating the error bound into a state-count/risk rate under an explicit bound on `E ceil(tau/m)` would also help readers see what the theorem yields.

---

## 7. Audit of the sparse Gaussian hidden-state realization

### 7.1 Model and predictive state

The hidden chain has `n=d+1` states. Every action selects a stochastic matrix with a fixed primitive support and a uniform lower bound on nonzero entries. A state-dependent missing probability produces an atom at `bot`; otherwise the report is Gaussian with common covariance and action-dependent means. Missingness is informative whenever the state probabilities differ, so it is correctly treated as a Bayes update rather than an exact hold.

The positive posterior, together with the time/action interface, determines every declared continuation. The indexed terminal Bernoulli probes separate its coordinates. This gives a direct predictive-state realization without invoking the abstract quotient theorem.

### 7.2 Mass-preserving compander

The deficit compander is a useful construction. Relative to a maximal coordinate, exponentiated deficits are rounded upward on a `K`-grid. Consequently the reconstructed deficits move inward, the projective error is bounded by

```text
C_{d,eta} M^{-1/d} exp(eta D(pi)),
```

and every reconstructed coordinate satisfies

```text
(Q_M pi)_i >= pi_i/n.
```

The count `n K^d`, the smallest-budget case, and the uniform seed are all handled. This lemma is not merely the old inward compander with different notation; the componentwise lower is the property needed by the block proof.

### 7.3 Exact block contraction

One-step posterior maps are nonexpansive in projective distance because right multiplication by a nonnegative matrix with no zero column is nonexpansive and multiplication by the common likelihood vector cancels in log ratios.

On a fixed report cube, every likelihood lies between uniform positive bounds. A block of `m` such reports has conditional probability bounded below without any independence assertion. The corresponding unnormalized product matrix has all entries in a common interval `[l,u]`, and its log-coordinate derivative contracts oscillation by at most `1-l/u`. Off that event the update is nonexpansive. This gives

```text
kappa = 1-p(1-chi^2) < 1.
```

The argument remains valid for report-adapted actions because only the common support and parameter bounds are used.

### 7.4 Robust candidate drift

The componentwise relation implies that each rounded posterior retains at least a fixed fraction of the pre-rounded coordinate. Iterating over a good primitive block therefore creates a uniform positive coordinate floor even though rounding occurs after every report. This is the decisive r6 step.

On the complement, posterior spread grows by a transition constant plus the oscillation of the log-likelihood vector. Gaussian exponential moments control the latter. Choosing a sufficiently small Lyapunov exponent converts the positive good-block probability into strict expected drift. The proof treats arbitrary adapted relation-preserving selections, so it verifies the general hypothesis rather than only the chosen quantizer.

### 7.5 Actual acquired lower

The lower retains the actual event that the final report block is observed and lies in the chosen cube. Conditional on the prefix, the final predictive weights have a uniform coordinate floor. Because the final action is selected before the final report, the map from that report to the first `d` posterior coordinates has log-ratio matrix `B_a` and Jacobian determinant

```text
|det B_a| product_{i=0}^d pi_i.
```

The report density upper and determinant lower give an explicit density upper for a positive submeasure of the actual score law. Small balls in the task norm then yield `q_M >= c M^{-2/d}`. No global smoothness of the posterior law is assumed.

The finite dyadic output cut and hidden sign alternative are combined with this memory lower in one indexed task. The cardinality calculation using

```text
min{M,(2^b+1)^d}
```

is correct.

### 7.6 Significance and limitations

This is a legitimate nonlinear-filtering theorem, but its present significance should not be overstated. The class has fixed finite hidden dimension, known kernels, a common Gaussian covariance, a fixed primitive support, a uniform lower bound on every nonzero transition, uniformly nondegenerate observation probabilities, and a determinant lower bound for every action used in the acquired-density argument. Constants may deteriorate extremely rapidly with block length, dimension, support floor, cube probability, likelihood range, and determinant.

The terminal task is deliberately designed to read posterior coordinates and to expose output/calibration cuts. That is mathematically valid, but the paper would be stronger if it also derived a consequence for a standard filtering loss, prediction problem, or control objective used independently in the literature. At present the application verifies the framework more convincingly than it resolves a pre-existing central problem.

The finite-input subsection is careful but remains a route rather than a complete theorem. On unbounded Gaussian reports it clips to a horizon-dependent box, charges the failure event, and uses interval arithmetic inside the box. This should not be advertised as a horizon-uniform finite-packet implementation unless the growth of the box, input alphabet, workspace, program constants, and resulting defect are stated together.

---

## 8. Audit of the singular finite-acquisition realization

### 8.1 Completed predictive domain

The completed Cantor domain contains both physical infinite tails and all finite-word fair-tail centers. This is necessary because a finite acquisition history produces a posterior center rather than a physical Cantor point. The manuscript consistently preserves this distinction.

First-difference estimates give deletion gain at most `30` and fixed-prefix gain at most `6·3^{-s}`. The two-mode metric with weights `(1800,1)` and a large cross-mode distance is a valid metric and supports a finite prefix cover of size `2^(h+2)-2`.

### 8.2 Gain matrix

For same-mode pairs, the full source-to-destination squared-gain matrix is

```text
[(1-alpha_t)85/128,  900 alpha_t]
[2/59049,             1/2          ].
```

Multiplication by the mode-weight vector gives a uniform factor `17/20`. The off-diagonal deletion term is load bearing; omitting it would change the theorem. Cross-mode pairs contract because a common reported operation places both candidates in the same destination mode.

I found the arithmetic and the completed-domain interpretation consistent.

### 8.3 Actual finite-depth law

The initial paid reads and subsequent reported operations leave a known finite prefix and a fair unrevealed tail. The acquired depth evolves by the displayed prepend/delete/copy recursion. Conditional on terminal mode and depth, the prefix is uniform. The resulting predictive score law is therefore the stated finite atomic mixture.

The unresolved tail variance is comparable to the square of the current cylinder scale. The online machine retains only a bounded current prefix and mode, never reconstructs deleted bits, and its center readout is the appropriate conditional mean. The physical-oracle Cantor law is used only as a lower witness; it is not substituted for the actual atomic law in the exact checkpoint formula.

The final profile

```text
delta^2 + E ell_{min(H_T,floor(log_2 M))}^2
```

is a genuine joint acquisition-memory-calibration law, uniform over the declared schedules and nonhomogeneous ratios.

### 8.4 Significance boundary

This is an elegant and sharp construction. It includes expanding deletion, nonreset transport, changing or vanishing mode masses, finite acquisition, singular scales, and actual atomic geometry. It satisfies the manuscript's internal singular-extension target.

It remains purpose built. The operation probabilities, prefix lengths, weights, and terminal score are selected so that a uniform gain matrix and an exact oracle witness are available. A theorem covering a recognized class of partially observed expanding or singular random dynamical systems would materially strengthen the general-mathematics case.

---

## 9. Coupling, report continuity, and causal morphisms

### 9.1 Jointly measurable maximal coupling

The coupling lemma constructs jointly measurable Radon–Nikodym versions by refining finite partitions of the standard-Borel report space. The common part is the pointwise minimum of the two densities; the residual measures are mutually singular; their product therefore puts no mass on the diagonal. This gives a measurable maximal-coupling kernel with disagreement probability equal to the manuscript's total-variation convention.

The proof is plausible and self-contained. A standard reference may still be useful, but the paper no longer depends on an uncited parameterized selection claim.

### 9.2 Stopped report-law comparison

Successive maximal couplings are used until the first report discrepancy. Before that time the controllers see the same transcript, choose the same actions, and make the same stopping decisions. Continuing a physical-law shadow after disagreement avoids conditioning the error process on coupling success. Summing first-discrepancy probabilities yields the stopped complete-law bound.

This is correctly a finite stopped comparison for the same declared controller class. It is not an infinite-transcript equivalence, a large-deviation transfer, or an optimized-control theorem.

### 9.3 Typed morphisms

Definition `def:morphism` now specifies:

- source and target parameter-indexed experiments;
- standard-Borel visible histories and legal actions;
- parameter-independent transducer kernels;
- a strategy lift;
- bounded physical completion times and compatible stopping;
- a common scored outcome and decision space;
- uniform complete stopped-law defect; and
- separate predictor, simulator, controller, clock, workspace, program, precision, call, and time resources.

The composition theorem follows by retaining the serial tuple, applying bounded-loss total-variation comparison, and using data processing and the triangle inequality. The reverse statement is correctly conditional on a reverse certificate and transfers lower bounds at an inflated budget.

The product `MRDQ` is only a constructive serial upper unless an executable challenge or reverse morphism proves necessity. The manuscript states this correctly and should preserve that distinction in every summary.

### 9.4 Editorial integration

The morphism section is mathematically sound but conceptually broad relative to the central block theorem. For a specialist submission, the author should decide whether it is an essential second half of the paper or a reusable formal appendix. At present the paper moves from a sharp finite-memory theorem into a general comparison formalism whose strongest lower implications require extra certificates not supplied for the main Gaussian application. The connection is real, but the narrative can be tightened.

---

## 10. Literature positioning and novelty

The current comparison with predictive-state representations, Blackwell–Le Cam comparison, recursive filter quantization, approximate information states, finite-window POMDP control, zero-delay Markov coding, and nonanticipative rate distortion is useful. The manuscript correctly disclaims novelty for conditional projection, quantization, Gaussian Bayes algebra, projective nonexpansiveness, maximal coupling, and total-variation contraction.

The closest novelty claim is the combination of:

1. a static budget-dependent cover preserving a fixed budget-independent relation;
2. strict stability only after a physical block;
3. rounding after every raw report;
4. actual acquired-score geometry for a matching checkpoint converse; and
5. explicit causal resource interfaces.

I found no cited theorem that obviously contains this exact combination.

The literature map is nevertheless incomplete for a paper with this title and scope. At minimum, the revision should compare its object and conclusion with the following nearby lines:

- Z. Zhang, M. Littman, and X. Chen, “Covering Number as a Complexity Measure for POMDP Planning and Learning,” AAAI 2012;
- Z. Zhang, D. Hsu, and W. S. Lee, “Covering Number for Efficient Heuristic-based POMDP Planning,” ICML 2014;
- D. Grover and C. Dimitrakakis, “Adaptive Belief Discretization for POMDP Planning,” arXiv:2104.07276;
- R. Andriushchenko, M. Češka, S. Junges, and J.-P. Katoen, “Inductive Synthesis of Finite-State Controllers for POMDPs,” UAI 2022;
- A. Anjarlekar, R. Etesami, and R. Srikant, “Scalable Policy-Based RL Algorithms for POMDPs,” arXiv:2510.06540;
- Y. Zhu and Y. Lu, “A Covering Framework for Offline POMDPs Learning Using Belief Space Metric,” AISTATS 2026; and
- D. Hudák et al., “Finite-State Controllers for (Hidden-Model) POMDPs using Deep Reinforcement Learning,” arXiv:2602.08734.

These works have different goals. They generally study planning, learning, reachable-belief covering, finite windows, or synthesized controllers; they do not appear to provide the manuscript's actual-score small-ball converse or its relation-preserving block recursion. Precisely because the differences are substantive, they should be stated theorem by theorem rather than left outside the comparison.

The paper should also explain how “acquired geometry” differs from the reachable-belief covering numbers already used as POMDP complexity measures. The manuscript's actual law and task pushforward are more probabilistic and task specific than a reachable-set cover; that distinction is potentially important and deserves a direct comparison.

An exhaustive priority determination is beyond this report. The independent search did not reveal a direct duplicate, but it did reveal a broader adjacent literature than the current seventeen-item bibliography suggests.

---

## 11. Assessment against the controlling targets F1–F4

### F1 — Causal acquired-geometry transfer

**Achieved as a substantial sufficient theorem.**

The theorem starts at the raw experiment, constructs a legal hard-label recursion, proves deterministic-time online control, and uses actual acquired mass for the checkpoint lower. The r5 one-step restriction is genuinely relaxed.

The qualification is important: no necessary, near-necessary, dual, or classification theorem is proved.

### F2 — Resource–resolution–risk composition

**Partially achieved.**

Acquisition uncertainty, persistent labels, output precision, and calibration are matched in the two realizations. Numerical and readout errors enter one root task norm. Complete-law defect enters bounded risk through a typed morphism. Reverse certificates and interface challenges can transfer selected lower bounds.

There is still no matched optimal region for the full vector of raw calls, predictor states, simulator states, controller states, clock states, workspace, program description, arithmetic time, input precision, and deficiency. Most coordinates beyond the predictor label remain upper accounts.

### F3 — Singular or nonuniform extension

**Achieved in a meaningful explicit class.**

The singular theorem has nonhomogeneous scales, finite atomic acquisition, expanding deletion, nonreset transport, changing mode masses, and no invariant-reference shortcut. The Gaussian theorem adds genuine block-only contraction and state-dependent missingness.

A broader natural singular or nonuniformly stable class remains open.

### F4 — Distinct realizations

**Achieved.**

The sparse Gaussian hidden-state experiment and the finite-read Cantor experiment are genuinely different raw-kernel verifications. Neither is used to prove the general theorem.

---

## 12. Major revisions required before specialist-journal publication

### 12.1 State the exact novelty and status before the broad motivation

The introduction should give a compact theorem-level statement such as:

> A fixed relation preserved by a static finite cover, together with physical-law all-pair block contraction and relation-robust drift, is sufficient to construct an `M`-state causal predictor rounded after every report; actual acquired small-ball mass yields the matching checkpoint lower.

It should immediately add that this is not a necessary-and-sufficient characterization.

### 12.2 Expand the closest literature comparison

Add a theorem-level comparison with reachable-belief covering, adaptive belief discretization, recent belief-metric covering, and finite-state-controller synthesis/extraction. Distinguish:

- reachable set versus actual acquired law;
- planning value versus a fixed prediction task;
- finite window versus finite persistent state;
- adaptive/nonuniform belief discretization versus a static relation-preserving cover;
- synthesized controller memory versus predictor-label memory; and
- approximation upper bounds versus actual-law lower bounds.

### 12.3 Explain the conceptual status of the admissibility relation

The relation is the main new mechanism, but the manuscript currently presents it mostly as a sufficient device verified in one simplex class. The paper should discuss:

- when relation-preserving covers exist;
- whether the relation can be generated from an order, cone, minorization, or regeneration certificate;
- how restrictive the quantification over all adapted admissible perturbations is;
- examples where block contraction holds but no useful relation-preserving cover exists; and
- whether a weaker local or probabilistic relation would suffice.

Without such discussion, the theorem risks appearing as a well-designed verification template rather than a broadly transportable principle.

### 12.4 Add a consequence for a standard task

The indexed posterior-coordinate probe is legitimate, but it is tailored to make the predictive geometry visible. Add a corollary for a standard filtering or prediction loss, or explain precisely why the probe formulation is the correct universal reduction. A natural control or coding consequence would materially improve impact.

### 12.5 Separate exact Borel implementation from finite-bit implementation

The exact theorem gives a finite retained alphabet but permits exact report access, exact known constants, Borel cell membership, and real arithmetic. The finite-input subsection gives an important enclosure route, yet it does not state one closed theorem bounding input alphabet, workspace, program length, runtime, clipping probability, and risk defect together. The abstract and introduction should not blur these two levels.

### 12.6 Clarify all uniformity quantifiers

For the main theorem and Gaussian realization, state in one place whether constants are uniform over:

- deterministic horizon;
- report-adapted legal strategies;
- action sequences;
- initial predictive states;
- all candidate representatives;
- fixed dimension;
- fixed support pattern and primitive length;
- fixed transition, missingness, mean, variance, and determinant bounds; and
- numerical implementations preserving the same relation.

### 12.7 Sharpen the stopped result's interface statement

Define the stopped baseline, task, and label/clock cut in the theorem. Give a corollary under an explicit stopping-cost assumption. Preserve the statement that deterministic-time matching does not imply stopped matching.

### 12.8 Tighten the role of the morphism section

Either integrate the morphism theorem into a concrete transfer corollary for the two realizations or move some general formalism to an appendix/supplement. The current formalism is correct but broader than what is used to obtain the main matched rates.

### 12.9 Reconsider the title and “Theta” terminology

The word “Theta” is not a standard mathematical object defined by the paper, and “Foundations” creates an expectation of an intrinsic classification. The author should either define the umbrella term and explain its mathematical necessity or adopt a narrower title centered on block-stable finite-memory prediction and acquired geometry.

### 12.10 Preserve the provenance caveats

The clean build, manifests, receipts, and regression controls are valuable. Continue to say explicitly that they certify source identity and selected finite calculations, not theorems or the entire repository.

---

## 13. Technical and expository comments

1. In Proposition `prop:quotient`, identify the topology on the positive-density update domain in the statement and repeat that a common null-report version is extra data.

2. Define the vector-valued interpretation of `q_M(nu_T)` for an independently selected probe index at the first occurrence, rather than relying on the weighted-norm sentence alone.

3. In Theorem `thm:main`, replace “compatible with that past” by a named measurable fiber or an explicit condition on the included interface coordinates.

4. State whether the static codebook is literally time independent or may be indexed by a publicly charged finite phase. The proof uses one fixed domain/codebook notation.

5. The theorem allows numerical error `u` only when the implementation remains inside the fixed relation. Repeat this next to every later use of generic “rounding error.”

6. In the block-pair condition, remind the reader that future actions are functions of the physical transcript, not of the candidate shadow.

7. In the stopped theorem, define the case `tau=0` and the stopped Bayes baseline explicitly in the statement.

8. In the Gaussian model, move the finiteness of the action set, if required, into the formal assumptions of Theorem `thm:hmm`.

9. State explicitly that `P^m>0` is entrywise positivity of the support product and that every realized supported product inherits a lower entry bound.

10. In the good-block argument, display the conditional iteration proving probability at least `p_0^m`; this will prevent readers from misreading it as independence.

11. In the robust-drift proof, isolate the concavity inequality used to pass from the `eta_0` exponential moment to the smaller exponent `eta`.

12. In the acquired-density proof, retain the statement that the last action is chosen before the final report. This is essential for the fixed Jacobian matrix.

13. Give the softmax-Jacobian determinant identity as a short lemma or one-line derivation.

14. In the output-grid lower, specify that one retained label plus the public probe index determines one vector in the Cartesian output grid.

15. For the digital Gaussian interface, state how `U` must grow with the horizon to keep the clipping defect at the same order as `M^{-2/d}`.

16. In the singular section, state the admissibility relation explicitly when `w=1`; the proof appears to use the full completed domain.

17. In the singular converse, keep the selected-mode submeasure mass in the union-of-balls calculation rather than switching informally between conditional and unconditional masses.

18. In Proposition `prop:report`, say whether preparation-report discrepancy is included as a time-zero term or assumed absent.

19. The maximal-coupling lemma should mention that nested finite partitions can be generated by a countable separating algebra on a standard-Borel space.

20. In Theorem `thm:morphism`, repeat that the target and source baselines are not separately subtracted unless the common-task certificate identifies them.

21. The notation `D` is used for projective spread, the calligraphic relation, and controller cardinality. The audit explains this, but one of these symbols should be changed in the article itself.

22. The abstract is dense. It should separate the general theorem, Gaussian realization, singular realization, and stopped/morphism additions into shorter sentences and state the sufficient-class status explicitly.

23. The bibliography should add the missing belief-covering and finite-controller works and use final published versions when available.

24. The paper should avoid treating the number of regression checks as evidence in any mathematical significance discussion; the current receipts already observe this boundary.

---

## 14. What would materially change the top-four assessment

More polishing, more finite regression checks, or a third certificate-designed example would not by itself change the recommendation. A top-four case would require an advance of a different order, for example:

1. **An intrinsic criterion:** a necessary-and-sufficient, near-necessary, dual, or minimax characterization of when checkpoint geometry is recursively realizable with the same memory order.

2. **A broad obstruction theorem:** a converse showing that failure of an intrinsic stability/order/regeneration condition forces separation between online and checkpoint curves in a natural class.

3. **A natural difficult application:** a theorem resolving the finite-memory law of a recognized nonuniformly stable filter, partially observed expanding system, regime-switching nonlinear model, or singular observation problem not designed around the certificate.

4. **Adaptive experiment design:** matching acquisition-memory-risk bounds when actions, stopping, calibration, or model learning are optimized under a raw resource budget.

5. **A genuine multi-resource region:** one theorem with matched upper and lower bounds for several intrinsic resources beyond the persistent prediction alphabet and a selected output/calibration interface.

Any one of these could turn the present architecture into a result of broad general-mathematics significance.

---

## 15. Final evaluation

Revision r6 is a serious and successful response to the r5 report. Its block theorem contains a real new mechanism. The finite encoder is constructed rather than assumed; rounding occurs after every physical report; the proof shadow is not retained; sparse-product positivity is protected by a fixed mass relation; and actual acquired geometry supplies the converse. The Gaussian and singular realizations are mathematically distinct and carefully derived. The stopped theorem, coupling lemma, and typed morphism section substantially improve the operational completeness of the paper.

I found no elementary fatal error in the principal arguments checked. The source/provenance pipeline is unusually disciplined and accurately limits its claims.

The manuscript nevertheless remains below the exceptional threshold of the four leading general mathematics journals. Its main theorem is still a global sufficient criterion rather than an intrinsic theory. Its applications demonstrate the mechanism but do not yet settle a broadly recognized hard natural problem. Its full resource programme remains only partly matched, and its literature positioning is incomplete relative to the breadth of the title.

Accordingly:

**Top-four general-journal recommendation:** reject in the present form.  
**Reason:** insufficient intrinsic breadth, natural-problem impact, and concentration of novelty for that exceptional level; not an identified fatal correctness defect.  
**Specialist-journal outlook:** favorable after a focused major revision addressing the literature map, conceptual status of the admissibility relation, standard-task consequences, finite-bit implementation boundary, interface quantifiers, and title/scope framing.
