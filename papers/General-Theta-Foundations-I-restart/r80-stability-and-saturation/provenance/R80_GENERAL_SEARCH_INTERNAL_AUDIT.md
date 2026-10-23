# R80 finite-search theorem: internal mathematical challenge

## Identity and scope

This is an internal author-team proof challenge by a separate assistant agent. It is not an independent human referee report, formal proof verification, mathematical-priority clearance, or editorial assessment.

The source read in full for this audit is `59-finite-search-saturation.tex`, SHA-256:

`3220cac3bd7ab6220d96eb3115e006ff040959098cc4171513a9b1aa9f70cd9d`.

The audit concerns the displayed scalar search family with a finite number `n >= 2` of fixed hidden models, `n` commands, strictly positive deterministic costs `c_i`, strictly interior matching failure probabilities `0 < r_i < 1`, one failure report, compulsory success stopping, autonomous fixed stochastic command/update kernels, and a prescribed counted pure initial label. It makes no assertion that the arithmetic classification extends to arbitrary quantum instruments, zero call costs, matching failure probabilities equal to zero or one, or free external clocks/private memory.

**Finding:** no substantive mathematical gap was found in the seven declarations or their complete proofs at the source hash above. The qualifications and classical attribution in the draft are appropriate. The numerical constants are intentionally conservative sufficient bounds, not optimal constants or minimal memory thresholds.


### Final-source change boundary

The complete mathematical proof was initially reviewed at SHA-256 `8e48af95faf9f8ce8c563b3d9b9d51c8fce408881ece30eee68e8ba74c31b053`. The final source above differs only in five checked text blocks: the saturation theorem title now says “for any finite number of locations”; the initializer explicitly restricts division by p_a to p_a>0 and assigns unreachable p_a=0 update rows arbitrarily; the prior-constant display uses `aligned` in place of `split`; and the rate-constant and rational-cap displays are wrapped across two lines. The intermediate title/convention/wrapping version had SHA-256 `ad5e939156204c372d76bc587a36b6c2169f705012133ba89a43f6aaf6653dbd` before the native LaTeX alignment correction.

These changes were read and checked. As an exact change-boundary verification, reversing those five specified blocks in memory recovers the original reviewed source SHA-256 `8e48af95faf9f8ce8c563b3d9b9d51c8fce408881ece30eee68e8ba74c31b053`. Thus no additional source change is being silently covered by this repin. The zero-probability-row convention is consistent with the previously tested explicit controllers and makes the counted initialization definition complete. No theorem hypothesis, conclusion, formula, constant, proof inference, or dependency has changed. The diagnostic script and both completed result files remain unchanged; no rerun or extra mathematical test is claimed for this repin.

## Statement-by-statement review

### 1. `lem:r80-finite-search-one-label`

The one-call expected cost is `sum_i tau_i x_i`, where `x_i=p_i q_i`; the model-i expected total cost is that common numerator divided by `x_i`. If some `x_i=0`, that model has infinite cost because call costs have a positive lower bound. The lower bound `V_1 >= sum_i tau_i` is immediate from `x_i >= min_j x_j`. The proposed row makes all success masses equal and attains the bound simultaneously in every model. This works with arbitrary positive command costs; no normalization `c_i=q_i` is needed.

### 2. `lem:r80-finite-search-saddle`

The planned-word reduction is valid: conditional on a command prefix, its physical failure likelihood is the same for every private realization of that prefix. Thus conditioning does not leak the hidden model into the command kernels. Positive matching failure probabilities are essential here and later.

The adjacent exchange vector was recomputed directly from the two orders. Components other than i and j are unchanged, because only the order of the two costs changes and their model-specific survival factor is unchanged. The Bayes exchange coefficient is exactly `c_i c_j (a_j r_j^k_j-a_i r_i^k_i)`.

The finite bubble-sort argument compares a finite prescribed greedy prefix with the full nonnegative cost of a finite-cost competitor. Every required next letter occurs eventually because finite cost in every model forces every letter to appear infinitely often. The argument does not assume that an infinite sequence of swaps itself preserves an infinite series. Strictly incorrect choices admit a finite strict improvement. Uniform geometric tails are then proved independently from bounded log-score spread, establishing finiteness of every greedy word and justifying subsequent limits.

