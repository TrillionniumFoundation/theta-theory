# Response to the thirtieth referee report

**General Theta Foundations I — Revision 49**  
**Sign and Magnitude Duality for Numerical Word Realizations**  
27 September 2026

Controlling report: `reviews/general-theta-foundations-i-v46-certified-positive-realization-harsh-top4-r30-2026-09-27/REFEREE_REPORT.md`, pinned at `6ecf57a2d7ce804352f85daead8ec38e56377631`. It reviews v46 at `d7914880e7df679756c3b6ae86311485ac922f8a`. The completed v47 publication `98b59f3f45f63dacd8dba8cf132d23e54e7596e8` is the mathematical/source ancestor of this revision; its two-state results are inherited, not retrospectively attributed to r30 or claimed new. A distinct v49 branch was created remotely before the new sources were published. The pre-existing v48 work is not overwritten.

The report's main mathematical request is a structural certificate excluding whole realization classes, not another test of a supplied candidate. The present revision completes the two-state antisymmetric class and exhibits an exact positive-error optimum at a nonzero horizon with different commands. It retains the earlier general Hankel, Gram, moment, arithmetic and bit-implementation results rather than substituting a narrower assertion for any of them.

Stable labels below are resolved to theorem numbers and pages in the executed `THEOREM_LOCATIONS.json`.

## Structural infeasibility rather than candidate verification

**Addressed by `lem:support49`, `thm:duality49`, `thm:algebraic49` and `prop:tight49`.**

The inherited v47 scalar normal form reduces every all-two-label machine, without a free symmetrization coin, to a bounded product over seed, command epoch and query factors. The new support lemma handles the points where a target entry equals the proposed tolerance. Active entries force a finite set of nonzero factor coordinates and explicit lower magnitude bounds. All other factors may be set to zero without increasing the permitted error. This is necessary for a correct logarithmic formulation; simply declaring all factors positive would omit legitimate boundary optima.

Within each compatible factor-sign chamber, exact absolute mean-error intervals become a bounded linear system `Cy<=log b`. Nonexistence is equivalent to a nonnegative integer vector z with `z^T C=0` and `product b_i^z_i<1`. At most v+1 inequalities are needed in one chamber. Global infeasibility requires excluding every compatible chamber, or a verified sign contradiction; the article does not convexify across chambers by giving a free persistent selector.

The coefficients are integral, and on each threshold stratum the bases are positive algebraic affine functions or their reciprocals. A finite enumeration of certificate rays and univariate root isolation determines the exact optimum. Algebraic stochastic witnesses are recovered from vertices of the logarithmic polytope. This is a finite structural algorithm for an explicit tensor, not a polynomial procedure in a compressed horizon and not a theorem for arbitrary widths.

The accompanying rational threshold checker does not compare approximate logarithms. It retains exact rational linear combinations of logarithms and clears exponents to compare rational products. Fourier--Motzkin elimination preserves nonnegative proof multipliers; paired equality constraints are eliminated by exact substitutions using their opposing inequalities. The verification routine reconstructs the constraint system from the supplied target, checks input binding, and verifies coverage of every sign chamber. Resource exhaustion is reported as undetermined. The full symbolic optimizer is proved in the article; software claims are limited to implemented threshold decisions, rational bisection and the worked algebraic example.

## A fully worked nonzero-horizon optimal error

**Addressed by `thm:cubic49`, `prop:orthogonal49`, and the retained v47 frontier.**

The cubic example is a rational 2-by-2-by-2 positive-seed mean tensor, with negative seeds appended. Entries of Hamming weight 0,1,2,3 are respectively 1/10,2/5,4/5,2/5. The two commands have different prescribed responses. Every decomposable tensor obeys `g011*g101*g110=g000*g111^2`. At mean tolerance delta this forces

```
(4/5-delta)^3 <= (1/10+delta)*(2/5+delta)^2.
```

The unique root t of `500t^3-375t^2+540t-124` is the exact critical mean error. Factors `( (1/10+t)^(1/3), (2/5+t)^(1/3) )` in each mode give legal stochastic initialization, command rows and terminal columns attaining it. The five-entry multiplicative identity proves optimality against every machine; a positive Gram residual merely verifies that this supplied machine is not exact. Those two roles are deliberately distinguished.

Irreducibility modulo seven proves t irrational. Consequently, for rational signal, no rational machine at this profile attains the positive optimal error, although dyadic machines exist below every prescribed larger tolerance. This is a directly proved positive-error rational/real separation, not an inference from the literature on fields of exact nonnegative factorizations. Exact rational root brackets, a strict lower certificate and a dyadic upper machine are included.

The second example is an actual rational orthogonal experiment, with identity and coordinate swap, two rational unit seeds and their negatives. Its exact all-two-label error is rho/20 for every positive horizon. The same lower value survives two distinct two-label cuts with arbitrary intervening widths. This magnitude obstruction is not claimed invisible to every static flattening. The inherited quarter-turn theorem supplies the genuine separately-feasible/jointly-incompatible frontier and remains unchanged.

