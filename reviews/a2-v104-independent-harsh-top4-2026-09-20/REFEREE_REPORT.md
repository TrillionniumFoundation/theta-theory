# Independent harsh referee report on A2 revision 104

**Manuscript:** *Intrinsic finite-sheet reduction and reconstruction of metric quotients*  
**Reviewed revision branch:** `revision/a2-v104-intrinsic-reduction-endpoint-reconstruction-2026-09-20`  
**Reviewed revision head:** `b8c9da734b8ecbadc16ec95c5a8490c7fcf0276a`  
**Principal mathematical/build source commit:** `ff20178a3ac04712ceed5eb333e1ba3e1c518b74`  
**Principal source tree:** `35629baf76a5add33c5a0e1a0c06ee4b271a9c60`  
**Principal article source:** `papers/A2-v17-boundary-information-coarsening/article/v104/paper.tex`  
**Controlling prior report:** `reviews/a2-v103-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`  
**Controlling prior review commit:** `f38495b78e52496d78b44cb5d461fbec65ff530b`  
**Independent review branch:** `review/a2-v104-independent-harsh-top4-2026-09-20`  
**Date:** 2026-09-20

## 1. Recommendation

**Recommendation for an Annals / Acta / Inventiones / JAMS-level general mathematics journal: reject in the present form.**

This is again **not a correctness rejection**.

Revision 104 is a substantial mathematical advance over revision 103. It directly addresses almost every item in the previous report rather than evading them through repackaging. In particular, it now contains:

1. a genuine finite-sheet reduction theorem starting from a polynomial fast map rather than from pre-specified affine sheets;
2. an all-dimensional reconstruction theorem for minimal endpoint representations on a nonempty open fully visible class;
3. an all-dimensional native stochastic family whose quotient image, secants, and exact deterministic ray complexity are computed exactly;
4. a finite-alphabet LAN theorem identifying the variational quadratic cost with efficient Gaussian discrimination;
5. explicit local-algebra and real-accessibility lemmas; and
6. the corrected clock-pair quantifier with an accompanying proof-level audit.

I found **no direct counterexample** to the principal v104 theorems in the material reviewed.

The remaining objection is therefore narrower than in v103 and is now primarily one of **conceptual level and intrinsic scope**.

The paper has proved several strong conditional/class-specific classification theorems, but the bridge between them is still largely a bridge of **realization**: one can construct a finite-sheet regime satisfying the polar-gap conditions; one can construct a fully visible endpoint quotient; one can construct a paired-contrast probability experiment realizing any prescribed positive quotient; and one can embed the finite-map residual problem into such a probability model.

For the stated journal class, I would expect a theorem showing that these structures are **forced, stable, or canonically attached to a broad natural class of the original singular observation problems**, not merely that they can be simultaneously realized by a sufficiently flexible construction.

The key unresolved mathematical question is now:

> **Which natural singular polynomial observation germs necessarily satisfy the polar-gap mechanism, and how does that condition interact intrinsically with endpoint visibility and the native stochastic quotient, without changing the observation model to a purpose-built realization?**

The manuscript does not yet answer that question.

Independently, the full source-bound native run recorded for v104, GitHub Actions run **35509714156**, was still **pending** with no conclusion at the time of this review. There is therefore still no durable successful composite runtime receipt for the full preserved graph. The authors correctly do not claim otherwise.

## 2. Scope of this report

I reviewed directly:

- `A2_REVISION_V104_INDEX.md`;
- `revisions/a2-v104/README.md`;
- `revisions/a2-v104/RESPONSE_TO_REFEREE.md`;
- `revisions/a2-v104/CONTENT_PRESERVATION.md`;
- `revisions/a2-v104/QUANTIFIER_AUDIT.md`;
- `revisions/a2-v104/LOCAL_VALIDATION.json`;
- `revisions/a2-v104/EXACT_DIAGNOSTICS.json`;
- `revisions/a2-v104/SOURCE_MANIFEST.json`;
- the complete 18-page v104 principal source, including all seven literal input files;
- `scripts/check_a2_v104.py`;
- `scripts/build_a2_v104.py`;
- `.github/workflows/a2-v104.yml`;
- the controlling v103 report;
- the v104 comparison against the controlling review;
- pull request #59; and
- the current state of native run 35509714156.

The mathematical/build source is pinned to `ff20178a3ac04712ceed5eb333e1ba3e1c518b74`. The revision head is one evidence/documentation commit beyond that source. The comparison from the mathematical source to the branch head adds only revision index/response/validation/provenance files; it does not alter the pinned principal mathematics or build inputs.

