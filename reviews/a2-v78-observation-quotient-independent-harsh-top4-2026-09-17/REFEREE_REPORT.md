# Independent harsh referee report on A2 revision 78

**Manuscript:** *Marked clocked laws and reconstruction of generating actions*  
**Author:** Qian Qi  
**Date:** September 17, 2026  
**Reviewed source branch:** `revision/a2-v78-observation-quotient-root-free-2026-09-17`  
**Reviewed head:** `9b0b6c25a3194cb99ba719d118c00a23dfb8febe`  
**Reviewed head tree:** `9c7d4a9f610b67b3f63b95adaf9fe245c91f1fb5`  
**Previous substantive revision:** `revision/a2-v77-three-clock-smooth-atlas-2026-09-17` at `97d1ead42809508cea508ee44576e71b95fdcc06`  
**Revision delta:** 4 commits ahead of that v77 head, with no commits behind  
**Prior controlling report inspected:** `reviews/a2-v77-three-clock-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md`  
**Requested standard:** the level expected of *Annals of Mathematics*, *Inventiones Mathematicae*, *Acta Mathematica*, or the *Journal of the American Mathematical Society*.

This is an author-requested independent referee-style assessment, not a commissioned journal report or an editorial decision. I deliberately apply the severe standard appropriate to the four leading general mathematics journals. I distinguish three questions that should not be conflated:

1. whether the displayed mechanisms are mathematically coherent under their stated hypotheses;
2. whether revision 78 genuinely answers the previous referee objections;
3. whether the resulting theorem package has the conceptual depth, naturality, breadth and literature position required for a top-four general journal.

My conclusions on these three questions are different.

## 1. Recommendation

**I would not recommend acceptance at the requested top-four general-journal level in the present form.**

Revision 78 is a real and substantial improvement over revision 77. It is not a cosmetic relabelling. The authors have done three things that directly answer the previous report:

- they separate the principal clocked-action article from the large inherited periodic companion;
- they remove the supplied matching-root bracket by proving a root-selection-free theorem;
- they add a fixed six-law inverse problem for a whole infinite-dimensional class of uniformly convex discrete mechanical systems, rather than relying only on a billiard atlas selected around an individual table.

I also do **not** find a fatal local algebraic error in the new three-clock quotient, the downward-zero/root-selection argument, the strongly convex mechanical reconstruction, or the displayed finite-record rate. The current negative recommendation is therefore not a disguised claim that the paper is obviously false.

The remaining difficulty is more fundamental. Revision 78 now makes explicit that, in its exact shared-weight model, the three clocked laws modulo common positive reweighting carry **exactly the same information as the absolute action function**. This is a useful clarification, but it removes a possible source of conceptual novelty: the statistical layer is an invertible encoding of action data, not a weaker information class. Once the action is recovered, the central inverse steps are generating-function composition, a one-dimensional uniqueness argument at matching roots, and finite Euclidean distance reconstruction. These are elegant and competently assembled, but the manuscript does not yet demonstrate that this synthesis constitutes a new principle of the depth expected by a top general journal.

The billiard theorem also remains based on a highly marked, reference-dependent acquisition architecture: exact branch identities, obstacle and lift labels, scalar boundary coordinates, prescribed branch/prefix pairings, branch-specific gates, admissible absolute clocks and a cross-clock shared-weight hypothesis. Root brackets and anchor marks are now successfully removed, but the observation operator is still not a single natural, table-independent datum on a broad billiard class.

The new discrete-mechanical theorem is mathematically cleaner in this respect because its endpoint gates and thresholds can be fixed over the class. However, the observation is an **action-threshold experiment**: a trajectory is retained according to the inequality `alpha + S_n(s,t) < T`. This is an intentionally engineered observation rule that directly thresholds the unknown action itself. Unless the paper supplies an independent physical or geometric mechanism realizing that event without already having access to the action, the example demonstrates a mathematically valid encoding theorem rather than resolving the natural-observation objection that remains in the billiard problem.

