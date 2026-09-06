# Mathematical audit accompanying the v16 referee report

Submission: `9f6875ebf1473b84dcde2ccabcb1556202233276`. Source identifiers refer to `SOURCE_INDEX.md`. This document records analytic reconstructions, not just test outcomes. No result below is asserted to be a new research contribution of the referee.

## A1. From a true tangent to an unconditional lower measure

Let \(T=\operatorname{im}DP\), \(Z=\mu P>0\), and \(LQ=(\mu Q,\mu(Q\phi))\). Suppose \(P\in T\). With \(v=LP/Z\), the normalized differential is

\[
Q\longmapsto Z^{-1}(LQ-v e_0LQ).
\]

On \(L(T)\), \(e_0v=1\) and \(v\in L(T)\), so the kernel of the map in parentheses is exactly the span of \(v\). This proves a loss of precisely one rank, not a heuristic subtraction from an unrelated ambient dimension. If \(L\) is onto \(\mathbb R^{p+1}\), the nonconstant normalized coordinates have rank \(p\). [S4]

The measure statement needs a further argument. At a witness \(u_*\), let \(K\) have orthonormal rows spanning \(\ker Dz(u_*)\), and consider

\[
F(u)=(z(u),K(u-u_*)).
\]

The least singular value of \(DF(u_*)\) is at least \(\min(\sigma,1)\). The bounded second derivative gives a uniform inverse neighborhood. If \(\|DF\|\le B\), then the inverse Jacobian has absolute determinant at least \(B^{-d}\). Multiply by the joint command-density bound and by the report evidence, at least \(\kappa^n\), and integrate over the entire kernel-coordinate cube. This gives a subprobability minorization of a \(p\)-cube. Restricting commands to a lower-dimensional section without this integration would not suffice.

For the ordered model, determinant integration pairs the evaluation determinants of two strict Chebyshev systems. The product has fixed nonnegative sign; full support assigns positive mass to a product of separated interior intervals where it is positive. No density is needed. Uniformity over a dominated prior family follows from weak compactness and uniform-norm continuity of the tests and command derivatives. These are precisely the hypotheses printed in Theorem 3.2. [S4]

## A2. The collision-uniform monomial chain

At factors \(F_i=(1+c_it^D)/2\), with distinct small positive \(c_i\), put \(z=t^D\). The polynomials

\[
\prod_{h\ne i}(1+c_hz),\quad i=1,\ldots,n,
\]

span the polynomials of degree at most \(n-1\): evaluation at \(-1/c_j\) proves linear independence. Varying all one-step monomial coefficients yields tangent exponents

\[
\{jD:0\le j\le n\}\;\cup\;
\{a+jD:a\in A\setminus\{0,D\},\;0\le j<n\}.
\]

They are distinct because \(0<a<D\). Thus the true tangent has dimension \(n(r-1)+1\), independent of future additive collisions. [S5]

Retain formal future-node multiplicities. For the finite Leja order \(x_1,\ldots,x_q\), its pivots satisfy \(d_1=1\), \(d_j\ge d_{j+1}\ge0\), and

\[
\prod_{j=1}^{\ell}d_j
\le\mathcal V_{m,\ell}
\le\ell!\prod_{j=1}^{\ell}d_j.
\]

Newton evaluation gives raw moments as \(L D\) times normalized complete-flag moments. The active leading block of \(L\) has bounded entries and diagonal of modulus one; its inverse is bounded in fixed dimension. Zero pivots are never inverted. [S7]

Every complete prefix of divided differences spans the corresponding complete Hermite data, even when repetitions are not consecutive. Applied to \(t^{Hx}\), this gives whole blocks \(t^{Hy}(\log t)^j\), not isolated logarithmic tests. Together with the constant, the prefix is a strict Chebyshev system. Applying A1 to the actual tangent therefore attains every prefix through

\[
p_{n,m}=\min\{n(r-1),q_m\}.
\]

