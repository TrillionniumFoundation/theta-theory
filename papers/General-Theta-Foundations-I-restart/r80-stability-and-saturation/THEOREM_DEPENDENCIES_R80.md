# R80 theorem dependencies, hypotheses and claim boundaries

This is the author dependency addendum for General Theta Foundations I. The actual paired native index has **267 statement labels**: all **252 inherited R79 labels** and **15 additions** (10 main, 5 supplement). Supporting lemmas and corollaries are included; this is not a novelty count. The independent R58 companion keeps its separate source and numbering.

## Reading the map

Direct logical prerequisites are actual premises of the proof. Inherited mechanisms identify related retained arguments or a construction reproduced in full. Definition labels and internal facts are separate. Automatically extracted references in the structured record are syntactic evidence and do not replace this author analysis.

The actual compiled index and every new proof source are hashed in `provenance/R80_PROOF_DEPENDENCIES.json`. The final Git identity is supplied by the source/publication handshake. Current native kind is authoritative: a label beginning `thm:` may name a compiled corollary and is not counted again as an independent theorem.

## 1. An exact square-root singularity at fixed memory

**Native locator:** main, theorem 5.1, page 20; `thm:r80-sharp-modulus` in `sections/57-sharp-stability.tex`.

**Hypotheses.** Two scalar fixed hidden models with success probabilities (1-epsilon,0) and (0,1/4) for commands a,b, respectively; one failure report and deterministic unit paid call costs. Mandatory stopping at success; every command always legal; sampled command observed; prescribed pure initial live label counted; no free clock, history or persistent seed. Every stochastic controller with at most two live labels is included through all six independent command/update probabilities. Two scalar fixed hidden models; two commands; one failure report; deterministic unit call costs; success stopping; prescribed pure initial label; all stochastic two-live-label controllers; epsilon tends to zero from above.

**Conclusion.** V2(0)=(1+sqrt(65))/2 and V2(epsilon)=V2(0)+c0 sqrt(epsilon)+o(sqrt(epsilon)), with explicit positive c0. This proves optimality of the inherited general instrument-modulus exponent 1/2 at M=2.

**Direct logical prerequisites.** `lem:r80-boundary-rigidity`, `lem:r80-boundary-coercivity`, `thm:r79-dark-feasibility`, `thm:r79-quantum-frontier`, `thm:r79-frontier-stability`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Full six-parameter controller classification at epsilon=0; coercivity at its unique effective optimizer; exact activated-trap cost identity; compactness and lower semicontinuity; first-order lower limit over every optimizer; explicit matching controller. No restriction of the converse to a proposed ansatz.

**Classical ingredients and priority boundary.** Two-state substochastic Bellman equations and positive-potential policy improvement; Compactness and lower semicontinuity of nonnegative total cost; Taylor expansion and the arithmetic-geometric mean inequality. New exact model-specific singular asymptotic, with a general consequence: sharpness of the inherited uniform primitive exponent at fixed memory.

**Limits.** No formula for V2 at positive epsilon, no optimal global constant in the inherited upper bound, and no sharpness assertion under a strictly positive success floor.

## 2. The unique effective optimal program at zero perturbation

**Native locator:** main, lemma 5.2, page 21; `lem:r80-boundary-rigidity` in `sections/57-sharp-stability.tex`.

**Hypotheses.** Two scalar fixed hidden models with success probabilities (1-epsilon,0) and (0,1/4) for commands a,b, respectively; one failure report and deterministic unit paid call costs. Mandatory stopping at success; every command always legal; sampled command observed; prescribed pure initial live label counted; no free clock, history or persistent seed. Every stochastic controller with at most two live labels is included through all six independent command/update probabilities. The same two-model family at epsilon=0; every six-parameter stochastic two-label controller.

**Conclusion.** The unique effective optimizer has r=r0, s=gamma=delta=0, alpha=1; xi is irrelevant. Opposite row ordering r<=s has the attained strictly larger minimum 2(sqrt(19)-2).

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Elementary two-state Bellman equations; routing comparison in the model where a-failure has positive probability; a displayed positive-polynomial identity for one row orientation; explicit monotone derivative elimination for the other; inaccessible dark-label cases are handled directly.