The robust upper cost set is convex, upward closed, and closed by compactness of word laws plus convergence of each bounded continuous finite-prefix cost. Its finite-dimensional separation from the strict lower orthant supplies a nonnegative least-favourable prior. Full support is proved rather than assumed: deleting all commands outside the prior's support strictly reduces its weighted cost; finite prefix completion by the common proper fallback converts this deletion into admissible competitors in all models. This also proves all robust optima equalize all model costs and are supported on greedy words.

The support-function argument for at most n consistent-priority words is valid even for signed linear functionals. At a tied level z, the exchange changes a functional by `c_i c_j z (lambda_j/pi_j-lambda_i/pi_i)`. Hence the same descending priority of `lambda_i/pi_i` minimizes every tied block. Uniform tails justify sorting successively more blocks and passing to the limit. Compactness of the greedy risk image and finite-dimensional separation put it inside the convex hull of the n! consistent-priority risks. The Bayes hyperplane has affine dimension at most n-1, so elementary affine elimination leaves at most n words. These are classical search ingredients, not the manuscript's claimed new resource theorem.

### 3. `lem:r80-projected-word-rigidity`

The support of the planned label distribution evolves by a fixed deterministic map on nonempty subsets: union all positive command/update transitions. If the projected class is prescribed at time t, every positive command in every reachable label must belong to that class. The class therefore depends only on that support set. Finitely many support sets imply eventual periodicity. The lemma permits stochastic command rows within a class and stochastic label updates. Its hypothesis correctly requires one fixed finite onset time for the deterministic projected suffix.

### 4. `thm:r80-finite-search-saturation`

Necessity correctly handles partial commensurability, rather than assuming all pairs are irrational. Between two different rational commensurability classes, any two geometric streams can share at most one tied pair. There are finitely many pairs of streams, and each positive level has finite rank in their merged ordering. Beyond a single finite cutoff all ties are within classes, yielding one deterministic class suffix for all greedy laws.

Class frequencies are positive and have the form `H_C/H`, with `H_C=A_C/u_C` and `A_C` positive rational. Distinct class-frequency ratios are irrational. An eventually periodic class word has positive rational frequencies and rational ratios, contradicting the projected finite-state rigidity lemma. The inherited finite-budget attainment theorem is correctly used to convert nonattainment into the strict gap `V_M>V`; nonattainment alone would not imply this without attainment.

For sufficiency, rational commensurability gives `u_i=h_i ell`. Each relative log score belongs to a fixed lattice coset and a bounded interval. The relative tuple determines the next command, tie choice, and next tuple under a fixed priority, hence gives a finite deterministic automaton. A mixture of at most n words is implemented by one pure initial label: choose its first command with the correct aggregate probability, then conditionally choose the tail branch after failure. The physical failure probability of that first command is common to all branches with that command, so the conditional weights are correct in every model. Branch identities are stored in explicitly counted tail labels. No free initial random label or external seed is used.

### 5. `lem:r80-finite-search-prior-cap`

The constants are valid with arbitrary positive rational or real costs:

- `T0=ceil(2B/c_min)` makes success by call T0 have probability at least 1/2 for every model under a robust optimum, since its expected call count is at most B/c_min.
- In model i, success by that time implies that the planned word's first i-command occurs by then. Thus that planned event has probability at least 1/2.
- Under any other model j, that first omitted i-call has survival at least `r_min^T0` and cost at least c_min. Deleting all i-commands therefore saves at least `g=c_min*r_min^T0/2` in every other model. Retained survival factors are unchanged by the deletion.
- The restricted problem truly uses only the other commands. An attaining restricted law exists by the same word-law compactness argument, including the one-model case.
- Truncating it after `T1=ceil(2B^2/(c_min*g))` calls and switching to the B-cost fallback gives other-model costs at most `V-g/2` and the omitted model cost at most `K=c_max*T1+B`.
- The least-favourable-prior inequality then gives `pi_i >= (g/2)/(K-V+g/2) >= g/(2K)=delta`. The last comparison requires `V>=c_min>g/2`, explicitly supplied in the proof. The denominator is positive because `K>=B>=V`.

### 6. `thm:r80-finite-search-resource-bounds`

