# Independent Harsh Referee Report — General Theta Foundations I, ninth causal-minimax revision

**Manuscript:** General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed frozen revision:** revision/general-theta-foundations-i-v9-causal-minimax-referee-ready-2026-09-23  
**Reviewed branch HEAD:** 71d5fa4c5d8b6d6f0f3d5c61aba07cedd342373a  
**Source-bound mathematical commit recorded by the build receipt:** 6bcd0de01f7d164a8feab28f82d44f6149ba385f  
**Canonical article:** papers/GTF-I-v9-causal-minimax/paper.pdf, 47 pages  
**Complete preserved development:** papers/GTF-I-v9-causal-minimax/complete-development.pdf, 140 pages  
**Controlling predecessor report:** 1e2ad3c7c5687e9cc9c0e7e0b37e983795f9f4c5  
**Controlling predecessor manuscript:** 83a887b9212c54e5e09f88821296ccce3d051504  
**Review date:** 23 September 2026  
**Standard:** external referee standard appropriate to Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  

## Recommendation

**Reject / return in the present form for a top-four general mathematics journal.**

This is, however, the strongest General Theta Foundations I revision I have inspected. Revision 9 genuinely answers the central Route C request in the preceding report: it proves a finite controlled common-encoder minimax theorem with the common encoder inside the feasible set, keeps one task controller across that task's unknown-parameter rows, distinguishes shared from private randomization, gives an exact finite support-function/occupancy formulation, and exhibits a genuine delayed-query Gaussian temporal penalty.

I do not find a decisive counterexample to the new finite minimax/risk-body theorem, its controlled-partition characterization, the shared/private seed separation example, or the delayed-query Gaussian exponent in the scope inspected. My negative recommendation is therefore not a claim that the revision is mathematically empty or obviously false.

The reasons for rejection have changed. The principal remaining issues are now:

1. the central variational theorem is exact but finite and, at proof level, built from finite deterministic-design enumeration, classical convex minimax/separation, and a designer occupancy recursion whose closest conceptual ingredients are already acknowledged as classical;
2. the new saturation theorem overstates its type if “instrument” is read as the hidden-state marked instrument used by the main decision theorem: it reconstructs the report experiment and parameter likelihoods, not arbitrary latent-state decision marks;
3. the saturation minimality is minimality inside a deliberately specified posterior-plus-raw-prediction coordinate class, not a minimality theorem for all exact causal simulators or all decision-complete quotients;
4. the finite compiler gives honest effectivity, but it is brute-force finite synthesis and can be exponential in the expanded tree; it does not yet produce an intrinsic computational complexity theory;
5. the new variational principle unifies an important finite family of decision problems, but it still does not derive the retained Wasserstein, infinite predictive-tree, nonlinear-filtering, count, and microscopic-model regimes from one common invariant;
6. the literature audit does not yet establish a top-four priority position for the exact new combination, especially against the broader filtered-experiment / real-time coding / finite-memory control literature;
7. at repository level, the pipeline remains **2 verified protocol adapters and 9 conditional interfaces**; the current A2 primary chain is explicitly recorded as independent and not consumed by GTF;
8. the title and programmatic role remain substantially broader than the theorem that is currently both exact and structurally new.

The revision is a serious mathematical response. It is not yet a top-four foundation for the eleven-paper program.

---

# 1. Status and review scope

This is an owner-requested, AI-assisted external-referee-style assessment. It was not commissioned by Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, Acta Mathematica, or another journal, and it should not be represented as a journal-issued report or editorial decision.

I froze the submission at branch HEAD

71d5fa4c5d8b6d6f0f3d5c61aba07cedd342373a.

I distinguished that publication/evidence HEAD from the source-bound commit named by the build receipt,

6bcd0de01f7d164a8feab28f82d44f6149ba385f.

The v9 line starts from the actual v8 decision-spectrum referee report 1e2ad3c7..., not from the older nominal-v8 review. The mathematical v9 commits then add the common-encoder minimax theorem, occupancy/saturation/delayed-Gaussian theory, the private-randomization converse, and finally the source-bound publication products and evidence.

I inspected, in particular:

