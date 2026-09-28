# Independent harsh referee report on A2 revision 100

**Manuscript:** *Projective polynomial observations: real weighted degenerations and identification walls*  
**Reviewed branch:** revision/a2-v100-canonical-degeneration-and-singular-entrances-2026-09-20  
**Reviewed exact head:** 7407ad098cac70ac07bb7d9d01f562890041cada  
**Principal entrypoint:** papers/A2-v17-boundary-information-coarsening/rigidity_v100.tex  
**Principal article source:** papers/A2-v17-boundary-information-coarsening/article/v100/paper.tex  
**Controlling prior report:** reviews/a2-v99-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md  
**Controlling prior review commit:** 5485ed6d127b8443fce059db118dc215b68e283a  
**Prior reviewed paper head:** c49c6d0604f83badf47b32dfdf25dc043b4117ef  
**Date:** 2026-09-20

## 1. Recommendation

**Recommendation for an Annals / Acta / Inventiones / JAMS-level general mathematics journal: reject in the present form.**

This is not a rejection based on a counterexample to a principal theorem.

Revision 100 is a serious revision. It responds to the preceding report with actual mathematics rather than only editorial repair. I found no direct contradiction in the new weighted-tangent comparison, the quadratic-probe reconstruction formula, the binary full-model valuative example, or the general semialgebraic entrance theorem under their stated hypotheses. The exact finite calculations are also now accompanied by a source-pinned diagnostic package rather than asserted only in prose.

The difficulty is now more fundamental.

Revision 99 was rejected because the paper had not yet shown that its general machinery produced a canonical, structurally new theorem at the scale required by a top-four general journal. Revision 100 tries to solve precisely that problem. It adds

1. a positive-real weighted tangent relation;
2. filtered naturality;
3. reconstruction from quadratic scalar probes;
4. a full binary-model example with identical scalar order data but different leading metric geometry;
5. a finite rational entrance-order theorem without a regular-corner hypothesis;
6. realization of every rational entrance order at varying format.

These are the right topics to address. But, in my assessment, the newly added theorems still do not supply the missing top-four-level conceptual jump. Several of them are consequences of very general facts once the relevant object is defined:

- the new weighted tangent relation is defined by essentially the same positive rescaling closure used to define the old joint initial fibre;
- a compact set is determined by its distance function, so reconstruction from quadratic distance probes is a universal metric fact;
- two positive-definite analytic local metrics have the same orders on every analytic arc while their unit balls and metric constants can differ;
- a one-variable semialgebraic minimum has a Puiseux-type rational leading order, and its eventual sign relative to another semialgebraic germ is decidable after stratification.

Revision 100 therefore closes many literal referee requests while leaving the central significance question open:

> What theorem here is both specific enough to be genuinely new and broad enough to reorganize the subject, rather than an application of standard weighted degeneration, semialgebraic geometry, distance-function reconstruction, and one-variable Puiseux behavior to a carefully designed inverse problem?

The strongest genuinely distinctive mathematics still appears to me to be the concrete binary/cubic analysis inherited from revisions 98–99: the full-rank multiplicity law, the exact rank-deficient cubic fibre, the cross-rank inverse, and the two identification walls. Those results have substance. The new v100 abstract layer does not yet elevate them into a general theory of comparable depth.

## 2. Scope of this report

I reviewed the exact source head

7407ad098cac70ac07bb7d9d01f562890041cada.

Relative to the reviewed v99 paper head c49c6d0604f83badf47b32dfdf25dc043b4117ef, v100 is four commits ahead. The comparison is addition-only. It adds the v100 article files, exact diagnostic record, validation scripts, source manifest, response to the referee, workflow, and the preceding v99 report without modifying the inherited v99 mathematical source.

I treated the principal v100 article as the mathematical object under review and the repository package as reproducibility evidence. I did not treat a passing finite regression as evidence for a universal theorem.

My standard is deliberately severe. A theorem can be correct, nontrivial, and publishable while not meeting the originality, inevitability, and conceptual concentration expected in the four general journals named above.

## 3. Executive diagnosis

The revision has made the conceptual situation clearer.

### 3.1 What is now credible

The manuscript has a coherent hierarchy:

- a relative semialgebraic/resolution atlas produces rational weights and uniform asymptotic data;
- the actual positive-real weighted relation retains feasibility lost by an unconstrained algebraic initial ideal;
- the root-image diameter of its observation-unit section gives the leading spectral modulus;
- full-rank binary models admit explicit Fisher/multiplicity laws;
- the rank-deficient cubic model has a complete exact fibre and two distinct identification walls;
- remote exact representatives have semialgebraic entrance germs, regular or singular.

