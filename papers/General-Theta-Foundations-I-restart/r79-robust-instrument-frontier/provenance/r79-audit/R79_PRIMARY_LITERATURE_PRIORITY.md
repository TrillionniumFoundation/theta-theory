# R79 primary-literature and priority check

Search date: 23 October 2026. This is an author-side comparison of the proposed R79 results against directly examined primary papers, publisher records and official proceedings. It is not an independent referee report, an exhaustive priority certification, or evidence of editorial acceptance. The exact manuscript theorems and their proofs determine what may be claimed; this note records the strongest relevant precedents found and the distinctions that still require mathematical proof.

## Contribution boundary after complete inheritance comparison

The broad setting of quantum sequential control, fixed-size stochastic-controller synthesis, quantum reachable-support calculation and expected-cost potentials is established. More specifically, this manuscript's inherited Section12 and the face certificate already prove arbitrary-CP support and potential verification, finite-model fixed-memory algebraic synthesis and compact attainment. Sections17 and19 already supply primitive fallback, a centered effect estimate and finite-history completion. Their current self-contained restatement is not an R79 discovery claim.

The principal additional statement is same-M controller-label regularization: returning occasionally to the already counted initial label, without physically resetting the experiment or changing its fixed hidden model, gives bounded full-space cost witnesses and hence a primitive stability modulus uniform over all finite memory budgets, including support-changing boundaries. The compact-semialgebraic arbitrary-feedback cost certificate is a scoped extension supporting that argument. The exact golden-ratio model and positive-success Lipschitz refinement supply matching special-model bounds. The latter uses classical resolvent theory and does not prove that the general square-root modulus is sharp. The complete statements and written proofs, rather than a literature-search absence, define these claims.

## Direct precedents and necessary attribution

### Fixed-controller optimization: Amato, Bernstein and Zilberstein

