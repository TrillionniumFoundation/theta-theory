# Independent harsh referee report on A2 revision 102

**Manuscript:** *Intrinsic metric data and cancellation laws for polynomial observations*  
**Reviewed revision branch:** revision/a2-v102-intrinsic-metric-contact-walls-2026-09-20  
**Principal mathematical source commit:** 370116f6876f72b30d162a055f7937c1c70d6a3e  
**Native-build trigger source commit recorded by the revision:** 7961db6030cd6f2a2072847fe06dd3179373d243  
**Principal article source:** papers/A2-v17-boundary-information-coarsening/article/v102/paper.tex  
**Controlling prior report:** reviews/a2-v101-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md  
**Controlling prior review commit:** 9e7caa42cce40587828f7e8357c119e127a56805  
**Prior reviewed paper head:** d1654974140410eb356240d3121c5f36267a89d2  
**Independent review branch:** review/a2-v102-independent-harsh-top4-2026-09-20  
**Date:** 2026-09-20

## 1. Recommendation

**Recommendation for an Annals / Acta / Inventiones / JAMS-level general mathematics journal: reject in the present form.**

This is **not** a correctness rejection.

Revision 102 is a serious revision. It directly addresses the most important objections in the v101 report rather than merely adding repository infrastructure. In particular, it now supplies:

1. a canonical residual-tensor envelope attached to all positive-definite leading metric coefficients;
2. an exact secant-kernel criterion for finite quadratic probes and a deterministic adaptive lower bound over a variable-metric class;
3. an endpoint-effective quotient function obtained by minimizing over one-sided invisible variables;
4. a cancellation-uniform relative factorization for a finite polynomial residual;
5. a strictly positive probability realization with the corresponding Hellinger coefficient; and
6. a much shorter 13-page principal article, with the historical mathematics moved to supporting/archive volumes.

Those are real improvements.

Nevertheless, the revision still does not reach the mathematical depth and inevitability expected at the stated journal level.

The decisive issue has changed. Revision 101 was still missing a genuinely intrinsic finite-information theorem and a family-level wall statement. Revision 102 now supplies literal answers to those requests. The problem is that, after those answers are written cleanly, the mathematical mechanisms exposed by the principal article are substantially more standard than the rhetoric of a top-four submission permits:

- the metric contact envelope is a convex-duality packaging of rank-one residual tensors and their lower support values;
- the all-positive-definite finite-probe theorem is linear injectivity on the space of symmetric matrices, with the sharp count coming from dimension and polarization;
- the endpoint-effective metric is the value function of a strictly convex quadratic program over an orthant and therefore has the usual finite active-set piecewise-quadratic structure;
- the cancellation-uniform wall theorem is a clean but one-dimensional divided-difference/shear perturbation argument around the exact scalar residual C(a,z);
- the divisorial exponent remains classical Łojasiewicz/integral-closure territory, with the genuinely new metric information carried separately by the residual vectors or resolved units.

I found no direct counterexample to the stated principal theorems. My objection is that the paper has not yet shown that these standard mechanisms combine into a new theorem of the scale required for a top-four general mathematics journal.

## 2. Scope of this report

I reviewed the v102 principal source, the point-by-point response to the v101 report, the source manifest, local validation record, exact diagnostic record, v102 build workflow and builder, and the controlling v101 referee report.

I also checked the current native-build state associated with the run ID recorded in the v102 manifest.

The principal article is short enough that the mathematical claims can now be reviewed directly rather than through the repository history. That is an important improvement.

My standard remains deliberately severe. The question is not whether this is a correct or publishable piece of mathematics. The question is whether the present revision contains a theorem whose conceptual force, technical depth, generality, and novelty plausibly justify Annals / Acta / Inventiones / JAMS-level consideration.

## 3. Executive diagnosis

The v102 principal paper has a much clearer spine than v101.

The intended chain is now:

1. leading residuals determine a canonical convex tensor envelope;
2. local binary root geometry yields positive-definite quotient forms;
3. finite ray probes recover those forms exactly under a secant-kernel condition;
4. endpoint invisibility replaces the full matrix by a smaller effective value function;
5. remote one-dimensional polynomial models admit an exact scalar cancellation polynomial whose value controls the distance uniformly through all cancellations;
6. a probability-simplex realization transfers this to Hellinger geometry.

This is coherent.

The difficulty is that each arrow is currently much closer to a standard construction than to a new structural theorem.

The paper therefore faces a sharper top-four problem than before:

> the mathematical story is finally clean enough that one can see exactly where the novelty is, and at present that novelty is too thin relative to the surrounding classical machinery.