The standard applied here is intentionally severe. The issue is not whether the paper contains publishable mathematics. It plainly does. The issue is whether the central structure has reached the breadth, inevitability, and conceptual closure expected in a general top-four mathematics journal.

## 3. Executive assessment

Revision 104 changes the nature of the review.

In v103, the principal complaint was that the paper had exact theorems inside several normal forms but lacked the theorem deriving those normal forms from the original observation problem. Revision 104 answers a significant part of that complaint.

The new chain is:

1. start from a polynomial finite map (F) and residual (G);
2. exclude the critical/boundary value set and impose explicit polar-gap inequalities;
3. derive all inverse sheets and an affine leading residual set with a uniform relative estimate;
4. pass from the intrinsic leading residual set to a finite semidefinite tensor envelope;
5. classify the orthant-profile quotient on a fully visible endpoint class in arbitrary endpoint dimension;
6. construct a native paired-contrast stochastic family whose Hellinger quotient fills an open set of the relevant tensor space;
7. identify exact ray costs with the efficient Gaussian quotient experiment; and
8. support the scalar-order side by a real proper normal-crossings presentation.

That is a coherent architecture.

The difficulty is that the decisive hypotheses in step 2 are not yet themselves characterized in intrinsic geometric terms, while steps 5 and 6 concern deliberately selected open/model classes. The paper therefore still stops at the following level:

> **if** the original map satisfies the polar-gap bounds, finite sheets follow;  
> **if** the endpoint representation is fully visible, complete minimal reconstruction follows;  
> **if** one works in the paired-contrast family, native quotient and ray complexity are exactly classified.

Those are strong theorems. But the manuscript does not yet show that a broad natural class central to the original singular inverse problem is compelled to satisfy all three mechanisms, nor does it classify the strata where they fail.

This is the remaining top-four gap.

## 4. What revision 104 genuinely fixes

A harsh report should be explicit about the advances.

### 4.1 R103.1: the paper now derives finite sheets from an original polynomial fast map

Theorem 2.2 is a real response to the central v103 objection.

The paper no longer begins the reduction theory by assuming finitely many affine sheets. Instead it defines

[
Delta=F({det DF=0})cup F(partial N),
]

chooses a marked tube avoiding (Delta), and controls the slow residual through

[
A_F=DG,DF^{-1},
qquad
M(t)=sup|D_xA_F,DF^{-1}|.
]

Under the displayed polar-gap conditions, the theorem constructs the inverse branches, obtains a uniform quadratic Taylor remainder, localizes all global minimizers to the fast tube, and compares the true residual minimum with the exact affine-sheet costs **relative to the exact branch residual**, including cancellation.

This is substantially stronger and conceptually cleaner than v103.

The theorem also identifies the entire leading residual set by a closure construction in the original residual coordinates. That is important: the output is not merely a list of branch formulas depending on the chosen inverse charts.

### 4.2 The discriminant example is genuinely nontrivial

Example 2.6 is not a fixed-distance regular-fibre example.

For

[
F(x,y)=(x^2+y^2,xy)
]

the target approaches the ramified critical-value wall at a different scale from the principal fast scale, and the four inverse branches separate at unequal orders. The explicit derivative estimates show that the theorem can operate while the marked target approaches the discriminant.

This answers an important objection to treating the reduction as merely a regular covering theorem far from singularity.

### 4.3 R103.3: endpoint reconstruction now works in every endpoint dimension on a visible class

Theorem 4.3 is one of the strongest results in the revision.

Under full visibility, the local quadratic matrices form a Boolean lattice under Loewner order. The rank-one covers of the largest matrix recover the normalized cross columns, the largest-to-smallest difference recovers the normalized endpoint coupling, and the intrinsic rank proves global minimal endpoint dimension.

The theorem then goes further: any competing representation with the same minimal number of endpoints must itself realize all (2^e) active-set polynomials, hence is fully visible and is recovered by the same reconstruction. The complete minimal-dimensional fibre is therefore reduced to positive diagonal endpoint scaling and permutation.

This is a genuine all-dimensional extension of the one-endpoint result.

### 4.4 R103.2: the native exact-query theorem is now all-dimensional for an explicit stochastic class

The paired-contrast model is mathematically clean.

Because the nuisance mass derivatives are symmetric and the retained derivatives are antisymmetric within each pair, the nuisance-retained Fisher block vanishes exactly. This gives