**Classical ingredients and priority boundary.** Two-state substochastic Bellman equations and positive-potential policy improvement; Compactness and lower semicontinuity of nonnegative total cost; Taylor expansion and the arithmetic-geometric mean inequality. New exact optimizer rigidity and opposite-orientation classification for the displayed two-model instrument.

**Limits.** Specific to the displayed beta=1/4 baseline; no general unique-optimizer or controller-purification assertion.

## 3. Coercivity near the boundary optimizer

**Native locator:** main, lemma 5.3, page 23; `lem:r80-boundary-coercivity` in `sections/57-sharp-stability.tex`.

**Hypotheses.** Two scalar fixed hidden models with success probabilities (1-epsilon,0) and (0,1/4) for commands a,b, respectively; one failure report and deterministic unit paid call costs. Mandatory stopping at success; every command always legal; sampled command observed; prescribed pure initial live label counted; no free clock, history or persistent seed. Every stochastic controller with at most two live labels is included through all six independent command/update probabilities. All six-parameter controllers near the baseline effective optimizer with robust baseline excess cost at most Delta.

**Conclusion.** s+delta=O(Delta), gamma=O(Delta(s+delta)), and r-r0=O(Delta), uniformly in the otherwise unrestricted a-failure update parameters.

**Direct logical prerequisites.** `lem:r80-boundary-rigidity`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Positive coefficients of the exact polynomial identity yield (gamma+(s+delta)^2)/(s+delta+gamma) control; monotonicity and nonzero derivative of f give the row estimate.

**Classical ingredients and priority boundary.** Two-state substochastic Bellman equations and positive-potential policy improvement; Compactness and lower semicontinuity of nonnegative total cost; Taylor expansion and the arithmetic-geometric mean inequality. New local coercivity estimate at the explicitly classified singular optimizer; load-bearing for global-controller sharpness.

**Limits.** Local and family-specific; constants exist on a fixed neighborhood and are not claimed globally uniform over instruments.

## 4. A common one-label fallback

**Native locator:** main, lemma 6.1, page 26; `lem:r80-finite-search-one-label` in `sections/59-finite-search-saturation.tex`.

**Hypotheses.** An arbitrary finite number n >= 2 of fixed hidden scalar models and commands; command i succeeds only in model i, with failure probability 0 < r_i < 1. Each command i has deterministic positive model-independent cost c_i; one failure report; success is mandatory stopping. The initial label is prescribed and pure and counts toward memory; autonomous stochastic command/update kernels are allowed; no free clock, persistent seed, history, or model input.

**Conclusion.** The exact one-label robust value is B=sum_i c_i/(1-r_i), attained by p_i proportional to 1/(1-r_i), with all model costs equal to B.

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Write x_i=p_i(1-r_i). The worst cost is sum_i tau_i*x_i/min_i x_i; its lower bound is sum_i tau_i and equality requires equal success masses.

**Classical ingredients and priority boundary.** Geometric waiting-time identity; Positive weighted-average bound. Classical elementary optimal row calculation, reproduced for the primitive-data fallback.

**Limits.** The displayed imperfect-search family and one-label controllers only; not a general instrument closed form.

## 5. The finite-search saddle

**Native locator:** main, lemma 6.2, page 27; `lem:r80-finite-search-saddle` in `sections/59-finite-search-saturation.tex`.

**Hypotheses.** An arbitrary finite number n >= 2 of fixed hidden scalar models and commands; command i succeeds only in model i, with failure probability 0 < r_i < 1. Each command i has deterministic positive model-independent cost c_i; one failure report; success is mandatory stopping. The initial label is prescribed and pure and counts toward memory; autonomous stochastic command/update kernels are allowed; no free clock, persistent seed, history, or model input.

**Conclusion.** Interior-prior Bayes-optimal words are precisely greedy list merges; they have uniform geometric tails and frequencies 1/(H*u_i). The robust value is attained at an interior least-favourable prior and equalized risk vector, realized by a mixture of at most n consistent-priority words.

**Direct logical prerequisites.** `lem:r80-finite-search-one-label`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Adjacent exchanges prove the greedy characterization. Minimum-score increments keep logarithmic spread bounded, giving tails and frequencies. Cylinderwise compactness and separation give a saddle; deleting absent-prior commands followed by finite-prefix fallback proves interiority. A single descending lambda_i/pi_i tie priority minimizes every linear functional, so the greedy risk set lies in the convex hull of consistent orders; affine elimination gives at most n words.

