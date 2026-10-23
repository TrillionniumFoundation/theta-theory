# R78 author-team mathematical challenge and primary-source comparison

Date: 23 October 2026. This document records an independent author-team AI challenge, not an external referee report, a human expert endorsement, formal verification, or an editorial decision.

## 1. Inherited baseline examined

The read-only input was the complete R77 source at `/workspace/scratch/3d6caf252b4a/theta-theory/papers/General-Theta-Foundations-I-restart/r77-shared-preparation-and-memory`, including the main compilation graph, the shared-preparation section, the optimal-reset-memory section, the finite reset-control theorem, the convex-specification normal form, the R77 proof audit, and the stored R65 report. Repository-wide selection of the controlling author/review commits is the separate provenance census; this challenge does not infer a new independent review from an internal audit.

No contradiction was found in the R77 shared identity-word projection, its distinct-pure-initializer count, the invariant-polytope formula, or the common-mean joint Fourier construction. In particular the common mean, the common decoder, the all-word quantifier, and the difference between pure and mixed preparation are substantive hypotheses. The positive-exposure limitation of the R77 reset-cover theorem is real: its supplied semidefinite counterexample has a one-label robust optimum despite locally nonoptimal behavior at a reset state. The new proof should extend this result without deleting or relabelling the earlier correct theorem.

## 2. Adversarial check of the new reset normalization

For a fixed palette of command rows `p^1,...,p^M`, treat selection of a row as an action of a finite stochastic shortest-path problem on the reset indices. The cost and transition law for row `k` at reset `i` are the corresponding mixtures of the primitive `c_ia` and `Q_iaj`. The original autonomous controller is an admissible history-dependent policy of this comparison problem: its private label evolution simply chooses members of the existing palette.

The delicate step is finiteness on **every** reset state. All-initial-state robustness includes each physical density matrix `sigma_i`. Restarting the original device in its prescribed label with that initial state therefore gives a proper finite-cost policy using the same palette. This proves that the palette Bellman values are finite and bounded by the original robust cost. It does not assume that every product pair `(reset state, retained label)` of the original device is proper or reachable.

The simultaneous Bellman minimizer chooses one of the existing rows after each observed report. Its implementation retains that row's existing label and preserves the original initial row. Positive costs make the finite Bellman equality proper. Its continuation value is at most the original continuation cost at each reached history, giving an operator inequality for the complete initial-state cost, not merely an inequality at one prior. Hence a deterministic update depending only on the current reset report suffices at no extra label cost. The claim still allows mixed command rows; it does not purify every command distribution.

### Boundaries checked

- An unreachable improper product pair does not invalidate a robust pure-start controller. Requiring the full `sM` product matrix to have spectral radius below one would be an incorrect proof shortcut. The independent diagnostic includes a controller that succeeds immediately from every physical state, with an unused label that would trap forever. Its full product system is singular.
- The global finite-potential cap cannot be inferred from performance at one fixed prior. A command can succeed immediately at the allowed prior and trap at another reset state, while a second command makes the primitive experiment globally feasible. The finite diagnostic includes this case.
- With an all-state competitor of cost at most `b`, the minimal palette potential satisfies `x_i <= b` because each `sigma_i` is an allowed initial state. Therefore a known finite one-label robust upper bound `C0` gives a safe compact cap `0 <= x_i <= C0` for the optimization at budgets `b <= C0`.
- A finite nonnegative Bellman supersolution and a strictly positive per-call cost floor imply properness by bounded expected call count. Without the cost floor, a zero-cost infinite failure loop could satisfy a supersolution inequality.
- The observation port remains the declared report. A realized charge, a hidden intermediate measurement, an uncounted classical label, or a protected quantum state is not an extra controller observation. The result concerns the stated classical autonomous controllers, not observer-owned quantum memory.
- The finite reset property is essential to this reduction. An arbitrary quantum instrument can retain input-dependent posterior information after a report, so a report index need not determine its state or future law.

## 3. Adversarial check of the exact covering-family frontier

In the R77 physical covering family the total failure probability is the same number `r` at every call. If `h_i = min_k p^k(A_i^c)`, the reset Bellman equations solve exactly as

`x_i = 1 + h_i + r (1 + mean(h))/(1-r)`.

The initial-state coordinates used to impose the initial command penalty dominate the reset coordinates, so the objective is

`3 + r/(1-r) + max_a p^1_a + r/[s(1-r)] sum_i h_i`.

For fixed other rows this is concave in any continuing row `p^k`, `k>=2`; at least one extreme row is no worse. Starting at a global minimizer, sequentially replacing each such row by an extreme row retains global optimality. This establishes the existence of pure continuing commands, without claiming that every optimizer is pure or that the same fact holds for general instruments.

