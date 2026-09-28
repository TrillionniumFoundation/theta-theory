# Independent harsh referee report on A2 revision 79

**Manuscript:** *Clocked action reconstruction: robust quotients and convex twist suspensions*  
**Author:** Qian Qi  
**Date:** September 18, 2026  
**Reviewed revision branch:** `revision/a2-v79-robust-clock-quotient-contact-suspension-2026-09-17`  
**Reviewed revision head:** `a0c5b0329141d73ded1cb2ea68d0c71a7c5863e9`  
**Controlling previous referee head:** `f9de5e1e471df61f5ac02718d0c7b18b2e7d955e`  
**Principal source:** `papers/A2-v17-boundary-information-coarsening/rigidity_v79.tex`  
**Requested standard:** the level expected of *Annals of Mathematics*, *Inventiones Mathematicae*, *Acta Mathematica*, or the *Journal of the American Mathematical Society*.

This is an author-requested external-referee-style report, not a commissioned report from any journal and not an editorial decision. I apply the severe standard appropriate to the four leading general mathematics journals. I distinguish mathematical correctness, closure of the previous objections, and top-four significance. Those three questions do not have the same answer.

## 1. Recommendation

**I would not recommend acceptance at the requested top-four general-journal level in the present form.**

Revision 79 is a genuine and substantial mathematical revision. It should not be confused with the separate nominal branch `revision/a2-v79-universal-records-stable-quotient-2026-09-17`, which points to the old referee head and was correctly rejected on provenance grounds in the existing report
`reviews/a2-v79-provenance-blocker-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md`.
The branch reviewed here is different: it is one substantive commit beyond the controlling v78 review and adds a new 35-page principal article, new theorem/proof material, a response, a proof ledger, and a new build/verification package.

The revision also answers several previous objections in a mathematically serious way:

- the ambient quotient of arbitrary positive clocked observations is now explicitly topologized and metrized;
- the exact model is given global split coordinates on a nondegenerate inverse chart;
- small clock-dependent weight errors are treated quantitatively;
- exact action-confounded nuisance is characterized;
- a two-sided action-risk theorem is proved on a specified Hölder class;
- the old action-threshold objection is replaced by a genuine elapsed-time realization in a contact suspension;
- the abstract generating-function hypotheses are verified on a broad class of uniformly convex negative-twist functions;
- the branch-resolution preparation cost is now charged at the raw-launch level;
- the bibliography is materially improved.

I do **not** find a short fatal algebraic error in the core new formulas after auditing the split quotient, the nuisance formula, the nonparametric lower-bound mechanism, the convex-twist cofactor estimate, the contact suspension, the class-wide deadline construction, and the inherited prefix/distance chain.

Nevertheless, the paper still does not establish the level of conceptual necessity, naturality, breadth, and literature separation that I would require for one of the four leading general journals. The strongest new results remain very closely tied to an observation design whose purpose is to turn an unknown generating action into a clock law from which the action can be algebraically recovered. The v79 paper is now much better mathematics than v78, but the top-four case is still not made merely by increasing the number of theorem chains.

My recommendation is therefore:

**reject at the top-four level in the present form, while recognizing revision 79 as a real mathematical advance over revision 78.**

For a specialist journal I would request major revision rather than reject on correctness grounds.

---

## 2. Provenance and scope of this review

The reviewed branch is the genuine v79 source branch

`revision/a2-v79-robust-clock-quotient-contact-suspension-2026-09-17`

at head

`a0c5b0329141d73ded1cb2ea68d0c71a7c5863e9`.

It is based directly on the previous review head

`f9de5e1e471df61f5ac02718d0c7b18b2e7d955e`

and adds a substantive manuscript delta. This point matters because the repository also contains a different branch called
`revision/a2-v79-universal-records-stable-quotient-2026-09-17`
which is not a revision at all: it is the previous referee commit. The existing provenance-blocker report is correct for that branch but does **not** apply to the branch reviewed here.