**Classical ingredients and priority boundary.** Adjacent-exchange search ordering; Compactness of laws on a finite-alphabet product; Finite-dimensional convex separation; Affine-dependence reduction. Classical search and robust-game structure, with full self-contained proof; not claimed new.

**Limits.** Only interior priors and the displayed scalar search family; a mixture of infinite words is not yet a finite-memory implementation.

## 6. A deterministic class suffix from finite stochastic memory

**Native locator:** main, lemma 6.3, page 28; `lem:r80-projected-word-rigidity` in `sections/59-finite-search-saturation.tex`.

**Hypotheses.** An arbitrary finite number n >= 2 of fixed hidden scalar models and commands; command i succeeds only in model i, with failure probability 0 < r_i < 1. Each command i has deterministic positive model-independent cost c_i; one failure report; success is mandatory stopping. The initial label is prescribed and pure and counts toward memory; autonomous stochastic command/update kernels are allowed; no free clock, persistent seed, history, or model input. More generally, any finite autonomous stochastic controller with a finite command partition and a single failure report; after a fixed time its planned class output is deterministic almost surely.

**Conclusion.** The prescribed class suffix is ultimately periodic, even when labels randomize arbitrarily among commands within each class.

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** The positive-probability label support evolves by one deterministic union map on finitely many nonempty subsets. A prescribed output class is determined by this support. A repeated support therefore forces a periodic output suffix.

**Classical ingredients and priority boundary.** Finite deterministic-state eventual periodicity; Support propagation for stochastic kernels. Elementary finite-support realization rigidity used to treat all stochastic controllers, not a deterministic-controller-only obstruction.

**Limits.** Requires an autonomous finite controller and a prescribed class suffix; does not assert that arbitrary stochastic output words are periodic.

## 7. Finite-search saturation for any finite number of locations

**Native locator:** main, theorem 6.4, page 29; `thm:r80-finite-search-saturation` in `sections/59-finite-search-saturation.tex`.

**Hypotheses.** An arbitrary finite number n >= 2 of fixed hidden scalar models and commands; command i succeeds only in model i, with failure probability 0 < r_i < 1. Each command i has deterministic positive model-independent cost c_i; one failure report; success is mandatory stopping. The initial label is prescribed and pure and counts toward memory; autonomous stochastic command/update kernels are allowed; no free clock, persistent seed, history, or model input.

**Conclusion.** Some finite counted memory attains the history optimum if and only if every ratio log(r_i)/log(r_j) is rational. Otherwise every finite-budget optimum has a strict gap while the values converge to the history optimum. In the commensurable case at most n ultimately periodic consistent-priority words suffice.

**Direct logical prerequisites.** `lem:r80-finite-search-saddle`, `lem:r80-projected-word-rigidity`, `thm:r79-quantum-frontier`, `cor:r79-history-limit`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Partition log-failure increments into rational commensurability classes. Distinct classes share only finitely many tied items, leaving a deterministic class suffix of every greedy word. Class frequency ratios are irrational between distinct classes, contradicting projected-output periodicity for any finite stochastic controller. When all increments share one lattice, bounded relative logarithmic states give finite deterministic orbits. A counted pure initial label implements the optimal finite word mixture after its first sampled command.

**Classical ingredients and priority boundary.** Classical common-power eventual search cycles; Rational commensurability of finite real lists; Positive limiting frequencies; Finite-state realization of ultimately periodic words. Counted-stochastic-memory arithmetic classification: the all-stochastic necessity through partial commensurability classes is the added resource obstruction. Common-power eventual cycles and sufficiency ingredients are classical search consequences explicitly credited.

**Limits.** Applies only to the displayed finite scalar imperfect-search family. It does not classify arbitrary instruments, prove a numerical lower gap bound, or claim classical common-power cycles as new.

## 8. An explicit least-favourable prior bound

**Native locator:** main, lemma 6.5, page 30; `lem:r80-finite-search-prior-cap` in `sections/59-finite-search-saturation.tex`.

