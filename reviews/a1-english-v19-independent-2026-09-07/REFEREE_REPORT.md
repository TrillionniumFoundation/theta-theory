# Independent referee report on A1 English v19

**Manuscript:** *Attainable information geometry in positive experiments*, Qian Qi.  
**Submission examined:** `01abeb689b203ea871b88495d16a826bb4942e16`.  
**Source branch:** `revision/a1-english-v19-rectangular-and-degeneration-2026-09-07`.  
**Manuscript directory:** `papers/A1-english-v19/`.  
**Controlling previous report:** `reviews/a1-english-v18-independent-2026-09-07/REFEREE_REPORT.md`, committed at `e5fff530c95a4f3aa1163a2087838ff2795f052b`, reviewing v18 submission `be8effe038608bef255fa97318a9ee3b4434af2d`.  
**Date:** 7 September 2026.  
**Requested publication standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica.

This is an owner-requested, AI-assisted external-referee-style assessment, not a journal-commissioned report or an assertion of editorial appointment. The recommendation concerns the pinned A1 submission, not the entire repository or the eleven-paper programme. Stable source labels are used instead of unverified compiled theorem or page numbers.

## 1. Recommendation and mathematical disposition

**REJECT for the requested four-journal standard.** The decisive issue remains the mathematical weight of the contribution, reassessed here using the actual v19 additions rather than by repeating the previous verdict. There is also a concrete, correctable scope error in the description of the rectangular kernel result. Section 4 gives a complete counterexample to the stronger exact-kernel reading of the introduction and response letter.

**The distinction is important:** the counterexample does **not** refute `thm:v19-rank-alternative` as printed. That theorem asserts containment in a kernel, together with attainment of the minimum rank. Those assertions survive inspection. I found no blocking counterexample or essential missing argument in the ten new formal results under their stated hypotheses. This is an assessment of the proofs examined, not formal verification of the entire inherited manuscript.

The revision has made genuine progress. It supplies a rectangular criterion without assuming a square reduction, an informative physical five-point example, a fixed experiment realizing arbitrary sufficiently small covariance matrices, and a uniform analytic-arc memory law. It also makes the finite matrix predecessors explicit. It would be inaccurate to say that v19 only adds another scalar cancellation, or that the old attribution objection remains unanswered.

Nevertheless, the new rectangular mechanism is finite-dimensional moment separation and its kernel-containment consequences. The local covariance construction is an elementary orthogonal-product density perturbation. The analytic-arc law then composes the already established affine theorem with classical determinantal orders and an elementary finite envelope. The resulting statements are useful and correctly connected to the physical model. In my judgment, their cumulative conceptual and mathematical depth does not yet establish the case for the four journals specified above.

That judgment does not erase the strongest inherited contribution: the collision-uniform conjunction of actual acquisition mass, global approximation, and gap-free causal updating. Nor does it mean that elementary proofs cannot support an important paper. The issue is the significance of the conclusions obtained from them in this submission. Another referee may assign more weight to that synthesis; the present editorial assessment is not a theorem about the paper's possible importance.

## 2. Scope and source basis

The new mathematics was read in full in `sections/rectangular_attainment.tex` and `sections/covariance_degenerations.tex`, including all ten statement/proof pairs and both displayed physical examples. The response letter, the relevant introduction, main input structure, and the v19 bibliography additions were examined. The main affine classification, its projective-law and thick-set quantization proofs, the operational integer-envelope argument, the opening general structural-rank chain, and the principal collision checkpoint/streaming chain were also inspected. The preceding v18 report was used to identify the controlling issues, not as a substitute for reading the revised arguments.

This is not an assertion that all 109 advertised proof blocks, every circular or uncertainty argument, every numerical compiler routine, or every appendix has been independently reverified in this turn. The build source was inspected, but the author validator, source-preservation mutation, full LaTeX build, and CI were not rerun. The reported manuscript size and preservation counts are author-side claims unless otherwise indicated below.

The scope of the mathematical model also matters. The horizon is fixed and finite; the prior and physical interface are known for code design; future queries are selected after the retained label is formed. Persistent labels are charged, while the fixed program and specified read-only information follow the manuscript's resource convention. The new covariance law is a one-acquisition-step law. The analytic classification is arcwise, not a simultaneous multiparameter Smith form or a finite-data procedure for estimating unknown orders. These are printed qualifications, not omissions invented by this report.