[
Q(a)=4sum_j rac{z_jz_j^{mathsf T}}{a_j}.
]

The native image is relatively open in the rank-one tensor span, and the normalized secants fill the entire unit sphere of that span. The fixed and deterministic adaptive exact-ray complexities are both exactly the dimension (s) of that span.

The contrasts (e_i) and (e_i+e_j) yield the whole (operatorname{Sym}_k) in every dimension.

This is much stronger than the isolated two-variance determinant witness in v103.

### 4.5 R103.4: the ray cost now has an explicit statistical interpretation

Theorem 6.1 supplies the missing conceptual interpretation.

The finite-alphabet local likelihood calculation yields the Gaussian quotient experiment

[
Ysim N(Qv,Q),
]

with affinity (exp(-v^{mathsf T}Qv/8)) and the corresponding simple-alternative Neyman--Pearson power.

The paper is careful to say that exact ray-query complexity is **not** sample complexity.

That distinction is correct and materially improves the manuscript.

### 4.6 R103.5 and R103.6: the local algebra, real accessibility, and clock quantifier are now explicit

Appendix A contains actual lemmas for:

- factorization of individual real-analytic factors from a normal-crossings product;
- the even-exponent/common-factor property of a real sum of squares;
- proper pruning of positive-time source components; and
- explicit transverse real arcs reaching the divisor faces used in order ratios.

Appendix B corrects the clock statement to the precise form:

> for each fixed clock (i), there exists a separating clock (j).

The manuscript explicitly rejects the stronger false reading that every prescribed pair separates or that a single pair works uniformly over an entire compact family.

These are real improvements.

## 5. Main objection I: the polar-gap theorem is conditional at exactly the point where the intrinsic classification should begin

Theorem 2.2 is strong.

Its present role in the paper is still not strong enough for the claimed general-journal level.

### 5.1 The polar-gap inequalities encode the decisive geometry

The essential hypotheses are

[
sup_{Omega_t}|DG,DF^{-1}|le K_0,
qquad
c(t)/r(t)	o0,
qquad
r(t)sup_{Omega_t}|D_x(DG,DF^{-1})DF^{-1}|	o0.
]

Once these hold, the affine reduction follows by covering theory, Taylor expansion, and localization.

But these inequalities are not merely technical side conditions. They encode the exact small-shear relationship between the fast inverse geometry and the slow residual.

The manuscript currently does not give an intrinsic characterization of when a singular observation germ satisfies them.

### 5.2 The real-resolution theorem computes scalar orders, not the matrix derivative geometry needed by Theorem 2.2

Appendix A is useful, but it does not close this gap.

The proper real order presentation gives monomial exponents for (t) and (|R|), and it correctly supplies accessible real arcs realizing the maximal ratio.

That controls scalar contact order.

The finite-sheet theorem, however, depends on the stronger objects

[
DG,DF^{-1},
qquad
D_x(DG,DF^{-1})DF^{-1},
]

uniformly on a target tube that may itself approach the discriminant.

The final paragraph of Appendix A says that the semialgebraic suprema have graphs and their orders can therefore be extracted and tested. This is true as an **algorithmic reduction of a check to one-variable order data**, but it is not a structural theorem explaining why the strict inequalities hold for a broad natural class.

Thus the resolution machinery tells the reader how to test the hypothesis after enough data have been supplied; it does not classify the germs for which the hypothesis is automatically satisfied.

### 5.3 Corollary 2.5 and Example 2.6 are sufficient classes, not an intrinsic classification

The weighted-homogeneous initial-map result is valuable, and the ramified example is instructive.

But they still leave open:

- stability of the polar-gap property under natural perturbations;
- a geometric criterion in terms of ramification/polar data;
- behaviour under changes of resolution;
- necessity versus sufficiency of the displayed exponent inequalities;
- how the property stratifies a deformation family;
- what happens at the codimension-one boundary where (rM) stops tending to zero;
- whether the leading affine-sheet object has a canonical replacement when the condition fails.

Those questions are now the natural mathematical continuation of the paper.

A top-four version should, in my view, answer at least a substantial part of them.

## 6. Main objection II: realization is not yet unification

Corollary 5.2 is mathematically correct-looking and useful.

It should not bear the conceptual weight currently placed on it.

### 6.1 Realizing every positive quotient inside a paired-contrast model is permissive

Given (Q_0>0), the proof builds a paired-contrast experiment by selecting enough contrast vectors and centre masses so that the Hellinger quotient equals (Q_0).

