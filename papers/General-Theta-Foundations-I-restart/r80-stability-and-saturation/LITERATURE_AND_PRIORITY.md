# Literature and mathematical priority — R80 author revision

## Purpose, controlling source, and preserved ledger

This document identifies what the current manuscript proves, which ingredients are classical or inherited, and which external comparisons have actually been made. It is an author priority ledger, not an independent specialist report or an editorial assessment.

The complete preceding ledger is retained without alteration at [inputs/r79/LITERATURE_AND_PRIORITY.md](inputs/r79/LITERATURE_AND_PRIORITY.md), SHA-256 `544cbd895ce72c728b77cbe4f578e28036b17678510d8d216278ab85a7367fee`. That file preserves the full R79 comparisons and the route to R78 and earlier ledgers. Its historical descriptions of retrieval and examination remain historical; linking it does not mean that every older cited paper was freshly read again in R80.

The current main proof additions are `sections/57-sharp-stability.tex` and `sections/59-finite-search-saturation.tex`. The entire two-location refinement `sections/58-arithmetic-saturation.tex`, including its stronger normalized constants, is retained in the current supplement before the inherited technical body. The source and theorem maps control the final integrated locations and identities. The fresh reading record is `provenance/R80_PRIMARY_LITERATURE.json`; the detailed targeted comparison is `provenance/R80_PRIORITY_ADDENDUM.md`.

## Current contribution and internal inheritance

The principal new classification asks when a robust optimal history law for a finite imperfect-search experiment has an autonomous implementation with finitely many classical labels. It allows every finite number `n>=2` of fixed hidden models and commands, arbitrary positive deterministic command costs, strictly interior matching failure probabilities, one failure report, compulsory success stopping, and arbitrary stochastic command/update kernels. The initial label is prescribed, pure, and included in the budget.

Theorem `thm:r80-finite-search-saturation` proves that some finite budget attains the history value exactly if and only if all ratios of failure logarithms are rational. Its necessity argument covers partially commensurate families. Across different rational classes only finitely many tied priority levels occur. Consequently every optimal word has the same projected class suffix after a fixed finite time, although its commands within a class may remain random. A finite stochastic controller producing that prescribed class sequence would force an ultimately periodic suffix by positive-support recurrence. The irrational ratios of positive class frequencies contradict such periodicity.

The sufficiency direction uses the classical cyclic search structure, with a counted pure-start realization of the optimal finite word mixture. It is not claimed as a new discovery of periodic search. The explicit prior floor in `lem:r80-finite-search-prior-cap` supplies additional quantitative information: it depends only on the primitive failures and costs. It yields the upper memory gap in `thm:r80-finite-search-resource-bounds` and the effective rational-data cap in `cor:r80-finite-search-effective`. Those constants are sufficient, not sharp, and the cap is not a minimal-memory result.

The second structural addition is `thm:r80-sharp-modulus`. The inherited R79 same-label regularization proves an instrument modulus of order `sqrt(eta)` uniformly in the live-label budget. R80 shows that its exponent cannot improve under those assumptions, using a two-model, two-command, two-live-label family with unit costs and a uniform common fallback. It proves an exact nonzero leading square-root coefficient through a rigidity theorem at zero perturbation, a lower comparison covering every stochastic controller, and a matching realization. The physical discrepancy equals the perturbation parameter. The same family's one-label value is smooth. This is a statement about optimization at a fixed memory budget; it is not a claim about the sensitivity of one fixed policy.

### Claim-by-claim allocation

| Current component | Priority allocation and mathematical role |
|---|---|
| General finite-dimensional cost certificates, reachable support, supported potentials | Inherited from `lem:reachable-support`, `thm:memory-certificate`, `thm:face`, and their positive-cost assembly in Section 54. Not a new R80 discovery. |
| Fixed-budget attainment and algebraic synthesis | Inherited from `cor:memory-algebraic` and `thm:r79-quantum-frontier`; generic FSC parameterization and real-algebraic methods have external precedents. |
| Same-label regularization and uniform-in-memory stability | The R79 structural contribution, retained with its complete proof and actual assumptions. R80 supplies the matching exponent obstruction. |
| `lem:r80-finite-search-one-label` | An elementary geometric waiting-time calculation, used as the explicit common fallback. Its inclusion as a numbered lemma is not a novelty claim. |
| `lem:r80-finite-search-saddle` | Classical greedy search, interior/equalizer, and finite consistent-tie mixture structure; fully reproved for a transparent dependency chain. |
| Common-power search cycles and commensurate sufficiency | Classical structural ingredients, combined with explicitly counted initialization and tail labels. |
| `lem:r80-projected-word-rigidity` and the noncommensurate direction | Finite-support recurrence is elementary; its use for the deterministic commensurability-class suffix excludes the full stochastic controller class, including mixed rational/irrational relations. |
| Explicit least-favorable prior floor | A primitive-data refinement proved by deleting one command, estimating the strict gain in other models, and completing a restricted policy with the common fallback. |
| Exponential finite-memory approximation | A counted construction with explicit dependence on model number, failures, and positive costs; an upper bound rather than a matched memory-gap asymptotic. |
| Rational-data decision test and finite cap | Prime factorization and lattice counting are classical. The classification and prior floor make them an effective sufficient-budget certificate for this resource problem. |
| Exact two-label square-root singularity | The new sharpness statement for the optimized memory frontier, supported by a converse over all permitted stochastic rows. It does not assert that fractional-power phenomena in optimization are new. |
| Original causal-transfer, reset, discrimination, rank, geometry, and timing results | Preserved with their original scope, proofs, predecessors, and outstanding questions; they are not silently reassigned to the new search model. |