This is substantially more mature than earlier versions.

### 3.2 What remains unconvincing at the top-four level

The conceptual centre is still unstable.

The paper now labels the joint limit as a positive-real weighted tangent relation, but the main comparison theorem largely says that the previously defined fixed-centre rescaling limit equals the newly defined rescaling limit.

The reconstruction theorem gives exact scalar sufficiency, but it uses a distance function that determines every closed set in every metric space.

The valuative separation theorem is stronger than the old marginal example, but its mechanism is the elementary and ubiquitous fact that valuation/order data erase positive units.

The singular entrance theorem is broader than the old regular-corner theorem, but its rational exponent is a standard consequence of semialgebraicity of the minimum function; it is not a classification of singular entrances in terms of intrinsic singularity data.

Thus the revision has improved correctness, auditability, and logical closure more than it has improved the scale of the new mathematical principle.

## 4. What revision 100 genuinely fixes from revision 99

A fair harsh review must distinguish closed objections from merely renamed ones.

### 4.1 The weighted object is now compared with a standard algebraic construction

Theorem thm:canonical explicitly identifies the algebraic special fibre with the weight-initial ideal after saturation by the scale variable and separates that algebraic object from the positive-real liftable part.

This is a real improvement. The paper no longer presents the weighted algebraic deformation itself as a new operation.

### 4.2 Real liftability is stated correctly

The cusp example y^2=x^3 with equal weights is a clean illustration: the algebraic special fibre contains both signs on the x-axis, whereas positive-real liftability retains only x>=0.

This example does what it is supposed to do.

### 4.3 A naturality statement has been added

Theorem thm:filtered-naturality makes explicit the conditions under which filtered coordinate changes transport the weighted tangent relation and its decoded spectral image.

This closes an important ambiguity about coordinate dependence.

### 4.4 The paper now states a positive scalar reconstruction theorem

Theorem thm:reconstruction prevents the manuscript from making an overbroad claim that “scalar information is insufficient.” It correctly distinguishes scalar orders from richer scalar values.

### 4.5 The scalar-separation example is now inside the principal binary experiment

This is materially better than the disconnected-label construction in v99. All model parameters remain unknown, the centres are interior and full rank, and the exact Fisher ellipsoids are computed.

### 4.6 The remote theory no longer assumes a regular corner

Theorem thm:singular-entrances treats the distance-to-remote-component germ directly as a semialgebraic value function. This is a legitimate generalization of the regular metric-projection calculation.

### 4.7 The regular corner has been repositioned against variational analysis

The discussion now cites Rockafellar–Wets and Bonnans–Shapiro and no longer presents metric projection itself as a new operation.

### 4.8 Geometric-certificate effectivity has been demoted

The direct first-order output algorithms are now separated from the supplementary existence-by-enumeration certificate search. This is the right correction.

### 4.9 The critical examples now have an actual exact record

The v100 branch contains an exact rational diagnostic script and a lossless compressed record, with explicit separation between finite example checks and universal theorem verification.

### 4.10 The revision is source-pinned and auditable

The source manifest pins the reviewed v99 paper, controlling report and new source hashes. The new audit code distinguishes source-only validation from a successful native build.

These are real improvements. My negative recommendation should not be read as saying that revision 100 failed to respond to the previous report.

## 5. Main objection I: the “canonical” weighted tangent theorem remains too close to a definition

The paper defines, for the image germ S of the actual observation–coefficient relation,

\[
\mathfrak D_w^+(S)
=
\overline{\{(\varepsilon,D_\varepsilon^{-1}y):
\varepsilon>0,\ y\in S\}},
\qquad
T_w^+S=\{v:(0,v)\in\mathfrak D_w^+(S)\}.
\]

It then proves

\[
\mathcal I_0=T_w^+S\cap\{\|U\|\le1\}.
\]

This is useful notation and the boundary rescaling at \(\|U\|=1\) is worth recording. But one should be precise about the level of content.

The old \(\mathcal I_0\) was already constructed by the same positive fixed-centre weighted rescaling and closure, together with the observation-unit constraint. The new theorem therefore does not discover an unexpected identification between two independently defined objects. It packages the existing construction as a weighted tangent relation and checks that the unit constraint behaves correctly at the boundary.

That is mathematically legitimate. It is not, by itself, a top-four structural theorem.

### 5.1 Presentation invariance is obtained by moving to the image germ

Once S is defined to be the image germ of the actual relation, invariance under a proper surjective presentation of that same image is nearly built into the definition.

This is the correct way to make the object presentation independent, but it should not be advertised as a deep invariance principle.

### 5.2 Filtered naturality assumes almost exactly the behavior it concludes

