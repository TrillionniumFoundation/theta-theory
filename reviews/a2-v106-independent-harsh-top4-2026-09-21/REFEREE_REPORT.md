# Independent External Referee Report on A2 Revision 106

## Manuscript reviewed

**Title:** *Ramification, Hankel information, and endpoint metric quotients*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed source branch:** revision/a2-v106-residual-scale-hankel-endpoint-strata-2026-09-20  
**Pinned source commit:** 5cbbe96cd2ac590bfa2e17bcef97b0630cd91c4a  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v106/paper.tex  
**Review date:** 2026-09-21  
**Standard applied:** external referee standard for a general top-four mathematics journal.

This report is based on the v106 principal source and the inherited v104 components that v106 explicitly inputs. I also compared v106 against the v105 source line and the preceding independent referee report. The present report is not a review of the broader theta-theory program; it concerns the mathematical article represented by the pinned v106 source above.

## Recommendation

**Reject in the present form for a general top-four mathematics journal.**

This recommendation is materially different from the preceding v105 recommendation.

Revision 106 is a genuine mathematical revision. It is not a bookkeeping branch, and it does answer several of the previous referee's central requests. In particular, it adds a residual-scale reduction theorem, a divisorial certificate for the derivative regime, nontrivial first visibility-loss classifications, a model-native Hankel information theorem, and a local compatibility theorem linking the root, information, and endpoint constructions. I did not find a short counterexample to the principal new statements in this audit.

The reason for rejection is therefore no longer that the manuscript lacks serious mathematics. It plainly contains serious mathematics.

The present obstacle is that the article still does not establish, at the level of generality and inevitability expected for a general top-four journal, that the three substantial mechanisms assembled here constitute one intrinsic structural theory rather than three strong but partly model-dependent theories joined by a specially tractable compatibility example. The new divisorial theorem classifies a marked certificate, not the underlying observation germ independently of the marked finite-map presentation; the new binary compatibility theorem is natural but locally regular in the symmetric coordinates and collapses the root-label multiplicity to a single observed affine sheet; and the first visibility-loss theory, although genuinely new in scope relative to v104, remains a first-stratum analysis rather than a general degeneration theorem.

There is also a second, independent top-four obstacle: the novelty and priority analysis remains much too thin for the breadth of the paper. The four references added in v106 do not provide a theorem-by-theorem comparison with the closest literature on moment spaces, optimal design, total positivity and Cauchy systems, inverse parametric quadratic programming/complementarity, nuisance-efficient information, or algebraic/statistical identifiability. The manuscript now has stronger theorems than its literature section is capable of placing.

In short: v106 is a substantial advance over v104/v105, and several previous objections should be marked as answered. It is still not ready for top-four acceptance.

## 1. What v106 actually changes

The v106 branch is three commits ahead of the v105 mathematical line and adds a new principal article together with six new mathematical parts. The substantive additions are:

1. a residual-scale replacement of the radius-scale second-derivative hypothesis;
2. a proper-real divisorial criterion for the residual-scale derivative certificate;
3. an explicit nonlinear example at the true residual-scale boundary;
4. complete reconstruction when exactly one endpoint active cell is missing for endpoint dimension at least three;
5. a complete two-endpoint three-cell fibre calculation;
6. a rank-one cross-block degeneration analysis;
7. a calibrated binary family whose inverse efficient information lies in a finite Hankel moment cone;
8. exact secant and deterministic exact-query statements for the inverse-information image;
9. total-positivity consequences for endpoint visibility in the one-colour binary subfamily;
10. a compatibility theorem deriving root, efficient-information, and endpoint quotient objects from the same calibrated binary observation mechanism;
11. explicit equivalence conventions and expanded covering/minimal-competitor lemmas.

These are not cosmetic additions. Several of them are exactly the kind of mathematics requested in the previous report.

## 2. Disposition of the previous referee requests

The previous report should not simply be repeated. My assessment of those requests after reading v106 is as follows.

