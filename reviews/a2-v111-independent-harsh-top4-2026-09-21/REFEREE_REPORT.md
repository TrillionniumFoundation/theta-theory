# Independent harsh referee report on A2 revision 111

**Manuscript:** *Recovery of information metrics: contact multiplication and global degeneracy*  
**Reviewed revision branch:** revision/a2-v111-global-degeneracy-boundary-experiment-2026-09-21  
**Reviewed branch head:** f7c55b929c8750a98c9219803863e746968a423d  
**Source-bound mathematical snapshot:** 1e21bcbe1741c9fb67a8b3fabe0f6bc20cfdb559  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v111/paper.tex  
**Principal source blob:** a491bc71bd9114a349bbdfb69765fb028b23047b  
**Controlling preceding referee report:** review/a2-v110-independent-harsh-top4-2026-09-21, commit 043495e949f535554c5540c24b679b4aafa6a31d  
**Verified source-bound workflow:** run 35580711331, status passed  
**Date of report:** 21 September 2026  
**Standard applied:** general-journal standard comparable to Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Recommendation:** **reject in the present form**

This is an owner-requested, AI-assisted external-referee-style assessment. It is not a journal-commissioned report and must not be represented as an editorial decision. I have treated the revision branch as immutable review material and placed this report only on a new isolated review branch.

---

## 1. Executive assessment

Revision 111 is the strongest version of this manuscript that I have seen, and it responds materially to the central objections in the v110 report.

The improvement is not cosmetic. The paper no longer rests its venue-level case primarily on the sharp one-contact threshold obtained by transferring a classical maximal-rank theorem. Instead, it proves a new global statement for the failure locus of several within-contact multiplication spaces:
\[
 \Delta^{(L)}
 =
 \left\{
   (U_1,\ldots,U_L)\in\operatorname{Gr}(c,V_n)^L:
   \sum_{\nu=1}^L U_\nu^2\ne V_{2n}
 \right\},
\]
and claims the exact reduced-set codimension
\[
 \operatorname{codim}\Delta^{(L)}
 =
 \min\left\{
   L\binom{c+1}{2}-(2k-1)+1,\,
   Lc-3
 \right\}.
\]
It also identifies an irreducible common-secant subvariety that realizes the second bound, proves an exact fixed-space criterion for positive native realization with global two-point fibre, and replaces the former computed-contact statistical pipeline by a genuinely direct randomized compression of observed Poisson counts.

These are real advances. In particular:

1. the global codimension theorem is mathematically nontrivial and substantially deeper than the v110 generic-surjectivity theorem;
2. the common-secant family is a concrete geometric obstruction rather than a formal expected-codimension count;
3. the single-contact sharp threshold can now be deduced internally from the global incidence theorem instead of depending on rational-curve maximal rank for the saturated range;
4. the fixed-space realization theorem cleanly separates positivity from the coordinate-sign decomposition obstruction;
5. the statistical section now distinguishes a true direct score compression from the old deterministic re-encoding pipeline;
6. the coalesced-root boundary is explicitly treated as a cone experiment;
7. the source-bound build and preservation workflow is unusually careful.

I did not find a fatal algebraic counterexample to Theorem 1.1 in the scope of this review. I checked the logic of the Hankel-rank stratification, the isotropic Grassmannian dimension count, the rank optimization, the common-secant incidence, the fixed-space sign criterion, and the linear-Gaussian information identity. The finite diagnostics are consistent with the displayed formulas, though of course they do not prove the universal statements.

Nevertheless I still recommend rejection at the stated top-four standard.

The reason is no longer that the main theorem is visibly nonsharp or that the paper lacks a genuine global result. The reason is that the manuscript now reaches a credible specialized theorem, but still does not establish the level of conceptual depth, breadth, or structural completeness expected of a general top-four mathematics paper.

The new global theorem determines **one numerical invariant of the bad locus—its codimension—and one maximal-dimensional component in one regime**. It does not classify the irreducible components, determine the scheme structure, compute degrees or classes, describe generic singularities, or give a conceptual generalization beyond binary forms and quadratic multiplication. The proof is an efficient synthesis of classical Hankel rank geometry, an isotropic incidence count, a simple optimization, a rank-two secant construction, and a general determinantal height bound. That synthesis is good mathematics. It is not yet, in my judgment, a sufficiently broad geometric theory to sustain an Annals/Inventiones/JAMS/Acta claim.