Theorem thm:filtered-naturality assumes that

\[
D_\varepsilon^{-1}\phi D_\varepsilon\to\phi_0
\quad\text{and}\quad
D_\varepsilon^{-1}\phi^{-1}D_\varepsilon\to\phi_0^{-1}
\]

locally uniformly on bounded sets.

Under those hypotheses, carrying weighted tangent limits by \(\phi_0\) is expected. If the observation norm and decoder are also transported, invariance of the decoded diameter is then formal.

Again, the theorem is correct in spirit. It does not yet give a classification-independent or category-level universal property that would make the object unavoidable.

### 5.3 The algebraic comparison is standard associated-graded geometry

The saturation and weight-initial-ideal statement is exactly the standard weighted associated-graded construction. The manuscript now says so, which is good.

But the novelty must then lie in the real liftable locus, the unit section, or their interaction with the target. The paper has not yet proved a sufficiently strong theorem about that interaction.

### 5.4 The adjacent real/positive tropical literature must be confronted directly

The bibliography now contains Fulton, the Stacks normal-cone section, Maclagan–Sturmfels and Bernig–Lytchak. That is not enough for the positive-real claim.

At minimum the authors need to compare their liftable weighted relation with the literature on real and positive tropicalization of semialgebraic or positive real sets. Two directly adjacent references are:

- Philipp Jell, Claus Scheiderer and Josephine Yu, “Real Tropicalization and Analytification of Semialgebraic Sets,” *International Mathematics Research Notices* 2022, 928–958, DOI 10.1093/imrn/rnaa112.
- Kemal Rose and Máté L. Telek, “Computing positive tropical varieties and lower bounds on the number of positive roots,” *Journal of Symbolic Computation* 132 (2026), 102477, DOI 10.1016/j.jsc.2025.102477.

I am **not** asserting that either paper already contains the manuscript’s exact fixed-centre observation-unit section. The point is the opposite: the current manuscript has not established the precise relation or distinction. Real tropicalization explicitly retains sign/semialgebraic information, and positive tropicalization explicitly studies when initial data do or do not capture positive real liftability. A top-four novelty claim in this neighborhood requires a theorem-level comparison, not only citations to complex weighted initial ideals.

### 5.5 What is still needed

A result that could change my assessment would be something like:

- an intrinsic universal property of the weighted real relation;
- a theorem identifying it with, or sharply distinguishing it from, a real/positive tropical or normal-cone object;
- a classification of which positive-real initial points are liftable in the paper’s observation geometry;
- a functorial construction that does not assume convergence of the filtered conjugates as a hypothesis;
- a theorem extracting new geometric constraints on the possible joint leading sets.

At present the paper has a well-defined object, not yet a sufficiently deep theory of that object.

## 6. Main objection II: quadratic reconstruction is a universal metric fact, not the missing structural theorem

Theorem thm:reconstruction states, in essence,

\[
m_0(a)=\operatorname{dist}(a,\mathcal C_0)^2
\]

and

\[
\mathcal C_0
=
\bigcap_{a\in\mathbb Q^N}
\{v:\|v-a\|^2\ge m_0(a)\}.
\]

It also gives a finite-net estimate for Hausdorff distance.

These statements are correct.

They are also general facts about closed subsets of metric spaces.

A closed set is determined by its distance function. If two compact sets lie in a bounded region, the supremum norm of the difference of their distance functions recovers their Hausdorff distance; restricting to a sufficiently fine net gives the stated approximation. Rational centres suffice by density.

Nothing in this reconstruction principle is specific to weighted tangent geometry, polynomial roots, singular inverse problems, semialgebraic sets, or even algebra.

The only model-specific input is that the limiting distance probes are first-order definable and hence effectively describable for algebraic input. That effectivity is useful, but after semialgebraicity is known it is an expected application of quantifier elimination.

Therefore this theorem does **not** answer the v99 request for a nontrivial structural theorem governing the joint object.

It answers a different and narrower question:

> Can sufficiently rich scalar *values* determine the compact joint set?

Yes, because distance-to-set values determine every compact set.

That clarification is worth keeping. It should not carry the headline conceptual novelty.

## 7. Main objection III: the binary “valuative equivalence without metric equivalence” theorem is stronger than v99, but its mechanism is generic unit loss

Theorem thm:binary-separation is one of the most carefully constructed new pieces of v100.

The two centres are legitimate interior full-rank points of the actual binary model. No parameter is held known. Their exact profiled Fisher matrices differ, and so do their leading spectral diameters.

The theorem also proves that along every nonconstant real analytic arc

\[
\operatorname{ord} G_{1/4}
=
\operatorname{ord} G_{1/8}
=
2\min_i\operatorname{ord} z_i.
\]