| Previous request | v106 status |
|---|---|
| Materialize an actual mathematical revision | **Closed.** v106 is a real mathematical manuscript. |
| Geometric characterization of the polar-gap regime | **Substantially addressed, but not fully closed at the claimed intrinsic level.** The divisorial theorem gives an exact criterion for the marked derivative certificate. |
| Natural unification rather than designed realization | **Partially addressed.** The calibrated binary model is natural relative to the preserved observation mechanism, but its local symmetric-coordinate observation is regular and its labelled root sheets collapse observationally. |
| First visibility-loss strata | **Substantially addressed.** The one-missing-cell theorem and the full two-endpoint three-cell fibre are meaningful advances. |
| Native tensor/secant theorem for a pre-existing model | **Substantially addressed.** The Hankel inverse-information theorem is the strongest new conceptual contribution in v106. |
| State equivalence relations globally | **Addressed.** Section 1 makes the categories materially clearer. |
| Expand the compressed covering and competitor arguments | **Addressed.** The new standalone lemmas are appropriate. |
| Expand the novelty map | **Not closed.** The literature additions are far too small for the breadth of the new claims. |
| Close source-bound archival/runtime evidence | **Not closed by the v106 mathematical delta.** I do not regard this as the principal mathematical reason for rejection, but it remains an archival issue. |

This is real progress. The remaining report should therefore focus on what the new mathematics does and does not establish.

## 3. The residual-scale theorem is a genuine strengthening

Theorem 2.1 is, in my view, one of the cleanest improvements in the revision.

The old reduction theorem controlled the nonlinear Taylor remainder through the tube radius via r(t)M(t). The new argument observes that a minimizing residual is localized at the much smaller scale c(t), and it replaces the decisive smallness condition by c(t)M(t) -> 0 while keeping c(t)/r(t) -> 0. The proof uses the first residual block to localize both exact and affine minimizers, then compares the Taylor error with the residual norm without dividing by a possibly vanishing branch residue.

That is the right mechanism. It also correctly shows that rM of order one is not itself a nonlinear boundary when c/r tends to zero.

I regard this as a meaningful theorem, not a repackaging of the v104 estimate.

### 3.1 The true scope must nevertheless be stated more sharply

The theorem still assumes the marked finite-map presentation F and a chosen tube avoiding the critical/boundary image. The quantity M is computed in fast F-coordinates, and the divisorial criterion that follows is a criterion for this marked presentation.

Section 1 now says this explicitly, which is good. But the introduction, abstract, and broader rhetoric still repeatedly move between:

- an invariant residual germ;
- a marked finite-map presentation;
- a tube chosen relative to that presentation; and
- a resolution of the resulting tube graph.

Those are not the same object.

A theorem that says “for this marked finite-map presentation, the certificate is equivalent to these divisorial inequalities” can be excellent mathematics. It should not be advertised as a canonical classification of the observation germ unless one also proves how the certificate transforms under changing the fast presentation itself.

At present the paper proves invariance under feasible source reparametrization transporting the marked F. It does **not** prove invariance under replacing F by a genuinely different finite set of fast observables defining the same residual germ.

That distinction should be promoted from a caveat to a structural part of the statement.

## 4. The divisorial criterion is strong, but it classifies the certificate rather than the full boundary theory

Theorem 2.3 introduces

J = det DF,  
P = DG adj(DF),  
N_2 = (J D_x P - P D_x J) adj(DF),

so that A_F = P/J and D_x A_F DF^{-1} = N_2/J^3.

After a proper real corner presentation, the theorem monomializes t, r, c, J and the norms of P and N_2 and reduces boundedness/smallness to finite inequalities among the exponent vectors. This is exactly the correct kind of application of real uniformization and normal crossings if all chart and accessibility details are handled as claimed.

I consider this a serious response to the previous complaint that the polar-gap condition was merely “checked”.

However, three points remain.

### 4.1 It is a classification of a sufficient-and-necessary certificate, not a classification of all affine-limit mechanisms

The manuscript itself eventually says this, but the distinction is crucial.