The new source inspected includes:

- `rigidity_v79.tex`;
- `article/v79/01_introduction.tex`;
- `article/v79/02_information.tex`;
- `article/v79/03_robust_quotient.tex`;
- `article/v79/04_statistics.tex`;
- `article/v79/05_prefix_cancellation.tex`;
- `article/v79/05_root_free.tex`;
- `article/v79/07_convex_suspensions.tex`;
- `article/v79/09_robust_geometry.tex`;
- the inherited physical-clock, distance-registration, finite-coverage, mechanical, and finite-record sections active through the v79 input graph;
- `RESPONSE_TO_REFEREE_V79.md`;
- `PROOF_LEDGER_V79.md`;
- the v79 source/build manifests.

I also compared the v79 response against the controlling harsh v78 report.

The committed build audit reports a clean local 35-page build. I treat that as source/build evidence only. I do not use the verification scripts or build success as mathematical proof certification.

---

## 3. What revision 79 genuinely fixes

A severe report should not pretend that every previous objection remains unchanged. Several do not.

### R79-C1. The ambient quotient objection is substantially closed

The paper now defines the action of common positive reweighting on the whole space of strictly positive density tuples and introduces anchored log contrasts
[
Y_j(f)(z)
=
lograc{f_j(z)}{f_1(z)}
-
lograc{f_j(z_0)}{f_1(z_0)}.
]

Proposition 4.1 identifies the topological quotient with
[
(C^m_0(Q))^{J-1}
]
and thereby supplies a complete metric. The proof is explicit and, as written, is convincing: equality of anchored ratios is exactly equality modulo common reweighting, and the exponential normalized representative gives a continuous section.

This resolves the v78 complaint that the quotient-space language was stronger than the defined topology.

### R79-C2. The split chart is a real structural result

Theorem 4.2 is not merely the old three-clock formula rewritten. On a nondegenerate two-anchor chart it gives a global product decomposition
[
y longleftrightarrow (mathcal R(y),mathcal S(y))
]
between an action and a complemented residual space.

The rational coordinate using the second contrast and one scalar value of the third contrast is especially useful: two clocks determine the functional shape up to an absolute scalar gauge, and the third clock fixes that scalar. The residual then gives genuine off-model coordinates.

I checked the displayed elimination formula for (u_0), the recovery of (u_y), and the inverse identity. I do not find an algebraic defect in this part.

### R79-C3. The exact nuisance ambiguity is now characterized rather than hand-waved

Theorem 4.4 correctly isolates the confounded perturbations:
[
eta_j
=
b+c_j+lograc{T_j-V}{T_j-W}.
]
This is the right form: common nuisance and clock constants disappear under normalization, while the displayed logarithmic ratio exactly changes one action into another.

The theorem also makes the important negative point that extra clocks do not eliminate this particular ambiguity. That is a substantive improvement over treating exact source sharing as an unexamined modeling axiom.

### R79-C4. The statistical layer is now mathematically nontrivial

Theorem 5.2 supplies a genuine two-sided risk statement
[
inf_{widehat W}sup
mathbb E|widehat W-W|_{C^m}
asymp
left(rac{log n}{n}ight)^{(eta-m)/(2eta+d)}
+epsilon
]
on a specified nondegenerate Hölder class.

The upper bound uses ordinary derivative density estimation followed by the smooth quotient inverse. The statistical lower bound uses spatially separated bumps and a Fano-type argument. The misspecification lower bound uses an exactly indistinguishable action/nuisance pair.

I do not see a rate-exponent mismatch in the displayed proof. In particular, the logarithmic sup-norm rate and the (C^m) derivative loss are consistent with the chosen bandwidth.

### R79-C5. The old “action-threshold device” objection is no longer literally valid