The strongest new part, in my view, is the cancellation-uniform relative estimate. It is elegant and useful. But it is proved for a one-dimensional remote parameter x with a residual pair of the special form

\[
(x^m-\delta,\ g_a(x)).
\]

The strongest conceptual part is the residual-tensor envelope. But its reconstruction theorem is essentially the separating-hyperplane theorem applied to the closed convex upper hull generated by \(yy^{\mathsf T}\).

The strongest finite-information part is the adaptive lower bound. But over the full class of positive-definite forms the lower bound is dimension counting plus an exact-query adversary, while the native fixed-Hellinger family—the family that belongs to the observation problem—does not receive a comparable sharp lower bound.

Revision 102 is therefore cleaner, but the clean-up exposes rather than removes the novelty problem.

## 4. What revision 102 genuinely fixes

A harsh report should record the improvements precisely.

### 4.1 R101.1: the status of the scalar datum is now stated honestly

The manuscript explicitly calls the constrained quantity \(c_p(v)\) a model-dependent variational oracle.

It says that it is not:

- an empirical scalar statistic;
- a physical intervention;
- a sample-complexity statement.

That resolves an important ambiguity from v101.

### 4.2 R101.2: there is now a genuine exact probe criterion

Theorem 3.3 no longer merely presents one polarization family.

It characterizes sufficiency on a matrix family \(\mathscr Q\) by

\[
\ker \mathcal A_V\cap(\mathscr Q-\mathscr Q)=\{0\}.
\]

For the full positive-definite class this reduces to spanning \(\operatorname{Sym}_k\) by the rank-one probe tensors.

The theorem also includes a deterministic adaptive exact-query lower bound.

This is a literal and mathematically correct-looking answer to the previous request for necessity/minimality.

### 4.3 R101.2: endpoint invisibility is now handled explicitly

Theorem 3.5 correctly recognizes that, when endpoint sums disappear at the leading root scale, the spectral fibre does not identify the full quotient matrix.

The replacement

\[
G_Q(x)=\min_{z\ge0}(x,z)^{\mathsf T}Q(x,z)
\]

is the right object.

The 2-by-2 example makes the noninjectivity of \(Q\mapsto G_Q\) concrete.

This closes a real logical weakness in v101.

### 4.4 R101.3/R101.4: the intrinsic object is no longer a divisor list

The pair \((\rho,\mathcal C_\rho)\) is defined before choosing a resolution.

The presentation-dependent real divisors are relegated to a computational appendix.

This is conceptually better than advertising a coordinate-divisor list as canonical.

### 4.5 R101.5: there is now a family-level wall theorem

Theorem 4.1 is materially stronger than a fixed generic-order calculation.

The estimate is relative to the exact residual scalar \(C(a,z)\), not relative to its first generic nonzero monomial.

That distinction is important because it survives cancellations.

The crossover and higher-cancellation corollaries are genuine consequences.

### 4.6 R101.6: the principal article is now theorem-driven

The 13-page principal is a major editorial improvement over the cumulative v101 architecture.

Repository preservation no longer forces the reader to treat every historical layer as principal exposition.

### 4.7 The response is careful about what the computations prove

The revision does not claim that finite diagnostics prove the universal theorems.

It does not infer native success from a queued workflow.

That evidentiary discipline is appropriate.

## 5. Main objection I: the “complete metric contact data” theorem is mathematically valid-looking but too close to a definition plus convex separation

Theorem 2.2 is presented as the new canonical invariant.

Let

\[
\mathcal E_\rho
\]

be the set of all normalized leading residual limits, and define

\[
\mathcal C_\rho
=
\overline{\operatorname{conv}
\{yy^{\mathsf T}:y\in\mathcal E_\rho\}
+\operatorname{Sym}_M^+}.
\]

Then, for \(H>0\),

\[
a_H^2
=
\inf_{S\in\mathcal C_\rho}\operatorname{tr}(HS),
\]

and the family of all such values reconstructs \(\mathcal C_\rho\).

I do not object to the proof.

I object to the scale of the claimed conceptual contribution.

### 5.1 The completeness statement is close to tautological

The set \(\mathcal C_\rho\) is designed precisely so that positive-definite linear functionals recover the minima of \(y^{\mathsf T}Hy\).

Once this upper closed convex hull has been defined, reconstruction from all separating linear functionals is standard convex duality.

The nontrivial asymptotic point is that the leading coefficient of the original minimization problem equals the minimum over \(\mathcal E_\rho\).

That is useful.

But the word “complete” should not obscure the fact that the invariant is constructed to be exactly the quotient seen by those functionals.

