# Independent harsh referee report on A2 revision 87

**Review date:** 19 September 2026  
**Reviewed branch:** revision/a2-v87-gap-free-singular-quotient-2026-09-19  
**Review branch:** review/a2-v87-independent-harsh-top4-2026-09-19  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v87/paper.tex  
**Principal source blob SHA:** 92662fda998a6e6e04704cebc7d07fbcc233432cf623d60b467a90b428b05f10  
**Companion:** papers/A2-v17-boundary-information-coarsening/rigidity_v87_companion.tex  
**Response reviewed:** reviews/a2-v87-response-to-v86-2026-09-19/RESPONSE_TO_REFEREE.md  
**Predecessor audit reviewed:** reviews/a2-v87-response-to-v86-2026-09-19/LITERATURE_AUDIT.md  
**Controlling previous report:** reviews/a2-v86-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md

## Editorial recommendation

**Reject in the present form at the standard of Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica.**

This recommendation is materially different from my recommendation on revision 86. Revision 87 **does** answer the central architectural objection in the previous report: the principal paper is no longer an accumulation of unrelated regimes. It is now a compact theorem paper centered on one projective matrix-curve experiment, one gap-free singular inverse estimate, one intrinsicized observation signal, and matching finite-experiment lower-bound families.

I also did **not** find a short counterexample or a fatal local proof error in the new main theorem, the two-clock fibre, the arbitrary-rank product family, the collapsing-spectrum family, or the adaptive-design lower bound. The central proof strategy is coherent.

The remaining objection is therefore not “the paper still has no theorem.” It now has a theorem. The issue is whether that theorem, in its present scope and literature position, has the conceptual depth and breadth required for a four-leading-general-mathematics-journal paper. I do not think that threshold has yet been crossed.

The strongest new result is mathematically clean, but its unification occurs inside a highly rigid affine projective model
\[
P(T)=A+\frac{B}{T-h},
\qquad
K(T)=(T-h)P(T)
      =U\operatorname{diag}(\alpha_b(T-\xi_b))V^{\mathsf T},
\]
and after the scalar pole is recovered the main inverse proof becomes a structured finite-dimensional pencil perturbation argument in the true channel coordinates. The arbitrary-rank extension is genuine, but “arbitrary fixed rank” is not by itself the kind of conceptual enlargement that compensates for how specialized the observation law remains.

My present view is that this is now a serious specialist paper with a potentially publishable core. It is not yet a top-four general-mathematics paper.

---

## 1. What revision 87 genuinely fixes

The authors should receive full credit for changing the mathematical and expository architecture rather than merely adding another module.

The new ten-page principal article has a clear theorem spine:

1. exact recovery of the common pole from three projective observations;
2. an explicit nontrivial two-clock fibre with fixed channels;
3. a one-sided, gap-free inverse estimate against the entire closed competitor model;
4. an observation-fibre envelope \(\vartheta_*\);
5. honest residual confidence regions with no supplied signal floor;
6. an arbitrary-rank weak-channel family with exactly fixed marginals;
7. a full-spectrum-collapse family with well-conditioned channels;
8. matching minimax and confidence-diameter orders, including adaptive clock selection.

This is a real response to sections 4, 5, 9 and 14 of the v86 report. The paper is no longer relying on the binary determinant calculation as the conceptual center. The proof of Theorem 1.1 isolates the two losses
\[
\kappa=\sigma_k(U)\sigma_k(V),
\qquad
\gamma=\|B\|_F,
\qquad
\vartheta=\frac{\kappa\gamma}{\kappa+\gamma},
\]
and obtains coefficient error of order
\[
\delta\left(\kappa^{-1}+\gamma^{-1}\right)
=\delta/\vartheta
\]
without charging the pole error a second channel-inverse factor. This is the right cancellation to look for.

The product lower-bound family is also much better than a binary special case. It works for every fixed admissible latent capacity and rectangular alphabet, keeps both observed marginals exactly fixed, and exposes the tensor-product interaction direction directly. The collapse family separately proves that a perfectly conditioned channel pair does not help when the whole projective curve becomes constant.

The principal/companion split is also a substantial improvement. The new article can actually be read as a paper.

These are important advances over v86.

---

## 2. The main theorem is correct-looking, but its generality is narrower than the title and rhetoric suggest

Theorem 1.1 is the paper's strongest result. I checked the core proof route carefully.

