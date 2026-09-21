# Independent harsh top-four referee report on A2 revision 107

**Manuscript:** *Hankel information and nonlinear contact of synchronized roots*  
**Author:** Qian Qi  
**Revision reviewed:** A2 v107  
**Reviewed branch:** revision/a2-v107-synchronized-root-contact-budget-geometry-2026-09-21  
**Reviewed commit:** a17d3cad6aeebe75f29102ecb2d1ef6784927f4e  
**Previous mathematical baseline:** 5cbbe96cd2ac590bfa2e17bcef97b0630cd91c4a (A2 v106)  
**Previous independent report:** bcd8052659a783632de3873af49f05f600a8f764  
**Review date:** 2026-09-21  
**Standard used:** external referee standard for a general top-four mathematics journal.

## 1. Recommendation

**Disposition: reject in the present form at a general top-four mathematics journal.**

This is nevertheless a materially stronger paper than v106. Revision 107 does not merely rewrite the previous manuscript. It adds substantial mathematics: a synchronized-root nonlinear contact theorem, a fixed-total-exposure fibre theorem, a weighted leading-map theorem with genuine coefficient variation, a more explicit distinction between intrinsic residual geometry and marked fast-coordinate certificates, completed planar endpoint arguments, and a semialgebraic equality framework for arbitrary endpoint degenerations.

I did not find a short algebraic counterexample invalidating the three principal new theorems I audited most closely: Theorem thm:synchronized, Theorem thm:budget, and Theorem thm:critical-jets. Their proof mechanisms are coherent and the finite symbolic checks cover several useful examples. That is an important improvement over earlier versions.

The reason for rejection is therefore not that the revision is empty or obviously false. The problem is that the manuscript still does not meet the conceptual, novelty, and architectural standard expected of a general top-four paper. The new central theorem places three previously developed structures in one natural statistical model, but their mathematical interaction remains substantially factorized. The arbitrary-stratum endpoint theorem is an exact representation-comparison test, not a function-only inverse classification. The theorem-level literature discussion is much better, but it still misses a directly relevant inverse-parametric-programming literature. Finally, the source-bound native build was not closed at the reviewed HEAD at the time of this report.

In short: **v107 closes many technical objections from R106, but it has not yet converted the program into one decisive, irreducible top-four theorem.**

## 2. What revision 107 genuinely accomplishes

I begin by recording the progress because the remaining objections should not obscure it.

### 2.1 A genuinely nonlinear residual now occurs in the native binary experiment

The synchronized-root construction is the first result in this line that puts a non-affine critical residual directly inside the calibrated binary polynomial model rather than adding an abstract finite-map example alongside the statistical model.

With root pairs
\[
r_i+s_i/2\pm a_i^{\mathsf T}\eta,
\]
the retained variance map becomes
\[
q_A(\eta)=\big((a_i^{\mathsf T}\eta)^2\big)_{i=1}^k.
\]
Under the spanning hypothesis on the measurement tensors \(a_i a_i^{\mathsf T}\), the quadratic map is proper modulo the simultaneous sign ambiguity. The proof then uses the locally nonsingular ambient symmetric-coordinate model to localize a bounded normalized residual at
\[
s,\text{mixing},z=O(t),\qquad \eta=O(\sqrt t),
\]
and obtains the complete leading residual
\[
E_b=
\{\mathsf L a+\mathsf D_x(q_A(\eta)-b)+\mathsf D_z z:
a\in\mathbb R^{k+1},\eta\in\mathbb R^d,z\in\mathbb R_+^e\}.
\]

This is a real improvement over v106. In particular the example with loadings
\[
(1,0),(0,1),(1,1)
\]
produces the non-affine cone
\[
(v_3-v_1-v_2)^2=4v_1v_2
\]
after the irrelevant simultaneous sign has already been quotiented out. That directly addresses the previous complaint that the regular symmetric-coordinate compatibility theorem collapsed the difficult root-label multiplicity to one observed affine sheet.

### 2.2 The contact formula is clean and, at the formal level, convincing

The Hellinger expansion and nuisance profiling lead to
\[
\lim_{t\downarrow0}\frac4{t^2}
\inf \sum_j\lambda_j h^2(p_j,p_j^{\rm target}(t))
=
\min_{\eta,z\ge0}
(q_A(\eta)-b,z)^{\mathsf T}Q(q_A(\eta)-b,z).
\]
The localization argument is appropriately two-sided: a trial gives the \(O(t^2)\) upper bound, the ambient inverse gives bounded rescaled variables, and uniform quadratic expansion gives the liminf/limsup match.