This is correct because both observation germs have positive-definite quadratic leading forms.

But this reveals the limitation at the same time.

### 7.1 Every positive-definite analytic metric germ has this order behavior

If

\[
G(z)=Q(z)+O(\|z\|^3),
\qquad Q>0,
\]

then every analytic arc has order twice the smallest coordinate order, independent of the positive-definite matrix Q.

Thus the theorem’s observation-order equivalence is not a special rigidity phenomenon of the binary model. It is what one expects whenever two smooth identified models induce different positive-definite local metrics in the same coordinates.

The metric unit ball, and hence the sharp constant, depends on Q. The valuation does not.

That distinction is real, but it is generic.

### 7.2 The target-scalar order statement is automatic once the target map is literally the same

The two experiments use common parameter coordinates and the target coefficient increment map \(\Delta c(z)\) is literally identical at the two centres.

Therefore every polynomial H of \(\Delta c\) is the same analytic function of z in both experiments, so its arc orders agree automatically.

The hard arithmetic in the theorem is the exact Fisher comparison. The equality of target-scalar orders is not an independent obstruction theorem.

### 7.3 The theorem demonstrates loss of positive units, not yet a deep impossibility principle

The paper says this explicitly near the end: the scalar orders erase positive units.

I agree.

But once stated that way, the result is conceptually closer to

> valuations do not determine metric normalization

than to a theorem saying that the proposed joint weighted geometry captures information inaccessible to every natural scalar invariant of the problem.

For a top-four paper, I would want a stronger separation result in which one fixes a scalar data set that retains substantially more unit information, or a theorem characterizing exactly which scalar invariants recover the joint metric object.

### 7.4 The “one common real monomial presentation” wording needs tightening

The theorem says that the accessible real divisorial order data “can be computed on one common real monomial presentation and agree as well.” The proof later says that *any finite specified collection* of polynomial combinations can be principalized on a common space.

Those are not literally the same assertion if “every polynomial H” is interpreted simultaneously.

Because there are infinitely many polynomial combinations H, the manuscript should state exactly what is common:

- a fixed common modification on which the observation order is controlled and the coefficient germs define the same divisorial valuations; or
- for every finite chosen family of H, a common refinement exists.

The current wording invites an unnecessarily strong simultaneous-mononomialization reading.

## 8. Main objection IV: the singular entrance theorem is a semialgebraic Puiseux theorem for a value function, not a classification of singular entrances

Theorem thm:singular-entrances removes the regular-corner hypothesis. That is a genuine broadening.

The key move is to stop parametrizing the remote component and instead study the exact value function

\[
d_j(\theta,\delta)
=
\min_{x\in N_{j,\theta}}
\|f_\theta(x)-p_\theta(\delta)\|.
\]

Because the feasible set is compact semialgebraic and the objective is semialgebraic, the graph of d_j is semialgebraic.

At that point, much of the theorem follows from standard one-variable semialgebraic geometry:

- an eventually nonzero nonnegative semialgebraic germ has a rational Puiseux leading exponent;
- after finite stratification, only finitely many support balances can occur at fixed presentation format;
- an eventual sign comparison of two semialgebraic germs is decidable;
- the leading coefficient can be made Nash on strata;
- compactness and the finite exact fibre identify the limiting target representative.

This is mathematically correct and useful.

It is not yet a structural theory of singular entrances.

### 8.1 The theorem classifies the value-function germ, not the source singularity

The result does not tell the reader what geometric feature of a singular remote component produces a given rational exponent.

It does not relate \(\rho_j\) to an intrinsic multiplicity, polar invariant, Newton datum, tangent cone, contact exponent, or another singularity invariant of the observation map.

It says that some rational exponent exists because the minimum is semialgebraic.

That is a definability theorem, not a singularity classification theorem.

### 8.2 “Fixed format” must be made mathematically explicit

The phrase “all data have fixed format” carries significant weight in the finite-exponent-list and effectivity claims.

The paper should specify the format as an actual finite complexity datum: number of variables, Boolean structure, number and degrees of polynomials, algebraic coefficient representation, degree of target, and complexity of the centre path, or another precise convention.

Without that, “finite list determined by fixed format” reads as a meta-complexity slogan rather than a theorem with a reusable hypothesis.

### 8.3 The realization theorem is elementary and intentionally outside the main cubic model

Theorem thm:entrance-realization constructs two disjoint polynomial probability branches

\[
P_{\rm base}(s)=P_0+As,\qquad
P_{\rm rem}(u)=P_0+A u^m+B u^n
\]

and obtains \(\rho=n/m\).

This is a perfectly good example.

