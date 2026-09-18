# Independent harsh referee report on A2 revision 80

**Manuscript:** *Action rigidity from calibrated endpoint records*  
**Author:** Qian Qi  
**Review date:** September 18, 2026  
**Reviewed revision branch:** \`revision/a2-v80-calibrated-records-intrinsic-rigidity-2026-09-18\`  
**Reviewed revision head:** \`831dc905d139377e117138238d20d96833f4122d\`  
**Controlling substantive v79 manuscript head:** \`a0c5b0329141d73ded1cb2ea68d0c71a7c5863e9\`  
**Controlling previous harsh-review commit:** \`97bd4e64f4805c55793115c8bf4bd1744b6d9c53\`  
**Principal source:** \`papers/A2-v17-boundary-information-coarsening/rigidity_v80.tex\`  
**Requested standard:** the level expected of *Annals of Mathematics*, *Inventiones Mathematicae*, *Acta Mathematica*, or the *Journal of the American Mathematical Society*.

This is an author-requested external-referee-style mathematical report. It is not a commissioned report from any journal and is not an editorial decision. I apply the unusually severe standard appropriate to the four leading general mathematics journals: correctness is necessary, but so are conceptual inevitability, broad mathematical significance, a convincing separation from classical mechanisms, and a theorem hierarchy whose principal result remains important after the experimental encoding is stripped away.

I reviewed the new v80 source rather than merely comparing version labels. In particular I inspected the raw-measure inverse, calibrated-channel theorem and rank obstruction, the action-lift/Reeb-return section, the new regularity proposition and four-deadline convex theorem, the physical-retention nuisance construction and lower bound, the finite-record calibration theorem, the active v80 introduction and framework, and the inherited v79/v77 proof components on which the new headline theorem depends. I also compared the revision against the two substantive v79 referee audits already present in the repository.

My conclusions distinguish three questions that should not be conflated:

1. **Has v80 genuinely repaired important v79 objections?** Yes.
2. **Do I find a short fatal algebraic contradiction in the new v80 core?** No.
3. **Would I recommend the paper at the requested top-four general-journal level?** No.

The third answer is not a disguised version of the second. The principal remaining problem is now conceptual rather than a missing local estimate.

---

## 1. Recommendation

**Recommendation at the requested four-leading-general-journals level: reject in the present form.**

Revision 80 is a substantial revision, and several objections from the previous harsh reports are genuinely closed rather than rhetorically bypassed.

Most importantly:

- raw success masses are now retained, so two deadlines recover an absolute action and its raw weight by an exact affine inverse;
- false positive scientific branch labels are allowed through a calibrated full-column-rank channel;
- the previous finite-order stability gap for the convex-twist theorem is addressed by an explicit stationary-action regularity proposition and a quantitative root-collar argument;
- the abstract nuisance model is connected to an actual Bernoulli retention mechanism;
- a physical two-point lower bound is given using noncongruent billiard deformations;
- the deterministic exact-symplectic content is separated from the clock experiment through an action-lift formulation and a coprime-power identity;
- the manuscript is more explicit about what is classical and what is not.

These are real advances.

However, the revision also makes the remaining top-four issue sharper. Once the new layers are written transparently, the leading mechanisms are:

1. an elementary affine inversion after the experiment retains raw success masses;
2. a standard left inverse for a **calibrated** finite label channel;
3. a Bézout identity in the group of exact action lifts once two full powers have already been reconstructed;
4. classical return-time/action geometry for a Reeb global section;
5. an inherited strongly marked/reference-atlas billiard reconstruction;
6. standard smooth density estimation and finite-dimensional channel calibration composed with the deterministic inverse.

The synthesis is technically serious. But the strongest unresolved issue is that the hard branch-discovery and geometric-data problem is still moved into strong observation design assumptions: an exhaustive finite catalogue, known structural branch identities for calibration, a ground-truth audit on calibration records, endpoint-independent finite channels, common admissible clock windows inside each confusion block, reference-atlas scalar labels, and—for the Reeb theorem—a global section and a phase-graph cover of the powers to be inverted.

Thus v80 has made the observation model more honest and more robust, but it has not yet produced the kind of **natural-data rigidity principle** I would expect to justify publication in one of the four leading general journals.

For a strong specialist journal, I would now regard the manuscript much more favorably than v79, subject to the technical and presentation revisions below. At the requested top-four level, I remain negative.

---

## 2. Provenance and exact scope of this review

The source branch I reviewed is

\`revision/a2-v80-calibrated-records-intrinsic-rigidity-2026-09-18\`

at

\`831dc905d139377e117138238d20d96833f4122d\`.

Relative to the substantive v79 branch

\`revision/a2-v79-robust-clock-quotient-contact-suspension-2026-09-17\`,

the v80 source is a genuine mathematical delta, not a relabelled referee branch. The new principal input graph includes, among other files,

- \`article/v80/01_introduction.tex\`;
- \`article/v80/02_framework.tex\`;
- \`article/v80/03_raw_records.tex\`;
- \`article/v80/04_intrinsic_actions.tex\`;
- \`article/v80/07_convex_suspensions.tex\`;
- \`article/v80/08_regularity.tex\`;
- \`article/v80/09_physical_nuisance.tex\`;
- \`article/v80/10_calibrated_statistics.tex\`;
- \`article/v80/references.tex\`;
- the inherited v79 quotient/statistics/prefix material;
- the inherited v77 distance-registration and finite-coverage material.

The repository root README on this branch is stale and still advertises older A2 revisions. There is no v80 review-ready root entry analogous to several earlier revisions. The v80 GitHub workflow currently exports an immutable source archive; it is not a LaTeX compilation workflow. I also found no commit-status result attached to the v80 head through the available repository status query. I therefore treat v80 as a source-level mathematical revision. I do **not** treat the repository metadata as an independent proof or build certification.

The mathematical assessment below is based on source inspection and adversarial consistency checking of the principal new theorem chains. It is not a claim that every line of every inherited proof has been formally verified.

---

## 3. What revision 80 genuinely fixes

A harsh report should say plainly when earlier objections have been answered. Several have.

### R80-C1. The raw-measure distinction is mathematically real and closes the constant-action/normalization issue

The new observation operator retains the successful **subdensity**

\[
r_j=a(T_j-W)
\]

rather than only its normalized conditional density. With \(\Delta=T_2-T_1\),

\[
a=\frac{r_2-r_1}{\Delta},\qquad
W=\frac{T_1r_2-T_2r_1}{r_2-r_1}.
\]

This is correct, and it changes the information geometry in a genuine way. Absolute scale is no longer lost to per-clock normalization. Constant actions are recoverable. The inverse is locally Lipschitz in \(C^m\) under a positive weight floor and a positive clock gap.

The paper is also correct that applying this formula to normalized conditional densities would be wrong. The raw and conditional experiments are different statistical experiments.

This is a clean conceptual improvement over the previous three-conditional-law formulation.

### R80-C2. The exact scientific-label assumption is genuinely relaxed

The v79 robust billiard theorem excluded false positive branch labels. V80 now lets the reported label be wrong on scientific records.

On a finite acquisition block,

\[
g_j=C_j r_j,
\]

where \(C_j\) is a calibrated \(A\times B\) channel and \(r_j\) is the vector of true component subdensities. Under full column rank,

\[
r_j=C_j^\dagger g_j
\]

and the two-raw-deadline inverse then applies componentwise.

This is not merely accounting for missed labels. It tolerates actual positive misclassification. The conditioning by the smallest singular value is explicit, and the rank-deficient counterexample correctly shows that adding clocks cannot in general replace branch separation in the unrestricted action-pencil class.

Thus the literal v79 objection “false positive labels are forbidden” is no longer valid for v80.

### R80-C3. The v79 finite-order stability gap is substantially closed

The previous adversarial audit identified a concrete proof-completeness problem: the convex-suspension theorem claimed a uniform \(C^{k+2}\)-law to \(C^k\)-generator inverse without a stated derivative budget, quantitative stationary-action regularity, or an explicit common root collar.

V80 directly repairs this.

Proposition 8.1 gives a recursive quantitative implicit-function estimate for the stationary minimizer and propagates a \(C^{m+2}\) bound on \(L\) to \(C^{m+2}\) bounds on the stationary action. The theorem then states a concrete sufficient budget:

- \(C^{k+4}\) control of \(L\);
- \(C^{k+2}\) control of source and efficiency;
- positive source/efficiency floors;
- fixed class and twist margins.

The root derivative has a quantitative lower bound, and the proof explicitly chooses a collar radius using a bound on its variation.

I no longer regard the old v79 regularity-budget complaint as an open theorem-level gap in the same form.

### R80-C4. The paper now contains a physical nuisance realization rather than only an abstract one

The retention tangent is simple but important. If an endpoint-dependent Bernoulli retention probability stays strictly inside \((0,1)\), then every sufficiently small smooth log perturbation

\[
e_j=e\exp(\xi_j)
\]

is an actual physical perturbation of the apparatus.

More significantly, along a smooth physical deformation the formula

\[
e_{j,b}^{(t)}
=
e_b\,
\frac{J_b^{(0)}}{J_b^{(t)}}
\frac{T_j-W_b^{(0)}}{T_j-W_b^{(t)}}
\]

exactly compensates the changed action and Jacobian-source factor in the raw law.

Thus the manuscript now proves a real observational nonidentifiability inside a declared physical apparatus class rather than inferring “physical sharpness” from an arbitrary functional nuisance.

This is a serious response to v79.

### R80-C5. The noncongruent-billiard lower bound is a meaningful strengthening

The outward deformation of one obstacle produces a genuine geometric separation while preserving the finite regular atlas for small deformation. Compensating retention probabilities make all finitely many prescribed raw record laws identical.

Subject to the scope issue discussed below, this gives a legitimate two-point lower bound of order \(\epsilon\) for geometric loss under the declared efficiency-uncertainty class.

The paper is careful not to claim that its sampling exponent is minimax optimal. That restraint is appropriate.

### R80-C6. The deterministic exact-symplectic content is cleaner

The action-lift formalism is useful. If

\[
g=(F,A),\qquad dA=F^*\lambda-\lambda,
\]

then the lifts form a group under the stated composition law. For coprime \(m,n\),

\[
g=(g^m)^u(g^n)^v,\qquad um+vn=1.
\]

This separates a deterministic question from the clock encoding and removes the artificial need for convexity at the group-theoretic stage.

The manuscript also correctly states that this identity is elementary and is **not** claimed as a new group-theoretic rigidity phenomenon.

### R80-C7. The Reeb return-time interpretation is formulated correctly

For a genuine global section of a Reeb flow,

\[
F^*\lambda-\lambda=d\tau,
\]

so the first-return time is an absolute primitive for the exact return map. The suspension description is the expected one under the stated hypotheses.

This clarifies an important modeling point: in an existing Reeb system the return-time action is intrinsic to the contact form and chosen section; in the convex-twist application the unknown system is instead the \(L\)-dependent constructed suspension.

The manuscript now distinguishes these uses much better than earlier versions did.

### R80-C8. The finite-record theorem accounts for raw calibration cost

The new finite-record theorem counts all scientific and calibration launches before success, rejection, or audit. The channel error enters explicitly through

\[
\sqrt{\frac{\ell}{N_cp_c}},
\]

and the joint subdensities are estimated without introducing a random success-normalization denominator.

This is the right statistical object for the raw experiment.

---

## 4. Major concern: calibrated misclassification still externalizes the hardest branch-identification problem

This is now, in my view, the single most important structural objection.

V80 says that scientific records may have incorrect positive word/lift labels. That is true. But the theorem achieves this by requiring all of the following:

1. a **finite exhaustive catalogue** of true components in each acquisition block;
2. a fixed identification of the catalogue columns with structural branches;
3. a channel that is independent of endpoint position conditional on the true component;
4. full column rank with a positive singular-value margin;
5. either a known channel or an auxiliary calibration experiment;
6. in that calibration experiment, a **true-component audit** after the physical gate/retention stage;
7. a positive lower bound on the probability that every true component is available to the audit.

This is supervised calibration with ground-truth component information.

That is a legitimate model. It is also a strong one.

The most difficult combinatorial inverse question—what branch actually generated a record, how many branches are present, and how an unknown mixture should be decomposed—is not solved. It is moved to the audit/certification layer.

### R80-M1. The paper should not present this as unmarked branch recovery

The scientific sample is not exactly labelled, but the structural component identities are still externally available in the calibration apparatus.

The correct description is:

> recovery with noisy scientific labels under a calibrated finite closed-world catalogue.

That is materially stronger than v79, but materially weaker than unsupervised or intrinsically unmarked recovery.

### R80-M2. The audit is not a minor technical convenience

If the calibration audit can reveal the exact true word/lift/component for selected records, then it possesses exactly the discrete information whose absence makes the scientific problem difficult.

The paper should explain what physical or mathematical mechanism supplies this ground truth and why that mechanism is reasonably regarded as calibration rather than as an auxiliary oracle.

For a specialist article, it is enough to declare the audit as an extra sensor. At a top-four level, the mathematical significance of the main theorem cannot rest on language suggesting that the branch-label problem itself has been solved.

### R80-M3. Endpoint-independent confusion is a strong structural assumption

The equation \(g_j(z)=C_jr_j(z)\) requires that, conditional on the true branch, the label channel not depend on the endpoint \(z\).

In a geometric classifier, misclassification probabilities can naturally vary with endpoint, grazing proximity, local curvature, or the separability of neighboring trajectory families.

If the channel becomes \(C_j(z)\), the present matrix correction and its calibration proof change substantially.

This endpoint-independence assumption belongs in the headline hypotheses, not only in the technical definition.

### R80-M4. Unknown or omitted components remain outside the theorem

The catalogue is exhaustive. An omitted background branch is not a small perturbation of the calibrated matrix model; it is a new mixture component.

The paper explicitly admits this. That nonclaim is correct and important.

At top-four level, however, this is still a major limitation because the catalogue itself is part of the hard inverse structure.

---

## 5. Major concern: common-clock compatibility inside confusion blocks is assumed rather than turned into a geometric theorem

The false-label extension introduces a new compatibility requirement that was largely absent when every branch could be treated separately.

Every true component in one confusion block must admit the same two raw deadlines, with uniform strict margins, on the common transported endpoint gate.

The finite-record geometric theorem assumes such blocks.

This deserves more attention.

### R80-M5. Prove a nonvacuous block-construction theorem for the billiard atlas

The current identifying-atlas theorem gives branchwise gates and admissible clocks. The calibrated-mixture theorem needs groups of branches with common endpoint coordinates and common deadlines.

Those are not identical statements.

For the billiard application, the authors should prove that the reference-atlas neighborhood can be partitioned into finitely many confusion blocks satisfying the simultaneous window conditions under the proposed classifier architecture, or explicitly promote this to an independent acquisition-design hypothesis.

Without such a proposition, the false-positive extension is mathematically sound **conditional on compatible blocks**, but the existence of those blocks is not yet part of the geometric rigidity theorem.

---

## 6. Major concern: the new raw inverse is clean but too elementary to carry the top-four significance burden

The two-deadline theorem is correct and useful. Its proof is the subtraction of two affine functions of the deadline.

Once raw subdensities are retained, the unknown weight and action are just the slope and intercept of an affine pencil.

This is precisely why the result is attractive—but also why the editorial significance question becomes unavoidable.

### R80-M6. The paper gains information by strengthening the observation operator

The transition from normalized conditional laws to raw subprobability laws is not merely a more efficient proof of the same theorem. It retains success masses that the older observation operator discarded.

That is mathematically legitimate. But then the central question is:

> Why is this raw observation operator natural, difficult, or unexpected enough that its exact affine inversion should anchor a top-four rigidity paper?

The manuscript gives a physical flow-box/release-delay derivation. That establishes realizability. It does not by itself establish depth.

### R80-M7. The main inverse should be stress-tested under less information-rich raw data

A substantially stronger direction would be one of:

- unknown deadline-dependent exposure constants;
- partially missing failure counts;
- raw masses observed only up to a common calibration scale;
- a single natural point process whose multiple clocks are not independently normalized experimental settings;
- unknown branch-dependent launch rates coupled across settings.

A theorem showing which absolute information survives under such coarsening would turn the affine observation into a genuine information-rigidity principle rather than an exact inversion of deliberately preserved slope/intercept data.

---

## 7. Major concern: the coprime action-lift theorem is algebraically exact but not itself a new rigidity phenomenon

The action-lift theorem is elegant in its formulation but mathematically elementary once the hypotheses are granted.

If \(g^m\) and \(g^n\) are known as **full elements of a group** and \(\gcd(m,n)=1\), then Bézout gives \(g\).

The paper acknowledges this.

The difficult content is therefore entirely upstream:

- how the observed endpoint laws give absolute generating functions for the powers;
- how those local type-I charts cover the actual phase graphs;
- how sheets are catalogued and transported;
- how inverse factors remain inside the supplied chart domains.

### R80-M8. Do not let “coprime return rigidity” obscure the strength of the input

Knowing the complete action lifts \(g^m\) and \(g^n\) is already much stronger than knowing an unmarked spectrum, a return-time distribution, a set of periodic actions, or a partially observed canonical relation.

A top-four theorem would become genuinely interesting if it recovered the one-step system from **partial or quotient data on the powers**, not from the powers themselves as group elements.

Examples include:

- canonical graphs without absolute primitive constants;
- unpaired local sheets;
- return-time distributions without phase labels;
- only common observation charts rather than a phase-graph cover;
- powers known modulo conjugacy or gauge.

At present the group theorem organizes the proof well, but it does not add top-four depth.

---

## 8. Major concern: the Reeb theorem improves naturality only conditionally

There are two distinct contact statements in the paper.

### Existing Reeb system

If a Reeb flow already has a global section with smooth positive return time and the necessary regular phase-graph cover, then its return time is the exact action and the flow is the suspension of the return data.

This is classical geometry in an appropriate formulation.

### Constructed convex-twist system

For the convex generator \(L\), the paper constructs the contact suspension whose roof is \(c+L\). The return-time data then encode the action by design.

Both statements are valid. Neither, by itself, produces an unexpected natural-data inverse theorem.

### R80-M9. The global-section and phase-cover assumptions already encode much of the dynamical organization

The corollary does not discover a global section from observations. It assumes one.

It does not resolve caustics or unknown sheet structure. It assumes a regular phase-graph cover.

It does not identify the number of branches. It assumes a finite covered catalogue.

Thus the Reeb theorem should be viewed as a clean transport of the raw-action inverse into a class of already organized return systems.

### R80-M10. A genuinely natural contact inverse remains open

What would change the assessment is a theorem starting from data naturally attached to a pre-existing contact flow—without a supplied full phase-graph cover—and proving that the contact dynamics or geometry is rigid.

The current theorem verifies that the observation mechanism is physically meaningful. That is important. It is not yet the same as discovering a new contact rigidity invariant.

---

## 9. Major concern: the billiard theorem remains strongly marked and reference-atlas dependent

V80 improves label robustness but does not remove the structural marks.

The billiard framework still fixes or supplies:

- obstacle labels;
- lift labels as structural component identities;
- reflection-word catalogue;
- scalar boundary label spaces and chart transitions;
- branch-specific or block-specific gates;
- prefix/extension pairings through the identifying atlas;
- a reference-table finite atlas;
- overlap registration in the scalar label space;
- strict geometric certificate margins;
- an exhaustive branch list for each calibrated block.

The scientific classifier may now report the wrong word/lift. But the **meaning of each true component column** remains part of the calibrated experimental architecture.

### R80-M11. This is not an intrinsic unmarked billiard inverse

The manuscript now says this explicitly. That honesty should be preserved.

The strongest accurate description is a marked/reference-atlas rigidity theorem with calibrated label noise.

### R80-M12. The reference-atlas construction remains local in model space

For each table one can build a finite protocol that persists on a neighborhood. The experiment is not one table-independent acquisition rule that works across the broad billiard class.

Again, this is a meaningful theorem. It is not the same kind of result as rigidity from a canonical invariant such as a marked length spectrum, scattering relation, or lens data defined without first tailoring an atlas to the unknown reference object.

### R80-M13. The next advance should attack the marks, not add another layer of estimates

A top-four-changing theorem would do at least one of the following:

1. recover the branch catalogue from unlabeled or partially labelled mixtures;
2. prove that only a much weaker mark structure is sufficient;
3. construct one intrinsic adaptive acquisition family with a finite stopping theorem;
4. eliminate the supplied scalar overlap registration;
5. prove sharp counterexamples showing that specific marks are unavoidable.

Without such a theorem, the billiard result remains sophisticated but heavily designed.

---

## 10. Major concern: the physical efficiency lower bound is valuable, but its scope should be sharpened

The physical compensation theorem is one of the best new ideas in v80. It deserves a more exact formulation of what the lower bound proves.

### R80-M14. Hold the non-efficiency nuisance fixed if the conclusion is called an “efficiency floor”

In the proof of the billiard lower bound, the manuscript says to choose a smooth family of normalized raw sources along the geometric deformation. Since source functions are themselves unknown nuisances in the broad model, this still gives a valid two-point lower bound for that broad parameter class.

But if the stated interpretation is specifically:

> geometry is nonidentifiable to order \(\epsilon\) because of clock-dependent efficiency uncertainty,

then the sharpest theorem should keep the source law fixed in the common scalar phase coordinates while varying only geometry and retention, or explain carefully why the common experimental source necessarily changes its coordinate density when the geometry changes.

This is probably repairable. It matters because the point of v80 is precisely to move from an abstract nuisance lower bound to a **physical attribution**.

### R80-M15. The nuisance class is extremely rich

The theorem allows an independently clock-dependent endpoint retention function with essentially arbitrary small smooth log perturbation.

That is physically realizable as a Bernoulli decision rule, but it is also a very large apparatus class.

A stronger result would study structured detector families:

- one common detector with a finite-dimensional clock dependence;
- a known detector physics with unknown parameters;
- endpoint-independent retention;
- monotone or separable retention constraints.

Then one could ask exactly which geometric directions remain confounded.

The current lower bound is sharp for the declared broad apparatus class, not a universal statement that every realistic detector imposes an \(O(\epsilon)\) geometric floor.

---

## 11. Major concern: the finite-record theorem is technically plausible but its statistical novelty is limited

The finite-record theorem now has a coherent pipeline:

1. kernel-estimate raw joint subdensities;
2. estimate a finite channel matrix from supervised audited calibration;
3. apply a stable pseudoinverse;
4. use the two-deadline affine action inverse;
5. apply the deterministic geometric inverse.

The displayed rate is consistent with that pipeline.

I do not see an obvious exponent inconsistency in the stated bandwidth balance.

However, the statistical difficulty is largely inherited from familiar components:

- derivative density estimation;
- finite-dimensional multinomial calibration;
- smooth matrix inversion;
- a locally Lipschitz deterministic inverse.

### R80-M16. There is no sharp sampling theory for the geometric problem

The paper correctly says its geometric sampling exponent is not claimed minimax optimal.

That restraint also limits the extent to which the statistical theorem can carry a top-four significance argument.

A more decisive result would prove matching lower bounds for one or more of:

- scientific sample size \(N\);
- calibration size \(N_c\);
- coordinate noise \(\delta\);
- channel conditioning \(\sigma\);
- branch rarity \(p_c\);
- geometric derivative loss.

### R80-M17. The calibration theorem needs the audit mechanism stated more probabilistically

The proof treats the number of audited observations from each true component as a binomial-type count with a lower success probability.

This is reasonable only if the mechanism deciding whether a retained calibration record receives a true-component audit does not bias the reported-label distribution within that component.

The theorem should explicitly state the conditional independence or sampling design needed for the empirical channel-column frequencies to be unbiased.

If audit availability depends on endpoint or reported label, the displayed calibration estimator can be biased.

This is a technical clarification, not a fatal flaw, but it should be explicit at the level of a theorem.

---

## 12. Major concern: the literature positioning is still too thin for the breadth claimed

The v80 bibliography is larger and better targeted than earlier versions. It now acknowledges:

- generating functions/discrete variational mechanics;
- contact action/return constructions;
- marked-length and scattering rigidity;
- calibrated label noise;
- mutual contamination;
- nonparametric density estimation.

That is progress.

It is still not enough for a manuscript whose main theorem simultaneously touches exact symplectic dynamics, contact return systems, inverse billiards, misclassification/deconvolution, and nonparametric statistics.

Fourteen references cannot by themselves establish priority or depth across all of those areas.

The problem is not merely numerical. The manuscript needs a much sharper **theorem-by-theorem prior-art comparison**.

### R80-M18. Separate classical ingredients from genuinely new implications

For every principal theorem, state:

1. the nearest classical input/result;
2. exactly which hypotheses differ;
3. exactly which conclusion is stronger, weaker, or incomparable;
4. why that difference matters mathematically.

In particular:

- the Reeb global-section action identity is classical;
- Bézout reconstruction from full powers in a group is elementary;
- linear correction for a known confusion matrix is classical;
- kernel derivative estimation is classical;
- generating-function composition is classical.

The novelty must therefore lie in a specific new coupling of these mechanisms to the geometric inverse. That coupling needs to be argued, not merely asserted by placing them in one paper.

### R80-M19. The inverse-billiard comparison remains incomplete

The manuscript compares its marked reference-atlas data to marked length/lens/scattering results, but it still needs a precise information ordering or incomparability discussion.

For example:

- Which marks are stronger than a marked length spectrum?
- Which continuous endpoint laws are stronger than a scattering relation?
- Does the finite identifying atlas contain local canonical-graph information already sufficient to reconstruct the table by more direct methods?
- Which part of the reconstruction specifically uses the clock experiment rather than the supplied mark structure?

A top-four referee must be able to answer these questions from the paper itself.

---

## 13. Major concern: the principal article still contains several different papers

V80 now contains, in one principal source:

1. raw affine action identification;
2. conditional-law quotient geometry;
3. nonparametric action minimax theory;
4. calibrated label-noise inversion;
5. exact action-lift algebra;
6. Reeb return-time geometry;
7. convex-twist reconstruction;
8. marked periodic billiard reconstruction;
9. physical nuisance tangent and lower bound;
10. finite-record geometric estimation.

There is a common phrase—“action rigidity”—but the logical dependence is not strong enough to make all of these components one unavoidable theorem.

For example:

- the conditional-law minimax theorem is not needed for the raw-data headline theorem;
- the convex-twist theorem is not needed for the billiard theorem;
- the billiard distance certificate is not needed for the action-lift theorem;
- the physical efficiency floor is not needed for exact reconstruction.

### R80-M20. Breadth currently dilutes rather than amplifies the central theorem

At a top general journal, breadth can be an advantage if one principle forces surprising consequences in several fields.

Here the paper still reads more as a sophisticated toolkit and integration paper.

The authors should either:

- formulate a genuinely overarching information-rigidity theorem from which the principal applications follow as necessary instances; or
- split the work into focused papers with sharper claims and literature positions.

Adding more applications would not solve this problem.

---

## 14. Technical comments requiring revision

The following points are not all top-four blockers, but I would require them to be addressed before publication.

### R80-T1. Promote endpoint-independence of the label channel to a headline assumption

The matrix model \(g_j=C_jr_j\) fails if label noise depends on endpoint location. This should appear in the main calibrated theorem and finite-record theorem in unmistakable language.

### R80-T2. State the audit sampling design precisely

Specify whether every retained calibration record is independently selected for ground-truth audit, or whether audit availability is guaranteed by another mechanism.

The proof of the channel rate should explicitly condition on a design under which audited label frequencies are unbiased for each column of \(C_j\).

### R80-T3. Prove or isolate the common-deadline block assumption

For the billiard application, either construct confusion blocks with common admissible two-deadline windows on a reference-atlas neighborhood or state this compatibility as an additional independent experimental hypothesis.

Do not let readers infer it automatically from branchwise admissibility.

### R80-T4. Distinguish scientific-label robustness from catalogue robustness

The theorem tolerates incorrect reported labels **within a known finite exhaustive catalogue**. It does not tolerate unknown components or an unknown catalogue.

Use this exact terminology throughout the abstract and introduction.

### R80-T5. Tighten the physical lower-bound attribution

If the lower bound is called an efficiency floor, formulate a version with the raw source fixed across the two physical parameter points, if possible.

If not, rename the result as a source/efficiency apparatus-nuisance floor and explain which nuisance coordinates vary.

### R80-T6. Keep the rank obstruction scoped to the unrestricted action-pencil class

The kernel construction need not correspond to actual billiard generating actions. The manuscript already says this; keep that qualification visible.

### R80-T7. Separate “four raw laws” from the inherited “six conditional laws” in section titles

The section title “A fixed six-clock inverse for convex twist suspensions” is now confusing because the v80 headline result is a four-raw-law theorem.

Rename the section or make the conditional/raw distinction explicit in its title.

### R80-T8. Make the principal theorem hierarchy shorter

The introduction currently asks the reader to hold several observation operators and several geometric applications simultaneously.

A top-level theorem should identify one principal result. Secondary conditional-law and statistical results can then be stated as companions.

### R80-T9. Give a one-page hypothesis/data dependency diagram

At minimum distinguish:

- raw versus conditional archives;
- exact versus calibrated labels;
- known versus audited channels;
- phase-graph versus billiard atlases;
- physical nuisance versus abstract nuisance;
- exact law versus finite-record estimates.

The current text is correct but cognitively expensive.

### R80-T10. Expand the exact-symplectic/contact bibliography

The global-section identity, action cocycle, mapping-torus/suspension viewpoint, and reconstruction from iterates should be situated in a more complete classical context.

One or two representative citations are not enough for the priority burden the paper places on this language.

### R80-T11. Expand the statistical misclassification bibliography beyond deep-learning correction

A known confusion matrix and a ground-truth calibration sample are classical measurement-error/misclassification settings well beyond modern neural-network label-noise papers.

The paper should engage the statistical literature most structurally adjacent to its model.

### R80-T12. State constant dependence consistently

Every “uniform” estimate should expose dependence on the relevant list, including:

- atlas margins;
- clock gaps;
- weight floors;
- channel singular value;
- component count;
- audit probability;
- derivative budgets;
- source/efficiency floors;
- convexity/twist constants;
- return counts;
- domain collars.

### R80-T13. Preserve the manuscript's current honest nonclaims

In particular, do not remove the statements that:

- the billiard theorem is marked/reference-atlas dependent;
- the catalogue is not learned;
- omitted components are not absorbed;
- the geometric sampling exponent is not claimed minimax;
- the contact suspension for the convex class varies with \(L\);
- the coprime-power group identity itself is not claimed new;
- a regular phase-graph cover is assumed rather than discovered.

Those qualifications make the paper mathematically stronger, not weaker.

### R80-T14. Repair the repository-level submission entry

The root README on the reviewed branch still points readers to older revisions. A referee should not have to infer the current manuscript from branch history.

Add a pinned v80 review entry recording:

- source branch and source head;
- principal TeX entry point;
- exact active input graph;
- response/proof ledger if one is used;
- build status;
- artifact hashes if PDFs are supplied.

### R80-T15. Do not describe the current v80 source-export workflow as a native manuscript build

The workflow presently archives the source. If a compiled PDF is claimed, provide an actual reproducible LaTeX build job and its source-matched artifact.

This is submission hygiene rather than mathematics, but it matters in a manuscript with such a long revision history.

---

## 15. Assessment of the new theorem chains

### 15.1 Two raw deadlines

Mathematically correct and exceptionally transparent.

Its virtue is that it reveals exactly what information was lost in the conditional-law archive.

Its weakness, editorially, is the same transparency: once the masses are retained, the inverse is an affine slope/intercept identity.

I would keep this theorem, but I would not make it the deepest conceptual pillar of a top-four submission without a stronger information-coarsening theorem around it.

### 15.2 Calibrated false labels

This is a genuine improvement.

The correct object to invert is the vector of joint subdensities, not normalized class-conditional densities. That coupling to the raw action pencil is clean.

The theorem should nevertheless be advertised as supervised calibrated deconvolution over a known finite catalogue.

The mathematically harder unsupervised mixture problem remains open.

### 15.3 Coprime action lifts

The action-lift group is a useful language for preserving additive action constants.

The uniqueness from relatively prime powers is elementary.

The real theorem is therefore observational: recovering the full powers, including their primitives, from endpoint records.

The paper should emphasize that distinction even more strongly.

### 15.4 Convex suspension

The v80 regularity section materially improves the proof.

The globally uniformly convex negative-twist class is infinite-dimensional and genuinely two-variable, but dynamically it remains an exceptionally well-conditioned regime: one stationary branch, global twist, no caustics, and unique minimizers.

A deeper result would weaken those assumptions or make the branch structure itself part of the inverse.

### 15.5 Physical nuisance

This is one of the strongest v80 additions.

The exact compensation formula and noncongruent-table construction demonstrate a genuine physical nonidentifiability mechanism.

I encourage the authors to develop this into a more structural theorem describing the tangent cone of **restricted** physical detector models. That could become conceptually stronger than the current broad endpoint-dependent Bernoulli class.

### 15.6 Finite-record geometry

The theorem is coherent as a composition of known statistical estimates with the deterministic inverse.

Its value is operational completeness.

Its weakness as a top-four result is that neither the scientific sampling rate nor calibration complexity is characterized sharply for geometry.

---

## 16. What would materially change my top-four assessment

Another round of local estimate polishing, artifact manifests, or additional applications will not change my recommendation.

A theorem of one of the following types might.

### Path A. Unsupervised or weakly supervised branch recovery

Remove the ground-truth component audit, or replace it with much weaker side information, and identify the branch mixture jointly with geometry.

Even a theorem for a sharply delimited nontrivial class would be a major conceptual advance.

### Path B. Unknown catalogue / open-world robustness

Allow an unknown finite number of branches or a small omitted-component contamination and prove stable recovery or a sharp impossibility threshold.

### Path C. Canonical billiard acquisition

Replace the reference-table identifying atlas by one table-independent or intrinsically adaptive acquisition rule with a proved finite stopping criterion on a substantial class.

### Path D. A true partial-data powers-to-root theorem

Recover an exact map from powers when the powers are not already supplied as complete action-lift group elements—for example from unpaired canonical sheets, quotient primitives, or return-time data without a full phase-graph cover.

That would turn the current Bézout observation into a genuinely new rigidity theorem.

### Path E. Natural contact rigidity

Start from a pre-existing contact/geometric class and an intrinsic return-time observation, without constructing the roof from the unknown action and without supplying a complete phase-graph cover, and prove reconstruction.

### Path F. Geometry under structured detector nuisance

Replace arbitrary clock-dependent endpoint efficiencies by a physically constrained detector family and determine the exact identifiable/nonidentifiable geometric directions.

A matching upper/lower theorem here could be conceptually strong.

### Path G. Recovery beyond global convexity

Allow multiple stationary branches, caustics, or weaker twist assumptions and recover the generator together with a nontrivial branch-resolution theorem.

### Path H. Necessity of the supplied marks

If unmarked recovery is impossible, prove counterexamples establishing exactly which catalogue, lift, word, overlap, or audit information is necessary.

A sharp impossibility theorem can be as important as a positive inverse theorem.

---

## 17. Venue-level assessment

### Correctness

**New exact algebraic core:** I find it substantially credible on the inspected scope. I do not find a short fatal contradiction in the two-raw inverse, calibrated left inverse, action-lift algebra, Reeb-return identity, physical compensation formula, or convex regularity mechanism.

**Inherited geometric chain:** internally coherent under its strong marked/reference-atlas hypotheses in the portions inspected.

**Finite-record estimates:** plausible and consistent with the stated kernel/calibration pipeline, subject to making the audit sampling design fully explicit.

This is not a formal proof certification.

### Novelty

There are genuine new combinations and some genuinely useful structural observations, especially the coupling of raw subdensity information to absolute action, calibrated label noise, and the physical nuisance lower bound.

But several headline mechanisms are classical or elementary once their strong inputs are granted.

### Depth

The hardest geometric/combinatorial uncertainty is still substantially encoded in the experimental design:

- the finite catalogue;
- calibrated column identities;
- ground-truth audits;
- reference atlases;
- global sections;
- phase-graph covers.

That is the principal obstacle to a top-four recommendation.

### Breadth

The manuscript is extremely broad, but the breadth has not yet crystallized into one theorem whose conceptual force exceeds the sum of its modules.

### Recommendation by venue

- **Annals / Inventiones / Acta / JAMS:** reject in present form.
- **Strong specialist journal:** major revision; the paper is now mathematically serious enough to merit consideration after scope and positioning are sharpened.
- **Future top-four resubmission:** should be driven by a new theorem attacking the observation-design/oracle structure, not by another incremental response layer.

---

## 18. Final referee statement

Revision 80 is the strongest A2 revision I have inspected in this repository.

It genuinely answers important prior objections. The authors no longer discard the raw mass and then struggle to recover an absolute scale from normalized laws. They no longer require every positive scientific branch label to be correct. They no longer leave the convex-twist finite-order regularity budget implicit. They no longer rely only on an abstract nuisance to claim an efficiency floor. They no longer present the iterated-generating-function step as if convexity were conceptually necessary at the group level.

Those improvements matter.

The reason for my negative top-four recommendation is therefore **not** that v80 failed to respond to the previous reports. It responded to them unusually directly.

The remaining issue is deeper.

The paper recovers strikingly rich geometry after the observation architecture supplies strikingly rich organization: raw success masses, a finite exhaustive branch catalogue, calibrated channel columns, true-component audit data, compatible deadline blocks, reference scalar atlases, phase-graph covers, and global sections. The new algebra shows that these data are sufficient. What is not yet established is that this is a natural or unexpectedly weak data set, or that the hard combinatorial/geometric identification problem survives rather than being placed into the calibration layer.

Likewise, once two full action lifts \(g^m\) and \(g^n\) are known, coprimality recovers \(g\) by an elementary group identity. Once raw subdensities at two deadlines are known, the action is the intercept/slope ratio of an affine pencil. Once a full-rank channel is calibrated, linear deconvolution is standard. Once a global Reeb section and its phase-graph cover are supplied, return time is the exact action. These are all clean facts. Their integration is useful. But at the requested editorial level, the paper still needs a theorem whose conceptual content cannot be reduced to this sequence of strong information inputs plus classical inversions.

The most promising directions are therefore not additional layers of bookkeeping. They are to remove or prove the necessity of the audit, catalogue, mark, cover, or reference-atlas assumptions; or to derive a genuinely natural contact/billiard invariant from which the same geometry follows.

**Final recommendation: reject at the four-leading-general-journals level in the present form; major conceptual revision required for a future top-four submission.**