The pole estimate from the ratio of consecutive differences is sound-looking. After the pole has been recovered, multiplication by the true left/right pseudoinverses gives
\[
M(T)
=(D_\alpha+E_1)T-D_\alpha D_\xi+E_0,
\qquad
\|E_0\|+\|E_1\|
\lesssim \delta(\kappa^{-1}+\gamma^{-1}).
\]
For sufficiently small perturbation the leading coefficient is invertible. The candidate leading coefficient factorization then forces the reduced candidate outer factors to be invertible, so the roots of \(\det M(T)\) are exactly the candidate action multiset. The gap-free matching lemma completes the argument without an individual spectral-gap denominator.

I do not see an immediate algebraic defect in this chain.

But the theorem's scope should be described more soberly. The model has all of the following built into it:

- a **single scalar common pole** \(h\);
- an **affine numerator** after pole clearing;
- two fixed stochastic channel matrices;
- a known latent capacity \(k\);
- a positive component-weight floor \(\alpha_*\);
- three controlled clocks in a fixed compact interval above the action interval;
- finite-dimensional categorical observations;
- constants allowed to depend on all fixed dimensions, intervals, clocks and the weight floor.

This is not yet a general singular-quotient theory. It is a sharp theorem for one especially favorable rational matrix curve.

The phrase “for every fixed latent rank” is mathematically correct but editorially easy to overread. No dimension dependence is derived, no high-rank regime is controlled, and no statement is uniform as \(k,m_1,m_2\) grow or \(\alpha_*\downarrow0\). The arbitrary-rank result is therefore algebraic generality, not a dimension-uniform theory.

At top-four level, the paper needs to say exactly what principle survives if the affine numerator or one-pole structure is changed. At present it is not clear whether the theorem is the first case of a broader mechanism or a very elegant exploitation of this one model.

---

## 3. The main proof must be positioned against generalized-eigenvalue and matrix-polynomial perturbation theory, not only Bauer--Fike

The predecessor audit remains too thin around the mathematical technology that is closest to the new theorem.

The paper cites Bauer--Fike, but the central step is a **regular generalized eigenvalue / matrix-pencil perturbation problem with repeated real eigenvalues and structured perturbations**. There is an extensive literature on precisely these questions.

At minimum the revised paper should compare its result carefully with:

- E. K.-W. Chu, *Exclusion Theorems and the Perturbation Analysis of the Generalized Eigenvalue Problem*, SIAM J. Numer. Anal. 24 (1987), 1114--1125;
- E. K.-W. Chu, *Perturbation of Eigenvalues for Matrix Polynomials via the Bauer--Fike Theorems*, SIAM J. Matrix Anal. Appl. 25 (2003);
- N. J. Higham, D. S. Mackey and F. Tisseur, *The Conditioning of Linearizations of Matrix Polynomials*, SIAM J. Matrix Anal. Appl. 28 (2006), 1005--1028;
- the structured-pseudospectrum / structured-condition-number literature for polynomial and rational eigenvalue problems.

I am **not** claiming that one of these papers already proves Theorem 1.1. The special point here is that the observation perturbation is first passed through a pole-recovery step, and the authors exploit the true channel coordinates so that the pole error is diagonal and does not receive another channel condition factor. That may well be new in this model.

But the paper currently makes the novelty comparison too easy for itself. A top-four submission cannot present a structured pencil perturbation theorem while comparing essentially only to the original 1960 Bauer--Fike paper.

The same issue appears on the latent-structure side. Bonhomme--Jochmans--Robin is cited, which is good, but robust/polynomial identifiability work such as Bhaskara--Charikar--Vijayaraghavan, *Uniqueness of Tensor Decompositions with Applications to Polynomial Identifiability* (COLT 2014), is a natural comparison point for the claim that the novelty is robustness through degeneracy rather than exact diagonalization alone.

The current literature section is a useful start, not an adversarial novelty audit.

---

## 4. \(\vartheta_*\) is invariant by definition, but the paper has not yet turned it into a structural singular invariant

Equation (1.5)
\[
\vartheta_*(P)
=\max\{\vartheta(\omega):\mathcal P(\omega)=P\}
\]
solves a real problem: at repeated spectra, the factorization may have gauges, so the raw product of smallest channel singular values is representation-dependent.

Defining the maximum over the exact observation fibre makes the quantity invariant. That is mathematically legitimate.

However, at present this is still an **optimization definition**, not a structural characterization of the singular quotient.

The paper does not establish, for example:

- a formula or dual characterization of \(\vartheta_*(P)\);
- continuity or a sharp semicontinuity theorem for \(P\mapsto\vartheta_*(P)\);
- an equality or two-sided comparison with distance to the nonidentifiable observation set;
- an observable Jacobian/singular-value characterization;
- a classification of the zero set \(\{\vartheta_*=0\}\) beyond the displayed channel-rank and full-spectrum-collapse mechanisms;
- a computationally usable certificate for \(\vartheta_*\) at repeated spectra.