- frontmatter.tex and introduction.tex;
- controlled-minimax.tex;
- variational-principle.tex;
- effective-saturation.tex;
- finite-compilation.tex;
- delayed-gaussian.tex;
- the v9 proof ledger;
- the point-by-point response to the v8 referee;
- the literature comparison;
- the history audit;
- the source manifest;
- the diagnostics and pipeline contract check;
- PIPELINE_DEPENDENCIES.json;
- the controlling v8 report; and
- the branch-level status of the current A1/A2 and broader eleven-component pipeline.

I did not independently re-prove every retained theorem in the 140-page preserved development. Preserved source, a successful build, exact hashes, and finite diagnostic checks are valuable audit evidence but are not proof certificates. The v9 documentation itself correctly says this.

---

# 2. What revision 9 genuinely fixes

A harsh review must not recycle objections that the author has actually solved.

## 2.1 Route C is genuinely implemented

The preceding report asked for a controlled common-encoder converse rather than another collection of separate rates.

Revision 9 provides one.

For the finite controlled instrument, a deterministic design contains one update family common to all tasks and parameters, while each task may have its own controller and decoder, but those rules are common across that task's unknown-parameter rows. The risk vectors are therefore generated by executable coupled designs, not by separately optimizing each row.

The theorem identifies the shared-seed upper risk body as

\[
\operatorname{co}\{R(\omega):\omega\in\Omega_{\bf S}\}
+\mathbb R_+^J
\]

and derives the minimax dual

\[
\Theta_{\rm sh}
=
\max_{w\in\Delta_J}
\{h_E({\bf S};w)-w\cdot b\}.
\]

This is the correct kind of quantifier architecture to address the v8 criticism.

## 2.2 The private/shared randomization issue is no longer hidden

The manuscript explicitly separates:

- an independent shared seed available to encoder and controller throughout execution; and
- fresh private randomization with no free retained common variable.

The two-label / three-symbol example gives exact worst-parameter errors

\[
\Theta_{\rm sh}(2)=\frac13,
\qquad
\Theta_{\rm pr}(2)=\frac12.
\]

The proof is not merely numerical. The shared lower bound is a trace/counting argument, and the private lower bound is a genuine pigeonhole bound on two decoder probability vectors.

This is a useful and conceptually clarifying example.

## 2.3 The finite feasible set has an intrinsic partition description

The controlled successor condition

\[
h\sim_t h'
\Longrightarrow
hay\sim_{t+1}h'ay
\quad
\text{for every }a,y
\]

correctly captures deterministic finite-state encoders on the full action-report tree. In particular, the update is not allowed to become task-dependent merely because one task never visits a branch.

This closes an important loophole in weaker history-partition arguments.

## 2.4 The occupancy recursion is an exact representation of the finite support function

The offline occupancy recursion keeps the common update table coupled across tasks and parameters. The manuscript is careful not to pretend that this occupancy is free online memory.

Within the finite model, the backward recursion appears sound: each continuation corresponds to an executable deterministic design, and each support value is the minimum of finitely many linear forms.

The manuscript also correctly acknowledges the common-information/designer dynamic-programming antecedents rather than presenting dynamic programming itself as new.

## 2.5 The delayed-query Gaussian theorem repairs the previous dynamic objection

This is an important improvement.

The v8 sequential Gaussian theorem could be read as terminal dimension plus append-only storage. The v9 delayed-query experiment is different: all \(d\) coordinates are acquired before the independent coordinate query is disclosed.

The lower bound is imposed at the **pre-query** register. The posterior-mean vector has a density bounded below on a cube; any \(S\)-state pre-query register induces at most \(S\) reconstruction centres; the volume argument gives

\[
\mathcal E_S\gtrsim S^{-2/d}.
\]

The matching base-\(L\) construction gives the same order, whereas a query-aware static checkpoint needs only scalar quantization and obtains \(S^{-2}\).

This is a real temporal information penalty. The prior v8 objection should be considered closed for this example.

## 2.6 The finite saturation and finite compiler are real mathematical additions

The saturation section does not simply assume that a finite predictive state exists. It gives a backward construction based on posterior vectors, next-report predictive rows, and successor classes.

The compiler section also improves the resource discussion. For rational finite data it records finite program size, initialization bits, persistent state, transient workspace, and a conservative bit-serial running-time bound. It explicitly allows synthesis to be exponential and does not disguise physical acquisition of a report as free arithmetic.

These are positive changes.

---

# 3. Technical audit of the main finite minimax theorem

I do not see a fatal defect in Theorem thm:v9-minimax as written for its finite class.

The key proof steps are:

1. include controller and decoder tables in the deterministic design;
2. freeze all random tapes to obtain a distribution over complete deterministic common designs;
3. average their row-risk vectors before the outer worst-row operation;
4. use a finite linear programme / convex minimax identity;
5. use nonnegative separation to recover the upper body from lower support values; and
6. retain a mixture index in the actual register when a public shared seed is removed.

This is coherent.

The manuscript also handles a subtle point correctly: for a minimax task the baseline is the full-history minimax risk of the task, not a parameterwise oracle baseline. One controller must work across all rows belonging to that task.

The support-size statement of at most \(M+1\) deterministic designs is a standard finite-dimensional convex consequence. The private implementation then pays the design index in the state, giving the displayed \((M+1)S\) width.

I would still ask the final paper to separate more sharply:

- the new information-pattern statement;
- the classical convex-analysis machinery;
- the already-known designer/common-information dynamic programme; and
- the genuinely new consequences.

At present these are mathematically intertwined in a way that risks making a finite convexification theorem look broader than its novelty claim can presently support.

---

# 4. Major issue I — the exact variational theorem is still too finite to carry the advertised foundation

The central theorem is exact for:

- finite horizon;
- finite parameter set;
- finite hidden states;
- finite reports;
- finite controls;
- finite task family;
- finite action sets; and
- bounded losses.

That is a legitimate and useful class.

But the paper's main object, the marked decision spectrum, is stated more broadly and the research program is much broader still. The exact theorem does not currently extend to the standard-Borel setting in which the earlier terminal deficiency theorem lives, nor to an infinite task family, nor to a stationary/infinite-horizon causal experiment.

More importantly, the proof architecture is fundamentally finite:

- enumerate deterministic designs;
- convexify their finite risk vectors;
- apply finite separation/minimax;
- recurse on a finite occupancy state.

This is not a criticism of correctness. It is a criticism of conceptual scale.

At a top-four general journal, one would expect the finite theorem either to be the visible finite shadow of a more intrinsic theorem, or to solve a finite problem of exceptional independent depth. Here the finite theorem is being asked to support a general-foundations title and an eleven-paper pipeline.

The missing extension need not be maximal generality. But the next version should supply at least one theorem showing that the risk-body/support-function principle survives a genuinely nonfinite class under natural compactness/measurability hypotheses, with the common-encoder constraint retained and without reducing the proof to an unstructured enumeration.

A particularly natural target would be a standard-Borel controlled experiment with compact randomized encoder kernels, measurable selectors, a well-defined closed attainable risk body, and an exact duality for a nontrivial class of task families.

Without such a theorem, v9 is a strong finite causal-decision theorem embedded in a substantially broader framework.

---

# 5. Major issue II — the saturation theorem is over-typed relative to the main hidden-state decision instrument

This is the most concrete new technical issue I found.

Section 3 defines the controlled instrument with hidden state \(Z_t\) and allows terminal losses

\[
\ell_{d\theta}(Z_T,b).
\]

By contrast, Theorem thm:v9-saturation constructs a quotient from:

- the parameter likelihood vector;
- reference next-report probabilities; and
- successor quotient classes.

The text itself correctly warns:

> Additional latent-target marks require the corresponding conditional kernels as further decorations; parameter sufficiency alone does not imply their sufficiency.

That warning is essential. But the theorem then states that the original and quotient **instruments** have mutually exact causal simulations.

If “instrument” here means the full hidden-state marked instrument of Section 3, that statement is too strong.

The construction proves exact reconstruction of the **report stream** under every admissible policy, uniformly over the parameter. It does not, without additional decorations, reconstruct the joint law of latent marks such as \(Z_T\) that appear in the main decision losses.

A simple finite example isolates the problem.

Take one observation time, no control, two parameters \(\theta\in\{0,1\}\), and a strictly positive prior with

\[
\pi(0)=0.9,\qquad \pi(1)=0.1.
\]

Let the report \(Y\) be an independent fair bit under both parameters, and let the terminal hidden target be

\[
Z=Y\oplus\theta.
\]

Because the report law is the same under both parameters, observing \(Y\) does not change the parameter posterior. At the terminal time, the v9 saturation key imposes only the posterior condition, so the two report histories have the same saturated class.

Yet for the decision problem “guess \(Z\)” with zero-one loss:

- with the actual report \(Y\), the Bayes rule \(b=Y\) has error \(0.1\);
- from the terminal quotient class alone, \(Z\) is marginally fair and the best constant decision has error \(1/2\).

The v9 reconstruction kernel can reproduce a fair report from the quotient transition, but unless the quotient is additionally decorated with the correct latent-target conditional law, the synthetic report is not coupled to the latent \(Z\) in the way required by the decision loss.

This does **not** refute the report-process reconstruction theorem. It refutes a broad reading of “mutually exact causal simulations” as a theorem about every hidden-state marked task admitted in Section 3.

The fix is conceptually straightforward but must be made theorem-level:

1. rename/retype the object as the parameterized report experiment and state exact simulation only for its observable report process; or
2. extend the saturation key by the required latent-target conditional kernels and prove exact simulation of the marked instrument; or
3. formulate a marked saturation theorem indexed by a declared family of downstream task marks.

Until this is repaired, the manuscript's finite sufficiency bridge is not correctly typed against its own main risk-body theorem.

This issue also affects pipeline language wherever thm:v9-saturation is cited as though it automatically preserves arbitrary downstream latent observables.

---

# 6. Major issue III — “least saturated quotient” is least only inside a definition that already prescribes most of the answer

The backward construction in thm:v9-saturation appears correct for the class it defines.

But the minimality statement must be interpreted narrowly.

A coordinate is declared saturated and predictive only if it:

1. determines the full parameter posterior vector;
2. determines every raw next-report predictive vector for every control; and
3. has a deterministic recursive update.

The backward key is then built precisely from those quantities and future classes.

It is therefore unsurprising that every coordinate satisfying those same requirements refines the constructed key.

That is useful canonicalization, but it is not a minimality theorem among:

- all exact causal simulators;
- all decision-complete coordinates for a given task family;
- all Blackwell-equivalent finite experiments;
- all randomized recursive realizations; or
- all resource-optimal marked quotients.

The manuscript says this in places, but the title “least saturated finite quotient” and the surrounding foundation rhetoric make the stronger reading easy.

For top-four significance, one needs a more intrinsic necessity statement.

For example, a substantially stronger theorem would characterize the minimum state size needed for parameter-uniform causal equivalence of the observable experiment, without requiring a priori that the state explicitly determine the chosen posterior and raw-prediction coordinates. Another route would characterize the minimal marked quotient for a declared class of decision tasks.

The present theorem is an effective Myhill–Nerode-style canonical refinement within a specified coordinate vocabulary. That is mathematically valid, but it is not yet the universal causal-sufficiency object suggested by the broader architecture.

---

# 7. Major issue IV — the finite compiler is honest, but not yet an intrinsic resource theory

Theorem thm:v9-compiler improves the manuscript because it refuses to hide computational cost.

For rational finite data it supplies:

- exact finite synthesis;
- rational optimal mixtures;
- dyadic approximation from \(p\) fair bits;
- explicit fixed-description size;
- explicit persistent-state enlargement when the shared design index must be stored;
- logarithmic transient counters under sequential table access; and
- a conservative bit-operation bound.

I see no immediate contradiction in those accounting statements.

The limitation is that the theorem is essentially a universal finite-table compiler.

The synthesis may require enumeration of the entire deterministic design set and may be exponential in horizon, report count, hidden-state count, or task count. The saturation construction is polynomial only in the **expanded history tree**, which itself may be exponentially large.

Thus the theorem establishes computability and finite description, not tractability or an intrinsic complexity law.

For a paper whose title emphasizes “resource-aware reduction,” the next conceptual step should not be another list of resource counters. It should be a theorem connecting a structural property of the experiment to computational synthesis complexity.

Examples of meaningful targets would be:

- fixed-parameter polynomial synthesis under bounded treewidth / bounded continuation width;
- a separation between memory complexity and synthesis complexity;
- hardness of computing the optimal common-encoder spectrum;
- approximation schemes under natural mixing or low-rank conditions; or
- a resource-composition theorem that controls program, memory, randomness, and time under causal morphisms.

At present “resource aware” is accurate bookkeeping, but not yet a general complexity theory.

---

# 8. Major issue V — the common variational principle is real, but it still does not unify the retained mathematical regimes

Revision 9 materially improves this point over v8.

The same finite risk body now yields:

- the common controlled minimax theorem;
- the occupancy support recursion;
- the common quadratic conditional-variance formula;
- the finite A1 maximum-over-tasks specialization; and
- a finite exponential-moment / risk-sensitive specialization.

