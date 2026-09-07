# Referee report on A1 English v21

**Manuscript:** *Attainable information geometry in positive experiments*, Qian Qi.  
**Submission examined:** `7c44bdccc91667c583b5d5cbcff3f8d9160a57d6`.  
**Source branch:** `revision/a1-english-v21-causal-transfer-and-proof-hierarchy-2026-09-07`.  
**Manuscript directory:** `papers/A1-english-v21/`.  
**Controlling previous report:** `reviews/a1-english-v20-independent-2026-09-07/REFEREE_REPORT.md`, at `078f34222b00797203cdf6dd421eab9f9f428c59`.  
**Previous submission:** `6f103ad252d7c65f140720f4095585026f7bb1b9`.  
**Date:** 7 September 2026.  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica.

This is an owner-requested, AI-assisted external-referee-style assessment. It is not a journal-commissioned report, a claim of editorial appointment, or an assertion of institutional independence. The mathematical arguments and diagnostic implementation described below were examined in this review rather than accepted on the authority of the preceding report. All manuscript paths below are relative to the directory above. Stable source labels identify results; compiled numbering is used only where the source documentation identifies it. `REVIEW_SCOPE.json` records the pinned source provenance and the limits of the examination.

## 1. Recommendation and its precise basis

**REJECT in its present form for the requested four-journal standard.** The controlling reason is my assessment of the demonstrated mathematical significance of the contribution, not a counterexample to the principal collision law. This distinction is essential: I found no blocking error in the new transfer theorem, its monomial verification, or the five new statement–proof pairs examined here. The current central proof is coherent under its stated fixed-horizon, fixed-prior, known-calibration and persistent-label conventions. This is a favorable mathematical assessment of the inspected arguments, not certification of the entire manuscript.

The revision has responded substantively to the previous report. The dimension-free feasibility problem is repaired. The finite maximum-rank specialization is correctly identified as classical linear matroid intersection. The moving-kernel example is included with an actual positive experiment and its physical covariance scale. Most importantly, the principal result now has a direct proof through an explicitly stated geometry-to-causal transfer theorem. It would be unfair to describe these changes as merely cosmetic or to repeat the v19 containment-versus-exact-kernel objection against this submission.

There nevertheless remains a substantial gap between a mathematically coherent, technically careful classification in this experimental class and a compelling case for the exceptional importance sought here. The new abstract transfer statement packages a sufficient mechanism; once its rather detailed geometric and measure hypotheses are available, its conclusion follows by a standard covering lower bound and a Lipschitz representative recursion. The real contribution continues to be the simultaneous verification of those hypotheses for the monomial model, uniformly through additive collisions. That verification is meaningful. It does not, in my assessment, acquire substantially broader mathematical consequences merely because it has now been isolated as a reusable theorem.

The two-parameter phase example is a genuine consequence, not just a restatement of rank. The constrained exact-kernel theorem is also a legitimate companion result. I do not dismiss either. My negative recommendation concerns the force of their combined contribution at the specifically requested journal level. I have not established that the central collision theorem already occurs in the literature, and I do not claim this. Nor do I claim that elementary methods, finite horizons, or a specialized model are inherently inappropriate for those journals. The judgment is about this demonstrated result and its present mathematical reach.

There are concrete, finite corrections to make as well: the reorganized main route still uses some setup notation before defining it, several consequence proofs retain references to the alternative appendix route, and one new bibliographic entry has the wrong conference ordinal and title. These are not disguised fatal objections. Correcting them would repair the identified local defects, but would not by itself reverse the significance judgment.

## 2. What was examined, and what was not

I read the new introduction and main statement; the detector and delayed-query resource model; the exact-information statement; the mixed-moment and binomial-tangent arguments; the interpolation and thin-rectangle covering inputs; the complete new transfer section; the acquired Newton flags; the direct monomial application; and the bit, collision-tree and two-parameter consequences. This covers the main proof chain, not merely its abstract and response letter.

I also read the dimension-free feasibility lemma, the complete exact-kernel section, the finite common-independence and moving-kernel section, and the supporting affine covariance classification through its invariant and interior-example discussion. The entry point, README, v21 response, proof hierarchy, new bibliography wrapper, and finite-approximation comparison were checked. The preceding report was consulted to distinguish resolved objections from new ones; its favorable assessments were not treated as proof of the revised assertions.