But it mainly confirms the general Puiseux picture. It does not show that such a hierarchy of singular entrances occurs naturally in the principal polynomial observation model, much less classify it there.

### 8.4 The regular-corner criterion is standard differential/conic geometry

Proposition prop:corner-criterion is essentially:

- Nash implicit-function coordinates;
- independent active constraints;
- a tangent cone;
- injectivity/coercivity on the feasible cone;
- exclusion of the centre velocity from the image cone.

That is the right criterion. It is also standard in spirit.

The manuscript is now appropriately cautious about this.

### 8.5 What would constitute a genuine next theorem

A substantially stronger result would connect entrance exponents to the intrinsic local algebra or geometry of the observation map.

For example:

- a Newton/polyhedral formula for \(\rho_j\) in a broad class;
- a finite list derived from resolution divisors with an intrinsic interpretation;
- a generic stratification theorem describing which exponents occur;
- a classification of nonregular entrances in the binary polynomial model;
- a theorem describing interaction of multiple remote branches or wall intersections.

That would be a theory of singular entrances. The present theorem is a semialgebraic asymptotic theorem for their distance functions.

## 9. Main objection V: the breadth mismatch remains

The manuscript combines two very different levels of mathematics.

### 9.1 The broad layer

The first layer invokes:

- resolution/principalization;
- real branch descent;
- semialgebraic stratification;
- quantifier elimination;
- rational asymptotic exponents;
- weighted degenerations;
- metric tangent language;
- effective real algebraic output.

### 9.2 The distinctive concrete layer

The strongest nonformal discoveries are still concentrated in:

- the fixed-degree full-rank binary multiplicity law;
- the exact rank-deficient cubic fibre;
- the inverse through channel-rank loss;
- the weight wall;
- the endpoint wall;
- their different nonidentified-side opening mechanisms.

These are specific, model-dependent theorems.

### 9.3 Revision 100 does not yet prove that the broad machinery is essential to the distinctive discoveries

The multiplicity theorem is derived directly from local coefficient/root expansions and Fisher projection.

The cubic fibre is classified by the affine pencil.

The cross-rank inverse is proved by second-marginal recovery and robust pencil isolation.

The two walls are proved by exact feasible charts and score separation.

The new singular entrance theorem then tells us that any semialgebraic remote distance has a rational leading exponent. That does not retroactively make the resolution/atlas layer essential to the cubic analysis.

The paper therefore still risks being two papers superposed:

1. a general semialgebraic asymptotic framework;
2. an explicit singular inverse problem with unusually detailed algebra.

A top-four general-journal paper can certainly combine a general theory and a model. But there must be a theorem showing that the general theory extracts something from the model that direct analysis could not reasonably supply, or that the model forces a new general theory.

That theorem is still missing.

## 10. Detailed correctness assessment of the new v100 statements

I record the points I checked because the recommendation is not a correctness rejection.

### 10.1 Boundary rescaling in thm:canonical

The argument at \(\|U\|=1\) rescales epsilon by

\[
a_n=\max(1,\|U_n\|^{1/q})
\]

and correspondingly rescales each coefficient block by its weight. Since \(a_n\to1\), the same unscaled relation point approaches the same weighted limit while satisfying the unit constraint.

This is a legitimate way to avoid an unjustified interchange of closure and intersection.

### 10.2 Algebraic special fibre

The saturation-by-epsilon description and minimum-weight initial ideal are standard and consistent with the chosen convention.

I see no immediate algebraic contradiction.

### 10.3 Cusp example

For y^2=x^3 with equal weights, the weighted equation becomes

\[
v_y^2=\varepsilon v_x^3,
\]

so the algebraic special fibre is \(v_y=0\), while positive-real liftability forces \(v_x\ge0\).

This example is correct.

### 10.4 Quadratic reconstruction

The set-theoretic formula is correct. If v lies outside C, choose a rational a close enough to v that

\[
\|v-a\|<\operatorname{dist}(a,C).
\]

The finite-net bound follows from the Lipschitz property of distance functions.

Again, my objection is novelty, not correctness.

### 10.5 Binary local-order calculation

Positive definiteness of the Fisher quadratic form implies two-sided local comparison with \(\|z\|^2\). Hence the order formula along analytic arcs is consistent.

The profiled ellipsoid formula is also standard Schur-complement geometry once the full score has rank seven.

The exact rational matrices deserve independent arithmetic checking, which the repository now supports.

### 10.6 Singular entrance localization

The finite exact fibre and compact separation imply that minimizers in a chosen remote neighbourhood converge to that remote representative. This justifies independence of sufficiently small isolating neighbourhoods at the germ level.

The semialgebraicity of the attained minimum is also standard from quantifier elimination.

