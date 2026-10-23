# Proof audit — General Theta Foundations I, R80

## Audit scope and controlling authority

This is an author audit of written mathematics and source consistency. It is not an independent referee report or proof-assistant certificate. The exact predecessor is R79 source `90cae2f5aca243b39d3a2194a4d6e0696671a101`, preserved through publication `a1b6a0be3b97b2cbcfc8c5cf457ec738bb33a5d2`. All 252 previous statement labels, their full proof bodies and nondisplay dependency fields remain current. The R65 report's earlier accepted scoped conclusions are inherited; no new defect in them is alleged without a demonstrated argument.

The current new proof declarations and their native source hashes are in `provenance/R80_PROOF_DEPENDENCIES.json`. The final native build binds these to an exact Git source SHA. Every mathematical assertion below is justified by its written proof, not by the diagnostic count.

## Load-bearing new sharpness chain

| Step | Mathematical issue | Resolution in the native proof |
|---|---|---|
| Six controller parameters | A proposed repairing policy alone cannot prove a lower bound for all stochastic controllers. | `eq:r80-six-parameters` parameterizes both command rows and all four failure updates; the lower argument keeps them unrestricted. |
| Reachability boundary | A full two-state inverse can fail at an inaccessible dark label even though initial cost is finite. | The initial reachable case is treated directly; the polynomial divisions are restricted to positive denominators. Endpoint rows are excluded or evaluated before division. |
| Baseline orientation | Label exchange cannot silently change the counted initial state. | Both row orderings are proved separately. The opposite ordering has the attained larger lower value `2(sqrt(19)-2)`. |
| Exact inequality | A numerical grid cannot establish optimizer uniqueness. | `eq:r80-positive-polynomial` is an explicitly expanded nonnegative polynomial; its equality conditions determine the unique effective optimum. |
| Quantitative rigidity | Compactness alone supplies convergence but no escape scale. | `lem:r80-boundary-coercivity` bounds `s+delta`, `gamma/(s+delta+gamma)` and the initial row shift by baseline excess cost. |
| Activated trap | The lower bound must charge a newly accessible formerly dark label. | `eq:r80-trap-cost` is an exact two-state identity. Its numerator includes the mandatory new failure contribution; nonnegative extra routing can only raise the lower bound. |
| Arbitrary perturbed optima | An ansatz or selected subsequence must not exclude better programs. | Attainment and compactness place every near-zero optimizer near the classified baseline; all scaled limit points satisfy the same two lower inequalities. |
| Matching coefficient | A positive order lower bound does not by itself identify the leading term. | The lower convex combination/AM–GM bound and the explicit `r_0+h sqrt(epsilon)`, `delta=k sqrt(epsilon)` program yield the identical coefficient. |

The new theorem proves sharpness of the exponent in the inherited general instrument class. Its coefficient and local rigidity belong to the displayed scalar family. It gives no exact positive-epsilon formula, no universally best upper constant and no contradiction to the stronger positive-success Lipschitz theorem.

## Load-bearing arbitrary-finite-n saturation chain

The main proof in `sections/59-finite-search-saturation.tex` allows every finite n>=2, every positive deterministic command cost and every failure probability strictly between zero and one. The common one-label fallback has exact value B=sum c_i/(1-r_i). All unrestricted policies are represented by laws on planned failure-path words; positive physical likelihood cancels when conditional next-command kernels are reconstructed.

The self-contained classical saddle proof uses adjacent exchanges, bounded logarithmic-score spread, compact word laws and separation. Deleting commands outside a boundary prior's support strictly reduces Bayes cost; finite-prefix fallback completion preserves admissibility in all models. Every robust optimum therefore equalizes every risk at an interior saddle and is supported on greedy words. A support-functional tie-order argument puts every greedy risk in the convex hull of the n! consistently ordered risks; affine dependence reduces an optimum to at most n words. This is classical search structure, not a new hard-budget convexity claim.

For necessity, commands are partitioned by rational commensurability of their failure logarithms. Each cross-class pair can tie at most once, so all greedy words have the same deterministic projected class suffix after a fixed time. Ratios of positive class frequencies are irrational when classes differ. The finite-controller support-set recurrence forces any deterministic projected suffix to be ultimately periodic. This contradiction excludes arbitrary stochastic command and update kernels, including mixtures inside a class. It does not assert that arbitrary finite Markov chains have rational stationary frequencies.

For sufficiency, a common-power relation and bounded relative logarithmic scores give a finite coset orbit for each consistent-priority word. This is a classical cyclic-search consequence. The mixture is compiled through one prescribed initial label and command-conditioned updates into disjoint counted tail controllers. Zero-probability first-command rows are unreachable and are assigned arbitrary updates. There is no persistent external random seed or free clock.

The quantitative prior bound is proved by deletion rather than assumed: the optimal expected call bound supplies a positive chance of an early occurrence of each command; removing it saves at least g in every other model. A finite restricted-search prefix and the common fallback yield pi_i>=delta by the saddle inequality. This controls the logarithmic spread by primitive data. At most n length-T word prefixes plus fallback use at most nT labels, yielding B*A*kappa^floor(M/n). For rational primitives, a prime-vector criterion and an explicit finite relative-coset count give a sufficient cap and inherited algebraic synthesis. Constants are conservative; no matching lower approximation rate, minimal cap or efficient algorithm is inferred.