Revision 78 used the event
[
alpha+S_n(s,t)<T
]
as an abstract threshold rule. Revision 79 now constructs a contact suspension in which (c+L) is the actual Reeb return-time roof.

Proposition 10.2 verifies invariance of
[
alpha=dz+p,dx
]
under the deck transformation and obtains first-return time (c+ell). For the convex twist map, the (n)-return time is
[
nc+S_n(s,t).
]

Thus the experimenter can count returns and compare an elapsed clock against a fixed deadline. The observation rule need not be instructed to evaluate the unknown action.

This is a real answer to the literal implementability objection in v78-M3.

### R79-C6. The generating class is genuinely infinite-dimensional and two-variable

The new class
[
lambda Ipreceq D^2LpreceqLambda I,
qquad -L_{xy}ge b
]
contains arbitrary smooth nonseparable perturbations subject to strong convexity and twist inequalities.

Lemma 10.1 derives:

- global deterministic twist dynamics;
- unique finite-horizon minimizing actions;
- explicit nonvanishing mixed derivatives;
- positive stationary Schur complements;
- the physical-prefix meaning of every match.

The cofactor lower bound
[
|(S_n)_{st}|
ge
bleft(rac{b}{2Lambda}ight)^{n-1}
]
is consistent with the tridiagonal positive Hessian argument.

This closes much of the v78 criticism that the abstract theorem merely assumed all difficult generating-system hypotheses.

### R79-C7. The class-wide deadline construction is substantially stronger than the old mechanical example

Theorem 10.3 constructs gates, a phase box, a release interval, the roof offset, and all six deadlines from class constants. The backward recurrence gives a fixed initial-coordinate bound; the global quadratic lower bound gives a positive roof; trial paths give a fixed action upper bound.

The theorem therefore does more than recover a finite-dimensional parameter or a scalar potential. It recovers an unknown two-variable generating function on any prescribed compact square.

### R79-C8. Raw branch rarity is now explicitly charged

Definition 13.1 and Proposition 13.2 improve the finite-record interpretation. The raw source is normalized before branch selection, classification failure is charged, and the success floor includes the classification factor. This is better than silently normalizing after entry into the desired branch.

### R79-C9. The literature discussion is materially improved

The revision now cites and discusses:

- Bálint–De Simoi–Kaloshin–Leguil on marked lengths for open dispersing billiards;
- De Simoi–Kaloshin–Leguil on analytic billiard determination;
- Finamore–Leguil on enriched marked-length rigidity for Sinai billiards;
- Marsden–West on discrete variational mechanics;
- Hutchings on action/contact constructions;
- standard nonparametric references;
- complete bipartite rigidity.

This is a serious correction relative to the four-entry v78 bibliography.

---

## 4. Major concerns that remain

The following are the reasons for the negative top-four recommendation.

### R79-M1. The conceptual core is still an engineered information equivalence, not yet a top-four rigidity principle

The v79 paper now has a cleaner factorization than ever:
[
	ext{clock laws}
longrightarrow
	ext{action}
longrightarrow
	ext{generating function}
longrightarrow
	ext{geometry}.
]

The first arrow is now understood extremely well. That is mathematically valuable. But it also makes the top-four significance question sharper.

On the exact model, the law quotient is explicitly coordinatized by the action. In the robust model, the action is recovered by a smooth projection, and the minimax rate is the usual density-estimation rate transferred through that projection plus the exact nuisance-confounding floor.

The post-action reconstruction is then stationary composition plus a scalar monotonicity argument.

For a leading general journal, the paper needs one theorem whose importance does not depend primarily on the fact that the acquisition mechanism was designed to encode the action. At present I do not see such a theorem.

The strongest possible response is **not** to make the manuscript longer. It is to isolate a principle that would still look deep if the action functions (S_n,S_{n+1}) were simply given to the reader.

Questions the manuscript still does not answer convincingly are:

1. What new rigidity phenomenon about generating systems is discovered, rather than encoded?
2. What obstruction is overcome that was not already latent in the classical generating-function formalism?
3. What natural data class is shown to carry unexpectedly complete information?
4. What sharp impossibility theorem makes the six-clock construction conceptually necessary?

Without one of these, the result remains an elegant inverse-design mechanism rather than a top-four rigidity theorem.

### R79-M2. The contact-suspension theorem solves the old physical-clock objection, but by building the unknown action into the roof

The v79 response is correct that the observer no longer evaluates (S_n). However, the unknown contact system is itself constructed so that the return-time roof is
[
c+L.
]

This is a perfectly legitimate dynamical system. It is also exactly the structure needed by the clock algebra.

Thus the new theorem changes the objection from

> “the apparatus thresholds the unknown action directly”

to the subtler question

> “why is observing the mapping torus whose roof *is* the unknown action a natural or conceptually difficult inverse problem?”

That is progress, but not a full top-four answer.

The paper should make the distinction explicit:

- the contact suspension is a mathematically natural realization of an exact symplectic action;
- the inverse theorem is therefore no longer circular at the level of the observation rule;
- nevertheless, the suspension has been chosen so that its return time is precisely the quantity to be reconstructed.

For a specialist journal this is entirely acceptable. For a top general journal, more is needed: either a natural pre-existing class of contact/return systems for which the theorem solves a recognized inverse problem, or a structural theorem showing that this roof construction is canonical and unavoidable in a broad setting.

### R79-M3. The six-deadline theorem is information-rich in a way that the paper does not yet conceptually calibrate

The theorem receives full two-dimensional conditional endpoint laws for (S_n) and (S_{n+1}), three deadlines for each. After quotient inversion, it knows both long generating actions as functions on open two-dimensional gates.

From that point, recovering (L) by matching a shared prefix is powerful but also very close to the composition law of generating functions.

This does not invalidate the theorem. It does mean that the paper must calibrate what has been achieved against classical twist-map data:

- Is knowing (S_n) and (S_{n+1}) on gates already essentially knowing two iterated generating functions?
- Is the recovery of (L) from these two iterates known, implicit, or genuinely new?
- Is the nontrivial content the six-law encoding, the uniform class-wide gate construction, the root-free inverse, or all three together?
- Which of those pieces survives if the clock mechanism is removed?

At present the manuscript cites discrete variational mechanics but does not provide a sufficiently sharp novelty comparison for the specific “two consecutive iterated actions determine the one-step generator” mechanism.

This is a major top-four positioning gap.

### R79-M4. The statistical minimax theorem is sharp for the abstract weighted-action model, not for the physical inverse problems

The theorem correctly says this, but the paper still leans heavily on the sharp risk statement in its significance narrative.

The (epsilon)-lower bound uses nuisance perturbations
[
eta_j=lograc{T_j-W_*}{T_j-W_1}
]
chosen specifically to make two actions exactly observationally identical.

That proves a sharp confounding floor in the abstract weighted-action class. It does **not** show that the same lower bound is realizable by:

- perturbations of an actual billiard source and retention mechanism;
- perturbations of a physical classifier;
- perturbations of a contact-suspension preparation law subject to additional dynamical constraints.

Likewise, the statistical term is a classical nonparametric density-estimation lower bound transferred through a locally bi-Lipschitz coordinate.

The paper is admirably explicit about these scopes. For a top-four significance claim, however, one needs a sharper bridge between the abstract nuisance model and the natural physical families.

A materially stronger theorem would characterize the tangent or minimax nuisance cone **inside the realizable physical experiment**, rather than in the unrestricted clock-dependent weight space.

### R79-M5. The billiard theorem remains heavily marked and reference-dependent

Revision 79 does not change the decisive structural fact that the billiard acquisition uses:

- exact obstacle labels;
- exact lift labels;
- exact reflection words;
- prescribed prefix/extension pairing;
- known scalar boundary label spaces and overlap maps;
- branch-specific gates;
- branch-specific admissible clock triples;
- exact classification or rejection with no false positive labels.