The witness's normalized rank remains full even when some physical pivots vanish. The auxiliary extension and the physical observable rank must not be confused. Uniformity is obtained over finitely many formal node orders on the compact calibration family. [S5–S7]

The global image is a rational image of bounded factor-command parameters; the denominator is positive evidence, and prior integrals enter only as real coefficients. Its dimension is at most \(n(r-1)\), and its physical coordinates lie in a rectangle with sides bounded by multiples of \(d_j\). The real variation inequality, bounded component counts for fixed-format semialgebraic slices, and the projected rectangle volume bound

\[
\operatorname{vol}_{j}(\operatorname{proj}_{E}R)
\le 2^j\binom qj d_1\cdots d_j
\]

yield the dimension-truncated cover. This use of the real entropy input is supported by the explicitly real equations (4)–(5) recalled in Comte–Halupczok; Zhang–Kileel supplies the relevant regularity statements. No nonarchimedean transfer is involved. [S6–S7; L3–L4]

For the causal step, every required posterior raw moment updates as a ratio of bounded linear forms in the previous raw moments. The denominator is the next report probability and is at least \(\kappa\), including along segments corresponding to mixtures of posterior measures. This gives the needed gap-independent Lipschitz bound. The next exact image of a reachable representative is reachable, so subsequent quantization has a valid domain. [S7]

## A3. An explicit audit reduction for the finite-label law

The following elementary implication separates the geometric obligations from the coding calculation. It is a reconstruction of the mechanism in the paper, not a claim of new generality or priority.

Suppose that in physical prediction coordinates, uniformly in a parameter:

1. A compact state set \(S\subset\mathbb R^q\) lies in a rectangle with side orders \(s_1\ge\cdots\ge s_q\ge0\), has dimension at most \(p\), and has bounded semialgebraic format. Prediction loss is uniformly equivalent to squared Euclidean distance on this image.
2. For each \(\ell\le p\) with positive first \(\ell\) sides, the projection of the actual acquisition law dominates a fixed positive multiple of uniform measure on a translated rectangle with sides comparable to \(s_1,\ldots,s_\ell\).
3. For a causal statement, stage updates in these coordinates are uniformly Lipschitz, take reachable representatives to reachable states, and the horizon is fixed.

Define

\[
e_M=\max_{1\le\ell\le p}
\left(\frac{s_1\cdots s_\ell}{M}\right)^{1/\ell}.
\]

The thin-rectangle bound gives

\[
\mathcal N(S,r)\le C_0\sum_{\ell=0}^{p}
 r^{-\ell}s_1\cdots s_\ell.
\]

At \(r=Ae_M\), the positive-order part is at most \(C_0M\sum_{\ell=1}^{p}A^{-\ell}\). Choose fixed \(A\) so this is at most \(M/2\). For \(M\ge2C_0\), the zero-order term fits as well. For the remaining integer budgets, one representative suffices at radius \(O(s_1)\), while \(e_M\ge s_1/M\). Replacing an external ball center by a point of \(S\) costs only a factor two. If every side is zero, \(S\) is a singleton. Thus the worst-history squared error is \(O(e_M^2)\).

For an output outside the prediction image, choose a nearest attainable prediction. Compactness and the triangle inequality increase its distance to any target by at most a factor two, so arbitrary decoder outputs cause no difficulty. Conversely, project the resulting \(M\) centers onto the first \(\ell\) physical coordinates. Their radius-\(r\) balls cover at most a fraction

\[
C_\ell M r^\ell/(s_1\cdots s_\ell)
\]

of the minorized rectangle. Set \(r=c_\ell(s_1\cdots s_\ell/M)^{1/\ell}\) so this fraction is at most one half. The unconditional squared error is bounded below by a fixed multiple of \(r^2\). Maximizing over \(\ell\) yields \(\Omega(e_M^2)\). Independent coding randomization cannot improve this lower bound: condition on the independent seed, and use the same uniform estimate for the resulting decoder centers. Decoder randomization can also be removed by conditional Jensen.

