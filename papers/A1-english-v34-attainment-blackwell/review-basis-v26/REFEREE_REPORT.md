# Referee report on A1 English v26

**Manuscript:** *Attainable information, exponent collisions, and adaptive order*, Qian Qi.  
**Assessment date:** 7 September 2026.  
**Examined revision:** `revision/a1-english-v26-separator-capacity-2026-09-07`.  
**Immutable submission:** `a2e5d3737085241137211f1cf21393d5bcafa1ce`.  
**Submission commit timestamp:** 7 September 2026, 15:16:21 UTC.  
**Principal entry point:** `papers/A1-english-v26/main.tex`.  
**Controlling v25 report:** report blob `ef18197ba6213d92d41ac197bd23aa5f7e5194a9`, retained in `papers/A1-english-v26/review-basis-v25/REFEREE_REPORT.md`; the response identifies its originating review commit as `ab0ebddd80f1e46712650eb6730e113e5c66562f`.  
**Previously reviewed submission:** `8a84075ee518035069d38fd9262bd455aff4ac86`.

This is an owner-requested, AI-assisted repository assessment using the requested Annals/Inventiones/JAMS/Acta level of scrutiny. It is not a journal appointment, a human referee report, or formal proof certification. A negative judgment of significance is distinguished throughout from a mathematical counterexample or a missing proof.

