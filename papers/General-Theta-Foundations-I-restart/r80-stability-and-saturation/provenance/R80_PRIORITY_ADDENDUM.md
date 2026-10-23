# R80 targeted primary-literature priority addendum

Date: 23 October 2026 UTC.

**Purpose and status.** This is an internal author literature comparison, not an independent referee report or a proof of priority. It examines the extension from two search locations to arbitrary finite `n`, and the exact square-root sensitivity of the optimum at a fixed finite-controller memory budget. The literature search began while the general-`n` proof was under checking. This updated note was aligned with completed `59-finite-search-saturation.tex`, SHA-256 `8e48af95faf9f8ce8c563b3d9b9d51c8fce408881ece30eee68e8ba74c31b053`, its seven-declaration inventory, and `R80_GENERAL_SEARCH_INTERNAL_AUDIT.md`, SHA-256 `f51f188b56f25e0560aff6f8c77c50dc3b73315f75e4c8a9ca1afd9fc0bcd912`. It does not replace that separate internal mathematical audit or supply human priority clearance. The complete two-location section remains in the current supplement with its sharper normalized constants.

## Findings that should control the wording

1. The established search-theoretic ingredients identified in §B must remain attributed when `n` is arbitrary.

2. The **sufficient** direction follows closely from §B's existing results plus counted initial selection and disjoint finite tails. It should be described as a resource-accounted consequence, not a new discovery of cyclic search.

3. The precise additional mathematical claim is the **necessary** direction against all autonomous finite stochastic controllers, particularly when some but not all failure probabilities are commensurate. The delivered proof treats arbitrary stochastic command and update rows, non-observable internal labels, fresh random draws, and a counted pure initial state, using a deterministic projected suffix of commensurability classes. Failure of one chosen deterministic greedy word to be periodic would not exclude the entire stochastic class.

4. No inspected primary source stated the delivered all-stochastic finite-realization equivalence in this exact model. The bounded search did not locate an equivalent theorem. Neither observation establishes that the result is the first in the literature, nor that its deduction from classical search and finite-state methods will be considered sufficiently difficult or significant for a particular journal.

5. The sharp sensitivity theorem concerns an **optimum over every allowed controller with a fixed label budget**, not the perturbation sensitivity of one fixed controller. The distinction matters: parametric Markov-chain descriptions and fixed-controller value analysis are long established. The explicit nonzero square-root asymptotic and all-controller converse are the precise assertions to compare.

## Primary-source comparisons

### A. Matula: periodic optimal search

David Matula, *A Periodic Optimal Search*, American Mathematical Monthly 71(1) (1964), 15–21. Publisher DOI: <https://doi.org/10.1080/00029890.1964.11992194>. JSTOR record: <https://www.jstor.org/stable/2311296>.

The publisher/JSTOR metadata were verified. Direct publisher full-text retrieval was blocked with HTTP 403, and the JSTOR page did not expose the article text. Accordingly, this check does **not** claim to have freshly read Matula's complete original argument. The concrete use of Matula's periodicity result below is identified through the inspected primary paper by Clarkson, Lin and Glazebrook. The manuscript's DOI is correct; a search result giving JSTOR identifier `2311300` was rejected because that identifier is a different article.

### B. Clarkson–Lin–Glazebrook: the closest substantive predecessor

Jake Clarkson, Kyle Y. Lin and Kevin D. Glazebrook, *A Classical Search Game in Discrete Locations*, Mathematics of Operations Research 48(2) (2023), 687–707, DOI <https://doi.org/10.1287/moor.2022.1279>. Inspected primary preprint: <https://arxiv.org/pdf/2103.09310> (arXiv v1; theorem numbering below is that version).

Proposition 3 gives interior optimal hiding probabilities and equalized location costs. Theorem 10 provides an optimal mixture of at most `n` search sequences with consistent preference-based tie rules. Section 6, equation (21), defines the cyclic case by common positive integer powers of the failure probabilities. Section 6.1 and Appendix C describe the finite transient and repeating search cycle, attributing the relevant periodic-search fact to Matula. Their acyclic case, equation (22), requires pairwise incommensurability; it is stronger than merely failing global commensurability when `n>2`.