A top-four theorem would need substantially more than this dual representation.

### 5.2 No realization or classification theorem is proved for the envelope

The paper does not characterize which closed convex \(\operatorname{Sym}_M^+\)-upper sets arise from semialgebraic residual germs.

It does not classify envelopes under natural operations.

It does not give a finite intrinsic presentation.

It does not identify extremal tensors or exposed faces in terms of singularity geometry.

It does not show that the envelope controls more than the deliberately chosen family of positive-definite leading coefficients.

Any of these could turn the construction into a substantive new object.

At present the theorem says, roughly:

> all metric minima are encoded by the closed convex object whose lower support values are those metric minima.

That is a useful package, not yet a deep classification.

### 5.3 The semialgebraic asymptotic argument is short because the hard structure is absent

Compactness, definability, norm equivalence, and curve selection give:

- existence of one rational leading exponent;
- equality of that exponent for all equivalent positive-definite norms;
- attainment of leading metric coefficients;
- a minimizing Puiseux arc.

These are clean statements.

They are also expected in a compact semialgebraic setting.

The paper must therefore explain what new phenomenon the tensor envelope reveals that is not already obvious from definable minimization plus convex support theory.

## 6. Main objection II: the headline finite-probe theorem is exact but its sharp part is essentially linear algebra

Theorem 3.3 is better than its v101 predecessor.

But the top-four significance problem remains.

### 6.1 The secant-kernel criterion is the injectivity criterion for a linear sampling map

The map

\[
\mathcal A_V(H)
=
(v_i^{\mathsf T}Hv_i)_i
\]

is linear in \(H\).

Therefore the condition

\[
\ker\mathcal A_V\cap(\mathscr Q-\mathscr Q)=\{0\}
\]

is exactly the statement that the linear measurements are injective on \(\mathscr Q\).

This is correct.

It is also the first criterion one writes down for injectivity of a linear measurement map on a subset.

Calling this a characterization is formally accurate, but it should not be mistaken for a difficult inverse theorem.

### 6.2 The \(k(k+1)/2\) bound over all positive-definite forms is dimension counting

For the full class \(\operatorname{Sym}_k^{++}\), injectivity requires the rank-one tensors \(v_iv_i^{\mathsf T}\) to span \(\operatorname{Sym}_k\).

The lower bound

\[
m\ge k(k+1)/2
\]

is therefore the dimension of the symmetric-matrix space.

The probes \(e_i\) and \(e_i+e_j\) recover the entries by polarization.

Again, this is correct.

But it is elementary linear algebra.

The theorem becomes genuinely model specific only when \(\mathscr Q\) is the actual quotient-form family generated by the stochastic polynomial observation model.

The paper does not solve that sharper problem.

### 6.3 The adaptive lower bound is an exact-query adversary for the full matrix class

The adaptive argument fixes a positive-definite \(Q_0\), records fewer than \(\dim\operatorname{Sym}_k\) queried rank-one tensors, and chooses a nonzero symmetric perturbation orthogonal to all of them.

That is the standard adversary one expects for exact linear queries.

It does not require special structure from the observation model.

It does not survive automatically under noise, approximate answers, randomized queries, or a restricted model-generated family \(\mathscr Q\).

Thus the adaptive theorem is sharp for the chosen oracle class, but the chosen oracle class is too broad to establish a sharp information theorem for the original Hellinger observation problem.

### 6.4 The most relevant fixed-Hellinger problem is explicitly left open

The manuscript is commendably honest:

> the \(k(k+1)/2\) lower bound is not asserted for the smaller fixed-Hellinger family.

That honesty also identifies the missing theorem.

For the actual stochastic observation model, what is the dimension and geometry of the family of quotient forms obtainable by varying the centre, clocks, channel parameters, and design weights under the fixed Hellinger metric?

Which probes are necessary and sufficient on that family?

Can fewer than \(k(k+1)/2\) exact scalar costs always suffice?

Are there model-specific algebraic relations among the entries of \(Q\)?

Until this is answered, the strongest lower bound is for an artificially enlarged metric class rather than for the native statistical geometry.

## 7. Main objection III: the endpoint-effective theorem is a standard parametric quadratic-program value function

Theorem 3.5 defines

\[
G_Q(x)=\min_{z\ge0}(x,z)^{\mathsf T}Q(x,z)
\]

and proves that \(G_Q\) is continuous, homogeneous of degree two, and piecewise quadratic on finitely many polyhedral cones, with Schur-complement formulas determined by active endpoint sets.

I see no obvious correctness problem.

But this structure is classical.