Finally, the literature positioning is currently far below the standard required for a top-four submission. The principal article has only four bibliography entries despite making claims across dispersing-billiard rigidity, exact twist/generating functions, discrete variational mechanics, distance geometry and nonparametric reconstruction. A paper making a broad conceptual claim about “reconstruction of generating actions” cannot establish novelty with such a bibliography.

The right editorial description is therefore: **substantial mathematical progress, no obvious fatal flaw in the audited core, but the top-four significance case is not established and several statements still overstate the proved scope.**

## 2. Scope of this review

I audited the source actually active at the pinned v78 head rather than treating build scripts or repository labels as mathematical certification. The principal entry point is

- `papers/A2-v17-boundary-information-coarsening/rigidity_v78.tex`.

It assembles the new v78 sections

- `article/v78/01_introduction.tex`;
- `article/v78/02_information.tex`;
- `article/v78/03_root_free.tex`;
- `article/v78/04_mechanics.tex`;
- `article/v78/05_uniform_records.tex`;

with the inherited v77 physical-clock, prefix-cancellation, distance-registration and finite-coverage sections.

I also inspected

- `periodic_companion_v78.tex` and `article/v78/determinant_dependencies.tex` to verify the claimed architectural separation;
- the prior v77 harsh report and the v77 response materials;
- `tools-v78/check_revision_v78.py` and the v78 build workflow at the level relevant to understanding what is and is not being checked.

The repository diagnostics contain useful symbolic and numerical consistency checks. I do not count them as proof verification. The conclusions below are based on the written mathematics and on independent algebraic checking of the displayed identities.

For literature positioning I also checked the immediately neighboring published/preprint record, including:

- L. Noakes and L. Stoyanov, *Lens Rigidity in Scattering by Unions of Strictly Convex Bodies in R^2*, SIAM J. Math. Anal. 52 (2020), 471–480;
- P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, Homoclinic Orbits and the Geometry of Open Dispersing Billiards*, Comm. Math. Phys. 374 (2020), 1531–1575;
- D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983 (2025);
- the standard exact-twist/generating-function and discrete-variational literature, including the classical discrete-mechanics framework of Marsden–West.

The omission of the Bálint–De Simoi–Kaloshin–Leguil paper from the v78 principal bibliography is especially conspicuous because it is directly about marked length information and geometry in dispersing billiards.

## 3. What revision 78 genuinely fixes

A harsh report should record actual progress rather than mechanically repeat old objections.

### R78-C1. This is a genuine source revision

Relative to the substantive v77 head `97d1ead...`, v78 is four commits ahead. The mathematical commit introduces the exact observation quotient, root-selection-free matching, the fixed-class mechanical application, the focused principal article and the separated periodic companion. The latest head then adds reproducible build and diagnostic infrastructure.

The new source should therefore be reviewed on its own merits. It would be incorrect to recycle an earlier objection that there is no mathematical delta.

### R78-C2. The paper architecture is materially improved

The principal paper `rigidity_v78.tex` is now focused on the clocked-action principle and its two applications. The inherited periodic determinant/contact theory is moved to `periodic_companion_v78.tex` rather than being concatenated as the second half of the same principal article.

This substantially answers the v77 complaint that two logically independent inverse problems had been merged into a single oversized manuscript. The companion may still require its own editorial evaluation, but the principal article now has a recognizable spine.

### R78-C3. The exact observation quotient is algebraically correct under the stated model

For fixed clocks and a common positive weight,

\[
 f_j=\frac{a(T_j-W)}{\int a(T_j-W)}
\]

indeed determines the absolute action `W` and the nuisance shape `a/a(z_0)`. Multiplying all three laws by a common positive function and renormalizing changes only `a`, so the orbit under common reweighting is indexed by `W`.

At the set-theoretic level, the statement

\[
 \mathscr L/\{\text{common positive reweightings}\}\simeq \mathscr W
\]

is correct for the model image `mathscr L` as defined in the paper. The two-clock fractional-linear ambiguity exhibited later is also a valid ambiguity in the unrestricted weighted-function model.

This is a useful clarification because it prevents the paper from suggesting an information ordering that has not been proved.

