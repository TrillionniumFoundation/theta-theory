# Mathematical audit accompanying the A1 v12 report

All manuscript references concern commit `71907d83ba4eb235949e2a929b4b7f85349e96e5`. Evidence keys are defined in [SOURCE_INDEX.md](SOURCE_INDEX.md). This note records the arguments independently reconstructed in the review; it is not a certificate for every retained appendix.

## A1. What the intrinsic theorem actually classifies

At a checkpoint `n+m=N`, the formal future monomial labels have normalized exponent nodes `x_alpha=(alpha dot a)/H`. With `q_m` nonconstant formal labels and `p=min(n(r-1),q_m)`, the squared-regret profile is

\[
 \Psi_{n,m}(M,a)=\max_{1\le\ell\le p}
       \left(\frac{\mathcal V_{m,\ell}(a)}{M}\right)^{2/\ell},
 \qquad \Xi_N(M,a)=\max_{1\le n<N}\Psi_{n,N-n}(M,a).
\]

The following links were checked separately. [S2–S7]

**Physical test space.** Products of a fixed attainable failure-factor basis span the formal degree-m test space. A future-only continuation cannot inspect a discarded prefix. Every chosen probe uses its remaining m physical trials; unused hypothetical probes are not charged as executed trials. Squared-loss excess is the mean squared difference of actual conditional event probabilities.

**Attainable tangent.** For distinct small `c_i`, the factors `(1+c_i t^D)/2` give tangent monomials `jD` and `a+jD` with `0<a<D`. They are distinct, yielding `n(r-1)+1` directions. The polynomials `P/(1+c_i z)` span degree at most n-1 by evaluation at their distinct roots. This proves an equality of tangent spaces, not just an inclusion.

**Normalized rank.** The product belongs to that tangent. Writing `v=LP/(mu P)`, the derivative is `(mu P)^(-1)(LQ-v e_0 LQ)`. Since `e_0 v=1` and v lies in the image of L, the normalization loses exactly one rank. The resulting dimension is `min(n(r-1),|mA|-1)`. For the continuous-encoding upper bound, storing ordered normalized factors before a single switch to future moments avoids an unjustified global embedding of an arbitrary curved image into its intrinsic dimension.

**Confluence and uniformity.** Prefix divided differences span complete Hermite blocks, including nonadjacent repeated labels. For positive exponents bounded below by `a_*`, the functions `t^a(log t)^j` are bounded and extend continuously by zero at the origin. The zero-exponent constant is a single block. Strict confluent mixed pairing follows from an ordered evaluation determinant and determinant integration against the full-support prior. A density is not needed: finitely many separated positive intervals have positive mass. Finitely many label permutations and compactness give uniform row-singular-value bounds for the unscaled attainable flag.

**Probability lower bound.** Complete the derivative by kernel coordinates, use a uniform local inverse and integrate the kernel box. The acquisition law includes the all-failure probability, bounded below by a fixed positive number. No exact command is assigned a positive atom and no ambient flat ball is assumed.

**Global covering.** The entire scaled reachable image is described by bounded-degree polynomial relations in command variables, with strictly positive evidence. Prior integrals are real coefficients; their dependence on a need not be semialgebraic. Its dimension is at most p, and it lies in a rectangle with ordered widths proportional to the Leja pivots. A coefficient-independent section-component bound and the classical real entropy inequality give

\[
 \mathcal N(S,\varepsilon)\le C\sum_{j=0}^{p}
           \varepsilon^{-j}\prod_{i=1}^{j}a_i.
\]

The projection-volume estimate follows by expanding a projected rectangle as a zonotope. Almost all sections of codimension greater than p are empty. The separate small-M argument enforces the actual integer budget and replacement by reachable centres costs at most a factor two. Zhang–Kileel's version-specific regularity lemma was checked in the primary PDF; the additional entropy inequality is the classical input explicitly invoked in the manuscript, not a theorem proved from that lemma alone. [L2]