For a causal realization, quantize the exact update of the stored representative at each stage. The state errors obey

\[
E_{n+1}\le L_nE_n+C e_{n+1,M},\qquad E_0=0.
\]

At fixed horizon this is \(O(\max_n e_{n,M})\). A checkpoint with the largest profile supplies the matching causal lower bound. Constants can depend substantially on the horizon; this argument proves no growing-horizon theorem.

The real mathematical work is therefore in verifying these three obligations for the submitted experiments. Neither an arbitrary positive detector nor a general smooth parametrization automatically satisfies them. This reduction explains the significance assessment without replacing the model-specific proofs by a dimension heuristic. [S4, S6–S8]

## A4. Circular acquisition, physical norm, and causal indexing

Write the unnormalized Laurent product as \(P(w)=\sum p_jw^j\). A term contributing to \(p_j\) chooses \(j+h\) positive powers and \(h\) negative powers, whence

\[
p_j=\tau^jP_{n,j}(\tau^2),\qquad P_{n,j}(0)=e_j(z_1,\ldots,z_n).
\]

Haar normalization divides by \(p_0\ge(1-\tau)^n\). Thus \(c_j=\tau^j S_j\) and \(Y_j=\tau^{2j}S_j\). The physical right inverse from a small complex \(z\)-box to the four command probabilities has no inverse contrast. At distinct \(z_i\), differentiating \(\prod_i(\lambda+z_i)\) and evaluating at \(\lambda=-z_i\) proves invertibility of the elementary-symmetric coefficient differential. Compact continuity over finitely many stages provides the small-contrast interval. A1 supplies positive history measure, retaining the evidence \(p_0\prod_i a_i\). [S8]

For the repeated-failure query, coefficient extraction gives

\[
q_l=2^{-m}B_{m,0}(\tau^2)
 +2^{1-m}\Re\sum_{j=1}^{m}B_{m,j}(\tau^2)Y_j e^{ij\varphi_l},
\]

where

\[
B_{m,j}(s)=\sum_{h=0}^{\lfloor(m-j)/2\rfloor}
\frac{m!\rho^{j+2h}s^h}{(j+h)!h!(m-j-2h)!}.
\]

For \(j\le m\), \(B_{m,j}(0)=\binom mj\rho^j>0\). The \(2m+1\) equally spaced phases eliminate every cross term, so

\[
\frac1{2m+1}\sum_l|q_l-q_l'|^2
=2^{1-2m}\sum_{j=1}^{m}B_{m,j}(\tau^2)^2|Y_j-Y_j'|^2.
\]

Each complex harmonic gives two real sides of order \(\tau^{2j}\). The product of the first \(2j\) sides is \(\tau^{2j(j+1)}\); its squared quantization branch is \(\tau^{2(j+1)}M^{-1/j}\). At order \(2j+1\), the logarithmic branch is the convex combination of the neighboring even branches with weights \(j/(2j+1)\) and \((j+1)/(2j+1)\). The first odd branch is at most the order-two branch for \(M\ge1\). Thus no phase is missing. [S8]

Multiplying \(P\) by one new likelihood proves the printed weighted update directly. Its denominator equals the posterior expectation of \(f/a\), hence is at least \(1-\tau\), also for mixtures. At the next stage, a needed coordinate \(j+1\) is either stored at the previous future horizon or is zero because it exceeds the previous past degree. This is the indexing fact needed for a causal code. A3 then proves the maximum-checkpoint statement. At \(\tau=0\), the physical state is constant and the loss is zero. [S8, S13]

## A5. Nonconstant-history pullback and common-name overlap

For bounded tests \(\phi\) with posterior covariance \(\Gamma\), put

\[
f_v=v^T\Gamma^{-1}(\phi-\nu\phi).
\]