## 3. Disposition of the v18 report

| Previous concern | Disposition in v19 |
| --- | --- |
| E18.1: precise predecessor for the finite square-pairing criterion | **Resolved in substance.** Banaji–Pantea is now explicitly identified, with the relevant definition and lemma. |
| Novelty of finite rectangular positive-diagonal algebra | The new section proactively cites Müller et al. The finite sign-vector mechanism is not presented as an independently new algebraic input. |
| The existing full-support degeneration example was only scalar | **No longer a valid description of the revision.** The fixed sign-cube construction realizes arbitrary small rectangular matrices and scaled analytic matrix germs. |
| Lack of a rectangular counterpart beyond the square hypothesis | **Substantively answered.** A compact-space product-cone alternative and a physical obstruction to a fixed evidence-preserving square subpairing are proved. |
| Four-journal significance | Reassessed below. A substantive mathematical response does not by itself settle an editorial significance judgment. |
| Standalone preparation and historical inverse-source anchoring | Source inspection shows that `prepare()` calls `verify_history()` before copying the baseline, and that the latter checks pinned v18 and v17 manifests, including the inverse source. The advertised repair is visible in code; its execution was not independently repeated here. |

For [R1], the finite square specialization concerns the determinant of a positive-diagonal weighted pairing. Their strong-compatibility condition and rank alternative supply the existing finite criterion after transposition and normalization of weights. For [R2], take the set in Lemma 2.1 to be the nonzero evaluation vectors of the smaller function space. These comparisons now have the right mathematical location. They should not be reopened as though the revision had ignored them.

## 4. E19.1 — containment is not exact kernel realization

**Classification: a substantive but repairable statement-of-scope error; not a counterexample to the printed theorem.**

The introduction says that `thm:v19-rank-alternative` identifies “all possible kernel subspaces.” The response letter says that “Each permitted kernel is realized” by a full-support mixture. The formal theorem proves instead

\[
\exists\mu\text{ of full support with }U\subseteq\ker H_\mu
\quad\Longleftrightarrow\quad
0\in\operatorname{ri}K_U.
\]

It obtains equality with the specified subspace when that subspace has **maximal permitted dimension**. It does not obtain equality for every subspace satisfying the displayed relative-interior condition. Describing every such subspace as an exactly realizable kernel is false.

### 4.1 An eight-point counterexample

Let

\[
X=\{1,2,3,4\}\times\{-1,1\}
\]

with the discrete topology. Write a point as \((j,\sigma)\). Let \(e_j\) be the indicator of the two-point block with first coordinate \(j\), and put

\[
E=\operatorname{span}\{e_1,e_2,e_3,e_4\},\qquad
F=\operatorname{span}\{1,\sigma,j\sigma\},\qquad
U=\operatorname{span}\{\sigma\}.
\]

These are spaces of continuous functions with dimensions \(4\), \(3\), and \(1\), respectively. Both \(E\) and \(F\) contain the constant function. Thus the example is genuinely rectangular and does not exploit the absence of evidence from either space.

For an arbitrary full-support probability let

\[
p_{j,+}>0,\quad p_{j,-}>0,\qquad
s_j=p_{j,+}+p_{j,-},\quad d_j=p_{j,+}-p_{j,-}.
\]

In the displayed bases the pairing matrix is

\[
H_\mu=
\begin{pmatrix}
s_1&d_1&d_1\\
s_2&d_2&2d_2\\
s_3&d_3&3d_3\\
s_4&d_4&4d_4
\end{pmatrix}.
\]

The condition \(U\subseteq\ker H_\mu\) is exactly \(d_1=\cdots=d_4=0\). Under that condition the third column vanishes as well. Since every \(s_j>0\), the matrix has rank one and

\[
\ker H_\mu=\operatorname{span}\{\sigma,j\sigma\}.
\]

Consequently **no full-support probability has kernel exactly \(U\)**.

