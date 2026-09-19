# Independent harsh referee report on A2 revision 96

**Review date:** 20 September 2026  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** `revision/a2-v96-uniform-stratified-spectral-laws-2026-09-20`  
**Reviewed exact head:** `423a0e135c217d6dc42fc973d8da4ee13893e865`  
**Immediate manuscript predecessor:** `revision/a2-v95-real-valuations-cubic-classification-2026-09-19` at `ebb796e49ca51a62b90d92ec0d09819cfe8d00a4`  
**Latest prior independent A2 referee report found in the repository:** `reviews/a2-v95-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`  
**Prior review commit:** `c020b5ede3ca07852db4166f614354341b0d8494`  
**Reviewed manuscript:** *Projective polynomial observations: real valuations and stratified spectral laws*  
**Author:** Qian Qi  
**Review status:** owner-requested AI-assisted external-referee-style assessment; not a journal-commissioned peer review.

## 1. Recommendation

**Recommendation to the editor: reject in the present form at the Annals/Inventiones/JAMS/Acta level.**

This is a substantially more positive mathematical assessment than I would have given several revisions ago, and it is not based on a newly discovered fatal counterexample. Revision 96 contains real theorem-level progress. In particular, I find the following additions serious:

1. the exact spectral fibre is classified across both ranks of the first channel for the named binary cubic family, including the weight-isolated rank-one region;
2. the pointwise leading-fibre calculation is upgraded to a whole-model Hausdorff normal form uniform on compact subsets of the identifiable region;
3. the leading constant is reduced to finitely many active-set tests, giving a semialgebraic phase partition and exact rational formulas for (C^4);
4. continuity across active-set changes and across identified channel-rank changes is addressed at theorem level rather than left as a numerical observation;
5. two rational examples are supplied with exact arithmetic rather than floating-point fitting.

I did not find a responsible basis for calling these results false. The discriminant calculation, stochastic affine-pencil reconstruction, Schur-complement Fisher program, KKT active-set reduction, radial realization argument, and diameter computation are internally coherent on the stated domain.

However, the manuscript still does not meet the standard of a leading general mathematics journal. The central reasons are now conceptual rather than merely local:

- the claimed “stratified spectral laws” are a finite chamber decomposition **inside one fixed binary cubic singularity type**, not a general singularity stratification;
- the broad real-valuative theorem remains very close to classical resolution/Łojasiewicz technology and to current valuative finite-max theory, and revision 96 does not give the theorem-by-theorem novelty separation requested by the latest referee;
- the general “effective finite algorithm” remains compressed at precisely the points where the previous report asked for proof-grade specifications;
- the strongest uniform theorem is only compact-interior uniformity on the identifiable set; the behavior as one approaches the actual identification walls is still not classified;
- the complete manuscript remains an accretive research-program compendium even though the preceding report explicitly asked either for conceptual generalization or for architectural narrowing;
- most seriously as a review-process matter, revision 96 declares revision 94 to be the controlling report and says that no later A2 report was found, even though the independent v95 report had already been committed to the repository before the v96 head was created.

I therefore do **not** recommend another local “closure round” at the same venue. A future top-four submission needs either a genuinely broader singularity-atlas theorem or a substantially narrower article with a much sharper novelty boundary.

## 2. Source pin, chronology, and scope of this review

Revision 96 is exactly one commit ahead of revision 95. The v95 head is

`ebb796e49ca51a62b90d92ec0d09819cfe8d00a4`,

and the v96 head is

`423a0e135c217d6dc42fc973d8da4ee13893e865`.

The v95-to-v96 delta is addition-only and consists of the new v96 article modules, revision packet, diagnostics, exact-arithmetic evaluator, source-audit script, and branch-scoped workflow. The complete entrypoint is

`papers/A2-v17-boundary-information-coarsening/rigidity_v96.tex`,

which imports `article/v96/paper.tex`. The latter imports the v95 model and real-valuative theorem, then the new v96 family classification, uniform normal form, and active-set sections, followed by the retained historical appendices.

I reviewed, in particular:

