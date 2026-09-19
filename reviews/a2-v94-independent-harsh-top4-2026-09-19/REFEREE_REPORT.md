# Independent harsh referee report on A2 revision 94

**Review date:** 19 September 2026  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** revision/a2-v94-germ-newton-stochastic-intersection-2026-09-19  
**Reviewed branch head:** 5e01e5a2d6e93ef4c1e2619707608626fdc0f6cf  
**Controlling previous report:** reviews/a2-v93-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md, commit 7d5e9d80a6033399afe633da21b44e4d6f435a2f  
**Previous reviewed manuscript head:** 2832f7a7060217f6c8110688b66b73b9b946d13a  
**Reviewed manuscript:** *Projective polynomial observations: intrinsic Newton geometry and additive normalization*  
**Author:** Qian Qi  
**Review status:** owner-requested AI-assisted external-referee-style assessment; not a journal-commissioned peer review.

## 1. Recommendation

**Recommendation to the editor: reject in the present form at the stated four-leading-general-mathematics-journal level.**

This is a substantially more positive mathematical assessment than my report on revision 93. Revision 94 directly addresses the principal conceptual objection in that report: it no longer substitutes an affine tangent experiment for the nonlinear admissible stochastic germ at the singular points where higher model jets matter. The new full-germ theorem is coherent, the left-right metric transport issue has been repaired, and the cubic rank-loss construction is a genuine whole-model identifiable stochastic singularity rather than an ambient rational perturbation mislabeled as stochastic.

I did not find an immediate counterexample that invalidates the new intrinsic Newton theorem or the exact-fibre argument in the cubic example. In particular, I regard the main v93 correctness objections concerning nonlinear-germ composition, fibre identification, and metric transport as materially addressed.

The reason for rejection has therefore shifted. The remaining obstacle is now the level and form of the mathematical contribution.

The full-germ theorem obtains its exponent from the observation-ball envelopes of the cluster coefficients themselves. This is an exact and useful structural representation, but at the genuinely singular points it does not yet produce a finite local algebra, normal form, stratification, or model-jet classification from which the exponent can be read without solving essentially the same semialgebraic inverse optimization that defines the original modulus. The explicit composed-jet formula does provide such a calculation, but only under an immersed analytic observation chart, i.e. away from the central singular-observation difficulty. The featured stochastic theorem then handles one carefully engineered binary cubic intersection by bespoke inequalities. It establishes existence of an important phenomenon, but it does not classify a family of singular strata, prove genericity or stability, or compute the new exact leading coefficient object in that example.

At a specialist inverse-problems, matrix-polynomial, algebraic-statistics, or singular-statistics venue, I would now view this as a serious manuscript with several publishable components. At the level claimed here, I would require one more theorem-level step: either a genuine singular-germ Newton algorithm/normal form for a nontrivial class of stochastic strata, or a model-wide classification showing that the new invariant organizes a broad family of intersecting singularities rather than one constructed example.

The paper has moved from “the central theorem is not yet intrinsic to the model” to “the central intrinsic theorem is mathematically plausible but too close to an exact reformulation unless it is converted into a classification principle.”

## 2. Scope of this review and exact source pin

I reviewed revision 94 at exact head

5e01e5a2d6e93ef4c1e2619707608626fdc0f6cf.

The v94 branch is based on the v93 review commit and adds the new mathematical sources

- papers/A2-v17-boundary-information-coarsening/article/v94/germ_newton.tex;
- papers/A2-v17-boundary-information-coarsening/article/v94/stochastic_intersection.tex;
- papers/A2-v17-boundary-information-coarsening/article/v94/metric_transport.tex;
- papers/A2-v17-boundary-information-coarsening/article/v94/paper.tex;

together with the v94 response, source manifest, verifier, review-ready note, entrypoint, and branch-scoped workflow.

I read the new main manuscript source, the three new theorem/proof modules, the response to the v93 report, the retained intrinsic-modulus theorem from v92, the retained literature discussion, the v94 verifier and manifest, and the latest two v94 commits. I also checked the branch-specific Actions state.

At the time of this report, workflow run 35441749047 for exact head 5e01e5a2d6e93ef4c1e2619707608626fdc0f6cf was still **queued** and had no conclusion. The earlier v94 run at f07761aebdad27e520ac0218a25f44ce881266cb was also queued. Therefore I do **not** record the complete exact-head manuscript as remotely compiled or source-audited. This is an operational qualification, not a mathematical objection.