On the other hand, the product-evaluation vectors for \(U\) are the eight vectors \(\pm\mathbf e_j\) in \(\mathbb R^4\). Their convex hull is the full-dimensional crosspolytope, and zero is in its interior. The uniform probability, assigning mass \(1/8\) to every point, is an explicit full-support witness. Thus the relative-interior condition in the formal theorem holds, while the stronger exact-kernel conclusion fails.

This does not contradict the minimum-rank formula. In this example the minimum rank is one, the maximum permitted nullity is two, and a subspace of that maximal dimension is realized exactly. The distinction between an arbitrary contained subspace and an entire kernel is the whole point.

### 4.2 The example also fits a positive physical interface

The issue is not confined to an irrelevant abstract pairing. Take three acquisition features

\[
f_i(j,\sigma)=\frac16\mathbf1_{\{j=i\}},\quad i=1,2,3,
\qquad
L_y(u,j,\sigma)=\frac12\left(1+y\sum_{i=1}^3u_if_i(j,\sigma)\right),
\]

with \(u\in[-1,1]^3\). All likelihoods are at least \(5/12\). At \(u=0\), the history product and command derivatives span \(E\). Use the two fixed query probabilities

\[
g_1(j,\sigma)=\frac12+\frac\sigma4,\qquad
g_2(j,\sigma)=\frac12+\frac{j\sigma}{16}.
\]

Both belong to \([1/4,3/4]\), and their augmented test space is \(F\). Thus positivity, a finite physical query menu, and the evidence direction do not repair the exact-kernel assertion.

### 4.3 Required correction

The introduction and response should say that the theorem characterizes **subspaces that can be contained in a pairing kernel**, and constructs priors attaining the **minimum rank**. The maximal-dimension equality should remain explicit. This change preserves every correct formal statement and proof.

To retain an exact-kernel classification for arbitrary \(U\), an additional condition is necessary. On the moment slice imposing \(H_\mu U=0\), the induced map on \(F/U\) must have rank \(k-\dim U\); equivalently, some maximal minor of that induced map must be nonzero at an admissible full-support moment. The relative-interior condition for the annihilation equations alone does not impose this requirement. Merely repeating the convex-hull argument does not supply it.

## 5. Audit of the ten new formal results

### 5.1 Full-support moments and rectangular alternatives

`lem:v19-moment-image` is correct as inspected. A proper supporting affine functional has strictly positive integral under a full-support probability if its pullback is nonnegative and nonzero somewhere. This rules out a relative-boundary mean. Conversely, for an interior target mean, a sufficiently small mixture with a fixed full-support probability leaves a residual mean inside the convex body; finite-dimensional convex representation supplies the stated atomic residual. The mixture weight need not be uniform, and the text correctly says so. An interior moment need not have only full-support representations.

`thm:v19-rectangular` follows by applying this moment-image identity separately to each nonzero function in the smaller space. The multiplier formulation follows from separation, with strict positivity somewhere rather than everywhere. Integrating that nonnegative nonzero product under full support supplies the contradiction. No single common multiplier is required for all functions, and no fixed square subpairing is assumed.

`thm:v19-rank-alternative` correctly applies the same moment identity to all products \(u_i e_a\) simultaneously. The maximum permitted dimension exists because the set of possible dimensions is a nonempty subset of a finite set of integers. A witness for a maximal-dimensional permitted subspace cannot have a still larger kernel. These observations justify the minimum-rank formula and its actual attainment, subject to the scope correction in Section 4.

### 5.2 Quantitative margin and positive-history consequence

`prop:v19-dominated-margin` has the correct optimization order. For fixed unit \(f\), writing \(\mu=c\mu_0+(1-c)\nu\) fills the translated convex body \(ca_f+(1-c)K_f\). Minimization over the unit sphere and probabilities can be interchanged. Compactness and the universal full-column-rank property give a positive minimum. Full support without domination would not imply the claimed uniform margin; domination is present in the statement.

The compact-family qualification also matters: dimensions and continuous bases are fixed, and the universal criterion holds at every parameter. In that setting the relevant parameter-measure product is compact. The simple check \(E=F=\operatorname{span}\{1,x\}\) on \(X=\{-1,1\}\) gives the exact margin \(c\): the pairing is \(\left(\begin{smallmatrix}1&m\\m&1\end{smallmatrix}\right)\), domination gives \(|m|\le1-c\), and its least singular value is \(1-|m|\).