Then \(\nu f_v=0\) and \(\nu(\phi f_v)=v\). Uniform boundedness of \(f_v\) over a whole cube of \(v\)'s gives a simultaneous body inclusion, not just separate directional alternatives. To realize it by a *prior* perturbation at history likelihood \(\ell\), use

\[
d\mu'=\frac{1+s f_v}{1+s\mu f_v}\,d\mu.
\]

Since \(\nu f_v=0\), its posterior is exactly \((1+s f_v)\nu\). Small fixed-multiple \(s\) meets the relative prior envelope. The denominator cannot be omitted: the independent exact fixture has \(\mu f_v=-373217/141723\ne0\). This fixture is a regression illustration, not a new defect in the manuscript. [S9, S10; E]

For the common-name lower bound, \(\mu_\pm=(1\pm\epsilon f)\mu\) with \(\mu f=0\) gives

\[
\frac{d\mathsf P_\pm}{d\mathsf P_0}(h)=1\pm\epsilon\nu_hf,
\qquad
\nu_h^+q-\nu_h^-q
=\frac{2\epsilon\operatorname{Cov}_{\nu_h}(q,f)}
 {1-\epsilon^2(\nu_hf)^2}.
\]

The likelihood ratios are uniformly bounded below, not necessarily equal. A uniformly visible physical query and the interior prior-envelope/name slack then supply the \(\delta^2\) floor. Combining it with the memory lower bound through a maximum is equivalent to their sum up to constants. [S11]

For the upper bound, paired histories in two compatible experiments have close raw moments by subtraction of rational numerators and denominators, with evidence at least \(\kappa^n\). This bounds the Hausdorff distance of state sets and their covering radii. The common-advice construction uses the same numerical lists and stops on a common radius or precision floor. Its construction contract gives

\[
E_{n+1}\le L_nE_n+G_nh+r_{n+1}+2\tau,
\]

rather than merely measuring a potentially poor program's own residual. At the stopping scale \(h\asymp\min\{1,e(M)+\rho\}\), the single program achieves \(O(e(M)+\rho)\) prediction error for every compatible experiment. No unknown center is selected. This checks the analytic construction reduction, not all code-level implementation and bit-workspace claims. [S12]

## A6. A finite-command interpretation would be a different theorem

This is the basis of the wording correction E16.1, not a disproof of the formal model.

If the command alphabet has \(B\) elements and reports have five possibilities, encode a length-\(n\) history as its base-\(5B\) index. With a read-only clock, at most \((5B)^{N-1}\) states retain every prefix before the terminal horizon. Read-only model-dependent output tables then give the exact conditional probability for each future query. The worst-history and unconditional prediction losses are zero once this finite budget is reached.

For \(\tau>0\), the printed \(\mathcal H_{n,m}(M,\tau)\) is strictly positive at every finite \(M\). Therefore the theorem cannot be interpreted as using a fixed finite command alphabet. The actual continuously varying gate probabilities in the formal model avoid this contradiction. The phrase in the added comparison should say so. [S1:79–88; S8:18–55]

## A7. What the execution does and does not establish

`reproduce_review.py` is independent of author helper modules. It uses exact fractions for finite Leja inequalities, integrated confluent pairings, limiting Jacobian ranks, logarithmic profile identities, and prior perturbations. The full Laurent-update and query-metric checks are explicitly floating point; small absolute residuals do not establish relative accuracy near zero. Its 2,333 assertions separate 1,000 exact mathematical checks, 1,206 floating checks, and 127 integrity checks.

These finite checks do not prove a continuum-uniform inverse-function radius, arbitrary-prior positivity, a global covering theorem, minimax optimality, or novelty. Those matters require the analytic arguments above or, for significance and priority, an appropriately limited scholarly judgment. The execution receipt is not an author-suite rerun, a TeX build receipt, or a proof-assistant certificate.