The source entry point documents a main narrative followed by seven appendices. The authors report a 114-page build, with Appendix A beginning on page 22. I did **not** rebuild or visually audit that manuscript PDF in this review. I did not rerun the author's validator, independently verify all advertised proof-preservation hashes, or re-audit every circular, ambiguity, decision-theoretic, numerical-compiler and resource-bound appendix. The standalone diagnostics accompanying this report are the reviewer's own finite exact checks, not a rerun of the author implementation.

The generated `build/*.tex` sources used in the main route were available and readable at the pinned submission. They are not missing proofs. Likewise, preservation counts and successful compilation are not substitutes for proof verification; the authors now explicitly recognize that distinction.

## 3. Disposition of the previous objections

| Previous issue | Disposition in v21 |
| --- | --- |
| E20.1: dimension-free theorem invokes a dimension-ordered feasibility result | **Resolved.** `lem:dimension-free-feasibility` supplies a self-contained argument without comparing the dimensions of the pairing spaces, including the zero-dimensional case. |
| E20.2: finite unconstrained maximum rank needs explicit classical identification | **Resolved mathematically and in attribution.** `prop:finite-matroid-rank` states the common-independence specialization and proves it. A minor bibliographic correction remains below. |
| Square evidence-containing moving kernel | **Addressed.** `prop:square-moving-kernel` includes the example and computes the physical one-step scale. It supports the exact-kernel criterion rather than refuting it. |
| E20.3: expose the central compatibility argument | **Substantially addressed.** `thm:causal-transfer` and the direct application make the set, measure and update obligations explicit. The main application does not assume the old checkpoint or streaming classification. |
| E20.4: organize a principal route while preserving the complete mathematics | **Substantially addressed in the source structure.** The direct alternative proofs are in Appendix D. Some inherited references and notation have not been fully adapted to that reorganization. |
| Significance at the requested journal standard | **Reassessed independently; recommendation remains negative.** This is not an unresolved mathematical lemma and should not be entered into a proof ledger as though it were one. |

The exact-kernel repair from v20 remains valid. In particular, no request to replace exact realization by containment is made here. There is no basis for suppressing the earlier counterexample or for weakening the now-correct theorem to avoid it.

## 4. Audit of the new geometry-to-causal theorem

**Locators:** `sections/causal_transfer.tex`, `thm:causal-transfer`, `lem:positive-remaining-update`.

### 4.1 The hypotheses have the right logical separation

The theorem begins with a compact reachable state set and physical weighted query coordinates of the form

\[
p_n(v)=b_n+G_nv,
\]

where both the query map and a left inverse are uniformly bounded. This is a statement about the physical prediction metric. It does not whiten away a small observable scale.

Condition (G) supplies a uniformly invertible ambient coordinate change, a bounded-format semialgebraic image of dimension at most \(p_n\), and containing widths \(s_{n,1}\ge\cdots\ge s_{n,q_n}\ge0\). Condition (A) supplies actual unconditional acquisition mass on every initial nonzero resolution rectangle. Condition (C) supplies reachable-state updates with uniformly bounded Lipschitz constants, reading only current state and input. None of these statements is the desired optimal coding conclusion itself.

They are nevertheless strong sufficient hypotheses. The theorem should continue to be described as a transfer theorem, not as a classification of all positive experiments satisfying only positivity or finite-dimensional closure. The current text makes this distinction, and I find no overclaim in the printed theorem on this point.

### 4.2 The checkpoint lower bound is legitimate

For any label and independent public seed, conditional averaging removes decoder randomization under squared loss. At a fixed seed there are at most \(M\) prediction centers. A bounded left inverse of \(G_n\), followed by the bounded coordinate change, converts prediction error into a lower bound on projected state error.

For a dominated rectangle in \(\ell\) coordinates, the fraction covered by \(M\) balls of radius \(r\) is bounded above by a constant times

\[
\frac{Mr^\ell}{\prod_{i=1}^\ell s_{n,i}}.
\]

