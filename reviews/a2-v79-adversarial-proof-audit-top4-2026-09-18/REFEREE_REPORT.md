# Adversarial external-referee proof audit of A2 revision 79

**Manuscript:** *Clocked action reconstruction: robust quotients and convex twist suspensions*  
**Author:** Qian Qi  
**Review date:** September 18, 2026  
**Reviewed revision branch:** revision/a2-v79-robust-clock-quotient-contact-suspension-2026-09-17  
**Reviewed revision head:** a0c5b0329141d73ded1cb2ea68d0c71a7c5863e9  
**Parent / controlling previous review head:** f9de5e1e471df61f5ac02718d0c7b18b2e7d955e  
**Principal source:** papers/A2-v17-boundary-information-coarsening/rigidity_v79.tex  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This report is an owner-requested, AI-assisted external-referee-style audit. It is not a journal-commissioned report and it is not an editorial decision. I have deliberately treated the requested venue standard as severe: correctness is necessary but far from sufficient, and a technically correct chain of inverse constructions is not by itself evidence of top-four conceptual significance.

This is a fresh adversarial audit of the substantive v79 branch. I have also read the two existing v79 review branches in the repository. One of them concerns the nominal v79 branch that was only the old v78 review head and therefore has a provenance blocker; that objection does not apply to the substantive branch reviewed here. The other is a genuine harsh review of the substantive v79 source. I do not simply reproduce that report. I independently rechecked the main algebraic inversions, the quotient construction, the statistical lower-bound mechanism, the convex-twist and contact-suspension chain, the fixed-deadline construction, and the inherited prefix/distance reconstruction on the active input graph.

## 1. Recommendation

**Recommendation at the requested four-leading-general-journals level: reject in the present form.**

This recommendation is not based on a one-line counterexample to the exact core. After adversarial checking, I do **not** find a short fatal algebraic contradiction in the following central exact statements:

1. three normalized clock laws recover the absolute action under a common unknown positive weight;
2. anchored log contrasts identify the ambient observation quotient by common reweighting;
3. on a nondegenerate two-anchor chart, the quotient admits the stated global action/residual split;
4. the exact clock-dependent nuisance confounding family has the displayed logarithmic form;
5. the declared nonparametric action-risk rate has a plausible and essentially correct upper/lower-bound mechanism;
6. the globally uniformly convex negative-twist class gives a genuine single-valued exact symplectic twist map and unique finite stationary actions;
7. the contact suspension realizes the positive action roof as an actual Reeb return time;
8. fixed class-dependent gates and deadlines recover the two consecutive generating actions and hence the one-step generator on a prescribed compact square;
9. the inherited marked billiard prefix-cancellation and finite distance-certificate chain is internally coherent under its strong branch and atlas hypotheses.

However, I find one theorem-level proof-completeness problem that should be repaired before the quantitative convex-suspension theorem is stated in its present form, and several remaining conceptual/modeling obstacles that are decisive at the top-four level.

The most important technical issue is:

> **The exact part of Theorem 10.3 is substantially supported, but its claimed uniform finite-order Lipschitz stability is not proved at the level of precision stated.**

The proof currently invokes “bounded finite-order derivatives,” “bounded next derivatives,” implicit differentiation of stationary minimizers, a common root collar, and composition estimates without specifying the derivative budget or proving a standalone uniform stationary-action regularity proposition with constants. At a specialist-journal standard I would require this claim to be made fully auditably quantitative or weakened.

The most important structural issues are:

- the contact construction removes literal circularity but still encodes the unknown action into the return roof by construction;
- the robust finite-record billiard theorem permits missed classifications but forbids false-positive branch labels, so it is not robust to the branch mixtures that are statistically most dangerous;
- the whole-table billiard theorem remains strongly marked and reference-atlas dependent;
- the statistical minimax theorem is useful but much of its stochastic difficulty is inherited from standard density-derivative estimation and then transported through a smooth explicit inverse;
- the principal article combines several mathematically different programs without yet producing one theorem whose force genuinely requires the whole synthesis.

Revision 79 is therefore a real mathematical improvement. It is not, in my assessment, a top-four general-journal paper in its current form.

---

## 2. Scope of the audit and provenance