The prior bound implies initial log-score spread at most `L=log C`, where `C=tau_max/(delta*tau_min)`. Greedy spread is at most `R=max(L,u_max)`. The weighted log-score mean increases by exactly `1/H` per command, yielding model survival at most `A*kappa^T`, with

`A=exp(R+L)=C*max(C,1/r_min)` and `kappa=exp(-1/H)`.

The rational expression for A is exact, not a floating approximation. Replacing the tails of an optimal mixture of at most n words by the common fallback costs at most `B*A*kappa^T`. One initializer, at most `n(T-1)` continuation labels, and one fallback label require at most nT labels because n>=2. Thus the floor in the stated bound is correct for every M>=n. The bound applies to commensurate and noncommensurate data alike. No matching lower rate is claimed.

### 7. `cor:r80-finite-search-effective`

For rational failure probabilities, positive rational collinearity of signed prime-exponent vectors is equivalent to the required logarithmic commensurability. Dividing one vector by the gcd of its entries produces a primitive integer vector; Bezout's identity ensures each other collinear integral vector is an integer multiple, so the common base is rational.

All constants used to select J are rational. The algorithm compares `t^(-J)` to C without evaluating logarithms or an unknown least-favourable prior. Each relative-score coordinate has at most `2N0+1` possible values in its bounded lattice coset, including both interval endpoints. Thus `N=(2N0+1)^(n-1)` bounds each deterministic tail state set and `M0=1+nN` counts the pure initializer and all copies. The inherited finite-budget real-algebraic synthesis theorem then makes `V=V_M0` algebraic and computable in this rational saturating family. This does not claim tractable complexity, minimal memory, or exact algebraic computation in the nonsaturating case.

## Independent finite diagnostics

Script: `diagnostics_r80_general_search.py`

SHA-256: `e176adba2c2a4906e530908fe6db3b662468baf9ce12f4a0d6194d8c4dbc9425`.

The standalone script uses Python's exact `fractions.Fraction`, direct word sums, independently assembled substochastic product chains, exact Gaussian elimination, finite enumeration, and prime factorization. It uses explicit exceptions rather than optimization-removable `assert` statements.

The completed normal run records **24,254 exact rational conditions**, zero floating conditions. Its checks include:

- 1,727 independently costed finite words in three- and four-location cases, grouped by fixed command counts; this is not a finite-horizon stopping claim.
- Adjacent exchange identities and two independently permuted tied blocks for signed support functionals.
- 48 counted pure-start finite prefix-mixture controllers, including degenerate mixture weights, compared with direct mixture cost formulas.
- 22 full eventually periodic mixture controllers, with the initial branch chosen only after the first observed failure, compared with exact geometric word sums.
- 32 individual finite-coset periodic automata, with separate product-chain and geometric-series evaluation.
- Exact one-label formulas with unequal positive costs.
- Deletion bounds on six symmetric exactly attaining mixture families and four uniformly proper one-label families with worst cost B.
- Exact scalar exclusion inequalities underlying the lower prior bound, including normalized and unequal rational costs.
- Rational powered tail inequalities through 120 commands. If `sum_i 1/h_i=a/b`, the identity `kappa^a=t^b` eliminates floating logarithms entirely.
- Prime-vector classification and partially commensurate three-/four-model examples whose projected class words coalesce while their command words continue to differ.

These are finite probes, not exhaustive tests of every controller or universal proof verification. The no-eventual-period claim is supported by the analytic irrational-frequency proof, not inferred from a long finite prefix.

Both the normal and optimized-Python executions completed with exit status zero. Their separately saved JSON outputs are byte-identical, SHA-256 `e8d5bebbd57429a9b03f108eefb5a8207c6785622f5074535d7d955e706b8409`. The integration pipeline must bind any claimed success to the exact source and script bytes it actually executes.

## Remaining limits

The new theorem completely classifies finite stochastic saturation within the displayed finite-search family and supplies explicit sufficient approximation/cap bounds there. It does not classify general instrument saturation or prove a quantitative positive lower gap from irrationality alone. The sharper two-location normalized constants remain useful and are correctly retained in Section 58. The literature attribution of classical greedy search, interior saddle/finite-mixture structure, and common-power cycles must remain intact. Whether these resource conclusions meet a particular journal's novelty and significance threshold remains an external editorial question.
