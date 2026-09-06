# Referee report — A1, English revision 9

**Manuscript:** *Sparse observation algebras and memory across exponent collisions*  
**Author named in the manuscript:** Qian Qi  
**Date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation:** **REJECT at the requested four-journal level in its present form.**

This is an owner-requested, AI-assisted external referee-style assessment. It is not a report commissioned by any named journal. The negative recommendation below concerns demonstrated mathematical significance at the requested destination. It is **not** a finding that the central rate is false, an assertion of an already published identical theorem, or a negative conclusion about the research program's feasibility.

## 1. Submission, scope, and evidence

```text
repository:       TrillionniumFoundation/theta-theory
revision branch:  revision/a1-english-v9-intrinsic-collision-geometry-2026-09-06
submission SHA:   e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5
submission tree:  c26e2f59760ac4c88f7a7e98d1a5e72e86ed98a3
principal path:   papers/A1-english-v9/
controlling v8
review SHA:       5f52bf456272b53bcb4df8d949effd2ab59bb79f
v8 submission:    5d3d7e04b172f98bddfd037c488d93d516d20a98
new review branch:
 review/a1-english-v9-harsh-referee-2026-09-06
```

The revision branch was checked again before this review branch was created and still pointed to the submission above. This review branch starts from that exact commit. The comparison from the controlling v8 review to the submission contains **25 added paths and no modified or deleted paths**. That repository comparison establishes preservation of pre-existing paths, not the truth or originality of their contents.

I read the new intrinsic theorem and its complete proof, its introduction and operational definitions, the inherited sparse-rank, confluent, attainable-covering, streaming, decision, and mechanical arguments, the response letter, and the controlling v8 report. The result-by-result disposition is in [CLAIM_AUDIT.md](CLAIM_AUDIT.md). References below use source labels, rather than result numbers inferred from an unexamined PDF. All principal source references are at the immutable submission SHA. The relevant source index is at the end of this report.

The independent program [referee_checks.py](referee_checks.py) was written and executed in this review without importing author code. It passed **3,821 exact assertions**, including **135 normalized-flag configurations**, **18 index-only streaming fixtures**, and **450 exact raw-update vector comparisons**. The count includes routine denominator and state-bound checks and should not be mistaken for 3,821 independent mathematical propositions. [INDEPENDENT_DIAGNOSTICS.json](INDEPENDENT_DIAGNOSTICS.json) records the actual run. [TECHNICAL_NOTE.md](TECHNICAL_NOTE.md) supplies an additional analytic comparison, not merely numerical evidence.

**Limits of this audit:** I did not execute the author's three test programs, rebuild the manuscript, download and inspect its standalone review archive, or inspect a newly rendered principal PDF. Author-supplied build counts and preservation hashes are therefore not independent executions in this report. Nor did I rereview every historical branch, every legacy companion, or all eleven planned papers. The mathematical assessment is a source review with targeted primary-literature checks and separately executed finite diagnostics. These limits are also recorded in [EXECUTION_REPORT.json](EXECUTION_REPORT.json).

## 2. Executive assessment

V9 is a genuine strengthening of v8. The paper no longer only follows a one-parameter affine collision with a predetermined list of jet orders. It gives a calibration-uniform formula on an arbitrary compact subset of the open one-step exponent chamber, permits intersecting additive-collision loci, and recovers pathwise phases from pairwise orders of contact. It supplies a two-parameter example with three distinct rank strata and arbitrarily high tangency order. Calling this an unchanged affine theorem with another example attached would be inaccurate.

**I did not identify a blocking counterexample or an essential unfilled step in the central proof under its printed hypotheses.** In particular, the repeated-node flag argument does not infer rank at a singular point from rank away from it; the upper bound covers the entire attainable image; and the online construction neither divides by an exponent gap nor rereads an exact prefix. The formulas for the two-parameter example survive independent exact checks.