The theorem characterizes when the displayed derivative certificate holds. It does not prove that every singular germ with an affine leading quotient must satisfy that certificate in some canonical presentation. Therefore it is not a converse classification of all affine limits.

This is not a defect in the theorem. It is a defect only if the article treats the theorem as if it settled the intrinsic classification problem.

### 4.2 The perturbation statement is much weaker than the word “stability” suggests

The theorem says that the inequalities persist under perturbations preserving the displayed orders and the unit bounds.

But the order vectors and the resolution type are precisely the data that can jump under perturbation. Preservation after assuming those data remain fixed is useful bookkeeping; it is not yet a parameter-space stability theorem.

A top-four version should either:

- construct a finite parameter stratification on which one simultaneous resolution/order type works and prove stability on those strata; or
- sharply downgrade the language and state that no perturbation theorem across changes of resolution type is being claimed.

The current paragraph after Theorem 2.3 partly acknowledges this, but the main theorem and introduction still make the result sound more global than it is.

### 4.3 The proof should expose the simultaneous monomialization step as a theorem-level dependency

The proof currently compresses several delicate operations into one paragraph: pass to the compact positive-time tube graph, uniformize, resolve the product of the scalar and sum-of-squares factors, prune inaccessible components, factor the vector numerators, and then read off all suprema from accessible coordinate faces.

The inherited appendix makes this plausible, and I do not presently see a contradiction. Nevertheless this is now the central theorem of the first third of the article. A top-four submission should not make the reader reconstruct the exact simultaneous-resolution argument from an older general appendix.

I would require a standalone proposition that states the precise resolved space, proper map, retained components, treatment of identically zero numerator blocks, and the equivalence between the chartwise monomial bounds and the original tube suprema.

## 5. The nonlinear wall example is good, but one example is not a nonlinear boundary theory

Proposition 2.5 is valuable.

The example

F(y,x) = (y, x^3 + y^2 x),  
G(y,x) = yx^2,

with the stated target produces cM of order one and a genuinely nonlinear normalized residual set. The Euclidean cost is explicitly reduced to a one-variable polynomial minimization, and the affine-centre prediction can be strictly wrong.

This is exactly the kind of example the earlier versions lacked.

But the paper should be careful about what has been achieved.

The revision now identifies:

- a false wall: rM approximately one can be harmless when c/r -> 0;
- a true nonlinear example at cM approximately one.

It does **not** classify the possible normalized residuals at cM approximately one, nor prove that there is a canonical nonlinear normal form on that boundary.

Thus the first part of the paper now has a sharp certificate theorem plus an instructive failure example. It still does not have a general boundary classification.

For a specialized journal this could be entirely satisfactory. For a general top-four paper built around a claim of structural closure, I would expect one further theorem explaining at least a broad class of critical cM approximately one limits.

## 6. The endpoint section is materially stronger than v104

Theorem 4.1, the one-missing-cell theorem for e >= 3, is a substantial result.

The paper correctly separates loss of active-cell visibility from loss of cross-block rank. With B still full rank, all algebraic active-set Hessians remain distinct even if one active cell ceases to occur. The proof then reconstructs the missing information from rank-one and rank-two deficits, with separate arguments for a missing singleton, missing full cell, and missing empty cell.

This is exactly the right continuation of the fully visible Boolean-lattice theorem.

The explicit codimension-one example is also useful because it demonstrates that the nonvisible stratum is not empty or purely formal.

### 6.1 The two-endpoint three-cell fibre theorem is conceptually important

Theorem 4.3 shows something the earlier manuscript did not: in endpoint dimension two, loss of one cell can release a genuine scalar modulus rather than merely deleting a label.

That is a significant structural phenomenon.

The chain, missing-empty, and missing-full cases also explain why one cannot infer fibre rigidity solely from the number of remaining quadratic pieces.

### 6.2 The proof is too compressed for the strength of the classification claim

The classification uses several nontrivial assertions about a two-dimensional KKT fan:

- exactly three local matrices imply the stated chain/fork order types;
- every minimal competing representation has the same order type;
- the selected signs of u and v are intrinsic;
- the one-parameter normal forms exhaust all competitors;
- the ratio bounds are simultaneously necessary and sufficient on the whole retained cone;
- no alternative gluing of the same three quadratic forms is possible.

I believe the intended geometry is plausible. But these steps are currently compressed into prose in a way that makes independent verification harder than it should be.

For a theorem claiming the **entire** minimal fibre, I would require a separate planar-fan classification lemma with a complete case table and explicit derivation of the normal forms from KKT inequalities.

This is especially important because the theorem is not merely local identification of parameters. It is a global equality statement for value functions on the whole labelled orthant.

### 6.3 The first nonvisible strata are now treated; the general nonvisible problem is still open

The new results cover:

- exactly one missing cell with full rank for e >= 3;
- all three-cell full-rank cases for e = 2;
- a rank-one cross-block degeneration for e = 2.

That is a good first-stratum theory.

It is not a classification of general visibility loss for e >= 3, where multiple cells can disappear, several Hessian differences can coalesce, rank can drop, and different combinatorial fans can share the same observed pieces.

The manuscript should describe these new theorems as first-stratum classification results, not as if the endpoint inverse problem has now been globally solved.

## 7. The native Hankel theorem is the strongest new conceptual contribution

Theorem 6.1 is, to my reading, the most promising part of v106.

The model is no longer constructed by selecting contrast vectors to realize a desired Q. Instead, one begins with calibrated binary observations, polynomial component factors, separated repeated clusters, simple endpoints, clocks, and exposures. At the minimally identifying clock count, the scalar score matrix is square. Lagrange interpolation then gives explicit columns of the inverse score map, and nuisance profiling forces

R = Q^{-1}

to be a fixed congruence of a finite Hankel moment cone.

This is a real mechanism.

The important point is not that Hankel cones or Cauchy matrices are new. They are not. The important point is that this particular observation model **forces the inverse efficient information** into that class.

That model-to-geometry implication is the genuinely interesting statement.

### 7.1 The interpolation proof should be isolated and made easier to audit

The proof currently moves quickly through:

- invertibility of the rational score system;
- multiplication by h(T);
- polynomial interpolation at the clocks;
- extraction of highest principal-part coefficients;
- construction of the Cauchy-form columns;
- change to the polynomial basis p_*(T)/(T-rho_a);
- identification of the full Hankel span.

This chain is elegant, but it is also where a sign, degree, or indexing error would propagate into every subsequent secant and visibility theorem.

I recommend promoting the coefficient-inverse identity to a standalone algebraic theorem or lemma, with dimensions displayed at every stage and a short worked n = 2 or n = 3 example.

Finite symbolic checks are welcome here, but they are not a substitute for this exposition.

### 7.2 The exact query theorem is correct in spirit but should remain secondary

Once the R-image is relatively open in a linear space of dimension 2n-1, exact noiseless quadratic-form query complexity is essentially finite-dimensional linear algebra. The adaptive lower bound by two opposite perturbations with identical transcripts is standard in spirit and appears sound.

The manuscript correctly says this is not sample complexity.

I would not make the query result a major significance claim in a top-four submission. It is a clean corollary of the geometric classification, not a separate conceptual breakthrough.

### 7.3 The fixed-budget slice deserves more discussion if it is statistically primary

The cone theorem varies exposures freely without fixing their sum. The paper correctly adds the nonlinear budget equation when total exposure is fixed.

But the fixed-budget section is the statistically more conventional design object. If the intended statistical significance is substantial, the geometry of that section should not be left as a single equation followed by a disclaimer that the unconstrained secant theorem is no longer asserted.

Either the paper should develop the fixed-budget geometry, or it should state plainly that the cone theorem is an unnormalized exposure geometry chosen because it exposes the structural algebra.

## 8. Total positivity gives useful visibility theorems, but the novelty map is inadequate

The one-colour visibility theorem is an attractive application of the Hankel/Cauchy representation.

