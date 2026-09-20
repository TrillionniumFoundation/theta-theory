# Independent harsh referee report on A2 revision 103

**Manuscript:** *Finite-sheet metric contact and spectral quotients of polynomial observations*  
**Reviewed revision branch:** revision/a2-v103-finite-sheet-metric-quotients-2026-09-20  
**Reviewed revision head:** 3e52776024376f6034ab54d0466cdb648f4e221d  
**Principal mathematical source commit:** b50fbbe0ce30856bd1b10cd66ab70351fd8f4295  
**Native-build trigger source commit:** 618b0b098654f53e61a782138272349df92d16ad  
**Principal article source:** papers/A2-v17-boundary-information-coarsening/article/v103/paper.tex  
**Controlling prior report:** reviews/a2-v102-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md  
**Controlling prior review commit:** 8054ae5d5c318b7e59f9ad42545ae27b416bec09  
**Independent review branch:** review/a2-v103-independent-harsh-top4-2026-09-20  
**Date:** 2026-09-20

## 1. Recommendation

**Recommendation for an Annals / Acta / Inventiones / JAMS-level general mathematics journal: reject in the present form.**

This is **not a correctness rejection**.

Revision 103 is materially stronger than revision 102. It does not merely rename the previous objects or add repository infrastructure. It proves several genuinely substantive statements that answer important parts of the preceding report:

1. an exact semidefinite lift and exposed-face formula for finite affine leading-residual sheets, together with realization and product operations;
2. a multivariable, multi-sheet, vector-valued cancellation theorem with a relative estimate through exact cancellation;
3. a rational-moment description of the native fixed-Hellinger quotient family;
4. a sharp three-query theorem on a genuinely native two-variance family with clocks and weights fixed;
5. an all-dimensional finite equality test and range representation for endpoint elimination;
6. a complete fibre classification when there is one invisible endpoint;
7. a much better organized whole-model local limit proof; and
8. a more explicit real-analytic presentation theorem and literature comparison.

I found no direct counterexample to the principal v103 theorems.

The reason for rejection is therefore narrower and more demanding than in v102. The paper now contains enough real mathematics that the question is no longer whether there is a theorem. The question is whether the principal theorems, taken together, constitute a conceptual advance of the breadth, depth, and inevitability expected at the stated general-journal level.

My conclusion is still no.

The central difficulty is that the paper has produced several strong **class-specific** structure theorems, but has not yet proved the theorem that makes those classes intrinsic or unavoidable for the underlying observation problem. The finite-sheet theorem is exact once affine sheets are present; the cancellation theorem produces such sheets once a fast-coordinate normal form is assumed; the native query theorem is sharp for one two-variance chart; and the endpoint quotient is completely classified only for one invisible endpoint. These are meaningful advances, but the paper still stops one level before a general structural classification.

A second, independent issue remains unresolved: the source-bound full archival native run recorded by the revision, GitHub Actions run 35504308437, is still queued with no conclusion and no durable RUNTIME_RECEIPT.json on the reviewed branch. The authors themselves correctly do not claim R102.8 closed. I agree with that boundary.

## 2. Scope of this report

I reviewed the following v103 materials directly:

- A2_REVISION_V103_INDEX.md;
- papers/A2-v17-boundary-information-coarsening/article/v103/paper.tex;
- revisions/a2-v103/RESPONSE_TO_REFEREE.md;
- revisions/a2-v103/CONTENT_PRESERVATION.md;
- revisions/a2-v103/EXACT_DIAGNOSTICS.json;
- revisions/a2-v103/LOCAL_VALIDATION.json;
- revisions/a2-v103/SOURCE_MANIFEST.json;
- scripts/check_a2_v103.py;
- scripts/build_a2_v103.py;
- the v103 workflow definition;
- the controlling v102 referee report;
- the current state of pull request #58; and
- the current state of native run 35504308437.

I also checked that the reviewed branch head is one documentation/evidence commit beyond the native-build trigger and that this extra commit adds only the v103 index, response, preservation map, diagnostics, validation, and source manifest. It does not alter the mathematical/build source bound to the native trigger.

The standard applied here is deliberately severe. A technically correct specialized theorem, or even a collection of several technically correct specialized theorems, is not by itself enough for the journal class under discussion. The principal question is whether the work reveals a general mechanism that changes how one understands the singular inverse geometry, rather than providing an exact toolkit for several important normal forms.

## 3. Executive assessment

Revision 103 has a much stronger mathematical spine than revision 102.

The new chain is roughly:

1. finite affine residual sheets have an exact spectrahedral moment lift;
2. positive-definite metrics expose the tensors of the minimizing sheets;
3. a small-shear theorem reduces a multivariable fast system to exact vector residuals on finitely many inverse sheets;
4. weighted polynomial systems realize that structure on semialgebraic opening arcs;
5. binary stochastic polynomial observations yield a local quotient form under the native Hellinger metric;
6. the native quotient family has finite rational-moment dimension;
7. exact ray information can be bounded in terms of that dimension, and one native two-variance family attains the full three-dimensional Sym_2 geometry;
8. invisible endpoint coordinates induce a parametric-QP quotient with a finite equality test and a complete one-endpoint classification.

This is coherent and considerably better than v102.

The difficulty is that the strongest conclusions still live at different levels of generality.

- The finite-sheet theorem is general **inside the affine-sheet category**, but the paper does not characterize when a natural singular observation germ belongs to that category.
- The cancellation theorem is multivariable and vector-valued, but it assumes the decisive fast-coordinate form x_i^{m_i}-t eta_i from the outset.
- The native information theorem is sharp in a concrete d=2 chart, but the general higher-pattern native secant geometry is left open.
- The endpoint equality theorem is all-dimensional, but the full equivalence-class/minimal-representation theorem stops at endpoint dimension one.
- The real monomial presentation computes classical order data, but it is not yet connected to a theorem extracting the finite affine sheets or native quotient geometry from a general resolved singularity.

Thus the revision has successfully answered many local objections while exposing the remaining global one:

> the paper still lacks a theorem showing that its several exact normal forms are manifestations of one intrinsic structure in a broad natural class.

For a specialized journal, the present collection could be substantial. For a top-four general mathematics journal, I would expect that missing theorem.

## 4. What revision 103 genuinely fixes

A harsh report should state clearly where the authors succeeded.

### 4.1 R102.1: the metric envelope now has genuine finite structure in a nontrivial class

Theorem 2.2 is a real strengthening over the v102 support-function packaging.

For a finite union of affine sheets, it gives the exact representation

C(E) = { sum_b A_b M_b A_b^T + P :
         M_b >= 0, P >= 0, sum_b (M_b)_{last,last} = 1 }.

The proof does more than invoke separation. It identifies the moment cone of each affine sheet, handles zero-weight covariance contributions, proves closedness using full column rank of [L_b,c_b], and identifies the positive-metric exposed face exactly as the convex hull of the minimizing projected residual tensors.

The realization theorem and product closure are also useful.

This substantially answers the previous request to prove structure beyond the bare convex-duality reconstruction.

### 4.2 R102.2: the paper now has a truly native sharp query theorem

This is one of the strongest improvements in v103.

Theorem 5.3 fixes the Hellinger metric, clocks, weights, second channel, and root locations, and varies only three stochastic centre parameters. The exact first-jet computation gives a nonzero 3-by-3 Jacobian over Q, certified by the nonzero residue 933885 modulo 1000003. Hence the native quotient image contains an open subset of Sym_2^{++}.

This matters because the v102 lower bound was for an artificially enlarged class of all positive-definite forms. The v103 theorem places an open three-dimensional family inside the native probability geometry itself.

The exact adaptive lower bound of three ray queries then follows from a valid local adversary inside that open native image, and the three polarization rays attain it.

I regard this as a genuine answer to the strongest part of R102.2 for at least one nontrivial native pattern.

### 4.3 R102.3: endpoint elimination is now more than “piecewise quadratic”

Theorem 6.1 gives an all-dimensional finite equality criterion by comparing Schur matrices on full-dimensional intersections of active cones. It also gives a geometric range representation by distance to a simplicial cone.

Theorem 6.2 then completely classifies the one-endpoint fibres, including:

- the nonquadratic mixed-sign case;
- recovery of the oriented rank-one direction;
- the positive endpoint-rescaling ambiguity;
- fibre dimensions;
- minimal endpoint dimension; and
- a canonical representative.

That is materially beyond the classical statement that a parametric quadratic-program value function is piecewise quadratic.

### 4.4 R102.4: the cancellation theorem is no longer scalar

Theorems 3.1 and 3.2 are a serious generalization.

There may be several fast equations, a vector-valued slow residual, and finitely many inverse sheets. The relative estimate is with respect to the exact vector C_b(t), not merely a generic leading monomial, so exact cancellation is retained.

Corollary 3.3 identifies the complete leading residual set on a nonexact opening arc and links it to the finite-sheet envelope.

Theorem 3.6 embeds the class into strictly positive probability observations.

This is a real answer to the request for a multivariable/multi-branch extension.

### 4.5 R102.5: the paper now distinguishes classical ingredients from added conclusions

The introduction explicitly separates:

