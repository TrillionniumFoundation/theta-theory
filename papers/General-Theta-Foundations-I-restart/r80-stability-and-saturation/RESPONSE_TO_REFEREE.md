# Response to the controlling referee report — General Theta Foundations I, R80

## Identity, baseline, and interpretation of the report

This is an author revision of **General Theta Foundations I**. Its original research identity, causal and experimental resource questions, and objective of consideration by Annals of Mathematics, Acta Mathematica, Inventiones Mathematicae, or the Journal of the American Mathematical Society remain in force. We answer the contribution objection by developing the current mathematical chain, while preserving the earlier valid results and their proofs. Neither a longer manuscript nor a successful build constitutes a favorable assessment of mathematical significance.

The immediate complete mathematical baseline is R79 source commit `90cae2f5aca243b39d3a2194a4d6e0696671a101`, source subtree `582c4a664cb571c63927940ab7ef08be869cf10b`, at `papers/General-Theta-Foundations-I-restart/r79-robust-instrument-frontier`. Its publication commit is `a1b6a0be3b97b2cbcfc8c5cf457ec738bb33a5d2`. The present revision continues those sources. The refreshed audit authenticated all 806 R79 source files and 23 publication files against the corresponding Git trees and verified that the publication preserves the source subtree. R78 is a valid ancestor, not the latest complete baseline.

The controlling report remains the R65 report at commit `358481b21ceeeedb1205ebd30f86982e32a2cb04`, original path `GENERAL_THETA_FOUNDATIONS_I_RESTART_R65_BOUNDARY_MEMORY_EXTERNAL_REFEREE_REPORT_R65.md`, Git blob `d1ff9c5662390156ee212c82b173e86a21180e84`, SHA-256 `8c7d45d762736009fda667621fdf5019fa934f5f45f39364c747f837e6d7343c`. It assessed R65 source `0469eb4f852eeea953cb3725d4b34dfdd2bf9d36` and publication `ee79ca9114f8009d62c056d07381b766645e3fc4`. It did not assess R66–R80. R66–R79 already supplied substantial responses; the fifty items below are not represented as fifty previously untouched errors.

The fresh all-ref census agrees across two GitHub enumeration routes on 1309 branch refs and 875 distinct heads. Its authenticated history extension covers 2715 ancestor commits and 7273 distinct scoped text blobs. The R79 branch changes and the independent A2DYN addition were inspected against the retained authenticated traversal. No later applicable independent report was found. Empty review branches, source transfers, old publications, pipeline audits, and internal author diagnostics do not supersede R65. The precise distinction between fresh remote retrieval, retained authenticated archive traversal, content indexing, and mathematical proof checking is recorded in `provenance/r80-audit`.

## What is added mathematically

The central new result is an exact arithmetic classification of finite stochastic implementation for **every finite number of imperfect-search locations**, accompanied by explicit memory bounds obtained solely from the primitive data. It addresses the gap between convergence of finite-memory values and exact attainment at some finite memory. The general nonreset quantum cost frontier inherited from R79 remains the framework: its fixed-budget attainment and exact certificates support this distinction, while its same-label regularization gives a primitive perturbation modulus of order `sqrt(eta)+zeta`, uniformly over the memory budget. R80 also proves that this exponent is optimal. These are connected resource questions with distinct scopes.

For the new classification, fix any finite `n>=2`, matching failure probabilities `0<r_i<1`, and arbitrary positive command costs `c_i`. In hidden model `i`, only command `i` can succeed. The hidden model stays fixed, one failure report is observed, and success stops the experiment. Set `tau_i=c_i/(1-r_i)`, `B=sum_i tau_i`, and `H=sum_i 1/(-log r_i)`. Theorem `thm:r80-finite-search-saturation` proves

`there exists finite M with V_M=V_hist  iff  log(r_i)/log(r_j) is rational for every i,j`.

If the condition fails, every finite budget has an attained strict gap, although its value decreases to the history optimum. The necessity proof covers all autonomous stochastic command and update kernels. It partitions commands into rational commensurability classes; after finitely many cross-class ties, every optimal word has the same projected class suffix. The ratios of positive class frequencies are irrational when there is more than one class. A finite stochastic controller producing one prescribed class suffix would force that suffix to be ultimately periodic through a deterministic recurrence on its positive label supports, a contradiction. This proof includes partially commensurate families whose command words still have infinitely many within-class ties.