The review is pinned to the substantive revision head

a0c5b0329141d73ded1cb2ea68d0c71a7c5863e9.

The active principal source is

papers/A2-v17-boundary-information-coarsening/rigidity_v79.tex.

I inspected the active v79 files and the inherited files actually input by that source, including in particular:

- article/v79/01_introduction.tex;
- article/v77/02_physical_clocks.tex;
- article/v79/02_information.tex;
- article/v79/03_robust_quotient.tex;
- article/v79/04_statistics.tex;
- article/v79/05_prefix_cancellation.tex;
- article/v79/05_root_free.tex;
- article/v77/04_distance_registration.tex;
- article/v77/05_finite_coverage.tex;
- article/v79/07_convex_suspensions.tex;
- article/v78/04_mechanics.tex;
- article/v78/05_uniform_records.tex;
- article/v79/09_robust_geometry.tex;
- article/v79/references.tex;
- RESPONSE_TO_REFEREE_V79.md;
- PROOF_LEDGER_V79.md;
- BUILD_AUDIT_V79.json;
- verification_v79.json.

The local-build receipt records a clean 35-page build. I regard this only as source/build evidence. A successful TeX build and finite diagnostic scripts are not proof certification and do not affect the mathematical recommendation.

The repository contains another branch named revision/a2-v79-universal-records-stable-quotient-2026-09-17 whose head is the old v78 referee commit f9de5e1e.... That branch is not the revision under review here. The substantive v79 branch is one commit beyond the controlling v78 review and contains the new article material.

---

## 3. What survives adversarial checking

A harsh report should separate genuine mathematical progress from venue-level objections. Several pieces of v79 are clean enough that I would not ask the authors to re-prove them from scratch merely because the top-four recommendation is negative.

### 3.1 Three-clock absolute action recovery

The three-clock algebra remains one of the cleanest components of the paper. With

f_j(z) proportional to a(z)(T_j-W(z)),

normalization constants and the unknown joint multiplier can be eliminated by anchored ratios. The affine relation used in the proof gives an absolute anchor value W(z_0), not merely W up to an additive constant. The second ratio then recovers W pointwise.

The nonconstancy assumption supplies a usable second scalar point. The denominator identities have the right clock-separation factors, and the local C^m stability is the standard stability of evaluation, multiplication, logarithm/reciprocal operations on bounded sets with positive denominator margins.

I do not find a hidden additive gauge after three absolute clocks.

### 3.2 Ambient quotient and Banach coordinate

Proposition 4.1 is mathematically useful and, in my reading, correct.

The common positive reweighting action changes each f_j/f_1 only by a clock-dependent constant; anchoring at z_0 removes that constant. Conversely, equality of all anchored log ratios implies that all components differ by one common positive function plus normalization constants. The explicit exponential section gives a continuous inverse from the Banach contrast coordinate to the quotient.

This is an actual repair of the older quotient-language problem. It also clarifies that the quotient construction itself is an exact-law statement, not a finite-sample sufficiency theorem.

### 3.3 Global split coordinates on a nondegenerate chart

Theorem 4.2 deserves credit. The two-anchor formulas are not merely notation around the old inverse. They give an explicit product chart between:

- the action W; and
- a fixed complementary residual space.

The second contrast determines the functional reciprocal coordinate up to one scalar, and the third contrast at the second anchor determines that scalar. Residuals in the declared normal space leave those determining quantities unchanged, so the inverse identities are transparent.

This part is strong structurally even though its proof is elementary once the correct coordinates are found.

### 3.4 Complete exact nuisance confounding

The formula

eta_j = b + c_j + log((T_j-V)/(T_j-W))

is the correct exact ambiguity family in the declared weighted-action model. It exhibits precisely why arbitrarily many clocks cannot remove a clock-dependent nuisance that is tangent to the action manifold in the appropriate nonlinear way.

This is more valuable than a generic perturbation estimate because it identifies the entire zero-residual ambiguity on the chart.

### 3.5 Statistical action-risk theorem

Theorem 5.2 is not a vacuous corollary of exact identification. It contains a real finite-record statement.

For the upper bound, the C^m density-estimation error has the expected bias/stochastic balance