**Lower scale and causal compatibility.** Projection onto each first ell active coordinates of the minorized cube yields a rectangle with side product proportional to `d_1...d_ell`. M radius-b balls cover at most a constant times `M b^ell/(d_1...d_ell)` of its uniform mass. Taking the maximum over ell and using the Leja-product comparison gives the lower profile. Raw-moment posterior updates have positive denominators even along posterior-mixture segments. Updating a reachable representative remains feasible; subsequent quantization gives one causal filter. Each checkpoint lower bound uses a prefix of one common exploration law. These are distinct steps and were not inferred from the spectral identity alone.

**Assessment:** no blocking gap found in this examined chain. This is not an independent verification of every collision-tree specialization or later mechanical appendix.

## A2. Finite compilation, adaptive stopping and the new construction theorem

Let e(M) denote the largest unrestricted-centre covering radius of the true stage sets. For a fixed numerical list with total state error tau and history-net error `A h`, farthest-first gives

\[
 \max\{0,r/2-\tau\}\le e(M)\le r+A h+2\tau.
\]

The lower inequality uses M+1 separated numerical samples and an arbitrary true M-ball cover; it does not assume that the optimal centres are reachable. The upper inequality moves from an actual history to a grid history, a numerical sample, a selected numerical centre, and its actual representative. [S8]

For the original adaptive rule, `tau=h`, `c=A+2`, and `r>=4c h`. At a successful scale, the bracket implies `3r/8<=e<=5r/4`. Failure at the preceding scale gives `e<10c h` at the new scale; the successful lower bracket gives the opposite comparison. Thus the first successful h is comparable to e without requiring a collision decision. The comparison `e(M)^2 asymp Xi_N(M,a)` uses the previously established checkpoint law, not the adaptive conclusion; the proof is not circular.

For the new fixed-list construction, the appended representative history is already in the next candidate list. An independently checked nearest target is therefore at numerical distance at most `r_(n+1)`. Two evaluation errors give true distance at most `r_(n+1)+2 tau`. Hence

\[
 E_0=0,\quad E_{n+1}\le L_n E_n+G_n h+r_{n+1}+2\tau,
 \quad |\widehat Q_n-Q_n|\le K_n E_n+\tau.
\]

The initial state error is zero because the true representative of the empty history is the true initial state, even if its numerical name is imperfect. Approximate vectors are not passed to a true transition outside its domain. The theorem is valid under its stated error and horizon assumptions. The implementation mutations violate those assumptions while bypassing the gate; they do not invalidate the implication. [S9, X]

## A3. Finite-data stability and the prior envelope

Telescoping n report factors and then changing their finite moment entries gives numerator and evidence errors bounded by `D_n delta`, where

\[
 D_n=nJr(B+1)^{n-1}+(B+1)^n.
\]

For two true experiments with evidences `Z,Z'>=kappa^n` and raw conditional moments `q=A/Z`, `q'=A'/Z'` in [0,1],

\[
 |q-q'|\le\frac{|A-A'|+|q'|\,|Z-Z'|}{Z}
          \le2D_n\kappa^{-n}\delta.
\]