**Hypotheses.** An arbitrary finite number n >= 2 of fixed hidden scalar models and commands; command i succeeds only in model i, with failure probability 0 < r_i < 1. Each command i has deterministic positive model-independent cost c_i; one failure report; success is mandatory stopping. The initial label is prescribed and pure and counts toward memory; autonomous stochastic command/update kernels are allowed; no free clock, persistent seed, history, or model input.

**Conclusion.** Every least-favourable prior has all coordinates at least delta=g/(2K), where T0=ceil(2B/c_min), g=(c_min/2)*r_min^T0, T1=ceil(2B^2/(c_min*g)), and K=c_max*T1+B.

**Direct logical prerequisites.** `lem:r80-finite-search-one-label`, `lem:r80-finite-search-saddle`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** A robust optimum tries every model command by T0 with planned probability at least one half. Deleting all copies of one command lowers every other model cost by at least g. Truncate an optimal restricted-task law at T1 and then apply fallback B; this yields cost <=V-g/2 on other models and <=K on the deleted model. Least-favourability forces the coordinate bound.

**Classical ingredients and priority boundary.** Markov inequality; Deletion of commands with unchanged other-model survival; Finite-prefix completion with a proper fallback. Explicit primitive-data quantitative refinement of the classical interior-prior conclusion.

**Limits.** Constants are sufficient and can be very large or small; no sharpness or practical-complexity claim.

## 9. An explicit exponential memory approximation

**Native locator:** main, theorem 6.6, page 30; `thm:r80-finite-search-resource-bounds` in `sections/59-finite-search-saturation.tex`.

**Hypotheses.** An arbitrary finite number n >= 2 of fixed hidden scalar models and commands; command i succeeds only in model i, with failure probability 0 < r_i < 1. Each command i has deterministic positive model-independent cost c_i; one failure report; success is mandatory stopping. The initial label is prescribed and pure and counts toward memory; autonomous stochastic command/update kernels are allowed; no free clock, persistent seed, history, or model input.

**Conclusion.** For M >= n, 0 <= V_M-V_hist <= B*A*kappa^floor(M/n), with C=tau_max/(delta*tau_min), A=C*max(C,1/r_min), and kappa=exp(-1/H).

**Direct logical prerequisites.** `lem:r80-finite-search-one-label`, `lem:r80-finite-search-saddle`, `lem:r80-finite-search-prior-cap`, `thm:r80-finite-search-saturation`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** The quantitative prior floor bounds all initial log-score offsets. Greedy survival is bounded by A*kappa^T uniformly in models and tie orders. Truncate at most n optimal consistent words after T commands and use common fallback; a counted initializer, disjoint continuation chains and shared fallback require 2+n(T-1)<=nT labels.

**Classical ingredients and priority boundary.** Geometric survival tail estimates; Finite-word truncation; Counted implementation of a finite mixture. Constructive primitive-data convergence rate with explicit dependence on model number and counted memory.

**Limits.** An upper approximation bound for this family, not a matching lower rate; constants are not sharp. It applies in both saturating and nonsaturating regimes.

## 10. A decidable rational criterion and a sufficient label cap

**Native locator:** main, corollary 6.7, page 31; `cor:r80-finite-search-effective` in `sections/59-finite-search-saturation.tex`.

**Hypotheses.** An arbitrary finite number n >= 2 of fixed hidden scalar models and commands; command i succeeds only in model i, with failure probability 0 < r_i < 1. Each command i has deterministic positive model-independent cost c_i; one failure report; success is mandatory stopping. The initial label is prescribed and pure and counts toward memory; autonomous stochastic command/update kernels are allowed; no free clock, persistent seed, history, or model input. All failure probabilities r_i and deterministic costs c_i are rational.

**Conclusion.** Finite saturation is decidable by positive rational collinearity of signed prime exponent vectors. In the saturating case compute r_i=t^h_i, choose J with t^(-J)>=tau_max/(delta*tau_min), and put N0=max(J,max h_i), N=(2N0+1)^(n-1), M0=1+nN. Then V_M0=V_hist and the history value is algebraic and computable through the inherited finite-M real-algebraic formula.

**Direct logical prerequisites.** `thm:r80-finite-search-saturation`, `lem:r80-finite-search-prior-cap`, `thm:r80-finite-search-resource-bounds`, `thm:r79-quantum-frontier`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Prime factorization converts rational log relations into exact integer power identities. A primitive exponent direction yields a rational common base. The explicit prior bound gives a computable lattice strip; each relative-score coordinate has at most 2*N0+1 values and each priority controller at most N states. Counted initialization adds one state to at most n disjoint tails. The inherited attained finite-budget semialgebraic frontier then computes the history optimum.