- convex separation/moment/Schur tools;
- parametric quadratic-program structure;
- classical contact-order and valuation theory; and
- the additional finite-sheet, vector-cancellation, native-family, and endpoint-classification conclusions.

The bibliography is still short for a work with this breadth, but it is no longer defensible to say that the principal article completely ignores the relevant classical mechanisms.

I also checked the 2003 corrigendum to the cited Bemporad–Morari–Dua–Pistikopoulos paper. The published correction concerns Example 7.1, not the general piecewise-affine structural statement on which v103 relies. Thus I do not see a substantive citation problem there, although adding the corrigendum to the bibliography would be good practice.

### 4.6 R102.6: the real presentation is now stated as an actual theorem

Theorem A.1 no longer treats the desired real monomial presentation as an unexplained black box.

It invokes proper real-analytic uniformization, normal crossings for the product t sum_i R_i^2, uses noncancellation of real squares to extract a common residual monomial, and explicitly discusses positive-time accessibility and feasibility.

This is a substantial improvement.

### 4.7 R102.7: the whole-model local proof is better organized

The coefficient inverse, cluster estimates/realization, and Hausdorff limit are now separated into Lemma 4.1, Lemma 4.2, and Theorem 4.3.

The two Hausdorff inclusions and radial contractions are stated explicitly.

This is much closer to an independently reviewable proof.

### 4.8 R102.8: the authors correctly leave the runtime evidence open

The response explicitly says the full graph has not been executed locally and that the queued remote workflow is not a successful receipt.

That evidentiary honesty is correct.

It does not close R102.8, but it avoids a false closure claim.

## 5. Main objection I: the finite-sheet theory is exact, but the paper does not yet prove that finite affine sheets are the intrinsic singularity class

Theorem 2.2 is good mathematics.

It is not, by itself, the top-four conceptual jump.

### 5.1 The realization theorem is permissive rather than classificatory

Every finite affine-sheet arrangement is realized by taking disjoint feasible balls, assigning each sheet a residual L_b x + c_b t^p, embedding the balls with tags, and interpolating in the tag.

This proves realizability.

But the construction is deliberately flexible. It does not show that affine leading sheets arise naturally or canonically from a broad class of singular inverse problems.

In other words, the theorem establishes:

> every prescribed finite affine arrangement can be encoded by some polynomial residual problem.

The more important reverse direction would be:

> a broad natural class of polynomial or stochastic observation singularities necessarily has, after an intrinsic reduction, a finite affine leading-sheet arrangement of the kind classified here.

That reverse theorem is missing.

### 5.2 The paper does not classify the minimal or intrinsic lift

The spectrahedral lift in Theorem 2.2 need not be minimal or unique; the paper says so.

For top-four depth, one would like to know, for example:

- which features of the lift are intrinsic;
- the minimal number and dimensions of affine sheets compatible with the envelope;
- whether exposed-face adjacency reconstructs the sheet incidence;
- when different sheet arrangements have the same envelope;
- whether there is an intrinsic stratification of metric space by branch competition;
- how the lift changes under perturbation of the original singular germ;
- whether the envelope determines or refines a standard singularity invariant.

At present the finite-sheet theorem gives an exact computation once the sheet arrangement is already supplied.

### 5.3 Corollary 3.3 links one normal form to the sheet theorem, but not general singularities to that normal form

This is the central structural gap.

The weighted system of Theorem 3.2 is important, but its fast coordinates are explicitly prescribed as

x_i^{m_i} - t eta_i.

The theorem then shows that the slow polynomial G becomes a small shear in those charts.

What is not proved is that a generic or suitably resolved polynomial observation singularity admits such a fast-coordinate description with finitely many real inverse sheets and the required uniform localization.

Appendix A monomializes order data, but it does not derive Theorem 3.2's finite affine-sheet geometry from the resolved charts.

A theorem connecting Appendix A to Sections 2–3 would greatly strengthen the paper.

## 6. Main objection II: the native three-query theorem is a real advance, but the general information theory remains pattern-specific and oracle-dependent

Revision 103 resolves a major weakness of v102, but it does not fully resolve the significance problem.

### 6.1 The d=2 result is sharp because the native image is locally all of Sym_2

The first-jet rank witness is exactly the right way to prove the local open-image statement.

Once the image contains an open subset of Sym_2^{++}, the three-query lower bound is essentially forced.

That is a genuine native theorem.

But the decisive geometry is still established by one concrete rank certificate at one rational centre.

The genericity sentence follows because the relevant rational minor is not identically zero. That is legitimate, but it does not classify the native quotient image for other patterns.

### 6.2 The general 2s+1 upper bound is a semialgebraic incidence theorem, not a model classification

Theorem 5.2 is correct-looking and useful.

However, after the native family dimension s has been supplied, the bound