Let `H` be the continuing actions and let `b_a` count the uncovered sets that omit action `a`. For the initial-row problem `min_p [max p + lambda b.p]`, fix the cap `t=max p`. Greedily filling coordinates of smallest `b_a` gives a function affine between consecutive breakpoints `1/k`. Some optimum therefore has a uniform initial row on `k` actions of smallest `b_a`. Flat segments may give additional nonuniform optimizers, so the theorem should claim existence of a uniform-subset optimizer rather than uniqueness.

For singleton sets on `n>=2` actions and `r=1/2`, the optimal uniform subset is the full action set and the full exact staircase is

`V_M = 4 + 1/n + max(n-M+1,0)(n-1)/n^2`.

Every step is strict through `M=n+1`, after which the value saturates. The condition `n>=2` is required for strictness. On this singleton family the full gap is exactly twice the R77 one-step residual certificate; that factor is not a universal claim for all set systems or all failure probabilities. The formula is an exact frontier for this expanding physical family, not the previously open squared-sign qubit minimax-risk frontier.

### Continuity and the noncommuting perturbation

The complete R78 draft `53-reset-memory-frontier.tex` was subsequently read through all five named results. The continuity proof uses the same transient full-support row to obtain locally uniform caps. A fixed attaining report selector stays transient under small perturbations, giving the upper limit. Compact supersolution certificates and a constant-selector subsequence give the lower limit. The limiting certificate need only have a finite potential, not lie under one particular formula for the base-point cap. This correctly avoids a hidden continuity assumption about optimal selectors.

The explicit perturbation replaces `E_11` by `E_11 + epsilon X`, where `X=|e_1><f_1|+|f_1><e_1|` and `0<epsilon<(n-1)/(8n^2)`. It is positive definite and leaves the reset transition numbers unchanged. Its change in any palette's initial cost operator has norm at most `4 epsilon`, so the adjacent optimal gaps remain at least `(n-1)/n^2 - 8 epsilon > 0`.

Noncommuting effects and cost operators need a joint physical realization, not independent specifications. The final draft supplies one: failure costs one, while success splits into effects `F_9=(G-I)/8` and `F_1=B-F_9`, with costs nine and one. Here `F_1 >= (1/8-epsilon)I > 0`; the aggregate mean is `I+8F_9=G`. Thus the perturbed paid costs are `{1,9}`, and their mean operators still lie between `I` and `4I`. The statement that every realized cost lies in `[1,4]` belongs only to the unperturbed diagonal construction. This qualification was checked and retained.

## 4. Original literature and priority

Only primary author manuscripts, publisher pages, and official proceedings were used for the substantive comparisons below. The URLs were read on 23 October 2026. A literature search is not exhaustive priority clearance.

### Stochastic shortest-path theory

