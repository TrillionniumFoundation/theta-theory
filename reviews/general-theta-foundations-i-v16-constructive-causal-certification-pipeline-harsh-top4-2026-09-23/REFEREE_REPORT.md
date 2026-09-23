# External Pipeline-Aware Harsh Referee Report

## General Theta Foundations I: Constructive Causal Deficiency and Physical Testing — sixteenth revision

**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed branch:** `revision/general-theta-foundations-i-v16-constructive-causal-certification-referee-ready-2026-09-23`  
**Reviewed HEAD:** `5941223e297f6c54583d729cc292831c183277e9`  
**Immediate complete mathematical base:** v15 certified-physical-comparison, `09d5540897d592a5e434f7431bfff470b4ebad1a`  
**Review date:** 23 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica level  
**Review type:** independent, external-referee-style, pipeline-aware harsh audit

**Provenance note.** This is an owner-requested, AI-assisted external-referee-style assessment. It is not a report commissioned by a journal. I reviewed the frozen v16 source, the new theorem files, the v13--v15 theorem spine that v16 imports, the response and proof ledgers, exact-arithmetic evidence, prior harsh reports, and the repository-wide Round-Seventeen dependency materials. I also made targeted external literature checks where the claimed novelty boundary matters.

---

# Recommendation

## Reject in the present form at the requested top-four general-mathematics standard

This recommendation is **not** based on finding a one-line contradiction in the main finite theorem. On the contrary, after re-deriving the main inequalities, I regard the new finite power-weighted/Bernstein certificate as mathematically plausible at the stated fixed finite rational scope, and the explicit two-time example checks out. I also independently recomputed the new physical scalar value:
[
d(	au)approx 0.20580912288771521416,
]
which lies inside the deposited rational enclosure, and the private two-time optimum agrees with (sqrt2-1).

The reason for rejection is more serious at this venue level: **the sixteenth revision still does not contain a top-four-scale theorem whose conceptual depth matches the title, physical rhetoric, and repository-wide foundational role being claimed.**

The new mathematics consists principally of:

1. an endogenous power-weighted approximation of a finite maximum, followed by a classical Bernstein-basis positivity certificate on a cube;
2. a two-time nonconvex example showing why a fixed convex mixture of tests can miss a private-resource obstruction;
3. a highly solvable hard-sphere collective coordinate whose entire evolution is governed by conserved total momentum;
4. the composition of that finite lower certificate with the already-existing v15 physical-presentation theorem;
5. an elementary sharp total-variation-to-log-moment bound.

These are coherent contributions. They are not, in my judgment, sufficient for the requested journal tier. Most importantly, the physical example eliminates the difficult collision dynamics rather than confronting them, the explicit marked-deficiency example does not physically realize the private/hidden/visible resource separation that motivates the paper, the v16 physical certification theorem is substantially inherited from v15, the strongest downstream B4 kinetic gate remains explicitly open, and the closest positivity-certificate literature is not yet compared at theorem level.

I would therefore **not recommend another minor-revision cycle** on this manuscript at the requested venue. A future top-tier submission would need a qualitatively stronger theorem, not additional certificates around the present architecture.

---

# 1. Exact submission object and what is genuinely new in v16

Unlike the earlier mislabeled v15 branch that prompted the previous report, this v16 branch is a real materialized revision. The source package is present, builds are recorded, the response-to-referee is explicit about what was and was not available, and the review-ready ref is frozen.

The Git comparison from the complete v15 head
`09d5540897d592a5e434f7431bfff470b4ebad1a`
to the reviewed v16 head
`5941223e297f6c54583d729cc292831c183277e9`
shows five commits and a complete new v16 package. This is a substantial improvement in submission integrity.

However, the mathematical delta must be described accurately. The v16 canonical core imports, essentially unchanged:

- v13 intrinsic deficiency;
- v14 local certificates and residual certificates;
- v15 behavior-dimension witnesses;
- v13 endogenous tasks and regenerative risks;
- v15 task tolerance;
- v13 active hard spheres;
- v15 finite report presentations;
- v15 enriched convergent certificates;
- v15 constructive collision charts;
- v15 same-budget physical certification;
- v15 physical data.