The finite identifying atlas is constructed from each table and persists on a neighborhood. That is an important theorem, but it is not a single intrinsic observation operator on a broad class.

The v79 raw-cost definition charges the probability of successful branch classification. It does not remove the informational content of exact classification.

This remains a central top-four blocker. The natural next theorem is not another stability estimate on the same marked atlas. It is one of:

1. reconstruction from a table-independent acquisition family with a proved stopping rule;
2. recovery when branch/lift labels are unknown or partially corrupted;
3. a mixture-identifiability theorem separating branches from unlabeled clock laws;
4. a sharp counterexample showing that the present labels are genuinely necessary.

Until such a result exists, the strongest billiard statement should be advertised as a **marked identifying experiment attached to a reference atlas**, not as a broad natural-data rigidity theorem.

### R79-M6. Exact classification is still an oracle-level assumption under finite records

Definition 13.1 now states the issue honestly: the classifier returns the exact prescribed word and lift or failure, with no false positive labels.

Charging classification rarity is good. It is not the same as solving classification.

In finite noisy data, a wrong positive label is much more serious than a missed branch because it creates branch mixtures, and the paper itself notes that mixtures survive additional clocks.

Thus the robust geometric theorem has a severe asymmetry:

- missed classifications are allowed and charged;
- false classifications are forbidden.

For a statistical theorem whose headline includes finite records and robust output, this is a substantial idealization.

A stronger version should allow a controlled confusion matrix or small branch-mixture contamination and prove either:

- stable deconvolution / recovery under separation assumptions; or
- an impossibility threshold.

That would materially strengthen both the statistics and the billiard contribution.

### R79-M7. The quantitative stability statement in Theorem 10.3 is under-specified

The exact uniqueness part of Theorem 10.3 is substantially convincing. The finite-order stability statement is less satisfactory at a top-four proof standard.

The theorem says, in effect, that on subclasses with “bounded finite-order derivatives on the compact phase and configuration domains constructed below,” one obtains uniform local Lipschitz recovery from (C^{k+2}) laws to (C^k) generating functions.

The proof then invokes:

- implicit differentiation of minimizing paths;
- bounds for derivatives of (S_n) and (S_{n+1});
- persistence of a common root collar;
- bounded “next derivatives” to control the collar;
- the clock-anchor theorem;
- composition through the root map.

What is missing is a precise quantitative hypothesis specifying which derivatives of (L), source, and efficiency are bounded as a function of (k), and a clean lemma propagating those bounds to the needed derivatives of the stationary actions.

This is not a fatal gap for the exact theorem. It is a proof-completeness issue for the claimed uniform finite-order stability.

For publication, replace the phrase “bounded finite-order derivatives” by an explicit family of assumptions, e.g. fixed (C^{k+r}) bounds for a stated (r), and prove the corresponding stationary-action estimates in a standalone proposition.

### R79-M8. The literature review is improved but still not commensurate with the breadth of the paper

Ten references are much better than four. They are still too few for a paper spanning:

- inverse billiards;
- marked length/lens/scattering rigidity;
- exact symplectic twist maps;
- generating functions of iterates;
- discrete variational mechanics;
- contact suspensions and action functions;
- Euclidean distance geometry;
- nonparametric derivative estimation;
- statistical model misspecification;
- minimax lower bounds with nuisance confounding.

The paper now cites representative landmarks, but it still reads more like a proof package with selected neighboring citations than a definitive positioning of a broad general-journal contribution.

The most important missing comparison is not another bibliography item by itself. It is a theorem-level novelty map:

| v79 mechanism | closest classical mechanism | exact new content |
|---|---|---|
| three-clock quotient | normalized density-ratio identification | what is structurally new? |
| split chart | Banach normal coordinates / nuisance decomposition | why nonstandard? |
| two consecutive actions (	o L) | generating-function composition | what is new beyond inversion of a classical composition law? |
| contact roof | mapping-torus/contact action realization | what inverse content is new? |
| whole-table billiard reconstruction | marked-length/lens rigidity | what data are weaker/stronger/incomparable? |

Without that map, I cannot judge priority and depth at the level required for a top-four recommendation.

### R79-M9. The manuscript still contains several logically different papers under one title

The present principal article contains at least four substantial themes:

1. a Banach quotient and nuisance geometry for normalized clock laws;
2. a minimax theorem for nonparametric action estimation;
3. a contact/symplectic inverse for uniformly convex twist generators;
4. a marked dispersing-billiard whole-table inverse with finite-record output.

The common device is the clocked action. That is a real unifying thread. But at 35 pages, the manuscript moves rapidly across several research communities, and the strongest theorem in one section is not needed for the strongest theorem in another.

For a top general journal, breadth is helpful only if the synthesis creates a principle stronger than the sum of the components. At present the paper risks the opposite: each component is compressed to make room for the others, while the editorial center remains unclear.

I would seriously consider splitting the work into:

- a quotient/statistics paper centered on robust action identification; and
- a deterministic inverse paper centered on convex twist/contact and billiard reconstruction,

unless a single overarching theorem can be formulated that genuinely requires both.

---

## 5. Technical comments and points requiring revision

These are not all top-four blockers, but they should be addressed before publication anywhere.

### R79-T1. State the exact regularity budget in the convex-suspension stability theorem

For each target (C^k) bound, specify the required (C^{k+r}) control of (L), the source, and the efficiency. Do not leave “bounded finite-order derivatives” as an existential phrase.

### R79-T2. Separate exact identification, statistical estimation, and physical realizability even more aggressively

The paper mostly does this well. Keep the distinctions visible in every main theorem:

- quotient identification is a statement in a function model;
- minimax risk is in an unrestricted nuisance class;
- contact realization is a statement about a constructed return system;
- billiard reconstruction assumes a marked physical branch architecture.

No single theorem should inherit a stronger interpretation from another section.

### R79-T3. Clarify the status of the contact suspension as part of the unknown system

The theorem should say explicitly that the observed object is the contact suspension associated with the unknown (F_L) and the fixed choice (c=C_0+1). The experimental settings are fixed across the class, but the underlying contact manifold/form varies with (L).

That is not a defect. It is an important modeling distinction.

### R79-T4. The minimax lower bound should be described as sharp for the declared nuisance class, not “physically sharp”

The present theorem statement is acceptable. Maintain this exact scope in the abstract, introduction, response letter, and future summaries.

### R79-T5. Give a dedicated proposition for physical realizability of nuisance perturbations if such a claim is desired

If the authors want the (epsilon) term to be interpreted physically for billiards, they should prove that an appropriate nontrivial subset of (eta_j) arises from admissible perturbations of preparation/retention/classification mechanisms while the underlying dynamics remain fixed.

Otherwise, leave the minimax theorem explicitly abstract.

### R79-T6. Do not describe no-false-positive branch labels as “robust branch resolution”

The current definition is exact classification with rejection. A truly robust branch-resolution theorem would have to tolerate some false positives or mixtures.

### R79-T7. The response file is useful, but the manuscript should carry all essential caveats by itself

The response correctly narrows many claims. Those caveats should not be needed to interpret the theorem statements.

In particular, the distinctions between

- action risk and billiard risk;
- exact quotient and physical realizability;
- contact return time and unsuspended ordinary time;
- raw preparation cost and exact classification capability

should be visible directly in the paper.

### R79-T8. Expand the bibliography enough to support a priority claim, not merely to avoid obvious omissions

The current references fix the most conspicuous v78 omissions. A top-four submission still needs a broader and more explicit engagement with twist-map generating functions, contact mapping-torus constructions, inverse problems for discrete Lagrangian systems, and statistical nuisance/robustness literature.