- `article/v96/paper.tex`;
- `article/v96/family.tex`;
- `article/v96/uniform_normal_form.tex`;
- `article/v96/active_sets.tex`;
- the unchanged v95 `finite_newton.tex`;
- the relevant literature discussion and added bibliography;
- `revisions/a2-v96/RESPONSE_TO_REFEREE.md`;
- `revisions/a2-v96/MATH_DIAGNOSTICS.json`;
- `revisions/a2-v96/EXACT_CONSTANTS.json`;
- `scripts/verify_a2_v96_math.py`;
- the exact-head audit/workflow definitions;
- the independent v95 referee report.

I have treated the finite symbolic and numerical diagnostics as regression evidence only, exactly as the branch itself instructs. They are not proof verification.

### 2.1 A concrete source-control problem: v96 did not use the actual latest report

The v96 response begins by stating that the controlling report is the v94 report and says:

> No later A2 report was found in the review branches inspected for this revision.

That statement is inconsistent with the repository chronology.

The independent v95 review commit

`c020b5ede3ca07852db4166f614354341b0d8494`

was created at **2026-09-19T18:35:37Z**.

The v96 manuscript commit

`423a0e135c217d6dc42fc973d8da4ee13893e865`

was created at **2026-09-19T18:55:55Z**.

Thus the v95 report was already present in the repository roughly twenty minutes before the v96 head was committed. It is on the branch

`review/a2-v95-independent-harsh-top4-2026-09-20`

and consists of a 502-line referee report specifically reviewing the exact v95 head from which v96 was derived.

This is not a mathematical counterexample, but it is not a cosmetic bookkeeping matter either. Revision 96 should have been written against the actual latest referee report. Some of its new mathematics happens to address parts of that report, but the author response does not establish that systematically and leaves several of the report's principal requests untouched.

For a serious revision chain, the next author response should source-pin the latest report by branch, path, and commit and give a point-by-point disposition against that report, not against an older one.

## 3. What revision 96 genuinely accomplishes

### 3.1 The exact fibre theorem now covers the whole named family across first-channel rank

Theorem `thm:family-classification-v96` is a genuine strengthening of the v95 family result.

For

[
f(z)=z(z-r)^2,qquad g(z)=(z-s)^3,qquad 0<s<r<D,
]

with a positive arbitrary first channel (U), a positive invertible second channel (V), strict mixture weights and at least seven clocks, the theorem introduces

[
A=(r+3s)(2r-3s)^2,qquad
B=(3D-r)s-2rD,
]

and

[
E=(1-alpha)A-4alpha_*r^3.
]

It then claims the exact spectral fibre is a singleton precisely on

[
mathfrak I
=
{det U
eq0}cup{B<0}cup{E<0}.
]

On the complement, all additional component-polynomial pairs are given explicitly by

[
(f,(1-c)f+cg),qquad
c_*le cle min{c_D,(1-alpha)/alpha_*}.
]

This is no longer merely an open rank-one region. It includes:

- all positive rank-two first channels;
- root-geometry identification at rank one;
- weight-floor identification at rank one;
- the equality cases where the extra fibre is born.

The proof is also structurally appropriate. Seven-clock interpolation fixes the monic normalizer and matrix polynomial. At rank two, the determinant recovers the aggregate spectral polynomial. At rank one, the observable second marginal forces competitors into the affine pencil, and the cubic discriminant plus the domain and weight constraints give the full feasible interval.

I found no simple counterexample to this classification.

### 3.2 The whole-model inverse is a meaningful upgrade

Lemma `lem:uniform-inverse-v96` is one of the most important new ingredients.

The lemma does not merely control alternatives chosen inside the displayed parametric family. It asserts that every nearby competitor in the entire closed binary cubic model is, after a component permutation, (O(delta))-close in component coefficients and non-root parameters.

The rank-two proof uses a two-clock generalized-eigenvector reconstruction. The rank-one proof uses quantitative inversion of the second marginal, local affine-pencil isolation near the two base components, and coefficient functionals to recover weights and channels.

That is the correct kind of theorem if one wants the subsequent leading-set statement to describe the whole observation ball rather than one hand-selected perturbation path.

### 3.3 The leading-set theorem is substantially stronger than a pointwise Puiseux statement

Theorem `thm:uniform-normal-v96` states a Hausdorff approximation

[
d_H(mathcal R_	heta(t),mathcal L_	heta)
le C_Hsqrt t
]

uniformly for (	heta) on compact subsets of the identifiable set.

The leading set is described by the double- and triple-root variables

[
X,Yge0,qquad
J_	heta(X,Y)le4,qquad
27Z^2le4Y^3.
]

