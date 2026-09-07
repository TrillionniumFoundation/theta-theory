# Independent referee report on A1 English v20

**Manuscript:** *Attainable information geometry in positive experiments*, Qian Qi.  
**Submission examined:** `6f103ad252d7c65f140720f4095585026f7bb1b9`.  
**Source branch:** `revision/a1-english-v20-exact-kernels-and-causal-geometry-2026-09-07`.  
**Manuscript directory:** `papers/A1-english-v20/`.  
**Controlling previous report:** `reviews/a1-english-v19-independent-2026-09-07/REFEREE_REPORT.md`, at `59018a3231abb551d93947929f7e9bf0e3ddcd9e`.  
**Previous reviewed manuscript:** `01abeb689b203ea871b88495d16a826bb4942e16`.  
**Date:** 7 September 2026.  
**Requested publication standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica.

This is an owner-requested, AI-assisted external-referee-style assessment, not a journal-commissioned report or an assertion of editorial appointment. It concerns the pinned submission, not a future revision or the eleven-paper programme. Source paths below are relative to the manuscript directory unless otherwise indicated. Stable source labels, rather than unverified compiled theorem numbers, identify the arguments examined.

## 1. Recommendation

**REJECT in its present form for the requested four-journal standard.** This is principally an editorial judgment about mathematical significance and the architecture of the contribution, not a finding that the new exact-kernel theorem is false. The v19 exact-kernel objection has been substantively answered. Repeating that objection against the revised theorem would be incorrect.

The revision contains a genuine theorem-level repair. Its quotient moment chart converts the existence of an admissible prior into an open set of unrestricted quotient coordinates. A nonzero determinantal polynomial must then attain a nonzero value on that set. This supplies the missing sufficiency argument for exact realization; it is more than a renamed containment condition. The forced-kernel identity and the balanced-block classification are also correct as inspected. I found no blocking counterexample in the five new statement/proof pairs.

The strongest inherited contribution remains the conjunction of unconditional acquisition mass, a dimension-truncated cover of the whole prediction image, and a gap-free causal update, uniformly through additive exponent collisions. I re-examined the principal dependencies of this conjunction rather than taking the previous report's favorable assessment on trust. The inspected chain is coherent under its printed fixed-horizon, fixed-prior and calibration assumptions.

There is a small, precisely repairable mismatch between the dimension-free scope of the new section and a theorem it invokes; Section 4 supplies the repair. Section 5 supplies a stronger stress example for the determinantal condition, with both spaces containing evidence and with no dimensional obstruction. The example supports the new theorem rather than refuting it. Section 6 identifies a further classical finite specialization that should be made explicit in the contribution comparison.

Nevertheless, the added exact-kernel machinery is a finite-dimensional separation/projection/generic-rank argument, and its physical corollary gives local rank and local mass, not a new general multistep resolution classification. The manuscript correctly acknowledges this limitation. In my judgment, the current combination of conclusions still does not make a sufficiently compelling case for the exceptional mathematical importance requested here. This judgment is not settled by the number of results, the preservation of proof blocks, or successful diagnostics. Nor would the addition of another small example, on its own, settle it.

Elementary arguments can prove important theorems. A fixed-horizon theorem can also be important. Neither feature is a disqualification. The objection is to the demonstrated significance of this particular package, not to the permissible methods or to the possibility of developing the programme further.

## 2. Scope and disposition of the previous report

The new mathematics in `sections/exact_kernels.tex` was read in full. The response letter, full principal introduction including the scope table, source entry point, relevant comparison sections, build/preservation implementation, and execution receipt were examined. The inherited collision chain was inspected through `core/02_experiments.tex`, `core/03_transversality.tex`, the confluent positivity argument in `core/05_confluence.tex`, the thin-rectangle covering argument in `core/06a_attainable_filtration.tex`, `sections/classical.tex`, and the checkpoint/streaming arguments in `core/06b_collision_geometry.tex`. The opening structural classification, normalized-rank and actual-history-mass arguments were also examined. The dimension assumptions of `sections/rectangular_attainment.tex` were checked directly.