### R79-T9. Preserve the honest nonclaims

The following qualifications are good and should remain:

- the billiard theorem is marked;
- the protocol is reference-atlas dependent;
- the minimax theorem is for action, not optimal billiard geometry;
- the contact time is not ordinary time of the unsuspended map;
- the exact confounding formula does not exhibit noncongruent billiards;
- numerical checks are not proof certification.

Removing these qualifications to make the abstract sound stronger would make the paper worse.

---

## 6. Detailed assessment of the new theorem chains

### 6.1 Ambient quotient and split coordinates

This is the cleanest new section.

The quotient statement is explicit, global, and easy to audit. The split theorem then identifies the model image as a complemented graph inside the log-contrast Banach space.

The mathematical strength is clarity rather than difficulty. That is not a criticism: a transparent structural theorem can be important. The top-four problem is that the paper currently asks this section to carry more conceptual weight than its proof complexity and surrounding literature position support.

I would encourage the authors to extract the following genuinely useful message:

> Three normalized clock laws do not merely identify an action on-model; in log-contrast coordinates they define a smooth finite-codimension model manifold with an explicit global chart and a computable normal residual.

That is a good theorem. It should be positioned as such, without implying that it alone creates a deep new statistical geometry.

### 6.2 Nuisance decomposition

The exact ambiguity theorem is stronger than a generic perturbation estimate because it classifies the entire zero-residual nuisance family on the chart.

This is one of the most valuable v79 additions.

The next serious step would be to connect this abstract ambiguity space to physically realizable nuisance mechanisms. Without that bridge, the theorem is sharp algebraically but only partially informative physically.

### 6.3 Finite-record risk

The theorem is technically plausible and the proof is appropriately self-contained at the level of the claimed rate.

Its novelty is limited by design:

- the stochastic rate comes from standard density-derivative estimation;
- the action inverse is locally smooth;
- the (epsilon) lower bound comes from an explicit indistinguishable nuisance pair.

The result is still worth stating. I simply do not view it as the theorem that elevates the whole article to top-four level.

### 6.4 Convex twist dynamics

The class-wide derivation is a real improvement over an abstract hypothesis list.

The strong convexity and uniformly negative mixed derivative assumptions make the global dynamics exceptionally well controlled. Every finite endpoint problem has a unique minimizer, and the tridiagonal Hessian gives explicit twist bounds.

This is mathematically clean. It is also a very special regime. The manuscript should not let the phrase “arbitrary two-variable function” obscure the strength of the class assumptions.

A substantially deeper version would weaken global convexity or permit multiple stationary branches and still recover the generator from clocked data.

### 6.5 Contact realization

The contact construction is correct in spirit and the displayed pullback identity is the right one.

Its purpose is methodological: it converts action into elapsed return time without asking the observer to evaluate the action. That purpose is achieved.

What remains open is significance: the return roof is, by construction, the exact action plus a constant. Thus this section validates the observation model rather than creating an unexpected dynamical invariant.

### 6.6 Six-deadline inverse

The uniform backward bounds and fixed deadlines are a substantive technical contribution. The proof makes good use of the global class inequalities.

Still, the theorem should be understood as:

1. recover two iterated generating actions from two three-clock experiments;
2. match them;
3. subtract the common prefix.

That is a strong exact inverse, but its novelty must be compared directly with classical knowledge about iterated generating functions.

### 6.7 Billiard geometry

The inherited geometric chain remains the most ambitious application.

The distance certificate and overlap registration are explicit. The finite identifying atlas theorem genuinely reconstructs full smooth boundaries from full conditional laws, not merely finitely many sampled distances.

The price is the heavy marked architecture. Revision 79 improves the accounting but does not remove that architecture.

This is still the point at which I would expect the strongest top-four theorem to emerge if the authors can reduce the amount of supplied combinatorial information.