My recommendation nevertheless remains negative at the specifically requested four-journal level. After making the closest classical comparison explicit, the incremental v9 argument consists of a finite Newton–Hermite extension of an existing transversality calculation, a finite-dimensional Vandermonde scale description, and reuse of the inherited bounded-format covering and raw-update mechanisms. The resulting classification is coherent and nontrivial. The manuscript has not, in my judgment, established why this classification has the exceptional mathematical importance or independently consequential reach necessary for the requested destination. Its larger parameter space does not by itself establish that importance.

This judgment separates three questions. **Correctness:** no central blocking defect found. **Priority:** no identical earlier theorem identified by this targeted search, but no exhaustive priority certificate. **Editorial significance:** not demonstrated sufficiently for the requested journals. A harsh review should be explicit about that separation rather than manufacture a false mathematical objection.

## 3. Disposition of the controlling v8 report

| V8 item | What v9 actually supplies | Disposition |
|---|---|---|
| E8.1: isolate the new assertion from the classical mechanisms | Arbitrary repeated-node Newton flags, intrinsic determinant profile, and an explicit classical-input discussion | The requested identification is supplied. Its strength is assessed anew in Section 7 below; this is not an allegation of missing attribution. |
| E8.2: broaden the theorem without obscuring resource quantifiers | An arbitrary compact calibration set, fixed positive full-rank coefficient matrix, known calibration, and one stage-compatible filter for each calibration and budget | A real enlargement of the stated class. The remaining fixed-experiment assumptions are explicit, not concealed defects. |
| E8.3: provide a structural consequence beyond another affine horizon | Pair-order tree allocation and the intersecting three-line arrangement with high-order tangent paths | Supplied. These consequences should receive credit even though their editorial force remains limited. |
| P8.1: explicit quantifier order | The introduction and intrinsic streaming theorem state uniform constants followed by calibration/budget-dependent existence | Closed. No calibration-blind codebook is asserted. |
| P8.2: pin bibliography versions | Zhang–Kileel v4 and the published Comte–Halupczok record are specified | Closed as a source-presentation request. Targeted inputs were checked as described below. |
| P8.3: put the final classification first | `thm:resolution-main` is the first named theorem in the introduction | Closed. Further narrative compression is a different, nonblocking matter. |
| P8.4: address the standalone skipped assertion | The response states that the exact sibling v7 input is packaged and the inherited program retained | The proposed remedy addresses the reported cause. Standalone execution is **not independently verified here**, so this is neither falsely certified nor relabeled as a new mathematical failure. |

The older closures concerning the probability of the failure prefix, the dimension-truncated global cover, genuine index-only updates, the common decision baseline, and the distinction between a continuous history encoding and a global quotient chart remain closed. An adverse editorial recommendation does not license reopening them without new evidence.

## 4. Audit of the intrinsic classification

### 4.1 The object being classified and the role of formal labels

Sources: [S1], [S2], [S8], especially `thm:resolution-main` and `thm:intrinsic-checkpoint`.

At a checkpoint with past length n and remaining length m, the positive formal homogeneous labels retain multiplicities even when their exponent sums coincide. There are q_m such labels. Their normalized nodes lie in a fixed interval bounded away from zero, because the one-step calibration set is compact inside the strictly ordered positive chamber. The constant label is removed separately.

The past capacity is p = min{n(r−1), q_m}. The maximal Vandermonde product over l positive labels is V_(m,l), with V_(m,1)=1 and zero value when fewer than l distinct positive nodes exist. The claimed checkpoint law is

\[
 \Psi_{n,m}(M,a)=
 \max_{1\le l\le p}\left(\frac{\mathcal V_{m,l}(a)}{M}\right)^{2/l}.
\]

The causal law takes its maximum over checkpoints. This is an all-budget comparison up to constants, not an exact optimal distortion constant or an exact integer crossover threshold.

Keeping formal labels does not claim that coincident moments are independently observable. The fixed full-column-rank product expansion is a statement in the formal homogeneous polynomial space. The physically reachable vectors satisfy the additional equalities at coincident exponents. The zero determinant volumes and zero diagonal scales remove precisely those directions. Confusing formal coefficient rank with physical rank would be a serious error, but the proof does not make it.