This is not a claim to have independently reverified every one of the advertised 114 proof blocks, every circular/ambiguity argument, the entire numerical compiler, or every appendix. The manuscript PDF was not rebuilt or visually audited in this review. Generated `build/*.tex` inputs are documented outputs of preparation; their absence as individual tracked files is not treated as a missing-proof objection. The reviewer executed the accompanying independent diagnostics, not the author's validator.

| Controlling issue | Disposition in v20 |
| --- | --- |
| E19.1: containment described as exact kernel realization | **Resolved in substance.** The introduction now distinguishes the two questions, and `thm:exact-kernel` supplies the extra condition with a valid sufficiency mechanism. |
| The eight-point counterexample | Correctly retained and explained, rather than suppressed. The new block family also supplies exact positive alternatives. |
| The need to identify the mathematical center | Substantially addressed in the introduction and input order. The collision/causal synthesis now leads. The remaining concern is the force and economy of the contribution, not the absence of a stated center. |
| Classical square/rectangular criteria and covariance construction | The explicit Banaji–Pantea, Müller et al., Fourier and analytic-order attributions must receive credit. They should not be reopened as unanswered old objections. |
| Four-journal significance | Reassessed, not automatically inherited from the preceding rejection. The recommendation remains negative for the reasons in Sections 6–8. |

The revision is therefore not merely cosmetic. Conversely, resolving a mathematical objection does not oblige a referee to recommend publication at a specified journal tier.

## 3. Audit of the five new results

### 3.1 Local coordinates on the constrained prior slice

`lem:kernel-moment-chart` is correct as inspected. With

\[
W_U=\operatorname{span}(EU),\qquad V=\operatorname{span}(\{1\}\cup EF),
\]

the selected classes \([1],[v_1],\ldots,[v_s]\) are independent in \(V/W_U\). At a feasible full-support probability \(\mu_*\), the functions

\[
h_\nu=v_\nu-\mu_*v_\nu-\Pi_{W_U}v_\nu
\]

are continuous, bounded, centered and orthogonal to \(W_U\). A linear dependence among them would contradict the quotient basis. Full support makes the continuous-function Gram form definite, even when the prior has no density with respect to an ambient reference measure. Thus the Gram matrix \(B\) is positive definite and the moment map of the density tilt is exactly \(\mu_*v+Bt\).

The strict bound on the sup norm of the tilt preserves positivity and full support, while centering preserves total mass. Repeating this argument at every feasible prior proves openness of the full quotient moment image; convexity follows from mixing full-support priors. There is no unwarranted assumption that a possibly lower-dimensional constrained image is open in an oversized ambient coordinate space: the quotient has already removed precisely those linear relations. The empty-coordinate case \(s=0\) is handled correctly.

### 3.2 Exact-kernel criterion and local realization

The principal content of `thm:exact-kernel` is the equivalence

\[
\exists\mu\text{ of full support}:\ker H_\mu=U
\quad\Longleftrightarrow\quad
W_U\cap C(X)_+=\{0\},\qquad
\operatorname{rank}_{\mathbb R(z)}\mathscr H_U(z)=\dim(F/U).
\]

After feasibility has been established, the matrix induced on \(F/U\) is exactly the quotient pencil evaluated at the moment coordinates. A nonzero maximal minor cannot vanish on the open moment image from the preceding lemma. This proves sufficiency. The same reasoning proves that the maximal rank on the entire constrained full-support slice is the algebraic rank of that pencil. Necessity is immediate from the same identity and the positivity of the integral of any nonzero nonnegative continuous function under full support.

The stronger approximation claim is justified. In a local chart, substitution by the invertible affine map preserves nonzero polynomials. A sufficiently small box keeps the density perturbation below the prescribed sup-norm tolerance; a tensor grid with \(r_U+1\) values in each coordinate detects a nonzero minor of degree at most \(r_U\). Relative weak openness of maximal rank follows from continuity of finitely many moment entries and a nonzero minor. The proof does not confuse relative weak topology on the feasible full-support class with openness in the space of all probabilities.