The local diagnostics are correctly described by the authors as finite regressions rather than proof verification. I treat them only in that role.

## 3. What revision 94 genuinely fixes

### 3.1 The affine-slice objection from v93 is answered in principle

Theorem “Intrinsic Newton law” is the right conceptual response to the main v93 criticism.

Instead of selecting a tangent space and expanding the determinant there, revision 94 works on the actual compact semialgebraic admissible set X, the actual observation map F, and the monic spectral polynomial A_x. Once the spectral target is constant on the exact observation fibre, it factors the nearby spectrum into separated base clusters and uses the cluster coefficients c_{r,a}(x). The quantities

b_{r,a}(t) = max over the full Hellinger ball of |c_{r,a}(x)|

are then assigned their semialgebraic orders beta_{r,a}, and the root exponent is

alpha_P = min beta_{r,a}/(m_r-a).

This does retain nonlinear constraints, higher model jets, rank loss, boundary inequalities, conjugacy, and all other semialgebraic restrictions. It is not an affine tangent statement.

That distinction is the central improvement in this revision.

### 3.2 The joint limiting coefficient fibre is better than coordinatewise envelope arithmetic

The definition of the rescaled joint coefficient set C_t and its limiting fibre C_0 is a meaningful refinement.

The manuscript correctly observes that separate envelope maxima do not retain the dependence among coefficients needed for the leading diameter. The proof that C_t converges to C_0 in Hausdorff distance uses semialgebraicity to rule out oscillatory subsequence behavior, and then uniform continuity of the monic-root multiset map converts coefficient-set convergence into root-set convergence.

This is a good argument. It is also the part of the theorem that is genuinely sharper than merely saying “the modulus is semialgebraic and hence has a Puiseux exponent,” which was already present in v92.

### 3.3 The composed-jet theorem explicitly includes higher model jets

Theorem “Composed-jet formula” fixes precisely the formal defect highlighted in the v93 report.

For

M(x)=M_0+E_1(x)+E_2(x)+...

the quadratic determinant jet now contains both

D det(M_0)[E_2(x)]

and

(1/2) D^2 det(M_0)[E_1(x),E_1(x)].

This is the right invariant calculation after composition with the admissible map. The curved-cancellation examples are also well chosen: they show that identical affine tangents can have delayed spectral exposure or local spectral rigidity once higher jets are included.

I regard this part of the v93 objection as closed.

### 3.4 The left-right metric issue is repaired

The new metric-transport proposition makes the needed distinction between algebraic covariance and statistical isometry.

If T(X)=AXB, the determinant scaling is algebraic. The observation metric is preserved only after pullback,

h_tilde(Q,Q') = h(T^{-1}Q,T^{-1}Q'),

and the stacked-clock Fisher form transforms as

H_tilde = T^{-T} H T^{-1}.

The latest head also corrects the notation and makes the stacked map I_ell tensor (B^T tensor A) explicit. This directly addresses the v93 complaint that the leading metric constant had been claimed invariant without transporting the metric.

### 3.5 The cubic example is genuinely a whole-model stochastic singularity

Theorem “Rank loss, multiple roots, and a vanishing intrinsic modulus” is the strongest model-specific addition in v94.

The point has:

- rank U = 1;
- a double root in f;
- a triple root in g;
- one active root-boundary constraint;
- strict positive observed cells;
- strict weights;
- a positive and invertible second channel;
- tau(P_*) > 0;
- a noninjective ambient coefficient observation Jacobian.

The exact-fibre argument is substantially better than the earlier pointed constructions. The proof first recovers the monic normalizer and numerator polynomial from the exact observation by tau(P_*)>0 and interpolation. It then uses the second marginal to force the two competitor component polynomials into the affine pencil generated by f and g. The cubic discriminant, endpoint sign, and depressed-cubic inequalities isolate the two admissible real-rooted points of that pencil.

Subject to the smaller proof-detail request in Section 8 below, I accept that this proves singleton **spectral** fibre for the whole closed model at the displayed datum.

### 3.6 The local upper and lower root orders in the cubic example are credible

The upper proof is not merely an application of the abstract theorem. It derives O(delta) coefficient recovery for the two component polynomials, then uses the anchored real-rooted comparison to obtain O(sqrt(delta)) root displacement.

The lower family

g_u(z)=(z-s)((z-s)^2-u^2)

