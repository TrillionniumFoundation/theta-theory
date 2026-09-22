# Independent harsh referee report on A2 revision 112 — second external round

Repository: TrillionniumFoundation/theta-theory

Revision branch reviewed: revision/a2-v112-components-schemes-quantitative-experiments-2026-09-21

Mathematical source commit: 0c696736e6ec22259c730672f61ebd8ef0d95460

Revision branch head inspected: e8eb87d4b22e341295175e2c3223fd21c68f41df

Principal manuscript: papers/A2-v17-boundary-information-coarsening/article/v112/paper.tex

Title: Recovery of information metrics: multiplication failure schemes

Referee standard: a general top-four mathematics journal (Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica level)

Recommendation: **Reject in the present form at a general top-four mathematics journal.**

I would not interpret this recommendation as saying that the manuscript has no substantial mathematics. Revision 112 is the strongest version of this line that I have examined. It contains a real structural theorem, not merely a collection of dimension counts and examples. My negative recommendation is driven by the gap between that theorem and the conceptual reach, completeness, priority positioning, and inevitable organization normally required for a general top-four paper.

## 1. Repository and provenance audit

Before discussing the mathematics, I record the exact repository state because the branch naming is currently misleading.

Two branches named as A2 revision 113 are present:

- revision/a2-v113-all-dimension-residual-wall-2026-09-21
- revision/a2-v113-residual-conormal-complete-ranks-2026-09-21

They point to the same head. Relative to the v112 revision branch, their delta is the addition and formatting of the v112 referee report. I found no v113 principal manuscript at papers/A2-v17-boundary-information-coarsening/article/v113/paper.tex and no v113 response or verification package.

Accordingly, the latest actual mathematical manuscript in the repository is still v112. This report therefore reviews v112 and is based on a clean review branch created from the v112 revision branch, not from either misleading v113-named branch.

The source/evidence separation in v112 is otherwise good. The mathematical source is pinned separately from generated evidence. Compilation receipts and finite diagnostics are useful engineering evidence, but they are not treated here as proofs of universal mathematical claims.

## 2. Executive assessment

Revision 112 materially improves the paper.

The central improvement is Section 5. The manuscript now studies the maximal-minor scheme rather than only the reduced failure locus. In the stated stable range it introduces the nondegenerate component Phi_L and the signed secant components Sigma_epsilon; it proves Cohen--Macaulayness in expected codimension, reducedness at the wall, integrality in the strict determinantal regime, generic corank one, a Thom--Porteous cycle formula, and a residual multiplication mechanism explaining the equality

    a - b = L * C(c,2) - (2k-5).

The signed-secant refinement is mathematically natural. The common-secant component from earlier versions is indeed only one sign pattern. The residual removal of the two secant points is also the most conceptually interesting idea in the present manuscript.

The statistical repair is also real. The Poisson-to-Gaussian comparison is no longer justified only by a weak limit; the manuscript supplies a total-variation argument. The deterministic quantized score protocol closes the exact-lattice-encoding loophole in a sensible way. The authors now distinguish raw counts, score compression, computed distance features, and independent noisy distance observations.

These changes fix several important deficiencies of v111.

However, the paper still does not meet a general top-four standard for four independent reasons.

First, the new structural theorem remains highly special: binary forms, quadratic multiplication, Hankel annihilators, products of Grassmannians, and a stable range. The paper does not yet extract a general principle from which the two extremal components and the residual wall follow.

Second, the scheme-theoretic story is incomplete exactly at the most interesting geometry: component intersections at the wall and the excess-codimension regime.

Third, several logically decisive proof transitions are still compressed. I do not currently see a one-line counterexample, but I would require fuller arguments before treating the global component theorem as publication-ready at this level.

Fourth, the priority audit is explicitly incomplete, while priority is central to the venue claim. In particular, the manuscript itself admits that Ballico's 1993 failure-locus paper has not been fully examined. I confirmed the bibliographic existence of E. Ballico, "On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces," Mathematische Nachrichten 163 (1993), 5--13, DOI 10.1002/mana.19931630102. I am not claiming that this paper contains the theorem of v112; I am saying that a general top-four submission cannot leave such an obviously adjacent antecedent unread while asking the referee to certify novelty.

