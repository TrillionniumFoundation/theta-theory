# Response to the controlling independent referee report — twelfth revision

**Paper:** General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction  
**Author:** Qian Qi  
**Date:** 23 September 2026  
**Controlling report:** `8e44610a9826b799f190639cec80c0435f14487c`, reviewing v10 head `4507bd5b6e61206d0d82c9f52fcbe279585ce1c7`  
**Starting revision:** v11 referee-ready head `b5875ec059e24b328321dcca6d60065cbc3da643`

The remote branch survey for this revision found the tenth-revision report to remain the newest GTF-I report. It did not find an eleventh-revision review. We therefore continue the mathematical response to E10.1–E10.7 from the published v11 manuscript; we do not attribute invented objections or an invented new report to a referee. The earlier report and both earlier manuscript branches remain unchanged.

The central development in this revision is a connection between exact causal task completion, infinite-horizon resource comparison, and approximation of actual microscopic observations. We preserve every predecessor mathematical body and introduce no change of task family merely to claim that a historical target is solved. The statements below describe what the new proofs establish and what they do not establish.

## E10.1 — Resource-aware comparison as a mathematical invariant

V11's explicit product-register comparison and complete-state fusion remain in the canonical article, with their full proofs. This revision adds two connections that are not contained in a list of separate finite results.

First, `thm:v12-transport` proves a coherent infinite-time implementation theorem: one simulator works on all prefixes; its persistent widths multiply the consumer widths, and its separately charged seed combines with the consumer's seed. For a summable criterion the risk error is the weighted sum of the actual marked prefix errors. Prefix restrictions are restrictions of one machine, not independently selected approximating channels at different horizons.

Second, `thm:v12-certificate` joins the risk comparison to the new exact task-cover theorem. A finite restart family has either zero common-encoder minimax excess or a positive gap given by its loss table. A two-sided cost-one comparison whose risk and benchmark errors are less than a quarter of this gap classifies the original exact width profile by one threshold. A costed one-sided comparison gives the corresponding KS cover conclusion, and exactness eliminates the extra public seed without pretending that positive-excess private and public risks coincide.

The public seed is part of the joint comparison interface whenever it is readable by the output consumer. Section `sec:v12-infinite` makes this convention explicit. A simulator that outputs Y = W XOR U can have the same marginal (Y,W) law as an uninformative target while its public seed U reveals the mark jointly with Y. Thus marginal comparison with the simulator seed discarded cannot justify a seed-aware feedback comparison. The new transport theorem uses the joint condition, and the physical channels satisfy it with no additional seed. The finite diagnostic suite includes this counterexample.

No converse asserting the existence of a prescribed-cost simulator from support inequalities is claimed. The certificate theorem consumes an independently verified comparison; it does not manufacture an inverse randomization theorem.

## E10.2 — Beyond a fixed finite horizon

The dominated finite-horizon theorem and the singular displayed-covariate theorem from v10–v11 remain intact. The new `thm:v12-infinite` removes the fixed-horizon restriction for summable criteria.

The hypotheses are stated on each finite-prefix loss effect, with no common dominating measure on the full infinite path. The private policy space is the countable product of the prefix-compatible weak-star policy blocks. The proof supplies simultaneous measurable representatives, norm continuity of the infinite risk map by a uniform tail estimate, norm continuity of barycentres, compact private and fixed-finite-seed bodies, compact convex ideal-public bodies, and attained minimax duality. It does not simply take a scalar limit of finite-horizon minimax values.

The Bernoulli path example shows the distinction: all finite prefixes are dominated, but the complete path family has uncountably many mutually singular typical sets and no common sigma-finite dominating measure. `cor:v12-seed` proves that a fixed-accuracy public mixture uses at most N(J,h)+1 private designs, with private storage cost (N(J,h)+1)S_t at every time. That number does not grow with the truncation horizon. Exact ideal public randomness is still a separately priced signature.

`cor:v12-geometric` gives the explicit discounted coupling bound e/(1-beta+beta e) under a uniform conditional step coupling. The physical application uses a different unconditional union bound; it does not assume that an L2 bound on the initial density remains true for posteriors.

The theorem is for summable criteria and coherent dominated prefixes. Arbitrary average cost and arbitrary filtered strategic-measure closure are not asserted. This is an extension of the mathematical scope, not a relabeling of standard Borel carriers as a general compactness theorem.

## E10.3 — Exact task-specific causal compression on the actual support