h^(beta-m) + sqrt(log n/(n h^(2m+d))),

leading to the displayed sup-norm derivative rate at the chosen bandwidth.

For the statistical lower bound, the disjoint bump packing has:

- C^m separation of order h^(beta-m);
- KL divergence per experiment of order n h^(2 beta+d);
- logarithmic packing size of order log(1/h);

so the chosen logarithmic bandwidth scale is consistent with the Fano calculation.

The epsilon lower bound is also legitimate in the **declared abstract nuisance class**: the paper constructs two different actions with exactly identical law tuples by compensating with clock-dependent weights.

I therefore do not object to the theorem as an abstract weighted-action minimax statement. My objection later is to its significance and to any physical interpretation stronger than the theorem proves.

### 3.6 Convex negative-twist dynamics

For the class

lambda I <= D^2 L <= Lambda I,
-L_xy >= b,

the map defined by p=-L_x and q=L_y is indeed globally invertible: for fixed x, y -> -L_x(x,y) is strictly increasing with slope bounded below; for fixed y, x -> L_y(x,y) is strictly decreasing with slope bounded away from zero. The global growth follows from those slope bounds.

The exact symplectic identity is the standard first-variation identity for the generating function. Strong convexity gives unique finite-horizon minimizers. The tridiagonal stationary Hessian has positive determinant and diagonal entries bounded by 2 Lambda, so the cofactor expression gives the stated nonzero mixed derivative lower bound.

I do not see a sign error in the exact twist calculation.

### 3.7 Contact suspension

The deck transformation

G(x,p,z) = (F(x,p), z-r(x,p))

preserves alpha=dz+theta exactly when F^*theta-theta=d ell and r=c+ell. The positive roof makes the integer action proper and prevents earlier positive returns to the section. The Reeb field is the z-translation field, and its first return time is the roof.

Thus v79 really does replace the literal “device evaluates an unknown action threshold” with an elapsed-time observation in a constructed contact suspension.

That is a mathematical improvement over v78.

### 3.8 Exact six-deadline recovery

The exact identification part of Theorem 10.3 is the strongest new deterministic statement in v79.

The proof gives class-dependent but L-independent:

- endpoint gates;
- an initial phase box;
- a positive roof offset;
- an external delay interval;
- three deadlines at return count n;
- three deadlines at return count n+1.

The backward recurrence gives a fixed initial-coordinate range for any terminal pair in the target square. Strong convexity turns the backward stationary path into the unique minimizing path. The action upper and lower bounds make the clock windows uniform. Three laws recover each of S_n and S_{n+1}; initial-covector matching identifies the common prefix; subtraction recovers L(t,v).

I do not find an obvious counterexample to this **exact** reconstruction under the global convexity/twist hypotheses.

### 3.9 Prefix cancellation and distance reconstruction

The inherited billiard cancellation mechanism is also coherent under its strong hypotheses.

At a genuine common-prefix match,

H_s = -U_st^2/B < 0.

The important point is that v79 does not incorrectly claim H_s<0 everywhere. It only uses the negative derivative at every zero, plus determinism ensuring that every zero represents a physical common prefix. The one-dimensional downward-zero lemma then gives uniqueness on the connected initial interval.

Once the final-flight distance kernel is known, the finite Euclidean certificate is a legitimate sufficient condition: cross-difference rank fixes relative bilinear coordinates, the five-equation system fixes the metric/translation parameters, and trilateration recovers the full smooth patches.

The issue at the top-four level is therefore not that these arguments are empty; it is how much marking and reference architecture is supplied to make them work.

---

## 4. Major theorem-level objection: the quantitative part of Theorem 10.3 is not yet auditable

This is the most concrete mathematical revision request in this report.

The exact six-deadline identification theorem is supported. The final paragraph of its proof then upgrades the result to the statement:

> on subclasses with bounded finite-order derivatives ... reconstruction is uniformly locally Lipschitz from C^{k+2} laws to C^k generating functions for every finite k.

That sentence currently compresses several nontrivial uniform estimates into prose.

The proof invokes:

1. implicit differentiation of the minimizing path as a function of endpoints;
2. bounds on derivatives of S_n and S_{n+1};
3. persistence of a common matching root collar;
4. a lower bound for the derivative of the matching equation;
5. “bounded next derivatives” to keep that lower bound on the collar;
6. the clock inverse at a usable anchor;
7. composition with the root map;
8. subtraction to obtain L;
9. an additional perturbation caused by clock-dependent nuisance.

For a qualitative local statement, this is a credible sketch. For the stated **uniform finite-order Lipschitz theorem**, it is not enough.

### R79-A1. State the regularity budget as a function of k

For each target C^k recovery bound, the theorem should specify exactly what uniform derivative bounds are assumed on L.

For example, if the proof needs C^{k+r} control of L on the fixed compact configuration region, state r explicitly. If the source and efficiency enter only the conversion from records to conditional law estimates, say so separately; if their derivatives enter the deterministic law-to-L inverse, specify those orders too.

The phrase “bounded finite-order derivatives” is not a mathematical hypothesis at the precision claimed.

### R79-A2. Prove a standalone stationary-action regularity proposition

The paper needs a proposition of the following form.

For fixed n and fixed compact endpoint/configuration boxes, under:

- lambda I <= D^2L <= Lambda I;
- -L_xy >= b;
- a specified C^r bound for L;

the minimizer map

(s,t) -> (x_1(s,t),...,x_{n-1}(s,t))

has specified C^q bounds, and consequently S_n has specified C^{q+?} bounds, with constants depending only on the declared class parameters.

This should be proved recursively or by a quantitative implicit-function theorem with the inverse Hessian bound recorded explicitly.

At present the manuscript says these bounds follow by implicit differentiation. That is plausible but not yet a proof of the uniform theorem as stated.

### R79-A3. Quantify the common root collar

At the exact root one has a uniform derivative lower bound. To use one fixed collar, the proof needs a uniform bound on the next derivative of the matching function. That bound in turn depends on higher derivatives of the stationary actions.

State:

- the collar radius;
- the derivative order used to control variation of H_s;
- the resulting endpoint sign margin;
- the dependence on n, lambda, Lambda, b, R, and the relevant C^r bound of L.

Without this, “bounded next derivatives make a common collar possible” is a placeholder for the central quantitative step.

### R79-A4. Separate chartwise Lipschitzness from an algorithm with chart selection

The three-clock inverse is locally Lipschitz on a fixed nondegenerate anchor chart. The paper later invokes a finite set of candidate anchors and chooses a usable one.

If the theorem claims existence of a locally Lipschitz inverse, this is fine chartwise. If it claims one explicit reconstruction map that selects the “best” candidate from finite tests, the selection rule must be formulated so that ties and chart transitions do not create an artificial discontinuity.

The clean options are:

- state the stability theorem chartwise on a finite open cover with uniform constants;
- fix a candidate with a strict margin on each neighborhood;
- or give a finite partition/selection rule with hysteresis and prove the resulting map has the claimed continuity.

This is a formulation issue, not a counterexample to exact recovery. It should nevertheless be made precise.

### R79-A5. Scope the nuisance-stability consequence correctly

Theorem 4.4 gives a C^{k+2} action perturbation bound on a fixed chart. Propagating that to a C^k generator requires exactly the root/action derivative estimates missing above.

Therefore the additional O(epsilon) conclusion in Theorem 10.3 should be regarded as unproved at its stated uniform finite-order strength until A1–A4 are supplied.

**Required disposition:** either provide the complete quantitative lemma chain or weaken Theorem 10.3 to exact identification plus a qualitative local-stability statement.

This point alone would prevent me from accepting the theorem exactly as written even at a strong specialist journal.

---

## 5. Major modeling objection: the “robust” billiard theorem excludes the dangerous classification error

Definition 13.1 now charges branch rarity honestly, which is good. But it assumes:

> the apparatus either supplies the exact prescribed word and lift labels or returns failure; there are no false positive labels.

This creates a strong asymmetry.

- False negatives are allowed and paid for through the success probability.
- False positives are forbidden.

Yet a false positive is precisely the error that creates a mixture of branch laws. The paper itself explains earlier that branch mixtures are not removed merely by adding more clocks.

Consequently the finite-record geometric theorem is robust to:

- finite sampling;
- coordinate error;
- small clock-dependent weight misspecification;

