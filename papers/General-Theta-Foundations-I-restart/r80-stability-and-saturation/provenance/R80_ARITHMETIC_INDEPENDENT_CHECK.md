# Internal adversarial check of the R80 arithmetic saturation argument

**Disposition:** no substantive mathematical defect was found in the inspected argument, at the scope stated below. This is an internal AI-assisted author diagnostic. It is not a human referee report, a machine-checked formal proof, an editorial assessment, or evidence of publication-level novelty.

## Exact source and scope

- Checked file: `/tmp/theta-math-challenge/58-arithmetic-saturation.tex`.
- Final checked SHA-256: `eb24afb20c54ca916293324a74ecc0a8c193489bae58d1030d956400013897de`.
- The complete mathematical proof was reread at predecessor SHA-256 `b63de1ae344c92ea08e2952bd9293b1905606b964863e0b16b604a39c96d3b37`. Subsequent changes add the word “fixed” to the finite-time hypothesis of the support-rigidity lemma, identify Blackwell as the index-rule originator reported by Matula, and wrap the constants in a two-line display for native layout. The final hash and these nonmathematical changes were checked separately.
- Check date: 23 October 2026 UTC. The clock read during final checking was 13:10:44 UTC.
- Main statements inspected: `lem:r80-search-saddle`, `lem:r80-finite-word-rigidity`, `thm:r80-arithmetic-saturation`, `cor:r80-effective-saturation`, and `ex:r80-rational-nonsaturation`.
- Inherited dependency interfaces inspected in the current R80 copy: the assumptions, statement, and attainment/algebraic-synthesis argument of `thm:r79-quantum-frontier`, and the statement/construction of `cor:r79-history-limit`. This check does not re-certify every earlier theorem in the repository.

The class has two fixed hidden scalar models, two commands, one failure report, strictly positive failure probabilities on every finite command prefix, strictly positive deterministic command costs, compulsory stopping at success, and autonomous finite classical controllers with a prescribed pure initial label. The necessity-and-sufficiency theorem allows arbitrary positive command costs. The displayed explicit approximation constants and effective algebraic label cap are restricted to the normalized costs stated in the source.

## 1. Word laws and the unbounded cost objective

For any private randomization scheme, condition on a fixed commanded prefix along hypothetical failures. In either model the physical likelihood of that prefix's failures depends on the command prefix alone. It does not depend on which private random draws or internal labels produced that prefix. Thus conditioning on physical failures does not introduce hidden-model dependence into the conditional distribution of private routes given the commanded prefix. The planned word law is therefore legitimate for arbitrary history policies and for finite controllers with stochastic command and update rows.

Conversely, cylinder conditional probabilities implement any word law; arbitrary choices on zero-mass cylinders have no effect. The command space is finite, so no additional measurable-selection step is hidden here. Nonnegative summation gives the expected cost by Tonelli without exchanging a conditionally convergent series. The first call is included through the term with zero preceding calls.

The closed upward risk-set proof is appropriate for these unbounded costs. Cylinderwise convergence gives convergence of each finite truncation, and monotone convergence bounds the limit's full cost. The proof never treats expected duration as a bounded continuous function or deduces it from total-variation continuity. A proper full-support memoryless row supplies a finite feasible point.

## 2. General-cost exchange rule and its converse

Independently expanding the two orders after counts `(i,j)` gives

\[
C_0(ab)-C_0(ba)=-c_b(1-r)r^i,
\qquad
C_1(ab)-C_1(ba)=c_a(1-s)s^j.
\]

Hence the priority indices are precisely

\[
\frac{\pi q_a}{c_a}r^i=\frac{\pi}{\tau_a}r^i,
\qquad
\frac{(1-\pi)q_b}{c_b}s^j=\frac{1-\pi}{\tau_b}s^j.
\]

Moving a desired larger item left across repeated copies of the other command does not increase the Bayes cost. A strict index violation gives a strict reduction. Finite cost in both models forces infinitely many visits to both commands, so the desired next occurrence always exists. Finite exchanges preserve the later count vector; no infinite rearrangement theorem is being assumed. Comparing finite greedy prefixes against the full transformed competitor and passing to increasing prefix length proves optimality once finiteness is established. Thus the argument establishes necessity as well as sufficiency for every finite-cost word. An interior Bayes prior assigns infinite cost to a word that is infinite-cost in either model.

The logarithmic recurrence is correct for arbitrary positive costs:

\[
z_0=\log\frac{\pi\tau_b}{(1-\pi)\tau_a},
\qquad z_t=z_0-ui_t+vj_t.
\]

The invariant interval `[min(z0,-u), max(z0,v)]` holds also at ties. Solving with `i_t+j_t=t` yields the stated asymptotic frequency and the two exact exponential survival identities. These justify finite costs uniformly over tie choices at a fixed prior.

## 3. Attainment, separating prior, and the two extremal words

The disjoint open lower quadrant and closed upward risk set admit a nonzero separator. Upward closure and unboundedness of the opposite quadrant force nonnegative coefficients. The attained diagonal point forces the separating value to equal the robust value after normalization. This is a finite-dimensional separation argument; it does not assert convexity or a minimax theorem for a hard finite-label class.

The endpoint exclusion remains sound with unequal arbitrary positive costs. In model 0, a finite-cost proper policy has expected number `1/q_a` of command-a calls; the sum of their success probabilities is one. Its baseline cost is therefore `tau_a`. Finite cost in model 1 forces a command-b call on some finite prefix of positive planned probability. Every such finite prefix has strictly positive failure likelihood in model 0, so the additional expected cost of command b is strictly positive. The reversed argument applies in model 1. Applying both strict inequalities to an attaining robust policy gives `V_hist > max(tau_a,tau_b)`. Each endpoint Bayes infimum is the corresponding known-model cost, approached by a sequence of proper full-support memoryless rows. The separating prior is consequently interior.

At that prior a robust optimum is supported almost surely on Bayes-minimal words, since its nonnegative Bayes excess has expectation zero. Both model costs must equal the robust value. Each equality between the two strictly decreasing priority lists pairs exactly one item from each list. The two items are consecutive in every greedy merge, and reversing them leaves all later counts unchanged. All exchange vectors lie on the same Bayes-level line; their absolute sums are bounded by convergent geometric series. The all-ab and all-ba tie rules therefore bound every greedy risk vector, and a mixture of those two endpoints attains the equalizer point. This covers arbitrary word laws, not merely initially countable mixtures.

## 4. Obstruction for the full finite stochastic-controller class

The support lemma does not assume that the visible history determines the retained label. After a fixed deterministic time at which the output suffix is prescribed, every positively supported label must emit its prescribed command with probability one. The next support is the union of the fixed update supports for that command and the repeated failure report. Hence the next support and emitted symbol are functions of the current support. There are only finitely many nonempty label subsets, so a repeated support yields ultimate periodicity. Real-valued hidden label probabilities and fresh coins cannot circumvent this argument: their magnitudes may change, but a deterministic output is constrained by every positive support element.

When `u/v` is irrational, two distinct ties would imply a nonzero integer relation between `u` and `v`. Thus there is at most one tied pair. All Bayes-optimal words have an identical suffix after a fixed finite time, and its limiting command frequency `v/(u+v)` is irrational. That suffix cannot be ultimately periodic. A finite controller attaining the history value would contradict the support lemma. Strict positivity of all primitive failure probabilities is essential here and is satisfied by the stated open parameter range.

The inherited compact finite-controller parameter space and lower-semicontinuous cost objective give attainment at each fixed budget. The new proof correctly uses this fact to turn nonrealizability of the history optimum into the strict inequality `V_M > V_hist`; nonattainment by itself would not have proved a value gap. Padding unused labels gives monotonicity, and the inherited finite-history truncation theorem supplies convergence for arbitrary positive costs.

## 5. Rational realization and counted initialization

For rational `u/v`, writing `u=h ell`, `v=k ell` confines the logarithmic state to a discrete coset inside a bounded interval. Each fixed tie rule is deterministic on that finite set, so its entire word has a finite transient followed by a cycle.

The mixture construction correctly charges one pure initial label and disjoint labels for the two tails. The first command distribution aggregates the desired branch weights by their first symbol. On failure, the command-conditioned update chooses a compatible tail with probability equal to its weight divided by that symbol's aggregate weight. For a chosen symbol the physical failure probability is the same for every compatible branch, so this generates exactly the desired word mixture in both models. No persistent external seed, freely randomized initial label, or free clock appears. A zero aggregate class is never entered.

The one-label value calculation was checked independently. With `x=p q_a` and `y=(1-p)q_b`, the two costs are `tau_a+tau_b y/x` and `tau_b+tau_a x/y`. Their robust minimum is `tau_a+tau_b`, attained at `x=y`. Endpoint rows are improper and are not silently included in this division.

