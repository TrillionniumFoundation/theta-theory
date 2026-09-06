# Mathematical audit of A1 v13

Pinned submission: `fc6465b86fbc7ee6a4e8f3ccfb54ea32a64dc8b6`. Source paths below are relative to `papers/A1-english-v13/`. The identifiers S0–S9 and L1–L4 resolve in `SOURCE_INDEX.md`. This is a proof audit, not a formal verification certificate.

## A1. The inherited geometric input

### A1.1 Normalization and attainable dimension

The one-step likelihoods lie in W=span{1,t^{a1},…,t^D}. The fixed coefficient matrix has full column rank, so a bounded right inverse converts an interior coefficient perturbation around the constant failure factor into actual commands. The commands realizing a fixed coefficient vector are common across calibrations; the functions they realize vary with the exponents. Positivity is uniform on the fixed compact chamber. [S2]

For distinct small c_i, the all-failure product of (1+c_i t^D)/2 has tangent span supported at

`{jD: 0<=j<=n} union {a_i+jD: 1<=i<r-1, 0<=j<n}`.

There are n(r−1)+1 distinct exponents: different translates occupy disjoint D-sized intervals, and the interior one-step exponents remain strictly between 0 and D. This explains why arbitrary collisions among future sums do not force collisions in the chosen past tangent basis.

Mixed moment matrices pair these tangent monomials with future test functions. The integration-of-determinants identity and the same-sign generalized Vandermonde determinants give strict positivity under any fixed full-support prior. The product likelihood itself lies in the tangent space. Normalizing by evidence therefore removes exactly the constant direction and gives rank min{n(r−1),h_A(m)−1}. This is the relevant attainable dimension, not the ambient number of formal coordinates. [S2]

### A1.2 The flag through exact collisions

For the formal positive future nodes x_alpha=(alpha·a)/H, a finite Leja order gives scales d_j, with d_1=1 and subsequent d_j products of previous gaps. Since all normalized gaps are at most one, the scales are nonincreasing. The Newton evaluation matrix, divided columnwise by positive pivots, has bounded entries, a triangular leading block, and bounded inverse in fixed dimension. Zero pivots are assigned zero columns rather than inverted. Products d_1…d_l and the maximal l-node Vandermonde product V_{m,l} are comparable by fixed factorial factors. [S3, lines 77–143]

At a repeated-node limit, a complete Newton prefix becomes a complete Hermite system. It is not an arbitrary selection of isolated high derivatives. Adding the constant gives a complete exponential-polynomial Chebyshev system. The positive-node lower bound makes all functions t^a(log t)^k and the finitely many needed parameter derivatives bounded near t=0. The confluent mixed pairing with the separated past tangent basis stays full rank.

There are finitely many label orders. On compact closures of the regions for those orders, divided differences extend continuously and the corresponding normalized row rank never vanishes. A compactness argument gives a uniform least row singular value. Uniform local inversion, retaining a box in the kernel variables, gives an attained cube for every truncated flag. The all-failure event has probability bounded below by a fixed positive likelihood power, so the push-forward is an unconditional subprobability minorization rather than merely a conditional geometric set. [S3, lines 145–222]

This is the strongest nontrivial geometric step in the examined manuscript. Its proof is not replaced by an estimate on a Vandermonde matrix alone.

### A1.3 Why the global cover is a separate valid input

For each fixed model, posterior raw moments are rational functions of command coordinates with positive evidence denominators. The prior integrals are real coefficients; the prior need not have a semialgebraic density. Normalizing each factor removes its irrelevant scalar and bounds the image dimension by n(r−1). Bounded degrees, numbers of coordinates, and quantifier elimination give a coefficient-independent semialgebraic format bound. No semialgebraicity of the calibration set K is inferred or needed. [S3]

For a bounded-format set S in a rectangle with decreasing widths a_1,…,a_q and dimension at most p, generic codimension-j sections have a bounded number of components, and those with j>p are empty almost everywhere. The j-dimensional projection of the rectangle has volume at most a fixed multiple of a_1…a_j. The real Vitushkin inequality therefore gives

`N(S,epsilon) <= C sum_{j=0}^p epsilon^(-j) a_1...a_j`.

Its M-center inversion yields the maximum of the truncated product scales. This is a global image estimate, not an assertion that a local coordinate cube covers the image. The cited real inequality and bounded-format regularity input were checked in L1–L2. [S3]