### 10.7 Rational exponent and exact threshold comparison

For a one-variable semialgebraic germ, a rational power law after Puiseux reparametrization is expected. Eventual sign is likewise a standard o-minimal/semialgebraic property.

The theorem’s insistence that equality is included because the observation ball is closed is correct.

### 10.8 Realization of rational exponents

The construction with \(x=u^m\) and the orthogonal \(B u^n\) perturbation gives the intended \(n/m\) order after minimizing the leading Fisher norm.

I do not see an immediate flaw in the example.

## 11. Literature positioning remains incomplete

Revision 100 has improved the bibliography substantially.

The added comparison with variational analysis is appropriate. The normal-cone and weighted-initial references are also appropriate. Bernig–Lytchak helps prevent conflation with inner-metric tangent limits.

But the literature discussion still does not surround the central positive-real claim tightly enough.

The manuscript should explicitly discuss real tropicalization of semialgebraic sets and positive tropicalization/positive liftability. In particular, it should tell the reader:

1. whether \(T_w^+S\) is a one-weight fibre or slice of an established real tropicalization/real analytification construction;
2. whether the retained branch conditions correspond to sign data in a real tropical object;
3. how positive-real liftability relates to positive tropical varieties and initial-ideal criteria;
4. exactly what the observation-unit section and target decoder add beyond those objects;
5. which theorem in the present manuscript is new after those comparisons are imposed.

Without that, “positive-real weighted tangent relation” remains insufficiently positioned for a claim of conceptual priority.

## 12. Effectivity: now more honest, still not a source of top-four novelty

The revision has correctly separated three things:

- geometric existence;
- direct first-order output procedures;
- finite exact arithmetic in examples.

This is a significant expository improvement.

The direct algorithms for compact minima, limit graphs, sign decisions, algebraic outputs and root isolation are credible at the level stated.

But they are applications of real quantifier elimination once the relevant sets and functions are first-order definable.

The geometric certificate enumeration remains much less informative computationally. The revision now calls it supplementary rather than asking it to carry the main contribution. I agree with that demotion.

No further expansion of this certificate machinery would improve my assessment unless the paper is being reconceived as an algorithms paper.

## 13. Reproducibility and repository audit

The v100 repository discipline is much better than v99.

### 13.1 Positive points

The branch contains:

- a source manifest with hashes;
- a lossless exact diagnostic record;
- a script that recomputes the named finite rational programs;
- a recursive native TeX builder;
- an audit that binds source inputs and generated PDFs to HEAD;
- a workflow that checks out the triggering SHA exactly;
- an explicit local-validation record that refuses to claim unexecuted native success.

This is exemplary in intent.

### 13.2 The exact reviewed head still lacks durable native success evidence in the committed branch

The committed LOCAL_VALIDATION.json states:

- principal native build executed locally: false;
- archive native build executed locally: false;
- complete native build executed locally: false;
- full principal source-graph check executed locally: false;
- remote native success observed: false.

Thus the exact branch itself does not contain a completed head-bound runtime receipt.

The workflow definition is not a build result, as the revision README correctly says.

My available GitHub status interface also showed no combined commit statuses for the reviewed SHA and no pull-request-triggered run, but that interface does not enumerate every push-triggered Actions run. I therefore do **not** infer from that limited query that no push run exists. The narrower and fully supported statement is that no successful runtime receipt is committed at the reviewed source head and the local validation record itself does not claim one.

This is not a mathematical reason for rejection. It is a remaining reproducibility gap.

### 13.3 Artifact retention is not archival preservation

The workflow retains uploaded artifacts for 90 days.

For a source-pinned referee package that is intended to remain independently auditable, the final successful runtime receipt and critical hashes should be committed, attached to a release, or otherwise durably preserved rather than relying only on expiring Actions artifacts.

### 13.4 The root README is stale

On the v100 revision branch, the root README still says “Theta-Theory — A2 revision 82” and points to an A2 v82 referee entry.

I understand why an addition-only preservation policy produced this state. But an external referee landing on the reviewed branch sees the wrong current entrypoint.

A preservation policy should not prevent adding a clearly authoritative top-level CURRENT_REVIEW_ENTRY.md, updating a nonhistorical index, or otherwise making the current review target unambiguous.

## 14. Disposition of the v99 referee requests

My current assessment is:

### R1. Identify the joint initial fibre relative to standard weighted tangent/initial constructions

**Substantially answered at the algebraic-comparison level, but not closed as an originality issue.**

The paper now identifies the algebraic construction correctly. It still needs direct comparison with real/positive tropicalization and a non-tautological structural theorem.

### R2. Add a nontrivial structural theorem for the joint object