For a strong specialized journal in algebraic geometry, algebraic statistics, inverse problems, or mathematical statistics, the present manuscript is much closer to a serious submission. For a general top-four journal, it still lacks another conceptual layer.

## 3. What v112 genuinely fixes

The improvement from v111 should be recognized precisely.

### 3.1 From a codimension minimum to a component theorem

The previous central formula was

    codim Delta^(L) = min{ L*C(c+1,2) - (2k-1) + 1, Lc - 3 }.

That formula by itself did not explain why the two endpoints were geometrically privileged.

Revision 112 now proposes a structural answer in the stable range c >= 8 and k >= 2c+1.

If a < b, the maximal-minor scheme is claimed integral and Cohen--Macaulay, supported on a full-rank-Hankel component Phi_L.

If a = b, the scheme is claimed reduced and Cohen--Macaulay with one full-rank component plus 2^(L-1) signed rank-two secant components.

If b < a, the signed secant components are claimed to be exactly the maximal-dimensional irreducible components.

This is qualitatively stronger mathematics than the earlier version.

### 3.2 The residual wall is a real mechanism

The identity

    a - b = L*C(c,2) - (2k-5)

is not used merely as arithmetic. After factoring the common quadratic g from the radicals of a rank-two Hankel annihilator, the residual problem becomes multiplication by (c-1)-planes in a (k-2)-dimensional binary space.

That is the best conceptual feature of the paper.

It converts the wall between the full-rank and rank-two mechanisms into a saturation threshold for a residual multiplication problem. The tangent computation of the signed components then uses the already proved full-range codimension theorem at (k-2,c-1), rather than an induction on the new structural theorem.

### 3.3 The scheme language is more disciplined

The manuscript now distinguishes:

- the reduced support Delta^(L);
- the maximal-minor scheme D_L;
- expected codimension versus excess codimension;
- generic scheme smoothness versus global smoothness;
- reducedness in the expected-codimension regime versus the unclassified excess scheme.

This is a substantial improvement in mathematical hygiene.

### 3.4 The statistical comparison is technically more defensible

The jittered Poisson comparison now supplies an explicit L1 / total-variation bound of order N^(-1/5). The deterministic quantization theorem supplies a second route with error controlled by

    N^(-1/5) + 1/(sqrt(N)*eta_N) + eta_N.

These arguments are not optimal-rate results, but optimality is not claimed. The key point is that the paper no longer infers a strong Le Cam conclusion from weak convergence alone.

## 4. Principal top-four blocker: the structural theorem is still too special

Theorem 5.1 is now the paper's true mathematical center. The venue question should therefore be answered by asking what principle that theorem reveals.

At present, the theorem is tied simultaneously to:

- the source curve P^1;
- binary forms;
- quadratic multiplication Sym^2(U);
- Hankel/catalecticant annihilators;
- a product of independently varying Grassmannians;
- c >= 8;
- k >= 2c+1;
- expected codimension for the complete scheme statement.

This is a strong special-case classification. It is not yet a general theory.

The paper still does not determine whether the two-endpoint phenomenon is fundamentally:

- a theorem about binary quadratic multiplication;
- a theorem about apolar/catalecticant rank stratification;
- a theorem about secant-versus-determinantal competition;
- a first case of Sym^m(U) multiplication for m >= 3;
- a first case of a Veronese or higher-dimensional source theorem;
- or a manifestation of a more invariant deformation-theoretic recursion.

A general top-four paper can certainly be about a special object. But then the classification usually needs to be so complete, unexpected, and structurally explanatory that the special case becomes a model theorem. Revision 112 has not yet reached that level.

The current manuscript explicitly chooses not to pursue higher products. That is a legitimate scope decision. It does not, however, remove the significance question.

A materially stronger paper would need at least one of the following:

1. a theorem for Sym^m(U) with m >= 3;
2. a higher-dimensional source / Veronese analogue;
3. a recursive structural theorem for all annihilator ranks and all residual strata;
4. a complete all-c classification, including exceptional low-dimensional equality cases;
5. an invariant geometric principle from which the signed components and residual wall become formal consequences.