The fixed symbolic query matrix has full column rank even when exponent values coincide. Coincidence restricts the physically attainable vectors, not the column rank of the formal polynomial change of basis. Projection of arbitrary decoder outputs onto this query span allows the geometric lower argument to apply to arbitrary M-message decoders. The attained scaled cube supplies the lower volume estimate. Taking the best prefix length gives Xi_N.

### A1.4 Causality and the source of fixed-horizon constants

The formal raw-moment update uses only moments of the current remaining degree. On the segment joining two attainable states, its denominator is a report probability under a posterior mixture and is at least kappa. Differentiating the quotient gives a gap-independent Lipschitz bound. Updating a representative history produces another attainable history, so the next codebook is used on its actual domain. [S3, lines 294–354]

If E_n is the raw error and e_n is the stage covering scale, the recurrence is

`E_0=0; E_(n+1)<=L_n E_n + C e_(n+1)`.

At fixed N this gives squared query error O(max_n e_n^2). Conversely, every causal state index is an M-message encoder at that checkpoint, and the common independent exploration law supplies all checkpoint lower bounds. No access to the original history is granted at runtime. The constants need not remain bounded as N increases; no infinite-horizon conclusion follows from this recurrence.

## A2. The new uniform common-name ambiguity

Let c_- mu_0<=mu<=c_+ mu_0, with a fixed interior margin lambda. Put z=t^{a_1}, f=z−mu(z), epsilon=delta/2. Because mu(f)=0 and |f|<=1,

`mu_±=(1±epsilon f) mu`

are probability measures for epsilon<=1/2. The measure perturbation is bounded by epsilon c_+ mu_0. Hence epsilon c_+<=lambda suffices to keep both measures in the outer envelope. Every formal monomial v belongs to [0,1], so

`|mu_±(v)-mu(v)| = epsilon |mu(v f)| <= epsilon`.

The center-name error at most delta/2 and epsilon=delta/2 put both models in the same radius-delta consistency class. Their calibration can be the center calibration itself, even at a collision intersection. [S5, lines 140–210]

For a history w with likelihood L_w, let nu_w be the posterior under mu. Directly,

`nu_(w,±)(q) = [nu_w(q) ± epsilon nu_w(q f)] / [1 ± epsilon nu_w(f)]`.

Subtracting gives the exact identity

`nu_(w,+)(q)-nu_(w,-)(q) = 2 epsilon Cov_(nu_w)(q,f) / [1-epsilon^2 nu_w(f)^2]`.

The denominator is positive and no bigger than one. If w has n reports, L_w>=kappa^n and its evidence is at most one, so nu_w>=kappa^n mu>=kappa^n c_- mu_0. Using the infimum characterization of variance,

`Var_(nu_w)(z) >= kappa^n c_- Var_(mu_0)(z)`.

Continuity on the compact exponent chamber and full support give v_0=min_a Var_(mu_0)(t^{a_1})>0. For m remaining trials, the actual ordered query F_1 F_0^(m−1) equals

`q = 2^(-m) + beta 2^(-(m-1)) z`.

It is one member of the uniform r^m-element menu. Its posterior separation is at least

`2 epsilon beta 2^(-(m-1)) kappa^n c_- v_0`.

The observation laws satisfy P_±>=(1−epsilon)P_0 because the latent-prior density factors do. They are not equal in general. For a single conditional prediction kernel A used in both models,

`[(A-p_+)^2+(A-p_-)^2]/2 >= (p_+-p_-)^2/4`.

Integration against the common lower measure and selection of the displayed query gives average risk at least

`delta^2 r^(-m) beta^2 2^(-2(m-1)) kappa^(2n) c_-^2 v_0^2 / 8`.

Finite minimization over checkpoints gives a uniform positive constant. Independent randomization of the rule does not alter the squared-loss inequality. This proves the examined delta-squared lower term even with full-history access. It uses prior ambiguity in a uniformly observable direction, not a claim about calibration-only uncertainty. [S5, lines 95–210]

## A3. How much of the joint theorem is a general transfer argument?

Consider the following four properties, with constants uniform over the declared family:

1. At a center theta_0, every M-state rule has risk at least c Phi(M,theta_0).
2. One program constructed from a common name has worst-model risk at most C(e(M,theta_0)+delta)^2.
3. The relevant covering scale obeys e(M,theta_0)^2 comparable to Phi(M,theta_0), and remains stable within the common-name class.
4. Two models within that class force risk at least c' delta^2 for a common rule, even without a memory restriction.