The genuinely new theorem files are concentrated in:

- `nonlinear-testing.tex`;
- `collective-hard-spheres.tex`;
- `physical-testing.tex`.

This distinction matters because the abstract and introduction can leave the impression that v16 newly establishes the entire physical certification chain. It does not. The end-to-end stateless physical-to-finite-rational bridge, the convergent enriched analytic certificate, and the constructive fixed-particle collision-chart integration machinery were already v15 results.

The v16 strengthening is therefore narrower:

- replace/augment the v14 local finite lower certificate by a global positive-polynomial certificate;
- give a particularly explicit collective physical class with a closed approximation rate and exact marked scalar deficiency;
- compose the new finite lower certificate with the inherited v15 bridge;
- add the exponential transfer estimate.

That is a valid revision. It is also a substantially more incremental revision than the title and top-four positioning suggest.

---

# 2. Audit of the new finite theorem: technically credible, conceptually overstated

Theorem `thm:v16-dual` is the strongest genuinely new finite statement.

For a fixed finite resource signature, the feasible simulator rows are parameterized polynomially by a cube through stick breaking. If
[
F(q)=max_i f_i(q),qquad h_i(x)=f_i(q(x)),qquad g_i=(1+h_i)/2,
]
then the manuscript defines
[
A_p(x)=rac{sum_i g_i(x)^p h_i(x)}{sum_i g_i(x)^p}.
]
Pointwise, this is a power-weighted average concentrating on the largest (g_i), hence on the largest (h_i). The proof obtains
[
0le max_i h_i-A_ple 2(1-m^{-1/(p+1)})
   le rac{2log m}{p+1},
]
and monotonicity in (p) follows from log-convexity of the power sums. Taking minima gives convergence to the original nonconvex deficiency without convexifying the feasible behavior image.

I find this argument sound at its stated scope.

The Bernstein step is also standard-looking and correctly used. A strictly positive polynomial on the cube has eventually positive tensor Bernstein coefficients after degree elevation; the manuscript supplies an elementary explicit (O(1/n)) coefficient-to-grid-value bound and obtains a finite exact rational certificate for every strict rational lower level.

The problem is **not correctness**. The problem is the way this result is being asked to carry the paper.

## 2.1 This is not a duality theorem in the usual mathematical sense

The displayed identity is an exact approximation of a pointwise finite maximum by candidate-dependent power weights. There is no independent dual feasible object, no minimax exchange, no separation theorem over the original nonconvex set, and no dual attainment statement.

Calling it an “endogenous polynomial testing dual” is understandable as terminology internal to the paper, but at top-four level it risks overstating the conceptual content. The new weights are a smooth/power approximation to (max_i h_i(x)), followed by universal quantification over (x). That is useful, but it is much closer to a certificate transform than to a new duality theory.

The paper should either:

- formulate a genuine resource-sensitive dual object with an independent variational meaning; or
- call the result what it is: a complete positive-polynomial lower-certificate scheme for the original nonconvex resource image.

## 2.2 The “constructive” content is qualitative semidecision, not useful quantitative complexity

The certificate is finite and exact, but the dimension (D), number of event tests (m), power (p), polynomial degree, Bernstein degree (n), and coefficient count can all explode.

Even in the small two-variable example the deposited certificate uses:

- power (p=12);
- degree 96 in each coordinate;
- 9,409 exact Bernstein coefficients.

For a real causal experiment, (D) contains every stochastic-row coordinate and (m) contains the finite marked feedback event family. The generic certificate count ((n+1)^D) is potentially enormous.

The manuscript is honest that it makes no polynomial-time claim. That honesty should be retained. But then the word “constructive” should not be allowed to do conceptual work that the theorem does not support. What is proved is termination of a dovetailed search under fixed finite rational data, not an end-to-end complexity theorem with meaningful scaling.

At top-four level, one would want a structural result controlling at least one of:

- certificate support;
- algebraic degree;
- bit complexity;
- horizon dependence;
- resource-width dependence;
- intrinsic behavior dimension rather than raw row dimension.