Theorem 1.1 makes the definition useful: if a maximizing representative has positive signal, the target is constant on the exact fibre and the same one-sided bound applies. But the phrase “intrinsic observation signal” is stronger than what has been structurally proved.

This is, in my view, the most important mathematical direction for a next revision. A true singular-quotient theorem would identify \(\vartheta_*\) (or a replacement) as the metric slope, smallest nonzero singular value, distance-to-discriminant, or another canonical invariant of the quotient map.

Right now the paper has made the signal representation-independent, but it has not yet explained what the invariant **is**.

---

## 5. The minimax theorem is sharp at the class level, but it is not a classification of singular strata

Theorem 7.1 proves
\[
\inf_{\widehat\xi}
\sup_{\vartheta_*\ge s}
\mathbb E d_\infty(\widehat\xi,\xi)^2
\asymp \min\{1,(Ns^2)^{-1}\}.
\]

The upper bound follows from the one-sided modulus. The lower bound is obtained by embedding an explicit weak-channel family with \(\epsilon_u\epsilon_v\asymp s\). The collapsing-spectrum family supplies a second attained singular mechanism. The adaptive-clock extension via conditional relative entropy is clean.

This is a valid and useful minimax statement.

But the paper should not let “matching singular orders” drift into a stronger claim than what is proved.

The theorem does **not** classify the local minimax geometry of every singular point in the model. It does not show that every observation with \(\vartheta_*\approx s\) has local modulus comparable to \(1/s\), nor does it identify all possible anisotropic exponents at intersections of singular strata. It proves a worst-case class upper bound and matches that class order with explicit least-favourable paths.

That distinction matters because the introduction repeatedly uses the language of “singular quotient theory.” A true stratified theory would state what happens at all relevant rank/action multiplicity patterns and at their intersections, not only show that two mechanisms attain the global class rate.

The paper partly acknowledges this in the sentence that it does not identify the exact directional condition number of every anisotropic latent factorization. I think that limitation should be moved much closer to the principal theorem and abstract.

---

## 6. The arbitrary-rank product family is strong, but one uniqueness step should be made explicit

Lemma 5.1 is a genuine improvement over the binary construction.

The exact marginal cancellation is transparent and the singular-value calculation is plausible. The right singular direction \((1,-1,0,\ldots,0)/\sqrt2\) has output magnitude \(\epsilon_u/(\sqrt2\lambda)\), while the orthogonal complement maps into the fixed independent directions \(u_0,e_3,\ldots,e_k\). With \(\epsilon_*\) small enough, the displayed smallest singular value is therefore exact. The same holds for \(V_t\).

The argument that \(\vartheta_*=\vartheta\) uses simple-spectrum factor uniqueness. I think this is correct, but the paper should make one point explicit:

> if another exact representation of the same three-clock datum exists, then the observable affine coefficient \(A\) has rank \(k\); hence the alternative \(U'\operatorname{diag}(\alpha')V'^{\mathsf T}\) must also have rank \(k\), which forces both alternative channel matrices to have full column rank. Only then does the simple-spectrum reconstruction show uniqueness up to permutation.

The current Proposition 3.3 proves reconstruction from one full-rank representation, but it does not spell out this exact-fibre implication at the place where \(\vartheta_*=\vartheta\) is used. This is repairable and not a substantive objection.

---

## 7. The matching lemma is plausible, but the proof should be written at the standard expected for the central gap-free claim

Lemma 3.1 is doing important work: it replaces the usual separated-eigenvalue labeling argument by a multiset matching bound that survives repeated actions.

The disk-component homotopy argument is reasonable. Still, because the no-gap claim is one of the paper's main selling points, I would either:

1. cite an exact theorem from the perturbation literature and explain why its hypotheses apply; or
2. make the proof fully formal, including the argument-principle step on the moving disks and the passage from component root counts to the monotone real matching.

The present proof is probably correct, but it is compressed enough that a reader may reasonably ask whether the component boundaries remain uniformly root-free along the homotopy and how the limiting disk inflation is chosen when adjacent components merge.

Again, this is not a counterexample. It is a request that the central gap-free lemma be written defensively.

---

## 8. The statistical upper bound is information-theoretic rather than algorithmic

The residual estimator and confidence region are defined by optimization over the entire compact parameter space \(\mathcal K\). Compactness gives existence, and the finite categorical sample space avoids measurable-selection complications.