The proof includes both directions:

- necessity, by extracting exact root coordinates from arbitrary nearby closed-model competitors and radially rescaling the first-order jet;
- sufficiency, by constructing actual stochastic alternatives with a radial interior correction.

The consequence

[
omega_	heta(t)=C(	heta)sqrt t+O_H(t)
]

is therefore more informative than a fixed-point little-(o) expansion.

This directly addresses a major weakness of earlier versions.

### 3.4 The active-set reduction materially answers part of the v95 stability objection

The v95 report explicitly requested a finite active-set/wall-chamber analysis for the Fisher programs.

Revision 96 supplies one.

For each of (kappa_x) and (kappa_y), there are four possible supports in the two remaining nonnegative coordinates. The KKT conditions are explicit rational sign tests. Hence, after refining by identification signs and the rank condition, one obtains a finite semialgebraic partition on which

[
C^4=
rac4{kappa_x}
quad	ext{or}quad
rac{64}{9kappa_y}.
]

The switching wall is

[
9kappa_y-16kappa_x=0.
]

This is a useful and clean theorem. The proof's minimal-positive-support argument correctly handles singular two-column active Gram matrices without pretending that a fixed support remains valid everywhere.

### 3.5 Exact arithmetic is used in the right way

The rational examples are genuinely exact evaluations of the finite programs. The rank-one example gives a very large leading constant,

[
3778.707<C<3778.708,
]

while a specified rank-two example gives

[
59.970<C<59.971.
]

The accompanying file records exact rational Gram matrices and rational fourth powers. This is much stronger than presenting an optimizer's floating-point output as evidence for the theorem.

The branch also continues to label the regression scripts honestly as finite checks rather than proof verification.

## 4. Major objection I: “stratified spectral laws” still means stratification inside one fixed singularity pattern

This is the principal top-four breadth objection.

Revision 96 has a finite semialgebraic partition, but the ambient family is still extremely rigid:

- two latent components;
- degree three;
- a fixed boundary simple root plus an interior double root in the first component;
- a fixed interior triple root in the second component;
- fixed root multiplicities;
- a positive invertible second channel;
- positive (2	imes2) channels;
- a fixed binary observation architecture;
- clocks strictly beyond the root interval;
- at least seven clocks;
- fixed stochastic weight-floor architecture.

The new partition varies:

- the rank of the first channel;
- whether the additional affine-pencil branch fits inside the root domain;
- whether the weight floor removes that branch;
- which nonnegative active set solves each of two finite Fisher programs;
- which of the double- or triple-root directions dominates the leading constant.

That is useful. But it is not yet a **singularity stratification theorem** in the broader sense requested by the v95 report.

The following are not part of the finite atlas:

- changes of root multiplicity;
- movement of the simple root away from the boundary;
- collisions between the two base clusters;
- changes in the number of latent components;
- changes of polynomial degree;
- loss of invertibility of the second channel;
- zero entries in the centre's channels;
- changes in the set of accessible real divisorial valuations in the general theorem;
- transitions between different root-cluster combinatorial types;
- changes in the observation architecture itself.

The title and abstract now use the phrase “stratified spectral laws.” For a specialist reading the definitions carefully, this is defensible because the manuscript specifies the family. For a leading general journal, however, the natural standard is higher: the stratification should organize a **class of singularities**, not only the active sets inside one already selected singularity type.

The v95 report requested, in substance, a theorem where exact fibre type, valuation candidates, exponent, leading fibre, and leading constant vary coherently across a nontrivial semialgebraic class. Revision 96 supplies the last two layers for one family but does not connect them to parameter-dependent changes of the general real-valuative data.

### What is still needed

A genuinely broader theorem should allow at least one of the following to vary:

1. the root-multiplicity pattern;
2. the boundary/interior status of roots;
3. the channel-rank pattern on both sides;
4. the accessible real valuation list arising from the observation-spectral graph.

A finite stratification controlling those changes would materially alter the significance assessment.

## 5. Major objection II: the novelty boundary with classical and current Łojasiewicz theory remains unresolved

The v95 report's first major objection was not that the real-valuative theorem was obviously wrong. It was that the manuscript had not isolated sharply enough what is new beyond established resolution/Łojasiewicz machinery.

Revision 96 does not change `article/v95/finite_newton.tex`. The general real-valuative theorem and its proof remain inherited.