q_fixed <= 2s+1

comes from a general dimension estimate on normalized secants and rank-one quadratic measurements.

The hard model-specific problem is therefore pushed into the value and geometry of s and of the secant set.

For higher-degree and mixed boundary/multiplicity patterns, the paper does not determine:

- the exact native dimension;
- the exact secant dimension;
- the sharp fixed-ray complexity;
- the sharp adaptive complexity;
- whether the generic 2s+1 count is attained or improvable;
- whether special algebraic relations force fewer queries;
- how these quantities change at pattern boundaries.

The d=2 theorem proves that the native family can be full dimensional. It does not yet give a general native measurement theory.

### 6.3 The ray oracle is still not an observational sample-complexity object

The manuscript is admirably explicit about this.

The unknown member is supplied only through exact variational ray costs. If the numerical centre law and design parameters are instead supplied, Lemma 4.1 and the Schur formula compute Q directly, so the ray-query count is not an observation count.

Thus Theorem 5.3 is a theorem about the information content of a chosen exact oracle.

That is mathematically valid.

For the claimed journal level, however, the paper should explain why this oracle is a canonical quotient of the original observation problem rather than a deliberately restricted interface imposed after exact model identification.

A stronger result would connect these exact queries to an intrinsic decision problem, statistical experiment, or unavoidable reconstruction interface.

### 6.4 The exact certificate proves nonvanishing, not the surrounding universal theorems

The finite-field calculation is clean and appropriately scoped.

It establishes a particular Jacobian rank.

It does not verify Theorems 2.2, 3.1, 4.3, 5.2, 6.1, or A.1.

The authors already say this. The paper should continue to resist any temptation to treat the certificate count as a proxy for proof depth.

## 7. Main objection III: endpoint equality is all-dimensional, but the full quotient classification stops at one invisible endpoint

Section 6 is substantially improved.

It also makes the next missing theorem very clear.

### 7.1 Theorem 6.1 gives a decision criterion, not a global fibre classification

Given Q and Q', one can compare the Schur matrices on active-cone intersections.

That is useful and exact.

The canonical locally quadratic data also determine G_Q.

But this does not classify the set of all Q producing the same G.

For endpoint dimension e >= 2, the paper does not determine:

- the dimension of a generic fibre;
- the continuous gauge group, if any;
- discrete ambiguities;
- minimal endpoint dimension;
- canonical representatives;
- when two different simplicial cones and maps T yield the same distance function on the positive orthant;
- the relation between nonminimal representations and redundant endpoint coordinates.

These questions are not cosmetic. They are the natural higher-dimensional content of the quotient Q -> G_Q.

### 7.2 The one-endpoint theorem is elegant precisely because it exposes what is missing in higher endpoint dimension

For e=1, the formula

G_Q(x) = x^T A x - min{u^T x,0}^2

reduces the quotient to one oriented rank-one hinge.

The mixed-sign case is then completely identifiable up to positive endpoint scaling.

For e>=2, interactions between multiple active faces, cone automorphisms, and overlapping Schur reductions are much richer.

A top-four endpoint theorem would, in my view, need to enter that regime.

### 7.3 The range representation is attractive but not yet a uniqueness theorem

The representation

G(x) = x^T S x + dist(Tx, L R_+^e)^2

is geometrically clean.

But many triples (S,T,L) may represent the same function.

The paper gives existence and a matrix construction, not a classification of those representations.

That remaining nonuniqueness is exactly the structural problem.

## 8. Main objection IV: the multivariable cancellation theorem assumes the decisive normal form rather than deriving it

Theorem 3.1 is one of the strongest technical results in the paper.

Its limitation should be stated just as clearly.

### 8.1 The small-shear theorem is abstract but conditional

If the residual is already represented in finitely many charts as

(U, C_b(t) + B_b(U,t)U)

with B_b -> 0, if C_b=o(r_t), and if all global minimizers localize to these charts, then the Schur-norm conclusion is natural and clean.

The hard geometric work in a general singular inverse problem is often precisely to prove those hypotheses.

### 8.2 The weighted polynomial theorem verifies the hypotheses for an explicit fast system

That is valuable.

But the class is still built from exact equations x_i^{m_i}=t eta_i.

The multivariable theorem does not cover, for example, a general coupled fast system with a nontrivial discriminant, ramified branches that cannot be separated by independent monomial equations, or singular branch collisions in which the chart radii and inverse derivatives degenerate at different rates.

These are the situations where a genuinely new normal-form theorem would have the most force.

### 8.3 Positive-probability realization is one direction only

Theorem 3.6 shows that this fast-coordinate geometry can occur in a stochastic observation model.