## The direct approximation literature and novelty boundary

The paper now compares Gillis–Shitov, Lemmas 1–2 and Theorem 3, and Morozov–Smirnov–Zamarashkin, Theorem 5.3. Fixed-sign matrix Chebyshev feasibility and threshold-active support deletion have direct prior antecedents. Logarithmic monomial linearization and fitting by threshold bisection are explicit in Boyd–Kim–Vandenberghe–Hassibi. Farkas' theorem is used in its classical form. These mechanisms are not presented as discoveries.

The new theorem supplies the full bounded multi-epoch tensor alternative, including signs and zeros, the finite multiplicative certificates and their stochastic reconstruction. The worked cubic frontier demonstrates information beyond sign consistency or a candidate residual. The article's comparison table separates prior problem, assumptions and current conclusion. A direct transfer of the matrix theorem identifies an NP-complete one-epoch binary-query input model with variable seed and command alphabets. It is labelled a corollary of prior work, not a fixed-dimensional orthogonal or multi-epoch NP-membership theorem.

## Encoding contract and rational-height requirement

**Addressed in `sec:encoding49` and `lem:grambits49`.**

Horizon is unary and the stochastic candidate is explicitly displayed for polynomial candidate-verification claims. Rational coefficients have binary numerator/denominator encoding. Algebraic coefficients include defining polynomials and isolating intervals; arbitrary-real oracles are not assumed. All augmented block dimensions are now explicit. A common-denominator monomial count bounds every intermediate Gram and backward-witness bit length by a polynomial in displayed input and horizon. Higher moments have their separate numerical-p and fixed-dimension dependence.

The global two-state alternative instead receives the complete finite response tensor. Its chamber count and ray enumeration can be exponential, and its boundary polynomials can have high degree. The executable checker has explicit stopping limits. None of these facts is replaced by a real-arithmetic operation count or by a generic quantifier-elimination slogan.

## Precise retained statements and requested wording repairs

The current copy of the finite-certificate section uses absolute even moments, distinguishes the scalar cardinality from the rational field symbol, samples a minimizing algebraic machine in the endpoint fiber, and states dyadic approximation as existence below every strictly larger tolerance. It does not assert that every larger real error is itself attained by dyadic rows. The nonnegative-factorization comparison concerns exact field dependence at a minimal inner dimension, not an unproved rational-error optimizer claim. All modifications are registered in the preservation manifest; original v46/v47 files remain unchanged.

The all-word Gram theorem checks a legal proposed candidate. Its existential version and the moment minimization concern unknown candidates and do not have the same algorithmic cost. The moment inequalities remain valid, inherited norm comparisons; the arithmetic-grid theorem remains a general compact optimization tool. Neither is counted as the new structural dual theorem. The two-state theorem is the class where the new certificate is complete; higher-width realizations retain their earlier existential characterization without a fabricated complete Farkas alternative.

## Exact-head validation and publication

The branch-specific workflow separates source restoration/publication, read-only validation of that exact source commit, and artifact publication. The validation job has read-only repository permission. The final job checks that the work ref still equals the validated SHA, stages only generated files in the new package and the new root entry, and uses a non-force atomic push to the work and referee-ready refs. Source publication and final publication suppress retriggering; a concurrent ref change causes refusal rather than overwriting. A clean rebuild from the isolated core archive must agree page-by-page with the validated article. An earlier failed run is not relabelled successful.

The build binds the exact source, controlling report and v47 ancestor independently. It exercises the inherited v44 and v47 programs and the new v49 program in ordinary and optimized Python. Counts are recorded only after execution. Negative controls include altered input bases, omitted sign chambers and invalid multipliers, not merely candidate row normalization. No test claims to establish the universal theorem or external priority.

## Preservation and historical pipeline

The current article loads all v47 substantive mathematical modules. Its two earlier introductions are retained as original source files. The complete published v47 article and its cumulative mathematical/development volumes are copied or appended unchanged. Large archives are excluded from the compact journal-facing package. No prior work/review path or unrelated branch is modified.

The Round-Seventeen ledger was read at the r30 SHA. Its A2–A3–A4–C2–D1 and B2/B1/B3/B4/C1/C2/D1 dependencies retain their separate Fourier/local-limit, stopped-LDP, global-kernel, nonlinear-semigroup, graph-core, filtering and optional-projection proof obligations. The finite two-label certificate does not discharge those analytic gates. The program title is retained with a precise mathematical subtitle; no editorial outcome follows from it. The response is the added complete finite-class duality and exact stochastic frontier, not a no-go replacement or a change of journal target.

## Scope of the next review

The main items for independent scrutiny are the support reduction at zero thresholds, completeness across all sign chambers, sparse integer certificates, algebraic recovery at the optimum, and the cubic lower/upper witnesses. General higher-width structural duality, all finite orthogonal width frontiers and external priority certification are not asserted. The new finite-class proofs, code and exact-source artifacts are provided for that scrutiny.