`thm:v12-support` goes beyond v11's checkpoint covers and strictly positive causal Brier signatures. It permits zero next-report probabilities and finite tasks with multiple Bayes-optimal actions.

A cell must have a common optimal action for each task. A cover is causally closed when all actually supported successors of a cell under one control and report lie in one next cell. The cells may overlap. This is essential: unsupported branches have no target signature, and compatible covers need not admit a coarsest feasible partition.

The proof identifies the positive supports of a randomized retained message. Zero excess forces compatibility. A positive output of one common update row contains all its supported successor histories, which proves closure. Conversely the cover supplies a deterministic causal machine. Conditioning on an independent public seed proves the same equivalence for arbitrary public signatures. This answers the exact zero-excess question for the declared restart family at every checkpoint, not just one checkpoint at a time.

`cor:v12-gap` then gives a positive lower bound alpha gamma for every randomized design when no such cover exists. The proof averages finite time-indexed deterministic tables only to prove a lower bound; their index is not supplied as free public memory. The Brier version gives alpha delta^2/2. Completion under all actual marked continuation-event predictions recovers the universal quotient. A locally finite infinite-tree corollary characterizes exact infinite machines by their finite-prefix cover feasibility.

The source includes both a repeated-report example and a constant-second-report example with identical checkpoint task minima but different causal feasibility, plus a nontransitive-support example. These explicitly distinguish task-specific causal width from a universal quotient or a sequence of independently optimal checkpoint partitions.

The task-cover theorem concerns restart tasks with fixed open-loop histories and the explicitly defined conditional loss tables. It does not claim that this solves optimal lossy memory synthesis for every endogenous task-dependent controlled game.

## E10.4 — Historical operator memory and actual microscopic approximation

This revision develops the historical common-domain memory and microscopic generator direction rather than substituting another finite positive hidden-state model.

`thm:v12-memory` assumes a contraction generator L and a finite resolved space in D(L) intersect D(L*). It proves that the orthogonal block D = QLQ on QD(L) is a generator, by a bounded off-diagonal perturbation and a dissipativity argument. It derives the forced Volterra equation for every initial observable, the exact block-resolvent inverse, a right-half-plane inverse bound, and the skew-adjoint memory sign. The adjoint-domain condition is written explicitly; finite rank alone is insufficient. The proof retains the unresolved initial component. `prop:v12-stability` gives an explicit cosh error bound and includes a separate reconstruction residual for the full observable. Accurate resolved coordinates alone are not passed off as accurate physical observations.

Using v11's collision-compatible microscopic graph core, `thm:v12-galerkin` constructs nested finite graph-core spaces for the genuine hard-sphere Koopman generator and proves strong resolvent and time-uniform-on-compacts orbit approximation. Its proof includes the resolvent core argument and an Euler/Gamma estimate, not a bare invocation of convergence.

`thm:v12-physical` then converts the full physical observable error into marked total variation error uniformly in every finite-register width profile, every admissible feedback design and every independent seed signature. The initial density family is uniformly L2 bounded. The proof integrates the first report-mismatch contribution under the initial law and sums over controls, avoiding an unjustified posterior-density bound. Coupling the same actual mark is essential. The infinite-time risk error tends to zero by finite-prefix approximation and the criterion tail. `cor:v12-physical-duality` verifies the effect hypotheses for compact L1-continuous density families.

**Historical content now discharged in this category:** an explicit common domain and orthogonal generator for finite-rank microscopic memory; its forcing and quantitative reconstruction; a graph-core Galerkin limit of the full microscopic observable; and a resource-uniform marked decision limit which genuinely consumes the comparison theorem. The microscopic Hilbert space is infinite dimensional and the Liouville generator is unbounded. Finite rank is the resolved projection, not a replacement of the physical dynamics by a finite Markov chain.

**Historical content not identified with this result:** the A4 Sinai multiplier algebra and left-strip renewal/transmission-zero estimates, the C2 general form-bundle/connection and optional-projection limit, and the B4 nonlinear kinetic action-sublevel BBGKY corrector and Boltzmann--Grad limit. The inherited B2 factorial/recollision and B3 observability inputs required for that stronger kinetic closure are not proved by L2 approximation. These targets remain recorded as separate tasks; the manuscript does not delete them or mark them complete. E10.4 has a new rigorous microscopic operator/decision consumer, but not a claim of full historical kinetic closure.

## E10.5 — Theorem-level antecedents and priority