The manuscript now says more clearly that ratios of divisor orders are classical and credits Bierstone--Milman, Bivià-Ausina--Encinas, semialgebraic elimination, metric regularity, and Hà's 2026 valuative work. This is an improvement in tone.

But the key request remains unanswered:

> Suppose the reader grants, for free, the strongest applicable finite-max theorem for Łojasiewicz exponents/filtrations after resolution. Which theorem of this paper is still genuinely new, and what hypotheses and outputs distinguish it from those results?

The answer is presumably not “the divisor-ratio formula.” The strongest candidate for the paper's distinctive contribution is instead the **joint real constrained weighted specialization**, together with its spectral root image and stochastic feasibility constraints.

That distinction should be formalized as a theorem comparison, not left in narrative prose.

This matters particularly because the current literature is close to the manuscript's rhetoric. Bivià-Ausina and Encinas explicitly give an effective resolution-based route to Łojasiewicz exponents. Hà's 2026 preprint develops a valuative theory whose advertised structural features include finite-max principles and parameter-family stratification/stability phenomena. The manuscript cites these works but still does not give a hypothesis-by-hypothesis and output-by-output comparison.

At a top-four venue, “our application is different” is not enough. The paper should state precisely:

- what follows formally from existing principalization/Łojasiewicz results;
- what additional theorem is required to retain the real stochastic inequalities;
- what additional theorem is required to retain **joint** coefficient relations rather than scalar coefficient envelopes;
- what additional theorem turns the initial coefficient set into the leading root-set diameter;
- what part is specific to the stochastic normalization model.

Until that separation is done, the broadest theorem risks carrying novelty weight that properly belongs to the much more model-specific weighted leading-set construction.

## 6. Major objection III: the general “effective finite algorithm” remains under-specified

The v95 referee report devoted a full major objection to the effective construction. Revision 96 does not repair that proof because the relevant file is inherited unchanged.

The claimed algorithm still compresses a long sequence of nontrivial operations:

- semialgebraic decomposition into basic closed pieces;
- introduction of square-slack algebraic lifts;
- constructive resolution of the lifted algebraic sets;
- recursive treatment of lower-dimensional singular real loci;
- simultaneous principalization of the observation and cluster functions;
- detection of real-accessible exceptional divisors;
- selection of local cluster branches;
- weighted rescaling;
- real closure at (arepsilon=0);
- projection of bounded model coordinates;
- quantifier elimination;
- algebraic encoding of complex roots over real coordinates;
- finite matching for the bottleneck metric;
- compact optimization of the resulting semialgebraic objective;
- extraction of an isolating polynomial and interval for the optimum.

Every step is plausible. The composition of all of them is exactly what the theorem claims to make effective, so the interfaces cannot be left at the level of “standard methods apply.”

Several concrete issues from the v95 report remain.

### 6.1 The definition still treats identically zero (H) explicitly but not identically zero (G)

Definition `def:real-data-v95` says that a displayed (H) may be identically zero on a box. The proof later says that components on which “a function” vanishes identically are treated separately, so the intended treatment of (Gequiv0) is inferable.

But the definition itself still does not state what the monomial datum is on a source component lying entirely over the exact observation fibre.

This should be made explicit. Positive-dimensional exact fibres are part of the advertised scope; the definition should not rely on a reader repairing the asymmetry from the proof.

### 6.2 “Real algebraic input” needs a formal representation theorem

The algorithm claims exact output for real algebraic input. The paper should define once and for all how the following are represented:

- model coefficients;
- interval endpoints;
- clocks and weights;
- datum probabilities;
- polynomial graph equations;
- inequalities;
- cluster-isolating discs;
- algebraic constants appearing in the observation map.

The current proof gestures toward minimal polynomials and isolating intervals only after several earlier operations have already been declared effective.

### 6.3 The real-locus recursive cover deserves its own proposition

The proof says that uncovered singular algebraic subsets are recursively resolved, with dimension dropping at each step, and that real feasibility of charts/divisors is decided by quantifier elimination.

That is plausible but is exactly the part distinguishing the claimed **real-accessible** valuation list from an ordinary complex resolution. It should be isolated as a proposition proving:

- finite termination;
- coverage of every sufficiently small admissible observation neighbourhood;
- retention of all active inequalities;
- existence of an admissible real transversal for every recorded divisor;
- omission of divisors with no relevant real generic point.