The statistical advance is also valid but narrower than the title-level narrative may suggest. The direct contact-score experiment is built on a **preselected least-favourable local submodel around a known centre with known mark laws**, and the retained statistic is a designed linear score compression of Poisson counts with added jitter. Once the raw local experiment is Gaussianized, the exact information formula and the equivalence criterion are consequences of standard linear Gaussian experiment theory. This is a much better theorem than the old plug-in recoding, but it is not an intrinsic observation model of physical contact measurements, nor a global equivalence result for the original calibrated experiment.

My present assessment is therefore:

- **main algebraic theorem:** plausible and substantial;
- **sharpness:** genuinely achieved;
- **global failure geometry:** substantially improved but incomplete;
- **native realization:** clean and useful, but elementary relative to the venue target;
- **statistical experiment comparison:** correct-looking and carefully qualified, but engineered and local;
- **boundary asymptotics:** coherent, largely standard once the model is set up;
- **structured-family extension:** useful supporting material, not a second deep theorem;
- **proof/reproducibility discipline:** strong;
- **top-four originality/significance:** still not established;
- **recommendation:** reject in the present form.

---

## 2. Scope of this review and source integrity

I reviewed the v111 principal source and its five mathematical parts, the response to R110, the preservation/dependency record, the controlling v110 report, and the source-bound CI receipt.

The current revision head is an evidence-only bot commit. The mathematical source is bound to commit 1e21bcbe1741c9fb67a8b3fabe0f6bc20cfdb559. The CI receipt records a successful four-volume build of v111 together with unchanged v110, v109, and v108 companions. The principal v111 paper is 20 pages and the receipt reports no undefined references, multiply defined references, or overfull boxes.

This is good repository hygiene. It removes the ambiguity that affected much earlier rounds of this project.

However, build success and exhaustive finite arithmetic diagnostics are not mathematical certification. The manuscript itself correctly says this. I likewise do not use the CI success as evidence for universal correctness or originality.

---

## 3. What v111 genuinely closes from R110

Several objections in the preceding report should now be marked as substantially closed.

### 3.1 The paper now has a genuinely global theorem

R110 criticized the failure-geometry section as a first determinantal layer without a global theorem. V111 remedies this. Theorem 1.1 is not merely a tangent-space statement or an expected-codimension assertion. Its proof ranges over all ranks of an annihilating Hankel form, all feasible radical-intersection dimensions, and all contacts simultaneously.

This is a serious improvement.

### 3.2 The common-base-point locus is no longer mistaken for the main obstruction

The manuscript now identifies a larger common-secant family of codimension \(Lc-3\), proves that the old base-point family lies properly inside it for one contact, and explains why the base-point family is not itself an irreducible component.

This is exactly the sort of correction that a good revision should make.

### 3.3 The sharp threshold no longer depends on the classical maximal-rank theorem in the saturated range

The paper still records the classical rational maximal-rank theorem in the appendix, with a more precise specialization to Larson's theorem. But the saturated generic-surjectivity conclusion now follows from the new global codimension theorem itself.

That addresses the main conceptual weakness of v110.

### 3.4 Fixed-space local versus global realization is now classified

Theorem 5.1 gives a clean if-and-only-if statement:

- local positive realization is equivalent to \(JU^\perp\) meeting the positive orthant;
- global two-point fibre is equivalent to the additional absence of invariance under every nonconstant coordinate-sign matrix.

This is stronger than merely intersecting two generic open conditions.

### 3.5 The old statistical recoding is no longer presented as a new observation model

The response explicitly concedes the v110 criticism that
\[
 \text{raw sample}\to\widehat\theta\to\text{computed contact}\to\widetilde\theta
\]
is deterministic re-encoding. That result is moved to an appendix and correctly relabelled.

Section 9 instead constructs a statistic directly from observed counts. This is a genuine conceptual repair.

### 3.6 The boundary interpretation is much cleaner

The paper now distinguishes the two-sided smooth likelihood extension used for differentiation from the physically admissible cone \(v\ge0\). The local Gaussian quotient is parameterized by \(h\in\mathbb R_{\ge0}^k\), and the \(N^{-1/4}\) root-amplitude scale is connected explicitly to the quadratic synchronization map.

