# Mathematical audit accompanying the A1 v15 referee report

**Reviewed commit:** `e1d0ff2ef04a8641ac77923b664c4d3e8386f212`  
**Date:** 7 September 2026

This is the mathematical working record supporting `REFEREE_REPORT.md`. It records reconstructed arguments, their hypotheses, and the boundaries of the conclusion. It is not a formal proof-assistant certificate. Source identifiers refer to `SOURCE_INDEX.md`.

## A1. Normalization and a genuinely full-dimensional history measure

Write \(d=nb\), let \(P\) be the product likelihood, and let \(T=\operatorname{im}DP\). Put

\[
LQ=(\mu Q,\mu(Q\phi)),\quad Z=\mu P>0,\quad v=LP/Z.
\]

The unnormalized output differential factors through \(L(T)\). The normalized differential is

\[
\mathcal DQ=Z^{-1}\{LQ-v(e_0LQ)\}.
\]

If \(P\in T\), then \(v\in L(T)\). Also \(e_0v=1\). A vector \(w\in L(T)\) lies in the kernel of \(w\mapsto w-v(e_0w)\) precisely when it is a multiple of \(v\). Therefore

\[
\operatorname{rank}\mathcal D=\operatorname{rank}(L|_T)-1.
\]

The condition \(P\in T\) is what makes the exact rank loss justified. Surjectivity of \(L|_T\) then gives all \(p\) nonconstant output directions. In the detector model, varying one factor in its own direction proves \(P\in T\), and the interior command-to-factor map is onto. [S1, S3]

For the probability statement, suppose \(J=Dz(u_*)\) has least row singular value at least \(\sigma\). Let the rows of \(K\) be an orthonormal basis of \(\ker J\) and set

\[
F(u)=(z(u),K(u-u_*)).
\]

The nonzero row spaces of \(J\) and \(K\) are orthogonal, so the least singular value of \(DF(u_*)\) is at least \(s=\min(\sigma,1)\). Choose a command ball of radius \(r\), uniformly interior, on which \(\|DF-DF(u_*)\|\le s/2\). The contraction equation for the inverse places an output ball of radius at least \(sr/2\) in the image. A smaller product cube with half-side \(\rho\) lies in this ball.

If \(\|DF\|\le B\), the absolute determinant of the forward derivative is at most \(B^d\). Suppose the command density is at least \(a\) and each report factor is at least \(\kappa\). The command-and-report subprobability density is then at least \(a\kappa^n\). On the output cube, its density after applying \(F\) is at least \(a\kappa^nB^{-d}\). Integration over the full \((d-p)\)-dimensional kernel cube gives

\[
z_*(Z\,d\mathsf Q)\ge
\beta\,\operatorname{Unif}(z(u_*)+[-\rho,\rho]^p),
\qquad
\beta=a\kappa^nB^{-d}(2\rho)^d,
\]

after decreasing constants when necessary. The precise displayed choice is not needed by the manuscript, but it shows what its proof controls. All dimensions are fixed. A local section without this integration would not yield the claimed probability measure. The submitted proof includes the integration. [S3]

## A2. Two Chebyshev systems and prior-envelope uniformity

Let \((v_0,\ldots,v_p)\subset T\) and \((1,\phi_1,\ldots,\phi_p)\) be the two strict systems. After orientation, determinant expansion gives

\[
\det[\mu(v_i\phi_j)]_{i,j=0}^p
=\frac{1}{(p+1)!}\int
\det[v_i(t_k)]\det[\phi_j(t_k)]\prod_k\mu(dt_k).
\]

The product of determinants is unchanged by a common permutation of the points, nonnegative on the whole integration domain, and positive on distinct interior points. Disjoint ordered interior intervals each have positive mass under a full-support prior. The integral is positive. Thus \(L|_T\) is onto, and A1 applies.

For the dominated family \(c_-\mu_0\le\mu\le c_+\mu_0\), weak subsequential limits of probabilities exist on the compact interval. The inequalities pass to limits against nonnegative continuous functions. A limit still dominates \(c_-\mu_0\), so has full support. Joint continuity of the normalized Jacobian follows from uniform-norm continuity of its factors and tests and the positive evidence denominator. Rank deficiency at a limiting sequence would contradict the determinant conclusion. This supplies a uniform least row singular value, not just pointwise generic rank. [S3]

The theorem does not derive its hypotheses from \(\dim W\). It requires the indicated subsystem in the actual product tangent. This is the exact boundary between a sufficient attainment criterion and a classification of all positive detectors.

## A3. The circular experiment is physically implementable