Pair identical histories in both directions to obtain Hausdorff distance at most `C delta`. Covering either set by the other's arbitrary centres then gives `|e_n(M)-e'_n(M)|<=C delta`, uniformly in M. This step does not require a common exponent-equality pattern. [S9]

For `D={mu:c_- mu_0<=mu<=c_+ mu_0}`, the measure inequalities are weakly closed on a compact space, and `c_->0` preserves full support. The relevant bounded complete-confluent functions depend continuously on calibration. Their determinant integrals remain positive uniformly, either by compactness or by domination of separated-interval products by `c_-^k mu_0^k`. Uniform local inverses and acquisition probabilities follow; the global semialgebraic format does not change when its moment coefficients change. This gives the stated family-uniform constants.

It is incorrect to criticize this lemma for promising uniformity over all full-support priors: it does not. The original fixed-prior classification remains separate. Combining the radius stability with the geometric equivalence yields the two inequalities for Xi with an added `delta^2` term. These are comparison inequalities, not an assertion that the displayed Xi function itself has a universal additive Lipschitz constant.

## A4. One common name: quantifiers and first-success calculation

For every compatible system, the **same** data at scale h have error `tau=max(h,rho)`. At the first stopping scale, tau is at most 2h: before crossing the floor tau=h, and the first dyadic crossing lies above rho/2. Put `c=A+4`. The shared radius therefore gives

\[
 \max(0,r/2-2h)\le e_{\mathcal E}(M)\le r+c h
\]

for each compatible system separately. If the preceding scale failed both tests, then

\[
 e_{\mathcal E}(M)<10c h,\qquad \rho<2h.
\]

If the radius test succeeds now, `4c h<=r<=2e+4h`, so `h<=e/(2c-2)`. Otherwise the floor test gives `h<=rho`. Together these give `h asymp min(1,e+rho)`, including the separately bounded initial stopping case. The construction recurrence then gives error `O(e+rho)` for every compatible system, using one table and no hidden model selection. Squaring and using uniform geometry gives `O(Xi_N+delta^2)` when `rho=2C_0 delta`. [S9]

This is why the theorem is sound and why its additional mechanism is a general perturbation-and-covering argument once the geometric comparison is known. Genericity of this mechanism does not erase the importance of proving that comparison for the actual positive experiments.

## A5. The physical uncertainty lower bound

For the detector

\[
 k_0=1/4,\qquad k_1=3/8+t/8,\qquad k_2=3/8-t/8,
\]

and priors with densities `1 +/- epsilon(2t-1)`, `epsilon=6delta<=1/2`,

\[
 m_k^\pm=\frac1{k+1}\pm\epsilon\frac{k}{(k+1)(k+2)}.
\]

The coefficient is at most 1/6 for every integer k>=0, so uniform-prior moments are common delta-accurate advice. Accepted cell 0 has likelihood `g_0/4`, constant in t. Conditional on this report, the joint command/history distributions agree and the posterior stays equal to the prior. Its probability is at least 1/16 for eta=1/4.

The displayed probe command gives rejection function `q(t)=1/2+t/32`. Since the two first moments differ by `epsilon/3=2delta`, the query gap is `delta/16`. Any common-advice prediction Y has the same distribution on those identical histories, and

\[
 \tfrac12\{\mathbb E(Y-q_-)^2+\mathbb E(Y-q_+)^2\}
 =\mathbb E(Y-(q_-+q_+)/2)^2+\delta^2/1024.
\]

Multiplying by the positive report mass and the fixed positive probe-selection probability gives an unconditional lower bound. The independent fixed-prior memory lower bound is `c M^-2`; combining two lower bounds by `max(x,y)>=(x+y)/2` gives the claimed sum order. The upper bound comes from the common-advice corollary. The attached script verifies the finite arithmetic for three delta values and moments k=0,...,32; the all-k statement follows analytically, not from that enumeration. [S9, X]

This proves a sharp uncertainty example without collisions. It is not a lower theorem for every colliding prior/calibration neighbourhood.

## A6. Exact arithmetic and the two executable contract failures

For a fixed rational circuit, numerator/denominator lengths grow at most by addition of operand lengths and fixed extra bits per gate; hence all intermediates have `O_fixed(b+1)` bits. For `x_b=(2^b-1)/2^b`, the numerator of `x_b^N` is odd, so its reduced denominator is exactly `2^(Nb)`. The corrected v12 wording is valid. [S8–S9]

For the precision diagnostic, the interval has length 1/4. M radius-e balls cover length at most 2Me, so `e>=1/(8M)`; equally spaced midpoint centres attain equality. The script's rational command grids really have radius at most h. With zero-bit ties-to-even rounding, its reachable samples lie in {0,1}; two centres give numerical radius zero even though the true two-centre radius is 1/16. At b=7, the routine's allowance is

\[
 0+(A+2)h=(5/2)/128=5/256<1/16.
\]

The checker has faithfully verified the wrong numerical scale. This is a false certificate produced after an accepted injected fault, not a failure of the mathematical radius inequality with its required total-error bound.

For the horizon diagnostic, use the complete finite command alphabet and A=0. A one-stage program and audit are internally consistent, but cannot implement the requested two-stage machine. The checker derives its enumeration horizon from the returned transition table, accepts the shorter object, and the second required lookup is absent. External specification binding is the common missing condition. [S10, X]