### 4.2 Leja ordering and zero pivots

Source: [S8], `lem:leja-scales`.

The finite greedy construction supplies nonincreasing pivots d_1=1, d_j=product_(i<j)|x_j−x_i|. The interval normalization makes every remaining distance at most one, which is what justifies monotonicity. Once all distinct sites have appeared, the remaining pivots vanish.

The interpolation matrix has entries bounded by one because each selected node maximizes the relevant product over the remaining nodes. Its leading active block is lower triangular with diagonal entries of absolute value one. Consequently the active block and its inverse have bounds depending only on the finite number of labels, not on a smallest nonzero gap. This proves the weighted metric equivalence also when there is a zero tail.

For every l, evaluation of the monic Newton polynomials on an l-element subset gives

\[
 \prod_{j\le l}d_j\le\mathcal V_{m,l}
 \le l!\prod_{j\le l}d_j.
\]

The upper bound is a determinant expansion, and the selected Leja subset gives the lower bound. The zero case follows without division. I found no missing gap-dependent constant here. This is useful finite-dimensional interpolation bookkeeping; its correctness should not be confused with a new general interpolation theorem.

### 4.3 Arbitrary repeated-node flags and normalized attainment

Sources: [S3], [S5], [S8], particularly `lem:binomial-tangent`, `lem:confluent-positive`, and `lem:newton-attainment`.

This is the critical experiment-specific step. At the common interior binomial tuple, the unnormalized product differential is the monomial space with n(r−1)+1 distinct exponents. That calculation remains valid throughout the one-step chamber.

For any initial ordered multiset of p positive nodes, the p Newton divided-difference functionals span the full Hermite evaluation space at that multiset. At each distinct node this includes all derivatives from order zero through its multiplicity minus one; repetitions need not be adjacent. Applied to z↦t^(Hz), this is the complete corresponding exponential-polynomial space. Adjoining the constant produces p+1 tests, not a selection of isolated higher jets with missing predecessors.

The strict mixed/confluent moment pairing with the binomial tangent therefore has column rank p+1 for every full-support prior. Since the product itself is in the tangent and its normalized constant coordinate equals one, normalization loses exactly one rank. This directly proves the p-dimensional desingularized submersion at collisions. It does not assert that all p coordinates remain physically visible after multiplication by the vanishing diagonal.

The repeated-node spanning fact is classical Newton–Hermite theory; de Boor's Proposition 7 makes the relevant prefix property explicit. The paper's application to the attained normalized product is valid. The correct editorial comparison is therefore not that de Boor already proved the posterior theorem, but that the extension of the test flag itself is an established interpolation fact. This distinction is important in evaluating what is genuinely added in v9.

### 4.4 Uniformity, evidence, and the absence of a prior-density hypothesis

Source: [S8], `lem:newton-attainment`, together with the explicit inverse construction in [S5] and [S7].

Positive exponents remain uniformly bounded away from zero. The Hermite–Genocchi representation bounds the divided differences and the finitely many required derivatives by bounded functions of the form t^c|log t|^j. Thus the derivatives in the command variables extend continuously to every repeated-node configuration. There are finitely many formal orderings. After rank has been proved at every configuration, compactness supplies a positive minimum row singular value for each relevant map, and then for their finite collection.

Discontinuities in a chosen greedy ordering do not defeat this argument: one considers each fixed permutation before taking the finite minimum. There is no need for a jointly continuous choice of Leja ordering, local frame, or codebook. Nor does arbitrary compact K need to be a semialgebraic family for this step.

Uniform second-command-derivative bounds and a common interior command radius give the local inverse box. The exploration density is multiplied by the all-failure evidence, which is bounded below by the appropriate power of the command margin. Integrating complementary command coordinates gives an actual subprobability minorization of a translated p-cube. The density being transformed is the command density, not a density of the hidden-parameter prior. These are adequate reasons for both the claimed prior generality and the unconditional lower bound.