The delayed-query Gaussian theorem is also conceptually connected to the same conditional-variance geometry.

This is genuine progress.

But the paper still retains major regimes whose sharp rates arise from different mathematical objects:

- predictive-tree energy and separated-cylinder geometry;
- Wasserstein law-presentation entropy;
- terminal Blackwell–Le Cam comparison;
- Gaussian experiment approximation;
- count/Poisson experiment comparison;
- nonlinear filtering examples; and
- historical microscopic dynamical-system interfaces.

The v9 variational principle does not produce all of those as specializations of one intrinsic functional. It does not, for example, derive the Wasserstein presentation entropy from the common-encoder risk body, nor compute the predictive-tree energy as a dual risk support, nor turn the A2 algebraic primary chain into a consumer of the finite decision theorem.

Therefore the manuscript has moved from “umbrella only” to “one real finite core plus several retained surrounding theories.” That is a significant improvement, but it still falls short of the global unification implied by General Theta Foundations I.

The strongest route forward would be to decide what the actual invariant is.

If it is the attainable upper risk body, then prove a broad theorem showing that the other resource profiles are recoverable as marked decision bodies after precise output/task choices.

If it is a richer marked object, define it so that tree energy, metric entropy, experiment deficiency, and delayed-query variance are provable projections of one structure rather than parallel sections.

---

# 9. Major issue VI — the novelty boundary of the central finite theorem is not yet closed

The manuscript deserves credit for unusually explicit attribution discipline.

It says, correctly, that:

- Blackwell/Le Cam/Torgersen supply classical comparison and convex-separation foundations;
- Witsenhausen and later real-time coding work are close structural neighbours;
- the common-information/designer dynamic-programming idea is established;
- Nayyar–Mahajan–Teneketzis already treat finite local memory and an unconditional designer occupancy in a no-common-history case;
- predictive equivalence / continuation ideas have Nerode and computational-mechanics antecedents; and
- the finite Gaussian volume lower bound is elementary quantization geometry.

This honesty makes the novelty question sharper.

What exactly remains new enough for a top-four general journal?

The candidate is the **combination**:

- one encoder common to a finite family of tasks;
- one controller per task across parameter rows;
- an exact attainable risk body;
- the corresponding support-function dual;
- controlled continuation partitions;
- distinct private versus shared randomization;
- and the priced design-index conversion.

That may well be a publishable contribution.

But the current literature audit does not yet establish that this precise combination is absent from filtered statistical experiment comparison, finite-memory stochastic control, real-time coding, information-constrained team/control theory, or robust/POMDP finite-controller optimization.

In particular, the manuscript itself records only a publisher-level check rather than a full theorem-by-theorem comparison for Norberg's filtered-experiment work. The Witsenhausen comparison is also not a full proof audit.

For a specialist venue, a focused novelty statement and ordinary revision could be enough. For a top-four journal, the paper must know its nearest theorem-level predecessors exceptionally well.

I therefore regard **priority certification as open**, exactly as the repository documentation itself does.

A future submission should include a theorem-by-theorem crosswalk that distinguishes:

1. the known finite-memory/control recursion;
2. the known statistical-experiment comparison structure;
3. the known convex risk-set formalism;
4. the known public/private common-randomness phenomena; and
5. the genuinely new common-encoder minimax theorem after all those ingredients are removed.

Without this, a referee cannot tell whether the central theorem is a deep new invariant or a well-organized synthesis of known finite machinery.

---

# 10. Major issue VII — the repository-level pipeline remains overwhelmingly conditional

This is the decisive programmatic issue.

The v9 PIPELINE_DEPENDENCIES.json contains eleven components:

A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, D1.

Its own status classification is:

- **A1: verified_protocol_adapter**
- **A2: verified_protocol_adapter**
- **A3: conditional_interface_only**
- **A4: conditional_interface_only**
- **B1: conditional_interface_only**
- **B2: conditional_interface_only**
- **B3: conditional_interface_only**
- **B4: conditional_interface_only**
- **C1: conditional_interface_only**
- **C2: conditional_interface_only**
- **D1: conditional_interface_only**

The machine-generated contract check records exactly:

- 11 components;
- 2 verified protocol adapters;
- 9 conditional interfaces;
- 0 imported historical model gates; and
- live_heads_checked = false.