Choosing a sufficiently small fixed multiple of \((\prod_{i\le\ell}s_{n,i}/M)^{1/\ell}\) leaves positive unconditional mass outside. Randomized assignment cannot outperform nearest-center distance. Maximizing over \(\ell\) gives the claimed lower profile, including vanishing products. Conditioning on independent coding randomness is harmless here because the exploration law is fixed independently of that randomness.

The proof does not replace a report word by a probability-one event. This is precisely the place where that mistake would invalidate the lower bound, and it has not been made.

### 4.3 The whole-image upper bound and the integer budget are respected

The cited thin-rectangle lemma provides a cover of the **entire** reachable image. Its dimension truncation comes from the vanishing of higher-codimension section variations almost everywhere, not from an assertion that a selected regular patch fills the image.

The proof also handles actual integer budgets rather than asymptotic covering counts alone. For sufficiently large \(M\), increasing the radius absorbs the fixed component-count term. For the finitely many smaller budgets, the diameter bound and the first scale suffice. Replacing an external center by a point of the covered set costs only a constant factor. Thus the chosen representatives are reachable, a fact needed by the causal step.

The real entropy input is independently identifiable in Comte–Halupczok, equations (4)–(5), and the coefficient-independent bounded-format regularity input is consistent with Zhang–Kileel, Lemma 2.18; see the primary sources in Section 11. This is not an application of a nonarchimedean theorem to a real set.

### 4.4 The recursion is a genuine finite-label filter

Updating the retained reachable representative and quantizing it in the next reachable codebook gives

\[
e_{n+1}\le L_ne_n+C\sqrt{Q_{n+1}(M_{n+1})}.
\]

Induction yields the printed accumulated-error formula

\[
e_n\le C\sum_{j=1}^n\left(\prod_{i=j}^{n-1}L_i\right)\sqrt{Q_j(M_j)}.
\]

Earlier errors have not been discarded. The clock supplies the stage; no past command or report tape is reread. Every causal label is also a full-prefix encoder at its checkpoint, so the common-law checkpoint lower bounds apply before optimizing over causal filters. Taking their maximum is legitimate because the checkpoint marginals belong to one exploration experiment.

This establishes bounded-factor equivalence at the stated fixed horizon. It does not establish equality of optimal constants, a bound uniform in unbounded horizons, or a theorem about the total machine description and arithmetic workspace. None is claimed in the statement inspected.

### 4.5 The positive-update lemma is sound with dependent tests

A mixture of two posterior measures has the corresponding convex combination of their moment vectors. Along such a segment the report denominator remains at least \(\kappa\). Bounded coefficient representations and bounded test functions then control the derivative of the Bayes quotient, irrespective of linear dependencies among the tests.

This correctly avoids inversion of a singular test covariance or interpolation map. Reachability is also not merely formal: a representative posterior associated with an actual prefix can be extended by the admitted current command and report. Positivity is doing essential denominator work here, but supplies neither the global geometric cover nor the acquired measure on its own.

## 5. Independent audit of the monomial verification

**Locators:** `core/02_experiments.tex`, `core/03_transversality.tex`, `build/collision_flags.tex`, `sections/collision_transfer_application.tex`.

### 5.1 Formal coordinates and zero pivots

The fixed failure-factor basis induces an invertible change on homogeneous polynomials before exponent labels are identified. Therefore the physical product-query matrix can have full column rank in the formal coordinate space even when attainable moment vectors satisfy equal-coordinate relations. Coinciding exponents do not contradict that formal full-rank statement.

Let the active columns of the Leja evaluation matrix be \(L_{:,1:s}=(A^t,B^t)^t\), and let \(D_a\) denote the diagonal pivot matrix. The new application explicitly uses

\[
T=\begin{pmatrix}A^{-1}&0\\-BA^{-1}&I\end{pmatrix},
\qquad
T^{-1}=\begin{pmatrix}A&0\\B&I\end{pmatrix}.
\]

The active triangular block has diagonal entries of magnitude one and uniformly bounded entries. Its inverse, and hence both displayed ambient matrices, are bounded in the fixed dimension. The exact identity is \(TL D_a=D_a\), including inactive zero coordinates. This is the correct ambient extension. Simply using the active inverse and forgetting the lower-left block would leave nonzero duplicated raw coordinates; the accompanying negative controls detect that error.

The Leja pivot comparison

