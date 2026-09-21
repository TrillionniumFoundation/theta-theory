# Independent harsh referee report on A2 revision 108

**Manuscript:** *Contact tomography in Hankel information geometry*  
**Reviewed revision branch:** revision/a2-v108-hankel-contact-tomography-intrinsic-fibres-2026-09-21  
**Reviewed source commit:** 4ed51300c2aa6e7b11e701a38ed1d14f8b9e8191  
**Date of report:** 21 September 2026  
**Standard applied:** general-journal standard comparable to Annals / Inventiones / JAMS / Acta  
**Recommendation:** **reject in the present form**

This is an owner-requested, AI-assisted external-referee-style assessment. It is not a journal-commissioned report and should not be represented as an editorial decision. I have treated the submitted commit as immutable review material and have placed this report only on the isolated review branch.

## 1. Executive assessment

Revision 108 is a genuine and substantial improvement over v107. The authors have finally produced the kind of non-factorized statement that the previous report requested: observed second contact jets of the synchronized rank-one cone are used to recover the native inverse information, and in shared dimension two the native Hankel restriction removes a one-dimensional ambiguity that persists for arbitrary positive metrics. The new principal theorem is mathematically coherent, the three-root formula is explicit, the endpoint inverse theorem now really does take the scalar value function as input, and the inverse-parametric-programming comparison is materially more accurate.

I do **not** find a fatal counterexample to the principal conormal calculation in the scope I checked. Independent exact spot checks reproduce the one-dimensional quadratic kernel in a generic d=2, k=4 example, full quadratic rank in a d=3, k=6 example, and the expected 2k-1 dimension of the three-site native span. Those checks are recorded separately and are not proof certification.

The reason for rejection is now different from the reason for rejection of v107.

The central new obstruction is **priority and significance**. The geometric core of the new theorem is, after stripping away the application notation, the classical projective-dual fact that the dual of the quadratic Veronese variety is the discriminant hypersurface of singular quadratic forms. In matrix coordinates this is the determinant hypersurface of singular symmetric matrices. Consequently, the statement that no nonzero quadratic form can vanish on that discriminant when d>=3, while in d=2 the unique quadratic equation is the determinant, is not a new conormal geometry phenomenon of the present model. It is an elementary low-degree consequence of a classical discriminant picture.

The genuinely model-specific step then consists of intersecting that classical ambiguity space with the linear subspace forced by Cauchy/Hankel interpolation. In d=2 this gives a useful and clean transversality criterion. In d>=3, however, the native Hankel geometry is not needed for identifiability at all: arbitrary positive metrics are already determined by the conormal second jets. Thus the essential “Hankel/contact interaction” survives only in the lowest shared dimension.

For a specialized inverse-problem or algebraic-statistics paper, that may still be a worthwhile theorem. For a general top-four mathematics journal, the present central mechanism is too close to classical projective duality plus finite-dimensional linear algebra, and the manuscript does not yet supply a second conceptual leap that would justify its breadth and length.

There is also a concrete reproducibility defect at the exact reviewed HEAD. The committed paper.tex inputs four files under article/v108/prepared/, but those files do not exist at commit 4ed51300c2aa6e7b11e701a38ed1d14f8b9e8191. The claimed evidence/verification.json also does not exist at that commit. Therefore the exact reviewed HEAD is not a self-contained compilable source state, and R107.8 is not closed on the object actually reviewed.

My overall view is therefore:

- mathematical correctness of the new central calculation: **plausible and substantially improved**;
- closure of the main conceptual criticism in R107: **partly achieved**;
- top-four novelty/significance: **not established**;
- exact-source reproducibility at the reviewed HEAD: **not closed**;
- recommendation: **reject, not routine major revision**.

## 2. What v108 actually proves

The principal theorem considers the quadratic measurement map

\[
  \mathcal A_A(S)=(a_i^{\mathsf T}Sa_i)_i,
\]

assumed injective on symmetric d by d matrices, and the rank-one image

\[
  q_A(\eta)=\mathcal A_A(\eta\eta^{\mathsf T}).
\]

For the metric squared-distance contact function

\[
  C_R(b)=\min_\eta (q_A(\eta)-b)^{\mathsf T}R^{-1}(q_A(\eta)-b),
\]

the normal second jet at a smooth positive point determines the restriction of R to the Euclidean normal space. Equivalently, the dual normal quadratic values are n^T R n.

