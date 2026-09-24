# Referee Report — General Theta Foundations I, Revision 29

**Manuscript:** *General Theta Foundations I: Intrinsic Continuation Geometry and Causal Memory*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v29-referee-ready-2026-09-24`  
**Reviewed head:** `b0bd13753456c15815b174db1106e2ce6ee7433b`  
**Native mathematical source commit recorded by the manuscript:** `966cb98627d3384f756c3d7a0d9a680e4f59d2e9`  
**Controlling previous report:** `9c8161e9df1b017fa2dfb46218a4fa42f42e9bdd`  
**Previous reviewed manuscript:** `cdc749027c5f7a6f66c572ea498cd15e1b1a3391`  
**Review branch:** `review/general-theta-foundations-i-v29-intrinsic-continuation-pipeline-harsh-top4-r14-2026-09-24`

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level in the present form.**

Revision 29 is a real mathematical revision, not an infrastructural relabeling. It directly addresses the principal objection in the preceding report. The lower capacity is no longer defined from a hand-selected stock of facial witnesses. Instead, the paper forms a graph from the minimal faces of all normalized residual continuations, sums affine ranks over its connected components, and proves a cutwise lower bound against arbitrary stochastic state continuations. When each component hull is a simplex, residual vertices supply one compatible machine attaining the lower profile at every cut. The paper also adds a growing binary-query family with exact linear and exponential memory regimes, a product theorem, and adaptive-acquisition lower bounds.

I did not find a short fatal counterexample to the new theorem spine. In the complete finite clocked model actually stated, the face argument behind the lower bound is sound, the residual-shift construction gives a compatible upper realization, the product proof is coherent, and the weak- and strong-signal random-access proofs establish the displayed regimes. This is a substantial improvement over revision 28.

The negative recommendation is therefore not based on an allegation that the new main theorems are false. It is based on mathematical level and originality. In its cleanest form, the central classification says that support-separated blocks of residual rows require at least their ordinary affine ranks, and that this bound is attained when the residual hull in each block is a simplex and is closed under normalized shifts. This is elegant and useful, but it is a narrow rank-complete class whose proof is a short convex-face observation combined with the classical residual-state construction. The manuscript has not established that this is a four-journal advance over probabilistic residual automata, positive realization, and nested-polytope/nonnegative-rank theory. The closest probabilistic-residual predecessor is not even included in the theorem-level crosswalk.

The scalable example does not cure this problem. Its two exact regimes leave essentially the entire intermediate signal range unclassified, its adaptive theorem is a barrier factorization rather than a general controlled-scheduling theorem, and its product growth is obtained under a stipulated full product output law. The repository-wide “foundations” claim also remains unearned: revision 29 does not discharge, replace, or materially simplify any of the A2/A3/A4/B4/C2/D1 analytic gates. Its advertised consumers are mostly a re-expression of the already established five-state example and products of a prescribed terminal channel.

I would view a sharply rewritten paper centered on the finite residual theorem and the streaming example as potentially publishable in a strong specialist venue, subject to a serious priority analysis and stronger results in the intermediate regime. I do not regard the present 69-page consolidation as top-four mathematics.

---

## 1. Scope of this review

I reviewed the revision-29 theorem spine and the records needed to place it in the repository pipeline:

- `intrinsic-continuation.tex`;
- `tensor-continuation.tex`;
- `streaming-access.tex`;
- `contact-application.tex`;
- `literature-theorems.tex`;
- the new introduction and theorem hierarchy in `main.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `HISTORY_AUDIT.md`;
- `RESOURCE_LEDGER.md`;
- `LITERATURE_CROSSWALK.md`;
- the revision-29 exact-check record and build receipt;
- the controlling revision-28 report;
- the retained positive-noise/contact/facial-scheduling/exact-memory arguments to which the new applications refer;
- the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I compared the referee-ready revision 29 against the referee-ready revision 28. The new branch is four commits ahead and adds the intrinsic-continuation package while preserving the previous report and the substantive revision-28 mathematical body.

This is a mathematical referee audit, not a claim to have mechanically re-proved every page of the 842-page preserved development. Build receipts, source hashes, finite regressions, and theorem-location records are useful provenance. They are not independent certification of the mathematical claims or of priority.