### 6.4 The algebraic optimum statement should be separated from the closure construction

The manuscript gives a reasonable schematic first-order closure condition and explains that a singleton semialgebraic set over the real algebraic numbers is real algebraic.

That is helpful, but the final theorem would be stronger if the exact logical formula for the leading fibre and the finite matching objective were written explicitly enough that the algebraic-number conclusion became immediate rather than asserted at the end of a paragraph.

No complexity bound is necessary. Proof-grade specification is.

## 7. Major objection IV: the uniform inverse and rank-crossing normal form are plausible but too compressed for the role they now play

I do not have a counterexample to Lemma `lem:uniform-inverse-v96`, and its proof has the right architecture.

Nevertheless, this lemma has become the load-bearing bridge from exact identification to the entire uniform leading-set theorem. At top-four standards, its most delicate part deserves more space.

The rank-one argument uses several steps in rapid succession:

1. exact-fibre compactness excludes remote spectral alternatives;
2. the observable second marginal yields a uniform lower bound on the competitor's second-channel singular value;
3. nearby component polynomials are reduced to bounded affine-pencil coordinates (c_b);
4. endpoint and discriminant inequalities isolate (c_b) near zero;
5. a depressed-cubic real-rootedness inequality isolates (c_b) near one;
6. coefficient functionals then recover the rank-one coefficient matrices, weights, and channels.

Each step is plausible, but the proof currently hides the quantitative separation constants that become essential when the compact set (H) crosses the rank-one/rank-two locus.

The final sentence invokes a finite neighbourhood cover. That is standard once the local constants have genuinely been established, but the current presentation makes the most delicate constants implicit.

I would require a standalone quantitative lemma of the following form:

> On every compact (HSubsetmathfrak I), there is a uniform positive separation between the base spectral fibre and every remote admissible affine-pencil branch, and the local inverse constants for the normalization map, marginal factorization, and two base-pencil points admit a common bound.

That statement would make the subsequent coercivity and Hausdorff arguments much easier to audit.

This is not a request for a new theorem of independent significance. It is a request that the theorem already carrying the paper be proved at publication-grade granularity.

## 8. Major objection V: the actual identification walls are still not analyzed

Revision 96 proves continuity of (C(	heta)) on the open identifiable set (mathfrak I) and uniform remainder estimates on compact subsets (HSubsetmathfrak I).

That is useful, but it deliberately stops before the most interesting singular limit.

The exact-fibre theorem identifies concrete walls:

- (det U=0);
- (B=0), where the geometric pencil first reaches the root-domain boundary;
- (E=0), where the stochastic weight floor first permits the extra pencil component.

At those walls the exact fibre can cease to be a singleton.

For a paper whose new organizing language is “stratified spectral laws,” the natural next questions are unavoidable:

- Does (kappa_x) or (kappa_y) vanish as an identification wall is approached?
- At what algebraic rate?
- What is the corresponding blow-up rate of (C(	heta))?
- Does the (t^{1/2}) modulus cross over to a nonvanishing exact-fibre diameter at the wall?
- What is the two-parameter scaling law when (tdownarrow0) while the centre approaches (B=0) or (E=0)?
- At (B=0), where the extra pencil branch is born at a root hitting (D), what is the local normal form?
- At (E=0), where the extra branch is admitted exactly at the weight floor, what is the constrained local normal form?
- Is the large rank-one constant in the rational example a precursor of a quantified blow-up near one of these walls, or merely conditioning at that selected datum?

The current compact-interior theorem cannot answer these questions.

This is not merely an optional embellishment. The v95 report specifically asked which walls force the Fisher constants toward zero and what the blow-up rate of the leading constant is. Revision 96 proves continuity away from the wall but does not supply the requested boundary asymptotics.

## 9. Major objection VI: the family partition is not yet connected to the general valuative stratification problem

There are currently two powerful but insufficiently connected parts of the manuscript:

1. a general resolution-based real-valuative construction for an arbitrary compact semialgebraic observation-spectral graph;
2. a completely explicit active-set partition for one binary cubic family.

What is missing is the theorem joining them.

The v96 family partition is obtained from elementary explicit formulas (B,E), the rank of (U), and the finite Fisher KKT signs. It does **not** show that, in a general algebraic family, the accessible divisor list, the minimizing valuation, the weighted initial fibre, and the Fisher active set vary over a finite semialgebraic stratification.