### 4.5 The global upper bound is not a local-chart extrapolation

Sources: [S7], `lem:tame-rectangle`; [S8], proof of `thm:intrinsic-checkpoint`.

For each report word, the evidence and the selected moment numerators are polynomials in the command entries. The prior integrals and exponent-dependent test integrals appear as real coefficients. Their parameter dependence need not be semialgebraic: fixed-format estimates are applied separately with constants independent of those coefficients. Finite union over report words preserves a bounded format.

Individually normalizing the n report factors gives at most n(r−1) affine coordinates; the moment map is rational in them. The complete scaled image therefore has dimension at most p and lies in a rectangle with half-widths B d_j. The inherited real integral-geometric estimate bounds its covering number by a sum of the first p products of side lengths. Its proof uses uniformly bounded component counts of affine sections and projection volumes of the containing rectangle. It does not require the reachable set to be flat or a global quotient chart to exist.

The integer-budget inversion handles small M separately and recenters nonempty covering balls on the reachable image. Zero-width coordinates do not invalidate the argument. This genuinely provides at most M reachable representatives covering every admitted history. No omitted logarithm, hidden coefficient lower bound, or unjustified replacement of an intrinsic dimension by an affine-hull dimension was found.

### 4.6 The lower bound uses the correct metric and arbitrary centers

Source: [S8], proof of `thm:intrinsic-checkpoint`.

Conditional averaging of decoder randomness leaves at most M query-prediction centers. Projecting to the appropriate affine query span and applying a bounded left inverse of the fixed product matrix reduces the problem to raw moments. The inverse of the active Leja block then recovers the scaled coordinates without dividing by a pivot. Projecting onto any first l active attainable coordinates gives a minorized rectangle with volume proportional to d_1...d_l.

The probability covered by M radius-b balls is bounded by a dimensional constant times M b^l/(d_1...d_l). Choosing b so that a positive fraction of that minorized mass remains yields the required squared-error term. Maximizing over l gives the full profile. Randomized assignment cannot improve on the closest center. Independent public coding randomness can be fixed and averaged because it does not generate the acquisition history.

The argument allows centers outside the attainable set; it does not assume that an optimal decoder is a reachable posterior. At an exact collision the zero-volume terms contribute nothing. These details close the usual potential gaps in such a converse.

### 4.7 The same rates are causally compatible

Sources: [S6], operational definition; [S8], `thm:intrinsic-streaming`.

The raw homogeneous-label update is

\[
 v'_\alpha=
 \frac{\sum_i f_i(g,x)v_{\alpha+e_i}}
      {\sum_i f_i(g,x)v_{e_i+(m-1)e_0}},
 \qquad |\alpha|=m-1.
\]

Every index on the right belongs to the previous raw state. The denominator is a report probability and remains at least the positive margin on a segment joining two reachable vectors, since that segment represents a mixture of their posterior measures. Bounded coefficients and moments then give a Lipschitz estimate independent of exponent gaps.

An updated reachable representative is reachable at the next stage. Quantizing it in that stage's codebook is therefore legitimate. The finite error recurrence accumulates all prior lossy updates and is controlled by the maximum checkpoint profile. The exact prefix is an analysis variable, not stored implementation data. Conversely, every streaming index is a checkpoint encoder, and all checkpoint acquisition laws are prefixes of the same exploration law. The maximum lower bound consequently applies to one filter before taking the infimum.

This is a genuine persistent-state theorem in the stated exact-real program model. It is not effective codebook synthesis, a bound on arithmetic workspace, a horizon-uniform stability theorem, or a calibration-blind implementation. Those limitations are explicit. They delimit the result's significance; they do not refute it.

## 5. Tree phases and the two-parameter consequence

Source: [S8], `thm:collision-tree` and `cor:two-parameter`.

Given pairwise power orders, the valuation of a subset Vandermonde product is the sum of its pair orders. Maximizing among finitely many positive products selects the smallest such sum. There is no cancellation issue in this step. The triangle inequality gives w_(alpha,gamma) ≥ min{w_(alpha,beta),w_(beta,gamma)}, so the threshold classes are nested. Charging each internal cluster increment by the number of selected pairs in that cluster gives the stated tree decomposition and finite allocation recurrence. Identical analytic sums must first be identified, as the statement requires.

