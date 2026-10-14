# Literature comparison — checked 13 October 2026

Primary references used in the manuscript and checked online include Dufour--Prieto-Rumeau, *Absorbing Markov Decision Processes* (arXiv:2309.07059; revised 9 October 2025), their *Geometric Properties and Sufficiency of Finite Mixtures of Deterministic Policies* (arXiv:2512.17511, 19 December 2025), Kim's *Finite Memory Belief Approximation* (arXiv:2601.03132v1, 6 January 2026), and Sokolov's *Markovization of Randomized Stopping Times* (arXiv:2609.24652v1, 21 September 2026). These preprints are not presented as journal acceptance or independent endorsement.

| Prior/retained tool | This revision's precise distinction |
|---|---|
| Conditional projection, positive-map resolvents, randomized termination | Standard mechanisms; the new proof combines a same-label mean reserve with actual-occupation errors and strict-slack feasible finite enumeration |
| Phantom occupation decomposition (Dufour--Prieto-Rumeau) | Inherited from prior literature; not a new discovery. Used in a finite predictive common-program realization |
| Finite mixtures for uniformly absorbing MDPs | Different policy/resource object. Current competitors need not be uniformly absorbing; only synthesized programs are regularized, with the cost paid inside N |
| Value-directed belief compression (Poupart--Boutilier) | Task-directed compression is prior. Here global lower ranges over all legal hard-state stopped observers and a single unknown-model program |
| Kim's fixed-policy Wasserstein/window-memory bounds | Current theorem optimizes action/routing/stopping over hard total states; it is not merely cost replacement under one closed-loop policy |
| Bayes risk/Bregman quantization (Varshney) | Prior geometry; retained dynamic Bayesian appendix credited, not the new contribution |
| Stopping Markovization (Sokolov) | Time/state intensities do not by themselves supply a fixed hard-state controller; current controller has no free clock |
| Trimmed quantization/rejection sampling | Static profile and sampling tools are prior; mean-budget causal profile law inherited from earlier restart manuscripts |
| R46 exact occupation + profile | Fully retained and explicitly cited. New part is finite two-sided realization at identical N,M plus raw same-budget modulus |

The search is targeted, not exhaustive. No priority certificate or claim of solving a named open problem is made. The finite synthesis theorem does not establish computational efficiency or an optimal description-length lower frontier.