That is enough for minimax theory.

But the manuscript also gestures at “exhaustive implementation” through finite forward nets. Such a construction is generally exponential in dimension/resolution and does not give a practically meaningful estimator.

This is acceptable if the paper clearly labels the statistics as **information-theoretic**. If the authors want the statistical section to carry broader weight, they should either:

- give a polynomial-time or otherwise structurally efficient estimator with the same modulus order; or
- remove any suggestion that computational tractability has been addressed.

For a top general journal, an existence-only estimator is not fatal, but it reduces the breadth of the statistical contribution.

---

## 9. The exact three-clock threshold is elegant, but still tied to one projective normalization law

Proposition 2.2 gives an explicit smooth two-clock fibre while keeping the channels fixed, and the third clock resolves the scalar pole. This is a clean exact threshold inside the model.

The next conceptual question is: what survives for a broader projective curve?

For example, if pole clearing gives a degree-\(d\) matrix polynomial, or several nuisance poles, or a low-dimensional rational numerator space, is there an invariant saying how many clocks are needed and what the corresponding singular modulus is?

The companion contains many other clock-count regimes, but they remain logically separate. Revision 87 has successfully unified the affine projective experiment; it has not unified those broader finite-clock problems.

A top-four version would become much more compelling if Theorem 1.1 were the \(d=1\) instance of a theorem about a class of projective matrix functions rather than the endpoint of one special model.

---

## 10. The companion solves the archive/article problem only partially

The principal article is now appropriately short. This is a major improvement.

However, the submission package still includes a 122-page companion preserving essentially the entire historical program. That is excellent repository practice and may be useful as supporting material. It is not automatically good journal architecture.

For an actual top-four submission, the authors should decide which companion statements are logically needed for the principal theorem and which are independent papers or archival derivations. The fact that old mathematics is preserved in the repository is not a reason that every regime should travel with this article as a formal companion.

I am not recommending deletion from the repository. I am recommending a sharper submission boundary.

---

## 11. Literature positioning remains below the standard required for the breadth of the claims

The new LITERATURE_AUDIT.md is more careful than previous versions. In particular it correctly distinguishes exact identification from the new singular modulus and cites Ho--Nguyen for mixture singularities.

But the novelty audit still has important holes.

### 11.1 Matrix pencils and polynomial/rational eigenvalue conditioning

As discussed above, the paper needs direct comparison with generalized eigenvalue perturbation, polynomial eigenvalue conditioning, structured pseudospectra and rational matrix-function conditioning. Merely citing Bauer--Fike is not enough.

### 11.2 Robust latent decomposition

The manuscript cites classical latent-structure diagonalization but does not seriously compare with robust tensor/latent decomposition results that quantify perturbation under nondegeneracy assumptions. Bhaskara--Charikar--Vijayaraghavan is an obvious starting point. Even if the present target is only the action multiset and therefore avoids eigenvector instability, that distinction must be made against the strongest robust latent-decomposition literature, not only against exact identifiability.

### 11.3 Singular statistical models

Ho--Nguyen is relevant, but the paper would benefit from a broader comparison with algebraic/singular statistical models and weakly identifiable mixtures. The key claim is not simply that singularity slows rates, but that **partial action collision does not** slow the chosen spectral target whereas channel-rank loss and full projective collapse do. That target-dependent distinction is interesting and should be positioned more aggressively.

A broad journal will ask whether the theorem is a genuinely new inverse-problem principle or a particularly clean finite-dimensional example of existing condition-number/singularity technology. The present bibliography does not yet force an expert reader to answer that question in the authors' favor.

---

## 12. Proof-level comments

These are not the main editorial reason for rejection, but they should be addressed.

### 12.1 Exact-fibre uniqueness in the simple-spectrum case

Explicitly prove that every exact representation of a simple-spectrum full-rank datum is itself full rank because the observable coefficient \(A\) has rank \(k\). Then the equality \(\vartheta_*=\vartheta\) on the lower-bound family is completely transparent.

### 12.2 Regularity of \(P\mapsto\vartheta_*(P)\)

The maximizer exists by compactness, but the paper should state what regularity is known. If continuity is false, say so and give the correct semicontinuity statement. If continuity is true on the identifiable locus, prove it. This matters for treating \(\vartheta_*\) as an intrinsic signal.

### 12.3 Lower-bound class bookkeeping

In the proof of Theorem 7.1 the constants in
\[
\vartheta_*\asymp \epsilon_u\epsilon_v
\]
must be synchronized with the fixed \(t\)-interval, positivity bounds, the choice \(\epsilon_u\epsilon_v=Ms\), and the testing displacement \(t\asymp(\sqrt N s)^{-1}\). The argument is standard and appears fixable, but a uniform minimax theorem deserves the constants to be stated in a single lemma rather than distributed across prose.