In the commensurate case, relative logarithmic scores belong to bounded lattice cosets. Classical consistent-priority words therefore have finite realizations, and a command-conditioned update after the first failure realizes an optimal mixture of at most `n` words from one counted pure initial label. The exact one-label value is `V_1=B`. The greedy rule, interior preparation saddle, finite consistent-priority mixture, and common-power cycles are classical search ingredients, explicitly attributed and proved in full. The rational direction is a classical structural consequence together with counted initialization; the all-stochastic obstruction and quantitative resource conclusions are identified separately.

The primitive-data bounds do not presuppose a known optimal prior. With `c_-=min_i c_i`, `c_+=max_i c_i`, and `r_-=min_i r_i`, define

`T_0=ceil(2B/c_-), g=(c_-/2) r_-^T_0, T_1=ceil(2B^2/(c_- g)), K=c_+ T_1+B, delta=g/(2K)`.

Lemma `lem:r80-finite-search-prior-cap` proves that every least-favorable prior has each coordinate at least `delta`. A deletion-and-completion construction proves that estimate. With `C=tau_max/(delta tau_min)`, `A=C max(C,1/r_-)`, and `kappa=exp(-1/H)`, Theorem `thm:r80-finite-search-resource-bounds` gives

`0 <= V_M-V_hist <= B A kappa^floor(M/n)` for every `M>=n`.

The constants apply to arbitrary positive command costs, in both saturating and nonsaturating cases. This is an upper approximation rate, not a matched rate for the positive gap. For rational primitive failures and costs, `cor:r80-finite-search-effective` decides saturation by positive rational collinearity of signed prime-exponent vectors. In the affirmative case it computes a rational common base `r_i=t^h_i`; an exact rational comparison chooses `J` with `t^(-J)>=C`. Then `N_0=max(J,max_i h_i)` and `M_0=1+n(2N_0+1)^(n-1)` give a sufficient budget. The inherited finite-budget algebraic procedure at that cap computes the history value and an attaining algebraic controller, without evaluating an unknown logarithmic prior. Neither the cap nor the computational complexity is claimed optimal.

The second central result, `thm:r80-sharp-modulus`, proves that the square-root exponent in the general primitive cost modulus cannot be improved on its stated class. Two scalar hidden models, two commands, two live labels, unit costs, and a common one-row bound already give

`V_2(epsilon) = (1+sqrt(65))/2 + c_0 sqrt(epsilon) + o(sqrt(epsilon))`,

with an explicit positive algebraic constant `c_0`. The proof covers every permitted stochastic two-label controller, establishes the rigidity of the zero-perturbation optimum, derives a coercive lower comparison, and supplies a matching realizing family. The primitive discrepancy is exactly `epsilon`; the costs do not change. The one-label value is smooth in the same parameter. Thus this is a sharp obstruction for the optimized memory frontier, not a loss of feasibility or a divergent one-command waiting time.

The complete two-location refinement, including `thm:r80-arithmetic-saturation`, its sharper normalized approximation constants, and its smaller sufficient rational label cap, is retained intact in the current supplement before the historical technical body. The main article contains the sharpness section and the general finite-search section. The special refinement is not silently deleted or presented as an independent general theorem.

The declared inventory contains 252 inherited numbered declarations and 15 newly added numbered declarations, for 267 in total. Those counts include lemmas, examples, and explicit restatements of classical ingredients; they do not mean 267 new theorems or 15 independent priority claims. The diagnostic inventory contains 29 inherited suites and three added suites, for 32. Their actual execution status belongs to the exact-source receipts. Neither the general search classification nor the sharp modulus solves the original arbitrary-memory noisy-qubit squared-sign risk frontier or the independent Theta construction goals.

## Responses to the ten major requests

### R65-17.1 — Identify the mathematical center and distinguish theorem layers

**Issue: organization and breadth.** The mathematical center now follows the strongest proved current statement: an exact obstruction-and-realization classification of finite stochastic saturation for arbitrary finite imperfect-search families, together with explicit primitive-data bounds. It distinguishes approximate value convergence from exact finite-memory realizability. The optimality of the general primitive stability exponent supplies a second structural conclusion, supported by the already proved uniform upper theorem.

The original boundary-attainment, unique-decision residual, quantum obstruction, and positive finite-memory results remain intact. Arbitrary-experiment causal-transfer statements, the general declared-interface cost theorem, known-reset normal forms, exact special-model values, and local spectral geometry retain separate hypotheses. The general finite-search path is `lem:r80-finite-search-saddle` and `lem:r80-projected-word-rigidity` → `thm:r80-finite-search-saturation`, followed by the explicit prior bound, memory approximation, and effective cap. It uses inherited fixed-budget attainment and history convergence. The parallel general cost path is `thm:r79-quantum-frontier` → `thm:r79-label-restart` → `thm:r79-frontier-stability` → `thm:r80-sharp-modulus`. Historical geometric and timing routes remain traceable complementary results. The theorem and dependency maps give the reading order.

