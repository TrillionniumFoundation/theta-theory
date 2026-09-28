# Independent harsh referee report on A2 revision 82

**Manuscript:** *Action rigidity with selective detection*  
**Author:** Qian Qi  
**Review date:** September 18, 2026  
**Reviewed revision branch:** `revision/a2-v82-selective-detector-rigidity-2026-09-18`  
**Mathematical source commit declared by the revision:** `80133d376cc28cc8f2555f58324a3285f9dcfb67`  
**Inherited v81 source head:** `8315577eeb8dcc711c4c1c89fc804d132be2e52e`  
**Controlling earlier harsh report:** `reviews/a2-v80-calibrated-records-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md`  
**Principal new source:** `papers/A2-v17-boundary-information-coarsening/article/v82/principal.tex`  
**Requested standard:** the level expected of *Annals of Mathematics*, *Inventiones Mathematicae*, *Acta Mathematica*, or the *Journal of the American Mathematical Society*.

This is an author-requested independent referee-style report, not a commissioned journal report and not an editorial decision. I have read the v82 principal source, its front matter, the response to the v80 report, the proof/source ledger, the review-ready entry, and the v80 controlling report. I also compared v82 to the immediately preceding v81 branch at the repository level.

The correct high-level assessment is now substantially different from the v80 report:

1. v82 genuinely attacks the strongest v80 structural objection rather than merely adding another calibrated layer;
2. I do not find a short algebraic counterexample to the five-deadline selective-detector theorem or its scalar rigidity mechanism;
3. nevertheless, I would still not recommend the paper at the requested top-four general-journal level in its present form;
4. the remaining blockers are now concentrated in the stability/globalization proof, the geometry/application bridge, the naturality and depth of the observation class, and the overall theorem hierarchy.

My recommendation is therefore negative at the requested venue level, but for materially different reasons from v80.

---

## 1. Recommendation

**Recommendation at the four-leading-general-journals level: reject in the present form.**

Revision 82 is a mathematically meaningful improvement. It removes the calibrated finite catalogue and true-component audit from the new principal theorem. It allows an unknown visible component count, endpoint-dependent uncalibrated readout channels, projective loss of total mass, branch-selective deadline dependence, and action coincidences separated by detector rates. The five-value scalar lemma is a real exact identification result, not a cosmetic restatement of the v80 raw affine inversion.

The paper therefore deserves credit for moving the principal result into a genuinely more intrinsic multi-view latent observation model.

However, the top-four case still fails for four reasons.

First, the genuinely new part of the main theorem remains a finite-dimensional scalar interpolation/identifiability mechanism placed after a classical multi-view spectral decomposition. The mathematics is clean, but the present manuscript does not yet establish that this mechanism constitutes a sufficiently deep or broadly inevitable rigidity principle for a top general journal.

Second, Proposition `prop:v82-stable` does not yet justify the full global (C^m) stability claim as stated. The proof establishes local smooth inverses on fixed minor/eigenvalue/anchor charts, but the passage from these local quotient-valued inverses to one globally labelled, gauge-fixed Lipschitz reconstruction under off-model perturbations is too compressed. The sentence that “fixed smooth gluing functions combine the local extensions” hides the principal compatibility problem.

Third, the return-dynamics corollary still assumes essentially all of the difficult global phase-domain information needed to turn recovered local generating sheets into full powers and then into the target lift. V82 solves an important local latent-sheet identification problem, but it does not solve the hard global coverage/root problem. The paper's strongest geometric conclusion therefore remains conditional on a supplied phase cover for the relevant powers and inverse factors.

Fourth, the integrated article still contains too many historically accumulated companion regimes. The new v82 core is much sharper than the full inherited submission. At top-four level the paper needs to become one theorem with several forced consequences, not an archive in which a new theorem is prepended to a long sequence of earlier observation models.

For a strong specialist journal I would regard v82 as substantially more competitive than v80, provided the stability/globalization issue is repaired and the scope is sharply focused. For the requested four general journals, I would require a further conceptual theorem, not merely another revision round.

---

## 2. What I checked

The principal v82 mechanism is

[
M_j
=
U,operatorname{diag}!left{
a_b e^{kappa_b T_j}(T_j-W_b)
ight}_{b=1}^B V^{mathsf T},
]