`cor:v19-rectangular-history` correctly adjoins the evidence direction before normalization. If \(L:T\to\Phi^*\) is the moment pairing and \(Y=LP=(Z,Zp)\), normalization kills exactly \(\mathbb RY\). Since \(\operatorname{im}L=\mathbb RY+L(\operatorname{im}DP)\), the actual command derivative has rank \(\operatorname{rank}L-1\). There is no assumption that the radial direction is a physical command derivative.

The mass conclusion uses an output projection completed by kernel coordinates, an inverse chart, and integration over the whole kernel-coordinate box. Multiplication by the word probability retains unconditional mass. The proof does not place probability on a section of zero ambient measure. Its uniform version has the required common likelihood, density, interior-neighborhood, derivative, domination, and fixed-dimension assumptions. The rank-zero case is not claimed to produce positive-dimensional mass.

### 5.3 The five-point physical example

`prop:v19-pentagon` is correct. All twenty displayed separator values were checked exactly. A nonconstant affine function of the ordered values \(h=0,1,2,3,4\) changes sign at most once, so the four separators supply the multiplier condition; weak-sign and zero cases cause no exception.

The evidence-preserving square obstruction is especially transparent. For a prospective direction \(ax+by\), let the consecutive increments be

\[
g_0=2a,\quad g_1=a+b,\quad g_2=-2a+2b,\quad g_3=-2a-2b.
\]

The identity \(2g_0+g_2+g_3=0\) forces \(g_0=g_2=g_3=0\) whenever all increments are nonnegative. Hence \(a=b=0\); reversing signs handles the antitone case. The square determinant criterion therefore cannot hold for a nonconstant direction. The qualification **containing evidence** is essential and is correctly printed. The example should not be advertised as excluding every conceivable square reformulation.

The likelihood and query bounds are valid. The nonzero row covariance and the inherited affine theorem give its one-step memory profile. This is a useful example, not merely an arbitrary rectangular matrix.

### 5.4 Covariance realization

`thm:v19-covariance-realization` is correct as inspected. Under the uniform sign-cube law, the products \(\xi_i\zeta_j\) are centered and orthonormal. Thus the density

\[
1+\sum_{j,i}A_{ji}\xi_i\zeta_j
\]

has integral one, retains zero individual sign means, and gives cross moments \(A_{ji}\). The entrywise absolute-sum bound places the density between \(1/2\) and \(3/2\). With the printed acquisition scaling and square-root query weights, the covariance is exactly \(A/(8b\sqrt q)\), not \(A/(8bq)\). The fixed likelihoods are bounded below by \(1/4\).

The prior map is affine and injective because its displayed cross moments recover all coefficients. Scaling a bounded analytic matrix germ into the prescribed entrywise ball therefore preserves every determinantal rank locus. This is an actual fixed experiment with a fixed query menu, not an abstract spectrum declared attainable after the fact.

### 5.5 Analytic orders, joint law, and phases

`lem:v19-analytic-orders` uses a valid one-variable analytic elimination argument. A minimal-order nonzero entry divides all entries in the convergent power-series ring after its unit is removed. Row and column operations preserve this divisibility in the remaining block. Iteration gives nondecreasing pivot orders and analytic invertible multipliers. Cauchy–Binet in both directions identifies the minor ideals, and bounded multipliers and inverses give two-sided singular-value comparisons. Rectangular zero padding and identically zero directions are handled correctly. The classical invariant-factor/singular-value connection is expressly attributed to [R3].

`thm:v19-analytic-memory` follows from the affine theorem with constants independent of the prior and its nonzero singular values. For a fixed analytic germ, bounded Smith multipliers give constants independent of both the small arc parameter and the integer memory budget. The endpoint is evaluated with the affine theorem at the endpoint prior itself, not by interchanging a limit with optimization over encoders. If the endpoint covariance vanishes, one label is exact for this affine query task. This is not the stronger and generally false assertion that every zero-rank finite-report task is a singleton.