The finite-atom mixture conclusion also has the correct quantifier. One first fixes all moments in \(V\), then represents the same interior moment by a mixture with the prescribed full-support reference probability. This preserves the whole pairing, not only the equations annihilating \(U\). The weight of the full-support component need not be uniform, and the theorem does not say that it is. The empty-minor and constant-pencil conventions are appropriate.

This is a mathematically sound repair, subject to the citation clarification in Section 4. It is not a new general determinantal identity, and the manuscript itself now says so.

### 3.3 The forced kernel

`prop:forced-kernel` correctly identifies

\[
\bigcap_{\mu\in\mathcal P_U}\ker H_\mu
=\{f\in F:Ef\subset W_U\}.
\]

For the nontrivial inclusion, take \(g=ef\), subtract its projection onto \(W_U\), and perturb a feasible prior in that residual direction. The residual is centered because \(g\) and its projection both have zero mean at the chosen prior. The perturbed integral of \(g\) is a scalar multiple of its squared residual norm. Vanishing for all small positive and negative perturbations forces the residual to be zero. Continuity and full support then upgrade almost-everywhere equality to equality of functions.

The product-space equality and idempotence follow from the two evident inclusions. The statement correctly stops short of treating the absence of a forced direction as sufficient for an injective quotient pairing. Section 5 makes the importance of this last distinction particularly transparent.

### 3.4 Exact balanced-block kernels

`prop:block-kernels` is correct. Writing the mass and imbalance of block \(j\) as \(s_j\) and \(d_j\), the annihilation equations force \(d_j=0\) precisely away from the common roots \(Z_S\). A row outside \(Z_S\) forces the constant coefficient of any kernel element to be zero. Such a row exists because \(S\ne0\), the degree bound gives \(|Z_S|\le m-1\), and the stated lower bound on \(n\) is more than sufficient.

Distinct-point polynomial evaluation on the remaining roots has rank \(|Z_S|\). The printed positive witness therefore has rank \(1+|Z_S|\) and kernel equal to the polynomials vanishing on those roots. Exact realization of \(S\) is equivalent to equality with this entire root-vanishing space, not just containment in it. The factor-theorem description follows.

The likelihood and query realizations are genuine: the acquisition features stay within a common positive likelihood bound, and the fixed query probabilities stay between \(1/4\) and \(3/4\). The referee's exact diagnostics include 42 root-saturated instances, the original eight-point obstruction, a nonsaturated polynomial line, and the associated physical covariance ranks. These checks supplement the preceding proof analysis; they do not prove its unrestricted statement.

### 3.5 Return to the acquired prediction state

`cor:kernel-history-rank` correctly adjoins the evidence direction before normalization. For the pairing \(L\), one has

\[
L(F)=\mathbb RY+L(\operatorname{im}DP),\qquad Y=LP=(Z,Zp),\quad Z>0.
\]

Normalization kills exactly \(\mathbb RY\) on this image. The actual command derivative consequently has rank \(\operatorname{rank}L-1\), without assuming that the history product is itself a command derivative.

The unconditional mass argument is also legitimate. It completes independent output rows with kernel coordinates, uses a local inverse on a product box, and integrates over the entire kernel-coordinate box while retaining the probability of the specified report word. It does not assign ambient history mass to a lower-dimensional section. The corollary correctly makes no general whole-image covering or multistep uniform-memory conclusion from this local fact alone.

## 4. E20.1 — clarify the dimension-free feasibility citation

**Classification: minor proof-dependency/scope mismatch; not a counterexample to the theorem.**

The opening of `sections/exact_kernels.tex` explicitly imposes no ordering on \(d=\dim E\) and \(k=\dim F\). In the feasibility part of the proof of `thm:exact-kernel`, however, the text invokes `thm:v19-rank-alternative`. The standing assumptions of `sections/rectangular_attainment.tex`, where that theorem is stated, include \(1\le k\le d\). The new proof should not invoke the old theorem outside those printed hypotheses without explanation.