Christopher Amato, Daniel S. Bernstein and Shlomo Zilberstein, *Optimizing fixed-size stochastic controllers for POMDPs and decentralized POMDPs*, Autonomous Agents and Multi-Agent Systems **21** (2010), 293–320, DOI [10.1007/s10458-009-9103-z](https://link.springer.com/article/10.1007/s10458-009-9103-z).

This paper formulates fixed-size stochastic-controller optimization as a nonlinear program and studies practical optimization. Consequently, fixed-M nonlinear optimization is not a new organizing principle of R79. Cite the existing manuscript key `AmatoBernsteinZilberstein10`. The contribution must be in the additional exact mathematical structure, quantified uncertainty, boundary behavior and proved resource-preserving comparison, not in introducing optimization variables for a controller.

### Parameter synthesis: Junges and coauthors

Sebastian Junges, Nils Jansen, Ralf Wimmer, Tim Quatmann, Leonore Winterer, Joost-Pieter Katoen and Bernd Becker, *Finite-state Controllers of POMDPs via Parameter Synthesis*, UAI 2018, 519–529. The [official proceedings PDF](https://www.auai.org/uai2018/proceedings/papers/195.pdf) uses “via”; earlier listings and preprints vary in title.

Section 3, Theorem 2 gives the correspondence between bounded FSCs and instantiations of an induced parametric Markov chain. Section 4, Theorem 3 establishes reductions between controller and parameter synthesis. Indefinite-horizon reward specifications are expressly included; Section 5 discusses zero probabilities and graph preservation. Thus neither a product construction nor exact bounded-controller synthesis through real parameters is independently new. A fair R79 comparison must specify its CP operator setting, common controller under uncertainty, exact reachable-domain certificate and perturbation result.

### Robust undiscounted FSC synthesis: Cubuktepe and coauthors

Murat Cubuktepe, Nils Jansen, Sebastian Junges, Ahmadreza Marandi, Marnix Suilen and Ufuk Topcu, *Robust Finite-State Controllers for Uncertain POMDPs*, AAAI **35**(13) (2021), 11792–11800, DOI [10.1609/aaai.v35i13.17401](https://ojs.aaai.org/index.php/AAAI/article/view/17401). Examined [arXiv v2](https://arxiv.org/html/2009.11459v2), Sections 2–4.

This is a direct predecessor: one FSC must satisfy an undiscounted expected-reward-to-goal requirement for all fixed model instantiations. It uses a semi-infinite nonlinear formulation, dualization and sequential convex programming. Section 2 assumes no dead ends, stated as eventual goal reachability under every policy, and graph-preserving uncertainty. Do not describe this literature as only discounted or only nonrobust. R79 can distinguish its model-dependent reachable supports, support-changing boundaries, general CP instruments, lack of an all-label properness assumption, and proved global equivalence/attainment. Its construction should not be advertised as the first robust FSC program.

### Fixed hidden model and common finite memory: Galesloot and coauthors

Maris F. L. Galesloot, Roman Andriushchenko, Milan Češka, Sebastian Junges and Nils Jansen, *Robust Finite-Memory Policy Gradients for Hidden-Model POMDPs*, IJCAI 2025, 8518–8526, DOI [10.24963/ijcai.2025/947](https://www.ijcai.org/proceedings/2025/947). Examined [arXiv:2505.09518](https://arxiv.org/pdf/2505.09518), Sections 2–4.

This work optimizes a shared FSC against a finite family of fixed hidden models using worst-model evaluation and policy-gradient methods. It considers expected reward until a goal and makes reachability/support assumptions for finite differentiable values. Hence common-controller robust finite-memory optimization over a hidden fixed model is established. R79 should identify its compact semialgebraic continuum, exact certificates at boundary controllers, and uniform perturbation theorem. FSC observation conventions also matter: counts cannot be compared directly if current observations are freely available to action selection in one model but must be encoded in charged labels in the other.

### Quantum control models: Barry, Barry and Aaronson

Jennifer Barry, Daniel T. Barry and Scott Aaronson, *Quantum partially observable Markov decision processes*, Physical Review A **90** (2014), 032311, DOI [10.1103/PhysRevA.90.032311](https://doi.org/10.1103/PhysRevA.90.032311). Examined [arXiv:1406.2858](https://arxiv.org/pdf/1406.2858), under the preprint title *Quantum POMDPs*.

The paper already models quantum states, action-selected instruments, observed outcomes and rewards, and establishes complexity and undecidability results for its policy problems. R79 is not an introduction of quantum POMDPs. Its fixed finite-memory algebraic setting is narrower than unrestricted-policy questions; the proposed decidability result must not be said to contradict general undecidability. Reuse the existing key `Barry14`.

### Finite reachable support: Yu–Ying and Ying–Feng–Yu–Ying

Nengkun Yu and Mingsheng Ying, *Reachability and Termination Analysis of Concurrent Quantum Programs*, CONCUR 2012, LNCS **7454**, 69–83, DOI [10.1007/978-3-642-32940-1_7](https://doi.org/10.1007/978-3-642-32940-1_7). In [arXiv:1206.1935](https://arxiv.org/pdf/1206.1935), Theorem 1 computes the reachable subspace by at most d iterates of the summed positive transition map. The proof is finite-dimensional stabilization of an ascending support chain.

Shenggang Ying, Yuan Feng, Nengkun Yu and Mingsheng Ying, *Reachability Probabilities of Quantum Markov Chains*, CONCUR 2013, LNCS **8052**, 334–348, DOI [10.1007/978-3-642-40184-8_24](https://link.springer.com/chapter/10.1007/978-3-642-40184-8_24). [arXiv:1304.0060](https://arxiv.org/pdf/1304.0060), Lemma 1(2), restates the finite-iterate support description and attributes it to Yu–Ying. The paper develops quantum recurrent/transient structure and reachability algorithms.

Therefore the Md-step support generation for the controller–physical product is a specialization of established finite-dimensional reachability. Give a short self-contained proof for the block-positive-map convention and cite this origin. Its use to make the new robust finite-witness statement exact is the new synthesis under consideration; the support stabilization itself should not carry a novelty claim.

### Expected-cost observables: Liu, Zhou, Barthe and Ying

Junyi Liu, Li Zhou, Gilles Barthe and Mingsheng Ying, *Quantum Weakest Preconditions for Reasoning about Expected Runtimes of Quantum Programs*, Journal of the ACM **72**(3) (2025), Article 20, 1–51, DOI [10.1145/3734516](https://doi.org/10.1145/3734516). Examined [arXiv:1911.12557v3](https://arxiv.org/pdf/1911.12557), extended version.

Theorems 1–2 and the matrix-method section provide runtime observables on termination domains and connect finite-dimensional almost-sure termination with finite expected runtime. R79 should acknowledge both the operator representation and the relevance of the correct termination subspace. Requiring a finite cost witness only where initial states can reach is mathematically necessary, but it is not a newly discovered principle of quantum verification. R79 must prove its optimization, uniform quantification, implementability and boundary claims in its own conventions.

### Cost supersolutions: Avanzini and coauthors

Martin Avanzini, Georg Moser, Romain Péchoux, Simon Perdrix and Vladimir Zamdzhiev, *Quantum Expectation Transformers for Cost Analysis*, LICS 2022, Article 10, 10:1–10:13, DOI [10.1145/3531130.3533332](https://doi.org/10.1145/3531130.3533332). Examined [arXiv:2201.09361](https://arxiv.org/pdf/2201.09361), Section 4 and its loop upper-invariant rule.

This work develops sound and adequate expected-cost transformers for mixed classical–quantum programs. Positive supersolutions bound least fixed points, including loop costs. The inequality relating a cost witness to immediate cost and its adjoint continuation is therefore a familiar verification structure. The new manuscript should prove exactly when such witnesses exist for its reachable block spaces and how they characterize the robust resource frontier, rather than claim novelty for telescoping a positive supersolution.

### Current complexity and perturbation literature

Eline M. Bovy, Caleb Probine, Marnix Suilen, Ufuk Topcu and Nils Jansen, *On the Complexity Gap Between POMDPs and Multi-Environment POMDPs*, [arXiv:2610.15010v1](https://arxiv.org/html/2610.15010v1), 10 October 2026, especially Section 7.2. This recent preprint treats finite-horizon robust rewards and time-dependent FSC classes and proves real-algebraic complexity results. Its time-dependent controller convention and finite horizon differ from autonomous stopped total cost. Cite it as a preprint if discussing current complexity; do not assert publication merely from its template year.

Yunus Emre Demirci, Ali Devran Kara and Serdar Yüksel, *Sensitivity of Filter Kernels and Robustness Bounds to Transition and Measurement Kernel Perturbations in Partially Observable Stochastic Control*, [arXiv:2508.10658v3](https://arxiv.org/abs/2508.10658), 2025. This addresses explicit robustness bounds for discounted and average-cost partially observed control. Reuse `Demirci25`. It prevents a blanket first-continuity claim, while the proposed undiscounted stopped-cost bound under exactly the same charged memory is a distinct target. No directly matching same-label nonreset restart theorem was found in this search; that is a search outcome, not proof of priority.

## What the revised claims must make explicit

1. **Finite data and effective coefficients.** Semialgebraic representability over arbitrary real coefficients differs from an algorithm with rational or effectively specified algebraic input. State the coefficient model for any decidability claim. A finite threshold formula does not imply a practical solver or a polynomial complexity bound.
2. **Order of quantifiers.** The strategy must be common to all models. Reachable supports and cost operators may vary with the model. Exchanging these quantifiers changes the scientific problem. A uniform bound on witness norms must not be introduced unless proved; compactness of the model set alone does not establish such a bound when supports degenerate.
3. **Properness and attainment.** Positive call cost makes an infinite surviving trajectory costly. The equivalence between finite value and a reachable-space witness must be proved without presuming all controller labels are reachable. Attainment should follow from the actual compact controller space and lower-semicontinuity argument, not from an unjustified compactness claim for all witnesses.
4. **Same charged resources.** Restart means a randomized update of existing controller labels. It must not reset the quantum system, add a clock, add a hidden mode or supply an uncharged random initialization. Show the implemented action/update row explicitly. The pure initial label and all permitted physical initial states must survive the construction.
5. **Uniform stability.** Give the exact instrument norm, cost norm, local one-row cap and positive cost floor. State which constants depend on dimension, model family, experiment and M. A square-root upper modulus is not a sharp exponent unless a matching obstruction is proved. The theorem concerns the stated robust frontier, not arbitrary optional stopping or the whole Theta pipeline.
6. **Closed-form examples.** A two-model scalar example can demonstrate strict 1/2/3-label differences and irrational optimal randomization. Its exact lower bound and optimal realization are valuable tests of the general theorem, but it does not replace a general theorem or settle general-M squared-sign risk or the unresolved stopped-response asymptotic gap.

## Suggested main-text positioning

“Finite-state controller optimization and its reduction to parametric models are established in classical partially observed control. Robust synthesis already covers undiscounted goal rewards, and finite-dimensional quantum reachability and expected-cost observables supply further ingredients. Our result concerns their combination under a strict autonomous memory budget: one controller must work for an entire uncertain quantum instrument family, while its finite certificate is formed on the model-dependent reachable subspace. The same-memory perturbation theorem is obtained by restarting controller labels without resetting the physical state. The proofs below treat unreachable labels and support-changing boundary models explicitly.”

Use this paragraph only after the exact statements have been proved. The literature check supports a careful comparison, not a declaration that the mathematical importance demanded by a leading general mathematics journal has been settled.

## Additional targeted restart/robustness search

A follow-up search for proper-policy perturbations and finite-controller restart arguments also examined Dimitri P. Bertsekas and Huizhen Yu, *Stochastic Shortest Path Problems Under Weak Conditions*, [author report LIDS-2909, January 2016 revision](https://web.mit.edu/dimitrib/www/SSP_Weak_Conditions.pdf). Section 2 adds a small positive cost to every nonterminal transition to distinguish proper from improper policies. This is an important classical regularization precedent, but that operation changes stage costs; it does not prove the proposed same-M label-update perturbation estimate. The inherited `BertsekasTsitsiklis91` citation already supplies the classical positive-cost SSP foundation. Avoid describing regularization or properness itself as newly introduced.

Benjamin Kraske, Qi Heng Ho, Federico Rossi, Morteza Lahijanian and Zachary Sunberg, *Robustness Analysis of POMDP Policies to Observation Perturbations*, [arXiv:2604.21256v1](https://arxiv.org/pdf/2604.21256), 23 April 2026, studies the largest observation perturbation tolerated by a given policy, with static and history-dependent model variants and finite-controller reductions. This is another direct precedent for robustness questions at fixed controller size. The examined formulation evaluates a fixed policy through parametric/interval Markov chains; its statements do not supply the proposed optimal-frontier continuity theorem with replacement of the controller by a regularized controller of exactly the same size. This comparison is limited to the inspected statements and proof mechanisms, not a negative theorem about the literature.