The prior and rate bounds allow arbitrary positive costs. The special two-location normalized constants below are retained as a sharper refinement, and are not the scope limit of the main theorem. The classification excludes perfect or impossible detection endpoints and zero costs; no unproved extension to these changed experiments is asserted.

## Load-bearing two-location saturation chain

The word-law reduction separates private planned commands from physical failure probabilities. For a fixed command prefix, the physical likelihood is independent of the private route that generated it. This justifies a model-independent planned-word measure and model-dependent cost weights; it does not impose the old model-independent herald condition.

The greedy index, attained interior least-favorable prior, equalizer risk and two consistently tie-broken extreme sequences are classical search results, explicitly credited to Blackwell/Matula and Clarkson–Lin–Glazebrook. Their self-contained proof uses finite adjacent exchanges, a bounded logarithmic strip, compact cylinder laws and finite-dimensional separation. It does not invoke an unjustified hard-memory minimax interchange. The convexified object is the unrestricted word-law class; the hard-M class remains nonconvex.

For arbitrary positive command costs, an attaining robust law has strict excess over each known-model cost: properness in the other model forces a wrong command at some finite prefix with positive likelihood in both models. This excludes endpoint separating priors. At an interior prior, expectation of a nonnegative Bayes excess forces support on the entire set of optimal words.

When the logarithmic failure ratio is irrational, at most one tied pair can occur. Every optimal word has the same deterministic nonperiodic suffix with irrational frequency. The finite-controller obstruction is a recurrence on positive label supports, not an assumption that internal states are deterministic functions of observations. Arbitrary stochastic updates and fresh coins are included.

When the ratio is rational, the bounded logarithmic orbit lies in a finite coset. A fixed tie rule therefore has an ultimately periodic realization. The robust mixture is implemented from a single pure initial label by its actual command row and command-conditioned branch update; disjoint tail labels carry the persistent branch choice. The initialization is paid in the count. The prefix approximation includes every position and the fallback. The explicit rational-data cap uses exact prime factors and rational inequalities, avoiding an oracle for the least-favorable transcendental prior.

The dichotomy holds only in its stated imperfect-search family. The explicit two-location exponential constants and efficient-in-label prefix count have their stated cost normalization. They are not matching lower approximation rates or minimal-state formulas.

## Independent internal challenges and finite diagnostics

The author team performed separate AI proof reads and algebraic cross-checks. Source-pinned records are retained under `provenance/R80_*CHALLENGE*`, `provenance/R80_INTERNAL_CROSS_AUDIT.md` and `provenance/R80_ARITHMETIC_INDEPENDENT_CHECK.md`. These records preserve discarded exploratory formulas and their mathematical replacements. They do not impersonate outside experts, and their SHA-bound scope is not silently broadened by later layout changes.

`diagnostics_r80_sharp.py` independently checks exact symbolic identities, quadratic-field constants, an arbitrary six-parameter rational grid and explicit repaired chains. Its high-precision samples evaluate only the constructive upper family. They do not numerically certify global positive-epsilon optimization.

`diagnostics_r80_arithmetic.py` uses exact rational arithmetic for adjacent exchanges, finite fixed-count word order, general-cost one-label values, independently solved product chains, counted pure-start mixtures, commensurate cycles, powered tail comparisons and the prime-exponent test. Its finite irrational-word sample is only a diagnostic; the written irrationality and finite-support proof establish the infinite conclusion.

`diagnostics_r80_general_search.py` independently checks exact rational n=3/4 exchanges and signed tie functionals, 48 prefix-mixture and 22 complete periodic-mixture controllers through assembled product chains, 32 finite-coset/resolvent comparisons, deletion/prior inequalities, powered tail bounds, effective caps, prime vectors and partial commensurability. The 24,254 finite checks do not prove infinite nonperiodicity; that conclusion follows from the projected-word argument. Its source-pinned separate AI audit is `provenance/R80_GENERAL_SEARCH_INTERNAL_AUDIT.md`.

All 29 inherited diagnostic suites remain byte-identical and are rerun. The strict receipt gives actual current suite/check counts and ordinary/optimized equality. A disabled Python `assert` cannot supply a passing check. No finite grid, floating tolerance, numerical optimization or search result replaces a quantified proof.

## Preserved proof boundaries

The general cost framework retains a positive mean cost floor, all-initial-state robustness, a fixed hidden model, a finite declared interface and mandatory success stopping. Same-label restart is classical memory reset only. A support-dependent witness is an offline certificate, not a hidden model input. Uniform witnesses are obtained by the proved regularization, not assumed for the original controller.

The stronger reported-reset normal form retains its all-state quantifier and known reset states. Arbitrary Bellman ties are allowed there, but the simpler action-cover threshold still needs exposure. Shared-preparation mean assumptions, the physical-dictionary Born/Diophantine hypotheses, local geometric strata, hard-width nonconvexity and the distinction between bounded performed-law scores and unbounded duration remain unchanged.

The original general-M noisy-qubit risk, unrestricted-decoder rate gap, intermediate timing, arbitrary optional commitment, unknown-model predictive quotient and independent Theta goals remain open at their stated scopes. No source audit closes a mathematical research question or a journal contribution objection.

## Execution categories

The final publication receipt separates: ordinary written proofs; exact finite algebra; floating finite probes; native compilation and layout inspection; source/history authentication; hosted workflow readback; human assessment; and editorial decision. The strict local verifier authenticates its actual source SHA, checks every active locator, compiles the paired article and supplement plus companion, and records unchanged source trees. An old hosted success cannot be reported as current execution. Historical failures remain failures at their original source identities.