The declaration inventory contains 252 inherited and 15 added numbered items, for 267. These include classical and elementary lemmas, examples, and new conclusions. Neither the total nor the increment counts independent discoveries. The 32 diagnostic suites—29 inherited and three added—are an execution-coverage inventory, not a proof or novelty count.

## Current direct primary comparisons

### Imperfect search and finite implementation

David Matula, *A Periodic Optimal Search*, American Mathematical Monthly **71**(1) (1964), 15–21, DOI [10.1080/00029890.1964.11992194](https://doi.org/10.1080/00029890.1964.11992194), is the original periodic-search antecedent cited in the manuscript. The publisher metadata and [JSTOR identity](https://www.jstor.org/stable/2311296) were checked. The fresh full-text request was blocked, so this ledger does not claim a newly completed reading of Matula's original proof. Its use is identified through the inspected primary search paper below. The greedy rule is attributed to Blackwell as reported by Matula.

Jake Clarkson, Kyle Y. Lin and Kevin D. Glazebrook, *A Classical Search Game in Discrete Locations*, Mathematics of Operations Research **48**(2) (2023), 687–707, DOI [10.1287/moor.2022.1279](https://doi.org/10.1287/moor.2022.1279), is the closest structural predecessor. The inspected [arXiv version](https://arxiv.org/pdf/2103.09310) supplies Proposition 3, Theorem 10, and the common-power discussion in Section 6.1/Appendix C. These support the classical allocations above. Their cyclic/acyclic split must not be confused with R80's treatment of partially commensurate classes. The new resource claim quantifies over autonomous finite stochastic implementations, rather than counting the number of infinite sequences in an optimal mixture.

Thuy Bui, Thomas Lidbetter and Kyle Y. Lin, *Optimal Pure Strategies for a Discrete Search Game*, inspected [arXiv:2306.10908v1](https://arxiv.org/html/2306.10908v1) (2023), subsequently European Journal of Operational Research **313**(2) (2024), 767–775, studies optimal pure infinite search sequences. Its definition of a pure strategy does not charge an autonomous implementation's states. R80 does not equate purity with finite memory, contradict their pure-strategy results, or claim to solve every pure-strategy question. The bibliography key `BuiLidbetterLin2023` identifies the examined preprint; the year in that key is not an assertion of a 2023 journal issue.

The complete search proofs are written in the manuscript. In particular, the general-`n` proof does not assume that an arbitrary finite Markov chain has rational limiting frequencies—this would be false for real transition probabilities. The required periodicity concerns a prescribed deterministic **projected output**, proved by support recurrence. This is the exact point that needs comparison with finite-state realization literature beyond the classical ordering rule.

### Fixed memory parameterization and zero edges

Sebastian Junges and coauthors, *Finite-State Controllers of POMDPs via Parameter Synthesis*, UAI 2018, 519–529, [official proceedings](https://www.auai.org/uai2018/proceedings/papers/195.pdf), provides the FSC/parametric-Markov-chain correspondence in Theorem 2 and synthesis reductions in Theorem 3. Section 5 explicitly discusses zero probabilities and graph-preserving restrictions. Controller parameterization and awareness of boundary transitions are established. R80's comparison concerns the precise stopped-cost stability and sharpness conclusions, and its all-stochastic search implementation classification, not the existence of controller variables.

### Discounted robustness and the current stopped-cost modulus

Ali Devran Kara and Serdar Yüksel, *Robustness to Incorrect System Models in Stochastic Control*, SIAM Journal on Control and Optimization **58**(2) (2020), 1144–1182, DOI [10.1137/18M1208058](https://doi.org/10.1137/18M1208058), inspected [arXiv:1803.06046v7](https://arxiv.org/pdf/1803.06046), studies discounted optimal values and policies. Its Theorems 2.6 and 3.1 give total-variation error bounds under their hypotheses. The discount and bounded stage-cost regime differ from the current support-changing undiscounted cost frontier. R80 makes no first-continuity claim and does not present its square-root exponent as replacing their linear discounted bounds.

The current source retains its earlier stochastic-shortest-path and perturbation predecessors. Standard resolvent perturbation with a uniform success floor remains the mechanism behind the stronger Lipschitz regime. The new lower example instead addresses the general feasible class where a label can be dark and inaccessible in one model before perturbation. Its proof covers the reoptimized fixed-memory class, not only a chosen one-parameter repair strategy.

### Fixed-policy observation perturbations

Benjamin Kraske, Qi Heng Ho, Federico Rossi, Morteza Lahijanian and Zachary Sunberg, *Robustness Analysis of POMDP Policies to Observation Perturbations*, [arXiv:2604.21256](https://arxiv.org/pdf/2604.21256) (2026), was inspected at its fixed-policy formulation and FSC reductions. It studies admissible observation perturbations relative to a prescribed degradation threshold; the infinite-horizon contraction argument uses discounting. It is a relevant neighboring study, not an equivalent formulation of the fixed-budget optimized undiscounted frontier. This contextual comparison is retained here without inventing a journal publication or adding an unsupported bibliography entry.

## Earlier comparisons retained without fresh-reading inflation

The complete R79 ledger records the following relevant predecessors and the exact scopes examined then. Their original details remain at the explicit archived link rather than being silently dropped or represented as newly verified in this round.

| Earlier comparison | Retained priority consequence |
|---|---|
| Amato–Bernstein–Zilberstein, fixed-size stochastic-controller optimization | Nonlinear programming of finite controller rows is established. |
| Cubuktepe et al., robust FSCs for uncertain POMDPs | Robust undiscounted FSC synthesis predates this revision; its stated support/properness conventions must be compared precisely. |
| Galesloot et al., fixed hidden-model finite-memory policy gradients | A common controller for an unknown fixed model is established. |
| Barry–Barry–Aaronson, quantum POMDPs | Quantum action-selected instruments and sequential policy questions are established; fixed-budget effectivity does not resolve unrestricted-policy undecidability. |
| Yu–Ying and Ying–Feng–Yu–Ying, quantum reachability | Finite-dimensional reachable-support stabilization is established. |
| Liu–Zhou–Barthe–Ying; Avanzini et al., runtime observables and cost transformers | Positive runtime/cost observables, termination domains, and supersolution verification precede the current synthesis and comparison results. |
| Bertsekas–Tsitsiklis; Bertsekas–Yu, stochastic shortest paths | Properness and positive-cost regularization are classical concerns. Changing only a counted controller update requires its own proved bound. |
| Demirci–Kara–Yüksel, filter and model perturbations | Quantitative robustness is an existing area; the exact criterion, objective, and memory convention determine the comparison. |
| Bovy et al., POMDP/multi-environment complexity | Robust finite-memory algebraic formulations and their computational complexity have prior studies with different horizon and time-dependence conventions. |
| R78 and preceding original-paper ledgers | Residual automata, experiment comparison, statistical discrimination, rank bounds, variational/dual methods, and local geometry retain their original predecessor allocations. |

This table describes the preserved comparison record. It does not assert a fresh full-text examination or a changed publication status of every item. The old document is byte-authenticated; that establishes preservation, not re-review.

## Effectivity, assumptions, and open scope

The finite-search arithmetic classification uses strictly interior matching failure probabilities. At zero failure the all-failure positivity and infinite-retry arguments change; at unit failure that model is infeasible. Positive command costs are required for the call-count, deletion, and properness estimates. Costs are model-independent for each chosen command, as used by the exchange identity. An external clock, an uncounted persistent seed, or freely randomized initialization would change the implementation problem.

For rational failures, signed prime-exponent vectors make the commensurability test exact. In the saturating rational family, the explicit prior bound determines a sufficient finite label budget without knowing an optimal prior. The inherited finite-budget real-algebraic formula then computes the optimal value and a controller. Factorization, the size of the cap, and quantifier elimination are not claimed to have polynomial or practical complexity. The bound is not a minimum state count. No algebraicity claim is made for the unrestricted value in the nonsaturating case.

The exponential memory estimate is an upper bound. A proof of strictness at each finite budget is not a numerical lower bound or a matching asymptotic rate. The optimal perturbation exponent established at two labels does not solve the original arbitrary-memory squared-sign qubit-risk law. The unrestricted-decoder approximation gap, intermediate timing frontier, arbitrary tied terminal-loss classification, optional commitment, general instrument saturation, common unknown-model predictive quotients, and the separate A1/A2/Theta construction objectives retain their own open scope.

## Reading evidence and priority limits

`provenance/R80_PRIMARY_LITERATURE.json` records which primary texts were directly inspected, which metadata alone were accessible, the failed Matula full-text retrieval, and which comparisons are inherited. `provenance/R80_PRIORITY_ADDENDUM.md` provides the targeted analysis and its source-level limitations. The primary sources cited here support specified statements; an abstract is not represented as a full paper reading.

The targeted search did not locate an exact equivalent of the delivered all-stochastic finite-saturation criterion or the sharp optimized two-label perturbation asymptotic in the inspected sources. That is a bounded retrieval result. It cannot prove absence of such a theorem under different terminology or in uninspected older literature, and it is not specialist priority clearance. Universal phrases such as “the first finite-memory search theorem,” “the first square-root singularity in control,” or “all previous methods assume positive transitions” are not justified and are not used as contribution claims.

All essential current proof steps are written out. Native compilation, exact finite diagnostics, source authentication, and a separate AI author challenge provide different kinds of evidence; none constitutes human referee acceptance or a machine-checked universal proof. The four-journal research objective remains unchanged. Independent mathematical and editorial assessment must evaluate the scope, depth, and significance of the complete results, including the extent to which classical ingredients already supply parts of the argument.