### 12.4 Adaptive-clock experiment

Formally define the adaptive experiment: at step \(i\), the clock \(T_i\in[T_1,T_3]\) should be measurable with respect to the previous observations and external randomization, followed by one categorical draw from \(P_\omega(T_i)\). The KL chain-rule argument is then immediate. The current proof says this informally.

### 12.5 Empty confidence set convention

Reporting an empty set on the noncoverage event is fine, and assigning diameter zero there for the expected-diameter loss is mathematically explicit. Still, this convention should be highlighted in the theorem statement rather than only in the construction paragraph, because it makes the expected-diameter quantity look slightly better on model-inconsistency outcomes.

### 12.6 Theorem 1.1 constants

Because all constants may depend on \(k,m_1,m_2,\alpha_*,L,D,T_1,T_2,T_3\), the theorem should state this immediately adjacent to the theorem rather than only in the setup. This will prevent readers from interpreting “every fixed latent rank” as dimension-uniform conditioning.

---

## 13. Reproducibility status at the reviewed branch

The local records are much better organized than in earlier revisions.

I credit the following branch-local facts:

- v87-local-verification.json records passed source/identity diagnostics;
- v87-local-build.json records a successful local native build;
- the principal build is reported as 10 pages and the companion as 122 pages;
- the local record explicitly denies formal proof certification and does not claim GitHub Actions success.

However, at the reviewed branch the expected workflow-generated files are absent:

- verification/v87-native-verification.json;
- verification/v87-native-source-commit.txt;
- verification/v87-native-pdf-sha256.txt;
- rigidity_v87.pdf as the workflow-published branch artifact.

Therefore I do **not** credit an independent GitHub Actions native build in this report. I credit the local build record only.

This is not a mathematical objection.

---

## 14. What would change the editorial assessment

Revision 87 has already taken the most obvious step requested in v86. Another cycle of adding one more regime would not help.

A further top-four review would be justified by one of the following genuinely structural advances.

### 14.1 Characterize the intrinsic singular quotient

Replace the optimization definition of \(\vartheta_*\) by, or prove it equivalent to, a canonical metric/analytic invariant of the observation map. Ideally identify the singular set and derive two-sided local moduli on its strata.

### 14.2 Extend the theorem beyond the one-pole affine curve

Prove a theorem for a natural class of projective rational or polynomial matrix curves in which the present three-clock result is the first nontrivial case. The clock threshold and singular modulus should emerge from one complexity invariant.

### 14.3 Prove a genuine stratified local minimax theorem

Classify the local rates and anisotropies at the relevant rank/action-multiplicity strata and their intersections, rather than only giving a global class rate with two attaining families.

### 14.4 Establish a sharp comparison theorem with the pencil/latent-decomposition literature

Show precisely which standard generalized-eigenvalue or robust latent-decomposition condition numbers would produce weaker rates, and prove that the present quotient target eliminates those losses. This could itself become a conceptual contribution if formulated abstractly.

### 14.5 Add dimension-uniform content

If “arbitrary rank” is to carry major weight, derive explicit dependence on \(k,m_1,m_2,\alpha_*\) and determine whether any meaningful high-dimensional regime remains stable.

Any one of these would materially change my assessment. A larger companion or more finite verification would not.

---

## 15. Final assessment

Revision 87 is the strongest and best-organized A2 revision I have reviewed.

It does three things that the previous version did not:

1. it puts the principal mathematics into one coherent projective experiment;
2. it extends the determinant-product phenomenon to arbitrary fixed latent rank with a gap-free spectral target;
3. it proves matching finite-experiment orders with explicit weak-channel and whole-spectrum-collapse families.

I did not identify a fatal flaw in these results.

But at the level of the four leading general mathematics journals, correctness plus a clean model-specific singular modulus is not enough. The paper still needs a more canonical singular invariant, a broader structural theorem, or a substantially stronger novelty comparison showing that the main result is more than a tailored structured-pencil perturbation theorem with sharp model-specific lower bounds.

Accordingly my recommendation remains:

**Reject in the present form at the stated top-four level.**

I would encourage submission to a strong specialist journal after the proof-level and literature-positioning issues are repaired, or another genuinely structural revision along one of the routes in section 14.

---

*This is an owner-requested independent external-referee-style assessment of the repository manuscript. It is not a journal-commissioned report and does not represent an editorial decision.*