The inherited v15 witness-dimension theorem goes part of the way for the number of tests. V16 does not combine that theorem with the Bernstein construction into a sharp global complexity statement.

## 2.3 The two-time example is correct and useful, but it is an example, not the missing conceptual theorem

For the target ((0,0)/(1,1)) mixture and private width-one simulator with independent Bernoulli parameters (p,q), the objective
[
max{0,	frac12-pq,	frac12-(1-p)(1-q),p+q-2pq}
]
does indeed have minimum (sqrt2-1). A hidden two-valued selector reproduces the target exactly, while an exposed selector does not erase the fiberwise obstruction. The target also lies in the convex hull of private deterministic behaviors, so a fixed constant test mixture cannot separate it.

This is the right example to demonstrate why naïve convexification is wrong.

But the example proves only that the paper's resource distinction is real. It does not establish that the power/Bernstein mechanism is a deep or uniquely natural resolution. A top-four paper would need a broader theorem revealing the geometry of the nonconvex resource image, not only a complete but potentially enormous positivity certificate.

---

# 3. A serious novelty-boundary problem: the closest Bernstein positivity literature is missing

The manuscript says that Bernstein positivity and degree elevation are classical, but its reference list does not directly engage the literature that already proves constructive hypercube positivity certificates and degree/error bounds.

A particularly relevant omitted comparison is:

E. de Klerk and M. Laurent,  
“Error Bounds for Some Semidefinite Programming Approaches to Polynomial Minimization on the Hypercube,”  
SIAM Journal on Optimization 20 (2010), 3104--3120,  
doi:10.1137/100790835.

That paper explicitly uses multivariate Bernstein approximations to obtain constructive positivity certificates and degree/error bounds for polynomial minimization on the hypercube.

I am **not** claiming that de Klerk--Laurent contains the present causal resource theorem. It does not, on the evidence inspected. The point is the opposite: because the algebraic engine is already a developed classical technology, the present paper must isolate exactly what is new after importing that technology.

At minimum the revised literature section must compare:

1. the manuscript's coefficient formula and (O(1/n)) elevation bound;
2. known Bernstein positivity/degree bounds on the cube;
3. Positivstellensatz/SOS alternatives for the same finite nonconvex optimization;
4. what the causal-resource structure adds that those generic polynomial-optimization tools do not already give.

Without that comparison, the paper's principal v16 theorem cannot yet support a top-four novelty claim.

---

# 4. The hard-sphere realization is mathematically valid but dynamically degenerate

The new collective construction is presented as the place where a nonconserved collision-compatible observable, a nonzero generator residual, and a positive exact marked deficiency finally coexist.

The formulas appear correct. Let
[
artheta=rac{2pi}{ell}sum_i q_{i,1},qquad
X=N^{-1/2}sum_i v_{i,1},qquad
f=cosartheta.
]
Elastic collisions conserve total momentum, so
[
U(t)f=cos(artheta+omega Xt).
]

This is exactly the issue.

The difficult hard-sphere interaction disappears from the observable dynamics. The evolution factors through the center-of-mass angle and conserved total momentum. The collisions are present in the ambient phase space, but they do no mathematical work in the displayed orbit formula.

The same effective model can be represented by a one-angle/one-Gaussian latent system:
[
(artheta,X)mapsto(artheta+omega Xt,X).
]
The sphere diameter, collision graph, recollision geometry, collision frequency, and nonlinear hierarchy never enter the exact deficiency calculation.

Therefore the phrase “interacting hard-sphere realization” is literally true but mathematically misleading if used as evidence that the certification machinery has penetrated interacting collision dynamics.

## 4.1 The nonzero residual does not cure this degeneracy

The residual
[
R=omega^2
]
is nonzero because (Lf) leaves the one-dimensional span of (f). It is not a collision-generated residual. The same residual appears for free transport on the reduced ((artheta,X)) system.

Thus v16 succeeds in putting “positive deficiency” and “nonzero graph residual” into the same ambient hard-sphere model, but only by choosing a collective mode on which the collision mechanics cancel exactly.

This is a cleaner example than v15. It is not a harder physical theorem.

## 4.2 The (2^k	o k+1) word reduction is also a consequence of the same degeneracy