is an actual stochastic alternative. Its coefficient and observation perturbation are quadratic in u while the root displacement is linear. The nonzero Hellinger derivative with respect to u^2 is justified through the already established normalization injectivity.

Thus the order 1/2 is not an artifact of an ambient coefficient ball.

### 3.7 The manuscript now distinguishes exact local, uniform, and ambient statements more responsibly

Revision 94 keeps the datum-dependent germ theorem separate from the older boundary-uniform common-flag estimates and does not insert pointwise pole orders into a moving-class theorem with old constants. It also explicitly distinguishes positive-rational examples from stochastic factorizations.

This quantifier discipline is an important improvement.

## 4. Major objection I: the full-germ “Newton law” is exact but not yet a singular-germ computation theorem

This is now the decisive conceptual issue.

The theorem defines beta_{r,a} as the order of

b_{r,a}(t)=max_{x: h(F(x),P)<=t}|c_{r,a}(x)|.

That is an exact invariant. However, at a singular observation point, determining b_{r,a}(t) is itself a semialgebraic optimization problem over the full inverse image of the observation ball. In general it contains essentially the same singular inverse geometry as omega_P(t), merely expressed coefficient by coefficient.

The theorem therefore gives a decomposition of the original modulus, not yet a classification of the singularity.

The distinction matters because the manuscript repeatedly uses language such as “Newton law,” “finite cluster-coefficient envelopes determine the exponent,” and “intrinsic Newton geometry.” In classical Newton-polyhedron arguments, the point of the construction is that the leading order is read from finite algebraic data that are manifest before solving the entire local optimization problem. Here, for the most difficult singular-observation case, the finite list of functions is finite only in number; their orders still come from full semialgebraic maximization over the original admissible germ.

This is not a correctness criticism. It is a novelty and theorem-strength criticism.

Revision 92 had already proved that omega_P(t) itself is semialgebraic and therefore has a rational Puiseux exponent. Revision 94 improves this by showing that the exponent can be recovered from finitely many cluster-coefficient envelopes and that the exact leading diameter is the root image of a joint rescaled coefficient fibre. That is useful. But the proof remains, at its core:

1. semialgebraic preparation for finitely many optimized coefficient functions;
2. elementary root-versus-coefficient scaling;
3. definable Hausdorff convergence;
4. continuity of polynomial roots.

For a top-four claim, I would want the theorem to go one layer deeper and identify beta_{r,a}, or the limiting fibre C_0, from a finite local algebra attached to the singular observation germ.

Examples of a genuinely stronger endpoint would be:

- a Newton-polyhedron or valuation formula on a Whitney/semialgebraic stratification;
- a finite module/ideal construction whose valuations give all beta_{r,a};
- a resolution or monomialization theorem specialized to the observation-spectral map, with a finite set of candidate edges;
- a normal-form theorem for a broad class of singular stochastic strata;
- an algorithm that takes polynomial defining equations of the local model and returns the exponent and leading fibre without first constructing the observation-ball maxima as new optimization functions.

The current “finite description by real quantifier elimination and algebraic branch analysis” is an effectiveness statement, not such a structural classification. In particular, it does not explain which singular features of the stochastic model determine the exponent.

This is the main reason I still do not see the central theorem at the claimed general-journal level.

## 5. Major objection II: the stochastic breakthrough is one tuned example, not a class or stratification

The cubic rank-loss example is mathematically worthwhile. It also appears highly engineered.

The construction uses:

- k=m_1=m_2=2;
- degree d=3;
- one channel with exactly repeated columns;
- a specifically related pair f(z)=z(z-r)^2 and g(z)=(z-2r/3)^3;
- one root pinned to the endpoint of [0,1];
- a specially chosen affine cubic pencil whose discriminant has zeros exactly at the two admissible endpoints c=0,1;
- an invertible second channel to recover the row space;
- seven clocks, allowing the normalization and interpolation argument to be exact.

This proves existence of an identifiable intersection of several singular mechanisms. It does **not** yet show that such identifiable intersections form a stable, generic, open, positive-codimension, or classifiable family.

Indeed, the isolation mechanism uses an active inequality face. If the endpoint root at zero is moved into the interior, the sign condition h_c(0)<=0 disappears in its present form. If the special relation s=2r/3 is perturbed, the pencil discriminant and real-rooted intersection geometry change. The manuscript does not tell the reader which aspects are stable and which are accidental.