**Formally answered, conceptually not yet answered.**

Filtered naturality and quadratic reconstruction are valid, but the former assumes the appropriate filtered limit behavior and the latter is a universal distance-function fact.

### R3. Strengthen scalar separation inside the principal observation model

**Answered literally and substantially.**

The example is now in the full binary model and keeps all arc orders of the specified scalar functions.

However, the conceptual mechanism is generic loss of positive units, so the top-four significance question remains.

### R4. Position the regular remote formula in variational analysis

**Answered.**

The manuscript now cites the relevant sensitivity literature and no longer claims metric projection itself as new.

### R5. Broaden the wall theory or narrow the claims

**Answered at the definability level, not at the singularity-classification level.**

The semialgebraic entrance theorem is genuinely broader. It classifies possible value-function germs after stratification, not the underlying singular geometries.

### R6. Narrow the geometric effectivity claim

**Answered.**

The direct QE outputs are separated from supplementary certificate enumeration.

### R7. Add exact diagnostics

**Answered.**

The branch contains a source-pinned exact rational record and verification script.

### R8. Restore exact-head CI

**Partially answered.**

An exact-head workflow exists. A durable successful runtime receipt is not part of the reviewed branch, and the local validation file explicitly declines to claim one.

### R9. Add a response/manifest package

**Answered.**

The response, manifest, validation record and reproduction README are present.

### R10. Expand literature positioning

**Partially answered.**

The bibliography is much better, but the literature nearest to positive-real/real-tropical liftability remains absent.

## 15. What would change my assessment

I see two coherent routes.

### Route A: prove a genuinely intrinsic theorem about the real weighted object

This route should not add more infrastructure.

It should prove something that is not true of an arbitrary closed set or arbitrary semialgebraic value function.

Examples include:

- a universal property relative to real/positive tropicalization;
- a classification of liftable faces of the weighted initial fibre;
- a finite intrinsic invariant determining the feasible joint leading set;
- a functoriality theorem under a natural category of observation maps, rather than under an assumed convergent filtered conjugacy;
- a structural restriction theorem for leading sets arising from polynomial observation models;
- a theorem connecting the joint metric set to singularity invariants in a way not reducible to “retain the positive unit.”

If such a theorem were strong enough, the broad atlas could become justified.

### Route B: make the explicit binary/cubic theory the paper

This would produce a more focused and, in my view, stronger article.

The central spine could be:

1. the full-rank multiplicity law;
2. the rank-deficient cubic fibre;
3. the cross-rank inverse;
4. the local Fisher normal form;
5. the weight wall;
6. the endpoint wall;
7. the contrast between local multiplicity instability and remote nonidentification;
8. only the minimum general semialgebraic machinery needed to organize those facts.

That paper would make a narrower claim but would put the technically deepest mathematics in the foreground.

## 16. Specific revisions required before reconsideration at the same journal class

### R100.1 — Establish the exact relationship to real/positive tropical geometry

Add theorem-level comparison with the real tropicalization of semialgebraic sets and positive tropicalization/positive liftability.

Do not merely add citations.

State precisely which part of \(T_w^+S\) is established theory, which part is the manuscript’s observation-specific section, and what new theorem follows from the difference.

### R100.2 — Replace quadratic reconstruction as a headline structural result

Keep the theorem if useful, but do not use the universal distance-function identity as the main answer to the canonicality problem.

Add a property specific to feasible weighted observation relations.

### R100.3 — Strengthen the separation theorem beyond generic positive-unit sensitivity

The present theorem shows that orders forget metric units.

A stronger result should keep a substantially richer natural scalar datum fixed, or characterize a maximal scalar datum that still fails, while changing the joint spectral object.

Alternatively, prove a sufficiency theorem for a natural finite scalar invariant rather than the complete distance function.

### R100.4 — Turn entrance orders into singularity geometry

Relate \(\rho_j\) and, ideally, its leading coefficient to intrinsic geometric or algebraic data of the remote observation germ.

A mere existence of rational Puiseux order after semialgebraic minimization is not enough for the paper’s broad wall-theory rhetoric.

### R100.5 — Define “fixed format” explicitly

The finite-list and effective claims must name the exact complexity datum being held fixed.

### R100.6 — Tighten the monomial-presentation wording

Clarify whether one fixed modification handles the entire infinite family of polynomial scalar functions or whether a common refinement is asserted only for every finite selected family.

### R100.7 — Make the general/concrete dependency explicit

For each major concrete theorem, state exactly where the general atlas is essential.

If it is not essential, reorganize the article so the direct model theorem is primary and the general framework is supporting material.

### R100.8 — Complete durable exact-head validation