but not to even a small amount of branch-label contamination unless that contamination happens to preserve the single-action form.

At top-four level, this is not a minor engineering caveat. The observation convention supplies an exact discrete classifier whose hardest failure mode is excluded.

### R79-B1. Add a controlled-confusion theorem or an impossibility theorem

A materially stronger result would allow a confusion matrix or contamination level tau:

- the accepted sample for branch gamma may contain an O(tau) mixture of specified neighboring branches;
- prove stable recovery under a separation or transversality condition;

or prove a sharp impossibility threshold showing when such mixtures cannot be deconvolved.

Either direction would turn the current caveat into mathematics.

### R79-B2. Do not call exact classification with rejection “robust branch resolution”

The paper is mostly careful on this point, and that care should be preserved. The robust theorem is robust **conditional on exact positive labels**.

### R79-B3. Distinguish acquisition cost from acquisition identifiability

Charging all raw launches answers a cost-accounting objection. It does not prove that the exact word/lift classifier exists from the raw observables.

Those are different mathematical problems.

---

## 6. Top-four significance objection: the contact realization is correct but still engineered around the action

Revision 79 successfully fixes the literal circularity objection to the old threshold experiment. Nevertheless the conceptual problem remains.

The contact suspension is built from the unknown exact symplectic map and its action primitive. Its roof is

r = c + ell.

Therefore the observed dynamical object itself varies with L in precisely the way needed for the elapsed return time to equal the generating action plus a constant.

This is legitimate mathematics. It does not automatically produce a natural inverse problem.

### R79-C1. The experiment is class-wide, but the observed contact system is L-dependent

The settings are fixed across the class, which is an advance. But the underlying contact manifold/form is the suspension associated with the unknown F_L and its action.

The theorem should state this modeling fact prominently, not only explain it after the construction.

### R79-C2. The inverse content should be separated from the classical action-roof mechanism

The deepest deterministic content is not the existence of a suspension with return time equal to action. The inverse chain is:

1. clock laws recover S_n;
2. clock laws recover S_{n+1};
3. the two consecutive generating actions determine L by prefix matching and subtraction.

The paper would be stronger if it isolated step 3 as an independent deterministic rigidity theorem and compared it seriously with the classical theory of generating functions of iterates.

### R79-C3. A natural contact inverse problem would change the assessment

A stronger result would start from a geometric/contact class that exists independently of the desired encoding and show that naturally available return-time data determine the generator.

At present the contact construction is best viewed as a rigorous realization of the clock law, not as an unexpected contact rigidity phenomenon.

---

## 7. Top-four significance objection: the globally convex twist regime is broad in dimension of parameters, but very rigid dynamically

The phrase “arbitrary two-variable function” is literally true inside the class, but it risks understating the strength of the assumptions.

The class has:

- a globally uniformly positive Hessian;
- a globally uniformly negative mixed derivative;
- no competing stationary branches;
- global invertibility of the twist relation;
- unique finite-horizon minimizers for every endpoint pair.

This is an infinite-dimensional class, but it is a particularly well-conditioned dynamical regime.

The theorem becomes conceptually deeper if one weakens this regime while preserving a nontrivial inverse conclusion.

Examples of meaningful directions include:

- finitely many stationary branches with branch transitions;
- loss of global convexity but retention of local twist and coercivity;
- conjugate-point phenomena with a recoverable branch structure;
- a sharp characterization of exactly what fails when uniqueness of the stationary path is lost.

I do not require the authors to solve all of these. I do require the manuscript to avoid presenting “arbitrary two-variable” as if it meant arbitrary generating dynamics.

---

## 8. Top-four significance objection: the marked billiard theorem still receives a large amount of combinatorial structure

The billiard part remains the most ambitious geometric application, but it also remains highly marked.

The observation convention supplies or fixes:

- scalar boundary charts;
- obstacle labels;
- lattice lift labels;
- reflection words;
- branch gates;
- a finite identifying atlas attached to the reference table;
- overlap maps in the scalar label space;
- exact positive branch classification;
- cross-clock source sharing on each branch.

The theorem does recover Euclidean embeddings, lattice vectors, distances, and boundary geometry. Those are genuine unknowns. But the supplied combinatorial architecture is substantial.