The manuscript then observes that

\[
  n\in N_\eta
  \quad\Longleftrightarrow\quad
  \mathcal A_A^*(n)\eta=0,
\]

so the union of normal spaces maps to singular symmetric matrices. The new ambiguity calculation is:

1. for d=2, a quadratic form on the normal coordinate n that vanishes on the entire conormal union is a multiple of det(\mathcal A_A^*(n));
2. for d>=3, there is no nonzero quadratic form with that property.

In d=2 the determinant becomes the explicit matrix direction B_A with off-diagonal entries det(a_i,a_j)^2.

Independently, the native calibrated binary model forces R into a 2k-1 dimensional linear span W_k described by three-site divided-difference relations among its off-diagonal entries. The determinant ambiguity is removed exactly when at least one such relation is nonzero on B_A.

This yields:

- exact second-jet identifiability on the native cone under a transversality condition in d=2;
- automatic identifiability in d>=3;
- 2k-1 exact scalar dual-jet queries as a sharp dimension count;
- in the three-root d=2 case, five ordinary directional contact curvatures and an explicit reconstruction formula;
- transport of the reciprocal fixed-budget image and its design fibres into the recovered contact-data coordinates.

Separately, the manuscript gives a function-input endpoint representation theorem by writing positive-definite orthant-QP representability as a first-order formula over the reals and applying quantifier elimination.

This is a clear theorem package. The issue is not that the authors have failed to state anything precise. The issue is how much of this package is genuinely new, how broad it is, and whether it clears the significance threshold of the venue being targeted.

## 3. The main geometric lemma is classical Veronese-dual geometry in coordinates

This is the most important issue in the present report.

The map

\[
  \eta \longmapsto \eta\eta^{\mathsf T}
\]

is the affine cone over the quadratic Veronese embedding. The hyperplanes tangent to that Veronese variety are represented by singular quadratic forms. Projectively, the dual variety of the quadratic Veronese is the discriminant hypersurface; in symmetric-matrix coordinates its equation is the determinant.

This is classical material. A standard reference is Gelfand, Kapranov, and Zelevinsky, *Discriminants, Resultants and Multidimensional Determinants* (1994): the dual of a Veronese variety is the discriminant, and for quadratic forms that discriminant is the symmetric determinant. This is also a routine example in treatments of projective duality.

Lemma thm:determinantal-kernel is therefore not introducing a new dual variety. The proof in v108 is a perfectly serviceable elementary real-coordinate proof, but its central algebraic content is the following classical fact:

- the quadratic Veronese dual is det=0;
- det has degree d;
- hence the degree-two part of its principal ideal is zero for d>=3;
- for d=2 the degree-two part is exactly the determinant line.

The manuscript currently presents this as “quadratic forms on the conormal union” without placing it in the classical Veronese/discriminant framework. I found no Veronese discussion or GKZ-style reference in the v108 references, and a repository search for “Veronese” returned no result.

At a top-four journal, this is not a cosmetic bibliography issue. It changes the novelty accounting of the principal theorem.

The authors must explicitly separate:

- **classical geometry:** the conormal/dual discriminant calculation for the rank-one symmetric cone;
- **new model-specific geometry:** the pullback through the measurement map and the intersection with the native Cauchy/Hankel information subspace;
- **new statistical consequence:** whatever cannot be read off from those two ingredients by elementary finite-dimensional inversion.

At present these layers are fused, making the central theorem appear deeper and more novel than its proof architecture supports.

## 4. In d>=3 the “Hankel interaction” disappears

The new paper is titled around Hankel information geometry, and the response letter correctly says that a top-level theorem should use the Hankel restriction essentially.

That is now true only in d=2.

Part (a) of the principal theorem says that for d>=3 the full second-jet data identify an arbitrary positive definite R before any native information constraint is imposed. Once that is established, the fact that the true R lies in the native Hankel span is irrelevant for identifiability.

Thus the theorem has two qualitatively different regimes:

- **d=2:** conormal geometry leaves one determinant ambiguity and native Hankel geometry can remove it;
- **d>=3:** conormal geometry alone determines the metric, so there is no native ambiguity left for Hankel geometry to resolve.

The d=2 result is the genuinely coupled theorem. The d>=3 result is a generic-metric tomography theorem with a native corollary.