The repair is immediate and does not change the result. Apply `lem:v19-moment-image` directly to the vector of products \(G_U=(e_a u_i)\), or to a basis of \(W_U\). Separation identifies the absence of a nonzero nonnegative element of \(W_U\) with \(0\) belonging to the relative interior of the corresponding moment body; the moment-image lemma supplies the full-support annihilating probability. Neither step compares \(d\) and \(k\). When \(W_U=0\), the zero-dimensional moment map gives the same conclusion.

Alternatively, explicitly state the dimension-free containment consequence of that lemma and cite it. The old containment proof already uses no dimension ordering. This is a local exposition/proof-reference correction, not a reopening of the repaired distinction between containment and equality.

## 5. A stronger stress test: a square, evidence-containing pencil with a moving kernel

The response mentions a one-row/two-column example showing that closure is not sufficient. That example has an immediate dimensional explanation. The following four-point example removes that explanation while remaining a positive physical experiment. It is offered as an independent diagnostic and explanatory example, not as a claim of a globally new construction.

Let \(X=\{1,2,3,4\}\), let \(e_i\) denote the singleton indicators, and put

\[
E=\operatorname{span}\{1,e_1,e_2\},\qquad
F=\operatorname{span}\{1,e_3,e_4\},\qquad U=0.
\]

Both spaces have dimension three and contain the constant function. For any full-support probability \(p=(p_1,p_2,p_3,p_4)\), the pairing in these bases is

\[
H_p=
\begin{pmatrix}
1&p_3&p_4\\
p_1&0&0\\
p_2&0&0
\end{pmatrix}.
\]

Its determinant vanishes identically, whereas its upper-left \(2\times2\) minor is \(-p_1p_3\ne0\). Hence every such pairing has rank two and

\[
\ker H_p=\operatorname{span}\{p_4e_3-p_3e_4\}.
\]

The common kernel over all full-support priors is zero: the ratio \(p_3/p_4\) varies. Also \(\operatorname{cl}_E(0)=0\), directly because \(1\in E\). Thus feasibility holds, closure fixes \(U\), and \(\dim(F/U)=\dim E\); nevertheless no full-support prior realizes the zero kernel. The missing condition is exactly the one supplied by v20: \(r_0=2<3\).

For a physical realization choose acquisition features

\[
f=(e_1,e_2)^t/4,\qquad
L_y(u,x)=\tfrac12(1+y\,u^tf(x)),\quad u\in[-1,1]^2,
\]

and two equally weighted future binary queries

\[
g_1=\tfrac12+\tfrac14e_3,\qquad
g_2=\tfrac12+\tfrac14e_4.
\]

All likelihoods lie in \([3/8,5/8]\); both query probabilities lie in \([1/2,3/4]\). At \(u=0\), the history product and derivatives span \(E\), and the augmented query space is \(F\). With the manuscript's square-root query weighting, the physical covariance is

\[
C_p=-\frac1{16\sqrt2}
\begin{pmatrix}p_3\\p_4\end{pmatrix}
\begin{pmatrix}p_1&p_2\end{pmatrix}.
\]

It has rank one for every full-support prior, with sole nonzero singular value

\[
s(p)=\frac{\sqrt{p_1^2+p_2^2}\sqrt{p_3^2+p_4^2}}{16\sqrt2}.
\]

Accordingly the affine theorem yields the one-step law \(R_M\asymp s(p)^2M^{-2}\), consistent with the normalized history rank \(\operatorname{rank}H_p-1=1\).

The accompanying code verifies the symbolic determinant, nonzero minor, moving kernel, covariance identity and scale. It additionally checks pairing rank two and physical rank one for 55 strictly positive rational probability vectors. Two of the displayed full-support pairings already have zero common kernel when stacked. This is not a counterexample to v20. It shows that its determinant condition detects a real obstruction not visible either to the multiplication closure or to a dimension count.

## 6. E20.2 — make the finite maximum-rank specialization explicit

