# Technical note — independent checks of the attainable law and its quantifiers

**Reviewed source:** A1 English v8, `5d3d7e04b172f98bddfd037c488d93d516d20a98`.  
**Status:** mathematical deductions and finite diagnostics supporting the referee report. None of the examples below is a counterexample to a printed v8 theorem. Part II is a consequence of the author's new theorem, not an extension claimed by this review.

## I. Why the past-limited cover and lower bound fit together

Write p=min{n(r−1),K_m−1} and let a_i=theta^{nu_i} in decreasing physical-width order. Suppose first that theta>0. The manuscript establishes two different facts, neither of which can be omitted:

1. The complete scaled attainable set S has bounded semialgebraic format, dimension at most p and a fixed-multiple containing rectangle with widths a_i.
2. The acquired-history law, projected onto the first p desingularized coordinates, minorizes a fixed positive multiple of a p-cube.

The first fact gives

\[
N(S,\delta)\le C\sum_{j=0}^{p}\delta^{-j}\prod_{i=1}^{j}a_i.
\]

Set

\[
e=\max_{1\le j\le p}\left(M^{-1}\prod_{i=1}^j a_i\right)^{1/j}.
\]

For every j, the jth product is at most M e^j. Choosing a fixed sufficiently large L makes the nonconstant sum at radius Le at most M/2; the constant term is absorbed for sufficiently large M. For the finitely bounded remaining budgets, e≥a_1/M and a diameter bound suffice. Empty balls can be removed, and every remaining center can be moved onto S at a cost of at most two in radius. Thus the upper bound uses at most M genuinely reachable representatives.

For the second fact, scale the projected minorized cube by its physical widths. For every ell≤p, the probability captured by M radius-r balls in the first ell coordinates is at most a dimensional multiple of M r^ell/(a_1...a_ell). Taking r a fixed multiple of (a_1...a_ell/M)^{1/ell} gives the matching mean squared lower bound. The fixed full-column-rank query matrix changes constants only. At zero, delete vanishing physical widths in both arguments.

This reasoning explains precisely why it is legitimate to truncate at p. A p-dimensional local tangent alone would not control global covering numbers, and a bounded-format set in a rectangle alone would not force a matching lower bound. V8 proves both needed facts, with the second one tied to the actual exploration law rather than an invented distribution on the image.

For the seven-trial peak, p=8 and the selected order list is 0 repeated six times followed by 1 repeated twice. The only potentially maximal terms are

\[
A=M^{-1/3},\qquad B=\theta^{2/7}M^{-2/7},\qquad C=\theta^{1/2}M^{-1/4}.
\]

Since B=A^{3/7}C^{4/7}, it cannot exceed max(A,C). Their crossover is M=theta^{−6}, at physical squared-loss scale theta^2. The actual selected limiting tests, ordered by limiting exponent, are

\[
1,t,t^2,t^2\log t,t^3,t^3\log t,t^4,t^5,t^6.
\]

Their uniform-prior pairing with 1,t,...,t^8 has determinant

\[
\frac{1}{5263867814258605833254325984952320000000000}.
\]

The independent program computes this determinant rather than loading the author's recorded value. Strict positivity for all full-support priors comes from the written confluent argument, not from this one calculation.

## II. A second-order attained jet yields three checkpoint regimes

To test more than first-order collisions, keep A_theta={0,1,2+theta}, take n=9 and m=5, and restrict to 0≤theta≤1/8. Different formal five-fold pairs have distinct positive-calibration exponents on this interval: their limiting coordinates differ by integers, while the possible slope differences have absolute value at most five.

The formal five-fold pairs are (i+2j,j), with i,j≥0 and i+j≤5. There are 21 pairs. Grouped at limiting exponents 0 through 10, their multiplicities are

\[
1,1,2,2,3,3,3,2,2,1,1.
\]

The nonconstant future order list has ten zeros, seven ones and three twos. However, the past capacity is 2n=18, so the attainable truncation keeps

\[
\underbrace{0,\ldots,0}_{10},\quad
\underbrace{1,\ldots,1}_{7},\quad 2.
\]