**Disposition:** the organization follows proved mathematical development rather than preserving R65's then-current headline indefinitely. The broader significance assessment remains for an independent reader.

### R65-17.2 — Compare with Moore/Myhill–Nerode and classical predecessors

**Issue: priority and the boundary of novelty.** We retain the explicit distinction between the classical residual theorem for deterministic output machines and the paper's operational derivation of a task-specific forced output function through minimax zero slack. Its wordwise uniqueness hypothesis removes stochastic advantage only at that scope. The resulting task/dictionary quotient is not the complete predictive quotient.

The same priority discipline is applied to the new search analysis for arbitrary finite `n`. The index rule is attributed to Blackwell as reported by Matula. Clarkson–Lin–Glazebrook's Proposition 3 and Theorem 10 in their arXiv version supply the interior/equalizer and finite mixture statements reproduced in `lem:r80-finite-search-saddle`; their Section 6.1 and Appendix C credit the classical common-power cycles. The commensurate sufficiency direction is therefore presented as a classical consequence with counted initialization. The added obstruction treats all stochastic controllers and partially commensurate classes, while the quantitative prior bound removes the unknown prior from the explicit memory estimates. Bui–Lidbetter–Lin's optimal pure infinite sequence question remains distinct from finite implementation. Reachable supports, supported potentials, algebraic elimination, and the earlier certificate theorems are likewise not recounted as new discoveries.

**Disposition:** inherited attribution closures are preserved and the new contribution is delimited. Targeted primary-source comparison is not an exhaustive clearance of all mathematical priority.

### R65-17.3 — Develop the robust tied case

**Issue: necessity, sufficiency, and stochastic realization.** The inherited weighted-face, invariant-polytope, and stopping-rigidity criteria remain valid on their declared interfaces. R79's fixed-budget common-controller certificate already permits tied command and update choices and modelwise quantum witnesses, but fixed-budget decidability alone does not decide eventual saturation at some finite budget.

R80 now supplies such a necessity-and-sufficiency statement for every finite `n` in the displayed imperfect-search family, with arbitrary positive command costs. The proof does not assume pairwise irrationality or uniqueness of each optimal command. It partitions the logarithmic increments into rational commensurability classes. Ties across different classes occur only finitely often, so all optimal words share one deterministic class suffix. Several classes have irrational ratios of positive frequencies. Finite stochastic memory would force that suffix to be ultimately periodic, even while commands within each class remain randomized, giving the necessary obstruction. With one class, the classical consistent-priority words have finite lattice-state realizations; the optimal mixture of at most `n` words is implemented from one counted pure start.

**Locations:** `lem:r80-finite-search-saddle`, `lem:r80-projected-word-rigidity`, `thm:r80-finite-search-saturation`, and the inherited `eq:r79-robust-budget-quantifiers`. The two-location proof and sharper normalized bounds remain in the supplement.

**Disposition:** this is a complete finite-saturation classification for the stated family, including stochastic ties. Arbitrary tied terminal loss and optional commitment remain separate open problems.

### R65-17.4 — Broaden the herald model

**Issue: physical assumptions and sufficient information.** The active general cost theorem already permits several commands and reports, state- and model-dependent success, arbitrary finite-dimensional completely positive failure maps, nonreset posteriors, changing reachable supports, and a hidden model fixed during execution. Its proof does not assume model-independent failure words. This general framework is retained, including the internal attribution of its earlier certificate ingredients.

R80 strengthens the resulting uniform stability theorem by proving a matching exponent obstruction on an actual feasible physical subfamily. The exact saturation classification permits arbitrary finite model and command number, model-dependent failures, and arbitrary positive costs; it does not replace the general nonreset framework by that special family. Its all-failure word law is justified by conditioning on the actual commanded prefix, whose failure likelihood is common across private routes, and not by importing the old model-independent herald assumption.

The remaining general hypotheses stay explicit: finite time-homogeneous interface, globally legal commands, robustness over all initial density matrices, positive conditional mean costs, a declared observation port, and compulsory stopping at success. A classical label restart does not reset the physical state. Optional commitment is not inferred.

**Disposition:** the current structural chain has broader physical scope than the R65 herald model; exact search formulas remain special-model results.

### R65-17.5 — Obtain a sharp general-M noisy-qubit risk law