**Classification: contribution-comparison obligation, not a claim that the complete constrained theorem was already published verbatim.**

The existing Banaji–Pantea and Müller et al. comparisons concern preservation of full rank for every positive weighting. The new exact-kernel section also concerns a different quantifier: maximum rank, and attainment of that rank on a positive moment slice. A further finite specialization should be explained rather than left implicit under the general phrase “determinantal geometry.”

For finite \(X=\{x_1,\ldots,x_s\}\) and \(U=0\), let \(A\) and \(B\) have columns given by the evaluations of bases of \(E\) and \(F\). Then

\[
H(w)=A\operatorname{diag}(w_1,\ldots,w_s)B^t.
\]

For equal-sized row sets \(I,J\), Cauchy–Binet gives

\[
\det H(w)_{I,J}
=\sum_{|S|=\ell}\det A_{I,S}\det B_{J,S}
                       \prod_{s\in S}w_s.
\]

The monomials indexed by distinct subsets are distinct. Consequently some \(\ell\)-minor is a nonzero polynomial precisely when there is an \(\ell\)-element column set independent in both evaluation matrices. The generic rank is the maximum size of such a common independent set. A nonzero polynomial cannot vanish throughout the positive orthant. Since the minors are homogeneous, normalizing positive weights to sum one does not change this maximum-rank statement.

This is the symbolic-matrix formulation of linear matroid intersection. For an explicitly checked primary-source statement of the common-base determinant criterion, see [R1, p. 39:2]; [R2] gives older algebraic matroid-intersection background. The accompanying referee code checks the Cauchy–Binet identities and the common-independent-set rank interpretation in six finite configurations, including zero-rank and structurally singular examples.

This observation has a precise limit. After imposing \(H_\mu U=0\), the weights are restricted by additional linear equations. The unrestricted monomial argument cannot simply be transplanted to that affine slice. Nor does the finite statement by itself prove bounded continuous density-tilt realization on an arbitrary compact space. Those are exactly the aspects for which the new quotient chart must receive credit.

The requested revision is therefore a short, exact comparison: identify the classical finite \(U=0\) corner, then explain what the quotient and full-support chart add for constrained kernels. I am not alleging plagiarism or denying the value of the repair. I am asking that its mathematical position be stated at the same level of precision now used for the older universal-pairing results.

## 7. Independent audit of the collision/causal spine

### 7.1 The spectral calculation is not the attainment argument

`lem:leja-scales` and `prop:exterior-profile` have a valid fixed-dimensional proof. The greedy pivots are nonincreasing because all distances lie in \([0,1]\). Newton evaluation gives a bounded triangular active block with diagonal entries of modulus one; the inactive columns are multiplied by zero. Selected-row determinants then give

\[
\prod_{j=1}^{\ell}d_j\le\mathcal V_{m,\ell}
                         \le\ell!\prod_{j=1}^{\ell}d_j.
\]

No reciprocal zero pivot is needed. The uniformly bounded change from the power basis to monic Newton polynomials also justifies the exterior-singular-value comparison. The referee diagnostics include repeated nodes and two separated close pairs, but the proof, not those configurations, supplies the gap-uniform assertion.

Clustered Vandermonde spectra have substantial independent literature. In particular, [R5] studies a rectangular, unit-circle, clustering regime. That result should not be conflated with the fixed-dimensional real-node calculation here, and it does not establish posterior acquisition mass or a causal finite-label minimax theorem. An observation-side spectral estimate alone is not a valid prior result from which to declare the whole A1 theorem redundant.

### 7.2 The attainable Newton prefix has the required rank

The binomial product tangent in `lem:binomial-tangent` is explicitly identified, not guessed from the dimension of the ambient posterior algebra. The polynomials obtained by omitting one distinct factor \(1+c_i z\) form a basis through degree \(n-1\), by evaluation at \(-1/c_j\). Constant and top-exponent variations then generate the multiples of \(D\), while the interior-exponent variations give disjoint translated strings. This verifies the count \(n(r-1)+1\).