The manuscript derives strict total positivity by Cauchy determinants, Cauchy-Binet, and Jacobi complementary minors, then converts the sign pattern into positive-kernel conditions for endpoint visibility. The k = 2, e = 2 missing-empty case is especially useful because it lands exactly in the newly classified three-cell fibre.

I do not object to using classical total positivity here.

I do object to the current literature positioning.

The article now spans:

- finite moment cones;
- Hankel matrices;
- Cauchy systems;
- total positivity;
- optimal experimental design;
- efficient information under nuisance profiling;
- exact recovery of quadratic forms;
- parametric quadratic programming and complementarity fans;
- inverse representation of piecewise-quadratic value functions;
- latent/binary polynomial identifiability.

Four new references do not establish priority across this landscape.

A general top-four referee must be able to tell, theorem by theorem:

1. which matrix/moment statement is classical;
2. which inverse-QP statement is known in another language;
3. which total-positivity implication is standard;
4. which information-geometry identity is routine;
5. which exact part is new because of the polynomial binary observation mechanism;
6. which endpoint-fibre result has no close predecessor.

The current “Relation to earlier work” subsection is an improvement, but it remains a compressed list of broad areas rather than a priority analysis.

This alone would prevent me from recommending acceptance at a top-four journal.

## 9. The compatibility theorem is natural, but it does not yet unify the difficult parts of the paper

Theorem 7.1 is a useful response to the previous criticism that the stochastic model had been reverse-engineered from a desired quotient.

The calibrated binary family is defined first. The same model then gives:

- a finite labelled-root quotient;
- an affine leading observation residual in symmetric coordinates;
- an efficient information matrix with Hankel inverse;
- an endpoint profile G_Q.

This is genuinely better than universal realization by designed contrasts.

However, the theorem does **not** yet provide the deep unification suggested by the overall narrative.

The reason is important.

After passing to cluster sums, variances, endpoint shifts, and mixing, the clock observation map has an invertible derivative V and is a local analytic diffeomorphism. The 2^k labelled root branches correspond only to exchanging the two roots in each repeated cluster, and the manuscript itself observes that all these labelled root sheets produce the **same observation sheet**.

Thus the compatibility theorem connects the native-information and endpoint theories to the easiest affine residual regime: one observed affine sheet in regular symmetric coordinates.

It does not connect them to the genuinely difficult finite-map phenomena of the first part:

- competing distinct observed sheets;
- unequal ramification scales;
- branch collisions affecting the minimizing residual;
- the critical cM approximately one nonlinear transition.

This is the central conceptual reason I am not ready to call the paper a unified structural theory.

A genuinely decisive theorem would exhibit a natural observation class in which:

1. the original singular map has several distinct competing intrinsic leading residual sheets, or a classified nonlinear critical residual;
2. the same model forces a nontrivial native information geometry;
3. endpoint profiling has a reconstructible or classified degeneration; and
4. these structures are related by a theorem, not merely present in separate coordinate layers.

The current binary compatibility theorem is a meaningful first step toward this. It is not yet that theorem.

## 10. The article now needs theorem-level novelty statements, not program-level rhetoric

The current manuscript contains several results that may well be publishable independently:

- residual-scale finite-map reduction;
- divisorial certificate for the derivative regime;
- first visibility-loss fibre classifications;
- binary-model forcing of a Hankel inverse-information cone;
- total-positivity visibility consequences.

The danger is that the paper asks the reader to accept their union as the primary novelty.

For a general top-four journal, breadth does not replace a single clearly identifiable conceptual advance.

The authors should decide which of the following is the actual central theorem.

### Option A: intrinsic singular-geometric classification

Then the finite-map/divisorial part must be promoted to a theorem that is less dependent on the marked presentation and that treats a meaningful critical boundary class.

### Option B: inverse endpoint representation theory

Then the paper should build a substantially more general stratified classification beyond one missing cell and the complete two-endpoint case, and connect it to existing inverse-QP/complementarity literature.

### Option C: model-forced information geometry

Then the Hankel theorem should become the centre of the paper, with a deep priority analysis, fixed-budget consequences, and the endpoint/finite-map pieces reorganized as applications.