This is honest repository engineering. It is also strong evidence against the paper's current programmatic role as a completed foundation.

## 10.1 A1 is a real but narrow consumer

The v9 A1 adapter now genuinely benefits from the new common maximum-over-tasks quadratic formula and the unchanged-width private polynomial formulation.

But its verified scope is explicitly finite command support, finite horizon, finite report alphabet, fixed prior, and weighted quadratic tasks.

The continuous-command geometry and collision-scale structure of the broader A1 program are not derived by GTF.

## 10.2 A2 remains structurally independent at its primary theorem level

The current A2 branch is the v122 intrinsic-primary/K3-boundaries revision, and the v9 dependency record watches its current ref.

But the same dependency record explicitly states:

**primary_chain.status = independent_not_consumed**

and

**verified_gtf_dependency = false**.

Thus even the current A2 primary theorem chain is not a consequence of General Theta Foundations I.

The verified A2 GTF adapter remains the statistical known-mark finite-experiment window, not the present primary algebraic geometry.

This matters because “the pipeline contains A2” and “A2's primary theorem depends on GTF” are very different statements.

## 10.3 The nine remaining components do not become verified because v9 labels were attached

For A3/B2/B3/C2, v9 minimax/stability labels transport decision risks only after the actual physical/statistical simulator has been proved.

For A4/C1, v9 saturation/compiler labels require the true predictive kernel, likelihood saturation, and correctly typed conditional structure.

For B4/D1, occupancy/pressure formulae do not create the missing nonlinear semigroup or phase model.

For B1, terminal sufficiency does not produce the Fourier/local-coefficient estimates.

These are exactly the right distinctions to record. They are also exactly why the foundation is not yet visibly driving the pipeline.

A top-four foundation for this program should discharge nontrivial hypotheses in several difficult downstream papers, not merely provide a correct interface conditional on those hypotheses.

---

# 11. The current A2 branch makes the pipeline limitation especially visible

The current A2 v122 work is mathematically far from the finite causal-decision theorem: its primary chain concerns relation tensors, ramification determinants, intrinsic embedded torsion, primary powers, and recovery of genus-one/K3 geometry from a multiplication-failure scheme.

The GTF v9 contract does not claim to derive that chain. This is appropriate.

But it exposes a structural question for the whole theta-theory program:

**What makes these papers one theorem pipeline rather than a repository containing several mathematically distinct programs under a common governance layer?**

At present, GTF gives useful language and protocol-level comparison tools, while A2's principal algebraic theorem is independent.

That is not a defect in A2. It is a challenge to GTF's foundational claim.

The same issue is even stronger for the conditional dynamical, kinetic, nonlinear-semigroup, and operator-theoretic components.

---

# 12. Major issue VIII — the manuscript is still architecturally too broad for the depth of its central new theorem

The canonical article is 47 pages, while the complete preserved development is 140 pages.

The repository has done a good job separating canonical and archival objects. Nevertheless, the principal paper still asks one new finite theorem to support a very broad title and a large retained mathematical ecosystem.

The result is an asymmetry:

- the sharpest new theorem is finite and decision-theoretic;
- the broadest prose is programmatic and cross-domain;
- the strongest retained results have heterogeneous assumptions and proof mechanisms; and
- most downstream components remain conditional.

A top-four article should make the central theorem feel inevitable and dominant.

I would strongly consider one of two strategies.

### Strategy A — deepen the central theorem

Extend the common-encoder risk-body theorem to a broad measurable controlled class, give an intrinsic minimal marked quotient, and prove nontrivial downstream applications that genuinely discharge model hypotheses.

### Strategy B — narrow the paper

Present the finite controlled common-encoder theorem, shared/private randomization, finite quotient construction, compiler, and delayed-query Gaussian theorem as one focused paper. Move the retained historical regimes entirely to a companion/reference document.

The repository can preserve all material without forcing the journal article to carry the whole history.

At present the paper is mathematically improved enough that narrowing would be a strength, not a retreat.

---

# 13. Technical comments on the saturation theorem

## 13.1 Retype “original and quotient instruments”

As explained above, replace this by “parameterized report experiments” unless all latent marks required by the task family are included in the quotient.

## 13.2 Make the marked extension a formal theorem, not a sentence

The sentence saying that latent-target marks require decorations is correct but insufficient.