Run the principal/archive/complete native build at the exact reviewed head and preserve a source-head-bound runtime receipt durably.

Fix the current review entrypoint so a referee does not land on the stale v82 root README.

### R100.9 — Stop adding infrastructure unless it proves a new theorem

The repository already has enough manifests, scripts, response matrices and certificate plumbing.

The next revision should be mathematically smaller and conceptually stronger.

## 17. Editorial comments

1. The abstract currently says “We prove its presentation invariance.” The body proves invariance of the image-germ construction and filtered naturality under explicit convergence hypotheses. I would state this more narrowly in the abstract.

2. “Canonical” is an expensive word at this journal level. If it is retained, the paper should state the category and universal property with respect to which the construction is canonical.

3. The distinction between algebraic initial fibre, positive-real liftable subset and observation-unit section should appear in one boxed schematic early in the introduction.

4. The quadratic-probe theorem should be described as a metric reconstruction lemma, not as evidence that the weighted object has a special scalar reconstruction phenomenon.

5. The binary valuative example should foreground the positive-unit mechanism. Hiding that mechanism behind very large rational matrices makes the conceptual content look more mysterious than it is.

6. The singular entrance theorem should say “semialgebraic entrance asymptotics” rather than suggest a classification of singularities.

7. The exact finite examples are useful, but their numerical sizes should not be used rhetorically as evidence of generality.

8. The paper should not enlarge the appendix again unless a referee can point to a genuine logical gap. The current problem is not missing technical bulk.

## 18. Correctness assessment

My current view is more favorable than the recommendation may suggest.

### General relative atlas

I retain the v99 assessment: after the repairs made there, I do not have a direct counterexample to the principal relative real-atlas statements.

### Weighted tangent comparison

The v100 comparison theorem is consistent with its definitions and the standard associated-graded construction.

### Natural transformation statement

Under the stated filtered convergence of the map and inverse, the tangent-relation transport is plausible.

### Reconstruction

Correct, but generic.

### Binary valuative separation

The local order claim and the mechanism of different Fisher ellipsoids are consistent. The exact matrices should remain subject to independent arithmetic reproduction, but the branch now provides that route.

### Singular entrance theorem

The semialgebraic minimum argument and rational leading exponent are plausible and align with standard one-variable semialgebraic/Puiseux behavior.

### Concrete cubic theory

I found no new contradiction in the imported exact-fibre, cross-rank inverse, regular-corner second-order formula, or the two explicit wall analyses.

Accordingly, this report is **not** a correctness rejection.

## 19. Originality and depth assessment

The manuscript’s deepest-looking original content remains:

1. the exact singular inverse geometry of the binary/cubic polynomial experiment;
2. the separation of local multiplicity instability from remote exact nonidentification;
3. the two distinct identification-wall mechanisms and their exact local/remote scales.

The v100 additions are useful conceptual hygiene around those results. They do not yet constitute a comparably deep general theory.

In particular:

- naming the positive rescaling closure a weighted tangent relation does not by itself create a new invariant theory;
- reconstructing a compact set from its distance function is not a special theorem about this inverse problem;
- equal valuation orders with different positive-definite metric units is a generic phenomenon;
- rational entrance exponents of semialgebraic minima are expected from Puiseux/o-minimal geometry.

A top-four paper needs a theorem that makes the distinctive mathematics unavoidable after these standard observations have been factored out.

## 20. Final assessment

Revision 100 is a better paper than revision 99.

It substantially repairs the v99 reproducibility regression, narrows effectivity responsibly, improves the literature discussion, moves scalar separation into the real model, and generalizes remote entrance from regular corners to arbitrary finite semialgebraic fibres at the level of value-function asymptotics.

I do not think those improvements are enough for the stated journal class.

The reason is no longer missing proof architecture.

The reason is that the revision’s proposed answers to the canonicality and generality problem are themselves too formal:

- the “canonical” object is very close to the defining rescaling closure;
- the reconstruction theorem is a universal distance-function identity;
- the valuative separation theorem exposes the standard loss of positive units;
- the singular entrance theorem exposes the standard Puiseux behavior of a semialgebraic minimum.

Meanwhile the technically richest results remain the concrete binary/cubic theorems.

I therefore recommend **rejection in the present form** for an Annals / Acta / Inventiones / JAMS-level general mathematics journal.

I would encourage another revision only if it is conceptually selective. The next version should not add another layer of audit machinery or another general definability theorem. It should either prove one genuinely intrinsic structural theorem about the positive-real weighted object or singular entrance geometry, after direct comparison with the nearest real/positive tropical literature, or it should reorganize the article around the explicit binary/cubic mathematics and let that strong concrete theory stand on its own.