**Issue: the particular unresolved quantitative risk problem.** The requested general-M squared-sign noisy-qubit risk law remains open. The exact one-/two-label qubit formulas, fixed-budget strict gaps, distinguishing-depth certificates, and prefix upper bounds are retained. The unrestricted-decoder approximation lower/upper rate gap also remains open.

R80 answers two different quantitative questions. It proves the exact square-root asymptotic of the two-label cost value under primitive perturbation, against all stochastic controllers, establishing the optimal exponent in the general uniform stability theorem. For arbitrary finite search families with positive costs, it gives the explicit upper gap `B A kappa^floor(M/n)` and proves strictness at every finite budget whenever logarithmic commensurability fails. That search upper rate is not claimed to be matched from below, and irrationality alone is not converted into an explicit positive numerical lower gap. Neither result is renamed as a solution of the original qubit-risk objective.

**Locations:** `thm:r80-sharp-modulus`, `eq:r80-sharp-asymptotic`, `thm:r80-finite-search-resource-bounds`; retained `thm:two-label-quantum`, `prop:boundary-depth-gap`, and `thm:r77-unrestricted-qubit`. The sharper two-location normalized upper estimate remains `eq:r80-memory-exponential` in the supplement.

**Disposition:** the general stability exponent is now sharp; the specifically requested arbitrary-M qubit-risk law is not closed.

### R65-17.6 — Establish an external consequence

**Issue: mathematical significance and a natural application.** R80 relates the resource framework to the classical imperfect-search game. Its additional question is whether an optimal law can actually be implemented with finite autonomous classical storage, and the proof settles that question for every finite number of locations, including partially commensurate instances, under the stated observation and initialization rules. Explicit prior bounds, memory approximation, and a rational-data synthesis cap make the resource consequences concrete. The general same-memory perturbation theorem, now with an optimal exponent, supplies a separate control-theoretic consequence extending beyond the original qubit example.

This does not claim that the search game, its greedy solution, or its saddle structure is new. Nor does it claim that a previously unknown natural quantum protocol has been solved. The original qubit remains a valid exact example and obstruction, but is not the sole support for the current resource theorem. The mathematical importance of the new rigidity, sharpness, and implementation results requires independent assessment; repository checks and author diagnostics cannot supply that assessment.

**Disposition:** a concrete connection and exact resource consequence are supplied. No external expert endorsement or top-four editorial conclusion is claimed.

### R65-17.7 — Strengthen effective and computational content

**Issue: decidability, synthesis, and input size.** Fixed-budget exact algebraic synthesis and its encoded-input assumptions are inherited. The new effective saturation corollary addresses an additional unbounded-budget decision question for arbitrary finite search families with rational failures and costs: the existence of any finite exact realization is decided by whether all signed prime-exponent vectors lie on one positive rational ray. This is not an unbounded search over possible controllers.

For arbitrary positive rational command costs in the affirmative case, the proof computes rational `t` and positive integers `h_i` with `r_i=t^h_i`. The explicit prior floor determines `C`, an exact rational comparison finds `J` with `t^(-J)>=C`, and the proof gives `M_0=1+n(2 max(J,max_i h_i)+1)^(n-1)`. The inherited fixed-budget procedure at that cap computes an attaining algebraic controller and the history value. It needs no exact transcendental prior oracle. The cap is not asserted minimal, factorization is not asserted polynomial-time, and general quantifier elimination is not reported as a practical computation already performed. The smaller normalized two-location cap is preserved as a refinement in the supplement.

**Locations:** `lem:r80-finite-search-prior-cap`, `cor:r80-finite-search-effective`, `thm:r79-quantum-frontier`; supplement `cor:r80-effective-saturation` and `eq:r80-rational-label-cap`.

**Disposition:** exact eventual-saturation decidability and a sufficient synthesis cap are proved for a stated rational family. General minimal-memory complexity remains open.

### R65-17.8 — Read back the actual hosted run

**Issue: execution evidence.** The historical run `38861581555` was freshly read back as `completed` with conclusion `success`, at head SHA `ee79ca9114f8009d62c056d07381b766645e3fc4`. The raw readback is retained in `provenance/r80-audit/R65_WORKFLOW_READBACK.json`. This closes the requested historical status check. The report's observation that the run was queued at its cutoff remains an accurate historical observation.

Fresh source-specific and publication-specific queries for R79 returned zero runs. The R65 success is not evidence of an R79 or R80 hosted run. Current native builds and any current hosted execution must be read from their own exact-source receipts in the final publication records. An attempted or failed build is recorded as such and cannot be promoted to a passing result by a later source edit.

**Disposition:** the specific R65 hosted-status request is closed at its correct SHA; current execution status remains separately source-bound.