Give a theorem: for a finite family of marks \(W_t\), define a marked key containing the relevant conditional kernels and prove exact marked reconstruction. Then state precisely which decision tasks are preserved.

## 13.3 Separate posterior sufficiency from causal realization

The parameter posterior is one kind of statistical sufficiency. Raw-report prediction is another property. Decision completeness for latent losses is a third.

The current terminology sometimes lets these slide together.

## 13.4 The minimality theorem should state its category in the theorem title

Something like “minimal posterior-and-report-predictive recursive coordinate” would be more accurate than an unqualified “least saturated finite quotient.”

---

# 14. Technical comments on randomization and the risk body

## 14.1 The shared-seed order must remain explicit everywhere

The theorem is correct only because the independent seed is averaged before the adversarial row is selected. Do not abbreviate this later as an ordinary randomized minimax theorem without restating the order.

## 14.2 The \(M+1\) factor is not uniform

The paper says this. Keep it prominent.

For growing task families, the difference between \(S\) and \((M+1)S\) can affect finite-resource statements and can affect asymptotics if \(M\) grows with the resolution.

## 14.3 Randomized initialization is part of the model

The private implementation uses a sampled design index before observations. If a downstream model forbids such initialization, the interface must pay for an enlarged convention.

The manuscript says this locally. The pipeline contract should propagate it explicitly to every consumer using the seed-price inequality.

## 14.4 Avoid calling support-function completeness a classification of the experiment

The support function determines the **chosen finite risk body**. That is a finite convex-geometric classification of that marked task system, not a Blackwell-equivalence classification of the full controlled experiment unless the task row family is decision complete.

This distinction is especially important when comparing two experiments.

---

# 15. Technical comments on the occupancy recursion

The occupancy recursion is a useful proof device.

But the novelty claim should not rest on the fact that such a recursion exists. The manuscript itself recognizes designer/common-information antecedents.

The genuinely distinctive statement is the equality between that recursion and the support function of the **coupled common-encoder minimax body**, with the same update map across tasks and the same task controller across parameter rows.

I recommend stating that as the central novelty sentence and deleting broader claims that could be read as inventing finite-memory occupancy dynamic programming.

It would also help to provide a nontrivial worked example where:

- taskwise-optimal encoders differ;
- the common-encoder optimum is strictly worse;
- the outer dual weight is nondegenerate; and
- the private and shared optima differ.

The current seed-gap example addresses the last point, but a single example exhibiting the full common-encoder dual geometry would make the theory easier to evaluate.

---

# 16. Technical comments on the finite compiler

## 16.1 Distinguish source size from expanded-tree size

The saturation construction is polynomial in the expanded history tree, not necessarily polynomial in the succinct source description.

This distinction should be repeated anywhere “polynomial” appears.

## 16.2 State synthesis complexity separately from execution complexity

The online table scan is finite and explicitly bounded. The offline search over deterministic designs can dominate everything.

Readers should not conflate a finite compiled implementation with an efficient compiler.

## 16.3 Program-description bounds are representation dependent

The displayed \(P_0\) is a valid table-code upper bound. It is not an intrinsic Kolmogorov/minimal-description complexity of the encoder.

Use “table description length” consistently.

## 16.4 Exact rational probabilities versus fixed fair-bit sampling

The manuscript correctly notes that exact non-dyadic sampling generally requires a different time/randomness convention. Keep this caveat theorem-adjacent.

---

# 17. Technical comments on the delayed-query Gaussian theorem

This theorem is one of the best parts of v9.

I would nevertheless sharpen three points.

## 17.1 State the information pattern as a formal experiment

The prose says observations are discarded before the query and that there is no external transcript. This should be encoded in a formal causal signature adjacent to the theorem.

## 17.2 Separate cardinality from arithmetic

The theorem allows unrestricted real evaluation of the posterior mean \(m(x)\). The paper says this. The finite compiler does not automatically apply because the Gaussian input is continuous.

A future “resource-aware” Gaussian theorem should quantify finite-precision evaluation of \(m\), threshold comparison, and input acquisition.

## 17.3 Explain the connection to the finite variance theorem precisely

The lower bound uses the same conditional-variance geometry, but the history space is continuous and the finite combinatorial successor-partition theorem is not literally being applied.

The current final paragraph mostly says this correctly; retain that precision.

---

# 18. Literature and priority work required before top-four resubmission