The proof also correctly keeps the rank-one constraint. Replacing \(q_A(\eta)\) by the convex PSD relaxation would generally change the minimum, so the paper is right not to smuggle convexification into the theorem.

### 2.3 The fixed-budget geometry is substantially developed

Theorem thm:budget is a genuine addition rather than a disclaimer. The reciprocal budget functional
\[
\chi(y)=
\min\left\{
\sum_j\frac{a_j}{\omega_j}:
\omega>0,\ T\omega=y
\right\}
\]
has a unique minimizer, analytic dependence, positive Hessian, and the expected homogeneity. The kernel dimension
\[
d_0=m-(2n-1)=2-e
\]
then yields a useful trichotomy:

- two endpoints: a smooth hypersurface and one exposure vector;
- one endpoint: a convex region whose interior fibre has two points;
- no endpoints: a convex region whose interior fibre is a circle.

The radial proof on each positive affine moment fibre is simple but effective. This closes the most obvious weakness in v106, where fixed total exposure was statistically natural but mathematically underdeveloped.

### 2.4 The coefficient-stability theorem is a real stability theorem

Theorem thm:critical-jets is conceptually cleaner than the previous fixed-resolution persistence statement. Under a proper weighted leading map \(P\), higher weighted order remainder, and a positive unit-section margin, the normalized residual is
\[
P(K)-b,
\]
and the metric minimum converges uniformly on compact coefficient families. The leading coefficients themselves may vary. This is importantly different from merely keeping a divisorial order vector fixed.

The proof is elementary weighted scaling plus properness. That simplicity is a strength for correctness, though it matters for novelty, as discussed below.

### 2.5 The marked/intrinsic distinction is now mathematically explicit

Proposition prop:fast-switch and Example ex:marked-certificate do useful work. They demonstrate that a residual germ can be invariant while a chosen derivative certificate fails after a nontransverse change of fast coordinate. The chain-rule hypotheses under which second-fast-derivative smallness transfers are stated explicitly.

Likewise, Proposition prop:simultaneous makes the role of proper real uniformization, normal crossings, retained positive-time corners, identically zero numerator blocks, and accessible faces considerably more auditable than the compressed proof in v106.

This substantially closes R106.2 at the level of mathematical hygiene.

### 2.6 The planar endpoint proof is much easier to audit

The explicit KKT sector tables in Lemma lem:planar-fan and the exhaustion argument in Proposition prop:planar-exhaustion are valuable. The earlier two-endpoint three-cell theorem had the right shape but demanded too much reconstruction from prose. The new version makes the missing-sector geometry and the scalar interval conditions visible.

The separate missing-singleton and missing-extreme lemmas also improve the first-stratum reconstruction theorem.

### 2.7 The dependency and provenance story is now acceptable in principle

The new dependency table distinguishes inherited v104/v106 statements from v107 statements and makes clear which new results are companion results rather than prerequisites. The manuscript also explicitly says that finite algebra checks are examples, not theorem verification, and that language-model assistance is not mathematical validation.

That is the correct evidentiary hierarchy.

## 3. The main remaining blocker: the central theorem is still mathematically factorized

This is the most important point in the report.

Revision 106 had three strong but largely parallel themes:

1. singular residual geometry;
2. native Hankel inverse-information geometry;
3. endpoint inverse representation.

Revision 107 now places all three in the synchronized binary model. That is progress. But the central theorem still does not show a sufficiently deep mathematical interaction among them.

The structure is, schematically,
\[
\boxed{\text{synchronized root loading }A}
\quad\Longrightarrow\quad
\mathcal V_A
\]
and independently
\[
\boxed{\text{ambient clocks/roots/exposures}}
\quad\Longrightarrow\quad
Q^{-1}=J_*H(\omega)J_*^{\mathsf T},
\]
after which the contact is the generic metric minimization
\[
\min_{v\in\mathcal V_A}\widehat G_Q(v-b).
\]
Finally, in the fully visible one-colour class,
\[
G_Q|_{\mathbb R_+^k}
\quad\Longrightarrow\quad
Q\ \text{up to endpoint gauge},
\]
and therefore the recovered \(Q\) can be inserted into the preceding minimization.

All of these arrows are meaningful. The problem is that the first and second arrows remain largely independent.

The loading family \(A=(a_i)\) is prescribed externally, subject to the spanning condition. The native Hankel metric \(Q\) is produced by the ambient score system and the exposures. There is no nontrivial identity forcing the measurement tensors \(a_i a_i^{\mathsf T}\) to interact with the Hankel moment coordinates, the clock polynomial, or the endpoint fan. The endpoint theorem reconstructs \(Q\); once \(Q\) is known, of course it determines the \(Q\)-metric cost of any closed feasible set supplied afterward.