It does not prove that natural singular stochastic polynomial models reduce to it.

Again the missing direction is a structural converse or reduction theorem.

### 8.4 The paper should connect the real resolution appendix to the fast-sheet theorem

Appendix A supplies proper real analytic charts and monomial order data.

Sections 2–3 classify finite affine residual sheets.

The obvious top-level question is:

> under what hypotheses does the resolved residual, after choosing the correct weighted scale, actually produce finitely many affine leading sheets with a uniform small-shear estimate?

A theorem answering that would unify the manuscript.

Without it, the resolution appendix and the finite-sheet/cancellation theory remain adjacent rather than logically fused.

## 9. Main objection V: the manuscript is mathematically dense but conceptually overassembled

The 18-page principal is admirably concise.

It may now be too concise in a different sense.

The manuscript combines:

- convex tensor envelopes;
- spectrahedral moment representations;
- singular fast-slow normal forms;
- Hellinger information geometry;
- local polynomial inverse theory;
- semialgebraic incidence bounds for oracle queries;
- parametric quadratic-program quotients; and
- real-analytic uniformization/normal crossings.

Every piece has a role.

But a top-four paper usually needs the reader to feel that these pieces are forced by one central theorem, not merely compatible modules in a research program.

Revision 103 is close to such a story but has not reached it.

The paper's strongest possible thesis would be something like:

> singular polynomial observation germs admit an intrinsic finite metric quotient whose local pieces are affine-sheet envelopes, whose stochastic localizations are native Hellinger forms, and whose invisible directions are classified by a canonical cone quotient.

The current theorems do not yet establish that statement.

Instead they prove each component in a different class.

That is why the manuscript still reads more like an unusually strong programmatic synthesis than a single inevitable general theorem.

## 10. Correctness audit of the principal v103 statements

I record my current mathematical assessment separately from significance.

### 10.1 Proposition 2.1

I found no direct flaw.

Semialgebraic minimization gives a rational leading exponent; norm equivalence preserves it across positive-definite metrics; normalized minimizers give the leading residual set; and closed convex separation reconstructs the upper tensor envelope.

This is plausible and standard in mechanism.

### 10.2 Theorem 2.2

The moment identity for an affine sheet is correct-looking.

The assumption c_b not in ran L_b together with full column rank of L_b makes A_b=[L_b,c_b] full column rank, which justifies the trace bound used for closedness.

The exposed-face argument is also sound-looking.

The realization theorem is permissive, as discussed above, but I see no contradiction in it.

### 10.3 Corollary 2.3

Synchronizing the two semialgebraic arcs by the same positive time is plausible because each time coordinate is eventually monotone on a punctured interval.

No direct objection.

### 10.4 Theorems 3.1 and 3.2

The small-shear argument is clean.

The trial U=0 localizes minimizers, the unsheared minimum is exactly the Schur norm, and the quadratic minimizing U is feasible because C_b=o(r_t).

The weighted polynomial derivative estimate t^{nu-1} is also consistent.

No direct correctness objection.

### 10.5 Corollary 3.3

The leading residual set formula is plausible once the branch residuals are semialgebraic and the largest contact exponent is selected.

The paper correctly treats a parameter path as part of one fixed residual germ.

### 10.6 Theorem 3.6

The Hellinger expansion around a uniformly positive P_0 gives the displayed native quadratic metric.

The relative-error transfer appears sound.

### 10.7 Lemma 4.1: one wording/proof defect should be corrected

The sentence

“Two clocks i,j have distinct ratios f_a(T_j)/f_a(T_i). Otherwise f_1-cf_2 would vanish at more than d clocks ...”

is too strong as written.

The argument proves that the ratio f_1(T)/f_2(T) cannot be the same at **all** clocks, because that would give more than d zeros of f_1-cf_2. It therefore proves the existence of a pair of clocks with distinct component ratios, which is enough for the generalized-eigenvector recovery.

It does not prove that an arbitrary pair i,j has distinct ratios.

This appears to be a local wording/quantifier defect rather than a failure of the inverse theorem, but it should be fixed explicitly.

### 10.8 Lemma 4.2 and Theorem 4.3

The cluster coefficient estimates, repeated-root square-root scale, endpoint linear scale, feasible realization, and Schur quotient are all plausible.

The two Hausdorff inclusions are now sufficiently explicit that I do not see the previous structural gap.

I would still prefer the score-injectivity argument to display the exact partial-fraction basis and its correspondence with every retained/free column, but I did not find a counterexample.

### 10.9 Theorem 5.1

The denominator-degree count and rational-moment representation are plausible.

The use of Caratheodory is correct for preservation of the information matrix, and the manuscript correctly says this need not preserve global identification by the compressed clock set.