observed only projectively through

[
P_j
=
rac{M_j}{mathbf 1^{mathsf T}M_jmathbf 1}
=
Uoperatorname{diag}(pi_{j,b})V^{mathsf T}.
]

The new proof has four main stages:

1. rank of (P_1) identifies the full-rank visible component count;
2. two reduced operators (K_2,K_3) identify common rank-one latent projectors when the pairs ((W_b,kappa_b)) are distinct;
3. component log-ratios reduce the problem to
   [
   A+KT+log(T-x)-log(T-y);
   ]
4. five deadlines identify an unequal-action anchor globally, after which three deadlines identify every remaining action relative to that anchor.

I checked the algebraic identities used in the reduced-operator construction and the component-matrix formula. I also checked the logic of the five-value root-sum argument: after differentiating the difference of two candidate log-ratios, multiplication by the four-pole denominator gives a quartic with the same cubic coefficient as the denominator when the affine slope difference is nonzero. Four Rolle zeros all lie above (T_1), whereas their sum would be (x+y+widetilde x+widetilde y<4T_1), giving the advertised contradiction. I do not see an immediate defect in that argument.

I likewise do not see a short contradiction in the polynomial-degree extension. The degree count in the repeated-Rolle argument is consistent with the claimed sufficient number of clocks.

This report should therefore not be read as alleging that the v82 core is obviously false. The main objections below concern what is proved globally, how stable reconstruction is defined, how the local information theorem becomes geometry, and whether the resulting theorem hierarchy reaches the requested editorial level.

---

## 3. Major positive advance over v80: the hard catalogue/audit objection is genuinely addressed

The strongest v80 criticism was that the scientific-label robustness theorem still assumed a finite exhaustive catalogue and a true-component audit in calibration. V82 does not merely rename that model.

The new principal theorem instead learns the visible rank (B) directly from (P_1), reconstructs the latent component matrices from two uncalibrated independent readouts, and derives the action parameters from their clock trajectories. This is a genuine unsupervised finite-mixture identification statement inside the declared full-rank multi-view model.

This matters. In particular, the following v80 objections are no longer fair descriptions of the v82 headline result:

- “the component count is supplied”;
- “the true finite catalogue is supplied”;
- “ground-truth component audits are needed for the main inverse”;
- “the readout channels are calibrated”;
- “absolute mass must be measured”.

The new theorem removes all of those from the principal observation model.

That is a substantial improvement, and any future referee report should acknowledge it explicitly.

---

## 4. Major concern: the global (C^m) stability statement is not yet fully proved in the form stated

This is the most important theorem-level issue I found.

Proposition `prop:v82-stable` claims that, after local permutation and gauge choice, the inverse extends to a neighborhood of the exact normalized matrix data and obeys a global (C^m) Lipschitz estimate. The proof establishes several correct local facts:

- inversion of a fixed nonsingular minor is smooth;
- one can select a separating finite linear combination with a quantitative eigenvalue gap on a local chart;
- simple eigenvalues and projectors vary smoothly there;
- the scalar anchor map has a nonsingular local Jacobian;
- remaining actions have a local three-coordinate inverse.

The unresolved point is the transition from these local chart inverses to one globally meaningful reconstruction of labelled component functions on (Q) for perturbed data.

### R82-M1. “Smooth gluing functions” do not by themselves solve permutation and gauge compatibility

On exact model data, two local reconstructions agree on an overlap after a permutation and relative-gauge transition. For perturbed data, the proof explicitly concedes that the outputs need not satisfy the exact latent-model identities.

At that point, two independently extended local inverses generally do **not** agree exactly on overlaps. They are only close to the true quotient class.

A partition-of-unity average of locally labelled action vectors is not invariant under a changing permutation. A partition-of-unity average of gauge-dependent relative coefficients is likewise not intrinsically defined until the transition data have been fixed coherently.

The proof needs one of the following:

1. a globally specified label-selection and gauge-fixing algorithm with quantitative overlap consistency;
2. a stability theorem stated in an explicit quotient metric modulo the finite permutation group and continuous gauge, avoiding global labels;
3. a covering/continuation argument proving that local labels can be propagated uniquely from one base chart under the uniform pair-separation margins, together with quantitative bounds for noisy continuation;
4. a global spectral object whose projectors are defined without chartwise changes of the separating linear combination.