### 7.1 Active-set piecewise quadraticity is expected

A strictly convex quadratic program with polyhedral inequality constraints has a piecewise-affine optimizer and a piecewise-quadratic value function on critical regions.

The proof given in the manuscript is the direct KKT/active-set derivation of that standard fact.

The paper currently gives no citation to the classical multiparametric quadratic-programming literature.

That omission matters because this theorem is one of the stated headline contributions.

### 7.2 The genuinely interesting problem is the quotient \(Q\mapsto G_Q\), not the active-set formula

The paper proves that different positive-definite matrices may yield the same \(G_Q\).

Good.

But it stops immediately after a 2-by-2 example.

A deeper theorem would characterize the equivalence relation

\[
Q\sim Q'
\quad\Longleftrightarrow\quad
G_Q=G_{Q'}
\text{ on }\mathbb R_+^r.
\]

For example:

- what is the dimension of a generic equivalence class?
- is there a canonical minimal representative?
- which Schur-complement data are intrinsic?
- can \(G_Q\) be represented by a minimal finite fan?
- which piecewise-quadratic homogeneous functions arise from positive-definite \(Q\) by this endpoint elimination?
- how does this quotient behave under changes of spectral coordinates?

Those questions would be new structural mathematics.

The present theorem merely identifies the standard value function that the spectral decoder sees.

## 8. Main objection IV: the cancellation-uniform wall theorem is elegant but too one-dimensional to carry the paper at top-four level

Theorem 4.1 is, in my view, the best new theorem in the principal article.

The key identity

\[
g_a(x)
=
C(a,z)
+
(x^m-z^m)B_a(x,z)
\]

combined with

\[
B_a(x,z)=O(z^{n_1-m})
\]

gives a small shear of the quadratic residual pair.

Because the estimate is relative to \(|C(a,z)|\), it survives exact and near-exact cancellation.

That is a nice idea.

The problem is its scope.

### 8.1 The theorem is a one-variable normal-form calculation

The remote parameter is scalar \(x\).

The first residual coordinate is exactly \(x^m-\delta\).

The second residual is a finite polynomial in the same scalar \(x\).

The wall is therefore the exact scalar equation

\[
C(a,z)=g_a(z)=0.
\]

After localization, the proof reduces to a two-dimensional quadratic norm and a small shear.

This is much more special than the general semialgebraic singularity language used elsewhere in the project.

### 8.2 “Arbitrary cancellation” means arbitrary cancellation inside one finite scalar polynomial

This is still useful.

But it should be described precisely.

The theorem does not classify arbitrary cancellations in a multivariable singular family.

It does not handle multiple competing remote branches, nonisolated critical manifolds, several coupled residual equations, or a nontrivial discriminant of feasible branches.

It says that once the geometry has been reduced to this one-dimensional polynomial normal form, the exact finite polynomial \(C\) retains all cancellation information.

That is a strong normal-form consequence.

What is missing is the theorem that places a broad class of observation singularities into this normal form.

### 8.3 The probability realization is an embedding, not a classification

Theorem 4.5 embeds the residual pair into a positive probability simplex by choosing independent zero-sum directions \(A,B\).

The Hellinger metric then produces the expected Fisher quadratic form to leading order.

This is a correct and useful realization.

But the construction is flexible enough that it mainly shows that the one-dimensional wall theorem can occur inside a probability model.

It does not classify probability-model singularities.

It does not show that naturally arising polynomial stochastic observations reduce to this model.

For top-four significance, the direction should be reversed:

> prove that a substantial natural class of singular stochastic observation problems has this cancellation polynomial as an intrinsic normal form.

Without that reverse theorem, the probability realization is an existence example.

## 9. Main objection V: the local “observable-law” formulation is cleaner but still not an information theorem about observations

Revision 102 carefully avoids the overclaim from v101.

That is good.

But the limitation remains mathematically important.

### 9.1 The variational oracle is defined using the known model and the exact centre law

The quantity

\[
c_p(v)
=
\lim_{t\downarrow0}
\frac4{t^2}
\inf\{h_w(p',p)^2:\tau_p(p')=tv\}
\]

is defined on the observable model image.

However, the coordinate \(\tau_p\) itself uses:

- the recovered component decomposition;
- the central root clusters;
- their multiplicities;
- their endpoint status;
- selected first and second cluster coefficients.

At a full-rank centre those objects are indeed recoverable from the exact law by Lemma 3.1.

But that means the finite-probe theorem is operating after the hard exact inversion has already been performed.

It is an intrinsic quotient of the identified local germ, not a direct finite summary of raw observational data.

### 9.2 Exact-centre recoverability is not robust stratum recovery

The paper says multiplicities can be specified by gcd conditions and endpoint evaluation.

Correct.

But such discrete pattern information is not stable across multiplicity-changing strata.

The uniform Hausdorff statement is only on compact subsets of a fixed pattern stratum.

The paper therefore does not yet have a single finite invariant that passes continuously through root collisions, endpoint creation, or multiplicity changes.

That is exactly where a deeper singularity-theoretic information theorem would become interesting.

### 9.3 The full-rank inverse still does most of the model-specific work

The coefficient inverse recovers the centre.

The partial-fraction independence identifies the relevant score columns.

The local expansion supplies the retained/free split.

After that, the quadratic quotient and its probing are standard.

A top-four local theorem would need to reveal structure that is not already implicit in this exact inverse plus Taylor expansion.

## 10. Main objection VI: the literature positioning is not adequate for a top-four submission

The principal bibliography contains only three items:

1. Lejeune-Jalabert–Teissier/Risler;
2. Jell–Scheiderer–Yu;
3. the authors’ own v101 supporting manuscript.

This is not enough.

The problem is not cosmetic citation count.

Several principal theorems sit squarely inside classical areas whose literature must be confronted directly.

### 10.1 Convex support reconstruction needs explicit positioning

The metric envelope theorem uses:

- closed convex hulls;
- support/separation;
- positive-semidefinite upper closures;
- reconstruction from linear functionals.

The manuscript should explain what part is new beyond standard convex analysis.

### 10.2 The endpoint theorem needs comparison with multiparametric quadratic programming

Piecewise-affine optimizers and piecewise-quadratic value functions on polyhedral active-set regions are classical.

The manuscript should cite and distinguish that theory.

Without such a comparison, a referee cannot tell whether Theorem 3.5 is intended as an application of standard parametric QP or as a claimed new theorem.

### 10.3 The Łojasiewicz literature comparison is now too narrow

The v102 introduction cites the classical integral-closure mechanism.

That is necessary but no longer sufficient.

Recent work also matters.

In particular, Tai Huy Ha, *An algebraic theory of Łojasiewicz exponents*, arXiv:2602.18410 (2026), explicitly develops valuative finite-max principles and states stability, stratification, and wall-chamber phenomena for Łojasiewicz exponents in families.

Whether or not the present paper ultimately overlaps technically with that preprint, a September 2026 top-journal submission discussing finite divisorial computation, family stratification, and wall behavior must compare itself with such current work.

The present bibliography does not.

### 10.4 The paper needs a theorem-by-theorem novelty table in mathematical prose

For each principal result, the authors should state:

- what theorem is classical;
- what theorem is a direct specialization;
- what theorem is genuinely new;
- what hypothesis is weaker or conclusion stronger than existing literature;
- what part uses the stochastic polynomial model in an essential way.

At present the reader has to infer this.

For a top-four submission, that is unacceptable.

## 11. Main objection VII: several proofs are plausible but too compressed for the claimed level

I did not find a direct contradiction.

I do, however, find several places where the exposition is below the proof-detail standard appropriate for the claimed venue.

### 11.1 The whole-model Hausdorff convergence in Proposition 3.2 needs a standalone proof lemma

The proof moves rapidly from coefficient/stochastic \(O(t)\) control to:

- repeated-root \(O(\sqrt t)\) control;
- endpoint \(O(t)\) control;
- radial contraction of retained/free variables;
- feasibility of reconstructed competitors;
- outer and inner Hausdorff bounds;
- uniformity on compact pattern sets;
- exclusion of remote components of the whole-model ball.

That is a large amount of geometry in one paragraph.

The statement is central.

It should be split into lemmas with explicit constants and quantifiers.

In particular, the radial-contraction argument should state exactly how the contraction dominates the Taylor remainder uniformly near cone boundaries.

### 11.2 Lemma 3.1 should spell out the polynomial divisibility step

The sentence about applying the invertible channel and obtaining

\[
q\mid ef_1,\qquad q\mid ef_2
\]

is too compressed for a reader who has not reconstructed the matrix algebra.

This may be routine, but it is the exact-identification input on which the local theorem depends.

It should be written as an explicit calculation.

### 11.3 The existence statement for the real monomial presentation needs a precise theorem and citation

Appendix A defines a sufficiently strong presentation and then says that simultaneous principalization and real rectilinearization supply such presentations in the setting of the supporting volume.

That sentence carries substantial geometric content.

The paper must identify the exact theorem guaranteeing:

- finite covering;
- properness;
- surjectivity onto the real feasible germ;
- monomialization of time and residual ideal;
- compatibility with inequalities;
- the positive-time closure;
- the accessibility property used in the maximum-ratio argument.

A top-four paper cannot leave this as an uncited umbrella statement.

### 11.4 Corollary 4.2 should state explicitly that the coefficient arc is absorbed into the residual germ

The corollary applies the intrinsic-envelope language along a semialgebraic coefficient path \(a(\delta)\).

That is fine if one defines the resulting residual as the fixed semialgebraic germ

\[
R(x,\delta)
=
(x^m-\delta,\ g_{a(\delta)}(x)).
\]

The paper should say this explicitly before identifying \(\mathcal E_\rho\).

### 11.5 The fixed-pattern qualifier should be visible earlier

Several uniform statements are uniform only on compact subsets of a fixed multiplicity/boundary pattern.

That restriction is mathematically important.

It should appear prominently in the theorem-level summary, not mainly inside the local section.

## 12. Correctness audit of the principal v102 statements

I record here my current mathematical assessment.

### 12.1 Theorem 2.2: metric contact envelope

I found no direct flaw.

The use of semialgebraic minimization and norm equivalence to force the same exponent for every positive-definite norm is sound-looking.

The positive-definite reconstruction from a positive-semidefinite separating functional plus a small identity perturbation is also sound-looking.

The result is conceptually modest for the reasons above, but not evidently false.

### 12.2 Proposition 2.4: arc formula

The minimizer-selection argument is plausible.

Because the norm of a real Puiseux vector has order equal to the minimum coordinate order, the selected minimizing arc attains the ratio.

Again, I see no counterexample under the stated compact semialgebraic hypotheses.

### 12.3 Lemma 3.1: coefficient inverse

The polynomial interpolation and simple generalized-eigenvector recovery are plausible under coprimality and invertible positive channels.

The proof should be expanded, but I did not identify a contradictory case.

### 12.4 Proposition 3.2: local quotient

The partial-fraction independence supports injectivity of the combined score.

The Schur complement is positive definite.

The root-scale distinction between repeated interior roots and endpoint/simple roots is consistent with the coefficient expansions.

The main concern is proof compression and uniformity, not an explicit counterexample.

### 12.5 Theorem 3.3: probes

The linear-algebra criterion and the full positive-definite lower bound are correct-looking.

The adaptive adversary is also correct for deterministic exact queries.

The limitation is relevance to the native fixed-Hellinger form family.

### 12.6 Theorem 3.5: endpoint-effective metric

The KKT active-set formula is correct-looking.

Strict convexity gives a unique minimizing endpoint variable.

The resulting value function is piecewise quadratic and homogeneous.

No direct correctness objection.

### 12.7 Theorem 4.1: cancellation-uniform factorization

The proof is clean.

The trial \(x=z\) gives localization.

The divided-difference coefficient is \(O(z^{n_1-m})\).

The resulting shear of \((U,C)\) is uniformly small.

The unrestricted quadratic minimizer in \(U\) remains feasible because \(U_*=O(z^{n_1})=o(z^m)\).

This appears sound and is the strongest new argument in the paper.

### 12.8 Theorem 4.5: Hellinger realization

The local Hellinger quadratic expansion and Schur complement produce the displayed coefficient.

The strict-positivity construction is straightforward.

The theorem appears sound as an existence realization.

## 13. Reproducibility audit

The repository discipline is good, but the full native closure claimed as the final R101.7 target is not yet complete at the time of this review.

### 13.1 Local principal build

The committed LOCAL_VALIDATION.json reports:

- principal native compilation passed;
- 13 pages;
- no unresolved references or citations;
- no overfull or underfull boxes;
- source blob readback matched;
- finite diagnostics passed.

I treat this as useful evidence for the principal source.

### 13.2 The full native archival graph is not locally executed

The same record explicitly says:

- full archival native status: not executed locally;
- no remote success inferred.

That wording is correct.

### 13.3 The recorded remote run is still queued

SOURCE_MANIFEST.json records full native run ID

35500287312.

At the time of this review, the run has one job:

- job name: native;
- status: queued;
- conclusion: null.

No workflow artifact is present for that run.

### 13.4 No durable runtime receipt is present on the reviewed revision branch

The expected file

revisions/a2-v102/native/RUNTIME_RECEIPT.json

is not present.

The associated native log/summary files are also absent.

Therefore the correct conclusion is:

> source-bound full native success has not yet been durably established for v102.

This is not a mathematical rejection reason.

It does mean R101.7 is not yet closed.

## 14. Disposition of the v101 requests

### R101.1 — Clarify the status of the finite scalar datum

**Answered.**

The manuscript now calls it a model-dependent variational oracle and explicitly denies stronger operational interpretations.

### R101.2 — Prove a genuinely intrinsic finite-information theorem

**Partially answered.**

The exact secant-kernel criterion and adaptive lower bound are substantial literal improvements.

However, the sharp \(k(k+1)/2\) result is for the full variable-metric positive-definite class, not the native fixed-Hellinger family.

The theorem therefore does not yet establish the intrinsic measurement complexity of the original observation model.

### R101.3 — Separate the new divisorial content from classical Łojasiewicz theory

**Improved but not adequately completed.**

The introduction now acknowledges the classical mechanism.

The literature comparison is still far too narrow, especially given current work on valuative finite-max principles, stability, and wall-chamber behavior.

### R101.4 — Make the data canonical or say what is canonical

**Answered in form.**

The paper now defines \((\rho,\mathcal C_\rho)\) intrinsically and explicitly says the divisor list is presentation dependent.

The remaining issue is whether \(\mathcal C_\rho\) is mathematically deep enough to justify being the central new invariant.

### R101.5 — Connect contact theory to a wall-classification theorem

**Answered in a special but genuine family.**

Theorem 4.1 gives a real family-level classification for the one-dimensional polynomial residual model.

The unresolved issue is generality.

### R101.6 — Reduce cumulative principal architecture

**Answered.**

The 13-page principal article is much better.

### R101.7 — Complete source-bound native validation

**Not answered yet.**

The run is queued, there is no artifact, and no runtime receipt is committed.

## 15. Revisions required before reconsideration at the same journal class

I do not think another incremental layer of notation will help.

The next revision must deepen at least one of the present principal theorems.

### R102.1 — Prove that the metric contact envelope has nontrivial structure beyond convex duality

A materially stronger result would do at least one of the following:

- characterize the envelopes realizable by semialgebraic or Nash residual germs;
- give a finite intrinsic representation in a significant class;
- identify extremal/exposed tensors by geometric valuations or arcs;
- prove a product/composition theorem;
- prove stability or wall crossing of the envelope in families;
- recover a known singularity invariant and strictly refine it.

Without such a theorem, the envelope remains an elegant bookkeeping device.

### R102.2 — Solve the finite-probe problem for the actual model-generated quotient family

Do not rely on the artificially enlarged class of all positive-definite forms.

Characterize the family \(\mathscr Q_{\mathrm{model}}\) arising from the fixed Hellinger observation geometry.

Then prove:

- its dimension;
- its secant geometry;
- the sharp deterministic query complexity;
- whether adaptive queries help;
- whether the polarization count is generically or uniformly minimal.

This would make the information theorem genuinely model specific.

### R102.3 — Classify the endpoint quotient \(Q\mapsto G_Q\)

The active-set formula itself is not enough.

Characterize when two positive-definite matrices have the same effective function.

Find canonical data for the equivalence class.

Determine which homogeneous piecewise-quadratic functions arise.

A true quotient-classification theorem here could become a new central result.

### R102.4 — Either generalize the wall theorem or prove a broad normal-form theorem reducing to it

The current one-dimensional theorem is clean.

To justify general-journal scale, prove one of:

- a multivariable analogue;
- a multi-branch analogue;
- a theorem for several coupled residual equations;
- a normal-form theorem showing that a broad natural class of polynomial observation singularities reduces to the present scalar cancellation polynomial.

The current probability construction is only a realization.

### R102.5 — Bring the literature review to top-journal standard

Add direct comparisons with:

- classical convex duality/support theory;
- multiparametric quadratic programming and piecewise-quadratic value functions;
- classical and modern Łojasiewicz/integral-closure/valuation theory;
- current 2026 work on finite-max and wall-chamber behavior.

Explain theorem by theorem what is new.

A three-reference bibliography is not defensible for the present claims.

### R102.6 — Formalize the real monomial-presentation existence theorem

State and cite the exact result supplying the presentation used in Appendix A.

Do not leave properness, surjectivity, real inequality rectilinearization, and accessibility implicit.

### R102.7 — Expand the local Hausdorff theorem proof

Separate:

- coefficient inverse;
- cluster estimates;
- feasible realization;
- score expansion;
- outer bound;
- inner bound;
- uniformity;
- exclusion of other components.

The present proof is too compressed for such a central theorem.

### R102.8 — Complete the native source-bound receipt

Let run 35500287312 finish or rerun the exact source-bound job.

Commit the successful receipt, logs, and hashes to the revision branch if the job passes.

Do not claim closure before the durable receipt exists.

## 16. Editorial comments

1. “Complete metric contact data” sounds stronger than the theorem’s actual novelty. Consider a title that does not conflate convex completeness with singularity classification.

2. The abstract should say more explicitly that the sharp \(k(k+1)/2\) lower bound is over the variable positive-definite metric class, not the fixed Hellinger family.

3. The term “information” should be used carefully. The ray-query oracle is a theoretical variational oracle after exact centre identification.

4. Theorem 3.5 should cite the classical parametric-QP active-set literature.

5. The paper should not use the 2-by-2 endpoint example as the main evidence of a new quotient theory. A classification theorem is needed.

6. The polynomial wall theorem should advertise its true strength: uniform relative control through exact cancellation. That is stronger and more precise than broader “singular wall” rhetoric.

7. The probability realization should be presented as an embedding theorem, not as evidence that the general stochastic model has been classified.

8. Appendix A should separate what is assumed about a supplied real monomial presentation from what is guaranteed by external resolution/rectilinearization theorems.

9. The supporting volume is useful for repository preservation, but the principal paper must remain independently reviewable without asking the referee to accept the archive as a black box.

10. The current principal source is short enough that a full theorem-by-theorem literature comparison should be added directly.

## 17. Originality and depth assessment

Revision 102 has made the mathematical architecture much easier to judge.

That is progress.

The principal contributions now fall into four recognizable classes.

### 17.1 Definable asymptotic minimization

The exponent, minimizing arcs, and leading metric coefficients belong to tame/semialgebraic asymptotic analysis.

The new envelope packages all metric coefficients simultaneously.

The package is clean, but the new structure is currently convex rather than singularity-theoretic.

### 17.2 Finite-dimensional quadratic inverse geometry

The local quotient forms are meaningful outputs of the binary inverse problem.

But once the form \(Q\) is present, full-class finite recovery and the deterministic adaptive lower bound are standard linear algebra.

The genuinely difficult problem is the restricted model-generated family.

### 17.3 Parametric convex quadratic elimination

The endpoint-effective metric is exactly the value function of a strictly convex parametric QP over an orthant.

This is the correct object, but its piecewise-quadratic form is classical.

The new problem is to classify the quotient induced on \(Q\).

### 17.4 One-dimensional cancellation-uniform contact

This is the most distinctive new piece.

The relative estimate through arbitrary finite polynomial cancellation is elegant.

But it is still a narrow normal form.

The paper has not yet proved that this normal form is universal or structurally unavoidable in the broader theta-theory observation program.

For a specialized journal, the collection could be substantial.

For a top-four general mathematics journal, I would expect one of these four mechanisms to be pushed to a theorem that changes how the underlying inverse/singularity problem is understood.

That theorem is not yet present.

## 18. Final assessment

Revision 102 is a mathematically serious response to revision 101.

It resolves several earlier objections honestly and constructively:

- the finite scalar object is now correctly identified as an oracle;
- exact probe sufficiency and necessity are separated;
- deterministic adaptive lower bounds are proved on the declared full metric class;
- endpoint invisibility is handled by the correct partial-minimum invariant;
- the divisor list is no longer called canonical;
- a real cancellation-uniform family-level wall theorem is proved;
- the principal article is no longer a historical accumulation.

I found no direct counterexample to the principal theorems.

I nevertheless recommend **rejection in the present form** for an Annals / Acta / Inventiones / JAMS-level general mathematics journal.

The reason is now more fundamental than in v101.

The revision has finally exposed a clean mathematical core, but that core is not yet deep enough relative to known mechanisms:

- convex separation explains the metric-envelope reconstruction;
- dimension counting and polarization explain the full-class finite probe theorem;
- active-set quadratic programming explains the endpoint-effective metric;
- a one-dimensional divided-difference/shear argument explains the cancellation wall;
- classical Łojasiewicz/integral-closure theory still explains the exponent.

The paper needs one additional conceptual jump, not another incremental extension.

The most promising routes are:

1. classify the realizable metric contact envelopes and connect their extremal geometry to singularity data;
2. solve the sharp finite-information problem for the actual fixed-Hellinger model-generated quotient family;
3. classify the endpoint quotient \(Q\mapsto G_Q\);
4. prove a broad normal-form theorem that makes the cancellation polynomial universal for a substantial class of singular polynomial observations.

If one of those succeeds, the existing exact inverse and wall machinery could support a genuinely stronger top-journal submission.

Until then, revision 102 is cleaner and more coherent than v101, but it still falls short of the originality/depth threshold claimed by the target journal class.