The selected order-two coordinate is the first such coordinate in the increasing-limiting-exponent convention; its cluster is lambda=4. Together with the constant and preceding selected jets, the tests form complete initial cluster blocks. At zero, the binomial tangent is the full polynomial space through degree 18. The normalized rank is therefore 18, by the same strict pairing argument. The independent program checks the corresponding exact rank for three full-support priors, including one with atoms, but these finite examples are not the proof of its universality.

Applying the v8 checkpoint theorem gives

\[
R_{M;9,5}^{\theta}\asymp
\max\left\{M^{-1/5},\;
\theta^{14/17}M^{-2/17},\;
\theta M^{-1/9}\right\}.
\tag{T1}
\]

There is no additional maximal term inside a constant-order block. Indeed, in such a block S_ell=c ell+d, so the logarithm of theta^{2S_ell/ell}M^{−2/ell} is affine in 1/ell; intermediate terms are geometric interpolations of endpoint terms. The two transitions in (T1) occur at orders

\[
M=\theta^{-10},\quad R=\theta^2;
\qquad
M=\theta^{-27},\quad R=\theta^4.
\]

This is a **checkpoint** calculation at (9,5). It is not asserted to be the entire fourteen-trial maximum-stage streaming profile. That profile would require taking the maximum over all its checkpoints, as Theorem 7.2 prescribes. No leading distortion constant or exact integer transition is claimed.

This test demonstrates that the truncation mechanism is not inherently limited to a single weak scale. It also illustrates why merely adding another horizon would not, by itself, settle an editorial significance question: this result is already an algebraic consequence of v8.

## III. Full support cannot make the lower constants uniform over priors

The manuscript fixes the prior before choosing its comparison constants. That qualification is essential. Here is a direct example within its positive finite experiment, not a proposed strengthening that the author must prove.

Fix t_0 in the parameter interval, let lambda be a full-support probability there, and set

\[
\mu_\delta=(1-\delta)\delta_{t_0}+\delta\lambda,
\qquad 0<\delta\le1/2.
\]

Each mu_delta has full support. For any n-step admitted history, write its likelihood as F_h. If every report likelihood is between kappa and one, then

\[
\kappa^n\le F_h(t)\le1.
\]

The posterior mass of the continuous/full-support mixture component is at most

\[
\alpha_h
=\frac{\delta\lambda(F_h)}{(1-\delta)F_h(t_0)+\delta\lambda(F_h)}
\le\frac{\delta}{(1-\delta)\kappa^n}
\le2\delta\kappa^{-N},\qquad n\le N.
\]

For any future event test H taking values in [0,1], the posterior prediction differs from H(t_0) by at most alpha_h. The one-state decoder announcing H(t_0) for each supplied query therefore has squared-prediction regret at most

\[
4\delta^2\kappa^{-2N}
\]

uniformly in histories and checkpoints. This tends to zero as delta tends to zero, while the rank formula continues to hold for every positive delta. Thus no strictly positive lower comparison constant independent of all full-support priors can follow from that formula.

This is **not a defect in v8**, whose constants may depend on the fixed prior. It clarifies the distinction between a prior-independent rank statement and uniform quantitative conditioning across a family of priors. The negative editorial recommendation must not be represented as a demand for the impossible prior-uniform lower bound just ruled out.

## IV. What the independent executions do and do not establish

`referee_checks.py` imports no author code. Its 327 successful check families comprise exact selected-flag ranks and normalized ranks, a separately computed seven-trial determinant, exact Newton-to-physical identities, physical product-menu ranks, exact-logarithm envelope checks, integer-budget box-allocation checks, and actual single-index transition fixtures.

The streaming fixtures use two commands and four reports, four calibrations (including zero and 1/2), two full-support priors, and state budgets 1,3,5. The implemented machine has one persistent field, `index`. A stage clock and transition tables are externally supplied read-only data, as in the manuscript. Exact prefix products are retained only by the reference harness. Across 24 fixtures, 16 sampled input streams and seven updates each, the program makes 2,688 exact rational comparisons of the raw update with direct posterior integration. Coincident formal exponents are checked for consistent moment values.

Those codebooks are finite-input diagnostic codebooks, not claimed optimal asymptotic quantizers. No result about a continuous-command minorization, the general semialgebraic cover, all priors, effective synthesis or top-journal significance is inferred from their execution. The author suites' 97 and 255 local checks are separately counted and are not added to the independent 327 as if they were all independent proofs.