Without such an advance, the main theorem reads to me as a strong specialized classification rather than a general mathematical breakthrough.

## 5. The scheme geometry is incomplete exactly where it becomes most interesting

The title now foregrounds "multiplication failure schemes." That raises the standard for the scheme-theoretic analysis.

### 5.1 The wall a = b

At the wall, the theorem claims exactly

    1 + 2^(L-1)

minimal components.

But the paper says almost nothing about how these components meet.

The missing geometry includes at least:

- Phi_L intersect Sigma_epsilon;
- Sigma_epsilon intersect Sigma_epsilon' for distinct sign patterns;
- codimensions of these intersections;
- generic local equations on the intersections;
- tangent cones;
- singularities produced by the intersections;
- normalization and seminormality questions;
- whether there is a combinatorial incidence complex indexed by sign patterns;
- whether pairwise intersections themselves admit residual descriptions.

This is not a cosmetic omission. The wall is precisely where two mechanisms have equal codimension. Their intersections are where the geometric transition should be most visible.

A paper whose central theorem is a scheme decomposition should not stop at the generic points of the irreducible components.

### 5.2 The excess regime b < a

The manuscript is appropriately honest that, in the excess regime, it classifies only maximal-dimensional components.

It does not classify:

- smaller components;
- embedded associated primes;
- unmixedness;
- nilpotent structure;
- the complete singular locus;
- the entire annihilator-rank stratification.

For a specialized journal, that may be acceptable.

For a general top-four claim, it leaves the scheme theorem visibly unfinished.

### 5.3 The local probability exponent avoids the hard geometry

The local small-singular-value exponent is proved only near smooth corank-one points disjoint from other components.

That result is correct in spirit and useful, but it is deliberately insulated from:

- component intersections;
- higher-corank points;
- singular residual strata;
- excess components;
- global random loading laws.

So it should not be used rhetorically as if the paper now understands conditioning near the global failure scheme. It understands conditioning near selected smooth points.

## 6. Proof-completeness concerns in the new structural theorem

I do not currently identify a fatal false statement. My concern is that several global conclusions depend on arguments that are still too compressed for a theorem of this strength.

### 6.1 From annihilator incidence dimensions to all irreducible components

The proof of Theorem 5.1 uses the strict rank-gap lemma to conclude that the generic annihilator rank on a top-dimensional component must be either k or 2.

That is plausible, but the manuscript should isolate and prove a general incidence-to-component proposition.

A clean statement would be something like:

> Let C be an irreducible component of the support of the maximal-minor scheme. On a dense open subset of C, the projective annihilator space has constant dimension and its intersection with each Hankel rank stratum has constant generic behavior. If a rank-r stratum dominates C, then C is dominated by the corresponding rank-r incidence.

The present proof passes rapidly from dimension bounds for the pair incidence ([ell],U) to a complete list of components of the projection.

At a general top-four level I would not want this transition left implicit.

In particular, the proof should rule out carefully the possibility that the generic annihilator projective space on a component has positive dimension and moves through several rank strata in a way not detected by choosing one generic annihilator.

The corank-one arguments later make this unlikely, but the logical order should be explicit.

### 6.2 Birationality of the nondegenerate incidence needs one more written step

For Phi_L, the manuscript argues:

- dim F_L = dim Phi_L;
- therefore the generic fibre is zero-dimensional;
- the fibre is the full-rank open subset of the projective annihilator space;
- therefore the generic multiplication corank is one;
- therefore the generic fibre is one point.

I believe the intended argument is sound, but the key linearity step should be stated.

If the projective annihilator space had dimension at least one, its intersection with the open set of full-rank Hankel forms would be either empty or positive-dimensional. Since it is nonempty on the full-rank incidence, a zero-dimensional generic fibre forces the projective annihilator space itself to be a point.

Write this explicitly. The present version asks the reader to supply the decisive argument.

### 6.3 The residual map should be proved dominant

In the signed-component smoothness argument, the manuscript writes

    W_nu = g K_nu

and then treats the K_nu as independent general (c-1)-planes in V_(n-2).

This is intuitively correct from the relative-Grassmannian parametrization, but it is one of the central inputs to the residual saturation argument.