### R65-17.9 — Reduce the editorial dependency surface

**Issue: readable proof organization and archival preservation.** The general finite-search theorem has a self-contained route through the classical saddle, projected support rigidity, partial-commensurability obstruction, counted realization, explicit prior floor, and quantitative/effective consequences. The support-safe fixed-memory frontier, same-label regularization, uniform stability, and sharpness theorem form the complementary general cost path. Their theorem-level dependencies are stated explicitly, allowing a reader to inspect the new center without retracing every historical revision.

The main article contains the sharpness and general finite-search sections. The complete two-location section, with its original proof and sharper normalized constants, is retained intact in the current supplement before the historical technical body. The independent companion retains its distinct mathematical role. Complete prior source, prior response, and historical derivations are preserved in traceable inputs and maps. Archival material is distinguished from the current main/supplement proof path. The new proofs increase the mathematical material; we do not claim that mere relocation or a shorter reading guide solves a contribution objection. Any journal packet must retain all premises and technical arguments actually used by its main results.

**Disposition:** the dependency route is made explicit while historical retention remains complete. The theorem map, dependency map, and preservation map are part of the review entry.

### R65-17.10 — Keep every resource convention explicit

**Issue: definitions and quantifiers.** The finite-memory values count live classical labels and include the prescribed pure initial label. Event stopping and state stopping retain their distinct total-label conventions. Decoder values, program descriptions, arithmetic working storage, protected physical state, and the mathematical information in an unrestricted history remain separate resources.

The new saturation realization explicitly counts its mixture branch and position labels and uses command-conditioned updates; it does not assume a randomized initializer or persistent private coin. The approximation count includes the initial row, every retained prefix position, and the fallback row. The sharpness lower bound ranges over all six stochastic command/update parameters of a two-label controller and hence is not a bound for an artificially deterministic subclass. Offline priors and modelwise operator witnesses are never runtime information supplied to the controller.

**Disposition:** the new theorems preserve the existing resource conventions and make the implementation counts explicit.

## Responses to the forty technical comments

### R65-18.1 — Fixed decoder dictionary

The original boundary-memory theorem retains its fixed dictionary `C`. The current mandatory-success cost problem has its own terminal convention and does not establish convexity or density for an optimized hard decoder width. The dictionary-dependent residual theorem remains in the preserved mathematical packet with its original quantifiers.

### R65-18.2 — Model-independent word probabilities

This remains a hypothesis of the old herald theorem. The general quantum cost analysis uses actual model-dependent completely positive maps. In the new search proof, the planned command law is model-independent because, conditional on a command prefix, the physical failure likelihood is identical for all private routes yielding that prefix. The physical failure probabilities themselves are explicitly model-dependent; the two notions are not conflated.

### R65-18.3 — First compulsory call

The first call remains counted in `1/p` and in the zero-prefix term of each total-cost series. The search formula starts at `t=0`; its first-call lower bound charges the first wrong command. The explicit prefix/fallback controller performs and pays for all `T` prefix calls before entering the fallback.

### R65-18.4 — Separately performed audit

Any separately executed audit continues to contribute to the resource budget. The new search and sharpness families stop at the primitive success event and do not introduce a free terminal audit or unreported measurement. Nothing in the cost-only specialization removes paid audit costs from the earlier discrimination and boundary-risk statements.

### R65-18.5 — Offline least-favorable witnesses

The least-favorable prior in the search proof and the modelwise operator witnesses in the general certificate are offline objects. One executing controller is common to all `n` fixed hidden models. The explicit primitive-data prior floor provides a computable sufficient label cap; in the rational saturating case, fixed-budget algebraic synthesis can construct an attaining controller without an exact evaluation of the logarithmic prior. No model label or witness is observed at runtime.

### R65-18.6 — Wordwise uniqueness hypothesis

The old stochastic determinization theorem retains uniqueness word by word under one attaining least-favorable measure. R80 does not infer universal determinization from it. The new obstruction uses its separately proved characterization of every Bayes-optimal word and the finite-support lemma for the projected commensurability-class suffix. It allows continuing ties and randomization within a class. The commensurate case explicitly permits a nontrivial mixture of tied words.

### R65-18.7 — Positive word masses

Zero expected slack is promoted to pointwise zero only where the relevant word has positive mass. All finite failure prefixes in the new search family have strictly positive physical likelihood, which is explicitly used to compare support and to exclude least-favorable priors with a zero coordinate. The general unregularized quantum certificate instead restricts to actually reachable invariant supports and does not declare inaccessible histories positive.

### R65-18.8 — The residual right congruence