**Comparison:** the finite-mixture theorem counts infinite search sequences, not the states of an autonomous stochastic implementation. For a partially commensurate instance, the new necessity argument must handle infinitely many ties within commensurability classes. That case cannot be covered merely by citing their no-further-ties acyclic discussion. The new statement should acknowledge the classical sufficiency ingredients and identify the added stochastic support/realization obstruction explicitly.

### C. Bui–Lidbetter–Lin: pure infinite sequences are a different resource notion

Thuy Bui, Thomas Lidbetter and Kyle Y. Lin, *Optimal Pure Strategies for a Discrete Search Game*, European Journal of Operational Research 313(2) (2024), 767–775. Inspected primary preprint: <https://arxiv.org/html/2306.10908v1> (2023). Publisher record: <https://www.sciencedirect.com/science/article/abs/pii/S0377221723006707>.

The paper defines a pure search strategy as one infinite deterministic sequence and studies when such a sequence attains the minimax value. Section 2 assumes a common-power relation for its ensuing pure-strategy analysis. It distinguishes consistently tie-broken sequences from more general sequences; later pure strategies need not amount to selecting one finite-state periodic controller. Its introduction and preliminaries also credit the index rule and finite optimal mixture to earlier work.

**Comparison:** “pure” means absence of initial mixing among infinite sequences, while “finite memory” means an autonomous implementation with finitely many retained states. Neither property implies the other in general. R80 should not imply that its irrational nonrealizability contradicts a classical existence theorem for pure infinite strategies, or that its finite randomized realization settles all pure-strategy questions.

### D. Junges et al.: the finite-controller parameterization is established

Sebastian Junges, Nils Jansen, Ralf Wimmer, Tim Quatmann, Leonore Winterer, Joost-Pieter Katoen and Bernd Becker, *Finite-State Controllers of POMDPs via Parameter Synthesis*, UAI 2018. Official primary proceedings paper: <https://www.auai.org/uai2018/proceedings/papers/195.pdf>.

Theorem 2 gives a correspondence between fixed-memory randomized FSCs and instantiations of a parametric Markov chain. Theorem 3 relates the associated synthesis problems computationally. Section 5 explicitly distinguishes graph-preserving and uniformly positive parameter restrictions, and discusses consequences of zero probabilities. Section 6.3 treats symbolic rational functions of controller parameters.

**Comparison:** neither randomized FSC parameterization nor the need to track zero edges is new. Those results do not by themselves provide a uniform-in-memory primitive modulus for an optimized undiscounted total cost through a reachability change, or the explicit sharp two-label lower asymptotic. This distinction should be stated using the actual objective and hypotheses, not a generic claim that prior controller theory ignores boundary probabilities.

### E. Kara–Yüksel: optimal control robustness predates this manuscript

Ali Devran Kara and Serdar Yüksel, *Robustness to Incorrect System Models in Stochastic Control*, SIAM Journal on Control and Optimization 58(2) (2020), 1144–1182, DOI <https://doi.org/10.1137/18M1208058>. Inspected primary preprint: <https://arxiv.org/pdf/1803.06046> (v7).

The paper studies continuity of optimal values and robustness of optimal policies for fully and partially observed models with an infinite-horizon **discounted** expected-cost criterion. Its total-variation results include Theorem 2.6 and Theorem 3.1; the latter gives a linear model-error bound with coefficient `2 ||c||_infinity beta/(1-beta)^2` for a fixed prior and bounded stage cost. Its policy space is not introduced as a fixed autonomous label budget.

**Comparison:** continuity under primitive/model perturbation is not itself a new problem. The source's discounted bounds have a quantitative properness mechanism absent at the support-changing undiscounted boundary in R80. Their result does not assert the two-label square-root expansion or refute it: the objectives and policy constraints differ. It is inappropriate to suggest that the square-root exponent replaces their discounted linear bound.

### F. Kraske et al.: a recent fixed-policy robustness comparison