### R78-C4. The root-selection-free argument is a real improvement

The key new observation is that at **every actual zero** of

\[
 H(s,t,v)=V_s(s,v)-U_s(s,t),
\]

determinism identifies the physical prefix and the positive stationary Schur complement gives

\[
 H_s=-\frac{U_{st}^2}{B}<0.
\]

A `C^1` scalar function whose every zero is crossed downward has at most one interior zero. Therefore the endpoint sign test on a connected initial interval determines whether the physical match exists, and no externally supplied root label or local root bracket is needed.

This is stronger than the v77 local implicit-function statement. I do not see a defect in the one-dimensional downward-zero lemma or in its application **provided** the theorem hypotheses guarantee that every zero lies on the same physical branch family; I return to the need to state that hypothesis more explicitly below.

### R78-C5. The abstract generating-action theorem is formally valid under its hypotheses

Once equality of initial covectors is assumed to identify a common deterministic trajectory and the matched stationary composition has positive `B`, the same argument reconstructs the one-step generating function from long actions.

The proof is short because the real content has been packed into the hypotheses, but the implication itself is correct.

### R78-C6. The fixed-class discrete mechanical theorem is mathematically coherent

For

\[
 L_{\mu,P}(x,y)=\frac\mu2(y-x)^2+P(x),\qquad
 0<\kappa\le P''\le\Lambda,
\]

the stationary action is strongly convex in the interior variables. The tridiagonal Hessian is positive definite, the corner-cofactor formula gives the nonzero mixed twist, and the backward recurrence bounds the required initial coordinate uniformly on fixed endpoint gates.

The threshold bounds are also internally consistent: uniform lower and upper action bounds allow one set of three thresholds to work for both `S_n` and `S_{n+1}`. After recovering the one-step `L`, the mass is obtained exactly from a second finite difference in the second variable and `P(t)` follows by subtraction.

I do not find an algebraic error in this theorem.

### R78-C7. The long-prefix conditioning cost is no longer hidden

The explicit lower bound for the mixed derivative decays with prefix length, and the matching derivative inherits its square divided by a Schur bound. The billiard uniform section similarly retains a possible exponential conditioning penalty through `u_*` and charges rare retained successes through `p_*`.

This is preferable to presenting long prefixes as cost-free simply because the inverse is exact.

### R78-C8. The finite-record theorem has the correct qualitative nonparametric scaling

For a two-dimensional density, estimating derivatives of order `m=k+2` from `C^{m+s}` smoothness gives a bias of order `h^s` and stochastic size of order

\[
 (n h^{2m+2})^{-1/2}
\]

up to logarithms. Balancing these terms produces the displayed exponent

\[
 \frac{s}{2(k+2+s)+2}.
\]

The deterministic coordinate-error term `delta/h^{m+3}` likewise gives the displayed power of `delta` after balancing with `h^s`.

I have not found a dimension/exponent mismatch in the stated sufficient rate. It is appropriately not claimed to be minimax.

## 4. Major concerns

The following issues prevent a positive top-four recommendation.

### R78-M1. The new quotient theorem clarifies the information content, but it also removes the statistical layer as the main source of novelty

This is the central conceptual issue in revision 78.

The paper now proves that, within the exact model image and modulo a common positive reweighting, three normalized endpoint laws are equivalent to the absolute action. Thus the inverse problem factors as

\[
 \text{three exact normalized laws}
 \longleftrightarrow
 \text{absolute action}
 \longrightarrow
 \text{one-step generating function}
 \longrightarrow
 \text{geometry}.
\]

This is clean. It is also much less mysterious than the earlier narrative suggested.

For a top general journal, the manuscript must therefore make a compelling case that one of the **post-action** arrows contains a genuinely new, broadly important rigidity principle. At present:

- prefix cancellation is a generating-function composition identity plus a scalar root argument;
- the root-free upgrade is a useful monotonic-crossing observation once determinism and positivity are assumed;
- Euclidean patch recovery is an explicit finite distance-geometry solve;
- finite coverage uses compactness, visibility and local regular branch construction.