\[
\prod_{j\le\ell}d_j\le\mathcal V_{m,\ell}\le\ell!\prod_{j\le\ell}d_j
\]

follows from the determinant of evaluations of the first monic Newton polynomials. It remains valid when the products vanish. I found no hidden division by a zero pivot in this part of the proof.

### 5.2 The acquired flag is not inferred from observation rank alone

The tangent at the common binomial history has \(n(r-1)+1\) distinct monomial directions. The disjointness assertion for the listed exponents uses \(0<a_i<a_{r-1}\), not a generic assumption about additive sums. This is why it persists through the relevant collisions.

Every initial divided-difference prefix spans a complete Hermite evaluation space, including nonadjacent repeated nodes. Adding the constant test produces the full confluent Chebyshev system needed by the mixed pairing. The proof does not select an isolated high logarithmic derivative and then claim positivity for an incomplete system.

The unnormalized pairing has rank \(p+1\). The product itself belongs to the tangent, and its evidence coordinate is nonzero; normalization therefore loses exactly one direction. This proves the required surjectivity onto the first \(p\) Newton coordinates. The logarithmic test bounds at zero, continuity on the compact calibration set, and the finite number of formal permutations support the asserted uniform lower singular-value bound for the fixed prior.

These steps are substantive model-specific work. A Vandermonde singular-value calculation by itself would not imply the acquisition conclusion.

### 5.3 The probability and global-dimension arguments have different jobs

The local inverse construction adds orthonormal kernel coordinates to the independent output rows. Integrating over the resulting kernel-coordinate box gives a genuine lower density in output space. Multiplication by the actual failure-word probability remains present. Consequently the local section is not being assigned ambient history mass by fiat. The same independent command experiment can be used for the different checkpoint prefixes.

For the upper bound, each report-word raw-moment map is rational in its command variables, with uniformly positive evidence denominator and bounded degrees. Normalizing each factor by its own prior integral puts it in an affine hyperplane of dimension \(r-1\), without changing the posterior. This gives the dimension bound \(n(r-1)\) for the complete image. A finite union over report words preserves bounded semialgebraic format. Arbitrary real coefficients depending on the prior or calibration do not invalidate a format bound for each fixed parameter.

Finally, remaining raw monomials close under multiplication by the next likelihood with bounded formal coefficients. The positive-update lemma applies without recovering a discarded command and without dividing by a collision gap. Thus the three transfer hypotheses are established separately, on the same experiment and with compatible uniformity.

### 5.4 The phase consequence adds information beyond dimension

At the two-parameter example's critical checkpoint, the three within-group gaps are \(|u|\), \(|v-u|\), and \(|v-2u|\). Their largest two are comparable, while the smallest can be much smaller. The intermediate seven-dimensional term is dominated by the geometric interpolation of the six- and eight-dimensional terms. This gives the printed three-branch law.

On \(u=\theta\), \(v=\theta+\theta^k\), the crossovers \(M\asymp\theta^{-6}\) and \(M\asymp\theta^{-(8k-2)}\) are consistent with errors of orders \(\theta^2\) and \(\theta^{2k}\). The independent diagnostics check the corresponding exponent identities. Thus it would be incorrect to criticize this consequence as merely the fixed-parameter dimension exponent in different notation.

## 6. The feasibility, exact-kernel and finite-pairing results

**Locators:** `sections/kernel_feasibility.tex`, `sections/exact_kernels.tex`, `sections/finite_pairing_comparison.tex`, and `sections/affine_geometry.tex`.

The new feasibility lemma closes E20.1. Separation of the finite moment body gives the equivalence between absence of a nonzero nonnegative function in \(W\) and the relative-interior condition at zero. A sufficiently small mixture with any prescribed full-support reference probability then produces a full-support annihilator. The argument needs no comparison of \(\dim E\) and \(\dim F\), and the explicit \(W=0\) convention is correct. I do not regard this as an unresolved gap.

The exact-kernel theorem still obtains the crucial open moment chart in the quotient \(V/W_U\). Orthogonal projection at a feasible full-support measure gives continuous, bounded, centered tilt functions with positive-definite Gram matrix. Their moment map is an invertible affine map on the quotient coordinates. A nonzero maximal minor of the quotient multiplication pencil must therefore be nonzero at an admissible positive tilt. This proves exact realization, not just annihilation of the proposed kernel. Small boxes and polynomial interpolation justify the finite grid witness statement. The theorem appropriately declines to identify this algebraic test with computability from unspecified real moments.