The task-specific residual congruence of the forced decision function, the full predictive quotient, and the modelwise reachable quantum support remain distinct. The new finite-support recurrence is a proof about deterministic projected class suffixes of stochastic controllers, even with stochastic commands within each class; it is not presented as a replacement definition of predictive state.

### R65-18.9 — Live labels and stopping totals

The pure initial live label is included in every `M`. Under event stopping no extra persistent terminal label is introduced by the cost model; a state-stopped realization uses its separately charged disjoint terminal label. The search mixture and approximation constructions give their full counted live-label totals explicitly, rather than reporting only tail or cycle states.

### R65-18.10 — Unreachable rows

Unreachable rows may be completed without changing the realized process, but are not used to inflate or misstate a minimal reached-machine claim. Fixed-budget classes may be padded by unused labels to prove monotonicity. An inaccessible row or physical corner may be improper; the sharpness proof explicitly handles the discontinuous change from an inaccessible dark label to a reachable one, and the unregularized cost certificate remains support-restricted.

### R65-18.11 — Positive successors only

The inherited deterministic subcontroller construction selects only positive-probability successors. The new suffix lemma likewise uses sets of labels with positive probability and unions of the corresponding update supports. Zero-weight transitions cannot generate a reached state or a contradiction, and zero-weight mixture branches are never selected.

### R65-18.12 — Robust ties and randomization

The robust tied example and its warning remain. Known-reset routing determinization does not purify command rows or extend automatically to hidden models. An optimal search law is obtained from at most `n` consistent-priority words, and the proof constructs its finite implementation with counted labels in the commensurate case. The projected necessity argument allows arbitrary stochastic command choices inside each commensurability class. The sharpness lower bound includes every stochastic command and update row.

### R65-18.13 — Distinguishing depth and effectivity

The existence of finite distinguishing depth `H_M` is not upgraded to computability from arbitrary real input data. The new eventual-saturation decision procedure has a different, explicit input model: finitely many positive rational failure probabilities and costs, with exact signed prime exponents. Its positive-ray test and explicit cap are finite procedures. The general fixed-budget algebraic procedure continues to require effectively encoded algebraic primitives.

### R65-18.14 — Positivity versus a sharp frontier

The old distinguishing-depth gap remains a positive gap, not a sharp risk-memory asymptotic. R80's sharpness claim concerns the explicitly specified primitive perturbation problem at two labels and proves an exact square-root asymptotic. Its search memory approximation is only an upper estimate. No sharp arbitrary-M noisy-qubit risk claim is made.

### R65-18.15 — Irrational rotation

The original rotating-qubit proof retains the rational-algebraic-integer obstruction at `6/5`. The new rational search example uses a separate exact argument: a rational ratio `log(2)/log(3)` would imply equality of a positive power of 2 and a positive power of 3. Numerical samples of either orbit do not serve as irrationality proofs.

### R65-18.16 — Nonzero cosines

The original exclusion of zero cosine retains its root-of-unity implication and remains in the preserved proof. The search saturation result uses no trigonometric nonvanishing premise and does not displace that argument. The two arithmetic obstructions have distinct roles.

### R65-18.17 — Positive polarization

The uncertain-polarization uniqueness theorem continues to require a strictly positive lower polarization. At zero polarization the stated uniqueness can fail, and the revision introduces no endpoint extension. New scalar search and cost-perturbation parameters do not change that original hypothesis.

### R65-18.18 — Pure periodicity and uniqueness

The exact unitary decision-orbit result retains uniqueness at every orbit time. The new stochastic support lemma has a different explicit premise: after a fixed finite time, one prescribed **class** suffix is emitted almost surely. Its application follows from the full search equality characterization and the finite number of cross-class tied levels. It does not presume command uniqueness or prohibit continuing ties inside classes. The two-location command-suffix refinement remains in the supplement.

### R65-18.19 — Contraction and a strict decision gap

The contraction theorem still requires a common limiting state and a strict limiting action gap. Same-label regularization is a controller intervention used to obtain bounded cost witnesses; it is not a physical contraction theorem. The new arithmetic realization criterion does not weaken the earlier contraction hypotheses.

### R65-18.20 — Contraction alone is insufficient

The depolarizing counterexample remains intact. Value stability and exact-memory stability are separate: the new search result gives arbitrarily close finite-memory values together with strict nonattainment at every finite budget whenever the failure logarithms occupy more than one rational commensurability class. This reinforces the distinction without claiming that contraction alone produces an exact finite decision machine.

### R65-18.21 — Matrix and state conventions