For an arbitrary ordered prefix of repeated future nodes, the divided-difference functionals span complete Hermite blocks. The triangular evaluation on ordinary powers proves independence even with nonadjacent repetitions. Mixed-moment positivity and the confluent Chebyshev argument apply to these complete blocks. The positive exponent lower bound controls the logarithmic functions at the endpoint \(t=0\). Exactly one evidence direction is lost upon normalization.

These facts justify `lem:newton-attainment`. There are finitely many formal label permutations, and the derivative is continuous for each permutation through the compact parameter set. Compactness can therefore supply a common positive lower bound on the relevant row singular value. This would not be justified by merely asserting generic rank on a moving open stratum; the printed argument is stronger and uses the collision configurations themselves.

The conversion to probability is also present: the inverse chart includes kernel coordinates and retains the all-failure word probability. Thus the argument establishes unconditional mass, not just a smooth image of a probability-zero section.

### 7.3 The whole-image upper cover is an independent step

`lem:tame-rectangle` uses bounded-format affine-section component counts and the real Vitushkin entropy inequality. The dimensional truncation is valid: affine sections of codimension exceeding the set's dimension are empty almost everywhere. For the remaining orders, the projected containing rectangle has volume bounded by a constant times the product of its largest side lengths. The argument includes zero-width axes and a separate small-integer-budget step when converting the entropy estimate to at most \(M\) reachable centers.

The relevant coefficient-independent semialgebraic regularity is explicitly available in [R3, Lemma 2.18]. The real Vitushkin inequality and the affine-section form used here appear in the introductory equations (4)–(5) of [R4]; those introductory real statements, not that paper's new nonarchimedean results, are the pertinent comparison.

The application in `thm:intrinsic-checkpoint` is sound as inspected. For each fixed calibration, prior moments and divided-difference values are real coefficients in a bounded-format rational command map. They do not need to depend semialgebraically on the calibration parameter. Normalizing each factor separately supplies the past-dimensional upper bound. A local regular chart is not being substituted for a global cover. The lower bound separately uses the minorized prefix cubes and a volume argument for the union of \(M\) balls.

### 7.4 The causal part charges the retained information correctly

The recurrence in `thm:intrinsic-streaming` uses formal raw moments, not unscaled divided differences. Multiplying a remaining test by the next likelihood stays in the previous remaining-test space. Its denominator is positive not only at reachable posteriors but also along their mixture segments. The quotient rule therefore gives a Lipschitz update without reciprocal collision gaps.

Updating a reachable representative produces another reachable state; quantization then stays within its stated domain. The finite recurrence includes all earlier errors. It does not secretly recover the exact prefix at each checkpoint. On the lower-bound side, every causal label is also a checkpoint message, and the exploration laws at different checkpoints are restrictions of one common law. Taking the maximum of the checkpoint lower bounds is legitimate.

The result concerns a fixed finite horizon. The codebooks can depend on the known calibration and budget, and the clock, calibration and fixed real-valued program are read-only under the resource definition. This is not a claim of a calibration-blind filter, uniform-in-horizon constants, or a finite-bit bound on the complete stored program and arithmetic workspace. The scope table states these distinctions and deserves credit. Known finite-window POMDP approximation results such as [R6] address a different resource and stability regime; their existence does not on its own settle the finite-label collision law here.

**Disposition of this audit:** no blocking defect was found in this inspected proof spine. This is not a formal verification certificate for every downstream result in the manuscript.

## 8. E20.3 and E20.4 — significance and mathematical architecture

### E20.3: the additional exact-kernel theory does not by itself carry the journal case

The chart theorem resolves a real issue. But, once the correct finite product quotient is identified, its central proof is orthogonal projection followed by the elementary nonvanishing principle for polynomials. The block classification is polynomial interpolation on a finite set; the history-rank corollary is normalization followed by an inverse chart. These are useful and correctly assembled conclusions. They are not, on the evidence presently supplied, an independent advance of the scale implied by the requested publication standard.