I would require a substantially more complete nearest-neighbour audit.

At minimum:

1. filtered comparison of statistical experiments with temporal information;
2. finite-state controller optimization for POMDPs / robust POMDPs;
3. real-time source coding with finite memory;
4. common-information / coordinator formulations;
5. constrained experiment design with common encoders across multiple tasks;
6. public versus private randomization under memory constraints; and
7. finite automata / probabilistic bisimulation / predictive-state minimization where the comparison is genuinely theorem-level.

The paper need not prove that every ingredient is new. On the contrary, it should isolate the smallest theorem that is new after all classical ingredients have been removed.

A top-four novelty claim based on “this exact combination does not appear in the sources we checked” is not yet enough when several closest sources were not audited at proof level.

---

# 19. Concrete revision requirements

For a future top-four reconsideration I would want a package along the following lines.

## E9.1 — repair the saturation theorem's type

Either:

- restrict it explicitly to the parameterized report experiment; or
- prove a marked saturation theorem preserving the latent target kernels required by the main task family.

The current broad “mutually exact causal simulations” wording should not survive unchanged.

## E9.2 — strengthen minimality beyond a definition-built coordinate class

Prove a necessity theorem for all exact finite causal simulators / marked decision-complete quotients, or make the present narrower categorical minimality completely explicit in title and claims.

## E9.3 — move beyond finite enumeration

Give a standard-Borel / compact controlled common-encoder version of the risk-body duality, or another nonfinite theorem showing that v9 is not only a finite LP architecture.

## E9.4 — close the priority boundary

Supply a theorem-level comparison to the nearest filtered-experiment, real-time coding, finite-memory control, and common-information results.

## E9.5 — make the pipeline consume the foundation

Turn several conditional interfaces into actual verified adapters that discharge nontrivial model hypotheses.

For example, I would regard conversion of **at least three** of A3/A4/B2/B3/B4/C1/C2/D1 from conditional interface to genuine theorem-level consumer as materially more persuasive than adding more framework sections.

This is not a magic numerical threshold; the point is that consumption should reach difficult model mathematics, not only protocol fragments.

## E9.6 — decide whether current A2 belongs to the dependency chain

The present A2 primary chain is explicitly independent. Either explain why that is compatible with the intended logical architecture, or prove a real GTF dependency. Do not imply dependence merely because both live in the same repository.

## E9.7 — reduce architectural breadth if the stronger theorem is not pursued

A focused finite causal-decision paper containing:

- the common-encoder risk body;
- controlled partitions;
- private/shared randomization;
- finite saturation;
- the compiler; and
- delayed-query Gaussian complexity

could be much easier to judge on its own mathematical merits.

---

# 20. Final assessment

Revision 9 is a substantive success as a response to the previous referee.

It closes the most important v8 request: there is now a genuine controlled common-encoder minimax theorem with the correct coupled feasible set and a real variational representation.

It also adds two particularly valuable pieces:

- a mathematically explicit shared-versus-private randomization separation; and
- a delayed-query Gaussian theorem where causality changes the cardinality exponent.

These changes mean that I would no longer criticize General Theta Foundations I as merely a container with no central theorem.

But the top-four question is stricter.

The new central theorem is still finite and assembled from classical convex/minimax and occupancy ingredients whose precise novelty boundary remains incompletely audited. The new saturation theorem has a real type/scope defect if interpreted as equivalence of the full hidden-state marked instrument, and its minimality is narrower than the broad foundation language suggests. The effective compiler proves computability rather than a structural complexity theorem. Most importantly, the repository-level pipeline remains two verified protocol adapters and nine conditional interfaces, with the current A2 primary chain explicitly independent of GTF.

Accordingly my recommendation is:

**REJECT / RETURN IN THE PRESENT FORM for Annals / Inventiones / JAMS / Acta standard.**

I would encourage a mathematically substantive revision, not another layer of manifests or local patches. The next decisive advance should be one of:

- a genuinely nonfinite common-encoder classification/duality theorem;
- a correctly typed minimal marked causal quotient;
- multiple hard downstream theorem adapters that visibly consume the foundation; or
- a narrower paper whose title and claims match the finite theory now actually proved.

The v9 mathematics is serious enough that the remaining gap is no longer “write down a theorem.” The remaining gap is to show that the theorem is both **intrinsically new at the required scale** and **actually foundational for the program it is claimed to organize**.