D. P. Bertsekas and J. N. Tsitsiklis, *An Analysis of Stochastic Shortest Path Problems*, Mathematics of Operations Research **16** (1991), 580–595, DOI [10.1287/moor.16.3.580](https://pubsonline.informs.org/doi/10.1287/moor.16.3.580). [Author-hosted original PDF](https://www.mit.edu/~jnt/Papers/J034-91-berts-SSP.pdf).

The finite SSP reduction, Bellman verification, and properness reasoning are classical ingredients. The scanned author PDF was available but did not yield searchable text through the web reader; the publisher metadata and abstract were verified. The current author proof should remain self-contained instead of hiding its finite-cost and positive-cost arguments behind this citation.

### Finite-policy product chains

N. Meuleau, K.-E. Kim, L. P. Kaelbling and A. R. Cassandra, *Solving POMDPs by Searching the Space of Finite Policies*, UAI 1999, 417–426. [Author-hosted original paper](https://www.cassandra.org/arc/papers/uai99.pdf).

The paper's introduction and policy-graph construction explicitly use the product of the physical state and controller node to evaluate finite policies and develop bounded-controller search. The formulation optimizes a discounted prior-based objective and includes stochastic policy graphs. Therefore finite-state parameterization, product-chain evaluation, or bounded-memory search cannot be claimed as new here. The reset result instead removes stochastic update kernels for an entire fixed row palette, reduces continuation values to the reset index alone, and uses an unknown-state spectral objective with a counted pure initial label.

### Bounded stochastic controllers

P. Poupart and C. Boutilier, *Bounded Finite State Controllers*, Advances in Neural Information Processing Systems **16**, conference 2003. [Official proceedings](https://papers.nips.cc/paper_files/paper/2003/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html).

The official abstract presents bounded policy iteration over fixed-size stochastic controllers. Its existence precludes framing bounded stochastic-controller optimization as a newly introduced research problem. The manuscript should identify the structural simplification proved under the reset hypotheses and distinguish it from a new general POMDP algorithm.

### Exact nonlinear formulations are prior work

C. Amato, D. S. Bernstein and S. Zilberstein, *Optimizing fixed-size stochastic controllers for POMDPs and decentralized POMDPs*, Autonomous Agents and Multi-Agent Systems **21** (2010), 293–320, DOI [10.1007/s10458-009-9103-z](https://link.springer.com/article/10.1007/s10458-009-9103-z). The publisher confirms online publication on 25 August 2009 and the 2010 issue. [Searchable author manuscript](https://web.cs.umass.edu/publication/docs/2007/UM-CS-2007-070.pdf).

Section 4.1, Table 2 and Theorem 1 give a nonlinear program defining the optimal fixed-size stochastic controller for a specified initial distribution. Its variables include action selection, node transitions and values for node–state pairs. Consequently the existence of a finite nonlinear or semialgebraic optimization is not by itself the R78 contribution. The manuscript should explicitly compare the reset-dependent elimination of transition variables, the common `s`-dimensional potential, positive-cost undiscounted attainment, and the all-density-matrix initial spectral bound. The exact covering-family solution provides more content than restating a general nonlinear program. Publisher full text was subscription-restricted, but the author manuscript containing the cited theorem was actually read.

### Machine convention matters

C. Amato, B. Bonet and S. Zilberstein, *Finite-State Controllers Based on Mealy Machines for Centralized and Decentralized POMDPs*, AAAI **24** (2010), 1052–1058, DOI [10.1609/aaai.v24i1.7748](https://ojs.aaai.org/index.php/AAAI/article/view/7748).

The official abstract and bibliographic record compare Mealy and Moore controller representations. They support making the present interface explicit: the next command is determined by the retained counted label; the most recent report only selects that label at the update. Permitting the next action to consult an uncounted report register would change the resource model. Only the official abstract was inspected; no theorem-level claim about the full paper is made here.

### Complexity is not new merely because the program is nonconvex

N. Vlassis, M. L. Littman and D. Barber, *On the Computational Complexity of Stochastic Controller Optimization in POMDPs*, ACM Transactions on Computation Theory **4** (2012). [Author manuscript, arXiv:1107.3090v2](https://arxiv.org/html/1107.3090v2).

Sections 1–3 establish hardness even for a fixed stochastic blind row in a discounted model, and distinguish exact numerical threshold questions from deterministic-controller guesses. This cautions against asserting that exact synthesis has polynomial complexity or lies in NP merely because the label count is finite. The R77 explicit reset covering reduction remains a specific physically realized hardness result; the R78 exact finite procedure should make no running-time claim not proved in the source.

## 5. Proposed manuscript wording

> Finite-state controller optimization and its nonlinear-programming formulations are classical. The structural point of the following theorem is that a finite reset experiment admits, for every fixed collection of command rows, one deterministic report update which dominates all stochastic autonomous updates using those rows. Thus the continuation potential has one coordinate per reset report, rather than per report–label pair. The resulting attained variational principle includes every initial density matrix and charges the prescribed initial row; its proof does not require strictly positive failure effects. A covering-family specialization then yields an exact formula for the entire memory–cost frontier, not only a certificate of the minimum memory at the unrestricted optimum.

This paragraph is an author comparison, not a claim of exhaustive novelty. It should be supported by the direct citations above and the actual new proofs.

## 6. Independent diagnostic implementation

`diagnostics_r78_palette.py` evaluates arbitrary stochastic controllers by rational elimination on their reachable product chains and compares them with independently enumerated report-only selectors. It includes commuting diagonal effects with zeros, noncommuting qubit effects and costs with nonorthogonal reset states, an unreachable improper pair, a fixed-prior boundary example, the R77 semidefinite nonexposure example, exact rational palette grids for the covering formula, and every resource level of the singleton family for `n=2,...,8`.

The final development executions both completed successfully, with byte-identical normal and optimized outputs. They record 102,462 exact conditions and zero floating-point probes. Coverage includes 108 diagonal product-controller instances, 36 noncommuting qubit instances, 100,380 rational palettes across 264 covering/resource instances, 49 singleton resource points, and the stated degeneracy checks. The script SHA-256 is `ab93a8a64420e94b5dccd9f19ef2580e0c37ebf420a4e22955b9a0a2c2780cd1`; each JSON output SHA-256 is `7dd43324862a2af394e9a3043a2eb0330f589c82d93973a67e661c1c45776932`.

These normal and optimized Python outputs are development execution records; final integration must rerun them against the integrated source hash. The general quantified results rely on the manuscript proofs, not on these finitely many cases.