**Classical ingredients and priority boundary.** Unique prime factorization; Bezout identity for primitive integer vectors; Counting lattice-coset points in bounded intervals; Real-algebraic quantifier elimination. Effective arithmetic and finite-memory certificate built from the classification and the new explicit prior bound; no claim that prime factorization or common-power cycles are new.

**Limits.** Effectivity only, with no practical runtime bound for factorization, the label cap, or quantifier elimination; no analogous algebraicity assertion in the nonsaturating regime.

## 11. Greedy words and an attained interior preparation saddle

**Native locator:** supplement, lemma S1.1, page 2; `lem:r80-search-saddle` in `sections/58-arithmetic-saturation.tex`.

**Hypotheses.** Two scalar fixed hidden models, two commands, one failure report, compulsory success stopping, positive failure factors r,s in (0,1). Prescribed pure initial live label; autonomous stochastic command and update rows; no extra history, clock, or persistent seed. Arbitrary positive deterministic command costs ca, cb. Interior prior for the Bayesian ordering; no prior given to robust controller.

**Conclusion.** The classical index rule characterizes every Bayes-optimal word; a robust optimum and interior least-favorable prior exist; two consistent extreme tie rules suffice, with equalized model risks.

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Adjacent exchanges plus monotone prefix limits; bounded logarithmic phase; closed convex upward risk set from cylinder compactness; separation; strict known-model baseline; absolute summability of tie exchanges.

**Classical ingredients and priority boundary.** Classical search ordering and convex risk separation as explicitly attributed.. Classical two-location search/saddle specialization, reproduced self-contained; no novelty claim.

**Limits.** A mixture of finitely many infinite words is not yet a finite autonomous implementation.

## 12. Deterministic tails of finite stochastic controllers

**Native locator:** supplement, lemma S1.2, page 4; `lem:r80-finite-word-rigidity` in `sections/58-arithmetic-saturation.tex`.

**Hypotheses.** Finite fixed controller with stochastic command/update rows and one repeated failure report. One prescribed command suffix occurs almost surely after some fixed finite time.

**Conclusion.** The prescribed suffix is ultimately periodic.

**Direct logical prerequisites.** None listed in this category.

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Every reachable label after the suffix begins has the same pure command row; finite support subsets evolve deterministically and must recur.

**Classical ingredients and priority boundary.** Classical search ordering and convex risk separation as explicitly attributed.. Elementary finite-state support argument, explicitly proved; no claim to invent deterministic automata periodicity.

**Limits.** Does not assert periodicity of general randomized finite-controller output laws.

## 13. Arithmetic dichotomy and exponentially accurate finite memory

**Native locator:** supplement, theorem S1.3, page 4; `thm:r80-arithmetic-saturation` in `sections/58-arithmetic-saturation.tex`.

**Hypotheses.** Two scalar fixed hidden models, two commands, one failure report, compulsory success stopping, positive failure factors r,s in (0,1). Prescribed pure initial live label; autonomous stochastic command and update rows; no extra history, clock, or persistent seed. Arbitrary positive command costs for the exact finite-saturation dichotomy. Normalized ca=1-r, cb=1-s only for the displayed quantitative approximation constants.

**Conclusion.** V1=ca/(1-r)+cb/(1-s); some finite budget attains unrestricted history value iff log(r)/log(s) is rational. In the irrational case every attained finite-budget gap is strict. The normalized family has explicit exponential-in-M upper error.

**Direct logical prerequisites.** `lem:r80-search-saddle`, `lem:r80-finite-word-rigidity`, `thm:r79-quantum-frontier`, `cor:r79-history-limit`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Irrationality gives at most one tied pair and a common irrational-frequency suffix, impossible for finite stochastic supports. Rationality gives finite phase orbits and a counted pure-start mixture. Two finite prefixes plus one fallback use at most 2T labels.

**Classical ingredients and priority boundary.** Classical search ordering and convex risk separation as explicitly attributed.. Counted stochastic implementation theorem built on attributed classical search ordering and finite-state reasoning; not a first cyclic/acyclic search claim.