The synthesis is nontrivial, but the manuscript does not yet establish why this combination reaches the conceptual threshold of the four leading general journals.

The authors should not try to repair this by reintroducing claims that the normalized laws are intrinsically weaker than action data. Revision 78 correctly proves the opposite equivalence in the stated model. The significance argument must instead be rebuilt around a genuinely new rigidity theorem after the quotient has been taken.

### R78-M2. The billiard observation operator remains highly marked and reference-dependent

Root brackets and action-anchor marks have been removed, which is a real gain. However the billiard experiment still assumes substantial structure that is not reconstructed:

- an exact scalar boundary label space and its charts;
- obstacle identities and lattice-lift labels;
- exact reflection words / branch identities;
- exact association of a prefix branch with its one-flight extension;
- branch-specific endpoint gates;
- three admissible absolute clock times for every measured branch;
- the same preparation/retention multiplier across the clocks of a branch;
- branch resolution, so mixtures of different physical branches are not part of the data.

The finite-atlas theorem says that **for each table** one can choose a finite identifying experiment and that the same experiment persists on a neighborhood. The reference-uniform theorem then fixes that list on the chosen neighborhood. This is not the same as injectivity of one natural observation map on a broad class.

This distinction is decisive at top-four level. The theorem is global in the reconstructed target but local/reference-dependent in the acquisition design.

A major conceptual strengthening would be one of the following:

1. a table-independent acquisition rule with a proved finite stopping procedure on a substantial billiard class;
2. a canonical observation operator whose branch/gate structure is intrinsic rather than selected from the unknown table;
3. reconstruction when important labels are absent or only partially resolved;
4. a theorem showing that the existing marked data are unavoidable by constructing genuine nonidentifiability without them.

Without such a step, the paper should state its result as an **identifying marked experiment attached to a table**, not as a general natural-data rigidity theorem.

### R78-M3. The mechanical “fixed protocol” is mathematically valid but experimentally engineered around the unknown action

The new mechanical example is intended to answer the previous objection that the billiard experiment is object-dependent. Formally it succeeds: the gates and thresholds can be fixed over the whole class.

But the retained event is defined by

\[
 \alpha+S_n(s,t)<T.
\]

The unknown stationary action itself therefore appears in the data-acquisition mechanism. The paper says, correctly, that the device does not record an individual action value. That does not remove the conceptual issue: in order to implement this retention event, some physical or algorithmic mechanism must respond to the accumulated action.

As an abstract statistical experiment this is legitimate. As evidence that the general principle arises from natural inverse data, it is much weaker.

The authors should either:

- derive this threshold event from an independently specified physical process in which `S_n` is naturally accumulated and thresholded; or
- explicitly present the mechanical theorem as an abstract encoding application and supply a different natural fixed-protocol application; or
- prove a general theorem showing that action-threshold observations arise canonically in a broad class of systems.

At present the example risks looking designed specifically so that integration in the auxiliary variable produces the factor `T-S_n` needed by the clock algebra.

### R78-M4. The abstract generating-action theorem is close to being a repackaging of its hypotheses

The general scalar theorem assumes:

- deterministic twist dynamics;
- equality of initial covectors identifies the common trajectory;
- a stationary composition with a positive Schur complement at every match;
- three clocked laws already giving absolute long actions.

Under these hypotheses, the conclusion follows by differentiating the stationary composition and applying the downward-zero lemma. The theorem is correct, but the genuinely difficult part has largely been assumed.

To justify the title’s broad emphasis on “reconstruction of generating actions,” the manuscript should demonstrate a substantial family beyond the two hand-built examples for which these hypotheses are nontrivial to verify and the resulting inverse was not already implicit in standard twist-map/generating-function theory.

A top-four theorem should not obtain breadth merely by abstracting the notation of a short argument. The abstraction must buy a new class, a new invariant, a sharp obstruction, or a reusable theorem whose verification is itself substantive.

### R78-M5. The exact shared-weight hypothesis is structurally fragile and the manuscript has no model-misspecification theorem