This matters because the manuscript repeatedly markets the principal result as a general conormal rigidity theorem “in native Hankel geometry” for all shared dimensions. The essential interaction is not dimension-uniform. The strongest conceptual sentence of the response—“the native restriction has a necessary and sufficient downstream role”—is literally correct only in the d=2 branch.

I would require the authors either to:

1. make d=2 the honest conceptual centre and explain why that low-dimensional interaction is itself sufficiently important; or
2. find a genuinely native obstruction/consequence in higher shared dimension, where the Hankel restriction does nontrivial work rather than merely restricting an already identifiable metric.

Without that, the all-d formulation broadens the statement but weakens the central narrative.

## 5. The d=2 coupling is clean but currently too elementary for a top-four centrepiece

Suppose one grants the classical determinant ambiguity. The remaining d=2 argument is:

1. the arbitrary-metric second-jet fibre is the affine line R + R B_A;
2. the native inverse-information span W_k is cut out by explicit linear three-site relations;
3. the native fibre is the intersection of that affine line with the native cone;
4. injectivity is equivalent to B_A not lying in W_k;
5. this is detected by at least one explicit scalar tau_ijl(A).

This is correct, useful, and explicit. But structurally it is one-dimensional linear transversality.

The three-root formula is the same mechanism in its smallest instance: five quartic evaluations leave the determinant line, and one native linear relation fixes the coordinate on that line.

The paper should not confuse “sharp” with “deep.” The criterion is sharp because the ambiguity space is one-dimensional and the native relation can either kill it or not. The five-query lower bound is sharp because the native parameter space has dimension five. Those facts are exact, but exactness alone does not create the level of conceptual difficulty expected in a general top-four paper.

For reconsideration at that level, I would need a theorem where the native information geometry changes the conormal inverse problem in a substantially richer way than intersecting a classical one-dimensional ambiguity with a linear subspace.

Examples of directions that would materially change the assessment include:

- non-injective quadratic measurements, where the pullback of the determinant/discriminant has nontrivial additional geometry;
- partial conormal observation, rather than access to all normal restrictions;
- overidentified clock systems where the native image is no longer the present exact square-clock Hankel congruence class;
- endpoint strata genuinely coupled to the contact tomography rather than retained as companion theory;
- higher-order contact where the classical degree-d discriminant no longer makes the quadratic ambiguity vanish automatically;
- finite noisy statistical observations with an optimal stability or minimax theorem, rather than an exact-real oracle.

I am not prescribing a particular direction. I am saying that another local algebraic patch to the present theorem is unlikely to change the venue-level conclusion.

## 6. The 2k-1 query theorem is a dimension theorem for a bespoke exact oracle

Part (c) is carefully worded, and the response improves v107 by saying explicitly that these are scalar dual second-jet queries, not raw observations or statistical samples.

That clarification is important because the lower bound is essentially dimension counting.

At an interior reference point, each exact query supplies one linear functional of R in the 2k-1 dimensional native span. Fewer than 2k-1 responses leave a nonzero common kernel, and small opposite perturbations preserve the deterministic adaptive transcript. This is a correct standard adversarial argument.

What it is **not**:

- a sample-complexity lower bound;
- a noisy inverse-problem lower bound;
- a minimax statistical lower bound;
- an information-theoretic lower bound under a finite experimental protocol;
- a theorem about how accurately the second contact jet can be estimated from data.

The manuscript mostly avoids these overclaims now. Nevertheless, the word “tomography” and the surrounding statistical model create an expectation of an observational inverse problem. The principal quantitative theorem is still an exact finite-dimensional oracle theorem.

At a top-four standard, I would want either substantially richer geometry or a genuine statistical inverse theorem. The current exact query count does not supply that missing significance.

## 7. The “native” class remains highly specialized

The principal theorem fixes:

- endpoint-free root pairs;
- the square-clock count 2k+1;
- calibrated polynomial binary observations;
- an injective quadratic loading measurement map;
- exact small-time contact;
- exact second jets;
- the particular Cauchy interpolation structure that yields the native span.

The manuscript is commendably explicit about some limitations. It even preserves the seven-clock overidentification counterexample and says not to extrapolate the exact square-clock Hankel congruence.

That honesty is good. But the consequence is that the theorem should not be sold as a broad information-geometric rigidity principle. It is a rigidity theorem for a special algebraic experiment.