At present the manuscript tries to be all three papers at once. That is intellectually ambitious, but it weakens the top-level theorem.

## 11. Proof presentation and audit requirements

I list the following proof-level requirements independently of the larger significance question.

### 11.1 Residual/divisorial part

Provide a standalone simultaneous-resolution proposition specifying:

- the compact graph being resolved;
- the analytic coordinate functions after uniformization;
- the precise product subjected to normal crossings;
- what happens on components where P or N_2 vanishes identically;
- why every chart face used in a necessary inequality is positively accessible;
- how the chartwise bounds reproduce the supremum over the entire original tube;
- exactly which conclusions are invariant under refinement and which still depend on the marked F.

### 11.2 Endpoint part

Provide a planar KKT-fan lemma that fully proves the chain/fork trichotomy and the exhaustion of the one-parameter fibres in Theorem 4.3.

For Theorem 4.1, separate the missing-singleton, missing-full, and missing-empty reconstructions into lemmas. The current proof is clever but dense.

### 11.3 Hankel part

Separate the rational interpolation inverse into a lemma with explicit dimensions and signs. Then state the moment-cone theorem as a consequence.

The manuscript should also state clearly which conclusions survive when the number of clocks exceeds the minimal square count, because the current exact classification is tied closely to m = 2k + e + 1.

### 11.4 Compatibility part

State explicitly that the local observation map is nonsingular in the symmetric coordinates and that the root-label multiplicity is observationally quotiented out at leading order. This is mathematically fine, but it matters for the strength of the claimed unification.

### 11.5 Dependency map

The paper now imports large v104 sections verbatim and inserts v106 sections between them. A top-four reader should not have to reconstruct which theorem depends on which inherited result.

Add a one-page theorem dependency map identifying:

- inherited v104 results used unchanged;
- genuinely new v106 results;
- which new theorem depends on which inherited theorem;
- which statements are logical consequences and which are independent companion results.

## 12. Reproducibility and source state

The v106 source line is a genuine mathematical source revision, which resolves the provenance problem identified in v105.

However, I did not find in the v106 mathematical delta a new source-bound archival receipt establishing a successful native build/replay for the pinned v106 source. The pinned commit also does not provide a status record that I can use as independent mathematical validation.

This is secondary. A successful CI run cannot prove the universal theorems.

But because this repository has repeatedly used exact symbolic checks, generated artefacts, and native build receipts as part of its review history, the next revision should keep the evidentiary hierarchy explicit:

1. manuscript proof;
2. independently checkable finite algebra examples;
3. source-bound build/replay receipt;
4. never the reverse.

Do not describe finite tests as theorem verification.

## 13. Required next revision

If the manuscript is to be reconsidered at the same general top-four level, I would require the following.

### R106.1 — Choose and prove the central structural theorem

The paper needs one theorem that makes the union of its three subjects inevitable.

My preferred route is a natural singular observation class in which a genuinely nontrivial finite-sheet or critical residual geometry, the native information geometry, and the endpoint profile are all simultaneously forced and related.

A regular symmetric-coordinate model whose root permutations collapse to one observed sheet is not enough to close this request.

### R106.2 — Separate intrinsic objects from marked-presentation certificates everywhere

The abstract, introduction, theorem statements, and conclusion should consistently distinguish:

- invariants of the feasible residual germ;
- invariants of a labelled endpoint value function;
- invariants of a labelled statistical experiment;
- quantities attached to a marked fast map F and its tube.

If the divisorial exponents are only certificate data for a marked presentation, say so every time they are used as classification data.

### R106.3 — Either prove a genuine stability theorem or remove the implication of one

A stability theorem should handle parameter variation before fixing the resolution/order vectors, for example through a finite simultaneous stratification.

Otherwise restrict the claim to “persistence within a fixed resolution/order type”.

### R106.4 — Strengthen the critical-boundary theory

Go beyond one nonlinear example at cM approximately one.