The forced-kernel identity also has the right quantifier. A residual orthogonal to \(W_U\) can be used as a small admissible tilt; vanishing under all such tilts forces that residual to be zero. The absence of a common forced direction does not imply that some pairing is injective. The balanced-block classification and the square moving-kernel example preserve this distinction.

In the finite unconstrained case, the Cauchy–Binet expansion of an \(\ell\)-minor of \(A\operatorname{diag}(w)B^t\) has distinct subset monomials. It is nonzero exactly when an \(\ell\)-element column set is independent in both represented matroids. Nonvanishing somewhere in the positive orthant and homogeneity give positive probability weights. This classical specialization is now correctly identified, with a primary-source comparison in Terao's paper and its attribution to earlier algebraic work. Under additional annihilation equations, the monomials need not remain independent on the constrained slice, so that finite argument alone does not prove the full constrained compact-space theorem.

For the four-point example, the matrix

\[
H_p=\begin{pmatrix}1&p_3&p_4\\p_1&0&0\\p_2&0&0\end{pmatrix}
\]

has rank two for every positive prior and kernel \(\operatorname{span}\{p_4e_3-p_3e_4\}\). Both spaces contain evidence; the common kernel is zero; dimensions do not explain the failure of injectivity. With the printed acquisition features and query weights the squared singular scale is

\[
\frac{(p_1^2+p_2^2)(p_3^2+p_4^2)}{512}.
\]

Direct covariance calculations in the diagnostics agree. The supporting affine theorem is appropriate: its exact projective acquisition coordinates have a uniformly thick input law and denominators bounded away from zero. This example is explanatory evidence for the corrected theorem, not a newly discovered obstruction to it.

## 7. E21.1 — restore the setup notation in the reorganized principal route

**Severity:** required self-containedness correction; not a counterexample.

The present `main.tex` includes the new introduction, `core/02_experiments.tex`, `build/operational_model.tex`, `build/exact_information.tex`, and `core/03_transversality.tex` in that order. In this actual reading route, the introduction specifies the latent interval as \([0,1]\), but it does not establish several pieces of notation subsequently used by the inherited core files:

* `build/exact_information.tex`, `thm:main`, uses \(h_A(m)\) in the displayed definition of \(d_A(n,m)\) without defining it there or in the preceding included setup.
* `core/03_transversality.tex`, `lem:binomial-tangent`, uses \(D\) for the extremal exponent without the preceding setup declaring \(D=a_{r-1}\).
* `core/02_experiments.tex` uses \(I\), and its realizability proof uses the endpoint \(u\); the mixed-moment proof in `core/03_transversality.tex` then refers to \((l,u)\). The preceding new introduction uses \([0,1]\) rather than introducing these general-interval symbols.

The intended meanings can be reconstructed, but a submission should not make the reader recover them from historical files or later material. Add a short explicit setup paragraph before the core arguments, for example

\[
I=[l,u]=[0,1],\qquad D=a_{r-1},\qquad
mA=\{a_{i_1}+\cdots+a_{i_m}\},\qquad h_A(m)=|mA|,
\]

with \(0A=\{0\}\), or consistently rewrite the inherited interval notation for the specialized main setting. This restores definitions; it changes no theorem. A compilation check for undefined references does not detect an undefined mathematical symbol, so successful TeX validation does not answer this point.

## 8. E21.2 and E21.3 — route and bibliography corrections

### E21.2: the consequences still point to the alternative route

**Severity:** minor proof-navigation correction.

The new main proof itself is independent of the appendix classification, as claimed. However, in `build/collision_consequences.tex`, the proof of `cor:intrinsic-bits` still invokes `eq:intrinsic-streaming`, and the proof of `thm:collision-tree` invokes `thm:intrinsic-checkpoint` and `thm:intrinsic-streaming`. Those are now the alternative direct route in Appendix D.

These are valid mathematical references, not a logical contradiction. But they unnecessarily weaken the advertised minimal route and send the reader to an appendix for consequences that follow immediately from `thm:resolution-main`. Replace the controlling references by that theorem, keeping the appendix references as optional alternative derivations. The inherited theorem and proof blocks can remain intact in the archival and alternative-proof material. No deletion of mathematical content is requested.