The three-clock inverse depends crucially on the same unknown multiplier `a(z)` occurring at all clocks of a branch. The paper correctly notes that an arbitrary clock-dependent weight can absorb a change in `W`.

This means identifiability is discontinuously tied to an exact structural equality in the nuisance model. The finite-record theorem treats sampling noise around a perfectly specified model; it does not address even a small violation of the common-weight assumption.

For a paper that presents statistical records as a central observation interface, the absence of a misspecification result is serious. At minimum one needs a theorem of the form:

- if the three weights are `a(1+epsilon_j)` with controlled `C^m` discrepancies, what bias is induced in the recovered action?;
- which component of clock-dependent nuisance is identifiable and which is genuinely confounded with `W`?;
- is there an overidentified four- or five-clock version that permits testing or estimating departures from the common-weight model?

Without such analysis, the “statistical” inverse is exact but brittle.

### R78-M6. The literature review is not remotely sufficient for the breadth of the claims

The v78 principal bibliography contains only four entries. This is not a cosmetic issue.

The article invokes or relies on ideas from:

- dispersing billiards and inverse billiard geometry;
- marked length and lens/scattering rigidity;
- exact symplectic twist maps and generating functions;
- variational composition of discrete actions;
- discrete Lagrangian mechanics;
- Euclidean distance geometry / global rigidity;
- nonparametric density-derivative estimation;
- statistical inverse problems and identifiability under nuisance reweighting.

The current references do not adequately map that landscape.

Most strikingly, the principal paper does not cite Bálint–De Simoi–Kaloshin–Leguil (Comm. Math. Phys. 374 (2020), 1531–1575), a directly relevant paper on marked length spectrum and the geometry of open dispersing billiards. The paper also needs proper engagement with the standard exact-twist/generating-function literature and with discrete variational mechanics; a statement that generating-function composition is “classical” is not a literature comparison.

Before any priority or top-four significance claim can be evaluated, the authors must expand the related-work discussion enough to answer:

1. which part of the clock/action quotient is new;
2. which part of root-free composition is new relative to standard twist-map generating functions;
3. which billiard rigidity conclusions are stronger, weaker or incomparable to existing marked-length/lens results;
4. what is new in the discrete mechanical inverse relative to the discrete-calculus-of-variations literature;
5. whether the finite distance certificate is used merely as a self-contained tool or is claimed as a new rigidity contribution.

At the present level, the paper has not earned its novelty claims bibliographically.

### R78-M7. Several headline statements are broader than the theorems actually proved

There are at least two concrete scope mismatches.

**(a) “Whole smooth potential.”**  
The abstract and introduction say that the fixed six-law mechanical protocol recovers “a whole smooth potential.” The theorem fixes `R>0` and recovers only

\[
 P|_{[-R,R]}.
\]

For every larger `R` one can design another fixed protocol, but one finite protocol in the theorem does not recover the entire function on `\mathbb R`. The abstract must say “the potential on any prescribed compact interval” or an equivalent precise formulation.

**(b) “Bounded billiard classes.”**  
The abstract says that “On bounded billiard classes” the constructive finite-record inverse is available. The actual theorem fixes a **bounded neighborhood carrying one fixed reference atlas and positive certificate margins**. It explicitly says that uniformity is not asserted on the union of all such neighborhoods.

The abstract should reflect that narrower statement. A bounded set of positive-curvature billiards need not carry common branch, clock, rank, nongrazing and overlap margins merely because it is bounded in a smooth norm.

At a top journal, these distinctions must be exact in the title page, abstract and main theorem statements, not repaired only deep in the proofs.

### R78-M8. The finite-record cost model still hides part of the branch-resolution burden

The sampling theorem commendably charges every attempted setting and includes a retained-success floor `p_*`. However, the meaning of one “setting” already includes exact branch resolution, scalar gates and branch-specific preparation conventions.

The theorem should make completely explicit whether an attempt means:

1. the apparatus is able to prepare a state in the required branch/gate setting by design; or
2. the apparatus launches from a broader source and later classifies a successful trajectory into its exact branch/lift word.