That last implication is almost formal:
\[
\text{reconstruct }Q
\quad\Rightarrow\quad
\text{compute every functional explicitly defined from }Q.
\]
The synchronized cone makes this functional interesting, but it does not by itself make the reconstruction-contact relationship a new rigidity phenomenon.

This is why I do not regard Theorem thm:synchronized, in its current form, as the decisive unification theorem requested in R106.1.

### 3.1 What would make the coupling genuinely stronger?

At least one of the following would materially change my assessment.

First, derive the loading geometry from the same polynomial/clock mechanism instead of allowing an essentially arbitrary spanning family \(A\). A theorem relating the quadratic measurement tensors to the Hankel congruence class would make the coexistence nonaccidental.

Second, classify the possible pairs
\[
(\mathcal V_A,Q)
\]
that can arise from one native experiment and prove a restriction that would fail for an arbitrary rank-one measurement cone paired with an arbitrary positive metric.

Third, prove a new rigidity or stability statement for the contact
\[
b\mapsto \min_{v\in\mathcal V_A}\widehat G_Q(v-b)
\]
that uses the Hankel structure of \(Q\), not merely its positive definiteness. For example, a structural classification of minimizer transitions, singular strata, or reconstructibility that is false for generic \(Q\) would constitute an actual interaction theorem.

Fourth, prove that the fixed-budget Hankel image imposes a nontrivial geometry on the synchronized contact family. The present theorem states both objects, but the proof of the contact theorem does not use the fixed-budget fibre classification.

Without such a step, the current central theorem reads to me as a rigorous and useful composition of three components, not yet as one irreducible theorem of the kind expected to carry a broad general-journal paper.

## 4. The phrase “same observation model” does not by itself close the unification problem

The manuscript repeatedly emphasizes that the metric was not chosen to manufacture the cone. That is a legitimate distinction from the earlier realization-style constructions.

But “not reverse engineered from a desired \(Q\)” is weaker than “the two structures constrain one another.”

The synchronized subfamily is imposed inside an ambient experiment whose efficient information has already been computed in the unrestricted symmetric coordinates. The proof explicitly says that synchronization changes the feasible residual set but not the ambient Fisher metric. That is mathematically clean, but it also exposes the factorization:

- the singularity lives in the feasible subset;
- the Hankel theorem lives in the ambient metric;
- their combination is a constrained quadratic-distance problem.

There is nothing wrong with this. It may be publishable mathematics. The top-four question is whether the combination produces a new phenomenon beyond juxtaposition. The current paper has not yet demonstrated that at the required level.

## 5. The arbitrary-stratum endpoint theorem is not an intrinsic inverse classification from the function alone

Theorem thm:all-strata is useful, but the manuscript should be much more precise about what problem it solves.