### E21.3: the SWAT entry has incorrect metadata

**Severity:** minor bibliographic correction.

`references-v21.tex` describes Terao's paper as appearing in the “19th Scandinavian Symposium and Workshops on Algorithm Theory.” The publisher's entry for DOI `10.4230/LIPIcs.SWAT.2026.39` gives **20th Scandinavian Symposium on Algorithm Theory (SWAT 2026)**. The volume 370 and article pages 39:1–39:19 agree. Correct the ordinal and conference title. This does not invalidate the finite-pairing proposition or its classical attribution.

## 9. E21.4 — significance and the remaining contribution case

**Severity:** controlling editorial assessment at the requested tier, not a missing proof.

The revision now states its mathematical center and provides a credible proof architecture. I am therefore not asking it to identify a center that it has already identified, to re-prove the repaired exact-kernel criterion, or to add another small example merely to increase the theorem count.

My remaining concern has three specific aspects. First, the abstract transfer theorem is a sufficient interface between geometric estimates and a stable finite-horizon recursion. Its breadth is conditional on verifying the global cover and actual flag mass, which are almost the entire difficult part of the classification problem. The theorem is useful organization, but the present revision has not demonstrated that this abstraction substantially enlarges the mathematical reach of the monomial classification itself.

Second, the physical prediction model is carefully defined but deliberately specialized: fixed horizon, a fixed full-support prior, known calibration, a selected finite spanning menu of future products, and a label-cardinality resource with exact-real read-only data. Those are legitimate hypotheses, not defects. However, the manuscript must be evaluated for the theorem in this model, rather than for an unrestricted theory of finite-memory inference, AI, or total computational memory. The stated comparisons with finite approximation and information states correctly decline such broader claims. They improve accuracy of positioning, but do not themselves supply additional consequences.

Third, the companion results do not presently turn the local prior-slice classification into a general collision-sensitive multistep law. The affine covariance theorem has a complete one-step profile. The exact-kernel theorem has a strong local realization conclusion. The main monomial theorem has the compatible global geometry and causal conclusion. These are different levels of information. The revised scope table recognizes this, and I agree with it. Their juxtaposition is not yet, in my judgment, a sufficiently powerful common theorem to change the publication recommendation at the requested level.

This is not a claim that an application to a famous open problem or an unbounded-horizon theorem is necessary. I impose neither requirement. Nor is the remedy necessarily another theorem: an explicit, economical demonstration of the reach of the present invariant in independently motivated problems, or of the transfer principle's substantive reuse across the already developed classes, could change how the existing mathematics is evaluated. Such a demonstration must add mathematical understanding, not only a new umbrella name.

The report's concrete corrections are finite and listed above. There is no moving list of alleged proof failures. At the same time, a referee cannot promise that performing those local corrections will yield acceptance at a chosen journal tier. My present recommendation remains negative even after granting the correctness assessments in Sections 4–6.

## 10. Independent exact diagnostics and reproducibility

The accompanying `independent_diagnostics.py` imports no author theorem implementation. It was executed in this review with Python 3.13.5 and SymPy 1.14.0, both normally and under `python -O`. The JSON outputs were byte-identical. The checks use explicit exceptions, not removable `assert` statements.

**Actual result: 140 grouped cases and 657 explicit checks, all passing.** These counts describe the script's test grouping, not 140 independent theorems or 140 distinct experimental distributions. In particular, the 81 moving-kernel cases are positive integer weight tuples in \(\{1,2,3\}^4\); proportional tuples can normalize to the same prior.

| Diagnostic group | Cases | Checks |
| --- | ---: | ---: |
| Integrated Newton/Hermite identities | 6 | 6 |
| Leja pivots, maximal volumes and full ambient maps | 14 | 143 |
| Normalized acquisition ranks and remaining-moment updates | 28 | 236 |
| Square moving-kernel pairings and physical covariance | 81 | 243 |
| Finite common-independence specializations | 4 | 4 |
| Accumulated causal-error recurrences | 3 | 9 |
| Two-parameter crossover exponents | 4 | 8 |
| Negative controls and their execution guard | — | 8 |
| **Total** | **140** | **657** |