The source comparison has been updated, including primary literature revised in 2026. In particular, Widder–Zimmer–Schilling, arXiv:2503.20457v6, Section 2 and its semigroup discussion, and Widder–Schilling, arXiv:2604.20453v2, Section II, already treat the finite-rank bounded-perturbation and domain issues behind Mori projection. We explicitly credit that mechanism. The new article does not claim to originate orthogonal dynamics, Volterra well-posedness, graph-core semigroup convergence, compact product spaces, finite mixture approximation, or compatible covers of partial machines.

The proposed contribution is the connection to the common-encoder resource invariant: support-aware zero faces and positive risk witnesses; infinite-time coherent costed comparison; and a full microscopic observation approximation uniform over all retained widths, combined with exact-profile certification. The original finite-prefix team, common-information and weighted-automata comparison from v11 remains part of the audit, with the distinction between inspecting original statements and certifying global priority.

**Still unresolved:** the full Norberg filtered-experiment original was not obtained. Publisher and repository/library routes did not produce a readable original full text in this session. We do not infer absence of a theorem from an abstract, and no proof-level priority exclusion against that paper is claimed. The classical partial-machine literature also requires a dedicated original-source priority audit before treating a compatible-cover formulation by itself as novel. `LITERATURE_COMPARISON.md` records the precise boundary instead of using novelty rhetoric to conceal it.

## E10.6 — A2 and the eleven-component graph

All eleven historical components remain in `PIPELINE_GRAPH.json`. Their inherited statuses are retained; the new memory, Galerkin and physical-comparison edges are added with exact labels. A new operator-domain consumer does not change an entire component into a closed historical target.

The graph continues to distinguish the older A2 acquisition adapter from the independently developed primary algebraic-geometric chain. The latter observation remains explicitly frozen at v127, commit `d6c730f8caff71ddbc8208c0bd00cb90138de85a`; it is not advertised as a fresh audit of every A2 branch. Neither source order nor the name “Foundations” is substituted for a theorem implication.

`HISTORY_AUDIT.md` records the inspected round-seventeen files and section ranges across A1–D1, the complete pinned GTF source ancestry, and the additional A4/C2 operator-domain issues. Earlier claimed closure paragraphs are not imported as premises of the new results merely because they exist in the repository.

## E10.7 — Preserve the mathematics while making the connection explicit

No existing repository file is edited or deleted. The canonical v12 manuscript includes every v11 canonical mathematical body. The complete development additionally includes the v11 introduction and all earlier inherited bodies and introductions. Every v11 companion label is checked for preservation. The new introduction foregrounds comparison, support completion, the infinite-time risk body, and the physical decision limit; the certification theorem states their mathematical connection.

The main text is a theorem–proof article in the existing AMS style. Source manifests, finite-test counts, branch identities and status declarations are kept in the response/evidence files rather than used as substitutes for mathematical arguments.

## Technical comments 11.1–11.8

**11.1:** Finite-prefix product domination, the singular displayed-covariate model, and infinite summable criteria are separately stated. “Standard Borel” is never used to erase the analytic hypotheses.

**11.2:** Finite q and an ideal seed are distinct. The finite-mixture price is explicit at every time; the simulator seed belongs to the joint comparison if readable by the consumer.

**11.3:** The KS multiplier remains in the finite and coherent infinite theorems and in the one-sided exact-cover certificate. Complete-state fusion is retained with its additional hypothesis.

**11.4:** Task-specific width is now a causally closed cover on the actual support. The universal marked quotient is recovered only by the stated prediction completion.

**11.5:** The corrected median-index sentence from v11 is retained by importing that source unchanged.

**11.6:** B4's already proved finite Nisio theorem, microscopic linear generator/memory results, and historical infinite-dimensional nonlinear kinetic targets are distinct ledger entries.

**11.7:** The pipeline script checks identities, declared edge labels and component inventory. It is not a semantic theorem verifier.

**11.8:** The receipt records only executed tests, compilation, hashes, input preservation and source identity. Finite tests include independently enumerated covers and deterministic machines, randomized risk inequalities, seed/mark controls, block memory identities and approximation formulas. None certifies an analytic proof or a journal decision.

## Reconsideration requested

We submit the new statements and complete proofs for independent examination. The manuscript now has a support-aware exact resource characterization connected to infinite-horizon comparison and a genuine unbounded microscopic observation limit. The remaining full kinetic and source-priority questions are explicitly located, without removing the historical targets or converting them into claims already proved.
