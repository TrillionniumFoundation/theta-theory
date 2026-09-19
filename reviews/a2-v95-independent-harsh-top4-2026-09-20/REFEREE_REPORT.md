# Independent harsh referee report on A2 revision 95

**Review date:** 20 September 2026  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** revision/a2-v95-real-valuations-cubic-classification-2026-09-19  
**Reviewed exact head:** ebb796e49ca51a62b90d92ec0d09819cfe8d00a4  
**Controlling previous report:** reviews/a2-v94-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md  
**Controlling previous report commit:** dbbad2d84c6a3b358bddabf84dc16f0b09b38634  
**Previous reviewed manuscript head:** 5e01e5a2d6e93ef4c1e2619707608626fdc0f6cf  
**Reviewed manuscript:** *Projective polynomial observations: real valuations and identifiable singularities*  
**Author:** Qian Qi  
**Review status:** owner-requested AI-assisted external-referee-style assessment; not a journal-commissioned peer review.

## 1. Recommendation

**Recommendation to the editor: reject in the present form at the stated four-leading-general-mathematics-journal level, while recognizing that revision 95 is a substantial theorem-level advance and that I no longer see the central mathematical deficiency identified in revision 94.**

This recommendation is materially different from the revision 94 report.

Revision 94 ended by saying that any one of three developments would materially change the top-level assessment:

1. finite singular-germ Newton data obtained before optimizing the observation-ball envelopes;
2. a classification of a nontrivial family of identifiable stochastic singular intersections;
3. an explicit computation of the flagship leading coefficient fibre and its exact asymptotic constant.

Revision 95 attempts, and in large part succeeds at, **all three simultaneously**.

The new finite real-valuative theorem replaces the optimized coefficient-envelope definition of the exponent by finitely many orders on accessible real divisors. The new cubic theorem classifies the exact fibre for a two-parameter double-root/triple-root family and gives a necessary-and-sufficient nonidentification criterion. The new leading-fibre theorem writes the complete first nontrivial coefficient fibre explicitly and reduces its diameter to two finite Fisher least-squares programs, with stochastic arcs realizing the extremal shapes.

I did not find a fatal counterexample to these three new results. The discriminant calculation, the affine-pencil classification, the whole-model recovery mechanism, the one-sided Fisher projection, the real-cubic leading set, and the diameter calculation are mutually consistent on the stated domain. The manuscript has therefore crossed an important mathematical threshold: this is no longer merely an exact language for a singular modulus plus one lower-bound path.

My remaining negative recommendation is a **top-four significance, novelty-boundary, and theorem-architecture judgment**, together with several places where the new general theorem is still proved at a level of compression that I would not accept in a final general-journal version.

The main issue is now the following. The finite-divisor part of the new general theorem lies very close to classical resolution/Łojasiewicz technology and to current valuative finite-max theory. The genuinely model-specific content is the accessible-real probability graph, the weighted cluster specialization, and the complete stochastic leading fibre. Yet the manuscript does not isolate that delta sharply enough. At the same time, the strongest fully explicit nonclassical classification remains a highly structured binary cubic family. I do not yet see the broad singularity-classification theorem, wall-chamber theorem, or model-wide stratification result that would make this framework unavoidable at the Annals/Inventiones/JAMS/Acta level.

This is no longer a request for another incremental closure round. If the authors continue to target a leading general mathematics journal, the next step should be a conceptual consolidation and generalization, not another accumulation of special lemmas.

## 2. Scope of review and source pin

I reviewed the revision 95 branch at exact head

ebb796e49ca51a62b90d92ec0d09819cfe8d00a4.

Relative to the revision 94 manuscript head, the revision adds the new v95 main article sources

- article/v95/finite_newton.tex;
- article/v95/cubic_geometry.tex;
- article/v95/cubic_leading.tex;
- article/v95/model.tex;
- article/v95/global_statements.tex;
- article/v95/paper.tex;
- article/v95/references_extra.tex;

together with the complete and core entrypoints, response to the v94 report, source manifest, local validation receipts, diagnostics, verifier, and branch-scoped native workflow.