All manuscript paths below are relative to the [immutable v26 source directory](https://github.com/TrillionniumFoundation/theta-theory/tree/a2e5d3737085241137211f1cf21393d5bcafa1ce/papers/A1-english-v26). The theorem and equation labels are source locators, not inferred PDF numbering.

## 1. Recommendation

**Reject at the requested four-journal level.** This is not a recommendation of major revision consisting of a few repairable proof defects. I found no fatal counterexample or unresolved central proof gap in the principal collision-classification and graph arguments examined here. The negative recommendation concerns the mathematical advance and reach demonstrated by the submission, including the new v26 material.

V26 makes a genuine addition. Its new statistical lower bound is indexed by separators of the visited-set lattice rather than complete observation orders. Its common event restricts only first acquired blocks, while correctly integrating out completion reports. It also extends collision-path asymptotics to a finite graph-order optimization and distinguishes a fixed order serving an interval of resolutions from one serving only two endpoints. These are mathematical statements with proofs, not merely changes of terminology or packaging.

Nevertheless, the revision does not, in my assessment, establish a sufficiently substantial further advance to reverse the venue recommendation. The separator construction applies an elementary path-hitting union bound to local small-ball estimates inherited from the acquisition charts; vertex splitting gives its classical flow certificate. The analytic phase theorem combines the already available scalar collision-order formula and bit inversion with a finite minimum of maxima of affine functions. The nonconvex four-phase example and the interval-regret calculation are correct and informative, but their new combinatorics is the comparison of partitions of three leaves.

The strongest mathematics remains the collision-uniform conjunction of attainable transversality, global dimension-truncated covering, unconditional lower mass, and a single causal filter. I do not dismiss that conjunction as a Vandermonde calculation. However, the present additions sharpen and organize that theory rather than demonstrate an advance of exceptional breadth or depth at the requested level. This is an editorial assessment of what has been established, not a claim that an identical theorem is already in the literature or that the research program cannot lead to stronger results.

The previous three definite corrections are now closed. They must not be recycled as reasons for rejecting v26.

## 2. Reading scope and limits of this assessment

The reading was pinned to the submission commit above, not to a moving branch name. The latest A1 revision branch search was repeated during this review and still returned v26 as the highest numbered revision.

The inspected principal route comprises the main entry point; the scalar introduction and main classification statement; `core/02_experiments.tex`; `text/operational_model.tex`; `risk_criteria.tex`; `text/exact_information.tex`; `core/03_transversality.tex`; `text/analytic_inputs.tex`; `text/collision_flags.tex`; `text/collision_direct.tex`; and `text/collision_consequences.tex`. For the graph part, the complete `v25/graph_model.tex`, `v25/adaptive_proof.tex`, and `v25/graph_consequences.tex` were read. All new v26 mathematical modules were read: `v26/introduction.tex`, `v26/selection.tex`, `v26/capacity.tex`, and `v26/phases.tex`.

The README, response, actual proof ledger, active principal bibliography, author diagnostic source, and the controlling report's technical assessment, concrete objections, and recommendation were also inspected. The new arguments were assessed against the retained arguments actually present in this submission, rather than inferred solely from the response.

This is not a fresh exhaustive audit of the separately compiled companion, every historical derivation, or the eleven-paper program. In particular, I do not claim to have newly audited the original v10 shared-memory manuscript. The current source explicitly credits that manuscript; the deterministic product construction used here was checked in its retained v25 formulation. The author's historical source-preservation claims are not relabelled as an independently reproduced full-tree identity audit.

No native two-volume LaTeX build, PDF visual inspection, or successful GitHub Actions run was executed or certified in this review. The README itself distinguishes an isolated typesetting harness from a full build. I do not convert that disclosure into a theorem-level objection, but neither does this report certify submission-ready typesetting. The author's 843 checks and the prior referee's checks were not executed or included in the new diagnostic count. The independent implementation accompanying this report was written after inspecting the mathematical source and author diagnostics; it is an independent reimplementation, not a blinded or preregistered test.

## 3. Disposition of the controlling report

| Matter | Evidence in v26 | Disposition |
|---|---|---|
| E25.1: materially incorrect cutwidth reference | The active `references-main.tex` names A. Amarilli and B. Groz, *Cutwidth bounds via vertex partitions*, arXiv:2504.01574v2. The primary article confirms the authors and title. | **Closed.** No new priority claim is inferred from correcting the entry. |
| E25.2: absent proof ledger | `PROOF_LEDGER.md` is actually present and gives active files, statement labels, dependencies, and the two decoder conventions. | **Closed.** A navigation ledger is not a substitute for proof, but the relevant proofs are present. |
| E25.3: nominal negative controls | `diagnostics.py` computes both expectation/max operations and both controller/checkpoint operations on an actual two-by-two loss array. The cap control compares the same total cap and the same coefficient index. | **Closed at source level.** The independent tests also instantiate these witnesses. |
| Suggestion to isolate finite selection | `lem:v26-finite-selection` states and proves the reduction, including its dimension- and checkpoint-dependent constant. | Implemented. This was an expository suggestion, not an acceptance condition. |
| Principal article/companion separation and early scalar example | The direct principal proof route and early intersecting-collision example remain active. | Not reopened. The companion is not counted as though every one of its pages belonged to the principal article. |
| Significance of the mathematical advance | New separator, first-block, phase, and interval-regret results are supplied. | Reassessed independently in Sections 7–8 below; the venue judgment remains negative. |

The primary-source check for E25.1 used the [versioned article](https://arxiv.org/html/2504.01574v2). Its cutwidth objective is the maximum crossing load over prefixes, minimized over orders, not the sum objective of minimum linear arrangement. The definition in A1 uses the correct objective.

## 4. What the principal claims do, and do not, assert

The scalar classification fixes a horizon, a full-support prior, a positive detector coefficient matrix, and a compact chamber of strictly separated one-step exponents. Additive sums may collide. The constants are uniform in calibration and every integer label budget, not in all priors, arbitrary horizons, or arbitrary observation spaces.

The graph experiment fixes a finite loopless multigraph and independent scalar experiments on its edges. Visiting an edge's first endpoint acquires its first block; visiting its second completes it. Commands are exogenous and revealed only after a vertex is chosen. A vertex is one atomic input batch. The charged resource is the joint label retained at a boundary, not temporary space inside the batch, total arithmetic workspace, or the size of the read-only real program.

At a boundary, the decoder sees the label and a query descriptor identifying the visited set and tensor-product probe. It does not thereby receive discarded continuous commands or reports. There is one queried checkpoint per physical run, and all remaining raw trials of the selected probe count, including trials after a nonfailure. The sample-space construction of complete potential tapes is a coupling for the proof, not a mechanism allowing the controller to inspect future tape entries.

Two decoder models must remain distinct. The retained qualitative `thm:v25-adaptive` grants the decoder the finite order prefix as additional information. The new quantitative `thm:v26-separator` does **not** grant that prefix: at a fixed visited set it needs at most M prediction vectors, rather than a separate set of M vectors for each prefix reaching that set. Both lower bounds allow the scheduler its full revealed past. The manuscript makes this distinction explicitly. I found no silent transfer of the new quantitative constants to the stronger decoder.

The risk is an infimum over one common controller, followed by a maximum over boundaries. Independent coding randomness is averaged before a worst-tape supremum. These conventions are substantive. Neither independently optimal checkpoint encoders nor a decoder carrying uncharged continuous history would establish the stated theorem.

## 5. Audit of the inherited ingredients actually needed by v26

### 5.1 Acquisition and confluence

Sources: `core/03_transversality.tex`, especially `lem:binomial-tangent`; `text/analytic_inputs.tex`, `lem:confluent-positive`; and `text/collision_flags.tex`, `lem:newton-attainment`.

The attainable binomial product has an unnormalized tangent containing exactly n(r−1)+1 distinct monomials. The partial-product argument proves equality of the tangent span, not just a lower-dimensional inclusion. Strict mixed-moment positivity pairs this span with the future tests. Evidence normalization loses exactly one direction because the normalized product lies in the image and has constant coordinate one.

At collisions, the required initial divided-difference lists span complete Hermite families, including every lower derivative in each repeated-node cluster. An arbitrary list of isolated logarithmic derivatives would not justify this step. The text uses the complete family. The bounds on positive powers times logarithms give continuity through coincident nodes, including at t=0. Compactness and the finitely many formal-label orderings then give a uniform positive least row singular value at the common command tuple.

Full support is used to obtain positive mass on separated interior intervals in the determinant integral. A density of the latent prior is not needed and is not differentiated. Thus the prior hypotheses are not stronger in the proof than in the stated theorem.

### 5.2 Positive scaled recovery and the whole-image upper bound

Sources: `lem:leja-scales`, `lem:tame-rectangle`, and `thm:intrinsic-checkpoint`.

The leading nonzero Leja block is triangular with diagonal entries ±1 and bounded entries. Its inverse is uniformly bounded in this fixed dimension. It recovers the **scaled** Newton coordinates; it does not divide by a small scale. Columns corresponding to zero pivots are not inverted. The comparisons

`D_ell <= V_ell <= ell! D_ell`

remain valid when both sides vanish. Coincident physical exponents impose relations on attainable moment vectors, not a loss of column rank of the formal product-probe coefficient matrix. These distinctions justify the arbitrary-center recovery maps used later.

For the upper bound, each fixed-report-word moment image is rational in the commands with a positive evidence denominator. Its semialgebraic format is coefficient-uniform, and independent normalization of the factors bounds its dimension by the acquired cap. Prior integrals enter as real coefficients; semialgebraic dependence of the prior or calibration set is not required.

The rectangle covering estimate follows from bounded affine-section component counts and the classical real variation/entropy inequality. The projection-volume argument truncates the products at the dimension of the image, rather than the number of ambient sides. The treatment of small M prevents a bound of order C M from being passed off as a code with at most M labels. These points support the use of the scalar upper bound for every integer budget.

### 5.3 Causality and product compression

Sources: `thm:intrinsic-streaming`, `v25/graph_model.tex`, `prop:v25-fixed-order`, and `eq:v25-tensor-metric`.

Updates are performed in raw remaining moments. The Bayes denominator is bounded below on the posterior-mixture segment joining reachable states, so the update bound contains no reciprocal collision gap. Updating a reachable representative produces another reachable state; quantization at the next checkpoint is therefore defined on its domain. The recurrence retains all preceding errors before taking the finite-horizon maximum.

For independent edges, the tensor probe left inverse recovers each edge's raw coordinates by selecting entries with all other indices constant. It is defined on arbitrary prediction centers. The product-cover expansion keeps each individual acquired cap. It does not replace these constraints by a single total ambient cap. Empty cuts are singletons, and nonempty cuts have a positive first scale. The corresponding deterministic causal construction works with one joint label.

These are substantial ingredients. Their role is inherited in v26, however, and must not be counted anew as part of the incremental separator or phase contribution.

### 5.4 The regular box has the upper density needed for selection

Source: `v25/adaptive_proof.tex`, `lem:v25-regular-box`.

Completing the full-cap Jacobian by orthonormal kernel coordinates gives a square local map with uniformly bounded derivative and inverse. Taking the inverse image of a product box and integrating the complementary coordinates supplies both upper and lower densities on one full-cap box. The same command subset works for each prefix. Scaling a positive prefix gives the upper bound h_(e,ell)/D_(e,ell).

This is stronger than merely assigning a positive lower mass to an acquired patch. The upper bound is exactly what survives arbitrary measurable restrictions by a selected path. No zero-probability frozen command slice is substituted for actual acquisition mass.

## 6. The separator-capacity converse survives the technical review

Sources: [selection module](https://github.com/TrillionniumFoundation/theta-theory/blob/a2e5d3737085241137211f1cf21393d5bcafa1ce/papers/A1-english-v26/v26/selection.tex) and [capacity module](https://github.com/TrillionniumFoundation/theta-theory/blob/a2e5d3737085241137211f1cf21393d5bcafa1ce/papers/A1-english-v26/v26/capacity.tex).

### 6.1 The common event and its density are correctly normalized

For each edge, the event A_e requires its first command block to lie in Omega_e and its first n_e reports to be failures. Its mass is the actual integrated first-word evidence beta_e(a). The complete edge tapes are independent under the product prior, so A has mass beta(a)=product_e beta_e(a). Every completion command and report is unrestricted.

Marginalizing a completion block integrates its command law and sums its conditional report probabilities to one. Consequently the first-block mass is not multiplied by an unnecessary completion-word evidence. This is a legitimate improvement over the old all-T-failures event.

For a selected positive allocation on F, the manuscript obtains

`P(A, X_(F,ell) in U) <= [beta(a)/D_(F,ell)] product_(e selected)[h_(e,ell)/beta_e(a)] vol_k(U)`.

The cancellation is important: an edge supplying selected coordinates is bounded using its unweighted command-chart density times evidence at most one; every other edge contributes its actual event mass. Deleting completion evidences without this selected-edge density accounting would be wrong. The printed proof does not do that.

On A, an active edge has revealed exactly its first block, so its potential first-block coordinates agree with its actual posterior coordinates. Reports on completed, distinct edges do not alter this posterior under the product prior. A nonanticipatory vertex choice contributes no further latent likelihood once the revealed history is fixed. None of these claims asserts independence conditional on a visited set.

### 6.2 Node capacities apply before adaptive restriction

Fix all independent coding seeds. At a specified visited set S, the decoder has at most M query-probability centers in the original decoder model. A loss at most t places the true query vector within weighted distance sqrt(t) of one of them. Applying the affine recovery map places the selected scaled coordinates in at most M balls of radius L_(S,ell) sqrt(t).

The unconditioned restricted density therefore bounds the event that A occurs, S is visited, and its boundary loss is at most t. Intersecting with the visited-set event can only decrease its mass. No assertion about the conditional distribution given S, and no regularity of the scheduler's decision regions, is needed.

The volume factor, recovery norm and density ratios give precisely the displayed C_(S,ell)(a). Minimization over positive allocations is legitimate because the same small-loss event satisfies each bound. The additional bound by beta(a) gives the truncation at one. Nonempty cuts admit a positive allocation of total one; empty cuts have capacity one. Thus zero determinants do not cause a hidden inverse or an undefined optimization.

The treatment of coding randomness is adequate. A finite query menu allows independent decoder seeds to be fixed in advance for its finitely many possible inputs. The estimate is uniform in those seeds. They are averaged only after obtaining the bound on the sum of boundary losses; no history-correlated seed is supplied as free memory.

### 6.3 The separator, integral, and flow arguments are valid but elementary

Every realized order is a path through the Boolean lattice, and every internal separator meets that path. If all boundary losses are at most t, a visited vertex of any such separator also has loss at most t. The union bound gives

`P(A, max_j L_j <= t) <= beta(a) min_C sum_(S in C) c_S(t)`.

Layer-cake integration gives a bound on the expectation of the maximum. The manuscript then uses

`E max_j L_j <= sum_j E L_j <= (v-1) max_j E L_j`.

This explains the factor 1/(v−1) in `thm:v26-separator`. It is not permissible to replace the expectation of a maximum by the maximum of expectations without this step. The printed proof has the correct step, also after averaging seeds, and takes the infimum only over a single common controller.

Vertex splitting with linking capacity 1+sum c_S converts the separator optimization into a finite maximum-flow problem. A minimum cut cannot use such a linking arc, and the residual-cut argument works for real capacities by compactness of the feasible flow polytope. This is classical flow–cut reasoning, explicitly credited in the manuscript. Its presence is not a new graph theorem.

### 6.4 Recovery of Q has the correct inequality direction

In `cor:v26-profile-recovery`, every order encounters a cut whose profile is at least Q_G. Hence the collection of all such visited sets is a separator. For an allocation attaining that cut profile, one has

`M Q_G^(k/2) <= V_(F,ell)`,

not the reverse inequality. Combining this with `V_(F,ell)/D_(F,ell) <= product_e ell_e!` gives the stated sufficient inequality for sigma. Integrating over [0,sigma Q_G] yields the advertised lower comparison.

There are finitely many sets and allocations, their constants have uniform upper bounds for the fixed experiment, and beta(a) has a uniform positive lower bound. This gives uniformity in calibration and M. It does not give uniformity in graph size. Empty-edge graphs produce zero risk consistently with the capacity formula.

**Technical disposition:** I found no counterexample or unclosed central gap in the new separator proof under its stated decoder and acquisition model.

## 7. The phase law and the interval obstruction

Source: [phase module](https://github.com/TrillionniumFoundation/theta-theory/blob/a2e5d3737085241137211f1cf21393d5bcafa1ce/papers/A1-english-v26/v26/phases.tex), together with `text/collision_consequences.tex` and `v25/graph_consequences.tex`.

### 7.1 Analytic valuation and uniformity

For a nonidentically zero analytic node difference, its absolute value is comparable to a positive constant times theta raised to its finite integer order. A fixed Vandermonde product has the sum of the corresponding pair orders. Since the products are absolute products and there are finitely many subsets, their maximum has the smallest available order; there is no cancellation between different subset products.

Identically coincident formal labels are handled by infinite pair order, with the resulting unavailable terms omitted. The zero allocation remains available. The scalar collision-tree theorem already present in the principal article supplies this underlying contact-order mechanism. The new step is its graph-order aggregation and interval-regret consequence, not a first derivation of scalar analytic collision orders.

The bit law gives, with U=log_2(1/theta),

`b_e(theta^(2s),a(theta)) = U max_ell(ell s - eta_(e,ell)) + O(1)`.

The error is uniform in s on the stated compact interval, since the determinant comparisons are simultaneous and the number of branches is finite. The retained graph bit theorem has a uniform additive remainder for the fixed graph. Finite sums, maxima, minima, and the finite family of fixed orders preserve a bounded error. This justifies both the optimal-bit expansion and the min-over-orders, sup-over-resolutions regret expansion; the selected order may depend on theta.

The finite affine-arrangement argument establishes continuity, nonnegative integer slopes, rational breakpoints, and a deterministic optimizing order on each open cell. These are leading asymptotic phase statements. Bounded terms can decide ties at a transition, so they are not exact finite-theta integer switching thresholds.

### 7.2 The same 24-trial star really has four phases

The actual three-edge experiment has leading edge costs

`w_1(s)=7s`, `w_2(s)=max(6s,9s-3)`, `w_3(s)=s`.

An order partitions the leaves before and after the center. Isolating edge 1 costs 7s for s<=1 and 10s−3 thereafter. Isolating edge 2 costs 8s for s<=3 and 9s−3 thereafter. The other partition types are no better. Their minimum is therefore

| Resolution exponent s | Leading optimal bit coefficient W(s) |
|---|---:|
| 0<s<=1 | 7s |
| 1<=s<=3/2 | 10s−3 |
| 3/2<=s<=3 | 8s |
| s>=3 | 9s−3 |

The drop of slope from 10 to 8 is a genuine nonconvexity. It is not contradicted by convexity of each edge cost: a minimum over orders need not preserve convexity.

On [1/2,2], the maximum excess for isolating edge 1 is one, attained at s=2. For isolating edge 2 it is also one, attained at s=1. At just the two endpoints the latter maximum is instead one half. The remaining partitions are worse. Thus the best fixed deterministic order has leading regret U+O(1) on the whole interval but U/2+O(1) at the endpoints alone.

The independent implementation enumerated all 24 orders and constructed the full affine-intersection arrangement, rather than accepting agreement on a sampling grid as proof of a complete phase diagram. It reproduced the four pieces and both regret coefficients.

### 7.3 The fixed-order quantifier must not be enlarged

The regret compares `B_pi^*` and `B_G^*`. It fixes the vertex permutation across resolutions; it does not require one set of codebooks or one finite-state transducer to work at every resolution. Those are reoptimized within each bit optimum. Nor does this theorem establish an analogous obstruction for a single randomized or history-dependent scheduling rule required to serve all resolutions.

The current formulas concern deterministic fixed orders and are correct on that reading. A future abstract, summary, or response must not enlarge the conclusion to all universal adaptive policies. This is a scope clarification, not a counterexample to the statement actually proved.

## 8. Why the venue recommendation remains negative

### 8.1 The explicit lower certificate is not a sharp new minimax classification

The separator integral is an explicit lower bound once the chart-density constants, recovery norms, event masses, and determinant products are supplied. It is not shown to equal the minimax distortion, or to have a matching upper bound with those same quantitative constants. The profile-recovery corollary returns the qualitative collision profile already established in v25.

The distinction between complete paths and decoder-visible visited sets is useful. However, replacing v! trace indices by 2^v−2 internal vertices is not, by itself, a theorem of controlled adaptivity gaps over growing graphs. The graph is fixed, and the event mass, query tensor inverse, chart densities, and recovery costs may deteriorate with it. V26 states this honestly. Its honesty prevents an overclaim; it does not supply the missing breadth of consequence needed for the stronger significance case.

Similarly, dropping completion-word restrictions makes the common event less wasteful, but a larger event mass alone does not compare two complete lower bounds numerically: the associated density constants also matter. In addition, the old qualitative theorem permits a stronger decoder. A like-for-like quantitative comparison must keep the decoder model and constant choices fixed. The submission has not exhibited a fully evaluated same-model instance showing how much its complete separator certificate improves the earlier bound.

I regard this as a quantitative methodological refinement, not a demonstrated sharp characterization of optimal constants or a new graph-structural classification. The criticism concerns the significance attached to the refinement, not the correctness of its formula.

### 8.2 The new phase theorem is a finite aggregation of an existing scalar mechanism

The scalar contact-order theorem and the graph bit inversion already make the leading edge costs finite maxima of affine functions. Taking finitely many cut sums, maxima, and order minima produces a finite piecewise affine envelope. The subset recursion is the usual bottleneck dynamic programming on the subset lattice once the costs are supplied. The manuscript correctly avoids a polynomial-time claim and correctly separates these comparisons from computing arbitrary prior moments.

The substantive additional phenomenon is that optimizing the order can destroy convexity and that an interval of resolutions can impose a larger deterministic-order penalty than its endpoints. The star demonstrates both exactly. But the general phase theorem follows from finite-envelope operations, and the example reduces to a three-item partition comparison. In the present manuscript this does not provide a sufficiently deep additional structural result to change my assessment of the requested venue.

This is not an argument that elementary arguments or small examples can never have major significance. It is an assessment that the consequences established here have not been shown to have that significance. Adding theorem labels, computing more finite checks, or extending the same example from two selected resolutions to its complete envelope does not automatically establish it.

### 8.3 The complete theorem is stronger than its ingredients, but its exceptional reach remains unestablished

The principal scalar result combines facts that must be proved together: actual acquisition rather than ambient rank, complete confluent flags rather than separated nodes, a whole-image upper bound rather than one local patch, all integer budgets rather than a subsequence, and a causal filter rather than a family of unrelated checkpoint encoders. That combination deserves credit.

The relevant question is whether the full paper, with the new graph extension, establishes an advance commensurate with the requested journals. My assessment remains negative. The revision reinforces a carefully specified fixed-horizon, fixed-experiment classification. It does not yet demonstrate comparably broad consequences, a new general mechanism beyond the local-chart/covering/finite-selection framework, or a sharp structural theory for the additional scheduling problem. A different referee could assign greater weight to the conjunction; this report should not disguise that evaluative aspect as a proved mathematical defect.

I am not imposing a growing-graph theorem, a correlated-prior theorem, or an exact-constant theorem as a compulsory replacement for what the authors chose to study. Those different results were not promised. Their absence is not a gap. They illustrate why the presently demonstrated contribution should not be marketed as though it already had those forms of reach.

### 8.4 Editorial requests, not a mechanical route to acceptance

The response should acknowledge that the significance objection remains open as an editorial disagreement even though E25.1–E25.3 are closed. It should not recast another test receipt or a reorganization as resolution of that disagreement.

For a subsequent version, the most useful presentation improvement would be a single compact statement contrasting the two decoder models, the qualitative profile comparison, and the quantitative separator certificate. The fixed-order regret paragraph should explicitly say that only the order is shared across resolutions, while the predictors may be reoptimized. These would make the theorem's scope easier to assess, not strengthen its mathematical conclusion.

A worked evaluation of the full separator lower bound with chosen density and recovery constants could help establish the practical mathematical value of the quantitative refinement. This is a request for evidence supporting the claimed importance, not an assertion that a proof is missing from the current theorem, and not a guarantee of a different venue decision.

No correct theorem should be weakened, no companion erased, and no already repaired citation reopened merely to manufacture a new revision checklist.

## 9. Targeted primary-source verification

These checks were targeted, not an exhaustive literature-priority search.

**[P1]** Antoine Amarilli and Benoît Groz, *Cutwidth Bounds via Vertex Partitions*, arXiv:2504.01574v2, 3 April 2025. The [primary HTML article](https://arxiv.org/html/2504.01574v2) confirms the corrected metadata and the cutwidth objective. It is not a source for the submitted adaptive statistical theorem.

**[P2]** L. R. Ford, Jr. and D. R. Fulkerson, *Maximal Flow Through a Network*, Canadian Journal of Mathematics 8 (1956), 399–404, [doi:10.4153/CJM-1956-045-5](https://doi.org/10.4153/CJM-1956-045-5). The publisher record supports the classical attribution. The finite real-capacity argument was assessed from the complete proof printed in A1, not represented as a new theorem of the authors.

**[P3]** Yifan Zhang and Joe Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, [arXiv:2311.05116v4](https://arxiv.org/html/2311.05116v4), especially Lemma 2.18. The accessible primary treatment supports the coefficient-independent semialgebraic regularity input. It does not establish the experiment's acquired measure or its causal minimax law.

**[P4]** Georges Comte and Immanuel Halupczok, *Motivic Vitushkin invariants*, [arXiv:2206.15412v2](https://arxiv.org/html/2206.15412v2), introduction, equations (4)–(5). The cited passage explicitly recalls the classical real affine-section variations and entropy inequality. The manuscript is not using the paper's nonarchimedean results as a substitute for that real inequality.

I make no claim that these classical sources, or an unexamined branching-program or filtering theorem, already prove the submitted conjunction. The negative significance judgment is not a fabricated priority finding.

## 10. Executed independent diagnostics

The accompanying `independent_diagnostics.py` completed **4,307 explicit checks** using standard-library exact rational arithmetic. Normal Python and `python -O` produced byte-identical JSON. Tests use explicit exceptions, not removable `assert` statements. The executed script's SHA-256 is

`f5808647810a4808d90238b9217af8a754116b3ee722f01d8fe136a49a48daee`.

`DIAGNOSTICS.json` records the individual categories and concrete witnesses. The main groups are:

| Check group | What was independently evaluated |
|---|---|
| Graph bottleneck profiles | All 74 labelled simple graphs on two through four vertices at four exact weight regimes; additional arbitrary nonadditive subset costs; parallel edges and isolated vertices. |
| Separator certificates | 746 rational capacity vectors, comparing a residual-network flow implementation with exhaustive enumeration of separators, including Boolean lattices with four vertices in the underlying graph. |
| Adaptive selection arithmetic | Three genuine finite selected-path laws; node subprobabilities, separator tail inequalities, and their integrated lower bounds. |
| Collision orders | All 511 nonempty subsets of the nine actual formal future labels, at contact orders 1, 2 and 4; polynomial multiplication verifies each Vandermonde valuation rather than assuming its pair count. |
| Leja recovery scales | Exact and near collisions, monotonicity, every positive-volume index, and the factorial determinant comparison. |
| Full star phase and regret | All 24 orders and all affine-intersection cells, including the nonconvex slope change and the interval-versus-endpoint distinction. |
| Integer budgets and quantifiers | Capped factorization, 960 integer-budget inversion witnesses, same-total-cap negative control, and actual expectation/max and infimum/max operations. |
| Report evidence | An actual positive retention detector with uniform acquisition commands integrated analytically; every completion word through length five is retained and summed. |

The report-evidence witness deserves specificity. Let the prior be uniform on [0,1], with cells `k_0=1/2+t/4` and `k_1=1/2−t/4`, and independent commands uniform on `[1/4,3/4]^2`. Restrict the first command to

`Omega=[1/4,3/8] x [5/8,3/4]`

and require its failure report. Integrating the command variables gives the latent subprobability polynomial `1/32+3t/512`, with mass **35/1024** and posterior mean **18/35**. The three integrated completion-report likelihoods are `1/2`, `1/4+t/8`, and `1/4−t/8`. Summing all completion words returns the same first-block mass and first-moment numerator, whereas requiring m further failures gives only `35/(1024*2^m)`. This independently checks the evidence-marginalization mechanism in the actual command/report model. It does not assert that this chosen rectangle is the theorem's uniform regular chart.

The diagnostic loss array `(1,0),(0,1)` gives `E max=1`, `max E=1/2`, `inf max=1`, and `max inf=0`. The individual-cap witness keeps total cap three and changes the actual common coefficient A_3 from 1/4 to 1/16. These are genuine negative controls, not comparisons of unrelated constants or differently sized arrays.

Finite diagnostics cannot prove the uniform inverse chart for arbitrary full-support priors, the continuum small-ball estimates, the semialgebraic covering theorem, or the minimax optimum over all causal filters. They do not certify the complete companion, typesetting, or a journal decision. The count is a reproducibility record, not a measure of mathematical significance.

## 11. Final disposition and handoff

The new first-block subprobability, visited-set separator converse, finite subset recursion, analytic graph phase law, and deterministic interval-regret consequence survive this review under their stated hypotheses. The inherited scalar route supplies the needed collision-uniform acquisition, global geometry, and causal update estimates without a newly identified central gap.

The concrete v25 bibliography, ledger, and negative-control objections are closed. There is no new demonstrated fatal counterexample in this report. Conversely, no formal proof certification, full native build, exhaustive companion audit, or exhaustive priority search is claimed.

**My recommendation remains reject at the requested four-journal level, for the significance assessment in Section 8.** That judgment should not be softened into an acceptance prediction, nor rewritten as a false theorem the author must repair. A later revision should identify its genuinely new mathematical advance against this pinned submission and address its significance directly. Preserving the valid mathematics and its explicit scope is preferable to adding unsupported generality or restarting already closed corrections.