The paper would be stronger if it identified the invariant abstract hypotheses under which the argument works and then proved that the binary experiment is one realization. At present the abstract part is incomplete: the conormal side is abstract, but the information side is still tied to one Cauchy/Hankel construction.

A top-four paper normally needs either much greater generality or a special case of exceptional depth. I do not yet see either.

## 8. The function-input endpoint theorem is a correct effective decision theorem, not a structural classification

Theorem thm:intrinsic-fibre is an honest improvement over v107 because it no longer requires a hidden reference representation.

For fixed e, the authors introduce the coefficients of Q as unknowns, write positivity, normalization, and KKT optimality as polynomial conditions, universally quantify over the observed graph, and apply quantifier elimination over real closed fields.

I believe this is correct in the stated exact algebraic input model. The strict convexity of the endpoint block makes the KKT formula necessary and sufficient; under a finite-representability promise, enumeration in e terminates at the first nonempty fibre.

But this theorem is very close to a direct application of Tarski-Seidenberg / real quantifier elimination once the model class has been written down.

Its output is:

- a finite semialgebraic description;
- an emptiness decision at fixed e;
- a sample point;
- termination under an external finite-representability promise.

It does not provide:

- a tractable complexity bound;
- an explicit normal-form classification;
- a finite intrinsic bound on e for arbitrary inputs;
- a structural description of the representation fibre beyond general semialgebraicity;
- a new quantifier-elimination method.

The manuscript itself now admits most of this. That is progress.

My recommendation is to demote this theorem from a second major selling point to an effective companion proposition unless the authors can extract new geometry from the resulting fibres. As written, it closes a logical input-category gap; it does not add another top-four-level theorem.

## 9. The inverse-parametric-programming comparison is now substantially better

R107 asked for direct comparison with Hempel–Goulart–Lygeros and Nguyen–Olaru–Rodriguez-Ayerbe–Hovd–Necoara.

That request is substantially closed.

The new discussion correctly distinguishes a supplied continuous piecewise-affine optimizer/output map from the present supplied scalar optimal-value graph. It also avoids the previous inaccurate suggestion that those inverse-programming papers simply assume a known hidden active fan.

The parameter-only objective-addition observation is a good clean reason why optimizer reconstruction alone cannot identify the observed value function.

I would keep this discussion.

However, closing this literature gap exposes rather than cures the venue problem: once the companion inverse-programming theorem is correctly contextualized as a restricted value-function representation problem solved by quantifier elimination, it contributes less to the paper's high-level novelty than the previous rhetoric suggested.

## 10. The reciprocal-fibre theorem is clean and correctly separated

The new abstract reciprocal-fibre lemma is one of the better editorial changes in v108.

It makes clear which statements come from:

- strict convexity of sum a_j / omega_j on a positive affine fibre;
- the positive covector that bounds the fibre;
- the corank of the moment map;

and which statements are supplied by the binary experiment.

The singleton boundary fibre and S^{d-1} interior fibre follow cleanly by radial parametrization in the kernel directions. The d=2 endpoint-free case yields S^1 fibres because the moment map has corank two.

I do not see a problem with this argument in the scope reviewed.

But it is a general convex lemma of modest difficulty. Its top-level contribution is the transport of this already-understood fibre geometry through the contact recovery map. That transport is linear once the metric has been recovered.

Again, the result is correct and tidy, but it does not compensate for the limited depth of the principal mechanism.

## 11. The local second-jet calculation appears sound

I specifically checked the formula relating the contact Hessian to the normal restriction of R.

For a smooth point q_A(eta), the quadratic term of the squared R^{-1}-distance to the embedded rank-one manifold is obtained by minimizing the ambient quadratic form modulo the tangent space. If n lies in the Euclidean normal space, the dual normal quadratic value is indeed n^T R n.

The three-root specialization

\[
 D^2 C_R(q(\eta))
 =
 \frac{2n_A(\eta)n_A(\eta)^{\mathsf T}}
      {n_A(\eta)^{\mathsf T} R n_A(\eta)}
\]

has the correct factor under the manuscript's convention, and the directional normalization v=n/(n^T n) gives the reciprocal relation used in the five-curvature theorem.

I therefore do not base the rejection on an error in this calculation.

## 12. The determinant-kernel proof is acceptable, but the proof should be rewritten with the classical geometry visible