---

## 7. What would materially change my assessment

Another round of local estimates, build checks, or additional response prose will not change the top-four verdict. One of the following would.

### Path A. Unmarked or partially marked billiard recovery

Allow branch mixtures, unknown lift/word labels, or controlled false classifications, and still prove reconstruction.

### Path B. A canonical class-wide billiard acquisition

Replace the reference-table finite atlas by one intrinsic acquisition family with a proved finite stopping criterion on a substantial class.

### Path C. A physical nuisance classification theorem

Determine exactly which clock-dependent weight perturbations are realizable by perturbing source, efficiency, or classifier within the physical model, and prove sharp physical identifiability/minimax consequences.

### Path D. Recovery beyond globally convex twist systems

Permit multiple stationary branches or substantially weaker twist/convexity hypotheses, while retaining a nontrivial clock inverse.

### Path E. A theorem on consecutive iterated generating functions independent of the clock encoding

Prove a broad deterministic rigidity theorem saying that two or finitely many consecutive iterated generating functions determine the one-step generator under natural hypotheses, with sharp obstructions and a serious comparison to classical twist dynamics.

If such a theorem is independently significant, the clock laws can then be presented as a genuinely new route for obtaining its hypotheses from observations.

### Path F. A natural contact inverse problem

Identify a pre-existing geometric/dynamical class in which the contact return-time data of the theorem arise intrinsically, rather than because the suspension roof was selected to equal the action, and prove a reconstruction theorem there.

Any of these would materially change the editorial discussion.

---

## 8. Required changes for a strong specialist-journal version

Even if the target is lowered from the four leading general journals, I would still require the following.

1. Specify exact regularity budgets for every quantitative stability theorem.
2. Expand the literature discussion and explain novelty mechanism-by-mechanism.
3. Clarify in the theorem statement that the unknown contact suspension varies with (L).
4. Keep the minimax theorem scoped to the abstract weighted-action nuisance class unless physical realizability is proved.
5. State explicitly that exact classification with rejection is assumed and false positive labels are excluded.
6. Avoid any phrase suggesting a universal unmarked billiard inverse.
7. Keep all nonclaims about optimal billiard risk and ordinary unsuspended time.
8. Make the principal theorem hierarchy more obvious; consider splitting the manuscript if a single conceptual theorem cannot organize all four themes.
9. Add a concise comparison table between v79 data and the data used in neighboring marked-length/lens rigidity results.
10. Preserve the exact branch/revision provenance now that a genuine v79 source exists.

---

## 9. Final assessment

Revision 79 is the strongest version of this manuscript I have reviewed in the repository.

It is a genuine mathematical revision, not a relabelled review branch. It repairs the quotient topology, adds a true off-model decomposition, gives a sharp abstract misspecification theory, turns the old action-threshold mechanism into a real elapsed-time contact experiment, verifies the generating hypotheses on an infinite-dimensional two-variable class, and improves the accounting of branch-selection cost.

Those are substantial advances.

The reason for the negative top-four recommendation is therefore **not** that revision 79 failed to answer the previous report. It answered much of it.

The remaining objection is harder:

> the paper still has not isolated a theorem whose conceptual force is clearly greater than the carefully engineered chain by which clock laws encode actions and actions encode generating systems.

The contact suspension removes literal circularity but keeps the action as the return roof. The minimax theorem is sharp in the declared abstract nuisance class but largely transfers classical density-estimation difficulty through an explicit smooth inverse. The convex-twist theorem operates in an exceptionally rigid globally convex regime. The billiard theorem remains strongly marked and reference-atlas dependent.

This is serious, technically competent work. I would be interested in a substantially refocused version. I would not, however, recommend the present manuscript for *Annals*, *Inventiones*, *Acta Mathematica*, or *JAMS*.

**Recommendation: reject at the requested top-four level; major conceptual revision required before a new top-four submission.**