I would require an explicit morphism from the dense signed incidence to

    Gr(c-1,V_(n-2))^L

and a proof that it is dominant, preferably with a description of the fibre.

Without that statement, "general signed incidence gives general residual planes" remains a sentence where a theorem-level dominance claim is being used without being formally proved.

This is especially important because the generic smoothness of every signed component depends on applying the earlier full-range saturation theorem to these residual planes.

### 6.4 The rank-two sign decomposition deserves a normalization statement

The manuscript's sign count is convincing, but the geometry would be cleaner if it were formulated through the normalization of the rank-two annihilator incidence.

A rank-two quadratic form has two isotropic hyperplanes. Globally those two hyperplanes are exchanged by the natural double cover of the rank-two base. For L contacts, the sign sectors should be described as the relative product of these two choices modulo the simultaneous deck transformation.

That formulation would explain conceptually why the count is 2^(L-1), and it would prepare the missing intersection theory.

The present coordinate construction with h_+ and h_- is adequate for generic counting, but not yet the most invariant form of the theorem.

### 6.5 The Eagon--Northcott step should be split into formal propositions

The expected-codimension argument is essentially:

- on each affine Grassmannian chart, the maximal-minor ideal has height a;
- the chart ring is regular;
- grade equals height;
- Eagon--Northcott resolves;
- the quotient is Cohen--Macaulay and unmixed;
- generic reducedness on all minimal components implies reducedness.

This is a reasonable argument.

But because the whole-scheme conclusion is one of the paper's main upgrades, I recommend separating the commutative algebra into explicit propositions:

1. expected grade of the maximal-minor ideal on every nonempty chart;
2. Eagon--Northcott perfection / Cohen--Macaulayness;
3. no embedded associated primes;
4. generically reduced plus no embedded primes implies reduced.

The current proof compresses all of this into one long theorem proof.

### 6.6 Low-dimensional equality cases are not merely bookkeeping

The stable range c >= 8 and k >= 2c+1 is introduced partly to eliminate equality cases in the rank optimization and maximal orthogonal-Grassmannian bifurcations.

For a specialized paper this is fine.

For a top-four structural theorem, I would want either:

- the complete exceptional list, with the geometry of each exception; or
- a conceptual reason why the small cases form a different class.

At present the stable range looks partly technical rather than intrinsic.

## 7. The priority audit is not sufficient for a top-four novelty claim

The authors' LITERATURE_AUDIT.md is more responsible than the literature sections of earlier revisions because it states explicitly that it is not an exhaustive priority certificate.

That disclaimer is also enough to block a general top-four recommendation.

The paper concerns a cluster of classical topics:

- failure loci of projective embeddings;
- quadratic normality;
- non-complete linear series;
- rational normal curves and their projections;
- secant spaces;
- catalecticant/Hankel rank loci;
- degeneracy loci on Grassmannians;
- maximal-rank multiplication maps.

The bibliography is still surprisingly short for a manuscript whose central novelty claim sits at the intersection of these subjects.

Most importantly, the audit itself says that Ballico's 1993 paper on higher-order failure loci was not fully examined.

That paper is:

E. Ballico, "On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces," Mathematische Nachrichten 163 (1993), 5--13, DOI 10.1002/mana.19931630102.

The point is not that I have found a theorem there that kills the novelty of v112. I have not made that claim.

The point is that a referee should not be asked to certify top-four novelty while the authors explicitly leave unread a close antecedent whose title is almost a description of the paper's algebraic-geometric theme.

The literature review should also be expanded around:

- non-complete linear series on P^1;
- normal generation of projected rational normal curves;
- secant descriptions of failures of k-normality;
- determinantal and apolar descriptions of catalecticant degeneracy;
- incidence geometry of isotropic subspaces for varying symmetric forms.

A top-four version should state theorem-by-theorem what is new relative to the strongest antecedent, not only explain that the exact displayed formula does not appear in Green--Lazarsfeld or Ballico 1996.

## 8. The statistical half remains a second paper

The statistics in v112 are significantly cleaner, but they still do not provide the missing conceptual layer for the algebraic theorem.