### R79-D1. The finite-atlas existence theorem is not a canonical acquisition theorem

For each table, a suitable finite design exists and persists on a neighborhood. This does not produce one intrinsic protocol that works across a broad unknown class.

The manuscript acknowledges this. That acknowledgement is correct and should remain.

### R79-D2. The strongest next theorem is unmarked or partially marked recovery

Any of the following would materially strengthen the paper:

- recover word/lift assignments from mixtures;
- tolerate partial branch labels;
- infer overlap registration without supplied scalar overlap maps;
- prove a canonical adaptive acquisition scheme with finite stopping on a substantial class;
- prove a sharp obstruction showing that some of the supplied marks are mathematically necessary.

Without one such advance, I view the result as a powerful marked identifying experiment rather than a natural-data rigidity theorem.

---

## 9. The minimax theorem is useful, but it does not by itself supply top-four statistical depth

The minimax theorem is one of the best-organized additions in v79. Its scope is also correctly limited to the weighted-action experiment.

The stochastic term, however, comes from a familiar mechanism:

1. estimate several smooth positive densities and their derivatives;
2. take anchored log contrasts;
3. apply a smooth finite-order inverse.

The statistical lower bound is a standard bump-packing construction inside the exact submodel.

The epsilon term is structurally more interesting because it is tied to the exact nonlinear nuisance ambiguity. Even there, the lower bound is generated by an explicitly constructed indistinguishable nuisance pair.

This makes the theorem worthwhile, but not obviously a leading-general-journal statistical theorem.

### R79-E1. Physical realizability of nuisance would materially increase significance

The paper correctly says that the nuisance class is abstract and does not assert that every eta_j arises from a physical billiard perturbation.

A stronger theorem would characterize the tangent/cone of nuisance perturbations realizable by perturbing:

- source preparation;
- retention;
- classification;
- detector response;

while holding the dynamics fixed.

Then one could state a physical identifiability or minimax theorem rather than an abstract weighted-action one.

### R79-E2. Keep the current scope if that theorem is not proved

Do not let later summaries convert “sharp for the declared nuisance class” into “sharp for billiard reconstruction.”

---

## 10. Literature positioning remains below the standard demanded by the breadth of the manuscript

Revision 79 has improved the bibliography substantially. That is not the same as establishing novelty at a top-four level.

The manuscript spans:

- exact symplectic twist maps;
- generating functions and stationary composition;
- discrete variational mechanics;
- contact suspensions and action roofs;
- inverse billiards and marked length/lens information;
- distance geometry;
- nonparametric derivative estimation;
- minimax nuisance confounding.

For such a broad paper, a short list of representative references is not enough. The authors need a theorem-level novelty map.

I recommend a table with columns:

| v79 theorem/mechanism | closest established mechanism | exact hypothesis difference | exact new conclusion | why the difference matters |
|---|---|---|---|---|

At minimum this should be done for:

1. three-clock absolute action identification;
2. Banach quotient and split residual coordinates;
3. two consecutive iterated generating actions determining the one-step generator;
4. action-as-return-time contact suspension;
5. marked whole-table billiard reconstruction;
6. abstract nuisance minimax risk.

The question is not “has the paper cited something in each area?” The question is “what is mathematically new after all classical pieces are subtracted?”

Until that is answered theorem by theorem, a top-four referee cannot reliably assess priority or depth.

---

## 11. The article still contains several different papers and lacks one unavoidable organizing theorem

The principal article contains at least four substantial projects:

1. observation quotient and nuisance geometry;
2. nonparametric action estimation;
3. convex-twist/contact inverse reconstruction;
4. marked billiard whole-table reconstruction.

There is a common device: clocked actions. That is a genuine theme.

But the strongest theorem in one block is not logically needed for the strongest theorem in another block. The minimax theorem does not drive the exact convex-suspension theorem. The convex-suspension theorem does not drive the billiard finite-atlas theorem. The billiard distance certificate does not deepen the Banach quotient theorem.

At a specialist venue, a broad toolkit paper can be acceptable. At a top general journal, breadth must usually produce a conceptual theorem greater than the sum of the components.

Revision 79 has not yet reached that point.