I read the complete new core argument, the response to the v94 report, the controlling v94 referee report, the retained theorem graph referenced by the new proofs, the new exact-head verifier, and the finite diagnostic code and receipt. I also inspected the exact-head Actions state.

At the time of this review, workflow run 35445410633 for exact head ebb796e49ca51a62b90d92ec0d09819cfe8d00a4 was still **queued** and had no conclusion. The branch itself records that the 12-page core was compiled locally, while the full inherited-appendix manuscript was not compiled locally and an exact-checkout source audit was not executed locally. I therefore do not record the complete exact-head manuscript as successfully compiled or source-audited.

This is an operational qualification, not a mathematical reason for rejection. The authors correctly label the finite diagnostics as regressions rather than proof verification, and I treat them only as such.

## 3. What revision 95 genuinely accomplishes

### 3.1 The previous “optimized envelope” objection is substantially answered

Theorem “Finite real-valuative Newton formula” is the theorem-level answer that the revision 94 report requested.

The input is now the actual real observation-spectral graph. The proof introduces the squared observation distance G and the squared cluster coefficients H_{r,a}, simultaneously monomializes them, discards complex exceptional divisors with no accessible real point, and reads the coefficient orders from finitely many ratios b/a. The spectral exponent is then obtained by dividing by the appropriate cluster-root weight m_r-a.

This is conceptually stronger than revision 94. The exponent is no longer defined by first maximizing each coefficient over every observation ball and then taking the Puiseux order of that optimized function.

The real-locus qualification is also important. For a stochastic model with active inequalities, a complex exceptional divisor without an admissible real transversal must not be allowed to determine the observable exponent. Revision 95 says this explicitly.

### 3.2 The weighted leading specialization is the most interesting general part of v95

The construction with t = epsilon^q, rescaled observation variables, and simultaneously rescaled cluster coefficients is a useful general object.

It retains:

- the full real admissibility constraints;
- all relations among coefficients within a cluster;
- relations across distinct clusters;
- the observation metric;
- bounded model coordinates until closure;
- the finite root-permutation geometry needed for the target bottleneck metric.

This is substantially better than multiplying independent coordinate envelopes. In my view, this joint real weighted specialization, not the bare existence of finitely many divisorial ratios, is the part of the general theorem with the clearest chance of constituting a distinctive contribution.

### 3.3 The cubic family is now classified, not merely exhibited

The revision 94 example was one tuned identifiable point. Revision 95 replaces that with a two-parameter family

f(z) = z(z-r)^2,    g(z) = (z-s)^3,    0 < s < r < D,

and determines the complete real-rooted affine pencil.

The discriminant factorization gives the only possible additional branch, and the theorem incorporates both the root-domain restriction z_* <= D and the stochastic weight floor c_* <= gamma/alpha_*.

The result is a genuine necessary-and-sufficient statement for the exact spectral fibre of the specified family, over the entire closed stochastic model. The open region

0 < s < 2rD/(3D-r)

is therefore a real identifiable region, not a single algebraically tuned equality.

This directly answers one of the main revision 94 objections.

### 3.4 The whole-model coefficient recovery proof is much more convincing

The revised proof now writes the key singular-value transfer explicitly. It distinguishes the fixed row span from the perturbed row span, controls V'^{-1} using the second singular value of the observable second marginal, uses monicity to normalize the affine coefficients, excludes both rows collapsing onto the same component, and then recovers the non-root parameter matrices by fixed coefficient functionals.

That is the right structure. In particular, the leading-score calculation is no longer silently assuming that nuisance parameters remain controlled.

### 3.5 The flagship leading fibre is actually computed

This is the largest concrete improvement.

The leading cluster polynomials are claimed to be exactly

z,    z^2 - X,    z^3 - Yz - Z,

subject to

X >= 0,   Y >= 0,   J(X,Y) <= 4,   27 Z^2 <= 4 Y^3.

The endpoint motion is treated as a one-sided nuisance direction, the free channel/weight/root-sum directions are projected out in the Fisher metric, and the remaining cost J is an explicit piecewise quadratic program.