This establishes a universal realization theorem.

It does **not** show that a natural observation family that produced (Q_0) in the first place has the paired-contrast structure, nor that its nuisance geometry is equivalent to that structure.

The same distinction applies to embedding a finite-map residual into a positive categorical observation by feeding the observation coordinates into a sufficiently flexible paired model.

This proves compatibility.

It does not prove canonical origin.

### 6.2 The three principal structures are still joined by construction rather than necessity

The manuscript now has three strong components:

1. polar-gap finite-map reduction;
2. fully visible endpoint reconstruction;
3. paired-contrast native quotient classification.

The paper can make each component occur together by designing a suitable stochastic observation.

What remains missing is a theorem of the form:

> a broad, independently defined class of singular observation models naturally produces a polar-gap finite-sheet residual, whose endpoint quotient is visible on a controlled stratum, and whose native Hellinger image has the asserted tensor geometry.

That would be a genuine unification theorem.

At present the connections are closer to closure properties and realizability.

For a specialized journal that may be entirely satisfactory. For the stated journal class, it is the central remaining limitation.

## 7. Main objection III: the endpoint theorem is complete on the visible stratum, but the singular strata are exactly where the quotient geometry becomes hardest

Theorem 4.3 should be retained.

My objection is not that the theorem is too weak as stated.

The issue is the paper's broader reconstruction claim.

### 7.1 Full visibility is a strong open-stratum hypothesis

The fully visible class requires:

- (B) to have full column rank; and
- every one of the (2^e) active sets to occur with strict inequalities on an open subset of the positive orthant.

Proposition 4.4 proves this class is nonempty and open for (kge e+1).

That is good.

But the quotient map becomes more interesting, not less, when visibility fails:

- active faces disappear;
- several endpoint coordinates may become observationally indistinguishable;
- local Hessians can coalesce;
- different cones can produce the same restricted value function;
- minimal dimension can drop;
- nonminimal representations can acquire continuous redundancy not generated by diagonal scaling.

The paper explicitly leaves these regimes open.

### 7.2 Proposition 4.5 is a deletion test, not a stratified classification

The finite KKT-based coordinate-deletion criterion is useful.

The invariant