For rejection probabilities \(u\), direct expansion of the four detector cells gives

\[
f_{u,\dagger}(\theta)=a\{1+\tau(zw+\bar z w^{-1})\},\quad
 a=\tfrac14\sum u_j,\quad
 z=\frac{u_{1,+}-u_{1,-}-i(u_{2,+}-u_{2,-})}{8a}.
\]

The command vector

\[
(\tfrac12+2\Re z,\tfrac12-2\Re z,
 \tfrac12-2\Im z,\tfrac12+2\Im z)
\]

realizes \(a=1/2\) on a fixed neighborhood of zero. This is a four-entry lookup interface and does not inspect the hidden angle. All report factors are positive in the stated command and contrast ranges. Accepted-report coefficients also satisfy \(|z|\le1/2\). Thus the upper bounds apply to all admitted report histories, not only to the all-failure chart used for the converse. [S4]

For the product likelihood, selecting positive and negative Laurent powers shows that a contribution to \(p_j\), \(j\ge0\), uses \(j+h\) positive selections and \(h\) negative selections. Its contrast degree is \(j+2h\). Consequently

\[
p_j=\tau^jP_{n,j}(z,\bar z;\tau^2),\qquad
P_{n,j}(z,\bar z;0)=e_j(z).
\]

Haar integration extracts \(p_0\), and pointwise positivity gives \(p_0\ge(1-\tau)^n\). The normalized polynomial ratios \(S_j=P_{n,j}/P_{n,0}\) and their first two command derivatives are bounded at fixed horizon, including at zero contrast.

At distinct central values \(\zeta_i\), the differential of the elementary-symmetric map is injective. Indeed, zero differential coefficients in \(\prod_i(\lambda+\zeta_i)\) imply

\[
\sum_i\dot z_i\prod_{h\ne i}(\lambda+\zeta_h)=0.
\]

Evaluation at \(\lambda=-\zeta_i\) forces \(\dot z_i=0\). The square complex derivative is invertible, hence its real form has rank \(2n\); every initial \(2k\)-row block has rank \(2k\). The physical command right inverse transfers this rank to the actual command variables. With finitely many \(n,k\le N\), continuity in \(\tau^2\) provides one positive interval and uniform least row singular values.

Applying the quantitative inverse argument to \(S\) retains the actual evidence \(p_0\prod_i a_i\). This verifies the normalized flag minorization. At \(\tau=0\), \(S\) is only an auxiliary extension: the physical coordinates \(Y_j=\tau^{2j}S_j\) all vanish. No positive physical rank is asserted at zero.

## A4. The query metric, including all attenuation factors

For the repeated query at phase \(\varphi_l\), the coefficient of \(w^j\) is

\[
2^{-m}\tau^jB_{m,j}(\tau^2)e^{-ij\varphi_l},\qquad
B_{m,j}(s)=\sum_{h=0}^{\lfloor(m-j)/2\rfloor}
 \frac{m!\rho^{j+2h}s^h}{(j+h)!h!(m-j-2h)!}.
\]

The constant term of \(B_{m,j}\) is \(\binom mj\rho^j>0\). All coefficients are nonnegative, so uniform upper and lower bounds follow on the compact contrast interval for each fixed finite menu. For \(c_j=p_j/p_0\), Haar multiplication gives

\[
q_l=2^{-m}B_{m,0}+2^{1-m}\Re\sum_{j=1}^m B_{m,j}Y_je^{ij\varphi_l},
\qquad Y_j=\tau^jc_j.
\]

For \(L=2m+1\), every nonzero integer frequency between \(-2m\) and \(2m\) has zero average on the \(L\)-point phase grid. There is therefore no aliasing between any of the sine and cosine columns in this calculation. Squaring the difference of two query vectors gives

\[
\|q-q'\|_{\rm av}^2
=2^{1-2m}\sum_{j=1}^mB_{m,j}^2|Y_j-Y'_j|^2.
\]

An unrestricted decoder can first be orthogonally projected onto this affine Fourier span; projection does not increase the loss against a true query vector in that span. Thus the same metric controls the lower bound. [S4]

A useful exact check is \(n=m=1\): \(p_0=1\), \(c_1=\tau z\), and