Those are different experimental costs. If branch classification occurs after launch, the probability of hitting the desired branch and correctly assigning its word must be included in the preparation budget. If branch preparation is assumed, that ability is itself part of the marked observation model and should be stated in the theorem.

This is not a complaint that every inverse problem must model laboratory engineering. It is a complaint that the paper makes a finite-preparation claim while some of the most informative marks are built into the definition of a setting.

### R78-M9. The quotient-space language is stronger than the topology actually defined

The set-theoretic orbit statement is clear. The phrase “the identification is locally Lipschitz” is less clear when written as an assertion about

\[
 \mathscr L/G\simeq\mathscr W.
\]

No quotient metric or Banach-manifold structure on `\mathscr L/G` is defined. What the proof actually establishes is that, for representatives satisfying uniform denominator bounds, the explicit recovery map from the three density functions to `W` and `a/a(z_0)` is locally Lipschitz in fixed `C^m` norms.

The paper should either define the quotient topology/norm being used or restrict the theorem to this representative-level stability statement. “Isomorphism” should also be qualified as set-theoretic unless additional structure is proved.

### R78-M10. The physical-branch hypothesis behind “every zero is physical” should be stated more explicitly

The new root-free theorem depends on a subtle but essential point: whenever

\[
 V_s(s,v)=U_s(s,t),
\]

the two stationary actions must correspond to physical trajectories in the same deterministic branch family, with the same outgoing half-plane, so equality of the initial covector forces the whole common prefix to coincide.

The proof explains this informally. The theorem statement should encode it explicitly.

For arbitrary stationary generating functions, equality of initial covectors does not by itself guarantee that two different stationary branches have the same physical itinerary. The abstract theorem later adds a “common trajectory” hypothesis; the billiard theorem should be equally explicit that `U` and `V` are single-valued regular **physical branch actions on the whole product domain under consideration**, not merely smooth stationary-value branches obtained by continuation.

I believe this condition is intended and is satisfied in the local branch construction. It should nevertheless be stated because the new global root-free conclusion rests on it.

## 5. Minor and presentation issues

These are secondary to the major concerns but should be corrected in any revision.

### R78-m1. State exactly what is meant by “absolute action”

In symplectic/generating-function language an additive constant is usually a gauge. Here the absolute clock values remove that gauge. The introduction should say this once explicitly and distinguish it from the canonical relation, which determines only `dW`.

### R78-m2. Separate model identification from model validation

The quotient theorem assumes the observed triple lies in the model image `\mathscr L`. It does not provide a criterion for testing whether three arbitrary density functions have that form. This is fine, but should be said next to the theorem, especially because the later finite-record data are off-model before smoothing error vanishes.

### R78-m3. The two-clock ambiguity should remain carefully scoped

The paper currently says the right thing: the fractional-linear deformation is an ambiguity in the unrestricted weighted-function model and is not asserted to come from two noncongruent billiards. Keep this qualification prominent. Do not market the third clock as a sharp *physical billiard* threshold unless an actual realizability/nonidentifiability theorem is proved.

### R78-m4. The paper should distinguish “fixed protocol” from “fixed nuisance law”

In the mechanical theorem the gates, thresholds and auxiliary interval are fixed across the class, while the unknown source/efficiency functions may vary subject to the cross-threshold sharing rule. This is mathematically acceptable but should be spelled out in the theorem to prevent “fixed protocol” from being read as a fixed full data-generating distribution.

### R78-m5. Clarify what part of the scalar atlas is observation and what part is gauge

The atlas coordinates and overlap maps are known labels, whereas Euclidean speed, tangent and normal are not known. This is stated, but the distinction is important enough to repeat in the main theorem rather than leaving it in the experiment subsection.

### R78-m6. The principal article should cite the source of standard billiard generating-function identities

The identities `p=-W_s`, `q=W_t`, twist nondegeneracy and variational composition are central to the argument. Even if the paper proves the needed local facts, a serious general-journal manuscript should locate them in the classical billiards/twist-map literature.

### R78-m7. Avoid using verification artifacts as rhetorical evidence of proof depth