`cor:v19-memory-phases` is also correct as inspected. With \(A_\ell=\sum_{j\le\ell}\alpha_j\), the maximum of powers of \(t\) selects the smallest exponent. The ceiling in \(M=\lceil t^{-\gamma}\rceil\) changes only constants. Adjacent transition values are

\[
\beta_\ell=\ell\alpha_{\ell+1}-A_\ell,
\qquad
\beta_{\ell+1}-\beta_\ell=(\ell+1)(\alpha_{\ell+2}-\alpha_{\ell+1})\ge0.
\]

This justifies chaining adjacent comparisons, including tied orders and intervals of length zero. The inverse transform uses the full unbounded integer-budget curve. Its zero values beyond the generic rank follow from the large-budget limit, not from a finite list of evaluations.

The non-diagonal example has determinant \(t^6/256\), orders \((1,5)\), and risk comparable to \(\max(t^2M^{-2},t^6M^{-1})\). The transition is \(M\asymp t^{-4}\). All these calculations agree with the text.

## 6. E19.2 — novelty and significance after the additions

**Classification: publication-decisive editorial assessment, distinct from E19.1.** Correcting the exact-kernel language would not by itself change the recommendation.

### 6.1 Rectangular generality is real, but its mechanism should be described at its actual level

The compact-space rectangular criterion is a genuine extension of the presentation in v18. It should receive credit for actual full-support witnesses and its posterior-history interpretation. Its proof, however, passes through one finite-dimensional moment-image identity and elementary separation. The minimum-rank formula optimizes the dimensions of subspaces for which simultaneous annihilation is feasible; it does not furnish a structural classification of exact kernels. The counterexample in Section 4 demonstrates that the latter description would be stronger than what is proved.

The quantitative margin is an exact reformulation of an infimum over priors and unit vectors, followed by compactness. It is not a new estimate that remains effective without the stated dominated envelope. The history corollary reuses the normalization and positive-mass mechanism already central to v18. The pentagon example is informative, but it does not turn the general convex feasibility formulation into a new taxonomy of experiment geometries.

None of these observations is a proof defect. They locate the intellectual advance more narrowly than a count of six additional results would suggest.

### 6.2 The covariance construction has a classical orthogonal-expansion baseline

The elementary Fourier expansion on a finite cube identifies coefficients by inner products with product characters; see [R4, Section 2.2, equation (1)]. Applying that basis to a density and retaining only selected cross terms gives the construction used here. Positivity in an absolute-sum ball follows directly from the triangle inequality. This is the relevant baseline for the density-realization step, rather than an unspecified difficult moment-realizability problem.

The manuscript's contribution at this point is the choice of fixed positive acquisition and query functions, their physical scaling, and coupling the resulting covariance to its proved memory theorem. I do not claim that [R4] contains that experiment-level conclusion or the manuscript's regret law. Nor is this a second allegation comparable to the previously missing finite square theorem. It is an assessment of how much new mathematics the realization mechanism itself contributes.

The arbitrary-germ statement is useful, but it inherits its generality from the ability to install any small matrix of cross coefficients into an otherwise unconstrained sign-cube construction. Realization of every ordered list then uses a diagonal matrix with the desired powers. Once the local realization and affine profile are available, this does not impose or resolve an additional restriction on possible phase orders.

### 6.3 The analytic law is a clean consequence, not an independent new normal-form theory

The arc theorem composes three ingredients: the manuscript's affine forward classification, classical one-variable determinantal orders, and a maximum of finitely many power laws. Its uniformity in the memory budget is genuine because the affine comparison constants survive covariance rank loss. Its treatment of zero directions is also useful.

Still, the strongest new assertion is confined to one acquisition step and a fixed analytic arc. It does not resolve anisotropic degeneration of arbitrary polynomial history images, or compatibility of such local arc descriptions with multi-step causal compression in the general structural class. The manuscript explicitly does not claim those stronger results, and their absence is not being called a gap. It simply means that those stronger interpretations cannot support the significance case for the result that is actually proved.

A new paper need not solve every adjacent problem. Equally, attaching the words “all phases,” “arbitrary germs,” or “complete classification” to a direct consequence does not by itself establish the magnitude of a four-journal advance. The mathematical content of the generality, rather than the breadth of those phrases, is what must be evaluated.