The authors should either:

- formulate one overarching rigidity principle that genuinely subsumes and requires the principal mechanisms; or
- split the material into a quotient/statistics paper and a deterministic inverse-geometry paper, each with a sharper literature position.

Merely adding more applications would worsen this issue.

---

## 12. Detailed technical requests

The following are concrete changes I would require in a serious revision.

### R79-T1. Make Theorem 10.3 exact/stable parts visibly separate

State one theorem for exact recovery under the C^\infty convex-twist class.

State a second theorem for C^k stability under explicit finite regularity assumptions.

This prevents the exact theorem from depending rhetorically on a quantitative paragraph that is not yet fully proved.

### R79-T2. Give the exact derivative budget

For every k, state a concrete r(k) such that a uniform C^{r(k)} bound on L suffices for C^{k+2}-law to C^k-generator stability.

Do the same for any source/efficiency regularity that is genuinely needed.

### R79-T3. Prove quantitative minimizer dependence

Add a lemma/proposition giving bounds for derivatives of the stationary minimizer and S_n. Record constant dependence.

### R79-T4. Prove the root-collar estimate

Do not say only that bounded next derivatives make a common collar possible. Give the inequality.

### R79-T5. Clarify the topology of the stable inverse across anchor charts

State whether the inverse is:

- chartwise locally Lipschitz;
- uniformly locally Lipschitz on a finite cover;
- or one globally defined selected algorithm.

Then prove precisely that version.

### R79-T6. Keep exact-law quotient, finite-sample validation, and physical realization separate

These are three different levels of statement. The manuscript has improved here; maintain that separation in every theorem and abstract sentence.

### R79-T7. State explicitly that the contact suspension varies with L

The deadlines/settings are class-fixed; the contact form/manifold is the one associated with the unknown F_L. Both facts should appear in the theorem statement or immediately adjacent text.

### R79-T8. Avoid “arbitrary two-variable generator” without the class qualifier

Use “arbitrary member of the globally uniformly convex negative-twist class” or an equally precise phrase.

### R79-T9. Do not describe exact positive branch labels as a solved robustness problem

No-false-positive classification is an assumption.

### R79-T10. Give a contamination extension or an explicit nonclaim

If no mixture theorem is added, state in the main robust theorem that any positive false-label contamination is outside its guarantee.

### R79-T11. Keep raw-launch cost and classifier availability distinct

Charging the probability of correct classification is not a proof that the classifier can be constructed from the recorded data.

### R79-T12. Expand the novelty comparison around iterated generating functions

This is the deterministic heart of the convex-suspension inverse. It deserves much more than a generic citation to variational mechanics.

### R79-T13. State constant dependence in all “uniform” bounds

At minimum list dependence on:

n, R, lambda, Lambda, b, A_0, A_1, k, derivative bounds, source floor, efficiency floor, and clock margins.

### R79-T14. Preserve the current honest caveats

The manuscript currently says, correctly, that:

- the minimax theorem is not a billiard minimax theorem;
- the billiard theorem is marked;
- the finite protocol is reference-atlas dependent;
- contact return time is not ordinary time of the unsuspended discrete map;
- exact nuisance confounding is not a construction of noncongruent billiards;
- build/diagnostic checks are not proof certification.

Do not remove these caveats in an attempt to strengthen the presentation.

### R79-T15. Shorten the response-letter logic inside the article

The principal article should read as a theorem-driven paper, not as a sequence of defenses against old reports. Move provenance/build/rebuttal language to revision metadata where possible.

### R79-T16. Give one dependency diagram for the mathematical theorems

A one-page diagram should distinguish:

- exact law algebra;
- statistical estimation;
- abstract generating reconstruction;
- contact realization;
- billiard specialization;
- finite-record geometry.

This would make it immediately clear which conclusions depend on which hypotheses.

---

## 13. What would materially change the top-four assessment

Another round of formatting, numerical diagnostics, or local constant optimization would not change my recommendation. A theorem of one of the following types might.

### Path A. Robust recovery with branch contamination

Allow a small but nonzero rate of false positive word/lift labels and prove stable deconvolution or a sharp threshold.

This directly attacks the weakest point of the current “robust” billiard claim.