Conversely, the general real-valuative theorem does not provide a parameter-dependent finite wall decomposition.

That bridge is exactly what would justify the manuscript's broadest rhetoric.

A top-four-strength version would ideally prove something like:

> For a specified algebraic family of stochastic polynomial observation problems with bounded degree and fixed combinatorial ambient data, parameter space admits a finite semialgebraic stratification such that the exact fibre dimension/type, accessible real valuation candidates, intrinsic exponent, weighted leading coefficient fibre, and finite leading-constant program are constant in combinatorial type and semialgebraic/analytic in the parameters on each stratum.

I am not asserting that such a theorem is easy. I am saying that the present manuscript stops one conceptual level below it.

## 10. Major objection VII: the complete article is still an accretive research-program compendium

The v95 report was explicit on this point. Revision 96 has not adopted the narrowing route.

The v96 paper intentionally keeps every inherited mathematical and bibliography module active and byte-identical. After the new core, the complete article still imports a long chain of earlier modules on:

- cubic geometry and earlier leading calculations;
- additive/global normalization;
- clock complexity;
- observable recovery;
- global proof details;
- intrinsic moduli;
- germ Newton constructions;
- stochastic intersections;
- metric transport;
- local conditioning;
- coefficient recovery;
- local minimax theory;
- quotient geometry;
- flag gauges;
- residues;
- algorithms;
- statistics and polynomial statistics;
- fibres and admissibility;
- singular normal forms;
- sharp flags;
- constrained Newton laws;
- relations and literature.

Repository preservation is commendable. It is not the same thing as journal architecture.

The strongest v96 story is now relatively clean:

[
	ext{real constrained graph}
	o
	ext{exact binary-cubic fibre classification}
	o
	ext{uniform leading spectral set}
	o
	ext{finite active-set constant}.
]

If the authors do not prove a genuinely broader stratification theorem that logically needs the historical apparatus, then the top-four submission should be rebuilt around this spine and most inherited material should move to companion papers or archival appendices outside the principal article.

At this stage, adding more modules would weaken rather than strengthen the submission.

## 11. The statistical corollary remains mathematically legitimate but secondary

The new uniform oracle-risk corollary is carefully scoped.

The centre is specified, the parameter neighbourhood shrinks in the observation metric, and the upper bound can therefore use a centre-dependent constant decision. The lower bound is a two-point argument.

Nothing in revision 96 turns this into:

- unknown-centre adaptation;
- honest confidence regions across singular strata;
- an estimator that discovers the active stratum;
- a global minimax theorem over the entire closed stochastic model.

The manuscript correctly disclaims those stronger interpretations.

Accordingly, I would keep the statistical result as a corollary. It does not materially alter the general-journal significance assessment.

If statistics is to become a co-equal contribution, the appropriate next theorem is an adaptive result across at least two of the identified strata or walls. Otherwise the current oracle interpretation is the right one.

## 12. Detailed mathematical and editorial requests

### 12.1 Correct the controlling referee source

The next response must cite the v95 report

`reviews/a2-v95-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`

at commit

`c020b5ede3ca07852db4166f614354341b0d8494`.

A point-by-point response should distinguish:

- fully answered;
- partially answered;
- intentionally deferred;
- rejected with mathematical reason.

### 12.2 Give a theorem-by-theorem novelty table

For each of the following, state the closest prior theorem and the exact delta:

- finite divisor-ratio exponent;
- real-accessibility restriction;
- cluster-weight conversion from coefficient order to spectral order;
- joint weighted leading coefficient set;
- root-set diameter extraction;
- family exact-fibre classification;
- uniform Fisher normal form;
- active-set phase partition.

The current prose is not sufficiently precise for the claimed venue.

### 12.3 Broaden the stratification or narrow the title and claim

Either prove a stratification allowing a genuine change of singularity type, or make unmistakably clear in the title/abstract that the finite phase theorem concerns one fixed binary cubic boundary double/triple-root family.

### 12.4 State the (Gequiv0) case directly in the monomial-data definition

Do not leave it only in the proof's generic sentence about identically vanishing functions.

### 12.5 Formalize the effective input model

Give a single definition of “real algebraic input” and the representation of all constants, inequalities, graphs and cluster-isolating data.