The direct count-to-contact experiment is built around:

- known mark laws;
- a preassigned interior centre lambda^0;
- a least-favourable local section B_* h;
- a fixed contact compression L;
- either artificial jitter or deterministic finite-precision quantization.

Within that model, the local information calculation is useful and largely convincing.

But once the Poisson experiment has been reduced to a Gaussian shift, the formula

    L^T (L Sigma L^T)^dagger L

is standard Gaussian linear algebra.

The deep part remains the rank of L, which is the algebraic multiplication problem.

Conversely, the algebraic theorem does not need most of the statistical sections.

The resulting manuscript still contains two papers:

1. an algebraic-geometric paper on multiplication failure schemes of binary subseries;
2. a statistical paper on known-mark local score compression and finite-precision Gaussian comparison.

The connection is real but not yet inevitable.

For a general top-four paper I would either:

- split them; or
- prove an intrinsic statistical theorem whose singularity structure genuinely depends on the newly classified component intersections and excess geometry.

At present the statistics use the algebraic geometry mainly as a rank criterion.

## 9. Detailed comments on the algebraic geometry

### 9.1 Theorem 1.1 remains useful and should stay

The all-dimension codimension theorem is a solid organizing result.

It is important that the new stable-range theorem does not replace or weaken it.

### 9.2 Lemma 4.1: Hankel rank strata

The citation to Conca--Mostafazadehfard--Singh--Varbaro is now much more precise.

For final publication, I would still state in one self-contained paragraph the exact rectangular/square Hankel ideal identification needed here.

The result is too central to be left as a citation plus a sentence about changing shape.

### 9.3 Lemma 4.2: isotropic incidence dimensions

The dimension formula is standard and appears consistent.

Because orthogonal Grassmannians can be disconnected in the maximal case, the manuscript should flag exactly where the later stable inequality 2c < k guarantees geometric irreducibility of the fibres used in F_L.

### 9.4 Lemma 4.3 and Lemma 5.2: rank optimization

The arithmetic is improved and the strict-gap lemma is useful.

But the proof still feels like an integer optimization with a geometric interpretation added afterward.

A stronger paper would reverse this order: derive the two endpoints from a geometric dichotomy, then use arithmetic only to exclude intermediates.

The residual theorem partly accomplishes this for rank two. A comparable conceptual explanation for why no intermediate rank can compete would materially strengthen the paper.

### 9.5 Lemma 5.3: signed secants

The generic uniqueness of the secant hyperplane from the first c-plane is plausible and the dimension estimate is appropriate.

However, this lemma is doing several jobs at once:

- rationality of the base;
- uniqueness of the secant decomposition;
- construction of the partner involution;
- birationality of the plane incidence;
- uniqueness of the rank-two annihilator;
- distinctness of sign patterns.

I recommend decomposing it into two or three lemmas.

### 9.6 Lemma 5.4: nondegenerate incidence

The argument through the nonmaximal orthogonal Grassmannian is plausible.

The claim that the relative incidence is smooth and irreducible should be written in standard relative language:

- smooth morphism over the nonsingular Hankel open;
- geometrically irreducible fibres;
- irreducible base;
- hence irreducible total space.

This is present in substance but not stated as cleanly as it should be.

### 9.7 Lemma 5.5: corank-one chart

This is one of the cleanest parts of the new proof.

The local Schur-complement description is exactly the right tool.

I suggest extracting the conormal space explicitly, because that would make the later small-singular-value result look like a natural corollary rather than a separate calculation.

### 9.8 Lemma 5.6: signed-component smoothness

This is the conceptual highlight and also the place where I would demand the most detailed proof.

In particular:

- prove dominance of the residual K_nu map;
- state exactly which open set gives saturation;
- verify that the tangent solution using the b_nu coordinates is independent across contacts;
- state the resulting normal/conormal dimension as a proposition.

### 9.9 Thom--Porteous class

The use of the dual map is correct in form and should be emphasized because it removes a common sign/convention ambiguity.

At the wall, the equality of the fundamental cycle with the sum of component cycles is only as strong as the reducedness theorem. That dependency should be cross-referenced explicitly.

### 9.10 Real native strata