This closes the interpretive ambiguity identified in R110.

---

## 4. Correctness audit of the global codimension theorem

This is the mathematical center of v111, and it deserves a careful audit.

### 4.1 Hankel rank strata

For a functional \(\ell\in V_{2n}^*\), the paper considers the symmetric Hankel form
\[
 H_\ell(f,g)=\ell(fg)
\]
on \(V_n\), \(\dim V_n=k\).

The cited classical dimension formula
\[
 h_r=
 \begin{cases}
  2r-1,&r<k,\\
  2k-2,&r=k
 \end{cases}
\]
for the projective exact-rank-\(r\) stratum is consistent with the standard catalecticant/secant description of binary forms. The manuscript is careful to include confluent limits rather than only sums of distinct evaluations.

I have no substantive objection to this step, though a final version should quote the exact proposition/theorem from the cited source rather than ask the reader to reconstruct the identification from two sections.

### 4.2 Isotropic \(c\)-plane dimension count

Let \(E=\operatorname{rad} H_\ell\), \(\dim E=k-r\), and let
\[
 s=\dim((U+E)/E),\qquad a=c-s.
\]
The feasibility range
\[
 \max\{0,c-k+r\}\le s\le \min\{c,\lfloor r/2\rfloor\}
\]
is correct.

The dimension decomposition into:

1. choice of \(U\cap E\);
2. choice of a totally isotropic \(s\)-plane in the nondegenerate \(r\)-dimensional quotient;
3. choice of lifts;

leads to
\[
 D_{r,s}=(c-s)(r-s)+\frac{s(s+1)}2
\]
as the codimension in \(\operatorname{Gr}(c,k)\).

This is coherent. The note about two components of a maximal even orthogonal Grassmannian is appropriate because only dimension is used.

### 4.3 Rank optimization

The key numerical lemma asserts
\[
 L D_{r,s}-h_r
 \ge
 \min\{Lq-2k+2,Lc-3\}.
\]

I do not see an algebraic error in the case split. The exceptional small cases \((L,c)=(1,4)\) and \((1,5)\) are explicitly isolated. The endpoint cases \(s=c-1\) and \(s=c\) are not silently folded into the concavity argument.

This is exactly the kind of elementary but fragile calculation where hidden off-by-one errors often occur; here the displayed arithmetic appears internally consistent.

For a publication-level proof I would nevertheless recommend extracting the optimization into a compact standalone combinatorial proposition, with the feasible polygon drawn or tabulated and the minima identified conceptually. The current case split works, but it obscures why precisely the two competing codimensions \(Lq-p+1\) and \(Lc-3\) emerge.

### 4.4 Common-secant incidence

The common-secant construction is the most geometric part of the proof.

For
\[
 h=\alpha\operatorname{ev}_x+\beta\operatorname{ev}_y
\]
and \(U\subset\ker h\), the relation
\[
 \alpha f(x)=-\beta f(y)
\]
implies that
\[
 \ell=\alpha^2\operatorname{ev}^{(2n)}_x-\beta^2\operatorname{ev}^{(2n)}_y
\]
annihilates every product \(fg\) with \(f,g\in U\).

This is correct and explains the second codimension term geometrically.