### 12.6 Isolate the real-accessible resolution-cover theorem

Prove finite coverage and admissible real transversals as a standalone proposition.

### 12.7 Expand the uniform inverse proof

State and prove the uniform remote-branch separation and the local inverse constants that survive across rank changes inside compact subsets of (mathfrak I).

### 12.8 Analyze at least one identification wall asymptotically

The natural candidates are (B=0) or (E=0). A two-scale normal form showing how (C(	heta)) diverges and how the exact fibre is born would be a genuinely new structural result.

### 12.9 Connect valuation walls to Fisher walls

The present active-set walls live after the square-root exponent has already been fixed. The general theory should explain when the **valuation itself** changes and how that interacts with the Fisher phase partition.

### 12.10 Keep finite diagnostics in their proper role

The existing discipline is good. Preserve it. Symbolic identities, exact rational examples, NNLS comparisons, and Taylor-remainder checks are regression evidence only.

### 12.11 Rebuild the article around one theorem graph

If the broad stratification theorem is not proved, split the historical global material into companion articles rather than keeping every prior module active in the principal PDF.

### 12.12 Distinguish three different notions of stability

The manuscript should consistently separate:

1. persistence of the square-root root-multiplicity exponent;
2. stability of exact spectral identification;
3. conditioning of the leading constant.

A rank change can affect these differently.

## 13. Comments on the v96 exact arithmetic and diagnostics

The ancillary verification is unusually careful and should be retained.

Positive features include:

- symbolic checking of the cubic discriminant and pencil derivative;
- numerical rank checks for the free score matrix;
- comparison of the hand-enumerated active sets with NNLS;
- actual stochastic root arcs at both rank-one and rank-two centres;
- exact verification of a nonidentified affine-pencil transformation;
- explicit checking of the triple-diameter geometry;
- exact rational evaluation of two Fisher programs;
- rational isolating intervals for the fourth root.

I emphasize, however, that the very large rank-one constant is mathematically informative. It shows that compact-interior positivity of (kappa_x,kappa_y) is not the end of the conditioning story.

A future revision should use exact arithmetic not only to show that (C) can be large, but to explain **why** it becomes large and how that behavior is organized by the nearby semialgebraic walls.

## 14. Reproducibility and exact-head build status

The v96 source discipline is strong.

The branch adds an exact-head audit script that:

- pins the v95 base commit;
- requires the v96 delta to be addition-only and manifest-approved;
- verifies hashes of new sources;
- checks inherited active inputs against the v95 base;
- checks the actual TeX input graph;
- can bind the complete build log, `.fls`, and PDF to runtime HEAD.

The workflow is designed to compile the full manuscript, not merely the eight-page family reading copy.

The revision itself correctly states, however, that locally:

- the family reading copy compiled;
- finite regressions passed;
- the two exact rational examples passed;
- the complete inherited-appendix manuscript was **not** compiled in the local staging directory;
- an exact-checkout full repository audit was **not** executed locally.

I do not upgrade those claims beyond what is evidenced. The GitHub connector available to this review does not surface push-triggered workflow runs through its commit-run query, and there is no combined status record exposed for this exact head. I therefore do not record a successful remote full-build conclusion in this report.

This is an operational qualification, not the basis of my mathematical recommendation.

## 15. What revision 96 changes relative to the v95 referee report

It is important to be precise: revision 96 does answer part of the v95 report even though it did not cite that report as controlling.

### Substantially answered

- The request for active-set behavior of (kappa_x,kappa_y) is substantially answered.
- Continuity and semialgebraic/analytic phase structure of the leading constant inside the identifiable family are substantially answered.
- Rank-two perturbations of the first channel are no longer merely numerical; they are included in the theorem.
- The weight-isolated rank-one region is explicitly classified.
- Exact rational examples replace floating-point evidence for representative constants.

### Partially answered

- The request for a wall-chamber theorem is answered only inside a fixed binary cubic singularity type.
- The request to distinguish rank, boundary and multiplicity mechanisms is improved but not completed near the actual identification walls.
- Stability is proved on compact subsets of the identifiable region, not through the singular boundary where identification fails.

### Not answered