The proof also correctly distinguishes the symmetric triple split from the true diameter. The shapes (-2h,h,h) and (-h,-h,2h) show that the symmetric split is not extremal for the complete triple fibre.

This closes the most concrete gap in revision 94.

### 3.6 The exact asymptotic constant is reduced to finite linear algebra

The formula

C_P = max{ sqrt(2) kappa_x^(-1/4), 2 sqrt(2/3) kappa_y^(-1/4) }

is a genuine explicit finite program, not a renaming of the original inverse observation-ball optimization.

The homogeneity argument giving X_max and Y_max, and the sorted-triple diameter calculation, are coherent. The stochastic realizing arcs make the result stronger than a tangent-cone outer bound.

### 3.7 The statistical claim is now appropriately scoped

The manuscript repeatedly says that the risk theorem concerns a shrinking, center-known oracle neighbourhood. The two-point lower bound and constant-decision upper bound are consistent with that local experiment.

I do not regard the statistical statement as a global adaptation theorem, and the manuscript no longer presents it as one.

## 4. Major objection I: the novelty boundary of the finite real-valuative theorem is still not sharp enough

The general exponent theorem now uses exactly the kind of finite divisorial information that one expects after principalization/resolution.

That is mathematically legitimate, but it creates a serious novelty-positioning burden.

Bierstone-Milman supply the real/subanalytic uniformization and resolution technology. Bivià-Ausina and Encinas explicitly give an effective resolution-based method for Łojasiewicz exponents. More importantly for the current timing of this submission, Hà's 2026 preprint develops a valuative theory of Łojasiewicz exponents whose advertised central contribution is a finite-max principle and which also includes stratification, stability, and wall-chamber phenomena in families.

The manuscript cites these works, but the current prose still understates the proximity.

Saying that the classical papers provide “the mechanism” while this paper applies it to the real probability graph is not yet enough. The editor and reader need a theorem-by-theorem delta.

In particular, the paper should separate the following statements.

1. **Classical consequence:** after resolving/principalizing finitely many semialgebraic or algebraic functions, a Hölder/Łojasiewicz exponent can be read from finitely many order ratios.

2. **Real-accessibility refinement:** only divisors with admissible real transversals contribute to the stochastic model.

3. **Root-cluster weighting:** the spectral exponent is the minimum of coefficient orders divided by root multiplicity weights.

4. **Joint leading-object theorem:** simultaneous weighted specialization, with all real constraints retained, produces the complete leading coefficient fibre.

5. **Target-diameter theorem:** the root image of that joint fibre yields the leading spectral diameter.

Items 2-5 are where the paper can plausibly claim a distinctive observation-spectral contribution. Item 1 should not carry the rhetorical weight of the main novelty.

At present the abstract and introduction place the finite real-valuative formula first and give it a “Newton” framing that risks making a classical resolution calculation sound more novel than it is. I would reverse the emphasis: make the joint constrained specialization the central theorem, and state the divisor formula as the finite computation of its exponent.

### What I require here

The revised paper should contain a precise comparison proposition or table that says which parts follow formally from known Łojasiewicz/resolution theory and which parts do not. For the Hà preprint in particular, the authors should compare hypotheses and outputs, not merely cite it as philosophical support.

The crucial question is:

**What theorem in revision 95 would still be new if the reader granted the strongest applicable finite-max valuation theorem for the relevant ideals/filtrations for free?**

That theorem should become the centerpiece.

## 5. Major objection II: the “effective finite algorithm” is too compressed for the strength of the claim

Lemma “Construction of the data” and Proposition “Effective leading fibre and diameter” contain several strong effective assertions.

I believe the route is plausible, but the proof currently compresses too many nontrivial operations into a few paragraphs.

The claimed pipeline is roughly:

- decompose a compact semialgebraic graph into basic closed pieces;
- convert inequalities into algebraic square-slack lifts;
- resolve the resulting algebraic sets;
- recursively cover uncovered lower-dimensional singular real loci;
- principalize all nonzero G and H functions;
- decide which exceptional divisors have accessible real generic points;
- choose and encode the correct local cluster branches;
- impose rational weighted rescaling;
- take the real closure at epsilon = 0 while retaining all model coordinates;
- project bounded model variables;
- eliminate quantifiers;
- encode complex root multisets over the reals;
- encode the bottleneck matching over finitely many permutations;
- maximize a semialgebraic objective;
- output an isolating polynomial and rational interval for C_{P,X}.

Every one of these steps is standard-looking in isolation. The complete composition is nevertheless the theorem.

At four-leading-journal standards, “one can do this by resolution and quantifier elimination” is not enough when the result is advertised as an effective singular Newton procedure.

### Specific gaps of presentation

First, Definition “Real monomial data” should explicitly say what happens on source components on which G is identically zero. The proof discusses identically vanishing functions, but the definition only explicitly gives the alternative for H. Positive-dimensional exact fibres make this more than a cosmetic point.

Second, “real algebraic input” should be formalized once. Are all endpoints, clocks, weights, observation probabilities, graph coefficients, and cluster-isolating data required to be real algebraic? What exact representation is part of the input?

Third, the recursive real-locus construction deserves a standalone proposition. The manuscript should prove that the resulting finite collection covers every sufficiently small admissible observation neighbourhood and that every divisor entering the minimum admits the claimed real transversal.

Fourth, the closure-fibre algorithm should be stated as a first-order formula, at least schematically. The phrase “every positive-radius ball meets the set with epsilon > 0” is correct in spirit, but the effective theorem should make the quantifier pattern and bounded variables explicit.

Fifth, the step from a quantifier-free leading coefficient fibre to an isolating polynomial for the diameter should state precisely why the optimum is a single real algebraic number over the input field and how degeneracies of the finite matching minimum are encoded.

I am not asking for complexity bounds. I am asking for a proof-grade specification of the algorithm that the theorem claims exists.

## 6. Major objection III: the complete cubic classification is strong but still too special to bear the full general-journal significance claim

The new cubic classification is a serious result. It should receive more credit than the single-point v94 construction.

But it still lives in a very narrow geometry:

- k = 2;
- d = 3;
- m_1 = m_2 = 2;
- the first channel has two identical columns at the singular datum;
- the second channel is positive and invertible;
- one component has a boundary simple root plus a double interior root;
- the other has a triple interior root;
- the exact-fibre problem reduces to a one-dimensional affine pencil of cubics;
- the real-rooted pencil can be solved by one discriminant and one rational critical point.

The open set in (r,s) is important, but openness in two root-location parameters is not the same as a classification of an open class of stochastic singularity types.

The paper partly acknowledges this. It explicitly says that it is not classifying every binary cubic model or every multiplicity pattern. That is the correct disclaimer.

For a specialist paper, the theorem may already be enough. For a leading general mathematics journal, I would want the family theorem to be converted into a **stratification or wall-chamber theorem**.

The natural walls are already visible:

- the pencil-discriminant transition at s = 2r/3;
- the geometric boundary z_* = D;
- the stochastic weight wall c_* = gamma/alpha_*;
- channel-rank changes;
- multiplicity changes;
- movement of the endpoint root into the interior.

Revision 95 analyzes several of these separately, but it does not yet assemble them into a finite singularity atlas.

### What would materially strengthen this part

A theorem of the following type would change my assessment:

> For a nontrivial semialgebraic class of binary cubic stochastic observations, parameter space admits a finite stratification such that the exact spectral fibre type, intrinsic exponent, and leading coefficient-fibre type are constant or given by finitely many explicit formulas on each stratum, with stated wall transitions.

That would connect the new family calculation to the finite-valuative general theory and would be much closer to a field-level organizing result.

## 7. Major objection IV: stability of the exact leading constant is not developed enough

The leading constant theorem is explicit at a fixed rank-one datum, but the paper says relatively little about how the finite program behaves as the datum moves.

This matters because the diagnostics themselves show that the least-squares constants can be extremely small at the sample point:

kappa_x approximately 2.73 x 10^(-11),  
kappa_y approximately 1.42 x 10^(-13),

with a sample leading constant around 2.66 x 10^3.

These numbers are not evidence of an error. They are evidence that the constant is highly conditioned and that the geometry of the projected score directions deserves theorem-level analysis.

The paper proves positivity of kappa_x and kappa_y from coercivity at a fixed point. It also proves uniform coefficient recovery on compact subsets with margins. But it does not characterize:

- continuity or semialgebraicity of kappa_x, kappa_y, and C_P as functions of the family parameters;
- which walls force either kappa to zero;
- the blow-up rate of C_P near those walls;
- whether the extremizing active set in the nonnegative quadratic program changes across finitely many chambers;
- how the leading fibre changes under a small rank-two perturbation of the first channel.

This is exactly the kind of structure that could turn the current explicit example into a reusable singularity theorem.

I strongly recommend proving a finite active-set/wall-chamber description for J, kappa_x, kappa_y, and C_P over compact subregions of the identifiable family.

For representative numerical examples, the paper should also provide rigorous algebraic or interval certificates for the least-squares values if it displays them as mathematical evidence. Floating-point diagnostics are useful regressions, but they should not be the only quantitative illustration of such an ill-conditioned program.

## 8. Major objection V: the complete manuscript remains an accretive research-program compendium

The new 12-page core has a much cleaner spine than revision 94:

model -> finite real-valuative data -> cubic classification -> complete leading fibre -> exact constant.

That is good.

The complete manuscript, however, still activates the full inherited apparatus: global normalization, clock design, quotient geometry, local condition numbers, local minimax results, residues, algorithms, polynomial statistics, intrinsic moduli, singular normal forms, sharp flags, constrained Newton laws, fibres, admissibility, and multiple generations of perturbation theory.

The source manifest emphasizes that all 25 inherited mathematical/bibliography modules remain active and byte-identical.

Preservation is excellent repository discipline. It is not automatically good journal architecture.

A leading general mathematics paper does not become stronger merely because every historically useful theorem remains in the same PDF. The final article should contain the minimum theory needed to make the principal theorem inevitable.

At this stage I would no longer recommend adding further inherited material. I recommend the opposite.

Either:

- make the v95 real-valuative specialization and singular classification the paper, moving most older global/algorithmic material to separate companion papers; or
- prove a genuinely general stratification theorem that makes the inherited apparatus logically necessary to one unified result.

The current hybrid still reads partly as the terminal consolidation of a long research program rather than a single article designed around one decisive theorem.

## 9. The statistical consequence remains correct-looking but secondary

The local minimax theorem is deliberately narrow.

The experiment is centered at a specified P, the parameter set shrinks at radius c N^(-1/2), and the decision rule may use that center. The upper bound therefore comes from a center-dependent constant decision, while the lower bound is a two-point test.

This is mathematically legitimate.

But it should remain a corollary, not a major motivation for the entire article. It does not provide adaptation to an unknown singular stratum, an implementable estimator that discovers the local geometry, or honest uncertainty quantification over the whole stochastic model.

If the paper wishes to make statistics a co-equal contribution, it needs an unknown-center adaptive result. Otherwise the current careful “oracle neighbourhood” language should be retained everywhere, including the abstract and any cover letter.

## 10. Detailed mathematical requests

### 10.1 State G-identically-zero components explicitly in the monomial-data definition

The proof explains that identically zero functions are treated separately, but Definition “Real monomial data” only explicitly gives the identically-zero alternative for H.

If a source component maps entirely into the exact observation fibre, then G is identically zero there. State whether such a component is discarded from exponent computation after recording its target coefficient values, or represented by a separate exact-fibre piece.

### 10.2 Make the cluster-matching step explicit in the general diameter theorem

Formula for C_{P,X} takes a maximum over base clusters. This is valid only after one uses the positive separation of the distinct base roots to show that, for sufficiently small t, an optimal bottleneck matching cannot cross base clusters.

The cubic constant proof says this explicitly. The general proposition should also say it explicitly.