The global reversal actions act only by changing the sign of the conserved total momentum. The controlled word therefore collapses to a signed clock:
[
s(w)=Deltasum_jprod_{ile j}a_i.
]
The (k+1) distinct mean functions are a consequence of this one-dimensional conserved coordinate.

Again this is mathematically useful, but it should not be sold as evidence that the general feedback/collision combinatorics have been controlled. They have been bypassed by symmetry.

---

# 5. The exact physical deficiency does not realize the paper's resource-sensitive obstruction

This is the most important conceptual mismatch in the physical part.

In `thm:v16-exactphysical`:

- there is no informative earlier report;
- the action is chosen before the informative acquisition;
- (X) is symmetric and independent of the initial mark (W=operatorname{sgn}cosartheta);
- global reversal does not change the joint law relevant to the deficiency;
- every source-generated report remains independent of (W), conditional on any independent selector.

Consequently the same scalar deficiency holds for every nonempty finite private, hidden-selector, and visible-selector signature.

That is a valid theorem. It is also a theorem in which the **resource architecture is inert**.

The lower bound is fundamentally a static marked-dependence obstruction: the target has dependence between (W) and (Y), while the source simulator cannot access (W). Consumer memory does not matter. Hidden persistent selection does not help. Exposed selection does not help. Feedback does not matter. The action law is symmetry-invariant.

This means the paper has two separate examples:

- the finite two-time example realizes the private/hidden/visible nonconvex resource gap, but has no hard-sphere physics;
- the physical example realizes a positive marked deficiency and nonzero one-dimensional residual, but the private/hidden/visible distinction collapses.

The paper repeatedly suggests that the finite resource obstruction and physical realization have been “joined.” At theorem-composition level they have. At the level of an explicit nontrivial example they have **not**.

A decisive physical example should exhibit, in the same controlled microscopic system:

1. a genuinely collision-sensitive observable;
2. feedback that changes future information;
3. a strict private/hidden/visible resource separation;
4. a same-budget lower certificate;
5. a convergent physical presentation with explicit errors.

V16 does not provide this.

---

# 6. V16's “main physical theorem” is substantially a corollary of v15

Theorem `thm:v16-main` states that a finite Bernstein lower certificate (L) and same-budget finite upper table (U), together with two-sided stateless presentation errors (a_j,c_j), transfer to
[
max{0,L-a_j-c_j}ledelta_{mathfrak b}(E,F)
lemin{1,U+a_j+c_j}.
]

This is correct.

But the same physical stability and same-budget composition statement was already the core of `thm:v15-main`. V15 had:

- active Gaussian physical acquisitions;
- convergent enriched trial presentations;
- finite report quantization;
- rational marked-tree construction;
- two-sided stateless comparison;
- local finite lower certificates;
- executable upper row tables;
- effective collision-chart integration;
- convergence of the physical intervals.

V16 swaps in the new global polynomial lower certificate and gives a special class with an explicit analytic rate.

That is a meaningful strengthening of the finite certificate layer. It is not a new physical certification principle.

For clarity and scholarly accuracy, the paper should state a proposition of the form:

> V16 strengthens the finite lower-certificate module of the v15 same-budget physical certification theorem; the physical transfer inequality itself is inherited.

At present the theorem naming and surrounding prose blur that distinction.

---

# 7. The exponential-transfer theorem is correct but far below the advertised downstream kinetic target

Theorem `thm:v16-exponential` gives
[
left|rac1etalog E_Pe^{eta h}
-rac1etalog E_Qe^{eta h}ight|
le
rac1etalog{1+arepsilon(e^{etaoperatorname{osc}(h)}-1)}.
]

This is a useful and sharp bookkeeping inequality. It follows directly from the total-variation expectation bound applied to (e^{eta h}).

The manuscript itself correctly says that this is not a large-deviation theorem. I agree.

But the pipeline rhetoric still asks this estimate to serve as a “B4 edge.” That should be treated with extreme caution.

The Round-Seventeen B4 gate in the repository requires, among other things:

- compact dynamic-action sublevels;
- state-dependent multiplier transfer;
- a Nisio resolvent identity;
- m-dissipativity;
- one diagonal hierarchy/graph-core corrector;
- nonlinear Trotter--Kato convergence.