The same distinction applies to the general structural exponent law: determining the actual image dimension and transferring bounded-format covering and positive local mass to a fixed-horizon finite-label exponent is useful. A dimension exponent is nevertheless not a uniform multiscale classification. The monomial collision theorem supplies the latter in a special class, and the affine theorem supplies a whole-class one-step profile. The manuscript appropriately keeps those assertions separate. It should not ask the sheer breadth of their juxtaposition to substitute for demonstrating why their synthesis solves a central mathematical problem.

In my assessment, the principal collision theorem is the place to make that case. What is special is not that a finite-dimensional set has a covering law or that a positive Bayes update is locally Lipschitz. It is the compatibility of complete acquired flags, the global attainable geometry, and one causal realization at degeneracy. A revision should expose exactly which implication in that compatibility is new, what previously unavailable conclusion it produces, and why that conclusion matters beyond the chosen model and resource convention. The current introduction states the compatibility accurately but does not yet persuade me of the required level of significance.

This is an evaluative objection, not a demand for an unrelated grand theorem. Adding progressively broader wording, another version number, or further finite examples would not answer it. A clearer and mathematically stronger demonstration of the central contribution might; no particular auxiliary result or checklist guarantees a different journal recommendation.

### E20.4: preservation history and submission architecture are different obligations

The collision-first reordering and the scope table are genuine improvements. It would be unfair to describe v20 as lacking either. Nevertheless, the source entry point still carries successive affine, attainable, intrinsic, structural, circular, ambiguity and effective developments, with several earlier special-case proofs retained in the compilation. The author's receipt reports 111 pages. I have not conducted a page-by-page typography audit, and the page count alone is not a criticism. The issue visible in the source is the burden imposed by the layered logical architecture.

A journal submission should make it easy to locate the single main statement, its minimal dependency chain, and the status of the other results as essential ingredients, consequences, or genuinely independent theorems. Historical source preservation is valuable for this repository. Byte-identical preservation of every earlier compiled proof is not, by itself, a mathematical reason for maintaining every earlier route in the journal narrative.

No correct content needs to be silently deleted. Historical versions can remain immutable in the repository, while a carefully organized complete appendix preserves technical material and the submitted argument is arranged by logical dependence. The existing table of model scopes is not a replacement for that proof hierarchy. Nor should reorganization alone be advertised as having resolved the significance objection.

## 9. Concrete disposition for a subsequent revision

**Required mathematical clarification:** correct the dimension-free feasibility reference in E20.1, including the zero-dimensional convention. This does not require weakening `thm:exact-kernel`.

**Required contribution comparison:** explain the finite unconstrained maximum-rank/matroid-intersection specialization in E20.2 and distinguish it from the constrained compact-space result. Retain the already correct attribution of the universal positive-diagonal criteria.

**Recommended explanatory improvement:** include the square moving-kernel example, or an equally informative example, to show that the generic-minor test is genuinely stronger than feasibility, closure and a dimension count together. It must be presented as evidence supporting the criterion, not as a defect in the current theorem.

**Principal editorial obligation:** make the contribution case around the strongest collision/causal theorem and organize its proof hierarchy accordingly. Merely appending a new theorem to answer each paragraph of a report is not an adequate route to a coherent four-journal submission. The local exact-kernel result should retain its correct scope; it should not be promoted into an unproved global resolution theorem.

The recommendation is rejection at the requested tier, not conditional acceptance after these mechanical corrections. Equally, it is not a verdict that the programme is impossible, that all its mathematics is wrong, or that the paper has no publishable content.

## 10. Executed diagnostics and reproducibility limits

The accompanying `independent_checks.py` imports no author or repository theorem code and uses exact rational and symbolic arithmetic. It uses explicit exceptions, not removable Python `assert` statements. Execution with Python 3.13.5 and SymPy 1.14.0 passed **119 cases and 399 explicit checks**. A second execution under `python -O` produced an identical receipt.