### 10.3 Separate “finite divisor formula” from “finite ordinary-jet formula”

Revision 95 correctly says that it does not claim a universal ordinary Taylor-jet cutoff.

That disclaimer should be elevated. A resolution-generated finite divisor list can encode arbitrarily high blowup complexity and is conceptually different from a finite jet criterion in the original parameter coordinates.

The phrase “finite Newton data” should not invite the reader to conflate the two.

### 10.4 Clarify independence from the chosen real resolution

The proof says that two covers give the same minimum because the coefficient-envelope order is intrinsic.

That proves numerical independence after identifying both with the envelope order. It would be helpful to formulate this as a corollary: the minimum over accessible real divisors on any admissible simultaneous monomialization is a birationally invariant presentation of the same real Łojasiewicz order.

### 10.5 Give a direct theorem for parameter dependence of the real divisorial data

The paper's own cubic family and Hà's current valuative theory both suggest wall-chamber behavior.

If the real-accessible divisor set changes with parameters, how does the minimum change? Even an upper-semicontinuity or finite-candidate result on a fixed algebraic family would connect Sections 2 and 3 much more strongly.

### 10.6 Distinguish stability of the square-root order from stability of the singularity mechanism

The coefficient recovery theorem says that the square-root order persists under sufficiently small perturbations of U, including rank-two U.

But the flagship singular interpretation depends on rank loss at the base datum.

A rank-two perturbation may preserve the repeated-root square-root order while removing the channel-rank singularity. These are different statements. The discussion should make clear which part of the exponent is caused by root multiplicity, which part by the active boundary, and which part by channel rank loss.

### 10.7 Characterize both exact-fibre walls, not only the open identifiable region

The nonidentification criterion involves both z_* <= D and c_* <= gamma/alpha_*.

The paper should discuss what happens at equality in each wall:

- whether the extra fibre is born with zero length or positive length;
- which root hits the domain boundary;
- how the spectral fibre diameter grows beyond the wall;
- whether the local modulus exponent or leading constant changes discontinuously.

This is low-hanging structure already latent in the formulas.

### 10.8 Tighten the literature comparison around the joint leading fibre

The paper currently compares itself to general Hölder metric regularity and to resolution-based Łojasiewicz exponents.

The key missing comparison is with literature on tangent cones/normal cones of definable set-valued maps and initial degenerations of semialgebraic/algebraic families. The authors need not cite an enormous literature, but the joint weighted closure fibre should be positioned against the closest existing “initial set” constructions, not only against scalar exponent theory.

### 10.9 Explain the algebraic-number claim for the exact constant in the presence of square roots and matching minima

The claim is likely correct over real algebraic input. Still, the final proof should make clear that all root coordinates are introduced through polynomial relations over the input field and that every max/min is represented by a finite first-order semialgebraic formula, so the unique optimum lies in the real algebraic closure of that field.

### 10.10 Do not use diagnostic success as evidence for universal theorem correctness

The branch is already careful on this point. Keep that discipline.

The finite pencil grid, symbolic discriminant checks, finite-difference scores, and sample least-squares calculations are useful regression tests. They do not validate the quantifiers in the general real-resolution theorem or the necessity part over all nearby closed-model competitors.

## 11. Reproducibility and source audit

The revision's provenance discipline is strong.

Positive points include:

- the v95 branch is addition-only relative to the controlling review;
- all inherited active modules are checked byte-for-byte;
- the old normalization theorem is checked as retained verbatim;
- the workflow compares runtime HEAD to GITHUB_SHA;
- the exact compiled input graph is intended to be checked through the .fls file;
- the complete manuscript, rather than only the core reading copy, is the workflow target;
- diagnostics are explicitly labeled as non-proof verification;
- artifacts are named by the actual commit SHA.

At exact reviewed head ebb796e49ca51a62b90d92ec0d09819cfe8d00a4, however, the native workflow was still queued when this report was written.

Therefore the correct evidence statement is:

- local core build: reported passed, 12 pages;
- local finite diagnostics: reported passed;
- local full inherited-appendix build: not executed;
- local exact-checkout audit: not executed;
- remote exact-head full build/audit: no successful conclusion available at review time.