[
delta(G)=dimoperatorname{span}{operatorname{ran}(S-S')}
]

gives a universal lower bound.

But the manuscript also correctly says that repeated deletion need not find a global minimum outside the visible class.

Thus the general quotient (Qmapsto G_Q) is not classified.

For a paper whose main title and abstract emphasize reconstruction of metric quotients, a top-four treatment should ideally identify at least the first degeneracy strata beyond full visibility and describe how the fibre changes there.

## 8. Main objection IV: the paired-contrast theorem is exact, but much of its all-dimensional geometry is built into the model

Theorem 5.1 is elegant.

Its significance needs to be calibrated carefully.

### 8.1 The linear tensor image is a consequence of the symmetric pair design

The paired cells have derivatives (z_j) and (-z_j), while the nuisance mass derivative is ((1/2,1/2)). The nuisance cross block therefore vanishes identically.

After the substitution (c_j=4/a_j), the quotient is a linear image

[
(c_j)longmapstosum_j c_j z_jz_j^{mathsf T}.
]

The exact dimension and secant sphere then follow from finite-dimensional linear algebra and openness.

This is clean mathematics, but it means the model has been designed so that the difficult quotient geometry collapses to a rank-one tensor span.

### 8.2 The theorem does not classify the native geometry of the original binary polynomial family

The manuscript is admirably explicit about this.

It does not claim that every higher-degree binary mixture has full-dimensional quotient image or the same exact-query complexity.

That honesty is important.

It also means, however, that the all-dimensional theorem does not by itself resolve the broader native-classification problem that motivated earlier versions of the paper.

A stronger top-four result would derive a comparable classification for a natural pre-existing family central to the program, rather than for a model introduced to make the tensor geometry exact.

### 8.3 The exact-ray complexity theorem remains an oracle theorem

The adaptive lower bound is sound-looking for deterministic exact queries.

The paper correctly says that if the full numerical centre law is supplied, the quotient can be computed directly.

The statistical LAN theorem gives the ray a canonical local-discrimination meaning, but it still does not turn the number of exact quadratic evaluations into a sample lower bound.

This is no longer a defect in correctness or exposition.

It is a limitation on how much conceptual weight the exact-query theorem should carry in the top-journal significance argument.

## 9. The statistical experiment theorem is valuable interpretation, but it is mostly classical machinery rather than the principal new mathematics

Theorem 6.1 is useful because it closes an interpretive gap left in v103.

The finite-alphabet LAN expansion, Schur-complement efficient information, Gaussian shift quotient, Hellinger affinity, and Neyman--Pearson power are standard mechanisms.

The contribution here is to connect them cleanly to the manuscript's variational ray cost and singular root scalings.

That should be presented as a supporting conceptual theorem.

I would not count it as an independent major source of top-four novelty unless the manuscript develops a substantially new comparison-of-experiments result in the singular setting.

The final statement on bidirectional Markov equivalence is appropriately restricted to **labelled quotient experiments with the same retained coordinates**. That qualifier should remain prominent so that the reader does not mistake it for an equivalence theorem for the original nuisance experiments.

## 10. Proof-level audit

I separate correctness from significance.

### 10.1 Theorem 2.2: no direct counterexample found, but the covering argument should be written more formally

The geometric mechanism is sound-looking:

- the target tube avoids critical and boundary values;
- the restriction of (F) is therefore a proper local diffeomorphism;
- each component covers the contractible target ball;
- the inverse branches give the Taylor representation;
- the exact branch residual is (o(r)), which places the affine minimizer inside the chart;
- the first residual coordinate excludes global minimizers outside the tube; and
- the quadratic remainder is a relative (O(rM)) error.

The proof becomes too compressed at the sentence applying the same argument to

[
(t,x)mapsto (t,F(x)-a(t))
]

over the variable-radius base.

Since (a(t)) and (r(t)) are initially assumed only continuous semialgebraic, the paper should explicitly formulate the total inverse set as a proper definable covering after a finite cell decomposition, state why the fibre cardinality is constant, and derive the semialgebraic sheet trivialization from that statement.

I believe this is repairable proof exposition, not a discovered false theorem.

### 10.2 Theorem 3.1: the moment lift and exposed-face formula are sound-looking

The second-moment representation of an affine sheet is correct.

The full-column-rank condition on ([L_b,c_b]) gives the trace coercivity needed for closedness.

For (H>0), equality at the minimum removes covariance and positive-semidefinite slack and leaves precisely the convex hull of minimizing rank-one tensors.

I found no direct objection.

### 10.3 Lemma 4.2 / Theorem 4.3: the endpoint reconstruction is plausible and strong

The Boolean order is supported by the block Schur-complement identity.

Because the columns of (B) are independent, the rank increment is exactly the number of newly active endpoints.

The reconstruction formula

[
overline C=
left[U^+(A-S)(U^+)^{mathsf T}ight]^{-1}
]

is algebraically correct in the stated normalized coordinates.

The global minimality argument using (operatorname{rank}(A-S)=e) is convincing.

The step showing that every competing (e)-endpoint representation is itself fully visible is important and should be expanded. The present counting argument is concise:

- (G) intrinsically has (2^e) distinct local quadratic polynomials;
- any (e)-endpoint representation has at most (2^e) active-set polynomials;
- therefore every active set must occur on a full-dimensional cell;
- full column rank prevents the strict KKT conditions from degenerating identically on such a cell.

I think this is essentially correct, but it deserves a standalone lemma at this level.

The distance-representation uniqueness statement should also specify the minimal ambient dimension/factor dimensions explicitly before invoking the fact that two invertible Gram factors differ by an orthogonal map.

### 10.4 Proposition 4.4: the positive-kernel construction is convincing

Surjectivity of (B^{mathsf T}) gives a preimage of any prescribed KKT right-hand side, and a large multiple of a strictly positive kernel vector moves that preimage into the positive orthant.

This realizes every active set with strict inequalities.

The openness argument is also plausible.

### 10.5 Proposition 4.5: no direct objection

The missing-coordinate KKT inequality is exactly the condition for the reduced minimizer to remain optimal in the full problem.

Because the reduced problem has finitely many active cones, the global test reduces to finitely many polyhedral dual-cone checks.

The lower-bound invariant follows from the range of Hessian differences.

### 10.6 Theorem 5.1: the exact native dimension/secant/query result is sound-looking

The nuisance-retained cross term cancels pairwise.

The image is the linear image of an open set under a surjection onto (mathcal V), hence relatively open.

An interior relative ball implies every nonzero direction of (mathcal V) occurs as a secant direction.

The (s)-query upper bound is finite-dimensional separation by quadratic evaluations.

The deterministic adaptive lower bound correctly uses a transcript at an interior (Q_0), finds a nonzero perturbation in the common kernel of fewer than (s) recorded evaluation functionals, and keeps both perturbations inside the same native open image.

I found no direct flaw.

### 10.7 Corollary 5.2: plausible as a realization theorem; it should be described precisely as such

The construction of an open native neighbourhood around an arbitrary (Q_0>0) is algebraically clear.

The Hellinger embedding of the finite-map residual is also plausible on a sufficiently small positive-probability neighbourhood.

My objection is conceptual, not correctness: this is a flexible realization result, not a proof that the original observation problem canonically has this paired-contrast form.

### 10.8 Theorem 6.1: the LAN and efficient quotient calculations are sound-looking

On a finite alphabet, the (o(n^{-1/2})) probability expansion is sufficient for the displayed LAN calculation under the stated uniformity.

The Schur complement is the covariance/information of the efficient score.

Bidirectional Markov equivalence preserves the Hellinger affinity in both directions, and equality of (v^{mathsf T}Qv) on a cone with nonempty interior identifies (Q).

No direct correctness objection.

### 10.9 Appendix A: the factorization/accessibility gap in v103 is substantially repaired

The coordinate ideals are prime in the local real-analytic ring, and successive analytic division gives the individual monomial factors.

The sum-of-squares argument correctly forces even coordinate orders and a common vector factor.

The proper-pruning lemma gives the missing compactness argument for retaining positive-time accessibility.

The final theorem is a legitimate real order-presentation result.

Again, the remaining limitation is that it produces/order-tests scalar quantities and does not by itself supply a geometric classification of the polar-gap derivative conditions.

### 10.10 Appendix B: the clock quantifier is now correct

The proof establishes exactly the existential statement it needs.

The partial-fraction independence argument is standard and clean.

I regard R103.6 as answered.

## 11. Reproducibility and source-provenance audit

The repository discipline remains unusually explicit.

### 11.1 The mathematical source is cleanly pinned

The v104 records identify:

- source commit `ff20178a3ac04712ceed5eb333e1ba3e1c518b74`;
- source tree `35629baf76a5add33c5a0e1a0c06ee4b271a9c60`;
- controlling review commit `f38495b78e52496d78b44cb5d461fbec65ff530b`; and
- exact hashes for the principal and all literal input files.

The branch-head delta beyond the mathematical source is documentation/evidence only.

### 11.2 Local principal validation is positive but properly scoped

The local record reports:

- a successful native 18-page principal build;
- no undefined references or citations;
- no multiply-defined labels;
- no LaTeX warnings;
- no overfull or underfull boxes; and
- passing exact rational/symbolic diagnostics.

The diagnostics check representative endpoint dimensions, native dimensions, a ramified collision instance, and the clock quantifier.

The files correctly say these checks are **not** formal verification of the universal theorems.

### 11.3 The full native builder has the right source-binding design

The builder:

1. binds current source files to the checked-out commit;
2. replays the exact v103 source trigger in a detached worktree;
3. requires a successful v103 runtime receipt;
4. verifies inherited source and replay artifact hashes;
5. compiles all four v104 targets; and
6. emits a composite receipt only after success.

This is the correct evidentiary architecture.

### 11.4 R103.7 / R102.8 remains open

At the time of this review, run **35509714156** was still:

- status: `pending`;
- conclusion: `null`.

No successful durable composite receipt was available on the reviewed branch.

Therefore the full archived graph has **not** yet been demonstrated by the source-bound remote run.

This is not a mathematical counterexample.

It remains a reproducibility blocker for a claim of complete native archival validation.

## 12. Disposition of the v103 requests

| Prior request | v104 disposition | Referee assessment |
|---|---|---|
| R103.1 intrinsic reduction into the finite-sheet category | **Substantially answered technically; only partially answered conceptually** | Theorem 2.2 derives sheets from a polynomial finite map under explicit polar-gap conditions and includes a ramified example. Missing: intrinsic characterization/stability/genericity of those conditions for a broad natural singular class. |
| R103.2 native quotient geometry beyond the d=2 witness | **Answered for the paired-contrast class in every dimension** | Exact dimension, secants, rank loci, and sharp deterministic fixed/adaptive exact-ray counts are obtained. Missing: comparable classification for the original broader binary/singular families. |
| R103.3 endpoint fibres for (ege2) | **Answered on a nonempty open fully visible class** | Minimal dimension and the complete minimal-dimensional fibre are reconstructed. Nonvisible strata and general nonminimal fibres remain open. |
| R103.4 canonical role of the ray oracle | **Answered at the local-experiment level** | The ray is identified with efficient Gaussian discrimination. The paper correctly separates query complexity from sample complexity. |
| R103.5 theorem-proof complete real resolution step | **Largely answered** | Explicit local factorization, pruning, and accessibility lemmas are present. |
| R103.6 clock quantifier and proof-level audit | **Answered** | The existential pair statement is correct and the scope audit is explicit. |
| R103.7 source-bound native receipt | **Not answered** | Run 35509714156 remains pending; no durable successful composite receipt was available at review time. |

## 13. Literature and positioning

The principal bibliography now contains seven references spanning real algebraic geometry, real uniformization, parametric quadratic programming, convex optimization, comparison of experiments, and LAN.

That is enough to identify the classical mechanisms used in the proofs.

It is not enough, in my view, to substantiate broad priority claims for a paper presenting itself as a general theory across:

- singular inverse geometry;
- real resolution/contact invariants;
- inverse representation of piecewise-quadratic value functions;
- semidefinite/moment lifts of affine arrangements;
- statistical information quotients;
- comparison of experiments; and
- oracle reconstruction of quadratic forms.

I am **not** asserting that the main results are known.

I am saying that, from the current bibliography, I cannot independently certify that the manuscript has located all of its closest conceptual neighbours or explained precisely which reconstruction statements are new relative to those literatures.

For a top-four submission, that comparison should be much broader and more explicit.

## 14. Revisions required before reconsideration at the same journal class

The next revision should not primarily add more examples, finite certificates, or repository infrastructure.

It needs to deepen the intrinsic structure.

### R104.1 — Characterize the polar-gap regime geometrically

Prove a theorem that gives natural, coordinate-invariant sufficient conditions—and ideally a sharp or stratified characterization—for the polar-gap inequalities from intrinsic data of the finite map and residual germ.

The result should address at least some of:

- stability under perturbation;
- behaviour under real resolution;
- ramification indices/polar data controlling (DF^{-1});
- residual orders controlling (DG,DF^{-1});
- the boundary (rMasymp1);
- invariance of the criterion under allowed source/observation changes; and
- what replaces the affine-sheet limit when the criterion fails.

This is the most important mathematical request.

### R104.2 — Replace permissive realization by a natural unification theorem

Identify a broad observation family defined independently of the desired quotient geometry and prove that its singular germs naturally produce:

- the finite-sheet reduction;
- a controlled endpoint quotient; and
- the native information geometry,

without first redesigning the observation law into the paired-contrast realization.

A theorem of this form would convert the present toolkit into an intrinsic theory.

### R104.3 — Develop the first nonvisible endpoint strata

Go beyond the open fully visible class.

At minimum, classify codimension-one visibility failures and determine:

- when local Hessians coalesce;
- how minimal endpoint dimension changes;
- the fibre dimension and gauge group;
- which redundancies are removable by coordinate deletion and which are not; and
- canonical normal forms on the first degeneracy strata.

A complete all-strata theory may be too large, but the paper should show that the singular boundary of the visible class is mathematically controlled.

### R104.4 — Prove a native classification for a natural pre-existing model family

The paired-contrast family is an excellent exactly solvable model.

For top-four breadth, add a theorem in which the tensor span, secant geometry, and query complexity are derived for a natural family already central to the original singular observation problem, rather than designed to realize arbitrary (Q).

The earlier binary polynomial model is one possible target.

### R104.5 — Expand the novelty/priority comparison

Provide a serious literature map explaining the relationship of the new results to:

- real and semialgebraic singularity/contact theory;
- inverse problems for parametric quadratic programs and piecewise-quadratic value functions;
- spectrahedral/moment representations of affine or quadratic data;
- information geometry and efficient information;
- comparison of experiments; and
- exact quadratic-form reconstruction/query complexity.

The manuscript should distinguish classical ingredients, known adjacent structure, and genuinely new reconstruction statements theorem by theorem.

### R104.6 — Expand two compressed proof transitions

For a paper at this level, make the following steps standalone lemmas:

1. the parameterized proper definable covering/trivialization used in Theorem 2.2; and
2. the counting/strictness argument proving that every competing minimal (e)-endpoint representation in Theorem 4.3 must itself be fully visible.

Also state the ambient dimension assumptions explicitly in the distance-representation uniqueness claim.

### R104.7 — Complete the source-bound native receipt

Run the exact v104 source-bound workflow to a successful conclusion and commit the durable composite receipt, PDFs, logs, and hashes that the current builder is designed to produce.

Do not mark the runtime item closed while the run remains pending or without a source-bound receipt.

## 15. Editorial comments

1. The phrase **“intrinsic finite-sheet reduction”** is defensible for the output once the polar-gap hypotheses are imposed. The introduction should nevertheless make equally prominent that the present paper does not intrinsically classify when those hypotheses hold.

2. Corollary 5.2 should consistently be described as a **realization/embedding theorem**. It should not be used rhetorically as evidence that the paired-contrast model is the canonical stochastic source of an arbitrary quotient.

3. The abstract is much more accurate than in earlier revisions. It could still distinguish more sharply between “all-dimensional within an exactly solvable class” and “all-dimensional for the original observation models.”

4. The endpoint theorem deserves more conceptual emphasis than the exact symbolic checker. It is one of the genuinely structural contributions.

5. The exact diagnostic files are appropriately scoped. Keep them as verification aids, not as mathematical evidence for universal statements.

6. The 18-page principal is compact relative to the number of ideas. Several proofs would benefit from an extra page or two of structural lemmas rather than further compression.

7. The paper should define early and explicitly the precise equivalence relation under which a “metric quotient” is considered intrinsic. Different sections currently use coordinate covariance, endpoint congruence/permutation, and labelled statistical equivalence; these are related but not identical notions.

8. The supporting/historical volume is useful for provenance, but the journal-level mathematical judgment should continue to rest on the self-contained principal.

## 16. Originality and depth assessment

Revision 104 contains multiple results that I regard as independently interesting.

### 16.1 Finite-sheet reduction

The strongest advance is that affine sheets are now derived from an original finite polynomial map under quantitative polar-gap hypotheses.

The exact-residual relative estimate through cancellation is technically useful.

The remaining step is to characterize the hypothesis itself in intrinsic singularity-theoretic terms.

### 16.2 Endpoint reconstruction

The Boolean Hessian lattice and all-dimensional recovery of the complete minimal visible fibre are conceptually strong.

The remaining step is a stratified theory across visibility loss.

### 16.3 Native stochastic geometry

The paired-contrast theorem is complete and clean inside its class.

The remaining step is to show that a comparably rich tensor/secant structure is forced in a natural model class rather than introduced by design.

### 16.4 Statistical interpretation

The efficient Gaussian quotient gives the variational ray a correct intrinsic decision-theoretic meaning.

The remaining step is not more LAN machinery; it is to integrate that meaning into the natural singular model classification.

These are no longer disconnected technical requests. They point to one missing theorem:

> a natural structural classification that explains when and why the same singular observation problem gives rise to the finite-sheet, endpoint, and information quotients studied separately here.

## 17. Final assessment

Revision 104 is a serious and substantial response to the v103 report.

It closes most of the previous **technical** objections:

- finite sheets are now derived rather than postulated;
- endpoint reconstruction is genuinely all-dimensional on an open visible class;
- native stochastic quotient geometry is exactly classified in every dimension for a fixed family;
- the ray cost has a proper local statistical interpretation;
- the real-resolution steps are explicit; and
- the clock quantifier is repaired.

I found no direct counterexample to the principal theorems.

Nevertheless, for an Annals / Acta / Inventiones / JAMS-level general mathematics journal, I still recommend **rejection in the present form**.

The reason is now sharply focused.

The central theorem is conditional on polar-gap inequalities whose intrinsic geometric scope is not yet classified; the endpoint classification is confined to the fully visible stratum; and the all-dimensional native theorem concerns a paired-contrast family engineered so that the quotient becomes a linear rank-one tensor span. Corollary 5.2 proves that these worlds can be made compatible by realization, but not that they are canonically the same structure in a broad natural class of the original singular observation problems.

That is a meaningful distinction at the stated journal level.

At a strong specialized journal, this version could support a serious positive discussion after proof expansion and literature positioning. Under the much higher general-journal standard requested here, I would want the next revision to replace one more layer of realizability by an intrinsic structural theorem.

Finally, the reproducibility item remains open: run 35509714156 was pending at review time and no durable source-bound composite runtime receipt was available.

**Disposition:** mathematically serious; materially stronger than v103; no direct correctness rejection; most prior technical requests answered; one major intrinsic-classification step still missing; not ready for the stated top-four general mathematics journal class in its present form.