For the top-four threshold, I would want at least one of the following:

1. a theorem characterizing all binary cubic rank-loss identifiable intersections up to an explicit equivalence;
2. a transversality or stability theorem showing an open family of inequality-constrained singularities with the same intrinsic exponent;
3. a higher-dimensional family with a computable singular invariant;
4. a stratification theorem for the closed stochastic model that places this example in one named stratum and gives a formula on that stratum;
5. a construction for arbitrary degree or multiplicity pattern, not only this cubic pencil.

Without such a result, the example is a convincing witness that the phenomenon exists, but it does not yet demonstrate that the new theory controls a substantial portion of the model.

## 6. Major objection III: the paper advertises an exact leading constant but does not compute it in the flagship stochastic example

The abstract and main theorem emphasize that the joint rescaled coefficient fibre determines the exact leading root-multiset diameter.

This is potentially one of the strongest additions of v94.

However, in the principal stochastic theorem the manuscript does not actually identify C_0 or compute C_*.

The proof proceeds differently:

- a bespoke whole-model argument gives omega(t) <= C sqrt(t);
- one explicit path gives omega(t) >= c sqrt(t);
- the abstract full-germ theorem then upgrades the matched order to the existence of an exact asymptotic C_* sqrt(t)+o(sqrt(t)).

That is logically legitimate, but it means the flagship example does not demonstrate the advertised exact-constant mechanism. The constant is named as “the joint coefficient-fibre diameter,” but the joint fibre is not written down.

For a general theorem whose new content beyond v92 is specifically the leading limiting set and exact diameter, this omission is significant.

I recommend computing, or at least reducing to an explicit finite optimization, the limiting coefficient fibre for the cubic example. Ideally the paper should answer:

- Which rescaled cluster coefficients survive at order t^{1/2(m_r-a)}?
- What relations among them are forced by the closed stochastic constraints?
- Which admissible arcs realize the extreme points?
- Does the explicit symmetric split g_u attain the diameter, or only one side of it?
- Is C_* expressible in terms of r, alpha, u, V, the clocks, and the Hellinger weights?
- If not in closed form, what explicit semialgebraic finite program determines it?

Until this is done, the exact-constant part of the theory remains mostly abstract in the one singular stochastic example that is supposed to justify it.

## 7. Major objection IV: the novelty boundary with classical semialgebraic and perturbation theory remains underdeveloped

The manuscript now credits the correct broad classical ingredients:

- semialgebraic elimination and Puiseux preparation;
- matrix-polynomial root perturbation;
- structured multiple-eigenvalue conditioning;
- rational interpolation and realization;
- local asymptotic minimax theory.

That is good, but the comparison is still not sharp enough for the new v94 theorem.

The full-germ result is very close in spirit to classical statements about definable moduli, Łojasiewicz exponents, metric regularity/subregularity, arc criteria, and semialgebraic optimization. The paper needs to explain, theorem by theorem, what is not already a standard consequence of those frameworks after choosing the spectral target map.

In particular:

- v92 already proves semialgebraicity and a Puiseux law for the intrinsic modulus;
- the root map from monic coefficients to unordered multisets has classical Hölder behavior;
- cluster-factor coefficients are local analytic functions of polynomial coefficients;
- definable set-valued maps have strong tame convergence properties.

The new point is presumably the **exact weighted cluster decomposition with the joint limiting coefficient fibre**, plus its use with the probability-normalized stochastic image. If that is the novelty, it should be isolated as a precise theorem and compared directly with the strongest relevant definable-error-bound and structured root-perturbation results.

At present the literature section mostly says the ingredients are classical but the composition is specific. That is not enough for a leading general journal. A reader should be able to see a proposition-by-proposition delta from the classical theory.

I would also strongly encourage the authors to add direct references on Łojasiewicz exponents, definable metric regularity/error bounds, and tame set-valued asymptotics rather than relying almost entirely on general real-algebraic-geometry texts for the new intrinsic modulus machinery.

## 8. Major objection V: several important steps in the cubic whole-model proof are compressed too aggressively

I did not find a contradiction in the cubic proof, but a few transitions are too short for a theorem carrying much of the paper’s significance.

### 8.1 The singular-value transfer from B' to V' should be written explicitly

The manuscript says:

> The coefficient matrix of B' has its second singular value bounded below. The component polynomial coefficients and weights range over a fixed compact set. ... this forces the least singular value of V' to be bounded below as well.