### Path B. Canonical or adaptive unmarked billiard acquisition

Replace the reference-table identifying atlas by an intrinsic rule with a finite stopping theorem on a broad class.

### Path C. Physical nuisance geometry

Characterize which clock-dependent nuisances are realizable by physical perturbations of source/retention/classification, then prove sharp identifiability and minimax consequences in that physical class.

### Path D. Consecutive-generating-function rigidity beyond the clock encoding

Prove a standalone theorem that finitely many consecutive iterated generating functions determine the one-step generator under natural hypotheses, with sharp obstructions and a serious classical comparison.

If this theorem is independently deep, the clock experiment becomes a new data-acquisition route to a pre-existing hard inverse problem rather than the central source of identifiability.

### Path E. Recovery beyond global convexity

Permit multiple stationary branches or weaker convexity/twist assumptions and still recover meaningful generator information.

### Path F. Natural contact return-time rigidity

Find a contact/geometric class where the return-time data arise intrinsically, not because the roof was deliberately set equal to the action, and prove reconstruction there.

### Path G. Necessity / impossibility theorems for marks

If unmarked recovery is false, prove sharp counterexamples showing exactly which word/lift/atlas information is indispensable.

A sharp impossibility theorem can be as conceptually valuable as a stronger positive theorem.

---

## 14. Venue-level assessment

### Mathematical correctness

**Exact core:** substantially credible on the inspected scope. I found no short fatal counterexample.

**Quantitative stability:** not fully closed. Theorem 10.3's finite-order uniform Lipschitz claim needs an explicit regularity/constant-propagation proof.

**Finite-record billiard theorem:** coherent conditional on exact positive branch classification, but that assumption is a major limitation of the robustness interpretation.

### Novelty and depth

The v79 additions are genuine:

- global quotient coordinates;
- an exact nuisance classification;
- a two-sided abstract action-risk theorem;
- a class-wide fixed-deadline inverse;
- contact elapsed-time realization;
- better raw-cost accounting.

But the paper still relies on several classical or deliberately engineered mechanisms whose combination has not yet produced a single top-four-level organizing principle.

### Exposition

The manuscript is substantially clearer than earlier versions, especially in its nonclaims. It remains too compressed across multiple research areas to carry the burden of priority and significance expected at a top general journal.

### Recommendation by target

- **Annals / Inventiones / Acta / JAMS:** reject in present form.
- **Strong specialist journal:** potentially interesting after major revision, especially after closing the quantitative stability proof and clarifying the main conceptual center.
- **Resubmission at top-four level:** should be driven by a genuinely new theorem of the kind listed in Section 13, not by another layer of local repairs.

---

## 15. Final referee statement

Revision 79 should be credited as a substantive mathematical revision. It is not a provenance-only repackaging, and it does answer several previous objections.

The quotient is now mathematically defined rather than rhetorical. The off-model residual has an explicit global chart. The nuisance ambiguity is classified exactly. The statistical layer has a real minimax theorem. The contact construction replaces an action-evaluating threshold by an actual elapsed-time return experiment. The convex-twist hypotheses are verified from intrinsic inequalities on an infinite-dimensional two-variable class. The raw billiard preparation cost is accounted for rather than normalized away.

The remaining difficulty is therefore more serious than a list of missing estimates.

First, one quantitative theorem is stated more sharply than it is presently proved: the C^{k+2}-law to C^k-generator uniform stability claim needs an explicit finite-regularity theorem and constant chain.

Second, the robust billiard theorem is robust only after exact positive branch classification. False positive labels, which generate mixtures and are not neutralized by more clocks, are excluded.

Third, the contact inverse is mathematically valid but still obtains its clock from a suspension whose roof is built from the action itself. This resolves implementability; it does not yet create a natural rigidity invariant of comparable depth.

Fourth, the billiard inverse remains strongly marked and reference-atlas dependent.

Finally, the article combines quotient geometry, statistics, contact/twist dynamics, and marked billiard reconstruction without one theorem that mathematically forces these components into a single top-four contribution.

For those reasons my recommendation remains negative at the requested venue level.

**Final recommendation: reject at the four-leading-general-journals level; major conceptual and quantitative revision required.**