The derivative formula for Q is the standard profiled-information cancellation.

No direct objection.

### 10.10 Theorem 5.2

The generic fixed-query upper bound follows from the dimension of the normalized secant set and the codimension-one zero set of a nonzero quadratic polynomial on an open ray cone.

The adaptive lower bound using semialgebraic fibres is also correct-looking as a deterministic exact-query adversary.

The limitation is interpretation and model specificity, not evident correctness.

### 10.11 Theorem 5.3

The exact modular certificate is sufficient to prove the rational Jacobian determinant is nonzero, provided all reduced denominators are units; the checker explicitly tests this.

The inverse function theorem then gives an open native image.

The adaptive three-query lower bound inside that open image is sound.

I regard this theorem as one of the strongest parts of v103.

### 10.12 Proposition 5.4

The least-squares perturbation bound and radial sandwich follow from operator-norm control relative to Q >= lambda I.

No direct objection.

### 10.13 Theorem 6.1

The active-cone equality test is plausible.

Equality of quadratic polynomials on a full-dimensional open intersection forces equality of their matrices, and the full-dimensional cells are dense after removing lower-dimensional boundaries.

The distance-to-simplicial-cone representation follows by completing the square.

No direct objection.

### 10.14 Theorem 6.2

The scalar endpoint minimization formula is correct.

In the mixed-sign case the two quadratic regions meet the positive orthant, the rank-one difference determines u up to sign, and the active halfspace fixes orientation.

The stated scaling ambiguity in c is correct-looking.

No direct objection.

### 10.15 Theorem A.1

The theorem is plausible but deserves a more formal local-algebra lemma.

From normal crossings of t times sum_i R_i^2, the proof concludes that t and the sum of squares separately are coordinate monomials times units. In a regular local analytic ring this is natural because the coordinate parameters are prime and the zero divisor of each factor must be supported on those parameters.

For a paper at this level, I would state this as an explicit lemma or cite the exact local-factorization result rather than compressing it into “successively dividing by each prime coordinate.”

Likewise, the passage from the proper uniformization source to the retained positive-time components and the transverse accessibility of every divisor face used in a ratio should be isolated as a precise compactness/accessibility lemma.

I do not currently claim this is false. I claim the proof is still too compressed at exactly the place where real feasibility distinguishes the paper from a purely complex or formal resolution argument.

## 11. Reproducibility and source-provenance audit

The repository discipline in v103 is good.

The final runtime closure is not.

### 11.1 Local principal validation is positive evidence

LOCAL_VALIDATION.json records:

- successful native compilation of the principal;
- 18 pages;
- no undefined citations or references;
- no multiply defined labels;
- no overfull or underfull boxes;
- no LaTeX warnings;
- source blob readback match;
- principal/wrapper rendered parity; and
- exact finite diagnostics passed.

I accept this as useful evidence for the principal source.

### 11.2 The exact diagnostic record is internally consistent in scope

EXACT_DIAGNOSTICS.json records, among other checks:

- det(I_LL) = 743349 modulo 1000003;
- the fixed-experiment native Jacobian determinant = 933885 modulo 1000003;
- an independent design minor = 230039 modulo 1000003;
- probability normalization/positivity checks;
- coupled polynomial substitutions;
- endpoint rescaling checks; and
- affine moment/projection checks.

The file explicitly says these are finite certificates and displayed-example checks, not formal verification of universal theorems.

That is the correct claim.

### 11.3 The source-bound trigger is cleanly pinned

SOURCE_MANIFEST.json pins the native trigger to

618b0b098654f53e61a782138272349df92d16ad.

The current revision head

3e52776024376f6034ab54d0466cdb648f4e221d

is one commit later.

The diff from the trigger to the current head adds only documentation/evidence files. It does not modify the mathematical/build source.

Thus the source-provenance story is coherent.

### 11.4 The full archival native graph still has no successful receipt

At the time of this review, GitHub Actions run 35504308437 is still:

- status: queued;
- conclusion: null.

The v103 revision directory contains no native/RUNTIME_RECEIPT.json.

LOCAL_VALIDATION.json says explicitly:

- full_archival_native_status: not_executed_locally;
- success_claimed: false.

Therefore the only defensible conclusion is:

> R102.8 remains open. A full source-bound native success has not been durably demonstrated for v103.

This is not a mathematical counterexample.

It is a reproducibility blocker for any claim that the complete preserved graph has been natively validated.

## 12. Disposition of the v102 requests