The manuscript and response should continue to preserve these distinctions.

## 12. What would change my top-four recommendation

Revision 95 has already done enough that I would **not** ask for yet another special example or another local proof repair.

A further leading-general-journal submission should do one of two things.

### Route A: prove a general singularity stratification theorem

This is the strongest route.

For an explicitly defined algebraic/semialgebraic class of stochastic polynomial models, produce a finite stratification or wall-chamber decomposition on which the following are controlled by finitely many formulas:

- exact spectral fibre type;
- accessible real valuation candidates;
- intrinsic exponent;
- joint leading coefficient fibre;
- active Fisher program;
- leading constant or its finite candidate set.

The cubic calculation should then appear as the first complete cell of the general theorem, not as an isolated bespoke family.

### Route B: narrow the paper and sharpen the truly new theorem

If a broad stratification theorem is not available, the paper should stop trying to carry the entire historical A2 apparatus.

A much stronger specialist-to-general submission could be built around:

1. the real constrained weighted-specialization theorem;
2. a precise novelty theorem relative to classical Łojasiewicz finite-divisor theory;
3. the complete binary cubic classification;
4. the exact leading Fisher fibre and constant;
5. a concise discussion of the oracle local risk consequence.

Move global normalization, algorithmic material, older quotient theory, and unrelated perturbation infrastructure to companion papers.

A shorter article with a sharper novelty boundary would be stronger than the current encyclopedic manuscript.

## 13. Editorial assessment

My assessment of revision 95 is therefore mixed but substantially improved.

**Correctness:** I found no fatal counterexample to the new central claims within the scope reviewed. Several effective-resolution steps need fuller proof-grade specification, but I do not presently regard them as obviously false.

**Originality:** The complete real constrained leading specialization and the stochastic cubic fibre/Fisher calculation look materially more specific than the classical scalar Łojasiewicz machinery. The finite-divisor exponent formula itself is much closer to established and current valuation theory than the manuscript's framing presently suggests.

**Depth:** The cubic family analysis is nontrivial and now complete enough to be interesting. The general theorem is conceptually useful. The combination is serious mathematics.

**Breadth:** This remains the weakest point for the stated venue. The exact explicit classification is still confined to one highly structured low-dimensional family, while the broadest theorem borrows much of its exponent-computation engine from classical resolution/Łojasiewicz theory.

**Exposition:** The 12-page core is much better. The complete manuscript remains too accretive.

**Reproducibility:** The branch discipline is unusually careful, but the exact-head full workflow had no completed result at review time.

## 14. Bottom line

Revision 95 should not be described as “another incremental repair.” It materially answers the revision 94 referee report.

The authors have now supplied finite singular-germ divisorial data, a genuine family classification, and an explicit flagship leading constant. Those are real advances, and I do not see a responsible basis for repeating the old claim that the singular invariant is merely an optimized-envelope reformulation.

The remaining question is whether the resulting package has the conceptual breadth and novelty required for one of the four leading general mathematics journals.

In my judgment, **not yet**.

The finite-divisor exponent mechanism is too close to classical and current Łojasiewicz/valuation theory to carry the main novelty by itself. The genuinely distinctive constrained leading-fibre machinery is not yet developed into a broad stratification theorem. The fully explicit classification and constant are impressive but remain tied to a special binary cubic geometry. And the complete manuscript still carries too much historical infrastructure around a much cleaner new core.

Accordingly, I recommend **rejection at the stated four-leading-general-journal level in the present form**, with a substantially more positive mathematical assessment than in revision 94.

A future version would materially change my recommendation if it either:

- upgrades the cubic calculation into a finite singularity stratification/wall-chamber theorem for a broader stochastic class; or
- sharply narrows the manuscript and demonstrates, theorem by theorem, that the real constrained weighted-specialization result contributes something genuinely beyond the strongest applicable classical and 2026 valuative finite-max results.

That is the level of revision now needed. More diagnostics, more historical appendices, or another isolated example would not address the remaining issue.