\[
q_l=\tfrac12+\rho\tau^2\Re(ze^{i\varphi_l}),\qquad
\|q(z)-q(z')\|_{\rm av}^2
=\tfrac12\rho^2\tau^4|z-z'|^2.
\]

Replacing the acquired coefficient by an order-one variable would lose one attenuation factor and give the wrong squared contrast power. This is a genuine acquisition–observation interaction, not a statement about the rank of a Fourier evaluation matrix.

## A5. From paired axes to the sharp fixed-label law

Set \(k=\min(n,m)\). The containing real rectangle has half-width orders

\[
a_{2j-1}=a_{2j}=\tau^{2j},\qquad 1\le j\le k,
\]

up to constants depending only on fixed data. The normalized flag minorization supplies a translated cube before this scaling. Its projection onto any first \(l\) coordinates yields an actual subprobability with a uniform density lower bound on a rectangle of volume comparable to \(\prod_{i\le l}a_i\).

For any \(M\) decoder centers, radius-\(b\) balls cover at most a constant times \(Mb^l/\prod_{i\le l}a_i\) of the normalized rectangle probability. Choose

\[
b=c_l\left(M^{-1}\prod_{i\le l}a_i\right)^{1/l}
\]

with small fixed \(c_l\). A fixed positive part of the minorized probability remains at distance at least \(b\). Thus the squared loss is bounded below by a fixed multiple of \(b^2\). Randomized assignment cannot improve upon the closest center; independent public coding randomness can be fixed and then averaged. No report event is conditioned out of the risk.

For the upper bound, a rectangular grid has count at most

\[
C_d\sum_{l=0}^d r^{-l}\prod_{i\le l}a_i.
\]

For \(M\ge2C_d\), take \(r=A\max_{l\ge1}(M^{-1}\prod_{i\le l}a_i)^{1/l}\) with fixed large \(A\). The constant term and all nonconstant terms together are then at most \(M\). For the bounded set of smaller integer budgets, one representative and a larger constant suffice, using \(r\ge a_1/M\). Replacing grid centers whose balls meet the reachable set by points of that set at most doubles the radius. This gives actual reachable codebooks for every integer \(M\ge1\).

For \(l=2j\),

\[
\left(M^{-1}\prod_{i\le2j}a_i\right)^{2/(2j)}
=\tau^{2(j+1)}M^{-1/j}.
\]

Let \(h_l=2(\sum_{i\le l}\log a_i-\log M)/l\). For \(j\ge2\), the equality of the last paired axes gives

\[
h_{2j-1}=\frac{j-1}{2j-1}h_{2j-2}
        +\frac{j}{2j-1}h_{2j}.
\]

Also \(a_1^2/M^2\le a_1a_2/M\) for \(M\ge1\). Hence no odd order enlarges the maximum. This proves the asserted profile for positive contrast. At zero contrast, the physical posterior and all query predictions are known and the loss is exactly zero. [S4]

Equating adjacent even-order terms gives \(M=\tau^{-2j(j+1)}\). These crossing points increase with \(j\) when \(0<\tau<1\), and the slopes \(-1/j\) in \(\log M\) increase. Each harmonic pair therefore has its own interval in the upper envelope. The phase statement is an algebraic consequence of the sharp profile, not a separate source of the lower bound.

## A6. One causal realization and the shrinking state

Multiplication of the posterior Laurent density by a new factor gives

\[
c'_j=\frac{c_j+\tau zc_{j-1}+\tau\bar zc_{j+1}}
                  {1+\tau z\bar c_1+\tau\bar zc_1}.
\]

Multiplying by \(\tau^j\) yields exactly

\[
Y'_j=\frac{Y_j+\tau^2zY_{j-1}+\bar zY_{j+1}}
                 {1+z\bar Y_1+\bar zY_1},\qquad Y_0=1.
\]

This derivation verifies both the \(\tau^2\) and the normalization denominator. The denominator is the posterior expectation of the normalized report factor, and is at least \(1-\tau\). On the segment between reachable states it is the same expectation under a posterior mixture. The numerator and denominator have uniformly bounded affine coefficients and reachable states are bounded. Direct subtraction of two fractions therefore gives a Lipschitz constant independent of reciprocal contrast. [S4]

At stage \(n\), retain the future-relevant coordinates through \(m=N-n\). Indices above \(n\) are identically zero. After the next report only indices through \(m-1\) are required, and their updates use no index above the old \(m\). This remains true before and after the past/future changeover. At each stage choose reachable representatives of the cover from A5. Updating a representative by the actual new command and report gives a reachable next state; quantize that state into the next codebook.

If the true and representative states differ by \(e_n\),

\[
e_{n+1}\le L_ne_n+r_{n+1},\qquad e_0=0.
\]

There are finitely many stages, so \(e_n\le C_N\max_s r_s\). The query metric converts the square of this bound to the asserted maximum-checkpoint law. Only an index among \(M\) representatives persists; the clock and fixed exact-real program are read-only under the stated resource model. This is not a bound on the program size or numerical workspace.

The same independent acquisition law supplies all checkpoint converses. Every causal index is an \(M\)-message encoder of the prefix, and the largest attainable harmonic count is \(\lfloor N/2\rfloor\). This proves the matching maximum-checkpoint lower order. It does not establish checkpointwise optimal rates for a single filter, and the manuscript does not make that stronger claim.

For exact dimension, positive contrast gives a local physical prediction patch of real dimension \(2k\). A sufficient continuous encoding is injective on a local section, so invariance of domain excludes fewer coordinates. Every continuation likelihood is a trigonometric polynomial of degree at most \(m\), proving sufficiency of the retained Fourier coordinates for all future laws. At zero contrast the state is constant.

## A7. The retained collision chain and the distinct role of prior ambiguity

The monomial tangent calculation uses \(F_i=(1+c_it^D)/2\). The polynomials \(\prod_{h\ne i}(1+c_ht^D)\) span the degree-\((n-1)\) polynomials in \(t^D\), as evaluation at the distinct roots \(-1/c_i\) verifies. This gives the stated separated support with cardinality \(n(r-1)+1\). Pairing it with complete confluent flags, then applying A1, proves the relevant attained rank. [S6, S7]

The normalized Newton functions are bounded by fixed multiples of \(t^{a_*}|\log t|^{j-1}\), and repeated-node limits retain complete Hermite blocks. Compactness over each of finitely many formal orders supplies uniform singular values. This avoids an invalid appeal to continuity of the greedy order itself.

For the global upper bound, the posterior image is semialgebraic in command variables with fixed format and arbitrary real coefficients. Its dimension is at most the number of normalized factor coordinates. The real variation inequality and the coefficient-independent affine-section component bound give a thin-rectangle cover whose products stop at that dimension. The geometric integration does not require a density or semialgebraicity of the prior. The raw-moment recurrence then avoids all inverse collision pivots. [S7, S8; L1, L2]

For prior ambiguity, a separate calculation is needed. Let \(\Gamma=\operatorname{Cov}_\nu(\phi,\phi)\ge\lambda I\), \(\|\phi_j\|_\infty\le B\), and \(v\in[-1,1]^q\). Then

\[
f_v=v^{\mathsf T}\Gamma^{-1}(\phi-\nu\phi),\quad
\nu f_v=0,\quad\nu(\phi f_v)=v,\quad
\|f_v\|_\infty\le2qB/\lambda.
\]

With \(K=\max(1,2qB/\lambda)\), \(s=\varepsilon/(4K)\), the prior

\[
\mu'=\frac{1+s f_v}{1+s\mu f_v}\mu
\]

is a probability in the stated relative ball. Since \(\nu f_v=0\), Bayes normalization gives \(\nu'=(1+s f_v)\nu\) exactly. The displacement is \(sv\), while any admissible relative perturbation has coordinate displacement at most \(4B\varepsilon\). Applying an arbitrary observation map gives the simultaneous sandwich even at rank loss. [S5]

This is the correctly attributed bounded-dual reduction. The complete confluent covariance lower bound gives uniform constants; the active triangular block then yields the width orders. Exact prefix equalities use nonzero pivots only as exact algebraic constraints. At the constant-failure history their physical realization has weight \(2^{-n}\), and the loss outside that event is expressly zero. Neither argument substitutes this exact local advice for a common inaccurate moment name.

The common-name section's posterior-tilt identity and overlapping-history converse were checked. The center's slack places both alternatives in the same consistency class. Its upper proof invokes retained stability and construction results; the present audit checks that dependence and its information convention, not all implementation details of those results. [S9]

## A8. Execution, negative controls, and non-conclusions

`reproduce_review.py` imports only the Python standard library and does not import author modules. Its exact arithmetic checks were actually executed. The stored execution contains 1,800 passing assertions and the script SHA-256. The five mutation families deliberately break correct formulas or hypotheses. Their detection is evidence about diagnostic sensitivity, not evidence of five manuscript defects.

Finite samples with nonzero rank at several contrasts do not establish a uniform interval. The proof of that interval is the nonsingular central derivative and continuity in A3. The script does not implement an optimal finite-label transducer or solve its minimax risk, and it does not rerun the author's compiler suites. No historical receipt is counted as a new execution.

The review's significance judgment is separate from these calculations. The inspected Bayesian phase-estimation literature establishes a relevant comparison for Fourier representations and updates; it does not by itself establish the specific fixed-label law audited here. A priority or nonoriginality conclusion would require additional evidence not supplied by that comparison. [L3, L4]