| Prior request | v103 disposition | Referee assessment |
|---|---|---|
| R102.1 finite intrinsic structure of the metric envelope | **Substantially answered in the finite affine-sheet class** | Exact lift, exposed faces, realization, and products are real progress. Missing: intrinsic characterization/reduction from broad natural germs. |
| R102.2 finite-probe problem for the actual native family | **Answered sharply for one nontrivial native pattern; broadly bounded in general** | Theorem 5.3 is a genuine native sharp result. Missing: general pattern/secant classification and sharper interpretation of the oracle. |
| R102.3 classify Q -> G_Q | **Substantially answered for equality/range; completely answered only for e=1 fibres** | Strong improvement. Higher-endpoint fibre/minimal-representation theory remains open. |
| R102.4 generalize the wall theorem or prove a normal form | **Answered for an explicit multivariable fast-coordinate class** | Several fast equations, vector residuals, and competing sheets are handled. Missing: a theorem deriving this normal form from a broad natural singular class. |
| R102.5 literature comparison | **Substantially answered** | Classical mechanisms are now acknowledged. Literature remains narrow relative to the breadth of the paper. |
| R102.6 formalize real monomial presentation | **Mostly answered** | Theorem A.1 is a real existence statement. I still want the local factorization/accessibility steps stated as precise lemmas. |
| R102.7 expand whole-model Hausdorff proof | **Answered** | The proof is now split and the two inclusions are explicit. One clock-ratio quantifier sentence must be fixed. |
| R102.8 source-bound native receipt | **Not answered** | Run 35504308437 remains queued; no durable runtime receipt exists. |

## 13. Revisions required before reconsideration at the same journal class

The next revision should not be another layer of examples or certificates.

It needs a conceptual unification.

### R103.1 — Prove an intrinsic reduction theorem into the finite-sheet category

A major result should start from a broad natural class of polynomial/semialgebraic observation singularities and conclude, after an intrinsic or controlled real resolution, that the leading metric problem is represented by finitely many affine sheets with the small-shear structure required by Theorem 3.1.

The theorem should state:

- precise hypotheses on the original observation germ;
- how the finite sheets are extracted;
- invariance under allowed coordinate changes;
- how branch collisions/cancellations are represented;
- uniformity in parameter families; and
- what data are independent of the chosen presentation.

This would connect Appendix A to Sections 2–3 and give the paper a genuine central theorem.

### R103.2 — Determine the native quotient geometry beyond the single d=2 rank witness

For a significant class of fixed patterns, determine:

- the exact dimension of the native Hellinger quotient image;
- the dimension/structure of its secant set;
- sharp fixed and adaptive exact-ray complexities;
- whether the generic 2s+1 upper bound is sharp;
- the loci where rank drops; and
- behaviour under multiplicity/boundary transitions.

The d=2 theorem may serve as the base case, not the endpoint.

### R103.3 — Classify endpoint fibres for e >= 2

Extend the one-endpoint result to a genuinely higher-dimensional quotient theory.

At minimum, determine:

- generic fibre dimension;
- minimal endpoint dimension;
- canonical or normalized representatives;
- cone automorphism/scaling ambiguities;
- criteria for redundancy of endpoint coordinates; and
- invariants of the distance representation x^T S x + dist(Tx,K)^2.

This is the natural next theorem after 6.1–6.2.

### R103.4 — Clarify the canonical role of the ray oracle

The paper should explain why the exact variational ray oracle is mathematically intrinsic to the observation problem.

If the intended claim is purely an oracle-complexity theorem, say so prominently and reduce “information” rhetoric accordingly.

If a stronger observational interpretation is intended, prove a theorem connecting the oracle to an actual statistical/experimental reconstruction problem.

### R103.5 — Make the real-resolution step theorem-proof complete

Add an explicit local-algebra lemma showing how normal crossings of the product imply monomial-times-unit factorizations of the individual real analytic factors used in the proof.

Add a separate accessibility lemma explaining exactly why every divisor face used in the ratio is reached by positive-time feasible arcs after the component/orthant pruning.

This should be stated with quantifiers and not left inside prose.

### R103.6 — Correct the clock-ratio quantifier and perform a proof-level quantifier audit

In Lemma 4.1 replace the universal-sounding pair statement by the exact existential statement actually proved and used.

Then audit similar phrases throughout the principal paper for:

- “all clocks” versus “there exists a pair”;
- “uniform on a fixed pattern” versus cross-pattern claims;
- fixed-design versus fixed-centre families;
- equality of a leading coefficient versus equality of the full finite-time minimizer;
- generic open-dense claims versus uniform claims.

These are small individually but important at this level.

### R103.7 — Complete the native source-bound runtime receipt

Run the exact v103 source-bound job to completion.

If successful, commit:

- RUNTIME_RECEIPT.json;
- all four intended volume PDFs;
- native logs;
- dependency/source hashes; and
- the source head actually compiled.