### 6.4 The inherited collision synthesis remains the strongest part

The principal collision chain examined here still has to coordinate three different tasks. Complete Newton–Hermite prefixes must be acquired by actual positive histories with unconditional mass. The entire reachable image, rather than only a local chart, must admit a dimension-truncated anisotropic cover. Finally, raw-moment transitions and reachable representatives must propagate approximation error without reciprocal collision gaps or an uncharged command tape.

The inspected proof architecture addresses these separately. The bounded triangular Newton conversion and maximal Vandermonde products are not substituted for the acquisition proof. Bounded-format whole-image geometry is used for the upper cover. The raw update has a positive evidence denominator on posterior-mixture segments, and the finite causal recurrence includes accumulated earlier errors. This conjunction deserves substantially more credit than a statement that the paper merely computes a Vandermonde determinant.

I have not identified a source that simply contains this entire combined law in the specified physical model. Nevertheless, in the submitted architecture the accumulation of general rank reductions, explicit model classifications, inverse-envelope consequences, prior uncertainty, and numerical-resource appendices does not yet establish, in my judgment, an advance of the required depth and consequence. This is the editorial reason for rejection. It is not an assertion that every component is already known, or that a correct proof must be technically complicated to matter.

## 7. Presentation and revision obligations

The report does not prescribe a new sequence of small additions as a route to automatic acceptance. In particular, the previous request for a structural extension has been answered; it would be unfair to pretend otherwise. A future submission should address three concrete matters.

First, make every statement about kernels agree with the proved containment theorem, or add and prove the genuinely stronger exact-kernel criterion. The eight-point example should be used as a regression test for the language and any stronger assertion.

Second, distinguish the elementary separation, product-character perturbation, and classical determinantal-order inputs from the experiment-level consequences. The finite-square attribution has already been repaired. The next contribution statement should explain what the combined results establish that is not supplied by these inputs alone, without counting routine consequences as separate conceptual breakthroughs.

Third, give the paper a clear mathematical center. The strongest collision/causal synthesis should be connected explicitly to the broader structural and affine results, with a concise table of which hypotheses, uniformities, and resource conventions each result uses. This is an organizational request, not a demand to discard valid proofs or delete historical material. Repository preservation records can remain complete without making the main narrative a chronological response ledger.

These corrections are necessary for accurate communication. They are not a promise of acceptance at any particular journal. The significance judgment requires a persuasive case for the mathematics already achieved, not simply another passing checklist.

## 8. Independent calculations and reproducibility

The accompanying `independent_checks.py` was executed locally with Python 3.13.5 and SymPy 1.14.0. It imports no repository code and requires no network. Its actual output is `INDEPENDENT_CHECK_RESULTS.json`.

**Executed result: nine suites, 2,445 exact checks, all passed.** The suites cover the symbolic eight-point kernel counterexample and a positive physical realization; the pentagon separators and square obstruction; symbolic Walsh covariance identities and finite physical-bound examples; non-diagonal rectangular minor orders and zero endpoints; phase-envelope branches for 125 ordered integer lists; integer-budget envelope witnesses; a dominated-margin example; the projective evidence/Jacobian exponent; and finite Leja volume checks including exact repetitions.

These counts count explicit check calls, not distinct theorems. The symbolic and rational calculations are diagnostics. Finite positivity examples do not replace the universal triangle-inequality proof. Finite Leja configurations do not prove uniform attainable transversality. Checking several rectangular matrix arcs does not replace the analytic Smith argument. No optimizer over all encoders or formal proof assistant was used.

The source SHA-256 of the executed script is

`beb1cedbff2e5d6a6de6ecdf79a3b7b8012bdccc3d48b4b36501b5aa8c778350`.

Reproduce with:

```sh
python -m pip install sympy==1.14.0
python independent_checks.py --output INDEPENDENT_CHECK_RESULTS.json
```

The execution duration in a regenerated receipt may differ. The author validator, source-preservation mutation, full PDF build, and CI were not rerun. Source inspection of `build.py` supports the specific standalone anchoring repair; it does not independently establish every claimed historical digest or execution receipt. Build success, source preservation, mathematical validity, novelty, and editorial importance are separate assertions.

## 9. Source anchors and primary literature