A satisfactory result would classify a broad family of critical normalized residuals, or at minimum give a normal-form theorem with explicit hypotheses and show how the nonlinear residual depends on the resolved leading jets.

### R106.5 — Complete the proof architecture of the endpoint first-stratum results

Add the planar KKT-fan classification and separate reconstruction lemmas described above.

The result is important enough to deserve a proof whose exhaustiveness is transparent.

### R106.6 — Reframe and deepen the Hankel novelty claim

Provide theorem-by-theorem comparison with the closest literature on:

- finite/truncated moment spaces and Hankel cones;
- Cauchy and totally positive systems;
- optimal design and information matrices;
- nuisance elimination and efficient information;
- exact quadratic-form recovery;
- latent/algebraic identifiability.

The manuscript must identify exactly what is new in passing from the binary polynomial observation to the inverse-information cone.

### R106.7 — Develop or explicitly demote the fixed-budget design geometry

If statistical design is a major advertised application, analyze the fixed-total-exposure slice beyond writing its defining equation.

If not, make clear that the free-exposure cone is used as an algebraic classification device.

### R106.8 — Add a theorem dependency and provenance table

Pin every principal theorem to its source part, identify inherited versus new content, and state the exact source commit in the manuscript/revision record.

### R106.9 — Produce source-bound build/replay evidence for the v106 source

This is not a substitute for review. It is simply the remaining archival closure item.

## 14. Minor and expository comments

1. The phrase “intrinsic” is overloaded. The new categories section helps, but the title and introduction still use the word across different equivalence categories.
2. The sentence after the divisorial theorem calling the admissible exponent region “relatively open” should be stated with the exact ambient face/stratum, because several displayed inequalities are weak inequalities.
3. The manuscript should distinguish “finite moment cone at fixed clocks” from broader truncated moment cones; the former is polyhedral in the weights even though its span is the Hankel subspace.
4. The total-positivity argument is elegant enough that the exact sign convention for the diagonal conjugation should be fixed once and reused rather than reintroduced verbally.
5. “Exact query complexity” should always carry “deterministic noiseless value oracle” nearby. The paper mostly does this already.
6. The e = 2 fibre theorem should explicitly discuss the case where the admissible scalar interval degenerates to a point. The stated dimension-three conclusion is correctly restricted to the interior of a nontrivial interval, but the boundary geometry deserves one sentence.
7. The local compatibility theorem should state the Hellinger convention by direct reference to the inherited experiment section so that the factor 4 is self-contained.
8. The use of language-model assistance is disclosed. That is appropriate. The disclosure should remain separated from mathematical validation claims.

## 15. Final assessment

Revision 106 is the first version in this line that I would describe as a serious candidate for a high-level research article rather than primarily a programmatic assembly.

The following achievements are real:

- the radius-scale derivative gap is sharpened to the residual scale;
- the derivative certificate is reduced to finite proper-real divisorial tests;
- a true nonlinear residual boundary example is exhibited;
- the first visibility-loss strata are analyzed nontrivially;
- a scalar fibre modulus is discovered in the two-endpoint three-cell case;
- a natural calibrated binary model forces an inverse-information Hankel geometry;
- total positivity connects that geometry to endpoint visibility;
- the previously compressed topological and competitor arguments are expanded.

Those advances materially improve the paper.

Nevertheless, at the standard of a general top-four mathematics journal, I still see three independent blockers:

1. **Conceptual closure:** the three main theories are compatible in one natural model, but the compatibility theorem does not yet couple their genuinely difficult regimes.
2. **Intrinsic scope:** the divisorial theorem is exact for a marked finite-map certificate but is not yet a presentation-independent classification of singular observation germs or their critical nonlinear boundaries.
3. **Priority and positioning:** the literature analysis is not remotely commensurate with the breadth of the mathematics now being claimed.

I therefore would not recommend acceptance, and I would not recommend a routine “minor/major revision” decision at a top-four venue. The next version would need to sharpen the paper around one decisive structural theorem and document its novelty at theorem level.

**Disposition: reject in the present form, with a materially more positive mathematical assessment than v105.**