If the current run remains indefinitely queued, rerun through a functioning runner but preserve the source binding.

Do not mark R102.8 closed until the durable receipt exists.

## 14. Editorial comments

1. The abstract is now accurate about the two-variance sharp query theorem, but it still makes the paper sound more uniform across degrees/patterns than the proofs justify. Distinguish the general moment/dimension bounds from the sharp d=2 theorem in the abstract itself.

2. The phrase “finite-sheet metric contact” is appropriate for Section 2, but the paper should avoid suggesting that every singular contact problem has already been reduced to finite affine sheets.

3. Theorem 2.2's realization is best described as a universal realization inside a permissive semialgebraic feasible category, not as evidence that the arrangement is a natural normal form.

4. Theorem 5.3 should be advertised as an exact native-oracle theorem. It is not a sample-complexity or experimental-design lower bound.

5. The manuscript should explicitly distinguish “fixed experiment, unknown centre parameters to the oracle” from the original inverse setting where an exact centre law identifies those parameters.

6. The BMDP reference should ideally mention the 2003 corrigendum even though the correction concerns Example 7.1 rather than the structural theorem used here.

7. Six principal bibliography entries are still remarkably few for a paper simultaneously invoking real singularity theory, semialgebraic geometry, spectrahedral/moment representations, parametric QP, information geometry, and inverse problems. A top-journal manuscript should give the reader a broader map.

8. The exact modular calculations are useful, but the paper should keep them in Appendix B rather than allow them to dominate the conceptual presentation.

9. Theorem A.1 should not be treated as routine. Real feasibility and positive-time accessibility are precisely the subtle features that deserve a slower proof.

10. The complete historical archive is useful for provenance, but the principal paper should continue to be judged entirely on the 18-page self-contained source.

## 15. Originality and depth assessment

Revision 103 is the first version in this sequence for which I would say that several principal results are independently interesting.

The finite-sheet lift is clean.

The vector cancellation theorem is useful.

The native d=2 query theorem is genuinely model-specific.

The endpoint one-variable fibre classification is elegant.

The real issue is no longer whether there is enough mathematics.

It is whether these results have been lifted to their natural general level.

### 15.1 Finite-sheet geometry

The new theorem turns an arbitrary finite affine arrangement into an exact positive-metric tensor theory.

That is a useful finite model.

The missing top-level theorem is a canonical passage from natural singular germs to this finite model.

### 15.2 Native Hellinger information

The paper now demonstrates a native open quotient family and a sharp exact-query count.

That is a legitimate new result.

The missing top-level theorem is a general classification of native quotient dimension and secants across the model's singularity patterns.

### 15.3 Endpoint quotient geometry

The paper now does more than invoke parametric QP.

The one-endpoint classification is genuinely structural.

The missing top-level theorem is the higher-endpoint equivalence theory.

### 15.4 Cancellation geometry

The small-shear estimate through exact cancellation is technically strong and conceptually clear.

The missing top-level theorem is a broad normal-form result making this geometry unavoidable rather than constructed.

These four missing statements point in the same direction. The paper needs one unifying theorem that turns the current toolkit into an intrinsic theory.

## 16. Final assessment

Revision 103 is a serious mathematical advance over revision 102.

It closes or substantially advances nearly every mathematical request in the controlling report.

In particular:

- the metric envelope now has an exact finite lift in a meaningful class;
- the wall theorem is genuinely multivariable and vector-valued;
- the native Hellinger family has a sharp nontrivial exact-query theorem;
- endpoint elimination receives a real quotient classification in the one-endpoint case;
- the whole-model proof is much more reviewable; and
- the real analytic presentation is no longer left as an undefined assumption.

I found no direct counterexample to the principal theorems.

Nevertheless, for an Annals / Acta / Inventiones / JAMS-level general mathematics journal, I still recommend **rejection in the present form**.

The reason is not that the paper is empty, incorrect, or merely computational.

The reason is that the revision now sits one theorem short of its own natural scale.

It has exact results for:

- finite affine sheets;
- explicit fast-coordinate systems;
- one sharp native d=2 quotient chart; and
- one-endpoint quotient fibres.

What it does not yet prove is the general structural theorem connecting these normal forms to the broad singular polynomial observation problem.

A successful next revision should therefore aim not to add another special pattern, another exact determinant, or another preserved volume, but to prove one of the missing classification/reduction theorems at the general level.

Finally, independently of mathematical significance, the reproducibility item R102.8 is still open: run 35504308437 is queued and no durable v103 full-graph runtime receipt exists.

My disposition is therefore:

**mathematically serious; no direct correctness rejection; major conceptual revision required; not ready for the stated top-four journal class in its present form.**