For A_(u,v)={0,1,2+u,3+v} at the peak checkpoint n=3,m=2, there are six separated limiting groups and three possible within-group gaps: |u|, |v−u|, and |v−2u|. Their two largest values are comparable to rho=max{|u|,|v|}; the smallest is tau. Thus the products for l=6,7,8,9 have orders 1, rho, rho², and rho² tau. The seven-dimensional term is a geometric interpolation of the six- and eight-dimensional terms. This gives exactly

\[
 \max\{M^{-1/3},\rho^{1/2}M^{-1/4},
                  (\rho^2\tau)^{2/9}M^{-2/9}\}.
\]

The other checkpoints cannot exceed the six-dimensional strong term. The exact peak dimensions are nine off the three collision lines, eight on a line away from the intersection, and six at the origin. Along u=theta, v=theta+theta^k, the determinant order list is

\[
 (\beta_1,\ldots,\beta_9)=(0,0,0,0,0,0,1,2,k+2).
\]

The crossover budget exponents are 6 and 8k−2, and the corresponding regret exponents are 2 and 2k. These calculations were checked independently for k=2,3,4,7,11, as well as on a signed 25-point calibration grid and separate nested trees.

The pathwise constants may depend on the nonzero leading coefficients of the path. This is not the same uniformity as the determinant theorem's uniformity on K. The manuscript states the distinction correctly. The tree result organizes supplied pair orders; it does not, by itself, determine those orders for arbitrary smooth paths or classify all additive collision arrangements.

## 6. Inherited claims and targeted literature comparison

The exact sparse rank and the causal continuous history encoding remain consistent with their stated notions of sufficiency. The three-cell Hilbert-function calculation, the five- and seven-trial rates, and the prescribed-exploration control upper bound have no newly identified blocking defect. The control bound still has its separate, weaker power and is not a sharp lower law for arbitrary rewards.

The ticket construction correctly transfers squared prediction loss into half that loss in one binary-action experiment. The erasure comparator is the exact specified statistic T_theta, not the best possible four-dimensional statistic. Its value gap and the necessary budget use the same full-history baseline. The mechanical section concerns a separately counted, uncensored two-cartridge experiment. Its partition optimization and small-amplitude threshold do not provide an independent proof of the intrinsic collision theorem, but they are internally consistent with their own protocol. The audit table keeps these dependencies visible.

The targeted primary-source comparison was as follows.