Benjamin Kraske, Qi Heng Ho, Federico Rossi, Morteza Lahijanian and Zachary Sunberg, *Robustness Analysis of POMDP Policies to Observation Perturbations*, primary preprint <https://arxiv.org/pdf/2604.21256> (2026).

The inspected formulation asks for the largest observation-model deviation compatible with a prescribed degradation threshold for a **fixed policy**. Sections 3–5 separate stationary uncertainty from node/history-dependent variants and use FSC/Markov-chain reductions. Their infinite-horizon contraction argument uses a discount factor strictly below one. The work is directly relevant to robustness evaluation, but the decision variable and objective are different from minimizing an undiscounted total cost over all controllers with exactly the same allowed memory budget.

**Comparison:** cite it as a nearby fixed-policy perturbation study. A search over the paper found no stated sharp square-root optimized-memory asymptotic. That limited observation is not a conclusion about every result in the broader POMDP robustness literature.

## Interpretation of the delivered general-n theorem

The following are analytical comparisons, not claims copied from the cited literature.

The finite implementation must count its initializer, branch identity, cycle/transient positions, and any reported observations. Those implementation counts should not obscure the classical origin identified in §B.

For failure logarithms split into several rational-proportionality classes, a single pair of classes may be incommensurate even while each class has infinitely recurring internal ties. The delivered necessity proof controls the projected sequence of classes. It does not assume that all optimal full command words have a unique suffix, as in the two-location irrational case. Nor does it infer rational empirical frequencies from an arbitrary finite stochastic controller: a finite Markov chain with arbitrary real transition probabilities can have irrational stationary frequencies. The proved rigidity uses a **prescribed deterministic projected output** from a finite support process. The explicit deletion/completion prior floor, primitive-data exponential memory upper bound, and rational sufficient cap are further quantitative claims; their sufficient constants are not represented as sharp or computationally practical.

For the sensitivity theorem, a fixed finite controller on an unchanged transient support has a value obtained from finite linear equations. Optimization over a continuous controller family can produce singular behavior when the optimum approaches a reachability boundary. The manuscript's claim is therefore most accurately assessed as the combination of an explicit physical boundary family, a global lower argument against every admissible two-label controller, and a matching implementation. Merely observing a square root after minimizing one selected one-parameter family would not establish the stated optimality result.

## Suggested manuscript wording

For the completed general-`n` proof at the checked source identity, a defensible comparison is:

> Building on the classical search structure summarized above, we determine when the optimal value has an autonomous finite stochastic implementation under the counted-label convention. The necessity argument covers partially commensurate instances and arbitrary stochastic command and update rows; the converse records a counted implementation of the classical cyclic strategies.

For the stability theorem:

> The square-root loss concerns optimization at a fixed classical memory budget under undiscounted total cost. We prove its exact leading asymptotic in a two-model, two-label family and a converse against all permitted stochastic controllers. Discounted robustness bounds, fixed-policy sensitivity, and the parametric representation of finite controllers are established antecedents with different assumptions.

Avoid “the first finite-memory search theorem,” “a complete new solution of the classical search game,” “all prior methods assume positive transition entries,” and “the first square-root singularity in control.” None is justified by this check. A narrowly stated theorem can be presented as a proved manuscript contribution without making any of those universal historical assertions.

## Search coverage and evidence limits

This was a bounded targeted check, using thirteen query strings in four search batches plus direct inspection of the primary sources above. Query families combined discrete/imperfect search with finite memory, finite automata and finite-state realization; they also combined FSC/POMDP sensitivity with perturbation, Hölder regularity and square-root value behavior. Broad search produced substantial unrelated material, which was not used as evidence. The paper-specific reads concentrated on the exact classical search structure, the meaning of a pure infinite sequence, FSC parameterization, and robustness objectives/assumptions.

No equivalent all-stochastic finite-saturation criterion or matching sharp two-label perturbation asymptotic was identified in these inspected sources. There may be relevant results in older search monographs, automata realization theory, parametric stochastic optimization, or terminology not captured by these queries. In particular, the complete Matula original was not available for fresh reading. The correct outcome is a precise comparison and transparent remaining priority uncertainty, not a declaration of exhaustive novelty or specialist approval.