The current proof does not provide any of these in sufficient detail.

### R82-M2. The norm in the conclusion is not quotient-invariant

The estimate is written as

[
|widehat W-W|_{C^m}
+
|widehat U-U|_{C^m}
+
|widehat V-V|_{C^m}
+
|widehat A-A|_{C^m}
+
|widehat K-K|_{C^m}
le C|widehat P-P|_{C^m}.
]

But the theorem simultaneously says that the exact inverse is only determined up to permutation and gauge.

Therefore the statement must specify exactly how the representative on the left is selected. “After a local permutation and gauge choice” is not enough for a norm over all of (Q). If the intended norm is an infimum over global permutations and admissible gauges, state that. If the intended representative is obtained by continuation, construct it.

### R82-M3. Chart changes of the separating operator need quantitative transition control

The proof selects (K_2+tK_3) from a finite set, with (t) possibly different on different subcharts. This is fine for exact local identification. It is not automatically a global smooth reconstruction operator under perturbation.

The authors should show that projectors reconstructed using two valid choices (t,t') remain quantitatively aligned on overlaps and that the alignment can be chosen consistently through order (m). Exact equality on the model is not by itself a proof of a globally Lipschitz off-model extension.

### R82-M4. The theorem should separate local stability from global atlas stability

The local inverse theorem is strong and, in my view, credible.

The global statement should be split into:

- a **local labelled/gauge-fixed inverse** on one quantitative chart; and
- a separate **global continuation theorem** on a simply connected gate under a uniform separation margin.

That separation would make the proof auditable and would likely remove the present gap.

Until this is repaired, I would not accept the full stability theorem as proved in its current form.

---

## 5. Major concern: the exact theorem identifies a quotient, but the manuscript sometimes speaks as though it has produced a canonical component atlas

The exact theorem correctly states a simultaneous permutation ambiguity. The model also has a common multiplicative/exponential gauge.

This is mathematically appropriate.

However, later geometric prose comes close to turning the recovered unordered component family into a canonical cross-gate atlas without enough discussion of the residual discrete topology.

The base domain (Q) is a compact rectangle, so one can plausibly trivialize the finite covering defined by pairwise-distinct parameter tuples. But that argument should be made explicitly.

### R82-M5. Prove the global permutation statement as a covering/trivialization result

The sentence

> “Since distinct parameter pairs cannot exchange continuously, two continuous global representations differ by one constant permutation on the connected gate.”

is too quick as a general principle. On a merely connected parameter domain, unordered distinct points can have nontrivial monodromy. What saves the present theorem is the stronger topology of the stated domain (Q), not connectedness alone.

The paper should use the fact that (Q) is a rectangle (hence contractible/simply connected), or state the needed triviality hypothesis directly.

This is not a fatal issue for the theorem on a rectangle, but the proof should not attribute the conclusion merely to connectedness.

---

## 6. Major concern: the return-dynamics corollary still assumes the hard global phase information

Corollary `cor:v82-return` is the bridge from the new information theorem to dynamics.

Its assumptions include:

- finite families of regular endpoint gates for each iterate;
- actual generating sheets on those gates;
- phase graphs covering all domains required by a fixed Bézout word;
- inverse factors also covered;
- fixed collars and regular mixed derivatives;
- the assertion that these sheets belong to the same deterministic lift.

Under those assumptions, recovery of the local generating functions does indeed give local canonical graphs, and the group identity can reconstruct the target lift.

But the assumptions contain much of the difficult global inverse geometry.

### R82-M6. V82 solves local sheet discovery, not global phase-cover discovery

This distinction should become the central scope statement of the geometric theorem.

The new contribution is that, **within each already valid regular gate**, the component count, readout channels, and local sheet actions are learned from projective selective-detector data.

The theorem does not discover:

- which finite collection of gates covers the relevant phase domain;
- whether the observed sheets exhaust a full iterate;
- whether the required inverse-factor domains are present;
- whether a global section exists;
- whether unobserved folds/caustics obstruct continuation;
- whether the local sheets are sufficient to define the required powers globally.

Those are not minor details. They are exactly the global problems that often make inverse dynamics hard.

### R82-M7. “No supplied cross-gate pairing” is weaker than a global unmarked rigidity theorem

The paper is correct that one need not carry semantic component labels from gate to gate once the canonical graphs themselves are reconstructed.

But this should not be advertised as if the entire global branch problem disappeared. The phase cover and iterate organization are still supplied as hypotheses.

At top-four level, I would want a theorem that either constructs the cover from a natural observation process or proves that no weaker global data can suffice.

---

## 7. Major concern: the selective-detector family is identifiable, but its naturality and necessity are not yet mathematically compelling enough

The principal theorem assumes branchwise log-affine detector dependence in the clock:

[
e_b(T,z)propto e^{kappa_b(z)T}.
]

The polynomial extension assumes a fixed a priori degree bound.

These are valid finite-dimensional nuisance families. The paper also correctly proves that arbitrary branchwise deadline dependence can compensate action changes.

The missing issue is why these particular families are the right structural boundary for the geometric problem rather than convenient interpolation classes.

### R82-M8. The main theorem currently reads as finite-dimensional nuisance separation

At a top general journal, I would want a structural characterization such as:

- a maximal detector class for which action is identifiable;
- an invariant criterion on the detector family equivalent to identifiability;
- a sharp clock complexity theorem for a broad Chebyshev/T-system class;
- a classification in terms of finite-dimensional exponential-polynomial spaces;
- a necessity theorem showing that the proposed family arises from a natural apparatus model.

The present result proves a strong theorem for log-affine and polynomial-log families, but it does not yet reveal the general principle governing those examples.

### R82-M9. The polynomial extension is technically useful but conceptually too close to interpolation counting

The proof is repeated Rolle plus degree counting after multiplication by a pole denominator. This is clean. It is also very close to classical univariate identifiability/interpolation mechanisms.

The paper should explain whether the result is an instance of a more general extended complete Chebyshev system or rational-interpolation theorem. If so, formulate the strongest natural version instead of treating degree (q) as a bespoke extension.

### R82-M10. Clock-count sharpness is incomplete

The paper proves:

- three clocks fail for the log-affine class;
- four clocks give a local anchor inverse;
- five clocks give a global inverse;
- no global optimality of five is claimed.

This leaves a conspicuous gap: is four globally sufficient under an additional monotonicity/order condition? Are there genuine four-clock global ambiguities? Is five optimal on the unrestricted class?

A sharp answer is not required for correctness, but it would materially strengthen the significance of the central theorem.

---

## 8. Major concern: the physical realization is a good model example, but not yet a geometric application of comparable depth

Proposition `prop:v82-shear` is useful. It shows that the assumptions are not empty, includes an action coincidence, uses a fixed source, and realizes distinct detector rates through a phase-dependent survival rate.

I view this as a successful consistency example.

I do not view it as a major geometric rigidity theorem.

### R82-M11. The nonconvex shear is engineered around the algebraic model

The map

[
F(x,p)=(x+p^3-p,p)
]

has explicit branches and explicit action. It is deliberately chosen so that the three-sheet geometry can be written down and checked.

That is perfectly acceptable as an example. It does not establish that the selective-detector theorem resolves a previously difficult natural class of billiards, Reeb flows, or Hamiltonian systems.

### R82-M12. The strongest natural billiard consequences remain inherited and strongly marked

The full integrated revision retains the older marked/reference-atlas billiard framework. The v82 theorem improves the observation layer feeding into that framework, but the paper still does not derive a canonical unmarked billiard invariant from ordinary physical records.

Thus the top-four geometric significance still depends on inherited strong organizational hypotheses.

---

## 9. Major concern: the literature positioning is improved but still too narrow for the precise novelty claim

V82 adds a direct joint-diagonalization predecessor and correctly says that the latent-class spectral mechanism is classical.

That is good.

The remaining novelty is therefore concentrated in the scalar clock-rigidity theorem and its coupling to generating actions.

This part needs a much more adversarial literature comparison.

### R82-M13. Compare against classical rational/exponential interpolation and T-system theory

The functions

[
1, T, log(T-x)-log(T-y)
]

and their polynomial extensions form a very structured univariate family. The proof uses exactly the sign-variation / zero-count phenomenon that underlies classical Chebyshev-system and generalized interpolation theory.

The paper should explain whether the five-value theorem is:

- a new special theorem not covered by standard T-system results;
- a direct corollary of an existing extended Chebyshev framework;
- or a convenient elementary proof of a known identifiability principle.

Without that comparison, it is difficult to evaluate novelty.

### R82-M14. Compare against multi-view latent variable identification more precisely

The paper cites latent-class identifiability, observable operators, and joint diagonalization. It should state exactly what is and is not new relative to standard two-view-plus-covariate or repeated-measurement models.

The novelty is not “recovering latent components from several matrices” in the abstract. It is the specific deadline-parametrized scalar law and the recovery of the affine zero (W_b). That distinction should dominate the introduction.

### R82-M15. Avoid making the application breadth substitute for priority analysis

Exact symplectic maps, Reeb suspensions, billiards, latent mixtures, and nonparametric error propagation appear in one manuscript. Each area has a substantial literature.

A top-four paper cannot carry the priority burden by one or two representative citations per field. The authors need a theorem-by-theorem comparison table that identifies the nearest mathematical result and the precise new conclusion.

---

## 10. Major concern: the integrated manuscript remains structurally overgrown

The review-ready note says the core is ten pages and that the complete integrated manuscript retains many earlier regimes.

That is a warning sign.

The v82 principal theorem is now strong enough to deserve a focused paper. Keeping every inherited conditional, calibrated, convex, marked, statistical, and nuisance theorem active in one submission makes the paper harder to evaluate and weakens its conceptual center.

### R82-M16. The paper should be rebuilt around v82, not merely inherit v81/v80

A top-four article should have a theorem hierarchy roughly of the form:

1. one principal information-rigidity theorem;
2. its sharp obstruction/necessity theorem;
3. a general structural extension;
4. one or two genuinely consequential geometric applications.

Instead, the full entry remains an accumulated revision stack.

The response says this breadth is retained intentionally rather than deleted. I do not regard preservation of historical content as a mathematical virtue in a submission. A journal article is not a repository ledger.

### R82-M17. Companion regimes should move to separate papers or appendices unless logically necessary

In particular, the old calibrated catalogue regime and several conditional-law/statistical companions are no longer logically required to understand the v82 theorem.

Keeping them in the main integrated submission risks making the paper look like a collection of solved subproblems rather than one inevitable theorem.

---

## 11. Technical comments

### R82-T1. State the global topology used for label trivialization

Replace “connected gate” by the actual hypothesis needed for one global permutation, or prove the statement using the contractibility of (Q).

### R82-T2. Define the quotient/gauge metric in the stability theorem

The estimate should either minimize over one global permutation and admissible gauge or provide a canonical representative.

### R82-T3. Separate exact identification from stable noisy identification

The exact theorem is cleaner than the present stability theorem. Give each its own complete proof architecture rather than appending global stability through one gluing sentence.

### R82-T4. Make the local anchor selection algorithm explicit

The second divided difference detects unequal actions exactly. Under noise, specify a quantitative threshold tied to the anchor margin (gamma), and show that the selected pair remains valid on the local chart.

### R82-T5. Clarify how the finite cover is chosen from observable quantities

The proposition assumes a finite gate cover, selected minors, separating combinations, and anchors. Distinguish which are existential proof devices and which form part of a reconstruction algorithm.

### R82-T6. Prove overlap alignment for perturbed projectors

When two local spectral choices produce nearby projectors, give an explicit matching rule and bound it using the uniform spectral separation.

### R82-T7. State whether (kappa_b) themselves are (C^m) bounded or only relative rates are

The model has a common additive rate gauge. All stability assumptions and norms should be written in gauge-invariant relative coordinates.

### R82-T8. Tighten the polynomial theorem's gauge language

Because constants in the detector polynomial are absorbed into (a_b), specify whether the “common degree-(q) polynomial” gauge includes a constant term or whether that constant is represented separately by the common weight multiplier.

### R82-T9. Distinguish visible-rank recovery from model-order recovery under misspecification

Rank gives (B) exactly only inside the full-rank exact latent model. Under perturbation, the paper correctly invokes singular-value thresholding. Keep this limitation visible wherever “component count is learned” is stated.

### R82-T10. Add a genuine four-clock global analysis

Even a counterexample would improve the paper substantially. The present local/global clock gap is too central to leave unexamined.

### R82-T11. Expand the discussion of two independent readouts

The full-column-rank two-view assumption is the real latent-separation engine. Explain physical situations in which two conditionally independent finite readouts are natural and why their deadline invariance is credible.

### R82-T12. Do not call the detector family “unknown” without immediately saying “unknown within a fixed finite-dimensional clock family”

The distinction is important because the paper itself proves nonidentifiability for unrestricted deadline dependence.

### R82-T13. Make the geometric corollary's supplied information auditable in one table

List separately what is learned and what is assumed:

- gate locations;
- endpoint coordinates;
- iterate identity;
- phase cover;
- inverse-factor cover;
- component count;
- component pairing;
- readout channels;
- actions;
- detector rates.

This would prevent readers from overinterpreting “unpaired sheets”.

### R82-T14. Compile the complete integrated manuscript before declaring the branch review-ready

The review-ready note explicitly says that the ten-page core was built locally but the complete integrated manuscript was not natively built locally. The workflow may later close that gap, but the repository entry should record the actual completed status at the reviewed head.

### R82-T15. Reduce repository-process prose in the mathematical article

Proof ledgers, source graphs, workflow provenance, and historical preservation are useful repository artifacts. They should not influence the mathematical presentation or substitute for a shorter theorem dependency structure.

---

## 12. Assessment of the principal theorem chain

### 12.1 Joint spectral recovery

Within the exact model, the reduced-operator calculation is clean.

The key observation that ((q_{2,b},q_{3,b})) are distinct when ((W_b,kappa_b)) are distinct is correct under the stated clock ordering because the log-ratio has strictly signed second derivative when the actions differ and is nonconstant affine when only the rates differ.

The deterministic finite choice of a separating linear combination is a useful detail.

I regard this part as credible and appropriately attributed to classical latent/spectral ideas.

### 12.2 Five-value scalar rigidity

This is the strongest new mathematical nugget in v82.

The root-sum contradiction is elegant. It gives global uniqueness from five values without a genericity assumption or nonlinear optimization theorem.

The paper should make this lemma the conceptual center and then generalize it to the natural function-system class in which it belongs.

At present it is convincing as a theorem but not yet positioned convincingly as a top-four theorem.

### 12.3 Anchor recovery

The observable second divided difference is a good device. It removes the need for an externally labelled unequal-action pair.

This is one of the best aspects of the revision.

For noisy stability, however, the thresholding/continuation version must be written out quantitatively.

### 12.4 Polynomial detector theorem

The extension is plausible and the degree count is coherent.

Its weakness is conceptual: it looks like the obvious repeated-Rolle generalization of the log-affine proof. The manuscript should either state the general T-system principle or explain why the polynomial version is the physically canonical endpoint.

### 12.5 Equal-action obstruction

Correct and important.

It demonstrates that distinct detector rates can separate components without recovering a common action offset when all actions coincide. This gives a clean exact boundary to the positive theorem.

### 12.6 Three-clock ambiguity

The implicit-function argument gives a real local nonidentifiability mechanism.

Again, the missing piece is the four-clock global question.

### 12.7 Return reconstruction

Correct in spirit under its strong domain hypotheses.

The novelty lies in having recovered the local generating sheets from weaker observations, not in the Bézout identity itself.

The manuscript says this, which is appropriate.

---

## 13. What would materially change my top-four assessment

Another revision that only strengthens constants, adds examples, expands the response ledger, or adds another detector polynomial degree will not change my recommendation.

One of the following would.

### Path A. A general detector-family classification

Replace the log-affine/polynomial examples by a theorem characterizing the finite-dimensional function spaces for which the action zero is globally identifiable from finitely many projective clocks.

A Chebyshev-system or variation-diminishing classification with sharp clock complexity could become a broad theorem in its own right.

### Path B. Close the four-versus-five global gap

Prove five clocks are globally optimal, or characterize exactly when four suffice. A sharp theorem here would substantially increase the depth of the scalar rigidity result.

### Path C. Prove a global noisy quotient inverse

Build a complete stability theory modulo permutation and gauge, with a globally defined reconstruction map on a neighborhood of the model manifold. This would turn the current local calculations into a genuine geometric inverse theorem.

### Path D. Discover the phase cover from observations

Replace the supplied finite phase-graph cover in the return corollary by an intrinsic acquisition rule with a proved finite stopping/coverage theorem on a nontrivial class.

That would attack the remaining hard global geometry directly.

### Path E. Recover through folds or caustics

Extend the local generating-sheet theorem beyond regular type-I graphs, with an intrinsic treatment of branch birth/merger or caustic crossing.

This would be a substantial geometric advance rather than another observation-model refinement.

### Path F. Obtain a natural billiard/contact theorem with weaker marks

Use the new latent-sheet machinery to remove a genuinely important reference-atlas, semantic mark, or phase-coverage assumption from a natural rigidity theorem.

### Path G. Prove necessity of the remaining global hypotheses

If the phase cover, independent second readout, or finite-dimensional detector restriction is unavoidable, prove sharp counterexamples. A necessity theorem can be as valuable as another positive reconstruction theorem.

---

## 14. Venue-level assessment

### Correctness

**Exact v82 algebraic core:** credible on the inspected scope; I found no short fatal contradiction.

**Global stability theorem:** not yet complete in its present form because quotient/permutation/gauge compatibility under off-model perturbation is not fully proved.

**Return-dynamics consequence:** credible under the explicit phase-cover and regularity hypotheses, but those hypotheses are strong.

**Inherited full manuscript:** not re-certified line by line in this review.

### Novelty

Substantially improved relative to v80. The principal theorem is no longer calibrated deconvolution plus an affine raw inverse.

The new scalar rigidity lemma and its coupling to uncalibrated multi-view latent recovery are genuinely interesting.

The novelty case is nevertheless incomplete without a sharper comparison to classical interpolation/T-system theory and latent multi-view identification.

### Depth

The deepest remaining issue is that the local observation theorem is stronger than the global geometric theorem. The latter still assumes the difficult phase organization.

The detector extension is currently finite-dimensional interpolation rather than a structural classification.

### Breadth

The repository contains remarkable breadth, but the submission remains too broad for its logical core.

The v82 theorem should be allowed to dominate the paper rather than coexist at equal weight with many historical companion regimes.

### Recommendation by venue

- **Annals / Inventiones / Acta / JAMS:** reject in present form.
- **Strong specialist journal:** potentially publishable after a serious stability/globalization repair and a major restructuring of scope.
- **Future top-four submission:** should be driven by a new structural/global theorem of the kinds listed above, not by another incremental revision number.

---

## 15. Final referee statement

Revision 82 is a genuine mathematical advance over revision 80.

The strongest earlier objection—that the paper had moved the hard branch problem into a finite catalogue, calibrated confusion matrix, and ground-truth audit—has been answered for the new principal theorem. The visible component count is learned, the channels are uncalibrated, total mass may be lost, detector response may be branch-selective, and action crossings are permitted. This is not cosmetic progress.

The central five-value lemma is elegant, and I do not find a short algebraic defect in it. The joint spectral stage is standard in spirit but is used appropriately. The equal-action obstruction and the three-clock ambiguity give the positive theorem a meaningful boundary.

The reason I still recommend rejection at the requested four-general-journal level is therefore narrower and more demanding than before.

The paper has not yet converted its strong local information theorem into an equally strong global geometric rigidity theorem. The stability proof does not fully resolve permutation/gauge compatibility for noisy data across charts. The return corollary assumes the phase coverage needed to assemble the powers and inverse factors. The detector family is identifiable because it belongs to a fixed finite-dimensional clock space, but the manuscript does not yet characterize the general structural boundary of that phenomenon. The polynomial extension reads as interpolation degree counting rather than a final conceptual theorem. The complete article also remains burdened by too many inherited companion regimes.

In short: **v82 is now mathematically serious enough that the main obstacle is no longer an obvious observation-model oracle. The remaining obstacle is to turn the local selective-detector identification theorem into a globally intrinsic, structurally classified rigidity theorem of unmistakable general significance.**

Until that happens, I would not recommend publication in *Annals*, *Inventiones*, *Acta*, or *JAMS*.

**Final recommendation: reject at the four-leading-general-journals level in the present form; major conceptual revision required for a future top-four submission.**