This is plausible, but it should not be left as prose.

Write the coefficient matrix as

B'_coef = V' diag(alpha') F'_coef.

Then state the exact singular-value inequality used, the uniform bound on ||diag(alpha') F'_coef||, and conclude a quantitative lower bound for sigma_min(V'). Since this bound is what permits inversion of V' for **arbitrary nearby closed-model competitors**, it is a key part of the whole-model claim.

### 8.2 The passage from V'^{-1}B' to the affine pencil deserves a displayed derivation

The manuscript says that multiplying the coefficient error by the inverse gives

f'_b = (1-c_b)f+c_bg + O_coef(delta).

The argument should explicitly distinguish:

- the exact row span of B;
- the perturbed row span of B';
- division by weights bounded below by alpha_*;
- the monicity constraint forcing the two affine coefficients to sum to 1+O(delta);
- the uniform boundedness of c_b.

This is all recoverable, but it is exactly where a hidden competitor dependence could enter. The proof should show the constants.

### 8.3 The “cannot both approach the same polynomial” step should be quantified

Again, the rank-two coefficient matrix gives the right idea. But the proof should say that if both rows approach f (or both approach g), the second singular value of F'_coef tends to zero, hence the second singular value of B'_coef tends to zero under uniformly bounded V' and weights, contradicting the established lower bound.

### 8.4 The normalization-kernel argument should state the marginal polynomial identity

The tau(P_*) proof is elegant but very compressed. After qE=eK, the paper should explicitly write the second marginal identity and the multiplication by V^{-1} that yields q | ef and q | eg. It should then state why gcd(f,g)=1 implies q|e. These are easy steps, but they are the reason a rank-one first channel does not destroy normalization recovery.

For a routine lemma I would not insist on this level of detail. For the flagship singular example, I do.

## 9. Major objection VI: the manuscript is still an accretive theory compendium rather than a top-four article with one inevitable spine

The v94 introduction is much better than the earlier architecture. It now has a recognizable principle: observed admissible germ geometry.

Nevertheless, the submitted object still carries a very large inherited apparatus:

- global additive normalization;
- clock complexity;
- observable polynomial conditioning;
- quotient charts;
- regular Fisher geometry;
- local minimax theory;
- residue methods;
- algorithms;
- polynomial statistics;
- intrinsic moduli;
- singular normal forms;
- sharp flags;
- constrained affine Newton laws;
- fibres and admissibility;
- the new full-germ theorem;
- the new stochastic intersection.

The active v94 graph has twenty-seven TeX inputs.

The issue is not length by itself. The issue is theorem hierarchy. A top-four paper should make it obvious which one or two theorems change the field and which results are corollaries, infrastructure, or earlier-generation scaffolding.

At present the paper still feels like the complete historical closure of a research program rather than the minimal article forced by one decisive theorem.

I would seriously consider splitting the material:

- one paper on global additive normalization and clock/recovery geometry;
- one paper on intrinsic semialgebraic singular moduli and stochastic rank-loss intersections;
- perhaps a separate paper on the common-flag/constrained matrix-polynomial perturbation theory.

If the authors insist on a single article, then the appendices should be aggressively reorganized around dependency rather than revision history. The current v89/v90/v91/v92/v93/v94 source lineage is reasonable repository provenance, but it should not be visible in the mathematical architecture of a final top-journal submission.

## 10. The composed-jet theorem is useful but does not solve the hardest singular case

The manuscript correctly restricts Theorem “Composed-jet formula” to an analytic chart with positive cells and injective derivative J.

Within that regime the formula is explicit and the finite cutoff argument is clean.

But note what this means for the overall story.

The one place where the paper can compute the Newton edge from ordinary finite jets is the place where the observation map is already locally immersed. The singular rank-loss example, where the ambient Jacobian is not injective, is not computed by this theorem. It falls back to the abstract full-germ envelope theorem plus a bespoke proof.

Thus the paper still lacks an explicit finite jet or local-algebra formula at the singular observation points that motivate the title.

I would not call this a flaw if the manuscript were presented as “a general definable asymptotic theorem plus one example.” I do regard it as a limitation relative to the stronger “intrinsic Newton geometry” framing.

A decisive next step would be a singular-chart theorem: after a semialgebraic stratification or a resolution of the observation map, compute alpha_P from finitely many valuations of the composed cluster coefficients and the observation ideal. That would turn the present structural theorem into an actual singular Newton principle.

## 11. The stochastic example depends essentially on an inequality boundary, and the paper should say more about that

The example deliberately has an endpoint root. The paper does disclose this.

The endpoint is not cosmetic. It supplies the sign restriction h_c(0)<=0 and therefore contributes to isolating the real-rooted pencil.

This raises a natural structural question: is the identifiability mechanism fundamentally a **boundary** phenomenon?

The paper should test at least the following variants:

- move the endpoint root slightly into (0,1);
- perturb the relation s=2r/3;
- allow a small rank-two perturbation of U;
- perturb the clocks;
- perturb V and alpha;
- change the degree while keeping one rank defect and one multiple-root defect.

Some of these perturbations will remove the singularity; that is fine. What matters is to identify which geometric conditions preserve an analogous isolated admissible intersection.

Without this analysis, it is difficult to decide whether Theorem v94 is the first case of a robust theory or a single algebraic coincidence.

## 12. The local minimax result remains an anchored oracle-neighbourhood statement

Corollary “The intrinsic local risk exponent” is mathematically consistent with the v92 theorem, and the scaling N^{-alpha_P} for squared loss follows from t_N=cN^{-1/2}.

But the statistical interpretation should remain narrow.

The decision problem is over a shrinking Hellinger ball centered at a fixed known datum P, and the trivial upper bound may use a constant decision chosen from that local target set. This is a valid local minimax experiment. It is not a globally adaptive estimator, not an honest confidence procedure over the whole model, and not an algorithm for learning the unknown singular stratum.

The manuscript usually says this correctly, but the abstract phrase “the same exponent determines the squared minimax risk” can be read more broadly than the theorem.

At a top-four level, either keep the statistical statement explicitly local-oracle throughout, or add an adaptive theorem that estimates the local stratum/scale without knowing the center.

## 13. The “finite description” statement should be formalized if it is to carry conceptual weight

Theorem v94 states that for real algebraic input the exponents, limiting coefficient set, and variational diameter admit finite descriptions by real quantifier elimination and algebraic branch analysis.

I believe this is plausible.

But if this statement is intended to answer the criticism that the envelope definition is nonconstructive, it is too informal.

The paper should specify:

- the exact finite input encoding;
- which parameters are assumed algebraic;
- how the cluster factors are represented;
- how rational powers t^{p/q} are encoded semialgebraically;
- how C_0 is obtained as a definable closure fibre;
- how complex root multisets and the finite permutation bottleneck metric are encoded over the reals;
- what the output representation of C_P is;
- whether the procedure yields a defining formula, an algebraic number, or only an optimization problem with algebraic data.

No complexity bound is needed. But a theorem claiming effective finiteness should state what is effectively produced.

## 14. The new main theorem should separate three levels of “exactness”

The manuscript now uses “exact” in several distinct senses:

1. the exponent is an exact asymptotic exponent;
2. C_P is the exact leading diameter constant for the abstract germ;
3. finite symbolic diagnostics verify exact polynomial identities.

These should be kept terminologically separate.

For the principal stochastic example, only item 1 is concretely identified as 1/2. Item 2 exists by the general theorem but is not evaluated. Item 3 is computational regression evidence, not mathematical exactness of the theorem.

I suggest reserving “exact leading constant” for cases where the limiting fibre has actually been characterized, and using “variational leading constant” otherwise.

## 15. Smaller mathematical and expository requests

### 15.1 State the coefficient norm once for all new v94 lemmas

The stochastic pencil lemma uses ||p-h_c||_coef. The main paper has several coefficient norms from inherited sections. Specify the finite-dimensional norm and note norm-equivalence if the choice is immaterial.

### 15.2 Clarify the determinant degree in the composed-jet theorem

The assumption that the leading matrix is invertible implies that det M(x,z) has fixed degree locally. State this directly before the cluster argument so no reader worries about roots escaping to infinity.

### 15.3 Make the semialgebraicity of local cluster coefficients explicit

The proof says the cluster coefficients are analytic and semialgebraic because factorization is locally unique. Add one sentence invoking the semialgebraic implicit-function/unique-choice principle, rather than deriving semialgebraicity only from analytic inversion.

### 15.4 State why zero belongs to C_0

It is because every observation ball contains an exact-fibre representative whose spectral polynomial is A_0. This is obvious once said, but it is used in the positivity argument for C_P.

### 15.5 Separate whole-model and pointed notation consistently

The definition allows a pointed compact local X as an alternative. In later statements, add a superscript or a phrase whenever X is not the full closed model. The paper is now careful conceptually; the notation should enforce that care.

### 15.6 Do not let repository provenance leak into theorem presentation

The final PDF should not read like a sequence of historical revision repairs. The v94 source organization can remain in Git, but theorem references and appendix labels should describe mathematics, not version ancestry.

## 16. Reproducibility and source audit

The v94 provenance machinery is stronger than in earlier revisions.

Positive points:

- the revision branch has a workflow with no restrictive path filter;
- the verifier checks runtime HEAD against GITHUB_SHA;
- the manifest records the active input graph;
- inherited active v93 source identities are compared against the controlling review commit;
- changed or removed inherited paths are rejected;
- new-source SHA256 values are checked;
- the workflow compiles the complete manuscript and searches the log for undefined references, duplicate labels, and overfull boxes;
- artifacts are named by actual commit SHA;
- the authors explicitly refuse to equate queued or failed CI with a successful build.

At exact reviewed head 5e01e5a2d6e93ef4c1e2619707608626fdc0f6cf, however, the native workflow remained queued during this review. Therefore the only execution evidence currently available in the branch itself is the stated six finite diagnostic groups and the eleven-page core-only typesetting check.

I do not regard this as a reason for mathematical rejection. It simply means the exact-head full build and audit were not independently available when this report was written.

## 17. What would materially change my recommendation

A further revision would need more than additional examples, diagnostics, or prose.

Any one of the following would materially change the top-four assessment.

### Option A: singular-germ finite Newton data

Prove a theorem that computes the intrinsic exponent on a nontrivial class of singular observation germs from finite algebraic data before solving the full observation-ball optimization.

For example: a monomialization/resolution theorem for the observation-spectral map, a valuation formula, or a finite ideal/module invariant whose slopes give alpha_P and whose initial set gives C_0.

### Option B: classify a family of identifiable stochastic intersections

Generalize the cubic theorem to a stable family or a complete low-dimensional classification. State necessary and sufficient conditions for singleton spectral fibre at rank-loss/multiplicity intersections and derive the intrinsic exponent from those conditions.

### Option C: compute the flagship leading constant

Determine C_0 and C_* explicitly for the cubic rank-loss example, ideally with a proof identifying all extremizing admissible arcs.

This alone would not fully resolve the breadth objection, but it would demonstrate that the new exact-constant theorem has concrete force.

### Option D: prove a local-to-stratified theorem

Construct a finite semialgebraic stratification of the closed stochastic model on which the intrinsic exponent and leading fibre admit uniform formulas or finite candidate lists. This would convert the present pointwise theory into an organizing theorem for the model.

### Option E: substantially narrow and sharpen the article

If the authors do not pursue A-D, then I recommend targeting a specialist venue and rewriting the paper around the strongest proved contribution: the intrinsic semialgebraic root modulus plus the identifiable rank-loss cubic example. Many inherited global and flag results could move to separate papers.

## 18. Bottom line

Revision 94 is a real mathematical advance over revision 93.

The previous central objection — that the paper’s sharp local invariant lived only on an affine rational slice and therefore did not classify the nonlinear stochastic germ — has been answered at the level of an exact semialgebraic germ theorem. The metric-transport defect has been fixed. The paper also supplies a genuine whole-model stochastic point where channel-rank loss, repeated roots, and an active inequality constraint intersect while the aggregate spectral target remains identified.

I therefore do **not** base this report on a discovered fatal counterexample.

My negative recommendation is instead about what the theorem now amounts to at the stated venue level. The most general singular result is still an exact decomposition in terms of optimized coefficient envelopes; the explicit finite-jet formula applies only to immersed observation charts; and the singular stochastic application is one tuned binary cubic example whose leading constant is not actually computed. The work demonstrates a phenomenon and gives a correct-looking abstract language for it, but it does not yet provide the classification theorem that would make the new language unavoidable.

For a four-leading-general-mathematics-journal submission, I would want the next revision to turn “the full admissible germ has an exact definable Newton asymptotic” into “a broad, explicitly described class of stochastic singularities has a computable intrinsic Newton invariant.”

Until that step is present, my recommendation remains **reject at the stated level, while encouraging resubmission after a theorem-level singular classification rather than another incremental closure round**.