The v78 checker is well designed as a regression test: it checks symbolic identities, nonanalytic mechanical fixtures, roots and conditioning numerically. The manuscript and any response letter should continue to state that these are diagnostics, not independent mathematical certification.

### R78-m8. A v78 response/roadmap file would improve traceability

The branch contains the v77 report but no concise v78 response explaining which old major objections are claimed to be closed. This is not a mathematical defect, but after dozens of historical revisions a short point-by-point response would make the active logical delta far easier to audit.

## 6. What would materially change the top-four assessment

Another round of local estimates or a longer appendix would not address the principal objection. A materially stronger revision would need at least one conceptual advance of the following type.

### Path A: a natural fixed billiard observation operator

Prove injectivity for one table-independent observation map on a broad class, rather than first selecting a finite atlas from each reference table. Ideally remove or infer some of the exact branch/lift labels.

### Path B: a sharp information theorem

Give a genuine identifiability/nonidentifiability classification for clocked laws under progressively weaker nuisance assumptions. For example, identify the maximal clock-dependent reweighting class under which `W` remains recoverable, or prove an actual billiard counterexample below the threshold.

### Path C: a robust quotient theorem

Develop the clock quotient as a substantive statistical inverse problem: approximate common weights, overidentification with more clocks, model testing, optimal stability or minimax lower bounds. This would make the statistical layer mathematically meaningful beyond exact algebraic inversion.

### Path D: a genuinely broad generating-action theorem

Find a nontrivial class of deterministic generating systems for which the physical-match hypothesis and positivity are consequences of intrinsic geometry, and derive a rigidity theorem not already implicit in standard twist-map composition. The current mechanical example alone is too engineered to establish this breadth.

### Path E: a substantially stronger natural mechanical inverse

Replace action-threshold retention by observations generated from a natural trajectory process that does not directly threshold the unknown action, while retaining fixed acquisition over the class.

Any of these could change the significance assessment. Merely polishing the existing exact inverses would not.

## 7. Required corrections even for a specialist-journal version

Independently of top-four placement, I would require the following before publication elsewhere:

1. correct “whole smooth potential” to recovery on a prescribed compact interval, unless a single global protocol is actually proved;
2. correct “bounded billiard classes” to the fixed-atlas bounded neighborhoods for which uniform margins are established;
3. expand the bibliography and related-work discussion substantially, including the directly relevant 2020 marked-length paper of Bálint–De Simoi–Kaloshin–Leguil and standard twist/discrete-variational references;
4. state the physical single-branch hypothesis explicitly in the root-free theorem;
5. define the topology/metric intended by the quotient-space Lipschitz language or rewrite the statement at representative level;
6. state the experimental meaning and cost of exact branch resolution in the finite-record theorem;
7. explain whether the action-threshold mechanical experiment is intended as a physical model, an abstract statistical experiment, or both;
8. keep the principal article and periodic companion separate.

## 8. Final assessment

Revision 78 deserves credit for responding intelligently to the previous harsh review. The authors have removed a supplied root-selection mark, isolated a clean exact observation quotient, produced a fixed-class mechanical inverse, exposed long-prefix conditioning, strengthened the finite-record output and separated the principal theorem from the inherited periodic companion.

The central formulas I audited are coherent under their stated hypotheses. I would not reject this work on the ground that the new mathematics is obviously wrong.

I would nevertheless reject it **at the four-leading-general-journal level in its current form**. The paper has not yet crossed the conceptual threshold from an elaborate exact encoding-and-reconstruction scheme to a broadly compelling rigidity theorem. Its natural billiard data remain heavily marked and reference-dependent; its fixed mechanical observation is engineered around an action threshold; the exact quotient shows that the normalized-law layer is information-equivalent to action data; and the bibliography is too thin to establish priority or conceptual separation from the surrounding rigidity, twist-map and discrete-mechanics literature.

The appropriate next revision is therefore not “more details everywhere.” It is a narrower and harder task: identify the one genuinely general rigidity principle that survives after quotienting out the statistical encoding, formulate it against a natural observation class, and position it rigorously against the existing literature.