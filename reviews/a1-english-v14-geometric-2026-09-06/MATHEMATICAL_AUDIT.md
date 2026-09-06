# Mathematical audit accompanying the A1 v14 referee report

**Submission:** `ffb9214b0fc7e218d6183c1f81bccb3e47587421`. Source identifiers refer to `SOURCE_INDEX.md`. This document supplies the mathematical basis for the report's distinction between a valid new consequence and a new principal mechanism. It is not an allegation that the submitted theorems are false.

## A1. A general bounded-test-vector lemma

Let \(\mu\) be a probability, let a fixed likelihood satisfy \(0<c\le\ell\le C<\infty\), and write \(\nu=\ell\mu/(\mu\ell)\). Let \(\phi=(\phi_1,\ldots,\phi_q)\) be a bounded measurable test vector with covariance \(\Gamma=\operatorname{Cov}_\nu(\phi,\phi)\ge\lambda I_q\), where \(\lambda>0\). For \(0<\varepsilon\le1/2\), vary the prior over

\[
\mathcal B_\varepsilon(\mu)=
\{(1+u)\mu:\mu u=0,\ \|u\|_\infty\le\varepsilon\}.
\]

Use the same likelihood for every prior. Denote the set of normalized moment displacements by

\[
T_\varepsilon=
\{\nu'\phi-\nu\phi:\mu'\in\mathcal B_\varepsilon(\mu)\}.
\]

Then, for constants depending only on the dimension, a bound on the tests and the covariance lower bound,

\[
c_0\varepsilon[-1,1]^q\subset T_\varepsilon
\subset C_0\varepsilon[-1,1]^q.
\]

Consequently, for any linear map \(A:\mathbb R^q\to\mathbb R^d\),

\[
c_0\varepsilon A[-1,1]^q\subset A T_\varepsilon
\subset C_0\varepsilon A[-1,1]^q.
\]

The constants in these inclusions do not depend on the singular values of \(A\).

### Proof, including the finite-radius normalization