All repository paths below refer to the pinned submission identified at the beginning of this report. The accompanying manifest records the retrieved source blobs and the review's limits.

**S1.** `papers/A1-english-v19/sections/rectangular_attainment.tex`: `lem:v19-moment-image`, `thm:v19-rectangular`, `thm:v19-rank-alternative`, `prop:v19-dominated-margin`, `cor:v19-rectangular-history`, `prop:v19-pentagon`.

**S2.** `papers/A1-english-v19/sections/covariance_degenerations.tex`: `thm:v19-covariance-realization`, `lem:v19-analytic-orders`, `thm:v19-analytic-memory`, `cor:v19-memory-phases`, and the final non-diagonal example.

**S3.** `papers/A1-english-v19/sections/affine_geometry.tex`: the physical covariance definition, `thm:v18-affine-classification`, `lem:v18-projective-law`, `lem:v18-thick-linear`, and `cor:v18-affine-invariant`.

**S4.** `papers/A1-english-v19/sections/operational_reconstruction.tex`: `lem:integer-envelope-duality` and `thm:operational-reconstruction`.

**S5.** `papers/A1-english-v19/core/06b_collision_geometry.tex`: `lem:leja-scales`, `lem:newton-attainment`, `thm:intrinsic-checkpoint`, `thm:intrinsic-streaming`, and the collision-tree argument; read as the principal inherited chain, not as certification of every appendix dependency.

**S6.** `papers/A1-english-v19/sections/introduction.tex`, subsection *Rectangular attainment and realizable degenerations*, and `RESPONSE_TO_REFEREE.md`, subsection *Rectangular universal attainment, not an assumed square reduction*: the exact-kernel scope issue in Section 4.

**S7.** `papers/A1-english-v19/build.py`: `verify_history()` and its call before baseline copying in `prepare()`.

**R1.** M. Banaji and C. Pantea, *Some results on injectivity and multistationarity in chemical reaction networks*, SIAM Journal on Applied Dynamical Systems 15 (2016), 807–869. DOI: [10.1137/15M1034441](https://doi.org/10.1137/15M1034441). The inspected [arXiv v6 text](https://arxiv.org/html/1309.6771v6) includes Definition 2.5, Definition 2.24, and Lemma 2.36. In particular, its strict compound-sign notation means common weak sign with a nonzero entry, not positivity of every entry.

**R2.** S. Müller, E. Feliu, G. Regensburger, C. Conradi, A. Shiu, and A. Dickenstein, *Sign conditions for injectivity of generalized polynomial maps with applications to chemical reaction networks and real algebraic geometry*, Foundations of Computational Mathematics 16 (2016), 69–97. DOI: [10.1007/s10208-014-9239-3](https://doi.org/10.1007/s10208-014-9239-3). Inspected [arXiv v2 text, Lemma 2.1](https://arxiv.org/html/1311.5493v2).

**R3.** K. Kaveh and P. Makhnatch, *Invariant factors as limit of singular values of a matrix*. Inspected [arXiv:1811.07706v2](https://arxiv.org/html/1811.07706v2), Theorem 1.1 and Section 6, including Lemma 6.1 and the convergent power-series argument. The comparison concerns the classical matrix-order input, not a claim that this source proves the manuscript's physical memory theorem.

**R4.** R. de Wolf, *A Brief Introduction to Fourier Analysis on the Boolean Cube*, author-hosted [full text](https://homepages.cwi.nl/~rdewolf/publ/other/fourier.pdf), Section 2.2, printed page 2, equation (1). The product-character orthonormality and inversion formula were read in the PDF. The density specialization in Section 6.2 is an elementary application of that formula, not an attribution of the whole A1 construction or regret theorem to this source.

## 10. Final assessment

The author has responded substantively to v18. The formal rectangular and covariance additions are mathematically credible within the inspected scope, and the prior attribution issue is resolved. The exact-kernel description is too strong and has a concrete counterexample, while the printed containment theorem remains intact. After giving credit to these additions and to the inherited collision/causal synthesis, I do not recommend publication at the requested four-journal level. The report's negative recommendation is based on contribution and accurate scope, not on a fabricated fatal flaw or a claim that further progress is impossible.