The elementary proof of the d>=3 vanishing statement is sound in outline:

- split the normal-coordinate space into a lift of Sym_d plus ker A_A^*;
- eliminate pure kernel and mixed terms;
- reduce to a quadratic polynomial f on Sym_d vanishing on singular matrices;
- diagonalize S=U diag(t) U^T;
- for fixed U, a degree-two polynomial in t_1,...,t_d vanishing whenever any coordinate is zero must vanish when d>=3;
- for d=2, direct coefficient comparison leaves the determinant.

This proof is not wrong. The problem is that it disguises a classical algebraic-geometric object as if it were model-born.

I would actually prefer a revised proof structure that says:

1. the rank-one cone is the affine cone over v_2(P^{d-1});
2. its dual discriminant is det=0;
3. the ambiguity space is the degree-two part of the ideal of that dual variety pulled back by A_A^*;
4. because det has degree d and is irreducible, the degree-two piece is zero for d>=3 and one-dimensional for d=2;
5. give the current real-coordinate proof as an optional elementary appendix.

That would be shorter, conceptually clearer, and honest about priority.

## 13. The three-site native span calculation is useful but not, by itself, a new Hankel theory

The manuscript proves that the native span is described by

\[
 \frac{(r_j-r_i)X_{ij}}{d_i d_j}
 -\frac{(r_l-r_i)X_{il}}{d_i d_l}
 +\frac{(r_l-r_j)X_{jl}}{d_j d_l}=0.
\]

The dimension count is k free diagonal entries plus k-1 divided-difference parameters, hence 2k-1.

This is a good explicit coordinate description. It should remain.

But the paper should be careful about calling this a deep “Hankel information geometry” phenomenon. Algebraically it is a linear Cauchy interpolation identity inside Sym_k. The important new point is its intersection with the conormal ambiguity, not the existence of the linear relations themselves.

That new point is strongest for k=3,d=2, where there is exactly one relation and exactly one ambiguity. In higher k the native subspace has larger codimension, but the arbitrary-metric conormal ambiguity is still only one-dimensional in d=2, so only one scalar transversality is needed for injectivity.

This reinforces the assessment that the current coupling mechanism is simpler than the manuscript's scale suggests.

## 14. The paper is still too large relative to its new centre

V108 has improved the theorem hierarchy. The principal theorem is now named, the companion endpoint theorem is labelled as such, and old material has been moved into appendices.

Nevertheless the manuscript still includes the complete historical machinery of finite-map reduction, weighted jets, tensor envelopes, endpoint visibility, local experiments, real resolution, binary inverse results, and earlier positioning text.

Preservation of prior work is a repository-management objective. It is not automatically a good publication architecture.

For a general top-four article, the relevant question is not whether every previous proof is retained. It is whether every included theorem is needed to understand the central contribution.

The answer is still no.

A paper whose genuinely new centre is:

- classical Veronese duality in measured coordinates;
- one native Cauchy/Hankel transversality condition;
- exact finite-dimensional recovery;
- reciprocal fibre transport;

does not become stronger by carrying a long archive of companion results. The archive instead makes it harder to see the true scale of the main advance.

I would require a serious editorial separation. This is not a request to delete mathematics from the repository. It is a request to distinguish the journal article from the repository's accumulated theorem archive.

## 15. Exact-source reproducibility is not closed at the reviewed commit

This is a concrete, objective defect.

The exact reviewed HEAD is:

4ed51300c2aa6e7b11e701a38ed1d14f8b9e8191

At that commit, paper.tex contains inputs to:

- article/v108/prepared/synchronized.tex
- article/v108/prepared/geometry.tex
- article/v108/prepared/endpoint-completion.tex
- article/v108/prepared/positioning.tex

Those files are **not present** at the reviewed HEAD.

Likewise:

- article/v108/evidence/verification.json is not present;
- the branch HEAD remains 4ed51300c2aa6e7b11e701a38ed1d14f8b9e8191 during this review;
- no successful exact-source evidence commit is therefore part of the reviewed object.

The preparation script explains the intended workflow: generate the prepared files, commit them, build that exact source commit, then add a separate evidence commit.

That design is reasonable.

But an intended future workflow state is not evidence for the current source commit.

Accordingly:

- I cannot treat the current HEAD as a self-contained compilable source package;
- I cannot mark R107.8 closed;
- any later generated source/evidence commit would need to be separately pinned and, if it changes the reviewed source tree, separately reviewed.

This is not evidence that the mathematics is false. It is a reproducibility and submission-integrity defect.

## 16. Independent finite diagnostics

I independently ran exact symbolic spot checks separate from the author's checks.

They reproduce:

1. **d=2, k=4:** the sampled conormal quadratic measurement operator has rank 9 on Sym_4, hence nullity one; the matrix B_A with squared 2x2 minors lies in that kernel.

2. **d=3, k=6:** for an explicit injective loading family, sampled normal restrictions span all 21 coordinates of Sym_6.

3. **k=4 native relations:** the three-site constraint matrix has rank 3 inside the 10-dimensional symmetric space, leaving dimension 7=2k-1.

The script and result are stored with this report.

These computations support the finite-dimensional algebra. They do not establish the universal theorem and do not address originality.

## 17. Assessment of the previous R107 requests

### R107.1 — Prove an interaction theorem

**Substantially closed mathematically, but a new priority problem appears.**

The d=2 native transversality really does make the Hankel restriction essential. This is no longer mere coexistence.

However, the conormal ambiguity being intersected is the classical quadratic-Veronese discriminant ambiguity, and the remaining interaction is one-dimensional linear transversality.

### R107.2 — Decide the single principal theorem

**Improved, but not fully closed editorially.**

The paper now names one principal theorem and demotes several older results to companion appendices. That is a major improvement.

The manuscript is still too large and historically cumulative relative to the new central mechanism.

### R107.3 — Function-only endpoint inverse data

**Closed as an effective decision problem; not upgraded to a structural classification.**

The input is now genuinely the scalar graph. Fixed-e fibres are definable and decidable by quantifier elimination. Minimal e is found under a representability promise.

This should not be advertised as an explicit classification.

### R107.4 — Inverse-parametric-QP literature

**Closed to my satisfaction.**

The cited comparisons are now direct and materially accurate.

### R107.5 — Novelty of reciprocal fixed-budget fibres

**Substantially closed in positioning.**

The general convex lemma is separated from the model-specific reciprocal transform and corank.

The result is clear but modest.

### R107.6 — Use the Hankel restriction downstream

**Closed in d=2, vacuous for identifiability in d>=3.**

This is now a real theorem in the two-shared-parameter case. In higher shared dimension arbitrary metrics are already identifiable.

### R107.7 — Tighten statements

**Mostly closed.**

The full residual versus profiled quotient, b>=0 target domain, spanning margin, reciprocal boundary notions, and perturbation class are now much better controlled.

### R107.8 — Exact-source native replay

**Not closed at the reviewed HEAD.**

The current source commit references generated files that are absent and contains no successful evidence receipt.

## 18. Required changes for any top-four reconsideration

I would not recommend another revision that merely patches the items below locally. The next version must change the novelty profile of the paper.

### R108.1 — Rebase the conormal theorem on classical projective duality and redo the novelty accounting

Cite the classical fact that the dual of the quadratic Veronese is the determinant/discriminant hypersurface.

State explicitly which part of the conormal-kernel lemma is classical.

Then identify a theorem that is genuinely new after this classical input is removed from the novelty claim.

A new proof of a classical fact in application coordinates is not enough.

### R108.2 — Produce a native interaction beyond one-dimensional d=2 transversality

For a top-four claim, the paper needs a regime where native information geometry changes the inverse problem in a structurally richer way.

Possible directions include non-injective measurements, partial normal data, overidentified clocks, endpoint-coupled tomography, or higher-order jets.

The authors need not choose these exact directions, but the next central theorem should not reduce to “classical ambiguity line + one linear native constraint.”

### R108.3 — Clarify the status of d>=3

Either:

- separate the generic-metric d>=3 tomography theorem from the genuinely native d=2 theorem; or
- prove a new d>=3 consequence for which the native Hankel structure is essential.

Do not let “all d>=2” suggest a dimension-uniform native mechanism when there is none.

### R108.4 — Upgrade or demote the exact-query result

If the query theorem remains central, connect it to an observational problem: noise, finite samples, stable jet estimation, or a meaningful minimax criterion.

Otherwise present the 2k-1 result for what it is: an exact linear-oracle dimension theorem.

### R108.5 — Demote the quantifier-elimination endpoint theorem unless new fibre geometry is proved