**Limits.** Exact classification for this family; no minimal rational saturation count, matching lower convergence rate, or general quantum saturation criterion.

## 14. An effective saturation test for rational primitives

**Native locator:** supplement, corollary S1.4, page 6; `cor:r80-effective-saturation` in `sections/58-arithmetic-saturation.tex`.

**Hypotheses.** Two scalar fixed hidden models, two commands, one failure report, compulsory success stopping, positive failure factors r,s in (0,1). Prescribed pure initial live label; autonomous stochastic command and update rows; no extra history, clock, or persistent seed. r,s rational; arbitrary positive command costs for deciding existence of finite saturation. Normalized costs for the explicit M0 cap and exact algebraic history-value computation.

**Conclusion.** Finite saturation is equivalent to positive rational proportionality of signed prime-exponent vectors. In the normalized affirmative case exact rational comparisons construct M0=1+2(max(J,h)+max(J,k)+1) attaining the history value; fixed-budget algebraic synthesis computes it.

**Direct logical prerequisites.** `thm:r80-arithmetic-saturation`, `thm:r79-quantum-frontier`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Prime exponents give common rational base t with r=t^h,s=t^k. The least-favorable phase strip contains at most N lattice-coset points; two N-label tails and one initializer give the cap.

**Classical ingredients and priority boundary.** Classical search ordering and convex risk separation as explicitly attributed.. Effective resource corollary of the realization theorem and unique factorization.

**Limits.** No optimal count or efficient factorization/elimination claim; no exact irrational history-value algorithm is asserted.

## 15. A rational primitive with no finite saturation

**Native locator:** supplement, example S1.5, page 6; `ex:r80-rational-nonsaturation` in `sections/58-arithmetic-saturation.tex`.

**Hypotheses.** Two scalar fixed hidden models, two commands, one failure report, compulsory success stopping, positive failure factors r,s in (0,1). Prescribed pure initial live label; autonomous stochastic command and update rows; no extra history, clock, or persistent seed. r=1/2,s=1/3; ca=1/2,cb=2/3.

**Conclusion.** Rational instrument data have V1=2 and an attained strict gap at every finite memory, while finite controllers approximate exponentially in M. Each fixed-M optimum is algebraically computable.

**Direct logical prerequisites.** `thm:r80-arithmetic-saturation`, `thm:r79-quantum-frontier`

**Inherited mechanisms and contextual authorities.** None listed in this category.

**Proof mechanism.** Unique factorization proves log(2)/log(3) irrational; apply the theorem.

**Classical ingredients and priority boundary.** Classical search ordering and convex risk separation as explicitly attributed.. Exact displayed arithmetic example; no transcendence assertion for unrestricted value.

**Limits.** The example does not determine a closed formula for its intermediate finite-memory values.

## Retained authority and unresolved questions

All 252 predecessor proof records retain every nondisplay field unchanged. Current document, number, page, source and locator-description fields are refreshed. The original ledger remains byte-identical, as do the R74–R79 addenda and all protected proof bodies. Edition-relative words such as 'new' within an unchanged old record refer to that original edition, not to R80.

The original general-M squared-sign risk frontier, optional-stopping tied control and universal finite-memory saturation, unrestricted high-contrast classification for every finite group, the matching unrestricted-decoder approximation rate, intermediate timing, coefficient-bit/precision/program/workspace costs, unknown-model recovery and independent Theta objectives remain distinct. In particular matrix parameter-feasibility equivalence does not classify every off-boundary positive factorization, and a sharp excursion probability is not a sharp universal approximation cost. The inherited R76 matching leading logarithm applies only to the stated fixed physical density dictionaries with Born terminal decoders, at fixed positive target budget and a fixed badly approximable phase.

## Evidence categories

The written proofs are ordinary author arguments. Author-team AI challenges, finite exact/floating diagnostics, native compilation, source hashing, independent human assessment and editorial decisions remain separate evidence types. General real quantifier elimination is an existence/computability ingredient; these maps do not claim it was executed. The R65 deposited report is not reclassified as a review of R80.

Regenerate with `python build_theorem_map.py` and check with `python build_theorem_map.py --check`. Missing labels, a different inherited authority, altered nondisplay old proof fields or an incomplete current statement inventory are rejected.