The v16 pipeline checker itself records:
`full_historical_B4_closed: false`.

A sharp TV-to-log-MGF estimate at fixed particle number does not materially close these kinetic analytic steps. It tells the author what accuracy a presentation would need if an exponential scale is already specified. It does not construct the large-deviation action, establish exponential tightness, prove particle-uniform recollision estimates, or identify a nonlinear limiting semigroup.

Therefore the B4 edge should be described as an **accuracy-transfer prerequisite**, not as a substantive kinetic bridge.

---

# 8. Repository-wide pipeline audit: GTF-I remains an interface paper, not the foundation from which the hard eleven-paper chain follows

I reviewed the Round-Seventeen historical derivation audit and proof-dependency ledger.

The repository's own noncircular hard-sphere chain is:
[
	ext{B2-GC}	o	ext{B1}	o	ext{B2-MC}	o	ext{B3}	o	ext{B4}
	o	ext{C1/C2}	o	ext{D1}.
]

The B4 gate is already strong enough to make the point: it requires hierarchy realizability, compact dynamic action, nonlinear resolvent theory, m-dissipativity, a diagonal corrector, and nonlinear Trotter--Kato.

The GTF-I v16 theorem does not prove these.

Likewise, the Sinai chain
[
	ext{A2}	o	ext{A3}	o	ext{A4}	o	ext{C2}	o	ext{D1}
]
contains hard geometric/spectral/response theorems not consequences of the resource-comparison machinery.

The v16 history audit is commendably honest about this. The paper should follow that honesty consistently and stop using “foundations” language as if typed adapters were theorem-generating implications.

At present GTF-I is best understood as a **comparison/certification interface theory** that can consume rigorously supplied finite-horizon physical data. That is potentially valuable. It is not yet the mathematical foundation from which the full repository pipeline is derived.

For a top-four submission bearing the title “General Theta Foundations I,” I would expect at least one historically hard downstream theorem to become shorter, stronger, or newly provable specifically because of the GTF machinery. V16 still does not demonstrate that.

---

# 9. The closest filtered-experiment priority boundary remains incomplete

The literature audit explicitly admits that the original Norberg text was not inspected at proof level.

That is not acceptable as a stable publication boundary for a paper whose main conceptual claim concerns resource-sensitive causal/filtered comparison.

Norberg's published article is:

E. Norberg, “Comparison of Statistical Experiments with Filtered Probability Spaces,”  
Statistics & Risk Modeling 20 (2002), 1--28,  
doi:10.1524/strm.2002.20.14.1.

Its published abstract explicitly concerns sequential actions while observing a parameter-dependent stochastic process and gives several equivalent expressions for filtered deficiency/risk comparison. That makes it directly relevant.

The manuscript does a serious comparison with Weisshaupt. That is not a substitute for reading Norberg's theorem and proof.

The required comparison is not “does Norberg already prove the present finite-state theorem verbatim?” The required comparison is:

- what is Norberg's exact filtered deficiency object?
- what comparison/randomization kernels are allowed?
- where is persistent state charged or uncharged?
- what role does external randomization play?
- what are the exact risk-duality statements?
- can a finite-state constraint be inserted into Norberg's proof or not?
- which part of v13--v16 is genuinely new after this comparison?

Until this is answered, the novelty claim remains provisional.

The same principle applies, though less centrally to v16, to Paull--Unger and the compatible-cover/state-minimization lineage.

---

# 10. The physical computability theorem is impressive as an existence algorithm, but does not rescue top-four significance

I re-read the inherited v15 constructive collision-chart theorem because v16 repeatedly relies on it.

The full-measure regular-chart exhaustion is a serious attempt to turn “almost everywhere hard-sphere flow” into an effective integration procedure. It carefully handles:

- nongrazing simple binary collisions;
- rational box margins;
- Gaussian velocity cutoffs;
- algebraic kicks;
- null exceptional sets;
- computable configuration normalization;
- time-integrated graph-core functions;
- marked Gaussian prefix masses.

This is one of the more ambitious inherited pieces.