The history tests use the full-support measures

\[
\mu_\alpha=\alpha\,dt+(1-\alpha)\delta_0,
\qquad \alpha\in\{1,2/5\},
\]

and rational calibration configurations with exact collisions and small nonzero gaps. A separate integrated formula provides the divided-difference moments:

\[
\int_0^1 t^b[x_1,\ldots,x_j](z\mapsto t^{Hz})\,dt
=\frac{(-H)^{j-1}}{\prod_{i=1}^j(b+1+Hx_i)}.
\]

It follows by taking the divided difference of \((b+1+Hz)^{-1}\); continuity supplies repeated nodes. Positive nodes make the logarithmic tests vanish at zero, so the atomic component contributes zero to these test integrals. This permits exact rational calculation of the normalized Jacobian, separately from evaluating a near-singular numerical Vandermonde matrix.

The script checks the complete first-\(p\) Newton rank, the smaller raw rank at collisions, the evidence-augmented rank, and raw updates against direct posterior multiplication. Six deliberately incomplete ambient maps, with the necessary lower-left subtraction omitted, fail the correct matrix identity as expected. A deliberately truncated recurrence also fails; the eighth negative-control check confirms that the collision controls were actually exercised.

These tests are diagnostic support only. They do not prove compact-uniform lower singular-value constants, inverse-chart mass, the real entropy inequality, or optimal finite-state coding. They do not construct an optimal filter or establish the compiler's complexity. No successful finite test count is used as evidence for journal-level significance.

Reproduction from this review directory:

```sh
python independent_diagnostics.py --output DIAGNOSTICS.json
python -O independent_diagnostics.py --output DIAGNOSTICS_OPTIMIZED.json
cmp DIAGNOSTICS.json DIAGNOSTICS_OPTIMIZED.json
```

The committed `DIAGNOSTICS.json` contains the script SHA-256, runtime versions, per-group counts and limitations. `REVIEW_SCOPE.json` records the actual commands and the identical-output result.

## 11. Primary-source checks used in this report

The literature checks here are targeted verification of inputs and attribution, not an exhaustive novelty search.

**[P1]** Georges Comte and Immanuel Halupczok, *Motivic Vitushkin invariants*, arXiv:2206.15412v2, equations (4)–(5) in the introductory discussion of the classical real theory. The displayed page containing those formulas was inspected. Those formulas recall the real section-variation and metric-entropy input used in the manuscript; no motivic analogue is substituted for it. Primary text: https://arxiv.org/pdf/2206.15412.

**[P2]** Yifan Zhang and Joe Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, arXiv:2311.05116v4, Lemma 2.18. The page displaying the lemma was inspected for the bounded-format semialgebraic regularity input. Primary text: https://arxiv.org/pdf/2311.05116.

**[P3]** Tatsuya Terao, *Faster Approximate Linear Matroid Intersection*, 20th Scandinavian Symposium on Algorithm Theory (SWAT 2026), LIPIcs 370, 39:1–39:19, DOI 10.4230/LIPIcs.SWAT.2026.39. The primary text explicitly recalls the common-base determinant criterion and earlier algebraic work; the publisher metadata resolves the conference-title correction. Primary text: https://arxiv.org/html/2604.11725v1. Publisher record: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SWAT.2026.39.

All online checks were made on 7 September 2026. Harvey's earlier work is correctly part of the manuscript's attribution; this report does not pretend to have performed a separate full reading of that paper or of every work in the manuscript bibliography.

## 12. Final assessment

The appropriate conclusion is neither “the revision is mathematically empty” nor “all referee concerns are now settled because the code passes.” The revision contains a coherent and nontrivial uniform collision argument, an explicit causal implementation at the stated resource level, and a valid exact-kernel realization mechanism. The new proof architecture makes those claims substantially easier to evaluate. The principal scope restrictions are now stated honestly.

I require the setup, reference-route and bibliographic corrections in Sections 7–8 for a self-contained revised presentation. I do not identify a new fatal counterexample to the main result. Nevertheless, I do not recommend publication of this submission at the requested four-journal standard, for the significance reasons in Section 9. This editorial conclusion should remain separate from the record of which mathematical objections have actually been resolved.