The original two-state calculation retains its row/source/destination convention. The new sharpness proof separately defines both command probabilities and all four command-conditioned cross-label update probabilities, with label 1 the initial label. Its two-state cost formula treats an inaccessible second state before dividing by a determinant. The search construction specifies which command-conditioned failure row stores the branch.

### R65-18.22 — Randomized terminal decisions

The original exact two-label risk theorem continues to optimize decoder expectations throughout `[-1,1]`, including randomized terminal decisions. Neither a mandatory-success cost example nor deterministic greedy command words reduce that earlier admissible decoder class. The objectives and optimization variables remain distinct.

### R65-18.23 — Endpoints and degeneracy

The original `x=0` and `c=±1` endpoints are retained. The new sharpness theorem treats its zero-perturbation support boundary explicitly. The search theorem assumes `0<r_i<1` for every command and strictly positive costs; it does not include perfect detection, zero success, or zero-cost endpoints by continuity. Improper one-label rows with zero success mass in a model and zero-weight initialization classes are handled before division.

### R65-18.24 — Scope of the qubit threshold

The threshold `q alpha>1/3` remains attached only to the displayed `c=3/5` qubit family. Neither the uniform cost modulus nor the new search arithmetic criterion is claimed to generalize that threshold. The current theorem map separates these special-model conclusions.

### R65-18.25 — Intermediate timing frontier

The intermediate phase-type timing frontier remains a distinct unresolved problem. Exact two-label qubit risk, known-reset cost formulas, the hidden-model golden-ratio frontier, the square-root perturbation asymptotic, and search saturation each have their own objective. None silently closes the intermediate timing problem.

### R65-18.26 — Exact input representation

The unary rational algorithm retains exact primitive entries and fixed dictionary losses. Compact-model algebraic synthesis likewise assumes encoded algebraic coefficients and its stated semialgebraic parameter set. The new rational prime-factor test uses exact integers; finite-precision log comparisons are not a substitute for it, and arbitrary real parameters are not declared algorithmically decidable.

### R65-18.27 — Quantitative constants

Herald-rate dependence remains explicit in the old precision bounds. General cost stability displays its positive-cost and one-row feasibility margins. The arbitrary-cost finite-search theorem gives `T_0`, `g`, `T_1`, `K`, `delta`, `C`, `A`, and `kappa` entirely from the primitive data, including model number, cost bounds, and failure probabilities. The sharper normalized two-location constants remain in the supplement. No uniform bound is asserted at excluded zero-success or zero-cost endpoints, and the sufficient constants are not claimed sharp.

### R65-18.28 — Additional program inputs

Primitive, dictionary, model-description, and numerical encoding lengths remain additional program resources. Counting finite live labels does not count these lengths. The rational saturation test presupposes access to exact rational data; the computed finite label cap is not a bound on its total bit complexity or the description length of an algebraic sampling implementation.

### R65-18.29 — Dense arithmetic representation

The earlier arithmetic upper bound continues to use dense `d²`-coordinate superoperators unless a separate structural assumption is stated. Scalar examples and reset-only certificate reductions do not reduce the arithmetic cost of arbitrary nonreset quantum instruments. The dimension dependence is preserved in the inherited resource statements.

### R65-18.30 — Program table, work space, and coins

The output program table, transient arithmetic storage, and persistent controller labels remain distinct. Fresh coins can sample a command or an update but cannot store a branch for free. The counted mixture construction stores that branch in disjoint tail labels. Exact algebraic probabilities are mathematical synthesis outputs; they do not establish a finite-bit exact random sampling implementation without a separate computational model.

### R65-18.31 — Meaning of local verification

Native compilation verifies assembly, references, and execution of the build pipeline at the recorded source. Finite exact algebraic checks and floating diagnostics test specified calculations. Separately read AI author arguments are internal checks. None of these is a formal proof certificate, a human specialist report, or an editorial decision. The proof audit identifies which evidence actually supports each claim.

### R65-18.32 — Historical queued hosted run

The original queued-at-cutoff observation is preserved. The fresh historical readback now records `completed/success` for run `38861581555` at exactly `ee79ca9114f8009d62c056d07381b766645e3fc4`. This is not reported as a hosted success for R79, R80, or another commit. Current publication receipts identify their own source and execution status.

### R65-18.33 — Main and supplement together

The current main and technical supplement remain a paired native submission, with cross-document references and compiled theorem locations checked together. The independent companion has its own source/build role. Historical PDFs are not substituted for current native output, and the review entry identifies which files form the current mathematical packet.

### R65-18.34 — Preservation is not re-review