The function-input theorem is useful as a completeness statement. It should not carry top-level novelty unless the authors extract structural information that is not a generic consequence of real quantifier elimination.

### R108.6 — Rewrite the journal article around the actual dependency spine

Keep the full historical mathematics in the repository if desired.

But the submitted article should include only:

- the classical geometric input with correct attribution;
- the genuinely new information-geometric interaction;
- the statistical/contact theorem needed to interpret it;
- consequences that materially depend on that interaction.

The current appendix archive is still too large for the strength of the centre.

### R108.7 — Close source-bound replay on an exact, self-contained source commit

The reviewed source commit itself must contain every input needed by paper.tex.

Then provide a separate, successful evidence commit containing:

- exact source SHA;
- source manifest;
- final TeX log with no unresolved citations/references;
- PDF hash;
- independent finite-check receipts;
- workflow URL.

Do not claim closure for 4ed51300c2aa6e7b11e701a38ed1d14f8b9e8191; that commit does not contain the prepared inputs.

## 19. Minor and proof-level comments

1. In the main theorem, state the necessary feasibility condition k >= d(d+1)/2 next to injectivity of A_A. It is immediate but helps readers understand the measurement regime.

2. In part (a), call the ambiguity classification “quadratic ambiguity of the pulled-back Veronese discriminant” or equivalent. This would expose the classical geometry immediately.

3. In d=2, distinguish carefully between the ambiguity line in the ambient vector space and the actual positive-definite fibre segment. The manuscript mostly does this correctly.

4. The lower-bound theorem should formally define the deterministic exact-real scalar oracle model in one sentence. The proof uses that model exactly.

5. Keep the statement that equal second jets do not imply equal full contact functions in the exceptional family. This is an important limitation.

6. Keep the distinction between ordinary directional curvature in the three-root hypersurface case and dual normal quadratic queries in higher codimension.

7. The transversality invariant tau_A is useful. Consider phrasing it intrinsically as evaluation of the native annihilator on the determinant ambiguity before expanding it into root/interpolation coordinates.

8. The phrase “conormal rigidity” is stronger than the content in d>=3 if no classical attribution is supplied. With the Veronese duality made explicit, a more specific title may be preferable.

9. The fixed-budget observable region is convex because it is a linear image of the reciprocal-value sublevel set. This is clear; do not overstate it as a new general convexity principle.

10. The function-input theorem should state prominently that the effective algorithm may have enormous quantifier-elimination complexity and that no practical reconstruction complexity is claimed.

11. The current source date and reviewed commit should be printed in the PDF or accompanying submission metadata so that a referee can tell whether a later workflow-generated commit has changed the source.

12. The new inverse-programming references are appropriate. Keep them in the main text rather than only the response letter.

13. Add a foundational projective-duality/discriminant reference. GKZ is the obvious starting point.

14. Consider whether the B_A formula is best presented as the pullback of the 2x2 determinant polarization. That would make its invariance and classical origin clearer.

15. The independent finite checks confirm representative ranks but should remain explicitly non-certifying, as the manuscript already does with its own checks.

## 20. Final recommendation

Revision 108 has solved the most serious structural defect of v107: there is now an actual theorem in which the synchronized contact geometry can constrain recovery of the native inverse information.

That is meaningful progress.

But the new theorem also reveals that the manuscript's conceptual centre is less novel than its current presentation suggests. The conormal ambiguity calculation is the classical discriminant geometry of the quadratic Veronese in linear coordinates. In shared dimension two, the native model removes the resulting determinant line by an explicit linear transversality condition. In higher shared dimension, the native restriction is unnecessary for identifiability. The remaining sharp query count is a finite-dimensional exact-oracle dimension argument, and the function-only endpoint theorem is a standard real-quantifier-elimination construction.

This is a coherent and potentially publishable body of mathematics. It is not, in its present form, a general top-four paper.

The paper needs either a substantially deeper native interaction theorem or a much broader inverse-geometry result whose content survives after the classical Veronese/discriminant input is properly credited. Merely adding the missing citation and completing the workflow would not be enough to change my recommendation.

The exact reviewed HEAD also fails the source-closure criterion because its required prepared inputs and verification receipt are absent.

**Recommendation: reject in the present form. A future top-four reconsideration would require a new conceptual theorem, not another round of local repairs.**