| Diagnostic group | Cases | Explicit checks |
| --- | ---: | ---: |
| Square pencil with a varying kernel, including the symbolic family | 56 | 117 |
| Root-saturated balanced-block witnesses and physical ranks | 42 | 168 |
| Containment versus exact-kernel regressions | 2 | 4 |
| Constrained local density chart and exact-kernel tilts | 5 | 21 |
| Zero-dimensional conventions | 2 | 2 |
| Leja/Newton identities, including exact collisions | 6 | 46 |
| Finite Cauchy–Binet/common-independence checks | 6 | 41 |
| **Total** | **119** | **399** |

Reproduce with:

```sh
python independent_checks.py --output CHECK_RESULTS.json
python -O independent_checks.py --output CHECK_RESULTS_OPTIMIZED.json
```

The counts denote explicit test predicates, not independent theorems or exhaustive parameter coverage. The code does not optimize over all possible encoders, prove a semialgebraic entropy theorem, or replace the analytic acquisition argument.

The author receipt `validation/EXECUTION_REPORT.json` reports ten suites, 86,056 assertions, a successful inverse-source mutation check, three TeX passes, 114 compiled proof blocks, 117 compiled statement blocks and a 111-page PDF. I independently checked that GitHub workflow run `34078020936` is recorded as completed/successful, with input commit `28808c05820e288f65b4ba75aaf0d7fd64749e0d`. The reviewed commit `6f103ad252d7c65f140720f4095585026f7bb1b9` is the subsequent published-source/artifact commit. This corroborates the existence and status of the author run; it is not an independent rerun of those suites, the mutation test, or the LaTeX build.

No repository manuscript, historical report, CI configuration, branch protection, permission, or pull-request state is changed by this report. Its publication is confined to a new review branch descending from the pinned submission.

## 11. Primary-source comparison record

These references identify the limited comparisons actually used in this report. They do not amount to an exhaustive novelty search.

**[R1]** T. Terao, *Faster Approximate Linear Matroid Intersection*, SWAT 2026, LIPIcs 370, Article 39, pp. 39:1–39:19, DOI `10.4230/LIPIcs.SWAT.2026.39`. Page 39:2 states the symbolic diagonal common-base determinant criterion; that page was inspected as a rendered PDF page as well as in the extracted text. Primary source: `https://drops.dagstuhl.de/storage/00lipics/lipics-vol370-swat2026/LIPIcs.SWAT.2026.39/LIPIcs.SWAT.2026.39.pdf`.

**[R2]** N. J. A. Harvey, *Algebraic Algorithms for Matching and Matroid Problems*, SIAM Journal on Computing 39(2) (2009), 679–702, DOI `10.1137/070684008`. The publisher's record was checked for the older algebraic matroid-intersection background. No uninspected theorem number from this paper is relied upon. Primary record: `https://epubs.siam.org/doi/10.1137/070684008`.

**[R3]** Y. Zhang and J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, arXiv `2311.05116`, version 4, Lemma 2.18. Primary source inspected: `https://arxiv.org/html/2311.05116v4`.

**[R4]** G. Comte and I. Halupczok, *Motivic Vitushkin invariants*, arXiv `2206.15412`, version 2, introduction, equations (4)–(5), including its explicit reference to the classical real entropy inequality. Primary source inspected: `https://arxiv.org/html/2206.15412v2`.

**[R5]** D. Batenkov, B. Diederichs, G. Goldman and Y. Yomdin, *The spectral properties of Vandermonde matrices with clustered nodes*, arXiv `1909.01927`. The abstract's rectangular unit-circle clustering regime was checked; no claim is made here to have reverified all its spectral theorems. Primary source: `https://arxiv.org/abs/1909.01927`.

**[R6]** A. D. Kara and S. Yüksel, *Near Optimality of Finite Memory Feedback Policies in Partially Observed Markov Decision Processes*, Journal of Machine Learning Research 23(11) (2022), 1–46. The stated finite-window/filter-stability comparison is taken from the authors' journal abstract, not identified with a cardinality-constrained collision law. Primary source: `https://jmlr.org/papers/v23/20-1152.html`.