But v16 does not add a new hard result here. Its explicit collective example avoids this machinery almost entirely by reducing to a Gaussian/circle calculation.

Thus the strongest constructive-physics theorem remains inherited from v15, while the strongest v16 explicit example is exactly the one for which collision-chart complexity is unnecessary.

That mismatch reinforces the main editorial conclusion: the revision has improved explicitness, not deepened the hard physical analysis.

---

# 11. Proof/certificate evidence: useful, correctly scoped, but not a substitute for theorem novelty

The evidence package is unusually disciplined.

The verifier states that it is not an analytic proof checker. The negative controls catch several intended mutations. The polynomial certificate is exact rational arithmetic. The physical interval uses rational enclosures for (pi), exponentials, square roots, and the series remainder.

I spot-checked the key numerical conclusions independently and found them consistent.

This is good reproducibility practice.

It should not, however, be counted as evidence of top-four mathematical depth. A 9,409-coefficient exact certificate can verify one instance without explaining the geometry of the general theorem. Likewise, a narrow rational interval for a scalar deficiency verifies the calculation but does not make the hard-sphere interaction essential.

The manuscript mostly respects this distinction already. The submission rhetoric should respect it everywhere.

---

# 12. Manuscript architecture and exposition

The canonical v16 article is more coherent than the complete-development archive, but the source still imports theorem bodies across several historical revision directories.

For repository preservation this is sensible. For a journal submission it creates two problems.

First, it obscures which claims are new and which are inherited. A reader sees a long integrated paper and must use Git history to know the actual contribution.

Second, the “complete development” contains historical introductions and earlier bodies that should not be part of the review object for a conventional journal.

I recommend that any future submission have:

- one clean self-contained source tree;
- one theorem dependency map in an appendix;
- explicit tags “new in this paper” versus “recalled from previous work” only if there truly are prior published works;
- no reliance on repository chronology to establish novelty or logical dependence.

The issue is not page count alone. It is mathematical identity.

---

# 13. Major requirements for any future top-tier reconsideration

I would regard the following as blocking.

## E16.1 — Close the novelty boundary for the finite certificate theorem

Give a proof-level comparison with Bernstein positivity and polynomial optimization on the hypercube, including de Klerk--Laurent and related Positivstellensatz/Bernstein certificate results. State precisely what is new after those tools are subtracted.

## E16.2 — Stop calling the power-weight identity a “dual” unless a genuine dual object is supplied

Either develop a true resource-sensitive duality theorem with an independent variational object, or rename the result as a complete positive-polynomial certificate hierarchy.

## E16.3 — Produce a genuinely resource-sensitive physical example

The same microscopic experiment should exhibit a strict difference between at least two of private, hidden-selector, and visible-selector deficiencies. The distinction should depend on causal information/memory, not merely on a hidden mark inaccessible to all simulators.

## E16.4 — Make the physical observable genuinely collision-sensitive

The central observable should not factor through conserved center-of-mass momentum so that all collision mechanics disappear. At least one quantitative certificate must use collision geometry in an essential way.

## E16.5 — Isolate the exact mathematical strengthening over v15

State which part of `thm:v16-main` is inherited and which part is new. Do not present the v15 physical transfer principle as a v16 discovery.

## E16.6 — Either close a hard downstream pipeline gate or sharply limit the foundation claim

A convincing route would be a particle-uniform theorem that feeds a genuine B4 hypothesis, not merely a fixed-(N) TV-to-log-MGF accuracy estimate. If that is not done, the title and pipeline language should not imply that the eleven-paper hard analytic chain is founded by this theorem.

## E16.7 — Complete the Norberg comparison

Obtain and read the 2002 published article at proof level. Crosswalk definitions, kernels, sequential decision timing, risk criteria, and randomization exactly.

## E16.8 — Give quantitative meaning to “constructive” or narrow the term

At least one nontrivial complexity or certificate-size theorem should be proved in intrinsic parameters. Otherwise the strongest correct description is effective/dovetailed certification for fixed finite rational signatures.

---

# 14. Technical comments