The projection-dimension argument is also plausible: for general \(h\), a general \(c\)-plane in \(\ker h\) is not contained in a second secant hyperplane, because the locus admitting another \(h'\) has strictly smaller dimension when \(c\ge4\).

I would still strengthen this part. “Generically one-to-one” is important enough that the exceptional incidence should be defined explicitly and the fibre dimension argument written as a lemma. The current proof is short relative to the role it plays in identifying an actual irreducible component.

### 4.5 Determinantal height bound

After proving generic surjectivity by the incidence lower bound, the manuscript invokes the classical height bound for maximal minors on a Grassmannian chart to obtain
\[
 \operatorname{codim}\Delta^{(L)}\le Lq-p+1.
\]

This is standard and legitimate.

But because the exact equality of codimensions is the headline result, the local algebra deserves one extra sentence: specify the regular coordinate ring on the chosen chart, the size of the matrix, and the exact height inequality being applied to the ideal of \(p\times p\) minors. This would eliminate any concern about silently switching between the global scheme and an affine chart.

### 4.6 Overall correctness of Theorem 1.1

Taken together, the proof architecture is convincing:

- every failure tuple has a projective annihilator;
- annihilators are stratified by Hankel rank;
- all isotropic \(c\)-planes for each rank are dimension-counted;
- the numerical optimization gives the universal lower bound;
- rank-two secants attain one upper bound;
- determinantal height attains the other;
- the bounds match.

I therefore do **not** base my rejection on a discovered fatal flaw in Theorem 1.1.

That is an important difference from earlier rounds.

---

## 5. The central remaining venue-level problem: exact codimension is not yet a global geometry

The paper now repeatedly uses phrases such as “global degeneracy,” “global failure geometry,” and “entire bad set.” These are defensible in the narrow sense that the codimension bound is global over the entire reduced failure set.

But at a top-four level, an exact codimension is only the beginning of a geometry.

The theorem does **not** determine:

- all irreducible components of \(\Delta^{(L)}\);
- which component dominates when the determinantal term \(Lq-p+1\) is smaller;
- whether the determinantal scheme is reduced;
- whether it is equidimensional;
- its degree or Chow class;
- its generic singularity type;
- the intersections among the common-secant component and other components;
- the closure relations among Hankel-rank strata;
- the generic corank on each maximal component;
- the normalization or birational type of the principal components;
- the real topology of the bad set;
- the distribution of distance to the bad set for natural random models.

The manuscript openly acknowledges many of these omissions. That honesty is good. It also reveals the limit of the present result.

In the secant-dominant regime, one maximal-dimensional component is identified. In the determinantal-dominant regime, the theorem gives the dimension of the bad set but does not identify a corresponding geometric component with comparable specificity.

This asymmetry matters. A top-four paper whose main claim is a “global geometry” should ideally explain the geometry producing **both** branches of the minimum, not just the numerical height of the second branch.

The current proof of the \(Lq-p+1\) branch is, at bottom, a general maximal-minor height bound. That is enough for codimension. It is not enough for a structural description.

---

## 6. The common-secant component is elegant but still a rank-two obstruction

The new component is a good idea. It is also geometrically simple.

Its parameter is a point of the secant variety of the rational normal curve, hence essentially a rank-two Hankel functional, together with \(L\) Grassmannians of \(c\)-planes inside the corresponding hyperplane.

This produces the obstruction
\[
 \operatorname{codim}=Lc-3.
\]

The manuscript then optimizes over all higher Hankel ranks to show that no larger-dimensional failure family exists.

That optimization is useful. But the geometric content of the extremizer is still concentrated in a rank-two secant construction.

For a stronger general-journal result, I would want the paper to go beyond “rank two wins the dimension optimization” and explain a more robust principle, for example:

- a classification of maximal components by apolar/Hankel rank;
- a theorem describing which Hankel ranks can produce components rather than embedded subloci;
- a higher-product analogue for \(\operatorname{Sym}^m U\);
- a multigraded or multivariate analogue where the secant geometry is genuinely new;
- a theorem on singularities or degrees of the failure component;
- a deformation-theoretic explanation of the two codimension branches.

Without such a layer, Theorem 1.1 remains a sharp specialized calculation rather than a broad theory.

---

## 7. Originality and literature positioning are still not strong enough

The bibliography improved its attribution of rational maximal rank and Hankel determinantal geometry. But for a paper now centered on **failure loci of quadratic normality/multiplication maps over Grassmannians**, the literature discussion remains too narrow.

There is a substantial classical literature on projective normality, quadratic normality, failure loci/cycles, secant explanations of failure, degeneracy loci, and projections of curves. The current paper cites Ballico–Ellia for maximal rank, Larson, CMSV for Hankel determinantal rings, and general secant/dual references, but it does not make a serious attempt to situate the new failure-locus theorem against the broader failure-cycle and quadratic-normality literature.

At minimum, the authors should explain the relationship to work such as Ballico's papers on failure loci and failure cycles for quadratic normality, and to the Green–Lazarsfeld/projective-normality framework. I am **not** claiming that those papers contain Theorem 1.1. I am saying that the manuscript has not done enough to demonstrate that its exact codimension theorem is genuinely new relative to that surrounding body of work.

For a specialized journal, a precise novelty paragraph may suffice.

For Annals/Inventiones/JAMS/Acta, the authors need a much stronger priority audit:

1. state the closest known degeneracy-locus problem in the literature;
2. state what was previously known about the dimension/codimension of failure;
3. state whether the common-secant component has appeared before in another language;
4. state whether the two-branch minimum is new;
5. explain why the binary-form/Hankel specialization is mathematically consequential rather than merely computable.

At present the paper asks the referee to infer novelty from the fact that the exact displayed formula is not among the cited theorems. That is not enough.

---

## 8. Fixed-space native realization: correct, useful, and too elementary to carry venue significance

Theorem 5.1 is one of the cleanest results in the paper.

Let \(T=JU^\perp\). The proof shows:

- necessity of a positive vector \(t=z^2\in T\);
- sufficiency by choosing \(z_i=\sqrt{t_i}\) and a frame of \(T\);
- global two-point separation by avoiding the finite union \(T\cap D_sT\).

This is a good theorem because it gives an exact criterion.

But the proof is essentially a frame construction plus a finite sign-invariance argument. The submersion statement is the ordinary frame-to-Grassmannian submersion after the change of variables \(A\mapsto\operatorname{diag}(Ae_1)A\).

I regard this as elegant supporting structure, not a top-four-level theorem by itself.

The manuscript should not overstate it as a deep classification of realizable geometry. It classifies the specific quadratic loading model at one prescribed normal space, which is valuable, but mathematically short.

---

## 9. The sharp single-contact threshold is now a corollary, which is the right status

The exact threshold
\[
 k_{\min}(d)
 =
 d+\left\lceil\frac{3+\sqrt{16d+1}}2\right\rceil
\]
is correct given the dimension inequality.

In v110 this was the headline theorem and suffered from the fact that its generic maximal-rank input was classical. V111 correctly subordinates it to the global failure theorem.

That improves the paper.

I would go further. The title, abstract, and introduction should make even clearer that the threshold is now an **application** of the multiplication-failure geometry plus native realization, not an independent principal source of originality.

---

## 10. The direct count-to-contact experiment is a real repair, but it is an engineered local score experiment

Section 9 is much better than the former plug-in pipeline.

The paper fixes a centre \(\lambda^0\), defines the derivative \(D\) of the moment parameter with respect to exposures, and chooses the local submodel
\[
 \lambda_N(h)
 =
 \lambda^0+N^{-1/2}B_*h,
 \qquad
 B_*=\Lambda D^{\mathsf T}\Sigma^{-1},
\]
so that
\[
 D B_*=I.
\]

This is a standard least-favourable/right-inverse construction. It makes the local moment parameter exactly \(h\) to first order and yields information \(\Sigma^{-1}\).

The retained contact score is a fixed linear compression of the jittered standardized counts. After Gaussian approximation, the limiting experiment is simply
\[
 Z\sim N(h,\Sigma),
\]
followed by the linear map \(\mathcal L Z\).

The information matrix
\[
 \mathcal L^{\mathsf T}
 (\mathcal L\Sigma\mathcal L^{\mathsf T})^\dagger
 \mathcal L
\]
and the criterion “no information loss iff \(\mathcal L\) is injective” are then standard facts about linear Gaussian experiments.

This theorem is correct-looking and useful because it connects the algebraic product rank to local statistical information loss.

But the statistical depth should be described accurately.

The result does **not** show:

- that physical distance/contact measurements are observed;
- that the full original categorical model is globally equivalent to contact data;
- that unknown mark laws can be discarded;
- that an unknown calibration centre can be estimated without affecting the comparison;
- that the reduction is sufficient outside the chosen least-favourable submodel;
- that multiple contacts arise as independent experimental channels;
- that the nonregular root parameter itself has a new contact-induced minimax theory.

The theorem says that, in a carefully chosen full-dimensional local exposure subexperiment, a linear score compression retains exactly the directions seen by the contact operator.

That is mathematically legitimate. It is also much closer to standard LAN/Le Cam linear algebra than to a new statistical theory of contact observations.

---

## 11. The jitter is mathematically clever but operationally artificial

I agree with the manuscript's reason for adding uniform jitter: without it, a real-valued linear encoding of an integer vector can remain injective for number-theoretic reasons even when the linear map has deficient real rank. Weak convergence alone would not rule out such pathological exact encodings.

So the jitter is not a pointless technical flourish.

However, it changes the interpretation.

The theorem is now about a **randomized statistical protocol chosen by the analyst**, in which auxiliary randomization is deliberately not retained. That protocol is designed to enforce the intended continuous-information comparison.

This is acceptable in Le Cam theory, but it is not a naturally occurring contact observation.

The paper should therefore resist rhetoric suggesting that the experiment has discovered an intrinsic physical “contact statistic.” It has constructed a randomized score compression whose limiting information is controlled by the contact multiplication operator.

That is a narrower, more precise statement.

---

## 12. The Poisson-to-Gaussian total-variation step is underproved relative to its importance

Lemma 9.1 is one place where I would demand a stronger proof before publication even in a specialized venue.

The manuscript claims uniform total-variation convergence of the jittered, standardized Poisson vector to the corresponding Gaussian vector over compact local parameter sets.

The proof gives a short Stirling argument on a growing central region and a second-moment tail bound.

This is plausible. But the lemma is carrying the full Le Cam equivalence claim, not merely a central limit theorem.

A final proof should either:

1. cite a precise local limit theorem in total variation for jittered Poisson variables with the required uniformity; or
2. give a self-contained quantitative \(L^1\) bound, including the central region, lattice-cell interpolation, covariance replacement, and tails.

The present few sentences are too compressed for a theorem whose entire purpose is to upgrade weak Gaussian convergence to a strong experiment comparison.

I do not call this a fatal counterexample. I call it a proof-completeness issue.

---

## 13. The boundary cone and \(N^{-1/4}\) root rate are coherent but mostly standard asymptotic theory

Theorem 8.1 now handles the physically constrained local parameter correctly.

The efficient Gaussian quotient
\[
 Y\sim N(h,R),\qquad h\in\mathbb R_{\ge0}^k
\]
is natural after nuisance projection, and the synchronized alternative \(h=q_A(\zeta)\) gives the distance profile.

The \(N^{-1/4}\) root-amplitude scale follows from the quadratic relation \(v=t^2v_0\). The two-point lower bound on a fixed ray is also standard once the LAN expansion is established.

This section is important for interpretation. It is not, in my view, a new asymptotic principle.

The paper itself partly acknowledges this. That restraint should remain.

---

## 14. The structured-family section is still auxiliary

The generic-transfer proposition is correctly demoted to a proposition. The block-spectral theorem is a useful explicit computation:
\[
 \rho(\mathcal K,c)
 =
 \min\left\{s,\binom{c+1}{2}\right\}.
\]

The diagonal and real symmetric circulant examples are nice checks that the loading-realization mechanism is not limited to Hankel matrices.

But the proof is elementary: choose rows whose rank-one outer products span the symmetric matrices, then use a simultaneous congruence under column orthonormalization.

This is good supporting material. It does not materially change my venue assessment.

A genuinely broad structured-compression theory would need sharp results for nontrivial families where the rank is not immediate from a fixed orthogonal spectral decomposition—for example Toeplitz, block-Hankel, graph-sparse, low displacement rank, or representation-theoretic families.

---

## 15. The manuscript is mathematically cleaner, but still too heterogeneous

The paper now contains:

- exact contact fibres;
- a calibrated Hankel information model;
- global Grassmannian failure geometry;
- native loading realization;
- local stability;
- structured matrix compression;
- cone LAN at a boundary;
- direct Poisson score experiments;
- classical rational maximal rank;
- additive bases;
- finite-sample categorical estimation;
- independent Gaussian contact noise;
- several historical complementary results.

The individual pieces are mostly related through the contact-compression theme.

But at 20 pages plus dense appendices, the paper still feels like several research notes compressed into one article.

A top-four paper normally has a very clear conceptual spine in which the major results force one another. Here the algebraic geometry theorem and the local statistical comparison are both interesting, but neither truly needs the full detail of the other.

I would consider splitting the project:

1. a pure/inverse-geometry paper centered on multiplication failure loci, native realization, and sharp thresholds;
2. a statistical paper centered on the physical boundary experiment and information-preserving score reductions.

That split would make the novelty claims much easier to audit.

---

## 16. Major mathematical revisions required for reconsideration at a top-four standard

I would not recommend another incremental round consisting of more finite diagnostics, more examples, or another specialized matrix family.

A serious reconsideration would require at least one major advance of the following scale.

### A. Classify the maximal components of the failure locus

Determine the irreducible components of \(\Delta^{(L)}\), at least generically in the two parameter regimes, and identify the component realizing the \(Lq-p+1\) branch geometrically.

This would turn the codimension formula into an actual structural theorem.

### B. Determine scheme structure, degree, or singularities

For example, prove reducedness/equidimensionality in a meaningful range, compute a Chow class or degree, or describe the generic singularity along the common-secant component.

Any one of these could substantially deepen the algebraic geometry.

### C. Generalize beyond binary quadratic multiplication

A theorem for
\[
 \operatorname{Sym}^m U\to H^0(\mathbb P^1,\mathcal O(mn))
\]
or for higher-dimensional polynomial spaces would reveal whether the two-branch phenomenon is a special accident or a general principle.

### D. Prove a quantitative random-conditioning theorem

The paper knows the bad-set codimension but not how close random native designs come to it. A dimension-dependent tail law for the least multiplication singular value would turn qualitative generic identifiability into a genuine robust theory.

### E. Make the statistical contact experiment intrinsic

Derive contact statistics from the original observation process without imposing a bespoke least-favourable local exposure submodel, or prove a broader Le Cam equivalence under unknown marks/exposures and estimated centre.

### F. Treat a singular statistical regime where the geometry changes the rate

For example, analyze shrinking multiplication singular values or high-contact-order degeneracy and derive a nonstandard minimax transition controlled by the failure geometry.

### G. Establish priority relative to the full quadratic-normality/failure-locus literature

This is mandatory even if no new theorem is added.

---

## 17. Specific proof and presentation comments

The following are not substitutes for the major issues above, but they should be addressed in any next version.

1. **State Theorem 1.1's set/scheme distinction in the theorem title.** The codimension is for the underlying reduced closed set; the scheme is used only as a determinantal vehicle.

2. **Quote the exact Hankel-rank source.** “Sections 1–2” is too broad for a principal external input. Give proposition/theorem numbers or a short independent proof of the dimension.

3. **Separate exact-rank and rank-at-most-\(r\) notation consistently.** The proof moves between them correctly, but a reader should not have to infer when closure has been taken.

4. **Promote the isotropic dimension calculation to a more invariant statement.** Explain it as the dimension of a relative isotropic Grassmannian over the radical intersection stratum.

5. **Reorganize the optimization lemma.** The current arithmetic case split is correct-looking but unenlightening. Explain geometrically why the extrema occur at full-rank/determinantal and rank-two/secant ends.

6. **Strengthen the generic one-to-one proof for the common-secant incidence.** Define the exceptional double-hyperplane incidence and compute its dimension explicitly.

7. **Clarify the phrase “common-secant component.”** It is a component only when its codimension attains the minimum. Elsewhere it is merely an irreducible subvariety of the bad set.

8. **When the two bounds are equal, discuss possible additional components.** The manuscript notes that they may exist; say whether anything more can be proved.

9. **In the determinant-height step, state the exact affine chart and ideal height inequality.**

10. **For real native realizability of the secant family, distinguish existence from genericity.** The construction gives a real open subset in the incidence; explain precisely where birationality is used to transfer codimension.

11. **The fixed-space sign criterion should mention that \(s\) and \(-s\) give the same partition.** This is minor but clarifies the finite obstruction set.

12. **Clarify the algebraic status of the positive-realizable image.** It is Euclidean open and Zariski dense, not a Zariski-open subset characterized by positivity.

13. **In the global distance lemma, give the dependence of the projection tube explicitly.** The paper says it depends on \(A\), the germ, and a compact metric set; this is correct and should be kept visible whenever the theorem is used.

14. **Do not let “generic global distance” sound uniform in \(d,k\).** No dimension-uniform tube or stability constant is proved.

15. **The stability theorem's upper bound by distance to the real bad set is chart-dependent.** State the compact chart domain on which the Lipschitz constant is controlled.

16. **The block-spectral theorem should be demoted in the abstract, if mentioned at all.** It is an example, not a central theorem.

17. **For the boundary LAN theorem, specify the exact local parameter set and norm in the uniform \(o_P(1)\).**

18. **For the root-rate corollary, show the finite-sample moment bound used for the upper risk estimate rather than only referring back to the LAN calculation.** Weak LAN by itself does not imply uniform second-moment control.

19. **For Lemma 9.1, replace the one-paragraph total-variation proof with a quantitative local-limit lemma or a precise citation.**

20. **State the Le Cam metric being controlled.** The text speaks of asymptotic equivalence and uniform total variation; formalizing the two deficiencies would make the claim cleaner.

21. **Clarify what “raw local target experiment” means.** It is the specified least-favourable exposure submodel, not the full original model.

22. **Do not call the score statistic a physical contact measurement.** The final paragraph mostly avoids this; keep that discipline in the abstract and introduction.

23. **Explain why the jitter is part of the experiment rather than an analytical device.** If it is analyst-added randomization, say so prominently.

24. **Discuss whether a deterministic coarsening with finite precision would avoid the lattice pathology without randomization.** This would help readers understand how operational the jitter issue really is.

25. **If the centre \(\lambda^0\) is estimated from a preliminary sample, state what changes.** The current theorem assumes it is fixed before observation.

26. **The known-mark assumption is substantial.** It should appear in the theorem label or first sentence, not only in setup prose.

27. **The information projector identity is standard.** Present it as the consequence of the Gaussian compression theorem rather than as an independent novelty claim.

28. **Expand the literature discussion on failure loci and quadratic normality.** The current references are not enough for a venue-level priority claim.

29. **Separate “new theorem” from “native application” in the introduction.** The abstract currently interleaves them tightly.

30. **Consider moving most historical appendices out of the principal article.** They make the submission look cumulative rather than conceptually distilled.

31. **The source-bound verification material should remain outside the mathematical narrative.** V111 does this well; do not reverse that improvement.

32. **Do not add more witness tables.** The universal proof is the relevant object.

33. **Do not add another family merely to enlarge the list of examples.** Only a family requiring genuinely new mathematics would affect the significance assessment.

34. **If the project continues to target a top-four journal, the next revision should be theorem-driven, not response-driven.** The manuscript now needs a new conceptual layer, not another round of patching individual referee bullets.

---

## 18. Assessment of the response to R110

The response letter is unusually explicit about what is and is not claimed, and I view that positively.

In particular, it correctly concedes that:

- the old computed-contact pipeline was deterministic re-encoding;
- the new statistical theorem is local and known-mark;
- independently designed contacts are not arbitrary contacts on one fixed loading;
- the complex codimension theorem does not imply real points on every component;
- no full component classification or scheme-reducedness theorem is proved;
- finite diagnostics do not certify universal correctness.

Those qualifications make the paper more credible, not less.

However, the response also illustrates the current problem: a large fraction of the intellectual effort is devoted to closing a very long sequence of review objections. The result is a technically careful manuscript whose venue-level story is still assembled from many repairs.

At this stage I would stop optimizing against prior reports and ask a more fundamental question: **what single theorem would make this paper important to a mathematician who knows nothing about the repository history?**

Theorem 1.1 is the first version that comes close to answering that question. It needs to be developed much further.

---

## 19. Final recommendation

I recommend **rejection in the present form** at a general top-four mathematics journal.

This recommendation should not be read as saying that the revision failed mathematically. On the contrary, v111 is a substantial improvement and appears to contain a real, sharp, publishable theorem about multiplication failure loci of binary linear series, together with a clean native realization mechanism and a careful local statistical interpretation.

The problem is the venue standard.

At present the principal algebraic result gives an exact codimension formula and one explicit dominant component, but stops before a full structural theory of the failure locus. The statistical result gives an exact information-loss calculation for a deliberately chosen local randomized score-compression experiment, but not an intrinsic or global contact observation theory. The remaining supporting theorems are either classical inputs, elementary realizations, or standard asymptotic consequences after the model has been reduced to finite-dimensional Gaussian form.

For a strong specialized journal in algebraic geometry, inverse problems, algebraic statistics, or mathematical statistics, I would regard the paper as potentially viable after a serious literature audit and proof polishing.

For Annals / Inventiones / JAMS / Acta, I would require another major conceptual theorem—preferably a structural classification or a generalization that explains the codimension phenomenon rather than merely computes it in the binary quadratic case.

**Recommendation: reject.**