The distinction between Euclidean-open positivity and Zariski density is now handled responsibly.

Do not strengthen this into a statement about the global real locus of every component.

## 10. Detailed comments on the statistical sections

### 10.1 Cone LAN

The physical restriction v >= 0 is now visible and the two-sided analytic extension is no longer conflated with the physical parameter space.

That is an important repair.

### 10.2 N^(-1/4) root scale

The one-ray result is fine as a local boundary calculation.

It is not a new global nonregular minimax theory.

The manuscript mostly says this correctly and should continue to do so.

### 10.3 Poisson total variation

The new proof is much better than the old weak-limit argument.

For publication I would still give an explicit N_0(lambda_-,lambda_+) after which the Stirling/Taylor central-region estimate is valid, or state a lemma with all uniform constants collected.

### 10.4 Deterministic quantization

This theorem is useful because it removes the worry that exact real-valued compression can encode the entire integer vector.

Its conceptual status should nevertheless remain modest: it is a finite-precision implementation theorem for a chosen score statistic, not a new intrinsic observation principle.

### 10.5 Full exposure tangent model

The nuisance decomposition is helpful.

I would avoid the phrase "quotienting the experiment" unless a quotient experiment is formally defined. The proposition itself contains the concrete Gaussian decomposition, which is enough.

## 11. Organization and exposition

The principal manuscript is still too heterogeneous for the strongest version of its mathematical contribution.

The algebraic-geometric paper wants to be organized around:

1. the failure scheme;
2. annihilator-rank incidences;
3. the two extremal components;
4. the residual wall;
5. the complete wall/intersection geometry;
6. consequences for native realizations.

The statistical paper wants to begin from a rank criterion as an input and then study:

1. boundary LAN;
2. score compression;
3. finite precision;
4. nuisance structure;
5. singular local regimes.

Trying to do both in one article makes the paper feel cumulative rather than inevitable.

A top-four manuscript should make the reader feel that every section is forced by the main theorem.

Revision 112 is cleaner than v111 but still visibly carries the history of many revision rounds.

## 12. What would materially change my assessment

More diagnostics, more build receipts, more examples, or another structured matrix family would not change this recommendation.

A serious reconsideration at a general top-four level would require at least one advance of the following scale.

### A. Complete the wall geometry

Classify pairwise and higher intersections of the signed components and Phi_L.

Describe their codimensions, tangent cones, generic singularity types, and normalization/seminality properties.

### B. Complete the excess regime

Classify all associated primes or provide a recursive residual theorem that explains every lower-dimensional component and embedded structure.

### C. Generalize the multiplication theorem

Move from Sym^2 to Sym^m, or from P^1 to a broader source class, while retaining a sharp component theorem.

### D. Remove the stable-range restriction

Give the complete exceptional list and geometric explanation of low-dimensional phenomena.

### E. Build a genuinely intrinsic statistical singularity theory

Derive an observation experiment in which the newly classified algebraic singularities control a nontrivial family of minimax rates or local asymptotic experiments, rather than entering only through a rank test.

### F. Complete the priority audit

Read and compare the adjacent failure-locus and non-complete-linear-series literature theorem by theorem. Add the missing Ballico 1993 source and any stronger antecedents it leads to.

## 13. Recommendation

Revision 112 is a serious improvement and, in my view, contains publishable mathematics.

I do not currently see a short counterexample that invalidates its main theorem.

That is not enough for a general top-four recommendation.

The main theorem is still a stable-range classification for quadratic multiplication of binary subseries. The entire scheme is understood only in expected codimension. The most interesting component intersections are not analyzed. The excess regime is incomplete. Several global incidence-to-component arguments should be expanded. The priority audit is explicitly unfinished. The statistical half, while technically improved, remains largely separable from the algebraic theorem.

My recommendation is therefore:

**Reject in the present form at a general top-four mathematics journal.**

For a strong specialized journal, I would encourage a substantially reorganized version centered on the multiplication-failure scheme, after the proof details and priority audit are completed.

For a renewed general top-four attempt, I would not recommend another incremental response round. The next revision should add a new structural layer: either a complete recursive scheme theory or a genuine higher-product/higher-dimensional generalization.