Then the common-program minimax risk is comparable to Phi(M,theta_0)+delta^2. Indeed, the lower bound is the maximum of the two separate lower bounds, which is at least half their sum after reducing the constant. The upper follows from (e+delta)^2<=2e^2+2delta^2. There is no additional mixed term requiring a different asymptotic profile.

In v13, property 1 is the inherited intrinsic theorem; properties 2–3 come from v12's common-advice construction, paired-history estimate, and dominated-family uniformity; property 4 is the new physical tilt argument. The comparison of center and other compatible models is valid because both lie near the same name. The algorithm takes the name, not the center. This explains both the validity of the new theorem and the referee's limited assessment of its additional geometric content. [S4–S6]

The transfer calculation is not a cited external theorem or a priority claim. It is an explicit logical decomposition of this manuscript's proof. Its hypotheses do real work: without interior name slack property 4 can fail; without attainability property 1 need not use the claimed exterior profile; without the numerical interface property 2 is not an algorithm.

## A4. Saturation and the five-trial arrangement

From the definition Xi=max_(n,l)(V_(N-n,l)/M)^(2/l), each inequality Xi<=delta^2 is exactly equivalent to M>=V_(N-n,l) delta^(-l). Taking the maximum gives the stated profile threshold. Integer budgets require a ceiling. This is exact algebra for the profile; comparison constants in minimax risk remain comparison constants. [S5, lines 256–307]

For A={0,1,2+u,3+v}, N=5, the n=3,m=2 future exponents split into six separated groups, three doubled. Their small gaps are |u|, |v−u|, |v−2u|. In decreasing order, the largest two are comparable to rho=max(|u|,|v|), while the smallest is tau. Thus V_l is comparable to one through l=6, rho at l=7, rho^2 at l=8, and rho^2 tau at l=9. The l=7 term is interpolated by the l=6 and l=8 terms. Other checkpoints have attainable dimension at most six. [S3, lines 479–558]

The noisy risk is therefore comparable to

`max{M^(-1/3), rho^(1/2) M^(-1/4), (rho^2 tau)^(2/9) M^(-2/9), delta^2}`,

and its threshold has order

`max{delta^(-6), rho^2 delta^(-8), rho^2 tau delta^(-9)}`.

On u=theta, v=theta+theta^k, the switch accuracies have orders theta and theta^k. The three threshold orders are delta^(-6), theta^2 delta^(-8), and theta^(k+2) delta^(-9). These substitutions are valid also when an exterior term vanishes; no logarithm of zero is used. They do not establish exact constants or a numerical program-size lower bound.

## A5. What the request checker actually certifies

The request is fixed before synthesis. It binds T, alphabets, M, coordinate/query schema, precision v, raw-error allowance sigma, total allowance tau, and the complete finite numerical name. It requires sigma+2^(-v-1)<=tau. The returned object is checked against these independent data, not used to define them. [S7]

Conditional on the raw numerical accuracy and command-net assumptions, the independently reconstructed finite radius r_n satisfies

`max(0,r_n/2−tau) <= e_n(M) <= r_n+A_n h+2tau`.

Nearest-center transition checking supplies the same finite-horizon recurrence as the mathematical compiler. It does not certify an arbitrary external oracle, all imaginable malicious Python behavior, or the truth of a hash-identified model. This is why the ten rejected request faults close the v12 precision/horizon findings without making an unlimited verification claim.

## A6. Executed probes and build

`reproduce_review.py` imports only the production compiler modules. It reconstructs the interval truth and physical exponent-keyed integration separately, verifies the pinned source manifest and every listed source file, tests four nominal brackets and ten request mutations, and compiles one physical M=64 program from one common imperfect table. It uses the entire finite two-command/four-report acquisition alphabet through two stages. At this budget the true finite-history covering radius is zero, so the floor-only stop is an independently known positive control rather than a fitted covering oracle.

The executed result has 4,909 assertions and ten rejected faults. At the physical stop, b=11, h=1/2048, the stage counts are (1,8,64), and rho=1451520/1943011333. Exact per-model discrepancies and all relevant metadata are deposited in `INDEPENDENT_PROBES.json`. The four author-suite reruns and separate three-pass PDF rebuild are recorded in `EXECUTION.json`. The artifact omissions and finite-domain limitations remain explicit.