The theorem begins by fixing a **reference representation \(Q\)**. The active cones \(K_I\) and local matrices \(S_I\) of that reference representation are then compared with those of a candidate \(Q'\). Equality follows from finitely many polynomial identities on the intersection cones.

This is an exact and elegant **representation-equivalence test**:
\[
Q,\ Q' \quad\mapsto\quad
\text{do they define the same labelled value function?}
\]

It is not, by itself, a reconstruction algorithm that starts only from an observed function \(G\) and recovers all its minimal representations on arbitrary visibility/rank strata.

That distinction matters because the first-stratum results genuinely do something stronger. In the fully visible, one-missing-cell, and two-endpoint three-cell cases, one can read intrinsic local quadratic data from \(G\), orient rank-one differences using labelled open regions, and reconstruct or parameterize the minimal representation. The arbitrary-stratum theorem instead assumes that one presentation is already available so that its full active data can be enumerated.

The subsequent Hardt triviality statement is also an existence theorem for a finite semialgebraic partition of a parameterized family. It does not produce an explicit normal-form classification of higher degenerations.

The paper partly acknowledges this in the final paragraph of the section, but elsewhere the language “covers arbitrary visibility and rank strata” risks suggesting that the general inverse problem has been solved in the same sense as the first-stratum problems.

For a top-four submission I would insist on one of two choices:

- **Narrow the claim:** call Theorem thm:all-strata a finite semialgebraic equality/representation test relative to a supplied reference presentation; or
- **Strengthen the theorem:** formulate an intrinsic input model for the labelled function itself and recover the minimal fibre from that data without assuming a hidden reference matrix.

At present the theorem is correct-looking but less powerful than its placement in the paper suggests.

## 6. The weighted critical theorem is useful, but its mathematical depth should not be overstated

Theorem thm:critical-jets is a good theorem to have. It gives exactly the stability statement that v106 lacked.

However, its proof is essentially the standard weighted-homogeneous scaling argument:

1. properness of the degree-one weighted initial map gives a coercive lower bound;
2. bounded normalized residual forces weighted radius \(O(t)\);
3. the higher-weight terms are \(o(t)\);
4. rescaling gives the limiting image and metric minimum.

This is a clean normal-form lemma. It is not, in my view, a deep singularity classification theorem.

The manuscript is mostly careful about this, saying it does not classify every critical germ. That caveat should remain prominent. The theorem should not carry any implication that arbitrary singularities have been reduced to weighted homogeneous leading maps. On resolved charts one still has to establish properness, chart coverage, and feasibility, and different charts may have genuinely different initial structures.

For a general top-four article, the weighted theorem should support the main result rather than function as a second major novelty axis.

## 7. The endpoint inverse-representation literature review is still incomplete

Revision 107 greatly improves the literature section, but there is a concrete omission that is too close to the paper's inverse-optimization language to ignore.

The manuscript now cites the linear complementarity literature and forward multiparametric quadratic programming, including classical piecewise-affine optimizers and piecewise-quadratic value functions. It then positions the endpoint results as an inverse problem: recover a positive quadratic-program representation from a labelled value function when endpoint count and active-set names are not supplied.

There is established literature explicitly called **inverse parametric quadratic programming** that should be compared theorem by theorem.

In particular:

- A. B. Hempel, P. J. Goulart, and J. Lygeros, *Inverse Parametric Quadratic Programming and an Application to Hybrid Control*, IFAC Proceedings Volumes 45(17), 68–73 (2012), DOI 10.3182/20120823-5-NL-3013.00033. This work constructs constraints and a quadratic objective whose unique parametric minimizer is a supplied continuous piecewise-affine function, and describes the inverse problem as complete when such a representation exists.

- N. A. Nguyen, S. Olaru, P. Rodriguez-Ayerbe, M. Hovd, and I. Necoara, *Constructive Solution of Inverse Parametric Linear/Quadratic Programming Problems*, Journal of Optimization Theory and Applications 172(2), 623–648 (2017), DOI 10.1007/s10957-016-0968-0. This develops constructive inverse LP/QP representation methods and explicitly discusses the relation with parametric quadratic optimal-cost functions.

These papers are not identical to the present theorem. They emphasize reconstruction of an optimizer map and a parametric program, whereas the present manuscript studies a very special orthant-constrained quadratic value function, positivity, minimal endpoint dimension, and labelled Hessian data.

But that is exactly why they must be discussed. The paper needs to state precisely:

1. what information is supplied in those inverse-PQP problems versus here;
2. whether the constraint fan is supplied or recovered;
3. whether the optimizer map or only the value function is observed;
4. what minimality/uniqueness notion is proved;
5. what positivity/orthant structure makes the current theorem stronger or different;
6. whether any of the current reconstruction can be reduced to an existing inverse-PQP construction.

At a top-four venue, omission of directly named inverse-parametric-QP literature is not a minor bibliography issue when inverse representation is one of the manuscript's three principal themes.

## 8. The fixed-budget theorem needs a sharper novelty comparison

The fixed-budget theorem is one of the best additions in v107, but its novelty is currently asserted more than established.

The key object is the image of the positive exposure simplex under the reciprocal weight map and the fixed-clock moment map. The proof is driven by strict convexity of
\[
\phi(\omega)=\sum_j a_j/\omega_j
\]
on an affine moment fibre, plus the fact that
\[
\dim\ker T=2-e.
\]

This yields a particularly transparent fibre topology because the kernel dimension is at most two. The result is attractive. But the paper should compare it more directly with classical and modern optimal-design descriptions of information-matrix images under approximate designs, moment-space parametrizations, and equivalence classes of designs generating the same information matrix.

The current Kiefer-Wolfowitz/Pukelsheim paragraph is too broad to establish that the **complete fibre topology** claimed here is new rather than a specialized consequence of known design equivalence geometry.

A theorem-level comparison should answer:

- Is the function \(\chi\) a known gauge or dual design functional in this fixed-support setting?
- Is the one-point/two-point/circle fibre trichotomy already implicit in standard descriptions of design equivalence classes when the kernel dimension is \(0,1,2\)?
- Which part depends essentially on the reciprocal transformation \(\omega_j=a_j/\lambda_j\) forced by the inverse-information formula?
- Which part would remain true for any positive matrix \(T\) of corank at most two?

If the answer to the last question is “almost all of it,” then the contribution should be described as a clean application to the native experiment rather than as another central structural theorem.

## 9. The rectangular-clock result should remain carefully limited

Proposition prop:overidentified is useful because it prevents the square-clock Hankel theorem from being silently extrapolated.

The seven-clock example proves that the congruence \(J_*\) selected from one six-clock subdesign does not continue to send the overidentified inverse information into the same Hankel subspace. That is enough for the proposition as written.

It does **not** prove that no exposure-independent alternative congruence can exist for that overidentified model, nor does it classify the overidentified inverse-information image.

The text currently includes the necessary caveat. It must stay. No abstract, introduction, or conclusion should convert the displayed counterexample into a global impossibility theorem for all Hankel-type coordinates.

## 10. The synchronized theorem needs a more precise statement of what is intrinsic

The theorem mixes several levels of structure:

- the full probability residual \(E_b\);
- the quotient by the free score space;
- the quadratic measurement cone \(\mathcal V_A\);
- the endpoint orthant;
- the native metric \(Q\);
- the labelled endpoint profile \(G_Q\) on the positive retained orthant.

The abstract says that the “complete leading residual is a linear image of a rank-one quadratic measurement cone.” Literally, the displayed complete residual also contains the free score subspace and the endpoint cone. The rank-one cone is exact only after the corresponding decomposition/quotient.

This should be stated with the same precision used in the theorem itself. A top-four abstract should not rely on the reader to infer which nuisance and endpoint directions have been suppressed.

Similarly, the phrase “for every loading family and every target” should retain the theorem's target domain \(b\in\mathbb R_+^k\) unless a separate extension to arbitrary real \(b\) is intended. The endpoint profile extends to real retained arguments once \(Q\) is recovered, but the target \(tb\) is introduced as a feasible variance target in the unrestricted polynomial model and therefore has its own sign restriction.

## 11. The “fully visible profile determines every nonlinear contact” statement is formally stronger than it is conceptually new

The third paragraph of Theorem thm:synchronized is true-looking under the inherited reconstruction theorem:

1. \(G_Q\) on the positive orthant reconstructs \(Q\) up to endpoint scaling and permutation;
2. these endpoint congruences preserve the minimization over \(z\ge0\);
3. therefore the extension \(\widehat G_Q(y)\) is fixed for all real retained \(y\);
4. hence the synchronized contact is known for every allowed \(A,b\).

But once step 1 is available, steps 2–4 are close to functorial bookkeeping.

The manuscript should identify a consequence that is specific to the nonlinear cone and not simply “knowing \(Q\) lets one evaluate a \(Q\)-dependent formula.” Otherwise the endpoint reconstruction theorem remains the substantive inverse theorem and the synchronized contact theorem remains a separate application.

This point is closely related to Section 3 above and is, in my view, the key conceptual issue for the next revision.

## 12. The manuscript still contains too many competing centres of gravity

Even after the reorganization, I count at least five theorem families that could each anchor a specialized paper:

1. finite-map residual reduction and divisorial certificates;
2. weighted critical initial maps;
3. endpoint inverse representation and visibility strata;
4. model-forced Hankel inverse information and total positivity;
5. fixed-budget design fibres and synchronized nonlinear contact.

The dependency table helps the reader know where the results came from. It does not by itself solve the editorial problem of what the paper is **about**.

A top-four paper may be long and broad, but its breadth normally grows from one theorem or one mechanism. Here the paper still reads as an accumulation of several successful rounds of referee repair.

The current title points to Hankel information and synchronized-root contact. If that is the intended final paper, then the manuscript should be rewritten so that those results form the spine and the older finite-map/divisorial/endpoint machinery is included only where it is logically needed or clearly presented as companion theory.

This does not mean deleting mathematics arbitrarily. It means imposing a theorem hierarchy:

- one central theorem;
- a small number of indispensable structural inputs;
- clearly segregated companion results;
- technical archives or appendices for historically important but nonessential material.

At present the historical preservation goal is still visible in the mathematical exposition.

## 13. The general semialgebraic theorem should not be marketed as an explicit classification

Theorem thm:all-strata proves semialgebraicity and invokes quantifier elimination and Hardt triviality. Those are strong general-purpose tools, but the resulting statement is qualitative:

- there exists a finite Boolean polynomial description;
- there exists a finite partition with constant semialgebraic homeomorphism type.

This is not the same level of information as the explicit scalar interval in the two-endpoint three-cell theorem, or the normalized reconstruction formula in the fully visible theorem.

The manuscript itself says this in the final paragraph. The abstract and introduction should preserve that hierarchy.

For arbitrary visibility/rank degeneration, v107 now has an exact **finite decision framework**, not a usable catalogue of normal forms.

That is a respectable result. It should be called exactly that.

## 14. Source-bound reproducibility is not yet closed at the reviewed HEAD

I separately audited the GitHub workflow state because the manuscript explicitly presents source-bound native replay as part of its revision evidence.

At commit e8cbaa8c53e1d65e1bcc72600d26bad8794dfd9e, workflow run 35549580825 completed with failure in the step “Compile both pinned manuscripts and run finite exact checks.”

The important distinction is:

- the finite exact algebra checks **passed**;
- the workflow recorded eight check groups, including the synchronized cone identity, rational inverse examples, fixed-budget fibre example, three planar endpoint families, and the retained v106 cubic example;
- the native v107 manuscript build/reference closure **failed**, with unresolved references/citations recorded in the generated receipt.

At the exact reviewed HEAD a17d3cad6aeebe75f29102ecb2d1ef6784927f4e, the follow-up workflow run 35549978977 was still queued when this report was finalized. Therefore I cannot record a successful source-bound native receipt for v107.

This is not evidence that a theorem is false. It is an archival/reproducibility defect.

But R106.9 explicitly requested source-bound build/replay closure. On the evidence available at the reviewed commit, that request is **not yet closed**.

The next revision should include a successful run tied to the exact source commit and should ensure that the final log, not merely an intermediate first-pass log, has no unresolved references or citations.

## 15. Proof-level comments on Theorem thm:synchronized

The main proof is substantially better than the previous regular compatibility argument, but I would still request the following refinements.

### 15.1 Define the uniform spanning margin precisely

The theorem says the uniform conclusion holds with a positive lower bound for the spanning measurement map. Define an explicit quantity, for example the smallest singular value of
\[
S\mapsto(a_i^{\mathsf T}Sa_i)_i
\]
on \(\operatorname{Sym}_d\) with a fixed norm, and state the compactness assumptions in those terms.

This matters because the quadratic coercivity constant for \(q_A\) is the localization mechanism.

### 15.2 Separate the ambient inverse theorem from the synchronized singular localization

The proof currently invokes local bi-Lipschitzness of the ambient symmetric model and then immediately restricts to the synchronized subfamily. A short lemma saying exactly which ambient coordinates are recovered with a uniform inverse bound would make the proof modular and would clarify which constant is independent of the loading family.

### 15.3 State target feasibility and domain consistently

The target uses unrestricted nonnegative variances \(tb\). Keep \(b\ge0\) in every global claim unless the target construction is extended.

### 15.4 Make the quotient statement primary when discussing non-affinity

The full residual includes a free linear subspace. The genuinely new singular object is the quotient cone. The introduction should state that directly rather than alternate between “complete residual” and “quadratic cone.”

### 15.5 The perturbation statement deserves a named uniform hypothesis

For
\[
\ell_i(\eta)=a_i^{\mathsf T}\eta+O(|\eta|^2),
\]
the proof uses uniform \(C^2\) bounds and persistence of quadratic coercivity on a fixed neighbourhood. Put these in the theorem statement as a single explicit class of perturbations so that “analytic or semialgebraic \(C^2\)” is not doing hidden work.

## 16. Proof-level comments on the fixed-budget theorem

I found the proof mechanism convincing, but some presentation points matter.

### 16.1 Distinguish the open exposure simplex from its closure

The theorem uses positive exposures. Therefore designs with zero exposure are excluded. The moment image is described inside the open fixed-clock moment cone \(\mathscr M\).

Please state explicitly which boundary is:

- the relative boundary of the image inside \(\mathscr M\);
- the limit as some exposure tends to zero;
- the boundary of the ambient finite moment cone.

These are different notions.

### 16.2 The spherical fibre statement is differential-topological, not affine

For \(e=0\) the interior fibre is diffeomorphic to \(S^1\). It is not asserted to be a Euclidean circle in the original exposure coordinates. The manuscript mostly says this correctly. Keep “diffeomorphic to a circle” whenever the coordinates matter.

### 16.3 Explain how much of the theorem is model-specific

The proof uses only the positive reciprocal functional and a moment map of corank \(2-e\). A reader should be told exactly which hypotheses come from the binary experiment and which are a general convex-fibre lemma.

A clean way to do this would be to state the reciprocal-fibre theorem abstractly and then give the native design result as a corollary. That would simultaneously clarify the novelty issue.

## 17. Proof-level comments on endpoint reconstruction

The new planar tables are a strong improvement.

I nevertheless recommend three additional changes.

First, in Proposition prop:planar-exhaustion, spell out exactly where labelled regions are used to orient the rank-one forms. The phrase “reversing either sign would put a different polynomial on a labelled open set” is correct in spirit, but this is the step that prevents hidden sign gluings.

Second, in the missing-singleton reconstruction, the proof should explicitly say why the two chosen pair ranges exist when \(e=3\) and why the “contains exactly one known line” criterion cannot accidentally select another pair after a nontrivial linear dependence. Column independence appears to supply this, but one extra sentence would make the argument airtight to a reader auditing only that lemma.

Third, keep the distinction between the first-stratum intrinsic reconstruction theorems and the general reference-based equality theorem. The latter should not be used retroactively to claim that the former proofs were unnecessary.

## 18. Proof-level comments on the simultaneous-resolution proposition

The new proposition is much more transparent than the old compressed argument.

However, it is logically dependent on the inherited semialgebraic/compact hypotheses for the tube graph. Since the new main paper imports material from several historical source trees, the proposition should restate enough of those hypotheses that it can be read without searching backward across versions.

In particular state directly:

- the source set is compact semialgebraic and the relevant maps/arcs are semialgebraic/analytic where needed;
- \(J\neq0\) on the positive-time tube;
- the positive-time graph closure is the object being uniformized;
- pruning retains a surjective preimage of the germ.

The proof already uses these facts. The theorem statement should expose them.

## 19. Priority and significance of the Hankel theorem

The native Hankel inverse-information theorem remains, in my view, one of the strongest conceptual components of the paper.

The key point is not that finite Hankel moment cones or Cauchy matrices are new. It is that the specific calibrated binary polynomial score system forces the retained **inverse** efficient information into a fixed congruence class.

The new rational-inverse lemma helps a great deal. The explicit four-clock example is useful, and the overidentified counterexample defines the boundary of the exact square-clock statement.

I would therefore encourage the authors to make the Hankel mechanism more central, not less.

But to justify a general top-four placement, the paper still needs a theorem that uses the Hankel restriction in an essential way. At present many downstream statements need only \(Q>0\), not \(Q^{-1}\) Hankel.

This is another formulation of the central-coupling problem: the most distinctive native structure is derived, but then much of the rest of the paper treats the metric as a generic positive definite matrix.

## 20. The response to R106: item-by-item assessment

For clarity, here is my assessment of the previous numbered requests.

### R106.1 — central structural theorem

**Partially closed, not fully closed.**

The synchronized-root theorem is a substantial response because it places a genuinely nonlinear residual, native information, and endpoint reconstruction in one observation model. However, the interaction is still factorized as explained in Sections 3–4.

### R106.2 — intrinsic objects versus marked certificates

**Substantially closed.**

The fast-coordinate transition proposition and counterexample now make the dependence of the derivative certificate mathematically explicit.

### R106.3 — genuine stability

**Closed for the stated weighted-leading-map class.**

The coefficient family may vary without preserving a fixed resolution/order vector. This is the right kind of positive theorem. It does not imply arbitrary singular-germ stability, and the manuscript appropriately says so.

### R106.4 — critical-boundary theory

**Substantially closed at the level of a broad sufficient normal-form class.**

The weighted theorem plus synchronized quadratic cone goes well beyond one cubic example. It is not a classification of all critical germs, but the manuscript no longer needs to pretend that it is.

### R106.5 — endpoint proof architecture

**Closed to my satisfaction for the first strata.**

The KKT fan tables and reconstruction lemmas materially improve auditability.

### R106.6 — Hankel novelty and priority

**Improved but not closed.**

The theorem-level comparison is much better, but the inverse-parametric-QP omission is material, and the fixed-budget theorem also needs a more precise novelty comparison.

### R106.7 — fixed-total-exposure geometry

**Closed mathematically, pending positioning.**

There is now a genuine theorem rather than a defining equation.

### R106.8 — dependency and provenance map

**Closed in source organization.**

The new table is useful and appropriately distinguishes retained from new results.

### R106.9 — source-bound native build/replay

**Not closed at the reviewed HEAD.**

The first v107 native workflow failed the manuscript build/reference criterion; the HEAD follow-up was still queued when this report was completed.

## 21. Required next revision

If this manuscript is to be reconsidered at the same general top-four standard, I would require the following rather than another accumulation of local patches.

### R107.1 — Prove an interaction theorem, not only a coexistence theorem

Give a theorem in which the synchronized residual geometry and the native Hankel information geometry constrain one another.

A result that would remain unchanged after replacing \(Q\) by an arbitrary positive definite matrix is not sufficient for this purpose.

### R107.2 — Decide what the paper's single principal theorem is

The current title suggests that the answer should be the synchronized-root/Hankel theorem.

If so, reorganize the article so that every major imported result is visibly either:

- an input to that theorem;
- a consequence of that theorem;
- or a clearly segregated companion result.

The paper should no longer read like a chronological union of v104, v106, and v107 advances.

### R107.3 — Correct the scope of the all-strata endpoint theorem

Either:

- state plainly that it is a finite semialgebraic equality test relative to a supplied reference representation, or
- upgrade it to a genuinely intrinsic inverse theorem whose input is the labelled value function rather than a hidden reference \(Q\).

Do not use Hardt triviality to imply an explicit normal-form classification that it does not provide.

### R107.4 — Add the inverse-parametric-QP literature and compare hypotheses theorem by theorem

At minimum discuss Hempel–Goulart–Lygeros (2012) and Nguyen–Olaru–Rodriguez-Ayerbe–Hovd–Necoara (2017), and explain exactly why the present value-function/minimal-endpoint problem is different.

This comparison should be in the manuscript, not only in a response letter.

### R107.5 — Establish the novelty of the fixed-budget fibre theorem

Separate the general reciprocal-fibre geometry from what is forced by the binary model, and compare the resulting image/fibre classification with design-equivalence and fixed-support moment-space literature.

### R107.6 — Use the Hankel restriction in a genuinely downstream theorem

The paper derives a distinctive Hankel constraint but often uses only \(Q>0\) afterward. Produce at least one central consequence that fails for a generic metric and depends essentially on the fixed-clock Hankel class.

### R107.7 — Tighten the principal statements

In particular:

- distinguish full residual from its nuisance quotient in the abstract;
- keep the target domain \(b\ge0\) explicit;
- define the uniform spanning margin;
- distinguish positive-exposure image boundaries from closure with zero exposures;
- maintain the limited claim of the overidentified counterexample.

### R107.8 — Close source-bound replay at the exact reviewed source

The final revision should have a successful native build at its exact commit, no unresolved citations/references, a source manifest, and the already useful finite-check receipt.

Again, this is archival evidence only. It does not replace proof.

## 22. Minor comments

1. The title is now much better aligned with the strongest new mathematics than the historical A2 title, but the body still contains several older centres of gravity that do not obviously belong under it.

2. The abstract should replace “the complete leading residual is a linear image of a rank-one quadratic measurement cone” by a formulation that mentions the free score directions and endpoint orthant, or explicitly says “after quotienting the free score directions.”

3. The phrase “every such nonlinear contact” should specify the fixed native experiment and the allowed target domain.

4. The stronger-than-necessary assumption that \(\{a_i a_i^{\mathsf T}\}\) spans \(\operatorname{Sym}_d\) is fine for a clean theorem, but the paper should not let readers confuse it with a sharp phase-retrieval measurement condition.

5. In the fixed-budget section, use “relative boundary in the open moment cone” consistently.

6. The exact seven-clock obstruction is valuable. Keep the explicit sentence that it does not exclude every possible alternative congruence.

7. The finite symbolic checks are well chosen. Continue to label them as finite examples and identities rather than verification of the universal theorems.

8. The language-model disclosure is appropriately separated from mathematical validation. Keep that separation.

9. The dependency table is useful enough that it should remain even after a full editorial rewrite.

10. The manuscript should use “intrinsic” with an explicit category attached whenever possible: intrinsic residual germ, intrinsic labelled value function, intrinsic statistical experiment, or marked-presentation certificate.

## 23. Final assessment

Revision 107 is a serious mathematical revision.

The synchronized-root cone is a genuine nonlinear observation singularity. The Hellinger contact calculation is well organized. The fixed-budget theorem is a meaningful new piece of geometry. The weighted leading-map theorem supplies the coefficient stability that was absent before. The endpoint proof architecture is now much easier to audit. The manuscript is also considerably more disciplined about provenance, assistance, and the limits of finite computation.

Those are all real achievements.

But a general top-four journal needs more than a collection of correct and interesting theorems. It needs an unmistakable conceptual centre whose consequences justify the breadth of the paper.

I do not yet see that centre in v107.

The current central theorem says, in effect, that a natural synchronized subfamily supplies a nonconvex rank-one quadratic feasible cone, the ambient binary experiment supplies a Hankel-constrained efficient metric, and a previously reconstructed endpoint profile supplies that metric. The combination is mathematically legitimate, but the two principal structures do not yet constrain one another in a way that makes the whole greater than the parts.

The endpoint theory has also not been globally solved in the intrinsic inverse sense suggested by some of the surrounding rhetoric: the arbitrary-stratum theorem is a finite equality test relative to a reference representation. And the literature review, although greatly improved, still omits directly relevant inverse-parametric-quadratic-programming work.

For these reasons I would not recommend acceptance, and I would not characterize the remaining work as a routine major revision. A successful next version would need a conceptual re-centering and at least one genuinely non-factorized theorem.

**Recommendation: reject in the present form, with a substantially more positive assessment of the mathematics than for v106.**