Complete retention of R64 and subsequent sources is provenance, not a new assessment of those proofs. The immediate R79 mathematical files, earlier derivations, prior responses, and independent companion remain traceable through the preservation map and authenticated inputs. Previously accepted scoped conclusions are inherited without inventing a new rejection or new independent endorsement.

### R65-18.35 — Scope of the historical audit

The new census goes beyond branch-name inspection: two independent all-ref enumerations agree, changed relevant commits and trees are inspected, retained raw commit and source identities are authenticated, and the scoped historical text archive is traversed with a minimal new delta. The records distinguish fresh remote bytes, authenticated retained bytes, lexical indexing, and proof review. The 7273-blob content audit is not represented as a new mathematical proof audit of every historical theorem.

### R65-18.36 — Bounded scores and expected duration

The performed-law theorem continues to compare bounded scores. Current expected-cost results use actual nonnegative cost series, positive-cost floors, properness, supported potentials, and justified fallback constructions. The search proof uses truncated costs and monotone convergence for risk-set closure. No bound for unbounded remaining duration is inferred merely from total variation of stopped records.

### R65-18.37 — Hard budgets and convexity

Fixed-dictionary convexity is not extended to optimized hard width or fixed controller memory. Fixed-M attainment uses compact controller parameters and lower semicontinuity. The search separation argument is carried out only in the unrestricted word-law risk set. Its mixture of at most `n` consistent-priority words is then implemented with explicitly counted labels, or truncated with `2+n(T-1)<=nT` labels for approximation. Mixing is not assumed free inside an arbitrary hard-M class.

### R65-18.38 — Witness dimensions versus runtime states

Sparse physical dual atoms, operator potentials, Hilbert dimension, decoder values, and live controller labels retain separate meanings. The support subsets in the new obstruction are proof objects used to establish periodicity; they are not extra runtime registers furnished to the controller. Certificate size does not itself establish a memory upper or lower bound.

### R65-18.39 — Protected physical state and observation interface

The protected qubit remains part of the experiment rather than observer-owned quantum memory. The controller accesses only declared outcomes and its sampled command, not the hidden model, unreported tomography, or a cost value that the interface does not reveal. The new scalar examples add no physical observation port. Label regularization changes a classical update without a quantum reset.

### R65-18.40 — Open scope after the new results

General same-boundary finite-memory density for the original bounded-risk problem, arbitrary robust tied terminal-loss classification, optional commitment, the original general-M noisy-qubit risk law, the unmatched unrestricted-decoder approximation rates, intermediate timing, common unknown-model predictive quotients, and the independent Theta construction goals remain explicitly distinguished. R80 closes finite stochastic saturation for the displayed imperfect-search family with arbitrary finite `n` and positive costs, supplies its stated upper/effective bounds, and resolves the sharp exponent question for the general cost modulus. It does not classify saturation for arbitrary noncommuting instruments or provide a matching lower search-gap rate. An open question is removed only where a theorem with matching scope has now been proved.

## Historical obligations retained beyond the fifty R65 items

The original-paper v94/R62 report, the restart R59 round-three report, and the R64 report were freshly fetched at their original report SHAs and byte-authenticated. Their complete earlier responses and numbered crosswalks remain in the preserved R79 response and historical source chain. This current response does not make a later limited report supersede an older unanswered issue on a different part of the paper.

The original two-stage reset variational and dual principles, rank-constrained discrimination envelope, optimal attainment and realization, finite communication/no-message distinctions, spectral geometry, and local rigidity results remain inherited at their stated scope. Arbitrary-pair closed formulas, arbitrary-horizon classification, and global changing-support geometry are not inferred. The earlier request for independent human specialist assessment of priority is not fulfilled by author literature searches or internal AI checks; no such endorsement is claimed.

The R59 actual-history causal-transfer construction, paid resource accounting, mixed-stratum profile, and fixed-law predictive quotient remain preserved. An intrinsic primitive criterion replacing all supplied certificates and a general common predictive quotient for unknown models are not claimed. R64's boundary full-history attainment, fixed-dictionary duality, sparse witnesses, Bellman slack, hard-width counterexamples, and timing endpoint results retain their separate hypotheses. The new total-cost stability and finite-saturation results do not settle their remaining bounded-risk or intermediate-timing questions.

The controlling R65 report's top-four rejection was a significance judgment about R65. It remains an authentic historical judgment; it is neither erased nor treated as an assessment of these new proofs. We submit the strengthened mathematics for a fresh independent reading while retaining the original research objective. The source, proof/dependency maps, exact preservation records, native outputs, execution receipts, and this response make that next review concrete without claiming its outcome.