- A theorem-by-theorem novelty comparison with the strongest applicable classical/current valuative results.
- A broader singularity stratification where multiplicity or accessible valuation data change.
- Proof-grade expansion of the general effective real-resolution algorithm.
- The (Gequiv0) definitional issue.
- Boundary blow-up rates for the exact leading constant.
- Architectural narrowing of the complete article.
- A response sourced to the actual latest v95 referee report.

This is why I regard v96 as a substantial mathematical revision but not a closure of the latest referee objections.

## 16. What would materially change my top-four recommendation

I see two coherent routes.

### Route A: prove a genuine singularity-atlas theorem

This is the stronger route.

Fix a nontrivial algebraic/semialgebraic class of stochastic polynomial models broader than the single v96 family. Prove a finite stratification on which one controls, in one theorem:

- exact spectral fibre type;
- dimension and combinatorics of nonidentifiable fibres;
- accessible real valuation candidates;
- intrinsic Hölder exponent;
- weighted leading coefficient fibre;
- root-leading-set type;
- Fisher active set;
- leading constant formula;
- transitions across identification and multiplicity walls.

The current binary cubic family could then be the first explicit cell calculation of a genuinely general theory.

A theorem of that type would make the current resolution machinery, real inequalities, stochastic normalization, root geometry and Fisher calculation parts of one unavoidable structure.

### Route B: narrow the paper aggressively

If Route A is not available, I recommend abandoning the attempt to make the complete historical A2 apparatus one top-four general-journal article.

A much stronger focused paper could contain:

1. a precise real constrained weighted-specialization theorem;
2. a rigorous novelty comparison showing exactly what is beyond scalar Łojasiewicz finite-max theory;
3. the complete binary cubic exact-fibre classification;
4. the uniform whole-model spectral normal form;
5. the finite active-set formula for (C);
6. one carefully analyzed identification wall;
7. the oracle risk consequence as a short corollary.

Move the unrelated global normalization, clock, quotient, residue, algorithmic and statistical infrastructure to companion papers.

That narrower paper could be very strong. It would also make the novelty much easier to judge.

## 17. Editorial assessment

**Correctness.** I did not find a fatal counterexample to the new v96 family classification, uniform normal form, or active-set formula. Several load-bearing inverse/uniformity steps are too compressed for a final top-four proof, but the mathematical architecture is plausible.

**Originality.** The model-specific stochastic fibre classification and joint constrained leading spectral set look substantially more distinctive than the bare divisor-ratio exponent formula. The latter remains close to established and current valuation/Łojasiewicz machinery.

**Depth.** The combination of exact fibre classification, whole-model leading set, and finite Fisher phase calculation is serious mathematics.

**Breadth.** Still insufficient for the stated venue. The explicit stratification remains confined to one fixed low-dimensional singularity pattern.

**Exposition.** The new core is clearer than the inherited complete article. The full manuscript remains too accretive.

**Reproducibility.** Strong source discipline and useful exact arithmetic. Full exact-head build success is not certified by the evidence available to this review.

**Revision discipline.** Deficient in one concrete respect: v96 failed to identify and answer the already-committed v95 referee report.

## 18. Bottom line

Revision 96 is not a cosmetic patch.

It upgrades the binary cubic example into a genuine cross-rank exact-fibre classification, proves a uniform whole-model leading normal form, and gives a finite semialgebraic active-set formula for the exact leading constant. Those are meaningful advances, and I do not see a responsible basis for dismissing them as mere diagnostics or notation.

Nevertheless, the manuscript still falls short of the standard of the four leading general mathematics journals.

The finite phase partition is a chamber decomposition inside one fixed singularity type rather than a broad singularity atlas. The general real-valuative theorem remains too close to classical/current Łojasiewicz technology without a sufficiently sharp novelty theorem. The effective general algorithm remains compressed. The most interesting singular behavior at the actual identification walls is still outside the uniform theorem. The complete article remains overgrown. And the revision chain itself failed to engage the true latest referee report that was already present before v96 was committed.

Accordingly, my recommendation remains:

**reject in the present form at the Annals/Inventiones/JAMS/Acta level.**

A future submission could materially change that recommendation if it either proves the broader singularity-stratification theorem described above or substantially narrows the article while making the genuinely new constrained leading-set theorem and its wall behavior unmistakably central.

What would *not* change my recommendation is another local accumulation of diagnostics, another isolated numerical example, or another round that keeps the entire inherited apparatus while adding one more special-case lemma.