If \(\mu'=(1+u)\mu\), Bayes' formula gives exactly

\[
\nu'\phi-\nu\phi=
\frac{\nu\{u(\phi-\nu\phi)\}}{1+\nu u}.
\]

If \(\max_j\|\phi_j\|_\infty\le B\), each coordinate has absolute value at most \(2B\varepsilon/(1-\varepsilon)\le4B\varepsilon\). This proves the outer inclusion.

For \(v\in[-1,1]^q\), define

\[
f_v=v^{\mathsf T}\Gamma^{-1}(\phi-\nu\phi).
\]

Then \(\nu f_v=0\) and \(\nu(\phi f_v)=v\). A single finite bound \(K\ge1\) on \(\|f_v\|_\infty\) works for every such \(v\); for example a dimension-dependent multiple of \(B/\lambda\) suffices. Put \(s=\varepsilon/(4K)\) and

\[
\frac{d\mu'}{d\mu}=\frac{1+s f_v}{1+s\mu f_v}.
\]

This density is positive and integrates to one. Moreover

\[
\left\|\frac{d\mu'}{d\mu}-1\right\|_\infty
\le\frac{2sK}{1-sK}
=\frac{\varepsilon/2}{1-\varepsilon/4}\le\varepsilon.
\]

Since \(\nu f_v=0\), the new evidence is \(\mu\ell/(1+s\mu f_v)\). Thus the new posterior is exactly \((1+s f_v)\nu\). Its moment displacement is \(sv\), proving the inner inclusion. Applying a linear map preserves both inclusions. No limiting expansion, moment-realizability assumption on an arbitrary supplied table, or choice of a different likelihood is used. □

### What this says about Proposition 6.2

Take \(A=L_aD_a\). Lemma 6.1 supplies the uniform covariance hypothesis, and Lemma 5.1 supplies the conditioned active block of \(L_a\). The body inclusion in Proposition 6.2 is an instance of the lemma above. The uniform hypothesis is justified in A2 below, not assumed away. The reduction identifies the additional mechanism precisely: a bounded finite-dimensional right inverse and an exact posterior-to-prior pullback. It does not use the dimension of the acquired-history image, the command submersion, or the global semialgebraic cover. [S3, S4]

This is a mathematical explanation of the editorial reservation E14.1. It is not a proof that the proposition lacks originality in the literature, and it does not diminish the distinction between a simultaneous body inclusion and separate direction-dependent feasible classes.

## A2. Complete flags, zero pivots and all width orders

For every fixed permutation of the formal positive nodes, the Newton flag together with the constant spans complete exponential-polynomial blocks

\[
1,\quad t^{H\xi}(\log t)^j,
\qquad 0\le j<m_\xi.
\]

The positive exponents stay bounded away from zero on the compact chamber. The Hermite–Genocchi bound gives uniform boundedness and continuity, including at \(t=0\). Complete blocks, rather than isolated high derivatives, are important here. Their linear independence under a full-support probability makes the covariance positive definite. Compactness can be applied separately for finitely many permutations even though the selected Leja order itself jumps. [S2–S4]

For \(\mu\ge c_-\mu_0\) and \(\kappa^n\le\ell_h\le1\),

\[
\inf_b\nu_h((w^T\phi-b)^2)
\ge\kappa^n c_-\inf_b\mu_0((w^T\phi-b)^2).
\]

This transfers a fixed-prior covariance bound uniformly to the posterior family. No density is required, and no assertion about uniformity over all full-support priors follows without the lower envelope.

Let \(s_a\) be the number of distinct positive future exponents. The first \(s_a\) columns of \(L_a\) have a uniformly invertible leading triangular block. All later \(d_j\) are zero. Hence the nonzero singular values of \(L_aD_a\) are comparable in decreasing order to \(d_1,\ldots,d_{s_a}\). Since the Euclidean unit ball is contained in the cube and the cube is contained in the ball of radius \(\sqrt q\), A1 gives

\[
w_k(\mathcal A_h)\asymp\varepsilon d_{k+1}.
\]

For \(k\ge s_a\), both sides are zero. The proof does not invert a zero pivot. The normalized covariance can remain full rank while the physically observed body loses rank; these statements concern different maps and are compatible.

A terminology point: these are orders of Kolmogorov widths for the definition printed in the manuscript. The inclusions need not identify an exact ellipsoid or a canonical set of physical axes.

## A3. Exact prefixes and the change of statistical problem

If \(k<s_a\), the first \(k\) diagonal pivots are nonzero, so exact equality of the first raw moments is equivalent to exact equality of the first normalized moments. In A1, choosing \(v=\pm e_{k+1}\) gives two admissible priors satisfying the same prefix constraints. Their raw, and hence physical query, vectors differ by at least a constant times \(\varepsilon d_{k+1}\). The squared-loss two-point inequality gives a radius lower bound of order \(\varepsilon^2d_{k+1}^2\). The central prediction and the outer inclusion give the matching upper bound. No numerical conditioning claim follows from this exact triangular calculation. [S4]

For \(A_\theta=\{0,1,2+\theta\}\), the five positive two-trial labels have exponents

\[
1,\ 2,\ 2+\theta,\ 3+\theta,\ 4+2\theta.
\]

There are four separated groups and one gap of order \(|\theta|\). Therefore the first four scales stay nonzero in order and the fifth vanishes linearly. At horizon three, both memory checkpoints use only two flag coordinates, so the memory order remains \(M^{-1}\). Prefix-four prior ambiguity sees the fifth direction and has squared radius of order \(\varepsilon^2\theta^2\). This establishes the contrast claimed in the paper.

At a constant-failure history, its likelihood is \(2^{-n}\). The event probability is the same under every admissible prior, and on that event the posterior is the prior. Scoring only on that event turns the local construction into a common-prior decision problem with exact pre-acquisition prior-moment advice. The factor \(2^{-n}\) multiplies the risk and does not change its comparison order at fixed horizon.

This does not identify the local class with an approximate finite moment name. Nor does it give the same risk for a payoff scored on other histories. Those stronger statements are not asserted. The report records the distinction to evaluate the extent of the contribution, not to demand an unprinted theorem.

## A4. The non-generic part of the main result

The physical attainment argument has content not supplied by A1. The binomial history factors have tangent monomials supported on

\[
\{jD:0\le j\le n\}\ \cup\
\bigcup_{a\in A\setminus\{0,D\}}\{a+jD:0\le j<n\}.
\]

These \(n(r-1)+1\) exponents remain distinct in the compact strictly ordered chamber. Pairing with the selected complete future flag has rank \(p+1\). If \(L\) is the pairing map and \(v=LF/(\mu F)\), then \(e_0v=1\) and the normalized derivative has image

\[
(\mu F)^{-1}\{LQ-v e_0LQ:Q\text{ in the product tangent}\}.
\]

Because \(L\) is onto the \(p+1\) selected coordinates, this is exactly the \(p\)-dimensional hyperplane with constant coordinate zero. Uniform inverse estimates with complementary kernel coordinates produce the output cube. Integrating the original command density times its failure evidence gives a genuine subprobability minorization. There is no discarded rare-event factor. [S2, S3]

The upper argument does not follow from that local cube. For a fixed report word, the full scaled image is described by equations \(Z(u)y_j=d_jN_j(u)\), with uniformly positive evidence and polynomial degrees bounded by the horizon. Normalize each likelihood factor individually to see dimension at most \(n(r-1)\). All prior integrals are coefficients, not extra variables whose definability must be assumed. [S2, S3]

For a bounded-format set in an ordered thin rectangle, the real variation inequality and coefficient-independent section-component bounds give

\[
N(S,\rho)\le C\sum_{j=0}^{p}\rho^{-j}\prod_{i\le j}a_i.
\]

The manuscript's proof handles small integer budgets separately and replaces external covering centers by reachable representatives at a fixed factor in radius. This produces the same truncated products as the lower bound. The intrinsic proof then uses raw-moment updates, positive evidence and a finite error recurrence to realize all checkpoints causally. These steps explain both why the main result is not merely spectral and why its later phase and coding formulas follow once the attainment/covering match is established. [S2, S3; L1, L2]

## A5. Common-name quantifiers and implementation boundary

The common-name lower proof fixes one center in a dominated interior family. For \(f=t^{a_1}-\mu(t^{a_1})\), take \(\mu_\pm=(1\pm\delta f/2)\mu\). The prescribed slack puts both alternatives inside the same consistency class. For any fixed history, the posterior separation follows by subtraction of two normalized fractions. The corresponding history measures satisfy common lower domination; equality of those measures is not needed. One visible physical query has posterior variance bounded below uniformly on the chamber, which gives the \(\delta^2\) lower term. [S5]

The memory lower bound at the center survives when the code is required to serve a larger consistency class. If a nonnegative risk is bounded below by \(c_1\Xi\) and \(c_2\delta^2\), it is bounded below by \(\min(c_1,c_2)(\Xi+\delta^2)/2\). Paired-history stability and the common numerical construction give the converse upper order without selecting that center. This is a valid joint law, but its uncertainty mechanism is separate from the vanishing fifth direction in A3. [S5, S6]

The read-only program, numerical advice and persistent label are separate resources. The intrinsic label lower bound does not establish optimality of program length or numerical advice. The manuscript states that boundary. The acceptance contracts fix the requested precision and horizon before checking the returned tables. Current author suites were rerun, but the present independent probe targets the new geometry rather than replaying the earlier implementation fault injections. [S6–S8]

## A6. Independent exact diagnostics

`reproduce_review.py` uses the standard library and imports no author helper. For a prefix of nodes it forms the confluent Hermite interpolation matrix

\[
B_{(x,k),j}=\binom{j}{k}x^{j-k},\qquad j\ge k,
\]

and obtains the Newton divided difference as the leading polynomial coefficient of the Hermite interpolant to \(t^{Hz}\). The test functions are finite sums of \(t^a(\log t)^k\). Their integrals against polynomial densities are evaluated exactly using

\[
\int_0^1t^a(\log t)^k\,dt=
\frac{(-1)^k k!}{(a+1)^{k+1}},\qquad a>-1.
\]

Endpoint atoms are evaluated separately. The non-density prior is

\[
d\mu(t)=\tfrac12(1+t)\,dt+\tfrac18\delta_0+\tfrac18\delta_1.
\]

Its continuous part has mass three quarters, so it is a normalized full-support probability. The histories are either two constant failures or two positive nonconstant factors. The probe uses both Leja order and interleaved node order; the latter tests the complete covariance and Newton identity, not an incorrectly asserted diagonal Leja factorization for arbitrary orders.

The 60 configurations pass 21,691 assertions. Half use nonconstant histories and detect the deliberately omitted prior-normalization denominator. The submitted denominator passes. All comparisons are exact rational identities or inequalities. The diagnostic verifies its source input against the submission's manifest blob and 80 file hashes before running. Execution numbers and hashes are recorded in `EXECUTION.json`.

The calculations support specific finite checks and distinguish the present test from a repeated author-suite execution. They do not replace the continuum, uniformity, minimax or literature arguments.