## 6. Quantitative constants and exact rational decision test

All following constants are correctly limited to `c_a=q_a`, `c_b=q_b`. For an interior prior the indicated memoryless row has Bayes cost `1+2 sqrt(pi(1-pi))`. The first-call lower bound at prior one half gives `V_hist >= 1+m/2`. Therefore every least-favorable prior obeys `pi(1-pi) >= m^2/16 = delta`, which implies `delta <= pi <= 1-delta` and `|z0| <= L`.

The two survival prefactors are bounded by

\[
\exp\!\frac{u(v+L)}{u+v},\qquad
\exp\!\frac{v(u+L)}{u+v},
\]

and hence by the stated common `A`. The exponent `kappa=exp(-uv/(u+v))` is strictly below one. Truncating after `T` calls and using the normalized one-row fallback adds at most `2 A kappa^T` to either model's cost. The label count is exactly bounded by one initial label, `2(T-1)` branch/position labels, and one fallback label: `2T`, including `T=1`. Setting `T=floor(M/2)` proves the displayed bound. This is an upper estimate, not a matched asymptotic rate for the finite-memory gap.

For positive rational failures, unique factorization proves that a rational logarithmic ratio is equivalent to positive rational proportionality of signed prime-exponent vectors. Reducing the proportionality to coprime integers makes the exponent coordinates divisible as asserted and gives rational `t` with `r=t^h`, `s=t^k`. Repeated rational multiplication finds a finite `J` without a transcendental comparison oracle. The interval length in logarithmic lattice units bounds the number of coset points by `N=max(J,h)+max(J,k)+1`, irrespective of the offset of the coset. The pure-start mixture therefore needs at most `1+2N` labels. In the normalized rational-data setting, the inherited fixed-budget algebraic procedure applies and computes the value/controller without computing the exact least-favorable logarithmic prior. No minimal-state or polynomial-time claim follows.

The example `r=1/2`, `s=1/3` uses unique factorization, not numerical evidence of irrationality. Its all-budget strict gap, exponential upper approximation, and algebraic fixed-budget values are mutually consistent. The proof does not determine whether the unrestricted history value is algebraic or transcendental.

## 7. Classical priority and the precise additional assertion

Primary source comparison: Clarkson, Lin and Glazebrook, *A Classical Search Game in Discrete Locations*, [arXiv:2103.09310v1](https://arxiv.org/pdf/2103.09310), Proposition 3 and Theorem 10, already supplies interior optimal hiding distributions, equalized conditional costs, and an optimal mixture of at most `n` consistently tie-broken search sequences. Its introduction credits the greedy index to Blackwell as reported by Matula; its cyclic/acyclic discussion and appendix treat commensurate search sequences. The revised source explicitly identifies the saddle lemma as a two-location specialization and disclaims these facts as new. This attribution is appropriate.

Bui, Lidbetter and Lin, [*Optimal Pure Strategies for a Discrete Search Game*](https://arxiv.org/html/2306.10908v1), studies whether a single infinite deterministic search sequence is robust-optimal. Such a sequence is not, by definition, an autonomous finite-label implementation. Thus its pure-strategy notion must not be conflated with the resource question here.

The argument checked here adds the exact equivalence between commensurability and attainment by a finite autonomous stochastic controller under a counted pure initialization convention, proves the obstruction against the full stochastic class, and supplies the stated counted approximation/cap consequences. This inspection of primary sources supports the stated distinction; it is not an exhaustive proof that no prior literature anywhere contains an equivalent finite-automaton consequence. The elementary nature of several connecting steps and their relation to existing search theory should remain visible in any claim of significance.

## Limits and remaining research questions

No finite-budget numerical experiment, root-finding output, or sample orbit is used to replace a proof in this check. No additional execution or compilation is asserted by this note. No formal verification system was run. The note only records a separately read mathematical derivation and its identified dependencies.

The result does not classify arbitrary nonreset quantum instruments, general partially observed control, more than two hidden search locations, optional commitment, all tied decision faces, or the original arbitrary-memory squared-sign risk frontier. It does not provide a matching lower rate for `V_M-V_hist`, a minimal rational-case label count, or a complexity bound for general algebraic synthesis. Independent A1/A2/Theta construction questions and human specialist/Editorial assessment remain outside this check. The stated open parameter range excludes zero failure, zero success and zero call cost; the proof does not silently include those degenerate endpoints.