* **de Boor, Divided Differences:** Proposition 7, printed page 48, explicitly identifies an initial Newton sum with the full Hermite interpolant at an arbitrary node multiset. This is the relevant classical prefix fact in the new flag argument. [Primary text](https://arxiv.org/pdf/math/0502036).
* **Batenkov–Diederichs–Goldman–Yomdin:** the actual statements of Theorems 2.2–2.3 and Corollary 2.1, printed page 6 of arXiv:1909.01927v2, concern clustered Fourier Vandermonde spectra under their stated separation and quasiuniformity conditions. They neither prove attainable posterior minorization nor the present index-only theorem. [Pinned primary text](https://arxiv.org/pdf/1909.01927v2).
* **Comte–Halupczok:** the retrieved preprint identifies itself as arXiv:2206.15412v2, 25 September 2024. Introduction equations (4)–(5) recall the classical real variations and covering inequality actually used here; no nonarchimedean theorem is substituted for a real result. The published record is Compositio Mathematica 161 (2025), 959–992. [Primary text](https://arxiv.org/pdf/2206.15412) and [published record](https://doi.org/10.1112/S0010437X25007031).
* **Zhang–Kileel:** Lemma 2.18 in the versioned v4 text gives coefficient-independent regularity for semialgebraic sets in terms of degree, ambient dimension, and number of inequalities. Fixed-format quantifier elimination and finite union are the additional standard steps needed for the formulas here. [Versioned primary text](https://arxiv.org/html/2311.05116v4).

I did not separately inspect the full Yomdin–Comte monograph or establish exhaustive priority across the interpolation, total-positivity, information-state, and quantization literatures. The report makes no such claim.

## 7. Grounds for the negative editorial recommendation

### E9.1 — The intrinsic determinant is a classical finite spectral profile; the residual theorem must carry the significance

The attached technical note proves, using the manuscript's own finite Newton factorization, that for the square ordinary Vandermonde matrix W(x)=(x_i^(j−1)) and its ordered singular values,

\[
 \mathcal V_l(x)\asymp_q\prod_{j=1}^{l}\sigma_j(W(x)),
\]

uniformly over nodes in [0,1], including coincidences. Thus the determinant profile is, up to fixed-dimensional constants, the exterior singular-value profile of an ordinary finite evaluation matrix. This is not an additional mysterious geometric invariant whose novelty follows from being called intrinsic.

That comparison does **not** subsume the attained-posterior theorem. The latter still needs the specific product tangent, positivity for every full-support prior, the acquired-history minorization, the global dimensional cover, and compatible updates. Those are precisely the ingredients whose significance should be defended. V9 correctly distinguishes them in prose, but the resulting contribution remains a specific compatibility theorem rather than a new general spectral or entropy mechanism.

The v8-to-v9 increment becomes particularly clear after this separation. Arbitrary Newton prefixes span complete Hermite spaces; the existing strict confluent pairing then applies. Compactness over finitely many orderings replaces compactness along the old affine interval. The bounded-format upper bound and raw-moment recurrence require essentially the same argument already used in v8. This is a clean and useful completion of the classification. In my judgment, the manuscript has not shown that this completion transforms the contribution into an exceptional general-mathematics result.

This is not the claim that a short proof cannot be profound or that classical tools cannot produce a major theorem. It is a judgment about the importance established by this particular theorem and its consequences, after the standard finite-matrix content is removed.

### E9.2 — The new consequences are valid but remain close to the input formula

The tree theorem is a real structural consequence, not another single numerical horizon. Nevertheless, its energy is the valuation of a finite product, its hierarchy follows from the order inequality for differences, and its recursion is finite allocation over a laminar tree. The two-parameter example then reduces to three explicit linear gaps between nine nodes. Arbitrarily high contact order is inserted through the chosen path and propagated correctly into the rate.

These conclusions demonstrate that the intrinsic theorem handles phenomena outside the old affine list. They do not yet establish a comparably consequential theorem in another mathematical setting, a classification of collision arrangements beyond the given pair-order data, or an unexpected restriction on possible memory phases. I do not require any one of those as a mandatory extension; they explain the kind of independent mathematical force that is not demonstrated by the present examples.

The response has answered E8.3 and should not be sent back with the false complaint that no new structural consequence was supplied. The stronger and more accurate criticism is that the supplied consequence, although valid, is still largely an explicit reading of the same finite determinant formula.

### E9.3 — Breadth of calibration is not breadth of the memory problem

Allowing an arbitrary compact K is an important enlargement of the parameter domain. It does not remove the experiment's other defining structure: one hidden scalar, a positive sparse monomial likelihood space with a fixed coefficient realization, a fixed prior and horizon, continuously supplied exploration commands, and the specified spanning query task. The filter may use exact real-valued read-only data and calibration-dependent codebooks.

These conditions are not mistakes. Nor would dropping them without a proof be an improvement. But they mean that the result is a sharp order classification for this family of statistical experiments, not a general law of effective online computation or optimal decision making. The separate ticket and mechanical comparisons do not enlarge the intrinsic theorem to such a law.

The manuscript largely states this honestly. The remaining editorial burden is to explain why the mathematically precise classification it actually proves is sufficiently important on its own. Increasing the number of parameters, retained labels, or passed diagnostics is not an answer to that question. At present I am not persuaded.

## 8. Nonblocking presentation requests

**P9.1 — Make the finite spectral comparison explicit at theorem level.** A short proposition equivalent to Section 1 of the technical note would make the relation between maximal determinant products, Leja pivots, and ordinary Vandermonde singular values transparent. This is not a correction to the rate. It is a clearer identification of its classical coordinate content. It must be accompanied by the explicit statement that this comparison alone does not imply attainable posterior geometry.

**P9.2 — State the arbitrary-prefix Hermite lemma before applying it to posteriors.** The current proof contains the argument, so there is no missing lemma on which the theorem is unsupported. Isolating it would prevent readers from mistaking the Hermite spanning fact for the new statistical result and would make nonadjacent repetitions completely transparent. Cite the precise classical prefix statement, rather than only divided-difference calculus in general.

**P9.3 — Separate the final proof architecture from the revision history.** The final intrinsic theorem now appears first, as requested. The body nevertheless retains successive full-future, affine, attainable, and intrinsic versions with repeated proof architectures, followed by operational examples and historical preservation discussion. A mathematical reader should be able to follow one dependency spine from the product tangent through the intrinsic theorem to its consequences. The detailed special-case proofs can remain in explicitly labeled supplementary sections or appendices. No arbitrary deletion of correct results is requested, and preservation of old sources is entirely compatible with a more selective principal narrative.

**P9.4 — Keep provenance claims separate from reproduction claims.** The statement that all predecessor proof hashes occur in the new source is a preservation statement, not a new mathematical test. A local execution receipt and a remotely reproducible publication build are different artifacts. The response already distinguishes these; maintain that distinction in subsequent handoffs. This review does not independently certify the standalone archive remedy because that archive was not executed here.

None of P9.1–P9.4 would, by itself or as a completed checklist, reverse the editorial recommendation. They are concrete improvements, not disguised claims that the main theorem is false.

## 9. Final recommendation and next-review handoff

**Reject at the requested four-journal level.** The central argument appears mathematically sound under its stated assumptions on the evidence examined. V9 substantially answers the prior review and genuinely extends the theorem beyond affine paths. The negative judgment concerns the demonstrated depth and independent consequences of that stronger result, not a nonexistent counterexample, a missing failure probability, an ambient-dimension mistake, or an illicit exact-prefix tape.

The next review should start from these closures. It should not demand a weaker theorem, invent an impossible prior-uniform constant, or automatically award acceptance for another generalization. Any further contribution should be assessed for the mathematical problem it settles and for consequences not already immediate from the same finite-matrix calculation. The program is not ruled out; the current submission has not established the exceptional significance claimed by its target.

### Immutable source index

All S1–S12 are in `papers/A1-english-v9/` at submission `e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5`.

- [S1: Introduction and main statements](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/01_introduction.tex)
- [S2: Experiment and future-only equivalence](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/02_experiments.tex)
- [S3: Attainable transversality and exact rank](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/03_transversality.tex)
- [S4: Observation algebra](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/04_observation_algebra.tex)
- [S5: Confluent positivity and checkpoint quantization](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/05_confluence.tex)
- [S6: Finite-state model and inherited streaming/control](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/06_streaming.tex)
- [S7: Global attainable cover and affine causal law](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/06a_attainable_filtration.tex)
- [S8: Complete intrinsic collision geometry](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/06b_collision_geometry.tex)
- [S9: Five-trial uniform realization](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/07_uniform_resolution.tex)
- [S10: Same-task decision comparison](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/08_sequential_value.tex)
- [S11: Separate counted mechanical experiment](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/09_common_risk.tex)
- [S12: Declared scope](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/sections/10_scope.tex)
- [Controlling v8 report](https://github.com/TrillionniumFoundation/theta-theory/blob/5f52bf456272b53bcb4df8d949effd2ab59bb79f/reviews/a1-english-v8-2026-09-06/REFEREE_REPORT.md)
- [V9 response letter](https://github.com/TrillionniumFoundation/theta-theory/blob/e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5/papers/A1-english-v9/RESPONSE_TO_REFEREE.md)