My scrutiny concentrated on the places where revision 29 could materially change the previous recommendation:

1. whether the support-component rank is truly intrinsic rather than certificate-dependent;
2. whether its lower bound covers arbitrary stochastic implementations, not only residual-state machines;
3. whether the residual-vertex upper construction is simultaneously causal at all cuts;
4. whether product closure survives correlated internal implementations;
5. whether the binary-query construction gives an actual online machine rather than a terminal factorization;
6. whether adaptive acquisition is genuinely covered;
7. whether these results alter the repository proof DAG;
8. whether the literature comparison establishes a top-journal originality boundary.

---

## 2. What revision 29 genuinely fixes

### 2.1 The selected-witness defect of revision 28 is fixed on a stated finite class

The preceding report objected that the revision-28 field \(c(v)\) was an invariant of the experiment plus an analyst-selected collection of discovered certificates. Revision 29 no longer has that defect.

At a charged cut, the paper takes every normalized continuation \(R_h\) arising from a positive controller prefix, places it in the full causal polytope, joins two residuals when their minimal faces intersect, and defines
\[
s_t(C)=\sum_j\bigl(\dim\operatorname{aff}\mathscr R_{t,j}+1\bigr).
\]
No trial controller and no witness list enter this definition. For an explicit complete finite array, the residuals, zero patterns, face intersections, affine dimensions, and component hulls are finite data.

The lower proof also addresses the main loophole that would have made a residual-only theorem inadequate. A competing state continuation \(B_{t,s}\) is not assumed to be a residual or to lie in the residual hull. If it is used with positive weight in a convex decomposition of \(R_h\), the face property forces it into the minimal face of \(R_h\). A single physical state therefore cannot serve residuals in different support components. Ordinary affine rank then gives the number of states required inside each component.

That is an all-stochastic lower bound in the stated model. It is materially stronger than saying that the canonical residual machine is minimal among residual machines.

I therefore withdraw the central revision-28 criticism that the general lower field is merely the strength of the witnesses supplied by the author.

### 2.2 The upper bounds are made simultaneously causal

A separate factorization at every cut would not establish an implementable finite-memory process. Revision 29 correctly checks the shift condition.

Every chosen state in the upper construction is an actual residual vertex. Its next-action probability is independent of the unread report. After action \(a\) and report \(y\), the normalized shift \(R^{a,y}\) is another actual residual at the next cut. Decomposing that residual into the next cut's chosen vertices supplies a legal stochastic update row. Backward induction then proves that the same machine realizes the entire future array from every selected state.

Thus the upper profiles are not obtained by splicing unrelated nonnegative factorizations. In the componentwise-simplicial case, the lower affine rank equals the number of residual vertices component by component, so one machine attains all cutwise minima simultaneously.

This directly answers an important part of the previous report.

### 2.3 The paper now contains a scalable family

The binary-query experiment is not another five-, ten-, or twelve-state finite table. The input length \(n\) grows, the final output remains binary, and the paper proves two exact memory laws:
\[
W_n(\eta)=n+1\quad (0<\eta\le n^{-2}),
\qquad
W_n(\eta)=2^n\quad (1-n^{-1}<\eta\le1).
\]

The weak-signal result includes an explicit online sequence of simplices, not merely a final enclosing simplex. At time \(t\), the controller stores one of \(t+1\) vertex labels. The inclusion
\[
P_t\times\{-\eta,\eta\}\subset P_{t+1}
\]
makes the barycentric update causal. The proof therefore establishes the full profile \(t+1\), not just the final checkpoint rank.

The strong-signal converse is also clean. The corner-error functions force a generator used for one input corner to be unavailable to every other corner. This gives \(2^n\) states even though ordinary predictive rank is only \(n+1\).

These are genuine scalable statements.

### 2.4 Adaptive acquisition is addressed in the new examples

For the random-access experiment, every adaptive choice of the next unread coordinate and every past random choice must pass through the state at the acquisition barrier. Conditioning on the complete input therefore yields one encoder and a common query decoder. The checkpoint lower bounds survive any adaptive acquisition order, while a fixed order attains them.

The product-channel barrier corollary uses the same logic: the law of the entire labelled output vector factors through the retained state, regardless of the order in which outputs are later released.