1. **Terminology of tests.** In the two-time example, formalize exactly what class of “constant test mixtures” is being ruled out and how the empty event is treated. The current argument is understandable, but this point is central enough to deserve a standalone definition.

2. **Visible selectors.** In every theorem that says the visible case is unchanged, keep the joint reference selector law explicit in the theorem statement rather than relying on inherited conventions.

3. **Exact physical theorem.** Spell out in the statement that the action is chosen before any informative report and that action symmetry makes the relevant marked target law invariant. This makes clear why all resource signatures have the same value.

4. **Hard-sphere wording.** Replace any phrasing that might suggest collision-induced mixing or recollision control. The new mode is collision-compatible but collision-insensitive.

5. **Residual interpretation.** Clarify that (R=omega^2) is the projection residual of the chosen one-dimensional trial space, not a measure of interaction strength.

6. **Bernstein literature.** Add explicit citations for positivity under degree elevation, multivariate coefficient bounds, and hypercube optimization. “Classical” without a citation is insufficient because this mechanism is now the centerpiece of v16.

7. **Certificate complexity.** Report (D,m,p,n,(n+1)^D) symbolically in the main theorem discussion so readers can see where the combinatorial explosion enters.

8. **End-to-end rate.** For the collective mode, the analytic Taylor rate is explicit but the finite rationalization and polynomial-certificate stages are still only effective. Do not call the whole end-to-end procedure quantitatively explicit unless all stages have quantitative bounds.

9. **Exponential transfer.** The sharpness example is static. Do not infer any large-deviation or nonlinear-semigroup sharpness from it.

10. **Pipeline graph.** Preserve the current field `full_historical_B4_closed: false`. It is an important correction against overclaiming.

---

# 15. What I would regard as a genuinely decisive next theorem

There are two credible routes.

## Route A: make the finite resource theory deep enough to stand alone

Prove a structural theorem about the original nonconvex causal behavior image that is not simply generic polynomial positivity. Examples of the right scale would be:

- an intrinsic geometric dual object;
- a sharp certificate-support theorem;
- a dimension/width law for private versus hidden versus visible resources;
- a nontrivial lower/upper complexity classification;
- a theorem connecting positive-error state complexity, universal continuation state, and causal congruence.

Then the hard-sphere material can be an application rather than part of the novelty burden.

## Route B: make the physical bridge genuinely hard

Construct a collision-sensitive microscopic acquisition for which:

- the interaction changes the informative observable;
- feedback changes future information;
- a private/hidden/visible gap survives;
- the same-budget certificate is explicit;
- the approximation is controlled in a scaling relevant to B4.

A particle-uniform or kinetic-scaling theorem would transform the significance of the paper.

At present the manuscript does neither.

---

# 16. Final assessment

Revision v16 is materially better than the inherited v14 object that motivated the earlier harsh reports.

Several previous technical blockers have in fact been addressed:

- the physical-to-finite-rational same-budget bridge exists in v15 and is retained;
- the enriched analytic estimator has a convergence proof;
- constructive fixed-particle collision-chart data are supplied;
- the new finite lower certificate no longer requires exhaustive policy-cell localization for its logical completeness;
- the new explicit physical example puts a nonzero trial residual and a positive exact marked deficiency in one ambient hard-sphere model;
- the branch and evidence provenance are much cleaner.

Those improvements should be credited.

They do **not** change my top-four recommendation.

The v16 finite theorem is, at core, a power approximation to a finite maximum plus classical Bernstein positivity. The explicit physical theorem is built on a collective mode whose dynamics are exactly controlled by conserved total momentum, so collisions are analytically inessential. The physical example does not realize the private/hidden/visible resource obstruction. The new main physical interval theorem substantially reuses v15. The exponential transfer estimate is elementary and does not close the repository's nonlinear kinetic gate. The B4 historical target remains open by the paper's own ledger. The closest filtered-experiment and Bernstein-positivity priority comparisons remain incomplete.

Accordingly, I would not recommend publication of this manuscript in its present form at Annals of Mathematics, Inventiones Mathematicae, Journal of the AMS, or Acta Mathematica level.

The work contains serious mathematics and a disciplined reproducibility layer. What it presently lacks is the one theorem that would make the package unavoidable at that level.