These quantifiers are stronger than fixed-path scheduling.

The manuscript is also careful not to import them into the original collision-validation problem. It does not claim that every report-dependent physical validation scheduler needs twelve states. That restraint is correct.

### 2.5 The known-target/acquired-target distinction remains explicit

The exact five- and twelve-state physical results still require a specified target and exact atomic stochastic rows. Acquired calibration remains an approximate-score theorem with counters and finite precision. Revision 29 does not conflate these notions.

This semantic precision should be preserved.

---

## 3. Technical audit of the intrinsic continuation theorem

### 3.1 The lower-bound argument is correct in the stated complete clocked model

Let
\[
R_h=\sum_s E_h(s)B_{t,s}.
\]
Because \(F_t(R_h)\) is a face containing \(R_h\), every \(B_{t,s}\) with positive coefficient lies in \(F_t(R_h)\). If the same state continuation were used for residuals \(R\) and \(R'\), it would lie in both minimal faces, hence those faces would intersect. Residuals in different connected components therefore use disjoint state sets.

Within a component, all residuals lie in the affine span of the union of its used normalized state continuations. If the component has affine dimension \(d\), at least \(d+1\) normalized states are required. Summation over components gives \(K_t\ge s_t(C)\).

This proof does not assume deterministic encoders and does not force the state continuations into the residual affine hull. Those are important points.

The statement depends, however, on all persistent distinctions being in the state and on the future program from a fixed state at cut \(t\) being well defined. The paper states those conventions. Additional autonomous shared-row equalities are expressly outside the clocked theorem.

### 3.2 The simultaneous upper construction is valid

The extreme points of the convex hull of a finite residual component are themselves residuals. Each residual can be decomposed into the selected vertices. For a selected residual \(R\), its action probabilities and normalized shifts specify the next stochastic row. Each shift is decomposed at the child cut. This realizes the same response array recursively.

I do not see a hidden dependence on the unread report in the action row. Nor do I see a splicing error between cutwise factorizations.

The theorem is therefore a legitimate exact-profile result on its componentwise-simplicial class.

### 3.3 The completeness condition is sufficient, not close to a characterization

The square example correctly shows that the affine-rank lower bound may be strict outside the simplicial class. It does not show that componentwise simpliciality is remotely necessary for rank completeness.

Many nonsimplicial residual configurations can still have unrestricted nonnegative rank equal to ordinary rank, and many may admit compatible minimal updates for reasons not captured by simplex geometry. Conversely, deciding unrestricted positive realization can remain difficult even when support is simple.

Revision 29 gives one readily checkable sufficient class. It does not characterize the exact-memory arrays, the rank-complete arrays, or the causally compatible rank-complete arrays.

This distinction is central to the venue assessment. The term “complete class” in the manuscript means that the theorem is exact on the class, not that the class is maximal or structurally definitive.

### 3.4 The decidability corollary is modest

For an explicitly listed finite rational array, enumerating residuals, testing zero-pattern face intersections, computing ranks, finding extreme points, and solving barycentric systems is finite. That is correct.

The result is not an efficient algorithm in the horizon, in a succinct controller description, or in the number of reports. The input table can already be exponentially large. The paper says so.

Accordingly, this corollary should not be presented as resolving the computational problem of causal-memory minimization. It is a finite recognition and synthesis procedure for a narrow explicit class.

### 3.5 The declared-schedule corollary is correct but does not solve controlled scheduling

At a fixed schedule vertex, all prefix rows are included and the intrinsic capacity no longer depends on a chosen certificate. If every vertex passes the simplex test, bottleneck dynamic programming over declared paths gives the exact fixed-clock optimum.

This is a clean replacement for the revision-28 certificate field.

It remains a theorem about a finite graph of externally declared paths. An observation-dependent scheduler changes the response array itself. The theorem can test a specified adaptive array, but it does not optimize over all adaptive policies.

That is a substantial remaining boundary, not a minor technicality.

---

## 4. Technical audit of products and the scalable example

### 4.1 Product multiplicativity is coherent under the stipulated specification

For terminal channels, minimal faces are coordinatewise support faces. Product-face intersections occur exactly when the projected faces intersect in both factors. With loops, the product component graph has components equal to products of factor components.

If the factors have \(k\) and \(\ell\) linearly independent normalized simplex vertices, their \(k\ell\) tensor products are linearly independent. The product component hull is therefore a simplex with \(k\ell\) vertices. The all-stochastic lower bound then rules out savings from correlated internal generators.

This proof is sound.

Its scope is also very strong: the complete joint product output law is specified. Independent inputs, additive payoffs, or marginal correctness do not imply this law. Once the product law is imposed, multiplicativity is close to formal linear algebra. It should not be advertised as a broad tensor theorem for causal-memory minimization.

### 4.2 The weak-signal streaming construction works

The simplex
\[
P_t=\{z:z_i\ge-t\eta,\ \sum_i z_i\le t\eta\}
\]
has \(t+1\) vertices. For \(t\le n\) and \(\eta\le n^{-2}\), every coordinate of every vertex lies in \([-1,1]\). Appending \(\pm\eta\) preserves the defining inequalities for \(P_{t+1}\). The displayed barycentric coordinates are nonnegative and sum to one.

The resulting transition depends only on the old vertex label and the newly read bit. The register stores a finite label, not a real vector. Induction gives mean vector \(\eta(x_1,\ldots,x_t)\), and the final binary decoder realizes the required conditional law.

The affine-dimension lower bound gives \(t+1\) states for the fixed order, and the query barrier gives \(n+1\) against adaptive acquisition.

I find this part correct and well presented.

### 4.3 The strong-signal corner argument works

For input corner \(x\), the encoder average of
\[
d_x(z)=\frac12\sum_i(1-x_i z_i)
\]
is \(n(1-\eta)/2<1/2\). Hence some used generator lies in the strict cap \(d_x(z)<1/2\). Caps for distinct corners are disjoint because their error sums are at least one. Thus every corner requires a distinct generator.

Full retention attains \(2^n\). The conclusion is independent of acquisition order.

This is a valid exact exponential separation.

### 4.4 The approximation proposition is correctly separated from exact synthesis

The one-state fair-output approximation has row total-variation error \(\eta/2\). The singular-value calculation gives a nonzero rank margin for any factorization through at most \(n\) states.

The paper correctly does not claim that these approximation bounds match.

---

## 5. Why revision 29 is still below the four-journal level

### 5.1 The central theorem is a narrow rank-equality criterion with a very short proof

The new invariant is intrinsic, but the mathematical content should be described without rhetorical inflation.

At each cut:

1. zero patterns separate residuals into blocks that cannot share a positive generator;
2. ordinary affine rank lower-bounds the number of normalized generators in each block;
3. if the residual hull of a block is a simplex, its residual vertices provide a factorization attaining that rank;
4. residual closure supplies the time-consistent updates.

This is a useful theorem. It is also a direct combination of elementary face geometry, rank, and the canonical residual construction.

A short proof can of course be a virtue. But a four-journal paper with such a short central mechanism must establish either extraordinary reach, a definitive classification, a deep unexpected application, or a clearly new conceptual equivalence. Revision 29 does not do so.

The simplex hypothesis is strong and visibly sufficient. The paper gives no converse, no maximality theorem, no substantially larger exact class, no obstruction theory for compatibility, and no complexity theorem for the unrestricted problem. The square counterexample merely shows that rank can fail; it does not identify the boundary.

The result is better described as an exact tractable subclass than as a general theory of causal memory.

### 5.2 The closest probabilistic-residual predecessor is omitted

The theorem-level literature section discusses Denis and Esposito’s later work on rational stochastic languages. It does not discuss the earlier and more directly relevant paper:

> Y. Esposito, A. Lemay, F. Denis, and P. Dupont,  
> “Learning Probabilistic Residual Finite State Automata,”  
> ICGI 2002, LNCS 2484, pp. 77–91,  
> DOI `10.1007/3-540-45790-9_7`.

That paper explicitly advertises an intrinsic characterization by finite generation of residual stochastic languages and canonical minimal forms. Whether its minimality notion is identical to the present unrestricted all-stochastic realization problem is precisely the question that revision 29 must answer at proof level.

It is not enough to compare only with a later residual-generation proposition and then say that residual minimality “need not” imply all-machine minimality. The manuscript must state the exact model and minimality theorem of the 2002 PRFA work, map its residuals and convex generators to the present causal arrays, and isolate a concrete theorem or example lying outside that framework.

The present all-machine lower step may indeed be new in this precise support-component form. But it is a one-paragraph face argument. A top-journal originality claim cannot rest on the referee inferring that no classical positive-realization or residual-automaton formulation already contains it.

The literature audit also remains expressly incomplete with respect to Heller and Norberg. That candor is preferable to overclaiming, but it leaves the principal originality burden unresolved.

### 5.3 The nonnegative-rank boundary is not developed deeply enough

For a full-support terminal channel there is one support component. The lower invariant is then simply the ordinary row rank, while exact realization at a checkpoint is a nonnegative-rank/nested-polytope problem. The simplex condition gives an obvious case in which nonnegative rank equals rank.

For multiple support components, the theorem sums the same observation over blocks that cannot share generators.

This relationship should be made mathematically explicit, not merely mentioned in a literature paragraph. The reader needs to know:

- whether the support-component decomposition is a known block decomposition of nonnegative rank;
- what new class of matrices or channels is proved rank-complete;
- whether the simplex condition is equivalent to a known separability, simplicial-cone, or restricted-rank condition;
- how causal shift compatibility changes the static problem;
- whether recognizing a larger compatible rank-complete class is tractable or hard;
- whether there are examples where every cut is statically rank-complete but no simultaneous rank profile is causally realizable.

Without such results, the theorem sits very close to a repackaging of familiar positive-factorization geometry.

### 5.4 The random-access theorem leaves the central geometric regime open

The paper proves exact formulas only when
\[
\eta\le n^{-2}
\quad\text{or}\quad
\eta>1-n^{-1}.
\]
For large \(n\), nearly the entire interval \((0,1)\) remains unclassified.

The weak threshold is the range in which one particular nested simplex stays inside the outer cube. The strong threshold is the range in which one particular disjoint-cap argument becomes strict. Neither threshold is shown sharp, asymptotically optimal, or close to the transition.

The manuscript does not determine:

- the exact checkpoint number \(K_n(\eta)\) in the intermediate range;
- the exact streaming peak \(W_n(\eta)\) there;
- whether \(K_n(\eta)\) and \(W_n(\eta)\) can differ;
- the largest \(\eta\) for which an \(n+1\)-vertex enclosing simplex exists;
- the largest \(\eta\) for which a compatible chain of such simplices exists;
- polynomial, quasipolynomial, or exponential lower regimes between the endpoints;
- any asymptotic phase diagram.

This is not a small omitted case. It is the main convex-geometric problem suggested by the example.

The theorem therefore demonstrates two separated phenomena rather than classifying the family.

### 5.5 The adaptive result is a barrier theorem, not a theory of controlled memory

Adaptive acquisition cannot help once the entire input must pass through a single state before an external query. The lower bound is then an encoder-decoder factorization. This is correct, but structurally simple.

The difficult adaptive problem raised by the previous report was different: the controller chooses the next experimental action based on partial observations, and that choice interacts with future information and memory throughout the run. There need not be one terminal barrier at which the whole transcript is compressed before all remaining interaction.

Revision 29 can classify a specified adaptive response array if it passes the simplex test. It does not optimize jointly over adaptive response arrays, actions, and state complexity. The original collision-validation adaptive optimum remains explicitly open.

Thus the paper has not yet produced a general controlled-scheduling theorem.

### 5.6 Product multiplicativity is too formal to carry the significance claim

The product theorem requires every conditional probability of the joint independent output channel. Under that specification, the product residual set is the Cartesian product of the factor residual sets, and tensor independence gives the state count.

This is useful closure, but it does not prove multiplicativity for:

- minimax values;
- optimal responses selected separately in each block;
- arbitrary nonnegative rank;
- approximate realization;
- shared observations;
- correlated targets;
- adaptive inter-block experimentation;
- product experiments with only marginal performance constraints.

The \(5^m\) application consequently says that a stipulated product of the five-state continuation channel has capacity \(5^m\). It is not a theorem about an \(m\)-block physical audit, an \(m\)-block saddle, or a repository consumer.

The paper is honest about this. The venue assessment must be equally honest about its limited depth.

### 5.7 The “downstream consumer” is mostly a reinterpretation of prior work

The five-state physical result was already proved in revision 28. Revision 29 observes that its five forced rows have support components of dimensions \(1,0,1\), so the new invariant recovers \(2+1+2=5\).

That is a useful conceptual compression. It is not a new downstream theorem.

The product \(5^m\) statement assumes the exact product continuation law. The weak-signal streaming construction is developed in the same new package to illustrate the theorem. Neither is an independent repository theorem that previously lacked a proof and is now unlocked.

The Round-Seventeen ledger remains unchanged:

- A2 still requires branch-bundle, lattice-rank, returned-UNI, physical integration-by-parts, unsmoothed-tail, and raw-density-LLT work;
- A3 still requires the exact entropy and stopped-LDP chain;
- A4 still requires the global kernel, Harris/drift, renewal, and Mori–Zwanzig chain;
- B3 still requires closed range, process CLT, normalization, and Mosco recovery;
- B4 still requires law-hierarchy realizability, Nisio resolvent, \(m\)-dissipativity, graph core, and nonlinear Trotter–Kato;
- C2 still requires strict duality, form/operator compression, rigidity, and changing-filtration projection;
- D1 still requires the labelled LDP and posterior-semigroup chain.

The revision-29 pipeline status explicitly records that A2 is not replaced, B4 and C2 are not closed, and the eleven-paper aggregate is not closed.

This honesty is commendable. It also confirms that *General Theta Foundations I* remains a local finite-array branch of the program rather than a mathematical root from which the major analytic papers flow.

### 5.8 The paper remains overpacked and insufficiently distilled

The canonical article is 69 pages. The genuinely new revision-29 theorem spine occupies roughly the first fifteen pages. The remainder retains the full revision-28 body as supporting appendices, including several logically distinct programs:

- controlled minimax;
- exact finite saddles;
- Brownian target identification;
- fixed-clock validation order;
- autonomous testing;
- revelation laws;
- all-preparation localization;
- quantitative certification;
- acquisition and transport consumers.

Preservation is valuable for repository provenance. It is not a persuasive editorial reason to keep all material in one top-journal article.

The new theorem would be easier to evaluate in a focused paper containing:

1. the finite residual classification;
2. a sharp comparison with probabilistic residual automata and nonnegative rank;
3. the streaming family;
4. one genuinely new statistical application.

The current document still reads as an accumulated project volume. Its length obscures rather than amplifies the conceptual contribution.

---

## 6. A more exact statement of the mathematical contribution

The paper would benefit from stating its core contribution in the following restrained form.

For a complete finite clocked causal array, partition normalized residuals by the transitive closure of intersections of their minimal support faces. Every normalized positive realization needs disjoint generator sets for distinct components and at least the affine rank in each component. Residual vertices give a compatible causal realization. Therefore, when every component residual hull is a simplex, unrestricted stochastic state complexity equals the sum of the component ranks at all cuts simultaneously.

This is a clean theorem.

What the paper has **not** shown is equally important:

- the invariant is not exact for all arrays;
- the simplex condition is not shown necessary;
- the exact arrays are not characterized;
- unrestricted minimization is not solved;
- succinct computational complexity is not determined;
- autonomous shared-row minimization is not included;
- partial almost-sure specifications are not canonically handled;
- adaptive policy optimization is not solved;
- approximate state complexity is not classified;
- the intermediate binary-query regime is open;
- repository-wide analytic proof gates are unaffected.

The manuscript states many of these caveats individually. The title, abstract, and venue ambition still outrun their collective implication.

---

## 7. Specific requests that would materially change the assessment

A further revision should not add another preservation manifest, another finite regression, or another prescribed product channel. It needs a stronger mathematical theorem.

### 7.1 Establish the priority boundary rigorously

The authors should add a theorem-by-theorem comparison with at least:

- Esposito–Lemay–Denis–Dupont (2002), probabilistic residual finite-state automata;
- Denis–Esposito, rational stochastic languages and residual representations;
- Heller/Vidyasagar positive realization;
- restricted and unrestricted nonnegative rank / nested polytopes;
- compatible coverings for incompletely specified sequential machines;
- filtered-experiment comparison in the precise model actually used.

For each source, state:

1. the object being minimized;
2. whether state languages/continuations must be residuals;
3. whether arbitrary positive generators are allowed;
4. the exact minimality conclusion;
5. whether time-consistent transitions are part of the theorem;
6. whether support zeros or incomplete specifications are allowed;
7. a concrete example or theorem in revision 29 not covered by that source.

Without this, the main originality claim remains unverified.

### 7.2 Go beyond the simplex sufficient condition

A top-level advance would characterize a substantially larger exact class or identify the correct invariant.

Possible directions include:

- necessary and sufficient conditions for equality between support-component rank and unrestricted state complexity;
- a causal analogue of nonnegative rank with a theorem relating cutwise and simultaneous complexity;
- a characterization of when statically minimal factorizations can be chosen shift-compatible;
- an obstruction theory for causal compatibility;
- complexity or hardness results for exact membership and minimization;
- a canonical decomposition that is not restricted to simplices.

Another isolated sufficient polytope shape would not be enough.

### 7.3 Solve or sharply bound the intermediate random-access regime

The current example naturally asks for a phase diagram. At minimum, the paper should produce asymptotically meaningful upper and lower bounds across the intermediate range and separate:

- terminal checkpoint complexity;
- online fixed-order complexity;
- adaptive-acquisition complexity.

The threshold for an \(n+1\)-vertex terminal enclosure should be compared with the threshold for a compatible nested sequence. If these differ, that difference would itself be a strong causal-memory phenomenon.

An exact or asymptotically sharp transition would materially raise the paper’s level.

### 7.4 Prove a genuine controlled/adaptive theorem

A significant extension would optimize over observation-dependent actions while charging the policy state throughout the experiment, without reducing the problem to one final acquisition barrier.

For the physical validation model, either prove that feedback cannot beat twelve states or construct and classify a better feedback schedule. More generally, identify conditions under which adaptive actions preserve the intrinsic field or require a new controlled invariant.

That would address the natural problem rather than a simpler neighbouring interface.

### 7.5 Produce an independent mathematical consumer

A true repository consumer would use the intrinsic theorem to eliminate a proof obstruction in another paper, not merely restate an already known five-state count.

The consumer need not close all of A2/B4/C2. But it should be a theorem whose proof genuinely depends on the new invariant and would otherwise require a separate nontrivial argument.

Absent such a result, the paper should moderate the “foundations” framing.

### 7.6 Rewrite as a focused article

The archival complete manuscript and preserved development can remain in the repository. The journal article should be reorganized around one theorem spine and a small number of applications.

A focused version would likely be shorter, clearer, and easier to compare with the correct literature.

---

## 8. Points that do not presently constitute correctness objections

For clarity, I am **not** asserting any of the following:

- that the face-separation lower bound is false;
- that a competing generator must lie in the residual hull;
- that the residual-vertex updates are incompatible across cuts;
- that the weak-signal controller stores an uncharged real vector;
- that adaptive acquisition evades the barrier lower bound;
- that the corner-cap proof fails in its stated strict range;
- that correlated internal states can reduce the prescribed product-channel capacity;
- that the physical target identification reintroduces the former \(\mathbb E e^2\) error;
- that acquired calibration is claimed exact;
- that revision 29 claims to solve adaptive collision scheduling;
- that the repository ledger is being falsely declared closed.

The authors have been careful on these points.

The rejection is based on scope, depth, originality, sharpness, and foundational reach.

---

## 9. Editorial and presentation comments

1. The abstract should call componentwise simpliciality a sufficient exactness condition, not allow “classification” to suggest a characterization of all finite arrays.

2. “Complete class” is potentially misleading. Consider “a decidable exact class” or “the componentwise-simplicial class.”

3. The closest 2002 PRFA paper must be cited and discussed in the main article.

4. The paper should explicitly rewrite the terminal full-support case as a nonnegative-rank problem. Readers should not have to reconstruct this relation from scattered remarks.

5. The distinction between ordinary rank, restricted nonnegative rank, unrestricted nonnegative rank, residual-state size, and unrestricted stochastic-state size deserves one formal comparison proposition or table.

6. The weak and strong thresholds should be described as proved regimes, not as evidence of a near-complete law.

7. The phrase “adaptive” should always be qualified: adaptive acquisition with a terminal barrier is not arbitrary controlled scheduling.

8. The \(5^m\) statement should not be placed near language suggesting an \(m\)-block minimax theorem.

9. The repository dependency discussion is responsible, but it belongs in a brief scope paragraph rather than as rhetorical support for publication.

10. The 842-page preserved development and source-bound evidence should be treated as archival material, not as part of the journal contribution.

11. The main article would benefit from a single notation table. It currently moves among residual rows, response arrays, state continuations, query channels, and physical response functions with considerable cognitive overhead.

12. The square counterexample should be stated as a formal proposition with a complete lower-bound proof if it is to carry the burden of showing nonuniversality.

13. The real-algebraic decidability sentence should cite the exact decision procedure being invoked and state its input representation.

14. The conclusion should separate “proved exact class,” “open unrestricted problem,” and “open intermediate-signal problem” in three explicit paragraphs.

---

## 10. Final assessment

Revision 29 succeeds at the task set by the previous report more substantially than any cosmetic revision would have.

It replaces an analyst-chosen facial certificate with an intrinsic finite residual object. It proves a lower bound against arbitrary stochastic continuations. It checks simultaneous causal realizability. It gives product closure. It adds a growing full-support example with exact linear and exponential regimes, including adaptive-acquisition converses. I found no short fatal defect in those arguments.

That progress should be acknowledged plainly.

Nevertheless, the new central theorem is an exact sufficient criterion for a narrow simplicial residual class, obtained from an elementary support-face/rank argument and a classical residual construction. The manuscript has not demonstrated a sufficiently strong originality boundary from probabilistic residual automata and positive realization. The closest 2002 predecessor is omitted. The random-access family is classified only in two far-separated endpoint regimes. The adaptive result relies on a compression barrier. Product multiplicativity assumes the full product law. The claimed downstream consumers do not change the repository proof DAG. The paper remains an overpacked consolidation rather than a distilled foundational theorem.

Those limitations are decisive at the Annals / Inventiones / JAMS / Acta level.

**Recommendation: Reject at the four-journal level in the present form.**

A focused specialist paper could be viable after:

- a rigorous priority comparison;
- a more restrained statement of the intrinsic theorem;
- substantial progress on the intermediate random-access regime or on controlled scheduling;
- removal of the large inherited appendix from the journal narrative.

---

## Referee checklist

- Repository confirmed: `TrillionniumFoundation/theta-theory`.
- Latest referee-ready General Theta Foundations I revision identified as revision 29.
- Reviewed branch pinned at `revision/general-theta-foundations-i-v29-referee-ready-2026-09-24`.
- Reviewed head pinned at `b0bd13753456c15815b174db1106e2ce6ee7433b`.
- Native mathematical source recorded as `966cb98627d3384f756c3d7a0d9a680e4f59d2e9`.
- Controlling prior report pinned at `9c8161e9df1b017fa2dfb46218a4fa42f42e9bdd`.
- Compared revision 29 against the revision-28 referee-ready branch.
- Confirmed revision 29 is four commits ahead of revision 28.
- Read the full response to the thirteenth pipeline-aware report.
- Audited the support-component definition and lower-bound proof.
- Audited the residual-vertex simultaneous upper construction.
- Audited the finite recognition/synthesis corollary.
- Audited the declared-schedule corollary.
- Audited product component geometry and tensor independence.
- Audited the adaptive product-barrier corollary.
- Audited the weak-signal nested-simplex construction.
- Audited the strong-signal disjoint-cap converse.
- Audited the rank-based approximation margin.
- Audited the contact-rigid application and five-state decomposition.
- Re-read the retained physical known-target/acquisition distinction.
- Re-read the Round-Seventeen proof-dependency ledger.
- Confirmed A2, B4, C2, and the eleven-paper aggregate are not claimed closed.
- Confirmed the original adaptive collision-validation optimum is not claimed.
- Confirmed the intermediate random-access regime is not claimed solved.
- Confirmed exact arbitrary stochastic rows remain an atomic-row convention.
- No short fatal counterexample found to `thm:intrinsic29`.
- No short fatal counterexample found to `thm:tensor29`.
- No short fatal counterexample found to the two displayed regimes of `thm:access29`.
- The negative recommendation is based on theorem depth, sharpness, originality boundary, general controlled scope, editorial concentration, and repository-wide foundational reach.
